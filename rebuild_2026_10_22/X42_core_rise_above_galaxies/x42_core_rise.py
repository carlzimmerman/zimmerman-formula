#!/usr/bin/env python3
"""X42_core_rise_above_galaxies: does a physically motivated rule give the cold dark energy core rise above galaxy scale?
H1 self-similar collapse floor s = max(1, (M/M_x)^(1/3)), M_x calibrated on cluster MID terciles only (SPARC + groups out
of sample); alpha free reported; H1-EPS (slope from X41_collapse_floor_sigma) and H1-cM (Dutton & Maccio 2014, PROVISIONAL)
reported only.  H2 baryon retention s = max(1, f_b,sys / f_b,gal), f_b,gal = SPARC median (bg A); within-SPARC f_b trend.

Frozen: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (4a13086d02), AMENDMENT_A1.md (9caa641111).  X40b's machinery (EM1 SPARC,
X30 clusters, P4 groups) executed read-only with output paths redirected into this lane.  One thread.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x42_core_rise.py                 -> .out, _results.json  (exit 0 iff checks pass)
    X42_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x42_core_rise.py    -> exponent 0, f_b inverted (K2, K3 must fail)
"""
import os, sys, json, math, time, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X40B_MUTATE", None); os.environ.pop("X30_MUTATE", None)
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import spearmanr

T0 = time.time()
MUTATE = os.environ.get("X42_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ X40b machinery, read-only (up to its K0 block)
SRC = os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling.py"); TXT = open(SRC).read()
code = TXT[:TXT.index("# ------------------------------------------------------------------ K0: s = 1 reproduces X38")]
old = 'os.path.join(HERE, "x40b_x30_machinery" + TAG + ".log")'; assert code.count(old) == 1
code = code.replace(old, f'{os.path.join(HERE, "x42_x30_machinery" + TAG + ".log")!r}')
NS = {"__file__": os.path.join(HERE, "x40b_sd_scaling.py"), "__name__": "x40b_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, SRC, "exec"), NS)
g = lambda k: NS[k]
FEET, HK, GE, MSUNE, MPCE, KPC = g("FEET"), g("HK"), g("GE"), g("MSUNE"), g("MPCE"), g("KPC")
A0, SIG, SIG_PC, B, r0_fast, GALS, fit_one, pooled, line, UPS = (g(k) for k in ("A0", "SIG", "SIG_PC", "B", "r0_fast", "GALS", "fit_one", "pooled", "line", "UPS"))
prep, RM, I, TID, T3M, ALLI, N = (g(k) for k in ("prep", "RM", "I", "TID", "T3M", "ALLI", "N"))
BGS, X38J, MPIV_MSUN, GROUPS, NSG = g("BGS"), g("X38J"), g("MPIV_MSUN"), g("GROUPS"), g("NSG")
G540, MS540, KP540, HERN_RE, XG, LXG, RHO_H, M_H = (NSG[k] for k in ("G540", "MSUN540", "KPC540", "HERN_RE", "XG", "LXG", "RHO_H", "M_H"))
orig_cluster_halo = NS["cluster_halo"]; grade_clusters = NS["grade_clusters"]
K4_X40b = dict(NS["checks"])["K4"]; K1_X40b = dict(NS["checks"])["K1"]
P(f"X42_core_rise_above_galaxies  {'MUTATE run (H1 exponent 0, H2 f_b inverted)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian, law emergent); cold dark energy (not matter) Burkert cores, Sigma = s * a0/(2 pi G); not theory closed")
P(f"X40b machinery executed read-only [{time.time() - T0:.0f} s]; Sigma_a0 canonical {SIG_PC['canonical']:.2f}, alt {SIG_PC['alt']:.2f} Msun/pc^2")
PC2 = KPC ** 2 / 1e6 / MSUNE                       # (kg/m^2) -> Msun/pc^2
RES = dict(frozen="4a13086d02", amendment="9caa641111", mutate=MUTATE, checks={}, footings={f: {} for f in FEET}); checks = []
STEP0 = json.load(open(os.path.join(HERE, "x42_step0_results.json")))
k1 = bool(STEP0["pass_"]); P(f"K1 Step 0 (scratch rerun of X40b vs committed JSON): {STEP0['n_diff']} differences -> {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))
if not k1:
    P("STOP RULE: Step 0 failed"); open(os.path.join(HERE, f"x42_core_rise{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)

# ------------------------------------------------------------------ rule plumbing: a per-halo s function
CTX = {"sfun": None}
def cluster_halo(i, foot, hk, rule, bcg=True, alpha=None):
    if rule != "X": return orig_cluster_halo(i, foot, hk, rule, bcg, alpha)
    pp = prep(i, foot, hk); rta = pp["rta"]; Mt = pp["Mfair"]
    s = float(CTX["sfun"](kind="cl", i=i, foot=foot, hk=hk, pp=pp, M=Mt))
    r0 = float(r0_fast(Mt, rta, SIG[foot] * s)[0])
    REC.append(("cl", foot, hk, i, Mt / MSUNE, s))
    return math.pi * SIG[foot] * s * r0 ** 2 * B(np.minimum(RM, rta) / r0), s, r0, Mt
NS["cluster_halo"] = cluster_halo
REC = []
def grade_cl(foot, sfun, cells=("h0672", "h0686")):
    CTX["sfun"] = sfun; NS["HK"] = tuple(cells)
    try:
        gc, S_all, M_all = grade_clusters(foot, "X")
    finally:
        NS["HK"] = HK
    return gc

def rc_of(h): return 3 * (100 * h * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
def sparc(f, bgk, sfun, resid=False):
    bg = BGS[bgk]; rc = rc_of(bg["h"]); rows = []; ss = []; lfb = []; res = []; r0s = []; nsat = 0
    for q in GALS:
        lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3); R = q["Rm"]
        Mb = 10 ** q["lMb"]; fb = Mb / (Mb + 10 ** lM)
        s = float(sfun(kind="gal", M=M200, fb=fb)); r0, sat = r0_fast(M200, R200, SIG[f] * s); r0 = float(r0); nsat += int(sat)
        gh = GE * math.pi * SIG[f] * s * r0 ** 2 * B(R / r0) / R ** 2
        lgp = np.log10(np.maximum(q["GB"] + gh[:, None], 1e-300)); w = fit_one(q, lgp); rows.append(w)
        ss.append(s); lfb.append(math.log10(fb)); r0s.append(r0 / KPC)
        if resid:
            iu = int(w[2]); ok = np.broadcast_to(q["OK"], lgp.shape)[:, iu]; r = np.log10(q["GO"][ok]) - lgp[ok, iu]; ww = np.broadcast_to(q["W"][:, None], lgp.shape)[ok, iu]; res.append(float(np.sum(ww * r) / np.sum(ww)))
        REC.append(("gal", f, bgk, None, M200 / MSUNE, s, fb))
    st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])
    st.update(line=line(st), s_median=float(np.median(ss)), s_max=float(np.max(ss)), frac_s_gt1=float(np.mean(np.array(ss) > 1 + 1e-12)),
              r0_median_kpc=float(np.median(r0s)), saturated=nsat)
    return st, np.array(lfb), np.array(res)

def group_logsig(o, foot, sfun, dlM=0.0, fair=False):
    lMb = o["lM"] + dlM; Mb = 10 ** lMb * MS540; a = o["Re"] * KP540 / HERN_RE
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540)
    M200 = (5.364 * Mb) if fair else 10 ** (bg["a"] + bg["b"] * (lMb - 10)) * MS540
    R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    s = float(sfun(kind="grp", M=M200, fb=Mb / (Mb + M200)))
    r0 = float(r0_fast(M200, R200, SIG[foot] * s)[0]); REC.append(("grp", foot, None, None, M200 / MS540, s))
    Mh = math.pi * SIG[foot] * s * r0 ** 2 * B(np.minimum(XG * a, R200) / r0)
    gN = M_H / XG ** 2 + Mh / Mb / XG ** 2
    s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mb / a
    return 0.5 * math.log10(s2) - 3.0, s
def grade_groups(foot, sfun, fair=False):
    d, sl, ss = [], [], []
    for o in GROUPS:
        v, s = group_logsig(o, foot, sfun, fair=fair)
        sp = (group_logsig(o, foot, sfun, 0.01, fair)[0] - group_logsig(o, foot, sfun, -0.01, fair)[0]) / 0.02
        d.append(o["ls"] - v); sl.append(sp); ss.append(s)
    st = NSG["class_stats"](d, sl); st["s_median"] = float(np.median(ss)); st["PASS"] = st["verdict"] == "CONSISTENT"
    return st

ONE = lambda **k: 1.0
# K0: s = 1 reproduces X38 (SPARC, 30 cluster preds) and X40b's X38 groups
k0d = 0.0; k0g = 0.0
X40BJ = json.load(open(os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling_results.json")))
for f in FEET:
    for t in BGS:
        st, _, _ = sparc(f, t, ONE); x = X38J["footings"][f]["sparc"][t]; k0d = max(k0d, abs(st["rms"] - x["rms"]), abs(st["U_median"] - x["U_median"]))
    gc = grade_cl(f, ONE)
    for hk in HK:
        for k, v in gc["cells"][hk].items(): k0d = max(k0d, abs(v["pred"] - X38J["footings"][f]["clusters"]["cells"][hk][k]["pred"]))
    gr = grade_groups(f, ONE); k0g = max(k0g, abs(gr["mean"] - X40BJ["footings"][f]["X38_groups"]["mean"]))
    RES["footings"][f]["X38"] = dict(clusters=gc, groups=gr, groups_fair=grade_groups(f, ONE, fair=True))
k0 = k0d < 1e-6 and k0g < 1e-9
P(f"K0 s = 1 reproduces X38 (SPARC + 30 cluster preds per footing) max |d| {k0d:.1e}; X40b X38-groups mean max |d| {k0g:.1e}: {'PASS' if k0 else 'FAIL'}  [{time.time() - T0:.0f} s]")
checks.append(("K0", k0)); REC.clear()

# ------------------------------------------------------------------ H1 family: s = max(1, (M/M_x)^alpha) [or c-M shape]
EXP13 = 0.0 if MUTATE else 1.0 / 3.0
J41 = json.load(open(os.path.join(REB, "X41_collapse_floor_sigma", "x41_collapse_floor_results.json")))
TAB = {float(k): float(v[0]) for k, v in J41["sigma_coll_table"].items()}
LMT = np.array(sorted(math.log10(m) for m in TAB)); LST = np.array([math.log10(TAB[10 ** l]) for l in LMT])
A_EPS = float((math.log10(TAB[1e15]) - math.log10(TAB[1e13])) / 2.0)
def sig_eps(Msun):
    """X41's EPS Sigma_coll, log-log interpolation; linear log-log extrapolation from the edge pair outside 1e11..1e15."""
    x = math.log10(Msun)
    if x < LMT[0]: return 10 ** (LST[0] + (x - LMT[0]) * (LST[1] - LST[0]) / (LMT[1] - LMT[0]))
    if x > LMT[-1]: return 10 ** (LST[-1] + (x - LMT[-1]) * (LST[-1] - LST[-2]) / (LMT[-1] - LMT[-2]))
    return 10 ** float(np.interp(x, LMT, LST))
P(f"X41_collapse_floor_sigma EPS Sigma_coll table (bg A, Msun/pc^2): " + ", ".join(f"1e{int(l)} {10 ** s_:.2f}" for l, s_ in zip(LMT, LST)) + f"; alpha_EPS (1e13-1e15) = {A_EPS:.4f}")
# Dutton & Maccio 2014 c200 (PROVISIONAL, literature), NFW rho_s r_s shape
HDM = 0.672
def S_cM(Msun):
    c = 10 ** (0.905 - 0.101 * math.log10(Msun * HDM / 1e12)); m = math.log1p(c) - c / (1 + c)
    return Msun ** (1 / 3) * c * c / m                     # proportional to rho_s r_s at fixed 200 rho_c
def s_pow(alpha, lMx):
    return lambda **k: max(1.0, (k["M"] / MSUNE / 10 ** lMx) ** alpha)
def s_cM(lMx):
    Sx = S_cM(10 ** lMx); return lambda **k: max(1.0, S_cM(k["M"] / MSUNE) / Sx) if not MUTATE else 1.0
CHI_CACHE = {}
def chi_cal(foot, maker, key, lMx):
    ck = (foot, key, round(lMx, 9))
    if ck not in CHI_CACHE:
        gc = grade_cl(foot, maker(lMx), cells=("h0672",)); c = gc["cells"]["h0672"]
        CHI_CACHE[ck] = float(sum(c[f"G-MID-T{t}"]["Z"] ** 2 for t in (1, 2, 3)))
    return CHI_CACHE[ck]
MFAIR_MAX = {}
def calibrate(foot, maker, key):
    """0.1-dex grid on log10 M_x in [8, 16], then bounded Brent inside the best grid bracket to 1e-4 dex."""
    grid = np.round(np.arange(8.0, 16.0001, 0.1), 1); vals = []
    flat = None
    for lx in grid:
        if lx > MFAIR_MAX[foot] and flat is not None: vals.append(flat); continue          # s = 1 for every cluster: X38 (exact, cached)
        v = chi_cal(foot, maker, key, float(lx)); vals.append(v)
        if lx > MFAIR_MAX[foot]: flat = v
    k = int(np.argmin(vals)); lo, hi = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    r = minimize_scalar(lambda lx: chi_cal(foot, maker, key, float(lx)), bounds=(lo, hi), method="bounded", options={"xatol": 1e-4})
    best = (float(r.x), float(r.fun)) if r.fun <= vals[k] else (float(grid[k]), float(vals[k]))
    return best
REC.clear()
for f in FEET:
    MFAIR_MAX[f] = max(math.log10(prep(int(i), f, hk)["Mfair"] / MSUNE) for i in ALLI for hk in HK); NS["PREP"].clear()

def full_grade(f, sfun, sfun_fair=None):
    REC.clear()
    sp = {t: sparc(f, t, sfun, resid=(t == "A_c2b_refit"))[0] for t in BGS}
    gc = grade_cl(f, sfun); gr = grade_groups(f, sfun); grf = grade_groups(f, sfun_fair or sfun, fair=True)
    recs = list(REC)
    return dict(sparc=sp, clusters=gc, groups=gr, groups_fair=grf), recs
def chi15(gc): return float(sum(v["Z"] ** 2 for v in gc["cells"]["h0672"].values()))
def legs(res, extra=None):
    bad = [f"SPARC [{t}] (rms {v['rms']:.4f}, U {v['U_median']:.2f})" for t, v in res["sparc"].items() if not v["line"]]
    if not res["groups"]["PASS"]: bad.append(f"groups ({res['groups']['verdict']}, Z {res['groups']['Z']:+.2f})")
    bad += [f"cluster {k}" for k in res["clusters"]["fails"]]
    if extra: bad += extra
    return bad
def show(f, name, res):
    sp = res["sparc"]; gc = res["clusters"]; gr = res["groups"]; grf = res["groups_fair"]; c0, c1 = gc["cells"]["h0672"], gc["cells"]["h0686"]
    for t, v in sp.items():
        P(f"     SPARC [{t}]: rms {v['rms']:.4f}, median U {v['U_median']:.2f} -> {'PASS' if v['line'] else 'FAIL'}; s median {v['s_median']:.3f}, max {v['s_max']:.3f}, frac s>1 {v['frac_s_gt1']:.2f}; r0 med {v['r0_median_kpc']:.2f} kpc; sat {v['saturated']}")
    for k in c0:
        P(f"     {k:10s} meas {c0[k]['meas']:+.3f}+-{c0[k]['s']:.3f} pred {c0[k]['pred']:+.3f} Z {c0[k]['Z']:+.2f} | h0.686 Z {c1[k]['Z']:+.2f}" + ("" if gc["ok"][k] else "  FAIL"))
    P(f"     cluster s by KT tercile {json.dumps({k: round(v, 3) for k, v in gc['meta']['h0672']['s_KT'].items()})}; r0 (Mpc) {json.dumps({k: round(v, 3) for k, v in gc['meta']['h0672']['r0_Mpc'].items()})}; chi2(15 keys, h0.672) {chi15(gc):.2f}")
    P(f"     groups: mean {gr['mean']:+.4f} Z {gr['Z']:+.2f} tot {gr['tot']:.4f} {gr['verdict']} (s median {gr['s_median']:.3f}); fair-share variant {grf['mean']:+.4f} Z {grf['Z']:+.2f} {grf['verdict']} (s median {grf['s_median']:.3f})")

H1R = {}
for f in FEET:
    P(f"\n=== [{f}] Sigma_a0 {SIG_PC[f]:.1f} Msun/pc^2   X38 baseline: groups Z {RES['footings'][f]['X38']['groups']['Z']:+.2f}, cluster chi2_cal "
      f"{sum(RES['footings'][f]['X38']['clusters']['cells']['h0672'][f'G-MID-T{t}']['Z'] ** 2 for t in (1, 2, 3)):.2f}")
    FR = RES["footings"][f]
    for key, label, maker in (("H1", "H1 (alpha = 1/3, graded)", lambda lx: s_pow(EXP13, lx)),
                              ("H1EPS", f"H1-EPS (alpha_EPS = {A_EPS:.4f}, reported only)", lambda lx: s_pow(0.0 if MUTATE else A_EPS, lx)),
                              ("H1cM", "H1-cM (Dutton & Maccio 2014 shape, PROVISIONAL, reported only)", s_cM)):
        lMx, chi = calibrate(f, maker, key)
        sf = maker(lMx)
        res, recs = full_grade(f, sf, sf)
        s_cl = [r for r in recs if r[0] == "cl" and r[2] == "h0672"]
        Sss14 = SIG_PC[f] * (1e14 / 10 ** lMx) ** (A_EPS if key == "H1EPS" else EXP13) if key != "H1cM" else SIG_PC[f] * S_cM(1e14) / S_cM(10 ** lMx)
        Mcl_med = float(np.median([r[4] for r in s_cl]))
        def Sss(Msun):
            if key == "H1cM": return SIG_PC[f] * S_cM(Msun) / S_cM(10 ** lMx)
            return SIG_PC[f] * (Msun / 10 ** lMx) ** (A_EPS if key == "H1EPS" else EXP13)
        conc = {m: Sss(m) / sig_eps(m) for m in (1e13, 1e14, 1e15)}; conc["M_cl_median"] = Sss(Mcl_med) / sig_eps(Mcl_med)
        P(f"  --- {label}: calibrated on cluster MID terciles (h 0.672): log10 M_x = {lMx:.4f}, chi2_cal = {chi:.3f}; Sigma_ss(1e14 Msun) = {Sss14:.1f} Msun/pc^2 "
          f"= {Sss14 / SIG_PC[f]:.2f} Sigma_a0; median cluster M_fair {Mcl_med:.3e}")
        P(f"     implied core-concentration factor Sigma_ss / Sigma_coll(EPS, X41_collapse_floor_sigma): " + ", ".join(f"{k if isinstance(k, str) else f'{k:.0e}'} {v:.1f}x" for k, v in conc.items())
          + f"; peer eta_needed {J41['footings'][f]['eta_needed']}")
        show(f, key, res)
        ok = not legs(res)
        FR[key] = dict(lMx=lMx, chi2_cal=chi, chi2_15=chi15(res["clusters"]), Sigma_ss_1e14_Msun_pc2=Sss14, conc_factor=conc, M_cl_median=Mcl_med,
                       grades=res, passes=ok, failing=legs(res))
        if key == "H1": H1R[f] = recs
        P(f"     {key} [{f}]: {'PASSES' if ok else 'FAILS'}" + ("" if ok else f" (failing: {'; '.join(legs(res))})") + f"   [{time.time() - T0:.0f} s]")
    # alpha free (profile over M_x on chi2_cal)
    prof = {}
    for al in sorted(set([float(x) for x in np.round(np.arange(0.0, 1.0001, 0.05), 2)] + [1 / 3, A_EPS])):
        if al == 0.0:
            prof[al] = dict(lMx=None, chi2_cal=chi_cal(f, lambda lx: ONE, "a0", 12.0)); continue
        lMx, chi = calibrate(f, lambda lx, al=al: s_pow(al, lx), f"a{al:.6f}")
        prof[al] = dict(lMx=lMx, chi2_cal=chi)
    cmin = min(v["chi2_cal"] for v in prof.values()); abest = min(prof, key=lambda a: prof[a]["chi2_cal"])
    allowed = [a for a in prof if prof[a]["chi2_cal"] - cmin <= 4.0]
    d13 = prof[1 / 3]["chi2_cal"] - cmin; dE = prof[A_EPS]["chi2_cal"] - cmin
    for a in sorted(prof): P(f"     alpha {a:.4f}: log10 M_x {prof[a]['lMx'] if prof[a]['lMx'] is None else round(prof[a]['lMx'], 3)}, chi2_cal {prof[a]['chi2_cal']:.3f}, dchi2 {prof[a]['chi2_cal'] - cmin:.3f}")
    P(f"  alpha free: alpha_best {abest:.4f} (chi2_cal {cmin:.3f}); alphas with dchi2 <= 4: {min(allowed):.2f} .. {max(allowed):.2f}; "
      f"alpha = 1/3 dchi2 {d13:.3f} -> {'ALLOWED' if d13 <= 4 else 'NOT ALLOWED'}; alpha_EPS dchi2 {dE:.3f}")
    FR["alpha_free"] = dict(profile={f"{a:.6f}": v for a, v in prof.items()}, alpha_best=abest, chi2_min=cmin, allowed_range=[min(allowed), max(allowed)],
                            dchi2_one_third=d13, one_third_allowed=bool(d13 <= 4), dchi2_alpha_EPS=dE)

# ------------------------------------------------------------------ H2: baryon retention
FBG = [10 ** q["lMb"] / (10 ** q["lMb"] + 10 ** (BGS["A_c2b_refit"]["a"] + BGS["A_c2b_refit"]["b"] * (q["lMb"] - 10))) for q in GALS]
FB_GAL = float(np.median(FBG))
RCA = rc_of(BGS["A_c2b_refit"]["h"])
def r200_solve(Mfun, rgrid, rho200):
    """first radius on rgrid (outward) where the mean enclosed density falls to rho200; brentq in log r. None if no crossing."""
    lm = np.log(3 * Mfun(rgrid) / (4 * np.pi * rgrid ** 3)) - math.log(rho200)
    k = np.where(lm <= 0)[0]
    if len(k) == 0 or k[0] == 0: return None
    j = int(k[0]); return math.exp(brentq(lambda lr: math.log(3 * float(Mfun(np.array([math.exp(lr)]))[0]) / (4 * math.pi * math.exp(3 * lr))) - math.log(rho200),
                                          math.log(rgrid[j - 1]), math.log(rgrid[j]), xtol=1e-13))
# K4b: test halo, point mass M: R200 analytic
Mtst = 1e14 * MSUNE; Rex = (3 * Mtst / (4 * math.pi * 200 * RCA)) ** (1 / 3)
rt = r200_solve(lambda r: np.full_like(np.asarray(r, float), Mtst), np.geomspace(0.01 * Rex, 100 * Rex, 400), 200 * RCA)
k4b = abs(3 * Mtst / (4 * math.pi * rt ** 3) / (200 * RCA) - 1) < 1e-8
k4 = K4_X40b and k4b
P(f"\nK4 groups integrator vs P4 (X40b K4) {K4_X40b}; R200 solver test halo |rho/200rho_c - 1| {abs(3 * Mtst / (4 * math.pi * rt ** 3) / (200 * RCA) - 1):.1e}: {'PASS' if k4 else 'FAIL'}")
checks.append(("K4", k4))
FBC = {}; NO200 = {}
LRM = np.log(RM)
for f in FEET:
    for hk in HK:
        n0 = 0
        for i in ALLI:
            i = int(i); pp = prep(i, f, hk); Mt = pp["Mfair"]; rta = pp["rta"]
            r0 = float(r0_fast(Mt, rta, SIG[f])[0])
            Mb = pp["Mb"]
            def Mfun(r, Mb=Mb, r0=r0, rta=rta):
                r = np.asarray(r, float)
                mb = np.exp(np.interp(np.log(r), LRM, np.log(np.maximum(Mb, 1e-300))))
                return mb + math.pi * SIG[f] * r0 ** 2 * B(np.minimum(r, rta) / r0)
            R2 = r200_solve(Mfun, RM, 200 * RCA)
            if R2 is None: R2 = rta; n0 += 1
            mb = float(np.exp(np.interp(math.log(R2), LRM, np.log(np.maximum(Mb, 1e-300))))); mh = float(math.pi * SIG[f] * r0 ** 2 * B(min(R2, rta) / r0))
            FBC[(f, hk, i)] = mb / (mb + mh)
        NO200[(f, hk)] = n0; NS["PREP"].clear()
def s_H2(**k):
    fb = FBC[(k["foot"], k["hk"], int(k["i"]))] if k["kind"] == "cl" else k["fb"]
    return max(1.0, (FB_GAL / fb) if MUTATE else (fb / FB_GAL))
def s_H2_rta(**k):
    fb = (1 / 6.364) if k["kind"] == "cl" else k["fb"]
    return max(1.0, (FB_GAL / fb) if MUTATE else (fb / FB_GAL))
H2_fair = lambda **k: max(1.0, (FB_GAL * 6.364) if MUTATE else (1 / 6.364) / FB_GAL)
P(f"\n=== H2 baryon retention: f_b,gal (SPARC median, bg A) = {FB_GAL:.4f}; SPARC f_b range {min(FBG):.4f} .. {max(FBG):.4f}")
H2R = {}
for f in FEET:
    FR = RES["footings"][f]
    fbt = {f"T{t+1}": float(np.median([FBC[(f, 'h0672', int(i))] for i in I[TID == t]])) for t in range(3)}
    fbg = [o["lM"] for o in GROUPS]
    bgA = BGS["A_c2b_refit"]
    fbgr = [10 ** l / (10 ** l + 10 ** (bgA["a"] + bgA["b"] * (l - 10))) for l in fbg]
    P(f"  [{f}] cluster f_b(R200) median by KT tercile {json.dumps({k: round(v, 4) for k, v in fbt.items()})}, all {np.median([FBC[(f, 'h0672', int(i))] for i in ALLI]):.4f}; "
      f"no R200 inside grid (r_ta used) {NO200[(f, 'h0672')]}/{NO200[(f, 'h0686')]}; groups f_b median {np.median(fbgr):.4f} (range {min(fbgr):.4f} .. {max(fbgr):.4f})")
    res, recs = full_grade(f, s_H2, H2_fair); H2R[f] = recs
    # T-fb: within-SPARC residual trend vs log f_b (bg A), under H2 and under X38
    def tfb(sfun):
        st, lfb, rr = sparc(f, "A_c2b_refit", sfun, resid=True); rho, p = spearmanr(lfb, rr); sl = float(np.polyfit(lfb, rr, 1)[0])
        return dict(rho=float(rho), p=float(p), ols_slope_dex_per_dex=sl, strong=bool(abs(rho) >= 0.30 and p < 0.01))
    REC.clear(); T_H2 = tfb(s_H2); T_X38 = tfb(ONE); REC.clear()
    P(f"  --- H2 [{f}]")
    show(f, "H2", res)
    P(f"     T-fb (within SPARC, bg A, residual vs log f_b): H2 rho {T_H2['rho']:+.3f} p {T_H2['p']:.2e} slope {T_H2['ols_slope_dex_per_dex']:+.3f} -> {'STRONG' if T_H2['strong'] else 'not strong'}; "
          f"X38 rho {T_X38['rho']:+.3f} p {T_X38['p']:.2e} slope {T_X38['ols_slope_dex_per_dex']:+.3f} -> {'STRONG' if T_X38['strong'] else 'not strong'}")
    rv, _ = full_grade(f, s_H2_rta, H2_fair)
    P(f"     (reported) cluster f_b at r_ta (1/6.364, s = {(1 / 6.364) / FB_GAL:.3f}): MID T3 Z {rv['clusters']['cells']['h0672']['G-MID-T3']['Z']:+.2f}, fails {rv['clusters']['fails'] or 'none'}")
    lg = legs(res, ["T-fb STRONG"] if T_H2["strong"] else None); ok = not lg
    FR["H2"] = dict(f_b_gal=FB_GAL, f_b_cluster_KT=fbt, groups_f_b_median=float(np.median(fbgr)), no_R200=[NO200[(f, h)] for h in HK], grades=res, T_fb_H2=T_H2, T_fb_X38=T_X38,
                    variant_rta=dict(MID_T3_Z=rv["clusters"]["cells"]["h0672"]["G-MID-T3"]["Z"], fails=rv["clusters"]["fails"], chi2_15=chi15(rv["clusters"])),
                    chi2_15=chi15(res["clusters"]), passes=ok, failing=lg)
    P(f"     H2 [{f}]: {'PASSES' if ok else 'FAILS'}" + ("" if ok else f" (failing: {'; '.join(lg)})") + f"   [{time.time() - T0:.0f} s]")

# ------------------------------------------------------------------ c-M comparison curve (PROVISIONAL)
cm = {f"1e{l}": float((math.log(S_cM(10 ** (l + 0.01))) - math.log(S_cM(10 ** (l - 0.01)))) / (0.02 * math.log(10))) for l in (11, 12, 13, 14, 15)}
RES["cM_curve"] = dict(local_slope=cm, ratio_1e15_over_Mpiv=S_cM(1e15) / S_cM(MPIV_MSUN), M_piv=MPIV_MSUN)
P(f"\n(reported only, PROVISIONAL) Dutton & Maccio 2014 NFW rho_s r_s local slope: " + ", ".join(f"{k} {v:.3f}" for k, v in cm.items())
  + f"; S(1e15)/S(M_piv {MPIV_MSUN:.2e}) = {RES['cM_curve']['ratio_1e15_over_Mpiv']:.2f}; alpha_EPS (X41_collapse_floor_sigma) {A_EPS:.3f}")

# ------------------------------------------------------------------ checks K2, K3
def k2_of(recs, f):
    lMx = RES["footings"][f]["H1"]["lMx"]
    sall = [r[5] for r in recs]; okf = all(s >= 1.0 for s in sall) and all(r[5] == 1.0 for r in recs if r[4] <= 10 ** lMx)
    cl = {r[3]: r[5] for r in recs if r[0] == "cl" and r[2] == "h0672"}
    t1 = float(np.median([cl[int(i)] for i in I[TID == 0]])); t3 = float(np.median([cl[int(i)] for i in I[TID == 2]]))
    return okf and t3 > t1, t1, t3
k2 = True
for f in FEET:
    ok, t1, t3 = k2_of(H1R[f], f); k2 &= ok
    P(f"K2 [{f}] H1 floor + rise: s >= 1, s = 1 at M <= M_x, median s KT T3 {t3:.3f} > T1 {t1:.3f}: {'ok' if ok else 'FAIL'}")
checks.append(("K2", k2))
k3 = True
for f in FEET:
    gal = [r for r in H2R[f] if r[0] == "gal"]; cl = [r[5] for r in H2R[f] if r[0] == "cl" and r[2] == "h0672"]
    okg = all(r[5] == 1.0 for r in gal if r[6] <= FB_GAL); ok = okg and float(np.median(cl)) > 1.0; k3 &= ok
    P(f"K3 [{f}] H2 floor: SPARC f_b <= f_b,gal -> s = 1 ({okg}); cluster median s {np.median(cl):.3f} > 1: {'ok' if ok else 'FAIL'}")
checks.append(("K3", k3))
import resource
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
checks.append(("K5", rss < 1.0))

# ------------------------------------------------------------------ verdict
pas = {h: {f: RES["footings"][f][h]["passes"] for f in FEET} for h in ("H1", "H2")}
labels = []
if all(pas["H1"].values()): labels.append("H1 PASSES OUT OF SAMPLE")
if all(pas["H2"].values()): labels.append("H2 PASSES")
if not labels:
    if any(any(v.values()) for v in pas.values()): labels.append(f"UNDECIDED (per-footing passes: {pas})")
    else: labels.append("BOTH FAIL")
RES["verdict"] = " + ".join(labels); RES["passes"] = pas
P(f"\n=== VERDICT: {RES['verdict']}")
for h in ("H1", "H2"):
    for f in FEET:
        P(f"  {h} [{f}] failing: {'; '.join(RES['footings'][f][h]['failing']) or 'none'}")
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss:.2f} GB")
open(os.path.join(HERE, f"x42_core_rise{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x42_core_rise_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
