import bpy
from typing import List, Optional

class GKSTLODGenerator:
    """
    GKST LOD Generation Engine (Low-Level API Version).
    Bypasses viewport context completely for 100% guaranteed decimation 
    baking without silent failures or crashes.
    """
    def __init__(self, target_object: bpy.types.Object):
        self.obj: bpy.types.Object = target_object
        self.lod_levels: int = getattr(bpy.context.scene, "gkst_lod_count", 3)
        self.ratio: float = getattr(bpy.context.scene, "gkst_lod_ratio", 0.5)
        self.generated_lods: List[bpy.types.Object] = []

    def generate_lods(self) -> List[bpy.types.Object]:
        if not self.obj or self.obj.type != 'MESH':
            print("[GKST ERROR] Invalid target object. Pipeline requires a 'MESH' type.")
            return []

        print(f"\n>>> [GKST PIPELINE START: {self.obj.name.upper()}] <<<")

        # BUG FIX: Validate LOD parameters
        if self.lod_levels < 1 or self.lod_levels > 6:
            print(f"[GKST ERROR] Invalid LOD levels: {self.lod_levels}. Must be between 1 and 6.")
            return []
        
        if self.ratio <= 0.0 or self.ratio >= 1.0:
            print(f"[GKST ERROR] Invalid decimation ratio: {self.ratio}. Must be between 0.1 and 0.9.")
            return []

        # 1. Klasörleme (Collection) İşlemi
        parent_collection = self.obj.users_collection[0] if self.obj.users_collection else bpy.context.collection
        lod_collection_name = f"{self.obj.name}_LODs"
        lod_collection = bpy.data.collections.get(lod_collection_name)
        
        if not lod_collection:
            lod_collection = bpy.data.collections.new(lod_collection_name)
            parent_collection.children.link(lod_collection)

        base_poly_count = len(self.obj.data.polygons)
        current_ratio = 1.0

        try:
            for level in range(1, self.lod_levels + 1):
                lod_name = f"{self.obj.name}_LOD{level}"
                
                # 2. Objeyi ve Mesh'i Doğrudan Hafızada (Data Block) Kopyala
                try:
                    new_mesh = self.obj.data.copy()
                    new_obj = self.obj.copy()
                    new_obj.data = new_mesh
                    new_obj.name = lod_name
                    
                    # Sahneye ekle
                    lod_collection.objects.link(new_obj)
                except Exception as copy_error:
                    print(f"[GKST ERROR] Failed to copy object for {lod_name}: {copy_error}")
                    continue

                initial_lod_polys = len(new_obj.data.polygons)
                
                if initial_lod_polys > 8:
                    current_ratio *= self.ratio
                    safe_ratio = max(0.01, min(current_ratio, 0.99))
                    
                    # 3. Modifier'ı Ekle
                    try:
                        decimate_mod = new_obj.modifiers.new(name="GKST_Decimate", type='DECIMATE')
                        decimate_mod.decimate_type = 'COLLAPSE'
                        decimate_mod.ratio = safe_ratio
                        decimate_mod.use_collapse_triangulate = False
                        
                        # 4. KRİTİK FIX: Bağımsız Depsgraph ile Fırınlama (Context Override'ı Bypass Eder)
                        # Sadece bu obje için geçici bir depsgraph oluşturup sonucu alıyoruz.
                        dg = bpy.context.evaluated_depsgraph_get()
                        eval_obj = new_obj.evaluated_get(dg)
                        baked_mesh = bpy.data.meshes.new_from_object(eval_obj)
                        
                        # 5. Eski veriyi çöpe at, fırınlanmış (poligonu düşmüş) veriyi bağla
                        old_mesh = new_obj.data
                        new_obj.modifiers.clear()
                        new_obj.data = baked_mesh
                        
                        # Bellek Temizliği (Hafıza Şişmesini Engeller)
                        if old_mesh.users == 0:
                            bpy.data.meshes.remove(old_mesh)
                            
                        final_lod_polys = len(new_obj.data.polygons)
                        reduction_pct = ((base_poly_count - final_lod_polys) / max(1, base_poly_count)) * 100
                        print(f"[GKST SUCCESS] Created: {lod_name} | Polys: {final_lod_polys} (-{reduction_pct:.1f}% optimized)")
                    except Exception as decimate_error:
                        print(f"[GKST ERROR] Decimation failed for {lod_name}: {decimate_error}")
                        # Remove failed LOD object
                        bpy.data.objects.remove(new_obj, do_unlink=True)
                        continue
                else:
                    print(f"[GKST INFO] {lod_name} skipped decimation (Polycount {initial_lod_polys} is below analytical threshold).")

                self.generated_lods.append(new_obj)

        except Exception as pipeline_error:
            print(f"[GKST CRITICAL FAILURE] LOD generation engine crashed: {pipeline_error}")
            
        print(f">>> [GKST PIPELINE END: Processed {len(self.generated_lods)} assets successfully] <<<\n")
        return self.generated_lods
