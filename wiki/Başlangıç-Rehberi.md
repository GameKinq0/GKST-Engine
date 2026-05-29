# Başlangıç Rehberi

GKST Engine ile ilk projenizi başlatmaya hoşgeldiniz!

## Ön Koşullar

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- Temel Python bilgisi

## Adım 1: Kurulum

```bash
pip install gkst-engine
```

Veya repository'den yüklemek için:

```bash
git clone https://github.com/GameKinq0/GKST_Engine.git
cd GKST_Engine
python setup.py install
```

## Adım 2: İlk Projenizi Oluşturun

```python
from gkst_engine import Engine

# Engine örneği oluşturun
engine = Engine()

# Uygulamanızı başlatın
engine.run()
```

## Adım 3: Temel Yapılandırma

```python
from gkst_engine import Engine, Config

# Özel konfigürasyon
config = Config(
    app_name="Benim Uygulamam",
    debug=True,
    log_level="INFO"
)

engine = Engine(config=config)
engine.run()
```

## Sonraki Adımlar

- **[API Referansı](./API-Referansı)** - Tüm API'ler hakkında bilgi edinin
- **[Örnek Projeler](./Örnek-Projeler)** - Pratik örnekleri inceleyin
- **[Sorun Giderme](./Sorun-Giderme)** - Yaygın sorunlar ve çözümler

## Yardım ve Destek

Sorularınız veya sorunlarınız varsa:
- [Issues](https://github.com/GameKinq0/GKST_Engine/issues) açın
- [Discussions](https://github.com/GameKinq0/GKST_Engine/discussions) kısmında sorgular sorun
