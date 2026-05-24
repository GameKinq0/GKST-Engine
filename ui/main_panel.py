import bpy
import mathutils
import os
from ..core.lod_generator import GKSTLODGenerator
from ..core.collision_builder import GKSTCollisionBuilder
from ..exporters.smart_exporter import GKSTSmartExporter
from ..core.mesh_utils import GKSTMeshSplitter

# --- INITIALIZE PROPERTIES ---
def init_properties():
    bpy.types.Scene.gkst_target_engine = bpy.props.EnumProperty(
        name="Target Engine",
        items=[
            ('ROBLOX', "Roblox Studio", "Roblox (Auto Chunking)"),
            ('UNREAL', "Unreal Engine", "Unreal (Auto Lightmap)"),
            ('UNITY', "Unity 3D", "Unity (Scale Fix)")
        ],
        default='ROBLOX'
    )
    bpy.types.Scene.gkst_export_path = bpy.props.StringProperty(
        name="Output Folder", default="//", subtype='DIR_PATH'
    )
    bpy.types.Scene.gkst_lod_count = bpy.props.IntProperty(name="LOD Levels", default=3, min=1, max=6)
    bpy.types.Scene.gkst_lod_ratio = bpy.props.FloatProperty(name="Reduction Ratio", default=0.5, min=0.1, max=0.9)
    bpy.types.Scene.gkst_export_textures = bpy.props.BoolProperty(name="Export Textures", default=True)
    bpy.types.Scene.gkst_auto_split = bpy.props.BoolProperty(name="Auto-Split (>10k)", default=True)

def clear_properties():
    props = ["gkst_target_engine", "gkst_export_path", "gkst_lod_count", "gkst_lod_ratio", "gkst_export_textures", "gkst_auto_split"]
    for p in props:
        if hasattr(bpy.types.Scene, p): 
            delattr(bpy.types.Scene, p)

# --- MAIN PANEL ---
class GKST_PT_MainPanel(bpy.types.Panel):
    bl_label = "GameKing Engine v2.5"
    bl_idname = "GKST_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GKST Toolkit'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object

        # Scene Statistics
        box = layout.box()
        box.label(text="Scene Statistics", icon='OUTLINER_OB_MESH')
        if obj and obj.type == 'MESH':
            obj.data.calc_loop_triangles()
            tri_count = len(obj.data.loop_triangles)
            box.label(text=f"Active: {obj.name}", icon='MESH_DATA')
            box.label(text=f"Triangle Count: {tri_count:,}", icon='MOD_DECIM')
        else:
            box.label(text="Select a Mesh first.", icon='ERROR')

        layout.separator()

        # Pipeline Settings
        col = layout.column(align=True)
        col.label(text="1. Engine & Output:", icon='PREFERENCES')
        col.prop(scene, "gkst_target_engine")
        col.prop(scene, "gkst_export_path")
        
        # Dynamic UI: Show Roblox options only if selected
        if scene.gkst_target_engine == 'ROBLOX':
            col.prop(scene, "gkst_auto_split", text="Roblox Poly Limit Protection")
            
        col.prop(scene, "gkst_export_textures", icon='MATERIAL')

        layout.separator()

        # Manual Tools
        layout.label(text="2. Manual Modules:", icon='MODIFIER')
        row = layout.row(align=True)
        row.operator("gkst.origin_to_bottom", text="Set Pivot to Bottom", icon='TRIA_DOWN')
        row.operator("gkst.purge_data", text="Clean & Unwrap UV", icon='UV')
        
        row2 = layout.row(align=True)
        row2.operator("gkst.split_mesh", text="Split Now", icon='MESH_GRID')
        row2.operator("gkst.extract_textures", text="Extract Textures Only", icon='FILE_IMAGE')

        grid = layout.grid_flow(columns=2, align=True)
        grid.prop(scene, "gkst_lod_count")
        grid.prop(scene, "gkst_lod_ratio")
        
        row3 = layout.row(align=True)
        row3.operator("gkst.generate_lod", text="Manual LOD", icon='MOD_LATTICE')
        row3.operator("gkst.build_collision", text="Manual Collision", icon='MESH_ICOSPHERE')

        layout.separator()

        # MASTER PIPELINE BUTTON
        box_master = layout.box()
        box_master.scale_y = 1.5
        box_master.operator("gkst.master_execute", text="1-CLICK MASTER PIPELINE", icon='PLAY')

# --- OPERATORS ---

class GKST_OT_ExtractTextures(bpy.types.Operator):
    bl_idname = "gkst.extract_textures"
    bl_label = "Extract Textures Only"
    
    def execute(self, context):
        scene = context.scene
        path = bpy.path.abspath(scene.gkst_export_path)
        
        if not path or path == "//":
            self.report({'ERROR'}, "GKST: Export folder not specified!")
            return {'FINISHED'}
        
        success_count = 0
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                exporter = GKSTSmartExporter(obj, path, scene.gkst_target_engine)
                if exporter.execute_export(export_mesh=False, export_textures=True):
                    success_count += 1
        
        self.report({'INFO'}, f"GKST: Textures extracted from {success_count} object(s).")
        return {'FINISHED'}

class GKST_OT_MasterExecute(bpy.types.Operator):
    bl_idname = "gkst.master_execute"
    bl_label = "Master Pipeline Execute"
    bl_description = "Execute complete pipeline: Split -> LOD -> Collision -> Textures -> Export"
    
    def execute(self, context):
        scene = context.scene
        path = bpy.path.abspath(scene.gkst_export_path)
        
        if not path or path == "//":
            self.report({'ERROR'}, "GKST: Export folder not specified!")
            return {'FINISHED'}
        
        selected_objects = list(context.selected_objects)
        if not selected_objects:
            self.report({'ERROR'}, "GKST: Select at least one object.")
            return {'FINISHED'}
        
        context.window_manager.progress_begin(0, len(selected_objects))
        
        for i, obj in enumerate(selected_objects):
            if obj.type != 'MESH': 
                continue
            
            bpy.context.view_layer.objects.active = obj
            
            # 1. Auto-Split (Roblox only)
            if scene.gkst_target_engine == 'ROBLOX' and scene.gkst_auto_split:
                obj.data.calc_loop_triangles()
                if len(obj.data.loop_triangles) > 9500:
                    print(f"[GKST PIPELINE] Splitting: {obj.name}")
                    GKSTMeshSplitter.split_object(obj, limit=9500)
            
            # 2. LOD Generation
            print(f"[GKST PIPELINE] Generating LODs: {obj.name}")
            GKSTLODGenerator(obj).generate_lods()
            
            # 3. Collision
            print(f"[GKST PIPELINE] Building collision: {obj.name}")
            GKSTCollisionBuilder(obj, scene.gkst_target_engine).build_convex_hull()
            
            # 4. Export
            print(f"[GKST PIPELINE] Exporting: {obj.name}")
            exporter = GKSTSmartExporter(obj, path, scene.gkst_target_engine)
            exporter.execute_export(export_mesh=True, export_textures=scene.gkst_export_textures)
            
            context.window_manager.progress_update(i)
            
        context.window_manager.progress_end()
        self.report({'INFO'}, f"GKST PIPELINE COMPLETE! Output: {path}")
        return {'FINISHED'}

class GKST_OT_OriginToBottom(bpy.types.Operator):
    bl_idname = "gkst.origin_to_bottom"
    bl_label = "Set Pivot to Ground"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
                min_z = min([v.z for v in bbox])
                center_x = sum([v.x for v in bbox]) / 8
                center_y = sum([v.y for v in bbox]) / 8
                bpy.context.scene.cursor.location = (center_x, center_y, min_z)
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        return {'FINISHED'}

class GKST_OT_PurgeData(bpy.types.Operator):
    bl_idname = "gkst.purge_data"
    bl_label = "Clean & Unwrap"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                try:
                    bpy.ops.uv.smart_project(angle_limit=1.15192, island_margin=0.01)
                except:
                    pass
                bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_recursive=True)
        return {'FINISHED'}

class GKST_OT_SplitMeshOperator(bpy.types.Operator):
    bl_idname = "gkst.split_mesh"
    bl_label = "Split to 10k Limit"
    
    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            GKSTMeshSplitter.split_object(obj, limit=9500)
        return {'FINISHED'}

class GKST_OT_GenerateLOD(bpy.types.Operator):
    bl_idname = "gkst.generate_lod"
    bl_label = "Generate LOD"
    
    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            GKSTLODGenerator(obj).generate_lods()
        return {'FINISHED'}

class GKST_OT_BuildCollision(bpy.types.Operator):
    bl_idname = "gkst.build_collision"
    bl_label = "Add Collision"
    
    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            GKSTCollisionBuilder(obj, context.scene.gkst_target_engine).build_convex_hull()
        return {'FINISHED'}

# --- REGISTRATION ---
classes = (
    GKST_PT_MainPanel, 
    GKST_OT_OriginToBottom, 
    GKST_OT_PurgeData, 
    GKST_OT_SplitMeshOperator, 
    GKST_OT_GenerateLOD, 
    GKST_OT_BuildCollision, 
    GKST_OT_ExtractTextures,
    GKST_OT_MasterExecute
)

def register():
    init_properties()
    for cls in classes: 
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes): 
        bpy.utils.unregister_class(cls)
    clear_properties()
