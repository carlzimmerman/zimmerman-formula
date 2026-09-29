#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E_reaction_energy_noether -- CFG121 G3 tests E1, E2, E3 and G3-edge, exactly as frozen.
E1 reaction: excess force on the baryons vs the target law, (i) pure phantom, (ii) V_U / V_B carrying the medium mass G1c requires.
E2 Noether: discrete 1D micro-model (baryon + medium centres + dipole charge pairs), total momentum conserved; MUTATE=recip breaks reciprocity.
E3 energy: E_int = integral_{r<r_e} w(|Pi|) dV, w = int g d|Pi| ; both r_ta conventions; E_net reported.  Line: E_int <= E_orb = (1/2) M V_f^2.
MUTATE=recip : non-reciprocal medium-baryon coupling in E2 -> E2 cells must change from PASS to FAIL.
"""
import math, sys, json, os
import numpy as np
import cfg121_common as C
from cfg121_common import G, A0, MASSES, rM_of, target_at, target_for, pol_model, nu_p2, MUTATE, HERE
from scipy.integrate import solve_ivp

R = C.Report("E_reaction_energy_noether")
R.banner(f"CFG121 E  (footing {C.FOOT}: a0 = {A0:.2f}; MUTATE='{MUTATE}')")
X = np.geomspace(0.3, 30.0, 121)
PS = json.load(open(os.path.join(HERE, "B_budget_pincer" + ("" if C.FOOT == "canonical" else "_second") + "_results.json")))["numbers"]["Pstar"]
Q_B, Q_U = PS["V_B"]["Q"], PS["V_U"]["Q"]


def M_D_cumulative(M, Q, xs):
    """M_D(<r) = integral M_c/(eps_c Q r) dr for the minimal medium (rho_D = M_c/(4 pi eps_c Q r^3), eps_c = 1), start at 0."""
    t = target_for(M)
    r, Mc = t["r"], t["w"] / G
    integrand = Mc / (Q * r)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(r))])
    rq = np.asarray(xs) * t["rM"]
    return np.interp(rq, r, cum)


# ------------------------------------------------------------------------------------------------ E1
R.banner("E1  reaction: max over x in [0.3, 30] of |g_model - g_tgt|/g_tgt   (line 0.10)")
E1 = {}
for M in MASSES:
    pm = pol_model(M, X)
    t = target_at(M, X)
    Mb, Mc, Mpol, r = t["Mb"], t["Mc"], pm["Mpol"], t["r"]
    base = np.abs(Mpol - Mc) / (Mb + Mc)
    E1[(M, "phantom")] = float(base.max())
    line = f"  M_b={M:.0e}: (i) pure phantom {base.max():.3f} (at x = {X[np.argmax(base)]:.2f})"
    for var, Qs in (("V_B", (1.0, Q_B)), ("V_U", (1.0, Q_U))):
        for Q in Qs:
            MD = M_D_cumulative(M, Q, X)
            if var == "V_B":
                Mdyn = Mb + Mpol + MD
            else:
                Mt = Mb + MD
                Mdyn = np.sqrt(Mt ** 2 + (A0 * r ** 2 / G) * Mt)
            rea = np.abs(Mdyn / (Mb + Mc) - 1.0)
            E1[(M, var, Q)] = float(rea.max())
            line += f";  {var} Q={Q:.3g}: {rea.max():.3f} (M_D/M_c at x=30: {MD[-1] / Mc[-1]:.3f})"
    R.P(line)
for var, Qkey in (("V_B", Q_B), ("V_U", Q_U)):
    st1 = max(E1[(M, var, 1.0)] for M in MASSES)
    stS = max(E1[(M, var, Qkey)] for M in MASSES)
    R.verdict(f"E1_{var}", "PASS" if (st1 <= 0.10 and stS <= 0.10) else "FAIL", f"worst reaction at Q = 1: {st1:.3f}; at Q* = {Qkey:.3g}: {stS:.3f}; pure phantom worst {max(E1[(M, 'phantom')] for M in MASSES):.3f} (the phantom-only excess is the T1.2 mismatch, 0 for a point mass)")

# ------------------------------------------------------------------------------------------------ E2
R.banner("E2  Noether check: 1D micro-model, pairwise gravity U = sum_{a<b} 2 pi G W_ab s_a s_b |x_a - x_b| (s = gravitational charge)")


def forces(x, s, W):
    n = len(x)
    F = np.zeros(n)
    for a in range(n):
        for b in range(n):
            if a != b:
                F[a] += -2 * math.pi * G * W[a, b] * s[a] * s[b] * np.sign(x[a] - x[b])
    return F


rng = np.random.default_rng(3)
ND = 13
xi = 0.2 * rng.standard_normal(ND)
Xc = np.sort(rng.uniform(-5, 5, ND))
pos = np.concatenate([[1.234], Xc, Xc + xi / 2, Xc - xi / 2])          # baryon, centres, +charges, -charges
Mb0, mD, qq = 1e10, 1e8, 5e7
s = np.concatenate([[Mb0], mD * np.ones(ND), qq * np.ones(ND), -qq * np.ones(ND)])
n = len(pos)
idx_b = 0
idx_c = np.arange(1, 1 + ND)
idx_p = np.arange(1 + ND, 1 + 3 * ND)
res2 = {}
for var in ("V_U", "V_B"):
    W = np.ones((n, n))
    if var == "V_B":
        # dipole charges interact with the baryon only (baryon-only auxiliary potential); centres interact with baryon and centres; charges not with centres
        W[np.ix_(idx_p, idx_c)] = 0.0
        W[np.ix_(idx_c, idx_p)] = 0.0
        W[np.ix_(idx_p, idx_p)] = 0.0
    if MUTATE == "recip":
        W = W.copy()
        W[idx_c, idx_b] = 0.0                                          # the baryon feels the medium, the medium does not feel the baryon: non-reciprocal medium-baryon coupling
        W[idx_b, idx_c] = 1.0
    F = forces(pos, s, W)
    tot = float(F.sum())
    scale = float(np.max(np.abs(F)))
    Fb = F[idx_b]
    Fothers = float(F[1:].sum())
    ok = abs(tot) / scale <= 1e-12
    res2[var] = (tot / scale, Fb, Fothers)
    R.P(f"  {var}: sum of all forces / max|F| = {tot / scale:.2e};  force on baryon {Fb:.6e}, force on (medium + dipole charges) {Fothers:.6e}, sum {Fb + Fothers:.2e}")
    R.verdict(f"E2_{var}", "PASS" if ok else "FAIL", f"momentum conservation |sum F|/max|F| = {abs(tot) / scale:.2e} (line 1e-12); force on baryon = minus force on (medium + bound charge)")
R.P("  scope: this checks the reciprocity built into the declared pairwise action; it is close to a tautology (a translation-invariant pair potential conserves momentum), and it does NOT test the field-theory coupling of the relativistic action.")
R.P("  the reaction on the baryons from the bound charge is the field of that charge, G M_pol(<r)/r^2, which for the pure phantom IS the law's phantom force (E1 (i): 0 for a point mass).")

# ------------------------------------------------------------------------------------------------ E3
R.banner("E3  energy: E_int = integral_{r<r_e} w 4 pi r^2 dr (w = W(P)/(4 pi G), P = 4 pi G |Pi|) vs E_orb = (1/2) M V_f^2, both r_ta conventions (r_e = 0.4 r_ta)")


def W_B(P):
    z = 2 * P / A0
    return -(1.0 / 8.0) * (A0 ** 2 * np.log1p(-z) + 2 * A0 * P + 2 * P ** 2)


def W_U(P):
    return W_B(P) + 0.5 * P ** 2


E3 = {}
for M in (1e9, 1e10, 1e11, 1e12):
    rM = rM_of(M)
    Vf2 = math.sqrt(G * M * A0)
    Eorb = 0.5 * M * Vf2
    for conv, rta in (("CFG48", C.r_ta_cfg48(M)), ("committed", C.r_ta_committed(M))):
        re = 0.4 * rta
        x = np.geomspace(1e-3, re / rM, 20001)
        pm = pol_model(M, x)
        P = pm["Mpol"] * G / pm["r"] ** 2                 # P = (nu-1) g_b (acceleration units)
        r = pm["r"]
        wB = W_B(P) / (4 * math.pi * G)
        wU = W_U(P) / (4 * math.pi * G)
        gtotU = P ** 2 / (A0 - 2 * P) + P
        enet = (W_U(P) - gtotU * P + 0.5 * P ** 2) / (4 * math.pi * G)
        integ = lambda w: float(np.trapz(w * 4 * math.pi * r ** 2, r))
        EB, EU, EN = integ(wB), integ(wU), integ(enet)
        E3[(M, conv)] = (EB / Eorb, EU / Eorb, EN / Eorb)
        R.P(f"  M_b={M:.0e} {conv:9s}: r_ta = {rta:7.1f} kpc, x_e = r_e/r_M = {re / rM:6.1f}:  E_int/E_orb  V_B {EB / Eorb:8.2f}   V_U {EU / Eorb:9.2f}   (V_U E_net/E_orb = {EN / Eorb:8.2f});  hand estimates: V_B (2/3) ln x_e = {2 / 3 * math.log(re / rM):.2f}, V_U x_e = {re / rM:.1f}")
for var, j in (("V_B", 0), ("V_U", 1)):
    worst = max(E3[k][j] for k in E3 if k[0] in (1e9, 1e10, 1e12))
    R.verdict(f"E3_{var}", "PASS" if worst <= 1.0 else "FAIL", f"worst E_int/E_orb over 1e9, 1e10, 1e12 and both r_ta conventions = {worst:.2f} (line 1); a reversible store, not an unfunded reservoir; CFG48/CFG70 exchange energy was 23-318x")

# ------------------------------------------------------------------------------------------------ G3-edge
R.banner("G3-edge  Gauss neutral-charge: a finite medium (R_D = 0.4 r_ta) carries zero net bound charge -> negative shell phi_max M_c(R_D) at eps_c Q = 1")


def phi_max(M, eq, xtop):
    t = target_for(M)
    r, rho, Mc = t["r"], t["rho"], t["w"] / G

    def rhs(lnr, y):
        rr = math.exp(lnr)
        rh = float(np.exp(np.interp(lnr, np.log(r), np.log(rho))))
        return [rr * (4 * math.pi * rr ** 2 * rh - y[0] / (eq * rr))]
    sol = solve_ivp(rhs, (math.log(r[0]), math.log(r[-1])), [0.0], t_eval=np.log(r), method="Radau", rtol=1e-9, atol=1e-3)
    return r / t["rM"], sol.y[0] / Mc, Mc


for M in (1e10, 1e11, 1e12):
    xs, ph, Mc = phi_max(M, 1.0, 200.0)
    for conv, rta in (("CFG48", C.r_ta_cfg48(M)), ("committed", C.r_ta_committed(M))):
        xe = 0.4 * rta / rM_of(M)
        phi = float(np.interp(xe, xs, ph))
        Mc_e = float(np.interp(xe, xs, Mc))
        cfg48_shell = M * (math.sqrt(1 + xe ** 2) - 1)
        R.P(f"  M_b={M:.0e} {conv:9s}: x_e = {xe:6.1f}, phi_max = {phi:.3f}, M_c(R_D) = {Mc_e:.3e}, negative shell = {phi * Mc_e:.3e} Msun;  CFG48-type flux-gated shell M_b(sqrt(1+x_e^2)-1) = {cfg48_shell:.3e}")
R.verdict("G3edge", "REPORTED", "no frozen pass line: a bounded polarised medium cannot carry its enclosed bound charge beyond its edge (net zero); the shell is phi_max M_c(R_D), the same order as CFG48's negative shell")
R.finish(required_change=["E2_V_U", "E2_V_B"] if MUTATE == "recip" else None)
