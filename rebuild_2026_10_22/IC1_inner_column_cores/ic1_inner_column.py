#!/usr/bin/env python3
"""IC1_inner_column_cores: is the missing cluster-core concentration the inner column of an ordinarily collapsed halo?
Rule IC1: Sigma_core = max(a0/(2 pi G), Sigma_IC), Sigma_IC = densest inside-out collapse column (NFW97 median EPS epoch
per inner fraction f, shell density 18 pi^2 rho_m(z_c), max over f), matched to Burkert by peak self-acceleration.
No free amplitude.

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (6e0ea16bc2); AMENDMENT_A1.md (pre-result, with this script).
X40b's committed machinery (EM1 SPARC, X30 clusters, P4 groups) and X41's committed EPS block are executed read-only, with
only output paths redirected. One thread.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ic1_inner_column.py                 -> .out, _results.json
    IC1_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ic1_inner_column.py    -> w with the opposite sign (K2 must fail)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
for _v in ("X30_MUTATE", "X40B_MUTATE", "X41_MUTATE"): os.environ.pop(_v, None)
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import erfcinv

T0 = time.time()
MUTATE = os.environ.get("IC1_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
P(f"IC1_inner_column_cores  {'MUTATE run (w with the opposite sign)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian, law emergent); cold dark energy (not matter) Burkert cores, Sigma = max(a0/(2 pi G), Sigma_IC); not theory closed")

# ------------------------------------------------------------------ X40b machinery, read-only (up to its K0 block)
X40BSRC = os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling.py"); TB = open(X40BSRC).read()
codeB = TB[:TB.index("# ------------------------------------------------------------------ K0: s = 1 reproduces X38")]
assert codeB.count('"x40b_x30_machinery"') == 1
codeB = codeB.replace('"x40b_x30_machinery"', '"ic1_x30_machinery"')                       # output path only
NB = {"__file__": os.path.abspath(__file__), "__name__": "x40b_ro"}; argv0 = sys.argv; sys.argv = [X40BSRC]
_cap = io.StringIO()
with contextlib.redirect_stdout(_cap):
    exec(compile(codeB, X40BSRC, "exec"), NB)
sys.argv = argv0
for l in _cap.getvalue().splitlines(): OUT.append("  [X40b] " + l)
P(f"X40b machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]; its own K1/K2a/K4: "
  + ", ".join(f"{k} {'PASS' if ok else 'FAIL'}" for k, ok in NB["checks"]) + (" (K2a printed only)" if not NB["k2a"] else ""))
FEET, HK, GALS, fit_one, pooled, line, UPS, A0 = (NB[k] for k in ("FEET", "HK", "GALS", "fit_one", "pooled", "line", "UPS", "A0"))
GE, MSUNE, MPCE, KPC = NB["GE"], NB["MSUNE"], NB["MPCE"], NB["KPC"]
B, r0_fast, SIG, SIG_PC, prep, RM, ALLI, I, TID, N = (NB[k] for k in ("B", "r0_fast", "SIG", "SIG_PC", "prep", "RM", "ALLI", "I", "TID", "N"))
BGS, X38J, GROUPS, MS540 = NB["BGS"], NB["X38J"], NB["GROUPS"], NB["MS540"]
G540, KP540, HERN_RE, XG, LXG, RHO_H, M_H, NSG = (NB[k] for k in ("G540", "KP540", "HERN_RE", "XG", "LXG", "RHO_H", "M_H", "NSG"))
X40BJ = json.load(open(os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling_results.json")))

# ------------------------------------------------------------------ X41 EPS block, read-only (EM1 with its CLASS backgrounds)
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- halo profiles")], EM1SRC, "exec"), NE)
sys.argv = argv0
X41SRC = os.path.join(REB, "X41_collapse_floor_sigma", "x41_collapse_floor.py"); T41 = open(X41SRC).read()
code41 = T41[T41.index("# ------------------------------------------------------------------ EPS formation"):T41.index("k2 = all(abs(EPS[t][\"s8\"]")]
N41 = {"np": np, "math": math, "MUTATE": False, "BGSE": NE["BGS"]}
exec(compile(code41, X41SRC, "exec"), N41)
EPS, sigma_coll41 = N41["EPS"], N41["sigma_coll"]
X41J = json.load(open(os.path.join(REB, "X41_collapse_floor_sigma", "x41_collapse_floor_results.json")))
P(f"X41 EPS block executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
checks = []
RES = dict(frozen="6e0ea16bc2", amendment="AMENDMENT_A1.md", mutate=MUTATE, Sigma_a0_Msun_pc2=SIG_PC, checks={}, footings={})

# S0b / K1: X41's sigma_coll_table
k1d = 0.0
for k, (sc, zf) in X41J["sigma_coll_table"].items():
    s_, z_, _ = sigma_coll41("A_c2b_refit", float(k)); k1d = max(k1d, abs(s_ / sc - 1), abs(z_ - zf) / max(abs(zf), 1e-12))
k1 = k1d < 1e-8
P(f"S0b/K1 X41 sigma_coll_table reproduced: max rel |d| {k1d:.1e}: {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))

# ------------------------------------------------------------------ rule IC1 (frozen section 2)
DCRIT, DELTA = 1.686, 18 * math.pi ** 2
W = math.sqrt(2.0) * float(erfcinv(0.5)); W_USE = -W if MUTATE else W
PC2_MPC = 1e12                                                                         # (pc / Mpc)^2
h_ = lambda x: math.log(1 + x * x) + 2 * math.log(1 + x) - 2 * math.atan(x)
_kb = minimize_scalar(lambda lx: -h_(math.exp(lx)) / math.exp(2 * lx), bounds=(math.log(0.05), math.log(20)), method="bounded", options={"xatol": 1e-12})
KB = math.pi * (-_kb.fun)
mN = lambda x: math.log(1 + x) - x / (1 + x)
_nf = minimize_scalar(lambda lx: -mN(math.exp(lx)) / math.exp(2 * lx), bounds=(math.log(0.1), math.log(20)), method="bounded", options={"xatol": 1e-12})
NFWPK = -_nf.fun
P(f"w = sqrt(2) erfcinv(1/2) = {W:.6f}{' (MUTATE: used as ' + format(W_USE, '.6f') + ')' if MUTATE else ''}; k_B = pi sup h/x^2 = {KB:.6f}; NFW sup m/x^2 = {NFWPK:.6f}")

def zc_of(tag, M, f):
    """Return (z_c, D_c) for inner mass fraction f of halo mass M (Msun); D_c unclipped."""
    e = EPS[tag]; s2 = lambda l: float(np.interp(l, e["lMg"], e["s2"]))
    S = math.sqrt(max(s2(math.log10(f * M)) - s2(math.log10(M)), 0.0)); Dc = DCRIT / (DCRIT + W_USE * S)
    if Dc >= 1.0 or Dc <= 0.0: return 0.0, Dc
    return float(np.interp(-Dc, -e["Dg"], e["zg"])), Dc
def Ccol(tag, M, f):
    zc, _ = zc_of(tag, M, f); rho = DELTA * EPS[tag]["rhom0"] * (1 + zc) ** 3
    rf = (3 * f * M / (4 * math.pi * rho)) ** (1 / 3); return rho * rf / PC2_MPC, zc      # Msun/pc^2
CACHE = {}
def sigma_IC(tag, M):
    """Msun/pc^2 (Burkert-equivalent), plus argmax f, z_c, C_hat, BOUNDARY flag."""
    key = (tag, float(M))
    if key in CACHE: return CACHE[key]
    fmin = max(1e-6, 10 ** float(EPS[tag]["lMg"][0]) / M)
    lf = np.arange(math.log10(fmin), math.log10(0.5) + 1e-12, 0.02)
    if lf[-1] < math.log10(0.5) - 1e-12: lf = np.append(lf, math.log10(0.5))
    cv = np.array([Ccol(tag, M, 10 ** l)[0] for l in lf]); k = int(np.argmax(cv))
    if 0 < k < len(lf) - 1:
        r = minimize_scalar(lambda l: -Ccol(tag, M, 10 ** l)[0], bounds=(lf[k - 1], lf[k + 1]), method="bounded", options={"xatol": 1e-6})
        lbest, cbest = float(r.x), -float(r.fun)
        if cv[k] > cbest: lbest, cbest = float(lf[k]), float(cv[k])
    else:
        lbest, cbest = float(lf[k]), float(cv[k])
    bnd = k <= 1
    out = dict(S=(4 * math.pi / 3) * cbest / KB, f=10 ** lbest, zc=Ccol(tag, M, 10 ** lbest)[1], C=cbest, boundary=bool(bnd), at_half=bool(k == len(lf) - 1))
    CACHE[key] = out; return out
def sigma_IC2(tag, M):
    """BORROWED comparator: NFW with Dutton & Maccio 2014 c200(M), z = 0, peak-acceleration matched. Msun/pc^2."""
    h = BGS[tag]["h"]; rc = 2.775e11 * h ** 2; R200 = (3 * M / (4 * math.pi * 200 * rc)) ** (1 / 3)
    c = 10 ** (0.905 - 0.101 * math.log10(M * h / 1e12)); rs_rhos = M * c * c / (4 * math.pi * R200 ** 2 * mN(c)) / PC2_MPC
    return 4 * math.pi * rs_rhos * NFWPK / KB
CNT = {"boundary": 0, "sat": 0, "active": 0, "n": 0}
def s_of(rule, foot, tag, M):
    if rule == "one": return 1.0
    if rule == "IC1":
        d = sigma_IC(tag, M); CNT["boundary"] += int(d["boundary"]); S = d["S"]
    elif rule == "IC2":
        S = sigma_IC2(tag, M)
    CNT["n"] += 1; CNT["active"] += int(S > SIG_PC[foot])
    return max(1.0, S / SIG_PC[foot])
def reset():
    for k in CNT: CNT[k] = 0

# ------------------------------------------------------------------ K2: collapse epoch; K3: shape constants; K4: matching identity
k2 = True; zrows = []
for Mt in (1e12, 1e14, 1e15):
    zl = []
    for f in (1e-4, 1e-3, 1e-2, 0.1, 0.5):
        zc, Dc = zc_of("A_c2b_refit", Mt, f); e = EPS["A_c2b_refit"]
        resid = abs(float(np.interp(zc, e["zg"], e["Dg"])) - Dc) if 0 < Dc < 1 else float("inf")
        ok = (0 < Dc <= 1.0) and resid < 1e-8; k2 &= ok; zl.append(zc)
    mono = all(zl[i] >= zl[i + 1] - 1e-12 for i in range(len(zl) - 1)); k2 &= mono
    zrows.append(f"M {Mt:.0e}: z_c(f=1e-4..0.5) " + "/".join(f"{z:.3f}" for z in zl) + f" monotone {mono}")
P("K2 collapse epoch: " + "; ".join(zrows) + f": {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
CD1J = json.load(open(os.path.join(REB, "CD1_a0_cored_dwarf_ceiling", "cd1_dwarf_ceiling.json")))
k3 = abs(KB - 2 * math.pi * CD1J["ceiling_over_a0"]) < 1e-6 and abs(NFWPK - 0.216217) < 1e-5 and abs(KB - math.pi * math.exp(NB["LYMAX"])) < 1e-9
P(f"K3 shape constants: k_B {KB:.9f} vs 2 pi x CD1 {2 * math.pi * CD1J['ceiling_over_a0']:.9f} vs X40b pi e^LYMAX {math.pi * math.exp(NB['LYMAX']):.9f}; NFW {NFWPK:.6f}: {'PASS' if k3 else 'FAIL'}")
checks.append(("K3", k3))
d14 = sigma_IC("A_c2b_refit", 1e14); Sig_si = d14["S"] * MSUNE / (3.0857e16) ** 2; r0t = 3.0857e21
gmax = -minimize_scalar(lambda lr: -GE * math.pi * Sig_si * r0t ** 2 * float(B(math.exp(lr) / r0t)) / math.exp(2 * lr),
                        bounds=(math.log(r0t * 0.05), math.log(r0t * 20)), method="bounded", options={"xatol": 1e-12}).fun
gIC = GE * (4 * math.pi / 3) * d14["C"] * MSUNE / (3.0857e16) ** 2
k4 = abs(gmax / gIC - 1) < 1e-6
P(f"K4 matching identity at 1e14 Msun: Burkert peak g {gmax:.6e} vs g_IC {gIC:.6e} m/s^2 (rel {gmax / gIC - 1:+.1e}): {'PASS' if k4 else 'FAIL'}"); checks.append(("K4", k4))
CACHE.clear()

# ------------------------------------------------------------------ graded machinery (X40b's bodies, the s-rule replaced)
def sparc(f, tag, rule):
    bg = BGS[tag]; a, b, hh = bg["a"], bg["b"], bg["h"]
    rc = 3 * (100 * hh * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []; sch = []; r0ch = []; nsat = 0
    for q in GALS:
        lM = a + b * (q["lMb"] - 10); M200 = 10 ** lM * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3); R = q["Rm"]
        s = s_of(rule, f, tag, 10 ** lM)
        r0, sat = r0_fast(M200, R200, SIG[f] * s); r0 = float(r0); nsat += int(sat)
        gh = np.zeros((len(R), len(UPS))); gh[:] = (GE * math.pi * SIG[f] * s * r0 ** 2 * B(R / r0) / R ** 2)[:, None]
        w = fit_one(q, np.log10(np.maximum(q["GB"] + gh, 1e-300))); rows.append(w); sch.append(s); r0ch.append(r0 / KPC)
    st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])
    return dict(st, line=line(st), s_median=float(np.median(sch)), s_max=float(np.max(sch)), frac_s_gt1=float(np.mean(np.array(sch) > 1 + 1e-12)),
                r0_median_kpc=float(np.median(r0ch)), sat=nsat)
def cluster_halo(i, foot, hk, rule, bcg=True, alpha=None):
    pp = prep(i, foot, hk); rta = pp["rta"]; Mt = pp["Mfair"]
    Mic = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE                                    # X41's executed cluster mass (A1)
    s = s_of(rule, foot, "A_c2b_refit", Mic)
    r0, sat = r0_fast(Mt, rta, SIG[foot] * s); r0 = float(r0); CNT["sat"] += int(sat)
    return math.pi * SIG[foot] * s * r0 ** 2 * B(np.minimum(RM, rta) / r0), s, r0, Mt
def group_logsig_halo(o, foot, rule, dlM=0.0, fair=False, alpha=None, halo=True, ret_s=False):
    lMb = o["lM"] + dlM; Mb = 10 ** lMb * MS540; a = o["Re"] * KP540 / HERN_RE
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540)
    M200 = (5.364 * Mb) if fair else 10 ** (bg["a"] + bg["b"] * (lMb - 10)) * MS540
    R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    gN = M_H / XG ** 2; s = 1.0
    if halo:
        s = s_of(rule, foot, "A_c2b_refit", M200 / MS540)
        r0 = float(r0_fast(M200, R200, SIG[foot] * s)[0])
        rr = XG * a
        Mh = math.pi * SIG[foot] * s * r0 ** 2 * B(np.minimum(rr, R200) / r0)
        gN = gN + Mh / Mb / XG ** 2
    s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mb / a
    v = 0.5 * math.log10(s2) - 3.0
    return (v, s) if ret_s else v
NB["cluster_halo"] = cluster_halo; NB["group_logsig_halo"] = group_logsig_halo                # X40b's graders call these
grade_clusters, grade_groups = NB["grade_clusters"], NB["grade_groups"]

# ------------------------------------------------------------------ S0a / K0: s = 1 reproduces the committed X38 baseline
k0d = 0.0
for f in FEET:
    for t in BGS:
        st = sparc(f, t, "one"); x = X38J["footings"][f]["sparc"][t]
        k0d = max(k0d, abs(st["rms"] - x["rms"]), abs(st["U_median"] - x["U_median"]))
    gc, _, _ = grade_clusters(f, "one")
    for hk in HK:
        for k, v in gc["cells"][hk].items():
            k0d = max(k0d, abs(v["pred"] - X38J["footings"][f]["clusters"]["cells"][hk][k]["pred"]))
    gr = grade_groups(f, "one"); xb = X40BJ["footings"][f]["X38_groups"]
    k0d = max(k0d, abs(gr["mean"] - xb["mean"]), abs(gr["Z"] - xb["Z"]))
    RES["footings"].setdefault(f, {})["X38"] = dict(clusters=gc, groups=gr)
k0 = k0d < 1e-6
P(f"S0a/K0 s = 1 reproduces X38's committed SPARC + 30 cluster preds and X40b's committed X38 groups mean/Z per footing: max |d| {k0d:.1e}: {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0)); P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
if not (k0 and k1):
    P("STOP RULE (section 0): Step 0 failed; no graded number is produced.")
    RES["checks"] = {k: bool(ok) for k, ok in checks}; RES["verdict"] = "STOPPED AT STEP 0"
    open(os.path.join(HERE, f"ic1_inner_column{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"ic1_inner_column_results{TAG}.json"), "w"), indent=1, default=float); sys.exit(1)

# ------------------------------------------------------------------ reported: Sigma_IC table, slope, crossover, eta_IC
TAB = {}
for tag in BGS:
    TAB[tag] = {}
    for l in (11, 12, 13, 14, 15):
        d = sigma_IC(tag, 10.0 ** l); sc41 = sigma_coll41(tag, 10.0 ** l)[0]
        TAB[tag][f"1e{l}"] = dict(Sigma_IC=d["S"], f_argmax=d["f"], z_c=d["zc"], C_hat=d["C"], boundary=d["boundary"], at_half=d["at_half"],
                                  Sigma_coll_X41=sc41, eta_IC=d["S"] / sc41, Sigma_IC2_borrowed=sigma_IC2(tag, 10.0 ** l))
        r = TAB[tag][f"1e{l}"]
        P(f"  Sigma_IC [{tag}] M 1e{l}: {r['Sigma_IC']:.1f} Msun/pc^2 (f* {r['f_argmax']:.2e}, z_c {r['z_c']:.2f}{', BOUNDARY' if r['boundary'] else ''}{', at f=1/2' if r['at_half'] else ''}); "
          f"eta_IC = Sigma_IC / Sigma_coll(X41) {r['eta_IC']:.2f}; IC2 borrowed {r['Sigma_IC2_borrowed']:.1f}")
    sl = (math.log10(TAB[tag]["1e15"]["Sigma_IC"]) - math.log10(TAB[tag]["1e13"]["Sigma_IC"])) / 2
    TAB[tag]["slope_13_15"] = sl
    xo = {}
    for f in FEET:
        g = lambda lm: math.log(sigma_IC(tag, 10 ** lm)["S"] / SIG_PC[f])
        lo, hi = 9.0, 16.0
        if g(lo) < 0 < g(hi):
            for _ in range(60):
                mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if g(mid) < 0 else (lo, mid)
            xo[f] = 0.5 * (lo + hi)
        else: xo[f] = None
    TAB[tag]["crossover_log10M"] = xo
    P(f"  [{tag}] log slope 1e13-1e15 {sl:.3f} (X40b requires 0.25-0.30); crossover Sigma_IC = Sigma_a0 at log10 M = "
      + ", ".join(f"{f} {('%.3f' % v) if v is not None else 'none in [9, 16]'}" for f, v in xo.items())
      + "; eta_IC vs X42 post-hoc 13.6 and X41's 11-23 (comparison only)")
RES["Sigma_IC_table"] = TAB

# ------------------------------------------------------------------ grading per footing
INNER = ["G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-IN-all", "G-IN-Mall"]
def fmt_keys(gc, base):
    c0, c1 = gc["cells"]["h0672"], gc["cells"]["h0686"]
    for k in c0:
        P(f"     {k:10s} meas {c0[k]['meas']:+.3f}+-{c0[k]['s']:.3f} pred {c0[k]['pred']:+.3f} Z {c0[k]['Z']:+.2f} (X38 Z {base[k]['Z']:+.2f}) | h0.686 Z {c1[k]['Z']:+.2f}" + ("" if gc["ok"][k] else "  FAIL"))
def run_rule(f, rule):
    reset(); sp_ = {t: sparc(f, t, rule) for t in BGS}; spc = dict(CNT); reset()
    gc, SC, MC = grade_clusters(f, rule); clc = dict(CNT); reset()
    gr = grade_groups(f, rule); grf = grade_groups(f, rule, fair=True); reset()
    return sp_, spc, gc, clc, gr, grf
VERD = {}
for f in FEET:
    base = RES["footings"][f]["X38"]["clusters"]["cells"]["h0672"]; FR = RES["footings"][f]
    P(f"\n=== [{f}] Sigma_a0 {SIG_PC[f]:.1f} Msun/pc^2   X38 groups (s = 1): mean {FR['X38']['groups']['mean']:+.4f} Z {FR['X38']['groups']['Z']:+.2f} {FR['X38']['groups']['verdict']}")
    for rule, lab in (("IC1", "IC1 (native, verdict-bearing)"), ("IC2", "IC2 (BORROWED Dutton & Maccio comparator, no verdict weight)")):
        P(f"  --- {lab}")
        sp_, spc, gc, clc, gr, grf = run_rule(f, rule)
        for t, st in sp_.items():
            x = X38J["footings"][f]["sparc"][t]
            P(f"  SPARC [{t}]: rms {st['rms']:.4f}, median U {st['U_median']:.2f} -> line {'PASS' if st['line'] else 'FAIL'} (X38 {x['rms']:.4f}@{x['U_median']:.2f}); "
              f"s median {st['s_median']:.3f}, max {st['s_max']:.3f}, frac s>1 {st['frac_s_gt1']:.3f}; median r0 {st['r0_median_kpc']:.2f} kpc; SATURATED {st['sat']}")
        P(f"  SPARC counts (both backgrounds): halos {spc['n']}, Sigma > Sigma_a0 in {spc['active']}, BOUNDARY {spc['boundary']}")
        fmt_keys(gc, base)
        m = gc["meta"]["h0672"]
        P(f"     cluster s by KT tercile {json.dumps({k: round(v, 3) for k, v in m['s_KT'].items()})}, all-326 median {m['s_median_all']:.3f}, max {m['s_max']:.3f}; "
          f"r0 (Mpc) {json.dumps({k: round(v, 3) for k, v in m['r0_Mpc'].items()})}; cluster-cells {clc['n']}, active {clc['active']}, BOUNDARY {clc['boundary']}, SATURATED {clc['sat']}")
        inner_ok = {k: gc["ok"][k] for k in INNER}
        P(f"     inner sub-grade (reported, not a class pass): {sum(inner_ok.values())}/{len(INNER)} pass; failing {[k for k, v in inner_ok.items() if not v] or 'none'}"
          f" (X38: {sum(FR['X38']['clusters']['ok'][k] for k in INNER)}/{len(INNER)})")
        P(f"     groups: mean {gr['mean']:+.4f} Z {gr['Z']:+.2f} tot {gr['tot']:.4f} {gr['verdict']} (s median {gr['s_median']:.3f}); fair-share variant {grf['mean']:+.4f} Z {grf['Z']:+.2f} {grf['verdict']}")
        spass = all(st["line"] for st in sp_.values()); cpass = not gc["fails"]
        inactive = spc["active"] == 0 and clc["active"] == 0
        v = ("IC1 INACTIVE" if inactive else "IC1 PASSES" if spass and cpass else "IC1 PASSES SPARC ONLY" if spass
             else "IC1 PASSES CLUSTERS ONLY" if cpass else "IC1 FAILS")
        if rule == "IC2": v = v.replace("IC1", "IC2 (BORROWED)")
        suf = []
        if clc["n"] and clc["boundary"] / clc["n"] > 0.10: suf.append("BOUNDARY-LIMITED")
        if any(st["frac_s_gt1"] > 0.10 for st in sp_.values()): suf.append("FLOOR-BREAKING")
        v = v + ("".join(f" [{s_}]" for s_ in suf))
        det = ([] if spass else ["SPARC line"]) + gc["fails"]
        FR[rule] = dict(sparc=sp_, sparc_counts=spc, clusters=gc, cluster_counts=clc, groups=gr, groups_fair=grf, inner=inner_ok, verdict=v, failing=det)
        P(f"     {rule} [{f}]: {v}" + (f"  (failing: {', '.join(det)})" if det else "") + f"; groups {'PASS' if gr['PASS'] else 'FAIL'}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
        if rule == "IC1": VERD[f] = v

# ------------------------------------------------------------------ reported: dwarf ordering
P("\n=== dwarf ordering (reported only; mass-only EPS median, EM1 relation extrapolated, M_b = M*)")
bgA = BGS["A_c2b_refit"]; DW = {}
for f in FEET:
    rows = {r["name"]: r for r in CD1J["footings"][f]["rows"]}; d = {}
    for nm in ("Draco", "Sextans", "Fornax", "Leo I"):
        r = rows[nm]; lM200 = bgA["a"] + bgA["b"] * (r["logM"] - 10); si = sigma_IC("A_c2b_refit", 10 ** lM200)
        d[nm] = dict(logMstar=r["logM"], log10M200=lM200, Sigma_IC=si["S"], s_IC=max(1.0, si["S"] / SIG_PC[f]), boundary=si["boundary"], S_CD1=r["S"])
        P(f"  [{f}] {nm:8s} logM* {r['logM']:.2f} -> log M200 {lM200:.2f}: Sigma_IC {si['S']:.1f} Msun/pc^2, s_IC {d[nm]['s_IC']:.3f}{' BOUNDARY' if si['boundary'] else ''}; CD1 measured S {r['S']:.3f}")
    sv = {k: v["s_IC"] for k, v in d.items()}
    if all(abs(x - 1.0) < 1e-12 for x in sv.values()): lab = "DWARFS INACTIVE"
    elif min(sv["Draco"], sv["Sextans"]) > max(sv["Fornax"], sv["Leo I"]): lab = "ORDER RIGHT"
    elif min(sv["Fornax"], sv["Leo I"]) > max(sv["Draco"], sv["Sextans"]): lab = "ORDER WRONG"
    else: lab = "MIXED"
    raw = {k: v["Sigma_IC"] for k, v in d.items()}
    rawlab = ("right" if min(raw["Draco"], raw["Sextans"]) > max(raw["Fornax"], raw["Leo I"]) else
              "wrong" if min(raw["Fornax"], raw["Leo I"]) > max(raw["Draco"], raw["Sextans"]) else "mixed")
    DW[f] = dict(rows=d, label=lab, unfloored_order=rawlab)
    P(f"  [{f}] label: {lab} (unfloored Sigma_IC order: {rawlab})")
RES["dwarfs"] = DW

# ------------------------------------------------------------------ verdict + checks
RES["verdict_per_footing"] = VERD
RES["verdict"] = VERD["canonical"] if VERD["canonical"] == VERD["alt"] else f"UNDECIDED (footings disagree: {VERD})"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
for f in FEET:
    FR = RES["footings"][f]
    P(f"  [{f}] IC1 failing: {FR['IC1']['failing'] or 'none'}; groups {FR['IC1']['groups']['verdict']} (Z {FR['IC1']['groups']['Z']:+.2f}); "
      f"IC2 (borrowed) failing: {FR['IC2']['failing'] or 'none'}; groups {FR['IC2']['groups']['verdict']} (Z {FR['IC2']['groups']['Z']:+.2f})")
checks.append(("K5", rss() < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"ic1_inner_column{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"ic1_inner_column_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
