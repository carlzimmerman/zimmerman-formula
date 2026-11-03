#!/usr/bin/env python3
"""KT16: Cassini quadrupole for filtered QUMOND (Sun's phantom sourced by its mass smoothed over xi), simple nu, KT7's integral and ceiling. python3 kt16.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import json, math, os, sys
import numpy as np
from scipy import integrate
from scipy.special import erf
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
GM = 6.6743e-11 * 1.98892e30; GEXT, CEIL = 2.32e-10, 5.2e-27; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; KPC = 3.0857e19; AU = 1.495978707e11
nu = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else (lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
def gh(r, xi):
    r = np.asarray(r, float)
    if xi <= 0: return 1 / r ** 2
    x = r / xi; small = x < 1e-3; out = np.empty_like(r)
    out[~small] = (erf(x[~small] / math.sqrt(2)) - math.sqrt(2 / math.pi) * x[~small] * np.exp(-x[~small] ** 2 / 2)) / r[~small] ** 2
    out[small] = math.sqrt(2 / math.pi) / 3 * r[small] / xi ** 3 * (1 - 0.3 * x[small] ** 2); return out
def q(eta, xi, nr=20000, nm=200, rmin=1e-7, rmax=1e5):
    u = np.linspace(math.log(rmin), math.log(rmax), nr); r = np.exp(u); mu, w = np.polynomial.legendre.leggauss(nm); g = gh(r, xi)[:, None]; M = mu[None, :]
    A = nu(np.sqrt(eta * eta + g * g + 2 * eta * g * M)) - 1; f = (A * (eta * (3 * M - 5 * M ** 3) + g * (1 - 3 * M * M))) @ w
    return 1.5 * float(np.trapz(f / r, u))
# C2
xi = 0.7; r = np.array([50.0, 1e-5]); v = gh(r, xi); e = max(abs(v[0] * r[0] ** 2 - 1), abs(v[1] / (0.26596152 * r[1] / xi ** 3) - 1)); ok = e <= 1e-6; fail += not ok; P(f"C2 smoothed field limits max rel {e:.1e}: {'PASS' if ok else 'FAIL'}")
for foot, a0 in A0.items():
    eta = GEXT / a0; rM = math.sqrt(GM / a0); pref = 1.5 * a0 / rM; qp = CEIL / pref; R = RES[foot] = dict(eta=eta, r_M_AU=rM / AU, q_pass=qp)
    if not MUT:
        ig = lambda m, vv: float((nu(math.sqrt(max(eta * eta + vv ** 4 + 2 * eta * vv * vv * m, 1e-300))) - 1) * (eta * (3 * m - 5 * m ** 3) + vv * vv * (1 - 3 * m * m)))
        qd = abs(1.5 * integrate.dblquad(ig, 0, 400.0, lambda vv: -1, lambda vv: 1, epsabs=1e-7, epsrel=1e-5)[0]); qm = abs(q(eta, 0.0, rmin=1 / 400.0)); e1 = abs(qm / qd - 1); ok = e1 <= 1e-3; fail += not ok; P(f"C1 [{foot}] xi 0, v <= 400: this {qm:.5f} vs KT7 dblquad {qd:.5f}, rel {e1:.1e}: {'PASS' if ok else 'FAIL'}")
    arms = [("plain", 0.0), ("scaled eps 0.2154", 0.2154), ("universal 2 kpc", 2 * KPC / rM)]
    for nm, x in arms:
        qq = abs(q(eta, x)); R[nm] = dict(xi_over_rM=x, xi_AU=x * rM / AU, q=qq, Q2=qq * pref, x_ceiling=qq / qp)
        P(f"[{foot}] eta {eta:.3f} r_M {rM / AU:.0f} AU; {nm}: xi/r_M {x:.4g} ({x * rM / AU:.4g} AU) q {qq:.4g} Q2 {qq * pref:.3e} = {qq / qp:.3g} x ceiling: {'PASS' if qq < qp else 'FAIL'}")
        if not MUT:
            q2 = abs(q(eta, x, nr=40000, nm=400)); e3 = abs(q2 / max(qq, 1e-300) - 1) if qq > 1e-12 else abs(q2 - qq); ok = e3 <= 1e-3; fail += not ok; P(f"    C3 doubled r and mu resolution: {q2:.4g}, change {e3:.1e}: {'PASS' if ok else 'FAIL'}")
    if not MUT:
        xs = np.geomspace(0.05, 50, 61); qs = np.array([abs(q(eta, x, nr=8000, nm=120)) for x in xs]); R["scan"] = dict(xi=xs.tolist(), q=qs.tolist())
        ok_ = xs[qs < qp]; th = None
        if len(ok_):
            lo, hi = xs[max(np.argmax(qs < qp) - 1, 0)], ok_[0]
            for _ in range(40):
                m = math.sqrt(lo * hi); (lo, hi) = (m, hi) if abs(q(eta, m)) >= qp else (lo, m)
            th = hi
        peak = float(xs[np.argmax(qs)]); R["threshold_xi_over_rM"] = th; R["q_peak_at"] = peak
        P(f"[{foot}] scan: q peaks at xi/r_M {peak:.3g} ({qs.max() / qp:.3g} x ceiling); smallest passing xi/r_M {th:.4g} ({th * rM / AU:.4g} AU) -> eps needed {th:.3g} vs MW's 0.2154" if th else f"[{foot}] no passing xi in 0.05-50 r_M")
        s = R["scaled eps 0.2154"]; R["label_scaled"] = "SCALED FILTER PASSES CASSINI" if s["x_ceiling"] < 1 else f"SCALED FILTER FAILS CASSINI ({s['x_ceiling']:.3g}x)"; u = R["universal 2 kpc"]; R["label_universal"] = "UNIVERSAL 2 kpc PASSES" if u["x_ceiling"] < 1 else f"UNIVERSAL 2 kpc FAILS ({u['x_ceiling']:.3g}x)"; P(f"LABEL [{foot}]: {R['label_scaled']}; {R['label_universal']}; plain {R['plain']['x_ceiling']:.3g}x")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt16{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt16{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)
