#!/usr/bin/env python3
"""G2: PT-reality of the minimal PU+a0 modified-inertia model.

Model (preferred frame = CMB rest):
  L = (m/2) xdot^2 - (m a0^2 / (2 w^2)) k(y) - m Phi(x),   y = |xddot|^2/a0^2
  k(y) -> y as y->0 recovers the pure PU term -(m/2w^2) xddot^2.
Choices tested:
  k_sat(y) = y/(1+y)          (saturating: Newtonian at high a BY CONSTRUCTION, PU at low a)
  k_tail(y) = y + 2 beta sqrt(y)  (tail-matching: reproduces framework 1-mu ~ a0/2a exponent)
Quadratic PU facts per Bender & Mannheim PRL 100, 110402 (2008); equal-frequency
danger per Bender & Mannheim J.Phys.A 41, 244005 (2008); benign/malicious per
Smilga Nucl.Phys.B 706 (2005) 598, J.Phys.A 42 (2009) 155208.
"""
import sympy as sp
import numpy as np

m, w, W0, A, t, a0s = sp.symbols('m w Omega0 A t a0', positive=True)
om = sp.symbols('omega')

# ---- 1. PU-in-a-well spectrum: x'''' + w^2 x'' + w^2 W0^2 x = 0
char = om**4 - w**2*om**2 + w**2*W0**2
r1, r2 = sp.solve(char, om**2)
assert sp.simplify(r1 + r2 - w**2) == 0 and sp.simplify(r1*r2 - w**2*W0**2) == 0
disc = w**4 - 4*w**2*W0**2   # real, distinct frequencies iff disc>0  <=> w > 2*W0
w_EP = sp.solve(sp.Eq(disc, 0), w)
print("PU frequencies^2:", r1, "|", r2)
print("Exceptional (Jordan) point: w =", [s for s in w_EP if s != 0], " (w=2*Omega0)")
# broken phase w<2W0: omega^2 complex-conjugate pair -> complex energies = broken PT
w_num, W0_num = 1.8, 1.0
rts = np.roots([1, 0, w_num**2, 0, w_num**2*W0_num**2])  # lambda^4+w^2 lambda^2+w^2W0^2 (x~e^{lam t})
maxRe = max(rts.real)
assert maxRe > 0.1, "w<2W0 must give growing mode (broken PT / complex omega)"
print(f"w=1.8 W0: max Re(lambda) = {maxRe:.4f} W0  -> BROKEN (exp growth)")

# ---- 2. Ghost assignment: Ostrogradsky energy of the fast mode of L0
xf = sp.Function('x')(t)
v1, a1, j1 = sp.symbols('v1 a1 j1')  # placeholders for xdot, xddot, xdddot
L0g = m*v1**2/2 - m*a1**2/(2*w**2)
px_g = sp.diff(L0g, v1) - j1*sp.diff(sp.diff(L0g, a1), a1)  # p_x = dL/dv - d/dt(dL/da); dL/da linear in a
pv_g = sp.diff(L0g, a1)
E_g = v1*px_g + a1*pv_g - L0g
x = A*sp.cos(w*t)
sub = {v1: sp.diff(x,t), a1: sp.diff(x,t,2), j1: sp.diff(x,t,3)}
E = sp.simplify(E_g.subs(sub))
assert sp.simplify(E + m*A**2*w**2/2) == 0
print("Fast-mode Ostrogradsky energy:", E, " (< 0: the w-mode is the classical ghost; BM PT-cure targets it)")

# ---- 3. PT-evenness of L_int: under P: x->-x (xdd->-xdd); T: t->-t (xdd->+xdd) => PT: xdd->-xdd
# any k(xdd^2) is PT-even.  (symbolic bookkeeping)
xdd = sp.symbols('xdd')
for kfun in [xdd**2, xdd**2/(1+xdd**2), sp.sqrt(xdd**2)]:
    assert sp.simplify(kfun.subs(xdd, -xdd) - kfun) == 0
print("L_int = k(xdd^2): PT-even for all candidates -> perturbative reality criterion available")
print("  (PT-even V + unbroken nondegenerate H0 => real corrections order-by-order,")
print("   Caliceti-Graffi-Maioli-type argument; nonperturbative benignity = Smilga caveat, UNDETERMINED)")

# ---- 4. Sign of the induced quartic ghost self-interaction (Smilga risk flag)
c2 = sp.symbols('c2', positive=True); pvs = sp.symbols('pv')
La = -(m*a0s**2/(2*w**2))*( (xdd**2/a0s**2) - c2*(xdd**2/a0s**2)**2 )  # k = y - c2 y^2 (saturating expansion)
pv_of_a = sp.expand(sp.diff(La, xdd))          # = -(m/w^2) xdd + (2 c2 m/(w^2 a0^2)) xdd^3
# series inversion (fixed point to O(pv^3)):  xdd = -(w^2/m) pv + (2 c2/a0^2) xdd^3
a_lead = -(w**2/m)*pvs
a_inv = a_lead + (2*c2/a0s**2)*a_lead**3
resid = sp.expand(pv_of_a.subs(xdd, a_inv) - pvs).series(pvs, 0, 4).removeO()
assert sp.simplify(resid.coeff(pvs,1)) == 0 and sp.simplify(resid.coeff(pvs,3)) == 0, "inversion wrong at O(pv^3)"
Ha = sp.expand(pvs*a_inv - La.subs(xdd, a_inv)).series(pvs, 0, 5).removeO()
q2 = sp.simplify(Ha.coeff(pvs, 2)); q4 = sp.simplify(Ha.coeff(pvs, 4))
print("H_a(p_v) = (", q2, ") p_v^2 + (", q4, ") p_v^4 + ...")
assert sp.simplify(q2 + w**2/(2*m)) == 0
print("  quadratic: -(w^2/2m) p_v^2 (standard indefinite PU); quartic coeff sign:",
      sp.sign(q4.subs({m:1,w:1,a0s:1,c2:1})), " (negative => ghost-momentum self-attraction: Smilga-malicious RISK)")

# ---- 5. Where does MOND live in the frequency ratio?  Exact circular-orbit identity gives
#   mu_eff = 1 - (Omega/w_eff)^2,  w_eff^2 = w^2/k'(y)  (transverse);  PT-real needs w_eff >= 2*Omega
#   => softening cap in the UNBROKEN phase:  mu_eff >= 1 - 1/4 = 3/4  (harmonic-well threshold; O(1) epicyclic factor for disks)
print("\nTHEOREM (quadratic level): unbroken PT  <=>  w_eff >= 2 Omega  <=>  mu_eff >= 3/4.")
xx = sp.symbols('x', positive=True)
mu_fw = (sp.sqrt(1+4*xx**2)-1)/(2*xx)            # framework mu(a/a0), from g_obs=sqrt(gb^2+gb*a0)
x_cap = sp.solve(sp.Eq(mu_fw, sp.Rational(3,4)), xx)
print("  framework mu_fw(a/a0)=3/4 at a =", x_cap, "* a0  => ENTIRE g_bar < ~1.3 a0 regime is past the EP.")

# MOND-tuned numbers (saturating k, full-|xddot| EFE reading), MW edge: a=0.7a0, v=200 km/s
a0n, v = 9.36e-11, 2.0e5
kp = lambda y: 1.0/(1.0+y)**2
aMW = 0.7*a0n; OmMW = aMW/v; muT = float(mu_fw.subs(xx, 0.7))
w_tuned = OmMW*np.sqrt(kp(0.7**2)/(1.0-muT))
print(f"  MOND-on tuning: w = {w_tuned:.2e} s^-1 (~{w_tuned/2.27e-18:.0f} H0); mu(0.7a0)={muT:.3f}")
# broken window on the MW curve: r(a)=w_eff/(2*Omega)=1
from scipy.optimize import brentq
r = lambda a_: (w_tuned*(1+(a_/a0n)**2))/(2*(a_/v))
lo = brentq(lambda a_: r(a_)-1, 1e-3*a0n, 0.7*a0n); hi = brentq(lambda a_: r(a_)-1, 0.7*a0n, 50*a0n)
print(f"  broken-PT window on MW curve: a in [{lo/a0n:.2f}, {hi/a0n:.2f}] a0  == the MOND window itself")
assert lo < 0.7*a0n < hi
print("\nG2 VERDICT: unbroken-PT plausible ONLY where mu_eff>=3/4 (Newtonian side);")
print("a->0 maps w_eff/2Omega BELOW 1: deep MOND sits past the Jordan block, in the BROKEN-PT/complex-frequency zone.")
print("EXIT 0")
