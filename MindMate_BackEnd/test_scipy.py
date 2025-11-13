import test_scipy
import scipy.sparse
print("SciPy version:", test_scipy.__version__)
print("SciPy path:", test_scipy.__file__)
from scipy.sparse import coo_matrix
print("coo_matrix:", coo_matrix)