#!/usr/bin/env python3
"""HLF1 copy of closure_2026_11_09/CO1_form_b_cosmology_computed/co1_hm.py (CO1 criteria 020522140a). Changes (HLF1 FROZEN_CRITERIA
123947b9dc, A.1 to A.3): the population switch gains the own list (HLF1_LIST=inherited|own; own = Tinker 2008 x r_j and Tinker 2010 x
bias ratio inside the resolved bins of hlf1_halos.json); KA1 is computed with the inherited list; PD1 path; output names; A.2 f_res
(inherited run) and MUTATE MA3 (own run, -> hlf1_hm_MUTATE.json). Every formula of the layout is unchanged. Original docstring:
CO1 (FROZEN_CRITERIA.md, 020522140a) part 1: the 1-halo redistribution of form B's stated layout.
CFG556's halo model, library part executed read-only (nothing in that folder is written). Section 3 of the criteria:
  galaxy regime (v_vir <= v_stiff): ONE1's galaxy rule in its Lagrangian scope;
  group / cluster regime (v_vir > v_stiff): PD1 A1 / A2's rule in the R200c scope;
  comparison layout Rb: the same baryons, the cold component in the reference NFW shape.
R_tot = 1 + (P_B - P_Lta) / P_std, R_bar = 1 + (P_Rb - P_Lta) / P_std, R_cold = R_tot / R_bar.  z = 0.

  nice -n 10 python3 co1_hm.py     -> co1_hm.json, co1_hm.out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Inherited halo list (flagged in the criteria)."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LIST = os.environ.get("HLF1_LIST", "inherited"); assert LIST in ("inherited", "own", "own5e13")   # own5e13: AMENDMENT A1 reported bracket (own bins with lower edge >= 5e13 only)
HAL = json.load(open(os.path.join(HERE, "hlf1_halos.json"))) if LIST != "inherited" or os.path.exists(os.path.join(HERE, "hlf1_halos.json")) else None
SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
os.environ["CFG556_MUTATE"] = "0"
L = {"__file__": SRC, "__name__": "cfg556_lib"}
exec(compile(code[:cut], SRC, "exec"), L)                     # cosmology, mass function, NFW, baryon shapes, U(k), spectra
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
h, FB, RHO_M, G, A0MPC, LM, MM, KK = (L[k] for k in ("h", "FB", "RHO_M", "G", "A0MPC", "LM", "MM", "KK"))
m_nfw, M_L, rgrid, U_of, nu_k = (L[k] for k in ("m_nfw", "M_L", "rgrid", "U_of", "nu_k"))
FOOTS = ("canonical", "alt")
VST = {"canonical": 265.8, "alt": 288.1}                     # PD1 A1, km/s
CS_IGM = 15.0
try:
    _pd1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust", "pd1.json")))
    XSH = {f: float(np.median([r["share_over_Mb"] for r in _pd1[f]["share_tables"]["z0.0"]])) for f in FOOTS}; XSRC = "pd1.json"
except Exception as e:                                        # the criteria's printed values
    XSH = {"canonical": 59.486, "alt": 59.503}; XSRC = f"criteria constants ({type(e).__name__})"
KSEL = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0]

# ------------------------------------------------------------------ baryon shapes (CFG556's baryon_cum with the gas core as a parameter)
def bar_cum(hb, Mbret, r, Rt, rc_fac=0.1):
    ms = min(L["mstar"](hb), Mbret); mg = Mbret - ms
    a = 0.015 * hb["r200c"] / (1 + math.sqrt(2)); rc = rc_fac * hb["r200c"]
    rr = np.minimum(r, Rt)
    hs = lambda x: x ** 2 / (x + a) ** 2
    gb = lambda x: x / rc - np.arctan(x / rc)
    return ms * hs(rr) / hs(Rt) + mg * gb(rr) / gb(Rt)

def phantom(mb, r, a0, kernel):
    """M_b(<r) [nu(G M_b / r^2 a0) - 1] in Msun/h (r in Mpc/h; a0 in (km/s)^2 / Mpc)."""
    if kernel == "simple":
        return np.sqrt(0.25 * mb ** 2 + mb * r ** 2 * a0 / (G * h)) - 0.5 * mb
    y = G * mb * h / (np.maximum(r, 1e-30) ** 2 * a0)
    return np.where((r > 0) & (mb > 0), mb * (nu_k(y) - 1.0), 0.0)

def v_vir(hb): return math.sqrt(G * hb["M200c"] / hb["r200c"])
def is_cluster(hb, foot, bound):
    return (hb["M"] > 1e13) if bound == "m13" else (v_vir(hb) > VST[foot])

def layout(hb, foot, mode="B", pre=0.5, bound="vstiff", gal_scope="lag", clu_scope="r200c", rc_fac=0.1, kernel="simple", Wzero=False):
    """(r, M(<r), info) on [0, r_ta]. mode: B (form B) | Rb (same baryons, cold in the reference shape) | L (the reference itself)."""
    a0 = A0MPC[foot]; X = XSH[foot]; rta, Mta = hb["rta"], hb["Mta"]
    r = rgrid(hb, rta); ML = M_L(hb, r)
    if mode == "L":
        return r, ML.copy(), dict(regime="L")
    if not is_cluster(hb, foot, bound):
        Rs, Ms = (rta, Mta) if gal_scope == "lag" else (hb["r200"], hb["M"])
        Mcold = (1 - FB) * Ms; Mb = Mcold / X; rM = math.sqrt(G * Mb * h / a0); rt = math.sqrt(X * (X + 1)) * rM
        r = np.unique(np.concatenate([r, [min(rt, Rs), Rs]])); r = r[r <= rta * (1 + 1e-14)]; ML = M_L(hb, r)
        rin = np.minimum(r, Rs); shape = M_L(hb, rin) / Ms; outside = np.where(r > Rs, ML - Ms, 0.0)
        unc = (FB * Ms - Mb) * shape
        if mode == "Rb":
            return r, Mb + Mcold * shape + unc + outside, dict(regime="galaxy", Mb=Mb)
        ph = np.minimum(phantom(np.full_like(r, Mb), rin, a0, kernel), Mcold)
        rem = max(Mcold - float(ph[-1] if gal_scope == "lag" else np.interp(Rs, r, ph)), 0.0)
        cold = ph + rem * rin / Rs
        return r, Mb + cold + unc + outside, dict(regime="galaxy", Mb=Mb, rM=rM, rt=rt, rt_over_rta=rt / rta, rt_over_r200m=rt / hb["r200"],
                                                  rem_over_cold=rem / Mcold)
    # group / cluster regime
    R2, M2 = hb["r200c"], hb["M200c"]
    Ms = M2 if clu_scope == "r200c" else Mta
    Mbs = FB * Ms; share = (1 - FB) * Ms
    r = np.unique(np.concatenate([r, [R2]])); ML = M_L(hb, r)
    rin = np.minimum(r, R2); mb = bar_cum(hb, Mbs, r, R2, rc_fac)
    outside = np.where(r > R2, ML - M2, 0.0) if clu_scope == "r200c" else 0.0
    nfw_in = m_nfw(rin / hb["rs"]) / m_nfw(R2 / hb["rs"])
    if mode == "Rb":
        return r, mb + share * nfw_in + outside, dict(regime="cluster")
    v = v_vir(hb)
    fc = 1.0 if pre == "all" else pre * (1 - (VST[foot] / v) ** 2)
    fc = min(max(fc, 0.0), 1.0)
    W = 0.0 if Wzero else 1.5 * v * v / (1.5 * v * v + CS_IGM ** 2)
    E = (1 - fc) * share
    ph_raw = W * phantom(mb, r, a0, kernel); ph = np.minimum(ph_raw, E)
    reached = bool(ph_raw[-1] >= E)
    rtr = float(np.interp(E, ph_raw, r)) if (reached and E > 0) else (0.0 if E == 0 else float("nan"))
    rem = max(E - float(ph[-1]), 0.0)
    return r, mb + fc * share * nfw_in + ph + rem * r / rta + outside, dict(regime="cluster", v_vir=v, f_core=fc, W=W, Rtrunc_over_R200c=rtr / R2,
                                                                         rem_over_share=rem / share, reached=reached)

# ------------------------------------------------------------------ population switches (inherited ingredients; brackets)
BASE = {k: L[k] for k in ("W_M", "BIAS", "A_MISS", "HB", "MTA", "NORM_TA", "conc")}
def own_factors(rmult=1.0):
    fw = np.ones_like(MM); fb = np.ones_like(MM)
    lo_min = 5e13 if LIST == "own5e13" else 0.0
    for b in HAL["bins"]:
        if b["lo"] < lo_min: continue
        g = (MM >= b["lo"]) & (MM < b["hi"]); fw[g] = b["r"] * rmult
    for b in HAL["bias_bins"]:
        if b["used"] and b["lo"] >= lo_min:
            g = (MM >= b["lo"]) & (MM < b["hi"]); fb[g] = b["ratio"]
    return fw, fb
def set_population(mf=None, cfac=1.0, rmult=1.0):
    mf = mf or ("tinker" if LIST == "inherited" else "own")
    SIG = L["SIG"]; DC = L["DC"]
    if mf == "tinker":
        W_M, BIAS = BASE["W_M"], BASE["BIAS"]
    elif mf == "own":
        fw, fb = own_factors(rmult); W_M, BIAS = BASE["W_M"] * fw, BASE["BIAS"] * fb
    else:                                                      # Press-Schechter with the Mo-White bias
        nu = DC / SIG; f = math.sqrt(2 / math.pi) * nu * np.exp(-0.5 * nu ** 2)
        dlns = np.gradient(np.log(SIG), LM * math.log(10))
        W_M = f * RHO_M / MM * (-dlns) * L["DLM"]; BIAS = 1 + (nu ** 2 - 1) / DC
    L["W_M"], L["BIAS"] = W_M, BIAS
    L["A_MISS"] = 1.0 - float(np.sum(W_M * BIAS * MM)) / RHO_M
    L["conc"] = (lambda M: cfac * 10.14 * (M / 2e12) ** -0.081)
    L["HB"] = [L["halo_basics"](M) for M in MM] if cfac != 1.0 else BASE["HB"]
    L["MTA"] = np.array([hb["Mta"] for hb in L["HB"]])
    L["NORM_TA"] = float(np.sum(W_M * BIAS * L["MTA"])) / RHO_M

def ratios(foot, **opt):
    """R_tot, R_bar, R_cold on KK for the current population."""
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, IL = L["spectra_ta"](UL)
    UB, infB = L["U_set"](lambda hb: layout(hb, foot, mode="B", **opt)); PB, _, IB = L["spectra_ta"](UB)
    optR = {k: v for k, v in opt.items() if k in ("bound", "gal_scope", "clu_scope", "rc_fac")}
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb", **optR)); PR, _, IR = L["spectra_ta"](UR)
    Rtot = 1 + (PB - PLta) / Pstd; Rbar = 1 + (PR - PLta) / Pstd
    w8 = L["_W8"](KK * 8.0) ** 2 * KK ** 2 / (2 * math.pi ** 2)
    s8 = lambda R: math.sqrt(np.trapz(Pstd * R * w8, KK))
    return dict(Rtot=Rtot, Rbar=Rbar, Rcold=Rtot / Rbar, Pstd=Pstd, UB=UB, UR=UR, IB=IB, IR=IR, infB=infB,
                s8_tot=s8(Rtot) / s8(np.ones_like(KK)), s8_bar=s8(Rbar) / s8(np.ones_like(KK)), I_B=float(IB[0]), I_R=float(IR[0]))
def at(R): return {str(k): float(np.interp(k, KK, R)) for k in KSEL}

RES = dict(lane="HLF1", halo_list=LIST, part="halo model (CO1 copy)", criteria="020522140a; HLF1 123947b9dc", note="kappa = 1/2 FITTED; not theory closed; adopts nothing; inherited halo list",
           k=KK.tolist(), X=XSH, X_source=XSRC, v_stiff=VST, KA={}, primary={}, brackets={}, MUTATE={})
P("CO1 part 1: the 1-halo redistribution of form B's layout (CFG556 machinery, read-only). kappa = 1/2 FITTED; not theory closed.")
P(f"X (PD1's printed share) {XSH['canonical']:.4f} / {XSH['alt']:.4f} from {XSRC}; v_stiff {VST['canonical']} / {VST['alt']} km/s; FB {FB:.5f} "
  f"(cold / baryon {(1 - FB) / FB:.3f})")

# ------------------------------------------------------------------ KA1: CFG556's committed primary table
C556 = json.load(open(os.path.join(os.path.dirname(SRC), "cfg556_results.json")))
set_population(mf="tinker")
Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
Ulta, _ = L["U_set"](lambda hb: L["frame_profile"](hb, "canonical", mode="lta")); Plta, _, _ = L["spectra_ta"](Ulta)
CANDB = {}; ka1 = {}
for ft in FOOTS:
    U, _ = L["U_set"](lambda hb: L["frame_profile"](hb, ft, edge="cen")); PF, _, _ = L["spectra_ta"](U)
    R = 1 + (PF - Plta) / Pstd; CANDB[ft] = R
    w8 = L["_W8"](KK * 8.0) ** 2 * KK ** 2 / (2 * math.pi ** 2)
    s8r = math.sqrt(L["s8_of"](Pstd) ** 2 + np.trapz((PF - Plta) * w8, KK)) / L["s8_of"](Pstd)
    c = C556["cases"][f"{ft}|census|cen"]
    ka1[ft] = dict(R1=float(np.interp(1.0, KK, R)), R1_committed=c["R_at"]["1.0"], s8_ratio=s8r, s8_committed=c["s8_ratio"],
                   max_rel_R=float(np.max(np.abs(R / np.array(c["R"]) - 1))))
    ka1[ft]["pass_"] = bool(abs(ka1[ft]["R1"] - c["R_at"]["1.0"]) <= 1e-3 and abs(s8r - c["s8_ratio"]) <= 1e-3)
    P(f"KA1 {ft}: candidate B primary R(k 1) {ka1[ft]['R1']:.4f} (committed {c['R_at']['1.0']:.4f}), sigma8 ratio {s8r:.4f} ({c['s8_ratio']:.4f}), "
      f"max rel over k {ka1[ft]['max_rel_R']:.1e} -> {'PASS' if ka1[ft]['pass_'] else 'FAIL'}")
RES["KA"]["KA1"] = ka1
RES["MUTATE"]["M1_candB_R"] = {ft: CANDB[ft].tolist() for ft in FOOTS}
set_population()
# HLF1 code fix (2026-11-11, disclosed): KA2's reference spectra are recomputed under the population in use (identical for the inherited list)
Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
Ulta, _ = L["U_set"](lambda hb: L["frame_profile"](hb, "canonical", mode="lta")); Plta, _, _ = L["spectra_ta"](Ulta)

# ------------------------------------------------------------------ KA2, KA3, KA7
ka2 = {}; ka3 = 0.0; mono = True
for ft in FOOTS:
    UL, _ = L["U_set"](lambda hb: layout(hb, ft, mode="L")); PLx, _, _ = L["spectra_ta"](UL)
    n1 = float(np.max(np.abs((PLx - Plta) / Pstd)))
    UB, _ = L["U_set"](lambda hb: layout(hb, ft, mode=("B" if is_cluster(hb, ft, "vstiff") else "Rb"), pre="all", Wzero=True))
    UR, _ = L["U_set"](lambda hb: layout(hb, ft, mode="Rb"))
    PB, _, _ = L["spectra_ta"](UB); PR, _, _ = L["spectra_ta"](UR)
    n2 = float(np.max(np.abs((1 + (PB - Plta) / Pstd) / (1 + (PR - Plta) / Pstd) - 1)))
    ka2[ft] = dict(null_reference=n1, null_cluster_core_only=n2, pass_=bool(n1 <= 1e-6 and n2 <= 1e-6))
    P(f"KA2 {ft}: reference through my code path max |R - 1| {n1:.1e}; cluster rule with the whole share in the core, W = 0: max |R_cold - 1| {n2:.1e} "
      f"-> {'PASS' if ka2[ft]['pass_'] else 'FAIL'}")
    for hb in L["HB"]:
        for mode in ("B", "Rb"):
            for opt in (dict(), dict(pre=1.0), dict(pre=0.0), dict(bound="m13"), dict(gal_scope="vir"), dict(rc_fac=0.2), dict(kernel="cfg556"), dict(clu_scope="lag")):
                if mode == "Rb": opt = {k: v for k, v in opt.items() if k in ("bound", "gal_scope", "clu_scope", "rc_fac")}
                r, Mc, _ = layout(hb, ft, mode=mode, **opt)
                ka3 = max(ka3, abs(Mc[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(Mc) >= -1e-9 * hb["Mta"]))
RES["KA"]["KA2"] = ka2
RES["KA"]["KA3"] = dict(max_rel_mass=ka3, monotone=mono, pass_=bool(ka3 <= 1e-9 and mono))
P(f"KA3 every layout (primary and brackets), every mass: max |M(<r_ta) - M_ta| / M_ta {ka3:.1e}; non-decreasing {mono} -> {'PASS' if RES['KA']['KA3']['pass_'] else 'FAIL'}")
ka7 = max(abs((0.5 + math.sqrt(0.25 + X * (X + 1))) - (1 + X)) for X in XSH.values())
RES["KA"]["KA7"] = dict(err=ka7, pass_=bool(ka7 <= 1e-12)); P(f"KA7 m(x_t) = 1 + X at x_t^2 = X (X + 1): err {ka7:.1e} -> {'PASS' if ka7 <= 1e-12 else 'FAIL'}")

# ------------------------------------------------------------------ primary
def describe(foot, infB):
    HBs = L["HB"]; cl = np.array([i["regime"] == "cluster" for i in infB])
    out = dict(boundary_M200m=float(MM[np.argmax(cl)]) if cl.any() else None, boundary_M200c=float(HBs[int(np.argmax(cl))]["M200c"]) if cl.any() else None)
    rows = {}
    for lm in (11.0, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0):
        i = int(np.argmin(abs(LM - lm))); inf = infB[i]; hb = HBs[i]
        rB, MB_, _ = layout(hb, foot, mode="B"); rR, MR_, _ = layout(hb, foot, mode="Rb")
        xs = (0.1, 0.3, 0.5, 0.7, 1.0, 2.0)
        rat = [float(np.interp(x * hb["r200c"], rB, MB_) / np.interp(x * hb["r200c"], rR, MR_)) for x in xs]
        rows[f"{lm:g}"] = dict(regime=inf["regime"], M_B_over_M_Rb_at_xR200c=dict(zip(map(str, xs), rat)),
                               **{k: float(v) for k, v in inf.items() if k not in ("regime", "reached") and v is not None})
    out["rows"] = rows; out["n_remainder"] = int(sum(1 for i in infB if i.get("rem_over_share", i.get("rem_over_cold", 0.0)) > 1e-9))
    return out
def drivers(Rr):
    W_M, BIAS, NORM_TA, MTA, PL = (L[k] for k in ("W_M", "BIAS", "NORM_TA", "MTA", "PL")); out = {}
    for kk in (0.35, 1.0, 3.0):
        j = int(np.argmin(abs(KK - kk)))
        d1 = W_M * ((Rr["UB"][:, j] / RHO_M) ** 2 - (Rr["UR"][:, j] / RHO_M) ** 2)
        d2 = PL[j] * (Rr["IB"][j] + Rr["IR"][j]) * W_M * BIAS * (Rr["UB"][:, j] - Rr["UR"][:, j]) / RHO_M / NORM_TA
        dec = {}
        for lo in range(10, 16):
            mm = (np.log10(MTA) >= lo) & (np.log10(MTA) < lo + 1)
            dec[f"{lo}-{lo + 1}"] = dict(oneh=float(d1[mm].sum() / Rr["Pstd"][j]), twoh=float(d2[mm].sum() / Rr["Pstd"][j]))
        out[str(kk)] = dict(dR=float((Rr["Rtot"][j] - Rr["Rbar"][j])), by_logMta=dec)
    return out
P("\nPrimary layout. R_cold = R_tot / R_bar (the cold component re-laid, same baryons). k in h/Mpc.")
P("  k:        " + "  ".join(f"{k:>6g}" for k in KSEL))
for ft in FOOTS:
    set_population(); Rr = ratios(ft)
    RES["primary"][ft] = dict(R_tot=Rr["Rtot"].tolist(), R_bar=Rr["Rbar"].tolist(), R_cold=Rr["Rcold"].tolist(), R_tot_at=at(Rr["Rtot"]), R_bar_at=at(Rr["Rbar"]),
                              R_cold_at=at(Rr["Rcold"]), s8_ratio_tot=Rr["s8_tot"], s8_ratio_bar=Rr["s8_bar"], s8_ratio_cold=Rr["s8_tot"] / Rr["s8_bar"],
                              I_k1e3=[Rr["I_B"], Rr["I_R"]], layout=describe(ft, Rr["infB"]), drivers=drivers(Rr))
    for nm, key in (("R_tot ", "Rtot"), ("R_bar ", "Rbar"), ("R_cold", "Rcold")):
        P(f"  {ft:9s} {nm}: " + "  ".join(f"{np.interp(k, KK, Rr[key]):6.3f}" for k in KSEL))
    d = RES["primary"][ft]
    P(f"  {ft:9s} sigma8 ratio: tot {d['s8_ratio_tot']:.4f}, bar {d['s8_ratio_bar']:.4f}, cold {d['s8_ratio_cold']:.4f}; 2-halo I(k 1e-3) {Rr['I_B']:.6f} / {Rr['I_R']:.6f}; "
      f"regime boundary M200m {d['layout']['boundary_M200m']:.3e} (M200c {d['layout']['boundary_M200c']:.3e}) Msun/h; halos with a remainder {d['layout']['n_remainder']}")
    for lm, row in d["layout"]["rows"].items():
        ex = (f"r_t/r_ta {row['rt_over_rta']:.2f}, r_t/r200m {row['rt_over_r200m']:.2f}" if row["regime"] == "galaxy"
              else f"f_core {row['f_core']:.3f}, R_trunc/R200c {row['Rtrunc_over_R200c']:.2f}, remainder/share {row['rem_over_share']:.3f}")
        P(f"      log M200m {lm:>4s} {row['regime']:7s} M_B/M_Rb at r/R200c 0.1 0.3 0.5 0.7 1 2: " + " ".join(f"{v:.2f}" for v in row["M_B_over_M_Rb_at_xR200c"].values()) + f" | {ex}")
    for kk, dv in d["drivers"].items():
        P(f"      R_tot - R_bar at k {kk}: {dv['dR']:+.4f}; by log M_ta decade (1-halo / 2-halo): " + "; ".join(f"{a} {b['oneh']:+.4f}/{b['twoh']:+.4f}" for a, b in dv["by_logMta"].items()))

# ------------------------------------------------------------------ brackets and M4
BR = [("pre_1", dict(pre=1.0), {}), ("pre_0", dict(pre=0.0), {}), ("boundary_1e13", dict(bound="m13"), {}), ("galaxy_virial_scope", dict(gal_scope="vir"), {}),
      ("gas_core_0.2", dict(rc_fac=0.2), {}), ("press_schechter", {}, dict(mf="ps")), ("conc_x0.7", {}, dict(cfac=0.7)), ("conc_x1.3", {}, dict(cfac=1.3)),
      ("kernel_cfg556", dict(kernel="cfg556"), {})]
P("\nBrackets (reported, never graded): R_cold at k = 0.3, 0.5, 1, 2, 3, 5; sigma8 ratio (cold)")
for ft in FOOTS:
    RES["brackets"][ft] = {}
    for name, opt, pop in BR:
        set_population(**pop); Rr = ratios(ft, **opt)
        RES["brackets"][ft][name] = dict(R_tot=Rr["Rtot"].tolist(), R_bar=Rr["Rbar"].tolist(), R_cold_at=at(Rr["Rcold"]), s8_ratio_cold=Rr["s8_tot"] / Rr["s8_bar"])
        P(f"  {ft:9s} {name:20s}: " + "  ".join(f"{np.interp(k, KK, Rr['Rcold']):6.3f}" for k in (0.3, 0.5, 1.0, 2.0, 3.0, 5.0)) + f"   | {Rr['s8_tot'] / Rr['s8_bar']:.4f}")
    set_population(); Rr = ratios(ft, clu_scope="lag")
    r1 = float(np.interp(1.0, KK, Rr["Rcold"])); r0 = RES["primary"][ft]["R_cold_at"]["1.0"]
    RES["MUTATE"].setdefault("M4", {})[ft] = dict(R_cold_k1=r1, primary=r0, rise=r1 - r0, bites=bool(r1 - r0 >= 0.10), R_tot=Rr["Rtot"].tolist(), R_bar=Rr["Rbar"].tolist())
    P(f"  {ft:9s} M4 cluster rule in the Lagrangian scope: R_cold(k 1) {r1:.3f} against {r0:.3f}: rise {r1 - r0:+.3f} -> {'bites' if r1 - r0 >= 0.10 else 'DOES NOT BITE'}")
set_population()
# ------------------------------------------------------------------ HLF1 A.2: resolved share f_res (inherited run) and MUTATE MA3 (own run)
if HAL is not None and HAL.get("M_lo") and HAL.get("M_hi"):
    MLO, MHI = HAL["M_lo"], HAL["M_hi"]; RES["f_res"] = {}
    for ft in FOOTS:
        set_population(mf="tinker"); Rr = ratios(ft); W_M, BIAS, NORM_TA, PL = (L[k] for k in ("W_M", "BIAS", "NORM_TA", "PL")); row = {}
        for kk in (1.0, 3.0):
            j = int(np.argmin(abs(KK - kk)))
            d1 = W_M * ((Rr["UB"][:, j] / RHO_M) ** 2 - (Rr["UR"][:, j] / RHO_M) ** 2)
            d2 = PL[j] * (Rr["IB"][j] + Rr["IR"][j]) * W_M * BIAS * (Rr["UB"][:, j] - Rr["UR"][:, j]) / RHO_M / NORM_TA
            d = np.abs(d1 + d2); g = (MM >= MLO) & (MM < MHI)
            row[str(kk)] = dict(f_res=float(d[g].sum() / d.sum()), below=float(d[MM < MLO].sum() / d.sum()), above=float(d[MM >= MHI].sum() / d.sum()))
        RES["f_res"][ft] = row
        P(f"A.2 f_res {ft}: resolved [{MLO:.2e}, {MHI:.2e}] carries " + "; ".join(f"k {k}: {v['f_res']:.3f} (below {v['below']:.3f}, above {v['above']:.3f})" for k, v in row.items()))
    set_population()
if LIST == "own":
    set_population(); Ps1 = float(np.interp(1.0, KK, L["spectra_std"](L["U_std"]())[0]))
    set_population(rmult=2.0); Ps2 = float(np.interp(1.0, KK, L["spectra_std"](L["U_std"]())[0])); set_population()
    MA3 = dict(P_std_k1_own=Ps1, P_std_k1_doubled=Ps2, change=Ps2 / Ps1 - 1, bites=bool(abs(Ps2 / Ps1 - 1) >= 0.10))
    json.dump(dict(lane="HLF1", MUTATE=dict(MA3=MA3), note="kappa = 1/2 FITTED; not theory closed; adopts nothing"), open(os.path.join(HERE, "hlf1_hm_MUTATE.json"), "w"), indent=1)
    open(os.path.join(HERE, "hlf1_hm_MUTATE.out"), "w").write(f"MA3 own list with every r_j doubled: P_std(k 1) {Ps1:.4e} -> {Ps2:.4e} ({Ps2 / Ps1 - 1:+.3f}) -> {'bites' if MA3['bites'] else 'DOES NOT BITE'}\n")
    P(f"MA3 (MUTATE file): P_std(k 1) change {Ps2 / Ps1 - 1:+.3f} -> {'bites' if MA3['bites'] else 'DOES NOT BITE'}")
RES["KA_ok"] = bool(all(v["pass_"] for v in ka1.values()) and all(v["pass_"] for v in ka2.values()) and RES["KA"]["KA3"]["pass_"] and RES["KA"]["KA7"]["pass_"])
P(f"\nKnown answers of this part all pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, f"hlf1_hm_{LIST}.json"), "w"), indent=1)
open(os.path.join(HERE, f"hlf1_hm_{LIST}.out"), "w").write("\n".join(OUT) + "\n")
