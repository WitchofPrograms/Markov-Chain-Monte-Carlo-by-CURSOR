# Metropolis-Hastings Markov Chain Sampler

This project provides a Python script (`curAI.MARKOV`) that demonstrates the Metropolis-Hastings algorithm for Markov Chain Monte Carlo (MCMC) sampling. The script supports four different likelihood/prior combinations:

- **Gaussian (Normal) distribution**
- **Bernoulli distribution with Beta prior**
- **Beta distribution**
- **Poisson distribution with Gamma prior**

The script calculates the acceptance probability for a proposed new state using the Metropolis-Hastings formula and prints all relevant intermediate values.

## Requirements

- Python 3.x
- numpy
- scipy

Install dependencies with:

```
pip install numpy scipy
```

## Usage

Run the script from the command line, specifying the distribution and parameters as needed:

### Gaussian Example
```
python3 curAI.MARKOV --dist gaussian
```

### Bernoulli Example
```
python3 curAI.MARKOV --dist bernoulli --y 1 --x_t 0.7 --sigma 0.1 --a 2 --b 2
```

### Beta Example
```
python3 curAI.MARKOV --dist beta --y 0.5 --x_t 2.0 --sigma 0.2 --b 2
```

### Poisson Example
```
python3 curAI.MARKOV --dist poisson --y 3 --x_t 2.0 --sigma 0.5 --alpha 2 --beta_param 1
```

## Arguments
- `--dist`: Distribution type (`gaussian`, `bernoulli`, `beta`, `poisson`)
- `--y`: Observed value (float or int, depending on distribution)
- `--x_t`: Current value (float, probability, or parameter)
- `--sigma`: Proposal standard deviation
- `--a`, `--b`: Beta/Bernoulli prior parameters
- `--alpha`, `--beta_param`: Poisson prior parameters

## Output
The script prints:
- The proposed new value
- Likelihoods, priors, proposal probabilities for current and proposed states
- The acceptance probability `a`

## License
This project is for educational and demonstration purposes. 