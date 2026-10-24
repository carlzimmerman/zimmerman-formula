#!/usr/bin/env python3
"""X22_cosmic_dust_window (FROZEN_CRITERIA.md, a2b532e3c6): is there a window in scale, time or environment where a cold
component clusters enough for the Lyman-alpha forest and sigma8, yet is absent from isolated galaxies today?

  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x22_cosmic_dust_window.py              -> x22_cosmic_dust_window.out, _results.json
  PYTHONHASHSEED=0 X22_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 x22_cosmic_dust_window.py -> *_MUTATE.* (exit 1 by design)

kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 m/s^2 never pooled; a0 absent at linear order on FRW (forest/sigma8
side footing-independent). The cold component is gravitating field mass, never a particle. No knob fitted: alpha, p and
key thresholds are graded on frozen grids or bounded by lines, never adopted. Not "theory closed".
Copied with provenance: X6's SPARC d2 machinery and CFG946 constants (x6_dust_coupling.py L337-409), X4's L346/L319 gate
code (x4_dbi_door.py L473-519), the record's BBKS+Sugiyama shape and grms construction (prep_2026/mi_linear_cosmology/mi_growth.py).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import csv
import hashlib
import json
import math
import resource
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp, quad

T0 = time.time()
MUT = os.environ.get("X22_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTF = open(os.path.join(HERE, f"x22_cosmic_dust_window{TAG}.out"), "w")
RES = {"lane": "X22_cosmic_dust_window", "criteria": "a2b532e3c6", "date": "2026-10-24", "mutate": MUT, "checks": {},
       "settings": "kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; cold component = field mass; not theory closed"}
READS = {}
np.seterr(all="ignore")


def P(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    OUTF.write(s + "\n")
    OUTF.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": str(value), "threshold": str(thr)}
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {value}   (line: {thr})")


def rd(rel):
    p = os.path.join(REPO, rel)
    READS[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return json.load(open(p)) if rel.endswith(".json") else open(p).read()


def rss_gb():
    pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return pk / 1e9 if sys.platform == "darwin" else pk / 1e6


A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
P("X22_cosmic_dust_window" + (" [MUTATE m1-m7: control output, not physics]" if MUT else "") +
  ": criteria a2b532e3c6; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")

# ============================================================== constants (CFG946 via X6, verbatim)
G_SI, KPC946, MSUN946, PC946 = 6.67430e-11, 3.0856775814913673e19, 1.98847e30, 3.0856775814913673e16
MPC_M = 1e6 * PC946
H0_946 = 67.4e3 / MPC_M
RHOC_946 = 3 * H0_946 ** 2 / (8 * math.pi * G_SI)
OB946 = 0.0493
OC946 = 5.364 * OB946
OM946 = OB946 + OC946
RHOM946 = OM946 * RHOC_946
DTA = 5.55
HH = 0.674
FC, FB = 5.364 / 6.364, 1.0 / 6.364
RHOM_H = RHOM946 * MPC_M ** 3 / MSUN946 / HH ** 2           # rho_m in h^2 Msun / Mpc^3 (comoving)


def r_ta(Mb_kg):
    return (3 * (OM946 / OB946) * Mb_kg / (4 * math.pi * DTA * RHOM946)) ** (1.0 / 3.0)


def law_g(gN, a0):
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def nu1(yv):
    yv = np.maximum(np.asarray(yv, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / yv)


# ============================================================== S0-1: L346 gate (X4 code)
P("\n== S0-1: L346 bins and bands from its JSON (X4 code) vs X4 F0a")
L346 = rd("real_research/g03_audit_2026/L346_switch_forest_gate_results.json")
X4J = rd("rebuild_2026_10_22/X4_growth_native_cap/x4_dbi_door_results.json")
runs346 = L346["numbers"]["runs"]


def r346(name, z):
    a = np.array(runs346[name]["pk"][z])
    b = np.array(runs346["lcdm"]["pk"][z])
    kk = b[:, 0]
    fo = (kk >= 1.0) & (kk <= 4.0)
    return kk[fo], (a[:, 1] / b[:, 1])[fo]


KB346 = r346("sw5_canon", "3.0")[0]
bands = {}
for n in ("sw5_canon", "sw5_alt", "never_on"):
    for z in ("3.0", "2.0"):
        _, rr = r346(n, z)
        bands[f"{n}_{z}"] = (float(rr.min()), float(rr.max()))
cmp_name = {"sw5_canon": "sw5_alt" if MUT else "sw5_canon", "sw5_alt": "sw5_alt", "never_on": "never_on"}   # m1
dev01 = max(abs(bands[f"{cmp_name[n]}_{z}"][i] - X4J["F0a"]["bands"][f"{n}_{z}"][i])
            for n in ("sw5_canon", "sw5_alt", "never_on") for z in ("3.0", "2.0") for i in (0, 1))
devb = float(np.max(np.abs(KB346 - np.array(X4J["F0a"]["bins_hMpc"]))))
RES["S0_1"] = {"bins_hMpc": KB346.tolist(), "bands": bands, "max_dev_bands": dev01, "max_dev_bins": devb}
check("S0-1", dev01 <= 1e-9 and devb <= 1e-9, f"bins {np.round(KB346, 3).tolist()}; max |band - X4| {dev01:.2e}; bins {devb:.2e}", "<= 1e-9")

# ============================================================== S0-2: L319 line and the cut family
P("\n== S0-2: L319's WDM line (the cut family)")
rd("real_research/dark_sector_2026/L319_lambda_triggered_kicked_decay.py")
h19 = 0.6736
Om19 = (0.02237 + 0.1200) / h19 ** 2
K_H19 = np.geomspace(0.02, 30.0, 44)
K5 = float(K_H19[int(np.argmin(np.abs(K_H19 - 5.0)))])
NU = 1.12
EXPO = (-5.0 / NU) if MUT else (-10.0 / NU)                       # m2


def alpha_wdm(m_keV):                                               # L319 L169-171
    return 0.049 * m_keV ** -1.11 * (Om19 / 0.25) ** 0.11 * (h19 / 0.7) ** 1.22


def T2cut(k_h, alpha):
    return (1 + (alpha * np.asarray(k_h, float)) ** (2 * NU)) ** EXPO


def alpha_at(T2line, k_h):                                          # closed form: T2(k) = T2line
    return (T2line ** (1.0 / EXPO) - 1.0) ** (1.0 / (2 * NU)) / k_h


T2_53 = float(T2cut(K5, alpha_wdm(5.3)))
RES["S0_2"] = {"k5_hMpc": K5, "T2_5.3keV": T2_53, "X4": X4J["F0b"]["T2_5.3keV"]}
check("S0-2", abs(T2_53 - X4J["F0b"]["T2_5.3keV"]) <= 1e-12 and abs(T2_53 - 0.995) <= 5e-4,
      f"T2_5.3keV(k5 = {K5:.4f}) = {T2_53:.10f} (X4 {X4J['F0b']['T2_5.3keV']:.10f})", "<= 1e-12 and within 5e-4 of 0.995")


def forest_class(t2bins_by_z, t2k5_by_z):
    allbins = [v for z in t2bins_by_z for v in t2bins_by_z[z]]
    k5s = list(t2k5_by_z.values())
    if min(k5s) < 0.9 or min(allbins) < 0.5 or max(allbins) > 2.0:
        return "FAIL"
    if all(0.8 <= v <= 1.2 for v in allbins) and min(k5s) >= T2_53:
        return "PASS"
    return "UNDECIDED"


def cut_class(alpha):
    tb = {z: T2cut(KB346, alpha).tolist() for z in ("3", "2")}
    tk = {z: float(T2cut(K5, alpha)) for z in ("3", "2")}
    return forest_class(tb, tk)


# ============================================================== S0-3 / S0-4: X6's SPARC machinery (verbatim copy)
P("\n== S0-3 / S0-4: X6's SPARC d2 machinery")
X6J = rd("rebuild_2026_10_22/X6_dust_coupling/x6_dust_coupling_results.json")
KPC_S = 3.0857e19
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2) * (1.1 if MUT else 1.0)     # m3
SD = os.path.join(REPO, "real_research", "data", "sparc_data")
GALS = []
for fn in sorted(os.listdir(SD)):
    if not fn.endswith("_rotmod.dat"):
        continue
    try:
        dd = np.genfromtxt(os.path.join(SD, fn), comments="#")
    except Exception:
        continue
    if dd.ndim != 2 or dd.shape[1] < 6:
        continue
    q = dict(name=fn.replace("_rotmod.dat", ""), R=dd[:, 0], Vobs=dd[:, 1], eV=dd[:, 2], Vgas=dd[:, 3], Vdisk=dd[:, 4], Vbul=dd[:, 5])
    Rm = q["R"] * KPC_S
    VB2 = np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None] ** 2 + UPS[None, :] * q["Vdisk"][:, None] ** 2 + 1.4 * UPS[None, :] * q["Vbul"][:, None] ** 2
    GB = VB2 * 1e6 / Rm[:, None]
    GO = ((q["Vobs"] * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
    OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (q["Vobs"] > 0)[:, None]
    Wt = 1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None)) ** 2
    Mb = np.maximum(VB2[-1, :], 0.0) * 1e6 * Rm[-1] / G_SI
    rta = np.array([r_ta(m) if m > 0 else 1.0 for m in Mb])
    q.update(Rm=Rm, GB=GB, GO=GO, OK=OK, Wt=Wt, Mb=Mb, rta=rta)
    GALS.append(q)
READS["real_research/data/sparc_data/*_rotmod.dat"] = f"{len(GALS)} files read"


def sparc_stats_g(a0, gd_fn):
    """X6's sparc_stats with the cold acceleration supplied per galaxy: gd_fn(i, q) -> array (nR, nU)."""
    wr2 = wsum = 0.0
    U, IDX = [], []
    for i, q in enumerate(GALS):
        GBt = q["GB"] + gd_fn(i, q)
        lgp = np.log10(np.where(q["GB"] > 0, nu1(np.maximum(GBt, 1e-300) / a0) * np.maximum(GBt, 1e-300), 1e-300))
        r = np.where(q["OK"], np.log10(np.where(q["OK"], q["GO"], 1.0)) - lgp, 0.0)
        Wm = np.where(q["OK"], q["Wt"][:, None], 0.0)
        mse = (Wm * r * r).sum(0) / np.maximum(Wm.sum(0), 1e-300)
        j = int(np.argmin(mse))
        wr2 += float((Wm[:, j] * r[:, j] ** 2).sum())
        wsum += float(Wm[:, j].sum())
        U.append(UPS[j])
        IDX.append(j)
    return dict(rms=math.sqrt(wr2 / wsum), U_median=float(np.median(U)), N=len(GALS), idx=IDX)


def gd_DF(fd_vec):                                                  # X6's D-F profile, per-galaxy fraction
    def f(i, q):
        return G_SI * fd_vec[i] * 5.364 * q["Mb"][None, :] * np.minimum(q["Rm"][:, None] / q["rta"][None, :], 1.0) / q["Rm"][:, None] ** 2
    return f


def sparc_stats(a0, fd):                                            # X6's scalar form (verbatim body)
    wr2 = wsum = 0.0
    U = []
    for q in GALS:
        gd = G_SI * fd * 5.364 * q["Mb"][None, :] * np.minimum(q["Rm"][:, None] / q["rta"][None, :], 1.0) / q["Rm"][:, None] ** 2
        GBt = q["GB"] + gd
        lgp = np.log10(np.where(q["GB"] > 0, nu1(np.maximum(GBt, 1e-300) / a0) * np.maximum(GBt, 1e-300), 1e-300))
        r = np.where(q["OK"], np.log10(np.where(q["OK"], q["GO"], 1.0)) - lgp, 0.0)
        Wm = np.where(q["OK"], q["Wt"][:, None], 0.0)
        mse = (Wm * r * r).sum(0) / np.maximum(Wm.sum(0), 1e-300)
        i = int(np.argmin(mse))
        wr2 += float((Wm[:, i] * r[:, i] ** 2).sum())
        wsum += float(Wm[:, i].sum())
        U.append(UPS[i])
    return dict(rms=math.sqrt(wr2 / wsum), U_median=float(np.median(U)), N=len(GALS))


NG = len(GALS)
LAW = {f: sparc_stats_g(A0[f], lambda i, q: 0.0) for f in FOOTS}
U_EDGE = {f: min(0.50, LAW[f]["U_median"]) for f in FOOTS}


def line_ok(f, s_, rms_only=False):
    if rms_only:
        return s_["rms"] <= 0.110
    return s_["rms"] <= 0.110 and U_EDGE[f] <= s_["U_median"] <= 0.80


d03 = [abs(LAW[f]["rms"] - X6J["d"]["law_sparc"][f]["rms"]) for f in FOOTS]
u03 = [LAW[f]["U_median"] == X6J["d"]["law_sparc"][f]["U_median"] for f in FOOTS]
RES["S0_3"] = {f: {"rms": LAW[f]["rms"], "U_median": LAW[f]["U_median"], "N": NG} for f in FOOTS}
check("S0-3", max(d03) <= 1e-9 and all(u03), "; ".join(f"{f}: rms {LAW[f]['rms']:.6f} U {LAW[f]['U_median']:.2f} "
      f"(X6 {X6J['d']['law_sparc'][f]['rms']:.6f} {X6J['d']['law_sparc'][f]['U_median']:.2f})" for f in FOOTS) + f"; N {NG}",
      "rms <= 1e-9, same U median")


def bisect_f(pred):
    if pred(1.0):
        return 1.0
    if not pred(0.0):
        return float("nan")
    lo, hi = 0.0, 1.0
    for _ in range(20):
        md = 0.5 * (lo + hi)
        (lo, hi) = (md, hi) if pred(md) else (lo, md)
    return lo


fmax_both = bisect_f(lambda fd: all(line_ok(f, sparc_stats(A0[f], fd), rms_only=MUT) for f in FOOTS))   # m4
fc6 = X6J["growth"]["f_c"]["cap_10"]["ai1e3"]
_d = np.genfromtxt(os.path.join(SD, "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC946
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3) + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MB_N = GN_N[-1] * R_N[-1] ** 2 / G_SI
RTA_N = r_ta(MB_N)
ngc = {}
for f in FOOTS:
    gd = G_SI * fc6 * 5.364 * MB_N * np.minimum(R_N / RTA_N, 1.0) / R_N ** 2
    ngc[f] = float(np.max(np.abs(np.log10(law_g(GN_N + gd, A0[f]) / law_g(GN_N, A0[f])))))
d04 = max([abs(fmax_both - X6J["d"]["f_d_max_d2"])] + [abs(ngc[f] - X6J["d"]["per_footing"][f]["f_c"]["ngc3198_dex"]) for f in FOOTS])
RES["S0_4"] = {"f_d_max_d2_both": fmax_both, "X6": X6J["d"]["f_d_max_d2"], "ngc3198_dex_at_fc": ngc, "f_c": fc6}
check("S0-4", d04 <= 1e-9, f"f_d,max(both) {fmax_both:.10f} (X6 {X6J['d']['f_d_max_d2']:.10f}); NGC 3198 at f_c {fc6:.4f}: "
      + "; ".join(f"{f} {ngc[f]:.6f} dex" for f in FOOTS), "<= 1e-9")

# ============================================================== S0-5: X19 table
P("\n== S0-5: X19 class table")
rd("rebuild_2026_10_22/X19_selector_rank_test/x19_classes.csv")
X19 = {}
with open(os.path.join(REPO, "rebuild_2026_10_22/X19_selector_rank_test/x19_classes.csv")) as fh:
    for row in csv.DictReader(fh):
        X19[(row["footing"], row["class"])] = row
h19x = 0.70 if MUT else 0.672                                        # m5
G19, MSUN19, KPC19 = 6.674e-11, 1.989e30, 3.0857e19                   # X19's own unit constants (x19_selector_rank_test.py L25; A1)
rhoc_pc = 3 * (h19x * 100e3 / (KPC19 * 1e3)) ** 2 / (8 * math.pi * G19) * (KPC19 / 1e3) ** 3 / MSUN19
rb0, rb1100 = 0.049 * rhoc_pc, 0.049 * rhoc_pc * 1101 ** 3
ok5 = []
for f in FOOTS:
    bg = X19[(f, "Cosmic background")]
    ok5.append(abs(float(bg["rho_b_p16"]) / rb0 - 1) <= 1e-6 and abs(float(bg["rho_b_p84"]) / rb1100 - 1) <= 1e-6
               and (f, "SPARC small") in X19 and (f, "SPARC large") in X19)
RHOB0 = float(X19[("canonical", "Cosmic background")]["rho_b_p16"])
RES["S0_5"] = {"rho_b_z0": rb0, "rho_b_z1100": rb1100, "X19_band": [RHOB0, float(X19[("canonical", "Cosmic background")]["rho_b_p84"])]}
check("S0-5", all(ok5), f"Omega_b rho_crit(1+z)^3: z=0 {rb0:.6e}, z=1100 {rb1100:.6e} Msun/pc^3 vs X19 band "
      f"{RHOB0:.6e} - {float(X19[('canonical', 'Cosmic background')]['rho_b_p84']):.6e}; SPARC rows present", "<= 1e-6 relative")

STOP = not all(RES["checks"][c]["pass"] for c in ("S0-1", "S0-2", "S0-3", "S0-4", "S0-5"))
if STOP and not MUT:
    P("\nSTOP RULE: a Step-0 reproduction failed; verdict UNDECIDED; no Step 1-3 numbers graded.")
    RES["verdict"] = "UNDECIDED (stop rule)"
    json.dump(RES, open(os.path.join(HERE, f"x22_cosmic_dust_window_results{TAG}.json"), "w"), indent=1)
    sys.exit(1)

# ============================================================== STEP 1: lambda_forest
P("\n== STEP 1: lambda_forest from the L319 cut family T2 = [1+(alpha k)^(2 nu)]^(-10/nu), nu = 1.12 (n = 2.24, m = 5/nu)")
a_strict = alpha_at(T2_53, K5)
a_bandtop = alpha_at(0.8, KB346.max())
a_loose = alpha_at(0.9, K5)
a_bin05 = alpha_at(0.5, KB346.max())          # for T2 <= 1 decreasing in k, the worst bin is the highest k
A_PASS = min(a_strict, a_bandtop)
A_NF = min(a_loose, a_bin05)
c1 = (cut_class(1e-6) == "PASS" and cut_class(alpha_wdm(1.0)) == "FAIL" and abs(float(T2cut(K5, alpha_wdm(5.3))) - T2_53) <= 1e-15
      and cut_class(A_PASS * (1 - 1e-9)) == "PASS" and cut_class(A_PASS * (1 + 1e-6)) != "PASS"
      and cut_class(A_NF * (1 - 1e-9)) != "FAIL" and cut_class(A_NF * (1 + 1e-6)) == "FAIL")
check("C1", c1, f"alpha->0 {cut_class(1e-6)}; 1 keV {cut_class(alpha_wdm(1.0))}; class flips at alpha_PASS {A_PASS:.5f} and alpha_NF {A_NF:.5f} Mpc/h",
      "PASS / FAIL / edges consistent")
x_hm = (0.25 ** (1.0 / EXPO) - 1.0) ** (1.0 / (2 * NU))          # alpha k_hm


def mass_of_k(k_h):                                                 # Lagrangian mass for R = pi/k (Msun/h), radius Mpc/h
    R = math.pi / k_h
    return 4 * math.pi / 3 * RHOM_H * R ** 3, R


S1 = {}
for lab, al in (("alpha_PASS", A_PASS), ("alpha_NF", A_NF), ("WDM_5.3keV", alpha_wdm(5.3))):
    khm = x_hm / al
    M, R = mass_of_k(khm)
    S1[lab] = {"alpha_Mpc_h": al, "k_c_hMpc": 1 / al, "k_hm_hMpc": khm, "lambda_hm_Mpc_h": 2 * math.pi / khm, "R_hm_Mpc_h": R,
               "M_hm_Msun_h": M, "M_hm_Msun": M / HH, "T2_k10": float(T2cut(10.0, al)), "class": cut_class(al * (1 - 1e-9))}   # class just inside the edge (A2)
    P(f"  {lab}: alpha = k_c^-1 = {al:.5f} Mpc/h; k_hm {khm:.3f} h/Mpc; lambda_hm {2 * math.pi / khm:.3f} Mpc/h; "
      f"R_hm(Lagr.) {R * 1e3:.1f} kpc/h; M_hm {M:.3e} Msun/h ({M / HH:.3e} Msun); T2(k=10) {S1[lab]['T2_k10']:.3f}; class {S1[lab]['class']}")
S1["alpha_lines"] = {"strict_k5": a_strict, "band_top_0.8": a_bandtop, "loose_k5_0.9": a_loose, "bin_0.5": a_bin05}
S1["lambda_line_Mpc_h"] = 2 * math.pi / K5
S1["pincer_loose_k10_0.5_alpha"] = alpha_at(0.5, 10.0)
P(f"  lines: strict alpha <= {a_strict:.5f}, band top <= {a_bandtop:.5f}, loose <= {a_loose:.5f}, bin 0.5 <= {a_bin05:.5f} Mpc/h; "
  f"lambda_line = 2pi/k5 = {2 * math.pi / K5:.3f} Mpc/h; pincer loose yardstick alone allows alpha <= {S1['pincer_loose_k10_0.5_alpha']:.5f}")
LAMBDA_FOREST = S1["alpha_NF"]["lambda_hm_Mpc_h"]
P(f"  => lambda_forest (half-mode at alpha_NF) = {LAMBDA_FOREST:.3f} Mpc/h comoving; Lagrangian M_hm = {S1['alpha_NF']['M_hm_Msun']:.3e} Msun")
RES["step1"] = S1

# ============================================================== STEP 2: galaxy side
P("\n== STEP 2: the galaxy side (per footing)")
RLAST = np.array([q["R"][-1] for q in GALS])
VLAST = np.array([q["Vobs"][-1] for q in GALS])
pct = lambda v: [float(np.min(v)), float(np.percentile(v, 16)), float(np.median(v)), float(np.percentile(v, 84)), float(np.max(v))]
S2 = {"R_last_kpc_min_p16_p50_p84_max": pct(RLAST), "V_last_kms": pct(VLAST)}
P(f"  R_gal: SPARC R_last min/16/50/84/max = " + " / ".join(f"{v:.2f}" for v in S2["R_last_kpc_min_p16_p50_p84_max"]) + " kpc")


def hydro_frac_enclosed(beta, x):                                    # M_c(<r)/(5.364 M_b) at x = r/r_ta, r <= r_ta
    ex = (2.0 - beta) if MUT else (3.0 - beta)                       # m7
    return (1.0 / DTA) * 3.0 / (3.0 - beta) * np.power(np.minimum(x, 1.0), ex)


# C4: closed form vs quadrature of 4 pi r^2 rho, rho = rho_cbar (r/r_ta)^-beta, in units of (5.364 M_b): rho_cbar 4pi r_ta^3/3 = 1/DTA
c4dev = 0.0
for beta in (0.3, 1.0, 2.2):
    for x in (0.05, 0.3, 1.0):
        num = quad(lambda s: 3.0 / DTA * s ** 2 * s ** (-beta), 0, x, limit=200)[0]
        c4dev = max(c4dev, abs(num / float(hydro_frac_enclosed(beta, x)) - 1))
check("C4", c4dev <= 1e-8, f"max |closed form / quadrature - 1| = {c4dev:.2e} (beta 0.3, 1, 2.2; x 0.05, 0.3, 1)", "<= 1e-8")

BCAP = 2.9


def gd_hydro(cs):
    def f(i, q):
        beta = min((VLAST[i] / cs) ** 2, BCAP)
        Mc = 5.364 * q["Mb"][None, :] * hydro_frac_enclosed(beta, q["Rm"][:, None] / q["rta"][None, :])
        return G_SI * Mc / q["Rm"][:, None] ** 2
    return f


FMAX, FMAX_RMS, CSNEED, MLAG, KLAG, S2F = {}, {}, {}, {}, {}, {}
for f in FOOTS:
    a0 = A0[f]
    FMAX[f] = bisect_f(lambda fd: line_ok(f, sparc_stats(a0, fd)))
    FMAX_RMS[f] = bisect_f(lambda fd: line_ok(f, sparc_stats(a0, fd), rms_only=True))
    idx = LAW[f]["idx"]
    Mb_law = np.array([GALS[i]["Mb"][idx[i]] for i in range(NG)])
    rta_law = np.array([GALS[i]["rta"][idx[i]] for i in range(NG)])
    xr = RLAST * KPC_S / rta_law
    tol = FMAX[f] * 5.364 * np.minimum(xr, 1.0)
    ML = (OM946 / OB946) * Mb_law / MSUN946                          # Msun
    RL = (3 * ML * HH / (4 * math.pi * RHOM_H)) ** (1.0 / 3.0)       # Mpc/h (M in Msun/h = ML*h)
    MLAG[f], KLAG[f] = ML, math.pi / RL
    # c_s,need: bisection in log c_s on [1, 3000] km/s, 30 steps
    lo, hi = math.log(1.0), math.log(3000.0)
    okhi = line_ok(f, sparc_stats_g(a0, gd_hydro(3000.0)))
    oklo = line_ok(f, sparc_stats_g(a0, gd_hydro(1.0)))
    if okhi and not oklo:
        for _ in range(30):
            md = 0.5 * (lo + hi)
            (lo, hi) = (lo, md) if line_ok(f, sparc_stats_g(a0, gd_hydro(math.exp(md)))) else (md, hi)
        CSNEED[f] = math.exp(hi)
    else:
        CSNEED[f] = float("nan")
    sneed = sparc_stats_g(a0, gd_hydro(CSNEED[f]))
    ncap = int(np.sum((VLAST / CSNEED[f]) ** 2 > BCAP))
    s_vir = float(np.median(np.array([float(hydro_frac_enclosed(2.0, x)) / min(x, 1.0) for x in xr])))
    S2F[f] = {"f_max": FMAX[f], "f_max_rms_only": FMAX_RMS[f], "law_rms": LAW[f]["rms"], "law_U": LAW[f]["U_median"], "U_edge": U_EDGE[f],
              "Mc_max_over_Mb_at_Rlast": pct(tol), "R_last_over_r_ta": pct(xr), "M_L_Msun": pct(ML), "R_L_Mpc_h": pct(RL),
              "k_L_hMpc": pct(math.pi / RL), "cs_need_kms": CSNEED[f], "sparc_at_cs_need": {"rms": sneed["rms"], "U": sneed["U_median"]},
              "n_beta_capped_at_cs_need": ncap, "content_beta2_over_fair_inside_Rlast_median": s_vir,
              "cs_need_over_Vlast": pct(CSNEED[f] / VLAST)}
    P(f"  {f}: f_max (d2 line, this footing) = {FMAX[f]:.5f}; rms-only bound {FMAX_RMS[f]:.5f}; law rms {LAW[f]['rms']:.4f}, U {LAW[f]['U_median']:.2f} (edge {U_EDGE[f]:.2f})")
    P(f"     tolerated M_c(<R_last)/M_b min/16/50/84/max = " + " / ".join(f"{v:.4f}" for v in pct(tol)) +
      f"; R_last/r_ta median {np.median(xr):.3f}")
    P(f"     Lagrangian M_L = (Om/Ob) M_b: " + " / ".join(f"{v:.3e}" for v in pct(ML)) + " Msun; R_L " +
      " / ".join(f"{v:.3f}" for v in pct(RL)) + " Mpc/h; k_L = pi/R_L " + " / ".join(f"{v:.2f}" for v in pct(math.pi / RL)) + " h/Mpc")
    P(f"     hydrostatic c_s,need = {CSNEED[f]:.1f} km/s (SPARC at it: rms {sneed['rms']:.4f}, U {sneed['U_median']:.2f}; beta capped in {ncap} galaxies); "
      f"c_s,need/V_last median {np.median(CSNEED[f] / VLAST):.2f}; gravitational virial heating (beta = 2) leaves median {s_vir:.3f} of the fair share inside R_last")
c5 = all(abs(sparc_stats_g(A0[f], gd_DF(np.full(NG, fv)))["rms"] - sparc_stats(A0[f], fv)["rms"]) == 0.0
         and sparc_stats_g(A0[f], gd_DF(np.full(NG, fv)))["U_median"] == sparc_stats(A0[f], fv)["U_median"] for f in FOOTS for fv in (FMAX[f], 1.0))
check("C5", c5, "vector form with fd_i = f equals X6 scalar form at f_max and 1, both footings", "exact")
S2["per_footing"] = S2F
RES["step2"] = S2

# ============================================================== STEP 3A: frozen comoving cut
P("\n== STEP 3A: frozen comoving cut (gravity only), captured fraction c_i = T2(k_L,i) (window-favourable)")
S3A = {}
for f in FOOTS:
    S3A[f] = {}
    for lab, al in (("alpha_NF", A_NF), ("alpha_PASS", A_PASS)):
        ci = T2cut(KLAG[f], al)
        st = sparc_stats_g(A0[f], gd_DF(ci))
        okl = line_ok(f, st)
        xex = (FMAX[f] ** (1.0 / EXPO) - 1.0) ** (1.0 / (2 * NU)) if FMAX[f] > 0 else float("inf")
        kex = xex / al
        Mex = mass_of_k(kex)[0] / HH                                  # Msun
        frac_below = float(np.mean(MLAG[f] < Mex))
        S3A[f][lab] = {"captured_T2_min_p16_p50_p84_max": pct(ci), "sparc_rms": st["rms"], "sparc_U": st["U_median"], "d2_line": okl,
                       "k_excl_hMpc": kex, "M_excl_Msun": Mex, "gap_ML_p16_over_Mexcl": float(np.percentile(MLAG[f], 16) / Mex),
                       "gap_ML_p50_over_Mexcl": float(np.median(MLAG[f]) / Mex), "gap_ML_min_over_Mexcl": float(np.min(MLAG[f]) / Mex),
                       "frac_SPARC_below_Mexcl": frac_below, "k_ratio_excl_over_k5": kex / K5}
        P(f"  {f} {lab}: captured T2(k_L) min/16/50/84/max " + " / ".join(f"{v:.4f}" for v in pct(ci)) +
          f" -> SPARC rms {st['rms']:.4f}, U {st['U_median']:.2f} -> d2 {'PASS' if okl else 'FAIL'}")
        P(f"     exclusion needs T2 <= f_max = {FMAX[f]:.4f}: k_excl = {kex:.1f} h/Mpc ({kex / K5:.1f} x k5), M_excl = {Mex:.3e} Msun; "
          f"SPARC M_L min/p16/p50 over M_excl = {np.min(MLAG[f]) / Mex:.3g} / {np.percentile(MLAG[f], 16) / Mex:.3g} / {np.median(MLAG[f]) / Mex:.3g}; "
          f"fraction of SPARC below M_excl {frac_below:.3f}")
        if frac_below > 0:
            Mb_eq = Mex * OB946 / OM946 * MSUN946
            rt = r_ta(Mb_eq)
            idx = LAW[f]["idx"]
            sel = np.where(MLAG[f] < Mex)[0]
            fr = [float((OC946 / OM946) * Mex * MSUN946 * min(RLAST[i] * KPC_S / rt, 1.0) /
                        (5.364 * GALS[i]["Mb"][idx[i]] * min(RLAST[i] * KPC_S / GALS[i]["rta"][idx[i]], 1.0))) for i in sel]
            S3A[f][lab]["infall_from_Mexcl_over_fair_reported"] = pct(np.array(fr))
            P(f"     infall (reported): suppressed galaxies sitting in an M_excl structure get " + " / ".join(f"{v:.3g}" for v in pct(np.array(fr))) + " x their fair share inside R_last")
for f in FOOTS:                                                     # reported only (A3): forest half-mode vs galaxy Lagrangian scales
    S3A[f]["scale_gap_reported_A3"] = {}
    for lab in ("alpha_NF", "alpha_PASS"):
        RL_ = math.pi / KLAG[f]
        g_ = {"R_L_over_R_hm_min_p16_p50_p84_max": pct(RL_ / S1[lab]["R_hm_Mpc_h"]),
              "M_L_over_M_hm_min_p16_p50_p84_max": pct(MLAG[f] / S1[lab]["M_hm_Msun"]),
              "frac_SPARC_M_L_below_M_hm": float(np.mean(MLAG[f] < S1[lab]["M_hm_Msun"]))}
        S3A[f]["scale_gap_reported_A3"][lab] = g_
        P(f"  {f} {lab} (reported, A3): R_L / R_hm min/16/50/84/max " + " / ".join(f"{v:.3g}" for v in g_["R_L_over_R_hm_min_p16_p50_p84_max"]) +
          "; M_L / M_hm " + " / ".join(f"{v:.3g}" for v in g_["M_L_over_M_hm_min_p16_p50_p84_max"]) + f"; fraction of SPARC with M_L < M_hm {g_['frac_SPARC_M_L_below_M_hm']:.3f}")
WINDOW_A = all(S3A[f]["alpha_NF"]["d2_line"] for f in FOOTS)
P(f"  Window-A (d2 passes on both footings at alpha_NF): {WINDOW_A}")
RES["step3A"] = S3A

# ============================================================== STEP 3B: time-dependent Jeans cut
P("\n== STEP 3B: Jeans cut lambda_J,com ~ a^p, c_s(a) = c_s,need a^(p-1/2); linear two-fluid ODE from a_i = 1e-3")
OL946 = 1.0 - OM946
SRC = 1.4 if MUT else 1.5                                            # m6


def Ea(a):
    return math.sqrt(OM946 * a ** -3 + OL946)


def grow(k_h, cs_fn, ai=1e-3, zout=(3.0, 2.0, 0.0), segments=None):
    def rhs(N, y):
        a = math.exp(N)
        E2 = OM946 * a ** -3 + OL946
        Oma = OM946 * a ** -3 / E2
        dlnH = -1.5 * Oma
        cs = cs_fn(a)
        J = (cs * k_h / (100.0 * a * math.sqrt(E2))) ** 2
        src = SRC * Oma * (FC * y[0] + FB * y[2])
        return [y[1], -(2 + dlnH) * y[1] + src - J * y[0], y[3], -(2 + dlnH) * y[3] + src]
    Ns = sorted([math.log(1 / (1 + z)) for z in zout])
    edges = [math.log(ai)] + (sorted(segments) if segments else []) + [0.0]
    y = [ai, ai, ai, ai]
    out = {}
    for s0, s1 in zip(edges[:-1], edges[1:]):
        te = [N for N in Ns if s0 < N <= s1]
        sol = solve_ivp(rhs, (s0, s1), y, method="LSODA", rtol=1e-8, atol=1e-14, t_eval=te if te else None)
        for j, N in enumerate(te):
            out[round(1 / math.exp(N) - 1, 6)] = FC * sol.y[0][j] + FB * sol.y[2][j]
        y = sol.y[:, -1].tolist()
    return out


# C2: c_s = 0 -> T2 == 1; growth vs LCDM integral normalised in the matter era at a_i
def D_lcdm(a):
    return 2.5 * OM946 * Ea(a) * quad(lambda x: 1.0 / (x * Ea(x)) ** 3, 0, a, epsabs=0, epsrel=1e-12, limit=400)[0]


g0 = grow(1.0, lambda a: 0.0)
g1 = grow(1.0, lambda a: 0.0)
Dn = D_lcdm(1.0) / D_lcdm(1e-3) * 1e-3
c2dev = abs(g0[0.0] / Dn - 1)
check("C2", c2dev <= 2e-3 and abs(g0[0.0] / g1[0.0] - 1) <= 1e-10, f"c_s = 0: delta_m(z=0) {g0[0.0]:.6f} vs LCDM integral {Dn:.6f} "
      f"(|dev| {c2dev:.2e}); T2 identically 1 ({abs(g0[0.0] / g1[0.0] - 1):.1e})", "<= 2e-3; 1e-10")

# k grids
KS8 = np.geomspace(1e-3, 30.0, 61)
KF = np.concatenate([KB346, [K5]])
REF = {}
for k in np.concatenate([KS8, KF]):
    REF[float(k)] = grow(float(k), lambda a: 0.0)

# record BBKS + Sugiyama shape (mi_growth.py constants verbatim)
h_m, Om_m, Ob_m, ns_m = 0.674, 0.315, 0.0493, 0.965
Gam = Om_m * h_m * np.exp(-Ob_m * (1.0 + np.sqrt(2 * h_m) / Om_m))
rd("prep_2026/mi_linear_cosmology/mi_growth.py")


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


def grade(cs_fn, segments=None):
    T2_8 = np.array([(grow(float(k), cs_fn, segments=segments, zout=(0.0,))[0.0] / REF[float(k)][0.0]) ** 2 for k in KS8])
    gF = {float(k): grow(float(k), cs_fn, segments=segments, zout=(3.0, 2.0)) for k in KF}
    tb, tk = {}, {}
    for z, zs in ((3.0, "3"), (2.0, "2")):
        tb[zs] = [(gF[float(k)][z] / REF[float(k)][z]) ** 2 for k in KB346]
        tk[zs] = (gF[K5][z] / REF[K5][z]) ** 2
    return {"R_sigma8": sigma8_ratio(T2_8), "forest": forest_class(tb, tk), "bins_z3": tb["3"], "bins_z2": tb["2"], "T2_k5": tk,
            "T2_z0_at_k_0.1_1_10": [float(np.interp(math.log(kk), np.log(KS8), T2_8)) for kk in (0.1, 1.0, 10.0)]}


# C3: monotone in c_s at p = 0.5 (constant c_s), z = 0, all graded k
c3 = True
for k in list(KS8[::6]) + list(KF):
    prev = 2.0
    for cs in (0.0, 10.0, 100.0, 300.0):
        t = (grow(float(k), lambda a, cs=cs: cs)[0.0] / REF[float(k)][0.0]) ** 2
        c3 = c3 and (t <= prev + 1e-9)
        prev = t
check("C3", c3, "T2(z = 0) non-increasing in c_s over {0, 10, 100, 300} km/s at every graded k (p = 0.5)", "monotone")
pc = grow(10.0, lambda a: 4.0)[3.0] / grow(10.0, lambda a: 0.0)[3.0]
P(f"  reported: pincer control, constant c_s = 4 km/s: T2(k = 10, z = 3) = {pc ** 2:.4f} (pincer: 'loses 7%' in its own setup)")

PGRID = [-0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]
S3B = {}
for f in FOOTS:
    S3B[f] = {}
    c0 = CSNEED[f]
    for p in PGRID:
        gr = grade(lambda a, c0=c0, p=p: c0 * a ** (p - 0.5))
        win = gr["forest"] != "FAIL" and gr["R_sigma8"] >= 0.95
        gr.update({"p": p, "cs_z3_kms": c0 * 0.25 ** (p - 0.5), "cs_z2_kms": c0 * (1 / 3) ** (p - 0.5), "cs_z0_kms": c0, "window": win})
        S3B[f][str(p)] = gr
        P(f"  {f} p = {p:+.1f}: c_s(z=3/2/0) = {gr['cs_z3_kms']:.3g} / {gr['cs_z2_kms']:.3g} / {c0:.3g} km/s; forest {gr['forest']} "
          f"(z3 bins {min(gr['bins_z3']):.3f}-{max(gr['bins_z3']):.3f}, T2(k5) z3/z2 {gr['T2_k5']['3']:.3f}/{gr['T2_k5']['2']:.3f}); "
          f"R_sigma8 {gr['R_sigma8']:.4f}; T2(z=0) at k 0.1/1/10: " + " / ".join(f"{v:.3f}" for v in gr["T2_z0_at_k_0.1_1_10"]) +
          f" -> window {win}")
WB = {p: all(S3B[f][str(p)]["window"] for f in FOOTS) for p in PGRID}
WINDOW_B_GRAV = [p for p in PGRID if WB[p] and p <= 0.5]
WINDOW_B_HEAT = [p for p in PGRID if WB[p] and p > 0.5]
P(f"  Window-B at p <= 0.5 (EOS only): {WINDOW_B_GRAV}; at p > 0.5 (needs late heating): {WINDOW_B_HEAT}")
RES["step3B"] = {"per_footing": S3B, "window_p_le_0.5": WINDOW_B_GRAV, "window_p_gt_0.5": WINDOW_B_HEAT, "pincer_control_T2_k10_z3": pc ** 2}

# ============================================================== STEP 3C: environment keys
P("\n== STEP 3C: environment keys (X19 variables placeable on FRW + delta_b)")


def cls(f, c, v):
    r = X19[(f, c)]
    return float(r[f"{v}_p16"]) if r[f"{v}_p16"] != "NA" else None, float(r[f"{v}_p84"]) if r[f"{v}_p84"] != "NA" else None


def t_age(a):                                                       # seconds
    return quad(lambda x: 1.0 / (x * H0_946 * Ea(x)), 0, a, epsabs=0, epsrel=1e-10, limit=400)[0]


def N_orb_uniform(rho_kg, a):                                      # t_age / t_orb, t_orb = 2 pi / sqrt(4 pi G rho / 3)
    return t_age(a) * math.sqrt(4 * math.pi * G_SI * rho_kg / 3) / (2 * math.pi)


DF_LO, DF_HI, DF_LOOSE = 0.1, 10.0, 100.0
S3C = {}
for f in FOOTS:
    K = {}
    s_lo = lambda v: min(cls(f, "SPARC small", v)[0], cls(f, "SPARC large", v)[0])
    s_hi = lambda v: max(cls(f, "SPARC small", v)[1], cls(f, "SPARC large", v)[1])
    bg = lambda v: cls(f, "Cosmic background", v)
    # rho_b
    blo, bhi = bg("rho_b")
    flo, fhi = RHOB0 * 27 * DF_LO, RHOB0 * 64 * DF_LOOSE
    Clo, Chi = min(blo, flo), max(bhi, fhi)
    ov = not (Chi < s_lo("rho_b") or Clo > s_hi("rho_b"))
    zm = (s_lo("rho_b") / RHOB0) ** (1 / 3) - 1
    K["rho_b"] = {"C": [Clo, Chi], "S": [s_lo("rho_b"), s_hi("rho_b")], "separates": not ov, "z_match_bg_enters_S_lo": zm,
                  "z_match_bg_enters_S_hi": (s_hi("rho_b") / RHOB0) ** (1 / 3) - 1, "type": "physical"}
    # x
    blo, bhi = bg("x")
    K["x"] = {"C": [blo, bhi], "S": [s_lo("x"), s_hi("x")], "separates": (bhi < s_lo("x")) or (blo > s_hi("x")), "type": "physical"}
    # rho_env
    blo, bhi = bg("rho_env")
    K["rho_env"] = {"C": [blo, bhi], "S": [s_lo("rho_env"), s_hi("rho_env")], "separates": (bhi < s_lo("rho_env")) or (blo > s_hi("rho_env")), "type": "physical"}
    # e, kT, H: background values by convention
    blo, bhi = bg("e")
    K["e"] = {"C": [blo, bhi], "S": [s_lo("e"), s_hi("e")], "separates": (bhi < s_lo("e")) or (blo > s_hi("e")), "type": "CONVENTION (background e set to 0)"}
    blo, bhi = bg("kT")
    K["kT"] = {"C": [blo, bhi], "S": [s_lo("kT"), s_hi("kT")], "separates": (bhi < s_lo("kT")) or (blo > s_hi("kT")), "type": "CONVENTION (SPARC kT set to 0: no X-ray gas)"}
    blo, bhi = bg("H")
    K["H"] = {"C": [blo, bhi], "S": [s_lo("H"), s_hi("H")], "separates": (bhi < s_lo("H")) or (blo > s_hi("H")), "type": "binary"}
    # N_orb: physical value for the cosmic medium (uniform-sphere t_orb at the epoch's density)
    rhom0 = RHOM946
    Nbg = [N_orb_uniform(rhom0 / a ** 3, a) for a in (1 / 1101, 1 / 4, 1 / 3, 1.0)]
    Nf = [N_orb_uniform(rhom0 * (1 + z) ** 3 * D, 1 / (1 + z)) for z in (2.0, 3.0) for D in (DF_LO, DF_HI, DF_LOOSE)]
    NCmax = max(Nbg + Nf)
    K["N_orb"] = {"C": [min(Nbg + Nf), NCmax], "C_background_z1100_3_2_0": Nbg, "C_forest": Nf, "S": [s_lo("N_orb"), s_hi("N_orb")],
                  "separates": NCmax < s_lo("N_orb"), "type": "physical (computed for the cosmic medium)",
                  "separates_strict_PROVISIONAL_10": max(Nbg + Nf[:2] + Nf[3:5]) < s_lo("N_orb")}
    # delta_b = rho_b / rho_b,mean(z)
    Sd = [s_lo("rho_b") / RHOB0, s_hi("rho_b") / RHOB0]
    K["delta_b"] = {"C": [0.0, DF_LOOSE], "C_PROVISIONAL": [DF_LO, DF_HI], "S": Sd, "separates": DF_LOOSE < Sd[0],
                    "gap_S_lo_over_C_hi_loose": Sd[0] / DF_LOOSE, "gap_S_lo_over_C_hi_PROVISIONAL": Sd[0] / DF_HI, "type": "physical (derived)"}
    S3C[f] = K
    for kname, v in K.items():
        P(f"  {f} {kname:8s}: C [{v['C'][0]:.3g}, {v['C'][1]:.3g}]  S [{v['S'][0]:.3g}, {v['S'][1]:.3g}]  separates {v['separates']}  ({v['type']})")
    P(f"     rho_b: the background enters S at z = {K['rho_b']['z_match_bg_enters_S_hi']:.1f} - {K['rho_b']['z_match_bg_enters_S_lo']:.1f} (S hi - lo); "
      f"N_orb background (z 1100/3/2/0) " + " / ".join(f"{v:.3f}" for v in Nbg) + f", forest max {max(Nf):.3f}; delta_b gap S_lo / 100 = {K['delta_b']['gap_S_lo_over_C_hi_loose']:.0f}")

# rho_b-key consequence: c_s,need on for z >= z_match (S lo), off after
P("  rho_b key consequence (sharp key at S lo: c_s = c_s,need while the background is above it):")
for f in FOOTS:
    zm = S3C[f]["rho_b"]["z_match_bg_enters_S_lo"]
    Nm = math.log(1 / (1 + zm))
    gr = grade(lambda a, c0=CSNEED[f], am=1 / (1 + zm): c0 if a < am else 0.0, segments=[Nm])
    S3C[f]["rho_b"]["consequence"] = gr
    P(f"    {f}: on for z >= {zm:.1f} at {CSNEED[f]:.1f} km/s -> forest {gr['forest']} (z3 bins {min(gr['bins_z3']):.3g}-{max(gr['bins_z3']):.3g}, "
      f"T2(k5) z3 {gr['T2_k5']['3']:.3g}); R_sigma8 {gr['R_sigma8']:.4f}")

# reported: rms linear peculiar gravity (mi_growth grms construction) vs SPARC e a0
sig8_t = 0.811
Am = sig8_t ** 2 / np.trapz(D2shape * Wth(kfine * 8.0) ** 2, np.log(kfine))
k_m = kfine * h_m / MPC_M
Ibase = math.sqrt(np.trapz(Am * D2shape / k_m ** 2, np.log(kfine)))
H0m = h_m * 100e3 / MPC_M
grms = {}
for z in (0.0, 2.0, 3.0):
    a = 1 / (1 + z)
    grms[z] = 1.5 * Om_m * H0m ** 2 / a ** 2 * (D_lcdm(a) / D_lcdm(1.0)) * Ibase
P("  reported: rms linear peculiar gravity g_rms(z = 0/2/3) = " + " / ".join(f"{grms[z]:.3e}" for z in (0.0, 2.0, 3.0)) + " m/s^2 = " +
  " / ".join(f"{grms[z] / A0['canonical']:.3f}" for z in (0.0, 2.0, 3.0)) + " a0 (canonical); SPARC e (16-84) " +
  f"{S3C['canonical']['e']['S'][0]:.3f}-{S3C['canonical']['e']['S'][1]:.3f}")
S3C["grms_m_s2"] = {str(z): grms[z] for z in grms}

# side effects of a delta_b (equivalently N_orb) key: classes on each side
side = {}
for f in FOOTS:
    side[f] = {}
    Slo = S3C[f]["delta_b"]["S"][0]
    for (ff, c), r in X19.items():
        if ff != f or c == "Cosmic background" or r["rho_b_p16"] == "NA":
            continue
        dlo, dhi = float(r["rho_b_p16"]) / RHOB0, float(r["rho_b_p84"]) / RHOB0
        where = "emptied by every separating threshold" if dlo >= Slo else ("kept by every separating threshold" if dhi <= DF_LOOSE else "threshold-dependent")
        side[f][c] = {"delta_b": [dlo, dhi], "label": r["label_LS"], "fate": where}
for c, v in side["canonical"].items():
    P(f"  side effect (canonical) {c:22s} delta_b {v['delta_b'][0]:.3g}-{v['delta_b'][1]:.3g}  label {v['label']:6s}  {v['fate']}")
S3C["delta_b_side_effects"] = side
RES["step3C"] = S3C

PHYS_SEP = [k for k in ("rho_b", "x", "rho_env", "N_orb", "delta_b") if all(S3C[f][k]["separates"] for f in FOOTS)]
CONV_SEP = [k for k in ("e", "kT") if all(S3C[f][k]["separates"] for f in FOOTS)]
P(f"  physical keys separating C from S on both footings: {PHYS_SEP}; convention-only separations (no weight): {CONV_SEP}")

# ============================================================== verdict
REQ = ("S0-1", "S0-2", "S0-3", "S0-4", "S0-5", "C1", "C2", "C3", "C4", "C5")
allok = all(RES["checks"][c]["pass"] for c in REQ)
grav_window = WINDOW_A or bool(WINDOW_B_GRAV)
if not allok:
    V = "UNDECIDED"
elif grav_window:
    V = "WINDOW EXISTS"
elif WINDOW_B_HEAT or PHYS_SEP:
    V = "WINDOW ONLY WITH A NON-GRAVITATIONAL EXCLUSION"
else:
    V = "NO WINDOW: the forest scale is smaller than the galaxy exclusion scale, so any cold component that passes the forest falls into galaxies"
GRAV_LINE = ("gravity alone (frozen cut, Jeans a^p with p <= 0.5): " + ("WINDOW" if grav_window else
             "NO WINDOW: any cold component that passes the forest falls into galaxies"))
RES["verdict"] = V
RES["gravity_alone"] = GRAV_LINE
RES["window_kinds"] = {"late_heating_p": WINDOW_B_HEAT, "keys": PHYS_SEP}
P(f"\nVERDICT: {V}")
P(f"  {GRAV_LINE}")
P(f"  non-gravitational routes open: late heating at p = {WINDOW_B_HEAT}; keys {PHYS_SEP}")
if MUT:
    must = ("S0-1", "S0-2", "S0-3", "S0-4", "S0-5", "C2", "C4")
    failed = [c for c in RES["checks"] if not RES["checks"][c]["pass"]]
    RES["mutate_required_fail"] = {c: (not RES["checks"][c]["pass"]) for c in must}
    P(f"MUTATE: required failures {must}: " + ", ".join(f"{c} {'FAILED' if not RES['checks'][c]['pass'] else 'passed (BAD)'}" for c in must)
      + f"; all failing checks {failed}")
RES["reads_sha256"] = READS
RES["runtime_s"] = time.time() - T0
RES["peak_rss_GB"] = rss_gb()
P(f"checks {sum(RES['checks'][c]['pass'] for c in RES['checks'])}/{len(RES['checks'])} PASS; runtime {RES['runtime_s']:.0f} s; peak RSS {RES['peak_rss_GB']:.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"x22_cosmic_dust_window_results{TAG}.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
sys.exit(0 if (allok and not MUT) else 1)
