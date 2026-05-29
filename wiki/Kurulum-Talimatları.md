# Kurulum Talimatları

GKST Engine'i farklı sistemlerde nasıl kuracağınızı öğrenin.

## Windows

### Python Yükleme

1. [python.org](https://www.python.org) adresinden Python indirin
2. Installer'ı çalıştırın
3. ✅ "Add Python to PATH" seçeneğini işaretleyin

### GKST Engine Yükleme

```bash
pip install gkst-engine
```

## macOS

### Homebrew ile (Önerilen)

```bash
brew install python3
pip3 install gkst-engine
```

### Manuel Yükleme

1. [python.org](https://www.python.org) adresinden DMG dosyasını indirin
2. Installer'ı çalıştırın
3. Terminal'de çalıştırın:

```bash
pip install gkst-engine
```

## Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install gkst-engine
```

## Linux (Fedora/RHEL)

```bash
sudo dnf install python3 python3-pip
pip3 install gkst-engine
```

## Kaynaktan Yükleme

```bash
git clone https://github.com/GameKinq0/GKST_Engine.git
cd GKST_Engine
python setup.py install
```

## Geliştirme Modu

Kod üzerinde çalışmak için:

```bash
git clone https://github.com/GameKinq0/GKST_Engine.git
cd GKST_Engine
pip install -e .
pip install -r requirements-dev.txt
```

## Kurulumu Doğrulama

```bash
python -c "import gkst_engine; print(gkst_engine.__version__)"
```

## Sorun Giderme

### "pip komutu bulunamadı" hatası

Windows'ta:
```bash
python -m pip install gkst-engine
```

macOS/Linux'ta:
```bash
python3 -m pip install gkst-engine
```

### Sürüm uyuşmazlığı

```bash
pip install --upgrade gkst-engine
```

### Virtual Environment Kullanma (Önerilen)

```bash
# Virtual environment oluşturun
python -m venv venv

# Etkinleştirin
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Yükleyin
pip install gkst-engine
```
