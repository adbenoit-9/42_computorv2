stockage data: `dictionary`

# TO DO
- Class:
    - [x] Complex
    - [x] Matrix
    - [x] Function

- function
    - [x] equation syntax
    - [ ] resolve
        - [x] y is real
        - [ ] y is complex
        - [ ] y is matrix: error
        - [x] replace X by the parameter name
    - [ ] calculate image
        - [x] x is real
        - [ ] x is complex
        - [ ] x is matrix
        - [x] x is calc
        - [x] x formula
    - [x] handle var

- expression:
    - [x] name format
    - [x] replace var in simple calcul
    - [x] replace var in function
    - [x] real type
    - [ ] matrix type
    - [x] function type
    - [ ] complex type
    - [ ] decomposition: pas sure que ca soit la bonne solution

- priority:
    - [x] mul/div/mod
    - [x] bracket calc
    - [ ] bracket function

- [x] exit program : quit and CTRL+D

- to handle:
    - [x] 7 * x * 6
    - [x] x^2^3 => 2 * 3
    - [ ] f(x) = 7 + i
    - [ ] f(x) = i ?
    - [ ] (3 + 8i) * 2

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
    - [x] Ajout de fonctions usuelles (exponentielle, racine carrée, valeur absolue, cosinus, sinus, tangente, etc.)

- parsing flemme:
    - [ ] Calcul de norme
    - [ ] Inversion de matrice et d'autres deja fait dans Matrix
    - [ ] Ajout du calcul en radian pour les angles

- parsing mega flemme:
    - [ ] Composition de fonction

- facile si pyplot autorise
    - [ ] Affichage de courbe de fonctions
