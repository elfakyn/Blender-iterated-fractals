import bpy

class MengerSponge:
    def __init__(self):
        self.idx = 0;
        self.verts = []
        self.faces = []
        self.face_materials = []
        self.base_materials = 
    
    def recurse(self, pos, size, depth):
        
        if depth == 0:
            for x in range(2):
                for y in range(2):
                    for z in range(2):
                        self.verts.append((pos[0]+x*size, pos[1]+y*size, pos[2]+z*size)) # make vertices
            self.faces.append((self.idx+4, self.idx+5, self.idx+7, self.idx+6))
            self.faces.append((self.idx+0, self.idx+1, self.idx+3, self.idx+2))
            self.faces.append((self.idx+2, self.idx+3, self.idx+7, self.idx+6))
            self.faces.append((self.idx+0, self.idx+1, self.idx+5, self.idx+4))
            self.faces.append((self.idx+1, self.idx+5, self.idx+7, self.idx+3))
            self.faces.append((self.idx+0, self.idx+4, self.idx+6, self.idx+2))
            self.idx += 8
            return
            # todo: maybe use bpy.ops.mesh instead?
        
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if x%2 + y%2 + z%2 < 2: # check if valid. ugly but almost twice as fast as x%3==1
                        self.recurse([pos[0]+x*size/3, pos[1]+y*size/3, pos[2]+z*size/3], size/3, depth-1)
    
    def generate(self, size, depth):
        self.recurse([0.0, 0.0, 0.0], size, depth)
        mesh = bpy.data.meshes.new(name="MengerSponge")
        object = bpy.data.objects.new('MESH', mesh)
        bpy.context.scene.objects.link(object)
        mesh.from_pydata(self.verts, [], self.faces)
        mesh.update(calc_edges = True)
        
        bpy.context.scene.objects.active = object
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode = 'OBJECT')

sponge = MengerSponge()
sponge.generate(10,2)