# ⚙️ GameKing Asset Engine (GKST)

![Blender](https://img.shields.io/badge/Blender-3.6+-orange?style=for-the-badge&logo=blender)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Maintained](https://img.shields.io/badge/Maintained-Yes-success?style=for-the-badge)

**Choose Language / Dil Seçimi:**  
[🇬🇧 English](#-english) | [🇹🇷 Türkçe](#-türkçe)

---

## 🇬🇧 ENGLISH

**The ultimate 3D asset pipeline for Roblox Studio, Unreal Engine, and Unity.**  
Developed by [GameKing Studio](https://github.com/GameKing-Studio).

### 🚀 What is GKST Asset Engine?
Importing complex 3D models into game engines is a nightmare. Roblox has strict 10,000 triangle limits per MeshPart, Unreal Engine uses Z-Up coordinates and requires specific `UCX_` collision names, and Unity expects Y-Up. 

**GKST Asset Engine** is a professional Blender add-on that automates this entire pipeline with a single click.

### ✨ Key Features
*   🟦 **Roblox Smart Chunking:** Automatically detects if a mesh exceeds Roblox's 10k triangle limit and precisely splits it into safe 9,500-poly chunks. Say goodbye to import errors.
*   🟩 **Unreal Engine Auto-Collider:** Generates perfectly optimized Convex Hull collision meshes with the correct `UCX_[ModelName]` prefix for Unreal Engine.
*   🟨 **Engine-Specific Axis Correction:** Automatically rotates and scales models during export (Z-Up for UE, Y-Up for Unity/Roblox). No more models laying face-down on the floor.
*   📉 **One-Click LOD Generation:** Mathematically decimates your mesh into LOD1, LOD2, and LOD3 variations, keeping your game perfectly optimized.

### 🛠️ Installation
1. Download the latest release (`GKST_Asset_Engine.zip`) from the Releases tab.
2. Open Blender -> `Edit` -> `Preferences` -> `Add-ons`.
3. Click **Install...**, select the downloaded `.zip` file.
4. Check the box next to **3D View: GameKing Asset Engine** to enable it.
5. Press `N` in the 3D viewport to open the GKST Toolkit panel.

### 🎮 How to Use
1. Select your target 3D model in Blender.
2. Open the **GKST Toolkit** on the right sidebar.
3. Select your target game engine from the dropdown list (Roblox, Unreal, or Unity).
4. Click **"Akıllı Export / Smart Export"**. The engine will handle chunking, axis fixing, and scale applying automatically.

---

## 🇹🇷 TÜRKÇE

**Roblox Studio, Unreal Engine ve Unity için nihai 3D model otomasyon motoru.**  
[GameKing Studio](https://github.com/GameKing-Studio) tarafından geliştirilmiştir.

### 🚀 GKST Asset Engine Nedir?
Karmaşık 3D modelleri oyun motorlarına aktarmak bir kabustur. Roblox'un parça (MeshPart) başına katı 10.000 poligon sınırı vardır, Unreal Engine Z-Up koordinat sistemini kullanır ve özel `UCX_` collision (çarpışma) isimleri ister, Unity ise Y-Up bekler. 

**GKST Asset Engine**, tüm bu teknik süreçleri (pipeline) tek tıkla otomatikleştiren profesyonel bir Blender eklentisidir.

### ✨ Temel Özellikler
*   🟦 **Roblox Akıllı Parçalama (Smart Chunking):** Modelin 10.000 üçgen sınırını aşıp aşmadığını otomatik algılar ve tam 9.500 poligonluk güvenli parçalara böler. Hata mesajlarına elveda deyin.
*   🟩 **Unreal Engine Otomatik Çarpışma (Auto-Collider):** Unreal Engine için doğru `UCX_[ModelAdı]` ön ekiyle mükemmel optimize edilmiş Convex Hull (dışbükey) çarpışma ağları üretir.
*   🟨 **Motora Özel Eksen Düzeltme:** Dışa aktarım sırasında modelleri otomatik olarak döndürür ve ölçeklendirir (UE için Z-Up, Unity/Roblox için Y-Up). Yüz üstü yere yatan modellere son.
*   📉 **Tek Tıkla LOD Üretimi:** Oyununuzun mükemmel şekilde optimize kalmasını sağlayarak, modelinizi matematiksel olarak LOD1, LOD2 ve LOD3 varyasyonlarına düşürür.

### 🛠️ Kurulum
1. Releases sekmesinden en son sürümü (`GKST_Asset_Engine.zip`) indirin.
2. Blender'ı açın -> `Edit` -> `Preferences` -> `Add-ons`.
3. **Install...** butonuna tıklayın ve indirdiğiniz `.zip` dosyasını seçin.
4. Etkinleştirmek için **3D View: GameKing Asset Engine** yanındaki kutucuğu işaretleyin.
5. GKST Toolkit panelini açmak için 3D ekranında `N` tuşuna basın.

### 🎮 Nasıl Kullanılır
1. Blender'da hedef 3D modelinizi seçin.
2. Sağ kenar çubuğundaki **GKST Toolkit** panelini açın.
3. Açılır listeden hedef oyun motorunuzu (Roblox, Unreal veya Unity) seçin.
4. **"Akıllı Export (Smart Export)"** butonuna tıklayın. Motor; parçalama, eksen düzeltme ve ölçek uygulamalarını otomatik halledecektir.

---
*Created by GameKinq0 - Founder & Lead Developer at GameKing Studio.*
