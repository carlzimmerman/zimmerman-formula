#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE1 -- THE VACUUM GATE'S OWN HIGH-z PRICE: does the dark-energy-gated MOND switch keep MOND on at the framework's
flagship radius at z ~ 2.5?

WHY.  In the construction the record assembled (C-H/K + vacuum-gated switch + bound-region kernel + carrier), dark energy
does two jobs: it sets the MOND scale, a0 = kappa c sqrt(G rho_Lambda), and its share of the expansion gates WHERE the
MOND response acts (L359):
      u = x~ [Omega_Lambda(z)/Omega_Lambda,0]^p >= x_c0,   i.e.   x_c,eff(z) = x_c0 E(z)^(2p),   Omega_Lambda = 3 Lambda/K^2.
The framework's distinctive prediction (the flagship) is a FLAT a0(z): the deep-MOND Tully-Fisher zero point at the
outer radius g_bar = 0.1 a0 is unchanged at z ~ 2.5 (framework 0.00 dex, LCDM +0.33).  GP5 and L356 priced the CARRIER
there.  The gate's own price there has not been computed.  It matters because the best-standing construction uses the
gate at p = 2, x_c0 = 2 (L364's cosmic-shear cell; L367 finds cosmic shear passes with it and fails with p = 1 at the
window kicks; L380 runs it), and the gate rises steeply into the matter era.  By Gauss (L352 Z1), beyond the switch edge
a galaxy weighs exactly its baryons, so if the flagship radius lies beyond the edge its zero point moves by
-2 log10 nu(0.1) ~ -1.1 dex (the Newtonian value) instead of 0.

THE EDGE IN CLOSED FORM.  In deep MOND the switch variable at radius r is x(r) = 4 pi G rho_dyn(r)/H^2 = v_f^2/(r H)^2
(the local density of the isothermal phantom; the background rho_bar is < 1% there), so the edge is
      r_e(z) = v_f / (sqrt(x_c,eff(z)) H(z)) = v_f / (sqrt(x_c0) H0 E(z)^(1+p))                 (L352 Z6 at z = 0)
and the deepest acceleration still inside the MOND region is
      y_edge(z) = G M_b/(a0 r_e^2) = x_c0 (H0^2/a0^(3/2)) sqrt(G M_b) E(z)^(2+2p).
The flagship (y = 0.1) survives iff  E(z)^(2+2p) <= 0.1 a0^(3/2) / (x_c0 H0^2 sqrt(G M_b)),  i.e. below the mass
      M_*(z) = [0.1 a0^(3/2)/(x_c0 H0^2)]^2 / (G E(z)^(4+4p)),
which falls as E^-12 for p = 2 and E^-8 for p = 1.  The numeric edge below is L352's own machinery, loaded unedited: the
on-branch nu_mono profile of a point mass, x = 4 pi G (rho_dyn - rho_bar)/H(z)^2, the edge at the largest r with
x >= x_c,eff (the most favourable placement, L352 Z2).

CHECKS
  C1 CONTROL: L352's committed z = 0 edge predictions (Z6: M_b = 1e10/6e10/2e11 at x_c = 2/2.5 -> 1.11/0.99/1.73/1.55/
     2.34/2.10 Mpc) are reproduced by the closed form (1%), and L352's numeric edge machinery equals the closed form with
     the mean-density term, r_e = v_f/(H sqrt(x_c + 1.5 Omega_m(z))) (2%).  (A first version of this control compared
     the numeric edge with Z6 directly and failed by 10%: Z6 quoted the closed form without the background term, which
     moves z = 0 edges in by 10% and is < 0.4% of x_c,eff at z = 2.5.)
  C2 CONTROL: L359's gate reproduces its committed x_c,eff(z = 0.25) for all eleven cells (1e-9).
  C3 CONTROL: at the flagship masses and z = 2.5 the numeric edge agrees with the closed form, background term included
     (5%).
  E1 (reported) THE EDGE TABLE: r_e, r_flag and y_edge for L359's eight window cells, M_b = 1e10 / 1e10.5 / 1e11,
     z = 0.5 ... 4, both footings.
  F1 THE FLAGSHIP GATE for the cosmic-shear cell (p = 2, x_c0 = 2), pre-declared as in GP5 F1: the deep-MOND Tully-Fisher
     zero point at z = 2.5 stays within 0.10 dex of the framework for M_b = 1e10, 1e10.5, 1e11, both footings, both
     kernels (L320's nu_RAR and L340's nu_mono).
     HYPOTHESIS (set before the run, from the closed form): F1 FAILS at M_b = 1e11 on the canonical footing
     (r_e ~ 37 kpc < r_flag ~ 39 kpc) and passes on the alt footing -- a marginal failure at the flagship's own epoch.
  F2 (reported) for every window cell, the highest redshift z_max at which the flagship survives for all three masses,
     both footings (numeric edge, bisection).
  P1 THE GATE EXPONENT THE FLAGSHIP ALLOWS: p_max(x_c0) at z = 2.5 for M_b = 1e11 from the closed form, confirmed by the
     numeric edge (the flagship passes at p_max - 0.02 and fails at p_max + 0.02, both footings).
  O1 (informational) the observable reading: the edge in units of r(y = 1), the radius where the baryonic field equals a0,
     which high-z kinematics reach today; the gate touches deep MOND only.
MUTATE=1 removes the gate (p = 0 in every cell): the edge moves far out at z = 2.5 and F1 must PASS (inverted control,
rc = 0 for the mutated run).

SCOPE.  Isolated point-mass baryons (the record's flagship definition, L356/GP5); the switch variable on the on-branch
profile (L352's placement, the most favourable); a step switch (L352 Z2: smooth switches have no regular static edge);
the gate's power-law form E(z)^(2p) as built in L359.  This lane prices the switch only; the carrier's price at z ~ 2.5
is GP5/L356's.

Run from the repository root:  python3 real_research/dark_energy_2026/DE1_vacuum_gate_flagship.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy.optimize import brentq
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE1_vacuum_gate_flagship"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE1", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the gate is removed (p = 0 in every cell); F1 must PASS (inverted control) ***")

# ---------------------------------------------------------------------------------- L352's machinery, loaded unedited
P52 = os.path.join(REPO, "real_research", "g03_audit_2026", "L352_switch_gauss_compensation.py")
L52 = {"__name__": "l352", "__file__": P52}
_s52 = open(P52).read().split("real_mode = ")[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_s52, L52)
G, MS, MPCm, KPCm = L52["G"], L52["MS"], L52["MPCm"], L52["MPCm"] / 1e3
H0, Om, OL, rho_crit0 = L52["H0"], L52["Om"], L52["OL"], L52["rho_crit0"]
Hz, nu_mono_vec, model_M2, A0 = L52["Hz"], L52["nu_vec"], L52["model_M2"], L52["A0"]
rr = L52["rr"]
P(f"\n  L352 loaded: H0 = {H0:.4e} s^-1, Om = {Om:.4f}; kernel nu_mono; edge grid {rr[0]/KPCm:.1f} kpc - {rr[-1]/MPCm:.0f} Mpc   "
  f"[{time.time() - T0:.0f}s]")


def nu_rar(y):                                                       # L320's kernel (the flagship's default, GP5)
    return 1.0 / (1.0 - math.exp(-math.sqrt(max(y, 1e-12))))


def nu_mono(y):
    return float(nu_mono_vec(np.array([y]))[0])


# L359's gate: L347's background (Om = 0.3138, OL = 1 - Om), x_c,eff(z) = x_c0 E(z)^(2p)
OM47 = 0.3138
E2 = lambda z: OM47 * (1 + z) ** 3 + (1 - OM47)
XCEFF = lambda z, xc0, p: xc0 * E2(z) ** (0.0 if MUTATE else p)
WINDOW = [(0.5, 1.5), (0.5, 2.0), (0.5, 2.5), (1.0, 1.5), (1.0, 2.0), (1.0, 2.5), (2.0, 1.5), (2.0, 2.0)]
SHEAR_CELL = (2.0, 2.0)
MBS = (10.0, 10.5, 11.0)
FEET = ("canonical", "alt")


def r_flag(Mb, a0):
    return math.sqrt(G * Mb * MS / (0.1 * a0))


def xbar(z):
    """4 pi G rho_bar/H^2 = (3/2) Omega_m(z): the mean-density term L352's switch variable subtracts."""
    return 1.5 * Om * (1 + z) ** 3 * (H0 / Hz(z)) ** 2


def r_edge_closed(Mb, a0, z, xc0, p):
    """deep-MOND edge with the background term: v_f^2/(r H)^2 - xbar = x_c,eff."""
    vf = (G * Mb * MS * a0) ** 0.25
    return vf / (math.sqrt(XCEFF(z, xc0, p) + xbar(z)) * Hz(z))


def r_edge_numeric(Mb, a0, z, xc):
    """L352's model_M2 edge (on-branch nu_mono profile, x = 4 pi G (rho_dyn - rho_bar)/H^2 >= xc, largest r)."""
    M = Mb * MS * nu_mono_vec(G * Mb * MS / rr ** 2 / a0)
    rho_dyn = np.gradient(M, rr) / (4 * math.pi * rr ** 2)
    rho_bar = Om * rho_crit0 * (1 + z) ** 3
    on = 4 * math.pi * G * (rho_dyn - rho_bar) / Hz(z) ** 2 >= xc
    if not on.any():
        return 0.0
    it = int(np.where(on)[0].max())
    if it + 1 >= len(rr):
        return float(rr[-1])
    # interpolate the crossing in log r between the last on and first off grid point
    xa = 4 * math.pi * G * (rho_dyn[it] - rho_bar) / Hz(z) ** 2; xb = 4 * math.pi * G * (rho_dyn[it + 1] - rho_bar) / Hz(z) ** 2
    t = (math.log(xa) - math.log(xc)) / (math.log(xa) - math.log(max(xb, 1e-300))) if xb > 0 else 0.0
    return float(math.exp(math.log(rr[it]) + t * (math.log(rr[it + 1]) - math.log(rr[it]))))


def flagship_shift(Mb, foot, z, xc0, p, kernel):
    """2 log10(g_switch/g_framework) at r(g_bar = 0.1 a0): 0 inside the edge, the Newtonian value beyond it (Gauss)."""
    a0 = A0[foot]; rf = r_flag(Mb, a0); re = r_edge_numeric(Mb, a0, z, XCEFF(z, xc0, p))
    nu = nu_rar if kernel == "nu_RAR" else nu_mono
    return (0.0 if re >= rf else -2 * math.log10(nu(0.1))), re, rf


# ============================================================================================ C1-C3 controls
banner("C1-C3  CONTROLS: L352's z = 0 edges; L359's gate; closed form vs numeric at z = 2.5")
c1 = []
L352_Z6 = [(1e10, 2.0, 1.11), (1e10, 2.5, 0.99), (6e10, 2.0, 1.73), (6e10, 2.5, 1.55), (2e11, 2.0, 2.34), (2e11, 2.5, 2.10)]
xbar0 = 1.5 * Om * (1 + 0.0) ** 3 * (H0 / Hz(0.0)) ** 2                  # 4 pi G rho_bar / H^2 = (3/2) Omega_m(z)
for Mb, xc, ref in L352_Z6:
    vf = (G * Mb * MS * A0["canonical"]) ** 0.25
    rc_ = vf / (math.sqrt(xc) * Hz(0.0)) / MPCm                          # L352 Z6's own formula (no background term)
    rb_ = vf / (math.sqrt(xc + xbar0) * Hz(0.0)) / MPCm                  # with the background term L352's numeric edge carries
    rn_ = r_edge_numeric(Mb, A0["canonical"], 0.0, xc) / MPCm
    c1.append((Mb, xc, ref, rc_, rb_, rn_))
    P(f"    M_b = {Mb:.0e}, x_c = {xc}: L352 Z6 {ref:.2f} Mpc | closed form {rc_:.3f} | with background {rb_:.3f} | "
      f"L352 numeric edge {rn_:.3f}")
dev_c1a = max(abs(rc_ / ref - 1) for _, _, ref, rc_, _, _ in c1)
dev_c1b = max(abs(rn_ / rb_ - 1) for _, _, _, _, rb_, rn_ in c1)
OUT["numbers"]["C1"] = [dict(Mb=a, xc=b, l352_z6=c, closed=d, closed_bg=e, numeric=f) for a, b, c, d, e, f in c1]
check("C1 CONTROL: L352's committed z = 0 edge predictions (Z6) reproduced by the closed form (1%), and L352's numeric edge "
      "equals the closed form with the background term, r_e = v_f/(H sqrt(x_c + 1.5 Omega_m(z))) (2%)",
      f"Z6 vs closed form {dev_c1a:.2%}; numeric vs closed form with background {dev_c1b:.2%}",
      dev_c1a < 0.01 and dev_c1b < 0.02,
      "the mean-density term (3/2) Omega_m(z) moves z = 0 edges in by 10% (Z6 quoted the closed form without it); at "
      "z = 2.5 it is < 0.4% of x_c,eff for every window cell")

L359 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L359_vacuum_gated_switch_results.json")))
dev_c2 = max(abs(OM47_x - v["x_eff"]) for k_, v in L359["numbers"]["K1"].items()
             for OM47_x in [float(k_.split("/")[1]) * E2(0.25) ** float(k_.split("/")[0])])
check("C2 CONTROL: L359's gate reproduces its committed x_c,eff(z = 0.25) for all eleven cells (1e-9)",
      f"max |diff| = {dev_c2:.1e}", dev_c2 < 1e-9 or MUTATE, "the gate form and background are L359's exactly")

c3 = []
for foot in FEET:
    for lMb in MBS:
        Mb = 10 ** lMb
        rc_ = r_edge_closed(Mb, A0[foot], 2.5, *SHEAR_CELL[::-1])
        rn_ = r_edge_numeric(Mb, A0[foot], 2.5, XCEFF(2.5, SHEAR_CELL[1], SHEAR_CELL[0]))
        c3.append((foot, lMb, rc_ / KPCm, rn_ / KPCm))
dev_c3 = max(abs(n_ / c_ - 1) for _, _, c_, n_ in c3)
for foot, lMb, c_, n_ in c3:
    P(f"    z = 2.5, cell p = 2 / x_c0 = 2, {foot:9s} M_b = 1e{lMb:.1f}: r_e closed {c_:6.1f} kpc, numeric {n_:6.1f} kpc")
OUT["numbers"]["C3"] = [dict(foot=a, lMb=b, closed_kpc=c, numeric_kpc=d) for a, b, c, d in c3]
check("C3 CONTROL: at z = 2.5 the numeric edge agrees with the deep-MOND closed form (5%) at the flagship masses",
      f"max deviation {dev_c3:.2%}", dev_c3 < 0.05,
      "the closed form r_e = v_f/(sqrt(x_c,eff + 1.5 Omega_m(z)) H) is the edge law; nu_mono's finite-y correction is "
      "the residual (the background term is < 0.4% of x_c,eff for the gated cells at z = 2.5)")

# ============================================================================================ E1 edge table
banner("E1  THE EDGE TABLE: r_e / r_flag and y_edge for the eight window cells (numeric edge)")
ZS = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0)
E1 = {}
for (p, xc0) in WINDOW:
    for foot in FEET:
        a0 = A0[foot]
        for lMb in MBS:
            Mb = 10 ** lMb; rf = r_flag(Mb, a0)
            row = []
            for z in ZS:
                re = r_edge_numeric(Mb, a0, z, XCEFF(z, xc0, p))
                row.append(dict(z=z, re_kpc=re / KPCm, ratio=re / rf, y_edge=G * Mb * MS / (a0 * re ** 2) if re > 0 else float("inf")))
            E1[f"{p}/{xc0}/{foot}/{lMb}"] = row
    P(f"    p = {p:3.1f}, x_c0 = {xc0:3.1f}: r_e/r_flag (canonical, M_b = 1e11) at z = " +
      ", ".join(f"{r_['z']:.1f}: {r_['ratio']:.2f}" for r_ in E1[f"{p}/{xc0}/canonical/11.0"]))
OUT["numbers"]["E1"] = E1

# ============================================================================================ F1 flagship gate
banner("F1  THE FLAGSHIP GATE FOR THE COSMIC-SHEAR CELL (p = 2, x_c0 = 2) AT z = 2.5 (GP5's gate: |shift| <= 0.10 dex)")
F1 = []
for foot in FEET:
    for lMb in MBS:
        for kern in ("nu_RAR", "nu_mono"):
            s, re, rf = flagship_shift(10 ** lMb, foot, 2.5, SHEAR_CELL[1], SHEAR_CELL[0], kern)
            F1.append(dict(foot=foot, lMb=lMb, kernel=kern, shift_dex=s, re_kpc=re / KPCm, rflag_kpc=rf / KPCm))
            P(f"    {foot:9s} M_b = 1e{lMb:.1f} {kern:7s}: r_e = {re/KPCm:6.1f} kpc, r_flag = {rf/KPCm:5.1f} kpc -> "
              f"zero-point shift {s:+.3f} dex")
OUT["numbers"]["F1"] = F1
worst = min(r_["shift_dex"] for r_ in F1)
fails = sorted({(r_["foot"], r_["lMb"]) for r_ in F1 if abs(r_["shift_dex"]) > 0.10})
check("F1 THE FLAGSHIP (GP5's gate): with the cosmic-shear switch cell p = 2, x_c0 = 2 the deep-MOND Tully-Fisher zero "
      "point at z = 2.5 stays within 0.10 dex of the framework for M_b = 1e10-1e11, both footings, both kernels",
      f"worst shift {worst:+.3f} dex; failing (footing, log M_b): {fails if fails else 'none'}",
      abs(worst) <= 0.10,
      "beyond the switch edge Gauss leaves the baryons alone: the zero point jumps to the Newtonian value, "
      "-2 log10 nu(0.1) (the opposite sign to LCDM's +0.33)")
hyp = (("canonical", 11.0) in fails) and not any(f_ == "alt" for f_, _ in fails)
P(f"    pre-declared hypothesis (fails at 1e11 canonical only, passes alt): {'CONFIRMED' if hyp else 'NOT confirmed'}")
OUT["numbers"]["F1_hypothesis_confirmed"] = hyp

# ============================================================================================ F2 z_max per cell
banner("F2  THE HIGHEST REDSHIFT AT WHICH EACH WINDOW CELL KEEPS THE FLAGSHIP (all three masses, numeric edge)")
F2 = {}
for (p, xc0) in WINDOW:
    for foot in FEET:
        a0 = A0[foot]
        def margin(z, p=p, xc0=xc0, a0=a0):
            return min(math.log(max(r_edge_numeric(10 ** l_, a0, z, XCEFF(z, xc0, p)), 1e-30) / r_flag(10 ** l_, a0))
                       for l_ in MBS)
        if margin(0.0) < 0:
            zm = 0.0
        elif margin(12.0) > 0:
            zm = float("inf")
        else:
            zm = brentq(margin, 0.0, 12.0, xtol=1e-4)
        F2[f"{p}/{xc0}/{foot}"] = zm
    P(f"    p = {p:3.1f}, x_c0 = {xc0:3.1f}: z_max canonical {F2[f'{p}/{xc0}/canonical']:.2f}, alt {F2[f'{p}/{xc0}/alt']:.2f}")
OUT["numbers"]["F2"] = F2

# ============================================================================================ P1 p_max
banner("P1  THE GATE EXPONENT THE FLAGSHIP ALLOWS AT z = 2.5 (M_b = 1e11): closed form, confirmed numerically")
P1 = {}
ok_p1 = True
for xc0 in (1.5, 2.0, 2.5):
    for foot in FEET:
        a0 = A0[foot]; Mb = 1e11
        # closed form: r_e >= r_flag  <=>  x_c0 E2(z)^p H(z)^2 <= v_f^2/r_flag^2 = 0.1 a0^(3/2)/sqrt(G M_b)
        # (the gate's E2 is L359's background, the edge's H(z) is L352's; equal to 1e-3 -- kept exact here)
        rhs = 0.1 * a0 ** 1.5 / (xc0 * Hz(2.5) ** 2 * math.sqrt(G * Mb * MS))
        pmax_c = math.log(rhs) / math.log(E2(2.5))
        def m_(p, xc0=xc0, a0=a0):
            return math.log(max(r_edge_numeric(Mb, a0, 2.5, xc0 * E2(2.5) ** p), 1e-30) / r_flag(Mb, a0))
        pmax_n = brentq(m_, 0.0, 6.0, xtol=1e-5) if (m_(0.0) > 0 > m_(6.0)) else float("nan")
        good = m_(pmax_n - 0.02) > 0 > m_(pmax_n + 0.02) if math.isfinite(pmax_n) else False
        ok_p1 &= good and abs(pmax_n - pmax_c) < 0.1
        P1[f"{xc0}/{foot}"] = dict(pmax_closed=pmax_c, pmax_numeric=pmax_n)
        P(f"    x_c0 = {xc0}, {foot:9s}: p_max closed form {pmax_c:.3f}, numeric {pmax_n:.3f}")
OUT["numbers"]["P1"] = P1
check("P1 the flagship's bound on the gate exponent at z = 2.5 (M_b = 1e11): the closed form agrees with the numeric edge "
      "(0.1) and the numeric edge brackets it (passes at p_max - 0.02, fails at p_max + 0.02)",
      "; ".join(f"x_c0 {k_}: {v_['pmax_numeric']:.2f}" for k_, v_ in P1.items()), ok_p1 or MUTATE,
      "the flagship caps the gate exponent near 2: the construction's p = 2 cell sits on the cap")

# ============================================================================================ O1 observable reading
banner("O1  THE OBSERVABLE READING: the edge against r(y = 1), the radius high-z kinematics reach today")
O1 = []
for foot in FEET:
    a0 = A0[foot]
    for lMb in MBS:
        Mb = 10 ** lMb; r1 = math.sqrt(G * Mb * MS / a0)
        for z in (2.5, 3.0):
            re = r_edge_numeric(Mb, a0, z, XCEFF(z, SHEAR_CELL[1], SHEAR_CELL[0]))
            O1.append(dict(foot=foot, lMb=lMb, z=z, re_over_r1=re / r1, r1_kpc=r1 / KPCm))
            P(f"    {foot:9s} M_b = 1e{lMb:.1f} z = {z}: r(y=1) = {r1/KPCm:5.1f} kpc, r_e/r(y=1) = {re/r1:.2f}")
OUT["numbers"]["O1"] = O1
check("O1 (informational) with p = 2, x_c0 = 2 the edge stays beyond r(y = 1) at z = 2.5-3 for the flagship masses: "
      "the gate removes DEEP MOND only, not the transition region current z ~ 2.5 rotation curves sample",
      f"min r_e/r(y=1) = {min(o['re_over_r1'] for o in O1):.2f}", min(o["re_over_r1"] for o in O1) > 1.0,
      load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
p2 = F2.get("2.0/2.0/canonical"), F2.get("2.0/2.0/alt")
p1 = F2.get("1.0/1.5/canonical"), F2.get("1.0/1.5/alt")
P(f"""  The vacuum gate prices the flagship through one closed form: the deepest MOND acceleration visible at redshift z is
  y_edge = x_c0 (H0^2/a0^1.5) sqrt(G M_b) E(z)^(2+2p).  For the cosmic-shear cell (p = 2, x_c0 = 2) the flagship
  (y = 0.1) survives for all three masses only to z = {p2[0]:.2f} (canonical) / {p2[1]:.2f} (alt); at z = 2.5 the worst shift is
  {worst:+.2f} dex (the Newtonian value, beyond the edge).  For p = 1, x_c0 = 1.5 it survives to z = {p1[0]:.2f} / {p1[1]:.2f}.
  The flagship caps the gate exponent at p_max ~ {P1['2.0/canonical']['pmax_numeric']:.2f} (x_c0 = 2, canonical) at z = 2.5.
  Above the cap the gate turns the framework's flat-a0 prediction into a Newtonian outer disc at high z: distinctive, but
  not the flagship.  The gate touches deep MOND only; today's z ~ 2.5 kinematics (r <~ r(y = 1)) are inside the edge.
  Whether ANY gate exponent serves cosmic shear (z = 0.5), KiDS (z = 0.25) and the flagship (z = 2.5) together is DE2.""")

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail
OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
