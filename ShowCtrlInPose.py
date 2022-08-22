import bpy


# Show Only Deform Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_show_deform_only(bpy.types.Operator):
    bl_idname = "anime_pose_tools.show_deform_only"
    bl_label = "Deform"

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
    bl_label = "Control"

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
    bl_label = "All"

    # execute
    def execute(self, context):
        # 全PoseBone対象
        armature = bpy.context.active_object
        for pose_bone in armature.pose.bones:
            pose_bone.bone.hide = False

        return {'FINISHED'}


# Show All Layers
# =================================================================================================
class ANIME_POSE_TOOLS_OT_show_all_layers(bpy.types.Operator):
    bl_idname = "anime_pose_tools.show_all_layers"
    bl_label = "Show All Layers"

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

        return {'FINISHED'}


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Show Util:")

    box = layout.box()
    row = box.row()
    row.alignment = 'EXPAND'
    row.operator("anime_pose_tools.show_deform_only")
    row.operator("anime_pose_tools.show_control_only")
    row.operator("anime_pose_tools.show_all")
    box.operator("anime_pose_tools.show_all_layers")
