#!/usr/bin/env python3
"""GH10 post-hoc robustness (NOT frozen): shape of the misfit, point sensitivity, r systematic, gas-mass limit."""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); EXT = os.path.join(os.path.dirname(os.path.dirname(ROOT)), "_external_data"); Z = os.path.join(EXT, "desi_dr2_ksz_zenodo", "x", "zenodo"); J = json.load(open(os.path.join(HERE, "gh10.json")))
A, B = [np.load(os.path.join(Z, f"Fig6_BGS_BRIGHT-20.2_logm{l}.npz")) for l in ("10.50", "11.00")]; w = J["w"]; T = np.array(J["Tb"]); C = (A["cov"] - (1 - w) ** 2 * B["cov"]) / w ** 2; m = np.array(J["m18"]); th = np.array(J["th"]); e = np.sqrt(np.diag(C)); R = np.array(J["R"]); RES = {}
def fit(sel):
    Ci = np.linalg.inv(C[np.ix_(sel, sel)]); s = 1 / math.sqrt(m[sel] @ Ci @ m[sel]); a = float(m[sel] @ Ci @ T[sel]) * s * s; return a, s, float((T[sel] - a * m[sel]) @ Ci @ (T[sel] - a * m[sel]))
print("theta  R_Mpc  T  err  model  T/model  (T-m)/err")
for t, r, x, s, y in zip(th, R, T, e, m): print(f"{t:5.2f} {r:5.2f} {x:6.2f} {s:6.2f} {y:6.2f} {x / y:6.2f} {(x - y) / s:+5.1f}")
al = np.ones(len(T), bool); a, s, c = fit(al); RES["all"] = (a, s, c); print(f"all: A {a:.3f}+-{s:.3f}, chi2 best {c:.1f}/12", flush=True)
for hi in (2, 2.7, 3.5, 4.3, 5.1, 6.7): a2, s2, c2 = fit(th <= hi); RES[f"le{hi}"] = (a2, s2, c2); print(f"theta <= {hi}: n {(th <= hi).sum()} A {a2:.3f}+-{s2:.3f} chi2 {c2:.1f} A+2s {a2 + 2 * s2:.3f}", flush=True)
for i in range(5):
    q = al.copy(); q[i] = False; print(f"drop theta {th[i]:.2f}: A {fit(q)[0]:.3f}+-{fit(q)[1]:.3f}", flush=True)
for sysr in (.1,):
    st = math.hypot(s, a * sysr); RES["with_r10"] = (a, st); print(f"with 10% r systematic: {a:.3f}+-{st:.3f}, A+2s {a + 2 * st:.3f}", flush=True)
# bound on M_gas(<1.8 Rvir) for the bin's corrected mass
lm = 10.75 + .19 + .031; Rv = float(np.interp(lm, [10.75, 11], [210, 295])); rr = np.linspace(.01, 1.8 * Rv, 200001); sh = (1 + (rr / 6.) ** 2) ** (-.645) * rr ** 2; ratio = np.trapz(sh, rr) / np.trapz(sh[rr <= Rv], rr[rr <= Rv]); Mneed = 1.84 * 10 ** lm * ratio; st = RES["with_r10"][1]; RES.update(lm=lm, Rv=Rv, ratio=float(ratio), Mneed=float(Mneed), Mmeas=float(a * Mneed), Mlim=float((a + 2 * st) * Mneed)); print(f"log M*corr {lm:.2f} Rvir {Rv:.0f}: M_gas(<1.8 Rvir) need {Mneed:.2e} = {Mneed / 10 ** lm:.2f} M*; measured {a * Mneed:.2e}; A+2s limit {(a + 2 * st) * Mneed:.2e}", flush=True)
json.dump(RES, open(os.path.join(HERE, "gh10_post.json"), "w"), indent=1)
