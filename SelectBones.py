import bpy
import re


# Listup Selected Bones
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


# Listup Selected Bones
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


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Select Bones:")

    box = layout.box()
    row = box.row()
    row.alignment = 'EXPAND'
    row.operator("anime_pose_tools.select_to_edge")
    row.operator("anime_pose_tools.select_to_top")
    box.operator("anime_pose_tools.select_bones_with_a_key")
