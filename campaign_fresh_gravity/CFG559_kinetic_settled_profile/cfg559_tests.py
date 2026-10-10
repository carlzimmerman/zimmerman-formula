#!/usr/bin/env python3
"""CFG559 task 2 (i) growth, (iii) groups, (iv) MW, (v) LG (FROZEN_CRITERIA.md, criteria commit 8485002fc).
ONE change against CFG557's tested runs: the settled profile S_kin(r) = S_sharp(r) + M_set Delta m(r / r_e) (cfg559_lib, toy tables).
Source machinery read-only: CFG556 halo model (exec'd up to its run block), CFG557 frame_profile_sc / group_sc / ShellPair (copied),
CFG543 groups (imported), CFG522 timing (exec'd up to its main block), CFG513 Prof.
  OMP_NUM_THREADS=4 nice -n 10 python3 cfg559_tests.py                -> cfg559_tests.out, cfg559_tests_results.json
  CFG559_MUTATE=1 OMP_NUM_THREADS=4 nice -n 10 python3 cfg559_tests.py  -> *_MUTATE.* (MK0 sigma = 0 reproduces CFG557; MK2 sigma x 2 halo model)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "4")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
D557 = os.path.join(LANES, "CFG557_settling_catchment_derived")
sys.path.insert(0, HERE); sys.path.insert(0, D557)
import cfg559_lib as K9
import cfg557_lib as L

MUTATE = os.environ.get("CFG559_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
try:
    os.nice(10)
except OSError:
    pass
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
FOOTS = ("canonical", "alt")
JD = json.load(open(os.path.join(D557, "cfg557_derive_results.json")))
J557 = json.load(open(os.path.join(D557, "cfg557_tests_results.json")))
assert JD["verdict"]["tested"] == "ff"
res = dict(lane="CFG559", script="cfg559_tests", date="2026-10-10", mutate=MUTATE, criteria_commit="8485002fc",
           settings="kappa = 1/2 FITTED; footings never pooled; nu_mono; candidate B; G9; no EFE; FIX-2 velocity target POSITED (CFG554); cold energy mass required; not theory closed")
P(f"CFG559 tests {'(MUTATE)' if MUTATE else ''} -- FROZEN_CRITERIA.md (8485002fc). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
E0 = L.Epoch(0.0)

# ====================================================================== (i) CFG556 halo model
P556 = os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
_src = open(P556).read(); _cut = _src.index("# ------------------------------------------------------------------ run")
H = {"__file__": P556, "__name__": "cfg556_ro"}
_e = os.environ.pop("CFG556_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "cfg556_ro", "exec"), H)
HB, MTA, KK, U_set, U_std, spectra_ta, spectra_std, s8_of = (H[k] for k in ("HB", "MTA", "KK", "U_set", "U_std", "spectra_ta", "spectra_std", "s8_of"))
M_L, baryon_cum, rgrid, nu_k, fret_of = H["M_L"], H["baryon_cum"], H["rgrid"], H["nu_k"], H["fret_of"]
G, h, FB, A0MPC = H["G"], H["h"], H["FB"], H["A0MPC"]

def frame_profile_sc(hb, foot, sc):
    """CFG557 frame_profile_sc, copied verbatim."""
    r = rgrid(hb, hb["rta"]); Mta = hb["Mta"]; ML = M_L(hb, r)
    f = fret_of(math.log10(Mta))
    if sc <= 0.0:
        return r, ML.copy(), dict(re=0.0, q=0.0, capped=False, fret=f)
    Mb = f * FB * Mta; supply = sc * (1 - FB) * Mta; a0 = A0MPC[foot]
    rM = math.sqrt(G * Mb * h / a0)
    re = rM / math.log1p(f * FB / ((1 - FB) * sc))
    capped = re >= hb["rta"]
    re = min(re, hb["rta"])
    r = np.unique(np.concatenate([r, [re]])); ML = M_L(hb, r)
    mb = baryon_cum(hb, Mb, r, re)
    y = G * mb * h / (np.maximum(r, 1e-30) ** 2 * a0)
    Min = np.where(r > 0, mb * nu_k(y), 0.0)
    iout = np.searchsorted(r, re)
    Mout = Min[iout]; MLout = ML[iout]
    if capped or MLout >= Mta * (1 - 1e-12):
        rem = max(Mta - Min[-1], 0.0)
        MF = Min + rem * ML / Mta; q = 0.0
    else:
        MF = np.where(r <= re, Min, Mout + (Mta - Mout) * (ML - MLout) / (Mta - MLout))
        q = 1.0 - (Mta - Mout) / (Mta - MLout)
    return r, MF, dict(re=re, q=q, capped=capped, fret=f, supply=supply, Mb=Mb, Mout=Mout)

def frame_profile_kin(hb, foot, sc, kind, variant):
    """the ONE change: + M_set Delta m(r / r_e), M_set = settled phantom at the edge = S_sharp(r_e)."""
    r, MF, inf = frame_profile_sc(hb, foot, sc)
    dmf = K9.DM(math.log10(hb["Mta"]), foot, variant, kind)
    if kind == "sharp":
        inf.update(Mset=float("nan"), r99_over_rta=float("nan"), min_dM=float(np.min(np.diff(MF))))
        return r, MF, inf
    Mset = inf["Mout"] - inf["Mb"]
    MFk = MF + Mset * dmf(r / inf["re"])
    inf.update(Mset=Mset, r99_over_rta=min(dmf.r99() * inf["re"], hb["rta"]) / hb["rta"], min_dM_rel=float(np.min(np.diff(MFk)) / hb["Mta"]))
    return r, MFk, inf

Ustd = U_std(); Pstd, _, _ = spectra_std(Ustd)
Ulta, _ = U_set(lambda hb: (lambda r: (r, M_L(hb, r), {}))(rgrid(hb, hb["rta"])))
Plta, _, _ = spectra_ta(Ulta)
W8K = H["_W8"](KK * 8.0) ** 2 * KK ** 2 / (2 * math.pi ** 2)
KSEL = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 2.0]

def hm_case(foot, scs, kind, variant):
    U, infos = U_set(lambda hb, _it=iter(scs): frame_profile_kin(hb, foot, next(_it), kind, variant))
    PF, _, IF = spectra_ta(U)
    R = 1 + (PF - Plta) / Pstd; Rr = PF / Plta
    s8r = math.sqrt(s8_of(Pstd) ** 2 + np.trapz((PF - Plta) * W8K, KK)) / s8_of(Pstd)
    m = (KK >= 0.05) & (KK <= 1.0)
    E, D = float(np.max(R[m] - 1)), float(np.min(R[m] - 1)); mx = max(abs(E), abs(D))
    o = dict(R=R.tolist(), E=E, D=D, maxdev=mx, kE=float(KK[m][np.argmax(R[m])]), E_ratio=float(np.max(Rr[m] - 1)), s8_ratio=s8r,
             R_at={str(k): float(np.interp(k, KK, R)) for k in KSEL}, passed=bool(mx <= 0.10 and abs(s8r - 1) <= 0.05))
    lt = np.log10(MTA)
    o["re_over_rta_at"] = {str(l): float(np.interp(l, lt, [i["re"] / hb["rta"] for i, hb in zip(infos, HB)])) for l in (12, 13, 14, 15)}
    if kind != "sharp":
        o["r99_over_rta_at"] = {str(l): float(np.interp(l, lt, [i["r99_over_rta"] for i in infos])) for l in (12, 13, 14, 15)}
        o["min_dM_rel"] = float(min(i["min_dM_rel"] for i in infos))
    j = int(np.argmin(abs(KK - 1.0))); W_M, BIAS, RHO_M, NORM_TA, PL = H["W_M"], H["BIAS"], H["RHO_M"], H["NORM_TA"], H["PL"]
    _, _, Il = spectra_ta(Ulta)
    d1 = W_M * ((U[:, j] / RHO_M) ** 2 - (Ulta[:, j] / RHO_M) ** 2)
    d2 = PL[j] * (IF[j] + Il[j]) * W_M * BIAS * (U[:, j] - Ulta[:, j]) / RHO_M / NORM_TA
    o["drivers_k1"] = {f"{lo}-{lo + 1}": float((d1 + d2)[(lt >= lo) & (lt < lo + 1)].sum() / Pstd[j]) for lo in range(10, 16)}
    pr = {}
    for l in (12, 13, 14, 15):
        i = int(np.argmin(abs(lt - l))); hb = HB[i]
        r, Mc, inf = frame_profile_kin(hb, foot, scs[i], kind, variant)
        pr[str(l)] = {str(x): float(np.interp(x * hb["rta"], r, Mc) / M_L(hb, x * hb["rta"])) for x in (0.05, 0.1, 0.2, 0.3, 0.5)}
    o["profile_ratios"] = pr
    return o

res["halo_model"] = {}
SC_PRIM = {ft: JD["grid"][ft]["ff"] for ft in FOOTS}
if not MUTATE:
    P("\n(i) CFG556 halo model, settled supply x s_c* (CFG557 ceiling) + kinetic redistribution.  PASS iff max|R-1| <= 0.10 (k 0.05-1) AND |s8 ratio - 1| <= 0.05")
    for ft in FOOTS:
        res["halo_model"][ft] = {}
        for nm, scs, kind, var in (("PRIMARY_kin", SC_PRIM[ft], "kin", "primary"), ("VARIANT_full_kin", [1.0] * len(HB), "kin", "full")):
            o = hm_case(ft, scs, kind, var); res["halo_model"][ft][nm] = o
            ref = J557["halo_model"][ft]["TESTED"] if nm.startswith("PRIMARY") else J557["halo_model"][ft]["context_turnaround_sc1"]
            o["E_sharp"] = ref["E"]; o["s8_sharp"] = ref["s8_ratio"]
            tag = ("PASS" if o["passed"] else "FAIL") if nm.startswith("PRIMARY") else "(variant, reported)"
            P(f"  [{ft:9s}] {nm:17s} E {o['E']:+.3f} (k {o['kE']:.2f}; sharp {ref['E']:+.3f})  D {o['D']:+.3f}  ratio-form {o['E_ratio']:+.3f}  s8 ratio {o['s8_ratio']:.4f} (sharp {ref['s8_ratio']:.4f}) -> {tag}")
            P("        R(k): " + "  ".join(f"{k}:{v:.3f}" for k, v in o["R_at"].items()) + " | k=1 drivers: " + " ".join(f"{d}:{v:+.3f}" for d, v in o["drivers_k1"].items() if abs(v) > 5e-4))
            P("        r_e/r_ta 12/13/14/15: " + "/".join(f"{o['re_over_rta_at'][str(l)]:.3f}" for l in (12, 13, 14, 15)) + "; kinetic r_99/r_ta: "
              + "/".join(f"{o['r99_over_rta_at'][str(l)]:.3f}" for l in (12, 13, 14, 15)) + f"; min dM/M_ta {o['min_dM_rel']:.1e}")
            for l, v in o["profile_ratios"].items():
                P(f"        M_F/M_L logM_ta {l}: " + " ".join(f"{x}:{v[x]:.3f}" for x in ("0.05", "0.1", "0.2", "0.3", "0.5")))
else:
    P("\nMK0 (sigma = 0 => Delta m = 0) halo model vs CFG557 TESTED; MK2 (sigma x 2) halo model vs sigma x 1")
    J1 = json.load(open(os.path.join(HERE, "cfg559_tests_results.json")))
    tm = {}
    for ft in FOOTS:
        o0 = hm_case(ft, SC_PRIM[ft], "sharp", "primary"); ref = J557["halo_model"][ft]["TESTED"]
        dR = float(np.max(np.abs(np.array(o0["R"]) - np.array(ref["R"])))); ds8 = abs(o0["s8_ratio"] - ref["s8_ratio"])
        o2 = hm_case(ft, SC_PRIM[ft], "kin2", "primary"); E1 = J1["halo_model"][ft]["PRIMARY_kin"]["E"]
        tm[ft] = dict(MK0_maxdR=dR, MK0_ds8=ds8, MK0_bites=dR <= 1e-10 and ds8 <= 1e-10, MK2_E=o2["E"], MK2_D=o2["D"], MK2_s8=o2["s8_ratio"],
                      MK2_R_at=o2["R_at"], MK2_r99_over_rta_at=o2["r99_over_rta_at"], E_sigma1=E1, MK2_E_lower=o2["E"] < E1,
                      MK2_overshoots_growth=bool(o2["R_at"]["1.0"] < 0.90), MK2_profile_ratios=o2["profile_ratios"])
        P(f"  [{ft}] MK0: max|dR| {dR:.1e}, |ds8| {ds8:.1e} -> {'BITES' if tm[ft]['MK0_bites'] else 'FAILS'};  MK2: E {o2['E']:+.3f} D {o2['D']:+.3f} (sigma x1 E {E1:+.3f}) "
          f"R(1) {o2['R_at']['1.0']:.3f}, s8 {o2['s8_ratio']:.4f}; r_99/r_ta 12-15 " + "/".join(f"{o2['r99_over_rta_at'][str(l)]:.3f}" for l in (12, 13, 14, 15))
          + f" -> E lower: {tm[ft]['MK2_E_lower']}")
    res["teeth_halo_model"] = tm

# ====================================================================== (iii) CFG543 P2 groups
sys.path.insert(0, os.path.join(LANES, "CFG543_group_supply"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg543_group_supply as M43                                                     # noqa: E402
M43.GEO = M43.gas_geometry(M43.lovisari())
ROWS = M43.read_groups()
J43 = json.load(open(os.path.join(LANES, "CFG543_group_supply", "cfg543_results.json")))
FMAP = {"can": "canonical", "alt": "alt"}

def group_lMta(o):
    return math.log10(10 ** o["lM"] / (0.10 * L.FB) * L.h)

def group_sc(o, foot):
    Mb = 10 ** o["lM"]
    return L.s_catch(E0, Mb / (0.10 * L.FB) * L.h, Mb * L.h, foot, math.inf)

def sigma_log_kin(o, a0, cfg, dlM=0.0, smult=1.0, dmf=None):
    """CFG543 sigma_log (P2 path, no newton / bound), copied, with ONE change: g += G M_set Delta m(r / r_e) / r^2 (M_set = mph at the edge)."""
    lM = o["lM"] + dlM
    M, Mhot, Msup, _ = M43.config_masses(lM, cfg)
    Msup *= smult
    Re = o["Re"] / cfg.get("k", 1.0)
    a = Re * M43.KPC / M43.HERN_RE
    X = M43.X; r = X * a
    Mb = M * M43.M_T
    if Mhot > 0:
        Rt_f = cfg.get("Rt", 1.0); rc_f = M43.GEO["rc_over_R500"]
        if Rt_f == 1.0:
            R5 = M43.R500_of(Mhot)
        else:
            frac = M43.beta_shape(1.0, rc_f) / M43.beta_shape(Rt_f, rc_f); R5 = M43.R500_of(Mhot * frac)
        rc = rc_f * R5 * M43.KPC; Rt = Rt_f * R5 * M43.KPC
        Mg = Mhot * M43.beta_shape(np.minimum(r, Rt), rc) / M43.beta_shape(Rt, rc)
        Mb = Mb + Mg
    gN = M43.G * Mb * M43.MSUN / r ** 2
    nu = M43.C.nu(gN / a0)
    g = nu * gN
    if cfg.get("edge", True):
        mph = (nu - 1.0) * Mb
        k = np.where(mph >= Msup)[0]
        if len(k):
            xe = k[0]
            g = np.where(np.arange(len(X)) > xe, M43.G * (Mb + mph[xe]) * M43.MSUN / r ** 2, g)
            if dmf is not None and dmf.kind != "sharp":
                g = g + M43.G * mph[xe] * dmf(r / r[xe]) * M43.MSUN / r ** 2
    s2 = np.trapezoid(4 * np.pi * X ** 2 * M43.RHO_T * r * g * X, M43.LX) / 3.0
    return 0.5 * math.log10(s2) - 3.0

def run_groups(a0, scs, dmfs, cfg=dict(kind="P2")):
    lp = np.array([sigma_log_kin(o, a0, cfg, 0.0, s, d) for o, s, d in zip(ROWS, scs, dmfs)])
    lp2 = np.array([sigma_log_kin(o, a0, cfg, 0.01, s, d) for o, s, d in zip(ROWS, scs, dmfs)])
    D = np.array([o["ls"] for o in ROWS]) - lp
    return M43.stats(D, (lp2 - lp) / 0.01)

res["groups"] = {}
for fk, a0 in M43.FOOT.items():
    ft = FMAP[fk]
    scs = np.array([group_sc(o, ft) for o in ROWS])
    if not MUTATE:
        dk = [K9.DM(group_lMta(o), ft, "primary", "kin") for o in ROWS]
        st = run_groups(a0, scs, dk)
        dkf = [K9.DM(group_lMta(o), ft, "full", "kin") for o in ROWS]
        stf = run_groups(a0, np.ones(len(ROWS)), dkf)
        ref = J557["groups"][ft]["TESTED"]
        res["groups"][ft] = dict(PRIMARY_kin=st, sharp=ref, VARIANT_full_kin=stf, cfg543_P2_full_sharp=J43["footings"][fk]["configs"]["P2"]["mean"],
                                 sc_median=float(np.median(scs)), log10_Mta_range=[min(group_lMta(o) for o in ROWS), max(group_lMta(o) for o in ROWS)],
                                 passed=bool(abs(st["Z"]) < 2))
        if ft == "canonical":
            P("\n(iii) CFG543 P2 groups, supply x s_c* + kinetic redistribution; PASS iff |Z| < 2")
        P(f"  [{ft:9s}] P2 kin: mean {st['mean']:+.4f} Z {st['Z']:+.2f} (sharp {ref['mean']:+.4f} Z {ref['Z']:+.2f}) -> {'PASS' if abs(st['Z']) < 2 else 'FAIL'};  "
          f"variant full supply kin: {stf['mean']:+.4f} Z {stf['Z']:+.2f} (CFG543 sharp {J43['footings'][fk]['configs']['P2']['mean']:+.4f})")
    else:
        st0 = run_groups(a0, scs, [K9.DM(0, ft, "primary", "sharp") for _ in ROWS]); ref = J557["groups"][ft]["TESTED"]["mean"]
        res.setdefault("teeth_groups", {})[ft] = dict(MK0_mean=st0["mean"], ref=ref, MK0_bites=abs(st0["mean"] - ref) <= 1e-6)
        P(f"  [{ft}] MK0 groups sigma=0: {st0['mean']:+.6f} vs CFG557 {ref:+.6f} -> {'BITES' if abs(st0['mean'] - ref) <= 1e-6 else 'FAILS'}")

# ====================================================================== (v)+(iv) CFG522 machinery
P522 = os.path.join(LANES, "CFG522_local_group_timing", "cfg522_lg_timing.py")
_src = open(P522).read()
_mk = "fM, f31 = L.fret_census(MB_PRIM)[0], L.fret_census(MB_M31)[0]"
assert _src.count(_mk) == 1
KN = {"__file__": P522, "__name__": "cfg522_ro"}
_e = os.environ.pop("CFG522_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_src.index(_mk)], "cfg522_ro", "exec"), KN)
Pair, full_stats, Prof, L15 = KN["Pair"], KN["full_stats"], KN["Prof"], KN["L"]
MB_PRIM, MB_M31, D_LG, COLD = KN["MB_PRIM"], KN["MB_M31"], KN["D_LG"], KN["COLD"]
H16 = L15.H16
fLG = L15.fret_census(MB_PRIM + MB_M31)[0]
LM200 = np.array(JD["grid"]["canonical"]["log10_M200m"]); LMTA = np.array(JD["grid"]["canonical"]["log10_Mta"])
halo_basics = H["halo_basics"]
GKPC = 4.30091727e-6

def sc_obj(Mta_h, Mb_h, foot):
    return L.s_catch(E0, Mta_h, Mb_h, foot, math.inf)

class ShellPair:
    """CFG557 ShellPair copied (M1 shared catchment, settled supply x s_i, unsettled drained shell), + ONE change:
    each galaxy's settled cold mass M_set,i Delta m(d / r_e,i) added to the pair's cold-mass table."""
    def __init__(self, foot, s_mw, s_m31, shell=True, kind="kin", variant="primary"):
        self.p = Pair(foot, MB_PRIM, fLG / s_mw if s_mw > 0 else 1e30, MB_M31, fLG / s_m31 if s_m31 > 0 else 1e30)
        d = 10 ** self.p.ld
        self.extra = np.zeros_like(d); self.kin = np.zeros_like(d); self.info = {}
        for nm, prof, Mb, s in (("mw", self.p.mw, MB_PRIM, s_mw), ("m31", self.p.m31, MB_M31, s_m31)):
            Mbt = prof.Mb_tot(); Mta_h = Mbt * H16 / (fLG * L.FB)
            hb = halo_basics(10 ** float(np.interp(math.log10(Mta_h), LMTA, LM200)))
            U = (1 - s) * COLD * Mbt / fLG
            re_h = prof.redge / 1000.0 * L.h; rta_kpc = hb["rta"] / L.h * 1000.0
            dh = d / 1000.0 * L.h
            MLd = M_L(hb, np.minimum(dh, hb["rta"])); MLe = float(M_L(hb, min(re_h, hb["rta"])))
            frac = np.clip((MLd - MLe) / (hb["Mta"] - MLe), 0.0, 1.0) if re_h < hb["rta"] else np.zeros_like(d)
            self.extra += U * frac if shell else 0 * frac
            dmf = K9.DM(math.log10(Mta_h), foot, variant, kind)
            self.kin += prof.Mcold * dmf(d / prof.redge)
            self.info[nm] = dict(s=s, U=U, edge_kpc=prof.redge, rta_kpc=rta_kpc, log10_Mta_h=math.log10(Mta_h),
                                 r99_kpc=(dmf.r99() * prof.redge if kind != "sharp" else prof.redge))
        self.p.Mc_sc = self.p.Mc_sc + self.extra + self.kin
        self.p.M1 = self.p.mw.Mb_tot() + COLD * self.p.mw.Mb_tot() / fLG
        self.p.M2 = self.p.m31.Mb_tot() + COLD * self.p.m31.Mb_tot() / fLG

res["mw"] = {}; res["lg"] = {}
fM, lMta_mw = L15.fret_census(MB_PRIM)
J553 = json.load(open(os.path.join(LANES, "CFG553_sealed_gaia_dr4_predictions", "cfg553_predictions.json")))
for ft in FOOTS:
    s = sc_obj(10 ** lMta_mw, MB_PRIM * H16, ft)
    pr = Prof("mw", Mb=MB_PRIM, foot=ft, fret=fM / s)
    if MUTATE:
        pr0 = Prof("mw", Mb=MB_PRIM, foot=ft, fret=fM / s); ref = J557["mw"][ft]["edge_new_kpc"]
        res.setdefault("teeth_mw", {})[ft] = dict(edge=pr0.redge, ref=ref, MK0_bites=abs(pr0.redge / ref - 1) <= 1e-9)
        P(f"  [{ft}] MK0 MW edge {pr0.redge:.6f} vs CFG557 {ref:.6f} -> {'BITES' if abs(pr0.redge / ref - 1) <= 1e-9 else 'FAILS'}")
        continue
    dmf = K9.DM(lMta_mw, ft, "primary", "kin")
    rows = {}
    for rk in (8.2, 16.0, 20.0, 30.0, 60.0):
        x = rk / pr.redge; dM = pr.Mcold * float(dmf(np.array([x]))[0]); M = float(pr.M_enc(np.array([rk]))[0])
        mk = float(dmf.m_kin(np.array([x]))[0]); eM = pr.Mcold * math.sqrt(max(mk * (1 - mk), 0) / 30000)
        V = math.sqrt(GKPC * M / rk); dV = math.sqrt(GKPC * max(M + dM, 0) / rk) - V; eV = 0.5 * V * eM / M
        rows[str(rk)] = dict(x=x, dM=dM, dM_over_M=dM / M, sigma_dM=eM, V=V, dV=dV, sigma_dV=eV)
    r1, r2 = 6.0, 10.5
    sh = pr.Mcold * float(dmf(np.array([r2 / pr.redge]))[0] - dmf(np.array([r1 / pr.redge]))[0])
    mk1, mk2 = (float(dmf.m_kin(np.array([v / pr.redge]))[0]) for v in (r1, r2))
    esh = pr.Mcold * math.sqrt(max(mk2 - mk1, 0) / 30000)
    vol = 4 / 3 * math.pi * (r2 ** 3 - r1 ** 3) * 1e9                                         # pc^3
    dSig = 2 * 1100.0 * sh / vol; eSig = 2 * 1100.0 * esh / vol
    passed = all(abs(rows[str(rk)]["dV"]) <= 5.4 for rk in (8.2, 16.0, 20.0, 30.0)) and abs(dSig) <= 5.8
    res["mw"][ft] = dict(sc=s, edge_kpc=pr.redge, Mcold=pr.Mcold, r99_kpc=dmf.r99() * pr.redge, log10_Mta_h=lMta_mw, rows=rows,
                         dSigma_dark_R0=dSig, sigma_dSigma=eSig, passed=bool(passed))
    if ft == "canonical":
        P("\n(iv) MW inside 30 kpc (CFG513 Prof, s_c*), kinetic redistribution; PASS iff |dV_c| <= 5.4 km/s at r <= 30 kpc AND |dSigma_dark(R0, 1.1)| <= 5.8 Msun/pc^2 (CFG553 band half-widths)")
    P(f"  [{ft:9s}] edge {pr.redge:.0f} kpc, kinetic r_99 {dmf.r99() * pr.redge:.0f} kpc; " + "; ".join(
        f"{k} kpc: dM/M {v['dM_over_M']:+.4f} dV {v['dV']:+.2f}+-{v['sigma_dV']:.2f} km/s" for k, v in rows.items())
      + f"; dSigma_dark(R0) {dSig:+.2f}+-{eSig:.2f} Msun/pc^2 -> {'PASS' if passed else 'FAIL'}")

if not MUTATE:
    P("\n(v) LG timing (CFG522 M1 + CFG557 shell) with the kinetic redistribution; PASS iff |z_full| < 2")
for ft in FOOTS:
    Mbt_mw = Prof("mw", Mb=MB_PRIM, foot=ft, fret=fLG).Mb_tot()
    s_mw = sc_obj(Mbt_mw * H16 / (fLG * L.FB), Mbt_mw * H16, ft)
    s_31 = sc_obj(MB_M31 * H16 / (fLG * L.FB), MB_M31 * H16, ft)
    if MUTATE:
        sp = ShellPair(ft, s_mw, s_31, shell=True, kind="sharp")
        with contextlib.redirect_stdout(io.StringIO()):
            fs = full_stats(sp.p, "MK0")
        ref = J557["lg"][ft]["TESTED"]["z_full"]
        res.setdefault("teeth_lg", {})[ft] = dict(z_full=fs["z_full"], ref=ref, MK0_bites=abs(fs["z_full"] - ref) <= 1e-6)
        P(f"  [{ft}] MK0 LG z_full {fs['z_full']:+.6f} vs CFG557 {ref:+.6f} -> {'BITES' if abs(fs['z_full'] - ref) <= 1e-6 else 'FAILS'}")
        continue
    out = {}
    for nm, args in (("PRIMARY_kin", (s_mw, s_31, True, "kin", "primary")), ("VARIANT_full_kin", (1.0, 1.0, False, "kin", "full"))):
        sp = ShellPair(ft, *args)
        with contextlib.redirect_stdout(io.StringIO()):
            fs = full_stats(sp.p, nm)
        out[nm] = dict(z_meas=fs["z_meas"], z_full=fs["z_full"], z_full_LMC=fs["z_full_LMC"], sigma_full=fs["sigma_full"], Meff_780=sp.p.Meff(D_LG),
                       edges=[sp.info["mw"]["edge_kpc"], sp.info["m31"]["edge_kpc"]], r99=[sp.info["mw"]["r99_kpc"], sp.info["m31"]["r99_kpc"]])
    ref = J557["lg"][ft]["TESTED"]
    out["sharp"] = dict(z_meas=ref["z_meas"], z_full=ref["z_full"], Meff_780=ref["Meff_780"])
    out["passed"] = bool(abs(out["PRIMARY_kin"]["z_full"]) < 2)
    res["lg"][ft] = out
    t = out["PRIMARY_kin"]; v = out["VARIANT_full_kin"]
    P(f"  [{ft:9s}] edges {t['edges'][0]:.0f}/{t['edges'][1]:.0f} kpc -> kinetic r_99 {t['r99'][0]:.0f}/{t['r99'][1]:.0f} kpc; M_eff(780) {t['Meff_780']:.3e} (sharp {ref['Meff_780']:.3e}); "
          f"z_meas {t['z_meas']:+.2f} (sharp {ref['z_meas']:+.2f}); z_full {t['z_full']:+.2f} (sharp {ref['z_full']:+.2f}) -> {'PASS' if out['passed'] else 'FAIL'};  "
          f"variant full supply kin: z_full {v['z_full']:+.2f}")

if MUTATE:
    allb = all(v["MK0_bites"] for v in res["teeth_halo_model"].values()) and all(v["MK0_bites"] for v in res["teeth_groups"].values()) \
        and all(v["MK0_bites"] for v in res["teeth_mw"].values()) and all(v["MK0_bites"] for v in res["teeth_lg"].values()) \
        and all(v["MK2_E_lower"] for v in res["teeth_halo_model"].values())
    res["all_teeth_bite_tests"] = bool(allb)
    P(f"\nMUTATE (tests part): MK0 all reproduce CFG557 and MK2 lowers E on both footings -> {allb}")
json.dump(res, open(os.path.join(HERE, f"cfg559_tests_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg559_tests{SUF}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE:
    sys.exit(1 if res["all_teeth_bite_tests"] else 0)
