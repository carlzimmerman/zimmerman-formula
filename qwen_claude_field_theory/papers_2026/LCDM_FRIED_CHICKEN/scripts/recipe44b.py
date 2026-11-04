"""A43 post-result diagnostic (written after recipe44.out, disclosed in ../FROZEN_A43.md): the frozen (a) rows floor
g_b + eta g_gas at 1e-3 g_b where SPARC's V_gas^2 < 0 (central HI holes), which costs about -3 dex per floored point.
Here: (i) the frozen rows' E1 with floored points excluded; (ii) rival-favourable variant, dark term clipped at zero
(eta max(g_gas, 0), so the dark gas never pulls outward), refitted. Not a frozen grade.
Rival language, adopts nothing, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe44.py'), encoding='utf-8').read()
exec(src[:src.index("RES = {}")])
RES = {}; SUN_ETA = 20 / 13.7
def hraw(g, eta, eps=0.): return g.gb + eta * g.ggas + eps * g.gst
def hclip(g, eta, eps=0.): return g.gb + eta * np.maximum(g.ggas, 0.) + eps * g.gst
def e1x(eta, eps=0.):
    d = []
    for g in GS:
        gt = hraw(g, eta, eps); ok = gt >= 1e-3 * g.gb; d.append(np.log10(gt[ok]) - np.log10(g.gl[ok]))
    d = np.concatenate(d); return float(np.sqrt((d**2).mean())), len(d)
for tag, eta, eps in [('H0 eta 7', 7., 0.), ('H1 eta 7.1363', 7.1363, 0.), ('H2 eta 4.8971 eps 1.0412', 4.8971, 1.0412)]:
    e, nn = e1x(eta, eps); print(f'(i) {tag}: E1 excluding floored points {e:.4f} over {nn} points [{P(e <= .02)}]', flush=True)
print('\n(ii) dark term clipped at zero, refitted', flush=True)
def fitC(gsl, x0, lo, hi, two):
    lg = np.log10(np.concatenate([g.gl for g in gsl]))
    res = lambda k: np.log10(np.concatenate([hclip(g, k[0], k[1] if two else 0.) for g in gsl])) - lg
    r = least_squares(res, x0, bounds=(lo, hi), diff_step=1e-4); return r.x
cur = [hclip(g, 7.) for g in GS]; show('C0 eta 7 clipped (0 fitted)', GS, cur, 0)
for tag, two, x0, lo, hi in [('C1 global eta clipped', False, [7.], [0.], [50.]), ('C2 global eta + eps clipped', True, [7., .5], [0., 0.], [50., 10.])]:
    p = fitC(GS, x0, lo, hi, two); cur = [hclip(g, p[0], p[1] if two else 0.) for g in GS]; r = show(tag, GS, cur, len(p))
    po = fitC(EVEN, x0, lo, hi, two); hu = ev(ODD, [hclip(g, po[0], po[1] if two else 0.) for g in ODD])
    sd, am, nh = g4(cur)
    print(f'  knobs {np.round(p, 4).tolist()}; holdout unseen E1 {hu["e1"]:.4f} [{P(hu["e1"] <= .025)}]; G4 {sd:.3f} [{P(sd <= .1)}]; C_loc eta x 13.7 = {p[0] * 13.7:.1f} vs 20 [{P(p[0] <= SUN_ETA)}]', flush=True)
for tag, two in [('C3 per-galaxy eta clipped (171)', False), ('C4 per-galaxy eta + eps clipped (342)', True)]:
    pk = []
    for g in GS:
        lg = np.log10(g.gl)
        r = least_squares(lambda k: np.log10(hclip(g, k[0], k[1] if two else 0.)) - lg, [7., .5] if two else [7.], bounds=([0., 0.] if two else [0.], [200., 20.] if two else [200.]), diff_step=1e-4)
        pk.append(r.x)
    pk = np.array(pk); cur = [hclip(g, q[0], q[1] if two else 0.) for g, q in zip(GS, pk)]; show(tag, GS, cur, 171 * (2 if two else 1))
    sd, am, nh = g4(cur)
    print(f'  eta median {np.median(pk[:, 0]):.2f} (16-84 {np.percentile(pk[:, 0], 16):.2f}-{np.percentile(pk[:, 0], 84):.2f}); fraction eta <= {SUN_ETA:.2f}: {(pk[:, 0] <= SUN_ETA).mean():.3f}; G4 {sd:.3f}', flush=True)
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
