import bpy
import json, traceback


# To Pose Position
# =================================================================================================
class ANIME_POSE_TOOLS_OT_anim_export(bpy.types.Operator):
    bl_idname = "anime_pose_tools.anim_export"
    bl_label = "Export Animations"

    # ファイル選択ダイアログ
    filepath: bpy.props.StringProperty()
    filter_glob: bpy.props.StringProperty(
        default="*.json",
    )
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    # execute
    def execute(self, context):
        # かならず.jsonに
        if not self.filepath.lower().endswith(".json"):
            self.filepath += ".json"

        data = {}

        try:
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except:
            self.report({'ERROR'}, traceback.format_exc())
            return {'CANCELLED'}


        return {'FINISHED'}


# To Rest Position
# =================================================================================================
class ANIME_POSE_TOOLS_OT_anim_import(bpy.types.Operator):
    bl_idname = "anime_pose_tools.anim_import"
    bl_label = "Import Animations"

    # ファイル選択ダイアログ
    filepath: bpy.props.StringProperty()
    filter_glob: bpy.props.StringProperty(
        default="*.json",
    )
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    # execute
    def execute(self, context):
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
        except:
            self.report({'ERROR'}, traceback.format_exc())
            return {'CANCELLED'}

        print(data)

        return {'FINISHED'}


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Export/Import Animations:")
    box = layout.box()
    box.operator("anime_pose_tools.anim_export")
    box.operator("anime_pose_tools.anim_import")
