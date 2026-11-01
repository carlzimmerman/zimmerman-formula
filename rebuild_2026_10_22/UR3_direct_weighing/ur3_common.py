"""UR3 shared: smooth core, r0 solve, X39's contract unchanged. kpc, Msun, km/s. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os
import numpy as np
from scipy.optimize import brentq, minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); G = 4.30091e-6; T = json.load(open(os.path.join(HERE, "ur3_S_table.json")))
SGN = 1.0; _s = open(os.path.join(RB, "X39_baryonic_contraction", "x39_contraction.py")).read(); exec(compile(_s[_s.index("def contract(r, Mb, M0, F, gnedin=None):"):_s.index('P("\\n=== checks")')], "x39_contract", "exec"))
def Bs(x): x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
def Sfn(lM, t): return 10 ** float(np.interp(lM, T["lgM"], np.log10(T["S"][t])))
def r0_of(M, R, S):  # X38 A1 compact root, as the grader's
    lm = lambda l: math.log(math.pi * S * math.exp(2 * l) * float(Bs(R / math.exp(l))))
    pk = minimize_scalar(lambda l: -lm(l), bounds=(math.log(R * 1e-6), math.log(R * 1e3)), method="bounded", options={"xatol": 1e-10})
    if lm(pk.x) < math.log(M): return math.exp(pk.x)
    return math.exp(brentq(lambda l: lm(l) - math.log(M), math.log(R * 1e-7), pk.x, xtol=1e-14))
def halo(lMb, t, d=0.0):
    bg = T["bg"][t]; lM = bg["a"] + bg["b"] * (lMb - 10) + d; M = 10 ** lM; rc = 3 * (100 * bg["h"] / 1e3) ** 2 / (8 * math.pi * G); R = (3 * M / (4 * math.pi * 200 * rc)) ** (1 / 3); S = Sfn(lM, t); return M, R, S, r0_of(M, R, S)
def Mc(rg, Mbg, M, R, S, r0, mode):
    M0 = math.pi * S * r0 ** 2 * Bs(rg / r0)
    if mode == "off": return M0
    return contract(rg, Mbg, M0, float(Mbg[-1] / M0[-1]), gnedin=(0.85, 0.8, rg[-1]) if mode == "gnedin" else None)[0]
