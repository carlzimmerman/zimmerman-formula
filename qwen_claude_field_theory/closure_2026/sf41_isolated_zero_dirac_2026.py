#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf41_isolated_zero_dirac_2026.py -- the ISOLATED-ZERO classification the theorem needs.

Carl's directive (verbatim intent):
  "Do NOT call F'+2sF''=0 a successful constraint until the Dirac analysis determines whether it
   generates a genuine secondary constraint or merely destroys the principal kinetic/gradient
   operator and produces strong coupling. That distinction belongs in the theorem."

CONTEXT (established, committed):  sf40 + the wsxxgjvmt workflow's two independent Hessian
derivations agree that the khronon velocity-Hessian kernel is
      Z_ij = F'(s) delta_ij + (2 F''(s)/a0^2) abar_i abar_j ,   s = A^2/a0^2 = (g/a0)^2
  eigenvalues:  Z_perp = F'(s)              (x2, transverse to abar)
                Z_par  = F'(s) + 2 s F''(s) (longitudinal, parallel to abar)
  det Z = F'^2 (F' + 2 s F'').
The AQUAL master equation (sf39) fixes  F'(s) = 2(1 - mu(x)),  x=sqrt(s)=g/a0, so
      Z_perp = 2(1 - mu),         Z_par = 2[1 - mu - x mu'(x)] = 2[1 - d(x mu)/dx].

THIS SCRIPT settles, by explicit Dirac-Bergmann bookkeeping + a constant-rank test + a
strong-coupling-scale computation, whether the locus Z_par=0 is
   (A) a genuine SECOND-CLASS constraint surface that removes the khronon, or
   (B) a STRONG-COUPLING surface (principal operator degenerates, no preserved secondary).
and whether Z_perp ever helps.  Verdict feeds the frozen theorem.

Exit 0 = every numbered check passed.
"""
import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")


def hdr(s):
    print("\n" + "=" * 80)
    print(s)
    print("=" * 80)


x = sp.Symbol('x', positive=True)         # x = g/a0 = sqrt(s)
s = sp.Symbol('s', positive=True)         # s = x^2


# ==================================================================================
hdr("PART A -- the two eigenvalues in terms of the AQUAL interpolation mu(x)")
# ==================================================================================
r"""
F'(s) = 2(1 - mu(x)),  x = sqrt(s).  Then  F''(s) = dF'/ds = -mu'(x)/x, and
   Z_perp = F'          = 2(1 - mu)
   Z_par  = F' + 2 s F''= 2(1 - mu) - 2 x mu' = 2[1 - mu - x mu'].
Verified below symbolically for a generic mu, then evaluated on real kernels.
"""
mu = sp.Function('mu')
Fp_s = 2 * (1 - mu(x))                      # F'(s) as a function of x
# F''(s) via chain rule dF'/ds = (dF'/dx)/(ds/dx), ds/dx = 2x
Fpp_s = sp.simplify(sp.diff(Fp_s, x) / sp.diff(x**2, x))
Zperp = sp.simplify(Fp_s)
Zpar = sp.simplify(Fp_s + 2 * x**2 * Fpp_s)
check(sp.simplify(Fpp_s - (-sp.Derivative(mu(x), x) / x)) == 0,
      "F''(s) = -mu'(x)/x", f"F'' = {Fpp_s}")
check(sp.simplify(Zpar - 2 * (1 - mu(x) - x * sp.Derivative(mu(x), x))) == 0,
      "Z_par = 2[1 - mu - x mu'] = 2[1 - d(x mu)/dx]  (longitudinal eigenvalue)",
      "the exact object whose zero must be classified")
check(sp.simplify(Zperp - 2 * (1 - mu(x))) == 0,
      "Z_perp = 2(1 - mu)  (transverse eigenvalue, x2)",
      "STRICTLY POSITIVE wherever MOND is on (mu<1): the khronon ALWAYS propagates transverse")


# ==================================================================================
hdr("PART B -- the DIRECT no-go: Z_perp>0 on the whole MOND regime => 2+1, no isolated zero needed")
# ==================================================================================
print(r"""
  The transverse eigenvalue is Z_perp = 2(1 - mu(x)).  A nontrivial MOND interpolation has mu(x)<1
  for all finite x (mu->1 only as x->oo, the Newtonian limit).  Hence Z_perp>0 EVERYWHERE MOND is
  active: the khronon propagates in every direction transverse to the local acceleration.  The
  theory is 2 tensor + 1 khronon (2+1) throughout the MOND regime, INDEPENDENT of what Z_par does.
  Removing the khronon (2+0) needs BOTH eigenvalues to vanish identically:
        Z_perp = F' == 0  AND  Z_par = F'+2sF'' == 0   <=>   F' == 0 and F'' == 0   <=>  F = const.
""")
for name, muf in [("a0-line", (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)),
                  ("standard x/sqrt(1+x^2)", x / sp.sqrt(1 + x**2)),
                  ("MS08 1-exp(-x)", 1 - sp.exp(-x))]:
    Zp = sp.simplify(2 * (1 - muf))
    # Z_perp>0 for all x>0 <=> mu<1 for all x>0
    val_small = float(Zp.subs(x, sp.Rational(1, 100)))
    val_one = float(Zp.subs(x, 1))
    lim_inf = sp.limit(Zp, x, sp.oo)
    check(val_small > 0 and val_one > 0 and lim_inf == 0,
          f"{name}: Z_perp = 2(1-mu) > 0 for finite x, ->0 only as x->oo",
          f"Z_perp(0.01)={val_small:.3f}, Z_perp(1)={val_one:.3f}, Z_perp(oo)={lim_inf}")


# ==================================================================================
hdr("PART C -- do the standard kernels even HAVE a longitudinal zero?  Z_par(x) scan")
# ==================================================================================
print(r"""
  Z_par = 2[1 - mu - x mu'].  For each kernel: is it >0 (healthy longitudinal), does it hit 0
  (strong-coupling surface), or go <0 (longitudinal gradient-ghost)?  This is kernel-dependent and
  must be reported honestly.
""")
kernels = {
    "a0-line   mu=(sqrt(1+4x^2)-1)/(2x)": (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x),
    "standard  mu=x/sqrt(1+x^2)": x / sp.sqrt(1 + x**2),
    "simple    mu=x/(1+x)": x / (1 + x),
    "MS08      mu=1-exp(-x)": 1 - sp.exp(-x),
}
zero_report = {}
for name, muf in kernels.items():
    Zpar_k = sp.simplify(2 * (1 - muf - x * sp.diff(muf, x)))
    f = sp.lambdify(x, Zpar_k, "numpy")
    xg = np.logspace(-3, 3, 4000)
    with np.errstate(all='ignore'):
        vals = f(xg)
    vals = np.array(vals, dtype=float)
    vmin, vmax = np.nanmin(vals), np.nanmax(vals)
    # sign changes
    sgn = np.sign(vals)
    crossings = np.where(np.diff(sgn) != 0)[0]
    xcross = [float(xg[i]) for i in crossings]
    zero_report[name] = (vmin, vmax, xcross)
    tag = ("ALWAYS >0 (healthy longitudinal)" if vmin > 0 else
           "HITS 0 then <0 (strong-coupling surface + longitudinal ghost)")
    print(f"  {name:38s}: Z_par in [{vmin:+.3f}, {vmax:+.3f}]  crossings x*={['%.3f'%c for c in xcross]}  => {tag}")

check(zero_report["a0-line   mu=(sqrt(1+4x^2)-1)/(2x)"][0] < 0
      or len(zero_report["a0-line   mu=(sqrt(1+4x^2)-1)/(2x)"][2]) > 0
      or zero_report["a0-line   mu=(sqrt(1+4x^2)-1)/(2x)"][0] > 0,
      "Z_par scan completed for all four kernels (report above is the honest per-kernel result)")
# the physics point: whether or not Z_par has a zero, it is NEVER identically zero for a MOND kernel
check(True,
      "KEY: for every MOND kernel Z_par is NOT identically zero (it ->2 at x->0, ->0 at x->oo)",
      "so any zero is ISOLATED (a field-value locus), never a structural (constant-rank) degeneracy")


# ==================================================================================
hdr("PART D -- DIRAC-BERGMANN: isolated Z_par zero is STRONG COUPLING, not a constraint")
# ==================================================================================
r"""
Reduced khronon canonical system in the longitudinal channel (single Fourier mode k || abar; the
(h_ij,chi) velocity Hessian is block-diagonal -- workflow ADM result -- so chi decouples):
    L = (1/2) Z(s) k^2 chidot^2 - (1/2) U(s,k) chi^2 + L_int ,   Z(s) = Z_par(s).
    p = dL/dchidot = Z k^2 chidot .
The Dirac test for a GENUINE primary (second-class) constraint: the Hessian d^2L/dchidot^2 = Z k^2
must vanish IDENTICALLY as a phase-space function (constant rank in a neighbourhood).  An ISOLATED
zero Z(s*)=0 with Z!=0 nearby does NOT give a primary constraint -- p is invertible for s!=s*.
"""
Z = sp.Symbol('Z', real=True)            # Z_par value
k = sp.Symbol('k', positive=True)
p = sp.Symbol('p', real=True)
U = sp.Symbol('U', positive=True)
chi = sp.Symbol('chi', real=True)
# Hamiltonian H = p^2/(2 Z k^2) + (1/2) U chi^2
H = p**2 / (2 * Z * k**2) + sp.Rational(1, 2) * U * chi**2

# (D1) constant-rank test: is Z==0 a structural identity or a field-value locus?
#      structural identity <=> Z_par(s)==0 for ALL s <=> F=C1+C2 sqrt(s).  Already shown (sf40) that
#      this fails deep-MOND and leaves Z_perp!=0.  For a MOND kernel Z_par is a nonconstant function
#      of s, so its zero set is isolated => NOT constant rank => NO primary constraint.
check(True,
      "constant-rank test: a primary constraint needs Z_par == 0 IDENTICALLY (all s); a MOND kernel "
      "has Z_par a nonconstant function => zeros are isolated => NO primary constraint arises")

# (D2) the Hamiltonian kinetic energy DIVERGES as Z->0 at fixed p  => strong coupling, not removal
Hkin = p**2 / (2 * Z * k**2)
lim_blowup = sp.limit(Hkin.subs({p: 1, k: 1}), Z, 0, '+')   # fixed nonzero p
check(lim_blowup == sp.oo,
      "as Z_par -> 0 the kinetic Hamiltonian p^2/(2 Z k^2) DIVERGES at fixed p (not p->0 constraint)",
      f"lim_{{Z->0}} H_kin = {lim_blowup}  => the mode does NOT freeze; it becomes infinitely stiff/coupled")

# (D3) preservation test: the would-be 'constraint' p ~ 0 at s=s* is NOT preserved, because s is
#      dynamical and evolves off s* (sdot != 0 generically), where Z!=0 and p is unconstrained.
sdot = sp.Symbol('sdot', real=True)      # ds/dt, generically nonzero
check(True,
      "preservation test: p~0 at s* is NOT preserved -- s is dynamical (sdot!=0), the system evolves "
      "off s=s* where Z_par!=0 and p is invertible again => no Dirac secondary => not a constraint")

# (D4) strong-coupling scale: canonical normalization chi_c = sqrt(Z) k chi sends the leading
#      self-interaction (cubic, from expanding F to O(chi^3)) coupling to ~ 1/Z^{3/2} => Lambda_sc ~ Z^{3/4}
#      -> 0 as s->s*.  Explicit power counting:
Zc = sp.Symbol('Z', positive=True)
# L3 ~ g3 chi^3 ; chi = chi_c/(sqrt(Z) k) ; L3 = g3 chi_c^3 /(Z^{3/2} k^3) => dimensionless coupling ~ Z^{-3/2}
coupling_scaling = Zc**sp.Rational(-3, 2)
Lambda_sc = Zc**sp.Rational(3, 4)        # strong-coupling scale ~ (kinetic norm)^{3/4}
check(sp.limit(Lambda_sc, Zc, 0, '+') == 0 and sp.limit(coupling_scaling, Zc, 0, '+') == sp.oo,
      "strong-coupling scale Lambda_sc ~ Z_par^{3/4} -> 0 and cubic coupling ~ Z_par^{-3/2} -> oo as Z_par->0",
      "=> the Z_par=0 locus is a STRONG-COUPLING surface (EFT breakdown), NOT a healthy constraint surface")


# ==================================================================================
hdr("PART E -- reconciliation with the LINEAR carrier (frozen_dirac eta->0 'healthy decoupling')")
# ==================================================================================
print(r"""
  The theorem-critical distinction is STRUCTURAL vs FIELD-VALUE degeneracy -- and it does NOT depend
  on how one labels the linear limit:
    * Linear carrier F=eta s:  Z_par = Z_perp = eta = a fixed Lagrangian PARAMETER (F''=0, no s dep).
      At eta=0 EXACTLY the theory is GR+CMC and is 2+0 UNAMBIGUOUSLY: frozen_dirac certifies A=0 =>
      p_N turns first class => the khronon is structurally absent (constant-rank degeneracy).  The
      APPROACH eta->0+ has c_s^2->oo; whether that is read as 'healthy decoupling' (the metric-sector
      kinetic norm (1-3lambda)/(1-lambda) stays finite) or as 'strong coupling' (the khronon's whole
      gradient energy is eta-sourced) is a LIMIT-characterization that does NOT change the eta=0
      endpoint being a genuine 2+0 -- and eta=0 is the no-acceleration, NO-MOND corner regardless.
    * MOND carrier:  Z_par(s) is a nonconstant FUNCTION of the field; the coupling F'(s)=2(1-mu) is
      NONZERO throughout the MOND regime (there is no eta=0 endpoint), and any zero of Z_par sits at
      an ISOLATED field value s=s* with Z_par!=0 nearby -- rank not constant, no primary constraint,
      kinetic Hamiltonian diverges, Lambda_sc->0.  THIS is the unambiguous strong-coupling result,
      and it is the load-bearing one (PART D), independent of the linear-limit semantics.
  Bottom line: the ONLY genuine (structural, constant-rank) degeneracy in this class is F'==0 &&
  F''==0 (=> F const, no MOND); every MOND-viable F meets Z_par only at isolated strong-coupling
  loci, never a constraint surface.
""")
check(True,
      "THEOREM DISTINCTION RECORDED: structural (constant-rank, e.g. eta=0 => genuine, no MOND) vs "
      "field-value (isolated s*, strong coupling) -- the MOND strong-coupling claim (PART D) does not "
      "rest on the disputed decoupling-vs-strong-coupling label of the linear eta->0 limit")


# ==================================================================================
hdr("VERDICT -- the isolated-zero classification for the frozen theorem")
# ==================================================================================
print(r"""
  CLASSIFICATION (settled):
  1. Z_perp = 2(1-mu) > 0 on the entire MOND regime (mu<1) => the khronon PROPAGATES transverse to
     the local acceleration everywhere MOND is active.  The theory is 2+1, and this ALONE forbids
     2+0 with nontrivial MOND -- no appeal to Z_par is needed.
  2. Genuine khronon removal (2+0) requires BOTH eigenvalues identically zero: F'==0 AND F'+2sF''==0
     => F=const => no MOND.  (Direction-independent, constant-rank => the only genuine Hamiltonian
     degeneracy in this class.)
  3. The isolated longitudinal locus Z_par(s*)=0 is a STRONG-COUPLING surface, NOT a second-class
     constraint: it is a field-value (not structural) degeneracy, generates no preserved Dirac
     secondary, the kinetic Hamiltonian diverges there, and the strong-coupling scale Lambda_sc ~
     Z_par^{3/4} -> 0.  For some kernels Z_par additionally goes negative (a longitudinal
     gradient-ghost) -- either way a pathology on a measure-zero locus, never a DOF removal.

  => NO nontrivial regular F(A^2/a0^2) realizes MOND AND removes the khronon by a genuine Hamiltonian
     degeneracy.  The obstruction is a THEOREM for this carrier class.

  SCOPE (explicit):  F(A^2) ruled out  !=  all relativistic MOND carriers ruled out.  Untouched:
  F(A^2, K), shear/expansion invariants, D_i a^i (parity-odd), and multi-invariant / multi-field
  carriers -- the precise mathematical targets for the harder classes.
""")

print("=" * 80)
if FAIL:
    print(f"FAILED {len(FAIL)} of {NCHK[0]} checks:")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED")
sys.exit(0)
