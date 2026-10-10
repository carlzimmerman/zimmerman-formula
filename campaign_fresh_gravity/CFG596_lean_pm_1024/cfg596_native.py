#!/usr/bin/env python3
"""CFG596 framework-native shear test (FROZEN_CRITERIA.md section 3-4, commit f6c27d401).
CFG592's native machinery (cfg592_native.py library part, exec'd UNCHANGED: data, covariance, n(z), published cuts, support cut,
nuisances, PM background, DESI distances, extensions, z-node interpolation, fit, klass) applied to the CFG596 L100 N1024 runs:
  framework = the run's MEASURED gravitating P(k, z) at z = 0, 0.5, 1 (CFG592 'F' code path with B = 1);  S0 = its particle P (= gravitating).
  robustness set: widen2, noIA, DESI, held (= CFG592's former PRIMARY: P_part,F(z) x B_F(z = 0)), 'held' replacing 'fade'.
  tooth T-OWN (NEW, post-hoc relative to CFG592): S0 best-fit mock x B_foot(k) (CFG530 L100 N512 cache, z = 0, held in z, flat outside
  0.08-4.02) must give an S0 refit chi2_min >= 9, else that survey x footing is NOT DIAGNOSTIC.  NZ1 carried over; NZ2 (20% ramp) reported only.
  nice -n 10 python3 cfg596_native.py                  -> cfg596_native.out, cfg596_native_results.json   (reads the MUTATE JSON for T-OWN)
  CFG596_MUTATE=1 nice -n 10 python3 cfg596_native.py  -> *_MUTATE.out / .json (exit 1 = NZ1 bites everywhere)
  python3 cfg596_native.py --test530                   -> pipeline check on CFG530 L100 N512 (held construction = CFG592's PRIMARY); writes *_test530.*
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, glob, time
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(CFG, "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
exec(compile(code[:cut], SRC, "exec"), G)
import numpy as np
from scipy.stats import chi2 as CH
EXT = G["EXT"]; W596 = os.path.join(EXT, "cfg596_work")
MUT = os.environ.get("CFG596_MUTATE", "0") == "1"; TEST = "--test530" in sys.argv
SUF = ("_test530" if TEST else "") + ("_MUTATE" if MUT else "")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
Pmat, fit, theory, nuis_spec, support_mask, subset, klass, SURV, G_INJ = (G[k] for k in ("Pmat", "fit", "theory", "nuis_spec", "support_mask", "subset", "klass", "SURV", "G_INJ"))
LN, BG, ZG, DZG, Dgrow, node_P = G["LN"], G["BG"], G["ZG"], G["DZG"], G["Dgrow"], G["node_P"]

# ------------------------------------------------------------------ tooth boosts (CFG530 L100 N512 caches, z = 0)
PROF = os.path.join(EXT, "cfg530_work", "profiles", "N512")
def Bfoot(foot):
    d = np.load(os.path.join(PROF, f"cfg526_LR{'can' if foot == 'canonical' else 'alt'}_L100.npz"))
    k = np.array(d["kgrav"]); B = np.array(d["pgrav"]) / np.array(d["ppart"]); return k, B
def Binj(foot):
    k, B = Bfoot(foot); lk, lb = np.log(k), np.log(B)
    return lambda KK: np.exp(np.interp(np.log(np.clip(KK, k[0], k[-1])), lk, lb))

# ------------------------------------------------------------------ runs
ZK = {0.0: "z0", 0.5: "z0.5", 1.0: "z1"}
def load596(job):
    f = glob.glob(os.path.join(W596, job, "cfg596_*.json")); return json.load(open(f[0])) if f else None
def build(F, S, N, L, foot, label):
    k = np.array(F["snap"]["z0"]["k"]); assert np.allclose(k, np.array(S["snap"]["z0"]["k"]), rtol=1e-6)
    nodes = {z: (np.array(F["snap"][key]["P_grav"]), np.array(S["snap"][key]["P"])) for z, key in ZK.items()}
    held = {z: (np.array(F["snap"][key]["P"]), np.array(S["snap"][key]["P"])) for z, key in ZK.items()}
    B0 = np.array(F["snap"]["z0"]["P_grav"]) / np.array(F["snap"]["z0"]["P"])
    extra = {}
    for key, v in F["snap"].items():
        if key.startswith("x"):
            extra[float(v["z"])] = (np.array(v["P_grav"]), np.array(S["snap"][key]["P"]))
    base = dict(name=label, foot=foot, N=N, L=L, k=k, k_lo=float(k[0]), k_hi=float(math.pi * N / (4 * L)))
    return dict(base, B=np.ones_like(k), nodes=nodes), dict(base, B=B0, nodes=held), extra, B0
def runs_list():
    out = []
    if TEST:
        R530 = os.path.join(EXT, "cfg530_work", "runs")
        S = json.load(open(glob.glob(os.path.join(R530, "S0_L100_N512", "cfg527_S0_*.json"))[0]))
        for foot, run in (("canonical", "LRcan"), ("alt", "LRalt")):
            F = json.load(open(glob.glob(os.path.join(R530, f"{run}_L100_N512", "cfg527_RES_*.json"))[0]))
            d = np.load(os.path.join(PROF, f"cfg526_{run}_L100.npz")); B0 = np.array(d["pgrav"]) / np.array(d["ppart"])
            for key in ZK.values():                                   # test only: framework 'grav' = particle x B(z = 0) (held)
                F["snap"][key]["P_grav"] = list(np.array(F["snap"][key]["P"]) * B0)
            out.append((foot, F, S, 512, 100.0))
        return out
    S = load596("P0")
    for foot, job in (("canonical", "P1"), ("alt", "P2")):
        F = load596(job)
        if F is None or S is None or "z0" not in F["snap"] or "z0" not in S["snap"]: continue
        out.append((foot, F, S, int(F["np"]), float(F["L"])))
    return out

def Pmat_nodes(run, which, nodes_z):
    """reported-only five-node variant of CFG592 Pmat (log-linear in z between the given nodes; D^2 above the last)."""
    chi = BG["PM"][0]; KK = (LN[:, None] + 0.5) / chi[None, :]
    lnP = np.array([np.log(node_P(run["k"], run["nodes5"][z][0 if which == "F" else 1], run["k_lo"], run["k_hi"], KK)) for z in nodes_z])
    Pm = np.empty_like(KK); zn = np.array(nodes_z)
    for j, z in enumerate(ZG):
        if z <= zn[-1]:
            i = min(np.searchsorted(zn, z, side="right") - 1, len(zn) - 2); w = (z - zn[i]) / (zn[i + 1] - zn[i])
            Pm[:, j] = np.exp(lnP[i, :, j] + w * (lnP[i + 1, :, j] - lnP[i, :, j]))
        else:
            Pm[:, j] = np.exp(lnP[-1, :, j]) * (DZG[j] / Dgrow(1 / (1 + zn[-1]))) ** 2
    return Pm

def strip(r): return {k: v for k, v in r.items() if k != "t"}
RESULT = dict(lane="CFG596", date="2026-10-10", criteria_commit="f6c27d401", mutate=MUT, test530=TEST, runs={})
P("CFG596 framework-native shear test (own PM gravitating-field P(k, z) vs matched S0; CFG592 machinery unchanged)" + (" [MUTATE]" if MUT else "") + (" [PIPELINE TEST on CFG530 L100 N512]" if TEST else ""))
P("kappa = 1/2 FITTED; footings never pooled; cold energy MASS still required; not theory closed. T-OWN is post-hoc relative to CFG592 (disclosed).")
mfn = os.path.join(HERE, f"cfg596_native_results{'_test530' if TEST else ''}_MUTATE.json")
TOWN = json.load(open(mfn))["T_OWN"] if (not MUT and os.path.exists(mfn)) else {}
for foot, F, S, N, L in runs_list():
    run, held, extra, B0 = build(F, S, N, L, foot, f"L{L:g}_N{N}_{foot}")
    res = dict(foot=foot, N=N, L=L, k_lo=run["k_lo"], k_hi=run["k_hi"], B_at={str(kk): float(np.interp(math.log(kk), np.log(run["k"]), B0)) for kk in (0.3, 0.5, 1.0, 2.0, 4.0)}, surveys={})
    P(f"\n--- {run['name']} (k {run['k_lo']:.3f}-{run['k_hi']:.3f} h/Mpc); own B(z=0) at k 0.3/0.5/1/2/4: " + " / ".join(f"{v:.3f}" for v in res["B_at"].values()))
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F"); PFh = Pmat(held, "F"); PS0d = Pmat(run, "S0", bg="DESI"); PFd = Pmat(run, "F", bg="DESI")
    if extra:                                                          # reported: interpolation check at the extra snapshots
        ic = {}
        for z, (pf, ps) in extra.items():
            i = 0 if z <= 0.5 else 1; w = (z - [0.0, 0.5, 1.0][i]) / 0.5; m = run["k"] <= run["k_hi"]
            dev = {}
            for nm, col in (("F", 0), ("S0", 1)):
                a_, b_ = run["nodes"][[0.0, 0.5, 1.0][i]][col], run["nodes"][[0.0, 0.5, 1.0][i + 1]][col]
                lp = np.log(a_) + w * (np.log(b_) - np.log(a_)); meas = np.log(pf if col == 0 else ps)
                dev[nm] = float(np.max(np.abs(lp[m] - meas[m])))
            ic[f"{z:.4f}"] = dev
        res["interp_check_max_abs_dlnP"] = ic
        P("  interpolation check (reported): " + "; ".join(f"z {z}: F {d['F']:.4f}, S0 {d['S0']:.4f}" for z, d in ic.items()))
        nodes5 = dict({z: run["nodes"][z] for z in (0.0, 0.5, 1.0)}, **extra); run["nodes5"] = nodes5; zs5 = sorted(nodes5)
    for sn, Sv in SURV.items():
        f = support_mask(Sv, run, PS0); keep = Sv["pubkeep"] & (f >= 0.9); D = subset(Sv, keep)
        Npub = int(Sv["pubkeep"].sum()); r = dict(N_kept=D["N"], N_published=Npub, frac_lost=1 - D["N"] / Npub); N_ok = D["N"] >= 10
        kept_th = {}
        for (s, a, b, ab, ang, *_), kp in zip(Sv["rows"], keep):
            if kp: kept_th.setdefault(f"xi{s}_{a}{b}", []).append(round(ang, 2))
        r["kept_theta"] = {k_: [min(v), max(v), len(v)] for k_, v in kept_th.items()}
        if D["N"] == 0:
            r["class"] = r["class_noIA"] = "NOT DIAGNOSTIC"; res["surveys"][sn] = r; P(f"  {sn}: N_kept 0 -> NOT DIAGNOSTIC"); continue
        if MUT:
            s0 = fit(Sv, D, PS0); f0 = fit(Sv, D, Pmat(run, "F0"))
            nz1 = abs(s0["chi2"] - f0["chi2"]) <= 1e-9
            par = nuis_spec(Sv, 1.0, True)[3](np.array(s0["x"]))
            mock = theory(Sv, D, par, Pmat(run, "S0", inject=Binj(foot)), "PM"); town = fit(Sv, D, PS0, data=mock)["chi2"]
            mock2 = theory(Sv, D, par, Pmat(run, "S0", inject=G_INJ), "PM"); nz2 = fit(Sv, D, PS0, data=mock2)["chi2"]
            r["MUT"] = dict(NZ1=bool(nz1), NZ1_dchi2=abs(s0["chi2"] - f0["chi2"]), T_OWN_chi2=town, T_OWN=bool(town >= 9), NZ2_chi2_reported=nz2, N=D["N"])
            P(f"  {sn}: N {D['N']}; NZ1 |dchi2| {abs(s0['chi2'] - f0['chi2']):.1e} -> {'bites' if nz1 else 'FAILS'}; T-OWN (own boost injected) S0 chi2_min {town:.2f} -> "
              f"{'DIAGNOSTIC' if town >= 9 else 'NOT DIAGNOSTIC'}; NZ2 (CFG592 20% ramp, reported) {nz2:.2f}")
            res["surveys"][sn] = r; continue
        out = {}
        for ia in (True, False):
            tag = "IA" if ia else "noIA"; s0 = fit(Sv, D, PS0, ia=ia); fF = fit(Sv, D, PF, ia=ia)
            out[tag] = dict(S0=strip(s0), F=strip(fF), dchi2=fF["chi2"] - s0["chi2"])
        d = out["IA"]["dchi2"]
        rob = dict(widen2=fit(Sv, D, PF, widen=2.0)["chi2"] - fit(Sv, D, PS0, widen=2.0)["chi2"], noIA=out["noIA"]["dchi2"],
                   held=fit(Sv, D, PFh)["chi2"] - out["IA"]["S0"]["chi2"],
                   DESI=fit(Sv, D, PFd, bg="DESI")["chi2"] - fit(Sv, D, PS0d, bg="DESI")["chi2"])
        rob_noIA = dict(widen2=fit(Sv, D, PF, widen=2.0, ia=False)["chi2"] - fit(Sv, D, PS0, widen=2.0, ia=False)["chi2"],
                        held=fit(Sv, D, PFh, ia=False)["chi2"] - out["noIA"]["S0"]["chi2"],
                        DESI=fit(Sv, D, PFd, bg="DESI", ia=False)["chi2"] - fit(Sv, D, PS0d, bg="DESI", ia=False)["chi2"])
        cls = klass(d, list(rob.values()), N_ok); cls_noIA = klass(out["noIA"]["dchi2"], list(rob_noIA.values()), N_ok)
        t_ok = TOWN.get(run["name"], {}).get(sn)
        if t_ok is False: cls = cls_noIA = "NOT DIAGNOSTIC"; r["T_OWN_failed"] = True
        if t_ok is None: r["T_OWN_missing"] = True
        pS = float(CH.sf(out["IA"]["S0"]["chi2_data"], D["N"])); pF = float(CH.sf(out["IA"]["F"]["chi2_data"], D["N"]))
        r.update(fits=out, robust=rob, robust_noIA=rob_noIA, dchi2=d, dchi2_noIA=out["noIA"]["dchi2"], **{"class": cls}, class_noIA=cls_noIA, p_S0=pS, p_F=pF)
        ph = {}
        for thr in (0.8, 0.7):                                        # reported only (CFG592 post-hoc thresholds)
            Dp = subset(Sv, Sv["pubkeep"] & (f >= thr))
            if Dp["N"] >= 10:
                a_ = fit(Sv, Dp, PS0); b_ = fit(Sv, Dp, PF); ph[str(thr)] = dict(N=Dp["N"], dchi2=b_["chi2"] - a_["chi2"])
            else: ph[str(thr)] = dict(N=Dp["N"])
        r["posthoc_support"] = ph
        if extra:                                                     # reported: five-node variant
            P5F = Pmat_nodes(run, "F", zs5); P5S = Pmat_nodes(run, "S0", zs5)
            r["dchi2_five_node"] = fit(Sv, D, P5F)["chi2"] - fit(Sv, D, P5S)["chi2"]
        P(f"  {sn}: N_kept {D['N']} of {Npub} ({100 * r['frac_lost']:.0f}% lost); chi2 S0 {out['IA']['S0']['chi2']:.2f} (p {pS:.3f}), F {out['IA']['F']['chi2']:.2f} (p {pF:.3f}) "
          f"-> dchi2 {d:+.2f} (A_IA S0 {out['IA']['S0']['A_IA']:.2f}, F {out['IA']['F']['A_IA']:.2f}); robust {({k_: round(v, 2) for k_, v in rob.items()})}; "
          f"T-OWN {'pass' if t_ok else ('FAIL' if t_ok is False else 'missing')} -> {cls}")
        P(f"  {sn}: no IA: dchi2 {out['noIA']['dchi2']:+.2f}; robust {({k_: round(v, 2) for k_, v in rob_noIA.items()})} -> {cls_noIA}"
          + (f"; five-node (reported) {r['dchi2_five_node']:+.2f}" if extra else "") + f"; post-hoc support {ph}")
        res["surveys"][sn] = r
    RESULT["runs"][run["name"]] = res
if MUT:
    allb = all(s["MUT"].get("NZ1", True) for r in RESULT["runs"].values() for s in r["surveys"].values() if "MUT" in s)
    RESULT["NZ1_all_bite"] = allb
    RESULT["T_OWN"] = {n: {sn: s["MUT"]["T_OWN"] for sn, s in r["surveys"].items() if "MUT" in s} for n, r in RESULT["runs"].items()}
    P(f"\nMUTATE: NZ1 all bite = {allb}; T-OWN per run x survey = {RESULT['T_OWN']}   ({time.time() - T0:.0f} s)")
else:
    SUM = {}
    for n, r in RESULT["runs"].items():
        for sn, s in r["surveys"].items():
            SUM[f"{r['foot']}|{sn}"] = dict(class_=s.get("class"), class_noIA=s.get("class_noIA"), dchi2=s.get("dchi2"))
    for foot in ("canonical", "alt"):
        if not any(r["foot"] == foot for r in RESULT["runs"].values()):
            for sn in SURV: SUM[f"{foot}|{sn}"] = dict(class_="PENDING (run not done)")
    RESULT["footing_summary"] = SUM
    P("\nfooting summary: " + "; ".join(f"{k}: {v.get('class_')}" for k, v in SUM.items()) + f"   ({time.time() - T0:.0f} s)")
json.dump(RESULT, open(os.path.join(HERE, f"cfg596_native_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg596_native{SUF}.out"), "w").write("\n".join(OUT) + "\n")
if MUT: sys.exit(1 if RESULT["NZ1_all_bite"] else 0)
