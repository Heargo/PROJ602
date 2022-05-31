from Grid import *
import numpy as np
from scipy.sparse import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
import polyscope as ps
import polyscope.imgui as psim
import sys


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

def addSource():
    # ... do something important here ...
    print("executing function")

if __name__ == "__main__":
    #charge les vertices et faces
    path="./data/arm.obj" #use arm, alien, dragon, bubble or cat /!\ alien et dragon prenent du temps
    if len(sys.argv)>1:
        path=sys.argv[1]
    Affiche_prct_progression=True #conseillé pour alien et dragon.
    vertices=loadVertices(path)
    faces=loadFaces(path) #bug si pas que des triangles ? 
        

    #creer la grille
    G = Grid(vertices=vertices, faces=faces)
    sources=[]
    print("Model loaded")

    # Define our callback function, which Polyscope will repeatedly execute while running the UI.
# We can write any code we want here, but in particular it is an opportunity to create ImGui 
# interface elements and define a custom UI.
def callback():
    global sources
    psim.PushItemWidth(150)
    psim.TextUnformatted("Séléctionnez un point pour ajouter une source.")
    #input
    # sourceCustom=psim.InputInt("Id du point ")
    psim.Separator()

    #liste des sources
    psim.TextUnformatted("Liste des sources")
    #affiche chaque id de la liste sources
    for i in range(len(sources)):
        psim.TextUnformatted(str(sources[i]))
    psim.Separator()

    if(psim.Button("Ajouter une source")):
        # This code is executed when the button is pressed
        newSource=int(ps.get_selection()[1])
        if newSource<len(vertices):
            sources.append(newSource)
    
    if(psim.Button("Reset les sources")):
        sources=[]
    
    if(psim.Button("Diffuse")):
        U0=G.sources(sources)
        U=G.implicitEuler( U0, 100, 50,debug=Affiche_prct_progression )
        ps_mesh.add_scalar_quantity("propagation", U, defined_on='vertices')
        print("Diffusion terminée")

    



ps.init() 
ps.set_user_callback(callback)
ps_mesh=ps.register_surface_mesh("sphere", vertices, faces)
ps.show()
