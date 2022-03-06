import bpy


# Deform Bones
# =================================================================================================
class ANIME_FACE_RIG_OT_show_deform(bpy.types.Operator):
    bl_idname = "anime_face_rig.show_deform"
    bl_label = "Show Deform Bones"

    # execute
    def execute(self, context):
        # 全PoseBone対象
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            bone = context.object.data.bones[pose_bone.name]
            if bone.use_deform:
                pose_bone.bone.hide = False

        return {'FINISHED'}

class ANIME_FACE_RIG_OT_hide_deform(bpy.types.Operator):
    bl_idname = "anime_face_rig.hide_deform"
    bl_label = "Hide Deform Bones"

    # execute
    def execute(self, context):
        # 全PoseBone対象
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            bone = context.object.data.bones[pose_bone.name]
            if bone.use_deform:
                pose_bone.bone.hide = True

        return {'FINISHED'}

# Hide Control Bones
# =================================================================================================
class ANIME_FACE_RIG_OT_show_control(bpy.types.Operator):
    bl_idname = "anime_face_rig.show_control"
    bl_label = "Show Control Bones"

    # execute
    def execute(self, context):
        # 全PoseBone対象
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            bone = context.object.data.bones[pose_bone.name]
            if not bone.use_deform:
                pose_bone.bone.hide = False

        return {'FINISHED'}

class ANIME_FACE_RIG_OT_hide_control(bpy.types.Operator):
    bl_idname = "anime_face_rig.hide_control"
    bl_label = "Hide Control Bones"

    # execute
    def execute(self, context):
        # 全PoseBone対象
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            bone = context.object.data.bones[pose_bone.name]
            if not bone.use_deform:
                pose_bone.bone.hide = True

        return {'FINISHED'}


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    # 選択中BoneにControll用Boneを生やす
    layout.label(text="Face Rig Edit Support:")
    layout.operator("anime_face_rig.show_deform")
    layout.operator("anime_face_rig.hide_deform")
    layout.operator("anime_face_rig.show_control")
    layout.operator("anime_face_rig.hide_control")
