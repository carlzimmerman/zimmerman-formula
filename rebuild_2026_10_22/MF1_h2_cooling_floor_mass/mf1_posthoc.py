#!/usr/bin/env python3
"""MF1 POST-HOC (no frozen verdict depends on this; written after the frozen run's results were read).

How much power does the class-median grade have? Per-system chi2 = sum (E/s)^2, class Z and Spearman on a fine lg M_f grid, 5.5 to 9.
Also: scatter-inflated chi2 with the sigma_int that gives chi2/N = 1 at M_f = 0, so a few tight systems do not dominate.
"""
import csv, json, math, os
import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
G, MSUN, PC, MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
SIG = {f: A0[f] / (2 * math.pi * G) for f in FEET}
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
        out.append(dict(cls=r["cls"], lm=float(r["logMstar"]), gobs=3 * (sc * 1e3) ** 2 / r12, gN=G * (Mb / 2) * MSUN / r12 ** 2, r12=r12,
                        M200=10 ** (a_ + b_ * (math.log10(Mb) - 10)), s=float(r["sdMC[Newton]"])))
    return out
def boot(E, s, rng, n=2000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float); ry = np.argsort(np.argsort(y)).astype(float); rx -= rx.mean(); ry -= ry.mean()
    return float((rx * ry).sum() / math.sqrt((rx ** 2).sum() * (ry ** 2).sum()))
def Es(Rw, f, Mf):
    out = []
    for x in Rw:
        M = max(x["M200"], Mf); R2 = R200_of(M); r0 = solve_r0(M * MSUN, R2, SIG[f])
        out.append(math.log10(x["gobs"] / (x["gN"] + G * math.pi * SIG[f] * r0 ** 2 * float(B(min(x["r12"], R2) / r0)) / x["r12"] ** 2)))
    return np.array(out)
P("MF1 POST-HOC; no frozen verdict depends on this. kappa = 1/2 FITTED; not theory closed")
RES = {}
for f in FEET:
    Rw = base(f); s = np.array([x["s"] for x in Rw]); lm = np.array([x["lm"] for x in Rw]); cl = np.array([x["cls"] for x in Rw])
    E0 = Es(Rw, f, 0.0)
    si = brentq(lambda v: np.sum(E0 ** 2 / (s ** 2 + v ** 2)) / len(E0) - 1, 0.0, 3.0)
    P(f"\n[{f}] N {len(Rw)}; sigma_int {si:.3f} dex at M_f = 0 (X49 itself)")
    P("  lg M_f   chi2   chi2_si  UFD chi2_si  rho   " + " ".join(f"{c[:9]:>9s}" for c in CLS) + "  all5")
    tab = {}
    for lg in [0.0] + list(np.arange(5.5, 9.01, 0.25)):
        E = Es(Rw, f, 10 ** lg if lg else 0.0); rng = np.random.default_rng(20261026)
        Z = [(lambda m_sd: m_sd[0] / m_sd[1])(boot(E[cl == c], s[cl == c], rng)) for c in CLS]
        c1 = float(np.sum((E / s) ** 2)); c2 = float(np.sum(E ** 2 / (s ** 2 + si ** 2))); u = cl == "MW ultra-faint"; c3 = float(np.sum(E[u] ** 2 / (s[u] ** 2 + si ** 2)))
        rho = spearman(lm, E); ok = all(abs(z) < 2 for z in Z); tab[f"{lg:.2f}"] = dict(chi2=c1, chi2_si=c2, ufd=c3, rho=rho, Z=Z, all5=ok)
        P(f"  {'none' if not lg else f'{lg:5.2f}':>6s} {c1:7.0f} {c2:7.1f} {c3:9.1f}  {rho:+.2f}  " + " ".join(f"{z:+9.2f}" for z in Z) + f"  {'YES' if ok else 'no'}")
    RES[f] = dict(sigma_int=si, table=tab)
json.dump(RES, open(os.path.join(HERE, "mf1_posthoc_results.json"), "w"), indent=1, default=lambda o: bool(o))
open(os.path.join(HERE, "mf1_posthoc.out"), "w").write("\n".join(OUT) + "\n")
