#!/usr/bin/env python3
# FINAL-7F (FORMATION READING): is DD1's class-median residual an integral of a history
# (formation) or a function of a present-state variable (force)?
#
# Reads DD1's frozen table only. Criteria PREREGISTER.md (committed alone, before this file).
# Footings never pooled. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
import csv, json, math, os, sys, time
import numpy as np

T0 = time.time()
HERE = __file__.rsplit('/', 1)[0]
# 2026-11-12: TABLE was an absolute path; it now resolves from this file, to the same file.
TABLE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'fable52_push', 'DD1_deduce_from_data', 'dd1_table.csv'))
SEED = 20261112
NPERM = 100000
NBOOT = 10000

A0 = {'can': 9.3603e-11, 'alt': 1.1312e-10}
FOOTINGS = ['can', 'alt']
G_SI = 6.67430e-11
KPC_M = 3.0856775814913673e19
C_SI = 2.99792458e8

LINE_DEX = 0.10          # DD1's |off| line
LINE_SIG = 3.0           # DD1's 3 se line
SIGMA_RAW_HISTORY = 0.25  # L5/L6 boundary
F_DETECT = 0.30          # minimum robust scatter reduction for a carrying detection
HOLM_ALPHA = 0.05

# ---------------------------------------------------------------- table
def load_table(path=TABLE):
    rows = []
    with open(path) as fh:
        hdr = None
        for line in fh:
            line = line.rstrip('\r\n')
            if not line.strip():
                continue
            if line.startswith('#'):
                continue
            if hdr is None:
                hdr = line.strip().split(',')
                continue
            r = dict(zip(hdr, line.strip().split(',')))
            if r['bracket'] != '':
                continue                      # main bracket only
            try:
                rec = dict(
                    cls=r['cls'], sys=r['sys'],
                    r=float(r['r_kpc']), lgb=float(r['lgb']), lgo=float(r['lgo']),
                    eY=float(r['eY']), z=float(r['z']),
                    lSig=(float(r['lSig']) if r['lSig'] not in ('nan', '', 'NaN') else float('nan')),
                    last=(int(r['last']) if r['last'] not in ('', 'nan') else 0),
                )
            except ValueError:
                continue
            rows.append(rec)
    return rows

def med(v):
    v = [x for x in v if x is not None and not (isinstance(x, float) and math.isnan(x))]
    if not v:
        return float('nan')
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])

def mad(v):
    m = med(v)
    return med([abs(x - m) for x in v])

# ---------------------------------------------------------------- the law
def XL(lgb, a0):
    gb = 10.0 ** lgb
    return (math.sqrt(1.0 + 4.0 * a0 / gb) - 1.0) / 2.0

def YL(lgb, a0):
    return math.log10(1.0 + XL(lgb, a0))

def YL_vec(lgb, a0):
    gb = np.power(10.0, lgb)
    return np.log10(1.0 + (np.sqrt(1.0 + 4.0 * a0 / gb) - 1.0) / 2.0)

# ---------------------------------------------------------------- statistics
def kendall_taub(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = len(x)
    sx = np.sign(x[:, None] - x[None, :])
    sy = np.sign(y[:, None] - y[None, :])
    iu = np.triu_indices(n, 1)
    a, b = sx[iu], sy[iu]
    num = float(np.sum(a * b))
    tx = float(np.sum(np.abs(a)))          # non-tied pairs in x
    ty = float(np.sum(np.abs(b)))          # non-tied pairs in y
    n0 = n * (n - 1) / 2.0
    n1 = float(sum(t * (t - 1) / 2.0 for t in
                   [len(list(g)) for _, g in __import__('itertools').groupby(sorted(x))]))
    n2 = float(sum(t * (t - 1) / 2.0 for t in
                   [len(list(g)) for _, g in __import__('itertools').groupby(sorted(y))]))
    den = math.sqrt((n0 - n1) * (n0 - n2)) if (n0 - n1) > 0 and (n0 - n2) > 0 else 0.0
    tau = num / den if den > 0 else 0.0
    # normal-approximation p (tie-corrected variance)
    var = (4 * n + 10) / (9.0 * n * (n - 1)) if n > 1 else 0.0  # crude; permutation p is primary
    zt = tau / math.sqrt(2 * (2 * n + 5) / (9.0 * n * (n - 1))) if n > 1 else 0.0
    p_norm = 2 * 0.5 * math.erfc(abs(zt) / math.sqrt(2))
    return dict(tau=tau, num=num, den=den, n0=n0, n1=n1, n2=n2,
                ties_x=1 - tx / n0, ties_y=1 - ty / n0, p_norm=p_norm)

def rankdata(v):
    v = np.asarray(v, float)
    order = np.argsort(v, kind='mergesort')
    r = np.empty(len(v), float)
    r[order] = np.arange(1, len(v) + 1, dtype=float)
    # average ties
    s = np.asarray(sorted(v))
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        if j > i:
            idx = np.where(v == s[i])[0]
            r[idx] = 0.5 * (i + 1 + j + 1)
        i = j + 1
    return r

def spearman(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    den = math.sqrt(float(np.sum(rx * rx)) * float(np.sum(ry * ry)))
    return float(np.sum(rx * ry) / den) if den > 0 else 0.0

def tie_groups(v):
    import itertools
    return [len(list(g)) for _, g in itertools.groupby(sorted(np.asarray(v, float)))]

def perm_p(x, y, rng, nperm=NPERM, batch=2000):
    """Two-sided permutation p for Kendall tau-b and Spearman rho, permuting y (the residual).
    Batches of permutations so the 100k draws stay cheap; identical statistic, identical seed."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = len(x)
    A = np.sign(x[:, None] - x[None, :]).astype(np.float64)      # antisymmetric, fixed
    B = np.sign(y[:, None] - y[None, :]).astype(np.float64)      # antisymmetric, fixed
    n0 = n * (n - 1) / 2.0
    n1 = float(sum(t * (t - 1) / 2.0 for t in tie_groups(x)))
    n2 = float(sum(t * (t - 1) / 2.0 for t in tie_groups(y)))
    den = math.sqrt((n0 - n1) * (n0 - n2)) if (n0 - n1) > 0 and (n0 - n2) > 0 else 0.0
    tau_obs = (0.5 * float(np.sum(A * B))) / den if den > 0 else 0.0
    rho_obs = spearman(x, y)
    rx = rankdata(x); ry = rankdata(y)
    rxc = rx - rx.mean(); ryc = ry - ry.mean()
    sxx = float(np.sum(rxc * rxc)); syy = float(np.sum(ryc * ryc))
    cnt_t = 0; cnt_r = 0
    done = 0
    while done < nperm:
        m = min(batch, nperm - done); done += m
        Pm = np.argsort(rng.random((m, n)), axis=1)              # m independent permutations
        Bs = B[Pm[:, :, None], Pm[:, None, :]]                   # (m,n,n)
        taus = (0.5 * np.sum(A[None, :, :] * Bs, axis=(1, 2))) / den if den > 0 else np.zeros(m)
        cnt_t += int(np.sum(np.abs(taus) >= abs(tau_obs) - 1e-12))
        rhos = np.sum(rxc[None, :] * ryc[Pm], axis=1) / math.sqrt(sxx * syy)
        cnt_r += int(np.sum(np.abs(rhos) >= abs(rho_obs) - 1e-12))
    return (cnt_t + 1) / (nperm + 1), (cnt_r + 1) / (nperm + 1)

def lad_line(x, y):
    """Exact least-absolute-deviation line: an LAD fit with one predictor passes through two points."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = len(x)
    Dx = x[:, None] - x[None, :]
    Dy = y[:, None] - y[None, :]
    ok = np.abs(Dx) > 1e-12
    with np.errstate(divide='ignore', invalid='ignore'):
        b = np.where(ok, Dy / np.where(ok, Dx, 1.0), np.nan)
    a = y[:, None] - b * x[:, None]
    S = np.sum(np.abs(y[None, None, :] - a[:, :, None] - b[:, :, None] * x[None, None, :]), axis=2)
    S = np.where(ok, S, np.inf)
    i, j = np.unravel_index(np.nanargmin(S), S.shape)
    return float(a[i, j]), float(b[i, j])

def boot_slope(x, y, rng, nboot=NBOOT):
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = len(x)
    out = np.empty(nboot)
    for k in range(nboot):
        idx = rng.integers(0, n, n)
        xs, ys = x[idx], y[idx]
        if np.ptp(xs) <= 1e-12:
            out[k] = float('nan'); continue
        out[k] = lad_line(xs, ys)[1]
    out = out[~np.isnan(out)]
    if len(out) == 0:
        return float('nan'), float('nan')
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))

def partial_kendall(x, y, z):
    """Kendall between rank-residuals of x and y after linear detrending on z's ranks."""
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    rx = rx - np.polyval(np.polyfit(rz, rx, 1), rz)
    ry = ry - np.polyval(np.polyfit(rz, ry, 1), rz)
    return kendall_taub(rx, ry)['tau']

def holm(pairs):
    """pairs: list of (name, p). Returns dict name -> (p_holm, rank)."""
    s = sorted(pairs, key=lambda t: t[1])
    m = len(s)
    out, run = {}, 0.0
    for i, (nm, p) in enumerate(s):
        run = max(run, min(1.0, (m - i) * p))
        out[nm] = (run, i + 1)
    return out

# ---------------------------------------------------------------- build the lane's numbers
def build(rows, a0):
    # per point
    for r in rows:
        r['Y'] = r['lgo'] - r['lgb']
        r['YL'] = YL(r['lgb'], a0)
        r['d'] = r['Y'] - r['YL']
        r['lr'] = math.log10(r['r'])
        r['lMb'] = r['lgb'] + 2.0 * math.log10(r['r'] * KPC_M) - math.log10(G_SI)
        r['dep'] = r['lgo'] + math.log10(r['r'] * KPC_M) - 2.0 * math.log10(C_SI)
        r['zz'] = math.log10(r['z'] + 0.001)
    # per system
    sysd = {}
    for r in rows:
        sysd.setdefault((r['cls'], r['sys']), []).append(r)
    sysv = {}
    for key, rs in sysd.items():
        last = [r for r in rs if r['last'] == 1]
        if not last:
            mx = max(r['r'] for r in rs)
            last = [r for r in rs if r['r'] == mx]
        sysv[key] = dict(
            cls=key[0], sys=key[1],
            d=med([r['d'] for r in rs]),
            e=med([r['eY'] for r in rs if not math.isnan(r['eY'])]),
            zz=med([r['zz'] for r in rs]),
            lgb=med([r['lgb'] for r in rs]),
            lgo=med([r['lgo'] for r in rs]),
            lgb_last=med([r['lgb'] for r in last]),
            lgo_last=med([r['lgo'] for r in last]),
            lr=med([r['lr'] for r in rs]),
            lMb=med([r['lMb'] for r in rs]),
            dep=med([r['dep'] for r in rs]),
            dsys=max(r['dep'] for r in rs),
            lSig=med([r['lSig'] for r in rs if not math.isnan(r['lSig'])]),
            npts=len(rs),
        )
    # per class
    bycls = {}
    for key, v in sysv.items():
        bycls.setdefault(v['cls'], []).append(v)
    cls = {}
    for c, vs in bycls.items():
        ds = [v['d'] for v in vs]
        n = len(vs)
        if n >= 2:
            se = max(1.2533 * 1.4826 * mad(ds) / math.sqrt(n),
                     math.sqrt(sum((v['e'] if not math.isnan(v['e']) else 0.0) ** 2 for v in vs)) / n)
        else:
            se = vs[0]['e']
        cls[c] = dict(
            n_sys=n, n_pts=sum(v['npts'] for v in vs),
            d=med(ds), se=se, mads=1.4826 * mad(ds) if n >= 2 else float('nan'),
            zz=med([v['zz'] for v in vs]),
            lgb=med([v['lgb'] for v in vs]),
            lgo=med([v['lgo'] for v in vs]),
            lgb_last=med([v['lgb_last'] for v in vs]),
            lgo_last=med([v['lgo_last'] for v in vs]),
            lr=med([v['lr'] for v in vs]),
            lMb=med([v['lMb'] for v in vs]),
            dep=med([v['dep'] for v in vs]),
            dsys=med([v['dsys'] for v in vs]),
            lSig=med([v['lSig'] for v in vs if not math.isnan(v['lSig'])]),
            YL=YL(med([v['lgb'] for v in vs]), a0),
        )
        cls[c]['nsig'] = sum(1 for v in vs if not math.isnan(v['lSig']))
    return cls, sysv, sysd

VARS = {
    'E1':  dict(key='zz',       label='zz  = log10(z+0.001)                     [epoch, the only measured one]', kind='epoch'),
    'B1':  dict(key='lgb',      label='lgb = log10 g_bar (= log10 Sigma_b(point)) ', kind='present'),
    'B2':  dict(key='lgb_last', label='lgb at the outermost point (aperture-matched Sigma_b)', kind='present'),
    'D1':  dict(key='lgo',      label='lgo = log10 g_obs (= log10 Sigma_dyn(point))', kind='present'),
    'D2':  dict(key='lgo_last', label='lgo at the outermost point (aperture-matched Sigma_dyn)', kind='present'),
    'P1':  dict(key='lr',       label='lr  = log10 r (kpc)                       [size]', kind='present'),
    'P2':  dict(key='lMb',      label='lMb = log10 enclosed baryon mass          [mass]', kind='present'),
    'P3':  dict(key='dep',      label='dep = log10(g_obs r / c^2)                [local depth]', kind='present'),
    'P4':  dict(key='dsys',     label='dsys= system max depth                    [system depth]', kind='present'),
    'C1':  dict(key='YL',       label='YL  = log10(1+X_L) at the class g_bar     [confound: law shape]', kind='confound'),
}
FAMILY = ['E1', 'B1', 'B2', 'D1', 'D2', 'P1', 'P2', 'P3', 'P4', 'C1']
PRESENT = ['B1', 'B2', 'D1', 'D2', 'P1', 'P2', 'P3', 'P4']

def analyse(classes, dvec, rng, family=FAMILY, nperm=NPERM):
    """dvec: dict cls -> residual. Returns per-variable stats + raw scatter."""
    cl = list(classes)
    d = np.array([dvec[c] for c in cl], float)
    sigma_raw = 1.4826 * float(np.median(np.abs(d - np.median(d))))
    rms_raw = float(np.sqrt(np.mean((d - d.mean()) ** 2)))
    res = dict(sigma_raw=sigma_raw, rms_raw=rms_raw, rng_range=float(d.max() - d.min()))
    out = {}
    for vid in family:
        v = np.array([classes[c][VARS[vid]['key']] for c in cl], float)
        ok = ~(np.isnan(v) | np.isnan(d))
        vv, dd = v[ok], d[ok]
        kt = kendall_taub(vv, dd)
        rho = spearman(vv, dd)
        pt, pr = perm_p(vv, dd, rng, nperm=nperm)
        a, b = lad_line(vv, dd)
        fit = a + b * vv
        resid = dd - fit
        sigma_imp = 1.4826 * float(np.median(np.abs(resid - np.median(resid))))
        rms_imp = float(np.sqrt(np.mean(resid ** 2)))
        f = 1.0 - sigma_imp / sigma_raw if sigma_raw > 0 else float('nan')
        var_raw = float(np.var(dd, ddof=1)); var_imp = float(np.var(resid, ddof=1))
        R2 = 1.0 - var_imp / var_raw if var_raw > 0 else float('nan')
        lo, hi = boot_slope(vv, dd, np.random.default_rng(SEED + 7))
        out[vid] = dict(
            n=int(ok.sum()), tau=kt['tau'], rho=rho, p_tau_perm=pt, p_rho_perm=pr,
            p_tau_norm=kt['p_norm'], slope=b, slope_lo=lo, slope_hi=hi, intercept=a,
            sigma_imp=sigma_imp, rms_imp=rms_imp, f=f, R2=R2,
            ties_v=kt['ties_x'], ties_d=kt['ties_y'],
            degenerate=(kt['ties_x'] > 0.90),
            v_first=float(vv[0]),
        )
    res['vars'] = out
    return res

def label_me(res, classes, dvec):
    cl = list(classes)
    d = np.array([dvec[c] for c in cl], float)
    sigma_raw = res['sigma_raw']
    nsys3se = 0
    for c in cl:
        se = classes[c]['se']
        if se > 0 and abs(dvec[c]) > LINE_SIG * se:
            nsys3se += 1
    P0 = dict(sigma_raw=sigma_raw, n_beyond_3se=nsys3se,
              median_se=float(np.median([classes[c]['se'] for c in cl])),
              rng_range=res['rng_range'])
    if sigma_raw <= 0.10 and nsys3se == 0:
        return 'NO CLASS SPREAD - FORCE READING NOT EXCLUDED', P0, {}
    # Holm
    fam = [v for v in FAMILY if v in res['vars'] and not res['vars'][v]['degenerate']]
    excl = [v for v in FAMILY if v in res['vars'] and res['vars'][v]['degenerate']]
    holm_adj = holm([(v, res['vars'][v]['p_tau_perm']) for v in fam])
    det, mixed = [], []
    for v in fam:
        s = res['vars'][v]
        s['p_holm'] = holm_adj[v][0]
        s['detected'] = bool(s['p_holm'] <= HOLM_ALPHA and np.sign(s['tau']) == np.sign(s['rho'])
                             and np.sign(s['rho']) != 0)
        s['carrying'] = bool(s['detected'] and s['f'] >= F_DETECT)
        if s['detected'] and not s['carrying']:
            s['note'] = 'detected but f < %.2f' % F_DETECT
        if s['detected']:
            det.append(v)
        elif np.sign(s['tau']) != np.sign(s['rho']):
            mixed.append(v)
    pdet = [v for v in det if v in PRESENT]
    pcar = [v for v in pdet if res['vars'][v]['carrying']]
    edet = 'E1' in det
    if pcar and not edet:
        lab = 'PRESENT-STATE ORGANIZED (force-like)'
    elif pcar and edet:
        lab = 'PRESENT-STATE ORGANIZED, EPOCH ALSO'
    elif edet and not pdet:
        lab = 'EPOCH ORGANIZED'
    elif not det:
        lab = ('NOT A FUNCTION OF ANY TESTED VARIABLE (history-like)' if sigma_raw >= SIGMA_RAW_HISTORY
               else 'NO STRUCTURE')
    else:
        lab = 'MIXED'
    if det == ['C1']:
        lab += ', confounded by the law shape'
    P0['excluded_degenerate'] = excl
    return lab, P0, dict(detected=det, carrying=pcar, mixed=mixed)

# ---------------------------------------------------------------- main
def main():
    rows = load_table()
    nsys = len(set((r['cls'], r['sys']) for r in rows))
    out = dict(meta=dict(lane='FINAL7F', seed=SEED, nperm=NPERM, nboot=NBOOT,
                         table='fable52_push/DD1_deduce_from_data/dd1_table.csv',
                         n_points=len(rows), n_systems=nsys,
                         n_classes=len(set(r['cls'] for r in rows)),
                         a0=A0, kappa='1/2 FITTED; not theory closed'))
    print('FINAL-7F (FORMATION READING)  points %d  systems %d  classes %d'
          % (len(rows), nsys, len(set(r['cls'] for r in rows))))

    foot = {}
    for f in FOOTINGS:
        cls, sysv, sysd = build(rows, A0[f])
        foot[f] = dict(cls=cls, sysv=sysv)
        # point-median residuals, computed while this footing's per-point d is in `rows`
        foot[f]['pt_med'] = {c: med([r['d'] for r in rows if r['cls'] == c]) for c in cls}
    order = sorted(foot['can']['cls'], key=lambda c: foot['can']['cls'][c]['d'])
    out['class_order'] = order
    out['classes'] = {f: foot[f]['cls'] for f in FOOTINGS}

    # ---------------- KA1: reproduction of DD1 / FINAL-2
    KA = {}
    fin2 = {'tidal dwarfs': -0.687, 'NGC 1052 UDGs': -0.843, 'MW ultra-faints': 0.592,
            'M31 dwarfs': 0.090, 'faint rotators': -0.239, 'X-COP': 0.504}
    dev = {}
    for c, v in fin2.items():
        dev[c] = dict(system_median=foot['can']['cls'][c]['d'],
                      point_median=foot['can']['pt_med'][c],
                      fin2=v, dev_point=foot['can']['pt_med'][c] - v,
                      dev_sys=foot['can']['cls'][c]['d'] - v)
    KA['KA1'] = dict(per_class=dev,
                     max_abs_dev_point=max(abs(d['dev_point']) for d in dev.values()),
                     max_abs_dev_sys=max(abs(d['dev_sys']) for d in dev.values()),
                     range_can=foot['can']['cls'][order[-1]]['d'] - foot['can']['cls'][order[0]]['d'])
    # footing offset
    deep = [c for c in order if foot['can']['cls'][c]['lgb'] < math.log10(A0['can'])]
    diff = [foot['alt']['cls'][c]['d'] - foot['can']['cls'][c]['d'] for c in order]
    diff_deep = [foot['alt']['cls'][c]['d'] - foot['can']['cls'][c]['d'] for c in deep]
    KA['KA2'] = dict(n_deep=len(deep), deep_classes=deep,
                     median_diff_deep=med(diff_deep),
                     expected=-0.5 * math.log10(A0['alt'] / A0['can']),
                     median_diff_all=med(diff))
    # KA4 identities
    errs = []
    for lgb in np.linspace(-3, 3, 601):
        gb = 10.0 ** lgb
        for a0 in A0.values():
            g = 0.5 * (gb + math.sqrt(gb * gb + 4 * a0 * gb))
            errs.append(abs(gb * (g + a0) - g * g) / (gb * (g + a0)))
            errs.append(abs((1 + XL(lgb, a0)) - g / gb) / (g / gb))
    KA['KA4'] = dict(max_rel_err=max(errs), grid=601)
    out['KA'] = KA

    # ---------------- P0 + correlations
    rng = np.random.default_rng(SEED)
    results = {}
    for f in FOOTINGS:
        cls = foot[f]['cls']
        dvec = {c: cls[c]['d'] for c in order}
        res = analyse(cls, dvec, rng)
        lab, P0, dd = label_me(res, cls, dvec)
        res['label'] = lab; res['P0'] = P0; res['decision'] = dd
        results[f] = res
        print('\n=== footing %s ===' % f)
        print('P0: sigma_raw %.4f  rms_raw %.4f  range %.4f  classes beyond 3 se: %d  median se %.4f'
              % (P0['sigma_raw'], res['rms_raw'], P0['rng_range'], P0['n_beyond_3se'], P0['median_se']))
        print('%-18s %4s %8s %7s %8s %7s %7s %7s %7s %7s %7s %7s %7s %7s' %
              ('class', 'nsys', 'd', 'se', 'zz', 'lgb', 'lgo', 'lgb_l', 'lgo_l', 'lr', 'lMb', 'dep', 'dsys', 'lSig'))
        for c in order:
            s = cls[c]
            print('%-18s %4d %+8.3f %7.3f %+8.3f %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f'
                  % (c, s['n_sys'], s['d'], s['se'], s['zz'], s['lgb'], s['lgo'], s['lgb_last'],
                     s['lgo_last'], s['lr'], s['lMb'], s['dep'], s['dsys'], s['lSig']))
        print('%-4s %-9s %-9s %-9s %-9s %-7s %-7s %-6s %-6s %s' %
              ('id', 'tau', 'p_tau', 'p_holm', 'rho', 'slope', 'f', 'sig_imp', 'det', 'label'))
        for vid in FAMILY:
            s = res['vars'][vid]
            print('%-4s %+9.4f %9.4f %9.4f %+9.4f %+7.3f %+7.3f %6.3f %-6s %s' %
                  (vid, s['tau'], s['p_tau_perm'], s.get('p_holm', float('nan')), s['rho'],
                   s['slope'], s['f'], s['sigma_imp'], str(s.get('detected', '')),
                   'DEGENERATE' if s['degenerate'] else ''))
        # partial correlations for the D/B degeneracy
        pc = {}
        for (a, b) in [('D1', 'B1'), ('B1', 'D1'), ('D2', 'B2'), ('B2', 'D2'), ('E1', 'B1')]:
            x = np.array([cls[c][VARS[a]['key']] for c in order])
            y = np.array([cls[c][VARS[b]['key']] for c in order])
            pc['%s|%s' % (a, b)] = partial_kendall(x, dvec_arr(order, dvec), y)
        res['partial'] = pc
        # lSig, 9 classes, outside the Holm family
        sub = [c for c in order if not math.isnan(cls[c]['lSig']) and cls[c]['nsig'] >= 3]
        if len(sub) >= 5:
            v = np.array([cls[c]['lSig'] for c in sub]); dd2 = np.array([dvec[c] for c in sub])
            kt = kendall_taub(v, dd2)
            pt, pr = perm_p(v, dd2, np.random.default_rng(SEED + 3), nperm=20000)
            a_, b_ = lad_line(v, dd2)
            imp = 1.4826 * float(np.median(np.abs((dd2 - (a_ + b_ * v)) - np.median(dd2 - (a_ + b_ * v)))))
            sraw = 1.4826 * float(np.median(np.abs(dd2 - np.median(dd2))))
            res['B3'] = dict(classes=sub, n=len(sub), tau=kt['tau'], rho=spearman(v, dd2),
                             p_tau_perm=pt, p_rho_perm=pr, slope=b_,
                             sigma_raw=sraw, sigma_imp=imp, f=1 - imp / sraw if sraw else float('nan'))
        print('LABEL: %s' % lab)
        print('detected %s  carrying %s' % (dd.get('detected'), dd.get('carrying')))
    out['results'] = results

    # ---------------- KA3 synthetic truths
    KA3 = {}
    cls = foot['can']['cls']
    base = {c: cls[c]['d'] for c in order}
    def medv(key):
        return float(np.median([cls[c][key] for c in order]))
    plants = {
        'i_zz':    ('E1', {c: 0.30 * (cls[c]['zz'] - medv('zz')) for c in order}),
        'ii_lgb':  ('B1', {c: 0.30 * (cls[c]['lgb'] - medv('lgb')) for c in order}),
        'iii_lgo': ('D1', {c: 0.30 * (cls[c]['lgo'] - medv('lgo')) for c in order}),
        'iv_zero': (None, {c: 0.0 for c in order}),
        'v_shuf':  (None, {c: base[s] for c, s in zip(order, list(np.random.default_rng(SEED).permutation(order)))}),
    }
    for name, (target, dv) in plants.items():
        r = analyse(cls, dv, np.random.default_rng(SEED + 11), nperm=20000)
        lab, P0, dd = label_me(r, cls, dv)
        KA3[name] = dict(target=target, label=lab, detected=dd.get('detected'),
                         sigma_raw=r['sigma_raw'],
                         tau={v: r['vars'][v]['tau'] for v in FAMILY},
                         p_holm={v: r['vars'][v].get('p_holm') for v in FAMILY},
                         f={v: r['vars'][v]['f'] for v in FAMILY})
    out['KA3'] = KA3
    print('\nKA3 synthetic: ' + '; '.join('%s -> %s' % (k, v['label']) for k, v in KA3.items()))

    # ---------------- MUTATE
    M = {}
    for f in FOOTINGS:
        cls = foot[f]['cls']
        dvec = {c: cls[c]['d'] for c in order}
        # M1 shuffle
        sh = list(np.random.default_rng(SEED).permutation(order))
        d1 = {c: dvec[s] for c, s in zip(order, sh)}
        r1 = analyse(cls, d1, np.random.default_rng(SEED + 1), nperm=20000)
        l1, p01, d1d = label_me(r1, cls, d1)
        maxt = max(abs(r1['vars'][v]['tau']) for v in FAMILY)
        maxt0 = max(abs(results[f]['vars'][v]['tau']) for v in FAMILY)
        # M2 plant epoch
        mz = float(np.median([cls[c]['zz'] for c in order]))
        d2 = {c: dvec[c] + 0.5 * (cls[c]['zz'] - mz) for c in order}
        r2 = analyse(cls, d2, np.random.default_rng(SEED + 2), nperm=20000)
        l2, p02, d2d = label_me(r2, cls, d2)
        # M3 plant present-state
        mo = float(np.median([cls[c]['lgo'] for c in order]))
        d3 = {c: dvec[c] + 0.5 * (cls[c]['lgo'] - mo) for c in order}
        r3 = analyse(cls, d3, np.random.default_rng(SEED + 3), nperm=20000)
        l3, p03, d3d = label_me(r3, cls, d3)
        # M4 drop the two R-channel classes
        keep = [c for c in order if c not in ('tidal dwarfs', 'NGC 1052 UDGs')]
        cls4 = {c: cls[c] for c in keep}; d4 = {c: dvec[c] for c in keep}
        r4 = analyse(cls4, d4, np.random.default_rng(SEED + 4), nperm=20000)
        l4, p04, d4d = label_me(r4, cls4, d4)
        M[f] = dict(
            M1=dict(label=l1, detected=d1d.get('detected'), max_abs_tau=maxt,
                    max_abs_tau_orig=maxt0, bites=(len(d1d.get('detected', [])) == 0
                                                   and maxt <= maxt0 - 0.20)),
            M2=dict(label=l2, detected=d2d.get('detected'),
                    tau_E1=r2['vars']['E1']['tau'], p_holm_E1=r2['vars']['E1'].get('p_holm'),
                    bites=('E1' in d2d.get('detected', []) and l2 != results[f]['label'])),
            M3=dict(label=l3, carrying=d3d.get('carrying'),
                    tau_D1=r3['vars']['D1']['tau'], f_D1=r3['vars']['D1']['f'],
                    p_holm_D1=r3['vars']['D1'].get('p_holm'),
                    bites=('D1' in d3d.get('carrying', []) and l3.startswith('PRESENT-STATE'))),
            M4=dict(label=l4, detected=d4d.get('carrying'), n=len(keep),
                    sigma_raw=r4['sigma_raw'],
                    new_carrying=[v for v in d4d.get('carrying', [])
                                  if v not in results[f]['decision'].get('carrying', [])]),
        )
    # M5 a0 x 2
    cls2, _, _ = build(rows, 2 * A0['can'])
    M['M5'] = dict(sparc_d_can=foot['can']['cls']['SPARC']['d'],
                   sparc_d_a0x2=cls2['SPARC']['d'],
                   delta=cls2['SPARC']['d'] - foot['can']['cls']['SPARC']['d'],
                   bites=abs(cls2['SPARC']['d'] - foot['can']['cls']['SPARC']['d']) > 0.05)
    out['MUTATE'] = M

    out['runtime_s'] = time.time() - T0
    with open(HERE + '/final7f.json', 'w') as fh:
        json.dump(out, fh, indent=1, default=float)
    print('\nwrote final7f.json in %.1f s' % (time.time() - T0))

def dvec_arr(order, dvec):
    return np.array([dvec[c] for c in order], float)

if __name__ == '__main__':
    main()
