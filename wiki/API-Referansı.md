# API Referansı

GKST Engine'in eksiksiz API dokümantasyonu.

## Temel Sınıflar

### Engine

Ana engine sınıfı.

```python
from gkst_engine import Engine

engine = Engine(config=None)
```

#### Metodlar

| Metod | Açıklama |
|-------|----------|
| `run()` | Engine'i başlat |
| `stop()` | Engine'i durdur |
| `update(delta_time)` | Engine'i güncelle |
| `render()` | Ekranı render et |

### Config

Konfigürasyon sınıfı.

```python
from gkst_engine import Config

config = Config(
    app_name="Uygulamam",
    debug=False,
    log_level="INFO"
)
```

#### Parametreler

| Parametre | Tür | Varsayılan | Açıklama |
|-----------|-----|-----------|----------|
| `app_name` | str | "GKST App" | Uygulama adı |
| `debug` | bool | False | Debug modu |
| `log_level` | str | "INFO" | Log seviyesi |
| `fps` | int | 60 | Kare hızı |
| `width` | int | 800 | Pencere genişliği |
| `height` | int | 600 | Pencere yüksekliği |

### Logger

Logging sistemi.

```python
from gkst_engine import Logger

logger = Logger(__name__)

logger.info("Bilgi mesajı")
logger.warning("Uyarı mesajı")
logger.error("Hata mesajı")
logger.debug("Debug mesajı")
```

## Dekoratörler

### @event_handler

Event işleyici dekoratörü.

```python
from gkst_engine import event_handler

@event_handler("on_update")
def handle_update(delta_time):
    pass
```

### @component

Component dekoratörü.

```python
from gkst_engine import component

@component
class MyComponent:
    def __init__(self):
        self.value = 0
```

## Utilities

### Vector2

2D vektör sınıfı.

```python
from gkst_engine.utils import Vector2

v1 = Vector2(10, 20)
v2 = Vector2(5, 15)

result = v1 + v2  # Vector2(15, 35)
distance = v1.distance_to(v2)
```

### Color

Renk sınıfı.

```python
from gkst_engine.utils import Color

red = Color(255, 0, 0)
blue = Color(0, 0, 255)
```

## Sabitler

```python
from gkst_engine import constants

constants.MAX_ENTITIES  # Maksimum entity sayısı
constants.DEFAULT_FPS   # Varsayılan FPS
```

## Hata Yönetimi

```python
from gkst_engine.exceptions import (
    EngineError,
    ConfigError,
    RenderError
)

try:
    engine.run()
except EngineError as e:
    print(f"Engine hatası: {e}")
except ConfigError as e:
    print(f"Config hatası: {e}")
```

## Daha Fazla Bilgi

- [Başlangıç Rehberi](./Başlangıç-Rehberi)
- [Örnek Projeler](./Örnek-Projeler)
- [GitHub Issues](https://github.com/GameKinq0/GKST_Engine/issues)
