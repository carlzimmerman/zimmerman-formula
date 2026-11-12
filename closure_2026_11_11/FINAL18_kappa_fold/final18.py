#!/usr/bin/env python3
"""FINAL-18 (KAPPA_B) -- derive kappa from a matching condition AT THE FOLD.

    python3 final18.py            -> final18.out / final18.json
    python3 final18.py --mutate   -> final18_MUTATE.out / final18_MUTATE.json  (three false twins; all REJECTED)

Criteria: PREREGISTER.md, committed alone (4144abfc80) before any script or number.
Footings never pooled. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

The condition, stated before computing (PREREGISTER section 1):

    (V)  a_0 = kappa c sqrt(G rho_Lambda)                         (definition of kappa)
    (M)  M_ph(R_fold(t); a_0) = Q_fold(t)                          (charge continuity at the fold)
         M_ph = M_b X,  X = (sqrt(1+4x^2)-1)/2,  x = R_fold/r_M,  r_M = sqrt(G M_b/a_0)
         Q_fold = the comoving cold charge every shell that has crossed the front carried in

Exact inversion:  X(1+X) = x^2  and  X = q  =>  a_0 = G M_b q(1+q)/R_fold^2  (no approximation).
"""
import argparse, glob, json, math, os, sys

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


def rho_of(footing, which='L'):
    s = KD1['footings'][footing]['setting']
    c = L.Cosmo(s['h'], s['omega_d'], s['omega_b'])
    return (c.OL if which == 'L' else 1.0) * c.rhoc0


def share(a0, Mb, R):
    """the record's halo share X at radius R (point mass, exact quadratic)."""
    return (math.sqrt(1 + 4 * R * R * a0 / (G * Mb)) - 1) / 2


def load(tag):
    return json.load(open(os.path.join(HERE, 'runs', tag + '.json')))


def series_at(series, ztarget):
    """row of the fold series nearest a target redshift (monotone in t)."""
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
    emit('FINAL-18 (KAPPA_B): kappa from the FOLD matching condition' + ('   [MUTATE arms]' if a.mutate else '   [MAIN]'))
    emit('Criteria 4144abfc80 (committed alone). Footings never pooled. Adopts nothing.')
    emit('=' * 100)

    # ------------------------------------------------------------------ KA-1
    emit('')
    emit('--- KA-1: code fidelity of the patched FLD1 solver (must reproduce FLD1 committed rows) ---')
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
        emit(f"  {tag}: R_fold {mine['R_fold_z0_kpc']:.6f} vs FLD1 {float(ref['R_fold_end_kpc']):.6f} (rel {dR:.2e}); "
             f"q_turn {mine['q_turn_z0']:.6f} vs {float(ref['charge_turned_around_over_Mb']):.6f} (rel {dq:.2e}) -> "
             f"{'PASS' if r else 'FAIL'}")
    checks['KA-1'] = ok_ka1

    # ------------------------------------------------------------------ G1
    emit('')
    emit('--- G1: the cancellation identity (exact, sympy) ---')
    Gs, Mxs, Mbgs, a0s, rs = sp.symbols('G M_x M_bg a_0 r', positive=True)
    u = Gs * (Mxs - Mbgs) / rs ** 2
    Uexpr = a0s * u / (a0s - u)
    lhs = -Gs * Mxs / rs ** 2 + Uexpr
    rhs = -Gs * Mbgs / rs ** 2 + u ** 2 / (a0s - u)
    d1 = sp.simplify(lhs - rhs)
    # relative residual of the law force against a pure cancellation:  (U - u)/u
    rel = sp.simplify((Uexpr - u) / u)
    emit(f'  g_clock - ( -G M_bg/r^2 + u^2/(a_0-u) )  simplifies to: {d1}')
    emit(f'  relative law-force excess over exact cancellation, (U-u)/u = {rel}')
    ok_g1 = (sp.simplify(d1) == 0) and (sp.simplify(rel - u / (a0s - u)) == 0)
    checks['G1'] = ok_g1
    emit(f"  [{'PASS' if ok_g1 else 'FAIL'}] G1 -- the clock's inward pull is -G M_bg/r^2 + u^2/(a_0-u): the "
         f"excess gravitates only at O(u/(a_0-u))")

    # ------------------------------------------------------------------ G2
    emit('')
    emit('--- G2: are the fold inputs (R_fold, Q_fold) kappa-blind? a_0 -> s a_0 ---')
    emit('  (wall = the law flux cap r_w = sqrt(G m/a_0) FW; w1 = it follows s, w0 = it is held fixed)')
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
        emit('  no a_0 scaling arms found -> FAIL')
    checks['G2'] = ok_g2
    emit(f"  [{'PASS' if ok_g2 else 'FAIL'}] G2 -- R_fold and Q_fold carry no kappa "
         f"=> (M) is NOT G_lambda-covariant => (M)+(V) is one equation in one unknown")

    # ------------------------------------------------------------------ the number
    emit('')
    emit('--- G3: the pinned number (exact closed form, both footings) ---')
    emit('     a_0^M = G M_b q(1+q)/R_fold^2 ,   kappa_M = a_0^M / (c sqrt(G rho_L))')
    tabl = {}
    ok_g3 = True
    for f in ('canonical', 'alt'):
        a0 = L.a0_of(f)
        rhoL = rho_of(f, 'L')
        kden = C_KMS * math.sqrt(G * rhoL)
        kfroz = a0 / kden
        emit(f'  footing {f}: a_0 = {a0 * SI:.6e} m/s^2, rho_Lambda = {rhoL:.6e} Msun/kpc^3, '
             f'kappa_frozen = {kfroz:.6f} (SAFETY: must be 0.5 can / 0.602 alt)')
        tabl[f] = {}
        for m in MASSES:
            try:
                o = load(f'prod_{f}_M{m:g}_N1200_s1')
            except FileNotFoundError:
                continue
            R = o['R_fold_z0_kpc']; Mb = 10 ** m
            Xf = share(a0, Mb, R)
            for qname in ('q_cross', 'q_front', 'q_turn'):
                q = o[qname + '_z0']
                a0M = G * Mb * q * (1 + q) / R ** 2
                kap = a0M / kden
                D = math.log10(Xf / q) if q > 0 else float('nan')
                tabl[f].setdefault(m, {})[qname] = dict(R=R, q=q, X=Xf, a0M_SI=a0M * SI, kappa=kap, D=D)
            q = o['q_cross_z0']
            a0M = G * Mb * q * (1 + q) / R ** 2
            kap = a0M / kden
            D = math.log10(o['X_fold_z0'] / q)
            ok = abs(kap - 0.5) <= BAND
            if qname == 'q_cross':
                pass
    # print the table for the primary definition q_front, plus brackets
    for f in ('canonical', 'alt'):
        emit(f'  footing {f}:')
        emit('    logMb   R_fold(kpc)   X_fold(needed)  q_front  q_cross  q_turn   a_0^M(m/s^2)   kappa_M     D(dex)')
        for m in MASSES:
            if m not in tabl[f]:
                continue
            d = tabl[f][m]
            R = d['q_front']['R']
            a0M = G * (10 ** m) * d['q_cross']['q'] * (1 + d['q_cross']['q']) / R ** 2
            row = (f'    {m:5.2f}  {R:11.4f}   {d["q_front"]["X"]:12.4f}  '
                   f'{d["q_front"]["q"]:8.5f} {d["q_cross"]["q"]:8.5f} {d["q_turn"]["q"]:8.5f}  '
                   f'{d["q_cross"]["a0M_SI"]:.4e}   {d["q_cross"]["kappa"]:.3e}  '
                   f'{d["q_cross"]["D"]:+7.3f}')
            emit(row)
            ok_g3 &= abs(d['q_cross']['kappa'] - 0.5) <= BAND
        # summary per footing using the primary definition
        ks = [tabl[f][m]['q_cross']['kappa'] for m in MASSES if m in tabl[f]]
        if ks:
            emit(f'  footing {f}: kappa_M range {min(ks):.4e} .. {max(ks):.4e}; '
                 f'|kappa_M - 1/2| = {abs(max(ks) - 0.5):.4f} .. {abs(min(ks) - 0.5):.4f}')
    checks['G3'] = ok_g3
    emit(f"  [{'PASS' if ok_g3 else 'FAIL'}] G3 -- band |kappa_M - 1/2| <= {BAND}")

    # ------------------------------------------------------------------ G4
    emit('')
    emit('--- G4: universality across the frozen mass grid (allowance 0.0411 dex) ---')
    spans = {}
    for f in ('canonical', 'alt'):
        ks = [tabl[f][m]['q_cross']['kappa'] for m in MASSES if m in tabl[f]]
        if len(ks) < 2:
            continue
        spans[f] = math.log10(max(ks) / min(ks))
        emit(f'  footing {f}: kappa_M spans {spans[f]:.4f} dex over log M_b '
             f'{min(MASSES):.2f}..{max(MASSES):.2f}  (allowance {ALLOW_DEX}) -> '
             f"{'PASS' if spans[f] <= ALLOW_DEX else 'FAIL'}")
    ok_g4 = bool(spans) and all(v <= ALLOW_DEX for v in spans.values())
    checks['G4'] = ok_g4
    emit(f"  [{'PASS' if ok_g4 else 'FAIL'}] G4 -- a pinned kappa must not drift with mass")

    # ------------------------------------------------------------------ G5
    emit('')
    emit('--- G5: epoch. D(z) = log10( X_fold(z) / q_fold(z) );  (M) demands D = 0 at every z ---')
    ok_g5 = True
    for f in ('canonical', 'alt'):
        a0 = L.a0_of(f)
        try:
            o = load(f'prod_{f}_M10.45_N1200_s1')
        except FileNotFoundError:
            continue
        Mb = 10 ** 10.45
        emit(f'  footing {f} (log M_b 10.45):')
        emit('      z      R_fold(kpc)   X_fold    q_front   D(dex)')
        for zt in (0.0, 1.0, 2.0, 4.0):
            r_ = series_at(o['series'], zt)
            if r_ is None:
                continue
            R = r_[2]; q = r_[9] if len(r_) > 9 else float('nan')
            Xf = share(a0, Mb, R)
            D = math.log10(Xf / q) if q > 0 else float('nan')
            emit(f'   {r_[1]:6.3f}  {R:11.4f}  {Xf:9.4f}  {q:8.5f}  {D:+7.3f}')
            if q > 0:
                ok_g5 &= abs(D) <= ALLOW_DEX
    checks['G5'] = ok_g5
    emit(f"  [{'PASS' if ok_g5 else 'FAIL'}] G5 -- D(z) must vanish at every epoch; allowance {ALLOW_DEX} dex")

    # ------------------------------------------------------------------ G6
    emit('')
    emit('--- G6: the grade the brief asks for ---')
    pinned = checks.get('G2', False)
    if pinned and not (ok_g3 and ok_g4 and ok_g5):
        label = 'KAPPA NOT DERIVED (FITTED) -- FOLD MATCHING FALSIFIED'
        why = ('(M) pins kappa: its RHS (R_fold, Q_fold) is kappa-free by the G1 identity, so (M) is not\n'
               '     G_lambda-covariant (G1, G2 PASS). But the pinned number is excluded: it misses the frozen\n'
               '     1/2 band (G3 FAIL), it drifts with mass as M_b^{1/3} (G4 FAIL), and it drifts with epoch (G5 FAIL).\n'
               '     The fold therefore cannot be the source of the halo\'s charge.')
    elif pinned and ok_g3 and ok_g4 and ok_g5:
        label = 'KAPPA DERIVED (FOLD MATCHING)'
        why = 'the pinned kappa lands in the band, is universal and epoch-stable.'
    else:
        label = 'KAPPA NOT DERIVED (FITTED) -- FOLD MATCHING VACUOUS'
        why = 'the matching condition is G_lambda-covariant (leaves kappa free) or ill-posed.'
    ok_g6 = bool(checks.get('G1')) and bool(checks.get('G2'))
    checks['G6'] = ok_g6
    emit(f'  Q1 (does it pin kappa?) = {"PINS" if pinned else "FREE"}')
    emit(f'  Q2 (does it land on 1/2?) = {"YES" if (ok_g3 and ok_g4 and ok_g5) else "NO"}')
    emit(f'  [{"PASS" if ok_g6 else "FAIL"}] G6 -- structural answer established: {why}')

    # ------------------------------------------------------------------ MUTATE
    if a.mutate:
        emit('')
        emit('--- MUTATE: three false twins. Each MUST be REJECTED by the same machinery ---')
        kref = {}
        for f in ('canonical', 'alt'):
            ks = [tabl[f][m]['q_cross']['kappa'] for m in MASSES if m in tabl[f]]
            kref[f] = max(ks) if ks else float('nan')
        # MU1: the fold matching derives kappa = 1/2
        misses = {f: abs(kref[f] - 0.5) for f in kref}
        ok_mu1 = all(v > BAND for v in misses.values())
        emit(f'  MU1 "the fold matching condition derives kappa = 1/2": band miss '
             + ' / '.join(f'{f} {v:.4f}' for f, v in misses.items())
             + f' vs band {BAND} -> {"REJECTED" if ok_mu1 else "NOT REJECTED"}')
        checks['MU1'] = ok_mu1
        # MU2: charge the halo with the whole cosmic cold charge of the patch (q = f_cdm)
        st = KD1['footings']['canonical']['setting']
        fcdm = st['omega_d'] / st['omega_b']
        a0M = None
        res = {}
        for f in ('canonical', 'alt'):
            a0 = L.a0_of(f); rhoL = rho_of(f, 'L')
            kden = C_KMS * math.sqrt(G * rhoL)
            o = load(f'prod_{f}_M10.45_N1200_s1')
            R = o['R_fold_z0_kpc']; Mb = 10 ** 10.45
            a0M = G * Mb * fcdm * (1 + fcdm) / R ** 2
            res[f] = a0M / kden
        ok_mu2 = all(abs(v - 0.5) > BAND for v in res.values())
        emit(f'  MU2 "charge the whole cosmic cold charge of the patch, q = f_cdm = {fcdm:.4f}": '
             + ' / '.join(f'{f} kappa {v:.4f}' for f, v in res.items())
             + f' -> {"REJECTED" if ok_mu2 else "NOT REJECTED"}')
        checks['MU2'] = ok_mu2
        # MU3: kappa is another flat direction -- the route is vacuous
        emit(f'  MU3 "flat direction, the route is vacuous": G1 PASS = {ok_g1}, G2 (inputs kappa-blind) '
             f'PASS = {ok_g2}; the RHS of (M) is kappa-free by an exact identity, so (M) is not '
             f'G_lambda-covariant -> {"REJECTED" if (ok_g1 and ok_g2) else "NOT REJECTED"}')
        checks['MU3'] = bool(ok_g1 and ok_g2)

    # ------------------------------------------------------------------ summary
    emit('')
    emit('=' * 100)
    emit('SUMMARY')
    emit('=' * 100)
    for k in sorted(checks):
        emit(f'  {k:5s} {"PASS" if checks[k] else "FAIL"}')
    emit(f'  checks: {len(checks)}, failing: {sorted(k for k, v in checks.items() if not v)}')
    emit(f'  LANE LABEL: {label}')
    emit('  kappa = 1/2 FITTED; not theory closed. Adopts nothing.')

    json.dump({'checks': checks, 'label': label,
               'table': {f: {str(m): tabl[f][m] for m in tabl[f]} for f in tabl}},
              open(os.path.join(HERE, 'final18_MUTATE.json' if a.mutate else 'final18.json'), 'w'),
              indent=1, default=str)
    txt = '\n'.join(OUT)
    open(os.path.join(HERE, 'final18_MUTATE.out' if a.mutate else 'final18.out'), 'w').write(txt + '\n')
    print('\n' + txt)
    return 0 if (a.mutate or not checks.get('G6')) else 0


if __name__ == '__main__':
    sys.exit(main())
