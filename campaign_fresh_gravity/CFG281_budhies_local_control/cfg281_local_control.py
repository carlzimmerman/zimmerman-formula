#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG281 -- the BUDHIES width -> V -> baryon chain (CFG260) run on a same-pipeline LOCAL HI sample (ALFALFA widths + SDSS stellar masses), mass-matched to the BUDHIES primary set PC.
A calibration of the chain, not a gravity test.  kappa = 1/2 is FITTED.  No verdict words.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG281_budhies_local_control/FROZEN_CRITERIA.md (b766cf43e).
  local set L   code 1, M_HI >= 3e9, 20-85 Mpc, complete photometry; matched set LC = 4,000 stratified resamples of 100 galaxies in each of the four equal-count bins of the PC's log M_HI quartiles
  chain         W_c = (W50 - 9) / (1+z); V = W_c / (2 sin 60 deg); M_gas = 1.33 M_HI; M* = the catalogue's Taylor+11 colour mass; R = D_HI/2 (D_HI-M_HI relation); g_bar = G M_b / R^2; g_obs = V^2 / R; CFG223's s*
  STAGE=A  blind: no width column is loaded.   STAGE=B  the measurement (once, after stage A, the SELFTEST and this script are committed); STAGE=B SELFTEST=1; STAGE=B MUTATE=1 (widths x 1.1892); STAGE=B MUTATE=2 (sin i_eff 0.70).
Variants and knobs use the first 1,000 of the same resamples (common random numbers); the primary estimate and its interval use all 4,000.
Run: STAGE=A python3 .../cfg281_local_control.py ; STAGE=B SELFTEST=1 python3 ... ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ... ; STAGE=B MUTATE=2 python3 ...
"""
import os, sys, json, math, time, re, csv
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

TSTART = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common")); sys.path.insert(0, os.path.join(CFG, "CFG260_budhies_a0_z02"))
import hzq_core as H
import cfg260_core as C

STAGE = os.environ.get("STAGE", "").strip().upper()
MUT = int(os.environ.get("MUTATE", "0") or 0)
SELFTEST = os.environ.get("SELFTEST", "0") == "1"
assert STAGE in ("A", "B"), "set STAGE=A or STAGE=B"
assert not ((MUT or SELFTEST) and STAGE == "A") and not (MUT and SELFTEST) and MUT in (0, 1, 2), "MUTATE / SELFTEST apply to stage B, one at a time"
SFX = f"_stage{STAGE}" + (f"_MUTATE{MUT}" if MUT else "") + ("_SELFTEST" if SELFTEST else "")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}{'' if load_bearing else ' (not load-bearing)'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
P(f"\nSTAGE {STAGE}" + (f"  *** MUTATE={MUT}: " + ("widths x 1.1892 ***" if MUT == 1 else "sin i_eff 0.70 ***") if MUT else "") + ("  *** SELFTEST: FABRICATED widths on the law at s_true = 2 (isotropic inclinations, 0.03 dex scatter in V); debugging only ***" if SELFTEST else ""))

G, MSUN, KPC, CKMS = C.G, C.MSUN, C.KPC, C.CKMS
NU, NUP2, A0 = C.NU, C.NU_P2, C.A0
A0C, A0A = A0["canonical"], A0["alt"]
LOADW = (STAGE == "B") and not SELFTEST                                      # the SELFTEST never loads the real widths
CSVP = os.path.join(REPO, "data_assembly", "alfalfa_sdss_local_control", "alfalfa_sdss.csv")
RES260 = json.load(open(os.path.join(CFG, "CFG260_budhies_a0_z02", "cfg260_results.json")))["results"]
SREF = 1.20 / 0.93603                                                        # SPARC-empirical scale on the canonical footing (1.282)
SIN60 = math.sin(math.radians(60.0))
B_FULL, B_VAR, B_UNM, PER_BIN = 4000, 1000, 2000, 100
BASE = ["agc", "in_durbala2020", "in_a100_table2", "vhel_kms", "dist_mpc", "e_dist_mpc", "s21_jykms", "snr", "hi_code", "logmhi", "e_logmhi", "ba_r", "imag_abs_corr", "gi_corr", "logms_taylor", "logms_mcgaugh", "logms_gswlc"]
WIDTHS = ("w50_kms", "e_w50_kms")                                            # the forbidden-until-stage-B columns
d = pd.read_csv(CSVP, usecols=BASE + (list(WIDTHS) if LOADW else []))
P(f"local table {os.path.basename(CSVP)} sha256 {H.sha(CSVP)}; {len(d)} rows; width columns loaded: {LOADW}")

# ---------------------------------------------------------------- the local set L (frozen, section 2)
steps = []
m = d.in_durbala2020.eq(1) & d.in_a100_table2.eq(1); steps.append(("in both catalogues", int(m.sum())))
m &= d.hi_code.eq(1); steps.append(("HI code 1", int(m.sum())))
m &= (d.logmhi >= math.log10(3e9)); steps.append(("M_HI >= 3e9", int(m.sum())))
m &= d.dist_mpc.between(20.0, 85.0); steps.append(("20 <= D <= 85 Mpc", int(m.sum())))
m &= d[["gi_corr", "logms_taylor", "imag_abs_corr", "ba_r"]].notna().all(axis=1) & (d.s21_jykms > 0) & (d.s21_jykms < 900); steps.append(("complete photometry and a valid flux", int(m.sum())))
L = d[m].reset_index(drop=True)
nL = len(L)
P("selection: " + " -> ".join(f"{k} {v}" for k, v in steps))
Lz = (L.vhel_kms.values / CKMS).astype(float)
AR = dict(mhi=10 ** L.logmhi.values.astype(float), ms=10 ** L.logms_taylor.values.astype(float), z=Lz)
LMHI = L.logmhi.values.astype(float)

# ---------------------------------------------------------------- the PC (BUDHIES) side: non-width inputs only at stage A
gals0 = C.load_galaxies(widths=False); pc0 = C.select(gals0, "PC")
pc_m = np.log10([g["mhi"] for g in pc0]); PCQ = np.percentile(pc_m, [0, 25, 50, 75, 100])
BINS = [np.where((LMHI >= PCQ[i]) & ((LMHI < PCQ[i + 1]) if i < 3 else (LMHI <= PCQ[i + 1])))[0] for i in range(4)]
P(f"PC (BUDHIES primary set): N {len(pc0)}, log M_HI quartiles {np.array2string(PCQ, precision=3)}, z_bar {np.mean([g['z'] for g in pc0]):.4f}; local galaxies per PC-quartile bin {[len(b) for b in BINS]}; below the PC minimum {int((LMHI < PCQ[0]).sum())}, above the maximum {int((LMHI > PCQ[4]).sum())}")
rngI = np.random.default_rng(np.random.SeedSequence([281, 1]))
IDX = np.concatenate([BINS[i][rngI.integers(0, len(BINS[i]), size=(B_FULL, PER_BIN))] for i in range(4)], axis=1)       # (B_FULL, 400) indices into L, equal weight per bin
REC0 = dict(delta=9.0, k=1, sini=SIN60, tau_ms=0.0, tau_b=0.0, rdex=0.0, hubble=70.0, h2=0.0, kernel="nu_mono")


# ---------------------------------------------------------------- the chain (CFG260 section 3 with the local inputs)
def baryons_local(a, rec):
    ds = 70.0 / rec["hubble"]
    Mhi = a["mhi"] * ds ** 2
    Ms = a["ms"] * ds ** 2 * 10 ** rec["tau_ms"]
    Mg = (1.33 + rec["h2"]) * Mhi
    R = 0.5 * 10 ** (0.506 * np.log10(Mhi) - 3.293 + rec["rdex"]) * KPC
    tb = 10 ** rec["tau_b"]
    return Mg * tb, Ms * tb, (Mg + Ms) * tb, R


def chain_core(W, z, Mb, R, delta, k, sini):
    """the width -> V -> acceleration step (the same formulae as cfg260_core.derive); returns (D, g_bar, V, ok)"""
    Wc = (np.asarray(W, float) - delta) / (1 + z) ** k
    ok = Wc > 0
    V = np.where(ok, Wc, np.nan) / (2 * sini) * 1e3
    gb = G * Mb * MSUN / R ** 2
    return (V ** 2 / R) / gb, gb, V, ok


def derive_local(a, W, rec, sini=None):
    Mg, Ms, Mb, R = baryons_local(a, rec)
    D, gb, V, ok = chain_core(W, a["z"], Mb, R, rec["delta"], rec["k"], rec["sini"] if sini is None else sini)
    return dict(D=D, gb=gb, V=V, ok=ok, Mb=Mb, Mg=Mg, Ms=Ms, R=R, y=gb / A0C)


def matched(D, gb, nu, a0, Bn):
    ls, unb = C.implied(D[IDX[:Bn]], gb[IDX[:Bn]], nu, a0)
    return ls, unb


def mstat(ls, unb):
    return dict(med=float(np.median(ls)), s=10 ** float(np.median(ls)), sd=float(np.std(ls)), q=[float(v) for v in np.percentile(ls, [2.5, 16, 84, 97.5])], noroot=float(np.mean(unb)))


def unmatched(D, gb, nu, a0, B=B_UNM, seed=2):
    ok = np.isfinite(D); Dk, gk = D[ok], gb[ok]; n = len(Dk)
    l0, u0 = C.implied(Dk, gk, nu, a0)
    I = np.random.default_rng(np.random.SeedSequence([281, seed, n])).integers(0, n, size=(B, n))
    lb, ub = C.implied(Dk[I], gk[I], nu, a0)
    return dict(n=int(n), log_s=float(l0[0]), s=10 ** float(l0[0]), unb=bool(u0[0]), sd=float(np.std(lb)), q=[float(v) for v in np.percentile(lb, [2.5, 16, 84, 97.5])])


def kernel(rec):
    return NUP2 if rec.get("kernel", "nu_mono") == "P2" else NU


# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (no width column is loaded)")
    check("C1 CONTROL (loader): the table has 31,503 rows with both source flags; the stage-A loader reads no width column (the loaded frame contains none); the PC log M_HI quartiles equal CFG260's 9.588 / 9.849 / 9.936 / 10.124 / 10.525 and N = 32",
          f"rows {len(d)}; in both {int((d.in_durbala2020.eq(1) & d.in_a100_table2.eq(1)).sum())}; width columns in the loaded frame {[c for c in d.columns if c in WIDTHS or c == 'w20_kms']}; PC quartiles {np.array2string(PCQ, precision=3)}; N {len(pc0)}",
          len(d) == 31503 and not any(c in d.columns for c in WIDTHS + ("w20_kms",)) and len(pc0) == 32 and np.allclose(PCQ, [9.588, 9.849, 9.936, 10.124, 10.525], atol=6e-4))
    dev = np.abs(L.logmhi.values - np.log10(2.356e5 * L.dist_mpc.values ** 2 * L.s21_jykms.values)); imax = int(np.argmax(dev))
    check("C2 CONTROL: log M_HI = log10(2.356e5 D^2 S21) to 0.01 dex for every selected row (the catalogue's own identity)", f"max deviation {float(dev.max()):.4f} dex (AGC {int(L.agc.iloc[imax])}, D = {float(L.dist_mpc.iloc[imax]):.1f} Mpc); median {float(np.median(dev)):.4f}", float(dev.max()) <= 0.01)
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read(); seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}; exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr_ = np.random.default_rng(1234); same = True; same60 = True
    for _ in range(200):
        Dq = 10 ** rr_.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr_.uniform(-12, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = H.AI.implied(Dq, gq, NU, A0C); a3, u3 = C.implied(Dq, gq, NU, A0C)
        same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2); same60 = same60 and float(np.max(np.abs(a1 - a3))) < 1e-12 and np.array_equal(u1, u3)
    check("C3 CONTROL: the imported estimators equal CFG223's original (bit for bit, hzq_core) and CFG260's `implied` (1e-12) on 200 random sets", f"hzq_core identical {same}; cfg260_core within 1e-12 {same60}", bool(same and same60))
    Mg, Ms, Mb, R = baryons_local(AR, REC0); gbL = G * Mb * MSUN / R ** 2; dn = 0.0
    for st_ in (0.5, 1.0, 2.5):
        gobs = gbL * C.nuv(NU, gbL / (A0C * st_)); Wf = 2 * np.sqrt(gobs * R) / 1e3 * SIN60 * (1 + Lz) ** REC0["k"] + REC0["delta"]
        D_, gb_, V_, ok_ = chain_core(Wf, Lz, Mb, R, REC0["delta"], REC0["k"], REC0["sini"]); l1, u1 = C.implied(D_[ok_], gb_[ok_], NU, A0C); ls_m, un_m = matched(D_, gb_, NU, A0C, 200)
        dn = max(dn, abs(float(l1[0]) - math.log10(st_)), float(np.max(np.abs(ls_m - math.log10(st_)))) if not un_m.any() else 9.0)
    check("C4 CONTROL: the noiseless world (widths from the inverse chain on the law at s_true = 0.5, 1, 2.5, sin i_eff = sin 60 for every galaxy) returns s_true to 1e-6 dex on L and on every one of 200 matched resamples", f"max |d log10 s| {dn:.1e}", dn < 1e-6)
    ms_draw = LMHI[IDX[:1000].ravel()]; qd = np.percentile(ms_draw, [25, 50, 75])
    check("C5 CONTROL: the matched resamples carry equal weight per PC-quartile bin (exactly 100 draws each) and their log M_HI quartiles lie within 0.05 dex of the PC's", f"draws per bin {[int(((LMHI[IDX[0]] >= PCQ[i]) & (LMHI[IDX[0]] <= PCQ[i + 1])).sum()) for i in range(4)]}; matched quartiles {np.array2string(qd, precision=3)} against PC {np.array2string(PCQ[1:4], precision=3)}",
          bool(np.all(np.abs(qd - PCQ[1:4]) <= 0.05)))
    P("\nA1  THE BARYON SIDE (no width: y, gas fraction and radii of the set and of the matched resamples)")
    yy = Mb * G * MSUN / R ** 2 / A0C; gf = Mg / Mb
    yd = yy[IDX[:1000].ravel()]; gd = gf[IDX[:1000].ravel()]
    P(f"    L (N = {nL}): y quartiles {np.array2string(np.percentile(yy, [5, 25, 50, 75, 95]), precision=4)} (5/25/50/75/95 %); fraction y < 0.3 {float(np.mean(yy < 0.3)):.3f}; gas fraction median {float(np.median(gf)):.3f}; R median {float(np.median(R) / KPC):.1f} kpc; log M_HI median {float(np.median(LMHI)):.3f}; z median {float(np.median(Lz)):.4f}")
    P(f"    matched: y quartiles {np.array2string(np.percentile(yd, [5, 25, 50, 75, 95]), precision=4)}; fraction y < 0.3 {float(np.mean(yd < 0.3)):.3f}; gas fraction median {float(np.median(gd)):.3f}; PC y (CFG260): median 0.068, Q1 0.042, Q3 0.114, max 0.207, all below 0.3")
    P(f"    stellar mass methods (log M*, median over L): Taylor {float(np.median(L.logms_taylor)):.3f}, McGaugh {float(np.nanmedian(L.logms_mcgaugh)):.3f} ({int(L.logms_mcgaugh.isna().sum())} missing), GSWLC {float(np.nanmedian(L.logms_gswlc)):.3f} ({int(L.logms_gswlc.isna().sum())} missing); stars/gas mass ratio median {float(np.median(Ms / Mg)):.2f}")
    P(f"    variant sets: 20-50 Mpc {int((L.dist_mpc <= 50).sum())}, 50-85 Mpc {int((L.dist_mpc > 50).sum())}, M_HI >= 5e9 {int((LMHI >= math.log10(5e9)).sum())}; axis-ratio quartiles {np.array2string(np.percentile(L.ba_r, [5, 25, 50, 75, 95]), precision=2)}")
    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P(f"\nDECISION  PF-D1 ESTIMATOR AND LOADER VALIDATED: {pfd1} (controls C1-C5)")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 8) scored (HE3-HE9 are scored at stage B):")
    he = {"HE1": bool(0.03 <= float(np.median(yd)) <= 0.12 and float(np.mean(yd < 0.3)) >= 0.90 and 0.45 <= float(np.median(gd)) <= 0.80), "HE2": bool(float(dev.max()) <= 0.01)}
    P(f"    HE1: matched median y {float(np.median(yd)):.4f} (0.03-0.12), fraction y < 0.3 {float(np.mean(yd < 0.3)):.3f} (>= 0.90), gas fraction median {float(np.median(gd)):.3f} (0.45-0.80): {'hit' if he['HE1'] else 'MISS (kept as it falls)'}")
    P(f"    HE2: M_HI identity max deviation {float(dev.max()):.4f} dex (<= 0.01): {'hit' if he['HE2'] else 'MISS (kept as it falls)'}")
    NUM.update(selection=steps, pc=dict(n=len(pc0), quartiles=PCQ.tolist()), bins=[len(b) for b in BINS], y=dict(L=np.percentile(yy, [5, 25, 50, 75, 95]).tolist(), matched=np.percentile(yd, [5, 25, 50, 75, 95]).tolist()), gas_fraction=dict(L=float(np.median(gf)), matched=float(np.median(gd))), hand_estimates=he, pf=dict(PF_D1=bool(pfd1)),
               controls_numbers=dict(mhi_identity_max=float(dev.max()), noiseless_max=dn))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (f" (MUTATE={MUT})" if MUT else ""))
    rec = dict(REC0)
    if MUT == 2: rec["sini"] = 0.70
    # widths
    if SELFTEST:
        W = None
    else:
        W = L.w50_kms.values.astype(float)
        if MUT == 1: W = (W - rec["delta"]) * 1.1892 + rec["delta"]
    sz_med = float(np.median(Lz[IDX[:1000].ravel()]))

    def run_all(W_, rec_, sini=None, nu=NU, a0=A0C, a=AR, Bn=B_VAR):
        dd = derive_local(a, W_, rec_, sini); return dd, matched(dd["D"], dd["gb"], nu, a0, Bn)

    if SELFTEST:
        worlds = []
        Mg, Ms, Mb, R = baryons_local(AR, rec); gbL = G * Mb * MSUN / R ** 2; gobs = gbL * C.nuv(NU, gbL / (A0C * 2.0))
        for w in range(100):
            rw = np.random.default_rng(100000 + w); V = np.sqrt(gobs * R) * 10 ** rw.normal(0, 0.03, nL); sini = np.sqrt(1 - rw.uniform(0, 1, nL) ** 2)
            Wf = 2 * V / 1e3 * sini * (1 + Lz) ** rec["k"] + rec["delta"]; dd = derive_local(AR, Wf, rec); ls, unb = matched(dd["D"], dd["gb"], NU, A0C, 200)
            q = np.percentile(ls, [2.5, 97.5]); worlds.append((float(np.median(ls)), bool(q[0] <= math.log10(2.0) <= q[1]), float(np.mean(unb))))
        med_w = float(np.median([w[0] for w in worlds])); cov = float(np.mean([w[1] for w in worlds]))
        P(f"  SELFTEST over 100 fabricated worlds (200 matched resamples each): median log10 s* = {med_w:+.4f} (truth {math.log10(2.0):+.4f}); SD over worlds {float(np.std([w[0] for w in worlds])):.4f}; the resample 95 % interval contains the truth in {cov:.2f} of the worlds; mean unbounded fraction {float(np.mean([w[2] for w in worlds])):.3f}")
        check("SELFTEST: the median over 100 worlds of the matched estimate lies within 0.05 dex of log10 2 (the isotropic-inclination and median argument)", f"median {med_w:+.4f} against {math.log10(2.0):+.4f}", abs(med_w - math.log10(2.0)) <= 0.05)
        NUM["selftest"] = dict(median=med_w, coverage=cov, sd=float(np.std([w[0] for w in worlds])))
    else:
        out = {}
        dd, (ls4, un4) = run_all(W, rec, Bn=B_FULL)
        prim = mstat(ls4, un4); n_ok = int(dd["ok"].sum()); n_drop = nL - n_ok
        Dm = dd["D"]; gbm = dd["gb"]
        P(f"  PRIMARY matched set LC: N(L) {nL}, dropped (W - delta <= 0) {n_drop}; s* = {prim['s']:.4f} (log10 {prim['med']:+.4f}); resample SD {prim['sd']:.4f} dex; 68 % [{10 ** prim['q'][1]:.4f}, {10 ** prim['q'][2]:.4f}], 95 % [{10 ** prim['q'][0]:.4f}, {10 ** prim['q'][3]:.4f}]; no-root fraction {prim['noroot']:.4f}; the SPARC-empirical scale is {SREF:.3f}")
        out["LC"] = dict(prim, n=nL, dropped=n_drop)
        unm = unmatched(Dm, gbm, NU, A0C); out["LU"] = unm
        P(f"  UNMATCHED set LU: N {unm['n']}; s* = {unm['s']:.4f}; bootstrap SD {unm['sd']:.4f} dex; 95 % [{10 ** unm['q'][0]:.4f}, {10 ** unm['q'][3]:.4f}]")
        yv = dd["y"][np.isfinite(Dm)]; P(f"  regime (L): y quartiles {np.array2string(np.percentile(yv, [25, 50, 75]), precision=4)}; fraction y < 0.3 {float(np.mean(yv < 0.3)):.3f}")
        if not MUT:
            # baryon bands
            bands = {}
            for t in (-0.30, -0.15, 0.15, 0.30):
                dt, (lt, ut) = run_all(W, dict(rec, tau_b=t)); bands[f"{t:+.2f}"] = dict(s=10 ** float(np.median(lt)), noroot=float(np.mean(ut)))
            out["bands"] = bands; P("  baryon bands (all baryons x 10^t): " + ", ".join(f"{k}: s* {v['s']:.4f}" + (f" (no-root {v['noroot']:.2f})" if v["noroot"] > 0.01 else "") for k, v in bands.items()))
            # recipe knobs
            KN = (("delta", (0.0, 18.0), "width correction (km/s)"), ("sini", (0.80, 0.92), "sin i_eff"), ("tau_ms", (-0.25, 0.25), "M* zero point (dex)"), ("rdex", (-0.15, 0.15), "R scale (dex)"), ("hubble", (67.4, 73.0), "H0 (distance scale)"))
            ref_v = float(np.median(matched(derive_local(AR, W, rec)["D"], derive_local(AR, W, rec)["gb"], NU, A0C, B_VAR)[0])); rows = {}
            for key, br, label in KN:
                lss = []
                for v in br:
                    dk, (lk, uk) = run_all(W, dict(rec, **{key: v})); lss.append(float(np.median(lk)))
                rows[key] = dict(label=label, brackets=list(br), log_s=lss, half=0.5 * abs(lss[1] - lss[0]))
            half = math.sqrt(sum(v["half"] ** 2 for v in rows.values())); out["recipe"] = dict(rows=rows, half=half, ref_log_s=ref_v)
            P("  recipe knobs (half-width of each, dex): " + "; ".join(f"{k}: {v['half']:.3f}" for k, v in rows.items()) + f"; quadrature half-width {half:.3f} dex")
            # variants
            VAR = {}
            for nm, lo, hi in (("V1 20-50 Mpc", 20, 50), ("V1 50-85 Mpc", 50, 85)):
                msk = ((L.dist_mpc.values >= lo) & (L.dist_mpc.values <= hi)); u_ = unmatched(np.where(msk, Dm, np.nan), gbm, NU, A0C, B=500, seed=3); VAR[nm] = u_
            msk5 = LMHI >= math.log10(5e9); VAR["V2 M_HI >= 5e9"] = unmatched(np.where(msk5, Dm, np.nan), gbm, NU, A0C, B=500, seed=4)
            for nm, col in (("V4 stellar mass: McGaugh", "logms_mcgaugh"), ("V4 stellar mass: GSWLC", "logms_gswlc")):
                a_ = dict(AR, ms=10 ** L[col].values.astype(float)); dv, (lv, uv) = run_all(W, rec, a=a_); VAR[nm] = dict(s=10 ** float(np.median(lv)), n=int(np.isfinite(dv["D"][IDX[0]]).sum()))
            q_ = np.clip(L.ba_r.values.astype(float), 0.2, 1.0); cos2 = (q_ ** 2 - 0.04) / 0.96; sin_i = np.maximum(np.sqrt(np.clip(1 - cos2, 0, 1)), math.sin(math.radians(20.0)))
            dv, (lv, uv) = run_all(W, rec, sini=sin_i); VAR["V5 inclination from b/a"] = dict(s=10 ** float(np.median(lv)), sini_median=float(np.median(sin_i)))
            for nm, upd in (("V6 other frame (k = 0)", dict(k=0)), ("V7 H2 added (0.3 M_HI)", dict(h2=0.3))):
                dv, (lv, uv) = run_all(W, dict(rec, **upd)); VAR[nm] = dict(s=10 ** float(np.median(lv)))
            dv, (lv, uv) = run_all(W, rec, nu=NUP2); VAR["V8 P2 kernel"] = dict(s=10 ** float(np.median(lv)))
            a0i = (dd["V"] ** 4 / (G * dd["Mb"] * MSUN)); VAR["V9 BTFR route"] = dict(s=float(10 ** np.median(np.log10(np.nanmedian(a0i[IDX[:B_VAR]], axis=1) / A0C))))
            dv, (lv, uv) = run_all(W, rec, a0=A0A); VAR["V10 alt footing"] = dict(s=10 ** float(np.median(lv)), check=abs(float(np.median(lv)) + math.log10(A0A / A0C) - float(np.median(run_all(W, rec)[1][0]))))
            out["variants"] = VAR
            P("  variants: " + "; ".join(f"{k}: s* {v['s']:.4f}" + (f" (N {v['n']})" if 'n' in v else "") for k, v in VAR.items()))
            drift = abs(math.log10(VAR["V1 20-50 Mpc"]["s"]) - math.log10(VAR["V1 50-85 Mpc"]["s"]))
            offset = math.log10(prim["s"] / SREF); cal_i = abs(offset) <= 0.15; cal_ii = half <= 0.20; cal_iii = drift <= 0.10; calibrated = bool(cal_i and cal_ii and cal_iii)
            P(f"\n  CALIBRATION (frozen rule): (i) |log10(s*_LC / {SREF:.3f})| = {abs(offset):.3f} (<= 0.15): {cal_i}; (ii) recipe half-width {half:.3f} (<= 0.20): {cal_ii}; (iii) distance-window drift {drift:.3f} (<= 0.10): {cal_iii}  ->  " + ("CALIBRATED" if calibrated else "NOT CALIBRATED") + f"; local chain offset b_L = {offset:+.3f} dex")
            out["calibration"] = dict(offset_dex=offset, i=cal_i, ii=cal_ii, iii=cal_iii, drift=drift, calibrated=calibrated)
            # BUDHIES / local ratio
            rb = RES260["PC|rest"]; sB, sdB, halfB = rb["s"], rb["sd_log"], RES260["PC|rest"]["recipe_half"]; logrho = math.log10(sB) - prim["med"]
            sig_stat = math.hypot(sdB, prim["sd"]); sig_tot = math.sqrt(sig_stat ** 2 + halfB ** 2 + half ** 2)
            zB = float(np.mean([g["z"] for g in pc0])); FH = H.LAWS["H(z)"](zB) / H.LAWS["H(z)"](sz_med)
            rho = dict(rho=10 ** logrho, log10_rho=logrho, sig_stat=sig_stat, sig_tot=sig_tot, pull_FLAT_stat=logrho / sig_stat, pull_FLAT_tot=logrho / sig_tot, pull_Hz_stat=(logrho - math.log10(FH)) / sig_stat, pull_Hz_tot=(logrho - math.log10(FH)) / sig_tot, F_Hz=FH, sB=sB, sdB=sdB, halfB=halfB, zB=zB, zL=sz_med)
            out["rho"] = rho
            P(f"  BUDHIES / local: rho = s*_B(PC, rest) {sB:.4f} / s*_LC {prim['s']:.4f} = {rho['rho']:.4f} (log10 {logrho:+.4f} +- {sig_stat:.3f} statistics, +- {sig_tot:.3f} with both recipe widths {halfB:.3f} and {half:.3f}); statistics-only pulls: FLAT (F = 1) {rho['pull_FLAT_stat']:+.2f}, H(z) (F = {FH:.3f}) {rho['pull_Hz_stat']:+.2f}; with the recipe widths {rho['pull_FLAT_tot']:+.2f} / {rho['pull_Hz_tot']:+.2f}  [valid only under the same-pipeline assumption]")
        NUM["out"] = out
        # ---------------------------------------------------------------- controls
        P("\nCONTROLS (stage B)")
        if MUT:
            main = json.load(open(os.path.join(HERE, "cfg281_stageB_results.json")))["numbers"]["out"]["LC"]["med"]; resp = prim["med"] - main
            lo_, hi_ = (0.25, 0.35) if MUT == 1 else (0.31, 0.43)
            check(f"M2 MUTATE={MUT} (reactivity): " + ("the widths x 1.1892 (V x 1.1892) raise s* by 0.30 +- 0.05 dex" if MUT == 1 else "sin i_eff 0.70 instead of 0.866 raises s* by 0.37 +- 0.06 dex"), f"main {main:+.4f}, mutated {prim['med']:+.4f}: response {resp:+.4f} dex (window {lo_}-{hi_})", lo_ <= resp <= hi_)
        else:
            check("M1 CONTROL: the alt footing implies the same absolute a0 (matched primary)", f"max |d log10| = {out['variants']['V10 alt footing']['check']:.1e}", out["variants"]["V10 alt footing"]["check"] < 1e-9)
            gw = C.load_galaxies(widths=True); pcw = C.select(gw, "PC"); aa = C.Arr(pcw); Wb = np.array([g["w50"] for g in pcw]); recb = dict(C.REC0, k=0)
            l_ref = float(C.s_star(aa, Wb, recb)[0]); Mg_, Ms_, Mb_, R_ = C.baryons(aa, recb); D_, gb_, V_, ok_ = chain_core(Wb, aa.z, Mb_, R_, recb["delta"], recb["k"], recb["sini"]); l_mine = float(C.implied(D_[ok_], gb_[ok_], NU, A0C)[0][0])
            check("M5 the same-chain control: this script's chain core, fed the BUDHIES PC arrays with CFG260's recipe (delta 28, k = 0, the B - R colour step through cfg260_core.baryons), reproduces CFG260's s* (PC, rest-frame) to 1e-6", f"mine {10 ** l_mine:.6f}, cfg260_core {10 ** l_ref:.6f}, CFG260's committed result {RES260['PC|rest']['s']:.6f}", abs(l_mine - l_ref) < 1e-6 and abs(10 ** l_ref - RES260["PC|rest"]["s"]) < 1e-5)
            check("M3 (reported) the unmatched set's s* and the matched set's agree within the recipe band", f"matched {prim['s']:.4f}, unmatched {unm['s']:.4f}: difference {abs(math.log10(prim['s']) - math.log10(unm['s'])):.3f} dex against the half-width {out['recipe']['half']:.3f}", abs(math.log10(prim["s"]) - math.log10(unm["s"])) <= out["recipe"]["half"], load_bearing=False)
            P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 8; HE1-HE2 were scored at stage A) scored:")
            v_ = out["variants"]; ct = out["calibration"]; base_l = out["recipe"]["ref_log_s"]; mcm = [abs(math.log10(v_[k]["s"]) - base_l) for k in ("V4 stellar mass: McGaugh", "V4 stellar mass: GSWLC")]
            he = {"HE3": bool(0.6 <= prim["s"] <= 2.0), "HE4": bool(ct["calibrated"]), "HE5": bool(abs(math.log10(v_["V5 inclination from b/a"]["s"]) - base_l) <= 0.10), "HE6": bool(max(mcm) <= 0.08), "HE7": bool(0.10 <= out["rho"]["rho"] <= 0.40), "HE8": bool(ct["drift"] <= 0.10)}
            P(f"    HE3: s*_LC {prim['s']:.4f} (needs 0.6-2.0): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}")
            P(f"    HE4: CALIBRATED {ct['calibrated']} (needs True): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
            P(f"    HE5: the b/a inclination variant moves s* by {abs(math.log10(v_['V5 inclination from b/a']['s']) - base_l):.3f} dex (against the same 1,000 resamples) (needs <= 0.10): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
            P(f"    HE6: the stellar-mass methods move s* by {[round(x, 3) for x in mcm]} dex (needs <= 0.08): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
            P(f"    HE7: rho {out['rho']['rho']:.4f} (needs 0.10-0.40): {'hit' if he['HE7'] else 'MISS (kept as it falls)'}")
            P(f"    HE8: the distance-window drift {ct['drift']:.3f} dex (needs <= 0.10): {'hit' if he['HE8'] else 'MISS (kept as it falls)'}")
            NUM["hand_estimates_B"] = he
        # ---------------------------------------------------------------- the points file
        pcols = H.CHART_HEADER + ["recipe_half_dex", "y_median", "n", "n_dropped", "set", "calibration", "log10_rho", "limit", "quality"]
        check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
        rows = []
        bd = out.get("bands", {})
        for nm, st_, lab in (("ALFALFA-SDSS local control, matched to the BUDHIES primary set (log M_HI quartiles)", prim, "LC"), ("ALFALFA-SDSS local control, unmatched", None, "LU")):
            if lab == "LC":
                s_, q_ = prim["s"], prim["q"]; lo68, hi68, lo95, hi95 = 10 ** q_[1], 10 ** q_[2], 10 ** q_[0], 10 ** q_[3]; nn = nL; nd = n_drop
            else:
                s_ = unm["s"]; q_ = unm["q"]; lo68, hi68, lo95, hi95 = 10 ** q_[1], 10 ** q_[2], 10 ** q_[0], 10 ** q_[3]; nn = unm["n"]; nd = nL - unm["n"]
            b15 = (bd["-0.15"]["s"], bd["+0.15"]["s"]) if bd else ("", ""); b30 = (bd["-0.30"]["s"], bd["+0.30"]["s"]) if bd else ("", "")
            hf = out["recipe"]["half"] if "recipe" in out else float("nan")
            rows.append(["CFG281", nm, "HI (HI measured; H2 neglected; stars from the catalogue's colour mass)", f"{sz_med:.4f}", f"{sz_med:.4f}", 0, f"{s_:.6g}", f"{s_ * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                         (f"{min(b15):.6g}" if bd else ""), (f"{max(b15):.6g}" if bd else ""), 0, (f"{min(b30):.6g}" if bd else ""), (f"{max(b30):.6g}" if bd else ""), 0, f"{hf:.4f}", f"{float(np.median(yv)):.4f}", nn, nd, lab,
                         ("CALIBRATED" if out.get("calibration", {}).get("calibrated") else "NOT CALIBRATED") if "calibration" in out else "", f"{out['rho']['log10_rho']:.4f}" if "rho" in out else "",
                         "local control of the BUDHIES chain, NOT a high-z point", "the chain's output on a local sample whose a0 is known (SPARC scale 1.282 in s units); the BUDHIES row is not written; not a law statement"])
        H.write_points(os.path.join(HERE, f"cfg281_points{SFX}.csv"), pcols, rows)
        P(f"\n  points written: cfg281_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg281{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUT, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg281{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
