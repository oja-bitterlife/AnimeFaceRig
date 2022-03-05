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


        # size = 1.0
        # for bone in selected_bones:
        #     print(bone.head)
        #     ctrl_bone = armature.data.edit_bones.new(bone.name + "_AFR_ctrl")
        #     ctrl_bone.use_connect = False
        #     ctrl_bone.head = bone.head
        #     ctrl_bone.tail = bone.head + mathutils.Vector((0, 0, 1))

        return{'FINISHED'}


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
