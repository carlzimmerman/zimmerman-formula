#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG277 -- implied-a0 estimates (upper bounds or floors) for the four Roman-Oliveira+23 [CII] discs (z 4.26-4.43): measured CO gas (class S), stars missing; J081740's corpus M* as a separate branch.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG277_roman_oliveira_four_discs/FROZEN_CRITERIA.md (e591b71c1).
  rows      J081740 [gas], J081740 [gas+M*], BRI1335-0417 [gas], SGP38326-1 [gas], SGP38326-2 [gas] (headline); J081740 [FIR gas], J081740 [CII gas] (sensitivity)
  g_obs     (V_ext^2 + 3.36 sigma_ext^2) / r_ext, r_ext = (N - 1) RADSEP kpc/arcsec (CFG197's committed constants); g_bar = f_enc G (M_gas [+ M*]) / r_ext^2 with f_enc = 0.5
  STAGE=A   the blind pre-flight: no velocity-bearing column is loaded; no g_obs, D, delta or s* is formed.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (V_ext and sigma_ext x 2); STAGE=B SELFTEST=1 (fabricated V_ext on the law at s = 2).
Run: STAGE=A python3 .../cfg277_roman_oliveira.py ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
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
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: V_ext and sigma_ext x 2 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V_ext on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
B_MC = 10000
ALPHA = 3.36                                                                 # the SINS pressure coefficient (the disc scale is not tabulated)
FENC = 0.5                                                                   # CFG197's enclosed fraction of the baryons
LOADVEL = (STAGE == "B") and not SELFTEST                                   # the SELFTEST never loads the real velocity-bearing columns
DA = os.path.join(REPO, "data_assembly")
SAMPP = os.path.join(DA, "arxiv_tables", "romanoliveira2023_sample.csv")
GASP = os.path.join(DA, "arxiv_tables", "romanoliveira2023_gasmasses.csv")
KINP = os.path.join(DA, "arxiv_tables", "romanoliveira2023_kinematics.csv")
MULTIP = os.path.join(DA, "multitracer_gas", "singles_multitracer_galaxies.csv")
GALP = os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_galaxies.csv")
RINGP = os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_rings.csv")
TEXP = os.path.join(os.path.dirname(REPO), "_external_data", "arxiv_src", "2005.09661", "J0817HDV4_Mergedwfig.tex")
C197P = os.path.join(CFG, "CFG197_gas_floor_highz", "CFG197_preflight_results.json")
RINGS = {"BRI1335-0417": (5, 0.15), "J081740": (4, 0.13), "SGP38326-1": (5, 0.13), "SGP38326-2": (3, 0.12)}      # (N rings, RADSEP arcsec): CFG197's committed constants
SIDS = list(RINGS)

samp = pd.read_csv(SAMPP, usecols=["id", "z", "kpc_per_arcsec", "beam_major_arcsec", "beam_minor_arcsec"]).set_index("id")
gas = pd.read_csv(GASP, usecols=["id", "mh2_msun", "e_mh2", "mh2_flag"]).set_index("id")
kin_cols = ["id"] + (["vrot_ext_kms", "vrot_ext_kms_errhi", "vrot_ext_kms_errlo", "sigma_ext_kms", "sigma_ext_kms_errhi", "sigma_ext_kms_errlo", "vext_over_sigma_ext"] if LOADVEL else [])
kin = pd.read_csv(KINP, usecols=kin_cols).set_index("id")
multi = pd.read_csv(MULTIP, usecols=["galaxy", "stated_gas_masses_and_conversions"]); multi = multi[multi["galaxy"].str.startswith("J081740")]
gal = pd.read_csv(GALP, usecols=["galaxy", "redshift", "log_mstar_msun"]); gal = gal[gal["galaxy"] == "J0817"].reset_index(drop=True)
tex = open(TEXP, encoding="utf-8", errors="ignore").read() if os.path.exists(TEXP) else ""
c197 = json.load(open(C197P))["numbers"]["roman_oliveira"]
P(f"tables: sample {H.sha(SAMPP)}, gas {H.sha(GASP)}, kinematics {H.sha(KINP)}, multitracer {H.sha(MULTIP)}, corpus galaxies {H.sha(GALP)}, Neeleman+20 TeX {H.sha(TEXP) if tex else 'MISSING'}; velocity-bearing columns loaded: {LOADVEL}")

mt = str(multi["stated_gas_masses_and_conversions"].iloc[0]) if len(multi) else ""
def _mt(tag):
    m = re.search(tag + r" ([0-9.]+)\+-([0-9.]+)e10", mt)
    return (float(m.group(1)) * 1e10, float(m.group(2)) * 1e10) if m else (float("nan"), float("nan"))
MT_CO, MT_FIR, MT_CII = _mt("CO"), _mt("FIR"), _mt(r"\[CII\]")
LMS_J = float(gal["log_mstar_msun"].iloc[0]) if len(gal) else float("nan")

Z = {s: float(samp.loc[s, "z"]) for s in SIDS}
KPA = {s: float(samp.loc[s, "kpc_per_arcsec"]) for s in SIDS}
R_PRI = {s: (RINGS[s][0] - 1.0) * RINGS[s][1] * KPA[s] for s in SIDS}
R_VAR = {s: (RINGS[s][0] - 1.5) * RINGS[s][1] * KPA[s] for s in SIDS}
BEAM_KPC = {s: math.sqrt(float(samp.loc[s, "beam_major_arcsec"]) * float(samp.loc[s, "beam_minor_arcsec"])) * KPA[s] for s in SIDS}
GAS_M = {s: (float(gas.loc[s, "mh2_msun"]), float(gas.loc[s, "e_mh2"]) if np.isfinite(float(gas.loc[s, "e_mh2"])) else float("nan")) for s in SIDS}


def sig_dex(m, e):
    """log10 sigma of a log-normal for a gas mass m with an absolute error e; 0.30 dex declared when no error is published"""
    return (e / m) / math.log(10.0) if np.isfinite(e) and e > 0 else 0.30


ROWS = [dict(label="J081740 [gas]", sid="J081740", gas="CO", star=False, role="headline", tracer="CO(2-1)", gcls="S (CO(2-1) at alpha_CO = 3.0; stars missing)"),
        dict(label="J081740 [gas+M*]", sid="J081740", gas="CO", star=True, role="headline", tracer="CO(2-1)", gcls="S (CO(2-1) at alpha_CO = 3.0) + corpus M*"),
        dict(label="BRI1335-0417 [gas]", sid="BRI1335-0417", gas="CO", star=False, role="headline", tracer="CO", gcls="S (CO; starburst quasar host; stars missing)"),
        dict(label="SGP38326-1 [gas]", sid="SGP38326-1", gas="CO", star=False, role="headline", tracer="CO", gcls="S (CO, approx mass; stars missing)"),
        dict(label="SGP38326-2 [gas]", sid="SGP38326-2", gas="CO", star=False, role="headline", tracer="CO", gcls="S (CO, approx mass; stars missing)"),
        dict(label="J081740 [FIR gas]", sid="J081740", gas="FIR", star=False, role="sensitivity", tracer="FIR continuum", gcls="L (FIR continuum, alpha_850 = 6.7e19; stars missing)"),
        dict(label="J081740 [CII gas]", sid="J081740", gas="CII", star=False, role="sensitivity", tracer="[CII] luminosity", gcls="S ([CII] at alpha_[CII] = 30; stars missing)")]
for r_ in ROWS:
    s_ = r_["sid"]; r_["z"] = Z[s_]; r_["r"] = R_PRI[s_]; r_["rvar"] = R_VAR[s_]
    m_, e_ = {"CO": GAS_M[s_], "FIR": MT_FIR, "CII": MT_CII}[r_["gas"]]
    r_["Mg"], r_["eMg"], r_["sg"] = m_, e_, sig_dex(m_, e_)
    r_["Ms"] = 10 ** LMS_J if r_["star"] else 0.0
    r_["gband"] = (0.213, 0.671); r_["sband"] = (0.15, 0.30)


def g_pt(M, r, f=FENC):
    """point-mass baryon acceleration of the enclosed fraction f of the mass M (Msun) at r (kpc), m s^-2"""
    return f * H.G_KPC * M / r ** 2 * H.G2SI


for r_ in ROWS:
    r_["gg0"] = g_pt(r_["Mg"], r_["r"]); r_["gs0"] = g_pt(r_["Ms"], r_["r"]) if r_["star"] else 0.0
    r_["gb0"] = r_["gg0"] + r_["gs0"]; r_["y0"] = r_["gb0"] / A0C
P("rows: " + "; ".join(f"{r_['label']}: r_ext {r_['r']:.3f} kpc, M_gas {r_['Mg']:.2e} (sigma {r_['sg']:.3f} dex)" + (f", M* {r_['Ms']:.2e}" if r_["star"] else "") for r_ in ROWS))

# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (no velocity-bearing column is loaded; no g_obs, D, delta or s* is formed)")
    kpa_dev = max(abs(KPA[s] / H.kpc_per_arcsec(Z[s]) - 1) for s in SIDS)
    tex_ok = all(t in tex for t in ("(8.8~$\\pm$~2.6)", "(5.7 $\\pm$ 0.7)", "(9.8 $\\pm$ 0.6)"))
    check("C1 CONTROL (loader): five ids in the sample and gas tables, the four kinematics ids, the sample table's kpc/arcsec equal to the programme's cosmology to 0.5 %, the corpus J0817 row with log M* 10.5, the multitracer and TeX gas masses (CO 8.8 +- 2.6e10, FIR 5.7 +- 0.7e10, [CII] 9.8 +- 0.6e10) present and equal to the tables",
          f"sample ids {list(samp.index)}; gas ids {list(gas.index)}; kinematics ids {list(kin.index)}; kpc/arcsec deviation {kpa_dev:.1e}; corpus J0817 rows {len(gal)}, log M* {LMS_J}; multitracer CO {MT_CO}, FIR {MT_FIR}, CII {MT_CII}; TeX strings found {tex_ok}",
          len(samp) == 5 and len(gas) == 5 and set(kin.index) == set(SIDS) and kpa_dev < 5e-3 and len(gal) == 1 and abs(LMS_J - 10.5) < 1e-9 and all(abs(x - y) <= 1e-9 * abs(y) for x, y in zip(MT_CO + MT_FIR + MT_CII, (8.8e10, 2.6e10, 5.7e10, 0.7e10, 9.8e10, 0.6e10))) and tex_ok
          and abs(GAS_M["J081740"][0] - 8.8e10) < 1 and abs(GAS_M["J081740"][1] - 2.6e10) < 1)
    dr = max(max(abs(R_PRI[s] / c197[f"{s}|primary|fg0.5|canonical"]["r_ext_kpc"] - 1), abs(R_VAR[s] / c197[f"{s}|variant|fg0.5|canonical"]["r_ext_kpc"] - 1)) for s in SIDS)
    dg = 0.0
    for s in SIDS:
        gg = g_pt(GAS_M[s][0], R_PRI[s]) / A0C; dg = max(dg, abs(gg / c197[f"{s}|primary|fg0.5|canonical"]["g_gas_over_a0"] - 1))
    check("C2 CONTROL (reproduction of CFG197's committed gas-only numbers): r_ext (primary and variant) to 1e-3 and g_gas/a0 at f_enc = 0.5 (canonical) to 1e-4, relative, for the four discs",
          f"max relative difference in r_ext {dr:.1e}; in g_gas/a0 {dg:.1e}; g_gas/a0: " + ", ".join(f"{s} {g_pt(GAS_M[s][0], R_PRI[s]) / A0C:.4f}" for s in SIDS), dr < 1e-3 and dg < 1e-4)
    check("C3 CONTROL: the multitracer row's CO mass and error equal the Roman-Oliveira M_H2 for J081740", f"multitracer {MT_CO}, table {GAS_M['J081740']}", abs(MT_CO[0] - GAS_M["J081740"][0]) <= 1e-9 * GAS_M["J081740"][0] and abs(MT_CO[1] - GAS_M["J081740"][1]) <= 1e-9 * GAS_M["J081740"][1])
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
            ls, unb = H.s_star(NU(np.array([r_["gb0"] / (A0C * st)])), np.array([r_["gb0"]])); d5 = max(d5, abs(ls - math.log10(st)) if not unb else 9.0)
    check("C5 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on every row's baryon side", f"max |d log10 s| {d5:.1e}", d5 < 1e-6)

    P("\nA1 / A2  BARYON SIDE AND THE CFG240 READING (noiseless world; point mass, f_enc = 0.5; ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    for r_ in ROWS:
        lv, fl = H.lever1(NU(np.array([r_["y0"]])), np.array([r_["gb0"]])); r_["lever"], r_["ill"] = lv, bool(fl or abs(lv) >= 10)
        P(f"    {r_['label']:22s} z {r_['z']:.3f} r_ext {r_['r']:.3f} kpc: g_bar {r_['gb0']:.3e} m/s^2, y = {r_['y0']:.2f}, lever {lv:+.2f}{' (not computable)' if fl else ''}  {'ILL-CONDITIONED' if r_['ill'] else 'conditioned'}")
    ys = [r_["y0"] for r_ in ROWS]
    P(f"    CFG240: T3 (the a0 dependence disappears at large y): y(B0) runs {min(ys):.1f}-{max(ys):.1f}, near-Newtonian for every row; T4 floor 3 sigma / sqrt(N) at sigma = 0.2 dex is {3 * 0.2:.2f} dex for N = 1; the break-even design needs y >~ 8 with deep points (y < 0.3): none here")
    P("\nA3  KNOB EFFECTS ON g_bar (dex relative to the primary; f_enc, helium, radius)")
    for r_ in ROWS[:5]:
        P(f"    {r_['label']:22s} f_enc 0.25 {np.log10(0.25 / FENC):+.3f}, f_enc 1.0 {np.log10(1.0 / FENC):+.3f}, helium x1.36 on the gas {np.log10((1.36 * r_['gg0'] + r_['gs0']) / r_['gb0']):+.3f}, radius variant {np.log10(g_pt(r_['Mg'] + r_['Ms'], r_['rvar']) / g_pt(r_['Mg'] + r_['Ms'], r_['r'])):+.3f} (r {r_['rvar']:.3f} kpc)")
    P("\nA4  r_ext AGAINST THE ALMA BEAM (geometric-mean FWHM from the sample table, in kpc)")
    for s in SIDS: P(f"    {s:14s} r_ext {R_PRI[s]:.3f} kpc, beam {BEAM_KPC[s]:.3f} kpc, ratio {R_PRI[s] / BEAM_KPC[s]:.2f} (variant radius {R_VAR[s]:.3f}: {R_VAR[s] / BEAM_KPC[s]:.2f})")
    P("\nA5  THE J081740 STELLAR-MASS BRANCH")
    rg, rs = ROWS[0], ROWS[1]; P(f"    y {rg['y0']:.2f} [gas] -> {rs['y0']:.2f} [gas+M*] (log M* {LMS_J}, M* {rs['Ms']:.2e} against M_gas {rs['Mg']:.2e}); the corpus value has no source or error; Roman-Oliveira say there is none")
    P("\nC6  COVERAGE (noiseless world on each non-ILL row's baryons; a declared 0.15 dex on g_obs and the row's gas error; 100 mocks, B = 1,000)")
    rng6 = np.random.default_rng(277); cov = {}
    for r_ in ROWS:
        if r_["ill"]: continue
        gob_true = float(r_["gb0"] * NU(np.array([r_["y0"]]))[0]); c68 = c95 = nd = 0
        for it in range(100):
            god = gob_true * 10 ** rng6.normal(0, 0.15); gobm = god * 10 ** rng6.normal(0, 0.15, 1000)
            Mg_o = r_["Mg"] * 10 ** rng6.normal(0, r_["sg"]); Mgd = Mg_o * 10 ** rng6.normal(0, r_["sg"], 1000)
            Msd = (r_["Ms"] * 10 ** rng6.normal(0, 0.30, 1000)) if r_["star"] else 0.0
            gbd = g_pt(Mgd + Msd, r_["r"]); lsd, ud = H.AI.implied((gobm / gbd)[:, None], gbd[:, None], NU, A0C); q, fr = H.rooted_pct(lsd, ud)
            if np.isfinite(q[0]): nd += 1; c68 += (q[1] <= 0.0 <= q[3]); c95 += (q[0] <= 0.0 <= q[4])
        cov[r_["label"]] = (c68 / max(nd, 1), c95 / max(nd, 1), nd); P(f"    {r_['label']}: 68 % coverage {cov[r_['label']][0]:.2f}, 95 % coverage {cov[r_['label']][1]:.2f} (mocks with a root {nd} of 100)")
    if cov:
        check("C6 (reported; load-bearing for the conditioned rows): the 68 % and 95 % coverage of the conditioned rows are >= 60 % and >= 88 %", "; ".join(f"{k}: {c[0]:.2f} / {c[1]:.2f}" for k, c in cov.items()), all(c[0] >= 0.60 and c[1] >= 0.88 for c in cov.values()), load_bearing=False)
    else: P("    no conditioned row: coverage not applicable")
    pfd1 = all(ok for n, ok, lb in CHK if lb and not n.startswith("C6"))
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C5)")
    P("  PF-D2 ILL-CONDITIONED rows: " + (", ".join(r_["label"] for r_ in ROWS if r_["ill"]) or "none"))
    P("  PF-D3 DRAWABLE as an estimate: " + (", ".join(r_["label"] for r_ in ROWS if pfd1 and not r_["ill"]) or "none"))
    P(f"  PF-D4 NEAR-NEWTONIAN (gas-only y >= 4): {all(y >= 4 for y in ys)} (y {min(ys):.1f}-{max(ys):.1f}; reported, not blocking: the measurement is run and the label travels with the rows)")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9) scored (HE4-HE9 are scored at stage B):")
    he = {}
    he["HE1"] = bool([r_["label"] for r_ in ROWS[:5] if not r_["ill"]] == ["BRI1335-0417 [gas]"])
    ratios = {s: R_PRI[s] / BEAM_KPC[s] for s in SIDS}
    he["HE2"] = bool(all(v > 1.0 for v in ratios.values()) and min(ratios, key=ratios.get) == "SGP38326-2" and 1.0 <= ratios["SGP38326-2"] <= 2.0)
    he["HE3"] = bool(1.2 <= ROWS[1]["y0"] / ROWS[0]["y0"] <= 1.5)
    for k, v in he.items(): P(f"    {k}: {'hit' if v else 'MISS (kept as it falls)'}")
    NUM.update(inputs=dict(r_pri=R_PRI, r_var=R_VAR, beam_kpc=BEAM_KPC, z=Z, kpa=KPA, gas=GAS_M, mt=dict(CO=MT_CO, FIR=MT_FIR, CII=MT_CII), log_mstar_corpus=LMS_J),
               rows={r_["label"]: dict(r=r_["r"], Mg=r_["Mg"], Ms=r_["Ms"], gb0=r_["gb0"], y0=r_["y0"], lever=r_["lever"], ill=r_["ill"]) for r_ in ROWS}, coverage={k: list(v) for k, v in cov.items()}, hand_estimates=he, pf=dict(PF_D1=bool(pfd1)))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V_ext and sigma_ext x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2770)
    KIN = {}
    for r_ in ROWS:
        s_ = r_["sid"]
        if SELFTEST:
            g_t = r_["gb0"] * float(NU(np.array([r_["gb0"] / (2.0 * A0C)]))[0]) * 10 ** rngS.normal(0, 0.15); Vf = math.sqrt(g_t * r_["r"] / H.G2SI)
            KIN[r_["label"]] = dict(V=Vf, eVhi=0.10 * Vf, eVlo=0.10 * Vf, S=0.0, eShi=0.0, eSlo=0.0)
        else:
            k_ = kin.loc[s_]; mult = 2.0 if MUTATE else 1.0
            KIN[r_["label"]] = dict(V=mult * float(k_["vrot_ext_kms"]), eVhi=mult * float(k_["vrot_ext_kms_errhi"]), eVlo=mult * float(k_["vrot_ext_kms_errlo"]), S=mult * float(k_["sigma_ext_kms"]), eShi=mult * float(k_["sigma_ext_kms_errhi"]), eSlo=mult * float(k_["sigma_ext_kms_errlo"]))

    def gobs_of(r_, kk, rr, alpha=ALPHA, V=None, S=None):
        Vv = kk["V"] if V is None else V; Ss = kk["S"] if S is None else S
        return (Vv ** 2 + alpha * Ss ** 2) / rr * H.G2SI

    def gbar_of(r_, rr, f=FENC, he=1.0, Mg=None, Ms=None):
        Mg = r_["Mg"] if Mg is None else Mg; Ms = r_["Ms"] if Ms is None else Ms
        return g_pt(he * Mg + Ms, rr, f)

    def mc_row(r_, kk, B, rng):
        Vd = H.split_normal(rng, kk["V"], kk["eVhi"], kk["eVlo"], B); Sd = np.maximum(H.split_normal(rng, kk["S"], kk["eShi"], kk["eSlo"], B), 0.0)
        Mg_d = r_["Mg"] * 10 ** rng.normal(0, r_["sg"], B); Ms_d = (r_["Ms"] * 10 ** rng.normal(0, 0.30, B)) if r_["star"] else 0.0
        god = gobs_of(r_, kk, r_["r"], V=Vd, S=Sd); gbd = g_pt(Mg_d + Ms_d, r_["r"]); Dd = god / gbd
        lsd, ud = H.AI.implied(Dd[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud); frc = float(np.mean(ud & (Dd > 1.0)))
        dFd = np.log10(god / (gbd * NU(gbd / A0C))); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        return q, frn, frc, dq

    KGR = {"pressure: alpha = 0 (CFG197 primary)": "pressure", "pressure: alpha = 1.68": "pressure", "radius: (N - 1.5) RADSEP": "radius", "geometry: f_enc = 0.25": "geometry", "geometry: f_enc = 1.0": "geometry", "helium x1.36 on the gas": "gas", "kernel P2": "kernel"}
    KN_LIST = list(KGR)
    RES = {}
    for r_ in ROWS:
        lab = r_["label"]; kk = KIN[lab]
        GO = gobs_of(r_, kk, r_["r"]); GO_ROT = gobs_of(r_, kk, r_["r"], alpha=0.0); gb0 = r_["gb0"]; D0 = GO / gb0
        ls0, st0 = H.s_status(np.array([D0]), np.array([gb0]))
        rng = np.random.default_rng(zlib.crc32(("277|" + lab).encode()) % 100000)
        q, frn, frc, dq = mc_row(r_, kk, B_MC, rng)
        dF0 = float(np.log10(GO / (gb0 * float(NU(np.array([gb0 / A0C]))[0]))))
        # bands: gas inner +-0.213 / outer +-0.671, stars inner +-0.15 / outer +-0.30, joint = same sign; plus the class-D style all-baryon corners
        def corner(sg, ss):
            gbp = r_["gg0"] * 10 ** sg + r_["gs0"] * 10 ** ss; l_, s_t = H.s_status(np.array([GO / gbp]), np.array([gbp])); return H.s_val_status(l_, s_t), s_t
        band = {}
        for lvl, (sg, ss) in (("inner", (0.213, 0.15)), ("outer", (0.671, 0.30))):
            cm, cp = corner(-sg, -ss), corner(+sg, +ss)
            band[lvl] = dict(lo=min(cm[0], cp[0]), hi=max(cm[0], cp[0]), noroot=int(cm[1] != "root" or cp[1] != "root"), s_minus=cm[0], s_plus=cp[0], st_minus=cm[1], st_plus=cp[1])
        allb = {}
        for lvl, sh in (("inner", 0.15), ("outer", 0.30)):
            gm, gp = gb0 * 10 ** (-sh), gb0 * 10 ** sh; lm, sm = H.s_status(np.array([GO / gm]), np.array([gm])); lp, sp = H.s_status(np.array([GO / gp]), np.array([gp]))
            allb[lvl] = dict(lo=min(H.s_val_status(lm, sm), H.s_val_status(lp, sp)), hi=max(H.s_val_status(lm, sm), H.s_val_status(lp, sp)))
        kn = {}

        def variant(nm):
            if nm == "pressure: alpha = 0 (CFG197 primary)": return GO_ROT, gb0, NU
            if nm == "pressure: alpha = 1.68": return gobs_of(r_, kk, r_["r"], alpha=1.68), gb0, NU
            if nm == "radius: (N - 1.5) RADSEP": return gobs_of(r_, kk, r_["rvar"]), gbar_of(r_, r_["rvar"]), NU
            if nm == "geometry: f_enc = 0.25": return GO, gbar_of(r_, r_["r"], f=0.25), NU
            if nm == "geometry: f_enc = 1.0": return GO, gbar_of(r_, r_["r"], f=1.0), NU
            if nm == "helium x1.36 on the gas": return GO, gbar_of(r_, r_["r"], he=1.36), NU
            if nm == "kernel P2": return GO, gb0, NUP2
        for nm in KN_LIST:
            go_, gb_, nu_ = variant(nm); lk, sk = H.s_status(np.array([go_ / gb_]), np.array([gb_]), nu_)
            kn[nm] = None if (st0 != "root" or sk != "root") else lk - ls0; kn[nm + "|status"] = sk
        grp = {}
        for nm in KN_LIST:
            if kn.get(nm) is not None: grp.setdefault(KGR[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        n_root = sum(1 for nm in KN_LIST if kn.get(nm + "|status") == "root")
        lv_nl, lf_nl = H.lever1(NU(np.array([gb0 / A0C])), np.array([gb0])); d1 = H.shift_to_s1(np.array([D0]), np.array([gb0]))
        RES[lab] = dict(label=lab, sid=r_["sid"], role=r_["role"], tracer=r_["tracer"], z=r_["z"], r_kpc=r_["r"], Mg=r_["Mg"], Ms=r_["Ms"], GO=GO, GO_rot=GO_ROT, GB=gb0, D=D0, y=r_["y0"], ls=ls0, status=st0, s=H.s_val_status(ls0, st0), q=q, frac_mc_noroot=frn, frac_mc_ceiling=frc,
                        delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1], band=band, allb=allb, knobs=kn, recipe_half=half, n_knobs_with_root=n_root, lever=lv_nl, ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=H.delta_floor(np.array([D0])),
                        delta_to_s1=d1, baryon_ratio_req=(10 ** d1 - 1 if np.isfinite(d1) else float("nan")), g_head_over_rot_dex=float(np.log10(GO / GO_ROT)))
        R_ = RES[lab]
        b0 = (f"s* <= {10 ** ls0:.3g}" if st0 == "root" else ("FLOOR (D <= 1)" if st0 == "floor" else "CEILING (s* > 1000)"))
        qs = f"68 % [{10 ** q[1]:.3g}, {10 ** q[3]:.3g}] 95 % [{10 ** q[0]:.3g}, {10 ** q[4]:.3g}]" if np.isfinite(q[0]) else "no draw interval (< 20 rooted draws)"
        P(f"  {lab:22s} r {r_['r']:.2f}: g_obs {GO:.3e} (rot-only {GO_ROT:.3e})  g_bar {gb0:.3e}  D {D0:.3f}  dF {dF0:+.3f}  y {r_['y0']:.2f}  {b0}; MC {qs} (no root {frn:.2f}, ceiling {frc:.2f}); baryon ratio for s* = 1: {R_['baryon_ratio_req']:+.2f}; recipe half-width {half:.3f}; band inner [{band['inner']['lo']:.3g}, {band['inner']['hi']:.3g}] outer [{band['outer']['lo']:.3g}, {band['outer']['hi']:.3g}]{' ILL' if R_['ill'] else ''}")
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg277_stageB_results.json")))["numbers"]["rows"]
        def inv_nu(Dv):
            lo, hi = -25.0, 25.0
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if float(NU(np.array([math.exp(mid)]))[0]) > Dv: lo = mid
                else: hi = mid
            return math.exp(0.5 * (lo + hi))
        bad = 0.0; nroot = 0; n_gt1_m = 0; n_gt1_0 = 0
        for r_ in ROWS:
            R_ = RES[r_["label"]]; n_gt1_m += int(R_["D"] > 1); n_gt1_0 += int(main[r_["label"]]["D"] > 1)
            if R_["status"] == "root": nroot += 1; bad = max(bad, abs(math.log10(R_["GB"] / inv_nu(R_["D"]) / A0C) - R_["ls"]))
        check("M2 MUTATE=1 (reactivity; the count is of rows with D > 1, not of roots): V_ext and sigma_ext x 2; rows with status ROOT satisfy the closed-form inversion of their own (D, g_bar) to 1e-6 dex and the number of rows with D > 1 is at least the main run's",
              f"rows with D > 1: mutated {n_gt1_m}, main {n_gt1_0}; rows with a root {nroot}; max |d log10 s*| against the independent inversion {bad:.1e}", bad < 1e-6 and n_gt1_m >= n_gt1_0)
    else:
        d1m = 0.0
        for r_ in ROWS:
            R_ = RES[r_["label"]]
            if R_["status"] != "root": continue
            la, ua = H.AI.implied(np.array([[R_["D"]]]), np.array([[R_["GB"]]]), NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for r_ in ROWS if RES[r_['label']]['status'] == 'root')} rows with a root)", d1m < 1e-9)
        check("M3 the seven rows are present with their branches and tracers (five headline, two sensitivity)", f"{[(RES[r_['label']]['role'], RES[r_['label']]['tracer']) for r_ in ROWS]}", [RES[r_["label"]]["role"] for r_ in ROWS] == ["headline"] * 5 + ["sensitivity"] * 2)
        if not SELFTEST:
            rj = pd.read_csv(RINGP, usecols=["galaxy", "Vrot_kms"]); rj = rj[rj["galaxy"] == "J0817"]["Vrot_kms"].values.astype(float)
            vext = float(kin.loc["J081740", "vrot_ext_kms"]); rel5 = abs(vext / float(np.mean(rj)) - 1)
            check("M5 Roman-Oliveira's V_ext for J081740 equals the mean of the corpus rings' V (two on-disk fits of one galaxy) to within 5 %", f"V_ext {vext} against the ring mean {float(np.mean(rj)):.2f} (rings {np.array2string(rj, precision=2)}); relative difference {rel5:.3f}", rel5 <= 0.05)
            rr6 = {s: abs(float(kin.loc[s, "vrot_ext_kms"]) / float(kin.loc[s, "sigma_ext_kms"]) / float(kin.loc[s, "vext_over_sigma_ext"]) - 1) for s in SIDS}
            check("M6 V_ext / sigma_ext reproduces the table's vext_over_sigma_ext to within 2 % for the four discs (the table prints one decimal)", "; ".join(f"{s} {float(kin.loc[s, 'vrot_ext_kms']) / float(kin.loc[s, 'sigma_ext_kms']):.2f} vs {float(kin.loc[s, 'vext_over_sigma_ext'])} (diff {v:.3f})" for s, v in rr6.items()), max(rr6.values()) <= 0.02)
        else:
            tested = [r_["label"] for r_ in ROWS if RES[r_["label"]]["status"] == "root" and not RES[r_["label"]]["ill"]]
            inside = [t for t in tested if np.isfinite(RES[t]["q"][0]) and RES[t]["q"][0] <= math.log10(2.0) <= RES[t]["q"][4]]
            if tested: check("SELFTEST: every row that is conditioned and has a root returns the fabricated truth (s = 2) inside its 95 % interval", f"{len(inside)} of {len(tested)}: {[(t, 'in' if t in inside else 'OUT') for t in tested]}", len(inside) == len(tested))
            else: P("  SELFTEST: no conditioned row with a root: truth recovery not applicable")
            P("  SELFTEST statuses: " + "; ".join(f"{r_['label']}: {RES[r_['label']]['status']}" + (f" s* {RES[r_['label']]['s']:.3g}" if RES[r_['label']]['status'] == 'root' else "") + (" ILL" if RES[r_["label"]]["ill"] else "") for r_ in ROWS))
    if not (MUTATE or SELFTEST):
        P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9; HE1-HE3 were scored at stage A) scored:")
        Rr = RES; b, j, jm, s1, s2, fir, cii = (Rr["BRI1335-0417 [gas]"], Rr["J081740 [gas]"], Rr["J081740 [gas+M*]"], Rr["SGP38326-1 [gas]"], Rr["SGP38326-2 [gas]"], Rr["J081740 [FIR gas]"], Rr["J081740 [CII gas]"])
        m56 = [ok for n_, ok, lb in CHK if n_.startswith("M5") or n_.startswith("M6")]
        he = {"HE4": bool(b["status"] == "floor" and 0.35 <= b["D"] <= 0.8),
              "HE5": bool(j["status"] == "floor" and jm["status"] == "floor" and 0.6 <= j["D"] <= 1.2 and 0.45 <= jm["D"] <= 0.9),
              "HE6": bool(s1["status"] == "root" and s2["status"] == "root" and 2 <= s1["D"] <= 3.5 and 1.3 <= s2["D"] <= 2.3 and 30 <= s1["s"] <= 90 and 40 <= s2["s"] <= 130 and s1["ill"] and s2["ill"]),
              "HE7": bool(0.15 <= b["g_head_over_rot_dex"] <= 0.30 and all(Rr[k]["g_head_over_rot_dex"] < 0.05 for k in ("J081740 [gas]", "SGP38326-1 [gas]", "SGP38326-2 [gas]"))),
              "HE8": bool(fir["status"] == "root" and 2 <= fir["s"] <= 8 and cii["status"] == "floor"),
              "HE9": bool(len(m56) == 2 and all(m56))}
        P(f"    HE4: BRI1335-0417 {b['status']}, D {b['D']:.3f} (needs a floor and D in 0.35-0.8): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5: J081740 [gas] {j['status']} D {j['D']:.3f} (0.6-1.2), [gas+M*] {jm['status']} D {jm['D']:.3f} (0.45-0.9): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6: SGP38326-1 {s1['status']} D {s1['D']:.2f} s* <= {s1['s']:.3g} ILL {s1['ill']}; SGP38326-2 {s2['status']} D {s2['D']:.2f} s* <= {s2['s']:.3g} ILL {s2['ill']} (needs D 2-3.5 / 1.3-2.3, s* 30-90 / 40-130, both ILL): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        P(f"    HE7: alpha = 0 lowers g_obs by {b['g_head_over_rot_dex']:.3f} dex (BRI1335-0417; needs 0.15-0.30) and by {j['g_head_over_rot_dex']:.3f} / {s1['g_head_over_rot_dex']:.3f} / {s2['g_head_over_rot_dex']:.3f} dex (J081740, SGP-1, SGP-2; each < 0.05): {'hit' if he['HE7'] else 'MISS (kept as it falls)'}")
        P(f"    HE8: J081740 [FIR gas] {fir['status']}" + (f" s* <= {fir['s']:.3g}" if fir['status'] == 'root' else "") + f" (needs a root in 2-8); [CII gas] {cii['status']} (needs a floor): {'hit' if he['HE8'] else 'MISS (kept as it falls)'}")
        P(f"    HE9: M5 and M6 {'hold' if he['HE9'] else 'do not both hold'}: {'hit' if he['HE9'] else 'MISS (kept as it falls)'}")
        NUM["hand_estimates_B"] = he
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling",
                              "allb_in_lo", "allb_in_hi", "allb_out_lo", "allb_out_hi", "delta_floor", "delta_to_s1", "baryon_ratio_req", "status", "tracer", "role", "r_ext_kpc", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    for r_ in ROWS:
        R_ = RES[r_["label"]]; st = R_["status"]; q = R_["q"]; bi, bo = R_["band"]["inner"], R_["band"]["outer"]
        empty = 1000.0 if st == "ceiling" else FLOOR
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(R_["z"], lo95, hi95, (bi["lo"], bi["hi"]), (bo["lo"], bo["hi"]), st == "root"); half = R_["recipe_half"]
        extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], R_["allb"]["inner"]["lo"], R_["allb"]["inner"]["hi"], R_["allb"]["outer"]["lo"], R_["allb"]["outer"]["hi"],
                 R_["delta_floor"], R_["delta_to_s1"], R_["baryon_ratio_req"], st, R_["tracer"], R_["role"], R_["r_kpc"]]
        q_ = ("ILL-CONDITIONED (near-Newtonian); " if R_["ill"] else "near-Newtonian baryon side (CFG240 T3); ") + {"root": "has a root: an upper bound only if the gas mass is right (class S/L, stars missing)", "floor": "FLOOR: no root, D <= 1 (the baryons already exceed the dynamics): robust against added stars, not against a lower alpha_CO",
                                                                                         "ceiling": f"CEILING: D = {R_['D']:.1f} > 1 but s* > 1000: vacuous"}[st] + ("; corpus M* branch (source unrecorded)" if r_["star"] else "") + ("; sensitivity row" if r_["role"] == "sensitivity" else "")
        sstar = R_["s"]
        rows.append(["CFG277", r_["label"], r_["gcls"], f"{R_['z']:.4f}", f"{R_['z']:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{bi['lo']:.6g}", f"{bi['hi']:.6g}", bi["noroot"], f"{bo['lo']:.6g}", f"{bo['hi']:.6g}", bo["noroot"], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_["n_knobs_with_root"],
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], "gas is class S/L and stars are missing: not a limit unless the gas mass is right", fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg277_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg277_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg277{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg277{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
