"""CFG773 -- can the tether's field law (AQUAL, simple mu) be built on a bench?

Criteria: FROZEN_CRITERIA.md (committed alone first, 276866312).
A1 electric no-go (Kramers-Kronig); A2 magnetic-pole mapping; A3 superconducting-grain composite exact design (Maxwell-Garnett,
Bruggeman) + Monte-Carlo; A4 seven real superconductors (NNLS engineering fit); A5 analogue 'rotation curve'.
Run: python3 cfg773.py   (CFG773_MUTATE=1 for the teeth).  Seconds-minutes, < 200 MB.
"""
import json
import math
import os
import sys

import numpy as np
from scipy import integrate, optimize

MUT = os.environ.get("CFG773_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"cfg773{SUF}.out"), "w")
RNG = np.random.default_rng(773)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUTF.write(s + "\n")


RES = {"lane": "CFG773", "mutate": MUT, "checks": {}, "numbers": {}}
FAILS = []


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


mu_law = lambda x: x / (1 + x)
P("CFG773  bench analogue of the tether's field law" + ("  [MUTATE]" if MUT else ""))

# ======================================================== A1 electric no-go
P("\nA1  passive Drude-Lorentz media: eps(0) = 1 + sum f_j wp_j^2 / w_j^2; KK check eps(0)-1 = (2/pi) int eps''/w dw")
n_viol, kk_err = 0, 0.0
for i in range(10000):
    nj = RNG.integers(1, 5)
    fj, wj, gj = RNG.uniform(0, 3, nj), RNG.uniform(0.1, 10, nj), RNG.uniform(0.01, 2, nj)
    e0 = 1 + np.sum(fj / wj ** 2)
    n_viol += e0 < 1
    if i < 20:
        epp = lambda w: float(np.sum(fj * gj * w / ((wj ** 2 - w ** 2) ** 2 + (gj * w) ** 2)))
        kk = 2 / math.pi * integrate.quad(lambda w: epp(w) / w, 0, np.inf, limit=800, points=None)[0]
        kk_err = max(kk_err, abs(kk - (e0 - 1)) / (e0 - 1))
check("A1 ELECTRIC FORBIDDEN", n_viol == 0 and kk_err < 1e-4,
      f"{n_viol} of 10^4 passive media with eps(0) < 1; KK sum rule reproduces eps(0)-1 to {kk_err:.1e} (20 samples). "
      "Gravity's polarization anti-screens (g > g_N) <=> eps < 1: no passive dielectric can do it")

# ======================================================== A2 magnetic mapping
P("\nA2  magnetic poles in a current-free medium: div(mu_r(H) H) = rho_m; point pole mu_r(H) H = Q/(4 pi r^2)")
errs = []
for b in np.logspace(-4, 4, 41):  # b = B/(mu0 H0) at the radius, H in units of H0
    H = optimize.brentq(lambda h: mu_law(h) * h - b, 1e-12, 1e8, xtol=1e-15, rtol=1e-14)
    g = 0.5 * (b + math.sqrt(b * b + 4 * b))  # law: g_N = g^2/(g + a0) with g_N = b, a0 = 1
    errs.append(abs(H / g - 1))
check("A2 mapping reproduces the law", max(errs) <= 1e-12, f"max |H/g - 1| = {max(errs):.1e} over g_N/a0 = 1e-4..1e4 (H <-> g, B/mu0 <-> g_N, H0 <-> a0)")

# ======================================================== A3 exact composite design
P("\nA3  superconducting grains (mu = 0 spheres; mu_i = 2 under MUTATE M1) in a mu = 1 matrix")
MU_I = 2.0 if MUT else 0.0
beta = (MU_I - 1) / (MU_I + 2)


def mg(fs):
    return (1 + 2 * fs * beta) / (1 - fs * beta)


def br(fs):  # symmetric Bruggeman, inclusions mu_i, host 1
    if MU_I == 0.0:
        return 1 - 1.5 * fs
    # general: fs (mu_i - m)/(mu_i + 2m) + (1-fs)(1-m)/(1+2m) = 0
    return optimize.brentq(lambda m: fs * (MU_I - m) / (MU_I + 2 * m) + (1 - fs) * (1 - m) / (1 + 2 * m), 1e-9, 10)


def fs_req_mg(x):
    m = mu_law(x)
    return (1 - m) / (1 + m / 2) if MU_I == 0.0 else (m - 1) / (beta * (2 + m))   # solve mg(fs) = m


def fs_req_br(x):
    return (2 / 3) * (1 - mu_law(x)) if MU_I == 0.0 else float("nan")


P("  MG: f_s(x) = 2/(2+3x) (check below);  BR: f_s(x) = (2/3)/(1+x)  -> both a shape-1 Lomax switching-field law")
xs_chk = np.logspace(-2, 2, 9)
if not MUT:
    a3a = max(abs(fs_req_mg(x) - 2 / (2 + 3 * x)) for x in xs_chk) + max(abs(fs_req_br(x) - (2 / 3) / (1 + x)) for x in xs_chk)
    P(f"  closed forms verified to {a3a:.1e}")
else:
    neg = all(fs_req_mg(x) < 0 for x in xs_chk)
    P(f"  M1 tooth: with paramagnetic grains (mu_i = 2) the required f_s is {'NEGATIVE for every x -> no solution (bites)' if neg else 'not negative (DID NOT BITE)'}")
    FAILS.append("MUTATE M1 (designed)")

DES = {}
if not MUT:
    for name, f_tot, fsr, emt in (("MG", 0.5, fs_req_mg, mg), ("BR", 0.6, fs_req_br, br)):
        x_min = optimize.brentq(lambda x: fsr(x) - f_tot, 1e-6, 1e3)
        S = lambda x: np.where(x < x_min, 1.0, fsr(np.maximum(x, x_min)) / f_tot)
        # sample switching fields from S by inversion on a fine grid
        xg = np.logspace(math.log10(x_min), 6, 20001)
        Sg = S(xg)
        u = RNG.uniform(Sg[-1], 1.0, 100000)
        xsw = np.interp(-u, -Sg, xg)
        xt = np.logspace(math.log10(x_min), 2, 200)
        S_emp = np.array([(xsw > x).mean() for x in xt])
        mu_emp = np.array([emt(f_tot * s) for s in S_emp])
        dev = float(np.max(np.abs(mu_emp - mu_law(xt))))
        DES[name] = dict(f=f_tot, x_min=x_min, mu_min=float(mu_law(x_min)), max_dev=dev)
        check(f"K1 {name} Monte-Carlo (N = 1e5)", dev <= 0.01,
              f"f = {f_tot}: x_min = {x_min:.3f} (mu_min {mu_law(x_min):.3f}, max boost {1 / mu_law(x_min):.2f}x); max |mu_eff - x/(1+x)| over [x_min, 100] = {dev:.4f}")
RES["numbers"]["A3"] = DES

# ======================================================== A4 real materials
P("\nA4  seven real superconductors (T -> 0 critical fields, mT; provisional): intermediate-state window (2/3)Hc..Hc per sphere")
HC = {"Al": 10.5, "In": 28.1, "Sn": 30.5, "Hg": 41.0, "Pb": 80.3, "Ta": 83.0, "Nb(Hc1)": 180.0}
names = list(HC)
hc = np.array([HC[k] for k in names])
if MUT:
    hc = hc * np.array([10.0 ** ((-1) ** j) for j in range(len(hc))])  # M2 shuffle by x10


def eta(H, Hc):  # superconducting volume fraction of a sphere in applied field H
    return np.clip(3 * (Hc - H) / Hc, 0, 1)


A4 = {}
for name, f_tot, fsr, emt in (("MG", 0.5, fs_req_mg if not MUT else (lambda x: 2 / (2 + 3 * x)), mg if not MUT else (lambda fs: (1 - fs) / (1 + fs / 2))),
                              ("BR", 0.6, fs_req_br if not MUT else (lambda x: (2 / 3) / (1 + x)), br if not MUT else (lambda fs: 1 - 1.5 * fs))):
    x_min = optimize.brentq(lambda x: fsr(x) - f_tot, 1e-6, 1e3)
    xt = np.logspace(math.log10(x_min), math.log10(30), 120)
    target = np.array([fsr(x) / f_tot for x in xt])
    best = None
    for H0 in np.logspace(-0.5, 2.5, 241):
        Amat = np.array([[eta(x * H0, h) for h in hc] for x in xt])
        Aaug = np.vstack([Amat, 30 * np.ones(len(hc))])
        baug = np.concatenate([target, [30.0]])
        w, _ = optimize.nnls(Aaug, baug)
        fs = f_tot * (Amat @ w)
        muv = np.array([emt(min(max(v, 0), 0.6666)) for v in fs])
        rms = float(np.sqrt(np.mean((muv - mu_law(xt)) ** 2)))
        if best is None or rms < best[0]:
            best = (rms, H0, w, muv)
    rms, H0, w, muv = best
    # stability: B ~ mu H must increase with H
    Hf = np.logspace(math.log10(x_min * H0), math.log10(30 * H0), 2000)
    fsf = f_tot * np.array([[eta(h, c) for c in hc] for h in Hf]) @ w
    Bf = np.array([emt(min(max(v, 0), 0.6666)) for v in fsf]) * Hf
    mono = bool(np.all(np.diff(Bf) >= -1e-12 * Bf[:-1]))
    A4[name] = dict(rms=rms, H0_mT=float(H0), weights={names[j]: float(w[j]) for j in range(len(names))}, x_min=float(x_min), B_monotone=mono,
                    max_dev=float(np.max(np.abs(muv - mu_law(xt)))))
    P(f"  {name} f={f_tot}: best H0 = {H0:.2f} mT, rms |dmu| = {rms:.4f} (max {A4[name]['max_dev']:.4f}) over x in [{x_min:.3f}, 30]; "
      f"B(H) monotone: {mono}; weights " + ", ".join(f"{k} {v:.2f}" for k, v in A4[name]['weights'].items() if v > 1e-3))
RES["numbers"]["A4"] = A4
if not MUT:
    lab = {k: ("BUILDABLE" if v["rms"] <= 0.03 else "APPROXIMATE") for k, v in A4.items()}
    check("A4 class (reported)", True, ", ".join(f"{k}: {v} (rms {A4[k]['rms']:.4f})" for k, v in lab.items()))
    RES["A4_class"] = lab
else:
    try:
        main = json.load(open(os.path.join(HERE, "cfg773_results.json")))
        worse = all(A4[k]["rms"] > main["numbers"]["A4"][k]["rms"] for k in A4)
        mut_r = ", ".join(f"{k} {A4[k]['rms']:.4f}" for k in A4)
        main_r = ", ".join(f"{k} {main['numbers']['A4'][k]['rms']:.4f}" for k in A4)
        P(f"  M2 tooth: shuffled critical fields rms {mut_r} vs main {main_r} -> {'bites' if worse else 'DID NOT BITE'}")
    except FileNotFoundError:
        P("  M2 tooth: run the main mode first")
    FAILS.append("MUTATE M2 (designed)")

# ======================================================== A5 analogue rotation curve
if not MUT:
    P("\nA5  point pole: s(r) = dln(rH)/dln r (law: s -> 0 deep, -1 Newtonian); flat = |s| <= 0.1")
    A5 = {}
    for name, f_tot, fsr, emt in (("MG", 0.5, fs_req_mg, mg), ("BR", 0.6, fs_req_br, br), ("LAW", None, None, None)):
        r = np.logspace(-3, 3, 3001)            # b = 1/r^2 in units where b = 1 at r = 1
        b = 1 / r ** 2
        if name == "LAW":
            H = 0.5 * (b + np.sqrt(b * b + 4 * b))
        else:
            H0, w = A4[name]["H0_mT"], np.array(list(A4[name]["weights"].values()))
            def muH(h):  # h in units of H0
                fs = f_tot * float(np.dot(w, eta(h * H0, hc)))
                return emt(min(max(fs, 0), 0.6666))
            H = np.array([optimize.brentq(lambda h: muH(h) * h - bb, 1e-12, 1e9) for bb in b])
        s = np.gradient(np.log(r * H), np.log(r))
        flat = np.abs(s) <= 0.1
        # longest contiguous flat run in decades
        best, cur = 0, 0
        for fl in flat:
            cur = cur + 1 if fl else 0
            best = max(best, cur)
        dec = best * (6 / 3000)
        A5[name] = dict(flat_decades=float(dec), s_min_abs=float(np.min(np.abs(s))))
        P(f"  {name:3s}: longest flat run {dec:.2f} decades in r; min |s| = {np.min(np.abs(s)):.3f}")
    RES["numbers"]["A5"] = A5
    check("A5 deep regime (reported)", True, f"BR flat {A5['BR']['flat_decades']:.2f} dec -> "
          f"{'DEEP REGIME REACHABLE' if A5['BR']['flat_decades'] >= 1 else 'DEEP REGIME NOT REACHED'}; MG {A5['MG']['flat_decades']:.2f} dec; law {A5['LAW']['flat_decades']:.2f} dec (grid edge)")

RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"cfg773_results{SUF}.json"), "w"), indent=1, default=float)
P("\nFAILS:", FAILS if FAILS else "none")
OUTF.close()
sys.exit(1 if FAILS else 0)
