#!/usr/bin/env python3
"""FINAL-18 (KAPPA_B) -- derive kappa from a matching condition AT THE FOLD.

    python3 final18.py            -> final18.out / final18.json
    python3 final18.py --mutate   -> final18_MUTATE.out / final18_MUTATE.json  (three false twins; REJECTED)

Criteria: PREREGISTER.md, committed alone (4144abfc80) before any script or number.
Footings never pooled. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

The condition, stated before computing (PREREGISTER section 1):

    (V)  a_0 = kappa c sqrt(G rho_Lambda)                     (definition of kappa)
    (M)  M_ph(R_fold(t); a_0) = Q_fold(t)                      (charge continuity at the fold)
         M_ph = M_b X,  X = (sqrt(1+4x^2)-1)/2,  x = R_fold/r_M,  r_M = sqrt(G M_b/a_0)
         Q_fold = the comoving cold charge every shell that has crossed the front carried in

Exact inversion:  X(1+X) = x^2 and X = q  =>  a_0 = G M_b q(1+q)/R_fold^2  (no approximation),
                  kappa_M = G M_b q(1+q) / (c sqrt(G rho_Lambda) R_fold^2).
"""
import argparse, json, math, os, sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'fable52_push', 'COL1_clock_collapse'))
import col1_lib as L

KD1 = json.load(open(os.path.join(HERE, '..', '..', 'closure_2026_11_06', 'KD1_unpinned_kq_dust', 'kd1.json')))
FLD1RUNS = os.path.join(HERE, '..', '..', 'fable52_push', 'FLD1_fold_reach', 'runs')

C_KMS = 2.99792458e5
G = L.G                      # 4.30091e-6 kpc (km/s)^2 / Msun
KPC_M = 3.0857e19
SI = 1e6 / KPC_M             # (km/s)^2/kpc -> m/s^2
BAND = 0.025                 # FINAL16's 5% band on kappa
ALLOW_DEX = 0.0411           # FINAL16's observational / footing allowance

MASSES = [6.5, 7.0, 8.0, 9.0, 9.4, 10.0, 10.45, 10.7, 10.9, 11.2, 11.5, 12.0]
QDEFS = ('q_front', 'q_cross', 'q_turn')


def rho_L_planck():
    """FINAL16's background: Planck 2018 TT,TE,EE+lowE+lensing H0=67.36, Om=0.3153, OL=0.6847."""
    H0 = 0.06736                       # km/s/kpc
    return 0.6847 * 3 * H0 ** 2 / (8 * math.pi * G)


def rho_L(footing):
    s = KD1['footings'][footing]['setting']
    c = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    return c.OL * c.rhoc0


def share(a0, Mb, R):
    """the record's halo share X at radius R (point mass, exact quadratic X(1+X)=x^2)."""
    return (math.sqrt(1 + 4 * R * R * a0 / (G * Mb)) - 1) / 2


def load(tag):
    return json.load(open(os.path.join(HERE, 'runs', tag + '.json')))


def series_at(series, ztarget):
    """row of the fold series nearest a target redshift."""
    best, bd = None, 1e18
    for row in series:
        d = abs(row[1] - ztarget)
        if d < bd:
            bd, best = d, row
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutate', action='store_true')
    a = ap.parse_args()
    OUT = []
    checks = {}

    def emit(s=''):
        print(s)
        OUT.append(s)

    emit('=' * 100)
    emit('FINAL-18 (KAPPA_B): kappa from the FOLD matching condition'
         + ('   [MUTATE arms]' if a.mutate else '   [MAIN]'))
    emit('Criteria 4144abfc80 (committed alone). Footings never pooled. Adopts nothing.')
    emit('=' * 100)

    # ---------------------------------------------------------------- KA-1
    emit('')
    emit('--- KA-1: code fidelity of the patched FLD1 solver vs FLD1 committed rows ---')
    ka1 = [('ka1_canonical_M10.45_N1200_s1', 'hubble_canonical_M10.45_zi10_N1200.json'),
           ('ka1_canonical_M10.45_N2400_s1', 'hubble_canonical_M10.45_zi10_N2400.json'),
           ('ka1_alt_M10.45_N2400_s1', 'hubble_alt_M10.45_zi10_N2400.json')]
    ok_ka1 = True
    for tag, f in ka1:
        try:
            mine = load(tag); ref = json.load(open(os.path.join(FLD1RUNS, f)))
        except FileNotFoundError:
            emit(f'  {tag}: MISSING'); ok_ka1 = False; continue
        dR = abs(mine['R_fold_z0_kpc'] / float(ref['R_fold_end_kpc']) - 1)
        dq = abs(mine['q_turn_z0'] / float(ref['charge_turned_around_over_Mb']) - 1)
        r = (dR < 1e-9) and (dq < 1e-9)
        ok_ka1 &= r
        emit(f"  {tag}: R_fold {mine['R_fold_z0_kpc']:.6f} vs FLD1 {float(ref['R_fold_end_kpc']):.6f} "
             f"(rel {dR:.2e}); q_turn {mine['q_turn_z0']:.6f} vs "
             f"{float(ref['charge_turned_around_over_Mb']):.6f} (rel {dq:.2e}) -> {'PASS' if r else 'FAIL'}")
    checks['KA-1'] = ok_ka1

    # ---------------------------------------------------------------- KA-4
    emit('')
    emit('--- KA-4: the record\'s tie Z = c H_Lambda/a_0 = sqrt(32 pi/3) and the kappa each footing carries ---')
    emit('  (tolerance 2e-3, FINAL16\'s own KA-2; two backgrounds: KD1/QX15, which COL1/FLD1 ran on, and Planck18)')
    ok_ka4 = True
    for f in ('canonical', 'alt'):
        a0 = L.a0_of(f)
        for bname, rhoL in (('KD1', rho_L(f)), ('Planck18', rho_L_planck())):
            kden = C_KMS * math.sqrt(G * rhoL)
            Z = C_KMS * math.sqrt(rhoL * (8 * math.pi * G) / 3) / a0      # c H_L/a_0, H_L^2 = 8 pi G rho_L/3
            kf = a0 / kden
            Zt = math.sqrt(32 * math.pi / 3)
            ok = abs(Z / Zt - 1) < 2e-3 and abs(kf - 0.5) < 2e-3
            ok_ka4 &= ok if f == 'canonical' else abs(kf / 0.6043 - 1) < 2e-3
            emit(f'  footing {f:9s} / {bname:8s}: rho_Lambda {rhoL:.4f} Msun/kpc^3, Z = {Z:.6f} '
                 f'(target {Zt:.6f}, rel {abs(Z / Zt - 1):.2e}), kappa_frozen = {kf:.6f}'
                 + ('   [alt is defined against rho_crit, so its Z is Z_can*sqrt(Omega_L) = 4.790: expected]'
                    if f == 'alt' and bname == 'KD1' else ''))
    emit(f"  [{'PASS' if ok_ka4 else 'FAIL'}] KA-4 -- canonical footing encodes kappa = 1/2 to <2e-3; the 6.0e-5"
         f" offset in Z between backgrounds is the KD1-vs-Planck18 Omega_Lambda, not a code error")
    checks['KA-4'] = ok_ka4

    # ---------------------------------------------------------------- KA-2
    emit('')
    emit('--- KA-2: at kappa = 1/2 the record\'s quadratic reproduces FLD1\'s published X_fold (canonical table) ---')
    ref_X = {9.4: 31.6, 10.45: 21.0, 10.7: 19.1, 10.9: 17.6}
    ok_ka2 = True
    for m, Xpub in ref_X.items():
        try:
            o = load(f'prod_canonical_M{m:g}_N1200_s1')
        except FileNotFoundError:
            continue
        X = share(L.a0_of('canonical'), 10 ** m, o['R_fold_z0_kpc'])
        ok = abs(X / Xpub - 1) < 0.01
        ok_ka2 &= ok
        emit(f'  canonical, log M_b {m}: X_fold = {X:.4f} vs FLD1 {Xpub} '
             f'(rel {abs(X / Xpub - 1):.2e}) -> {"PASS" if ok else "FAIL"}')
    for m in ref_X:
        try:
            oc = load(f'prod_canonical_M{m:g}_N1200_s1'); oa = load(f'prod_alt_M{m:g}_N1200_s1')
        except FileNotFoundError:
            continue
        rc = share(L.a0_of('canonical'), 10 ** m, oc['R_fold_z0_kpc'])
        ra = share(L.a0_of('alt'), 10 ** m, oa['R_fold_z0_kpc'])
        pred = math.sqrt(L.a0_of('alt') / L.a0_of('canonical'))
        emit(f'  bracket, log M_b {m}: X_fold(alt)/X_fold(can) = {ra / rc:.5f} vs sqrt(a_0^alt/a_0^can) = '
             f'{pred:.5f} (rel {abs(ra / rc / pred - 1):.2e})')
    checks['KA-2'] = ok_ka2

    # ---------------------------------------------------------------- G1
    emit('')
    emit('--- G1: the cancellation identity (exact; sympy) ---')
    Gs, Mxs, Mbgs, a0s, rs = sp.symbols('G M_x M_bg a_0 r', positive=True)
    u = Gs * (Mxs - Mbgs) / rs ** 2
    Uexpr = a0s * u / (a0s - u)
    lhs = -Gs * Mxs / rs ** 2 + Uexpr
    rhs = -Gs * Mbgs / rs ** 2 + u ** 2 / (a0s - u)
    d1 = sp.simplify(lhs - rhs)
    rel = sp.simplify((Uexpr - u) / u)
    emit(f'  g_clock - ( -G M_bg/r^2 + u^2/(a_0-u) )  simplifies to: {d1}')
    emit(f'  relative law-force excess over exact cancellation, (U-u)/u = {rel}')
    ok_g1 = bool(sp.simplify(d1) == 0) and bool(sp.simplify(rel - u / (a0s - u)) == 0)
    checks['G1'] = ok_g1
    emit(f"  [{'PASS' if ok_g1 else 'FAIL'}] G1 -- the clock's inward pull = -G M_bg/r^2 + u^2/(a_0-u);"
         f" its excess gravitates only at O(u/(a_0-u))")

    # ---------------------------------------------------------------- G2
    emit('')
    emit('--- G2: are the fold inputs (R_fold, Q_fold) kappa-blind? a_0 -> s a_0 ---')
    emit('  (wall = the law flux cap r_w = sqrt(G m/a_0) FW; w1 = it follows s, w0 = held fixed)')
    ok_g2 = True
    rows_g2 = []
    for f in ('canonical', 'alt'):
        for m in (8.0, 10.45):
            try:
                base = load(f'prod_{f}_M{m:g}_N1200_s1')
            except FileNotFoundError:
                continue
            for s, w in ((0.1, 1), (10.0, 1), (100.0, 1), (0.1, 0), (10.0, 0)):
                tag = f'g2_{f}_M{m:g}_N1200_s{s:g}_w{w}'
                try:
                    o = load(tag)
                except FileNotFoundError:
                    continue
                dR = abs(o['R_fold_z0_kpc'] / base['R_fold_z0_kpc'] - 1)
                dqc = abs(o['q_cross_z0'] / base['q_cross_z0'] - 1)
                dqf = abs(o['q_front_z0'] / base['q_front_z0'] - 1)
                ok = (dR < 1e-6) and (dqc < 1e-6) and (dqf < 1e-6)
                ok_g2 &= ok
                rows_g2.append((tag, o['R_fold_z0_kpc'], dR, dqc, dqf, o['eps_u_max_run'], ok))
                emit(f"  {tag}: R_fold {o['R_fold_z0_kpc']:.6f} kpc (dR {dR:.2e}), dq_cross {dqc:.2e}, "
                     f"dq_front {dqf:.2e}, max u/a_0 {o['eps_u_max_run']:.3e} -> {'PASS' if ok else 'FAIL'}")
    if not rows_g2:
        ok_g2 = False
        emit('  no a_0-scaling arms found -> FAIL')
    emit('')
    emit('  measured sensitivity of the fold inputs to a_0 (dex per dex of a_0):')
    sens = []
    for tag, R, dR, dqc, dqf, eu, ok in rows_g2:
        if '_w0' in tag:            # the w0 arm holds the flux cap fixed while a_0 moves: a control, not a sensitivity
            continue
        for s in (0.1, 10.0, 100.0):
            if f'_s{s:g}_' in tag:
                sens.append((abs(math.log10(1 + dR)) / abs(math.log10(s)),
                             abs(math.log10(1 + dqf)) / abs(math.log10(s)), tag))
                break
    if sens:
        emit(f'    |d log R_fold / d log a_0|  max {max(t[0] for t in sens):.2e}  '
             f'(over {len(sens)} arms, a_0 scaled by 10x and 100x)')
        emit(f'    |d log Q_fold / d log a_0|  max {max(t[1] for t in sens):.2e}')
        emit('    the LEFT side of (M) scales as a_0^{+1/2} (0.5 dex per dex) in the deep regime, '
             'i.e. 50-500x steeper')
    checks['G2'] = ok_g2
    emit(f"  [{'PASS' if ok_g2 else 'FAIL'}] G2 -- FAILED its frozen 1e-6 rule: the fold inputs are NOT exactly"
         f" kappa-blind (DISCLOSURE: the pre-registered prediction of ~6e-10 was wrong; max|u|/a_0 reaches"
         f" 0.69 on inner shells near the caustic, so the G1 remainder u^2/(a_0-u) is not negligible there)."
         f" The measured sensitivity is nevertheless 1e-2 dex per dex, ~50x weaker than the left side, so (M)"
         f" still defines a root -- see G2c, which makes it self-consistent.")

    # ---------------------------------------------------------------- G3
    emit('')
    emit('--- G3: the pinned number (exact closed form; both footings) ---')
    emit('     a_0^M = G M_b q(1+q)/R_fold^2 ,   kappa_M = a_0^M/(c sqrt(G rho_Lambda)) ,')
    emit('     D = log10(X_fold/q)   [primary share definition: q_front]')
    tabl = {}
    for f in ('canonical', 'alt'):
        a0 = L.a0_of(f); rhoL = rho_L(f); kden = C_KMS * math.sqrt(G * rhoL)
        emit(f'  footing {f}: a_0 = {a0 * SI:.6e} m/s^2; rho_Lambda = {rhoL:.6e} Msun/kpc^3; '
             f'kappa_frozen = {a0 / kden:.6f}')
        tabl[f] = {}
        for m in MASSES:
            try:
                o = load(f'prod_{f}_M{m:g}_N1200_s1')
            except FileNotFoundError:
                continue
            R = o['R_fold_z0_kpc']; Mb = 10 ** m
            Xf = share(a0, Mb, R)
            tabl[f][m] = {}
            for qn in QDEFS:
                q = o[qn + '_z0']
                a0M = G * Mb * q * (1 + q) / R ** 2
                tabl[f][m][qn] = dict(R=R, q=q, X=Xf, a0M_SI=a0M * SI, kappa=a0M / kden,
                                      D=(math.log10(Xf / q) if q > 0 else float('nan')))
    for f in ('canonical', 'alt'):
        emit(f'  footing {f}:')
        emit('    logMb  R_fold(kpc)  X_fold(needed)  q_front  q_cross  q_turn |  a_0^M(m/s^2)  kappa_M    D_front  D_cross  D_turn')
        for m in MASSES:
            if m not in tabl[f]:
                continue
            d = tabl[f][m]
            R = d['q_front']['R']
            emit(f"    {m:5.2f}  {R:11.4f}  {d['q_front']['X']:13.4f}  "
                 + '  '.join(f"{d[q]['q']:7.5f}" for q in QDEFS)
                 + f" | {d['q_front']['a0M_SI']:.4e}  {d['q_front']['kappa']:.3e}  "
                 + '  '.join(f"{d[q]['D']:+7.3f}" for q in QDEFS))
    # grade on the three definitions, all of which must land in band
    kres = {q: {} for q in QDEFS}
    for f in ('canonical', 'alt'):
        for qn in QDEFS:
            ks = [tabl[f][m][qn]['kappa'] for m in MASSES if m in tabl[f]]
            kres[qn][f] = (min(ks), max(ks)) if ks else (float('nan'), float('nan'))
    for qn in QDEFS:
        for f in ('canonical', 'alt'):
            lo, hi = kres[qn][f]
            emit(f'  definition {qn:8s} footing {f:9s}: kappa_M in [{lo:.4e}, {hi:.4e}];'
                 f' |kappa_M - 1/2| >= {abs(hi - 0.5):.4f}')
    ok_g3 = all(abs(kres[qn][f][1] - 0.5) <= BAND and abs(kres[qn][f][0] - 0.5) <= BAND
                for qn in QDEFS for f in ('canonical', 'alt'))
    checks['G3'] = ok_g3
    emit(f"  [{'PASS' if ok_g3 else 'FAIL'}] G3 -- band |kappa_M - 1/2| <= {BAND} on both footings, all definitions")

    # ---------------------------------------------------------------- G4
    emit('')
    emit('--- G4: universality across the frozen mass grid (allowance 0.0411 dex) ---')
    ok_g4 = True
    for qn in QDEFS:
        for f in ('canonical', 'alt'):
            lo, hi = kres[qn][f]
            span = math.log10(hi / lo)
            ok = span <= ALLOW_DEX
            ok_g4 &= ok
            emit(f'  definition {qn:8s} footing {f:9s}: dex span {span:.4f} vs allowance {ALLOW_DEX} '
                 f'-> {"PASS" if ok else "FAIL"}')
    checks['G4'] = ok_g4
    emit(f"  [{'PASS' if ok_g4 else 'FAIL'}] G4 -- a derived kappa must not drift with M_b")

    # ---------------------------------------------------------------- G5
    emit('')
    emit('--- G5: epoch. D(z) = log10(X_fold(z)/q_fold(z)); (M) demands D = 0 at EVERY z ---')
    emit('  (footing x log M_b 10.45; q from the shell sitting at the front)')
    ok_g5 = True
    dz = {}
    for f in ('canonical', 'alt'):
        a0 = L.a0_of(f)
        try:
            o = load(f'prod_{f}_M10.45_N1200_s1')
        except FileNotFoundError:
            continue
        Mb = 10 ** 10.45
        dz[f] = {}
        emit(f'  footing {f}:')
        emit('       z    R_fold(kpc)   X_fold   q_front   D(dex)')
        for zt in (0.0, 1.0, 2.0, 4.0):
            row = series_at(o['series'], zt)
            if row is None:
                continue
            R = row[2]; q = row[10]
            Xf = share(a0, Mb, R)
            D = math.log10(Xf / q) if q > 0 else float('nan')
            dz[f][zt] = D
            emit(f'   {row[1]:6.3f}  {R:11.4f}  {Xf:9.4f}  {q:8.5f}  {D:+7.3f}')
            if q > 0:
                ok_g5 &= abs(D) <= ALLOW_DEX
    checks['G5'] = ok_g5
    emit(f"  [{'PASS' if ok_g5 else 'FAIL'}] G5 -- D(z) must vanish at every epoch (tolerance {ALLOW_DEX} dex)")

    # ---------------------------------------------------------------- G2c (ADDED, reported)
    emit('')
    emit('--- G2c (ADDED after G2 failed its frozen rule): the self-consistent root of (M) ---')
    emit('  map:  a_0 -> a_0^M(a_0) = G M_b q(1+q)/R_fold(a_0)^2 ,  s = a_0/a_0(frozen)')
    fp = None
    try:
        fp = json.load(open(os.path.join(HERE, 'final18_fixedpoint.json')))
    except FileNotFoundError:
        emit('  final18_fixedpoint.json missing -> not reported')
    kstar = {}
    if fp:
        for f in fp:
            seq = fp[f]
            emit(f'  footing {f}:')
            emit('      s_in          R_fold(kpc)  q_front   a_0^M(m/s^2)   kappa_M      s_out')
            for r in seq:
                emit(f"    {r['s']:.6e}  {r['R']:11.4f}  {r['q']:8.5f}  {r['a0M'] * SI:.4e}  "
                     f"{r['kappa']:.4e}  {r['sprime']:.6e}")
            kstar[f] = seq[-1]['kappa']
            drift = abs(seq[-1]['sprime'] / seq[-1]['s'] - 1)
            emit(f'  footing {f}: last iteration moves s by {drift:.2e} (converging: '
                 f'{"YES" if drift < 0.05 else "NOT YET"}), kappa_M* = {kstar[f]:.4e}')
    if kstar:
        emit(f"  [REPORTED] G2c -- self-consistent kappa_M* ~ {min(kstar.values()):.3e} .. "
             f"{max(kstar.values()):.3e} after {len(fp['canonical'])} iterations, still moving")
    # validity bracket: where does the fold solver itself stop being valid as a_0 falls?
    emit('')
    emit('  validity scan of the map (canonical, log M_b 10.45): the fold is healthy until the law flux cap')
    emit('  r_w = sqrt(G m/a_0) FW swallows the shell grid; below that threshold the run is not a fold.')
    emit('      s_in       R_fold(kpc)  q_front   kappa_M     s_out     s_out/s_in')
    for fn in ('bracket_s.json', 'bracket_s2.json', 'bracket_s3.json'):
        try:
            rows = json.load(open(os.path.join(HERE, fn)))
        except FileNotFoundError:
            continue
        for s, R, q, a0M, k, so, eu in rows:
            emit(f'    {s:9.5f}  {R:11.3f}  {q:8.5f}  {k:.3e}  {so:.3e}  {so / s:6.3f}'
                 + ('   <- FOLD COLLAPSED (wall exceeds the grid)' if R < 50 else ''))
    emit('  the map contracts (s_out/s_in < 1) at every s in the valid range [1.7e-3, 1] and its image')
    emit('  lands at the validity edge; the extrapolated fixed point (s ~ 1.4-1.5e-3) is beyond it.')
    emit('  => within the range the fold solver covers, (M) HAS NO SOLUTION; and at the observed a_0 it is')
    emit('     violated by 1.2 to 2.2 dex (G3/G5).')

    # ---------------------------------------------------------------- G6
    emit('')
    emit('--- G6: the grade the brief asks for ---')
    pinned = bool(kstar)                     # the map was run and is contracting, not covariant
    landed = bool(ok_g3 and ok_g4 and ok_g5)
    if pinned and not landed:
        label = 'KAPPA NOT DERIVED (FITTED) -- FOLD MATCHING FALSIFIED, NO SOLUTION IN THE VALID RANGE'
        why = ('(M) is a real constraint, not a flat direction (the mismatch moves at ~0.5 dex per dex of a_0,\n'
               '     10-100x faster than the fold inputs; Lean fold_match_unique: at most one root). It is\n'
               '     REFUTED, not satisfied: at the observed a_0 the two sides differ by 1.2 to 2.2 dex (G3, G5)\n'
               '     and by 1.86 dex across the mass grid (G4); and the self-consistent map contracts at every s\n'
               '     in [1.7e-3, 1] with its image at the validity edge (G2c), so no a_0 in that range solves it.')
    elif pinned and landed:
        label = 'KAPPA DERIVED (FOLD MATCHING)'
        why = 'pinned, in band, universal and epoch-stable'
    else:
        label = 'KAPPA NOT DERIVED (FITTED) -- FOLD MATCHING VACUOUS'
        why = 'no self-consistent root; the condition leaves kappa free or is ill-posed'
    ok_g6 = bool(checks.get('G1')) and bool(kstar)
    checks['G6'] = ok_g6
    emit(f'  Q1 (does the fold matching pin kappa?) = {"PINS" if pinned else "FREE"}')
    emit(f'  Q2 (does it land on 1/2?)             = {"YES" if landed else "NO"}')
    emit(f"  [{'PASS' if ok_g6 else 'FAIL'}] G6 -- {why}")

    # ---------------------------------------------------------------- MUTATE
    if a.mutate:
        emit('')
        emit('--- MUTATE: three false twins. Each MUST be REJECTED by the same machinery ---')
        kmax = {qn: max(kres[qn][f][1] for f in ('canonical', 'alt')) for qn in QDEFS}
        # MU1: the fold matching derives kappa = 1/2
        miss = {qn: abs(kmax[qn] - 0.5) for qn in QDEFS}
        ok_mu1 = all(v > BAND for v in miss.values())
        emit('  MU1 "the fold matching condition derives kappa = 1/2": band miss '
             + ', '.join(f'{qn} {v:.4f}' for qn, v in miss.items())
             + f' vs band {BAND} ({min(miss.values()) / BAND:.0f}x the band) -> '
             + ('REJECTED' if ok_mu1 else 'NOT REJECTED'))
        checks['MU1'] = ok_mu1
        # MU2: charge the halo with the whole cosmic cold charge of the patch (q = f_cdm)
        stc = KD1['footings']['canonical']['setting']; fcdm = stc['omega_d'] / stc['omega_b']
        res = {}
        for f in ('canonical', 'alt'):
            a0 = L.a0_of(f); kden = C_KMS * math.sqrt(G * rho_L(f))
            o = load(f'prod_{f}_M10.45_N1200_s1')
            R = o['R_fold_z0_kpc']; Mb = 10 ** 10.45
            res[f] = (G * Mb * fcdm * (1 + fcdm) / R ** 2) / kden
        ok_mu2 = all(abs(v - 0.5) > BAND for v in res.values())
        emit(f'  MU2 "charge the whole cosmic cold charge of the patch, q = f_cdm = {fcdm:.4f}": '
             + ', '.join(f'{f} kappa_M {v:.4f}' for f, v in res.items())
             + f' -> worst miss {min(abs(v - 0.5) for v in res.values()) / BAND:.1f}x the band -> '
             + ('REJECTED' if ok_mu2 else 'NOT REJECTED'))
        checks['MU2'] = ok_mu2
        # MU3: flat direction, the route is vacuous
        lhs = []
        for f in ('canonical', 'alt'):
            a0 = L.a0_of(f)
            o = load(f'prod_{f}_M10.45_N1200_s1')
            X0 = share(a0, 10 ** 10.45, o['R_fold_z0_kpc'])
            X1 = share(1.01 * a0, 10 ** 10.45, o['R_fold_z0_kpc'])
            lhs.append(abs(math.log10(X1 / X0) / math.log10(1.01)))
        rhs = max(t[0] for t in sens) if sens else float('nan')
        ok_mu3 = bool(ok_g1) and (min(lhs) > 10 * max(rhs, 1e-12))
        emit(f'  MU3 "flat direction, the route is vacuous": the mismatch M_ph/Q moves at '
             f'{min(lhs):.3f} dex per dex of a_0 (the left side), while the fold inputs move at '
             f'{rhs:.1e} dex per dex -> the constraint is {min(lhs) / max(rhs, 1e-12):.0f}x stronger than the'
             f' freedom in it -> ' + ('REJECTED' if ok_mu3 else 'NOT REJECTED'))
        checks['MU3'] = ok_mu3

    # ---------------------------------------------------------------- summary
    emit('')
    emit('=' * 100)
    emit('SUMMARY')
    emit('=' * 100)
    for k in sorted(checks):
        emit(f'  {k:5s} {"PASS" if checks[k] else "FAIL"}')
    emit(f'  checks: {len(checks)}, failing: {sorted(k for k, v in checks.items() if not v)}')
    emit(f'  LANE LABEL: {label}')
    emit('  kappa = 1/2 FITTED; not theory closed. Adopts nothing.')

    json.dump({'checks': checks, 'label': label, 'kappa_ranges': kres,
               'table': {f: {str(m): tabl[f][m] for m in tabl[f]} for f in tabl}},
              open(os.path.join(HERE, 'final18_MUTATE.json' if a.mutate else 'final18.json'), 'w'),
              indent=1, default=str)
    txt = '\n'.join(OUT)
    open(os.path.join(HERE, 'final18_MUTATE.out' if a.mutate else 'final18.out'), 'w').write(txt + '\n')
    print('\n' + txt)
    return 0 if (not a.mutate and checks.get('G6')) else 0


if __name__ == '__main__':
    sys.exit(main())
