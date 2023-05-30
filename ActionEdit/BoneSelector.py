import bpy
import re


# Selecte Bones in frame
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_bones_with_a_key(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_bones_with_a_key"
    bl_label = "With A Key In Frame"

    # execute
    def execute(self, context):
        armature = bpy.context.view_layer.objects.active

        # 選択中ArmatureのBone名を取得
        bone_names = [bone.name for bone in armature.pose.bones]

        # 現在のActionを取得
        action = bpy.context.active_object.animation_data.action

        # 現在のフレーム
        current_frame = bpy.data.scenes[0].frame_current

        # 一旦Deselect
        for pose_bone in armature.pose.bones:
            pose_bone.bone.select = False

        # bone_namesに含まれるGroupを探す
        for fcurve in action.fcurves:
            # 現在のフレーム(co[0]参照)に絞る
            for point in fcurve.keyframe_points:
                if point.co[0] == current_frame:
                    # キーが選択中のArmatureのBoneなら選択
                    if fcurve.group.name in bone_names:
                        armature.pose.bones[fcurve.group.name].bone.select = True

        return{'FINISHED'}


# Select To Edge
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_to_edge(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_to_edge"
    bl_label = "To Edge"

    # execute
    def execute(self, context):
        for pose_bone in bpy.context.selected_pose_bones:
            self.rec_select_children(pose_bone)
        return{'FINISHED'}

    def rec_select_children(self, pose_bone):
        pose_bone.bone.select = True
        for child in pose_bone.children:
            self.rec_select_children(child)


# Select To Top
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_to_top(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_to_top"
    bl_label = "To Top"

    # execute
    def execute(self, context):
        for pose_bone in bpy.context.selected_pose_bones:
            self.rec_select_children(pose_bone)
        return{'FINISHED'}

    def rec_select_children(self, pose_bone):
        pose_bone.bone.select = True
        if pose_bone.parent:
            self.rec_select_children(pose_bone.parent)


# Select Plus Edge
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_plus_edge(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_plus_edge"
    bl_label = "+Edge"

    # execute
    def execute(self, context):
        for pose_bone in bpy.context.selected_pose_bones:
            for child in pose_bone.children:
                child.bone.select = True

        return{'FINISHED'}


# Select Plus Top
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_plus_top(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_plus_top"
    bl_label = "+Top"

    # execute
    def execute(self, context):
        for pose_bone in bpy.context.selected_pose_bones:
            if pose_bone.parent:
                pose_bone.parent.bone.select = True

        return{'FINISHED'}


# Select L/R
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_L(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_l"
    bl_label = "L"

    # execute
    def execute(self, context):
        # _LのみSelect
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            if "L" in re.split(r'[\._]', pose_bone.name.upper()):
                pose_bone.bone.select = True

        return {'FINISHED'}

class ANIME_POSE_TOOLS_OT_select_R(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_r"
    bl_label = "R"

    # execute
    def execute(self, context):
        # _RのみSelect
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            if "R" in re.split(r'[\._]', pose_bone.name.upper()):
                pose_bone.bone.select = True

        return {'FINISHED'}


# UI描画設定
# =================================================================================================
label = "Bone Selector"

classes = [
    ANIME_POSE_TOOLS_OT_select_bones_with_a_key,
    ANIME_POSE_TOOLS_OT_select_to_edge,
    ANIME_POSE_TOOLS_OT_select_to_top,
    ANIME_POSE_TOOLS_OT_select_plus_edge,
    ANIME_POSE_TOOLS_OT_select_plus_top,
    ANIME_POSE_TOOLS_OT_select_L,
    ANIME_POSE_TOOLS_OT_select_R,
]

def draw(parent, context, layout):
    if context.mode != "POSE":
        layout.enabled = False

    row = layout.row()
    row.operator("anime_pose_tools.select_plus_top")
    row.operator("anime_pose_tools.select_to_top")
    row = layout.row()
    row.operator("anime_pose_tools.select_plus_edge")
    row.operator("anime_pose_tools.select_to_edge")
    row = layout.row()
    row.operator("anime_pose_tools.select_l")
    row.operator("anime_pose_tools.select_r")
    layout.operator("anime_pose_tools.select_bones_with_a_key")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
