import bpy
from mathutils import Vector

from .Util import BoneUtil


COLLISION_BOX_PREFIX = "APT_ColBox@"

# 箱生成用
BOX_VERTS = [(0,-0.5,0),(0,0.5,0),  # 0-1
            (-0.5,-0.5,-0.5),(0,-0.5,-0.5),(0.5,-0.5,-0.5),  # 2-4
            (-0.5,-0.5,0),(0.5,-0.5,0),  # 5-6
            (-0.5,-0.5,0.5),(0,-0.5,0.5),(0.5,-0.5,0.5),  # 7-9
            (-0.5,0.5,-0.5),(0,0.5,-0.5),(0.5,0.5,-0.5),  # 10-12
            (-0.5,0.5,0),(0.5,0.5,0),  # 13-14
            (-0.5,0.5,0.5),(0,0.5,0.5),(0.5,0.5,0.5)]  # 15-17

BOX_FACES = [(2,3,0,5),(3,4,6,0),(5,0,8,7),(0,6,9,8),  # 上面
            (10,13,1,11),(11,1,14,12),(13,15,16,1),(1,16,17,14),  # 下面
            (2,5,13,10),(5,7,15,13),
            (4,12,14,6),(6,14,17,9),
            (2,10,11,3),(3,11,12,4),
            (7,8,16,15),(8,9,17,16)]


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
            rot_matrix = armature.matrix_world.to_3x3() @ edit_bone.matrix.to_3x3()
            box_verts = [(rot_matrix @ Vector([v[0]*size, v[1]*size, v[2]*size])).xyz for v in BOX_VERTS]
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
