# PROJ602
Calcul de distances et de géodésiques sur des surfaces triangulées

## Quels sont les librairies utilisées ?
- [`numpy`](https://numpy.org/)
- [`matplotlib`](https://matplotlib.org/)
- [`scipy`](https://www.scipy.org/)
- [`polyscope`](https://polyscope.run/)

Pour les installer:

```sh
pip install numpy matplotlib scipy polyscope
```

## Comment lancer le projet ?
```sh 
python main.py path/fichier.obj
```
Le fichier obj doit être triangulé. Pour trianguler un obj, utiliser Blender. [Docs Blender](https://docs.blender.org/manual/fr/dev/modeling/modifiers/generate/triangulate.html)
Par defaut, si le chemin n'est pas précisé le projet utilise le fichier `./data/arm.obj`

