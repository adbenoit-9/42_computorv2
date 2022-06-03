from ft_complex import Complex
from ft_matrix import Matrix
from parser import Parser
import sys

p = Parser({})
print(p.reduce(sys.argv[1]))
