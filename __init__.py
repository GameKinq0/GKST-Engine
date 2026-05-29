bl_info = {
    "name": "GameKing Asset Engine (GKST)",
    "author": "GameKinq0 (GameKing Studio)",
    "version": (3, 1, 0),
    "blender": (3, 6, 0),
    "category": "3D View",
}

import bpy
# Modülleri relative import ile bağla
from .ui import main_panel
from .core import lod_generator, collision_builder, mesh_utils
from .exporters import smart_exporter

def register():
    main_panel.register()
    print("[GKST LOG] GameKing Asset Engine v2.5 başarıyla yüklendi.")

def unregister():
    main_panel.unregister()
    print("[GKST LOG] GameKing Asset Engine devreden çıkarıldı.")