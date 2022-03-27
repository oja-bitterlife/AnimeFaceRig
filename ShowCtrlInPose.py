import bpy


# Show Only Deform Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_show_deform_only(bpy.types.Operator):
    bl_idname = "anime_pose_tools.show_deform_only"
    bl_label = "Show Deform Only"

    # execute
    def execute(self, context):
        # 全PoseBone対象
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            bone = context.object.data.bones[pose_bone.name]
            pose_bone.bone.hide = not bone.use_deform

        return {'FINISHED'}


# Show Only Control Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_show_control_only(bpy.types.Operator):
    bl_idname = "anime_pose_tools.show_control_only"
    bl_label = "Show Control Only"

    # execute
    def execute(self, context):
        # 全PoseBone対象
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            bone = context.object.data.bones[pose_bone.name]
            pose_bone.bone.hide = bone.use_deform

        return {'FINISHED'}


# Show All
# =================================================================================================
class ANIME_POSE_TOOLS_OT_show_all(bpy.types.Operator):
    bl_idname = "anime_pose_tools.show_all"
    bl_label = "Show All"

    # execute
    def execute(self, context):
        # 全PoseBone対象
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            pose_bone.bone.hide = False

        return {'FINISHED'}


# Reset All
# =================================================================================================
class ANIME_POSE_TOOLS_OT_reset_all(bpy.types.Operator):
    bl_idname = "anime_pose_tools.reset_all"
    bl_label = "Reset All Layers"

    # execute
    def execute(self, context):
        armature = bpy.context.active_object

        # ボーンの存在する全レイヤー表示
        visible_list = [False]*len(context.object.data.layers)
        for bone in armature.data.bones:
            for i, layer in enumerate(bone.layers):
                if layer:
                    visible_list[i]= True
        for i, layer in enumerate(visible_list):
            context.object.data.layers[i] = visible_list[i]
        
        # 全PoseBone表示
        for pose_bone in armature.pose.bones:
            pose_bone.bone.hide = False

        # 全ポーズのクリア
        bpy.ops.pose.select_all(action='SELECT')
        bpy.ops.pose.transforms_clear()
        bpy.ops.pose.select_all(action='DESELECT')

        return {'FINISHED'}


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    # 選択中BoneにControll用Boneを生やす
    layout.label(text="Select Util:")

    # box = layout.box()
    # box.label(text="")
    layout.operator("anime_pose_tools.show_deform_only")
    layout.operator("anime_pose_tools.show_control_only")
    layout.operator("anime_pose_tools.show_all")
    layout.operator("anime_pose_tools.reset_all")
