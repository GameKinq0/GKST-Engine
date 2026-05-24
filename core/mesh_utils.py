import bpy
import mathutils
from typing import Optional, Dict, Any

class GKSTMeshSplitter:
    """
    GKST Profesyonel Mesh Bölme Motoru.
    Modeli en uzun ekseninden hesaplayarak, UV'yi bozmadan ve siyah yüzey (artefakt) 
    oluşturmadan ikiye böler.
    """

    @staticmethod
    def _calculate_optimal_cut_plane(obj: bpy.types.Object):
        """BUG FIX: Add bounds checking for empty bound_box"""
        try:
            local_coords = [mathutils.Vector(corner) for corner in obj.bound_box]
            
            if not local_coords:
                print(f"[GKST MESH WARNING] Empty bound box for {obj.name}")
                return obj.location, mathutils.Vector((0, 0, 1))
            
            max_coord = mathutils.Vector((
                max(c[0] for c in local_coords), max(c[1] for c in local_coords), max(c[2] for c in local_coords)
            ))
            min_coord = mathutils.Vector((
                min(c[0] for c in local_coords), min(c[1] for c in local_coords), min(c[2] for c in local_coords)
            ))

            dimensions = max_coord - min_coord
            local_center = (max_coord + min_coord) / 2.0
            world_center = obj.matrix_world @ local_center
            world_rotation = obj.matrix_world.to_3x3()
            
            if dimensions.x >= dimensions.y and dimensions.x >= dimensions.z:
                plane_normal = world_rotation @ mathutils.Vector((1, 0, 0))
            elif dimensions.y >= dimensions.x and dimensions.y >= dimensions.z:
                plane_normal = world_rotation @ mathutils.Vector((0, 1, 0))
            else:
                plane_normal = world_rotation @ mathutils.Vector((0, 0, 1))

            return world_center, plane_normal.normalized()
        except Exception as e:
            print(f"[GKST MESH ERROR] Failed to calculate cut plane: {e}")
            return obj.location, mathutils.Vector((0, 0, 1))

    @staticmethod
    def split_object(obj: bpy.types.Object, limit: int = 9500) -> bool:
        if not obj or obj.type != 'MESH':
            print(f"[GKST MESH ERROR] Invalid object type: {obj.type if obj else 'None'}")
            return False

        # BUG FIX: Check for valid 3D view context
        window = bpy.context.window
        if not window:
            print("[GKST MESH ERROR] No active window context found")
            return False
        
        screen = window.screen
        if not screen:
            print("[GKST MESH ERROR] No screen found in window")
            return False
        
        area = next((a for a in screen.areas if a.type == 'VIEW_3D'), None)
        if not area:
            print("[GKST MESH ERROR] No 3D View area found")
            return False
        
        region = next((r for r in area.regions if r.type == 'WINDOW'), None)
        if not region:
            print("[GKST MESH ERROR] No window region found in 3D View")
            return False

        override: Dict[str, Any] = {
            'window': window, 'screen': screen, 'area': area, 'region': region,
            'scene': bpy.context.scene, 'view_layer': bpy.context.view_layer,
        }

        original_active_name = obj.name
        original_selected_names = [o.name for o in bpy.context.selected_objects]
        original_mode = obj.mode
        parent_collection = obj.users_collection[0] if obj.users_collection else bpy.context.collection

        try:
            with bpy.context.temp_override(**override):
                if original_mode != 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')

                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                plane_co, plane_no = GKSTMeshSplitter._calculate_optimal_cut_plane(obj)

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                
                # KRİTİK FİX: use_fill=False yapıldı. Ortaya siyah, UV'siz yüzey atması engellendi.
                bpy.ops.mesh.bisect(
                    plane_co=plane_co, 
                    plane_no=plane_no, 
                    use_fill=False, 
                    clear_inner=False, 
                    clear_outer=False
                )
                bpy.ops.mesh.split()
                bpy.ops.mesh.separate(type='LOOSE')
                bpy.ops.object.mode_set(mode='OBJECT')

                bpy.context.view_layer.update()

                resulting_parts = [o for o in bpy.context.selected_objects if o.type == 'MESH']
                
                for index, part in enumerate(resulting_parts, start=1):
                    part.name = f"{original_active_name}_Part_{index}"
                    if parent_collection not in list(part.users_collection):
                        parent_collection.objects.link(part)
            
            print(f"[GKST MESH SUCCESS] {obj.name} split into {len(resulting_parts)} parts")
            return True

        except Exception as e:
            print(f"[GKST MESH CRITICAL] Bölme Hatası: {e}")
            return False

        finally:
            try:
                with bpy.context.temp_override(**override):
                    bpy.ops.object.select_all(action='DESELECT')
                    for name in original_selected_names:
                        if name in bpy.data.objects:
                            bpy.data.objects[name].select_set(True)
                    if original_active_name in bpy.data.objects:
                        active_obj = bpy.data.objects[original_active_name]
                        bpy.context.view_layer.objects.active = active_obj
                        if active_obj.mode != original_mode:
                            bpy.ops.object.mode_set(mode=original_mode)
            except Exception as cleanup_error:
                print(f"[GKST MESH WARNING] Cleanup failed: {cleanup_error}")
