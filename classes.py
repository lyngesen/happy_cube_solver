from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from polycubes import generate_cube_coords, get_coords, get_coords_cubegrid
from copy import deepcopy

DIMS = range(3)
class Brick:
    def __init__(self,cubegrid):
        self.cubegrid = tuple(cubegrid) # fixed
        self.or_list = self.orientations()
        self.name = '?'
        self.color = '#FFD65D30'
    def __str__(self):
        chr_dict =  {1:'🟦',0:"  "}
        return "\n".join(["".join([chr_dict[b] for b in row]) for row in self.cubegrid]) #return "\n".join(["".join([row]) for row in self.cubegrid])
    
    def __repr__(self):
        return "\n" + self.__str__() +"\n"

    def rotate(self):
        self.cubegrid = list(reversed(list(zip(*self.cubegrid))))
        self.cubegrid = [list(row) for row in self.cubegrid]
    def flip(self):
        self.cubegrid = [list(reversed(row)) for row in self.cubegrid]

    def orientations(self):
        orientation_list = []
        for _ in range(4):
            if self.cubegrid not in [b.cubegrid for b in orientation_list]:
                orientation_list.append(deepcopy(self))
            self.rotate()
        self.flip()
        for _ in range(4):
            if self.cubegrid not in [b.cubegrid for b in orientation_list]:
                orientation_list.append(deepcopy(self))
            self.rotate()
        return orientation_list


@dataclass
class Voxel:
    x : int
    y : int
    z : int
    
    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        if item == 2:
            return self.z
    
    # def __eq__(self,other):

    def get_index(self,S):
        # & & &
        return np.logical_and.reduce([(self[d] == S[d]) for d in range(3)])
    def get_face(self,dims: list[int],S):

        self.D = list()
        for d in range(3):
            if d in dims:
                current_dim = (S[d] <= self[d] +2 ) & (S[d] >= self[d] -2 )
                self.D.append((current_dim))
            else:
                current_dim = (S[d] == self[d])
                self.D.append((current_dim))
        return np.logical_and.reduce(self.D)


@dataclass
class Face:
    center: Voxel 
    dims : list[int]
    cubegrid = [[0]*5]*5
    color = "#FFD65D10"

    cube_center_to_ij = dict()
    ij_to_cube_center = dict()
    def get_face(self, S):
        if isinstance(self.center, tuple):
            return Voxel.get_face(Voxel(*self.center), self.dims, S)

        return Voxel.get_face(self.center, self.dims, S)


    def get_active_face(self, S):
        D = list()
        if self.color != "#FFD65D10":
            # print(f"{self.cubegrid=}")
            # print(f"{get_coords_cubegrid(np.array(self.cubegrid))=}")
            # print(f"{self.dims=}")
            all_cords = get_coords_cubegrid(np.array(self.cubegrid))
            dim_list = list(self.dims)
            global_d1 = dim_list[0]
            global_d2 = dim_list[1]
            d1 = min(dim_list[0],1)
            d2 = min(dim_list[1],1)
            D.append(np.logical_or.reduce([(S[global_d1] == coord[d1]) & (S[global_d2] == coord[d2])  for coord in all_cords]  ))
 
            # print(f"{self.cubegrid}")
            # print(f"{self.color=}")

            # print(f"{all_cords=}")
            # print(f"{self.cube_center_to_ij.keys()=}")
            # print(f"{len(self.cube_center_to_ij.keys())=}")
            # D.append(np.logical_or.reduce([(S[d1] == coord[d1]) & (S[d2] == coord[d2])  &  (S[d3] == coord[d3])  for coord in all_cords]  ))

            # edge_centers = self.cube_center_to_ij.keys()

            # print(f"{self.cube_center_to_ij=}")
            # # print(f"{all_cords=}")
            # # print(f"{edge_centers=}")
            # print(f"{len(all_cords)=}")
            # print(f"{len(edge_centers)=}")
            
            # print(f"")
            # for point in edge_centers:
                # print(f"    {point=}")
                # pair = []
                # for d in range(3):
                    # pair.append((S[d] == point[d] ))
                # D.append(np.logical_and.reduce(pair))

            # D.append(np.logical_or.reduce([(S[global_d1] == self.ij_to_cube_center[coord][d1]) & (S[global_d2] == self.ij_to_cube_center[coord][d2])  for coord in self.ij_to_cube_center]  ))
            # for all center points in dims

            d = [d for d in range(3) if d not in self.dims][0]
            current_dim = (S[d] == self.center[d])
            D.append(current_dim)

        else:
            for d in range(3):
                if d in self.dims:
                    current_dim = (S[d] <= self.center[d] +1 ) & (S[d] >= self.center[d] -1 )
                    D.append((current_dim))
                else:
                    current_dim = (S[d] == self.center[d])
                    D.append((current_dim))

        return np.logical_and.reduce(D)
 

    def get_active_face_old(self, S):
        D = list()
        for d in range(3):
            if d in self.dims:
                if self.color != "#FFD65D10":
                    # print(f"{self.cubegrid=}")
                    # print(f"{get_coords_cubegrid(np.array(self.cubegrid))=}")
                    current_dim = (S[d] <= self.center[d] +1 ) & (S[d] >= self.center[d] -1  )
                else:
                    current_dim = (S[d] <= self.center[d] +1 ) & (S[d] >= self.center[d] -1 )
                D.append((current_dim))

            else:
                current_dim = (S[d] == self.center[d])
                D.append((current_dim))


        all_voxels = np.logical_and.reduce(D)

        D = []
        if self.color != "#FFD65D10":
            # add face edges:
            # print(f"{self.ij_to_cube_center=}")
            all_cords = get_coords_cubegrid(np.array(self.cubegrid))
            # for coord in all_cords:
                # if self.cubegrid[coord[0]][coord[1]] == 0: Continue
                # point = self.ij_to_cube_center[coord[0], coord[1]]     

            points = [point for (i,j), point in self.ij_to_cube_center.items() if self.cubegrid[i][j] ==1]

            for point in points:
                pair = []
                for d in range(3):
                    pair.append((S[d] == point[d] ))
                D.append(np.logical_and.reduce(pair))

        edge_voxels = np.logical_or.reduce(D)

        return  all_voxels | edge_voxels
    
    def faces_share_edge(self, other,S):
        return (self.get_face(S) & other.get_face(S)).any()
    
    def get_shared_edges(self, other, S):
        shared_cords = get_coords(self.get_face(S) & other.get_face(S))
        return shared_cords
        # print(f"{shared_cords=}")

    def same_center(self, other):
        # return True
        return self.center == other.center

    # def __str__(self):
        # chr_dict =  {1:'█',0:"o",2:'x', None: " ", 'T':'T'}
        #chr_dict =  {1:'█',0:"x"}
        # return "\n".join(["".join([chr_dict[b] for b in row]) for row in self.cubegrid])
    def set_face(self,brick):
        self.cubegrid =brick.cubegrid 
        self.color = brick.color
    def clear_face(self):
        self.cubegrid = [[0]*5]*5
    def set_cell(self,val,h,w):
        self.cubegrid[h][w] = val 

    def cubegrid_coord_dir(self):
        # pass
        # # {coord : (i,j) ~ id in cubegrid which maps to coord} 
        ij_to_cube_center = dict()
        cube_center_to_ij = dict()
        dims = list(self.dims)
        for i in range(5):
            for j in range(5):
                center = list(self.center)
                center[dims[0]] += -2 + i
                center[dims[1]] += -2 + j
                ij_to_cube_center[i,j] = tuple(center)
                cube_center_to_ij[tuple(center)] = (i,j)
                # i = e.center[f1_dims[0]] + 2 - e.f1.center[f1_dims[0]]
                # f1_j = e.center[f1_dims[1]] + 2 - e.f1.center[f1_dims[1]]
                # e.f1.ij_to_cube_center[(f1_i, f1_j)] = e.center
                # print(f"{f1_i, f1_j=}")       
        self.ij_to_cube_center = ij_to_cube_center
        self.cube_center_to_ij = cube_center_to_ij 
        
    def __getitem__(self, item):
        # item is a cubecenter tuple
        return self.dims[item]

@dataclass
class MonoCube:
    coord: tuple[int]
    faces:  list = None


    def __post_init__(self):
        self.center = 2+4*np.array(self.coord)

    def get_face_centers(self):
        for direction in [-2,2]:
            for d in DIMS:
                face_center = list(self.center)
                face_center[d] += direction
                face_center = tuple(face_center)
                yield Face(face_center, set(DIMS) - {d}) 

    def add_face(self, face):
        if self.faces == None:
            self.faces = [face]
        else:
            self.faces.append(face)

    def delete_face(self, face_center):
        pass
    # faces: list[Face]

@dataclass
class Edge:
    center : tuple[int]
    f1: Face
    f2: Face


@dataclass
class FigureSpace:

    def add_edge(self,edge):
        self.edges.append(edge)

    def edge_val(self,e):
        f1_i, f1_j = e.f1.cube_center_to_ij[e.center]
        f2_i, f2_j = e.f2.cube_center_to_ij[e.center]
        
        e_val1 = e.f1.cubegrid[f1_i][f1_j]
        e_val2 = e.f2.cubegrid[f2_i][f2_j]
        
        return e_val1 + e_val2

    def check_edge(self,e):
#         print(f"{e.f1.cubegrid=}")
        # print(f"{e.f2.cubegrid=}")
        # print(f"{e.center=}")
        # print(f"{e.f1.center=}")
        # print(f"{e.f1.dims=}")
 #        f1_dims = list(e.f1.dims)
        # f1_i = e.center[f1_dims[0]] + 2 - e.f1.center[f1_dims[0]]
        # f1_j = e.center[f1_dims[1]] + 2 - e.f1.center[f1_dims[1]]
        # # e.f1.ij_to_cube_center[(f1_i, f1_j)] = e.center
        # # print(f"{f1_i, f1_j=}")
        # # e.f1.cube_center_to_ij[e.center] = (f1_i, f1_j)
        # # e.f1.ij_to_cube_center[f1_i, f1_j] = e.center
        
        # f2_dims = list(e.f2.dims)
        # f2_i = e.center[f2_dims[0]] + 2 - e.f2.center[f2_dims[0]]
        # f2_j = e.center[f2_dims[1]] + 2 - e.f2.center[f2_dims[1]]
        # e.f2.ij_to_cube_center[(f2_i, f2_j)] = e.center
        # e.f2.edge_center_to_ij[e.f2.center] = (f2_i, f2_j)
        # e.f2.cube_center_to_ij[e.f2.center] = (f2_i, f2_j)
        # e.f2.ij_to_cube_center[f2_i, f2_j] = e.f2.center
        # e.f2.cube_center_to_ij[e.center] = (f2_i, f2_j)
        # e.f2.ij_to_cube_center[f2_i, f2_j] = e.center
        
        # self.cube_center_to_ij = cube_center_to_ij 
        if self.edge_val(e) <= 1:
            return True
        else:
            return False

    def check_all(self):
        for e in self.edges:
            if self.check_edge(e) == False:
                return False
        return True

#     def check_cube(self, center):
        # center_sum = 0
        # max_val = len(self.edge_dir[center])
        # for e in self.edge_dir[center]:
            # print(f"{e=}, {self.edge_val(e)=}")
            # center_sum += self.edge_val(e)
        # if center_sum > max_val - 1:
            # print(f"{center_sum=}")
            # return False
        # return True

    def check_complete(self):
        for center in self.edge_dir:
            # print(f"{center=}")
            center_sum = 0
            max_val = len(self.edge_dir[center])
            for e in self.edge_dir[center]:
                print(f"{e=}, {self.edge_val(e)=}")
                center_sum += self.edge_val(e)
            if center_sum > max_val - 1:
                print(f"{center_sum=}")
                return False
        return True

        # for e in self.edges:
            # if self.edge_val(e) ==0:
                # print(f"  {e}")
                # print(f"   {self.edge_val(e)}")
        # return all((self.edge_val(e)==1 for e in self.edges))


    def plot(self, color_edges = False, show=True):
        all_voxels = [f.get_active_face_old(self.S) for f in self.faces]
        voxelarray = np.logical_or.reduce(all_voxels)
        # set the colors of each object
        colors = np.empty(voxelarray.shape, dtype=object)
        # colors[link] = 'red'
        # colors[cube1] = 'blue'

        # for cube in all_voxels:
            # # colors[cube] = 'green'
            # colors[cube] = '#FFD65D30'

        for face in self.faces:
            colors[face.get_active_face_old(self.S)] = face.color
 
        if color_edges:
            for edge in self.edges:
                colors[Voxel(*edge.center).get_index(self.S)] = 'red'

   
        # asd = C.get_index(S)
        # print(f"{asd=}")

        # for C in voxels:
            # colors[C.get_index(S)] = 'blue'

        # and plot everything
        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxelarray, facecolors=colors, edgecolor='k', linewidth=0.1)

        ax.set_xlim([0, voxelarray.shape[0]])
        ax.set_ylim([0, voxelarray.shape[1]])
        ax.set_zlim([0, voxelarray.shape[2]])
        plt.axis("off")
        ax.set_box_aspect((1, 1, 1))
        if show:
            plt.show()

    
        def __iter__(self):
            return iter(self.Faces)


def setup_FigureSpace(n, k, cube_cords = None, max_faces = None):

    if not cube_cords:
        cubes_coords_list = generate_cube_coords(n)
        print(f"possible polycubes of size n={n} is k={len(cubes_coords_list)}")
        cube_cords = cubes_coords_list[k]
    space_size = max([ 5*(max(coord)+1) for coord in cube_cords])
    x, y, z = np.indices((space_size, space_size, space_size))
    S = (x,y,z)
    F = FigureSpace()
    F.S = S

    # generate all not duplicate face centers
    all_face_centers = set()  # dict with face_center : {MC ids} 
    face_center_duplicates = set()
    monocubes = [MonoCube(cords) for cords in cube_cords]
    for MC in monocubes:
        # print(f"{MC=}")
        for f in MC.get_face_centers():
            if f.center not in all_face_centers:
                all_face_centers.add(f.center)
            else:
                face_center_duplicates.add(f.center)

    # filter out duplicates
    # print(f"{len(face_center_duplicates)=}")
    all_face_centers = all_face_centers - face_center_duplicates

    all_faces = []

    F.faces = all_faces

    # return if there are more faces in the figure than possible, as determined by the arg max_faces
    if max_faces and len(F.faces) > max_faces:
        return F

    # add all faces
    for MC in monocubes:
        for f in MC.get_face_centers():
            if f.center in all_face_centers:
                MC.add_face(f)
                all_faces.append(f)
                # print(f"   {f}")

        # print(f"{len(MC.faces)=}")

    for f in F.faces:
        # print(f"{f}")
        f.cubegrid_coord_dir()

        # print(f"{f.ij_to_cube_center=}")
        
    
    shared_edges = []
    edges = []
    for i, f1 in enumerate(all_faces):
        for j, f2 in enumerate(all_faces):
            if i >= j: continue
            if f1.center == f2.center: continue
            # if f1.same_center(f2):
            if f1.faces_share_edge(f2, S):
                f1_f2_edges = f1.get_shared_edges(f2, S)
                for edge in f1_f2_edges:
                    edges.append(Edge(edge,f1,f2))
            
                shared_edges += f1_f2_edges
                # print(f"   {f1} and {f2} edge")
                # print(f"{f1.get_face(S)}")


    # create edge_dir
    #edge_dir = {cube_center : list[edges] with cube center cube_center }
    edge_dir = {}
    for e in edges:
        if e.center not in edge_dir:
            edge_dir[e.center] = [e]
        elif e.center in edge_dir:
            edge_dir[e.center].append(e)

    F.edge_dir = edge_dir
    


    F.edges = edges


    return F




def main():
    cubes_coords_list = generate_cube_coords(2)
    # cube_cords = [(0,0,0), (0,0,2), (0,1,0), (3,2,1),(1,2,3)]
    cube_cords = cubes_coords_list[0]
    space_size = max([ 5*(max(coord)+1) for coord in cube_cords])
    print(f"{space_size=}")
    x, y, z = np.indices((space_size, space_size, space_size))
    S = (x,y,z)

    F = FigureSpace()
    F.S = S
    # generate all not duplicate face centers
    all_face_centers = set()  # dict with face_center : {MC ids} 
    face_center_duplicates = set()

    monocubes = [MonoCube(cords) for cords in cube_cords]
    for MC in monocubes:
        print(f"{MC=}")
        for f in MC.get_face_centers():
            if f.center not in all_face_centers:
                all_face_centers.add(f.center)
            else:
                face_center_duplicates.add(f.center)

    # filter out duplicates
    print(f"{len(face_center_duplicates)=}")
    all_face_centers = all_face_centers -face_center_duplicates

    all_faces = []

    F.faces = all_faces

    # add all faces
    for MC in monocubes:
        for f in MC.get_face_centers():
            if f.center in all_face_centers:
                MC.add_face(f)
                all_faces.append(f)
                print(f"   {f}")

        print(f"{len(MC.faces)=}")

    shared_edges = []
    edges = []
    for i, f1 in enumerate(all_faces):
        for j, f2 in enumerate(all_faces):
            if i >= j: continue
            if f1.center == f2.center: continue
            # if f1.same_center(f2):
            if f1.faces_share_edge(f2, S):
                f1_f2_edges = f1.get_shared_edges(f2, S)
                for edge in f1_f2_edges:
                    edges.append(Edge(edge,f1,f2))

                shared_edges += f1_f2_edges
                # print(f"   {f1} and {f2} edge")
                # print(f"{f1.get_face(S)}")

    F.edges = edges



    print(f"{edges[0]=}")
    print(f"{f1=}")
    print(f"{f2=}")
    print(f"{f1.faces_share_edge(f2, S)=}")

    
    print(f"{f1.get_shared_edges(f2, S)=}")

    
    # voxels = [Voxel(*coord) for coord in f1.get_shared_edges(f2, S)]
    print(f"{shared_edges=}")
    voxels = [Voxel(*coord) for coord in shared_edges]
    faces = [f1,f2] + all_faces

    # cubes = [2+ 4*np.array(cords) for cords in cube_cords]
    # voxels = []
    # faces = []

    # for center in cubes:    

        # for d in DIMS:
            # for direction in [-2,2]:
                # v = np.zeros(3)
                # v[d] = direction 
                # voxels.append(Voxel(*(v + center)))
                # faces.append(Face(center = Voxel(*(v + center)), dims = set(DIMS) - {d}))

  
    all_voxels = [f.get_face(S) for f in faces] + [C.get_index(S) for C in voxels]
    voxelarray = np.logical_or.reduce(all_voxels)
    # set the colors of each object
    colors = np.empty(voxelarray.shape, dtype=object)
    # colors[link] = 'red'
    # colors[cube1] = 'blue'

    for cube in all_voxels:
        # colors[cube] = 'green'
        colors[cube] = '#FFD65DC0'

    # asd = C.get_index(S)
    # print(f"{asd=}")

    for C in voxels:
        colors[C.get_index(S)] = 'blue'

    # and plot everything
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(voxelarray, facecolors=colors, edgecolor='k', linewidth=0.1)

    ax.set_xlim([0, voxelarray.shape[0]])
    ax.set_ylim([0, voxelarray.shape[1]])
    ax.set_zlim([0, voxelarray.shape[2]])
    plt.axis("off")
    ax.set_box_aspect((1, 1, 1))
    plt.show()


if __name__ == "__main__":
    main()
        
