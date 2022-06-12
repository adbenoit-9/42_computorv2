stockage data: `dictionary`

# TO DO
- Class:
    - [x] Complex
    - [x] Matrix
    - [x] Function

- function
    - [x] equation syntax
    - [x] resolve
        - [x] y is real
        - [x] y is complex
        - [x] y is matrix: error
        - [x] replace X by the parameter name
    - [x] calculate image
        - [x] x is real
        - [x] x is complex
        - [x] x is matrix
        - [x] x is calc
        - [x] x formula
    - [x] handle var

- expression:
    - [x] name format
    - [x] replace var in simple calcul
    - [x] replace var in function
    - [x] real type
    - [x] matrix type
    - [x] function type
    - [x] complex type
    - [x] decomposition

- priority:
    - [x] mul/div/mod
    - [x] bracket calc
    - [x] bracket function

- [x] exit program : quit and CTRL+D

- to handle:
    - [x] 7 * x * 6
    - [x] x^2^3 = x^(2 * 3)
    - [x] f(x) = 7 + i*x => f(2+x)
    - [x] (3 + 8i) * 2
    - [x] x*(3-4)
    - [x] f(3+4)
    - [x] (4+x)^2 + 3
    - [x] f(x)=tan(x)
    - [x] 16+4*1+4*1+1^2+3
    - [x] funB(y) = 43 * y / (4 % 2 * y)
    - [x] funC(z) = -2 * z - 5
    - [x] funA(2) + funB(4) = ? (funA(x) = 2 * 4 + x, funB(x) = 4 -5 + (x + 2)^2 - 4)
    - [x] funA(2) + funB(4) = ? (funA(x) = 2 * 4 + x, funB(y) = 43 * y / (4 % 2 * y)
    - [x] 4 / (2+i) = ? 
    - [ ] ([[2,3];[4,3]] + [[2,3];[4,3]]) * 3
    - [x] f(x) = exp(x)  => f(2) = ?
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
    - [x] Afficher la liste des variables stockées ainsi que leurs valeurs
    - [x] Historique des commandes avec résultats
    - [x] Ajout de fonctions usuelles (exponentielle, racine carrée, valeur absolue, cosinus, sinus, tangente, etc.)
    - [x] Composition de fonction
    - [x] matrix transpose

- parsing flemme:
    - [ ] Calcul de norme
    - [ ] Inversion de matrice et d'autres deja fait dans Matrix
    - [ ] Ajout du calcul en radian pour les angles

- facile si pyplot autorise
    - [ ] Affichage de courbe de fonctions
