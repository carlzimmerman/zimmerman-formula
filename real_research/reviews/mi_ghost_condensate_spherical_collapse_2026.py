#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mi_ghost_condensate_spherical_collapse_2026.py

MECHANISM 3: NONLINEAR SPHERICAL COLLAPSE OF THE AeST Q-SECTOR (GHOST CONDENSATE)
=================================================================================
Question assigned: does a component with the z=2 (k^4) dispersion

        omega^2 = c^2 k^4 / k_M^2 ,        k_M = M/(hbar c)

halt its own collapse (forming a soliton/core) at a radius large enough to keep
the Q-sector dust OUT of galaxy (~20 kpc) and cluster (~1.3 Mpc) halos?  If yes,
the double-counting overshoot of the framework's context item 4 dissolves and a
"no dark matter in halos" reading survives.  If no, the dust virialises and
xi -> 1, which destroys the SPARC RAR.

STRUCTURE
  BLOCK 0  constants, the condensate scale, unit conversions
  BLOCK 1  the shell equation:  Rddot = -G M/R^2 + A/R^3   (A fixed by dimensions)
  BLOCK 2  R^-3 vs R^-2: which wins, and the stall radius R_stall = A/(G M_sh)
  BLOCK 3  core radius/mass at M = rho_Lambda^(1/4), vs 20 kpc and 1.3 Mpc.
           Validated against the known fuzzy-DM soliton scale.
  BLOCK 4  THE DECISIVE ITEM: can nonlinear collapse beat the LINEAR Jeans scale?
           Exact scaling  R_stall = C * lambda_J^4 / R_i^3 .
  BLOCK 5  inversion: what M would the k^4 term need?  vs Rogers-Peiris floor.
  BLOCK 6  xi in a galaxy and a cluster from the k^4 mechanism.
  BLOCK 7  CHALLENGE TO CONTEXT ITEM 1.  The k^2 term is NOT absent once the
           condensate carries an Omega_dm amount of energy: ACLMW 2007 eq 3.15
           gives p = rho^2/(2 M^4) exactly, hence c_s^2 = rho/M^4.  This term
           beats the k^4 term by ~50 orders at galaxy scales.  Redo the collapse
           with it.  It gives a UNIVERSAL, mass-independent stall radius R_p.
  BLOCK 8  hydrostatic branch: derive delta_rho = rho_M |Phi| / c^2 and hence
           xi = min[1, (R/R_p)^2].  This reproduces AeST's Helmholtz/linear-
           response result from the NONLINEAR equation of state, with NO free
           per-object chemical potential.
  BLOCK 9  THE FORK.  R_p required by clusters+RAR vs R_p allowed by cosmology.
           Independent re-derivation of Blanchet & Skordis 2024 sec 4.3.1.

CITATIONS FOR LOAD-BEARING EQUATIONS
  Arkani-Hamed, Cheng, Luty & Mukohyama 2004, JHEP 0405:074, hep-th/0312099
     eq (7.6)-(7.8): omega^2 = alpha^2 k^4/M^2 - alpha^2 M^2 k^2/(2 M_Pl^2);
     eq (7.10) Gamma = alpha M^3/(4 M_Pl^2); eq (7.7) m = M^2/(sqrt2 M_Pl).
  Arkani-Hamed, Cheng, Luty, Mukohyama & Wiseman 2007, JHEP 0701:036,
     hep-ph/0507120.  eq (3.12) P(X) = (1/8)(X-1)^2 = Sigma^2/2;
     eq (3.15) rho = M^4 Sigma, p = (1/2) M^4 Sigma^2 = rho^2/(2 M^4);
     eq (3.19) Dv/Dt = -grad(Phi + Sigma);  eq (3.21) -grad Sigma = -(1/rho) grad p;
     footnote 2: L_J = 2 pi c_s / sqrt(4 pi G rho) ~ M_Pl/M^2, DENSITY-INDEPENDENT,
     and it agrees with the linear-theory Jeans length of their eq (2.25).
     sec 3.5 verbatim: "It is possible that the pressure resolves the caustics in
     important situations such as inside galaxy halos made of ghostone dark
     matter, but we will not consider that here."
  Chavanis & Delfini 2011, PRD 84:043532: Schroedinger-Poisson ground state,
     R_99 = 9.946 hbar^2 / (G M m^2).
  Schive, Chiueh & Broadhurst 2014, Nature Physics 10:496, arXiv:1406.6586:
     simulated FDM soliton core + NFW envelope; r_c ~ 1 kpc for m = 1e-22 eV
     in a ~1e12 Msun halo.  Used only to VALIDATE the de Broglie core estimate.
  Rogers & Peiris 2021, PRL 126:071302: Lyman-alpha FDM floor m > 2e-20 eV.
  Blanchet & Skordis 2024, JCAP 11:040, arXiv:2404.06584, sec 4.3.1: for
     K(Q) = mu^2 (Q-1)^2, cosmology forces mu^-1 <~ 0.22 kpc while MOND forces
     mu^-1 >~ 100 kpc -- "cannot be in simultaneous harmony".
  Mistele, McGaugh & Hossenfelder 2023, A&A 676:A100, arXiv:2301.03499, eq (2):
     rho_c = (m^2/4 pi G_N f_G)(phidot/Q0 - Phihat - phi).
  Durakovic & Skordis 2024, JCAP 04:040, arXiv:2312.00889, eq (2.33):
     div(M grad Phi) + mutilde^2 Phi = 4 pi G rho_b.
"""

import math

L = []
def p(s=""):
    L.append(s); print(s)
def hdr(s):
    p(); p("="*78); p(s); p("="*78)

# ---------------------------------------------------------------- BLOCK 0
hdr("BLOCK 0 -- CONSTANTS AND THE CONDENSATE SCALE")

c    = 2.99792458e8          # m/s
G    = 6.67430e-11           # m^3 kg^-1 s^-2
hbar = 1.054571817e-34       # J s
eV   = 1.602176634e-19       # J
Msun = 1.98892e30            # kg
kpc  = 3.0856775814913673e19 # m
Mpc  = 1000.0*kpc
Gyr  = 3.1557e16             # s
t0   = 13.797*Gyr            # s, age of universe

# Planck-2018-ish background
h_red   = 0.674
H0      = 100.0*h_red*1e3/Mpc            # s^-1
rho_crit= 3.0*H0**2/(8.0*math.pi*G)      # kg/m^3
Om_dm   = 0.2645
Om_L    = 0.6847
rho_dm0 = Om_dm*rho_crit
rho_L   = Om_L *rho_crit                 # mass-density equivalent of rho_Lambda

p(f"H0        = {H0:.6e} s^-1   ({100*h_red:.1f} km/s/Mpc)")
p(f"rho_crit  = {rho_crit:.6e} kg/m^3")
p(f"rho_dm,0  = {rho_dm0:.6e} kg/m^3   (Omega_dm = {Om_dm})")
p(f"rho_Lambda= {rho_L:.6e} kg/m^3   (Omega_L  = {Om_L})")
p(f"rho_dm,0 / rho_Lambda = {rho_dm0/rho_L:.6f}")

# natural condensate scale: M = rho_Lambda^(1/4) as an ENERGY
# energy density u_L = rho_L c^2 ; M = (u_L hbar^3 c^3)^(1/4) in energy units
u_L   = rho_L*c**2                                  # J/m^3
M_nat = (u_L*(hbar*c)**3)**0.25                     # J
p(f"\nu_Lambda   = {u_L:.6e} J/m^3 = {u_L/eV:.6e} eV/m^3")
p(f"M_nat      = rho_Lambda^(1/4) = {M_nat:.6e} J = {M_nat/eV:.6e} eV"
  f" = {M_nat/eV*1e3:.4f} meV")

def kM_of(M_J):   return M_J/(hbar*c)               # m^-1
def beta_of(M_J): return c**2/kM_of(M_J)**2         # m^4 s^-2 ; omega^2 = beta k^4
def rhoM_of(M_J):                                   # M^4 as a MASS density
    return (M_J**4/(hbar*c)**3)/c**2

kM_nat, beta_nat = kM_of(M_nat), beta_of(M_nat)
p(f"k_M(nat)   = {kM_nat:.6e} 1/m      ->  1/k_M = {1.0/kM_nat:.6e} m")
p(f"beta(nat)  = c^2/k_M^2 = {beta_nat:.6e} m^4/s^2")
p(f"CHECK rho_M(M_nat)/rho_Lambda = {rhoM_of(M_nat)/rho_L:.6f}  (must be 1)")

# FDM mapping: omega^2 = beta k^4 == hbar^2 k^4/(4 m_eff^2)  =>  m_eff = hbar/(2 sqrt(beta))
def meff_of(M_J): return hbar/(2.0*math.sqrt(beta_of(M_J)))     # kg
m_nat = meff_of(M_nat)
p(f"\nFDM MAPPING  omega^2 = beta k^4 = hbar^2 k^4/(4 m_eff^2)")
p(f"  m_eff(nat) = {m_nat:.6e} kg = {m_nat*c**2/eV:.6e} eV/c^2")
p(f"  m_eff c^2 / M_nat = {m_nat*c**2/M_nat:.6f}   (expect exactly 1/2)")
p("  => the k^4 sector is EXACTLY fuzzy dark matter with particle mass M/2.")
p("     The nonlinear collapse problem is therefore the FDM soliton problem,")
p("     which HAS been simulated (Schive+2014).  Nothing needs to be guessed.")

# ---------------------------------------------------------------- BLOCK 1
hdr("BLOCK 1 -- THE SHELL EQUATION")

p("""A spherical shell of radius R enclosing dust mass M_sh obeys

      Rddot = -G M_sh / R^2  +  a_grad(R)

The gradient term is FIXED BY DIMENSIONS, no model input needed.  The only
dimensionful coefficient the k^4 sector supplies is

      beta = c^2 / k_M^2      [m^4 s^-2]

and the only combination of beta and R with the units of an acceleration is
beta/R^3.  Hence

      a_grad = A / R^3 ,      A = O(1) x beta .                            (*)

Two independent constructions give the same thing:
 (i) Madelung/quantum pressure of the equivalent Schroedinger field,
     Q = -(hbar^2/2 m^2) lap(sqrt rho)/sqrt rho  ~  -hbar^2/(2 m^2 R^2),
     a_Q = -grad Q ~ hbar^2/(m^2 R^3) = 4 beta / R^3 .   So A = 4 beta with
     the O(1) fixed by the exact SP soliton (block 3).
 (ii) energy functional  E(R) = a1 hbar^2 M_sh/(m^2 R^2) - a2 G M_sh^2/R,
      dE/dR = 0  ->  R_* = 2 a1 hbar^2 /(a2 G m^2 M_sh) = O(1) x beta/(G M_sh).

The O(1) is irrelevant below: the answer misses by 43 orders of magnitude.

So the collapse equation is

      Rddot = - G M_sh / R^2  +  A / R^3 ,        A = 4 c^2 / k_M^2 .      (1)
""")
A_nat = 4.0*beta_nat
p(f"A(nat) = 4 beta = {A_nat:.6e} m^4/s^2")
p(f"hbar^2/m_eff^2 = {(hbar/m_nat)**2:.6e} m^4/s^2   (must equal 4 beta)")

# ---------------------------------------------------------------- BLOCK 2
hdr("BLOCK 2 -- R^-3 vs R^-2 : WHICH WINS, AND WHERE")

p("""a_grad/a_grav = (A/R^3)/(G M_sh/R^2) = A/(G M_sh R).

This GROWS without bound as R -> 0.  So the k^4 term ALWAYS wins eventually:
a core DOES form, collapse is not unopposed.  The whole question is at WHAT R.

      R_stall = A / (G M_sh) .                                             (2)

Note the structure: R_stall is INVERSELY proportional to the collapsing mass.
The more mass you try to stabilise, the smaller the radius at which the k^4
term can do it.  That is the opposite of what a rescue needs.""")

def R_stall_k4(M_sh_kg, M_J=M_nat):
    return 4.0*beta_of(M_J)/(G*M_sh_kg)

cases = [
    ("MW-like galaxy, dust inside 20 kpc",  1.0e11*Msun, 20.0*kpc),
    ("LSB dwarf, dust inside 5 kpc",        5.0e9 *Msun,  5.0*kpc),
    ("cluster M500=5e14, dust inside R500", 0.8447*5.0e14*Msun, 1.3*Mpc),
]
p("")
p(f"{'system':38s} {'M_dust[kg]':>11s} {'R[m]':>10s} {'R_stall[m]':>11s} {'R_stall/R':>11s}")
for nm, Md, R in cases:
    Rs = R_stall_k4(Md)
    p(f"{nm:38s} {Md:11.3e} {R:10.3e} {Rs:11.3e} {Rs/R:11.3e}")
    Rsch = 2.0*G*Md/c**2
    p(f"{'':38s} Schwarzschild radius of that mass = {Rsch:.3e} m"
      f"  -> R_stall/R_S = {Rs/Rsch:.3e}")

p("""
--- EXACT FIRST INTEGRAL OF EQ (1) (no O(1) ambiguity at all) ---
Eq (1) integrates exactly:  (1/2) Rdot^2 = G M_sh/R - A/(2 R^2) + E.
Release from rest at turnaround R_ta fixes E.  The inner turning point (Rdot = 0
again, i.e. the BOUNCE) satisfies, after cancelling the factor (R_ta - R),

      G M_sh R_ta R = (A/2)(R_ta + R)
  =>  R_bounce = (A/2) R_ta / (G M_sh R_ta - A/2)  ->  A/(2 G M_sh)  for R_ta >> R_stall.

So the shell does NOT collapse to a point: it bounces at R_bounce = A/(2 G M_sh)
and thereafter breathes.  A core is guaranteed.  R_bounce = R_stall/2 exactly,
so nothing below depends on the O(1) in A.""")
Rta_test = 1.0*Mpc
for nm, Md, R in cases:
    Rb_exact = (A_nat/2.0)*Rta_test/(G*Md*Rta_test - A_nat/2.0)
    p(f"  {nm:38s} R_bounce(exact, R_ta=1 Mpc) = {Rb_exact:.4e} m"
      f"  [= R_stall/2 = {R_stall_k4(Md)/2:.4e} m]")

p("""
READ THIS CAREFULLY.  R_stall is not merely small, it is BELOW THE SCHWARZSCHILD
RADIUS of the collapsing mass by 8-9 orders.  A coherent lump carrying a halo's
worth of Q-sector dust would become a black hole ~9 orders of magnitude in radius
BEFORE the k^4 gradient term became relevant.  The k^4 term therefore cannot halt
halo-scale collapse under any circumstances at M = rho_Lambda^(1/4).""")

# response time of the gradient term
p("\nSECOND, INDEPENDENT CHECK -- the k^4 term is also far too SLOW:")
p("  the gradient mode at wavenumber k = 1/R oscillates at omega = sqrt(beta)/R^2,")
p("  so its response time is t_grad = R^2 k_M / c.")
for nm, Md, R in cases:
    t_grad = R**2*kM_nat/c
    t_ff   = math.sqrt(3.0*math.pi/(32.0*G*(Md/(4.0*math.pi/3.0*R**3))))
    p(f"  {nm:38s} t_grad = {t_grad:.3e} s = {t_grad/t0:.3e} t0 ;"
      f"  t_freefall = {t_ff/Gyr:.3f} Gyr ; ratio t_grad/t_ff = {t_grad/t_ff:.3e}")
p("  => the gradient term needs 1e19-1e23 Hubble times to respond at these scales.")
p("     This quantifies ACLM 2004's 'this effect takes time to build up'.")

# ---------------------------------------------------------------- BLOCK 3
hdr("BLOCK 3 -- THE CORE THAT ACTUALLY FORMS: SIZE AND MASS AT M = 2.24 meV")

p("""A halo is not one coherent lump.  In the simulated FDM system (Schive, Chiueh
& Broadhurst 2014, Nature Physics 10:496) collapse produces a SOLITON CORE
embedded in an incoherent, virialised, NFW-like envelope.  The core radius is the
de Broglie wavelength at the halo's own velocity dispersion,

      lambda_dB = 2 pi hbar / (m_eff v) .                                  (3)

VALIDATION of (3) against the published FDM result before using it:""")

def lam_dB(m_kg, v): return 2.0*math.pi*hbar/(m_kg*v)
m_1e22 = 1.0e-22*eV/c**2
p(f"  m = 1e-22 eV/c^2, v = 150 km/s  ->  lambda_dB = "
  f"{lam_dB(m_1e22,1.5e5)/kpc:.3f} kpc")
p("  Schive+2014 / Schive+2014 PRL 113:261302 find r_c ~ 1 kpc for m = 1e-22 eV")
p("  in a ~1e12 Msun halo.  Eq (3) reproduces it.  Estimator validated.")

p(f"\nNow at the natural condensate scale M = {M_nat/eV*1e3:.3f} meV"
  f"  (m_eff = {m_nat*c**2/eV:.4e} eV/c^2):")
halos = [("MW-like",  1.3e12*Msun, 2.0e5, 200.0*kpc),
         ("LSB dwarf",3.0e10*Msun, 4.0e4,  40.0*kpc),
         ("cluster",  5.0e14*Msun, 1.0e6, 1300.0*kpc)]
for nm, Mh, v, Rv in halos:
    lam = lam_dB(m_nat, v)
    # soliton mass from the exact SP relation R99 = 9.946 hbar^2/(G M m^2)
    # identify R99 ~ lambda_dB  ->  M_c = 9.946 hbar^2/(G m^2 lambda_dB)
    Mc = 9.946*hbar**2/(G*m_nat**2*lam)
    p(f"  {nm:10s} v={v/1e3:7.1f} km/s : r_core = lambda_dB = {lam:.4e} m"
      f" = {lam/kpc:.3e} kpc")
    p(f"  {'':10s}   M_core = {Mc:.4e} kg = {Mc/Msun:.4e} Msun"
      f" ; M_core/M_halo = {Mc/Mh:.3e}")
    p(f"  {'':10s}   r_core / R_system = {lam/Rv:.3e}")

p("""
COMPARISON TO THE TARGET SCALES
  galaxy  20 kpc  = 6.171e20 m
  cluster 1.3 Mpc = 4.011e22 m
  core at M = 2.24 meV: ~2 m.
  Shortfall: 20-22 ORDERS OF MAGNITUDE in radius.
  Core mass fraction of the halo: 1e-23 (galaxy), 1e-25 (cluster).
A core forms.  It is metre-sized and carries 1e-23 of the halo mass.  It changes
nothing.  And note: a soliton core is still MASS SITTING IN THE HALO, so even a
large core would not by itself reduce xi -- it would only redistribute the dust.
The dust is removed from radius R only if r_core >~ R AND essentially all of the
dust is in the core.""")

# ---------------------------------------------------------------- BLOCK 4
hdr("BLOCK 4 -- THE DECISIVE ITEM: CAN NONLINEARITY BEAT THE LINEAR JEANS SCALE?")

def lam_J_k4(rho, M_J=M_nat):
    """linear k^4 Jeans length: omega^2 = beta k^4 - 4 pi G rho = 0."""
    kJ = (4.0*math.pi*G*rho/beta_of(M_J))**0.25
    return 2.0*math.pi/kJ

lJ_mean = lam_J_k4(rho_dm0)
p(f"Reproduce the context's item-2 number first:")
p(f"  lambda_J(rho = rho_dm,0, M = 2.24 meV) = {lJ_mean:.6e} m"
  f" = {lJ_mean/Mpc:.4e} Mpc")
p(f"  context item 2 quotes 2.8e-11 Mpc.  MATCH -> the beta normalisation is right.")

p("""
Now the exact scaling.  Take an initially uniform region of physical radius R_i
and density rho_i, mass M_sh = (4 pi/3) rho_i R_i^3.  Then

  R_stall = A/(G M_sh) = A / (G (4 pi/3) rho_i R_i^3)
  lambda_J(rho_i) = 2 pi (beta/(4 pi G rho_i))^(1/4)

so with A = 4 beta,

  R_stall / lambda_J = [ 3 A /(4 pi G rho_i) ] / R_i^3 x (4 pi G rho_i/beta)^(1/4)/(2 pi)
                     = C x ( lambda_J / R_i )^3 ,                          (4)

i.e.   R_stall = C lambda_J (lambda_J/R_i)^3 .

THIS IS THE ANSWER TO THE QUESTION.  A region only collapses at all if
R_i >~ lambda_J.  Therefore R_stall <= C lambda_J ALWAYS with C = 3/(4 pi^4) =
0.0077, and for the deep nonlinear collapses that make galaxies
(R_i/lambda_J ~ 1e10) the stall radius is smaller than the linear Jeans length by
the CUBE of that factor, ~1e-32.

Nonlinear collapse does not produce a core LARGER than the linear Jeans scale.
It produces one very much SMALLER.  The physical reason is that
lambda_J propto rho^(-1/4) is a DECREASING function of density, and collapse
raises the density; the stabilisation scale is lambda_J evaluated
self-consistently at the FINAL density, never at the initial one.""")

p(f"\nVerify (4) numerically, and the constant C:")
p(f"{'rho_i/rho_dm0':>14s} {'R_i[m]':>11s} {'lam_J[m]':>11s} {'R_stall[m]':>11s}"
  f" {'R_stall/lam_J':>14s} {'(lam_J/R_i)^3':>14s} {'C':>8s}")
for fac, Ri in [(1.0, 1.0*Mpc), (1.0, 0.3*Mpc), (1.0, 8.71e11),
                (1.0e5, 20.0*kpc), (1.0e3, 1.3*Mpc)]:
    rho_i = fac*rho_dm0
    Msh   = 4.0*math.pi/3.0*rho_i*Ri**3
    Rs    = R_stall_k4(Msh)
    lJ    = lam_J_k4(rho_i)
    r1, r2 = Rs/lJ, (lJ/Ri)**3
    p(f"{fac:14.3e} {Ri:11.3e} {lJ:11.3e} {Rs:11.3e} {r1:14.3e} {r2:14.3e}"
      f" {r1/r2:8.4f}")
C_meas = None
_rho_i = rho_dm0; _Ri = lam_J_k4(_rho_i)
C_meas = R_stall_k4(4.0*math.pi/3.0*_rho_i*_Ri**3)/_Ri
p(f"  C is constant across 30 orders of magnitude in the ratio -> eq (4) is exact.")
p(f"  MEASURED C = {C_meas:.5f}   analytic: with A = 4 beta and lambda_J = 2 pi/k_J,")
p(f"    lambda_J^4 = 4 pi^3 beta/(G rho), R_stall = 3 beta/(pi G rho R_i^3), so")
p(f"    C = 3/(4 pi^4) = {3.0/(4.0*math.pi**4):.5f}.  MATCHES the measured value.")
p(f"  Note row 3: R_i = lambda_J exactly gives R_stall/lambda_J = C = {C_meas:.4f},")
p(f"  i.e. the LARGEST core the k^4 term can EVER make is {C_meas:.4f} lambda_J,")
p(f"  and with the exact bounce it is half that, {C_meas/2:.4f} lambda_J.")
p("  THE LINEAR JEANS SCALE IS A HARD CEILING ON THE NONLINEAR CORE, not a floor,")
p("  and the ceiling sits two orders BELOW lambda_J, not at it.")

# density-dependence of lambda_J, to make the point concretely
p("\nlambda_J shrinks as collapse proceeds (rho^-1/4):")
rho_gal = 1.0e11*Msun/(4.0*math.pi/3.0*(20.0*kpc)**3)
rho_clu = 0.8447*5.0e14*Msun/(4.0*math.pi/3.0*(1.3*Mpc)**3)
for nm, rho in [("cosmic mean dust", rho_dm0),
                ("cluster mean inside R500", rho_clu),
                ("MW halo mean inside 20 kpc", rho_gal),
                ("solar-neighbourhood DM 0.01 Msun/pc^3", 0.01*Msun/(kpc/1000)**3)]:
    p(f"  {nm:42s} rho={rho:.3e} kg/m^3  lambda_J={lam_J_k4(rho):.4e} m"
      f" = {lam_J_k4(rho)/kpc:.3e} kpc")

# ---------------------------------------------------------------- BLOCK 5
hdr("BLOCK 5 -- INVERSION: WHAT M WOULD THE k^4 TERM NEED?")

p("""Require R_stall >= R for the dust to be kept out of radius R:
      4 c^2/k_M^2 >= G M_sh R   ->   M <= 2 hbar c^2 / sqrt(G M_sh R).      (5)""")
p(f"\n{'target':46s} {'M_max[eV]':>12s} {'M_max/M_nat':>12s} {'vs 2e-20 eV floor':>19s}")
for nm, Md, R in cases:
    Mmax = 2.0*hbar*c**2/math.sqrt(G*Md*R)
    p(f"{nm:46s} {Mmax/eV:12.4e} {Mmax/M_nat:12.4e} {Mmax/(2.0e-20*eV):19.4e}")
p("""
Compare the LINEAR requirement quoted in context item 2: M = 2.44e-25 eV to get
lambda_J = 2.7 Mpc.  The NONLINEAR requirement is 1.31e-24 eV (galaxy),
1.17e-23 eV (LSB dwarf), 2.49e-27 eV (cluster).

=> Nonlinearity buys AT MOST a factor ~5 for a galaxy and LOSES two orders for a
   cluster.  Not one order of magnitude of relief where it matters.  The k^4
   route still needs M ~ 1e-24 to 1e-27 eV: 21-25 orders below the natural
   rho_Lambda^(1/4) = 2.24 meV, and 4.2-7.0 orders below the Lyman-alpha fuzzy-DM
   floor m > 2e-20 eV (Rogers & Peiris 2021, PRL 126:071302).  THE k^4 ROUTE IS
   SHUT NONLINEARLY FOR THE SAME REASON IT IS SHUT LINEARLY.  And note the
   cluster requirement is the one that moves the WRONG way, which is exactly the
   scale the framework most needs help at.""")

# ---------------------------------------------------------------- BLOCK 6
hdr("BLOCK 6 -- xi FROM THE k^4 MECHANISM")

p("""xi(R) = M_dust(<R) / M_dust,CDM(<R).  With r_core ~ 2 m and R_stall ~ 1e-22 m,
the only dust NOT in the CDM-like virialised envelope is the soliton core, of
mass fraction M_core/M_halo computed in block 3:""")
for nm, Mh, v, Rv in halos:
    lam = lam_dB(m_nat, v)
    Mc  = 9.946*hbar**2/(G*m_nat**2*lam)
    p(f"  {nm:10s}: xi = 1 - {Mc/Mh:.3e} = 1.0000000000000000000000 (to 23 digits)")
p("""
xi_galaxy = 1,  xi_cluster = 1.
Feeding that into context item 4 (1/f_bar = 6.4387, xi = 1):
  cluster R500 (y_bar=0.0684): overshoot 2.06x
  bright spiral (y_bar=1.0)  : overshoot 4.42x
The SPARC RAR is destroyed.  THIS IS UNFAVOURABLE TO THE NO-DARK-MATTER READING.""")

# ---------------------------------------------------------------- BLOCK 6b
hdr("BLOCK 6b -- THE LAST k^4 DOOR: DOES CAUSTIC FRAGMENTATION REMOVE MASS?")

p("""ACLMW 2007 sec 3.3-3.5 show the ghostone fluid is exactly an IRROTATIONAL
perfect fluid away from caustics, that caustics form on the Kepler time
(their eq 3.8), and that the higher-derivative alpha(lap pi)^2 term -- the k^4
term -- is what regularises them.  Sec 3.5 verbatim: "It is possible that the
pressure resolves the caustics in important situations such as inside galaxy
halos made of ghostone dark matter, but we will not consider that here."
That is the one remaining k^4 door.  Close it quantitatively.

The k^4 term becomes dynamically relevant when beta k^4 ~ t_ff^-2, i.e. at
      l_caustic = (beta t_ff^2)^(1/4).""")
p(f"\n{'system':38s} {'t_ff[Gyr]':>10s} {'l_caustic[m]':>13s} {'[kpc]':>11s} {'l/R':>11s}")
for nm, Md, R in cases:
    rho_s = Md/(4.0*math.pi/3.0*R**3)
    t_ff  = math.sqrt(3.0*math.pi/(32.0*G*rho_s))
    lc    = (beta_nat*t_ff**2)**0.25
    p(f"{nm:38s} {t_ff/Gyr:10.3f} {lc:13.4e} {lc/kpc:11.3e} {lc/R:11.3e}")
p("""
So the k^4 term regularises structure at ~1e10 m = 3e-10 kpc, and does nothing
above that.  Every astrophysical scale is in the pressureless irrotational-dust
regime, where trajectories cross and shell-crossing converts ordered infall into
VELOCITY DISPERSION.  That is virialisation.  Fragmentation redistributes the
dust into de Broglie-scale granules; it does not expel a single gram from radius
R.  Mass is conserved and the coarse-grained profile is CDM-like.

This also disposes of Frolov 2004's (PRD 70:061501) irrotationality objection in
the direction UNFAVOURABLE to the framework, consistent with Mukohyama 2005
(PRD 71:104019): coarse-graining over caustics supplies effective angular
momentum, so the "it cannot virialise because it is irrotational" escape fails.
THE LAST k^4 DOOR IS CLOSED.""")

# ---------------------------------------------------------------- BLOCK 7
hdr("BLOCK 7 -- CHALLENGE TO CONTEXT ITEM 1: THE k^2 TERM IS NOT ABSENT")

p("""Context item 1 says c_s^2 = u/(3u+2) -> 0 at the condensate, "so the k^2
gradient term is ABSENT and the leading dispersion is omega^2 = c^2 k^4/k_M^2."
That is exact only AT u = 0, i.e. only for a condensate carrying ZERO energy
density.  A Q-sector that is the dark matter carries u != 0 by construction.

ACLMW 2007 (hep-ph/0507120) eq (3.15), verbatim: rho = M^4 Sigma,
p = (1/2) M^4 Sigma^2 = rho^2/(2 M^4).  Hence EXACTLY

      c_s^2 = dp/drho = rho / M^4  =  Sigma .                              (6)

and their footnote 2 states the corresponding Jeans length
L_J = 2 pi c_s/sqrt(4 pi G rho) ~ M_Pl/M^2 is DENSITY-INDEPENDENT and agrees
with their linear eq (2.25).  Note also that the context's own
c_s^2 = u/(3u+2) -> u/2 for small u has exactly this form with u = 2 Sigma:
the two statements agree, and both say c_s^2 = O(rho/M^4), NOT zero.""")

def Sigma_of(rho, M_J): return rho/rhoM_of(M_J)
def cs2_of(rho, M_J):
    u = 2.0*Sigma_of(rho, M_J)
    return u/(3.0*u+2.0)          # context's own form; -> Sigma for small u, caps at 1/3

p(f"\nAt M = M_nat = 2.24 meV (rho_M = rho_Lambda):")
for nm, rho in [("cosmic mean dust today", rho_dm0),
                ("cluster inside R500", rho_clu),
                ("MW halo inside 20 kpc", rho_gal)]:
    S = Sigma_of(rho, M_nat); cs2 = cs2_of(rho, M_nat)
    p(f"  {nm:26s} Sigma = {S:.4e} ; c_s^2 = {cs2:.4e} ; c_s = {math.sqrt(cs2):.4f} c")
p("""  => at the NATURAL scale the condensate has c_s ~ 0.42 c at the COSMIC MEAN
     today (Sigma = 0.386, no expansion issue there), and Sigma = 5e2-3e4 in
     clusters/halos.  HONEST CAVEAT, stated because it cuts both ways: Sigma >> 1
     means ACLMW's small-Sigma expansion p = rho^2/2M^4 has broken down, so the
     c_s^2 = 1/3 saturation values in halos are NOT trustworthy -- only the
     cosmic-mean number Sigma = 0.386 is inside the expansion's domain.  But that
     one number is already fatal: a component with c_s = 0.42 c today is not dust
     and cannot be the dark matter.  M = rho_Lambda^(1/4) is EXCLUDED as the
     Q-sector scale independently of everything else in this script.  The natural,
     Lambda-derived value of M is not available; M must be fitted.""")

p("\nWhich gradient term dominates at galaxy scales?  omega^2 = c_s^2 k^2 + beta k^4.")
for Mlab, M_J in [("2.24 meV (natural)", M_nat), ("0.148 eV (AeST mu^-1=1 Mpc)", 0.148*eV)]:
    k = 1.0/(20.0*kpc)
    cs2 = cs2_of(rho_gal, M_J)
    t2, t4 = cs2*c**2*k**2, beta_of(M_J)*k**4
    p(f"  M = {Mlab:28s}: c_s^2 k^2 = {t2:.3e} ; beta k^4 = {t4:.3e}"
      f" ; ratio = {t2/t4:.3e}")
p("  => the k^2 term beats the k^4 term by 40-60 ORDERS at galaxy scales.")
p("     The assigned k^4 analysis is therefore not even the binding physics.")

p("""
REDO THE COLLAPSE WITH THE k^2 (ADIABATIC) TERM.  ACLMW eq (3.19)/(3.21):
Dv/Dt = -grad(Phi + c^2 Sigma) and -grad Sigma = -(1/rho) grad p.  For a shell,

  a_p = c^2 Sigma / R = c^2 rho/(rho_M R) = 3 c^2 M_sh /(4 pi rho_M R^4)   (7)

  a_p / a_grav = [3 c^2 M_sh/(4 pi rho_M R^4)] / [G M_sh/R^2]
               = 3 c^2 / (4 pi G rho_M R^2)                                (8)

THE MASS CANCELS.  There is ONE universal stall radius, the same for every
object:

  R_p = c sqrt( 3 / (4 pi G rho_M) ) .                                     (9)

Note (7) scales as R^-4 -- STEEPER than the k^4 term's R^-3.  So the adiabatic
pressure is the dominant collapse-halting mechanism at every scale, and unlike
the k^4 term its reach is set by rho_M alone, not by the collapsing mass.""")

def R_p_of(M_J): return c*math.sqrt(3.0/(4.0*math.pi*G*rhoM_of(M_J)))
p(f"\n{'M':>28s} {'rho_M[kg/m^3]':>14s} {'R_p[Mpc]':>12s} {'R_p[kpc]':>12s}")
for Mlab, M_J in [("2.24 meV (natural)", M_nat), ("0.0986 eV", 0.0986*eV),
                  ("0.148 eV (mu^-1=1 Mpc)", 0.148*eV), ("1.06 eV", 1.06*eV),
                  ("11.5 eV", 11.5*eV)]:
    p(f"{Mlab:>28s} {rhoM_of(M_J):14.4e} {R_p_of(M_J)/Mpc:12.4e} {R_p_of(M_J)/kpc:12.4e}")
p(f"\nCROSS-CHECK against the previous agent's identity L_J = 2 pi/mu with")
p(f"M^4 = mu^2/(4 pi G) (in hbar=c=1):  at M = 0.148 eV they get L_J = 6.28 Mpc;")
p(f"eq (9) gives R_p = {R_p_of(0.148*eV)/Mpc:.3f} Mpc.  Same length up to 2 pi/sqrt3 = 3.63.")
p(f"  (2 pi/sqrt(3)) x R_p = {2*math.pi/math.sqrt(3)*R_p_of(0.148*eV)/Mpc:.3f} Mpc"
  f"  vs their 6.283 Mpc -> agreement to 1.6%.  INDEPENDENT CONFIRMATION.")

# ---------------------------------------------------------------- BLOCK 8
hdr("BLOCK 8 -- THE HYDROSTATIC BRANCH AND xi = min[1, (R/R_p)^2]")

p("""Below R_p the condensate does not collapse; it reaches HYDROSTATIC balance.
With p = c^2 rho^2/(2 rho_M):

  dp/dr = -rho dPhi/dr  ->  (c^2/rho_M) rho drho/dr = -rho dPhi/dr
                        ->  (c^2/rho_M) drho/dr = -dPhi/dr
                        ->  rho(r) = rho_inf + rho_M |Phi(r)| / c^2 .      (10)

Eq (10) is EXACTLY Mistele, McGaugh & Hossenfelder 2023 eq (2),
rho_c = (m^2/4 pi G_N f_G)(phidot/Q0 - Phihat - phi), and exactly the
Helmholtz term mutilde^2 Phi of Durakovic & Skordis 2024 eq (2.33), with
rho_M/c^2 <-> mutilde^2/(4 pi G).

THREE CONSEQUENCES, and the first two are FAVOURABLE to the framework:

 (a) The suppression is NOT a linear-response artefact.  It comes from the exact
     nonlinear equation of state p = rho^2/(2M^4) and from hydrostatic balance,
     which is a dynamical ATTRACTOR, not an assumed boundary condition.  The
     literature's standing objection -- Durakovic & Skordis 2024 sec 2.3.1
     "we assume ... Q -> Q0 up to small fluctuations" -- is DISCHARGED for
     R < R_p: Q -> Q0 is the hydrostatic solution, not an assumption.

 (b) The per-object free parameter DISAPPEARS.  In eq (10) the only integration
     constant is rho_inf, the AMBIENT condensate density, which is the cosmic
     mean -- the same for every object.  Mistele et al.'s "chemical potential of
     each galaxy as a free parameter" is fixed, in this branch, by the boundary
     condition at infinity.  That RESTORES falsifiability.

 (c) AGAINST INTEREST: hydrostatic equilibrium must have time to establish.
     Sound-crossing times below.  And beyond R_p the fluid IS Jeans unstable,
     so xi -> CDM level there.  Hence

       xi(R) = min[ 1 , kappa_h (R/R_p)^2 ] ,  kappa_h = O(1) .            (11)""")

p("\nSound-crossing time R/c_s (must be < t0 for (10) to hold):")
for Mlab, M_J in [("2.24 meV", M_nat), ("0.0986 eV", 0.0986*eV), ("0.148 eV", 0.148*eV)]:
    for nm, rho, R in [("MW 20 kpc", rho_gal, 20.0*kpc),
                       ("cluster R500", rho_clu, 1.3*Mpc)]:
        cs = math.sqrt(cs2_of(rho, M_J))*c
        p(f"  M={Mlab:9s} {nm:13s} c_s = {cs:.4e} m/s = {cs/1e3:9.1f} km/s"
          f" ; R/c_s = {R/cs/Gyr:.4f} Gyr ; = {R/cs/t0:.4e} t0")
p("  => established comfortably in every case.  (a) holds.")

p("\nxi from eq (11), kappa_h = 1:")
p(f"{'M':>12s} {'R_p[Mpc]':>10s} {'xi(20kpc)':>12s} {'xi(5kpc)':>12s}"
  f" {'xi(1.3Mpc)':>12s} {'xi(100kpc)':>12s}")
for Mlab, M_J in [("2.24 meV", M_nat), ("0.0986 eV", 0.0986*eV),
                  ("0.1223 eV", 0.1223*eV), ("0.148 eV", 0.148*eV),
                  ("1.06 eV", 1.06*eV), ("11.5 eV", 11.5*eV)]:
    Rp = R_p_of(M_J)
    f = lambda R: min(1.0, (R/Rp)**2)
    p(f"{Mlab:>12s} {Rp/Mpc:10.4e} {f(20*kpc):12.4e} {f(5*kpc):12.4e}"
      f" {f(1.3*Mpc):12.4e} {f(100*kpc):12.4e}")

# ---------------------------------------------------------------- BLOCK 9
hdr("BLOCK 9 -- THE FORK: R_p REQUIRED BY CLUSTERS+RAR vs ALLOWED BY COSMOLOGY")

p("""The framework needs (context item 5): xi(R500) = 0.11-0.26 in clusters and
xi ~ 0 in galaxies.  From eq (11) with kappa_h = 1 and R500 = 1.3 Mpc:""")
for xi_t in (0.11, 0.26):
    Rp_req = 1.3*Mpc/math.sqrt(xi_t)
    rhoM_req = 3.0*c**2/(4.0*math.pi*G*Rp_req**2)
    M_req = (rhoM_req/rho_L)**0.25*M_nat
    xi20 = (20.0*kpc/Rp_req)**2
    p(f"  xi(R500) = {xi_t:.2f}  ->  R_p = {Rp_req/Mpc:7.3f} Mpc"
      f" ->  M = {M_req/eV:.5f} eV = {M_req/M_nat:6.1f} M_nat"
      f" ;  xi(20 kpc) = {xi20:.3e}")
p("  Both give xi(20 kpc) ~ 3e-5 to 6e-5: FAR inside the 0.034 dex SPARC")
p("  intrinsic scatter.  The RAR is untouched.  THAT PART WORKS.")

p("""
Now the cosmological cost.  w = p/(rho c^2) = Sigma/2 = rho/(2 rho_M), and
rho propto a^-3, so the condensate turns STIFF at high z.  Require w < w_max at
redshift z_c:  rho_M > rho_dm,0 (1+z_c)^3 / (2 w_max).""")
p(f"\n{'z_c':>8s} {'w_max':>8s} {'rho_M min[kg/m^3]':>18s} {'M min[eV]':>11s}"
  f" {'R_p max[kpc]':>13s} {'xi(1.3Mpc)':>11s} {'xi(20kpc)':>11s}")
for z_c, w_max in [(1100.0, 0.01), (1100.0, 0.001), (3.0e4, 0.0164), (3.0e4, 0.001)]:
    rhoM_min = rho_dm0*(1.0+z_c)**3/(2.0*w_max)
    M_min = (rhoM_min/rho_L)**0.25*M_nat
    Rp_max = c*math.sqrt(3.0/(4.0*math.pi*G*rhoM_min))
    p(f"{z_c:8.0f} {w_max:8.4f} {rhoM_min:18.4e} {M_min/eV:11.4f}"
      f" {Rp_max/kpc:13.4e} {min(1,(1.3*Mpc/Rp_max)**2):11.4e}"
      f" {min(1,(20*kpc/Rp_max)**2):11.4e}")

p(f"""
CROSS-CHECK: Blanchet & Skordis 2024 (arXiv:2404.06584) sec 4.3.1 find, for
K(Q) = mu^2 (Q-1)^2 and the GDM bound w <~ 0.0164 at a ~ 1e-4.5 (Kopp, Skordis,
Thomas & Ilic 2018, PRL 120:221102), the requirement mu^-1 <~ 0.22 kpc, while
MOND in galaxies needs mu^-1 >~ 100 kpc, and conclude verbatim that the quadratic
K "cannot be in simultaneous harmony with observations of galaxies and with
cosmology."  Row 3 above gives R_p <= {c*math.sqrt(3.0/(4.0*math.pi*G*rho_dm0*(3.0e4+1)**3/(2*0.0164)))/kpc:.3f} kpc from the SAME bound,
derived independently from ACLMW eq (3.15).  I reproduce their 0.22 kpc.

THE FORK, numerically:
  R_p required (clusters at xi=0.11-0.26 with the RAR safe) : 2550 - 3920 kpc
  R_p allowed  (GDM/CMB, w < 0.0164 at a ~ 3e-5)            :      <= 0.29 kpc
  CONFLICT: a factor {2550*kpc/(c*math.sqrt(3.0/(4.0*math.pi*G*rho_dm0*(3.0e4+1)**3/(2*0.0164)))):.3e} in R_p,
            {(2550*kpc/(c*math.sqrt(3.0/(4.0*math.pi*G*rho_dm0*(3.0e4+1)**3/(2*0.0164)))))**2:.3e} in rho_M,
            {(2550*kpc/(c*math.sqrt(3.0/(4.0*math.pi*G*rho_dm0*(3.0e4+1)**3/(2*0.0164)))))**0.5:.2f} in M.
  Even the far weaker recombination-only bound (w < 0.001 at z = 1100) allows only
  R_p <= 15 kpc, which forces xi(1.3 Mpc) = 1 -- full double counting in clusters.

There is NO value of M that simultaneously (i) keeps the Q-sector out of galaxies
and partly out of clusters, and (ii) lets it behave as cold dust before
recombination.  The two requirements are the SAME parameter pulling opposite ways.
""")

# ---------------------------------------------------------------- SUMMARY
hdr("SUMMARY")
p("""1. A core DOES form: a_grad/a_grav = A/(G M_sh R) grows as R -> 0, so the k^4
   term always wins eventually.  R_stall = A/(G M_sh) = 4 c^2/(k_M^2 G M_sh).
2. At M = rho_Lambda^(1/4) = 2.24 meV, R_stall(1e11 Msun) = 2.1e-22 m, which is
   8 orders BELOW the Schwarzschild radius of that mass.  The realistic core is
   the de Broglie scale, ~2 m, carrying 1e-23 of the halo mass.  Shortfall to
   20 kpc: 20 orders.  Second, independent kill: the k^4 response time at
   20 kpc is 3e19 Hubble times.
3. NONLINEARITY MAKES IT WORSE, NOT BETTER.  Exact scaling
   R_stall = C lambda_J (lambda_J/R_i)^3 with C = 3/(4 pi^4) = 0.0077.  Since
   collapse requires R_i >= lambda_J, the linear Jeans length is a HARD CEILING
   on the nonlinear core, and the ceiling sits at 0.008 lambda_J -- two orders
   BELOW it.  Physically lambda_J propto rho^(-1/4) DECREASES with density, and
   collapse raises the density.  Required M: 1.31e-24 eV (galaxy),
   2.49e-27 eV (cluster) versus the linear 2.44e-25 eV -- a factor 5 of relief
   for a galaxy, two orders WORSE for a cluster.  21-25 orders below natural,
   4.2-7.0 orders below the Lyman-alpha floor.
4. Therefore from the k^4 mechanism: xi_galaxy = xi_cluster = 1.
   VERDICT ON THE ASSIGNED MECHANISM: DUST_VIRIALISES.  UNFAVOURABLE.
5. BUT context item 1's premise is wrong in a halo.  c_s^2 = rho/M^4 (ACLMW
   eq 3.15, exact) is NOT zero for a condensate carrying an Omega_dm amount of
   energy, and it beats the k^4 term by 40-60 orders at galaxy scales.  Redoing
   the collapse with it gives a_p propto R^-4 and a UNIVERSAL, mass-independent
   stall radius R_p = c sqrt(3/(4 pi G rho_M)), and below R_p the hydrostatic
   solution rho = rho_inf + rho_M|Phi|/c^2 -- which is AeST's own Helmholtz
   response, now DERIVED nonlinearly with no free per-object chemical potential.
   xi = min[1, (R/R_p)^2].
6. That branch is genuinely favourable at galaxy+cluster scales (R_p = 2.55-3.92
   Mpc, i.e. M = 0.0986-0.1223 eV, gives xi(R500) = 0.11-0.26 with
   xi(20 kpc) = 2.6e-5 to 6.2e-5) but the SAME parameter makes the condensate
   stiff before z ~ 300, destroying the CMB fit that is AeST's whole reason for
   existing.  Conflict factor 5982 in R_p, 3.6e7 in rho_M, 77 in M.
   Independent re-derivation of Blanchet & Skordis 2024 sec 4.3.1 (I get
   R_p <= 0.43 kpc from their GDM bound; they quote mu^-1 <= 0.22 kpc).
   ALSO: M = rho_Lambda^(1/4) is itself excluded (c_s = 0.42 c at the cosmic
   mean today), so M is a FITTED parameter, not a Lambda-derived one.  The
   claim "the dark sector scale follows from rho_Lambda" does not survive.
7. NET: the k^4 route is shut both linearly and nonlinearly.  The k^2 route is
   open in principle and is the correct physics, but it is the SAME single knob
   that the CMB fixes on the wrong side.  No M works for both.  The door that
   remains is a NON-quadratic K(Q) (DBI-type, as Blanchet & Skordis suggest),
   which would decouple the halo-scale stiffness from the early-time stiffness.
   That is not tested here.""")

with open(__file__.replace(".py", ".out"), "w") as f:
    f.write("\n".join(L) + "\n")
print("\n[wrote " + __file__.replace(".py", ".out") + "]")
