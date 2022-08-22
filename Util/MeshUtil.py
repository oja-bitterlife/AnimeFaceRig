# OBJECTモード中で頂点選択を外す
def deselect_vertex_in_object_mode(obj):
    for polygon in obj.data.polygons:
        polygon.select = False
    for edge in obj.data.edges:
        edge.select = False
    for vertex in obj.data.vertices:
        vertex.select = False
