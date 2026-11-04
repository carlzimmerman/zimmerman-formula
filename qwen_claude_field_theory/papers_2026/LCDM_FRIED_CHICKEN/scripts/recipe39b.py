"""A38 post-result row (disclosed in ../FROZEN_A38.md): control C_F failed (spherical average of Eq. 11 gives r0/r_D 0.71, paper's
in-plane 1.4), so the paper's own stated equivalent is graded: quasi-isothermal r0 = k R_d with the 2017 BTFR normalisation
lambda R_SN = K sqrt(M_b/1e10), i.e. 4 pi rho0 r0^2 = lambda R_SN. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os
for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[v] = '1'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe39.py'), encoding='utf-8').read()
exec(src[:src.index("print(f'A38 recipe39")])
def qb(g, lamR, k):
    r0 = k * g.Rd; x = g.r / r0; return g.gb + G * lamR * r0 * (x - np.arctan(x)) / g.r**2
K20 = np.log10(np.sqrt(A0 * 1e10 * Msun / G))
rows = [('F2q (k 1.4 fixed, K)', lambda g, p: qb(g, 10**p[0] * np.sqrt(g.Mb / 1e10), 1.4), [K20], [K20 - 4], [K20 + 4]),
        ('F2qk (K, k)', lambda g, p: qb(g, 10**p[0] * np.sqrt(g.Mb / 1e10), p[1]), [K20, 1.4], [K20 - 4, .2], [K20 + 4, 10]),
        ('F3q (K, p, k)', lambda g, p: qb(g, 10**p[0] * (g.Mb / 1e10)**p[1], p[2]), [K20, .5, 1.4], [K20 - 4, 0, .2], [K20 + 4, 1.5, 10])]
for tag, fn, x0, lo, hi in rows:
    p, atb = fitg(fn, x0, lo, hi, GS); po, atbo = fitg(fn, x0, lo, hi, EVEN)
    cur = [fn(g, p) for g in GS]; show(tag + ' tuned on all', GS, cur, len(p)); sd, am, nh = g4(cur)
    hu = ev(ODD, [fn(g, po) for g in ODD]); aF = G * (10**p[0])**2 / (1e10 * Msun)
    print(f'  knobs {np.round(p, 4).tolist()} at bound {atb}; G4 rms {sd:.3f} over {nh} hosts [{P(sd <= .1)}]; holdout unseen E1 {hu["e1"]:.4f} [{P(hu["e1"] <= .025)}]; '
          f'a_F {aF / A0:.4f} A0, kappa_eff {aF / AC:.4f}', flush=True)
cur = []
for g in GS:
    l0 = np.log10(np.sqrt(A0 * g.Mb * Msun / G)); lg = np.log10(g.gl)
    r = least_squares(lambda q: np.log10(qb(g, 10**q[0], q[1])) - lg, [l0, 1.4], bounds=([l0 - 4, .05], [l0 + 4, 30]), diff_step=1e-4); cur.append(qb(g, 10**r.x[0], r.x[1]))
show('F5q per galaxy lamR_i, k_i (342 params)', GS, cur, 342)
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
