"""CRG1's C1: native N cold dark energy profile, no response, background A, reading A1a, capped at R200. A KNOWN-ANSWER candidate only. The cold sector stays retired and nothing here reinstates it; only the owner can. Reads lgMb, a measured baryon mass; absent from a row's Q, the row is NOT COMPUTABLE."""
import json, math, os, sys
import numpy as np
NAME = "cold halo, CRG1 C1, retired, known answer only"; VERTICAL = ()
_HERE = os.path.dirname(os.path.abspath(__file__)); _RB = os.path.join(_HERE, "..", ".."); _P = {}
READ_RECORD = "CRG1 C1, not computed here, never a pass: keys 12 of 15, G-OUT-M3 +4.41; X-COP +0.013, 0.075; Dw MW ultra-faint +5.02; MW FEASIBLE (WIDE PRIORS ONLY)"
def _core():
    if "nr" in _P: return _P
    import crg1_core as C
    v = json.load(open(os.path.join(_RB, "CRG1_clean_room_regrade", "v1", "crg1_results.json")))["C1"]["canonical"]["detail"]
    A = _find(v, "A1a_values"); _P.update(C=C, b=C.bg("A_c2b_refit"), nr=C.NR(A["eta12"], A["rho10"], A["rho11"], "A1a"), mem={}); return _P
def _find(d, k):
    if isinstance(d, dict):
        if k in d: return d[k]
        for x in d.values():
            r = _find(x, k)
            if r is not None: return r
    return None
def g(Q):
    gb = np.asarray(Q["gb"], float); lgMb = float(Q["lgMb"]); r = np.asarray(Q["r"], float); P = _core(); C = P["C"]; E = C.E; b = P["b"]
    if lgMb not in P["mem"]:
        lg = float(b.lgM200(lgMb)); M200 = 10 ** lg * E.Msun; R2 = C.R200_of(M200, b.h, E.G, E.Mpc); S = P["nr"].S(10 ** lg / C.f_c, b); P["mem"][lgMb] = (R2, S, C.solve_r0(M200, R2, S, C.B_S))
    R2, S, r0 = P["mem"][lgMb]
    return gb + E.G * math.pi * S * r0 ** 2 * C.B_S(np.minimum(r, R2) / r0) / r ** 2
