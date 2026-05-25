import bpy
import bmesh
from typing import List

class GKSTRetopologyOptimizer:
    """
    GKST Automatic Retopology & Optimization Engine.
    Uses pure DECIMATE (COLLAPSE) method for fast polygon reduction.
    """
    
    def __init__(self, target_object: bpy.types.Object, target_poly_count: int = 5000):
        self.obj: bpy.types.Object = target_object
        self.target_poly_count: int = target_poly_count
        self.original_poly_count: int = 0
    
    def _get_current_poly_count(self) -> int:
        """Get current triangle count of the object."""
        self.obj.data.calc_loop_triangles()
        return len(self.obj.data.loop_triangles)
    
    def optimize(self) -> bool:
        """
        Main retopology optimization pipeline.
        Uses COLLAPSE decimate directly.
        """
        if not self.obj or self.obj.type != 'MESH':
            print(f"[GKST RETOPO ERROR] Invalid mesh object")
            return False
        
        self.original_poly_count = self._get_current_poly_count()
        
        print(f"\n>>> [GKST RETOPO START: {self.obj.name.upper()}] <<<")
        print(f"[GKST RETOPO] Original poly count: {self.original_poly_count:,}")
        print(f"[GKST RETOPO] Target poly count: {self.target_poly_count:,}")
        
        # If already under target, no optimization needed
        if self.original_poly_count <= self.target_poly_count:
            print(f"[GKST RETOPO INFO] Already under target ({self.original_poly_count:,} ≤ {self.target_poly_count:,})")
            print(f">>> [GKST RETOPO END] <<<\n")
            return True
        
        try:
            # Calculate reduction ratio
            reduction_ratio = self.target_poly_count / self.original_poly_count
            reduction_ratio = max(0.01, min(reduction_ratio, 0.99))  # Clamp between 1-99%
            
            print(f"[GKST RETOPO] Reduction ratio: {reduction_ratio:.2%}")
            
            # Store original state
            original_mode = self.obj.mode
            original_selected = [o for o in bpy.context.selected_objects]
            original_active = bpy.context.view_layer.objects.active
            
            # Switch to OBJECT mode
            bpy.ops.object.select_all(action='DESELECT')
            self.obj.select_set(True)
            bpy.context.view_layer.objects.active = self.obj
            
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            
            print(f"[GKST RETOPO] Applying COLLAPSE decimate...")
            
            # Add decimate modifier with COLLAPSE
            decimate_mod = self.obj.modifiers.new(name="GKST_Retopo_Decimate", type='DECIMATE')
            decimate_mod.decimate_type = 'COLLAPSE'
            decimate_mod.ratio = reduction_ratio
            decimate_mod.use_collapse_triangulate = False
            
            # Apply modifier
            bpy.ops.object.modifier_apply(modifier=decimate_mod.name)
            
            print(f"[GKST RETOPO SUCCESS] Decimate applied successfully")
            
            # Check result
            final_poly_count = self._get_current_poly_count()
            final_reduction = (self.original_poly_count - final_poly_count) / self.original_poly_count
            
            print(f"[GKST RETOPO] Final poly count: {final_poly_count:,}")
            print(f"[GKST RETOPO] Total reduction: {final_reduction:.1%}")
            print(f">>> [GKST RETOPO END] <<<\n")
            
            return True
            
        except Exception as e:
            print(f"[GKST RETOPO ERROR] Retopology failed: {e}")
            print(f">>> [GKST RETOPO END] <<<\n")
            return False
        
        finally:
            # Restore state
            try:
                bpy.ops.object.select_all(action='DESELECT')
                for obj in original_selected:
                    if obj and obj.name in bpy.data.objects:
                        obj.select_set(True)
                if original_active and original_active.name in bpy.data.objects:
                    bpy.context.view_layer.objects.active = original_active
            except:
                pass
