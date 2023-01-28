import bpy

from . import PositionMode, WeightUtil
from . import AnimExport
from . import SelectBones
from . import CursorToSelected, RemoveKeys


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

    def draw(self, context):
        # 何も選択されていない
        if bpy.context.view_layer.objects.active == None:
            return

        # 状態によって使うUIを切り替える
        if context.mode == "OBJECT":
            # Aramture選択時
            if bpy.context.view_layer.objects.active.type == "ARMATURE":
                PositionMode.ui_draw(context, self.layout)
                self.layout.separator()
                AnimExport.ui_draw(context, self.layout)
            if bpy.context.view_layer.objects.active.type == "MESH":
                WeightUtil.ui_draw(context, self.layout)
            #     ClothUtil.ui_obj_draw(context, self.layout)

        if context.mode == "POSE":
            # Aramtureが選択されていない
            armature = bpy.context.view_layer.objects.active
            if armature == None or armature.type != "ARMATURE":
                self.report({'ERROR'}, "activeなオブジェクトがArmatureじゃない(通常あり得ない)")
                return {'CANCELLED'}

            # ShowCtrlInPose.ui_draw(context, self.layout)
            # self.layout.separator()
            CursorToSelected.ui_draw(context, self.layout)
            # self.layout.separator()
            # SelectBones.ui_draw(context, self.layout)
            self.layout.separator()
            RemoveKeys.ui_draw(context, self.layout)
            # self.layout.separator()
            # ClothUtil.ui_pose_draw(context, self.layout)
            # self.layout.separator()
            # BonePhysics.ui_draw(context, self.layout)
            # self.layout.separator()
            # ListupSelectedBones.ui_draw(context, self.layout)

