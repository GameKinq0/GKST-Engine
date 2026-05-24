import bpy
import bmesh
import mathutils
from typing import Optional, Dict, Any, List, Tuple

class GKSTMeshSplitter:
    """
    GKST Professional Mesh Splitting Engine.
    Recursively splits meshes by poly count limit until all parts are under the limit.
    """

    @staticmethod
    def _calculate_optimal_cut_plane(obj: bpy.types.Object) -> Tuple[mathutils.Vector, mathutils.Vector]:
        """Calculates the cutting plane based on the longest axis of the bounding box (Local Space)."""
        local_coords = [mathutils.Vector(corner) for corner in obj.bound_box]
        
        max_coord = mathutils.Vector((
            max(c[0] for c in local_coords), max(c[1] for c in local_coords), max(c[2] for c in local_coords)
        ))
        min_coord = mathutils.Vector((
            min(c[0] for c in local_coords), min(c[1] for c in local_coords), min(c[2] for c in local_coords)
        ))

        dimensions = max_coord - min_coord
        local_center = (max_coord + min_coord) / 2.0
        
        # Determine the longest axis
        if dimensions.x >= dimensions.y and dimensions.x >= dimensions.z:
            plane_normal = mathutils.Vector((1, 0, 0))
        elif dimensions.y >= dimensions.x and dimensions.y >= dimensions.z:
            plane_normal = mathutils.Vector((0, 1, 0))
        else:
            plane_normal = mathutils.Vector((0, 0, 1))

        return local_center, plane_normal.normalized()

    @staticmethod
    def _split_single_cut(obj: bpy.types.Object) -> Optional[List[bpy.types.Object]]:
        """
        Performs a single bisect operation by duplicating and clearing opposite sides.
        100% crash-proof method without using split/separate operators.
        """
        if not obj or obj.type != 'MESH':
            return None

        window = bpy.context.window
        screen = window.screen
        area = next((a for a in screen.areas if a.type == 'VIEW_3D'), None)
        region = next((r for r in area.regions if r.type == 'WINDOW'), None) if area else None

        override: Dict[str, Any] = {
            'window': window, 'screen': screen, 'area': area, 'region': region,
            'scene': bpy.context.scene, 'view_layer': bpy.context.view_layer,
        }

        original_mode = obj.mode
        parent_collection = obj.users_collection[0] if obj.users_collection else bpy.context.collection

        try:
            with bpy.context.temp_override(**override):
                if original_mode != 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')

                bpy.ops.object.select_all(action='DESELECT')
                
                plane_co, plane_no = GKSTMeshSplitter._calculate_optimal_cut_plane(obj)

                # 1. İkinci parça için objeyi tamamen kopyala
                new_obj = obj.copy()
                new_obj.data = obj.data.copy()
                new_obj.name = f"{obj.name}_Part2"
                parent_collection.objects.link(new_obj)

                # 2. Orijinal Objeyi Kes ve BİR tarafını sil (clear_inner=True)
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bisect(
                    plane_co=plane_co, plane_no=plane_no, 
                    use_fill=False, clear_inner=True, clear_outer=False
                )
                bpy.ops.object.mode_set(mode='OBJECT')
                obj.select_set(False)

                # 3. Kopya Objeyi Kes ve DİĞER tarafını sil (clear_outer=True)
                bpy.context.view_layer.objects.active = new_obj
                new_obj.select_set(True)
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bisect(
                    plane_co=plane_co, plane_no=plane_no, 
                    use_fill=False, clear_inner=False, clear_outer=True
                )
                bpy.ops.object.mode_set(mode='OBJECT')
                new_obj.select_set(False)

                # 4. Sonsuz Döngü Koruması
                # Eğer bisect bıçağı boşa salladıysa (obje düzlem dışındaysa), bir obje tamamen boş kalır. Onu sil.
                valid_parts = []
                for part in [obj, new_obj]:
                    if len(part.data.polygons) == 0:
                        bpy.data.objects.remove(part, do_unlink=True)
                    else:
                        valid_parts.append(part)

                return valid_parts

        except Exception as e:
            print(f"[GKST MESH CRITICAL] Split error: {e}")
            return None

    @staticmethod
    def split_object_recursive(obj: bpy.types.Object, limit: int = 10000) -> bool:
        if not obj or obj.type != 'MESH':
            print(f"[GKST SPLIT ERROR] Invalid object: {obj}")
            return False

        obj.data.calc_loop_triangles()
        tri_count = len(obj.data.loop_triangles)

        print(f"\n>>> [GKST SPLIT START: {obj.name}] <<<")
        print(f"[GKST SPLIT] Current triangles: {tri_count:,} | Limit: {limit:,}")

        if tri_count <= limit:
            print(f"[GKST SPLIT INFO] {obj.name} is under limit. No split needed.")
            print(f">>> [GKST SPLIT END] <<<\n")
            return True

        print(f"[GKST SPLIT ACTION] Splitting {obj.name} ({tri_count:,} > {limit:,})...")
        resulting_parts = GKSTMeshSplitter._split_single_cut(obj)

        # CRITICAL FIX: Sonsuz Döngüyü (Blender donmasını) engeller
        if not resulting_parts or len(resulting_parts) <= 1:
            print(f"[GKST SPLIT WARNING] {obj.name} daha fazla bolunemiyor (Sonsuz dongu korumasi devreye girdi).")
            print(f">>> [GKST SPLIT END] <<<\n")
            return False

        print(f"[GKST SPLIT] {obj.name} split into {len(resulting_parts)} parts")

        # Çıkan parçaları tekrar kontrol et, büyükse tekrar böl
        for part in resulting_parts:
            part.data.calc_loop_triangles()
            part_tri_count = len(part.data.loop_triangles)
            print(f"[GKST SPLIT] Part {part.name}: {part_tri_count:,} triangles")
            
            if part_tri_count > limit:
                print(f"[GKST SPLIT] Part hala limit uzerinde, alt parcalara bolunuyor...")
                GKSTMeshSplitter.split_object_recursive(part, limit)

        print(f">>> [GKST SPLIT END] <<<\n")
        return True

    @staticmethod
    def split_object(obj: bpy.types.Object, limit: int = 9500) -> bool:
        return GKSTMeshSplitter.split_object_recursive(obj, limit)