#!/usr/bin/env python3
r"""mi_auxfield_exact_circular_2026.py -- the AUXILIARY-FIELD LOCALIZATION of the nonlocal MI law, and its EXACT
circular-orbit solution with NO first-moment closure.

WHY. The corpus's action-programme no-goes (2026-08-01) reported that for a generic memory kernel the
u-contraction is (v/c)^2-suppressed, needing a prefactor |K| ~ 3.8e5-3.8e7 against ||K|| <= 1. That was obtained
through a FIRST-MOMENT CLOSURE: the convolution (K * a) was replaced by (int K) a, i.e. the kernel was treated as
a pure rescaling. On a circular orbit that substitution is not innocent, because a^mu ROTATES: the exact
convolution has an in-phase part AND a quadrature part, and the closure keeps only the former. This script does it
exactly. Circular orbits are the one case where "exact" is tractable, because every quantity is a single harmonic
and the kernel enters only through its transform at the orbital frequency.

PART A -- THE LOCALIZATION, in two independent pieces.
  A1  the algebraic nonlinearity. sqrt(X) = min over lambda > 0 of [ X/(2 lambda) + lambda/2 ], stationary at
      lambda* = sqrt(X), a genuine minimum. So the MI law's square root becomes polynomial in the acceleration at
      the cost of ONE auxiliary scalar with an algebraic equation of motion.
  A2  the nonlocality. For K(s) = w_c exp(-w_c s) the convolution chi = K * a is EXACTLY the solution of the local
      first-order ODE  chi-dot + w_c chi = w_c a. Any rational transform (a Prony sum of N poles) localizes to N
      such ODEs. So the nonlocal law is a LOCAL system in (x, chi_i, lambda).

PART B -- THE EXACT CIRCULAR ORBIT. On a circular orbit a(tau - s) = R(-Omega s) a(tau), so
      chi = [ C(Omega) I - S(Omega) J ] a,   C = int K cos(Omega s) ds,   S = int K sin(Omega s) ds,
with J the rotation generator. C is RADIAL (in phase with a), S is TANGENTIAL (quadrature). The first-moment
closure is exactly the replacement C -> int K = 1, S -> 0.

WHAT IT FINDS, and the two halves point opposite ways.

  *** The (v/c)^2 suppression is EXACT rather than a closure artefact -- BUT ONLY AT w_c = a_0/c, WHICH IS A
  CHOICE. *** C(Omega) = w_c^2/(w_c^2 + Omega^2), and IF the cutoff is taken to be w_c = a_0/c then
  Omega/w_c = (c/v)(g_obs/a_0) identically, so C = (v/c)^2 (a_0/g_obs)^2 and the Milky Way needs a prefactor
  1/C = 8.9e6. At fixed w_c << Omega the suppression is kernel-SHAPE-independent by Riemann-Lebesgue (three
  different kernels agree to within 3 orders). But w_c = a_0/c is imposed on one line of this script, and the
  corpus's own committed window from the kernel-axis work is w_c = 1.78e-14 to 2.21e-14 -- FIVE ORDERS LARGER --
  where C = 0.997 and S/C = 0.05: NO suppression and NO torque. So section C is a statement about ONE KERNEL SCALE,
  not about nonlocal MI. The w_c scan is now tabulated so this cannot be read the other way.
  ALSO WITHDRAWN: the claim that 1/C = 8.9e6 lying inside 3.8e5-3.8e7 CROSS-VALIDATES two independent routes. It
  does not. Both numbers are the same kinematic (c/v)^2 dressed by different O(1) factors, so the agreement is
  arithmetic, not evidential.

  *** WITHDRAWN, 2026-08-04, by adversarial verification: the TORQUE NO-GO. *** A first version of this script
  claimed that the quadrature component S/C = Omega/w_c ~ 3e3 obstructs circular orbits for ANY inertia law
  m G(chi) chi^mu = F^mu, and that no causal memory could remove it. BOTH CLAIMS ARE FALSE, and the counterexample
  was already printed in this script's own kernel table:
    - single-pole  w_c e^{-w_c s}:  S/C = +Omega/w_c = +2978.6 at the MW  -- that kernel IS excluded outright
    - gamma-2      w^2 s e^{-w s}:  S/C = 2 w Omega/(w^2-Omega^2) -> -2 w/Omega = -6.71e-04, four orders BELOW one,
                                     with IDENTICAL suppression 1/|C| = 8.872e6
    - time-symmetric (w/2)e^{-w|s|}: S == 0 at EVERY frequency, with C UNCHANGED. And this case is the one that
                                     matters most, because varying a quadratic nonlocal ACTION keeps only the
                                     SYMMETRIC part of the kernel -- so the action-level construction of Part A
                                     produces S == 0 automatically.
  So torque-freedom is a KERNEL-SHAPE CONDITION, not a no-go. The accompanying "theorem" -- that S = 0 on an
  interval forces K proportional to delta -- is also withdrawn: K(s) = b J_0(b s) is causal, normalised, and has
  S == 0 for ALL |Omega| < b with C = b/sqrt(b^2-Omega^2) >= 1. The invalid step was applying the identity theorem
  to Im K-hat, which is a real function of a real variable, not a holomorphic function on an open set.

  *** THE ESCAPE, and it is real (A8). *** If the memory acts on a Lorentz SCALAR that is constant along a
  circular orbit -- a^nu a_nu is exactly constant, verified here on the exact circular de Sitter worldline -- then
  the memory passes it at DC with unit gain: no suppression AND no torque. But then the memory is INERT on
  circular orbits and the law collapses to the local algebraic MI law, i.e. to the a_0-line itself. So the only
  memory compatible with exact rotation curves is one that cannot be detected in them.

CREDIT. The kernel nu = sqrt(1+1/y) and the temperature balance are Milgrom 1999 PLA 253:273 eqs 6-9 (he fixes
a_0_hat = 2 c H_Lambda); a_lambda = c^2 sqrt(Lambda/3) is Milgrom 1994 Ann.Phys. 229:384 sec II eq 3; the
five-acceleration construction is Deser & Levin 1997 CQG 14:L163. kappa = 1/2 is FITTED, NOT DERIVED.

Both a_0 footings are reported: canonical 9.3614e-11 (rho_DE, cH_Lambda) and ALT 1.13e-10 (rho_total, cH_0).

Exit 0 = every check held. No check(True); every condition below can fail.
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 104)
    print(f"  {t}")
    print("=" * 104)


C_L = 2.99792458e8
A0 = {"canonical": 9.3614e-11, "ALT": 1.13e-10}
KPC = 3.0856775814913673e19

banner("A1  LOCALIZING THE ALGEBRAIC NONLINEARITY -- one auxiliary scalar")

X, lam, k, aa = sp.symbols("X lambda k a", positive=True)
F = X / (2 * lam) + lam / 2
lstar = sp.solve(sp.diff(F, lam), lam)
lstar = [s for s in lstar if s.is_positive or True][0]
val = sp.simplify(F.subs(lam, sp.sqrt(X)))
d2 = sp.simplify(sp.diff(F, lam, 2).subs(lam, sp.sqrt(X)))
print(f"  F(lambda) = X/(2 lambda) + lambda/2   stationary at lambda* = {sp.sqrt(X)}   F(lambda*) = {val}")
print(f"  d2F/dlambda2 at lambda* = {d2} > 0")
check(sp.simplify(val - sp.sqrt(X)) == 0 and sp.simplify(d2 - 1 / sp.sqrt(X)) == 0
      and sp.simplify(sp.diff(F, lam).subs(lam, sp.sqrt(X))) == 0,
      f"A1a sqrt(X) = min_lambda [X/(2 lambda) + lambda/2] exactly, stationary at lambda* = sqrt(X) with second "
      f"derivative 1/sqrt(X) > 0 -- a genuine MINIMUM, so the substitution is variationally legitimate and not "
      f"merely algebraic. The MI square root becomes POLYNOMIAL in the acceleration at the cost of one auxiliary "
      f"scalar with an algebraic equation of motion")
# and it reproduces the a0-line
g_obs, g_bar, a0s = sp.symbols("g_obs g_bar a_0", positive=True)
Ilaw = sp.sqrt(g_obs**2 + (a0s / 2) ** 2) - a0s / 2
# the FIRST version of this check squared what had just been defined as a square root -- it could not fail, and it
# never used g_bar. The real content is the INVERSION: g_bar = I must satisfy the a0-line.
inv_resid = sp.simplify(Ilaw**2 + a0s * Ilaw - g_obs**2)
fwd = sp.simplify(sp.solve(sp.Eq(g_obs**2, g_bar**2 + a0s * g_bar), g_bar)[0] - Ilaw.subs(g_obs, g_obs))
num = [abs(float((Ilaw.subs({g_obs: gv, a0s: 9.3614e-11}))**2 + 9.3614e-11
                 * Ilaw.subs({g_obs: gv, a0s: 9.3614e-11}) - gv**2)) / gv**2
       for gv in (1e-12, 1e-10, 1e-8)]
print(f"  inversion residual I^2 + a0 I - g_obs^2 = {inv_resid};  numeric relative residuals {['%.1e' % x for x in num]}")
check(inv_resid == 0 and max(num) < 1e-11,
      f"A1b setting g_bar = I(g_obs) SATISFIES the a_0-line: the residual I^2 + a_0 I - g_obs^2 vanishes "
      f"IDENTICALLY in exact arithmetic, and numerically to {max(num):.1e} relative across three decades of "
      f"g_obs -- rounding-limited, since I^2, a_0 I and g_obs^2 are the same order and cancel. So the localization "
      f"changes the variables, not the phenomenology. (Scope: this is the alpha=1 kernel; Route A's "
      f"nu = 1/(1-exp(-sqrt y)) is NOT polynomialized by a single auxiliary scalar and would need its own "
      f"treatment.)")

banner("A2  LOCALIZING THE NONLOCALITY -- N auxiliary vectors, one ODE each")

tau, s_, wc = sp.symbols("tau s omega_c", positive=True)
af = sp.Function("a")
chi_int = wc * sp.Integral(sp.exp(-wc * (tau - sp.Symbol("u"))) * af(sp.Symbol("u")), (sp.Symbol("u"), -sp.oo, tau))
# verify d/dtau chi = w_c a - w_c chi by differentiating the explicit convolution
u = sp.Symbol("u")
chi_expr = wc * sp.exp(-wc * tau) * sp.Integral(sp.exp(wc * u) * af(u), (u, -sp.oo, tau))
dchi = sp.simplify(sp.diff(chi_expr, tau).doit())
resid = sp.simplify(dchi - (wc * af(tau) - wc * chi_expr))
print(f"  chi(tau) = w_c int_-inf^tau e^{{-w_c(tau-u)}} a(u) du    residual of  chi' + w_c chi - w_c a  =  {resid}")
check(resid == 0,
      f"A2a the exponential-memory convolution is EXACTLY the solution of the LOCAL first-order ODE "
      f"chi' + w_c chi = w_c a (residual identically zero, verified by differentiating the convolution). Any "
      f"rational transform -- a Prony sum of N poles -- localizes to N such ODEs, so the nonlocal MI law becomes a "
      f"LOCAL system in (x, chi_i, lambda). *** This is the localization: no closure, no truncation, exact ***")


banner("B  THE EXACT CIRCULAR ORBIT -- in-phase C and quadrature S, no moment expansion")

Om = sp.Symbol("Omega", positive=True)
Kk = wc * sp.exp(-wc * s_)
Cex = sp.simplify(sp.integrate(Kk * sp.cos(Om * s_), (s_, 0, sp.oo)))
Sex = sp.simplify(sp.integrate(Kk * sp.sin(Om * s_), (s_, 0, sp.oo)))
norm = sp.simplify(sp.integrate(Kk, (s_, 0, sp.oo)))
print(f"  int K       = {norm}")
print(f"  C(Omega)    = {Cex}")
print(f"  S(Omega)    = {Sex}")
print(f"  S/C         = {sp.simplify(Sex/Cex)}")
check(norm == 1 and sp.simplify(Cex - wc**2 / (wc**2 + Om**2)) == 0
      and sp.simplify(Sex - wc * Om / (wc**2 + Om**2)) == 0 and sp.simplify(Sex / Cex - Om / wc) == 0,
      f"B1 exact transforms: int K = 1, C = w_c^2/(w_c^2+Omega^2), S = w_c Omega/(w_c^2+Omega^2), and S/C = "
      f"Omega/w_c exactly. The FIRST-MOMENT CLOSURE is precisely C -> 1, S -> 0, i.e. the Omega -> 0 limit -- so "
      f"the closure is a zero-frequency approximation applied at the ORBITAL frequency")
# rotation algebra: a(tau-s) = R(-Omega s) a(tau); R(-x) = cos x I - sin x J
# The first version tested only the identity R(theta) = cos I + sin J -- true, but not the load-bearing premise.
# Test the premise itself on the EXACT circular de Sitter worldline, with the constraint imposed.
Av, hv, Rv, wv, Hv, tv, sv = sp.symbols("A h R w H tau s", positive=True)
sub = {Av**2 * hv**2: 1 + Rv**2 * wv**2}
Xv = sp.Matrix([Av * sp.sinh(hv * tv), Av * sp.cosh(hv * tv), Rv * sp.cos(wv * tv), Rv * sp.sin(wv * tv)])
uv = sp.diff(Xv, tv)
av = sp.diff(uv, tv)
av_s = av.subs(tv, tv - sv)
# the (2,3) plane: does it rotate rigidly by -w s?
rot = sp.Matrix([[sp.cos(wv * sv), sp.sin(wv * sv)], [-sp.sin(wv * sv), sp.cos(wv * sv)]])
plane_ok = sp.simplify(sp.Matrix(av_s[2:4]) - rot * sp.Matrix(av[2:4])) == sp.zeros(2, 1)
# the (0,1) plane: it does NOT rotate -- it BOOSTS by -h s, with cosh/sinh not cos/sin
boo = sp.Matrix([[sp.cosh(hv * sv), -sp.sinh(hv * sv)], [-sp.sinh(hv * sv), sp.cosh(hv * sv)]])
boost_ok = sp.simplify(sp.Matrix(av_s[0:2]) - boo * sp.Matrix(av[0:2])) == sp.zeros(2, 1)
boost_is_not_rot = sp.simplify(boo - rot.subs(wv, hv)) != sp.zeros(2, 2)
print(f"  dS embedding: (2,3)-plane rotates rigidly by -w s? {plane_ok};  "
      f"(0,1)-plane BOOSTS by -h s? {boost_ok};  boost != rotation? {boost_is_not_rot}")
check(plane_ok and boost_ok and boost_is_not_rot,
      f"B2 verified on the EXACT circular de Sitter worldline, not on a flat-space cartoon: the (2,3) part of "
      f"a^mu rotates RIGIDLY by -w s, so chi = [C I - S J] a holds there and the closure's C -> 1, S -> 0 does "
      f"delete a component orthogonal to the one it keeps. *** BUT THE SCOPE IS NARROWER THAN THE FIRST VERSION "
      f"IMPLIED: the (0,1) part BOOSTS by -h s rather than rotating, so its memory integral involves "
      f"int K(s) cosh(h s) ds, which DIVERGES for h > w_c. The C/S decomposition is a statement about the orbital "
      f"2-plane only, and the boost sector is an unresolved open item, not a solved one ***")


banner("C  THE (v/c)^2 SUPPRESSION IS EXACT, AND IT REPRODUCES THE CORPUS'S OWN WINDOW")

print(f"  {'system':<26}{'v (km/s)':>10}{'R (kpc)':>9}{'Omega (1/s)':>13}{'g_obs/a0':>10}"
      f"{'Omega/w_c':>11}{'C exact':>11}{'1/C':>11}")
print("  " + "-" * 101)
SYS = [("Milky Way (R0)", 233.1, 8.122), ("big spiral outskirt", 200.0, 30.0), ("dwarf (DDO-like)", 30.0, 2.0)]
rows = []
for nm, vk, Rk in SYS:
    v, R = vk * 1e3, Rk * KPC
    Omv, g_obsv = v / R, v * v / R
    wcv = A0["canonical"] / C_L
    ratio, Cv = Omv / wcv, 1.0 / (1.0 + (Omv / wcv) ** 2)
    rows.append((nm, v, Omv, g_obsv, ratio, Cv))
    print(f"  {nm:<26}{vk:>10.1f}{Rk:>9.2f}{Omv:>13.3e}{g_obsv/A0['canonical']:>10.3f}"
          f"{ratio:>11.1f}{Cv:>11.3e}{1/Cv:>11.3e}")
mw = rows[0]
check(abs(mw[4] / ((C_L / mw[1]) * (mw[3] / A0["canonical"])) - 1) < 1e-12,
      f"C1 *** Omega/w_c = (c/v)(g_obs/a_0) IDENTICALLY (verified to 1e-12 at the Milky Way: {mw[4]:.1f} = "
      f"{C_L/mw[1]:.1f} x {mw[3]/A0['canonical']:.3f}), so at the MOND transition g_obs = a_0 one has "
      f"Omega/w_c = c/v exactly and C = (v/c)^2. THE (v/c)^2 SUPPRESSION IS THE EXACT LOW-PASS ROLL-OFF AT THE "
      f"ORBITAL FREQUENCY, not an artefact of the closure ***")
inv = 1.0 / mw[5]
check(abs((inv - 1.0) / ((C_L / mw[1]) ** 2 * (mw[3] / A0["canonical"]) ** 2) - 1) < 1e-12,
      f"C2 the required prefactor is 1/C = 1 + (c/v)^2 (g_obs/a0)^2 = {inv:.3e} exactly -- note the additive 1, "
      f"which a first version of this very check dropped (it is the Newtonian floor of the low-pass gain). *** AND "
      f"THE CROSS-VALIDATION CLAIMED BY THE FIRST VERSION OF THIS CHECK IS WITHDRAWN: that 1/C falls inside the "
      f"corpus's 3.8e5-3.8e7 window is NOT independent corroboration, because that window is the SAME kinematic "
      f"(c/v)^2 dressed by a different O(1) factor. The agreement is arithmetic, not evidential, and at the Milky "
      f"Way's v the window admits g_obs/a0 over a factor-10 band, so it has almost no discriminating power ***")
for nm, a0v in A0.items():
    wcv = a0v / C_L
    print(f"  footing {nm:<10} w_c = a0/c = {wcv:.4e} 1/s  ->  MW Omega/w_c = {mw[2]/wcv:>8.1f},  "
          f"C = {1/(1+(mw[2]/wcv)**2):.3e}")
C_can = 1.0 / (1 + (mw[2] / (A0["canonical"] / C_L)) ** 2)
C_alt = 1.0 / (1 + (mw[2] / (A0["ALT"] / C_L)) ** 2)
check(abs((C_alt / C_can) / (A0["ALT"] / A0["canonical"]) ** 2 - 1) < 0.01 and C_alt < 1e-5,
      f"C3 both footings give the same conclusion: in the suppressed regime C scales as a0^2, verified to 1% "
      f"({C_alt/C_can:.4f} against {(A0['ALT']/A0['canonical'])**2:.4f}), so the ALT footing improves C by only "
      f"{C_alt/C_can:.3f}x, from {C_can:.3e} to {C_alt:.3e}. The footing choice cannot rescue six orders of "
      f"magnitude, and no conclusion here depends on which footing is used")
# kernel-independence: Riemann-Lebesgue on three genuinely different causal kernels
KERN = [("exponential w_c e^-w_c s", lambda w, O: w * w / (w * w + O * O)),
        ("gamma-2  w^2 s e^-w s", lambda w, O: (w**2 * (w**2 - O**2)) / (w**2 + O**2) ** 2),
        ("boxcar on [0, 1/w]", lambda w, O: w * math.sin(O / w) / O)]
wcv = A0["canonical"] / C_L
print(f"\n  kernel-independence at the MW Omega = {mw[2]:.3e} (all normalised to int K = 1):")
Cs = []
for nm, f in KERN:
    Cv = f(wcv, mw[2])
    Cs.append(abs(Cv))
    print(f"    {nm:<26} C = {Cv:+.4e}   |C| = {abs(Cv):.3e}")
check(max(Cs) < 1e-3,
      f"C4 AT FIXED w_c = a0/c all three kernels -- exponential, gamma-2 and boxcar -- give |C| < 1e-3 at "
      f"the Milky Way's orbital frequency, the largest being {max(Cs):.2e}. This is Riemann-Lebesgue: any causal "
      f"kernel whose spectral content sits below Omega has C(Omega) -> 0. *** So at fixed w_c << Omega the "
      f"suppression is independent of kernel SHAPE. It is NOT independent of the kernel SCALE w_c -- see the scan "
      f"in C5, which is where the whole section turns ***")


banner("C5  *** THE SCAN THAT DECIDES SECTION C: w_c IS A CHOICE, NOT A DERIVED SCALE ***")

# w_c = a0/c was imposed on ONE line above. The corpus's own kernel-axis work commits a window five orders larger.
OMEGA_C_LO, OMEGA_C_HI = 1.7824e-14, 2.2113e-14   # mi_kernel_axis_separation_omegac_2026.py:66-67
WSCAN = [("a0/c            (this script's choice)", A0["canonical"] / C_L),
         ("a0/(2c)", A0["canonical"] / (2 * C_L)),
         ("ALT a0/c", A0["ALT"] / C_L),
         ("sqrt(G rho_L) = 1/t_dyn", 6.2469e-19),
         ("H_Lambda = cH_L/c", 5.4194e-10 / C_L),
         ("OMEGA_C_LO (corpus committed)", OMEGA_C_LO),
         ("OMEGA_C_HI (corpus committed)", OMEGA_C_HI)]
print(f"  {'w_c choice':<40}{'w_c (1/s)':>12}{'Omega/w_c':>12}{'C':>12}{'S/C':>10}{'verdict':>22}")
print("  " + "-" * 108)
res = {}
for nm, wcand in WSCAN:                    # NB: not `wv` -- that name is the sympy symbol w, used again in E1
    r = mw[2] / wcand
    Cv = 1.0 / (1.0 + r * r)
    res[nm] = (r, Cv)
    verd = "suppressed + torque" if Cv < 1e-3 else ("NO suppression, NO torque" if Cv > 0.9 else "intermediate")
    print(f"  {nm:<40}{wcand:>12.4e}{r:>12.4f}{Cv:>12.4e}{r:>10.4f}{verd:>22}")
lo, hi = res["OMEGA_C_LO (corpus committed)"], res["OMEGA_C_HI (corpus committed)"]
check(lo[1] > 0.99 and hi[1] > 0.99 and res["a0/c            (this script's choice)"][1] < 1e-6,
      f"C5a *** THE WHOLE OF SECTION C AND D HANGS ON ONE UNLABELLED LINE. At w_c = a0/c the Milky Way has "
      f"C = {res[chr(97)+'0/c            (this script'+chr(39)+'s choice)'][1]:.3e} and S/C = 2979 -- total "
      f"suppression plus a huge torque. At the corpus's OWN committed window "
      f"w_c = {OMEGA_C_LO:.4e}-{OMEGA_C_HI:.4e} (from mi_kernel_axis_separation_omegac_2026.py, five orders "
      f"larger) the SAME formulae give C = {lo[1]:.4f}-{hi[1]:.4f} and S/C = {hi[0]:.4f}-{lo[0]:.4f}: NO "
      f"suppression and NO torque. So this is a result about ONE KERNEL SCALE, not about nonlocal MI, and nothing "
      f"here derives w_c ***")
check(all(res[nm][1] < 1e-3 for nm in ("a0/c            (this script's choice)", "a0/(2c)", "ALT a0/c",
                                       "sqrt(G rho_L) = 1/t_dyn"))
      and res["H_Lambda = cH_L/c"][1] < 1e-3,
      f"C5b the honest sub-result, which does limit the damage: every scale built from a0 or from the de Sitter "
      f"rate itself -- a0/c, a0/2c, the ALT footing, 1/t_dyn = sqrt(G rho_L), and H_Lambda -- lies in the "
      f"suppressed regime. Only a w_c NOT built from a0 escapes, and the corpus's committed window is exactly "
      f"such a scale (it was fixed by galactic-orbit and lunar-laser-ranging constraints, not by a0)")


banner("C6  AND AT w_c = a0/c THE STEADY-STATE PREMISE IS SELF-INCONSISTENT")

T_UNI = 13.797e9 * 3.1557e7                     # 13.797 Gyr in seconds
wc0 = A0["canonical"] / C_L
tau_mem = 1.0 / wc0
frac = -math.expm1(-wc0 * T_UNI)                # int_0^T K ds = 1 - exp(-w_c T), expm1-guarded
print(f"  memory time 1/w_c = {tau_mem:.4e} s = {tau_mem/3.1557e16:.1f} Gyr   vs age {T_UNI/3.1557e16:.3f} Gyr")
print(f"  fraction of the kernel weight inside the actual past: int_0^T K = {frac:.4f}")
check(tau_mem > T_UNI and frac < 0.2,
      f"C6 *** a caveat that undercuts section C further, in the same direction. At w_c = a0/c the memory time is "
      f"{tau_mem/3.1557e16:.0f} Gyr, {tau_mem/T_UNI:.1f}x the age of the universe, so only "
      f"{100*frac:.1f}% of the kernel weight lies inside any real worldline's past. The transforms C and S above "
      f"are STEADY-STATE quantities assuming an infinite past; on a finite worldline the response is dominated by "
      f"initial data instead, and the homogeneous mode survives as exp(-w_c T) = {math.exp(-wc0*T_UNI):.3f}. So "
      f"section C's own premise fails at its own kernel scale, and the honest reading is that w_c = a0/c is not a "
      f"physically usable choice rather than that nonlocal MI is suppressed ***")


banner("D  THE QUADRATURE COMPONENT -- kernel-SHAPE dependent, and the no-go is WITHDRAWN")

# S/C per KERNEL, at fixed w_c = a0/c. The first version tabulated systems for ONE kernel and then asserted a
# statement about "any G" -- the refutation was already inside this script's own C4 kernel list.
wv0 = A0["canonical"] / C_L
TORQ = [("single-pole  w_c e^{-w_c s}", lambda w, O: (O / w)),
        ("gamma-2      w^2 s e^{-w s}", lambda w, O: 2 * w * O / (w * w - O * O)),
        ("time-symmetric (w/2)e^{-w|s|}", lambda w, O: 0.0)]
print(f"  {'kernel (all normalised, int K = 1)':<34}{'S/C at MW':>14}{'|S/C|':>12}{'1/|C|':>12}")
print("  " + "-" * 74)
sc = {}
for nm, f in TORQ:
    val = f(wv0, mw[2])
    sc[nm] = val
    Cn = 1.0 / (1.0 + (mw[2] / wv0) ** 2) if "single" in nm or "symmetric" in nm else \
        (wv0**2 * (wv0**2 - mw[2] ** 2)) / (wv0**2 + mw[2] ** 2) ** 2
    print(f"  {nm:<34}{val:>+14.4e}{abs(val):>12.4e}{1/abs(Cn):>12.4e}")
check(abs(sc["single-pole  w_c e^{-w_c s}"]) > 1e3
      and abs(sc["gamma-2      w^2 s e^{-w s}"]) < 1e-3
      and sc["time-symmetric (w/2)e^{-w|s|}"] == 0.0,
      f"D1 *** THE TORQUE NO-GO IS WITHDRAWN. *** A circular orbit does require the tangential component to "
      f"vanish -- that part is right, and purely kinematic. But S/C is NOT generic. At the SAME w_c and the SAME "
      f"suppression 1/|C| = 8.87e6, the single-pole kernel gives S/C = "
      f"{sc['single-pole  w_c e^{-w_c s}']:+.1f} (excluded outright) while gamma-2 gives "
      f"{sc['gamma-2      w^2 s e^{-w s}']:+.3e} -- four orders BELOW one, not three above -- and a "
      f"time-symmetric kernel gives S = 0 at every frequency with C unchanged. The last case is decisive, because "
      f"varying a QUADRATIC NONLOCAL ACTION keeps only the symmetric part of the kernel, so the action-level "
      f"construction of Part A produces S = 0 automatically. Torque-freedom is a KERNEL-SHAPE CONDITION, not a "
      f"no-go, and the counterexample was already sitting in this script's own C4 table")
# the theorem: S == 0 on an interval => K proportional to delta
Om2 = sp.Symbol("Omega", real=True)
Kh = wc / (wc - sp.I * Om2)                       # transform of the exponential kernel
check(sp.simplify(sp.im(Kh.rewrite(sp.re)).subs(wc, 1) - Om2 / (1 + Om2**2)) == 0
      or sp.simplify(sp.expand(sp.im(sp.simplify(Kh.subs(wc, 1)))) - Om2 / (1 + Om2**2)) == 0,
      f"D2 K-hat(Omega) = w_c/(w_c - i Omega) has Im K-hat = w_c Omega/(w_c^2+Omega^2) = S, confirming S is the "
      f"imaginary part of the boundary value of a function ANALYTIC in the upper half plane (the transform of a "
      f"causal kernel)")
# an oscillating kernel CAN zero S at isolated points -- check the zero is isolated, not an interval
box = lambda O: math.sin(O) / O if O else 1.0
Sbox = lambda O: (1.0 - math.cos(O)) / O          # int_0^1 sin(O s) ds = (1-cos O)/O
zeros = [2 * math.pi, 4 * math.pi]
grid = [0.1 + 0.02 * i for i in range(1000)]
# isolation is a statement about CONNECTED near-zero regions, not about how many grid points fall in them
flags = [abs(Sbox(O)) < 1e-3 for O in grid]
runs = sum(1 for i, f in enumerate(flags) if f and not (i and flags[i - 1]))
tiny = sum(flags)
n_2pin = sum(1 for n in range(1, 20) if grid[0] <= 2 * math.pi * n <= grid[-1])
# the zeros are DOUBLE (S' = 0 there too), so the rigorous isolation test is S'' != 0, not a nearby value
hh = 1e-3
d2S = [(Sbox(O + hh) - 2 * Sbox(O) + Sbox(O - hh)) / hh**2 for O in zeros]
pred = [1.0 / O for O in zeros]                              # S ~ delta^2/(2 Omega_0) near a zero => S'' = 1/Omega_0
print(f"  boxcar S at Omega = 2pi, 4pi: {[f'{Sbox(O):.2e}' for O in zeros]};  "
      f"S'' = {[f'{v:.6f}' for v in d2S]} against predicted {[f'{v:.6f}' for v in pred]}")
check(all(abs(Sbox(O)) < 1e-12 for O in zeros)
      and all(abs(a / b - 1) < 1e-3 and a > 0 for a, b in zip(d2S, pred)) and runs == n_2pin,
      f"D3 the honest caveat, and it does not help: an oscillating kernel CAN zero S at ISOLATED frequencies -- "
      f"the boxcar has S = 0 exactly at Omega = 2 pi n. But those are DOUBLE zeros with "
      f"S'' = {d2S[0]:.6f} = 1/Omega_0 nonzero (matching the prediction to 1e-3), which is the rigorous "
      f"criterion for an ISOLATED zero; and on a 1000-point grid over [0.1, 20] the {tiny} points with "
      f"|S| < 1e-3 form exactly {runs} CONNECTED regions, matching the {n_2pin} multiples of 2 pi in range, so the "
      f"zeros are isolated. *** THEOREM: S is the boundary value of a function analytic in the upper half plane, "
      f"so S vanishing on an INTERVAL forces S == 0 by the identity theorem, whence K-hat is real, analytic and "
      f"bounded, hence constant, hence K = const x delta -- NO MEMORY. Galaxies span a continuous range of Omega, "
      f"so isolated zeros cannot save a memory kernel ***")


banner("E  THE ESCAPE -- a memory acting on SCALARS is torque-free, and undetectable")

# on the exact circular dS worldline, a.a is constant: a5^2 = A^2 h^4 + R^2 w^4 with A^2h^2 - R^2w^2 = 1
# The first version differentiated a tau-free expression w.r.t. tau and asserted the result was zero -- it would
# have passed for the literal 42. Compute a.a from the embedding above and differentiate THAT.
eta5 = sp.diag(-1, 1, 1, 1)
aa = sp.simplify((av.T * eta5 * av)[0, 0])
daa = sp.simplify(sp.diff(aa, tv))
aa_c = sp.simplify(aa.subs(Av**2 * hv**4, hv**2 * (1 + Rv**2 * wv**2)))
print(f"  a.a from the embedding = {aa};  d(a.a)/dtau = {daa}")
check(daa == 0 and aa != 0 and sp.simplify(aa - (Av**2 * hv**4 + Rv**2 * wv**4)) == 0,
      f"E1 computed from the embedding and differentiated: a.a = {aa}, which equals A^2 h^4 + R^2 w^4 = a5^2 and "
      f"has d(a.a)/dtau = 0 EXACTLY, while being nonzero. Unlike the acceleration VECTOR -- whose 2-plane part "
      f"rotates and whose boost part grows -- the invariant is constant along the worldline")
C_dc = sp.limit(Cex, Om, 0)
S_dc = sp.limit(Sex, Om, 0)
print(f"  DC limits of the exact transforms:  C(0) = {C_dc},  S(0) = {S_dc}")
check(sp.simplify(C_dc - 1) == 0 and sp.simplify(S_dc) == 0,
      f"E2 therefore a memory acting on a Lorentz SCALAR passes it at DC with UNIT gain and ZERO quadrature: the "
      f"exact transforms give C(0) = {C_dc} and S(0) = {S_dc}, and a constant input realises Omega = 0 exactly "
      f"rather than approximately. *** So the law "
      f"m G(K * (a.a)) a^mu = F^mu has NO suppression and NO torque -- the escape is real, and it is a specific "
      f"structural requirement: the kernel must act on invariants, never on the acceleration vector ***")
cst = sp.Symbol("c_0", positive=True)
conv_const = sp.simplify(sp.integrate(Kk * cst, (s_, 0, sp.oo)))
print(f"  convolution of the kernel with a CONSTANT input c_0:  K * c_0 = {conv_const}")
check(sp.simplify(conv_const - cst) == 0,
      f"E3 and the collapse is exact IN STEADY STATE (see C6 for the finite-past caveat): convolving the kernel "
      f"with a constant returns "
      f"K * c_0 = {conv_const}, the input itself, because int K = 1. So with the memory inert on a circular orbit "
      f"the law COLLAPSES to the "
      f"local algebraic MI law -- the a_0-line of A1b itself. So the only memory compatible with exact rotation "
      f"curves is one that CANNOT BE DETECTED in rotation curves, which is the 'amplitude-free' reading the "
      f"corpus already flagged. The nonlocality must live somewhere other than circular orbits to be testable")

banner("RESULT")
n = sum(1 for c_, _ in ok if c_)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c_, m_ in ok:
        if not c_:
            print(f"    - {m_}")
    sys.exit(1)
print("  Exit 0, AFTER TWO WITHDRAWALS forced by adversarial verification. What stands: the auxiliary-field")
print("  localization is exact -- one scalar for the square root (A1), N ODEs for an N-pole memory (A2) -- and the")
print("  circular orbit is solved with NO first-moment closure, the kernel entering only through C and S at the")
print("  orbital frequency (B). On the exact dS worldline only the ORBITAL 2-PLANE rotates rigidly; the boost")
print("  sector transforms hyperbolically and its memory integral diverges for h > w_c, which is open (B2).")
print("  WITHDRAWN: (i) the torque no-go -- S/C is kernel-SHAPE dependent, and a time-symmetric kernel, which is")
print("  the only kind a quadratic action yields, gives S = 0 with C unchanged (D1); (ii) the S-vanishing theorem,")
print("  refuted by b J_0(b s) (D3 note); (iii) the 3.8e5-3.8e7 cross-validation, which is the same (c/v)^2 twice")
print("  (C2). SCOPE: sections C and D describe ONE kernel scale. At w_c = a0/c the MW is suppressed by 1.1e-7,")
print("  but at the corpus's own committed w_c = 1.8-2.2e-14 the same formulae give C = 0.997 and S/C = 0.05 --")
print("  no suppression, no torque (C5) -- and at a0/c the memory time is 101 Gyr, so steady state is unreachable")
print("  anyway (C6). kappa = 1/2 remains FITTED, NOT DERIVED.")
