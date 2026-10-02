#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG282 -- CFG277's Roman-Oliveira+23 [CII] discs (SGP38326-1, SGP38326-2, BRI1335-0417) with the literature SED stellar masses added: gas (CFG277's CO masses, class S) + SED stars, five rows never pooled.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG282_ro_stellar_masses/FROZEN_CRITERIA.md (3af1cf10d, corrected in section 9 by e111bcc30: provenance wording only).
  rows     SGP38326-1 [gas+M* T26 11.04] / [gas+M* Ma19 11.52]; SGP38326-2 [T26 11.39] / [Ma19 11.27]; BRI1335-0417 [T26 12.05, AGN-included, unconstrained]
  g_obs    (V_ext^2 + 3.36 sigma_ext^2) / r_ext;  g_bar = 0.5 G (M_gas + M*) / r_ext^2 (CFG197's point-mass geometry, f_enc = 0.5);  CFG223's s*
  STAGE=A  the blind pre-flight (no velocity-bearing column loaded).  STAGE=B  the measurement (once, after stage A, the SELFTEST and this script are committed); STAGE=B SELFTEST=1; STAGE=B MUTATE=1 (V_ext, sigma_ext x 2).
Run: STAGE=A python3 .../cfg282_ro_stellar.py ; STAGE=B SELFTEST=1 python3 ... ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, json, math, time, zlib
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
    P(f"  [{'PASS' if ok else 'FAIL'}{'' if load_bearing else ' (not load-bearing)'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: V_ext and sigma_ext x 2 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V_ext on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
B_MC = 10000
ALPHA, FENC, SIGM = 3.36, 0.5, 0.30
LOADVEL = (STAGE == "B") and not SELFTEST
DA = os.path.join(REPO, "data_assembly")
SAMPP = os.path.join(DA, "arxiv_tables", "romanoliveira2023_sample.csv")
GASP = os.path.join(DA, "arxiv_tables", "romanoliveira2023_gasmasses.csv")
KINP = os.path.join(DA, "arxiv_tables", "romanoliveira2023_kinematics.csv")
MSP = os.path.join(DA, "ro23_stellar_masses_2026-10-01", "ro23_stellar_masses.csv")
C197P = os.path.join(CFG, "CFG197_gas_floor_highz", "CFG197_preflight_results.json")
C277P = os.path.join(CFG, "CFG277_roman_oliveira_four_discs", "cfg277_stageB_results.json")
RINGS = {"BRI1335-0417": (5, 0.15), "SGP38326-1": (5, 0.13), "SGP38326-2": (3, 0.12)}      # (N rings, RADSEP arcsec): CFG197's committed constants
SIDS = list(RINGS)
samp = pd.read_csv(SAMPP, usecols=["id", "z", "kpc_per_arcsec"]).set_index("id")
gas = pd.read_csv(GASP, usecols=["id", "mh2_msun", "e_mh2", "mh2_flag"]).set_index("id")
kin_cols = ["id"] + (["vrot_ext_kms", "vrot_ext_kms_errhi", "vrot_ext_kms_errlo", "sigma_ext_kms", "sigma_ext_kms_errhi", "sigma_ext_kms_errlo"] if LOADVEL else [])
kin = pd.read_csv(KINP, usecols=kin_cols).set_index("id")
ms = pd.read_csv(MSP, usecols=["id", "log_mstar_msun", "err_lo", "err_hi", "limit_flag", "source_arxiv"])
c197 = json.load(open(C197P))["numbers"]["roman_oliveira"]
c277 = json.load(open(C277P))["numbers"]["rows"]
P(f"tables: sample {H.sha(SAMPP)}, gas {H.sha(GASP)}, kinematics {H.sha(KINP)}, stellar masses {H.sha(MSP)}; velocity-bearing columns loaded: {LOADVEL}")

ROWSPEC = [("SGP38326-1 [gas+M* T26]", "SGP38326-1", 11.04, "2609.30375", "TRICEPS I (Lelli+2026 preprint): JWST-based SED, method deferred to Paper II"),
           ("SGP38326-1 [gas+M* Ma19]", "SGP38326-1", 11.52, "1908.08043", "Ma+2019 MAGPHYS, blended pair, no AGN term, IRAC S/N 2-3"),
           ("SGP38326-2 [gas+M* T26]", "SGP38326-2", 11.39, "2609.30375", "TRICEPS I (Lelli+2026 preprint)"),
           ("SGP38326-2 [gas+M* Ma19]", "SGP38326-2", 11.27, "1908.08043", "Ma+2019 MAGPHYS, blended pair"),
           ("BRI1335-0417 [gas+M* T26]", "BRI1335-0417", 12.05, "2609.30375", "TRICEPS I, AGN-included, exceeds every dynamical mass: unconstrained")]
ROWS = [dict(label=l, sid=s, lms=lm, src=sa, srcnote=sn) for l, s, lm, sa, sn in ROWSPEC]
Z = {s: float(samp.loc[s, "z"]) for s in SIDS}
KPA = {s: float(samp.loc[s, "kpc_per_arcsec"]) for s in SIDS}
R_PRI = {s: (RINGS[s][0] - 1.0) * RINGS[s][1] * KPA[s] for s in SIDS}
R_VAR = {s: (RINGS[s][0] - 1.5) * RINGS[s][1] * KPA[s] for s in SIDS}
GAS_M = {s: (float(gas.loc[s, "mh2_msun"]), float(gas.loc[s, "e_mh2"]) if np.isfinite(float(gas.loc[s, "e_mh2"])) else float("nan")) for s in SIDS}


def sig_dex(m, e):
    return (e / m) / math.log(10.0) if np.isfinite(e) and e > 0 else 0.30


def g_pt(M, r, f=FENC):
    return f * H.G_KPC * M / r ** 2 * H.G2SI


for r_ in ROWS:
    s_ = r_["sid"]; r_["z"] = Z[s_]; r_["r"] = R_PRI[s_]; r_["rvar"] = R_VAR[s_]; r_["Mg"], r_["eMg"] = GAS_M[s_]; r_["sg"] = sig_dex(r_["Mg"], r_["eMg"]); r_["Ms"] = 10 ** r_["lms"]
    r_["gg0"] = g_pt(r_["Mg"], r_["r"]); r_["gs0"] = g_pt(r_["Ms"], r_["r"]); r_["gb0"] = r_["gg0"] + r_["gs0"]; r_["y0"] = r_["gb0"] / A0C
P("rows: " + "; ".join(f"{r_['label']}: r_ext {r_['r']:.3f} kpc, M_gas {r_['Mg']:.2e} (sigma {r_['sg']:.3f} dex), M* {r_['Ms']:.2e}" for r_ in ROWS))

# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (no velocity-bearing column is loaded; no g_obs, D, delta or s* is formed)")
    sed = ms[ms["limit_flag"] == "none"]
    found = [(r_["label"], bool(((sed["id"] == r_["sid"]) & (np.abs(sed["log_mstar_msun"] - r_["lms"]) < 1e-9) & (sed["source_arxiv"].astype(str).str.contains(r_["src"]))).any())) for r_ in ROWS]
    check("C1 CONTROL (loader): the five SED stellar masses (11.04 and 11.52, 11.39 and 11.27, 12.05) are found in the agent's table with limit_flag 'none' and the stated source; the three ids are in the sample, gas and kinematics tables; the sample's kpc/arcsec equals the programme's cosmology to 0.5 %; the gas masses are CFG277's (1.9e11 / 7.6e10 approx, 1.0e11)",
          f"found {found}; sed rows in the table {len(sed)}; ids {SIDS in [list(samp.index)] or all(s in samp.index and s in gas.index and s in kin.index for s in SIDS)}; kpc/arcsec deviation {max(abs(KPA[s] / H.kpc_per_arcsec(Z[s]) - 1) for s in SIDS):.1e}; gas {GAS_M}",
          all(f[1] for f in found) and all(s in samp.index and s in gas.index and s in kin.index for s in SIDS) and max(abs(KPA[s] / H.kpc_per_arcsec(Z[s]) - 1) for s in SIDS) < 5e-3 and abs(GAS_M["SGP38326-1"][0] - 1.9e11) < 1 and abs(GAS_M["SGP38326-2"][0] - 7.6e10) < 1 and abs(GAS_M["BRI1335-0417"][0] - 1.0e11) < 1)
    dr = max(max(abs(R_PRI[s] / c197[f"{s}|primary|fg0.5|canonical"]["r_ext_kpc"] - 1), abs(R_VAR[s] / c197[f"{s}|variant|fg0.5|canonical"]["r_ext_kpc"] - 1)) for s in SIDS)
    dg = max(abs(g_pt(GAS_M[s][0], R_PRI[s]) / A0C / c197[f"{s}|primary|fg0.5|canonical"]["g_gas_over_a0"] - 1) for s in SIDS)
    check("C2 CONTROL (reproduction of CFG197's committed gas-only numbers): r_ext (primary and variant) to 1e-3 and g_gas/a0 at f_enc = 0.5 (canonical) to 1e-4, relative, for the three discs", f"max relative difference in r_ext {dr:.1e}; in g_gas/a0 {dg:.1e}", dr < 1e-3 and dg < 1e-4)
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read(); seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}; exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr_ = np.random.default_rng(1234); same = True
    for _ in range(200):
        Dq = 10 ** rr_.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr_.uniform(-11, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = H.AI.implied(Dq, gq, NU, A0C); same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2)
    check("C3 CONTROL: the imported estimator equals CFG223's original bit for bit on 200 random sets", f"identical {same}", bool(same))
    d5 = 0.0
    for r_ in ROWS:
        for st in (0.5, 1.0, 2.5):
            ls, unb = H.s_star(NU(np.array([r_["gb0"] / (A0C * st)])), np.array([r_["gb0"]])); d5 = max(d5, abs(ls - math.log10(st)) if not unb else 9.0)
    check("C4 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on every row's baryon side", f"max |d log10 s| {d5:.1e}", d5 < 1e-6)
    P("\nA1 / A2  BARYON SIDE AND THE CFG240 READING (noiseless world; point mass, f_enc = 0.5; ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    for r_ in ROWS:
        lv, fl = H.lever1(NU(np.array([r_["y0"]])), np.array([r_["gb0"]])); r_["lever"], r_["ill"] = lv, bool(fl or abs(lv) >= 10)
        y_gas = r_["gg0"] / A0C
        P(f"    {r_['label']:28s} z {r_['z']:.3f} r_ext {r_['r']:.3f} kpc: y(gas only, CFG277) {y_gas:.2f} -> y(gas+M*) {r_['y0']:.2f} (M*/M_gas {r_['Ms'] / r_['Mg']:.2f}); lever {lv:+.2f}{' (not computable)' if fl else ''}  {'ILL-CONDITIONED' if r_['ill'] else 'conditioned'}")
    P("\nA3  KNOB EFFECTS ON g_bar (dex relative to the primary; f_enc, helium on the gas, radius, the other SED branch)")
    for r_ in ROWS:
        oth = [x for x in ROWS if x["sid"] == r_["sid"] and x is not r_]
        P(f"    {r_['label']:28s} f_enc 0.25 {np.log10(0.25 / FENC):+.3f}, f_enc 1.0 {np.log10(1.0 / FENC):+.3f}, helium x1.36 on the gas {np.log10((1.36 * r_['gg0'] + r_['gs0']) / r_['gb0']):+.3f}, radius variant {np.log10(g_pt(r_['Mg'] + r_['Ms'], r_['rvar']) / g_pt(r_['Mg'] + r_['Ms'], r_['r'])):+.3f}"
          + (f", the other SED branch {np.log10((r_['gg0'] + oth[0]['gs0']) / r_['gb0']):+.3f}" if oth else ""))
    P("\nA5  THE CFG277 REFERENCE (gas-only, committed): " + "; ".join(f"{k}: D {v['D']:.3f}, {v['status']}" + (f" s* <= {v['s']:.3g}" if v["status"] == "root" else "") for k, v in c277.items() if k in ("SGP38326-1 [gas]", "SGP38326-2 [gas]", "BRI1335-0417 [gas]")))
    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C4)")
    P("  PF-D2 ILL-CONDITIONED rows: " + (", ".join(r_["label"] for r_ in ROWS if r_["ill"]) or "none"))
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 8) scored (HE3-HE6 are scored at stage B):")
    yv = {r_["label"]: r_["y0"] for r_ in ROWS}
    he = {"HE1": bool(14 <= yv["SGP38326-1 [gas+M* T26]"] <= 22 and 25 <= yv["SGP38326-1 [gas+M* Ma19]"] <= 38 and 70 <= yv["SGP38326-2 [gas+M* T26]"] <= 110 and 60 <= yv["SGP38326-2 [gas+M* Ma19]"] <= 90 and 40 <= yv["BRI1335-0417 [gas+M* T26]"] <= 70), "HE2": bool(all(r_["ill"] for r_ in ROWS))}
    P(f"    HE1: y(gas+M*) {[round(v, 1) for v in yv.values()]} (needs 14-22, 25-38, 70-110, 60-90, 40-70): {'hit' if he['HE1'] else 'MISS (kept as it falls)'}")
    P(f"    HE2: all five rows ILL-CONDITIONED ({sum(r_['ill'] for r_ in ROWS)} of 5): {'hit' if he['HE2'] else 'MISS (kept as it falls)'}")
    NUM.update(inputs=dict(r_pri=R_PRI, r_var=R_VAR, z=Z, kpa=KPA, gas=GAS_M), rows={r_["label"]: dict(r=r_["r"], Mg=r_["Mg"], Ms=r_["Ms"], gb0=r_["gb0"], y0=r_["y0"], lever=r_["lever"], ill=r_["ill"]) for r_ in ROWS}, hand_estimates=he, pf=dict(PF_D1=bool(pfd1)))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V_ext and sigma_ext x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2820)
    KIN = {}
    for r_ in ROWS:
        s_ = r_["sid"]
        if SELFTEST:
            g_t = r_["gb0"] * float(NU(np.array([r_["gb0"] / (2.0 * A0C)]))[0]) * 10 ** rngS.normal(0, 0.15); Vf = math.sqrt(g_t * r_["r"] / H.G2SI)
            KIN[r_["label"]] = dict(V=Vf, eVhi=0.10 * Vf, eVlo=0.10 * Vf, S=0.0, eShi=0.0, eSlo=0.0)
        else:
            k_ = kin.loc[s_]; mult = 2.0 if MUTATE else 1.0
            KIN[r_["label"]] = dict(V=mult * float(k_["vrot_ext_kms"]), eVhi=mult * float(k_["vrot_ext_kms_errhi"]), eVlo=mult * float(k_["vrot_ext_kms_errlo"]), S=mult * float(k_["sigma_ext_kms"]), eShi=mult * float(k_["sigma_ext_kms_errhi"]), eSlo=mult * float(k_["sigma_ext_kms_errlo"]))

    def gobs_of(kk, rr, alpha=ALPHA, V=None, S=None):
        Vv = kk["V"] if V is None else V; Ss = kk["S"] if S is None else S
        return (Vv ** 2 + alpha * Ss ** 2) / rr * H.G2SI

    def gbar_of(r_, rr, f=FENC, he=1.0, Ms=None):
        Ms = r_["Ms"] if Ms is None else Ms
        return g_pt(he * r_["Mg"] + Ms, rr, f)

    def mc_row(r_, kk, B, rng):
        Vd = H.split_normal(rng, kk["V"], kk["eVhi"], kk["eVlo"], B); Sd = np.maximum(H.split_normal(rng, kk["S"], kk["eShi"], kk["eSlo"], B), 0.0)
        Mg_d = r_["Mg"] * 10 ** rng.normal(0, r_["sg"], B); Ms_d = r_["Ms"] * 10 ** rng.normal(0, SIGM, B)
        god = gobs_of(kk, r_["r"], V=Vd, S=Sd); gbd = g_pt(Mg_d + Ms_d, r_["r"]); Dd = god / gbd
        lsd, ud = H.AI.implied(Dd[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud); frc = float(np.mean(ud & (Dd > 1.0)))
        dFd = np.log10(god / (gbd * NU(gbd / A0C))); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        return q, frn, frc, dq

    KGR = {"pressure: alpha = 0": "pressure", "pressure: alpha = 1.68": "pressure", "radius: (N - 1.5) RADSEP": "radius", "geometry: f_enc = 0.25": "geometry", "geometry: f_enc = 1.0": "geometry", "helium x1.36 on the gas": "gas", "kernel P2": "kernel", "stellar mass: the other SED branch": "stars", "stellar mass: -0.30 dex": "stars", "stellar mass: +0.30 dex": "stars"}
    KN_LIST = list(KGR)
    RES = {}
    for r_ in ROWS:
        lab = r_["label"]; kk = KIN[lab]; oth = [x for x in ROWS if x["sid"] == r_["sid"] and x is not r_]
        GO = gobs_of(kk, r_["r"]); GO_ROT = gobs_of(kk, r_["r"], alpha=0.0); gb0 = r_["gb0"]; D0 = GO / gb0
        ls0, st0 = H.s_status(np.array([D0]), np.array([gb0]))
        rng = np.random.default_rng(zlib.crc32(("282|" + lab).encode()) % 100000)
        q, frn, frc, dq = mc_row(r_, kk, B_MC, rng)
        dF0 = float(np.log10(GO / (gb0 * float(NU(np.array([gb0 / A0C]))[0]))))

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
            if nm == "pressure: alpha = 0": return GO_ROT, gb0, NU
            if nm == "pressure: alpha = 1.68": return gobs_of(kk, r_["r"], alpha=1.68), gb0, NU
            if nm == "radius: (N - 1.5) RADSEP": return gobs_of(kk, r_["rvar"]), gbar_of(r_, r_["rvar"]), NU
            if nm == "geometry: f_enc = 0.25": return GO, gbar_of(r_, r_["r"], f=0.25), NU
            if nm == "geometry: f_enc = 1.0": return GO, gbar_of(r_, r_["r"], f=1.0), NU
            if nm == "helium x1.36 on the gas": return GO, gbar_of(r_, r_["r"], he=1.36), NU
            if nm == "kernel P2": return GO, gb0, NUP2
            if nm == "stellar mass: the other SED branch": return (GO, gbar_of(r_, r_["r"], Ms=oth[0]["Ms"]), NU) if oth else None
            if nm == "stellar mass: -0.30 dex": return GO, gbar_of(r_, r_["r"], Ms=r_["Ms"] * 10 ** -0.30), NU
            if nm == "stellar mass: +0.30 dex": return GO, gbar_of(r_, r_["r"], Ms=r_["Ms"] * 10 ** 0.30), NU
        for nm in KN_LIST:
            v = variant(nm)
            if v is None: continue
            go_, gb_, nu_ = v; lk, sk = H.s_status(np.array([go_ / gb_]), np.array([gb_]), nu_)
            kn[nm] = None if (st0 != "root" or sk != "root") else lk - ls0; kn[nm + "|status"] = sk
        grp = {}
        for nm in KN_LIST:
            if kn.get(nm) is not None: grp.setdefault(KGR[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        n_root = sum(1 for nm in KN_LIST if kn.get(nm + "|status") == "root")
        lv_nl, lf_nl = H.lever1(NU(np.array([gb0 / A0C])), np.array([gb0])); d1 = H.shift_to_s1(np.array([D0]), np.array([gb0]))
        RES[lab] = dict(label=lab, sid=r_["sid"], z=r_["z"], r_kpc=r_["r"], Mg=r_["Mg"], Ms=r_["Ms"], lms=r_["lms"], GO=GO, GO_rot=GO_ROT, GB=gb0, D=D0, y=r_["y0"], ls=ls0, status=st0, s=H.s_val_status(ls0, st0), q=q, frac_mc_noroot=frn, frac_mc_ceiling=frc,
                        delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1], band=band, allb=allb, knobs=kn, recipe_half=half, n_knobs_with_root=n_root, lever=lv_nl, ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=H.delta_floor(np.array([D0])),
                        delta_to_s1=d1, baryon_ratio_req=(10 ** d1 - 1 if np.isfinite(d1) else float("nan")), g_head_over_rot_dex=float(np.log10(GO / GO_ROT)))
        R_ = RES[lab]
        b0 = (f"s* <= {10 ** ls0:.3g}" if st0 == "root" else ("FLOOR (D <= 1)" if st0 == "floor" else "CEILING (s* > 1000)"))
        qs = f"68 % [{10 ** q[1]:.3g}, {10 ** q[3]:.3g}] 95 % [{10 ** q[0]:.3g}, {10 ** q[4]:.3g}]" if np.isfinite(q[0]) else "no draw interval (< 20 rooted draws)"
        P(f"  {lab:28s} r {r_['r']:.2f}: g_obs {GO:.3e}  g_bar {gb0:.3e}  D {D0:.3f}  dF {dF0:+.3f}  y {r_['y0']:.2f}  {b0}; MC {qs} (no root {frn:.2f}, ceiling {frc:.2f}); baryon ratio for s* = 1: {R_['baryon_ratio_req']:+.2f}; recipe half-width {half:.3f}; band inner [{band['inner']['lo']:.3g}, {band['inner']['hi']:.3g}] outer [{band['outer']['lo']:.3g}, {band['outer']['hi']:.3g}]{' ILL' if R_['ill'] else ''}")
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg282_stageB_results.json")))["numbers"]["rows"]

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
        check("M3 the five rows are present (two stellar-mass branches for each SGP38326 disc, one for BRI1335-0417)", f"{[RES[r_['label']]['lms'] for r_ in ROWS]}", [RES[r_["label"]]["lms"] for r_ in ROWS] == [11.04, 11.52, 11.39, 11.27, 12.05])
        if not SELFTEST:
            dm = 0.0
            for s_, lab_ in (("SGP38326-1", "SGP38326-1 [gas]"), ("SGP38326-2", "SGP38326-2 [gas]"), ("BRI1335-0417", "BRI1335-0417 [gas]")):
                k_ = KIN[[r_["label"] for r_ in ROWS if r_["sid"] == s_][0]]; go277 = c277[lab_]["GO"]
                rr_ = [r_ for r_ in ROWS if r_["sid"] == s_][0]; go_mine = gobs_of(k_, rr_["r"]); dm = max(dm, abs(go_mine / go277 - 1) if go277 else 9.0)
            check("M5 the g_obs of each disc equals CFG277's committed g_obs for the same disc (the same inputs and pressure term) to 1e-9, relative", f"max relative difference {dm:.1e}", dm < 1e-9)
        else:
            tested = [r_["label"] for r_ in ROWS if RES[r_["label"]]["status"] == "root" and not RES[r_["label"]]["ill"]]
            if tested:
                inside = [t for t in tested if np.isfinite(RES[t]["q"][0]) and RES[t]["q"][0] <= math.log10(2.0) <= RES[t]["q"][4]]
                check("SELFTEST: every row that is conditioned and has a root returns the fabricated truth (s = 2) inside its 95 % interval", f"{len(inside)} of {len(tested)}: {[(t, 'in' if t in inside else 'OUT') for t in tested]}", len(inside) == len(tested))
            else: P("  SELFTEST: no conditioned row with a root: truth recovery not applicable")
            P("  SELFTEST statuses: " + "; ".join(f"{r_['label']}: {RES[r_['label']]['status']}" + (f" s* {RES[r_['label']]['s']:.3g}" if RES[r_['label']]['status'] == 'root' else "") + (" ILL" if RES[r_["label"]]["ill"] else "") for r_ in ROWS))
            rep = {}
            for r_ in ROWS:
                inn = 0; nroot_w = 0; nfloor = 0
                for w in range(100):
                    rw = np.random.default_rng(100000 + 1000 * ROWS.index(r_) + w); g_t = r_["gb0"] * float(NU(np.array([r_["gb0"] / (2.0 * A0C)]))[0]) * 10 ** rw.normal(0, 0.15); Vf = math.sqrt(g_t * r_["r"] / H.G2SI)
                    kw = dict(V=Vf, eVhi=0.10 * Vf, eVlo=0.10 * Vf, S=0.0, eShi=0.0, eSlo=0.0); lsw, stw = H.s_status(np.array([g_t / r_["gb0"]]), np.array([r_["gb0"]])); nfloor += int(stw == "floor")
                    qw, _, _, _ = mc_row(r_, kw, 1000, rw)
                    if stw == "root" and np.isfinite(qw[0]): nroot_w += 1; inn += int(qw[0] <= math.log10(2.0) <= qw[4])
                rep[r_["label"]] = (inn, nroot_w, nfloor); P(f"  SELFTEST repeat (reported): {r_['label']}: the 95 % interval contains s = 2 in {inn} of {nroot_w} fabricated worlds with a root ({nfloor} of 100 worlds at the floor)")
            NUM["selftest_repeat"] = rep
    if not (MUTATE or SELFTEST):
        P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 8; HE1-HE2 were scored at stage A) scored:")
        Rr = RES; a, a2, b, b2, c = (Rr["SGP38326-1 [gas+M* T26]"], Rr["SGP38326-1 [gas+M* Ma19]"], Rr["SGP38326-2 [gas+M* T26]"], Rr["SGP38326-2 [gas+M* Ma19]"], Rr["BRI1335-0417 [gas+M* T26]"])
        m5 = [ok for n_, ok, lb in CHK if n_.startswith("M5")]
        he = {"HE3": bool(a["status"] == "root" and 1.3 <= a["D"] <= 2.1 and 8 <= a["s"] <= 60 and a["s"] < c277["SGP38326-1 [gas]"]["s"]), "HE4": bool(0.8 <= a2["D"] <= 1.2 and (a2["status"] == "floor" or (a2["status"] == "root" and a2["s"] > 100))),
              "HE5": bool(b["status"] == "floor" and b2["status"] == "floor" and 0.3 <= b["D"] <= 0.6 and 0.3 <= b2["D"] <= 0.6 and c["status"] == "floor" and 0.02 <= c["D"] <= 0.08), "HE6": bool(len(m5) == 1 and all(m5))}
        P(f"    HE3: SGP38326-1 [T26] {a['status']} D {a['D']:.3f} (1.3-2.1) s* {a['s']:.3g} (8-60, below CFG277's {c277['SGP38326-1 [gas]']['s']:.3g}): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}")
        P(f"    HE4: SGP38326-1 [Ma19] {a2['status']} D {a2['D']:.3f} (0.8-1.2; floor or a root with s* > 100): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5: SGP38326-2 [T26] {b['status']} D {b['D']:.3f}, [Ma19] {b2['status']} D {b2['D']:.3f} (floors, 0.3-0.6); BRI1335 {c['status']} D {c['D']:.3f} (floor, 0.02-0.08): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6: M5 holds (MUTATE=1's reactivity is scored in its own run): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        NUM["hand_estimates_B"] = he
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling",
                              "allb_in_lo", "allb_in_hi", "allb_out_lo", "allb_out_hi", "delta_floor", "delta_to_s1", "baryon_ratio_req", "status", "log_mstar", "stellar_source", "r_ext_kpc", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    LOW = {"SGP38326-1": 11.04, "SGP38326-2": 11.27, "BRI1335-0417": 12.05}
    for r_ in ROWS:
        R_ = RES[r_["label"]]; st = R_["status"]; q = R_["q"]; bi, bo = R_["band"]["inner"], R_["band"]["outer"]
        empty = 1000.0 if st == "ceiling" else FLOOR
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(R_["z"], lo95, hi95, (bi["lo"], bi["hi"]), (bo["lo"], bo["hi"]), st == "root"); half = R_["recipe_half"]
        extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], R_["allb"]["inner"]["lo"], R_["allb"]["inner"]["hi"], R_["allb"]["outer"]["lo"], R_["allb"]["outer"]["hi"],
                 R_["delta_floor"], R_["delta_to_s1"], R_["baryon_ratio_req"], st, R_["lms"], r_["src"], R_["r_kpc"]]
        q_ = "ILL-CONDITIONED (near-Newtonian); " + {"root": "has a root: an upper bound only if the gas mass and the SED stellar mass are right", "floor": "FLOOR: no root, D <= 1 (the baryons already exceed the dynamics)", "ceiling": f"CEILING: D = {R_['D']:.1f} > 1 but s* > 1000: vacuous"}[st] \
            + f"; stellar mass: {r_['srcnote']}" + ("; RECOMMENDED CHART ROW by the frozen rule (the lower-mass SED branch)" if r_["lms"] == LOW[r_["sid"]] else "")
        sstar = R_["s"]
        rows.append(["CFG282", r_["label"], f"S (CO gas, CFG277) + SED stars ({r_['src']})", f"{R_['z']:.4f}", f"{R_['z']:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{bi['lo']:.6g}", f"{bi['hi']:.6g}", bi["noroot"], f"{bo['lo']:.6g}", f"{bo['hi']:.6g}", bo["noroot"], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_["n_knobs_with_root"],
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], "class S gas and an SED stellar mass of limited reliability: not a limit unless both are right", fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg282_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg282_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg282{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg282{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
