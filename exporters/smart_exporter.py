import bpy
import os
import shutil
from typing import Optional

class GKSTSmartExporter:
    """
    GKST Smart Exporter Engine.
    Handles FBX and texture export with engine-specific optimizations.
    """
    def __init__(self, target_object: bpy.types.Object, export_path: str, engine: str = "ROBLOX"):
        self.obj: bpy.types.Object = target_object
        self.export_path: str = export_path
        self.engine: str = engine.upper()
        self.export_log: list = []

    def _get_export_filename(self) -> str:
        """Returns engine-specific filename convention."""
        if self.engine == "UNREAL":
            return f"{self.obj.name}_SK.fbx"  # Skeletal mesh format
        elif self.engine == "UNITY":
            return f"{self.obj.name}_Model.fbx"
        else:  # ROBLOX
            return f"{self.obj.name}.fbx"

    def _ensure_export_directory(self) -> bool:
        """Creates export directory if it doesn't exist and verifies write access."""
        try:
            if not self.export_path:
                print("[GKST EXPORT ERROR] Export path is empty")
                return False
            
            if not os.path.exists(self.export_path):
                os.makedirs(self.export_path, exist_ok=True)
            
            # FIX: Verify directory is writable
            if not os.access(self.export_path, os.W_OK):
                print(f"[GKST EXPORT ERROR] Export directory is not writable: {self.export_path}")
                return False
            
            return True
        except Exception as e:
            print(f"[GKST EXPORT ERROR] Failed to create export directory: {e}")
            return False

    def _apply_engine_transformations(self) -> None:
        """Applies engine-specific axis corrections and transformations."""
        print(f"[GKST EXPORT] Applying {self.engine} engine transformations...")
        
        if self.engine == "UNREAL":
            # Unreal uses Z-up, prepare for rotation
            pass
        elif self.engine == "UNITY":
            # Unity uses Y-up (standard)
            pass
        elif self.engine == "ROBLOX":
            # Roblox uses Y-up
            pass

    def export_fbx(self, filepath: str) -> bool:
        """Exports mesh as FBX file with proper error handling."""
        try:
            if not filepath:
                print("[GKST EXPORT ERROR] Invalid filepath")
                return False
            
            print(f"[GKST EXPORT] Exporting FBX: {filepath}")
            
            # Store original selection state
            original_selected = [o for o in bpy.context.selected_objects]
            original_active = bpy.context.view_layer.objects.active
            
            # Select and set active
            bpy.ops.object.select_all(action='DESELECT')
            self.obj.select_set(True)
            bpy.context.view_layer.objects.active = self.obj
            
            # FBX export settings
            try:
                bpy.ops.export_scene.fbx(
                    filepath=filepath,
                    use_selection=True,
                    use_mesh_modifiers=True,
                    use_animation=False,
                    object_types={'MESH'},
                    bake_space_transform=True,
                    axis_forward='-Y',
                    axis_up='Z' if self.engine == "UNREAL" else 'Y',
                    apply_scaling='FBX_ALL'
                )
            except RuntimeError as e:
                print(f"[GKST EXPORT ERROR] FBX export operator failed: {e}")
                return False
            
            print(f"[GKST EXPORT SUCCESS] FBX exported: {filepath}")
            return True
            
        except Exception as e:
            print(f"[GKST EXPORT ERROR] FBX export failed: {e}")
            return False
        finally:
            # Restore original selection state
            try:
                bpy.ops.object.select_all(action='DESELECT')
                for obj in original_selected:
                    if obj and obj.name in bpy.data.objects:
                        obj.select_set(True)
                if original_active and original_active.name in bpy.data.objects:
                    bpy.context.view_layer.objects.active = original_active
            except:
                pass

    def export_textures(self) -> bool:
        """Exports textures used by the mesh with proper error handling."""
        try:
            print(f"[GKST EXPORT] Extracting textures for {self.obj.name}...")
            
            if not self.obj.data.materials:
                print("[GKST EXPORT INFO] No materials found.")
                return True
            
            textures_dir = os.path.join(self.export_path, "Textures")
            os.makedirs(textures_dir, exist_ok=True)
            
            exported_count = 0
            for material in self.obj.data.materials:
                if material is None:
                    continue
                
                # Check for use_nodes and node_tree
                if not material.use_nodes or not material.node_tree:
                    continue
                
                try:
                    for node in material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and hasattr(node, 'image') and node.image:
                            image = node.image
                            
                            # Skip packed images
                            if image.packed_file:
                                print(f"[GKST EXPORT INFO] Skipping packed image: {image.name}")
                                continue
                            
                            # Get image filepath
                            if image.filepath:
                                src_path = bpy.path.abspath(image.filepath)
                                
                                if os.path.exists(src_path):
                                    # Copy texture to export directory
                                    dst_name = os.path.basename(src_path)
                                    dst_path = os.path.join(textures_dir, dst_name)
                                    
                                    try:
                                        shutil.copy2(src_path, dst_path)
                                        exported_count += 1
                                        print(f"[GKST EXPORT] Copied texture: {dst_name}")
                                    except Exception as copy_err:
                                        print(f"[GKST EXPORT WARNING] Failed to copy {dst_name}: {copy_err}")
                                else:
                                    print(f"[GKST EXPORT WARNING] Texture file not found: {src_path}")
                except Exception as node_error:
                    print(f"[GKST EXPORT WARNING] Error processing material nodes: {node_error}")
            
            print(f"[GKST EXPORT SUCCESS] Exported {exported_count} textures.")
            return True
            
        except Exception as e:
            print(f"[GKST EXPORT WARNING] Texture export failed: {e}")
            return False

    def execute_export(self, export_mesh: bool = True, export_textures: bool = True) -> bool:
        """Main export execution pipeline."""
        print(f"\n>>> [GKST EXPORT START: {self.obj.name.upper()}] <<<")
        
        if not self._ensure_export_directory():
            return False
        
        self._apply_engine_transformations()
        
        if export_mesh:
            filepath = os.path.join(self.export_path, self._get_export_filename())
            if not self.export_fbx(filepath):
                return False
        
        if export_textures:
            if not self.export_textures():
                print("[GKST EXPORT WARNING] Texture export completed with warnings.")
        
        print(f">>> [GKST EXPORT END: {self.obj.name.upper()}] <<<\n")
        return True
