#!/usr/bin/env python3
"""NV2 environment leaf E1 per system, from NV2's own E1 outputs (nv2_e1_sparc.json, nv2_e1_xcop.json, nv2_e1_lenses.json; FROZEN_CRITERIA + A1).
The same API as NV1's nv1_env.py (copied with attribution, E2-E4 removed), so NV1's sign test, fit and RQ3 loader run unchanged.
Missing = NaN = NOT COMPUTABLE, never imputed: Local Group dwarfs, IC 1613 (no SPARC alias), LITTLE THINGS without a SPARC alias, groups, MW, planets;
lens bins only when Step 0 passed and the KiDS photo-z fidelity control passed. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, re, sys
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
CRGI = os.path.join(RB, "CRG1_clean_room_regrade", "inputs")
CANDS = ("E1",); NAN = float("nan"); BIN_EDGES = (8.5, 10.3, 10.6, 10.8, 11.0)
def _j(n):
    p = os.path.join(HERE, n); return json.load(open(p)) if os.path.exists(p) else {}
_SP = _j("nv2_e1_sparc.json").get("E1", {}); _XC = _j("nv2_e1_xcop.json"); _LE = _j("nv2_e1_lenses.json"); _FI = _j("nv2_e1_fidelity.json")
KIDS_USABLE = bool(_FI.get("A_KiDS", {}).get("ok", False)); STEP0 = bool(_LE.get("step0", {}).get("passed", False)); TWOMPZ_USABLE = bool(_FI.get("B_2MPZ", {}).get("ok", False))
LENS_GRADED = KIDS_USABLE and STEP0
LENS_BINS = [b["E1_weighted"] for b in _LE.get("bins", [])] if LENS_GRADED else [NAN] * 4
def _sig_all():
    s = [v["sig"] for v in _SP.values()] + [v["sigma"] for k, v in _XC.items() if isinstance(v, dict) and v.get("computable") and TWOMPZ_USABLE]
    if LENS_GRADED: s += [b["sigma_median"] for b in _LE["bins"]]
    return float(np.median(s)) if s else NAN
SIG = dict(E1=_sig_all())

# ---------- naming helpers (NV1 / CX1, copied)
def norm(n): n = n.upper().replace(" ", ""); return re.sub(r"(?<=[A-Z])0+(?=\d)", "", n)
ALIAS = {norm(a): norm(b) for a, b in [("DDO 50", "UGC04305"), ("DDO 87", "UGC05918"), ("DDO 126", "UGC07559"), ("Haro 29", "UGCA281"),
                                        ("WLM", "UGCA444"), ("DDO 210", "Aquarius"), ("DDO 216", "Pegasus dIrr")]}
def sysid(n): k = norm(n); return ALIAS.get(k, k)
SPARC_NAMES = sorted(os.path.basename(f).replace("_rotmod.dat", "") for f in os.listdir(os.path.join(CRGI, "sparc", "rotmod")) if f.endswith("_rotmod.dat"))
def sparc_alias(name):
    sid = sysid(name); sp = [n for n in SPARC_NAMES if sysid(n) == sid]; return sp[0] if sp else None
X1 = {}
for _r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))):
    if _r["footing"] == "canonical": X1[_r["name"]] = _r

# ---------- per system kind
def sparc_E(n, c="E1"):
    v = _SP.get(n); return float(v["E1"]) if v and v.get("E1") is not None else NAN
def lt_E(n, c="E1"):
    sp = sparc_alias(n); return sparc_E(sp) if sp else NAN
def dwarf_E(name, host, lgMs, c="E1"): return NAN          # Local Group: no estimator (NV1)
def xcop_E(name, c="E1"):
    v = _XC.get(name)
    if not TWOMPZ_USABLE or not isinstance(v, dict) or not v.get("computable") or v.get("E1") is None: return NAN
    return float(v["E1"])
def group_E(lgMb, c="E1"): return NAN
def lens_bin_E(b): return LENS_BINS[b] if 0 <= b < 4 else NAN
def lgsys_E(c="E1"): return NAN
def sigma_E(c="E1"): return SIG["E1"]

# ---------- BF1 row indices -> names (NV1, copied)
def xcop_names():
    D = os.path.join(REPO, "real_research", "data", "xcop"); return sorted(x for x in os.listdir(D) if os.path.exists(os.path.join(D, x, f"{x}_mstar.fits")))
def sl1_lt_names():
    import pickle
    return [g["name"] for g in pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["lt"]]
def sl1_sparc_names():
    import pickle
    return sorted(g["name"] for g in pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["gals"])
def xcop_r500_map():
    from astropy.io import fits
    D = os.path.join(REPO, "real_research", "data", "xcop"); PCm = 3.0857e16; o = {}
    for n in xcop_names():
        with fits.open(os.path.join(D, n, f"{n}_hydro_mass.fits")) as h: o[n] = float(h[1].header["R500"]) * 1e3 * PCm
    return o
def rq3_table_build(c="E1"):
    T = dict(cand=c, disc={n: sparc_E(n) for n in SPARC_NAMES}, cluster_r500=[[r5, xcop_E(n), n] for n, r5 in xcop_r500_map().items()], MW=NAN, planet=NAN, group=None,
             lens="BINS" if LENS_GRADED else None, lens_bins=list(LENS_BINS), lens_edges=list(BIN_EDGES))
    lt = [r["name"] for r in csv.DictReader(open(os.path.join(CRGI, "little_things", "oh2015_table2.csv")))]; T["dwarf disc"] = {n: lt_E(n) for n in lt}
    T["dwarf"] = {r["name"]: NAN for r in X1.values()}
    return T

if __name__ == "__main__":
    T = rq3_table_build(); print("E1", {k: (sum(np.isfinite(v) for v in T[k].values()), len(T[k])) for k in ("disc", "dwarf disc", "dwarf")}, "X-COP", sum(np.isfinite(x[1]) for x in T["cluster_r500"]), "lens", T["lens"], "sigma_E", SIG)
