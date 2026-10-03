#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG301 -- the MIGHTEE-HI DR1 (COSMOS) catalogue width -> V -> baryon chain: a same-pipeline LOCAL a0 / calibration measurement and a distance-trend test,
plus the direct BTFR row of amendment A1.  kappa = 1/2 is FITTED.  No verdict words.
At z <= 0.093 this lane CANNOT separate FLAT from a0 ~ H(z) (the rival's lever is E(0.093) ~ 1.045, 2-4.5 % in a0): it measures the chain's local level
and the drift of that level with distance.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG301_mightee_hi_catalogue_width_chain/FROZEN_CRITERIA.md (2555ab142).
  cut     golden sample (five flags 0); 0.02 <= z_HI <= 0.093; 45 <= incl <= 80 deg; log M_HI >= 9.0; W50 >= 80 km/s and sigma_W50/W50 <= 0.15; SNR_3D >= 8
  chain   W_c = (W50 - delta)/(1+z), delta = 0; V = W_c/(2 sin i), catalogue inclination; M_gas = 1.33 M_HI; M_b = M_gas + M* (BAGPIPES);
          R = D_HI/2, D_HI = 10^(0.506 log M_HI - 3.293) kpc; g_bar = G M_b/R^2; g_obs = V^2/R; CFG223's median-residual s* (hzq_core), nu_mono,
          canonical a0 9.3603e-11 (alt 1.1312e-10 for M1); bootstrap over galaxies B = 4,000; windows = z_HI terciles W1 (nearest), W2, W3
  A1      a0_BTFR = V^4/(G M_b): median + bootstrap 68/95 % on (i) all survivors, (ii) M_gas > M*, (iii) y < 0.5 at D_HI/2; both footings
Run order: STAGE=A ; STAGE=SELFTEST ; STAGE=CC2 ; STAGE=B ; STAGE=B MUTATE=1 ; STAGE=B MUTATE=2 ; STAGE=M5   (each writes its own .out and _results.json)
  DRYRUN=1 STAGE=B [MUTATE=1|2]: the STAGE=B code on FABRICATED widths (the real widths not loaded), run once before the measurement as a code test (_DRYRUN outputs)

Implementation choices the frozen file leaves open, fixed HERE before any catalogue value was read (disclosed in the README):
  I1 windows: the survivors sorted by (z_HI, ID) and split by numpy.array_split into three equal-count groups.
  I2 "mass-matched": W1 and W2 are each matched to W3's log M_HI distribution (the high-z end is the mass-limited one): bins = W3's log M_HI quartiles
     (min, Q1, median, Q3, max; the last bin closed); every resample draws, with replacement, from the window's galaxies in each bin as many galaxies as W3
     has in that bin; window galaxies outside W3's range have weight 0; B = 4,000 resamples; the matched s* is the median over resamples of CFG223's
     estimator and its interval the 2.5/16/84/97.5 percentiles.  Matching is POSSIBLE for a window iff every bin holds >= 3 of its galaxies; this is
     decided at stage A from M_HI only.  If it is not possible, CC1/CC3 use the unmatched window and say so.  CC1 and CC3 always use the matched W1 when
     possible ("where needed" read as "always, when possible": a blind rule).
  I3 recipe half-width of an s* row: the draft's knobs, one at a time: delta = 11 km/s (one-sided: the full shift), M* +-0.25 dex (half the difference),
     D_HI (hence R) +-0.15 dex (half the difference; the draft names this knob twice, it is counted once), H0 = 67.4 (one-sided: the full shift; M_HI and
     M* scale as D^2); quadrature.  The isotropic sin 60 deg is the draft's "sensitivity": printed, and a second quadrature that includes it is printed;
     CC1(ii) uses the first.  Matched rows evaluate the knobs on the first 1,000 resamples (common random numbers), as CFG281.
  I4 D3: the slope of log10 s* on log10(median D_L of the window), ordinary least squares over the three windows; primary = the mass-matched windows
     (W1m, W2m against W3, the CC3 basis), jointly bootstrapped (resample b of W1m, W2m and bootstrap b of W3); the unmatched slope is a reported variant.
     rho_i = s*(W_i)/s*(W1m); its statistics-only width from the joint bootstrap of log rho; its recipe width by applying each knob to both windows.
  I5 A1 subsets are fixed at the primary recipe (a knob changes the values, not the membership); y = g_bar/a0 on the canonical footing (CFG260/281).
  I6 CC4 worlds: g_obs = g_bar nu(g_bar/(2 a0)) x 10^N(0, 0.15) (0.15 dex scatter at fixed g_bar), W = 2 sqrt(g_obs R) sin i (1+z) x (1 + 0.10 N(0,1))
     (10 % width errors), on the survivors' own M_HI, M*, z and catalogue inclinations; the pooled estimator with B = 4,000; PASS iff
     |median over 100 worlds of log10 s* - log10 2| <= 0.023 dex (CFG281's stated bias as the tolerance) AND the 95 % interval covers log10 2 in >= 90.
     Reported (not load-bearing): the same worlds on the pre-width-cut parent with W >= 80 km/s applied to the fabricated widths.
  I7 MUTATE responses are read on the pooled s*: MUTATE=1 against the main pooled s*; MUTATE=2 (sin i_eff = 0.70 for every galaxy) against the main run's
     isotropic sin 60 variant.  The selection is not re-applied.
  I8 M5: this script's chain function, fed CFG281's ALFALFA arrays (its selection, its seeds, delta 9, sin 60), reproduces CFG281's committed
     unmatched and matched s* (cfg281_stageB_results.json) to 1e-9 dex.
"""
import os, sys, json, math, time, inspect
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

TSTART = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common")); sys.path.insert(0, os.path.join(CFG, "CFG260_budhies_a0_z02"))
import hzq_core as H                                                         # CFG223's estimator (verbatim copy, a0implied), nu_mono, bands, helpers
import cfg260_core as C                                                      # CFG260's constants, D_L, the BUDHIES loader (non-width) for D4 and M5

STAGE = os.environ.get("STAGE", "").strip().upper()
MUT = int(os.environ.get("MUTATE", "0") or 0)
DRY = os.environ.get("DRYRUN", "0") == "1"                                   # STAGE=B code path on FABRICATED widths (law at s = 2); the real widths are not loaded
assert STAGE in ("A", "SELFTEST", "CC2", "B", "M5"), "set STAGE=A, SELFTEST, CC2, B or M5"
assert MUT in (0, 1, 2) and (MUT == 0 or STAGE == "B"), "MUTATE applies to STAGE=B only"
assert not DRY or STAGE == "B", "DRYRUN applies to STAGE=B only"
SFX = (f"_stage{STAGE}" if STAGE in ("A", "B") else f"_{STAGE}") + ("_DRYRUN" if DRY else "") + (f"_MUTATE{MUT}" if MUT else "")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}{'' if load_bearing else ' (not load-bearing)'}] {name}\n         {detail}")


P(__doc__.split("Implementation choices")[0].strip())
P(f"\nSTAGE {STAGE}" + ("  *** DRYRUN: FABRICATED widths (law at s_true = 2, 0.15 dex scatter, 10 % errors); the real widths are not loaded; a code test, not a measurement ***" if DRY else "") + (f"  *** MUTATE={MUT}: " + ("widths x 1.1892" if MUT == 1 else "sin i_eff = 0.70 for every galaxy") + " -- a reactivity test, not a measurement ***" if MUT else ""))

G, MSUN, KPC, CKMS = C.G, C.MSUN, C.KPC, C.CKMS
NU = H.NU
A0C, A0A = C.A0["canonical"], C.A0["alt"]                                   # FP0's full-precision values, as CFG260/281 (9.3603e-11, 1.1312e-10 to the quoted digits)
assert abs(A0C / H.A0C - 1) < 1e-5 and abs(A0A / H.A0A - 1) < 1e-5
SREF = 1.20 / 0.93603                                                        # SPARC-empirical scale on the canonical footing (1.282)
SIN60 = math.sin(math.radians(60.0))
B_FULL, B_VAR, MIN_PER_BIN = 4000, 1000, 3
CSVP = os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv")
SHA_EXPECT = "bcf9e8558bc56448"
FLAGS = ["low_confidence_flag", "blended_flag", "confused_flag", "bad_ellipse_flag", "contaminated_source_flag"]
NONWIDTH = ["ID_catalogue", "z_HI", "D_L_Mpc", "S_HI_Jy_Hz", "log_M_HI", "log_M_HI_err", "SNR_3D", "incl_deg", "axis_ratio", "log_M_stel", "log_M_stel_err"] + FLAGS
WIDTHS = ["W_50_km_s", "W_50_km_s_err"]                                     # read for the cut at stage A (never printed); loaded as data only at STAGE=B
EXPECTED_COLS = ("ID_catalogue,RA_deg,Dec_deg,freq_MHz,z_HI,z_spec,D_L_Mpc,S_HI_Jy_Hz,S_HI_Jy_Hz_err,log_M_HI,log_M_HI_err,SNR_3D,W_50_km_s,W_50_km_s_err,"
                 "incl_deg,axis_ratio,log_M_stel,log_M_stel_err,sfr_M_sol_year,sfr_M_sol_year_err,m_g,m_g_err,m_r,m_r_err,m_i,m_i_err,m_z,m_z_err,m_y,m_y_err,"
                 "m_Y,m_Y_err,m_J,m_J_err,m_H,m_H_err,m_K,m_K_err,low_confidence_flag,blended_flag,confused_flag,bad_ellipse_flag,contaminated_source_flag").split(",")
J281 = json.load(open(os.path.join(CFG, "CFG281_budhies_local_control", "cfg281_stageB_results.json")))["numbers"]["out"]
S281 = float(J281["LC"]["s"])                                                # CFG281's ALFALFA matched value (1.449)
STAGEA_JSON = os.path.join(HERE, "cfg301_stageA_results.json")
REC0 = dict(delta=0.0, k=1, sini=None, tau_ms=0.0, tau_b=0.0, rdex=0.0, h0=70.0)   # sini None = the catalogue inclination
KNOBS = (("delta", "one", (11.0,), "delta = 11 km/s (primary 0)"), ("tau_ms", "two", (-0.25, 0.25), "M* zero point +-0.25 dex"),
         ("rdex", "two", (-0.15, 0.15), "D_HI (R) scale +-0.15 dex"), ("h0", "one", (67.4,), "H0 = 67.4 (primary 70)"))
SENS = ("sini", "one", (SIN60,), "isotropic sin 60 deg (the draft's sensitivity)")
BTFR_KNOBS = (("tau_ms", "two", (-0.25, 0.25), "M* +-0.25 dex"), ("sini", "one", (SIN60,), "isotropic sin 60 deg"), ("delta", "one", (11.0,), "delta = 11 km/s"))
TAUS = (-0.30, -0.15, 0.15, 0.30)


# ================================================================== the chain (CFG260/281's formulae with this catalogue's inputs)
def chain(a, W, rec):
    """a: dict of arrays mhi, ms (Msun, catalogue distances), z, sini (catalogue); W: widths (km/s).  Returns the per-galaxy quantities."""
    ds = 70.0 / rec["h0"]
    Mhi = a["mhi"] * ds ** 2
    Ms = a["ms"] * ds ** 2 * 10 ** rec["tau_ms"]
    Mg = 1.33 * Mhi
    tb = 10 ** rec["tau_b"]
    Mg, Ms = Mg * tb, Ms * tb
    Mb = Mg + Ms
    R = 0.5 * 10 ** (0.506 * np.log10(Mhi) - 3.293 + rec["rdex"]) * KPC
    sini = a["sini"] if rec["sini"] is None else rec["sini"]
    Wc = (np.asarray(W, float) - rec["delta"]) / (1 + a["z"]) ** rec["k"]
    ok = Wc > 0
    V = np.where(ok, Wc, np.nan) / (2 * sini) * 1e3
    gb = G * Mb * MSUN / R ** 2
    go = V ** 2 / R
    return dict(D=go / gb, gb=gb, go=go, V=V, ok=ok, Mb=Mb, Mg=Mg, Ms=Ms, R=R, y=gb / A0C)


def law_widths(a, rec, s, rng=None, scat=0.0, werr=0.0):
    """the inverse chain: widths placed on the law at scale s (optionally with dex scatter in g_obs and fractional width errors)"""
    d0 = chain(a, np.full(len(a["z"]), 100.0), rec)
    go = d0["gb"] * C.nuv(NU, d0["gb"] / (A0C * s))
    if scat > 0:
        go = go * 10 ** rng.normal(0.0, scat, go.shape)
    sini = a["sini"] if rec["sini"] is None else rec["sini"]
    W = 2 * np.sqrt(go * d0["R"]) / 1e3 * sini * (1 + a["z"]) ** rec["k"]
    if werr > 0:
        W = W * (1 + werr * rng.normal(0.0, 1.0, W.shape))
    return W + rec["delta"]


def est(D, gb, a0=A0C):
    return H.AI.implied(D, gb, NU, a0)                                      # CFG223's estimator, verbatim (vectorised over rows)


def est1(D, gb, a0=A0C):
    l, u = est(D, gb, a0); return float(l[0]), bool(u[0])


def rng_of(*tags):
    return np.random.default_rng(np.random.SeedSequence([301] + [int(t) for t in tags]))


def boot_full(D, gb, B, tag, a0=A0C):
    n = len(D); I = rng_of(tag, n).integers(0, n, size=(B, n)); lb, ub = est(D[I], gb[I], a0); return lb, ub


def pct(x, q=(2.5, 16, 84, 97.5)):
    return [float(v) for v in np.percentile(x, q)]


def match_plan(win, ref, lmhi):
    q = np.percentile(lmhi[ref], [0, 25, 50, 75, 100])
    inb = [(lmhi >= q[i]) & ((lmhi < q[i + 1]) if i < 3 else (lmhi <= q[i + 1])) for i in range(4)]
    rc = [int(b[ref].sum()) for b in inb]
    wm = [win[b[win]] for b in inb]
    return dict(edges=q.tolist(), ref_counts=rc, win_counts=[len(x) for x in wm], members=wm, feasible=bool(all(len(x) >= MIN_PER_BIN for x in wm)),
                outside=int(len(win) - sum(len(x) for x in wm)))


def match_idx(plan, B, tag):
    r = rng_of(tag)
    return np.concatenate([m[r.integers(0, len(m), size=(B, c))] for m, c in zip(plan["members"], plan["ref_counts"])], axis=1)


# ================================================================== the catalogue and the frozen cut
def load(widths):
    hdr = open(CSVP).readline().strip().split(",")
    d = pd.read_csv(CSVP, usecols=NONWIDTH + (WIDTHS if widths else []), dtype={"ID_catalogue": str})
    return hdr, d


def cut(d, w=None):
    """the frozen cut (a)-(f) in the draft's order plus (g) valid inputs; w = the width frame (None: the parent without cut (e))."""
    steps = [("catalogue", len(d))]
    m = np.ones(len(d), bool)
    m &= (d[FLAGS].fillna(1).values == 0).all(axis=1); steps.append(("(a) golden sample: five flags 0", int(m.sum())))
    m &= d.z_HI.between(0.02, 0.093).values; steps.append(("(b) 0.02 <= z_HI <= 0.093", int(m.sum())))
    m &= d.incl_deg.between(45.0, 80.0).values; steps.append(("(c) 45 <= incl <= 80 deg", int(m.sum())))
    m &= (d.log_M_HI >= 9.0).values; steps.append(("(d) log M_HI >= 9.0", int(m.sum())))
    if w is not None:
        ww, ee = w.W_50_km_s.values.astype(float), w.W_50_km_s_err.values.astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            m &= np.isfinite(ww) & np.isfinite(ee) & (ww >= 80.0) & (ee / ww <= 0.15)
        steps.append(("(e) W50 >= 80 km/s and sigma_W50/W50 <= 0.15", int(m.sum())))
    else:
        steps.append(("(e) not applied (parent)", int(m.sum())))
    m &= (d.SNR_3D >= 8.0).values; steps.append(("(f) SNR_3D >= 8", int(m.sum())))
    m &= np.isfinite(d[["z_HI", "D_L_Mpc", "log_M_HI", "incl_deg", "log_M_stel"]].values.astype(float)).all(axis=1) & (d.log_M_stel > 0).values
    steps.append(("(g) valid inputs (finite; log M* > 0)", int(m.sum())))
    return m, steps


def arrays(S):
    return dict(mhi=10 ** S.log_M_HI.values.astype(float), ms=10 ** S.log_M_stel.values.astype(float), z=S.z_HI.values.astype(float),
                sini=np.sin(np.radians(S.incl_deg.values.astype(float))))


def windows_of(n):
    return [np.asarray(x) for x in np.array_split(np.arange(n), 3)]


def sorted_survivors(d, m):
    S = d[m].copy()
    return S.sort_values(["z_HI", "ID_catalogue"], kind="mergesort").reset_index(drop=True)


hdr, d = load(widths=(STAGE == "B" and not DRY)) if STAGE in ("A", "SELFTEST", "B") else (None, None)
if d is not None:
    P(f"catalogue {os.path.relpath(CSVP, REPO)} sha256 {H.sha(CSVP)}; {len(d)} rows; width columns loaded as data: {STAGE == 'B' and not DRY}")


# ================================================================== STAGE A: counts only
if STAGE == "A":
    P("\nSTAGE A  COUNTS ONLY (the width columns are read by the cut code for cut (e) and discarded; no width, V, g_obs or s* is computed or printed)")
    ok_load = (len(d) == 293 and hdr == EXPECTED_COLS and H.sha(CSVP) == SHA_EXPECT and d.ID_catalogue.is_unique and not any(c in d.columns for c in WIDTHS))
    check("A1 CONTROL (loader): 293 rows, the 43 expected column names in order, sha256 prefix bcf9e8558bc56448, unique IDs; the data frame carries no width column",
          f"rows {len(d)}; header match {hdr == EXPECTED_COLS} ({len(hdr)} columns); sha {H.sha(CSVP)}; IDs unique {d.ID_catalogue.is_unique}; width columns in the frame {[c for c in d.columns if c in WIDTHS]}", ok_load)
    wcut = pd.read_csv(CSVP, usecols=WIDTHS)
    m, steps = cut(d, wcut)
    mpar, steps_par = cut(d, None)
    del wcut
    P("selection: " + " -> ".join(f"{k} {v}" for k, v in steps))
    P("parent (all cuts except (e), for the SELFTEST's width-cut variant): " + " -> ".join(f"{k} {v}" for k, v in steps_par[1:]))
    S = sorted_survivors(d, m); N = len(S); SP = sorted_survivors(d, mpar)
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read(); seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}; exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr = np.random.default_rng(1234); same = True; same60 = True
    for _ in range(200):
        Dq = 10 ** rr.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr.uniform(-12, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = est(Dq, gq); a3, u3 = C.implied(Dq, gq, NU, A0C)
        same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2); same60 = same60 and float(np.max(np.abs(a1 - a3))) < 1e-12 and np.array_equal(u1, u3)
    check("A2 CONTROL: the estimator used here (hzq_core / a0implied) equals CFG223's original bit for bit and cfg260_core.implied to 1e-12 on 200 random sets", f"bit-identical to CFG223 {same}; cfg260_core within 1e-12 {same60}", bool(same and same60))
    W3s = windows_of(N)
    check("A3 CONTROL: three equal-count windows (sizes differ by at most 1) partition the survivors in z order", f"sizes {[len(w) for w in W3s]}; N {N}",
          N >= 3 and max(len(w) for w in W3s) - min(len(w) for w in W3s) <= 1 and sum(len(w) for w in W3s) == N)
    mhi_id = np.log10(49.7 * S.D_L_Mpc.values ** 2 * S.S_HI_Jy_Hz.values); dev = np.abs(S.log_M_HI.values - mhi_id)
    check("A4 (reported) the catalogue's M_HI identity log M_HI = log10(49.7 D_L^2 S_HI[Jy Hz]) over the survivors", f"max deviation {float(dev.max()):.4f} dex, median {float(np.median(dev)):.4f} (a form from memory; not load-bearing)", float(dev.max()) <= 0.02, load_bearing=False)
    dlc = np.array([C.DL_mpc(float(z)) for z in S.z_HI.values]); rdl = np.abs(S.D_L_Mpc.values / dlc - 1)
    check("A5 (reported) D_L_Mpc equals flat LCDM (H0 70, Omega_M 0.3) at z_HI to 0.5 % (the catalogue's stated distances; the basis of the H0 knob)", f"max |D_L/D_L(z) - 1| {float(rdl.max()):.4f}, median {float(np.median(rdl)):.5f}", float(rdl.max()) <= 0.005, load_bearing=False)
    a = arrays(S); dd0 = chain(a, np.full(N, 100.0), REC0)                     # baryon side only (the width argument is a dummy; V and g_obs are not used)
    y = dd0["y"]; gf = dd0["Mg"] / dd0["Mb"]; lmhi = S.log_M_HI.values.astype(float)
    P("\nA-COUNTS  windows (z_HI terciles) and the baryon side (no width)")
    win_rows = []
    for i, w in enumerate(W3s):
        zz = S.z_HI.values[w]; DL = S.D_L_Mpc.values[w]
        row = dict(n=len(w), z_min=float(zz.min()), z_max=float(zz.max()), z_med=float(np.median(zz)), DL_med=float(np.median(DL)), lmhi_q=pct(lmhi[w], (0, 25, 50, 75, 100)),
                   y_q=pct(y[w], (5, 25, 50, 75, 95)), frac_y_lt_05=float(np.mean(y[w] < 0.5)), gas_frac_med=float(np.median(gf[w])), n_gas_dom=int(np.sum(dd0["Mg"][w] > dd0["Ms"][w])))
        win_rows.append(row)
        P(f"    W{i + 1}: N {row['n']}; z {row['z_min']:.4f}-{row['z_max']:.4f} (median {row['z_med']:.4f}); median D_L {row['DL_med']:.1f} Mpc; log M_HI min/Q1/med/Q3/max {np.array2string(np.array(row['lmhi_q']), precision=3)}; "
          f"y 5/25/50/75/95 % {np.array2string(np.array(row['y_q']), precision=3)}; fraction y < 0.5 {row['frac_y_lt_05']:.2f}; gas fraction median {row['gas_frac_med']:.2f}; gas-dominated {row['n_gas_dom']}")
    P(f"    pooled: N {N}; y 5/25/50/75/95 % {np.array2string(np.percentile(y, [5, 25, 50, 75, 95]), precision=3)}; deep subset (y < 0.5) {int(np.sum(y < 0.5))}; gas-dominated subset (M_gas > M*) {int(np.sum(dd0['Mg'] > dd0['Ms']))}; "
      f"gas fraction median {float(np.median(gf)):.2f}; R median {float(np.median(dd0['R']) / KPC):.1f} kpc; log M_HI median {float(np.median(lmhi)):.3f}; log M* median {float(np.median(S.log_M_stel)):.3f}")
    plans = {}
    for nm, w in (("W1", W3s[0]), ("W2", W3s[1])):
        pl = match_plan(w, W3s[2], lmhi); plans[nm] = pl
        P(f"    matching {nm} -> W3's log M_HI quartile bins {np.array2string(np.array(pl['edges']), precision=3)}: W3 per bin {pl['ref_counts']}, {nm} per bin {pl['win_counts']} ({pl['outside']} outside W3's range); POSSIBLE (>= {MIN_PER_BIN} per bin): {pl['feasible']}")
    he1 = bool(40 <= N <= 120)
    P(f"\nHAND ESTIMATE (A3, frozen): HE1 survivors N = {N} (estimate ~70, plausible 40-120): {'hit' if he1 else 'MISS (kept as it falls)'}")
    NUM.update(selection=steps, parent_selection=steps_par, N=N, windows=win_rows, matching={k: {kk: vv for kk, vv in v.items() if kk != 'members'} for k, v in plans.items()},
               survivor_ids=S.ID_catalogue.tolist(), parent_ids=SP.ID_catalogue.tolist(), window_ids=[S.ID_catalogue.values[w].tolist() for w in W3s],
               pooled=dict(y_q=pct(y, (5, 25, 50, 75, 95)), n_deep=int(np.sum(y < 0.5)), n_gas_dom=int(np.sum(dd0['Mg'] > dd0['Ms']))), hand_estimates=dict(HE1=he1),
               controls_numbers=dict(mhi_identity_max=float(dev.max()), dl_max_rel=float(rdl.max())))


# ================================================================== the survivors from stage A (SELFTEST and B)
if STAGE in ("SELFTEST", "B"):
    JA = json.load(open(STAGEA_JSON))["numbers"]
    mpar, steps_par = cut(d, None)
    SP = sorted_survivors(d, mpar)
    if STAGE == "B" and not DRY:
        m, steps = cut(d, d[WIDTHS])
        S = sorted_survivors(d, m)
    else:
        S = SP[SP.ID_catalogue.isin(set(JA["survivor_ids"]))].reset_index(drop=True)
    N = len(S); WIN = windows_of(N); a = arrays(S); lmhi = S.log_M_HI.values.astype(float); DLmed = [float(np.median(S.D_L_Mpc.values[w])) for w in WIN]
    same_ids = S.ID_catalogue.tolist() == JA["survivor_ids"] and [S.ID_catalogue.values[w].tolist() for w in WIN] == JA["window_ids"]
    check(f"{STAGE}-C0 CONTROL: the survivors and the windows equal stage A's (IDs, in order)", f"N {N} (stage A {JA['N']}); identical {same_ids}", bool(same_ids))
    PLANS = {nm: match_plan(w, WIN[2], lmhi) for nm, w in (("W1", WIN[0]), ("W2", WIN[1]))}


# ================================================================== STAGE SELFTEST (CC4): fabricated widths only
if STAGE == "SELFTEST":
    P("\nSTAGE SELFTEST (CC4)  *** FABRICATED widths; the real widths are not loaded ***")
    dn = 0.0
    for st in (0.5, 1.0, 2.5):
        Wf = law_widths(a, REC0, st); dd = chain(a, Wf, REC0)
        for ix in [np.arange(N)] + WIN:
            dn = max(dn, abs(est1(dd["D"][ix], dd["gb"][ix])[0] - math.log10(st)))
    check("S1 CONTROL (noiseless identity): widths from the inverse chain on the law at s_true = 0.5, 1, 2.5 (catalogue inclinations) return s_true to 1e-6 dex, pooled and in every window", f"max |d log10 s| {dn:.1e}", dn < 1e-6)
    worlds = []; t0 = time.time()
    for w in range(100):
        r = rng_of(4, w)
        Wf = law_widths(a, REC0, 2.0, rng=r, scat=0.15, werr=0.10); dd = chain(a, Wf, REC0)
        l0, u0 = est1(dd["D"], dd["gb"]); lb, ub = boot_full(dd["D"], dd["gb"], B_FULL, 40000 + w)
        q = np.percentile(lb, [2.5, 97.5]); worlds.append((l0, bool(q[0] <= math.log10(2.0) <= q[1]), float(np.mean(ub)), float(np.std(lb))))
    med = float(np.median([x[0] for x in worlds])); cov = int(sum(x[1] for x in worlds)); bias = med - math.log10(2.0)
    P(f"  100 worlds (s_true = 2, 0.15 dex scatter in g_obs, 10 % width errors, catalogue inclinations, pooled N {N}, B = {B_FULL}): median log10 s* {med:+.4f} (truth {math.log10(2.0):+.4f}; bias {bias:+.4f} dex); "
      f"SD over worlds {float(np.std([x[0] for x in worlds])):.4f}; median bootstrap SD {float(np.median([x[3] for x in worlds])):.4f}; 95 % interval covers the truth in {cov}/100; mean unbounded fraction {float(np.mean([x[2] for x in worlds])):.4f}  ({time.time() - t0:.0f} s)")
    check("CC4 (SELFTEST, frozen): |bias| <= 0.023 dex (CFG281's stated bias as the tolerance) AND the 95 % interval covers s_true in >= 90 of 100 worlds", f"bias {bias:+.4f} dex; coverage {cov}/100", abs(bias) <= 0.023 and cov >= 90)
    aP = arrays(SP); NPar = len(SP); vb = []; nsel = []
    for w in range(100):
        r = rng_of(5, w)
        Wf = law_widths(aP, REC0, 2.0, rng=r, scat=0.15, werr=0.10); keep = Wf >= 80.0
        dd = chain(aP, Wf, REC0); vb.append(est1(dd["D"][keep], dd["gb"][keep])[0] - math.log10(2.0)); nsel.append(int(keep.sum()))
    P(f"  reported variant (not load-bearing): the same worlds on the pre-width-cut parent (N {NPar}) with W >= 80 km/s applied to the fabricated widths: median selected N {int(np.median(nsel))}; median bias {float(np.median(vb)):+.4f} dex (SD {float(np.std(vb)):.4f})")
    NUM["selftest"] = dict(noiseless_max=dn, median=med, bias=bias, coverage=cov, sd_worlds=float(np.std([x[0] for x in worlds])), parent_variant=dict(n_parent=NPar, n_sel_median=int(np.median(nsel)), bias_median=float(np.median(vb)), bias_sd=float(np.std(vb))),
                           pass_cc4=bool(abs(bias) <= 0.023 and cov >= 90))


# ================================================================== STAGE CC2: SPARC closure of the baryon side
if STAGE == "CC2":
    P("\nSTAGE CC2  the recipe's baryon side on SPARC (Lelli+2016c table on disk; SPARC_table.txt is never read)")
    src = inspect.getsource(H.K4.load_sparc)
    gal = H.K4.load_sparc(); tab = [g for g in gal if g.get("meta")]
    check("C2-1 CONTROL (loader): CFG4_common.load_sparc reads SPARC_Lelli2016c.mrt (never SPARC_table.txt) and returns 175 galaxies, each with its table row",
          f"source names the .mrt {('SPARC_Lelli2016c.mrt' in src)}; names SPARC_table.txt {('SPARC_table.txt' in src)}; galaxies {len(gal)}, with table rows {len(tab)}",
          "SPARC_Lelli2016c.mrt" in src and "SPARC_table.txt" not in src and len(gal) == 175 and len(tab) == 175)
    st = [("table rows", len(tab))]
    sel = [g for g in tab if g["meta"]["Q"] <= 2]; st.append(("Q <= 2", len(sel)))
    sel = [g for g in sel if g["meta"]["Inc"] >= 30.0]; st.append(("i >= 30 deg", len(sel)))
    sel = [g for g in sel if g["meta"]["Vflat"] > 0]; st.append(("V_flat > 0", len(sel)))
    sel = [g for g in sel if g["meta"]["MHI"] > 0]; st.append(("M_HI > 0", len(sel)))
    P("selection: " + " -> ".join(f"{k} {v}" for k, v in st))
    MHI = np.array([g["meta"]["MHI"] for g in sel]) * 1e9; L36 = np.array([g["meta"]["L36"] for g in sel]) * 1e9
    VF = np.array([g["meta"]["Vflat"] for g in sel]) * 1e3; RHI = np.array([g["meta"]["RHI"] for g in sel])
    Mb = 1.33 * MHI + 0.5 * L36; R = 0.5 * 10 ** (0.506 * np.log10(MHI) - 3.293) * KPC
    gb = G * Mb * MSUN / R ** 2; go = VF ** 2 / R; D = go / gb; yS = gb / A0C
    l0, u0 = est1(D, gb); lb, ub = boot_full(D, gb, B_FULL, 2)
    s0 = 10 ** l0; off = math.log10(s0 / SREF)
    P(f"  SPARC closure: N {len(sel)}; s* = {s0:.4f} (log10 {l0:+.4f}); a0 = {s0 * A0C:.4e} m/s^2; bootstrap SD {float(np.std(lb)):.4f} dex; 68 % [{10 ** pct(lb)[1]:.4f}, {10 ** pct(lb)[2]:.4f}], 95 % [{10 ** pct(lb)[0]:.4f}, {10 ** pct(lb)[3]:.4f}]; "
      f"no root {u0}; offset from the SPARC scale {SREF:.3f}: {off:+.4f} dex; y quartiles {np.array2string(np.percentile(yS, [25, 50, 75]), precision=3)}")
    rh = RHI > 0
    Rm = RHI[rh] * KPC; gbm = G * Mb[rh] * MSUN / Rm ** 2; Dm = (VF[rh] ** 2 / Rm) / gbm; lm, um = est1(Dm, gbm)
    lr, ur = est1(D[rh], gb[rh]); sz = float(np.median(np.log10(R[rh] / Rm)))
    P(f"  reported diagnostic (not a criterion): the {int(rh.sum())} galaxies with a measured R_HI: s* with the size relation {10 ** lr:.4f}, with the measured R_HI {10 ** lm:.4f} (median log10(R_relation/R_HI) {sz:+.3f} dex)")
    a0b = VF ** 4 / (G * Mb * MSUN); mb = float(np.median(a0b)); yy = yS < 0.5
    P(f"  reported diagnostic: SPARC BTFR level V_flat^4/(G M_b) with M/L 0.5: median {mb:.4e} m/s^2 = {math.log10(mb / A0C):+.3f} dex vs canonical, {math.log10(mb / A0A):+.3f} dex vs alt (N {len(sel)}); "
      f"on y < 0.5 at the size-relation radius (N {int(yy.sum())}): {float(np.median(a0b[yy])):.4e}")
    ok2 = abs(off) <= 0.15
    check("CC2 (calibration control, frozen; a finding, not a code failure): SPARC closure s* within +-0.15 dex of 1.282", f"s* {s0:.4f}: offset {off:+.4f} dex", ok2, load_bearing=False)
    he4 = bool(abs(off) <= 0.2)
    P(f"\nHAND ESTIMATE (A3, frozen): HE4 the CC2 closure within +-0.2 dex: offset {off:+.4f}: {'hit' if he4 else 'MISS (kept as it falls)'}")
    NUM.update(selection=st, n=len(sel), log_s=l0, s=s0, unb=u0, sd=float(np.std(lb)), q=pct(lb), offset_dex=off, pass_cc2=ok2, y_q=pct(yS, (25, 50, 75)),
               rhi_diag=dict(n=int(rh.sum()), s_relation=10 ** lr, s_measured_RHI=10 ** lm, median_log_R_ratio=sz), btfr_sparc=dict(median=mb, deep_median=float(np.median(a0b[yy])), n_deep=int(yy.sum())),
               hand_estimates=dict(HE4=he4))


# ================================================================== STAGE B: the measurement (once) and MUTATE=1/2
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (f" (MUTATE={MUT})" if MUT else ""))
    W = law_widths(a, REC0, 2.0, rng=rng_of(9, 0), scat=0.15, werr=0.10) if DRY else S.W_50_km_s.values.astype(float)
    rec = dict(REC0)
    if MUT == 1:
        W = (W - rec["delta"]) * 1.1892 + rec["delta"]
    if MUT == 2:
        rec["sini"] = 0.70
    dd = chain(a, W, rec)
    check("B1 CONTROL: every survivor has W - delta > 0 (no galaxy dropped by the chain)", f"dropped {int((~dd['ok']).sum())} of {N}", bool(dd["ok"].all()))
    D, gb = dd["D"], dd["gb"]; ALL = np.arange(N)
    lP, uP = est1(D, gb); lbP, ubP = boot_full(D, gb, B_FULL, 10)
    if MUT:
        main = json.load(open(os.path.join(HERE, "cfg301_stageB" + ("_DRYRUN" if DRY else "") + "_results.json")))["numbers"]
        ref = main["pooled"]["log_s"] if MUT == 1 else main["recipe"]["pooled"]["rows"]["sini"]["log_s"][0]
        resp = lP - ref; lo_, hi_ = (0.25, 0.35) if MUT == 1 else (0.31, 0.43)
        # the regime's own expectation (diagnostic): the same galaxies placed on the law at the main pooled s*, then the same mutation
        s_main = 10 ** main["pooled"]["log_s"]; Wl = law_widths(a, REC0, s_main)
        base_l = est1(*[chain(a, Wl, dict(REC0, sini=(SIN60 if MUT == 2 else None)))[k] for k in ("D", "gb")])[0]
        Wm = (Wl - REC0["delta"]) * 1.1892 + REC0["delta"] if MUT == 1 else Wl
        mut_l = est1(*[chain(a, Wm, dict(REC0, sini=(0.70 if MUT == 2 else None)))[k] for k in ("D", "gb")])[0]
        win_s = [10 ** est1(D[w], gb[w])[0] for w in WIN]
        P(f"  MUTATED pooled s* {10 ** lP:.4f} (log10 {lP:+.4f}; bootstrap SD {float(np.std(lbP)):.4f}); windows {', '.join(f'{x:.4f}' for x in win_s)}  [MUTATED -- a reactivity test, not a measurement]")
        P(f"  reference: " + ("the main pooled s*" if MUT == 1 else "the main run's isotropic sin 60 variant of the pooled s*") + f" log10 {ref:+.4f}; response {resp:+.4f} dex")
        P(f"  diagnostic (not a criterion): the same galaxies placed on the law at the main pooled s* respond by {mut_l - base_l:+.4f} dex (the regime's own expectation for this mutation)")
        check(f"M2 MUTATE={MUT} (reactivity, frozen): " + ("widths x 1.1892 raise the pooled s* by 0.30 +- 0.05 dex" if MUT == 1 else "sin i_eff 0.70 (against the isotropic sin 60 variant) raises the pooled s* by 0.37 +- 0.06 dex"),
              f"response {resp:+.4f} dex (window {lo_}-{hi_}); regime expectation {mut_l - base_l:+.4f}", lo_ <= resp <= hi_)
        NUM.update(mutate=MUT, pooled=dict(log_s=lP, s=10 ** lP, sd=float(np.std(lbP))), windows=win_s, reference_log_s=ref, response=resp, regime_expectation=mut_l - base_l)
    else:
        JS = json.load(open(os.path.join(HERE, "cfg301_SELFTEST_results.json"))); JC = json.load(open(os.path.join(HERE, "cfg301_CC2_results.json")))
        # ---------------- sets: pooled, windows (unmatched), matched W1m and W2m
        res = {}
        res["pooled"] = dict(n=N, log_s=lP, s=10 ** lP, a0=10 ** lP * A0C, unb=uP, sd=float(np.std(lbP)), q=pct(lbP), unb_frac=float(np.mean(ubP)), y_q=pct(dd["y"], (25, 50, 75)))
        LBW = []
        for i, w in enumerate(WIN):
            l0, u0 = est1(D[w], gb[w]); lb, ub = boot_full(D[w], gb[w], B_FULL, 11 + i); LBW.append(lb)
            res[f"W{i + 1}"] = dict(n=len(w), log_s=l0, s=10 ** l0, a0=10 ** l0 * A0C, unb=u0, sd=float(np.std(lb)), q=pct(lb), unb_frac=float(np.mean(ub)), y_q=pct(dd["y"][w], (25, 50, 75)),
                                    z_med=float(np.median(a["z"][w])), DL_med=DLmed[i])
        IDXM, LSM = {}, {}
        for j, nm in enumerate(("W1", "W2")):
            pl = PLANS[nm]
            if pl["feasible"]:
                IDXM[nm] = match_idx(pl, B_FULL, 20 + j)
                ls, us = est(D[IDXM[nm]], gb[IDXM[nm]]); LSM[nm] = ls
                qm = np.percentile(lmhi[IDXM[nm][:B_VAR]].ravel(), [25, 50, 75]); qr = np.percentile(lmhi[WIN[2]], [25, 50, 75])
                res[f"{nm}m"] = dict(n=int(IDXM[nm].shape[1]), log_s=float(np.median(ls)), s=10 ** float(np.median(ls)), a0=10 ** float(np.median(ls)) * A0C, sd=float(np.std(ls)), q=pct(ls), unb_frac=float(np.mean(us)),
                                     mhi_q=qm.tolist(), mhi_q_ref=qr.tolist())
                ed = pl["edges"]
                inb_draw = [((lmhi[IDXM[nm]] >= ed[b_]) & ((lmhi[IDXM[nm]] < ed[b_ + 1]) if b_ < 3 else (lmhi[IDXM[nm]] <= ed[b_ + 1]))).sum(axis=1) for b_ in range(4)]
                cnt_ok = all(bool(np.all(inb_draw[b_] == pl["ref_counts"][b_])) for b_ in range(4)) and bool(np.all(np.isin(IDXM[nm], WIN[0 if nm == "W1" else 1])))
                check(f"B2 CONTROL: every {nm} matched resample draws only {nm} galaxies and exactly W3's count in each of W3's log M_HI quartile bins", f"per-bin counts W3 {pl['ref_counts']}; all {B_FULL} resamples match: {cnt_ok}", cnt_ok)
                P(f"         (reported) matched log M_HI Q1/med/Q3 {np.array2string(qm, precision=3)} against W3's {np.array2string(qr, precision=3)}")
            else:
                P(f"  matching {nm} -> W3 NOT POSSIBLE (decided at stage A: per-bin counts {pl['win_counts']}, need >= {MIN_PER_BIN}); the unmatched {nm} is used")
        SPEC = {"pooled": ("full", ALL), "W1": ("full", WIN[0]), "W2": ("full", WIN[1]), "W3": ("full", WIN[2])}
        for nm in IDXM:
            SPEC[f"{nm}m"] = ("matched", IDXM[nm])

        def ev(spec, dk):
            kind, ix = spec
            if kind == "full":
                return est1(dk["D"][ix], dk["gb"][ix])[0]
            l, u = est(dk["D"][ix[:B_VAR]], dk["gb"][ix[:B_VAR]]); return float(np.median(l))
        DDK = {}
        for key, kind, vals, lab in KNOBS + (SENS,) + BTFR_KNOBS:
            for v in vals:
                DDK[(key, v)] = chain(a, W, dict(rec, **{key: v}))
        for t in TAUS:
            DDK[("tau_b", t)] = chain(a, W, dict(rec, tau_b=t))
        REC = {}
        for nm, spec in SPEC.items():
            ref = ev(spec, dd); rows = {}
            for key, kind, vals, lab in KNOBS + (SENS,):
                ls = [ev(spec, DDK[(key, v)]) for v in vals]
                rows[key] = dict(label=lab, log_s=ls, half=(abs(ls[0] - ref) if kind == "one" else 0.5 * abs(ls[1] - ls[0])))
            h4 = math.sqrt(sum(rows[k]["half"] ** 2 for k, _, _, _ in KNOBS)); h5 = math.sqrt(h4 ** 2 + rows["sini"]["half"] ** 2)
            bands = {f"{t:+.2f}": 10 ** ev(spec, DDK[("tau_b", t)]) for t in TAUS}
            REC[nm] = dict(ref_log_s=ref, rows=rows, half=h4, half_with_sin60=h5, bands=bands)
            res[nm]["recipe_half"] = h4; res[nm]["recipe_half_with_sin60"] = h5; res[nm]["bands"] = bands
        # ---------------- M1: footings
        lA, uA = est1(D, gb, A0A); m1 = abs(lA + math.log10(A0A / A0C) - lP)
        check("M1 CONTROL: the alt footing implies the same absolute a0 (pooled)", f"|d log10 a0| = {m1:.1e}", m1 < 1e-9)
        # ---------------- calibration controls
        w1k = "W1m" if "W1" in IDXM else "W1"; w2k = "W2m" if "W2" in IDXM else "W2"
        s1 = res[w1k]["s"]; o_sp = math.log10(s1 / SREF); o_281 = math.log10(s1 / S281); h1 = res[w1k]["recipe_half"]
        cc1 = abs(o_sp) <= 0.15 and abs(o_281) <= 0.15 and h1 <= 0.20
        drift = res["W3"]["log_s"] - res[w1k]["log_s"]; cc3 = abs(drift) <= 0.10
        cc2 = bool(JC["numbers"]["pass_cc2"]); cc4 = bool(JS["numbers"]["selftest"]["pass_cc4"])
        CAL = bool(cc1 and cc2 and cc3)
        TAG = "" if CAL else "   [NOT CALIBRATED — not an a0 measurement]"
        P("\nCALIBRATION CONTROLS (frozen, section 3; evaluated before the a0 numbers below are printed)")
        check(f"CC1 (calibration control; a finding, not a code failure): {w1k} s* within +-0.15 dex of 1.282 AND of CFG281's {S281:.3f}, recipe half-width <= 0.20 dex",
              f"{w1k} s* {s1:.4f}: {o_sp:+.4f} dex vs 1.282, {o_281:+.4f} dex vs {S281:.3f}; recipe half-width {h1:.3f} (with the sin 60 sensitivity {res[w1k]['recipe_half_with_sin60']:.3f})", cc1, load_bearing=False)
        check("CC2 (calibration control, from STAGE=CC2): SPARC closure within +-0.15 dex of 1.282", f"s* {JC['numbers']['s']:.4f}: offset {JC['numbers']['offset_dex']:+.4f} dex", cc2, load_bearing=False)
        check(f"CC3 (calibration control; a finding): |log10 s*(W3) - log10 s*({w1k})| <= 0.10 dex", f"drift {drift:+.4f} dex", cc3, load_bearing=False)
        check("CC4 (from STAGE=SELFTEST): the estimator recovers s_true = 2 on fabricated widths", f"bias {JS['numbers']['selftest']['bias']:+.4f} dex, coverage {JS['numbers']['selftest']['coverage']}/100", cc4, load_bearing=False)
        P(f"  D1 CALIBRATION STATUS (CC1-CC3): {'CALIBRATED' if CAL else 'NOT CALIBRATED'}" + ("" if CAL else f" (failed: {', '.join(k for k, v in (('CC1', cc1), ('CC2', cc2), ('CC3', cc3)) if not v)})"))
        # ---------------- D2: the level
        P("\nD2  THE LEVEL (s* = implied a0 / 9.3603e-11; a0 = s* x 9.3603e-11 m/s^2; bootstrap over galaxies, B = 4,000)" + ("" if CAL else "  -- every number in D2-D4 and A1: NOT CALIBRATED, not an a0 measurement"))
        for nm in ["W1", "W2", "W3", "W1m", "W2m", "pooled"]:
            if nm not in res:
                continue
            r = res[nm]; q = r["q"]
            extra = (f"; z median {r['z_med']:.4f}, median D_L {r['DL_med']:.1f} Mpc" if "z_med" in r else "") + (f"; matched to W3 (log M_HI quartiles {np.array2string(np.array(r['mhi_q']), precision=3)})" if "mhi_q" in r else "")
            P(f"  {nm}: N {r['n']}; s* = {r['s']:.4f} (log10 {r['log_s']:+.4f}); a0 = {r['a0']:.4e}; SD {r['sd']:.4f} dex; 68 % [{10 ** q[1]:.4f}, {10 ** q[2]:.4f}], 95 % [{10 ** q[0]:.4f}, {10 ** q[3]:.4f}]; "
              f"no-root fraction {r['unb_frac']:.4f}; recipe half-width {r['recipe_half']:.3f} dex ({r['recipe_half_with_sin60']:.3f} with sin 60); "
              f"bands -0.30/-0.15/+0.15/+0.30: {', '.join(f'{v:.3f}' for v in r['bands'].values())}" + (f"; y Q1/med/Q3 {np.array2string(np.array(r['y_q']), precision=3)}" if "y_q" in r else "") + extra + TAG)
        for nm in ("pooled", w1k):
            rows = REC[nm]["rows"]
            P(f"  recipe knobs ({nm}; half-width, dex): " + "; ".join(f"{v['label']}: {v['half']:.3f}" for v in rows.values()) + f"; quadrature (draft knobs) {REC[nm]['half']:.3f}, with sin 60 {REC[nm]['half_with_sin60']:.3f}" + TAG)
        # ---------------- D3: the distance trend
        P("\nD3  THE DISTANCE TREND" + TAG)
        X = np.log10(np.array(DLmed))

        def slope(Y):
            Y = np.atleast_2d(Y); xm = X.mean()
            return ((X - xm) * (Y - Y.mean(axis=1, keepdims=True))).sum(axis=1) / ((X - xm) ** 2).sum()
        L1 = LSM["W1"] if "W1" in LSM else LBW[0]; L2 = LSM["W2"] if "W2" in LSM else LBW[1]; L3 = LBW[2]
        sl_pt = float(slope(np.array([res[w1k]["log_s"], res[w2k]["log_s"], res["W3"]["log_s"]]))[0]); sl_b = slope(np.vstack([L1, L2, L3]).T)
        slu_pt = float(slope(np.array([res["W1"]["log_s"], res["W2"]["log_s"], res["W3"]["log_s"]]))[0]); slu_b = slope(np.vstack(LBW).T)
        P(f"  median D_L of W1/W2/W3: {', '.join(f'{x:.1f}' for x in DLmed)} Mpc")
        P(f"  slope d log10 s* / d log10 D_L, {w1k}/{w2k}/W3 (primary): {sl_pt:+.3f}; joint bootstrap median {float(np.median(sl_b)):+.3f}, 68 % [{pct(sl_b)[1]:+.3f}, {pct(sl_b)[2]:+.3f}], 95 % [{pct(sl_b)[0]:+.3f}, {pct(sl_b)[3]:+.3f}]" + TAG)
        P(f"  slope, unmatched W1/W2/W3 (variant): {slu_pt:+.3f}; bootstrap 68 % [{pct(slu_b)[1]:+.3f}, {pct(slu_b)[2]:+.3f}], 95 % [{pct(slu_b)[0]:+.3f}, {pct(slu_b)[3]:+.3f}]" + TAG)
        RHO = {}
        for nm, Lb, key in ((w2k, L2, w2k), ("W3", L3, "W3")):
            lr = res[key]["log_s"] - res[w1k]["log_s"]; sd = float(np.std(Lb - L1))
            hr2 = 0.0
            for kk, kind, vals, lab in KNOBS:
                a_ = REC[key]["rows"][kk]["log_s"]; b_ = REC[w1k]["rows"][kk]["log_s"]
                if kind == "one":
                    hr2 += ((a_[0] - b_[0]) - (REC[key]["ref_log_s"] - REC[w1k]["ref_log_s"])) ** 2
                else:
                    hr2 += (0.5 * ((a_[1] - b_[1]) - (a_[0] - b_[0]))) ** 2
            hr = math.sqrt(hr2); tot = math.hypot(sd, hr)
            RHO[nm] = dict(log_rho=lr, rho=10 ** lr, sd_stat=sd, recipe_half=hr, sd_tot=tot, pull_stat=lr / sd, pull_tot=lr / tot)
            P(f"  rho({nm}/{w1k}) = {10 ** lr:.4f} (log10 {lr:+.4f} +- {sd:.4f} statistics; recipe half-width of log rho {hr:.4f}; total {tot:.4f}): pull against rho = 1 {lr / sd:+.2f} (statistics), {lr / tot:+.2f} (with the recipe width)" + TAG)
        zl = [res[f"W{i}"]["z_med"] for i in (1, 3)]; lev = math.log10(H.LAWS["H(z)"](zl[1]) / H.LAWS["H(z)"](zl[0]))
        P(f"  the rival's lever between W1 and W3 (z {zl[0]:.4f} -> {zl[1]:.4f}): log10 E ratio {lev:+.4f} dex, against a statistics-only width of log rho(W3) of {RHO['W3']['sd_stat']:.3f} dex: this lane cannot separate FLAT from a0 ~ H(z)")
        v281 = J281["variants"]; d281 = math.log10(v281["V1 50-85 Mpc"]["s"] / v281["V1 20-50 Mpc"]["s"])
        P(f"  CFG281 (ALFALFA, the BUDHIES chain): s* {v281['V1 20-50 Mpc']['s']:.3f} at 20-50 Mpc, {v281['V1 50-85 Mpc']['s']:.3f} at 50-85 Mpc: change {d281:+.3f} dex over a factor ~2 in distance (CFG281 recorded the drift 0.105 and fitted no slope); BUDHIES/ALFALFA rho = {J281['rho']['rho']:.3f} at z = 0.2 (log10 {J281['rho']['log10_rho']:+.3f})")
        # ---------------- D4: the extrapolation to the BUDHIES distance
        gals0 = C.load_galaxies(widths=False); zB = float(np.mean([g["z"] for g in C.select(gals0, "PC")])); DB = C.DL_mpc(zB); lev4 = math.log10(DB / DLmed[2])
        d4 = sl_pt * lev4; d4b = sl_b * lev4
        P(f"\nD4  EXTRAPOLATION, NOT A RESULT: if the primary slope continued from W3 (median D_L {DLmed[2]:.1f} Mpc) to the BUDHIES distance (z {zB:.4f}, D_L {DB:.0f} Mpc, H0 70): "
          f"d log10 s* = {sl_pt:+.3f} x {lev4:.3f} = {d4:+.3f} dex (bootstrap 68 % [{pct(d4b)[1]:+.3f}, {pct(d4b)[2]:+.3f}], 95 % [{pct(d4b)[0]:+.3f}, {pct(d4b)[3]:+.3f}]); for scale, BUDHIES/ALFALFA log10 rho = {J281['rho']['log10_rho']:+.3f} (CFG281)" + TAG)
        # ---------------- A1: the direct BTFR rows
        P("\nA1  THE DIRECT BTFR ROWS: a0_BTFR = V^4/(G M_b) per galaxy (deep-MOND limit; overestimates a0 where y is not small); median and bootstrap (B = 4,000)" + TAG)
        a0i = dd["V"] ** 4 / (G * dd["Mb"] * MSUN)
        SUB = {"(i) all survivors": ALL, "(ii) gas-dominated (M_gas > M*)": np.where(dd["Mg"] > dd["Ms"])[0], "(iii) deep (y < 0.5 at D_HI/2)": np.where(dd["y"] < 0.5)[0]}
        BT = {}
        for j, (nm, ix) in enumerate(SUB.items()):
            n = len(ix)
            if n < 3:
                BT[nm] = dict(n=n); P(f"  {nm}: N {n} -- too few for a median and bootstrap"); continue
            x = a0i[ix]; med = float(np.median(x)); I = rng_of(30 + j, n).integers(0, n, size=(B_FULL, n)); mb = np.median(x[I], axis=1); q = pct(mb)
            rows = {}
            for key, kind, vals, lab in BTFR_KNOBS:
                ms_ = [float(np.median((DDK[(key, v)]["V"] ** 4 / (G * DDK[(key, v)]["Mb"] * MSUN))[ix])) for v in vals]
                rows[key] = dict(label=lab, medians=ms_, half=(abs(math.log10(ms_[0] / med)) if kind == "one" else 0.5 * abs(math.log10(ms_[1] / ms_[0]))))
            hb = math.sqrt(sum(v["half"] ** 2 for v in rows.values()))
            # diagnostic added after STAGE=CC2 and before this run (baryons only): a galaxy ON the nu_mono law at scale s shows V^4/(G M_b) = a0 s * y_s nu(y_s)^2
            kf = {lab_: float(np.median((lambda ys: ys * C.nuv(NU, ys) ** 2)(dd["gb"][ix] / (A0C * s_)))) for lab_, s_ in (("s=1", 1.0), ("s=1.282", SREF))}
            BT[nm] = dict(n=n, median=med, q=q, sd_log=float(np.std(np.log10(mb))), dex_canonical=math.log10(med / A0C), dex_alt=math.log10(med / A0A),
                          q_dex_canonical=[math.log10(v / A0C) for v in q], q_dex_alt=[math.log10(v / A0A) for v in q], recipe=rows, recipe_half=hb, y_med=float(np.median(dd["y"][ix])), kernel_factor=kf)
            P(f"  {nm}: N {n} (median y {BT[nm]['y_med']:.3f}); median {med:.4e} m/s^2; 68 % [{q[1]:.4e}, {q[2]:.4e}], 95 % [{q[0]:.4e}, {q[3]:.4e}]; "
              f"vs canonical 9.3603e-11: {BT[nm]['dex_canonical']:+.3f} dex (68 % [{BT[nm]['q_dex_canonical'][1]:+.3f}, {BT[nm]['q_dex_canonical'][2]:+.3f}]); "
              f"vs alt 1.1312e-10: {BT[nm]['dex_alt']:+.3f} dex (68 % [{BT[nm]['q_dex_alt'][1]:+.3f}, {BT[nm]['q_dex_alt'][2]:+.3f}]); recipe half-width {hb:.3f} dex ("
              + "; ".join(f"{v['label']} {v['half']:.3f}" for v in rows.values()) + ")" + TAG)
            P(f"      diagnostic (baryons only, added after STAGE=CC2): kernel factor median(y nu_mono(y)^2) = {kf['s=1']:.3f} at a0 = 9.3603e-11 ({math.log10(kf['s=1']):+.3f} dex), {kf['s=1.282']:.3f} at the SPARC scale 1.20e-10 "
              f"({math.log10(kf['s=1.282']):+.3f} dex): a population on the nu_mono law at that a0 would show a BTFR median about this factor above a0; the SPARC BTFR level of the same recipe is {JC['numbers']['btfr_sparc']['median']:.3e} (STAGE=CC2)")
        P(f"  (with y on the alt footing the deep subset would hold {int(np.sum(dd['gb'] / A0A < 0.5))} galaxies; the frozen definition uses the canonical footing)")
        kii, kiii = "(ii) gas-dominated (M_gas > M*)", "(iii) deep (y < 0.5 at D_HI/2)"
        gd = (math.log10(BT[kii]["median"] / BT[kiii]["median"]) if ("median" in BT[kii] and "median" in BT[kiii]) else float("nan"))
        P(f"  gas-dominated minus deep: {gd:+.3f} dex")
        # ---------------- hand estimates
        P("\nHAND ESTIMATES (A3, frozen; HE1 was scored at stage A, HE4 at STAGE=CC2):")
        he = {"HE2": bool(1.1 <= s1 <= 1.7), "HE3": bool(abs(drift) <= 0.3), "HE5": bool("median" in BT[kiii] and 0.7e-10 <= BT[kiii]["median"] <= 2.0e-10), "HE6": bool(np.isfinite(gd) and abs(gd) <= 0.15)}
        P(f"    HE2: s*({w1k}) {s1:.4f} (estimate 1.4 +- 0.3): {'hit' if he['HE2'] else 'MISS (kept as it falls)'}")
        P(f"    HE3: |log10 s*(W3)/s*({w1k})| {abs(drift):.4f} (<= 0.3): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}")
        P(f"    HE5: deep-subset BTFR median {BT[kiii].get('median', float('nan')):.4e} (estimate 1.2e-10, plausible 0.7-2.0e-10): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6: gas-dominated minus deep {gd:+.4f} dex (within +-0.15): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        NUM.update(results=res, pooled=res["pooled"], recipe=REC, calibration=dict(cc1=cc1, cc2=cc2, cc3=cc3, cc4=cc4, calibrated=CAL, w1_key=w1k, offset_sparc=o_sp, offset_281=o_281, w1_recipe_half=h1, drift=drift),
                   trend=dict(DL_med=DLmed, slope=sl_pt, slope_q=pct(sl_b), slope_boot_median=float(np.median(sl_b)), slope_unmatched=slu_pt, slope_unmatched_q=pct(slu_b), rho=RHO, rival_lever_W1_W3=lev,
                              cfg281=dict(s_20_50=v281["V1 20-50 Mpc"]["s"], s_50_85=v281["V1 50-85 Mpc"]["s"], change=d281, rho_budhies=J281["rho"]["rho"])),
                   d4=dict(z_budhies=zB, DL_budhies=DB, lever=lev4, dlog_s=d4, q=pct(d4b)), btfr=BT, gas_minus_deep=gd, hand_estimates=he, matching={k: {kk: vv for kk, vv in v.items() if kk != 'members'} for k, v in PLANS.items()})


# ================================================================== STAGE M5: reproduce CFG281's committed s* from its arrays
if STAGE == "M5":
    P("\nSTAGE M5  this script's chain fed CFG281's ALFALFA arrays (its selection, its seeds, delta 9, sin 60 deg) against CFG281's committed s*")
    csv281 = os.path.join(REPO, "data_assembly", "alfalfa_sdss_local_control", "alfalfa_sdss.csv")
    cols = ["in_durbala2020", "in_a100_table2", "vhel_kms", "dist_mpc", "s21_jykms", "hi_code", "logmhi", "ba_r", "imag_abs_corr", "gi_corr", "logms_taylor", "w50_kms"]
    dA = pd.read_csv(csv281, usecols=cols)
    mA = dA.in_durbala2020.eq(1) & dA.in_a100_table2.eq(1) & dA.hi_code.eq(1) & (dA.logmhi >= math.log10(3e9)) & dA.dist_mpc.between(20.0, 85.0)
    mA &= dA[["gi_corr", "logms_taylor", "imag_abs_corr", "ba_r"]].notna().all(axis=1) & (dA.s21_jykms > 0) & (dA.s21_jykms < 900)
    L = dA[mA].reset_index(drop=True); nL = len(L); LMHI = L.logmhi.values.astype(float)
    aL = dict(mhi=10 ** LMHI, ms=10 ** L.logms_taylor.values.astype(float), z=(L.vhel_kms.values / CKMS).astype(float), sini=np.full(nL, SIN60))
    WL = L.w50_kms.values.astype(float); recL = dict(REC0, delta=9.0, sini=SIN60)
    ddL = chain(aL, WL, recL)
    src281 = open(os.path.join(CFG, "CFG281_budhies_local_control", "cfg281_local_control.py")).read()
    ns = {"np": np, "G": G, "MSUN": MSUN}; exec(compile(src281[src281.index("def chain_core"):src281.index("def derive_local")], "cfg281_local_control.py", "exec"), ns)
    Mg_ = 1.33 * aL["mhi"]; Mb_ = Mg_ + aL["ms"]; R_ = 0.5 * 10 ** (0.506 * np.log10(aL["mhi"]) - 3.293) * KPC
    D81, gb81, V81, ok81 = ns["chain_core"](WL, aL["z"], Mb_, R_, 9.0, 1, SIN60)
    dmax = float(np.nanmax(np.abs(np.log10(ddL["D"]) - np.log10(D81))))
    check("M5a CONTROL: this script's chain equals CFG281's committed chain_core (exec'd read-only) on CFG281's arrays", f"N {nL} (CFG281: 1,370); max |d log10 D| {dmax:.1e}", nL == 1370 and dmax < 1e-12)
    okL = np.isfinite(ddL["D"]); lU, uU = est1(ddL["D"][okL], ddL["gb"][okL])
    pc0 = C.select(C.load_galaxies(widths=False), "PC"); PCQ = np.percentile(np.log10([g["mhi"] for g in pc0]), [0, 25, 50, 75, 100])
    BINS = [np.where((LMHI >= PCQ[i]) & ((LMHI < PCQ[i + 1]) if i < 3 else (LMHI <= PCQ[i + 1])))[0] for i in range(4)]
    rI = np.random.default_rng(np.random.SeedSequence([281, 1]))
    IDX = np.concatenate([BINS[i][rI.integers(0, len(BINS[i]), size=(4000, 100))] for i in range(4)], axis=1)
    lC, uC = est(ddL["D"][IDX], ddL["gb"][IDX]); lCm = float(np.median(lC))
    dU = abs(lU - J281["LU"]["log_s"]); dC = abs(lCm - J281["LC"]["med"])
    check("M5b CONTROL: the unmatched CFG281 s* (LU) is reproduced to 1e-9 dex", f"mine {10 ** lU:.6f} (log10 {lU:+.10f}); CFG281 committed {J281['LU']['s']:.6f} (log10 {J281['LU']['log_s']:+.10f}); |d| {dU:.1e}", dU < 1e-9)
    check("M5c CONTROL: the matched CFG281 s* (LC, 4,000 stratified resamples, CFG281's seed) is reproduced to 1e-9 dex", f"mine {10 ** lCm:.6f} (log10 {lCm:+.10f}); CFG281 committed {J281['LC']['s']:.6f} (log10 {J281['LC']['med']:+.10f}); |d| {dC:.1e}", dC < 1e-9)
    NUM.update(n=nL, chain_max_dlogD=dmax, LU=dict(mine=10 ** lU, committed=J281["LU"]["s"], d=dU), LC=dict(mine=10 ** lCm, committed=J281["LC"]["s"], d=dC))


nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg301{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUT, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg301{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
