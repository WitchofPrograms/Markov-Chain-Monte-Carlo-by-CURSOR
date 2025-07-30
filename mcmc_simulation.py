#!/usr/bin/env python3
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, bernoulli, poisson

# --- Utility functions for each distribution ---
def gaussian_likelihood(y, x):
    return math.exp(- (y - x) ** 2 / 2) / math.sqrt(2 * math.pi)

def gaussian_prior(x):
    return math.exp(- x ** 2 / 2) / math.sqrt(2 * math.pi)

def gaussian_proposal(x_from, x_to, sigma):
    return math.exp(- (x_from - x_to) ** 2 / (2 * sigma ** 2)) / (math.sqrt(2 * math.pi) * sigma)

def bernoulli_likelihood(y, p):
    # y: observed (0 or 1), p: probability
    return p if y == 1 else (1 - p)

def bernoulli_prior(p, a=1, b=1):
    # Beta prior for Bernoulli parameter
    return beta.pdf(p, a, b)

def bernoulli_proposal(p_from, p_to, sigma):
    # Propose new p from Normal(p_from, sigma), truncated to [0,1]
    if 0 <= p_to <= 1:
        return math.exp(- (p_from - p_to) ** 2 / (2 * sigma ** 2)) / (math.sqrt(2 * math.pi) * sigma)
    else:
        return 0.0

def beta_likelihood(y, a, b):
    # y: observed value in [0,1], a,b: beta parameters
    return beta.pdf(y, a, b)

def beta_prior(a, b):
    # Flat prior for demonstration (could use e.g. gamma prior)
    return 1.0

def beta_proposal(a_from, a_to, sigma):
    # Propose new a from Normal(a_from, sigma), truncated to >0
    if a_to > 0:
        return math.exp(- (a_from - a_to) ** 2 / (2 * sigma ** 2)) / (math.sqrt(2 * math.pi) * sigma)
    else:
        return 0.0

def poisson_likelihood(y, lam):
    return poisson.pmf(y, lam)

def poisson_prior(lam, alpha=1, beta_param=1):
    # Gamma prior for Poisson rate
    if lam > 0:
        return (beta_param ** alpha) * (lam ** (alpha - 1)) * math.exp(-beta_param * lam) / math.gamma(alpha)
    else:
        return 0.0

def poisson_proposal(lam_from, lam_to, sigma):
    # Propose new lambda from Normal(lam_from, sigma), truncated to >0
    if lam_to > 0:
        return math.exp(- (lam_from - lam_to) ** 2 / (2 * sigma ** 2)) / (math.sqrt(2 * math.pi) * sigma)
    else:
        return 0.0

# --- MCMC Simulation Functions ---
def metropolis_hastings_mcmc(dist, y, x0, sigma, steps, verbose=False, **kwargs):
    """
    Metropolis-Hastings MCMC simulation for different distributions
    
    Args:
        dist: distribution type ('gaussian', 'bernoulli', 'beta', 'poisson')
        y: observed value
        x0: initial value
        sigma: proposal standard deviation
        steps: number of MCMC steps
        verbose: whether to print acceptance rate
        **kwargs: additional parameters for specific distributions
    
    Returns:
        samples: list of MCMC samples
        acceptance_rate: acceptance rate of the chain
    """
    x_t = x0
    samples = []
    accepted = 0
    
    for i in range(steps):
        if dist == 'gaussian':
            x_star = x_t + np.random.normal(0, sigma)
            Lyx_star = gaussian_likelihood(y, x_star)
            Px_star = gaussian_prior(x_star)
            Qx_tx_star = gaussian_proposal(x_t, x_star, sigma)
            Lyxt = gaussian_likelihood(y, x_t)
            Pxt = gaussian_prior(x_t)
            Qx_starx_t = gaussian_proposal(x_star, x_t, sigma)
            
        elif dist == 'bernoulli':
            # x_t and x_star are probabilities in [0,1]
            x_star = x_t + np.random.normal(0, sigma)
            x_star = min(max(x_star, 0), 1)  # truncate to [0,1]
            Lyx_star = bernoulli_likelihood(y, x_star)
            Px_star = bernoulli_prior(x_star, kwargs.get('a',1), kwargs.get('b',1))
            Qx_tx_star = bernoulli_proposal(x_t, x_star, sigma)
            Lyxt = bernoulli_likelihood(y, x_t)
            Pxt = bernoulli_prior(x_t, kwargs.get('a',1), kwargs.get('b',1))
            Qx_starx_t = bernoulli_proposal(x_star, x_t, sigma)
            
        elif dist == 'beta':
            # x_t and x_star are 'a' parameters, b is fixed
            b = kwargs.get('b', 2)
            x_star = x_t + np.random.normal(0, sigma)
            x_star = max(x_star, 0.01)  # avoid zero or negative
            Lyx_star = beta_likelihood(y, x_star, b)
            Px_star = beta_prior(x_star, b)
            Qx_tx_star = beta_proposal(x_t, x_star, sigma)
            Lyxt = beta_likelihood(y, x_t, b)
            Pxt = beta_prior(x_t, b)
            Qx_starx_t = beta_proposal(x_star, x_t, sigma)
            
        elif dist == 'poisson':
            # x_t and x_star are lambda > 0
            x_star = x_t + np.random.normal(0, sigma)
            x_star = max(x_star, 0.01)
            Lyx_star = poisson_likelihood(y, x_star)
            Px_star = poisson_prior(x_star, kwargs.get('alpha',1), kwargs.get('beta_param',1))
            Qx_tx_star = poisson_proposal(x_t, x_star, sigma)
            Lyxt = poisson_likelihood(y, x_t)
            Pxt = poisson_prior(x_t, kwargs.get('alpha',1), kwargs.get('beta_param',1))
            Qx_starx_t = poisson_proposal(x_star, x_t, sigma)
        else:
            raise ValueError('Unknown distribution')

        # Calculate acceptance probability
        numerator = Lyx_star * Px_star * Qx_tx_star
        denominator = Lyxt * Pxt * Qx_starx_t
        a = min(1, numerator / denominator if denominator > 0 else 1)

        # Accept or reject
        u = np.random.uniform(0, 1)
        if u < a:
            x_t = x_star
            accepted += 1

        samples.append(x_t)
        
        # Print progress every 1000 steps
        if verbose and (i + 1) % 1000 == 0:
            print(f"Step {i + 1}/{steps}, Current value: {x_t:.4f}, Acceptance rate: {accepted/(i+1):.3f}")

    acceptance_rate = accepted / steps
    if verbose:
        print(f"\nFinal acceptance rate: {acceptance_rate:.3f}")
    
    return samples, acceptance_rate

def plot_mcmc_results(samples, dist_name, y_value, burn_in=0):
    """
    Plot MCMC results including trace plot and histogram
    """
    # Remove burn-in period
    samples_clean = samples[burn_in:]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Trace plot
    ax1.plot(samples_clean, alpha=0.7)
    ax1.set_title(f'{dist_name.capitalize()} MCMC Trace Plot')
    ax1.set_xlabel('Step')
    ax1.set_ylabel('Parameter Value')
    ax1.grid(True, alpha=0.3)
    
    # Histogram
    ax2.hist(samples_clean, bins=50, density=True, alpha=0.7, edgecolor='black')
    ax2.set_title(f'{dist_name.capitalize()} MCMC Histogram')
    ax2.set_xlabel('Parameter Value')
    ax2.set_ylabel('Density')
    ax2.grid(True, alpha=0.3)
    
    # Add some statistics
    mean_val = np.mean(samples_clean)
    std_val = np.std(samples_clean)
    ax2.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.3f}')
    ax2.axvline(mean_val + std_val, color='orange', linestyle=':', label=f'±1σ: {std_val:.3f}')
    ax2.axvline(mean_val - std_val, color='orange', linestyle=':')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Print summary statistics
    print(f"\n{dist_name.capitalize()} MCMC Summary Statistics:")
    print(f"Observed value (y): {y_value}")
    print(f"Mean: {mean_val:.4f}")
    print(f"Std: {std_val:.4f}")
    print(f"95% CI: [{np.percentile(samples_clean, 2.5):.4f}, {np.percentile(samples_clean, 97.5):.4f}]")
    print(f"Min: {np.min(samples_clean):.4f}")
    print(f"Max: {np.max(samples_clean):.4f}")

# --- Example usage and testing ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MCMC simulation for different distributions.")
    parser.add_argument('--dist', choices=['gaussian','bernoulli','beta','poisson'], default='gaussian', help='Distribution type')
    parser.add_argument('--y', type=float, default=2.5, help='Observed value')
    parser.add_argument('--x0', type=float, default=1.0, help='Initial value')
    parser.add_argument('--sigma', type=float, default=0.5, help='Proposal stddev')
    parser.add_argument('--steps', type=int, default=10000, help='Number of MCMC steps')
    parser.add_argument('--burn_in', type=int, default=1000, help='Burn-in period')
    parser.add_argument('--verbose', action='store_true', help='Print progress')
    parser.add_argument('--plot', action='store_true', help='Show plots')
    parser.add_argument('--a', type=float, default=1.0, help='Beta/Bernoulli prior a')
    parser.add_argument('--b', type=float, default=2.0, help='Beta/Bernoulli prior b')
    parser.add_argument('--alpha', type=float, default=1.0, help='Poisson prior alpha')
    parser.add_argument('--beta_param', type=float, default=1.0, help='Poisson prior beta')
    args = parser.parse_args()

    print(f"Running MCMC for {args.dist} distribution...")
    print(f"Parameters: y={args.y}, x0={args.x0}, sigma={args.sigma}, steps={args.steps}")
    
    # Run MCMC
    if args.dist == 'gaussian':
        samples, acc_rate = metropolis_hastings_mcmc('gaussian', args.y, args.x0, args.sigma, args.steps, args.verbose)
    elif args.dist == 'bernoulli':
        samples, acc_rate = metropolis_hastings_mcmc('bernoulli', int(args.y), args.x0, args.sigma, args.steps, args.verbose, a=args.a, b=args.b)
    elif args.dist == 'beta':
        samples, acc_rate = metropolis_hastings_mcmc('beta', args.y, args.x0, args.sigma, args.steps, args.verbose, b=args.b)
    elif args.dist == 'poisson':
        samples, acc_rate = metropolis_hastings_mcmc('poisson', int(args.y), args.x0, args.sigma, args.steps, args.verbose, alpha=args.alpha, beta_param=args.beta_param)
    
    print(f"\nMCMC completed!")
    print(f"Acceptance rate: {acc_rate:.3f}")
    
    if args.plot:
        plot_mcmc_results(samples, args.dist, args.y, args.burn_in)
    
    # Save samples to file
    output_file = f"mcmc_samples_{args.dist}.txt"
    np.savetxt(output_file, samples)
    print(f"Samples saved to {output_file}") 