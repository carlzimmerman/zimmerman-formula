"""A42 post-result diagnostic (disclosed in ../FROZEN_A42.md, written after recipe43.out): the frozen kick rows K2/K4 ran v_k to
~750-900 km/s, where every shell's daughters escape and the kick model reduces to decay to dark radiation. This run holds v_k inside
Peter & Benson's 20-200 km/s window, where the bound (heating) branch acts, with tau free in [1, 1000] Gyr. Not a frozen grade.
Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE_ = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE_, 'recipe43.py'), encoding='utf-8').read(); src = src[:src.index('# ======================= controls')]
src = src.replace("CK = os.path.join(HERE, 'recipe43.json')", "CK = os.path.join(HERE, 'recipe43b.json')")
exec(compile(src, 'recipe43_head', 'exec'))
lv = np.log10([20., 200.])
for tag, fn, x0, lo, hi in [('K2b', lambda i, e, k: eng_kick(i, e, k[0], k[1]), [1.5, 1.7], [0., lv[0]], [3., lv[1]]),
                            ('K4b', lambda i, e, k: eng_kick(i, e, k[0], k[1], k[2], k[3]), [1.5, 1.7, 0., 0.], [0., lv[0], -.3, -.3], [3., lv[1], .3, .3])]:
    k, atb = tune(fn, x0, lo, hi, 25, list(range(len(GS)))); ko, atbo = tune(fn, x0, lo, hi, 25, EVEN)
    cur = run(fn, k); grade(f'{tag} (v_k in 20-200 km/s) tuned on all', cur, f'({len(k)} knobs {np.round(k, 3).tolist()}; at bound {atb})')
    sd, nh = g4(cur); hu = ev(ODD, run(fn, ko, ODD))
    esc = []
    for i in range(len(GS)):
        g, r, Di, dD, mbf = shells(i, E00, *(k[2:] if len(k) > 2 else (0., 0.)), NG['kick']); vc2 = G * (mbf(r) + Di) / r
        esc.append(float(dD[(10**k[1] * 1e3)**2 >= vc2].sum() / dD.sum()))
    print(f' {tag}: tau {10**k[0]:.3g} Gyr, v_k {10**k[1]:.3g} km/s, F(z=0) {Fdec(E00, k[0]):.4f}; G4 {sd:.3f} over {nh}; holdout {np.round(ko, 3).tolist()} (at bound {atbo}) unseen E1 {hu["e1"]:.4f} [{P(hu["e1"] <= .025)}]; '
          f'median escaping dark-mass share {np.median(esc):.3f}; Peter-Benson (tau <~ 30 Gyr out) {"VIOLATED" if 10**k[0] < 30 else "satisfied"}', flush=True)
# optimiser check: DR3 landed at tau 782 Gyr (decay nearly off) with E1 0.0921; restart from DR1's tau with dn, dc 0, 60 evaluations
fn, x0, lo, hi, _ = ROWS['DR3']; lg = np.log10(np.concatenate([g.gl for g in GS]))
r = least_squares(lambda k: np.log10(np.concatenate(run(fn, k))) - lg, [1.717, 0., 0.], bounds=(lo, hi), max_nfev=60, diff_step=.02)
cur = run(fn, list(r.x)); grade('DR3 restart from DR1 tau (optimiser check)', cur, f'(3 knobs {np.round(r.x, 3).tolist()}; tau {10**r.x[0]:.3g} Gyr, F(z=0) {Fdec(E00, r.x[0]):.4f})')
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
