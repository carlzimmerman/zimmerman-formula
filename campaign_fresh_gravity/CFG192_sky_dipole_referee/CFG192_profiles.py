#!/usr/bin/env python3
"""CFG192_profiles -- per-galaxy profile curves chi2_i(log a0) for all usable SPARC galaxies (>= 5 points), primary settings:
kernel nu_mono, LML priors, 4 nuisances profiled, grid -11.3..-9.0 step 0.01.
MUTATE=k: 1 point-level injection A=0.5 ; 2 injection A=0.2 ; 4 fixed nuisances ; 6 Newtonian kernel (3,5,7 reuse other files).
Outputs CFG192_profiles.npz / .out (MUTATE: CFG192_profiles_MUTATE_k.*).  Exit 0 (2 on error)."""
import os
import sys
import numpy as np
from scipy.optimize import least_squares
from CFG192_common import *
import CFG192_common as CC

MUT = int(os.environ.get("MUTATE", "0"))
SEED_DIR = 19211


def inj_dir():
    v = np.random.default_rng(SEED_DIR).normal(size=3)
    return v / np.linalg.norm(v)


def main():
    suf = f"_MUTATE_{MUT}" if MUT else ""
    R = Run("CFG192_profiles", suf)
    R.banner(f"CFG192 profiles  MUTATE={MUT}   repo=<repo>")
    if MUT in (3, 5, 7):
        R.P(f"MUTATE={MUT} reuses the profiles of {'MUTATE_1' if MUT in (3, 5) else 'the primary run'}; nothing built here.")
        return R.finish(0)
    G = load_all()
    P = [prep(g) for g in G]
    R.P(f"galaxies in the rotmod set: {len(P)}; with (l,b): {sum(p['n'] is not None for p in P)}")
    P = [p for p in P if p["N"] >= 5]
    R.P(f"usable (>= 5 points with Vobs>0, eV>0, fiducial Vbar^2>0): {len(P)} galaxies, {sum(p['N'] for p in P)} points")
    cfg = make_cfg()
    if MUT in (1, 2):
        A = 0.5 if MUT == 1 else 0.2
        d = inj_dir()
        D = A * d
        R.P(f"MUTATE {MUT}: point-level injection A = {A} toward (l, b) = ({vec_to_lb(d)[0]:.1f}, {vec_to_lb(d)[1]:.1f}) seed {SEED_DIR}; a0ref = 1.13e-10")
        P = [inject_point(p, D) for p in P]
    elif MUT == 4:
        cfg = make_cfg(prof=())
        R.P("MUTATE 4: nuisances FIXED (Yd 0.5, Yb 0.7, catalogue D and Inc): no profiling")
    elif MUT == 6:
        cfg = make_cfg(nu="newton", step=0.05)
        R.P("MUTATE 6: Newtonian kernel nu = 1, grid step 0.05")
    pr = build_profiles(P, cfg)
    R.T("profiles built")
    chi = pr["chi"]
    grid = pr["grid"]
    R.check("finite", f"all finite: {np.isfinite(chi).all()}", np.isfinite(chi).all())
    kmin = np.argmin(chi, 1)
    R.P(f"best-grid-index hits at the lower edge: {int((kmin == 0).sum())}, upper edge: {int((kmin == len(grid) - 1).sum())} of {len(P)}")
    bs = birge(chi, pr["N"])
    R.P(f"Birge factor: median {np.median(bs):.3f}, min {bs.min():.2f}, max {bs.max():.1f}")
    hw, best = curve_halfwidth(grid, chi / bs[:, None])
    R.P(f"Birge-scaled Delta chi2 = 1 half-width: median {np.median(hw):.3f} dex; best log a0 16/50/84%: "
        f"{np.percentile(best, 16):.2f} {np.percentile(best, 50):.2f} {np.percentile(best, 84):.2f}")
    R.num("birge_median", float(np.median(bs)))
    R.num("halfwidth_median", float(np.median(hw)))
    if MUT == 0:
        # optimiser check: profile value <= brute-force multi-start minimum at 10 grid points x 5 galaxies
        rng = np.random.default_rng(192)
        ok_all = True
        worst = 0.0
        sub = [i for i in range(len(P)) if P[i]["N"] >= 10][:5:1]
        sub = [i for i in range(len(P)) if P[i]["N"] >= 10][::max(1, len(P) // 5)][:5]
        for i in sub:
            p = P[i]
            th0 = dict(lYd=math.log10(0.5), lYb=math.log10(0.7), Dp=p["D"], ip=p["Inc"])
            act = ["lYd"] + (["lYb"] if p["has_bul"] else []) + ["Dp", "ip"]
            lo = dict(lYd=math.log10(0.05), lYb=math.log10(0.05), Dp=0.2 * p["D"], ip=5.0)
            hi = dict(lYd=math.log10(3), lYb=math.log10(3), Dp=3 * p["D"], ip=90.0)
            cen = dict(lYd=math.log10(0.5), lYb=math.log10(0.7), Dp=p["D"], ip=p["Inc"])
            sg = dict(lYd=0.1, lYb=0.1, Dp=p["eD"], ip=p["eInc"])
            for k in np.linspace(0, len(grid) - 1, 10).astype(int):
                la = grid[k]

                def res(x):
                    th = dict(th0)
                    th.update(dict(zip(act, x)))
                    Vp = CC._model_V(p, th, la, nu_mono, act)
                    return np.concatenate([(p["Vobs"] - Vp) / p["eV"], [(th[a] - cen[a]) / sg[a] for a in act]])
                bb = np.inf
                for _ in range(24):
                    x0 = np.array([rng.uniform(lo[a], hi[a]) for a in act])
                    try:
                        s = least_squares(res, x0, bounds=([lo[a] for a in act], [hi[a] for a in act]),
                                          x_scale=np.array([sg[a] for a in act]), xtol=1e-10, ftol=1e-10, gtol=1e-10)
                        bb = min(bb, 2 * s.cost)
                    except Exception:
                        pass
                diff = chi[i, k] - bb
                worst = max(worst, diff)
                ok_all &= diff <= 1e-3 * max(1.0, bb)
        R.check("optimiser check (profile <= 24-start brute force, 10 grid points x 5 galaxies)", f"worst excess {worst:.2e}", ok_all)
    np.savez(os.path.join(HERE, f"CFG192_profiles{suf}.npz"), grid=grid, chi=chi, chiv=pr["chiv"], theta=pr["theta"], N=pr["N"],
             names=np.array([p["name"] for p in P]), fD=np.array([p["fD"] for p in P]), Q=np.array([p["Q"] for p in P]),
             Inc=np.array([p["Inc"] for p in P]), eInc=np.array([p["eInc"] for p in P]), D=np.array([p["D"] for p in P]),
             eD=np.array([p["eD"] for p in P]), has_bul=np.array([p["has_bul"] for p in P]),
             n=np.array([p["n"] for p in P]), lb=np.array([p["lb"] for p in P]))
    R.P(f"wrote CFG192_profiles{suf}.npz")
    return R.finish(0)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
