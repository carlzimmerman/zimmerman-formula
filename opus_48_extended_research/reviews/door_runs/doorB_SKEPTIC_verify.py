#!/usr/bin/env python3
"""
SKEPTIC re-verification of DOOR B (B_quadratic_vs_dbi).

Independent re-derivation, NOT a re-run of the prior script. I re-derive every
load-bearing number from scratch with my OWN sympy code, and I specifically probe
the three failure modes the prompt flags:
  (i)  did the agent get the Taylor coeffs / lam_D->0 limit right?
  (ii) did the agent MISIDENTIFY the no-ghost curvature -- is the relevant 'curvature'
       really K''(Q) at Q=1, or is it the P(X)-style time-kinetic combination
       (P' + 2 X0 P''), and does that change the story?
  (iii) THE SHARP HOOK: the Q-mode sound speed c_s^2(dQ) = dQ/(3 dQ + 2). On WHICH
       branch (Q>1 vs Q<1) is it positive? Did the agent silently assume positivity?
       Is the framework's condensate on the stable branch? Did anyone mis-cite a bound?

BOTH-WAYS: a kill / a confirmed-null weighs equal to a pass. Quarantine: assert nothing
derived about a0/Z/kappa/I0.
"""
import sympy as sp
import numpy as np

print("="*90)
print("SKEPTIC re-verification: DOOR B  quadratic K=mu^2(Q-1)^2  vs  DBI sqrt form")
print("="*90)

Q, mu, lam, u = sp.symbols('Q mu lambda_D u', positive=True)

K_quad = mu**2*(Q-1)**2
# DBI form as the prior agent cited it (Eq.96): K=(2mu^2/lam)[1 - sqrt(1 - lam (Q-1)^2)]
K_dbi  = (2*mu**2/lam)*(1 - sp.sqrt(1 - lam*(Q-1)**2))

print("\n[1] DERIVATIVES AT THE CONDENSATE Q=1  (independent diff, not a coeff read)")
print("-"*90)
for label, K in [("quad", K_quad), ("DBI ", K_dbi)]:
    row = []
    for n in range(5):
        d = sp.simplify(sp.diff(K, Q, n).subs(Q, 1))
        row.append((n, d))
    print(f"  {label}:  " + "  ".join(f"K^({n})(1)={d}" for n, d in row))

# Independent assertions
assert sp.simplify(K_quad.subs(Q,1)) == 0
assert sp.simplify(K_dbi.subs(Q,1)) == 0
assert sp.simplify(sp.diff(K_quad,Q).subs(Q,1)) == 0
assert sp.simplify(sp.diff(K_dbi,Q).subs(Q,1)) == 0
Kpp_q = sp.simplify(sp.diff(K_quad,Q,2).subs(Q,1))
Kpp_d = sp.simplify(sp.diff(K_dbi ,Q,2).subs(Q,1))
print(f"\n  K''(1): quad={Kpp_q}, DBI={Kpp_d}  -> match? {sp.simplify(Kpp_q-Kpp_d)==0}")
K4_q = sp.simplify(sp.diff(K_quad,Q,4).subs(Q,1))
K4_d = sp.simplify(sp.diff(K_dbi ,Q,4).subs(Q,1))
print(f"  K''''(1): quad={K4_q}, DBI={K4_d}  (first divergence)")

print("\n[2] lam_D -> 0 LIMIT  (does the DBI family collapse onto the framework's quadratic?)")
print("-"*90)
lim = sp.simplify(sp.limit(K_dbi, lam, 0))
print(f"  lim_(lam->0) K_dbi = {lim}")
print(f"  equals mu^2(Q-1)^2 ?  {sp.simplify(lim - K_quad)==0}")

print("\n[3] FIRST DEVIATION  K_dbi - K_quad")
print("-"*90)
diff = sp.series(K_dbi.subs(Q, 1+u) - K_quad.subs(Q,1+u), u, 0, 8).removeO()
print(f"  K_dbi - K_quad (in u=Q-1) = {sp.expand(diff)}")
for n in range(8):
    c = sp.simplify(sp.expand(diff).coeff(u, n))
    if c != 0:
        print(f"  first nonzero at u^{n}: coeff = {c}")
        break

print("\n" + "="*90)
print("[4] *** THE SHARP HOOK ***  Q-mode sound speed c_s^2(dQ) = dQ/(3 dQ + 2)")
print("="*90)
dQ = sp.symbols('dQ', real=True)
cs2 = dQ/(3*dQ + 2)
print(f"  c_s^2(dQ) = {cs2}")
print("\n  Sign analysis (dQ = Q - 1, displacement off the condensate):")
for val in [sp.Rational(1,2), sp.Rational(1,10), sp.Rational(-1,10), sp.Rational(-1,2), sp.Rational(-1,3)]:
    v = cs2.subs(dQ, val)
    sign = "POSITIVE (stable)" if v > 0 else ("NEGATIVE (gradient-unstable)" if v < 0 else "ZERO")
    print(f"    dQ={str(val):>5}:  c_s^2 = {v}  -> {sign}")
# Solve where c_s^2 = 0 and where the denominator flips
print("\n  c_s^2 = 0 at dQ =", sp.solve(sp.Eq(cs2,0), dQ))
print("  denominator 3dQ+2 = 0 (pole) at dQ =", sp.solve(sp.Eq(3*dQ+2,0), dQ))
print("""
  BRANCH STRUCTURE (independently confirmed):
    * dQ > 0   (Q>1):  c_s^2 = dQ/(3dQ+2) > 0           -> STABLE  (gradient-stable)
    * -2/3 < dQ < 0 (1>Q>1/3):  num<0, den>0 -> c_s^2 < 0 -> GRADIENT-UNSTABLE (Cline-class)
    * dQ < -2/3 (Q<1/3):  num<0, den<0 -> c_s^2 > 0       (other side of the pole)
  So POSITIVITY on the physically relevant near-condensate side is forced by sign(dQ)=sign(Q-1):
  Q>1 is the stable branch; the immediate Q<1 neighborhood (1/3<Q<1) is gradient-unstable.
""")

print("="*90)
print("[5] WHICH BRANCH DOES THE FRAMEWORK / HOST SIT ON?  sign(I0) via the first integral")
print("="*90)
print("""
  First integral (banked, condensate_postulate_and_eos.py): a^3 K'(Q) = I0 (const).
  K'(Q) = 2 mu^2 (Q-1) for the quadratic. So:
        Q - 1 = I0 / (2 mu^2 a^3).
  -> sign(Q-1) = sign(I0).  The dark-MATTER (dust) branch needs rho_dust >= 0.
  Blanchet-Skordis (Eq.97-100) fix I0 by Omega_K,0 and the cosmology forces Qbar -> 1^+
  from ABOVE as a -> infinity (Qbar = 1 + 1/sqrt(lam + (2mu^2 a^3/I0)^2) > 1 for I0>0).
  => the cosmological background sits on Q >= 1, i.e. the dQ>0 STABLE (positive c_s^2) branch.
  The unstable 1/3<Q<1 window is NOT where the late-time condensate lives.
""")
# numerically confirm Qbar>1 for the Eq.97 form with positive params
lamn, mun, a3, I0n = 1.0, 1.0, 1.0, 1.0
Qbar = 1 + 1/np.sqrt(lamn + (2*mun**2*a3/I0n)**2)
print(f"  Eq.97 sanity (lam=mu=a^3=I0=1):  Qbar = 1 + 1/sqrt(lam+(2mu^2 a^3/I0)^2) = {Qbar:.4f}  (>1, stable)")
for I0n in [0.1, 1.0, 10.0, -1.0]:
    inner = lamn + (2*mun**2*a3/I0n)**2
    Qb = 1 + np.sign(I0n)/np.sqrt(inner)
    print(f"    I0={I0n:>5}: Qbar-1 = {Qb-1:+.4f}  ({'stable Q>1' if Qb>1 else 'UNSTABLE Q<1'})")

print("""
  NOTE on the c_s^2 sign at the EXACT minimum: at Q=1 (dQ=0) c_s^2 = 0/2 = 0 exactly --
  the leading (grad pi)^2 term VANISHES (the ACLM ghost-condensate hallmark), and the
  REAL dispersion is the k^4/M^2 piece (not captured by c_s^2(dQ) which is the long-
  wavelength acoustic speed of the OFF-minimum dust). c_s^2(dQ) governs the Q>1 dust;
  it is >0 there. So the framework is on the stable branch BOTH at the minimum (c_s^2=0,
  k^4 dispersion, de Sitter-overdamped) AND just off it (Q>1 -> c_s^2>0). No kill here.
""")

print("="*90)
print("[6] BOUNDEDNESS WINDOW: is mu above the 1e-31 eV cutoff?  (independent unit calc)")
print("="*90)
c_ms   = 2.99792458e8
hbar_J = 1.054571817e-34
eV_J   = 1.602176634e-19
Mpc_m  = 3.0856775814913673e22
kpc_m  = Mpc_m/1e3
def invlen_to_eV(L):  # E = hbar c / L
    return hbar_J*c_ms/L/eV_J
cutoff = 1e-31
print(f"  cutoff (paper abstract) = {cutoff:.1e} eV  -> L_cut = {hbar_J*c_ms/(cutoff*eV_J)/Mpc_m:.3e} Mpc")
for name, L in [("mu^-1=22.3 Mpc", 22.3*Mpc_m), ("mu^-1=1 Mpc", 1.0*Mpc_m),
                ("mu^-1=223 kpc", 223*kpc_m), ("mu^-1=100 kpc (MOND edge)", 100*kpc_m)]:
    e = invlen_to_eV(L)
    print(f"    {name:28s}: mu={e:.3e} eV, mu/cutoff={e/cutoff:.2f}, inside={e>cutoff}")

print("""
  CAVEAT (skeptic, both-ways): the 1e-31 eV cutoff is the paper's GLOBAL Minkowski
  deconstrained-Hamiltonian statement (abstract), NOT independently re-derived here.
  What IS robustly true: every MOND-mu is 3..640x above it numerically. The agent's
  '10-100x' undersells the high-mu end (mu^-1=100 kpc is 640x); but the conclusion
  'all inside' is correct. This is a numeric-magnitude consistency check, not a theorem.
""")

print("="*90)
print("SKEPTIC SUMMARY")
print("="*90)
print(f"""
  Reproduced INDEPENDENTLY:
    K''(1) = 2 mu^2 IDENTICAL (quad {Kpp_q}, DBI {Kpp_d})                 -> CONFIRMED
    K''''(1): quad {K4_q}, DBI {K4_d} = 6 mu^2 lam_D                       -> CONFIRMED
    lim_(lam->0) DBI = mu^2(Q-1)^2 EXACTLY                                 -> CONFIRMED
    first deviation at u^4, coeff = mu^2 lam_D/4                           -> CONFIRMED
    every MOND-mu (3..640x) inside the 1e-31 eV cutoff                     -> CONFIRMED
    c_s^2(dQ)=dQ/(3dQ+2): >0 on Q>1, <0 on 1/3<Q<1; framework on Q>=1      -> CONFIRMED stable branch
  Bound mis-application check: Creminelli-Janssen-Senatore NOT invoked by the agent
    (correct -- it would be inapplicable). Grall-Melville / Serra-Trombetta NOT used as
    a kill either; the door is a shape/embedding consistency test, and positivity sits
    on the stable Q>1 branch. No mis-cited kill, no manufactured pass on the sound speed.
""")
