import bpy


# Listup Selected Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_listup_selected_bones(bpy.types.Operator):
    bl_idname = "anime_pose_tools.listup_selected_bones"
    bl_label = "Listup Selected Bones"

    # execute
    def execute(self, context):
        armature = bpy.context.view_layer.objects.active

        # Aramtureが選択されていない
        if armature == None or armature.type != "ARMATURE":
            self.report({'ERROR'}, "activeなオブジェクトがArmatureじゃない(通常あり得ない)")
            return {'CANCELLED'}

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
def ui_draw(context, layout):
    layout.label(text="Listup Selected Bones:")
    box = layout.box()
    box.operator("anime_pose_tools.listup_selected_bones")
    box.prop(context.scene, "output_bones", text="Bone List:")

# =================================================================================================
def register():
    bpy.types.Scene.output_bones = bpy.props.StringProperty(name="OutputSelectedBones")
