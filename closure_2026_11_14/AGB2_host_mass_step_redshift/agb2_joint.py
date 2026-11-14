"""AGB2 Part J (criteria: FROZEN_CRITERIA.md, section "Part J").

The host measurement of the age slope (agb2_H.json) used as a Gaussian prior on the amplitude A of AGB1's Part A
model (DESI DR2 BAO + Dovekie supernovae, flat w0-wa, mu + M + A x T_S). AGB1's fitter and outputs are imported
unchanged from closure_2026_11_13/AGB1_progenitor_age_bias/.

  f(A): best chi2 at fixed A (AGB1's committed profile);  t(A): the same with q0 = 0 imposed;
  n(A): the same with q(z) >= 0 imposed on 0 <= z <= 2.33.
  joint amplitude: f + prior;  today: min[t + prior] - min[f + prior];  ever: min[n + prior] - min[f + prior].

Usage: python3 agb2_joint.py selftest [outdir]   pure arithmetic on made-up parabolas, reads no data
       python3 agb2_joint.py J [outdir]          the real thing; writes agb2_J.json"""
import json, os, sys, time
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
AGB1 = os.path.normpath(os.path.join(HERE, "..", "..", "closure_2026_11_13", "AGB1_progenitor_age_bias"))
MODE = sys.argv[1] if len(sys.argv) > 1 else "J"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else HERE
LO, HI = -1.0, 2.0
GRID_F = [round(x, 2) + 0.0 for x in np.arange(LO, HI + 1e-9, 0.1)]
GRID_N = [round(x, 2) + 0.0 for x in np.arange(LO, HI + 1e-9, 0.25)]
FINE = np.round(np.arange(LO, HI + 1e-9, 0.001), 3)


def smin(As, cs, prior):
    """Minimum over A of spline(As, cs) + prior on the fine grid: (A, value, spline, on the edge of the grid)."""
    sp = CubicSpline(As, cs); v = sp(FINE) + prior(FINE); i = int(np.argmin(v))
    return float(FINE[i]), float(v[i]), sp, bool(i == 0 or i == len(FINE) - 1)


def joint(Af, f, q0f, An, n, t, ah=None, sh=None):
    """Joint amplitude and the today / ever statistics. ah, sh: host amplitude and its error (None: no prior)."""
    prior = (lambda A: ((np.asarray(A, float) - ah)/sh)**2) if sh else (lambda A: 0.0*np.asarray(A, float))
    Aj, cj, spf, edge = smin(Af, f, prior)
    tot = spf(FINE) + prior(FINE) - cj

    def cross(level):
        i = int(np.argmin(tot)); above = tot >= level
        jl = np.where(above[:i])[0]; jr = np.where(above[i:])[0]
        return [float(FINE[jl[-1]]) if len(jl) else None, float(FINE[i + jr[0]]) if len(jr) else None]
    At, ct, _, edge_t = smin(Af, t, prior); Av, cv, _, edge_n = smin(An, n, prior)
    return dict(A=Aj, D_A0=float(spf(0.0) + prior(0.0) - cj), D_A1=float(spf(1.0) + prior(1.0) - cj), ci68=cross(1.0), ci95=cross(4.0),
                q0=float(np.interp(Aj, Af, q0f)), D_today=ct - cj, A_today=At, D_never=cv - cj, A_never=Av,
                edge=dict(joint=edge, today=edge_t, never=edge_n), prior=[ah, sh])


def selftest(log):
    Af = np.array(GRID_F); An = np.array(GRID_N)
    f = ((Af - 0.6)/0.43)**2 + 100.0; t = f + 3.0 + 10.0*(Af - 1.2)**2; n = ((An - 0.6)/0.43)**2 + 130.0 + 5.0*(An - 1.0)**2
    q0 = -0.37 + 0.5*Af
    r0 = joint(Af, f, q0, An, n, t)
    ah, sh = 0.1, 0.4; r = joint(Af, f, q0, An, n, t, ah, sh)
    w1, w2 = 1/0.43**2, 1/sh**2; a_exact = (0.6*w1 + ah*w2)/(w1 + w2)
    d0_exact = (w1 + w2)*a_exact**2; d1_exact = (w1 + w2)*(a_exact - 1)**2
    # today with the prior, exact: minimise (w1 (A-.6)^2 + 3 + 10 (A-1.2)^2 + w2 (A-ah)^2) - joint minimum
    c2 = w1 + 10 + w2; c1 = w1*0.6 + 12.0 + w2*ah; c0 = w1*0.36 + 3 + 14.4 + w2*ah*ah
    jmin = w1*0.36 + w2*ah*ah - (w1*0.6 + w2*ah)**2/(w1 + w2)
    dt_exact = c0 - c1*c1/c2 - jmin
    ok = (abs(r0["A"] - 0.6) <= 1e-3 and abs(r0["D_A0"] - (0.6/0.43)**2) <= 1e-3 and abs(r0["D_A1"] - (0.4/0.43)**2) <= 1e-3
          and abs(r["A"] - a_exact) <= 1e-3 and abs(r["D_A0"] - d0_exact) <= 1e-3 and abs(r["D_A1"] - d1_exact) <= 1e-3
          and abs(r["D_today"] - dt_exact) <= 1e-3 and abs(r["q0"] - (-0.37 + 0.5*a_exact)) <= 1e-3)
    log(f"selftest: no prior A {r0['A']:.3f} (0.6) dchi2 {r0['D_A0']:.4f} {r0['D_A1']:.4f}; with prior A {r['A']:.4f} ({a_exact:.4f})"
        f" dchi2(0) {r['D_A0']:.4f} ({d0_exact:.4f}) dchi2(1) {r['D_A1']:.4f} ({d1_exact:.4f}) today {r['D_today']:.4f} ({dt_exact:.4f})"
        f" -> {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    t0 = time.time(); log = lambda s: print(s, flush=True)
    log(f"AGB2 joint, mode {MODE}")
    if MODE == "selftest":
        sys.exit(0 if selftest(log) else 1)
    sys.argv = ["agb1_run.py", "AGB2_J"]; sys.path.insert(0, AGB1)
    import agb1_run as R1, agb1_template as TPL
    H = json.load(open(os.path.join(HERE, "agb2_H.json")))["fits"]
    hosts = dict(H1_R=H["primary"]["H1"], H1_P=H["fork_P"]["H1"], H2_R=H["primary"]["H2"])
    for k, v in hosts.items(): log(f"host amplitude {k}: A {v['A']:+.4f} +- {v['sd_A']:.4f}")
    A1res = json.load(open(os.path.join(AGB1, "agb1_results.json")))["A"]
    res = dict(mode="J", grid_f=GRID_F, grid_n=GRID_N, hosts={k: [v["A"], v["sd_A"]] for k, v in hosts.items()}, samples={}); kj_ok = True
    for sample in ("full", "des_only"):
        J1 = json.load(open(os.path.join(AGB1, f"agb1_A_{sample}.json"))); prof = J1["profile"]; key = lambda a: f"{a:+.2f}"
        sn = R1.SN(sample); bao = R1.BAO("all"); sn.add_template("age", TPL.T(sn.z, "S")); F = R1.Fitter("A", sn, bao)
        log(f"sample {sample}: {sn.n} supernovae; AGB1 profile read on A = {LO} ... {HI}")
        f = {a: prof[key(a)]["chi2"] for a in GRID_F}; q0 = {a: prof[key(a)]["q0"] for a in GRID_F}
        refit = {a: F.fit({"age": a}, [], extra=(prof[key(a)],))["chi2"] - f[a] for a in (0.0, 1.0)}
        t, n, prev, tfit = {}, {}, None, {}
        for a in GRID_F:
            r = F.fit({"age": a}, [], "today", extra=(prof[key(a)], prev)); prev = r; tfit[a] = r
            if r["chi2"] < f[a] - 1e-7:              # a constrained fit can never beat the unconstrained one
                b = F.fit({"age": a}, [], "free", extra=(r, prof[key(a)])); log(f"  A {a:+.2f}: free fit improved by {f[a] - b['chi2']:.2e} from the q0 = 0 point")
                f[a] = min(f[a], b["chi2"])
            t[a] = r["chi2"]
            log(f"  A {a:+.2f}  f {f[a]:10.4f}  q0 {q0[a]:+.4f} | q0 = 0: {t[a]:10.4f} (+{t[a] - f[a]:.3f})")
        prev = None
        for a in GRID_N:
            r = F.fit({"age": a}, [], "never", extra=(tfit[a], prof[key(a)], prev)); prev = r; n[a] = r["chi2"]
            log(f"  A {a:+.2f}  never accelerated: {n[a]:10.4f} (+{n[a] - f[a]:.3f})  Om {r['Om']:.4f} w0 {r['w0']:+.4f} wa {r['wa']:+.4f} min q {r['qmin']:+.5f} edge {r['edge']}")
        Af = np.array(GRID_F); An = np.array(GRID_N)
        fa, ta, qa, na = (np.array([d[a] for a in g]) for d, g in ((f, GRID_F), (t, GRID_F), (q0, GRID_F), (n, GRID_N)))
        none = joint(Af, fa, qa, An, na, ta)
        fk = J1["forks"]
        kj = dict(D_A0=[none["D_A0"], A1res[sample]["D_A0"]], D_A1=[none["D_A1"], A1res[sample]["D_A1"]], refit=refit,
                  today_A0=[t[0.0] - f[0.0], fk["A0"]["D_today"]], today_A1=[t[1.0] - f[1.0], fk["A1"]["D_today"]],
                  never_A0=[n[0.0] - f[0.0], fk["A0"]["D_never"]], never_A1=[n[1.0] - f[1.0], fk["A1"]["D_never"]])
        ok = (abs(kj["D_A0"][0] - kj["D_A0"][1]) <= 0.02 and abs(kj["D_A1"][0] - kj["D_A1"][1]) <= 0.02
              and all(abs(v) <= 1e-3 for v in refit.values())
              and all(abs(kj[k][0] - kj[k][1]) <= 0.01 for k in ("today_A0", "today_A1", "never_A0", "never_A1")))
        kj["passed"] = bool(ok); kj_ok = kj_ok and ok
        log(f"KJ {sample}: no prior dchi2(A=0) {kj['D_A0'][0]:.4f} (AGB1 {kj['D_A0'][1]:.4f})  dchi2(A=1) {kj['D_A1'][0]:.4f} ({kj['D_A1'][1]:.4f});"
            f" refit at A = 0, 1: {refit[0.0]:+.1e} {refit[1.0]:+.1e}; today A=0 {kj['today_A0'][0]:.3f} ({kj['today_A0'][1]:.3f}) A=1 {kj['today_A1'][0]:.3f}"
            f" ({kj['today_A1'][1]:.3f}); never A=0 {kj['never_A0'][0]:.3f} ({kj['never_A0'][1]:.3f}) A=1 {kj['never_A1'][0]:.3f} ({kj['never_A1'][1]:.3f})"
            f" -> {'PASS' if ok else 'FAIL'}")
        out = dict(n_sn=sn.n, f=fa.tolist(), t=ta.tolist(), n=na.tolist(), q0=qa.tolist(), no_prior=none, KJ=kj, joint={})
        for hk, hv in hosts.items():
            r = joint(Af, fa, qa, An, na, ta, hv["A"], hv["sd_A"]); out["joint"][hk] = r
            log(f"  joint with {hk}: A {r['A']:+.3f} 68% {r['ci68']} 95% {r['ci95']}  dchi2(A=0) {r['D_A0']:.3f}  dchi2(A=1) {r['D_A1']:.3f}"
                f" | q0 at the joint best A {r['q0']:+.3f}; q0 = 0: dchi2 {r['D_today']:.3f} (at A {r['A_today']:+.3f});"
                f" never accelerated: dchi2 {r['D_never']:.3f} (at A {r['A_never']:+.3f})  edges {r['edge']}")
        a1, s1 = A1res[sample]["A"], 0.5*(A1res[sample]["ci68"][1] - A1res[sample]["ci68"][0])
        out["tension"] = {hk: (hv["A"] - a1)/np.hypot(hv["sd_A"], s1) for hk, hv in hosts.items()}
        log(f"  difference host minus distances in combined errors: " + ", ".join(f"{k} {v:+.2f}" for k, v in out["tension"].items()))
        res["samples"][sample] = out
    res["KJ_passed"] = bool(kj_ok); res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(OUTDIR, "agb2_J.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb2_J.json  ({res['seconds']} s)")


if __name__ == "__main__":
    main()
