#!/usr/bin/env python3
"""VSJ1 grader: gates G1-G7, known answers and labels from runs/*.json, vsj1_g2.json and vsj1_cosmo_tune.json.

    python3 vsj1_grade.py            -> vsj1_grade.json / .out
    python3 vsj1_grade.py mutate     -> vsj1_MUTATE.json / .out   (M1 heat removed, M2 hot charge zero, M3 law off)

Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'fable52_push', 'COL1_clock_collapse'))
import col1_lib as L                                                                    # noqa: E402
RUNS = os.path.join(HERE, 'runs')
AKS = json.load(open(os.path.join(REPO, 'toe_2026_11_10', 'AKS1_acceleration_keyed_sink', 'aks1_t.json')))['T7']
PD1 = json.load(open(os.path.join(REPO, 'closure_2026_11_09', 'PD1_phantom_is_dust', 'pd1_MUTATE.json')))
EDGES = np.load(os.path.join(REPO, 'real_research', 'data', 'lensing_rar', 'cfg110_perlens.npz'))['gbar_edges']
GSI, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19            # FLD1's constants for the KiDS edges
MASSES = (9.0, 10.5, 11.5); FOOT = ('canonical', 'alt'); GAM = 5.0 / 3.0
RSHARE = {'canonical': 5.409583, 'alt': 5.412268}
NSEED = {9.0: 600, 10.5: 600, 11.5: 300}
LINE = 0.10
MUT = sys.argv[1] == 'mutate' if len(sys.argv) > 1 else False


def load(name):
    p = os.path.join(RUNS, name + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def XL(x):
    return (np.sqrt(1 + 4 * np.asarray(x, float) ** 2) - 1) / 2


def law(gN, a0, off=False):
    """mu(g/a0) g = gN with mu = x/(1+x): g = [gN + sqrt(gN^2 + 4 gN a0)]/2."""
    return gN if off else 0.5 * (gN + np.sqrt(gN * gN + 4 * gN * a0))


def h2_share(footing, lM):
    tab = PD1[footing]['S_AM']['table']
    lm = np.array([r['logMb'] for r in tab]); sh = np.array([r['share_over_Mb'] for r in tab])
    return float(10 ** np.interp(lM, lm, np.log10(sh)))


def kids_edge(Mb, i):
    return math.sqrt(GSI * Mb * MSUN / EDGES[i]) / KPC


def standing_a1(r, v, MX, Mb):
    """AMENDMENT A1: a zone stands iff |v_zone| <= 0.10 v_ref there; R_st is the largest zone radius inside which at
    least 95 % of the charge sits in standing zones. Returns (zone index, R_st); (-1, 0) if none."""
    r = np.asarray(r, float); v = np.asarray(v, float); MX = np.asarray(MX, float)
    rc = 0.5 * (r + np.concatenate([[0.0], r[:-1]])); vz = 0.5 * (v + np.concatenate([[0.0], v[:-1]]))
    dM = np.diff(np.concatenate([[0.0], MX]))
    st = np.abs(vz) <= 0.10 * np.sqrt(L.G * (Mb + MX) / rc)
    ok = np.where(np.cumsum(dM * st) / np.cumsum(dM) >= 0.95)[0]
    i = int(ok.max()) if ok.size else -1
    return i, (float(r[i]) if i >= 0 else 0.0)


class Profile:
    """Settled state of one run, optionally scaled to another baryon mass (S-cosmo: r -> lam r, M -> lam^3 M).
    rule 'A1' (graded) or 'frozen' (the criteria's cumulative statistic, reported)."""

    def __init__(self, d, lM=None, rule='A1'):
        lam = 1.0 if lM is None else 10 ** ((lM - d['logMb']) / 3.0)
        self.d = d; self.lam = lam
        self.r = np.array(d['r']) * lam; self.v = np.array(d['v']) * lam; self.e = np.array(d['e']) * lam ** 2
        self.MX = np.array(d['MX']) * lam ** 3; self.Mb = d['Mb'] * lam ** 3
        self.dM = np.diff(np.concatenate([[0.0], self.MX]))
        self.rl = np.concatenate([[0.0], self.r[:-1]]); self.rc = 0.5 * (self.r + self.rl)
        if rule == 'A1':
            self.ist, rst = standing_a1(d['r'], d['v'], d['MX'], d['Mb']); self.R_st = rst * lam
        else:
            self.R_st = d['R_st'] * lam; self.ist = d['i_st']
        self.Q_st = float(self.MX[self.ist]) if self.ist >= 0 else 0.0

    def Q(self, r):
        """Clock charge inside r (uniform density inside the first node)."""
        r = np.asarray(r, float)
        q = np.exp(np.interp(np.log(np.maximum(r, 1e-300)), np.log(self.r), np.log(self.MX)))
        return np.where(r < self.r[0], self.MX[0] * (r / self.r[0]) ** 3, q)

    def sigma2(self, rmax):
        ins = self.rc <= rmax
        if not ins.any():
            return None, None
        vref2 = L.G * (self.Mb + self.MX) / self.rc
        return (float(np.sum(self.dM[ins] * (GAM - 1) * self.e[ins]) / np.sum(self.dM[ins])),
                float(np.sum(self.dM[ins] * vref2[ins]) / (3 * np.sum(self.dM[ins]))))


def g3(pr, a0, hot_zero=False, law_off=False, centre=False):
    rM = math.sqrt(L.G * pr.Mb / a0); x = np.logspace(0, 1, 21); r = x * rM
    Q = np.zeros_like(r) if hot_zero else (np.full_like(r, pr.Q_st) if centre else pr.Q(r))
    gb = L.G * pr.Mb / r ** 2; gN = L.G * (pr.Mb + Q) / r ** 2
    inside = r <= pr.R_st
    g = np.where(inside, law(gN, a0, law_off), gN)
    X = g / gb - 1
    dev = np.log10(np.maximum(X, 1e-300) / XL(x))
    k = int(np.argmax(np.abs(dev)))
    return {'max_abs_dev_dex': float(np.abs(dev).max()), 'dev_at_x1': float(dev[0]), 'dev_at_x10': float(dev[-1]),
            'worst_x': float(x[k]), 'worst_dev': float(dev[k]), 'X_tot_x10': float(X[-1]), 'X_L_x10': float(XL(10.0)),
            'Mhot_in_rM_over_Mb': float(Q[0] / pr.Mb), 'Mhot_in_10rM_over_Mb': float(Q[-1] / pr.Mb),
            'points_inside_R_st': int(inside.sum()), 'X_newton_x10': float(Q[-1] / pr.Mb),
            'pass': bool(np.abs(dev).max() <= LINE)}


def g4(pr, a0, law_off=False):
    R = pr.R_st
    if R <= 0:
        return {'pass': False, 'R_st': 0.0}
    rM = math.sqrt(L.G * pr.Mb / a0)
    Mreal = pr.Mb + pr.Q_st
    gN = L.G * Mreal / R ** 2; gin = law(gN, a0, law_off); J = gin / gN
    gL = law(L.G * pr.Mb / R ** 2, a0)
    mid = kids_edge(pr.Mb, 4)
    fail = math.log10(J) > LINE
    return {'R_st': R, 'R_st_over_rM': R / rM, 'R_st_over_R_ta': R / (pr.d['R_ta'] * pr.lam) if pr.d['R_ta'] > 0 else None, 'J': J, 'log10J': math.log10(J), 'layer_over_Mb': -(J - 1) * Mreal / pr.Mb,
            'real_charge_over_Mb': pr.Q_st / pr.Mb, 'law_halo_baryons_over_Mb': float(XL(R / rM)),
            'real_over_law_halo': pr.Q_st / pr.Mb / float(XL(R / rM)),
            'g_out_over_gL_baryons': gN / gL, 'kids_middle_edge': mid,
            'HE1_reason_applies': bool(fail and R < mid and gN < gL), 'pass': bool(not fail)}


def g5(pr, footing, lM):
    row = [x for x in AKS[footing]['rows'] if abs(x['logMb'] - lM) < 1e-9][0]
    inn, mid = kids_edge(pr.Mb, 7), kids_edge(pr.Mb, 4)
    return {'R_st': pr.R_st, 'R_cap': row['R_cap'], 'kids_inner_edge': inn, 'kids_middle_edge': mid,
            'cap_over_R_st': row['R_cap'] / pr.R_st if pr.R_st > 0 else None,
            'inner_over_R_st': inn / pr.R_st if pr.R_st > 0 else None, 'middle_over_R_st': mid / pr.R_st if pr.R_st > 0 else None,
            'pass': bool(pr.R_st >= row['R_cap'] and pr.R_st >= inn and pr.R_st >= mid)}


def g6(pr, a0, re_star=None):
    o = {}
    for key, rmax in (('inside_re_star', re_star), ('inside_R_st', pr.R_st)):
        if rmax is None or rmax <= 0:
            continue
        s2, sv2 = pr.sigma2(rmax)
        if s2 is None or s2 <= 0:
            continue
        o[key] = {'sigma_kms': math.sqrt(s2), 'dex_sigma4_over_law': math.log10(s2 ** 2 / (L.G * pr.Mb * a0 / 4)),
                  'sigma2_over_virial': s2 / sv2}
    return o


def fmt(x, f='.3g'):
    return 'n/a' if x is None else format(x, f)


def main():
    out = []; RES = {'mutate': MUT}
    P = out.append
    # ---------------- known answers
    ka1 = load('ka1_noh'); ka2 = load('ka2_rta'); ka4 = load('ka4_EdS_N300')
    g2 = json.load(open(os.path.join(HERE, 'vsj1_g2.json')))
    lo, hi = load('seed_canonical_10.5_N300'), load('seed_canonical_10.5_N600')
    KA = {}
    KA['KA1'] = bool(ka1 and ka1['pass'])
    P(f"KA1 Noh: shock {ka1['r_shock']:.4f} (0.2000), post-shock density {ka1['rho_post']:.1f} (64), energy {ka1['E_rel']:.1e} -> {'PASS' if KA['KA1'] else 'FAIL'}")
    KA['KA2'] = bool(ka2 and ka2['pass'])
    P(f"KA2 fluid terms off, R_ta: {ka2['a']['R_ta']:.1f} (FLD1 88) and {ka2['b']['R_ta']:.1f} (FLD1 600) -> {'PASS' if KA['KA2'] else 'FAIL'}")
    KA['KA3'] = bool(g2['KA3_pass'])
    P(f"KA3 SIS identities and the law's closed form (sympy): residual {g2['KA3']['residual']} -> {'PASS' if KA['KA3'] else 'FAIL'}")
    if ka4:
        ok4 = (ka4['status'] == 'done' and abs(ka4['shock_over_Rta'] / 0.339 - 1) <= 0.15 and abs(ka4['rho_slope'] + 2.25) <= 0.25)
        P(f"KA4 EdS self-similar: {ka4['status']}; shock/R_ta {ka4['shock_over_Rta']:.3f} (0.339), density slope {ka4['rho_slope']:.2f} (-2.25, {ka4['n_slope_zones']} zones), "
          f"M_ta/seed {ka4['M_ta_over_seed']:.0f} -> {'PASS' if ok4 else 'FAIL'}")
    else:
        ok4 = False; P('KA4: run missing -> FAIL')
    KA['KA4'] = bool(ok4)
    if lo and hi:
        a0c = L.a0_of('canonical'); pl, ph = Profile(lo), Profile(hi)
        ml, mh = g3(pl, a0c)['Mhot_in_10rM_over_Mb'], g3(ph, a0c)['Mhot_in_10rM_over_Mb']
        ok5 = (lo['settled_vsh1_rule'] == hi['settled_vsh1_rule'] and ph.R_st > 0 and abs(pl.R_st / ph.R_st - 1) <= 0.10
               and abs(ml / mh - 1) <= 0.20)
        P(f"KA5 resolution 10.5 canonical N 300 / 600: SETTLED {lo['settled_vsh1_rule']} / {hi['settled_vsh1_rule']}; R_st (A1) {pl.R_st:.1f} / {ph.R_st:.1f}; "
          f"M_hot(<10 r_M)/M_b {ml:.4f} / {mh:.4f} -> {'PASS' if ok5 else 'FAIL'}")
    else:
        ok5 = False; P('KA5: runs missing -> FAIL')
    KA['KA5'] = bool(ok5)
    if hi:
        k6 = g3(Profile(hi), L.a0_of('canonical'), hot_zero=True)
        KA['KA6'] = bool(k6['max_abs_dev_dex'] <= 1e-10)
        P(f"KA6 zero hot charge: max |log10(X_tot/X_L)| {k6['max_abs_dev_dex']:.1e} -> {'PASS' if KA['KA6'] else 'FAIL'}")
    else:
        KA['KA6'] = False
    RES['known_answers'] = KA; allka = all(KA.values())
    P(f"known answers: {'ALL PASS' if allka else 'FAIL'}")
    # ---------------- G2, G7
    RES['G2'] = {'pass': bool(g2['G2_pass']), 'residuals': {k: g2[k]['residual'] for k in ('G2a', 'G2b', 'G2c', 'G2c2', 'G2d', 'G2e')}}
    P(f"G2 what gravitates (sympy, six residuals 0): {'PASS' if RES['G2']['pass'] else 'FAIL'}: inside R_st the law's phantom of (baryons + hot charge), plus the hot charge")
    tune = json.load(open(os.path.join(HERE, 'vsj1_cosmo_tune.json'))) if os.path.exists(os.path.join(HERE, 'vsj1_cosmo_tune.json')) else {}
    RES['footings'] = {}
    law_off = MUT                                                    # M3 arm is computed beside the primary below
    for f in FOOT:
        a0 = L.a0_of(f); F = RES['footings'][f] = {}
        P(f'\n=== {f} (a0 {L.FOOT[f]:.4e} m/s^2) ===')
        nuF = AKS[f]['nu_F']; Kn = 3 * nuF / (1000.0 * 100.0)
        F['G7'] = {'nu_F': nuF, 'Kn': Kn, 'collisional': bool(Kn <= 0.1), 'fails_estimate': bool(Kn <= 0.1), 'passes_estimate': bool(Kn >= 10)}
        # ---- S-seed
        seed = {m: load(f'seed_{f}_{m:g}_N{NSEED[m]}') for m in MASSES}
        F['G1'] = {'runs': {}}
        for m in MASSES:
            d = seed[m]
            if d is None:
                P(f'G1 log M_b {m}: run missing'); continue
            F['G1']['runs'][str(m)] = {k: d[k] for k in ('status', 'z_stop', 'steps', 'N', 'R_sh', 'S', 'r_e_star', 'settled_vsh1_rule', 'z_pass',
                                                        'R_ta', 'visc_heat_frac', 'seconds')}
            P(f"G1 log M_b {m} (N {d['N']}): {d['status']} (z {d['z_stop']:.2f}); R_sh {d['R_sh']:.1f} vs r_e* {d['r_e_star']:.1f}; S {fmt(d['S'])} -> "
              f"{'SETTLED' if d['settled_vsh1_rule'] else 'not settled'}; shock past r_e* at z {fmt(d['z_pass'])}; R_ta {d['R_ta']:.1f}; "
              f"visc heat frac {fmt(d['visc_heat_frac'])}; steps {d['steps']}, {d['seconds']} s")
        d105 = seed[10.5]
        F['G1']['pass'] = bool(d105 is not None and d105['settled_vsh1_rule'])
        P(f"G1 (graded at 10.5): {'PASS' if F['G1']['pass'] else 'FAIL'}")
        sup = {}
        # supplies: name -> {mass: Profile}
        prof = {'S-seed': {m: Profile(seed[m]) for m in MASSES if seed[m] is not None and seed[m]['status'] == 'done'}}
        for br in ('H1', 'H2'):
            pm = {}
            for m in MASSES:
                t = tune.get(f, {}).get(br, {}).get(str(m))
                if t and load(t['run']):
                    pm[m] = Profile(load(t['run']), lM=m)
            prof[f'S-cosmo {br}'] = pm
        prof['S-seed, frozen R_st (reported)'] = {m: Profile(seed[m], rule='frozen') for m in MASSES
                                                  if seed[m] is not None and seed[m]['status'] == 'done'}
        for sname, pm in prof.items():
            S = sup[sname] = {'G3': {}, 'G4': {}, 'G5': {}, 'G6': {}, 'G3_centre': {}, 'G3_M2': {}, 'G3_M3': {}, 'G4_M3': {}, 'host': {}}
            P(f'--- {sname} ---')
            for m in MASSES:
                if m not in pm:
                    P(f'log M_b {m}: no run'); continue
                pr = pm[m]; key = str(m)
                if sname.startswith('S-cosmo'):
                    br = sname.split()[-1]; t = tune[f][br][key]
                    target = RSHARE[f] if br == 'H1' else h2_share(f, m)
                    ach = pr.Q_st / pr.Mb
                    fz = Profile(pr.d, lM=m, rule='frozen')
                    S['host'][key] = {'target_over_Mb': target, 'achieved_over_Mb': ach, 'A': t['A'], 'within_10pct': bool(abs(ach / target - 1) <= 0.10),
                                      'run': t['run'], 'status': pr.d['status'],
                                      'frozen_R_st': fz.R_st, 'frozen_host_over_Mb': fz.Q_st / fz.Mb}
                    P(f"log M_b {m}: host target {target:.2f} M_b, achieved {ach:.2f} (A {t['A']:.4g}; {pr.d['status']}) -> {'ok' if S['host'][key]['within_10pct'] else 'OUTSIDE 10 %'}; with the frozen R_st ({fz.R_st:.0f} kpc) the host reads {fz.Q_st / fz.Mb:.2f} M_b")
                S['G3'][key] = a = g3(pr, a0)
                S['G3_centre'][key] = c = g3(pr, a0, centre=True)
                S['G3_M2'][key] = g3(pr, a0, hot_zero=True)
                S['G3_M3'][key] = g3(pr, a0, law_off=True)
                S['G4'][key] = b = g4(pr, a0); S['G4_M3'][key] = g4(pr, a0, law_off=True)
                S['G5'][key] = c5 = g5(pr, f, m)
                S['G6'][key] = t6 = g6(pr, a0, pr.d.get('r_e_star'))
                P(f"log M_b {m}: G3 max |dex| {a['max_abs_dev_dex']:.3f} (at x {a['worst_x']:.2f}: {a['worst_dev']:+.3f}; x=1 {a['dev_at_x1']:+.3f}, x=10 {a['dev_at_x10']:+.3f}; "
                  f"X_tot(10) {a['X_tot_x10']:.2f} vs X_L {a['X_L_x10']:.2f}; M_hot(<r_M) {a['Mhot_in_rM_over_Mb']:.4f}, (<10 r_M) {a['Mhot_in_10rM_over_Mb']:.3f} M_b) -> "
                  f"{'PASS' if a['pass'] else 'FAIL'}; all charge at the centre: {c['max_abs_dev_dex']:.3f} {'PASS' if c['pass'] else 'FAIL'}; "
                  f"VSH1's-own-law reading X(10 r_M) {a['X_newton_x10']:.3f}")
                P(f"            G4 R_st {b['R_st']:.1f} kpc ({b['R_st_over_rM']:.1f} r_M, {fmt(b['R_st_over_R_ta'])} R_ta): jump J {b['J']:.2f} ({b['log10J']:.2f} dex), layer {b['layer_over_Mb']:.1f} M_b; real charge "
                  f"{b['real_charge_over_Mb']:.2f} M_b vs the baryons' law halo {b['law_halo_baryons_over_Mb']:.1f} M_b ({b['real_over_law_halo']:.3f}); g_out/g_L {b['g_out_over_gL_baryons']:.3f}; "
                  f"HE1's reason applies: {b['HE1_reason_applies']} -> {'PASS' if b['pass'] else 'FAIL'}")
                P(f"            G5 R_st {c5['R_st']:.0f} vs cap {c5['R_cap']:.0f} (x{fmt(c5['cap_over_R_st'])}), KiDS inner {c5['kids_inner_edge']:.0f} (x{fmt(c5['inner_over_R_st'])}), "
                  f"middle {c5['kids_middle_edge']:.0f} (x{fmt(c5['middle_over_R_st'])}) -> {'PASS' if c5['pass'] else 'FAIL'}")
                P('            G6 ' + '; '.join(f"{k}: sigma {v['sigma_kms']:.1f} km/s, sigma^4/law {v['dex_sigma4_over_law']:+.2f} dex, sigma^2/virial {v['sigma2_over_virial']:.2f}"
                                                 for k, v in t6.items()))
            done = all(str(m) in S['G3'] for m in MASSES)
            hostok = all(v['within_10pct'] and v['status'] == 'done' for v in S['host'].values()) if sname.startswith('S-cosmo') else True
            S['complete'] = bool(done and hostok)
            def tuned(m):
                return (not sname.startswith('S-cosmo')) or (S['host'][str(m)]['within_10pct'] and S['host'][str(m)]['status'] == 'done')
            for gk in ('G3', 'G4', 'G5'):
                S[gk + '_pass'] = bool(done and hostok and all(S[gk][str(m)]['pass'] for m in MASSES))
                # a gate is decided FAIL as soon as one tuned, evaluated mass fails; PASS needs all three
                S[gk + '_fail_decided'] = bool(any((not S[gk][str(m)]['pass']) and tuned(m) for m in MASSES if str(m) in S[gk]))
                S[gk + '_decided'] = bool(S[gk + '_pass'] or S[gk + '_fail_decided'])
            S['G3_M2_pass'] = bool(done and all(S['G3_M2'][str(m)]['pass'] for m in MASSES))
            S['G3_M3_pass'] = bool(done and all(S['G3_M3'][str(m)]['pass'] for m in MASSES))
            S['G4_M3_pass'] = bool(done and all(S['G4_M3'][str(m)]['pass'] for m in MASSES))
            if done:
                key = 'inside_R_st'
                ls = [math.log(10 ** S['G6'][str(m)][key]['dex_sigma4_over_law'] * (L.G * 10 ** m * a0 / 4)) for m in MASSES if key in S['G6'][str(m)]]
                if len(ls) == 3:
                    S['G6_slope_lnsigma4_lnMb'] = float(np.polyfit(np.log([10 ** m for m in MASSES]), ls, 1)[0])
                    S['G6_tied_to_law'] = bool(all(abs(S['G6'][str(m)][key]['dex_sigma4_over_law']) <= 0.10 for m in MASSES)
                                               and abs(S['G6_slope_lnsigma4_lnMb'] - 1) <= 0.1)
                    P(f"G6 (reported): d ln sigma^4/d ln M_b {S['G6_slope_lnsigma4_lnMb']:.2f} (law 1, virial 4/3); tied to the law: {S['G6_tied_to_law']}")
            word = lambda gk: 'PASS' if S[gk + '_pass'] else ('FAIL' if S[gk + '_fail_decided'] else 'NOT DECIDED')
            P(f"{sname}: all three masses tuned and run: {S['complete']}; G3 {word('G3')}, G4 {word('G4')}, G5 {word('G5')}")
        F['supplies'] = sup
        # reported floor: S-cosmo with no primordial perturbation at all (A = 0; canonical cosmology run only)
        d0 = load(f'cosmo_{f}_A0_N300')
        if d0 is not None and d0['status'] == 'done':
            F['S-cosmo_A0_floor'] = {}
            for m in MASSES:
                p0 = Profile(d0, lM=m); pf = Profile(d0, lM=m, rule='frozen'); a = g3(p0, a0)
                F['S-cosmo_A0_floor'][str(m)] = {'host_A1': p0.Q_st / p0.Mb, 'host_frozen_R_st': pf.Q_st / pf.Mb, 'G3_max_abs_dev_dex': a['max_abs_dev_dex'],
                                                 'Mhot_in_10rM_over_Mb': a['Mhot_in_10rM_over_Mb'], 'pass': a['pass']}
            v = F['S-cosmo_A0_floor']
            P(f"S-cosmo floor (reported; A = 0, baryon seed only): host {v['9.0']['host_A1']:.2f} M_b (frozen R_st: {v['9.0']['host_frozen_R_st']:.2f}); G3 max |dex| "
              + ' / '.join(f"{v[str(m)]['G3_max_abs_dev_dex']:.3f}" for m in MASSES) + f" -> {'PASS' if all(v[str(m)]['pass'] for m in MASSES) else 'FAIL'}")
        # S-cosmo passes a gate iff either bracket passes it; a supply survives iff G3, G4, G5 pass under one set of constants
        seedS = sup['S-seed']; h1, h2 = sup['S-cosmo H1'], sup['S-cosmo H2']
        g3_seed = seedS['G3_pass']; g3_cos = h1['G3_pass'] or h2['G3_pass']
        graded = {n: sup[n] for n in ('S-seed', 'S-cosmo H1', 'S-cosmo H2')}
        surv = {n: bool(s['complete'] and s['G3_pass'] and s['G4_pass'] and s['G5_pass']) for n, s in graded.items()}
        # the label needs every graded supply's G3 decided, and G4 decided wherever G3 passes
        complete = all(s['G3_decided'] and (s['G4_decided'] and s['G5_decided'] if s['G3_pass'] else True) for s in graded.values())
        P(f"G7 Bullet (ESTIMATE): Kn = 3 nu_F/(sigma L) = {Kn:.4f} (nu_F {nuF:.1f} kpc km/s, 1000 km/s, 100 kpc) -> "
          f"{'collisional: the hot charge shocks with the gas; RB1 gate 4 reads as its arm M4 (FAIL)' if Kn <= 0.1 else 'not collisional by this estimate'}")
        if not allka:
            lab = 'NO VERDICT (a known answer fails)'
        elif not F['G1']['pass']:
            lab = 'NO VERDICT (VSH1 NOT REPRODUCED)'
        elif not RES['G2']['pass'] or not complete:
            lab = 'NO VERDICT'
        elif any(surv.values()) and not F['G7']['fails_estimate']:
            lab = 'JOINT DERIVED'
        elif not g3_seed and not g3_cos:
            lab = 'STANDS BUT MISCOUNTED'
        elif all((not s['G4_pass']) for s in graded.values() if s['G3_pass']):
            lab = 'STANDS WITH A WALL'
        else:
            lab = 'NO VERDICT (unlisted case; see gates)'
        F['survives'] = surv; F['label'] = lab; F['G3_seed'] = g3_seed; F['G3_cosmo'] = g3_cos
        P(f"LABEL {f}: {lab}  [G1 {F['G1']['pass']}, G2 {RES['G2']['pass']}, G3 S-seed {g3_seed}, G3 S-cosmo {g3_cos} (H1 {h1['G3_pass']}, H2 {h2['G3_pass']}), "
          f"G4 S-seed {seedS['G4_pass']}, H1 {h1['G4_pass']}, H2 {h2['G4_pass']}; G5 S-seed {seedS['G5_pass']}, H1 {h1['G5_pass']}, H2 {h2['G5_pass']}; survives {surv}]")
        if MUT:
            m1 = load('seed_canonical_10.5_N300_M1')
            b1 = bool(m1 is not None and not m1['settled_vsh1_rule'])
            b2 = bool(h1['G3_M2_pass'] or h2['G3_M2_pass']) and not g3_cos
            # G4 must flip to PASS; G3 under S-seed must fail at every mass with at least one mass flipping from pass to fail
            b3 = bool(seedS['G4_M3_pass'] and not seedS['G4_pass'] and all(not v['pass'] for v in seedS['G3_M3'].values())
                      and any(v['pass'] for v in seedS['G3'].values()))
            F['MUTATE'] = {'M1_bites': b1, 'M1_status': m1['status'] if m1 else None, 'M1_S': m1['S'] if m1 else None, 'M1_R_sh': m1['R_sh'] if m1 else None,
                           'M2_bites': b2, 'M2_H1_G3': h1['G3_M2_pass'], 'M2_H2_G3': h2['G3_M2_pass'],
                           'M3_bites': b3, 'M3_G4_seed': seedS['G4_M3_pass'], 'M3_G3_seed': seedS['G3_M3_pass'],
                           'M3_G3_seed_dex': {k: v['max_abs_dev_dex'] for k, v in seedS['G3_M3'].items()}}
            P(f"MUTATE M1 heat removed (canonical 10.5, N 300): {m1['status'] if m1 else 'missing'}, R_sh {fmt(m1['R_sh']) if m1 else 'n/a'}, S {fmt(m1['S']) if m1 else 'n/a'} -> "
              f"{'BITES (not SETTLED)' if b1 else 'DOES NOT BITE'}")
            P(f"MUTATE M2 hot charge zero: S-cosmo G3 H1 {h1['G3_M2_pass']}, H2 {h2['G3_M2_pass']} (primary {g3_cos}) -> {'BITES' if b2 else 'DOES NOT BITE'}")
            P(f"MUTATE M3 law off for the standing clock: S-seed G4 {seedS['G4_M3_pass']} (primary {seedS['G4_pass']}), S-seed G3 per mass {[v['pass'] for v in seedS['G3_M3'].values()]} (primary {[v['pass'] for v in seedS['G3'].values()]}; "
              f"max dex {', '.join(f'{v:.2f}' for v in F['MUTATE']['M3_G3_seed_dex'].values())}) -> {'BITES' if b3 else 'DOES NOT BITE'}")
    # G6, footing dependence: the law's temperature has d ln sigma^4 / d ln a0 = 1
    try:
        dl = math.log(L.a0_of('alt') / L.a0_of('canonical')); RES['G6_dln_sigma4_dln_a0'] = {}
        for sname in ('S-seed', 'S-cosmo H1'):
            row = {}
            for m in MASSES:
                sc = RES['footings']['canonical']['supplies'][sname]['G6'][str(m)]['inside_R_st']['sigma_kms']
                sa = RES['footings']['alt']['supplies'][sname]['G6'][str(m)]['inside_R_st']['sigma_kms']
                row[str(m)] = 4 * math.log(sa / sc) / dl
            RES['G6_dln_sigma4_dln_a0'][sname] = row
            P(f"\nG6 (reported) {sname}: d ln sigma^4 / d ln a0 between the footings: " + ' / '.join(f'{v:+.4f}' for v in row.values()) + ' (the law: 1)')
    except KeyError:
        pass
    P('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
    name = 'vsj1_MUTATE' if MUT else 'vsj1_grade'
    json.dump(RES, open(os.path.join(HERE, name + '.json'), 'w'), indent=1)
    open(os.path.join(HERE, name + '.out'), 'w').write('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
