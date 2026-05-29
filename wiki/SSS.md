# Sık Sorulan Sorular (SSS)

## Genel Sorular

### GKST Engine nedir?

GKST Engine, Python tabanlı, hafif ve hızlı bir application framework'üdür. Oyun geliştirmesi, görselleştirme ve diğer interactive uygulamalar için tasarlanmıştır.

### Hangi Python sürümüne ihtiyaç duyuyorum?

Python 3.8 veya üzeri gereklidir.

### GKST Engine ücretsiz midir?

Evet! GKST Engine MIT Lisansı altında ücretsiz ve açık kaynaklıdır.

### Windows/macOS/Linux'ta çalışır mı?

Evet, GKST Engine tüm ana platformlarda çalışır.

## Kurulum ve Setup

### Kurulum sırasında "permission denied" hatası alıyorum

Yönetici modunda çalıştırmayı deneyin veya virtual environment kullanın:

```bash
python -m venv venv
source venv/bin/activate  # veya venv\Scripts\activate (Windows)
pip install gkst-engine
```

### Nasıl kaynaktan yükleyebilirim?

```bash
git clone https://github.com/GameKinq0/GKST_Engine.git
cd GKST_Engine
python setup.py install
```

### Virtual environment neden önemlidir?

Virtual environment, proje bağımlılıklarını izole eder ve sistem Python'u ile çakışmasını önler.

## Kullanım ve Geliştirme

### İlk projeyi nasıl başlatırım?

```python
from gkst_engine import Engine

engine = Engine()
engine.run()
```

Daha detaylı bilgi için [Başlangıç Rehberi](./Başlangıç-Rehberi) bölümüne bakın.

### Component nedir?

Component, engine'in modüler yapısını oluşturan bileşenleridir. Reusable ve independent fonksiyonaliteleri temsil ederler.

### Event handling nasıl çalışır?

```python
from gkst_engine import event_handler

@event_handler("on_update")
def handle_update(delta_time):
    print(f"Güncelleme: {delta_time}s")
```

### Debug modu nasıl etkinleştirilir?

```python
from gkst_engine import Config, Engine

config = Config(debug=True)
engine = Engine(config=config)
engine.run()
```

## Sorun Giderme

### "ModuleNotFoundError: No module named 'gkst_engine'" hatası

Engine'in yüklü olmadığını anlamına gelir. Kurulum yapın:

```bash
pip install gkst-engine
```

### Uygulama açılmıyor

- Python sürümünü kontrol edin (3.8+)
- Log dosyalarını kontrol edin
- Hata mesajını kopyalayıp [Issues](https://github.com/GameKinq0/GKST_Engine/issues) açın

### Düşük FPS problemi

- Config'de FPS ayarını kontrol edin
- Gereksiz işlemleri optimize edin
- İşlemci kullanımını azaltmayı deneyin

### Bellek sızıntısı yaşıyorum

- Event handler'ları düzgün kaydetmiş olduğunuzdan emin olun
- Kaynakları temizleyin

## Katkıda Bulunma

### Projede nasıl çalışabilirim?

1. Repository'yi fork edin
2. Geliştirme branchi oluşturun: `git checkout -b feature/yeni-ozellik`
3. Değişiklikleri commit edin: `git commit -am 'Yeni özellik ekle'`
4. Branch'e push edin: `git push origin feature/yeni-ozellik`
5. Pull Request açın

Daha detaylı bilgi için [Katkıda Bulunma](./Katkıda-Bulunma) bölümüne bakın.

### Bug report nasıl açabilirim?

[Issues](https://github.com/GameKinq0/GKST_Engine/issues) sayfasına gidin ve "New Issue" butonuna tıklayın. Detaylı açıklama, Python sürümü ve hata mesajını ekleyin.

### Yeni feature teklif edebilir miyim?

Evet! [Issues](https://github.com/GameKinq0/GKST_Engine/issues) kısmında feature request açabilirsiniz.

## İletişim ve Destek

### Soruların var mı?

- [GitHub Discussions](https://github.com/GameKinq0/GKST_Engine/discussions) kısmında soru sorabilirsiniz
- [Issues](https://github.com/GameKinq0/GKST_Engine/issues) açabilirsiniz

### Cevap almak ne kadar sürüyor?

Community-driven proje olduğu için cevap süresi değişebilir. Mümkün olduğunca hızlı cevap vermeye çalışıyoruz.

---

**Daha fazla yardım için:** [GitHub Repository](https://github.com/GameKinq0/GKST_Engine)
