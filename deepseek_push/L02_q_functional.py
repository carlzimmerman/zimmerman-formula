#!/usr/bin/env python3
"""
L02 -- CLOSE THE Q-FUNCTIONAL: does E[Q](tau0, q) have a closed form?
2026-09-23.  Continuation of J02 on the volume-source face.

Q := sum_j ell_j (u_j . u_final) = (x_tau - x_0) . u_final  (per photon, exact),
u_final = u_N = direction of the last (escape) flight, N = #collisions.

(1) MEASURE E[Q] on the grid tau0 in {0.3, 0.5, 1, 2, 3} x q in {0, 3, 10}
    (volume AND central), n = 1.5e5 per config, plus the per-collision
    decomposition  <Q/N>, E[Q/(N+1)], E[l_N], E[Q - l_N], and the
    per-segment direction diagnostics (the mixing law).
(2) Candidate closed forms: a*tau0*(1+q/3)/(1+q*b)+c (a = 3/8, 1/2, ...),
    (1/2)(1 - E[mu_exit]^2), E[tau]-type, rational/quadratic Pad(e) library;
    best residual per family in SE units.
(3) Derive route: exact facts (E[u_j . u_N] = 0 for j<N via E[mu]=0),
    the exchangeability obstruction proof, and the geometric mixing law
    E[(u_j . u_N)^2] = 1/3 + (2/3)(3/10)^{N-j} -- tested empirically.
(4) Honest exit: MEASURED-ONLY registration with kill condition (any claimed
    closed form must reproduce the table within 3 SE).

Engine: bit-identical RNG stream to J02.simulate_Q (imported kernels
thomson_mu / rate_integral); Q computed both ways (definitional sum and
X . u_final) and cross-checked.
"""
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from J02_moment_hierarchy import rate_integral, se, simulate, thomson_mu

OUT = "L02_results.json"


def measure(tau0, q, src, n, seed, with_segs=False):
    """Same trajectory as J02.simulate_Q on the same seed. Returns per-photon
    arrays: Q (definitional sum), X = (x-x0).u_final, N, last_l, tau, v2,
    and (optional) aggregated per-segment diagnostics for volume q=0 runs."""
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    if src == "volume":
        d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
        pos = d0 * rng.random(n)[:, None] ** (1 / 3)
    origin = pos.copy()
    d = rng.normal(size=(n, 3)); direc = d / np.linalg.norm(d, axis=1)[:, None]
    elapsed = np.zeros(n)
    S = np.zeros((n, 3))                  # running sum_j l_j u_j
    slens = [[] for _ in range(n)]
    sdirs = [[] for _ in range(n)] if with_segs else None
    alive = np.arange(n); steps = 0
    while len(alive):
        steps += 1
        if steps > 100000:
            raise RuntimeError("cap")
        p, u = pos[alive], direc[alive]
        pd = np.sum(p * u, axis=1)
        r2 = np.sum(p * p, axis=1)
        disc = pd * pd - r2 + 1.0
        wall = -pd + np.sqrt(np.maximum(disc, 0.0))
        U = rng.random(len(alive))
        tw = rate_integral(r2, pd, wall, tau0, q)
        esc = tw <= -np.log(U)
        s = wall.copy()
        inner = ~esc
        if inner.any():
            lo = np.zeros(inner.sum()); hi = wall[inner]
            Ui = U[inner]; r2i = r2[inner]; pdi = pd[inner]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                val = rate_integral(r2i, pdi, mid, tau0, q) + np.log(Ui)
                tak = val < 0
                lo[tak] = mid[tak]; hi[~tak] = mid[~tak]
            s[inner] = 0.5 * (lo + hi)
        elapsed[alive] += s
        pos[alive] += u * s[:, None]
        S[alive] += u * s[:, None]
        for i, idx in enumerate(alive):
            slens[idx].append(float(s[i]))
            if with_segs:
                sdirs[idx].append(u[i].copy())
        alive = alive[~esc]
        if len(alive) == 0:
            break
        p, u = pos[alive], direc[alive]
        r2 = np.sum(p * p, axis=1)
        mu = thomson_mu(rng, len(alive))
        t = rng.normal(size=(len(alive), 3))
        t -= np.sum(t * u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1)
        t = t / tn[:, None]
        newu = u * mu[:, None] + t * np.sqrt(1 - mu * mu)[:, None]
        direc[alive] = newu
    uf = direc.copy()                                # u_N per photon
    Q = np.sum(S * uf, axis=1)
    X = np.sum((pos - origin) * uf, axis=1)
    N = np.array([len(l) - 1 for l in slens])
    last_l = np.array([l[-1] for l in slens])
    prof = None
    if with_segs:
        # per-segment diagnostics: k = N - j (0 = final/escape segment)
        from collections import defaultdict
        acc = defaultdict(list)
        for i in range(n):
            dseg = np.array(sdirs[i]) @ uf[i]
            lseg = np.array(slens[i])
            kk = N[i] - np.arange(len(lseg))          # N - j
            for k, dd, ll in zip(kk.tolist(), dseg.tolist(), lseg.tolist()):
                acc[k].append((dd, ll))
        ks = sorted(acc)
        prof = dict(k=list(ks),
                    count=[len(acc[k]) for k in ks],
                    Ed2=[float(np.mean([a[0] * a[0] for a in acc[k]])) for k in ks],
                    Eld=[float(np.mean([a[1] * a[0] for a in acc[k]])) for k in ks],
                    Ed=[float(np.mean([a[0] for a in acc[k]])) for k in ks])
    return dict(Q=Q, X=X, N=N, last_l=last_l, tau=elapsed, prof=prof)


def mu_exit_estimator(tau0, q, n, seed):
    """E[mu at escape face], same RNG stream as measure()."""
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
    pos = d0 * rng.random(n)[:, None] ** (1 / 3)
    direc = rng.normal(size=(n, 3))
    direc = direc / np.linalg.norm(direc, axis=1)[:, None]
    mus = np.zeros(n); al = np.arange(n)
    while len(al):
        p, u = pos[al], direc[al]
        pd = np.sum(p * u, axis=1); r2 = np.sum(p * p, axis=1)
        disc = pd * pd - r2 + 1.0
        wall = -pd + np.sqrt(np.maximum(disc, 0.0))
        U = rng.random(len(al))
        esc = rate_integral(r2, pd, wall, tau0, q) <= -np.log(U)
        s = wall.copy()
        inner = al[~esc]
        if len(inner):
            p2, u2 = pos[inner], direc[inner]
            pd2 = np.sum(p2 * u2, axis=1); r22 = np.sum(p2 * p2, axis=1)
            lo = np.zeros(len(inner)); hi = wall[~esc]
            Ui = U[~esc]; r2i = r22; pdi = pd2
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                val = rate_integral(r2i, pdi, mid, tau0, q) + np.log(Ui)
                tak = val < 0
                lo[tak] = mid[tak]; hi[~tak] = mid[~tak]
            s[~esc] = 0.5 * (lo + hi)
        pos[al] += direc[al] * s[:, None]
        esc_idx = al[esc]
        xh = pos[esc_idx] / np.linalg.norm(pos[esc_idx], axis=1)[:, None]
        mus[esc_idx] = np.sum(xh * direc[esc_idx], axis=1)
        al = al[~esc]
        if len(al) == 0:
            break
        p, u = pos[al], direc[al]
        r2 = np.sum(p * p, axis=1)
        mu = thomson_mu(rng, len(al))
        t = rng.normal(size=(len(al), 3))
        t -= np.sum(t * u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1); t = t / tn[:, None]
        direc[al] = u * mu[:, None] + t * np.sqrt(1 - mu * mu)[:, None]
    return mus


def run_config(cfg):
    tau0, q, src, n, seed = cfg
    with_segs = (src == "volume" and q == 0.0)
    r = measure(tau0, q, src, n, seed, with_segs)
    mus = mu_exit_estimator(tau0, q, n, seed + 1000)
    Q, X, N, ll, tau = r["Q"], r["X"], r["N"], r["last_l"], r["tau"]
    Tless = Q - ll                       # sum over the N non-final segments
    D = tau - Q
    m = {}
    m["tau0"], m["q"], m["src"], m["n"] = tau0, q, src, n
    m["E_Q"] = float(np.mean(Q));  m["s_Q"] = se(Q)
    m["E_tau"] = float(np.mean(tau)); m["s_tau"] = se(tau)
    m["E_D"] = float(np.mean(D))
    m["E_N"] = float(np.mean(N));  m["s_N"] = se(N.astype(float))
    m["E_Q_over_N"] = float(np.mean(Q / np.maximum(N, 1.0)))
    m["E_Q_over_Np1"] = float(np.mean(Q / (N + 1.0)))
    m["E_lN"] = float(np.mean(ll));  m["s_lN"] = se(ll)
    m["E_Tless"] = float(np.mean(Tless)); m["s_Tless"] = se(Tless)
    m["E_Tless_over_N"] = float(np.mean(Tless / np.maximum(N, 1.0)))
    m["E_mu_exit"] = float(np.mean(mus)); m["s_mu"] = se(mus)
    m["max_book_err"] = float(np.max(np.abs(Q - X)))
    m["prof"] = r["prof"] if r["prof"] else None
    return m


TAUS = [0.3, 0.5, 1.0, 2.0, 3.0]
QS = [0.0, 3.0, 10.0]
NPH = 150000
SEED0 = 20260923


def make_grid():
    cfgs = []
    sid = SEED0
    for src in ("volume", "central"):
        for q in QS:
            for t0 in TAUS:
                cfgs.append((t0, q, src, NPH, sid))
                sid += 1
    cfgs.append((0.1, 0.0, "volume", 150000, sid)); sid += 1   # tau0->0 slope
    cfgs.append((0.1, 0.0, "central", 150000, sid)); sid += 1
    cfgs.append((0.05, 0.0, "volume", 150000, sid)); sid += 1  # tau0->0 limit probe
    cfgs.append((8.0, 0.0, "volume", 150000, sid)); sid += 1   # tau0->inf probe
    # anchor config: same seed (41) as J02 B4 so the photons are bit-identical
    for i, c in enumerate(cfgs):
        if c[0] == 1.0 and c[1] == 0.0 and c[2] == "volume":
            cfgs[i] = (c[0], c[1], c[2], c[3], 41)
    return cfgs, sid


# ----------------------------------------------------------------- fits ----
def fit_report(tab, fam, share=True):
    """tab: list of dicts (volume rows).  Return (max|resid|/SE, rms/SE,
    params-txt).  fam keys: 'a' list or None(free), 'c_if' bool offset, etc."""
    t0 = np.array([r["tau0"] for r in tab])
    q = np.array([r["q"] for r in tab])
    y = np.array([r["E_Q"] for r in tab])
    w = 1.0 / np.array([r["s_Q"] for r in tab])
    def resid(X, NAMES):
        coef, *_ = np.linalg.lstsq(X * w[:, None], y * w, rcond=None)
        r = (X @ coef - y) * w
        return r, coef, NAMES
    name = fam["name"]
    if name == "F1":            # a*tau0*A(q)/(1+qb)+c ; A=1+q/3
        A = 1 + q / 3.0
        best = None
        for b in np.linspace(0.01, 3.0, 400):
            if fam.get("a"):
                X = np.stack([fam["a"] * t0 * A / (1 + q * b),
                              np.ones_like(q)], 1)
                r, coef, N = resid(X, ["c"])
            else:
                X = np.stack([t0 * A / (1 + q * b), np.ones_like(q)], 1)
                r, coef, N = resid(X, ["a", "c"])
            mx = np.max(np.abs(r)); rms = float(np.sqrt(np.mean(r ** 2)))
            if best is None or (mx, rms) < best[:2]:
                best = (mx, rms, b, r, coef)
        txt = f"b={best[2]:.4f} coef={np.round(best[4], 4)}"
        return best[0], best[1], txt
    if name == "F2":            # a*tau0*A(q)/(1+qb), no offset
        A = 1 + q / 3.0
        best = None
        for b in np.linspace(0.0, 3.0, 400):
            X = np.stack([t0 * A / (1 + q * b)], 1)
            r, coef, N = resid(X, ["a"])
            mx = np.max(np.abs(r)); rms = float(np.sqrt(np.mean(r ** 2)))
            if best is None or (mx, rms) < best[:2]:
                best = (mx, rms, b, r, coef)
        return best[0], best[1], f"b={best[2]:.4f} a={best[4][0]:.5f}"
    if name == "F3":            # a*tau0/(1+b*tau0) * A(q)/(1+cq), no offset
        A = 1 + q / 3.0
        best = None
        for b in np.linspace(0.0, 3.0, 60):
            for c in np.linspace(0.0, 2.0, 60):
                X = np.stack([t0 / (1 + b * t0) * A / (1 + c * q)], 1)
                r, coef, N = resid(X, ["a"])
                mx = np.max(np.abs(r)); rms = float(np.sqrt(np.mean(r ** 2)))
                if best is None or (mx, rms) < best[:2]:
                    best = (mx, rms, b, c, r, coef)
        return best[0], best[1], f"b={best[2]:.3f} c={best[3]:.3f} a={best[5][0]:.5f}"
    if name == "F4":            # quadratic in tau0: (a t0 + b t0^2) A(q)/(1+cq)
        A = 1 + q / 3.0
        best = None
        for c in np.linspace(0.0, 2.0, 100):
            X = np.stack([t0 * A / (1 + c * q), t0 ** 2 * A / (1 + c * q)], 1)
            r, coef, N = resid(X, ["a", "b"])
            mx = np.max(np.abs(r)); rms = float(np.sqrt(np.mean(r ** 2)))
            if best is None or (mx, rms) < best[:2]:
                best = (mx, rms, c, r, coef)
        return best[0], best[1], f"c={best[2]:.4f} a={best[4][0]:.5f} b={best[4][1]:.5f}"
    if name == "F5":            # separable f(tau0)*g(q) with general Pade g
        utaus = sorted(set(t0.tolist()))
        best = None
        for a_ in np.linspace(0.0, 2.0, 60):
            for b in np.linspace(0.0, 2.0, 60):
                g = (1 + a_ * q) / (1 + b * q)
                X = np.stack([(t0 == tt) * g for tt in utaus], 1)
                r, coef, N = resid(X, [f"f({t})" for t in utaus])
                mx = np.max(np.abs(r)); rms = float(np.sqrt(np.mean(r ** 2)))
                if best is None or (mx, rms) < best[:2]:
                    best = (mx, rms, a_, b, r, coef)
        return best[0], best[1], f"alpha={best[2]:.3f} beta={best[3]:.3f} f={np.round(best[5],4)}"
    if name == "F6":            # saturating: (3/4)(1+aq)/(1+b t0 + c q)  [E[Q]->3/4 as t0->0]
        best = None
        for b in np.linspace(0.0, 3.0, 80):
            for c in np.linspace(0.0, 2.0, 80):
                den = 1 + b * t0 + c * q
                X = np.stack([0.75 / den, 0.75 * q / den], 1)   # [1, a]
                r, coef, N = resid(X, ["1", "a"])
                mx = np.max(np.abs(r)); rms = float(np.sqrt(np.mean(r ** 2)))
                if best is None or (mx, rms) < best[:2]:
                    best = (mx, rms, b, c, r, coef)
        return best[0], best[1], f"b={best[2]:.3f} c={best[3]:.3f} a={best[5][1]:.5f}"
    if name == "F7":            # + q-t0 interaction: (3/4)(1+aq)/(1+b t0 + c q + d q t0)
        best = None
        for b in np.linspace(0.0, 3.0, 35):
            for c in np.linspace(0.0, 2.0, 35):
                for d in np.linspace(0.0, 2.0, 35):
                    den = 1 + b * t0 + c * q + d * q * t0
                    X = np.stack([0.75 / den, 0.75 * q / den], 1)
                    r, coef, N = resid(X, ["1", "a"])
                    mx = np.max(np.abs(r)); rms = float(np.sqrt(np.mean(r ** 2)))
                    if best is None or (mx, rms) < best[:2]:
                        best = (mx, rms, b, c, d, r, coef)
        return best[0], best[1], f"b={best[2]:.2f} c={best[3]:.2f} d={best[4]:.2f} a={best[6][1]:.4f}"
    raise KeyError(name)


def main():
    t0all = time.time()
    grid, _ = make_grid()
    print(f"grid: {len(grid)} configs x n={NPH}  (volume+central, tau0 in {TAUS}, q in {QS})",
          flush=True)
    with ProcessPoolExecutor(max_workers=12) as ex:
        res = list(ex.map(run_config, grid))
    vol = [r for r in res if r["src"] == "volume"]
    cen = [r for r in res if r["src"] == "central"]

    # ---- J02 anchor cross-check ------------------------------------------
    a1 = next(r for r in vol if r["tau0"] == 1.0 and r["q"] == 0.0)
    print(f"\nanchor (tau0=1,q=0,volume): E[Q]={a1['E_Q']:.6f} +/- {a1['s_Q']:.6f}"
          f"  J02: 0.5971526  dz={abs(a1['E_Q']-0.5971526)/a1['s_Q']:.1f} SE")
    print(f"max |Q-X| bookkeeping over all runs: "
          f"{max(r['max_book_err'] for r in res):.2e}  (must be <1e-9)")
    # E[v^2] = 2 E[N] is exact (conditional Gaussian kick variance 2*ang,
    # E[ang]=E[N]); verify once on the J02 velocity engine.
    rv = simulate(100000, 1.0, 0.0, "volume", 7)
    dv2 = rv["v2"] - 2.0 * rv["N"]
    dev2 = float(np.mean(dv2))
    v2ok = abs(dev2) < 6.0 * se(dv2)
    print(f"E[v^2] - 2 E[N] (exact identity), J02 engine check: {dev2:.2e} "
          f"+/- {se(dv2):.2e}  -> {v2ok}")

    # ---- table -------------------------------------------------------------
    def show(rows, label, keys):
        print(f"\n=== {label} ===")
        hdr = ("tau0   q    E_Q     s_Q    E_N    E_tau    E_D    E_mu_exit  "
               "E_lN    E<Tless>  <Q/N>  <Q/(N+1)>")
        print(hdr)
        for r in sorted(rows, key=lambda r: (r["q"], r["tau0"])):
            print(f"{r['tau0']:5.1f} {r['q']:4.0f} {r['E_Q']:8.5f} {r['s_Q']:8.5f} "
                  f"{r['E_N']:6.3f} {r['E_tau']:8.4f} {r['E_D']:8.4f} "
                  f"{r['E_mu_exit']:8.4f} {r['E_lN']:8.4f} {r['E_Tless']:9.5f} "
                  f"{r['E_Q_over_N']:8.5f} {r['E_Q_over_Np1']:9.5f}")

    show(vol, "VOLUME grid (incl. tau0=0.1 slope probe)", None)
    show(cen, "CENTRAL grid", None)

    # profile check (empirical mixing law), volume q=0
    print("\n=== direction-chain mixing law: E[d_j^2 | k] vs 1/3 + (2/3)(3/10)^k (k=N-j) ===")
    for r in sorted(vol, key=lambda r: r["tau0"]):
        pr = r["prof"]
        if not pr:
            continue
        line = f"tau0={r['tau0']}: "
        for k, e2, nk in zip(pr["k"], pr["Ed2"], pr["count"]):
            pred = 1 / 3 + (2 / 3) * (0.3 ** k)
            line += f"k={k}: E[d2]={e2:.4f} (pred {pred:.4f}, n={nk})  "
        print(line)

    # ---- candidate library ---------------------------------------------------
    tbl = [dict(r) for r in vol]
    print("\n=== CANDIDATE CLOSED FORMS (volume grid: 16 pts incl. tau0=0.1) ===")
    rows16 = tbl
    families = [
        dict(name="F1", a=0.5), dict(name="F1", a=3 / 8), dict(name="F1", a=3 / 4),
        dict(name="F1", a=None), dict(name="F2"), dict(name="F3"), dict(name="F4"),
        dict(name="F5"), dict(name="F6"), dict(name="F7"),
    ]
    out = {"families": {}}
    for fam in families:
        mx, rms, txt = fit_report(rows16, fam)
        lbl = f"F1 a={fam['a']}" if fam["name"] == "F1" else fam["name"]
        out["families"][lbl] = {"max_resid_SE": round(mx, 2),
                                "rms_resid_SE": round(rms, 2), "params": txt}
        print(f"{lbl:12s}: max|resid|/SE = {mx:7.2f}   rms/SE = {rms:6.2f}   [{txt}]")

    # zero-free-parameter named candidates
    print("\n=== ZERO-FREE-PARAMETER NAMED CANDIDATES ===")
    named = {}
    for r in rows16:
        t, q, y, s = r["tau0"], r["q"], r["E_Q"], r["s_Q"]
        A = 1 + q / 3.0
        cand = {
            "(3/5) t0 A/(1+q/2)": 0.6 * t * A / (1 + q / 2),
            "(1/2)(1-muE^2)": 0.5 * (1 - r["E_mu_exit"] ** 2),
            "E_tau (1-muE^2)": r["E_tau"] * (1 - r["E_mu_exit"] ** 2),
            "E_tau muE^2": r["E_tau"] * r["E_mu_exit"] ** 2,
            "E_tau - 1/2": r["E_tau"] - 0.5,
            "(1/2)E_tau": 0.5 * r["E_tau"],
            "E_tau*(1-muE^2)*4/3": r["E_tau"] * (1 - r["E_mu_exit"] ** 2) * 4 / 3,
            "(3/4) t0 A/(1+q/2)": 0.75 * t * A / (1 + q / 2),
            "(3/5) t0": 0.6 * t,
        }
        for k, v in cand.items():
            named.setdefault(k, []).append(abs(v - y) / s)
    for k, rr in sorted(named.items(), key=lambda kv: (max(kv[1]), kv[0])):
        out.setdefault("named", {})[k] = {"max_SE": round(max(rr), 2),
                                          "mean_SE": round(float(np.mean(rr)), 2)}
        print(f"{k:32s}: max_SE={max(rr):7.2f}  mean_SE={np.mean(rr):6.2f}")

    # tau0 -> 0 limit probe (E[Q] -> E[l_0] = 3/4 by the chord-length bias
    # argument; E[Q]/tau0 -> +inf is NOT the right statement, the limit of
    # E[Q] itself is 3/4 since the unscattered first flight dominates)
    r01 = next(r for r in vol if r["tau0"] == 0.1)
    r005 = next(r for r in vol if r["tau0"] == 0.05)
    r8 = next(r for r in vol if r["tau0"] == 8.0)
    print(f"\ntau0->0 probes: E[Q](0.05,0)={r005['E_Q']:.5f}+/-{r005['s_Q']:.5f} "
          f" E[Q](0.1,0)={r01['E_Q']:.5f}+/-{r01['s_Q']:.5f}"
          f"  [limit E[l_0]=3/4]")
    print(f"tau0->8 probe: E[Q](8,0)={r8['E_Q']:.5f}+/-{r8['s_Q']:.5f}"
          f"  E[N]={r8['E_N']:.1f}  E[l_N]={r8['E_lN']:.5f}")
    # q-scalings at tau0=1
    print("q-dependence at tau0=1 (volume): ratios E_Q(q)/E_Q(0):")
    r0 = next(r for r in vol if r["tau0"] == 1.0 and r["q"] == 0.0)
    for r in vol:
        if r["tau0"] == 1.0:
            print(f"   q={r['q']:4.0f}: {r['E_Q']/r0['E_Q']:.5f}  "
                  f"((1+q/3)/(1+q/2)={(1+r['q']/3)/(1+r['q']/2):.5f}, "
                  f"1/(1+q/9)={1/(1+r['q']/9):.5f})")
    # pointwise b-consistency of the shape (1+q/3)/(1+q b), per tau0 row
    print("\nshape (1+q/3)/(1+q b): implied b from q=3 vs q=10 per tau0 row (volume):")
    for t in [0.3, 0.5, 1.0, 2.0, 3.0]:
        r0t = next(r for r in vol if r["tau0"] == t and r["q"] == 0.0)
        r3 = next(r for r in vol if r["tau0"] == t and r["q"] == 3.0)
        r10 = next(r for r in vol if r["tau0"] == t and r["q"] == 10.0)
        b3 = ((1 + 3 / 3) / (r3["E_Q"] / r0t["E_Q"]) - 1) / 3.0
        b10 = ((1 + 10 / 3) / (r10["E_Q"] / r0t["E_Q"]) - 1) / 10.0
        s3 = b3 * np.sqrt((r3["s_Q"] / r3["E_Q"]) ** 2 + (r0t["s_Q"] / r0t["E_Q"]) ** 2)
        s10 = b10 * np.sqrt((r10["s_Q"] / r10["E_Q"]) ** 2 + (r0t["s_Q"] / r0t["E_Q"]) ** 2)
        z = (b3 - b10) / np.sqrt(s3 * s3 + s10 * s10)
        print(f"   tau0={t}: b(q=3)={b3:.3f}+/-{s3:.3f}  b(q=10)={b10:.3f}+/-{s10:.3f}"
              f"  diff {abs(b3-b10):.3f} = {abs(z):.1f} SE")

    # ---- verdict -------------------------------------------------------------
    best = min(out["families"].values(), key=lambda f: f["max_resid_SE"])
    named_ok = [k for k, v in out.get("named", {}).items() if v["max_SE"] <= 3.0]
    if named_ok:
        verdict = ("CLOSED-FORM-CONFIRMED: zero-free-parameter candidate "
                   f"{named_ok} reproduces table within 3 SE")
    elif best["max_resid_SE"] <= 3.0:
        verdict = ("FITTED-FORM-ONLY: best fitted family reaches "
                   f"{best['max_resid_SE']} SE but parameters are data-fitted, "
                   "not algebraic -- registering E[Q] as MEASURED-ONLY")
    else:
        verdict = ("MEASURED-ONLY: best family residual "
                   f"{best['max_resid_SE']:.1f} SE > 3 SE; no closed form. "
                   "Kill condition: any claimed closed form must reproduce the "
                   "published table within 3 SE at all grid points.")
    out["verdict"] = verdict
    out["best_family"] = {"max_resid_SE": round(best["max_resid_SE"], 2)}

    # ---- results json ---------------------------------------------------------
    tab = []
    for r in rows16:
        d = {k: r[k] for k in ("tau0", "q", "src", "E_Q", "s_Q", "E_tau", "E_D",
                               "E_N", "E_Q_over_N", "E_Q_over_Np1", "E_lN",
                               "E_Tless", "E_Tless_over_N", "E_mu_exit")}
        d["E_Q"] = round(d["E_Q"], 8)
        tab.append(d)
    out["table_volume"] = tab
    out["table_central"] = [{k: round(r[k], 8) for k in
                             ("tau0", "q", "E_Q", "s_Q", "E_tau", "E_D", "E_N",
                              "E_Q_over_N", "E_mu_exit")} for r in cen]
    out["checks"] = {
        "bookkeeping_Q_eq_X": max(r["max_book_err"] for r in res) < 1e-9,
        "anchor_J02_0.59715": abs(a1["E_Q"] - 0.5971526) < 6 * a1["s_Q"],
        "E_v2_eq_2EN": v2ok,
        # q-cloud is kappa(r) = tau0 (1 + q r^2); frozen identity central:
        # E[D] = int_0^1 r kappa(r) dr = tau0 (1/2 + q/4), EXACT for any q.
        "central_D_frozen": all(abs(r["E_D"] - r["tau0"] * (0.5 + r["q"] / 4))
                                < 6 * max(r["s_tau"], r["s_Q"]) for r in cen),
    }
    out["passed"] = sum(1 for v in out["checks"].values() if v)
    out["total"] = len(out["checks"])
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(f"\nchecks: {out['checks']}")
    print(f"verdict: {verdict}")
    print(f"elapsed {time.time() - t0all:.0f}s; wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())