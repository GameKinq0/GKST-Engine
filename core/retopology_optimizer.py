import bpy
import bmesh
from typing import List

class GKSTRetopologyOptimizer:
    """
    GKST Automatic Retopology & Optimization Engine.
    Reduces polygon count to target while maintaining visual fidelity.
    Uses quadriflow or voxel remeshing for clean topology.
    """
    
    def __init__(self, target_object: bpy.types.Object, target_poly_count: int = 5000):
        """
        Initialize retopology optimizer.
        
        Args:
            target_object: Mesh object to retopologize
            target_poly_count: Target triangle count (default 5000)
        """
        self.obj: bpy.types.Object = target_object
        self.target_poly_count: int = target_poly_count
        self.original_poly_count: int = 0
        self.optimized_obj: bpy.types.Object = None
    
    def _get_current_poly_count(self) -> int:
        """Get current triangle count of the object."""
        self.obj.data.calc_loop_triangles()
        return len(self.obj.data.loop_triangles)
    
    def _apply_voxel_remesh(self, voxel_size: float = 0.1) -> bool:
        """
        Apply voxel remeshing for automatic retopology.
        Lower voxel size = more detail but more polys.
        """
        try:
            print(f"[GKST RETOPO] Applying voxel remeshing with size {voxel_size}...")
            
            # Store original state
            original_mode = self.obj.mode
            original_selected = [o for o in bpy.context.selected_objects]
            original_active = bpy.context.view_layer.objects.active
            
            # Select and set active
            bpy.ops.object.select_all(action='DESELECT')
            self.obj.select_set(True)
            bpy.context.view_layer.objects.active = self.obj
            
            # Apply voxel remesher
            bpy.ops.object.voxel_remesh(
                mode='SMOOTH',
                dimension=int(1.0 / voxel_size),  # Inverse relationship
                adaptivity=0.0,  # 0 = exact, higher = less detail
                use_mesh_symmetry=False,
                use_preserve_sharp=True,
                use_preserve_border=True,
            )
            
            print(f"[GKST RETOPO SUCCESS] Voxel remeshing completed")
            return True
            
        except Exception as e:
            print(f"[GKST RETOPO WARNING] Voxel remeshing failed: {e}")
            print(f"[GKST RETOPO INFO] Falling back to decimate method...")
            return False
        finally:
            # Restore state
            bpy.ops.object.select_all(action='DESELECT')
            for obj in original_selected:
                if obj and obj.name in bpy.data.objects:
                    obj.select_set(True)
            if original_active and original_active.name in bpy.data.objects:
                bpy.context.view_layer.objects.active = original_active
    
    def _apply_decimate_remesh(self, reduction_ratio: float) -> bool:
        """
        Apply decimate modifier for retopology (fallback method).
        Uses UNSUBDIVIDE or COLLAPSE decimation.
        """
        try:
            print(f"[GKST RETOPO] Applying decimate remeshing with ratio {reduction_ratio:.2%}...")
            
            # Store original state
            original_mode = self.obj.mode
            original_selected = [o for o in bpy.context.selected_objects]
            original_active = bpy.context.view_layer.objects.active
            
            # Select and set active
            bpy.ops.object.select_all(action='DESELECT')
            self.obj.select_set(True)
            bpy.context.view_layer.objects.active = self.obj
            
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            
            # Add decimate modifier
            decimate_mod = self.obj.modifiers.new(name="GKST_Retopo_Decimate", type='DECIMATE')
            decimate_mod.decimate_type = 'UNSUBDIVIDE'  # Clean quad topology
            decimate_mod.iterations = 3  # More aggressive reduction
            
            # Alternative: COLLAPSE method
            # decimate_mod.decimate_type = 'COLLAPSE'
            # decimate_mod.ratio = reduction_ratio
            
            # Apply modifier
            bpy.ops.object.modifier_apply(modifier=decimate_mod.name)
            
            print(f"[GKST RETOPO SUCCESS] Decimate remeshing completed")
            return True
            
        except Exception as e:
            print(f"[GKST RETOPO ERROR] Decimate remeshing failed: {e}")
            return False
        finally:
            # Restore state
            bpy.ops.object.select_all(action='DESELECT')
            for obj in original_selected:
                if obj and obj.name in bpy.data.objects:
                    obj.select_set(True)
            if original_active and original_active.name in bpy.data.objects:
                bpy.context.view_layer.objects.active = original_active
    
    def _calculate_voxel_size(self, current_poly: int, target_poly: int) -> float:
        """
        Calculate optimal voxel size based on poly reduction needed.
        Higher voxel size = fewer polys (more aggressive reduction).
        """
        if target_poly >= current_poly:
            return 0.05  # Very fine detail
        
        # Ratio of reduction needed
        reduction_ratio = target_poly / current_poly
        
        # Convert to voxel size (empirical formula)
        # Smaller voxel = more detail
        if reduction_ratio > 0.9:
            voxel_size = 0.05  # 95%+ kept
        elif reduction_ratio > 0.7:
            voxel_size = 0.1   # ~70% kept
        elif reduction_ratio > 0.5:
            voxel_size = 0.15  # ~50% kept
        elif reduction_ratio > 0.3:
            voxel_size = 0.2   # ~30% kept
        elif reduction_ratio > 0.1:
            voxel_size = 0.3   # ~10% kept
        else:
            voxel_size = 0.5   # Extreme reduction
        
        print(f"[GKST RETOPO] Calculated voxel size: {voxel_size} (reduction ratio: {reduction_ratio:.1%})")
        return voxel_size
    
    def optimize(self) -> bool:
        """
        Main retopology optimization pipeline.
        Automatically reduces poly count while maintaining shape.
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
        
        # Calculate reduction percentage
        reduction_needed = (self.original_poly_count - self.target_poly_count) / self.original_poly_count
        print(f"[GKST RETOPO] Reduction needed: {reduction_needed:.1%}")
        
        # Try voxel remeshing first (best quality)
        voxel_size = self._calculate_voxel_size(self.original_poly_count, self.target_poly_count)
        if self._apply_voxel_remesh(voxel_size):
            # Check result
            new_poly_count = self._get_current_poly_count()
            reduction_achieved = (self.original_poly_count - new_poly_count) / self.original_poly_count
            print(f"[GKST RETOPO] New poly count: {new_poly_count:,} (reduced by {reduction_achieved:.1%})")
            
            if new_poly_count > self.target_poly_count:
                print(f"[GKST RETOPO] Still over target, applying decimate...")
                reduction_ratio = self.target_poly_count / new_poly_count
                self._apply_decimate_remesh(reduction_ratio)
        else:
            # Fallback to decimate
            reduction_ratio = self.target_poly_count / self.original_poly_count
            self._apply_decimate_remesh(reduction_ratio)
        
        # Final check
        final_poly_count = self._get_current_poly_count()
        final_reduction = (self.original_poly_count - final_poly_count) / self.original_poly_count
        
        print(f"[GKST RETOPO] Final poly count: {final_poly_count:,}")
        print(f"[GKST RETOPO] Total reduction: {final_reduction:.1%}")
        
        if final_poly_count <= self.target_poly_count * 1.1:  # Allow 10% overage
            print(f"[GKST RETOPO SUCCESS] Optimization complete!")
            print(f">>> [GKST RETOPO END] <<<\n")
            return True
        else:
            print(f"[GKST RETOPO WARNING] Still above target by {((final_poly_count / self.target_poly_count - 1) * 100):.1f}%")
            print(f">>> [GKST RETOPO END] <<<\n")
            return False
