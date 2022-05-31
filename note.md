stockage data: `dictionary`

# TO DO
- [ ] Class:
    - [x] Complex : projet matrix
    - [x] Matrix : piscine python vector
    - [ ] Function : decomposition ?

- [ ] function
    - [ ] equation syntax
    - [ ] resolve
        - [x] y is real
        - [ ] y is complex
        - [ ] y is matrix
        - [ ] replace X by the parameter name
    - [x] calculate image
    - [] handle var

- [ ] matrix:
    - [ ] parse

- [ ] var:
    - [x] name format
    - [x] replace var in simple calcul
    - [ ] replace var in function
    - [x] real type
    - [ ] matrix type
    - [ ] function type
    - [ ] complex type

- [ ] priority:
    - [x] mul/div/mod
    - [ ] bracket

- [x] exit program : quit and CTRL+D

---
# example
```
> var1=6
> funct1(x) = x + 3
> mat1 = [[2, 3]; [1, 0]]
> comp1 = 1 + 4i
```
```
data = {
    'var1' = 6,
    'funct1' = Function("x + 3"),
    'mat1' = Matrix([[2, 3], [1, 0]]),
    'comp1' = Complex(1, 4)
}
```
---

# bonus
- facile:
    - [ ] Afficher la liste des variables stockées ainsi que leurs valeurs
    - [ ] Historique des commandes avec résultats (pas fun)

- parsing flemme:
    - [ ] Calcul de norme
    - [ ] Inversion de matrice et d'autres deja fait dans Matrix
    - [ ] Ajout du calcul en radian pour les angles
    - [ ] Ajout de fonctions usuelles (exponentielle, racine carrée, valeur absolue, cosinus, sinus, tangente, etc.)

- parsing mega flemme:
    - [ ] Composition de fonction

- facile si pyplot autorise
    - [ ] Affichage de courbe de fonctions