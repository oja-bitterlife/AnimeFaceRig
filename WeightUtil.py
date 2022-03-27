import bpy


# Remove Deform Weights
# =================================================================================================
class ANIME_POSE_TOOLS_OT_remove_deform(bpy.types.Operator):
    bl_idname = "anime_pose_tools.remove_deform"
    bl_label = "Remove Deform Groups"

    # execute
    def execute(self, context):
        # defomボーンを取得する
        deforms = [bone.name for armature in bpy.data.armatures for bone in armature.bones if bone.use_deform]

        # 選択中オブジェクトからdeformボーンの頂点グループをすべて削除する
        for obj in context.selected_objects:
            if obj.type == "MESH":
                for vg in obj.vertex_groups:
                    # deformボーンの頂点グループだった
                    if vg.name in deforms:
                        obj.vertex_groups.remove(vg)

        return {'FINISHED'}


# Add Group from Selected Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_add_groups_from_bones(bpy.types.Operator):
    bl_idname = "anime_pose_tools.add_groups_from_bones"
    bl_label = "Add Groups (Selected Bones)"

    # execute
    def execute(self, context):

        return {'FINISHED'}


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Change Position Mode:")
    box = layout.box()
    box.operator("anime_pose_tools.remove_deform")
    box.operator("anime_pose_tools.add_groups_from_bones")
