"""Amendment A10 of ../FROZEN_RECIPE.md: R13, joint global recipe, analytic stand-in. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
src = open('recipe6.py', encoding='utf-8').read().split("print('\\nMain rows')")[0]
exec(src)
A = .16
src4 = open('recipe4.py', encoding='utf-8').read(); exec(src4[src4.index('def ein'):src4.index('def gal(')])
from astropy.io import fits
import importlib.util as iu, time
sp = iu.spec_from_file_location('rt', os.path.join(HERE, '..', '..', 'REDTEAM_LCDM_PRIEST', 'scripts', 'lib.py')); rt = iu.module_from_spec(sp); sp.loader.exec_module(rt)
a_, b_ = RE[:-1], RE[1:]; vol = 4 * np.pi / 3 * (b_**3 - a_**3); SB = np.sqrt(np.maximum(b_[None, :]**2 - Rm[:, None]**2, 0)); SA = np.sqrt(np.maximum(a_[None, :]**2 - Rm[:, None]**2, 0))
MAT = (((b_**3 - a_**3)[None, :] - SB**3 + SA**3) * (4 * np.pi / 3) / vol / (np.pi * Rm[:, None]**2) - 2 * (SB - SA) / vol) * pc**2 / Msun; PT = 1 / (np.pi * Rm**2) * pc**2 / Msun
def fast(ms, M0): return MAT @ ms + PT * M0
def gal2(g, k, Mover=None):
    dn, dm, db, dg, le, a1, a2, a4, le0, a3, f0, f1, dc, sc, lcut = k[:15]
    M = Mover if Mover is not None else m200k(g.Ms, dn, dm, db, dg); c = float(cflat(M, dc, sc)); fb = min(g.Mb / M, .5); fg = max((g.Mb - g.Ms) / g.Mb, .01); sb = g.Mb / (g.Rd / kpc)**2 / 1e6 / 100
    e = 10**le * (g.Ms / M / .01)**a1 * sb**a2 * (fg / .5)**a4; n = np.tanh(min(e, 50)) / (1 + (M / 10**lcut)**2); eta = 10**le0 * (g.Ms / 1e9)**a3; f = np.clip(f0 + f1 * (np.log10(g.Mb) - 9.5), -1, 1)
    m0 = np.maximum(ein(g.r, M, c), 1e-30); ri = g.r.copy()
    for _ in range(12):
        mi = np.maximum(ein(ri, M, c), 1e-30); ri = .5 * ri + .5 * g.r * (g.mb + (1 - fb) * mi) / mi
    m = np.maximum((1 - f) * m0 + f * mi, 1e-3 * m0) * (1 - fb) * np.tanh(g.r / (eta * 1.75 * g.Rd))**n
    return G * m / g.r**2, M
H = Gal(); H.r = RE[1:]
def lensd(Ms, Mg, k):
    h = copy.copy(H); h.Ms = Ms * 10**k[15]; h.Mb = max(Mg * 10**k[15], h.Ms); h.Rd = 10**np.polyval(P, np.log10(h.Mb)) * kpc; h.mbtot = h.Mb * Msun; h.mb = np.full(len(h.r), h.mbtot); gd, M = gal2(h, k); R200 = (3 * M * Msun / (4 * np.pi * 200 * RHOC))**(1 / 3); m = gd * h.r**2 / G; m = np.where(h.r <= R200, m, np.interp(R200, h.r, m)); m = np.maximum.accumulate(np.maximum(m, 0))
    return fast(np.diff(np.r_[0, m]), h.mbtot) + 10**k[16] * float(BI.haloBias(M * cos.h, z=Zb, mdef='200c', model='tinker10')) * DMM, M
def hostd(lM):
    M = 10**lM; R = (3 * M * Msun / (4 * np.pi * 200 * RHOC))**(1 / 3); c = float(cflat(M, 0, 0)); rr = RE[1:]; m = M * Msun * mu(np.minimum(rr, R) * c / R) / mu(c); return fast(np.diff(np.r_[0, m]), 0) + float(BI.haloBias(M * cos.h, z=Zb, mdef='200c', model='tinker10')) * DMM
CHOL = {}
def whit(bins):
    I = np.concatenate([np.arange(i * n, (i + 1) * n) for i in bins])
    if tuple(bins) not in CHOL: CHOL[tuple(bins)] = (I, np.linalg.inv(np.linalg.cholesky(COV[np.ix_(I, I)])))
    return CHOL[tuple(bins)]
def kids(k, bins=(0, 1, 2, 3), every=3):
    o = np.zeros(4 * n); hd = hostd(k[18])
    for i in bins:
        S = SETS[i]; d = np.mean([lensd(a, b, k)[0] for a, b in zip(S[0][::every], S[1][::every])], axis=0); o[i * n:(i + 1) * n] = (1 - k[17]) * d + k[17] * hd
    return o
XD = os.path.join(D, 'xcop'); XC = []
def li(r, m, t): return float(10**np.interp(np.log10(t), np.log10(r), np.log10(m)))
for nm in sorted(x for x in os.listdir(XD) if os.path.exists(os.path.join(XD, x, f'{x}_mstar.fits'))):
    with fits.open(os.path.join(XD, nm, f'{nm}_hydro_mass.fits')) as h_: hm = h_[1].data.copy(); r5 = h_[1].header['R500']
    with fits.open(os.path.join(XD, nm, f'{nm}_fgas_profile.fits')) as h_: ga = h_[1].data.copy(); rg = h_[1].header['R500']
    with fits.open(os.path.join(XD, nm, f'{nm}_mstar.fits')) as h_: st = h_[2].data.copy()
    rows = []
    for x_ in (.1, .2, .3, .5, .7):
        rr_ = x_ * r5
        if not (hm['RADIUS'][0] <= rr_ <= hm['RADIUS'][-1] and ga['RADIUS'][0] * rg <= rr_ <= ga['RADIUS'][-1] * rg and st['RADIUS'][0] <= rr_ <= st['RADIUS'][-1]): continue
        rows.append((rr_ * kpc, li(hm['RADIUS'], hm['M_FORW'], rr_), li(ga['RADIUS'] * rg, ga['MGAS'], rr_), li(st['RADIUS'], st[st.names[1]], rr_), li(hm['RADIUS'], hm['EM_FORW'], rr_)))
    if len(rows) < 3: continue
    A_ = np.array(rows); g = Gal(); g.n = nm; g.r = A_[:, 0]; g.mb = (A_[:, 2] + A_[:, 3]) * Msun; g.mobs = A_[:, 1] * Msun; g.err = A_[:, 4] / A_[:, 1] / np.log(10); g.Mb = float(li(ga['RADIUS'] * rg, ga['MGAS'], min(r5, ga['RADIUS'][-1] * rg)) + li(st['RADIUS'], st[st.names[1]], min(r5, st['RADIUS'][-1]))); g.Ms = float(li(st['RADIUS'], st[st.names[1]], min(r5, st['RADIUS'][-1]))); g.Rd = 10**np.polyval(P, np.log10(g.Mb)) * kpc; XC.append(g)
g = XC[0]; M_ = g.mobs[-1] / Msun; print(f'control {g.n}: r {g.r[-1] / kpc:.0f} kpc, M_HSE {M_:.2e}, M_b {g.mb[-1] / Msun:.2e}, f_b {g.mb[-1] / g.mobs[-1]:.3f}')
print(f'X-COP systems {len(XC)}, points {sum(len(g.r) for g in XC)}; median EM/M in dex {np.median(np.concatenate([g.err for g in XC])):.3f}')
def xres(k, S): return np.concatenate([np.log10((1 - k[19]) * (gal2(g, k, g.Mb / k[20])[0] * g.r**2 / G + g.mb) / g.mobs) for g in S])
LO = np.array([-.54, -.9, -1.2, -.6, -2, -3, -3, -3, -1, -1, -1, -1, -.33, -.15, 11, -.3, -.3, 0, 12.5, 0, .08]); HI = np.array([.54, .9, 1.2, .6, 1.48, 3, 3, 3, 1, 1, 1, 1, .33, .15, 14, .3, .3, .3, 14, .4, .16])
NM = 'SHMRnorm logM1 beta gamma log_eps a1 a2 a4 log_eta0 a3 f0 f1 cnorm cslope logMcut lensdM log2h fsat logMhost bHSE fcl'.split()
def sres(k, S): return np.concatenate([np.log10(g.gb + gal2(g, k)[0]) - np.log10(g.gl) for g in S])
def res(k, SS, bins, XX):
    r1 = sres(k, SS) / .02 * np.sqrt(60 / sum(len(g.r) for g in SS)); I, W = whit(bins); r2 = W @ (DAT - kids(k, bins))[I]; r3 = xres(k, XX) / .1; return np.r_[r1, r2, r3]
K14 = [-.512, .359, -.138, -.600, -.986, -.439, .052, -.139, .793, .597, 1., -.415, -.330, .150]; X0 = np.array(K14 + [13., .1, 0., .05, 13., .15, .13])
def tune(SS, bins, XX, x0, nfev=30):
    best = None
    for s in range(3):
        x = x0 if s == 0 else np.clip(x0 + np.random.default_rng(s).normal(0, .12, len(x0)) * (HI - LO), LO, HI); t0 = time.time()
        r = least_squares(res, np.clip(x, LO + 1e-4 * (HI - LO), HI - 1e-4 * (HI - LO)), args=(SS, bins, XX), bounds=(LO, HI), max_nfev=nfev, diff_step=.01, x_scale=HI - LO); print(f'  start {s}: cost {r.cost:.1f}, nfev {r.nfev}, {time.time() - t0:.0f}s', flush=True)
        if best is None or r.cost < best.cost: best = r
    return best.x
def kchi(m, bins=(0, 1, 2, 3)):
    I = np.concatenate([np.arange(i * n, (i + 1) * n) for i in bins]); r = (DAT - m)[I]; return r @ np.linalg.solve(COV[np.ix_(I, I)], r), len(I)
print('\nHoldout tuning', flush=True)
ko = tune(GS[::2], (0, 2), XC[::2], X0); so = sres(ko, GS[1::2]); xo = xres(ko, XC[1::2]); mo = kids(ko, (1, 3), 1); xh, nh = kchi(mo, (1, 3))
print(f'L8 SPARC unseen {np.sqrt((so**2).mean()):.4f} dex [<=0.05 {"PASS" if np.sqrt((so**2).mean()) <= .05 else "FAIL"}]; KiDS unseen bins chi2 {xh:.1f}/{nh} p {CH.sf(xh, nh):.1e} [{"PASS" if CH.sf(xh, nh) >= .01 else "FAIL"}]; X-COP unseen rms {np.sqrt((xo**2).mean()):.3f}, mean {xo.mean():+.3f} [{"PASS" if np.sqrt((xo**2).mean()) <= .15 else "FAIL"}]', flush=True)
print('\nAll-data tuning', flush=True)
ka = tune(GS, (0, 1, 2, 3), XC, ko); json.dump(ka.tolist(), open('recipe12_knobs.json', 'w'))
grade('L1, L2 R13', [g.gb + gal2(g, ka)[0] for g in GS], '(21 knobs)')
m = kids(ka, (0, 1, 2, 3), 1); X, N_ = kchi(m); I_ = np.concatenate([RM <= 1] * 4); Xi = (DAT - m)[I_] @ np.linalg.solve(COV[np.ix_(I_, I_)], (DAT - m)[I_]); bb = [kchi(m, (i,))[0] for i in range(4)]; print(f'L3 KiDS chi2 {X:.1f}/60, p at 54 dof {CH.sf(X, 54):.1e} [{"PASS" if CH.sf(X, 54) >= .01 else "FAIL"}]; R<=1 Mpc {Xi:.1f}/{I_.sum()}; bins {" ".join(f"{b:.1f}" for b in bb)}')
xa = xres(ka, XC); print(f'L4 X-COP mean {xa.mean():+.3f}, rms {np.sqrt((xa**2).mean()):.3f} dex [{"PASS" if abs(xa.mean()) <= .05 and np.sqrt((xa**2).mean()) <= .12 else "FAIL"}]')
b_ = np.array([min(v - a, c_ - v) < 1e-3 * (c_ - a) for v, a, c_ in zip(ka, LO, HI)]); print(' knobs', ' '.join(f'{nm}={v:+.3f}{"*" if q else ""}' for nm, v, q in zip(NM, ka, b_))); dM = [np.log10(m200k(g.Ms, *ka[:4]) / m200_of(g.Ms)) for g in GS]; pp = np.percentile(dM, [16, 50, 84]); print(f'L9 at bound {b_.sum()} of 21; dlogM200 p16, p50, p84 {np.round(pp, 2).tolist()} [{"PASS" if b_.sum() <= 3 and abs(pp[1]) <= .3 else "FAIL"}]', flush=True)
def setcos(C, z=0):
    global RHOC
    cc.setCurrent(C); h = C.h; lib.CG = np.array([float(CM.concentration(10**m_ * h, '200c', z, model='diemer19')) for m_ in LM]); RHOC = C.rho_c(z) * h**2 * Msun / kpc**3; return C.Ode0 * C.rho_c(0) * h**2 * Msun / kpc**3
def af(cm=1., Mm=1.):
    k = ka.copy(); k[12] += np.log10(cm); return fit_a(ALLB, np.concatenate([g.gb + gal2(g, k, m200k(g.Ms, *k[:4]) * Mm)[0] for g in GS]))
u, d, dl = rt.cosmo_case('rde'); wb = .0493 * .674**2; CU, CD = rt.setc(**u)[0], rt.setc(**d)[0]; KS = [rt.setc(H0=67.4, OL=.70, wb=wb)[0], rt.setc(H0=73., OL=.685, wb=wb)[0], rt.setc(H0=73., OL=.65, wb=wb)[0]]; C0 = rt.setc()[0]; R0 = setcos(C0); a00 = af(); GRP = [(C, setcos(C)) for C in (CU, CD, *KS)]; UNIT = lambda R: 2.998e8 * np.sqrt(G * R)
def state(v):
    A = []
    for C, R in GRP:
        setcos(C); h = C.H0 / 67.4; A.append(af((R / R0)**v[0] * h**v[1], h**v[2]))
    return A
A0s = state((0, 0, 0)); print(f'\nbase a {a00:.3e}; no hand: slope {np.log(A0s[0] / A0s[1]) / dl:+.3f}; kappa', [round(float(A0s[i + 2] / UNIT(GRP[i + 2][1])), 3) for i in range(3)])
v = least_squares(lambda v: np.r_[(np.log((AX := state(v))[0] / AX[1]) / dl - .5) * 2, [np.log(AX[i + 2] / UNIT(GRP[i + 2][1]) / .5) for i in range(3)]], [.2, 0, 0], max_nfev=12, diff_step=.05, bounds=([-3, -12, -12], [3, 12, 12])).x; AS = state(v); sl = np.log(AS[0] / AS[1]) / dl; ks = [float(AS[i + 2] / UNIT(GRP[i + 2][1])) for i in range(3)]
print(f'L5 hand p {v[0]:.2f}, r {v[1]:.2f}, s {v[2]:.2f}: slope {sl:+.3f} [{"PASS" if abs(sl - .5) <= .05 else "FAIL"} E4]; kappa', [round(x_, 3) for x_ in ks], f'[{"PASS" if all(abs(x_ / .5 - 1) <= .05 for x_ in ks) else "FAIL"}]', flush=True)
BAND = {1.: (.76, 1.03), 1.5: (.71, 1.12), 2.33: (.33, 1.21)}; TG = {1.: .91, 1.5: .94, 2.33: .91}
def zs(q):
    o = {}
    for z in BAND: setcos(C0, z); o[z] = af((1 + z)**(q[0] + q[1] * z)) / a00
    return o
print(' a(z)/a(0) no hand', {z: round(float(x_), 3) for z, x_ in zs((0, 0)).items()}); q = least_squares(lambda q: [np.log(zs(q)[z] / TG[z]) for z in BAND], [-1, 0], max_nfev=10, diff_step=.05).x; o = zs(q); print(f'L6 hand q1 {q[0]:.2f}, q2 {q[1]:.2f}:', {z: round(float(x_), 3) for z, x_ in o.items()}, f'[{"PASS" if all(BAND[z][0] <= o[z] <= BAND[z][1] for z in BAND) else "FAIL"} E5]')
print('L7 Cassini: PASS from A9, smooth halo, 2.0e-9 a0 at Saturn')
print('\nAnalytic stand-in. Passing shows freedom, not evidence. Lines not graded are listed in A10. kappa = 1/2 FITTED; not theory closed.')
