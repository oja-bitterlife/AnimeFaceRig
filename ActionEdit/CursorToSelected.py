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
        if context.mode == "POSE":
            bone = context.active_pose_bone
            vec = bone.tail - bone.head
            pos = bone.head + vec * context.scene.target_head_tail_weight
        else:
            bone = context.active_bone
            vec = bone.tail - bone.head
            pos = bone.head + vec * context.scene.target_head_tail_weight

        bpy.context.scene.cursor.location = armature.matrix_world @ pos

        return{'FINISHED'}



# UI描画設定
# =================================================================================================
label = "3D Cursor"
classes = [
    ANIME_POSE_TOOLS_OT_cursor_to_selected,
]

def draw(parent, context, layout):
    # Armatureが選択中のみ有効
    if bpy.context.view_layer.objects.active == None or bpy.context.view_layer.objects.active.type != "ARMATURE":
        layout.enabled = False

    layout.prop(context.scene, "target_head_tail_weight", text="Head / Tail", slider=True)
    layout.operator("anime_pose_tools.cursor_to_selected")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.target_head_tail_weight = bpy.props.FloatProperty(name="TargetHeadTailWeight", min=0, max=1, default=1)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
