
# Dessin en lignes droites de graphes planaires sur une grille
Implémentation Python d'un algorithme de dessin de graphe planaire proposé par de Fraysseix [1]. Cet algorithme, basé sur l'ordre canonique, prend en entrée un graphe planaire triangulé et retourne une liste associant chaque sommet à sa position sur une grille.

---

## Guide d'utilisation

### Librairies nécessaires

- *networkx* 
- *matplotlib*
- *numpy*

### Dessin de graphe sur une grille

Ouvre une fenêtre matplotlib affichant le dessin d'un graphe de la liste spécifiée. Des boutons permettent de changer le graphe affiché. Il est possible d'afficher les arêtes ajoutées pour trianguler le graphe ("dummy edges") ainsi que l’étiquetage des sommets correspondant à l'ordre canonique utilisé pour construire le dessin.

```
python main.py [-h] [-m MIN] [-M MAX] [-t] files [files ...]
```
       
Les différentes arguments sont les suivants:
- arguments positionnels:
  - files : spécifie les différents fichiers contenant les graphes qui seront traités. Si des graphes non-planaires sont trouvés, ils seront ignorés.
- arguments optionnels:
  - -h, --help : affiche l'aide.
  -  -m MIN, --min MIN : spécifie la taille minimale des graphes traités. Les graphes comptant trop peu de sommets sont ignorés.
  - -M MAX, --max MAX : spécifie la taille maximale des graphes traités. Les graphes trop grands sont ignorés.
  - -t, --tk : les graphes seront dessinés directement sur un canvas *tkinter* plutôt que dans une fenêtre matplotlib. Les dessins produits sont moins jolis et il n'est pas possible de ne pas afficher les "dummy edges", l'intention était de n'utiliser que matplotlib. Mais cette solution s'avérant beaucoup plus rapide, il est possible de l'utiliser via cette option.

optional arguments:
  -h, --help         show this help message and exit
  -m MIN, --min MIN  Specify the minimum size of the graphs treated. The too
                     little graphs are ignored.
  -M MAX, --max MAX  Specify the maximum size of the graphs treated. The too
                     big graphs are ignored.
  -t, --tk           Execute a tkinter window that displays the straight line
                     drawing of the specified graphs.The drawing is less
                     pretty than with matplotlib but faster.

Voici un exemple d'affichage de graphe:
![exMain](./pictures/exMain.png)

### Mesure du temps nécessaire à calculer le dessin

Le script *measure_time.py* mesure le temps nécessaire à calculer le dessin planaires des graphes spécifiés et porte les résultats en graphique. Pour chaque graphe, le temps mesuré désigne le temps nécessaire pour les étapes de : triangulation, calcul d'un ordre canonique et shift-algorithm. Le temps est mesuré à l'aide de la librairie *timeit*.

```
python measure_time.py [-h] [-m MIN] [-M MAX] [--repeat REPEAT] [-r] files [files ...]
```

Les différentes arguments sont les suivants:
- arguments positionnels:
  - files : spécifie les différents fichiers contenant les graphes qui seront traités. Si des graphes non-planaires sont trouvés, ils seront ignorés.
- arguments optionnels:
  - -h, --help : affiche l'aide.
  -  -m MIN, --min MIN : spécifie la taille minimale des graphes traités. Les graphes comptant trop peu de sommets sont ignorés.
  - -M MAX, --max MAX : spécifie la taille maximale des graphes traités. Les graphes trop grands sont ignorés.
  - \-\-repeat REPEAT : spécifie le nombre de mesures opérées sur chaque graphe. La mesure du temps affichée sera la moyenne des temps observés.
  - -r, --regression  : si cet argument est présent, une droite de régression est affichée.

Voici un exemple de graphique obtenu:
![exPlot](./pictures/exPlot.png)



---

[1] Hubert de Fraysseix, János Pach, and Richard Pollack. How to draw a planar graph on a grid. *Combinatorica*, 10(1) :41–51, 1990.


