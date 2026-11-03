"""MB1 arm K, unedited rule in ../mb1_core.py. A description; carries [LABEL]. Reinstates nothing."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mb1_core as C
NAME = "MB1 arm K"; VERTICAL = ("R",); TRAINED_ON = ("xcop",)
def g(Q): return C.g(Q, "K")
