#!/usr/bin/env python3
"""
k04 -- the four-form promotion of a0 (relayed OpenAI construction, 2026-09-06): sign, coefficient, and the local-sector feedback
================================================================================================================================
Construction under test: a three-form gauge potential with four-form field strength F = q eps (dual amplitude q), vacuum action
P(q) = Z q^2/2, and the MOND scale promoted to the flux, a0 = beta sqrt(G) |q|.  Standard four-form facts (Duff & van Nieuwenhuizen
1980; Bousso & Polchinski 2000): no propagating modes, stress tensor T_mu nu = (P - q P_q) g_mu nu, so the gravitating energy is
eps = q P_q - P (a Legendre form, NOT -P).  Consequences claimed in the note and checked here on the candidate's own kernel:

  F1 [sign]         the promoted primitive constant, L_vac = +b a0^2/G = +b beta^2 q^2 (b = (2-K_B) I/(16 pi) > 0, k01), has gravitating
                    energy +b a0^2/G: the k01 sign is reversed without touching the attractive MOND gradient term (sympy);
  F2 [coefficient]  the flux amplitude cancels from kappa^2 = a0^2/(G eps_vac) = 2 beta^2/(Z + 2 b beta^2); kappa = 1/2 requires
                    Z/beta^2 = 8 - 2b = 7.96.  Requirement: the action fixes Z/beta^2 (it does not: two couplings, one ratio);
  F3 [feedback]     a0 -> a0(q) puts the galaxy sector into the four-form equation d_mu(dL/dq) = 0, i.e. dL/dq = const: with
                    dJ/da0|_Y = (2/a0)(J - Y J_Y), Y J_Y = g_phi g_N = a0^2 s Delta and J = a0^2 j(s), the flux obeys
                       q [ Z + (2-K_B) beta^2 (s Delta - j)/(8 pi) ] = Z q_0   =>   a0_loc/a0 = 1/[1 + (2-K_B)(s Delta - j)/(64 pi)]  at Z = 8 beta^2,
                    solved self-consistently (s = g_N/a0_loc).  Galaxies: |Delta log g_obs| < 0.01 dex for g_N <= 100 a0 (RAR scatter 0.1 dex);
  F4 [Solar System] in the saturated regime the flux equation is LINEAR in q: a0_loc = a0 (1 - g_N/g_*) with g_* = 8 pi Z a0/((2-K_B) beta^2 Delta_sat)
                    = 155 a0 (K_B = 0, Z = 8 beta^2); beyond g_* the only solution is q = 0 (a kink of |q|): the scalar switches OFF.  The promoted
                    residual Delta_sat a0_loc against the g03d planetary sunward bound A_SUNWARD = a0/(2 x 1278) at Mercury-Neptune: does it replace xi?
  F5 [wide binaries] a0_loc at 2-20 kAU for a 1.5 Msun pair and the induced shift of gamma_v (d ln gamma_v/d ln a0 = 0.1155) vs DR4's +/-0.015;
  F6 [stability]    the effective flux stiffness Z_eff = Z + (2-K_B) beta^2 (s Delta - j)/(8 pi) stays positive (s Delta - j >= 0).
FAIL marks a requirement the construction does not meet.  Nothing here derives the 8.
"""
import numpy as np, math, json, sys
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
G = 6.674e-11; c = 2.998e8; MSUN = 1.989e30; AU = 1.496e11
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
print("=" * 118); print("k04 -- four-form promotion of a0: sign, coefficient, and the feedback on the local sector"); print("=" * 118)
# ---- kernel ----
Delta = lambda s: s/np.expm1(np.sqrt(s)) if s > 0 else 0.0
opt = minimize_scalar(lambda s: -Delta(s), bounds=(0.5, 6), method='bounded'); s_sat, D_sat = opt.x, -opt.fun
jsat = 2*(s_sat*D_sat - quad(Delta, 0, s_sat)[0])
def j_of(s): return 2*(s*Delta(s) - quad(Delta, 0, s)[0]) if s <= s_sat else jsat
def Dl(s): return Delta(s) if s <= s_sat else D_sat
I_rar = jsat
# ---- F1: sign (sympy) ----
q, Z, b, beta, Gs = sp.symbols('q Z b beta G', positive=True)
P = Z*q**2/2 + b*beta**2*q**2
eps = sp.simplify(q*sp.diff(P, q) - P)
a0sq_over_G = beta**2*q**2                       # a0^2/G = beta^2 q^2
print(f"    F1: P(q) = {P};  eps = q P_q - P = {eps};  promoted-primitive part = +b a0^2/G = {sp.simplify(eps - Z*q**2/2)}  (k01 had -b a0^2/G)")
check("F1 [sign] the promoted primitive's gravitating energy is +b a0^2/G (reversed from k01's -b a0^2/G) with the MOND gradient term untouched", sp.simplify(eps - Z*q**2/2 - b*a0sq_over_G) == 0)
# ---- F2: coefficient ----
kappa2 = sp.simplify(a0sq_over_G/eps)
ratio_needed = sp.solve(sp.Eq(kappa2, sp.Rational(1, 4)), Z)[0]/beta**2
b_num = {KB: (2 - KB)*I_rar/(16*math.pi) for KB in (0.0, 0.25)}
print(f"    F2: kappa^2 = {kappa2};  kappa = 1/2  <=>  Z/beta^2 = {ratio_needed} = {json.dumps({f'K_B={k}': round(float(ratio_needed.subs(b, v)), 3) for k, v in b_num.items()})}  (b = (2-K_B) I/(16 pi), I = {I_rar:.4f})")
check("F2 [coefficient] the action fixes the ratio Z/beta^2 (kappa = 1/2 needs 7.96); it is a free ratio of two couplings, q cancels", False, "the flux amplitude cancels from kappa, the coefficient does not: one number, undetermined")
# ---- F3: feedback in galaxies ----
def a0loc_ratio(gN, a0, KB, ZoB=8.0):
    r = 1.0
    for _ in range(200):
        s = gN/(a0*r); r_new = 1.0/(1.0 + (2 - KB)*(8.0/ZoB)*(s*Dl(s) - j_of(s))/(64*math.pi))
        if abs(r_new - r) < 1e-12: break
        r = r_new
    return r
rows = []
for KB in (0.0, 0.25):
    for foot, a0 in A0.items():
        for s0 in (0.01, 0.1, 1.0, 2.54, 10.0, 100.0, 1e3):
            gN = s0*a0; r = a0loc_ratio(gN, a0, KB); s = gN/(a0*r)
            gobs_p = gN + a0*r*Dl(s); gobs_0 = gN + a0*Dl(s0)
            rows.append(dict(KB=KB, foot=foot, s=s0, ratio=r, dlog=math.log10(gobs_p/gobs_0)))
for KB in (0.0, 0.25):
    line = ", ".join(f"s={r['s']:g}: {r['ratio']:.4f} ({r['dlog']:+.4f} dex)" for r in rows if r["KB"] == KB and r["foot"] == "canonical")
    print(f"    F3: K_B = {KB:.2f} canonical: a0_loc/a0 (Delta log g_obs): {line}")
check("F3 [feedback, galaxies] the environmental a0 changes the RAR by < 0.01 dex for g_N <= 100 a0 (both footings, K_B 0-0.25)", all(abs(r["dlog"]) < 0.01 for r in rows if r["s"] <= 100), f"max |Delta log g_obs| at s <= 100 = {max(abs(r['dlog']) for r in rows if r['s'] <= 100):.4f} dex; a0 falls by {100*(1-min(r['ratio'] for r in rows if r['s'] == 2.54)):.1f}% at the knee and {100*(1-min(r['ratio'] for r in rows if r['s'] == 100)):.0f}% at 100 a0")
# ---- F4: Solar System without the coherence length ----
PLANETS = {"Mercury": 0.387, "Venus": 0.723, "Earth": 1.0, "Mars": 1.524, "Jupiter": 5.203, "Saturn": 9.58, "Uranus": 19.2, "Neptune": 30.05}
ss = {}
for foot, a0 in A0.items():
    A_SUN = a0/(2*1278.0)
    for name, au in PLANETS.items():
        gN = G*MSUN/(au*AU)**2; r = a0loc_ratio(gN, a0, 0.0); gphi = D_sat*a0*r
        ss[(foot, name)] = dict(gN=gN, gphi=gphi, over=gphi/A_SUN)
    print(f"    F4: {foot:9s} promoted residual g_phi = Delta_sat a0_loc vs the sunward bound {A_SUN:.2e} m/s^2: " + ", ".join(f"{n} {ss[(foot, n)]['gphi']:.1e} ({ss[(foot, n)]['over']:.1f}x)" for n in ("Mercury", "Earth", "Saturn", "Neptune")))
check("F4 [Solar System] the promotion alone (no coherence length) keeps the planetary residual below the g03d sunward bound at every planet", all(v["over"] < 1 for v in ss.values()), f"largest residual/bound = {max(v['over'] for v in ss.values()):.1e}: the scalar is switched off inside g_N = 155 a0 (r < 205 AU); the Cassini quadrupole is set at s ~ 1 where a0_loc = 0.997 a0, so xi is still required")
# ---- F5: wide binaries ----
wb = {}
for foot, a0 in A0.items():
    for kau in (2, 3, 5, 10, 20):
        gN = G*1.5*MSUN/(kau*1e3*AU)**2; r = a0loc_ratio(gN, a0, 0.0); wb[(foot, kau)] = dict(s=gN/a0, ratio=r, dgam=0.1155*math.log(r))
    print(f"    F5: {foot:9s} a0_loc/a0 at 2, 3, 5, 10, 20 kAU (1.5 Msun): " + ", ".join(f"{wb[(foot, k)]['ratio']:.3f} (dgamma_v {wb[(foot, k)]['dgam']:+.4f})" for k in (2, 3, 5, 10, 20)))
check("F5 [wide binaries] the induced shift of gamma_v in the 2-3 kAU bins is below DR4's +/-0.015 (not separable this decade)", all(abs(v["dgam"]) < 0.015 for v in wb.values()), f"largest |dgamma_v| = {max(abs(v['dgam']) for v in wb.values()):.4f} at 2 kAU")
# ---- F6: stability ----
smin = min(s*Dl(s) - j_of(s) for s in np.geomspace(1e-3, 1e4, 60))
check("F6 [stability] the effective flux stiffness Z_eff = Z + (2-K_B) beta^2 (s Delta - j)/(8 pi) is positive everywhere (s Delta - j >= 0)", smin >= -1e-12, f"min(s Delta - j) = {smin:.2e}")
print("\n  OUTCOME: the four-form promotion does what the note claims and no more.  Sign: reversed (F1).  Form: a0 and rho_Lambda from ONE conserved flux,"
      "\n           so a0 ~ sqrt(G rho_Lambda) becomes structural and the flux amplitude cancels; the coefficient becomes the coupling ratio Z/beta^2 = 8,"
      "\n           which nothing fixes (F2).  Feedback: a0 becomes environmental, a0_loc = a0 (1 - g_N/155 a0): 1.2% low at the RAR knee, 64% low at 100 a0,"
      "\n           and the scalar switches OFF above 155 a0 = 1.4e-8 m/s^2 (inside 205 AU of the Sun); invisible in galaxies (F3), a 1-sigma shift of"
      "\n           DR4's 2 kAU bin (F5), stable (F6); it screens the Solar-System MONOPOLE by itself (F4) but not the Cassini quadrupole, set at s ~ 1,"
      "\n           so the coherence length is still required."
      "\n           Net: the half is now 'why Z = 8 beta^2', a cleaner question than 'why 32 pi', and still an open one.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
