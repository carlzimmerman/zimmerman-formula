#!/usr/bin/env python3
"""CFG646 (i): anatomy of CFG596's canonical raw-KiDS / DES dchi2 (POST HOC DIAGNOSTIC, no verdict change; DECLARATIONS.md 3c1c5a42f).
Uses cfg596_native.py's library (and CFG592's) unchanged; same data, cuts, nuisances, priors, fit routine.
  nice -n 10 python3 cfg646_anatomy.py  -> cfg646_anatomy.out, cfg646_anatomy.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import cfg646_lib as LB
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
NS = LB.load_ns()
Pmat, fit, theory, nuis_spec, subset, SURV = (NS[k] for k in ("Pmat", "fit", "theory", "nuis_spec", "subset", "SURV"))
REF = {"KiDS": 68.72643037972006, "DES": 22.365007549756143}
P("CFG646 (i) anatomy of CFG596 canonical dchi2 (post hoc diagnostic; no verdict change). kappa = 1/2 FITTED; not theory closed.")
RES = dict(lane="CFG646", part="i_anatomy", declarations="3c1c5a42f", surveys={})
for foot, run, held, extra, B0, F, S in LB.runs(NS):
    if foot != "canonical": continue
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F"); KK = LB.KK_of(NS)
    for sn, Sv in SURV.items():
        keep = LB.keep_mask(NS, Sv, run, PS0); D = subset(Sv, keep)
        s0 = fit(Sv, D, PS0); fF = fit(Sv, D, PF); d = fF["chi2"] - s0["chi2"]
        a0ok = abs(d - REF[sn]) <= 0.05
        P(f"\n=== {sn} (canonical, N_kept {D['N']}): dchi2 {d:+.3f} (CFG596 {REF[sn]:+.3f}) -> A0 {'PASS' if a0ok else 'FAIL'}")
        r = dict(N=D["N"], dchi2=d, A0=a0ok, chi2_S0=s0["chi2"], chi2_F=fF["chi2"])
        if not a0ok:
            RES["surveys"][sn] = r; continue
        _, _, _, unpack, prior = nuis_spec(Sv, 1.0, True)
        rS = D["d"] - s0["t"]; rF = D["d"] - fF["t"]; Ci = D["Cinv"]
        cS = rS * (Ci @ rS); cF = rF * (Ci @ rF); dc = cF - cS
        dprior = prior(np.array(fF["x"])) - prior(np.array(s0["x"]))
        tF_fix = theory(Sv, D, unpack(np.array(s0["x"])), PF, "PM"); rFx = D["d"] - tF_fix; cFx = rFx * (Ci @ rFx); dcx = cFx - cS
        P(f"  check: sum c_i(F) - sum c_i(S0) = {dc.sum():+.3f}, prior diff {dprior:+.3f}, total {dc.sum() + dprior:+.3f}; "
          f"fixed-nuisance (F at S0's best nuisances) dchi2 {dcx.sum():+.3f}")
        rows = [rw for rw, kp in zip(Sv["rows"], keep) if kp]
        sgn = np.array([rw[0] for rw in rows]); ang = np.array([rw[4] for rw in rows]); pair = np.array([f"{rw[1]}{rw[2]}" for rw in rows])
        fr, kmed = LB.kfractions(NS, Sv, run, PS0); fr = fr[:, keep]; kmed = kmed[keep]
        # model difference per point at fixed (S0) nuisances, in units of the diagonal error
        sig = np.sqrt(np.diag(Sv["cov"][np.ix_(keep, keep)])); dm = (tF_fix - s0["t"]) / sig
        def grp(lab):
            g = {}
            for L_ in sorted(set(lab), key=lambda x: (str(type(x)), x)):
                m = lab == L_
                g[str(L_)] = dict(n=int(m.sum()), dchi2=float(dc[m].sum()), dchi2_fixed=float(dcx[m].sum()),
                                  f_k_gt1=float(fr[2:, m].sum(0).mean()), kmed=float(np.median(kmed[m])), dmodel_sigma_mean=float(dm[m].mean()))
            return g
        r.update(dprior=dprior, dchi2_fixed=float(dcx.sum()))
        r["by_xi"] = grp(sgn); r["by_theta"] = grp(np.round(ang, 2)); r["by_pair"] = grp(pair)
        kb = np.digitize(kmed, [0.3, 0.5, 1.0, 2.0]); names = ["kmed<0.3", "0.3-0.5", "0.5-1", "1-2", ">2"]
        r["by_kmed"] = grp(np.array([names[i] for i in kb]))
        r["k_fraction_mean"] = dict(zip(["<0.3", "0.3-1", "1-2", ">2"], [float(v) for v in fr.mean(1)]))
        # dchi2-weighted k fractions (where the per-point dchi2 lives in k)
        w = dc; r["k_fraction_dchi2_weighted"] = dict(zip(["<0.3", "0.3-1", "1-2", ">2"], [float((fr[i] * w).sum() / w.sum()) for i in range(4)]))
        w2 = dcx; r["k_fraction_dchi2fixed_weighted"] = dict(zip(["<0.3", "0.3-1", "1-2", ">2"], [float((fr[i] * w2).sum() / w2.sum()) for i in range(4)]))
        for nm, gg in (("xi", r["by_xi"]), ("theta", r["by_theta"]), ("pair", r["by_pair"]), ("median k", r["by_kmed"])):
            P(f"  by {nm}: " + "; ".join(f"{k_} n{v['n']} {v['dchi2']:+.1f} (fixed {v['dchi2_fixed']:+.1f}, k>1 frac {v['f_k_gt1']:.2f})" for k_, v in gg.items()))
        P(f"  mean k fractions of kept points: {({k_: round(v, 3) for k_, v in r['k_fraction_mean'].items()})}; "
          f"dchi2-weighted: {({k_: round(v, 3) for k_, v in r['k_fraction_dchi2_weighted'].items()})}; fixed-nuisance weighted: "
          f"{({k_: round(v, 3) for k_, v in r['k_fraction_dchi2fixed_weighted'].items()})}")
        # k-swap refits
        sw = {}
        for kc in (0.3, 0.5, 1.0, 2.0):
            lo = fit(Sv, D, np.where(KK < kc, PF, PS0))["chi2"] - s0["chi2"]
            hi = fit(Sv, D, np.where(KK < kc, PS0, PF))["chi2"] - s0["chi2"]
            sw[str(kc)] = dict(F_below=lo, F_above=hi)
            P(f"  k-swap k_c {kc}: framework only below k_c -> dchi2 {lo:+.2f}; framework only above k_c -> dchi2 {hi:+.2f}")
        r["kswap"] = sw
        RES["surveys"][sn] = r
P(f"\n({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "cfg646_anatomy.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg646_anatomy.out"), "w").write("\n".join(OUT) + "\n")
