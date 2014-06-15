# Thanks to Ethan (@sherbondy) for the awesome idea of using CSG!
# Much slower than the other version, but it uses like 1/3 of the geometry
# Refactored version. slightly slower but more readable.

import bpy
import mathutils

bpy.ops.object.select_all(action='DESELECT')

pos = bpy.context.scene.cursor_location

bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False)
iterator = bpy.context.active_object
iterator.name = 'Iterator'

bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False)
menger = bpy.context.active_object
menger.name = 'MengerSponge'

def apply_modifier():
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Iterator"]
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

max_depth = 3

def cycle(array):
    new_array = []
    for i in range(len(array)):
        new_array.append(array[(i+1)%len(array)])
    return new_array



for depth in range (max_depth):
    for i in range(3**depth):
        for j in range(3**depth):
            scale = [1.01, 1/3**(depth+1), 1/3**(depth+1)]
            location = [0, -1+1/3**depth+2*i/3**depth, -1+1/3**depth+2*j/3**depth]
            for k in range(3):

                iterator.scale = scale
                iterator.location = pos + mathutils.Vector(location)
                apply_modifier()
                scale = cycle(scale)
                location = cycle(location)


bpy.ops.object.select_all(action='DESELECT')
iterator.select = True
bpy.ops.object.delete()

menger.select = True