import bpy

from . import PositionMode, WeightUtil
from . import CursorToSelected


# Main UI
# ===========================================================================================
# 3DView Tools Panel
class ANIME_POSE_TOOLS_PT_ui(bpy.types.Panel):
    bl_label = "Anime Pose Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AnimeTools"
    bl_idname = "APT_MAIN_UI"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 0

    def draw(self, context):
        # 何も選択されていない
        if bpy.context.view_layer.objects.active == None:
            return

        # 状態によって使うUIを切り替える
        if context.mode == "OBJECT":
            # Aramture選択時
            if bpy.context.view_layer.objects.active.type == "ARMATURE":
                PositionMode.ui_draw(context, self.layout)
            if bpy.context.view_layer.objects.active.type == "MESH":
                WeightUtil.ui_draw(context, self.layout)

        if context.mode == "POSE":
            # Aramtureが選択されていない
            armature = bpy.context.view_layer.objects.active
            if armature == None or armature.type != "ARMATURE":
                self.report({'ERROR'}, "activeなオブジェクトがArmatureじゃない(通常あり得ない)")
                return {'CANCELLED'}

            CursorToSelected.ui_draw(context, self.layout)

