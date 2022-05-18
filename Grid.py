import numpy as np
from scipy.sparse import *
from scipy.sparse.linalg import splu
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import sqrt

class Grid:
    
    def __init__( self, nbrow=None, nbcol=None,image=None,vertices=None,faces=None):
        """
        Constructeur. Fabrique une grille avec `nbrow` lignes et `nbcol` colonnes.
        """
        self.vertices = vertices
        self.faces = faces
        self.neighborsRegister=self.getNeighbors(vertices,faces)
        self.index={}
        for i in range(len(vertices)):
            x=vertices[i][0]
            y=vertices[i][1]
            z=vertices[i][2]
            self.index[(float(x),float(y),float(z))]=1
   
    def getNeighbors(self,vertices, faces):
        """
        Initialise un dictionnaire qui associe à chaque indice de points un tableau d'indices de voisins
        """
        neighbors = {}
        for i in range(len(vertices)):
            neighbors[i] = []
        #pour chaque face
        for face in faces:
            #on regarde chaque sommet de la face
            for i in range(len(face)):
                #on ajoute l'indice du voisin de droit et de gauche dans le tableau de voisins de l'indice i
                current=face[i]
                voisin = face[(i+1)%len(face)]
                voisin2 = face[(i-1)%len(face)]
                #si ils ne sont pas déjà dans le tableau de voisins
                if voisin not in neighbors[current]:
                    neighbors[current].append(voisin)
                if voisin2 not in neighbors[current]:
                    neighbors[current].append(voisin2)
        return neighbors

    def neighbors3D(self,idx):
        """
        Retourne la liste des voisins d'indice `idx`
        """
        return self.neighborsRegister[idx]    
    
    def size(self):
        """
        Taille n du vecteur u.
        """
        return len(self.vertices)

    def Identity(self):
        """
        Retourne la matrice identité de taille nxn
        """
        n = self.size()
        LIGS = [] # les lignes des coefficients
        COLS = [] # les colonnes des coefficients
        VALS = [] # les valeurs des coefficients
        for idx in range(n):
            LIGS.append( idx )
            COLS.append( idx )
            VALS.append( 1.0 )
        M = coo_matrix( (VALS,(LIGS,COLS)), shape = (n,n) )
        return M.tocsc()

    def Laplacian(self,debug=False):
        """
        Retourne la matrice du Laplacien de la grille
        """
        n = self.size()
        LIGS = [] # les lignes des coefficients
        COLS = [] # les colonnes des coefficients
        VALS = [] # les valeurs des coefficients
        if debug:
            print("Laplacien...")
        #on parcours tout les pixel de la grille
        for idx in range(n):
            #on ajoute la diagonale
            VALS.append( -len(self.neighbors3D(idx)) )
            LIGS.append( idx )
            COLS.append( idx )
            #pour chaque voisin on met un coefficient 1
            for idx_voisin in self.neighbors3D(idx):
                VALS.append( 1 )
                LIGS.append( idx )
                COLS.append( idx_voisin )
            
        
        M = coo_matrix( (VALS,(LIGS,COLS)), shape = (n,n) )
        return M.tocsc()

    def implicitEuler( self, U0, T, dt,debug=False ):
        """
        A partir du vecteur de valeurs U0, calcule U(T) en itérant des pas 
        dt successifs.
        """
        #On calcule A
        A = (self.Identity() - dt*self.Laplacian(debug))
        b = np.array(U0)
        #On calcule la matrice LU
        LU = splu(A)

        if debug:
            print("Diffusion...")
        for i in range( int(T/dt) ):
            #On résoud A*U = b
            b = LU.solve(b)
            if debug:
                print("diffusion",i*100/int(T/dt),"%")
        return b
    
    def sources( self,list_sources ):
        """
        Initialise le vecteur de valeurs contenant les sources d'émissions.
        """
        n = self.size()
        U0 = np.zeros(n)
        for e in list_sources:
            U0[e] = 1
        return U0