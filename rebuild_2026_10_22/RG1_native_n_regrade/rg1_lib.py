"""RG1: read the native-N table. S in Msun/pc^2 against M200 in Msun."""
import json, math, os
import numpy as np
_T = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rg1_rule_table.json")))
MUT = 0.5 if os.environ.get("RG1_MUTATE") == "1" else 1.0; FC = _T["fc"]
_L = {"A_c2b_refit": np.log10(_T["A"]), "B_cfg886_bg": np.log10(_T["B"])}; _G = np.array(_T["lg"])
def S_nat(M200, tag="A_c2b_refit"): return MUT * 10 ** float(np.interp(math.log10(M200), _G, _L[tag]))
def S_mt(Mt, tag="A_c2b_refit"): return S_nat(Mt * FC, tag)
def B_smooth(x):
    x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
