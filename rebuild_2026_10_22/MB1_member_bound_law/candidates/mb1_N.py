"""MB1 arm N, unedited rule in ../mb1_core.py. A description; carries [LABEL]. Reinstates nothing."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mb1_core as C
NAME = "MB1 arm N"; VERTICAL = ("R",)
def g(Q): return C.g(Q, "N")
