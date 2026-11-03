"""A7 control-failure diagnostic of ../FROZEN_RECIPE.md. Written after the first numbers. kappa = 1/2 FITTED; not theory closed."""
src = open('recipe9.py', encoding='utf-8').read().split("print('Controls on 12")[0]
exec(src)
Mh, a = 1e11 * Msun, 3 * kpc; x = np.linspace(np.log(a) - 6, np.log(a) + 8, 900); rr = np.exp(x); rho = Mh * a / (2 * np.pi * rr * (rr + a)**3); gt = G * Mh / (rr + a)**2
E, f, gE, psi = DF(x, rr, rho, gt); vg = (G * Mh / a)**.5; e = E * a / (G * Mh); ex = Mh / (8 * 2**.5 * np.pi**3 * a**3 * vg**3) * ((1 - e)**-2 * (3 * np.arcsin(e**.5) * (1 - 8 * e + 8 * e**2) * (e * (1 - e))**-.5 * 1 + 0) + 0 * e) if False else None
q = np.sqrt(e); fa = Mh / (8 * 2**.5 * np.pi**3 * a**3 * vg**3) * (3 * np.arcsin(q) + q * (1 - e)**.5 * (1 - 2 * e) * (8 * e**2 - 8 * e - 3)) / (1 - e)**2.5
w = (e > .02) & (e < .9); print(f'(a) Hernquist Eddington / analytic, e 0.02-0.9: median {np.median(f[w] / fa[w]):.3f}, range {np.min(f[w] / fa[w]):.3f}-{np.max(f[w] / fa[w]):.3f}')
print(f'    mass from f and g(E) / Hernquist mass: {np.trapz(f * gE, E) / Mh:.3f}')
def worst(fin, ini, f0): r = Dx(f0, *fin[:3]) / np.maximum(Dx(f0, *ini[:3]), 1e-300); return r.max(), int(np.argmax(r)), r
RK = {'same': [], 'c x4': [], 'c /4': [], 'mix': []}; A = []
for g in GS[::14]:
    x, rr, gb, gl, md, rho, R, Mt, Md, i = setup(g); c = float(cflat(Mt, 0, 0)); ini = DF(x, rr, *nfw_prof(rr, x, R, Md, Mt, c)); f0 = grid(ini, rr, g.r[0], g.r[-1])
    for k, m in (('c x4', 4), ('c /4', .25)):
        RK[k].append(worst(DF(x, rr, *nfw_prof(rr, x, R, Md, Mt, c * m)), ini, f0)[:2])
    E, f, gE, _ = ini; dV = gE * np.gradient(E); fm = f.copy()
    for s in range(0, len(f), 8):
        b = slice(s, s + 8); fm[b] = (f[b] * dV[b]).sum() / dV[b].sum()
    RK['mix'].append(worst((E, fm, gE), ini, f0)[:2])
for k in ('c x4', 'c /4', 'mix'):
    v = np.array(RK[k]); print(f'(b,c) {k}: max worst ratio {v[:, 0].max():.3f}; rank of worst f0 median {np.median(v[:, 1]):.0f}, range {v[:, 1].min():.0f}-{v[:, 1].max():.0f} of 0-28')
Rk = []; Rs = []; Hi = []
for g in GS:
    x, rr, gb, gl, md, rho, R, Mt, Md, i = setup(g); rt = rho * np.exp(-(rr / (2 * R))**2); fin = DF(x, rr, rt, gl); f0 = grid(fin, rr, g.r[0], g.r[-1]); c = float(cflat(Mt, 0, 0)); m, k, r = worst(fin, DF(x, rr, *nfw_prof(rr, x, R, Md, Mt, c)), f0); Rs.append(m); Rk.append(k); Hi.append(r[14:].max())
Rs, Rk, Hi = np.array(Rs), np.array(Rk), np.array(Hi); b = Rs > 1.05
print(f'(c) R12 at c Diemer19: failures {b.sum()}; their worst-f0 rank median {np.median(Rk[b]):.0f}, range {Rk[b].min()}-{Rk[b].max()}, in top half of f0 {(Rk[b] >= 14).sum()}; passing the 1.05 limit over top half of f0 alone: {(Hi <= 1.05).sum()} of {len(Hi)}')
print('Diagnostic, post-result. kappa = 1/2 FITTED; not theory closed.')
