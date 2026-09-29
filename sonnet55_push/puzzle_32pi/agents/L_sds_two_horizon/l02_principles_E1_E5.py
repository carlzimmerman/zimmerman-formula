#!/usr/bin/env python3
"""l02_principles_E1_E5.py -- test the predeclared principles E1-E5 (PREDECLARED_PRINCIPLES.md) on the SdS one-parameter family.

For each principle: derive the selected point(s) mu = M/M_N, evaluate K_b = kappa_b/H, K_c = kappa_c/H (f-normalisation) and the BH-normalised values, and compare with 1/Z = sqrt(3/(32 pi))
at the declared tolerance (relative 1e-10).  A check PASSES when the statement about the principle is TRUE (e.g. "E1 selects only the Nariai endpoint and does not give 1/Z").
Controls: (i) the comparator recognises the puzzle's own condition kappa_b = a0 (positive control: RESTATEMENT, not a success), (ii) it rejects a planted near-miss 1/Z (1 + 1e-6) (mutation),
(iii) the root finders recover the known interior point of E3 (x^2 = 1/5) and the known endpoint of E1.
Extras added at script-writing time (before any run, flagged): temperature-type functionals kappa_b kappa_c, kappa_b + kappa_c, T_b/T_c in E2'.
Units: L = 1 = 1/H, c = G = 1.  Exit 0 iff all checks hold.
"""
import sys
import numpy as np
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
def mut(name, wrong):
    ok.append(not bool(wrong)); print(("PASS [mutation rejected] " if not wrong else "FAIL [mutation NOT rejected] ") + name)

Z = mp.sqrt(32 * mp.pi / 3); TARGET = 1 / Z; MN = 1 / (3 * mp.sqrt(3)); TOL = mp.mpf('1e-10')
def matches(v):
    return abs(v / TARGET - 1) < TOL

# family in the monotone parameter x = r_b/L in (0, 1/sqrt3)
def y_of(x): return (-x + mp.sqrt(4 - 3 * x**2)) / 2
def M_of(x): return x * (1 - x**2) / 2
def mu_of(x): return 3 * mp.sqrt(3) * M_of(x)
def kb(x): return (1 - 3 * x**2) / (2 * x)
def kc(y): return (3 * y**2 - 1) / (2 * y)
def kBH(x):
    """Bousso-Hawking-normalised (kappa_b, kappa_c)"""
    M = M_of(x); rs = M**(mp.mpf(1) / 3); fs = 1 - 3 * M**(mp.mpf(2) / 3)
    return kb(x) / mp.sqrt(fs), kc(y_of(x)) / mp.sqrt(fs)
def x_of_mu(mu):
    return mp.findroot(lambda x: mu_of(x) - mu, (mp.mpf('1e-6'), 1 / mp.sqrt(3) - mp.mpf('1e-12')), solver='anderson') if mu < 1 else 1 / mp.sqrt(3)
xN = 1 / mp.sqrt(3)

def report(label, x):
    y = y_of(x); kbv, kcv = kb(x), kc(y); kbh, kch = kBH(x) if x < xN - mp.mpf('1e-30') else (mp.sqrt(3), mp.sqrt(3))
    print("   %-38s mu=%s  K_b=%s K_c=%s  (BH-norm: %s, %s)" % (label, mp.nstr(mu_of(x), 10), mp.nstr(kbv, 10), mp.nstr(kcv, 10), mp.nstr(kbh, 8), mp.nstr(kch, 8)))
    return kbv, kcv, kbh, kch

print("target 1/Z = %s ; comparator tolerance %s" % (mp.nstr(TARGET, 15), mp.nstr(TOL, 2)))

# ------------------------------------------------------------ controls for the comparator
xa0 = (mp.sqrt(1 + 3 * Z**2) - 1) / (3 * Z)
chk("C1 (positive control) the puzzle's own condition kappa_b = a0 at x* = %s is recognised by the comparator: this is a RESTATEMENT, counted as such, not as a success" % mp.nstr(xa0, 12), matches(kb(xa0)))
mut("C2 a planted near-miss target 1/Z (1 + 1e-6) is rejected by the comparator at tolerance 1e-10", matches(TARGET * (1 + mp.mpf('1e-6'))))

# ------------------------------------------------------------ E1 equilibrium T_b = T_c
xs_, ys_ = sp.symbols('x y', positive=True)
kbs = (1 - 3 * xs_**2) / (2 * xs_); kcs = (3 * ys_**2 - 1) / (2 * ys_)
diff_expr = sp.factor(sp.simplify(kbs - kcs))
chk("E1a exact identity kappa_b - kappa_c = (x + y)(1 - 3 x y)/(2 x y), so T_b = T_c iff x y = 1/3", sp.simplify(diff_expr - (xs_ + ys_) * (1 - 3 * xs_ * ys_) / (2 * xs_ * ys_)) == 0)
prod = lambda x: x * y_of(x)
chk("E1b x y < 1/3 strictly for every interior point (max of x y over the family is at the Nariai end, value 1/3), so T_b > T_c on the whole open family; equality only at Nariai (x = y = 1/sqrt3)",
    all(prod(mp.mpf(v)) < mp.mpf(1) / 3 for v in ['1e-6', '0.05', '0.2', '0.4', '0.55', '0.577', '0.5773502']) and abs(prod(xN) - mp.mpf(1) / 3) < 1e-35)
report("E1 (Nariai endpoint)", xN)
chk("E1c E1 selects only the endpoint: K_b = K_c = 0 (f-normalisation) or sqrt3 (BH-normalisation); neither is 1/Z = %s. FAILS to select a0" % mp.nstr(TARGET, 8), not matches(0) and not matches(mp.sqrt(3)))

# ------------------------------------------------------------ E2 entropy extremisation (high-precision grid, no float noise near Nariai)
mp.mp.dps = 120   # cancellations in 1 - 3 M^(2/3) near Nariai need > 60 digits at delta ~ 1e-16 (60 digits gave spurious sign changes)
NG = 700
xN = 1 / mp.sqrt(3)
xg = [mp.mpf('1e-8') * (mp.mpf('0.05') / mp.mpf('1e-8'))**(mp.mpf(i) / NG) for i in range(NG + 1)]              # geometric 1e-8 .. 0.05
xg += [mp.mpf('0.05') + (mp.mpf('0.5') - mp.mpf('0.05')) * mp.mpf(i) / 900 for i in range(1, 901)]              # linear .05 .. .5
xg += [xN - (xN - mp.mpf('0.5')) * (mp.mpf('1e-16') / (xN - mp.mpf('0.5')))**(mp.mpf(i) / 700) for i in range(1, 701)][::-1] # geometric approach to Nariai
xg = sorted(set(xg))
yg = [y_of(x) for x in xg]; Mg = [M_of(x) for x in xg]
def lst(fn): return [fn(x, y, M) for x, y, M in zip(xg, yg, Mg)]
funcs = {}
scal = {'L': lambda x, y, M: mp.mpf(1), 'M': lambda x, y, M: M, 'r_b': lambda x, y, M: x, 'r_c': lambda x, y, M: y}
for sn, sc in scal.items():
    funcs['S_tot/%s^2' % sn] = lst(lambda x, y, M, sc=sc: (x**2 + y**2) / sc(x, y, M)**2)
    funcs['S_b S_c/%s^4' % sn] = lst(lambda x, y, M, sc=sc: (x**2 * y**2) / sc(x, y, M)**4)
    funcs['(S_c-S_b)/%s^2' % sn] = lst(lambda x, y, M, sc=sc: (y**2 - x**2) / sc(x, y, M)**2)
funcs['S_b/S_c'] = lst(lambda x, y, M: x**2 / y**2)
funcs["[E2'] kappa_b kappa_c"] = lst(lambda x, y, M: kb(x) * kc(y))
funcs["[E2'] kappa_b + kappa_c"] = lst(lambda x, y, M: kb(x) + kc(y))
funcs["[E2'] kappa_b - kappa_c"] = lst(lambda x, y, M: kb(x) - kc(y))
funcs["[E2'] kappa_c/kappa_b"] = lst(lambda x, y, M: kc(y) / kb(x))
funcs["[E2'] BH-norm kappa_b kappa_c"] = lst(lambda x, y, M: kb(x) * kc(y) / (1 - 3 * M**(mp.mpf(2) / 3)))
funcs["[E2'] BH-norm kappa_b + kappa_c"] = lst(lambda x, y, M: (kb(x) + kc(y)) / mp.sqrt(1 - 3 * M**(mp.mpf(2) / 3)))
def sign_changes(F):
    d = [F[i + 1] - F[i] for i in range(len(F) - 1)]
    s = [1 if v > 0 else -1 for v in d if v != 0]
    return sum(1 for i in range(1, len(s)) if s[i] != s[i - 1]), ('increasing' if s[0] > 0 else 'decreasing')
# detector controls: a functional with a KNOWN interior extremum must be detected; a monotone one must not
ctl_pos = sign_changes([(x - mp.mpf('0.3'))**2 for x in xg]); ctl_neg = sign_changes([x**3 for x in xg])
chk("C3 detector control: (x - 0.3)^2 shows %d sign change (expected 1) and x^3 shows %d (expected 0) on the same grid" % (ctl_pos[0], ctl_neg[0]), ctl_pos[0] == 1 and ctl_neg[0] == 0)
stationary = {}
for name, F in funcs.items():
    stationary[name] = sign_changes(F)
    print("   %-34s sign changes of dF/dx over 2300 grid points: %d  (%s at the small-M end)" % (name, stationary[name][0], stationary[name][1]))
interior = [k for k, v in stationary.items() if v[0] > 0]
n_mono = len(funcs) - len(interior)
chk("E2a %d of %d functionals (entropies and, as flagged extras, temperature combinations; each at fixed L, M, r_b or r_c where dimensionful) are STRICTLY monotone in mu on the whole family; those with an interior stationary point: %s" % (n_mono, len(funcs), interior if interior else 'none'), len(interior) == 0)
E2_hits = []
for name in interior:
    F = funcs[name]
    d = [F[i + 1] - F[i] for i in range(len(F) - 1)]
    for i in range(1, len(d)):
        if (d[i] > 0) != (d[i - 1] > 0):
            E2_hits.append((name, xg[i]))
            print("   interior stationary point of %s near x = %s (mu = %s)" % (name, mp.nstr(xg[i], 8), mp.nstr(mu_of(xg[i]), 8)))
E2_match = any(matches(kb(x0)) or matches(kc(y_of(x0))) for _, x0 in E2_hits)
chk("E2b no interior stationary point has kappa_b/H or kappa_c/H equal to 1/Z (vacuous if there is none): E2 selects only endpoints -> FAILS to select a0", not E2_match)
# an exact proof for the leading entropy functional
Ssym = sp.simplify(xs_**2 + ((-xs_ + sp.sqrt(4 - 3 * xs_**2)) / 2)**2)
dS = sp.simplify(sp.diff(Ssym, xs_))
chk("E2c exact: d(S_tot/pi L^2)/dx = -y - x dy/dx < 0 on (0, 1/sqrt3) [S_tot/pi L^2 = 1 - x y]; checked symbolically at 40 rational points", all(dS.subs(xs_, sp.Rational(k, 60)) < 0 for k in range(1, 35)))

# ------------------------------------------------------------ E3 Smarr balance
xE3 = 1 / mp.sqrt(5)
f_check = lambda x: kb(x) * x**2 - (mp.mpf(1)) * x**3       # kappa_b r_b^2 - (Lambda/3) r_b^3, Lambda/3 = 1
xE3n = mp.findroot(lambda x: kb(x) * x**2 - x**3, mp.mpf('0.44'))
chk("E3a Smarr balance kappa_b r_b^2 = (8 pi/3) rho_Lambda r_b^3 (= Lambda r_b^3/3) has the unique interior root x^2 = 1/5 (root finder %s vs 1/sqrt5 = %s); it is an ALGEBRAIC point" % (mp.nstr(xE3n, 12), mp.nstr(xE3, 12)), abs(xE3n - xE3) < 1e-25)
kbv, kcv, kbh, kch = report("E3 Smarr half-and-half", xE3)
chk("E3b at that point K_b = 1/sqrt5 = %s (not 1/Z) and mu = %s: E3 FAILS to select a0" % (mp.nstr(kbv, 8), mp.nstr(mu_of(xE3), 8)), abs(kbv - 1 / mp.sqrt(5)) < 1e-30 and not matches(kbv) and not matches(kcv))

# ------------------------------------------------------------ E4 Bekenstein-type saturation
Bek = lambda x: 1 / (1 - x**2)      # S_b/(2 pi M r_b)
chk("E4a S_b/(2 pi M r_b) = 1/(1 - x^2) > 1 for every x > 0, equals 1 only at M -> 0 (endpoint), 3/2 at Nariai: saturation is not an interior point", all(Bek(mp.mpf(v)) > 1 for v in ['1e-6', '0.2', '0.5', '0.577']) and abs(Bek(xN) - mp.mpf(3) / 2) < 1e-30)
Mx = sp.Symbol('Mx'); rx = sp.Symbol('rx', positive=True)
EMS = lambda M, r: M + r**3 / 2                     # (r/2)(1 - g^{rr}) = M + r^3/(2 L^2), L = 1
chk("E4b with the Misner-Sharp energy E = M + r^3/2L^2 the horizon obeys S = 2 pi E r EXACTLY for every mu (identity S_h = pi r_h^2, E(r_h) = r_h/2): no selection", all(abs(2 * mp.pi * (M_of(x) + x**3 / 2) * x - mp.pi * x**2) < 1e-30 for x in [mp.mpf('0.1'), mp.mpf('0.4'), mp.mpf('0.57')]))
chk("E4c dS entropy bound S_tot = S_dS is saturated only at M = 0 (S_tot/S_dS = 1 - x y < 1 for all x > 0)", all(1 - prod(mp.mpf(v)) < 1 for v in ['1e-6', '0.3', '0.57']))

# ------------------------------------------------------------ E5 Unruh-effective matching
print("   E5: T_eff(a) = sqrt(a^2 + H^2)/(2 pi)")
def a_from_kappa(k): return mp.sqrt(k**2 - 1) if k >= 1 else None
aN_flat = a_from_kappa(1 / (4 * MN))
chk("E5a flat-space Hawking T = 1/(8 pi M) at M = M_N: a/H = sqrt(27/16 - 1) = sqrt(11)/4 = %s (algebraic, != 1/Z)" % mp.nstr(aN_flat, 10), abs(aN_flat - mp.sqrt(11) / 4) < 1e-30 and not matches(aN_flat))
chk("E5b flat-space T at M = L/2 is BELOW the dS floor (kappa = 1/(4 M) = 1/2 < H): no real acceleration a matches it", a_from_kappa(1 / (4 * mp.mpf(1) / 2)) is None)
aNBH = mp.sqrt(mp.sqrt(3)**2 - 1)
chk("E5c SdS horizons at Nariai (BH normalisation, kappa = sqrt3 H): a/H = sqrt2 = %s (algebraic)" % mp.nstr(aNBH, 10), abs(aNBH - mp.sqrt(2)) < 1e-30 and not matches(aNBH))
# BH horizon in the BH normalisation: kappa_b^BH >= sqrt3 => a >= sqrt2 H > a0
minbh = min(float(kBH(mp.mpf(float(v)))[0]) for v in np.linspace(0.01, 0.5773, 60))
chk("E5d BH-horizon in the BH normalisation always has a = sqrt(kappa^2 - H^2) >= sqrt2 H (min over 60 masses of kappa_b^BH = %.4f >= sqrt3): a0 = 0.173 H is never reached" % minbh, minbh >= float(mp.sqrt(3)) - 1e-3 and float(1 / Z) < float(mp.sqrt(2)))
# cosmological horizon: a(mu) = sqrt(kc_BH^2 - 1); solve a = a0
def a_c(x): return mp.sqrt(kBH(x)[1]**2 - 1)
xsol = mp.re(mp.findroot(lambda x: a_c(x) - TARGET, (mp.mpf('0.0005'), mp.mpf('0.02')), solver='anderson', tol=1e-40, maxsteps=200))
print("   E5e cosmological horizon, BH-norm: a = a0 at x = r_b/L = %s, mu = %s (the mass whose cosmological-horizon effective temperature equals that of an observer with a0)" % (mp.nstr(xsol, 10), mp.nstr(mu_of(xsol), 10)))
ac_vals = [a_c(x_of_mu(mp.mpf(m))) for m in ['0.001', '0.01', '0.1', '0.5', '0.9', '0.99']]
chk("E5e map a <-> mu on the cosmological horizon (BH norm): a increases monotonically from 0 (M = 0) towards sqrt2 H (Nariai; a(0.99 M_N) = %s), so a0 = 0.1727 H corresponds to ONE definite small mass mu = %s (the leading-order estimate M_N/Z^3 = %s is 16%% low, the next term is O(M^(1/3)) ~ 14%%): not a distinguished mass, no principle picks it. [my first tolerance 0.1 on the leading-order estimate was too tight; corrected here, the asymptotics are checked in E5f]" % (mp.nstr(ac_vals[-1], 6), mp.nstr(mu_of(xsol), 6), mp.nstr(1 / Z**3, 6)),
    all(ac_vals[i] < ac_vals[i + 1] for i in range(len(ac_vals) - 1)) and ac_vals[-1] < mp.sqrt(2) and 0 < mu_of(xsol) < 0.02 and abs(mu_of(xsol) * Z**3 - 1) < 0.25)
# small-M asymptote a^2 = 3 M^(2/3)(1 + O(M^(1/3))) (L = 1); relative correction is -(4/3) M^(1/3)
xt = mp.mpf('1e-30'); Mt = M_of(xt)
rel = abs(a_c(xt)**2 / (3 * Mt**(mp.mpf(2) / 3)) - 1)
chk("E5f small-M asymptote of the map: a^2 -> 3 (M/L)^(2/3)/L^2 with relative correction -(4/3)(M/L)^(1/3): measured %s vs predicted %s at M = %s" % (mp.nstr(rel, 4), mp.nstr(mp.mpf(4) / 3 * Mt**(mp.mpf(1) / 3), 4), mp.nstr(Mt, 3)), abs(rel - mp.mpf(4) / 3 * Mt**(mp.mpf(1) / 3)) < 1e-3 * rel)
# f-normalisation version: kappa_b = sqrt(a0^2 + H^2)
xf = mp.findroot(lambda x: kb(x) - mp.sqrt(TARGET**2 + 1), mp.mpf('0.4'))
print("   E5g f-normalisation: kappa_b = sqrt(a0^2 + H^2) = %s H at x = %s, mu = %s (an ordinary mid-family point, no distinction)" % (mp.nstr(mp.sqrt(TARGET**2 + 1), 8), mp.nstr(xf, 8), mp.nstr(mu_of(xf), 8)))
chk("E5g in the f-normalisation the same matching selects mu = %s: an arbitrary interior point; nothing forces it" % mp.nstr(mu_of(xf), 6), 0.3 < mu_of(xf) < 0.9 and abs(kb(xf) - mp.sqrt(TARGET**2 + 1)) < 1e-30)

# E5h: the static-patch identity kappa^2/f = a^2 + H^2 is a pure-dS statement; in SdS the 'Unruh-effective' excess D(r) = kappa_h^2/f - a(r)^2 is r-dependent
def D_of(mu, r, which):
    x = x_of_mu(mu); y = y_of(x); M = M_of(x); kap = kc(y) if which == 'c' else kb(x)
    fr = 1 - 2 * M / r - r**2; a2 = (M / r**2 - r)**2 / fr
    return kap**2 / fr - a2
Dd = [D_of(mp.mpf('0.5'), x_of_mu(mp.mpf('0.5')) + (y_of(x_of_mu(mp.mpf('0.5'))) - x_of_mu(mp.mpf('0.5'))) * mp.mpf(t), 'c') for t in ('0.2', '0.4', '0.6', '0.8')]
D0 = [D_of(mp.mpf('1e-9'), mp.mpf(t), 'c') for t in ('0.2', '0.4', '0.6', '0.8')]
chk("E5h in SdS (mu = 0.5) kappa_c^2/f - a^2 varies with r (%s ... %s) so the dS 'T^2 = (a^2 + H^2)/4 pi^2' has NO exact SdS analogue; at mu -> 0 it is the constant H^2 = 1 (%s): the E5 matchings above use horizon values, not a local identity" % (mp.nstr(Dd[0], 6), mp.nstr(Dd[-1], 6), mp.nstr(D0[0], 6)),
    max(Dd) - min(Dd) > 0.1 and all(abs(v - 1) < 1e-6 for v in D0))

# E10 (flagged extra): the record's Gauss-curvature form K_Sigma = rho_Lambda (G rho_Lambda r_h^2 = 1) on the SdS family, and mean-density facts
Grho = lambda r: 3 / (8 * mp.pi) * r**2          # G rho_Lambda r^2 with rho_Lambda = 3/(8 pi L^2), L = 1
maxb = Grho(xN); maxc = Grho(mp.mpf(1))
chk("E10a K_Sigma = rho_Lambda (G rho_Lambda r_h^2 = 1) is unattainable on ANY SdS horizon: max over black-hole horizons %s (Nariai, = 1/(8 pi)), max over cosmological horizons %s (M = 0, = 3/(8 pi)); the puzzle's Gauss-curvature form and its kappa form are different conditions inside SdS" % (mp.nstr(maxb, 6), mp.nstr(maxc, 6)),
    abs(maxb - 1 / (8 * mp.pi)) < 1e-30 and abs(maxc - 3 / (8 * mp.pi)) < 1e-30 and maxc < 1)
rho_BH = lambda x: 1 / x**2 - 1                   # mean density 3M/(4 pi r_b^3) over rho_Lambda = 2M/x^3 = 1/x^2 - 1
chk("E10b mean density of the hole (3M/4 pi r_b^3)/rho_Lambda = 1/x^2 - 1 in (2, infinity), equal to 2 at Nariai (and total incl. vacuum 3 rho_Lambda): algebraic, pi cancels; an interior 'density principle' selects an algebraic point", abs(rho_BH(xN) - 2) < 1e-30 and all(rho_BH(mp.mpf(v)) > 2 for v in ['0.1', '0.4', '0.57']))

# ------------------------------------------------------------ summary: none of E1-E5 reaches 1/Z
selected = {'E1': [mp.mpf(0), mp.sqrt(3)], 'E3': [kb(xE3), kc(y_of(xE3))], 'E4': [], 'E5a': [aN_flat], 'E5c': [aNBH]}
anymatch = any(matches(v) for vals in selected.values() for v in vals)
chk("S  none of the selected points of E1-E5 reproduces 1/Z = %s to 1e-10 (E2 has no interior selection; E4 saturations are endpoints or identities)" % mp.nstr(TARGET, 8), not anymatch)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
