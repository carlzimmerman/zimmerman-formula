#!/usr/bin/env python3
"""WLJ1 (FROZEN_CRITERIA.md, 03f9823de7) part 1: the matter-power ratios of the three cases (REF, ADOPT, SPLIT at f) at z = 0 to 3.
FZS1's fzs1_hm.py is executed read-only from its own path up to its "checkpointed run" marker (it executes FRZ1's frz1_hm.py library:
CFG556's halo model at z, CO1's layout made z-aware, FLD1's R_fold), exactly as JNT2's jnt2_hm.py does. The split layout is JNT2's
lay_J (copied, cited) with the boundary multiplier as an argument; v* from JNT2's jnt2_common.py (imported read-only, no bytecode).
Spectra: R_tot = 1 + (P_case - P_Lta) / P_std, R_bar = 1 + (P_Rb - P_Lta) / P_std, R_cold = R_tot / R_bar.
  Known answers KA-H1 to KA-H6; twin TW-B (boundary 2 v*) -> wlj1_hm_MUTATE.json; HLF1's own list; f_res (HLF1 A.2, copied).
  nice -n 10 python3 -I -B wlj1_hm.py  -> wlj1_hm.json, wlj1_hm.out, wlj1_hm_MUTATE.json, wlj1_hm_MUTATE.out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
JNT = os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint"); sys.path.insert(0, JNT); import jnt2_common as C  # noqa: E402
FZD = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius")
SRC = os.path.join(FZD, "fzs1_hm.py"); code = open(SRC).read()
cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
Z = {"__file__": SRC, "__name__": "fzs1_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), Z)
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

# ------------------------------------------------------------------ population: FRZ1's set_z, plus HLF1's own list (own_factors copied, LIST = "own")
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

# ------------------------------------------------------------------ the case layout (JNT2's lay_J, copied; boundary multiplier bfac)
def OPTR(opt): return {k: v for k, v in opt.items() if k in ("gal_scope", "clu_scope", "rc_fac")}
def lay_case(foot, z, fac, bfac, opt):
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
CASES = {"ADOPT": (math.inf, math.inf), "S1.25": (1.25, 1.0), "S2": (2.0, 1.0), "S3": (3.0, 1.0), "Sinf": (math.inf, 1.0),
         "U1.25": (1.25, math.inf), "U2": (2.0, math.inf), "U3": (3.0, math.inf), "TWB": (2.0, 2.0), "ALLREF": (2.0, 0.0)}
def ratios_case(foot, z, case, opt=None, keepU=False):
    opt = opt or {}; fac, bfac = CASES[case]; b = base(foot, opt)
    US, inf = L["U_set"](lay_case(foot, z, fac, bfac, opt)); PS, _, IS = L["spectra_ta"](US)
    Rtot = 1 + (PS - b["PLta"]) / b["Pstd"]; Rbar = 1 + (b["PR"] - b["PLta"]) / b["Pstd"]
    out = dict(R_tot=Rtot, R_bar=Rbar, R_cold=Rtot / Rbar, n_ref=sum(1 for i in inf if i.get("split_ref")), n=len(inf))
    if keepU: out.update(US=US, IS=IS, UR=b["UR"], IR=b["IR"])
    return out
def pack(r): return dict(R_tot=r["R_tot"].tolist(), R_bar=r["R_bar"].tolist(), R_cold=r["R_cold"].tolist(), R_cold_at=at(r["R_cold"]), R_tot_at=at(r["R_tot"]),
                         n_ref=r["n_ref"], n=r["n"])
def mrel(a, b): return float(np.max(np.abs(np.asarray(a) / np.asarray(b) - 1)))

RES = dict(lane="WLJ1", part="halo-model ratios", criteria="03f9823de7", k=KK.tolist(), KSEL=list(KSEL), cases={}, own={}, brackets={}, KA={}, membership={}, f_res={},
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
MUT = dict(lane="WLJ1", part="halo-model twins", criteria="03f9823de7", TWB={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P("WLJ1 part 1: matter-power ratios with the crossing-speed split. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

# ------------------------------------------------------------------ membership: v*(z), switch mass
ZALL = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
for ft in FOOTS:
    m = {}
    for z in ZALL:
        setz(z); vs = C.vstar_kms(ft, z); ab = [hb for hb in L["HB"] if F["v_vir"](hb) > vs]
        Man = (vs * 1e3) ** 3 / (10 * C.G * C.H0 * C.E(z)) / C.MSUN
        m[str(z)] = dict(vstar=vs, M200c_switch_analytic_Msun=Man, M200c_switch_analytic_Msun_h=Man * F["h"], n_above=len(ab), n=len(L["HB"]),
                         lightest_above_M200c_Msun_h=(min(hb["M200c"] for hb in ab) if ab else None))
    RES["membership"][ft] = m
    P(f"[{ft}] v*(z) and the switch: " + "; ".join(f"z {z}: v* {v['vstar']:.1f} km/s, M200c {v['M200c_switch_analytic_Msun']:.2e} Msun ({v['M200c_switch_analytic_Msun_h']:.2e} Msun/h), "
                                                 f"grid {v['n_above']}/{v['n']} above (lightest {v['lightest_above_M200c_Msun_h'] or float('nan'):.2e} Msun/h)" for z, v in m.items()))

# ------------------------------------------------------------------ KA-H1, KA-H2 at z = 0
setz(0.0); ka1 = {}; ka2 = {}
for ft in FOOTS:
    a = ratios_case(ft, 0.0, "ADOPT"); pr = CO1["primary"][ft]
    ka1[ft] = dict(R_tot=mrel(a["R_tot"], pr["R_tot"]), R_bar=mrel(a["R_bar"], pr["R_bar"]), R_cold=mrel(a["R_cold"], pr["R_cold"]))
    Rt, Rb, Rc, _ = F["ratios"](ft)
    r0 = ratios_case(ft, 0.0, "ALLREF")
    ka2[ft] = dict(adopt_vs_frz1_ratios=mrel(a["R_tot"], Rt), allref_Rcold_minus_1=float(np.max(np.abs(r0["R_cold"] - 1))))
RES["KA"]["KA_H1"] = dict(max_rel=ka1, pass_=bool(max(max(v.values()) for v in ka1.values()) <= 1e-8))
RES["KA"]["KA_H2"] = dict(rows=ka2, pass_=bool(max(max(v.values()) for v in ka2.values()) <= 1e-12))
P(f"KA-H1 ADOPT at z 0 against CO1's stored primary: {ka1} -> {'PASS' if RES['KA']['KA_H1']['pass_'] else 'FAIL'}")
P(f"KA-H2 nulls (no boundary, f inf = FRZ1's ratios; every halo above = REF): {ka2} -> {'PASS' if RES['KA']['KA_H2']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ KA-H3: JNT2's stored f2 split at z 2.2 / 4.4
ka3 = {}
for ft in FOOTS:
    for z in (2.2, 4.4):
        setz(z); r = ratios_case(ft, z, "S2"); ka3[f"{ft}|{z}"] = mrel(r["R_cold"], JNTH["cases"][f"f2.00|{ft}"][str(z)]["R_cold"])
RES["KA"]["KA_H3"] = dict(max_rel=ka3, pass_=bool(max(ka3.values()) <= 1e-9))
P(f"KA-H3 SPLIT f 2 against JNT2's stored R_cold at z 2.2 / 4.4: {ka3} -> {'PASS' if RES['KA']['KA_H3']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ cases at z
ZCASES = {0.0: ["ADOPT", "S1.25", "S2", "S3", "Sinf", "U1.25", "U2", "U3", "TWB"], 0.5: ["ADOPT", "S1.25", "S2", "S3", "Sinf", "U1.25", "U2", "U3", "TWB"],
          1.0: ["ADOPT", "S1.25", "S2", "S3", "Sinf", "U1.25", "U2", "U3", "TWB"]}
for z in (1.5, 2.0, 2.5, 3.0): ZCASES[z] = ["ADOPT", "S1.25", "S2", "S3", "Sinf", "TWB"]
for ft in FOOTS:
    for z, cl in ZCASES.items():
        setz(z)
        for cs in cl:
            r = ratios_case(ft, z, cs); (MUT["TWB"] if cs == "TWB" else RES["cases"])[f"{cs}|{ft}|{z}"] = pack(r)
        P(f"  [{ft}] z {z}: R_cold at k 0.1/0.3/1/3/10 " + "; ".join(f"{cs} " + "/".join(f"{x:.5f}" for x in (MUT['TWB'] if cs == 'TWB' else RES['cases'])[f'{cs}|{ft}|{z}']['R_cold_at'])
                                                                  + f" (ref haloes {(MUT['TWB'] if cs == 'TWB' else RES['cases'])[f'{cs}|{ft}|{z}']['n_ref']})" for cs in cl) + f"   [{time.time() - T0:.0f} s]")

# ------------------------------------------------------------------ KA-H4: mass conservation and order (z 0, 0.5, 1)
err = 0.0; mono = True
for ft in FOOTS:
    for z in (0.0, 0.5, 1.0):
        setz(z)
        for cs in ("S1.25", "S2", "S3", "Sinf", "TWB"):
            fac, bfac = CASES[cs]
            for opt in ({}, dict(pre=1.0), dict(pre=0.0), dict(gal_scope="vir"), dict(rc_fac=0.2)):
                if z > 0 and opt: continue
                fn = lay_case(ft, z, fac, bfac, opt)
                for hb in L["HB"]:
                    r, Mx, _ = fn(hb); err = max(err, abs(Mx[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(Mx) >= -1e-9 * hb["Mta"]))
RES["KA"]["KA_H4"] = dict(max_rel=err, monotone=mono, pass_=bool(err <= 1e-9 and mono))
P(f"KA-H4 mass conservation / order, every split, twin and bracket layout at z 0, 0.5, 1: {err:.1e}, {mono} -> {'PASS' if RES['KA']['KA_H4']['pass_'] else 'FAIL'}")

# ------------------------------------------------------------------ HLF1's own list at z = 0 (KA-H5) and f_res (HLF1 A.2 formula, copied)
ka5 = {}
for ft in FOOTS:
    setz(0.0, own=True)
    for cs in ("ADOPT", "S1.25", "S2", "S3", "Sinf"):
        RES["own"][f"{cs}|{ft}"] = pack(ratios_case(ft, 0.0, cs))
    ka5[ft] = mrel(RES["own"][f"ADOPT|{ft}"]["R_tot"], HOWN["primary"][ft]["R_tot"])
    setz(0.0); MLO, MHI = HAL["M_lo"], HAL["M_hi"]; row = {}
    for cs in ("ADOPT", "S1.25", "S2", "S3", "Sinf"):
        r = ratios_case(ft, 0.0, cs, keepU=True); W_M, BIAS, NORM_TA, PL = (L[k] for k in ("W_M", "BIAS", "NORM_TA", "PL")); rr = {}
        for kk in (1.0, 3.0):
            j = int(np.argmin(abs(KK - kk)))
            d1 = W_M * ((r["US"][:, j] / RHO_M) ** 2 - (r["UR"][:, j] / RHO_M) ** 2)
            d2 = PL[j] * (r["IS"][j] + r["IR"][j]) * W_M * BIAS * (r["US"][:, j] - r["UR"][:, j]) / RHO_M / NORM_TA
            d = np.abs(d1 + d2); g = (MM >= MLO) & (MM < MHI); tot = float(d.sum())
            rr[str(kk)] = dict(f_res=float(d[g].sum() / tot) if tot > 0 else float("nan"), below=float(d[MM < MLO].sum() / tot) if tot > 0 else float("nan"),
                               above=float(d[MM >= MHI].sum() / tot) if tot > 0 else float("nan"))
        row[cs] = rr
    RES["f_res"][ft] = row
    P(f"  [{ft}] own list (HLF1) R_cold at k 0.1/0.3/1/3/10: " + "; ".join(f"{cs} " + "/".join(f"{x:.5f}" for x in RES['own'][f'{cs}|{ft}']['R_cold_at']) for cs in ("ADOPT", "S2"))
      + f"; f_res at k 1: " + ", ".join(f"{cs} {v['1.0']['f_res']:.3f}" for cs, v in row.items()) + f"   [{time.time() - T0:.0f} s]")
RES["KA"]["KA_H5"] = dict(max_rel=ka5, pass_=bool(max(ka5.values()) <= 1e-8))
RES["KA"]["f_res_ADOPT_vs_HLF1_reported"] = {ft: [RES["f_res"][ft]["ADOPT"]["1.0"]["f_res"], HOWN.get("f_res", {}).get(ft, {}).get("1.0", {}).get("f_res")] for ft in FOOTS}
P(f"KA-H5 ADOPT with HLF1's own list against HLF1's stored R_tot: {ka5} -> {'PASS' if RES['KA']['KA_H5']['pass_'] else 'FAIL'}; f_res ADOPT (mine, HLF1's inherited-run value): {RES['KA']['f_res_ADOPT_vs_HLF1_reported']}")

# ------------------------------------------------------------------ CO1's layout brackets at z = 0 (KA-H6 per bracket)
BR = [("pre_1", dict(pre=1.0), {}), ("pre_0", dict(pre=0.0), {}), ("galaxy_virial_scope", dict(gal_scope="vir"), {}), ("gas_core_0.2", dict(rc_fac=0.2), {}),
      ("press_schechter", {}, dict(mf="ps")), ("conc_x0.7", {}, dict(cfac=0.7)), ("conc_x1.3", {}, dict(cfac=1.3))]
ka6 = {}
for ft in FOOTS:
    for name, opt, pop in BR:
        setz(0.0, **pop)
        for cs in ("ADOPT", "S1.25", "S2", "S3", "Sinf"):
            RES["brackets"][f"{name}|{cs}|{ft}"] = pack(ratios_case(ft, 0.0, cs, opt))
        e = mrel(RES["brackets"][f"{name}|ADOPT|{ft}"]["R_tot"], CO1["brackets"][ft][name]["R_tot"])
        ka6[f"{name}|{ft}"] = dict(max_rel=e, reproduced=bool(e <= 1e-6))
        P(f"  [{ft}] bracket {name:20s} R_cold k 1 / 3: " + "; ".join(f"{cs} {RES['brackets'][f'{name}|{cs}|{ft}']['R_cold_at'][2]:.5f}/{RES['brackets'][f'{name}|{cs}|{ft}']['R_cold_at'][3]:.5f}"
                                                                    for cs in ("ADOPT", "S2")) + f"; ADOPT vs CO1 {e:.1e} -> {'reproduced' if e <= 1e-6 else 'NOT REPRODUCED'}   [{time.time() - T0:.0f} s]")
RES["KA"]["KA_H6"] = ka6

# ------------------------------------------------------------------ TW-B bite (z = 0)
bite = {}
for ft in FOOTS:
    s2, tw = RES["cases"][f"S2|{ft}|0.0"], MUT["TWB"][f"TWB|{ft}|0.0"]
    a = abs(tw["R_cold_at"][3] - 1); b = abs(s2["R_cold_at"][3] - 1)
    bite[ft] = dict(n_ref_S2=s2["n_ref"], n_ref_TWB=tw["n_ref"], dRcold_k3_S2=b, dRcold_k3_TWB=a, bites=bool(tw["n_ref"] < s2["n_ref"] and a >= 1.2 * b))
MUT["TWB_bite"] = dict(rows=bite, bites=bool(all(v["bites"] for v in bite.values())))
P(f"TW-B (boundary 2 v*, f 2) at z 0: {bite} -> {'bites' if MUT['TWB_bite']['bites'] else 'DOES NOT BITE'}")

RES["KA_ok"] = bool(all(RES["KA"][k]["pass_"] for k in ("KA_H1", "KA_H2", "KA_H3", "KA_H4", "KA_H5")))
P(f"\nKnown answers H1-H5 all pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "wlj1_hm.json"), "w"), indent=1)
json.dump(MUT, open(os.path.join(HERE, "wlj1_hm_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "wlj1_hm.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
open(os.path.join(HERE, "wlj1_hm_MUTATE.out"), "w").write("\n".join(l for l in OUT if "TW-B" in l or "TWB" in l) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
P(f"done ({time.time() - T0:.0f} s)")
