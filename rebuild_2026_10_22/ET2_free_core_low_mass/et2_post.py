#!/usr/bin/env python3
"""ET2 POST-RESULT diagnostics, not in the frozen criteria: why K2 and the guard failed, and whether fit degeneracy can fake the rise. kappa = 1/2 FITTED; not theory closed."""
import os, sys
HERE0 = os.path.dirname(os.path.abspath(__file__)); SRC2 = open(os.path.join(HERE0, "et2_free.py")).read()
__file__ = os.path.join(HERE0, "et2_free.py"); exec(compile(SRC2[:SRC2.index('P(f"ET2 free')], "et2_head", "exec"))
L = []
def W(s): print(s, flush=True); L.append(s)
iu = I05; q = sel(100, 150)[0]
W("A. K2 with on-grid plants, same galaxy")
for i, j in ((61, 15), (89, 19), (117, 27)):
    a, b, _, _ = fit(q, iu, np.log10(np.maximum(q["GB"][:, iu] + gh(q, SG[i], RG[j]), 1e-300))); W(f" plant ({SG[i]:.1f}, {RG[j] / KPC:.2f}) -> ({a:.1f}, {b / KPC:.2f})")
W("B. mse scale, why Delta = 1/N_eff admits everything, and a relative guard (mse <= 1.25 x min, S span < 0.5 dex)")
rows = []
for g in SAMPLE:
    T, n = surface(g, iu); i, j = np.unravel_index(np.argmin(T), T.shape); s = np.where(T <= 1.25 * T[i, j])[0]
    rows.append((SG[i], RG[j], T[i, j], 1 / max(n, 1), np.log10(SG[s.max()] / SG[s.min()]) < 0.5))
S = np.array([r[0] for r in rows]); R0 = np.array([r[1] for r in rows]); MS = np.array([r[2] for r in rows]); D = np.array([r[3] for r in rows]); C = np.array([r[4] for r in rows])
W(f" median min mse {np.median(MS):.4f} dex^2; median Delta {np.median(D):.4f}; relative guard passes {C.sum()}/{len(C)}, below 150 km/s {(C & (Vf < 150)).sum()}/{(Vf < 150).sum()}")
rng = np.random.default_rng(RS)
for lo, hi in BINS[:3]:
    m = C & (Vf >= lo) & (Vf < hi); W(f" {lo}-{hi}: constrained n {m.sum()} S {np.median(S[m]) if m.sum() else None} {boot(S[m], rng) if m.sum() > 1 else None}")
m = C & (Vf < 150); W(" constrained rise rho %+.3f p %.4f" % spear(m, S)[:2])
W("C. flat truth S = 100 plus each galaxy's own real residuals, shuffled over its points; 8 seeds")
res = {}
for g, s, r in zip(SAMPLE, S, R0):
    ok = g["OK"][:, iu]; res[g["name"]] = (np.log10(g["GO"]) - np.log10(np.maximum(g["GB"][:, iu] + gh(g, s, r), 1e-300)))[ok]
for sd in range(8):
    pr = np.random.default_rng(RS + sd); Sf = []
    for g in SAMPLE:
        go = np.log10(np.maximum(g["GB"][:, iu] + gh(g, 100.0, r0_et1(g, 100.0)), 1e-300)).copy(); ok = g["OK"][:, iu]; go[ok] += pr.permutation(res[g["name"]]); Sf.append(fit(g, iu, go)[0])
    Sf = np.array(Sf); rho, p, v = spear(Vf < 150, Sf); W(f" seed {sd}: medians {[round(float(np.median(Sf[(Vf >= l) & (Vf < h)])), 1) for l, h in BINS[:3]]} rho {rho:+.3f} p {p:.4f} {v}")
open(os.path.join(HERE0, "et2_post.out"), "w").write("\n".join(L) + "\n")
