from ft_complex import Complex
from ft_matrix import Matrix

mat = Matrix([[1, 2, 5], [Complex(1, 2), 3, 3.]])

mat = Matrix((2, 3), 4)
mat1 = Matrix((3, 2), 2)
mat2 = Matrix((3, 3), 2)
print(repr(mat))
print(repr(mat1))
print(repr(mat ** mat1))
