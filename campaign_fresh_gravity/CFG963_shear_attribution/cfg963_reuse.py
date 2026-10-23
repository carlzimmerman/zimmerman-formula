#!/usr/bin/env python3
"""CFG963 AMENDMENT A1 (64718930a): a REUSABLE feedback-matched scorer + extra controls + SC1x vs the surrogate.  REPORTED ONLY.
Library use (any later lane; read only, nothing is written on import):
    spec = importlib.util.spec_from_file_location("cfg963_reuse", <path>); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
    R.score_vs_feedback_control(run_dict, "M3-1024")      # frozen CFG654 scorer: run vs NCS0 x T_M3(k, z) (control-slot surrogate)
    R.score_vs_NCS0(run_dict)                              # the same scorer vs plain NCS0 (= CFG654 / CFG960 production form)
    R.TRANSFER_NAMES -> ("M3-1024" PRIMARY, "M3-256", "M3-alone-256", "CFG646-R3", "unit")
  run_dict = a native_cmb 1024^3 L100 engine JSON (snap z0 / z0.5 / z1 with k, P, P_grav), e.g. json.load(open(<run>.json)).
  Pass mutate=True FIRST to get T-OWN (dict survey -> bool), then mutate=False with TOWN=that dict (as the frozen scorer does).
Script use (one process, one thread, nice 10; MUTATE FIRST):
  CFG596_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg963_reuse.py  -> cfg963_reuse_MUTATE.out / cfg963_reuse_results_MUTATE.json
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg963_reuse.py                  -> cfg963_reuse.out / cfg963_reuse_results.json
Items (amendment A1): K2 inherited reproduction of CFG650 T12 / T1x / T2x vs P0; K3 control-slot unit test (NC1x / NC2x vs NCS0 x 1);
K4 SC1x vs NCS0 x 1 reproduces CFG960's stored score; bracket R3 = CFG646 static DIFF-S; SC1x vs NCS0 x T for every bracket.
Guards: peak RSS > 0.95 GB -> exit 3; free + inactive memory < 3 GB -> pause.  No PM run.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, glob, time, copy, threading, resource, subprocess, hashlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(CFG, "..", "..", "_external_data"))
D654 = os.path.join(CFG, "CFG654_independent_inputs")
SCORER = os.path.join(D654, "cfg654" + "_native.py")
ZK = ("z0", "z0.5", "z1")
KHI256 = math.pi * 256 / (4 * 100.0)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
def peak_rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9          # macOS: bytes (peak)
def free_inactive_gb():
    try:
        out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
        ps = int(out.split("page size of")[1].split()[0]); v = {}
        for ln in out.splitlines():
            if ":" in ln:
                k, x = ln.split(":", 1); v[k.strip()] = x.strip().rstrip(".")
        return (int(v["Pages free"]) + int(v["Pages inactive"])) * ps / 1e9
    except Exception:
        return 99.0
def mem_wait():
    n = 0
    while free_inactive_gb() < 3.0:
        if n % 10 == 0: print(f"MEMORY PAUSE: free + inactive {free_inactive_gb():.1f} GB < 3 GB", flush=True)
        n += 1; time.sleep(30)

# ---------------------------------------------------------------- frozen CFG654 native scorer (read only)
_sp = importlib.util.spec_from_file_location("cfg654_native_readonly", SCORER)
N654 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(N654)
G = N654.load_lib("native_cmb")
Pmat, fit, theory, nuis_spec, support_mask, subset, SURV = (G[k] for k in ("Pmat", "fit", "theory", "nuis_spec", "support_mask", "subset", "SURV"))
PROF = os.path.join(EXT, "cfg530_work", "profiles", "N512")
def Binj(foot):
    d = np.load(os.path.join(PROF, f"cfg526_LR{'can' if foot == 'canonical' else 'alt'}_L100.npz"))
    k = np.array(d["kgrav"]); B = np.array(d["pgrav"]) / np.array(d["ppart"]); lk, lb = np.log(k), np.log(B)
    return lambda KK: np.exp(np.interp(np.log(np.clip(KK, k[0], k[-1])), lk, lb))

def score_pair(F, S, mutate, TOWN=None):
    """cfg654_native.score_production statements, verbatim (as cfg963_attrib.py), run dictionaries passed in, no file I/O."""
    INP = F.get("cfg654_inputs"); assert INP == "native_cmb" and S.get("cfg654_inputs") == INP, "both runs must carry the SAME native input set"
    assert "z0" in F["snap"] and "z0" in S["snap"]
    TOWN = TOWN or {}
    foot = F["foot"]; N, L = int(F["np"]), float(F["L"])
    run, held = N654.build(F, S, N, L, foot, f"L{L:g}_N{N}_{foot}")
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F"); PFh = Pmat(held, "F")
    R = dict(foot=foot, mutate=mutate, surveys={})
    gg = {}
    for key in ZK:
        kk_ = np.array(F["snap"][key]["k"]); rr_ = np.array(F["snap"][key]["P_grav"]) / np.array(S["snap"][key]["P"]); mm_ = kk_ <= 1.0 + 1e-9
        gg[key] = dict(G=float(np.max(np.abs(rr_[mm_] - 1))), at={str(q): float(np.exp(np.interp(math.log(q), np.log(kk_), np.log(rr_)))) for q in (0.3, 0.5, 1.0)})
    R["benchmark"] = gg
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
            R["surveys"][sn] = r; continue
        s0 = fit(Sv, D, PS0); fF_ = fit(Sv, D, PF); d = fF_["chi2"] - s0["chi2"]
        rob = dict(widen2=fit(Sv, D, PF, widen=2.0)["chi2"] - fit(Sv, D, PS0, widen=2.0)["chi2"],
                   noIA=fit(Sv, D, PF, ia=False)["chi2"] - fit(Sv, D, PS0, ia=False)["chi2"],
                   held=fit(Sv, D, PFh)["chi2"] - s0["chi2"],
                   LOC=fit(Sv, D, Pmat(run, "F", bg="LOC"), bg="LOC")["chi2"] - fit(Sv, D, Pmat(run, "S0", bg="LOC"), bg="LOC")["chi2"])
        desi = fit(Sv, D, Pmat(run, "F", bg="DESI"), bg="DESI")["chi2"] - fit(Sv, D, Pmat(run, "S0", bg="DESI"), bg="DESI")["chi2"]
        cls = N654.klass(d, list(rob.values()), N_ok); t_ok = TOWN.get(sn)
        if t_ok is False: cls = "NOT DIAGNOSTIC"; r["T_OWN_failed"] = True
        if t_ok is None: r["T_OWN_missing"] = True
        r.update(chi2_S0=s0["chi2"], chi2_F=fF_["chi2"], dchi2=d, robust=rob, DESI_reported=desi, **{"class": cls})
        R["surveys"][sn] = r
    if mutate:
        R["T_OWN"] = {sn: v.get("T_OWN") for sn, v in R["surveys"].items() if "T_OWN" in v}
        R["NZ1_all_bite"] = all(v.get("NZ1", True) for v in R["surveys"].values())
    return R

# ---------------------------------------------------------------- stored runs + transfers (FROZEN_CRITERIA.md section 2; A1 item 4)
_RUNS = {
    "NCS0": ("cfg654_work/NCS0", "cfg654cmb_cfg650_na_S0_canonical_N1024_*.json"),
    "NC1x": ("cfg654_work/NC1x", "cfg654cmb_cfg650_m1m2m3_RES_canonical_N1024_*.json"),
    "NC2x": ("cfg654_work/NC2x", "cfg654cmb_cfg650_m1m2m3_RES_alt_N1024_*.json"),
    "P0": ("cfg596_work/P0", "cfg596_S0_canonical_N1024_*.json"),
    "T12": ("cfg650_work/T12", "cfg650_m1m2_RES_canonical_N1024_*.json"),
    "T1x": ("cfg650_work/T1x", "cfg650_m1m2m3_RES_canonical_N1024_*.json"),
    "T2x": ("cfg650_work/T2x", "cfg650_m1m2m3_RES_alt_N1024_*.json"),
    "VLs": ("cfg596_work/VLs", "cfg596_S0_canonical_N256_*.json"),
    "V0": ("cfg650_work/V0", "cfg650_off_RES_canonical_N256_*.json"),
    "VM3": ("cfg650_work/VM3", "cfg650_m3_RES_canonical_N256_*.json"),
    "VM12": ("cfg650_work/VM12", "cfg650_m1m2_RES_canonical_N256_*.json"),
    "VM123": ("cfg650_work/VM123", "cfg650_m1m2m3_RES_canonical_N256_*.json"),
    "SC1x": ("cfg960_work/SC1x", "cfg960sctm_*_SCT_canonical_N1024_*.json"),
}
_J = {}; PROV = {}
def run(name):
    """stored run dictionary by name (read only; cached)."""
    if name not in _J:
        sub, pat = _RUNS[name]; g = sorted(glob.glob(os.path.join(EXT, sub, pat))); assert len(g) == 1, (name, g)
        _J[name] = json.load(open(g[0])); PROV[name] = dict(file=os.path.join("_external_data", sub, os.path.basename(g[0])), sha256=sha(g[0]))
    return _J[name]
CFG646_JSON = os.path.join(CFG, "CFG646_kids_anatomy_gas_expulsion", "cfg646_expulsion_pm.json")
TRANSFER_NAMES = ("M3-1024", "M3-256", "M3-alone-256", "CFG646-R3", "unit")
_TR = {}
def transfer(name):
    """T(k, z) on NCS0's 1024^3 bins: {key: dict(grav=..., part=...)}.  M3-1024 = PRIMARY (T1x / T12)."""
    if name in _TR: return _TR[name]
    k1 = np.array(run("NCS0")["snap"]["z0"]["k"]); out = {}
    def to1024(kb, t):
        return np.exp(np.interp(np.log(np.minimum(k1, KHI256)), np.log(kb), np.log(t)))
    if name == "unit":
        out = {key: dict(grav=np.ones_like(k1), part=np.ones_like(k1)) for key in ZK}
    elif name == "CFG646-R3":
        d = json.load(open(CFG646_JSON))["sources"]["P1"]["nodes"]
        for key in ZK:
            kb = np.array(d[key]["k"]); t = np.array(d[key]["ratio"]["DIFF-S"])
            out[key] = dict(grav=to1024(kb, t), part=np.ones_like(k1))       # static post-process: particles not moved
    else:
        a, b = {"M3-1024": ("T1x", "T12"), "M3-256": ("VM123", "VM12"), "M3-alone-256": ("VM3", "V0")}[name]
        for key in ZK:
            ka = np.array(run(a)["snap"][key]["k"]); assert np.allclose(ka, np.array(run(b)["snap"][key]["k"]), rtol=1e-6)
            tg = np.array(run(a)["snap"][key]["P_grav"]) / np.array(run(b)["snap"][key]["P_grav"])
            tp = np.array(run(a)["snap"][key]["P"]) / np.array(run(b)["snap"][key]["P"])
            if int(run(a)["np"]) == 256: tg, tp = to1024(ka, tg), to1024(ka, tp)
            else: assert np.allclose(ka, k1, rtol=1e-6)
            out[key] = dict(grav=tg, part=tp)
    _TR[name] = out; return out

def surrogate_S(T, label):
    """control-slot surrogate NCS0 x T: the control's lensing spectrum is its GRAVITATING spectrum (criteria section 2)."""
    S = copy.deepcopy(run("NCS0")); S["cfg963_surrogate"] = label
    for key in ZK:
        pS = np.array(run("NCS0")["snap"][key]["P"]); v = (pS * T[key]["grav"]).tolist()
        S["snap"][key]["P"] = v; S["snap"][key]["P_grav"] = list(v)
    return S
def surrogate_F(T, foot, label):
    """framework-slot surrogate S0+X: P_grav = P_NCS0 x T^grav, P = P_NCS0 x T^part."""
    F = copy.deepcopy(run("NCS0")); F["foot"] = foot; F["cfg963_surrogate"] = label
    for key in ZK:
        pS = np.array(run("NCS0")["snap"][key]["P"])
        F["snap"][key]["P_grav"] = (pS * T[key]["grav"]).tolist(); F["snap"][key]["P"] = (pS * T[key]["part"]).tolist()
    return F
def score_vs_feedback_control(F, transfer_name="M3-1024", mutate=False, TOWN=None):
    """REUSABLE: frozen-scorer score of run F against the feedback-matched control NCS0 x T_M3(k, z) (bracket by name)."""
    k1 = np.array(run("NCS0")["snap"]["z0"]["k"])
    for key in ZK: assert np.allclose(np.array(F["snap"][key]["k"]), k1, rtol=1e-6), "run must share NCS0's 1024^3 L100 k bins"
    return score_pair(F, surrogate_S(transfer(transfer_name), transfer_name), mutate, TOWN)
def score_vs_NCS0(F, mutate=False, TOWN=None):
    return score_pair(F, run("NCS0"), mutate, TOWN)

def line(name, R):
    if R["mutate"]:
        return "  " + name + ": " + "; ".join(f"{sn} N {v['N_kept']} NZ1 {'bites' if v.get('NZ1') else 'FAILS'} T-OWN {v.get('T_OWN_chi2', float('nan')):.2f} -> {'DIAGNOSTIC' if v.get('T_OWN') else 'NOT DIAGNOSTIC'}" for sn, v in R["surveys"].items())
    s = []
    for sn, v in R["surveys"].items():
        if "dchi2" not in v: s.append(f"{sn} N {v['N_kept']} {v['class']}"); continue
        s.append(f"{sn} N {v['N_kept']}: chi2 S0 {v['chi2_S0']:.2f} F {v['chi2_F']:.2f} dchi2 {v['dchi2']:+.2f} robust " +
                 "/".join(f"{x:+.2f}" for x in v["robust"].values()) + f" DESI {v['DESI_reported']:+.2f} -> {v['class']}")
    return "  " + name + ": " + " | ".join(s)
def _js(o):
    if isinstance(o, dict): return {k: _js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_js(v) for v in o]
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o

def main():
    def _rss_guard():
        while True:
            if peak_rss_gb() > 0.95:
                print(f"RSS GUARD: peak RSS {peak_rss_gb():.3f} GB > 0.95 GB -> exit 3", flush=True); os._exit(3)
            time.sleep(1.0)
    threading.Thread(target=_rss_guard, daemon=True).start()
    MUT = os.environ.get("CFG596_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
    T0 = time.time(); OUT = []
    def P(*a):
        s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
    P(f"CFG963 amendment A1 (64718930a): reusable feedback-matched scorer, extra controls, SC1x vs NCS0 x F_M3 ({'MUTATE pass' if MUT else 'main pass'}). REPORTED ONLY.")
    P(f"frozen CFG654 native scorer imported read only (sha256 {sha(SCORER)[:16]}...). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    R3 = transfer("CFG646-R3")
    P("bracket R3 (CFG646 static DIFF-S, P1 canonical) T^grav at k 0.3/0.5/1/2 (z0 | z0.5 | z1): " + " | ".join(
        "/".join(f"{float(np.exp(np.interp(math.log(q), np.log(np.array(run('NCS0')['snap']['z0']['k'])), np.log(R3[key]['grav'])))):.3f}" for q in (0.3, 0.5, 1.0, 2.0)) for key in ZK))
    PAIRS = [("K3_NC1x_vs_NCS0x1", lambda: score_vs_feedback_control(run("NC1x"), "unit", MUT, TOWN.get("K3_NC1x_vs_NCS0x1"))),
             ("K3_NC2x_vs_NCS0x1", lambda: score_vs_feedback_control(run("NC2x"), "unit", MUT, TOWN.get("K3_NC2x_vs_NCS0x1"))),
             ("K4_SC1x_vs_NCS0x1", lambda: score_vs_feedback_control(run("SC1x"), "unit", MUT, TOWN.get("K4_SC1x_vs_NCS0x1"))),
             ("S0+M3[CFG646-R3]_canonical_vs_NCS0", lambda: score_pair(surrogate_F(R3, "canonical", "CFG646-R3"), run("NCS0"), MUT, TOWN.get("S0+M3[CFG646-R3]_canonical_vs_NCS0"))),
             ("S0+M3[CFG646-R3]_alt_vs_NCS0", lambda: score_pair(surrogate_F(R3, "alt", "CFG646-R3"), run("NCS0"), MUT, TOWN.get("S0+M3[CFG646-R3]_alt_vs_NCS0"))),
             ("NC1x_vs_S0+M3[CFG646-R3]", lambda: score_vs_feedback_control(run("NC1x"), "CFG646-R3", MUT, TOWN.get("NC1x_vs_S0+M3[CFG646-R3]"))),
             ("NC2x_vs_S0+M3[CFG646-R3]", lambda: score_vs_feedback_control(run("NC2x"), "CFG646-R3", MUT, TOWN.get("NC2x_vs_S0+M3[CFG646-R3]")))]
    for t in ("M3-1024", "M3-256", "M3-alone-256", "CFG646-R3"):
        PAIRS.append((f"SC1x_vs_S0+M3[{t}]", (lambda t=t: score_vs_feedback_control(run("SC1x"), t, MUT, TOWN.get(f"SC1x_vs_S0+M3[{t}]")))))
    MFN = os.path.join(HERE, "cfg963_reuse_results_MUTATE.json")
    if MUT:
        TOWN = {}
    else:
        assert os.path.exists(MFN), "run the MUTATE pass first (CFG596_MUTATE=1)"
        MU = json.load(open(MFN)); assert MU.get("K_mutate_pass"), "MUTATE-pass K items failed: nothing is interpreted"
        TOWN = {nm: v["T_OWN"] for nm, v in MU["pairs"].items()}
    RES = dict(lane="CFG963", amendment="AMENDMENT_A1_2026-10-23.md (64718930a)", criteria="FROZEN_CRITERIA.md (d3b18181c)", mutate=MUT,
               scorer=dict(file="CFG654_independent_inputs/cfg654" + "_native.py", sha256=sha(SCORER)), pairs={})
    RES["transfer_R3_at"] = {key: {str(q): float(np.exp(np.interp(math.log(q), np.log(np.array(run('NCS0')['snap']['z0']['k'])), np.log(R3[key]['grav'])))) for q in (0.3, 0.5, 1.0, 2.0, 4.0)} for key in ZK}
    P("\n" + ("scorer MUTATE pass (NZ1, T-OWN):" if MUT else "main pass (T-OWN per pair from the MUTATE pass):"))
    for nm, fn in PAIRS:
        mem_wait(); R = fn(); RES["pairs"][nm] = R; P(line(nm, R))
    D960 = os.path.join(CFG, "CFG960_sctm_engine")
    if MUT:
        st = {"K3_NC1x_vs_NCS0x1": os.path.join(D654, "cfg654_native_results_NC1x_MUTATE.json"), "K3_NC2x_vs_NCS0x1": os.path.join(D654, "cfg654_native_results_NC2x_MUTATE.json"),
              "K4_SC1x_vs_NCS0x1": os.path.join(D960, "cfg960_score_results_SC1x_MUTATE.json")}
        kd = max(abs(RES["pairs"][nm]["surveys"][sn]["T_OWN_chi2"] - json.load(open(f))["surveys"][sn]["T_OWN_chi2"]) for nm, f in st.items() for sn in ("KiDS", "DES"))
        RES["K_mutate_max_abs_diff"] = kd; RES["K_mutate_pass"] = bool(kd <= 1e-9)
        RES["NZ1_all_bite"] = all(R.get("NZ1_all_bite", True) for R in RES["pairs"].values())
        P(f"K3/K4 (MUTATE): T-OWN chi2 vs stored, max |diff| {kd:.3e} -> {'PASS' if kd <= 1e-9 else 'FAIL'}; NZ1 bites everywhere: {RES['NZ1_all_bite']}")
    else:
        # ---- K3 / K4: exact reproduction of stored production scores through the control slot
        st = {"K3_NC1x_vs_NCS0x1": os.path.join(D654, "cfg654_native_results_NC1x.json"), "K3_NC2x_vs_NCS0x1": os.path.join(D654, "cfg654_native_results_NC2x.json"),
              "K4_SC1x_vs_NCS0x1": os.path.join(D960, "cfg960_score_results_SC1x.json")}
        kd = 0.0; cls_ok = True
        for nm, f in st.items():
            a_ = json.load(open(f))["surveys"]
            for sn in ("KiDS", "DES"):
                a, b = a_[sn], RES["pairs"][nm]["surveys"][sn]
                cls_ok &= (a["N_kept"] == b["N_kept"] and a["class"] == b["class"])
                kd = max([kd, abs(a["chi2_S0"] - b["chi2_S0"]), abs(a["chi2_F"] - b["chi2_F"]), abs(a["dchi2"] - b["dchi2"]), abs(a["DESI_reported"] - b["DESI_reported"])] +
                         [abs(a["robust"][q] - b["robust"][q]) for q in a["robust"]])
        RES["K34_max_abs_diff"] = kd; RES["K34_pass"] = bool(kd <= 1e-9 and cls_ok)
        P(f"\nK3/K4: NC1x, NC2x, SC1x vs NCS0 x 1 reproduce the stored CFG654 / CFG960 scores: max |diff| {kd:.3e}, N_kept and classes equal {cls_ok} -> {'PASS' if RES['K34_pass'] else 'FAIL'}")
        # ---- K2: inherited-pipeline reproduction of CFG650 T12 / T1x / T2x vs CFG596 P0 (frozen CFG654 module, inherited library)
        Ginh = N654.load_lib("inherited"); D650 = os.path.join(CFG, "CFG650_theory_v2_combined_pm")
        st650 = {"T12": json.load(open(os.path.join(D650, "cfg650_native_results_T12.json")))["runs"]["L100_N1024_canonical"]["surveys"],
                 "T1x": json.load(open(os.path.join(D650, "cfg650_native_results.json")))["runs"]["L100_N1024_canonical"]["surveys"],
                 "T2x": json.load(open(os.path.join(D650, "cfg650_native_results.json")))["runs"]["L100_N1024_alt"]["surveys"]}
        k2 = 0.0; k2n = True; RES["K2"] = {}
        for j, foot in (("T12", "canonical"), ("T1x", "canonical"), ("T2x", "alt")):
            mem_wait(); o = N654.score(Ginh, run(j), run("P0"), foot, robust=("widen2", "noIA", "held", "DESI"), extra_bg=()); RES["K2"][j] = o
            for sn in ("KiDS", "DES"):
                a, b = st650[j][sn], o[sn]; k2n &= (a["N_kept"] == b["N"])
                k2 = max([k2, abs(a["dchi2"] - b["dchi2"])] + [abs(a["robust"][q] - b["robust"][q]) for q in ("widen2", "noIA", "held", "DESI")])
            P(f"  K2 {j} ({foot}) vs P0, inherited pipeline: KiDS N {o['KiDS']['N']} dchi2 {o['KiDS']['dchi2']:+.3f} (stored {st650[j]['KiDS']['dchi2']:+.3f}); DES dchi2 {o['DES']['dchi2']:+.3f} (stored {st650[j]['DES']['dchi2']:+.3f})")
        RES["K2_max_abs_diff"] = k2; RES["K2_pass"] = bool(k2 <= 1e-6 and k2n)
        stepM3 = RES["K2"]["T1x"]["KiDS"]["dchi2"] - RES["K2"]["T12"]["KiDS"]["dchi2"]
        RES["inherited_step_T12_to_T1x_KiDS"] = stepM3
        P(f"K2: max |diff| {k2:.3e}, N_kept equal {k2n} -> {'PASS' if RES['K2_pass'] else 'FAIL'}; inherited pipeline, same ICs: S0 -> T12 (M1+M2) {RES['K2']['T12']['KiDS']['dchi2']:+.2f}, T12 -> T1x (adding M3) {stepM3:+.2f} (KiDS)")
        # ---- R3 attribution (section 6 rule, reported only)
        A0 = json.load(open(os.path.join(HERE, "cfg963_attrib_results.json")))["attribution"]
        dk = lambda nm: RES["pairs"][nm]["surveys"]["KiDS"]["dchi2"]
        RES["R3_attribution"] = {}
        for foot, x in (("canonical", "NC1x"), ("alt", "NC2x")):
            dN = A0[foot]["dchi2_framework_vs_NCS0"]; a3 = dk(f"S0+M3[CFG646-R3]_{foot}_vs_NCS0"); d = dk(f"{x}_vs_S0+M3[CFG646-R3]"); f = a3 / dN
            cls = "M3-CARRIED" if (f >= 0.70 and abs(d) <= 3.0) else ("LAW-CARRIED" if f < 0.30 else "SHARED")
            RES["R3_attribution"][foot] = dict(dchi2_S0M3_vs_NCS0=a3, f=f, dchi2_framework_vs_S0M3=d, attribution=cls)
            P(f"  R3 [{foot}]: S0+M3[CFG646-R3] vs NCS0 {a3:+.2f} -> f {f:.2f}; {x} vs S0+M3[R3] {d:+.2f} -> {cls} (reported only)")
        # ---- SC1x vs the feedback-matched control (CFG960 A2, reported only)
        sc0 = RES["pairs"]["K4_SC1x_vs_NCS0x1"]["surveys"]["KiDS"]
        P(f"\nSC1x (CFG960 SCT-M, canonical; SC2x not run) vs NCS0 (frozen CFG960 reading, first): KiDS dchi2 {sc0['dchi2']:+.2f} -> {sc0['class']}")
        RES["SC1x"] = dict(vs_NCS0=dict(dchi2=sc0["dchi2"], cls=sc0["class"]), vs_feedback_control={})
        for t in ("M3-1024", "M3-256", "M3-alone-256", "CFG646-R3"):
            v = RES["pairs"][f"SC1x_vs_S0+M3[{t}]"]["surveys"]["KiDS"]; w = RES["pairs"][f"SC1x_vs_S0+M3[{t}]"]["surveys"]["DES"]
            rd = ("over-produces structure relative to plain dust plus the same gas expulsion" if v["class"] == "EXCLUDED" else
                  "does not over-produce relative to plain dust plus the same expulsion" if v["class"] == "CONSISTENT" else v["class"])
            RES["SC1x"]["vs_feedback_control"][t] = dict(KiDS_dchi2=v["dchi2"], KiDS_robust=v["robust"], KiDS_class=v["class"], DES_dchi2=w["dchi2"], DES_class=w["class"], reading=rd)
            P(f"  SC1x vs NCS0 x F_M3[{t}]: KiDS dchi2 {v['dchi2']:+.2f} (robust " + "/".join(f"{q:+.2f}" for q in v["robust"].values()) + f") -> {v['class']}; DES {w['dchi2']:+.2f} -> {w['class']}; reading: SCT-M {rd}")
    RES["runs"] = PROV; RES["runtime_s"] = time.time() - T0; RES["peak_rss_gb"] = peak_rss_gb()
    P(f"\ndone in {RES['runtime_s']:.0f} s; peak RSS {RES['peak_rss_gb']:.3f} GB")
    json.dump(_js(RES), open(os.path.join(HERE, f"cfg963_reuse_results{SUF}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg963_reuse{SUF}.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
