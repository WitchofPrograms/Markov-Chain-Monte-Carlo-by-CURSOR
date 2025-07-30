# MCMC (Markov Chain Monte Carlo) Simülasyonu

Bu proje, Metropolis-Hastings algoritmasını kullanarak farklı dağılımlar için MCMC simülasyonu yapar.

## Dosyalar

- `mcmc_simulation.py`: Ana MCMC simülasyon kodu
- `test_mcmc.py`: Test dosyası
- `curAI.MARKOV`: Orijinal tek adım Metropolis-Hastings kodu

## Kurulum

Gerekli kütüphaneler:
```bash
pip install numpy scipy matplotlib
```

## Kullanım

### 1. Komut Satırından Kullanım

```bash
# Gaussian dağılım için MCMC
python mcmc_simulation.py --dist gaussian --y 2.5 --x0 1.0 --sigma 0.5 --steps 10000 --plot

# Bernoulli dağılım için MCMC
python mcmc_simulation.py --dist bernoulli --y 1 --x0 0.5 --sigma 0.1 --steps 10000 --plot

# Poisson dağılım için MCMC
python mcmc_simulation.py --dist poisson --y 3 --x0 2.0 --sigma 0.3 --steps 10000 --plot
```

### 2. Python Kodundan Kullanım

```python
from mcmc_simulation import metropolis_hastings_mcmc, plot_mcmc_results

# Gaussian MCMC
samples, acc_rate = metropolis_hastings_mcmc(
    'gaussian', y=2.5, x0=1.0, sigma=0.5, steps=10000, verbose=True
)

# Sonuçları görselleştir
plot_mcmc_results(samples, 'gaussian', 2.5, burn_in=1000)
```

### 3. Test Dosyası ile Kullanım

```bash
python test_mcmc.py
```

## Parametreler

### Genel Parametreler
- `dist`: Dağılım türü ('gaussian', 'bernoulli', 'beta', 'poisson')
- `y`: Gözlemlenen değer
- `x0`: Başlangıç değeri
- `sigma`: Proposal standart sapması
- `steps`: MCMC adım sayısı
- `burn_in`: Burn-in periyodu (görselleştirme için)

### Dağılım Özel Parametreleri

#### Gaussian
- Standart normal prior ve likelihood

#### Bernoulli
- `a`, `b`: Beta prior parametreleri (varsayılan: a=1, b=1)
- `y`: 0 veya 1 olmalı
- `x0`: [0,1] aralığında olmalı

#### Beta
- `b`: Beta dağılımının b parametresi (varsayılan: 2)
- `y`: [0,1] aralığında olmalı
- `x0`: > 0 olmalı

#### Poisson
- `alpha`, `beta_param`: Gamma prior parametreleri (varsayılan: 1, 1)
- `y`: Tam sayı olmalı
- `x0`: > 0 olmalı

## Çıktılar

1. **Kabul Oranı**: MCMC zincirinin kabul oranı (ideal: %20-50)
2. **Trace Plot**: Parametrenin zaman içindeki değişimi
3. **Histogram**: Parametrenin posterior dağılımı
4. **İstatistikler**: Ortalama, standart sapma, güven aralıkları
5. **Dosya**: Örnekler `mcmc_samples_[dist].txt` dosyasına kaydedilir

## Örnekler

### Gaussian MCMC
```python
# y=2.5 gözlemlendiğinde, x'in posterior dağılımını bul
samples, acc_rate = metropolis_hastings_mcmc(
    'gaussian', y=2.5, x0=1.0, sigma=0.5, steps=10000
)
```

### Bernoulli MCMC
```python
# y=1 gözlemlendiğinde, başarı olasılığının posterior dağılımını bul
samples, acc_rate = metropolis_hastings_mcmc(
    'bernoulli', y=1, x0=0.5, sigma=0.1, steps=10000
)
```

### Poisson MCMC
```python
# y=3 gözlemlendiğinde, lambda parametresinin posterior dağılımını bul
samples, acc_rate = metropolis_hastings_mcmc(
    'poisson', y=3, x0=2.0, sigma=0.3, steps=10000
)
```

## İpuçları

1. **Proposal Sigma**: Çok büyükse kabul oranı düşük olur, çok küçükse zincir yavaş hareket eder
2. **Burn-in**: İlk birkaç yüz adımı atın, zincir henüz kararlı değildir
3. **Adım Sayısı**: En az 1000 adım önerilir, daha iyi sonuçlar için 10000+
4. **Kabul Oranı**: %20-50 arası ideal, %10'dan az veya %80'den fazla ise sigma'yı ayarlayın

## Teorik Arka Plan

Metropolis-Hastings algoritması:
1. Mevcut durumdan yeni bir öneri üret
2. Kabul olasılığını hesapla: `min(1, (likelihood × prior × proposal) / (current_likelihood × current_prior × reverse_proposal))`
3. Rastgele sayı üret ve kabul et/reddet
4. Yeni durumu kaydet ve tekrarla

Bu süreç, hedef posterior dağılımdan örnekler üretir. 