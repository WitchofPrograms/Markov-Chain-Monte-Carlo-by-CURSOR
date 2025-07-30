#!/usr/bin/env python3
"""
Basit MCMC test dosyası
Bu dosya MCMC simülasyonunu test etmek için kullanılır.
"""

from mcmc_simulation import metropolis_hastings_mcmc, plot_mcmc_results
import numpy as np

def test_gaussian_mcmc():
    """Gaussian dağılım için MCMC testi"""
    print("=== Gaussian MCMC Testi ===")
    
    # Parametreler
    y = 2.5  # gözlemlenen değer
    x0 = 1.0  # başlangıç değeri
    sigma = 0.5  # proposal standart sapması
    steps = 5000  # MCMC adım sayısı
    
    print(f"Gözlemlenen değer (y): {y}")
    print(f"Başlangıç değeri (x0): {x0}")
    print(f"Proposal sigma: {sigma}")
    print(f"MCMC adımları: {steps}")
    
    # MCMC çalıştır
    samples, acceptance_rate = metropolis_hastings_mcmc(
        'gaussian', y, x0, sigma, steps, verbose=True
    )
    
    print(f"\nKabul oranı: {acceptance_rate:.3f}")
    
    # Sonuçları görselleştir
    plot_mcmc_results(samples, 'gaussian', y, burn_in=500)
    
    return samples

def test_bernoulli_mcmc():
    """Bernoulli dağılım için MCMC testi"""
    print("\n=== Bernoulli MCMC Testi ===")
    
    # Parametreler
    y = 1  # gözlemlenen değer (0 veya 1)
    x0 = 0.5  # başlangıç olasılığı
    sigma = 0.1  # proposal standart sapması (küçük tutuyoruz çünkü [0,1] aralığında)
    steps = 5000
    
    print(f"Gözlemlenen değer (y): {y}")
    print(f"Başlangıç olasılığı (x0): {x0}")
    print(f"Proposal sigma: {sigma}")
    
    # MCMC çalıştır
    samples, acceptance_rate = metropolis_hastings_mcmc(
        'bernoulli', y, x0, sigma, steps, verbose=True
    )
    
    print(f"\nKabul oranı: {acceptance_rate:.3f}")
    
    # Sonuçları görselleştir
    plot_mcmc_results(samples, 'bernoulli', y, burn_in=500)
    
    return samples

def test_poisson_mcmc():
    """Poisson dağılım için MCMC testi"""
    print("\n=== Poisson MCMC Testi ===")
    
    # Parametreler
    y = 3  # gözlemlenen sayı
    x0 = 2.0  # başlangıç lambda değeri
    sigma = 0.3  # proposal standart sapması
    steps = 5000
    
    print(f"Gözlemlenen sayı (y): {y}")
    print(f"Başlangıç lambda (x0): {x0}")
    print(f"Proposal sigma: {sigma}")
    
    # MCMC çalıştır
    samples, acceptance_rate = metropolis_hastings_mcmc(
        'poisson', y, x0, sigma, steps, verbose=True
    )
    
    print(f"\nKabul oranı: {acceptance_rate:.3f}")
    
    # Sonuçları görselleştir
    plot_mcmc_results(samples, 'poisson', y, burn_in=500)
    
    return samples

def quick_test():
    """Hızlı test - sadece Gaussian için"""
    print("=== Hızlı Gaussian MCMC Testi ===")
    
    samples, acc_rate = metropolis_hastings_mcmc(
        'gaussian', y=2.5, x0=1.0, sigma=0.5, steps=1000, verbose=False
    )
    
    print(f"Kabul oranı: {acc_rate:.3f}")
    print(f"Ortalama: {np.mean(samples):.4f}")
    print(f"Standart sapma: {np.std(samples):.4f}")
    
    # Basit histogram
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 6))
    plt.hist(samples, bins=30, density=True, alpha=0.7, edgecolor='black')
    plt.title('Gaussian MCMC Histogram')
    plt.xlabel('Parameter Value')
    plt.ylabel('Density')
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    # Hangi testi çalıştırmak istediğinizi seçin
    print("MCMC Test Seçenekleri:")
    print("1. Hızlı Gaussian test (1000 adım)")
    print("2. Detaylı Gaussian test (5000 adım)")
    print("3. Bernoulli test")
    print("4. Poisson test")
    print("5. Tüm testler")
    
    choice = input("\nSeçiminizi yapın (1-5): ").strip()
    
    if choice == '1':
        quick_test()
    elif choice == '2':
        test_gaussian_mcmc()
    elif choice == '3':
        test_bernoulli_mcmc()
    elif choice == '4':
        test_poisson_mcmc()
    elif choice == '5':
        test_gaussian_mcmc()
        test_bernoulli_mcmc()
        test_poisson_mcmc()
    else:
        print("Geçersiz seçim. Hızlı test çalıştırılıyor...")
        quick_test() 