### Dessin en lignes droites de graphes planaires sur une grille

Implémentation Python d'un algorithme basé sur l'ordre canonique proposé par de Fraysseix [1]. Cet algorithme prend en entrée un graphe planaire triangulé et retourne une liste associant chaque sommet à sa position sur une grille.

---

La bibliothèque networkx est utilisée pour calculer les plongements planaires et trianguler les graphes traités [2].
La visualisation graphique est réalisée à l'aide de tkinter.

---

[1] Hubert de Fraysseix, János Pach, and Richard Pollack. How to draw a planar graph on a grid. *Combinatorica*, 10(1) :41–51, 1990.

[2] https://networkx.github.io/documentation/stable/reference/algorithms/planarity.html
