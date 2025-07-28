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

## Conversation History

Below is the conversation that led to the creation and usage of this script:

---

**User:**
Markov Chain formula a = min(1,(Yeni Noktanın İhtimali / Mevcut Noktanın İhtimali) * (Mevcuttan Yeniye Öneri Olasılığı / Yeniden Mevcuda Öneri Olasılığı))

a=min(1, L(y∣(x^*)) * P(x^*) * Q(xt∣x^*) / L(y∣xt) * P(xt) * Q(x^*∣xt)
xt = mevcut  nokta
x^* = yeni nokta
L(y/x) = x noktasındaki(xt/x^*) veriye karşılık gelen olasılık likelihood
P(x) = x noktasındaki öncelik ihtimali(prior)
Q(x^*/xt) = şuanki noktadan yeni noktaya geçiş öneri olasılığı
Q(xt/x^*) = tersi
a = min(1, (yeni noktasındaki veriye karşılık gelen olasılık * yeni noktasındaki öncelik ihtimali * yeni noktadan şuanki noktaya geçiş öneri olasılığı) /(mevcut noktasındaki veriye karşılık gelen olasılık * mevcut noktasındaki öncelik ihtimali * mevcut noktadan yeni noktaya geçiş öneri olasılığı )
Eğer öneri dağılımı simetrikse (Q(x^*/xt) =  Q(xt/x^*)) ise denklem sadeleşir
x^* = xt + Normal(0,σ^2) genelikle bu şekilde seçilir
L(y∣x) = e^( -(y - x)^2 / 2) / √(2π) = P(y)/P(x)

import math
import numpy as np
y = 2.5;
x_t = 1.0;        # mevcut değer
sigma = 0.5;     # adım büyüklüğü

x_star = x_t + np.random.normal(0, sigma);
Lyx_star = math.exp(- math.pow(y - x_star, 2) / 2) / math.sqrt(2 * math.pi)
Px_star = math.exp(- math.pow(x_star, 2) / 2) / math.sqrt(2 * math.pi)
Qx_tx_star = math.exp(- math.pow(x_t - x_star, 2) / (2 * math.pow(sigma,2))) / (math.sqrt(2 * math.pi) * sigma)
Lyxt = math.exp(- math.pow(y - x_t, 2) / 2) / math.sqrt(2 * math.pi)
Pxt = math.exp(- math.pow(x_t, 2) / 2) / math.sqrt(2 * math.pi)
Qx_starx_t = math.exp(- math.pow(x_star - x_t, 2) / (2 * math.pow(sigma,2))) / (math.sqrt(2 * math.pi) * sigma)
a = min(1,(Lyx_star * Px_star * Qx_tx_star/(Lyxt * Pxt * Qx_starx_t)))

print(f"Yeni öneri: {x_star}");
print(f"L(y/(x^*)):{Lyx_star}")
print(f"P(x^*)):{Px_star}")
print(f"Q(xt∣x^*):{Qx_tx_star}")
print(f"L(y∣xt):{Lyxt}")
print(f"P(xt):{Pxt}")
print(f"Q(x^*∣xt):{Qx_starx_t}")
print(f"a:{a}")

build 1 python file which can calculate this markov calculations but not just using Gaussian method I want bernoulli Beta and Poisson too so make 4 of them in 1 code

**Assistant:**
Your file `projeler/markovcur/curAI.MARKOV` is now a Python script that can perform the Metropolis-Hastings acceptance probability calculation for four different likelihood/prior combinations: Gaussian, Bernoulli, Beta, and Poisson.

**User:**
create a readme file and   python3 curAI.MARKOV --dist gaussian
  python3 curAI.MARKOV --dist bernoulli --y 1 --x_t 0.7 --sigma 0.1 --a 2 --b 2
  python3 curAI.MARKOV --dist beta --y 0.5 --x_t 2.0 --sigma 0.2 --b 2
  python3 curAI.MARKOV --dist poisson --y 3 --x_t 2.0 --sigma 0.5 --alpha 2 --beta_param 1

**Assistant:**
A `README.md` file has been created in `projeler/markovcur/` with:
- A summary of what the script does
- Installation instructions
- Usage examples for all four distributions
- Argument explanations and output description.

**User:**
add our conversations too in README.md

**Assistant:**
(You are reading this section now!)

--- 