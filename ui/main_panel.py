import bpy
import mathutils
import os
from ..core.lod_generator import GKSTLODGenerator
from ..core.collision_builder import GKSTCollisionBuilder
from ..exporters.smart_exporter import GKSTSmartExporter
from ..core.mesh_utils import GKSTMeshSplitter

# --- KULLANICI AYARLARI ---
def init_properties():
    bpy.types.Scene.gkst_target_engine = bpy.props.EnumProperty(
        name="Hedef Motor",
        items=[
            ('ROBLOX', "Roblox Studio", "Roblox (Otomatik Parçalama)"),
            ('UNREAL', "Unreal Engine", "Unreal (Otomatik Lightmap)"),
            ('UNITY', "Unity 3D", "Unity (Scale Düzeltmesi)")
        ],
        default='ROBLOX'
    )
    bpy.types.Scene.gkst_export_path = bpy.props.StringProperty(
        name="Çıktı Klasörü", default="//", subtype='DIR_PATH'
    )
    bpy.types.Scene.gkst_lod_count = bpy.props.IntProperty(name="LOD Seviyesi", default=3, min=1, max=6)
    bpy.types.Scene.gkst_lod_ratio = bpy.props.FloatProperty(name="Azaltma Oranı", default=0.5, min=0.1, max=0.9)
    
    # Yeni Ayarlar
    bpy.types.Scene.gkst_export_textures = bpy.props.BoolProperty(name="Dokuları (Texture) Çıkar", default=True)
    bpy.types.Scene.gkst_auto_split = bpy.props.BoolProperty(name="Oto-Parçala (>10k)", default=True)

def clear_properties():
    props = ["gkst_target_engine", "gkst_export_path", "gkst_lod_count", "gkst_lod_ratio", "gkst_export_textures", "gkst_auto_split"]
    for p in props:
        if hasattr(bpy.types.Scene, p): delattr(bpy.types.Scene, p)

# --- PANEL ÇİZİMİ ---
class GKST_PT_MainPanel(bpy.types.Panel):
    bl_label = "GameKing Engine v3.5 (PRO)"
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
        
        # Dinamik Arayüz: Sadece Roblox seçiliyse Poly limit göster
        if scene.gkst_target_engine == 'ROBLOX':
            col.prop(scene, "gkst_auto_split", text="Roblox Poly Limit Koruması")
            
        col.prop(scene, "gkst_export_textures", icon='MATERIAL')

        layout.separator()

        # Manuel Araçlar
        layout.label(text="2. Manuel Modüller:", icon='MODIFIER')
        row = layout.row(align=True)
        row.operator("gkst.origin_to_bottom", text="Pivot'u Zemine Al", icon='TRIA_DOWN')
        row.operator("gkst.purge_data", text="Temizle & UV Aç", icon='UV')
        
        row2 = layout.row(align=True)
        row2.operator("gkst.split_mesh", text="Hemen Parçala", icon='MESH_GRID')
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
# Yeni: Sadece Doku Çıkarma
class GKST_OT_ExtractTextures(bpy.types.Operator):
    bl_idname = "gkst.extract_textures"
    bl_label = "Sadece Texture Çıkar"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        path = bpy.path.abspath(scene.gkst_export_path)
        
        if not path or path == "//":
            self.report({'ERROR'}, "GKST: Lütfen geçerli bir dışa aktarma yolu seçin.")
            return {'CANCELLED'}
        
        exported_count = 0
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                exporter = GKSTSmartExporter(obj, path, scene.gkst_target_engine)
                if exporter.execute_export(export_mesh=False, export_textures=True):
                    exported_count += 1
        
        self.report({'INFO'}, f"GKST: {exported_count} obje(nin) texture'ları başarıyla çıkarıldı.")
        return {'FINISHED'}

# Yeni: 1-Click Master Execute (Tüm Pipeline)
class GKST_OT_MasterExecute(bpy.types.Operator):
    bl_idname = "gkst.master_execute"
    bl_label = "Master Pipeline Başlat"
    bl_description = "Seçili objelere sırasıyla: Parçalama(Roblox) -> LOD -> Collision -> Texture Çıkarma -> FBX Export uygular."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        path = bpy.path.abspath(scene.gkst_export_path)
        
        # BUG FIX: Export path validation
        if not path or path == "//":
            self.report({'ERROR'}, "GKST: Lütfen geçerli bir dışa aktarma yolu seçin.")
            return {'CANCELLED'}
        
        if not context.selected_objects:
            self.report({'ERROR'}, "GKST: Lütfen en az bir mesh seçin.")
            return {'CANCELLED'}
        
        # Blender'ın fare imlecini işlem sürüyor (kum saati) ikonuna çevir (UX)
        mesh_objects = [o for o in context.selected_objects if o.type == 'MESH']
        context.window_manager.progress_begin(0, len(mesh_objects))
        
        try:
            for i, obj in enumerate(mesh_objects):
                if obj.type != 'MESH': 
                    continue
                
                bpy.context.view_layer.objects.active = obj
                
                # 1. Otomatik Parçalama (Eğer Roblox ise ve açıksa)
                if scene.gkst_target_engine == 'ROBLOX' and scene.gkst_auto_split:
                    obj.data.calc_loop_triangles()
                    if len(obj.data.loop_triangles) > 9500:
                        if not GKSTMeshSplitter.split_object(obj, limit=9500):
                            self.report({'WARNING'}, f"GKST: {obj.name} parçalama işlemi başarısız oldu.")
                
                # 2. LOD Üretimi
                try:
                    GKSTLODGenerator(obj).generate_lods()
                except Exception as e:
                    self.report({'WARNING'}, f"GKST: {obj.name} LOD üretimi başarısız: {str(e)}")
                
                # 3. Collision
                try:
                    GKSTCollisionBuilder(obj, scene.gkst_target_engine).build_convex_hull()
                except Exception as e:
                    self.report({'WARNING'}, f"GKST: {obj.name} collision oluşturması başarısız: {str(e)}")
                
                # 4. FBX ve Texture Export
                try:
                    exporter = GKSTSmartExporter(obj, path, scene.gkst_target_engine)
                    exporter.execute_export(export_mesh=True, export_textures=scene.gkst_export_textures)
                except Exception as e:
                    self.report({'WARNING'}, f"GKST: {obj.name} dışa aktarması başarısız: {str(e)}")
                
                context.window_manager.progress_update(i)
                
        finally:
            context.window_manager.progress_end()
        
        self.report({'INFO'}, f"GKST MASTER PIPELINE TAMAMLANDI! Klasör: {path}")
        return {'FINISHED'}

class GKST_OT_OriginToBottom(bpy.types.Operator):
    bl_idname = "gkst.origin_to_bottom"
    bl_label = "Pivot'u Zemine Al"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects_modified = 0
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                try:
                    bpy.context.view_layer.objects.active = obj
                    bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
                    min_z = min([v.z for v in bbox])
                    center_x = sum([v.x for v in bbox]) / 8
                    center_y = sum([v.y for v in bbox]) / 8
                    bpy.context.scene.cursor.location = (center_x, center_y, min_z)
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                    objects_modified += 1
                except Exception as e:
                    self.report({'WARNING'}, f"GKST: {obj.name} için origin ayarı başarısız: {str(e)}")
        
        self.report({'INFO'}, f"GKST: {objects_modified} objenin origin'i ayarlandı.")
        return {'FINISHED'}

class GKST_OT_PurgeData(bpy.types.Operator):
    bl_idname = "gkst.purge_data"
    bl_label = "Temizle/UV"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects_modified = 0
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                try:
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    try:
                        bpy.ops.uv.smart_project(angle_limit=1.15192, island_margin=0.01)
                    except RuntimeError:
                        # Smart project may fail, continue anyway
                        pass
                    bpy.ops.object.mode_set(mode='OBJECT')
                    objects_modified += 1
                except Exception as e:
                    self.report({'WARNING'}, f"GKST: {obj.name} için temizlik başarısız: {str(e)}")
        
        try:
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_recursive=True)
        except Exception as e:
            self.report({'WARNING'}, f"GKST: Orphan veri silme başarısız: {str(e)}")
        
        self.report({'INFO'}, f"GKST: {objects_modified} obje temizlendi ve UV açıldı.")
        return {'FINISHED'}

class GKST_OT_SplitMeshOperator(bpy.types.Operator):
    bl_idname = "gkst.split_mesh"
    bl_label = "Parçaları 10k Limitine Ayır"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "GKST: Lütfen aktif olarak bir Mesh seçin.")
            return {'CANCELLED'}
        
        if GKSTMeshSplitter.split_object(obj, limit=9500):
            self.report({'INFO'}, f"GKST: {obj.name} başarıyla parçalara ayrıldı.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"GKST: {obj.name} parçalaması başarısız oldu.")
            return {'CANCELLED'}

class GKST_OT_GenerateLOD(bpy.types.Operator):
    bl_idname = "gkst.generate_lod"
    bl_label = "LOD Üret"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "GKST: Lütfen aktif olarak bir Mesh seçin.")
            return {'CANCELLED'}
        
        try:
            lods = GKSTLODGenerator(obj).generate_lods()
            self.report({'INFO'}, f"GKST: {len(lods)} LOD seviyesi oluşturuldu.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"GKST: LOD üretimi başarısız: {str(e)}")
            return {'CANCELLED'}

class GKST_OT_BuildCollision(bpy.types.Operator):
    bl_idname = "gkst.build_collision"
    bl_label = "Collision Ekle"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "GKST: Lütfen aktif olarak bir Mesh seçin.")
            return {'CANCELLED'}
        
        try:
            collider = GKSTCollisionBuilder(obj, context.scene.gkst_target_engine).build_convex_hull()
            if collider:
                self.report({'INFO'}, f"GKST: Collision başarıyla oluşturuldu.")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "GKST: Collision oluşturması başarısız oldu.")
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"GKST: Collision hatası: {str(e)}")
            return {'CANCELLED'}

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
