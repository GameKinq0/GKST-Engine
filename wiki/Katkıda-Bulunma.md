# Katkıda Bulunma

GKST Engine projesine katkı vermek için teşekkürler! Bu kılavuz, nasıl katkıda bulunabileceğinizi anlatır.

## Başlamadan Önce

- Repository'yi [fork](https://github.com/GameKinq0/GKST_Engine/fork) edin
- Yerel makinenizde klonlayın
- Katkı kurallarımıza göz atın

## Katkı Türleri

### 1. Bug Reports

Bug bulduysanız:

1. [Issues](https://github.com/GameKinq0/GKST_Engine/issues) sayfasını kontrol edin (duplikasyon olmasın diye)
2. "New Issue" butonuna tıklayın
3. Aşağıdakileri ekleyin:
   - **Başlık**: Açık ve kısa
   - **Açıklama**: Neler yanlış gitti?
   - **Adımlar**: Hatayı yeniden oluşturmak için adımlar
   - **Beklenen Davranış**: Ne olması gerekiyordu?
   - **Gerçek Davranış**: Ne oldu?
   - **Ortam**: Python sürümü, OS, v.s.

### 2. Feature Requests

Yeni özellik önerisi yapmak istiyorsanız:

1. Issue açın
2. "enhancement" label'ı ekleyin
3. Açıkça anlatın:
   - Ne istiyorsunuz?
   - Neden gerekli?
   - Nasıl çalışmalı?

### 3. Code Contributions

### Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/KULLANICIADI/GKST_Engine.git
cd GKST_Engine

# Geliştirme ortamı oluşturun
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements-dev.txt
```

### Workflow

1. **Branch oluşturun**:
   ```bash
   git checkout -b feature/aciklayici-isim
   ```

2. **Kodunuzu yazın**:
   - Kod stili tutarlı tutun
   - Test yazın
   - Dokümantasyon ekleyin

3. **Commit edin**:
   ```bash
   git commit -am "Anlamlı commit mesajı"
   ```

4. **Push edin**:
   ```bash
   git push origin feature/aciklayici-isim
   ```

5. **Pull Request açın**:
   - Repository'ye gidin
   - "Compare & Pull Request" butonuna tıklayın
   - Açıklamasını yazın

## Kod Standartları

### Style Guide

- **Indentation**: 4 spaces
- **Line Length**: 79 characters
- **Naming**: snake_case for functions/variables, PascalCase for classes

### Örnek

```python
# Good
def calculate_distance(point1, point2):
    """Calculate distance between two points."""
    dx = point2.x - point1.x
    dy = point2.y - point1.y
    return (dx ** 2 + dy ** 2) ** 0.5

class Vector2:
    """2D Vector representation."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Bad
def calcDist(p1,p2):
    return ((p2.x-p1.x)**2+(p2.y-p1.y)**2)**0.5

class vec2:
    def __init__(self, x, y):
        self.x=x
        self.y=y
```

### Docstrings

```python
def function_name(param1, param2):
    """
    Kısa açıklama.
    
    Daha detaylı açıklama varsa buraya yazılır.
    
    Args:
        param1 (str): Parametrenin açıklaması
        param2 (int): Parametrenin açıklaması
        
    Returns:
        bool: Dönüş değerinin açıklaması
        
    Raises:
        ValueError: Ne zaman raise edilir?
    """
    pass
```

## Testing

Her kod değişikliği için test yazın:

```bash
# Testleri çalıştırın
python -m pytest

# Coverage raporu
python -m pytest --cov=gkst_engine
```

## Dokümantasyon

Yeni özellikler için wiki'yi güncelleyin:

- [API Referansı](./API-Referansı) - API değişiklikleri
- [Örnek Projeler](./Örnek-Projeler) - Yeni examples
- [SSS](./SSS) - Sık sorulan sorular

## Commit Mesajları

Anlamlı commit mesajları yazın:

```
# Good
- "Add Vector2 dot product method"
- "Fix memory leak in event handler"
- "Update documentation for Config class"

# Bad
- "fix"
- "changes"
- "asdasd"
```

## Pull Request Process

1. En son main branch'ı alın: `git pull upstream main`
2. Testlerin geçtiğini kontrol edin
3. Kodu review edin
4. PR açıklaması:
   - Ne yaptınız?
   - Neden yaptınız?
   - Related issues varsa linkleyin (#123)

## Davranış Kuralları

Lütfen:
- ✅ Saygılı olun
- ✅ Yapıcı geri bildirim verin
- ✅ Başkalarının zamanını değerlendirin

❌ Argo, hakaret içeren dil kullanmayın

## İletişim

- Sorular? [Discussions](https://github.com/GameKinq0/GKST_Engine/discussions)
- Öneriler? [Issues](https://github.com/GameKinq0/GKST_Engine/issues)

---

**Katkılarınız için teşekkürler! 🙏**
