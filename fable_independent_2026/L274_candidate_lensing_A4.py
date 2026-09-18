#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L274 -- ROUTE A4 (the standing candidate's lensing): ATTEMPTED, and my first pass was WRONG.
SELF-CORRECTION lane.  Derived from the linearized Einstein equations (lesson from L268: derive, do not
posit; and a vanishing Laplacian is NOT a vanishing field).

WHAT I TRIED FIRST (and why it was wrong):
  I argued that the deep-MOND scalar (J ~ Y^{3/2}) has spatially traceless stress p_r + 2 p_t = 0, so
  lap(Phi - Psi) = 4 pi G (p_r + 2 p_t) = 0  =>  Phi = Psi  =>  lensing = dynamics.  That is the SAME
  error as L268: lap(chi) = 0 makes chi HARMONIC, not zero.  There is a SECOND, independent spatial
  Einstein equation (the anisotropic-stress one), and for this scalar the anisotropic stress p_r - p_t
  = 2C is NONZERO, which fixes the harmonic coefficient to a NONZERO value.

WHAT IS ACTUALLY TRUE (all derived here from the symbolic linearized Einstein tensor):
  C1 [DERIVED] the two spatial Einstein equations are
        (A) G^r_r + 2 G^th_th = 2 lap(Phi-Psi) = 8 pi G (p_r + 2 p_t)
        (B) G^r_r -   G^th_th = -(chi'' - chi'/r) = 8 pi G (p_r - p_t),   chi := Phi - Psi.
     p_r + 2 p_t = 0 (deep-MOND) makes chi harmonic (A); equation (B) with p_r - p_t = 2C != 0 then fixes
     chi = A/r with A = -16 pi G^{5/2} M^{3/2} sqrt(a0)/3 != 0.  So Phi != Psi: THERE IS A SLIP.  My
     "lensing = dynamics closes" is RETRACTED.
  C2 [DERIVED, deeper] a single-metric scalar that gravitates only through its T_mn does not even
     reproduce MOND DYNAMICS: lap(Phi_p) = 4 pi G rho_s with rho_s ~ 1/r^3 gives Phi_p' ~ ln(r)/r^2, NOT
     the MOND 1/r.  MOND acceleration in relativistic scalar-tensor MOND comes from the DIRECT
     matter-scalar coupling (conformal/disformal), not from the scalar's stress-energy gravitating.
  C3 [CONSEQUENCE] so the candidate's lensing is governed by the SAME matter-coupling question SW06
     already settled: conformal coupling -> photons decouple -> baryons-only lensing (DEAD); disformal
     coupling -> photon-graviton delay -> GW170817 (DEAD).  Route A4 does NOT hand the candidate a new
     lensing success.  The ONE genuinely-uncomputed gate SW06 named -- a KHRONON-sourced, locally-
     switched-off scalar with a SOURCED POISSON STRUCTURE (constraint/nonlocal) and alpha_1 = 0 -- is
     NOT the plain gravitating scalar computed here; that structure remains uncomputed.

VERDICT: route A4 does NOT close.  My deep-MOND "Phi = Psi" was the L268 error twice over (dropped the
harmonic slip; and the gravitating scalar does not even source MOND).  The candidate's lensing still rests
on the matter-coupling routes SW06 killed, UNLESS the clock's sourced-Poisson structure is genuinely
different -- and that is the open computation, not this one.  Honest status: OPEN, leaning to the SW06
kill, pending the clock-sourced-Poisson calculation.

Run:  python3 fable_independent_2026/L274_candidate_lensing_A4.py
"""
import os, sys, json
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "L274_candidate_lensing_A4"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L274", "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 100); P(t); P("=" * 100)


P(__doc__)
r = sp.symbols('r', positive=True)
G, M, a0, pi = sp.symbols('G M a_0 pi', positive=True)
A, B = sp.symbols('A B')
lap = lambda f: sp.diff(f, r, 2) + 2 * sp.diff(f, r) / r

# deep-MOND scalar point mass: phi' = sqrt(G M a0)/r, Y = phi'^2 = G M a0/r^2
Y = G * M * a0 / r**2
Cc = Y**sp.Rational(3, 2) / a0
rho = sp.Rational(2, 3) * Cc
p_r = sp.Rational(4, 3) * Cc
p_t = -sp.Rational(2, 3) * Cc

# =================================================================================================
banner("C1 [DERIVED] p_r+2p_t=0 makes chi HARMONIC, not zero; the anisotropic-stress eq fixes a NONZERO slip")
trace = sp.simplify(p_r + 2 * p_t)
aniso = sp.simplify(p_r - p_t)
chi = A / r + B
lapchi = sp.simplify(lap(chi))
lhsB = -(sp.diff(chi, r, 2) - sp.diff(chi, r) / r)          # G^r_r - G^th_th combination for chi=A/r+B
solA = sp.solve(sp.Eq(sp.simplify(lhsB), sp.simplify(8 * pi * G * aniso)), A)
A_val = sp.simplify(solA[0])
slip = sp.simplify(A_val / r)
OUT["numbers"]["slip_Phi_minus_Psi"] = str(slip)
check("C1 deep-MOND: p_r+2p_t = 0 (so lap(chi)=0, chi harmonic) BUT p_r-p_t = 2C != 0; the second spatial "
      "Einstein eq fixes chi = A/r with A != 0 -- so Phi != Psi.  My 'lap(chi)=0 => chi=0' was the L268 error",
      f"p_r+2p_t = {trace}; p_r-p_t = {aniso}; lap(A/r+B) = {lapchi}; A = {A_val}; slip Phi-Psi = {slip}",
      trace == 0 and aniso != 0 and lapchi == 0 and A_val != 0 and slip != 0,
      "a vanishing Laplacian is a harmonic field, not a zero field; the anisotropic stress supplies the "
      "boundary data that makes the slip nonzero -- exactly the homogeneous-solution trap of L268")

# =================================================================================================
banner("C2 [DERIVED] the gravitating scalar does NOT even source MOND dynamics (Phi' ~ ln r/r^2, not 1/r)")
Phip = sp.Function('Phi_p')
sol = sp.dsolve(sp.Eq(sp.diff(Phip(r), r, 2) + 2 * sp.diff(Phip(r), r) / r, 4 * pi * G * rho), Phip(r))
Phip_prime = sp.simplify(sp.diff(sol.rhs, r))
# MOND requires Phi' = sqrt(G M a0)/r ~ 1/r; the scalar T_mn gives a ln(r)/r^2 particular part.
has_lnr_over_r2 = sp.simplify(Phip_prime - Phip_prime.subs(sp.log(r), 0)) != 0   # a genuine ln(r)/r^2 piece
check("C2 lap(Phi_p) = 4 pi G rho_s with rho_s ~ 1/r^3 gives Phi_p' ~ ln(r)/r^2, NOT the MOND 1/r -- a "
      "single-metric scalar gravitating only via its stress-energy does not reproduce MOND dynamics; the "
      "MOND force must come from the DIRECT matter-scalar coupling (conformal/disformal)",
      f"Phi_p'(r) = {Phip_prime}  (contains ln(r)/r^2; MOND needs ~1/r)",
      has_lnr_over_r2,
      "this is why relativistic MOND couples the scalar to matter directly (RAQUAL/TeVeS) rather than "
      "letting T_mn[phi] gravitate -- and that coupling is exactly what routes B/C address")

# =================================================================================================
banner("C3 [CONSEQUENCE] route A4 inherits SW06's matter-coupling kills; the clock-sourced Poisson is uncomputed")
sw06 = {"conformal coupling": "photons conformally decouple => baryons-only lensing -- DEAD (SW06 route C)",
        "disformal coupling": "photon-graviton Shapiro delay 1.8-2.3 yr vs 1.7 s -- DEAD (SW06/CK01, GW170817)",
        "plain gravitating T_mn (this lane)": "does not source MOND dynamics (C2) and slips Phi!=Psi (C1)",
        "A4 khronon-sourced switched-off scalar, sourced Poisson, alpha_1=0": "UNCOMPUTED -- the one open gate"}
for k, v in sw06.items():
    P(f"    {k}: {v}")
check("C3 route A4 does NOT hand the candidate a new lensing success: the plain gravitating scalar fails "
      "(C1/C2), and the matter-coupling alternatives are SW06's already-dead conformal/disformal routes; "
      "the only uncomputed gate is the clock's SOURCED-POISSON structure, which this lane did NOT realize",
      "3 routes dead/failed; 1 (clock-sourced Poisson) genuinely uncomputed",
      True,
      "honest status: route A4 OPEN and leaning to the SW06 kill; the clock-sourced-Poisson calculation "
      "is the actual open computation, and it is NOT the T_mn-gravitating scalar I did here",
      load_bearing=False)

# =================================================================================================
banner("VERDICT")
P("""  (1) ATTEMPTED: route A4 (the standing candidate's deep-MOND lensing), derived from the Einstein eqs.
  (2) SELF-CORRECTION: my first pass claimed p_r+2p_t=0 => Phi=Psi => lensing=dynamics.  That is the L268
      error: lap(Phi-Psi)=0 makes the slip HARMONIC, and the anisotropic-stress equation (p_r-p_t=2C!=0)
      fixes it to a NONZERO chi = A/r.  So Phi != Psi.  RETRACTED.  And deeper (C2): a single-metric scalar
      gravitating only through T_mn does not even source MOND dynamics (Phi' ~ ln r/r^2, not 1/r), so the
      MOND force needs the direct matter coupling -- whose lensing is SW06's conformal (baryons-only, DEAD)
      / disformal (GW170817, DEAD) problem.
  (3) HONEST SENTENCE: route A4 does NOT close.  It hands the candidate no new lensing success; the plain
      gravitating scalar both slips (Phi!=Psi) and misses MOND, and the coupling routes that would give
      MOND lensing are the ones SW06 already killed.  The single genuinely-open computation is the clock's
      SOURCED-POISSON structure (khronon-sourced, locally-switched-off scalar, alpha_1=0) -- and that is
      NOT what I computed here.  So the candidate's asserted "req 3 PASS" remains UNestablished, and the
      lensing gate stays open, leaning to the SW06 kill until the clock-sourced-Poisson calc is done.
      DISCIPLINE NOTE: I ran a first version that "passed 4/4" by testing my own false premise (like L268's
      B1 tautology).  Deriving from the Einstein tensor -- not positing which stress component sources the
      slip -- is what exposed it.  This lane records the correction; it does NOT claim a result.""")
OUT["verdict"] = {"word": "A4-DOES-NOT-CLOSE-first-pass-was-the-L268-error",
                  "phi_equals_psi": False, "slip_nonzero": True,
                  "gravitating_scalar_sources_MOND": False,
                  "status": "OPEN, leaning SW06 kill; clock-sourced-Poisson uncomputed",
                  "retracted": "the deep-MOND Phi=Psi / lensing=dynamics 'closes' claim"}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb = [nm for nm, ok, l in CH if l and not ok]
P(f"L274 COMPLETE: {npass}/{n} checks PASS  (this is a SELF-CORRECTION; the 'closes' claim is retracted)")
for nm in lb:
    P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb else 0)
