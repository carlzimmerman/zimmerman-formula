#!/usr/bin/env python3
"""X24b_vacuum_heated_cold (FROZEN_CRITERIA.md, 1d0f8c6967): vacuum-heated cold energy, Q = eps H rho_L c^2 per unit volume.

  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x24b_vacuum_heated_cold.py                 -> .out, _results.json
  PYTHONHASHSEED=0 X24B_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 x24b_vacuum_heated_cold.py   -> *_MUTATE.* (exit 1 by design)

Copied with provenance (verbatim bodies): X22's forest gate (L346 bins, L319 line, forest_class), linear two-fluid ODE, BBKS
sigma8 ratio and CFG946 constants (x22_cosmic_dust_window.py L68-171, L477-566); X23's e_pred grader (x23_late_heating_graded.py
L24-63). The ODE gains the derived non-barotropic VHC term (x24b_derive.py D3). kappa = 1/2 FITTED; footings never pooled;
cold component = field mass, never a particle; eps bounded, never fitted or scanned; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import csv, json, math, resource, sys, time
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.stats import spearmanr

T0 = time.time()
MUT = os.environ.get("X24B_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(RB, ".."))
OUT = []
RES = {"lane": "X24b_vacuum_heated_cold", "criteria": "1d0f8c6967", "mutate": MUT, "checks": {}}
np.seterr(all="ignore")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def check(name, ok, val):
    RES["checks"][name] = {"pass": bool(ok), "value": str(val)}
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {val}")
def rd(rel):
    return json.load(open(os.path.join(REPO, rel)))

P("X24b_vacuum_heated_cold" + (" [MUTATE: heating per unit MASS; control output, not physics]" if MUT else "") +
  ": kappa = 1/2 FITTED; footings never pooled; field mass, not a particle; not theory closed")

# ------------------------------------------------------------------ CFG946 constants (X22 verbatim)
G_SI, KPC946, MSUN946, PC946 = 6.67430e-11, 3.0856775814913673e19, 1.98847e30, 3.0856775814913673e16
MPC_M = 1e6 * PC946
H0_946 = 67.4e3 / MPC_M
RHOC_946 = 3 * H0_946 ** 2 / (8 * math.pi * G_SI)
OB946 = 0.0493
OC946 = 5.364 * OB946
OM946 = OB946 + OC946
OL946 = 1.0 - OM946
RHOM946 = OM946 * RHOC_946
DTA, BCAP = 5.55, 2.9
FC, FB = 5.364 / 6.364, 1.0 / 6.364
C_KMS = 299792.458
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")

X22J = rd("rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")
X23J = rd("rebuild_2026_10_22/X23_late_heating_graded/x23_late_heating_graded_results.json")
X19 = rd("rebuild_2026_10_22/X19_selector_rank_test/x19_selector_rank_test_results.json")
X21J = rd("rebuild_2026_10_22/X21_cluster_switch_anatomy/x21_switch_anatomy_results.json")
CSNEED = {f: X22J["step2"]["per_footing"][f]["cs_need_kms"] for f in FOOTS}

# ------------------------------------------------------------------ X22's forest gate (verbatim)
L346 = rd("real_research/g03_audit_2026/L346_switch_forest_gate_results.json")
runs346 = L346["numbers"]["runs"]
def r346(name, z):
    a = np.array(runs346[name]["pk"][z]); b = np.array(runs346["lcdm"]["pk"][z]); kk = b[:, 0]
    fo = (kk >= 1.0) & (kk <= 4.0)
    return kk[fo], (a[:, 1] / b[:, 1])[fo]
KB346 = r346("sw5_canon", "3.0")[0]
h19 = 0.6736
Om19 = (0.02237 + 0.1200) / h19 ** 2
K_H19 = np.geomspace(0.02, 30.0, 44)
K5 = float(K_H19[int(np.argmin(np.abs(K_H19 - 5.0)))])
NU, EXPO = 1.12, -10.0 / 1.12
def alpha_wdm(m_keV):
    return 0.049 * m_keV ** -1.11 * (Om19 / 0.25) ** 0.11 * (h19 / 0.7) ** 1.22
def T2cut(k_h, alpha):
    return (1 + (alpha * np.asarray(k_h, float)) ** (2 * NU)) ** EXPO
T2_53 = float(T2cut(K5, alpha_wdm(5.3)))
def forest_class(t2bins_by_z, t2k5_by_z):
    allbins = [v for z in t2bins_by_z for v in t2bins_by_z[z]]
    k5s = list(t2k5_by_z.values())
    if min(k5s) < 0.9 or min(allbins) < 0.5 or max(allbins) > 2.0:
        return "FAIL"
    if all(0.8 <= v <= 1.2 for v in allbins) and min(k5s) >= T2_53:
        return "PASS"
    return "UNDECIDED"

# ------------------------------------------------------------------ X22's linear ODE + the VHC term (D3)
SRC = 1.5
S_COEF = 0.0 if MUT else 5.0                 # s' = (2/3) d' - 5 (d + s)  [VHC];  MUTATE (per mass): s' = (2/3) d' - 5 s
A_ATTR = (1.0 / 9.0) if MUT else (-13.0 / 18.0)
def grow(k_h, cs_fn, ai=1e-3, zout=(3.0, 2.0, 0.0), vhc=False, track_s=False):
    def rhs(N, y):
        a = math.exp(N)
        E2 = OM946 * a ** -3 + OL946
        Oma = OM946 * a ** -3 / E2
        dlnH = -1.5 * Oma
        cs = cs_fn(a)
        J = (cs * k_h / (100.0 * a * math.sqrt(E2))) ** 2
        src = SRC * Oma * (FC * y[0] + FB * y[2])
        if not vhc:
            return [y[1], -(2 + dlnH) * y[1] + src - J * y[0], y[3], -(2 + dlnH) * y[3] + src]
        return [y[1], -(2 + dlnH) * y[1] + src - J * (y[0] + y[4]), y[3], -(2 + dlnH) * y[3] + src,
                (2.0 / 3.0) * y[1] - S_COEF * y[0] - 5.0 * y[4]]
    Ns = sorted([math.log(1 / (1 + z)) for z in zout])
    y = [ai, ai, ai, ai] + ([A_ATTR * ai] if vhc else [])
    sol = solve_ivp(rhs, (math.log(ai), 0.0), y, method="LSODA", rtol=1e-8, atol=1e-14, t_eval=Ns)
    out = {round(1 / math.exp(N) - 1, 6): FC * sol.y[0][j] + FB * sol.y[2][j] for j, N in enumerate(sol.t)}
    if track_s:
        return out, sol
    return out

KS8 = np.geomspace(1e-3, 30.0, 61)
KF = np.concatenate([KB346, [K5]])
REF = {float(k): grow(float(k), lambda a: 0.0) for k in np.concatenate([KS8, KF])}
h_m, Om_m, Ob_m, ns_m = 0.674, 0.315, 0.0493, 0.965
Gam = Om_m * h_m * np.exp(-Ob_m * (1.0 + np.sqrt(2 * h_m) / Om_m))
def Tk(k):
    qq = k / Gam
    return (np.log(1 + 2.34 * qq) / (2.34 * qq) * (1 + 3.89 * qq + (16.1 * qq) ** 2 + (5.46 * qq) ** 3 + (6.71 * qq) ** 4) ** -0.25)
kfine = np.logspace(-4, 2, 1200)
D2shape = kfine ** (3 + ns_m) * Tk(kfine) ** 2
def Wth(x):
    return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
W8 = Wth(kfine * 8.0) ** 2
def sigma8_ratio(T2_on_KS8):
    lt = np.interp(np.log(np.clip(kfine, KS8[0], KS8[-1])), np.log(KS8), np.log(np.maximum(T2_on_KS8, 1e-300)))
    T2f = np.where(kfine < KS8[0], 1.0, np.exp(lt))
    return math.sqrt(np.trapz(D2shape * W8 * T2f, np.log(kfine)) / np.trapz(D2shape * W8, np.log(kfine)))
def grade(cs_fn, vhc=False):
    T2_8 = np.array([(grow(float(k), cs_fn, zout=(0.0,), vhc=vhc)[0.0] / REF[float(k)][0.0]) ** 2 for k in KS8])
    gF = {float(k): grow(float(k), cs_fn, zout=(3.0, 2.0), vhc=vhc) for k in KF}
    tb, tk = {}, {}
    for z, zs in ((3.0, "3"), (2.0, "2")):
        tb[zs] = [(gF[float(k)][z] / REF[float(k)][z]) ** 2 for k in KB346]
        tk[zs] = (gF[K5][z] / REF[K5][z]) ** 2
    return {"R_sigma8": sigma8_ratio(T2_8), "forest": forest_class(tb, tk), "bins_z3": tb["3"], "bins_z2": tb["2"], "T2_k5": tk,
            "T2_z0_at_k_0.1_1_10": [float(np.interp(math.log(kk), np.log(KS8), T2_8)) for kk in (0.1, 1.0, 10.0)]}

# ------------------------------------------------------------------ X23's grader (verbatim)
def r_ta(Mb_kg):
    return (3 * (OM946 / OB946) * Mb_kg / (4 * math.pi * DTA * RHOM946)) ** (1.0 / 3.0)
def hydro_frac_enclosed(beta, x):
    return (1.0 / DTA) * 3.0 / (3.0 - beta) * np.power(np.minimum(x, 1.0), 3.0 - beta)
def law_g(gN, a0):
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))
def e_pred(Mb_tot_msun, r_m, gN, sigma_kms, a0, cs_kms):
    beta_raw = 2.0 * sigma_kms ** 2 / cs_kms ** 2
    beta = min(beta_raw, BCAP)
    Mb = Mb_tot_msun * MSUN946
    Mc = 5.364 * Mb * float(hydro_frac_enclosed(beta, r_m / r_ta(Mb)))
    gc = G_SI * Mc / r_m ** 2
    return float(np.log10(law_g(gN + gc, a0) / law_g(gN, a0))), beta_raw, beta_raw >= BCAP, gc / gN
def label(z):
    return "EXTRA" if z >= 2 else ("NONE" if z < 1 else "AMBIGUOUS")

# ================================================================== STEP 0 (K0)
P("\n== STEP 0: reproductions")
k0 = abs(CSNEED["canonical"] - 190.014) < 0.01 and abs(CSNEED["alt"] - 201.315) < 0.01
dev22 = 0.0
for p in (2.0, 3.0):
    c0 = CSNEED["canonical"]
    gr = grade(lambda a, c0=c0, p=p: c0 * a ** (p - 0.5))
    ref = X22J["step3B"]["per_footing"]["canonical"][str(p)]
    dev22 = max(dev22, abs(gr["R_sigma8"] - ref["R_sigma8"]), abs(gr["T2_k5"]["3"] - ref["T2_k5"]["3"]), abs(gr["T2_k5"]["2"] - ref["T2_k5"]["2"]))
    k0 = k0 and gr["forest"] == ref["forest"]
    P(f"  X22 p = {p}: forest {gr['forest']} (X22 {ref['forest']}), R_sigma8 {gr['R_sigma8']:.10f} (X22 {ref['R_sigma8']:.10f})")
dev23 = 0.0
for f in FOOTS:
    IV = X19["intervals"][f"{f}|p16_84"]
    for c, v in X23J["footings"][f]["classes"].items():
        iv = IV[c]; gN = iv["x"][2] * A0[f]
        r = 3 * gN / (4 * math.pi * G_SI * iv["rho_b"][2] * MSUN946 / PC946 ** 3)
        dev23 = max(dev23, abs(e_pred(iv["M_b"][2], r, gN, iv["sigma"][2], A0[f], CSNEED[f])[0] - v["E_pred"]))
k0 = k0 and dev22 <= 1e-9 and dev23 <= 1e-12
check("K0", k0, f"c_s,need {CSNEED['canonical']:.3f} / {CSNEED['alt']:.3f}; X22 p=2,3 rows max dev {dev22:.2e}; X23 E_pred max dev {dev23:.2e}")
STOP = not k0

# ================================================================== K1: derivation
DJ = json.load(open(os.path.join(HERE, f"x24b_derive_results{TAG}.json")))
k1 = all(v["pass"] for v in DJ["checks"].values())
check("K1", k1, "x24b_derive D1-D5: " + ", ".join(f"{k.split()[0]} {'ok' if v['pass'] else 'FAIL'}" for k, v in DJ["checks"].items()))

# ================================================================== spherical collapse (LCDM) and the entropy integral
def heat_integrand(rho_rel, a):
    """dk/dN with rho_rel = rho_c / rhobar_c0. VHC: rho^(-5/3). MUTATE (per mass): a^3 rho^(-2/3)."""
    return a ** 3 * rho_rel ** (-2.0 / 3.0) if MUT else rho_rel ** (-5.0 / 3.0)

def sc_run(delta_i, OL, ai=1e-3, rho_cap=None, stop="collapse"):
    Om = 1.0 - OL if OL == 0.0 else OM946
    def Ea(a):
        return math.sqrt(Om * a ** -3 + OL)
    def rhs(t, z):
        a, y, yd, k = z
        rho = 1.0 / max(y, 1e-30) ** 3                 # y = R / r_L, r_L the Lagrangian (mass) radius
        if rho_cap is not None:
            rho = min(rho, rho_cap)
        return [a * Ea(a), yd, -(Om / 2) / y ** 2 + OL * y, Ea(a) * heat_integrand(rho, a)]
    Hi = Ea(ai)
    yi = ai * (1 + delta_i) ** (-1.0 / 3.0)             # growing mode: rho/rhobar = 1 + delta_i, Rdot/R = H (1 - delta_i/3)
    z0 = [ai, yi, Hi * yi * (1 - delta_i / 3), ai ** 5 / 5]
    ev_ta = lambda t, z: z[2]; ev_ta.terminal = (stop == "turnaround"); ev_ta.direction = -1
    ev_col = lambda t, z: z[1] - 1e-4 * ai; ev_col.terminal = True; ev_col.direction = -1
    ev_a = lambda t, z: z[0] - 1.0; ev_a.terminal = True
    sol = solve_ivp(rhs, (0.0, 50.0), z0, method="LSODA", rtol=1e-10, atol=1e-14, events=[ev_ta, ev_col, ev_a], max_step=0.01)
    return sol

def find_delta(target_a, OL, kind="collapse"):
    lo, hi = 1e-6, 0.5
    for _ in range(45):
        md = math.sqrt(lo * hi)
        s = sc_run(md, OL, stop="turnaround" if kind == "turnaround" else "collapse")
        ev = s.t_events[0] if kind == "turnaround" else s.t_events[1]
        reached = len(ev) > 0
        a_ev = s.y_events[0][0][0] if (kind == "turnaround" and reached) else (s.y_events[1][0][0] if reached else 2.0)
        if reached and a_ev < target_a:
            hi = md
        else:
            lo = md
    return hi                                          # the event is reached at hi (a_event just below target)

def history(a_c, OL=None):
    """k_class for collapse at a_c: SC path with rho capped at rho_vir = 8 rho_ta, then rho_vir held to a = 1."""
    OL = OL946 if OL is None else OL
    di = find_delta(a_c, OL, "collapse")
    s1 = sc_run(di, OL, stop="turnaround")
    a_ta, y_ta = s1.y_events[0][0][0], s1.y_events[0][0][1]
    rho_ta = 1.0 / y_ta ** 3
    rho_vir = 8 * rho_ta
    s2 = sc_run(di, OL, rho_cap=rho_vir, stop="collapse")
    a_col, k_col = s2.y_events[1][0][0], s2.y_events[1][0][3]
    if MUT:
        k = k_col + rho_vir ** (-2.0 / 3.0) * (1 - a_col ** 3) / 3.0       # per-mass heating: integral of a^3 rho^(-2/3) dN
    else:
        k = k_col + rho_vir ** (-5.0 / 3.0) * (-math.log(a_col))            # held at rho_vir from a_c to 1
    return dict(delta_i=di, a_ta=a_ta, a_c=a_col, rho_ta_over_mean=rho_ta * a_ta ** 3, rho_vir_rel=rho_vir, k=k,
                k_pre=k_col, k_post=k - k_col)

def late_element():
    di = find_delta(1.0, OL946, "turnaround")
    s = sc_run(di, OL946, stop="turnaround")
    return dict(delta_i=di, a_ta=s.y_events[0][0][0], k=s.y_events[0][0][3], rho_ta_rel=1.0 / s.y_events[0][0][1] ** 3)

# K2: EdS limit and background closed form
OLsave = OL946
di_e = find_delta(0.5, 0.0, "collapse")
se = sc_run(di_e, 0.0, stop="turnaround")
a_ta_e, y_ta_e = se.y_events[0][0][0], se.y_events[0][0][1]
sc_ = sc_run(di_e, 0.0, stop="collapse"); a_c_e = sc_.y_events[1][0][0]
dlin = di_e * a_c_e / 1e-3
rta_e = (a_ta_e / y_ta_e) ** 3
sb = sc_run(0.0, OL946, stop="collapse")
kbg = sb.y[3][-1]; abg = sb.y[0][-1]
k2 = abs(dlin / 1.686 - 1) <= 5e-3 and abs(rta_e / (9 * math.pi ** 2 / 16) - 1) <= 5e-3 and abs(kbg / (abg ** 5 / 5) - 1) <= 1e-6
check("K2", k2, f"EdS: delta_lin(collapse) {dlin:.4f} (1.686), rho_ta/rhobar {rta_e:.4f} (5.552); background k(a={abg:.3f}) / (a^5/5) - 1 = {kbg / (abg ** 5 / 5) - 1:.2e}")

if STOP and not MUT:
    P("STOP RULE: Step 0 failed; verdict UNDECIDED")
    RES["verdict"] = "UNDECIDED (stop rule)"

# ================================================================== STEP 2: the eps bounds
P("\n== STEP 2: eps bounds")
def cs0_of_eps(eps):           # background c_s(z = 0), km/s (D1)
    return C_KMS * math.sqrt(2 * eps * OL946 / (15 * OC946))
def eps_of_cs0(c):
    return 15 * OC946 * (c / C_KMS) ** 2 / (2 * OL946)
def win_ok(eps):
    c0 = cs0_of_eps(eps)
    g = grade(lambda a: c0 * a ** 1.5, vhc=True)
    return g["forest"] != "FAIL" and g["R_sigma8"] >= 0.95, g
lo, hi = math.log(1e-12), math.log(1e-2)
assert win_ok(1e-12)[0] and not win_ok(1e-2)[0]
for _ in range(40):
    md = 0.5 * (lo + hi)
    (lo, hi) = (md, hi) if win_ok(math.exp(md))[0] else (lo, md)
EPS_UP = math.exp(lo)
g_up = win_ok(EPS_UP)[1]
P(f"  eps_up (forest + sigma8, VHC non-barotropic) = {EPS_UP:.4e}; background c_s(z=0) {cs0_of_eps(EPS_UP):.2f} km/s, c_s(z=3) {cs0_of_eps(EPS_UP) * 0.125:.3f}, "
  f"c_s(z=2) {cs0_of_eps(EPS_UP) / 3 ** 1.5:.3f}; forest {g_up['forest']} (T2(k5) z3/z2 {g_up['T2_k5']['3']:.4f}/{g_up['T2_k5']['2']:.4f}, "
  f"bins z3 {min(g_up['bins_z3']):.3f}-{max(g_up['bins_z3']):.3f}); R_sigma8 {g_up['R_sigma8']:.4f}; T2(z=0) k 0.1/1/10 " + " / ".join(f"{v:.3f}" for v in g_up["T2_z0_at_k_0.1_1_10"]))
g_baro = grade(lambda a: cs0_of_eps(EPS_UP) * a ** 1.5, vhc=False)
P(f"  reported: same history, barotropic (X22 form) at eps_up: forest {g_baro['forest']}, T2(k5) z3 {g_baro['T2_k5']['3']:.4f}")
LATE = late_element()
P(f"  late-accreted element: turnaround at a = {LATE['a_ta']:.4f}, rho_ta/rhobar {LATE['rho_ta_rel']:.3f}, k_late = {LATE['k']:.5f} (background a^5/5 = 0.2)")
S2 = {"eps_up": EPS_UP, "cs0_up_kms": cs0_of_eps(EPS_UP), "grade_at_eps_up": g_up, "barotropic_at_eps_up": {"forest": g_baro["forest"], "T2_k5": g_baro["T2_k5"]},
      "late": LATE, "per_footing": {}}
def cs_class(eps, k):
    return C_KMS * math.sqrt(2 * eps / 3 * OL946 / OC946 * k * DTA ** (2.0 / 3.0))
for f in FOOTS:
    cn = CSNEED[f]
    e_low = (cn / C_KMS) ** 2 / (2.0 / 3.0 * OL946 / OC946 * LATE["k"] * DTA ** (2.0 / 3.0))
    e_bg = eps_of_cs0(cn)
    S2["per_footing"][f] = {"eps_low": e_low, "eps_bg": e_bg, "window": e_low <= EPS_UP, "ratio_low_over_up": e_low / EPS_UP,
                            "cs0_bg_at_eps_low": cs0_of_eps(e_low)}
    P(f"  [{f}] c_s,need {cn:.1f}: eps_low (late-accreted, brief's definition) = {e_low:.4e} (background c_s(z=0) there {cs0_of_eps(e_low):.1f} km/s); "
      f"eps_bg = {e_bg:.4e}; eps_low / eps_up = {e_low / EPS_UP:.3f} -> window {'NON-EMPTY' if e_low <= EPS_UP else 'EMPTY'}")
RES["step2"] = S2

# K3: linear limits
gz = grade(lambda a: 0.0, vhc=True)
dz = max(abs(v - 1) for v in gz["bins_z3"] + gz["bins_z2"] + list(gz["T2_k5"].values()))
_, sol = grow(0.1, lambda a: cs0_of_eps(EPS_UP) * a ** 1.5, zout=(9.0,), vhc=True, track_s=True)
ratio_s = sol.y[4][-1] / sol.y[0][-1]
# A1: 1e-10 -> 1e-7 (REF is a 4-variable LSODA run, this a 5-variable one; rtol 1e-8 noise)
k3 = dz <= 1e-7 and abs(ratio_s - (-13.0 / 18.0)) <= 1e-3
check("K3", k3, f"eps -> 0: max |T2 - 1| {dz:.1e}; s/delta at a = 0.1, k = 0.1: {ratio_s:.5f} (-13/18 = {-13 / 18:.5f})")

# ================================================================== STEP 3: classes
ZC = {"SPARC small": (1.5, 1.0, 2.5), "SPARC large": (1.2, 0.8, 2.0), "Groups": (0.8, 0.5, 1.2), "Clusters T1": (0.6, 0.4, 0.9),
      "Clusters T2": (0.5, 0.3, 0.8), "Clusters T3": (0.4, 0.2, 0.7), "MW disc": (1.2, 0.8, 2.0), "LG field": (2.0, 1.0, 4.0),
      "MW classical": (3.0, 2.0, 5.0), "MW ultra-faint": (8.0, 6.0, 10.0), "bright M31": (3.0, 2.0, 5.0), "M31 others": (4.0, 2.0, 8.0),
      "Crater II": (3.0, 2.0, 5.0), "Antlia II": (3.0, 2.0, 5.0), "Coma UDGs": (2.0, 1.0, 3.0), "UMa members": (1.2, 0.8, 2.0),
      "TDGs": (0.1, 0.02, 0.3), "DF2/DF4": (1.0, 0.5, 1.5)}
HIST = {}
for z in sorted({z for t in ZC.values() for z in t}):
    HIST[z] = history(1.0 / (1.0 + z))
P("\n== STEP 3: histories (z_c: a_c reached, a_ta, rho_vir/rhobar_c0, k = k_pre + k_post, sqrt(k/k_late) = c_s,class/c_s,need at eps_low)")
for z, h in HIST.items():
    P(f"  z_c {z:5.2f}: a_c {h['a_c']:.4f}, a_ta {h['a_ta']:.4f}, rho_ta/rhobar(a_ta) {h['rho_ta_over_mean']:.3f}, rho_vir {h['rho_vir_rel']:.4g}, "
      f"k {h['k']:.4e} (pre {h['k_pre']:.3e}, post {h['k_post']:.3e}); sqrt(k/k_late) {math.sqrt(h['k'] / LATE['k']):.4f}")
RES["histories"] = {str(z): h for z, h in HIST.items()}

X19_EXTRA = ["Clusters T2", "Clusters T3", "MW ultra-faint", "bright M31", "M31 others"]
CORE = ["SPARC small", "SPARC large", "Clusters T2", "Clusters T3"]
HCORE = ("MW ultra-faint", "bright M31", "M31 others")       # replaced by the low-M* dwarf line as the core dwarf entry (A0)

# dwarfs per system: X1 inputs (sigma, rh, logMstar), X20 E/s/P0/P1 (B_iso)
X1R = list(csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))))
X20R = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(RB, "X20_hosted_dwarf_requirement", "x20_per_system.csv")))}
DCLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")

def eval_eps(eps, f, tag):
    a0 = A0[f]
    IV = X19["intervals"][f"{f}|p16_84"]; ET = X19["E_table"][f"{f}|iso"]
    out = {"eps": eps, "classes": {}}
    wrong, unsettled = [], []
    for c, zs in ZC.items():
        iv = IV[c]; Mb, sig, rho, x = iv["M_b"][2], iv["sigma"][2], iv["rho_b"][2], iv["x"][2]
        gN = x * a0; r = 3 * gN / (4 * math.pi * G_SI * rho * MSUN946 / PC946 ** 3)
        Eo, s = ET[c]["E"], ET[c]["s"]; xl = label(ET[c]["Z"])
        labs, rows = [], []
        for z in zs:
            cs = cs_class(eps, HIST[z]["k"])
            Ep, braw, capd, _ = e_pred(Mb, r, gN, sig, a0, cs)
            labs.append(label(Ep / s)); rows.append((z, cs, braw, capd, Ep))
        lp = labs[0]
        decisive = xl in ("EXTRA", "NONE")
        sign = "n/a" if not decisive else ("RIGHT" if lp == xl else ("UNSETTLED" if lp == "AMBIGUOUS" else "WRONG"))
        Ep = rows[0][4]; zr = (Eo - Ep) / s
        if decisive and c not in HCORE:
            if sign == "WRONG": wrong.append(c)
            if sign == "UNSETTLED": unsettled.append(c)
        # variant: rho_in = fair share at the measured rho_b (reported)
        rb_rel = rho / (OB946 * RHOC_946 * PC946 ** 3 / MSUN946)
        h0 = HIST[zs[0]]
        k_var = h0["k_pre"] + (rb_rel ** (-5.0 / 3.0) * (-math.log(h0["a_c"])) if not MUT else rb_rel ** (-2.0 / 3.0) * (1 - h0["a_c"] ** 3) / 3.0)
        lab_var = label(e_pred(Mb, r, gN, sig, a0, cs_class(eps, k_var))[0] / s)
        out["classes"][c] = dict(z_c=zs, cs_kms=[q[1] for q in rows], beta=[q[2] for q in rows], captured=[q[3] for q in rows],
                                 E_pred=[q[4] for q in rows], labels=labs, robust=len(set(labs)) == 1, x19_label=xl, sign=sign,
                                 E_obs=Eo, s=s, Z_res=zr, amp="REPRODUCED" if abs(zr) < 2 else ("UNDER" if zr > 0 else "OVER"),
                                 rho_b_over_mean=rb_rel, variant_fair_share_label=lab_var)
        P(f"  [{f} {tag}] {c:15s} z_c {zs[0]:4.1f}: c_s {rows[0][1]:8.2f} km/s (lo/hi z_c {rows[1][1]:.2f}/{rows[2][1]:.2f}); sigma {sig:6.1f}; "
          f"beta {rows[0][2]:9.3g}{'*' if rows[0][3] else ' '}; E_pred {Ep:+.4f} (z_c band {min(q[4] for q in rows):+.3f}..{max(q[4] for q in rows):+.3f}); "
          f"E_obs {Eo:+.3f} +- {s:.3f}; [var {lab_var}] pred {lp:9s}{'' if len(set(labs)) == 1 else ' [band: ' + '/'.join(labs) + ']'} vs X19 {xl:9s} -> {sign}")
    # dwarfs per system (A0)
    pts = []
    for r1 in X1R:
        if r1["footing"] != f or r1["cls"] not in DCLS:
            continue
        r20 = X20R.get((f, r1["name"]))
        Mb = 10 ** float(r1["logMstar"]); r12 = 4.0 / 3.0 * float(r1["rh_pc"]) * PC946
        gN = G_SI * (Mb / 2) * MSUN946 / r12 ** 2
        sig = float(r1["sigma"])
        cs = cs_class(eps, HIST[ZC[r1["cls"]][0]]["k"])
        Ep, braw, capd, _ = e_pred(Mb / 2, r12, gN, sig, a0, cs)
        if r20 is not None:
            Eo, s, lm, lr = float(r20["E_B_iso"]), float(r20["s_B_iso"]), float(r20["P0_logMstar"]), float(r20["P1_logrh"])
        else:
            Eo, s, lm, lr = float(r1["Delta[iso AQUAL L*0]"]), float(r1["sdMC[iso AQUAL L*0]"]), float(r1["logMstar"]), math.log10(float(r1["rh_pc"]))
        siso2 = sig ** 2 * 10 ** (-Eo)
        dsig = math.sqrt(max(siso2 * (10 ** Ep - 1), 0.0))
        pts.append(dict(name=r1["name"], cls=r1["cls"], hosted=r1["cls"] != "LG field", logM=lm, logrh=lr, E_obs=Eo, s=s, E_pred=Ep,
                        lab=label(Ep / s), cs=cs, beta=braw, captured=capd, dsigma_floor_kms=dsig, ok=abs(Eo - Ep) < 2 * s))
    low = [p for p in pts if p["logM"] < 6]
    nE = sum(p["lab"] == "EXTRA" for p in low); nN = sum(p["lab"] == "NONE" for p in low)
    dline = "RIGHT" if nE > len(low) / 2 else ("WRONG" if nN > len(low) / 2 else "UNSETTLED")
    rp = spearmanr([p["E_pred"] for p in pts], [p["logM"] for p in pts])[0]
    ro = spearmanr([p["E_obs"] for p in pts], [p["logM"] for p in pts])[0]
    rpr = spearmanr([p["E_pred"] for p in pts], [p["logrh"] for p in pts])[0]
    ror = spearmanr([p["E_obs"] for p in pts], [p["logrh"] for p in pts])[0]
    fl = [p["dsigma_floor_kms"] for p in low]
    rfl = spearmanr(fl, [p["logM"] for p in low])[0]                 # A1 reported: is the increment a floor (flat in M*)?
    out["dwarfs"] = dict(N=len(pts), N_low=len(low), low_EXTRA=nE, low_NONE=nN, line=dline, rho_pred_logM=rp, rho_obs_logM=ro,
                         rho_pred_logrh=rpr, rho_obs_logrh=ror, frac_consistent=sum(p["ok"] for p in pts) / len(pts),
                         median_E_pred_low=float(np.median([p["E_pred"] for p in low])), median_E_obs_low=float(np.median([p["E_obs"] for p in low])),
                         floor_kms_low_p16_50_84=[float(np.percentile(fl, q)) for q in (16, 50, 84)], rho_floor_logM_low=rfl,
                         cs_by_class={c: cs_class(eps, HIST[ZC[c][0]]["k"]) for c in DCLS},
                         hosted_median_E_pred=float(np.median([p["E_pred"] for p in pts if p["hosted"]])),
                         field_median_E_pred=float(np.median([p["E_pred"] for p in pts if not p["hosted"]])), systems=pts)
    D = out["dwarfs"]
    P(f"  [{f} {tag}] DWARFS per system (N {D['N']}, hosted + field): log M* < 6: {D['N_low']} systems, predicted EXTRA {nE}, NONE {nN} -> line {dline}; "
      f"median E_pred {D['median_E_pred_low']:+.4f} vs E_obs {D['median_E_obs_low']:+.3f}")
    P(f"      Spearman(E, log M*) pred {rp:+.3f} vs obs {ro:+.3f}; Spearman(E, log r_half) pred {rpr:+.3f} vs obs {ror:+.3f}; "
      f"|E_obs - E_pred| < 2s: {D['frac_consistent']:.3f}; hosted / field median E_pred {D['hosted_median_E_pred']:+.4f} / {D['field_median_E_pred']:+.4f}")
    P(f"      floor reading: VHC c_s by class " + ", ".join(f"{c} {v:.2f}" for c, v in D["cs_by_class"].items()) +
      f" km/s; implied sigma increment from the retained cold (log M* < 6) p16/50/84 " + " / ".join(f"{v:.2f}" for v in D["floor_kms_low_p16_50_84"]) + f" km/s; Spearman(increment, log M*) {rfl:+.3f}")
    core_wrong = [c for c in CORE if out["classes"][c]["sign"] == "WRONG"] + (["low-M* dwarfs"] if dline == "WRONG" else [])
    core_uns = [c for c in CORE if out["classes"][c]["sign"] == "UNSETTLED"] + (["low-M* dwarfs"] if dline == "UNSETTLED" else [])
    other_wrong = [c for c in wrong if c not in CORE]
    if core_wrong:
        sc = "WRONG SIGN (" + ", ".join(core_wrong + other_wrong) + ")"
    elif other_wrong:
        sc = "RIGHT SIGN EXCEPT {" + ", ".join(other_wrong) + "}"
    elif core_uns:
        sc = "UNDECIDED (core unsettled: " + ", ".join(core_uns) + ")"
    else:
        sc = "VHC RIGHT SIGN EVERYWHERE"
    out["sign_class"] = sc; out["unsettled"] = unsettled + core_uns
    # KT trend (reported)
    kt = X21J["binned"]["V1"]["terciles"]["cells"][f"{f}|h0672"]["A"]
    ep = [out["classes"][c]["E_pred"][0] for c in ("Clusters T1", "Clusters T2", "Clusters T3")]
    out["cluster_trend"] = dict(E_pred_T1_T3=ep, rising=ep[2] > ep[0], X21_KT_tercile_A_h0672=kt)
    P(f"  [{f} {tag}] clusters: E_pred T1/T2/T3 " + " / ".join(f"{v:+.3f}" for v in ep) + f" ({'rising' if ep[2] > ep[0] else 'not rising'}); "
      f"X21 KT-tercile A_MID (h 0.672) " + " / ".join(f"{v:.2f}" for v in kt) + " (rising)")
    P(f"  [{f} {tag}] SIGN CLASS: {sc}" + (f"; unsettled: {', '.join(out['unsettled'])}" if out["unsettled"] else ""))
    return out

RES["footings"] = {}
for f in FOOTS:
    S = S2["per_footing"][f]
    evals = [("eps_low", S["eps_low"]), ("eps_up", EPS_UP)]
    for c in ("SPARC small", "SPARC large"):                     # reported: eps needed by the SPARC class's own history
        kc = HIST[ZC[c][0]]["k"]
        S[f"eps_low_{c.replace(' ', '_')}_own_history"] = S["eps_low"] * LATE["k"] / kc
        P(f"  [{f}] reported: eps for c_s,class({c}, z_c {ZC[c][0]}) = c_s,need: {S['eps_low'] * LATE['k'] / kc:.3e} = {S['eps_low'] * LATE['k'] / kc / EPS_UP:.1f} x eps_up")
    if S["window"]:
        evals.append(("eps_gm", math.sqrt(S["eps_low"] * EPS_UP)))
    P(f"\n== STEP 3/4 [{f}]: evaluated at " + ", ".join(f"{t} {e:.4e}" for t, e in evals) + ("" if S["window"] else "  (outside a window: sign diagnostic)"))
    FR = RES["footings"][f] = {"evals": {}}
    for t, e in evals:
        FR["evals"][t] = eval_eps(e, f, t)
    if not S["window"]:
        FR["verdict"] = ("NO EPS WINDOW [at eps_low: " + FR["evals"]["eps_low"]["sign_class"] + "; at eps_up: " + FR["evals"]["eps_up"]["sign_class"] + "]")
    else:
        scs = [v["sign_class"] for v in FR["evals"].values()]
        FR["verdict"] = scs[0] if len(set(scs)) == 1 else "UNDECIDED (sign class differs across eps: " + " | ".join(scs) + ")"
    P(f"  VERDICT [{f}]: {FR['verdict']}")

V = {f: RES["footings"][f]["verdict"] for f in FOOTS}
if STOP and not MUT:
    RES["verdict"] = "UNDECIDED (stop rule)"
else:
    VC = {f: V[f].split(" [")[0] for f in FOOTS}                      # A1: footings compared on the verdict class; qualifiers per footing
    RES["verdict_literal_string_compare"] = "agree" if V["canonical"] == V["alt"] else "differ (qualifiers)"
    RES["verdict"] = VC["canonical"] if VC["canonical"] == VC["alt"] else ("UNDECIDED (footings differ: " + V["canonical"] + " || " + V["alt"] + ")")
    P("  qualifiers: " + " || ".join(f"{f}: {V[f]}" for f in FOOTS))
P(f"\n=== VERDICT (both footings): {RES['verdict']}")

# ================================================================== reported
P("\n== REPORTED")
rep = {}
for f in FOOTS:
    e = S2["per_footing"][f]["eps_low"]
    rep[f] = {"eps_low": e, "thermal_fraction_of_rhoL_c2": e / 5, "w_plus_1": e / 3, "a0_drift_dex_to_z1": -e / 2 * math.log10(0.5)}
    P(f"  [{f}] at eps_low: thermal energy today = eps/5 = {e / 5:.3e} of rho_L c^2; w_L + 1 = eps/3 = {e / 3:.3e} (DESI-scale w0 + 1 ~ 0.1-0.3, PROVISIONAL); "
      f"a0 drift to z = 1: {rep[f]['a0_drift_dex_to_z1']:.2e} dex")
P(f"  at eps_up: eps/5 = {EPS_UP / 5:.3e}, w_L + 1 = {EPS_UP / 3:.3e}")
RES["reported"] = rep

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
check("K4", rss < 1.0, f"peak RSS {rss:.3f} GB")
n = sum(v["pass"] for v in RES["checks"].values())
P(f"\nchecks {n}/{len(RES['checks'])}; runtime {time.time() - T0:.1f} s")
RES["runtime_s"] = time.time() - T0; RES["peak_rss_GB"] = rss
open(os.path.join(HERE, f"x24b_vacuum_heated_cold{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x24b_vacuum_heated_cold_results{TAG}.json"), "w"), indent=1, default=str)
sys.exit(0 if n == len(RES["checks"]) else 1)
