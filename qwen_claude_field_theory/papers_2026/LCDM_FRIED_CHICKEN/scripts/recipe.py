"""LCDM-flavoured recipes against the law on real SPARC baryons, per ../FROZEN_RECIPE.md.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
from lib import *
print('reference: law against observed, same points, no per-galaxy freedom')
print(f' rms {np.sqrt(((np.log10(ALLL) - np.log10(ALLO))**2).mean()):.4f} dex, mean {(np.log10(ALLL) - np.log10(ALLO)).mean():+.4f}')
k0 = np.array([0., 0., 0., 0.]); grade('R1 base, no tuning, no contraction', [r1(g, k0) for g in GS])
k1 = fit(r1, np.array([0, 0, 0, .5]), [-.33, -.15, -.54, -1], [.33, .15, .54, 1], 'R1'); grade('R1 tuned: c norm, c slope, SHMR norm, contraction', [r1(g, k1) for g in GS])
k2 = fit(r2, np.array([*k1[:3], 0, 1.75, .5, 0.]), [-.33, -.15, -.54, 0, .1, 0, -2], [.33, .15, .54, 0.0001, 10, 3, 2], 'R2'); grade('R2 tuned: R1 + core radius, n norm, n slope', [r2(g, k2) for g in GS])
def r3(g, k):
    rho0, sig = r3params(g, 10**k[0], 10**k[1]); return thermal(g, rho0, sig)
k3 = fit(r3, np.array([0., np.log10(A0 / G / 2)]), [-1, np.log10(A0 / G) - 2], [1, np.log10(A0 / G) + 2], 'R3')
g3 = [r3(g, k3) for g in GS]; grade('R3 thermal halo, two global laws', g3, f'(s={10**k3[0]:.3f}, G Sigma*/a0={10**k3[1] * G / A0:.3f}, Sigma*={10**k3[1] * kpc**2 / 1e6 / Msun:.0f} Msun/pc^2)')
# E4: thermal scales written with a0, then with a0 frozen
at = lambda a: fit_a(ALLB, np.concatenate([thermal(g, *r3params(g, 10**k3[0], 10**k3[1] * a / A0, a)) for g in GS]))
sl = np.log(at(1.2 * A0) / at(A0 / 1.2)) / np.log(1.44)
print(f'\nE4 R3: d ln a_fit / d ln a0 in the hand-written scales = {sl:.3f}; so rho_DE slope {sl * .5:+.3f} with a0 hand-tied to sqrt(rho_DE) [{"PASS" if abs(sl * .5 - .5) <= .05 else "FAIL"}], and 0 by construction if Sigma*, sigma scale are constants [FAIL]')
def r4(g, x0):
    rs = lambda v: np.log10(thermal(g, 10**v[0], 10**v[1])) - np.log10(g.gl); best = None
    for dv in ((0, 0), (.7, -.1), (-.7, .1)):
        r = least_squares(rs, x0 + np.array(dv), max_nfev=30, diff_step=.01)
        if best is None or r.cost < best.cost: best = r
    return best.x
x4 = [r4(g, np.array([np.log10(r3params(g, 10**k3[0], 10**k3[1])[0]), np.log10(r3params(g, 10**k3[0], 10**k3[1])[1])])) for g in GS]
g4 = [thermal(g, 10**x[0], 10**x[1]) for g, x in zip(GS, x4)]; grade('R4 thermal halo, rho0 and sigma free per galaxy', g4, f'({2 * len(GS)} parameters)')
sg = np.array([10**x[1] for x in x4]); mb = np.array([g.mbtot for g in GS]); s = np.array([sig4 for sig4 in 4 * sg**4 / (G * mb * A0)])
print(f' R4 sigma^4/(G M_b a0/4): median {np.median(s):.3f}, p16-p84 {np.percentile(s, 16):.3f}-{np.percentile(s, 84):.3f}')
sd = np.array([10**x[0] * 3 * sg_ / np.sqrt(4 * np.pi * G * 10**x[0]) for x, sg_ in zip(x4, sg)]) * G / A0
print(f' R4 G rho0 r_c/a0: median {np.median(sd):.3f}, p16-p84 {np.percentile(sd, 16):.3f}-{np.percentile(sd, 84):.3f}')
grade('R5 exact halo', [g.gb + (g.gl - g.gb) for g in GS], f'({len(ALLB)} free shell masses)')
# Checks on R5, smoothed baryons, tail Keplerian beyond the last point
out = dict(pos=0, jeans=0, edd=0, mono=0, n=0); res = []; dvs = []; cr = []; mr = []; rms = []
for g in GS:
    x = np.linspace(np.log(g.r[0]) - 3, np.log(g.r[-1]) + 5, 500); lr = np.log(g.r); rr = np.exp(x)
    lg = np.interp(x, lr, np.log(g.gb)); h = x < lr[0]; lg[h] = np.log(g.gb[0]) + (x[h] - lr[0]); t = x > lr[-1]
    gt_ = g.mbtot if g.mbtot > g.mb[-1] else g.mb[-1]; lg[t] = np.log(G * gt_ / rr[t]**2); lg = gaussian_filter1d(lg, .1 * np.log(10) / (x[1] - x[0]))
    gb = np.exp(lg); gl = law(gb); gd = gl - gb; md = rr**2 * gd / G; mt = rr**2 * gl / G
    rho = np.gradient(md, x) / (4 * np.pi * rr**3)
    i200 = np.argmax(mt / (4 / 3 * np.pi * rr**3) < 200 * RHOC); R200 = rr[i200]; M200 = mt[i200] / Msun
    w = rr <= R200; pos = (rho[w] > 0).all(); out['pos'] += pos; out['n'] += 1
    rhoT = np.maximum(rho, 1e-40) * np.exp(-(rr / (2 * R200))**2)
    sigr2 = np.cumsum((rhoT * gl * rr)[::-1])[::-1] * (x[1] - x[0]) / rhoT; jj = (sigr2[w] > 0).all(); out['jeans'] += jj
    vr = np.median((sigr2 / (gl * rr))[w]); dvs.append(vr)
    psi = np.cumsum((gl * rr)[::-1])[::-1] * (x[1] - x[0]); P = psi[::-1]; R = rhoT[::-1]; E = np.linspace(P[3], P[-1], 240); dR = np.diff(R) / np.maximum(np.diff(P), 1e-30); I = np.empty(len(E))
    for j, e in enumerate(E):
        p0, p1 = P[:-1], P[1:]; a = np.sqrt(np.maximum(e - p0, 0)); b = np.sqrt(np.maximum(e - p1, 0)); I[j] = (dR * 2 * (a - b)).sum()
    f = np.gradient(I, E); in200 = E >= psi[i200]; edd = f[in200].min() >= -.01 * f[in200].max(); out['edd'] += edd
    fb = min(g.Mb * Msun / (M200 * Msun), .5); mbg = mt - md
    ri = rr * (md + mbg) * (1 - fb) / md; Mi = md / (1 - fb); mono = (np.diff(ri[w]) > 0).all(); out['mono'] += mono
    keep = w & (x > lr[0]); ri2 = ri[keep]; Mi2 = Mi[keep]; ord_ = np.argsort(ri2)
    def rs(v): return np.log10(nfw_m(ri2, 10**v[0], 10**v[1])[0]) - np.log10(Mi2 * 1)
    v = least_squares(rs, [np.log10(M200), 1.]).x; rmsi = np.sqrt((rs(v)**2).mean()); rms.append(rmsi)
    cr.append(10**v[1] / np.interp(v[0], LM, CG)); mr.append(np.log10(M200 / m200_of(g.Ms)))
    res.append((g.n, np.log10(g.Mb), np.log10(M200), bool(pos), bool(jj), bool(edd), bool(mono), float(rmsi), float(10**v[1]), float(cr[-1])))
print(f"\nC1 density positive to R200: {out['pos']} of {out['n']} (smoothed 0.1 dex)\nC2 Jeans sigma_r^2 positive: {out['jeans']} of {out['n']}; median sigma_r^2/V^2 {np.median(dvs):.3f}\nC3 Eddington f(E) >= -1% of peak inside R200: {out['edd']} of {out['n']}")
print(f"C4 inverted Blumenthal initial profile monotonic: {out['mono']} of {out['n']}; NFW fit rms to initial M(r) median {np.median(rms):.3f} dex, p84 {np.percentile(rms, 84):.3f}; c_fit/c_Diemer median {np.median(cr):.2f}, p16-p84 {np.percentile(cr, 16):.2f}-{np.percentile(cr, 84):.2f}")
mr = np.array(mr); lm = np.array([r[1] for r in res])
print(f'C5 log M200(recipe)/M200(SHMR): median {np.median(mr):+.2f}, p16-p84 {np.percentile(mr, 16):+.2f} to {np.percentile(mr, 84):+.2f}')
for a, b in ((7, 9), (9, 10), (10, 11), (11, 12)):
    w = (lm >= a) & (lm < b); print(f' log M_b {a}-{b}: n {w.sum()}, median {np.median(mr[w]):+.2f}' if w.sum() else f' log M_b {a}-{b}: n 0')
json.dump(res, open(os.path.join(HERE, 'r5_checks.json'), 'w'), indent=0)
print('\nRival language; every knob disclosed. kappa = 1/2 FITTED; not theory closed.')
