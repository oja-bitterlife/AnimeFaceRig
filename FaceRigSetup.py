import bpy, mathutils
from . import ResetStretch

APT_FR_CONTROL_BONE_PREFIX = "APT_FR_ctrl_"


# 選択中のBoneのRollを設定する
# =================================================================================================
class ANIME_POSE_TOOLS_OT_setup_facerig_from_deform_bones(bpy.types.Operator):
    bl_idname = "anime_pose_tools.setup_facerig_from_deform_bones"
    bl_label = "Setup FaceRig From Deform Bones"

    # execute
    def execute(self, context):
        # 編集対象ボーンの回収
        armature = bpy.context.active_object
        selected_bones = []
        for bone in armature.data.edit_bones:
            if bone.select and is_layer_enable(armature, bone):
                selected_bones.append(bone)

        # deform_boneだけ選別しておく
        deform_bones = [bone for bone in selected_bones if bone.use_deform]

        # 以前の設定を一旦削除
        remove_from_selected(context, armature, selected_bones)

        marge_threshold = 0.0001

        if len(deform_bones) > 0:
            control_bone_size = 0
            for db in deform_bones:
                control_bone_size += (db.tail-db.head).length
            control_bone_size = control_bone_size / len(deform_bones) * 1.5
        else:
            control_bone_size = 1.0

        # headの位置にControlBoneを生やす
        new_control_bones = []
        for bone in deform_bones:
            # 近い位置にControlBoneがない場合のみ生成
            head_nearest_bone = self.find_nearest_bone(bone.head, new_control_bones, marge_threshold)
            if not head_nearest_bone:
                new_bone = self.create_ctrl_bone(armature, bone.name, bone.head, control_bone_size)
                new_control_bones.append(new_bone)
            else:
                new_bone = head_nearest_bone

            # headの位置のControlBoneは親にする
            bone.use_connect = False
            bone.parent = new_bone

        # tailの位置にControlBoneを生やす
        for bone in deform_bones:
            # 近い位置にControlBoneがない場合のみ生成
            if not self.find_nearest_bone(bone.tail, new_control_bones, marge_threshold):
                new_bone = self.create_ctrl_bone(armature, bone.name, bone.tail, control_bone_size)
                new_control_bones.append(new_bone)

        # constraintの設定(tailが重なっているのがtarget)
        for bone in deform_bones:
            target_bone = self.find_nearest_bone(bone.tail, new_control_bones)
            if target_bone:
                self.create_constraints(context, bone, armature, target_bone)

        return {'FINISHED'}

    # リスト内に近い頂点がないか調べる
    def find_nearest_bone(self, point, bone_list, threshold=0.000001):
        nearest_bone = None
        min_length = threshold
        for b in bone_list:
            length = (b.head-point).length
            # 0より小さくなることはないので終了            
            if length == 0:
                return b

            # 距離がより近いBoneを選択する
            if length < min_length:
                nearest_bone = b
                min_length = length

        return nearest_bone  # 頂点が近いBoneがなかった

    # ControlBoneを生やす
    def create_ctrl_bone(self, armature, base_name, point, ctrl_bone_size=1.0):
        ctrl_bone = armature.data.edit_bones.new(APT_FR_CONTROL_BONE_PREFIX + base_name)
        ctrl_bone.use_connect = False
        ctrl_bone.use_deform = False
        ctrl_bone.head = point
        ctrl_bone.tail = point + mathutils.Vector((0, -ctrl_bone_size, 0))

        return ctrl_bone

    # コンストレイントを設定する
    def create_constraints(self, context, edit_bone, target_armature, target_bone):
        pose_bone = context.object.pose.bones[edit_bone.name]

        damped_track = pose_bone.constraints.new("DAMPED_TRACK")
        damped_track.target = bpy.data.objects[target_armature.name]
        damped_track.subtarget = target_bone.name
        damped_track.name = APT_FR_CONTROL_BONE_PREFIX + "DAMPED_TRACK"

        stretch_to = pose_bone.constraints.new("STRETCH_TO")
        stretch_to.target = bpy.data.objects[target_armature.name]
        stretch_to.subtarget = target_bone.name
        stretch_to.name = APT_FR_CONTROL_BONE_PREFIX + "STRETCH_TO"


# ボーン名規約に沿ったボーンを削除する
# =================================================================================================
class ANIME_POSE_TOOLS_OT_remove_facerig_from_selected(bpy.types.Operator):
    bl_idname = "anime_pose_tools.remove_facerig_by_prefix"
    bl_label = "Remove FaceRig From Selected"

    # execute
    def execute(self, context):
        # 編集対象ボーンの回収
        armature = bpy.context.active_object
        selected_bones = []
        for bone in armature.data.edit_bones:
            if bone.select and is_layer_enable(armature, bone):
                selected_bones.append(bone)

        remove_from_selected(context, armature, selected_bones)

        return {'FINISHED'}

def remove_from_selected(context, armature, edit_bone_list):
    for bone in edit_bone_list:
        # Prefixチェック
        if bone.name.startswith(APT_FR_CONTROL_BONE_PREFIX) and not bone.use_deform:
            armature.data.edit_bones.remove(bone)
            continue

        pose_bone = context.object.pose.bones[bone.name]
        for constraint in pose_bone.constraints:
            if constraint.name.startswith(APT_FR_CONTROL_BONE_PREFIX):
                pose_bone.constraints.remove(constraint)


# boneが含まれているレイヤーがArmatureの表示レイヤーになっているかどうか
def is_layer_enable(armature, edit_bone):
    for i, b in enumerate(edit_bone.layers):
        if b:
            return armature.data.layers[i]
    return False


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    # 選択中BoneにControll用Boneを生やす
    layout.label(text="Face Rig Setting:")
    box = layout.box()
    box.operator("anime_pose_tools.setup_facerig_from_deform_bones")
    box.operator("anime_pose_tools.remove_facerig_by_prefix")

