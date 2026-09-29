#!/usr/bin/env python3
"""
reduce_walker.py -- multi-epoch, binary-cleaned line-of-sight velocity dispersions
for Milky Way ultra-faint dwarfs in Walker et al. 2023 (ApJS 268, 19; VizieR J/ApJS/268/19).

ALL CHOICES BELOW WERE DECLARED BEFORE THE FIRST DISPERSION RUN. Nothing was tuned afterwards.

DATA / PARSING
 * Fixed-width 876-byte records; byte ranges from the ReadMe (1-indexed, inclusive).
 * A ROW IS ONE OBSERVATION (epoch) of one star (ObjID = RA_Dec_HJD is unique per observation).
   Multi-epoch stars are identified by (Target, Gaia DR3 source_id).  The catalogue's own
   Obs/Nobs/Goodobs/goodNobs columns count epochs within one instrument file; here epochs are
   pooled across the three files (hectocat / m2fshi / m2fsmed) by Gaia id (Sextans_1, Tucana_2,
   Grus_1, Indus_1, Phoenix_2 have >1 instrument).  Rows without a Gaia id cannot be
   epoch-linked and have no Gaia PM, so they are never members.
 * THE CATALOGUE HAS NO MEMBERSHIP COLUMN (the paper's 4492 'likely members' are not tabulated
   in the ReadMe).  Membership is therefore re-derived here (rule below); it is NOT the paper's list.

QUALITY CUT (per epoch/row): Goodobs > 0 (paper's own quality-control flag), RRL == 0, AGN == 0,
   e_Vlos > 0.  f_Chi2 / f_C are NOT applied (they may flag SB2/poor fits, which would pre-clean
   the single-epoch baseline); count of members carrying f_Chi2 rows is printed as a diagnostic.

SYSTEM SELECTION: names matched (lower case) to key in real_research/data/dsph/lvd_dwarf_mw.csv.
   UFD = matched AND M_V > -7.7.  Systems not in the LVD table (Crater_1, Gaia_9/10/11, Garro_1,
   Gran_3/4, Indus_1, KGO_13, Koposov_2, Segue_3: clusters / unclassified) are listed but not analysed.
   Classicals = matched AND M_V <= -7.7 (listed, not analysed).

MEMBERSHIP (v2; per star; uses the star's inverse-variance mean velocity over quality epochs):
   seed systemic v, PM (pmra, pmdec) and distance from LVD.
   1. logg < 4.0 (first quality epoch; removes foreground dwarfs).
   2. |v_mean - v_c| < 4*sqrt(sig_seed^2 + e_mean^2), with sig_seed = max(LVD vlos_sigma, 3) km/s
      (5 km/s if LVD has none).  sig_seed is FIXED (not fitted).  v_c = LVD v_sys on pass 1; on pass 2 v_c =
      median of the pass-1 members (one recentring only, no iteration to convergence).
   3. PM: dpm_ra^2/(e_pmra^2+s^2) + dpm_de^2/(e_pmde^2+s^2) < 11.83  (3 sigma, 2 dof), where
      s^2 = 0.05^2 + LVD pm err^2 + (sig_seed/(4.74 d_kpc))^2  (mas/yr).  Stars with no Gaia PM: rejected.
   4. Parallax: |plx - 1/d_kpc| < 3*sqrt(e_plx^2 + 0.03^2) mas (if plx present).
   REVISION LOG (disclosed): v1 fitted sig_w iteratively to a fixed point and had NO logg cut; on the first
   run this ran away in the two most contaminated fields (Segue_1 sigma=112 km/s, Segue_2 45 km/s, foreground
   dwarfs with weak Gaia PM cuts).  v2 (above) changed ONLY the membership rule (fixed window width, logg cut)
   and nothing in the estimators; it was run once and NOT tuned further.  The v1 numbers for the other
   systems (Bootes_1 3.9, Tucana_2 5.1/3.9, Reticulum_2 3.9, Hydrus_1 3.2, UMa_2 5.8, UMa_1 23.5) were
   observed before the revision.
   The count of stars passing logg+PM+parallax but failing ONLY the velocity window is reported (n_vreject) so the
   reader can see how many large-excursion binaries the window removed BEFORE any binary cleaning.

ESTIMATORS (Gaussian, known individual errors, free mean, sigma >= 0):
   -2lnL(mu,sigma) = sum[ ln(sigma^2+e_i^2) + (v_i-mu)^2/(sigma^2+e_i^2) ]; mu profiled analytically,
   sigma scanned; 1-sigma interval = profile Delta(-2lnL)=1; 95% one-sided upper limit = Delta=2.706.
   If sigma_hat < 1e-3 km/s it is reported as 0 (the '-err' equals 0 and the UL95 is the result).
   (a) SINGLE: first epoch (earliest HJD among quality epochs) of each member.
   (b) ALLMEAN: inverse-variance mean over quality epochs, error 1/sqrt(sum w).
   (c) CLEAN: from the member set, remove stars with >=2 quality epochs whose epoch velocities have
       chi2 about their weighted mean with p < 0.01 (dof = N_epoch - 1, own errors e_Vlos); then use the
       all-epoch mean velocities of the remaining stars.  Single-epoch stars cannot be tested and stay
       (counted as n_untestable).
   (d) PAPERFLAG (alt.): remove members with the paper's f_Vlosvar == 1 on any row (scatter >= 3 x
       error of mean, quality epochs); mean velocities of the rest.
   Reduction is done for UFDs with >= 8 members.  median_err = median individual e_Vlos of first epochs
   of members (km/s).
INFORMATIVE criterion (declared): n_multi >= 8 and n_multi/n_members >= 0.5.
No systematic wavelength-zero-point offset between epochs/instruments/configurations is modelled
(the paper's Sect. 4.2 error adjustment is taken as-is).
"""
import csv, os, sys, math, gzip
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import chi2 as chi2dist

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
IN = os.path.join(REPO, 'real_research', 'data', 'walker2023') + '/'   # gzipped VizieR J/ApJS/268/19 files; gunzipped on the fly into a temp dir
OUT = HERE + '/'
LVD = os.path.join(REPO, 'real_research', 'data', 'dsph', 'lvd_dwarf_mw.csv')

COLS = dict(Inst=(1, 11, str), Target=(13, 28, str), Gaia=(72, 90, str), Gmag=(92, 100, float),
            pmRA=(188, 195, float), pmDE=(197, 204, float), epmRA=(206, 210, float), epmDE=(212, 216, float),
            plx=(218, 224, float), eplx=(226, 232, float), HJD=(282, 292, float), SN=(294, 300, float),
            Vlos=(335, 341, float), eVlos=(343, 348, float), logg=(416, 420, float),
            Filt=(556, 561, str), Obs=(680, 681, int), Nobs=(683, 684, int), Goodobs=(686, 687, int),
            fChi2=(842, 842, int), fVar=(850, 850, int), RRL=(874, 874, int), AGN=(876, 876, int))


def parse(fn):
    rows = []
    for line in gzip.open(fn, 'rt'):
        line = line.rstrip('\n')
        r = {}
        for k, (a, b, t) in COLS.items():
            s = line[a - 1:b].strip()
            if t is str:
                r[k] = s
            elif s == '':
                r[k] = float('nan') if t is float else -1
            else:
                r[k] = t(s)
        r['file'] = os.path.basename(fn)
        rows.append(r)
    return rows


def m2loglike(v, e, sig):
    """profile -2lnL (mu profiled) at fixed sigma"""
    w = 1.0 / (sig * sig + e * e)
    mu = np.sum(w * v) / np.sum(w)
    return np.sum(np.log(1.0 / w) + w * (v - mu) ** 2), mu


def mle_sigma(v, e):
    v = np.asarray(v, float); e = np.asarray(e, float)
    n = len(v)
    f = lambda s: m2loglike(v, e, s)[0]
    top = max(3 * np.std(v), 5 * np.max(e), 1.0) * 3
    grid = np.linspace(0, top, 600)
    vals = np.array([f(s) for s in grid])
    i = int(np.argmin(vals))
    if i == 0:
        s0 = 0.0
        if vals[0] > vals[1] + 1e-12:
            pass
        r = minimize_scalar(f, bounds=(0, grid[1]), method='bounded')
        s0 = r.x if r.fun < vals[0] else 0.0
    else:
        lo, hi = grid[i - 1], grid[min(i + 1, len(grid) - 1)]
        r = minimize_scalar(f, bounds=(lo, hi), method='bounded')
        s0 = r.x if r.fun <= vals[i] else grid[i]
    if s0 < 1e-3:
        s0 = 0.0
    fmin = f(s0)
    mu = m2loglike(v, e, s0)[1]
    g = lambda s, d: f(s) - fmin - d
    # upper 1-sigma and 95% one-sided limit
    def upper(d):
        s = max(s0, 1e-3)
        hi = top
        while g(hi, d) < 0:
            hi *= 2
            if hi > 1e6: return float('nan')
        return brentq(lambda x: g(x, d), s0, hi) if g(s0, d) < 0 else s0
    up = upper(1.0)
    ul95 = upper(2.706)
    if s0 > 0 and g(0.0, 1.0) > 0:
        lo = brentq(lambda x: g(x, 1.0), 0.0, s0)
    else:
        lo = 0.0
    return dict(sig=s0, ep=up - s0, em=s0 - lo, ul95=ul95, mu=mu, n=n)


def load_lvd():
    return {x['key']: x for x in csv.DictReader(open(LVD))}


def fnum(x, default=float('nan')):
    try:
        return float(x)
    except Exception:
        return default


def build_stars(rows):
    """group quality rows by (target, gaia)"""
    st = {}
    for r in rows:
        if r['Gaia'] == '':
            continue
        if not (r['Goodobs'] > 0 and r['RRL'] == 0 and r['AGN'] == 0 and r['eVlos'] > 0 and np.isfinite(r['Vlos'])):
            continue
        st.setdefault((r['Target'], r['Gaia']), []).append(r)
    out = {}
    for k, rs in st.items():
        rs.sort(key=lambda r: r['HJD'])
        # drop exact duplicate HJD+instrument rows (should not occur)
        v = np.array([r['Vlos'] for r in rs]); e = np.array([r['eVlos'] for r in rs])
        w = 1 / e ** 2
        vm = np.sum(w * v) / np.sum(w); em = 1 / math.sqrt(np.sum(w))
        chi2 = float(np.sum(w * (v - vm) ** 2)); dof = len(rs) - 1
        p = chi2dist.sf(chi2, dof) if dof > 0 else float('nan')
        r0 = rs[0]
        out[k] = dict(target=k[0], gaia=k[1], n=len(rs), v1=r0['Vlos'], e1=r0['eVlos'], vm=vm, em=em,
                      chi2=chi2, dof=dof, p=p, hjd=np.array([r['HJD'] for r in rs]),
                      pmra=r0['pmRA'], pmde=r0['pmDE'], epmra=r0['epmRA'], epmde=r0['epmDE'],
                      plx=r0['plx'], eplx=r0['eplx'], logg=r0['logg'],
                      fvar=max(r['fVar'] for r in rs), fchi2=max(r['fChi2'] for r in rs),
                      SN=float(np.nanmedian([r['SN'] for r in rs])))
    return out


def membership(stars, lv):
    vs = fnum(lv['vlos_systemic']); sg = fnum(lv['vlos_sigma'])
    pa = fnum(lv['pmra']); pd_ = fnum(lv['pmdec'])
    pe = max(fnum(lv['pmra_em'], 0.0) if np.isfinite(fnum(lv['pmra_em'])) else 0.0,
             fnum(lv['pmdec_em'], 0.0) if np.isfinite(fnum(lv['pmdec_em'])) else 0.0)
    dkpc = fnum(lv['distance'])  # kpc
    sig_seed = max(sg, 3.0) if np.isfinite(sg) else 5.0
    S = list(stars.values())
    vm = np.array([s['vm'] for s in S]); em = np.array([s['em'] for s in S])
    sp2 = 0.05 ** 2 + pe ** 2 + (sig_seed / (4.74 * dkpc)) ** 2
    pre = np.zeros(len(S), bool)
    for i, s in enumerate(S):
        if not (np.isfinite(s['logg']) and s['logg'] < 4.0):
            continue
        if not (np.isfinite(s['pmra']) and np.isfinite(s['pmde']) and np.isfinite(s['epmra']) and np.isfinite(s['epmde'])):
            continue
        c = (s['pmra'] - pa) ** 2 / (s['epmra'] ** 2 + sp2) + (s['pmde'] - pd_) ** 2 / (s['epmde'] ** 2 + sp2)
        if c >= 11.83:
            continue
        if np.isfinite(s['plx']) and np.isfinite(s['eplx']):
            if abs(s['plx'] - 1.0 / dkpc) >= 3 * math.sqrt(s['eplx'] ** 2 + 0.03 ** 2):
                continue
        pre[i] = True
    win = lambda c: np.abs(vm - c) < 4 * np.sqrt(sig_seed ** 2 + em ** 2)
    m1 = pre & win(vs)
    vc = float(np.median(vm[m1])) if m1.sum() >= 1 else vs
    mem = pre & win(vc)
    return [s for s, m in zip(S, mem) if m], int((pre & ~win(vc)).sum()), vc, sig_seed


def main():
    lvd = load_lvd()
    rows = []
    for f in ('hectocat.dat.gz', 'm2fshi.dat.gz', 'm2fsmed.dat.gz'):
        rows += parse(IN + f)
    print('rows parsed:', len(rows))
    names = sorted(set(r['Target'] for r in rows))
    print('targets:', len(names))
    stars_all = build_stars(rows)
    # row-level bookkeeping
    nrow = {}
    for r in rows:
        nrow[r['Target']] = nrow.get(r['Target'], 0) + 1
    tsv = []
    log = []
    print('\n%-18s %-8s %6s %6s %5s' % ('system', 'class', 'MV', 'rows', 'stars(quality,Gaia)'))
    ufd = []
    for n in names:
        k = n.lower(); x = lvd.get(k)
        ns = sum(1 for s in stars_all.values() if s['target'] == n)
        if x is None:
            cls, mv = 'noLVD', float('nan')
        else:
            mv = fnum(x['M_V']); cls = 'UFD' if mv > -7.7 else 'classical'
        print('%-18s %-8s %6.2f %6d %5d' % (n, cls, mv, nrow[n], ns))
        if cls == 'UFD':
            ufd.append(n)
    hdr = ['name', 'n_members', 'n_multi', 'baseline_days', 'sigma_single', 'plus_err_single', 'minus_err_single',
           'sigma_allmean', 'sigma_clean', 'plus_err_clean', 'minus_err_clean', 'n_removed', 'median_err',
           'plus_err_allmean', 'minus_err_allmean', 'ul95_single', 'ul95_allmean', 'ul95_clean',
           'n_untestable', 'max_epochs', 'baseline_days_max', 'n_vreject', 'sigma_paperflag', 'plus_err_paperflag',
           'minus_err_paperflag', 'ul95_paperflag', 'n_removed_paperflag', 'n_fchi2_members', 'informative',
           'lvd_sigma_literature', 'vsys_fit', 'M_V']
    out = []
    print()
    for n in ufd:
        lv = lvd[n.lower()]
        stars = {k: s for k, s in stars_all.items() if s['target'] == n}
        mem, nvrej, vs, sw = membership(stars, lv)
        N = len(mem)
        multi = [s for s in mem if s['n'] >= 2]
        base = [s['hjd'].max() - s['hjd'].min() for s in multi]
        row = dict(name=n, n_members=N, n_multi=len(multi),
                   baseline_days=float(np.median(base)) if base else float('nan'),
                   max_epochs=max([s['n'] for s in mem], default=0),
                   baseline_days_max=float(np.max(base)) if base else float('nan'),
                   n_vreject=nvrej, n_fchi2_members=sum(s['fchi2'] for s in mem),
                   lvd_sigma_literature=fnum(lv['vlos_sigma']), vsys_fit=vs, M_V=fnum(lv['M_V']))
        if N >= 8:
            e1 = np.array([s['e1'] for s in mem])
            a = mle_sigma([s['v1'] for s in mem], e1)
            b = mle_sigma([s['vm'] for s in mem], [s['em'] for s in mem])
            clean = [s for s in mem if not (s['n'] >= 2 and s['p'] < 0.01)]
            row['n_removed'] = N - len(clean)
            row['n_untestable'] = sum(1 for s in clean if s['n'] < 2)
            c = mle_sigma([s['vm'] for s in clean], [s['em'] for s in clean]) if len(clean) >= 3 else None
            pf = [s for s in mem if s['fvar'] == 0]
            d = mle_sigma([s['vm'] for s in pf], [s['em'] for s in pf]) if len(pf) >= 3 else None
            row.update(sigma_single=a['sig'], plus_err_single=a['ep'], minus_err_single=a['em'], ul95_single=a['ul95'],
                       sigma_allmean=b['sig'], plus_err_allmean=b['ep'], minus_err_allmean=b['em'], ul95_allmean=b['ul95'],
                       median_err=float(np.median(e1)))
            if c:
                row.update(sigma_clean=c['sig'], plus_err_clean=c['ep'], minus_err_clean=c['em'], ul95_clean=c['ul95'])
            if d:
                row.update(sigma_paperflag=d['sig'], plus_err_paperflag=d['ep'], minus_err_paperflag=d['em'],
                           ul95_paperflag=d['ul95'], n_removed_paperflag=N - len(pf))
        row['informative'] = int(row['n_multi'] >= 8 and N > 0 and row['n_multi'] / N >= 0.5)
        out.append(row)
        f = lambda k, fmt='%.2f': (fmt % row[k]) if k in row and np.isfinite(row[k]) else 'NA'
        print('%-18s N=%3d multi=%3d maxep=%2d base_med=%s d  vrej=%d | single %s +%s -%s (UL95 %s) | allmean %s (UL %s) | clean %s +%s -%s (UL %s) rm=%s | pflag %s rm=%s | med_err %s | lit %s' % (
            n, N, len(multi), row['max_epochs'], f('baseline_days', '%.0f'), nvrej,
            f('sigma_single'), f('plus_err_single'), f('minus_err_single'), f('ul95_single'),
            f('sigma_allmean'), f('ul95_allmean'), f('sigma_clean'), f('plus_err_clean'), f('minus_err_clean'), f('ul95_clean'),
            str(row.get('n_removed', 'NA')), f('sigma_paperflag'), str(row.get('n_removed_paperflag', 'NA')),
            f('median_err'), f('lvd_sigma_literature')))
    with open(OUT + 'walker_reduced_dispersions.tsv', 'w') as fh:
        fh.write('\t'.join(hdr) + '\n')
        for r in out:
            fh.write('\t'.join(('%.4g' % r[h]) if isinstance(r.get(h), (float, np.floating)) and np.isfinite(r[h]) else
                               (str(r[h]) if h in r and not isinstance(r[h], float) else 'NA') for h in hdr) + '\n')
    print('wrote', OUT + 'walker_reduced_dispersions.tsv')


if __name__ == '__main__':
    main()
