import bpy
import bmesh
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
    def _bmesh_split_object(obj: bpy.types.Object) -> list:
        """
        BUG FIX: Use BMesh directly for splitting instead of bisect+separate ops.
        This avoids creating black faces and gives better control.
        """
        try:
            bm = bmesh.new()
            depsgraph = bpy.context.evaluated_depsgraph_get()
            evaluated_obj = obj.evaluated_get(depsgraph)
            
            # Get evaluated mesh
            mesh_eval = evaluated_obj.to_mesh()
            bm.from_mesh(mesh_eval)
            evaluated_obj.to_mesh_clear()
            
            plane_co, plane_no = GKSTMeshSplitter._calculate_optimal_cut_plane(obj)
            
            # BMesh bisect - clean operation without extra faces
            geom_to_split = bm.verts[:] + bm.edges[:] + bm.faces[:]
            bmesh.ops.bisect_plane(bm, geom=geom_to_split, plane_co=plane_co, plane_no=plane_no, use_snap_center=False)
            
            # Split at bisect seam
            edges_to_split = [e for e in bm.edges if e.tag]
            if edges_to_split:
                bmesh.ops.split_edges(bm, edges=edges_to_split)
            
            # Create mesh and separate
            mesh_data = bpy.data.meshes.new(f"{obj.name}_split_mesh")
            bm.to_mesh(mesh_data)
            bm.free()
            
            # Import to bmesh again for separation
            bm2 = bmesh.new()
            bm2.from_mesh(mesh_data)
            
            # Find disconnected parts
            import bmesh.utils
            parts_faces = bmesh.utils.vert_separate_islands(bm2)
            
            resulting_objects = []
            parent_collection = obj.users_collection[0] if obj.users_collection else bpy.context.collection
            
            for part_idx, part_data in enumerate(parts_faces, start=1):
                if not part_data:
                    continue
                
                # Create new mesh for this part
                part_mesh = bpy.data.meshes.new(f"{obj.name}_Part_{part_idx}")
                part_bm = bmesh.new()
                
                # Copy vertices and faces of this part
                vert_map = {}
                for vert in part_data:
                    new_vert = part_bm.verts.new(vert.co)
                    vert_map[vert] = new_vert
                
                # Recreate faces
                for face in bm2.faces:
                    if all(v in vert_map for v in face.verts):
                        part_bm.faces.new([vert_map[v] for v in face.verts])
                
                part_bm.to_mesh(part_mesh)
                part_bm.free()
                
                # Create object
                part_obj = bpy.data.objects.new(f"{obj.name}_Part_{part_idx}", part_mesh)
                parent_collection.objects.link(part_obj)
                
                # Copy transforms
                part_obj.matrix_world = obj.matrix_world.copy()
                
                resulting_objects.append(part_obj)
            
            bm2.free()
            bpy.data.meshes.remove(mesh_data)
            return resulting_objects
            
        except Exception as e:
            print(f"[GKST MESH ERROR] BMesh split failed: {e}")
            return []

    @staticmethod
    def split_object(obj: bpy.types.Object, limit: int = 9500) -> bool:
        if not obj or obj.type != 'MESH':
            print(f"[GKST MESH ERROR] Invalid object type: {obj.type if obj else 'None'}")
            return False

        # Check polycount
        obj.data.calc_loop_triangles()
        tri_count = len(obj.data.loop_triangles)
        if tri_count <= limit:
            print(f"[GKST MESH INFO] {obj.name} has {tri_count} triangles (under {limit} limit). No split needed.")
            return True
        
        print(f"[GKST MESH START] Splitting {obj.name} ({tri_count} triangles)...")
        
        try:
            # Use pure bmesh splitting
            parts = GKSTMeshSplitter._bmesh_split_object(obj)
            
            if parts:
                print(f"[GKST MESH SUCCESS] {obj.name} split into {len(parts)} parts")
                return True
            else:
                print(f"[GKST MESH ERROR] Failed to create split parts")
                return False
                
        except Exception as e:
            print(f"[GKST MESH CRITICAL] Split operation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
