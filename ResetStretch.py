import bpy
from . import FaceRigSetup

# ボーン名規約に沿ったボーンを削除する
# =================================================================================================
class ANIME_POSE_TOOLS_OT_reset_facerig_stretchto(bpy.types.Operator):
    bl_idname = "anime_face_rig.reset_facerig_stretchto"
    bl_label = "Reset StretchTo"

    # execute
    def execute(self, context):
        armature = bpy.context.active_object

        # 選択中のボーンだけ処理
        selected_bones = bpy.context.selected_pose_bones
        for pose_bone in selected_bones:
            # opsを使うためにアクティブにする
            bone = context.object.data.bones[pose_bone.name]
            armature.data.bones.active = bone

            # すべてのコンストレイントをチェック
            for c in pose_bone.constraints:
                # 名前とタイプが一致したらリセット
                if c.name.startswith(FaceRigSetup.APT_FR_CONTROL_BONE_PREFIX) and c.type == "STRETCH_TO":
                    bpy.ops.constraint.stretchto_reset(constraint=c.name, owner='BONE')

        return {'FINISHED'}


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    # 選択中BoneにControll用Boneを生やす
    layout.label(text="Face Rig Setting:")
    box = layout.box()
    box.operator("anime_face_rig.reset_facerig_stretchto")
