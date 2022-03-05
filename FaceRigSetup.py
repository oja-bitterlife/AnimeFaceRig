import bpy, mathutils

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

        # ControlBoneの置く場所を調べる
        ctrl_bone_points = []
        marge_threshold = 0.0001
        for bone in deform_bones:
            if not self.is_point_in_list(bone.head, ctrl_bone_points, marge_threshold):
                self.create_ctrl_bone(armature, bone.name, bone.head)
                ctrl_bone_points.append(bone.head)
            if not self.is_point_in_list(bone.tail, ctrl_bone_points, marge_threshold):
                self.create_ctrl_bone(armature, bone.name, bone.tail)
                ctrl_bone_points.append(bone.tail)

        return{'FINISHED'}

    # ControlBoneを生やす
    def create_ctrl_bone(self, armature, base_name, point):
        ctrl_bone_size = 1.0
        ctrl_bone = armature.data.edit_bones.new("AFR_ctrl_" + base_name)
        ctrl_bone.use_connect = False
        ctrl_bone.use_deform = False
        ctrl_bone.head = point
        ctrl_bone.tail = point + mathutils.Vector((0, -ctrl_bone_size, 0))


    # リスト内に近い頂点がないか調べる
    def is_point_in_list(self, point, point_list, threshold=0.0):
        for p in point_list:
            if (p-point).length <= threshold:
                return True
        return False



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
