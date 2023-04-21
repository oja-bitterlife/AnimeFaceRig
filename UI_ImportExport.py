import bpy
from .ImportExport import AnimExport, ListupBones

modules = [
    AnimExport,
    ListupBones
]

class ANIME_POSE_TOOLS_PT_import_export(bpy.types.Panel):
    bl_label = "Import/Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "APT_POSE_PT_UI"
    bl_idname = "APT_POSE_PT_IMPORT_EXPORT"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        for i, module in enumerate(modules):
            if hasattr(module, "draw"):
                # if i > 0:
                #     self.layout.separator()
                if hasattr(module, "label"):
                    self.layout.label(text=module.label)
                module.draw(self, context, self.layout.box())

def register():
    for module in modules:
        if hasattr(module, "register"):
            module.register()

def unregister():
    for module in modules:
        if hasattr(module, "unregister"):
            module.unregister()
