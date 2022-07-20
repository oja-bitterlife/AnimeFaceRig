import bpy

from . import FaceRigSetup
from . import ResetStretch, ShowCtrlInPose, SelectedBoneList
from . import PositionMode, WeightUtil, AnimExport


# Main UI
# ===========================================================================================
# 3DView Tools Panel
class ANIME_FACE_RIG_PT_ui(bpy.types.Panel):
    bl_label = "Anime Pose Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AnimePoseTools"

    def draw(self, context):
        # 状態によって使うUIを切り替える
        if context.mode == "OBJECT":
            # Aramture選択時
            if bpy.context.view_layer.objects.active == None or bpy.context.view_layer.objects.active.type == "ARMATURE":
                PositionMode.ui_draw(context, self.layout)
                AnimExport.ui_draw(context, self.layout)
            if bpy.context.view_layer.objects.active == None or bpy.context.view_layer.objects.active.type == "MESH":
                WeightUtil.ui_draw(context, self.layout)

        if context.mode == "EDIT_ARMATURE":
            FaceRigSetup.ui_draw(context, self.layout)
        if context.mode == "POSE":
            ResetStretch.ui_draw(context, self.layout)
            ShowCtrlInPose.ui_draw(context, self.layout)
            SelectedBoneList.ui_draw(context, self.layout)

