#!/usr/bin/env python3
"""a03_egb_and_data.py -- adversarial audit of p03 (corrected 4D-EGB temperature; SPARC-amplitude table).

Independent methods:
 T1  first-law route: M(r_h) = (r_h^2 + alpha)/(2 r_h); entropy S(r_h) = pi r_h^2 + 4 pi alpha ln r_h (Wald/JM of the 4D-EGB action; the log is the D->4 limit);
     T = dM/dS.  This never uses f'(r_h) and so cannot share an error with p03's E2.  Compare with p03's T = (r^2 - alpha)/(4 pi r (r^2 + 2 alpha)).
 T2  direct high-precision numerical differentiation of the FULL metric function (mpmath) at fixed seeds (p03 used unseeded random points).
 T3  maximise kappa = 2 pi T with mpmath.findroot and compare kappa_max^2 alpha with 0.016368 and with 1/32.
 T4  the old (wrong) temperature T_old = r/(4 pi (r^2 + 2 alpha)) DOES have a maximum at r = sqrt(2 alpha) with kappa^2 alpha = 1/32 -- the 'lead' was an artefact
     of the misremembered formula, so the retraction is right; and p03's docstring still describes the OLD formula (stale text).
 D1  recompute the sigma-offset table for BOTH footings, and the H0-sensitivity (H0 = 67.4 vs 73.0).  Also test the README sentence
     'On the rho_Lambda footing all sit 2.4-3.7 sigma low' against the table.
Exit 0 = the checks held (they include a check that the README sentence about the rho_Lambda footing is WRONG for the Nariai-shell candidate).
"""
import math, sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- T1 first law
r, al = sp.symbols('r alpha', positive=True)
M = (r**2 + al) / (2 * r)
S = sp.pi * r**2 + 4 * sp.pi * al * sp.log(r)
T_first = sp.simplify(sp.diff(M, r) / sp.diff(S, r))
T_p03 = (r**2 - al) / (4 * sp.pi * r * (r**2 + 2 * al))
chk("T1 first law T = dM/dS with S = pi r^2 + 4 pi alpha ln r reproduces p03's corrected T = (r^2 - alpha)/(4 pi r (r^2 + 2 alpha))", sp.simplify(T_first - T_p03) == 0)

# ---------------------------------------------------------------- T2 numerical derivative of the full metric (seeded points)
def f_full(x, a, Mv):
    return 1 + x**2 / (2 * a) * (1 - mp.sqrt(1 + 8 * a * Mv / x**3))
worst = 0
for (rh, a) in [(1.7, 0.4), (3.3, 0.9), (2.2, 0.05), (5.0, 2.0), (1.3, 0.3)]:
    rh = mp.mpf(rh); a = mp.mpf(a)
    Mv = (rh**2 + a) / (2 * rh)
    assert abs(f_full(rh, a, Mv)) < mp.mpf(10)**(-30)
    fp = mp.diff(lambda x: f_full(x, a, Mv), rh)
    worst = max(worst, abs(fp / (4 * mp.pi) - (rh**2 - a) / (4 * mp.pi * rh * (rh**2 + 2 * a))))
chk("T2 numerical f'(r_h)/(4 pi) from the full metric agrees with T_p03 at 5 fixed points (max |err| = %.1e)" % float(worst), worst < mp.mpf(10)**(-25))

# ---------------------------------------------------------------- T3 maximum of kappa
kap = lambda x, a: (x**2 - a) / (2 * x * (x**2 + 2 * a))
xs = mp.findroot(lambda x: mp.diff(lambda y: kap(y, 1), x), 2.3)
kmax2 = kap(xs, 1)**2
print("   r_h^2/alpha at the maximum = %s ; (5+sqrt 33)/2 = %s ; kappa_max^2 alpha = %s ; 1/32 = %s" % (mp.nstr(xs**2, 12), mp.nstr((5 + mp.sqrt(33)) / 2, 12), mp.nstr(kmax2, 10), mp.nstr(mp.mpf(1) / 32, 10)))
chk("T3 kappa_max^2 alpha = %.6f, max at r_h^2 = alpha (5 + sqrt 33)/2 (independent numerical maximisation)" % float(kmax2),
    abs(xs**2 - (5 + mp.sqrt(33)) / 2) < mp.mpf(10)**(-25) and abs(kmax2 - mp.mpf('0.016368')) < mp.mpf('1e-5'))
# closed form
x0 = (5 + sp.sqrt(33)) / 2
kclosed = sp.simplify((x0 - 1)**2 / (4 * x0 * (x0 + 2)**2))
chk("T3b closed form kappa_max^2 alpha = (x0-1)^2/(4 x0 (x0+2)^2), x0 = (5+sqrt33)/2, = %.6f != 1/32" % float(kclosed), abs(float(kclosed) - 1 / 32) > 0.01 and abs(float(kclosed) - float(kmax2)) < 1e-9)
# ---------------------------------------------------------------- T4 the old formula
kold = lambda x, a: x / (2 * (x**2 + 2 * a))          # kappa = 2 pi T_old = r/(2 (r^2 + 2 alpha))
xo = mp.findroot(lambda x: mp.diff(lambda y: kold(y, 1), x), 1.3)
chk("T4 the OLD (misremembered) temperature has its maximum at r = sqrt(2 alpha) with kappa^2 alpha = 1/32 exactly: the retracted 'lead' was an artefact, retraction is correct",
    abs(xo**2 - 2) < mp.mpf(10)**(-25) and abs(kold(xo, 1)**2 - mp.mpf(1) / 32) < mp.mpf(10)**(-25))
print("   NOTE: p03's docstring still lists the OLD formula in E2/E3 ('T = r_h/(4 pi (r_h^2+2 alpha))', 'kappa_max^2 = 1/(32 alpha)') -- stale text contradicting the code and .out")

# ---------------------------------------------------------------- K1 the README's 'checked by hand' Kounterterm / Jacobson-Myers statement (not scripted in p03)
Ls = sp.symbols('L', positive=True); alK = sp.symbols('alpha_K', real=True)
Vol4 = sp.Rational(8, 3) * sp.pi**2 * Ls**4
I_E = -(1 / (16 * sp.pi)) * ((12 / Ls**2 - 2 * 3 / Ls**2) * Vol4 + alK * 64 * sp.pi**2)      # -(1/16 pi) Int (R - 2 Lambda + alpha E4) on S^4(L), Int E4 = 64 pi^2
al_kt = sp.solve(sp.Eq(I_E, 0), alK)[0]
A_ = sp.symbols('A', positive=True)
S_JM = A_ / 4 + (alK / 2) * 8 * sp.pi                       # Jacobson-Myers: (1/4) Int (1 + 2 alpha R_h) dA on a round S^2 (Int R_h dA = 8 pi)
chk("K1 Kounterterm coefficient (vanishing on-shell S^4 action) alpha = -L^2/4, and S_JM = A/4 + 4 pi alpha vanishes at A = 4 pi L^2 (the dS horizon area), as README section 5 states (recomputed here; p03 only scripts alpha = -3/(4 Lambda))",
    sp.simplify(al_kt + Ls**2 / 4) == 0 and sp.simplify(S_JM.subs({alK: al_kt, A_: 4 * sp.pi * Ls**2})) == 0)

# ---------------------------------------------------------------- D1 footings
c = 2.99792458e8
Mpc = 3.0856775814913673e22
a0_hat, sig = 1.0766e-10, 0.0544
OmL = 0.685
def table(H0kms):
    H0 = H0kms * 1e3 / Mpc
    out = {}
    for nm, Zc in [("Milgrom 2 pi", 2 * math.pi), ("Verlinde 6", 6.0), ("framework sqrt(32pi/3)", math.sqrt(32 * math.pi / 3)), ("Nariai-shell 3 sqrt 3", 3 * math.sqrt(3))]:
        out[nm] = ((c * H0 / Zc - a0_hat) / (sig * a0_hat), (c * H0 * math.sqrt(OmL) / Zc - a0_hat) / (sig * a0_hat))
    return out
t674 = table(67.4); t730 = table(73.0)
print("   %-26s %10s %10s | %10s %10s   (offset in sigma of the SPARC fit; sigma = 5.44%% statistical)" % ("coefficient", "H0 foot.", "H_L foot.", "H0=73 tot", "H0=73 L"))
for nm in t674:
    print("   %-26s %+9.2f  %+9.2f  | %+9.2f  %+9.2f" % (nm, t674[nm][0], t674[nm][1], t730[nm][0], t730[nm][1]))
low = [nm for nm in t674 if t674[nm][1] < -2.0]
chk("D1 on the rho_Lambda (H_L) footing exactly THREE candidates sit 2.4-3.7 sigma low; the Nariai-shell 3 sqrt3 is at %+.2f sigma, i.e. WITHIN 1 sigma -- README section 6 says 'all sit 2.4-3.7 sigma low' (wrong for that candidate)" % t674["Nariai-shell 3 sqrt 3"][1],
    len(low) == 3 and abs(t674["Nariai-shell 3 sqrt 3"][1]) < 1.0)
chk("D2 H0 sensitivity: moving H0 from 67.4 to 73.0 raises every H0-footing offset by ~1.5-1.8 sigma; the framework moves from %+.2f to %+.2f sigma (outside 2 sigma) and Milgrom from %+.2f to %+.2f (the 'three of four within 1 sigma' statement is footing- AND H0-dependent)" %
    (t674["framework sqrt(32pi/3)"][0], t730["framework sqrt(32pi/3)"][0], t674["Milgrom 2 pi"][0], t730["Milgrom 2 pi"][0]),
    t730["framework sqrt(32pi/3)"][0] > 2.0 and abs(t730["Milgrom 2 pi"][0]) < 1.0 and all(1.4 < t730[k][0] - t674[k][0] < 1.9 for k in t674))
# matches p03's printed numbers?
chk("D3 reproduces p03's table (Milgrom -0.59, Verlinde +0.25, framework +0.93, Nariai +3.14 on H0; -3.65, -2.96, -2.40, -0.57 on H_L)",
    all(abs(a - b) < 0.006 for a, b in zip([t674[k][0] for k in t674] + [t674[k][1] for k in t674], [-0.59, 0.25, 0.93, 3.14, -3.65, -2.96, -2.40, -0.57])))
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
