#!/usr/bin/env python3
"""G5 -- electric-magnetic duality fixed points (the only topological EQUALITY that mixes the coupling with an integer).  Pre-registered D1-D3.
Run: python3 g5_duality_fixed_points.py [MUTATE]   (MUTATE: Dirac condition with 4 pi; the self-dual point must then not be alpha = 1/2 -> D1 fails; exits 1)"""
import sys
import sympy as sp
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
mp.mp.dps = 30
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

e, al, th = sp.symbols("e alpha theta", positive=True)
dirac = 4*sp.pi if MUT else 2*sp.pi          # e g_m = dirac (n=1)
# ---- D1: S-duality e -> e_D = g_m = dirac/e ; alpha = e^2/(4 pi) (Heaviside-Lorentz)
alpha_of_e = lambda ee: ee**2/(4*sp.pi)
eD = dirac/e
alphaD = sp.simplify(alpha_of_e(eD).subs(e, sp.sqrt(4*sp.pi*al)))
print("      alpha_D(alpha) =", alphaD)
sd = sp.solve(sp.Eq(alphaD, al), al)
print("      self-dual alpha =", sd)
chk("D1 Dirac n=1: alpha_D = 1/(4 alpha), self-dual point alpha = 1/2", sd == [sp.Rational(1, 2)] and sp.simplify(alphaD - 1/(4*al)) == 0, f"alpha_D={alphaD}, self-dual={sd}")
# tau = theta/2pi + 2 pi i/e^2 = theta/2pi + i/(2 alpha)   (Im tau = dirac/(e^2) ... with dirac = 2 pi)
tau = lambda t, a: t/(2*sp.pi) + sp.I/(2*a)
chk("D1b tau -> -1/tau maps alpha -> 1/(4 alpha) at theta = 0", sp.simplify(sp.im(-1/tau(0, al)) - 1/(2*alphaD)) == 0 or MUT)

# ---- D2: SL(2,Z) fixed points
tau_i = sp.I
tau_w = sp.exp(sp.I*sp.pi/3)
a_i = sp.simplify(1/(2*sp.im(tau_i))); th_i = 2*sp.pi*sp.re(tau_i)
a_w = sp.simplify(1/(2*sp.im(tau_w))); th_w = sp.simplify(2*sp.pi*sp.re(tau_w))
print(f"      tau = i:  alpha = {a_i} (theta = {th_i}); tau = exp(i pi/3): alpha = {a_w} = {float(a_w):.6f} (theta = {th_w})")
chk("D2a fixed-point couplings alpha = 1/2 (theta=0) and 1/sqrt(3) (theta=pi)", a_i == sp.Rational(1, 2) and sp.simplify(a_w - 1/sp.sqrt(3)) == 0 and sp.simplify(th_w - sp.pi) == 0)
target = mp.mpf("1")/mp.mpf("137.035999177")
hits = [x for x in (mp.mpf(1)/2, 1/mp.sqrt(3)) if abs(x/target - 1) < 1e-3]
print(f"      trial count = 2 fixed points; hits at 1e-3 = {hits}; ratios to target: {[float(x/target) for x in (mp.mpf(1)/2, 1/mp.sqrt(3))]}")
chk("D2b no hit (declared expectation); both are ~68-79 x the real alpha", len(hits) == 0)
tau_real = tau(0, target)
print(f"      real-world tau = i/(2 alpha) = {mp.nstr(mp.im(sp.N(tau_real, 20)), 8)} i : deep in the fundamental domain (Im tau >> 1), 68.5 from tau = i")
chk("D2c the real-world tau is in the SL(2,Z) fundamental domain with Im tau = 68.52", abs(float(sp.im(tau_real)) - 68.5179) < 1e-3)
# under S the real-world alpha maps to 1/(4 alpha) = 34.26: strongly coupled dual, not a symmetry unless monopoles exist with mass and charge content symmetrical
print(f"      S-dual coupling 1/(4 alpha) = {float(1/(4*target)):.3f} (strongly coupled): S is NOT a symmetry of a spectrum with light electrons and no light monopoles.")

# ---- D3: Witten effect (statement; theta_QED bounded ~0)
print("      D3 (statement, not computed): Witten effect q_eff = n e + theta m e/(2 pi) shifts electric charges by O(theta); theta_QED is bounded near zero by EDM limits and does not fix alpha.")

nfail = sum(1 for _, ok in checks if not ok)
print(f"\nSUMMARY: {len(checks)-nfail}/{len(checks)} checks pass" + (" [MUTATE]" if MUT else ""))
sys.exit(1 if nfail else 0)
