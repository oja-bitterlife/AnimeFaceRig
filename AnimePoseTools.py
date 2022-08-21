import bpy

from . import PositionMode, WeightUtil, AnimExport
from . import FaceRigSetup, BonePhysics
from . import SelectBones, SelectedBoneList
from . import ResetStretch, ShowCtrlInPose, CursorToSelected


# Main UI
# ===========================================================================================
# 3DView Tools Panel
class ANIME_FACE_RIG_PT_ui(bpy.types.Panel):
    bl_label = "Anime Pose Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AnimePoseTools"

    def draw(self, context):
        # 何も選択されていない
        if bpy.context.view_layer.objects.active == None:
            return

        # 状態によって使うUIを切り替える
        if context.mode == "OBJECT":
            # Aramture選択時
            if bpy.context.view_layer.objects.active.type == "ARMATURE":
                PositionMode.ui_draw(context, self.layout)
                AnimExport.ui_draw(context, self.layout)
            if bpy.context.view_layer.objects.active.type == "MESH":
                WeightUtil.ui_draw(context, self.layout)

        if context.mode == "EDIT_ARMATURE":
            FaceRigSetup.ui_draw(context, self.layout)
            BonePhysics.ui_draw(context, self.layout)

        if context.mode == "POSE":
            ResetStretch.ui_draw(context, self.layout)
            ShowCtrlInPose.ui_draw(context, self.layout)
            CursorToSelected.ui_draw(context, self.layout)
            SelectBones.ui_draw(context, self.layout)
            SelectedBoneList.ui_draw(context, self.layout)

