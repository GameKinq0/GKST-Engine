# Örnek Projeler

GKST Engine ile oluşturulmuş örnek projeler ve kod örnekleri.

## Örnek 1: Basit Uygulama

```python
from gkst_engine import Engine, Config

# Konfigürasyon
config = Config(
    app_name="Basit Uygulama",
    debug=True,
    width=800,
    height=600
)

# Engine oluştur
engine = Engine(config=config)

# Uygulamayı başlat
engine.run()
```

## Örnek 2: Event Handling

```python
from gkst_engine import Engine, event_handler

engine = Engine()

@event_handler("on_update")
def on_update(delta_time):
    print(f"Delta time: {delta_time}s")

@event_handler("on_render")
def on_render():
    print("Rendering...")

engine.run()
```

## Örnek 3: Vektör Matematikleri

```python
from gkst_engine.utils import Vector2

# Vektör oluştur
pos1 = Vector2(10, 20)
pos2 = Vector2(30, 40)

# İşlemler
distance = pos1.distance_to(pos2)
direction = (pos2 - pos1).normalized()
speed = direction * 5.0

print(f"Distance: {distance}")
print(f"Direction: {direction}")
print(f"Speed: {speed}")
```

## Örnek 4: Component Sistemi

```python
from gkst_engine import component, Engine

@component
class Transform:
    def __init__(self):
        self.position = (0, 0)
        self.rotation = 0

@component
class Renderer:
    def __init__(self):
        self.color = (255, 255, 255)

# Kullanımı
engine = Engine()
engine.run()
```

## Örnek 5: Logger Kullanımı

```python
from gkst_engine import Logger

logger = Logger(__name__)

logger.info("Uygulama başlıyor")
logger.debug("Debug bilgisi")
logger.warning("Uyarı: Düşük hafıza")
logger.error("Hata: Dosya bulunamadı")
```

## Örnek 6: Hata Yönetimi

```python
from gkst_engine import Engine
from gkst_engine.exceptions import EngineError, ConfigError

try:
    config = Config(width=-100)  # Geçersiz
    engine = Engine(config=config)
    engine.run()
except ConfigError as e:
    print(f"Konfigürasyon hatası: {e}")
except EngineError as e:
    print(f"Engine hatası: {e}")
except Exception as e:
    print(f"Beklenmeyen hata: {e}")
```

## Örnek Proje: Basit Oyun

```python
from gkst_engine import Engine, Config, event_handler
from gkst_engine.utils import Vector2

config = Config(
    app_name="Basit Oyun",
    fps=60,
    width=1024,
    height=768
)

engine = Engine(config=config)
player_pos = Vector2(512, 400)
game_running = True

@event_handler("on_update")
def game_update(delta_time):
    global player_pos
    # Oyun lojiği burada
    player_pos.x += 1 * delta_time

@event_handler("on_render")
def game_render():
    # Render lojiği burada
    pass

@event_handler("on_input")
def game_input(key):
    global game_running
    if key == "ESC":
        game_running = False

if __name__ == "__main__":
    engine.run()
```

## Kaynaklar

- [API Referansı](./API-Referansı)
- [Başlangıç Rehberi](./Başlangıç-Rehberi)
- [GitHub Repository](https://github.com/GameKinq0/GKST_Engine)
