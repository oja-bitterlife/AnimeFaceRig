import bpy
from .ActionEdit import BoneSelector, BoneVisible, CursorToSelected, PositionMode

modules = [
    CursorToSelected,
    PositionMode,
    BoneSelector,
    BoneVisible,
] 

class ANIME_POSE_TOOLS_PT_action_edit(bpy.types.Panel):
    bl_label = "Action Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "APT_POSE_PT_UI"
    # bl_options = {'DEFAULT_CLOSED'}

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
