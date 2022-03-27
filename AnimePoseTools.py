import bpy

from . import FaceRigSetup, ResetStretch, ShowCtrlInPose


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
        if context.mode == "EDIT_ARMATURE":
            FaceRigSetup.ui_draw(context, self.layout)
        if context.mode == "POSE":
            ResetStretch.ui_draw(context, self.layout)
            ShowCtrlInPose.ui_draw(context, self.layout)

