import bpy


# Listup Selected Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_remove_loc_keys(bpy.types.Operator):
    bl_idname = "anime_pose_tools.remove_loc_keys"
    bl_label = "Loc"

    # execute
    def execute(self, context):
        return{'FINISHED'}

class ANIME_POSE_TOOLS_OT_remove_rot_keys(bpy.types.Operator):
    bl_idname = "anime_pose_tools.remove_rot_keys"
    bl_label = "Rot"

    # execute
    def execute(self, context):
        return{'FINISHED'}

class ANIME_POSE_TOOLS_OT_remove_scale_keys(bpy.types.Operator):
    bl_idname = "anime_pose_tools.remove_scale_keys"
    bl_label = "Scale"

    # execute
    def execute(self, context):
        return{'FINISHED'}

class ANIME_POSE_TOOLS_OT_remove_other_keys(bpy.types.Operator):
    bl_idname = "anime_pose_tools.remove_other_keys"
    bl_label = "Other"

    # execute
    def execute(self, context):
        return{'FINISHED'}



# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Remove Keys from All Frame:")
    box = layout.box()
    row = box.row()
    row.operator("anime_pose_tools.remove_loc_keys")
    row.operator("anime_pose_tools.remove_rot_keys")
    row.operator("anime_pose_tools.remove_scale_keys")
    row.operator("anime_pose_tools.remove_other_keys")

