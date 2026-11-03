"""Amendment A9 of ../FROZEN_RECIPE.md: consequences if the halo is a real particle. Axiom for this exercise; not proof one exists. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
src = open('recipe10.py', encoding='utf-8').read().split("mU = mu_(Qs).min()")[0]
exec(src)
def full(fn, rlo, rhi):
    x = np.linspace(np.log(rlo), np.log(rhi) + 5, 700); rr = np.exp(x); gb = fn(rr); gl = law(gb); md = rr**2 * (gl - gb) / G; rho = np.maximum(np.gradient(md, x) / (4 * np.pi * rr**3), 1e-40); P = np.cumsum((rho * gl * rr)[::-1])[::-1] * (x[1] - x[0]); return x, rr, rho, P
LR, LP, GI = [], [], []
for i, g in enumerate(GS):
    lr = np.log(g.r); lg = np.log(g.gb); tail = G * max(g.mbtot, g.mb[-1]); fn = lambda rr, lr=lr, lg=lg, tail=tail: np.exp(gaussian_filter1d(np.where(np.log(rr) > lr[-1], np.log(tail / rr**2), np.interp(np.log(rr), lr, lg)), 5))
    x, rr, rho, P = full(fn, g.r[0], g.r[-1]); w = rr <= g.r[-1]; LR.append(np.log10(rho[w])); LP.append(np.log10(P[w])); GI.append(np.full(w.sum(), i))
LR, LP, GI = map(np.concatenate, (LR, LP, GI)); b = np.floor(LR * 2) / 2; S = []
for v in np.unique(b):
    s = b == v
    if len(np.unique(GI[s])) >= 20:
        pg = [LP[s][GI[s] == j].mean() for j in np.unique(GI[s])]; S.append((v, np.std(pg), len(pg)))
S = np.array(S); print(f'\nA1 log P at fixed log rho: rms by bin median {np.median(S[:, 1]):.3f} dex, range {S[:, 1].min():.3f}-{S[:, 1].max():.3f}, {len(S)} bins [{"PASS" if np.median(S[:, 1]) <= .1 else "FAIL"} one barotrope]')
pr = (G * np.array([g.Mb * Msun for g in GS]) * A0 / 4)**.25; r_ = SP[:, 1] / pr; print(f'A2 sigma/(G M_b a0/4)^(1/4) at last point: p16, p50, p84 {np.round(np.percentile(r_, [16, 50, 84]), 3).tolist()}; rms {np.std(np.log10(r_)):.3f} dex; m sigma^2 at 10 eV p50 {10 * np.median(SP[:, 1])**2 / c**2 * 1e3:.3f} meV')
Mw = 6.5e10; r = prof(lambda rr: G * Mw * Msun / rr**2, .5 * kpc, 300 * kpc, [8 * kpc])[0]; rb = 2 * 1.327e20 / r[1]**2; Rs = 1.43e12; ge = 4 * np.pi * G * r[0] * Rs / 3
print(f'A3 Milky Way 8 kpc: rho {r[0] * (kpc / 1e3)**3 / Msun:.3f} Msun/pc^3, sigma {r[1] / 1e3:.0f} km/s; binding radius to the Sun {rb / 1.496e11:.3f} AU; extra g at Saturn {ge:.2e} m/s^2 = {ge / A0:.1e} a0 [{"PASS" if ge / A0 < 1e-3 else "FAIL"}]; particle mass inside Saturn {4 * np.pi / 3 * r[0] * Rs**3:.1e} kg')
print('\nA4 window, eV (lower, upper; yes if lower < upper)')
for R in (50, 100, 200):
    cl = max(mu_(prof(lambda rr, Mb=Mb: G * Mb * Msun / rr**2, 10 * kpc, 3000 * kpc, [R * kpc])[0][0] * h_**3 / prof(lambda rr, Mb=Mb: G * Mb * Msun / rr**2, 10 * kpc, 3000 * kpc, [R * kpc])[0][1]**3) for Mb in (1e13, 1e14))
    for N in (.1, 1, 10):
        lo, u1, u2 = cl * N**-.25, mu_(Qs, N).min(), np.percentile(mu_(Qs, N), 5); print(f'  R {R} kpc, N {N:g}: lower {lo:.2f}; upper all 171 {u1:.2f} {"yes" if lo < u1 else "NO"}; upper 95 % {u2:.2f} {"yes" if lo < u2 else "NO"}')
print('Axiom for this exercise; consequences only. kappa = 1/2 FITTED; not theory closed.')
