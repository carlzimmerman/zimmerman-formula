#!/usr/bin/env python3
"""D1_skew_preflight: power pre-flight for the n=1 vs n=2 occupancy-noise skew test.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 d1_skew_preflight.py [--mutate]
Criteria: FROZEN_CRITERIA.md (committed before this script).  Deterministic, no network.
--mutate replaces the corrected occupancy skew by K30's N_s = 1 value (the record's error);
the check that the corrected N(3 sigma) exceeds K30's by >= 50x must then FAIL.
"""
import os, sys, json, math, csv, io, contextlib
import numpy as np
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C                     # SPARC loader: rotmod files + SPARC_Lelli2016c.mrt

OUT, CHK, RES = [], [], {}
LN10 = math.log(10.0)
FOOT = {"canonical": 9.36e-11, "alt": 1.13e-10}          # BRIEF rule 3
WIN_GN = (0.10227, 0.5)                                  # A63 K20 window in g_N/a0
WIN_G = (0.375, 1.0)


def P(s=""):
    print(s); OUT.append(str(s))


def ck(name, ok, val, thr, note=""):
    CHK.append((name, bool(ok)))
    P(f"{name} {'PASS' if ok else 'FAIL'} {val:.6g} {thr} {note}")


# ---------------------------------------------------------------- the two laws (units a0 = 1; x = g/a0)
def law(n, x):
    """theta, capacity C, u'(g) for the record's n=1 (Langmuir) and n=2 (self-depleting) elements."""
    if n == 1:
        return x / (1 + x), 1.0, 1.0 / (1 + x) ** 2
    r = math.sqrt(x * x + 0.25)
    A = x + 0.5 - r
    return 2 * A, 0.5, 1 - x / r


def x_of_y(n, y):
    """total g/a0 from baryonic g_N/a0 for each law."""
    return (y + math.sqrt(y * y + 4 * y)) / 2 if n == 1 else math.sqrt(y * y + y)


def s_lin(n, x, ns):
    th, _, _ = law(n, x)
    return (1 - 2 * th) / math.sqrt(ns * th * (1 - th))


def sig_rel(n, x, ns):
    """sigma_g / g of the occupancy part (A2 eq. 18)."""
    th, Cc, up = law(n, x)
    return Cc * math.sqrt(th * (1 - th) / ns) / (1 - up) / x


def s_log_lo(n, x, ns):
    """leading-order skew of log g: s_lin - 3 sigma_rel (both ~ N_s^-1/2)."""
    return s_lin(n, x, ns) - 3 * sig_rel(n, x, ns)


def exact_binom(n, x, ns):
    """exact skew of g and of ln g for an integer-N binomial occupancy through the record's linear map."""
    th, Cc, up = law(n, x)
    k = np.arange(ns + 1)
    pmf = np.array([comb(ns, int(i)) for i in k], float) * th ** k * (1 - th) ** (ns - k)
    g = x + Cc * (k / ns - th) / (1 - up)
    ok = g > 0
    out = []
    for v in (g, np.log(np.where(ok, g, np.nan))):
        w = pmf[ok]; v = v[ok]; w = w / w.sum()
        m = np.sum(w * v); d = v - m
        out.append(float(np.sum(w * d ** 3) / np.sum(w * d ** 2) ** 1.5))
    return out


def skew(a):
    a = np.asarray(a, float); d = a - a.mean()
    return float(np.mean(d ** 3) / np.mean(d ** 2) ** 1.5)


def n3(s):
    return 54.0 / s ** 2 if s != 0 else float("inf")


# =========================================================================== T1: reproduce the record
P("== T1 reproduce the record (N_s = 1)")
s1h, s2h = s_lin(1, 0.5, 1), s_lin(2, 0.5, 1)
ck("K1", abs(s1h - 0.707107) < 1e-6 and abs(s2h + 0.3483107) < 1e-6, s1h, "0.707107/-0.3483107",
   f"n2={s2h:.7f} (a63_results.json value; report.md K18 row prints -0.348327)")
phi_a2 = 0.03 / math.sqrt(0.03 ** 2 + 0.06 ** 2)
k30_as_written = 54.0 / (0.70710678 * phi_a2 ** 3) ** 2
ck("K2", abs(k30_as_written - 13500) < 100, k30_as_written, "1.35e4", f"phi={phi_a2:.4f} (A63 K30 as written)")
RES["record"] = dict(s_n1_half_Ns1=s1h, s_n2_half_Ns1=s2h, K30_phi=phi_a2, K30_N3sigma=k30_as_written)

# =========================================================================== T2: point (a) dilution
P("== T2 point (a): A2 normalisation 0.03 dex at g=a0 fixes N_s; the skew then carries N_s^-1/2")
ns_a2 = {n: (sig_rel(n, 1.0, 1) / (0.03 * LN10)) ** 2 for n in (1, 2)}
ck("K3", abs(ns_a2[1] - 93.1) < 0.2, ns_a2[1], "93.1", f"(n=2 at same 0.03 dex: {ns_a2[2]:.1f})")
t2 = {}
for n in (1, 2):
    for lab, ns in (("own_Ns", ns_a2[n]), ("Ns93", ns_a2[1])):
        # (i) K30's construction with only s_true corrected (phi = 0.447 as written)
        s_corr = s_lin(n, 0.5, 1) / math.sqrt(ns)
        if MUT:
            s_corr = s_lin(n, 0.5, 1)                     # the record's N_s = 1 value
        N_fix_phi = n3(s_corr * phi_a2 ** 3)
        # (ii) self-consistent: sigma_occ at g=a0/2 from the same N_s, 0.06 dex background, linear and log
        so = sig_rel(n, 0.5, ns) / LN10
        ph = so / math.sqrt(so ** 2 + 0.06 ** 2)
        s_obs_lin = s_corr * ph ** 3
        s_obs_log = s_log_lo(n, 0.5, ns) * ph ** 3
        t2[f"n{n}_{lab}"] = dict(N_s=ns, s_true_lin=s_corr, N3_phi0447=N_fix_phi, ratio_vs_K30=N_fix_phi / k30_as_written,
                                 sigma_occ_dex_half=so, phi_selfconsistent=ph, s_obs_lin=s_obs_lin, s_obs_log=s_obs_log,
                                 N3_lin_selfconsistent=n3(s_obs_lin), N3_log_selfconsistent=n3(s_obs_log))
        P(f"  n={n} {lab:6s} N_s={ns:7.1f} s_true={s_corr:+.4f} N3(phi=.447)={N_fix_phi:.3g} (x{N_fix_phi/k30_as_written:.0f} K30)"
          f" | self-consistent sigma_occ(a0/2)={so:.4f} dex phi={ph:.3f} s_obs lin {s_obs_lin:+.4f} log {s_obs_log:+.4f}"
          f" N3 lin {n3(s_obs_lin):.3g} log {n3(s_obs_log):.3g}")
r1 = t2["n1_own_Ns"]["ratio_vs_K30"]
ck("K4", r1 >= 50, r1, ">=50", "corrected N(3sigma)/K30 for n=1 at A2's N_s (mutate: N_s=1 -> ratio 1)")
err_a = abs(0.70710678 - s_lin(1, 0.5, 1) / math.sqrt(ns_a2[1])) / (s_lin(1, 0.5, 1) / math.sqrt(ns_a2[1]))
RES["T2_dilution"] = dict(N_s_A2=ns_a2, cases=t2, K30_relative_error_in_s_true=err_a,
                          error_in_record=bool(err_a > 0.10))
P(f"  K30 s_true vs the N_s=93 skew it is paired with: relative error {err_a:.2f} -> error in record: {err_a > 0.10}")

# =========================================================================== T3: point (b) log transform
P("== T3 point (b): occupancy skew in g vs in log g, window g/a0 in (0.375,1)")
xs = np.exp(np.linspace(math.log(0.30), math.log(1.5), 241))
signmap = {}
for n in (1, 2):
    lin = np.array([s_lin(n, x, 1) for x in xs]); lg = np.array([s_log_lo(n, x, 1) for x in xs])
    # flip points (sign changes) of the log-space skew
    flips = [float(xs[i]) for i in range(len(xs) - 1) if np.sign(lg[i]) != np.sign(lg[i + 1])]
    signmap[n] = dict(lin=lin, log=lg, log_flips_g_over_a0=flips)
inw = (xs > WIN_G[0]) & (xs < WIN_G[1])
lin_opp = bool(np.all(np.sign(signmap[1]["lin"][inw]) != np.sign(signmap[2]["lin"][inw])))
log_opp_frac = float(np.mean(np.sign(signmap[1]["log"][inw]) != np.sign(signmap[2]["log"][inw])))
for x in (0.375, 0.5, 0.75, 1.0):
    P(f"  g/a0={x:5.3f}  sqrt(N_s)*skew: n1 lin {s_lin(1,x,1):+.4f} log {s_log_lo(1,x,1):+.4f} | "
      f"n2 lin {s_lin(2,x,1):+.4f} log {s_log_lo(2,x,1):+.4f}")
P(f"  linear: opposite signs on the whole window: {lin_opp};  log: fraction of window with opposite signs {log_opp_frac:.3f}")
P(f"  log-space flips: n1 at g/a0={signmap[1]['log_flips_g_over_a0']}, n2 at {signmap[2]['log_flips_g_over_a0']}")
# exact binomial at N_s = 93 vs leading order
devs, signs_ok = [], True
for n in (1, 2):
    for x in (0.4, 0.5, 0.75, 0.95):
        el, eg = exact_binom(n, x, 93)
        devs.append(abs(el - s_lin(n, x, 93)) / max(abs(s_lin(n, x, 93)), 1e-3))
        signs_ok &= bool(np.sign(eg) == np.sign(s_log_lo(n, x, 93)) and np.sign(el) == np.sign(s_lin(n, x, 93)))
        P(f"  exact N_s=93 n={n} g/a0={x:.2f}: lin {el:+.4f} (LO {s_lin(n,x,93):+.4f})  log {eg:+.4f} (LO {s_log_lo(n,x,93):+.4f})")
ck("K5", max(devs) < 0.01 and signs_ok, max(devs), "<0.01", "exact binomial vs leading order: linear skew rel. dev; log-skew signs agree at all 8 probes (log magnitudes differ up to 28% at g=0.4a0)")
ck("K6", lin_opp, float(lin_opp), "True", "record's linear-g statement (opposite signs on whole window) reproduces")
# lognormal background: analytic linear skew vs MC
rng = np.random.default_rng(22)
sd = 0.06
mc = skew(10 ** rng.normal(0, sd, 400000))
an = (math.exp((sd * LN10) ** 2) + 2) * math.sqrt(math.exp((sd * LN10) ** 2) - 1)
ck("K7", abs(mc - an) < 0.02, mc, f"{an:.4f}", "linear-g skew of a log-symmetric 0.06 dex background (MC vs analytic)")
RES["T3_log_transform"] = dict(
    table={f"{x}": dict(n1_lin=s_lin(1, x, 1), n1_log=s_log_lo(1, x, 1), n2_lin=s_lin(2, x, 1), n2_log=s_log_lo(2, x, 1))
           for x in (0.375, 0.5, 0.75, 1.0)},
    note="values are sqrt(N_s) * skew of the occupancy part alone (leading order)",
    linear_opposite_whole_window=lin_opp, log_opposite_fraction_of_window=log_opp_frac,
    log_flips=dict(n1=signmap[1]["log_flips_g_over_a0"], n2=signmap[2]["log_flips_g_over_a0"]),
    lognormal_bg_linear_skew_006dex=an, lognormal_bg_linear_skew_MC=mc)

# =========================================================================== SPARC: floor, N, N_eff, best case
P("== SPARC (rotmod + SPARC_Lelli2016c.mrt, Q<=2, Ups 0.5/0.7): systematic floor and best-case signal")
KPC = 3.0857e19
gal = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]
rows = []
for gi, g in enumerate(gal):
    R = g["R"] * KPC
    gb = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2) * 1e6 / R
    go = (g["Vobs"] * 1e3) ** 2 / R
    em = 2 * np.clip(g["eV"], 0, None) / np.clip(g["Vobs"], 1, None) / LN10
    for a, b, e in zip(go, gb, em):
        if a > 0 and b > 0:
            rows.append((gi, math.log10(a), math.log10(b), e))
rows = np.array(rows)
GI, LO, LB, EM = rows[:, 0].astype(int), rows[:, 1], rows[:, 2], rows[:, 3]
ck("K8", len(gal) >= 140 and len(rows) > 2500, len(rows), ">2500", f"points, {len(gal)} Q<=2 galaxies")


def resid(sel_bins, a0, linear):
    """residuals demeaned within 0.1 dex bins of log g_bar (law-free)."""
    y = LB - math.log10(a0)
    edges = np.arange(-1.5, 1.5001, 0.1)
    r = np.full(len(LO), np.nan); b_id = np.full(len(LO), -1)
    for k in range(len(edges) - 1):
        m = (y >= edges[k]) & (y < edges[k + 1])
        if m.sum() < 5:
            continue
        v = 10 ** LO[m] if linear else LO[m]
        r[m] = v / v.mean() - 1 if linear else v - v.mean()
        b_id[m] = k
    return r, b_id, y


def gal_demean(r, mask):
    out = r.copy()
    for gi in np.unique(GI[mask]):
        m = mask & (GI == gi)
        out[m] = r[m] - r[m].mean() if m.sum() > 1 else np.nan
    return out


sp = {}
for foot, a0 in FOOT.items():
    d = {}
    yN = LB - math.log10(a0)
    win = (yN > math.log10(WIN_GN[0])) & (yN < math.log10(WIN_GN[1]))
    out_ = ~win & (np.abs(yN) < 1.5)
    d["N_window"] = int(win.sum()); d["galaxies_window"] = int(len(np.unique(GI[win])))
    d["median_meas_err_dex_window"] = float(np.median(EM[win]))
    for var in ("log", "lin"):
        r, bid, _ = resid(None, a0, var == "lin")
        ok = ~np.isnan(r)
        w, o = win & ok, out_ & ok
        s_win, s_out = skew(r[w]), skew(r[o])
        rg = gal_demean(r, w); rgo = gal_demean(r, o)
        s_win_gd = skew(rg[~np.isnan(rg)]); s_out_gd = skew(rgo[~np.isnan(rgo)])
        # per-bin skews outside the window
        pb = [skew(r[o & (bid == k)]) for k in np.unique(bid[o]) if (o & (bid == k)).sum() >= 30]
        # bootstrap over galaxies of the window skew
        gids = np.unique(GI[w]); rb = np.random.default_rng(22); bs = []
        idx_by = {gg: np.where(w & (GI == gg))[0] for gg in gids}
        for _ in range(2000):
            pick = rb.choice(gids, len(gids))
            bs.append(skew(r[np.concatenate([idx_by[p] for p in pick])]))
        se_b = float(np.std(bs)); se_g = math.sqrt(6.0 / w.sum()); D = (se_b / se_g) ** 2
        sig_tot = float(np.std(r[w]))
        d[var] = dict(window_skew_DIAGNOSTIC_NOT_A_TEST=s_win, out_window_skew=s_out, window_skew_galaxy_demeaned=s_win_gd,
                      out_window_skew_galaxy_demeaned=s_out_gd, out_window_perbin_skews=pb,
                      SE_boot_window=se_b, SE_gauss_window=se_g, design_effect=D, N_eff=float(w.sum() / D),
                      sigma_tot=sig_tot, s_floor=abs(s_out))
        P(f"  {foot:9s} {var}: N_win={w.sum()} gal={len(gids)} | floor |skew_out|={abs(s_out):.3f} "
          f"(gal-demeaned out {s_out_gd:+.3f}; per-bin out {min(pb):+.2f}..{max(pb):+.2f}) | SE_boot {se_b:.3f} vs "
          f"SE_gauss {se_g:.3f} D={D:.1f} N_eff={w.sum()/D:.0f} | DIAGNOSTIC window skew {s_win:+.3f} "
          f"(gal-demeaned {s_win_gd:+.3f}) [NOT a test of n]")
    # best case: all intrinsic log scatter in the window is occupancy; background = measurement only
    st = d["log"]["sigma_tot"]; sm = float(np.sqrt(np.mean(EM[win] ** 2)))
    sint = math.sqrt(max(st ** 2 - sm ** 2, 1e-6)); phi = sint / st
    best = {}
    for n in (1, 2):
        sl, sg, nsl = [], [], []
        for y in 10 ** yN[win]:
            x = x_of_y(n, y)
            ns = max((sig_rel(n, x, 1) / (sint * LN10)) ** 2, 1.0)
            # sigma_occ in dex equals sint (unless N_s clamped at 1); phi from data
            sl.append(s_lin(n, x, ns) * phi ** 3); sg.append(s_log_lo(n, x, ns) * phi ** 3); nsl.append(ns)
        best[f"n{n}"] = dict(N_s_median=float(np.median(nsl)), s_obs_lin_mean=float(np.mean(sl)),
                             s_obs_log_mean=float(np.mean(sg)), N3_lin=n3(float(np.mean(sl))),
                             N3_log=n3(float(np.mean(sg))))
    sep_lin = best["n1"]["s_obs_lin_mean"] - best["n2"]["s_obs_lin_mean"]
    sep_log = best["n1"]["s_obs_log_mean"] - best["n2"]["s_obs_log_mean"]
    d["best_case"] = dict(sigma_tot_dex=st, sigma_meas_dex=sm, sigma_int_dex=sint, phi_max=phi, **best,
                          sep_lin=sep_lin, sep_log=sep_log, N3_sep_lin=n3(sep_lin), N3_sep_log=n3(sep_log),
                          N3_sep_lin_eff=n3(sep_lin) * d["lin"]["design_effect"],
                          N3_sep_log_eff=n3(sep_log) * d["log"]["design_effect"])
    P(f"  {foot:9s} best case: sigma_tot {st:.3f} meas {sm:.3f} int {sint:.3f} dex phi_max {phi:.3f} | "
      f"n1 N_s~{best['n1']['N_s_median']:.0f} s_obs lin {best['n1']['s_obs_lin_mean']:+.4f} log {best['n1']['s_obs_log_mean']:+.4f} | "
      f"n2 N_s~{best['n2']['N_s_median']:.0f} s_obs lin {best['n2']['s_obs_lin_mean']:+.4f} log {best['n2']['s_obs_log_mean']:+.4f}")
    P(f"  {foot:9s} N(3sigma) to separate: lin {n3(sep_lin):.3g} (eff x D -> {d['best_case']['N3_sep_lin_eff']:.3g}); "
      f"log {n3(sep_log):.3g} (eff -> {d['best_case']['N3_sep_log_eff']:.3g}); available N_eff lin {d['lin']['N_eff']:.0f}, log {d['log']['N_eff']:.0f}")
    sp[foot] = d
ck("K9", all(sp[f][v]["design_effect"] > 0 for f in FOOT for v in ("log", "lin")), sp["canonical"]["log"]["design_effect"],
   ">0", "bootstrap design effects computed")
RES["SPARC"] = sp

# =========================================================================== other data on disk (inventory)
P("== other data on disk")
inv = {}
# LITTLE THINGS: V_bar^2 = V_tot^2 - V_DM^2 per matched radius (authors' M/L), both curves unscaled
lt = {}
for fn in ("rotdmbar.dat", "rotdm.dat"):
    for line in open(os.path.join(EXT, "little_things_oh2015", fn)):
        t = line.split()
        if len(t) == 7 and t[1] == "Data":
            lt.setdefault((fn, t[0]), []).append([float(v) for v in t[2:]])
ltp = []
for (fn, name), arr in lt.items():
    if fn != "rotdmbar.dat" or ("rotdm.dat", name) not in lt:
        continue
    a = np.array(arr); b = np.array(lt[("rotdm.dat", name)])
    m = min(len(a), len(b))
    Rk = a[:m, 0] * a[:m, 2]; Vt = a[:m, 1] * a[:m, 3]; Vd = b[:m, 1] * b[:m, 3]; eV = a[:m, 1] * a[:m, 4]
    ok = np.abs(Rk - b[:m, 0] * b[:m, 2]) < 0.02 * Rk + 0.01
    for R_, vt, vd, ev in zip(Rk[ok], Vt[ok], Vd[ok], eV[ok]):
        vb2 = vt ** 2 - vd ** 2
        if vb2 > 0 and R_ > 0:
            ltp.append((name, math.log10(vt ** 2 * 1e6 / (R_ * KPC)), math.log10(vb2 * 1e6 / (R_ * KPC)), 2 * ev / vt / LN10))
lt_inv = dict(point_level=True, per_point_baryons="yes (authors' V_tot^2 - V_DM^2, their M/L)", N_points=len(ltp))
for foot, a0 in FOOT.items():
    yy = np.array([p[2] for p in ltp]) - math.log10(a0)
    w = (yy > math.log10(WIN_GN[0])) & (yy < math.log10(WIN_GN[1]))
    lt_inv[foot] = dict(N_window=int(w.sum()), galaxies_window=len({ltp[i][0] for i in np.where(w)[0]}),
                        median_err_dex=float(np.median([ltp[i][3] for i in np.where(w)[0]])) if w.any() else None)
inv["LITTLE_THINGS_Oh2015"] = lt_inv
P(f"  LITTLE THINGS: {len(ltp)} matched points; window canonical {lt_inv['canonical']}, alt {lt_inv['alt']}")
# WALLABY DR2 kinematic catalogue: rotation curves, HI surface density, no stellar profile
wn, wp = 0, 0
with open(os.path.join(EXT, "wallaby_dr2", "wallaby_dr2_kinematic_catalogue.csv")) as f:
    for row in csv.DictReader(f):
        if row.get("Vrot_model"):
            wn += 1; wp += len(row["Vrot_model"].split(","))
inv["WALLABY_DR2"] = dict(point_level=True, per_point_baryons="no: HI surface density per ring but no resolved stellar profile "
                          "(only AllWISE integrated W1); g_bar per point needs an assumed stellar profile + M/L",
                          galaxies=wn, points=wp, note="30 arcsec beams: few beams per curve, ring points strongly correlated")
P(f"  WALLABY DR2: {wn} kinematic models, {wp} ring points, no per-point stellar baryons")
dt = [l.split("\t") for l in open(os.path.join(REPO, "real_research/data/diteodoro2023_hi_rotation_curves.tsv")) if
      not l.startswith("#") and not l.startswith("name")]
inv["DiTeodoro2023"] = dict(point_level=True, per_point_baryons="no (masses only in the companion table)",
                            galaxies=len({r[0] for r in dt}), points=len(dt),
                            median_err_dex=float(np.median([2 * float(r[3]) / float(r[2]) / LN10 for r in dt])),
                            note="15 massive spirals; mostly g_N >~ a0, outside the window")
P(f"  Di Teodoro 2023: {len(dt)} points, {inv['DiTeodoro2023']['galaxies']} galaxies, no per-point baryons")
mq = [l for l in open(os.path.join(REPO, "real_research/data/faint_rotators_mcquinn2022/apjac9285t2_mrt.txt"))
      if l[:3] in ("AGC", "DDO", "UGC", "Leo", "Sex", "And", "WLM") or l.startswith("AGC")]
inv["McQuinn2022_faint_rotators"] = dict(point_level=False, note="one velocity at one radius per galaxy", galaxies=len(mq))
inv["MIGHTEE_HI"] = dict(point_level=False, note="catalogue (integrated widths) + DR1 cubes; no rotation curves or per-point baryons on disk")
inv["KiDS_lensing_RAR"] = dict(point_level=False, note="stacked excess surface density; stacking averages the per-galaxy "
                                "occupancy noise; not a per-point g_N-conditioned residual; different regime")
inv["SPARC"] = {f: dict(N_window=sp[f]["N_window"], galaxies_window=sp[f]["galaxies_window"],
                        median_err_dex=sp[f]["median_meas_err_dex_window"]) for f in FOOT}
RES["inventory"] = inv
ck("K10", len(ltp) > 300 and wn > 100, len(ltp), ">300", "LITTLE THINGS matched points; WALLABY models counted")

# =========================================================================== verdict (frozen lines)
P("== verdict (FROZEN_CRITERIA lines)")
vd = {}
for foot in FOOT:
    bc = sp[foot]["best_case"]
    # variable where signs differ: linear (record), unless log also differs
    for var in ("lin", "log"):
        s1, s2 = bc["n1"][f"s_obs_{var}_mean"], bc["n2"][f"s_obs_{var}_mean"]
        signs_differ = np.sign(s1) != np.sign(s2)
        floor = sp[foot][var]["s_floor"]; se3 = 3 * sp[foot][var]["SE_boot_window"]
        runnable = signs_differ and min(abs(s1), abs(s2)) > max(floor, se3)
        need = bc[f"N3_sep_{var}_eff"]
        gated = signs_differ and min(abs(s1), abs(s2)) > floor and need <= 1e6
        vd[f"{foot}_{var}"] = dict(signs_differ=bool(signs_differ), min_abs_s_obs=min(abs(s1), abs(s2)), s_floor=floor,
                                   three_SE_boot=se3, N_eff_required=need, N_eff_available=sp[foot][var]["N_eff"],
                                   runnable=bool(runnable), data_gated=bool(gated and not runnable))
        P(f"  {foot:9s} {var}: signs differ {signs_differ}; min|s_obs| {min(abs(s1),abs(s2)):.4f} vs floor {floor:.3f}, "
          f"3SE {se3:.3f}; N_eff need {need:.3g} have {sp[foot][var]['N_eff']:.0f}")
if all(vd[f"{f}_lin"]["runnable"] or vd[f"{f}_log"]["runnable"] for f in FOOT):
    verdict = "RUNNABLE NOW"
elif all(vd[f"{f}_lin"]["data_gated"] or vd[f"{f}_log"]["data_gated"] or vd[f"{f}_lin"]["runnable"]
         or vd[f"{f}_log"]["runnable"] for f in FOOT):
    verdict = "DATA-GATED"
else:
    verdict = "SCOPED NO-GO"
RES["verdict"] = dict(lines=vd, verdict=verdict)
P(f"  VERDICT: {verdict}")

npass = sum(ok for _, ok in CHK)
P(f"D1 COMPLETE: {npass}/{len(CHK)} checks PASS.")
RES["checks"] = {k: v for k, v in CHK}


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    if isinstance(o, float) and (math.isinf(o) or math.isnan(o)):
        return str(o)
    return o


json.dump(clean(RES), open(os.path.join(HERE, f"d1_skew_preflight_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"d1_skew_preflight{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
