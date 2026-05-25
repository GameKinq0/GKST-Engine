# 🎮 User Guide - How to Use GKST Asset Engine

This guide will walk you through using GKST Asset Engine step-by-step.

## Before You Start

Make sure you have:
- ✅ [Installed GKST](Getting-Started)
- ✅ A 3D model loaded in Blender
- ✅ The GKST Toolkit panel open (Press `N` in 3D viewport)

---

## Basic Workflow

### Step 1: Load or Create Your Model

1. Open Blender and create or import your 3D model
2. Make sure your model is properly modeled and textured
3. **Join all meshes** into a single object if you have multiple parts:
   - Select all objects in your model (Press `A`)
   - Press `Ctrl + J` to join them
   - Give your model a clear name (e.g., "Knight_Model", "Building_Tower")

### Step 2: Select Your Model

1. In the **3D Viewport**, click on your model to select it
2. The model should be **highlighted in orange** (selected)
3. Make sure **only one mesh is selected** for export

### Step 3: Open GKST Toolkit

1. Press `N` in the 3D viewport to open the right sidebar
2. Look for the **"GKST Toolkit"** tab
3. You should see:
   - Engine selection dropdown
   - Export settings
   - Export button

### Step 4: Choose Your Target Engine

From the dropdown menu, select which engine you're exporting for:

```
▼ Select Engine
├─ Roblox Studio
├─ Unreal Engine 5
└─ Unity
```

**Choose based on where you'll use the model:**
- **Roblox Studio** - For Roblox games
- **Unreal Engine 5** - For UE5 projects
- **Unity** - For Unity projects

### Step 5: Smart Export

1. Click the **"Akıllı Export"** or **"Smart Export"** button
2. A file dialog will appear
3. Choose where to save your files
4. Click "Export"

### Step 6: Processing

GKST will now automatically:

**For Roblox:**
- ✅ Split the mesh if it exceeds 10k triangles
- ✅ Convert to Y-Up coordinates
- ✅ Generate LOD versions
- ✅ Export as FBX files ready for import

**For Unreal Engine:**
- ✅ Generate collision meshes with UCX_ prefix
- ✅ Convert to Z-Up coordinates
- ✅ Generate LOD versions
- ✅ Export as FBX files ready for import

**For Unity:**
- ✅ Convert to Y-Up coordinates
- ✅ Generate LOD versions
- ✅ Export as FBX files ready for import

### Step 7: Import Into Your Engine

**Roblox Studio:**
1. Open Roblox Studio
2. Go to `View` → `Toolbox` → `Inventory` → `My Models`
3. Click "Create" → "New Model Set"
4. Upload your exported FBX files
5. Insert into your game

**Unreal Engine 5:**
1. Open your UE5 project
2. In Content Browser, click "Import" or drag-drop the FBX
3. In import settings, make sure collision is enabled
4. The UCX_ mesh will be automatically detected as collision

**Unity:**
1. In Project window, drag-drop the FBX into your Assets folder
2. Configure materials and LOD settings if needed
3. Drag into your scene

---

## Advanced Options

### LOD Settings

After clicking Smart Export, you may see LOD configuration options:

```
Generate LODs:
☑ LOD0 (100% - Original quality)
☑ LOD1 (50% - Medium quality)
☑ LOD2 (25% - Low quality)
☑ LOD3 (10% - Very low quality)
```

**LOD Usage:**
- **LOD0** - Close-up, high detail view
- **LOD1** - Medium distance
- **LOD2** - Far distance
- **LOD3** - Very far distance (background)

### Scale Adjustment

Some models may need scale adjustment. In the toolkit, you can set:

```
Scale Factor: [1.0] (100%)
```

Enter a value:
- `0.5` - Half size
- `1.0` - Original size (default)
- `2.0` - Double size

### Export Format

Choose your export format (usually FBX is recommended):
- **FBX** (Recommended for all engines)
- **OBJ** (Basic compatibility)
- **GLTF** (Experimental)

---

## Common Workflows

### Workflow 1: Simple Asset for Roblox

```
1. Model in Blender ✓
2. Select model
3. Choose "Roblox Studio"
4. Smart Export
5. Wait for processing
6. Import into Roblox
7. Done!
```

### Workflow 2: Complex Asset for Unreal Engine

```
1. Model in Blender ✓
2. Add collision primitives (optional)
3. Select model
4. Choose "Unreal Engine 5"
5. Smart Export
6. Collision meshes generated automatically ✓
7. Import into UE5
8. Verify collision in viewport
9. Done!
```

### Workflow 3: Optimized Asset with LODs for Mobile Game (Unity)

```
1. High-poly model in Blender ✓
2. Select model
3. Choose "Unity"
4. Smart Export (LOD generation enabled)
5. Receives: LOD0, LOD1, LOD2, LOD3
6. Import all LODs into Unity
7. Set up LOD group component
8. Test performance
9. Done!
```

---

## Tips & Best Practices

### ✅ DO's

- ✅ **Clean geometry** - Remove unused vertices and faces
- ✅ **Proper naming** - Use clear, descriptive names for models
- ✅ **UV unwrapping** - Ensure models have proper UVs before export
- ✅ **Combine meshes** - Join multiple parts into one object
- ✅ **Test in target engine** - Always test the imported model in your engine
- ✅ **Keep backups** - Save your Blender file before exporting

### ❌ DON'Ts

- ❌ **Don't mix scales** - Keep consistent scale across your model
- ❌ **Don't export disconnected objects** - Join all parts first
- ❌ **Don't use modifiers** - Apply all modifiers before export
- ❌ **Don't ignore LOD quality** - Check that LODs look good at distance
- ❌ **Don't modify exported files manually** - Re-export if changes needed

---

## Troubleshooting

### Export Process Issues

**"Model appears rotated in engine"**
- Solution: This shouldn't happen with GKST axis correction. Try re-exporting.
- If issue persists: Check your Blender file's orientation before export.

**"Collision mesh missing in Unreal"**
- Solution: Ensure collision generation is enabled in export settings
- Check that model name doesn't contain special characters
- Verify collision appears as UCX_[ModelName] in Unreal

**"Model too small/large in engine"**
- Solution: Use the Scale Adjustment option in GKST Toolkit
- Adjust the scale factor and re-export

**"LOD versions look too simplified"**
- Solution: This is normal! LODs are meant to be simplified
- Adjust LOD decimation percentage if available
- Test multiple LOD levels to find best balance

---

**Need help?** Check the [Troubleshooting](Troubleshooting) page or [FAQ](FAQ)
