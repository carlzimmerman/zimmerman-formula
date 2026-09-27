#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG5 (2/6) -- THE REFINED MODEL: spherical collapse with the baryons' own infall and cooling, and the vacuum stress trigger
acting on coherent dark streams.  What does the principle leave behind, halo by halo?

WHY.  CFG5_1 stated the principle (the dark field's stress <= a0^2/8piG, written at coherent shell crossing) and its simple
reading: on a relaxed, self-similar (SIS) equilibrium the cap is a pull g_d <= sqrt(1 - f_b) a0 = 0.918 a0.  The stress of
streams that are still crossing is not the relaxed stress, and the baryons condense while the halo grows.  This lane runs the
collapse itself (CFG5_collapse_engine: the record's FP16 initial-profile recipe; orbits with a tangential velocity at
turnaround; baryons that cool at their first pericentre into a central galaxy; the trigger on coherent dark streams; daughters
kicked at FK1's v_k that escape or stay bound) and measures what survives.

RUNS.  Host masses 10^10.5 - 10^13 Msun (galaxies, groups) and 3e14, 1e15 (clusters), 600 Lagrangian dark + 600 baryon shells.
  dark-only   : the baryons stay hot (no condensation) -- the fossil of the dark collapse itself;
  cooling     : the baryons of each shell cool at its first pericentre (f_gal from the declared stellar-to-halo relation x 2)
                -- the fossil with the galaxy forming inside it (10^11, 10^12 Msun);
  no trigger  : the same collapse without the principle (the LCDM control of the same engine).
  Both footings for every triggered run; v_k = 600 km/s (FK1's window centre; 575 and 650 reported).

HYPOTHESES (declared before the first committed run; a scratch prototype of the same engine was run first and is disclosed
under HISTORY).
  H2a  THE FOSSIL FORMS: at every host mass where the trigger fires, the dark-only fossil's maximum dark pull lies below the
       no-trigger run's and below the equilibrium cap sqrt(1 - f_b) a0, on both footings.
  H2b  GALAXIES LOSE, CLUSTERS KEEP: the escaped share of the converted dark mass is >= 0.9 for hosts <= 1e11 Msun and
       <= 0.1 for hosts >= 1e13 Msun (dark-only, v_k = 600 km/s), both footings.
  H2c  A SMALL BUDGET: the converted dark mass is <= 15% of the host's own dark mass (inside r200) for every host <= 1e13 Msun,
       both footings (so the cosmological hot component stays small; CFG5_5 prices it).
  H2d  (reported) the realized cap: the dark-only fossil's maximum dark pull in a0 units, and its ratio to the equilibrium cap.
  H2e  (reported) with the galaxy condensing (cooling runs): the survivors' maximum dark pull, and the contraction factor
       over the dark-only fossil.
  H2f  (reported) clusters: the dark retention inside R500, eps = M_dark,fossil(<R500)/M_dark,no-trigger(<R500).
CHECKS
  C0a CONTROL [load-bearing]: the engine's no-trigger dark-only halos against NFW with the declared concentration-mass relation:
      M(<r)/M_NFW(<r) within 25% at 0.3, 0.5 and 1.0 r200 for every host (the inner profile is reported: orbits with a
      tangential velocity at turnaround core the centre).
  C0b CONTROL [load-bearing]: resolution: the 1e12 dark-only fossil at 600 vs 1000 shells -- max dark pull and converted
      fraction agree within 15%.
  H2a, H2b, H2c [load-bearing]; H2d, H2e, H2f, V (the v_k window) reported; W the ledger.
MUTATE=1 sets a0 -> 0 inside the cap (P_c = 0): every coherent crossing converts.  H2c must FAIL (rc = 1).

SCOPE.  One-dimensional and spherical: no substructure, no mergers, no disc geometry; the galaxy is static parcels at
0.02 r_ta; the stress estimator averages 48 radial neighbours; the coherence window is turnaround -> first apocentre after the
first pericentre.  Ringing is reduced by averaging all snapshots after a = 0.85.  These are declared modelling choices (the
ledger lists them); the lane's claims are the ones the checks name.  The dark field's mass is still required (FL1).

HISTORY (disclosed).  A scratch prototype of this engine (same physics, Python loops for the escape) was run on 1e11, 1e12,
1e13 (dark-only) and 1e12 (cooling) before the hypotheses were written.  It showed: the trigger fires below the equilibrium
cap (realized max pull ~0.2-0.4 a0 in dark-only collapse), hollowed centres, escaped shares 1.00 / 0.33 / 0.03, converted
2% / 4% / 10% of the host's dark mass, and, with cooling, survivors contracted to ~2 a0 in the inner 3 kpc.  The hypotheses'
thresholds (0.9 / 0.1 / 15%) were set from the physics (v_k against galaxy and cluster escape speeds; the forest-scale budget),
not tuned to those numbers.

Run from the repository root:  python3 campaign_fresh_gravity/CFG5_2_collapse.py
"""
import os, sys, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import CFG5_common as C
import CFG5_collapse_engine as E

L = C.Lane("CFG5_2_collapse", "CFG5.2")
P, banner, check = L.P, L.banner, L.check
MUT = L.MUTATE
P(__doc__.split("CHECKS")[0].strip())
if MUT:
    P("\n  *** MUTATE=1: a0 -> 0 inside the cap -- H2c must FAIL ***")
A0CAP = {f: (0.0 if MUT else a) for f, a in C.FOOT.items()}
GCAP = math.sqrt(1 - C.F_B)
CONV = 1e6 / C.KPC                                                   # (km/s)^2/kpc -> m/s^2
SIG = E.Sigma()
P(f"\n  CLASS sigma8 = {SIG.sigma8:.4f}; f_b = {C.F_B:.4f}; equilibrium cap sqrt(1 - f_b) = {GCAP:.4f} a0   {L.el()}")
RG = np.geomspace(0.2, 3000.0, 400)                                  # kpc
GAL_MASSES = [10 ** 10.5, 1e11, 10 ** 11.5, 1e12, 10 ** 12.5, 1e13]
CL_MASSES = [10 ** 14.5, 1e15]


def summarise(res, a0_ref):
    Md, Mdau, Mb = E.profiles(res, RG)
    Mtot = Md + Mb
    r200 = E.r200_of(RG, Mtot)
    gd = E.GK * Md / RG ** 2 * CONV
    gb = E.GK * Mb / RG ** 2 * CONV
    inside = RG <= r200
    md200 = float(np.interp(r200, RG, Md))
    return dict(Md=Md, Mdau=Mdau, Mb=Mb, r200=r200, gd=gd, gb=gb, hmax=float(gd[inside].max() / a0_ref),
                r_hmax=float(RG[inside][np.argmax(gd[inside])]), Md200=md200, budget=res["budget"], galaxy=res["galaxy"],
                nstep=res["nstep"], runtime=res["runtime"])


# ============================================================================================ the runs
banner("RUNS  (dark-only: no trigger, then the fossil on both footings; clusters; cooling; resolution; v_k window)")
R = {}
for M0 in GAL_MASSES + CL_MASSES:
    key = f"{M0:.3e}"
    R[key] = {"none": summarise(E.run(SIG, M0, 1.0, trigger=False, cooling=False), C.FOOT["canonical"])}
    for f in C.FOOT:
        R[key][f] = summarise(E.run(SIG, M0, A0CAP[f], trigger=True, cooling=False), C.FOOT[f])
    b = R[key]["canonical"]["budget"]
    P(f"    host {M0:.2e}: r200 {R[key]['none']['r200']:.0f} kpc; no trigger max h = {R[key]['none']['hmax']:.3f} (canonical a0); "
      f"fossil max h = {R[key]['canonical']['hmax']:.3f} / {R[key]['alt']['hmax']:.3f}; converted {b['converted']:.2e} "
      f"(escaped {b['escaped'] / max(b['converted'], 1):.2f})   {L.el()}")
COOL = {}
for M0 in (1e11, 1e12):
    key = f"{M0:.3e}"
    COOL[key] = {"none": summarise(E.run(SIG, M0, 1.0, trigger=False, cooling=True), C.FOOT["canonical"])}
    for f in C.FOOT:
        COOL[key][f] = summarise(E.run(SIG, M0, A0CAP[f], trigger=True, cooling=True), C.FOOT[f])
    P(f"    cooling host {M0:.2e}: galaxy {COOL[key]['none']['galaxy']:.2e} Msun; no trigger max h = {COOL[key]['none']['hmax']:.3f}; "
      f"fossil max h = {COOL[key]['canonical']['hmax']:.3f} / {COOL[key]['alt']['hmax']:.3f}   {L.el()}")
RES_HI = summarise(E.run(SIG, 1e12, A0CAP["canonical"], trigger=True, cooling=False, Nc=1000), C.FOOT["canonical"])
VKW = {vk: summarise(E.run(SIG, 1e12, A0CAP["canonical"], trigger=True, cooling=False, vk=vk), C.FOOT["canonical"])
       for vk in (575.0, 650.0)}
P(f"    resolution (1e12, 1000 shells) and v_k window (575, 650) done   {L.el()}")

# ============================================================================================ C0a the engine against NFW
banner("C0a CONTROL: the engine's no-trigger dark-only halos against NFW (declared concentration-mass relation)")
c0a = {}
for M0 in GAL_MASSES + CL_MASSES:
    key = f"{M0:.3e}"; s = R[key]["none"]
    Mtot = s["Md"] + s["Mb"]
    M200 = float(np.interp(s["r200"], RG, Mtot))
    halo = C.nfw_halo(M200, 0.0)
    r200_nfw = halo["r200"] / C.KPC
    rat = {}
    for x in (0.03, 0.1, 0.3, 0.5, 1.0):
        rr = x * s["r200"]
        rat[x] = float(np.interp(rr, RG, Mtot) / (halo["M_of"](rr * C.KPC) / C.MSUN))
    c0a[key] = dict(M200=M200, c=halo["c"], r200_engine=s["r200"], r200_nfw=r200_nfw, ratio=rat)
    P(f"    host {M0:.2e}: M200 {M200:.2e}, c_DM14 {halo['c']:.1f}; M/M_NFW at 0.03/0.1/0.3/0.5/1 r200 = "
      + " / ".join(f"{rat[x]:.2f}" for x in rat))
L.OUT["numbers"]["C0a"] = c0a
check("C0a CONTROL: the engine's no-trigger halos match NFW (declared c-M) within 25% at 0.3, 0.5 and 1.0 r200 for every host",
      {k: [round(v["ratio"][x], 2) for x in (0.3, 0.5, 1.0)] for k, v in c0a.items()},
      all(abs(v["ratio"][x] - 1) <= 0.25 for v in c0a.values() for x in (0.3, 0.5, 1.0)),
      "the inner 0.03-0.1 r200 is reported: the tangential velocity at turnaround (FP16's recipe) cores the centre")

# ============================================================================================ C0b resolution
banner("C0b CONTROL: resolution -- the 1e12 dark-only fossil at 600 vs 1000 shells")
lo_, hi_ = R[f"{1e12:.3e}"]["canonical"], RES_HI
fc_lo = lo_["budget"]["converted"] / max(lo_["Md200"], 1.0); fc_hi = hi_["budget"]["converted"] / max(hi_["Md200"], 1.0)
P(f"    max dark pull {lo_['hmax']:.3f} vs {hi_['hmax']:.3f} a0; converted fraction {fc_lo:.4f} vs {fc_hi:.4f}")
L.OUT["numbers"]["C0b"] = dict(hmax=(lo_["hmax"], hi_["hmax"]), conv_frac=(fc_lo, fc_hi))
check("C0b CONTROL: the 1e12 fossil's max dark pull and converted fraction agree within 15% between 600 and 1000 shells",
      f"h {lo_['hmax']:.3f}/{hi_['hmax']:.3f}; converted {fc_lo:.4f}/{fc_hi:.4f}",
      abs(lo_["hmax"] / max(hi_["hmax"], 1e-9) - 1) <= 0.15 and abs(fc_lo / max(fc_hi, 1e-12) - 1) <= 0.15)

# ============================================================================================ H2a the fossil forms
banner("H2a THE FOSSIL FORMS: the dark-only fossil's maximum dark pull, against the no-trigger run and the equilibrium cap")
h2a = {}
ok_a = True
for f in C.FOOT:
    for M0 in GAL_MASSES + CL_MASSES:
        key = f"{M0:.3e}"
        none_h = R[key]["none"]["hmax"] * C.FOOT["canonical"] / C.FOOT[f]
        fos = R[key][f]
        fired = fos["budget"]["fired_shells"] > 0
        h2a[f"{f}|{key}"] = dict(no_trigger=none_h, fossil=fos["hmax"], fired=fired, r_hmax=fos["r_hmax"])
        if fired:
            ok_a &= (fos["hmax"] < none_h) and (fos["hmax"] < GCAP)
    P(f"    [{f:9s}] " + "; ".join(f"{float(k.split('|')[1]):.1e}: {v['no_trigger']:.3f} -> {v['fossil']:.3f}"
                                     f"{'' if v['fired'] else ' (no fire)'}" for k, v in h2a.items() if k.startswith(f)))
L.OUT["numbers"]["H2a"] = h2a
check("H2a the dark-only fossil's maximum dark pull lies below the no-trigger run's and below sqrt(1 - f_b) a0 wherever the "
      "trigger fires, both footings", {k: f"{v['fossil']:.3f}" for k, v in h2a.items() if v["fired"]}, ok_a)

# ============================================================================================ H2b escape vs recapture
banner("H2b GALAXIES LOSE, CLUSTERS KEEP: the escaped share of the converted dark mass (v_k = 600 km/s)")
h2b = {}
for f in C.FOOT:
    for M0 in GAL_MASSES + CL_MASSES:
        b = R[f"{M0:.3e}"][f]["budget"]
        h2b[f"{f}|{M0:.3e}"] = b["escaped"] / b["converted"] if b["converted"] > 0 else float("nan")
    P(f"    [{f:9s}] " + ", ".join(f"{float(k.split('|')[1]):.1e}: {v:.2f}" for k, v in h2b.items() if k.startswith(f)))
L.OUT["numbers"]["H2b"] = h2b
small = [v for k, v in h2b.items() if float(k.split("|")[1]) <= 1.01e11 and math.isfinite(v)]
large = [v for k, v in h2b.items() if float(k.split("|")[1]) >= 0.99e13 and math.isfinite(v)]
check("H2b the escaped share is >= 0.9 for hosts <= 1e11 and <= 0.1 for hosts >= 1e13, both footings",
      f"<= 1e11: {[round(v, 2) for v in small]}; >= 1e13: {[round(v, 2) for v in large]}",
      len(small) > 0 and len(large) > 0 and min(small) >= 0.9 and max(large) <= 0.1)

# ============================================================================================ H2c the budget
banner("H2c A SMALL BUDGET: converted dark mass over the host's own dark mass inside r200")
h2c = {}
for f in C.FOOT:
    for M0 in GAL_MASSES + CL_MASSES:
        s = R[f"{M0:.3e}"][f]
        h2c[f"{f}|{M0:.3e}"] = s["budget"]["converted"] / max(s["Md200"], 1.0)
    P(f"    [{f:9s}] " + ", ".join(f"{float(k.split('|')[1]):.1e}: {v:.3f}" for k, v in h2c.items() if k.startswith(f)))
L.OUT["numbers"]["H2c"] = h2c
gal_frac = [v for k, v in h2c.items() if float(k.split("|")[1]) <= 1.01e13]
check("H2c the converted dark mass is <= 15% of the host's own dark mass for every host <= 1e13, both footings",
      f"max {max(gal_frac):.3f}", max(gal_frac) <= 0.15)

# ============================================================================================ H2d the realized cap (reported)
banner("H2d (reported) THE REALIZED CAP of the dark collapse: max dark pull [a0] and its ratio to the equilibrium cap")
h2d = {}
for f in C.FOOT:
    vals = {M0: R[f"{M0:.3e}"][f]["hmax"] for M0 in GAL_MASSES + CL_MASSES if R[f"{M0:.3e}"][f]["budget"]["fired_shells"] > 0}
    h2d[f] = {f"{k:.3e}": dict(h=v, over_eq_cap=v / GCAP, implied_stress_ratio=(GCAP / max(v, 1e-9)) ** 2) for k, v in vals.items()}
    P(f"    [{f:9s}] " + "; ".join(f"{k:.1e}: {v:.3f} a0 (x{v / GCAP:.2f} of the cap; crossing/relaxed stress ~{(GCAP / max(v, 1e-9)) ** 2:.1f})"
                                     for k, v in vals.items()))
L.OUT["numbers"]["H2d"] = h2d
check("H2d (reported) the realized cap of the dark collapse, per host", {f: {k: round(v["h"], 3) for k, v in h2d[f].items()} for f in h2d},
      True, load_bearing=False)

# ============================================================================================ H2e cooling (reported)
banner("H2e (reported) THE GALAXY CONDENSING INSIDE THE FOSSIL: survivors' max dark pull, contraction over the dark-only fossil")
h2e = {}
for M0 in (1e11, 1e12):
    key = f"{M0:.3e}"
    for f in C.FOOT:
        c_ = COOL[key][f]; d_ = R[key][f]
        a_ = C.FOOT[f]
        y = c_["gb"] / a_; h = c_["gd"] / a_
        rows = []
        for yy in (0.1, 0.3, 1.0, 3.0, 10.0):
            k = np.where((y >= yy) & (RG < c_["r200"]))[0]
            if len(k):
                rows.append((yy, float(h[k[-1]])))
        h2e[f"{f}|{key}"] = dict(hmax_cool=c_["hmax"], hmax_dark_only=d_["hmax"], contraction=c_["hmax"] / max(d_["hmax"], 1e-9),
                                 h_at_y=rows, hmax_no_trigger_cool=COOL[key]["none"]["hmax"] * C.FOOT["canonical"] / a_,
                                 galaxy=c_["galaxy"])
        P(f"    [{f:9s}] host {M0:.1e}: galaxy {c_['galaxy']:.2e}; max h with cooling {c_['hmax']:.3f} (dark-only fossil "
          f"{d_['hmax']:.3f}; x{c_['hmax'] / max(d_['hmax'], 1e-9):.1f}); LCDM with cooling {h2e[f'{f}|{key}']['hmax_no_trigger_cool']:.3f}; "
          f"h at y = " + ", ".join(f"{a:.1f}: {b:.2f}" for a, b in rows))
L.OUT["numbers"]["H2e"] = h2e
check("H2e (reported) with the galaxy condensing, the phase-mixed survivors contract above the collapse-time cap (the coherence "
      "clause forbids converting them): the fossil's baryon-dominated inner halo inherits the contraction",
      {k: f"{v['hmax_cool']:.2f} (x{v['contraction']:.1f})" for k, v in h2e.items()}, True, load_bearing=False)

# ============================================================================================ H2f clusters (reported)
banner("H2f (reported) CLUSTERS: the dark retention inside R500 (in-place conversion, daughters bound)")
h2f = {}
for M0 in CL_MASSES:
    key = f"{M0:.3e}"
    s0 = R[key]["none"]
    Mtot0 = s0["Md"] + s0["Mb"]
    rho_m = Mtot0 / (4 * math.pi / 3 * RG ** 3); tgt = 500 * 3 * E.H0 ** 2 / (8 * math.pi * E.GK)
    r500 = float(RG[np.where(rho_m >= tgt)[0][-1]])
    for f in C.FOOT:
        s1 = R[key][f]
        eps = float(np.interp(r500, RG, s1["Md"]) / max(np.interp(r500, RG, s0["Md"]), 1.0))
        eps200 = float(np.interp(s0["r200"], RG, s1["Md"]) / max(np.interp(s0["r200"], RG, s0["Md"]), 1.0))
        dau = float(np.interp(r500, RG, s1["Mdau"]) / max(np.interp(r500, RG, s1["Md"]), 1.0))
        h2f[f"{f}|{key}"] = dict(r500=r500, eps_R500=eps, eps_r200=eps200, daughter_share_R500=dau,
                                 conv_frac=s1["budget"]["converted"] / max(s1["Md200"], 1))
    P(f"    host {M0:.2e}: R500 {r500:.0f} kpc; " + "; ".join(
        f"{f}: eps(R500) {h2f[f'{f}|{key}']['eps_R500']:.3f}, eps(r200) {h2f[f'{f}|{key}']['eps_r200']:.3f}, daughters "
        f"{h2f[f'{f}|{key}']['daughter_share_R500']:.3f} of the dark mass in R500" for f in C.FOOT))
L.OUT["numbers"]["H2f"] = h2f
check("H2f (reported) clusters keep their dark mass: the retention inside R500 per footing", {k: round(v["eps_R500"], 3) for k, v in h2f.items()},
      True, load_bearing=False)

# ============================================================================================ V the v_k window (reported)
banner("V   (reported) FK1's v_k window at 1e12: escaped share and max dark pull")
vw = {vk: dict(escaped=s["budget"]["escaped"] / max(s["budget"]["converted"], 1), hmax=s["hmax"]) for vk, s in VKW.items()}
vw[600.0] = dict(escaped=R[f"{1e12:.3e}"]["canonical"]["budget"]["escaped"] / max(R[f"{1e12:.3e}"]["canonical"]["budget"]["converted"], 1),
                 hmax=R[f"{1e12:.3e}"]["canonical"]["hmax"])
P("    " + ", ".join(f"v_k {k:.0f}: escaped {v['escaped']:.2f}, max h {v['hmax']:.3f}" for k, v in sorted(vw.items())))
L.OUT["numbers"]["V"] = {f"{k:.0f}": v for k, v in vw.items()}
check("V (reported) the v_k window moves the escaped share, not the cap", {f"{k:.0f}": round(v["escaped"], 2) for k, v in vw.items()},
      True, load_bearing=False)

# the fossil profiles for later lanes (dark-only and cooling; canonical and alt)
L.OUT["numbers"]["profiles"] = dict(r_kpc=RG, dark_only={k: {f: dict(Md=v[f]["Md"], Mb=v[f]["Mb"]) for f in ("none", "canonical", "alt")}
                                                        for k, v in R.items()},
                                    cooling={k: {f: dict(Md=v[f]["Md"], Mb=v[f]["Mb"]) for f in ("none", "canonical", "alt")} for k, v in COOL.items()})

banner("W   THE LEDGER")
L.ledger("L2a", "DERIVED", "the dark collapse converts where coherent crossing streams exceed P_c; the survivors form a hollowed, capped core", "H2a, H2d")
L.ledger("L2b", "DERIVED", "galaxies lose the converted mass (v_k > v_esc), groups and clusters keep it bound and hotter", "H2b, H2f")
L.ledger("L2c", "DERIVED", "the converted budget is a few percent of a galaxy's dark mass", "H2c")
L.ledger("L2d", "CONSTRAINT", "phase-mixed survivors contract when the galaxy condenses (the coherence clause cannot convert them): "
         "the inner dark pull of baryon-dominated galaxies is the contracted fossil, not the collapse cap", "H2e")
L.ledger("L2e", "DECLARED", "the engine's choices: FP16's initial profile and MAH form, lambda_j 0.15-0.35, f_R = 0.02, f_gal = 2 M*/(f_b M_h), "
         "48-neighbour stress, the coherence window, softening 0.2 kpc", "SCOPE")
check("W the ledger (reported)", f"{len(L.OUT['ledger'])} links", True, load_bearing=False)

banner("VERDICT")
hd = L.OUT["numbers"]["H2d"]["canonical"]
P(f"""  The collapse writes the cap, but not at the relaxed value: crossing streams carry more stress than the relaxed isothermal
  body, so the trigger fires earlier and the dark-only fossil's maximum pull sits at {min(v['h'] for v in hd.values()):.2f}-{max(v['h'] for v in hd.values()):.2f} a0
  (canonical) instead of sqrt(1 - f_b) = 0.92, with hollowed centres.  Galaxies lose the converted mass; groups and clusters keep it
  bound (H2b, H2f).  The budget is a few percent of a galaxy's dark mass (H2c).  When the galaxy condenses inside the fossil the
  phase-mixed survivors contract (H2e): the baryon-dominated inner halo carries the contraction, not the collapse cap.  One
  dimension, spheres, declared cooling; kappa stays fitted; nothing here is closed.""")
sys.exit(L.finish())
