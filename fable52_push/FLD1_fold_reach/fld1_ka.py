#!/usr/bin/env python3
"""FLD1 known answers KA1a (static-field energy across reflections) and KA2 (Kepler shell), with the production step and
reflection kernel of fld1_shells.py (A1). KA1b, KA1c and KA3 are read from runs/ by fld1_compare.py.

    python3 fld1_ka.py -> fld1_ka.json / fld1_ka.out
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'COL1_clock_collapse'))
import col1_lib as L
G = L.G; RS = 0.3; FW = 1.2
OUT, RES = [], {}


def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def evolve(force, r, v, wall, T, ecorr=True):
    """The production kernel: global adaptive leapfrog, reflection at the wall, energy-corrected outgoing speed."""
    A = force(r); t = 0.0; nref = np.zeros(len(r), int); apo = np.zeros(len(r)); hist = []
    while t < T:
        dt = min(0.02 * np.min(r / np.maximum(np.abs(v), 1e-3)), 0.05 * np.min(np.sqrt(r / np.maximum(np.abs(A), 1e-12))), 1e-3, T - t)
        r_old, v_old = r, v
        vh = v + 0.5 * dt * A; rn = r + dt * vh; rw = wall(rn); hit = rn < rw
        if hit.any():
            rn[hit] = 2 * rw[hit] - rn[hit]; vh[hit] = np.abs(vh[hit])
        t += dt; r = rn; A = force(r); v = vh + 0.5 * dt * A
        if hit.any() and ecorr:
            idx = np.where(hit)[0]; ro, rn_ = r_old[idx], r[idx]; mid = 0.5 * (ro + rn_)
            dV = -(rn_ - ro) * (force(ro, idx) + 4 * force(mid, idx) + force(rn_, idx)) / 6
            v[idx] = np.sqrt(np.maximum(v_old[idx] ** 2 - 2 * dV, 0.0))
        nref += hit
        apo = np.where(nref > 0, np.maximum(apo, r), apo)
        hist.append((t, r.copy()))
    return r, v, nref, apo, hist


def ka1a():
    out = {}
    for f in ('canonical', 'alt'):
        a0 = L.a0_of(f); Mb = 10 ** 10.45; N = 200
        r0 = np.logspace(math.log10(3.5), 2.5, N); m = np.full(N, 3e9)
        U = lambda y: a0 * y / (a0 - np.abs(y))

        def force(x, idx=None):
            mm = m if idx is None else m[idx]
            return -G * Mb * x / (x * x + 1) ** 1.5 - G * mm / x ** 2 + U(np.clip(G * mm / x ** 2, -0.999999 * a0, 0.999999 * a0))
        wall = lambda x: np.maximum(np.sqrt(G * m / a0) * FW, RS)
        T = 13.0
        r, v, nref, apo, _ = evolve(force, r0.copy(), np.zeros(N), wall, T)
        tff = (math.pi / 2) * np.sqrt(r0 ** 3 / (2 * G * (Mb + m)))
        done = (nref > 0) & (2.2 * tff < T)                 # shells that complete an orbit well inside T
        ratio = apo[done] / r0[done]
        out[f] = {'n_complete': int(done.sum()), 'median': float(np.median(ratio)), 'max_dev': float(np.max(np.abs(ratio - 1)))}
        P(f'KA1a static field ({f}): {done.sum()} shells complete an orbit; apocentre/start median {np.median(ratio):.5f},'
          f' largest |ratio - 1| {np.max(np.abs(ratio - 1)):.2e} (lines 1e-3, 1e-2)')
    ok = all(abs(v['median'] - 1) <= 1e-3 and v['max_dev'] <= 1e-2 for v in out.values())
    return {'rows': out, 'pass': ok}


def ka2():
    M = 1e11; q = np.logspace(1, 2, 50)
    force = lambda x, idx=None: -G * M / x ** 2
    wall = lambda x: np.full(len(x), RS)
    k = np.sqrt(q ** 3 / (8 * G * M))

    def t_of_r(qq, rr):                                    # cycloid: r = q (1 + cos e)/2, t = k (e + sin e)
        e = np.arccos(2 * rr / qq - 1); return np.sqrt(qq ** 3 / (8 * G * M)) * (e + np.sin(e))
    t_rs = t_of_r(q, RS)
    T = 0.9 * (math.pi / 2) * math.sqrt(q[0] ** 3 / (2 * G * M))
    r, v, nref, apo, hist = evolve(force, q.copy(), np.zeros(len(q)), wall, T)
    def r_of_t(qq, tt):
        lo, hi = np.zeros_like(qq), np.full_like(qq, math.pi)
        for _ in range(200):
            mid = 0.5 * (lo + hi); tm = np.sqrt(qq ** 3 / (8 * G * M)) * (mid + np.sin(mid))
            lo = np.where(tm < tt, mid, lo); hi = np.where(tm < tt, hi, mid)
        return qq * (1 + np.cos(0.5 * (lo + hi))) / 2
    err_r = float(np.max(np.abs(r - r_of_t(q, T)) / r_of_t(q, T)))
    # time to reach r_s for the innermost shell, from a second run to 1.05 t(r_s)
    r2, v2, nref2, _, hist2 = evolve(force, q[:1].copy(), np.zeros(1), lambda x: np.full(len(x), RS), 1.05 * t_rs[0])
    th = next((tt for tt, rr in hist2 if rr[0] <= RS * 1.02), None)
    t_first_ref = next((hist2[i][0] for i in range(1, len(hist2)) if hist2[i][1][0] > hist2[i - 1][1][0]), None)
    err_t = abs(t_first_ref - t_rs[0]) / t_rs[0] if t_first_ref else float('nan')
    P(f'KA2 Kepler shells (M 1e11, q 10-100 kpc): max rel error of r at 0.9 t_ff(q_min) {err_r:.2e}; innermost shell reflects at'
      f' r_s after {t_first_ref:.6f} vs cycloid {t_rs[0]:.6f}: rel {err_t:.2e} (line 1e-3 each)')
    return {'max_rel_err_r': err_r, 'rel_err_t_rs': err_t, 'pass': bool(err_r <= 1e-3 and err_t <= 1e-3)}


if __name__ == '__main__':
    P('FLD1 known answers KA1a, KA2. kappa = 1/2 FITTED; not theory closed.')
    RES['KA1a'] = ka1a(); P(f'KA1a: {"PASS" if RES["KA1a"]["pass"] else "FAIL"}')
    RES['KA2'] = ka2(); P(f'KA2: {"PASS" if RES["KA2"]["pass"] else "FAIL"}')
    json.dump(RES, open(os.path.join(HERE, 'fld1_ka.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'fld1_ka.out'), 'w').write('\n'.join(OUT) + '\n\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n')
