"""UX3's term, unswitched: g = law x (1 + k g_gas/a0), k fitted on X-COP per footing (ux3_kfit.json). FITTED, a description, no action. A known-answer candidate; X-COP is its training set. kappa = 1/2 FITTED."""
import json, os
import numpy as np
NAME = "UX3 term, k fit, unswitched"; VERTICAL = ("R",); TRAINED_ON = ("xcop",)
_HERE = os.path.dirname(os.path.abspath(__file__)); _K = json.load(open(os.path.join(_HERE, "..", "..", "UX3_cluster_gas_term", "ux3_kfit.json")))
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]; k = _K["canonical"] if a < 1.0e-10 else _K["alt"]; gg = np.maximum(np.asarray(Q["gg"], float), 0.0)
    with np.errstate(all="ignore"): L = np.where(gb > 0, gb * (0.5 + np.sqrt(0.25 + a / np.where(gb > 0, gb, 1.0))), gb)
    return L * (1 + k * gg / a)
