#!/usr/bin/env python3
"""X59_formation_epoch_switch: cold dark energy is retained by an object only if eta Sigma_coll(M, z_c) > a0(z_c)/(2 pi G)
at its EPS collapse epoch (hypothesis FE). Retention by class, forest R1, EPS Monte Carlo early capture.

Frozen criteria + ledger: FROZEN_CRITERIA.md, ASSUMPTION_LEDGER.md (6c7210abf1, committed alone). EM1's code up to its halo
profiles (CLASS backgrounds) and X30's cluster machinery up to STEP 0 are executed read-only (as X41/X43); X30's log goes
to x59_x30_machinery*.log here. One thread.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x59_fe_switch.py                       -> .out, _results.json (exit 0)
    X59_MUTATE=reverse PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x59_fe_switch.py    -> K1 must fail (exit 1)
    X59_MUTATE=a0x10   PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x59_fe_switch.py    -> K1, K1b must fail (exit 1)
"""
import os, sys, json, math, time, resource, io, contextlib, csv
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X30_MUTATE", None)
import numpy as np
from scipy.optimize import brentq
from scipy.special import erfc

T0 = time.time()
MUT = os.environ.get("X59_MUTATE", "").strip()
assert MUT in ("", "reverse", "a0x10"), MUT
TAG = f"_MUTATE_{MUT}" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
LANES = os.path.join(REPO, "campaign_fresh_gravity")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

# ------------------------------------------------------------------ EM1 (read-only, up to halo profiles: includes CLASS backgrounds)
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
codeE = TE[:TE.index("# ---------------- halo profiles")]
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(codeE, EM1SRC, "exec"), NE)
sys.argv = argv0
GALS, A0, BGSE = NE["GALS"], NE["A0"], NE["BGS"]
GE, MSUNE = NE["G"], NE["MSUN"]
# ------------------------------------------------------------------ X30 (read-only, up to STEP 0)
X30SRC = os.path.join(REB, "X30_sheet_cluster_profile", "x30_sheet_cluster_profile.py"); TX = open(X30SRC).read()
codeX = TX[:TX.index("# ============================================================== STEP 0")]
old = 'OUTF = open(os.path.join(HERE, f"x30_sheet_cluster_profile{TAG}.out"), "w")'; assert codeX.count(old) == 1
codeX = codeX.replace(old, f'OUTF = open({os.path.join(HERE, "x59_x30_machinery" + TAG + ".log")!r}, "w")')
NX = {"__file__": X30SRC, "__name__": "x30_ro"}; sys.argv = [X30SRC]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(codeX, X30SRC, "exec"), NX)
sys.argv = argv0
FEET, HK, ALLI, N, prep, PREP = (NX[k] for k in ("FEET", "HK", "ALLI", "N", "prep", "PREP"))
P(f"X59_formation_epoch_switch  {('MUTATE run: ' + MUT) if MUT else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy is not matter; FE: retained iff eta Sigma_coll(M, z_c) > a0(z_c)/(2 pi G); not theory closed")
P(f"EM1 and X30 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
checks = []
def chk(name, ok, msg):
    checks.append((name, bool(ok))); P(f"{name} {msg}: {'PASS' if ok else 'FAIL'}")

# ------------------------------------------------------------------ EPS on background A (X41 section 1)
DC, OMEGA, DELTA = 1.686, 0.974, 18 * math.pi ** 2
B1 = 3 * math.log(2) - math.pi / 2
PC2 = (3.0857e16) ** 2
bg = BGSE["A_c2b_refit"]; cc = bg["c"]; hA = bg["h"]; RHOM0 = float(cc.Omega_m()) * 2.775e11 * hA ** 2       # Msun / Mpc^3
ZG = np.linspace(0, 30, 3001); DG = np.array([cc.scale_independent_growth_factor(z) for z in ZG]); DG /= DG[0]
LMG = np.linspace(7.0, 16.5, 191); sigf = bg["cB"].__defaults__[1]
S2G = np.array([float(sigf(10 ** l)[0]) ** 2 for l in LMG])
def s2(lm): return np.interp(lm, LMG, S2G)
def D(z): return np.interp(z, ZG, DG)
SIGPC = {f: A0[f] / (2 * math.pi * GE) * PC2 / MSUNE for f in FEET}                                       # Msun/pc^2

# X41 copy (reference, z_obs = 0) for K0 / K1 / K3
def zform41(M):
    S = math.sqrt(max(float(s2(math.log10(M / 2)) - s2(math.log10(M))), 0.0)); Df = DC / (DC + OMEGA * S)
    if Df >= 1.0: return 0.0
    return float(np.interp(-Df, -DG, ZG))
def sigma_coll41(M):
    zf = zform41(M); rho = DELTA * RHOM0 * (1 + zf) ** 3; rf = (3 * (M / 2) / (4 * math.pi * rho)) ** (1 / 3)
    return rho * rf / 1e12, zf
# generalised EPS (frozen section 0), vectorised in lm
def zform(lm, zobs):
    lm = np.asarray(lm, float); S = np.sqrt(np.maximum(s2(lm - math.log10(2)) - s2(lm), 0.0))
    Df = DC / (DC / D(zobs) + OMEGA * S)
    return np.interp(-Df, -DG, ZG), Df
def sigma_coll(lm, zobs):
    zf, _ = zform(lm, zobs); rho = DELTA * RHOM0 * (1 + zf) ** 3
    rf = (3 * (10 ** np.asarray(lm, float) / 2) / (4 * math.pi * rho)) ** (1 / 3)
    return rho * rf / 1e12, zf

# eta: X48 ng48 (primary) and c_f = 4 (variant)
X48T = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_regrade_ng48.json")))["table"]
LM48, CF48 = np.array(X48T["lgM"], float), np.array(X48T["cf"], float)
ETA4 = 4.0 / (3.0 * B1) * 4.0 ** 1.25
X48A2 = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_regrade_A2.json")))["table"]       # A2: nine-seed table (variant)
LMA2, CFA2 = np.array(X48A2["lgM"], float), np.array(X48A2["cf"], float)
def eta(lm, mode):
    if mode == "cf4": return np.full_like(np.asarray(lm, float), ETA4)
    if mode == "a2": return 4.0 / (3.0 * B1) * np.interp(lm, LMA2, CFA2) ** 1.25
    return 4.0 / (3.0 * B1) * np.interp(lm, LM48, CF48) ** 1.25

# F(z): M-DEC table (CFG223) + CPL continuation
J223 = json.load(open(os.path.join(LANES, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))
ZC = np.array(J223["curves"]["z"], float); MDEC = np.array(J223["curves"]["M-DEC"], float)
W0, WA = -0.838, -0.62
def F_cpl(z):
    a = 1.0 / (1.0 + np.asarray(z, float)); return np.sqrt(a ** (-3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a)))
def F(z, mode):
    z = np.asarray(z, float)
    if mode == "flat": f = np.ones_like(z)
    else: f = np.where(z <= ZC[-1], np.interp(z, ZC, MDEC), F_cpl(z))
    return f * (10.0 if MUT == "a0x10" else 1.0)

def FE(lm, zobs, foot, em, fm):
    """returns (retained, z_c, ratio = eta Sigma_coll / Sigma_a0(z_c))"""
    sc, zf = sigma_coll(lm, zobs); lhs = eta(lm, em) * sc; rhs = SIGPC[foot] * F(zf, fm)
    ret = (lhs < rhs) if MUT == "reverse" else (lhs > rhs)
    return ret, zf, lhs / rhs
COMBOS = [("x48", "mdec"), ("x48", "flat"), ("cf4", "mdec"), ("cf4", "flat")]
COMBOS_A2 = COMBOS + [("a2", "mdec"), ("a2", "flat")]
PRIMARY = ("x48", "mdec")
def cname(c): return f"c_f {dict(x48='X48 ng48', cf4='4', a2='X48 A2 nine-seed')[c[0]]} / F {'M-DEC' if c[1] == 'mdec' else 'flat'}"

# ------------------------------------------------------------------ K0, K2, K3
X41J = json.load(open(os.path.join(REB, "X41_collapse_floor_sigma", "x41_collapse_floor_results.json")))["sigma_coll_table"]
d0 = [abs(sigma_coll41(10.0 ** l)[0] / X41J[f"1e{l}"][0] - 1) for l in (11, 12, 13, 14, 15)]
tab = [round(sigma_coll41(10.0 ** l)[0], 1) for l in (11, 12, 13, 14, 15)]
k0 = max(d0) < 1e-6 and tab == [3.8, 6.8, 11.9, 20.5, 34.7] and abs(zform41(1e12) - 0.94) < 0.005 and abs(ETA4 - 14.83) < 0.005
chk("K0", k0, f"X41 Sigma_coll table {tab} (max rel dev vs X41 JSON {max(d0):.1e}); z_f(1e12) {zform41(1e12):.3f}; eta(c_f 4) {ETA4:.4f}")
w6 = ZC <= 6.0 + 1e-12; dF = float(np.max(np.abs(MDEC[w6] - F_cpl(ZC[w6]))))
Fv = [float(np.interp(z, ZC, MDEC)) for z in (1.0, 2.0, 3.0)]
k2 = dF < 2e-3 and all(abs(a - b) <= 0.002 for a, b in zip(Fv, (0.9889, 0.8739, 0.7750)))
chk("K2", k2, f"M-DEC vs CPL closed form max |dF| {dF:.1e} on [0, 6]; F(1, 2, 3) = {Fv[0]:.4f}, {Fv[1]:.4f}, {Fv[2]:.4f}")
d3 = max(abs(float(zform(l, 0.0)[0]) - zform41(10.0 ** l)) for l in (11, 12, 13, 14, 15))
lt = 12.0; zf2, Df2 = zform(lt, 2.0); Sx = math.sqrt(float(s2(lt - math.log10(2)) - s2(lt)))
res3 = abs(DC / float(D(float(zf2))) - (DC / float(D(2.0)) + OMEGA * Sx))
chk("K3", d3 < 1e-9 and res3 < 1e-3, f"generalised EPS at z_obs 0 vs X41 max |dz_f| {d3:.1e}; z_obs 2 equation residual {res3:.1e} (z_f {float(zf2):.3f})")
P(f"Sigma_a0 = a0/(2 pi G): canonical {SIGPC['canonical']:.1f}, alt {SIGPC['alt']:.1f} Msun/pc^2; M-DEC F(z) at 0 / 0.5 / 1 / 2 / 3 / 6 / 10: "
  + " / ".join(f"{float(F(z, 'mdec')):.3f}" for z in (0, 0.5, 1, 2, 3, 6, 10)))

# ------------------------------------------------------------------ systems
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
aR, bR = EM1J["rows"]["A_c2b_refit"]["R1"]["a"], EM1J["rows"]["A_c2b_refit"]["R1"]["b"]
def lm200(lMb): return aR + bR * (np.asarray(lMb, float) - 10.0)
SYS = {}
SYS["SPARC"] = {f: dict(lm=lm200([q["lMb"] for q in GALS])) for f in FEET}
TIAN = os.path.join(os.path.dirname(REPO), "_external_data", "vizier2026", "J_A_A_710_L39.tsv")
glM = []
for l in open(TIAN):
    if l.startswith("#"): continue
    r = l.rstrip("\n").split("\t")
    if len(r) < 13 or not r[0].strip().isdigit() or r[1].strip() != "Galaxy group": continue
    glM.append(float(r[7]))
SYS["groups"] = {f: dict(lm=lm200(glM)) for f in FEET}
SYS["clusters"] = {}
for f in FEET:
    ls_ = []
    for hk in HK:
        for i in ALLI:
            pp = prep(int(i), f, hk); ls_.append(math.log10((pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE))
        PREP.clear()
    SYS["clusters"][f] = dict(lm=np.array(ls_))
P(f"systems: SPARC {len(GALS)}, groups {len(glM)}, cluster cells {len(SYS['clusters']['canonical']['lm'])} per footing [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
# dwarfs: X51's halo() re-implemented with X51's constants
G51, MSUN51, MPC51 = 6.67430e-11, 1.98847e30, 3.0856775814913673e22
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
p3 = F3["A_c2b_refit"]["params"]; h3 = p3["h"]
RHOC51 = 3 * (100 * h3 * 1e3 / MPC51) ** 2 / (8 * math.pi * G51); RHOM51 = (p3["omega_b"] + p3["omega_cdm"]) / h3 ** 2 * RHOC51
KB, MP = 1.380649e-23, 1.67262192e-27
def Tvir(Mkg, z, mu):
    rho = 18 * math.pi ** 2 * RHOM51 * (1 + z) ** 3; rv = (3 * Mkg / (4 * math.pi * rho)) ** (1 / 3)
    return mu * MP * (G51 * Mkg / rv) / (2 * KB)
MCOOL = math.exp(brentq(lambda l: math.log(Tvir(math.exp(l), 8.0, 0.59) / 1e4), math.log(1e30), math.log(1e45), xtol=1e-14))
CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
SYS["dwarfs"] = {}
for f in FEET:
    rr = [r for r in X1 if r["footing"] == f and r["cls"] in CLS]
    M2 = [max(10 ** (aR + bR * (float(r["logMstar"]) - 10)) * MSUN51, MCOOL) / MSUN51 for r in rr]
    SYS["dwarfs"][f] = dict(lm=np.log10(M2), cls=[r["cls"] for r in rr], floor=[abs(m * MSUN51 / MCOOL - 1) < 1e-9 for m in M2])
X51J = json.load(open(os.path.join(REB, "X51_dwarf_cooling_floor", "x51_dwarfs_results.json")))["footings"]["canonical"]["classes"]
dd = SYS["dwarfs"]["canonical"]
d5 = max(abs(float(np.median([10 ** l for l, c in zip(dd["lm"], dd["cls"]) if c == k])) / X51J[k]["M200"] - 1) for k in CLS)
k5 = d5 < 1e-6 and len(GALS) == 175 and len(glM) == 63 and len(dd["lm"]) == 82
chk("K5", k5, f"X51 per-class median M200 max rel dev {d5:.1e}; counts SPARC {len(GALS)}, groups {len(glM)}, dwarfs {len(dd['lm'])}; M_cool {MCOOL / MSUN51:.3e}")

# ------------------------------------------------------------------ K1 identity and K1b crossover
def x43flag(lm, foot, em):
    return np.array([eta(l, em) * sigma_coll41(10 ** l)[0] > SIGPC[foot] for l in np.atleast_1d(lm)])
mism = 0; ntot = 0
for f in FEET:
    for em in ("x48", "cf4"):
        for cl in ("SPARC", "groups", "clusters", "dwarfs"):
            lm = SYS[cl][f]["lm"]; a = FE(lm, 0.0, f, em, "flat")[0]; b = x43flag(lm, f, em)
            mism += int(np.sum(a != b)); ntot += len(lm)
chk("K1", mism == 0, f"FE (flat F, z_obs 0) vs X43 flag eta Sigma_coll > Sigma_a0: {mism} mismatches of {ntot} system-evaluations")
XO = {}
for f in FEET:
    for em in ("cf4", "x48"):
        try: XO[(f, em)] = brentq(lambda l: float(eta(l, em) * sigma_coll(l, 0.0)[0] - SIGPC[f] * F(sigma_coll(l, 0.0)[1], "flat")), 8.0, 16.0)
        except ValueError: XO[(f, em)] = float("nan")                    # no crossover in 1e8-1e16 (reachable only in MUTATE a0x10)
k1b = abs(XO[("canonical", "cf4")] - 12.09) <= 0.005 and abs(XO[("alt", "cf4")] - 12.43) <= 0.005
chk("K1b", k1b, f"crossover (flat, z_obs 0) c_f 4: 10^{XO[('canonical', 'cf4')]:.3f} / 10^{XO[('alt', 'cf4')]:.3f} (X43 12.09 / 12.43)")
P(f"  reported: X48 ng48 c_f crossover 10^{XO[('canonical', 'x48')]:.3f} / 10^{XO[('alt', 'x48')]:.3f} (X58 uncommitted printout 10.83 / 11.16; no check weight)")
RES = dict(lane="X59_formation_epoch_switch", frozen="6c7210abf1", mutate=MUT or None,
           Sigma_a0_Msun_pc2=SIGPC, crossover_z0_flat={f"{f}|{em}": XO[(f, em)] for (f, em) in XO}, footings={})

# ------------------------------------------------------------------ (a) retention by class
def retention(f, c):
    em, fm = c; out = {}
    for cl in ("SPARC", "groups", "clusters"):
        lm = SYS[cl][f]["lm"]; r, zc, ra = FE(lm, 0.0, f, em, fm)
        out[cl] = dict(N=int(len(lm)), retained=int(r.sum()), frac=float(r.mean()), zc_median=float(np.median(zc)), ratio_median=float(np.median(ra)))
    dw = SYS["dwarfs"][f]; r, zc, ra = FE(dw["lm"], 0.0, f, em, fm)
    # variant: z_c = 8 for dwarfs on the cooling floor (half-mass object at z 8)
    lmv = np.asarray(dw["lm"]); zc8 = np.where(dw["floor"], 8.0, zc)
    rho = DELTA * RHOM0 * (1 + zc8) ** 3; sc8 = rho * (3 * (10 ** lmv / 2) / (4 * math.pi * rho)) ** (1 / 3) / 1e12
    ra8 = eta(lmv, em) * sc8 / (SIGPC[f] * F(zc8, fm)); r8 = (ra8 < 1) if MUT == "reverse" else (ra8 > 1)
    for k in CLS:
        m = np.array([c_ == k for c_ in dw["cls"]])
        out[f"dwarfs|{k}"] = dict(N=int(m.sum()), retained=int(r[m].sum()), frac=float(r[m].mean()), zc_median=float(np.median(zc[m])),
                                  ratio_median=float(np.median(ra[m])), frac_zc8=float(r8[m].mean()), ratio_median_zc8=float(np.median(ra8[m])))
    return out

# ------------------------------------------------------------------ (b) forest R1 and m_FE(z)
X22 = json.load(open(os.path.join(REB, "X22_cosmic_dust_window", [x for x in os.listdir(os.path.join(REB, "X22_cosmic_dust_window"))
                                                                     if x.endswith("results.json") and "MUTATE" not in x][0])))
MHM = float(X22["step1"]["alpha_NF"]["M_hm_Msun"]); MPASS = float(X22["step1"]["alpha_PASS"]["M_hm_Msun"])
FMAX = {f: float(X22["step2"]["per_footing"][f]["f_max"]) for f in FEET}
LMRES = math.log10(2e7)
LMT = np.round(np.arange(LMRES, 16.0 + 1e-9, 0.01), 6)
def mfe(zobs, f, c):
    r = FE(LMT, zobs, f, c[0], c[1])[0]
    if not r.any(): return None, True
    j = int(np.argmax(r)); return float(LMT[j]), bool(r[j:].all())

# ------------------------------------------------------------------ (c) EPS Monte Carlo early capture
ZZ = np.round(np.arange(0.0, 10.0 + 1e-9, 0.05), 6); BZ = DC / D(ZZ)
BZE = BZ - 0.5826 * math.sqrt(0.01)      # A1: Broadie-Glasserman-Kou continuity correction for discrete monitoring (crossing search only)
DS, NW, BLK = 0.01, 20000, 200     # A2: block 200 rows (same row-major random stream as 1000; memory only)
SRES = float(s2(LMRES))
LM_OF_S = lambda S: np.interp(-S, -S2G, LMG)            # S2G decreasing in lm
FET = {}                                                  # (f, c) -> bool table [iz, j] on LMT
for f in FEET:
    for c in COMBOS_A2:
        FET[(f, c)] = np.array([FE(LMT, z, f, c[0], c[1])[0] for z in ZZ])
def walks(lM0, seed_off):
    """yield per-block (k-index of first crossing per z (len -> none), S grid)"""
    S0 = float(s2(lM0)); n = int(math.ceil((SRES - S0) / DS)); Sg = S0 + DS * np.arange(n + 1)
    rng = np.random.default_rng(20261027 + seed_off)
    for b in range(NW // BLK):
        dl = np.empty((BLK, n + 1)); dl[:, 0] = DC
        dl[:, 1:] = DC + np.cumsum(rng.standard_normal((BLK, n)) * math.sqrt(DS), axis=1)
        rm = np.maximum.accumulate(dl, axis=1); del dl
        K = np.empty((BLK, len(ZZ)), dtype=np.int64)
        for w in range(BLK): K[w] = np.searchsorted(rm[w], BZE, side="left")
        del rm
        yield K, Sg
def run_host(lM0, seed_off, keyset, keep=False):
    acc = {k: dict(ever=0, single=np.zeros(len(ZZ)), zfirst=[]) for k in keyset}; ktest = []
    for K, Sg in walks(lM0, seed_off):
        ok = K < len(Sg); Kc = np.minimum(K, len(Sg) - 1)
        lmz = np.where(ok, LM_OF_S(Sg[Kc]), LMT[0] - 1.0)
        j = np.clip(np.round((lmz - LMT[0]) / 0.01).astype(np.int64), 0, len(LMT) - 1)
        for k in keyset:
            tab_ = FET[k]; cap = ok & (lmz >= LMT[0] - 1e-9) & tab_[np.arange(len(ZZ))[None, :], j]
            acc[k]["ever"] += int(cap.any(axis=1).sum()); acc[k]["single"] += cap.sum(axis=0)
        if keep: ktest.append((K, Sg))
    res = {}
    for k in keyset:
        sgl = acc[k]["single"] / NW; i = int(np.argmax(sgl))
        res[k] = dict(f_EC=acc[k]["ever"] / NW, f_self=float(FE(lM0, 0.0, k[0], k[1][0], k[1][1])[0]),
                      single_max=float(sgl[i]), z_single_max=float(ZZ[i]))
    return res, ktest
keys = [(f, c) for f in FEET for c in COMBOS_A2]
# K4: Monte Carlo vs analytic single-epoch fractions (host 1e12)
_, kt = run_host(12.0, 0, [], keep=True)
S0t = float(s2(12.0)); dev = []
for (lmm, z) in ((10.0, 1.0), (9.0, 2.0), (11.0, 0.5)):
    iz = int(round(z / 0.05)); Sm = float(s2(lmm))
    mc = sum(int(np.sum((K[:, iz] < len(Sg)) & (Sg[np.minimum(K[:, iz], len(Sg) - 1)] <= Sm))) for K, Sg in kt) / NW
    an = float(erfc((BZ[iz] - DC) / math.sqrt(2 * (Sm - S0t)))); dev.append((lmm, z, mc, an))
del kt
chk("K4", max(abs(a - b) for _, _, a, b in dev) < 0.02, "MC vs analytic f(>m, z | 1e12): " + "; ".join(f"m 1e{l:g} z {z}: {a:.4f} vs {b:.4f}" for l, z, a, b in dev))
P(f"[{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
lmb_med = float(np.median([q["lMb"] for q in GALS])); LM_MED = float(lm200(lmb_med)); LM_MW = float(lm200(math.log10(6.0e10)))
HOSTS = [round(x, 2) for x in np.arange(10.0, 13.0 + 1e-9, 0.25)]
MC = {}
for ih, lh in enumerate(HOSTS + [LM_MED, LM_MW]):
    MC[lh], _ = run_host(lh, 1 + ih, keys)
P(f"Monte Carlo done: {len(HOSTS) + 2} hosts x {NW} walks [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ grading
def grade(f, c):
    ret = retention(f, c)
    r1 = {z: FE(math.log10(MHM), z, f, c[0], c[1]) for z in (2.0, 2.5, 3.0)}
    r1pass = all(bool(v[0]) for v in r1.values())
    gl = [float(np.interp(l, HOSTS, [MC[h][(f, c)]["f_EC"] for h in HOSTS])) for l in SYS["SPARC"][f]["lm"]]
    fmed = MC[LM_MED][(f, c)]["f_EC"]; ec_fail = fmed > FMAX[f]
    pat = dict(SPARC=ret["SPARC"]["frac"] <= 0.10, groups=ret["groups"]["frac"] >= 0.50, clusters=ret["clusters"]["frac"] >= 0.90)
    for k in CLS: pat[f"dwarfs|{k}"] = ret[f"dwarfs|{k}"]["frac"] >= 0.50
    miss = [k for k, v in pat.items() if not v]
    if not r1pass or ec_fail:
        v = " + ".join(([] if r1pass else ["FE FAILS R1 (forest)"]) + (["FE FAILS BY EARLY CAPTURE (galaxy progenitors keep too much)"] if ec_fail else []))
    elif not miss:
        v = "FE REPRODUCES THE PATTERN AND PASSES R1"
    else:
        v = f"UNDECIDED (pattern miss: {', '.join(miss)})"
    mf = {z: mfe(z, f, c) for z in (0.0, 1.0, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0)}
    return dict(retention=ret, R1={str(z): dict(retained=bool(v_[0]), z_c=float(v_[1]), ratio=float(v_[2])) for z, v_ in r1.items()}, R1_pass=r1pass,
                M_hm=MHM, f_EC_median_SPARC_galaxy=fmed, f_EC_SPARC_median_of_galaxies=float(np.median(gl)),
                f_EC_MW=MC[LM_MW][(f, c)]["f_EC"], f_self_median=MC[LM_MED][(f, c)]["f_self"], f_self_MW=MC[LM_MW][(f, c)]["f_self"],
                single_epoch_max_median=MC[LM_MED][(f, c)]["single_max"], z_single_max_median=MC[LM_MED][(f, c)]["z_single_max"],
                f_max_X22=FMAX[f], EC_fail=ec_fail, pattern=pat, pattern_miss=miss,
                m_FE={str(z): dict(lm=v_[0], interval=v_[1]) for z, v_ in mf.items()},
                f_EC_hosts={str(h): MC[h][(f, c)]["f_EC"] for h in HOSTS}, verdict=v)
P(f"\nmedian SPARC galaxy: log M_b {lmb_med:.3f} -> log M200 {LM_MED:.3f}; MW: M_b 6.0e10 -> log M200 {LM_MW:.3f}; forest M_hm {MHM:.3e} (alpha_PASS {MPASS:.3e})")
for f in FEET:
    RES["footings"][f] = {}
    for c in COMBOS:
        g = grade(f, c); RES["footings"][f][cname(c)] = g
        P(f"\n=== [{f}] {cname(c)}{'  (PRIMARY)' if c == PRIMARY else '  (variant)'}")
        rt = g["retention"]
        P("  retention: " + "; ".join(f"{k} {v['retained']}/{v['N']} ({v['frac']:.2f})" for k, v in rt.items()))
        P("    median z_c / ratio: " + "; ".join(f"{k} {v['zc_median']:.2f} / {v['ratio_median']:.2f}" for k, v in rt.items()))
        P("    dwarfs z_c = 8 variant (frac / ratio): " + "; ".join(f"{k} {rt['dwarfs|' + k]['frac_zc8']:.2f} / {rt['dwarfs|' + k]['ratio_median_zc8']:.2f}" for k in CLS))
        P("  R1 forest M_hm: " + "; ".join(f"z {z}: {'retained' if v['retained'] else 'NOT'} (z_c {v['z_c']:.2f}, ratio {v['ratio']:.2f})" for z, v in g["R1"].items())
          + f" -> {'PASS' if g['R1_pass'] else 'FAIL'}")
        P("  m_FE(z_obs): " + "; ".join(f"z {z}: " + (f"10^{v['lm']:.2f}" if v["lm"] is not None else "none") + ("" if v["interval"] else " (non-monotone)") for z, v in g["m_FE"].items()))
        P(f"  early capture: median SPARC galaxy f_EC {g['f_EC_median_SPARC_galaxy']:.3f} (f_self {g['f_self_median']:.0f}; single-epoch max {g['single_epoch_max_median']:.3f} at z {g['z_single_max_median']:.2f}); "
          f"SPARC median of galaxies {g['f_EC_SPARC_median_of_galaxies']:.3f}; MW {g['f_EC_MW']:.3f} (f_self {g['f_self_MW']:.0f}); X22 f_max {g['f_max_X22']:.4f} -> {'FAIL' if g['EC_fail'] else 'pass'}")
        P("    f_EC by host log M0: " + ", ".join(f"{h}: {v:.3f}" for h, v in g["f_EC_hosts"].items()))
        P(f"  pattern miss: {g['pattern_miss'] or 'none'}")
        P(f"  CLASS [{f}] {cname(c)}: {g['verdict']}")
V = {f: RES["footings"][f][cname(PRIMARY)]["verdict"] for f in FEET}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
P(f"\n=== VERDICT (frozen section 2, PRIMARY c_f X48 ng48 / M-DEC, both footings): {RES['verdict']}")

# ------------------------------------------------------------------ A2: coordinator band gate (post-hoc, disclosed)
BANDS = dict(dwarfs=(8.0, 10.0), Lstar=(11.35, 12.05), groups_clusters=(13.0, 15.0))
def band_gate(f, c):
    out = {}
    for b, (lo, hi) in BANDS.items():
        g = np.round(np.arange(lo, hi + 1e-9, 0.05), 6); r, zc, ra = FE(g, 0.0, f, c[0], c[1])
        d = dict(frac_retained=float(r.mean()), ratio_min=float(ra.min()), ratio_max=float(ra.max()), zc_range=[float(zc.min()), float(zc.max())])
        if b == "dwarfs":
            rho = DELTA * RHOM0 * 9.0 ** 3; sc8 = rho * (3 * (10 ** g / 2) / (4 * math.pi * rho)) ** (1 / 3) / 1e12
            ra8 = eta(g, c[0]) * sc8 / (SIGPC[f] * F(8.0, c[1])); r8 = (ra8 < 1) if MUT == "reverse" else (ra8 > 1)
            d.update(frac_retained_zc8=float(r8.mean()), ratio8_min=float(ra8.min()), ratio8_max=float(ra8.max()))
            d["holds"] = bool(r.all())
        elif b == "Lstar":
            fec = np.array([float(np.interp(l, HOSTS, [MC[h][(f, c)]["f_EC"] for h in HOSTS])) for l in g])
            d.update(f_self_any=bool(r.any()), f_EC_min=float(fec.min()), f_EC_max=float(fec.max()), f_max=FMAX[f],
                     holds_rekeyed=bool(not r.any()))
            d["holds"] = bool((not r.any()) and fec.max() <= FMAX[f])
        else:
            d["holds"] = bool(r.all())
        out[b] = d
    miss = [b for b, d in out.items() if not d["holds"]]
    out["verdict"] = "FE BAND GATE PASSES" if not miss else f"FE BAND GATE FAILS ({', '.join(miss)})"
    return out
RES["A2_band_gate"] = {}
for f in FEET:
    RES["A2_band_gate"][f] = {}
    for c in [("cf4", "mdec"), ("cf4", "flat"), ("x48", "mdec"), ("x48", "flat"), ("a2", "mdec"), ("a2", "flat")]:
        bg_ = band_gate(f, c); RES["A2_band_gate"][f][cname(c)] = bg_
        d, l_, gc = bg_["dwarfs"], bg_["Lstar"], bg_["groups_clusters"]
        P(f"A2 [{f}] {cname(c)}{'  (A2 PRIMARY)' if c == ('cf4', 'mdec') else ''}: dwarfs 1e8-1e10 retained {d['frac_retained']:.2f} (ratio {d['ratio_min']:.2f}-{d['ratio_max']:.2f}; z_c {d['zc_range'][0]:.2f}-{d['zc_range'][1]:.2f}; z_c 8 variant {d['frac_retained_zc8']:.2f}, ratio {d['ratio8_min']:.2f}-{d['ratio8_max']:.2f}); "
          f"L* self-retained {l_['frac_retained']:.2f} (ratio {l_['ratio_min']:.2f}-{l_['ratio_max']:.2f}), f_EC {l_['f_EC_min']:.3f}-{l_['f_EC_max']:.3f} vs f_max {l_['f_max']:.4f}, re-keyed excluded {l_['holds_rekeyed']}; "
          f">=1e13 retained {gc['frac_retained']:.2f} (ratio {gc['ratio_min']:.2f}-{gc['ratio_max']:.2f}) -> {bg_['verdict']}")
VA2 = {f: RES["A2_band_gate"][f][cname(("cf4", "mdec"))]["verdict"] for f in FEET}
RES["A2_verdict"] = VA2["canonical"] if VA2["canonical"] == VA2["alt"] else f"UNDECIDED (footings disagree: {VA2})"
P(f"=== A2 BAND GATE (c_f 4 / M-DEC, both footings; post-hoc): {RES['A2_verdict']}")
chk("K6", rss() < 1.0, f"peak RSS {rss():.2f} GB")
RES["checks"] = {k: ok for k, ok in checks}
n = sum(ok for _, ok in checks)
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
if MUT:
    need = ["K1"] + (["K1b"] if MUT == "a0x10" else [])
    okm = all(not RES["checks"][k] for k in need)
    RES["mutate_named_checks_failed"] = okm
    P(f"MUTATE {MUT}: named checks {need} failed as required: {okm}")
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"x59_fe_switch{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x59_fe_switch_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
