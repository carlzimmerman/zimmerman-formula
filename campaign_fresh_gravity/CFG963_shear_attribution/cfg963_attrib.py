#!/usr/bin/env python3
"""CFG963: attribution of the native shear pass (FROZEN_CRITERIA.md, commit d3b18181c).  DIAGNOSTIC, no verdict weight.
Is the KiDS lead of NC1x / NC2x over NCS0 carried by the cold-sector rules (M1+M2) or by the census gas expulsion M3, which the
plain-Poisson control NCS0 lacks?  Surrogates S0+M3 = NCS0 x T_M3(k, z) and S0+M12 = NCS0 x T_M12(k, z) (transfers measured node by
node from matched stored runs, criteria section 2) are scored with the FROZEN CFG654 native scorer (imported read only; its
score_production statements re-implemented verbatim below, writing into THIS folder).  Scoring and arithmetic only: no PM run.
Usage (one process, one thread, nice 10; MUTATE FIRST):
  CFG596_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg963_attrib.py  -> cfg963_attrib_MUTATE.out / cfg963_attrib_results_MUTATE.json
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg963_attrib.py                  -> cfg963_attrib.out / cfg963_attrib_results.json
Guards: peak RSS > 0.95 GB -> exit 3 (CFG960's gate waits on python > 1 GB); free + inactive memory < 3 GB -> pause.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, glob, time, copy, threading, resource, subprocess, hashlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(CFG, "..", "..", "_external_data"))
MUTATE = os.environ.get("CFG596_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- guards (memory: this lane must stay light while CFG960 waits)
RSS_CAP_GB = 0.95
def peak_rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9          # macOS: bytes (peak)
def _rss_guard():
    while True:
        if peak_rss_gb() > RSS_CAP_GB:
            print(f"RSS GUARD: peak RSS {peak_rss_gb():.3f} GB > {RSS_CAP_GB} GB -> exit 3", flush=True); os._exit(3)
        time.sleep(1.0)
threading.Thread(target=_rss_guard, daemon=True).start()
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

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

# ---------------------------------------------------------------- the frozen CFG654 native scorer, imported read only
D654 = os.path.join(CFG, "CFG654_independent_inputs")
SCORER = os.path.join(D654, "cfg654" + "_native.py")
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
    """cfg654_native.score_production statements, verbatim, with the run dictionaries passed in (no file I/O)."""
    INP = F.get("cfg654_inputs"); assert INP == "native_cmb" and S.get("cfg654_inputs") == INP, "both runs must carry the SAME native input set"
    assert "z0" in F["snap"] and "z0" in S["snap"]
    TOWN = TOWN or {}
    foot = F["foot"]; N, L = int(F["np"]), float(F["L"])
    run, held = N654.build(F, S, N, L, foot, f"L{L:g}_N{N}_{foot}")
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F"); PFh = Pmat(held, "F")
    R = dict(foot=foot, mutate=mutate, surveys={})
    gg = {}
    for key in ("z0", "z0.5", "z1"):
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

def line(name, R):
    if R["mutate"]:
        return "  " + name + ": " + "; ".join(f"{sn} N {v['N_kept']} NZ1 {'bites' if v.get('NZ1') else 'FAILS'} T-OWN {v.get('T_OWN_chi2', float('nan')):.2f} -> {'DIAGNOSTIC' if v.get('T_OWN') else 'NOT DIAGNOSTIC'}" for sn, v in R["surveys"].items())
    s = []
    for sn, v in R["surveys"].items():
        if "dchi2" not in v: s.append(f"{sn} N {v['N_kept']} {v['class']}"); continue
        s.append(f"{sn} N {v['N_kept']}: chi2 S0 {v['chi2_S0']:.2f} F {v['chi2_F']:.2f} dchi2 {v['dchi2']:+.2f} robust " +
                 "/".join(f"{x:+.2f}" for x in v["robust"].values()) + f" DESI {v['DESI_reported']:+.2f} -> {v['class']}")
    return "  " + name + ": " + " | ".join(s)

# ---------------------------------------------------------------- stored runs (read only)
RUNS = {
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
    "VNcs": ("cfg654_work/VNcs", "cfg654cmb_cfg650_na_S0_canonical_N256_*.json"),
    "VNc12": ("cfg654_work/VNc12", "cfg654cmb_cfg650_m1m2_RES_canonical_N256_*.json"),
}
J = {}; PROV = {}
for n, (sub, pat) in RUNS.items():
    g = sorted(glob.glob(os.path.join(EXT, sub, pat))); assert len(g) == 1, (n, g)
    J[n] = json.load(open(g[0])); PROV[n] = dict(file=os.path.join("_external_data", sub, os.path.basename(g[0])), sha256=sha(g[0]))
ZK = ("z0", "z0.5", "z1")
K1024 = np.array(J["NCS0"]["snap"]["z0"]["k"])
for n in J:
    for key in ZK:
        kk = np.array(J[n]["snap"][key]["k"])
        ref = K1024 if int(J[n]["np"]) == 1024 else np.array(J["VLs"]["snap"]["z0"]["k"])
        assert kk.shape == ref.shape and np.allclose(kk, ref, rtol=1e-6), (n, key)
K256 = np.array(J["VLs"]["snap"]["z0"]["k"]); KHI256 = math.pi * 256 / (4 * 100.0); KHI1024 = math.pi * 1024 / (4 * 100.0)

# ---------------------------------------------------------------- transfers (criteria section 2)
TSPEC = {   # name: (numerator run, denominator run, denominator field for the gravitating ratio)
    "M3-1024": ("T1x", "T12", "P_grav"), "M3-256": ("VM123", "VM12", "P_grav"), "M3-alone-256": ("VM3", "V0", "P_grav"),
    "M12-1024": ("T12", "P0", "P"), "M12-256n": ("VNc12", "VNcs", "P"), "M12-256i": ("VM12", "VLs", "P"),
    "C1-can": ("T1x", "P0", "P"), "C1-alt": ("T2x", "P0", "P"),
}
def transfer(name):
    a, b, fden = TSPEC[name]; out = {}
    for key in ZK:
        tg = np.array(J[a]["snap"][key]["P_grav"]) / np.array(J[b]["snap"][key][fden])
        tp = np.array(J[a]["snap"][key]["P"]) / np.array(J[b]["snap"][key]["P"])
        if int(J[a]["np"]) == 256:
            kq = np.minimum(K1024, KHI256)
            tg = np.exp(np.interp(np.log(kq), np.log(K256), np.log(tg))); tp = np.exp(np.interp(np.log(kq), np.log(K256), np.log(tp)))
        out[key] = dict(grav=tg, part=tp)
    return out
TR = {n: transfer(n) for n in TSPEC}
TR["unit"] = {key: dict(grav=np.ones_like(K1024), part=np.ones_like(K1024)) for key in ZK}
TR["plant0.9"] = {key: dict(grav=np.full_like(K1024, 0.9), part=np.full_like(K1024, 0.9)) for key in ZK}
def tab_at(T, qs=(0.3, 0.5, 1.0, 2.0, 4.0, 8.0)):
    return {key: {str(q): float(np.exp(np.interp(math.log(q), np.log(K1024), np.log(T[key]["grav"])))) for q in qs} for key in ZK}

def surrogate_F(T, foot, label):
    F = copy.deepcopy(J["NCS0"]); F["foot"] = foot; F["cfg963_surrogate"] = label
    for key in ZK:
        pS = np.array(J["NCS0"]["snap"][key]["P"])
        F["snap"][key]["P_grav"] = (pS * T[key]["grav"]).tolist(); F["snap"][key]["P"] = (pS * T[key]["part"]).tolist()
    return F
def surrogate_S(T, label):
    S = copy.deepcopy(J["NCS0"]); S["cfg963_surrogate"] = label
    for key in ZK:
        pS = np.array(J["NCS0"]["snap"][key]["P"]); v = (pS * T[key]["grav"]).tolist()
        S["snap"][key]["P"] = v; S["snap"][key]["P_grav"] = list(v)
    return S

# ---------------------------------------------------------------- the scored pairs (criteria section 5)
PAIRS = [("K_NC1x_vs_NCS0", lambda: (J["NC1x"], J["NCS0"])), ("K_NC2x_vs_NCS0", lambda: (J["NC2x"], J["NCS0"]))]
for t in ("M3-1024", "M3-256", "M3-alone-256", "M12-1024", "M12-256n", "M12-256i"):
    for foot in ("canonical", "alt"):
        nm = ("S0+M3" if t.startswith("M3") else "S0+M12") + f"[{t}]_{foot}_vs_NCS0"
        PAIRS.append((nm, (lambda t=t, foot=foot: (surrogate_F(TR[t], foot, t), J["NCS0"]))))
PAIRS.append(("C1-can_vs_NCS0", lambda: (surrogate_F(TR["C1-can"], "canonical", "C1-can"), J["NCS0"])))
PAIRS.append(("C1-alt_vs_NCS0", lambda: (surrogate_F(TR["C1-alt"], "alt", "C1-alt"), J["NCS0"])))
for x in ("NC1x", "NC2x"):
    for t in ("M3-1024", "M3-256", "M3-alone-256", "M12-1024"):
        nm = f"{x}_vs_" + ("S0+M3" if t.startswith("M3") else "S0+M12") + f"[{t}]"
        PAIRS.append((nm, (lambda x=x, t=t: (J[x], surrogate_S(TR[t], t)))))
PLANTS = [("M0_unit_vs_NCS0", lambda: (surrogate_F(TR["unit"], "canonical", "unit"), J["NCS0"])),
          ("M1_plant0.9_vs_NCS0", lambda: (surrogate_F(TR["plant0.9"], "canonical", "plant0.9"), J["NCS0"]))]

RES = dict(lane="CFG963", criteria="FROZEN_CRITERIA.md (d3b18181c)", mutate=MUTATE, scorer=dict(file="CFG654_independent_inputs/cfg654" + "_native.py", sha256=sha(SCORER)),
           runs=PROV, k_hi_1024=KHI1024, k_hi_256=KHI256, transfers={n: tab_at(T) for n, T in TR.items() if n not in ("unit",)}, pairs={})
P(f"CFG963 attribution of the native shear pass ({'MUTATE pass' if MUTATE else 'main pass'}); frozen CFG654 native scorer imported read only (sha256 {RES['scorer']['sha256'][:16]}...)")
P("DIAGNOSTIC, no verdict weight. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
P("transfers T^grav at k 0.3 / 0.5 / 1 / 2 / 4 / 8 h/Mpc (z0 | z0.5 | z1):")
for n, tb in RES["transfers"].items():
    P(f"  {n:13s} " + " | ".join("/".join(f"{v:.3f}" for v in tb[key].values()) for key in ZK))
fi = {key: {str(q): float(np.exp(np.interp(math.log(q), np.log(K1024), np.log(np.array(J["T2x"]["snap"][key]["P_grav"]) / np.array(J["T1x"]["snap"][key]["P_grav"])))))
            for q in (0.3, 0.5, 1.0, 2.0)} for key in ZK}
RES["footing_indicator_T2x_over_T1x_grav"] = fi
RES["m3_expelled_mass_frac"] = {n: {key: J[n]["snap"][key].get("m3_expelled_mass_frac") for key in ZK} for n in ("NC1x", "NC2x", "T1x", "T2x", "VM123", "VM3")}
RES["e_sum"] = {n: {key: J[n]["snap"][key].get("e_sum") for key in ZK} for n in ("T12", "T1x", "VM12", "VM123")}
P("footing indicator P_grav(T2x)/P_grav(T1x) at k 0.3/0.5/1/2: " + " | ".join("/".join(f"{v:.3f}" for v in fi[key].values()) for key in ZK))
P("M3 expelled mass fraction (z0/z0.5/z1): " + "; ".join(f"{n} " + "/".join(f"{v:.4f}" for v in d.values()) for n, d in RES["m3_expelled_mass_frac"].items()))

MFN = os.path.join(HERE, "cfg963_attrib_results_MUTATE.json")
if MUTATE:
    P("\nscorer MUTATE pass (NZ1, T-OWN) for every pair:")
    for nm, mk in PAIRS:
        mem_wait(); F, S = mk(); R = score_pair(F, S, True); RES["pairs"][nm] = R; P(line(nm, R))
    st = {x: json.load(open(os.path.join(D654, f"cfg654_native_results_{x}_MUTATE.json"))) for x in ("NC1x", "NC2x")}
    kd = max(abs(RES["pairs"][f"K_{x}_vs_NCS0"]["surveys"][sn]["T_OWN_chi2"] - st[x]["surveys"][sn]["T_OWN_chi2"]) for x in st for sn in ("KiDS", "DES"))
    RES["K_mutate_max_abs_diff"] = kd; RES["K_mutate_pass"] = bool(kd <= 1e-9)
    P(f"K (MUTATE): T-OWN chi2 vs stored CFG654 MUTATE results, max |diff| {kd:.3e} -> {'PASS' if kd <= 1e-9 else 'FAIL'}")
    P("\nplanted controls (full scoring vs NCS0; T-OWN from the K MUTATE pass on NCS0):")
    TOWN_can = RES["pairs"]["K_NC1x_vs_NCS0"]["T_OWN"]
    for nm, mk in PLANTS:
        mem_wait(); F, S = mk(); R = score_pair(F, S, False, TOWN_can); RES["pairs"][nm] = R; P(line(nm, R))
    m0 = RES["pairs"]["M0_unit_vs_NCS0"]["surveys"]
    m0max = max(max([abs(v["dchi2"]), abs(v["DESI_reported"])] + [abs(x) for x in v["robust"].values()]) for v in m0.values())
    m1 = RES["pairs"]["M1_plant0.9_vs_NCS0"]["surveys"]["KiDS"]["dchi2"]
    RES["M0_max_abs"] = m0max; RES["M0_pass"] = bool(m0max <= 1e-9); RES["M1_KiDS_dchi2"] = m1; RES["M1_bites"] = bool(abs(m1) >= 1.0)
    P(f"M0 (T = 1): max |dchi2| over surveys and variants {m0max:.3e} -> {'PASS' if RES['M0_pass'] else 'FAIL'}")
    P(f"M1 (T = 0.9 planted): KiDS dchi2 {m1:+.2f} -> {'BITES' if RES['M1_bites'] else 'DOES NOT BITE'}")
    RES["NZ1_all_bite"] = all(R.get("NZ1_all_bite", True) for R in RES["pairs"].values() if R["mutate"])
    P(f"NZ1 bites on every pair x survey: {RES['NZ1_all_bite']}")
else:
    assert os.path.exists(MFN), "run the MUTATE pass first (CFG596_MUTATE=1)"
    MU = json.load(open(MFN))
    assert MU.get("K_mutate_pass") and MU.get("M0_pass") and MU.get("M1_bites"), "MUTATE-pass controls failed: nothing is interpreted"
    P("\nmain pass (T-OWN per pair from the MUTATE pass):")
    for nm, mk in PAIRS:
        mem_wait(); F, S = mk(); R = score_pair(F, S, False, MU["pairs"][nm]["T_OWN"]); RES["pairs"][nm] = R; P(line(nm, R))
    # ---- K: reproduction of the stored CFG654 production scores
    kd = 0.0
    for x in ("NC1x", "NC2x"):
        st = json.load(open(os.path.join(D654, f"cfg654_native_results_{x}.json")))["surveys"]; me = RES["pairs"][f"K_{x}_vs_NCS0"]["surveys"]
        for sn in ("KiDS", "DES"):
            a, b = st[sn], me[sn]
            assert a["N_kept"] == b["N_kept"] and a["class"] == b["class"], (x, sn)
            kd = max([kd, abs(a["chi2_S0"] - b["chi2_S0"]), abs(a["chi2_F"] - b["chi2_F"]), abs(a["dchi2"] - b["dchi2"]), abs(a["DESI_reported"] - b["DESI_reported"])] +
                     [abs(a["robust"][q] - b["robust"][q]) for q in a["robust"]])
    RES["K_max_abs_diff"] = kd; RES["K_pass"] = bool(kd <= 1e-9)
    P(f"\nK: stored NC1x / NC2x vs NCS0 reproduced, max |diff| {kd:.3e} -> {'PASS' if RES['K_pass'] else 'FAIL'}")
    # ---- closure C1 and attribution (criteria sections 4 and 6), KiDS
    dk = lambda nm, sn="KiDS": RES["pairs"][nm]["surveys"][sn]["dchi2"]
    ATT = {}
    for foot, x, cl in (("canonical", "NC1x", "C1-can"), ("alt", "NC2x", "C1-alt")):
        dN = dk(f"K_{x}_vs_NCS0"); dC = dk(f"{cl}_vs_NCS0"); c_ok = abs(dC - dN) <= 2.0
        A = dict(footing=foot, framework=x, dchi2_framework_vs_NCS0=dN, closure=dict(name=cl, dchi2=dC, diff=dC - dN, PASS=bool(c_ok)), by_transfer={})
        for t in ("M3-1024", "M3-256", "M3-alone-256"):
            a3 = dk(f"S0+M3[{t}]_{foot}_vs_NCS0"); d = dk(f"{x}_vs_S0+M3[{t}]"); f = a3 / dN
            cls = "M3-CARRIED" if (f >= 0.70 and abs(d) <= 3.0) else ("LAW-CARRIED" if f < 0.30 else "SHARED")
            rb = RES["pairs"][f"{x}_vs_S0+M3[{t}]"]["surveys"]["KiDS"]["robust"]
            dist = bool(abs(d) >= 4.0 and (all(v > 0 for v in rb.values()) or all(v < 0 for v in rb.values())))
            fr = {q: RES["pairs"][f"S0+M3[{t}]_{foot}_vs_NCS0"]["surveys"]["KiDS"]["robust"][q] / RES["pairs"][f"K_{x}_vs_NCS0"]["surveys"]["KiDS"]["robust"][q] for q in rb}
            fr["DESI"] = RES["pairs"][f"S0+M3[{t}]_{foot}_vs_NCS0"]["surveys"]["KiDS"]["DESI_reported"] / RES["pairs"][f"K_{x}_vs_NCS0"]["surveys"]["KiDS"]["DESI_reported"]
            A["by_transfer"][t] = dict(dchi2_S0M3_vs_NCS0=a3, f=f, f_selfconsistent=a3 / dC, dchi2_framework_vs_S0M3=d, d_robust=rb, f_robust=fr,
                                       attribution=cls + ("" if c_ok else " [transfer-limited: C1 closure FAILS]"), KiDS_distinguishes=dist)
        a12 = dk(f"S0+M12[M12-1024]_{foot}_vs_NCS0"); A["M12"] = dict(
            {t: dict(dchi2_S0M12_vs_NCS0=dk(f"S0+M12[{t}]_{foot}_vs_NCS0"), f_M12=dk(f"S0+M12[{t}]_{foot}_vs_NCS0") / dN) for t in ("M12-1024", "M12-256n", "M12-256i")},
            dchi2_framework_vs_S0M12=dk(f"{x}_vs_S0+M12[M12-1024]"), f_sum_primary=A["by_transfer"]["M3-1024"]["f"] + a12 / dN)
        pr = A["by_transfer"]["M3-1024"]["attribution"].split(" ")[0]; r1 = A["by_transfer"]["M3-256"]["attribution"].split(" ")[0]
        A["class_primary"] = A["by_transfer"]["M3-1024"]["attribution"] + ("" if pr == r1 else " [not robust to the resolution transfer]")
        ATT[foot] = A
        P(f"\n[{foot}] {x} vs NCS0 {dN:+.2f}; closure {cl} vs NCS0 {dC:+.2f} (diff {dC - dN:+.2f}) -> {'PASS' if c_ok else 'FAIL'}")
        for t, b in A["by_transfer"].items():
            P(f"  {t:13s}: S0+M3 vs NCS0 {b['dchi2_S0M3_vs_NCS0']:+.2f} -> f {b['f']:.2f} (self-consistent {b['f_selfconsistent']:.2f}); {x} vs S0+M3 {b['dchi2_framework_vs_S0M3']:+.2f} "
              f"(robust " + "/".join(f"{v:+.2f}" for v in b["d_robust"].values()) + f") -> {b['attribution']}; KiDS distinguishes: {b['KiDS_distinguishes']}")
            P("                 f by robustness variant: " + ", ".join(f"{q} {v:.2f}" for q, v in b["f_robust"].items()))
        P("  M12 (alternative attribution): " + "; ".join(f"{t} {v['dchi2_S0M12_vs_NCS0']:+.2f} (f_M12 {v['f_M12']:.2f})" for t, v in A["M12"].items() if isinstance(v, dict)) +
          f"; {x} vs S0+M12 {A['M12']['dchi2_framework_vs_S0M12']:+.2f}; f + f_M12 (primary) {A['M12']['f_sum_primary']:.2f}")
        P(f"  CLASS ({foot}, primary M3-1024): {A['class_primary']}")
    RES["attribution"] = ATT
RES["runtime_s"] = time.time() - T0; RES["peak_rss_gb"] = peak_rss_gb()
P(f"\ndone in {RES['runtime_s']:.0f} s; peak RSS {RES['peak_rss_gb']:.3f} GB")
def _js(o):
    if isinstance(o, dict): return {k: _js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_js(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(_js(RES), open(os.path.join(HERE, f"cfg963_attrib_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg963_attrib{SUF}.out"), "w").write("\n".join(OUT) + "\n")
