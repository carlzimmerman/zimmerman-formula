#!/usr/bin/env python3
"""X63_displacement_forest_prediction: X57's class M6 (displacement: galaxies form in cold dark energy deficits,
compensated anticorrelated initial patches) -> predicted small-scale Lyman-alpha gas 1D-power excess at z 4.2-5.4,
and whether the record's own forest gates (X22 forest_class: L346 bands + L319 line) already exclude it.
FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md committed alone first (ddd98ade21).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
no fitting; no downloads; not theory closed.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x63_m6_forest.py      (X63_MUTATE=1 twin)
"""
import os, sys, json, math, time, resource, re
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import quad

MUT = os.environ.get("X63_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(REB, ".."))
T0 = time.time()
OUT = open(os.path.join(HERE, f"x63_m6_forest{TAG}.out"), "w")
RES = {"lane": "X63_displacement_forest_prediction", "criteria": "ddd98ade21", "mutate": MUT, "checks": {},
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; "
                   "no fitting; no downloads; not theory closed"}
trapz = getattr(np, "trapezoid", None) or np.trapz


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


def J(rel):
    return json.load(open(os.path.join(REPO, rel)))


FOOTS = ("canonical", "alt")
P("X63_displacement_forest_prediction" + (" [MUTATE m1-m3: control output, not physics]" if MUT else "") +
  ": criteria ddd98ade21; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")

# ============================================================== constants (X22 / X57 verbatim)
OB = 0.0493; OC = 5.364 * OB; OM = OB + OC; OL = 1 - OM
HH = 0.674
RRAT = 5.364


def Ez(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def D_lcdm(a):                                                     # X57 L175-177 (X22 background)
    Ea = lambda x: math.sqrt(OM * x ** -3 + OL)
    return 2.5 * OM * Ea(a) * quad(lambda x: 1.0 / (x * Ea(x)) ** 3, 0, a, epsabs=0, epsrel=1e-12, limit=400)[0]


def Dz(z):
    return D_lcdm(1 / (1 + z)) / D_lcdm(1.0)


# ============================================================== STEP 0 (stop rule)
P("\n== STEP 0: record numbers (stop rule)")
X57 = J("rebuild_2026_10_22/X57_exclusion_mechanism/x57_exclusion_results.json")
X22 = J("rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")
X4J = J("rebuild_2026_10_22/X4_growth_native_cap/x4_dbi_door_results.json")
L346 = J("real_research/g03_audit_2026/L346_switch_forest_gate_results.json")
L347_TXT = open(os.path.join(REPO, "real_research", "g03_audit_2026", "L347_switch_forest_flux_power.py")).read()
M6J = X57["M6"]
ok0 = []
TGT = {"canonical": {"dci": -0.804, "dbi": 4.31, "fV": 0.188, "Fb3": 0.060, "Fb2": 0.106},
       "alt": {"dci": -0.973, "dbi": 5.22, "fV": 0.161, "Fb3": 0.048, "Fb2": 0.084}}
for f in FOOTS:
    m = M6J[f]
    ok0 += [round(m["delta_c_in"], 3) == TGT[f]["dci"], round(m["delta_b_in"], 2) == TGT[f]["dbi"], round(m["fV_max"], 3) == TGT[f]["fV"],
            round(m["Fb_max"]["3.0"], 3) == TGT[f]["Fb3"], round(m["Fb_max"]["2.0"], 3) == TGT[f]["Fb2"]]
ok0.append(round(M6J["CMB"]["max_rel_TT_compensated"], 7) == 7.4e-6)
# recompute sigma^2_ad(R_L, 0) and F_b,max with X57's code (L411-428)
h_m, Om_m, Ob_m, ns_m, S8 = 0.674, 0.315, 0.0493, 0.965, 0.82742
Gam = Om_m * h_m * np.exp(-Ob_m * (1.0 + np.sqrt(2 * h_m) / Om_m))
Tk = lambda kk: (np.log(1 + 2.34 * kk / Gam) / (2.34 * kk / Gam) * (1 + 3.89 * kk / Gam + (16.1 * kk / Gam) ** 2 + (5.46 * kk / Gam) ** 3 + (6.71 * kk / Gam) ** 4) ** -0.25)
W = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
kf = np.logspace(-4, 3, 4000)
shape = kf ** (3 + ns_m) * Tk(kf) ** 2
NORM = S8 ** 2 / trapz(shape * W(kf * 8.0) ** 2, np.log(kf))
RL = X22["step2"]["per_footing"]["canonical"]["R_L_Mpc_h"][2]
s2R0 = NORM * trapz(shape * W(kf * RL) ** 2, np.log(kf))
dev_s2 = abs(s2R0 / M6J["canonical"]["sigma2_ad_RL_z0"] - 1)
FBMAX = {}
dev_fb = 0.0
for f in FOOTS:
    di = -RRAT * M6J[f]["delta_c_in"]
    per = di ** 2 / (1 + di)
    dev_fb = max(dev_fb, abs(per / M6J[f]["var_per_Fb"] - 1))
    FBMAX[f] = {z: 0.2 * s2R0 * Dz(float(z)) ** 2 / per for z in ("3.0", "2.0")}
    for z in ("3.0", "2.0"):
        cmpv = M6J[f]["Fb_max"][z] * (1.01 if (MUT and f == "canonical" and z == "3.0") else 1.0)     # m3
        dev_fb = max(dev_fb, abs(FBMAX[f][z] / cmpv - 1))
ok0 += [dev_s2 <= 1e-9, dev_fb <= 1e-9]
# X22 forest numbers + L346 bins / bands vs X4 F0a
K5 = X22["S0_2"]["k5_hMpc"]; T2_53 = X22["S0_2"]["T2_5.3keV"]
ok0 += [round(K5, 4) == 4.6199, round(T2_53, 5) == 0.99519, round(X22["step1"]["alpha_NF"]["alpha_Mpc_h"], 5) == 0.02991,
        round(X22["step1"]["alpha_NF"]["lambda_hm_Mpc_h"], 4) == 0.4167, round(RL, 3) == 0.442, abs(RL - X57["step0"]["X22_R_L_med"]) <= 1e-12]
runs346 = L346["numbers"]["runs"]


def r346(name, z):
    a = np.array(runs346[name]["pk"][z]); b = np.array(runs346["lcdm"]["pk"][z])
    kk = b[:, 0]; fo = (kk >= 1.0) & (kk <= 4.0)
    return kk[fo], (a[:, 1] / b[:, 1])[fo]


KB = r346("sw5_canon", "3.0")[0]
devb = max(abs(v) for v in (KB - np.array(X4J["F0a"]["bins_hMpc"])))
devband = max(abs((lambda rr: (rr.min(), rr.max()))(r346(n, z)[1])[i] - X4J["F0a"]["bands"][f"{n}_{z}"][i])
              for n in ("sw5_canon", "sw5_alt", "never_on") for z in ("3.0", "2.0") for i in (0, 1))
ok0 += [len(KB) == 6, round(KB[0], 3) == 1.101, round(KB[-1], 3) == 3.557, devb <= 1e-9, devband <= 1e-9]
mRJ = re.search(r"R_J = ([0-9.]+) Mpc/h", L347_TXT)
RJ0 = float(mRJ.group(1)) if mRJ else None
ok0.append(RJ0 == 0.1)
S0 = {"X57_M6": {f: {k: M6J[f][k] for k in ("delta_c_in", "delta_b_in", "fV_max", "Fb_max", "var_per_Fb")} for f in FOOTS},
      "X57_CMB_comp": M6J["CMB"]["max_rel_TT_compensated"], "sigma2_ad_RL_z0_recomputed": s2R0, "dev_sigma2": dev_s2,
      "Fb_max_recomputed": FBMAX, "dev_Fb": dev_fb, "X22_k5": K5, "X22_T2_53": T2_53, "X22_R_L_med": RL,
      "L346_bins": KB.tolist(), "dev_bins": devb, "dev_bands": devband, "L347_R_J": RJ0, "n_items": len(ok0), "n_ok": int(sum(ok0))}
RES["step0"] = S0
for f in FOOTS:
    m = M6J[f]
    P(f"  [{f}] X57 M6: delta_c,in {m['delta_c_in']:+.4f}, delta_b,in {m['delta_b_in']:+.4f}, f_V <= {m['fV_max']:.4f}, "
      f"F_b,max z3 {m['Fb_max']['3.0']:.5f} / z2 {m['Fb_max']['2.0']:.5f} (recomputed {FBMAX[f]['3.0']:.5f} / {FBMAX[f]['2.0']:.5f})")
P(f"  sigma^2_ad(R_L {RL:.4f} Mpc/h, z 0) {s2R0:.6f} (X57 {M6J['canonical']['sigma2_ad_RL_z0']:.6f}, rel dev {dev_s2:.1e}); F_b rel dev {dev_fb:.1e}; "
  f"CMB compensated {M6J['CMB']['max_rel_TT_compensated']:.2e}")
P(f"  X22 k5 {K5:.4f} h/Mpc, T2_5.3keV {T2_53:.5f}; L346 bins {np.round(KB, 3).tolist()} (dev vs X4 {devb:.1e}, bands {devband:.1e}); L347 R_J {RJ0} Mpc/h")
check("K0", all(ok0), f"{sum(ok0)}/{len(ok0)} Step-0 items", "all reproduce")
if not all(ok0) and not MUT:
    P("STOP: Step 0 failed; nothing graded.")
    RES["verdict"] = "STOPPED AT STEP 0"
    json.dump(RES, open(os.path.join(HERE, f"x63_m6_forest_results{TAG}.json"), "w"), indent=1)
    sys.exit(1)

# ============================================================== spectra
KMAX = 200.0
KG = np.logspace(-4, math.log10(KMAX), 60001)                      # fine grid for the 1D projection
LNK = np.log(KG)


def P_ad0(k):                                                      # linear adiabatic, z = 0, (Mpc/h)^3
    k = np.asarray(k, float)
    return 2 * math.pi ** 2 * NORM * k ** (3 + ns_m) * Tk(k) ** 2 / k ** 3


def p1d(p3d_on_grid, kpar):
    """P1D(k_par) = (1/2pi) int_{k_par}^{KMAX} k P3D dk = (1/2pi) int k^2 P3D dlnk on KG."""
    f = KG ** 2 * p3d_on_grid
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(LNK))])
    tail = cum[-1] - np.interp(np.log(kpar), LNK, cum)
    return tail / (2 * math.pi)


# K1 projection identity
s_ = 0.3
kp_t = np.array([0.5, 2.0, 5.0])
num = p1d(np.exp(-KG ** 2 * s_ ** 2), kp_t)
ana = np.exp(-kp_t ** 2 * s_ ** 2) / (4 * math.pi * s_ ** 2)
k1dev = float(np.max(np.abs(num / ana - 1)))
check("K1", k1dev <= 1e-6, f"Gaussian P3D: max |P1D_num/P1D_analytic - 1| = {k1dev:.2e}", "<= 1e-6")

VP = 4 * math.pi * RL ** 3 / 3
PAD0_G = P_ad0(KG)
W2G = W(KG * RL) ** 2
s2ad_chk = trapz(KG ** 3 * PAD0_G / (2 * math.pi ** 2) * W2G, LNK)
ZREF = 3.0
D3 = Dz(ZREF)


def iso_amp(f, amp_scale=1.0):
    """f_V delta_b,in^2 V_p for the primary amplitude F_b = F_b,max(z=3); m1 flips the anticorrelation sign."""
    dci = M6J[f]["delta_c_in"]
    if MUT:
        dci = -dci                                                  # m1: patches ENRICHED in cold dark energy
    dbi = -RRAT * dci
    Fb = M6J[f]["Fb_max"]["3.0"]
    fV = Fb / (1 + dbi)
    sgn = 1.0 if dbi > -1 else -1.0                                 # negative baryon density -> negative "power" (unphysical)
    return {"delta_c_in": dci, "delta_b_in": dbi, "F_b": Fb, "f_V": fV, "A": amp_scale * sgn * abs(fV) * dbi ** 2 * VP}


def ratio_grid(A, zs, kh_by_z, RJ, iso_growth=False):
    """R = 1 + P1D_iso/P1D_ad on the grid (gas filter exp(-k^2 RJ^2) in power)."""
    filt = np.exp(-KG ** 2 * RJ ** 2)
    piso = A * W2G * filt
    out = {}
    for z in zs:
        D = Dz(z)
        gz = (D / D3) ** 2 if iso_growth else 1.0                   # m2: isocurvature grows like D^2
        pa = p1d(PAD0_G * D ** 2 * filt, kh_by_z[z])
        pi = p1d(piso * gz, kh_by_z[z])
        out[z] = 1.0 + pi / pa
    return out


ZP = [4.2, 4.6, 5.0, 5.4]
ZR = [3.0, 2.0]
KV = np.logspace(math.log10(0.005), math.log10(0.1), 20)            # s/km
kv2kh = lambda kv, z: kv * 100.0 * Ez(z) / (1 + z)
kh2kv = lambda kh, z: kh * (1 + z) / (100.0 * Ez(z))
KH = {z: kv2kh(KV, z) for z in ZP + ZR}
k5u = abs(kv2kh(0.01, 5.0) - 100 * Ez(5.0) / 6 * 0.01) <= 1e-12 and float(np.max(np.abs(kh2kv(KH[5.0], 5.0) - KV))) <= 1e-12
check("K5", k5u, f"k(0.01 s/km, z 5) = {kv2kh(0.01, 5.0):.6f} h/Mpc; round trip exact", "<= 1e-12")

# ============================================================== M6 per footing
GATE_KB = KB
RJS = [0.05, 0.1, 0.2]
FT = {}
for f in FOOTS:
    ia = iso_amp(f)
    A = ia["A"]
    # smoothed / point variance (for the N2 envelope)
    s2iso_sm = trapz(KG ** 3 * (A * W2G) / (2 * math.pi ** 2) * W2G, LNK)
    point = ia["f_V"] * ia["delta_b_in"] ** 2
    target = 0.2 * s2R0 * D3 ** 2
    scaleN2 = target / s2iso_sm if s2iso_sm > 0 else float("nan")
    fd = {"iso": {k: (float(v) if not isinstance(v, str) else v) for k, v in ia.items()}, "point_variance": point,
          "smoothed_variance_RL": s2iso_sm, "smoothed_over_point": s2iso_sm / point, "N2_amp_scale": scaleN2,
          "N2_target_0.2_sigma2_ad_RL_z3": target, "fV_bound": M6J[f]["fV_max"]}
    # record gates: 3D gas ratio at L346 bins and k5 (filter cancels)
    tb, tk = {}, {}
    for z in ZR:
        pa = P_ad0(GATE_KB) * Dz(z) ** 2
        gz = (Dz(z) / D3) ** 2 if MUT else 1.0
        tb[str(z)] = (1 + A * W(GATE_KB * RL) ** 2 * gz / pa).tolist()
        tk[str(z)] = float(1 + A * W(K5 * RL) ** 2 * gz / (P_ad0(K5) * Dz(z) ** 2))
    allb = [v for z in tb for v in tb[z]]
    if min(tk.values()) < 0.9 or min(allb) < 0.5 or max(allb) > 2.0:
        gate = "FAIL"
    elif all(0.8 <= v <= 1.2 for v in allb) and min(tk.values()) >= T2_53:
        gate = "PASS"
    else:
        gate = "UNDECIDED"
    why = []
    if max(allb) > 2.0: why.append("L346 bin > 2.0 (excess edge)")
    if max(allb) > 1.2: why.append("L346 bin > 1.2 (PASS-band top)")
    if min(allb) < 0.8: why.append("L346 bin < 0.8")
    if min(tk.values()) < T2_53: why.append("T2(k5) < L319 strict line")
    # same for the N2 envelope (reported)
    allbN2 = [1 + (v - 1) * scaleN2 for v in allb]
    gateN2 = "FAIL" if max(allbN2) > 2.0 else ("PASS" if max(allbN2) <= 1.2 else "UNDECIDED")
    fd["gate"] = {"bins_T2_proxy": tb, "k5_T2_proxy": tk, "class": gate, "why": why, "max_bin": max(allb),
                  "N2_max_bin": max(allbN2), "N2_class": gateN2}
    # predictions on the z 4.2-5.4 grid, three R_J
    fd["pred"] = {}
    for RJ in RJS:
        R = ratio_grid(A, ZP + ZR, KH, RJ, iso_growth=MUT)
        RN2 = ratio_grid(A * scaleN2, ZP, KH, RJ, iso_growth=MUT)
        fd["pred"][str(RJ)] = {"S": {str(z): (R[z] - 1).tolist() for z in ZP + ZR}, "S_N2": {str(z): (RN2[z] - 1).tolist() for z in ZP}}
    # L347 P1D gate (reported): k_par 0.2-2 h/Mpc at z 3, 2, R_J 0.1
    kp347 = np.logspace(math.log10(0.2), math.log10(2.0), 15)
    R347 = ratio_grid(A, ZR, {z: kp347 for z in ZR}, 0.1, iso_growth=MUT)
    fd["L347_reported"] = {"max_abs_dev": float(max(np.max(np.abs(R347[z] - 1)) for z in ZR)), "line": 0.10}
    FT[f] = fd

# K2: M5 null
R0 = ratio_grid(0.0, ZP, KH, 0.1)
k2dev = float(max(np.max(np.abs(R0[z] - 1)) for z in ZP))
check("K2", k2dev <= 1e-12, f"M6 amplitude 0 (M5 null): max |R - 1| = {k2dev:.1e}", "<= 1e-12")
# K3: sign and positivity
k3 = []
for f in FOOTS:
    ia = FT[f]["iso"]
    Smin = min(min(FT[f]["pred"]["0.1"]["S"][str(z)]) for z in ZP)
    k3.append(ia["delta_c_in"] < 0 and 1 + ia["delta_b_in"] > 0 and 0 < ia["f_V"] <= FT[f]["fV_bound"] and Smin > 0)
check("K3", all(k3), "; ".join(f"{f}: delta_c,in {FT[f]['iso']['delta_c_in']:+.3f}, 1+delta_b,in {1 + FT[f]['iso']['delta_b_in']:+.3f}, "
                               f"f_V {FT[f]['iso']['f_V']:.5f} (<= {FT[f]['fV_bound']:.3f}), min S {min(min(FT[f]['pred']['0.1']['S'][str(z)]) for z in ZP):+.3e}" for f in FOOTS),
      "delta_c,in < 0; 1 + delta_b,in > 0; 0 < f_V <= bound; S > 0")
# K4: frozen-mode scaling
want = (Dz(4.2) / Dz(5.4)) ** 2
k4dev = 0.0
for f in FOOTS:
    for RJ in RJS:
        s54 = np.array(FT[f]["pred"][str(RJ)]["S"]["5.4"]); s42 = np.array(FT[f]["pred"][str(RJ)]["S"]["4.2"])
        k4dev = max(k4dev, float(np.max(np.abs((s54 / s42) / want - 1))))
RES["K4_as_frozen_reported"] = {"max_rel_dev_fixed_s_per_km": k4dev, "note": "mis-specified (AMENDMENTS.md A1): fixed s/km maps to different comoving k at z 4.2 and 5.4"}
P(f"  [reported] K4_as_frozen (fixed s/km): max rel dev {k4dev:.2e} (A1: not graded; different comoving k at each z)")
KCOM = np.logspace(math.log10(0.5), math.log10(15.0), 20)            # A1: fixed comoving grid, h/Mpc
k4a = 0.0
for f in FOOTS:
    Rc = ratio_grid(FT[f]["iso"]["A"], [4.2, 5.4], {4.2: KCOM, 5.4: KCOM}, 0.1, iso_growth=MUT)
    k4a = max(k4a, float(np.max(np.abs(((Rc[5.4] - 1) / (Rc[4.2] - 1)) / want - 1))))
RES["K4_amended_A1"] = {"max_rel_dev_fixed_comoving_k": k4a, "k_hMpc": KCOM.tolist()}
check("K4", k4a <= 1e-6, f"(A1) fixed comoving k 0.5-15 h/Mpc: S(5.4)/S(4.2) vs [D(4.2)/D(5.4)]^2 = {want:.6f}: max rel dev {k4a:.2e}", "<= 1e-6")

# ============================================================== print + testability
SIG = {"MED (eBOSS/DESI)": 0.03, "HIGH (XQ-100, HIRES/MIKE/UVES)": 0.10}


def dataset_mask(name, z, kv):
    if name.startswith("MED"):
        return (z <= 4.6) & (kv <= 0.04)
    return np.ones_like(kv, bool)


P("\n== M6 prediction: S = P1D_gas(ad + M6)/P1D_gas(ad) - 1 (linear proxy; F_b = X57 F_b,max(z 3))")
for f in FOOTS:
    fd = FT[f]
    ia = fd["iso"]
    P(f"\n  [{f}] delta_c,in {ia['delta_c_in']:+.4f}, delta_b,in {ia['delta_b_in']:+.4f}, F_b {ia['F_b']:.5f}, f_V {ia['f_V']:.5f} (positivity <= {fd['fV_bound']:.4f}); "
      f"A = f_V delta^2 V_p = {ia['A']:.5f} (Mpc/h)^3; point variance f_V delta^2 {fd['point_variance']:.5f}; smoothed at R_L {fd['smoothed_variance_RL']:.5f} "
      f"(ratio {fd['smoothed_over_point']:.4f}); N2 envelope = x{fd['N2_amp_scale']:.3f}")
    g = fd["gate"]
    P(f"    record gate (X22 forest_class on 1 + P_iso/P_ad, L346 bins z 3/2 + k5): bins z3 {min(g['bins_T2_proxy']['3.0']):.4f}-{max(g['bins_T2_proxy']['3.0']):.4f}, "
      f"z2 {min(g['bins_T2_proxy']['2.0']):.4f}-{max(g['bins_T2_proxy']['2.0']):.4f}; T2(k5) z3 {g['k5_T2_proxy']['3.0']:.4f} z2 {g['k5_T2_proxy']['2.0']:.4f} -> {g['class']} "
      f"{g['why']}; N2 envelope max bin {g['N2_max_bin']:.4f} -> {g['N2_class']}")
    P(f"    L347 P1D line (reported): max |R - 1| over k_par 0.2-2 h/Mpc, z 3/2 = {fd['L347_reported']['max_abs_dev']:.4f} vs 0.10")
    for RJ in RJS:
        pr = fd["pred"][str(RJ)]
        P(f"    R_J {RJ} Mpc/h:")
        for z in ZP + ZR:
            Sv = np.array(pr["S"][str(z)])
            idx = [0, 5, 9, 14, 19]
            P(f"      z {z}: S at k = " + ", ".join(f"{KV[i]:.4f}:{Sv[i]:+.4f}" for i in idx) + f" s/km; max {Sv.max():+.4f} at {KV[int(np.argmax(Sv))]:.4f} s/km"
              + (f"; N2 max {max(pr['S_N2'][str(z)]):+.4f}" if z in ZP else ""))
    # testability at primary R_J
    fd["testability"] = {}
    for RJ in RJS:
        pr = fd["pred"][str(RJ)]
        tt = {}
        for ds, sg in SIG.items():
            Ss = np.concatenate([np.array(pr["S"][str(z)])[dataset_mask(ds, z, KV)] for z in ZP])
            if Ss.size == 0:
                continue
            tt[ds] = {"sigma_PROV": sg, "n_bins": int(Ss.size), "max_S": float(Ss.max()), "max_S_over_sigma": float(Ss.max() / sg),
                      "combined_SN": float(math.sqrt(np.sum((Ss / sg) ** 2))), "sigma_needed_3sigma_combined": float(math.sqrt(np.sum(Ss ** 2)) / 3)}
        fd["testability"][str(RJ)] = tt
        P(f"    testability R_J {RJ}: " + "; ".join(f"{ds}: {v['n_bins']} bins, max S {v['max_S']:.4f} = {v['max_S_over_sigma']:.2f} sigma_PROV ({v['sigma_PROV']}), "
                                                   f"combined S/N {v['combined_SN']:.2f}, per-bin precision for combined 3 sigma {v['sigma_needed_3sigma_combined']:.4f}" for ds, v in tt.items()))

# ============================================================== verdict
P("\n== VERDICT (frozen section 5)")
VER = {}
for f in FOOTS:
    fd = FT[f]
    gate = fd["gate"]["class"]
    X = max(max(fd["pred"]["0.1"]["S"][str(z)]) for z in ZP)
    perz = {str(z): max(fd["pred"]["0.1"]["S"][str(z)]) for z in ZP}
    qual = lambda RJ: "ABOVE" if any(v["max_S_over_sigma"] >= 1 for v in fd["testability"][str(RJ)].values()) else "BELOW"
    quals = {str(RJ): qual(RJ) for RJ in RJS}
    # gate does not depend on R_J (filter cancels in 3D ratio)
    if len(set(quals.values())) > 1:
        v = "UNDECIDED (testability qualifier flips across R_J variants)"
    elif gate == "FAIL":
        v = f"M6 EXCLUDED BY RECORD FOREST LINES ({fd['gate']['why']})"
    else:
        v = f"M6 PREDICTION COMPUTED; TESTABLE AT LEVEL X = {X:.4f} ({quals['0.1']} TYPICAL PER-BIN PRECISION, PROVISIONAL)"
    VER[f] = {"verdict": v, "X": X, "max_S_by_z": perz, "qualifier_by_RJ": quals, "record_gate": gate}
    P(f"  [{f}] {v}; per-z max S (R_J 0.1): " + ", ".join(f"z {z}: {s:+.4f}" for z, s in perz.items()) + f"; qualifier by R_J {quals}; record gate {gate}")
same = VER["canonical"]["verdict"].split(" (")[0].split(" = ")[0] == VER["alt"]["verdict"].split(" (")[0].split(" = ")[0]
footdiff = max(abs(a - b) for z in ZP for a, b in zip(FT["canonical"]["pred"]["0.1"]["S"][str(z)], FT["alt"]["pred"]["0.1"]["S"][str(z)]))
P(f"  footings agree on the class: {same}; max |S_canonical - S_alt| = {footdiff:.2e} (f_V delta^2 is fixed by X57's bound: 0.2 sigma^2_ad(R_L, z 3) on both footings)")
RES.update({"footings": FT, "verdicts": VER, "footings_agree": same, "max_footing_diff_S": footdiff, "KV_s_per_km": KV.tolist(),
            "KH_h_per_Mpc": {str(z): KH[z].tolist() for z in ZP + ZR}, "D_over_D0": {str(z): Dz(z) for z in ZP + ZR},
            "sigma2_ad_check_grid": float(s2ad_chk)})

# ============================================================== K6 + exit
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
check("K6", rss < 1.0, f"peak RSS {rss:.3f} GB, OMP_NUM_THREADS={os.environ.get('OMP_NUM_THREADS')}", "< 1 GB, one thread")
RES["elapsed_s"] = time.time() - T0; RES["peak_rss_GB"] = rss
allpass = all(c["pass"] for c in RES["checks"].values())
if MUT:
    req_fail = {"K0", "K3", "K4"}; req_pass = {"K1", "K2", "K5", "K6"}
    twin_ok = all(not RES["checks"][k]["pass"] for k in req_fail) and all(RES["checks"][k]["pass"] for k in req_pass)
    RES["twin_ok"] = twin_ok
    P(f"\nMUTATE: failing checks {[k for k, c in RES['checks'].items() if not c['pass']]}; required K0, K3, K4 FAIL and K1, K2, K5, K6 PASS -> twin {'OK' if twin_ok else 'BROKEN'}")
P(f"\nchecks {'ALL PASS' if allpass else 'NOT ALL PASS'}; elapsed {RES['elapsed_s']:.1f} s")
json.dump(RES, open(os.path.join(HERE, f"x63_m6_forest_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(0 if allpass else 1)
