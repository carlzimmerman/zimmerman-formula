"""A22 post-result diagnostic (not a gate): optimiser check of N3m, m on a grid, per ../FROZEN_A22.md.
recipe24's bounded scalar search on all data stopped at m 4.75 eV (0.1419) while the GS[::2]-tuned m 0.193 eV scored 0.0767 unseen,
so the all-data N3m minimum was local. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe24.py')).read().split('# ---------------- (a)')[0]
exec(src)
LD = RDEN**.25; aN3 = (.5 / kap(1., LD))**(1 / 3); best = None
print(f'N3 grid: Lambda^4 = rho_DE, alpha {aN3:.3f} by hand, m on 21 log steps 0.1 to 10 eV, dn 0')
for lm in np.linspace(-1, 1, 21):
    x = np.array([np.log10(aN3), np.log10(LD * 1e3), lm, 0.]); cu, inf, S, sol = model(x)
    ra, re, ro = rms_on(cu, ALL), rms_on(cu, EV), rms_on(cu, OD); fin = sum(int(round(i[0] * len(g.r))) for g, i in zip(GS, inf)) / len(ALLB)
    print(f' m {10**lm:7.3f} eV: rms all {ra:.4f}, even {re:.4f}, odd {ro:.4f}; inside R_NFW {fin:.3f}; median R_NFW {np.nanmedian(sol[4]) / kpc:.1f} kpc')
    if best is None or ra < best[0]: best = (ra, lm)
x = np.array([np.log10(aN3), np.log10(LD * 1e3), best[1], 0.]); cu, inf, S, sol = model(x)
report(f'(N3 grid best on all) m {10**best[1]:.3g} eV', x, cu, inf, S, sol, '1 knob m from the grid; alpha by hand')
print('Rival language. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.')
