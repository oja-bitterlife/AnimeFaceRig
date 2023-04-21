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
        if (context.mode == "POSE"):
            for bone in context.selected_pose_bones:
                bone_names.append(bone.name)
        elif (context.mode == "EDIT_ARMATURE"):
            for bone in armature.data.edit_bones:
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
label = "ListupBones"
classes= [
    ANIME_POSE_TOOLS_OT_listup_selected_bones,
]

def draw(self, context, layout):
    if context.mode != "POSE" and context.mode != "EDIT_ARMATURE":
        layout.enabled = False

    box = layout.box()
    box.operator("anime_pose_tools.listup_selected_bones")
    box.prop(context.scene, "output_bones", text="Bone List:")


# =================================================================================================
def register():
    bpy.types.Scene.output_bones = bpy.props.StringProperty(name="OutputSelectedBones")

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
