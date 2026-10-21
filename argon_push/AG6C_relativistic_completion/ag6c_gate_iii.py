"""AG6C gate (iii): Solar System of candidate C1 (stiffness = cold-medium pressure, acting on div P only).

Criteria: FROZEN_CRITERIA.md (committed alone first, e926935c3).
Re-implements CFG770's Fourier linear response of the Sun's perturbation in the Galaxy's uniform background (read-only
reference: campaign_fresh_gravity/CFG770_cassini_stiff_action/cfg770.py; nothing imported or executed from there).
  L49 (CFG770):  m_i = (A_i + s)/(A_i + 1 + s),  deficit 1 - S = sum_i khat_i^2/(A_i + 1 + s),  s = Lam^2 k^2, Lam^2 = gamma/K
  C1 (this lane): stiffness on div P only => G_eff/G = 1 + 1/(1/E_k - 1 + s),  E_k = sum_i khat_i^2/(1 + A_i),
                 deficit 1 - S = E_k/(1 + s E_k)
  dPhi(k) = -4 pi G M/(k^2 S);  Q2 = (G M/pi) int k^2 dk int dc P2(c) (1/S - 1)   [Park/Hees convention, as CFG770]
Control K: the L49 branch must reproduce cfg770_results.json (T1 Q2 and T3) to <= 1e-6 relative.
Run: python3 ag6c_gate_iii.py      (AG6C_MUTATE=1: L* = 1e-4 pc, the planetary gates must fail)
"""
import json
import math
import os
import sys

import numpy as np
from scipy import integrate

MUT = os.environ.get("AG6C_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag6c_gate_iii{SUF}.out"), "w")
RES = {"lane": "AG6C", "script": "ag6c_gate_iii", "mutate": MUT, "checks": {}, "numbers": {}}
FAILS = []
CFG770_JSON = os.path.join(HERE, "..", "..", "campaign_fresh_gravity", "CFG770_cassini_stiff_action", "cfg770_results.json")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.write(s + "\n")


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


G = 6.67430e-11
MSUN = 1.98847e30
GM = 1.32712440018e20
AU = 1.495978707e11
PC = 3.0856775814913673e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
GE = [2.00e-10, 2.32e-10, 2.64e-10]
Q2_CEIL, A_SUNWARD, M_SAT_BOUND, R_SAT = 5.2e-27, 3.66e-14, 6.7e-11, 9.54 * AU     # CFG770's ceilings, inherited
R = lambda u, a0: u * u / (a0 - u)
dR = lambda u, a0: (2 * u * a0 - u * u) / (a0 - u) ** 2


def background(ge, a0):
    ue = a0 * ge / (a0 + ge)
    return dict(ue=ue, gNe=ge - ue, Apar=dR(ue, a0), Aperp=R(ue, a0) / ue)


XC, WC = np.polynomial.legendre.leggauss(96)
P2C = 0.5 * (3 * XC ** 2 - 1)


def defic(kap, Apar, Aperp, model):
    if model == "L49":
        return XC ** 2 / (Apar + 1 + kap ** 2) + (1 - XC ** 2) / (Aperp + 1 + kap ** 2)
    Ek = XC ** 2 / (Apar + 1) + (1 - XC ** 2) / (Aperp + 1)
    return Ek / (1 + kap ** 2 * Ek)


def defic0(kap, Apar, Aperp, model):          # the c = 0 value
    if model == "L49":
        return 1.0 / (Aperp + 1 + kap ** 2)
    E0 = 1.0 / (Aperp + 1)
    return E0 / (1 + kap ** 2 * E0)


def J(kap, Apar, Aperp, model):
    d = defic(kap, Apar, Aperp, model)
    d0 = defic0(kap, Apar, Aperp, model)
    return float(np.sum(WC * P2C * (d / (1 - d) - d0 / (1 - d0))))


def Q2(Lam, Apar, Aperp, model):
    f = lambda t: (math.exp(t) ** 3) * J(math.exp(t), Apar, Aperp, model)
    val = 0.0
    for lo, hi in [(-12, -4), (-4, 0), (0, 4), (4, 12)]:
        val += integrate.quad(f, lo, hi, limit=400, epsabs=0, epsrel=1e-11)[0]
    return GM / (math.pi * Lam ** 3) * val


def a_anom(r, Lam, Apar, Aperp, model):
    lead = -GM / (2 * Lam ** 2)
    x0 = r / Lam

    def j1(x):
        return (math.sin(x) / x - math.cos(x)) / x if x > 1e-4 else x / 3 - x ** 3 / 30

    def g(t):
        kap = math.exp(t)
        d = defic(kap, Apar, Aperp, model)
        rem = float(0.5 * np.sum(WC * (d / (1 - d) - 1 / kap ** 2)))
        return kap * kap * j1(kap * x0) * rem

    val = 0.0
    for lo, hi in [(-14, -6), (-6, -2), (-2, 2), (2, 6), (6, 9)]:
        val += integrate.quad(g, lo, hi, limit=600, epsabs=1e-30, epsrel=1e-10)[0]
    return lead - (2 * GM / math.pi) * val / Lam ** 2


P("AG6C gate (iii): Solar System of C1 vs L49 (CFG770 replica)" + ("  [MUTATE: L* = 1e-4 pc]" if MUT else ""))
BG = {(f, ge): background(ge, a0) for f, a0 in A0.items() for ge in GE}
for (f, ge), b in BG.items():
    P(f"  {f:9s} g_e {ge:.2e}: u_e/a0 {b['ue'] / A0[f]:.4f}, A_par {b['Apar']:.4f}, A_perp {b['Aperp']:.4f}, "
      f"e = g_e/a0 = {ge / A0[f]:.3f}")

# ---------------------------------------------------------------- P1 structure
P("\nP1  structure: gravity = Einstein-Hilbert, baryons dark-neutral, matter minimally coupled =>")
P("    PPN beta = gamma = 1, alpha_1 = alpha_2 = alpha_3 = xi = zeta_i = 0 (GR's values); the only non-GR effect is the")
P("    cold medium's Newtonian potential (static, screened), computed below. Local cold density (Galactic, smooth on")
P("    scales < L*) acts like any uniform matter background.")

# ---------------------------------------------------------------- control K: reproduce CFG770
P("\nControl K: the L49 branch at L* = 5.75 pc must reproduce cfg770_results.json")
ref = json.load(open(CFG770_JSON))["numbers"]
Lam575 = 5.75 * PC / math.sqrt(2)
kerr = 0.0
for (f, ge), b in BG.items():
    key = f"{f}_{ge:.2e}"
    q = Q2(Lam575, b["Apar"], b["Aperp"], "L49")
    a1 = a_anom(AU, Lam575, b["Apar"], b["Aperp"], "L49")
    aS = a_anom(R_SAT, Lam575, b["Apar"], b["Aperp"], "L49")
    Ms = abs(aS) * R_SAT ** 2 / G / MSUN
    e1 = abs(q / ref["T1_Q2"][key] - 1)
    e2 = abs(a1 / ref["T3"][key]["a1AU"] - 1)
    e3 = abs(Ms / ref["T3"][key]["Msat"] - 1)
    kerr = max(kerr, e1, e2, e3)
    P(f"  {key}: Q2 {q:+.6e} (CFG770 {ref['T1_Q2'][key]:+.6e}), 1 AU {a1:+.6e}, Saturn {Ms:.6e}; max rel dev {max(e1, e2, e3):.1e}")
check("K CFG770 reproduced", kerr <= 1e-6, f"max relative deviation {kerr:.1e} over Q2, 1 AU pull, Saturn monopole")

# ---------------------------------------------------------------- C1 at both stiffness points
LS_LIST = [1e-4] if MUT else [5.75, 24.0]
tabs = {}
for Lpc in LS_LIST:
    Lam = Lpc * PC / math.sqrt(2)
    P(f"\nC1 and L49 at L* = {Lpc:g} pc")
    t = {}
    for (f, ge), b in BG.items():
        key = f"{f}_{ge:.2e}"
        row = {}
        for model in ("L49", "C1"):
            q = Q2(Lam, b["Apar"], b["Aperp"], model)
            a1 = a_anom(AU, Lam, b["Apar"], b["Aperp"], model)
            aS = a_anom(R_SAT, Lam, b["Apar"], b["Aperp"], model)
            Ms = abs(aS) * R_SAT ** 2 / G / MSUN
            row[model] = dict(Q2=q, Q2_ratio=abs(q) / Q2_CEIL, a1AU=a1, pull_ratio=abs(a1) / A_SUNWARD, Msat=Ms,
                              Msat_ratio=Ms / M_SAT_BOUND)
        row["Q2_C1_over_L49"] = row["C1"]["Q2"] / row["L49"]["Q2"] if row["L49"]["Q2"] != 0 else float("nan")
        t[key] = row
        c1 = row["C1"]
        P(f"  {key}: C1 |Q2|/ceil {c1['Q2_ratio']:.3e} (C1/L49 = {row['Q2_C1_over_L49']:.4f}); 1 AU pull {c1['a1AU']:+.4e} "
          f"(ratio {c1['pull_ratio']:.4f}; L49 {row['L49']['a1AU']:+.4e}); Saturn {c1['Msat_ratio']:.4f} of bound")
    tabs[str(Lpc)] = t
    worst = max(max(v["C1"]["Q2_ratio"], v["C1"]["pull_ratio"], v["C1"]["Msat_ratio"]) for v in t.values())
    RES["numbers"][f"Lstar_{Lpc:g}pc"] = t
    if MUT:
        check(f"(iii) C1 Solar System at L* = {Lpc:g} pc [MUTATE]", worst < 1, f"worst ratio {worst:.3e}")
        P(f"  MUTATE tooth {'bites' if worst >= 1 else 'DID NOT BITE'}")
    elif Lpc == 24.0:
        check("(iii) C1 Solar System at L* = 24 pc", worst < 1,
              f"worst of |Q2|/ceiling, 1 AU pull/bound, Saturn monopole/bound = {worst:.3e} (3 fields x 2 footings)")
    else:
        P(f"  [REPORTED] worst ratio at L* = 5.75 pc: {worst:.4f} (Saturn monopole is tight by construction of CFG691's floor)")

RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"ag6c_gate_iii_results{SUF}.json"), "w"), indent=1, default=float)
P("\nFAILS:", FAILS if FAILS else "none")
OUT.close()
sys.exit(1 if FAILS else 0)
