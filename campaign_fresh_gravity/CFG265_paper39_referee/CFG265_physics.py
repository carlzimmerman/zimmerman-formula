#!/usr/bin/env python3
"""CFG265_physics.py: frozen-criteria section 4 re-derivations P2-P9, P13 (P1 is CFG265_lean_read.py, P10/P11 are
CFG265_audit_anchor.py, P12 is CFG265_route_recount.py). numpy / scipy / sympy only; no network; reads nothing that
writes into the repo.
  python3 CFG265_physics.py            exit 0 if every known-answer self-control passes, 1 otherwise
  python3 CFG265_physics.py --mutate   perturbs one input (the P2 kernel exponent 1/2 -> 0.45); must exit 1
A recomputation that disagrees with the draft prints CONTRADICTS (never an error exit). Writes CFG265_physics_results.json
(or CFG265_physics_MUTATE_results.json)."""
import sys, os, json, math
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad
from CFG265_common import HERE, scrub

MUT = '--mutate' in sys.argv
PEXP = 0.45 if MUT else 0.5          # the P2 kernel nu = (1 + 1/y)^PEXP; the MUTATE perturbs it
out, res, ctl = [], {}, []


def P(*a):
    s = ' '.join(str(x) for x in a)
    out.append(s); print(s)


def control(name, ok, detail=''):
    ctl.append((name, bool(ok)))
    P('  [%s] self-control %s %s' % ('PASS' if ok else 'FAIL', name, detail))


def verdict(tag, ok, detail):
    P('  %s %s: %s' % ('AGREES' if ok else 'CONTRADICTS', tag, detail))
    res.setdefault('verdicts', {})[tag] = dict(agrees=bool(ok), detail=detail)


def nuP2(y):
    return (1.0 + 1.0 / y) ** PEXP


def nuRAR(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


P('CFG265 physics re-derivations (frozen list P2-P9, P13)%s' % ('  [MUTATE: P2 exponent 0.45]' if MUT else ''))

# ------------------------------------------------------------------ P2 dimension theorem
P('\nP2 dimension theorem (monomials G^a M^b c^d X^e with b = 1/2 a length)')
a, b, d, e = sp.symbols('a b d e')
dims = {'G': (3, -1, -2), 'M': (0, 1, 0), 'c': (1, 0, -1)}   # (L, M, T)
X = {'a0 (accel)': (1, 0, -2), 'hbar': (2, 1, -1), 'Lambda (1/L^2)': (-2, 0, 0), 'rho_Lambda': (-3, 1, 0), 'H0 (1/T)': (0, 0, -1),
     'a length': (1, 0, 0), 'a mass': (0, 1, 0), 'a velocity': (1, 0, -1), 'G itself': (3, -1, -2), 'Planck force c^4/G': (1, 1, -2)}
sol0 = sp.solve([3 * a + d - 1, -a + b, -2 * a - d], [a, b, d], dict=True)
P('  (G, M, c) length: unique exponents', sol0, '-> G M / c^2, a length proportional to M^1, so no M^(1/2) length')
control('dimension: (G,M,c) length is GM/c^2', sol0 == [{a: 1, b: 1, d: -2}])
rowsP2 = []
for name, (xl, xm, xt) in X.items():
    eqs = [3 * a + d + xl * e - 1, -a + sp.Rational(1, 2) + xm * e, -2 * a - d + xt * e]
    s = sp.solve(eqs, [a, d, e], dict=True)
    exists = len(s) > 0
    # acceleration from (G, c, X): u X + v G + w c = (1, 0, -2)
    u, v, w = sp.symbols('u v w')
    s2 = sp.solve([u * xl + 3 * v + w - 1, u * xm - v, u * xt - 2 * v - w + 2], [u, v, w], dict=True)
    acc = len(s2) > 0
    massexp = xl + xm + xt
    rowsP2.append(dict(X=name, sqrtM_length=exists, acceleration_from_GcX=acc, massExp=massexp, exps=str(s[0]) if s else ''))
    P('  X = %-20s M^(1/2) length exists: %-5s  (G,c,X) give an acceleration: %-5s  massExp %+d  %s' % (name, exists, acc, massexp, (str(s[0]) if s else '')))
iff = all(r['sqrtM_length'] == r['acceleration_from_GcX'] == (r['massExp'] != 0) for r in rowsP2)
verdict('P2 "exists iff (G,c,X) form an acceleration scale; hbar admissible"', iff and rowsP2[1]['sqrtM_length'],
        'iff holds for all %d X tried; hbar exponents %s' % (len(rowsP2), rowsP2[1]['exps']))
res['P2'] = rowsP2

# ------------------------------------------------------------------ P3 AQUAL mu -> P2 kernel
P('\nP3 AQUAL mu(x) = (sqrt(1+4x^2) - 1)/(2x) -> kernel')
x, y = sp.symbols('x y', positive=True)
mu = (sp.sqrt(1 + 4 * x ** 2) - 1) / (2 * x)
xmu = sp.simplify(x * mu)
solx = sp.solve(sp.Eq(xmu, y), x)
nu_from = sp.simplify(solx[0] / y) if solx else None
P('  x mu(x) =', xmu, '; root x(y) =', solx, '; nu(y) = x/y =', nu_from)
deriv = sp.simplify(sp.diff(xmu, x))
P('  d(x mu)/dx =', deriv, ' (positive for x > 0); limits x mu -> 0 at 0+, -> oo at oo:', sp.limit(xmu, x, 0, '+'), sp.limit(xmu, x, sp.oo))
p2ok = nu_from is not None and sp.simplify(nu_from - sp.sqrt(1 + 1 / y)) == 0
control('AQUAL mu gives nu = sqrt(1+1/y) (the P2 kernel)', p2ok, str(nu_from))
yy = 1e-8
control('P2 deep limit nu*sqrt(y) -> 1', abs(nuP2(yy) * math.sqrt(yy) - 1) < 1e-3, '%.6f' % (nuP2(yy) * math.sqrt(yy)))
control('P2 Newtonian limit nu -> 1', abs(nuP2(1e8) - 1) < 1e-6, '%.9f' % nuP2(1e8))
verdict('P3 "P2 kernel follows from mu = (sqrt(1+4x^2)-1)/(2x); x mu increasing onto (0,oo)"', p2ok, 'nu = %s' % nu_from)
res['P3'] = dict(nu=str(nu_from), dxmu=str(deriv))

# ------------------------------------------------------------------ P4 footing
P('\nP4 Milgrom a0 = c H0/(2 pi) written as kappa c sqrt(G rho)')
OmL = 0.6847
k_crit = math.sqrt(2 / (3 * math.pi))
k_lam = math.sqrt(2 / (3 * math.pi * OmL))
P('  rho = rho_crit = 3H0^2/(8 pi G): kappa = sqrt(2/(3 pi)) = %.4f' % k_crit)
P('  rho = rho_Lambda = Omega_L rho_crit (Omega_L = %.4f, the A0Numeric point): kappa = sqrt(2/(3 pi Omega_L)) = %.4f' % (OmL, k_lam))
P('  the law is written a0 = kappa c sqrt(G rho_Lambda) everywhere in the draft; Footing.lean uses rho = 3H^2/(8 pi G) (the critical, total density).')
verdict('P4 "In the kappa c sqrt(G rho) convention Milgrom\'s value is sqrt(2/(3 pi))"', True,
        'true for rho = rho_crit (Footing.lean); in the draft\'s own rho_Lambda convention Milgrom\'s cH0/2pi is kappa = %.3f (undeclared choice)' % k_lam)
res['P4'] = dict(kappa_rho_crit=k_crit, kappa_rho_Lambda=k_lam, Omega_L=OmL)

# ------------------------------------------------------------------ P5 32 pi algebra
P('\nP5 the 32 pi bookkeeping (c, G explicit)')
c, G, rho = sp.symbols('c G rho', positive=True)
Lam = 8 * sp.pi * G * rho / c ** 2
Rs = c / sp.sqrt(G * rho)
a0 = c ** 2 / (2 * Rs)
P('  R*^2 Lambda =', sp.simplify(Rs ** 2 * Lam), '; a0 = c^2/(2R*) =', sp.simplify(a0), '-> kappa =', sp.simplify(a0 / (c * sp.sqrt(G * rho))))
C32 = sp.simplify(Lam * c ** 4 / a0 ** 2)
P('  C = Lambda c^4 / a0^2 =', C32, '(a pure number only with Lambda_geom = Lambda c^4; with c = 1 it is Lambda/a0^2)')
four = sp.simplify(G * rho / (a0 ** 2 / c ** 2))
P('  G rho_Lambda / (a0^2/c^2) =', four, '(the "rational 4"; G rho = 4 a0^2 in c = 1 units)')
RH = sp.sqrt(3 / Lam)
ratio = sp.simplify(Rs / RH)
P('  de Sitter horizon radius sqrt(3/Lambda); R*/R_H =', ratio, '= %.4f: R* lies outside the static-patch horizon, so R* is not a horizon' % float(ratio))
P('  horizon surface gravity c^2/R_H vs a0 = c^2/(2R*): a0/(c^2/R_H) =', sp.simplify(a0 / (c ** 2 / RH)), '= %.4f' % float(sp.simplify(a0 / (c ** 2 / RH))))
ok5 = sp.simplify(Rs ** 2 * Lam - 8 * sp.pi) == 0 and sp.simplify(C32 - 32 * sp.pi) == 0 and four == 4
control('R*^2 Lambda = 8 pi, C = 32 pi, rational 4', ok5)
verdict('P5 "R*^2 Lambda = 8 pi, a0 = c^2/(2R*): the algebra is correct; R* is not a horizon"', ok5, 'R*/R_H = %.3f' % float(ratio))
res['P5'] = dict(R_over_RH=float(ratio), C=str(C32), four=str(four))

# ------------------------------------------------------------------ P6 kappa and BBN arithmetic
P('\nP6 kappa and BBN arithmetic')
z_unruh = (1.447 - 0.465) / 0.076
P('  Unruh n = 2: (1.447 - 0.465)/0.076 = %.2f sigma (draft 12.9)' % z_unruh)
verdict('P6 12.9 sigma', abs(z_unruh - 12.9) < 0.05, '%.2f' % z_unruh)
P('  1/2 inside 0.465 +- 0.076: pull %+.2f; inside 0.547 +- 0.175: pull %+.2f' % ((0.5 - 0.465) / 0.076, (0.5 - 0.547) / 0.175))
gap = 0.98 - 0.824
P('  BBN: R < 0.824 vs G_BBN/G0 = 0.98 +- 0.06: gap %.3f = %.1f sigma if +-0.06 is 1 sigma; %.1f sigma if +-0.06 is the 95.4%% (2 sigma) half-width (STANDING: "at 95.4%%")'
  % (gap, gap / 0.06, gap / 0.03))
P('  A20 abstract (WebFetch 2026-10-01): BBN+CMB 0.99 +0.06/-0.05 at 2 sigma -> (0.99 - 0.824)/0.025 = %.1f sigma' % ((0.99 - 0.824) / 0.025))
res['P6'] = dict(unruh_sigma=z_unruh, bbn_gap=gap, bbn_sigma_if_1sig=gap / 0.06, bbn_sigma_if_95=gap / 0.03)
# footing likelihood (re-read numbers, from real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.out)
P('  footing likelihood (committed .out lines 75-80): Delta chi2 vs free best fit: kappa=1/2 canonical 63.90, 1/2pi (Milgrom 2020) 154.29, alt footing 7.04, Milgrom cH0/2pi own footing 5.34')
P('  -> Milgrom cH0/2pi fits better than BOTH framework footings (5.34 < 7.04 < 63.90); "as well as the framework (5.34 against 7.04 alt)" compares only to the alt footing')

# ------------------------------------------------------------------ P7 DR4
P('\nP7 DR4 (frozen sigma_sys = 0.02; per-pair constant fixed by 4,342 pairs at floor 1.1614)')
floor, floor_alt, ssys = 1.1614, 1.1917, 0.02
cpp = brentq(lambda cc: (floor - 1) / math.sqrt(ssys ** 2 + cc ** 2 / 4342) - 3, 0.1, 50)
st30 = math.sqrt(ssys ** 2 + cpp ** 2 / 30000)
P('  per-pair constant c = %.4f; sigma_fit(30k) = %.4f; sigma_tot(30k) = %.5f (CFG200: 0.02759; prereg table 0.028)' % (cpp, cpp / math.sqrt(30000), st30))
control('DR4 constant reproduces CFG200 sigma_tot 0.02759 within 2e-4', abs(st30 - 0.02759) < 2e-4, '%.5f' % st30)
nalt = (cpp ** 2) / (((floor_alt - 1) / 3) ** 2 - ssys ** 2)
P('  alt floor 1.1917: N3sigma = %.0f (draft/STANDING 2,900; WHAT_WOULD_DECIDE 2,940)' % nalt)
P('  cap (1.1614 - 1)/0.02 = %.2f (draft 8.1); separation at 30k = %.2f (record 5.8)' % ((floor - 1) / ssys, (floor - 1) / st30))
for nm_, sig in (('sigma_tot 0.028 (prereg table convention)', 0.028), ('sigma_tot %.5f (computed)' % st30, st30)):
    P('  %s: B kill 1 + 3s = %.4f (draft 1.084); Arm A 3-sigma edge 1.1614 - 3s = %.4f (draft "kills the bare law" 1.077)' % (nm_, 1 + 3 * sig, floor - 3 * sig))
P('  preregistration (edge_table_dr4.json hard edges): Arm A FALSIFIED below 1.056 (Amdt 11(d)); 1.056-1.084 Arm A "disfavored (2.8-3.8 sigma_tot)";')
P('    Arm B/C killed at >= 1.084 only if the frozen stability checks pass (else "systematic-limited, no verdict"); > 1.23 no verdict')
seps = {}
for lab, g in (('P2 merge canonical variant floor 1.063', 1.063), ('P2 merge canonical variant top 1.077', 1.077), ('P2 merge canonical primary floor 1.089', 1.089),
               ('P2 merge canonical primary top 1.102', 1.102), ('P2 merge alt variant floor 1.079', 1.079), ('P2 merge alt primary floor 1.111', 1.111),
               ('P2 merge alt primary top 1.127', 1.127), ('Arm A canonical 1.1614', 1.1614), ('Arm A canonical top 1.1814', 1.1814), ('chain ceiling 1.0725', 1.0725)):
    seps[lab] = (g - 1) / st30
    P('  %-42s vs ownership 1.000: %.2f sigma_tot at N = 30,000' % (lab, seps[lab]))
P('  P2 merge vs chain ceiling 1.0725: %.2f to %.2f sigma (never 3)' % ((1.077 - 1.0725) / st30, (1.102 - 1.0725) / st30))
band_lo, band_hi = seps['P2 merge canonical variant floor 1.063'], seps['P2 merge alt primary top 1.127']
verdict('P7 "1.063-1.127 separates from ownership by 2.3-3.7 sigma"', abs(band_lo - 2.3) < 0.05 and abs(band_hi - 3.7) < 0.05,
        'the band 1.063-1.127 spans %.2f-%.2f sigma; 2.3-3.7 is the CANONICAL footing only (1.063-1.102); the alt top 1.127 is %.2f sigma' % (band_lo, band_hi, band_hi))
verdict('P7 "gamma <= 1.077 kills the bare law"', False,
        '1.077 is Arm A (nu_RAR merge) floor minus 3 x 0.028 (a z-rule "disfavored" edge, CFG63 "frozen-rounded"); the preregistered falsification edge is 1.056; and 1.077 is the TOP of the P2 merge at the variant field, so it cannot kill a P2 bare law')
verdict('P7 "gamma >= 1.084 kills B"', True, '1 + 3 x 0.028 = 1.084 (frozen); requires the stability checks (prereg Amdt 13(d))')
verdict('P7 cap 8.1 and 4,300 pairs', abs((floor - 1) / ssys - 8.07) < 0.01, 'cap %.2f, N3 4342 by construction' % ((floor - 1) / ssys))
res['P7'] = dict(c=cpp, sigma_tot_30k=st30, n3_alt=nalt, seps=seps)

# ------------------------------------------------------------------ P8 satellites
P('\nP8 satellites arithmetic')
zkm = 0.3245 / math.sqrt(0.038 ** 2 + 0.077 ** 2)
P('  0.3245 / sqrt(0.038^2 + 0.077^2) = %.2f (draft 3.77; CFG259 DV0 3.77)' % zkm)
verdict('P8 3.77 sigma', abs(zkm - 3.77) < 0.02, '%.3f' % zkm)
P('  corrections as fractions of the offset: 0.068/0.3245 = %.2f, 0.104/0.3245 = %.2f ("a fifth to a third")' % (0.068 / 0.3245, 0.104 / 0.3245))
P('  DV3 RAR alt Delta chi2_V2 = 9.24 -> 0.24 above 9; DV0 RAR alt 8.60 -> 0.40 below 9 ("+8.60 ... falls")')
P('  without the ultra-faints: CFG244 "Delta about -1.3"; CFG259 "-1.3 to -1.8 at DV0" (draft "about -1.3")')
P('  "capped near 2.5 sigma" (Section 7) is the cap on separating the bare law from B\'s derived cold-mass RULE (WHAT_WOULD_DECIDE 3: Delta 0.38 dex, floors 0.077 + 0.133);')
P('    B\'s isolated-law failure (3.5-3.9 sigma, Section 5) is a different statistic: the two are consistent only once that is said')
res['P8'] = dict(z_km=zkm)

# ------------------------------------------------------------------ P9 internal arithmetic (also the ARITH family of the checker)
P('\nP9 internal arithmetic')
A = [('A01 22+2+1 = 25', 22 + 2 + 1 == 25), ('A02 0+11+5+27+11 = 54', 0 + 11 + 5 + 27 + 11 == 54), ('A03 219+62 = 281', 219 + 62 == 281),
     ('A04 281+50 = 331', 281 + 50 == 331), ('A05 219 - 47 = 172, the library before the first of the three steps', 219 - 47 == 172),
     ('A06 sqrt(1000) = 31.62 (1e9..1e12)', abs(math.sqrt(1000) - 31.6228) < 1e-4), ('A07 12.9 sigma', abs(z_unruh - 12.9) < 0.05),
     ('A08 3.77 sigma', abs(zkm - 3.77) < 0.02), ('A09 cap 8.1', abs(0.1614 / 0.02 - 8.07) < 0.01),
     ('A10 kill B 1+3(0.028) = 1.084', abs(1 + 3 * 0.028 - 1.084) < 1e-9), ('A11 Arm A 1.1614-3(0.028) = 1.077', abs(1.1614 - 0.084 - 1.0774) < 1e-9),
     ('A12 fifth/third', 0.19 < 0.068 / 0.3245 < 0.22 and 0.31 < 0.104 / 0.3245 < 0.34),
     ('A13 Gamma tau 0.787 x 5.37 = 4.23 and 0.787 x 5.17 = 4.07 (the "4.1-4.2")', abs(0.787 * 5.37 - 4.23) < 0.01 and abs(0.787 * 5.17 - 4.07) < 0.01),
     ('A14 window 1.73-1.93 overlaps (generous bracket), "nearly meet" is the GAPS wording', 1.73 < 1.93),
     ('A15 R*^2 Lambda = 8 pi', ok5), ('A16 kappa_M = sqrt(2/(3pi)) = 0.4607', abs(k_crit - 0.4607) < 1e-4),
     ('A17 (1.447-0.465)/0.076 = 12.9', abs(z_unruh - 12.92) < 0.01), ('A18 9.24 - 9 = 0.24', abs(9.24 - 9 - 0.24) < 1e-9),
     ('A19 p = 0.327-0.343 -> "0.33-0.34"', round(0.327, 2) == 0.33 and round(0.343, 2) == 0.34),
     ('A20 x = 3 r_M point mass P2: nu = sqrt(10) = 3.162 ("up to 3.16")', abs(math.sqrt(10) - 3.1623) < 1e-4),
     ('A21 ten doors re-derived = nine referee lanes (CFG151-159) + door 2 none', len(range(151, 160)) == 9),
     ('A22 band 1.063-1.127 vs 2.3-3.7 sigma at 30k (see P7)', abs(band_hi - 3.7) < 0.05)]
for t, ok in A:
    P('  %-75s %s' % (t, 'OK' if ok else 'FAILS'))
res['P9'] = [dict(rel=t, ok=bool(ok)) for t, ok in A]

# ------------------------------------------------------------------ P13 local phantom vs the CFG44 target
P('\nP13 QUMOND local phantom C_loc = rho_ph r^3 g_tot against the CFG44 target (a0/4pi) M_b(<r)')
Gc = 4.30091e-6                                  # kpc (km/s)^2 / Msun
a0_can = 9.36e-11 * 3.0857e19 / 1e6              # (km/s)^2 / kpc
def C_ratio(Mb, h, kern, xs):
    rM = math.sqrt(Gc * Mb / a0_can)
    def Menc(r):
        s = r / h
        return Mb * (1 - math.exp(-s) * (1 + s + s * s / 2))
    def F(r):                                    # r^2 (nu - 1) g_N
        gN = Gc * Menc(r) / r ** 2
        return r ** 2 * (kern(gN / a0_can) - 1) * gN
    out_ = []
    for xx in xs:
        r = xx * rM
        dr = r * 1e-5
        dF = (F(r + dr) - F(r - dr)) / (2 * dr)
        rho_ph = dF / (4 * math.pi * Gc * r ** 2)
        gN = Gc * Menc(r) / r ** 2
        gt = kern(gN / a0_can) * gN
        out_.append(4 * math.pi * rho_ph * r ** 3 * gt / (a0_can * Menc(r)))
    return np.array(out_)
xs = np.logspace(-1, math.log10(30), 120)
# point mass control (P2): ratio 1 at every x
def C_ratio_pm(kern, xs):
    out_ = []
    for xx in xs:
        yv = 1 / xx ** 2
        h_ = 1e-6
        Fp = lambda q: (kern(1 / q ** 2) - 1) / q ** 2 * q ** 2     # (nu-1) g_N r^2 in units GM = 1, r = q r_M
        dF = (Fp(xx * (1 + h_)) - Fp(xx * (1 - h_))) / (2 * xx * h_)
        out_.append(dF * xx * kern(yv) * yv)  # 4 pi rho_ph r^3 g_tot / (a0 M) in units G M = a0 = 1
    return np.array(out_)
pm = C_ratio_pm(nuP2, xs)
control('P2 point mass: C_loc = C_44 at every x (ratio 1)', np.max(np.abs(pm - 1)) < 1e-4, 'max |R-1| = %.2e' % np.max(np.abs(pm - 1)))
rows13 = []
for kern, kn in ((nuP2, 'P2'), (nuRAR, 'nu_RAR (sensitivity; not nu_mono)')):
    for Mb in (1e9, 1e10, 1e11, 1e12):
        for h in (2.0, 3.0, 4.0, 5.0):
            R = C_ratio(Mb, h, kern, xs)
            rows13.append(dict(kernel=kn, Mb=Mb, h=h, maxR=float(R.max()), minR=float(R.min())))
for kn in ('P2', 'nu_RAR (sensitivity; not nu_mono)'):
    rr = [r for r in rows13 if r['kernel'] == kn]
    P('  %-36s max over x in [0.1,30] of C_loc/C_44: %.2f - %.2f (16 cells: 1e9-1e12 Msun x h = 2-5 kpc)' % (kn, min(r['maxR'] for r in rr), max(r['maxR'] for r in rr)))
mx = max(r['maxR'] for r in rows13 if r['kernel'] == 'P2')
verdict('P13 "ratio up to 2.33 for P2" (CFG245 on CFG118\'s spheres)', 1.5 < mx < 3.5,
        'this lane\'s generic exponential spheres give a P2 maximum %.2f; the exact value depends on the profile (CFG118\'s h per mass); order and sign agree' % mx)
P('  isolated-law internal/Newtonian ratio for a point mass (P2): x = 0.3, 1, 3 -> %.3f, %.3f, %.3f (draft "up to 3.16")' % (nuP2(1 / 0.09), nuP2(1.0), nuP2(1 / 9)))
res['P13'] = dict(point_mass_max_dev=float(np.max(np.abs(pm - 1))), rows=rows13)

# ------------------------------------------------------------------ summary
nfail = sum(1 for _, ok in ctl if not ok)
P('\nself-controls: %d of %d pass' % (len(ctl) - nfail, len(ctl)))
res['self_controls'] = [dict(name=n, ok=o) for n, o in ctl]
json.dump(res, open(os.path.join(HERE, 'CFG265_physics_MUTATE_results.json' if MUT else 'CFG265_physics_results.json'), 'w'), indent=1, default=str)
sys.exit(1 if nfail else 0)
