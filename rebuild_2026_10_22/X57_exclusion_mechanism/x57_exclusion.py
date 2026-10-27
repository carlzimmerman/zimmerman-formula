#!/usr/bin/env python3
"""X57_exclusion_mechanism: what keeps full-strength cold dark energy out of galaxies (and mostly out of cluster
outskirts) without heating or converting it?  Grades classes M1-M4, M6 against R1-R7 (FROZEN_CRITERIA.md, 6cadf4f9b0);
M5 reported only.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed.  Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x57_exclusion.py   (X57_MUTATE=1 twin)
"""
import os, sys, json, math, time, resource, subprocess, tempfile, hashlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import solve_ivp, quad
import sympy as sp

MUT = os.environ.get("X57_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(REB, ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
T0 = time.time()
OUT = open(os.path.join(HERE, f"x57_exclusion{TAG}.out"), "w")
RES = {"lane": "X57_exclusion_mechanism", "criteria": "6cadf4f9b0", "mutate": MUT, "checks": {},
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


def J(rel):
    return json.load(open(os.path.join(REB, rel)))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
P("X57_exclusion_mechanism" + (" [MUTATE m1-m4: control output, not physics]" if MUT else "") +
  ": criteria 6cadf4f9b0; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")

# ============================================================== constants (X22 verbatim)
G_SI, KPC, MSUN, PC = 6.67430e-11, 3.0856775814913673e19, 1.98847e30, 3.0856775814913673e16
MPC_M = 1e6 * PC
H0 = 67.4e3 / MPC_M
RHOC = 3 * H0 ** 2 / (8 * math.pi * G_SI)
OB = 0.0493; OC = 5.364 * OB; OM = OB + OC; OL = 1 - OM
HH = 0.674
FC, FB = 5.364 / 6.364, 1.0 / 6.364
RRAT = 5.364 if not MUT else 1 / 5.364                     # m4 (M6 positivity only)

# ============================================================== STEP 0
P("\n== STEP 0: record numbers (stop rule)")
X22 = J("X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")
X34 = J("X34_recombination_release/x34_recombination_release_results.json")
X54 = J("X54_cold_de_exchange/x54_cold_de_exchange_results.json")
X55 = J("X55_one_halo_mass_for_both/x55_one_halo_results.json")
X56L = J("X56_law_floor_structure/x56_x43copy_law_x48_results.json")
X43 = J("X43_collapse_core_floor/x43_collapse_core_results.json")
X40 = J("X40b_core_surface_density_scaling/x40b_sd_scaling_results.json")
X47 = J("X47_vacuum_tethered_core_floor/x47_vt_floor_results.json")
X32 = J("X32_bullet_cold_sector/x32_bullet_cold_sector_results.json")
s2 = X22["step2"]
S0 = {
    "X22_alpha_NF": X22["step1"]["alpha_NF"]["alpha_Mpc_h"], "X22_lambda_hm": X22["step1"]["alpha_NF"]["lambda_hm_Mpc_h"],
    "X22_M_hm": X22["step1"]["alpha_NF"]["M_hm_Msun"],
    "X22_f_max": {f: s2["per_footing"][f]["f_max"] for f in FOOTS},
    "X22_mu_med": {f: s2["per_footing"][f]["Mc_max_over_Mb_at_Rlast"][2] for f in FOOTS},
    "X22_Rlast": s2["R_last_kpc_min_p16_p50_p84_max"], "X22_Vlast": s2["V_last_kms"],
    "X22_capture_med": X22["step3A"]["canonical"]["alpha_NF"]["captured_T2_min_p16_p50_p84_max"][2],
    "X22_content_virial": s2["per_footing"]["canonical"]["content_beta2_over_fair_inside_Rlast_median"],
    "X22_M_L_med": s2["per_footing"]["canonical"]["M_L_Msun"][2], "X22_R_L_med": s2["per_footing"]["canonical"]["R_L_Mpc_h"][2],
    "X22_grms": {z: X22["step3C"]["grms_m_s2"][z] for z in ("2.0", "3.0")},
    "X22_x_S": {f: X22["step3C"][f]["x"]["S"] for f in FOOTS},
    "X22_k5": X22["S0_2"]["k5_hMpc"], "X22_T2_53": X22["S0_2"]["T2_5.3keV"],
    "X34_zon_allowed": X34["Q1_summary"]["R1"]["z_on_allowed"], "X34_zon_excl": X34["Q1_summary"]["R1"]["z_on_excl"],
    "X54_int95": {k: X54["analysis"][k]["int95"] for k in ("C_DES5", "C_PP", "C_U3")}, "X54_CFG681": X54["S0"]["CFG681"],
    "X53_dchi2": {f: X55["step0_X53"][f"{f}|all|H2H"]["value"] - X55["step0_X53"][f"{f}|all|L2H"]["value"] for f in FOOTS},
    "X55_nsep": {f: X55["footings"][f]["n_sep"] for f in FOOTS},
    "X56law_OUT": {f: {hk: X56L["footings"][f]["clusters"]["cells"][hk]["G-OUT-all"] for hk in ("h0672", "h0686")} for f in FOOTS},
    "X56law_MIDT3_Z": {f: X56L["footings"][f]["clusters"]["cells"]["h0672"]["G-MID-T3"]["Z"] for f in FOOTS},
    "X43_MIDT3_Z": X43["footings"]["canonical"]["clusters"]["cells"]["h0672"]["G-MID-T3"]["Z"],
    "X43_groups_Z": X43["footings"]["canonical"]["groups"]["Z"],
    "X40b_gb": {f: [X40["footings"][f]["A"]["reported"]["gb_r0_diag"][t]["gb_over_a0"] for t in ("T1", "T2", "T3")] for f in FOOTS},
    "X47_verdicts": [X47["verdict"], X47["verdict_VT_O"]],
    "X32_tracer_fret": [X32["passages_reported"]["CDMlike|2700"]["main"]["f_ret"], X32["passages_reported"]["CDMlike|4740"]["main"]["f_ret"]],
}
RES["step0"] = S0
TGT = {  # frozen / printed record values
    "X22_alpha_NF": 0.02991, "X22_lambda_hm": 0.4167, "X22_M_hm": 4.89e9, "f_c": 0.196, "f_a": 0.0269,
    "mu_c": 0.0354, "mu_a": 0.0049, "Rlast_med": 11.27, "Vlast_med": 99.7, "capture": 0.7603, "content": 0.5405,
    "zon_ok": 5e4, "zon_x": 2e4, "xi": [-0.0035, 0.0011], "dchi2_c": 429.57, "dchi2_a": 455.55, "nsep_c": 4.55, "nsep_a": 4.26,
    "OUT_meas_c": 0.716, "OUT_meas_a": 0.656, "OUT_Z": {"canonical": (-2.01, -2.14), "alt": (-2.66, -2.80)},
    "MIDT3": 0.30, "groups": 2.05,
}
if MUT:
    TGT["dchi2_c"] += 1.0                                                    # m3
r = lambda v, d: round(float(v), d)
ok0 = [
    r(S0["X22_alpha_NF"], 5) == TGT["X22_alpha_NF"], r(S0["X22_lambda_hm"], 4) == TGT["X22_lambda_hm"],
    abs(S0["X22_M_hm"] / TGT["X22_M_hm"] - 1) < 2e-3,
    r(S0["X22_f_max"]["canonical"], 3) == TGT["f_c"], r(S0["X22_f_max"]["alt"], 4) == TGT["f_a"],
    r(S0["X22_mu_med"]["canonical"], 4) == TGT["mu_c"], r(S0["X22_mu_med"]["alt"], 4) == TGT["mu_a"],
    r(S0["X22_Rlast"][2], 2) == TGT["Rlast_med"], r(S0["X22_Vlast"][2], 1) == TGT["Vlast_med"],
    r(S0["X22_capture_med"], 4) == TGT["capture"], r(S0["X22_content_virial"], 4) == TGT["content"],
    S0["X34_zon_allowed"] == TGT["zon_ok"], S0["X34_zon_excl"] == TGT["zon_x"],
    [r(v, 4) for v in S0["X54_int95"]["C_DES5"]] == TGT["xi"],
    r(S0["X53_dchi2"]["canonical"], 2) == TGT["dchi2_c"], r(S0["X53_dchi2"]["alt"], 2) == TGT["dchi2_a"],
    r(S0["X55_nsep"]["canonical"], 2) == TGT["nsep_c"], r(S0["X55_nsep"]["alt"], 2) == TGT["nsep_a"],
    r(S0["X56law_OUT"]["canonical"]["h0672"]["meas"], 3) == TGT["OUT_meas_c"], r(S0["X56law_OUT"]["alt"]["h0672"]["meas"], 3) == TGT["OUT_meas_a"],
    all(tuple(r(S0["X56law_OUT"][f][hk]["Z"], 2) for hk in ("h0672", "h0686")) == TGT["OUT_Z"][f] for f in FOOTS),
    r(S0["X43_MIDT3_Z"], 2) == TGT["MIDT3"], r(S0["X43_groups_Z"], 2) == TGT["groups"],
]
for f in FOOTS:
    P(f"  [{f}] X22 f_max {S0['X22_f_max'][f]:.4f}; tolerated Mc/Mb median {S0['X22_mu_med'][f]:.4f}; X53 dchi2(H2H-L2H) {S0['X53_dchi2'][f]:+.2f}; "
      f"X55 n_sep {S0['X55_nsep'][f]:.2f}; law-alone G-OUT-all " + "; ".join(f"{hk} meas {c['meas']:.3f}+-{c['s']:.3f} pred {c['pred']:.3f} Z {c['Z']:+.2f}" for hk, c in S0["X56law_OUT"][f].items())
      + f"; law-alone MID T3 Z {S0['X56law_MIDT3_Z'][f]:+.2f}; X40b g_b(r0)/a0 T1-T3 " + "/".join(f"{v:.3f}" for v in S0["X40b_gb"][f]) + f"; SPARC x(R_last) {S0['X22_x_S'][f][0]:.3f}-{S0['X22_x_S'][f][1]:.3f}")
P(f"  X22 alpha_NF {S0['X22_alpha_NF']:.5f} Mpc/h, lambda_hm {S0['X22_lambda_hm']:.4f} Mpc/h, M_hm {S0['X22_M_hm']:.3e}; capture median {S0['X22_capture_med']:.4f}; "
  f"virial content {S0['X22_content_virial']:.4f}; R_last/V_last medians {S0['X22_Rlast'][2]} kpc / {S0['X22_Vlast'][2]} km/s; grms z2/z3 {S0['X22_grms']['2.0']:.3e}/{S0['X22_grms']['3.0']:.3e} m/s2")
P(f"  X34 z_on allowed {S0['X34_zon_allowed']:.0f}, excluded {S0['X34_zon_excl']:.0f}; X54 int95 " + "; ".join(f"{k} [{v[0]:+.4f}, {v[1]:+.4f}]" for k, v in S0["X54_int95"].items())
  + f"; CFG681 Om BAO {S0['X54_CFG681'][1]:.4f}, BAO+PP {S0['X54_CFG681'][3]:.4f}")
P(f"  X43 MID T3 Z {S0['X43_MIDT3_Z']:+.2f}, groups Z {S0['X43_groups_Z']:+.2f}; X47 {S0['X47_verdicts']}; X32 dust-like tracer f_ret {S0['X32_tracer_fret'][0]:.2f}-{S0['X32_tracer_fret'][1]:.2f}")


# ============================================================== X22 growth ODE (verbatim structure) + couplings
L346 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L346_switch_forest_gate_results.json")))
_b = np.array(L346["numbers"]["runs"]["lcdm"]["pk"]["3.0"])[:, 0]
KB = _b[(_b >= 1.0) & (_b <= 4.0)]
K5 = S0["X22_k5"]; T2_53 = S0["X22_T2_53"]
KF = np.concatenate([KB, [K5]])


def forest_class(tb, tk):                                                  # X22 L154-161 verbatim rule
    allb = [v for z in tb for v in tb[z]]
    k5s = list(tk.values())
    if min(k5s) < 0.9 or min(allb) < 0.5 or max(allb) > 2.0:
        return "FAIL"
    if all(0.8 <= v <= 1.2 for v in allb) and min(k5s) >= T2_53:
        return "PASS"
    return "UNDECIDED"


def grow(k_h, beta=0.0, lam=1.0, nu_w=0.0, sgn=1.0, wsgn=1.0, zout=(3.0, 2.0, 0.0), ai=1e-3):
    """X22 two-fluid ODE in N = ln a; y = [dc, dc', db, db'].  M2: cross-coupling (1 - s beta_eff);
    M4: -(nu_w k_phys^2 / 2H)^2 on the cold equation (nu_w in kpc km/s)."""
    def rhs(N, y):
        a = math.exp(N)
        E2 = OM * a ** -3 + OL
        Oma = OM * a ** -3 / E2
        dlnH = -1.5 * Oma
        be = beta / (1.0 + (a / (k_h * HH * lam)) ** 2) if beta else 0.0
        cr = 1.0 - sgn * be
        Jw = wsgn * (nu_w * 1e-3 * k_h ** 2 * HH / (200.0 * a * a * math.sqrt(E2))) ** 2 if nu_w else 0.0
        sc = 1.5 * Oma * (FC * y[0] + FB * cr * y[2])
        sb = 1.5 * Oma * (FC * cr * y[0] + FB * y[2])
        return [y[1], -(2 + dlnH) * y[1] + sc - Jw * y[0], y[3], -(2 + dlnH) * y[3] + sb]
    Ns = sorted(math.log(1 / (1 + z)) for z in zout)
    sol = solve_ivp(rhs, (math.log(ai), 0.0), [ai, ai, ai, ai], method="LSODA", rtol=1e-8, atol=1e-14, t_eval=Ns)
    out = {}
    if not sol.success or sol.y.shape[1] != len(Ns):
        return None
    for j, N in enumerate(Ns):
        out[round(1 / math.exp(N) - 1, 6)] = (sol.y[0][j], sol.y[2][j])
    return out


def D_lcdm(a):
    Ea = lambda x: math.sqrt(OM * x ** -3 + OL)
    return 2.5 * OM * Ea(a) * quad(lambda x: 1.0 / (x * Ea(x)) ** 3, 0, a, epsabs=0, epsrel=1e-12, limit=400)[0]


P("\n== K1: beta = 0 ODE vs X22 C2")
g0 = grow(1.0, zout=(0.0,))
dm0 = FC * g0[0.0][0] + FB * g0[0.0][1]
Dn = D_lcdm(1.0) / D_lcdm(1e-3) * 1e-3
REF = {float(k): grow(float(k), zout=(3.0, 2.0)) for k in KF}
tb1 = max(abs(REF[float(k)][z][1] / REF[float(k)][z][0] - 1) for k in KF for z in (3.0, 2.0))
check("K1", abs(dm0 - 0.787089) <= 1e-5 and tb1 <= 1e-10, f"delta_m(z=0) {dm0:.6f} (X22 C2 0.787089; LCDM-integral form {Dn:.6f}); max |T_b - 1| at beta 0 {tb1:.1e}",
      "<= 1e-5; <= 1e-10")


def tr(g, ref, which):
    if which == "b":
        return g[1] / ref[1]
    return (FC * g[0] + FB * g[1]) / (FC * ref[0] + FB * ref[1])


def grade_forest(which="b", **kw):
    G = {}
    for k in KF:
        g = grow(float(k), zout=(3.0, 2.0), **kw)
        if g is None:
            return "FAIL", None
        G[float(k)] = g
    tb, tk = {}, {}
    for z, zs in ((3.0, "3"), (2.0, "2")):
        tb[zs] = []
        for k in KB:
            t = tr(G[float(k)][z], REF[float(k)][z], which)
            tb[zs].append(math.copysign(t * t, t))
        t = tr(G[float(K5)][z], REF[float(K5)][z], which)
        tk[zs] = math.copysign(t * t, t)
    return forest_class(tb, tk), {"bins": tb, "k5": tk}


# ============================================================== K4 sympy: Yukawa kernel limits
P("\n== K4: sympy (PYTHONHASHSEED=" + os.environ.get("PYTHONHASHSEED", "unset") + ") Yukawa kernel limits")
k, lam_s, beta_s, Gs, rho = sp.symbols("k lambda beta G rho", positive=True)
kern = beta_s * 4 * sp.pi * Gs * rho / (k ** 2 + lam_s ** -2)                # Newton: -4 pi G rho / k^2 ; repulsive Yukawa: opposite sign
loc = sp.series(kern, k, 0, 2).removeO()
far = sp.limit(kern / (-4 * sp.pi * Gs * rho / k ** 2), k, sp.oo)
k4 = sp.simplify(loc - 4 * sp.pi * Gs * beta_s * lam_s ** 2 * rho) == 0 and sp.simplify(far + beta_s) == 0
check("K4", k4, f"k lambda << 1: Phi_Y -> {sp.simplify(loc)} (i.e. the repulsive potential +4 pi G beta lambda^2 rho_b enters cold dark energy's energy); k lambda >> 1: ratio to Newton -> {far}",
      "exact (sympy)")

# ============================================================== M1
P("\n== M1 sector-dependent coupling (cold dark energy feels GR only)")
M1 = {}
for f in FOOTS:
    fm = S0["X22_f_max"][f]
    M1[f] = {"R1": "BC PASS (GR dust growth = X22 C2)", "R3_content_lower_bound": S0["X22_content_virial"], "R3_capture_frozen_cut": S0["X22_capture_med"],
             "f_max": fm, "R3": "FAIL" if S0["X22_content_virial"] > fm else "PASS", "R4": "BC PASS", "R7": "BC PASS",
             "ratio": S0["X22_content_virial"] / fm}
    P(f"  [{f}] content inside R_last >= {S0['X22_content_virial']:.4f} of fair share (X22 virial-heated; frozen-cut capture {S0['X22_capture_med']:.4f}) vs f_max {fm:.4f}: "
      f"x{M1[f]['ratio']:.1f} over -> R3 {M1[f]['R3']}; cold collapses on its own Lagrangian scales (X22 A3 M_L/M_hm median 9.5)")
RES["M1"] = M1

# ============================================================== M2
P("\n== M2 repulsive baryon <-> cold dark energy Yukawa (beta, lambda physical)")
sgn = -1.0 if MUT else 1.0                                                     # m1
gK2 = grow(float(K5), beta=1.0, lam=10.0, sgn=sgn, zout=(3.0, 2.0))
tK2 = tr(gK2[3.0], REF[float(K5)][3.0], "b")
check("K2", tK2 < 1.0, f"beta 1, lambda 10 Mpc, k5, z 3: T_b = {tK2:.4f}", "< 1 (repulsion lowers baryon clustering)")
LAMS = np.logspace(-4, 1, 41)
BLO, BHI = 1e-4, 1e4


def m2_fail(beta, lam):
    c, _ = grade_forest("b", beta=beta, lam=lam, sgn=sgn)
    return c == "FAIL"


# coarse monotonicity check (FAIL onset)
mono = True
for lam in (1e-3, 1e-2, 1e-1, 1.0):
    seq = [m2_fail(b, lam) for b in (1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0)]
    mono = mono and all((not seq[i]) or seq[i + 1] for i in range(len(seq) - 1))
P(f"  coarse FAIL-onset monotone in beta at lambda 1e-3..1 Mpc: {mono}")
BMAX = []
for lam in LAMS:
    if not m2_fail(BLO, lam):
        if not m2_fail(BHI, lam):
            BMAX.append(BHI); continue
        lo, hi = math.log(BLO), math.log(BHI)
        for _ in range(22):
            mid = 0.5 * (lo + hi)
            if m2_fail(math.exp(mid), lam):
                hi = mid
            else:
                lo = mid
        BMAX.append(math.exp(lo))
    else:
        BMAX.append(0.0)
BMAX = np.array(BMAX)
cls_db = {}
for lam, bm in zip(LAMS[::8], BMAX[::8]):
    cls_db[f"{lam:.1e}"] = grade_forest("m", beta=max(bm, 1e-12), lam=lam, sgn=sgn)[0]
M2 = {"lambda_Mpc": LAMS.tolist(), "beta_max_R1": BMAX.tolist(), "monotone": mono, "delta_m_class_at_beta_max_reported": cls_db}
RL = S0["X22_Rlast"][2] * 1e-3                                               # Mpc
for f in FOOTS:
    mu = S0["X22_mu_med"][f]
    x = RL / LAMS
    bmin3 = (1 + mu) * np.exp(x) / (1 + x)
    x1 = 1.0 / LAMS
    bmin3b = np.exp(x1) / (1 + x1)
    bas = (1 + 5.364) * np.exp(x) / (1 + x)
    r3 = BMAX / bmin3; r3b = BMAX / bmin3b; ras = BMAX / bas
    i3, i3b = int(np.argmax(r3)), int(np.argmax(r3b))
    inter3 = [float(l) for l, q in zip(LAMS, r3) if q >= 1]
    inter3b = [float(l) for l, q in zip(LAMS, r3b) if q >= 1]
    M2[f] = {"beta_min_R3": bmin3.tolist(), "beta_min_R3b": bmin3b.tolist(), "max_ratio_R1_over_R3": float(r3[i3]), "at_lambda": float(LAMS[i3]),
             "beta_max_R1_there": float(BMAX[i3]), "beta_min_R3_there": float(bmin3[i3]), "max_ratio_R1_over_R3b": float(r3b[i3b]), "at_lambda_b": float(LAMS[i3b]),
             "max_ratio_R1_over_assembly_reported": float(np.max(ras)), "lambda_allowed_R1_and_R3": inter3, "lambda_allowed_R1_and_R3b": inter3b}
    M2[f]["R1R3"] = "PASS (non-empty)" if inter3 else "FAIL"
    M2[f]["R1R3b"] = "PASS (non-empty)" if inter3b else "FAIL"
    P(f"  [{f}] R1 x R3 (median R_last {RL * 1e3:.2f} kpc, mu {mu:.4f}): max_lambda beta_max^R1/beta_min^R3 = {r3[i3]:.3g} at lambda {LAMS[i3]:.2e} Mpc "
      f"(beta_max {BMAX[i3]:.3g}, beta_min {bmin3[i3]:.3g}) -> {M2[f]['R1R3']}; R1 x R3b (1 Mpc): max ratio {r3b[i3b]:.3g} at lambda {LAMS[i3b]:.2e} -> {M2[f]['R1R3b']}; "
      f"assembly (reported) max ratio {np.max(ras):.3g}")
P("  beta_max^R1(lambda) [gas forest not FAIL]: " + ", ".join(f"{l:.0e}:{b:.3g}" for l, b in zip(LAMS[::4], BMAX[::4])))
# R4 illustrative cluster core (only meaningful if R1xR3 non-empty)
G_pc = 4.30091e-3                                                              # pc (km/s)^2 / Msun
for f in FOOTS:
    if M2[f]["lambda_allowed_R1_and_R3"]:
        lam = M2[f]["lambda_allowed_R1_and_R3"][-1]
        b = float(BMAX[list(LAMS).index(lam)])
        phi = 4 * math.pi * G_pc * b * (lam * 1e6) ** 2 * 3.4e-4
        M2[f]["R4_PhiY_over_sigma2"] = phi / 1e6
        M2[f]["R4"] = "PASS" if phi / 1e6 <= 0.1 else "FAIL"
        P(f"  [{f}] R4 at lambda {lam:.2e} Mpc, beta {b:.3g}: 4 pi G beta lambda^2 rho_gas / sigma^2 = {phi / 1e6:.3g} -> {M2[f]['R4']}")
    else:
        M2[f]["R4"] = "not graded (R1 x R3 empty)"
M2["EP"] = ("derived (ledger A9): the force acts only between baryons and cold dark energy; on Earth its source is cold dark energy within lambda, "
            "which R3 itself requires to be excluded; composition dependence enters only via mass-per-baryon differences; no external EP bound used")
RES["M2"] = M2

# ============================================================== M3
P("\n== M3 repulsion from the law's own field (phantom), sign s = +1 (outward)")


def nu1(y):
    return 0.5 + math.sqrt(0.25 + 1.0 / y)


M3 = {}
Mb_med = S0["X22_M_L_med"] / 6.364
for f in FOOTS:
    Q = {}
    for z in ("2.0", "3.0"):
        xl = S0["X22_grms"][z] / A0[f]
        y = FB * xl
        Q[z] = (nu1(y) - 1) * FB / FC
    xs, gb = S0["X22_x_S"][f], S0["X40b_gb"][f]
    inside = (min(gb) >= xs[0]) and (max(gb) <= xs[1])
    rstar = 5.364 * math.sqrt(G_SI * Mb_med * MSUN / A0[f]) / KPC
    M3[f] = {"Q_linear": Q, "R1_L": "FAIL" if min(Q.values()) >= 1 else "PASS", "R6_V": "FAIL (local x key cannot separate; becomes M5)",
             "cluster_x": gb, "sparc_x": xs, "R4": "FAIL" if inside else "PASS", "r_star_kpc_median_Mb": rstar, "Mb_median": Mb_med}
    P(f"  [{f}] (L) linear phantom / cold self-gravity Q(z=2) {Q['2.0']:.2f}, Q(z=3) {Q['3.0']:.2f} -> R1 {M3[f]['R1_L']}; "
      f"(V) R6 FAIL; R4: cluster x_b(r0) {min(gb):.3f}-{max(gb):.3f} inside SPARC x(R_last) {xs[0]:.3f}-{xs[1]:.3f}: {inside} -> {M3[f]['R4']}; "
      f"object scale r* = 5.364 sqrt(G M_b/a0) = {rstar:.1f} kpc (median M_b {Mb_med:.2e})")
RES["M3"] = M3

# ============================================================== M4
P("\n== M4 wave / coherence scale (field-energy parameter nu_w, kpc km/s)")
wsgn = -1.0 if MUT else 1.0                                                    # m2
nu1_ = 0.1
seq = []
for nv in (0.0, nu1_, 2 * nu1_, 4 * nu1_):
    g = grow(float(K5), nu_w=nv, wsgn=wsgn, zout=(3.0, 2.0))
    seq.append(tr(g[3.0], REF[float(K5)][3.0], "m") ** 2 if g else float("nan"))
check("K3", all(seq[i + 1] <= seq[i] + 1e-12 for i in range(3)), f"T2(k5, z=3) at nu_w 0/0.1/0.2/0.4 = " + "/".join(f"{v:.5f}" for v in seq), "non-increasing")


def m4_fail(nv):
    return grade_forest("m", nu_w=nv, wsgn=wsgn)[0] == "FAIL"


lo, hi = math.log(1e-4), math.log(1e3)
if m4_fail(math.exp(lo)):
    numax = 0.0
else:
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if m4_fail(math.exp(mid)):
            hi = mid
        else:
            lo = mid
    numax = math.exp(lo)
SD = os.path.join(REPO, "real_research", "data", "sparc_data")
RLs, VLs = [], []
for fn in sorted(os.listdir(SD)):
    if not fn.endswith("_rotmod.dat"):
        continue
    try:
        dd = np.genfromtxt(os.path.join(SD, fn), comments="#")
    except Exception:
        continue
    if dd.ndim != 2 or dd.shape[1] < 6:
        continue
    RLs.append(dd[-1, 0]); VLs.append(dd[-1, 1])
RLs, VLs = np.array(RLs), np.array(VLs)
rw = 2 * math.pi * numax / VLs
frac = float(np.mean(rw >= RLs))
nuneed = RLs * VLs / (2 * math.pi)
rw_cl = 2 * math.pi * numax / 1000.0 * 1e-3                                    # Mpc at sigma 1000 km/s
M4 = {"nu_w_max_kpc_kms": numax, "nu_w_max_m2_s": numax * KPC * 1e3, "N_sparc": int(len(RLs)), "median_rw_over_Rlast": float(np.median(rw / RLs)),
      "frac_rw_ge_Rlast": frac, "nu_need_median": float(np.median(nuneed)), "need_over_max": float(np.median(nuneed) / numax) if numax else float("inf"),
      "R3": "PASS" if frac >= 0.5 else "FAIL", "r_w_cluster_Mpc": rw_cl, "R4": "PASS" if rw_cl <= 0.27 else "FAIL",
      "scaling": "r_w = 2 pi nu_w / V: shrinks with mass (largest cores in the smallest objects)"}
P(f"  R1: nu_w,max (delta_m forest not FAIL) = {numax:.4g} kpc km/s ({numax * KPC * 1e3:.3e} m^2/s)")
P(f"  R3: SPARC N {len(RLs)}: median r_w/R_last {M4['median_rw_over_Rlast']:.3g}; fraction with r_w >= R_last {frac:.3f} -> {M4['R3']}; "
  f"nu_need (median R_last V_last / 2 pi) {M4['nu_need_median']:.4g} = x{M4['need_over_max']:.3g} nu_w,max")
P(f"  R4: r_w at sigma 1000 km/s = {rw_cl:.3g} Mpc vs core 0.27 Mpc -> {M4['R4']}; sign: {M4['scaling']}")
RES["M4"] = M4

# ============================================================== M6
P("\n== M6 displacement (compensated anticorrelated patches)")
fV, din, Fb = sp.symbols("f_V delta_in F_b", positive=True)
rr = sp.Rational(5364, 1000)
M6 = {}
for f in FOOTS:
    fm = S0["X22_f_max"][f]
    dci = -(1 - fm)
    dbi = -RRAT * dci
    fvmax = 1.0 / (1.0 + 5.364 * (1 - fm))
    grid = np.arange(0, 1, 1e-6)
    dco = -grid * dci / (1 - grid)                                           # compensating outside cold
    okp = (1 + (-RRAT * dco)) >= -1e-15
    fv_brute = float(grid[okp][-1])
    M6[f] = {"delta_c_in": dci, "delta_b_in": dbi, "fV_max": fvmax, "fV_brute": fv_brute}
k5ok = all(abs(M6[f]["fV_brute"] - M6[f]["fV_max"]) <= 1e-5 for f in FOOTS)
check("K5", k5ok, "; ".join(f"{f}: closed {M6[f]['fV_max']:.6f} brute {M6[f]['fV_brute']:.6f}" for f in FOOTS), "<= 1e-5")
# forest: adiabatic sigma at R_L (record BBKS shape, EM1 sigma8)
h_m, Om_m, Ob_m, ns_m = 0.674, 0.315, 0.0493, 0.965
Gam = Om_m * h_m * np.exp(-Ob_m * (1.0 + np.sqrt(2 * h_m) / Om_m))
Tk = lambda kk: (np.log(1 + 2.34 * kk / Gam) / (2.34 * kk / Gam) * (1 + 3.89 * kk / Gam + (16.1 * kk / Gam) ** 2 + (5.46 * kk / Gam) ** 3 + (6.71 * kk / Gam) ** 4) ** -0.25)
kf = np.logspace(-4, 3, 4000)
W = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
shape = kf ** (3 + ns_m) * Tk(kf) ** 2
norm = 0.82742 ** 2 / np.trapz(shape * W(kf * 8.0) ** 2, np.log(kf))
RLm = S0["X22_R_L_med"]
s2R0 = norm * np.trapz(shape * W(kf * RLm) ** 2, np.log(kf))
for f in FOOTS:
    di = -RRAT * M6[f]["delta_c_in"]
    per = di ** 2 / (1 + di)
    fb = {}
    for z in (3.0, 2.0):
        Dz = D_lcdm(1 / (1 + z)) / D_lcdm(1.0)
        fb[str(z)] = 0.2 * s2R0 * Dz ** 2 / per
    fbm = min(fb.values())
    M6[f].update({"sigma2_ad_RL_z0": float(s2R0), "var_per_Fb": per, "Fb_max": fb, "R1": "FAIL" if fbm < 0.01 else "ND"})
    P(f"  [{f}] delta_c,in {M6[f]['delta_c_in']:+.3f} -> delta_b,in {M6[f]['delta_b_in']:+.2f}; positivity f_V <= {M6[f]['fV_max']:.3f} (all baryons in patches at the bound); "
      f"sigma^2_ad(R_L {RLm:.3f} Mpc/h, z 0) {s2R0:.2f}; isocurvature var >= {per:.2f} F_b; forest F_b,max z3 {fb['3.0']:.3f} / z2 {fb['2.0']:.3f} -> R1 {M6[f]['R1']}")
# CMB through X34's vanilla CLASS
VAN = os.path.join(EXT, "class_aest_build_2026_10_22", "class_vanilla", "class")
C7 = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C7_aest_class", "c7_native_results.json")))["fits"]["LCDM"]["params"]
wb, wc = C7["omega_b"], C7["omega_dm(FITTED)"]
RUN = os.path.join(tempfile.gettempdir(), "x57_class_runs" + TAG); os.makedirs(RUN, exist_ok=True)


def run_class(name, extra):
    p = {"output": "tCl", "lensing": "no", "l_max_scalars": 2500, "T_cmb": 2.7255, "overwrite_root": "yes", "write_parameters": "no",
         "omega_b": wb, "omega_cdm": wc, "100*theta_s": C7["100theta_s"], "ln10^{10}A_s": C7["ln10^10A_s"], "n_s": C7["n_s"], "tau_reio": C7["tau"], **extra}
    root = os.path.join(RUN, name + "_"); p["root"] = root
    with open(root + ".ini", "w") as fh:
        for a_, b_ in p.items():
            fh.write(f"{a_} = {b_}\n")
    rr_ = subprocess.run(["nice", "-n", "15", VAN, root + ".ini"], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
    if rr_.returncode != 0:
        return None
    return np.loadtxt(root + "_cl.dat")


cmb = {"binary_sha256": sha(VAN) if os.path.exists(VAN) else None}
if os.path.exists(VAN):
    base = run_class("ad", {"ic": "ad"})
    comp = run_class("cip", {"ic": "ad,cdi,bi", "f_cdi": 1.0, "n_cdi": C7["n_s"], "f_bi": wc / wb, "n_bi": C7["n_s"], "c_cdi_bi": -1.0, "c_ad_cdi": 0.0, "c_ad_bi": 0.0})
    ctrl = run_class("cdi", {"ic": "ad,cdi", "f_cdi": 1.0, "n_cdi": C7["n_s"], "c_ad_cdi": 0.0})
    if base is not None and comp is not None and ctrl is not None:
        n = min(len(base), len(comp), len(ctrl))
        tt0 = base[:n, 1]
        cmb["max_rel_TT_compensated"] = float(np.max(np.abs(comp[:n, 1] / tt0 - 1)))
        cmb["max_rel_TT_uncompensated_control"] = float(np.max(np.abs(ctrl[:n, 1] / tt0 - 1)))
        cmb["class"] = "ND (linear CMB blind)" if cmb["max_rel_TT_compensated"] < 1e-3 else "SENSITIVE"
        P(f"  CMB (X34 vanilla CLASS, C7 params): max |dC_l^TT/C_l| l 2-2500: compensated (f_bi = omega_c/omega_b, c_cdi_bi = -1) {cmb['max_rel_TT_compensated']:.2e}; "
          f"uncompensated control {cmb['max_rel_TT_uncompensated_control']:.2e} -> {cmb['class']}")
    else:
        cmb["class"] = "CLASS run failed"; P("  CMB: CLASS run failed")
else:
    cmb["class"] = "binary absent"; P("  CMB: vanilla CLASS binary absent")
M6["CMB"] = cmb
RES["M6"] = M6

# ============================================================== R4b common line
P("\n== R4b common line: the law on cluster baryons vs X30 OUTER (coordinator)")
NPZ = os.path.join(REB, "X7_cluster_core_significance", "x7_measure_percluster.npz")
Mgas = float(np.median(np.load(NPZ)["Mgas500"]))
rhoc_bar = OC * RHOC * MPC_M ** 3 / MSUN                                       # Msun / Mpc^3
Mhole = 4 * math.pi / 3 * 27.0 * rhoc_bar
D = Mhole / Mgas
R4B = {"M_gas500_median": Mgas, "rho_c_bar_Msun_Mpc3": rhoc_bar, "M_hole_3Mpc": Mhole, "D": D}
for f in FOOTS:
    c = S0["X56law_OUT"][f]
    lawfail = all(abs(c[hk]["Z"]) > 2.0 for hk in ("h0672", "h0686"))
    need = 1 - c["h0672"]["meas"]
    grade = "FAIL" if (lawfail and D < need) else ("ND (evacuated-region bound not excluding)" if lawfail else "PASS")
    R4B[f] = {"law_Z": [c["h0672"]["Z"], c["h0686"]["Z"]], "law_fails_both_cells": lawfail, "needed_drop": need, "grade": grade}
    P(f"  [{f}] law alone G-OUT-all Z {c['h0672']['Z']:+.2f} / {c['h0686']['Z']:+.2f} (pred {c['h0672']['pred']:.3f}); evacuated-region bound D = "
      f"{Mhole:.3e}/{Mgas:.3e} = {D:.3f} vs needed drop {need:.3f} -> R4b {grade}")
# reported (post-freeze diagnostic, not graded): shear of a uniform evacuated sphere relative to M/(pi R^2) at R = 2 Mpc
Re, Rp = 3.0, 2.0
Sig = 2 * math.sqrt(Re ** 2 - Rp ** 2)
Mp = 4 * math.pi / 3 * (Re ** 3 - (Re ** 2 - Rp ** 2) ** 1.5)
R4B["reported_uniform_hole_dSigma_over_M_piR2"] = (Mp / (math.pi * Rp ** 2) - Sig) / (4 * math.pi / 3 * Re ** 3 / (math.pi * Rp ** 2))
P(f"  reported only: a uniform evacuated 3 Mpc sphere gives dSigma(2 Mpc) = {R4B['reported_uniform_hole_dSigma_over_M_piR2']:.3f} of M_hole/(pi R^2); "
  f"and only classes that empty cluster outskirts below the cosmic mean can use it (M1 and M4 do not)")
RES["R4b"] = R4B

# ============================================================== class verdicts
P("\n== CLASS VERDICTS (frozen order R1, R3, R3b, R4, R4b, R6)")
V = {}
for f in FOOTS:
    rb = R4B[f]["grade"]
    rows = {
        "M1": [("R3", M1[f]["R3"], f"content >= {M1[f]['R3_content_lower_bound']:.3f} vs f_max {M1[f]['f_max']:.3f}"), ("R4b", rb, "")],
        "M2": [("R1xR3", M2[f]["R1R3"], f"max beta_max^R1/beta_min^R3 {M2[f]['max_ratio_R1_over_R3']:.3g} at lambda {M2[f]['at_lambda']:.1e} Mpc"),
               ("R1xR3b", M2[f]["R1R3b"], f"max ratio {M2[f]['max_ratio_R1_over_R3b']:.3g}"), ("R4", M2[f]["R4"], ""), ("R4b", rb, "")],
        "M3": [("R1", M3[f]["R1_L"], f"Q {M3[f]['Q_linear']['2.0']:.2f}-{M3[f]['Q_linear']['3.0']:.2f} (reading L); reading V: R6 FAIL"),
               ("R4", M3[f]["R4"], f"cluster x {min(M3[f]['cluster_x']):.3f}-{max(M3[f]['cluster_x']):.3f} within SPARC {M3[f]['sparc_x'][0]:.3f}-{M3[f]['sparc_x'][1]:.3f}"), ("R4b", rb, "")],
        "M4": [("R3", M4["R3"], f"r_w/R_last median {M4['median_rw_over_Rlast']:.3g}; nu_need/nu_max {M4['need_over_max']:.3g}"), ("R4", M4["R4"], ""), ("R4b", rb, "")],
        "M6": [("R1", M6[f]["R1"], f"F_b,max {min(M6[f]['Fb_max'].values()):.3f}"), ("CMB", M6["CMB"].get("class", ""), ""), ("R4b", rb, "")],
    }
    V[f] = {}
    for m, rw_ in rows.items():
        fails = [(n, d) for n, g, d in rw_ if str(g).startswith("FAIL")]
        nds = [n for n, g, d in rw_ if str(g).startswith("ND")]
        fails_wo_r4b = [n for n, d in fails if n != "R4b"]
        if fails:
            v = f"CLASS {m[1]} EXCLUDED BY {fails[0][0]}" + (f" ({fails[0][1]})" if fails[0][1] else "")
        elif nds:
            v = "NOT DECIDABLE WITH RECORD DATA (" + ", ".join(nds) + ")"
        else:
            v = f"CLASS {m[1]} VIABLE"
        V[f][m] = {"verdict": v, "all_fails": [n for n, d in fails], "excluded_without_R4b": bool(fails_wo_r4b), "lines": [(n, str(g), d) for n, g, d in rw_]}
        P(f"  [{f}] {m}: {v}; all failing lines {[n for n, d in fails]}; excluded without R4b: {bool(fails_wo_r4b)}")
RES["verdicts"] = V
excl = {m: all(V[f][m]["verdict"].startswith(f"CLASS {m[1]} EXCLUDED") for f in FOOTS) for m in ("M1", "M2", "M3", "M4", "M6")}
viab = {m: all("VIABLE" in V[f][m]["verdict"] for f in FOOTS) for m in excl}
if all(excl.values()):
    overall = "NO GRADED CLASS VIABLE"
elif any(viab.values()):
    overall = "CLASS(ES) " + ", ".join(m for m in viab if viab[m]) + " VIABLE"
else:
    overall = "UNDECIDED"
RES["overall"] = overall
RES["overall_robust_without_R4b"] = {m: all(V[f][m]["excluded_without_R4b"] for f in FOOTS) for m in excl}
P(f"\n=== OVERALL (frozen rule): {overall}; excluded without R4b on both footings: {RES['overall_robust_without_R4b']}")
P("    M5 (object-keyed, nonlocal): REPORTED ONLY (see README; X58_object_keyed_switch runs it operationally)")

# ============================================================== checks summary
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9 + resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e9   # macOS: bytes
check("K0", all(ok0) and mono, f"{sum(ok0)}/{len(ok0)} step-0 items exact; M2 FAIL-onset monotone {mono}", "all")
check("K6", rss < 1.0 and os.environ.get("OMP_NUM_THREADS") == "1", f"peak RSS (self + children) {rss:.3f} GB; OMP_NUM_THREADS {os.environ.get('OMP_NUM_THREADS')}", "< 1 GB, 1 thread")
RES["elapsed_s"] = round(time.time() - T0, 1); RES["peak_rss_GB"] = round(rss, 3)
need_fail = {"K0", "K2", "K3", "K5"}
if MUT:
    good = all((not RES["checks"][c]["pass"]) == (c in need_fail) for c in RES["checks"])
    P(f"\nMUTATE: required-failing {sorted(need_fail)}; observed failing {sorted(c for c in RES['checks'] if not RES['checks'][c]['pass'])}; twin {'OK' if good else 'BROKEN'}")
    RES["mutate_twin_ok"] = good
json.dump(RES, open(os.path.join(HERE, f"x57_exclusion_results{TAG}.json"), "w"), indent=1, default=float)
P(f"checks {sum(c['pass'] for c in RES['checks'].values())}/{len(RES['checks'])}; {RES['elapsed_s']} s; RSS {rss:.3f} GB")
sys.exit(1 if (MUT or not all(c["pass"] for c in RES["checks"].values())) else 0)
