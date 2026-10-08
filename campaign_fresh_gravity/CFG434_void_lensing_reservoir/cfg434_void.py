#!/usr/bin/env python3
"""CFG434: void lensing (UNIONS x BOSS, arXiv 2507.13450v2 Table tab:fit_stats) vs a smooth
unsettled reservoir. Rule: FROZEN_CRITERIA.md (committed alone first, 7caa5042c).

A = b_ref / b_Vg. Reading I: A = (1 + eps*b_u)/R_sel. Reading II: A = (1 - eps*(1-b_u))/R_sel.
eps = f_u * 5.364/6.364, f_u in [0.65, 0.90]; R_sel in [1.00, 1.25]. b_u free in [0, 1].
Run: python3 cfg434_void.py [--mutate]   (seconds; numpy only)
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""

# ---- published inputs (2507.13450v2 Table tab:fit_stats; Sect. 2 text) ---------------------
CATS = {  # name: (b_Vg, sigma, mean z, mean R_V [Mpc/h])
    "Full": (2.47, 0.36, 0.467, 40.3),
    "LOWZ": (2.49, 0.49, 0.331, 40.3),
    "CMASS": (2.48, 0.55, 0.530, 40.3),
    "Small": (2.82, 0.60, 0.466, 33.7),
    "Large": (2.77, 0.57, 0.469, 57.9),
}
OM, H = 0.307, 0.6777          # paper fiducial
BETA = 0.37                    # reconstruction beta = f/b, matched to the fiducial cosmology
RATIO_L, RATIO_L_ERR = 1.36, 0.27   # paper: b_Vg / b_g(Sugiyama+22), Full
BREF_FRAC = 0.05               # declared uncertainty on b_ref

# ---- frozen brackets -------------------------------------------------------------------------
OC_OM = 5.364 / 6.364
FU = (0.65, 0.90)
EPS = (FU[0] * OC_OM, FU[1] * OC_OM)
RSEL = (1.00, 1.25)
NG = 21
EPS_G = np.linspace(*EPS, NG)
RSEL_G = np.linspace(*RSEL, NG)


def f_growth(z, om=OM):
    omz = om * (1 + z) ** 3 / (om * (1 + z) ** 3 + 1 - om)
    return omz ** 0.55


def a_obs(bvg, sig, bref):
    A = bref / bvg
    u, su = 1 / bvg, sig / bvg ** 2
    return A, A * np.hypot(su / u, BREF_FRAC)


GAUSS_B = None   # set to (b_obs, sigma_b, b_ref) for the Gaussian-in-b_Vg robustness row


def zfun(A, sA, Ap):
    if GAUSS_B is None:
        return (A - Ap) / sA
    b, sb, br = GAUSS_B
    return (b - br / Ap) / np.hypot(sb, BREF_FRAC * b) * -1.0


def pred(reading, bu, eps, rsel):
    if reading == "I":
        return (1 + eps * bu) / rsel
    if reading == "II":
        return (1 - eps * (1 - bu)) / rsel
    return 1.0 / rsel  # LCDM


def score(A, sA, reading, bu, rsel_g=RSEL_G):
    zs = np.array([[zfun(A, sA, pred(reading, bu, e, r)) for r in rsel_g] for e in EPS_G])
    i, j = np.unravel_index(np.argmin(np.abs(zs)), zs.shape)
    zmin = float(zs[i, j])
    v = "CONSISTENT" if abs(zmin) <= 2 else ("DISFAVOURED" if abs(zmin) <= 3 else "EXCLUDED")
    corners = {f"eps{e:.3f}_R{r:.2f}": float(zfun(A, sA, pred(reading, bu, e, r)))
               for e in EPS for r in (rsel_g[0], rsel_g[-1])}
    return dict(z_min=zmin, at_eps=float(EPS_G[i]), at_rsel=float(rsel_g[j]), verdict=v, corners=corners)


def bu_bound(A, sA, reading, rsel_g=RSEL_G):
    """Allowed b_u (|z|<=1.96) at the most lenient and most stringent corner (by allowed width)."""
    bus = np.linspace(0, 1, 1001)
    out = {}
    for e in EPS:
        for r in (rsel_g[0], rsel_g[-1]):
            ok = bus[np.abs((A - pred(reading, bus, e, r)) / sA) <= 1.96]
            out[f"eps{e:.3f}_R{r:.2f}"] = [float(ok.min()), float(ok.max())] if ok.size else None
    widths = {k: (v[1] - v[0]) if v else -1 for k, v in out.items()}
    return dict(corners=out, most_lenient=max(widths, key=widths.get), most_stringent=min(widths, key=widths.get))


lines = [f"CFG434 void lensing vs the unsettled reservoir   MUTATE={MUT}", ""]
res = dict(mutate=MUT, eps=EPS, rsel=RSEL, cats={})
checks = {}

# ---- references -------------------------------------------------------------------------------
bref_C = {k: f_growth(v[2]) / BETA for k, v in CATS.items()}
bref_L = CATS["Full"][0] / RATIO_L
lines.append(f"eps = f_u*5.364/6.364 in [{EPS[0]:.3f}, {EPS[1]:.3f}];  R_sel in {RSEL}")
lines.append(f"REF-C b_ref (f(z)/0.37): " + "  ".join(f"{k} {v:.3f}" for k, v in bref_C.items()))
lines.append(f"REF-L b_ref (Full, b_Vg/1.36) = {bref_L:.3f}")
for k, v in CATS.items():
    lines.append(f"  {k}: R_V {v[3]:.1f} Mpc/h = {v[3]/H:.1f} Mpc; Delta Sigma reaches 3 R_V = {3*v[3]/H:.0f} Mpc")
checks["C1_bref"] = bool(1.9 <= bref_C["Full"] <= 2.1)
checks["C2_refs_agree"] = bool(abs(bref_C["Full"] / bref_L - 1) <= 0.15)
c3 = all(abs(pred("I", b, 1e-15, r) - 1 / r) < 1e-12 and abs(pred("II", b, 1e-15, r) - 1 / r) < 1e-12
         and abs(pred("II", 1.0, e, r) - 1 / r) < 1e-12 for b in (0, .5, 1) for r in RSEL for e in EPS)
checks["C3_limits"] = bool(c3)

# ---- primary ----------------------------------------------------------------------------------
bvg, sig, z, rv = CATS["Full"]
A, sA = a_obs(bvg, sig, bref_C["Full"])
if MUT:
    A = (1 - 0.654) / 1.125
    lines.append(f"\n*** MUTATE: A_obs replaced by the planted reading-II SMOOTH value {A:.3f} (sigma kept {sA:.3f}) ***")
lines.append(f"\nPRIMARY (Full, REF-C): A_obs = {A:.3f} +- {sA:.3f}")
pow_gap = EPS[0] / RSEL[1]
checks["C_POW"] = bool(pow_gap >= 2 * sA)
lines.append(f"C-POW: smooth-vs-clumpy gap at least favourable corner = {pow_gap:.3f} vs 2 sigma_A = {2*sA:.3f} -> {'PASS' if checks['C_POW'] else 'FAIL'}")

prim = {}
for rd in ("I", "II"):
    for bu, lab in ((0.0, "SMOOTH"), (1.0, "CLUMPY")):
        s = score(A, sA, rd, bu)
        prim[f"{rd}_{lab}"] = s
        lines.append(f"  reading {rd:2s} {lab:6s}: min|z| = {s['z_min']:+.2f} at eps {s['at_eps']:.3f}, R_sel {s['at_rsel']:.2f} -> {s['verdict']}"
                     f"   corners " + " ".join(f"{v:+.2f}" for v in s['corners'].values()))
    bb = bu_bound(A, sA, rd)
    prim[f"{rd}_bound"] = bb
    lines.append(f"  reading {rd} b_u allowed (|z|<=1.96): most lenient {bb['most_lenient']} {bb['corners'][bb['most_lenient']]}; "
                 f"most stringent {bb['most_stringent']} {bb['corners'][bb['most_stringent']]}")
lcdm = score(A, sA, "LCDM", 0.0)
prim["LCDM"] = lcdm
lines.append(f"  C4 LCDM (A = 1/R_sel): min|z| = {lcdm['z_min']:+.2f} -> {lcdm['verdict']}")
checks["C4_LCDM_reported"] = True

vI, vII = prim["I_SMOOTH"]["verdict"], prim["II_SMOOTH"]["verdict"]
if not checks["C_POW"]:
    head = "NON-DIAGNOSTIC (power check failed)"
elif (vI == "CONSISTENT") != (vII == "CONSISTENT") and "EXCLUDED" in (vI, vII):
    head = f"BOOKKEEPING FORK: SMOOTH RESERVOIR {vI} under reading I, {vII} under reading II"
else:
    head = f"SMOOTH RESERVOIR {vI} under reading I / {vII} under reading II"
lines.append(f"\nHEADLINE: {head}")
res["primary"] = dict(A=A, sA=sA, scores=prim, headline=head)

# ---- robustness (never decisive) ---------------------------------------------------------------
lines.append("\nROBUSTNESS (reported, not decisive): SMOOTH min|z| reading I / reading II")
rob = {}
def rob_row(lab, A_, sA_, rsel_g=RSEL_G):
    sI, sII = score(A_, sA_, "I", 0.0, rsel_g), score(A_, sA_, "II", 0.0, rsel_g)
    rob[lab] = dict(A=A_, sA=sA_, I=sI, II=sII)
    lines.append(f"  {lab:28s} A = {A_:.3f} +- {sA_:.3f}:  I {sI['z_min']:+.2f} {sI['verdict']:11s} II {sII['z_min']:+.2f} {sII['verdict']}")
if not MUT:
    for k, (b_, s_, z_, r_) in CATS.items():
        if k != "Full":
            rob_row(f"{k} REF-C", *a_obs(b_, s_, bref_C[k]))
    rob_row("Full REF-L (scale-dependence)", *a_obs(bvg, sig, bref_L))
    GAUSS_B = (bvg, sig, bref_C["Full"])
    rob_row("Full REF-C Gaussian in b_Vg", A, sA)
    GAUSS_B = None
    rob_row("Full REF-C R_sel = 1 only", A, sA, rsel_g=np.array([1.0]))
    lines.append("  DES Y1 (Fang+2019): b_slope around voids slightly ABOVE the large-scale bias (<2 sigma) -> A < 1, same direction (qualitative)")
res["robustness"] = rob
res["checks"] = checks

lines.append("\nchecks: " + json.dumps(checks))
ok = all(v for k, v in checks.items())
if MUT:
    det = (prim["II_SMOOTH"]["verdict"] == "CONSISTENT" and prim["I_SMOOTH"]["verdict"] in ("DISFAVOURED", "EXCLUDED"))
    lines.append(f"MUTATE detected (II smooth -> CONSISTENT and I smooth -> DISFAVOURED/EXCLUDED): {det}")
    res["mutate_detected"] = bool(det)
print("\n".join(lines))
with open(os.path.join(HERE, f"cfg434_results{TAG}.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
if MUT:
    sys.exit(1 if res["mutate_detected"] else 0)
sys.exit(0 if ok else 1)
