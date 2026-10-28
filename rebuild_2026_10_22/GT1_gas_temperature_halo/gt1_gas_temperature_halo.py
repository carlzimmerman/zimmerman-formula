#!/usr/bin/env python3
"""GT1_gas_temperature_halo: where a hot atmosphere fills the potential, cold dark energy settles into the gas's isothermal
potential. Inside R_g (R500) the total mass is IB1's hydrostatic HG mass 3 beta sigma^2 r^3 / G(r^2 + r_c^2); beyond it the
halo carries the remaining GS1 native fair-share budget to r_ta by k-scaling the CL2 profile. Everything else is the CL2
picture + BS1's basin switch, unchanged.

FROZEN_CRITERIA.md committed alone first (ef8161361e); AMENDMENTS.md A1-A8 committed alone before this script (1c28336cbd).
Harnesses executed read-only as text copies: BS1's head (X43 / X53 / X51 copies, HO2's MW head), X43 + X30 (IB1's
configuration for K0), HG2 / HG1 (groups, D statistic), CS2's X-COP rows (as HO1). Nothing is downloaded.

kappa = 1/2 FITTED; footings never pooled (canonical primary); cold dark energy = gravitating w ~ 0 field component, never a
particle; the shared isothermal potential is a POSIT (no action written); not theory closed; nothing here says the data
favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gt1_gas_temperature_halo.py        (GT1_MUTATE=1 twin)
"""
import os, sys, io, csv, json, math, time, resource, contextlib, warnings
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
MUTATE = os.environ.get("GT1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUTATE else ""
for _v in [k for k in os.environ if k.endswith("_MUTATE")] + ["MUTATE", "CFG528_POSTFREEZE"]: os.environ.pop(_v, None)
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from astropy.io import fits
warnings.filterwarnings("ignore", category=RuntimeWarning); warnings.filterwarnings("ignore", category=DeprecationWarning)

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
FEET = ("canonical", "alt"); HKS = ("h0672", "h0686"); BETA = 2.0 / 3.0; S2FAC_K1 = 2.0 if MUTATE else 1.0
P(f"GT1_gas_temperature_halo  {'MUTATE (sigma^2 doubled on K1 analytic side; K1 must fail)' if MUTATE else 'normal run'}   criteria ef8161361e, amendments 1c28336cbd")
P("kappa = 1/2 FITTED; footings never pooled (canonical primary); hot systems: M_tot = M_HG inside R_g, k-scaled CL2 profile to the GS1 budget at r_ta; "
  "the shared isothermal potential is a POSIT; not theory closed")

# ================================================================== BS1's head, read-only text copy (A5)
BS1SRC = os.path.join(REB, "BS1_basin_switch", "bs1_basin_switch.py"); TB = open(BS1SRC).read()
def seg(a, b): i = TB.index(a); return TB[i:TB.index(b, i)]
head = TB[:TB.index("# ================================================================== STEP 0 / K0: every basin = the system alone")]
head += seg("# ================================================================== K1 helpers", "PRIM = make_cfg(R0D)")
head += seg("def mw_summary(m, lab):", "mwA = mw_summary(")
head += seg("def verdict(g, m, d):", "VA = verdict(")
for a in ("bs1_x43copy", "bs1_x53copy", "bs1_x51copy", "bs1_x30_machinery", "bs1_ho2copy"): head = head.replace(a, a.replace("bs1_", "gt1_"))
old = '    ns = run_copy(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py"), ed, "gt1_x43copy.py", {"ETA_FUN": ETAF})\n    return ns["RES"]'
assert head.count(old) == 1
head = head.replace(old, '    ed = GT_EDITS(ed)\n    ns = run_copy(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py"), ed, "gt1_x43copy.py", dict({"ETA_FUN": ETAF}, **GT_INJECT()))\n'
                         '    ns["RES"]["_gt"] = GT_POST(ns)\n    return ns["RES"]')
B = {"__file__": os.path.join(HERE, "gt1_bs1copy.py"), "__name__": "__main__"}          # __main__ so forked-pool pickling finds _child (bound below)
_cap = io.StringIO()
with contextlib.redirect_stdout(_cap):
    B.update(GT_EDITS=None, GT_INJECT=None, GT_POST=None)          # bound below, before any call
    exec(compile(head, BS1SRC, "exec"), B)
assert not B["MUTATE"]
P(f"BS1 head executed read-only (R0_data {B['R0D']:.1f} kpc, LG log M_basin {B['LGP']['lgM']:.4f}) [{time.time() - T0:.0f} s]")
NAT_RRAT = B["NAT_RRAT"]; call = B["call"]; CFG = B["CFG"]; _child = B["_child"]

# ================================================================== HG2 / HG1 (read-only) and X-COP rows (CS2, as HO1)
sys.path.insert(0, os.path.join(REB, "HG2_kids_lowg_hot_gas"))
with contextlib.redirect_stdout(io.StringIO()):
    import hg2_kids_lowg_hot_gas as hg2
hg1 = hg2.hg1
HJ = json.load(open(os.path.join(REB, "HG2_kids_lowg_hot_gas", "hg2_kids_lowg_hot_gas.json")))
gb_, go_, Cv_ = hg2.load(*hg2.BLUE)
groups_, mem_ = hg1.load_groups(); erass_ = hg1.load_erass()
ROWS, _ = hg1.build(groups_, mem_, erass_)
REF = hg2.Ref(gb_, go_, Cv_); BASE_D = hg2.deltas(ROWS, REF)
D0, nb0, nf0 = hg1.D_stat(ROWS, BASE_D); LO0, HI0 = float(HJ["ci95"][0]), float(HJ["ci95"][1])
EMG = {}
for e in erass_: EMG.setdefault(e[0], []).append(e)
assert all(len(EMG[r["erass"]]) == 1 for r in ROWS if r["flag"] == "BRIGHT")
hg2_id = abs(D0 - HJ["D"]) < 1e-9 and (len(ROWS), sum(r["flag"] == "BRIGHT" for r in ROWS), int(np.isfinite(BASE_D).sum())) == (190, 14, 188)
P(f"HG2 sample identity: {len(ROWS)} groups, BRIGHT {sum(r['flag'] == 'BRIGHT' for r in ROWS)}, supported {int(np.isfinite(BASE_D).sum())}; "
  f"D {D0:+.4f} (HG2 {HJ['D']:+.4f}); measured 95% [{LO0:+.3f}, {HI0:+.3f}]: {'PASS' if hg2_id else 'FAIL'}")

CJ = json.load(open(os.path.join(REB, "CS2_core_law_out_of_sample", "cs2_out_of_sample_results.json")))
TS = open(os.path.join(REB, "CS2_core_law_out_of_sample", "cs2_out_of_sample.py")).read()
codeS = TS[TS.index("# ------------------------------------------------------------------ X-COP (matched-clumping profiles)"):
           TS.index("# ------------------------------------------------------------------ graders per law")]
S = {"os": os, "np": np, "math": math, "csv": csv, "fits": fits, "minimize_scalar": minimize_scalar, "brentq": brentq, "REPO": REPO,
     "check": (lambda k, ok, msg: None), "R0C": CJ["calibration"]["r0_law"]["c"], "R0P": CJ["calibration"]["r0_law"]["p"], "SREF": 70.50}
exec(compile(codeS, "cs2_xcop_ro", "exec"), S)
XC = S["XC"]
IB1RF = json.load(open(os.path.join(REB, "IB1_inner_band_hse", "ib1_rf_results.json")))
EC = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data
ERA, EDE, EZ, EKT = (np.asarray(EC[k], float) for k in ("RA", "DEC", "BEST_Z", "KT"))
XSIG = {}
for c in XC:
    p_ = os.path.join(REPO, "real_research", "data", "xcop", c["name"])
    with fits.open(os.path.join(p_, f"{c['name']}_hydro_mass.fits")) as h:
        z = float(h[1].header["REDSHIFT"]); r500 = float(h[1].header["R500"]); ra = float(h[1].header["RA"]); de = float(h[1].header["DEC"])
    with fits.open(os.path.join(p_, f"{c['name']}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    mg500 = float(S["li"](gas["RADIUS"] * rg500, gas["MGAS"], r500))
    sep = np.degrees(hg1.sep_rad(ra, de, ERA, EDE)) * 60.0; j = int(np.argmin(sep))
    if sep[j] <= 3.0 and abs(EZ[j] - z) <= 0.02 and np.isfinite(EKT[j]) and EKT[j] > 0:
        XSIG[c["name"]] = dict(src="eRASS1 KT", kT=float(EKT[j]), sep_arcmin=float(sep[j]), r500_kpc=r500, z=z, Mg500=mg500)
    else:
        XSIG[c["name"]] = dict(src="RF fill", kT=None, sep_arcmin=float(sep[j]), r500_kpc=r500, z=z, Mg500=mg500,
                               sigma_kms=float(10 ** (IB1RF["fit"]["a"] + IB1RF["fit"]["b"] * math.log10(mg500))))
P("X-COP sigma sources (A4): " + "; ".join(f"{k} {v['src']}" + (f" {v['kT']:.2f} keV" if v["kT"] else f" {v['sigma_kms']:.0f} km/s") for k, v in XSIG.items()))

# ================================================================== the GT rule (runs inside the forked X43 copy)
GTCFG = dict(on=False, Rg="R500", offset=False, fill="rf", name="base")
GTS = {}
def _fills(NX):
    """tercile fill (SC1/OS1's, verbatim arithmetic) and IB1 RF's regression fill (A2)."""
    if "fills" in GTS: return GTS["fills"]
    KT = np.asarray(NX["KT"], float); okk = np.isfinite(KT) & (KT > 0); T3M = NX["T3M"]
    SKT = np.full(len(KT), np.nan); SKT[okk] = np.sqrt(KT[okk] * NX["KEV"] / (0.6 * NX["MP"])) / 1e3
    terc = SKT.copy()
    for t in range(3):
        m = T3M == t; terc[m & ~okk] = float(np.nanmedian(SKT[m & okk]))
    lm = np.log10(np.asarray(NX["MY"]["Mgas500"], float)); ls = np.log10(terc)
    A_ = np.c_[np.ones(okk.sum()), lm[okk]]; co = np.linalg.lstsq(A_, ls[okk], rcond=None)[0]
    rf = terc.copy(); rf[~okk] = 10 ** (co[0] + co[1] * lm[~okk])
    GTS["fills"] = dict(okk=okk, KT=KT, terc=terc, rf=rf, co=(float(co[0]), float(co[1])))
    return GTS["fills"]
def sig2(i, NX, fill):
    F = _fills(NX)
    return float(F["KT"][i] * NX["KEV"] / (0.6 * NX["MP"])) if F["okk"][i] else float((F[fill][i] * 1e3) ** 2)
def sig2_check(i, NX, fill):
    """K1's independent analytic side: sigma^2 from kT (IB1's own constants) or the fill; MUTATE doubles it."""
    F = _fills(NX); MP_, KEV_ = 1.67262192e-27, 1.602176634e-16
    v = F["KT"][i] * KEV_ / (0.6 * MP_) if F["okk"][i] else (F[fill][i] * 1e3) ** 2
    return S2FAC_K1 * float(v)
def gt_hook(i, foot, hk, pp, Mbase, s, r0, rule, a_, NX, Bf):
    if not (GTCFG["on"] and rule): return Mbase
    RM, G, MPC = NX["RM"], NX["G"], NX["MPC"]
    rc = 0.15 * pp["R500"] * MPC; rta = pp["rta"]; s2 = sig2(i, NX, GTCFG["fill"])
    mhg = lambda r: 3 * BETA * s2 * r ** 3 / (G * (r ** 2 + rc ** 2))
    Rg = {"R500": pp["R500"] * MPC, "0.7R500": 0.7 * pp["R500"] * MPC, "rta2": 0.5 * rta, "rta": rta}[GTCFG["Rg"]]
    Mb = pp["Mb"]; on_grid = RM[-1] > rta
    Mbt = float(Mb[-1]) if on_grid else pp["Mfair"] / NAT_RRAT
    Mh = lambda r: math.pi * s * r0 ** 2 * float(Bf(min(r, rta) / r0))
    Mcl2_Rg = float(np.interp(Rg, RM, Mb)) + Mh(Rg); Mcl2_rta = Mbt + Mh(rta); Mbud = Mbt + pp["Mfair"]; MHG = mhg(Rg)
    k, clamp, empty = float("nan"), False, Rg >= rta
    if GTCFG["offset"]:
        outer = Mbase + (MHG - Mcl2_Rg)
    elif empty:
        outer = np.full_like(Mbase, MHG)
    else:
        k = (Mbud - MHG) / (Mcl2_rta - Mcl2_Rg)
        if k < 0: k, clamp = 0.0, True
        outer = MHG + k * (Mbase - Mcl2_Rg)
    M = np.where(RM <= Rg, mhg(RM), outer)
    # K1: inner grid and M_tot(R_g) (outer formula at R_g) vs the independent analytic side
    s2c = sig2_check(i, NX, GTCFG["fill"]); ana = lambda r: 3 * (2.0 / 3.0) * s2c * r ** 3 / (G * (r ** 2 + rc ** 2))
    inn = RM <= Rg
    e_in = float(np.max(np.abs(M[inn] / ana(RM[inn]) - 1))) if inn.any() else 0.0
    at_Rg = MHG if (GTCFG["offset"] or empty) else MHG + k * (Mcl2_Rg - Mcl2_Rg)
    e_rg = abs(at_Rg / ana(Rg) - 1)
    # K2: grid beyond r_ta equals the budget
    e_k2 = None
    if (not GTCFG["offset"]) and (not empty) and k > 0:
        e_k2 = float(np.max(np.abs(M[RM > rta] / Mbud - 1))) if on_grid else abs((MHG + k * (Mcl2_rta - Mcl2_Rg)) / Mbud - 1)
    GTS.setdefault("log", {}).setdefault(f"{foot}|{hk}", []).append(dict(
        i=int(i), k=k, clamp=clamp, empty=empty, excess=MHG / Mbud, Rg_over_rta=Rg / rta, MHG_R500_over_MCL2=MHG / Mcl2_Rg, on_grid=bool(on_grid),
        above=bool(a_), kt=bool(_fills(NX)["okk"][i]), e_k1=max(e_in, e_rg), e_k2=e_k2))
    return M
def gt_stash(foot, hk, V, rule):
    if rule: GTS.setdefault("V", {})[f"{foot}|{hk}"] = V.copy()
def ib1_hook(i, foot, hk, pp, NX, fill):
    """IB1's m_hg verbatim (r_t = 3 Mpc, floor M_b), for K0 (A1)."""
    RG, G, MPC = NX["RG"], NX["G"], NX["MPC"]; rc = 0.15 * pp["R500"]
    F = _fills(NX); MP_, KEV_ = 1.67262192e-27, 1.602176634e-16
    s2 = F["KT"][i] * KEV_ / (0.6 * MP_) if F["okk"][i] else (F[fill][i] * 1e3) ** 2
    r = np.minimum(RG, 3.0) * MPC; M = 3 * BETA * s2 * r ** 3 / (G * (r ** 2 + (rc * MPC) ** 2))
    return np.where(M < pp["Mb"], pp["Mb"], M)

LINE_BS1 = 'V[i] = dvecN(int(i), foot, hk, LF_M(pp["Mb"], Mh, RM, GX, A0[foot], "clusters", a_))'
STASH_OLD = '        cl = f"{foot}|{hk}"; o = M[cl]; vB = bsum(V); vC = bsum(DC_[(foot, hk)])'
def GT_EDITS(ed):
    return ed + [(LINE_BS1, 'V[i] = dvecN(int(i), foot, hk, GT_HOOK(int(i), foot, hk, pp, LF_M(pp["Mb"], Mh, RM, GX, A0[foot], "clusters", a_), s, r0, rule, a_, NX, B))'),
                 (STASH_OLD, '        GT_STASH(foot, hk, V, rule)\n' + STASH_OLD)]
def GT_INJECT():
    GTS.clear(); return {"GT_HOOK": gt_hook, "GT_STASH": gt_stash}

# ---- HG2 groups (HO1's group_pred, plus GT on the BRIGHT arm; A3) and X-COP K4 (A4)
def group_pred(ns, foot, gt):
    NX = ns["NX"]; GE, MSUNE, MPCE, A0 = ns["GE"], ns["MSUNE"], ns["MPCE"], ns["A0"]; Bk, SAT = ns["B"], ns["SAT"]
    bg = ns["BGS"]["A_c2b_refit"]; rc_ = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
    gp, ab, info, k1e, k2e, gtn = [], [], [], [], [], 0
    for r in ROWS:
        bright = r["flag"] == "BRIGHT"
        mg500 = float(EMG[r["erass"]][0][4]) if bright else 0.0
        lMb = math.log10(r["mstar"] + mg500); M200 = 10 ** (bg["a"] + bg["b"] * (lMb - 10))
        R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc_)) ** (1 / 3)
        s, above = ns["sig_core"](foot, "A_c2b_refit", M200); r0 = ns["solve_r0"](M200 * MSUNE, R200, s)
        rr = r["r_mpc"] * hg1.MPC; Mh = math.pi * s * r0 ** 2 * float(Bk(min(rr, R200) / r0)); gh = GE * Mh / rr ** 2
        g = float(B["LF_G"](r["gbar"], gh, A0[foot], "hg2", bool(above)))
        if gt and gt["on"] and bright:
            gtn += 1; R500 = float(EMG[r["erass"]][0][5]); z = float(EMG[r["erass"]][0][3])
            s2 = (r["sigma"] * 1e3) ** 2; rcg = 0.15 * R500 * hg1.MPC
            mhg = lambda x: 3 * BETA * s2 * x ** 3 / (GE * (x ** 2 + rcg ** 2))
            mcl2 = lambda x: (0.5 * r["mstar"] + mg500 * hg1.beta_mass_fraction(x / hg1.MPC, R500)) * hg1.MSUN + math.pi * s * r0 ** 2 * float(Bk(min(x, R200) / r0))
            Mbx, Mbt = NX["_gc2_ext"](mg500, R500, z, 3.0 * 1.2 * mg500 * NX["MSUN"])
            rta = NX["r_ta_com"](Mbt) / (1 + z); Mbud = Mbt * (1 + NAT_RRAT)
            Rg = {"R500": R500 * hg1.MPC, "0.7R500": 0.7 * R500 * hg1.MPC, "rta2": 0.5 * rta, "rta": rta}[gt["Rg"]]
            MHG = mhg(Rg); empty = Rg >= rta; k, clamp = float("nan"), False
            if gt["offset"]: Mt = lambda x: mhg(x) if x <= Rg else mcl2(x) + (MHG - mcl2(Rg))
            elif empty: Mt = lambda x: mhg(min(x, Rg))
            else:
                McRg = mcl2(Rg); k = (Mbud - MHG) / (mcl2(rta) - McRg)
                if k < 0: k, clamp = 0.0, True
                Mt = lambda x, k=k, McRg=McRg: mhg(x) if x <= Rg else MHG + k * (mcl2(min(x, rta)) - McRg)
            g = GE * Mt(rr) / rr ** 2
            s2c = S2FAC_K1 * (r["sigma"] * 1e3) ** 2
            ana = 3 * (2.0 / 3.0) * s2c * Rg ** 3 / (GE * (Rg ** 2 + rcg ** 2))
            outer_at_Rg = MHG if (gt["offset"] or empty) else MHG + k * (mcl2(Rg) - mcl2(Rg))
            k1e.append(max(abs(Mt(Rg) / ana - 1), abs(outer_at_Rg / ana - 1)))
            if (not gt["offset"]) and (not empty) and k > 0: k2e.append(abs(Mt(rta) / Mbud - 1))
            info.append(dict(name=r["name"], sigma=r["sigma"], r_over_R500=rr / (R500 * hg1.MPC), Rg_over_rta=Rg / rta, k=k, clamp=clamp, empty=empty,
                             excess=MHG / Mbud, r_inside_Rg=bool(rr <= Rg), dlog_g=math.log10(g) - math.log10(float(B["LF_G"](r["gbar"], gh, A0[foot], "hg2b", bool(above))))))
        gp.append(g); ab.append(bool(above))
    return np.array(gp), np.array(ab), info, k1e, k2e, gtn
def D_pred(gp):
    dp = np.log10(gp) - REF.logref(np.array([r["gbar"] for r in ROWS]))
    return hg1.D_stat(ROWS, dp)
def GT_POST(ns):
    out = dict(cfg=dict(GTCFG), fills_co=list(_fills(ns["NX"])["co"]), log=GTS.get("log", {}))
    NX = ns["NX"]; dd = {}
    for key, V in GTS.get("V", {}).items():
        foot, hk = key.split("|"); d = NX["DAT"][hk]; WB = d["W"] * d["B"][None, :]
        nb = (WB * (d["D"] - NX["MY"]["leakP"][:, NX["HXI"][hk], 0])).sum(0); dd[key] = (V.sum(0) / nb).tolist()
    out["bin_pred_over_meas"] = dd
    hg = {}
    for f in FEET:
        gpb, abb, _, _, _, _ = group_pred(ns, f, None)
        Db, nbb, nfb = D_pred(gpb)
        r = dict(D_base=float(Db), n_bright=nbb, n_faint=nfb)
        if GTCFG["on"]:
            gpg, abg, info, k1e, k2e, gtn = group_pred(ns, f, GTCFG)
            Dg, nbg, nfg = D_pred(gpg)
            faint = np.array([x["flag"] != "BRIGHT" for x in ROWS])
            r.update(D_gt=float(Dg), n_bright_gt=nbg, n_faint_gt=nfg, info=info, k1_maxrel=max(k1e) if k1e else 0.0, k2_maxrel=max(k2e) if k2e else 0.0,
                     n_gt=gtn, faint_identical=bool(np.array_equal(gpg[faint], gpb[faint])))
        hg[f] = r
    out["hg2"] = hg
    if GTCFG["on"]:                                                            # K4 X-COP construction check (footing-free)
        GE, MSUNE, PCm = ns["GE"], ns["MSUNE"], 3.0857e16; d, per, byx = [], {}, {}
        for c in XC:
            m = XSIG[c["name"]]; s2 = m["kT"] * 1.602176634e-16 / (0.6 * 1.67262192e-27) if m["kT"] else (m["sigma_kms"] * 1e3) ** 2
            rc = 0.15 * m["r500_kpc"] * 1e3 * PCm; dl = []
            for x, rk, mh, mb in c["rows"]:
                if x > 0.75: continue
                rm = rk * 1e3 * PCm
                v = math.log10(GE * mh * MSUNE / rm ** 2) - math.log10(GE * (3 * BETA * s2 * rm ** 3 / (GE * (rm ** 2 + rc ** 2))) / rm ** 2)
                dl.append(v); byx.setdefault(f"{x:g}", []).append(v)
            d += dl; per[c["name"]] = float(np.mean(dl))
        d = np.array(d)
        out["xcop"] = dict(mean=float(d.mean()), rms=float(np.sqrt(np.mean(d ** 2))), n=len(d), per_cluster=per, by_x={k: float(np.mean(v)) for k, v in byx.items()})
    return out
B["GT_EDITS"], B["GT_INJECT"], B["GT_POST"] = GT_EDITS, GT_INJECT, GT_POST

def run_x43_ib1(fill, label):
    """K0 (A1): X43 copy WITHOUT GS1's budget edit (IB1's X30 machinery), cluster line = IB1's m_hg."""
    B["MODE"]["m"] = "on"
    ed = [('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'V[i] = dvecN(int(i), foot, hk, IB1_HOOK(int(i), foot, hk, pp, NX, %r))' % fill),
          ("for cf in (3.0, 5.0):", "for cf in ():"),
          ('f"x43_collapse_core{TAG}.out"', f'"gt1_x43copy_{label}.out"'), ('f"x43_collapse_core_results{TAG}.json"', f'"gt1_x43copy_{label}_results.json"'),
          ('"x43_x30_machinery"', '"gt1_x30_machinery_ib1"')]
    GTS.clear()
    ns = B["run_copy"](os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py"), ed, "gt1_x43copy_ib1.py", {"IB1_HOOK": ib1_hook})
    return dict(cells={f: ns["RES"]["footings"][f]["clusters"]["cells"] for f in FEET}, co=list(_fills(ns["NX"])["co"]))
B["run_x43_ib1"] = run_x43_ib1

def rss_all(): return B["rss_all"]()
checks = []
def check(k, ok, msg): checks.append((k, bool(ok))); P(f"{k} {'PASS' if ok else 'FAIL'}  {msg}")
RES = dict(criteria="ef8161361e", amendments="1c28336cbd", mutate=MUTATE, picture=dict(shape="S9", L=4.0, T=12.3, budget="GS1 measured", basin="BS1"))
LAB = lambda s: s + TAG

# ================================================================== STEP 0 / K0
P("\n=== STEP 0 (K0)")
PRIM = B["make_cfg"](B["R0D"])
CFG.update(T=PRIM["T"], SP=PRIM["spt"], DW=PRIM["dw"], MW=PRIM["mw"])
GTCFG.update(on=False, name="base")
r43b, st43b, _, _, _ = call(B["run_x43"], 4.0, PRIM["T"], LAB("base")); P(f"  X43 copy (GT off) done [{time.time() - T0:.0f} s]")
F53on, _, _, _, _ = call(B["run_x53"], "on", 4.0, PRIM["T"], LAB("base")); F53off, _, _, _, _ = call(B["run_x53"], "off", 4.0, PRIM["T"], LAB("base"))
P(f"  X53 copies done [{time.time() - T0:.0f} s]")
r51, _, _, _, _ = call(B["run_x51"], LAB("base")); r51["flags"] = PRIM["dw"]
C0, _, _, _, _ = call(B["run_sigma"]); B["HO2NS"]["TAB"].update(lg=np.array(C0["lg"]), lsc={t: np.array(v) for t, v in C0["lsc"].items()})
mw, _, _, _, _ = call(B["run_mw"], 4.0); P(f"  X51 + MW done [{time.time() - T0:.0f} s]")
with contextlib.redirect_stdout(io.StringIO()):
    g0 = B["grade"](r43b, F53on, F53off, r51["RES"], "GT off", quiet=True)
    mw0 = B["mw_summary"](mw, "GT off"); dw0 = B["dwarf_grade"](r51, "GT off", quiet=True)
BS1J = json.load(open(os.path.join(REB, "BS1_basin_switch", "bs1_basin_switch_results.json")))["primary"]
def deep_same(a, b, tol=1e-6, pre=""):
    """recursive leaf comparison (dicts, lists, scalars); numbers within tol (absolute, relative where |x| > 1)."""
    bad = []
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b): return [pre + " keys differ"]
        for k in a: bad += deep_same(a[k], b[k], tol, f"{pre}/{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): return [pre + " length differs"]
        for i, (x, y) in enumerate(zip(a, b)): bad += deep_same(x, y, tol, f"{pre}[{i}]")
    elif isinstance(a, (bool, str)) or isinstance(b, (bool, str)) or a is None or b is None:
        if a != b: bad.append(pre)
    elif abs(a - b) > tol * max(1.0, abs(b)): bad.append(pre)
    return bad
J = lambda o: json.loads(json.dumps(o, default=float))
bada = deep_same(J(g0), BS1J["grade"]); badm = deep_same(J(mw0), BS1J["mw"]); badd = deep_same(J(dw0), BS1J["dwarfs"])
ka, km, kd = not bada, not badm, not badd; bada, badm, badd = bada[:5], badm[:5], badd[:5]
check("K0a_BS1_base", ka and km and kd, f"GT off reproduces BS1's committed primary block to 1e-6: grade {ka} {bada or ''}, MW {km} {badm or ''}, field dwarfs {kd} {badd or ''}; "
      f"canonical fails {g0['canonical']['fails'] or 'none'}; alt fails {g0['alt']['fails']}")
HO1J = json.load(open(os.path.join(REB, "HO1_xcop_hotgas_heldout", "ho1_heldout_results.json")))["footings"]
dho = max(abs(r43b["_gt"]["hg2"][f]["D_base"] - HO1J[f]["hg2"]["D_pred"]) for f in FEET)
check("K0b_HO1_Dpred", dho < 1e-6 and hg2_id, f"GT off reproduces HO1(b) D_pred " + " / ".join(f"{r43b['_gt']['hg2'][f]['D_base']:+.4f}" for f in FEET) + f" (HO1 +0.229 / +0.201): max |d| {dho:.1e}")
IB1J = json.load(open(os.path.join(REB, "IB1_inner_band_hse", "ib1_hse_halo_results.json")))["footings"]
ib_t = call(B["run_x43_ib1"], "terc", LAB("ib1_hg_tercile"))[0]; ib_r = call(B["run_x43_ib1"], "rf", LAB("ib1_rf"))[0]
dib = max(max(abs(ib_t["cells"][f][h][k][q] - IB1J[f]["cells"][h][k][q]), abs(ib_r["cells"][f][h][k][q] - IB1RF[f]["cells"][h][k][q])) for f in FEET for h in HKS for k in IB1J[f]["cells"][h] for q in ("pred", "Z"))
dco = max(abs(ib_r["co"][0] - IB1RF["fit"]["a"]), abs(ib_r["co"][1] - IB1RF["fit"]["b"]))
m3 = [ib_t["cells"]["canonical"][h]["G-OUT-M3"]["Z"] for h in HKS]
check("K0c_IB1_HG", dib < 1e-6 and dco < 1e-12, f"IB1's configuration (A1) reproduces IB1 HG (tercile) and RF cells, 15 keys x 2 h x 2 footings, pred and Z: max |d| {dib:.1e}; "
      f"G-OUT-M3 Z {m3[0]:+.2f} / {m3[1]:+.2f}; RF fit (a, b) |d| {dco:.1e}")
RES["K0"] = dict(base_fails={f: g0[f]["fails"] for f in FEET}, D_base={f: r43b["_gt"]["hg2"][f]["D_base"] for f in FEET}, ib1_maxdiff=dib, ib1_m3=m3)
if not all(v for _, v in checks) and not MUTATE:
    P("STOPPED AT STEP 0"); RES["verdict"] = "STOPPED AT STEP 0"; RES["checks"] = dict(checks)
    open(os.path.join(HERE, f"gt1_gas_temperature_halo{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
    json.dump(RES, open(os.path.join(HERE, f"gt1_gas_temperature_halo_results{TAG}.json"), "w"), indent=1, default=float, sort_keys=True); sys.exit(1)

# ================================================================== GT runs (primary + reported variants)
RUNS = {}
VARS = [("primary", dict(Rg="R500", offset=False, fill="rf")), ("Rg_0.7R500", dict(Rg="0.7R500", offset=False, fill="rf")),
        ("Rg_rta_half", dict(Rg="rta2", offset=False, fill="rf")), ("continuity_offset", dict(Rg="R500", offset=True, fill="rf")),
        ("tercile_fill", dict(Rg="R500", offset=False, fill="terc")), ("literal_Rg_rta_k_unused", dict(Rg="rta", offset=False, fill="rf"))]
for name, cfg in VARS:
    GTCFG.update(on=True, name=name, **cfg)
    RUNS[name] = call(B["run_x43"], 4.0, PRIM["T"], LAB("GT_" + name))[0]
    P(f"  GT run {name} done [{time.time() - T0:.0f} s]")
CL2C = {f: BS1J["grade"][f]["clusters"] for f in FEET}
def summ(run, f):
    c = run["footings"][f]["clusters"]; lg = run["_gt"]["log"]; ks = [x for hk in HKS for x in lg.get(f"{f}|{hk}", [])]
    k0 = [x for x in lg.get(f"{f}|h0672", [])]
    kv = np.array([x["k"] for x in k0 if np.isfinite(x["k"])])
    return dict(cells={h: c["cells"][h] for h in HKS}, ok=c["ok"], fails=c["fails"],
                n_clamped=int(sum(x["clamp"] for x in k0)), n_empty=int(sum(x["empty"] for x in k0)), n_below_switch=int(sum(not x["above"] for x in ks)),
                k_median=float(np.median(kv)) if len(kv) else None, k_16_84=[float(np.percentile(kv, 16)), float(np.percentile(kv, 84))] if len(kv) else None,
                k_kt_median=float(np.median([x["k"] for x in k0 if x["kt"] and np.isfinite(x["k"])])) if len(kv) else None,
                k_fill_median=float(np.median([x["k"] for x in k0 if (not x["kt"]) and np.isfinite(x["k"])])) if len(kv) else None,
                excess_median=float(np.median([x["excess"] for x in k0])), excess_clamped=[x["excess"] for x in k0 if x["clamp"]],
                MHG_over_MCL2_at_Rg_median=float(np.median([x["MHG_R500_over_MCL2"] for x in k0])), Rg_over_rta_median=float(np.median([x["Rg_over_rta"] for x in k0])),
                bins=run["_gt"]["bin_pred_over_meas"].get(f"{f}|h0672"), hg2=run["_gt"]["hg2"][f])
GT = {name: {f: summ(RUNS[name], f) for f in FEET} for name, _ in VARS}

# ---- checks K1, K2 (all GT runs), base identity of non-hot lines
e1 = max(x["e_k1"] for r in RUNS.values() for v in r["_gt"]["log"].values() for x in v)
e1g = max(r["_gt"]["hg2"][f]["k1_maxrel"] for r in RUNS.values() for f in FEET)
same_nonhot = all(RUNS[n]["footings"][f]["sparc"][t]["rms"] == r43b["footings"][f]["sparc"][t]["rms"] and RUNS[n]["footings"][f]["sparc"][t]["U_median"] == r43b["footings"][f]["sparc"][t]["U_median"]
                  and RUNS[n]["footings"][f]["groups"]["Z"] == r43b["footings"][f]["groups"]["Z"] and RUNS[n]["footings"][f]["groups"]["mean"] == r43b["footings"][f]["groups"]["mean"]
                  for n in RUNS for f in FEET for t in r43b["footings"][f]["sparc"])
faint_same = all(RUNS[n]["_gt"]["hg2"][f]["faint_identical"] for n in RUNS for f in FEET)
ncl = sum(len(v) for v in RUNS["primary"]["_gt"]["log"].values())
k1 = e1 < 1e-9 and e1g < 1e-9 and same_nonhot and faint_same and ncl == 2 * 2 * 326
check("K1", k1, f"hot systems M_tot(R_g) = M_HG(R_g) (and inner grid): clusters max rel {e1:.1e}, BRIGHT groups {e1g:.1e} (1e-9); "
      f"non-hot lines equal base exactly: SPARC + 63 groups {same_nonhot}, FAINT g_pred {faint_same}; cluster profiles logged {ncl}")
e2 = [x["e_k2"] for r in RUNS.values() for v in r["_gt"]["log"].values() for x in v if x["e_k2"] is not None]
e2g = max(r["_gt"]["hg2"][f]["k2_maxrel"] for r in RUNS.values() for f in FEET)
noff = sum(not x["on_grid"] for r in RUNS.values() for v in r["_gt"]["log"].values() for x in v)
k2 = (max(e2) if e2 else 0.0) < 1e-6 and e2g < 1e-6
check("K2", k2, f"k > 0 systems reach M_budget at r_ta: clusters max rel {max(e2) if e2 else 0:.1e} over {len(e2)} profiles ({noff} with r_ta beyond the grid, analytic), BRIGHT groups {e2g:.1e} (1e-6)")

# ================================================================== grade (frozen verdict table, A6)
with contextlib.redirect_stdout(io.StringIO()):
    gG = B["grade"](RUNS["primary"], F53on, F53off, r51["RES"], "GT primary", quiet=True)
CLKEYS = list(GT["primary"]["canonical"]["cells"]["h0672"])
VER = {}
for f in FEET:
    s = GT["primary"][f]; A = all(s["ok"].values())
    Dg = s["hg2"]["D_gt"]; Bp = LO0 <= Dg <= HI0
    nonclu = [x for x in gG[f]["fails"] if not x.startswith("G-")]
    Cp = bool(dict(checks)["K0a_BS1_base"]) and not nonclu and mw0[f]["n_L1_L2a_L2b"] > 0
    if A and Bp and Cp: v = "GAS-STATE RULE HOLDS"
    elif A and Cp: v = "GAS-STATE RULE FIXES CLUSTERS ONLY"
    elif Bp and Cp: v = "GAS-STATE RULE FIXES GROUP SIGN ONLY"
    else:
        lines = ([] if A else ["clusters (" + ", ".join(s["fails"]) + ")"]) + ([] if Bp else [f"HG2 D_pred {Dg:+.3f} ({'ABOVE' if Dg > HI0 else 'BELOW'} [{LO0:+.3f}, {HI0:+.3f}])"]) \
                + ([] if Cp else ["base lines (" + ", ".join(nonclu + ([] if mw0[f]["n_L1_L2a_L2b"] > 0 else ["Milky Way"])) + ")"])
        v = "GAS-STATE RULE FAILS: " + "; ".join(lines)
    VER[f] = dict(verdict=v, A_clusters=A, B_group_sign=Bp, C_base=Cp, D_pred=Dg, nonclu_fails=nonclu)

# ================================================================== report
for f in FEET:
    s = GT["primary"][f]
    P(f"\n=== [{f}] GT primary (R_g = R500, k-scaled CL2 profile to the GS1 budget, RF sigma fill)")
    P("  cluster keys (h 0.672 | h 0.686): meas, GT pred, Z | Z   [CL2/BS1 Z h0.672 | IB1-HG Z h0.672]")
    for k in CLKEYS:
        a, b = s["cells"]["h0672"][k], s["cells"]["h0686"][k]
        P(f"   {k:10s} {a['meas']:+.3f}+-{a['s']:.3f} pred {a['pred']:+.3f} Z {a['Z']:+.2f} | {b['Z']:+.2f}  {'pass' if s['ok'][k] else 'FAIL'}   "
          f"[CL2 {CL2C[f][k]['Z']:+.2f} | IB1 {IB1J[f]['cells']['h0672'][k]['Z']:+.2f}]")
    P(f"  k (h0.672): median {s['k_median']:.3f} [16-84% {s['k_16_84'][0]:.3f}-{s['k_16_84'][1]:.3f}] (KT {s['k_kt_median']:.3f}, filled {s['k_fill_median']:.3f}); "
      f"clamped at k = 0: {s['n_clamped']} of 326 (excess M_HG(R_g)/M_budget of clamped: {', '.join(f'{x:.2f}' for x in sorted(s['excess_clamped'])) or 'none'}); "
      f"median M_HG(R500)/M_CL2(R500) {s['MHG_over_MCL2_at_Rg_median']:.2f}; median R500/r_ta {s['Rg_over_rta_median']:.3f}; below switch {s['n_below_switch']}")
    P("  per-bin pred/meas h0.672, bins 0-7: " + " ".join(f"{x:.2f}" for x in s["bins"]) + "   (base: " + " ".join(f"{x:.2f}" for x in r43b["_gt"]["bin_pred_over_meas"][f"{f}|h0672"]) + ")")
    h = s["hg2"]
    P(f"  HG2: D_pred {h['D_gt']:+.3f} (BRIGHT {h['n_bright_gt']} / FAINT {h['n_faint_gt']}) vs measured 95% [{LO0:+.3f}, {HI0:+.3f}]  (base {h['D_base']:+.3f})")
    P("    BRIGHT groups: " + "; ".join(f"{x['name']} s {x['sigma']:.0f} r/R500 {x['r_over_R500']:.2f} k {x['k']:.2f}{' CLAMP' if x['clamp'] else ''} dlog g {x['dlog_g']:+.2f}" for x in h["info"]))
    P(f"  base lines: {'reproduce BS1 (K0a)' if dict(checks)['K0a_BS1_base'] else 'DO NOT reproduce BS1'}; non-cluster fails: {VER[f]['nonclu_fails'] or 'none'}; MW cells L1+L2a+L2b {mw0[f]['n_L1_L2a_L2b']}; "
      f"field dwarfs (open item, not in C): {dw0[f]['isolated']['verdict']}" + (f", IC 1613 Z {dw0[f]['flags']['IC 1613']['Z']:+.2f}"))
    P(f"  VERDICT [{f}]: {VER[f]['verdict']}   (A {VER[f]['A_clusters']}, B {VER[f]['B_group_sign']}, C {VER[f]['C_base']})")
P("\n=== REPORTED VARIANTS (not graded)")
for name, _ in VARS[1:]:
    for f in FEET:
        s = GT[name][f]
        P(f"  {name} [{f}]: cluster fails {s['fails'] or 'none'}; G-OUT-M3 Z {s['cells']['h0672']['G-OUT-M3']['Z']:+.2f}/{s['cells']['h0686']['G-OUT-M3']['Z']:+.2f}, "
          f"G-IN-Mall {s['cells']['h0672']['G-IN-Mall']['Z']:+.2f}, G-OUT-all {s['cells']['h0672']['G-OUT-all']['Z']:+.2f}; clamped {s['n_clamped']}, empty {s['n_empty']}; "
          f"HG2 D_pred {s['hg2']['D_gt']:+.3f}")
xc = RUNS["primary"]["_gt"]["xcop"]
P(f"\nK4 X-COP construction residual inside R500 (35 points; reported, not graded): mean {xc['mean']:+.3f} dex, rms {xc['rms']:.3f}; per radius "
  + ", ".join(f"{k} R500 {v:+.3f}" for k, v in xc["by_x"].items()) + "; per cluster " + ", ".join(f"{k} {v:+.3f}" for k, v in xc["per_cluster"].items())
  + f"   [base (HO1): mean {HO1J['canonical']['xcop']['mean']:+.3f}, rms {HO1J['canonical']['xcop']['rms']:.3f}]")
HO2J = json.load(open(os.path.join(REB, "HO2_sluggs_milkyway_heldout", "ho2_heldout_results.json")))["sluggs"]
P("SLUGGS centrals: NOT A TEST (no X-ray kT on disk; the stellar sigma would make M_HG a Jeans mass of the graded kinematics). Base picture (HO2, unchanged under BS1): "
  + "; ".join(f"{f} {HO2J[f]['cls']}, mean {HO2J[f]['cl2']['mean']:+.3f} dex, {HO2J[f]['cl2']['n_cleared']} of 4 clear" for f in FEET))
check("K3", rss_all() < 1.0, f"peak RSS {rss_all():.2f} GB (max over processes), one thread")

RES.update(verdict={f: VER[f]["verdict"] for f in FEET}, verdict_detail=VER, GT=GT, xcop_K4=xc, xcop_sigma=XSIG,
           base=dict(grade=g0, mw=mw0, field_dwarfs={f: dict(verdict=dw0[f]["isolated"]["verdict"], IC1613_Z=dw0[f]["flags"]["IC 1613"]["Z"]) for f in FEET},
                     bins={k: v for k, v in r43b["_gt"]["bin_pred_over_meas"].items()}),
           compare=dict(CL2_BS1=CL2C, IB1_HG={f: IB1J[f]["cells"] for f in FEET}),
           k_per_cluster_primary_canonical_h0672=[x["k"] for x in RUNS["primary"]["_gt"]["log"]["canonical|h0672"]],
           sluggs_base=dict(note="NOT A TEST", **{f: dict(cls=HO2J[f]["cls"], mean=HO2J[f]["cl2"]["mean"]) for f in FEET}),
           hg2_interval=[LO0, HI0])
RES["checks"] = dict(checks); n = sum(v for _, v in checks)
P(f"\n=== VERDICT (frozen; canonical primary): {VER['canonical']['verdict']}\n=== alt (its own): {VER['alt']['verdict']}")
P(f"checks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks) + f"; runtime {time.time() - T0:.0f} s")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
open(os.path.join(HERE, f"gt1_gas_temperature_halo{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
json.dump(clean(RES), open(os.path.join(HERE, f"gt1_gas_temperature_halo_results{TAG}.json"), "w"), indent=1, sort_keys=True)
for fn in ("gt1_x43copy.py", "gt1_x53copy.py", "gt1_x51copy.py", "gt1_x43copy_ib1.py"):
    try: os.remove(os.path.join(HERE, fn))
    except OSError: pass
sys.exit(0 if n == len(checks) else 1)
