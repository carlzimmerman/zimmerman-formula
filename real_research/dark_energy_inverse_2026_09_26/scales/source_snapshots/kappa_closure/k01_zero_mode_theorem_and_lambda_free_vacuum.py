#!/usr/bin/env python3
"""
k01 -- the kappa-closure audit: can the candidate action relate a0 to Lambda?  (zero-mode theorem + the Lambda-free vacuum)
=========================================================================================================================
The empirical relation a0 = (1/2) c sqrt(G rho_Lambda) (kappa = 1/2, fitted) has never been derived.  The proposal under test
(relayed OpenAI note, 2026-09-06): integrate the nondynamical fields out of the candidate action S_full -> S_static[Phi] and
read the coefficient of the MOND primitive's additive constant against rho_Lambda.  Three outcomes were listed: a fixed
nontrivial normalisation eta_eff (prediction), eta_eff = 1 (kappa = 0.984, dead), or an arbitrary additive constant (the
normalisation zero mode, no derivation possible).  This script settles the audit for the action as written, in the
pipeline's convention (g03t):

    L = sqrt(-g) [ R - 2 Lambda - c1 T1 - c2 T2 - c3 T3 + c4 T4 + 2(2-K_B) J^mu d_mu phi - (2-K_B) J(Y) - K(Q) ] / (16 pi G) + L_m,

Y = q^{mu nu} d_mu phi d_nu phi (the MOND scalar's spatial gradient squared), J^i -> d_i Psi in the static limit, and the
carried kernel J_Y(s) = s / Delta(s) with g_phi = a0 Delta(s), s = g_N/a0 (THE_ACTION section 3): nu_RAR up to the maximum of
Delta (s = 2.540, Delta = 0.6476) and saturated beyond; the exponential carrier is the AQUAL mu(x) = 1 - e^{-x} with the same
saturation at its maximum (Delta = 1/e at x = 1).

  K1 [theorem, statics]   the static Euler-Lagrange equations contain J only through J' : J -> J + C leaves them invariant
                          (sympy, generic J);
  K2 [theorem, FLRW]      on the background Y = 0 the constant enters only as Lambda_eff = Lambda + (2-K_B) J(0)/2 + K(Q0)/2:
                          with Lambda explicit and free, no equation of the action relates a0 to Lambda -- outcome 3, proven;
  K3 [Lambda-free, sign]  delete the explicit Lambda and fix the primitive's zero by the only principle available to a local
                          action, an empty Newtonian vacuum (J = 0 at the saturated/Newtonian end).  The background vacuum
                          energy is then rho_vac = (2-K_B) J(0) / (16 pi G) = -(2-K_B) I a0^2 / (16 pi G) with
                          I = 2 int_0^{s_sat} s dDelta > 0 for every kernel of the class: NEGATIVE.  Requirement: rho_vac > 0;
  K4 [Lambda-free, size]  |rho_vac| / rho_Lambda = (2-K_B) I kappa^2 / (16 pi) at the footings' kappa (1/2, 0.602), with the
                          G renormalisations G_N/G = 1/(1 - c14/2) and G_cos/G = 1/(1 + 3 c2/2) folded in as a range.
                          Requirement: within a factor 2 of unity for some normalisation in the action;
  K5 [QUMOND reading]     the constant 4 pi^4 / 15 of the nu_RAR primitive (the OpenAI note's C_RAR) is what the UNSATURATED,
                          non-monotone branch returns: 2 int_0^inf s dDelta = -4 pi^4/15 for nu_RAR and -2 for the carrier.
                          The bounded-boost theorem forbids that branch.  Read as if it were the vacuum energy, it gives
                          kappa_pred = sqrt(60 / ((2-K_B) pi^3)) = 0.984 (K_B = 0) to 1.05 (K_B = 0.25) for nu_RAR and 3.5 for
                          the carrier.  Requirement: within 2 sigma of both measured kappa (0.465 +/- 0.076, 0.551 +/- 0.043).
  K6 [numerology guard]   the coefficient of C a0^2/(16 pi G) that would put the QUMOND reading at kappa = 1/2 is 16 pi/(kappa^2 C)
                          = 7.7 for nu_RAR, against the action's (2-K_B) in [1.75, 2] (a factor 3.9-4.4); (2-K_B)^2 gives only
                          0.70-0.80.  No term of the action carries such a coefficient.  Recorded so that no factor is adopted later.

Rule of the branch: no mechanism counts unless a0 and Lambda begin independent and the equations remove one degree of
freedom.  FAIL marks a requirement the action does not meet.
"""
import numpy as np, math, json, sys
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
G = 6.674e-11; c = 2.998e8
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KAPPA_FOOT = {f: a/(2*9.3619e-11) for f, a in A0.items()}                 # kappa = a0 / (c sqrt(G rho_Lambda)); canonical == 1/2 by construction
RHO_L = (2*A0["canonical"]/c)**2/G                                        # rho_Lambda from the canonical footing (5.84e-27 kg/m^3, Planck)
KAPPA_MEAS = {"BTFR": (0.465, 0.076), "distance-free": (0.551, 0.043)}   # project_zimmerman_coefficient_footing
print("=" * 118); print("k01 -- kappa-closure audit: zero-mode theorem and the Lambda-free vacuum of the candidate action"); print("=" * 118)
print(f"    rho_Lambda = {RHO_L:.3e} kg/m^3; footings kappa = {json.dumps({f: round(v, 4) for f, v in KAPPA_FOOT.items()})}; measured kappa = {KAPPA_MEAS}")
# ---------------- K1: statics -----------------
x = sp.symbols('x', real=True); KB, C, rho = sp.symbols('K_B C rho', real=True)
Psi = sp.Function('Psi')(x); phi = sp.Function('phi')(x); J = sp.Function('J')
Y = sp.diff(phi, x)**2
L = -2*sp.diff(Psi, x)**2 + 2*(2 - KB)*sp.diff(Psi, x)*sp.diff(phi, x) - (2 - KB)*J(Y) - rho*(Psi + phi)      # static sector, overall 1/16piG dropped
from sympy.calculus.euler import euler_equations
EL = euler_equations(L, [phi, Psi], x)
ELC = euler_equations(L - (2 - KB)*C, [phi, Psi], x)
same = all(sp.simplify(a.lhs - b.lhs) == 0 for a, b in zip(EL, ELC))
has_bare_J = any(e.lhs.has(J(Y)) and not e.lhs.has(sp.Derivative) for e in EL)
print(f"    K1: scalar equation  {sp.simplify(EL[0].lhs)} = 0   (J appears only through its derivative)")
check("K1 [theorem, statics] the static field equations are invariant under J -> J + C: J enters only through J'", same and not has_bare_J)
# ---------------- K2: FLRW background -----------------
Lam, J0, K0, a = sp.symbols('Lambda J_0 K_0 a', positive=True)
Lconst = a**3*(-2*Lam - (2 - KB)*J0 - K0)                                  # the constant part of the minisuperspace Lagrangian at Y = 0, Q = Q0
Lam_eff = sp.solve(sp.Eq(Lconst, a**3*(-2*sp.Symbol('Lambda_eff'))), sp.Symbol('Lambda_eff'))[0]
print(f"    K2: Lambda_eff = {sp.expand(Lam_eff)}")
check("K2 [theorem, FLRW] the background sees only Lambda + (2-K_B) J(0)/2 + K(Q0)/2; with Lambda explicit and free, no equation of the action relates a0 to Lambda (outcome 3 for the action as written)", sp.simplify(Lam_eff - (Lam + (2 - KB)*J0/2 + K0/2)) == 0)
# ---------------- kernels: Delta(s) and the primitive's span I = 2 int s dDelta -----------------
def rar_Delta(s): return s/np.expm1(np.sqrt(s)) if s > 0 else 0.0
opt = minimize_scalar(lambda s: -rar_Delta(s), bounds=(0.5, 6), method='bounded'); s_sat, D_sat = opt.x, -opt.fun
I_rar = 2*(s_sat*D_sat - quad(rar_Delta, 0, s_sat)[0])                    # 2 int_0^{s_sat} s Delta' ds = 2[s Delta] - 2 int Delta ds
I_rar_full = 2*(0 - quad(rar_Delta, 0, np.inf)[0])                        # the unsaturated branch returns to Delta = 0 at s -> inf
# exponential carrier: AQUAL mu = 1 - e^{-x}, x = g/a0: s = x(1 - e^{-x}), Delta = x e^{-x}; saturated at x = 1 (Delta = 1/e)
sx = lambda xx: xx*(1 - np.exp(-xx)); Dx = lambda xx: xx*np.exp(-xx); dDx = lambda xx: (1 - xx)*np.exp(-xx)
I_exp = 2*quad(lambda xx: sx(xx)*dDx(xx), 0, 1)[0]; I_exp_full = 2*quad(lambda xx: sx(xx)*dDx(xx), 0, np.inf)[0]
print(f"    kernels: nu_RAR saturates at s = {s_sat:.3f}, Delta = {D_sat:.4f}; I = 2 int s dDelta = {I_rar:.4f} a0^2 (saturated)  vs  {I_rar_full:.3f} a0^2 on the full unsaturated branch (-4 pi^4/15 = {-4*math.pi**4/15:.3f})")
print(f"             exp carrier saturates at x = 1, Delta = 1/e; I = {I_exp:.4f} a0^2 (saturated)  vs  {I_exp_full:.3f} a0^2 full branch (-2)")
# ---------------- K3 / K4: the Lambda-free vacuum with the Newtonian-vacuum-empty boundary condition -----------------
KBs = [0.0, 0.25]; Gfac = [(1.0, 1.0), (1/(1 - 0.5/2)*0 + 1/(1 - 1e-5/2), 1/(1 + 1.5*0.05))]   # (G_N/G at the PPN corner c14 -> 0, G_cos/G at c2 = 0.05)
rows = []
for kern, I in (("nu_RAR", I_rar), ("exp carrier", I_exp)):
    for KBv in KBs:
        for foot, kap in KAPPA_FOOT.items():
            base = (2 - KBv)*I*kap**2/(16*math.pi)                          # rho_vac / rho_Lambda, sign from J(0) = -I a0^2
            lo, hi = base*min(g1/g2 for g1, g2 in Gfac), base*max(g1/g2 for g1, g2 in Gfac)
            rows.append(dict(kernel=kern, KB=KBv, foot=foot, ratio=-base, lo=-hi, hi=-lo))
for r in rows: print(f"    K3/K4: {r['kernel']:12s} K_B = {r['KB']:.2f} {r['foot']:9s}: rho_vac / rho_Lambda = {r['ratio']:+.5f}  (G-renormalisation range {r['lo']:+.5f} .. {r['hi']:+.5f})")
check("K3 [Lambda-free, sign] with an empty Newtonian vacuum the background vacuum energy of the scalar's primitive is positive", all(r["ratio"] > 0 for r in rows), "it is negative for every kernel, K_B and footing: the scalar's gradient term carries the attractive sign, so its primitive rises toward the Newtonian end")
check("K4 [Lambda-free, size] |rho_vac| / rho_Lambda lies within a factor 2 of unity for some normalisation in the action", any(0.5 < abs(r["ratio"]) < 2 for r in rows), f"largest |ratio| = {max(abs(r['ratio']) for r in rows):.4f}; the needed |J(0)| = 16 pi a0^2/((2-K_B) kappa^2) = {16*math.pi/(2*0.25):.1f} a0^2 at K_B = 0, kappa = 1/2, against the primitive's whole span of {I_rar:.3f} a0^2 (nu_RAR): a factor {16*math.pi/(2*0.25)/I_rar:.0f}")
# ---------------- K5: the QUMOND / unsaturated reading -----------------
def kappa_pred(Cconst, KBv): return math.sqrt(16*math.pi/((2 - KBv)*Cconst))
def nsig(k): return {n: abs(k - m)/e for n, (m, e) in KAPPA_MEAS.items()}
q = {}
for kern, Cc in (("nu_RAR (4 pi^4/15)", -I_rar_full), ("exp carrier (2)", -I_exp_full)):
    for KBv in KBs:
        k = kappa_pred(Cc, KBv); q[(kern, KBv)] = k
        print(f"    K5: {kern:20s} K_B = {KBv:.2f}: kappa_pred = {k:.3f}; sigma from measured = {json.dumps({n: round(v, 1) for n, v in nsig(k).items()})}")
check("K5 [QUMOND reading] the unsaturated-branch constant read as the vacuum energy predicts kappa within 2 sigma of both measurements for some K_B in [0, 0.25]", any(all(v < 2 for v in nsig(k).values()) for k in q.values()), "0.98-1.05 for nu_RAR (>= 6 sigma), 3.5 for the carrier; and the branch it needs is the one the bounded-boost theorem forbids")
# ---------------- K6: numerology guard -----------------
Cr = -I_rar_full; need = {f: 16*math.pi/(k**2*Cr) for f, k in KAPPA_FOOT.items()}
kk = {KBv: math.sqrt(16*math.pi/((2 - KBv)**2*Cr)) for KBv in KBs}
print(f"    K6: coefficient of C a0^2/(16 pi G) needed for the footings' kappa: {json.dumps({f: round(v, 2) for f, v in need.items()})} against the action's (2-K_B) in [1.75, 2] "
      f"(factor {need['canonical']/2:.1f}-{need['canonical']/1.75:.1f} at canonical); (2-K_B)^2 would give kappa = {json.dumps({str(k): round(v, 3) for k, v in kk.items()})}, not in band either")
check("K6 [numerology guard] no coefficient available in the action ((2-K_B), (2-K_B)^2, the G renormalisations) reaches the needed 7.7 for the QUMOND reading: recorded so that no factor is adopted by hand", all(v > 2*1.1 for v in need.values()) and not any(all(s < 2 for s in nsig(k).values()) for k in kk.values()))
print("\n  OUTCOME: outcome 3 of the audit, proven for the action as written (K1, K2); the Lambda-free repair fails on sign (K3) and by a factor >~ 200 in size (K4);"
      "\n           the 4 pi^4/15 reading is the forbidden unsaturated branch and gives kappa ~ 1 (K5); no coefficient of the action reaches the needed 7.7 (K6)."
      "\n           kappa = 1/2 is an empirical boundary condition that this class of local MOND actions cannot derive; a derivation needs a principle that fixes"
      "\n           the absolute zero of the scalar's primitive AND flips its sign -- i.e. a structure outside the present action.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(0)
