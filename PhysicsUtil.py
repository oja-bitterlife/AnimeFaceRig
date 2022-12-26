import bpy


# Enable/Disable Cloth
# =================================================================================================
class ANIME_POSE_TOOLS_OT_enable_cloth(bpy.types.Operator):
    bl_idname = "anime_pose_tools.enable_seleted"
    bl_label = "Enable Selected"

    # execute
    def execute(self, context):
        # 選択中オブジェクトからdeformボーンの頂点グループをすべて削除する
        for obj in context.selected_objects:
            if obj.type == "MESH":
                obj.modifiers["Cloth"].show_viewport = True
                obj.modifiers["Cloth"].show_render = True
        return {'FINISHED'}

class ANIME_POSE_TOOLS_OT_disable_selected(bpy.types.Operator):
    bl_idname = "anime_pose_tools.disable_selected"
    bl_label = "Disable Selected"

    # execute
    def execute(self, context):
        # 選択中オブジェクトからdeformボーンの頂点グループをすべて削除する
        for obj in context.selected_objects:
            if obj.type == "MESH":
                obj.modifiers["Cloth"].show_viewport = False
                obj.modifiers["Cloth"].show_render = False
        return {'FINISHED'}


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Cloth Util:")
    box = layout.box()
    row = box.row()
    row.operator("anime_pose_tools.enable_seleted")
    row.operator("anime_pose_tools.disable_selected")
