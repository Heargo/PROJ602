from Grid import *
import numpy as np
from scipy.sparse import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
import polyscope as ps


#load .obj and get the list of vertices
def loadVertices(filename):
    """
    load les vertices d'un fichier .obj
    """
    with open(filename) as f:
        lines = f.read().splitlines()
    vertices = []
    for line in lines:
        if line.startswith('v '):
            vertices.append(line.split(' ')[1:])
    #to np array
    vertices=np.array(vertices)
    return vertices

def loadFaces(filename):
    """
    Load les faces d'un fichier .obj
    """
    with open(filename) as f:
        lines = f.read().splitlines()
    faces = []
    #génère le tableau des faces
    for line in lines:
        if line.startswith('f '):
            face = line.split(' ')[1:]
            cleanFace=[]
            for point in face:
                cleanFace.append(int(point.split('/')[0]))
            faces.append(cleanFace)
    #to np array
    faces=np.array(faces)
    #pour chaque face, on enleve 1 à chaque indice de points afin (les .obj commence à 1)
    faces=faces-1
    return faces

if __name__ == "__main__":
    #charge les vertices et faces
    obj="dragon" #use arm, alien, dragon, bubble or cat /!\ alien et dragon prenent du temps
    Affiche_prct_progression=True #conseillé pour alien et dragon.
    vertices=loadVertices('./data/'+obj+'.obj')
    faces=loadFaces('./data/'+obj+'.obj') #bug si pas que des triangles ? 
        

    #creer la grille
    G = Grid(vertices=vertices, faces=faces)
    print("Model loaded")
    #choisi une source
    #source=(float(vertices[0][0]), float(vertices[0][1]), float(vertices[0][2]))

    #init la matrice des sources
    if obj=="arm":
        sources=[44712,9401,5778,7548,11316,18775]
    elif obj=="cat":
        sources=[78783,469]
    elif obj=="alien":
        sources=[387810]
    elif obj=="dragon":
        sources=[311627]
    else:
        sources=[0]
    U0=G.sources(sources)
    print("Sources initialized")
    # print(U0)

    #calcule la propagation à un temps T
    U=G.implicitEuler( U0, 1000, 10,debug=Affiche_prct_progression ) # T=100
    print("Propagation done")

    # print(U)

    
    ps.init()
    ps_mesh=ps.register_surface_mesh("sphere", vertices, faces)
    ps_mesh.add_scalar_quantity("propagation", U, defined_on='vertices')
    ps.show()
