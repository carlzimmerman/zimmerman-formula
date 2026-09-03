#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h30_warp_onset.py -- HUNT ITEM 30: where do HI warps begin?
===========================================================
The hunt list's claim: "warps begin where the EFE takes over (Brada-Milgrom)", i.e. the warp onset radius should
track r_EFE = sqrt(G M_b/(e_N a_0)) = r_M/sqrt(e_N), with r_M = sqrt(G M_b/a_0) = v_flat^2/a_0 and e_N the
Newtonian external field in units of a_0.  Kepler-grade if the onset radius tracks r_EFE with scatter < 0.15 dex.
The standard alternative is that a warp begins at the EDGE OF THE STELLAR DISC -- Briggs' (1990) rules of behaviour
and van der Kruit's truncation picture -- which is a purely baryonic scale that knows nothing about the environment.

TWO CORRECTIONS TO THE LIST, BOTH FOUND WHILE BUILDING THIS
  1. The list cites "van Eymeren+11" for warp catalogues.  Those two papers (A&A 530, A29 and A30) are about
     LOPSIDEDNESS in WHISP galaxies, not warps.  They contain no warp onset radii.
  2. Garcia-Ruiz, Sancisi & Kuijken 2002 (A&A 394, 769), the paper the list actually wants, does NOT tabulate the
     per-galaxy warp radius -- it is only in their figures.  The numbers used here come instead from van der Kruit
     2007 (A&A 466, 883) Table 3, which measured R_warp on the sky for the same WHISP edge-on sample and prints it.

DATA (transcribed by hand this session into real_research/data/warps/, every number as printed):
  whisp_edgeon_warps.tsv       26 edge-on WHISP galaxies: R25, R_opt, inclination, two distance estimates, R_HI,
                               M_HI, W20, W50, warp angles and environment class (Garcia-Ruiz+2002 Tables 1 and 4);
                               R_deep (stellar truncation radius) and R_warp (van der Kruit 2007 Table 3).
  whisp_edgeon_companions.tsv  nearest catalogued companion of each, projected (Garcia-Ruiz+2002 Table 7).

THE CAVEAT THAT SIZES EVERYTHING, STATED FIRST
  R_warp is measured AS PROJECTED ON THE SKY and is therefore a LOWER limit on the in-plane onset radius; van der
  Kruit's own statistical deprojection puts the intrinsic value near 1.1 R_max.  A projection factor is a single
  multiplicative constant, so it moves every ratio's MEDIAN and leaves its SCATTER alone -- which is why the
  scatter comparison below is the load-bearing statistic and the median is quoted with that factor attached.
Both footings.  Mutation controls.  Checks CAN fail.

ROBUSTNESS ARM added on the audit pass (check 30e): van der Kruit's own clean statistic is 12 galaxies, not the 16
used here -- he requires a DETECTED truncation (three of the sixteen have none, so their R_deep is only an apparent
disc size) and he explicitly removes UGC 5986, 7125 and 8246 as disturbed.  The arm cuts to his selection and asks
whether the disc-edge result was an artefact of the looser sample.  It was not: every baryonic scale gets TIGHTER
and the MOND radius stays two to three times worse, so the negative verdict survives its own strictest cut.
"""
import sys, math, os
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(3007)
WD = os.path.join(DATA, "warps")
ARCMIN = math.pi/180.0/60.0
SIG_TURB = 10.0                     # km/s, the usual turbulent broadening removed from W50 in quadrature

def load(path, key="UGC"):
    rows = [l.rstrip("\n").split("\t") for l in open(path) if l.strip() and not l.startswith("#")]
    hdr = [h.strip() for h in rows[0]]
    out = {}
    for r in rows[1:]:
        d = dict(zip(hdr, r))
        out[d[key].strip()] = d
    return out

def f(v):
    try: return float(v)
    except Exception: return float("nan")

P("="*118); P("ITEM 30 -- the HI warp onset radius, against the MOND external-field radius and against the disc edge"); P("="*118)
W = load(os.path.join(WD, "whisp_edgeon_warps.tsv"))
C = load(os.path.join(WD, "whisp_edgeon_companions.tsv"))
info(f"WHISP edge-on sample: {len(W)} galaxies; {sum(1 for k in W if np.isfinite(f(W[k]['Rwarp_arcmin'])))} have a published "
     f"warp onset radius, {sum(1 for k in W if W[k]['flag']=='nowarp')} are classed as unwarped or unmeasurable")

gal = []
for k, d in W.items():
    rw = f(d["Rwarp_arcmin"])
    if not np.isfinite(rw) or d["flag"] != "ok": continue
    inc = f(d["inc_deg"]); W50 = f(d["W50_kms"])
    si = math.sin(math.radians(min(inc, 89.9)))
    vhw = 0.5*W50
    v = math.sqrt(max(vhw**2 - SIG_TURB**2, 1.0))/si                 # km/s, deprojected flat rotation speed
    D_V, D_TF = f(d["dV_Mpc"]), f(d["dTF_Mpc"])
    g = dict(name=k, inc=inc, v=v, W50=W50, D_V=D_V, D_TF=D_TF, env=int(f(d["env"])),
             th_warp=rw, th_25=f(d["R25_arcmin"]), th_opt=f(d["Ropt_arcmin"]),
             th_HI=f(d["RHI_arcmin"]), th_deep=f(d["Rdeep_arcmin"]), MHI=f(d["MHI_1e8"])*1e8)
    c = C.get(k, {})
    g["d_comp"] = f(c.get("d_comp_arcmin", "nan")); g["n_comp"] = f(c.get("n_comp", "nan"))
    g["trunc"] = d.get("trunc", "").strip(); g["dist"] = d.get("vdk_disturbed", "0").strip() == "1"
    g["vdk_clean"] = (g["trunc"] == "yes") and (not g["dist"])
    gal.append(g)
info(f"analysed: {len(gal)} galaxies with a clean published warp onset radius")
info(f"of these, {sum(1 for g in gal if g['vdk_clean'])} are in van der Kruit's OWN clean statistic (a detected truncation "
     f"AND not one of the three systems he removes as disturbed); "
     f"{sum(1 for g in gal if g['trunc']!='yes')} have NO detected truncation, so their R_deep is only an apparent disc size, "
     f"and {sum(1 for g in gal if g['dist'])} are systems he excludes -- both kept in the headline numbers below and "
     f"stripped out again in the robustness arm at the end")
info(f"deprojected flat speeds v = sqrt((W50/2)^2 - ({SIG_TURB:g})^2)/sin i: median {np.median([g['v'] for g in gal]):.0f} km/s, "
     f"range {min(g['v'] for g in gal):.0f} - {max(g['v'] for g in gal):.0f}")

# ---------------------------------------------------------------- a check on the mass scale that CAN fail
for g in gal:
    g["Mb_btfr"] = {ft: (g["v"]*1e3)**4/(G*A0[ft])/Msun for ft in A0}
    g["Mgas"] = 1.33*g["MHI"]
rat = np.array([g["Mb_btfr"]["canonical"]/g["Mgas"] for g in gal])
info(f"consistency check on the masses: the BTFR mass implied by v_flat is {np.median(rat):.1f}x the atomic-gas mass "
     f"(16-84%: {np.percentile(rat,16):.1f} - {np.percentile(rat,84):.1f}); for late-type discs the stars carry most of the "
     f"baryons, so a factor of a few is expected and a factor of 100 would mean the speeds or the gas masses are wrong")
ck("30a the BTFR mass and the measured gas mass are consistent to within the stellar contribution, so v_flat and the distances "
   "are not grossly wrong before any warp statistic is computed",
   2.0 < np.median(rat) < 30.0,
   f"median M_b(BTFR)/M_gas = {np.median(rat):.1f} on canonical, {np.median([g['Mb_btfr']['alt']/g['Mgas'] for g in gal]):.1f} on alt")

# ---------------------------------------------------------------- the scales the onset might track
def scatter(x):
    x = np.asarray([v for v in x if np.isfinite(v) and v > 0])
    return float(np.std(np.log10(x), ddof=1)), float(np.median(x)), len(x)

def build(dist_key, foot):
    out = {}
    D = np.array([g[dist_key] for g in gal])
    thw = np.array([g["th_warp"] for g in gal])
    rw = thw*ARCMIN*D*1000.0                                              # kpc
    rM = np.array([(g["v"]*1e3)**2/A0[foot]/kpc for g in gal])             # kpc, distance-free
    out["R_deep (stellar truncation)"] = thw/np.array([g["th_deep"] for g in gal])
    out["R_25 (optical radius)"] = thw/np.array([g["th_25"] for g in gal])
    out["R_opt (visual disc edge)"] = thw/np.array([g["th_opt"] for g in gal])
    out["R_HI (1 Msun/pc^2)"] = thw/np.array([g["th_HI"] for g in gal])
    out["r_M = v^2/a_0 (MOND radius)"] = rw/rM
    return out, rw, rM

info("")
info(f"{'candidate scale for the warp onset':34} {'N':>3} {'median ratio':>13} {'log scatter (dex)':>18}")
TAB = {}
for foot in ("canonical",):
    for dk, dn in (("D_V", "Virgocentric"),):
        ratios, rw, rM = build(dk, foot)
        for nm, v in ratios.items():
            s, m, n = scatter(v)
            TAB[nm] = (m, s, n)
            info(f"{nm:34} {n:3d} {m:13.3f} {s:18.3f}")
info("(the first four are distance-free ratios of two angles; only the MOND radius needs a distance)")

# ---------------------------------------------------------------- the external field, two independent estimates
info("")
M_COMP = 1e10                                                            # Msun, fiducial companion baryonic mass
for g in gal:
    if np.isfinite(g["d_comp"]) and g["d_comp"] > 0:
        d_m = g["d_comp"]*ARCMIN*g["D_V"]*Mpc                            # projected separation, metres (a LOWER limit)
        g["gN_comp"] = G*M_COMP*Msun/d_m**2
    else:
        g["gN_comp"] = float("nan")
eN_comp = {ft: np.array([g["gN_comp"]/A0[ft] for g in gal]) for ft in A0}
ok = np.isfinite(eN_comp["canonical"])
info(f"external field from the nearest catalogued companion, assuming a fiducial baryonic mass of {M_COMP:.0e} Msun and the "
     f"PROJECTED separation (both of which make this an UPPER limit): e_N median {np.nanmedian(eN_comp['canonical'][ok]):.2e}, "
     f"max {np.nanmax(eN_comp['canonical'][ok]):.2e} over {ok.sum()}/{len(gal)} galaxies with a companion")
E_LSS = {"canonical": 4.57e-3, "alt": 3.78e-3}                            # WALLABY median e_N incl. cluster term, h28
E_LSS_NC = {"canonical": 5.52e-4, "alt": 4.57e-4}                         # ... without it
info(f"large-scale-structure field for comparison: the committed 2M++/MCXC calculation for 237 WALLABY galaxies "
     f"(prep_2026/wallaby_firing/gext_wallaby_237.csv) gives a median e_N of {E_LSS['canonical']:.2e} with the cluster term "
     f"and {E_LSS_NC['canonical']:.2e} without it, on canonical")

# ---------------------------------------------------------------- what e_N the EFE-onset hypothesis REQUIRES
info("")
R30 = {}
for foot in ("canonical", "alt"):
    ratios, rw, rM = build("D_V", foot)
    eN_req = (rM/rw)**2                                                  # r_EFE = r_M/sqrt(e_N) = r_warp
    rE_lss = rM/math.sqrt(E_LSS[foot])
    s_req, m_req, _ = scatter(eN_req)
    s_efe, m_efe, n_efe = scatter(rw/rE_lss)
    over_lss = float(np.median(eN_req))/E_LSS[foot]
    ovc = np.array([e/max(g["gN_comp"]/A0[foot], 1e-30) for e, g in zip(eN_req, gal) if np.isfinite(g["gN_comp"])])
    info(f"[{foot}] to put the EFE radius AT the observed warp onset, the external field would have to be "
         f"e_N = {np.median(eN_req):.3f} (16-84%: {np.percentile(eN_req,16):.3f} - {np.percentile(eN_req,84):.3f})")
    info(f"[{foot}]   that is {over_lss:.0f}x the large-scale-structure field these galaxies actually sit in, and "
         f"{np.median(ovc):.0f}x the UPPER limit from their nearest catalogued companion")
    info(f"[{foot}]   equivalently, with the real field the EFE radius sits at r_EFE = {np.median(rE_lss):.0f} kpc while the "
         f"warp starts at {np.median(rw):.1f} kpc: r_warp/r_EFE = {m_efe:.3f} with {s_efe:.3f} dex scatter")
    R30[foot] = dict(eN_req=eN_req, m_efe=m_efe, s_efe=s_efe, over_lss=over_lss, over_comp=float(np.median(ovc)),
                     rw=rw, rM=rM, rE=rE_lss)

# ---------------------------------------------------------------- the acceleration at the warp onset
info("")
vv = np.array([g["v"] for g in gal])
for foot in ("canonical", "alt"):
    y = R30[foot]["rM"]/R30[foot]["rw"]                                   # v^2/(r_warp a_0) = g_obs(r_warp)/a_0
    sl = np.polyfit(np.log10(vv), np.log10(y), 1)[0]
    bs = np.std([np.polyfit(np.log10(vv[i]), np.log10(y[i]), 1)[0]
                 for i in (rng.integers(0, len(vv), len(vv)) for _ in range(2000))])
    info(f"[{foot}] the acceleration where the warp begins is g_obs(r_warp) = {np.median(y):.2f} a_0 "
         f"(16-84%: {np.percentile(y,16):.2f} - {np.percentile(y,84):.2f}), scatter {np.std(np.log10(y), ddof=1):.3f} dex, "
         f"with a rotation-speed trend of {sl:+.2f} +- {bs:.2f} dex per dex")
    R30[foot]["y_med"] = float(np.median(y)); R30[foot]["y_sc"] = float(np.std(np.log10(y), ddof=1))
    R30[foot]["y_sl"] = float(sl); R30[foot]["y_sle"] = float(bs)
info("so warps do begin near the MOND transition -- but three times less tightly than they track the stellar disc's edge, and")
info("with a residual mass trend, so this is a restatement of the disc-edge result and not an independent a_0 law.")

# ---------------------------------------------------------------- mutation control
thw = np.array([g["th_warp"] for g in gal])
def shuffled_scatter(num, den, n=4000):
    out = np.empty(n)
    for i in range(n):
        out[i] = np.std(np.log10(rng.permutation(num)/den), ddof=1)
    return float(np.mean(out)), float(np.std(out))
den_deep = np.array([g["th_deep"] for g in gal])
den_rM = R30["canonical"]["rM"]/(ARCMIN*np.array([g["D_V"] for g in gal])*1000.0)     # rM expressed as an angle
m_sh_d, s_sh_d = shuffled_scatter(thw, den_deep)
m_sh_m, s_sh_m = shuffled_scatter(thw, den_rM)
s_deep = TAB["R_deep (stellar truncation)"][1]; s_rM = TAB["r_M = v^2/a_0 (MOND radius)"][1]
info("")
info(f"MUTATION 1 (shuffle which warp radius belongs to which galaxy, 4000 draws): the truncation-radius ratio's scatter goes "
     f"from {s_deep:.3f} to {m_sh_d:.3f} +- {s_sh_d:.3f} dex ({(m_sh_d - s_deep)/s_sh_d:.1f} sigma of improvement over chance); "
     f"the MOND-radius ratio's goes from {s_rM:.3f} to {m_sh_m:.3f} +- {s_sh_m:.3f} ({(m_sh_m - s_rM)/s_sh_m:.1f} sigma)")
info("MUTATION 2 (a_0 x 100): r_M shrinks by 100, so the MEDIAN of r_warp/r_M moves by 2 dex while its SCATTER is unchanged --")
info("  a scale-free statistic cannot see a_0.  Only the median can, which is why both are reported and why the scatter")
info("  comparison alone would be a_0-blind.  Stated so the scatter result is not over-read.")
r2 = np.std(np.log10(R30["canonical"]["rw"]/(R30["canonical"]["rM"]/100.0)), ddof=1)
info(f"  check: scatter with a_0 x 100 = {r2:.3f} dex, identical to {s_rM:.3f}; median moves from "
     f"{TAB['r_M = v^2/a_0 (MOND radius)'][0]:.2f} to {np.median(R30['canonical']['rw']/(R30['canonical']['rM']/100.0)):.1f}")
ck("30b MUTATION CONTROLS behave: shuffling the warp radii between galaxies degrades every ratio's scatter, so the ratios do "
   "carry real per-galaxy information, and multiplying a_0 by 100 leaves the scatter statistic untouched -- which is exactly "
   "why the median is reported alongside it",
   m_sh_d > s_deep and abs(r2 - s_rM) < 1e-6,
   f"truncation ratio {s_deep:.3f} -> {m_sh_d:.3f} dex when shuffled; MOND ratio {s_rM:.3f} -> {m_sh_m:.3f}; "
   f"a_0 x100 leaves the MOND-ratio scatter at {r2:.3f}")

# ---------------------------------------------------------------- distance systematic
ratios_TF, rw_TF, rM_TF = build("D_TF", "canonical")
s_TF = np.std(np.log10(rw_TF/rM_TF), ddof=1)
info(f"distance systematic: swapping the Virgocentric-flow distances for the Tully-Fisher ones changes the r_warp/r_M scatter "
     f"from {s_rM:.3f} to {s_TF:.3f} dex and the median from {TAB['r_M = v^2/a_0 (MOND radius)'][0]:.2f} to "
     f"{np.median(rw_TF/rM_TF):.2f}.  The four angle ratios are distance-free and are untouched by this.")
dv = np.array([g["D_V"] for g in gal]); dt = np.array([g["D_TF"] for g in gal])
sd = float(np.std(np.log10(dv/dt), ddof=1)/math.sqrt(2.0))
s_rM_deconv = math.sqrt(max(s_rM**2 - sd**2, 0.0))
info(f"FAIRNESS CONTROL, because the comparison is not symmetric: the four disc-edge ratios are ratios of two ANGLES and carry "
     f"no distance error, while r_warp/r_M needs a distance.  The two independent distance estimates for these galaxies differ "
     f"by {np.std(np.log10(dv/dt), ddof=1):.3f} dex, i.e. about {sd:.3f} dex of error each.  Removing that in quadrature still "
     f"leaves the MOND-radius ratio at {s_rM_deconv:.3f} dex, more than twice the truncation ratio's {s_deep:.3f}, so the "
     f"conclusion is not an artefact of the distances.")

# ================================================================================================================
# ROBUSTNESS ARM, added on the audit pass: van der Kruit's OWN clean subsample
# ================================================================================================================
# Reading the source table again turned up two things the headline sample does not respect, both of which cut
# AGAINST the disc-edge comparison being made fairly and therefore have to be tested:
#   (1) four of the sixteen galaxies (UGC 6283, 7090, 8396, and on the other side 1281 which is excluded already)
#       have NO detected truncation, so their "R_deep" is only the apparent disc size at the deep clip level and
#       is not the truncation radius R_max that the disc-edge hypothesis is about;
#   (2) van der Kruit explicitly removes UGC 5986, 7125 and 8246 from his own statistics as disturbed systems,
#       and two of those three are in the sixteen.
# His clean statistic is 12 galaxies.  If the disc-edge result is an artefact of including the four ill-defined
# ones, restricting to his twelve should DEGRADE it.  This arm is therefore a check that can fail against the
# conclusion this script already drew, not a way to make it look better.
info("")
info("-"*114)
info("ROBUSTNESS ARM: van der Kruit's own clean subsample (a detected truncation, and none of his disturbed systems)")
info("-"*114)
keep = np.array([g["vdk_clean"] for g in gal])
info(f"restricting {len(gal)} -> {int(keep.sum())} galaxies; dropped for no truncation: "
     + ", ".join(f"UGC {g['name']}" for g in gal if g["trunc"] != "yes")
     + "; dropped as disturbed: " + ", ".join(f"UGC {g['name']}" for g in gal if g["dist"]))
info(f"  van der Kruit's own clean statistic is 12 -- these {int(keep.sum())} plus UGC 1281, whose R_warp he prints with a "
     f"question mark and which this script excludes on its own 'uncertain' flag before any of this.  Stated so the two "
     f"counts are not confused: {int(keep.sum())} is a subset of his 12, not a different selection.")
sub_th = np.array([g["th_warp"] for g in gal])[keep]
CLEAN = {}
for nm, den in (("R_deep (stellar truncation)", np.array([g["th_deep"] for g in gal])),
                ("R_25 (optical radius)", np.array([g["th_25"] for g in gal])),
                ("R_opt (visual disc edge)", np.array([g["th_opt"] for g in gal])),
                ("R_HI (1 Msun/pc^2)", np.array([g["th_HI"] for g in gal]))):
    s, m, n = scatter(sub_th/den[keep]); CLEAN[nm] = (m, s, n)
s_rM_c, m_rM_c, n_rM_c = scatter((R30["canonical"]["rw"]/R30["canonical"]["rM"])[keep])
CLEAN["r_M = v^2/a_0 (MOND radius)"] = (m_rM_c, s_rM_c, n_rM_c)
info(f"{'candidate scale':34} {'N':>3} {'median':>9} {'scatter':>9}   {'vs full sample':>16}")
for nm in ("R_deep (stellar truncation)", "R_25 (optical radius)", "R_opt (visual disc edge)",
           "R_HI (1 Msun/pc^2)", "r_M = v^2/a_0 (MOND radius)"):
    m, s, n = CLEAN[nm]
    info(f"{nm:34} {n:3d} {m:9.3f} {s:9.3f}   {TAB[nm][1]:6.3f} -> {s:.3f} dex")
s_efe_c, m_efe_c, _ = scatter((R30["canonical"]["rw"]/R30["canonical"]["rE"])[keep])
eNreq_c = R30["canonical"]["eN_req"][keep]
info(f"on this clean subsample the EFE picture is UNCHANGED: r_warp/r_EFE = {m_efe_c:.3f} with {s_efe_c:.3f} dex, and the "
     f"external field needed to put r_EFE at the warp onset is still e_N = {np.median(eNreq_c):.3f}, "
     f"{np.median(eNreq_c)/E_LSS['canonical']:.0f}x the large-scale-structure field.")
info(f"and van der Kruit's own published ratio for these same galaxies, R_warp/R_max, has a median of "
     f"{np.median([f(W[g['name']]['Rwarp_over_Rmax']) for g in gal if g['vdk_clean'] and np.isfinite(f(W[g['name']]['Rwarp_over_Rmax']))]):.2f} "
     f"-- an independent check that this script's angle ratio reproduces the number the paper prints.")
tight_c = min(CLEAN, key=lambda k: CLEAN[k][1])
ck("30e ROBUSTNESS ARM: the result does not come from the three galaxies with no measured truncation or from the two systems "
   "van der Kruit himself throws out.  Cut to his own selection, every baryonic disc-edge scale stays two to three times "
   "tighter than the MOND radius and the external-field radius stays the worst of them, so the negative verdict on the item "
   "is not a selection artefact",
   CLEAN["R_deep (stellar truncation)"][1] < 0.15 and CLEAN["r_M = v^2/a_0 (MOND radius)"][1] > 2*CLEAN["R_deep (stellar truncation)"][1],
   f"clean N = {int(keep.sum())}: R_warp/R_deep = {CLEAN['R_deep (stellar truncation)'][0]:.3f} at "
   f"{CLEAN['R_deep (stellar truncation)'][1]:.3f} dex (full sample {TAB['R_deep (stellar truncation)'][1]:.3f}); MOND radius "
   f"{CLEAN['r_M = v^2/a_0 (MOND radius)'][1]:.3f} dex (full {TAB['r_M = v^2/a_0 (MOND radius)'][1]:.3f}); tightest scale is "
   f"still '{tight_c}' at {CLEAN[tight_c][1]:.3f} dex; r_warp/r_EFE = {m_efe_c:.3f}")

# ---------------------------------------------------------------- verdicts
best_nm = min(TAB, key=lambda k: TAB[k][1])
ck("30 (the framework's stated warp mechanism does NOT survive) the external-field radius is the WORST of the candidate scales, "
   "not the best: with the external field these galaxies actually sit in, r_EFE lies far outside where their warps begin, and "
   "matching the two would need a field roughly forty times the large-scale structure these galaxies sit in and two hundred "
   "times the upper limit their nearest catalogued companion can supply",
   R30["canonical"]["s_efe"] < 0.15 and 0.5 < R30["canonical"]["m_efe"] < 2.0,
   f"r_warp/r_EFE = {R30['canonical']['m_efe']:.3f} (canonical) / {R30['alt']['m_efe']:.3f} (alt) with "
   f"{R30['canonical']['s_efe']:.3f} dex scatter (the criterion was < 0.15 dex and a ratio near 1); the required e_N is "
   f"{np.median(R30['canonical']['eN_req']):.2f}, {R30['canonical']['over_lss']:.0f}x the actual large-scale field and "
   f"{R30['canonical']['over_comp']:.0f}x the companion upper limit")
ck("30b2 what DOES organise the warp onset is a BARYONIC scale: all four disc-edge radii beat the MOND radius by a factor of "
   "two and a half to three in scatter, and the warp begins essentially AT the edge of the stellar disc.  That is the standard "
   "picture (Briggs 1990; van der Kruit 2007), it needs no external field, no halo and no a_0, and it is neutral between the "
   "framework and LambdaCDM -- and negative for the item as posed",
   TAB["R_deep (stellar truncation)"][1] < 0.15 and TAB["r_M = v^2/a_0 (MOND radius)"][1] > 2*TAB["R_deep (stellar truncation)"][1],
   f"tightest scale = '{best_nm}' at {TAB[best_nm][1]:.3f} dex; R_warp/R_deep = {TAB['R_deep (stellar truncation)'][0]:.3f} "
   f"with {TAB['R_deep (stellar truncation)'][1]:.3f} dex (N = {TAB['R_deep (stellar truncation)'][2]}); R_warp/R_opt "
   f"{TAB['R_opt (visual disc edge)'][1]:.3f}; R_warp/R_25 {TAB['R_25 (optical radius)'][1]:.3f}; against "
   f"{TAB['r_M = v^2/a_0 (MOND radius)'][1]:.3f} dex for the MOND radius")
ck("30b3 the weaker fallback -- that warps begin at a FIXED ACCELERATION in units of a_0 -- also fails, and is recorded as a "
   "claim that does not hold rather than as a near-miss: the onset acceleration is 0.4 a_0 in the median, which sounds like a "
   "law, but it carries a rotation-speed trend of a full dex per dex, so what is actually constant is r_warp/v_flat, i.e. the "
   "disc's size, not its acceleration",
   R30["canonical"]["y_sc"] < TAB["R_deep (stellar truncation)"][1] and abs(R30["canonical"]["y_sl"]) < 2*R30["canonical"]["y_sle"],
   f"g_obs(r_warp) = {R30['canonical']['y_med']:.2f} a_0 canonical / {R30['alt']['y_med']:.2f} a_0 alt, scatter "
   f"{R30['canonical']['y_sc']:.3f} dex against {TAB['R_deep (stellar truncation)'][1]:.3f} for R_deep; mass trend "
   f"{R30['canonical']['y_sl']:+.2f} +- {R30['canonical']['y_sle']:.2f} dex/dex in v_flat, i.e. r_warp propto v_flat^"
   f"{2-R30['canonical']['y_sl']:.2f} and not v_flat^2")
ck("30c TWO CORRECTIONS TO THE HUNT LIST, recorded: the papers it cites for warp catalogues (van Eymeren+2011, A&A 530 A29/A30) "
   "are about lopsidedness and contain no warp radii, and the Garcia-Ruiz+2002 paper it wants does not tabulate the per-galaxy "
   "warp radius at all -- it is only in their figures.  The numbers used here had to come from van der Kruit 2007 Table 3",
   True,
   f"{len(gal)} galaxies with a printed R_warp, out of {len(W)} in the WHISP edge-on sample")
ck("30d AGAINST INTEREST, the limits of this test: N = {} galaxies, the warp radii are PROJECTED (a lower limit; van der "
   "Kruit's own deprojection puts the intrinsic value near 1.1 R_max, a factor that moves medians and not scatters), the "
   "external fields are estimated and not measured for these particular galaxies, and a companion mass had to be assumed. "
   "None of that can close a factor of {:.0f} in e_N".format(len(gal), R30["canonical"]["over_lss"]),
   True,
   f"scatter comparison is the load-bearing statistic and is projection-proof; the median r_warp/r_EFE would need the "
   f"projection factor to be {1.0/R30['canonical']['m_efe']:.0f} rather than 1.1")
sys.exit(ck.done())
