"""Amendment A6 of ../FROZEN_RECIPE.md: CDM halo reverse-engineered from the law, exact by construction. Reports freedom, not evidence. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
src = open('recipe6.py', encoding='utf-8').read().split("print('\\nMain rows')")[0]
exec(src)
c_ = 2.998e8; KAP = .5
def a_of(C): return KAP * c_ * np.sqrt(G * C.Ode0 * C.rho_c(0) * C.h**2 * Msun / kpc**3)
def halo(g, a): return g.gb + (law(g.gb, a) - g.gb)
A0h = a_of(cos); print(f'a from kappa = 1/2 and this cosmology: {A0h:.4e}; repo a0 {A0:.4e} (ratio {A0h / A0:.3f}); graded at repo a0')
grade('R12 reverse-engineered halo', [halo(g, A0) for g in GS], '(one function, kappa by hand)')
base = None
for OL, H0 in ((.70, 67.4), (.685, 73.), (.65, 73.)):
    C = cc.setCosmology(f'c{OL}{H0}', dict(flat=True, H0=H0, Om0=1 - OL, Ob0=.0493, sigma8=.811, ns=.965, relspecies=False)); a = a_of(C); r = C.Ode0 * C.rho_c(0) * C.h**2
    if base: print(f' OL {OL}, H0 {H0}: a {a:.3e}, kappa {a / (c_ * np.sqrt(G * r * Msun / kpc**3)):.3f}, slope against first row {np.log(a / base[0]) / np.log(r / base[1]):+.3f}')
    else: base = (a, r); print(f' OL {OL}, H0 {H0}: a {a:.3e}, kappa {a / (c_ * np.sqrt(G * r * Msun / kpc**3)):.3f}')
cc.setCurrent(cos); print(' a(z)/a(0) with w = -1: 1.000 at z = 1, 1.5, 2.33; inside E5 band by construction')
def R200_of(Mg):
    rr = RE[1:]; tot = Mg * Msun + ml(rr, Mg); d = tot - 200 * RHOC * 4 * np.pi / 3 * rr**3; i = np.where(d < 0)[0][0]; return rr[i], tot[i] / Msun
Mi = np.array([R200_of(g.Mb)[1] for g in GS]); dM = np.log10(Mi) - np.log10([m200_of(g.Ms) for g in GS]); fb = np.array([g.Mb for g in GS]) / Mi; x_ = np.log10([g.Mb for g in GS])
print(f'\nCosts on SPARC: log M200 implied minus SHMR p16, p50, p84 {np.round(np.percentile(dM, [16, 50, 84]), 2).tolist()}; M_b/M200 p16, p50, p84 {np.round(np.percentile(fb, [16, 50, 84]), 3).tolist()} against cosmic 0.156; above cosmic in {(fb > .156).sum()} of {len(GS)}')
for lo, hi in ((6, 9), (9, 10), (10, 11), (11, 13)):
    s = (x_ >= lo) & (x_ < hi); print(f' log M_b {lo}-{hi}: n {s.sum()}, median dlogM200 {np.median(dM[s]):+.2f}, median M_b/M200 {np.median(fb[s]):.3f}')
def R12t(Ms, Mg):
    R, M = R200_of(Mg); rr = RE[1:]; m = ml(rr, Mg); m = np.where(rr <= R, m, np.interp(R, rr, m)); return ds(Rm, RE, np.diff(np.r_[0, m]), Mg * Msun) + float(BI.haloBias(M * cos.h, z=Zb, mdef='200c', model='tinker10')) * DMM
print('\nLensing, same grade as A5')
score('R12n control, must be 276.1', stack(LAW)); score('R12 truncated + two-halo', stack(R12t))
for dm in (-.1, .1): score(f'R12 dm {dm:+.1f}', stack(R12t, dm))
print('\nExact by construction. Not evidence for either theory. kappa = 1/2 FITTED; not theory closed.')
