#!/usr/bin/env python3
"""TOE0 graded items: TOE0-S (does action (A) reopen the flavor wall?) and TOE0-P (can the clock make its own charge
together with the baryons?). Criteria 8a99cb7c34, amendment A1 12225b6050.

Run:   python3 toe0.py            -> toe0.out / toe0.json
       python3 toe0.py --mutate   -> toe0_MUTATE.out / toe0_MUTATE.json  (M1 flipped susceptibility, M2 dropped c J term)

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json
import os
import sys

import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = "--mutate" in sys.argv
TAG = "toe0_MUTATE" if MUTATE else "toe0"
LINES = []
RES = {"criteria": "8a99cb7c34", "amendment": "12225b6050", "mutate": MUTATE}


def say(s=""):
    LINES.append(s)
    print(s, flush=True)


# ---------------------------------------------------------------- TOE0-S
say("== TOE0-S: matter couplings of action (A), read from QX17 ==")
qx17 = open(os.path.join(REPO, "closure_2026_11_06/QX17_covariant_field_equations/RESULT.md")).read().splitlines()
a_line = [l for l in qx17 if l.rstrip().endswith("(A)") and "S_m" in l]
e5_line = [l for l in qx17 if l.startswith("**(E5) Matter.**")]
say("(A): " + (a_line[0].strip() if a_line else "NOT FOUND"))
say("E5 : " + (e5_line[0].strip() if e5_line else "NOT FOUND"))
ok_a = len(a_line) == 1 and a_line[0].split("}")[-1].strip().startswith("+ S_m")
inside = a_line[0].split("{", 1)[1].rsplit("}", 1)[0] if a_line else ""
matter_tokens = [t for t in ("psi", "S_m", "J_B", "J_X", "T^m") if t in inside]
ok_e5 = len(e5_line) == 1 and "minimally coupled to g" in e5_line[0]
s_label = "WALL STANDS" if (ok_a and ok_e5 and not matter_tokens) else "WALL REOPENED or NOT READ"
say(f"S_m outside the gravity braces: {ok_a}; matter tokens inside the braces: {matter_tokens}; E5 minimal: {ok_e5}")
say(f"TOE0-S label: {s_label}")
RES["TOE0_S"] = {"label": s_label, "S_m_outside": ok_a, "matter_tokens_inside": matter_tokens, "E5_minimal": ok_e5}

# ---------------------------------------------------------------- TOE0-P, P1 and KA1, KA3
say()
say("== TOE0-P P1: Noether current of the dust term + L_c = c d_m tau J_X^m (generic inverse metric, sympy) ==")
t = sp.symbols("t0:4", real=True)          # d_m tau
j = sp.symbols("j0:4", real=True)          # J_X^m
gi = sp.Matrix(4, 4, lambda a, b: sp.Symbol(f"g{min(a, b)}{max(a, b)}", real=True))  # g^{ab}
muK, K, c = sp.symbols("mu_K K c", positive=True)
Q2 = -sum(gi[a, b] * t[a] * t[b] for a in range(4) for b in range(4))
Q = sp.sqrt(Q2)
LK = muK**2 * (Q - 1) ** 2 / (2 * K)
Lc = c * sum(t[m] * j[m] for m in range(4))
nU = [-sum(gi[m, b] * t[b] for b in range(4)) / Q for m in range(4)]
rhoQ = muK**2 * (Q - 1) / K

ka1 = [sp.simplify(sp.diff(LK, t[m]) - rhoQ * nU[m]) for m in range(4)]
ka1_ok = all(d == 0 for d in ka1)
say(f"KA1 dust-term current = mu_K^2 (Q-1)/K n^m : {'PASS' if ka1_ok else 'FAIL'}")
# charge along n: -n_m J^m with n_m = -t_m / Q
nL = [-t[m] / Q for m in range(4)]
chg = sp.simplify(-sum(nL[m] * rhoQ * nU[m] for m in range(4)) - rhoQ)
say(f"KA1b charge density along n equals rho_Q: {'PASS' if chg == 0 else 'FAIL'}")

claimed = [rhoQ * nU[m] + (0 if MUTATE else c * j[m]) for m in range(4)]   # M2 drops c J
p1 = [sp.simplify(sp.diff(LK + Lc, t[m]) - claimed[m]) for m in range(4)]
p1_ok = all(d == 0 for d in p1)
say(f"P1 total shift current = rho_Q n^m + c J_X^m {'(M2: c J dropped)' if MUTATE else ''}: {'PASS' if p1_ok else 'FAIL'}"
    f"  residuals {[str(d)[:40] for d in p1]}")

# FRW: d/dt [ a^3 dL/d(d_0 tau) ] = 0  with  d tau = (q(t),0,0,0), g^{00} = -1
tt = sp.symbols("t", real=True)
a = sp.Function("a")(tt)
q = sp.Function("q")(tt)
nX = sp.Function("n_X")(tt)
sub = {t[0]: q, t[1]: 0, t[2]: 0, t[3]: 0, j[0]: nX, j[1]: 0, j[2]: 0, j[3]: 0,
       gi[0, 0]: -1, gi[0, 1]: 0, gi[0, 2]: 0, gi[0, 3]: 0}
pi0 = sp.simplify((sp.diff(LK + Lc, t[0])).subs(sub).subs({q: sp.Symbol("qq", positive=True)}))
pi0 = pi0.subs(sp.Symbol("qq", positive=True), q)
frw_total = sp.simplify(pi0 - (muK**2 * (q - 1) / K + c * nX))
say(f"FRW: d L / d(d_0 tau) = rho_Q + c n_X  ->  d(a^3 rho_Q)/dt = -c d(a^3 n_X)/dt : "
    f"{'PASS' if frw_total == 0 else 'FAIL'}")
# KA3: X conserved -> clock charge unchanged
eom = sp.diff(a**3 * (muK**2 * (q - 1) / K + c * nX), tt)
ka3 = sp.simplify(eom.subs(sp.Derivative(nX, tt), -3 * sp.Derivative(a, tt) / a * nX)
                  - sp.diff(a**3 * muK**2 * (q - 1) / K, tt))
say(f"KA3 with d(a^3 n_X)/dt = 0 the clock's comoving charge obeys d(a^3 rho_Q)/dt = 0 (R541 reproduced): "
    f"{'PASS' if ka3 == 0 else 'FAIL'}")
RES["P1"] = {"pass": bool(p1_ok), "KA1": bool(ka1_ok and chg == 0), "FRW": bool(frw_total == 0), "KA3": bool(ka3 == 0)}

# ---------------------------------------------------------------- TOE0-P, P2 and KA2
say()
say("== TOE0-P P2: sign of c_X n_X(c_X Q) on exact FD / BE asymmetries (T = 1, g = 1, Q = 1, mu = c_X) ==")
mp.mp.dps = 30
SIGN = -1 if MUTATE else 1   # M1: flipped susceptibility


def n_asym(mu, m, stat):
    """particle minus antiparticle number density, T = 1, g = 1; None where it does not exist."""
    mu = mp.mpf(mu)
    m = mp.mpf(m)
    eta = 1 if stat == "FD" else -1
    if stat == "BE" and abs(mu) >= m and mu != 0:
        return None

    def f(p):
        E = mp.sqrt(p * p + m * m)
        return p * p * (1 / (mp.exp(E - mu) + eta) - 1 / (mp.exp(E + mu) + eta))

    val = mp.quad(f, [0, 0.5, 2, 8, 30, mp.inf]) / (2 * mp.pi**2)
    return SIGN * val


# KA2: massless FD exact
ka2 = []
for mu in (0.1, 0.3, 0.5):
    num = n_asym(mu, 0, "FD") * SIGN
    exact = mp.mpf(mu) / 6 + mp.mpf(mu) ** 3 / (6 * mp.pi**2)
    ka2.append(float(abs(num / exact - 1)))
ka2_ok = max(ka2) <= 1e-12
say(f"KA2 massless FD asymmetry = mu/6 + mu^3/(6 pi^2): max rel err {max(ka2):.2e} -> {'PASS' if ka2_ok else 'FAIL'}")

grid = [mp.mpf(-0.5) + mp.mpf(k) / 40 for k in range(41)]
rows = [("FD", 0), ("FD", 1), ("FD", 5), ("BE", 0), ("BE", 1), ("BE", 5)]
table = {}
for stat, m in rows:
    vals = []
    for mu in grid:
        n = n_asym(mu, m, stat)
        vals.append(None if n is None else float(mu * n))   # c_X n_X(c_X), c_X = mu
    table[f"{stat}_m{m}"] = vals
    defined = [v for v in vals if v is not None]
    say(f"  {stat} m/T={m}: defined {len(defined)}/41, min c*n = {min(defined):+.3e}, "
        f"max c*n = {max(defined):+.3e}, negatives {sum(1 for v in defined if v < 0)}")


def label(rowkeys):
    vals = [v for k in rowkeys for v in table[k]]
    if any(v is None for v in vals):
        neg = any(v is not None and v < -1e-25 for v in vals)
        return "CREATES" if neg else "UNDECIDED"
    if any(v < -1e-25 for v in vals):
        return "CREATES"
    return "DRAINS"


p2_frozen = label(list(table))
p2_amended = label([k for k in table if k != "BE_m0"])
say(f"P2 frozen reading (all 6 rows, 246 points): {p2_frozen}")
say(f"P2 amended reading A1 (5 rows, 205 points; BE m/T=0 undefined at {sum(1 for v in table['BE_m0'] if v is None)} "
    f"of 41 points): {p2_amended}")


def toe0p(p1, p2):
    if p1 and p2 == "DRAINS":
        return "CANNOT FIX 5.41"
    if p1 and p2 == "CREATES":
        return "CAN FIX 5.41 IN PRINCIPLE"
    return "NO VERDICT"


lab_frozen = toe0p(p1_ok, p2_frozen)
lab_amended = toe0p(p1_ok, p2_amended)
say(f"TOE0-P label: frozen {lab_frozen} / amended (A1) {lab_amended}")
RES["P2"] = {"KA2_max_rel_err": max(ka2), "KA2": bool(ka2_ok), "frozen": p2_frozen, "amended": p2_amended,
             "table": {k: v for k, v in table.items()}, "grid_mu_over_T": [float(x) for x in grid]}
RES["TOE0_P"] = {"frozen": lab_frozen, "amended": lab_amended}

# ---------------------------------------------------------------- reported numbers (not graded)
if not MUTATE:
    say()
    say("== reported, not graded ==")
    m_p = 0.93827208816            # GeV
    T = 130.0                      # GeV, sphaleron freeze-out
    gstar = 106.75
    s_over_ngamma0 = 7.04          # today
    eta_obs = 6.1e-10
    z3 = float(mp.zeta(3))
    rep = {}
    for foot, share in (("canonical", 5.410), ("alt", 5.412)):
        c541 = share * m_p
        out = {"c_X_GeV": c541}
        for Nf in (6, 5):
            muq = c541 / 3.0
            nq = 6.0 * (muq * T**2 / 6.0 + muq**3 / (6 * 3.141592653589793**2))   # g_q = 2 spin x 3 colour
            nB = Nf * nq / 3.0
            s = 2 * 3.141592653589793**2 / 45 * gstar * T**3
            eta = nB / s * s_over_ngamma0
            out[f"eta_Nf{Nf}"] = eta
            out[f"eta_over_obs_Nf{Nf}"] = eta / eta_obs
        rep[foot] = out
        say(f"{foot}: |c_X| for 5.41 rho_b = {c541:.4f} GeV; eta at T=130 GeV: Nf=6 {out['eta_Nf6']:.3e} "
            f"({out['eta_over_obs_Nf6']:.2e} x observed), Nf=5 {out['eta_Nf5']:.3e} ({out['eta_over_obs_Nf5']:.2e} x)")
    # c implied by observed eta (linear in c), and its drain
    s = 2 * 3.141592653589793**2 / 45 * gstar * T**3
    for Nf in (6, 5):
        per_c = Nf * 6.0 * (1.0 / 3.0) * T**2 / 6.0 / 3.0 / s * s_over_ngamma0    # eta per unit c (GeV^-1)
        c_obs = eta_obs / per_c
        rep[f"c_obs_Nf{Nf}_GeV"] = c_obs
        rep[f"drain_over_rho_b_Nf{Nf}"] = c_obs / m_p
        rep[f"n_init_over_nB_needed_Nf{Nf}"] = 5.41 * m_p / c_obs
        say(f"Nf={Nf}: observed eta needs |c_X| = {c_obs:.3e} GeV; drain = {c_obs / m_p:.2e} rho_b; "
            f"a 5.41 return from an excess start needs a primordial asymmetry {5.41 * m_p / c_obs:.2e} x today's")
    rep["zeta3"] = z3
    RES["reported"] = rep

with open(os.path.join(HERE, TAG + ".json"), "w") as fh:
    json.dump(RES, fh, indent=1)
with open(os.path.join(HERE, TAG + ".out"), "w") as fh:
    fh.write("\n".join(LINES) + "\n")
