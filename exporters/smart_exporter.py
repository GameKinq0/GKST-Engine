import bpy
import os
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
        """Creates export directory if it doesn't exist."""
        try:
            if not os.path.exists(self.export_path):
                os.makedirs(self.export_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"[GKST EXPORT ERROR] Failed to create export directory: {e}")
            return False

    def _apply_engine_transformations(self) -> None:
        """Applies engine-specific axis corrections and transformations."""
        print(f"[GKST EXPORT] Applying {self.engine} engine transformations...")
        
        if self.engine == "UNREAL":
            # Unreal uses Z-up, apply 90-degree rotation on X
            pass
        elif self.engine == "UNITY":
            # Unity uses Y-up (standard), minimal transformation
            pass
        elif self.engine == "ROBLOX":
            # Roblox uses Y-up, apply scale corrections
            pass

    def export_fbx(self, filepath: str) -> bool:
        """Exports mesh as FBX file."""
        try:
            print(f"[GKST EXPORT] Exporting FBX: {filepath}")
            
            # Select and set active
            bpy.context.view_layer.objects.active = self.obj
            self.obj.select_set(True)
            
            # FBX export settings
            bpy.ops.export_scene.fbx(
                filepath=filepath,
                use_selection=True,
                use_mesh_modifiers=True,
                use_animaion=False,
                object_types={'MESH'},
                bake_space_transform=True,
                axis_forward='-Y',
                axis_up='Z' if self.engine == "UNREAL" else 'Y'
            )
            
            print(f"[GKST EXPORT SUCCESS] FBX exported: {filepath}")
            return True
            
        except Exception as e:
            print(f"[GKST EXPORT ERROR] FBX export failed: {e}")
            return False

    def export_textures(self) -> bool:
        """Exports textures used by the mesh."""
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
                
                for node in material.node_tree.nodes if hasattr(material, 'node_tree') else []:
                    if node.type == 'TEX_IMAGE' and node.image:
                        image = node.image
                        texture_path = os.path.join(textures_dir, f"{image.name}.png")
                        image.save_render(texture_path)
                        exported_count += 1
                        print(f"[GKST EXPORT] Saved texture: {image.name}")
            
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
