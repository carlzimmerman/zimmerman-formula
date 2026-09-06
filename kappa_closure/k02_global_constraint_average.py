#!/usr/bin/env python3
"""
k02 -- a global constraint of the sequestering type: is <L_scalar> over spacetime anywhere near rho_Lambda?
=======================================================================================================
The one class of principle that removes an additive zero mode without choosing a constant is a GLOBAL constraint
(vacuum-energy sequestering, Kaloper & Padilla 2014; unimodular-plus-average variants): Lambda becomes a Lagrange multiplier
fixed by the spacetime average of the field Lagrangians.  In the candidate action the only sector whose scale is a0^2 is the
MOND scalar, so such a constraint would give rho_Lambda = eta <L_phi>, eta = O(1) (1/4 in the sequestering trace form).
This script computes <L_phi> honestly and compares it with the target rho_Lambda c^2 = 4 a0^2 / G (kappa = 1/2).

On shell and curl-free (the static law J_Y grad phi = grad Psi), the scalar's Lagrangian density is pointwise
    L_phi = (2-K_B) [2 grad Psi . grad phi - J(Y)] / (16 pi G) = (2-K_B) a0^2 F(s) / (16 pi G),   F(s) = 2 s Delta(s) - j(s),
j(s) = J/a0^2 = 2 int_0^s s' dDelta (k01), Delta the carried kernel (nu_RAR saturated at s = 2.540).  Deep MOND: F -> (4/3) s^{3/2}.

Cosmic model: the diffuse peculiar acceleration field is the volume-dominant source (halo interiors fill ~1e-8-1e-6 of the
volume); |g_pec| is Maxwellian with rms sigma_g(a) = sigma_g0 D(a)/a^2 (linear theory, physical gradient of a frozen comoving
potential), sigma_g0 = (3 Omega_m H0 / (2 f0)) v_rms with v_rms = 300-600 km/s (smoothed / unsmoothed brackets).  The spacetime
average up to cosmic time T is <L>(T) = int a^3 L dt / int a^3 dt.  A halo term is added at 100x its real filling factor
(f = 1e-4 at s = 3) to show it cannot matter.

  G1 [identity]  F(s) -> (4/3) s^{3/2} in deep MOND and F(s) = 2 s Delta_sat - j_sat + 2 (s - s_sat) Delta_sat beyond saturation;
  G2 [today]     <L_phi>(t0) / rho_Lambda >= 0.5 for some v_rms in [300, 600] km/s, K_B in [0, 0.25], either footing;
  G3 [future]    the spacetime average converges to a nonzero fraction of rho_Lambda (it must, for a global constraint to mean anything);
  G4 [regime]    the acceleration s_* at which L_phi alone equals rho_Lambda: the universe's volume-averaged |g| would have to be s_* a0.
FAIL marks a requirement the route does not meet.
"""
import numpy as np, math, json, sys
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
G = 6.674e-11; c = 2.998e8; MPC = 3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; KAPPA = {f: a/(2*9.3619e-11) for f, a in A0.items()}
H0 = 67.4e3/MPC; OM = 0.315; OL = 1 - OM
print("=" * 118); print("k02 -- global-constraint (sequestering-type) average of the MOND scalar's Lagrangian vs rho_Lambda"); print("=" * 118)
# ---- kernel ----
Delta = lambda s: s/np.expm1(np.sqrt(s)) if s > 0 else 0.0
opt = minimize_scalar(lambda s: -Delta(s), bounds=(0.5, 6), method='bounded'); s_sat, D_sat = opt.x, -opt.fun
def j_of(s):
    if s <= s_sat: return 2*(s*Delta(s) - quad(Delta, 0, s)[0])
    return 2*(s_sat*D_sat - quad(Delta, 0, s_sat)[0])                       # Delta constant beyond saturation: no further dDelta
def F_of(s): return 2*s*(Delta(s) if s <= s_sat else D_sat) - j_of(s)
deep_ok = all(abs(F_of(s)/((4/3)*s**1.5) - 1) < 0.03 for s in (1e-4, 1e-3))
sat_ok = abs(F_of(5) - (2*5*D_sat - j_of(s_sat))) < 1e-9
print(f"    kernel: s_sat = {s_sat:.3f}, Delta_sat = {D_sat:.4f}, j_sat = {j_of(s_sat):.4f}; F(1e-3)/(4/3 s^1.5) = {F_of(1e-3)/((4/3)*1e-3**1.5):.4f}; F(1) = {F_of(1):.4f}, F(3) = {F_of(3):.4f}, F(10) = {F_of(10):.3f}")
check("G1 [identity] F(s) -> (4/3) s^{3/2} in deep MOND and grows linearly beyond saturation", deep_ok and sat_ok)
# ---- cosmology ----
E = lambda a: math.sqrt(OM/a**3 + OL); Hh = lambda a: H0*E(a)
def D_growth(a):                                                              # linear growth factor, normalised D(1) = 1
    I = lambda aa: quad(lambda x: 1/(x*E(x))**3, 1e-6, aa)[0]
    return (E(a)*I(a))/(E(1)*I(1))
f0 = OM**0.55
t_of_a = lambda a: quad(lambda x: 1/(x*Hh(x)), 1e-6, a)[0]
t0 = t_of_a(1.0)
# Maxwellian <s^p> for |g| with rms sigma: <|g|^p> = sigma^p (2/sqrt(pi))^{...}; use direct quadrature on the 3D Maxwellian
def maxw_mean(func, sig):                                                     # mean of func(|g|) for a 3D Gaussian field with rms |g| = sig
    s1 = sig/math.sqrt(3)
    return quad(lambda g: func(g)*4*math.pi*g**2*math.exp(-g**2/(2*s1**2))/((2*math.pi)**1.5*s1**3), 0, 12*s1, limit=200)[0]
def L_ratio_at(a, sig_g0, a0, KB, halo=False):                                # <L_phi>/rho_Lambda at scale factor a (L in units of rho_Lambda)
    sig = sig_g0*D_growth(a)/a**2
    Fm = maxw_mean(lambda g: F_of(g/a0), sig)
    if halo: Fm += 1e-4*F_of(3.0)
    return (2 - KB)*Fm*(a0**2/G)/(16*math.pi)/(4*A0["canonical"]**2/G)       # rho_Lambda c^2 = 4 a0_can^2/G (kappa = 1/2, Planck)
res = {}
for vrms in (300e3, 600e3):
    sig_g0 = 3*OM*H0/(2*f0)*vrms
    for KB in (0.0, 0.25):
        for foot, a0 in A0.items():
            today = L_ratio_at(1.0, sig_g0, a0, KB); today_h = L_ratio_at(1.0, sig_g0, a0, KB, halo=True)
            avg = {}
            for Tfac in (1.0, 3.0, 10.0):
                a_T = brentq(lambda aa: t_of_a(aa) - Tfac*t0, 1.0, 1e6) if Tfac > 1 else 1.0
                num = quad(lambda aa: aa**3*L_ratio_at(aa, sig_g0, a0, KB)/(aa*Hh(aa)), 0.02, a_T, limit=60)[0]
                den = quad(lambda aa: aa**3/(aa*Hh(aa)), 0.02, a_T, limit=60)[0]
                avg[Tfac] = num/den
            res[(vrms, KB, foot)] = dict(sig_g0_a0=sig_g0/a0, today=today, today_halo=today_h, avg=avg)
            print(f"    v_rms = {vrms/1e3:.0f} km/s (sigma_g0 = {sig_g0/a0:.4f} a0), K_B = {KB:.2f}, {foot:9s}: L/rho_L today = {today:.2e} (with 100x halo term {today_h:.2e}); spacetime average to T = t0, 3 t0, 10 t0: " + ", ".join(f"{v:.2e}" for v in avg.values()))
check("G2 [today] the scalar's Lagrangian density averaged over the present cosmic volume reaches 0.5 rho_Lambda for some v_rms, K_B, footing", any(r["today_halo"] >= 0.5 for r in res.values()), f"largest = {max(r['today_halo'] for r in res.values()):.1e}")
conv = [r["avg"][10.0]/r["avg"][1.0] for r in res.values()]
check("G3 [future] the spacetime average converges to a nonzero fraction of rho_Lambda (average to 10 t0 within 10x of the average to t0, and >= 0.5 rho_Lambda)", all(x > 0.1 for x in conv) and any(r["avg"][10.0] >= 0.5 for r in res.values()), f"ratio(10 t0 / t0) = {min(conv):.1e}-{max(conv):.1e}; the de Sitter future drives it to zero")
s_star = {}
for KB in (0.0, 0.25):
    for foot, a0 in A0.items():
        s_star[(KB, foot)] = brentq(lambda s: (2 - KB)*F_of(s)*(a0**2/G)/(16*math.pi) - 4*A0["canonical"]**2/G, 1.0, 1e4)
print(f"    G4: the acceleration at which L_phi alone equals rho_Lambda: s_* = {json.dumps({f'K_B={k[0]}/{k[1]}': round(v, 1) for k, v in s_star.items()})} a0 -- the volume-averaged |g| of the universe is {min(r['sig_g0_a0'] for r in res.values()):.3f}-{max(r['sig_g0_a0'] for r in res.values()):.3f} a0")
check("G4 [regime] the acceleration at which the scalar's Lagrangian equals rho_Lambda lies within 10x of the cosmic rms peculiar acceleration", all(v < 10*max(r["sig_g0_a0"] for r in res.values()) for v in s_star.values()), f"s_* = {min(s_star.values()):.0f}-{max(s_star.values()):.0f} against 0.006-0.012: a factor {min(s_star.values())/max(r['sig_g0_a0'] for r in res.values()):.0f}+")
print("\n  OUTCOME: a global constraint tying Lambda to the spacetime average of the MOND scalar's Lagrangian misses rho_Lambda by five orders of magnitude"
      "\n           today and tends to zero in the de Sitter future; the universe would have to sit at ~80 a0 on average, not ~0.01 a0.  Closed on magnitude,"
      "\n           independently of sign and of the O(1) convention.  With k01 this exhausts the principles that act on the scalar's zero: the positive Lambda"
      "\n           must come from the geometric/boundary sector, where the only coefficient-free identification in hand is a0 = c^2/(2 pi L_dS) (kappa = 0.461).")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
