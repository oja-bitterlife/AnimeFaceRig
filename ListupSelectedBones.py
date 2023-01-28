import bpy


# Listup Selected Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_listup_selected_bones(bpy.types.Operator):
    bl_idname = "anime_pose_tools.listup_selected_bones"
    bl_label = "Listup Selected Bones"

    # execute
    def execute(self, context):
        armature = bpy.context.view_layer.objects.active

        # 出力初期化
        context.scene.output_bones = "Bone is not selected."
        bone_names = []

        # 選択中ボーンの回収
        for bone in armature.data.bones:
            if bone.select:
                bone_names.append(bone.name)

        # output bones
        text = ""
        for bone_name in bone_names:
            text += bone_name + "\n"

        if text != "":
            context.scene.output_bones = text

        return{'FINISHED'}



# UI描画設定
# =================================================================================================
class ANIME_POSE_TOOLS_PT_listup_selected_bones(bpy.types.Panel):
    bl_label = "Listup Selected Bones"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AnimeTools"
    bl_parent_id = "APT_MAIN_UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        box = self.layout.box()
        box.operator("anime_pose_tools.listup_selected_bones")
        box.prop(context.scene, "output_bones", text="Bone List:")


# =================================================================================================
def register():
    bpy.types.Scene.output_bones = bpy.props.StringProperty(name="OutputSelectedBones")
