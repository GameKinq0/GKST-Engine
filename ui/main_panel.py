import bpy
import mathutils
import os
from ..core.retopology_optimizer import GKSTRetopologyOptimizer
from ..core.lod_generator import GKSTLODGenerator
from ..core.collision_builder import GKSTCollisionBuilder
from ..exporters.smart_exporter import GKSTSmartExporter

# --- KULLANICI AYARLARI ---
def init_properties():
    bpy.types.Scene.gkst_target_engine = bpy.props.EnumProperty(
        name="Hedef Motor",
        items=[
            ('ROBLOX', "Roblox Studio", "Roblox (Otomatik Retopology)"),
            ('UNREAL', "Unreal Engine", "Unreal (Otomatik Lightmap)"),
            ('UNITY', "Unity 3D", "Unity (Scale Düzeltmesi)")
        ],
        default='ROBLOX'
    )
    bpy.types.Scene.gkst_export_path = bpy.props.StringProperty(
        name="Çıktı Klasörü", default="//", subtype='DIR_PATH'
    )
    bpy.types.Scene.gkst_target_poly_count = bpy.props.IntProperty(
        name="Hedef Polygon Sayısı", 
        default=5000, 
        min=100, 
        max=100000,
        description="Retopology sonrası hedef üçgen sayısı"
    )
    bpy.types.Scene.gkst_lod_count = bpy.props.IntProperty(name="LOD Seviyesi", default=3, min=1, max=6)
    bpy.types.Scene.gkst_lod_ratio = bpy.props.FloatProperty(name="Azaltma Oranı", default=0.5, min=0.1, max=0.9)
    bpy.types.Scene.gkst_export_textures = bpy.props.BoolProperty(name="Dokuları (Texture) Çıkar", default=True)

def clear_properties():
    props = ["gkst_target_engine", "gkst_export_path", "gkst_target_poly_count", "gkst_lod_count", "gkst_lod_ratio", "gkst_export_textures"]
    for p in props:
        if hasattr(bpy.types.Scene, p): delattr(bpy.types.Scene, p)

# --- PANEL ÇİZİMİ ---
class GKST_PT_MainPanel(bpy.types.Panel):
    bl_label = "GameKing Engine v3.1"
    bl_idname = "GKST_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GKST Toolkit'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object

        # İstatistikler (Box Layout)
        box = layout.box()
        box.label(text="Sahne İstatistikleri", icon='OUTLINER_OB_MESH')
        if obj and obj.type == 'MESH':
            obj.data.calc_loop_triangles()
            tri_count = len(obj.data.loop_triangles)
            box.label(text=f"Aktif Model: {obj.name}", icon='MESH_DATA')
            box.label(text=f"Üçgen Sayısı: {tri_count:,}", icon='MOD_DECIM')
        else:
            box.label(text="Lütfen bir Mesh seçin.", icon='ERROR')

        layout.separator()

        # Pipeline Ayarları
        col = layout.column(align=True)
        col.label(text="1. Motor ve Çıktı:", icon='PREFERENCES')
        col.prop(scene, "gkst_target_engine")
        col.prop(scene, "gkst_export_path")
        col.prop(scene, "gkst_target_poly_count", text="Hedef Polygon")
        col.prop(scene, "gkst_export_textures", icon='MATERIAL')

        layout.separator()

        # Manuel Araçlar
        layout.label(text="2. Manuel Modüller:", icon='MODIFIER')
        row = layout.row(align=True)
        row.operator("gkst.origin_to_bottom", text="Pivot'u Zemine Al", icon='TRIA_DOWN')
        row.operator("gkst.purge_data", text="Temizle & UV Aç", icon='UV')
        
        row2 = layout.row(align=True)
        row2.operator("gkst.retopology", text="Otomatik Retopology", icon='MOD_REMESH')
        row2.operator("gkst.extract_textures", text="Sadece Doku Al", icon='FILE_IMAGE')

        grid = layout.grid_flow(columns=2, align=True)
        grid.prop(scene, "gkst_lod_count")
        grid.prop(scene, "gkst_lod_ratio")
        
        row3 = layout.row(align=True)
        row3.operator("gkst.generate_lod", text="Manuel LOD", icon='MOD_LATTICE')
        row3.operator("gkst.build_collision", text="Manuel Collision", icon='MESH_ICOSPHERE')

        layout.separator()

        # MASTER PIPELINE BUTONU
        box_master = layout.box()
        box_master.scale_y = 1.5
        box_master.operator("gkst.master_execute", text="1-CLICK MASTER PIPELINE", icon='PLAY')

# --- OPERATÖRLER ---

# Otomatik Retopology
class GKST_OT_Retopology(bpy.types.Operator):
    bl_idname = "gkst.retopology"
    bl_label = "Otomatik Retopology"
    bl_description = "Modeli hedef polygon sayısına düşürmek için otomatik retopology uygula"
    
    def execute(self, context):
        scene = context.scene
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "GKST: Lütfen bir Mesh seçin.")
            return {'FINISHED'}
        
        target_poly = scene.gkst_target_poly_count
        print(f"\n[GKST RETOPO UI] Starting retopology: {obj.name} → {target_poly:,} polys")
        
        optimizer = GKSTRetopologyOptimizer(obj, target_poly)
        if optimizer.optimize():
            self.report({'INFO'}, f"GKST: Retopology başarılı! Hedef: {target_poly:,} poly")
        else:
            self.report({'WARNING'}, f"GKST: Retopology tamamlandı ama tam hedefe ulaşılamadı.")
        
        return {'FINISHED'}

# Sadece Doku Çıkarma
class GKST_OT_ExtractTextures(bpy.types.Operator):
    bl_idname = "gkst.extract_textures"
    bl_label = "Sadece Texture Çıkar"
    def execute(self, context):
        scene = context.scene
        path = bpy.path.abspath(scene.gkst_export_path)
        success_count = 0
        
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                exporter = GKSTSmartExporter(obj, path, scene.gkst_target_engine)
                if exporter.execute_export(export_mesh=False, export_textures=True):
                    success_count += 1
        
        self.report({'INFO'}, f"GKST: {success_count} objenin texture'ları başarıyla çıkarıldı.")
        return {'FINISHED'}

# 1-Click Master Execute (Tüm Pipeline)
class GKST_OT_MasterExecute(bpy.types.Operator):
    bl_idname = "gkst.master_execute"
    bl_label = "Master Pipeline Başlat"
    bl_description = "Retopology -> LOD -> Collision -> Texture Çıkarma -> FBX Export"
    
    def execute(self, context):
        scene = context.scene
        path = bpy.path.abspath(scene.gkst_export_path)
        
        if not path or path == "//":
            self.report({'ERROR'}, "GKST: Çıktı klasörü belirtilmedi!")
            return {'FINISHED'}
        
        selected_objects = list(context.selected_objects)
        if not selected_objects:
            self.report({'ERROR'}, "GKST: Lütfen en az bir obje seçin.")
            return {'FINISHED'}
        
        context.window_manager.progress_begin(0, len(selected_objects))
        
        for i, obj in enumerate(selected_objects):
            if obj.type != 'MESH': 
                continue
            
            bpy.context.view_layer.objects.active = obj
            
            # 1. Retopology (NEW!)
            print(f"[GKST PIPELINE] Retopology yapılıyor: {obj.name}")
            optimizer = GKSTRetopologyOptimizer(obj, scene.gkst_target_poly_count)
            optimizer.optimize()
            
            # 2. LOD Üretimi
            print(f"[GKST PIPELINE] LOD üretiliyor: {obj.name}")
            GKSTLODGenerator(obj).generate_lods()
            
            # 3. Collision
            print(f"[GKST PIPELINE] Collision oluşturuluyor: {obj.name}")
            GKSTCollisionBuilder(obj, scene.gkst_target_engine).build_convex_hull()
            
            # 4. FBX ve Texture Export
            print(f"[GKST PIPELINE] Export başlatılıyor: {obj.name}")
            exporter = GKSTSmartExporter(obj, path, scene.gkst_target_engine)
            exporter.execute_export(export_mesh=True, export_textures=scene.gkst_export_textures)
            
            context.window_manager.progress_update(i)
            
        context.window_manager.progress_end()
        self.report({'INFO'}, f"GKST MASTER PIPELINE TAMAMLANDI! Klasör: {path}")
        return {'FINISHED'}

# Origin To Bottom
class GKST_OT_OriginToBottom(bpy.types.Operator):
    bl_idname = "gkst.origin_to_bottom"
    bl_label = "Pivot'u Zemine Al"
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

# Purge Data
class GKST_OT_PurgeData(bpy.types.Operator):
    bl_idname = "gkst.purge_data"
    bl_label = "Temizle/UV"
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

# Generate LOD
class GKST_OT_GenerateLOD(bpy.types.Operator):
    bl_idname = "gkst.generate_lod"
    bl_label = "LOD Üret"
    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            GKSTLODGenerator(obj).generate_lods()
        return {'FINISHED'}

# Build Collision
class GKST_OT_BuildCollision(bpy.types.Operator):
    bl_idname = "gkst.build_collision"
    bl_label = "Collision Ekle"
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
    GKST_OT_GenerateLOD, 
    GKST_OT_BuildCollision, 
    GKST_OT_ExtractTextures,
    GKST_OT_Retopology,
    GKST_OT_MasterExecute
)

def register():
    init_properties()
    for cls in classes: bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes): bpy.utils.unregister_class(cls)
    clear_properties()
