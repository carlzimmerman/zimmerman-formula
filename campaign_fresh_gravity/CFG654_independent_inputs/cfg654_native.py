#!/usr/bin/env python3
"""CFG654 part 4: the scorer with framework-native background ingredients, as a loadable patch + post-hoc re-scoring.

Library use (CFG650-style scorers):   G = cfg654_native.load_lib("native")   (or "inherited" = CFG592's library exec'd unchanged)
  native patch of CFG592's cfg592_native.py library (the statistic, data, covariances, n(z), cuts, support cut, nuisances, fit and
  classes are NOT touched):
    BG    'PM' distances from the framework's own background: flat, Om_cb (native), radiation (photons + 3.044 massless nu),
          Lambda + CFG630 trickle (cfg654_scorer_tables.npz); 'LOC' = the same with H0 = 73.04 (SH0ES bracket, Om_cb = omega_m/h^2)
    Om    lensing-kernel and IA prefactor Omega_m = native Om_cb
    DZG / Dgrow   P(k) continuation above z = 1 (and the IA growth) with the native linear growth (the same ODE as the ICs;
          equals GR growth because the continuation is a linear large-scale statement)
    P_lin0        the k < k_lo continuation uses the native CAMB z = 0 linear cb SHAPE (matched to the measured node at k_lo)
          instead of the EH no-wiggle shape with sigma8 = 0.811
  Partial patches (attribution): parts = subset of {"bg", "om", "growth", "lowk"}.
Post-hoc diagnostic (main): CFG596 P1 vs P0 and CFG636 C1 vs P0, stored runs read only, scorer-only changes.  These runs were
evolved with the INHERITED ICs/background, so the native-scorer numbers are POST HOC DIAGNOSTICS of the scorer's sensitivity, not
verdicts and not a corrected CFG596/636 score.
  nice -n 10 python3 cfg654_native.py   -> cfg654_native_posthoc.out / cfg654_native_posthoc.json
Production (FROZEN_CRITERIA.md):  CFG596_MUTATE=1 nice -n 10 python3 cfg654_native.py --score N12 NS0   (FIRST), then without MUTATE
  -> cfg654_native_N12[_MUTATE].out / cfg654_native_results_N12[_MUTATE].json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, glob, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.integrate import quad
import warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul")   # spurious BLAS flags (numpy >= 2 / Accelerate); values finite, checked by reproduction

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(CFG, "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
ST = np.load(os.path.join(HERE, "cfg654_scorer_tables.npz"))
H0LOC = 0.7304

def native_E(Om, Or, OL, trick=True):
    trz, trd = np.array(ST["trz"]), np.array(ST["trd"])
    return lambda z: math.sqrt(Om * (1 + z) ** 3 + Or * (1 + z) ** 4 + OL * ((1.0 - float(np.interp(z, trz, trd))) if trick else 1.0))

def load_lib(inputs="native", parts=("bg", "om", "growth", "lowk")):
    code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
    G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
    exec(compile(code[:cut], SRC, "exec"), G)
    G["CFG654_INPUTS"] = inputs; G["CFG654_PARTS"] = tuple(parts) if inputs == "native" else ()
    Om, Or, OL = float(ST["Om"]), float(ST["Or"]), float(ST["OL"])
    ZG = G["ZG"]
    def bgd(Ez):
        chi = np.array([quad(lambda x: 1 / Ez(x), 0, z, epsabs=0, epsrel=1e-10)[0] for z in ZG]) * 2997.92458
        return chi, 2997.92458 / np.array([Ez(z) for z in ZG])
    hN = float(ST["h"]); omm = Om * hN ** 2; OmL = omm / H0LOC ** 2; OrL = Or * hN ** 2 / H0LOC ** 2
    G["BG"]["LOC"] = bgd(native_E(OmL, OrL, 1 - OmL - OrL))          # added distance variant (both modes; nothing else uses it)
    if inputs == "inherited":
        return G
    assert inputs == "native"
    if "bg" in parts:
        G["BG"]["PM"] = bgd(native_E(Om, Or, OL))
    if "om" in parts:
        G["Om"] = Om
    if "growth" in parts:
        lna, lnD = np.array(ST["lna"]), np.array(ST["lnD"])
        Dn = lambda a: float(math.exp(np.interp(math.log(a), lna, lnD)))
        G["Dgrow"] = Dn; G["DZG"] = np.array([Dn(a) for a in G["AG"]])
    if "lowk" in parts:
        lk, lp = np.log(np.array(ST["kh"])), np.log(np.array(ST["Plin_z0"]))
        G["P_lin0"] = lambda k: np.exp(np.interp(np.log(np.clip(k, math.exp(lk[0]), math.exp(lk[-1]))), lk, lp))
    return G

# ---------------------------------------------------------------- the CFG596 per-run statistic (cfg596_native.py block, compact)
ZK = {0.0: "z0", 0.5: "z0.5", 1.0: "z1"}
def build(F, S, N, L, foot, label):
    k = np.array(F["snap"]["z0"]["k"]); assert np.allclose(k, np.array(S["snap"]["z0"]["k"]), rtol=1e-6)
    nodes = {z: (np.array(F["snap"][key]["P_grav"]), np.array(S["snap"][key]["P"])) for z, key in ZK.items()}
    held = {z: (np.array(F["snap"][key]["P"]), np.array(S["snap"][key]["P"])) for z, key in ZK.items()}
    B0 = np.array(F["snap"]["z0"]["P_grav"]) / np.array(F["snap"]["z0"]["P"])
    base = dict(name=label, foot=foot, N=N, L=L, k=k, k_lo=float(k[0]), k_hi=float(math.pi * N / (4 * L)))
    return dict(base, B=np.ones_like(k), nodes=nodes), dict(base, B=B0, nodes=held)

def score(G, F, S, foot, robust=("widen2", "noIA", "held", "DESI"), extra_bg=("LOC",)):
    Pmat, fit, support_mask, subset, SURV = G["Pmat"], G["fit"], G["support_mask"], G["subset"], G["SURV"]
    N, L = int(F["np"]), float(F["L"])
    run, held = build(F, S, N, L, foot, f"L{L:g}_N{N}_{foot}")
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F"); PFh = Pmat(held, "F")
    out = {}
    for sn, Sv in SURV.items():
        f = support_mask(Sv, run, PS0); keep = Sv["pubkeep"] & (f >= 0.9); D = subset(Sv, keep)
        if D["N"] == 0: out[sn] = dict(N=0); continue
        s0 = fit(Sv, D, PS0); fF = fit(Sv, D, PF); s0n = fit(Sv, D, PS0, ia=False); fFn = fit(Sv, D, PF, ia=False)
        r = dict(N=D["N"], chi2_S0=s0["chi2"], chi2_F=fF["chi2"], dchi2=fF["chi2"] - s0["chi2"], dchi2_noIA=fFn["chi2"] - s0n["chi2"])
        rob = {}
        if "widen2" in robust: rob["widen2"] = fit(Sv, D, PF, widen=2.0)["chi2"] - fit(Sv, D, PS0, widen=2.0)["chi2"]
        if "noIA" in robust: rob["noIA"] = r["dchi2_noIA"]
        if "held" in robust: rob["held"] = fit(Sv, D, PFh)["chi2"] - s0["chi2"]
        for bgn in (["DESI"] if "DESI" in robust else []) + list(extra_bg):
            rob[bgn] = fit(Sv, D, Pmat(run, "F", bg=bgn), bg=bgn)["chi2"] - fit(Sv, D, Pmat(run, "S0", bg=bgn), bg=bgn)["chi2"]
        r["robust"] = rob
        out[sn] = r
    return out

def main():
    T0 = time.time(); OUT = []
    def P(*a):
        s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
    P("CFG654 part 4: scorer-only re-scoring of stored CFG596 P1 / CFG636 C1 vs CFG596 P0 (read only). POST HOC DIAGNOSTICS, NOT verdicts:")
    P("the runs used the INHERITED ICs and background; only the scorer's background, kernel Om, z > 1 growth and k < k_lo shape change.")
    P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    EXT = os.path.abspath(os.path.join(CFG, "..", "..", "_external_data"))
    S = json.load(open(glob.glob(os.path.join(EXT, "cfg596_work", "P0", "cfg596_*.json"))[0]))
    RUNS = {"CFG596_P1": json.load(open(glob.glob(os.path.join(EXT, "cfg596_work", "P1", "cfg596_*.json"))[0])),
            "CFG636_C1": json.load(open(glob.glob(os.path.join(EXT, "cfg636_work", "C1", "cfg636_hcb_RES_*.json"))[0]))}
    STORED = {"CFG596_P1": json.load(open(os.path.join(CFG, "CFG596_lean_pm_1024", "cfg596_native_results.json"))),
              "CFG636_C1": json.load(open(os.path.join(CFG, "CFG636_hcb_native_1024", "cfg636_native_results.json")))}
    VARIANTS = [("inherited", ()), ("native", ("bg", "om", "growth", "lowk")), ("native", ("bg",)), ("native", ("om",)),
                ("native", ("growth",)), ("native", ("lowk",))]
    RES = dict(lane="CFG654", part="scorer_posthoc", label="POST HOC DIAGNOSTIC (scorer only; runs evolved with inherited inputs)",
               native_background=dict(Om=float(ST["Om"]), Or=float(ST["Or"]), OL=float(ST["OL"]), h=float(ST["h"])), runs={})
    for vi, (inp, parts) in enumerate(VARIANTS):
        G = load_lib(inp, parts); tag = inp if inp == "inherited" else ("native_all" if len(parts) == 4 else "native_" + parts[0])
        full = vi < 2
        for rn, F in RUNS.items():
            o = score(G, F, S, "canonical", robust=("widen2", "noIA", "held", "DESI") if full else ("noIA",), extra_bg=("LOC",) if full else ())
            RES["runs"].setdefault(rn, {})[tag] = o
            for sn, r in o.items():
                if "dchi2" not in r: continue
                line = f"  [{tag:15s}] {rn} {sn}: N {r['N']}; chi2 S0 {r['chi2_S0']:.2f}, F {r['chi2_F']:.2f}; dchi2 {r['dchi2']:+.3f} (noIA {r['dchi2_noIA']:+.3f})"
                if full: line += "; robust " + str({k: round(v, 2) for k, v in r["robust"].items()})
                if tag == "inherited":
                    st = STORED[rn]["runs"]["L100_N1024_canonical"]["surveys"][sn]
                    ok = abs(st["dchi2"] - r["dchi2"]) < 1e-6 and abs(st["robust"]["DESI"] - r["robust"]["DESI"]) < 1e-6
                    r["reproduces_stored"] = bool(ok); line += f"  [stored {st['dchi2']:+.3f}: {'REPRODUCED' if ok else 'MISMATCH'}]"
                P(line)
    P("\nshift native_all - inherited (POST HOC, scorer only):")
    for rn in RUNS:
        for sn in ("KiDS", "DES"):
            a, b = RES["runs"][rn]["inherited"][sn], RES["runs"][rn]["native_all"][sn]
            sh = dict(dchi2=b["dchi2"] - a["dchi2"], dchi2_noIA=b["dchi2_noIA"] - a["dchi2_noIA"], chi2_S0=b["chi2_S0"] - a["chi2_S0"],
                      robust_min_inherited=min(a["robust"].values()), robust_min_native=min(b["robust"].values()))
            RES["runs"][rn].setdefault("shift", {})[sn] = sh
            parts = {p: RES["runs"][rn][f"native_{p}"][sn]["dchi2"] - a["dchi2"] for p in ("bg", "om", "growth", "lowk")}
            RES["runs"][rn]["shift"][sn]["by_part"] = parts
            P(f"  {rn} {sn}: dchi2 {a['dchi2']:+.3f} -> {b['dchi2']:+.3f} (shift {sh['dchi2']:+.3f}; noIA {sh['dchi2_noIA']:+.3f}); chi2_S0 shift {sh['chi2_S0']:+.2f}; "
              f"robust min {sh['robust_min_inherited']:+.2f} -> {sh['robust_min_native']:+.2f}; by part " + ", ".join(f"{p} {v:+.3f}" for p, v in parts.items()))
    RES["runtime_s"] = time.time() - T0
    P(f"\ndone in {RES['runtime_s']:.0f} s")
    json.dump(RES, open(os.path.join(HERE, "cfg654_native_posthoc.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg654_native_posthoc.out"), "w").write("\n".join(OUT) + "\n")


# ---------------------------------------------------------------- production scoring of the independent-inputs runs (FROZEN_CRITERIA.md)
CMB_GATE = "NOT EVALUATED (no committed CFG649 raw-data CMB-lensing form at this scorer's freeze)"
def klass(d, robust, N_ok):
    """CFG592/596 classes, unchanged."""
    if not N_ok: return "NOT DIAGNOSTIC"
    if d >= 9 and min([d] + robust) >= 9: return "EXCLUDED"
    if d >= 4: return "TENSION"
    if d < 4 and max(robust) < 9: return "CONSISTENT"
    return "NOT DIAGNOSTIC"
def score_production(jobF="N12", jobS="NS0", mutate=False):
    """N12 (native inputs, M1+M2) vs NS0 (native inputs, S0) with the NATIVE scorer; robustness set {widen2, noIA, held, LOC};
    DESI-chain distances reported only; T-OWN tooth and NZ1 MUTATE unchanged in form (MUTATE first)."""
    T0 = time.time(); OUT = []
    def P(*a):
        s_ = " ".join(str(x) for x in a); print(s_, flush=True); OUT.append(s_)
    EXT = os.path.abspath(os.path.join(CFG, "..", "..", "_external_data")); W = os.path.join(EXT, "cfg654_work")
    fF = glob.glob(os.path.join(W, jobF, "cfg654nat_cfg650_*_RES_*.json")); fS = glob.glob(os.path.join(W, jobS, "cfg654nat_cfg650_*_S0_*.json"))
    suf = f"_{jobF}" + ("_MUTATE" if mutate else "")
    P(f"CFG654 independent-inputs score: {jobF} vs {jobS} (native scorer)" + (" [MUTATE]" if mutate else ""))
    P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    if not fF or not fS:
        P("runs not present -> nothing scored"); return None
    F, S = json.load(open(fF[0])), json.load(open(fS[0]))
    assert F.get("cfg654_inputs") == "native" and S.get("cfg654_inputs") == "native", "both runs must carry native inputs"
    assert "z0" in F["snap"] and "z0" in S["snap"]
    G = load_lib("native")
    Pmat, fit, theory, nuis_spec, support_mask, subset, SURV, G_INJ = (G[k] for k in ("Pmat", "fit", "theory", "nuis_spec", "support_mask", "subset", "SURV", "G_INJ"))
    PROF = os.path.join(EXT, "cfg530_work", "profiles", "N512")
    def Binj(foot):
        d = np.load(os.path.join(PROF, f"cfg526_LR{'can' if foot == 'canonical' else 'alt'}_L100.npz"))
        k = np.array(d["kgrav"]); B = np.array(d["pgrav"]) / np.array(d["ppart"]); lk, lb = np.log(k), np.log(B)
        return lambda KK: np.exp(np.interp(np.log(np.clip(KK, k[0], k[-1])), lk, lb))
    foot = F["foot"]; N, L = int(F["np"]), float(F["L"])
    run, held = build(F, S, N, L, foot, f"L{L:g}_N{N}_{foot}")
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F"); PFh = Pmat(held, "F")
    R = dict(lane="CFG654", criteria="FROZEN_CRITERIA.md", jobs=[jobF, jobS], foot=foot, cmb_gate=CMB_GATE, mutate=mutate, surveys={})
    gg = {}
    for key in ("z0", "z0.5", "z1"):
        kk_ = np.array(F["snap"][key]["k"]); rr_ = np.array(F["snap"][key]["P_grav"]) / np.array(S["snap"][key]["P"]); mm_ = kk_ <= 1.0 + 1e-9
        gg[key] = dict(G=float(np.max(np.abs(rr_[mm_] - 1))), at={str(q): float(np.exp(np.interp(math.log(q), np.log(kk_), np.log(rr_)))) for q in (0.3, 0.5, 1.0)})
    R["benchmark"] = dict(gg, NOTE="benchmark vs the native-input S0 control, NOT an observational exclusion; no verdict weight")
    P(f"BENCHMARK (no verdict weight): z0 G {gg['z0']['G']:.3f}; P_grav/P_S0 at k 0.3/0.5/1: " + "/".join(f"{v:.3f}" for v in gg["z0"]["at"].values()))
    mfn = os.path.join(HERE, f"cfg654_native_results_{jobF}_MUTATE.json")
    TOWN = json.load(open(mfn))["T_OWN"] if (not mutate and os.path.exists(mfn)) else {}
    for sn, Sv in SURV.items():
        f = support_mask(Sv, run, PS0); keep = Sv["pubkeep"] & (f >= 0.9); D = subset(Sv, keep); N_ok = D["N"] >= 10
        r = dict(N_kept=D["N"])
        if D["N"] == 0:
            r["class"] = "NOT DIAGNOSTIC"; R["surveys"][sn] = r; continue
        if mutate:
            s0 = fit(Sv, D, PS0); f0 = fit(Sv, D, Pmat(run, "F0")); nz1 = abs(s0["chi2"] - f0["chi2"]) <= 1e-9
            par = nuis_spec(Sv, 1.0, True)[3](np.array(s0["x"]))
            town = fit(Sv, D, PS0, data=theory(Sv, D, par, Pmat(run, "S0", inject=Binj(foot)), "PM"))["chi2"]
            r.update(NZ1=bool(nz1), T_OWN_chi2=town, T_OWN=bool(town >= 9))
            P(f"  {sn}: N {D['N']}; NZ1 {'bites' if nz1 else 'FAILS'}; T-OWN S0 chi2_min {town:.2f} -> {'DIAGNOSTIC' if town >= 9 else 'NOT DIAGNOSTIC'}")
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
        R["verdict"] = V; P(f"verdict ({foot}): {V}; CMB gate {CMB_GATE}; conditional on the shared inputs listed in FROZEN_CRITERIA.md section 6")
    json.dump(R, open(os.path.join(HERE, f"cfg654_native_results{suf}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg654_native{suf}.out"), "w").write("\n".join(OUT) + "\n")
    return R

if __name__ == "__main__":
    if "--score" in sys.argv:          # python3 cfg654_native.py --score [N12 NS0]   (CFG596_MUTATE=1 first)
        a = [x for x in sys.argv[1:] if not x.startswith("--")]
        score_production(*(a or ["N12", "NS0"]), mutate=os.environ.get("CFG596_MUTATE", "0") == "1")
    else:
        main()
