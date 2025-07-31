# Otomatik Sigma Ayarı: --auto_sigma Kullanımı

Bu doküman, acceptance rate'i (kabul oranı) istenen aralığa getirmek için sigma parametresini otomatik ayarlayan `--auto_sigma` özelliğinin kullanımını açıklar.

## Özellik Nedir?

`--auto_sigma` parametresi, MCMC simülasyonunda sigma değerini otomatik olarak ayarlayarak kabul oranını (acceptance rate) 0.25 ile 0.35 aralığına getirmeye çalışır. Böylece el ile deneme yapmadan, zincirin verimli çalışmasını sağlayan bir sigma değeri bulunur.

## Kullanım

### Gaussian Dağılımı İçin
```bash
python3 mcmc_simulation.py --dist gaussian --y 2.5 --x0 1.0 --steps 1000 --auto_sigma
```

### Bernoulli Dağılımı İçin
```bash
python3 mcmc_simulation.py --dist bernoulli --y 1 --x0 0.5 --steps 1000 --auto_sigma --a 2 --b 2
```

### Beta Dağılımı İçin
```bash
python3 mcmc_simulation.py --dist beta --y 0.5 --x0 2.0 --steps 1000 --auto_sigma --b 2
```

### Poisson Dağılımı İçin
```bash
python3 mcmc_simulation.py --dist poisson --y 3 --x0 2.0 --steps 1000 --auto_sigma --alpha 2 --beta_param 1
```

## Ne Yapar?
- Farklı sigma değerleriyle kısa MCMC zincirleri çalıştırır.
- Her sigma için acceptance rate hesaplar.
- Acceptance rate 0.25–0.35 aralığına girene kadar sigma'yı otomatik ayarlar.
- Uygun sigma bulunduğunda, bu değeri kullanarak asıl MCMC simülasyonunu başlatır.

## Çıktı Örneği
```
Deneme 1: sigma=0.5000, acceptance rate=0.620
Deneme 2: sigma=0.6500, acceptance rate=0.480
Deneme 3: sigma=0.8450, acceptance rate=0.320
Uygun sigma bulundu: sigma=0.8450, acceptance rate=0.320
Kullanılacak sigma: 0.8450 (acceptance rate: 0.320)

MCMC completed!
Acceptance rate: 0.319
Samples saved to mcmc_samples_gaussian.txt
```

## Parametreler
- `--auto_sigma` : Otomatik sigma ayarı başlatılır.
- `--steps` : Her denemede ve asıl simülasyonda kullanılacak adım sayısı (ör. 1000 veya 10000 önerilir).
- Diğer parametreler: Dağılıma göre (ör. `--a`, `--b`, `--alpha`, `--beta_param`)

## Notlar
- Otomatik ayar, zincirin verimli çalışmasını sağlar ve elle deneme ihtiyacını ortadan kaldırır.
- Hedef aralığa ulaşılamazsa, en yakın acceptance rate'e sahip sigma değeri seçilir ve uyarı verilir.
- Daha uzun zincirler (daha yüksek `--steps`) daha güvenilir acceptance rate ölçümü sağlar.

## Teorik Arka Plan
- Acceptance rate'in ideal aralığı genellikle 0.2–0.5 arasıdır. Bu kodda 0.25–0.35 aralığı hedeflenmiştir.
- Çok düşük acceptance rate: Zincir yavaş hareket eder, örnekler bağımlı olur.
- Çok yüksek acceptance rate: Zincir çok küçük adımlar atar, karışım yavaş olur.

---
Daha fazla bilgi için ana dokümantasyon dosyalarına bakabilirsiniz. 