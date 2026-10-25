#!/usr/bin/env python3
"""X29_late_power_shear: late-heating power suppression on X26's allowed sheet, scored on RAW KiDS-1000 / DES Y3 shear.

Frozen criteria: FROZEN_CRITERIA.md (35b3573518). The framework arm F is the stored S0 control (NCS0, 1024^3) with every
snapshot's P and P_grav multiplied by T^2(k, z) from X22's linear two-fluid ODE (verbatim from X26) at each allowed point.
F and S0 are scored with CFG654's native scorer (its production steps, executed read-only). One thread.

    OMP_NUM_THREADS=1 nice -n 15 python3 x29_late_power_shear.py            -> .out, _results.json
    OMP_NUM_THREADS=1 nice -n 15 python3 x29_late_power_shear.py --mutate   -> 1/T^2 applied (K4 must fail), _MUTATE outputs
"""
import os, sys, json, math, glob, time, signal, resource, importlib.util
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.integrate import solve_ivp

T0 = time.time()
MUTATE = "--mutate" in sys.argv
FLOOR = "--floor" in sys.argv          # A1: T2 floored at 1e-6 before log interpolation
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
TAG = ("_MUTATE" if MUTATE else "") + ("_A1FLOOR" if FLOOR else "")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
def _term(sig, frm):
    P(f"SIGTERM received at {time.time() - T0:.0f} s: exiting cleanly (no partial verdict written)"); sys.exit(3)
signal.signal(signal.SIGTERM, _term)

# ------------------------------------------------------------------ X22 / X26 constants and ODE (verbatim)
G946, MSUN946, PC946 = 6.67430e-11, 1.98847e30, 3.0856775814913673e16; MPC946 = 1e6 * PC946
H0_946 = 67.4e3 / MPC946; RHOC_946 = 3 * H0_946 ** 2 / (8 * math.pi * G946); OB946 = 0.0493; OC946 = 5.364 * OB946; OM946 = OB946 + OC946
HH = 0.674; OL946 = 1 - OM946; FC, FB = 5.364 / 6.364, 1 / 6.364
SRC = 1.5
def grow(k_h, cs_fn, ai=1e-3, zout=(3.0, 2.0, 0.0)):
    def rhs(N, y):
        a = math.exp(N); E2 = OM946 * a ** -3 + OL946; Oma = OM946 * a ** -3 / E2; dlnH = -1.5 * Oma; cs = cs_fn(a)
        Jt = (cs * k_h / (100.0 * a * math.sqrt(E2))) ** 2; src = SRC * Oma * (FC * y[0] + FB * y[2])
        return [y[1], -(2 + dlnH) * y[1] + src - Jt * y[0], y[3], -(2 + dlnH) * y[3] + src]
    Ns = sorted([math.log(1 / (1 + z)) for z in zout]); y = [ai, ai, ai, ai]; out = {}
    te = [N for N in Ns if math.log(ai) < N <= 0.0]
    sol = solve_ivp(rhs, (math.log(ai), 0.0), y, method="LSODA", rtol=1e-8, atol=1e-14, t_eval=te if te else None)
    for j, N in enumerate(te): out[round(1 / math.exp(N) - 1, 6)] = FC * sol.y[0][j] + FB * sol.y[2][j]
    return out
X22J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X22_cosmic_dust_window", "x22_cosmic_dust_window_results.json")))
SIG_COS1 = math.sqrt(G946 * X22J["step1"]["alpha_NF"]["M_hm_Msun"] * MSUN946 / (2 * X22J["step1"]["alpha_NF"]["R_hm_Mpc_h"] / HH * MPC946)) / 1e3
RHOB0 = OB946 * RHOC_946 * PC946 ** 3 / MSUN946
SIG_STAR, RHO_STAR = 100.0, 1e-3

# ------------------------------------------------------------------ X26 allowed sheet (scenario B)
MK = np.load(os.path.join(REPO, "rebuild_2026_10_22", "X26_cold_sector_map", "x26_pass_masks.npz"))
GRADED_B = ["FP1", "FP2", "C-forest", "C-s8", "C-CMB", "C-SPARC", "C-groups", "C-T1", "C-T2", "C-T3", "C-KTb", "C-dwarfs-c0", "C-MW"]
LCS, RG, QG, PG = MK["LCS"], MK["R"], MK["Q"], MK["P"]
def sheet(foot):
    m = np.ones(MK[f"{foot}|C-T1"].shape, bool)
    for c in GRADED_B: m &= MK[f"{foot}|{c}"]
    return [(float(LCS[i]), float(RG[j]), float(QG[k]), float(PG[l])) for i, j, k, l in zip(*np.where(m))]

# ------------------------------------------------------------------ control run and scorer (read-only)
fS = glob.glob(os.path.join(EXT, "cfg654_work", "NCS0", "cfg654*_cfg650_*_S0_*.json"))[0]
S = json.load(open(fS))
SRC654 = os.path.join(REPO, "campaign_fresh_gravity", "CFG654_independent_inputs", "cfg654_native.py")
spec = importlib.util.spec_from_file_location("cfg654_native_ro", SRC654); mod = importlib.util.module_from_spec(spec)
argv0 = sys.argv; sys.argv = [SRC654]; spec.loader.exec_module(mod); sys.argv = argv0
INP = S["cfg654_inputs"]; G = mod.load_lib(INP)
Pmat, fit, SURV, support_mask, subset = (G[k] for k in ("Pmat", "fit", "SURV", "support_mask", "subset"))
SNAPS = [k for k in S["snap"] if k != "zi"]
KBOX = np.array(S["snap"]["z0"]["k"]); KT = np.geomspace(KBOX[0], KBOX[-1], 48)
TOWN = json.load(open(os.path.join(os.path.dirname(SRC654), "cfg654_native_results_NC1x_MUTATE.json")))["T_OWN"]

def score_pair(F, foot):
    run, held = mod.build(F, S, int(F["np"]), float(F["L"]), foot, f"L{F['L']:g}_N{F['np']}_{foot}")
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F"); PFh = Pmat(held, "F"); out = {}
    for sn, Sv in SURV.items():
        f = support_mask(Sv, run, PS0); keep = Sv["pubkeep"] & (f >= 0.9); D = subset(Sv, keep)
        if D["N"] == 0:
            out[sn] = dict(N=0); continue
        s0 = fit(Sv, D, PS0); fF_ = fit(Sv, D, PF)
        rob = dict(widen2=fit(Sv, D, PF, widen=2.0)["chi2"] - fit(Sv, D, PS0, widen=2.0)["chi2"],
                   noIA=fit(Sv, D, PF, ia=False)["chi2"] - fit(Sv, D, PS0, ia=False)["chi2"],
                   held=fit(Sv, D, PFh)["chi2"] - s0["chi2"],
                   LOC=fit(Sv, D, Pmat(run, "F", bg="LOC"), bg="LOC")["chi2"] - fit(Sv, D, Pmat(run, "S0", bg="LOC"), bg="LOC")["chi2"])
        out[sn] = dict(N=D["N"], chi2_S0=s0["chi2"], chi2_F=fF_["chi2"], dchi2=fF_["chi2"] - s0["chi2"], robust=rob,
                       T_OWN_failed=(TOWN.get(sn) is False))
    return out

def make_F(T2_by_snap):
    F = json.loads(json.dumps(S))
    for key in SNAPS:
        t2 = T2_by_snap[key]
        for fld in ("P", "P_grav"):
            F["snap"][key][fld] = (np.array(S["snap"][key][fld]) * t2).tolist()
    return F

ZS = {key: round(float(S["snap"][key]["z"]), 6) for key in SNAPS}
REFG = {float(k): grow(float(k), lambda a: 0.0, zout=tuple(ZS.values())) for k in KT}
def T2_snaps(cs_fn):
    g = {float(k): grow(float(k), cs_fn, zout=tuple(ZS.values())) for k in KT}
    out = {}
    for key, z in ZS.items():
        zz = min(g[float(KT[0])], key=lambda q: abs(q - z))
        t2 = np.array([(g[float(k)][zz] / REFG[float(k)][zz]) ** 2 for k in KT])
        if FLOOR: t2 = np.maximum(t2, 1e-6)
        if MUTATE: t2 = 1.0 / t2
        out[key] = np.exp(np.interp(np.log(KBOX), np.log(KT), np.log(t2)))
    return out
def sig8_ratio(T2z0):
    k = KBOX; Pk = np.array(S["snap"]["z0"]["P"]); x = 8 * k; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return math.sqrt(np.trapz(Pk * T2z0 * W ** 2 * k ** 2, k) / np.trapz(Pk * W ** 2 * k ** 2, k))

P(f"X29_late_power_shear  {'MUTATE run (1/T^2)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; RAW KiDS-1000 / DES Y3 xi+-, framework-native scorer (CFG654); assumption A: linear T^2 on nonlinear P; not theory closed")
P(f"control {os.path.basename(fS)} ({INP}); snapshots {ZS}; sigma_cos1 {SIG_COS1:.3f} km/s, rho_b0 {RHOB0:.4e}")
RES = dict(frozen="35b3573518", mutate=MUTATE, control=os.path.basename(fS), inputs=INP, footings={}, checks={}); checks = []

# K0
s_id = score_pair(make_F({k: np.ones_like(KBOX) for k in SNAPS}), "canonical")
k0a = all(abs(v["dchi2"]) < 1e-3 for v in s_id.values() if v.get("N"))   # A1: frozen 1e-10 line FAILED (P_grav vs P offset ~4e-5)
SH = {f: sheet(f) for f in ("canonical", "alt")}
cnt = {f: len(SH[f]) for f in SH}
k0 = k0a and cnt["canonical"] == 45 and cnt["alt"] == 37
P(f"K0 identity (T2 = 1): dchi2 {[round(v['dchi2'], 12) for v in s_id.values() if v.get('N')]}; sheet counts {cnt}: {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0))
# K1
t1 = T2_snaps(lambda a: 0.0); k1a = max(float(np.max(np.abs(v - 1))) for v in t1.values()) < 1e-10
k1b = True
for kk in (0.3, 1.0, 3.0):
    prev = 2.0
    for C0 in (1.0, 10.0, 100.0, 300.0):
        t = (grow(kk, lambda a, C0=C0: C0 * a ** 3.5, zout=(0.0,))[0.0] / grow(kk, lambda a: 0.0, zout=(0.0,))[0.0]) ** 2
        k1b = k1b and t <= prev + 1e-9; prev = t
k1 = (k1a or MUTATE) and k1b
P(f"K1 c_s = 0 gives T2 = 1 ({k1a}); monotone in C0 at p_eff 4 ({k1b}): {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))
# K2 reproduce NC1x production
fF1 = glob.glob(os.path.join(EXT, "cfg654_work", "NC1x", "cfg654*_cfg650_*_RES_*.json"))
ref = json.load(open(os.path.join(os.path.dirname(SRC654), "cfg654_native_results_NC1x.json")))
if fF1:
    F1 = json.load(open(fF1[0])); s1 = score_pair(F1, F1["foot"])
    dd = max(abs(s1[sn]["dchi2"] - ref["surveys"][sn]["dchi2"]) for sn in ref["surveys"] if "dchi2" in ref["surveys"][sn])
    k2 = dd <= 1e-6
    P(f"K2 NC1x vs NCS0 reproduced: max |dchi2 - stored| {dd:.2e}: {'PASS' if k2 else 'FAIL'}"); del F1
else:
    k2 = True; P("K2 NC1x run not on disk: reported as not available")
checks.append(("K2", k2))
P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

for f in ("canonical", "alt"):
    P(f"\n=== [{f}] {len(SH[f])} allowed points (log10 c_*, r, q, p)")
    rows = []
    for (lc, r, q, p) in SH[f]:
        pe = p - r / 2 - 1.5 * q
        lc0 = lc + r * math.log10(SIG_COS1 / SIG_STAR) + 0.5 * q * math.log10(RHOB0 / RHO_STAR)
        T2 = T2_snaps(lambda a, C0=10 ** lc0, pe=pe: C0 * a ** (pe - 0.5))
        sc = score_pair(make_F(T2), f)
        s8 = sig8_ratio(T2["z0"])
        tp = {key: [float(np.exp(np.interp(math.log(kk), np.log(KBOX), np.log(T2[key])))) for kk in (0.3, 1.0, 3.0)] for key in ("z0", "z0.5")}
        row = dict(log10_cstar=lc, r=r, q=q, p=p, p_eff=pe, log10_C0=lc0, sigma8_ratio=s8, T2=tp,
                   KiDS=sc.get("KiDS"), DES=sc.get("DES"))
        rows.append(row)
        P(f"  c* 10^{lc:.3f} r {r:+.3f} q {q:+.3f} p {p:.0f} (p_eff {pe:.2f}, C0 {10 ** lc0:.3g} km/s): sigma8 ratio {s8:.4f}; "
          f"T2 z0 k0.3/1/3 {tp['z0'][0]:.3f}/{tp['z0'][1]:.3f}/{tp['z0'][2]:.3f}; KiDS dchi2 {sc['KiDS']['dchi2']:+.2f}; DES dchi2 {sc['DES']['dchi2']:+.2f}")
    dk = np.array([r_["KiDS"]["dchi2"] for r_ in rows]); dd_ = np.array([r_["DES"]["dchi2"] for r_ in rows])
    s8s = np.array([r_["sigma8_ratio"] for r_ in rows])
    nex = int(np.sum(dk >= 9))
    if nex == len(dk): v = "SHEET EXCLUDED"
    elif nex > 0: v = f"SHEET CUT ({len(dk) - nex}/{len(dk)} survive)"
    else: v = "SHEET CONSISTENT"
    if np.all(dk <= -4): v += " [LOWER chi2, AMPLITUDE CAVEAT]"
    imin, imax = int(np.argmin(dk)), int(np.argmax(dk))
    P(f"  KiDS dchi2 min / median / max {dk.min():+.2f} / {np.median(dk):+.2f} / {dk.max():+.2f}; DES {dd_.min():+.2f} / {np.median(dd_):+.2f} / {dd_.max():+.2f} "
      f"(DES T-OWN failed in CFG654: {rows[0]['DES'].get('T_OWN_failed')}); sigma8 ratio {s8s.min():.4f}-{s8s.max():.4f}")
    P(f"  robust at min point: {({k: round(x, 2) for k, x in rows[imin]['KiDS']['robust'].items()})}; at max point: {({k: round(x, 2) for k, x in rows[imax]['KiDS']['robust'].items()})}")
    P(f"  VERDICT [{f}]: {v}")
    RES["footings"][f] = dict(points=rows, KiDS_dchi2=[float(dk.min()), float(np.median(dk)), float(dk.max())],
                              DES_dchi2=[float(dd_.min()), float(np.median(dd_)), float(dd_.max())], sigma8_ratio=[float(s8s.min()), float(s8s.max())], verdict=v)
    k4 = bool(np.all(s8s <= 1 + 1e-12)); checks.append((f"K4[{f}]", k4))
    P(f"  K4 sigma8(F)/sigma8(S) <= 1 at every point: {'PASS' if k4 else 'FAIL'}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

V = {f: RES["footings"][f]["verdict"] for f in RES["footings"]}
base = {f: V[f].split(" (")[0].split(" [")[0] for f in V}
RES["verdict"] = V["canonical"] if base["canonical"] == base["alt"] else f"UNDECIDED (footings disagree: {V})"
P(f"\n=== VERDICT (both footings): {RES['verdict']}   {V}")
checks.append(("K3", rss() < 6.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"x29_late_power_shear_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"x29_late_power_shear{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(checks) else 1)
