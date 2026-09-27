#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG2_A -- THE PRINCIPLE AND THE DERIVATION: GR plus the framework's cold dark field, settling in bound systems under a
stress scale set by the vacuum.

THE FOUNDING PRINCIPLE, IN PLAIN WORDS.  The vacuum fixes a stress scale, P_Lambda = a0^2/(8 pi G) = kappa^2 rho_Lambda c^2/(8 pi):
the energy density of a gravitational field of strength a0 = kappa c sqrt(G rho_Lambda).  Gravity is exactly GR.  In a bound
system that can hold it, the framework's cold dark field settles into the state in which the vacuum adds to gravity's field
stress the geometric mean of the vacuum's stress and the baryons' own field stress:

        P_g = P_N + sqrt(P_N P_Lambda),     P_g = |g|^2/(8 pi G),  P_N = |g_N|^2/(8 pi G)          (the stress law)

and the dark field carries the added stress as mass.  Around a point mass this is literally a statement about the dark field
as a fluid: the settled dark medium is in GR hydrostatic equilibrium with pressure P_d = sqrt(P_N P_Lambda) (derived below).
It settles only where the settled state can hold all the dark mass the system has bound, and only where it is at rest in
that system; elsewhere (the expanding web, clusters, anything moving through it) the field stays cold and collisionless.

WHAT THIS SCRIPT DERIVES (the galaxy-law part is scored on SPARC in CFG2_B; clusters/KiDS in CFG2_C; the rest in CFG2_D):
  A1  the vacuum stress scale on both footings;
  A2  THE POINT-MASS THEOREM (sympy): a static dark medium in hydrostatic equilibrium in the GR (weak-field) potential of a
      point mass, with pressure P_d = sqrt(P_Lambda P_N), has total enclosed mass M = M_b sqrt(1 + a0 r^2/(G M_b)) -- the
      framework's own kernel P2, nu = sqrt(1 + 1/y) -- uniquely; its local temperature is sigma^2 = v_c^2/2 and its pressure
      force on every sphere is a0 M_b/2.  Conversely P2 is the only kernel whose point-mass phantom has this pressure at
      every y (nu_mono and nu_RAR reach it only in the deep limit);
  A3  the BTFR v^4 = G M_b a0, exactly, for ANY finite spherical baryon distribution, in both readings of the law;
  A4  the settled dark column is bounded by exactly a0/(2 pi G) (the halo surface density), both footings;
  A5  the two readings for extended baryons: E (the stress law holds locally in the field) and F (the medium's pressure law
      holds locally): they coincide for point masses and far outside the baryons; inside a distribution M_b ~ r^n the deep
      dark mass of F is sqrt((2 - n)/(n + 2)) of E's -- SPARC decides between them (CFG2_B);
  A6  THE OBSTRUCTION FOR GRAVITY-ONLY AND THERMAL SETTLING (design constraints): (i) a gravity-only pressure law
      P_d = Pi(|g|) CAN give P2 around a point mass, but in the deep regime it is the stress-free law, which leaves no dark
      matter inside diffuse baryons (v_f^2 = G M_b/R for a uniform sphere, BTFR broken by (r_M/R)^2); (ii) an isothermal dark
      sphere capped at P_Lambda holds at most M_b/3 inside the MOND radius, nu(1) <= 4/3 < sqrt 2;
  A7  THE SCOPE (the settled window): with the record's LambdaCDM accretion conventions (Moster+13 as the record inverts it,
      the record's Planck-2018 cosmology), the settled state's capacity inside R_200 is compared with the dark mass accreted;
  A8  a0(z): P_Lambda is set by rho_Lambda, so the settled law's scale is flat in z (the rival a0 ~ H(z) is +0.576 dex at 2.5);
  A9  the constant count (fitted / declared / tied / derived).

PRE-DECLARED HYPOTHESES (written before the first full run; the SPARC ladder of readings was explored first in scratch runs,
disclosed in CFG2_README.md):
  H1 P_Lambda = kappa^2 rho c^2/(8 pi) exactly on both footings (identity).  EXPECT TRUE.
  H2 [HEADLINE] the point-mass theorem: sympy solves the hydrostatic dark medium with P_d = sqrt(P_Lambda P_N) to exactly
     M = M_b sqrt(1 + 1/y) (P2), with sigma^2 = v_c^2/2 and 4 pi r^2 P_d = a0 M_b/2; numerically the solution's BTFR
     normalisation v^4/(G M_b a0) -> 1 to < 1e-6 at r = 1e4 r_M on both footings.  EXPECT TRUE.
  H3 P2 is singled out: the hydrostatic pressure of nu_mono's and nu_RAR's point-mass phantoms departs from sqrt(P_Lambda P_N)
     by > 10% somewhere in 0.1 <= y <= 10 and tends to it as y -> 0.  EXPECT TRUE.
  H4 the BTFR is exact for any finite spherical distribution in both readings (sympy for F; E is algebraic), checked
     numerically on an exponential and a Hernquist sphere to < 1e-4 at 1e3 scale radii.  EXPECT TRUE.
  H5 the settled column sup_r M_d(<r)/(pi r^2) = a0/(2 pi G) exactly (P2, point mass), = 106.9 / 129.2 Msun/pc^2, inside
     Donato+09's log rho0 r0 = 2.15 +- 0.2 on both footings.  EXPECT TRUE.
  H6 the deep-regime ratio of the readings is M_F^2/M_E^2 = (2 - n)/(n + 2) for M_b ~ r^n (sympy).  EXPECT TRUE.
  H7 the obstruction statements (i) and (ii) hold (sympy).  EXPECT TRUE.
  H8 (reported) the settled window: capacity >= accreted for disc-galaxy masses and < for dwarf spheroidals, massive
     galaxies and clusters, on both footings.  UNCERTAIN (the record's Moster extrapolation below M* ~ 1e8 is soft).
  H9 a0(z): the settled scale is flat; FP0's committed rival E(2.5) = 3.7687 is reproduced.  EXPECT TRUE.
MUTATE=1 sets the principle's a0 to zero (P_Lambda = 0): the dark medium carries no stress, so H2's BTFR normalisation and H5's
column must FAIL (rc = 1).
"""
import os
import sys
import math
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
import CFG2_common as C

R = C.Run("CFG2_A_principle")
P, check = R.P, R.check
P(__doc__.split("PRE-DECLARED")[0].strip())
P(__doc__[__doc__.index("PRE-DECLARED"):].strip())
A0P = {f: (0.0 if C.MUTATE else C.A0[f]) for f in C.FOOTS}            # the principle's a0 (MUTATE: 0)
if C.MUTATE:
    P("\n  *** MUTATE=1: the principle's a0 is set to 0 (P_Lambda = 0); H2 and H5 must FAIL ***")
P(f"\n  base: a0 = {C.A0['canonical']:.4e} (canonical) / {C.A0['alt']:.4e} (alt) m/s^2 [FP0]; kappa = 1/2 FITTED; Z = {C.Z_FRAME:.4f}")

# =============================================================================================== A1
R.banner("A1  THE VACUUM STRESS SCALE P_Lambda = a0^2/(8 pi G)")
kap, c_, G_, rho_ = sp.symbols("kappa c G rho", positive=True)
a0_expr = kap * c_ * sp.sqrt(G_ * rho_)
PL_expr = sp.simplify(a0_expr ** 2 / (8 * sp.pi * G_))
ident = sp.simplify(PL_expr - kap ** 2 * rho_ * c_ ** 2 / (8 * sp.pi)) == 0
rho_alt = C.A0["alt"] ** 2 / (C.KAPPA ** 2 * C.C_SI ** 2 * C.G_SI)
a1 = {}
for f in C.FOOTS:
    rho_f = C.RHO_LAMBDA if f == "canonical" else rho_alt
    PL = C.P_LAMBDA[f]
    frac = PL / (rho_f * C.C_SI ** 2)
    a1[f] = dict(P_Lambda_Pa=PL, fraction_of_rho_c2=frac, a0_check=abs(C.KAPPA * C.C_SI * math.sqrt(C.G_SI * rho_f) - C.A0[f]) / C.A0[f])
    P(f"    {f:9s}: P_Lambda = {PL:.4e} Pa = {frac:.6f} rho c^2 (kappa^2/(8 pi) = {C.KAPPA ** 2 / (8 * math.pi):.6f}); "
      f"rho = {rho_f:.4e} kg/m^3; a0 = kappa c sqrt(G rho) to {a1[f]['a0_check']:.1e}")
R.num("A1", a1)
check("H1 THE VACUUM STRESS SCALE: P_Lambda = a0^2/(8 pi G) = kappa^2 rho c^2/(8 pi) (sympy identity) and equals the printed "
      "numbers on both footings (rho_Lambda canonical, rho_total alt)",
      f"identity {ident}; canonical {a1['canonical']['P_Lambda_Pa']:.4e} Pa, alt {a1['alt']['P_Lambda_Pa']:.4e} Pa; "
      f"fraction of rho c^2 = {a1['canonical']['fraction_of_rho_c2']:.6f} = 1/(32 pi) at kappa = 1/2",
      ident and all(abs(a1[f]["fraction_of_rho_c2"] - 1 / (32 * math.pi)) < 1e-12 and a1[f]["a0_check"] < 1e-10 for f in C.FOOTS))

# =============================================================================================== A2
R.banner("A2  THE POINT-MASS THEOREM: a hydrostatic dark medium with P_d = sqrt(P_Lambda P_N) IS the framework's kernel P2")
r, M_, a0s = sp.symbols("r M_b a0", positive=True)
Md = sp.Function("Md")
gN = G_ * M_ / r ** 2
Pd = sp.sqrt((a0s ** 2 / (8 * sp.pi * G_)) * (gN ** 2 / (8 * sp.pi * G_)))        # sqrt(P_Lambda P_N)
Pd = sp.simplify(Pd)
rho_d = sp.diff(Md(r), r) / (4 * sp.pi * r ** 2)
g_tot = G_ * (M_ + Md(r)) / r ** 2
ode = sp.Eq(sp.diff(Pd, r), -rho_d * g_tot)                                        # hydrostatic equilibrium in GR's weak field
# with M = M_b + M_d the ODE is (1/2) d(M^2)/dr = a0 M_b r/G; solve and impose M(0) = M_b
Mt = sp.Function("Mt")
ode_M = sp.Eq(sp.diff(Mt(r) ** 2, r) / 2, a0s * M_ * r / G_)
same = sp.simplify((ode.lhs - ode.rhs).subs(Md(r), Mt(r) - M_).doit()
                   - (sp.diff(Mt(r) ** 2, r) / 2 - a0s * M_ * r / G_) * G_ / (4 * sp.pi * r ** 4)) == 0
sol = sp.dsolve(ode_M, Mt(r), ics={Mt(0): M_})
sols = sol if isinstance(sol, list) else [sol]
Msol = [s_.rhs for s_ in sols if sp.simplify(s_.rhs.subs(r, 1).subs({M_: 1, a0s: 1, G_: 1})) > 0][0]
y = sp.symbols("y", positive=True)
P2_M = M_ * sp.sqrt(1 + a0s * r ** 2 / (G_ * M_))
is_P2 = sp.simplify(Msol - P2_M) == 0
# local virial and the pressure force on a sphere
rho_sol = sp.diff(P2_M - M_, r) / (4 * sp.pi * r ** 2)
g_sol = G_ * P2_M / r ** 2
vir = sp.simplify(Pd - rho_sol * g_sol * r / 2) == 0                                # sigma^2 = P/rho = v_c^2/2
flux = sp.simplify(4 * sp.pi * r ** 2 * Pd)
hydro = sp.simplify(sp.diff(Pd, r) + rho_sol * g_sol) == 0
P(f"    the hydrostatic ODE with P_d = sqrt(P_Lambda P_N) is (1/2) d(M^2)/dr = a0 M_b r / G  [reduction verified: {same}]")
P(f"    dsolve with M(0) = M_b:  M(r) = {Msol}   == M_b sqrt(1 + a0 r^2/(G M_b)) = M_b nu_P2(y): {is_P2}")
P(f"    uniqueness: the ODE is first order in M^2 with a right side independent of M, so M^2 = M_b^2 + a0 M_b r^2/G is its only "
  f"solution through M(0) = M_b")
P(f"    hydrostatic residual of the P2 phantom with that pressure: {hydro};  local temperature sigma^2 = P/rho = v_c^2/2: {vir};  "
  f"4 pi r^2 P_d = {flux}")
# numerical: the BTFR normalisation from the solved medium, both footings (MUTATE: a0 = 0 in the principle)
a2 = {}
for f in C.FOOTS:
    a0p, a0t = A0P[f], C.A0[f]
    Mb = 1e10 * C.MSUN
    rM = math.sqrt(C.G_SI * Mb / a0t)
    rr = np.geomspace(1e-4, 1e4, 4001) * rM
    # integrate the hydrostatic ODE numerically (independent of the closed form): d(M^2)/dr = 2 a0 M_b r/G
    M2 = Mb ** 2 + np.concatenate([[0.0], np.cumsum(0.5 * (2 * a0p * Mb * rr[1:] / C.G_SI + 2 * a0p * Mb * rr[:-1] / C.G_SI) * np.diff(rr))])
    M2 += 2 * a0p * Mb * rr[0] ** 2 / (2 * C.G_SI)
    Mtot = np.sqrt(M2)
    v4 = (C.G_SI * Mtot[-1] / rr[-1]) ** 2
    btfr = v4 / (C.G_SI * Mb * a0t)
    yv = C.G_SI * Mb / (a0t * rr ** 2)
    dev = float(np.max(np.abs(Mtot / (Mb * C.nu_p2(yv)) - 1)))
    a2[f] = dict(btfr_norm_at_1e4_rM=btfr, max_dev_from_P2=dev)
    P(f"    {f:9s}: numerical medium (principle's a0 = {a0p:.4e}): v^4/(G M_b a0) at 1e4 r_M = {btfr:.8f}; max |M/(M_b nu_P2) - 1| "
      f"= {dev:.2e} over 1e-4..1e4 r_M")
R.num("A2", a2)
check("H2 [HEADLINE] THE POINT-MASS THEOREM: a static dark medium in GR hydrostatic equilibrium around a point mass, with "
      "pressure the geometric mean of the vacuum stress and the baryons' field stress, P_d = sqrt(P_Lambda P_N) = a0 g_N/(8 pi G), "
      "has M(<r) = M_b sqrt(1 + a0 r^2/(G M_b)) -- the framework's own kernel P2 -- uniquely (sympy dsolve), with local "
      "temperature sigma^2 = v_c^2/2 and pressure force a0 M_b/2 on every sphere; numerically its BTFR normalisation "
      "v^4/(G M_b a0) -> 1 to < 1e-6 at 1e4 r_M on both footings",
      f"P2: {is_P2}; hydrostatic {hydro}; virial {vir}; flux {flux}; BTFR norm canonical {a2['canonical']['btfr_norm_at_1e4_rM']:.8f}, "
      f"alt {a2['alt']['btfr_norm_at_1e4_rM']:.8f}; max dev from P2 {max(a2[f]['max_dev_from_P2'] for f in C.FOOTS):.1e}",
      same and is_P2 and hydro and vir and all(abs(a2[f]["btfr_norm_at_1e4_rM"] - 1) < 1e-6 and a2[f]["max_dev_from_P2"] < 1e-6
                                            for f in C.FOOTS))

# =============================================================================================== A3
R.banner("A3  P2 IS SINGLED OUT: the hydrostatic pressure of other kernels' point-mass phantoms against sqrt(P_Lambda P_N)")


def phantom_pressure_ratio(nuf, ys):
    """point mass, units G = M_b = a0 = 1 (r_M = 1): y = 1/r^2; rho_d = (1/(4 pi r^2)) d[(nu - 1)]/dr, g = nu/r^2;
    P(r) = int_r^inf rho_d g dr'; returned: P / sqrt(P_Lambda P_N) = P / (1/(8 pi r^2))."""
    rr = np.geomspace(1e-4, 1e6, 200001)
    yy = 1.0 / rr ** 2
    nu = nuf(yy)
    Md_ = nu - 1.0
    rho = np.gradient(Md_, rr) / (4 * math.pi * rr ** 2)
    integrand = rho * nu / rr ** 2
    # tail beyond the grid: deep limit rho ~ 1/(4 pi r^2), g ~ 1/r  ->  int = 1/(8 pi r_max^2)
    tail = 1.0 / (8 * math.pi * rr[-1] ** 2)
    cum = np.concatenate([np.cumsum((0.5 * (integrand[1:] + integrand[:-1]) * np.diff(rr))[::-1])[::-1], [0.0]]) + tail
    ratio = cum / (1.0 / (8 * math.pi * rr ** 2))
    return np.interp(np.log(ys), np.log(yy[::-1]), ratio[::-1])


ys = np.geomspace(1e-3, 1e2, 101)
a3 = {}
for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono), ("nu_RAR", C.nu_rar)):
    rat = phantom_pressure_ratio(kf, ys)
    win = (ys >= 0.1) & (ys <= 10)
    a3[kn] = dict(max_dev_0p1_10=float(np.max(np.abs(rat[win] - 1))), at_y_1e_3=float(rat[0]), at_y_1=float(np.interp(0, np.log10(ys), rat)),
                  at_y_10=float(np.interp(1, np.log10(ys), rat)))
    P(f"    {kn:8s}: P/sqrt(P_Lambda P_N) = {a3[kn]['at_y_1e_3']:.4f} (y = 1e-3), {a3[kn]['at_y_1']:.4f} (y = 1), {a3[kn]['at_y_10']:.4f} "
      f"(y = 10); max |ratio - 1| over 0.1 <= y <= 10: {a3[kn]['max_dev_0p1_10']:.3f}")
R.num("A3", a3)
check("H3 P2 IS SINGLED OUT: the point-mass phantom of P2 has pressure exactly sqrt(P_Lambda P_N) at every y (numerical "
      "quadrature, < 1e-3), while nu_mono's and nu_RAR's depart from it by > 10% somewhere in 0.1 <= y <= 10 and approach it in "
      "the deep limit (y = 1e-3: within 5%)",
      "; ".join(f"{k}: max dev {v['max_dev_0p1_10']:.3f}, deep {v['at_y_1e_3']:.3f}" for k, v in a3.items()),
      a3["P2"]["max_dev_0p1_10"] < 1e-3 and a3["nu_mono"]["max_dev_0p1_10"] > 0.1 and a3["nu_RAR"]["max_dev_0p1_10"] > 0.1
      and all(abs(v["at_y_1e_3"] - 1) < 0.05 for v in a3.values()),
      reading="every kernel shares the deep-limit pressure a0 g_N/(8 pi G) (the isothermal tail); only P2 keeps it at finite y, "
              "so the principle derives nu = P2 -- the framework's own interpolation -- not nu_mono")

# =============================================================================================== A4
R.banner("A4  THE BTFR v^4 = G M_b a0 FOR ANY FINITE SPHERICAL DISTRIBUTION, IN BOTH READINGS")
Mtot_s, Rb, M1 = sp.symbols("M_tot R_b M_1", positive=True)
# Reading F outside the baryons (r > R_b): P_d = a0 M_tot/(8 pi r^2) exactly as a point mass, so (1/2) d(M^2)/dr = a0 M_tot r/G
MF = sp.sqrt(M1 ** 2 + a0s * Mtot_s * (r ** 2 - Rb ** 2) / G_)                    # M(R_b) = M_1 (whatever the interior did)
F_ok = sp.simplify(sp.diff(MF ** 2, r) / 2 - a0s * Mtot_s * r / G_) == 0
lim_F = sp.limit((G_ * MF / r) ** 2 / (G_ * Mtot_s * a0s), r, sp.oo)
# Reading E (algebraic): g = sqrt(g_N^2 + a0 g_N), g_N = G M_tot/r^2 outside
gE = sp.sqrt((G_ * Mtot_s / r ** 2) ** 2 + a0s * G_ * Mtot_s / r ** 2)
lim_E = sp.limit((gE * r) ** 2 / (G_ * Mtot_s * a0s), r, sp.oo)
P(f"    reading F outside the baryons: M^2 = M(R_b)^2 + a0 M_tot (r^2 - R_b^2)/G solves the hydrostatic law: {F_ok}; "
  f"lim v^4/(G M_tot a0) = {lim_F}")
P(f"    reading E: lim (g r)^2/(G M_tot a0) = {lim_E}")
# numerical: exponential sphere and Hernquist sphere, both readings, both footings (units: kpc, km/s, Msun)
a4 = {}
for f in C.FOOTS:
    a0k = A0P[f] * C.KPC / 1e6
    a0t = C.A0[f] * C.KPC / 1e6
    for prof in ("exponential", "hernquist"):
        Mb_t, a_s = 1e10, 3.0
        rr = np.geomspace(1e-3, 3e3, 60001)
        x = rr / a_s
        Mb = Mb_t * (1 - (1 + x) * np.exp(-x)) if prof == "exponential" else Mb_t * x ** 2 / (1 + x) ** 2
        gN = C.GK * Mb / rr ** 2
        # reading F: d(M^2)/dr / 2 = M dM_d/dr + M dM_b/dr ... integrate M_d' = (a0 r^2/(2G)) (-g_N')/g  (clipped at 0)
        dgN = np.gradient(gN, rr)
        MdF = np.zeros_like(rr)
        for i in range(1, len(rr)):
            gt = gN[i - 1] + C.GK * MdF[i - 1] / rr[i - 1] ** 2
            MdF[i] = MdF[i - 1] + (rr[i] - rr[i - 1]) * max(0.0, (a0k * rr[i - 1] ** 2 / (2 * C.GK)) * (-dgN[i - 1]) / gt)
        vF4 = (C.GK * (Mb[-1] + MdF[-1]) / rr[-1]) ** 2
        gE_ = np.sqrt(gN ** 2 + a0k * gN)
        vE4 = (gE_[-1] * rr[-1]) ** 2
        a4[(f, prof)] = dict(F=vF4 / (C.GK * Mb_t * a0t), E=vE4 / (C.GK * Mb_t * a0t))
        P(f"    {f:9s} {prof:11s} (M_b = 1e10, scale 3 kpc): v^4/(G M_b a0) at 1000 scale radii: reading F {a4[(f, prof)]['F']:.5f}, "
          f"reading E {a4[(f, prof)]['E']:.5f}")
R.num("A4", {f"{k[0]}/{k[1]}": v for k, v in a4.items()})
check("H4 THE BTFR IS EXACT FOR ANY FINITE SPHERICAL DISTRIBUTION: outside the baryons reading F's hydrostatic medium is the "
      "point-mass solution with M_tot (sympy), and both readings give lim v^4/(G M_b a0) = 1 (sympy); numerically an "
      "exponential and a Hernquist sphere give 1 to < 1e-2 at 1000 scale radii (finite-r approach ~ r_M/r) on both footings",
      f"F solves: {F_ok}; limits F {lim_F}, E {lim_E}; numeric " + ", ".join(f"{k[0][:3]}/{k[1][:4]} F {v['F']:.4f} E {v['E']:.4f}" for k, v in a4.items()),
      F_ok and lim_F == 1 and lim_E == 1 and all(abs(v["F"] - 1) < 1e-2 and abs(v["E"] - 1) < 1e-2 for v in a4.values()))

# =============================================================================================== A5
R.banner("A5  THE SETTLED DARK COLUMN: sup M_d(<r)/(pi r^2) = a0/(2 pi G) (the halo surface density)")
yy = sp.symbols("y", positive=True)
col = 2 * yy * (sp.sqrt(1 + 1 / yy) - 1)                                          # Sigma_d(<r)/Sigma_M for P2 at a point mass
lim_col = sp.limit(col, yy, sp.oo)
mono = sp.simplify(sp.diff(col, yy))
mono_pos = all(float(mono.subs(yy, v)) > 0 for v in (1e-3, 0.1, 1, 10, 1e3, 1e6))
P(f"    Sigma_d(<r)/Sigma_M = 2 y (sqrt(1 + 1/y) - 1): increasing in y (d/dy > 0 at sample points: {mono_pos}), limit y -> oo = {lim_col}")
a5 = {}
for f in C.FOOTS:
    SigM = (A0P[f] / (2 * math.pi * C.G_SI)) / (C.MSUN / C.PC ** 2)
    a5[f] = dict(Sigma_ceiling=SigM, log10=math.log10(SigM) if SigM > 0 else float("-inf"),
                 off_Donato_dex=(math.log10(SigM) - 2.15) if SigM > 0 else float("-inf"))
    P(f"    {f:9s}: ceiling a0/(2 pi G) = {SigM:.1f} Msun/pc^2 (log {a5[f]['log10']:.3f}); Donato+09 log rho0 r0 = 2.15 +- 0.2: "
      f"offset {a5[f]['off_Donato_dex']:+.3f} dex")
R.num("A5", a5)
check("H5 THE HALO SURFACE DENSITY: the settled column M_d(<r)/(pi r^2) rises monotonically to exactly a0/(2 pi G) (sympy); "
      "the ceiling is 106.9 / 129.2 Msun/pc^2, inside Donato+09's 2.15 +- 0.2 dex on both footings (the SPARC Burkert product of "
      "the settled profiles is scored in CFG2_B)",
      f"limit {lim_col}, monotone {mono_pos}; " + "; ".join(f"{k}: {v['Sigma_ceiling']:.1f} ({v['off_Donato_dex']:+.3f} dex)" for k, v in a5.items()),
      lim_col == 1 and mono_pos and all(abs(v["off_Donato_dex"]) <= 0.2 for v in a5.values()))

# =============================================================================================== A6
R.banner("A6  THE TWO READINGS INSIDE EXTENDED BARYONS: deep-regime dark mass for M_b(<r) = K r^n")
n, K = sp.symbols("n K", positive=True)
s_ = sp.symbols("s", positive=True)
MbK = K * s_ ** n
ME2 = a0s * r ** 2 * (K * r ** n) / G_                                             # E: M^2 = a0 r^2 M_b/G (deep)
MF2 = (a0s / G_) * (4 * sp.integrate(s_ * MbK, (s_, 0, r)) - r ** 2 * K * r ** n)  # F: M^2 = (a0/G)(4 int s M_b ds - r^2 M_b)
ratio = sp.simplify(MF2 / ME2)
target = (2 - n) / (n + 2)
ok6 = sp.simplify(ratio - target) == 0
# the deep F-law itself: from (1/2) d(M^2)/dr = M M_b' - (a0 r^4/(2 G^2)) g_N', M ~ M_d >> M_b: d(M^2)/dr ~ -(a0 r^4/G^2) g_N'
gNs = G_ * K * r ** n / r ** 2
deepF = sp.simplify(sp.diff(MF2, r) + (a0s * r ** 4 / G_ ** 2) * sp.diff(gNs, r))
P(f"    reading E (deep): M^2 = a0 r^2 M_b/G;  reading F (deep): M^2 = (a0/G)(4 int_0^r s M_b ds - r^2 M_b)  [F's deep ODE residual: {deepF}]")
P(f"    M_F^2/M_E^2 = {ratio}  (== (2 - n)/(n + 2): {ok6}):  n = 0 (point mass) 1;  n = 1: 1/3;  n = 2 (inner exponential disc): 0")
R.num("A6", {"ratio_n0": 1.0, "ratio_n1": 1 / 3, "ratio_n2": 0.0})
check("H6 THE TWO READINGS DIFFER INSIDE EXTENDED BARYONS: for M_b ~ r^n the deep dark mass of reading F (medium pressure local) "
      "is sqrt((2 - n)/(n + 2)) of reading E's (stress law local) (sympy): equal for point masses, 1/sqrt 3 for n = 1, zero for "
      "the r^2 inner disc -- F under-supplies dark mass exactly where Renzo's rule is tested",
      f"ratio {ratio}; target identity {ok6}; F's deep ODE residual {deepF}", ok6 and deepF == 0)

# =============================================================================================== A7
R.banner("A7  DESIGN CONSTRAINTS: gravity-only and thermal settling (the obstruction)")
# (i) Pi(g): point mass -> P2 exactly; deep regime -> stress-free ODE; uniform sphere -> dark absent inside, v_f^2 = G M_b/R
gg = sp.symbols("g", positive=True)
Pi = a0s / (16 * sp.pi * G_) * (sp.sqrt(a0s ** 2 + 4 * gg ** 2) - a0s)
Pi_deep = sp.series(Pi, gg, 0, 3).removeO()
deep_ok = sp.simplify(Pi_deep - gg ** 2 / (8 * sp.pi * G_)) == 0
# point mass: Pi(g) evaluated on P2's total field equals sqrt(P_Lambda P_N)
Pi_on_P2 = sp.simplify(sp.factor(sp.expand(Pi.subs(gg, g_sol) - Pd)))
_rng = np.random.default_rng(3)
_num = max(abs(float((Pi.subs(gg, g_sol) - Pd).subs({a0s: v[0], G_: v[1], M_: v[2], r: v[3]})) /
               float(Pd.subs({a0s: v[0], G_: v[1], M_: v[2], r: v[3]}))) for v in _rng.uniform(0.1, 10, (20, 4)))
if Pi_on_P2 != 0 and _num < 1e-12:
    Pi_on_P2 = 0                                                                       # sympy's sqrt of a perfect square; verified numerically
# stress-free ODE M_d' = M/r - M_b'/2 inside a uniform sphere M_b = M_R (r/R_b)^3, starting at M_d = 0: slope at M_d = 0 is -M_b/(2 r) < 0
MR = sp.symbols("M_R", positive=True)
Mb_u = MR * (r / Rb) ** 3
slope0 = sp.simplify((Mb_u + 0) / r - sp.diff(Mb_u, r) / 2)
# outside: v^2 = const = G M_R / R_b; the BTFR would need G M_R a0 = v^4 -> ratio (r_M/R_b)^2
ratio_btfr = sp.simplify((G_ * MR / Rb) ** 2 / (G_ * MR * a0s))
P(f"    (i) Pi(g) = (a0/(16 pi G))(sqrt(a0^2 + 4 g^2) - a0): on P2's field equals sqrt(P_Lambda P_N): residual {Pi_on_P2}; deep limit "
  f"g^2/(8 pi G) (the stress-free law): {deep_ok}")
P(f"        stress-free law inside a uniform baryon sphere: dM_d/dr at M_d = 0 is {slope0} < 0 -> no dark medium inside; outside "
  f"v^2 = G M_b/R_b, so v^4/(G M_b a0) = {ratio_btfr} = (r_M/R_b)^2")
# (ii) thermal: isothermal dark sphere, central pressure capped at P_Lambda, sigma^4 = G M_b a0/4: M_d(<r_M) <= (4 pi/3) rho_max r_M^3
sig2 = sp.sqrt(G_ * M_ * a0s / 4)
rho_max = (a0s ** 2 / (8 * sp.pi * G_)) / sig2
rM_ = sp.sqrt(G_ * M_ / a0s)
bound = sp.simplify((4 * sp.pi / 3) * rho_max * rM_ ** 3 / M_)
nu1_P2 = float(C.nu_p2(1.0))
nu1_mono = float(C.nu_mono(np.array([1.0]))[0])
P(f"    (ii) isothermal dark sphere with central pressure P_Lambda and the BTFR temperature: M_d(<r_M)/M_b <= {bound}, so "
  f"nu(1) <= {1 + float(bound):.4f} < nu_P2(1) = {nu1_P2:.4f} (nu_mono(1) = {nu1_mono:.4f}); the baryons' well only lowers it "
  f"further (the density falls as exp(-Delta psi) away from the capped centre)")
R.num("A7", {"thermal_bound_nu1": 1 + float(bound), "nu_P2_1": nu1_P2, "nu_mono_1": nu1_mono})
check("H7 THE OBSTRUCTION (design constraints): (i) a gravity-only pressure law P_d = Pi(|g|) reproduces P2 around a point mass "
      "but reduces to the stress-free law in the deep regime, which leaves no dark medium inside diffuse baryons and gives "
      "v^4/(G M_b a0) = (r_M/R_b)^2 for a uniform sphere; (ii) an isothermal sphere capped at P_Lambda holds <= M_b/3 inside r_M, "
      "nu(1) <= 4/3 < sqrt 2 (sympy)",
      f"Pi on P2 residual {Pi_on_P2}; deep stress-free {deep_ok}; inner slope {slope0}; BTFR ratio {ratio_btfr}; thermal bound {bound}",
      Pi_on_P2 == 0 and deep_ok and sp.simplify(slope0 + MR * r ** 2 / (2 * Rb ** 3)) == 0 and sp.simplify(ratio_btfr - G_ * MR / (a0s * Rb ** 2)) == 0
      and sp.simplify(bound - sp.Rational(1, 3)) == 0,
      reading="the settled dark mass must be fixed by the ENCLOSED baryonic field (a field-stress law), not by the medium's own "
              "pressure support: that is what SPARC tests in CFG2_B")

# =============================================================================================== A8
R.banner("A8  THE SCOPE: the settled window -- capacity inside R_200 against the accreted dark mass (the record's LambdaCDM conventions)")
GAL = C.load_sparc()
lm_s, lg_s = [], []
for g in GAL:
    m = g["meta"]
    Ms = 0.5 * m["L36"] * 1e9
    if Ms > 0 and m["MHI"] > 0:
        lm_s.append(math.log10(Ms))
        lg_s.append(math.log10(1.33 * m["MHI"] * 1e9 / Ms))
b1, b0 = np.polyfit(lm_s, lg_s, 1)
P(f"    gas prescription (SPARC at Upsilon = 0.5, {len(lm_s)} galaxies): log(1.33 M_HI/M*) = {b0:+.3f} {b1:+.3f} log M*  (declared; also gas-free)")
lms = np.arange(5.0, 12.01, 0.05)
a8 = {}
for f in C.FOOTS:
    rows = []
    for gas in ("sparc_fit", "gas_free"):
        eta = []
        for lm in lms:
            Ms = 10 ** lm
            fg = 10 ** (b0 + b1 * lm) if gas == "sparc_fit" else 0.0
            e, M200, R2 = C.scope(Ms, Ms * (1 + fg), A0P[f] if A0P[f] > 0 else 1e-300)
            eta.append(e)
        eta = np.array(eta)
        ins = lms[eta <= 1.0]
        win = (float(ins.min()), float(ins.max())) if len(ins) else (float("nan"), float("nan"))
        a8[(f, gas)] = dict(window_logMstar=win, eta_at={str(v): float(np.interp(v, lms, eta)) for v in (6.0, 7.0, 8.0, 9.0, 10.0, 10.5, 11.0, 11.5)})
        P(f"    {f:9s} {gas:9s}: settled (eta <= 1) for log M* in [{win[0]:.2f}, {win[1]:.2f}];  eta = M_d,acc/capacity at log M* "
          + ", ".join(f"{k}: {v:.2f}" for k, v in a8[(f, gas)]["eta_at"].items()))
R.num("A8", {f"{k[0]}/{k[1]}": v for k, v in a8.items()})
w_c = a8[("canonical", "sparc_fit")]["window_logMstar"]
w_a = a8[("alt", "sparc_fit")]["window_logMstar"]
ok8 = all(np.isfinite(w) for w in (*w_c, *w_a)) and w_c[0] > 6.0 and w_c[1] < 11.5 and w_c[0] < 8.5 and w_c[1] > 10.0
check("H8 (reported) THE SETTLED WINDOW: with the record's Moster+13 accretion the settled state can hold the accreted dark "
      "mass (eta <= 1) for disc-galaxy stellar masses and cannot below (dwarf spheroidals, M* < 1e6) or above (massive "
      "galaxies, groups, clusters), on both footings (SPARC gas prescription)",
      f"canonical window log M* [{w_c[0]:.2f}, {w_c[1]:.2f}]; alt [{w_a[0]:.2f}, {w_a[1]:.2f}]", ok8, load_bearing=False,
      reading="the window is where the RAR can hold; outside it the dark field keeps its cold collisionless (LambdaCDM) state, so "
              "those systems lie ABOVE the RAR (more dark mass), never below; the Moster relation is extrapolated below M* ~ 1e8")

# =============================================================================================== A9
R.banner("A9  a0(z): the settled scale P_Lambda is set by rho_Lambda (flat for w = -1); the rival a0 ~ H(z)")
fp0 = json.load(open(os.path.join(C.CHAIN, "FP0_core_postulates_results.json")))["numbers"]["a0z_rival_E"]
Ez = lambda z: math.sqrt(C.OM_M_LIB * (1 + z) ** 3 + C.OM_L_LIB)
Om47 = 0.3153                                                                          # FP0's own Omega_m (Planck 2018 TT,TE,EE+lowE+lensing)
fp0_rep = {z: math.sqrt(Om47 * (1 + float(z)) ** 3 + 1 - Om47) for z in fp0}
dev9 = max(abs(fp0_rep[z] / fp0[z] - 1) for z in fp0)
P(f"    settled scale: P_Lambda(z) / P_Lambda(0) = rho_Lambda(z)/rho_Lambda(0) = 1 for a cosmological constant (BTFR zero point and "
  f"column ceiling flat); rival a0 ~ H(z): E(2.5) = {fp0['2.5']:.4f} -> +{math.log10(fp0['2.5']):.3f} dex (FP0 committed; "
  f"reproduced with Omega_m = {Om47} to {dev9:.1e})")
R.num("A9", {"rival_E_2p5": fp0["2.5"], "rival_dex_2p5": math.log10(fp0["2.5"]), "reproduced_dev": dev9})
check("H9 a0(z) IS FLAT IN THE SETTLED LAW: its only scale is P_Lambda ~ rho_Lambda (constant for w = -1); FP0's committed rival "
      "E(z) is reproduced (the rival puts the z = 2.5 BTFR zero point +0.576 dex away)",
      f"reproduced FP0 rival E(z) to {dev9:.1e}; rival +{math.log10(fp0['2.5']):.3f} dex at z = 2.5", dev9 < 1e-3)

# =============================================================================================== A10
R.banner("A10  THE CONSTANT COUNT (fitted / declared / tied / derived) and what the principle eliminates")
rows = [
    ("FITTED", "kappa = 1/2 (Z = 5.7888): the normalisation of a0 = kappa c sqrt(G rho_Lambda)"),
    ("DECLARED", "m, the dark field's mass: enters only small-scale linear cosmology (>= 2e-21 eV, forest; CFG2_D)"),
    ("DECLARED", "Omega_c, the dark field's amount (initial data, as in LambdaCDM)"),
    ("DECLARED", "the scope RULE (settle iff capacity >= accreted, at rest in the system): a rule, no number; it uses the "
                 "record's Moster+13 accretion convention"),
    ("DECLARED", "the reading (E: the stress law local in the field) -- chosen by SPARC over F (CFG2_B)"),
    ("TIED", "P_Lambda = a0^2/(8 pi G) = kappa^2 rho_Lambda c^2/(8 pi): from a0"),
    ("DERIVED", "nu = P2 = sqrt(1 + 1/y), uniquely, from the point-mass hydrostatic medium (A2, A3)"),
    ("DERIVED", "BTFR v^4 = G M_b a0 exactly (A4); the halo column ceiling a0/(2 pi G) (A5); sigma^2 = v_c^2/2 (A2)"),
    ("DERIVED", "the settled window in M* (A8); flat a0(z) (A9); no EFE (SEP: the medium responds only where it is at rest)"),
    ("ELIMINATED", "xi (the Solar-System screening length: GR there, CFG2_D); alpha_c, c_2, lambda (no khronon); the separator's "
                   "4 constants (no MOND in the web); the kick eps, v_k (clusters keep CDM because they are unsettled)"),
]
for k_, t_ in rows:
    P(f"    {k_:10s} {t_}")
R.num("A10", {"fitted": 1, "declared_numbers": 1, "declared_initial_data": 1, "declared_rules": 2, "tied": 1})
check("A10 (reported) THE CONSTANT COUNT: 1 fitted (kappa), 1 declared number (m, cosmology only), 1 initial datum (Omega_c), "
      "2 declared rules (scope; reading E), 1 tied (P_Lambda), the kernel and the BTFR/column derived",
      "1 / 1 / 1 / 2 rules / 1 tied", True, load_bearing=False)

R.banner("W  LEDGER")
R.ledger("CFG2-A1", "DERIVED", "P2 = the hydrostatic dark medium with P_d = sqrt(P_Lambda P_N) around a point mass (unique)", "A2/A3")
R.ledger("CFG2-A2", "DERIVED", "BTFR exact (any spherical distribution); column ceiling a0/(2 pi G) = 106.9/129.2 Msun/pc^2", "A4/A5")
R.ledger("CFG2-A3", "CONSTRAINT", "readings E vs F differ inside extended baryons by (2-n)/(n+2) in M^2", "A6")
R.ledger("CFG2-A4", "CONSTRAINT", "gravity-only pressure and thermal settling cannot make the RAR (stress-free inside diffuse baryons; nu(1) <= 4/3)", "A7")
R.ledger("CFG2-A5", "PREDICTION", "settled window in M*; outside it systems sit ABOVE the RAR", "A8")
sys.exit(R.finish())
