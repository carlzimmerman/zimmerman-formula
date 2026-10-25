#!/usr/bin/env python3
"""X48 analysis: c_f = r_vir / r_-2 of the collapsed object at z_f in each run (FROZEN_CRITERIA section 2); summary + verdict.

    python3 x48_analyze.py [--runs DIR] [--mutate]      -> x48_analyze.out / _results.json  (K3 synthetic NFW test always run)
"""
import argparse, glob, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def centre(x, m):
    c = x.mean(0); r = np.sqrt(((x - c) ** 2).sum(1)).max()
    while True:
        sel = np.sqrt(((x - c) ** 2).sum(1)) < r
        if sel.sum() < 100: return c
        c = x[sel].mean(0); r *= 0.8


def measure(x, m, rho_m_z, eps):
    c = centre(x, m); r = np.sort(np.sqrt(((x - c) ** 2).sum(1))); n = np.arange(1, len(r) + 1)
    Menc = n * m; dens = Menc / (4 / 3 * math.pi * r ** 3)
    target = 18 * math.pi ** 2 * rho_m_z
    above = np.where(dens >= target)[0]
    if len(above) == 0: return dict(flag="no virial radius")
    rvir = float(r[above.max()])
    rconv = max(3 * eps, float(r[min(199, len(r) - 1)]))
    if rconv >= rvir / 2: return dict(flag="unresolved", rvir=rvir, rconv=rconv)
    edges = np.geomspace(rconv, rvir, 25); cnt, _ = np.histogram(r, edges)
    vol = 4 / 3 * math.pi * (edges[1:] ** 3 - edges[:-1] ** 3); rho = cnt * m / vol; rc = np.sqrt(edges[1:] * edges[:-1])
    ok = cnt > 0
    if ok.sum() < 8: return dict(flag="too few bins", rvir=rvir)
    lr, lrho = np.log(rc[ok]), np.log(rho[ok])
    sm = np.convolve(lrho, np.ones(3) / 3, mode="same"); sm[0], sm[-1] = lrho[0], lrho[-1]
    s = np.gradient(sm, lr)
    cr = np.where((s[:-1] > -2) & (s[1:] <= -2))[0]
    # reported: NFW-form fit of M(<r) on [rconv, rvir]
    sel = (r >= rconv) & (r <= rvir); cs = np.linspace(1.0, 30.0, 581)
    mu = lambda y: np.log1p(y) - y / (1 + y)
    best = min(cs, key=lambda cc: float(np.sum((np.log(mu(cc * r[sel] / rvir) / mu(cc)) - np.log(Menc[sel] / Menc[sel][-1] * (1.0))) ** 2)))
    if len(cr) == 0:
        return dict(flag="no -2 crossing", rvir=rvir, rconv=rconv, slope_range=[float(s.min()), float(s.max())], c_nfw_fit=float(best))
    i = cr[0]; rm2 = float(np.exp(np.interp(-2, [s[i + 1], s[i]], [lr[i + 1], lr[i]])))
    return dict(flag="ok", rvir=rvir, rconv=rconv, rm2=rm2, cf=rvir / rm2, n_inside_rm2=int((r < rm2).sum()), c_nfw_fit=float(best))


def synthetic_nfw(c, N, seed, rvir=1.0):
    rng = np.random.default_rng(seed); mu = lambda y: np.log1p(y) - y / (1 + y)
    u = rng.random(N) * mu(c); yg = np.geomspace(1e-6, c, 20000); y = np.interp(u, mu(yg), yg)
    r = y / c * rvir; v = rng.standard_normal((N, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
    return r[:, None] * v


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--runs", default=os.path.join(HERE, "runs")); ap.add_argument("--mutate", action="store_true")
    a = ap.parse_args(); TAG = "_MUTATE" if a.mutate else ""
    P("X48 analysis" + (" [MUTATE: synthetic c = 8]" if a.mutate else "") + "; kappa = 1/2 FITTED; not theory closed")
    # K3 synthetic NFW
    N = 12000; xs = synthetic_nfw(8.0 if a.mutate else 4.0, N, 1); msyn = 1.0 / N
    rho_target = (N * msyn) / (4 / 3 * math.pi * 1.0 ** 3) / (18 * math.pi ** 2)   # makes r_vir = 1
    res = measure(xs, msyn, rho_target, 1e-4)
    k3 = res.get("flag") == "ok" and abs(res["cf"] / 4.0 - 1) < 0.15
    P(f"K3 synthetic NFW (c = {'8' if a.mutate else '4'}): measured c_f {res.get('cf', float('nan')):.3f} ({res.get('flag')}), NFW-fit {res.get('c_nfw_fit', float('nan')):.2f}: {'PASS' if k3 else 'FAIL'}")
    R = dict(K3=dict(res, pass_=bool(k3)), runs={})
    for d in sorted(glob.glob(os.path.join(a.runs, "*"))):
        sn = os.path.join(d, "snap_zf.npz")
        if not os.path.exists(sn): R["runs"][os.path.basename(d)] = dict(flag="not finished"); continue
        Z = np.load(sn); x, v, m = Z["x"], Z["v"], float(Z["m"]); meta = json.loads(str(Z["meta"]))
        rho_mz = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3   # comoving mean -> physical
        out = measure(x, m, rho_mz, meta["eps"])
        drift = float(np.linalg.norm(v.mean(0)) / np.sqrt((v ** 2).sum(1).mean()))
        cc = meta["constraint_check"]; out.update(M=meta["M"], seed=meta["seed"], ng=meta["ng"], N=meta["N"], zf=meta["zf"], drift=drift,
                                                  constraint=max(abs(cc["c1"]), abs(cc["c2"])))
        R["runs"][os.path.basename(d)] = out
        P(f"  {os.path.basename(d)}: M {meta['M']:.0e} seed {meta['seed']} ng {meta['ng']} N {meta['N']}: {out['flag']}"
          + (f", c_f {out['cf']:.2f} (r_vir {out['rvir']:.3f}, r_-2 {out['rm2']:.3f} Mpc, n<r_-2 {out['n_inside_rm2']}, NFW-fit {out['c_nfw_fit']:.2f})" if out["flag"] == "ok" else "")
          + f"; drift {drift:.1e}; constraint {out['constraint']:.1e}")
    by = {}
    for k, o in R["runs"].items():
        if o.get("flag") == "ok" and o.get("ng") == 38: by.setdefault(o["M"], []).append(o["cf"])
    R["cf_by_mass"] = {f"{M:.0e}": (float(np.median(v)) if len(v) >= 2 else None) for M, v in sorted(by.items())}
    P("c_f by mass (median over seeds, ng 38): " + json.dumps(R["cf_by_mass"]))
    json.dump(R, open(os.path.join(HERE, f"x48_analyze_results{TAG}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"x48_analyze{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    return 0 if k3 else 1


if __name__ == "__main__":
    sys.exit(main())
