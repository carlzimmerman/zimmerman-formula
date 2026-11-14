#!/usr/bin/env python3
"""WLJ2 (FROZEN_CRITERIA.md, c3bc2d3871) part 1: matter-power ratios of REF, ADOPT, S2 (WLJ1's split f 2, the record's junction)
and the exact-junction cases Ec3, Ec2, E0.5, E0.75, E1, E2 at z = 0 to 3, with the twin TW-B (Ec2, boundary 2 v*).
COPY of WLJ1's wlj1_hm.py (closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/) with only the case list, the layout and
the known answers changed. The FZS1 prefix namespace is FWN1R's rec(), reached through XJ1's xj1_lib2.py (imported read-only from
closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface/, bytecode off) after its install() (criteria section 2, item 4).
The exact-junction layout is XJ1's exact_fn formula copied (cited) with WLJ1's lay_case plumbing of the layout options; KA-L proves
the copy equals exact_fn. v* from JNT2's jnt2_common.py (imported read-only).
  OMP_NUM_THREADS=1 nice -n 19 python3 -I -B wlj2_hm.py  -> wlj2_hm.json, wlj2_hm.out, wlj2_hm_MUTATE.json, wlj2_hm_MUTATE.out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
JNT = os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint"); sys.path.insert(0, JNT); import jnt2_common as C  # noqa: E402
XJD = os.path.join(REPO, "closure_2026_11_14", "XJ1_exact_junction_zero_velocity_surface"); sys.path.insert(0, XJD)
WLD = os.path.join(REPO, "closure_2026_11_13", "WLJ1_power_and_lensing_amplitude_with_split")
with contextlib.redirect_stdout(io.StringIO()):
    import xj1_lib2 as XL                                                     # noqa: E402  read-only
    INSTALL_DEV = XL.install()
Z = XL.X.rec()
F, L = Z["F"], Z["L"]; layout, set_z, Bar, rset_com, CUR = (Z[k] for k in ("layout", "set_z", "Bar", "rset_com", "CUR"))
KK, FOOTS, VST = Z["KK"], Z["FOOTS"], Z["VST"]; MM, RHO_M = L["MM"], L["RHO_M"]
assert VST == C.VSTIFF
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
KSEL = (0.1, 0.3, 1.0, 3.0, 10.0)
def at(R, ks=KSEL): return [float(np.interp(k, KK, R)) for k in ks]
CO1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed", "co1_hm.json")))
HLD = os.path.join(REPO, "closure_2026_11_10", "HLF1_own_halo_list_forest")
HAL = json.load(open(os.path.join(HLD, "hlf1_halos.json"))); HOWN = json.load(open(os.path.join(HLD, "hlf1_hm_own.json")))
JNTH = json.load(open(os.path.join(JNT, "jnt2_hm.json")))
W1 = json.load(open(os.path.join(WLD, "wlj1_hm.json")))

# ------------------------------------------------------------------ population (WLJ1's, copied)
def own_factors():
    fw = np.ones_like(MM); fb = np.ones_like(MM)
    for b in HAL["bins"]:
        g = (MM >= b["lo"]) & (MM < b["hi"]); fw[g] = b["r"]
    for b in HAL["bias_bins"]:
        if b["used"]:
            g = (MM >= b["lo"]) & (MM < b["hi"]); fb[g] = b["ratio"]
    return fw, fb
POP = {}
def setz(z, own=False, mf="tinker_z", cfac=1.0):
    set_z(z, mf=mf, cfac=cfac); POP.update(z=z, own=own, mf=mf, cfac=cfac)
    if own:
        assert z == 0.0
        fw, fb = own_factors(); W_M, BIAS = L["W_M"] * fw, L["BIAS"] * fb
        L["W_M"], L["BIAS"] = W_M, BIAS
        L["A_MISS"] = 1.0 - float(np.sum(W_M * BIAS * MM)) / RHO_M
        L["NORM_TA"] = float(np.sum(W_M * BIAS * L["MTA"])) / RHO_M

# ------------------------------------------------------------------ layouts
def OPTR(opt): return {k: v for k, v in opt.items() if k in ("gal_scope", "clu_scope", "rc_fac")}
def lay_split(foot, z, fac, bfac, opt):
    """WLJ1's lay_case (JNT2's lay_J), copied unchanged: the record's junction."""
    optR = OPTR(opt)
    vb = math.inf if math.isinf(bfac) else bfac * C.vstar_kms(foot, z)
    def fn(hb):
        if F["v_vir"](hb) > vb:
            CUR[0] = 0.0; rR, MR, inf = layout(hb, foot, mode="Rb", **optR); return rR, MR, dict(inf, R_set=0.0, split_ref=True)
        R = rset_com(hb, foot, z, fac); CUR[0] = R
        rB, MB, inf = layout(hb, foot, mode="B", **opt); rR, MR, _ = layout(hb, foot, mode="Rb", **optR); CUR[0] = 0.0
        if R <= 0 or inf["regime"] == "L": return rR, MR, dict(inf, R_set=R)
        assert len(rB) == len(rR) and np.array_equal(rB, rR)
        bar = Bar(hb, foot, rB, **optR); CB, CR = MB - bar, MR - bar
        i = int(np.argmin(abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
        s = CR[i] / CB[i]
        return rB, np.where(rB <= rB[i], bar + s * CB, bar + CR), dict(inf, R_set=R, s=float(s))
    return fn
def lay_exact(foot, z, col, mult, bfac, opt, force=None):
    """XJ1's exact_fn (xj1_lib2.py) formula, copied, with WLJ1's option plumbing: inside R_set the law's layout M_B unscaled;
    beyond, Bar + C_B(R_set) + t [C_R - C_R(R_set)], t = [C_tot - C_B(R_set)] / [C_tot - C_R(R_set)]; R_set from XJ1's rsurf_com."""
    optR = OPTR(opt)
    vb = math.inf if math.isinf(bfac) else bfac * C.vstar_kms(foot, z)
    def fn(hb):
        CUR[0] = 0.0
        if F["v_vir"](hb) > vb:
            rR, MR, inf = layout(hb, foot, mode="Rb", **optR); return rR, MR, dict(inf, split_ref=True)
        R = hb["rta"] if force == "rta" else 0.0 if force == "zero" else XL.rsurf_com(hb, foot, z, col, mult)
        if R <= 0:
            rR, MR, inf = layout(hb, foot, mode="Rb", **optR); return rR, MR, dict(inf, R_set=0.0, kind="zero")
        CUR[0] = R
        rB, MB, inf = layout(hb, foot, mode="B", **opt); rR, MR, _ = layout(hb, foot, mode="Rb", **optR); CUR[0] = 0.0
        if inf["regime"] == "L": return rR, MR, dict(inf, kind="L")
        assert np.array_equal(rB, rR)
        bar = Bar(hb, foot, rB, **optR); CB, CR = MB - bar, MR - bar
        i = int(np.argmin(np.abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
        den = CR[-1] - CR[i]
        if den <= 0: return rB, MB, dict(inf, t=1.0, s=1.0, R_set=R, i_set=i, kind="E")
        t = (CR[-1] - CB[i]) / den
        return rB, np.where(rB <= rB[i], MB, bar + CB[i] + t * (CR - CR[i])), dict(inf, t=float(t), s=float(CR[i] / CB[i]), R_set=R, i_set=i, kind="E")
    return fn
CK2, CK3, CF = XL.COL_K[2], XL.COL_K[3], XL.COL_FOLD
CASES = {"ADOPT": ("S", math.inf, math.inf), "S2": ("S", 2.0, 1.0), "ALLREF": ("S", 2.0, 0.0),
         "Ec3": ("E", CK3, 1.0, 1.0), "Ec2": ("E", CK2, 1.0, 1.0), "E0.5": ("E", CF, 0.5, 1.0), "E0.75": ("E", CF, 0.75, 1.0),
         "E1": ("E", CF, 1.0, 1.0), "E2": ("E", CF, 2.0, 1.0), "TWB": ("E", CK2, 1.0, 2.0),
         "E_null0": ("E", CF, 0.0, 1.0), "E_rta_noboundary": ("E", CF, 1.0, math.inf, "rta")}
ECASES = ["Ec3", "Ec2", "E0.5", "E0.75", "E1", "E2"]
def lay_case(foot, z, cs, opt):
    sp = CASES[cs]
    if sp[0] == "S": return lay_split(foot, z, sp[1], sp[2], opt)
    return lay_exact(foot, z, sp[1], sp[2], sp[3], opt, force=(sp[4] if len(sp) > 4 else None))
BASEC = {}
def base(foot, opt):
    key = (foot, POP["z"], POP["own"], POP["mf"], POP["cfac"], tuple(sorted(OPTR(opt).items())))
    if key not in BASEC:
        CUR[0] = 0.0
        Pstd, _, _ = L["spectra_std"](L["U_std"]())
        UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
        UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb", **OPTR(opt))); PR, _, IR = L["spectra_ta"](UR)
        BASEC.clear(); BASEC[key] = dict(Pstd=Pstd, PLta=PLta, PR=PR, UR=UR, IR=IR)
    return BASEC[key]
def ratios_case(foot, z, case, opt=None, keepU=False):
    opt = opt or {}; b = base(foot, opt)
    US, inf = L["U_set"](lay_case(foot, z, case, opt)); PS, _, IS = L["spectra_ta"](US)
    Rtot = 1 + (PS - b["PLta"]) / b["Pstd"]; Rbar = 1 + (b["PR"] - b["PLta"]) / b["Pstd"]
    out = dict(R_tot=Rtot, R_bar=Rbar, R_cold=Rtot / Rbar, n_ref=sum(1 for i in inf if isinstance(i, dict) and i.get("split_ref")), n=len(inf))
    if CASES[case][0] == "E":
        e = [(i, hb) for i, hb in zip(inf, L["HB"]) if isinstance(i, dict) and i.get("kind") == "E"]
        if e:
            tt = [i["t"] for i, _ in e]; ss = [i["s"] for i, _ in e]
            rr = [i["R_set"] / XL.rsurf_com(hb, foot, z, CF, 1.0) for i, hb in e]
            out["info"] = dict(n_settled=len(e), t_min_max=[float(min(tt)), float(max(tt))], s_min_max=[float(min(ss)), float(max(ss))],
                               capped_at_rta=int(sum(1 for i, hb in e if abs(i["R_set"] / hb["rta"] - 1) < 1e-12)),
                               R_set_over_R_fold_min_med_max=[float(np.min(rr)), float(np.median(rr)), float(np.max(rr))],
                               n_zero=int(sum(1 for i in inf if isinstance(i, dict) and i.get("kind") == "zero")))
    if keepU: out.update(US=US, IS=IS, UR=b["UR"], IR=b["IR"])
    return out
def pack(r):
    d = dict(R_tot=r["R_tot"].tolist(), R_bar=r["R_bar"].tolist(), R_cold=r["R_cold"].tolist(), R_cold_at=at(r["R_cold"]), R_tot_at=at(r["R_tot"]), n_ref=r["n_ref"], n=r["n"])
    if "info" in r: d["info"] = r["info"]
    return d
def mrel(a, b): return float(np.max(np.abs(np.asarray(a) / np.asarray(b) - 1)))

RES = dict(lane="WLJ2", part="halo-model ratios", criteria="c3bc2d3871", k=KK.tolist(), KSEL=list(KSEL), cases={}, own={}, brackets={}, KA={}, membership={}, f_res={},
           install_dev=INSTALL_DEV, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
MUT = dict(lane="WLJ2", part="halo-model twins", criteria="c3bc2d3871", TWB={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P("WLJ2 part 1: matter-power ratios with the law exact inside the settled radius. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P(f"XJ1 install(): shell runs' first five columns against FZS1's loaded FLD1 series, max rel {INSTALL_DEV:.1e}")

# ------------------------------------------------------------------ KA-V (v* of JNT2 vs FWN1R) and KA-Z0 (no zero surface at z 0 to 3)
ZALL = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
kav = max(abs(C.vstar_kms(ft, z) / XL.X.vstar(ft, z) - 1) for ft in FOOTS for z in ZALL)
RES["KA"]["KA_V"] = dict(max_rel=kav, pass_=bool(kav <= 1e-12))
z0c = {}
for ft in FOOTS:
    for z in ZALL:
        for col in (CK2, CK3, CF):
            vals = [XL.surf_kpc(ft, z, M, col) for M in Z["MASSES"]]
            z0c[f"{ft}|{z}|{col}"] = int(sum(1 for v in vals if v <= 0))
RES["KA"]["KA_Z0"] = dict(zero_counts={k: v for k, v in z0c.items() if v}, pass_=bool(all(v == 0 for v in z0c.values())))
P(f"KA-V JNT2 vstar_kms vs FWN1R vstar: {kav:.1e} -> {'PASS' if RES['KA']['KA_V']['pass_'] else 'FAIL'}; KA-Z0 zero surfaces at z 0-3: {RES['KA']['KA_Z0']['zero_counts']} -> {'PASS' if RES['KA']['KA_Z0']['pass_'] else 'FAIL'}")
for ft in FOOTS:
    P(f"  [{ft}] surfaces over R_fold at log M_b 10.45 (R_2 / R_3): " + "; ".join(f"z {z}: {XL.surf_kpc(ft, z, 10.45, CK2) / XL.surf_kpc(ft, z, 10.45, CF):.3f} / {XL.surf_kpc(ft, z, 10.45, CK3) / XL.surf_kpc(ft, z, 10.45, CF):.3f}" for z in ZALL))

# ------------------------------------------------------------------ membership (WLJ1's)
for ft in FOOTS:
    m = {}
    for z in ZALL:
        setz(z); vs = C.vstar_kms(ft, z); ab = [hb for hb in L["HB"] if F["v_vir"](hb) > vs]
        Man = (vs * 1e3) ** 3 / (10 * C.G * C.H0 * C.E(z)) / C.MSUN
        m[str(z)] = dict(vstar=vs, M200c_switch_analytic_Msun=Man, M200c_switch_analytic_Msun_h=Man * F["h"], n_above=len(ab), n=len(L["HB"]),
                         lightest_above_M200c_Msun_h=(min(hb["M200c"] for hb in ab) if ab else None))
    RES["membership"][ft] = m
    P(f"[{ft}] v*(z): " + "; ".join(f"z {z}: v* {v['vstar']:.1f} km/s, grid {v['n_above']}/{v['n']} above" for z, v in m.items()))

# ------------------------------------------------------------------ KA-L (copy = XJ1's exact_fn) and KA-E (XJ1's items at this lane's z)
kal = 0.0; kae = {}
EMAP = {"Ec3": (CK3, 1.0), "Ec2": (CK2, 1.0), "E0.5": (CF, 0.5), "E0.75": (CF, 0.75), "E1": (CF, 1.0), "E2": (CF, 2.0)}
for ft in FOOTS:
    for z in ZALL + [2.2]:
        setz(z); vs = C.vstar_kms(ft, z)
        w = dict(i=0.0, ii=0.0, iii=0.0, tmin=math.inf, vi=0.0)
        for cs, (col, mult) in EMAP.items():
            mine = lay_case(ft, z, cs, {}); xj = XL.exact_fn(ft, z, vs, col, mult)
            for hb in L["HB"]:
                r1, M1, i1 = mine(hb); r2, M2, i2 = xj(hb)
                kal = max(kal, float(np.max(np.abs(M1 - M2))) if (len(M1) == len(M2) and np.array_equal(r1, r2)) else math.inf)
                if z not in ZALL: continue
                if F["v_vir"](hb) > vs:
                    CUR[0] = 0.0; rR, MR, _ = layout(hb, ft, mode="Rb"); w["vi"] = max(w["vi"], float(np.max(np.abs(M1 - MR))) if len(M1) == len(MR) else math.inf); continue
                if i1.get("kind") != "E": continue
                CUR[0] = i1["R_set"]; rB, MB, _ = layout(hb, ft, mode="B"); CUR[0] = 0.0; k = i1["i_set"]
                w["i"] = max(w["i"], float(np.max(np.abs(M1[:k + 1] / MB[:k + 1] - 1))))
                w["ii"] = max(w["ii"], abs(M1[-1] / hb["Mta"] - 1)); w["iii"] = max(w["iii"], float(max(0.0, -np.min(np.diff(M1)))) / hb["Mta"])
                w["tmin"] = min(w["tmin"], i1["t"])
        if z in ZALL:
            ok = w["i"] <= 1e-12 and w["ii"] <= 1e-9 and w["iii"] <= 1e-9 and w["tmin"] >= -1e-12 and w["vi"] == 0
            kae[f"{ft}|{z}"] = dict(w, pass_=bool(ok))
RES["KA"]["KA_L"] = dict(max_abs=kal, pass_=bool(kal == 0.0))
RES["KA"]["KA_E"] = dict(rows=kae, pass_=bool(all(v["pass_"] for v in kae.values())))
P(f"KA-L this lane's E layout vs XJ1's exact_fn (z 0-3 and 2.2, every case, halo, footing): max |dM| {kal:.1e} -> {'PASS' if RES['KA']['KA_L']['pass_'] else 'FAIL'}")
P(f"KA-E at z 0-3: " + "; ".join(f"{k}: t_min {v['tmin']:.3f} (i) {v['i']:.0e} (ii) {v['ii']:.0e} (iii) {v['iii']:.0e} (vi) {v['vi']:.0e}" for k, v in kae.items()) + f" -> {'PASS' if RES['KA']['KA_E']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ KA-H1, KA-H2, KA-E0 at z = 0
setz(0.0); ka1 = {}; ka2 = {}; ke0 = {}
for ft in FOOTS:
    a = ratios_case(ft, 0.0, "ADOPT"); pr = CO1["primary"][ft]
    ka1[ft] = dict(R_tot=mrel(a["R_tot"], pr["R_tot"]), R_bar=mrel(a["R_bar"], pr["R_bar"]), R_cold=mrel(a["R_cold"], pr["R_cold"]))
    Rt, Rb, Rc, _ = F["ratios"](ft)
    r0 = ratios_case(ft, 0.0, "ALLREF")
    ka2[ft] = dict(adopt_vs_frz1_ratios=mrel(a["R_tot"], Rt), allref_Rcold_minus_1=float(np.max(np.abs(r0["R_cold"] - 1))))
    n0 = ratios_case(ft, 0.0, "E_null0"); nr = ratios_case(ft, 0.0, "E_rta_noboundary")
    ke0[ft] = dict(null_Rcold_minus_1=float(np.max(np.abs(n0["R_cold"] - 1))), rta_vs_ADOPT=mrel(nr["R_tot"], a["R_tot"]))
RES["KA"]["KA_H1"] = dict(max_rel=ka1, pass_=bool(max(max(v.values()) for v in ka1.values()) <= 1e-8))
RES["KA"]["KA_H2"] = dict(rows=ka2, pass_=bool(max(max(v.values()) for v in ka2.values()) <= 1e-12))
RES["KA"]["KA_E0"] = dict(rows=ke0, pass_=bool(max(max(v.values()) for v in ke0.values()) <= 1e-12))
P(f"KA-H1 ADOPT vs CO1: {ka1} -> {'PASS' if RES['KA']['KA_H1']['pass_'] else 'FAIL'}")
P(f"KA-H2 nulls: {ka2} -> {'PASS' if RES['KA']['KA_H2']['pass_'] else 'FAIL'}")
P(f"KA-E0 (R_set 0 = REF; R_set r_ta, no boundary = ADOPT): {ke0} -> {'PASS' if RES['KA']['KA_E0']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ KA-H3 (JNT2's stored f2 split) and KA-XJ (XJ1's stored matter R_cold and surfaces)
ka3 = {}
for ft in FOOTS:
    for z in (2.2, 4.4):
        setz(z); r = ratios_case(ft, z, "S2"); ka3[f"{ft}|{z}"] = mrel(r["R_cold"], JNTH["cases"][f"f2.00|{ft}"][str(z)]["R_cold"])
RES["KA"]["KA_H3"] = dict(max_rel=ka3, pass_=bool(max(ka3.values()) <= 1e-9))
P(f"KA-H3 S2 vs JNT2's stored R_cold at z 2.2 / 4.4: {ka3} -> {'PASS' if RES['KA']['KA_H3']['pass_'] else 'FAIL'}")
XM = {}
for ft in FOOTS:
    for fn_, names in (("xj1_matter_{}.json", ("E1", "E2")), ("xj1_matter2_{}.json", ("E0.5", "E0.75")), ("xj1_matter3_{}.json", ("Ec2", "Ec3"))):
        d = json.load(open(os.path.join(XJD, fn_.format(ft))))
        for nm in names: XM[(ft, nm)] = d["cases"][nm]["R_cold_at_k1_3_5_10"]
XT = {}
for fn_ in ("xj1_ka_tables.json", "xj1_ka_tables2.json", "xj1_ka_tables3.json"):
    d = json.load(open(os.path.join(XJD, fn_)))
    for key, v in d["surfaces"].items():
        for nm, row in v.items(): XT[(key, nm)] = row
kxm = 0.0; kxs = 0.0
for ft in FOOTS:
    for z in (2.2, 3.0, 4.4):
        setz(z)
        for cs in ECASES:
            r = ratios_case(ft, z, cs)
            mine = [float(np.interp(k, KK, r["R_cold"])) for k in (1.0, 3.0, 5.0, 10.0)]
            kxm = max(kxm, mrel(mine, XM[(ft, cs)][f"{z:.1f}"]))
            st = XT[(f"{ft}|{z}", cs)]; inf = r["info"]
            for a_, b_ in ((inf["t_min_max"], st["t_min_max"]), (inf["s_min_max"], st["s_min_max"]), (inf["R_set_over_R_fold_min_med_max"], st["R_set_over_R_fold_min_med_max"])):
                kxs = max(kxs, float(np.max(np.abs(np.array(a_) - np.array(b_)) / np.maximum(np.abs(np.array(b_)), 1e-300))))
            kxs = max(kxs, 0.0 if inf["n_settled"] == st["n"] else math.inf)
RES["KA"]["KA_XJ"] = dict(matter_Rcold_max_rel=kxm, surfaces_max_rel=kxs, pass_=bool(kxm <= 1e-9 and kxs <= 1e-9))
P(f"KA-XJ XJ1's stored matter R_cold (k 1/3/5/10, z 2.2/3.0/4.4) max rel {kxm:.1e}; surfaces (t, s, R_set/R_fold, n) max rel {kxs:.1e} -> {'PASS' if RES['KA']['KA_XJ']['pass_'] else 'FAIL'}   [{time.time() - T0:.0f} s]")

# ------------------------------------------------------------------ cases at z
CL = ["ADOPT", "S2"] + ECASES + ["TWB"]
for ft in FOOTS:
    for z in ZALL:
        setz(z)
        for cs in CL:
            r = ratios_case(ft, z, cs); (MUT["TWB"] if cs == "TWB" else RES["cases"])[f"{cs}|{ft}|{z}"] = pack(r)
        def g(cs): return (MUT["TWB"] if cs == "TWB" else RES["cases"])[f"{cs}|{ft}|{z}"]
        P(f"  [{ft}] z {z}: R_cold at k 0.1/0.3/1/3/10 " + "; ".join(f"{cs} " + "/".join(f"{x:.5f}" for x in g(cs)["R_cold_at"]) + f" (ref {g(cs)['n_ref']}"
                                                                 + (f", t {g(cs)['info']['t_min_max'][0]:.2f}-{g(cs)['info']['t_min_max'][1]:.2f}, capped {g(cs)['info']['capped_at_rta']}" if "info" in g(cs) else "") + ")" for cs in CL) + f"   [{time.time() - T0:.0f} s]")

# ------------------------------------------------------------------ KA-H4: mass conservation and order (z 0, 0.5, 1; brackets at z 0)
err = 0.0; mono = True
for ft in FOOTS:
    for z in (0.0, 0.5, 1.0):
        setz(z)
        for cs in ["S2"] + ECASES + ["TWB"]:
            for opt in ({}, dict(pre=1.0), dict(pre=0.0), dict(gal_scope="vir"), dict(rc_fac=0.2)):
                if z > 0 and opt: continue
                fn = lay_case(ft, z, cs, opt)
                for hb in L["HB"]:
                    r, Mx, _ = fn(hb); err = max(err, abs(Mx[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(Mx) >= -1e-9 * hb["Mta"]))
RES["KA"]["KA_H4"] = dict(max_rel=err, monotone=mono, pass_=bool(err <= 1e-9 and mono))
P(f"KA-H4 mass conservation / order, every layout (twins and brackets) at z 0, 0.5, 1: {err:.1e}, {mono} -> {'PASS' if RES['KA']['KA_H4']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ HLF1's own list (KA-H5) and f_res (HLF1 A.2, copied as WLJ1)
ka5 = {}; OWNC = ["ADOPT", "S2"] + ECASES
for ft in FOOTS:
    setz(0.0, own=True)
    for cs in OWNC: RES["own"][f"{cs}|{ft}"] = pack(ratios_case(ft, 0.0, cs))
    ka5[ft] = mrel(RES["own"][f"ADOPT|{ft}"]["R_tot"], HOWN["primary"][ft]["R_tot"])
    setz(0.0); MLO, MHI = HAL["M_lo"], HAL["M_hi"]; row = {}
    for cs in OWNC:
        r = ratios_case(ft, 0.0, cs, keepU=True); W_M, BIAS, NORM_TA, PL = (L[k] for k in ("W_M", "BIAS", "NORM_TA", "PL")); rr = {}
        for kk in (1.0, 3.0):
            j = int(np.argmin(abs(KK - kk)))
            d1 = W_M * ((r["US"][:, j] / RHO_M) ** 2 - (r["UR"][:, j] / RHO_M) ** 2)
            d2 = PL[j] * (r["IS"][j] + r["IR"][j]) * W_M * BIAS * (r["US"][:, j] - r["UR"][:, j]) / RHO_M / NORM_TA
            d = np.abs(d1 + d2); g_ = (MM >= MLO) & (MM < MHI); tot = float(d.sum())
            rr[str(kk)] = dict(f_res=float(d[g_].sum() / tot) if tot > 0 else float("nan"), below=float(d[MM < MLO].sum() / tot) if tot > 0 else float("nan"),
                               above=float(d[MM >= MHI].sum() / tot) if tot > 0 else float("nan"))
        row[cs] = rr
    RES["f_res"][ft] = row
    P(f"  [{ft}] own list R_cold k 1/3: " + "; ".join(f"{cs} {RES['own'][f'{cs}|{ft}']['R_cold_at'][2]:.5f}/{RES['own'][f'{cs}|{ft}']['R_cold_at'][3]:.5f}" for cs in OWNC)
      + "; f_res at k 1: " + ", ".join(f"{cs} {v['1.0']['f_res']:.3f}" for cs, v in row.items()) + f"   [{time.time() - T0:.0f} s]")
RES["KA"]["KA_H5"] = dict(max_rel=ka5, pass_=bool(max(ka5.values()) <= 1e-8))
P(f"KA-H5 ADOPT own list vs HLF1: {ka5} -> {'PASS' if RES['KA']['KA_H5']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ CO1's layout brackets at z = 0 (KA-H6)
BR = [("pre_1", dict(pre=1.0), {}), ("pre_0", dict(pre=0.0), {}), ("galaxy_virial_scope", dict(gal_scope="vir"), {}), ("gas_core_0.2", dict(rc_fac=0.2), {}),
      ("press_schechter", {}, dict(mf="ps")), ("conc_x0.7", {}, dict(cfac=0.7)), ("conc_x1.3", {}, dict(cfac=1.3))]
ka6 = {}
for ft in FOOTS:
    for name, opt, pop in BR:
        setz(0.0, **pop)
        for cs in OWNC: RES["brackets"][f"{name}|{cs}|{ft}"] = pack(ratios_case(ft, 0.0, cs, opt))
        e = mrel(RES["brackets"][f"{name}|ADOPT|{ft}"]["R_tot"], CO1["brackets"][ft][name]["R_tot"])
        ka6[f"{name}|{ft}"] = dict(max_rel=e, reproduced=bool(e <= 1e-6))
        P(f"  [{ft}] bracket {name:20s} R_cold k 1 / 3: " + "; ".join(f"{cs} {RES['brackets'][f'{name}|{cs}|{ft}']['R_cold_at'][2]:.5f}/{RES['brackets'][f'{name}|{cs}|{ft}']['R_cold_at'][3]:.5f}"
                                                                    for cs in ("ADOPT", "S2", "Ec2")) + f"; ADOPT vs CO1 {e:.1e} -> {'reproduced' if e <= 1e-6 else 'NOT REPRODUCED'}   [{time.time() - T0:.0f} s]")
RES["KA"]["KA_H6"] = ka6

# ------------------------------------------------------------------ KA-X1: WLJ1's stored arrays reproduced
x1 = 0.0
for ft in FOOTS:
    for z in ZALL:
        for cs in ("ADOPT", "S2"):
            a, b = RES["cases"][f"{cs}|{ft}|{z}"], W1["cases"][f"{cs}|{ft}|{z}"]
            x1 = max(x1, *(mrel(a[k], b[k]) for k in ("R_tot", "R_bar", "R_cold")))
    for cs in ("ADOPT", "S2"):
        a, b = RES["own"][f"{cs}|{ft}"], W1["own"][f"{cs}|{ft}"]; x1 = max(x1, *(mrel(a[k], b[k]) for k in ("R_tot", "R_bar", "R_cold")))
        for name, _, _ in BR:
            a, b = RES["brackets"][f"{name}|{cs}|{ft}"], W1["brackets"][f"{name}|{cs}|{ft}"]; x1 = max(x1, *(mrel(a[k], b[k]) for k in ("R_tot", "R_bar", "R_cold")))
        for kk in ("1.0", "3.0"): x1 = max(x1, abs(RES["f_res"][ft][cs][kk]["f_res"] / W1["f_res"][ft][cs][kk]["f_res"] - 1))
RES["KA"]["KA_X1"] = dict(max_rel=x1, pass_=bool(x1 <= 1e-10))
P(f"KA-X1 REF / ADOPT / S2 (z 0-3, own list, brackets, f_res) vs WLJ1's stored wlj1_hm.json: {x1:.1e} -> {'PASS' if RES['KA']['KA_X1']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ TW-B bite (z = 0), Ec2 in the place of S2
bite = {}
for ft in FOOTS:
    s2, tw = RES["cases"][f"Ec2|{ft}|0.0"], MUT["TWB"][f"TWB|{ft}|0.0"]
    a = abs(tw["R_cold_at"][3] - 1); b = abs(s2["R_cold_at"][3] - 1)
    bite[ft] = dict(n_ref_Ec2=s2["n_ref"], n_ref_TWB=tw["n_ref"], dRcold_k3_Ec2=b, dRcold_k3_TWB=a, bites=bool(tw["n_ref"] < s2["n_ref"] and a >= 1.2 * b))
MUT["TWB_bite"] = dict(rows=bite, bites=bool(all(v["bites"] for v in bite.values())))
P(f"TW-B (boundary 2 v*, at Ec2) at z 0: {bite} -> {'bites' if MUT['TWB_bite']['bites'] else 'DOES NOT BITE'}")

RES["KA_ok"] = bool(all(RES["KA"][k]["pass_"] for k in ("KA_H1", "KA_H2", "KA_H3", "KA_H4", "KA_H5", "KA_V", "KA_L", "KA_E", "KA_E0", "KA_XJ", "KA_X1")))
RES["KA_Z0_ok"] = RES["KA"]["KA_Z0"]["pass_"]
P(f"\nKnown answers (H1-H5, V, L, E, E0, XJ, X1) all pass: {RES['KA_ok']}; KA-Z0: {RES['KA_Z0_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "wlj2_hm.json"), "w"), indent=1)
json.dump(MUT, open(os.path.join(HERE, "wlj2_hm_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "wlj2_hm.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
open(os.path.join(HERE, "wlj2_hm_MUTATE.out"), "w").write("\n".join(l for l in OUT if "TW-B" in l or "TWB" in l) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
P(f"done ({time.time() - T0:.0f} s)")
