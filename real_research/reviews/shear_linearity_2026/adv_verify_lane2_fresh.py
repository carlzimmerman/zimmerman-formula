#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADVERSARIAL FRESH-SESSION VERIFICATION of lane2_gates.py (det-class four-gate table).
Independent METHODS on purpose: numeric random matrices (not sympy), finite differences
(not lambdified analytic derivatives), Gauss-Legendre tensor grid (not dblquad) for the
Q2 kernel. Also: the normalization-trap audit (deep-extrapolated eps_gal~2.8 vs the
self-consistent full-nu trajectory eps_bg~0.88 -- which one decides gate 2) and the
background-SHEAR-occupancy sensitivity of the tuned wall.
"""
import numpy as np

rng = np.random.default_rng(20260710)
c_l  = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
AU   = 1.495978707e11
Mpc  = 3.0857e22
Z    = np.sqrt(32*np.pi/3.0)
A0C  = 9.36e-11
A0A  = 1.13e-10
AMP_C = np.sqrt(Z/6.0)
AMP_A = np.sqrt((c_l*67.4e3/Mpc/6.0)/A0A)
r_sat = 9.5826*AU
g_sat = G*Msun/r_sat**2
EPM_DG = (A0C/2)/10**3.8
Q2_CEIL = 5.2e-27

print("="*96)
print(" [A] det(1+eps) ALGEBRA -- numeric random symmetric matrices (independent of sympy)")
print("="*96)
worst1 = worst2 = 0.0
for _ in range(200):
    M = rng.normal(size=(3,3)); E = 0.3*(M+M.T)/2
    J1 = np.trace(E); dev = E - (J1/3)*np.eye(3); J2 = np.sum(dev*dev)
    I1 = J1
    I2 = 0.5*(J1**2 - np.trace(E@E))
    I3 = np.linalg.det(E)
    d  = np.linalg.det(np.eye(3)+E)
    worst1 = max(worst1, abs(d - (1+I1+I2+I3)))
    worst2 = max(worst2, abs(I2 - (J1**2/3 - J2/2)))
print(f"  det(1+eps)=1+I1+I2+I3 : max |err| over 200 random eps = {worst1:.2e}")
print(f"  I2 = J1^2/3 - J2/2    : max |err|                     = {worst2:.2e}")
assert worst1 < 1e-12 and worst2 < 1e-12
# first-order shear-blindness at eps=0 AND at a purely VOLUMETRIC background:
for tag, bg in [("eps=0", np.zeros((3,3))), ("volumetric bg (0.3 I)", 0.1*np.eye(3)*3)]:
    worst = 0.0
    for _ in range(50):
        M = rng.normal(size=(3,3)); S = (M+M.T)/2; e = S - np.trace(S)/3*np.eye(3)  # traceless
        t = 1e-6
        d1 = (np.linalg.det(np.eye(3)+bg+t*e) - np.linalg.det(np.eye(3)+bg-t*e))/(2*t)
        worst = max(worst, abs(d1))
    print(f"  d det/dt along traceless directions at {tag:<22}: max = {worst:.2e}  (shear-BLIND)")
    assert worst < 1e-8
# at an ANISOTROPIC background the coupling is NOT zero and the 2nd-order cross coefficient
# of (e_bg : e_sun) in det is exactly -1 (the I2 cross term -> -F'(J)*(e_bg:e_sun) coupling):
coefs = []
for _ in range(50):
    M = rng.normal(size=(3,3)); S=(M+M.T)/2; ebg = 1e-4*(S - np.trace(S)/3*np.eye(3))
    M = rng.normal(size=(3,3)); S=(M+M.T)/2; esn = (S - np.trace(S)/3*np.eye(3))
    t = 1e-6
    d1 = (np.linalg.det(np.eye(3)+ebg+t*esn) - np.linalg.det(np.eye(3)+ebg-t*esn))/(2*t)
    coefs.append(d1/np.sum(ebg*esn))
print(f"  cross coefficient d det/d e_sun / (e_bg:e_sun) at small ANISOTROPIC e_bg: "
      f"{np.mean(coefs):+.6f} (expect -1)")
assert abs(np.mean(coefs) + 1) < 1e-3
print("  => the F-sector shear coupling exists ONLY through the background's SHEAR part e_bg;")
print("     a purely volumetric background is shear-blind to ALL orders. [lane-1 basis confirmed]")

print("\n" + "="*96)
print(" [B] STRAIN TRAJECTORY: monotonicity, saturation, tail threshold, double-valued exhibit")
print("="*96)
def eps_req(y, amp): return 2.0*amp*(np.sqrt(y*y+y) - y)
# cancellation-free identity: sqrt(y^2+y)-y = 1/(sqrt(1+1/y)+1)*1... derive: y(sqrt(1+1/y)-1)
#   = y*(1/y)/(sqrt(1+1/y)+1) = 1/(sqrt(1+1/y)+1)  => eps = 2A/(sqrt(1+1/y)+1), manifestly increasing.
def eps_stable(y, amp): return 2.0*amp/(np.sqrt(1.0+1.0/y)+1.0)
y = np.logspace(-8, 8, 400001)
agree = np.max(np.abs(eps_req(y[y<1e6],AMP_C)/eps_stable(y[y<1e6],AMP_C) - 1))
e = eps_stable(y, AMP_C)
assert np.all(np.diff(e) > 0), "eps not strictly increasing!"
print(f"  stable form eps=2A/(sqrt(1+1/y)+1) agrees with naive to {agree:.1e} (y<1e6);")
print(f"  eps strictly increasing on y=1e-8..1e8 [400k grid]  eps(1e8)={e[-1]:.5f} -> eps_inf={AMP_C:.5f}")
h = 1e-6
dln = (np.log(eps_req(10*np.exp(h),1.0)) - np.log(eps_req(10*np.exp(-h),1.0)))/(2*h)
print(f"  d ln eps/d ln y |_(y=10) = {dln:.5f}  (lane 2 claims 0.0233; ANY tail n > this de-monotonizes eps)")
assert abs(dln - 0.0233) < 5e-4
def eps_tail(yv, n, yc=10.0):
    ev = eps_req(yv, AMP_C)
    return np.where(yv > yc, ev*(yc/yv)**n, ev)
from scipy import optimize
tgt = eps_tail(np.array([2.0]), 0.82)[0]
y2 = optimize.brentq(lambda yy: eps_tail(np.array([yy]),0.82)[0]-tgt, 10.0000001, 1e6)
print(f"  EXHIBIT reproduced: eps(2)=eps({y2:.2f})={tgt:.4f}, budget ratio b(y2)/b(2)={y2/2:.2f}")
assert abs(tgt-0.8830) < 5e-4 and abs(y2/2 - 5.54) < 0.05
print("  => same det, two stored energies: NO single-valued F(det) realizes the n=0.82 tail. CONFIRMED")

print("\n" + "="*96)
print(" [C] F' AND F'' POSITIVITY by pure finite differences on the parametric (J(y), b(y))")
print("="*96)
yg = np.logspace(-8, 6, 3001)
Jg = (1 + eps_stable(yg, AMP_C)/3.0)**3
bg = 2*AMP_C**2*yg
Fp_num = np.gradient(bg, Jg)       # dF/dJ along the trajectory (ok at moderate y only)
# OWN analytic derivation (fresh): b'=2A^2; with q=sqrt(1+1/y): eps=2A/(q+1),
#   eps' = A/(q y^2 (q+1)^2);  J' = (1+eps/3)^2 eps'
#   => F'(y) = b'/J' = 2A q y^2 (q+1)^2 / (1+eps/3)^2
def Fp_ana(yv):
    q = np.sqrt(1.0+1.0/yv); ee = 2*AMP_C/(q+1)
    return 2*AMP_C*q*yv**2*(q+1)**2/(1+ee/3)**2
mid = (yg>1e-6)&(yg<1e2)
agree_fp = np.max(np.abs(Fp_num[mid][2:-2]/Fp_ana(yg[mid][2:-2]) - 1))
print(f"  analytic F'(y) vs numeric b'/J' gradient (y=1e-6..1e2): max rel dev {agree_fp:.1e}")
assert agree_fp < 1e-2
print(f"  F' min over y=1e-8..1e6 : {Fp_ana(yg).min():.3e}   (lane 2: 2e-4, monotone) -> F' > 0 EVERYWHERE")
# F'' = (dF'/dy)/(dJ/dy), well-conditioned central difference of the ANALYTIC F' in ln y:
h = 1e-6
def Fpp_ana(yv):
    q = np.sqrt(1.0+1.0/yv); ee = 2*AMP_C/(q+1)
    Jp = (1+ee/3)**2 * AMP_C/(q*yv**2*(q+1)**2)
    dFp = (Fp_ana(yv*np.exp(h)) - Fp_ana(yv*np.exp(-h)))/(2*h*yv)
    return dFp/Jp
Fpp = Fpp_ana(yg)
print(f"  F'' min over y=1e-8..1e6 : {Fpp.min():.3e}   (lane 2: >=1.0, convex) -> F'' > 0 EVERYWHERE")
print(f"  F''(J->1) = {Fpp_ana(np.array([1e-10]))[0]:.4f}  (kappa=1 check, expect ->1)")
assert Fp_ana(yg).min() > 0 and Fpp.min() > 0.5 and abs(Fpp_ana(np.array([1e-10]))[0]-1) < 1e-3
# deep-limit budget identity: eps_lin = 2A sqrt(y)  =>  eps_lin^2/2 = 2A^2 y = b EXACT
ycheck = 1e-6
assert abs((2*AMP_C*np.sqrt(ycheck))**2/2 - 2*AMP_C**2*ycheck) < 1e-20
print("  deep-limit b = eps_lin^2/2 identity: EXACT. Monotone-CONVEX hard wall CONFIRMED independently.")

print("\n" + "="*96)
print(" [D] Q2 KERNEL spot re-derivation -- Gauss-Legendre tensor grid (NOT dblquad)")
print("="*96)
def q_gl(nu1, etilde, vmax=60.0, Nv=4000, Nx=200):
    eN = optimize.brentq(lambda ee: (1.0+nu1(ee))*ee - etilde, 1e-9, etilde+5)
    xv, wv = np.polynomial.legendre.leggauss(Nx)          # xi in [-1,1]
    # v in [0, vmax] split log-ish: use substitution v = vmax*u^2 to resolve v->0
    uu, wu = np.polynomial.legendre.leggauss(Nv)
    u = (uu+1)/2; w_u = wu/2
    v = vmax*u**2; dv = vmax*2*u*w_u
    V, XI = np.meshgrid(v, xv, indexing='ij')
    WW = np.outer(dv, wv)
    D = eN**2 + V**4 + 2*eN*V**2*XI
    D = np.maximum(D, 0.0)
    ig = nu1(np.sqrt(np.maximum(D,1e-300)))*(eN*(3*XI-5*XI**3) + V**2*(1-3*XI**2))
    ig[D <= 0] = 0.0
    return 1.5*np.sum(ig*WW)
nu1_simple = lambda yv: (np.sqrt(1.0+4.0/np.maximum(yv,1e-12))-1.0)/2.0
nu1_fwm    = lambda yv: np.sqrt(1.0+1.0/np.maximum(yv,1e-300)) - 1.0
ratios = [abs(q_gl(nu1_simple, et))/anc for et, anc in ((1.0,0.094),(1.5,0.159),(2.0,0.221))]
CAL = 1.0/np.mean(ratios)
print(f"  Desmond-anchor calibration (independent integrator): CAL = {CAL:.4f}  (lane 2: 1.0334)")
vals = {}
for tag, a0 in (("canon", A0C), ("alt", A0A)):
    v3 = [CAL*abs((3.0*a0**1.5)/(2.0*np.sqrt(G*Msun))*q_gl(nu1_fwm, et)) for et in (1.9,2.2,2.6)]
    vals[tag] = (min(v3), max(v3))
    print(f"  scalar-class Q2 ({tag:5s}) over g_ext 1.9/2.2/2.6 a0: {min(v3):.3e} .. {max(v3):.3e} s^-2"
          f"   (lane 2: {'1.95-2.50e-26' if tag=='canon' else '2.59-3.31e-26'})")
wmax_c = Q2_CEIL/vals['canon'][1]; wmax_a = Q2_CEIL/vals['alt'][1]
print(f"  => w_max(worst corner): canonical {wmax_c:.3f} (lane 2: 0.208) | alt {wmax_a:.3f} (lane 2: 0.157)")
assert abs(CAL-1.0334) < 0.02 and abs(wmax_c-0.208) < 0.02 and abs(wmax_a-0.157) < 0.02

print("\n" + "="*96)
print(" [E] NORMALIZATION TRAP AUDIT: which eps_bg convention -- and does it decide gate 2?")
print("="*96)
# chain: g_D = (a0/2)*eps DEFINES eps; the boost must reproduce the framework nu at every y:
#   g_D = g_bar*(nu_member-1) = a0*AMP*y*(nu-1)  =>  eps(y) = 2*AMP*y*(nu(y)-1) = 2A(sqrt(y^2+y)-y)
# deep limit: eps -> 2A sqrt(y)  =>  g_D -> A*sqrt(a0*g_bar) = sqrt((Z/6)*a0*g_bar) = sqrt(a0_V*g_bar/6)
gD_deep = AMP_C*np.sqrt(A0C*0.01*A0C)   # y=0.01
tgt_deep = np.sqrt((Z*A0C)*0.01*A0C/6)
print(f"  displacement-law anchor: g_D(deep, y=0.01) member {gD_deep:.4e} vs required {tgt_deep:.4e}"
      f"  [ratio {gD_deep/tgt_deep:.6f}]")
assert abs(gD_deep/tgt_deep - 1) < 1e-12
for yv in (1.9, 2.2, 2.6):
    e_full = eps_req(yv, AMP_C)
    e_deepx = 2*AMP_C*np.sqrt(yv)          # the laneC 'eps_gal ~ 2.8' deep-extrapolation
    print(f"  y={yv}: full-nu trajectory eps_bg = {e_full:.4f} | deep-law EXTRAPOLATION = {e_deepx:.4f}"
          f"  (x{e_deepx/e_full:.2f})")
# which is self-consistent? the boost the deep-extrapolation implies at the Sun:
yv = 2.2
print(f"  boost at y=2.2 implied: full-nu {eps_req(yv,AMP_C)/(2*yv):.4f} vs framework nu-1 = "
      f"{np.sqrt(1+1/yv)-1:.4f} (MATCH) ; deep-extrap {2*AMP_C*np.sqrt(yv)/(2*yv):.4f} (x3.2 OVER-boost:")
print("  would CONTRADICT the framework's own rotation-curve nu at the solar circle).")
print("  => eps_bg ~ 0.88 (full-nu) is the ONLY self-consistent choice; eps_gal~2.8 in laneC is a")
print("     deep-law estimate. Had lane 2 used 2.8, eps_bg > eps_inf=0.982 and Saturn would be")
print("     TRIVIALLY screened (manufactured PASS). Lane 2 did NOT take that route.  AUDIT: CLEAN.")
# Saturn arithmetic, natural wall, by hand:
y_s = g_sat/A0C
dg_nat = (A0C/2)*(eps_req(y_s,AMP_C) - eps_req(1.9,AMP_C))
print(f"  Saturn natural-wall check: y_sat={y_s:.3e}, dg = {dg_nat:.3e} m/s^2 = {dg_nat/EPM_DG:.0f}x EPM"
      f" ({np.log10(dg_nat/EPM_DG):.2f} orders)   [lane 2: 653x, 2.8 orders]")
assert abs(dg_nat/EPM_DG - 653) < 15
# stricter EPM alternative (laneA's DG_BOUND = G*M_PP/r^2):
DGB = G*(7.9e-11*Msun)/r_sat**2
print(f"  bound-provenance fork: EPM_DG(banked 10^3.8)={EPM_DG:.2e} vs G*M_PP/r^2={DGB:.2e}"
      f" -> natural wall {dg_nat/DGB:.0f}x under the stricter form (verdict unchanged, 2.8->3.0 orders)")

print("\n" + "="*96)
print(" [F] BACKGROUND-SHEAR OCCUPANCY: was e_bg's shear part ignored, and which way does it cut?")
print("="*96)
# lane 2 credited 100% of the background budget to the BULK channel (eps_bg = eps_req(g_ext)).
# If a fraction f of the background strain ENERGY is shear (it must be >0 for a directional
# field; lane-1's w is precisely its anharmonic echo), bulk occupancy shrinks: b_bulk=(1-f)b.
for f in (0.0, 0.05, 0.2):
    b_bg = 2*AMP_C**2*1.9*(1-f)
    # invert the parametric budget to the bulk strain: b(y')=2A^2 y' -> y'=y(1-f); eps_bulk:
    e_bulk = eps_req(1.9*(1-f), AMP_C)
    print(f"  f_shear={f:>4}: bulk-channel eps_bg = {e_bulk:.4f}  -> tuned-wall ceiling eps_wall <= {e_bulk:.4f}")
print("  => ignoring the background SHEAR part is CHARITABLE to the wall: any f>0 pushes the")
print("     required wall LOWER (0.879 -> 0.85 at f=0.2), i.e. MORE knife-edge tuning, never less.")
print("     It cannot un-fail the natural wall (that gap is 0.10 in strain, ~650x in dg).")
print("     SPARC stays alive down to wall 0.85 (lane-2 scan), so the CONDITIONAL verdict holds,")
print("     with the tuning margin tighter than quoted.")

print("\nALL FRESH CHECKS PASSED -- EXIT 0")
