import bpy

# Main UI
# ===========================================================================================
# 3DView Tools Panel
class ANIME_POSE_TOOLS_PT_ui(bpy.types.Panel):
    bl_label = "Anime Pose Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AHT"
    bl_idname = "APT_POSE_PT_UI"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass

