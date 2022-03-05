import bpy, mathutils
import math

# from .Util.ListupUtil import ListupProperty


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
                self.create_constraints(bone, target_bone)

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
        ctrl_bone = armature.data.edit_bones.new("AFR_ctrl_" + base_name)
        ctrl_bone.use_connect = False
        ctrl_bone.use_deform = False
        ctrl_bone.head = point
        ctrl_bone.tail = point + mathutils.Vector((0, -ctrl_bone_size, 0))

        return ctrl_bone

    def create_constraints(self, bone, target_bone):
        print(bone)



# # 選択中BoneのConnect/Disconnect
# # =================================================================================================
# class ANIME_HAIR_TOOLS_OT_setup_bone_connect(bpy.types.Operator):
#     bl_idname = "anime_hair_tools.setup_bone_connect"
#     bl_label = "Connect All"

#     # execute
#     def execute(self, context):
#         # 編集対象ボーンの回収
#         armature = bpy.context.active_object
#         selected_bones = []
#         for bone in armature.data.edit_bones:
#             if bone.select and is_layer_enable(armature, bone):
#                 selected_bones.append(bone)

#         # connect
#         for bone in selected_bones:
#             bone.use_connect = True

#         return{'FINISHED'}


# class ANIME_HAIR_TOOLS_OT_setup_bone_disconnect(bpy.types.Operator):
#     bl_idname = "anime_hair_tools.setup_bone_disconnect"
#     bl_label = "Disconnect All"

#     # execute
#     def execute(self, context):
#         # 編集対象ボーンの回収
#         armature = bpy.context.active_object
#         selected_bones = []
#         for bone in armature.data.edit_bones:
#             if bone.select and is_layer_enable(armature, bone):
#                 selected_bones.append(bone)

#         # disconnect
#         for bone in selected_bones:
#             bone.use_connect = False

#         return{'FINISHED'}


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


# =================================================================================================
# def register():
#     # Rollの参照用メッシュ
#     bpy.types.Scene.AHT_roll_reference = bpy.props.PointerProperty(type=ListupProperty)
