import bpy


# Cursor move to selected bone
# =================================================================================================
class ANIME_POSE_TOOLS_OT_cursor_to_selected(bpy.types.Operator):
    bl_idname = "anime_pose_tools.cursor_to_selected"
    bl_label = "Cursor To Selected"

    # execute
    def execute(self, context):
        armature = bpy.context.view_layer.objects.active

        # アクティブなボーンの取得
        bone = context.active_pose_bone
        vec = bone.tail - bone.head
        pos = bone.head + vec * context.scene.target_head_tail_weight

        bpy.context.scene.cursor.location = armature.matrix_world @ pos

        return{'FINISHED'}



# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="3D Cursor:")
    box = layout.box()
    box.prop(context.scene, "target_head_tail_weight", text="Head / Tail", slider=True)
    box.operator("anime_pose_tools.cursor_to_selected")

# =================================================================================================
def register():
    bpy.types.Scene.target_head_tail_weight = bpy.props.FloatProperty(name="TargetHeadTailWeight", min=0, max=1, default=1)
