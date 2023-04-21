import bpy
import re


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
label = "Bone Visible"

classes = [
    ANIME_POSE_TOOLS_OT_show_deform_only,
    ANIME_POSE_TOOLS_OT_show_control_only,
    ANIME_POSE_TOOLS_OT_show_all,
    ANIME_POSE_TOOLS_OT_show_all_layers,
]

def draw(parent, context, layout):
    row = layout.row()
    row.alignment = 'EXPAND'
    row.operator("anime_pose_tools.show_deform_only")
    row.operator("anime_pose_tools.show_control_only")
    row.operator("anime_pose_tools.show_all")
    layout.operator("anime_pose_tools.show_all_layers")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
