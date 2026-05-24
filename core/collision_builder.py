import bpy
import bmesh
from typing import Optional, List, Dict, Any

class GKSTCollisionBuilder:
    """
    GKST Collision Generation Engine.
    Automates the creation of optimized, engine-compliant Convex Hull colliders.
    Uses bmesh for reliable mesh operations.
    """
    def __init__(self, target_object: bpy.types.Object, engine: str = "UNREAL"):
        self.obj: bpy.types.Object = target_object
        self.engine: str = engine.upper()
        self.generated_colliders: List[bpy.types.Object] = []

    def _get_engine_naming_convention(self) -> str:
        """Returns the standardized naming convention based on the target game engine."""
        if self.engine == "UNREAL":
            return f"UCX_{self.obj.name}_01"  # Unreal Engine automated collision convention
        elif self.engine == "UNITY":
            return f"COL_{self.obj.name}"      # Standard Unity collider naming convention
        elif self.engine == "ROBLOX":
            return f"{self.obj.name}_Collision" # Clean naming for Roblox grouped assets
        return f"COL_{self.obj.name}"

    def build_convex_hull(self) -> Optional[bpy.types.Object]:
        """
        Generates a tight-fitting Convex Hull collider using bmesh.
        BUG FIX: Uses bmesh instead of deprecated to_mesh() approaches.
        """
        if not self.obj or self.obj.type != 'MESH':
            print(f"[GKST COLLISION ERROR] Target must be a valid 'MESH'. Process aborted.")
            return None

        collider_name = self._get_engine_naming_convention()
        print(f"\n>>> [GKST COLLISION START: {self.obj.name.upper()}] <<<")

        bm = bmesh.new()
        mesh_data: Optional[bpy.types.Mesh] = None
        collider_obj: Optional[bpy.types.Object] = None

        try:
            # BUG FIX: Get evaluated mesh using proper bmesh workflow
            depsgraph = bpy.context.evaluated_depsgraph_get()
            evaluated_obj = self.obj.evaluated_get(depsgraph)
            
            # Get mesh from evaluated object
            mesh_eval = evaluated_obj.to_mesh()
            bm.from_mesh(mesh_eval)
            evaluated_obj.to_mesh_clear()

            # Execute the spatial Convex Hull operation
            ch_result = bmesh.ops.convex_hull(bm, input=bm.verts)
            
            # Advanced Geometry Cleanup: Purge non-surface structural elements
            geom_to_delete = []
            geom_to_delete.extend(ch_result.get("geom_interior", []))
            geom_to_delete.extend(ch_result.get("geom_hole", []))
            geom_to_delete.extend(ch_result.get("geom_unused", []))
            
            if geom_to_delete:
                bmesh.ops.delete(bm, geom=geom_to_delete, context='VERTS')

            # Create the data-block container for the new collider mesh
            mesh_data = bpy.data.meshes.new(collider_name)
            bm.to_mesh(mesh_data)
            
            collider_obj = bpy.data.objects.new(collider_name, mesh_data)

            # Context-safe collection synchronization
            parent_collection = self.obj.users_collection[0] if self.obj.users_collection else bpy.context.collection
            parent_collection.objects.link(collider_obj)

            # Clean Environment: Ensure collider carries no overhead rendering materials
            collider_obj.data.materials.clear()

            # Portfolio Feature: Mathematical Parenting & Transform Alignment Fix
            # Since vertex data was captured in local space, setting the parent first 
            # and zeroing out the local matrix prevents catastrophic offset bugs.
            collider_obj.parent = self.obj
            collider_obj.matrix_local.identity() # Perfect local overlay alignment

            # Visual optimizations for Technical Artists within the viewport
            collider_obj.display_type = 'WIRE'
            collider_obj.show_in_front = True
            
            # Hide from final renders automatically
            collider_obj.hide_render = True 

            self.generated_colliders.append(collider_obj)
            print(f"[GKST COLLISION SUCCESS] Created asset: '{collider_name}' parented to '{self.obj.name}'.")
            return collider_obj

        except Exception as engine_fault:
            print(f"[GKST COLLISION CRITICAL] Hull compilation pipeline failed: {engine_fault}")
            import traceback
            traceback.print_exc()
            
            # Safe memory rollout on failure
            if collider_obj and collider_obj.name in bpy.data.objects:
                try:
                    bpy.data.objects.remove(collider_obj, do_unlink=True)
                except:
                    pass
            if mesh_data and mesh_data.name in bpy.data.meshes:
                try:
                    bpy.data.meshes.remove(mesh_data)
                except:
                    pass
            return None
            
        finally:
            bm.free()
            print(f">>> [GKST COLLISION END] <<<\n")
