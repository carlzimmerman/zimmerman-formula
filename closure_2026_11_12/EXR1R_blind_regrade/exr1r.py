#!/usr/bin/env python3
"""EXR1R: blind re-grade of EXR1 (wide-lens X-ray cusp), written from the frozen texts only.

Env EXR1R_MUTATE in {'', inject, shift, newton, a1inject}: twins write exr1r_MUTATE_<name>.{out,json} and exit 1
when the mutation shows its frozen effect (3 if it does not bite). Offline: reads the raw caches only; any position
missing from the caches is listed in _external_data/exr1r_erass1/missing_*.json and the run stops (exit 2).
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import glob
import hashlib
import html as htmlmod
import json
import os
import re
import sys
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exr1r_lib import *  # noqa: E402,F401,F403
from exr1r_lib import _band_sum, _cumint_pl  # noqa: E402
from scipy.spatial import cKDTree  # noqa: E402

warnings.filterwarnings('ignore', message='.*encountered in matmul')
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get('EXR1R_MUTATE', '')
TAG = 'exr1r' + (f'_MUTATE_{MUT}' if MUT else '')
FETCH = os.path.join(EXT, 'exr1_erass1', 'fetch')
LIVE = os.path.join(EXT, 'exr1r_erass1')
LOG = []


def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------ raw caches
class ULCache:
    def __init__(self):
        recs = []
        files = sorted(glob.glob(os.path.join(FETCH, 'ul', '*.json'))) + \
            sorted(glob.glob(os.path.join(LIVE, 'ul_live_*.json')))
        for f in files:
            d = json.load(open(f))
            recs += d['limits']
        self.recs = recs
        ra = np.array([r['ra'] for r in recs], float)
        dec = np.array([r['dec'] for r in recs], float)
        self.tree = cKDTree(unitvec(ra, dec))
        self.nfiles = len(files)

    def lookup(self, ra, dec, tol_arcsec=1.0):
        ra, dec = np.atleast_1d(ra), np.atleast_1d(dec)
        dist, idx = self.tree.query(unitvec(ra, dec))
        found = dist < tol_arcsec * ARCSEC
        out = {k: np.full(len(ra), np.nan) for k in ('C', 'B', 'T', 'ULB', 'BSM')}
        out['desky'] = np.zeros(len(ra), bool)
        out['found'] = found
        for i in np.where(found)[0]:
            r = self.recs[idx[i]]
            out['desky'][i] = bool(r.get('de_sky', False))
            if out['desky'][i] and 'Count' in r:
                out['C'][i], out['B'][i], out['T'][i] = r['Count'], r['Bkg_counts'], r['Exposure']
                out['ULB'][i], out['BSM'][i] = r['UL_B'], r['Bkg_SourceMap']
        out['valid'] = out['desky'] & (np.nan_to_num(out['T']) > 0)
        return out


def load_nh():
    pos, val = [], []
    for f in sorted(glob.glob(os.path.join(FETCH, 'nh', '*.html'))) + \
            sorted(glob.glob(os.path.join(LIVE, 'nh_live_*.html'))):
        t = htmlmod.unescape(open(f, errors='replace').read())
        blocks = re.split(r'Input Equatorial coordinates:', t)[1:]
        for b in blocks:
            m = re.search(r'\[\s*([-\d.]+)\D+?,\s*([-\d.]+)', b)
            w = re.search(r'Weighted average nH \(cm\*\*-2\)\s+([\d.Ee+-]+)', b)
            if m and w:
                pos.append((float(m.group(1)), float(m.group(2))))
                val.append(float(w.group(1)))
    pos = np.array(pos)
    tree = cKDTree(unitvec(pos[:, 0], pos[:, 1]))

    def get(ra, dec):
        d, i = tree.query(unitvec(np.atleast_1d(ra), np.atleast_1d(dec)))
        v = np.array(val)[i]
        v[d > ARCSEC] = np.nan
        return v
    return get, len(val)


def parse_votable(path):
    t = open(path, errors='replace').read()
    fields = re.findall(r'<FIELD[^>]*?name="([^"]+)"', t)
    rows = []
    for tr in re.findall(r'<TR>(.*?)</TR>', t, flags=re.S):
        cells = re.findall(r'<TD>(.*?)</TD>|<TD/>', tr, flags=re.S)
        rows.append(dict(zip(fields, cells)))
    return rows


def load_cones():
    """All cached cone searches: list of (ra, dec, radius_deg, rows)."""
    man = json.load(open(os.path.join(FETCH, 'MANIFEST.json')))
    live_man = os.path.join(LIVE, 'MANIFEST_live.json')
    entries = [(os.path.join(FETCH, 'scs', e['file']), e['url']) for e in man if e['file'].startswith('scs_')]
    if os.path.exists(live_man):
        entries += [(os.path.join(LIVE, e['file']), e['url']) for e in json.load(open(live_man))
                    if e['file'].startswith('scs_live')]
    cones = []
    for p, url in entries:
        q = dict(re.findall(r'([A-Z]+)=([^&]+)', url))
        rows = parse_votable(p)
        cones.append((float(q['RA']), float(q['DEC']), float(q['SR']), rows))
    return cones


def sources_near(cones, ra, dec, rad_arcsec):
    """Main-catalogue sources within rad of (ra, dec) using a cached cone that covers it; None if none covers."""
    for cra, cdec, sr, rows in cones:
        s = sep_arcsec(cra, cdec, ra, dec)
        if s + rad_arcsec <= sr * 3600 + 0.01:   # centres rounded to 1e-6 deg
            out = []
            for r in rows:
                try:
                    sra, sdec = float(r['ra']), float(r['dec'])
                except (KeyError, ValueError):
                    continue
                if sep_arcsec(sra, sdec, ra, dec) <= rad_arcsec:
                    out.append(float(r.get('ml_flux_1') or 'nan'))
            return out
    return None


# ------------------------------------------------------------------ physics per lens
class Pred:
    """Per-lens G2 gas, temperature and catalogue-equivalent flux."""

    def __init__(self, ap, inst, fref_per_cr):
        self.ap, self.inst, self.k = ap, inst, fref_per_cr
        self._q = {}

    def q(self, key, z, DL, NH):
        """Count-rate response per unit node weight, H+He and metals."""
        if key in self._q:
            return self._q[key]
        Eobs = ECEN / (1 + z)
        v = (1 + z) / (4 * np.pi * (DL * 100) ** 2) * np.exp(-sigma_mm(Eobs) * NH) * self.inst.eff_fine(Eobs)
        res = (self.ap.hhe @ v, self.ap.met @ v)
        self._q[key] = res
        return res

    def node_w(self, L, A, a0, r_in, r_out, kT_scale=1.0, prof=None, nsh=400):
        if A <= 0 or r_out <= r_in:
            return np.zeros(len(self.ap.kT))
        rg, kTg = prof if prof is not None else L.kT_profile(A, a0)
        lr = np.linspace(np.log(r_in), np.log(r_out), nsh)
        r = np.exp(lr)
        kT = np.interp(lr, np.log(rg), kTg) / kT_scale
        ne_nh = XH * (A / r ** 2) ** 2 / (MU_E * MP ** 2) * 1e-12      # cm^-6
        f = ne_nh * 4 * np.pi * (r * 100) ** 3                         # per d ln r, cm^-3
        wt = np.full(nsh, lr[1] - lr[0])
        wt[0] = wt[-1] = 0.5 * (lr[1] - lr[0])
        return self.ap.node_weights(kT, f * wt)

    def fcat(self, W, Z, q):
        return (W @ q[0] + Z * (W @ q[1])) * self.k


def shell_em_newton_check(P):
    """K5: Newtonian r^-2 body at constant Lambda: total emission measure from Pred.node_w (the shell integrator
    used for every prediction) against 4 pi n0^2 r0^4 (1/r_in - 1/r_t) (n_H/n_e)."""
    A = 1e-3  # kg/m
    out = []
    for r_in, r_t in ((10 * KPC, 60 * KPC), (KPC, 300 * KPC), (20 * KPC, 300 * KPC)):
        rg = np.geomspace(0.01 * KPC, 300 * KPC, 50)
        prof = (rg, np.full(len(rg), 1.0))
        num = P.node_w(None, A, 0.0, r_in, r_t, prof=prof).sum()
        n0r02 = A / (MU_E * MP) * 1e-6 * 1e4   # n0 r0^2 in cm^-1
        ana = 4 * np.pi * n0r02 ** 2 * (1 / (r_in * 100) - 1 / (r_t * 100)) * (XH * MU_E)
        out.append(num / ana - 1)
    return max(out, key=abs)


def projection_check():
    """EUC1-style K1 on my projection: point mass and SIS through Lens nodes (a0 -> 0)."""
    d = dict(id='x', grade='A', ra=0, dec=0, z=0.5, logm=11.5, thE=2.0, thR=1.0, n=4.0)
    L = Lens(d)
    M = 1e41
    pm = L.RE ** 2 / G * np.sum(L._w * G * M / L._r ** 2) / M - 1
    v2 = (3e5) ** 2
    sis = L.RE ** 2 / G * np.sum(L._w * v2 / L._r) / (np.pi * L.RE * v2 / (2 * G)) - 1
    trunc = -2 * L.RE / (np.pi * RMAX_KPC * KPC)
    return pm, sis, trunc


# ------------------------------------------------------------------ statistics
def boot_sd(x, rng_seed=SEED, nb=2000):
    rng = np.random.default_rng(rng_seed)
    x = np.asarray(x)
    idx = rng.integers(0, len(x), (nb, len(x)))
    return float(np.std(x[idx].mean(axis=1), ddof=1))


def boot_ci(x, rng_seed=SEED, nb=2000):
    rng = np.random.default_rng(rng_seed)
    x = np.asarray(x)
    idx = rng.integers(0, len(x), (nb, len(x)))
    m = x[idx].mean(axis=1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def word(meas, sig, pmin):
    if pmin < 3 * sig:
        return 'NO POWER'
    if meas + 2 * sig < pmin:
        return 'EXCLUDED'
    return 'ALLOWED'


def clip(x):
    return np.minimum(x, FCLIP)


# ------------------------------------------------------------------ main
def main():
    res = {'lane': 'EXR1R', 'mutate': MUT, 'kappa': '1/2 FITTED'}
    say('EXR1R blind re-grade of EXR1. kappa = 1/2 FITTED; not theory closed. mutate =', MUT or 'none')
    base = os.path.join(EXT, 'euclid_dr1_eclipse')
    hk = sha256(os.path.join(base, 'eclipse_dr1_catalogue_key_v20261103.csv'))
    ho = sha256(os.path.join(base, 'ECLIPSE_object_catalogue.csv'))
    hc = sha256(os.path.join(ROOT, 'real_research', 'data', 'erass1cl_primary_v3.2.fits'))
    okhash = hk.startswith('65338917534c9c76') and ho.startswith('8247a4d5f23513b8')
    say('sha256 key', hk[:16], 'object', ho[:16], 'frozen hashes match' if okhash else 'HASH MISMATCH')
    say('sha256 erass1cl_primary_v3.2.fits', hc)
    res['sha256'] = {'key': hk, 'object': ho, 'clusters': hc}

    S, cnt = load_sample()
    W = [d for d in S if d['thE'] >= 1.7]
    say('sample S', len(S), 'W', len(W), 'cuts', cnt)
    res['N_S'], res['N_W'] = len(S), len(W)

    ul = ULCache()
    say('upper-limit records', len(ul.recs), 'from', ul.nfiles, 'files')
    nh_get, n_nh = load_nh()
    cones = load_cones()
    say('N_HI records', n_nh, 'cones', len(cones))

    # ---- positions
    dz = 0.5 if MUT == 'shift' else 0.0
    sra = np.array([d['ra'] for d in S])
    sdec = np.array([d['dec'] for d in S])
    if MUT == 'shift':
        sra, sdec = offset_pos(sra, sdec, 0.0, dz)
    U = ul.lookup(sra, sdec)
    iW = np.array([i for i, d in enumerate(S) if d['thE'] >= 1.7])
    PAS = np.arange(8) * 45.0
    wra = np.array([S[i]['ra'] for i in iW])
    wdec = np.array([S[i]['dec'] for i in iW])
    shp = [offset_pos(wra, wdec, pa, 0.5) for pa in PAS]
    SH = [ul.lookup(r, d) for r, d in shp]

    # clusters
    from astropy.io import fits
    cl = fits.open(os.path.join(ROOT, 'real_research', 'data', 'erass1cl_primary_v3.2.fits'))[1].data
    zc = np.array(cl['BEST_Z'], float)
    m500 = np.array(cl['M500'], float) * 1e13
    selc = (m500 >= 2e14) & (zc >= 0.1) & (zc <= 0.6) & np.isfinite(cl['RA']) & np.isfinite(cl['DEC'])
    cra, cdec = np.array(cl['RA'], float)[selc], np.array(cl['DEC'], float)[selc]
    cdet = np.array(cl['DETUID'])[selc]
    if MUT == 'shift':
        cra, cdec = offset_pos(cra, cdec, 0.0, dz)
    CU = ul.lookup(cra, cdec)
    say('positive-control clusters (M500 >= 2e14, 0.1 <= z <= 0.6):', int(selc.sum()))

    missing = []
    for lab, ra_, de_, look in (('S', sra, sdec, U), ('CL', cra, cdec, CU)) + tuple(
            (f'SH{k}', shp[k][0], shp[k][1], SH[k]) for k in range(8)):
        for j in np.where(~look['found'])[0]:
            missing.append({'set': lab, 'ra': round(float(ra_[j]), 7), 'dec': round(float(de_[j]), 7)})
    if MUT != 'shift' and missing:
        json.dump(missing, open(os.path.join(LIVE, 'missing_ul.json'), 'w'))
        say('MISSING upper-limit positions:', len(missing), '-> missing_ul.json; fetch and re-run')
        sys.exit(2)
    if MUT == 'shift':
        say('shift twin: positions not cached (left out):', len(missing))

    # ---- tested set T
    validW = U['valid'][iW]
    T = iW[validW]
    say('tested set T (W, de_sky, T > 0):', len(T), ' W in de_sky:', int(U['desky'][iW].sum()))
    res['N_T'] = int(len(T))
    meas_raw = (U['C'] - U['B']) / (0.75 * U['T'] * ECF)       # all S positions

    # ---- instrument and reference
    inst = Instrument()
    cr_ref, f_ref = powerlaw_ref(inst)
    say(f'reference PL (Gamma 2, NH 3e20): absolute ECF with the TM0 ARF = {cr_ref / f_ref:.4e} cm^2/erg '
        f'(catalogue 1.074e12; only the shape is used)')
    res['abs_ecf_tm0'] = cr_ref / f_ref
    ap = Apec(os.path.join(LIVE, 'apec_fine_table.npz'))
    P = Pred(ap, inst, f_ref / cr_ref)

    checks = {}
    # K1
    lb = lambda kT, Z, e1=0.001, e2=20.0: ap.band_energy(ap.node_weights(kT, 1.0), Z, e1, e2)
    k1a, k1b = lb(1.0, 0.0), lb(0.12, 1.0) / lb(0.12, 0.0)
    checks['K1'] = bool(abs(k1a / 8.917e-24 - 1) < 0.02 and abs(k1b / 30.1 - 1) < 0.05)
    say(f'K1 APEC reader: Lbol(1 keV, Z=0) = {k1a:.4e} (8.917e-24, 2 %); ratio(0.12 keV) = {k1b:.3f} (30.1, 5 %) '
        f'-> {"PASS" if checks["K1"] else "FAIL"}')
    res['K1'] = {'Lbol_1keV_Z0': k1a, 'ratio_012': k1b}
    # K2
    bands = [(0.2, 0.5, 9.217e11), (0.5, 1.0, 1.359e12), (1.0, 2.0, 1.014e12)]
    e024 = cr_ref / f_ref
    k2 = []
    for b1, b2, ecat in bands:
        c_, f_ = powerlaw_ref(inst, b1=b1, b2=b2)
        k2.append(((c_ / f_) / e024) / (ecat / 1.074e12))
    checks['K2'] = bool(all(abs(x - 1) < 0.08 for x in k2))
    say('K2 band ECF ratios (mine/catalogue):', ', '.join(f'{x:.4f}' for x in k2), '->',
        'PASS' if checks['K2'] else 'FAIL')
    res['K2'] = k2
    # K3
    vS = U['valid']
    ulb = kbn_ul(U['C'][vS], U['B'][vS]) / (0.75 * U['T'][vS] * ECF)
    rr = ulb / U['ULB'][vS]
    k3frac = float(np.mean(np.abs(rr - 1) < 0.02))
    checks['K3'] = bool(k3frac >= 0.99)
    say(f'K3 upper limits: KBN 99.87 % / UL_B within 2 % at {k3frac:.4f} of {int(vS.sum())} valid S positions '
        f'(median ratio {np.median(rr):.5f}) -> {"PASS" if checks["K3"] else "FAIL"}')
    res['K3'] = {'frac': k3frac, 'n': int(vS.sum()), 'median_ratio': float(np.median(rr))}
    # K5
    k5 = shell_em_newton_check(P)
    checks['K5'] = bool(abs(k5) < 1e-4)
    say(f'K5 luminosity integral (my shell integrator): worst relative error {k5:.2e} -> '
        f'{"PASS" if checks["K5"] else "FAIL"}')
    res['K5'] = k5
    pm, sis, tr = projection_check()
    say(f'projection self-check (EUC1 K1 form): point mass {pm:.2e} (1e-6); SIS {sis:.2e} '
        f'(truncation at 1e6 kpc predicts {tr:.2e}; 1e-4)')
    res['projection_check'] = {'point_mass': pm, 'sis': sis, 'sis_truncation_expected': tr}

    # K4 groups
    kt = np.array(cl['KT'], float)
    ktl, kth = np.array(cl['KT_L'], float), np.array(cl['KT_H'], float)
    # the catalogue writes -1 where kT is not measured; only measured kT (all three > 0) can qualify
    k4sel = (kth - ktl < 0.3 * kt) & (zc > 0.05) & (kt > 0) & (ktl > 0) & (kth > 0)
    g_ra, g_dec = np.array(cl['RA'], float)[k4sel], np.array(cl['DEC'], float)[k4sel]
    g_nh = nh_get(g_ra, g_dec)
    say('K4 groups:', int(k4sel.sum()), ' N_HI found for', int(np.isfinite(g_nh).sum()))
    gz, gkt = zc[k4sel], kt[k4sel]
    gcr, gf, gl = (np.array(cl[c], float)[k4sel] for c in ('CR500', 'F500', 'L500'))
    gmg, gr5, glb = (np.array(cl[c], float)[k4sel] for c in ('MGAS500', 'R500', 'Lbol500'))
    ra_, rb_, rc_, rd_ = [], [], [], []
    for j in range(len(gz)):
        Wn = ap.node_weights(gkt[j], 1.0)
        s = ap.spectrum(Wn, 0.3)
        DL = float(LCDM70.DL(gz[j]))
        Eobs = ECEN / (1 + gz[j])
        absb = np.exp(-sigma_mm(Eobs) * g_nh[j])
        ph = s * (1 + gz[j]) / (4 * np.pi * (DL * 100) ** 2) * absb
        cr = np.sum(ph * inst.eff_fine(Eobs))
        fabs = _band_sum(ph * Eobs * KEV / ERG, 0.2, 2.3, EDGES / (1 + gz[j]))
        lrest = _band_sum(s * ECEN * KEV / ERG, 0.2, 2.3)
        pred_a = ECF * (cr * f_ref / cr_ref) / fabs
        ra_.append((gcr[j] / (gf[j] * 1e-14)) / pred_a)
        pred_b = fabs * 4 * np.pi * (DL * 100) ** 2 / lrest
        rb_.append((gf[j] * 1e-14 * 4 * np.pi * (DL * 100) ** 2 / (gl[j] * 1e42)) / pred_b)
        M = gmg[j] * 1e11 * MSUN * 1e3
        V = 4 / 3 * np.pi * (gr5[j] * KPC * 100) ** 3
        lmin = lrest * XH * M ** 2 / (MU_E * (MP * 1e3) ** 2 * V)
        rc_.append(gl[j] * 1e42 / lmin)
        lbol = _band_sum(s * ECEN * KEV / ERG, 0.01, 60.0)
        rd_.append((glb[j] / gl[j]) / (lbol / lrest))
    k4a, k4b, k4c, k4d = (float(np.nanmedian(x)) for x in (ra_, rb_, rc_, rd_))
    checks['K4'] = bool(abs(k4a - 1) <= 0.10 and abs(k4b - 1) <= 0.10 and 1 <= k4c <= 30)
    say(f'K4 known answers (39 groups): (a) CR/F ratio median {k4a:.4f}; (b) K-correction ratio median {k4b:.4f}; '
        f'(c) L500/L_min median {k4c:.3f} -> {"PASS" if checks["K4"] else "FAIL"}')
    say(f'   own known answer KA1 (not frozen): catalogue Lbol500/L500 over my APEC Lbol/L_band (Z 0.3) median '
        f'{k4d:.4f}')
    res['K4'] = {'a': k4a, 'b': k4b, 'c': k4c, 'KA1_bol_over_band': k4d, 'N': int(len(gz))}

    # ---- own known answers (independent of EXR1)
    from astropy.io import fits as _f
    Co = _f.open(os.path.join(APEC_DIR, 'apec_v3.1.3_coco.fits'), memmap=True)
    i8 = int(np.argmin(np.abs(np.log(ap.kT / (8.617333262e-8 * 1e8)))))
    row = [r for r in Co[i8 + 2].data if int(r['Z']) == 1 and int(r['rmJ']) == 0][0]
    x = np.array(row['E_Cont'][:int(row['N_Cont'])], float)
    y = np.array(row['Continuum'][:int(row['N_Cont'])], float)
    lff = _cumint_pl(x, x * y, np.array([x[-1]]))[0] * KEV / ERG
    Tk = ap.kT[i8] / 8.617333262e-8
    gff = lff / (1.42e-27 * np.sqrt(Tk) * 1.0)
    # AG89 H abundance 1; table carries abundances: per n_e n_H, H only, Z=1
    say(f'KA2 pure-hydrogen free-free at T = {Tk:.3e} K: Lambda = {lff:.4e} erg cm^3/s, implied mean Gaunt factor '
        f'{gff:.3f} (Rybicki-Lightman 1.42e-27 T^1/2 g; expected 1.1-1.5)')
    say(f'KA3 MM83: sigma(1 keV) = {sigma_mm(1.0):.4e} cm^2 (2.42e-22); sigma(0.25 keV) = {sigma_mm(0.25):.4e}')
    res['KA'] = {'gaunt_ff_1e8K': gff, 'sigma_1keV': float(sigma_mm(1.0))}

    # ---- K7 positive control
    vC = CU['valid']
    fC = clip((CU['C'][vC] - CU['B'][vC]) / (0.75 * CU['T'][vC] * ECF))
    k7sig = boot_sd(fC)
    k7snr = float(fC.mean() / k7sig)
    order = np.argsort(cdet[vC])
    vra, vdec = cra[vC][order], cdec[vC][order]
    pick = np.random.default_rng(SEED).choice(len(vra), 60, replace=False)
    rec, miss_c = [], []
    for j in pick:
        s_ = sources_near(cones, vra[j], vdec[j], 60.0)
        if s_ is None:
            miss_c.append({'ra': round(float(vra[j]), 6), 'dec': round(float(vdec[j]), 6), 'sr': 0.016667})
        else:
            rec.append(len(s_) > 0)
    if miss_c:
        json.dump(miss_c, open(os.path.join(LIVE, f'missing_scs{"_shift" if MUT == "shift" else ""}.json'), 'w'))
        say('MISSING cluster cones:', len(miss_c), '-> missing_scs json; fetch and re-run')
        sys.exit(2)
    k7rec = float(np.mean(rec))
    checks['K7'] = bool(k7snr >= 5 and k7rec >= 0.90)
    say(f'K7 positive control: {int(vC.sum())} valid clusters, stack {fC.mean():.4e} +- {k7sig:.3e} '
        f'({k7snr:.1f} sigma); recovery {sum(rec)} of 60 within 60" -> {"PASS" if checks["K7"] else "FAIL"}')
    res['K7'] = {'N': int(vC.sum()), 'stack': float(fC.mean()), 'sigma': k7sig, 'snr': k7snr,
                 'recovered': int(sum(rec))}
    if MUT == 'shift':
        bite = not checks['K7']
        say('TWIN shift: K7 must fail ->', 'BITES' if bite else 'DOES NOT BITE')
        res['twin_bites'] = bite
        finish(res, 1 if bite else 3)

    # ---- measurement
    fT = clip(meas_raw[T])
    sh_f = np.array([clip((SH[k]['C'] - SH[k]['B']) / (0.75 * SH[k]['T'] * ECF)) for k in range(8)])  # (8, NW)
    sh_v = np.array([SH[k]['valid'] for k in range(8)])
    posT = np.where(validW)[0]   # indices within W for T

    # ---- predictions
    nhT = nh_get(np.array([S[i]['ra'] for i in T]), np.array([S[i]['dec'] for i in T]))
    say('N_HI found for', int(np.isfinite(nhT).sum()), 'of', len(T), 'tested lenses; median N_HI', np.nanmedian(nhT))
    if not np.all(np.isfinite(nhT)):
        miss = [{'ra': S[i]['ra'], 'dec': S[i]['dec']} for i, v in zip(T, nhT) if not np.isfinite(v)]
        json.dump(miss, open(os.path.join(LIVE, 'missing_nh.json'), 'w'))
        say('MISSING N_HI -> missing_nh.json')
        sys.exit(2)

    a0s = {k: (1e-30 if MUT == 'newton' else v) for k, v in A0.items()}
    lens_rows = {}
    gasW = {}
    for foot, a0 in a0s.items():
        for setting, (bs, zsf) in {'primary': (0.10, None), 'bstar0': (0.0, None),
                                   'central': (0.10, 'central')}.items():
            out = []
            for i in iW:
                d = S[i]
                zs = 1100.0 if zsf is None else max(2.0, d['z'] + 0.5)
                L = Lens(d, bstar=bs, zs=zs)
                A = L.solve_A(a0)
                out.append((L, A))
            gasW[(foot, setting)] = out
        say(f'gas solved for W, footing {foot}')

    def predict(foot, setting='primary', Z=0.1, nhf=2.0, mode='ap', rin='RE', kT_scale=1.0, subset=None):
        idx = posT if subset is None else subset
        pr = np.zeros(len(idx))
        for m, jw in enumerate(idx):
            L, A = gasW[(foot, setting)][jw]
            if A <= 0:
                continue
            i = iW[jw]
            nH = nh_get(S[i]['ra'], S[i]['dec'])[0] * nhf
            q = P.q((i, nhf), L.z, L.DL * 1.0, nH)
            r_in = {'RE': L.RE, 'RE2': 0.5 * L.RE, '1kpc': KPC}[rin]
            if mode == 'ap':
                r_out, fac = min(10 * ARCSEC * L.DA, L.rt), 2.0 / 3.0
            else:
                r_out, fac = L.rt, 1.0
            prof = getattr(L, '_prof', None)
            if prof is None or prof[0] != (foot, setting, A):
                L._prof = ((foot, setting, A), L.kT_profile(A, a0s[foot]))
            Wn = P.node_w(L, A, a0s[foot], r_in, r_out, kT_scale, prof=L._prof[1])
            pr[m] = fac * P.fcat(Wn, Z, q)
        return clip(pr)

    # null stacks (frozen)
    def nulls_frozen(sel_w):
        st = []
        for k in range(8):
            v = sh_v[k, sel_w]
            st.append(float(sh_f[k, sel_w][v].mean()) if v.any() else np.nan)
        return np.array(st)

    def grade(values, nulls, pm, about_mean=False):
        sig_b = boot_sd(values)
        nn = nulls - (np.nanmean(nulls) if about_mean else 0.0)
        sig_n = float(np.sqrt(np.nanmean(nn ** 2)))
        sig = max(sig_b, sig_n)
        meas = float(np.mean(values))
        return dict(meas=meas, sigma=sig, sigma_boot=sig_b, sigma_null=sig_n, pred_min=float(pm),
                    word=word(meas, sig, pm), nulls=[float(x) for x in nulls])

    def k8(g, nulls, scatter_only=False):
        sig = g['sigma']
        mn = float(np.nanmean(nulls))
        ok_mean = abs(mn) <= 0.75 * sig
        dev = nulls - (mn if scatter_only else 0.0)
        ok_sc = bool(np.all(np.abs(dev) <= 3.5 * sig))
        return (ok_sc if scatter_only else (ok_mean and ok_sc)), mn

    # A1 construction
    a1_keep, a1_val, a1_nullmat = [], [], []
    for m, jw in enumerate(posT):
        v = sh_v[:, jw]
        if v.sum() < 6:
            continue
        f8 = sh_f[:, jw]
        a1_keep.append(m)
        a1_val.append(fT[m] - f8[v].mean())
        row = np.full(8, np.nan)
        for k in range(8):
            if v[k]:
                oth = v.copy()
                oth[k] = False
                row[k] = f8[k] - f8[oth].mean()
        a1_nullmat.append(row)
    a1_keep = np.array(a1_keep)
    a1_val = np.array(a1_val)
    a1_nullmat = np.array(a1_nullmat)
    say(f'A1 set: {len(a1_keep)} of {len(T)} tested lenses keep >= 6 valid shifted positions')

    def a1_nulls(rows):
        return np.array([np.nanmean(a1_nullmat[rows, k]) for k in range(8)])

    gradeA = np.array([S[i]['grade'] == 'A' for i in T])
    zlow = np.array([S[i]['z'] <= 0.6 for i in T])
    res['footings'] = {}
    lane = {}
    predP = {}
    for foot in a0s:
        pr = predict(foot)
        predP[foot] = pr
        if MUT == 'inject':
            injected = clip(meas_raw[T] + predict('canonical'))
            values = injected
        else:
            values = fT
        nf = nulls_frozen(posT)
        g = grade(values, nf, pr.mean())
        ok8, mn8 = k8(g, np.array(g['nulls']))
        g['K8'] = ok8
        g['K8_null_mean'] = mn8
        # brackets
        br = {}
        for name, kw in {'Z=0': dict(Z=0.0), 'Z=0.3': dict(Z=0.3), 'NH=1xNHI': dict(nhf=1.0),
                         'point source': dict(mode='pt'), 'r_in=RE/2': dict(rin='RE2'),
                         'r_in=1kpc': dict(rin='1kpc')}.items():
            pb = predict(foot, **kw)
            br[name] = dict(pred_min=float(pb.mean()), word=word(g['meas'], g['sigma'], pb.mean()))
        for name, msk in (('grade A only', gradeA), ('z_l<=0.6 only', zlow)):
            gs = grade(values[msk], nulls_frozen(posT[msk]), pr[msk].mean())
            br[name] = dict(pred_min=gs['pred_min'], word=gs['word'], N=int(msk.sum()), meas=gs['meas'],
                            sigma=gs['sigma'])
        rep = {}
        for name, kw in {'Z=1.0': dict(Z=1.0), 'central source': dict(setting='central'),
                         'b*=0': dict(setting='bstar0')}.items():
            pb = predict(foot, **kw)
            rep[name] = dict(pred_min=float(pb.mean()), word=word(g['meas'], g['sigma'], pb.mean()))
        moved = [k for k, v in br.items() if v['word'] != g['word']]
        thr = g['meas'] + 2 * g['sigma']
        fM = float(np.sqrt(thr / g['pred_min'])) if thr > 0 and g['pred_min'] > 0 else float('nan')
        fTv = float('nan')
        if g['pred_min'] > thr:
            for fs in np.geomspace(1.0, 3000.0, 400)[1:]:
                if predict(foot, kT_scale=fs).mean() <= thr:
                    fTv = float(fs)
                    break
        g.update(brackets=br, reported=rep, tag_moves=moved, f_M=fM, f_T=fTv)
        # R reading (frozen stack, nulls about own mean, scatter half of K8)
        gR = grade(values, nf, pr.mean(), about_mean=True)
        gR['K8_scatter'] = k8(gR, np.array(gR['nulls']), scatter_only=True)[0]
        gR['K8_scatter_vs_zero'] = bool(np.all(np.abs(np.array(gR['nulls'])) <= 3.5 * gR['sigma']))
        # A1 reading
        a1v = a1_val.copy()
        if MUT in ('a1inject',):
            pc = predict('canonical')
            a1v = np.array([clip(meas_raw[T][m] + pc[m]) - sh_f[sh_v[:, posT[m]], posT[m]].mean()
                            for m in a1_keep])
        gA = grade(a1v, a1_nulls(np.arange(len(a1_keep))), pr[a1_keep].mean())
        gA['K8'], gA['K8_null_mean'] = k8(gA, np.array(gA['nulls']))
        brA = {}
        for name, kw in {'Z=0': dict(Z=0.0), 'Z=0.3': dict(Z=0.3), 'NH=1xNHI': dict(nhf=1.0),
                         'point source': dict(mode='pt'), 'r_in=RE/2': dict(rin='RE2'),
                         'r_in=1kpc': dict(rin='1kpc')}.items():
            pb = predict(foot, **kw)[a1_keep]
            brA[name] = dict(pred_min=float(pb.mean()), word=word(gA['meas'], gA['sigma'], pb.mean()))
        for name, msk in (('grade A only', gradeA[a1_keep]), ('z_l<=0.6 only', zlow[a1_keep])):
            rows = np.where(msk)[0]
            gs = grade(a1v[rows], a1_nulls(rows), pr[a1_keep][rows].mean())
            brA[name] = dict(pred_min=gs['pred_min'], word=gs['word'], N=int(len(rows)), meas=gs['meas'],
                             sigma=gs['sigma'])
        gA['brackets'] = brA
        gA['tag_moves'] = [k for k, v in brA.items() if v['word'] != gA['word']]
        thrA = gA['meas'] + 2 * gA['sigma']
        gA['f_M'] = float(np.sqrt(thrA / gA['pred_min'])) if thrA > 0 and gA['pred_min'] > 0 else float('nan')
        res['footings'][foot] = {'frozen': g, 'R': gR, 'A1': gA}
        lane[foot] = g
        say(f'--- footing {foot}: pred_min {g["pred_min"]:.4e}; measured {g["meas"]:.4e}; sigma {g["sigma"]:.3e} '
            f'(boot {g["sigma_boot"]:.3e}, null rms {g["sigma_null"]:.3e}) -> Part G word {g["word"]}; '
            f'pred_min/sigma {g["pred_min"] / g["sigma"]:.1f}')
        say(f'    nulls: {", ".join(f"{x:.3e}" for x in g["nulls"])}; K8 mean {mn8:.3e} vs 3sigma/4 '
            f'{0.75 * g["sigma"]:.3e} -> {"PASS" if ok8 else "FAIL"}')
        say(f'    brackets: ' + '; '.join(f'{k} {v["pred_min"]:.3e} {v["word"]}' for k, v in br.items()))
        say(f'    reported: ' + '; '.join(f'{k} {v["pred_min"]:.3e} {v["word"]}' for k, v in rep.items()))
        say(f'    tag moves: {moved or "none"}; f_M {fM:.4f}; f_T {fTv:.3g}')
        say(f'    R reading: sigma {gR["sigma"]:.3e} (null rms about own mean {gR["sigma_null"]:.3e}) -> '
            f'{gR["word"]}; K8 scatter {"PASS" if gR["K8_scatter"] else "FAIL"}')
        say(f'    A1 reading: N {len(a1_keep)}, measured {gA["meas"]:.4e}, sigma {gA["sigma"]:.3e} (boot '
            f'{gA["sigma_boot"]:.3e}, null rms {gA["sigma_null"]:.3e}), pred_min {gA["pred_min"]:.4e} -> '
            f'{gA["word"]}; K8 {"PASS" if gA["K8"] else "FAIL"} (null mean {gA["K8_null_mean"]:.3e}); '
            f'tag moves {gA["tag_moves"] or "none"}; f_M {gA["f_M"]:.4f}')
        say(f'    A1 brackets: ' + '; '.join(f'{k} {v["pred_min"]:.3e} {v["word"]}' for k, v in brA.items()))

    # ---- Part C
    ctrl_pool = [i for i, d in enumerate(S) if d['thE'] < 1.0 and U['valid'][i]]
    used = set()
    pairs = []
    for i in sorted(T, key=lambda k: S[k]['id']):
        best, bd = None, np.inf
        for j in ctrl_pool:
            if j in used:
                continue
            dd = ((S[j]['z'] - S[i]['z']) / 0.05) ** 2 + ((S[j]['logm'] - S[i]['logm']) / 0.1) ** 2
            if dd < bd or (dd == bd and S[j]['id'] < S[best]['id']):
                best, bd = j, dd
        used.add(best)
        pairs.append((i, best))
    Dv = np.array([clip(meas_raw[i]) - clip(meas_raw[j]) for i, j in pairs])
    lo, hi = boot_ci(Dv)
    wC = 'WIDE LENSES ARE BRIGHTER IN X-RAYS' if lo > 0 else 'NO EXCESS DETECTED'
    if len(pairs) < 100:
        wC = 'NOT EVALUABLE'
    say(f'Part C: {len(pairs)} pairs, mean D {Dv.mean():.4e}, 95 % [{lo:.4e}, {hi:.4e}] -> {wC}')
    res['partC'] = dict(N=len(pairs), meanD=float(Dv.mean()), lo=lo, hi=hi, word=wC)

    # ---- Part L
    nsrc, fl, chance, cover = [], [], [], 0
    for m, i in enumerate(T):
        s_ = sources_near(cones, S[i]['ra'], S[i]['dec'], 30.0)
        if s_ is None:
            nsrc.append(np.nan)
            continue
        cover += 1
        nsrc.append(len(s_))
        fl += s_
        jw = posT[m]
        for k in range(8):
            s2 = sources_near(cones, shp[k][0][jw], shp[k][1][jw], 30.0)
            if s2 is not None:
                chance.append(len(s2) > 0)
    nsrc = np.array(nsrc)
    ulT = U['ULB'][T]
    empty = 6.6448 / (0.75 * U['T'][T] * ECF)
    resL = dict(cones_covering=cover, lenses_with_source=int(np.nansum(nsrc > 0)),
                chance_rate=float(np.mean(chance)) if chance else None, n_shift_checked=len(chance),
                catalogued_fluxes=sorted([x for x in fl if np.isfinite(x)]))
    for foot in a0s:
        resL[f'ULB_below_pred_{foot}'] = int(np.sum(ulT < predP[foot]))
        resL[f'empty_bound_below_pred_{foot}'] = int(np.sum(empty < predP[foot]))
    say(f'Part L: cones cover {cover} of {len(T)}; lenses with a Main source within 30": '
        f'{resL["lenses_with_source"]}; chance rate at shifted positions {resL["chance_rate"]} '
        f'({len(chance)} positions); UL_B < pred: canonical {resL["ULB_below_pred_canonical"]}, alt '
        f'{resL["ULB_below_pred_alt"]}; empty-aperture bound < pred: canonical '
        f'{resL["empty_bound_below_pred_canonical"]}, alt {resL["empty_bound_below_pred_alt"]}')
    res['partL'] = resL

    # ---- Part D
    resD = {}
    for foot in a0s:
        mg, kre, nre, lall, lre, tc1, tc3 = [], [], [], [], [], [], []
        for jw in posT:
            L, A = gasW[(foot, 'primary')][jw]
            mg.append(L.mgas_total(A) / MSUN)
            if A <= 0:
                continue
            rg, kTg = L._prof[1] if hasattr(L, '_prof') else L.kT_profile(A, a0s[foot])
            kR = float(np.interp(np.log(L.RE), np.log(rg), kTg))
            kre.append(kR)
            ne = A / L.RE ** 2 / (MU_E * MP) * 1e-6
            nre.append(ne)
            nH_ = XH * A / L.RE ** 2 / MP * 1e-6
            ni = A / L.RE ** 2 / (MU_I * MP) * 1e-6
            for Z_, lst in ((0.1, tc1), (0.3, tc3)):
                lam = ap.band_energy(ap.node_weights(kR, 1.0), Z_, 0.001, 20.0)
                lst.append(1.5 * (ne + ni) * kR * KEV / ERG / (ne * nH_ * lam) / 3.156e13)
            for r0, lst in ((KPC, lall), (L.RE, lre)):
                Wn = P.node_w(L, A, a0s[foot], r0, L.rt, prof=L._prof[1])
                lst.append(_band_sum(ap.spectrum(Wn, 0.1) * ECEN * KEV / ERG, 0.2, 2.3))
        resD[foot] = dict(median_Mgas=float(np.median(mg)), median_kT_RE=float(np.median(kre)),
                          median_ne_RE=float(np.median(nre)), median_Lband_all_ge1kpc=float(np.median(lall)),
                          median_Lband_ge_RE=float(np.median(lre)), median_pred=float(np.median(predP[foot])),
                          median_tcool_Myr_Z01=float(np.median(tc1)), median_tcool_Myr_Z03=float(np.median(tc3)),
                          n_needing_gas=int(len(kre)))
        say(f'Part D {foot}: ' + ', '.join(f'{k} {v:.4g}' for k, v in resD[foot].items()))
    DLT = np.array([float(EUCLID.DL(S[i]['z'])) * 100 for i in T])
    resD['stack_mean_luminosity_obsband'] = float(np.mean(fT * 4 * np.pi * DLT ** 2))
    for nm, lo_, hi_ in (('1.3-1.7', 1.3, 1.7), ('1.0-1.3', 1.0, 1.3), ('<1.0', 0.0, 1.0)):
        sel = [i for i, d in enumerate(S) if lo_ <= d['thE'] < hi_ and U['valid'][i]]
        v = clip(meas_raw[sel])
        resD[f'class_{nm}'] = dict(N=len(sel), stack=float(v.mean()), sigma_boot=boot_sd(v))
        say(f'Part D class {nm}": N {len(sel)}, stack {v.mean():.4e} +- {boot_sd(v):.3e}')
    say(f'Part D stack as mean observed-band luminosity: {resD["stack_mean_luminosity_obsband"]:.4e} erg/s')
    res['partD'] = resD

    # ---- per-lens CSV (all W; gas for K6 post-unblinding)
    if not MUT:
        with open(os.path.join(HERE, 'exr1r_per_lens.csv'), 'w') as fh:
            cols = ['id', 'grade', 'ra', 'dec', 'z', 'logm', 'thE', 'n', 'valid', 'C', 'B', 'T', 'f_meas_clipped']
            for foot in a0s:
                cols += [f'Mgas_{foot}', f'kT_RE_{foot}', f'ne_RE_{foot}', f'pred_{foot}']
            fh.write(','.join(cols) + '\n')
            predmap = {foot: dict(zip(posT, predP[foot])) for foot in a0s}
            for jw, i in enumerate(iW):
                d = S[i]
                vals = [d['id'], d['grade'], f"{d['ra']:.7f}", f"{d['dec']:.7f}", f"{d['z']:.4f}", f"{d['logm']:.4f}",
                        f"{d['thE']:.4f}", f"{d['n']:.4f}", str(bool(U['valid'][i])), str(U['C'][i]),
                        f"{U['B'][i]:.6g}", f"{U['T'][i]:.6g}", f"{clip(meas_raw[i]):.6e}"]
                for foot in a0s:
                    L, A = gasW[(foot, 'primary')][jw]
                    if A > 0:
                        rg, kTg = L.kT_profile(A, a0s[foot])
                        kR = float(np.interp(np.log(L.RE), np.log(rg), kTg))
                        ne = A / L.RE ** 2 / (MU_E * MP) * 1e-6
                    else:
                        kR, ne = 0.0, 0.0
                    vals += [f'{L.mgas_total(A) / MSUN:.6e}', f'{kR:.6g}', f'{ne:.6g}',
                             f'{predmap[foot].get(jw, float("nan")):.6e}']
                fh.write(','.join(vals) + '\n')

    # ---- words
    allok = all(checks.values())
    res['checks'] = checks
    res['K6'] = 'deferred: evaluated after commit (needs ESZ1 outputs); blind words conditional on K6'
    words = {}
    for foot in a0s:
        g = res['footings'][foot]['frozen']
        lw = g['word'] if (allok and g['K8'] and len(T) >= 100) else 'NOT EVALUABLE'
        tag = f' [BRACKET-DEPENDENT: {", ".join(g["tag_moves"])}]' if g['tag_moves'] and lw != 'NOT EVALUABLE' else ''
        gA = res['footings'][foot]['A1']
        a1w = gA['word'] if (allok and gA['K8'] and len(a1_keep) >= 100) else 'NOT EVALUABLE'
        tagA = f' [BRACKET-DEPENDENT: {", ".join(gA["tag_moves"])}]' if gA['tag_moves'] and a1w != 'NOT EVALUABLE' \
            else ''
        gR = res['footings'][foot]['R']
        rw = gR['word'] if (allok and gR['K8_scatter'] and len(T) >= 100) else 'NOT EVALUABLE'
        words[foot] = dict(lane=lw + tag, partG=g['word'], A1=a1w + tagA, R=rw)
    pc_frozen = res['partC']['word'] if (allok and all(lane[f]['K8'] for f in a0s)) else 'NOT EVALUABLE'
    pc_a1 = res['partC']['word'] if allok else 'NOT EVALUABLE'
    res['words'] = words
    res['partC_word_frozen'] = pc_frozen
    res['partC_word_A1'] = pc_a1
    say('checks:', ', '.join(f'{k} {"PASS" if v else "FAIL"}' for k, v in checks.items()),
        '| K8 frozen:', ', '.join(f'{f} {"PASS" if lane[f]["K8"] else "FAIL"}' for f in a0s), '| K6 deferred')
    say('WORDS (blind, conditional on K6): frozen', ' / '.join(words[f]['lane'] for f in a0s),
        '| A1 reading', ' / '.join(words[f]['A1'] for f in a0s), '| R reading', ' / '.join(words[f]['R'] for f in a0s),
        '| Part G before checks', ' / '.join(words[f]['partG'] for f in a0s))
    say('Part C: frozen', pc_frozen, '| A1 reading', pc_a1)

    code = 0
    if MUT == 'inject':
        bite = all(res['footings'][f]['frozen']['word'] == 'ALLOWED' for f in a0s)
        say('TWIN inject: Part G word ALLOWED on both footings ->', 'BITES' if bite else 'DOES NOT BITE')
        res['twin_bites'] = bite
        code = 1 if bite else 3
    elif MUT == 'a1inject':
        bite = all(res['footings'][f]['A1']['word'] == 'ALLOWED' for f in a0s)
        say('TWIN a1inject: A1 word ALLOWED on both footings ->', 'BITES' if bite else 'DOES NOT BITE')
        res['twin_bites'] = bite
        code = 1 if bite else 3
    elif MUT == 'newton':
        ref = json.load(open(os.path.join(HERE, 'exr1r_results.json')))
        rise = {f: res['footings'][f]['frozen']['pred_min'] > ref['footings'][f]['frozen']['pred_min'] for f in a0s}
        bite = all(rise.values())
        say('TWIN newton: pred_min rises on both footings', rise, '->', 'BITES' if bite else 'DOES NOT BITE')
        res['twin_bites'] = bite
        code = 1 if bite else 3
    finish(res, code)


def finish(res, code):
    with open(os.path.join(HERE, f'{TAG}_results.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    with open(os.path.join(HERE, f'{TAG}.out'), 'w') as fh:
        fh.write('\n'.join(LOG) + '\n')
    sys.exit(code)


if __name__ == '__main__':
    main()
