# ✨ Features

GKST Asset Engine comes packed with powerful automation features designed for professional game development workflows.

## 🎯 Core Features

### 🟦 Roblox Smart Chunking

**Intelligent Mesh Subdivision for Roblox**

Roblox has a strict **10,000 triangle limit per MeshPart**. This can be a major bottleneck when working with complex models.

#### What it does:
- ✅ Automatically detects if a mesh exceeds the 10k triangle limit
- ✅ Precisely splits the mesh into **safe 9,500-poly chunks**
- ✅ Maintains original geometry and UV mapping
- ✅ Say goodbye to import errors and mesh splitting headaches

#### Example:
```
Original Model: 50,000 triangles
↓
GKST Smart Chunking
↓
Automatically creates:
  - Chunk_1: 9,500 triangles
  - Chunk_2: 9,500 triangles
  - Chunk_3: 9,500 triangles
  - Chunk_4: 9,500 triangles
  - Chunk_5: 12,000 triangles
```

---

### 🟩 Unreal Engine Auto-Collider

**Professional Collision Mesh Generation**

Unreal Engine requires specific collision mesh naming and formatting. Creating these manually is tedious and error-prone.

#### What it does:
- ✅ Generates perfectly optimized **Convex Hull collision meshes**
- ✅ Automatically applies the correct `UCX_[ModelName]` prefix
- ✅ Exports collision meshes in Unreal-compatible format
- ✅ No more manual collision setup in Unreal Editor

#### How it works:
```
Input: Your 3D model
↓
GKST Auto-Collider
↓
Output: 
  - Main mesh (without UCX prefix)
  - UCX_ModelName collision mesh
  - Ready to import into Unreal Engine
```

---

### 🟨 Engine-Specific Axis Correction

**Automatic Coordinate System Alignment**

Different game engines use different coordinate systems, which causes models to appear rotated or scaled incorrectly.

#### Supported Engines:
- **Unreal Engine** - Converts to Z-Up coordinates
- **Unity** - Converts to Y-Up coordinates  
- **Roblox** - Converts to Y-Up coordinates

#### What it prevents:
- ❌ Models laying face-down on the floor
- ❌ Incorrect scale/proportion
- ❌ Rotated models
- ❌ Manual axis adjustments

#### Automatic Conversions:
```
Blender (Right-handed Z-Up)
↓
GKST Axis Correction
↓
Unreal Engine (Right-handed Z-Up) ✓
Unity (Left-handed Y-Up) ✓
Roblox (Left-handed Y-Up) ✓
```

---

### 📉 One-Click LOD Generation

**Automatic Level-of-Detail Optimization**

Performance optimization is critical for games. GKST automatically creates LOD (Level-of-Detail) variations.

#### What it does:
- ✅ Creates **LOD1, LOD2, and LOD3** automatically
- ✅ Uses mathematical decimation for optimal quality
- ✅ Maintains UV mapping and material structure
- ✅ Keeps your game running smoothly

#### LOD Levels:
```
LOD0 (Original): 10,000 triangles (Closest camera distance)
LOD1: 5,000 triangles (Medium distance)
LOD2: 2,500 triangles (Far distance)
LOD3: 1,000 triangles (Very far distance)
```

#### Performance Impact:
- Faster rendering at distance
- Better frame rates
- Smoother gameplay experience
- Better battery life on mobile devices

---

## 🚀 Workflow Efficiency

All features are designed to work together in a **single smart export process**:

```
1. Select your 3D model in Blender
2. Choose target engine (Roblox/Unreal/Unity)
3. Click "Smart Export"
4. GKST handles:
   ├─ Mesh chunking (if needed)
   ├─ Collision generation (if needed)
   ├─ Axis correction (automatic)
   ├─ LOD generation (automatic)
   └─ File export (ready to import)
```

---

## 🎮 Supported Game Engines

| Engine | Smart Chunking | Auto-Collider | Axis Correction | LOD Generation |
|--------|:--------------:|:-------------:|:---------------:|:--------------:|
| Roblox | ✅ | ❌ | ✅ | ✅ |
| Unreal Engine | ❌ | ✅ | ✅ | ✅ |
| Unity | ❌ | ❌ | ✅ | ✅ |

---

## 💡 Pro Tips

1. **Always work at original scale** - GKST handles the conversion
2. **Combine meshes before export** - Reduces processing time
3. **Use high-quality models** - LOD generation preserves details
4. **Check collision meshes** - Review in Unreal before use
5. **Test each LOD level** - Ensure visual quality at distance

---

**Next:** Learn how to use these features in the [User Guide](User-Guide)
