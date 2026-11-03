"""Amendment A11 of ../FROZEN_RECIPE.md: R14, per-galaxy SPARC plus per-bin lensing freedom, and the law on X-COP. Analytic stand-in. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
src = open('recipe12.py', encoding='utf-8').read().split("print('\\nHoldout tuning'")[0]
exec(src)
ka = np.array(json.load(open('recipe12_knobs.json')))
xl = np.concatenate([np.log10(law(G * g.mb / g.r**2) * g.r**2 / G / g.mobs) for g in XC]); print(f'Law on X-COP, 35 points: mean {xl.mean():+.3f}, rms {np.sqrt((xl**2).mean()):.3f} dex; R13 was -0.001, 0.075')
def lens2(Ms, Mg, dm, lb, kt):
    k = ka; h = copy.copy(H); h.Ms = Ms * 10**dm; h.Mb = max(Mg * 10**dm, h.Ms); h.Rd = 10**np.polyval(P, np.log10(h.Mb)) * kpc; h.mbtot = h.Mb * Msun; h.mb = np.full(len(h.r), h.mbtot); gd, M = gal2(h, k); R200 = kt * (3 * M * Msun / (4 * np.pi * 200 * RHOC))**(1 / 3); m = gd * h.r**2 / G; m = np.where(h.r <= R200, m, np.interp(R200, h.r, m)); m = np.maximum.accumulate(np.maximum(m, 0))
    return fast(np.diff(np.r_[0, m]), h.mbtot) + 10**lb * float(BI.haloBias(M * cos.h, z=Zb, mdef='200c', model='tinker10')) * DMM
def mod(v, every=3):
    hd = hostd(v[12]); o = []
    for i in range(4):
        S = SETS[i]; d = np.mean([lens2(a, b, v[i], v[4 + i], v[13]) for a, b in zip(S[0][::every], S[1][::every])], axis=0); o.append((1 - v[8 + i]) * d + v[8 + i] * hd)
    return np.concatenate(o)
LO2 = np.r_[[-.3] * 4, [-.3] * 4, [0] * 4, 12.5, .5]; HI2 = np.r_[[.3] * 4, [.3] * 4, [.3] * 4, 14, 3]; NM2 = [f'dM{i}' for i in range(1, 5)] + [f'l2h{i}' for i in range(1, 5)] + [f'fs{i}' for i in range(1, 5)] + ['logMh', 'k']
Ix = np.arange(4 * n); odd = Ix[(Ix % n) % 2 == 0]; even = Ix[(Ix % n) % 2 == 1]
def W(I): return np.linalg.inv(np.linalg.cholesky(COV[np.ix_(I, I)]))
def fit(I):
    Wm = W(I); best = None
    for s in range(3):
        x = np.array([.0] * 4 + [.05] * 4 + [.05] * 4 + [13., 1.]) if s == 0 else np.random.default_rng(s).uniform(LO2, HI2)
        r = least_squares(lambda v: Wm @ (DAT - mod(v))[I], np.clip(x, LO2 + 1e-4, HI2 - 1e-4), bounds=(LO2, HI2), max_nfev=30, diff_step=.01, x_scale=HI2 - LO2); print(f'  start {s} cost {r.cost:.1f}', flush=True)
        if best is None or r.cost < best.cost: best = r
    return best.x
def chi(v, I):
    r = (DAT - mod(v, 1))[I]; return r @ np.linalg.solve(COV[np.ix_(I, I)], r), len(I)
vo = fit(odd); a, na = chi(vo, odd); b, nb = chi(vo, even); print(f'Holdout: tuned odd radii chi2 {a:.1f}/{na}; unseen even radii chi2 {b:.1f}/{nb}, p {CH.sf(b, nb):.1e} [{"PASS" if CH.sf(b, nb) >= .01 else "FAIL"}]', flush=True)
va = fit(Ix); X, _ = chi(va, Ix); bd = [min(x - l, h - x) < 1e-3 * (h - l) for x, l, h in zip(va, LO2, HI2)]; print(f'R14 KiDS chi2 {X:.1f}/60, p at 46 dof {CH.sf(X, 46):.1e} [{"PASS" if CH.sf(X, 46) >= .01 else "FAIL"}]; bounds {sum(bd)} of 14'); print(' ' + ' '.join(f'{m_}={x:+.3f}{"*" if q else ""}' for m_, x, q in zip(NM2, va, bd)))
print('Analytic stand-in, post-result escalation. kappa = 1/2 FITTED; not theory closed.')
