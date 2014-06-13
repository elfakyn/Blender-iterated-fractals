import bpy

global_depth = 3

def gen_mat (x): # x < 8
    mat = bpy.data.materials.new('menger_mat_'+str(x))
    mat.diffuse_color = (1-x//4 % 2, 1-x//2 % 2, 1-x % 2)
    
    return mat

def new_mat_idx (x, y, z, mat_idx):
    new_mat_idx = mat_idx
    
    if x >= 1:
        new_mat_idx[1] += 1
    if x <= 1:
        new_mat_idx[0] += 1
    
    if y >= 1:
        new_mat_idx[3] += 1
    if y <= 1:
        new_mat_idx[2] += 1
    
    if z >= 1:
        new_mat_idx[5] += 1
    if z <= 1:
        new_mat_idx[4] += 1
    return new_mat_idx

class MengerSponge:
    def __init__(self):
        self.idx = 0;
        self.verts = []
        self.faces = []
        self.face_mat_idx = []
    
    def recurse(self, pos, size, mat_idx, depth):
        
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
            
            self.face_mat_idx.extend(mat_idx)
            self.idx += 8
            return
            # todo: maybe use bpy.ops.mesh instead?
        
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if x%2 + y%2 + z%2 < 2: # check if valid. ugly but almost twice as fast as x%3==1
                        new_mat_idx = list(map(lambda x: x, mat_idx))
    
                        if x >= 1:
                            new_mat_idx[1] = depth
                        if x <= 1:
                            new_mat_idx[0] = depth
                        
                        if y >= 1:
                            new_mat_idx[3] = depth
                        if y <= 1:
                            new_mat_idx[2] = depth
                        
                        if z >= 1:
                            new_mat_idx[5] = depth
                        if z <= 1:
                            new_mat_idx[4] = depth
                        self.recurse([pos[0]+x*size/3, pos[1]+y*size/3, pos[2]+z*size/3], size/3, new_mat_idx, depth-1)
    
    def generate(self, size, depth):
        self.recurse([0.0, 0.0, 0.0], size, [0, 0, 0, 0, 0, 0], depth)
        mesh = bpy.data.meshes.new(name="MengerSponge")
        object = bpy.data.objects.new('MESH', mesh)
        bpy.context.scene.objects.link(object)
        mesh.from_pydata(self.verts, [], self.faces)
        mesh.update(calc_edges = True)
        
        for i in range(global_depth+1):
            object.data.materials.append(gen_mat(i))
        
        
        for f in mesh.polygons:
            f.material_index = self.face_mat_idx[f.index]
        
        bpy.context.scene.objects.active = object
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode = 'OBJECT')

sponge = MengerSponge()
sponge.generate(10,global_depth)