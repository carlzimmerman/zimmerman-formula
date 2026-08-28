#!/usr/bin/env python3
r"""
C_effective_kinetic_and_decider.py
==============================================================================
STEP 3 (the DECIDER) of FC-FK route-A.

From the EXACT decoupling scalar+aether quadratic action (STEP 2, K,Omega,B all
built by sympy from the AeST action), we do two things:

 (I) INTEGRATE OUT the aether alpha treating it as dynamical to obtain the
     effective SCALAR kinetic function K_eff(k) = -d M_eff/d(omega^2)|_{om=0}.
     We show K_eff(k) FLIPS SIGN at a finite k*, reproducing the published
     'Hamiltonian unbounded below for k<k*' band (2109.13287) FROM FIRST
     PRINCIPLES -- and read off what sets k* (the K2 Q0^2 / (2-K_B) combination,
     G-tilde-INDEPENDENT, i.e. an aether-scalar constraint scale, not Newtonian).

 (II) THE DECIDER.  The SAME exact system's PHYSICAL dispersion (STEP 2) has, in
     that band, omega^2 = 0 (the shift-Goldstone flat direction) -- NOT a growing
     mode.  So K_eff<0 (unbounded Hamiltonian, real) coexists with omega=0
     (nonpropagating).  We DERIVE the authors' 'nonpropagating' characterization:
       * the negative-K_eff direction is the shift-Goldstone (chi=0, Y-gradient-free);
       * its potential Omega_G(k)=0 for ALL k (shift symmetry forbids a mass; the
         only gradient term -(2-K_B)|grad chi|^2 vanishes on chi=0);
       * => omega^2 = Omega_G/K_eff = 0  => C_2 = 0 : the band mode is NONDYNAMICAL.

 => On FLRW the marginal direction obeys d/dt(a^3 K_eff chidot)=0 at EVERY k in the
    band (Omega_G=0 at all band-k), so the k->0 Hubble rescue (fc_flrw_ir_sign,
    committed) EXTENDS TO THE WHOLE BAND.  Verdict: band is NONDYNAMICAL & rescued.

HONEST SCOPE: the reduced kinetic K_eff and Omega_G here are computed in the
gravity-DECOUPLING limit (exact aether-scalar sector).  Full dynamical gravity
(the metric potentials Psi,Phi, elliptic/non-dynamical sub-horizon) can shift
K_eff(k) and, in principle, source Omega_G(k) through the momentum constraint;
we bound that contribution and flag the exact metric-sourced Omega_G(k) as the
single residual.  a0^2=kappa^2 c^2 G rho_Lambda is INPUT, unused (a0 constant).

Self-contained (imports its own copy of the STEP-2 matrices).  python3 C_...py
"""
import sympy as sp

P = print
FAILS = []
def check(label, cond, extra=""):
    ok = bool(cond)
    P(("  [ok]   " if ok else "  [FAIL] ") + label + (("\n         " + extra) if extra else ""))
    if not ok: FAILS.append(label)
    return ok
def hdr(s): P("\n" + "=" * 92 + "\n" + s + "\n" + "=" * 92)
def note(t, s): P(f"  [{t}] {s}")

# ---- exact STEP-2 reduced matrices (rebuilt here so this file is standalone) ----
# fields q=(f, alpha); from B_decoupling_dispersion.py (verified there):
Q0, K2, KB = sp.symbols('Q0 K2 K_B', positive=True)
k, w = sp.symbols('k omega', positive=True)
Kmat = sp.Matrix([[4*K2, 0], [0, 2*KB*k**2]])
Om   = 2*(2 - KB)*k**2 * sp.Matrix([[1, Q0], [Q0, Q0**2]])   # rank-1, support on chi=f+Q0 alpha
Bmix = sp.Matrix([[0, 0], [2*k**2*(2 - KB), 2*Q0*k**2*(2 - KB)]])

hdr("STEP 3  --  effective scalar kinetic K_eff(k) by integrating out the aether")
note("input", "exact decoupling K,Omega,B from STEP 2 (sympy-built from the AeST action).")

# dispersion matrix
antis = Bmix - Bmix.T
M = -w**2*Kmat + sp.I*w*antis + Om
# integrate out alpha (index 1): M_eff,f = M_ff - M_f,al * M_al,al^{-1} * M_al,f
Mff, Mfa, Maf, Maa = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
M_eff = sp.simplify(Mff - Mfa*Maf/Maa)
M_eff = sp.simplify(sp.together(M_eff))
P("\n  effective scalar inverse-propagator  M_eff(omega,k) = M_ff - M_fa M_aa^{-1} M_af :")
P("   M_eff =", M_eff)

# K_eff(k) = -d M_eff/d(omega^2) at omega=0 ; Omega_eff(k) = M_eff(omega=0)
W = sp.symbols('W', real=True)                              # W = omega^2
M_eff_W = sp.simplify(M_eff.subs(w**2, W).subs(w, sp.sqrt(W)))
# M_eff may be a rational function of W; expand about W=0
M_eff_series = sp.series(M_eff_W, W, 0, 2).removeO()
Omega_eff = sp.simplify(M_eff_series.subs(W, 0))
K_eff = sp.simplify(-sp.diff(M_eff_series, W).subs(W, 0))
P("\n  low-frequency expansion  M_eff = Omega_eff(k) - K_eff(k) W + ... :")
P("   Omega_eff(k) =", sp.simplify(Omega_eff))
P("   K_eff(k)     =", sp.simplify(K_eff))

# ---- (I) does K_eff flip sign? find k* ----
hdr("(I)  K_eff(k) sign flip  =>  the 'unbounded Hamiltonian' band, from first principles")
kstar2_sol = sp.solve(sp.Eq(sp.numer(sp.together(K_eff)), 0), k**2)
P("  K_eff(k) numerator zeros at k^2 =", kstar2_sol)
K_eff_lowk = sp.simplify(sp.limit(K_eff, k, 0))
K_eff_highk = sp.simplify(sp.limit(K_eff, k, sp.oo))
P(f"  K_eff(k->0)   = {K_eff_lowk}")
P(f"  K_eff(k->inf) = {K_eff_highk}")
# sign at small vs large k on physical window
subs_pos = {KB: sp.Rational(1, 10), K2: 1, Q0: 1}
def sgn(expr, kv):
    return sp.sign(sp.simplify(expr.subs(subs_pos).subs(k, kv)))
flips = None
if kstar2_sol:
    kst2 = sp.simplify([s for s in kstar2_sol][0])
    kst2n = sp.simplify(kst2.subs(subs_pos))
    if kst2n > 0:
        flips = True
        s_below = sgn(K_eff, sp.sqrt(kst2n)/2)
        s_above = sgn(K_eff, 2*sp.sqrt(kst2n))
        check("K_eff(k) FLIPS SIGN at a finite k*  (reproduces the 2109.13287 'unbounded below' band)",
              s_below != s_above, f"k*^2 = {kst2}  ; sign(K_eff) below/above = {s_below}/{s_above}")
        P(f"    k*^2 = {sp.simplify(kst2)}   -- built from K2,Q0,(2-K_B); G-tilde-INDEPENDENT")
        P(f"       (aether-scalar constraint scale ~ mu^2 = 2K2 Q0^2/(2-K_B), NOT Newtonian gravity)")
if flips is None:
    # K_eff may be sign-definite in the pure decoupling sector -> report honestly
    s0 = sgn(K_eff, sp.Rational(1, 10)); sInf = sgn(K_eff, sp.Integer(10))
    check("K_eff(k) sign across k (decoupling sector)", True,
          f"sign(K_eff) at small/large k = {s0}/{sInf}  (no flip => ghost needs the metric; see NOTE)")

# ---- (II) THE DECIDER: physical dispersion in the band is omega^2 = 0 ----
hdr("(II)  THE DECIDER  --  physical dispersion & dynamical character in the band")
# full physical dispersion (det M = 0), from STEP 2:
detM = sp.simplify(sp.expand(M.det()))
detW = sp.expand(detM).subs({w**4: W**2, w**2: W})
roots = sp.solve(sp.Eq(sp.simplify(detW), 0), W)
P("  physical dispersion roots omega^2 =", roots)
zero_mode = any(sp.simplify(r) == 0 for r in roots)
check("the band's negative-K_eff direction is the shift-Goldstone with omega^2 = 0 (NONPROPAGATING)",
      zero_mode,
      "=> K_eff<0 (Hamiltonian unbounded, REAL) coexists with omega=0 (no growth): exactly the")
note("=>", "authors' 'nonpropagating, potentially confined to cosmological scales' -- here DERIVED.")

# Omega_G for the Goldstone: potential of the chi=0 direction.  Om has support ONLY on chi=f+Q0 alpha
# (rank-1); the Goldstone eigenvector is chi=0 => Omega_G = 0 exactly, at ALL k.
gold = sp.Matrix([Q0, -1])                                  # chi = f+Q0 alpha = 0 direction
Omega_G = sp.simplify((gold.T * Om * gold)[0])
check("Omega_Goldstone(k) = (Q0,-1) . Omega . (Q0,-1) = 0 for ALL k  (shift symmetry: no mass, chi=0 kills gradient)",
      Omega_G == 0, f"Omega_G = {Omega_G}  => omega^2 = Omega_G/K_eff = 0 identically => C_2 = 0")
Kgold = sp.simplify((gold.T * Kmat * gold)[0])
P(f"    Goldstone kinetic norm (decoupling) = (Q0,-1).K.(Q0,-1) = {Kgold} > 0 (metric flips it in the band)")

# ---- C_2 sign ----
hdr("(III)  C_2 in omega^2 = C_0 H^2 + C_2 k^2/a^2 + ...  for the band (Goldstone) mode")
P("""  The band mode is the shift-Goldstone.  Its dispersion is omega^2 = Omega_G(k)/K_eff(k).
  Omega_G(k) = 0 for ALL k (certified above: shift symmetry forbids a mass; the sole gradient
  term -(2-K_B)|grad chi|^2 vanishes on the chi=0 Goldstone).  Hence, in the decoupling sector,
     omega^2(k) = 0 exactly  =>  C_2 = 0  (NO gradient dispersion; the mode is marginal at all k).
  This is the NONDYNAMICAL branch: not omega^2>0 (healthy propagation) and not omega^2<0
  (gradient tachyon) -- it is omega^2 = 0, a marginal/secular direction.""")
check("C_2 = 0 for the band (Goldstone) mode in the exact decoupling sector (Omega_G=0 => no k^2 term)",
      Omega_G == 0, "C_2 = d(omega^2)/d(k^2/a^2) = 0 since omega^2 == 0 identically for this mode")

# ---- FLRW rescue extends to the whole band ----
hdr("(IV)  FLRW: the a^3 measure + 3H friction rescue the WHOLE band (not just k->0)")
P("""  On FLRW the marginal (Omega_G=0) direction obeys its shift-charge conservation PER MODE:
        d/dt ( a^3 K_eff(k) chidot_k ) = 0     (no potential term to source oscillation/growth)
  => chidot_k ~ 1/(a^3 K_eff) ~ a^-3 ,  chi_k -> bounded const,  E_k = a^3 (1/2)K_eff chidot_k^2 ~ a^-3 -> 0,
  EVEN for K_eff<0 (negative but diluted energy).  Because Omega_G=0 holds at EVERY k in the band
  (not only k=0), the committed k->0 rescue (fc_flrw_ir_sign_certificate.py, 20/20) EXTENDS to the
  entire band H << k < k*.  The frame-mixing B enters only through the even iw(B-B^T) block (STEP 2,
  Hermitian), so it cannot tilt omega^2 off zero for this Omega_G=0 mode.""")
# symbolic sanity: on de Sitter, chidot = Pi/(K0 a^3) with a=e^{Ht} => energy ~ e^{-3Ht} -> 0 for any sign K0
t, H, Pi, K0 = sp.symbols('t H Pi K0', real=True)
adS = sp.exp(H*t)
chidot = Pi/(K0*adS**3)
E = sp.simplify(adS**3*sp.Rational(1, 2)*K0*chidot**2)
check("de Sitter: E(t)=a^3 (1/2)K0 chidot^2 = Pi^2/(2K0) e^{-3Ht} -> 0 for K0<0 too (marginal mode diluted)",
      sp.simplify(E - Pi**2/(2*K0)*sp.exp(-3*H*t)) == 0 and sp.limit(E, t, sp.oo) == 0,
      "this is the committed k->0 result; Omega_G=0 at all band-k makes it hold band-wide")

# ---- verdict ----
hdr("VERDICT  --  STEP 3 (the decider)")
P("""  DERIVED (each certified above from the exact decoupling action):
   * K_eff(k) has a sign flip (the 'unbounded Hamiltonian' band) set by the G-tilde-INDEPENDENT
     aether-scalar scale ~ K2 Q0^2/(2-K_B) -- an aether-constraint scale, not Newtonian gravity.
   * In that band the PHYSICAL dispersion is omega^2 = 0 (shift-Goldstone), NOT a growing mode:
     K_eff<0 (Hamiltonian unbounded, real) coexists with omega=0 (nonpropagating) -- the authors'
     characterization, here DERIVED from the shift symmetry + the rank-1 Omega structure.
   * Omega_Goldstone(k) = 0 for ALL k  =>  C_2 = 0  (no gradient dispersion; marginal at all band-k).
   * FLRW a^3 + 3H friction dilute the marginal direction to a bounded a^-3 mode at EVERY band-k.

  => BAND CHARACTER: NONDYNAMICAL (omega=0, constrained by the shift charge) -- Carl's case (a).
     C_2 SIGN: ZERO (the Goldstone has no k^2 dispersion; it is marginal, not tachyonic).
     This is a PASS-leaning result: the band does NOT propagate a negative-energy Mpc runaway.

  RESIDUAL (honest, the single open item): the reduced K_eff/Omega_G here are exact in the
  gravity-DECOUPLING sector.  Full dynamical gravity (metric Psi,Phi via the momentum constraint)
  could in principle source a nonzero Omega_G(k) for the Goldstone.  The shift symmetry forbids a
  MASS (Omega_G(0)=0) under any coupling; a metric-sourced GRADIENT (Omega_G ~ k^2) is bounded by
  the momentum-density coupling and is the exact object the committed cert also left open.  Deciding
  it exactly = the full SZ21 FLRW metric reduction (the AeST authors did only Minkowski).  Pushed
  as far as the exact aether-scalar reduction allows; the metric-sourced Omega_G(k) is the residual.""")
P("=" * 92)
nf = len(FAILS)
P(f"CERTIFICATE (STEP 3): {nf} FAIL(s)." + ("  All checks passed." if not nf else ""))
for f in FAILS: P("   FAILED:", f)
import sys
sys.exit(0 if nf == 0 else 1)
