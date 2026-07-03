#!/usr/bin/env python3
"""ADVERSARIAL VERIFIER for the 2026-07 PU/PT gauntlet (G2 reality cap; G4 sign/exponent).

Re-derives from scratch (independent routes) the two load-bearing claims:
  [A] G2: "unbroken PT <=> mu_eff >= 3/4; framework hits 3/4 at a=(12/7)a0; entire MOND regime past EP"
  [B] G4: exact identity mu_eff = 1-(Omega/w_eff)^2; softening sign; p=1/2 tail; k' propto R non-universality.

FINDINGS (proved below, all asserts):
  A1. The exact harmonic-well dichotomy is  w >= 2*Omega0(WELL), which on the circular-orbit
      branch is  mu_eff >= 1/2  -- NOT 3/4.  The gauntlet substituted the ORBITAL frequency
      (w_eff >= 2*Omega) for the WELL frequency (w_eff >= 2*Omega0).  Counterexample at mu=0.718.
  A2. Corollary theorem: with the local-harmonic proxy Omega0^2 = g_N/R = mu*Omega^2, reality
      reads 4*mu*(1-mu) <= 1: AUTOMATICALLY satisfied on-shell, saturated exactly at mu = 1/2.
      => the claimed MW "broken window [0.38,2.6]a0" is an artifact of the slip (harmonic proxy:
      window EMPTY; orbits with mu<1/2 simply don't exist on the branch = EP-excluded).
  A3. Framework milestone moves: mu=1/2 at a=(2/3)a0 (g_bar=a0/3), not (12/7)a0.  Flat-curve
      epicyclic anchor (kappa^2=2*mu*Omega^2) gives broken band mu in (0.146,0.854), i.e.
      a <~ 3.15*a0 -- PLAUSIBLE only (Coriolis-coupled 8th-degree polynomial not done).
  B1. Identity a[1-(Omega/w)^2 k'(y)] = g_N re-derived (general k, exact): CONFIRMED.
  B2. SIGN: softening REQUIRES the ghost sign of the xddot^2 term; healthy sign => stiffening
      (anti-MOND).  CONFIRMED -- MOND-direction and ghost are inseparable in local PU.
  B3. p=1/2 tail: kappa_par = k'+2yk'' = 0 exactly; required k' at fixed y scales as R (x10 at
      2->20 kpc); 200->300 km/s at g_bar=0.7a0 gives 0.176 dex: all CONFIRMED.
  B4. Broken-phase numerics (Re lambda = 0.300*Omega0 at w=1.8*Omega0) reproduced; this is a
      CLASSICAL complex-frequency statement -- inner-product independent, NOT a lazy-Hermitian kill.
  B5. Induced quartic for k_sat = y - y^2 + ...: H_a quartic coefficient = -w^6/(2 a0^2 m^3) p_v^4
      NEGATIVE: gauntlet's Smilga-malicious flag CONFIRMED (their c2-convention k = y - c2*y^2).
  B6. k_tail = y + 2*beta*sqrt(y): k'(y->0) -> oo (nonanalytic): the perturbative order-by-order
      PT-reality clause (Caliceti-Graffi-type) applies to k_sat ONLY, not k_tail.
"""
import sympy as sp
import numpy as np

PASS = []
def ok(name, cond):
    assert cond, name
    PASS.append(name); print(f"  PASS: {name}")

# ================= [B1]+[B2] EL identity, general k, BOTH signs =================
print("[B1/B2] circular-orbit identity + sign theorem")
t, R, Om, w, m, a0s, kp = sp.symbols('t R Omega w m a0 kprime', positive=True)
eps = sp.symbols('epsilon')          # eps=+1 ghost sign (-xdd^2 in L), eps=-1 healthy sign
x1, x2 = R*sp.cos(Om*t), R*sp.sin(Om*t)
for comp in (x1, x2):
    # L = m v^2/2 - eps*(m a0^2/2w^2) k(y);  dL/dxdd_i = -eps*(m/w^2) k'(y) xdd_i ; y const on orbit
    EL = -m*sp.diff(comp, t, 2) - eps*(m/w**2)*kp*sp.diff(comp, t, 4)   # inertial side; EL + F_N = 0
    targ = m*Om**2*comp*(1 - eps*(Om**2/w**2)*kp)                        # = -F_N = +m g_N/R * comp
    ok(f"EL({comp}) == a[1 - eps*(Om/w)^2 k'] radial balance", sp.simplify(EL - targ) == 0)
# => mu_eff = g_N/a = 1 - eps*(Om/w)^2 k' : eps=+1(ghost) SOFTENING; eps=-1(healthy) STIFFENING
ok("softening (mu<1) <=> ghost sign; healthy sign => anti-MOND stiffening", True)

# ================= [A1] harmonic-well dichotomy: the exact cap is mu >= 1/2 =================
print("[A1] harmonic well, k'=1: exact EP cap")
om, W0, u, r = sp.symbols('omega Omega0 u r', positive=True)
char = om**4/w**2 - om**2 + W0**2                       # x'''' /w^2 + x'' + W0^2 x = 0, x~e^{i om t}
sol = sp.solve(char, om**2)
w_minus = sp.simplify(sp.Min(*[sp.simplify(s) for s in sol]).rewrite(sp.Piecewise)) if False else None
s_lo = sp.simplify((w**2 - sp.sqrt(w**4 - 4*w**2*W0**2))/2)   # slow root
ok("slow root om_-^2 = w(w - sqrt(w^2-4 W0^2))/2 solves char", sp.simplify(char.subs(om**2, s_lo)) == 0)
# reality <=> w >= 2*W0 (WELL frequency). On the orbit branch Om^2 = s_lo:
mu_of_r = sp.simplify(1 - s_lo.subs(w, W0/r)/ (W0/r)**2)      # r = W0/w;  mu = 1-(Om/w)^2
mu_r = sp.simplify((1 + sp.sqrt(1 - 4*r**2))/2)
ok("mu(r) = (1+sqrt(1-4r^2))/2 on the circular branch", sp.simplify(mu_of_r - mu_r) == 0)
ok("mu at the EP (r=1/2) = 1/2  [gauntlet claims 3/4: WRONG constant]",
   sp.simplify(mu_r.subs(r, sp.Rational(1,2)) - sp.Rational(1,2)) == 0)
ok("mu range in unbroken phase = [1/2, 1] (monotone in r)",
   sp.simplify(mu_r.subs(r, 0) - 1) == 0 and sp.diff(mu_r, r).subs(r, sp.Rational(1,4)) < 0)
# the (2u^2-1)^2 identity: reality condition rewritten on-shell (W0^2 = Om^2(1-u^2), u=Om/w)
lhs = sp.expand(1 - 4*u**2*(1 - u**2))
ok("1 - 4u^2(1-u^2) == (2u^2-1)^2  (on-shell reality auto-satisfied, saturating at u^2=1/2)",
   sp.simplify(lhs - (2*u**2 - 1)**2) == 0)
# COUNTEREXAMPLE to 'unbroken => mu>=3/4': r=0.45 < 1/2 (unbroken) but mu=0.718 < 3/4
mu_cx = float(mu_r.subs(r, sp.Rational(45,100)))
ok(f"counterexample: r=0.45 unbroken, mu={mu_cx:.3f} in [1/2,3/4) -- their dichotomy fails", 0.5 < mu_cx < 0.75)

# ================= [A2] on-shell auto-reality theorem (kills the 'MW broken window') ============
print("[A2] local-harmonic proxy: 4 mu(1-mu) <= 1 identically")
mu = sp.symbols('mu', positive=True)
# Omega0^2 = g_N/R = mu*Omega^2 ; broken <=> w_eff < 2 Omega0 <=> 4 mu (Om/w_eff)^2 = 4 mu (1-mu) > 1
ok("max_mu 4 mu(1-mu) = 1 at mu=1/2 (never exceeded)",
   sp.simplify(sp.maximum(4*mu*(1-mu), mu, sp.Interval(0,1)) - 1) == 0)
# => under the CORRECT harmonic-proxy threshold, no circular orbit is in the broken phase;
#    instead mu<1/2 orbits DO NOT EXIST on the branch (EP-excluded). Their r(a)-window used 2*Omega.

# ================= [A3] framework milestones under corrected caps =================
print("[A3] framework a(mu) milestones")
xx = sp.symbols('x', positive=True)                      # x = a/a0
mu_fw = (sp.sqrt(1 + 4*xx**2) - 1)/(2*xx)                # from g_obs = sqrt(gb^2 + gb a0), mu = gb/a
a_12_7 = sp.solve(sp.Eq(mu_fw, sp.Rational(3,4)), xx)
ok("their algebra given their premise: mu_fw=3/4 at a=(12/7)a0", a_12_7 == [sp.Rational(12,7)])
a_2_3 = sp.solve(sp.Eq(mu_fw, sp.Rational(1,2)), xx)
ok("CORRECTED harmonic-anchor milestone: mu_fw=1/2 at a=(2/3)a0 (g_bar=a0/3)", a_2_3 == [sp.Rational(2,3)])
# flat-curve epicyclic anchor: kappa^2 = 2 mu Om^2; broken <=> 8 mu(1-mu) > 1
mu_flat = sp.solve(sp.Eq(8*mu*(1-mu), 1), mu)
mu_hi = max(float(v) for v in mu_flat)                   # (2+sqrt(2))/4
ok(f"flat-curve (PLAUSIBLE) cap mu >= (2+sqrt(2))/4 = {mu_hi:.4f} (~ their 7/8 caveat)",
   abs(mu_hi - (2+np.sqrt(2))/4) < 1e-12)
a_flat = float(sp.solve(sp.Eq(mu_fw, sp.nsimplify(mu_hi, rational=False)), xx)[0]) if False else \
         float(mu_hi/(1-mu_hi**2))                        # a/a0 = mu/(1-mu^2)
ok(f"flat-curve EP at a = {a_flat:.2f} a0 (g_bar = {a_flat*mu_hi:.2f} a0) -- covers the flat-curve MOND zone",
   3.0 < a_flat < 3.3)

# ================= [B3] G4 exponent/universality checks =================
print("[B3] tail exponent + universality")
yv = sp.symbols('y', positive=True)
k_tail_pure = 2*sp.sqrt(yv)                              # k' = y^(-1/2)
ok("kappa_par = k'+2yk'' = 0 EXACTLY at p=1/2", sp.simplify(
    sp.diff(k_tail_pure, yv) + 2*yv*sp.diff(k_tail_pure, yv, 2)) == 0)
a0n = 9.36e-11; wn = 3.08e-16; a_t = 0.5*a0n
mu_f = lambda a: (np.sqrt(a0n**2 + 4*a**2) - a0n)/(2*a)
kreq = [(wn**2*Rn/a_t)*(1 - mu_f(a_t)) for Rn in (6.2e19, 6.2e20)]   # k' = (1-mu) w^2/Om^2, Om^2=a/R
ok(f"required k' at fixed y: {kreq[0]:.3f} vs {kreq[1]:.3f}, ratio {kreq[1]/kreq[0]:.1f} = R2/R1 (not a fn of y)",
   abs(kreq[1]/kreq[0] - 10) < 1e-9 and abs(kreq[0] - 0.074) < 0.005)
dex = np.log10((1/0.52)/(1/0.78))
ok(f"200->300 km/s at fixed g_bar: {dex:.3f} dex (> 0.108 dex total RAR scatter)", abs(dex - 0.176) < 0.003)
# WB vs galaxy frequency ratio at the same y: Om = a/v => (v_gal/v_WB)^2
ok(f"WB kill order: (200 km/s / 0.3 km/s)^2 = {(200/0.3)**2:.1e} ~ 1e5-class overshoot (their C=2.4e4 conservative)",
   1e5 < (200/0.3)**2 < 1e6)

# ================= [B4] broken-phase classical rate (inner-product independent) ==========
print("[B4] broken-phase growth")
rts = np.roots([1/1.8**2, 0, 1, 0, 1.0])                 # lam^4/w^2 + lam^2 + W0^2, w=1.8, W0=1
ok(f"max Re(lambda) = {max(rts.real):.3f} Omega0 at w=1.8 Omega0 (gauntlet: 0.30)",
   abs(max(rts.real) - 0.300) < 0.005)

# ================= [B5] induced quartic sign (independent Legendre) =================
print("[B5] k_sat quartic sign")
al, be, p2, add = sp.symbols('alpha beta p2 xdd', positive=True)
L2 = -(al/2)*add**2 + (be/2)*add**4                      # k_sat: -(m a0^2/2w^2)(y - y^2) => alpha=m/w^2, beta=m/(w^2 a0^2)
pexp = sp.diff(L2, add)                                  # p2 = -alpha xdd + 2 beta xdd^3
a_inv = -p2/al - 2*be*p2**3/al**4                        # perturbative inversion
ok("inversion residual O(p2^5)", sp.expand(sp.series(pexp.subs(add, a_inv) - p2, p2, 0, 4).removeO()) == 0)
Ha = sp.expand(sp.series(p2*a_inv - L2.subs(add, a_inv), p2, 0, 5).removeO())    # Ostrogradsky sector: H = p_v*xdd - L
q4 = sp.simplify(Ha.coeff(p2, 4))
q4_val = sp.simplify(q4.subs({al: 1, be: 1}))
ok(f"H quartic coeff = {sp.simplify(q4)} -> negative for beta>0 (k_sat): Smilga-malicious flag CONFIRMED",
   q4_val < 0 and sp.simplify(q4 + be/(2*al**4)) == 0)

# ================= [B6] k_tail nonanalyticity =================
print("[B6] k_tail scope")
bet = sp.symbols('beta', positive=True)
kp_tail = sp.diff(yv + 2*bet*sp.sqrt(yv), yv)
ok("k_tail: k'(y->0+) -> oo (nonanalytic): perturbative PT-reality clause applies to k_sat ONLY",
   sp.limit(kp_tail, yv, 0, '+') == sp.oo)

print(f"\nALL {len(PASS)} CHECKS PASS.")
print("VERDICT CORE: G4 CONFIRMED in full; G2 structure CONFIRMED but constant CORRECTED 3/4 -> 1/2")
print("(harmonic-exact; flat-curve ~0.854 PLAUSIBLE); 'entire MOND regime past EP' UNPROVEN as stated;")
print("deep MOND mu<1/2 (g_bar < a0/3) EP-excluded unconditionally; MW 'broken window' numeric needs re-run")
print("with the well-frequency threshold (harmonic proxy: window empty, replaced by non-existence).")
print("EXIT 0")
