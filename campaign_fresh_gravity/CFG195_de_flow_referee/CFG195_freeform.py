#!/usr/bin/env python3
"""CFG195_freeform.py -- A3 (free-form NEC-respecting rho_DE(z) that must mimic a chain sample's background) and A7 (local vs cosmic).
Deterministic, no random numbers.  Reads only the three committed chains.  Time-boxed by construction (about a minute)."""
import math, os, numpy as np
from scipy.optimize import minimize
from CFG195_common import Run, find_repo
run = Run("CFG195_freeform", ()); repo = find_repo(); assert repo
D = os.path.join(repo, "fable_independent_2026", "data", "desi_dr2_w0wa_thinned")
CH = {n: np.loadtxt(os.path.join(D, f + ".txt")) for n, f in (("DESY5", "desy5sn"), ("Pantheon+", "pantheonplus"), ("Union3", "union3"))}
R, SQ3H = 0.2928, math.sqrt(3) / 2
ZN = np.array([0, 0.3, 0.6, 1.0, 1.5, 2.5, 5.0]); ZE = np.array([0.3, 0.6, 1.0, 1.5, 2.5, 5.0]); ZD = np.array([0.5, 1.0, 2.5])
zg = np.concatenate([np.linspace(ZN[i], ZN[i + 1], 300, endpoint=False) for i in range(6)] + [[5.0]])
idxn = np.array([np.argmin(abs(zg - z)) for z in ZN]); assert np.allclose(zg[idxn], ZN)
u = np.linspace(math.log(6.0), math.log(1e9), 3000); ztail = np.exp(u) - 1
def cumtrap(y, x): return np.concatenate([[0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))])
def model(Om, rn):
    r = np.interp(zg, ZN, rn); E = np.sqrt(Om * (1 + zg) ** 3 + (1 - Om) * r)
    cD = cumtrap(1 / E, zg); ct = cumtrap(1 / ((1 + zg) * E), zg)
    Et = np.sqrt(Om * (1 + ztail) ** 3 + (1 - Om) * rn[-1]); tail = np.trapz(1 / Et * (1 + ztail) / (1 + ztail), u) if False else np.trapz(1 / ((1 + ztail) * Et) * (1 + ztail), u)
    # tail of Int dz/((1+z)E): dz/(1+z) = du
    t0 = ct[-1] + np.trapz(1 / Et, u)
    Ez = E[[np.argmin(abs(zg - z)) for z in ZE]]; Dc = np.interp(ZD, zg, cD)
    seg = cD[idxn]; rp = np.diff(rn) / np.diff(ZN); num = float(np.sum(rp * (seg[1:] - seg[:-1])))
    return Ez, Dc, num / (3 * t0), E
def target(w0, wa, Om):
    f = lambda z: (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
    return model(Om, f(ZN))[:3], f(ZN)
def solve(tgt, ombounds, eps=None, minimize_eps=False, kfac=SQ3H):
    Et, Dt = tgt[0], tgt[1]
    def unpack(p): return p[0], np.concatenate([[1.0], p[1:7]]), (p[7] if minimize_eps else eps)
    def cons(p):
        Om, rn, e = unpack(p); Ez, Dc, _, _ = model(Om, rn)
        c = list(e - (Ez / Et - 1)) + list(e + (Ez / Et - 1)) + list(e - (Dc / Dt - 1)) + list(e + (Dc / Dt - 1))
        c += list(np.diff(rn))                                                            # NEC: rho nondecreasing in z (w >= -1)
        c += list(2 - (1 + ZN[1:]) * np.diff(rn) / np.diff(ZN) / (3 * np.maximum(rn[1:], 1e-9)))     # 1+w <= 2 at segment ends (w <= 1)
        c += list(2 - (1 + ZN[:-1]) * np.diff(rn) / np.diff(ZN) / (3 * np.maximum(rn[:-1], 1e-9)))
        return np.array(c)
    obj = (lambda p: p[7]) if minimize_eps else (lambda p: -kfac * model(p[0], np.concatenate([[1.0], p[1:7]]))[2])
    starts = []
    for om0 in (0.5 * (ombounds[0] + ombounds[1]), ombounds[0], ombounds[1]):
        for shape in (np.ones(6), np.linspace(1, 1.6, 6), np.linspace(1, 3, 6)):
            starts.append(np.concatenate([[om0], shape] + ([[0.05]] if minimize_eps else [])))
    best = None
    for s0 in starts:
        bnds = [ombounds] + [(0.0, 50.0)] * 6 + ([(0.0, 1.0)] if minimize_eps else [])
        try: r = minimize(obj, s0, method="SLSQP", bounds=bnds, constraints=[{"type": "ineq", "fun": cons}], options=dict(maxiter=300, ftol=1e-12))
        except Exception: continue
        if cons(r.x).min() > -1e-7 and (best is None or r.fun < best.fun): best = r
    return best
def wq(x, wt, q):
    i = np.argsort(x); cx = np.cumsum(wt[i]) / wt.sum(); return float(np.interp(q / 100, cx, x[i]))
out = {}; anyR = False; anyRfix = False; mism = {}
print("== A3: max F (k=sqrt3/2) over NEC-respecting free-form rho_DE(z) (nodes z=0,.3,.6,1,1.5,2.5,5; piecewise linear; w in [-1,1]) that reproduces a chain sample's E(z_j), D_C(z) within eps ==")
for n, d in CH.items():
    wt, w0, wa, om = d.T; ob = (wq(om, wt, 2.5), wq(om, wt, 97.5))
    # sample nearest the weighted 97.5th percentile of the CPL-clipped F (recomputed here with the same closed form, k=3/4)
    def Fclip(w0_, wa_, om_):
        z = np.linspace(0, 40, 4001); f = (1 + z) ** (3 * (1 + w0_ + wa_)) * np.exp(-3 * wa_ * z / (1 + z)); w = w0_ + wa_ * z / (1 + z)
        E = np.sqrt(om_ * (1 + z) ** 3 + (1 - om_) * f); zz = np.geomspace(1, 1e8, 2000) if False else None
        num = np.trapz(np.maximum(1 + w, 0) * f / ((1 + z) * E), z); t0 = np.trapz(1 / ((1 + z) * E), z) + np.trapz(1 / ((1 + np.geomspace(41, 1e8, 3000)) * np.sqrt(om_ * (1 + np.geomspace(41, 1e8, 3000)) ** 3 + (1 - om_) * (1 + np.geomspace(41, 1e8, 3000)) ** (3 * (1 + w0_ + wa_)) * np.exp(-3 * wa_ * np.geomspace(41, 1e8, 3000) / (1 + np.geomspace(41, 1e8, 3000))))), np.geomspace(41, 1e8, 3000))
        return 0.75 * num / t0
    sub = np.linspace(0, len(wt) - 1, 400).astype(int); Fs = np.array([Fclip(w0[i], wa[i], om[i]) for i in sub]); p975 = wq(Fs, wt[sub], 97.5); i975 = sub[np.argmin(abs(Fs - p975))]
    samples = {"chain mean": (float(np.sum(wt * w0) / wt.sum()), float(np.sum(wt * wa) / wt.sum()), float(np.sum(wt * om) / wt.sum())), "F97.5 sample": (w0[i975], wa[i975], om[i975])}
    for lab, (a_, b_, c_) in samples.items():
        tgt, rt = target(a_, b_, c_)
        fmin = solve(tgt, ob, minimize_eps=True)
        emin = float(fmin.x[7]) if fmin is not None else None
        line = f"  {n:10s} {lab:13s} (w0,wa,Om)=({a_:+.3f},{b_:+.3f},{c_:.4f}); CPL target rho(z_j)/rho0 = {np.round(rt,3)}; smallest achievable eps with w>=-1: " + (f"{emin:.4f}" if emin is not None else "none")
        print(line); rec = {"eps_min": emin}
        for eps in (0.01, 0.02):
            r = solve(tgt, ob, eps=eps)
            if r is None: print(f"      [Om free in chain 95%] eps={eps:.2f}: infeasible for a NEC-respecting rho(z)"); rec[f"F_eps{eps}"] = None
            else:
                Fv = -r.fun; rec[f"F_eps{eps}"] = Fv; anyR |= Fv >= R
                print(f"      [Om free in chain 95%] eps={eps:.2f}: F_max(k=sqrt3/2) = {Fv:.4f}  (Omega_m'={r.x[0]:.4f}, rho nodes {np.round(np.concatenate([[1],r.x[1:7]]),3)})")
        for eps in (0.005, 0.01, 0.02):
            r = solve(tgt, (c_, c_), eps=eps)
            if r is None: print(f"      [Om fixed = sample's] eps={eps:.3f}: infeasible for a NEC-respecting rho(z)"); rec[f"Ffix_eps{eps}"] = None
            else:
                Fv = -r.fun; rec[f"Ffix_eps{eps}"] = Fv; anyRfix |= Fv >= R
                print(f"      [Om fixed = sample's] eps={eps:.3f}: F_max(k=sqrt3/2) = {Fv:.4f}  (rho nodes {np.round(np.concatenate([[1],r.x[1:7]]),3)})")
        out[f"{n}|{lab}"] = rec
run.num("A3", out)
run.check("A3 every feasible NEC-respecting free-form fit (eps=1%,2%) has F_max(k=sqrt3/2) < R (0.2928)", str({k: v for k, v in out.items()}), not anyR)
inf = [k for k, v in out.items() if v["F_eps0.01"] is None]
run.check("A3c same, Omega_m held at the sample's value (eps=0.5%,1%,2%): F_max(k=sqrt3/2) < R (reported; the outcome depends on the tolerance and on Omega_m freedom, which the repo cannot settle without the likelihood)", str({k: (v.get("Ffix_eps0.005"), v.get("Ffix_eps0.01"), v.get("Ffix_eps0.02")) for k, v in out.items()}), not anyRfix, load_bearing=False)
run.check("A3b a NEC-respecting rho(z) reproduces the CPL background within 1% at every tested sample (if not: the CPL H(z) cannot come from w>=-1, so the clip-and-keep-CPL use in the README is not a NEC-respecting model)", f"infeasible at 1% for: {inf}; eps_min: {[(k, round(v['eps_min'],4) if v['eps_min'] is not None else None) for k,v in out.items()]}", len(inf) == 0, load_bearing=False)
print("\n== A7 local vs cosmic: a medium compacted to C rho_L needs only 1+w_loc >= 2R/C for the same column, but compaction needs 1+w ==")
Cr = (1.134e4, 4.766e5)
for C in Cr:
    wl = 2 * R / C; print(f"  C={C:.3e}: local NEC needs 1+w_loc >= {wl:.2e}; with that 1+w the compression n^(1+w) = C needs log10(n) = {math.log10(C)/wl:.2e}")
tr = {(C, nmax): math.log10(C) / math.log10(nmax) for C in Cr for nmax in (10, 1e3, 1e6)}
print("  1+w needed to reach C by volume compression n_max (rho ~ n^(1+w)):", {f"C={C:.1e},n={nm:.0e}": round(v, 2) for (C, nm), v in tr.items()})
run.num("A7", dict(need_1pw_local=[2 * R / C for C in Cr], compaction_1pw={f"{C:.3e}|{nm:.0e}": v for (C, nm), v in tr.items()}))
run.check("A7 the local momentum requirement (1+w_loc >= 2R/C ~ 1e-6-5e-5) is tiny, the compaction requirement (1+w ~ 0.8-5 for n<=1e6) is not: the two cosmic-mean/local conclusions rest on the compaction, not on the momentum column", f"{[2*R/C for C in Cr]}", 2 * R / Cr[0] < 1e-4 and min(v for v in tr.values()) > 0.8, load_bearing=False)
run.finish()
