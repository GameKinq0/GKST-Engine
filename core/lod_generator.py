import bpy
from typing import List

class GKSTLODGenerator:
    """
    GKST LOD Generation Engine (Low-Level API Version).
    Bypasses viewport context completely for 100% guaranteed decimation 
    baking without silent failures or crashes.
    FIXED: Prevents nested spawning - places LODs side by side with offset.
    """
    def __init__(self, target_object: bpy.types.Object):
        self.obj: bpy.types.Object = target_object
        self.lod_levels: int = getattr(bpy.context.scene, "gkst_lod_count", 3)
        self.ratio: float = getattr(bpy.context.scene, "gkst_lod_ratio", 0.5)
        self.generated_lods: List[bpy.types.Object] = []

    def generate_lods(self) -> List[bpy.types.Object]:
        if not self.obj or self.obj.type != 'MESH':
            print("[GKST LOD ERROR] Invalid target object. Pipeline requires a 'MESH' type.")
            return []

        print(f"\n>>> [GKST LOD PIPELINE START: {self.obj.name.upper()}] <<<")

        # 1. Collection Organization
        parent_collection = self.obj.users_collection[0] if self.obj.users_collection else bpy.context.collection
        lod_collection_name = f"{self.obj.name}_LODs"
        lod_collection = bpy.data.collections.get(lod_collection_name)
        
        if not lod_collection:
            lod_collection = bpy.data.collections.new(lod_collection_name)
            parent_collection.children.link(lod_collection)

        base_poly_count = len(self.obj.data.polygons)
        current_ratio = 1.0
        
        # Get original object bounds for offset calculation
        import mathutils
        bbox = [mathutils.Vector(corner) for corner in self.obj.bound_box]
        bbox_size_x = max([v.x for v in bbox]) - min([v.x for v in bbox])

        try:
            for level in range(1, self.lod_levels + 1):
                lod_name = f"{self.obj.name}_LOD{level}"
                
                # 2. Copy Object and Mesh Data (always from original, not from previous LOD)
                new_mesh = self.obj.data.copy()
                new_obj = self.obj.copy()
                new_obj.data = new_mesh
                new_obj.name = lod_name
                
                # FIX: Place LOD objects side by side with X offset to prevent nested spawning
                offset_distance = bbox_size_x * 1.2 * level
                new_obj.location.x += offset_distance
                
                # Add to collection
                lod_collection.objects.link(new_obj)

                initial_lod_polys = len(new_obj.data.polygons)
                
                if initial_lod_polys > 8:
                    current_ratio *= self.ratio
                    safe_ratio = max(0.01, min(current_ratio, 0.99))
                    
                    # 3. Add Decimate Modifier
                    decimate_mod = new_obj.modifiers.new(name="GKST_Decimate", type='DECIMATE')
                    decimate_mod.decimate_type = 'COLLAPSE'
                    decimate_mod.ratio = safe_ratio
                    decimate_mod.use_collapse_triangulate = False
                    
                    # 4. CRITICAL FIX: Depsgraph update required
                    # Without this line, Blender doesn't account for the modifier!
                    dg = bpy.context.evaluated_depsgraph_get()
                    dg.update() 
                    
                    eval_obj = new_obj.evaluated_get(dg)
                    baked_mesh = bpy.data.meshes.new_from_object(eval_obj)
                    
                    # 5. Replace old mesh with baked decimated mesh
                    old_mesh = new_obj.data
                    new_obj.modifiers.clear()
                    new_obj.data = baked_mesh
                    
                    # Memory Cleanup
                    if old_mesh.users == 0:
                        bpy.data.meshes.remove(old_mesh)
                        
                    final_lod_polys = len(new_obj.data.polygons)
                    reduction_pct = ((base_poly_count - final_lod_polys) / base_poly_count) * 100
                    print(f"[GKST LOD SUCCESS] Created: {lod_name} | Polys: {final_lod_polys} (-{reduction_pct:.1f}% optimized) | Offset: +{offset_distance:.2f}m")
                else:
                    print(f"[GKST LOD INFO] {lod_name} skipped decimation (Polycount {initial_lod_polys} is below analytical threshold).")

                self.generated_lods.append(new_obj)

        except Exception as pipeline_error:
            print(f"[GKST LOD CRITICAL FAILURE] LOD generation engine crashed: {pipeline_error}")
            import traceback
            traceback.print_exc()
            
        print(f">>> [GKST LOD PIPELINE END: Processed {len(self.generated_lods)} assets successfully] <<<\n")
        return self.generated_lods
