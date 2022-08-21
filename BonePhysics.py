import bpy
from .Util import BoneUtil

COLLISION_BOX_PREFIX = "APT_ColBox@"

# 箱生成用
BOX_VERTS = [(-0.5,-0.5,-0.5),(-0.5,0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(-0.5,-0.5,0.5),(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5)]
BOX_FACES = [(0,1,2,3), (4,5,6,7), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)]

# Physics setup to Bone
# =================================================================================================
class ANIME_POSE_TOOLS_OT_create_collision_box(bpy.types.Operator):
    bl_idname = "anime_pose_tools.create_collision_box"
    bl_label = "Create"

    # execute
    def execute(self, context):
        # 対象ボーンの回収
        armature = bpy.context.active_object
        selected_bones = []
        for bone in armature.data.edit_bones:
            if bone.select and BoneUtil.is_layer_enable(armature, bone):
                selected_bones.append(bone)


        # 対象ボーンの中央にBoxを配置
        for edit_bone in selected_bones:
            vec = edit_bone.tail - edit_bone.head
            size = vec.length * context.scene.collision_box_size * 0.5
            pos = armature.matrix_world @ (edit_bone.head + vec * 0.5)

            # 登録先コレクション取得
            collection = bpy.data.collections.get(context.scene.work_collection)
            if collection == None:
                collection = bpy.data.collections.new(context.scene.work_collection)
                bpy.context.scene.collection.children.link(collection)

            # Box作成
            mesh = bpy.data.meshes.new("BoxMesh")
            box_verts = [(v[0]*size, v[1]*size, v[2]*size) for v in BOX_VERTS]
            mesh.from_pydata(box_verts, [], BOX_FACES)
            mesh.update(calc_edges=True)
            obj = bpy.data.objects.new(COLLISION_BOX_PREFIX + edit_bone.name, mesh)
            obj.location = pos
            collection.objects.link(obj)



        return{'FINISHED'}

class ANIME_POSE_TOOLS_OT_remove_all(bpy.types.Operator):
    bl_idname = "anime_pose_tools.remove_all"
    bl_label = "Remove All"

    # execute
    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.name.startswith(COLLISION_BOX_PREFIX):
                bpy.data.objects.remove(obj)

        return{'FINISHED'}


# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Bone Physics:")
    box = layout.box()
    box.prop(context.scene, "work_collection", text="Work Collection", slider=True)
    create = box.box()
    create.label(text="Collistion Box:")
    create.prop(context.scene, "collision_box_size", text="Collision Size", slider=True)
    create.operator("anime_pose_tools.create_collision_box")
    box.operator("anime_pose_tools.remove_all")


# =================================================================================================
def register():
    bpy.types.Scene.work_collection = bpy.props.StringProperty(name="Work Collection Name", default="APT_Work")
    bpy.types.Scene.collision_box_size = bpy.props.FloatProperty(name="Collision Box Size", min=0, max=1, default=0.5)
