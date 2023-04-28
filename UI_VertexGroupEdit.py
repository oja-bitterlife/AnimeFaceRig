import bpy
from .VertexGroupEdit import VertexGroupEdit

modules = [
    VertexGroupEdit
]


class ANIME_POSE_TOOLS_PT_weight_util(bpy.types.Panel):
    bl_label = "Vertex Group Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "AHT_POSE_PT_UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        for i, module in enumerate(modules):
            if hasattr(module, "draw"):
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
