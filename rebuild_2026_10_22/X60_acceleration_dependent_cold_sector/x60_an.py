#!/usr/bin/env python3
"""X60_acceleration_dependent_cold_sector: can cold dark energy / dark energy be two phases of one field, keyed on acceleration?

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (c0c90a8425, committed alone before this script).
Reads EM1 (CLASS backgrounds, sigma(M)) read-only, and the committed JSON of X41, X43, X47, X48, X22, X54. Writes only into
this folder. kappa = 1/2 FITTED; footings never pooled; cold dark energy is a gravitating w~0 field component, not matter,
not a particle; not theory closed.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x60_an.py
    X60_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x60_an.py     # must exit 1
"""
import os, sys, json, math, time, resource, io, contextlib
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline
from scipy.special import erfc
from scipy.optimize import brentq

T0 = time.time()
MUTATE = os.environ.get("X60_MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
def J(*p): return json.load(open(os.path.join(REB, *p)))
RES = dict(frozen="c0c90a8425", mutate=MUTATE, checks={})
CHK = {}
P(f"X60_acceleration_dependent_cold_sector  {'MUTATE run (m1-m4)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w~0 field component, not matter, not a particle; not theory closed")

# ------------------------------------------------------------------ EM1 read-only (CLASS backgrounds A/B, sigma(M))
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
codeE = TE[:TE.index("# ---------------- halo profiles")]
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(codeE, EM1SRC, "exec"), NE)
sys.argv = argv0
BGSE = NE["BGS"]; G = NE["G"]; MSUN = NE["MSUN"]; MPC = NE["MPC"]
F3 = J("F3_growth_audit", "f3_growth_audit_results.json")["K2"]
PC = 3.0857e16; KPC = 3.0857e19; C = 299792458.0
FEET = ("canonical", "alt"); A0 = {f: float(NE["A0"][f]) for f in FEET}          # the record's footings (EM1/C4; 9.3603e-11 / 1.1312e-10 rounded)
BGT = ("A_c2b_refit", "B_cfg886_bg")
P(f"EM1 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ committed inputs
X47 = J("X47_vacuum_tethered_core_floor", "x47_vt_floor_results.json")
X54 = J("X54_cold_de_exchange", "x54_cold_de_exchange_results.json")
X41 = J("X41_collapse_floor_sigma", "x41_collapse_floor_results.json")
X48 = J("X48_native_cf_zoom", "x48_regrade_ng48.json")
X22 = J("X22_cosmic_dust_window", "x22_cosmic_dust_window_results.json")
GT = X47["g_T"]["g_T_m_s2"]; SIG = X41["Sigma_Msun_pc2"]
LAM_HM = X22["step1"]["alpha_NF"]["lambda_hm_Mpc_h"]; K_HM = X22["step1"]["alpha_NF"]["k_hm_hMpc"]
M_HM = X22["step1"]["alpha_NF"]["M_hm_Msun"]; ML_MIN = X22["step2"]["per_footing"]["canonical"]["M_L_Msun"][0]

# ------------------------------------------------------------------ STEP 0
P("\n=== STEP 0")
# S0a: X47 task-4 table; g_T from the Burkert closed form
def Bk(x): return (math.log((1 + x * x) * (1 + x) ** 2) - 2 * math.atan(x)) / x ** 2
from scipy.optimize import minimize_scalar
r_ = minimize_scalar(lambda x: -Bk(x), bounds=(0.5, 1.5), method="bounded", options={"xatol": 1e-12})
zeta = -r_.fun / 2
gT_ok = abs(zeta - X47["g_T"]["zeta_over_a0"]) < 1e-6 and all(abs(zeta * A0[f] / GT[f] - 1) < 1e-6 for f in FEET)
P(f"  S0a g_T: zeta = {zeta:.6f} a0 (X47 {X47['g_T']['zeta_over_a0']:.6f}); g_T = {GT['canonical']:.4e} / {GT['alt']:.4e} -> {gT_ok}")
KG = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]; ZG = [0, 0.5, 1, 2, 3, 5, 10, 30]
ZPOW = 3 if MUTATE else 2                                                # m1
BG = {}
for t in BGT:
    bg = BGSE[t]; cc = bg["c"]; h = bg["h"]; p = F3[t]["params"]
    sig = bg["cB"].__defaults__[1]; kk, Pk = sig.__defaults__[0], sig.__defaults__[1]
    D2 = kk ** 3 * Pk / (2 * math.pi ** 2)
    rc = 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G)
    rhoc0 = p["omega_cdm"] * rc; rhom0 = (p["omega_cdm"] + p["omega_b"]) * rc
    zg = np.linspace(0, 40, 4001); Dg = np.array([cc.scale_independent_growth_factor(z) for z in zg]); Dg /= Dg[0]
    BG[t] = dict(cc=cc, h=h, p=p, sig=sig, kk=kk, D2=D2, rhoc0=rhoc0, rhom0=rhom0, zg=zg, Dg=Dg,
                 Om=(p["omega_cdm"] + p["omega_b"]) / h ** 2, Oc=p["omega_cdm"] / h ** 2, OL=cc.Omega_Lambda())
def Dz(t, z): return float(np.interp(z, BG[t]["zg"], BG[t]["Dg"])) if z <= 40 else None
def Dexact(t, z): c_ = BG[t]["cc"]; return c_.scale_independent_growth_factor(z) / c_.scale_independent_growth_factor(0.0)
def gk(t, k, z, rho0):
    b = BG[t]; d2 = float(np.exp(np.interp(math.log(k), np.log(b["kk"]), np.log(b["D2"]))))
    return 4 * math.pi * G * rho0 * (1 + z) ** ZPOW * Dexact(t, z) * math.sqrt(d2) / (k * b["h"] / MPC)
def sig_g(t, z, rho0, kmin=1e-4, kmax=None, R=0.0, vec=True):
    """rms linear pull (3D), comoving top-hat R (Mpc/h) applied to the vector field (vec) or none."""
    b = BG[t]; kk = b["kk"]; w = (kk >= kmin) & (kk <= (kmax if kmax else kk[-1]))
    k_ = kk[w]; kp = k_ * b["h"] / MPC
    W = np.ones_like(k_) if R <= 0 else 3 * (np.sin(k_ * R) - k_ * R * np.cos(k_ * R)) / (k_ * R) ** 3
    return 4 * math.pi * G * rho0 * (1 + z) ** ZPOW * Dexact(t, z) * math.sqrt(np.trapz(b["D2"][w] * W ** 2 / kp ** 2, np.log(k_)))
s0a_dev = 0.0
for t in BGT:
    tab = X47["task4"][t]["table_m_s2"]
    for z in ZG:
        for k in KG:
            s0a_dev = max(s0a_dev, abs(gk(t, k, z, BG[t]["rhoc0"]) / tab[str(z)][str(k)] - 1))
        s0a_dev = max(s0a_dev, abs(sig_g(t, z, BG[t]["rhoc0"], kmin=0.01) / tab[str(z)]["cum"] - 1))
S0a = bool(gT_ok and s0a_dev < 1e-6)
P(f"  S0a X47 table (2 bg x 8 z x (7 k + cum)): max rel dev {s0a_dev:.2e} -> {'PASS' if S0a else 'FAIL'}")
# S0b: X54 interval, X54's own method
key54 = "D_DES5" if MUTATE else "C_DES5"                                   # m2
a54 = X54["analysis"][key54]
xs, cs = np.array(a54["grid"]), np.array(a54["chi2"])
spl = CubicSpline(xs, cs); fine = np.linspace(xs[0], xs[-1], 20001); cf = spl(fine); cmin = cf.min()
ins = cf - cmin <= 3.84; lo, hi = float(fine[ins][0]), float(fine[ins][-1])
ref = X54["analysis"]["C_DES5"]["int95"]
S0b = abs(lo - ref[0]) < 1e-6 and abs(hi - ref[1]) < 1e-6
FM = {k: X54["analysis"][k]["report"]["lo95"]["F_made"] for k in ("C_DES5", "C_PP", "C_U3", "D_DES5", "D_PP", "D_U3")}
LINE_P = abs(FM["C_DES5"]); LINE_R = max(abs(v) for v in FM.values())
P(f"  S0b X54 {key54} 95%: [{lo:+.7f}, {hi:+.7f}] vs committed C_DES5 [{ref[0]:+.7f}, {ref[1]:+.7f}] -> {'PASS' if S0b else 'FAIL'}")
P(f"      X54 cold->DE ends (F_made at lo95): " + ", ".join(f"{k} {v:+.4f}" for k, v in FM.items()) + f"; R2 line {LINE_P:.4f}, robustness {LINE_R:.4f}")
# S0c: X43 crossover from X41's table
TBL = X41["sigma_coll_table"]; LM = np.array([math.log10(float(k)) for k in TBL]); SC = np.array([TBL[k][0] for k in TBL]); ZF = np.array([TBL[k][1] for k in TBL])
ETA4 = 4 / (3 * Bk(1.0)) * 4 ** 1.25
def cross(target, eta_fun):
    """log10 M where eta(M) Sigma_coll(M) = target (Msun/pc^2); None if outside 1e11-1e15 (reported as < / >)."""
    f = lambda lm: math.log(eta_fun(lm) * math.exp(np.interp(lm, LM, np.log(SC)))) - math.log(target)
    if f(LM[0]) > 0: return ("<", LM[0])
    if f(LM[-1]) < 0: return (">", LM[-1])
    return ("=", brentq(f, LM[0], LM[-1], xtol=1e-10))
eta4 = lambda lm: ETA4
CFT = X48["table"]; eta48 = lambda lm: 4 / (3 * Bk(1.0)) * float(np.interp(lm, CFT["lgM"], CFT["cf"])) ** 1.25
x43 = {f: cross(SIG[f], eta4)[1] for f in FEET}
S0c = abs(ETA4 - 14.83) < 0.005 and abs(x43["canonical"] - 12.1) <= 0.05 and abs(x43["alt"] - 12.4) <= 0.05
P(f"  S0c X43 crossover (eta {ETA4:.3f}): 10^{x43['canonical']:.3f} / 10^{x43['alt']:.3f} vs 10^12.1 / 10^12.4 -> {'PASS' if S0c else 'FAIL'}")
STOP = not (S0a and S0b and S0c)
CHK["K0"] = not STOP
RES["S0"] = dict(S0a=S0a, S0a_maxdev=s0a_dev, zeta=zeta, S0b=S0b, int95=[lo, hi], F_made_lo95=FM, R2_line=LINE_P, R2_robust=LINE_R,
                 S0c=S0c, eta4=ETA4, x43_lgM=x43)

# ------------------------------------------------------------------ K1: R_k -> 0 reproduces X47's local failure
k1dev = 0.0; k1fail = True
for t in BGT:
    for z in ZG:
        v = sig_g(t, z, BG[t]["rhoc0"], kmin=0.01, R=1e-4)
        k1dev = max(k1dev, abs(v / X47["task4"][t]["table_m_s2"][str(z)]["cum"] - 1))
        if z <= 3: k1fail &= all(3 * v < GT[f] for f in FEET)
CHK["K1"] = bool(k1dev < 1e-4 and k1fail)
P(f"  K1 R_k=1e-4 Mpc/h vs X47 cum: max rel dev {k1dev:.2e}; 3 sigma < g_T at z<=3 on both footings (X47 local failure): {k1fail} -> {CHK['K1']}")

# ------------------------------------------------------------------ R1 numbers: rms linear pull, total matter
P("\n=== R1: rms linear pull of the total field, k 1e-4 .. k_hm = %.2f h/Mpc (X22 lambda_hm %.3f Mpc/h)" % (K_HM, LAM_HM))
ZR = [0, 0.5, 1, 2, 3]
SG = {t: {str(z): sig_g(t, z, BG[t]["rhom0"], kmax=K_HM) for z in ZR} for t in BGT}
for t in BGT:
    P(f"  [{t}] sigma_g (m/s^2): " + ", ".join(f"z {z}: {SG[t][str(z)]:.3e}" for z in ZR)
      + " | /g_T canon " + "/".join(f"{SG[t][str(z)] / GT['canonical']:.3f}" for z in ZR)
      + " | /g_T alt " + "/".join(f"{SG[t][str(z)] / GT['alt']:.3f}" for z in ZR))
RES["R1_sigma_g"] = SG

# ------------------------------------------------------------------ E1-a: R_k window
P("\n=== E1-a: smoothed scalar key K_R = [W_R * |grad Phi|^2]^(1/2), objects at the centre (uniform sphere r_f from X41)")
RK = np.logspace(-2, math.log10(30.0), 31)
MASSES = [11, 12, 13, 14, 15]
def obj(t, lm):
    M = 10 ** lm * MSUN; Sc = math.exp(np.interp(lm, LM, np.log(SC))) * MSUN / PC ** 2
    rf = math.sqrt(3 * M / (4 * math.pi * Sc)); return M, rf, Sc
def Kown(t, lm, Rk):
    M, rf, _ = obj(t, lm); R = Rk / BG[t]["h"] * MPC
    if R <= rf: return math.sqrt(0.6) * G * M * R / rf ** 3
    return math.sqrt(3 * G * G * M * M / R ** 3 * (1 / (5 * rf) + 1 / rf - 1 / R))
def Kobj(t, lm, Rk, Kenv):
    ko = Kown(t, lm, Rk)
    return math.sqrt(max(Kenv ** 2 - ko ** 2, 0.0)) if MUTATE else math.sqrt(Kenv ** 2 + ko ** 2)   # m4
E1 = {}
mono = True
for t in BGT:
    Kenv = SG[t]["0"]; rows = []
    for Rk in RK:
        Ko = {lm: Kobj(t, lm, Rk, Kenv) for lm in MASSES}
        mono &= all(Ko[lm] >= Kenv * (1 - 1e-12) for lm in MASSES)
        lo_g = max(Ko[11], Ko[12]); hi_cl = min(Ko[14], Ko[15])
        hi_forest = min(hi_cl, SG[t]["2"], SG[t]["3"]); hi_growth = min(hi_cl, min(SG[t][str(z)] for z in ZR))
        rows.append(dict(Rk=float(Rk), K={str(lm): Ko[lm] for lm in MASSES}, lo=lo_g, hi_forest=hi_forest, hi_growth=hi_growth,
                         forest_window=bool(lo_g < hi_forest), growth_window=bool(lo_g < hi_growth)))
    E1[t] = rows
CHK["K2"] = bool(mono)
P(f"  K2 (MT: K_obj >= K_env everywhere on the grid): {mono}")
for t in BGT:
    P(f"  [{t}] R_k (Mpc/h) | K(1e11) K(1e12) K(1e13) K(1e14) K(1e15) in units of g_T canon | forest window? growth window?")
    for r in E1[t][::3]:
        P(f"     {r['Rk']:7.3f} | " + " ".join(f"{r['K'][str(lm)] / GT['canonical']:8.4f}" for lm in MASSES)
          + f" | forest {'yes' if r['forest_window'] else 'no '} [{r['lo'] / GT['canonical']:.4f}, {r['hi_forest'] / GT['canonical']:.4f}]"
          + f" | growth {'yes' if r['growth_window'] else 'no'}")
fw = {t: [r for r in E1[t] if r["forest_window"]] for t in BGT}
gw = {t: [r for r in E1[t] if r["growth_window"]] for t in BGT}
E1sum = {}
for t in BGT:
    s = dict(n_forest=len(fw[t]), n_growth=len(gw[t]))
    if fw[t]:
        s["Rk_forest_range"] = [fw[t][0]["Rk"], fw[t][-1]["Rk"]]
        s["gprime_forest_range_over_gT_canon"] = [min(r["lo"] for r in fw[t]) / GT["canonical"], max(r["hi_forest"] for r in fw[t]) / GT["canonical"]]
        for f in FEET:
            s[f"gT_in_forest_window_{f}"] = any(r["lo"] < GT[f] < r["hi_forest"] for r in fw[t])
            s[f"a0_in_forest_window_{f}"] = any(r["lo"] < A0[f] < r["hi_forest"] for r in fw[t])
        # epoch where the linear rms falls below the lowest admissible g' (non-latching: linear field turns vacuum)
        zz = np.linspace(0, 3, 61); sg = np.array([sig_g(t, z, BG[t]["rhom0"], kmax=K_HM) for z in zz])
        s["z_off_range"] = [float(np.interp(min(r["lo"] for r in fw[t]), sg, zz)), float(np.interp(max(r["hi_forest"] for r in fw[t]), sg, zz))]
    E1sum[t] = s
    P(f"  [{t}] forest-only window: {s['n_forest']}/31 R_k" + (f", R_k {s['Rk_forest_range'][0]:.3f}-{s['Rk_forest_range'][1]:.3f} Mpc/h, g'/g_T(canon) {s['gprime_forest_range_over_gT_canon'][0]:.4f}-{s['gprime_forest_range_over_gT_canon'][1]:.4f}; "
      f"g_T inside: canon {s['gT_in_forest_window_canonical']}, alt {s['gT_in_forest_window_alt']}; a0 inside: {s['a0_in_forest_window_canonical']}/{s['a0_in_forest_window_alt']}; "
      f"linear rms falls below g' at z_off {s['z_off_range'][0]:.2f}-{s['z_off_range'][1]:.2f}" if s['n_forest'] else "") + f" | growth window (all z<=3): {s['n_growth']}/31 R_k")
RES["E1a"] = dict(grid=E1, summary=E1sum)

# REPORTED ONLY (A2, post-hoc, no verdict weight): environment scatter. K_env^2 = sigma_S^2 + |g_L|^2, g_L the R_k-smoothed vector
# (Maxwell, per-component sigma_L/sqrt3), sigma_S^2 = sigma_g^2 - sigma_L^2. Galaxies emptied at the 90 % level, clusters retained at 90 %.
from scipy.stats import chi as CHI
q10, q90 = float(CHI(3).ppf(0.10)), float(CHI(3).ppf(0.90))
SCAT = {}
P("  REPORTED (A2, no verdict weight): environment scatter; window g' in (q90 of galaxies 1e11/1e12, q10 of clusters 1e14/1e15) and < sigma_g(z=2)")
for t in BGT:
    s0 = SG[t]["0"]; rows = []
    for Rk in RK:
        sL = sig_g(t, 0, BG[t]["rhom0"], kmax=K_HM, R=Rk); sS2 = max(s0 ** 2 - sL ** 2, 0.0)
        qk = lambda lm, q: math.sqrt(sS2 + (sL / math.sqrt(3) * q) ** 2 + Kown(t, lm, Rk) ** 2)
        lo_ = max(qk(11, q90), qk(12, q90)); hi_ = min(qk(14, q10), qk(15, q10), SG[t]["2"])
        xL = (lo_ ** 2 - sS2) / (sL / math.sqrt(3)) ** 2
        fdust = float(CHI(3).sf(math.sqrt(xL))) if xL > 0 else 1.0       # linear-field dust fraction at z = 0 at g' = lo_
        rows.append(dict(Rk=float(Rk), sigma_L=sL, lo=lo_, hi=hi_, window=bool(lo_ < hi_), lin_dust_frac_z0_at_lo=fdust))
    SCAT[t] = rows
    win = [r for r in rows if r["window"]]
    P(f"  [{t}] scatter variant: forest window at {len(win)}/31 R_k" + (f" (R_k {win[0]['Rk']:.3f}-{win[-1]['Rk']:.3f} Mpc/h; g'/g_T canon {min(r['lo'] for r in win) / GT['canonical']:.3f}-{max(r['hi'] for r in win) / GT['canonical']:.3f})" if win else "")
      + f"; linear-field dust fraction at z = 0 when 90 % of galaxies are emptied: max over R_k {max(r['lin_dust_frac_z0_at_lo'] for r in rows):.3f}")
RES["E1a_scatter_reported"] = SCAT

# REPORTED ONLY (A3, coordinator request after the first full run; no verdict weight): can any key give X58's NON-MONOTONE retention
# (dwarfs 1e9-1e10 hold halos, L* 1e12 empty, clusters 1e14-1e15 hold)? Needs K(dwarf) > K(L*) < K(cluster) at one R_k.
# Sigma_coll below 1e11 is a log-log EXTRAPOLATION of X41's table (slope of its 1e11-1e12 segment) -- disclosed.
slope_lo = (math.log(SC[1]) - math.log(SC[0])) / (LM[1] - LM[0])
def Sc_ext(lm): return math.exp(math.log(SC[0]) + slope_lo * (lm - LM[0])) if lm < LM[0] else math.exp(np.interp(lm, LM, np.log(SC)))
def Kown_ext(t, lm, Rk):
    M = 10 ** lm * MSUN; Sc = Sc_ext(lm) * MSUN / PC ** 2; rf = math.sqrt(3 * M / (4 * math.pi * Sc)); R = Rk / BG[t]["h"] * MPC
    if R <= rf: return math.sqrt(0.6) * G * M * R / rf ** 3
    return math.sqrt(3 * G * G * M * M / R ** 3 * (1 / (5 * rf) + 1 / rf - 1 / R))
NM = {}
for t in BGT:
    s0 = SG[t]["0"]; u_rk = []; shapes = []
    for Rk in RK:
        K = {lm: math.sqrt(s0 ** 2 + Kown_ext(t, lm, Rk) ** 2) for lm in (9, 9.5, 10, 12, 14, 15)}
        dw = max(K[9], K[9.5], K[10]); cl = max(K[14], K[15])
        if dw > K[12] and cl > K[12]: u_rk.append(float(Rk))
        lms = np.linspace(9, 15, 61); kv = [Kown_ext(t, l, Rk) for l in lms]
        shapes.append(float(lms[int(np.argmax(kv))]))
    core_mono = all(np.diff([Sc_ext(l) for l in np.linspace(9, 15, 61)]) > 0)
    NM[t] = dict(U_shape_Rk=u_rk, own_key_peak_lgM_per_Rk=shapes, core_key_monotone_increasing=bool(core_mono), virial_key_monotone_increasing=bool(core_mono))
    P(f"  REPORTED (A3) [{t}] non-monotone pattern (dwarf > L* < cluster) at {len(u_rk)}/31 R_k; the smoothed key's own term peaks at lgM "
      f"{min(shapes):.1f}-{max(shapes):.1f} (inverted U: maximal where r_f ~ R_k); core and virial object keys monotone increasing in M: {core_mono}")
RES["nonmonotone_reported"] = NM

# AMENDMENT A1 (post-result, graded): R5 retention pattern
LD = np.arange(8.0, 10.0001, 0.05); LS = np.arange(11.35, 12.0501, 0.05); LG = [13.0, 14.0, 15.0]
R5 = {}
for t in BGT:
    s0 = SG[t]["0"]; best = None
    for Rk in RK:
        Kf = lambda lm: math.sqrt(s0 ** 2 + Kown_ext(t, lm, Rk) ** 2)
        gap = min(min(Kf(l) for l in LD), min(Kf(l) for l in LG)) - max(Kf(l) for l in LS)
        if best is None or gap > best[1]: best = (float(Rk), gap / GT["canonical"])
    # object keys: core (eta Sigma_coll, eta flat c_f=4) and virial (Sigma_coll): need K(L*) below both ends
    ck = lambda lm: Sc_ext(lm)
    obj_pass = min(ck(l) for l in LD) > max(ck(l) for l in LS) and min(ck(l) for l in LG) > max(ck(l) for l in LS)
    R5[t] = dict(smoothed_best_Rk=best[0], smoothed_best_gap_over_gT=best[1], smoothed_pass=bool(best[1] > 0), object_key_pass=bool(obj_pass),
                 dwarf_core_over_Lstar_core=ck(10.0) / ck(11.35))
    P(f"  R5 (A1) [{t}] smoothed key: best R_k {best[0]:.3f} Mpc/h, min(dwarf, >=1e13) - max(L*) = {best[1]:+.5f} g_T -> {'PASS' if best[1] > 0 else 'FAIL'}; "
      f"object keys (core/virial, monotone): Sigma_coll(1e10)/Sigma_coll(10^11.35) = {ck(10.0) / ck(11.35):.3f} -> {'PASS' if obj_pass else 'FAIL'}")
RES["R5_A1"] = R5

# ------------------------------------------------------------------ PS fractions
def fPS(t, M, z=0.0):
    s = float(BG[t]["sig"](M)[0]) * (Dexact(t, z) if z > 0 else 1.0)
    return float(erfc(1.686 / (math.sqrt(2) * s)))
k4ps = float(erfc(0.0)) == 1.0 and all(np.all(np.diff(BG[t]["sig"](np.logspace(6, 15, 40))) < 0) for t in BGT)   # A1: frozen text "erfc(0) = 1"; sigma(M) decreasing
k4s8 = all(abs(BGSE[t]["s8"] - BGSE[t]["s8_F3"]) <= 1e-3 for t in BGT)
CHK["K4"] = bool(k4ps and k4s8)
P(f"\n  K4: EM1 sigma8 vs F3 {k4s8}; erfc(0) = 1 and sigma(M) decreasing on 1e6-1e15 Msun: {k4ps} -> {CHK['K4']}  (reported: f(>1e6) = {fPS('A_c2b_refit', 1e6):.3f}; the P(k) table ends at k 150 h/Mpc)")

# ------------------------------------------------------------------ E1-b / E2-O crossovers
P("\n=== E1-b / E2-O: object keys (core peak pull without floor; virial mean pull)")
XO = {}
for f in FEET:
    XO[f] = {}
    for gl, gp in (("g_T", GT[f]), ("a0", A0[f])):
        tgt_core = SIG[f] * gp / GT[f]                                     # eta Sigma_coll = Sigma_a0 g'/g_T
        tgt_vir = gp / ((4 * math.pi / 3) * G) / (MSUN / PC ** 2)          # Sigma_coll where (4pi/3) G Sigma_coll = g'
        XO[f][gl] = dict(core_cf4=cross(tgt_core, eta4), core_ng48=cross(tgt_core, eta48), virial=cross(tgt_vir, lambda lm: 1.0))
        P(f"  [{f}] g' = {gl} ({gp:.3e}): crossover M_x core c_f=4 {XO[f][gl]['core_cf4'][0]}10^{XO[f][gl]['core_cf4'][1]:.2f}; "
          f"core ng48 {XO[f][gl]['core_ng48'][0]}10^{XO[f][gl]['core_ng48'][1]:.2f}; virial {XO[f][gl]['virial'][0]}10^{XO[f][gl]['virial'][1]:.2f}")
RES["E1b_crossovers"] = XO

# ------------------------------------------------------------------ R2: conversion budget
P("\n=== R2: converted fraction F_conv (PS, z = 0) vs X54")
MMIN = {"M_L_min_X22": ML_MIN, "M_hm_X22": M_HM, "1e11": 1e11}
R2 = {}
for f in FEET:
    R2[f] = {}
    for t in BGT:
        R2[f][t] = {}
        for lab, xo in (("core_cf4", XO[f]["g_T"]["core_cf4"]), ("core_ng48", XO[f]["g_T"]["core_ng48"])):
            Mx = 10 ** xo[1]
            row = {mm: fPS(t, mv) - fPS(t, Mx) for mm, mv in MMIN.items()}
            row["E1a_E2L_lower_bound"] = 1 - fPS(t, 1e12)
            row["z3_converted_above_Mhm"] = fPS(t, M_HM, 3.0) - fPS(t, Mx, 3.0)
            row["q_max_primary"] = LINE_P / row["M_L_min_X22"]; row["q_max_robust"] = LINE_R / row["M_L_min_X22"]
            row["Mx_lg"] = xo[1]
            R2[f][t][lab] = row
            P(f"  [{f}|{t}|{lab} M_x 10^{xo[1]:.2f}] F_conv: M_min 3.0e8 {row['M_L_min_X22']:.3f}, 4.9e9 {row['M_hm_X22']:.3f}, 1e11 {row['1e11']:.3f} "
              f"| vs line {LINE_P:.4f} (x{row['M_L_min_X22'] / LINE_P:.1f}), robust {LINE_R:.4f} (x{row['M_L_min_X22'] / LINE_R:.1f}) | q_max {row['q_max_primary']:.3f}/{row['q_max_robust']:.3f} "
              f"| E1-a/E2-L lower bound 1-f(>1e12) {row['E1a_E2L_lower_bound']:.3f} | already converted at z=3 (M_hm..M_x) {row['z3_converted_above_Mhm']:.3f}")
RES["R2"] = R2

# ------------------------------------------------------------------ R0: rigidity of the w = -1 phase (sympy)
P("\n=== R0: two-phase conservation (sympy, Minkowski, c = 1)")
tt, xx, yy, zz_ = sp.symbols("t x y z", real=True); X = (tt, xx, yy, zz_)
eta = sp.diag(-1, 1, 1, 1); rv = sp.Function("rho_v")(*X)
u = sp.symbols("u0:4", real=True)
pv = sp.Integer(0) if MUTATE else -rv                                     # m3
Tv = sp.Matrix(4, 4, lambda m, n: (rv + pv) * u[m] * u[n] + pv * eta[m, n])
target = [sp.simplify(-sum(eta[n, m] * sp.diff(rv, X[m]) for m in range(4))) for n in range(4)]
rig1 = all(sp.simplify(sp.diff(Tv[0, n], tt) + sum(sp.diff(Tv[m, n], X[m]) for m in range(1, 4)) - target[n]) == 0 for n in range(4))
rig2 = all(sp.simplify(Tv[0, i]) == 0 for i in range(1, 4))
CHK["K3"] = bool(rig1 and rig2)
P(f"  K3: div(-rho_v eta) = -d^nu rho_v: {rig1}; T_v^(0i) = 0 for any 4-velocity (no momentum density, no energy flux): {rig2} -> {CHK['K3']}")
# background: rho_d a^3 = const iff <Q^0> = 0
a_ = sp.Function("a")(tt); rd = sp.Function("rho_d")(tt); Q = sp.Symbol("Q")
eqb = sp.Eq(sp.diff(rd, tt) + 3 * sp.diff(a_, tt) / a_ * rd, -Q)
dra3 = sp.simplify(sp.diff(rd * a_ ** 3, tt).subs(sp.diff(rd, tt), sp.solve(eqb, sp.diff(rd, tt))[0]))
P(f"  background: d(rho_d a^3)/dt = {dra3}  -> zero iff <Q^0> = 0 (E3 satisfies X54 identically at background level)")
# numbers: what gradient a residual dust could bear vs what in-place conversion needs
R0 = {}
fair = {t: BG[t]["p"]["omega_cdm"] / BG[t]["p"]["omega_b"] for t in BGT}
for f in FEET:
    tol = X22["step2"]["per_footing"][f]["Mc_max_over_Mb_at_Rlast"][2]
    res_frac = tol / fair["A_c2b_refit"]                                 # residual cold / fair-share cold inside R_last
    need = (1 - res_frac) / res_frac                                     # rho_v,lump / rho_d,res if converted energy stays in place
    _, rf12, _ = obj("A_c2b_refit", 12.0)
    bear = {"R_last_median": A0[f] * X22["step2"]["R_last_kpc_min_p16_p50_p84_max"][2] * KPC / C ** 2, "r_f_1e12": A0[f] * rf12 / C ** 2}
    # transport loophole (w = -1 + eps): eps gamma^2 v/c needed to carry a 1e12 galaxy's cold share out of r_f in a Hubble time,
    # if the streaming phase has the ambient density rho_DE
    bgA = BG["A_c2b_refit"]; Mc = 1e12 * MSUN * bgA["Oc"] / bgA["Om"]; H0 = 100e3 * bgA["h"] / MPC
    rhoL = bgA["OL"] * 3 * H0 ** 2 / (8 * math.pi * G)
    eps_need = Mc / (4 * math.pi * rf12 ** 2 * (1 / H0) * rhoL * C)
    R0[f] = dict(tol_Mc_over_Mb=tol, residual_fraction_of_fair=res_frac, rho_v_over_rho_dres_needed=need, bearable=bear,
                 margin_log10=math.log10(need / max(bear.values())), source_ratio_inplace=-2.0, eps_gamma2_v_over_c_needed=eps_need,
                 r_f_1e12_kpc=rf12 / KPC)
    P(f"  [{f}] in place: residual cold {res_frac:.4f} of fair share (X22 tol {tol:.4f} M_b) -> rho_v/rho_d,res needed {need:.0f}; bearable at <= a0: "
      f"{bear['R_last_median']:.2e} (R_last median) / {bear['r_f_1e12']:.2e} (r_f 1e12 = {rf12 / KPC:.0f} kpc) -> short by 10^{R0[f]['margin_log10']:.1f}; "
      f"in-place lump gravitates with rho+3p = -2 rho_v (pull ratio -2)")
    P(f"  [{f}] transport loophole (w = -1 + eps, ambient rho_DE): eps gamma^2 v/c >= {eps_need:.2e} to empty a 1e12 halo through r_f in 1/H0")
RES["R0"] = R0

# ------------------------------------------------------------------ E3-P capacity
P("\n=== E3-P: in-place vacuum available for compensation inside clusters")
E3 = {}
for t in BGT:
    b = BG[t]; E3[t] = {}
    for lm in (14, 15):
        zf = float(np.interp(lm, LM, ZF))
        E3[t][str(lm)] = b["OL"] / (18 * math.pi ** 2 * b["Oc"] * (1 + zf) ** 3)
    for f in FEET:
        Mx = 10 ** XO[f]["g_T"]["core_cf4"][1]
        cap = max(E3[t]["14"], E3[t]["15"]) * fPS(t, Mx)
        Fc = R2[f][t]["core_cf4"]["M_L_min_X22"]
        E3[t][f] = dict(capacity=cap, F_conv=Fc, net=Fc - cap)
        P(f"  [{t}|{f}] rho_L/rho_c,vir: 1e14 {E3[t]['14']:.4f}, 1e15 {E3[t]['15']:.4f}; capacity x f(>M_x) = {cap:.5f} vs F_conv {Fc:.3f} -> net {Fc - cap:.3f}")
RES["E3"] = E3

# ------------------------------------------------------------------ grading
CHK["K5"] = rss() < 1.0
RES["checks"] = CHK
P(f"\nchecks: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in CHK.items()) + f"  (RSS {rss():.2f} GB)")
def grade(fails):
    return "AN EXCLUDED BY " + ", ".join(fails) if fails else "AN SURVIVES"
V = {}
if STOP or not all(CHK.values()):
    V = {e: {f: "UNDECIDED (step 0 / checks)" for f in FEET} for e in ("E1-a", "E1-b", "E2-L", "E2-O", "E3-P", "E3-N")}
else:
    tA = "A_c2b_refit"
    for f in FEET:
        inplace_R0 = R0[f]["rho_v_over_rho_dres_needed"] > max(R0[f]["bearable"].values())
        Fc = R2[f][tA]["core_cf4"]["M_L_min_X22"]; lb = R2[f][tA]["core_cf4"]["E1a_E2L_lower_bound"]
        xc = XO[f]["g_T"]["core_cf4"]
        r3_core = xc[1] >= 12.0 and xc[0] != "<"; r4_core = xc[1] <= 14.0 and xc[0] != ">"
        growth_empty = all(E1sum[t]["n_growth"] == 0 for t in BGT)
        g = {}
        # E1-a: non-latching smoothed key; galaxies' dust converts in place; linear field below g' at z=0 (MT)
        g["E1-a"] = [n for n, bad in (("R0", inplace_R0), ("R1", growth_empty), ("R2", lb > LINE_P)) if bad]
        # E1-b / E2-O: object key (core, c_f = 4), linear field untouched
        fb = [n for n, bad in (("R0", inplace_R0), ("R1", False), ("R2", Fc > LINE_P), ("R3", not r3_core), ("R4", not r4_core)) if bad]
        g["E1-b"] = fb; g["E2-O"] = list(fb)
        # E2-L: local hysteresis; unlatching galaxies unlatches the linear field (MT)
        g["E2-L"] = [n for n, bad in (("R0", inplace_R0), ("R1", bool(mono)), ("R2", lb > LINE_P)) if bad]
        # E3-P: compensation in place
        g["E3-P"] = [n for n, bad in (("R0", inplace_R0), ("R2", E3[tA][f]["net"] > LINE_P)) if bad]
        # E3-N: relocation through the vacuum phase (zero flux at w = -1)
        g["E3-N"] = [n for n, bad in (("R0", bool(rig2)), ("R3", not r3_core), ("R4", not r4_core)) if bad]
        r5s = not all(R5[t]["smoothed_pass"] for t in BGT); r5o = not all(R5[t]["object_key_pass"] for t in BGT)
        for e in g:
            if (r5s if e in ("E1-a", "E2-L") else r5o): g[e].append("R5")
        for e, fl in g.items():
            V.setdefault(e, {})[f] = grade(fl)
P("\n=== VERDICTS")
VE = {}
for e in V:
    vs = set(V[e].values()); VE[e] = V[e]["canonical"] if len(vs) == 1 else "UNDECIDED (footings disagree)"
    P(f"  {e}: canonical {V[e]['canonical']} | alt {V[e]['alt']} -> {VE[e]}")
surv = [e for e in VE if VE[e].startswith("AN SURVIVES")]
if surv: overall = "AN SURVIVES VIA " + ", ".join(surv)
elif all(VE[e].startswith("AN EXCLUDED") for e in VE):
    lines = sorted({x.strip() for e in VE for x in VE[e].replace("AN EXCLUDED BY ", "").split(",")})
    overall = "AN EXCLUDED BY " + ", ".join(lines)
else: overall = "UNDECIDED"
P(f"  OVERALL: {overall}")
RES["verdict_per_escape_per_footing"] = V; RES["verdict_per_escape"] = VE; RES["verdict"] = overall
RES["elapsed_s"] = time.time() - T0; RES["peak_rss_GB"] = rss()
json.dump(RES, open(os.path.join(HERE, f"x60_an_results{TAG}.json"), "w"), indent=1, default=lambda o: o if not isinstance(o, (np.bool_,)) else bool(o))
open(os.path.join(HERE, f"x60_an{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (not STOP and all(CHK.values())) else 1)
