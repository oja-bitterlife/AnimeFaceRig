import bpy


# To Rest Position
# =================================================================================================
class ANIME_POSE_TOOLS_OT_to_rest(bpy.types.Operator):
    bl_idname = "anime_pose_tools.to_rest"
    bl_label = "Set Rest Position"

    # execute
    def execute(self, context):
        armature = bpy.context.active_object
        return {'FINISHED'}

# To Pose Position
# =================================================================================================
class ANIME_POSE_TOOLS_OT_to_pose(bpy.types.Operator):
    bl_idname = "anime_pose_tools.to_pose"
    bl_label = "Set Pose Position"

    # execute
    def execute(self, context):
        armature = bpy.context.active_object
        return {'FINISHED'}


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Change Position Mode:")
    box = layout.box()
    box.operator("anime_pose_tools.to_rest")
    box.operator("anime_pose_tools.to_pose")
