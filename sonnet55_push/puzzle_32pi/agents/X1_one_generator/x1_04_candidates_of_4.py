#!/usr/bin/env python3
"""x1_04_candidates_of_4.py -- lane X1 task (2): candidate origins of the '4' in  32 pi = 8 pi x 4  (equivalently G rho_Lambda = 4 a0^2), each with SECOND,
independent predictions that could FAIL.  PRE-DECLARED (before any evaluation):

CANDIDATES (each is a structural claim with a D-lift N_c(D), N_c(4) = 4):
  c1  TRACE       4 = delta^mu_mu = D                    (T^mu_mu = -4 rho_Lambda)                        N = D
  c2  SPIN2       4 = s^2, s = 2 (graviton spin, D-indep)                                                   N = 4
  c3  POL         4 = (number of graviton polarisations)^2                                                  N = (D(D-3)/2)^2
  c4  SPHERE/DISC 4 = 4 pi/pi = area(S^{D-2}) / area(equatorial disc)                                       N = Omega_{D-2}/Vol(B^{D-2})
  c5  THERMO      4 = 8 pi/2 pi = Einstein coupling / thermal period  (the Bekenstein-Hawking quarter)     N = 4
  c6  QUAD-EH     4 = 1/(1/4), the second-order Einstein-Hilbert coefficient of a TT wave                   N = 4
  c7  HORIZON     4 = (r_h kappa)^-2 for a Schwarzschild(-Tangherlini) horizon                              N = (2/(D-3))^2
  c8  CHANNELS    4 = number of static-patch generators 1 + dim SO(D-1)                                     N = 1 + (D-1)(D-2)/2
  c9  GB-SHIFT    4 = 2(D-2)(D-3)  (MacDowell-Mansouri algebra)                                             N = 2(D-2)(D-3)
  c10 RESPONSE    4 = N_resp^2 with the response exponent N_resp = 2 (mu = 1 - (1-p)^N; 'two static channels')  N = 4

TESTS (each candidate is scored; a test a candidate cannot meet is a FAIL, a test that does not apply is n/a):
  S1  D-lift equals the graviton/Bekenstein-Hawking slot (constant 4) for D = 4..8      [if the puzzle's 4 shares the origin of kappa_g^2 = 8 pi G x 4]
  S2  D-lift equals the Tangherlini slot (2/(D-3))^2                                      [if it shares the horizon origin]
  S3  D-lift equals the MM/GB-shift slot 2(D-2)(D-3)                                      [if it shares the Euler-algebra origin]
  S4  a0(z): does the origin refer to the TOTAL source or to Lambda alone?  (flat vs evolving prediction, computed)
  S5  horizon-family extremality (Kerr-Newman D=4, Reissner-Nordstrom D=4,5, Myers-Perry single spin D=4,5,6): is the neutral static horizon the extremum?
  S6  convention-N version of S1: G_N instead of G_E (kappa_g^2/(8 pi G_N) = 4 G_E/G_N)
And a DECOY control for the whole exercise: how many low-complexity D-formulas equal 4 at D = 4 (agreement at D = 4 is worth almost nothing).
Exit 0 iff every check and control behaves as declared.  Needs x1_dlifts.json.
"""
import sys, json, itertools, time
import numpy as np
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name, flush=True)
def ctl(name, cond_rejected):
    ok.append(bool(cond_rejected)); print(("PASS CONTROL " if cond_rejected else "FAIL CONTROL ") + name, flush=True)
here = __file__.rsplit('/', 1)[0]
dl = json.load(open(here + '/x1_dlifts.json'))
T0 = time.time()
pi = sp.pi
Ds = (4, 5, 6, 7, 8)
Om = lambda n: sp.simplify(2 * pi ** sp.Rational(n + 1, 2) / sp.gamma(sp.Rational(n + 1, 2)))
Vb = lambda n: pi ** sp.Rational(n, 2) / sp.gamma(sp.Rational(n, 2) + 1)

# ---------------------------------------------------------------- candidate D-lifts (pre-declared formulas) and the slots (computed in x1_02)
cand = {
    'c1 TRACE':        lambda D: sp.Integer(D),
    'c2 SPIN2':        lambda D: sp.Integer(4),
    'c3 POL':          lambda D: sp.Integer((D * (D - 3) // 2) ** 2),
    'c4 SPHERE/DISC':  lambda D: sp.simplify(Om(D - 2) / Vb(D - 2)),
    'c5 THERMO':       lambda D: sp.simplify(8 * pi / (2 * pi)),
    'c6 QUAD-EH':      lambda D: sp.Integer(4),
    'c7 HORIZON':      lambda D: sp.Rational(4, (D - 3) ** 2),
    'c8 CHANNELS':     lambda D: sp.Integer(1 + (D - 1) * (D - 2) // 2),
    'c9 GB-SHIFT':     lambda D: sp.Integer(2 * (D - 2) * (D - 3)),
    'c10 RESPONSE':    lambda D: sp.Integer(2) ** 2,
}
slot_G = {D: sp.Integer(4) for D in Ds}                                       # graviton kappa_g^2/(8 pi G_E) = 4 and S = A/4G  (x1_02 L4, L5)
slot_T = {D: sp.Rational(dl['Tang_inv_sq'][str(D)]) for D in Ds}              # x1_02 L6
slot_M = {D: sp.Integer(2 * (D - 2) * (D - 3)) for D in Ds}                   # x1_02 L8
GNGE = {D: sp.sympify(dl['GN_over_GE'][str(D)]) for D in Ds}                  # G_N/G_E  (x1_02 L3)
slot_GN = {D: sp.simplify(4 / GNGE[D]) for D in Ds}                           # kappa_g^2/(8 pi G_N) = 4 G_E/G_N   (G_N = force-law constant, Omega_{D-2} G_N rho = Lap Phi)
slot_GN4 = {D: sp.Rational(2 * (D - 2), (D - 3)) for D in Ds}                 # same with the 4 pi-normalised Poisson constant (Lap Phi = 4 pi G_N' rho, G_N' = 2 (D-3) G_E/(D-2)):  4 G_E/G_N' = 2 (D-2)/(D-3)
# sanity: the slots as computed equal the closed forms
chk("D0 slot values at D = 4: graviton 4, Tangherlini 4, MM-shift 4, convention-N graviton 4 (all four equal 4 at D = 4 only)",
    slot_G[4] == slot_T[4] == slot_M[4] == slot_GN[4] == 4 and slot_G[5] != slot_T[5] and slot_T[5] != slot_M[5] and slot_G[5] != slot_M[5])
eq = lambda a, b: all(sp.simplify(a[D] - b[D]) == 0 for D in Ds)
print("\n  D-lift table (D = 4,5,6,7,8):")
res = {}
c4vec = {D: sp.simplify(cand['c4 SPHERE/DISC'](D)) for D in Ds}
for name, fn in cand.items():
    vec = {D: sp.simplify(fn(D)) for D in Ds}
    assert vec[4] == 4, name
    s1, s2, s3, s6 = eq(vec, slot_G), eq(vec, slot_T), eq(vec, slot_M), eq(vec, slot_GN)
    res[name] = dict(vec=vec, S1=s1, S2=s2, S3=s3, S6=s6)
    print("   %-16s %-44s S1 %s  S2 %s  S3 %s  S6(G_N) %s" % (name, [str(vec[D]) for D in Ds], s1, s2, s3, s6))
chk("D1 every candidate equals 4 at D = 4 (by construction: the exercise cannot separate them at D = 4)", all(res[n]['vec'][4] == 4 for n in res))
chk("D2 S1 (graviton/BH constant-4 slot): passed by c2, c5, c6, c10 (all D-independent), failed by c1, c3, c4, c7, c8, c9",
    [n for n in res if res[n]['S1']] == ['c2 SPIN2', 'c5 THERMO', 'c6 QUAD-EH', 'c10 RESPONSE'])
chk("D3 S2 (Tangherlini slot): passed only by c7 (its own definition); S3 (MM slot): only by c9 (its own definition)",
    [n for n in res if res[n]['S2']] == ['c7 HORIZON'] and [n for n in res if res[n]['S3']] == ['c9 GB-SHIFT'])
agree = [D for D in Ds if sp.simplify(c4vec[D] - slot_GN[D]) == 0]
agree4 = [D for D in Ds if sp.simplify(c4vec[D] - slot_GN4[D]) == 0]
chk("D4b S6': with the 4 pi-normalised Poisson constant (Lap Phi = 4 pi G_N' rho) the sphere/disc ratio agrees with the graviton slot 2(D-2)/(D-3) at D = %s only (the D = 5 coincidence is convention-dependent)" % agree4, agree4 == [4])
chk("D4 S6: in the Newton-G convention the sphere/disc ratio equals kappa_g^2/(8 pi G_N) at D = %s only (D = 5 is a coincidence: Vol(B^3) = 2 pi (D-3)/(D-2)); it fails for D = 6, 7, 8" % agree, agree == [4, 5])
ctl("D4 CONTROL: c1 (N = D) is not the graviton 4 at D = 5", res['c1 TRACE']['vec'][5] != slot_G[5])
print("   => no candidate other than the D-independent class {c2, c5, c6, c10} survives the one-generator premise (puzzle 4 = graviton 4 in every D); c4 survives only in convention N at D = 4, 5.")

# ---------------------------------------------------------------- S4: a0(z) under 'trace of the TOTAL source' versus 'Lambda alone' versus 'H(z)-tracking'
Om_m, Om_L = 0.315, 0.685
def ratios(z):
    rho_m = Om_m * (1 + z) ** 3
    flat = 1.0
    trace_total = np.sqrt((rho_m + 4 * Om_L) / (Om_m + 4 * Om_L))
    hz = np.sqrt(rho_m + Om_L)
    return flat, trace_total, hz
print("\n  S4  a0(z)/a0(0) under three readings of the variable held fixed (flat LCDM, Om_m = %.3f, radiation neglected):" % Om_m)
print("      z      Lambda-alone(flat)   trace of total stress-energy (c1 on the whole source)   a0 ~ H(z)")
for z in (0.0, 0.5, 1.0, 2.0, 2.5, 3.0):
    a, b, c_ = ratios(z)
    print("      %-4.1f   %-19.3f  %-54.3f %.3f" % (z, a, b, c_))
a25 = ratios(2.5)
chk("S4 c1 read on the total source (trace = rho_m + 4 rho_Lambda) predicts an EVOLVING a0: a0(2.5)/a0(0) = %.2f (H(z)-tracking gives %.2f); read on Lambda alone it is flat (1.00)" % (a25[1], a25[2]),
    abs(a25[0] - 1) < 1e-12 and 2.2 < a25[1] < 2.4 and 3.7 < a25[2] < 3.8)
print("      at z = 0 the total-trace reading is larger than the Lambda-only reading by sqrt(1 + Om_m/(4 Om_L)) = %.4f (a 5%% shift of the fitted coefficient)" % np.sqrt(1 + Om_m / (4 * Om_L)))
print("      (other candidates fix only the COEFFICIENT, not which density enters; they are silent on a0(z).  The framework's own law is the flat column.)")

# ---------------------------------------------------------------- S5: horizon-family extremality (checks c4/c7's 'a0 = sup kappa')
# (a) Kerr-Newman D = 4 : A kappa^2 / pi = (r_+ - r_-)^2 / (r_+^2 + a^2),  r_+ r_- = a^2 + Q^2  (G = 1).  Symbolic: 1 - A kappa^2/pi = (a^2 + r_-(2 r_+ - r_-)... ) / (r_+^2 + a^2)
rp, rm, a, Q = sp.symbols('r_p r_m a Q', positive=True)
Akap = (rp - rm) ** 2 / (rp ** 2 + a ** 2)
gap = sp.simplify((rp ** 2 + a ** 2) - (rp - rm) ** 2)                         # >= 0  <=>  A kappa^2 <= pi
chk("S5a Kerr-Newman: (r_+^2 + a^2) - (r_+ - r_-)^2 = a^2 + r_-(2 r_+ - r_-) >= 0 for 0 <= r_- <= r_+, with equality iff a = 0 and r_- = 0 (Schwarzschild):  %s" % gap,
    sp.simplify(gap - (a ** 2 + rm * (2 * rp - rm))) == 0)
rng = np.random.default_rng(2718)
worst = 0.0; nsamp = 200000; mx = 0.0
for _ in range(nsamp):
    rminus = rng.uniform(0, 1); aa = rng.uniform(0, 1); QQ2 = rminus * 1.0 - aa ** 2       # r_+ = 1 : a^2 + Q^2 = r_-
    if QQ2 < 0:
        continue
    val = (1 - rminus) ** 2 / (1 + aa ** 2)
    mx = max(mx, val)
chk("S5a numerically (2e5 random KN horizons, r_+ = 1): max A kappa^2/pi = %.6f <= 1, sup attained by the neutral static member" % mx, mx <= 1.0 + 1e-12)
ctl("S5a CONTROL: the bound A kappa^2/pi <= 1/2 would be violated (the sample maximum is %.3f): the scan can fail" % mx, mx > 0.5)
# consequence: mean Gauss curvature Kbar = 4 pi / A (Gauss-Bonnet, any S^2 horizon) => kappa <= (1/2) sqrt(Kbar)
Kbar, A_, kp = sp.symbols('Kbar A kappa', positive=True)
chk("S5a => with Kbar = 4 pi/A (2-d Gauss-Bonnet, any topological S^2), A kappa^2 <= pi reads  kappa <= (1/2) sqrt(Kbar)  (G = c = 1):  a0 = (1/2) sqrt(rho_Lambda) is the SUP of kappa over KN horizons with Kbar = rho_Lambda",
    sp.simplify((sp.pi / (4 * pi / Kbar)) - Kbar / 4) == 0)
# (b) Reissner-Nordstrom in D = 4, 5, 6: r_+ = 1, mu = 1 + q^2 (f(1) = 0), kappa = (D-3)(1 - q^2)/2, q^2 in [0, 1]
q2 = sp.symbols('q2', positive=True)
for D in (4, 5, 6):
    fRN = lambda r: 1 - (1 + q2) / r ** (D - 3) + q2 / r ** (2 * (D - 3))
    rr = sp.symbols('rr', positive=True)
    kap = sp.simplify(sp.diff(fRN(rr), rr).subs(rr, 1) / 2)
    F = sp.simplify(Om(D - 2) * kap ** (D - 2))                                # A kappa^(D-2) at r_+ = 1
    dF = sp.simplify(sp.diff(F, q2))
    chk("S5b RN D=%d: kappa r_+ = (D-3)(1 - q^2)/2 = %s; A kappa^(D-2) = %s decreasing in q^2 in [0,1], maximal at q = 0 (Tangherlini)" % (D, kap, F),
        sp.simplify(kap - sp.Rational(D - 3, 2) * (1 - q2)) == 0 and all(dF.subs(q2, v) < 0 for v in (0.1, 0.5, 0.9)))
# (c) Myers-Perry, single spin, D = 4..7: A = Omega_{D-2} (r_+^2 + a^2) r_+^{D-4},  kappa = ((D-3) r_+^2 + (D-5) a^2)/(2 r_+ (r_+^2 + a^2)).
# (formulas quoted from the standard MP literature; VERIFIED here only by the two limits below: D = 4 Kerr and a = 0 Tangherlini)
# D = 4: a <= r_+ (x <= 1, extremal Kerr at x = 1); D >= 5: x = a/r_+ is unbounded (extremal / ultraspinning limit x -> infinity)
xx = sp.symbols('x', nonnegative=True)
mp_out = {}
for D in (4, 5, 6, 7):
    Ax = Om(D - 2) * (1 + xx ** 2)                                             # r_+ = 1
    kx = ((D - 3) + (D - 5) * xx ** 2) / (2 * (1 + xx ** 2))
    Fx = sp.simplify(Ax * kx ** (D - 2))
    F0 = float(sp.N(Fx.subs(xx, 0)))
    grid = [0.0, 0.1, 0.3, 0.5, 0.8, 1.0] if D == 4 else [0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0]
    vals = [float(sp.N(Fx.subs(xx, v))) for v in grid]
    limits_ok = True
    if D == 4:
        Msym = (1 + xx ** 2) / 2                                              # Kerr: 2 M r_+ = r_+^2 + a^2, r_+ = 1
        limits_ok = sp.simplify(kx - (1 - Msym) / (2 * Msym)) == 0 and sp.simplify(Ax - 8 * pi * Msym) == 0
    tang_ok = sp.simplify(kx.subs(xx, 0) - sp.Rational(D - 3, 2)) == 0 and sp.simplify(Ax.subs(xx, 0) - Om(D - 2)) == 0
    # independent check of the quoted kappa, A, Omega_H: Smarr (D-3) M = (D-2)(kappa A/(8 pi) + Omega_H J),  M = (D-2) Omega_{D-2} mu/(16 pi), J = 2 M a/(D-2), mu = r_+^(D-5)(r_+^2 + a^2)
    a_ = xx; mu_ = (1 + a_ ** 2); M_ = (D - 2) * Om(D - 2) * mu_ / (16 * pi); J_ = 2 * M_ * a_ / (D - 2); OmH = a_ / (1 + a_ ** 2)
    smarr_ok = sp.simplify((D - 3) * M_ - (D - 2) * (kx * Ax / (8 * pi) + OmH * J_)) == 0
    smarr_bad = sp.simplify((D - 3) * M_ - (D - 2) * (2 * kx * Ax / (8 * pi) + OmH * J_)) != 0
    ctl("S5c Myers-Perry D=%d Smarr identity (D-3)M = (D-2)(kappa A/8pi + Omega_H J) holds for the quoted kappa, A (and would fail with kappa doubled): validates the formulas" % D, smarr_ok and smarr_bad)
    below = all(v <= F0 + 1e-9 for v in vals)
    mp_out[D] = below
    expected = D in (4, 5)
    chk("S5c Myers-Perry single spin D=%d: A kappa^(D-2) never exceeds its a = 0 (Tangherlini) value %.4f over the tested spins (max %.4f): %s; declared expectation: %s (Kerr/Tangherlini limits %s)"
        % (D, F0, max(vals), below, 'extremum at Tangherlini' if expected else 'FAILS (ultraspinning branch: A grows at fixed kappa)', limits_ok and tang_ok),
        limits_ok and tang_ok and (below == expected))
print("      => the 'neutral static horizon maximises A kappa^(D-2)' statement holds for KN (D=4), RN (D=4,5,6) and single-spin MP at D = 4, 5, and FAILS for MP at D = 6, 7 (ultraspinning): the 'sup kappa' reading of c7 is a D <= 5 statement, and Kbar = 4 pi/A is topological only at D = 4.")

# ---------------------------------------------------------------- DECOY control: how special is 'equals 4 at D = 4'?
factors = [lambda D: D, lambda D: D - 1, lambda D: D - 2, lambda D: D - 3]
names = ['D', 'D-1', 'D-2', 'D-3']
pool = []
for cc in (sp.Rational(1, 4), sp.Rational(1, 2), sp.Integer(1), sp.Integer(2), sp.Integer(4)):
    pool.append((str(cc), lambda D, cc=cc: cc))
    for i, e in itertools.product(range(4), (-2, -1, 1, 2)):
        pool.append(("%s*(%s)^%d" % (cc, names[i], e), lambda D, cc=cc, i=i, e=e: cc * sp.Integer(factors[i](D)) ** e))
    for (i, ei), (j, ej) in itertools.combinations(list(itertools.product(range(4), (-1, 1, 2))), 2):
        if i < j:
            pool.append(("%s*(%s)^%d*(%s)^%d" % (cc, names[i], ei, names[j], ej), lambda D, cc=cc, i=i, ei=ei, j=j, ej=ej: cc * sp.Integer(factors[i](D)) ** ei * sp.Integer(factors[j](D)) ** ej))
pool = [(n, f) for n, f in pool]
print("\n  DECOY control: pool of %d pre-declared D-formulas c*(D+a)^e [*(D+b)^f], c in {1/4,1/2,1,2,4}: how many hit each target at D = 4, and are non-constant?" % len(pool))
hits = {}
for tgt in (2, 3, 4, 6, 8, 12):
    n_hit = 0; n_nonconst = 0
    for n, f in pool:
        try:
            v4 = f(4)
        except ZeroDivisionError:
            continue
        if v4 == tgt:
            n_hit += 1
            try:
                if f(5) != v4 or f(6) != v4:
                    n_nonconst += 1
            except ZeroDivisionError:
                n_nonconst += 1
    hits[tgt] = (n_hit, n_nonconst)
    print("      target %-3d : %3d formulas equal it at D = 4, of which %3d are D-dependent" % (tgt, n_hit, n_nonconst))
chk("X1 agreement at D = 4 is cheap: %d pre-declared D-formulas (%d of them D-dependent) equal 4 at D = 4, and the decoy targets 2, 3, 6, 8, 12 are hit %s times: 4 is not special"
    % (hits[4][0], hits[4][1], [hits[t][0] for t in (2, 3, 6, 8, 12)]), hits[4][1] >= 10 and min(hits[t][0] for t in (2, 3, 6, 8, 12)) >= 5)
print("      (this pool is a control for how weak D = 4 evidence is; it is NOT used to select a candidate.  The candidate list itself was written knowing the target.)")

print("\n  SCORE TABLE (S1 const-4 slot, S2 Tangherlini slot, S3 MM slot, S4 total-source a0(z), S5 extremal, S6 G_N-slot)")
tab = {
 'c1 TRACE':       'S1 FAIL, S2 FAIL, S3 FAIL, S6 FAIL;  S4: total-trace reading contradicts the flat law (a0(2.5)/a0(0) = 2.31), Lambda-only reading is flat.  -> orphan at D != 4',
 'c2 SPIN2':       'S1 pass (D-independent);  S2-S3 n/a;  no mechanism (spin does not enter any coefficient)',
 'c3 POL':         'S1-S3, S6 FAIL -> orphan',
 'c4 SPHERE/DISC': 'S1 FAIL; S6 pass only at D = 4, 5 (coincidence), fails D >= 6; its horizon reading is c7 (S5)',
 'c5 THERMO':      'S1 pass (D-independent; Wald S = A/4G in every D);  the same 8 pi/2 pi that gives T = kappa/2 pi and S = A/4',
 'c6 QUAD-EH':     'S1 pass (D-independent; TT quarter computed D = 4..8)',
 'c7 HORIZON':     'S2 pass (own slot); S1 FAIL; S5: neutral static horizon extremises A kappa^(D-2) for KN (D=4), RN (D=4,5,6), MP (D=4,5) but NOT MP at D = 6, 7',
 'c8 CHANNELS':    'S1-S3, S6 FAIL -> orphan; no coefficient in any action counts Killing generators',
 'c9 GB-SHIFT':    'S3 pass (own slot); S1 FAIL; the MM closure exists only at D = 4 (x1_02 L8)',
 'c10 RESPONSE':   'S1 pass (constant 4); n/a otherwise; equals the record d-lock (kappa = 1/2 in every d)',
}
for k, v in tab.items():
    print("   %-16s %s" % (k, v))
print("\n%d/%d checks and controls behave as declared  (%.1f s)" % (sum(ok), len(ok), time.time() - T0))
sys.exit(0 if all(ok) else 1)
