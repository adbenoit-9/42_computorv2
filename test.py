from complex import Complex
from vector import Vector

comp1 = Complex(1, 2)
comp2 = Complex(1, 2)
comp3 = Complex(2, 3)
comp4 = Complex()
print(str(comp1))
print(str(comp3))
print(comp1 != comp3)
comp1 = comp3.copy()
comp3.real = 0
print(str(comp1))
