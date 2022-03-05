import bpy, mathutils

AFR_CONTROL_BONE_PREFIX = "AFR_ctrl_"


# 選択中のBoneのRollを設定する
# =================================================================================================
class ANIME_HAIR_TOOLS_OT_setup_from_deform_bones(bpy.types.Operator):
    bl_idname = "anime_face_rig.setup_from_deform_bones"
    bl_label = "Setup From Deform Bones"

    # execute
    def execute(self, context):
        # 編集対象ボーンの回収
        armature = bpy.context.active_object
        selected_bones = []
        for bone in armature.data.edit_bones:
            if bone.select and is_layer_enable(armature, bone):
                selected_bones.append(bone)

        control_bones = [bone for bone in selected_bones if not bone.use_deform]
        deform_bones = [bone for bone in selected_bones if bone.use_deform]

        # 選択中のControlBoneを削除する
        for bone in control_bones:
            armature.data.edit_bones.remove(bone)

        marge_threshold = 0.0001

        # headの位置にControlBoneを生やす
        new_control_bones = []
        for bone in deform_bones:
            new_bone = self.create_ctrl_bone(armature, bone.name, bone.head)
            new_control_bones.append(new_bone)

            # headの位置のControlBoneは親にする
            bone.use_connect = False
            bone.parent = new_bone

        # tailの位置にControlBoneを生やす
        for bone in deform_bones:
            # tailの時は近い位置にControlBoneがない場合のみ生成
            if not self.find_nearest_bone(bone.tail, new_control_bones, marge_threshold):
                new_bone = self.create_ctrl_bone(armature, bone.name, bone.tail)
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
    def create_ctrl_bone(self, armature, base_name, point):
        ctrl_bone_size = 1.0
        ctrl_bone = armature.data.edit_bones.new(AFR_CONTROL_BONE_PREFIX + base_name)
        ctrl_bone.use_connect = False
        ctrl_bone.use_deform = False
        ctrl_bone.head = point
        ctrl_bone.tail = point + mathutils.Vector((0, -ctrl_bone_size, 0))

        return ctrl_bone

    # コンストレイントを設定する
    def create_constraints(self, context, edit_bone, target_armature, target_bone):
        pose_bone = context.object.pose.bones[edit_bone.name]

        damped_track = self.find_or_new_constraint(pose_bone, "DAMPED_TRACK")
        damped_track.target = bpy.data.objects[target_armature.name]
        damped_track.subtarget = target_bone.name

        stretch_to = self.find_or_new_constraint(pose_bone, "STRETCH_TO")
        stretch_to.target = bpy.data.objects[target_armature.name]
        stretch_to.subtarget = target_bone.name
        stretch_to.rest_length = (edit_bone.head-edit_bone.tail).length

    # コンストレイントをTypeで探す。なければ新規で作る
    def find_or_new_constraint(self, pose_bone, type_name):
        # すでに存在していたらそれを返す
        for c in pose_bone.constraints:
            if c.type == type_name:
                return c
        # なければ新たに作る
        return pose_bone.constraints.new(type_name)


# ボーン名規約に沿ったボーンを削除する
# =================================================================================================
class ANIME_FACE_RIG_OT_remove_by_prefix(bpy.types.Operator):
    bl_idname = "anime_face_rig.remove_by_prefix"
    bl_label = "Remove By Prefix(AFR_ctrl_)"

    # execute
    def execute(self, context):
        # 編集対象ボーンの回収
        armature = bpy.context.active_object
        selected_bones = []
        for bone in armature.data.edit_bones:
            if bone.select and is_layer_enable(armature, bone):
                selected_bones.append(bone)

        for bone in selected_bones:
            # Prefixチェック
            if bone.name.startswith(AFR_CONTROL_BONE_PREFIX):
                armature.data.edit_bones.remove(bone)

        return {'FINISHED'}


# ControlBoneを削除する
# =================================================================================================
class ANIME_FACE_RIG_OT_remove_control_bones(bpy.types.Operator):
    bl_idname = "anime_face_rig.remove_control_bones"
    bl_label = "Remove Control Bones"

    # execute
    def execute(self, context):
        # 編集対象ボーンの回収
        armature = bpy.context.active_object
        selected_bones = []
        for bone in armature.data.edit_bones:
            if bone.select and is_layer_enable(armature, bone):
                selected_bones.append(bone)

        for bone in selected_bones:
            # ControlBoneチェック
            if not bone.use_deform:
                armature.data.edit_bones.remove(bone)

        return{'FINISHED'}


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
    box.operator("anime_face_rig.setup_from_deform_bones")
    box.operator("anime_face_rig.remove_by_prefix")
    box.operator("anime_face_rig.remove_control_bones")


# =================================================================================================
# def register():
#     # Rollの参照用メッシュ
#     bpy.types.Scene.AHT_roll_reference = bpy.props.PointerProperty(type=ListupProperty)
