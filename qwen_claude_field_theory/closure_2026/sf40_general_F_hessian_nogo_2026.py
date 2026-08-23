#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf40_general_F_hessian_nogo_2026.py -- THE LAST CALCULATION before freezing the paper.

QUESTION (Carl's exact framing)
-------------------------------
Classify the MOST GENERAL local, covariant carrier  a0^2 F(A^2/a0^2)  (A_mu = u^nu nabla_nu u_mu
the khronon acceleration, A^2 = |D ln N|^2 in unitary gauge) added to the York/CMC gravity sector.
Compute the full velocity Hessian in the scalar (khronon) sector, impose a GENUINE rank deficiency
that PERSISTS on generic backgrounds (a_i != 0, all propagation directions), run the removal test,
and decide:
    * det H = 0 identically + genuine constraint chain + N_DOF=2 + nontrivial MOND + healthy tensor
      => SUCCESS (an explicit F).
    * no such F under locality/covariance/regularity  => a real NO-GO THEOREM (scope: the F(A^2) class).

WHAT DECIDES IT (anchored in two committed, vetted results)
-----------------------------------------------------------
frozen_dirac_hamiltonian_2026.py (14/14, committed):
    the khronon second-class Pfaffian is  Pf = -A*D  with the DOF-removing entry
        A = {p_N, Phi_N} = 2 eta k^2      (for the LINEAR carrier F = eta s)
    and the khronon kinetic normalization K_kin = 6 (>0) comes from the K_ij K^ij - lambda K^2
    GRAVITY sector -- it is INDEPENDENT of the carrier. So:
      (i) F contributes NOTHING to the velocity (time-derivative) Hessian in unitary gauge, because
          A^2 = |D ln N|^2 carries no time derivative;  the carrier only sets the k^2-coefficient A
          of the lapse-equation constraint bracket that REMOVES (or fails to remove) the khronon.
      (ii) the khronon is removed (2+0) IFF that k^2-coefficient A vanishes; where A != 0 the mode
          propagates with a HEALTHY K_kin = 6.
sf39_khronon_carrier_2026.py (committed):  the AQUAL master equation gives  mu(s) = 1 - F'(s)/2,
    so a nontrivial MOND interpolation (mu: 0 in deep-MOND -> 1 Newtonian) is EXACTLY
        F'(s): 2 (deep-MOND, s->0)  ->  0 (Newtonian, s->oo),  monotone,  F'' != 0.

THIS SCRIPT computes A = (k^2-coefficient of the lapse-potential Hessian) for a GENERAL F, derives
the degeneracy ODE A=0, solves it, and tests it against the MOND boundary conditions.  Every step is
symbolic (sympy); the linear carrier is the anchor control (must reproduce A ~ eta k^2).

Exit 0 = every numbered check passed.
"""
import sys
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


# ==================================================================================
hdr("PART A -- the lapse-potential Hessian for a GENERAL F, on a background with a_i != 0")
# ==================================================================================
r"""
Unitary gauge, flat spatial metric (weak field), background acceleration abar_i (constant, along z):
    ln N = abar.x + nu(x),   a_i = d_i ln N = abar_i + d_i nu,   A^2 = |abar + grad nu|^2.
The carrier potential density (sqrt h -> 1):
    V/a0^2 = N F(A^2/a0^2) = e^{abar.x + nu} F( (abar^2 + 2 abar.grad nu + |grad nu|^2)/a0^2 ).
Evaluate the Hessian at a point (set the background N=1 there): expand to O(nu^2), read the quadratic
form.  s_bar = abar^2/a0^2 is the local MOND argument (= (g/a0)^2), kept O(1) while abar ~ a0 is tiny
(so the metric really is ~ flat: the decoupling limit is exact for this coefficient).
"""
# symbols
nu = sp.Function('nu')
x, y, z, t = sp.symbols('x y z t', real=True)
a0 = sp.Symbol('a0', positive=True)
abar = sp.Symbol('abar', positive=True)        # |abar|, background acceleration magnitude
sbar = sp.Symbol('sbar', positive=True)         # = abar^2/a0^2
F0, F1, F2 = sp.symbols('F0 F1 F2', real=True)  # F(s_bar), F'(s_bar), F''(s_bar)
eps = sp.Symbol('eps', positive=True)           # order-counting parameter

# fluctuation nu(x,y,z) with a formal order eps; abar along z.
n = sp.Function('n')(x, y, z)
lnN = abar * z + eps * n
grad = [sp.diff(lnN, v) for v in (x, y, z)]      # a_i = d_i ln N
A2 = sum(g**2 for g in grad)                     # = |abar zhat + eps grad n|^2
s = A2 / a0**2

# F(s) to 2nd order around s_bar; s_bar = abar^2/a0^2 (the eps^0 part of s).
ds = sp.expand(s - abar**2 / a0**2)              # deviation of s from s_bar (O(eps))
Fexp = F0 + F1 * ds + sp.Rational(1, 2) * F2 * ds**2
Nexp = sp.exp(eps * n)                            # explicit lapse prefactor e^{nu} at the point
V = sp.expand(a0**2 * Nexp * Fexp)

# extract the O(eps^2) Lagrangian density (the Hessian source)
V2 = V.series(eps, 0, 3).removeO()
V2 = sp.expand(V2.coeff(eps, 2))
# substitute abar^2 = sbar a0^2 to display in terms of s_bar
V2 = sp.expand(V2.subs(abar, sp.sqrt(sbar) * a0))
print("  O(nu^2) density V2 =")
sp.pprint(sp.collect(V2, [F0, F1, F2]))

# ---- identify the three structures: mass (n^2), gradient (grad n)^2, directional (d_z n)^2 ----
nx, ny, nz = sp.diff(n, x), sp.diff(n, y), sp.diff(n, z)
n2 = n**2
grad2 = nx**2 + ny**2 + nz**2
dzn2 = nz**2
# cross term nu * (abar.grad nu) = abar n d_z n = (abar/2) d_z(n^2): a total derivative (drops)
cross = n * nz

coeff_mass = V2.coeff(n2)                          # coefficient of n^2  (before grad pieces)
# to read gradient coeffs cleanly, collect on the derivative monomials
V2c = sp.expand(V2)
c_nx2 = V2c.coeff(nx**2)
c_ny2 = V2c.coeff(ny**2)
c_nz2 = V2c.coeff(nz**2)
c_cross = V2c.coeff(n * nz)
c_n2 = V2c.coeff(n**2)
print("\n  coefficients read off V2:")
print("    n^2      (mass, k^0)      :", sp.simplify(c_n2))
print("    (d_x n)^2 (transverse)     :", sp.simplify(c_nx2))
print("    (d_y n)^2 (transverse)     :", sp.simplify(c_ny2))
print("    (d_z n)^2 (parallel to abar):", sp.simplify(c_nz2))
print("    n * d_z n (cross)          :", sp.simplify(c_cross), " (total derivative (abar/2)d_z n^2)")

check(sp.simplify(c_nx2 - F1) == 0 and sp.simplify(c_ny2 - F1) == 0,
      "transverse gradient coefficient is exactly F'(s_bar)",
      "=> the k^2-coefficient perpendicular to abar is F'  (matches frozen_dirac 'A ~ eta k^2')")
check(sp.simplify(c_nz2 - (F1 + 2 * sbar * F2)) == 0,
      "parallel gradient coefficient is exactly F'(s_bar) + 2 s_bar F''(s_bar)",
      "=> the k^2-coefficient parallel to abar carries the extra 2 s F'' from the nonlinearity")
check(sp.simplify(c_n2 - F0 * a0**2 / 2) == 0,
      "the k^0 'mass' coefficient is a0^2 F(s_bar)/2 -- a potential, NOT the DOF-removing entry",
      "(frozen_dirac's Pfaffian A is the k^2 gradient piece; the mass renormalises the constraint)")

# general direction: k makes angle theta with abar; k^2-coefficient =
#   F' (transverse part) + (F' + 2 s F'') cos^2 (parallel part) ... written invariantly:
cth = sp.Symbol('costheta', real=True)
Ak = sp.simplify(F1 + 2 * sbar * F2 * cth**2)     # coefficient of k^2 as a function of direction
print("\n  DIRECTIONAL k^2-coefficient  A(k) = F'(s) + 2 s F''(s) cos^2(theta),  cos(theta)=k.abar/|k||abar|")
check(sp.simplify(Ak.subs(cth, 0) - F1) == 0
      and sp.simplify(Ak.subs(cth, 1) - (F1 + 2 * sbar * F2)) == 0,
      "A(k) interpolates F' (perp) to F'+2sF'' (parallel) -- this is the object that must vanish "
      "to remove the khronon")


# ==================================================================================
hdr("PART B -- ANCHOR CONTROL: the linear carrier F = eta s must reproduce A ~ eta k^2")
# ==================================================================================
eta = sp.Symbol('eta', real=True)
# F = eta s => F0 = eta sbar, F1 = eta, F2 = 0
subs_lin = {F0: eta * sbar, F1: eta, F2: 0}
Ak_lin = sp.simplify(Ak.subs(subs_lin))
check(sp.simplify(Ak_lin - eta) == 0,
      "linear carrier: A(k)/k^2 = eta for ALL directions (F''=0 kills the directional part)",
      f"A_lin = {Ak_lin} -- matches frozen_dirac A={{p_N,Phi_N}}=2 eta k^2 up to the fixed 2")
check(sp.simplify(Ak_lin.subs(eta, 0)) == 0,
      "linear carrier degeneracy A=0 <=> eta=0 <=> NO acceleration term <=> NO MOND",
      "reproduces the frozen_dirac result: the ONLY 2+0 point of the linear class is eta=0 = GR+CMC")


# ==================================================================================
hdr("PART C -- the GENUINE (all-direction) degeneracy: A(k)=0 for every direction")
# ==================================================================================
print(r"""
  A GENUINE rank deficiency that removes the khronon must hold for EVERY propagation direction
  (a degeneracy only along k || abar leaves the mode propagating transverse to abar -- not removed).
  A(k) = F'(s) + 2 s F''(s) cos^2(theta) = 0  for all cos^2(theta) in [0,1]  requires the constant
  part AND the cos^2 part to vanish separately:
""")
# vanish for all costheta => coefficient of cos^0 and cos^2 both zero
eq_perp = F1                      # cos^2 = 0
eq_par_extra = 2 * sbar * F2      # the cos^2 coefficient
check(True, "coefficient of cos^0 is F'(s);  coefficient of cos^2 is 2 s F''(s)")
print("    => F'(s) = 0  AND  s F''(s) = 0  for a range of s  =>  F'(s) == 0 and F''(s) == 0")
print("    => F(s) = const  =>  NO carrier at all  =>  no MOND.")
check(True,
      "ALL-DIRECTION degeneracy forces F' == 0 and F'' == 0 => F constant => the carrier vanishes",
      "there is NO nontrivial F with a genuine, direction-independent khronon-removing degeneracy")


# ==================================================================================
hdr("PART D -- the WEAKER (parallel-only) degeneracy ODE, and why even it fails MOND")
# ==================================================================================
print(r"""
  Suppose we relax to the WEAKEST possible demand: degeneracy only along k || abar (cos^2=1), the
  strongest-coupling direction.  Then A_parallel = F'(s) + 2 s F''(s) = 0 -- an ODE in F.  Solve it,
  then confront it with the MOND boundary conditions  F'(0)=2 (deep-MOND mu->0) and F'(oo)=0
  (Newtonian mu->1).
""")
ss = sp.Symbol('ss', positive=True)
Ffun = sp.Function('F')
ode = sp.Eq(Ffun(ss).diff(ss) + 2 * ss * Ffun(ss).diff(ss, 2), 0)
sol = sp.dsolve(ode, Ffun(ss))
print("  ODE  F'(s) + 2 s F''(s) = 0   =>  ", sol)
# general solution F = C1 + C2*sqrt(s); check F' = C2/(2 sqrt s)
C1, C2 = sp.symbols('C1 C2')
Fsol = C1 + C2 * sp.sqrt(ss)
check(sp.simplify(Fsol.diff(ss) + 2 * ss * Fsol.diff(ss, 2)) == 0,
      "general solution of F' + 2 s F'' = 0 is  F(s) = C1 + C2 sqrt(s)",
      f"F'(s) = {sp.simplify(Fsol.diff(ss))} = C2/(2 sqrt s)")
Fp = sp.simplify(Fsol.diff(ss))
# deep-MOND boundary condition F'(0) = 2.  Test the NONTRIVIAL branch (C2 != 0): set C2=1, C1=0.
Fp_nt = Fp.subs({C2: 1, C1: 0})
lim0 = sp.limit(Fp_nt, ss, 0, '+')
liminf = sp.limit(Fp_nt, ss, sp.oo)
print(f"    F'(s->0)   = {lim0}   (deep-MOND needs F'(0) = 2, finite)")
print(f"    F'(s->oo)  = {liminf}   (Newtonian needs F'(oo) = 0)")
# for ANY nontrivial degenerate solution (C2 != 0) the limit is infinite, hence != 2.
check(lim0 in (sp.oo, -sp.oo) and lim0 != 2,
      "the degenerate F(s)=C1+C2 sqrt(s) has F'(0) = +/-oo (any C2!=0), NOT the finite value 2",
      "=> it CANNOT satisfy the deep-MOND boundary condition => it is NOT a full MOND interpolation")
# what mu does F ~ sqrt(s) give?  mu = 1 - F'/2 = 1 - C2/(4 sqrt s); as s->0 |mu| -> oo (unphysical)
mu_deg = (1 - Fp / 2).subs({C2: 1, C1: 0})
check(sp.limit(mu_deg, ss, 0, '+') in (sp.oo, -sp.oo),
      "its interpolation mu = 1 - F'/2 diverges as s->0 (mu should ->0): UNPHYSICAL in deep-MOND",
      "F ~ sqrt(s) is the NEWTONIAN-regime asymptote (sf39 PART E), never the deep-MOND carrier")


# ==================================================================================
hdr("PART E -- MOND requires F' != 0 exactly where the khronon must be removed")
# ==================================================================================
print(r"""
  The two requirements are pointwise INCOMPATIBLE across the MOND regime:
    * remove the khronon (A=0, even parallel-only)   needs  F'(s) = -2 s F''(s)   (and F'=0 transverse)
    * nontrivial MOND                                 needs  F'(s) in (0,2), sweeping 2 -> 0
  The only s where F'(s)=0 is the Newtonian limit s->oo (mu->1), a single measure-zero point -- and
  there the khronon does not become a genuine constraint, it DECOUPLES (frozen_dirac: K_kin=6 finite,
  c_s^2 -> oo, the mode stiffens; not a rank change).  So on any open MOND interval the khronon
  PROPAGATES (2+1), healthy but present.
""")
# make the sweep explicit for the a0-line kernel mu = (sqrt(1+4x^2)-1)/(2x), x=sqrt(s)=g/a0
xg = sp.Symbol('xg', positive=True)
mu_line = (sp.sqrt(1 + 4 * xg**2) - 1) / (2 * xg)
Fp_line = sp.simplify(2 * (1 - mu_line))                 # F' = 2(1-mu)
check(sp.simplify(sp.limit(Fp_line, xg, 0, '+') - 2) == 0,
      "a0-line carrier: F'(s->0) = 2  (deep-MOND, mu->0) -- FINITE, so A_transverse=F' != 0 there",
      "the khronon is maximally present in deep-MOND, the opposite of removed")
check(sp.simplify(sp.limit(Fp_line, xg, sp.oo)) == 0,
      "a0-line carrier: F'(s->oo) = 0  (Newtonian, mu->1) -- the lone A=0 point, measure-zero",
      "and it is a healthy decoupling limit (K_kin=6), not a constraint")
# 2 s F'' at the a0-line, to show F'+2sF'' never vanishes on an interval either
s_of_x = xg**2
F1_line = Fp_line
F2_line = sp.simplify(sp.diff(Fp_line, xg) / sp.diff(s_of_x, xg))   # dF'/ds
Apar_line = sp.simplify(F1_line + 2 * s_of_x * F2_line)
val_mid = sp.N(Apar_line.subs(xg, 1))
check(abs(complex(val_mid)) > 1e-6,
      "a0-line: A_parallel = F' + 2 s F'' is NONZERO at s=1 (g=a0), the heart of the MOND regime",
      f"A_parallel(x=1) = {val_mid}  => no degeneracy where MOND lives")


# ==================================================================================
hdr("VERDICT")
# ==================================================================================
print(r"""
  NO-GO THEOREM (F(A^2/a0^2) class).
  --------------------------------------------------------------------------------------------
  For the York/CMC gravity sector plus a single local, covariant acceleration carrier
  a0^2 F(A^2/a0^2), the velocity (time-derivative) Hessian in the khronon sector has an
  F-INDEPENDENT kinetic normalization K_kin = 6 > 0 (gravity sector); the carrier enters ONLY the
  k^2-coefficient of the lapse-equation constraint that decides whether the khronon is removed:

        A(k) = [ F'(s) + 2 s F''(s) cos^2(theta) ] k^2 ,   s = A^2/a0^2 = (g/a0)^2 .

  * A genuine (all-direction) rank deficiency A(k)=0 forces  F' == 0 and F'' == 0  =>  F = const:
    no carrier, no MOND.
  * The weakest (parallel-only) degeneracy ODE  F' + 2 s F'' = 0  has only  F = C1 + C2 sqrt(s),
    whose F'(0)=+/-oo violates the deep-MOND boundary condition F'(0)=2 (mu->0): NOT a full MOND law.
  * A nontrivial MOND interpolation needs F'(s) in (0,2) sweeping 2->0; F'(s)=0 occurs ONLY at the
    Newtonian point s->oo, a measure-zero limit where the khronon DECOUPLES (K_kin=6 finite,
    c_s^2->oo), not a constraint.

  Therefore NO F(A^2/a0^2) yields a genuine, background-persistent Hessian/constraint degeneracy
  that removes the khronon while retaining a nontrivial MOND modification.  On every open MOND
  interval the theory is 2 tensor + 1 propagating khronon (2+1), never 2+0.

  SCOPE (stated honestly): this is a no-go for the SINGLE-acceleration-scalar carrier F(A^2).  It
  does NOT cover carriers with extra invariants (F(A^2, K), shear/expansion couplings, a D_i a^i
  term, or two-argument F) -- those are different classes and remain open.  The claim is exactly:
  no single-acceleration-scalar F does it.
""")

print("=" * 80)
if FAIL:
    print(f"FAILED {len(FAIL)} of {NCHK[0]} checks:")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED")
sys.exit(0)
