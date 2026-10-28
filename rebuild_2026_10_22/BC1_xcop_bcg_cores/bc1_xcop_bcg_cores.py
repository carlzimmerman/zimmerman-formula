#!/usr/bin/env python3
"""BC1_xcop_bcg_cores: X-COP cores with an explicit BCG (2MRS Ks light, Hernquist), graded with HO1(a)'s rule and machinery.
Frozen criteria 1180f5e8a4 (committed alone). Machinery: HO1's committed script (91cc5c3bd4) executed read-only up to its grade block.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I bc1_xcop_bcg_cores.py      (BC1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib, resource
import numpy as np
from astropy.io import fits

MUT = os.environ.get("BC1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
HO1 = os.path.join(REB, "HO1_xcop_hotgas_heldout", "ho1_heldout.py")
src = open(HO1).read(); src = src[:src.index("# ------------------------------------------------------------------ 6. grade per footing")]
src = src.replace('"ho1_heldout.out"', '"bc1_ho1_step0_STOPPED.out"').replace('"ho1_heldout_results.json"', '"bc1_ho1_step0_STOPPED.json"')
os.environ.pop("HO1_MUTATE", None)
NS = {"__file__": os.path.join(HERE, "ho1_ro.py"), "__name__": "ho1_ro"}
exec(compile(src, HO1, "exec"), NS)
P, XC, xcop_cl2, FEET = NS["P"], NS["XC"], NS["xcop_cl2"], NS["FEET"]
P("\n================ BC1_xcop_bcg_cores (criteria 1180f5e8a4)" + ("  [MUTATE: BCG subtracted in V-ADD]" if MUT else ""))
C_KMS, MPC_KPC = 299792.458, 1e3
DATA = os.path.join(REPO, "real_research", "data")
checks = {}

# 2MRS
T = []
for l in open(os.path.join(DATA, "2mrs_huchra2012.tsv")):
    if l.startswith("#") or not l.strip(): continue
    p = l.rstrip("\n").split("\t")
    try: T.append((float(p[0]), float(p[1]), float(p[2]), float(p[3])))
    except (ValueError, IndexError): continue
T = np.array(T)
def sep_deg(ra1, de1, ra2, de2):
    ra1, de1, ra2, de2 = map(np.radians, (ra1, de1, ra2, de2))
    c = np.sin(de1) * np.sin(de2) + np.cos(de1) * np.cos(de2) * np.cos(ra1 - ra2)
    return np.degrees(np.arccos(np.clip(c, -1, 1)))
def li(r, m, t):
    if t < r[0] or t > r[-1]: return np.nan
    return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))

BCG, STAR = {}, {}
for c in XC:
    nm = c["name"]; p_ = os.path.join(DATA, "xcop", nm)
    with fits.open(os.path.join(p_, f"{nm}_mstar.fits")) as h: st = h[2].data.copy(); hd = h[2].header
    with fits.open(os.path.join(p_, f"{nm}_hydro_mass.fits")) as h: r500 = float(h[1].header["R500"])
    z = float(hd["REDSHIFT"]); d = C_KMS * z / 70.0 * (1 + z / 2)                       # Mpc
    rad = sep_deg(hd["RA"], hd["DEC"], T[:, 0], T[:, 1]) * math.pi / 180 * d * MPC_KPC   # kpc (small angle)
    sel = (rad <= 0.1 * r500) & (np.abs(T[:, 2] - C_KMS * z) <= 1500)
    STAR[nm] = st
    if sel.any():
        j = np.where(sel)[0][np.argmin(T[sel, 3])]
        LK = 10 ** (-0.4 * (T[j, 3] - 5 * math.log10(d * 1e6) + 5 - 3.28))
        BCG[nm] = dict(Ktmag=float(T[j, 3]), offset_kpc=float(rad[j]), cz=float(T[j, 2]), Mstar=0.6 * LK, d_Mpc=d, r500_kpc=r500,
                       MSTAR_0p1_over_BCG=li(st["RADIUS"], st["MSTAR"], 0.1 * r500) / (0.6 * LK))
    else:
        BCG[nm] = None
P("  BCG matches (2MRS): " + "; ".join(f"{n}: " + (f"Ks {b['Ktmag']:.2f}, off {b['offset_kpc']:.0f} kpc, log M* {math.log10(b['Mstar']):.2f}, MSTAR(0.1R500)/M_BCG {b['MSTAR_0p1_over_BCG']:.2f}" if b else "none") for n, b in BCG.items()))
def hern(M, r, Re): a = Re / 1.8153; return M * r * r / (r + a) ** 2
checks["K1"] = all(abs(hern(b["Mstar"], 100 * 20.0, 20.0) / b["Mstar"] - 1) < 0.02 for b in BCG.values() if b)
ORIG = {c["name"]: list(c["rows"]) for c in XC}
k3 = True
def set_stars(mode, Re=20.0, fac=1.0):
    global k3
    for c in XC:
        nm = c["name"]; st = STAR[nm]; b = BCG[nm]; new = []
        for (x, r, mh, mb) in ORIG[nm]:
            ms0 = li(st["RADIUS"], st["MSTAR"], r); mg = mb - ms0
            if b is None or mode == "off": ms = ms0
            else:
                mbg = fac * hern(b["Mstar"], r, Re)
                if mode == "floor": ms = max(ms0, mbg)
                else: ms = ms0 + (-mbg if MUT else mbg)
            k3 &= ms >= ms0 - 1e-6 * ms0
            new.append((x, r, mh, mg + ms))
        c["rows"] = new
def run(lab, mode, Re=20.0, fac=1.0):
    set_stars(mode, Re, fac); out = {}
    for f in FEET:
        g = xcop_cl2(f); inner = [v for k, v in g["by_x"].items() if k in ("0.1", "0.2")]
        out[f] = dict(mean=g["mean"], rms=g["rms"], by_x=g["by_x"], inner_mean=float(np.mean(inner)), verdict=g["verdict"])
    P(f"  {lab:24s}: " + " | ".join(f"[{f}] mean {o['mean']:+.3f} rms {o['rms']:.3f} by_x {', '.join(f'{k}:{v:+.3f}' for k, v in o['by_x'].items())} -> {o['verdict']}" for f, o in out.items()))
    return out
RES = dict(criteria="1180f5e8a4", machinery="HO1 91cc5c3bd4 (read-only)", mutate=MUT, bcg=BCG, runs={})
R0 = run("STEP 0 (BCG off)", "off")
checks["K0"] = all(abs(R0[f]["mean"] - (-0.002)) < 0.0015 and abs(R0[f]["rms"] - 0.126) < 0.0015 for f in FEET)
P(f"  K0 reproduces HO1(a) (mean -0.002, rms 0.126): {'PASS' if checks['K0'] else 'FAIL'}")
RES["runs"]["step0"] = R0
base_inner = R0["canonical"]["inner_mean"]
for lab, mode, Re, fac in (("PRIMARY floor Re 20", "floor", 20, 1), ("V floor Re 10", "floor", 10, 1), ("V floor Re 40", "floor", 40, 1),
                           ("V-ADD Re 20", "add", 20, 1), ("V-ICL (ADD x2) Re 20", "add", 20, 2)):
    RES["runs"][lab] = run(lab, mode, Re, fac)
checks["K3"] = bool(k3)
def cls(o, f):
    if o[f]["verdict"] == "PASS": return "BCG FIXES THE X-COP SHAPE"
    if abs(o[f]["inner_mean"]) <= 0.05: return "BCG FIXES THE CORES ONLY"
    if abs(o[f]["inner_mean"]) <= 0.5 * abs(R0[f]["inner_mean"]): return "BCG HELPS"
    return "BCG DOES NOT HELP"
RES["verdict"] = {f: cls(RES["runs"]["PRIMARY floor Re 20"], f) for f in FEET}
RES["variant_classes"] = {k: {f: cls(v, f) for f in FEET} for k, v in RES["runs"].items() if k != "step0"}
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; checks["K2"] = peak < 1.0
RES["checks"] = checks
P(f"\n  K1 Hernquist total {'PASS' if checks['K1'] else 'FAIL'}; K3 stars never decrease {'PASS' if checks['K3'] else 'FAIL'}; K2 peak RSS {peak:.2f} GB")
P(f"  step-0 inner mean (x 0.1, 0.2): {base_inner:+.3f} canonical")
for k, v in RES["variant_classes"].items(): P(f"  {k:24s}: {v}")
P(f"=== VERDICT (PRIMARY): canonical {RES['verdict']['canonical']}; alt {RES['verdict']['alt']}")
fn = os.path.join(HERE, f"bc1_xcop_bcg_cores_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"bc1_xcop_bcg_cores{TAG}.out"), "w").write("\n".join(NS["OUT"]).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(checks.values()) else 1)
