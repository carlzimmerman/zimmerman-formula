"""A38 post-result diagnostic (disclosed in ../FROZEN_A38.md), not a grade: is the FKP failure on SPARC from the solver, from the
fixed (R, v0^2), or from real baryon shapes? FKP K0 parameters on the paper's own spherical exponential baryons with each SPARC
galaxy's M_b and L = R_d, graded against the law on those same baryons at the SPARC radii. Also by epsilon = sqrt(G M_b/(C a0 L^2)).
Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe39.py'), encoding='utf-8').read()
exec(src[:src.index("print(f'A38 recipe39")]); exec(src[src.index('GK = 4.30091e-6'):src.index('# control C_K')])
def expgal(g, Ca0, R, v02):
    Mb, L = g.Mb, g.Rd / kpc; rk = g.r / kpc; s = np.sqrt(Ca0 * GK * Mb)
    Mbf = lambda r: Mb * (1 - (1 + r / L / 2 * (r / L + 2)) * np.exp(-r / L)); rhobf = lambda r: Mb * np.exp(-r / L) / (8 * np.pi * L**3)
    sol = solve_dim(rk, Mbf, rhobf, Ca0, R * s / (8 * np.pi * GK * L**2), v02 * s, L)
    gb = GK * np.array([Mbf(r) for r in rk]) / rk**2
    return np.log10((gb + GK * sol[0] / rk**2) / law(gb, A0 * AU)), np.sqrt(GK * Mb / (Ca0 * L**2)), rk[-1] / L
for tag, (Ca0, R, v02) in [('K0 (C 1/16, a0 A0, R 5.7, v0^2 1.8)', (A0 * AU / 16, 5.7, 1.8))]:
    d, ep, xl = [], [], []
    for g in GS:
        r, e, x = expgal(g, Ca0, R, v02); d.append(r); ep.append(e); xl.append(x)
    al = np.concatenate(d); per = np.array([np.sqrt((r**2).mean()) for r in d]); mn = np.array([r.mean() for r in d]); ep = np.array(ep)
    print(f'{tag} on exponential spheres (SPARC M_b, L = R_d, SPARC radii): rms to law on same baryons {np.sqrt((al**2).mean()):.4f} dex, p95 per galaxy {np.percentile(per, 95):.4f}', flush=True)
    for lo_, hi_ in [(0, 1), (1, 2), (2, 4), (4, 8), (8, 100)]:
        m = (ep >= lo_) & (ep < hi_)
        if m.sum(): print(f'   epsilon {lo_}-{hi_}: {m.sum()} galaxies, median per-galaxy mean residual {np.median(mn[m]):+.3f}, median rms {np.median(per[m]):.3f}', flush=True)
    print(f'   epsilon over SPARC: median {np.median(ep):.2f}, 5-95 {np.percentile(ep, 5):.2f}-{np.percentile(ep, 95):.2f}; paper Table 2 range {np.sqrt(GK*1e8/(Ca0*.25)):.2f}-{np.sqrt(GK*1e10/(Ca0*4)):.2f}; last radius / L median {np.median(xl):.1f}', flush=True)
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
