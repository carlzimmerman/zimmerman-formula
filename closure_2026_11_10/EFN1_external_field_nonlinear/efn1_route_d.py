"""EFN1 route D (criteria 98364c8d20, amendment A1 c3e466efbf): time-stepping the nonlinear clock / gravity equations from
the static state plus a seed.  Usage:  python3 efn1_route_d.py <batch>   with batch in
  main     graded 12 backgrounds x {R2, R3, R4} and R3 with dt halved (A1 reading)
  ka       KA-c isolated twins, KA-d full form, KA-d zero seed (perturbative), KA-b2 eigen-seeded linear run (needs route W)
  mutate   M1 (eps x 10), M2 (nonlinear signs flipped), M3 (linear) on the four mutation backgrounds (R3)
  frozen   the frozen reading (plane rows dynamic) on canonical / alt expo 9.4 at R3 and R4
  ext      0.01 a0 axial expo 9.4, both footings, R3 and R4
Writes efn1_route_d_<batch>.json / .out (MUTATE batch: efn1_route_d_MUTATE.json / .out).  Each finished run is written to
the json as it lands; SIGTERM stops cleanly after the current step with the partial json kept (finished runs are skipped on
restart).  States are not dumped; histories are small arrays.
"""
import os, sys, json, math, time, signal, resource
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import efn1_core as C

STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__("flag", True))
FOOTER = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."


def fit_rate(t, a, t0, t1):
    t = np.asarray(t); a = np.asarray(a)
    m = (t >= t0) & (t <= t1) & (a > 0)
    if m.sum() < 3:
        return None
    return float(np.polyfit(t[m], np.log(a[m]), 1)[0])


def run(spec):
    foot, kind, logm, ge, res = spec["foot"], spec["kind"], spec["logm"], spec["ge"], spec["res"]
    eps = spec.get("eps", 1e-4); sig = spec.get("sig", 1); dtfac = spec.get("dtfac", 1.0)
    mode = spec.get("mode", "pert"); iso = spec.get("isolated", False); seed = spec.get("seed", "smooth")
    sheet_static = spec.get("sheet_static", True); tend_e = spec.get("tend_efolds", 30.0)      # A2: 30 e-folds
    ref = C.scs3_rate(foot, kind, logm, ge)
    Gam = ref["gamma_tu"]
    bg = C.background(foot, kind, logm, ge, res, isolated=iso)
    o = C.Ops(bg, sheet_static=sheet_static)
    N0ref = o.N0min
    if iso:
        # the isolated twin keeps the r_e (hence r_in), the seed centre and the normalisation of its external-field twin
        oe = C.Ops(C.background(foot, kind, logm, ge, res, isolated=False), sheet_static=sheet_static)
        o.istar = oe.istar; N0ref = oe.N0min; del oe
    norm = abs(N0ref)
    cmask = o.Didx[np.abs(o.N0[o.Didx]) >= 0.2 * norm]                                     # A2: cells for c(t)
    negD = o.Didx[o.N0[o.Didx] < 0]
    t_start = time.time()
    pi = np.zeros(o.n)
    if seed == "smooth":
        n = o.seed_n(eps, sign=spec.get("seed_sign", 1.0))
    elif seed == "none":
        n = np.zeros(o.n)
    else:                                                   # eigen seed (KA-b2): pure growing linear mode
        ev = spec["eig"]
        p = np.zeros(o.n); p[o.Didx] = ev
        q = (o.Cmat() @ ev) / (C.K * o.V) / math.sqrt(spec["lam"])
        sc = eps * norm / np.max(np.abs(q[o.Didx]))
        pi = p * sc; n = q * sc
    phi_extra = None
    if mode == "full":
        phi_extra = -o.Lp_lu.solve(o.resP())
    def amp(nv):
        a_ = np.abs(nv[o.Didx]); i = int(np.argmax(a_)); return float(a_[i] / norm), int(o.Didx[i])
    def camp(nv):
        c_ = np.abs(nv[cmask]) / np.abs(o.N0[cmask]); i = int(np.argmax(c_)); return float(c_[i]), int(cmask[i])
    a0_, _ = amp(n); c0_, _ = camp(n)
    dt_base = min(0.02 / Gam, 0.25 / o.omega_max) * dtfac
    dt0 = dt_base
    t = 0.0; tend = tend_e / Gam
    tH = 13.8 / C.TU_GYR
    miles = sorted(m_ for m_ in (14.0 / Gam, tH) if m_ < tend)
    snaps = {}
    hist = dict(tG=[], c=[], c_r_re=[], c_th=[], a=[], a_r_re=[], a_th=[], a_neg=[], neg_r_re=[], neg_th=[], vmax=[], dtG=[],
                nmin=[], nmax=[], newton=[])
    next_rec = 0.0; s_prev = None; stop = None; steps = 0; newton_max = 0
    last_good = (pi.copy(), n.copy())
    def rec():
        a_, k = amp(n); c_, kc = camp(n); v, _ = o.vmax_dt(pi)
        hist["tG"].append(t * Gam); hist["c"].append(c_); hist["c_r_re"].append(float(o.rcell[kc] / o.re))
        hist["c_th"].append(float(np.degrees(o.thcell[kc])))
        hist["a"].append(a_); hist["a_r_re"].append(float(o.rcell[k] / o.re)); hist["a_th"].append(float(np.degrees(o.thcell[k])))
        hist["vmax"].append(v); hist["dtG"].append(dt * Gam)
        hist["nmin"].append(float(n[o.Didx].min() / norm)); hist["nmax"].append(float(n[o.Didx].max() / norm))
        hist["newton"].append(newton_max)
        if len(negD):
            an = np.abs(n[negD]); j_ = int(np.argmax(an)); kk = negD[j_]
            hist["a_neg"].append(float(an[j_] / norm)); hist["neg_r_re"].append(float(o.rcell[kk] / o.re)); hist["neg_th"].append(float(np.degrees(o.thcell[kk])))
    def snapshot():
        _, _, inf = o.rhs(pi, n, sig=0, phi_extra=phi_extra)
        a_, k = amp(n); c_, kc = camp(n)
        return dict(t_efolds=float(t * Gam), t_gyr=float(t * C.TU_GYR), c=c_, c_at=[float(o.rcell[kc] / o.re), float(np.degrees(o.thcell[kc]))],
                    a=a_, a_at=[float(o.rcell[k] / o.re), float(np.degrees(o.thcell[k]))],
                    a_neg=float(np.abs(n[negD]).max() / norm) if len(negD) else None, dg=o.dg(inf["phi"]), vmax_kms=o.vmax_dt(pi)[0])
    dt = dt0
    while t < tend - 1e-12:
        if STOP["flag"]:
            return None
        v, hv = o.vmax_dt(pi)
        dt = min(dt_base, 0.25 * dtfac * hv, tend - t)
        if miles and t + dt > miles[0]:
            dt = miles[0] - t
        if dt < 1e-3 * dt0 and not (miles and abs(t + dt - miles[0]) < 1e-12) and t + dt < tend - 1e-12:
            stop = "F3 dt collapse"; break
        if t >= next_rec - 1e-12:
            rec(); next_rec += 0.1 / Gam
        ok = True; its = 0
        def f(pi_, n_):
            nonlocal s_prev, ok, its
            a_, b_, info = o.rhs(pi_, n_, sig=sig, s_prev=s_prev, phi_extra=phi_extra)
            if info["s"] is not None:
                s_prev = info["s"]
            ok = ok and info["ok"]; its = max(its, info["it"])
            return a_, b_
        k1 = f(pi, n)
        k2 = f(pi + 0.5 * dt * k1[0], n + 0.5 * dt * k1[1])
        k3 = f(pi + 0.5 * dt * k2[0], n + 0.5 * dt * k2[1])
        k4 = f(pi + dt * k3[0], n + dt * k3[1])
        newton_max = its
        if not ok:
            stop = "F2 inverse map"; break
        pi = pi + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        n = n + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        t += dt; steps += 1
        if not (np.all(np.isfinite(pi)) and np.all(np.isfinite(n))):
            stop = "F4 non-finite"; pi, n = last_good; t -= dt; break
        last_good = (pi.copy(), n.copy())
        if miles and abs(t - miles[0]) < 1e-9 * tend:
            snaps["14_efolds" if abs(miles[0] - 14.0 / Gam) < 1e-9 * tend else "t_H"] = snapshot(); miles.pop(0)
        if camp(n)[0] >= 10:
            stop = "F1 density fold (c >= 10)"; break
    rec()
    snaps["end"] = snapshot()
    tG = np.array(hist["tG"]); cc = np.array(hist["c"]); aa = np.array(hist["a"])
    i14 = tG <= 14.0 + 1e-9
    frozen = dict(a_reaches_10_before_14=bool(np.any(aa[i14] >= 10)), a_at_14=float(aa[i14][-1]),
                  a_rate_last3_to14=fit_rate(tG[i14], aa[i14], 11.0, 14.0))
    t_c = tG[np.argmax(cc >= 1e-2)] if np.any(cc >= 1e-2) else tG[-1]
    out = dict(spec={k_: v_ for k_, v_ in spec.items() if k_ not in ("eig",)}, scs3=dict(efold_gyr=ref["efold_gyr"], label=ref["label"], where=ref["where"]),
               grid=list(bg["g"].shape[:2]), n_dynamic=int(len(o.Didx)), n_c_cells=int(len(cmask)), a0=a0_, c0=c0_,
               omega_max_over_G=o.omega_max / Gam, efolds_in_tH=float(tH * Gam),
               route_L_max_efold_gyr=float(C.TU_GYR / math.sqrt(max(o.loc2[o.istar], 1e-300))),
               route_L_max_at=[float(o.rcell[o.istar] / o.re), float(np.degrees(o.thcell[o.istar]))],
               stop=stop, tF_efolds=float(t * Gam) if stop else None, tF_gyr=float(t * C.TU_GYR) if stop else None,
               t_end_efolds=float(t * Gam), steps=steps, snaps=snaps,
               rate_early=fit_rate(tG, cc, 1.0, t_c), rate_last3=fit_rate(tG, cc, tG[-1] - 3, tG[-1]),
               c_last3_maxmin=float(cc[tG >= tG[-1] - 3].max() / max(cc[tG >= tG[-1] - 3].min(), 1e-300)),
               frozen_reading=frozen, background_residual=bg["residual"], seconds=round(time.time() - t_start, 1),
               hist={k_: [float(f"{x_:.6g}") if isinstance(x_, float) else x_ for x_ in v_] for k_, v_ in hist.items()})
    for k_ in ("rate_early", "rate_last3"):
        if out[k_] is not None:
            out[k_] = out[k_] / Gam                         # in units of Gamma_ref
    if frozen["a_rate_last3_to14"] is not None:
        frozen["a_rate_last3_to14"] /= Gam
    return out


def tag(spec):
    return "_".join(str(spec.get(k_, "")) for k_ in ("name", "foot", "kind", "logm", "ge", "res")).replace(".", "p")


def batch_specs(b):
    L = []
    if b == "main":
        for foot, lst in C.GRADED.items():
            for kind, lm in lst:
                for res in (2, 3, 4):
                    L.append(dict(name="primary", foot=foot, kind=kind, logm=lm, ge=0.1, res=res))
                L.append(dict(name="dthalf", foot=foot, kind=kind, logm=lm, ge=0.1, res=3, dtfac=0.5))
    elif b == "mutate":
        for foot, kind, lm in C.MUT_SET:
            L.append(dict(name="M1_eps1e-3", foot=foot, kind=kind, logm=lm, ge=0.1, res=3, eps=1e-3))
            L.append(dict(name="M2_signflip", foot=foot, kind=kind, logm=lm, ge=0.1, res=3, sig=-1))
            L.append(dict(name="M3_linear", foot=foot, kind=kind, logm=lm, ge=0.1, res=3, sig=0))
            L.append(dict(name="M2b_seedsign", foot=foot, kind=kind, logm=lm, ge=0.1, res=3, seed_sign=-1.0))
    elif b == "ka":
        for foot, kind, lm in C.MUT_SET:
            L.append(dict(name="KAc_isolated", foot=foot, kind=kind, logm=lm, ge=0.1, res=3, isolated=True))
            L.append(dict(name="KAd_full_noseed", foot=foot, kind=kind, logm=lm, ge=0.1, res=3, mode="full", seed="none"))
        for foot, lst in C.GRADED.items():
            for kind, lm in lst:
                L.append(dict(name="KAd_pert_noseed", foot=foot, kind=kind, logm=lm, ge=0.1, res=3, seed="none", tend_efolds=2.0))
    elif b == "frozen":
        for foot in ("canonical", "alt"):
            for res in (3, 4):
                L.append(dict(name="frozen_sheet_dynamic", foot=foot, kind="expo", logm="9.4", ge=0.1, res=res, sheet_static=False))
    elif b == "frozenlin":                     # reported diagnostic (not graded): the frozen reading's runs with the nonlinear terms off
        for foot in ("canonical", "alt"):
            L.append(dict(name="frozen_sheet_dynamic_M3_linear", foot=foot, kind="expo", logm="9.4", ge=0.1, res=3, sheet_static=False, sig=0))
    elif b == "ext":
        for foot in ("canonical", "alt"):
            for res in (3, 4):
                L.append(dict(name="ext_0p01", foot=foot, kind="expo", logm="9.4", ge=0.01, res=res))
    elif b == "kab2":
        W = json.load(open(os.path.join(HERE, "efn1_route_w.json")))
        for foot, kind, lm in C.MUT_SET:
            key = f"{foot}_{kind}_{lm}_R3"
            ev = np.load(os.path.join(C.CACHE, f"eig_{key}.npy"))
            L.append(dict(name="KAb2_eigseed_linear", foot=foot, kind=kind, logm=lm, ge=0.1, res=3, seed="eig", sig=0,
                          eps=1e-8, tend_efolds=5.0, eig=ev, lam=W["rows"][key]["lam"]))
    return L


if __name__ == "__main__":
    b = sys.argv[1]
    only = sys.argv[2] if len(sys.argv) > 2 else None
    name = "MUTATE" if b == "mutate" else b
    jpath = os.path.join(HERE, f"efn1_route_d_{name}.json"); opath = os.path.join(HERE, f"efn1_route_d_{name}.out")
    RES = json.load(open(jpath)) if os.path.exists(jpath) else dict(lane="EFN1", script="efn1_route_d.py", batch=b,
                                                                     criteria="98364c8d20", amendment_A1="c3e466efbf", runs={})
    for spec in batch_specs(b):
        tg = tag(spec)
        if only and only not in tg:
            continue
        if tg in RES["runs"]:
            continue
        r = run(spec)
        if r is None:
            print("SIGTERM: stopped; partial json kept", flush=True); break
        RES["runs"][tg] = r
        RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
        RES["footer"] = FOOTER
        json.dump(RES, open(jpath + ".tmp", "w"), indent=0); os.replace(jpath + ".tmp", jpath)
        e = r["snaps"]["end"]
        line = (f"[{tg}] grid {r['grid']} nD {r['n_dynamic']} c0 {r['c0']:.2e} stop {r['stop']} tF {r['tF_efolds']} e-folds "
                f"({r['tF_gyr']} Gyr); t_end {r['t_end_efolds']:.2f}; c_end {e['c']:.3e} at {e['c_at'][0]:.3f} r_e {e['c_at'][1]:.1f} deg; "
                f"rate early {r['rate_early']} last3 {r['rate_last3']} (Gamma_ref); c last-3 max/min {r['c_last3_maxmin']:.3g}; "
                f"dg_end (r/r_e: theta max) " + ", ".join(f"{k_}: {v_[0]:.3g}" for k_, v_ in e['dg'].items())
                + f"; vmax {e['vmax_kms']:.3g} km/s; at 14 e-folds c {r['snaps'].get('14_efolds', {}).get('c')}; "
                f"at t_H c {r['snaps'].get('t_H', {}).get('c')}; frozen a: {r['frozen_reading']}; steps {r['steps']}; {r['seconds']} s")
        print(line, flush=True)
        with open(opath, "a") as fh:
            fh.write(line + "\n")
    print(FOOTER)
