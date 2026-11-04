"""A28: per-galaxy fits of the OBSERVED SPARC curves with nuisances (law, NFW, R11b, coreNFW), then the RAR the fits produce.
Per ../FROZEN_A28.md. Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import sys, os, json, time, resource; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from scipy.special import gammainc
from scipy.stats import chi2 as CHI2
src = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read(); exec(src[src.index('def m200k'):src.index('def gal(')])
src = open(os.path.join(HERE, 'recipe18.py'), encoding='utf-8').read(); exec(src[src.index('K11B ='):src.index('def tune(')])
T0 = time.time(); CK = os.path.join(HERE, 'recipe30.json'); GBMIN = 1e-14
# table extras: D, e_D, Inc, e_Inc
TX = {}
for l in open(os.path.join(D, 'SPARC_Lelli2016c.mrt')):
    p = l.split()
    if len(p) >= 17 and p[1].isdigit() and len(l) > 90:
        try: TX[p[0]] = dict(D=float(p[2]), eD=float(p[3]), I=float(p[5]), eI=float(p[6]), L=float(p[7]), Rd=float(p[11]), MHI=float(p[13]), Q=int(p[17]))
        except (ValueError, IndexError): pass
class Raw: pass
RAW = []
for g in GS:
    a = np.loadtxt(os.path.join(D, 'sparc_data', g.n + '_rotmod.dat')); a = a[a[:, 0] > 0]
    vb2 = a[:, 3] * abs(a[:, 3]) + YD * a[:, 4] * abs(a[:, 4]) + YB * a[:, 5] * abs(a[:, 5]); a = a[vb2 > 0]
    assert len(a) == len(g.r)
    w = Raw(); w.n = g.n; w.R = a[:, 0]; w.V = a[:, 1]; w.e = np.maximum(a[:, 2], 1e-3); w.vg2 = a[:, 3] * abs(a[:, 3]); w.vd2 = a[:, 4] * abs(a[:, 4]); w.vB2 = a[:, 5] * abs(a[:, 5])
    w.bul = bool((a[:, 5] > 0).any()); w.t = TX[g.n]; w.N = len(a); RAW.append(w)
NTOT = sum(w.N for w in RAW); print(f'A28: {len(RAW)} galaxies, {NTOT} points, {sum(w.bul for w in RAW)} with bulge', flush=True)
LYD, LYB, SU, SSHMR, SC = np.log10(.5), np.log10(.7), .1, .15, .11
def nuis(w, z):
    zd, zb, zD, zi = z; t = w.t; Yd = 10**(LYD + SU * zd); Yb = 10**(LYB + SU * zb) if w.bul else 0.
    fD = max(1 + t['eD'] / t['D'] * zD, .05); inc = np.clip(t['I'] + t['eI'] * zi, 10, 90); s = np.sin(np.radians(t['I'])) / np.sin(np.radians(inc))
    r = w.R * fD * kpc; vb2 = (w.vg2 + Yd * w.vd2 + Yb * w.vB2) * fD * 1e6; nclip = int((vb2 <= GBMIN * r).sum()); gb = np.maximum(vb2 / r, GBMIN)
    return dict(Yd=Yd, Yb=Yb, fD=fD, r=r, vb2=vb2, gb=gb, V=w.V * s * 1e3, e=w.e * s * 1e3, nclip=nclip)
def halo_nfw(w, q, lM, lc, n=None):
    M, c = 10**lM, 10**lc; Ms = q['Yd'] * w.t['L'] * 1e9 * q['fD']**2; Mb = Ms + 1.33 * w.t['MHI'] * 1e9 * q['fD']**2; fb = min(Mb / M, .5)
    m = (1 - fb) * nfw_m(q['r'], M, c)[0]
    if n is not None: m = m * np.tanh(q['r'] / (1.75 * 1.68 * w.t['Rd'] * q['fD'] * kpc))**n
    return q['gb'] + G * m / q['r']**2, Ms
def gR(w, q):
    g = Gal(); fD = q['fD']; g.r = q['r']; g.gb = q['gb']; g.mb = q['vb2'] * q['r'] / G; g.Ms = q['Yd'] * w.t['L'] * 1e9 * fD**2
    g.Mb = g.Ms + 1.33 * w.t['MHI'] * 1e9 * fD**2; g.Rd = w.t['Rd'] * fD * kpc; return gal3(g, K11B, [])
def model(m, w, x, ssh=SSHMR):
    """returns g_model, q, prior-pull vector (Gaussian terms only)"""
    z = [x[0], x[1] if w.bul else 0., x[2], x[3]]; q = nuis(w, z); pr = [z[0]] + ([z[1]] if w.bul else []) + [z[2], z[3]]
    if m == 'L': gm = law(q['gb'])
    elif m == 'R': gm = gR(w, q)
    else:
        lM, lc = x[4], x[5]; gm, Ms = halo_nfw(w, q, lM, lc, x[6] if m == 'C' else None)
        pr += [(np.log10(Ms) - np.log10(float(smhm(10**lM)))) / ssh, (lc - np.log10(float(cflat(10**lM, 0, 0)))) / SC]
    return gm, q, np.array(pr)
def resid(m, w, x, ssh=SSHMR):
    gm, q, pr = model(m, w, x, ssh); vm = np.sqrt(np.maximum(gm, 0) * q['r']); return np.concatenate([(q['V'] - vm) / q['e'], pr])
def fitgal(m, w, ssh=SSHMR):
    nz = 4; lo = [-5] * nz; hi = [5] * nz
    if not w.bul: lo[1], hi[1] = -1e-6, 1e-6
    starts = []
    if m in 'LR': starts = [[0, 0, 0, 0], [1, 0, 0, 0], [-1, 0, 0, 0]]
    else:
        M0 = np.log10(m200_of(.5 * w.t['L'] * 1e9)); M0 = float(np.clip(M0, 9, 15))
        for dM in (0, .5, -.5):
            lM = M0 + dM; base = [0, 0, 0, 0, lM, np.log10(float(cflat(10**lM, 0, 0)))]
            starts += [base + [.1], base + [.9]] if m == 'C' else [base]
        lo += [8.5, 0.]; hi += [15.5, 2.]
        if m == 'C': lo += [0.]; hi += [1.]
    best = None; lo, hi = np.array(lo, float), np.array(hi, float)
    for s in starts:
        r = least_squares(lambda x: resid(m, w, x, ssh), np.clip(s, lo + 1e-7, hi - 1e-7), bounds=(lo, hi), max_nfev=400, x_scale='jac')
        if best is None or r.cost < best.cost: best = r
    x = best.x; gm, q, pr = model(m, w, x, ssh); vm = np.sqrt(np.maximum(gm, 0) * q['r']); c2d = float((((q['V'] - vm) / q['e'])**2).sum())
    kg = 3 + w.bul + (2 if m in 'NC' else 0) + (1 if m == 'C' else 0); ngs = len(pr)
    return dict(x=x.tolist(), c2d=c2d, c2p=c2d + float((pr**2).sum()), kg=kg, ngs=ngs, pr=pr.tolist(), atb=int((np.abs(np.array(x[:4])[[0, 2, 3] + ([1] if w.bul else [])]) > 5 - 1e-3).sum()), nclip=q['nclip'])
MODELS = [('L', SSHMR), ('N', SSHMR), ('N20', .20), ('R', SSHMR), ('C', SSHMR)]
res = json.load(open(CK)) if os.path.exists(CK) else {}
for tag, ssh in MODELS:
    m = tag[0]; res.setdefault(tag, {})
    for i, w in enumerate(RAW):
        if w.n in res[tag]: continue
        res[tag][w.n] = fitgal(m, w, ssh)
        if (i + 1) % 25 == 0 or i + 1 == len(RAW):
            json.dump(res, open(CK, 'w')); print(f'  {tag}: {i + 1}/{len(RAW)} fitted, {time.time() - T0:.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB', flush=True)
    json.dump(res, open(CK, 'w'))
SUB = [w.n for w in RAW if w.t['Q'] < 3 and w.t['I'] >= 30]
print(f'\nsubset Q<3 and Inc>=30: {len(SUB)} galaxies')
print('\n== Fit quality (chi2_post = data + Gaussian prior pulls; acceptable p >= 0.01 on chi2_post, dof = N_g + n_gauss - k_g)')
print(f'{"model":5s} {"globals":>7s} {"k_total":>7s} {"chi2_data":>10s} {"chi2_post":>10s} {"AIC":>10s} {"BIC":>10s} {"accept":>8s} {"acc(data)":>9s} {"acc sub":>9s} {"med chi2nu":>10s}')
summ = {}
for tag, ssh in MODELS:
    R_ = res[tag]; glob_ = 14 if tag == 'R' else 0
    k = sum(R_[w.n]['kg'] for w in RAW) + glob_; c2d = sum(R_[w.n]['c2d'] for w in RAW); c2p = sum(R_[w.n]['c2p'] for w in RAW)
    acc = {}; accd = 0; nus = []
    for w in RAW:
        f = R_[w.n]; dof = w.N + f['ngs'] - f['kg']; acc[w.n] = CHI2.sf(f['c2p'], dof) >= .01
        accd += CHI2.sf(f['c2d'], max(w.N - f['kg'], 1)) >= .01; nus.append(f['c2d'] / max(w.N - f['kg'], 1))
    aic, bic = c2p + 2 * k, c2p + k * np.log(NTOT); summ[tag] = dict(k=k, c2d=c2d, c2p=c2p, aic=aic, bic=bic, acc=sum(acc.values()))
    print(f'{tag:5s} {glob_:7d} {k:7d} {c2d:10.1f} {c2p:10.1f} {aic:10.1f} {bic:10.1f} {sum(acc.values()):4d}/{len(RAW)} {accd:5d}/{len(RAW)} {sum(acc[n] for n in SUB):5d}/{len(SUB)} {np.median(nus):10.3f}')
    if tag == 'L': print(f'L     with kappa counted as 1 fitted global: k {k + 1}, AIC {aic + 2:.1f}, BIC {bic + np.log(NTOT):.1f}')
print('\n== Prior pulls: fraction |z| > 2 (and at the |z| = 5 bound)')
for tag, ssh in MODELS:
    R_ = res[tag]; Z = {'Yd': [], 'Yb': [], 'D': [], 'Inc': [], 'SHMR': [], 'c': []}; nb = 0; nclip = 0
    for w in RAW:
        f = R_[w.n]; x = f['x']; Z['Yd'].append(x[0]); Z['D'].append(x[2]); Z['Inc'].append(x[3]); nclip += f['nclip']
        if w.bul: Z['Yb'].append(x[1])
        if tag[0] in 'NC': Z['SHMR'].append(f['pr'][-2]); Z['c'].append(f['pr'][-1])
        nb += f['atb']
    nuz = np.abs(np.concatenate([Z[k] for k in ('Yd', 'Yb', 'D', 'Inc')]))
    line = f'{tag:5s} nuisances {np.mean(nuz > 2):.3f} ({len(nuz)}), at bound {nb}; ' + ', '.join(f'{k} {np.mean(np.abs(Z[k]) > 2):.3f}' for k in Z if len(Z[k]))
    if tag[0] in 'NC': line += f'; median z_SHMR {np.median(Z["SHMR"]):+.2f}, z_c {np.median(Z["c"]):+.2f}'
    if tag == 'C': line += f'; median n {np.median([R_[w.n]["x"][6] for w in RAW]):.2f}'
    print(line + f'; clipped g_b points {nclip}')
print('\n== Per galaxy against L: median delta chi2_post, galaxies where the row beats L')
for tag in ('N', 'N20', 'R', 'C'):
    d = np.array([res[tag][w.n]['c2p'] - res['L'][w.n]['c2p'] for w in RAW]); print(f'{tag:5s} - L: median {np.median(d):+.2f}, mean {d.mean():+.2f}, beats L in {(d < 0).sum()}/{len(RAW)}')
print('\n== Reverse question: the RAR each population of fits produces (g_b from its fitted nuisances)')
print(' Ra |log a/A0| <= 0.05; Rs intrinsic scatter about law(a_fit) <= 0.057; Rt rms to tied law <= 0.02 and worst bin <= 0.02')
def rar(gb, gt):
    a = fit_a(gb, gt); s = np.sqrt(((np.log10(gt) - np.log10(law(gb, a)))**2).mean()); d = np.log10(gt) - np.log10(law(gb)); t = np.sqrt((d**2).mean())
    b = np.floor(np.log10(gb) * 2) / 2; bins = [(x, d[b == x].mean()) for x in np.unique(b) if (b == x).sum() >= 50]; wb = max(abs(v) for _, v in bins)
    return a, s, t, wb, d.mean(), bins
for tag, ssh in MODELS:
    GB, GM, GO = [], [], []
    for w in RAW:
        gm, q, _ = model(tag[0], w, np.array(res[tag][w.n]['x']), ssh); GB.append(q['gb']); GM.append(np.maximum(gm, GBMIN)); GO.append(q['V']**2 / q['r'])
    GB, GM, GO = map(np.concatenate, (GB, GM, GO))
    a, s, t, wb, mn, bins = rar(GB, GM); ao, so, to, wbo, mno, _ = rar(GB, GO); la = np.log10(a / A0)
    v = ('' if tag == 'L' else f' [Ra {"PASS" if abs(la) <= .05 else "FAIL"}, Rs {"PASS" if s <= .057 else "FAIL"}, Rt {"PASS" if t <= .02 and wb <= .02 else "FAIL"}]')
    print(f'{tag:5s} model curves: a {a:.3e} ({la:+.3f} dex), scatter {s:.4f}, rms to tied law {t:.4f} (mean {mn:+.4f}), worst bin {wb:.4f}{v}')
    print(f'      bins ' + ' '.join(f'{x:.1f}:{y:+.3f}' for x, y in bins))
    print(f'      data under its nuisances: a {ao:.3e} ({np.log10(ao / A0):+.3f} dex), scatter {so:.4f}, rms to tied law {to:.4f}, worst bin {wbo:.4f}')
    summ[tag].update(a=a, s=s, t=t, wb=wb)
json.dump(res, open(CK, 'w'))
print(f'\nruntime {time.time() - T0:.0f} s, max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20:.0f} MB')
print('A comparable fit to data is not a derivation; a better or worse fit is not proof for either side.')
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
