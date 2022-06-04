from ft_complex import Complex
from ft_matrix import Matrix
from parser import Parser
import sys
from decompose import decompose

# p = Parser({})
# print(p.reduce(sys.argv[1]))
print(decompose(sys.argv[1]))

