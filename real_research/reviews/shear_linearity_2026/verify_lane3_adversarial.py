#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADVERSARIAL VERIFICATION of lane 3 (P6 tail from det-class + falsifiers).
Fresh session, independent re-derivations. Focus points (per the audit brief):
  [V1] THE KERNEL FORK: lane 3's q_integral divides by sqrt(D); the banked corrected kernel
       (decider_q2_crosscheck.py, validated on Desmond+2024 anchors) does NOT. Decide which
       reproduces the published anchors q(1)=.094, q(1.5)=.159, q(2)=.221 (nu_simple), then
       recompute lane 3's Q2/w_max with the ANCHOR-VALIDATED kernel and compare.
  [V2] det-class exact algebra, fresh: det(1+E) = 1+I1+I2+I3; I2 = J1^2/3 - J2/2;
       first-order det-derivative in a shear direction about ISOTROPIC pre-strain = 0;
       about a SHEARED pre-strain it is NONZERO (the e_bg term lane 1's w carries) --
       check lane 3's wording matches the algebra.
  [V3] eps_M mapping fresh from Verlinde's S_M, S_DE; y_c both footings; is 'footing-
       invariant' genuine or definitional?
  [V4] Independent recompute of the gate numbers: Saturn throttle M_eff, n_min, CAP,
       GW margins. (Hand-derived first, asserted here.)
  [V5] The throttle-increases-|Q2| 'honest surprise': check it holds on the anchor-
       validated kernel too (sign structure of the integrand).
"""
import numpy as np, sympy as sp
from scipy import integrate, optimize

c_l  = 2.99792458e8; G = 6.674e-11; Msun = 1.989e30; AU = 1.495978707e11
Mpc  = 3.0857e22
Z        = np.sqrt(32*np.pi/3.0)
A0_CANON = 9.36e-11; A0_ALT = 1.13e-10
cH_Lam   = Z*A0_CANON; H0 = 67.4e3/Mpc; cH0 = c_l*H0
Q2_CEIL  = 1.6e-27 + 2*1.8e-27
yc_can, yc_alt = cH_Lam/(2*A0_CANON), cH0/(2*A0_ALT)
nu_fw = lambda y: np.sqrt(1.0 + 1.0/np.maximum(y, 1e-15))
print("="*96)
print(" [V1] KERNEL FORK: with vs without /sqrt(D), against Desmond+2024 published anchors")
print("="*96)
nu1_simple = lambda y:(np.sqrt(1.0+4.0/np.maximum(y,1e-12))-1.0)/2.0
def q_kernel(nu1, etilde, withD, vmax=60.0):
    eN = optimize.brentq(lambda e:(1.0+nu1(e))*e-etilde, 1e-9, etilde+5)
    def ig(xi, v):
        D = eN*eN + v**4 + 2*eN*v*v*xi
        if D <= 0: return 0.0
        base = nu1(np.sqrt(D))*(eN*(3*xi-5*xi**3) + v*v*(1-3*xi*xi))
        return base/np.sqrt(D) if withD else base
    val,_ = integrate.dblquad(ig, 0.0, vmax, lambda v:-1.0, lambda v:1.0,
                              epsabs=1e-10, epsrel=1e-8)
    return 1.5*val
print(f"  {'etilde':>8}{'anchor':>9}{'|q| noD':>10}{'ratio':>8}{'|q| withD':>11}{'ratio':>8}")
r_noD, r_wD = [], []
for et, anchor in ((1.0,0.094),(1.5,0.159),(2.0,0.221)):
    qn = abs(q_kernel(nu1_simple, et, False)); qd = abs(q_kernel(nu1_simple, et, True))
    r_noD.append(qn/anchor); r_wD.append(qd/anchor)
    print(f"  {et:>8.1f}{anchor:>9.3f}{qn:>10.4f}{qn/anchor:>8.3f}{qd:>11.4f}{qd/anchor:>8.3f}")
CAL = 1.0/np.mean(r_noD)
print(f"  no-/sqrt(D) ratios {min(r_noD):.3f}-{max(r_noD):.3f} (consistent, CAL={CAL:.4f});"
      f"  with-/sqrt(D) ratios {min(r_wD):.3f}-{max(r_wD):.3f}")
noD_ok = max(abs(r-1) for r in r_noD) < 0.06
wD_ok  = max(abs(r-1) for r in r_wD) < 0.06
print(f"  => ANCHOR-VALIDATED kernel: {'no-/sqrt(D)' if noD_ok and not wD_ok else 'with-/sqrt(D)' if wD_ok and not noD_ok else 'AMBIGUOUS'}")

# recompute lane-3's A4 table with BOTH kernels (framework nu, throttle), lane-3's physical g_ext grid
def Q2_of(a0v, gext, numo, withD, ycv=None):
    et = gext/a0v
    # lane 3 used the closed-form eN for fw-nu: eN^2+eN=et^2 -- same as brentq with nu_fw; keep brentq w/ fw
    eN = optimize.brentq(lambda e:(1.0+(nu_fw(e)-1.0))*e-et, 1e-9, et+5)
    def ig(xi, v):
        D = eN*eN + v**4 + 2*eN*v*v*xi
        if D <= 0: return 0.0
        Y = np.sqrt(D)
        f = numo(Y) if ycv is None else numo(Y)*min(1.0, ycv/Y)
        base = f*(eN*(3*xi-5*xi**3) + v*v*(1-3*xi*xi))
        return base/Y if withD else base
    val,_ = integrate.dblquad(ig, 0.0, 60.0, lambda v:-1.0, lambda v:1.0, epsabs=1e-9, epsrel=1e-7)
    q = 1.5*val
    return abs((3.0*a0v**1.5)/(2.0*np.sqrt(G*Msun))*q)
F1 = lambda Y: nu_fw(Y)-1.0
print(f"\n  Recompute of lane-3 A4 (fw-nu), BOTH kernels, CAL applied to the validated one:")
print(f"  {'footing':<10}{'g_ext':>9}{'lane3(withD)':>14}{'validated noD*CAL':>19}{'ratio':>8}"
      f"{'  same, throttled':>18}{'thr/unthr':>11}")
worst = {}
for a0v, ycv, tag in [(A0_CANON, yc_can, "canonical"), (A0_ALT, yc_alt, "alt")]:
    wf, wt = 0.0, 0.0
    for gext in (1.9e-10, 2.32e-10, 2.6e-10):
        Q_l3   = Q2_of(a0v, gext, F1, True)
        Q_val  = CAL*Q2_of(a0v, gext, F1, False)
        Q_valT = CAL*Q2_of(a0v, gext, F1, False, ycv=ycv)
        wf, wt = max(wf, Q_val), max(wt, Q_valT)
        print(f"  {tag:<10}{gext:>9.2e}{Q_l3:>14.3e}{Q_val:>19.3e}{Q_l3/Q_val:>8.3f}"
              f"{Q_valT:>18.3e}{Q_valT/Q_val:>11.3f}")
    worst[tag] = (wf, wt)
print(f"\n  w_max on the VALIDATED kernel (worst corner): canonical {Q2_CEIL/worst['canonical'][0]:.3f}"
      f" (fw) -> {Q2_CEIL/worst['canonical'][1]:.3f} (throttled);"
      f" alt {Q2_CEIL/worst['alt'][0]:.3f} -> {Q2_CEIL/worst['alt'][1]:.3f}")
print(f"  lane 3 claimed: canonical 0.248 -> 0.246, alt 0.172 -> 0.172 (worst corner g_ext=1.9e-10)")

print("\n" + "="*96)
print(" [V2] det-CLASS ALGEBRA FRESH (incl. the sheared-background check lane 1's w lives on)")
print("="*96)
a,b,c2,d,e,f = sp.symbols('a b c2 d e f', real=True)
E = sp.Matrix([[a,d,e],[d,b,f],[e,f,c2]])
I  = sp.eye(3)
J1 = sp.trace(E); Edev = E - (J1/3)*I; J2 = sp.trace(Edev*Edev)
I1 = J1; I2 = sp.Rational(1,2)*(J1**2 - sp.trace(E*E)); I3 = sp.det(E)
assert sp.simplify(sp.det(I+E) - (1+I1+I2+I3)) == 0
assert sp.simplify(I2 - (J1**2/3 - J2/2)) == 0          # the cross-term coefficient claim
res = sp.expand(sp.det(I+E) - (1 + J1 + J1**2/3 - J2/2))
p = sp.Poly(res, a,b,c2,d,e,f); assert min(sum(m) for m in p.monoms()) == 3
print("  det(1+E)=1+I1+I2+I3 EXACT; I2 = J1^2/3 - J2/2 EXACT (so det ~ 1+J1+J1^2/3-J2/2+O(3));")
print("  shear enters volume at 2nd order. AGREES with lane 3.")
t, eps0, s0 = sp.symbols('t epsilon0 s0', real=True)
sh_probe = sp.Matrix([[0,1,0],[1,0,0],[0,0,0]])          # a DIFFERENT shear direction than lane 3 used
d_iso = sp.diff(sp.det(I + eps0*I + t*sh_probe), t).subs(t,0)
assert sp.simplify(d_iso) == 0
e_bg = sp.Matrix([[1,0,0],[0,-sp.Rational(1,2),0],[0,0,-sp.Rational(1,2)]])*s0   # axisymmetric bg shear
probe_par = sp.Matrix([[1,0,0],[0,-1,0],[0,0,0]])
d_shbg = sp.simplify(sp.diff(sp.det(I + eps0*I + s0*e_bg/s0*s0 + t*probe_par), t).subs(t,0))
d_shbg = sp.expand(d_shbg)
print(f"  1st-order det-derivative, shear probe about ISOTROPIC pre-strain: 0 EXACTLY (re-verified,")
print(f"  independent probe direction). About a SHEARED background (axisym e_bg, amp s0):")
print(f"    d/dt det = {d_shbg}   -> NONZERO, O(s0) leading term")
assert d_shbg != 0
lead = sp.Poly(d_shbg, s0).coeff_monomial(s0)
print(f"    leading coefficient in s0: {lead} -> the -F'(e_bg:e_probe)-type term lane 3 names.")
print("  => lane 3's wording is CORRECT: shear-blindness holds only about isotropic pre-strain;")
print("     the galactic e_bg term exists and is exactly what lane-1's w must carry. Lane 3 does")
print("     NOT ignore e_bg -- it defers w to lane 1 and only uses |directional| <= w x AQUAL,")
print("     which is w's DEFINITION (bookkeeping, not a smallness claim).")

print("\n" + "="*96)
print(" [V3] eps_M MAPPING FRESH + footing-invariance audit")
print("="*96)
r_,M_,L_,G_,c_,hb_ = sp.symbols('r M L G c hbar', positive=True)
S_M  = 2*sp.pi*M_*c_*r_/hb_                      # Verlinde 1611.02269 (5.32)-(5.34) form
S_DE = (r_/L_)*(4*sp.pi*r_**2)*c_**3/(4*G_*hb_)  # his volume-law DE entropy
ratio = sp.simplify(S_M/S_DE)
gbar = G_*M_/r_**2
assert sp.simplify(ratio - 2*gbar*L_/c_**2) == 0
print(f"  |S_M|/S_DE = {ratio} = 2 g_bar/(cH)  [L=c/H]  -- re-derived, matches lane 3.")
print(f"  Sigma-criterion cross-check: point mass Sigma(r)=M/(4 pi r^2) < a0V/(8 pi G)")
print(f"    <=> GM/r^2 < a0V/2 <=> eps_M < 1: same crossover. Verlinde eq (1.3) consistent.")
print(f"  y_c canonical = cH_Lam/(2 a0) = {yc_can:.4f} = Z/2 = {Z/2:.4f}")
print(f"  y_c alt       = cH0/(2 a0_alt) = {yc_alt:.4f}")
print(f"  FOOTING-INVARIANCE: genuine but DEFINITIONAL -- both footings define a0 = a0_V/Z, so")
print(f"  y_c = a0_V/(2 a0) = Z/2 by construction; alt differs only via rounding of 1.13e-10.")
print(f"  It is NOT an independent coincidence; it IS parameter-free given the framework's a0 defs.")
print(f"  Sun environment: g_ext 1.9-2.6e-10 -> eps_M = 2y/Z: "
      f"can {2*(1.9e-10/A0_CANON)/Z:.2f}-{2*(2.6e-10/A0_CANON)/Z:.2f}, "
      f"alt {2*(1.9e-10/A0_ALT)/(cH0/A0_ALT):.2f}-{2*(2.6e-10/A0_ALT)/(cH0/A0_ALT):.2f} of budget.")

print("\n" + "="*96)
print(" [V4] GATE NUMBERS, INDEPENDENT RECOMPUTE")
print("="*96)
r_sat = 9.5826*AU; g_sat = G*Msun/r_sat**2
M_S_BOUND = 7.9e-11*Msun
for a0v, ycv, tag, Mclaim, nclaim in [(A0_CANON, yc_can, "canonical", 3.04e-12, 0.737),
                                      (A0_ALT,  yc_alt, "alt",       4.43e-12, 0.764)]:
    y_s = g_sat/a0v
    Meff = (nu_fw(y_s)-1.0)*(ycv/y_s)          # in Msun
    nmin = np.log(((nu_fw(y_s)-1.0))/ (M_S_BOUND/Msun))/np.log(y_s/ycv)
    print(f"  {tag}: y_sat={y_s:.4e}  M_eff(throttle)={Meff:.3e} Msun (claim {Mclaim:.2e}; "
          f"ratio {Meff/Mclaim:.3f})  = {Meff/(M_S_BOUND/Msun):.4f}x strict ({1/(Meff/(M_S_BOUND/Msun)):.1f}x under)")
    print(f"             n_min={nmin:.4f} (claim {nclaim})")
    assert abs(Meff/Mclaim - 1) < 0.02 and abs(nmin - nclaim) < 0.005
gcap = cH_Lam/2; Mcap = r_sat**2*cH_Lam/(2*G)/Msun
print(f"  CAP canonical: g_D={gcap:.2e} m/s2, M_cap(Sat)={Mcap:.2e} Msun = "
      f"{Mcap/(M_S_BOUND/Msun):.1e}x strict ({np.log10(Mcap/(M_S_BOUND/Msun)):.1f} orders) -- DEAD confirmed")
H_L = cH_Lam/c_l; Lam = 3*H_L**2/c_l**2; k100 = 2*np.pi*100/c_l
dc2 = 4*Lam/k100**2
print(f"  GW: dc^2/c^2 (canonical, 100 Hz) = {dc2:.2e} (claim 9.9e-41); margin 10^"
      f"{np.log10(4.5e-16/(dc2/2)):.1f} vs GW170817 (claim ~25.0)")
assert abs(dc2/9.9e-41 - 1) < 0.05

print("\n" + "="*96)
print(" [V5] LEGENDRE COEFFS FRESH")
print("="*96)
lam, cc, s_ = sp.symbols('lambda x s', positive=True)
f2 = sp.series((1 + 2*lam*cc + lam**2)**(s_/2), lam, 0, 3).removeO()
a1 = sp.simplify(sp.Rational(3,2)*sp.integrate(sp.expand(f2)*cc, (cc,-1,1)))
a2 = sp.simplify(sp.Rational(5,2)*sp.integrate(sp.expand(f2)*(3*cc**2-1)/2, (cc,-1,1)))
assert sp.simplify(a1 - s_*lam) == 0 and sp.simplify(a2 - s_*(s_-2)/3*lam**2) == 0
print(f"  a1 = s*lam, a2 = s(s-2)/3 lam^2 -- re-derived exactly, matches lane 3 (hand-check also done).")
print("\nALL ADVERSARIAL CHECKS RUN. EXIT 0")
