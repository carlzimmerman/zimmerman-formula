#!/usr/bin/env python3
"""CFG960 scorer (FROZEN_CRITERIA.md section 3) = the frozen CFG654 scorer, unchanged.

The CFG654 scorer file (../CFG654_independent_inputs/cfg654_native.py, sha256 e5e3da3bf442e1b9...) is imported read-only by path and
its sha256 asserted.  load_lib("native_cmb"), build, klass and CMB_GATE are used as they are; score_production below is that file's
production control flow copied VERBATIM, with only the file locations changed (framework run from _external_data/cfg960_work/<JOB>/,
the control NCS0 from _external_data/cfg654_work/NCS0/, outputs in this folder).  Statistic, data, covariances, n(z), published and
support cuts, nuisances, IA marginalisation, robustness {widen2, noIA, held, LOC}, DESI reported only, T-OWN and NZ1 (MUTATE first),
classes and benchmark are CFG654's (FROZEN_CRITERIA + A1).
  OMP_NUM_THREADS=1 CFG596_MUTATE=1 nice -n 10 python3 cfg960_score.py --score SC1x   (FIRST; exit 0)
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg960_score.py --score SC1x
      -> cfg960_score_results_SC1x[_MUTATE].json / cfg960_score_SC1x[_MUTATE].out   (SC2x the same)
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg960_score.py --scorek    (V-SCORE: re-scores the stored NC1x / NC2x, compares with
      CFG654's committed result JSONs; writes cfg960_scorek.{out,json} only)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, glob, time, hashlib, importlib.util, resource, threading
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
RSSMAX = float(os.environ.get("CFG960_RSSMAX", "1.0"))           # in-script RSS guard (CFG960 compute rule)
def _guard():
    while True:
        r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
        if r > RSSMAX:
            sys.stderr.write(f"CFG960 RSS GUARD: peak {r:.3f} GB > {RSSMAX} GB -> abort\n"); sys.stderr.flush(); os._exit(3)
        time.sleep(0.25)
threading.Thread(target=_guard, daemon=True).start()

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(CFG, "..", "..", "_external_data"))
D654 = os.path.join(CFG, "CFG654_independent_inputs")
SC_PATH = os.path.join(D654, "cfg654" + "_native.py")
SC_SHA = "e5e3da3bf442e1b91797c19e232e828d996c4b1c2d91753ebfc42d0ffc79e67f"
_sha = hashlib.sha256(open(SC_PATH, "rb").read()).hexdigest(); assert _sha == SC_SHA, f"CFG654 scorer changed: {_sha}"
_spec = importlib.util.spec_from_file_location("cfg654_scorer", SC_PATH)
N = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(N)
load_lib, build, klass, CMB_GATE = N.load_lib, N.build, N.klass, N.CMB_GATE

def score_production(fF, fS, label, mutate=False, town=None, out_suffix=None):
    """= cfg654_native.score_production (statistic and control flow verbatim); file locations are arguments."""
    T0 = time.time(); OUT = []
    def P(*a):
        s_ = " ".join(str(x) for x in a); print(s_, flush=True); OUT.append(s_)
    P(f"CFG960 score (frozen CFG654 scorer, sha256 {SC_SHA[:16]}...): {label} vs NCS0 (native scorer)" + (" [MUTATE]" if mutate else ""))
    P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    if not fF or not fS:
        P("runs not present -> nothing scored"); return None
    F, S = json.load(open(fF)), json.load(open(fS))
    INP = F.get("cfg654_inputs"); assert INP in ("native", "native_cmb") and S.get("cfg654_inputs") == INP, "both runs must carry the SAME native input set"
    assert "z0" in F["snap"] and "z0" in S["snap"]
    G = load_lib(INP)
    Pmat, fit, theory, nuis_spec, support_mask, subset, SURV, G_INJ = (G[k] for k in ("Pmat", "fit", "theory", "nuis_spec", "support_mask", "subset", "SURV", "G_INJ"))
    PROF = os.path.join(EXT, "cfg530_work", "profiles", "N512")
    def Binj(foot):
        d = np.load(os.path.join(PROF, f"cfg526_LR{'can' if foot == 'canonical' else 'alt'}_L100.npz"))
        k = np.array(d["kgrav"]); B = np.array(d["pgrav"]) / np.array(d["ppart"]); lk, lb = np.log(k), np.log(B)
        return lambda KK: np.exp(np.interp(np.log(np.clip(KK, k[0], k[-1])), lk, lb))
    foot = F["foot"]; Nn, L = int(F["np"]), float(F["L"])
    run, held = build(F, S, Nn, L, foot, f"L{L:g}_N{Nn}_{foot}")
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F"); PFh = Pmat(held, "F")
    R = dict(lane="CFG960", criteria="CFG654 FROZEN_CRITERIA.md + ADDENDUM_A1 statistic, via CFG960 FROZEN_CRITERIA.md section 3", inputs=INP,
             jobs=[label, "NCS0"], files=[os.path.basename(fF), os.path.basename(fS)], foot=foot, cmb_gate=CMB_GATE, mutate=mutate, surveys={})
    gg = {}
    for key in ("z0", "z0.5", "z1"):
        kk_ = np.array(F["snap"][key]["k"]); rr_ = np.array(F["snap"][key]["P_grav"]) / np.array(S["snap"][key]["P"]); mm_ = kk_ <= 1.0 + 1e-9
        gg[key] = dict(G=float(np.max(np.abs(rr_[mm_] - 1))), at={str(q): float(np.exp(np.interp(math.log(q), np.log(kk_), np.log(rr_)))) for q in (0.3, 0.5, 1.0)})
    R["benchmark"] = dict(gg, NOTE="benchmark vs the native-input S0 control, NOT an observational exclusion; no verdict weight")
    P(f"BENCHMARK (no verdict weight): z0 G {gg['z0']['G']:.3f}; P_grav/P_S0 at k 0.3/0.5/1: " + "/".join(f"{v:.3f}" for v in gg["z0"]["at"].values()))
    TOWN = (town or {}) if not mutate else {}
    for sn, Sv in SURV.items():
        f = support_mask(Sv, run, PS0); keep = Sv["pubkeep"] & (f >= 0.9); D = subset(Sv, keep); N_ok = D["N"] >= 10
        r = dict(N_kept=D["N"])
        if D["N"] == 0:
            r["class"] = "NOT DIAGNOSTIC"; R["surveys"][sn] = r; continue
        if mutate:
            s0 = fit(Sv, D, PS0); f0 = fit(Sv, D, Pmat(run, "F0")); nz1 = abs(s0["chi2"] - f0["chi2"]) <= 1e-9
            par = nuis_spec(Sv, 1.0, True)[3](np.array(s0["x"]))
            town_ = fit(Sv, D, PS0, data=theory(Sv, D, par, Pmat(run, "S0", inject=Binj(foot)), "PM"))["chi2"]
            r.update(NZ1=bool(nz1), T_OWN_chi2=town_, T_OWN=bool(town_ >= 9))
            P(f"  {sn}: N {D['N']}; NZ1 {'bites' if nz1 else 'FAILS'}; T-OWN S0 chi2_min {town_:.2f} -> {'DIAGNOSTIC' if town_ >= 9 else 'NOT DIAGNOSTIC'}")
            R["surveys"][sn] = r; continue
        s0 = fit(Sv, D, PS0); fF_ = fit(Sv, D, PF); d = fF_["chi2"] - s0["chi2"]
        rob = dict(widen2=fit(Sv, D, PF, widen=2.0)["chi2"] - fit(Sv, D, PS0, widen=2.0)["chi2"],
                   noIA=fit(Sv, D, PF, ia=False)["chi2"] - fit(Sv, D, PS0, ia=False)["chi2"],
                   held=fit(Sv, D, PFh)["chi2"] - s0["chi2"],
                   LOC=fit(Sv, D, Pmat(run, "F", bg="LOC"), bg="LOC")["chi2"] - fit(Sv, D, Pmat(run, "S0", bg="LOC"), bg="LOC")["chi2"])
        desi = fit(Sv, D, Pmat(run, "F", bg="DESI"), bg="DESI")["chi2"] - fit(Sv, D, Pmat(run, "S0", bg="DESI"), bg="DESI")["chi2"]
        cls = klass(d, list(rob.values()), N_ok); t_ok = TOWN.get(sn)
        if t_ok is False: cls = "NOT DIAGNOSTIC"; r["T_OWN_failed"] = True
        if t_ok is None: r["T_OWN_missing"] = True
        r.update(chi2_S0=s0["chi2"], chi2_F=fF_["chi2"], dchi2=d, robust=rob, DESI_reported=desi, **{"class": cls})
        P(f"  {sn}: N_kept {D['N']}; chi2 S0 {s0['chi2']:.2f}, F {fF_['chi2']:.2f} -> dchi2 {d:+.2f}; robust {({k: round(v, 2) for k, v in rob.items()})}; DESI (reported) {desi:+.2f} -> {cls}")
        R["surveys"][sn] = r
    if mutate:
        R["T_OWN"] = {sn: v.get("T_OWN") for sn, v in R["surveys"].items() if "T_OWN" in v}
        R["NZ1_all_bite"] = all(v.get("NZ1", True) for v in R["surveys"].values())
    else:
        cl = [v.get("class") for v in R["surveys"].values()]
        if "EXCLUDED" in cl: V = "FAILS (EXCLUDED on raw data)"
        elif "CONSISTENT" in cl and "TENSION" not in cl: V = "PASS (shear side, this footing)"
        else: V = "TENSION" if "TENSION" in cl else "NOT DIAGNOSTIC"
        if any(v.get("T_OWN_missing") for v in R["surveys"].values()): V += " [PROVISIONAL: T-OWN missing, run the MUTATE pass first]"
        R["verdict_cfg654_form"] = V; P(f"CFG654-form verdict ({foot}): {V}; CMB gate {CMB_GATE}")
        k = R["surveys"].get("KiDS", {})
        others_bad = any(v.get("class") in ("EXCLUDED", "TENSION") for v in R["surveys"].values())
        if k.get("class") == "CONSISTENT" and k.get("dchi2", 1.0) <= 0 and not others_bad: rd = "PASS"
        elif k.get("class") == "CONSISTENT" and not others_bad: rd = "WEAKENED"
        else: rd = "FAILS"
        R["reading_cfg960"] = rd
        P(f"CFG960 pre-declared footing reading (FROZEN_CRITERIA_1024.md): {rd} (KiDS class {k.get('class')}, dchi2 {k.get('dchi2', float('nan')):+.2f}; no diagnostic survey EXCLUDED/TENSION: {not others_bad})")
    R["runtime_s"] = time.time() - T0
    if out_suffix:
        json.dump(R, open(os.path.join(HERE, f"cfg960_score_results{out_suffix}.json"), "w"), indent=1)
        open(os.path.join(HERE, f"cfg960_score{out_suffix}.out"), "w").write("\n".join(OUT) + "\n")
    return R

def files_for(job):
    fF = [f for f in glob.glob(os.path.join(EXT, "cfg960_work", job, "cfg960sctm_*_SCT_*.json"))]
    fS = glob.glob(os.path.join(EXT, "cfg654_work", "NCS0", "cfg654*_cfg650_*_S0_*.json"))
    assert len(fF) <= 1 and len(fS) <= 1, (fF, fS)
    return (fF[0] if fF else None), (fS[0] if fS else None)

def scorek():
    """V-SCORE: the wrapper re-scores the stored NC1x / NC2x vs NCS0 and must reproduce CFG654's committed JSONs to <= 1e-9."""
    OUT = []
    def P(*a):
        s_ = " ".join(str(x) for x in a); print(s_, flush=True); OUT.append(s_)
    P("CFG960 V-SCORE: re-score of the stored NC1x / NC2x vs NCS0 with cfg960_score.py; compared with CFG654's committed result JSONs.")
    RES = dict(lane="CFG960", gate="V-SCORE", scorer_sha256=SC_SHA, wrapper_sha256=hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest(), jobs={})
    fS = glob.glob(os.path.join(EXT, "cfg654_work", "NCS0", "cfg654*_cfg650_*_S0_*.json"))[0]
    worst = 0.0; ok_all = True
    for job in ("NC1x", "NC2x"):
        fF = glob.glob(os.path.join(EXT, "cfg654_work", job, "cfg654*_cfg650_*_RES_*.json"))[0]
        Rm = score_production(fF, fS, job, mutate=True)
        Sm = json.load(open(os.path.join(D654, f"cfg654_native_results_{job}_MUTATE.json")))
        dm = []
        for sn, v in Rm["surveys"].items():
            if "T_OWN_chi2" in v:
                dm.append(abs(v["T_OWN_chi2"] - Sm["surveys"][sn]["T_OWN_chi2"])); ok_all &= v["NZ1"] == Sm["surveys"][sn]["NZ1"] and v["T_OWN"] == Sm["surveys"][sn]["T_OWN"]
        R0 = score_production(fF, fS, job, mutate=False, town=Rm["T_OWN"])
        S0 = json.load(open(os.path.join(D654, f"cfg654_native_results_{job}.json")))
        d = []
        for sn, v in R0["surveys"].items():
            s = S0["surveys"][sn]
            if "dchi2" not in v: continue
            for k in ("chi2_S0", "chi2_F", "dchi2", "DESI_reported"): d.append(abs(v[k] - s[k]))
            for k in v["robust"]: d.append(abs(v["robust"][k] - s["robust"][k]))
            ok_all &= v["class"] == s["class"]
        for key in ("z0", "z0.5", "z1"):
            for q in ("0.3", "0.5", "1.0"): d.append(abs(R0["benchmark"][key]["at"][q] - S0["benchmark"][key]["at"][q]))
            d.append(abs(R0["benchmark"][key]["G"] - S0["benchmark"][key]["G"]))
        w = max(d + dm); worst = max(worst, w)
        RES["jobs"][job] = dict(max_abs_diff=w, classes={sn: v.get("class") for sn, v in R0["surveys"].items()},
                                KiDS_dchi2=R0["surveys"]["KiDS"]["dchi2"], stored_KiDS_dchi2=S0["surveys"]["KiDS"]["dchi2"])
        P(f"  {job}: max |difference| over chi2/dchi2/robust/DESI/benchmark/T-OWN = {w:.3e}; KiDS dchi2 {R0['surveys']['KiDS']['dchi2']:+.4f} (stored {S0['surveys']['KiDS']['dchi2']:+.4f}); classes equal: {ok_all}")
    RES["V_SCORE_PASS"] = bool(ok_all and worst <= 1e-9); RES["worst"] = worst
    P(f"V-SCORE -> {'PASS' if RES['V_SCORE_PASS'] else 'FAIL'} (worst {worst:.3e}, line 1e-9)")
    json.dump(RES, open(os.path.join(HERE, "cfg960_scorek.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg960_scorek.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    if "--scorek" in sys.argv:
        scorek()
    elif "--score" in sys.argv:
        job = [x for x in sys.argv[1:] if not x.startswith("--")][0]
        assert job in ("SC1x", "SC2x"), job
        mut = os.environ.get("CFG596_MUTATE", "0") == "1"
        fF, fS = files_for(job)
        tf = os.path.join(HERE, f"cfg960_score_results_{job}_MUTATE.json")
        town = json.load(open(tf))["T_OWN"] if (not mut and os.path.exists(tf)) else None
        score_production(fF, fS, job, mutate=mut, town=town, out_suffix=f"_{job}" + ("_MUTATE" if mut else ""))
