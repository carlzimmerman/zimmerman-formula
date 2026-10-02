#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG271 -- implied-a0 upper bounds (or floor / ceiling markers) for HZ9 (z = 5.5413) from the three-ring [CII] curve: stars-only baryons (a lower limit), class D (no gas), two stellar-mass branches never pooled.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG271_hz9_three_rings/FROZEN_CRITERIA.md (0f7f661b5).
  rows      HZ9 [M986] / HZ9 [M103] (outer ring R = 2.68 kpc; headline pair), the same two branches with the three rings as three rows, and with Parlanti+23's M_rot(< 5 kpc) at R = 5 kpc (sensitivity rows)
  g_obs     (V^2 + 2 sigma0^2 R / r_D) / R with sigma0 = 51 +- 9.5 and r_D = 2.7 kpc; g_bar  B0 = stars only (one exponential disc, scale r_D), B2 = scaling gas (extrapolated)
  STAGE=A   the blind pre-flight: no velocity-bearing column is loaded; no g_obs, D, delta or s* is formed.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (V, sigma0 x 2, M_rot x 4); STAGE=B SELFTEST=1 (fabricated V on the law at s = 2).
Run: STAGE=A python3 .../cfg271_hz9_rings.py ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, io, json, math, time, zlib, csv, contextlib, re
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

TSTART = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
import hzq_core as H

STAGE = os.environ.get("STAGE", "").strip().upper()
MUTATE = os.environ.get("MUTATE", "0") == "1"
SELFTEST = os.environ.get("SELFTEST", "0") == "1"
assert STAGE in ("A", "B"), "set STAGE=A or STAGE=B"
assert not ((MUTATE or SELFTEST) and STAGE == "A") and not (MUTATE and SELFTEST), "MUTATE / SELFTEST apply to stage B, one at a time"
SFX = f"_stage{STAGE}" + ("_MUTATE1" if MUTATE else "") + ("_SELFTEST" if SELFTEST else "")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: V and sigma0 x 2, M_rot x 4 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
B_MC = 10000
LOADVEL = (STAGE == "B") and not SELFTEST                                   # the SELFTEST never loads the real velocity-bearing columns
DA = os.path.join(REPO, "data_assembly")
RINGP = os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_rings.csv")
GALP = os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_galaxies.csv")
JRINGP = os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_tableA3_rings.csv")
JCLSP = os.path.join(DA, "highz_literature_tables", "jones2021_alpine", "jones2021_table1_sample_classes.csv")
PARLP = os.path.join(REPO, "real_research", "virial_floor_2026", "sources", "alma.csv")
L328P = os.path.join(REPO, "real_research", "virial_floor_2026", "highz_sigma_mstar.csv")

# ---------------------------------------------------------------- loading (stage A: no velocity-bearing column)
ring_cols = ["galaxy", "z", "R_kpc"] + (["Vrot_kms", "e_Vrot_kms", "sigma_kms", "e_sigma_kms", "Mdyn_msun"] if LOADVEL else [])
rings = pd.read_csv(RINGP, usecols=ring_cols); rings = rings[rings["galaxy"] == "HZ9"].reset_index(drop=True)
jr_cols = ["name", "R_kpc"] + (["vrot_kms", "vrot_kms_err", "sigma_kms", "sigma_kms_err", "Mdyn_Msun"] if LOADVEL else [])
jrings = pd.read_csv(JRINGP, usecols=jr_cols); jrings = jrings[jrings["name"] == "HZ9"].reset_index(drop=True)
gal_cols = ["galaxy", "redshift", "class_jones2021", "inc_morph_deg", "e_inc_morph_deg", "inc_kin_deg", "e_inc_kin_deg", "pa_morph_deg", "e_pa_morph_deg", "pa_kin_deg", "e_pa_kin_deg", "pa_delta_deg", "log_mstar_msun", "sfr_msun_yr",
            "n_rings", "r_min_kpc", "r_max_kpc", "beam_arcsec", "spatial_res_kpc", "w15_1_velocity_gradient", "w15_2_vrot_gt_sigma", "w15_3_sigma_peak_position", "w15_4_pa_agreement", "w15_5_intensity_alignment", "n_passed", "n_known_issues"]
gal = pd.read_csv(GALP, usecols=gal_cols); gal = gal[gal["galaxy"] == "HZ9"].reset_index(drop=True)
cls = pd.read_csv(JCLSP, usecols=["name", "z", "PA_moment", "PA_moment_err", "PA_3DBarolo", "PA_3DBarolo_err", "inc_moment", "inc_moment_err", "inc_3DBarolo", "inc_3DBarolo_err", "criteria_W15_1to5", "class_J21"])
cls = cls[cls["name"] == "HZ9"].reset_index(drop=True)
par_cols = ["name", "z", "logMstar", "logMstar_err", "notes"] + (["sigma", "sigma_err", "logMdyn"] if LOADVEL else [])
parl = pd.read_csv(PARLP, usecols=par_cols); parl = parl[parl["name"] == "HZ9"].reset_index(drop=True)
l328 = pd.read_csv(L328P, usecols=["name", "logMstar", "logMstar_err"] + (["construction"] if LOADVEL else [])); l328 = l328[l328["name"] == "HZ9"].reset_index(drop=True)
P(f"rings {os.path.basename(RINGP)} sha256 {H.sha(RINGP)}; Jones A3 {H.sha(JRINGP)}; galaxies {H.sha(GALP)}; classes {H.sha(JCLSP)}; Parlanti rows (L328 sources) {H.sha(PARLP)}; L328 table {H.sha(L328P)}; velocity-bearing columns loaded: {LOADVEL}")

Z0 = float(rings["z"].iloc[0]) if len(rings) else float("nan")
RING_R = rings["R_kpc"].values.astype(float)
R_OUT = float(RING_R[-1]) if len(RING_R) else float("nan")
R_MROT = 5.0
m_rd = re.search(r"r_D=([0-9.]+)\s*kpc", str(parl["notes"].iloc[0])) if len(parl) else None
RD = float(m_rd.group(1)) if m_rd else float("nan")
RE_STAR = H.XN * RD
INC0, EINC = float(gal["inc_kin_deg"].iloc[0]), float(gal["e_inc_kin_deg"].iloc[0])
BR = {"M986": dict(lm=float(parl["logMstar"].iloc[0]), elm=float(parl["logMstar_err"].iloc[0]), src="Parlanti+23 Table 2 (Capak+2015)"),
      "M103": dict(lm=float(gal["log_mstar_msun"].iloc[0]), elm=0.20, src="corpus row (no source or error recorded); declared 0.20 dex")}
SIG0, ESIG0 = 51.0, 9.5                                                      # Parlanti+23 Method-II sigma_gas (frozen in the criteria; stage B re-reads it from the Parlanti row and compares)
LMROT, ELMROT = 10.8, 0.4                                                    # Parlanti+23 log M_rot(< 5 kpc), frozen in the criteria; compared with the row at stage B
KPA = H.kpc_per_arcsec(Z0)
BEAM_FWHM = float(gal["beam_arcsec"].iloc[0]) * KPA
HWHM = 0.5 * BEAM_FWHM
ROWS = [dict(label="HZ9 [M986]", branch="M986", route="outer", role="headline"), dict(label="HZ9 [M103]", branch="M103", route="outer", role="headline"),
        dict(label="HZ9 [M986; 3 rings]", branch="M986", route="rings3", role="sensitivity"), dict(label="HZ9 [M103; 3 rings]", branch="M103", route="rings3", role="sensitivity"),
        dict(label="HZ9 [M986; Mrot]", branch="M986", route="mrot", role="sensitivity"), dict(label="HZ9 [M103; Mrot]", branch="M103", route="mrot", role="sensitivity")]


def row_R(row):
    return {"outer": np.array([R_OUT]), "rings3": RING_R, "mrot": np.array([R_MROT])}[row["route"]]


def mu_mol(z, logM):
    return 10 ** (0.06 - 3.3 * (np.log10(1 + z) - 0.65) ** 2 - 0.41 * (logM - 10.7))


def gbar_row(row, Ms, re=None, sph=False):
    f = H.gsph if sph else H.gdisc
    return f(Ms, RE_STAR if re is None else re, row_R(row))


for r_ in ROWS:
    r_["R"] = row_R(r_); r_["Ms"] = 10 ** BR[r_["branch"]]["lm"]; r_["gb0"] = np.asarray(gbar_row(r_, r_["Ms"]), float)
    r_["mu"] = float(mu_mol(Z0, BR[r_["branch"]]["lm"])); r_["gb2"] = r_["gb0"] * (1.0 + r_["mu"]); r_["y0"] = r_["gb0"] / A0C
P(f"HZ9: z {Z0}, rings R {RING_R.tolist()} kpc, r_D {RD} kpc (R_e,* {RE_STAR:.3f}), inclination {INC0:.0f} +- {EINC:.0f} deg; branches: " + "; ".join(f"{k} log M* {v['lm']} +- {v['elm']} ({v['src']})" for k, v in BR.items()) + f"; kpc/arcsec {KPA:.3f}, beam FWHM {BEAM_FWHM:.2f} kpc")


def inc_factor(i_deg):
    return math.sin(math.radians(INC0)) / np.sin(np.radians(i_deg))         # V deprojected at the fitted inclination -> V at another inclination


# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (no velocity-bearing column is loaded; no g_obs, D, delta or s* is formed)")
    jr_same = len(jrings) == 3 and np.allclose(jrings["R_kpc"].values, RING_R, atol=1e-9)
    check("C1 CONTROL (loader): 3 HZ9 rings in the corpus and in the Jones A3 table with equal radii; one HZ9 row in the Parlanti rows, the corpus galaxy table, the Jones class table and the L328 table; z 5.5413; r_D parses to 2.7; log M* 9.86 +- 0.23 (Parlanti) equals the L328 table's; inclination 58 +- 7; beam 1.0 arcsec; corpus log M* 10.3",
          f"rings {len(rings)}, Jones rings {len(jrings)} (radii equal {jr_same}); rows: Parlanti {len(parl)}, galaxy {len(gal)}, class {len(cls)}, L328 {len(l328)}; z {Z0}; r_D {RD}; M* {BR['M986']['lm']} +- {BR['M986']['elm']} (L328 {float(l328['logMstar'].iloc[0]) if len(l328) else float('nan')} +- {float(l328['logMstar_err'].iloc[0]) if len(l328) else float('nan')}); inc {INC0} +- {EINC}; beam {float(gal['beam_arcsec'].iloc[0])}; corpus M* {BR['M103']['lm']}",
          len(rings) == 3 and jr_same and len(parl) == len(gal) == len(cls) == len(l328) == 1 and abs(Z0 - 5.5413) < 1e-9 and abs(RD - 2.7) < 1e-9 and abs(BR["M986"]["lm"] - float(l328["logMstar"].iloc[0])) < 5e-5 and abs(BR["M986"]["elm"] - float(l328["logMstar_err"].iloc[0])) < 5e-5
          and INC0 == 58 and EINC == 7 and float(gal["beam_arcsec"].iloc[0]) == 1.0 and abs(BR["M103"]["lm"] - 10.3) < 1e-9 and np.allclose(RING_R, [0.54, 1.61, 2.68]))
    yy = np.linspace(0.05, 40, 400000); hh = H.i0e(yy) * H.k0e(yy) - H.i1e(yy) * H.k1e(yy); peak = float(np.max(2 * yy ** 2 * hh)); farr = float(H.gdisc(1e11, 3.0, 150.0) / (H.G_KPC * 1e11 / 150.0 ** 2 * H.G2SI))
    src29 = open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score.py")).read(); seg = src29[src29.index("def disc_v2"):src29.index("P(__doc__")]
    ns29 = {"G_KPC": H.G_KPC, "XN": H.XN, "G2SI": H.G2SI, "i0e": H.i0e, "i1e": H.i1e, "k0e": H.k0e, "k1e": H.k1e, "math": math, "np": np}; exec(compile(seg, "cfg229_score.py", "exec"), ns29)
    rr_ = np.random.default_rng(1234); dmax = 0.0
    for _ in range(200):
        M_, Re_, Rr_ = 10 ** rr_.uniform(9, 12.5), rr_.uniform(0.5, 8), rr_.uniform(1, 20); dmax = max(dmax, abs(H.gdisc(M_, Re_, Rr_) / ns29["gdisc"](M_, Re_, Rr_) - 1))
    check("C2 CONTROL: Freeman's peak V^2 = 0.3872 G M / R_d to 0.003, g -> G M / r^2 far from a compact mass to 1e-3, and gdisc equals CFG229's on 200 random inputs to 1e-12", f"peak {peak:.4f}; far-field ratio {farr:.5f}; max deviation {dmax:.1e}", abs(peak / 0.3872 - 1) < 0.003 and abs(farr - 1) < 1e-3 and dmax < 1e-12)
    g0, c0 = gal.iloc[0], cls.iloc[0]
    w15 = "".join("Y" if bool(g0[c]) else "N" for c in ("w15_1_velocity_gradient", "w15_2_vrot_gt_sigma", "w15_3_sigma_peak_position", "w15_4_pa_agreement", "w15_5_intensity_alignment"))
    check("C3 CONTROL: the corpus galaxy row and the Jones+21 class table agree (kinematic inclination 58 +- 7 and PA 17 +- 10; morphological PA 83 +- 22 and inclination 57 +- 14; criteria YYNNN; class ROT)",
          f"corpus inc_kin {g0['inc_kin_deg']} +- {g0['e_inc_kin_deg']}, class inc_3DBarolo {c0['inc_3DBarolo']} +- {c0['inc_3DBarolo_err']}; PA kin {g0['pa_kin_deg']} +- {g0['e_pa_kin_deg']} vs {c0['PA_3DBarolo']} +- {c0['PA_3DBarolo_err']}; PA morph {g0['pa_morph_deg']} +- {g0['e_pa_morph_deg']} vs {c0['PA_moment']} +- {c0['PA_moment_err']}; inc morph {g0['inc_morph_deg']} +- {g0['e_inc_morph_deg']} vs {c0['inc_moment']} +- {c0['inc_moment_err']}; W15 {w15} vs {c0['criteria_W15_1to5']}; class {g0['class_jones2021']} vs {c0['class_J21']}",
          g0["inc_kin_deg"] == c0["inc_3DBarolo"] and g0["e_inc_kin_deg"] == c0["inc_3DBarolo_err"] and g0["pa_kin_deg"] == c0["PA_3DBarolo"] and g0["e_pa_kin_deg"] == c0["PA_3DBarolo_err"] and g0["pa_morph_deg"] == c0["PA_moment"] and g0["e_pa_morph_deg"] == c0["PA_moment_err"]
          and g0["inc_morph_deg"] == c0["inc_moment"] and g0["e_inc_morph_deg"] == c0["inc_moment_err"] and w15 == "YYNNN" == str(c0["criteria_W15_1to5"]) and g0["class_jones2021"] == "ROT" == c0["class_J21"])
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read(); seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}; exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr_ = np.random.default_rng(1234); same = True
    for _ in range(200):
        Dq = 10 ** rr_.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr_.uniform(-11, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = H.AI.implied(Dq, gq, NU, A0C); same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2)
    check("C4 CONTROL: the imported estimator equals CFG223's original bit for bit on 200 random sets", f"identical {same}", bool(same))
    d5 = 0.0
    for r_ in ROWS:
        for st in (0.5, 1.0, 2.5):
            ls, unb = H.s_star(NU(r_["gb0"] / (A0C * st)), r_["gb0"]); d5 = max(d5, abs(ls - math.log10(st)) if not unb else 9.0)
    check("C5 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on every row's stars-only baryon side", f"max |d log10 s| {d5:.1e}", d5 < 1e-6)

    P("\nA1 / A2  BARYON SIDE AND THE CFG240 READING (noiseless world; B0 = stars only, one exponential disc of scale r_D = 2.7 kpc; ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    for r_ in ROWS:
        lv, fl = H.lever1(NU(r_["y0"]), r_["gb0"]); r_["lever"], r_["ill"] = lv, bool(fl or abs(lv) >= 10)
        P(f"    {r_['label']:22s} R {np.array2string(r_['R'], precision=2)} kpc: g_bar {np.array2string(r_['gb0'], precision=3)} m/s^2, y(B0) {np.array2string(r_['y0'], precision=3)}, y(B2) {np.array2string(r_['gb2'] / A0C, precision=3)} (mu_mol {r_['mu']:.2f}), lever {lv:+.2f}{' (not computable)' if fl else ''}  {'ILL-CONDITIONED' if r_['ill'] else 'conditioned'}")
    P(f"    CFG240: T4 floor 3 sigma / sqrt(N) at sigma = 0.2 dex is {3 * 0.2 / math.sqrt(1):.2f} dex for N = 1 (calibration free); the break-even design needs y >~ 8 with deep points (y < 0.3): here y(B0) at the outer ring is {ROWS[0]['y0'][0]:.2f} (M986) and {ROWS[1]['y0'][0]:.2f} (M103)")
    P("\nA3  KNOB EFFECTS ON g_bar AT THE OUTER RING (dex relative to B0; linear in M*, so the same for both branches)")
    for nm, kw in (("stellar scale x1.5", dict(re=1.5 * RE_STAR)), ("stellar scale /1.5", dict(re=RE_STAR / 1.5)), ("stellar scale /3 (compact)", dict(re=RE_STAR / 3.0)), ("spherical", dict(sph=True))):
        v = np.log10(gbar_row(ROWS[0], ROWS[0]["Ms"], **kw) / ROWS[0]["gb0"]); P(f"    {nm}: {np.array2string(v, precision=3)} dex")
    P("\nA4  mu_mol AND THE B2 / B0 RATIO (z = 5.54 is outside the range the relation was calibrated on: an extrapolation)")
    for k in BR: P(f"    {k}: mu_mol {mu_mol(Z0, BR[k]['lm']):.2f}; B2 / B0 g_bar = {1 + mu_mol(Z0, BR[k]['lm']):.2f}")
    P("\nA5  THE BEAM (1.0 arcsec; kpc/arcsec from flat LCDM H0 = 67.4, Om = 0.315)")
    P(f"    beam FWHM {BEAM_FWHM:.2f} kpc (the corpus quotes a spatial resolution of {float(gal['spatial_res_kpc'].iloc[0]):.1f} kpc), HWHM {HWHM:.2f} kpc; R / HWHM for the rings: {np.array2string(RING_R / HWHM, precision=2)}; rings inside the HWHM: {int((RING_R < HWHM).sum())} of 3; R_out / FWHM = {R_OUT / BEAM_FWHM:.2f}; r_D / HWHM = {RD / HWHM:.2f}")
    P(f"    W15 criteria passed {int(g0['n_passed'])} of 5 (known issues {int(g0['n_known_issues'])}); PA mismatch {float(g0['pa_delta_deg']):.0f} deg; inclination {INC0:.0f} +- {EINC:.0f} deg")

    P("\nC6  COVERAGE (noiseless world on the headline rows' B0 baryons; declared 0.15 dex on g_obs; the branch's M* error; the inclination draw 58 +- 7 deg; 100 mocks, B = 1,000)")
    rng6 = np.random.default_rng(271); cov = {}
    for r_ in ROWS[:2]:
        gob_true = float((r_["gb0"] * NU(r_["y0"]))[0]); elm = BR[r_["branch"]]["elm"]; c68 = c95 = nd = 0
        for it in range(100):
            i_true = float(np.clip(rng6.normal(INC0, EINC), 20, 85)); Ms_o = r_["Ms"] * 10 ** rng6.normal(0, elm)
            god = gob_true * (math.sin(math.radians(i_true)) / math.sin(math.radians(INC0))) ** 2 * 10 ** rng6.normal(0, 0.15)
            i_d = np.clip(rng6.normal(INC0, EINC, 1000), 20, 85); gobm = god * (np.sin(np.radians(INC0)) / np.sin(np.radians(i_d))) ** 2 * 10 ** rng6.normal(0, 0.15, 1000)
            Msd = Ms_o * 10 ** rng6.normal(0, elm, 1000); gbd = H.gdisc(Msd, RE_STAR, R_OUT)
            lsd, ud = H.AI.implied((gobm / gbd)[:, None], gbd[:, None], NU, A0C); q, fr = H.rooted_pct(lsd, ud)
            if np.isfinite(q[0]): nd += 1; c68 += (q[1] <= 0.0 <= q[3]); c95 += (q[0] <= 0.0 <= q[4])
        cov[r_["label"]] = (c68 / max(nd, 1), c95 / max(nd, 1), nd); P(f"    {r_['label']}: 68 % coverage {cov[r_['label']][0]:.2f}, 95 % coverage {cov[r_['label']][1]:.2f} (mocks with a root {nd} of 100)")
    okc = all(c[0] >= 0.60 and c[1] >= 0.88 for k, c in cov.items() if not ROWS[[x['label'] for x in ROWS].index(k)]["ill"])
    check("C6 (reported; load-bearing for the conditioned rows): the 68 % and 95 % coverage of the conditioned headline rows are >= 60 % and >= 88 %", "; ".join(f"{k}: {c[0]:.2f} / {c[1]:.2f}" for k, c in cov.items()), okc, load_bearing=False)

    pfd1 = all(ok for n, ok, lb in CHK if lb and not n.startswith("C6"))
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C5)")
    P("  PF-D2 ILL-CONDITIONED rows: " + (", ".join(r_["label"] for r_ in ROWS if r_["ill"]) or "none"))
    P("  PF-D3 DRAWABLE as an upper bound: " + (", ".join(r_["label"] for r_ in ROWS if pfd1 and not r_["ill"]) or "none") + " (every drawable row is an upper bound on s*, never a measurement)")
    pfd4 = bool(R_OUT < HWHM)
    P(f"  PF-D4 BEAM-LIMITED: {pfd4} (the outer ring at {R_OUT} kpc against the beam HWHM {HWHM:.2f} kpc; reported, not blocking: the measurement is run and carries the label)")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9) scored (HE4-HE10 are scored at stage B):")
    he = {}
    he["HE1"] = bool(0.8 <= ROWS[1]["y0"][0] <= 1.6 and 0.3 <= ROWS[0]["y0"][0] <= 0.6 and not ROWS[0]["ill"] and not ROWS[1]["ill"])
    he["HE2"] = bool(all(0.2 <= v <= 2.0 for r_ in ROWS[2:4] for v in r_["y0"]) and not any(r_["ill"] for r_ in ROWS[2:4]))
    he["HE3"] = bool(1.1 <= mu_mol(Z0, BR["M103"]["lm"]) <= 1.7 and 1.7 <= mu_mol(Z0, BR["M986"]["lm"]) <= 2.6)
    for k, v in he.items(): P(f"    {k}: {'hit' if v else 'MISS (kept as it falls)'}")
    NUM.update(inputs=dict(z=Z0, rings_R=RING_R.tolist(), r_D=RD, R_e_star=RE_STAR, inc=[INC0, EINC], branches=BR, beam_fwhm_kpc=BEAM_FWHM, hwhm_kpc=HWHM, kpc_per_arcsec=KPA),
               rows={r_["label"]: dict(R=r_["R"].tolist(), gb0=r_["gb0"].tolist(), y0=r_["y0"].tolist(), y2=(r_["gb2"] / A0C).tolist(), mu=r_["mu"], lever=r_["lever"], ill=r_["ill"]) for r_ in ROWS},
               coverage={k: list(v) for k, v in cov.items()}, hand_estimates=he, pf=dict(PF_D1=bool(pfd1), PF_D4=pfd4))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V and sigma0 x 2, M_rot x 4)" if MUTATE else ""))
    rngS = np.random.default_rng(2710)
    if SELFTEST:
        VK = np.zeros(3); EVK = np.zeros(3); MROT = 10.0; SIGA, ESIGA = 0.0, 0.0
        gob_true_k = {}
        for br in ("M986", "M103"):
            rb = [r_ for r_ in ROWS if r_["branch"] == br and r_["route"] == "rings3"][0]
            gob_true_k[br] = rb["gb0"] * NU(rb["gb0"] / (2.0 * A0C)) * 10 ** rngS.normal(0, 0.15, 3)
        P("SELFTEST: V fabricated from the law at s_true = 2 on each branch's B0 baryons (+0.15 dex scatter), sigma0 = 0, 10 % errors; the real velocity-bearing columns are not even loaded")
    else:
        VK = rings["Vrot_kms"].values.astype(float); EVK = rings["e_Vrot_kms"].values.astype(float)
        SIGA, ESIGA = float(parl["sigma"].iloc[0]), float(parl["sigma_err"].iloc[0]); LMR, ELMR = float(parl["logMdyn"].iloc[0]), 0.4
    if MUTATE:
        VK, EVK = 2.0 * VK, 2.0 * EVK
    SIG_USE, ESIG_USE = (SIGA * (2.0 if MUTATE else 1.0), ESIGA * (2.0 if MUTATE else 1.0)) if not SELFTEST else (0.0, 0.0)
    LMROT_USE = (LMR if not SELFTEST else None)
    if MUTATE: LMROT_USE = LMROT_USE + math.log10(4.0)
    # per-row kinematic inputs
    KIN = {}
    for r_ in ROWS:
        if SELFTEST:
            g_t = gob_true_k[r_["branch"]]
            if r_["route"] == "outer": KIN[r_["label"]] = dict(V=np.array([math.sqrt(g_t[-1] * RING_R[-1] / H.G2SI)]), eV=np.array([0.10 * math.sqrt(g_t[-1] * RING_R[-1] / H.G2SI)]))
            elif r_["route"] == "rings3": V_ = np.sqrt(g_t * RING_R / H.G2SI); KIN[r_["label"]] = dict(V=V_, eV=0.10 * V_)
            else:
                gM = float(r_["gb0"][0] * NU(r_["gb0"][0] / (2.0 * A0C)) * 10 ** rngS.normal(0, 0.15)); KIN[r_["label"]] = dict(logM=math.log10(gM * R_MROT ** 2 / (H.G_KPC * H.G2SI)), elogM=0.4)
        else:
            if r_["route"] == "outer": KIN[r_["label"]] = dict(V=VK[-1:], eV=EVK[-1:])
            elif r_["route"] == "rings3": KIN[r_["label"]] = dict(V=VK, eV=EVK)
            else: KIN[r_["label"]] = dict(logM=LMROT_USE, elogM=ELMROT)
    KGR = {"pressure: rotation only (sigma0 = 0)": "pressure", "pressure: sigma0 = 73": "pressure", "pressure: +3.36 sigma0^2": "pressure", "inclination 51 deg": "inclination", "inclination 65 deg": "inclination",
           "stellar scale x1.5": "geometry", "stellar scale /1.5": "geometry", "stellar scale /3 (compact)": "geometry", "spherical": "geometry", "kernel P2": "kernel"}
    KN_LIST = list(KGR)

    def gobs_from(r_, kin, sig, finc, vm="head", Vv=None, logM=None):
        R = r_["R"]; A = {"head": 2.0 * R / RD, "rot": 0.0 * R, "sins": 3.36 + 0.0 * R}[vm]
        if r_["route"] == "mrot":
            Mr = 10 ** (kin["logM"] if logM is None else logM); V2 = H.G_KPC * Mr / R + A * sig ** 2
        else:
            V2 = ((kin["V"] if Vv is None else Vv) * finc) ** 2 + A * sig ** 2
        return V2 / R * H.G2SI

    def mc_row(r_, kin, B, rng, sig0=SIG_USE, esig=ESIG_USE):
        elm = BR[r_["branch"]]["elm"]; n = len(r_["R"])
        i_d = np.clip(rng.normal(INC0, EINC, B), 20, 85); finc = (math.sin(math.radians(INC0)) / np.sin(np.radians(i_d)))[:, None]
        sg = np.maximum(rng.normal(sig0, esig, B), 0.0)[:, None]; Ms_d = (r_["Ms"] * 10 ** rng.normal(0, elm, B))[:, None]
        if r_["route"] == "mrot": god = gobs_from(r_, kin, sg, 1.0, logM=kin["logM"] + kin["elogM"] * rng.normal(size=(B, 1)))
        else: god = gobs_from(r_, kin, sg, finc, Vv=kin["V"][None, :] + kin["eV"][None, :] * rng.normal(size=(B, n)))
        gbd = np.asarray(H.gdisc(Ms_d, RE_STAR, r_["R"][None, :]), float); Dd = god / gbd
        lsd, ud = H.AI.implied(Dd, gbd, NU, A0C); q, frn = H.rooted_pct(lsd, ud); frc = float(np.mean(ud & (np.median(Dd, axis=1) > 1.0)))
        dFd = np.median(np.log10(god / (gbd * NU(gbd / A0C))), axis=1); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        return q, frn, frc, dq

    RES = {}
    for r_ in ROWS:
        lab = r_["label"]; kin = KIN[lab]; gb0 = r_["gb0"]
        GO = gobs_from(r_, kin, SIG_USE, 1.0); GO_ROT = gobs_from(r_, kin, 0.0, 1.0, vm="rot"); D0 = GO / gb0
        ls0, st0 = H.s_status(D0, gb0); ls2, st2 = H.s_status(GO / r_["gb2"], r_["gb2"])
        rng = np.random.default_rng(zlib.crc32(("271|" + lab).encode()) % 100000)
        q, frn, frc, dq = mc_row(r_, kin, B_MC, rng)
        dF0 = float(np.median(np.log10(GO / (gb0 * NU(gb0 / A0C)))))
        bands = H.band_solutions(D0, gb0); star_b = {s_: H.s_star(GO / (gb0 * 10 ** s_), gb0 * 10 ** s_) for s_ in (-0.30, -0.15, 0.15, 0.30)}

        def variant(nm):
            R = r_["R"]
            if nm == "pressure: rotation only (sigma0 = 0)": return gobs_from(r_, kin, 0.0, 1.0, vm="rot"), gb0, NU
            if nm == "pressure: sigma0 = 73": return gobs_from(r_, kin, 73.0, 1.0), gb0, NU
            if nm == "pressure: +3.36 sigma0^2": return gobs_from(r_, kin, SIG_USE, 1.0, vm="sins"), gb0, NU
            if nm in ("inclination 51 deg", "inclination 65 deg"):
                if r_["route"] == "mrot": return None
                return gobs_from(r_, kin, SIG_USE, inc_factor(float(nm.split()[1]))), gb0, NU
            if nm == "stellar scale x1.5": return GO, np.asarray(gbar_row(r_, r_["Ms"], re=1.5 * RE_STAR), float), NU
            if nm == "stellar scale /1.5": return GO, np.asarray(gbar_row(r_, r_["Ms"], re=RE_STAR / 1.5), float), NU
            if nm == "stellar scale /3 (compact)": return GO, np.asarray(gbar_row(r_, r_["Ms"], re=RE_STAR / 3.0), float), NU
            if nm == "spherical": return GO, np.asarray(gbar_row(r_, r_["Ms"], sph=True), float), NU
            if nm == "kernel P2": return GO, gb0, NUP2

        kn = {}
        for nm in KN_LIST:
            v = variant(nm)
            if v is None: continue
            go_, gb_, nu_ = v; lk, uk = H.s_star(go_ / gb_, gb_, nu_)
            kn[nm] = None if (st0 != "root" or uk) else lk - ls0; kn[nm + "|root"] = (not uk)
        grp = {}
        for nm in KN_LIST:
            if kn.get(nm) is not None: grp.setdefault(KGR[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        n_root = sum(1 for nm in KN_LIST if kn.get(nm + "|root")); n_k = sum(1 for nm in KN_LIST if nm + "|root" in kn)
        lv_nl, lf_nl = H.lever1(NU(gb0 / A0C), gb0); d1 = H.shift_to_s1(D0, gb0)
        RES[lab] = dict(label=lab, branch=r_["branch"], route=r_["route"], role=r_["role"], z=Z0, R=r_["R"].tolist(), logMs=BR[r_["branch"]]["lm"], GO=GO.tolist(), GO_rot=GO_ROT.tolist(), GB=gb0.tolist(), D=D0.tolist(), D_med=float(np.median(D0)), y=r_["y0"].tolist(), ls=ls0, status=st0, s=H.s_val_status(ls0, st0),
                        q=q, frac_mc_noroot=frn, frac_mc_ceiling=frc, delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1], status_B2=st2, s_B2=H.s_val_status(ls2, st2), D_B2=(GO / r_["gb2"]).tolist(), mu=r_["mu"],
                        bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, star_bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in star_b.items()},
                        knobs=kn, recipe_half=half, n_knobs_with_root=n_root, n_knobs=n_k, lever=lv_nl, ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=H.delta_floor(D0), delta_to_s1=d1,
                        gas_to_star_req=(10 ** d1 - 1 if np.isfinite(d1) else float("nan")), g_head_over_rot_dex=float(np.median(np.log10(GO / GO_ROT))))
        R_ = RES[lab]
        b0 = (f"s* <= {10 ** ls0:.3g}" if st0 == "root" else ("FLOOR (D <= 1)" if st0 == "floor" else "CEILING (s* > 1000)")); b2 = (f"s* = {R_['s_B2']:.3g}" if st2 == "root" else st2.upper())
        qs = f"68 % [{10 ** q[1]:.3g}, {10 ** q[3]:.3g}] 95 % [{10 ** q[0]:.3g}, {10 ** q[4]:.3g}]" if np.isfinite(q[0]) else "no draw interval (< 20 rooted draws)"
        P(f"  {lab:22s} R {np.array2string(r_['R'], precision=2)}: g_obs {np.array2string(GO, precision=3)}  D {np.array2string(D0, precision=3)}  dF {dF0:+.3f}  y {np.array2string(r_['y0'], precision=3)}  {b0}; MC {qs} (no root {frn:.2f}, ceiling {frc:.2f}); B2 D {np.array2string(GO / r_['gb2'], precision=2)} {b2}"
          + f"; gas_req {R_['gas_to_star_req']:+.2f}; recipe half-width {half:.3f}; rotation-only changes g_obs by {-R_['g_head_over_rot_dex']:+.3f} dex{' ILL' if R_['ill'] else ''}")
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    ok_unit = True
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg271_stageB_results.json")))["numbers"]["rows"]
        def inv_nu(Dv):
            lo, hi = -25.0, 25.0
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if float(NU(np.array([math.exp(mid)]))[0]) > Dv: lo = mid
                else: hi = mid
            return math.exp(0.5 * (lo + hi))
        bad = 0.0; nroot = 0; n_gt1_m = 0; n_gt1_0 = 0
        for r_ in ROWS:
            R_ = RES[r_["label"]]; D0 = np.array(R_["D"]); gb = np.array(R_["GB"]); n_gt1_m += int(np.median(D0) > 1); n_gt1_0 += int(np.median(main[r_["label"]]["D"]) > 1)
            if R_["status"] == "root" and len(D0) == 1: nroot += 1; bad = max(bad, abs(math.log10(gb[0] / inv_nu(D0[0]) / A0C) - R_["ls"]))
            elif R_["status"] == "root":                                      # three rows: the root of the median residual; check it solves it
                res = np.log10(D0 / NU(gb / (A0C * 10 ** R_["ls"]))); nroot += 1; bad = max(bad, abs(float(np.median(res))) / 1.0)
        check("M2 MUTATE=1 (reactivity; the count is of rows with median D > 1, not of roots): V and sigma0 x 2, M_rot x 4; rows with status ROOT satisfy the independent inversion of their own (D, g_bar) (closed form for one radius, the residual's zero for three) to 1e-6 and the number of rows with median D > 1 is at least the main run's",
              f"rows with median D > 1: mutated {n_gt1_m}, main {n_gt1_0}; rows with a root {nroot}; max inversion residual {bad:.1e}", bad < 1e-6 and n_gt1_m >= n_gt1_0)
    else:
        d1m = 0.0
        for r_ in ROWS:
            R_ = RES[r_["label"]]
            if R_["status"] != "root": continue
            la, ua = H.AI.implied(np.array(R_["D"])[None, :], np.array(R_["GB"])[None, :], NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for r_ in ROWS if RES[r_['label']]['status'] == 'root')} rows with a root)", d1m < 1e-9)
        ok3 = [RES[r_["label"]]["role"] for r_ in ROWS] == ["headline", "headline"] + ["sensitivity"] * 4 and [len(RES[r_["label"]]["R"]) for r_ in ROWS] == [1, 1, 3, 3, 1, 1]
        check("M3 the six rows are present with their roles (two headline, four sensitivity) and radii (1, 1, 3, 3, 1, 1)", f"{[(RES[r_['label']]['role'], len(RES[r_['label']]['R'])) for r_ in ROWS]}", ok3)
        if not SELFTEST:
            Mtab = rings["Mdyn_msun"].values.astype(float); Mcalc = VK ** 2 * RING_R / H.G_KPC; rel = np.abs(Mcalc / Mtab - 1)
            check("M5 V^2 R / G reproduces the corpus's M_dyn of the three rings to within 5 % (the table prints two to three digits)", f"V^2 R / G = {np.array2string(Mcalc, precision=3)} against {np.array2string(Mtab, precision=3)}; relative differences {np.array2string(rel, precision=3)}", bool((rel <= 0.05).all()))
            m_c = re.search(r"sigma0=([0-9.]+) \(\+/-([0-9.]+)\)", str(l328["construction"].iloc[0]))
            check("M6 the Parlanti sigma and its error and M* and its error equal the L328 table's HZ9 row (sigma0 and its error parsed from the table's construction text; to 5e-5)", f"Parlanti sigma {SIGA} +- {ESIGA}; L328 construction sigma0 {m_c.group(1) if m_c else None} +- {m_c.group(2) if m_c else None}; M* {BR['M986']['lm']} +- {BR['M986']['elm']} vs {float(l328['logMstar'].iloc[0])} +- {float(l328['logMstar_err'].iloc[0])}; frozen constants sigma0 {SIG0} +- {ESIG0}, log M_rot {LMROT} +- {ELMROT} (Parlanti row: {LMR})",
                  bool(m_c) and abs(SIGA - float(m_c.group(1))) < 5e-5 and abs(ESIGA - float(m_c.group(2))) < 5e-5 and abs(SIGA - SIG0) < 5e-5 and abs(ESIGA - ESIG0) < 5e-5 and abs(LMR - LMROT) < 5e-5 and abs(BR["M986"]["lm"] - float(l328["logMstar"].iloc[0])) < 5e-5 and abs(BR["M986"]["elm"] - float(l328["logMstar_err"].iloc[0])) < 5e-5)
            same_j = len(jrings) == 3 and np.allclose(jrings["vrot_kms"].values, VK, atol=1e-9) and np.allclose(jrings["vrot_kms_err"].values, EVK, atol=1e-9) and np.allclose(jrings["sigma_kms"].values, rings["sigma_kms"].values, atol=1e-9) and np.allclose(jrings["sigma_kms_err"].values, rings["e_sigma_kms"].values, atol=1e-9)
            check("M7 (reported addition to the frozen list; a loader control) the corpus rings' V, its error, sigma and its error equal the Jones+21 A3 table's", f"identical {same_j}; ring sigma {np.array2string(rings['sigma_kms'].values.astype(float), precision=2)} (galaxy mean {float(np.mean(rings['sigma_kms'].values.astype(float))):.2f}; the third ring's 4.82 +- 8 is the suspect value)", bool(same_j), load_bearing=False)
        else:
            tested = [r_["label"] for r_ in ROWS if RES[r_["label"]]["status"] == "root" and not RES[r_["label"]]["ill"]]
            inside = [t for t in tested if np.isfinite(RES[t]["q"][0]) and RES[t]["q"][0] <= math.log10(2.0) <= RES[t]["q"][4]]
            check("SELFTEST: the conditioned rows with a root return the fabricated truth (s = 2) inside their 95 % interval for at least 4 of the 6 rows (the rows are correlated)", f"{len(inside)} of {len(tested)} conditioned rooted rows inside; rows: {[(t, 't' if t in inside else 'OUT') for t in tested]}", len(inside) >= 4)
            # 100-world repeat for the headline rows (reported)
            rep = {}
            for r_ in ROWS[:2]:
                inn = 0; nroot_w = 0
                for w in range(100):
                    rw = np.random.default_rng(100000 + 1000 * ROWS.index(r_) + w); gt = r_["gb0"] * NU(r_["gb0"] / (2.0 * A0C)) * 10 ** rw.normal(0, 0.15, 1); Vw = np.sqrt(gt * R_OUT / H.G2SI)
                    kin_w = dict(V=Vw, eV=0.10 * Vw); lsw, stw = H.s_status(gt / r_["gb0"], r_["gb0"]); qw, _, _, _ = mc_row(r_, kin_w, 1000, rw)
                    if stw == "root" and np.isfinite(qw[0]): nroot_w += 1; inn += int(qw[0] <= math.log10(2.0) <= qw[4])
                rep[r_["label"]] = (inn, nroot_w); P(f"  SELFTEST repeat (reported): {r_['label']}: the 95 % interval contains s = 2 in {inn} of {nroot_w} fabricated worlds with a root")
            NUM["selftest_repeat"] = rep
    # ---------------------------------------------------------------- hand estimates
    if not (MUTATE or SELFTEST):
        P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9; HE1-HE3 were scored at stage A) scored:")
        a, b = RES["HZ9 [M986]"], RES["HZ9 [M103]"]; ma, mb = RES["HZ9 [M986; Mrot]"], RES["HZ9 [M103; Mrot]"]
        m56 = [ok for n_, ok, lb in CHK if n_.startswith("M5") or n_.startswith("M6")]
        he = {"HE4": bool(3 <= b["D"][0] <= 6 and 8 <= a["D"][0] <= 16 and a["status"] == "root" and b["status"] == "root"),
              "HE5": bool(a["status"] == "root" and b["status"] == "root" and 8 <= b["s"] <= 30 and 20 <= a["s"] <= 120),
              "HE6": bool(np.isfinite(b["gas_to_star_req"]) and 1.5 <= b["gas_to_star_req"] <= 4),
              "HE7": bool(a["status_B2"] == "root" and b["status_B2"] == "root" and 2 <= b["s_B2"] <= 6 and 7 <= a["s_B2"] <= 25),
              "HE8": bool(0.05 <= b["g_head_over_rot_dex"] <= 0.09),
              "HE9": bool(abs(math.log10(ma["D"][0] / a["D"][0])) <= math.log10(1.5) and abs(math.log10(mb["D"][0] / b["D"][0])) <= math.log10(1.5)),
              "HE10": bool(len(m56) == 2 and all(m56))}
        P(f"    HE4: outer-ring D(B0) {b['D'][0]:.2f} (M103; needs 3-6) and {a['D'][0]:.2f} (M986; needs 8-16), statuses {b['status']} / {a['status']}: {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5: s* upper bounds {b['s']:.3g} (M103; needs 8-30) and {a['s']:.3g} (M986; needs 20-120): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6: gas-to-stars ratio for s* = 1 (M103) {b['gas_to_star_req']:+.2f} (needs 1.5-4): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        P(f"    HE7: B2 statuses {b['status_B2']} / {a['status_B2']}, s*(B2) {b['s_B2']:.3g} (M103; needs 2-6) and {a['s_B2']:.3g} (M986; needs 7-25): {'hit' if he['HE7'] else 'MISS (kept as it falls)'}")
        P(f"    HE8: the pressure term raises the outer-ring g_obs by {b['g_head_over_rot_dex']:.3f} dex (needs 0.05-0.09): {'hit' if he['HE8'] else 'MISS (kept as it falls)'}")
        P(f"    HE9: D(Mrot)/D(outer) = {ma['D'][0] / a['D'][0]:.2f} (M986), {mb['D'][0] / b['D'][0]:.2f} (M103) (needs 1/1.5-1.5): {'hit' if he['HE9'] else 'MISS (kept as it falls)'}")
        P(f"    HE10: M5 and M6 {'hold' if he['HE10'] else 'do not both hold'}: {'hit' if he['HE10'] else 'MISS (kept as it falls)'}")
        NUM["hand_estimates_B"] = he
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling",
                              "star_in_lo", "star_in_hi", "star_out_lo", "star_out_hi", "delta_floor", "delta_to_s1", "gas_to_star_req", "s_B2", "status_B2", "status", "branch", "route", "role", "R_kpc", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    for r_ in ROWS:
        R_ = RES[r_["label"]]; st = R_["status"]; q = R_["q"]
        bands = {float(k): (v["ls"], v["unb"]) for k, v in R_["bands"].items()}; b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        empty = 1000.0 if st == "ceiling" else FLOOR
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(Z0, lo95, hi95, b15[:2], b30[:2], st == "root"); half = R_["recipe_half"]
        sb_ = {float(k): (v["ls"], v["unb"]) for k, v in R_["star_bands"].items()}; si = H.band_edges(sb_, -0.15, 0.15); so = H.band_edges(sb_, -0.30, 0.30)
        extra = [float(np.median(R_["y"])), R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D_med"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], si[0], si[1], so[0], so[1], R_["delta_floor"], R_["delta_to_s1"], R_["gas_to_star_req"], R_["s_B2"], R_["status_B2"], st,
                 R_["branch"], R_["route"], R_["role"], "/".join(f"{v:g}" for v in R_["R"])]
        q_ = ("ILL-CONDITIONED; " if R_["ill"] else "") + {"root": "has a root with stars-only baryons: s* is an UPPER bound", "floor": "FLOOR: no root, D <= 1 (stars alone exceed the dynamics): robust against any added gas", "ceiling": f"CEILING: median D = {R_['D_med']:.1f} > 1 but s* > 1000: vacuous upper bound, NOT a floor"}[st] \
            + "; BEAM-LIMITED (all rings inside one beam); rotation interpretation weak (W15 2 of 5); third-ring sigma suspect; M* branch " + R_["branch"] + (" (sensitivity row)" if R_["role"] == "sensitivity" else "")
        sstar = R_["s"]
        rows.append(["CFG271", R_["label"], "D (no gas; stars-only lower limit)", f"{Z0:.4f}", f"{Z0:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_["n_knobs_with_root"],
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], "baryons are a lower limit: s* is an upper bound", fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg271_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg271_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg271{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg271{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
