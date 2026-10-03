#!/usr/bin/env python3
"""CFG303 R1 + R2 -- RC100 and CRISTAL with the LCDM-MODEL inputs (f_DM and the joint-fit baryon masses) replaced by framework-native ones,
re-run through each lane's OWN committed estimator (CFG223 implied-a0 points, CFG216 within-sample slopes, CFG213's Z5 bin, MNRAS v3.1 S5 inversion).
Frozen criteria: FROZEN_CRITERIA.md (52976ec22) + FROZEN_CRITERIA_ADDENDUM_1.md, written before any replaced input was evaluated.
kappa = 1/2 FITTED.  The cold mass is still required; no dark-matter particle is added.  No sentence here says the data favour a law.
Native g_bar = M_bar,nat x disc_v2(1, R_e, R) / R  (CFG216's committed thin exponential disc, R_e = 1.678 R_d); g_obs kept (MODEL-OTHER, halo_in_fit = yes).
Run (from a git-archive mirror or the repo):  python3 campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_rc100_cristal_LCDMFREE.py
Outputs (this lane only): cfg303_rc100_cristal_LCDMFREE.out, cfg303_rc100_cristal_LCDMFREE_results.json, cfg303_rc100_pergalaxy_LCDMFREE.csv,
cfg303_cristal_pergalaxy_LCDMFREE.csv.  No committed output of any lane is written.
"""
import os, sys, io, csv, json, math, contextlib, tempfile, time, hashlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

T0 = time.time()
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
os.environ.pop("MUTATE", None)                       # the exec'd lanes must run in their committed (unmutated) mode
OUT, CHK = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def exec_upto(path, stop, env=None, start=None):
    """exec the committed source text of `path` from `start` (or the top) up to the unique marker `stop`; returns (namespace, source)."""
    src = open(path).read()
    assert src.count(stop) == 1, (path, stop, src.count(stop))
    i0 = 0 if start is None else src.index(start)
    saved = {}
    for k, v in (env or {}).items():
        saved[k] = os.environ.get(k); os.environ[k] = v
    ns = {"__file__": path, "__name__": "cfg303_exec"}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[i0:src.index(stop)], os.path.relpath(path, REPO), "exec"), ns)
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return ns, src


def block(src, a, b):
    assert src.count(a) == 1 and src.count(b) == 1, (a, b)
    return src[src.index(a):src.index(b)]


def run_block(ns, code, label):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, label, "exec"), ns)


P(__doc__.split("Run (")[0].strip())
P("")
P("Frozen files (sha256 at run time):")
for f in ("FROZEN_CRITERIA.md", "FROZEN_CRITERIA_ADDENDUM_1.md", "rc100_table3_cols5to8_transcribed.csv"):
    P(f"  {f}: {sha(os.path.join(LANE, f))}")

# ================================================================================================================ committed machinery
P("\nLOADING THE COMMITTED ESTIMATORS (exec of committed source text up to fixed markers)")
F223 = os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")
F216 = os.path.join(CFG, "CFG216_rc100_within_sample", "cfg216_rc100.py")
F217 = os.path.join(CFG, "CFG217_rc100_attack", "cfg217_attack.py")
F213 = os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided.py")
FPN = os.path.join(REPO, "qwen_claude_field_theory", "papers_2026", "mnras_submission_2026_v3", "paper_numbers.py")
ns223, src223 = exec_upto(F223, 'P("\\nCONTROLS")')
ns216, src216 = exec_upto(F216, "# expected slopes if each hypothesis were exactly true", env={"RC100_INPUT": "corrected"})
ns217, _ = exec_upto(F217, "# ------------------------------------------------------------------------------------------------ data (CFG216's sample)")
ns213, src213 = exec_upto(F213, "# ------------------------------------------------------------------------------------------------ reported extras")
srcPN = open(FPN).read()
nsPN = {"__file__": FPN, "__name__": "cfg303_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(srcPN[:srcPN.index('head("S2  ')], "paper_numbers.py[header+S1]", "exec"), nsPN)
    exec(compile(block(srcPN, 'head("S4  THE REDSHIFT LAWS', "g0, r0, c0_ = gmax_nfw("), "paper_numbers.py[S4 defs]", "exec"), nsPN)
    exec(compile(block(srcPN, "import csv\ndef rc100_run", "R5 = rc100_run(RC100)"), "paper_numbers.py[S5 rc100_run]", "exec"), nsPN)
P(f"  CFG223 (sha {sha(F223)[:12]}), CFG216 (sha {sha(F216)[:12]}), CFG217 mu_t18 (sha {sha(F217)[:12]}), CFG213 (sha {sha(F213)[:12]}), paper_numbers.py (sha {sha(FPN)[:12]}): loaded")

K = ns223["K"]
G2SI, G_KPC = ns216["G2SI"], ns216["G_KPC"]
disc_v2 = ns216["disc_v2"]                   # CFG216's committed thin exponential disc (XN = 1.678)
mu_t18 = ns217["mu_t18"]                     # CFG217's committed gas-fraction function (Tacconi-type; delta_MS not used)
A0L, NU = ns223["A0L"], ns223["NU"]
analyse, expectations, bands, flags_fn = ns223["analyse"], ns223["expectations"], ns223["bands"], ns223["flags"]
implied, LAWS223 = ns223["implied"], ns223["LAWS"]
J223 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))
C223 = {p["label"]: p for p in J223["points"]}
EDGES = np.array(J223["edges"])


def xi(Re, R):
    """g_bar per unit baryon mass [m s^-2 / Msun] at radius R for CFG216's thin exponential disc of effective radius Re."""
    return disc_v2(1.0, Re, R) / R * G2SI


def point(label, z, gb, go):
    z, gb, go = (np.asarray(v, float) for v in (z, gb, go))
    return dict(label=label, z=z, gb=gb, go=go, D=go / gb)


def point_D(label, z, gb, D):
    z, gb, D = (np.asarray(v, float) for v in (z, gb, D))
    return dict(label=label, z=z, gb=gb, D=D, go=gb * D)


def summarise(p):
    r, lb, I = analyse(p)
    r["expected"] = expectations(p, r["log_s"], lb, I)
    bd, nr = bands(p)
    r["bands"] = {str(k): v for k, v in bd.items()}; r["band_noroot"] = {str(k): v for k, v in nr.items()}
    r["flags"] = flags_fn(r, bd)
    r["a0_implied_1e-10"] = r["s"] * A0L / 1e-10
    y = p["gb"] / A0L
    r["y_quartiles"] = [float(v) for v in np.percentile(y, [25, 50, 75])]
    r["n_D_le_1"] = int((p["D"] <= 1).sum())
    r["label"] = p["label"]
    return r


def same_as_committed(r, c, tol=1e-9):
    d = max(abs(r["log_s"] - c["log_s"]), *(abs(math.log10(r[k]) - math.log10(c[k])) for k in ("lo95", "lo68", "hi68", "hi95")))
    d = max(d, *(abs(math.log10(r["expected"][L]["s"]) - math.log10(c["expected"][L]["s"])) for L in c["expected"]))
    d = max(d, *(abs(r["expected"][L]["pull"] - c["expected"][L]["pull"]) for L in c["expected"]))
    d = max(d, *(abs(math.log10(r["bands"][k]) - math.log10(c["bands"][k])) for k in c["bands"]))
    return d, d <= tol


def line(r):
    e = r["expected"]
    return (f"s* {r['s']:.3f} (a0 {r['a0_implied_1e-10']:.2f}e-10) 68% [{r['lo68']:.3f}, {r['hi68']:.3f}] 95% [{r['lo95']:.3f}, {r['hi95']:.3f}]"
            f"{' NO ROOT' if r['unbounded'] else ''} (no-root resamples {r['unb_frac']:.0%}); n {r['n']}, z_med {r['z_med']:.2f}; y quartiles "
            f"{r['y_quartiles'][0]:.2f}/{r['y_quartiles'][1]:.2f}/{r['y_quartiles'][2]:.2f}; D<=1: {r['n_D_le_1']}; pulls flat {e['FLAT']['pull']:+.2f} "
            f"proxy {e['PROXY']['pull']:+.2f} H(z) {e['H(z)']['pull']:+.2f}; +-0.15 dex band {r['bands']['-0.15']:.3f}{'(nr)' if r['band_noroot']['-0.15'] else ''}"
            f" to {r['bands']['0.15']:.3f}{'(nr)' if r['band_noroot']['0.15'] else ''}")


RES = dict(points={}, cfg216={}, s5={}, cfg213={}, controls={}, notes=[])

# ================================================================================================================ RC100 data
P("\nRC100 INPUTS")
rc_path = ns223["RC_PATH"]["corrected"]
rc = list(csv.DictReader(open(rc_path, newline="")))
tr = {r["idx"]: r for r in csv.DictReader(open(os.path.join(LANE, "rc100_table3_cols5to8_transcribed.csv"), newline=""))}
orig = {r["idx"]: r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"), newline=""))}
rc41 = {r["id"].replace("_", " "): r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "price2021_rc41", "price2021_rc41.csv"), newline=""))}
t1 = [r["idx"] for r in rc if abs(float(tr[r["idx"]]["logMbaryon"]) - float(r["logMbar_Msun"])) > 1e-9 or tr[r["idx"]]["name"] != r["name"]
      or abs(float(tr[r["idx"]]["z"]) - float(r["z"])) > 1e-9]
check("T1 transcribed column 7 (log M_baryon), name and z equal the corrected table in all 100 rows", f"{100 - len(t1)}/100 rows agree; mismatches {t1}", len(rc) == 100 and not t1)
B7 = ("58", "62", "63", "65", "77", "93", "95")
t2 = [i for i in B7 if abs(float(tr[i]["logMbulge"]) - float(orig[i]["logMbar_Msun"])) > 1e-9]
check("T2 transcribed column 8 (log M_bulge) equals the committed CSV's mistaken log M_baryon in rows 58, 62, 63, 65, 77, 93, 95", f"{7 - len(t2)}/7 agree; mismatches {t2}", not t2)
gal = []
for r in rc:
    z, Re, Vc, fd = (float(r[k]) for k in ("z", "Re_kpc", "Vc_Re_kms", "fDM_within_Re"))
    go = Vc ** 2 / Re * G2SI
    t = tr[r["idx"]]
    lms = float(t["logMstar"])
    Ms = 10 ** lms
    mu = mu_t18(z, lms)
    MB = Ms * (1 + mu)
    q = rc41.get(r["name"])
    MA = (10 ** float(q["logMstar_SED"]) + 10 ** float(q["logMgas"])) if q else float("nan")
    BT = float(q["BT"]) if q else float("nan")
    gal.append(dict(idx=r["idx"], name=r["name"], z=z, Re=Re, Vc=Vc, s0=float(r["sigma0_kms"]), fd=fd, go=go,
                    gb_lcdm=(1 - fd) * go, D_lcdm=1 / (1 - fd), lMfit=float(r["logMbar_Msun"]),
                    lMs=lms, mu=mu, MB=MB, gbB=MB * xi(Re, Re), inA=q is not None, MA=MA, BT=BT,
                    gbA=MA * xi(Re, Re) if q else float("nan"),
                    gbG2=(MA * ((1 - BT) * xi(Re, Re) + BT * G_KPC / Re ** 2 * G2SI)) if q else float("nan"),
                    lMs_price=float(q["logMstar_SED"]) if q else float("nan")))
A = [g for g in gal if g["inA"]]
dms = np.array([g["lMs"] - g["lMs_price"] for g in A])
P(f"  corrected table: {len(gal)} galaxies; RC41 overlap by name (sample A): {len(A)}")
check("T3 (reported) transcribed SED log M* against Price+21 SED log M* on the RC41 overlap", f"median {np.median(dms):+.3f} dex, median |diff| {np.median(np.abs(dms)):.3f} dex, "
      f"range [{dms.min():+.2f}, {dms.max():+.2f}], |diff| <= 0.15 for {int((np.abs(dms) <= 0.15).sum())}/{len(dms)}", True)
RES["controls"]["T3"] = dict(median=float(np.median(dms)), median_abs=float(np.median(np.abs(dms))), n=len(dms))
lB = np.array([math.log10(g["MB"]) for g in gal]); lF = np.array([g["lMfit"] for g in gal])
P(f"  sample B native log M_bar - joint-fit posterior log M_baryon: median {np.median(lB - lF):+.3f} dex (16-84% {np.percentile(lB - lF, 16):+.3f} to {np.percentile(lB - lF, 84):+.3f});"
  f" gas fraction mu median {np.median([g['mu'] for g in gal]):.2f}")
lA = np.array([math.log10(g["MA"]) for g in A]); lFA = np.array([g["lMfit"] for g in A])
P(f"  sample A native log M_bar - joint-fit posterior: median {np.median(lA - lFA):+.3f} dex (16-84% {np.percentile(lA - lFA, 16):+.3f} to {np.percentile(lA - lFA, 84):+.3f})")
xiF = np.array([g["gb_lcdm"] / 10 ** g["lMfit"] / xi(g["Re"], g["Re"]) for g in gal])
P(f"  diagnostic only (uses f_DM, not an input): the fit's own baryon geometry relative to CFG216's thin disc, (1 - f_DM) g_obs / [M_fit xi]: median {np.median(xiF):.3f} "
  f"(16-84% {np.percentile(xiF, 16):.3f}-{np.percentile(xiF, 84):.3f})")
RES["notes"].append(dict(dlogM_B_minus_fit=float(np.median(lB - lF)), dlogM_A_minus_fit=float(np.median(lA - lFA)), fit_geometry_over_thin_disc=float(np.median(xiF))))


def rc_mask(z, i):                          # CFG223 build_points' bin rule, verbatim logic
    lo, hi = EDGES[i], EDGES[i + 1]
    return (z >= lo) & ((z < hi) | ((i == 3) & (z <= hi)))


zall = np.array([g["z"] for g in gal])

# ================================================================================================================ C-ii(a): committed scripts reproduce themselves
P("\nC-ii(a): THE COMMITTED ESTIMATORS, RUN IN THIS PROCESS ON THEIR COMMITTED INPUTS, REPRODUCE THEIR COMMITTED NUMBERS")
J216 = json.load(open(os.path.join(CFG, "CFG216_rc100_within_sample", "cfg216_rc100_corrected_results.json")))["numbers"]
d216 = max(abs(ns216["RES"][tuple(k.split("|"))][kk] - v[kk]) for k, v in J216["results"].items() for kk in ("slope", "lo", "hi", "sd", "med", "mlo", "mhi"))
check("C-ii(a) CFG216 (corrected input) primary block re-executed: every slope, CI, sd and median equals cfg216_rc100_corrected_results.json", f"max |diff| {d216:.1e}", d216 <= 1e-9)
J213 = json.load(open(os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided_results.json")))["numbers"]
d213 = 0.0
for bname in ("Z1.4 (NOEMA3D)", "Z5 (CRISTAL primary)"):
    for k, v in J213[bname].items():
        a, rt, kn, ft, lw = k.split("|")
        mine = ns213["TABLE"][bname][(float(a), rt == "route", kn, ft, lw)]
        d213 = max(d213, *(abs(mine[q] - v[q]) for q in ("med", "lo", "hi")))
        d213 = max(d213, 0.0 if mine["v"] == v["v"] else 1.0)
check("C-ii(a) CFG213 BINS loop re-executed: every median, CI and verdict equals cfg213_two_sided_results.json", f"max |diff| {d213:.1e}", d213 <= 1e-9)
JPN = json.load(open(FPN.replace(".py", ".json")))["S5"]
s5c = nsPN["rc100_run"](nsPN["RC100"], verbose=False)
dpn = max(abs(s5c[k] - JPN[k]) / max(abs(JPN[k]), 1e-30) for k in ("slope", "slope_err", "median_a0", "median_y", "weakest_excl_Hz"))
check("C-ii(a) MNRAS S5 rc100_run on the corrected CSV equals paper_numbers.json S5 (slope, slope_err, median_a0, median_y, weakest_excl_Hz; relative)", f"max rel diff {dpn:.1e}; N {s5c['N']} vs {JPN['N']}",
      dpn <= 1e-12 and s5c["N"] == JPN["N"])

# ================================================================================================================ RC100 through CFG223
P("\nR1 / CFG223: RC100 IMPLIED-a0 POINTS (committed quartile edges " + ", ".join(f"{e:.4f}" for e in EDGES) + ")")
lab = lambda i: f"RC100 corrected, z quartile {i + 1} [{EDGES[i]:.2f}, {EDGES[i + 1]:.2f}]"
go_all = np.array([g["go"] for g in gal])
# C-i identity: the committed g_bar sent through the NATIVE formula (M_id = g_bar,committed / xi)
Mid = np.array([g["gb_lcdm"] / xi(g["Re"], g["Re"]) for g in gal])
gb_id = np.array([m * xi(g["Re"], g["Re"]) for m, g in zip(Mid, gal)])
worst_i, worst_ii = 0.0, 0.0
for i in range(4):
    m = rc_mask(zall, i)
    r_id = summarise(point(lab(i), zall[m], gb_id[m], go_all[m]))
    di, _ = same_as_committed(r_id, C223[lab(i)]); worst_i = max(worst_i, di)
    r_sw = summarise(point_D(lab(i), zall[m], np.array([g["gb_lcdm"] for g in gal])[m], np.array([g["D_lcdm"] for g in gal])[m]))
    dii, _ = same_as_committed(r_sw, C223[lab(i)]); worst_ii = max(worst_ii, dii)
check("C-i identity replacement: the committed g_bar passed through the native formula reproduces CFG223's four RC100 quartiles (s*, 68/95 edges, expected s*, pulls, bands)",
      f"max |diff| {worst_i:.1e} (log10 / pull units)", worst_i <= 1e-9)
check("C-ii(b) swap-back: the LCDM-MODEL input ((1 - f_DM) g_obs, D = 1/(1 - f_DM)) put back into the same per-galaxy structure reproduces CFG223's four RC100 quartiles",
      f"max |diff| {worst_ii:.1e}", worst_ii <= 1e-9)
gbB = np.array([g["gbB"] for g in gal])
nat = {}
for i in range(4):
    m = rc_mask(zall, i)
    nat[f"B Q{i + 1}"] = summarise(point(f"RC100 native B (SED M* col 6 + mu_t18 gas), Q{i + 1}", zall[m], gbB[m], go_all[m]))
nat["B pooled"] = summarise(point("RC100 native B, pooled (100)", zall, gbB, go_all))
mA = np.array([g["inA"] for g in gal])
gbA = np.array([g["gbA"] for g in gal]); gbG2 = np.array([g["gbG2"] for g in gal])
for i in range(4):
    m = rc_mask(zall, i) & mA
    nat[f"A Q{i + 1}"] = summarise(point(f"RC100 native A (Price+21 SED M* + gas), Q{i + 1}", zall[m], gbA[m], go_all[m]))
    nat[f"G2 Q{i + 1}"] = summarise(point(f"RC100 native A, G2 point-mass bulge, Q{i + 1}", zall[m], gbG2[m], go_all[m]))
nat["A pooled"] = summarise(point(f"RC100 native A, pooled ({int(mA.sum())})", zall[mA], gbA[mA], go_all[mA]))
nat["G2 pooled"] = summarise(point(f"RC100 native A, G2 point-mass bulge, pooled ({int(mA.sum())})", zall[mA], gbG2[mA], go_all[mA]))
# LCDM-route values on sample A (for a like-for-like old -> new on the same galaxies)
gbL = np.array([g["gb_lcdm"] for g in gal]); DL = np.array([g["D_lcdm"] for g in gal])
nat["A pooled, committed route"] = summarise(point_D(f"RC100 committed route (f_DM) on sample A, pooled", zall[mA], gbL[mA], DL[mA]))
nat["B pooled, committed route"] = summarise(point_D("RC100 committed route (f_DM), pooled (100)", zall, gbL, DL))
for i in range(4):
    c = C223[lab(i)]
    P(f"  Q{i + 1} committed (f_DM): s* {c['s']:.3f} 95% [{c['lo95']:.3f}, {c['hi95']:.3f}]; pulls flat {c['expected']['FLAT']['pull']:+.2f} H(z) {c['expected']['H(z)']['pull']:+.2f}")
    for s_ in ("B", "A", "G2"):
        P(f"     native {s_:2s}: " + line(nat[f"{s_} Q{i + 1}"]))
for k in ("B pooled", "B pooled, committed route", "A pooled", "A pooled, committed route", "G2 pooled"):
    P(f"  {k:28s}: " + line(nat[k]))
RES["points"]["RC100"] = nat

# ================================================================================================================ MUTATE (C-iii) on the native CFG223 points
P("\nC-iii MUTATE: M_bar,nat x 10^0.2 for every galaxy (native RC100 points)")


def med_delta(D, gb, s=1.0):
    return float(np.median(np.log10(D) - np.log10(K.nu_mono(gb / (A0L * s)))))


def brentq_s(D, gb):
    f = lambda ls: med_delta(D, gb, 10 ** ls)
    a, b = -3.0, 3.0
    if not (f(a) > 0 > f(b)):
        return None
    return brentq(f, a, b, xtol=1e-13, rtol=1e-13)


mut_ok, mut_rows = True, []
for key, mask, gbx in [(f"B Q{i + 1}", rc_mask(zall, i), gbB) for i in range(4)] + [("B pooled", np.ones(100, bool), gbB), ("A pooled", mA, gbA)]:
    D0, g0 = go_all[mask] / gbx[mask], gbx[mask]
    g1 = gbx[mask] * 10 ** 0.2; D1 = go_all[mask] / g1
    dD = np.log10(D1) - np.log10(D0); dg = np.log10(g1) - np.log10(g0)
    okD = np.allclose(dD, -0.2, atol=1e-12, rtol=0) and np.allclose(dg, 0.2, atol=1e-12, rtol=0)
    sh_ind = med_delta(D1, g1) - med_delta(D0, g0)
    sh_est = float(np.median(np.log10(D1) - np.log10(NU(g1 / A0L)))) - float(np.median(np.log10(D0) - np.log10(NU(g0 / A0L))))
    l0, u0 = implied(D0, g0, NU, A0L); l1, u1 = implied(D1, g1, NU, A0L)
    l0, u0, l1, u1 = float(l0[0]), bool(u0[0]), float(l1[0]), bool(u1[0])
    bq = brentq_s(D1, g1)
    agree = (bq is None and u1) or (bq is not None and abs(bq - l1) <= 1e-6)
    direction = (u0 and u1) or (l1 < l0) or (u1 and not u0)
    ok = okD and abs(sh_ind - sh_est) <= 1e-9 and agree and direction
    mut_ok &= ok
    mut_rows.append(dict(point=key, s0=10 ** l0, s1=None if u1 else 10 ** l1, noroot0=u0, noroot1=u1, median_delta_shift=sh_est, brentq=None if bq is None else 10 ** bq))
    P(f"  {key:9s}: log D shift -0.2 exact {okD}; median delta(s=1) shift {sh_est:+.4f} (independent {sh_ind:+.4f}); s* {10 ** l0:.3f}{' (no root)' if u0 else ''} -> "
      f"{'no root' if u1 else f'{10 ** l1:.3f}'}; brentq re-solve {'none' if bq is None else f'{10 ** bq:.3f}'}")
check("C-iii MUTATE (native RC100 points): every log D moves by -0.2000 and log g_bar by +0.2000 exactly, the median delta moves by the independently computed amount, "
      "s* moves down (or loses its root) and equals a scalar brentq re-solve to 1e-6", f"{len(mut_rows)} points", mut_ok)
RES["controls"]["mutate_rc100"] = mut_rows

# ================================================================================================================ RC100 through CFG216 (within-sample slopes)
P("\nR1 / CFG216: WITHIN-SAMPLE SLOPES OF delta ON z (CFG216's primary and expected-slope blocks re-executed on replaced rows)")
code_primary = block(src216, "# ------------------------------------------------------------------------------------------------ primary: slopes",
                     "# expected slopes if each hypothesis were exactly true")
src216_full = src216
code_exp = block(src216_full, "# expected slopes if each hypothesis were exactly true", "# level in z-halves")
committed_rows = ns216["rows"]
assert len(committed_rows) == 100 and [r["name"] for r in committed_rows] == [g["name"] for g in gal]


def cfg216_on(rows):
    ns216["rows"] = rows; ns216["z"] = np.array([r["z"] for r in rows])
    run_block(ns216, code_primary, "cfg216[primary]")
    run_block(ns216, code_exp, "cfg216[expected]")
    res = {"|".join(k): v for k, v in ns216["RES"].items()}
    exp = ns216["EXP"]
    zs = {law: {t: (res[f"nu_mono|canonical|{law}"]["slope"] - exp[t][law]) / res[f"nu_mono|canonical|{law}"]["sd"] for t in ("flat", "rival")} for law in ("flat", "rival")}
    return dict(results=res, expected=exp, z=zs, outcome=ns216["primary_outcome"], n=len(rows))


def rows216(gbcol, sel=None):
    out = []
    for g, gb in zip(gal, gbcol):
        if sel is not None and not sel(g):
            continue
        out.append(dict(name=g["name"], z=g["z"], Re=g["Re"], Vc=g["Vc"], fd=g["fd"], lm=g["lMfit"], gobs=g["go"], D=g["go"] / gb, gbar=gb))
    return out


c216_id = cfg216_on(rows216(gb_id))
did = max(abs(c216_id["results"][k][kk] - v[kk]) for k, v in J216["results"].items() for kk in ("slope", "lo", "hi", "sd", "med", "mlo", "mhi"))
check("C-i identity replacement (CFG216): the committed g_bar through the native formula reproduces every committed slope, CI, sd and median, and the outcome label",
      f"max |diff| {did:.1e}; outcome '{c216_id['outcome'].split(' ')[0]}' vs '{J216['outcome_primary'].split(' ')[0]}'", did <= 1e-9 and c216_id["outcome"] == J216["outcome_primary"])
c216_sw = cfg216_on([dict(r) for r in committed_rows])
dsw = max(abs(c216_sw["results"][k][kk] - v[kk]) for k, v in J216["results"].items() for kk in ("slope", "lo", "hi", "sd", "med", "mlo", "mhi"))
check("C-ii(b) swap-back (CFG216): the committed rows put back reproduce the committed numbers", f"max |diff| {dsw:.1e}", dsw <= 1e-9)
c216 = {"B": cfg216_on(rows216(gbB)), "A": cfg216_on(rows216(gbA, sel=lambda g: g["inA"])), "G2": cfg216_on(rows216(gbG2, sel=lambda g: g["inA"])),
        "A, committed route": cfg216_on([dict(r) for r in committed_rows if r["name"] in rc41])}
cB_mut = cfg216_on(rows216(gbB * 10 ** 0.2))
dDm = max(abs(math.log10(a["D"]) - math.log10(b["D"]) + 0.2) for a, b in zip(rows216(gbB * 10 ** 0.2), rows216(gbB)))
check("C-iii MUTATE (CFG216 sample B): every log D moves by -0.2000 exactly (slope shifts reported, not graded)", f"max |error| {dDm:.1e}; flat slope "
      f"{c216['B']['results']['nu_mono|canonical|flat']['slope']:+.4f} -> {cB_mut['results']['nu_mono|canonical|flat']['slope']:+.4f}, rival "
      f"{c216['B']['results']['nu_mono|canonical|rival']['slope']:+.4f} -> {cB_mut['results']['nu_mono|canonical|rival']['slope']:+.4f}", dDm <= 1e-12)
cc = J216["results"]
P(f"  committed (f_DM, n 100): flat slope {cc['nu_mono|canonical|flat']['slope']:+.3f} [{cc['nu_mono|canonical|flat']['lo']:+.3f}, {cc['nu_mono|canonical|flat']['hi']:+.3f}], "
  f"rival {cc['nu_mono|canonical|rival']['slope']:+.3f} [{cc['nu_mono|canonical|rival']['lo']:+.3f}, {cc['nu_mono|canonical|rival']['hi']:+.3f}]; outcome {J216['outcome_primary'].split(' ')[0]}")
for k, v in c216.items():
    f_, r_ = v["results"]["nu_mono|canonical|flat"], v["results"]["nu_mono|canonical|rival"]
    P(f"  {k:19s} (n {v['n']:3d}): flat median {f_['med']:+.3f} [{f_['mlo']:+.3f}, {f_['mhi']:+.3f}] slope {f_['slope']:+.3f} [{f_['lo']:+.3f}, {f_['hi']:+.3f}] "
      f"(z vs flat-true {v['z']['flat']['flat']:+.2f}, rival-true {v['z']['flat']['rival']:+.2f}); rival median {r_['med']:+.3f} slope {r_['slope']:+.3f} [{r_['lo']:+.3f}, {r_['hi']:+.3f}] "
      f"(z vs flat-true {v['z']['rival']['flat']:+.2f}, rival-true {v['z']['rival']['rival']:+.2f}); outcome {v['outcome'].split(' ')[0]}")
RES["cfg216"] = {k: dict(n=v["n"], outcome=v["outcome"], z=v["z"], expected=v["expected"],
                         primary={kk: v["results"][kk] for kk in ("nu_mono|canonical|flat", "nu_mono|canonical|rival")}, cells=v["results"]) for k, v in c216.items()}
RES["cfg216"]["B_MUTATE"] = dict(primary={kk: cB_mut["results"][kk] for kk in ("nu_mono|canonical|flat", "nu_mono|canonical|rival")})

# ================================================================================================================ RC100 through the MNRAS S5 inversion
P("\nR1 / MNRAS v3.1 S5: a0 = g_bar / [ln(1/f)]^2 with f = 1 - g_bar/g_obs (the paper's rc100_run, unchanged, fed through a temporary table)")
TMP = tempfile.mkdtemp(prefix="cfg303_")


def s5_table(name, gbcol, sel=None):
    path = os.path.join(TMP, name + ".csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["idx", "z", "fDM_within_Re", "g_Re_ms2", "Vc_Re_kms", "sigma0_kms"])
        rcd = {r["idx"]: r for r in csv.DictReader(open(nsPN["RC100"], newline=""))}
        for g, gb in zip(gal, gbcol):
            if sel is not None and not sel(g):
                continue
            r0 = rcd[g["idx"]]
            gobs = float(r0["g_Re_ms2"])
            fnat = repr(1 - gb / gobs) if gb is not None else r0["fDM_within_Re"]
            w.writerow([g["idx"], r0["z"], fnat, r0["g_Re_ms2"], r0["Vc_Re_kms"], r0["sigma0_kms"]])
    return path


gobsPN = {r["idx"]: float(r["g_Re_ms2"]) for r in csv.DictReader(open(nsPN["RC100"], newline=""))}
gV = max(abs(gobsPN[g["idx"]] / g["go"] - 1) for g in gal)
P(f"  the paper's g_Re_ms2 column against V_c^2/R_e: max relative difference {gV:.1e} (4 significant figures in the CSV)")
gb_id_pn = [(1 - g["fd"]) * gobsPN[g["idx"]] for g in gal]
s5_id = nsPN["rc100_run"](s5_table("identity", gb_id_pn), verbose=False)
did5 = max(abs(s5_id[k] - JPN[k]) / max(abs(JPN[k]), 1e-30) for k in ("slope", "slope_err", "median_a0", "median_y", "weakest_excl_Hz"))
check("C-i identity replacement (S5): f = 1 - g_bar/g_obs with the committed g_bar reproduces paper_numbers.json S5 (relative)", f"max rel diff {did5:.1e}; N {s5_id['N']}", did5 <= 1e-9 and s5_id["N"] == JPN["N"])
s5 = {}
for k, col, sel in (("B", [g["gbB"] for g in gal], None), ("A", [g["gbA"] for g in gal], lambda g: g["inA"]), ("G2", [g["gbG2"] for g in gal], lambda g: g["inA"])):
    s5[k] = nsPN["rc100_run"](s5_table(k, col, sel), verbose=False)
    n_in = sum(1 for g, gb in zip(gal, col) if (sel is None or sel(g)))
    s5[k]["n_input"] = n_in
s5_mut = nsPN["rc100_run"](s5_table("B_mut", [g["gbB"] * 10 ** 0.2 for g in gal]), verbose=False)
s5["B_MUTATE"] = s5_mut
P(f"  committed (f_DM): N {JPN['N']}, d log a0/dz {JPN['slope']:+.3f} +/- {JPN['slope_err']:.3f}, median a0 {JPN['median_a0']:.3e}, median y {JPN['median_y']:.2f}, "
  f"weakest exclusion of H(z) {JPN['weakest_excl_Hz']:.1f} sigma")
for k in ("B", "A", "G2", "B_MUTATE"):
    v = s5[k]
    P(f"  native {k:8s}: N {v['N']} of {v.get('n_input', 100)} (the rest outside the paper's f window (0.02, 0.98)), d log a0/dz {v['slope']:+.3f} +/- {v['slope_err']:.3f} "
      f"({v['slope'] / v['slope_err']:+.1f} sigma from 0), median a0 {v['median_a0']:.3e}, median y {v['median_y']:.2f}, matched-comparator distances: H(z) "
      f"{(v['slope_Hz_ols'] - v['slope']) / v['slope_err']:.1f} sigma, halo law {(v['slope_halo_ols'] - v['slope']) / v['slope_err']:.1f} sigma; weakest exclusion of H(z) {v['weakest_excl_Hz']:.1f}")
RES["s5"] = {k: {kk: v[kk] for kk in ("N", "slope", "slope_err", "median_a0", "median_y", "weakest_excl_Hz", "slope_Hz_ols", "slope_halo_ols", "a0_16_84", "n_below_gate")} | {"n_input": v.get("n_input", 100)}
             for k, v in s5.items()}
RES["s5"]["committed"] = {kk: JPN[kk] for kk in ("N", "slope", "slope_err", "median_a0", "median_y", "weakest_excl_Hz", "slope_Hz_ols", "slope_halo_ols")}

# ================================================================================================================ CRISTAL through CFG223 and CFG213
P("\nR2 / CFG223: CRISTAL")
cr, crbyid, rows_Re, n220 = ns223["cr"], ns223["crbyid"], ns223["rows_Re"], ns223["n220"]
EXCL, DET = ns223["EXCL"], list(ns223["DET"])
vec_rows = n220["vec_rows"]
ids12 = [g["id"] for g in cr if g["id"] not in EXCL]


def fin(*v):
    return all(isinstance(x, float) and math.isfinite(x) for x in v)


def Mind(g):
    return 10 ** g["logMstar"] / (1 - g["f_molgas"])


crrows = []


def cr_native_Re(ids, alpha=3.36):
    out = []
    for i in ids:
        g = crbyid[i]
        if not fin(g["Vrot"], g["sig0"], g["Re"], g["z"], g["logMstar"], g["f_molgas"]):
            continue
        go = (g["Vrot"] ** 2 + alpha * g["sig0"] ** 2) / g["Re"] * G2SI
        gb = Mind(g) * xi(g["Re"], g["Re"])
        out.append(dict(id=i, z=g["z"], gbar=gb, D=go / gb, go=go))
    return out


def cr_native_Rout(ids, rdef):
    vr = vec_rows(rdef); out = []
    for i in ids:
        g = crbyid[i]
        if i not in vr or not fin(g["Re"], g["z"], g["logMstar"], g["f_molgas"]):
            continue
        Rk, vb, vt = vr[i]
        go = vt ** 2 / Rk * G2SI
        gb = Mind(g) * xi(g["Re"], Rk)
        out.append(dict(id=i, z=g["z"], gbar=gb, D=go / gb, go=go, R=Rk, Rmarker=vec_rows("outermost_data_marker").get(i, (float("nan"),))[0]))
    return out


# C-i / C-ii for the four CRISTAL figure points
cmp_cr = []
for label, kind, route, ids in (("CRISTAL R_e, fit route (12 discs)", "Re", "fit", ids12), ("CRISTAL R_out, fit route (6)", "Rout", "fit", DET),
                                ("CRISTAL R_e, independent route (6 class-A)", "Re", "ind", DET), ("CRISTAL R_out, independent route (6)", "Rout", "ind", DET)):
    rows = ns223["cr_rows"](kind, route, ids)
    z = [r["z"] for r in rows]; gb = np.array([r["gbar"] for r in rows]); D = np.array([r["D"] for r in rows])
    if kind == "Re":
        xs = np.array([xi(crbyid[r["id"]]["Re"], crbyid[r["id"]]["Re"]) for r in rows])
    else:
        vr = vec_rows("table_Rout")
        xs = np.array([xi(crbyid[r["id"]]["Re"], vr[r["id"]][0]) for r in rows])
    gb_i = (gb / xs) * xs
    r_i = summarise(point_D(label, z, gb_i, D)); r_s = summarise(point_D(label, z, gb, D))
    cmp_cr.append((same_as_committed(r_i, C223[label])[0], same_as_committed(r_s, C223[label])[0]))
check("C-i identity replacement (CRISTAL): the committed g_bar through the native geometry factor reproduces CFG223's four CRISTAL points", f"max |diff| {max(a for a, _ in cmp_cr):.1e}",
      max(a for a, _ in cmp_cr) <= 1e-9)
check("C-ii(b) swap-back (CRISTAL): the committed (1 - f_DM)-based g_bar and D reproduce CFG223's four CRISTAL points", f"max |diff| {max(b for _, b in cmp_cr):.1e}", max(b for _, b in cmp_cr) <= 1e-9)
crn = {}
for key, rows in (("R_e native, six", cr_native_Re(DET)), ("R_e native, twelve-disc set with SED+gas", cr_native_Re(ids12)),
                  ("R_out native, six, outermost data marker (primary)", cr_native_Rout(DET, "outermost_data_marker")),
                  ("R_out native, six, table R_out (CFG223's radius; model curve at or beyond the last marker)", cr_native_Rout(DET, "table_Rout"))):
    crn[key] = summarise(point(key, [r["z"] for r in rows], [r["gbar"] for r in rows], [r["go"] for r in rows]))
    crn[key]["ids"] = [r["id"] for r in rows]
    for r in rows:
        crrows.append(dict(point=key, **{k: r.get(k) for k in ("id", "z", "gbar", "D", "go", "R", "Rmarker")}))
for label in ("CRISTAL R_e, fit route (12 discs)", "CRISTAL R_out, fit route (6)", "CRISTAL R_e, independent route (6 class-A)", "CRISTAL R_out, independent route (6)"):
    c = C223[label]
    P(f"  committed {label}: s* {c['s']:.3f} 95% [{c['lo95']:.3f}, {c['hi95']:.3f}]; pulls flat {c['expected']['FLAT']['pull']:+.2f} proxy {c['expected']['PROXY']['pull']:+.2f} H(z) {c['expected']['H(z)']['pull']:+.2f}")
for k, v in crn.items():
    P(f"  {k}: ids {v['ids']}\n     " + line(v))
# MUTATE on the CRISTAL native R_e six
rws = cr_native_Re(DET)
D0 = np.array([r["D"] for r in rws]); g0 = np.array([r["gbar"] for r in rws])
g1 = g0 * 10 ** 0.2; D1 = D0 / 10 ** 0.2
l0, u0 = implied(D0, g0, NU, A0L); l1, u1 = implied(D1, g1, NU, A0L)
bq = brentq_s(D1, g1)
okm = np.allclose(np.log10(D1) - np.log10(D0), -0.2, atol=1e-12, rtol=0) and (((bq is None) and bool(u1[0])) or (bq is not None and abs(bq - float(l1[0])) <= 1e-6)) and \
    (bool(u1[0]) or float(l1[0]) < float(l0[0]))
check("C-iii MUTATE (CRISTAL native R_e six): log D -0.2 exact, s* moves down or loses its root, brentq agrees", f"s* {10 ** float(l0[0]):.3f} -> "
      f"{'no root' if bool(u1[0]) else f'{10 ** float(l1[0]):.3f}'}", okm)
RES["points"]["CRISTAL"] = crn

P("\nR2 / CFG213: THE Z5 BIN ON NATIVE ROWS (CFG213's deltas, med_ci, verdict and robust rule; its bootstrap state as committed)")
deltas213, medci213, verdict213, KER213, A0F213 = ns213["deltas"], ns213["med_ci"], ns213["verdict"], ns213["KER"], ns213["A0F"]
z5 = {}
for alpha in (3.36, 1.68):
    rows = cr_native_Re(ids12, alpha=alpha)
    for kn, nu in KER213.items():
        for ft in A0F213:
            for law in ("flat", "rival"):
                m, lo, hi = medci213(deltas213(rows, law, ft, nu), ("cfg303", alpha, kn, ft, law))
                z5[(alpha, kn, ft, law)] = dict(n=len(rows), med=m, lo=lo, hi=hi, v=verdict213(lo, hi))
rob = {}
for law in ("flat", "rival"):
    vs = {z5[(a, k, f, law)]["v"] for a in (3.36, 1.68) for k in KER213 for f in A0F213}
    rob[law] = vs.pop() if len(vs) == 1 else "NOT robust (" + ", ".join(sorted(vs)) + ")"
nz5 = z5[(3.36, "nu_mono", "canonical", "flat")]["n"]
committed_route_n = J213["Z5 (CRISTAL primary)"]["3.36|route|nu_mono|canonical|flat"]["n"]
P(f"  native rows n = {nz5} (committed independent route n = {committed_route_n}; same n -> the same bootstrap index matrix: {nz5 == committed_route_n})")
for law in ("flat", "rival"):
    cfit = J213["Z5 (CRISTAL primary)"][f"3.36|fit|nu_mono|canonical|{law}"]; crt = J213["Z5 (CRISTAL primary)"][f"3.36|route|nu_mono|canonical|{law}"]
    nv = z5[(3.36, "nu_mono", "canonical", law)]
    P(f"  {law:5s} nu_mono canonical alpha 3.36: committed fit route {cfit['med']:+.3f} [{cfit['lo']:+.3f}, {cfit['hi']:+.3f}] {cfit['v']}; committed 'independent' route "
      f"{crt['med']:+.3f} [{crt['lo']:+.3f}, {crt['hi']:+.3f}] {crt['v']}; NATIVE {nv['med']:+.3f} [{nv['lo']:+.3f}, {nv['hi']:+.3f}] {nv['v']}")
P(f"  robust verdicts (alpha 3.36 and 1.68, both kernels, both footings): committed fit route: flat {J213['Z5 (CRISTAL primary) robust']['flat']}, rival {J213['Z5 (CRISTAL primary) robust']['rival']}; "
  f"NATIVE: flat {rob['flat']}, rival {rob['rival']}")
RES["cfg213"] = dict(cells={"|".join(map(str, k)): v for k, v in z5.items()}, robust=rob, n=nz5, committed_robust=J213["Z5 (CRISTAL primary) robust"])

# ================================================================================================================ outputs
with open(os.path.join(LANE, "cfg303_rc100_pergalaxy_LCDMFREE.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["idx", "name", "z", "Re_kpc", "Vc_kms", "g_obs_ms2", "fDM_committed", "g_bar_committed_fDM_ms2", "logMbar_jointfit_LCDMMODEL", "logMstar_SED_col6", "mu_t18",
                "g_bar_native_B_ms2", "D_native_B", "in_RC41", "logMstar_SED_Price", "logMgas_Price", "BT_Price", "g_bar_native_A_ms2", "D_native_A", "g_bar_native_G2_ms2"])
    for g in gal:
        q = rc41.get(g["name"])
        w.writerow([g["idx"], g["name"], g["z"], g["Re"], g["Vc"], f"{g['go']:.6e}", g["fd"], f"{g['gb_lcdm']:.6e}", g["lMfit"], g["lMs"], f"{g['mu']:.4f}",
                    f"{g['gbB']:.6e}", f"{g['go'] / g['gbB']:.4f}", int(g["inA"]), q["logMstar_SED"] if q else "", q["logMgas"] if q else "", q["BT"] if q else "",
                    f"{g['gbA']:.6e}" if q else "", f"{g['go'] / g['gbA']:.4f}" if q else "", f"{g['gbG2']:.6e}" if q else ""])
with open(os.path.join(LANE, "cfg303_cristal_pergalaxy_LCDMFREE.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["point", "id", "z", "g_bar_native_ms2", "D_native", "g_obs_ms2", "R_kpc", "R_outermost_marker_kpc"])
    for r in crrows:
        w.writerow([r["point"], r["id"], r["z"], f"{r['gbar']:.6e}", f"{r['D']:.4f}", f"{r['go']:.6e}", r.get("R") or "", r.get("Rmarker") or ""])
npass = sum(CHK)
P(f"\n{npass}/{len(CHK)} checks pass   ({time.time() - T0:.0f} s)")
RES["checks"] = dict(passed=npass, n=len(CHK))


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


json.dump(jclean(RES), open(os.path.join(LANE, "cfg303_rc100_cristal_LCDMFREE_results.json"), "w"), indent=1)
open(os.path.join(LANE, "cfg303_rc100_cristal_LCDMFREE.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
