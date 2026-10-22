#!/usr/bin/env python3
"""D7c_q2_rar_gate -- does any law form in the record's family pass BOTH Cassini Q2 and SPARC's RAR shape?

UNSCREENED law forms only (point-mass Sun + uniform external field; no L* screening -- that is lane D7d_screened_q2).
Q2: D7b's validated Route-M solver, exec'd read-only from D7b_cassini_Q2/d7b_cassini_q2.py (definitions only).
SPARC: AG4b's per-galaxy MAP-Upsilon pipeline and paired bootstrap z, reproduced verbatim (K2 checks it against
AG4b's committed results).  Criteria: FROZEN_CRITERIA.md (commit e9e5349368).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 d7c_q2_rar_gate.py [--mutate]
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import json
import math
import os
import sys

os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from scipy.optimize import brentq

MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT_TXT = os.path.join(HERE, f"d7c_q2_rar_gate{TAG}.out")
OUT_JSON = os.path.join(HERE, f"d7c_q2_rar_gate_results{TAG}.json")
LINES = []


def say(s=""):
    print(s)
    LINES.append(s)


CHECKS = []


def check(name, ok, value, thr):
    CHECKS.append(bool(ok))
    say(f"{name} {'PASS' if ok else 'FAIL'} {value} {thr}")


# ------------------------------------------------------------------ D7b solver (definitions only, read-only)
D7B = os.path.join(REPO, "doors_push_2026_10_22", "D7b_cassini_Q2", "d7b_cassini_q2.py")
src = open(D7B).read().split("# ================================================================== run")[0]
_argv = sys.argv
sys.argv = [D7B]
NS = {"__file__": D7B, "__name__": "d7b_defs"}
exec(compile(src, D7B, "exec"), NS)
sys.argv = _argv
q_route_m, Q2_from_q, gNe_from_total = NS["q_route_m"], NS["Q2_from_q"], NS["gNe_from_total"]
A0Q = NS["A0"]                       # Q2 footings (D7b): 9.36e-11 / 1.13e-10
GNE_A60, GE_KIN = NS["GNE_A60"], NS["GE_KIN"]
HEES, PARK = NS["HEES"], NS["PARK"]
H_LO, H_HI = HEES[0] - 2 * HEES[1], HEES[0] + 2 * HEES[1]     # -3e-27, 9e-27
P_LO, P_HI = PARK[0] - 2 * PARK[1], PARK[0] + 2 * PARK[1]     # -2e-27, 5.2e-27

# ------------------------------------------------------------------ record loader + kernels (CFG4, read-only)
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG4_common as C  # noqa: E402

A0S = {f: C.A0[f] for f in C.FOOTS}  # SPARC footings (CFG4): 9.3603e-11 / 1.1312e-10


def _y(y):
    return np.maximum(np.asarray(y, float), 1e-300)


def nu_L(y):
    y = _y(y)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))


def nu_Q(y):
    y = _y(y)
    return np.sqrt(1.0 + 1.0 / y)


def nu_S(y):          # standard mu = x/sqrt(1+x^2) inverted
    y = _y(y)
    return np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y ** 2)))


def nu_R(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


nu_M = C.nu_mono


def nu_cap(n):
    def f(y):
        y = _y(y)
        return 1.0 + 2.0 / (y * (np.sqrt(n * n + 4.0 / y) + n))   # = 1 + (sqrt(n^2+4/y)-n)/2, stable
    return f


def nu_bet(b):
    return lambda y: C.nu_beta(y, b)


def w_of(nu):
    return lambda y: nu(y) - 1.0


NAMED = {"L": nu_L, "Q": nu_Q, "M": nu_M, "S": nu_S, "R": nu_R}
NAMED_DESC = {"L": "n=1 canonical g_N=g^2/(g+a0)", "Q": "n=2 = quadrature P2 = alpha=1",
              "M": "nu_mono (CFG4/FP1 splice)", "S": "standard mu (alpha=2)", "R": "nu_RAR (reference shape, not a framework law)"}
N_GRID = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0]
B_GRID = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
LAWS = dict(NAMED)
for n in N_GRID:
    LAWS[f"n={n:g}"] = nu_cap(n)
for b in B_GRID:
    LAWS[f"beta={b:g}"] = nu_bet(b)
EL = ("E0", "E1", "E2", "E3")
RES = {"lane": "D7c_q2_rar_gate", "mutate": MUTATE, "scope": "UNSCREENED law forms (screened case: D7d_screened_q2)",
       "inputs": {"a0_Q2": A0Q, "a0_SPARC": A0S, "gNe_A60": GNE_A60, "ge_kinematic_total": GE_KIN,
                  "Hees2014": HEES, "Park2026": PARK, "Hees_2sigma": [H_LO, H_HI], "Park_2sigma": [P_LO, P_HI],
                  "n_grid": N_GRID, "beta_grid": B_GRID}}

say("=" * 100)
say("D7c_q2_rar_gate -- UNSCREENED law family vs Cassini Q2 and SPARC RAR shape" + (" [MUTATE: /sqrtD bug]" if MUTATE else ""))
say("=" * 100)


# ------------------------------------------------------------------ Q2
def Q2_law(nu, foot, elab, split=1.0):
    a0 = A0Q[foot]
    w = w_of(nu)
    if elab == "E0":
        gNe = GNE_A60
    else:
        gNe = gNe_from_total(GE_KIN[elab], a0, w)
    eN = gNe / a0
    return Q2_from_q(q_route_m(w, eN, split=split, sqrtD_bug=MUTATE), a0), gNe


def vd(vals, lo, hi):
    ins = [lo <= v <= hi for v in vals]
    return "PASS" if all(ins) else ("FAIL" if not any(ins) else "E-DEPENDENT")


Q2 = {}
for name, nu in LAWS.items():
    Q2[name] = {}
    for foot in A0Q:
        row = {e: Q2_law(nu, foot, e) for e in EL}
        vals = [row[e][0] for e in EL]
        Q2[name][foot] = {"Q2": dict(zip(EL, vals)), "gNe": {e: row[e][1] for e in EL},
                          "Hees": vd(vals, H_LO, H_HI), "Park": vd(vals, P_LO, P_HI),
                          "min_over_Hees_upper": min(vals) / H_HI, "max_over_Hees_upper": max(vals) / H_HI,
                          "sigma_Hees_min": (min(vals) - HEES[0]) / HEES[1],
                          "sigma_Hees_max": (max(vals) - HEES[0]) / HEES[1]}
RES["Q2"] = Q2

# ------------------------------------------------------------------ K1, K6, K5
d7b = json.load(open(os.path.join(REPO, "doors_push_2026_10_22", "D7b_cassini_Q2", "d7b_cassini_q2_results.json")))
k1 = max(abs(Q2["L"][f]["Q2"][e] / d7b["grid"][f]["none"][e]["Q2_M"] - 1) for f in A0Q for e in EL)
check("K1", k1 < 1e-6, f"max_rel_vs_D7b={k1:.2e} (L, no turn-off, 2 footings x E0-E3)", "<1e-6")
qa = -(16.0 / 49.0) * math.sqrt(2.0)
qn = q_route_m(lambda y: 1.0 / np.maximum(np.asarray(y, float), 1e-300), 2.0, sqrtD_bug=MUTATE)
check("K6", abs(qn / qa - 1) < 1e-3, f"q/q_exact-1={qn/qa-1:.2e} (nu-1=1/y, eN=2)", "<1e-3")
k5 = {}
for name in ("M", "S", "R", "n=8", "beta=6"):
    a = Q2_law(LAWS[name], "canonical", "E2", split=1.0)[0]
    b = Q2_law(LAWS[name], "canonical", "E2", split=2.0)[0]
    k5[name] = abs(b / a - 1)
RES["K5_split_rel"] = k5
check("K5", max(k5.values()) < 5e-3, "split1_vs_2 max_rel=" + f"{max(k5.values()):.1e}", "<5e-3")

# ------------------------------------------------------------------ K3, K4 identities
yy = np.logspace(-6, 4, 2001)
x = nu_Q(yy) * yy
mu_a1 = 2 * x / (np.sqrt(1 + 4 * x ** 2) + 1)          # = (sqrt(1+4x^2)-1)/(2x), stable form (first run: cancellation 6e-11)
k3 = max(np.max(np.abs(nu_cap(1.0)(yy) / nu_L(yy) - 1)), np.max(np.abs(nu_cap(2.0)(yy) / nu_Q(yy) - 1)),
         np.max(np.abs(nu_bet(1.0)(yy) / nu_Q(yy) - 1)), np.max(np.abs(mu_a1 * x / yy - 1)))
check("K3", k3 < 1e-12, f"max_rel={k3:.1e} (cap n1=L, n2=Q, beta1=Q, Q=inverse alpha1 mu)", "<1e-12")
A25 = dict(Y_P=2.5396382826332706, H_P=0.647610237891915, DELTA=0.05, Y_STAR=2.3374124053)
H_STAR = A25["Y_STAR"] / math.expm1(math.sqrt(A25["Y_STAR"]))
y4 = np.logspace(-4, 4, 4001)
hR = y4 / np.expm1(np.sqrt(np.minimum(y4, 1e4)))
hM = np.where(y4 <= A25["Y_STAR"], hR, H_STAR + A25["DELTA"] * A25["H_P"] * np.log((y4 + A25["Y_P"]) / (A25["Y_STAR"] + A25["Y_P"])))
k4 = float(np.max(np.abs(nu_M(y4) / (1 + hM / y4) - 1)))
RES["K4_numono_rel"] = k4
check("K4", k4 < 1e-10, f"max_rel CFG4 nu_mono vs A25 splice={k4:.2e}", "<1e-10")

# ------------------------------------------------------------------ SPARC: AG4b pipeline (verbatim)
LN10 = math.log(10.0)
KPC_S = 3.0857e19
LU0, SIG_U, S0 = math.log10(0.5), 0.10, 0.05
LU = LU0 + np.linspace(-0.5, 0.5, 201)
UG = 10 ** LU
GAL = C.load_sparc()
D_ = []
for g in GAL:
    R, Vo, eV, Vg, Vd, Vb = (np.asarray(g[k], float) for k in ("R", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"))
    Rm = R * KPC_S
    gb_lo = (np.sign(Vg) * Vg ** 2 + UG[0] * Vd ** 2 + 1.4 * UG[0] * Vb ** 2) * 1e6 / Rm
    gb_hi = (np.sign(Vg) * Vg ** 2 + UG[-1] * Vd ** 2 + 1.4 * UG[-1] * Vb ** 2) * 1e6 / Rm
    go = (Vo * 1e3) ** 2 / Rm
    m = (Vo > 0) & (go > 0) & (gb_lo > 0) & (gb_hi > 0) & np.isfinite(go) & (R > 0)
    if m.sum() < 5:
        continue
    gas = np.sign(Vg[m]) * Vg[m] ** 2 * 1e6 / Rm[m]
    star = (Vd[m] ** 2 + 1.4 * Vb[m] ** 2) * 1e6 / Rm[m]
    sv = 2.0 / LN10 * np.clip(eV[m], 1, None) / np.clip(Vo[m], 1, None)
    D_.append(dict(name=g["name"], go=go[m], gas=gas, star=star, sv=sv))


def fit_all(nu, a0):
    rms, chi = [], []
    for d in D_:
        gb = d["gas"][:, None] + d["star"][:, None] * UG[None, :]
        r = np.log10(d["go"])[:, None] - np.log10(nu(gb / a0) * gb)
        s2 = d["sv"][:, None] ** 2 + S0 ** 2
        c2 = (r ** 2 / s2).sum(0) + ((LU - LU0) / SIG_U) ** 2
        i = int(np.argmin(c2))
        rms.append(math.sqrt(np.mean((r[:, i] / 2) ** 2)))
        chi.append(float(c2[i]))
    return np.array(rms), np.array(chi)


def paired_z(d1, d2):          # AG4b: d = d2 - d1; z = -median/sigma (z > 0: law 2 better)
    d = d2 - d1
    d = d[np.isfinite(d)]
    n = len(d)
    rng = np.random.default_rng(20261020)
    idx = rng.integers(0, n, (10000, n))
    med = float(np.median(d))
    sd = float(np.std(np.median(d[idx], axis=1)))
    return med, sd, (-med / sd if sd > 0 else 0.0)


def chi_z(c1, c2):
    dc = c2 - c1
    return float(dc.sum()), (float(-dc.sum() / (np.std(dc) * math.sqrt(len(dc)))) if np.std(dc) > 0 else 0.0)


say(f"SPARC: {len(GAL)} rotmod files, {len(D_)} galaxies with >= 5 usable points (AG4b pipeline)")
FIT = {f: {k: fit_all(nu, A0S[f]) for k, nu in LAWS.items()} for f in C.FOOTS}

ag4b = json.load(open(os.path.join(REPO, "argon_push", "AG4b_sparc_population_upsilon", "ag4b_results.json")))
k2 = []
for f in C.FOOTS:
    D, sD, z = paired_z(FIT[f]["L"][0], FIT[f]["Q"][0])
    s1, _ = chi_z(FIT[f]["L"][1], FIT[f]["Q"][1])
    p = ag4b["footings"][f]["primary"]
    k2.append((abs(D - p["D"]), abs(z - p["z"]), abs(s1 - p["sum_dchi2"])))
ok2 = all(a <= 1e-4 and b <= 0.02 and c <= 0.5 for a, b, c in k2)
check("K2", ok2, "AG4b reproduced |dD|,|dz|,|dS1| = " + "; ".join(f"{a:.1e},{b:.2e},{c:.2f}" for a, b, c in k2),
      "<=1e-4, <=0.02, <=0.5")

SP = {}
for f in C.FOOTS:
    SP[f] = {}
    for k in LAWS:
        zs, cs = {}, {}
        for y_ in NAMED:
            if y_ == k:
                continue
            D, sD, z = paired_z(FIT[f][y_][0], FIT[f][k][0])     # z > 0: law k better than comparator y_
            s1, zc = chi_z(FIT[f][y_][1], FIT[f][k][1])
            zs[y_] = {"D": D, "sD": sD, "z": z}
            cs[y_] = {"sum_dchi2": s1, "z": zc}
        worst = min(zs, key=lambda q: zs[q]["z"])
        worst_c = min(cs, key=lambda q: cs[q]["z"])
        SP[f][k] = {"median_rms": float(np.median(FIT[f][k][0])), "sum_chi2": float(FIT[f][k][1].sum()),
                    "vs": zs, "vs_S1": cs, "worst_comparator": worst, "worst_z": zs[worst]["z"],
                    "worst_S1_comparator": worst_c, "worst_S1_z": cs[worst_c]["z"],
                    "SPARC": "PASS" if zs[worst]["z"] > -2 else "FAIL",
                    "S1_reading": "PASS" if cs[worst_c]["z"] > -2 else "FAIL"}
RES["SPARC"] = SP

# ------------------------------------------------------------------ table
say("")
say("Per law: Q2 [s^-2] at E0,E1,E2,E3 (canonical | alt) -> Hees verdict; SPARC worst paired z (comparator) per footing")
JOINT = {}
for k in LAWS:
    qc, qa_ = Q2[k]["canonical"], Q2[k]["alt"]
    sc, sa = SP["canonical"][k], SP["alt"][k]
    qpass = qc["Hees"] == "PASS" and qa_["Hees"] == "PASS"
    spass = sc["SPARC"] == "PASS" and sa["SPARC"] == "PASS"
    s1ag = sc["S1_reading"] == sc["SPARC"] and sa["S1_reading"] == sa["SPARC"]
    JOINT[k] = {"Q2_both": qpass, "SPARC_both": spass, "both": qpass and spass, "S1_agrees": s1ag}
    say(f"  {k:9s} Q2c=" + ",".join(f"{qc['Q2'][e]:.2e}" for e in EL) + f" [{qc['Hees']}]"
        + f" Q2a x[{qa_['min_over_Hees_upper']:.2f},{qa_['max_over_Hees_upper']:.2f}] [{qa_['Hees']}]"
        + f" Park {qc['Park']}/{qa_['Park']}"
        + f" | SPARC c z={sc['worst_z']:+.2f}({sc['worst_comparator']}) {sc['SPARC']}"
        + f" a z={sa['worst_z']:+.2f}({sa['worst_comparator']}) {sa['SPARC']}"
        + f" | S1 z c {sc['worst_S1_z']:+.2f} a {sa['worst_S1_z']:+.2f}"
        + f" | rms_med {sc['median_rms']:.4f}/{sa['median_rms']:.4f}  BOTH={'YES' if qpass and spass else 'no'}")
RES["joint"] = JOINT

# ------------------------------------------------------------------ outcome
passers = [k for k in LAWS if JOINT[k]["both"]]
fam = {}
for famname, keys in (("capacity_n", [f"n={n:g}" for n in N_GRID]), ("beta", [f"beta={b:g}" for b in B_GRID]),
                      ("named", list(NAMED))):
    qok = [k for k in keys if JOINT[k]["Q2_both"]]
    sok = [k for k in keys if JOINT[k]["SPARC_both"]]
    # (i) Hees sigma of SPARC-passing members at their most favourable E and footing
    sig_s = {k: min(Q2[k][f]["sigma_Hees_min"] for f in A0Q) for k in sok}
    # (ii) worst SPARC z of Q2-passing members (worst footing)
    z_q = {k: min(SP[f][k]["worst_z"] for f in C.FOOTS) for k in qok}
    # AMENDMENT A1 (post-result): a PASS needs every cell, so a member's Q2 miss is its WORST cell
    sig_w = {k: max(Q2[k][f]["sigma_Hees_max"] for f in A0Q) for k in sok}
    best_w = min(sig_w, key=sig_w.get) if sig_w else None
    best_s = min(sig_s, key=sig_s.get) if sig_s else None
    best_q = max(z_q, key=z_q.get) if z_q else None
    fam[famname] = {"Q2_pass_members": qok, "SPARC_pass_members": sok,
                    "SPARC_passers_min_Hees_sigma": sig_s, "Q2_passers_worst_SPARC_z": z_q,
                    "least_tense_SPARC_passer": best_s, "its_Hees_sigma": sig_s.get(best_s),
                    "SPARC_passers_worst_cell_Hees_sigma": sig_w, "least_tense_SPARC_passer_worstcell": best_w,
                    "its_worstcell_Hees_sigma": sig_w.get(best_w),
                    "least_tense_Q2_passer": best_q, "its_SPARC_z": z_q.get(best_q),
                    "edge_touch": bool(qok and keys[-1] in qok and not sok) or bool(sok and keys[0] in sok and not qok)}
RES["families"] = fam
say("")
for k, v in fam.items():
    say(f"  family {k}: Q2-pass {v['Q2_pass_members']}; SPARC-pass {v['SPARC_pass_members']}")
    if v["least_tense_SPARC_passer"]:
        say(f"     least-tense SPARC passer {v['least_tense_SPARC_passer']}: Q2 at {v['its_Hees_sigma']:+.2f} sigma_Hees (most favourable E, footing)")
    if v["least_tense_SPARC_passer_worstcell"]:
        say(f"     [A1] least-tense SPARC passer by worst cell {v['least_tense_SPARC_passer_worstcell']}: "
            f"Q2 at {v['its_worstcell_Hees_sigma']:+.2f} sigma_Hees (worst E, footing)")
    if v["least_tense_Q2_passer"]:
        say(f"     least-tense Q2 passer {v['least_tense_Q2_passer']}: SPARC worst z {v['its_SPARC_z']:+.2f}")
undec = [k for k in passers if not JOINT[k]["S1_agrees"]]
if passers and not undec:
    outcome = "A LAW PASSES BOTH: " + ", ".join(passers)
elif passers:
    outcome = "UNDECIDED: passers " + ", ".join(passers) + " but S1 contradicts the primary for " + ", ".join(undec)
else:
    tens = []
    for v in fam.values():
        cand = [abs(v["its_SPARC_z"]) if v["its_SPARC_z"] is not None else None,
                v["its_worstcell_Hees_sigma"] if v["its_worstcell_Hees_sigma"] is not None else None]   # A1
        cand = [c for c in cand if c is not None]
        if cand:
            tens.append(min(cand))
    N = min(tens) if tens else float("nan")
    outcome = f"NO LAW PASSES BOTH: the unscreened law family and Cassini are in tension at >= {N:.1f} sigma"
# AMENDMENT A1 (post-result, diagnostic): the beta family's one failing cell (alt footing, E0) beyond the frozen grid
bx = {}
for b in (4.0, 6.0, 10.0, 20.0, 40.0):
    bx[f"beta={b:g}"] = {"alt_E0": Q2_law(nu_bet(b), "alt", "E0")[0], "canonical_E0": Q2_law(nu_bet(b), "canonical", "E0")[0]}
RES["A1_beta_alt_E0_extension"] = bx
say("  [A1] beta family, alt footing E0 (beyond grid): " + "; ".join(f"{k} {v['alt_E0']:.3e} ({v['alt_E0']/H_HI:.3f}x)" for k, v in bx.items()))

# AMENDMENT A1 (post-result): footing-split reading (reported; the frozen outcome above needs both footings)
split = {}
for f in A0Q:
    fs = "canonical" if f == "canonical" else "alt"
    split[f] = [k for k in LAWS if Q2[k][f]["Hees"] == "PASS" and SP[fs][k]["SPARC"] == "PASS"]
    split[f + "_S1_also_pass"] = [k for k in split[f] if SP[fs][k]["S1_reading"] == "PASS"]
RES["A1_footing_split_passers"] = split
RES["outcome"] = outcome
say("")
say("OUTCOME: " + outcome)
for f in A0Q:
    say(f"  [A1] {f} footing alone: Q2(Hees, all E) AND SPARC primary pass: {split[f]}; of these S1 also passes: {split[f + '_S1_also_pass']}")

# ------------------------------------------------------------------ external-field dependence (canonical law L)
grid = np.logspace(math.log10(0.05), math.log10(30.0), 121)
efd = {}
for foot, a0 in A0Q.items():
    wL = w_of(nu_L)

    def Qge(r):
        ge = r * 9.36e-11
        return Q2_from_q(q_route_m(wL, gNe_from_total(ge, a0, wL) / a0, sqrtD_bug=MUTATE), a0)
    vals = np.array([Qge(r) for r in grid])
    out = {}
    for lab, B in (("Hees", H_HI), ("Park", P_HI)):
        edges = []
        s = vals - B
        for i in range(len(grid) - 1):
            if s[i] * s[i + 1] < 0:
                edges.append(brentq(lambda r: Qge(r) - B, grid[i], grid[i + 1], xtol=1e-6) * 9.36e-11)
        out[lab] = {"crossings_ge_total": edges, "pass_at_low_end": bool(s[0] <= 0), "pass_at_high_end": bool(s[-1] <= 0)}
    imax = int(np.argmax(vals))
    out["Q2_max_on_grid"] = float(vals[imax])
    out["ge_at_grid_max"] = float(grid[imax] * 9.36e-11)
    efd[foot] = out
    say(f"  E-field (L, {foot}): Q2 max on grid {vals[imax]:.2e} at g_e (grid top; Q2 grows ~sqrt(g_e))={grid[imax]*9.36e-11:.2e}; "
        f"Hees crossings g_e={['%.3e' % e for e in out['Hees']['crossings_ge_total']]}; "
        f"Park crossings g_e={['%.3e' % e for e in out['Park']['crossings_ge_total']]}")
RES["efield_dependence_L"] = efd
RES["efield_grid_over_9.36e-11"] = [float(grid[0]), float(grid[-1]), len(grid)]

npass = sum(CHECKS)
say("")
say(f"D7C_Q2_RAR_GATE COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
RES["checks_pass"] = npass
RES["checks_total"] = len(CHECKS)
open(OUT_TXT, "w").write("\n".join(LINES) + "\n")
json.dump(RES, open(OUT_JSON, "w"), indent=1, default=float)
sys.exit(0 if npass == len(CHECKS) else 1)
