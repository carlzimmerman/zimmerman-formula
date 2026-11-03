"""Amendment A5 of ../FROZEN_RECIPE.md: law, tuned recipes and base control against KiDS-1000 ESD. Analytic stand-in. Rival language for the recipes, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
from lib import *
import lib, copy
from scipy.stats import chi2 as CH
from colossus.lss import bias as BI
src = open(os.path.join(HERE, 'recipe4.py'), encoding='utf-8').read().split("\nreport('R11 12")[0]
exec(src.split('\n', 2)[2])
K11 = np.array([-.326, .677, -.881, -.600, -.638, -.757, .090, -.097, 1., .465, 1., -.332]); K14 = np.array([-.512, .359, -.138, -.600, -.986, -.439, .052, -.139, .793, .597, 1., -.415, -.330, .150]); KC = np.array([0, 0, 0, 0, -5., 0, 0, 0, 0, 0, 0, 0.])
LR = os.path.join(D, 'lensing_rar'); B = os.path.join(LR, 'brouwer2021_rar'); pc = kpc / 1e3
AD = [np.loadtxt(os.path.join(B, f'Fig-3_Lensing-rotation-curves_Massbin-{i}.txt')) for i in range(1, 5)]
RM = AD[0][:, 0]; DAT = np.concatenate([a[:, 1] / a[:, 4] for a in AD]); c = np.loadtxt(os.path.join(B, 'Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt'))
mins = np.unique(c[:, 0]); ii = {round(r, 8): k for k, r in enumerate(RM)}; n = len(RM); COV = np.zeros((4 * n, 4 * n))
for l in c:
    a, b = np.searchsorted(mins, l[0]) * n + np.argmin(abs(RM - l[2])), np.searchsorted(mins, l[1]) * n + np.argmin(abs(RM - l[3])); COV[a, b] = l[4] / l[6]
COV = .5 * (COV + COV.T); ICOV = np.linalg.inv(COV); print(f'data: {len(DAT)} points, R {RM[0]:.3f}-{RM[-1]:.3f} Mpc, S/N against zero {np.sqrt(DAT @ ICOV @ DAT):.1f}, cond {np.linalg.cond(COV):.1e}')
E_ = [8.5, 10.3, 10.6, 10.8, 11.0]; L0 = np.load(os.path.join(LR, 'lr_lenses.npz')); LM_, MG = L0['logM'], L0['Mgal']; Q = (np.arange(25) + .5) / 25
SETS = []
for i in range(4):
    s = (LM_ >= E_[i]) & (LM_ < E_[i + 1]); o = np.argsort(LM_[s]); idx = (Q * s.sum()).astype(int); SETS.append((10**LM_[s][o][idx], MG[s][o][idx])); print(f' bin {i + 1}: n {s.sum()}, median log M* {np.median(LM_[s]):.2f}, median log Mgal {np.median(np.log10(MG[s])):.2f}')
RE = np.logspace(np.log10(.2), np.log10(3e4), 401) * kpc
def ds(Rm, edges, Ms, M0=0.):
    """ESD in Msun/pc^2 at R (m) from shell masses Ms (kg) between edges (m), M0 point mass at the centre; constant density in each shell."""
    a, b = edges[:-1], edges[1:]; rho = Ms / (4 * np.pi / 3 * (b**3 - a**3)); out = []
    for R in Rm:
        sb, sa = np.sqrt(np.maximum(b**2 - R**2, 0)), np.sqrt(np.maximum(a**2 - R**2, 0)); S = (2 * rho * (sb - sa)).sum(); P = M0 + (rho * 4 * np.pi / 3 * ((b**3 - a**3) - sb**3 + sa**3)).sum(); out.append(P / (np.pi * R**2) - S)
    return np.array(out) * pc**2 / Msun
Rm = RM * 1e3 * kpc
sig = 1e5; ME = 2 * sig**2 * RE / G; t = ds(Rm, RE, np.diff(ME)); print(f'control SIS, max |ratio-1| R<1 Mpc: {abs(t / (sig**2 / (2 * G * Rm) * pc**2 / Msun) - 1)[RM < 1].max():.4f}'); t = ds(Rm, RE, np.zeros(400), 1e11 * Msun); print(f'control point mass, max |ratio-1|: {abs(t / (1e11 / (np.pi * (Rm / pc)**2)) - 1).max():.4f}')
def ml(rs, Mg): g = G * Mg * Msun / rs**2; return law(g) * rs**2 / G - Mg * Msun
def LAW(Ms, Mg, **k): return ds(Rm, RE, np.diff(np.r_[0, ml(RE[1:], Mg)]), Mg * Msun + ml(RE[:1], Mg)[0])
x = np.log10([g.Mb for g in GS]); y = np.log10([g.Rd / kpc for g in GS]); P = np.polyfit(x, y, 1); print(f'SPARC R_d line: log R_d = {P[1]:+.3f} {P[0]:+.3f} log M_b')
def rec(Ms, Mg, k):
    h = Gal(); h.Ms, h.Mb = Ms, max(Mg, Ms); h.Rd = 10**np.polyval(P, np.log10(h.Mb)) * kpc; h.r = RE[1:]; h.mbtot = h.Mb * Msun; h.mb = np.full(len(h.r), h.mbtot); h.gb = G * h.mb / h.r**2
    M = m200k(Ms, *k[:4]); R200 = (3 * M * Msun / (4 * np.pi * 200 * globals()['RHOC']))**(1 / 3); m = (gal(h, k) - h.gb) * h.r**2 / G; m = np.where(h.r <= R200, m, np.interp(R200, h.r, m)); m = np.maximum.accumulate(np.maximum(m, 0))
    return M, ds(Rm, RE, np.diff(np.r_[0, m]), h.mbtot)
Zb = .25; rg = np.logspace(-2.5, 2.2, 400); xi = cos.correlationFunction(rg * cos.h * (1 + Zb), Zb); rm = cos.rho_m(Zb) * cos.h**2
Eg = rg * 1e3 * kpc; DMM = ds(Rm, Eg, (4 * np.pi * rm * ((rg[1:] * 1e3)**3 - (rg[:-1] * 1e3)**3) / 3 * .5 * (xi[1:] + xi[:-1])) * Msun)
print(' mm ESD at 1 Mpc per unit bias:', round(float(np.interp(1, RM, DMM)), 3), 'Msun/pc^2')
def REC(Ms, Mg, k=None):
    M, d = rec(Ms, Mg, k); return d + float(BI.haloBias(M * cos.h, z=Zb, mdef='200c', model='tinker10')) * DMM
def stack(fn, dm=0., **k): return np.concatenate([np.mean([fn(a * 10**dm, b * 10**dm, **k) for a, b in zip(*S)], axis=0) for S in SETS])
IN = np.concatenate([RM <= 1] * 4); IC = np.linalg.inv(COV[np.ix_(IN, IN)])
def score(tag, m):
    r = DAT - m; X = r @ ICOV @ r; pv = CH.sf(X, len(DAT)); ri = r[IN]; Xi = ri @ IC @ ri; pi_ = CH.sf(Xi, IN.sum()); Aa = (m @ ICOV @ DAT) / (m @ ICOV @ m); e = (m @ ICOV @ m)**-.5
    bins = [float(r[i * n:(i + 1) * n] @ np.linalg.inv(COV[i * n:(i + 1) * n, i * n:(i + 1) * n]) @ r[i * n:(i + 1) * n]) for i in range(4)]
    print(f'{tag:30s} chi2 {X:7.1f}/60 p {pv:.1e} [{"PASS" if pv >= .01 else "FAIL"}]; R<=1 Mpc {Xi:7.1f}/{IN.sum()} p {pi_:.1e}; bins {" ".join(f"{b:.1f}" for b in bins)}; A {Aa:.3f}+-{e:.3f}', flush=True)
print('\nMain rows')
for tag, fn, k in (('L plain law', LAW, {}), ('R11 12 knobs', REC, dict(k=K11)), ('R11b 14 knobs', REC, dict(k=K14)), ('C base LCDM control', REC, dict(k=KC))):
    score(tag, stack(fn, **k))
print('\nM* and Mgal +-0.1 dex')
for dm in (-.1, .1):
    for tag, fn, k in (('L', LAW, {}), ('R11', REC, dict(k=K11)), ('R11b', REC, dict(k=K14)), ('C', REC, dict(k=KC))): score(f'{tag} dm {dm:+.1f}', stack(fn, dm, **k))
print('\nRecipes with c and rho_crit at z = 0.25')
RHOC = cos.rho_c(Zb) * cos.h**2 * Msun / kpc**3; lib.CG = np.array([float(CM.concentration(10**m * cos.h, '200c', Zb, model='diemer19')) for m in LM])
for tag, k in (('R11', K11), ('R11b', K14), ('C', KC)): score(f'{tag} z 0.25', stack(REC, k=k))
print('\nAnalytic stand-in. Grades these models on these lenses only; not evidence either theory is right. kappa = 1/2 FITTED; not theory closed.')
