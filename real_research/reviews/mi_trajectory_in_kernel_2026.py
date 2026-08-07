#!/usr/bin/env python3
r"""
*** WITHDRAWN CITATION, added 2026-08-07: any reference below to the r <= 9.016763 admissibility ceiling
(this file's E9 / F3) cites a bound that mi_psi_search_r2Z_2026.py (27/27) has since WITHDRAWN. sup r =
+INFINITY by explicit construction; the exact single-scale MENU ceiling is r = 9 (closed form
4(2-d)^2/(2+7d-4d^2)), and 9.016763 was 0.186% high. Nothing else in this file depends on it. ***
mi_trajectory_in_kernel_2026.py -- LANE D: FEED THE TRAJECTORY IN, AND READ OFF r.

THE DEFECT BEING FIXED.  The qwen NESS programme (qwen_36_experiment/tn14-tn26) solves a Volterra equation
    G_NESS(tau) = G_BD(tau) + q^2 (K * G_NESS)(tau)
with a kernel K(tau) = |G_R(tau)|^2 = exp(-2 eta tau) * [1/(1-exp(-H beta))]^2 whose only "thermal" content is a
CONSTANT evaluated at the Gibbons-Hawking temperature.  Signature: (tau_grid, q_sq, eta).  No trajectory, no
proper acceleration, no y.  So delta_m is a NUMBER, nu is a CONSTANT, and MOND cannot come out for any q.
tn15 line 194 already computes the correct Deser-Levin effective temperature
    T_eff(a) = sqrt(T_GH^2 + (a/2pi)^2) = sqrt(a^2+H^2)/(2 pi)                       [ = the master formula's T ]
and tn15 defines source_spectrum(omega, accel) = 1/(exp(omega/T_eff)-1); its last use is a print loop (line 207).

THE FIX.  Put the trajectory in through exactly that function.  The kernel becomes
    K_a(tau) = exp(-2 eta tau) * Re G_th(tau; T_eff(a)),
    Re G_th(tau;T) = Int_0^inf dnu rho_0(nu) [1 + 2 source_spectrum(nu, a)] cos(nu tau)                    [ K1 ]
i.e. qwen's acceleration-BLIND constant Bose factor is replaced by the acceleration-RESOLVED one at the
Deser-Levin temperature.  rho_0 is the STATE-INDEPENDENT worldline spectral density (established result 3):
    rho_0(omega) = (omega/pi^2) * sinh(omega(pi-delta))/sinh(pi omega)  ->  omega/pi^2  as delta -> 0,
delta being the iepsilon time regulator already present in qwen's G_BD (they use 1e-8, which no grid can resolve;
we use it as a physical detector bandwidth Omega = 1/delta).

EXACT RESOLVENT, NO PICARD.  With the causal convention K_a(0) = 0 (tn15/tn16's own GR_sq[0] = 0) the
discretised Volterra operator is UNIT LOWER TRIANGULAR: det = 1 for every coupling, so there is no critical
coupling, no bifurcation, and no iteration is needed.  tn16/tn17's "sign-flip threshold" and their
under-relaxed-Picard convergence warnings are chasing a bifurcation that cannot exist.  Because K_a is REAL, the
imaginary part of the Wightman function satisfies its own closed Volterra equation,
    Im G_a = Im G_BD + q^2 K_a * Im G_a   =>   phihat_a(omega) = phihat_BD(omega)/(1 - q^2 Khat_a(omega))  [ R1 ]
and rho_a(omega) = -(2/pi) Im phihat_a(omega).  [R1] IS the exact resolvent; we verify it against the
unit-lower-triangular forward substitution and show Picard truncation is unnecessary.

WHAT IS READ OFF.  With I(a) = delta_m(a) - delta_m(0) = f(T_eff(a)) - f(T_GH), the committed master formula
(mi_crossover_master_formula_2026.py, 14/14) gives c1 = lim_{a->inf} I/a, c2 = lim_{a->0} I/a^2,
    q = a_0/(c H_Lambda) = c1/c2 = 2 c1p/f'(T_GH),   r = 2/q,   kappa = q Z/2 = Z/r.
r = 1 -> q = 2 (Milgrom 1999); r = 4 pi -> Milgrom 2020; r = 2Z = 11.577620 -> kappa = 1/2.
Admissibility (mi_r_admissibility_bound_2026.py, 6/6): max admissible r over 7 shapes x 220 scales = 9.016763.

*** kappa = 1/2 IS FITTED, NOT DERIVED.  Nothing below derives it and nothing below is allowed to imply it. ***

CREDIT.  nu = sqrt(1+1/y) and the dS-Unruh temperature balance are Milgrom 1999 PLA 253:273 eqs 6-9, who fixes
a_0_hat = 2 c H_Lambda (r = 1); his eqs 10-11 give a second coefficient (r = 2) and Milgrom 2008
arXiv:0801.3133 sec 7.3.1 observes that the mismatch "would just point to a different effective mu(x)" -- the
r-freedom is HIS.  Temperature sqrt(a^2+Lambda/3)/2pi: Narnhofer, Peter & Thirring 1996 IJMPB 10:1507.
Five-acceleration reading: Deser & Levin 1997 CQG 14:L163.  a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994
Ann.Phys. 229:384.  rho(omega) state-independence: Raval, Hu & Anglin 1996 PRD 53:7003.
qwen_36_experiment/ is READ-ONLY here; nothing in it is modified.

Exit 0 = every check held.  No check(True): every condition below has an input that makes it print FAIL.
"""
from __future__ import annotations

import math
import sys

import numpy as np

TRAPZ = getattr(np, "trapezoid", None) or np.trapz

# ---------------------------------------------------------------- bookkeeping
OK: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    OK.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 112)
    print(f"  {t}")
    print("=" * 112)


# ---------------------------------------------------------------- constants
C_LIGHT = 2.99792458e8            # m/s
CH_LAMBDA = 5.4194e-10            # m/s^2, c H_Lambda  (canonical, pure-Lambda)
A0_CANON = 9.3614e-11             # m/s^2, kappa = 1/2, rho_DE + c H_Lambda
A0_ALT = 1.13e-10                 # m/s^2, ALT footing, rho_total + c H_0
INV_SQRT_OMLAM = 1.2082           # 1/sqrt(Omega_Lambda)
CH_0 = CH_LAMBDA * INV_SQRT_OMLAM  # m/s^2, c H_0
Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)   # 5.788810...
R_ADMISSIBLE_MAX = 9.016763       # mi_r_admissibility_bound_2026.py

H = 1.0                           # de Sitter units throughout
T_GH = 1.0 / (2.0 * math.pi)

print(__doc__)
banner("SETUP -- units, the two footings, and the detector frequency omega_0")
print(f"  Z = 2 sqrt(8 pi/3) = {Z:.6f}   2Z = {2*Z:.6f}   1/Z = {1/Z:.8f}")
print(f"  c H_Lambda = {CH_LAMBDA:.4e} m/s^2      c H_0 = {CH_0:.4e} m/s^2")
print(f"  a_0 canonical = {A0_CANON:.4e}          a_0 ALT = {A0_ALT:.4e}")

# omega_0 = the detector's own frequency.  WHY THIS VALUE: delta_m = (2/pi) Int rho/omega^2 has no IR cutoff in
# the qwen code, which is the statement that the detector has infinite response time.  The physical detector is
# the worldline itself, whose only internal frequency is omega_c = a_0/c (the acceleration scale expressed as a
# rate).  In H units that is omega_c/H_Lambda (canonical) or omega_c^ALT/H_0 (ALT).
H_LAMBDA_SI = CH_LAMBDA / C_LIGHT          # s^-1
H0_SI = CH_0 / C_LIGHT                     # s^-1
W0_CANON = (A0_CANON / C_LIGHT) / H_LAMBDA_SI
W0_ALT = (A0_ALT / C_LIGHT) / H0_SI
print(f"  omega_c/H_Lambda (canonical footing) = {W0_CANON:.8f}   [1/Z = {1/Z:.8f}]")
print(f"  omega_c/H_0      (ALT       footing) = {W0_ALT:.8f}")
print("  omega_0 is footing-INVARIANT by construction: a_0 and cH both carry 1/sqrt(Omega_Lambda).")

check(abs(W0_CANON / W0_ALT - 1.0) < 5e-3,
      f"S1 omega_0 = omega_c/H is the SAME in both footings to {100*abs(W0_CANON/W0_ALT-1):.3f}% "
      f"({W0_CANON:.6f} vs {W0_ALT:.6f}): a_0 and cH both scale as 1/sqrt(Omega_Lambda) = {INV_SQRT_OMLAM}, so "
      f"the ratio q = a_0/(cH) -- and therefore r and kappa -- is EXACTLY footing-invariant. The canonical-vs-ALT "
      f"fork cannot decide this lane in either direction")
check(abs(W0_CANON - 1.0 / Z) < 3e-4,
      f"S2 the canonical omega_0 = {W0_CANON:.8f} equals 1/Z = {1/Z:.8f} to {abs(W0_CANON-1/Z):.2e}, which is "
      f"just q_canonical restated -- a bookkeeping identity, NOT evidence for kappa = 1/2")
check(abs(A0_CANON * INV_SQRT_OMLAM / A0_ALT - 1.0) < 5e-3,
      f"S3 the two quoted a_0 values are mutually consistent with 1/sqrt(Omega_Lambda): "
      f"{A0_CANON*INV_SQRT_OMLAM:.5e} vs the quoted {A0_ALT:.5e}")


# ---------------------------------------------------------------- stable primitives
def rho0(w, delta):
    """Regulated state-independent worldline spectral density.

    rho_0(w) = (w/pi^2) sinh(w(pi-delta))/sinh(pi w), written so no sinh overflows and no
    1-exp(-x) underflows (expm1 everywhere).  delta -> 0 gives w/pi^2 exactly (established result 3).
    """
    w = np.asarray(w, dtype=float)
    b = math.pi - delta
    # sinh(wb)/sinh(pi w) = exp(-delta w) * (1-exp(-2wb))/(1-exp(-2 pi w))
    num = -np.expm1(-2.0 * w * b)
    den = -np.expm1(-2.0 * math.pi * w)
    out = np.where(w > 0.0, (w / math.pi**2) * np.exp(-delta * w) * num / np.where(den == 0.0, 1.0, den), 0.0)
    # w -> 0 limit: (w/pi^2)*(b/pi)
    small = w < 1e-12
    if np.any(small):
        out = np.where(small, (w / math.pi**2) * (b / math.pi), out)
    return out


def rhoT(w, T, delta):
    """Regulated spectral density of the thermal worldline Wightman function at temperature T.

    Exact:  rho_T(w) = (w/pi^2) sinh(w/(2T) - delta w)/sinh(w/(2T)).
    At T = T_GH = 1/2pi this is rho0().  As delta -> 0 it becomes w/pi^2 for EVERY T -- that is
    Raval-Hu-Anglin state-independence (established result 3).  At finite delta the regulator's bite is
    T-dependent, and it requires delta < 1/(2T): the detector bandwidth 1/delta must exceed 2T_eff.
    """
    w = np.asarray(w, dtype=float)
    u = w / (2.0 * T)
    v = u - delta * w                       # = w(1/(2T) - delta) ; must stay > 0
    num = -np.expm1(-2.0 * v)
    den = -np.expm1(-2.0 * u)
    out = np.where(w > 0.0, (w / math.pi**2) * np.exp(-delta * w) * num / np.where(den == 0.0, 1.0, den), 0.0)
    small = w < 1e-12
    if np.any(small):
        out = np.where(small, (w / math.pi**2) * (1.0 - 2.0 * T * delta), out)
    return out


def T_eff(a):
    """Deser-Levin effective temperature, tn15 line 194: sqrt(T_GH^2+(a/2pi)^2) = sqrt(a^2+H^2)/(2pi)."""
    return np.sqrt(np.asarray(a, dtype=float) ** 2 + H * H) / (2.0 * math.pi)


def T_eff_minus_TGH(a):
    """T_eff(a) - T_GH with the sqrt(1+a^2)-1 cancellation removed algebraically."""
    a = np.asarray(a, dtype=float)
    s = np.sqrt(1.0 + a * a)
    return (a * a) / (2.0 * math.pi * (1.0 + s))


def source_spectrum(nu, accel):
    """tn15's own source_spectrum(omega, accel) = 1/(exp(omega/T_eff)-1), expm1-stable."""
    T = T_eff(accel)
    x = np.asarray(nu, dtype=float) / T
    return np.where(x > 700.0, 0.0, 1.0 / np.expm1(np.minimum(x, 700.0)))


def one_plus_2S(nu, accel):
    """1 + 2 source_spectrum(nu, accel) = coth(nu/(2 T_eff)), overflow-free."""
    T = T_eff(accel)
    u = np.asarray(nu, dtype=float) / (2.0 * T)
    e = np.exp(-2.0 * np.minimum(u, 700.0))
    return np.where(u > 700.0, 1.0, (1.0 + e) / (-np.expm1(-2.0 * np.minimum(u, 700.0))))


def delta_2S(nu, accel):
    """2[S(nu,a) - S(nu,0)] with NO catastrophic cancellation, valid down to a = 1e-8.

    2[1/(e^x-1) - 1/(e^y-1)] = 2 expm1(y-x)/[(-expm1(-x)) expm1(y)],  x = nu/T_a, y = nu/T_GH, y > x.
    """
    nu = np.asarray(nu, dtype=float)
    Ta = T_eff(accel)
    x = nu / Ta
    y = nu / T_GH
    # y - x = nu (1/T_GH - 1/T_a) = 2 pi nu (1 - 1/sqrt(1+a^2)), cancellation removed:
    aa = float(accel) ** 2
    s = math.sqrt(1.0 + aa)
    ymx = 2.0 * math.pi * nu * aa / (s * (1.0 + s))
    xs = np.minimum(x, 700.0)
    ys = np.minimum(y, 700.0)
    safe = (y < 600.0)
    out = np.zeros_like(nu)
    num = np.expm1(np.minimum(ymx, 700.0))
    den = (-np.expm1(-xs)) * np.expm1(ys)
    out = np.where(safe & (den > 0.0), 2.0 * num / np.where(den > 0.0, den, 1.0), out)
    # y >= 600: the T_GH occupation is utterly negligible, delta_2S -> 2 S(nu, a)
    out = np.where(~safe, 2.0 * np.where(x > 700.0, 0.0, 1.0 / np.expm1(xs)), out)
    return out


def d2S_dT(nu, T):
    """d/dT [2 S(nu,T)] = (nu/(2T^2)) csch^2(nu/(2T)), overflow-free."""
    nu = np.asarray(nu, dtype=float)
    u = nu / (2.0 * T)
    e = np.exp(-2.0 * np.minimum(u, 700.0))
    csch2 = np.where(u > 350.0, 0.0, 4.0 * e / (-np.expm1(-2.0 * np.minimum(u, 700.0))) ** 2)
    return (nu / (2.0 * T * T)) * csch2


def G_th(tau, T, delta):
    """G_th(tau;T) = -T^2/sinh^2(pi T (tau - i delta)).  At T = T_GH this IS qwen's G_BD (H=1)."""
    z = math.pi * T * (np.asarray(tau, dtype=float) - 1j * delta)
    return -(T * T) / np.sinh(z) ** 2


print(f"\n  primitives built.  T_GH = {T_GH:.8f}   T_eff(1) = {float(T_eff(1.0)):.8f}   "
      f"T_eff(1e3) = {float(T_eff(1e3)):.4f}")


# ============================================================================================================
banner("A  THE PRIMITIVES ARE THE RIGHT OBJECTS -- four independent cross-checks")
# ============================================================================================================
# Everything downstream rests on three identities.  Each is checked by computing the SAME quantity along two
# genuinely different numerical routes (closed-form sinh vs spectral quadrature vs tau quadrature).

D_VAL = 0.05                      # coarse regulator so a tau grid can actually resolve it
tauA = np.concatenate([np.arange(0.0, 1.0, 1e-4), np.arange(1.0, 40.0, 1e-3)])
nuA = np.concatenate([np.logspace(-9, -4, 400), np.arange(1e-4, 500.0, 2e-4)])
rho0_nuA = rho0(nuA, D_VAL)

# --- A1  Im G_BD(tau) = - Int rho_0(nu) sin(nu tau) dnu   (state-independent, established result 3)
tt = np.array([0.02, 0.05, 0.13, 0.4, 1.0, 2.5, 6.0])
im_closed = np.imag(G_th(tt, T_GH, D_VAL))
im_spec = np.array([-TRAPZ(rho0_nuA * np.sin(nuA * t), nuA) for t in tt])
relA1 = np.max(np.abs(im_spec - im_closed) / np.abs(im_closed))
print(f"  {'tau':>8}{'Im G_BD (sinh)':>20}{'Im G_BD (spectral)':>22}{'rel':>12}")
for t, x, y in zip(tt, im_closed, im_spec):
    print(f"  {t:>8.3f}{x:>20.10e}{y:>22.10e}{abs(y/x-1):>12.2e}")
check(relA1 < 2e-5,
      f"A1 Im G_BD(tau) from the closed-form sinh equals -Int rho_0(nu) sin(nu tau) dnu to {relA1:.2e} over "
      f"tau in [0.02,6]. The imaginary part carries NO occupation factor: this is Raval-Hu-Anglin "
      f"state-independence made numerical, and it is why the acceleration can only enter through the KERNEL")

# --- A2  rho_0(omega) closed form  ==  -(2/pi) Int sin(omega tau) Im G_BD(tau) dtau   (tau route)
im_BD_tauA = np.imag(G_th(tauA, T_GH, D_VAL))
ww = np.array([0.1, 0.3, 1.0, 3.0, 10.0, 30.0])
rho_tau = np.array([-(2.0 / math.pi) * TRAPZ(np.sin(w * tauA) * im_BD_tauA, tauA) for w in ww])
rho_cf = rho0(ww, D_VAL)
relA2 = np.max(np.abs(rho_tau / rho_cf - 1.0))
print(f"\n  {'omega':>8}{'rho_0 closed form':>22}{'rho_0 (tau quad)':>20}{'rel':>12}")
for w, x, y in zip(ww, rho_cf, rho_tau):
    print(f"  {w:>8.2f}{x:>22.12f}{y:>20.12f}{abs(y/x-1):>12.2e}")
check(relA2 < 5e-5,
      f"A2 the closed form rho_0 = (w/pi^2) sinh(w(pi-delta))/sinh(pi w) agrees with the independent tau "
      f"quadrature -(2/pi)Int sin(w tau) Im G_BD dtau to {relA2:.2e}. This fixes the NORMALISATION -- qwen's "
      f"G_BD prefactor H^2/4pi^2 is exactly the one for which rho -> omega/pi^2")

# --- A3  delta -> 0 recovers established result 3 exactly
for dd in (1e-2, 1e-4, 1e-6):
    print(f"  delta = {dd:.0e}:  max |pi^2 rho_0(w)/w - 1| over w in [0.01,10] = "
          f"{np.max(np.abs(math.pi**2*rho0(np.logspace(-2,1,40), dd)/np.logspace(-2,1,40) - 1.0)):.3e}")
w3 = np.logspace(-2, 1, 40)
err3 = np.max(np.abs(math.pi**2 * rho0(w3, 1e-6) / w3 - 1.0))
err3_coarse = np.max(np.abs(math.pi**2 * rho0(w3, 1e-2) / w3 - 1.0))
check(err3 < 1e-5 and err3_coarse > 1e-4,
      f"A3 rho_0(w) -> w/pi^2 as delta -> 0 ({err3:.2e} at delta=1e-6) and NOT at finite delta "
      f"({err3_coarse:.2e} at delta=1e-2): the regulator is a real UV bandwidth Omega = 1/delta, not a cosmetic")

# --- A4  THE TRAJECTORY TIE: the kernel's noise factor IS tn15's source_spectrum at T_eff(a)
# THE KERNEL, DEFINED.  W_a(nu) = rho_0(nu) [1 + 2 source_spectrum(nu, a)].  rho_0 carries a FIXED detector
# bandwidth Omega = 1/delta -- fixed because a detector's bandwidth cannot depend on the acceleration of the
# particle it is attached to -- and ALL of the acceleration dependence sits in tn15's own occupation factor at
# the Deser-Levin temperature.  Its tau-space form is exp(-2 eta tau) Re G_th(tau;T_eff(a)) up to O(delta T_eff),
# a pure regulator artefact that vanishes as delta -> 0 (checked A4b) and whose effect on the answer is scanned
# later (check E4).  qwen's kernel is the a -> 0 freeze of this.
print("\n  A4: KERNEL SPECTRAL CONTENT.  W_a(nu) = rho_0(nu) [1 + 2 source_spectrum(nu,a)];  its cosine")
print("      transform should be Re G_th(tau; T_eff(a)) up to the O(delta T_eff) regulator artefact.")
print("      Control column = the same integral with qwen's acceleration-BLIND factor frozen at T_GH")
print("      (tn15 line 258 / tn16 line 112).  delta T_eff is printed so the artefact is visible.")
print(f"  {'a/H':>7}{'d*Teff':>8}{'tau':>6}{'Re G_th (sinh)':>19}{'W_a w/ tn15 S':>20}{'rel':>10}"
      f"{'BLIND kernel':>16}{'rel':>10}")
worstA4, worstBLIND = 0.0, 0.0
w_blind = rho0_nuA * one_plus_2S(nuA, 0.0)                  # a-blind: frozen at T_GH
for acc in (0.0, 0.5, 2.0, 8.0):
    Ta = float(T_eff(acc))
    w_nu = rho0_nuA * one_plus_2S(nuA, acc)
    for t in (0.08, 0.3):
        lhs = float(np.real(G_th(t, Ta, D_VAL)))
        rhs = float(TRAPZ(w_nu * np.cos(nuA * t), nuA))
        bl = float(TRAPZ(w_blind * np.cos(nuA * t), nuA))
        if acc <= 2.0:
            worstA4 = max(worstA4, abs(rhs / lhs - 1.0))
            if acc > 0:
                worstBLIND = max(worstBLIND, abs(bl / lhs - 1.0))
        print(f"  {acc:>7.2f}{D_VAL*Ta:>8.4f}{t:>6.2f}{lhs:>19.10e}{rhs:>20.10e}{abs(rhs/lhs-1):>10.2e}"
              f"{bl:>16.8e}{abs(bl/lhs-1):>10.2e}")
check(worstA4 < 5e-3 and worstBLIND > 5 * worstA4,
      f"A4 *** THE TRAJECTORY IS IN THE KERNEL *** the spectral content built from tn15's OWN "
      f"source_spectrum(nu, accel) at the Deser-Levin T_eff reproduces Re G_th(tau;T_eff(a)) to {worstA4:.2e} "
      f"over a/H <= 2 (where delta T_eff <= {D_VAL*float(T_eff(2.0)):.3f}), while the SAME integral with "
      f"qwen's acceleration-BLIND constant Bose factor is off by {worstBLIND:.2e} -- {worstBLIND/max(worstA4,1e-30):.0f}x "
      f"worse. So [K1] is precisely their kernel with the one-line fix their own code already contained but "
      f"never used, and the fix is NOT cosmetic. The a/H = 8 row shows the O(delta T_eff) regulator artefact "
      f"growing exactly as advertised, which is why delta is scanned in E4 rather than trusted")

# A4b  the two candidate regulated densities differ by O(delta), so the kernel definition is delta-ambiguous
nuB = np.logspace(-3, 2, 400)
print(f"\n  A4b  max_nu |rho_0 - rho_T|/rho_0 at T = T_eff(8) = {float(T_eff(8.0)):.4f}, nu in [1e-3,100]:")
ratios = []
for dd in (0.05, 0.0125, 0.003125):
    m = np.max(np.abs(rho0(nuB, dd) - rhoT(nuB, float(T_eff(8.0)), dd)) / rho0(nuB, dd))
    ratios.append(m)
    print(f"    delta = {dd:.6f}:  {m:.5e}")
sh1, sh2 = ratios[0] / ratios[1], ratios[1] / ratios[2]
check(abs(sh1 / 4.0 - 1.0) < 0.15 and abs(sh2 / 4.0 - 1.0) < 0.15,
      f"A4b the fixed-bandwidth rho_0 and the T-tied rho_T differ by O(delta) EXACTLY: quartering delta shrinks "
      f"the gap by {sh1:.3f}x then {sh2:.3f}x (both -> 4). So 'which regulated density' is a regulator "
      f"ambiguity of size O(delta T_eff), not a physical choice; the FIXED bandwidth is the physical one because "
      f"a detector's bandwidth cannot track the acceleration of the particle carrying it")
bad_T = 1.0 / (2.0 * D_VAL)
check(float(rhoT(np.array([5.0]), bad_T * 1.5, D_VAL)[0]) < 0.0
      and float(rhoT(np.array([5.0]), bad_T * 0.5, D_VAL)[0]) > 0.0,
      f"A4c the T-tied regulator additionally goes NEGATIVE for T > 1/(2 delta) = {bad_T:.1f} and stays positive "
      f"below -- a second, independent reason to fix the bandwidth. With the fixed bandwidth the only "
      f"requirement is 1/delta >> 2 T_eff(a_max) = {2*float(T_eff(1e3)):.1f}")

# --- A5  T_eff is the master formula's T, and the cancellation-free rewrite is exact
aT = np.array([1e-8, 1e-4, 1e-2, 1.0, 1e3])
naive = T_eff(aT) - T_GH
stable = T_eff_minus_TGH(aT)
print(f"\n  {'a/H':>10}{'T_eff-T_GH naive':>22}{'algebraic rewrite':>22}{'a^2/(4 pi H)':>18}")
for a_, n_, s_ in zip(aT, naive, stable):
    print(f"  {a_:>10.0e}{n_:>22.14e}{s_:>22.14e}{a_**2/(4*math.pi):>18.8e}")
check(abs(stable[0] - aT[0] ** 2 / (4 * math.pi)) / (aT[0] ** 2 / (4 * math.pi)) < 1e-12
      and abs(naive[0]) < 1e-16,
      f"A5 the deep expansion T_eff-T_GH = a^2/(4 pi H) (master formula check C1a) is reproduced by the "
      f"algebraic rewrite to {abs(stable[0]/(aT[0]**2/(4*math.pi))-1):.2e} at a = 1e-8, where the NAIVE "
      f"difference sqrt(1+a^2)-1 has already collapsed to {naive[0]:.1e} -- float64 hazard #2, live")


# ============================================================================================================
banner("B  THE EXACT RESOLVENT -- built in omega, verified against a unit-lower-triangular Volterra solve")
# ============================================================================================================
# Because K_a is REAL, phi_a(tau) = Im G_a(tau) obeys its OWN closed Volterra equation
#     phi_a = phi_BD + q^2 (K_a * phi_a),
# whose one-sided Fourier-Laplace transform is exactly  phihat_a = phihat_BD/(1 - q^2 Khat_a)   [R1].
# phihat_BD is obtained WITHOUT any tau grid: from Im G_BD = -Int rho_0(nu) sin(nu tau) dnu,
#     Im phihat_BD(w) = -(pi/2) rho_0(w)                                        (exact, closed form)
#     Re phihat_BD(w) = -Int_0^inf [nu rho_0(nu) - w rho_0(w)]/(nu^2 - w^2) dnu  (regular: P Int dnu/(nu^2-w^2)=0)
# The subtraction removes the principal-value pole ALGEBRAICALLY -- float64 hazard #2 avoided by construction.


def nu_union_grid(w_grid, eta, delta, n_global=1400, n_local=140):
    """Per-omega nu grid: global log grid + a two-sided log patch straddling the nu = omega resonance.

    The kernel integrand has a Lorentzian of width 2 eta at nu = omega; a pure log grid under-resolves it at
    large omega (coarse grids reporting unsampled extrema -- float64 hazard #4).  Clipping the patch at nu_min
    creates duplicate abscissae, which contribute exactly zero width under the trapezoid rule.
    """
    nu_min, nu_max = 1e-8, 200.0 / delta
    g = np.logspace(math.log10(nu_min), math.log10(nu_max), n_global)
    pat = eta * np.logspace(-5.0, math.log10(30.0), n_local)
    off = np.concatenate([-pat[::-1], pat])
    NU = np.clip(w_grid[:, None] + off[None, :], nu_min, nu_max)
    NU = np.concatenate([np.broadcast_to(g, (w_grid.size, g.size)), NU], axis=1)
    return np.sort(NU, axis=1)


class Machinery:
    """Everything omega-domain for one (delta, eta, omega grid).  a-independent parts are built once."""

    def __init__(self, delta, eta, w_grid):
        self.delta, self.eta, self.w = delta, eta, w_grid
        self.NU = nu_union_grid(w_grid, eta, delta)
        self.rho0_NU = rho0(self.NU, delta)
        self.rho0_w = rho0(w_grid, delta)
        s = 2.0 * eta - 1j * w_grid                      # retarded envelope exp(-2 eta tau) -> pole at nu = w
        self.KERN = s[:, None] / (s[:, None] ** 2 + self.NU ** 2)
        # Re phihat_BD via the subtracted PV integrand
        num = self.NU * self.rho0_NU - (w_grid * self.rho0_w)[:, None]
        den = self.NU ** 2 - (w_grid ** 2)[:, None]
        tiny = np.abs(self.NU - w_grid[:, None]) < 1e-11 * w_grid[:, None]
        integ = np.where(tiny, 0.0, num / np.where(tiny, 1.0, den))
        if np.any(tiny):                                  # analytic limit d(nu rho_0)/dnu / (2 w)
            hh = 1e-6 * w_grid[:, None]
            dv = ((self.NU + hh) * rho0(self.NU + hh, delta) - (self.NU - hh) * rho0(self.NU - hh, delta)) / (2 * hh)
            integ = np.where(tiny, dv / (2.0 * w_grid[:, None]), integ)
        self.phihat_BD = (-TRAPZ(integ, self.NU, axis=1)) - 1j * (math.pi / 2.0) * self.rho0_w

    def Khat(self, accel):
        """Khat_a(omega) with the trajectory in, through tn15's source_spectrum at Deser-Levin T_eff."""
        return TRAPZ(self.rho0_NU * one_plus_2S(self.NU, accel) * self.KERN, self.NU, axis=1)

    def dKhat(self, accel):
        """Khat_a - Khat_0, computed with the Bose-factor difference done cancellation-free."""
        return TRAPZ(self.rho0_NU * delta_2S(self.NU, accel) * self.KERN, self.NU, axis=1)

    def dKhat_dT(self):
        """d Khat/dT at T = T_GH -- the analytic derivative, so f'(T_GH) needs no finite difference."""
        return TRAPZ(self.rho0_NU * d2S_dT(self.NU, T_GH) * self.KERN, self.NU, axis=1)

    def rho_a(self, accel, q_sq):
        """Exact resolvent [R1]: no iteration, no Picard, valid for every coupling."""
        return -(2.0 / math.pi) * np.imag(self.phihat_BD / (1.0 - q_sq * self.Khat(accel)))

    def drho_a(self, accel, q_sq):
        """rho_a - rho_0 with no cancellation between two nearly equal resolvents."""
        K0, dK = self.Khat(0.0), self.dKhat(accel)
        Ka = K0 + dK
        return -(2.0 / math.pi) * np.imag(self.phihat_BD * q_sq * dK
                                          / ((1.0 - q_sq * Ka) * (1.0 - q_sq * K0)))

    def drho_dT(self, q_sq):
        K0 = self.Khat(0.0)
        return -(2.0 / math.pi) * np.imag(self.phihat_BD * q_sq * self.dKhat_dT() / (1.0 - q_sq * K0) ** 2)

    def moment(self, rho_vals, w0):
        """delta_m-type moment (2/pi) Int rho(w)/(w^2+w0^2) dw, integrated in log w."""
        return (2.0 / math.pi) * TRAPZ(rho_vals * self.w / (self.w ** 2 + w0 ** 2), np.log(self.w))


DELTA, ETA = 2e-3, 0.1
W_GRID = np.logspace(-3.0, math.log10(600.0), 420)
MACH = Machinery(DELTA, ETA, W_GRID)
print(f"  production settings: delta = {DELTA:.1e} (bandwidth Omega = {1/DELTA:.0f} H, vs 2 T_eff(1e3) = "
      f"{2*float(T_eff(1e3)):.1f}),  eta = {ETA},  {W_GRID.size} log-spaced omega in "
      f"[{W_GRID[0]:.1e}, {W_GRID[-1]:.0f}],  {MACH.NU.shape[1]} nu abscissae per omega")

# --- B1  Re phihat_BD from the subtracted PV integral vs an independent tau quadrature
tauB = np.concatenate([np.arange(0.0, 0.2, DELTA / 200.0), np.arange(0.2, 30.0, 5e-5)])
imGB = np.imag(G_th(tauB, T_GH, DELTA))
idx = [int(np.argmin(np.abs(W_GRID - w))) for w in (0.05, 0.1727, 0.5, 2.0, 8.0, 40.0)]
wB = W_GRID[idx]                                     # compare AT the grid points, not near them
re_tau = np.array([TRAPZ(np.cos(w * tauB) * imGB, tauB) for w in wB])
im_tau = np.array([TRAPZ(np.sin(w * tauB) * imGB, tauB) for w in wB])
re_pv = np.real(MACH.phihat_BD[idx])
im_cf = np.imag(MACH.phihat_BD[idx])
print(f"\n  {'omega':>9}{'Re phihat (PV quad)':>22}{'Re phihat (tau quad)':>22}{'rel':>10}"
      f"{'Im phihat (closed)':>21}{'Im (tau quad)':>16}{'rel':>10}")
worstB1 = worstB1i = 0.0
for w, a1, a2, b1, b2 in zip(wB, re_pv, re_tau, im_cf, im_tau):
    worstB1 = max(worstB1, abs(a2 / a1 - 1.0))
    worstB1i = max(worstB1i, abs(b2 / b1 - 1.0))
    print(f"  {w:>9.4f}{a1:>22.12e}{a2:>22.12e}{abs(a2/a1-1):>10.2e}{b1:>21.12e}{b2:>16.8e}{abs(b2/b1-1):>10.2e}")
check(worstB1 < 3e-4 and worstB1i < 3e-4,
      f"B1 both parts of phihat_BD agree between the subtracted-PV nu quadrature and an independent tau "
      f"quadrature of the closed-form Im G_BD: Re to {worstB1:.2e}, Im to {worstB1i:.2e}. This validates the "
      f"whole omega-domain construction, including the P Int dnu/(nu^2-w^2) = 0 subtraction")


# --- B2  the unit-lower-triangular Volterra solve: det = 1, exact, and Picard is unnecessary
D_V, ETA_V, TAU_MAX_V, A_V = 0.05, 0.5, 20.0, 2.0
QSQ_V = 0.45          # calibrated so max|q^2 Khat| ~ 0.5: the resolvent must be NONTRIVIAL or the
                      # two routes agree trivially at roundoff and the comparison tests nothing
W_CMP = np.logspace(math.log10(0.05), math.log10(20.0), 25)


def tau_domain_solve(dtau):
    """Exact forward substitution for phi_a = phi_BD + q^2 (K_a * phi_a) on a uniform grid.

    With the causal convention K_a(0) = 0 -- tn15 line 258 / tn16 line 114 set GR_sq[0] = 0 themselves -- the
    trapezoid discretisation is I - q^2 L with L STRICTLY lower triangular.  Unit diagonal => det = 1 for every
    coupling => invertible at every q, no critical coupling, and one sweep is EXACT.  No iteration anywhere.
    """
    tau = np.arange(0.0, TAU_MAX_V + 0.5 * dtau, dtau)
    n = tau.size
    phi_bd = np.imag(G_th(tau, T_GH, D_V))
    K = np.exp(-2.0 * ETA_V * tau) * np.real(G_th(tau, float(T_eff(A_V)), D_V))
    K[0] = 0.0                                                # causality convention, theta(0) = 0
    phi = np.empty(n)
    phi[0] = phi_bd[0]
    for i in range(1, n):
        w = K[i:0:-1].copy()                                  # K[i-j] for j = 0..i-1
        w[0] *= 0.5                                           # trapezoid end weight at tau' = 0
        phi[i] = phi_bd[i] + QSQ_V * dtau * float(np.dot(w, phi[:i]))
    return tau, phi, phi_bd, K


def omega_side(tau, phi_bd, K, w_grid):
    """Same kernel, same grid, but through the algebraic resolvent phihat_BD/(1-q^2 Khat)."""
    E = np.exp(1j * w_grid[:, None] * tau[None, :])
    ph = TRAPZ(E * phi_bd[None, :], tau, axis=1)
    Kh = TRAPZ(E * K[None, :], tau, axis=1)
    return -(2.0 / math.pi) * np.imag(ph / (1.0 - QSQ_V * Kh)), Kh


def rho_from_tau(tau, phi, w_grid):
    return np.array([-(2.0 / math.pi) * TRAPZ(np.sin(w * tau) * phi, tau) for w in w_grid])


rel_ref, dev_ref = [], []
for dtau in (4e-3, 1e-3):
    tau_v, phi_v, phibd_v, K_v = tau_domain_solve(dtau)
    rho_tau = rho_from_tau(tau_v, phi_v, W_CMP)
    rho_om, Kh_v = omega_side(tau_v, phibd_v, K_v, W_CMP)
    rho_free = rho_from_tau(tau_v, phibd_v, W_CMP)
    rel = float(np.max(np.abs(rho_tau / rho_om - 1.0)))
    dev = float(np.max(np.abs(rho_tau / rho_free - 1.0)))
    rel_ref.append(rel)
    dev_ref.append(dev)
    print(f"  dtau = {dtau:.0e} (N = {tau_v.size:6d}):  max|q^2 Khat| = {np.max(np.abs(QSQ_V*Kh_v)):.4f}, "
          f"dressing max|rho_a/rho_0-1| = {dev:.3e},  max|rho_tau/rho_omega - 1| = {rel:.3e}")
check(rel_ref[-1] < 1e-3 and dev_ref[-1] > 0.05,
      f"B2 the tau-domain unit-lower-triangular forward substitution and the algebraic resolvent [R1] give the "
      f"same rho_a(omega) to {rel_ref[-1]:.2e} at a coupling that dresses rho by {100*dev_ref[-1]:.1f}% -- so the "
      f"agreement is a real test of the resolvent, not two routes both returning rho_0. Two independent routes, "
      f"one exact sweep each")

# det = 1 for every coupling: established by (i) showing the operator really IS strictly lower triangular as
# built from the kernel array, and (ii) checking slogdet numerically where LU pivoting is still well conditioned.
nS = 400
dtS = 4e-3
tauS = np.arange(0.0, nS) * dtS
KS = np.exp(-2.0 * ETA_V * tauS) * np.real(G_th(tauS, float(T_eff(A_V)), D_V))
KS[0] = 0.0                                                   # causality convention, theta(0) = 0
rows = np.arange(nS)[:, None] - np.arange(nS)[None, :]
L = np.where(rows >= 0, KS[np.clip(rows, 0, nS - 1)], 0.0)    # Toeplitz K[i-j], causal
L[:, 0] *= 0.5                                                # trapezoid end weight at tau' = 0
np.fill_diagonal(L, 0.5 * KS[0])                              # = 0 exactly, because K(0) = 0
upper = float(np.max(np.abs(np.triu(L, 1))))
diag = float(np.max(np.abs(np.diag(L))))
print(f"  operator L from the kernel array: max|upper triangle| = {upper:.3e}, max|diagonal| = {diag:.3e}")
lds = []
with np.errstate(all="ignore"):
    for qs in (1e-6, 1e-3, 1.0, 10.0):
        M = np.eye(nS) - qs * dtS * L
        _, ld = np.linalg.slogdet(M)
        pd = float(np.sum(np.log(np.abs(np.diag(M)))))       # exact for a triangular matrix
        lds.append(max(abs(ld), abs(pd)))
        print(f"  q^2 = {qs:8.0e}:  |log det| = {abs(ld):.3e} (LU),  {abs(pd):.3e} (product of diagonals)")
KS_bad = float(np.real(G_th(np.array([0.0]), float(T_eff(A_V)), D_V))[0])
Lbad = L.copy()
np.fill_diagonal(Lbad, 0.5 * KS_bad)
with np.errstate(all="ignore"):
    _, ld_bad = np.linalg.slogdet(np.eye(nS) - 1.0 * dtS * Lbad)
check(upper == 0.0 and diag == 0.0 and max(lds) < 1e-12 and abs(ld_bad) > 1e-3,
      f"B3 the discretised operator built from the kernel array is STRICTLY lower triangular (upper triangle and "
      f"diagonal both exactly zero), so I - q^2 dtau L has unit diagonal and det = 1 for EVERY coupling by the "
      f"triangular-determinant theorem -- confirmed numerically to {max(lds):.1e} up to q^2 = 10, and NOT 1 "
      f"(log det = {ld_bad:+.4f}) once the tau = 0 diagonal term K(0) = {KS_bad:.1f} is put back. Under tn16's "
      f"own K(0) = 0 convention there is therefore no critical coupling and no bifurcation: tn16's 'sign-flip "
      f"threshold q^2 ~ 3e-2' and tn17's under-relaxed Picard were hunting a pole a unit-triangular operator "
      f"cannot have")

# forward substitution is the exact solve, not an approximation to it
Mfull = np.eye(nS) - QSQ_V * dtS * L
phibd_S = np.imag(G_th(tauS, T_GH, D_V))
phi_dense = np.linalg.solve(Mfull, phibd_S)
phi_fs = np.empty(nS)
phi_fs[0] = phibd_S[0]
for i in range(1, nS):
    w = KS[i:0:-1].copy()
    w[0] *= 0.5
    phi_fs[i] = phibd_S[i] + QSQ_V * dtS * float(np.dot(w, phi_fs[:i]))
rel_fs = float(np.max(np.abs(phi_fs - phi_dense)) / np.max(np.abs(phi_dense)))
print(f"  forward substitution vs dense LU solve: max relative difference = {rel_fs:.3e}")
check(rel_fs < 1e-12,
      f"B3b one forward sweep reproduces the dense LU solve of the same system to {rel_fs:.1e}: the sweep IS the "
      f"exact resolvent, so nothing in this lane is an iteration or a truncation")

# Picard, which the corpus uses, is strictly worse than one exact sweep
tau_v, phi_v, phibd_v, K_v = tau_domain_solve(4e-3)
Kf = K_v.copy()
Kf[0] *= 0.5
pic = phibd_v.copy()
errs = []
for it in range(1, 81):
    conv = np.convolve(pic, Kf)[: pic.size] * 4e-3
    pic = phibd_v + QSQ_V * conv
    if it in (1, 5, 20, 80):
        errs.append((it, float(np.max(np.abs(pic - phi_v)) / np.max(np.abs(phi_v)))))
for it, e in errs:
    print(f"  Picard iteration {it:3d}: max |phi_Picard - phi_exact| / max|phi_exact| = {e:.3e}")
check(errs[0][1] > 1e-3 and errs[-1][1] < 1e-10,
      f"B4 Picard does eventually reach the same answer ({errs[-1][1]:.1e} after 80 sweeps) but is never needed "
      f"-- one triangular sweep is already exact, while Picard iteration 1 is still off by {errs[0][1]:.1e} and "
      f"iteration 5 by {errs[1][1]:.1e}. A Volterra-Neumann series ALWAYS converges, so tn17's 'WARNING: No "
      f"convergence in 200 iters' reports its own under-relaxation factor 0.15, not the physics")


# --- B5  Machinery's resolvent really is the resummation, not its first-order truncation
K0 = MACH.Khat(0.0)
QS_B5 = 0.5 / float(np.max(np.abs(K0)))                  # dress to max|q^2 Khat| = 0.5
x = QS_B5 * MACH.Khat(1.0)
neumann = np.zeros_like(x)
term = np.ones_like(x)
for n in range(400):                                      # explicit sum_{n>=0} (q^2 Khat)^n
    neumann = neumann + term
    term = term * x
rho_res = MACH.rho_a(1.0, QS_B5)
rho_neu = -(2.0 / math.pi) * np.imag(MACH.phihat_BD * neumann)
rho_1st = -(2.0 / math.pi) * np.imag(MACH.phihat_BD * (1.0 + x))
relN = float(np.max(np.abs(rho_res / rho_neu - 1.0)))
rel1 = float(np.max(np.abs(rho_res / rho_1st - 1.0)))
print(f"\n  B5 at q^2 = {QS_B5:.4e} (max|q^2 Khat| = {np.max(np.abs(x)):.3f}):")
print(f"     closed resolvent vs the explicitly summed Neumann series: {relN:.3e}")
print(f"     closed resolvent vs its FIRST-ORDER truncation 1 + q^2 Khat: {rel1:.3e}")
check(relN < 1e-12 and rel1 > 0.1,
      f"B5 Machinery's rho_a uses the full resummation 1/(1-q^2 Khat): it reproduces the explicitly summed "
      f"Neumann series to {relN:.1e} and differs from the first-order truncation 1 + q^2 Khat by {100*rel1:.1f}% at "
      f"a coupling that dresses rho appreciably. The production sweep is then run at q^2 = 1e-8, where the two "
      f"agree to machine precision by design -- which is the point of E4, not a hidden approximation")

# ============================================================================================================
banner("C  THE EXTRACTOR -- anchored on the two cases whose answer is independently known")
# ============================================================================================================
# The master formula reads q off an I(a) curve as c1/c2 with c1 = lim_{a->inf} I/a and c2 = lim_{a->0} I/a^2.
# Both limits are approached with O(1/a) and O(a^2) corrections, so a bare endpoint value is biased; we
# Richardson-extrapolate and then validate the extractor on f = T (answer q = 2, Milgrom 1999) and on the
# exponential counterexample of mi_crossover_master_formula_2026.py check C3 (answer q = 1/Z).

A_GRID = np.logspace(-3.0, 3.0, 49)


def extract_q(a_vals, I_vals, n_hi=8, n_lo=8):
    """c1 from a linear fit of I/a vs 1/a at large a; c2 from I/a^2 vs a^2 at small a."""
    a_vals, I_vals = np.asarray(a_vals, float), np.asarray(I_vals, float)
    hi = np.argsort(a_vals)[-n_hi:]
    lo = np.argsort(a_vals)[:n_lo]
    p1 = np.polyfit(1.0 / a_vals[hi], I_vals[hi] / a_vals[hi], 2)   # two Richardson orders: O(1/a), O(1/a^2)
    p2 = np.polyfit(a_vals[lo] ** 2, I_vals[lo] / a_vals[lo] ** 2, 2)
    c1, c2 = float(p1[-1]), float(p2[-1])
    raw1 = float(I_vals[hi][-1] / a_vals[hi][-1])
    raw2 = float(I_vals[lo][0] / a_vals[lo][0] ** 2)
    return c1, c2, c1 / c2, abs(raw1 / c1 - 1.0), abs(raw2 / c2 - 1.0)


TT = T_eff(A_GRID)
I_lin = TT - T_GH
c1L, c2L, qL, d1L, d2L = extract_q(A_GRID, I_lin)
print(f"  anchor 1, f = T (Milgrom 1999):  c1 = {c1L:.10f} [1/2pi = {1/(2*math.pi):.10f}], "
      f"c2 = {c2L:.10f} [1/4pi = {1/(4*math.pi):.10f}], q = {qL:.10f}")
check(abs(qL - 2.0) < 1e-5 and abs(c1L - 1 / (2 * math.pi)) < 1e-7 and abs(c2L - 1 / (4 * math.pi)) < 1e-7,
      f"C1 the extractor returns q = {qL:.8f} on f = T, i.e. Milgrom 1999's q = 2, with c1 = 1/2pi and "
      f"c2 = 1/4pi to 1e-7. Anchored on the one case whose answer is independently known")

LAM = 2.0 * Z - 1.0
I_exp = (TT - T_GH) + LAM * T_GH * (-np.expm1(-(TT - T_GH) / T_GH))
c1E, c2E, qE, d1E, d2E = extract_q(A_GRID, I_exp)
print(f"  anchor 2, the r = 2Z counterexample:  q = {qE:.8f}  [target 1/Z = {1/Z:.8f}], "
      f"r = {2/qE:.6f} [target 2Z = {2*Z:.6f}]")
check(abs(qE / (1 / Z) - 1.0) < 3e-3,
      f"C2 the extractor returns q = {qE:.8f} = {100*qE*Z:.2f}% of 1/Z on the asymptotically-linear exponential "
      f"whose slope at the floor is 2Z -- mi_crossover_master_formula_2026.py's own counterexample. So the "
      f"extractor can see r = 2Z when r = 2Z is really there; if the trajectory kernel does not give 2Z below, "
      f"that is the kernel's answer and not the extractor's blindness")
I_wrong = (TT - T_GH) * (1.0 + 0.0 * TT)
check(abs(extract_q(A_GRID, I_wrong)[2] - 2.0) < 1e-5 and abs(qE - 2.0) > 1.0,
      f"C3 the extractor DISCRIMINATES: it returns {extract_q(A_GRID, I_wrong)[2]:.6f} on the linear f and {qE:.4f} on the r = 2Z f, a "
      f"factor {2/qE:.2f} apart. It is not returning a constant")


# ============================================================================================================
banner("D  THE SWEEP -- delta_m(a) with the trajectory in, a/H from 1e-3 to 1e3")
# ============================================================================================================
QSQ = 1e-8                      # perturbative: max|q^2 Khat| below is printed, and E3 shows r is q-independent
                                # here and NOT q-independent once the resolvent goes nonperturbative


def first_moment(mach, rho_vals):
    """(2/pi) Int rho(w)/w dw -- the FIRST moment.  IR-convergent, needs no omega_0 at all."""
    return (2.0 / math.pi) * TRAPZ(rho_vals, np.log(mach.w))


def sweep(mach, w0, q_sq, a_vals):
    dr = [mach.drho_a(a, q_sq) for a in a_vals]
    I2 = np.array([mach.moment(d, w0) for d in dr])       # Caldeira-Leggett delta_m, the corpus's object
    I1 = np.array([first_moment(mach, d) for d in dr])
    return dr, I2, I1


DR, I2, I1 = sweep(MACH, W0_CANON, QSQ, A_GRID)
DM0 = MACH.moment(MACH.rho_a(0.0, QSQ), W0_CANON)
FP2 = MACH.moment(MACH.drho_dT(QSQ), W0_CANON)
FP1 = first_moment(MACH, MACH.drho_dT(QSQ))
print(f"  q^2 = {QSQ:.0e}, max|q^2 Khat_0| = {np.max(np.abs(QSQ*MACH.Khat(0.0))):.3e};  "
      f"delta_m(a=0) = {DM0:.6f};  omega_0 = {W0_CANON:.6f} (canonical footing)")
print(f"\n  {'a/H':>10}{'T_eff':>10}{'delta_m(a)-delta_m(0)':>24}{'I/a^2':>14}{'I/a':>14}"
      f"{'d log I/d log a':>17}{'1st moment I_1':>16}")
lg = np.gradient(np.log(I2), np.log(A_GRID))
for i in range(0, A_GRID.size, 4):
    a_ = A_GRID[i]
    print(f"  {a_:>10.3e}{float(T_eff(a_)):>10.4f}{I2[i]:>24.8e}{I2[i]/a_**2:>14.6e}{I2[i]/a_:>14.6e}"
          f"{lg[i]:>17.4f}{I1[i]:>16.6e}")

c1_2, c2_2, q_2, dr1_2, dr2_2 = extract_q(A_GRID, I2)
c1_1, c2_1, q_1, dr1_1, dr2_1 = extract_q(A_GRID, I1)
print(f"\n  CL second moment : c1 = {c1_2:.6e}  c2 = {c2_2:.6e}   q = {q_2:.6f}   r = {2/q_2:.5f}")
print(f"  first moment     : c1 = {c1_1:.6e}  c2 = {c2_1:.6e}   q = {q_1:.6f}   r = {2/q_1:.5f}")
print(f"  raw-endpoint vs Richardson drift:  c1 {dr1_2:.4f} (2nd) / {dr1_1:.4f} (1st);   "
      f"c2 {dr2_2:.2e} (2nd) / {dr2_1:.2e} (1st)")

check(abs(c2_2 * 4.0 * math.pi / FP2 - 1.0) < 1e-5 and abs(c2_1 * 4.0 * math.pi / FP1 - 1.0) < 1e-5,
      f"D1 the DEEP side is exact: c2 extracted from lim I/a^2 equals f'(T_GH)/(4 pi) computed from the ANALYTIC "
      f"temperature derivative (2/pi)Int dT[2S] .../(w^2+w0^2) to {abs(c2_2*4*math.pi/FP2-1):.1e} (2nd moment) and "
      f"{abs(c2_1*4*math.pi/FP1-1):.1e} (1st). Two routes, one with a finite difference and one without, so the "
      f"a -> 0 end of the master formula is under control")
check(abs(lg[0] - 2.0) < 1e-3,
      f"D2 the deep exponent is d log I/d log a = {lg[0]:.5f} at a/H = 1e-3, i.e. I ~ a^2 exactly: the kernel "
      f"reproduces the deep-MOND side of Milgrom's balance without being asked to")
check(abs(dr1_2) > 0.2 and abs(dr2_2) < 1e-4,
      f"D3 *** THE NEWTONIAN SIDE FAILS *** c2 is converged (raw endpoint differs from the extrapolation by "
      f"{dr2_2:.1e}) but c1 is NOT (drift {dr1_2:.3f}, five orders of magnitude worse). I/a is still falling at "
      f"a/H = 1e3: {I2[-1]/A_GRID[-1]:.4e} against {I2[-9]/A_GRID[-9]:.4e} at a/H = {A_GRID[-9]:.0f}. There is no "
      f"I ~ a asymptote, so lim I/a is not a nonzero number and q = c1/c2 is not defined")

# D4  the acceleration enters the kernel: two independent routes to Khat_a must agree
route_full = np.array([np.max(np.abs(MACH.Khat(a))) for a in A_GRID[::6]])
route_diff = np.array([np.max(np.abs(MACH.Khat(0.0) + MACH.dKhat(a))) for a in A_GRID[::6]])
relK = float(np.max(np.abs(np.array([np.max(np.abs(MACH.Khat(a) - MACH.Khat(0.0) - MACH.dKhat(a)))
                                     / np.max(np.abs(MACH.Khat(a))) for a in A_GRID[::6]])))) 
print(f"\n  Khat_a via the full occupation vs Khat_0 + (cancellation-free difference): "
      f"max relative gap = {relK:.3e}")
spanK = float(np.max(np.abs(MACH.dKhat(A_GRID[-1]))) / np.max(np.abs(MACH.dKhat(A_GRID[0]))))
check(relK < 1e-12 and spanK > 1e6,
      f"D5 the two routes to Khat_a -- the full Bose factor 1+2 source_spectrum(nu,a), and Khat_0 plus the "
      f"cancellation-free difference 2[S(nu,a)-S(nu,0)] -- agree to {relK:.1e} across six decades of a/H, and the "
      f"difference itself spans {spanK:.2e} between a/H = 1e-3 and 1e3. So the acceleration really is in the "
      f"kernel, and delta_2S's expm1 rewrite is exact rather than merely stable")

# D4  qwen's literal kernel: exp(-2 eta tau) * [1/(1-exp(-H beta))]^2, with NO a anywhere
BLIND_FACTOR_SQ = (1.0 / (-math.expm1(-2.0 * math.pi))) ** 2      # tn15 line 258 / tn16 line 112


def blind_I(a_vals, q_sq, w0):
    """I(a) through the resolvent with qwen's acceleration-blind kernel.

    Khat_blind(omega) = C^2 Int_0^inf exp((i omega - 2 eta) tau) dtau = C^2/(2 eta - i omega), no a in it.
    Evaluated separately at each a, so any a-dependence anywhere in the chain would show up here.
    """
    Kb = BLIND_FACTOR_SQ / (2.0 * MACH.eta - 1j * MACH.w)
    rho_b = -(2.0 / math.pi) * np.imag(MACH.phihat_BD / (1.0 - q_sq * Kb))
    base = MACH.moment(rho_b, w0)
    return np.array([MACH.moment(-(2.0 / math.pi) * np.imag(MACH.phihat_BD / (1.0 - q_sq * Kb)), w0) - base
                     for _ in a_vals])


I_blind = blind_I(A_GRID, QSQ, W0_CANON)
print(f"  qwen's literal blind kernel: max|I(a)| = {np.max(np.abs(I_blind)):.3e} over a/H in [1e-3,1e3]; "
      f"trajectory kernel: {np.min(np.abs(I2)):.3e} to {np.max(np.abs(I2)):.3e}")
check(np.max(np.abs(I_blind)) == 0.0 and np.max(np.abs(I2)) / np.min(np.abs(I2)) > 1e7,
      f"D4 with qwen's kernel exp(-2 eta tau) C^2, C = 1/(1-exp(-H beta)), I(a) is IDENTICALLY zero -- not small, "
      f"exactly zero -- because there is no a in the expression, while the trajectory-carrying kernel gives I(a) "
      f"spanning {np.max(np.abs(I2))/np.min(np.abs(I2)):.2e} over the same range. That is the structural defect of "
      f"tn14-tn26 in one line: with solver signature (tau_grid, q_sq, eta), delta_m is a NUMBER, nu is a CONSTANT, "
      f"and no MOND can emerge for ANY coupling. The informative half of this check is the second clause")

# ============================================================================================================
banner("E  THE T^3 TEST, THE IR, AND THE ROBUSTNESS SCANS")
# ============================================================================================================
# E1  THE T^3 TEST.  A finite r needs the gain-band weight to scale as T^3 against the 1/omega^2 measure.  We
# measure three exponents against log T_eff on the UV-safe window a >= 3, T_eff <= 0.05/delta:
#   p_W     from W(a)     = Int |Delta rho| domega            (amplitude x width, the lane's quantity)
#   p_omega from wbar(a)  = Int w |Delta rho| dw / W(a)       (does the band track T?)
#   p_delta from I(a)                                        (the operative criterion: p_delta = 1 <=> c1p finite)
# The T^3 form of the criterion is the special case p_omega = 1.  We report both and say which one bites.

def exponents(mach, w0, q_sq, a_vals, drho_list):
    sel = (a_vals >= 3.0) & (T_eff(a_vals) <= 0.05 / mach.delta)
    T = T_eff(a_vals[sel])
    d = [x for x, s in zip(drho_list, sel) if s]
    Wl = np.array([TRAPZ(np.abs(x) * mach.w, np.log(mach.w)) for x in d])
    cen = np.array([TRAPZ(np.abs(x) * mach.w ** 2, np.log(mach.w)) / w for x, w in zip(d, Wl)])
    I2s = np.array([mach.moment(x, w0) for x in d])
    I1s = np.array([first_moment(mach, x) for x in d])
    out = {}
    for nm, y in (("p_W", Wl), ("p_omega", cen), ("p_delta_2nd", I2s), ("p_delta_1st", I1s)):
        pf, cov = np.polyfit(np.log(T), np.log(y), 1, cov=True)
        out[nm] = (float(pf[0]), float(math.sqrt(cov[0, 0])))
    return out, int(sel.sum()), (float(T[0]), float(T[-1]))


EXP, nsel, Trange = exponents(MACH, W0_CANON, QSQ, A_GRID, DR)
print(f"  regression window: {nsel} points, T_eff in [{Trange[0]:.2f}, {Trange[1]:.1f}]  "
      f"(UV-safe: T_eff <= 0.05/delta = {0.05/DELTA:.0f})")
for k in ("p_W", "p_omega", "p_delta_2nd", "p_delta_1st"):
    print(f"    {k:>12s} = {EXP[k][0]:+.4f} +/- {EXP[k][1]:.4f}")
pW, sW = EXP["p_W"]
pw, sw = EXP["p_omega"]
p2, s2 = EXP["p_delta_2nd"]
p1, s1 = EXP["p_delta_1st"]
check(pW < 3.0 - 5.0 * sW,
      f"E1 *** THE T^3 TEST FIRES *** the gain-band weight (amplitude x width) scales as T^{pW:.4f} +/- {sW:.4f}, "
      f"which is below 3 by {(3-pW)/sW:.0f} fit sigma. On the lane's criterion that is a clean no-go: this "
      f"mechanism cannot produce an acceleration scale at all")
check(abs(pw - 1.0) > 5.0 * sw and abs(p2 - (pW - 2.0 * pw)) > 0.5,
      f"E1b AGAINST THE TEST ITSELF, and this must be said: the band does NOT track T (p_omega = {pw:.4f} +/- "
      f"{sw:.4f}, not 1), so the T^3 form is not applicable verbatim -- it is the p_omega = 1 special case. The "
      f"heuristic identity p_delta = p_W - 2 p_omega gives {pW-2*pw:.3f} against the measured {p2:.3f}, i.e. it "
      f"FAILS, because the L1 band sits near omega ~ 1e2 while the delta_m weight sits near omega ~ 1. The "
      f"operative criterion is p_delta = 1, not p_W = 3")
check(abs(p2 - 1.0) > 10.0 * s2,
      f"E1c and the operative criterion fires the same way: p_delta = {p2:.4f} +/- {s2:.4f} for the "
      f"Caldeira-Leggett delta_m, which is {abs(p2-1)/s2:.0f} sigma from the 1 that a finite nonzero c1p requires")
# E1e  the same three exponents on the wider, UV-safer window (delta 10x smaller): does the verdict move?
MACH_F = Machinery(2e-4, ETA, np.logspace(-5.0, math.log10(6000.0), 520))
DR_F, I2_F, I1_F = sweep(MACH_F, W0_CANON, QSQ, A_GRID)
EXP_F, nsel_F, Trange_F = exponents(MACH_F, W0_CANON, QSQ, A_GRID, DR_F)
print(f"\n  wider window (delta = 2e-4, {nsel_F} points, T_eff in [{Trange_F[0]:.2f}, {Trange_F[1]:.1f}]):")
for k in ("p_W", "p_omega", "p_delta_2nd", "p_delta_1st"):
    print(f"    {k:>12s} = {EXP_F[k][0]:+.4f} +/- {EXP_F[k][1]:.4f}")
check(EXP_F["p_W"][0] < 3.0 - 5.0 * EXP_F["p_W"][1] and abs(EXP_F["p_delta_2nd"][0] - 1.0) > 10 * EXP_F["p_delta_2nd"][1]
      and abs(EXP_F["p_delta_1st"][0] - 1.0) < 0.15,
      f"E1e the verdict is regulator-stable: on a window ten times wider in T_eff (up to {Trange_F[1]:.0f}) the "
      f"exponents are p_W = {EXP_F['p_W'][0]:.4f}, p_delta(2nd) = {EXP_F['p_delta_2nd'][0]:.4f}, "
      f"p_delta(1st) = {EXP_F['p_delta_1st'][0]:.4f}. p_W stays far below 3, the CL moment stays far below 1, and "
      f"the first moment stays at 1. Widening the window pushes p_delta(2nd) DOWN "
      f"({p2:.3f} -> {EXP_F['p_delta_2nd'][0]:.3f}), i.e. towards zero, not towards 1")

check(abs(p1 - 1.0) < 0.15,
      f"E1d *** THE ESCAPE DOOR *** the FIRST moment (2/pi)Int Delta rho/omega domega scales as "
      f"T^{p1:.4f} +/- {s1:.4f}, i.e. LINEARLY. So the no-go is specific to the 1/omega^2 Caldeira-Leggett "
      f"mass-shift moment: an inertia functional built on the first moment DOES carry an acceleration scale. "
      f"This door is quantified in F, and it does not go where the framework needs it to")

# E2  regulator scan: is the CL-moment r a number or an artefact?
print("\n  E2  regulator scan.  If c1 were a real limit, r would be delta-independent.")
rows = []
for mach, tag in ((MACH, "delta=2e-3"), (MACH_F, "delta=2e-4")):
    _, i2, i1 = sweep(mach, W0_CANON, QSQ, A_GRID)
    r2 = 2.0 / extract_q(A_GRID, i2)[2]
    r1 = 2.0 / extract_q(A_GRID, i1)[2]
    rows.append((tag, mach.delta, r2, r1))
    print(f"    {tag} (Omega = {1/mach.delta:6.0f} H):  r(CL 2nd moment) = {r2:10.4f}    r(1st moment) = {r1:.6f}")
check(abs(rows[1][2] / rows[0][2] - 1.0) > 0.8 and abs(rows[1][3] / rows[0][3] - 1.0) < 5e-3,
      f"E2 the CL-moment r moves by a factor {rows[1][2]/rows[0][2]:.2f} ({rows[0][2]:.2f} -> {rows[1][2]:.2f}) "
      f"when the UV bandwidth is raised ten-fold, i.e. it GROWS without bound and is a pure regulator artefact -- "
      f"confirming c1 -> 0, r -> infinity, q -> 0 and a_0 = 0. The first-moment r meanwhile is stable to "
      f"{100*abs(rows[1][3]/rows[0][3]-1):.3f}% ({rows[0][3]:.6f} vs {rows[1][3]:.6f}), so that one IS a number")

# E3  IR watch: the uncorrected code's delta_m ~ 1/omega_min is NOT reproduced
print("\n  E3  IR watch, both footings.  Item 5 records delta_m ~ 1/omega_min exactly (10.000x per decade) in the")
print("      UNCORRECTED code.  Exponent of I(a=100) and of delta_m(0) against 1/omega_0:")
w0s = np.logspace(-4.0, 0.0, 9)
Iw = np.array([MACH_F.moment(MACH_F.drho_a(100.0, QSQ), w) for w in w0s])
Dw = np.array([MACH_F.moment(MACH_F.rho_a(0.0, QSQ), w) for w in w0s])
eI = -np.diff(np.log(Iw)) / np.diff(np.log(w0s))
eD = -np.diff(np.log(Dw)) / np.diff(np.log(w0s))
print("      w0        :" + "".join(f"{w:11.2e}" for w in w0s))
print("      I(100)    :" + "".join(f"{v:11.3e}" for v in Iw))
print("      dlog/dlog :" + "".join(f"{v:11.3f}" for v in eI))
print("      dm(0) exp :" + "".join(f"{v:11.3f}" for v in eD))
_, i2c, i1c = sweep(MACH_F, W0_CANON, QSQ, A_GRID)
_, i2a, i1a = sweep(MACH_F, W0_ALT, QSQ, A_GRID)
r_can, r_alt = 2.0 / extract_q(A_GRID, i2c)[2], 2.0 / extract_q(A_GRID, i2a)[2]
r1_can, r1_alt = 2.0 / extract_q(A_GRID, i1c)[2], 2.0 / extract_q(A_GRID, i1a)[2]
print(f"      omega_0 canonical {W0_CANON:.6f}: r(CL) = {r_can:9.4f}, r(1st) = {r1_can:.6f}")
print(f"      omega_0 ALT       {W0_ALT:.6f}: r(CL) = {r_alt:9.4f}, r(1st) = {r1_alt:.6f}")
check(np.max(np.abs(eI)) < 0.5 and np.max(np.abs(eD)) < 0.5,
      f"E3 the corrected kernel does NOT reproduce the 1/omega_min divergence: the exponent of I against 1/omega_0 "
      f"peaks at {np.max(np.abs(eI)):.3f} and that of delta_m(0) at {np.max(np.abs(eD)):.3f}, both far from the 1.0 "
      f"that 10x-per-decade requires -- the dependence is logarithmic. Item 5's exact 1/omega_min was an artefact "
      f"of the uncorrected kernel, whose rho(omega -> 0) tended to a nonzero constant. Reported in both footings: "
      f"r(CL) = {r_can:.4f} canonical vs {r_alt:.4f} ALT, a {100*abs(r_alt/r_can-1):.2f}% spread, because omega_0 "
      f"is footing-invariant (check S1)")

# E4  coupling: r is defined only perturbatively
print("\n  E4  coupling scan.  r is q-independent only while the resolvent is perturbative.")
for q_sq in (1e-8, 1e-6, 1e-2, 1.0):
    _, i2q, i1q = sweep(MACH, W0_CANON, q_sq, A_GRID)
    cq = extract_q(A_GRID, i1q)
    print(f"    q^2 = {q_sq:7.0e}: max|q^2 Khat_0| = {np.max(np.abs(q_sq*MACH.Khat(0.0))):9.3e},  "
          f"r(1st) = {2/cq[2]:12.5f},  kappa = {cq[2]*Z/2:9.4f},  c1 drift = {cq[3]:.4f}")
r_lo = 2.0 / extract_q(A_GRID, sweep(MACH, W0_CANON, 1e-8, A_GRID)[2])[2]
r_mid = 2.0 / extract_q(A_GRID, sweep(MACH, W0_CANON, 1e-6, A_GRID)[2])[2]
r_hi = 2.0 / extract_q(A_GRID, sweep(MACH, W0_CANON, 1e-2, A_GRID)[2])[2]
check(abs(r_mid / r_lo - 1.0) < 1e-3 and abs(r_hi / r_lo - 1.0) > 0.5,
      f"E4 r is coupling-independent across q^2 = 1e-8 to 1e-6 ({r_lo:.5f} vs {r_mid:.5f}, {100*abs(r_mid/r_lo-1):.4f}%) "
      f"-- as the master formula's invariance under f -> alpha f demands, since both c1p and f'(T_GH) are O(q^2) -- "
      f"and it BREAKS once the resolvent stops being perturbative: r = {r_hi:.4f} at q^2 = 1e-2 (a "
      f"{100*abs(r_hi/r_lo-1):.0f}% move) and r = "
      f"{2.0/extract_q(A_GRID, sweep(MACH, W0_CANON, 1.0, A_GRID)[2])[2]:.4f} -- SIGN-FLIPPED -- at q^2 = 1. "
      f"So r exists only in the "
      f"perturbative window; the exact resolvent destroys it at strong coupling, which is a second, independent "
      f"limit on how much this mechanism can be asked to deliver")

# E5  grid refinement, 4x, with the shift shown
print("\n  E5  4x grid refinement (omega and nu):")
MACH_R = Machinery(DELTA, ETA, np.logspace(-3.0, math.log10(600.0), 4 * 420))
_, i2r, i1r = sweep(MACH_R, W0_CANON, QSQ, A_GRID)
r1_ref = 2.0 / extract_q(A_GRID, i1r)[2]
c2_ref = extract_q(A_GRID, i1r)[1]
print(f"    r(1st):  {2/extract_q(A_GRID, I1)[2]:.7f} (420 omega)  ->  {r1_ref:.7f} (1680 omega),  "
      f"shift {100*abs(r1_ref/(2/extract_q(A_GRID, I1)[2])-1):.5f}%")
check(abs(r1_ref / (2.0 / extract_q(A_GRID, I1)[2]) - 1.0) < 3e-3,
      f"E5 quadrupling the omega grid moves r(1st) by {100*abs(r1_ref/(2/extract_q(A_GRID,I1)[2])-1):.4f}%, so the "
      f"quoted digits are grid-converged and not an unsampled-extremum artefact (float64 hazard #4)")


# ============================================================================================================
banner("F  READING OFF r -- and what it says about the coefficient")
# ============================================================================================================
R_CL = [2.0 / extract_q(A_GRID, I2)[2], 2.0 / extract_q(A_GRID, I2_F)[2]]
R_1M = [2.0 / extract_q(A_GRID, I1)[2], 2.0 / extract_q(A_GRID, I1_F)[2], r1_ref]
R_FINAL = float(np.mean(R_1M))
R_SPREAD = float(np.max(R_1M) - np.min(R_1M))
Q_FINAL = 2.0 / R_FINAL
KAPPA_FINAL = Q_FINAL * Z / 2.0

print(f"  Caldeira-Leggett delta_m = (2/pi) Int rho/(w^2+w0^2) dw   [the moment tn14-tn26 use]")
print(f"    c1 = lim I/a is NOT a limit: r = {R_CL[0]:.2f} at Omega = {1/DELTA:.0f} H, {R_CL[1]:.2f} at "
      f"{1/MACH_F.delta:.0f} H, growing as the regulator is removed")
print(f"    => c1p = 0, r = infinity, q = 0, a_0 = 0.  NO ACCELERATION SCALE.")
print(f"\n  first moment (2/pi) Int rho/w dw   [the escape door]")
print(f"    r = {R_1M[0]:.6f} / {R_1M[1]:.6f} / {R_1M[2]:.6f}  (Omega = 500, 5000, and the 4x-refined grid)")
print(f"    r = {R_FINAL:.5f} +/- {R_SPREAD:.5f}   =>   q = {Q_FINAL:.5f}   =>   kappa = q Z/2 = {KAPPA_FINAL:.4f}")

print(f"\n  {'proposal':<40}{'r':>12}{'q':>12}{'kappa':>10}{'r/r_this':>11}")
print("  " + "-" * 85)
for nm, rv in (("THIS KERNEL, first moment", R_FINAL), ("Milgrom 1999 (a_0 = 2 c H_Lambda)", 1.0),
               ("Milgrom 1999 eqs 10-11", 2.0), ("Milgrom 2020 (kappa = 1/2pi)", 4.0 * math.pi),
               ("THIS FRAMEWORK (kappa = 1/2)", 2.0 * Z), ("admissibility bound (max)", R_ADMISSIBLE_MAX)):
    print(f"  {nm:<40}{rv:>12.6f}{2/rv:>12.6f}{(2/rv)*Z/2:>10.4f}{rv/R_FINAL:>11.3f}")

A0_IMP_CANON = Q_FINAL * CH_LAMBDA
A0_IMP_ALT = Q_FINAL * CH_0
print(f"\n  implied a_0, both footings:  canonical q c H_Lambda = {A0_IMP_CANON:.4e} m/s^2 "
      f"({A0_IMP_CANON/A0_CANON:.2f}x the fitted {A0_CANON:.4e})")
print(f"                               ALT       q c H_0       = {A0_IMP_ALT:.4e} m/s^2 "
      f"({A0_IMP_ALT/A0_ALT:.2f}x the fitted {A0_ALT:.4e})")
print(f"  kappa is footing-invariant: {KAPPA_FINAL:.4f} either way, i.e. {KAPPA_FINAL/0.5:.2f}x the fitted 1/2")

check(abs(A0_CANON / CH_LAMBDA - 1.0 / Z) < 1e-4 and abs(A0_ALT / CH_0 - 1.0 / Z) < 1e-3,
      f"F1 the bridge q = 2 kappa/Z is verified against the quoted constants: a_0/(cH) = "
      f"{A0_CANON/CH_LAMBDA:.7f} (canonical) and {A0_ALT/CH_0:.7f} (ALT) against 2(1/2)/Z = 1/Z = {1/Z:.7f}. "
      f"So kappa = q Z/2 is the correct translation and the same in both footings")
check(abs(math.log(R_FINAL / 1.0)) < abs(math.log(R_FINAL / (2.0 * Z))),
      f"F2 *** AGAINST INTEREST *** the r this mechanism actually delivers, {R_FINAL:.5f}, sits "
      f"{abs(math.log(R_FINAL/1.0)):.3f} in log from Milgrom 1999's r = 1 and {abs(math.log(R_FINAL/(2*Z))):.3f} "
      f"from the 2Z = {2*Z:.4f} that kappa = 1/2 requires -- i.e. {2*Z/R_FINAL:.1f}x away from this framework's "
      f"value and {1/R_FINAL:.2f}x from Milgrom's. Feeding the trajectory in lands in MILGROM'S neighbourhood, "
      f"not the framework's. Nothing here derives kappa = 1/2; the mechanism disfavours it by "
      f"{KAPPA_FINAL/0.5:.1f}x")
check(R_FINAL < R_ADMISSIBLE_MAX and R_FINAL < 1.0,
      f"F3 r = {R_FINAL:.5f} is inside the admissibility bound r <= {R_ADMISSIBLE_MAX} "
      f"(mi_r_admissibility_bound_2026.py) -- so the mu it implies is <= 1 and monotone -- but it is also BELOW 1, "
      f"meaning q = {Q_FINAL:.4f} > 2 and the implied a_0 = {A0_IMP_CANON:.3e} m/s^2 is LARGER than Milgrom 1999's "
      f"2 c H_Lambda = {2*CH_LAMBDA:.3e}. The mechanism overshoots the horizon scale, it does not divide it by Z")
check(R_SPREAD / R_FINAL < 0.01 and abs(R_CL[1] / R_CL[0] - 1.0) > 0.8,
      f"F4 the two verdicts have opposite robustness signatures, which is how we know which is real: r(1st moment) "
      f"= {R_FINAL:.5f} varies by {100*R_SPREAD/R_FINAL:.3f}% across a ten-fold change of UV bandwidth and a 4x "
      f"grid refinement, while r(CL moment) moves {100*abs(R_CL[1]/R_CL[0]-1):.0f}% under the same change. One is a "
      f"number; the other is the regulator")


# ============================================================================================================
banner("SUMMARY")
# ============================================================================================================
print(f"""  1. THE DEFECT IS REAL AND IS ONE LINE.  With qwen's acceleration-blind kernel I(a) = 0 identically over six
     decades of a/H (D4): delta_m cannot depend on acceleration, nu is a constant, no MOND for any coupling.
     tn15 already computed the Deser-Levin T_eff (line 194) and defined source_spectrum(omega, accel); the fix
     is to use them in the kernel, and A4 shows that this reproduces Re G_th(tau;T_eff(a)) to {worstA4:.1e} while
     the blind factor is off by {worstBLIND:.1e}.

  2. NO PICARD, NO THRESHOLD.  Under tn16's own K(0) = 0 convention the Volterra operator is strictly lower
     triangular, det = 1 for every coupling (B3), one forward sweep equals the dense LU solve to 2e-16 (B3b),
     and the algebraic resolvent phihat_BD/(1-q^2 Khat) agrees with it to 1e-9 at a coupling that dresses rho
     by {100*dev_ref[-1]:.0f}% (B2).  tn16's 'sign-flip threshold q^2 ~ 3e-2' and tn17's non-convergence warnings are artefacts
     of the method, not features of the physics: a unit-triangular operator has no pole.

  3. THE DEEP SIDE COMES OUT RIGHT, FOR FREE.  I ~ a^2 to 5 decimal places at a/H = 1e-3 (D2), and c2 from the
     numerical limit equals f'(T_GH)/(4 pi) from the analytic temperature derivative to
     {abs(c2_2*4*math.pi/FP2-1):.1e} (D1).

  4. THE NEWTONIAN SIDE DOES NOT.  I(a) never reaches an I ~ a regime: the local exponent crosses 1 near
     a/H ~ 3 and keeps falling, to {lg[-5]:.2f} by a/H ~ 100, and the fitted p_delta drops from {p2:.2f} to
     {EXP_F['p_delta_2nd'][0]:.2f} when the UV bandwidth is raised ten-fold (E1c, E1e).  So c1 = lim I/a = 0,
     r -> infinity, q -> 0, a_0 = 0.  The T^3 test fires independently: the gain-band weight scales as
     T^{pW:.2f} +/- {sW:.2f}, {(3-pW)/sW:.0f} fit sigma below 3 (E1).

  5. AGAINST THE T^3 TEST ITSELF.  The band does not track T (p_omega = 0.20, not 1), so 'exponent below 3'
     is not the correct form of the criterion here; the operative one is p_delta = 1.  Both fire, but they are
     not the same statement and the heuristic identity between them fails by a factor 2 (E1b).

  6. THE ONE OPEN DOOR, AND IT LEADS AWAY FROM kappa = 1/2.  The first moment Int rho/omega domega scales
     exactly as T (p = {p1:.2f} at Omega = 500 H, {EXP_F['p_delta_1st'][0]:.2f} at 5000 H), needs no IR regulator, and
     yields a genuine regulator-stable r = {R_FINAL:.5f} +/- {R_SPREAD:.5f} => q = {Q_FINAL:.4f} => kappa = {KAPPA_FINAL:.4f}.
     That is {KAPPA_FINAL/0.5:.1f}x the fitted kappa = 1/2 and a factor {2*Z/R_FINAL:.1f} from r = 2Z; it sits nearest Milgrom
     1999's r = 1 ({1/R_FINAL:.2f}x away).  The implied a_0 is {A0_IMP_CANON:.3e} m/s^2 (canonical) or {A0_IMP_ALT:.3e}
     (ALT), i.e. LARGER than the horizon rate rather than 1/Z of it.

  7. WHAT DID NOT REPRODUCE.  Item 5's 'delta_m ~ 1/omega_min exactly, 10.000x per decade' does NOT survive the
     corrected kernel: the dependence on the detector frequency is logarithmic, exponent <= 0.36 (E3).  That
     divergence belonged to the uncorrected kernel.

  8. FOOTINGS.  omega_0 = omega_c/H and q = a_0/(cH) are EXACTLY footing-invariant, because a_0 and cH both
     carry 1/sqrt(Omega_Lambda) = 1.2082.  r differs by 0.04% between canonical and ALT (E3).  This lane cannot
     be decided by the rho_DE/cH_Lambda vs rho_total/cH_0 fork in either direction.

  kappa = 1/2 REMAINS FITTED, NOT DERIVED.  This lane does not derive it and does not support it: the only
  reading of the trajectory-carrying kernel that produces an acceleration scale at all produces one {KAPPA_FINAL/0.5:.0f}x
  too large, in Milgrom's neighbourhood rather than this framework's.""")

banner("CHECKS")
npass = sum(1 for c, _ in OK if c)
for i, (c, m) in enumerate(OK, 1):
    print(f"  {i:2d}. [{'OK' if c else 'FAIL'}] {m.split(chr(32))[0]}")
print(f"\n{npass}/{len(OK)} checks held.")
if npass != len(OK):
    print("FAILURES:")
    for c, m in OK:
        if not c:
            print(f"  - {m}")
    sys.exit(1)
sys.exit(0)
