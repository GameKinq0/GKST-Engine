import bpy
import bmesh
import mathutils
from typing import Optional, Dict, Any, List, Tuple

class GKSTMeshSplitter:
    """
    GKST Professional Mesh Splitting Engine.
    Recursively splits meshes by poly count limit until all parts are under the limit.
    No minimum threshold - splits even tiny meshes if requested.
    """

    @staticmethod
    def _calculate_optimal_cut_plane(obj: bpy.types.Object) -> Tuple[mathutils.Vector, mathutils.Vector]:
        """Calculates the cutting plane based on the longest axis of the bounding box."""
        local_coords = [mathutils.Vector(corner) for corner in obj.bound_box]
        
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
        
        # Determine the longest axis
        if dimensions.x >= dimensions.y and dimensions.x >= dimensions.z:
            plane_normal = world_rotation @ mathutils.Vector((1, 0, 0))
        elif dimensions.y >= dimensions.x and dimensions.y >= dimensions.z:
            plane_normal = world_rotation @ mathutils.Vector((0, 1, 0))
        else:
            plane_normal = world_rotation @ mathutils.Vector((0, 0, 1))

        return world_center, plane_normal.normalized()

    @staticmethod
    def _split_single_cut(obj: bpy.types.Object) -> Optional[List[bpy.types.Object]]:
        """
        Performs a single bisect operation on the object.
        Returns list of resulting objects after split.
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
                
                # CRITICAL FIX: use_fill=False prevents black UV-less artifacts
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
                
                return resulting_parts

        except Exception as e:
            print(f"[GKST MESH CRITICAL] Split error: {e}")
            return None
            
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
            except:
                pass

    @staticmethod
    def split_object_recursive(obj: bpy.types.Object, limit: int = 10000) -> bool:
        """
        Recursively splits object until all parts are under the poly limit.
        NO MINIMUM THRESHOLD - splits any poly count if requested.
        """
        if not obj or obj.type != 'MESH':
            print(f"[GKST SPLIT ERROR] Invalid object: {obj}")
            return False

        # Calculate triangle count (using loop_triangles for accuracy)
        obj.data.calc_loop_triangles()
        tri_count = len(obj.data.loop_triangles)

        print(f"\n>>> [GKST SPLIT START: {obj.name}] <<<")
        print(f"[GKST SPLIT] Current triangles: {tri_count:,} | Limit: {limit:,}")

        # If under limit, no split needed
        if tri_count <= limit:
            print(f"[GKST SPLIT INFO] {obj.name} is under limit ({tri_count:,} ≤ {limit:,}). No split needed.")
            print(f">>> [GKST SPLIT END] <<<\n")
            return True

        # Split this object
        print(f"[GKST SPLIT ACTION] Splitting {obj.name} ({tri_count:,} > {limit:,})...")
        resulting_parts = GKSTMeshSplitter._split_single_cut(obj)

        if not resulting_parts:
            print(f"[GKST SPLIT ERROR] Failed to split {obj.name}")
            print(f">>> [GKST SPLIT END] <<<\n")
            return False

        print(f"[GKST SPLIT] {obj.name} split into {len(resulting_parts)} parts")

        # Recursively check each part
        for part in resulting_parts:
            part.data.calc_loop_triangles()
            part_tri_count = len(part.data.loop_triangles)
            print(f"[GKST SPLIT] Part {part.name}: {part_tri_count:,} triangles")
            
            # Recursively split if still over limit
            if part_tri_count > limit:
                print(f"[GKST SPLIT] Part still over limit, splitting recursively...")
                GKSTMeshSplitter.split_object_recursive(part, limit)

        print(f">>> [GKST SPLIT END] <<<\n")
        return True

    # Legacy method for compatibility
    @staticmethod
    def split_object(obj: bpy.types.Object, limit: int = 9500) -> bool:
        """Legacy interface - calls recursive split."""
        return GKSTMeshSplitter.split_object_recursive(obj, limit)
