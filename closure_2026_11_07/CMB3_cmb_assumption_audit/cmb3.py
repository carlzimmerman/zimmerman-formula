#!/usr/bin/env python3
"""CMB3 (FROZEN_CRITERIA.md, origin e46081b7a9): assumption audit of the primary-CMB cold-component inference.
Imports F1A's own likelihood classes, footing rule and CAMB settings (f1a.py, read only). Nothing from QX3/QX10/QX15.
Usage: cmb3.py ka | a1 | mutate | a6point | fit <A2U|A2T|A3N|A4P|A6F> <canonical|alt> <cold|MB> | a4hess <foot> | ka2 <foot>
One process at a time, RSS < 1 GB. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); F1A = os.path.join(HERE, "../F1A_primary_cmb_audit")
sys.path.insert(0, F1A)
import f1a                                                   # noqa: E402  (likelihoods, footing rule; read only)
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
NOTE = f1a.NOTE; LTH = f1a.LTH; FOOT = f1a.FOOT
def dump(name, obj): json.dump(obj, open(os.path.join(PARTS, name), "w"), indent=1, default=float)
def stored(foot, mode): return json.load(open(os.path.join(F1A, "parts", f"fit_B2_{foot}_{mode}.json")))

def omr(nnu): return 2.4728e-5 * (1 + nnu * 7 / 8 * (4 / 11) ** (4 / 3))
def footing_h(foot, ob, od, nnu=3.046):
    w = 4 * FOOT[foot] ** 2 / (f1a.G * f1a.CL ** 2) / f1a.RHO_C100
    return math.sqrt(w + ob + od + omr(nnu)) if foot == "canonical" else math.sqrt(w)

# ------------------------------------------------------------------ theory with switches
_TMPL = {}
def template(foot):
    """A2-T: C_L^phiphi of the F1A B2 cold best fit (per footing), [L(L+1)]^2 C_L / 2 pi, held fixed."""
    if foot not in _TMPL:
        pr = stored(foot, "cold")["pars"]; r = camb_results(pr)
        _TMPL[foot] = r.get_lens_potential_cls(CMB_unit=None)[:, 0].copy()
    return _TMPL[foot]

def camb_results(pr, nnu=3.046, YHe=None, nrun=0.0):
    import camb
    p = camb.CAMBparams()
    p.set_cosmology(H0=100 * pr["h"], ombh2=pr["ob"], omch2=max(pr["oc"], 1e-7), tau=pr["tau"], mnu=0.0,
                    num_massive_neutrinos=0, nnu=nnu, YHe=YHe, TCMB=f1a.TCMB)
    p.InitPower.set_params(As=math.exp(pr["lnA"]) * 1e-10, ns=pr["ns"], nrun=nrun)
    p.set_for_lmax(LTH, lens_potential_accuracy=1); p.NonLinear = camb.model.NonLinear_none
    return camb.get_results(p)

def theory(pr, nnu=3.046, YHe=None, nrun=0.0, lens="own", Aphi=1.0, foot=None, clpp=None):
    r = camb_results(pr, nnu, YHe, nrun)
    if lens == "own": cl = r.get_total_cls(LTH, CMB_unit="muK")
    elif lens == "none": cl = r.get_unlensed_total_cls(LTH, CMB_unit="muK")
    else:
        pp = (clpp if clpp is not None else template(foot)) * Aphi
        cl = r.get_lensed_cls_with_spectrum(pp, lmax=LTH, CMB_unit="muK")
    return {"tt": cl[:, 0], "ee": cl[:, 1], "te": cl[:, 3]}

# ------------------------------------------------------------------ likelihood (F1A box, or A6's wide box)
WIDE_P = [(0.5, 1.5), (0, 1000), (0, 1000), (0, 1000), (-5, 10), (-5, 10), (-5, 10), (0.5, 1.5), (0.5, 1.5)]
WIDE_A = [(0.3, 3.0), (0.5, 1.5)]
F1A_A = [(0.5, 1.5), (0.9, 1.1)]
def PA_box(D, x0, Pb, Ab, prior):
    """CMB3's own nuisance profile with a chosen box and prior switch (A6); with F1A's box + priors it must equal f1a.PA (KA-4)."""
    x0 = x0 or {}; P = f1a.lik("Pcut"); A = f1a.lik("A")
    fP = (lambda x: P.chi2(D, x) + P.prior(x)) if prior else (lambda x: P.chi2(D, x))
    best = None
    for s in ([np.asarray(x0["Pcut"])] if x0.get("Pcut") is not None else []) + [P.X0]:
        r = minimize(fP, np.clip(s, [b[0] for b in Pb], [b[1] for b in Pb]), method="L-BFGS-B", bounds=Pb, options=dict(maxiter=600))
        if best is None or r.fun < best.fun: best = r
    sa = np.asarray(x0["A"]) if x0.get("A") is not None else np.array([1.0, 1.0])
    ra = minimize(lambda x: A.chi2(D, x[0], x[1]), sa, method="L-BFGS-B", bounds=Ab)
    return dict(PA=float(best.fun) + float(ra.fun), Pcut=float(best.fun), A=float(ra.fun),
                nuis=dict(Pcut=best.x.tolist(), A=ra.x.tolist()))
def PA(D, x0=None, wide=False):
    return PA_box(D, x0, WIDE_P, WIDE_A, False) if wide else f1a.PA(D, x0)

# ------------------------------------------------------------------ fits
BASE_LO = dict(ob=0.0215, od=0.0, lnA=1.5, ns=0.80, tau=0.01); BASE_HI = dict(ob=0.0230, od=0.40, lnA=4.5, ns=1.30, tau=0.15)
BASE_STEP = dict(ob=3e-4, od=0.01, lnA=0.05, ns=0.02, tau=0.02)
EXTRA = {"A2U": {}, "A6F": {},
         "A2T": dict(Aphi=(0.0, 15.0, 1.0, 0.3)),
         "A3N": dict(nnu=(1.0, 6.0, 3.046, 0.3), YHe=(0.10, 0.40, None, 0.02)),
         "A4P": dict(nrun=(-0.5, 0.5, 0.0, 0.02))}

def bbn_yhe(ob, nnu=3.046):
    import camb
    p = camb.CAMBparams(); p.set_cosmology(H0=67.0, ombh2=ob, omch2=0.12, nnu=nnu, mnu=0.0, num_massive_neutrinos=0); return float(p.YHe)

def setup(X, foot, mode):
    names = ["ob"] + (["od"] if mode == "cold" else []) + ["lnA", "ns", "tau"]
    lo = dict(BASE_LO); hi = dict(BASE_HI)
    if X == "A4P": lo.update(ns=0.50, lnA=0.0); hi.update(ns=2.50, lnA=5.0)
    st = stored(foot, mode); th = st["pars"]
    x0 = [th["ob"]] + ([th["oc"]] if mode == "cold" else []) + [th["lnA"], th["ns"], th["tau"]]
    step = [BASE_STEP[n] for n in names]; L = [lo[n] for n in names]; H = [hi[n] for n in names]
    for n, (a, b, s0, d) in EXTRA[X].items():
        names.append(n); L.append(a); H.append(b); step.append(d)
        x0.append(bbn_yhe(th["ob"]) if n == "YHe" else s0)
    return names, np.array(L), np.array(H), np.array(x0), np.array(step), st

def evaluate(X, foot, mode, names, x, x0n=None):
    v = dict(zip(names, x)); od = v.get("od", 1e-7) if mode == "cold" else 1e-7
    nnu = v.get("nnu", 3.046)
    pr = dict(h=footing_h(foot, v["ob"], od if mode == "cold" else 0.0, nnu), ob=v["ob"], oc=od, lnA=v["lnA"], ns=v["ns"], tau=v["tau"])
    lens = {"A2U": "none", "A2T": "tmpl"}.get(X, "own")
    D = theory(pr, nnu=nnu, YHe=v.get("YHe"), nrun=v.get("nrun", 0.0), lens=lens, Aphi=v.get("Aphi", 1.0), foot=foot)
    return pr, PA(D, x0n, wide=(X == "A6F"))

def do_fit(X, foot, mode, maxfev=None, tag=None):
    names, lo, hi, x0, step, st = setup(X, foot, mode)
    maxfev = maxfev or (250 if mode == "cold" else 300)
    state = dict(best=None, nu={k: np.array(v) for k, v in st["chi2"]["nuis"].items()}, n=0)
    def f(x):
        x = np.asarray(x); pen = float(np.sum(np.clip(lo - x, 0, None) ** 2 + np.clip(x - hi, 0, None) ** 2)) * 1e6
        xc = np.clip(x, lo, hi)
        try:
            pr, g = evaluate(X, foot, mode, names, xc, state["nu"]); val = g["PA"] + pen
            state["nu"] = {k: np.array(v) for k, v in g["nuis"].items()}
        except Exception as e:
            val = 1e9; g = None; print("eval error", e, flush=True)
        state["n"] += 1
        if g is not None and (state["best"] is None or val < state["best"][0]): state["best"] = (val, xc.tolist(), pr, g)
        return val
    simplex = [x0] + [x0 + np.eye(len(x0))[i] * step[i] for i in range(len(x0))]
    minimize(f, x0, method="Nelder-Mead", options=dict(initial_simplex=np.array(simplex), maxfev=maxfev, xatol=1e-6, fatol=0.01))
    val, x, pr, g = state["best"]
    res = dict(X=X, foot=foot, mode=mode, names=names, theta=dict(zip(names, x)), pars=pr, chi2=g, nfev=state["n"],
               start_chi2_F1A=st["chi2"]["PA"], at_edge=[n for n, xi, a, b in zip(names, x, lo, hi) if abs(xi - a) < 1e-6 or abs(xi - b) < 1e-6],
               R=(pr["oc"] / pr["ob"] if mode == "cold" else None), peak_rss_GB=f1a.rss(), note=NOTE)
    dump(f"fit_{tag or X}_{foot}_{mode}.json", res)
    print(X, foot, mode, json.dumps(res["theta"], default=float), g["PA"], "R", res["R"], "edge", res["at_edge"], flush=True)
    return res

# ------------------------------------------------------------------ KA
def do_ka():
    out = {"KA1": {}, "KA3": {}, "KA4": {}}
    for foot in FOOT:
        for mode in ("cold", "MB"):
            st = stored(foot, mode); pr = st["pars"]; x0 = {k: np.array(v) for k, v in st["chi2"]["nuis"].items()}
            g = f1a.PA(f1a.camb_theory(**pr), x0); d = g["PA"] - st["chi2"]["PA"]
            out["KA1"][f"{foot}_{mode}"] = dict(chi2=g["PA"], stored=st["chi2"]["PA"], d=d, pass_=abs(d) <= 0.1)
            print("KA1", foot, mode, g["PA"], d, flush=True)
        c, m = out["KA1"][f"{foot}_cold"], out["KA1"][f"{foot}_MB"]
        out["KA1"][f"{foot}_DeltaMB"] = dict(value=m["chi2"] - c["chi2"], stored=m["stored"] - c["stored"],
                                             pass_=abs((m["chi2"] - c["chi2"]) - (m["stored"] - c["stored"])) <= 0.2)
        st = stored(foot, "cold"); pr = st["pars"]; x0 = {k: np.array(v) for k, v in st["chi2"]["nuis"].items()}
        r = camb_results(pr); own = r.get_lens_potential_cls(CMB_unit=None)[:, 0]
        g3 = PA(theory(pr, lens="tmpl", Aphi=1.0, clpp=own), x0); d3 = g3["PA"] - st["chi2"]["PA"]
        out["KA3"][foot] = dict(chi2=g3["PA"], stored=st["chi2"]["PA"], d=d3, pass_=abs(d3) <= 0.5); print("KA3", foot, d3, flush=True)
        k4 = {}
        g = PA(theory(pr, nnu=3.046, YHe=bbn_yhe(pr["ob"])), x0); k4["A3_switch_off"] = g["PA"] - st["chi2"]["PA"]
        g = PA(theory(pr, nrun=0.0), x0); k4["A4_switch_off"] = g["PA"] - st["chi2"]["PA"]
        g = PA_box(f1a.camb_theory(**pr), x0, f1a.CamSpec.BOUNDS, F1A_A, True); k4["A6_code_F1A_box"] = g["PA"] - st["chi2"]["PA"]
        out["KA4"][foot] = dict(d=k4, pass_=all(abs(v) <= 0.1 for v in k4.values())); print("KA4", foot, k4, flush=True)
    out["note"] = NOTE; dump("ka.json", out)

def do_ka2(foot):
    # KA-2: F1A apparatus (own lensing, F1A box), 60 NM evaluations from the stored cold best fit
    EXTRA["KA2"] = {}
    res = do_fit("KA2", foot, "cold", maxfev=60, tag="KA2")
    st = stored(foot, "cold"); R0 = st["pars"]["oc"] / st["pars"]["ob"]
    res["KA2"] = dict(dchi2=res["chi2"]["PA"] - st["chi2"]["PA"], R=res["R"], R_F1A=R0, dR=res["R"] / R0 - 1,
                      pass_=(res["chi2"]["PA"] - st["chi2"]["PA"] >= -1.0 and abs(res["R"] / R0 - 1) <= 0.005))
    dump(f"fit_KA2_{foot}_cold.json", res); print("KA2", foot, res["KA2"], flush=True)

# ------------------------------------------------------------------ A1: is the law inert at z 1100?
def nu_simple(y): return 0.5 * (1 + math.sqrt(1 + 4 / y))
def do_a1():
    z = 1100.0; ks = np.array([0.02, 0.05, 0.1, 0.2, 0.3]); MPC = f1a.MPC; c = f1a.CL; out = {}
    for foot in FOOT:
        a0 = FOOT[foot]; row = {}
        for mode in ("cold", "MB"):
            pr = stored(foot, mode)["pars"]; r = camb_results(pr)
            H = r.hubble_parameter(z) * 1e3 / MPC                            # 1/s
            ev = r.get_redshift_evolution(np.concatenate([[1e-3], ks]), [z], ["Weyl"])[:, 0, 0]
            kk = np.concatenate([[1e-3], ks]); As = math.exp(pr["lnA"]) * 1e-10
            D2R = As * (kk / 0.05) ** (pr["ns"] - 1)
            PhiW = np.abs(ev / kk ** 2) * np.sqrt(D2R)                        # rms Weyl potential per ln k (c = 1)
            g = c ** 2 * PhiW * kk * (1 + z) / MPC                            # physical gradient, m/s^2
            y = g / a0
            row[mode] = dict(cH_over_a0=c * H / a0, H_z_per_s=H, transfer_large_scale=float(abs(ev[0] / kk[0] ** 2)),
                             k=kk[1:].tolist(), PhiW=PhiW[1:].tolist(), g=g[1:].tolist(), y=y[1:].tolist(),
                             nu_minus_1=[nu_simple(v) - 1 for v in y[1:]])
            est = []
            for dlt in (1e-4, 1e-3):
                for rc in (10.0, 30.0, 100.0, 300.0):
                    gg = 0.5 * H ** 2 * dlt * rc * MPC / (1 + z); est.append(dict(delta=dlt, r_comoving_Mpc=rc, g=gg, y=gg / a0))
            row[mode]["brief_estimate"] = est
        ymb = min(row["MB"]["y"])
        row["needed"] = dict(R=stored(foot, "cold")["pars"]["oc"] / stored(foot, "cold")["pars"]["ob"])
        row["needed"]["nu_needed"] = 1 + row["needed"]["R"]
        nn = row["needed"]["nu_needed"]; row["needed"]["y_needed"] = 1 / (nn * (nn - 1))   # nu(y) = n  <=>  y = 1/(n(n-1))
        row["label"] = ("HOLDS" if ymb >= 1 else "BREAKS POSSIBLE" if ymb <= row["needed"]["y_needed"] else "BENDS")
        row["max_nu_minus_1_MB"] = max(row["MB"]["nu_minus_1"]); row["min_y_MB"] = ymb
        out[foot] = row; print("A1", foot, row["label"], "min y MB", ymb, "y cold", row["cold"]["y"], "cH/a0", row["cold"]["cH_over_a0"], flush=True)
    out["note"] = NOTE; dump("a1.json", out)

# ------------------------------------------------------------------ MUTATE
def peaks(D):
    L = np.arange(len(D["tt"])); tt = D["tt"]
    def pk(a, b): w = (L >= a) & (L <= b); i = np.argmax(tt[w]); return float(tt[w][i]), int(L[w][i])
    return dict(H1=pk(150, 320), H2=pk(420, 620), H3=pk(700, 900))
def do_mutate():
    out = {"M1": {}, "M2": {}}
    for foot in FOOT:
        sc = stored(foot, "cold"); sm = stored(foot, "MB")
        Dc = f1a.camb_theory(**sc["pars"]); Dm = f1a.camb_theory(**sm["pars"])
        pm = dict(sm["pars"]); pm["ob"] = 2 * pm["ob"]; pm["h"] = footing_h(foot, pm["ob"], 0.0)
        Dmut = f1a.camb_theory(**pm); g = f1a.PA(Dmut, {k: np.array(v) for k, v in sm["chi2"]["nuis"].items()})
        P = {n: peaks(D) for n, D in (("cold", Dc), ("MB", Dm), ("mut", Dmut))}
        oe = {n: P[n]["H1"][0] / P[n]["H2"][0] for n in P}; r32 = {n: P[n]["H3"][0] / P[n]["H2"][0] for n in P}
        d_oe = oe["mut"] / oe["MB"] - 1; rest = abs(r32["mut"] / r32["cold"] - 1)
        out["M1"][foot] = dict(peaks=P, H1_H2=oe, H3_H2=r32, d_oe=d_oe, third_peak_offset=rest, chi2_mut=g["PA"],
                               dchi2_vs_cold=g["PA"] - sc["chi2"]["PA"],
                               pass_=bool(abs(d_oe) > 0.05 and rest > 0.02 and g["PA"] - sc["chi2"]["PA"] > 25))
        print("M1", foot, json.dumps(out["M1"][foot], default=float), flush=True)
        pr = sc["pars"]; x0 = {k: np.array(v) for k, v in sc["chi2"]["nuis"].items()}; c0 = sc["chi2"]["PA"]; m2 = {}
        m2["Aphi_3"] = PA(theory(pr, lens="tmpl", Aphi=3.0, foot=foot), x0)["PA"] - c0
        p5 = dict(pr); p5["h"] = footing_h(foot, pr["ob"], pr["oc"], 5.0)
        m2["Neff_5"] = PA(theory(p5, nnu=5.0), x0)["PA"] - c0
        m2["nrun_0.10"] = PA(theory(pr, nrun=0.10), x0)["PA"] - c0
        out["M2"][foot] = dict(dchi2=m2, pass_=all(v > 25 for v in m2.values())); print("M2", foot, m2, flush=True)
    out["note"] = NOTE; dump("mutate.json", out)

# ------------------------------------------------------------------ A6 step 1 (point re-profile, wide box, no priors)
def do_a6point():
    out = {}
    for foot in FOOT:
        for mode in ("cold", "MB"):
            st = stored(foot, mode); x0 = {k: np.array(v) for k, v in st["chi2"]["nuis"].items()}
            g = PA(f1a.camb_theory(**st["pars"]), x0, wide=True)
            out[f"{foot}_{mode}"] = dict(chi2_wide=g["PA"], chi2_F1A=st["chi2"]["PA"], d=g["PA"] - st["chi2"]["PA"], nuis=g["nuis"])
            print("A6point", foot, mode, g["PA"], g["PA"] - st["chi2"]["PA"], flush=True)
    out["note"] = NOTE; dump("a6point.json", out)

# ------------------------------------------------------------------ A4 Hessian (degeneracy direction)
def do_a4hess(foot):
    fit = json.load(open(os.path.join(PARTS, f"fit_A4P_{foot}_cold.json"))); names = fit["names"]
    x = np.array([fit["theta"][n] for n in names]); h = dict(ob=1.5e-4, od=1.2e-3, lnA=0.015, ns=0.004, tau=0.008, nrun=0.008)
    hv = np.array([h[n] for n in names]); nu0 = fit["chi2"]["nuis"]
    cache = {}
    def f(dx):
        key = tuple(np.round(dx, 12))
        if key not in cache: cache[key] = evaluate("A4P", foot, "cold", names, x + dx, nu0)[1]["PA"]
        return cache[key]
    n = len(x); f0 = f(np.zeros(n)); Hm = np.zeros((n, n)); e = np.eye(n) * hv
    for i in range(n):
        Hm[i, i] = (f(e[i]) - 2 * f0 + f(-e[i])) / hv[i] ** 2
        for j in range(i):
            Hm[i, j] = Hm[j, i] = (f(e[i] + e[j]) - f(e[i] - e[j]) - f(-e[i] + e[j]) + f(-e[i] - e[j])) / (4 * hv[i] * hv[j])
    cov = np.linalg.inv(Hm / 2); sd = np.sqrt(np.abs(np.diag(cov))); corr = cov / np.outer(sd, sd)
    I = {nm: k for k, nm in enumerate(names)}
    ob, od = fit["theta"]["ob"], fit["theta"]["od"]; R = od / ob
    dRdns = (cov[I["od"], I["ns"]] / ob - od / ob ** 2 * cov[I["ob"], I["ns"]]) / cov[I["ns"], I["ns"]]
    dRdrun = (cov[I["od"], I["nrun"]] / ob - od / ob ** 2 * cov[I["ob"], I["nrun"]]) / cov[I["nrun"], I["nrun"]]
    sR = math.sqrt(max(0.0, (np.array([-od / ob ** 2, 1 / ob]) @ cov[np.ix_([I["ob"], I["od"]], [I["ob"], I["od"]])] @ np.array([-od / ob ** 2, 1 / ob]))))
    out = dict(names=names, x=x.tolist(), chi2_0=f0, hessian=Hm.tolist(), sigma=dict(zip(names, sd.tolist())), corr=corr.tolist(),
               corr_od_ns=corr[I["od"], I["ns"]], corr_od_nrun=corr[I["od"], I["nrun"]],
               dod_dns=cov[I["od"], I["ns"]] / cov[I["ns"], I["ns"]], dR_dns=dRdns, dR_dnrun=dRdrun,
               dns_for_10pct_R=abs(0.1 * R / dRdns) if dRdns else None, sigma_R=sR, R=R, n_evals=len(cache), note=NOTE)
    dump(f"a4hess_{foot}.json", out); print("A4hess", foot, json.dumps({k: out[k] for k in ("sigma", "corr_od_ns", "corr_od_nrun", "dR_dns", "dns_for_10pct_R", "sigma_R")}, default=float), flush=True)

# ------------------------------------------------------------------ A1 reading (post-freeze, REPORTED not graded): total rms gradient
def do_a1rms():
    """The law's argument is the TOTAL gradient. Its rms over all bands, g_rms^2 = int dlnk (c^2 k_phys Phi_W(k))^2, at z 1100;
    long modes act on the short ones as an external field (EFE). Reported, not graded (added after the freeze)."""
    z = 1100.0; MPC = f1a.MPC; c = f1a.CL; kk = np.logspace(-4, 0.3, 80); out = {}
    for foot in FOOT:
        a0 = FOOT[foot]; out[foot] = {}
        for mode in ("cold", "MB"):
            pr = stored(foot, mode)["pars"]; r = camb_results(pr)
            ev = r.get_redshift_evolution(kk, [z], ["Weyl"])[:, 0, 0]
            D2R = math.exp(pr["lnA"]) * 1e-10 * (kk / 0.05) ** (pr["ns"] - 1)
            gk2 = (c ** 2 * np.abs(ev / kk ** 2) * np.sqrt(D2R) * kk * (1 + z) / MPC) ** 2
            lk = np.log(kk); g_rms = math.sqrt(float(np.sum(0.5 * (gk2[1:] + gk2[:-1]) * np.diff(lk))))
            cum = np.concatenate([[0], np.cumsum(0.5 * (gk2[1:] + gk2[:-1]) * np.diff(lk))]); half = float(kk[np.searchsorted(cum, 0.5 * cum[-1])])
            y = g_rms / a0
            out[foot][mode] = dict(g_rms=g_rms, y_rms=y, nu_minus_1_at_y_rms=nu_simple(y) - 1, k_half_of_g2=half)
            print("A1rms", foot, mode, json.dumps(out[foot][mode]), flush=True)
    out["note"] = NOTE + "; reported, not graded (post-freeze reading)"; dump("a1_rms.json", out)

if __name__ == "__main__":
    a = sys.argv[1:]; t0 = time.time()
    if a[0] == "ka": do_ka()
    elif a[0] == "ka2": do_ka2(a[1])
    elif a[0] == "a1": do_a1()
    elif a[0] == "mutate": do_mutate()
    elif a[0] == "a6point": do_a6point()
    elif a[0] == "fit": do_fit(a[1], a[2], a[3])
    elif a[0] == "a4hess": do_a4hess(a[1])
    elif a[0] == "a1rms": do_a1rms()
    print(f"done {a} {time.time() - t0:.0f} s, peak RSS {f1a.rss():.2f} GB", flush=True)
