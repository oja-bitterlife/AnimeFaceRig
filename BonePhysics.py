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

        # 対象ボーンの中央にBoxを配置
        for pose_bone in bpy.context.selected_pose_bones:
            vec = pose_bone.tail - pose_bone.head
            col_width = vec.length * context.scene.collision_box_width
            col_length = vec.length * context.scene.collision_box_length
            pos = armature.matrix_world @ (pose_bone.head + vec * 0.5)

            # 登録先コレクション取得
            collection = bpy.data.collections.get(context.scene.work_collection)
            if collection == None:
                collection = bpy.data.collections.new(context.scene.work_collection)
                bpy.context.scene.collection.children.link(collection)

            # Box作成
            # メッシュの頂点を変換して作成
            mesh = bpy.data.meshes.new("BoxMesh")
            rot_matrix = armature.matrix_world.to_3x3() @ pose_bone.matrix.to_3x3()
            # まずはサイズ調整
            tmp_verts = [Vector([v[0]*col_width, v[1]*col_length, v[2]*col_width]) for v in BOX_VERTS]
            # 上下中央はhead/tailの位置まで伸ばす
            tmp_verts[0].y = tmp_verts[0].y - (vec.length - col_length) * 0.5
            tmp_verts[1].y = tmp_verts[1].y + (vec.length - col_length) * 0.5
            box_verts = [(rot_matrix @ v).xyz for v in tmp_verts]  # ボーンの向きで傾ける
            mesh.from_pydata(box_verts, [], BOX_FACES)
            mesh.update(calc_edges=True)
            # オブジェクトにしてコレクションに登録
            obj = bpy.data.objects.new(COLLISION_BOX_PREFIX + pose_bone.name, mesh)
            obj.location = pos
            collection.objects.link(obj)

        return{'FINISHED'}


# Remove Physics setup
# =================================================================================================
class ANIME_POSE_TOOLS_OT_remove_all(bpy.types.Operator):
    bl_idname = "anime_pose_tools.remove_all"
    bl_label = "Remove All"

    # execute
    def execute(self, context):
        # 作業対象コレクションがない
        collection = bpy.data.collections.get(context.scene.work_collection)
        if collection == None:
            return{'FINISHED'}

        for obj in bpy.data.objects:
            # 削除するのはWork下だけ
            if collection.objects.get(obj.name) != None:
                # COLLISION_BOXの削除
                if obj.name.startswith(COLLISION_BOX_PREFIX):
                        bpy.data.objects.remove(obj)

        return{'FINISHED'}


# Check Overlaped bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_check_overlap(bpy.types.Operator):
    bl_idname = "anime_pose_tools.check_overlap"
    bl_label = "Check Overlaped "

    # execute
    def execute(self, context):
        # 対象ボーンの回収
        armature = bpy.context.active_object
        selected_bones = []
        for bone in armature.data.edit_bones:
            if bone.select and BoneUtil.is_layer_enable(armature, bone):
                selected_bones.append(bone)
                bone.select = False  # 一旦非選択に

        # チェック
        for check_bone in selected_bones:
            for cmp_bone in selected_bones:
                # 自身はチェックしない
                if check_bone.name == cmp_bone.name:
                    continue
                # 同一の親ならHeadが一致するのは当然なのでチェックしない
                if check_bone.parent.name == cmp_bone.parent.name:
                    continue


        return{'FINISHED'}



# UI描画設定
# =================================================================================================
def ui_draw(context, layout):
    layout.label(text="Bone Physics:")
    layout.operator("anime_pose_tools.check_overlap")
    box = layout.box()
    box.prop(context.scene, "work_collection", text="Work Collection", slider=True)
    create = box.box()
    create.label(text="Collistion Box:")
    create.prop(context.scene, "collision_box_width", text="Collision Width", slider=True)
    create.prop(context.scene, "collision_box_length", text="Collision Length", slider=True)
    create.operator("anime_pose_tools.create_collision_box")
    box.operator("anime_pose_tools.remove_all")


# =================================================================================================
def register():
    bpy.types.Scene.work_collection = bpy.props.StringProperty(name="Work Collection Name", default="APT_Work")
    bpy.types.Scene.collision_box_width = bpy.props.FloatProperty(name="Collision Box Width", min=0, max=1, default=0.25)
    bpy.types.Scene.collision_box_length = bpy.props.FloatProperty(name="Collision Box Length", min=0, max=1, default=0.5)
