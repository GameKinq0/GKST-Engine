# ❓ Frequently Asked Questions (FAQ)

## General Questions

### Q: What exactly is GKST Asset Engine?
**A:** GKST is a professional Blender add-on that automates the 3D asset pipeline for multiple game engines (Roblox, Unreal Engine, and Unity). It handles mesh optimization, axis correction, collision generation, and LOD creation automatically.

### Q: Is GKST free?
**A:** Yes! GKST is completely free and open-source under the MIT License.

### Q: Which engines are supported?
**A:** 
- ✅ Roblox Studio
- ✅ Unreal Engine 5
- ✅ Unity

### Q: Do I need any special Blender plugins to use GKST?
**A:** No! GKST is a standalone add-on. It only requires Blender 3.6+ and Python 3.9+ (which comes with Blender).

### Q: Can I use GKST on macOS and Linux?
**A:** Yes! GKST works on Windows, macOS, and Linux.

---

## Installation & Setup

### Q: Where do I download GKST?
**A:** Download from the [Releases page](https://github.com/GameKinq0/GKST_Engine/releases) on GitHub.

### Q: How do I install GKST?
**A:** See the [Getting Started - Installation](Getting-Started#installation) guide.

### Q: My add-on isn't showing up in Blender. What do I do?
**A:** 
1. Make sure you downloaded the `.zip` file (don't extract it)
2. Check that you installed it in `Edit → Preferences → Add-ons`
3. Update to Blender 3.6 or newer if you're using an older version
4. Restart Blender and try again

### Q: GKST Toolkit panel isn't visible. How do I open it?
**A:** Press `N` in the 3D viewport. If it still doesn't appear, check the tabs on the right sidebar.

### Q: Can I have multiple versions of GKST installed?
**A:** It's not recommended. Uninstall the old version before installing a new one.

---

## Features & Functionality

### Q: What is "Smart Chunking" for Roblox?
**A:** Roblox has a 10k triangle limit per MeshPart. Smart Chunking automatically splits larger meshes into safe 9,500-poly chunks, so you don't get import errors.

### Q: How does Auto-Collider work in Unreal Engine?
**A:** It generates convex hull collision meshes with the `UCX_[ModelName]` prefix. Unreal Engine automatically recognizes these as collision meshes during import.

### Q: What are LOD levels?
**A:** LOD (Level of Detail) versions are simplified versions of your model used at different distances. Close = detailed, far = simplified. This improves performance.

### Q: Can I customize LOD levels?
**A:** In advanced settings, you can adjust the decimation percentage for each LOD level.

### Q: Does GKST preserve my UV maps?
**A:** Yes! UV maps are preserved during all operations (chunking, collision, LOD generation).

### Q: Does GKST preserve materials?
**A:** GKST exports geometry and UVs. Material information is preserved for engines that support it (Unreal, Unity).

---

## Workflow Questions

### Q: Can I export the same model for multiple engines?
**A:** Yes! Export once for each engine. Select the engine and use Smart Export for each one.

### Q: Do I need to do anything special before exporting?
**A:** 
1. Join all meshes into a single object (`Ctrl + J`)
2. Apply all modifiers
3. Ensure proper UV mapping
4. Save your Blender file

### Q: What file formats does GKST export?
**A:** Primarily FBX (recommended for all engines). Also supports OBJ and GLTF with limitations.

### Q: How long does the export process take?
**A:** It depends on model complexity. Simple models: seconds. Complex models: up to a few minutes.

### Q: Can I export multiple models at once?
**A:** Not simultaneously. Export them one at a time.

---

## Troubleshooting

### Q: My model is rotated incorrectly in the engine. Why?
**A:** GKST should handle axis correction automatically. If this happens:
1. Check that you selected the correct engine
2. Try re-exporting
3. Check your model's orientation in Blender before export

### Q: Collision meshes aren't showing in Unreal Engine.
**A:** 
1. Ensure collision generation was enabled during export
2. Check that the model name has no special characters
3. Look for `UCX_[ModelName]` meshes in the content browser
4. In the static mesh editor, check "Show Collision" to verify

### Q: My LOD meshes look too simplified/strange.
**A:** This is normal! LODs are meant to be simplified. If quality is too low:
1. Try adjusting LOD decimation settings
2. Generate fewer LOD levels
3. Increase the quality target for specific LODs

### Q: Export failed / GKST crashed. What do I do?
**A:** 
1. Check the console output for error messages
2. Restart Blender
3. Make sure your Blender file is saved
4. Try exporting a simpler model first
5. Report the issue on GitHub with your error message

### Q: My model is too small/large in the engine.
**A:** Use the Scale adjustment in GKST Toolkit:
- Enter `0.5` for half size
- Enter `2.0` for double size
- Re-export with the new scale

### Q: GKST says there are "unsupported modifiers." What does this mean?
**A:** Before export, you need to apply all modifiers in Blender:
1. Select your model
2. In the Modifier properties, click the down arrow on each modifier
3. Click "Apply"
4. Re-export with GKST

---

## Advanced Questions

### Q: Can GKST handle very large models (1M+ triangles)?
**A:** GKST can handle large models, but:
- Smart Chunking is recommended for Roblox
- Processing may take longer
- Consider pre-decimating in Blender if too large

### Q: Can I use GKST in a batch/automated workflow?
**A:** Currently, GKST is designed for interactive use. Batch export may be available in future versions.

### Q: Can I use GKST for character rigging?
**A:** GKST focuses on static mesh optimization. For rigged characters, use dedicated character export pipelines.

### Q: Is GKST code open-source?
**A:** Yes! The source code is available on [GitHub](https://github.com/GameKinq0/GKST_Engine).

### Q: Can I contribute to GKST development?
**A:** Yes! Fork the repository and submit pull requests. See the repository for contribution guidelines.

---

## Still Have Questions?

- 📖 Check the [User Guide](User-Guide)
- 🐛 Check [Troubleshooting](Troubleshooting)
- 💬 Join our Discord: [GameKing Studio](https://discord.com/invite/tbDM8k7cnj)
- 🐙 Open an issue on [GitHub](https://github.com/GameKinq0/GKST_Engine/issues)
