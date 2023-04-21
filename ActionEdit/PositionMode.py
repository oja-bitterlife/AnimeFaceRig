import bpy


# To Pose Position
# =================================================================================================
class ANIME_POSE_TOOLS_OT_to_pose(bpy.types.Operator):
    bl_idname = "anime_pose_tools.to_pose"
    bl_label = "Pose"

    # execute
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == "ARMATURE":
                obj.data.pose_position = 'POSE'

        return {'FINISHED'}


# To Rest Position
# =================================================================================================
class ANIME_POSE_TOOLS_OT_to_rest(bpy.types.Operator):
    bl_idname = "anime_pose_tools.to_rest"
    bl_label = "Rest"

    # execute
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == "ARMATURE":
                obj.data.pose_position = 'REST'

        return {'FINISHED'}


# UI描画設定
# =================================================================================================
label = "Change Position Mode"

classes = [
    ANIME_POSE_TOOLS_OT_to_pose,
    ANIME_POSE_TOOLS_OT_to_rest,
]

def draw(parent, context, layout):
    row = layout.row()
    row.operator("anime_pose_tools.to_pose")
    row.operator("anime_pose_tools.to_rest")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
