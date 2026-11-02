"""MX1 cell FL. Rule in mx1_core.py. Reinstates nothing; kappa = 1/2 FITTED."""
import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("mx1_core", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "mx1_core.py")); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_r = _m.rule("FL"); NAME = "MAX MX1 cell FL"; VERTICAL = ("R", "A")
def g(Q): return _r.g(Q)
