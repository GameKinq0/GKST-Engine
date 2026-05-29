# 🔧 Troubleshooting Guide

Having issues with GKST? This guide covers common problems and their solutions.

---

## Installation Issues

### ❌ Problem: "Add-on could not be registered"

**Symptoms:**
- Error message when trying to enable GKST
- Add-on doesn't appear in the add-ons list

**Solutions:**
1. **Update Blender** - Ensure you have Blender 3.6 or newer
   - Download latest version from [blender.org](https://www.blender.org/download/)
   
2. **Reinstall the add-on:**
   - Remove GKST from Preferences → Add-ons
   - Restart Blender
   - Download fresh from [Releases](https://github.com/GameKinq0/GKST_Engine/releases)
   - Install again

3. **Check file integrity:**
   - Don't extract the ZIP file manually
   - Let Blender extract it during installation

---

### ❌ Problem: GKST Toolkit panel not visible

**Symptoms:**
- Installed and enabled GKST, but can't find the toolkit
- No GKST tab in the right sidebar

**Solutions:**
1. **Press N key**
   - In the 3D viewport, press `N` to toggle the right sidebar
   - Look for the GKST Toolkit tab

2. **Check tabs**
   - The right sidebar has multiple tabs
   - Look through all tabs to find GKST

3. **Reset Blender workspace**
   - Top menu → `Workspace` → Click any workspace tab
   - This resets all panels to default positions

---

### ❌ Problem: "Python 3.9 not found" error

**Symptoms:**
- Error about Python version
- GKST won't initialize

**Solutions:**
1. **Blender includes Python**
   - GKST uses Blender's bundled Python
   - If this error appears, try updating Blender to 3.6+

2. **Check Blender Python:**
   - Scripting workspace → Toggle system console
   - Should show Python version 3.9+

---

## Export Issues

### ❌ Problem: Export fails immediately or crashes

**Symptoms:**
- GKST crashes during export
- Export produces no files
- Error message in console

**Solutions:**
1. **Check your model:**
   - Is the model properly joined? (`Ctrl + J` to join)
   - Do all meshes have valid geometry?
   - Are there any mesh errors? (Use Mesh → Cleanup or Blender's checker)

2. **Apply all modifiers:**
   - Modifier panel → Click down arrow on each modifier
   - Click "Apply" on all modifiers
   - Then try export again

3. **Disable experimental features:**
   - Try with default settings
   - Disable any custom options you added

4. **Restart Blender:**
   - Save your file
   - Close Blender completely
   - Reopen and try again

---

### ❌ Problem: Model appears rotated/scaled incorrectly in engine

**Symptoms:**
- Model lying on its side
- Model appears tiny or huge
- Orientation wrong compared to Blender

**Solutions:**
1. **Verify engine selection:**
   - Make sure you selected the correct engine (Roblox/Unreal/Unity)
   - Re-export with correct engine selected

2. **Check Blender orientation:**
   - Is your model correctly oriented in Blender?
   - Press `Numpad 7` for top view
   - Press `Numpad 1` for front view
   - Ensure model looks correct in these views

3. **Adjust scale manually:**
   - In GKST Toolkit, find "Scale" setting
   - Try `0.5` (half size) or `2.0` (double size)
   - Re-export and check

4. **Reset model transforms:**
   - Select model in Blender
   - Press `Ctrl + A` → "All Transforms"
   - Try export again

---

### ❌ Problem: Mesh exceeds polygon limit but didn't get chunked

**Symptoms:**
- Selected Roblox, model over 10k triangles
- GKST said it would chunk but didn't
- Still one large mesh

**Solutions:**
1. **Verify chunking was enabled:**
   - In GKST Toolkit, check that Roblox Smart Chunking is enabled
   - Not all models need chunking (some under 10k are OK)

2. **Check triangle count:**
   - Select model in Blender
   - Look at bottom: "Verts: X, Edges: Y, Faces: Z"
   - Each face = 1-2 triangles
   - Multiply faces × 2 to estimate triangles

3. **Force chunking:**
   - In settings, set minimum size per chunk
   - Re-export

---

## Engine-Specific Issues

### Roblox Issues

#### ❌ Model won't import into Roblox

**Solutions:**
1. **Check file format** - Make sure it's FBX
2. **Verify size limits** - Each chunk under 10k triangles
3. **Check Roblox limits** - Some mesh sizes are restricted
4. **Try a test file** - Create simple cube and export to test

#### ❌ Chunks aren't aligning/visible

**Solutions:**
1. **Position chunks correctly** - GKST should auto-position
2. **Check collision** - Disable collision in import settings
3. **Verify scale** - All chunks should match original scale

---

### Unreal Engine Issues

#### ❌ Collision mesh not appearing

**Solutions:**
1. **Check collision naming:**
   - Look in Content Browser for `UCX_[YourModelName]`
   - If missing, collision generation failed
   - Re-export with collision enabled

2. **Enable collision display:**
   - Open the mesh in Static Mesh Editor
   - Click "Collision" → "Show Collision"
   - Check if UCX mesh is visible

3. **Verify import settings:**
   - When importing, "Import Mesh" and collision options enabled
   - Click Import

4. **Check asset naming:**
   - Avoid special characters in model names
   - Use simple names like "Crate", "Rock", "Door"

#### ❌ Model appears with wrong orientation

**Solutions:**
1. **Check Z-Up conversion:**
   - Model should be Z-Up (vertical) for Unreal
   - If lying down, axis conversion may have failed

2. **Re-export:**
   - Select correct engine (Unreal Engine 5)
   - Re-export

---

### Unity Issues

#### ❌ Model appears stretched or scaled wrong

**Solutions:**
1. **Check scale in inspector:**
   - Select imported model in Hierarchy
   - Check Scale X/Y/Z values in Inspector
   - Should be around (1,1,1)

2. **Check FBX import settings:**
   - Select FBX in Project folder
   - Inspector → Model tab
   - "Scale Factor" should be 1.0
   - "Root Motion Bone Name" should be empty

#### ❌ Textures/Materials are missing

**Solutions:**
1. **GKST exports geometry only** - Materials need to be set up in Unity:
   - Create materials in Unity
   - Apply to the model in the scene

2. **UV maps should be present:**
   - Model → Materials tab in inspector
   - Check that material slots match your mesh

---

## Performance Issues

### ❌ Problem: Export is very slow

**Symptoms:**
- Stuck on "Processing..."
- Export takes 10+ minutes
- Blender appears frozen

**Solutions:**
1. **Check model complexity:**
   - Very high-poly models take longer
   - Consider decimating in Blender first
   - Use fewer LOD levels

2. **Disable unnecessary features:**
   - Disable LOD generation if not needed
   - Export only to one engine at a time

3. **Free up resources:**
   - Close other applications
   - Restart Blender with fewer tabs open

4. **Reduce quality:**
   - Lower LOD detail levels
   - This trades quality for speed

---

## File & Data Issues

### ❌ Problem: Can't find exported files

**Symptoms:**
- Export says complete but files missing
- Don't know where files went

**Solutions:**
1. **Check selected folder:**
   - When you click "Export", a folder dialog appears
   - Make sure you selected a folder
   - Remember the path you chose

2. **Check default location:**
   - Windows: `C:\Users\[Username]\Documents\GKST_Export`
   - macOS: `~/Documents/GKST_Export`
   - Linux: `~/Documents/GKST_Export`

3. **Search computer:**
   - Search for `.fbx` files modified today
   - Should find recent exports

---

### ❌ Problem: Files are corrupted or won't import

**Symptoms:**
- Files exist but won't open in engine
- Error messages during import
- Files appear incomplete

**Solutions:**
1. **Re-export:**
   - Delete files
   - Export again from Blender
   - Full re-export takes only minutes

2. **Check permissions:**
   - Make sure you have write permissions to export folder
   - Try exporting to Desktop instead

3. **Verify Blender file:**
   - Save your Blender file properly
   - Try exporting different model first (test export)

---

## Getting Help

If these solutions don't work:

1. **Check the console:**
   - Windows: Enable system console in Blender
   - Look for error messages
   - Note the exact error text

2. **Create an issue on GitHub:**
   - Go to [GKST Issues](https://github.com/GameKinq0/GKST_Engine/issues)
   - Click "New Issue"
   - Include:
     - Your OS (Windows/macOS/Linux)
     - Blender version
     - GKST version
     - What you were trying to do
     - Exact error message
     - Model complexity (approx. poly count)

3. **Join the Discord:**
   - [GameKing Studio Discord](https://discord.com/invite/tbDM8k7cnj)
   - Ask in #support channel
   - Share screenshots or error messages

---

## Common Error Messages

| Error Message | Meaning | Solution |
|---|---|---|
| "Python 3.9 not found" | Python missing or version too old | Update Blender to 3.6+ |
| "Model has invalid geometry" | Bad mesh data | Use Mesh → Cleanup in Blender |
| "Modifiers must be applied" | Unapplied modifiers present | Press Ctrl+A → All Transforms |
| "Export path not writable" | Permission denied | Choose different folder |
| "Engine not supported" | Wrong engine selected | Select from dropdown |
| "No mesh selected" | You didn't select a model | Click model in 3D view first |

---

**Still stuck?** Check the [FAQ](FAQ) or [User Guide](User-Guide)
