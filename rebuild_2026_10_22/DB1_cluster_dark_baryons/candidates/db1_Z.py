"""DB1 arm Z, unedited rule in ../db1_core.py. A description; carries [LABEL]. Reinstates nothing."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db1_core as C
NAME = "DB1 arm Z"; VERTICAL = ("R",); TRAINED_ON = ("xcop",)
def g(Q): return C.g(Q, "Z")
