#!/usr/bin/env python3
"""
LMC1 DESIGN STUDY (before the freeze; purely synthetic; no star read, no LMC run).
Sets N, dt and the relaxation length: relaxes the tracers in the framework's MW field alone (census canonical)
and measures, full sky, per RAW1 bin: counts, dispersion drift over the final 2 Gyr, density slope, anisotropy;
and the statistical error of a dispersion ratio q under a synthetic uniform 30 km/s velocity offset applied
to one third of the sky (a stand-in for a reflex dipole; not the LMC).
Usage: python3 -I -B lmc1_design.py      Writes lmc1_design.out. Seeds: tracers 11, bootstrap 12, sky 13.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os
for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[k] = "1"
import sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lmc1_core as C

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
DT = 2.0; TREL = 5000.0; AOUT = float(sys.argv[2]) if len(sys.argv) > 2 else 5.5; BETA = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
OUT = open(os.path.join(HERE, "lmc1_design.out"), "w")
def say(s): print(s); OUT.write(s + "\n"); OUT.flush()
F = C.Field("FW_census", "canonical")
x, v = C.sample_tracers(F, N, 11, a_out=AOUT, beta=BETA)
p0 = np.array([-8.122, 0.0, 0.0208])
def stats(x, v):
    r = np.sqrt(np.einsum("ij,ij->i", x, x)); rh = x / r[:, None]; vr = np.einsum("ij,ij->i", v, rh) / C.KMS
    vt2 = (np.einsum("ij,ij->i", v, v) / C.KMS ** 2 - vr ** 2)
    _, n, vl = C.observe(x, v, p0)
    out = []
    for a, b in C.BINS:
        m = (r >= a) & (r < b)
        beta = 1 - np.mean(vt2[m]) / (2 * np.mean(vr[m] ** 2))
        out.append((int(m.sum()), float(np.std(vl[m])), float(beta)))
    m = (r >= 20) & (r < 80); lr = np.log(r[m])
    # ML slope of a pure power law on [20, 80)
    from scipy.optimize import minimize_scalar
    def nll(al):
        k = 3 - al; Z = (80 ** k - 20 ** k) / k if abs(k) > 1e-9 else math.log(4)
        return -(np.sum((2 - al) * lr) - m.sum() * math.log(Z))
    al = minimize_scalar(nll, bounds=(1, 9), method="bounded").x
    return out, float(al)
snaps = {int(t / DT): None for t in (0, 1000, 2000, 3000, 3500, 4000, 4500, 5000)}
res = {}
def fn(x, v): return stats(x, v)
import time
t0 = time.time()
x1, v1, res = C.integrate(F, x, v, DT, int(TREL / DT), snaps=set(snaps), snap_fn=fn)
say(f"N {N}, dt {DT} Myr, relax {TREL} Myr, initial outer slope {AOUT}, initial beta {BETA}")
print(f"wall {time.time() - t0:.1f} s")
for s in sorted(res):
    o, al = res[s]
    say(f"t {s * DT - TREL:+7.0f} Myr: alpha(20-80) {al:.3f}; " + "; ".join(f"{a:.0f}-{b:.0f}: n {nn} sig {sg:.2f} beta {bt:.3f}" for (a, b), (nn, sg, bt) in zip(C.BINS, o)))
fin = res[int(TREL / DT)][0]; mid = res[int(3000 / DT)][0]
say("drift final 2 Gyr (sig_0 / sig_-2 - 1): " + ", ".join(f"{fin[j][1] / mid[j][1] - 1:+.4f}" for j in range(4)))
# q-error stand-in: offset 30 km/s along a fixed direction for particles in one third of the sky
r, n, vl = C.observe(x1, v1, p0)
rng = np.random.default_rng(13); sky = n[:, 2] > 0.33   # about one third of the sky
dvec = np.array([0.3, -0.5, 0.8]); dvec /= np.linalg.norm(dvec)
vl2 = vl + 30.0 * (n @ dvec)
rb = np.random.default_rng(12)
for a, b in C.BINS:
    m = np.where((r >= a) & (r < b) & sky)[0]
    q = np.std(vl2[m]) / np.std(vl[m]); bs = []
    for _ in range(200):
        ii = m[rb.integers(0, len(m), len(m))]; bs.append(np.std(vl2[ii]) / np.std(vl[ii]))
    say(f"bin {a:.0f}-{b:.0f}: n(sky third) {len(m)}, synthetic q {q:.4f} +/- {np.std(bs):.4f}")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
