"""project_atomos engine — symbolic-regression search adapted for dimensionless SM targets.

Ported from hali_flow/bruteflow (symbolic_search.py + constrained_search.py), the engine that
found a0 = c sqrt(G rho_c)/2 -> cH0/sqrt(32pi/3). See notes/ENGINE_REVERSE_ENGINEERING.md.

The engine's ONLY job is cheap candidate generation under a hard structural filter, ranked by
closeness. It hands candidates to the gate; it does NOT self-certify. The whole value of the
project lives in gate/ (FDR survival + forced kernel + interlock).
"""
from .expr_tree import ExprNode, OpType, Label, DIMENSIONLESS, ACCELERATION
from .alphabet import Alphabet, build_default_alphabet
from .search import Grammar, Search

__all__ = [
    "ExprNode", "OpType", "Label", "DIMENSIONLESS", "ACCELERATION",
    "Alphabet", "build_default_alphabet", "Grammar", "Search",
]
