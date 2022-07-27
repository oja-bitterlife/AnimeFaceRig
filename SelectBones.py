import bpy
import re


# Listup Selected Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_bones_with_a_key(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_bones_with_a_key"
    bl_label = "With A Key"

    # execute
    def execute(self, context):
        armature = bpy.context.view_layer.objects.active

        # Aramtureが選択されていない
        if armature == None or armature.type != "ARMATURE":
            self.report({'ERROR'}, "activeなオブジェクトがArmatureじゃない(通常あり得ない)")
            return {'CANCELLED'}

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


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Select Bones:")
    box = layout.box()
    box.operator("anime_pose_tools.select_bones_with_a_key")
