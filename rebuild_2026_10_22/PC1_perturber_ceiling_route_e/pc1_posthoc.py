#!/usr/bin/env python3
"""PC1 POST-HOC (no frozen verdict depends on this; written after pc1_ceiling.py's results were read).

(a) B1938 V at a compact r0 instead of the frozen 2D ceiling's kpc-scale sheet. (b) Round trip of M200 <-> r0, and which classical
dwarf is above the ceiling. (c) A low-mass halo floor M200 = max(EM1 relation, M_f): is any single M_f compatible with all five X49
classes? M_f would be a NEW fitted constant, so a window here is a target for a derivation, not a result.
"""
import csv, json, math, os
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
G, MSUN, PC, MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
SIG = {f: A0[f] / (2 * math.pi * G) for f in FEET}; SIGPC = {f: SIG[f] * PC ** 2 / MSUN for f in FEET}
CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")
def B(x): x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
a_, b_ = EM1J["rows"]["A_c2b_refit"]["R1"]["a"], EM1J["rows"]["A_c2b_refit"]["R1"]["b"]; h = F3["A_c2b_refit"]["params"]["h"]
RHOC = 3 * (100 * h * 1e3 / MPC) ** 2 / (8 * math.pi * G)
def R200_of(M): return (3 * M * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
def solve_r0(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot): return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
def M200_of_r0(r0_pc, f):
    r0 = r0_pc * PC
    return math.exp(brentq(lambda lm: math.pi * SIG[f] * r0 ** 2 * float(B(R200_of(math.exp(lm)) / r0)) / MSUN - math.exp(lm), math.log(1e2), math.log(1e15)))
def rho_hat(s): return 1.0 / ((1 + s) * (1 + s * s))
def m2d_hat(X):
    def col(u): return 2 * quad(lambda z: rho_hat(math.hypot(u, z)), 0, math.sqrt(max(1e4 - u * u, 0.0)), limit=200)[0]
    return quad(lambda u: 2 * math.pi * u * col(u), 0, X, limit=200)[0]
P("PC1 POST-HOC; no frozen verdict depends on this. kappa = 1/2 FITTED; not theory closed")

# (a) B1938 V, 80 pc: 3D ceiling, and 2D mass inside 80 pc as r0 varies
P("\n(a) B1938 V: M_obs = 1.13e6 (2D, 80 pc), low edge 1.05e6")
for f in FEET:
    C3D = 1.5990 * SIGPC[f] * 80 ** 2
    P(f" [{f}] 3D ceiling at 80 pc {C3D:.3g} -> R(3D) {1.05e6 / C3D:.2f}")
    for r0 in (40., 83., 160., 400., 1600.):
        m2 = m2d_hat(80. / r0) * (SIGPC[f] / r0) * r0 ** 3; mw = M200_of_r0(r0, f)
        P(f"   r0 {r0:6.0f} pc  M2D(<80 pc) {m2:.3g}  R {1.05e6 / m2:5.2f}  mean column {m2 / (math.pi * 80 ** 2):6.1f} Msun/pc^2  M200 {mw:.2e}")

# (b) round trip
P("\n(b) round trip M200 -> r0 -> M200")
for f in FEET:
    for M in (1e6, 1e8, 1e10):
        r0 = solve_r0(M * MSUN, R200_of(M), SIG[f]) / PC; P(f" [{f}] M200 {M:.0e}: r0 {r0:7.1f} pc, back {M200_of_r0(r0, f):.4e}")

# (c) low-mass halo floor
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
def base(f):
    out = []
    for r in X1:
        if r["footing"] != f or r["cls"] not in CLS: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC; Mb = 10 ** float(r["logMstar"])
        out.append(dict(name=r["name"], cls=r["cls"], gobs=3 * (sc * 1e3) ** 2 / r12, gN=G * (Mb / 2) * MSUN / r12 ** 2, r12=r12,
                        M200=10 ** (a_ + b_ * (math.log10(Mb) - 10)), s=float(r["sdMC[Newton]"])))
    return out
def boot(E, s, rng, n=4000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
RES = {}
P("\n(c) M200 = max(EM1 relation, M_f). Z per class; a class is reproduced if |Z| < 2 (X49's rule)")
P("    " + "lg M_f  " + " ".join(f"{c[:13]:>13s}" for c in CLS) + "  all five")
for f in FEET:
    Rw = base(f); RES[f] = {}
    P(f" [{f}]")
    for lm in np.arange(5.5, 8.01, 0.25):
        rng = np.random.default_rng(20261026); zs = []
        for c in CLS:
            q = [x for x in Rw if x["cls"] == c]; E = []
            for x in q:
                M = max(x["M200"], 10 ** lm); R2 = R200_of(M); r0 = solve_r0(M * MSUN, R2, SIG[f])
                E.append(math.log10(x["gobs"] / (x["gN"] + G * math.pi * SIG[f] * r0 ** 2 * float(B(min(x["r12"], R2) / r0)) / x["r12"] ** 2)))
            m, sd = boot(np.array(E), np.array([x["s"] for x in q]), rng); zs.append(m / sd)
        ok = all(abs(z) < 2 for z in zs); RES[f][f"{lm:.2f}"] = dict(Z=zs, all_five=ok)
        P(f"    {lm:5.2f}  " + " ".join(f"{z:+13.2f}" for z in zs) + f"  {'YES' if ok else 'no'}")
    # the classical dwarf above the frozen ceiling
    for x in Rw:
        gC = x["gN"] + 0.2545 * A0[f]
        if x["cls"] == "MW classical" and math.log10(x["gobs"] / gC) > 2 * x["s"]:
            P(f"    classical above ceiling: {x['name']}  E_C {math.log10(x['gobs'] / gC):+.3f} +- {x['s']:.3f}; g_obs {x['gobs'] / A0[f]:.3f} a0")
json.dump(RES, open(os.path.join(HERE, "pc1_posthoc_results.json"), "w"), indent=1)
open(os.path.join(HERE, "pc1_posthoc.out"), "w").write("\n".join(OUT) + "\n")
