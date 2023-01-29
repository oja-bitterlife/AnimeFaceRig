import bpy


# Remove Deform Weights
# =================================================================================================
class ANIME_POSE_TOOLS_OT_remove_deform(bpy.types.Operator):
    bl_idname = "anime_pose_tools.remove_deform"
    bl_label = "Remove Deform Groups"

    # execute
    def execute(self, context):
        # defomボーンを取得する
        deforms = [bone.name for armature in bpy.data.armatures for bone in armature.bones if bone.use_deform]

        # 選択中オブジェクトからdeformボーンの頂点グループをすべて削除する
        for mesh in context.selected_objects:
            if mesh.type == "MESH":
                for vg in mesh.vertex_groups:
                    # deformボーンの頂点グループだった
                    if vg.name in deforms:
                        mesh.vertex_groups.remove(vg)

        return {'FINISHED'}


# Add Group from Selected Bones
# =================================================================================================
class ANIME_POSE_TOOLS_OT_add_groups_from_bones(bpy.types.Operator):
    bl_idname = "anime_pose_tools.add_groups_from_bones"
    bl_label = "Add Groups (Selected Bones)"

    # execute
    def execute(self, context):
        # defromボーンのみ追加するためリストアップ
        deforms = [bone.name for armature in bpy.data.armatures for bone in armature.bones if bone.use_deform]

        # 追加する頂点グループ名の取得
        add_vg_names = []
        for armature in context.selected_objects:
            if armature.type == "ARMATURE":
                for bone in armature.data.bones:
                    # 選択中のdefromボーン
                    if bone.select and bone.name in deforms:
                        add_vg_names.append(bone.name)

        # 頂点グループを追加
        for mesh in context.selected_objects:
            if mesh.type == "MESH":
                # すでに存在する頂点グループ名取得
                vg_names = [vg.name for vg in mesh.vertex_groups]
                for add_name in add_vg_names:
                    # 存在しない頂点グループ名だけ追加
                    if add_name not in vg_names:
                        mesh.vertex_groups.new(name=add_name)

        return {'FINISHED'}


# UI描画設定
# =================================================================================================
class ANIME_POSE_TOOLS_PT_weight_util(bpy.types.Panel):
    bl_label = "Vertex Group"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AnimeTools"
    bl_parent_id = "APT_POSE_PT_UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if context.mode == "OBJECT":
            self.layout.label(text="add/remove:")
            box = self.layout.box()
            box.enabled = bpy.context.view_layer.objects.active.type == "MESH"
            box.operator("anime_pose_tools.remove_deform")
            box.operator("anime_pose_tools.add_groups_from_bones")
