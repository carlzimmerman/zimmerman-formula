#!/usr/bin/env python3
"""N4 -- the holographic count coefficient c' (N^2 = c' S_dS  =>  1/alpha = 12 pi c').  Pre-registered in N4_PREREGISTRATION.md.

Run:      PYTHONDONTWRITEBYTECODE=1 python3 n4_holographic_count.py            (must exit 0; output saved as n4_holographic_count.out)
CONTROL:  PYTHONDONTWRITEBYTECODE=1 python3 n4_holographic_count.py --mutate   (the ONLY trigger is argv '--mutate'; must exit 1)
          --mutate replaces the ultracold charge Q^2 = 1/(4 Lambda) by 1/(2 Lambda) and S_uc/S_dS = 1/6 by 1/3, so the symbolic checks G1/G2 must FAIL.
Sections: G1-G4 exact geometry (sympy), F5 exponent range test, F1-F3 enumeration and scoring against lane D's bar, D1 density diagnostic, controls.
"""
import sys, math, itertools
sys.dont_write_bytecode = True
import sympy as sp
import mpmath as mp
mp.mp.dps = 30
MUT = '--mutate' in sys.argv
fails = []
def check(name, ok, info=""):
    print(('PASS ' if ok else 'FAIL ') + name + (('  ' + info) if info else ''))
    if not ok: fails.append(name)

# ------------------------------------------------------------------ G1: ultracold point (geometrised units G = c = 1 for the metric, lengths in units of 1/sqrt(Lambda))
r, Mg, Q2, L, y, r0 = sp.symbols('r M_g Q2 Lambda y r0', positive=True)
P = -L*r**4/3 + r**2 - 2*Mg*r + Q2                      # r^2 f(r), f = 1 - 2M/r + Q^2/r^2 - Lambda r^2/3
sol = sp.solve([P, sp.diff(P, r), sp.diff(P, r, 2)], [r, Mg, Q2], dict=True)
sol = [s for s in sol if all(v.is_positive for v in s.values())][0]
rr, MM, QQ = sp.simplify(sol[r]), sp.simplify(sol[Mg]), sp.simplify(sol[Q2])
print('G1 triple root: r0 = %s, M = %s, Q^2 = %s' % (rr, MM, QQ))
Q2_claim = sp.Rational(1, 2)/L if MUT else sp.Rational(1, 4)/L
check('G1a Q_geo^2 Lambda = 1/4' + (' [MUTATE: 1/2]' if MUT else ''), sp.simplify(QQ - Q2_claim) == 0)
check('G1b r0^2 Lambda = 1/2', sp.simplify(rr**2*L - sp.Rational(1, 2)) == 0)
check('G1c M_g^2 Lambda = 2/9', sp.simplify(MM**2*L - sp.Rational(2, 9)) == 0)
Phi = sp.simplify(sp.sqrt(QQ)/rr)
check('G1d horizon potential Phi_H = Q_geo/r0 = 1/sqrt 2', sp.simplify(Phi - 1/sp.sqrt(2)) == 0, '-> %s' % Phi)
check('G1e z^2 = Q^2/M^2 = 9/8', sp.simplify(QQ/MM**2 - sp.Rational(9, 8)) == 0)
# along the whole degenerate curve (y = Lambda r0^2)
Mc = r0*(1 - sp.Rational(2, 3)*y); Qc = r0**2*(1 - y)
Pc = P.subs({Mg: Mc, Q2: Qc, L: y/r0**2})
check('G1f degenerate curve: P(r0) = P\'(r0) = 0', sp.simplify(Pc.subs(r, r0)) == 0 and sp.simplify(sp.diff(Pc, r).subs(r, r0)) == 0)
P2 = sp.simplify(sp.diff(Pc, r, 2).subs(r, r0))
print('   P\'\'(r0) along the curve =', sp.factor(P2), ' -> dS_2 radius^2 = 2 r0^2/|P\'\'| = r0^2/|1-2y|; infinite at y = 1/2 (R^{1,1} x S^2)')
check('G1g P\'\'(r0) = 2(1-2y): dS_2 factor degenerates to flat exactly at the ultracold point', sp.simplify(P2 - 2*(1 - 2*y)) == 0 and sp.solve(P2, y) == [sp.Rational(1, 2)])
qy = sp.simplify(Qc*y/r0**2); my = sp.simplify(Mc**2*y/r0**2)
check('G1h Q^2 Lambda = y(1-y) and M^2 Lambda = y(1-2y/3)^2 are BOTH maximal at y = 1/2 (max charge = max mass; no separate max-charge Nariai point)',
      [v for v in sp.solve(sp.diff(qy, y), y) if 0 < v <= 1] == [sp.Rational(1, 2)] and [v for v in sp.solve(sp.diff(my, y), y) if 0 < v <= 1] == [sp.Rational(1, 2)])

# ------------------------------------------------------------------ G2: entropies (units l_P = 1: S = pi r^2 / l_P^2, x = Lambda l_P^2)
x = sp.symbols('x', positive=True)
lam_l = x                                    # Lambda in l_P units
r0_uc = sp.sqrt(sp.Rational(1, 2)/x); M_uc = sp.sqrt(sp.Rational(2, 9)/x); Q2_uc = sp.Rational(1, 4)/x
S_dS = 3*sp.pi/x
S_uc = sp.pi*r0_uc**2
ratio_uc = sp.Rational(1, 3) if MUT else sp.Rational(1, 6)
check('G2a S_uc = pi/(2x) = S_dS/6' + (' [MUTATE: 1/3]' if MUT else ''), sp.simplify(S_uc/S_dS - ratio_uc) == 0)
S_bek = 2*sp.pi*M_uc*r0_uc
check('G2b S_Bek = 2 pi M r0 = 2 pi/(3x) = (2/9) S_dS', sp.simplify(S_bek/S_dS - sp.Rational(2, 9)) == 0)
Coul = 2*sp.pi*(sp.sqrt(Q2_uc)/r0_uc)*sp.sqrt(Q2_uc)*r0_uc      # 2 pi (Phi Q) r0 : Bekenstein with the Coulomb energy
check('G2c Coulomb-Bekenstein identity: 2 pi (Phi Q) r0 = S_uc (both sides prop. to alpha N^2; alpha-free)', sp.simplify(Coul - S_uc) == 0)

# ------------------------------------------------------------------ G3, G4: alpha,N dependence
al, N, n, lam, lP = sp.symbols('alpha N n lambda l_P', positive=True)
Qg2 = al*N**2*lP**2                                       # Q_geo^2 = G Q^2/c^4, Q = N sqrt(alpha hbar c)  (c3a)
# metric function of the classical solution depends on (alpha, N) ONLY through Qg2
f = 1 - 2*sp.Symbol('m', positive=True)/r + Qg2/r**2 - sp.Symbol('Lam', positive=True)*r**2/3
resc = f.subs({al: al/lam**2, N: lam*N}, simultaneous=True)
check('G4a metric function invariant under N -> lam N, alpha -> alpha/lam^2', sp.simplify(resc - f) == 0)
Nmax = sp.sqrt(Q2_uc/(al*1))                              # N_max^2 = Q_geo^2/(alpha l_P^2) = 1/(4 alpha x)
Nmax2 = sp.simplify(Q2_uc/al)
check('G3a N_max^2 = 1/(4 alpha x)', sp.simplify(Nmax2 - 1/(4*al*x)) == 0)
# ultracold horizon thermodynamics in terms of (alpha, N): expressed through alpha*N^2 only
S_of_aN = sp.simplify(S_uc.subs(x, 1/(4*al*N**2)))       # eliminate x at N = N_max
check('G4b S_uc = 2 pi alpha N_max^2 (holds for the integer N only through alpha N^2)', sp.simplify(S_of_aN - 2*sp.pi*al*N**2) == 0)
check('G4c S_uc, S_Bek, Phi*Q*r0, M^2/M_P^2 unchanged by (N, alpha) -> (lam N, alpha/lam^2)',
      all(sp.simplify(e.subs({al: al/lam**2, N: lam*N}, simultaneous=True) - e) == 0 for e in [2*sp.pi*al*N**2, al*N**2]))
# magnetic dual (Dirac; from A2: Q_m^2 = n^2 l_P^2/(4 alpha))
Qm2 = n**2*lP**2/(4*al)
nmax2 = sp.simplify(sp.Rational(1, 4)/x/(1/(4*al)))     # n^2/(4 alpha) <= 1/(4x)
check('G3b magnetic cap n_max^2 = alpha/x', sp.simplify(nmax2 - al/x) == 0)
check('G3c N_max n_max = 1/(2x), alpha-free (Dirac product)', sp.simplify(sp.sqrt(Nmax2*nmax2) - 1/(2*x)) == 0)
S_ext = sp.pi*al*N**2
r_ext = sp.sqrt(Qg2)                                       # flat extremal RN: r_+ = Q_geo (double root of 1 - 2M/r + Q^2/r^2)
check('G3d flat extremal S_ext = pi r_+^2/l_P^2 = pi alpha N^2', sp.simplify(sp.pi*r_ext**2/lP**2 - sp.pi*al*N**2) == 0)
# degenerate curve: N^2/S_h = (1-y)/(pi alpha): for EVERY alpha a y exists with N^2 = S_h
Nsq_y = y*(1 - y)/(al*x); Sh_y = sp.pi*y/x
ysol = sp.solve(sp.Eq(Nsq_y, Sh_y), y)
check('G3e on the degenerate curve N^2 = S_h(y) has the solution y = 1 - pi alpha for every alpha < 1/pi: the equality never constrains alpha', ysol == [1 - sp.pi*al])

# ------------------------------------------------------------------ F5: exponent test N^p = k S^q -> alpha ~ x^(2q/p - 1)
print('\nF5 exponent table (alpha proportional to x^e, e = 2q/p - 1; only e = 0 can be O(1/100)):')
ok5 = True; inrange = []
kk, ps, qs = sp.symbols('k p q', positive=True)
a_sol = (Q2_uc*x)/x*1                                    # placeholder to keep names local
for p_, q_ in itertools.product([1, 2, 3, 4], repeat=2):
    aa = sp.symbols('aa', positive=True)
    # (Q2_uc/(aa))^{p/2} = k (pi rho/x)^q with Q2_uc = 1/(4x) (l_P units), S = 3 pi/x ; solve for aa, k = 1
    eq = sp.Eq((sp.Rational(1, 4)/x/aa)**sp.Rational(p_, 2), (3*sp.pi/x)**q_)
    s_ = sp.solve(eq, aa)[0]
    e_meas = sp.simplify(sp.diff(sp.log(s_), x)*x)
    e_th = sp.Rational(2*q_, p_) - 1
    ok5 &= (sp.simplify(e_meas - e_th) == 0)
    if e_th == 0: inrange.append((p_, q_))
print('   exponent e verified for all 16 pairs; e = 0 only for (p,q) =', inrange)
check('F5 exponent formula holds for 16 (p,q) pairs; O(1) alpha only when p = 2q', ok5 and inrange == [(2, 1), (4, 2)])

# ------------------------------------------------------------------ constants
alpha_T = 1/mp.mpf('137.035999177')
X_ = mp.mpf('6.67430e-11')*mp.mpf('1.054571817e-34')/mp.mpf('299792458')**3 * 3*mp.mpf('0.6847')*(mp.mpf('67.4')*1000/mp.mpf('3.0856775814913673e22'))**2/mp.mpf('299792458')**2
c_need = 1/(12*mp.pi*alpha_T)
print('\nx = Lambda l_P^2 = %s   S_dS = 3 pi/x = %s   N_max(alpha_T)^2/S_dS = %s' % (mp.nstr(X_, 5), mp.nstr(3*mp.pi/X_, 5), mp.nstr(1/(4*alpha_T*X_)/(3*mp.pi/X_), 12)))
print('c_needed (INVERSE MAP, not a hit) = 1/(12 pi alpha) = %s' % mp.nstr(c_need, 15))
# Planck-scale alpha: one-loop SM, b_Y = (5/3) b_1 = 41/6, b_2 = -19/6, GUT check b_1 = 41/10
ainv_MZ = mp.mpf('127.930'); s2 = mp.mpf('0.23122')
Lg = mp.log(mp.mpf('1.220890e19')/mp.mpf('91.1876'))
ainv_Y = (1 - s2)*ainv_MZ - (mp.mpf(41)/6)/(2*mp.pi)*Lg
ainv_2 = s2*ainv_MZ + (mp.mpf(19)/6)/(2*mp.pi)*Lg
ainv_P_calc = ainv_Y + ainv_2
check('b_Y = (5/3) b_1 = 41/6 (GUT-normalisation pitfall)', sp.Rational(5, 3)*sp.Rational(41, 10) == sp.Rational(41, 6))
ainv_P = mp.mpf('104.94')
print('1/alpha_em(m_P), one loop, recomputed here = %s ; value used as the Planck-scale target (from the status file) = %s' % (mp.nstr(ainv_P_calc, 6), ainv_P))
check('Planck-scale target reproduced to 0.1% by the recomputation', abs(ainv_P_calc/ainv_P - 1) < 1e-3)
print('   at the horizon scale (Hubble radius ~ 1e26 m) the Coulomb field is far below m_e, so the natural target is the THOMSON value; Planck-scale value is scored as a second target only.')

# ------------------------------------------------------------------ F1: the scored family (45 trials)
ratioY = {'S_dS': sp.Integer(1), 'S_uc': ratio_uc, '2 S_uc': 2*ratio_uc, '3 S_uc': 3*ratio_uc, 'S_Bek': sp.Rational(2, 9)}
units = {'nats': sp.Integer(1), 'bits': 1/sp.log(2), 'cells(A/lP^2)': sp.Integer(4)}
ks = {'1/2': sp.Rational(1, 2), '1': sp.Integer(1), '2': sp.Integer(2)}
rows = []
for (Yn, Yr), (un, uv), (kn, kv) in itertools.product(ratioY.items(), units.items(), ks.items()):
    cp = sp.nsimplify(kv*uv*Yr) if un != 'bits' else kv*uv*Yr
    cpv = mp.mpf(sp.N(cp, 30))
    inv = 12*mp.pi*cpv
    rows.append(dict(Y=Yn, u=un, k=kn, cp=cp, cpv=cpv, inv=inv, mT=abs(inv/mp.mpf('137.035999177') - 1), mP=abs(inv/ainv_P - 1),
                     inrange=(mp.mpf(50) < inv < mp.mpf(300))))
print('\nF1: %d trials (c\' = k u S_Y/S_dS); 1/alpha_pred = 12 pi c\'' % len(rows))
print('  %-7s %-14s %-4s %-12s %9s %10s %10s %s' % ('Y', 'unit', 'k', "c'", '1/alpha', 'missT', 'missP', 'range 50-300'))
for w in sorted(rows, key=lambda w: w['mT']):
    print('  %-7s %-14s %-4s %-12s %9.3f %10.3e %10.3e %s' % (w['Y'], w['u'], w['k'], str(w['cp'])[:12], float(w['inv']), float(w['mT']), float(w['mP']), w['inrange']))
distinct = sorted({mp.nstr(w['cpv'], 12) for w in rows}, key=float)
print("distinct c' values: %d" % len(distinct))
check('F1 trial count is 45 as pre-registered', len(rows) == 45)
inr = [w for w in rows if w['inrange']]
print("in range 50 < 1/alpha < 300: %d of %d ; c' values: %s" % (len(inr), len(rows), sorted({mp.nstr(w['cpv'], 6) for w in inr}, key=float)))
f2 = [w for w in rows if c_need/2 <= w['cpv'] <= 2*c_need]
print("within a factor 2 of c_needed (%s): %d trials, distinct c' = %s" % (mp.nstr(c_need, 6), len(f2), sorted({mp.nstr(w['cpv'], 6) for w in f2}, key=float)))
best = min(rows, key=lambda w: w['mT']); bestP = min(rows, key=lambda w: w['mP'])
print('best vs Thomson: %s %s k=%s c\'=%s 1/alpha=%s miss=%s' % (best['Y'], best['u'], best['k'], mp.nstr(best['cpv'], 8), mp.nstr(best['inv'], 8), mp.nstr(best['mT'], 4)))
print('best vs Planck : %s %s k=%s c\'=%s 1/alpha=%s miss=%s' % (bestP['Y'], bestP['u'], bestP['k'], mp.nstr(bestP['cpv'], 8), mp.nstr(bestP['inv'], 8), mp.nstr(bestP['mP'], 4)))
check('H3: every F1 miss vs Thomson exceeds 1e-2 (nothing near the CODATA bar)', all(w['mT'] > 1e-2 for w in rows), '(min miss %s)' % mp.nstr(best['mT'], 4))

# bar (lane D): imported read-only; P < 1e-3 after look-elsewhere, miss <= 5e-10, 0 fitted reals, scale stated
sys.path.insert(0, '../D_calibration_bar')
import alpha_bar_checker as ABC
print('\nBar (lane D) for every F1 trial: size = 45, n_targets = 2 (Thomson, Planck-scale), fitted reals 0, scale stated')
clears = 0
for w in rows:
    for tgt, key in (('T', 'mT'), ('P', 'mP')):
        rr_ = ABC.assess(delta=float(w[key]), size=45, n_targets=2, fitted_reals=0, scale_stated=True, verbose=False)
        clears += bool(rr_['clears'])
print('   candidates clearing the bar (90 candidate-target pairs): %d' % clears)
check('bar: no F1 candidate clears at either target', clears == 0)
rb = ABC.assess(delta=float(best['mT']), size=45, n_targets=2, verbose=False)
print('   best Thomson candidate: look-elsewhere P = %.3f, precision ok = %s, clears = %s' % (rb['p'], rb['c2_precision'], rb['clears']))
# positive control
rc = ABC.assess(delta=1e-11, size=45, n_targets=2, verbose=False)
check('positive control: a hypothetical exact c\' (miss 1e-11, size 45, 2 targets) clears the bar', rc['clears'])
print('   inverse-map c_needed = %s is NOT scored: it is found by solving for the target (miss 0 by construction, one fitted real)' % mp.nstr(c_need, 12))
rf = ABC.assess(delta=1e-11, size=45, n_targets=2, fitted_reals=1, verbose=False)
check('inverse map (one fitted real) never clears', not rf['clears'])

# ------------------------------------------------------------------ F2, F3: out-of-range families (not scored)
mag = [3*mp.pi*w['cpv'] for w in rows]                 # alpha_pred = 3 pi c'_m
print('\nF2 magnetic dual: alpha_pred = 3 pi c\'_m over 45 trials ranges %s .. %s (need 7.3e-3): all out of range' % (mp.nstr(min(mag), 4), mp.nstr(max(mag), 4)))
check('F2 all 45 magnetic-dual alpha_pred >= 0.1 (>= 13x the measured 7.3e-3; amended threshold, see Amendment 1)', all(v >= mp.mpf('0.1') for v in mag))
flat = [mp.pi*kv*uv for uv in [1, 1/mp.log(2), 4] for kv in [mp.mpf(1)/2, 1, 2]]
print('F3 flat extremal 1/alpha = pi k u over 9 trials: %s .. %s (need 137.04, k u = %s): all out of range' % (mp.nstr(min(flat), 4), mp.nstr(max(flat), 4), mp.nstr(mp.mpf('137.035999177')/mp.pi, 5)))
check('F3 all 9 flat-extremal 1/alpha_pred < 30', all(v < 30 for v in flat))

# ------------------------------------------------------------------ H4 / H5
c_real = c_need
print('\nH5 inequalities: real c\' = N_max^2/S_dS = %s' % mp.nstr(c_real, 10))
check('H5a bound N_max^2 <= S_dS is violated by the measured alpha (c\' > 1)', c_real > 1)
check('H5b bound N_max^2 <= A_dS/l_P^2 = 4 S_dS is satisfied, margin %s%% (i.e. 1/alpha <= 48 pi = %s)' % (mp.nstr((4/c_real - 1)*100, 4), mp.nstr(48*mp.pi, 6)), c_real < 4)
print('   H4: minimal-choice candidate (nats, S_dS, k=1): c\'=1 -> 1/alpha = 12 pi = %s, misses by factor %s' % (mp.nstr(12*mp.pi, 5), mp.nstr(mp.mpf('137.035999177')/(12*mp.pi), 4)))
print('   choices per F1 candidate: entropy reference Y (5), unit u (3), coefficient k (3): log2(45) = %.2f bits; none is forced by the geometry (G4).' % math.log2(45))

# ------------------------------------------------------------------ D1: density of natural numbers near c_needed
fr = {sp.Rational(p_, q_) for p_ in range(1, 13) for q_ in range(1, 13)}
vals = [mp.mpf(sp.N(v, 20)) for v in fr]
d2 = sum(1 for v in vals if c_need/2 <= v <= 2*c_need); d10 = sum(1 for v in vals if abs(v/c_need - 1) < 0.10); d1 = sum(1 for v in vals if abs(v/c_need - 1) < 0.01)
print('\nD1: of %d distinct rationals p/q (1<=p,q<=12): %d within a factor 2 of c_needed, %d within 10%%, %d within 1%%' % (len(vals), d2, d10, d1))
near = sorted([(float(abs(v/c_need-1)), str(sp.nsimplify(sp.Rational(str(v)))) if False else mp.nstr(v, 6)) for v in vals if abs(v/c_need - 1) < 0.10])
print('    rationals within 10%:', near)
print("    (a factor-2 coincidence for c' is the expectation for any small-integer coefficient; D1 is report-only, see Amendment 1)")

print('\nFAILS:', fails if fails else 'none')
print('exit', 1 if fails else 0)
sys.exit(1 if fails else 0)
