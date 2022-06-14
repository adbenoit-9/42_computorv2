# COMPUTORV2 (@Paris)

*Ton bc fait maison*

computor-v2 is an instruction interpreter that, like a shell, retrieves user inputs for advanced computations.

Mathematical types supported:
- Rational numbers
- Complex numbers (with rational coefficients)
- Matrices
- Polynomial equations of degrees less than or equal to 2

Operations supported: 
- multiplication: *
- division: /
- addition: +
- substraction: -
- modulo: %
- matrix multiplication: **

## Usage
```
$ git clone https://github.com/adbenoit-9/42_computorv2.git
$ cd 42_computorv2
$ python3 computorv2.py
>
```
### Variable

*var_name*: only contain letters and is case insensitive
*expression*: a computation with no unknown variable (function image, matrix, complex,real, etc..)

- Assignment
```
> var_name = expression
```

### Function
*funct_name*, *param*: only contain letters and is case insensitive \
*expression*: a computation with only one unknown variable (function, matrix, complex,real, etc..)

- Assignment
```
> funct_name(param) = expression
```

- Image
```
> funct_name(expression) = ?
```

- Resolve Polynomial
```
> funct_name(var_name) = expression ?
```

### Resolution of a computation
```
> computation = ?
```

### Matrix

syntax: `[[A0-0, A0-1, ...]; [A1-0, A1-1, ...]; ...]` A ∈ Mn-p(Q)\
The semicolon is used to separate the rows of a matrix\
the comma is used to separate the columns of a matrix

### Complex

syntax: `a + bi` (a, b) ∈ Q2

### Bonus

- Function Composition
- Usual functions supported:
    - exponential: `exp(expression)`
    - square root: `sqrt(expression)`
    - absolute value: `|expression|`
    - cosine: `cos(expression)`
    - sinus: `sin(expression)`
    - tangent: `tan(expression)`
- Display of the list of stored variables and their values
```
> show data
```