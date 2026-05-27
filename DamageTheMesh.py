bl_info = {
    "name": "Damage the Mesh",
    "author": "dimipats",
    "version": (1, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Damage the Mesh",
    "category": "Object",
}

import bpy


def update_gn(self, context):
    obj = context.active_object
    if not obj:
        return

    mod = obj.modifiers.get("Damage")

    mod["Socket_1"] = 3
    mod["Socket_2"] = 0
    mod["Socket_3"] = 0.1

    mod2 = obj.modifiers.get("Damage")

    mod2["Socket_1"] = 2
    mod2["Socket_2"] = 2
    mod2["Socket_3"] = 0.4




class OBJECT_OT_apply_gn(bpy.types.Operator):
    bl_idname = "object.apply_noise_gn"
    bl_label = "Apply Damage"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            return {'CANCELLED'}

        #add face deformation
        mod = obj.modifiers.new(name="Face Deformation", type='NODES')
        ng = bpy.data.node_groups.new("Face Deformation", 'GeometryNodeTree')
        mod.node_group = ng

        nodes = ng.nodes
        links = ng.links
        nodes.clear()

        #interface
        ng.interface.new_socket(
            "Geometry",
            in_out='INPUT',
            socket_type='NodeSocketGeometry'
        )

        ng.interface.new_socket(
            "Noise Scale",
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )

        ng.interface.new_socket(
            "Noise Detail",
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )

        ng.interface.new_socket(
            "Strength",
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )

        ng.interface.new_socket(
            "Geometry",
            in_out='OUTPUT',
            socket_type='NodeSocketGeometry'
        )

        #nodes
        group_in = nodes.new("NodeGroupInput")
        group_in.location = (-800, 0)

        group_out = nodes.new("NodeGroupOutput")
        group_out.location = (500, 0)

        set_pos = nodes.new("GeometryNodeSetPosition")
        set_pos.location = (300, 0)

        noise = nodes.new("ShaderNodeTexNoise")
        noise.location = (-500, -200)

        vsub = nodes.new("ShaderNodeVectorMath")
        vsub.operation = 'SUBTRACT'
        vsub.location = (-300, -200)

        vmul = nodes.new("ShaderNodeVectorMath")
        vmul.operation = 'MULTIPLY'
        vmul.location = (-100, -200)

        vsca = nodes.new("ShaderNodeVectorMath")
        vsca.operation = 'SCALE'
        vsca.location = (100, -200)

        norm = nodes.new("GeometryNodeInputNormal")
        norm.location = (-300, -500)


        #node links
        links.new(group_in.outputs["Geometry"], set_pos.inputs["Geometry"])
        links.new(set_pos.outputs["Geometry"], group_out.inputs["Geometry"])
        links.new(vsca.outputs[0], set_pos.inputs["Offset"])
        links.new(vmul.outputs[0], vsca.inputs[0])
        links.new(vsub.outputs[0], vmul.inputs[0])
        links.new(norm.outputs["Normal"], vmul.inputs[1])
        links.new(noise.outputs["Color"], vsub.inputs[0])
        links.new(group_in.outputs["Noise Scale"], noise.inputs["Scale"])
        links.new(group_in.outputs["Noise Detail"], noise.inputs["Detail"])
        links.new(group_in.outputs["Strength"], vsca.inputs[3])

        mod["Socket_1"] = 3
        mod["Socket_2"] = 0
        mod["Socket_3"] = 0.1

        #add edge damage
        mod2 = obj.modifiers.new(name="Edge Damage", type='NODES')
        ng2 = bpy.data.node_groups.new("Edge Damage", 'GeometryNodeTree')
        mod2.node_group = ng2

        nodes = ng2.nodes
        links = ng2.links
        nodes.clear()

        #interface
        ng2.interface.new_socket(
            "Geometry",
            in_out='INPUT',
            socket_type='NodeSocketGeometry'
        )

        ng2.interface.new_socket(
            "Noise Scale",
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )

        ng2.interface.new_socket(
            "Noise Detail",
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )

        ng2.interface.new_socket(
            "Edge Crease",
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )

        ng2.interface.new_socket(
            "Geometry",
            in_out='OUTPUT',
            socket_type='NodeSocketGeometry'
        )

        #nodes
        group_in2 = nodes.new("NodeGroupInput")
        group_in2.location = (-1000, 0)

        group_out2 = nodes.new("NodeGroupOutput")
        group_out2.location = (1000, 0)

        bool = nodes.new("GeometryNodeMeshBoolean")
        bool.operation = "INTERSECT"
        bool.location = (800, 0)

        set_pos1 = nodes.new("GeometryNodeSetPosition")
        set_pos1.location = (600, -200)

        vmul2 = nodes.new("ShaderNodeVectorMath")
        vmul2.operation = 'MULTIPLY'
        vmul2.location = (400, -400)

        vmul3 = nodes.new("ShaderNodeVectorMath")
        vmul3.operation = 'MULTIPLY'
        vmul3.location = (200, -400)

        pos1 = nodes.new("GeometryNodeInputPosition")
        pos1.location = (0, -400)

        mult = nodes.new("ShaderNodeMath")
        mult.operation = "MULTIPLY"
        mult.location = (0, -500)
        mult.inputs[1].default_value = -1.7

        set_pos2 = nodes.new("GeometryNodeSetPosition")
        set_pos2.location = (0, -200)

        subs = nodes.new("GeometryNodeSubdivisionSurface")
        subs.location = (-200, -200)

        vmul4 = nodes.new("ShaderNodeVectorMath")
        vmul4.operation = 'MULTIPLY'
        vmul4.location = (-200, -400)

        vmul5 = nodes.new("ShaderNodeVectorMath")
        vmul5.operation = 'MULTIPLY'
        vmul5.location = (-400, -400)

        pos2 = nodes.new("GeometryNodeInputPosition")
        pos2.location = (-600, -400)

        val = nodes.new("ShaderNodeValue")
        val.location = (-600, -500)
        val.outputs[0].default_value = -0.3

        noise2 = nodes.new("ShaderNodeTexNoise")
        noise2.location = (-600, -600)

        #node links
        links.new(bool.outputs["Mesh"], group_out2.inputs["Geometry"])
        links.new(group_in2.outputs["Geometry"], bool.inputs["Mesh"])
        links.new(group_in2.outputs["Geometry"], subs.inputs["Mesh"])
        links.new(subs.outputs["Mesh"], set_pos2.inputs["Geometry"])
        links.new(set_pos2.outputs["Geometry"], set_pos1.inputs["Geometry"])
        links.new(set_pos1.outputs["Geometry"], bool.inputs["Mesh"])
        links.new(vmul2.outputs[0], set_pos1.inputs["Offset"])
        links.new(vmul3.outputs[0], vmul2.inputs[0])
        links.new(pos1.outputs["Position"], vmul3.inputs[0])
        links.new(mult.outputs["Value"], vmul3.inputs[1])
        links.new(vmul4.outputs[0], set_pos2.inputs["Offset"])
        links.new(vmul5.outputs[0], vmul4.inputs[0])
        links.new(pos2.outputs["Position"], vmul5.inputs[0])
        links.new(val.outputs["Value"], vmul5.inputs[1])
        links.new(val.outputs["Value"], mult.inputs[0])
        links.new(noise2.outputs["Color"], vmul2.inputs[1])
        links.new(noise2.outputs["Color"], vmul4.inputs[1])
        links.new(group_in2.outputs["Noise Scale"], noise2.inputs["Scale"])
        links.new(group_in2.outputs["Noise Detail"], noise2.inputs["Detail"])
        links.new(group_in2.outputs["Edge Crease"], subs.inputs["Edge Crease"])

        mod2["Socket_1"] = 2
        mod2["Socket_2"] = 2
        mod2["Socket_3"] = 0.4

        return {'FINISHED'}



class VIEW3D_PT_gn_panel(bpy.types.Panel):
    bl_label = "Damage Tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Damage the Mesh"

    def draw(self, context):

        layout = self.layout

        layout.operator("object.apply_noise_gn")



classes = (
    OBJECT_OT_apply_gn,
    VIEW3D_PT_gn_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()