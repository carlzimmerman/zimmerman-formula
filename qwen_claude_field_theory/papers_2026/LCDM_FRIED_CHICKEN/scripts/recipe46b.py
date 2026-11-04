"""A45 post-result diagnostic (not a gate): grid checks that the fitted minima of recipe46 are global, and the
best pure-G-boost row for comparison. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, io, contextlib
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe46.py')).read())
gt = np.log10(ALLL)
def e1(model, p): return rms(np.log10(np.concatenate(model(GS, p)[0])) - gt)
def scan(tag, model, axes):
    import itertools; best = (9, None)
    for q in itertools.product(*axes):
        e = e1(model, list(q))
        if e < best[0]: best = (e, q)
    print(f'{tag}: grid min E1 {best[0]:.4f} at {np.round(best[1], 3).tolist()}', flush=True)
scan('NL2 grid log alpha x log mu', nl, [np.linspace(-2, 3, 21), np.linspace(-4, 1, 21)])
scan('NL1 grid log lambda0', nl1, [np.linspace(-1, 3, 41)])
scan('GA1 grid log rcH0 x log B', dgp, [np.linspace(-6, 1, 29), np.linspace(-3, 1.5, 19)])
scan('HA1 grid Upsilon1', hb, [np.linspace(-2 / 3, 2, 41)])
scan('HH1 grid Upsilon1 x dn', hbh, [np.linspace(-2 / 3, 2, 17), np.linspace(-.54, .54, 11)])
scan('control: pure G boost (1+k) g_b', lambda gs, p: ([(1 + 10**p[0]) * g.gb for g in gs], None), [np.linspace(-2, 2, 81)])
scan('control: halo with dn only (Upsilon1 = 0)', hbh, [[0.], np.linspace(-.54, .54, 55)])
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
