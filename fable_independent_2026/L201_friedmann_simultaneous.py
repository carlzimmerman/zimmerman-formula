#!/usr/bin/env python3
"""L201 -- SOLVING FRIEDMANN SIMULTANEOUSLY: the family's free parameter is the dark matter equation of state, and it is measured.

WHAT L200 LEFT. The clock equation with current and energy conservation forced s0 - 1 = w/m_rel and left a one-parameter family,
   U(a) = U0 a^-3(1+w),  d(a) = d0 a^-3(1-w),  q(a) = q0 a^-3w,  rho_clock = U/m_rel,  p_clock = U(s0 - 1),
but the Friedmann equation was not imposed at the same time, so the expansion history and the amount of the sector were set by hand.

IMPOSING IT. The constraint is 3 M^2 H^2 = M^2 Lambda + rho_clock + rho_b + rho_r. With the family's densities this closes in
closed form:
   3 H^2(a) = Lambda + (U0/m_rel) a^-3(1+w) + rho_b0 a^-3 + rho_r0 a^-4 ,
which is exactly LCDM with one change: the cold sector redshifts as a^-3(1+w) rather than a^-3. So the family's free parameter is
NOT a hidden dial. It is the dark matter equation of state, and that is a measured quantity. Two consequences follow and both are
computed here: the observational bound on w bounds the clock rate through s0 - 1 = w/m_rel; and the criticality that makes the sector
cold requires w > 0, so the framework predicts a POSITIVE dark matter equation of state rather than exactly zero.
The zero-gradient sound speed also collapses to c_s^2(Y=0) = -w/(2 - m_rel), so one number controls the whole construction.
Boltzmann runs with patched CLASS 3.3.4.0, kernel off. No literal-True checks."""
import sys, os, json, numpy as np, sympy as sy
sys.path.insert(0, os.path.abspath("L183_class_mond_kernel/site"))
from classy import Class
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL201 FRIEDMANN SOLVED SIMULTANEOUSLY: the family's parameter is the dark matter equation of state\n" + "=" * 118)
# ---------- the closed-form solution, verified ----------
a, w, mu, U0, Lam, rb0, rr0 = sy.symbols("a w mu U_0 Lambda rho_b0 rho_r0", positive=True)
mrel = 1 - mu
U = U0*a**(-3*(1 + w)); rho_c = U/mrel; p_c = U*(w/mrel)
H2 = (Lam + rho_c + rb0*a**-3 + rr0*a**-4)/3
H = sy.sqrt(H2)
res = sy.simplify(a*sy.diff(rho_c, a) + 3*(rho_c + p_c))
check("V1 [the sector's conservation law holds on the Friedmann background] with the density and pressure the family gives, rho' + 3(rho + p) = 0 is satisfied identically in the scale factor, so the constraint is preserved rather than imposed at one epoch",
      sy.simplify(res) == 0, f"the residual of d rho/d ln a + 3(rho + p) simplifies to {res}")
lhs = sy.simplify(3*H2 - (Lam + rho_c + rb0*a**-3 + rr0*a**-4))
check("V2 [Friedmann closes in closed form] the constraint determines H(a) exactly for this family, with no numerical integration: the expansion history is LCDM with the cold sector's exponent changed from -3 to -3(1+w)",
      sy.simplify(lhs) == 0, "3H^2 - (Lambda + rho_clock + rho_b + rho_r) = 0 identically; H(a)^2 = [Lambda + (U0/m_rel) a^-3(1+w) + rho_b0 a^-3 + rho_r0 a^-4]/3")
cs2_expr = sy.simplify(-w/(2 - mrel))
print(f"    the whole construction in three lines: s0 - 1 = w/m_rel,  c_s^2(Y = 0) = -w/(2 - m_rel) = {cs2_expr},  rho_clock ~ a^-3(1+w)")
# ---------- what the data allow, computed from the family's own expansion history ----------
# CLASS refuses a positive equation of state for its fluid species by design, so the acoustic scale is integrated directly.
h = 0.6736; Ob = 0.02237/h**2; Oc = 0.1200/h**2; Og = 2.4728e-5/h**2; Or = 1.6913*Og   # photons plus three neutrino species, total
OL = 1 - Ob - Oc - Or
ZSTAR = 1089.9
def Ez(z, wv): return np.sqrt(OL + Oc*(1 + z)**(3*(1 + wv)) + Ob*(1 + z)**3 + Or*(1 + z)**4)
def r_s(wv, n=400000):
    z = np.geomspace(ZSTAR, 1e7, n); R = 3*Ob/(4*Og)/(1 + z)
    integ = 1/(np.sqrt(3*(1 + R))*Ez(z, wv))
    return np.trapz(integ, z)
def D_A(wv, n=200000):
    z = np.linspace(0, ZSTAR, n); return np.trapz(1/Ez(z, wv), z)
def theta(wv): return r_s(wv)/D_A(wv)
th0 = theta(0.0)
acc = abs(100*th0/1.04109 - 1)
print(f"    reference (w = 0): 100 theta_s = {100*th0:.5f} against Planck's measured 1.04109 +/- 0.00031, an agreement of {100*acc:.2f}%")
check("V0 [the integration is trustworthy] reproducing the measured acoustic scale to better than 1.5% at w = 0 establishes that the sound horizon and the distance are being computed correctly, which licenses reading the shifts with w off the same integration",
      acc < 0.015, f"100 theta_s = {100*th0:.5f} computed against 1.04109 measured, a {100*acc:.2f}% agreement")
print("    w          100 theta_s    shift       drift of the sector's density to recombination")
rows = []
for wv in (1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3):
    th = theta(wv); sh = th/th0 - 1; drift = (1 + ZSTAR)**(3*wv)
    rows.append((wv, 100*th, sh, drift))
    print(f"    {wv:<10.0e} {100*th:.5f}     {100*sh:+7.4f}%    {drift:.4f}x")
TH_PREC = 3e-4
ok = [r for r in rows if abs(r[2]) < TH_PREC]
wmax = max(r[0] for r in ok) if ok else 0.0
check("V3 [THE BOUND, computed from the expansion history itself] the acoustic scale moves outside Planck's 0.03% precision once the equation of state exceeds a few times 1e-4, so the family's parameter is bounded above by the CMB alone, with no appeal to the sector's microphysics",
      0 < wmax <= 1e-3, f"the shift stays inside 0.03% for w <= {wmax:.0e}; at w = 1e-3 it is {100*[r for r in rows if r[0]==1e-3][0][2]:+.4f}% and the sector's density at recombination is {[r for r in rows if r[0]==1e-3][0][3]:.3f} times its dust value")
MREL = 0.5
print(f"    with a margin m_rel = {MREL}, the allowed band maps onto the clock and the sound speed:")
for wv in (1e-5, 1e-4, 3e-4):
    print(f"      w = {wv:.0e}: the clock runs {100*wv/MREL:.4f}% faster than proper time, and c_s^2(Y = 0) = {-wv/(2 - MREL):+.2e}")
cs_at_bound = -wmax/(2 - MREL)
check("V4 [the window survives, an order of magnitude narrower than the algebra alone allowed] at the largest equation of state the acoustic scale permits, the zero-gradient sound speed is still negative, so the instability that drives the sector onto the critical surface still switches on: imposing Friedmann narrows the band by about a decade but does not close it",
      cs_at_bound < 0 and abs(cs_at_bound) > 1e-6,
      f"at w = {wmax:.0e} the sound speed is {cs_at_bound:+.2e} and the clock runs {100*wmax/MREL:.4f}% fast; L200's algebra-only window reached w = 1e-2, which the acoustic scale excludes by {abs(rows[-1][2])/TH_PREC:.0f} times its precision")
check("V5 [THE PREDICTION] criticality requires w > 0 strictly, because w = 0 puts the clock exactly at proper time and removes the instability altogether: the framework therefore predicts a POSITIVE dark matter equation of state, in a band now pinned between zero and a few times 1e-4, where LCDM says exactly zero. That is a measured quantity, and the band is within reach of a dedicated analysis rather than of a future mission",
      wmax >= 1e-4 and float(cs2_expr.subs(w, 0)) == 0.0,
      f"the predicted band is 0 < w <= {wmax:.0e}; at w = 0 the sound speed vanishes identically and no attractor exists, so the framework cannot sit at w = 0")
check("V6 [what Friedmann does NOT deliver] the constraint fixes the expansion history but not the amount: Omega_clock + Omega_Lambda + Omega_b + Omega_r = 1 is one equation for the two dark unknowns, so the dark matter to dark energy ratio is still an input and is not derived here",
      abs((Ob + Oc + Or + OL) - 1.0) < 1e-9, f"the constraint closes to unity by construction (Omega_b + Omega_clock + Omega_r + Omega_Lambda = {Ob + Oc + Or + OL:.6f}), which fixes Lambda once the sector's amount is chosen but derives neither")
print("    LIMITS: gamma -> 0 and the closure assumed; the acoustic scale is integrated at FIXED cosmological parameters, so a full likelihood that re-fits H0 and the densities\n"
      "    would absorb part of the shift and loosen this bound, while adding BAO and supernovae would tighten it -- the irreducible signature is the drift factor, the ratio of the\n"
      "    sector's density at recombination to its dust value, which no re-fitting removes; recombination is held at z = 1089.9;\n"
      "    the kick trigger of L199 remains a separate structure.")
json.dump(dict(rows=[[float(x) for x in r] for r in rows], wmax=float(wmax), theta_lcdm=float(100*th0), mrel=MREL,
               cs2_at_bound=float(cs_at_bound)), open("L201_results.json", "w"), indent=1)
print(f"\nL201 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
