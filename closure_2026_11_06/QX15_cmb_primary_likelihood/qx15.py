#!/usr/bin/env python3
"""QX15 runner (FROZEN_CRITERIA.md 1df9dcc3e9 / origin 3ae5192a6b). One thread per job. Modes:
  ka                       KA-P (CamSpec TTTEEE at Cobaya NPIPE test point) and KA-A (ACT-lite test point); chi2_cal
  cells                    S(L) for C1-C4 (QX10 jcheck machinery, L <= 7000) -> parts/cellS.npz
  fit <foot> <main|MB|MA>  footing fit (Nelder-Mead on 5 params, nuisances profiled) -> parts/fit_<foot>_<mode>.json
  cell <foot> <C1..C4|P1>  local refit with Jeans-suppressed lensing -> parts/cell_<foot>_<c>.json
  acc <foot>               K-acc at the main best fit -> parts/acc_<foot>.json
  grade                    -> qx15.json/.out ; grade MUTATE -> qx15_MUTATE.json/.out
kappa = 1/2 FITTED; not theory closed. Footings never pooled."""
import os, sys, json, math, importlib.util
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import qx15_like as QL

REPO = QL.REPO; PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
G = 6.67430e-11; C = 2.99792458e8; MPC = 3.0856775814913673e22; TCMB = 2.7255
RHO_C100 = 3 * (1e5 / MPC) ** 2 / (8 * math.pi * G)
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
OMEGA_G = 2.4728e-5; OMEGA_R = OMEGA_G * (1 + 3.046 * 7 / 8 * (4 / 11) ** (4 / 3))
OB_BR = (0.0215, 0.0230); TAU_BR = (0.01, 0.15)
LPAD = 9001
NOTE = "kappa = 1/2 FITTED; not theory closed"


def background(foot, ob, od):                       # QX10's frozen footing rule
    w = 4 * FOOT[foot] ** 2 / (G * C ** 2) / RHO_C100
    if foot == "canonical":
        return math.sqrt(w + ob + od + OMEGA_R), w
    return math.sqrt(w), w - ob - od - OMEGA_R


def pad(cl):
    D = {}
    for k, j in (("tt", 0), ("ee", 1), ("te", 3)):
        a = np.zeros(LPAD); n = min(LPAD, cl.shape[0]); a[:n] = cl[:n, j]; D[k] = a
    return D


def camb_D(pars, S=None, lmax=7000, lpa=4):   # A1: lpa 1 -> 4 before any graded number
    import camb
    p = camb.CAMBparams(); p.set_cosmology(**pars["cosmo"]); p.InitPower.set_params(As=pars["As"], ns=pars["ns"])
    p.set_for_lmax(lmax, lens_potential_accuracy=lpa)
    for k, v in pars.get("extra", {}).items(): setattr(p, k, v)
    r = camb.get_results(p)
    if S is None:
        cl = r.get_total_cls(lmax, CMB_unit="muK")
    else:
        pp = r.get_lens_potential_cls(p.max_l)[:, 0].copy()   # CAMB needs clpp to Params.max_l (fix after crash)
        Ls = np.arange(len(pp)); Sx = np.ones(len(pp))
        LS, SS = S; Sx[2:] = np.interp(Ls[2:], LS, SS, left=SS[0], right=SS[-1])
        cl = r.get_lensed_cls_with_spectrum(pp * Sx, lmax=lmax, CMB_unit="muK")
    return pad(cl)


def pars_foot(foot, th, mode):
    ob, od, lnA, ns, tau = th
    h, ode = background(foot, ob, od)
    oc = 1e-7 if mode == "MB" else od
    out = dict(cosmo=dict(H0=100 * h, ombh2=ob, omch2=oc, mnu=0.0, nnu=3.046, num_massive_neutrinos=0, tau=tau, TCMB=TCMB),
               As=math.exp(lnA) * 1e-10, ns=ns)
    if mode == "MB":            # A2: CAMB's HMCode fails / returns NaN at omch2 ~ 0; linear lensing, as QX10's CLASS MB
        import camb; out["extra"] = {"NonLinear": camb.model.NonLinear_none}
    return out, h, ode


def class_D_MA(foot, th, lmax=7000):
    from classy import Class
    ob, od, lnA, ns, tau = th; h, ode = background(foot, ob, od)
    p = {'output': 'tCl,pCl,lCl', 'lensing': 'yes', 'l_max_scalars': lmax, 'h': h, 'omega_b': ob, 'A_s': math.exp(lnA) * 1e-10,
         'n_s': ns, 'tau_reio': tau, 'N_ur': 3.046, 'T_cmb': TCMB, 'omega_cdm': 1e-7, 'Omega_fld': od / h ** 2,
         'w0_fld': -1e-3, 'wa_fld': 0.0, 'cs2_fld': 1.0, 'use_ppf': 'no'}
    M = Class(); M.set(p); M.compute(); cl = M.lensed_cl(lmax); f = (TCMB * 1e6) ** 2
    l = np.arange(lmax + 1); arr = np.zeros((lmax + 1, 4))
    for j, X in ((0, "tt"), (1, "ee"), (3, "te")): arr[:, j] = l * (l + 1) * cl[X][:lmax + 1] * f / (2 * np.pi)
    M.struct_cleanup(); M.empty(); return pad(arr)


def pen(x, fixed_od):
    ob, od, lnA, ns, tau = x; s = 0.0
    s += (max(0, OB_BR[0] - ob) + max(0, ob - OB_BR[1])) / 1e-4
    s += (max(0, TAU_BR[0] - tau) + max(0, tau - TAU_BR[1])) / 1e-3
    if not fixed_od: s += (max(0, 0.005 - od) + max(0, od - 0.4)) / 1e-3
    s += (max(0, 0.7 - ns) + max(0, ns - 1.3)) / 1e-3
    return s


def make_obj(foot, mode, S=None, log=None):
    fixed_od = (mode == "MB"); cache = {}; state = {"x0": None, "best": None}
    def f(x):
        x = np.array(x, float)
        if fixed_od: x[1] = 1e-7
        key = tuple(np.round(x, 9))
        if key in cache: return cache[key]
        pp = pen(x, fixed_od)
        if pp > 0: cache[key] = 1e7 + 1e4 * pp; return cache[key]
        try:
            D = class_D_MA(foot, x) if mode == "MA" else camb_D(pars_foot(foot, x, mode)[0], S=S)
            g = QL.grade_spectra(D, x0=state["x0"]); v = g["PA"]
            if not np.isfinite(v): raise ValueError("non-finite chi2")   # A2: NaN no longer poisons the best tracker
            state["x0"] = {"Pcut": np.array(g["Pcut"]["nuis"]), "A": np.array(g["A"]["nuis"])}
            if state["best"] is None or v < state["best"][0]: state["best"] = (v, x.tolist(), g)
        except Exception as e:
            v = 1e8
            if log: print("ERR", repr(e), flush=True)
        cache[key] = v
        if log and len(cache) % 10 == 0: print(len(cache), "best", state["best"][0] if state["best"] else None, flush=True)
        return v
    return f, state, cache


def nm(f, s, step, maxfev):
    simplex = [s] + [s + np.eye(5)[i] * step[i] for i in range(5)]
    return minimize(f, s, method="Nelder-Mead", options=dict(initial_simplex=np.array(simplex), maxfev=maxfev, xatol=1e-5, fatol=0.05))


def qx10_start(foot, mode):
    fn = os.path.join(REPO, "closure_2026_11_06/QX10_window_hardening/iter_1_primary_cmb", f"fit_{foot}_{'MB' if mode == 'MB' else ('MA' if mode == 'MA' else 'main')}.json")
    t = json.load(open(fn))["theta"]; return np.array([t["omega_b"], t["omega_d"], t["lnAs1e10"], t["n_s"], t["tau"]])


def do_fit(foot, mode):
    f, st, cache = make_obj(foot, mode, log=True)
    step = np.array([3e-4, 0.01, 0.05, 0.02, 0.02])
    starts = [qx10_start(foot, mode), np.array([0.0224, 0.120, 3.04, 0.965, 0.055])]
    if mode == "MB": starts[1] = np.array([0.0224, 1e-7, 3.04, 0.965, 0.055])
    for s in starts: nm(f, s, step, 260)
    v, x, g = st["best"]; pr, h, ode = pars_foot(foot, x, mode)
    res = dict(foot=foot, mode=mode, theta=dict(zip(["omega_b", "omega_d", "lnAs1e10", "n_s", "tau"], x)), h=h, omega_DE=ode,
               chi2_PA=v, grade=g, nfev=len(cache), note=NOTE)
    json.dump(res, open(os.path.join(PARTS, f"fit_{foot}_{mode}.json"), "w"), indent=1, default=float); print(json.dumps(res, default=float))


def published_points():
    ns_ = 0.96399503; logA = 3.04920413
    P = dict(cosmo=dict(ombh2=0.02235048, omch2=0.12121379, cosmomc_theta=1.04240171e-2, tau=0.05, mnu=0.06, num_massive_neutrinos=1, TCMB=TCMB),
             As=math.exp(logA) * 1e-10, ns=ns_)
    nuisP = np.array([0.99818025, 10.35947284, 18.67072461, 7.54932654, 0.83715482, 0.94987418, 1.23385364, 0.98781552, 1.013345])
    A = dict(cosmo=dict(ombh2=0.022, omch2=0.117, cosmomc_theta=104.09e-4, tau=0.065, mnu=0.06, num_massive_neutrinos=1, TCMB=TCMB),
             As=2e-9, ns=0.96)
    return P, nuisP, A


def do_ka():
    P, nuisP, A = published_points()
    import camb
    def hi(pars, halofit=None, logl=None):
        p = camb.CAMBparams(); p.set_cosmology(**pars["cosmo"]); p.InitPower.set_params(As=pars["As"], ns=pars["ns"])
        p.set_for_lmax(9000, lens_potential_accuracy=8)
        if halofit: p.NonLinearModel.set_params(halofit_version=halofit)
        if logl: p.min_l_logl_sampling = logl
        r = camb.get_results(p); return pad(r.get_total_cls(9000, CMB_unit="muK"))
    DP = hi(P, "mead2020"); likeP, priP = QL.lik("P").chi2(DP, nuisP)
    DA = hi(A, None, 6000); chiA = QL.lik("A").chi2(DA, (1.0, 1.0))
    cal = QL.grade_spectra(DP)                          # yardstick: PA profiled at the published NPIPE test cosmology
    res = dict(KA_P=dict(chi2=likeP, ref=11337.34, diff=likeP - 11337.34, pass_=abs(likeP - 11337.34) <= 1.0),
               KA_A=dict(chi2=chiA, ref=790.96, diff=chiA - 790.96, pass_=abs(chiA - 790.96) <= 1.0),
               chi2_cal=dict(PA=cal["PA"], Pcut=cal["Pcut"], A=cal["A"]), note=NOTE + "; published points are code/gate calibrations, never inputs")
    json.dump(res, open(os.path.join(PARTS, "ka.json"), "w"), indent=1, default=float); print(json.dumps(res, default=float))


def do_cells():
    spec = importlib.util.spec_from_file_location("qx10_i1", os.path.join(REPO, "closure_2026_11_06/QX10_window_hardening/iter_1_primary_cmb/qx10_i1.py"))
    M10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(M10)
    import inspect
    src = inspect.getsource(M10.jcheck)
    assert "Ls = np.arange(2, 2501)" in src and "S = Sfull(Rr)" in src
    src = src.replace("Ls = np.arange(2, 2501)", "Ls = np.arange(2, 7001)")
    old = "S = np.ones(len(Ls)); ok = den > 0; S[ok] = num[ok] / den[ok]; return S"
    assert old in src
    src = src.replace(old, "S = np.ones(len(Ls)); ok = den > 0; S[ok] = num[ok] / den[ok]; COV['last'] = full; return S")
    # full coverage: every z-slice's k = (L+0.5)/chi inside the solver k-grid
    src = src.replace("        num = np.zeros(len(Ls)); den = np.zeros(len(Ls))",
                      "        num = np.zeros(len(Ls)); den = np.zeros(len(Ls)); full = np.ones(len(Ls), bool)")
    src = src.replace("kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])",
                      "kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1]); full &= m | (w[j] == 0)")
    src = src.replace("Rr = solve_gen(kJ) / N3[\"ref\"]; S = Sfull(Rr)", "Rr = solve_gen(kJ) / N3[\"ref\"]; S = Sfull(Rr); SOUT[cname] = (S.copy(), COV['last'].copy())")
    src = src.replace('json.dump(res, open(os.path.join(HERE, "jcheck.json"), "w"), indent=1)', "return res")
    ns = M10.__dict__; SOUT = {}; COV = {}; ns["SOUT"] = SOUT; ns["COV"] = COV
    exec(compile(src, "qx10_jcheck_extended", "exec"), ns)
    res = ns["jcheck"]()
    Ls = np.arange(2, 7001); out = {}; meta = {}
    for c, (S, full) in SOUT.items():
        Lcov = int(Ls[full].max()) if full.any() else 2
        S2 = S.copy(); S2[Ls > Lcov] = S[Ls == Lcov][0]
        out[c] = S2; meta[c] = dict(L_full_coverage=Lcov, S_min=float(S2.min()), S_at_L1000=float(S2[998]), S_at_L3000=float(S2[2998]), S_at_7000=float(S2[-1]),
                                   S_raw_min=float(S.min()), qx10_summary=res["cells"][c])
    np.savez(os.path.join(PARTS, "cellS.npz"), L=Ls, **out)
    json.dump(meta, open(os.path.join(PARTS, "cellS_meta.json"), "w"), indent=1, default=float); print(json.dumps(meta, default=float))


def do_cell(foot, c):
    base = json.load(open(os.path.join(PARTS, f"fit_{foot}_main.json")))
    x0 = np.array([base["theta"][k] for k in ["omega_b", "omega_d", "lnAs1e10", "n_s", "tau"]])
    Z = np.load(os.path.join(PARTS, "cellS.npz")); L = Z["L"]
    S = (L, np.full(len(L), 0.5)) if c == "P1" else (L, Z[c])
    f, st, cache = make_obj(foot, "main", S=S, log=True)
    nm(f, x0, np.array([1.5e-4, 0.004, 0.02, 0.008, 0.008]), 150)
    v, x, g = st["best"]
    res = dict(foot=foot, cell=c, theta=dict(zip(["omega_b", "omega_d", "lnAs1e10", "n_s", "tau"], x)), chi2_PA=v, chi2_main=base["chi2_PA"],
               delta_cell=v - base["chi2_PA"], grade=g, nfev=len(cache), note=NOTE)
    json.dump(res, open(os.path.join(PARTS, f"cell_{foot}_{c}.json"), "w"), indent=1, default=float); print(json.dumps(res, default=float))


def do_acc(foot):
    base = json.load(open(os.path.join(PARTS, f"fit_{foot}_main.json")))
    x = [base["theta"][k] for k in ["omega_b", "omega_d", "lnAs1e10", "n_s", "tau"]]
    pr = pars_foot(foot, x, "main")[0]
    lo = QL.grade_spectra(camb_D(pr))["PA"]; hi = QL.grade_spectra(camb_D(pr, lmax=9000, lpa=8))["PA"]  # lo = fit precision (lmax 7000, lpa 4)
    # S = 1 through the custom-lensing path (internal consistency of the cell route)
    L = np.arange(2, 7001); one = QL.grade_spectra(camb_D(pr, S=(L, np.ones(len(L)))))["PA"]
    res = dict(foot=foot, chi2_lo=lo, chi2_hi=hi, diff=hi - lo, pass_=abs(hi - lo) <= 2.0, chi2_customlens_S1=one, customlens_minus_std=one - lo, note=NOTE)
    json.dump(res, open(os.path.join(PARTS, f"acc_{foot}.json"), "w"), indent=1, default=float); print(json.dumps(res, default=float))


def L1(delta):
    if not np.isfinite(delta): return 'NO VERDICT (non-finite)'
    return "PASS" if delta <= 9 else ("TENSION" if delta <= 25 else "FAIL")


def Lc(delta):
    return "PASS" if delta <= 4 else ("TENSION" if delta <= 25 else "FAIL")


def do_grade(mutate=False):
    J = lambda n: json.load(open(os.path.join(PARTS, n)))
    ka = J("ka.json"); cal = ka["chi2_cal"]["PA"]
    out = dict(KA_P=ka["KA_P"], KA_A=ka["KA_A"], chi2_cal=cal, footings={}, note=NOTE)
    p2 = J("ka_p2.json"); out["KA_P2"] = p2                     # A1: KA-P read through KA-P2 (published test settings)
    ka_ok = p2["pass_"] and ka["KA_A"]["pass_"]
    for foot in ("canonical", "alt"):
        F = {}
        modes = ("MA", "MB") if mutate else ("main", "MB")
        for m in modes:
            r = J(f"fit_{foot}_{m}.json"); d = r["chi2_PA"] - cal
            F[m] = dict(chi2_PA=r["chi2_PA"], delta=d, label=L1(d), theta=r["theta"], h=r["h"],
                        P_full_at_fit=None, nuis_Pcut=r["grade"]["Pcut"]["nuis"], nuis_A=r["grade"]["A"]["nuis"],
                        chi2_Pcut=r["grade"]["Pcut"]["chi2"], chi2_A=r["grade"]["A"]["chi2"])
        if not mutate:
            acc = J(f"acc_{foot}.json"); F["K_acc"] = acc
            F["main"]["label_final"] = F["main"]["label"] if acc["pass_"] else "NO VERDICT (K-acc)"
            F["control_MB_bites"] = F["MB"]["label"] == "FAIL"
            P1 = J(f"cell_{foot}_P1.json"); F["P1"] = dict(delta=P1["delta_cell"], bites=P1["delta_cell"] > 25)
            F["cells"] = {}
            for c in ("C1", "C2", "C3", "C4"):
                r = J(f"cell_{foot}_{c}.json")
                lab = Lc(r["delta_cell"]) if F["P1"]["bites"] else "NO VERDICT (P1 no power)"
                F["cells"][c] = dict(delta_cell=r["delta_cell"], chi2_PA=r["chi2_PA"], label=lab, theta=r["theta"])
        else:
            F["MA_fails"] = F["MA"]["label"] == "FAIL"; F["MB_fails"] = F["MB"]["label"] == "FAIL"
        out["footings"][foot] = F
    out["KA_ok"] = ka_ok
    tag = "qx15_MUTATE" if mutate else "qx15"
    json.dump(out, open(os.path.join(HERE, tag + ".json"), "w"), indent=1, default=float)
    lines = [f"QX15 {'MUTATE ' if mutate else ''}grade. {NOTE}", f"KA-P chi2 {ka['KA_P']['chi2']:.2f} vs 11337.34 ({ka['KA_P']['diff']:+.2f}) pass={ka['KA_P']['pass_']}",
             f"KA-A chi2 {ka['KA_A']['chi2']:.2f} vs 790.96 ({ka['KA_A']['diff']:+.2f}) pass={ka['KA_A']['pass_']}", f"chi2_cal(PA) = {cal:.2f}"]
    for foot, F in out["footings"].items():
        for m in (("MA", "MB") if mutate else ("main", "MB")):
            lines.append(f"{foot:9s} {m:4s} chi2_PA {F[m]['chi2_PA']:.2f} delta {F[m]['delta']:+.2f} -> {F[m]['label']}  h {F[m]['h']:.4f} theta {json.dumps({k: round(v, 5) for k, v in F[m]['theta'].items()})}")
        if not mutate:
            lines.append(f"{foot:9s} K-acc diff {F['K_acc']['diff']:+.3f} pass={F['K_acc']['pass_']}; custom-lensing(S=1) - std {F['K_acc']['customlens_minus_std']:+.3f}; main final: {F['main']['label_final']}; MB control bites: {F['control_MB_bites']}")
            lines.append(f"{foot:9s} P1 (flat S=0.5) delta {F['P1']['delta']:+.2f} bites={F['P1']['bites']}")
            for c, r in F["cells"].items(): lines.append(f"{foot:9s} {c} delta_cell {r['delta_cell']:+.2f} -> {r['label']}")
    lines.append(f"KA-P2 (A1, published test settings, CAMB {p2['camb']}): chi2 {p2['chi2']:.3f} vs 11337.34 ({p2['diff']:+.3f}) pass={p2['pass_']}; frozen KA-P reading FAIL kept above")
    lines.append(f"KA ok (KA-P2 and KA-A): {ka_ok} (if False the lane is NO VERDICT)")
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "ka": do_ka()
    elif a[0] == "cells": do_cells()
    elif a[0] == "fit": do_fit(a[1], a[2])
    elif a[0] == "cell": do_cell(a[1], a[2])
    elif a[0] == "acc": do_acc(a[1])
    elif a[0] == "grade": do_grade(mutate=(len(a) > 1 and a[1] == "MUTATE"))
