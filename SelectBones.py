import bpy
import re


# Listup Selected Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_bones_with_a_key(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_bones_with_a_key"
    bl_label = "With A Key In Frame"

    # execute
    def execute(self, context):
        armature = bpy.context.view_layer.objects.active

        # 選択中ArmatureのBone名を取得
        bone_names = [bone.name for bone in armature.pose.bones]

        # 現在のActionを取得
        action = bpy.context.active_object.animation_data.action

        # 現在のフレーム
        current_frame = bpy.data.scenes[0].frame_current

        # 一旦Deselect
        for pose_bone in armature.pose.bones:
            pose_bone.bone.select = False

        # bone_namesに含まれるGroupを探す
        for fcurve in action.fcurves:
            # 現在のフレーム(co[0]参照)に絞る
            for point in fcurve.keyframe_points:
                if point.co[0] == current_frame:
                    # キーが選択中のArmatureのBoneなら選択
                    if fcurve.group.name in bone_names:
                        armature.pose.bones[fcurve.group.name].bone.select = True

        return{'FINISHED'}


# Select To Edge
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_to_edge(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_to_edge"
    bl_label = "To Edge"

    # execute
    def execute(self, context):
        for pose_bone in bpy.context.selected_pose_bones:
            self.rec_select_children(pose_bone)
        return{'FINISHED'}

    def rec_select_children(self, pose_bone):
        pose_bone.bone.select = True
        for child in pose_bone.children:
            self.rec_select_children(child)


# Select To Top
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_to_top(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_to_top"
    bl_label = "To Top"

    # execute
    def execute(self, context):
        for pose_bone in bpy.context.selected_pose_bones:
            self.rec_select_children(pose_bone)
        return{'FINISHED'}

    def rec_select_children(self, pose_bone):
        pose_bone.bone.select = True
        if pose_bone.parent:
            self.rec_select_children(pose_bone.parent)


# Select Plus Edge
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_plus_edge(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_plus_edge"
    bl_label = "Plus Edge"

    # execute
    def execute(self, context):
        for pose_bone in bpy.context.selected_pose_bones:
            for child in pose_bone.children:
                child.bone.select = True

        return{'FINISHED'}


# Select Plus Top
# =================================================================================================
class ANIME_POSE_TOOLS_OT_select_plus_top(bpy.types.Operator):
    bl_idname = "anime_pose_tools.select_plus_top"
    bl_label = "Plus Top"

    # execute
    def execute(self, context):
        for pose_bone in bpy.context.selected_pose_bones:
            if pose_bone.parent:
                pose_bone.parent.bone.select = True

        return{'FINISHED'}


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
class ANIME_POSE_TOOLS_PT_select_bones(bpy.types.Panel):
    bl_label = "Bone Selector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AnimeTools"
    bl_parent_id = "APT_POSE_PT_UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if context.mode == "POSE":
            self.layout.label(text="Show Control:")

            box = self.layout.box()
            row = box.row()
            row.alignment = 'EXPAND'
            row.operator("anime_pose_tools.show_deform_only")
            row.operator("anime_pose_tools.show_control_only")
            row.operator("anime_pose_tools.show_all")
            box.operator("anime_pose_tools.show_all_layers")

            self.layout.label(text="Select Bones:")

            box = self.layout.box()
            row = box.row()
            row.operator("anime_pose_tools.select_to_edge")
            row.operator("anime_pose_tools.select_to_top")
            row.operator("anime_pose_tools.select_plus_edge")
            row.operator("anime_pose_tools.select_plus_top")
            box.operator("anime_pose_tools.select_bones_with_a_key")
