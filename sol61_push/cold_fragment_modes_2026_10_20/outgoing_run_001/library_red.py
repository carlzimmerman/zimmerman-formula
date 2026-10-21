"""Test first: the existing l0/l2 helper is insufficient for natural l4 radiation."""
from pathlib import Path
import math,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from outgoing_test import poly
z=2.0
want=sum(math.factorial(4+k)/(math.factorial(k)*math.factorial(4-k))*(-1j/(2*z))**k for k in range(5))
assert abs(poly(4,z)-want)<1e-13, 'The old finite-ell polynomial must be extended before l4 natural-source use'
