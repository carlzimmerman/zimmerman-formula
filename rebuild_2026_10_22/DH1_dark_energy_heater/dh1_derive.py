#!/usr/bin/env python3
"""DH1_dark_energy_heater: is there a dark-energy-keyed, knob-free heater for the collisionless cold sector?

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (7ca9858740, committed alone).
kappa = 1/2 FITTED. Footings canonical / alt, never pooled. Cold dark energy = gravitating field component, never a
particle. No knob fitted or scanned. Not "theory closed". Nothing here says the data favour the framework or LCDM.

Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 dh1_derive.py               # exit 0
      PYTHONHASHSEED=0 DH1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 dh1_derive.py  # exit 1 by design
"""
import hashlib
import json
import math
import os
import re
import resource
import sys
import time

import numpy as np
import sympy as sp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # rebuild_2026_10_22
MUTATE = os.environ.get("DH1_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""

# MUTATE (frozen): m1 cooling exponent 2 -> 1; m2 matter dilution a^-3 -> a^-2; m3 drive gets a spatial gradient term
COOL = 1 if MUTATE else 2
DIL = 2 if MUTATE else 3
DRIVE_GRADIENT = MUTATE

C_KMS = 299792.458
FOOTINGS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}  # m/s^2
OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


P_X22 = os.path.join(ROOT, "X22_cosmic_dust_window", "x22_cosmic_dust_window_results.json")
P_X26 = os.path.join(ROOT, "X26_cold_sector_map", "x26_cold_sector_map_results.json")
P_X26OUT = os.path.join(ROOT, "X26_cold_sector_map", "x26_cold_sector_map.out")
P_X29 = os.path.join(ROOT, "X29_late_power_shear", "x29_late_power_shear_results.json")
P_X35 = os.path.join(ROOT, "X35_a0_tracks_ede", "x35_results.json")
INPUTS = [P_X22, P_X26, P_X26OUT, P_X29, P_X35]
x22 = json.load(open(P_X22))
x26 = json.load(open(P_X26))
x26out = open(P_X26OUT).read()
x29 = json.load(open(P_X29))
x35 = json.load(open(P_X35))

checks = {}


def check(name, ok, value, threshold):
    checks[name] = {"pass": bool(ok), "value": value, "threshold": threshold}
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value}  (line: {threshold})")


say("DH1_dark_energy_heater" + ("  [MUTATE: m1 cooling 2->1, m2 dilution a^-3->a^-2, m3 drive gradient]" if MUTATE else ""))
say("kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle; no knob fitted; not theory closed")
say()

# ---------------------------------------------------------------- step 0: record read-back
say("== Step 0: record read-back ==")
rec = {}
a, N, p_, m_, n_ = sp.symbols("a N p m n", positive=True)
# Jeans mapping: comoving lambda_J ~ c_s / (a sqrt(G rho)), rho ~ a^-DIL  =>  lambda_J ~ c_s a^(DIL/2 - 1)
# X22 defines lambda_J ~ a^p, so c_s ~ a^(p + 1 - DIL/2)  (= a^(p - 1/2) for DIL = 3)
cs_exp_of_p = sp.simplify(p_ + 1 - sp.Rational(DIL, 2))
dev0a = 0.0
for f in FOOTINGS:
    r = {}
    r["cs_need"] = x22["step2"]["per_footing"][f]["cs_need_kms"]
    for pp in ("2.0", "3.0"):
        row = x22["step3B"]["per_footing"][f][pp]
        r[pp] = {k: row[k] for k in ("cs_z3_kms", "cs_z2_kms", "cs_z0_kms", "forest", "p")}
        e = float(cs_exp_of_p.subs(p_, row["p"]))
        dev0a = max(dev0a, abs(row["cs_z3_kms"] / row["cs_z0_kms"] - 4.0 ** (-e)),
                    abs(row["cs_z2_kms"] / row["cs_z0_kms"] - 3.0 ** (-e)))
    r["k_hm_NF"] = x22["step1"]["alpha_NF"]["k_hm_hMpc"]
    r["x_separates"] = x22["step3C"][f]["x"]["separates"]
    r["x_C"] = x22["step3C"][f]["x"]["C"]
    r["x_S"] = x22["step3C"][f]["x"]["S"]
    rec[f] = r
grms = x22["step3C"]["grms_m_s2"]
check("K0a X22 p = 2 / 3 rows obey c_s ~ a^(p - 1/2) under this lane's Jeans mapping", dev0a < 1e-9,
      f"max |dev| {dev0a:.2e}; c_s,need {rec['canonical']['cs_need']:.3f} / {rec['alt']['cs_need']:.3f} km/s; "
      f"p=2 forest {rec['canonical']['2.0']['forest']}, p=3 {rec['canonical']['3.0']['forest']}", "<= 1e-9")

# X26: KT-median c_s range, sigma medians, virial r = 1 line
sig = {}
for f in FOOTINGS:
    m = re.search(rf"{f} SPARC median \(sigma ([0-9.]+) km/s", x26out)
    k = re.search(rf"{f} KT cluster median \(sigma ([0-9.]+) km/s", x26out)
    sig[f] = (float(m.group(1)), float(k.group(1)))
    rec[f]["sig_SPARC"], rec[f]["sig_KT"] = sig[f]
    rec[f]["cs_KT"] = x26["energy"][f]["KT cluster median"]["cs_kms"]
    rec[f]["cs_SPARC_sheet"] = x26["energy"][f]["SPARC median"]["cs_kms"]
    rec[f]["virial_r1_any"] = x26["special_cases"][f]["virial r=1,q=0 (B)"]["any"]
    rec[f]["universal_any"] = x26["special_cases"][f]["universal r=q=0 (B)"]["any"]
ok0b = all(abs(sig[f][0] - 70.5) < 0.05 and abs(sig[f][1] - 517.1) < 0.05 and rec[f]["virial_r1_any"] is False
           for f in FOOTINGS)
check("K0b X26 sigma medians and virial r=1 line", ok0b,
      f"sigma SPARC/KT {sig['canonical']} / {sig['alt']}; KT c_s canonical {rec['canonical']['cs_KT'][0]:.1f}-"
      f"{rec['canonical']['cs_KT'][1]:.1f}, alt {rec['alt']['cs_KT'][0]:.1f}-{rec['alt']['cs_KT'][1]:.1f}; "
      f"virial any = {rec['canonical']['virial_r1_any']} / {rec['alt']['virial_r1_any']}",
      "70.5 / 517.1 km/s; any = false")

# X29: survivors and C0 cap
nsurv = {}
for f in FOOTINGS:
    pts = x29["footings"][f]["points"]
    s = [q for q in pts if abs(q["KiDS"]["dchi2"]) < 1e6 and q["KiDS"]["dchi2"] < 9]
    nsurv[f] = len(s)
    rec[f]["C0_cap"] = max(10 ** q["log10_C0"] for q in s)
check("K0c X29 survivors (finite KiDS dchi2 < 9)", nsurv["canonical"] == 23 and nsurv["alt"] == 15,
      f"{nsurv['canonical']} / {nsurv['alt']}; cosmic C0 cap {rec['canonical']['C0_cap']:.1f} / {rec['alt']['C0_cap']:.1f} km/s",
      "23 / 15")

# X35: CFG689 sqrtX read-back
s035 = x35["step0"]["cfg689_sqrtX_med_2p33"]
sqrtX = (s035["BAO+SN"], s035["BAO"])
check("K0d X35 S0-3 CFG689 sqrtX(z* 2.33)", abs(sqrtX[0] - 0.9094) < 1e-4 and abs(sqrtX[1] - 0.9498) < 1e-4,
      f"{sqrtX}", "0.9094 / 0.9498")
say()

# ---------------------------------------------------------------- K1: sympy derivations
say("== K1: derivations (sympy) ==")
eps, c2, f0, u = sp.symbols("epsilon c2 f0 u", positive=True)
# D1: thermal specific energy u = (3/2) sigma^2 of a free collisionless medium, u ~ a^-COOL without source;
#     source per unit mass eps c^2 df/dN, f = rho_DE / rho_m = f0 e^(DIL N) (Lambda, matter ~ a^-DIL)
fN = f0 * sp.exp(DIL * N)
# particular (zero-initial) solution: u = A f with A from the ODE
A = sp.symbols("A")
Asol = sp.solve(sp.Eq(sp.diff(A * fN, N), -COOL * A * fN + eps * c2 * sp.diff(fN, N)), A)[0]
# X24b D1 (per-mass source eps c^2 f dN, i.e. Q = eps H rho_L c^2): u = eps c^2 f / 5
Asol_X24b = sp.solve(sp.Eq(sp.diff(A * fN, N), -COOL * A * fN + eps * c2 * fN), A)[0]
d1_ok = sp.simplify(Asol - sp.Rational(3, 5) * eps * c2) == 0 and sp.simplify(Asol_X24b - eps * c2 / 5) == 0
cs_exp_H1 = sp.Rational(DIL, 2)  # c_s ~ sqrt(u) ~ a^(DIL/2)
p_H1 = sp.solve(sp.Eq(cs_exp_of_p, cs_exp_H1), p_)[0]
say(f"  D1 H1 background: u = {Asol} * f  (X24b's Q = eps H rho_L c^2 form gives {Asol_X24b} * f);"
    f" c_s ~ a^{cs_exp_H1}  =>  X22 p = {p_H1}")
# D2: S ~ d(f^n)/dN  => c_s ~ a^(DIL n / 2)  => p ; p >= 3 needs n >= n_min
p_n = sp.solve(sp.Eq(cs_exp_of_p, sp.Rational(DIL, 2) * n_), p_)[0]
n_min = sp.solve(sp.Eq(p_n, 3), n_)[0]
say(f"  D2 power key S ~ f^n: p = {sp.simplify(p_n)};  p >= 3 needs n >= {n_min}")
d2_ok = sp.simplify(p_n - (sp.Rational(3, 2) * n_ + sp.Rational(1, 2))) == 0 and n_min == sp.Rational(5, 3)
# D3: Hamiltonian with homogeneous drive; deformation (Riccati) source is d2H/dx2
x, pm, t = sp.symbols("x p_m t", real=True)
At, Bt, Ct, Et = [sp.Function(s)(t) for s in ("A", "B", "C", "E")]
Phi = sp.Function("Phi")(x, t)
H = At * pm ** 2 / 2 + Bt * x * pm + Ct * x + Phi + (Et * sp.cos(x) if DRIVE_GRADIENT else 0)
Hxx = sp.diff(H, x, 2)
Hxp = sp.diff(H, x, pm)
Hpp = sp.diff(H, pm, 2)
d3_ok = sp.simplify(Hxx - sp.diff(Phi, x, 2)) == 0
say(f"  D3 d2H/dx2 = {Hxx};  d2H/dxdp = {Hxp};  d2H/dp2 = {Hpp}")
say("     Riccati for M = dp/dx along the sheet: dM/dt = -Hpp M^2 - 2 Hxp M - Hxx. The drive enters only Hpp and Hxp")
say("     (identity-proportional rescaling); folds (multi-stream, dispersion) are sourced only by Hxx = Phi''.")
# D4: homogeneous anti-friction v' = -(H - G) v  in a bound system: d(sigma^2)/dt|drive = 2 G sigma^2
Gm, s2 = sp.symbols("Gamma sigma2", positive=True)
rate = 2 * Gm * s2
d4_ok = sp.simplify(sp.diff(rate / s2, s2)) == 0
say(f"  D4 drive heating d(sigma^2)/dt = {rate}: proportional to sigma^2 (scale-free)  =>  c_s = A(t) sigma, r = 1")
# D5: wave medium omega = D k^2; driven at rate Gamma excites k_res = sqrt(Gamma/D), v = 2 D k_res; forest D k_f <= v_f
D_, kf, vf, Gam = sp.symbols("D k_f v_f Gamma_d", positive=True)
v_res = sp.simplify(2 * D_ * sp.sqrt(Gam / D_))
v_bound = sp.simplify(v_res.subs(D_, vf / kf))
d5_ok = sp.simplify(v_bound - 2 * sp.sqrt(vf * Gam / kf)) == 0
say(f"  D5 v_res = {v_res};  with D <= v_f/k_f:  v <= {v_bound}")
check("K1 sympy D1-D5", d1_ok and d2_ok and d3_ok and d4_ok and d5_ok,
      f"D1 {d1_ok} D2 {d2_ok} D3 {d3_ok} D4 {d4_ok} D5 {d5_ok}", "all True")
say()

# ---------------------------------------------------------------- K2: numerical cold sheet
say("== K2: 1-D cold sheet under a homogeneous drive (D3 numerically) ==")
rng = np.random.default_rng(20261025)
NP = 4000
x0 = np.linspace(0, 2 * np.pi, NP, endpoint=False)


def run_sheet(well, drive_grad, nstep=4000, dt=2e-3):
    xs = x0.copy()
    ps = np.zeros(NP)
    knots = rng.normal(size=(4, 9))
    tt = np.linspace(0, nstep * dt, 9)
    for i in range(nstep):
        ti = i * dt
        Ai, Bi, Ci, Ei = (1.0 + 0.5 * np.tanh(np.interp(ti, tt, knots[0])),
                          0.3 * np.interp(ti, tt, knots[1]), np.interp(ti, tt, knots[2]), np.interp(ti, tt, knots[3]))
        # force -dH/dx, velocity dH/dp (symplectic Euler)
        F = -Bi * ps - Ci
        if well:
            F = F - 1.0 * np.sin(xs)          # Phi = -cos(x)
        if drive_grad:
            F = F + 3.0 * Ei * np.sin(xs)     # E(t) cos(x) term from the mutated drive
        ps = ps + dt * F
        xs = xs + dt * (Ai * ps + Bi * xs)
    # streams: count sign changes of dx/dx0 (a fold makes the Lagrangian map non-monotone)
    dx = np.diff(xs)
    folds = int(np.sum(dx <= 0))
    return folds, float(np.ptp(ps))


folds_drive, ptp_drive = run_sheet(well=False, drive_grad=DRIVE_GRADIENT)
folds_well, _ = run_sheet(well=True, drive_grad=False)
say(f"  drive only{' (+ gradient, MUTATE)' if DRIVE_GRADIENT else ''}: folds {folds_drive}, momentum spread {ptp_drive:.2e}")
say(f"  control (cos well, no drive): folds {folds_well}")
check("K2 homogeneous drive keeps the sheet single-stream; a well folds it",
      folds_drive == 0 and ptp_drive <= 1e-12 and folds_well > 0,
      f"drive folds {folds_drive}, spread {ptp_drive:.1e}; control folds {folds_well}", "0, <= 1e-12; > 0")
say()

# ---------------------------------------------------------------- grading
say("== Grading H1-H6 per footing (gates G1-G5) ==")
H0_over_k = {f: 100.0 / rec[f]["k_hm_NF"] for f in FOOTINGS}  # km/s, h cancels
Om, OL = 0.315, 0.685  # PROVISIONAL, reported trigger epochs only
f_today = OL / Om
z_acc = (2 * OL / Om) ** (1 / 3) - 1
z_eqL = (OL / Om) ** (1 / 3) - 1
kap = 0.5
OmL_milgrom = 2 / (3 * math.pi * kap ** 2)
a3 = (Om / OL) * OmL_milgrom / (1 - OmL_milgrom)
z_milgrom = a3 ** (-1 / 3) - 1
a0_over_cH0 = kap * math.sqrt(3 * OL / (8 * math.pi))

results = {}
for f in FOOTINGS:
    r = rec[f]
    csn, sS, sK = r["cs_need"], r["sig_SPARC"], r["sig_KT"]
    lo, hi = r["cs_KT"]
    cap = r["C0_cap"]
    e3, e2 = r["3.0"]["cs_z3_kms"], r["3.0"]["cs_z2_kms"]
    g = {}

    # H1 ratio-rate heater (universal per mass, background rho_m)
    eH1 = float(cs_exp_H1)
    cs3, cs2 = csn * 4 ** (-eH1), csn * 3 ** (-eH1)
    # most forgiving variant: bound heat factor beta in [1, 5] (u_bound / u_cos), quadrature with sigma_well
    C_min_cl = math.sqrt(max(lo ** 2 - sK ** 2, 0) / 5)
    C_max_cl = math.sqrt(hi ** 2 - sK ** 2)
    C_min_sp = math.sqrt(max(csn ** 2 - sS ** 2, 0) / 5)
    Cwin = (max(C_min_cl, C_min_sp), min(C_max_cl, cap))
    cs3v, cs2v = Cwin[0] * 4 ** (-eH1), Cwin[0] * 3 ** (-eH1)
    s_nat = 2 * math.log(sqrtX[0]) / math.log(3.33)  # BAO+SN anchor (largest drift)
    cs3n = csn * 4 ** (-eH1) * 4 ** (s_nat / 2)
    cs2n = csn * 3 ** (-eH1) * 3 ** (s_nat / 2)
    eps_need = [15 * (C / C_KMS) ** 2 / (2 * f_today) / 3 for C in Cwin]  # per-mass eps c^2 df/dt; u = 3/5 eps c^2 f
    C_nat = C_KMS * math.sqrt(2 / 5 * f_today)
    g["H1"] = {
        "G1": ["FAIL", f"needs eps = {eps_need[0]:.2e}-{eps_need[1]:.2e} (fitted); eps = 1 gives cosmic c_s {C_nat:.0f} km/s"],
        "G2": ["FAIL" if (cs3 > e3 or cs2 > e2) else "PASS",
               f"c_s ~ a^{eH1:.2f} (p = {float(p_H1):.2f}); c_s(z3/z2) {cs3:.2f}/{cs2:.2f} vs edge {e3:.3f}/{e2:.3f};"
               f" forgiving C_min {Cwin[0]:.1f}: {cs3v:.2f}/{cs2v:.2f}; native DE drift (CFG689 sqrtX {sqrtX[0]}): "
               f"{cs3n:.2f}/{cs2n:.2f}"],
        "G3": ["FAIL", "D3: a spatially uniform per-mass source on a single-stream sheet adds no fine-grained spread; "
                       "a 'heat' term is not Hamiltonian, i.e. not an action term (H1 is a phenomenological source)"],
        "G4": ["NOT DECISIVE", f"bound/cosmic heat factor beta in [1,5]: cosmic C window {Cwin[0]:.1f}-{Cwin[1]:.1f} km/s "
                               f"(open only in this most forgiving reading)"],
        "G5": ["REDUCES", "background time law identical to X24b D1 (u ~ a^3, p = 2); differs only in spatial key (q = 0 vs -1)"],
    }
    # H1L local rho_m
    g["H1L"] = {
        "G1": ["FAIL", "same eps as H1"],
        "G2": ["PASS", "no heating in the linear medium beyond H1's"],
        "G3": ["FAIL", "d(rho_DE/rho_m,loc)/dt < 0 during collapse (cooling), = 0 once virialised"],
        "G4": ["FAIL", f"virialised SPARC gets no heat: c_s = sigma {sS:.1f} < c_s,need {csn:.1f}"],
        "G5": ["REDUCES", "sign structure of X24b's local theta/3 reading"],
    }
    # H2 coherent drive
    A_gal, A_cl = csn / sS, hi / sK
    g["H2"] = {
        "G1": ["FAIL", "drive rate Gamma_DE needs a coupling beta (knob)"],
        "G2": ["PASS", "cold cosmic sheet stays cold (D3)"],
        "G3": ["FAIL", "D3 + D4: only rescales gravitationally generated dispersion; heating ~ sigma^2"],
        "G4": ["FAIL", f"r = 1: SPARC needs A >= {A_gal:.3f}, KT clusters allow A <= {A_cl:.3f} (disjoint); "
                       f"X26 virial line any = {r['virial_r1_any']}"],
        "G5": ["DISTINCT", "multiplicative (r = 1), not X23/X24b's additive heat; lands on X26's excluded virial line"],
    }
    # H3 epoch trigger
    g["H3"] = {
        "G1": ["FAIL", f"latent specific energy is a knob; natural rho_L c^2/rho_c per mass = {OL / (Om * 5.364 / 6.364):.2f} c^2"],
        "G2": ["PASS", f"knob-free DE epochs: z(a''=0) {z_acc:.3f}, z(Omega_L=Omega_m) {z_eqL:.3f}, "
                       f"z(a0 = cH/2pi, kappa 1/2) {z_milgrom:.3f} (future); a0/(cH0) = {a0_over_cH0:.4f}"],
        "G3": ["FAIL", "D3: a homogeneous release cannot create fine-grained dispersion; it can only shift or rescale"],
        "G4": ["FAIL", "if released as rescaling: r = 1 (as H2); as bulk shift: no dispersion"],
        "G5": ["DISTINCT", "step in time; still homogeneous"],
    }
    # H4 a0-triggered local phase change (key g < a0(z))
    xr2 = grms["2.0"] / A0[f]
    xr3 = grms["3.0"] / A0[f]
    g["H4"] = {
        "G1": ["FAIL", "threshold and latent energy are knobs"],
        "G2": ["FAIL", f"cosmic medium is already below a0 at z = 2 / 3: x_rms {xr2:.3f} / {xr3:.3f}; the key fires before z = 2"],
        "G3": ["FAIL", "trigger region is the whole (uniform) cosmic medium: homogeneous release, D3"],
        "G4": ["FAIL", f"X22: key x does not separate cosmic medium from SPARC (separates = {r['x_separates']}; "
                       f"C {r['x_C']}, S {r['x_S']})"],
        "G5": ["DISTINCT", "acceleration key; with Lambda, a0 is constant, so there is no a0 epoch at all"],
    }
    # H5 wave medium
    v5 = 2 * math.sqrt(e2 * 3 * H0_over_k[f])
    need_sp = math.sqrt(csn ** 2 - sS ** 2)
    need_cl = math.sqrt(lo ** 2 - sK ** 2)
    g["H5"] = {
        "G1": ["FAIL", "D (the wave constant) is a knob"],
        "G2": ["PASS", "medium cold at z 2-3 by construction of the bound"],
        "G3": ["FAIL", f"D5: v <= 2 sqrt(v_f 3H0/k_f) = {v5:.1f} km/s (v_f {e2:.2f}, H0/k_f {H0_over_k[f]:.3f} km/s, generous) "
                       f"vs need {need_sp:.1f} (SPARC quadrature) / {need_cl:.1f} (KT quadrature)"],
        "G4": ["FAIL", f"factor {need_sp / v5:.1f} short in SPARC"],
        "G5": ["DISTINCT", "kinetic by construction; bounded by the forest itself"],
    }
    # H6 random kick field, sigma^2 = sigma_well^2 + v_k^2
    vk_lo = max(math.sqrt(lo ** 2 - sK ** 2), need_sp)
    vk_hi = min(math.sqrt(hi ** 2 - sK ** 2), cap)
    g["H6"] = {
        "G1": ["FAIL", "v_k and a correlation length l are knobs"],
        "G2": ["PASS", "step after the trigger"],
        "G3": ["FAIL", f"needs a stochastic force with l << system; the DE sector's only lengths are c/H0 = "
                       f"{C_KMS / 67.4 / 1e3:.2f} Gpc (h 0.674, PROVISIONAL) and c^2/a0 = "
                       f"{(C_KMS * 1e3) ** 2 / A0[f] / 3.0857e25:.1f} Gpc; L* >= 21.7/22.9 pc is one-sided (a knob)"],
        "G4": ["OPEN" if vk_lo <= vk_hi else "FAIL",
               f"v_k window {vk_lo:.1f}-{vk_hi:.1f} km/s (approx., A9)"],
        "G5": ["DISTINCT", "additive floor; its cluster c_s/sigma_KT lies in X30's failing range"],
    }
    found = [h for h, gg in g.items() if all(gg[k][0] in ("PASS", "OPEN", "NOT DECISIVE") for k in ("G1", "G2", "G3", "G4"))
             and all(gg[k][0] == "PASS" for k in ("G1", "G2", "G3"))]
    each_fails = all(any(gg[k][0] == "FAIL" for k in ("G1", "G2", "G3", "G4")) for gg in g.values())
    results[f] = {"gates": g, "found": found, "each_fails": each_fails,
                  "inherited": {"X30": f"KT c_s/sigma_KT {lo / sK:.3f}-{hi / sK:.3f}: X30 OUTER fails all sheet points",
                                "X32": "collisionless sigma_1D = c_s EXCLUDED in all 4 combinations (lane UNDECIDED on K4)"}}
    say(f"-- {f} --")
    for h, gg in g.items():
        say(f"  {h}: " + "; ".join(f"{k} {v[0]}" for k, v in gg.items()))
        for k, v in gg.items():
            say(f"      {k}: {v[1]}")
    say(f"  inherited: {results[f]['inherited']['X30']}; X32 {results[f]['inherited']['X32']}")
    say()

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
check("K3 peak RSS", rss < 1.0, f"{rss:.3f} GB", "< 1 GB")

allok = all(c["pass"] for c in checks.values())
verdict = {}
for f in FOOTINGS:
    if not allok:
        verdict[f] = "UNDECIDED (check failure)"
    elif results[f]["found"]:
        verdict[f] = "CANDIDATE FOUND: " + ", ".join(results[f]["found"])
    elif results[f]["each_fails"]:
        verdict[f] = "OBSTRUCTION"
    else:
        verdict[f] = "UNDECIDED"
say()
say(f"VERDICT canonical: {verdict['canonical']}   alt: {verdict['alt']}")

res = {"lane": "DH1_dark_energy_heater", "criteria": "7ca9858740", "mutate": MUTATE,
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle; no knob; not theory closed",
       "inputs_sha256": {os.path.relpath(pth, os.path.dirname(ROOT)): sha(pth) for pth in INPUTS},
       "checks": checks, "record": rec, "sqrtX_CFG689": sqrtX,
       "derived": {"p_H1": str(p_H1), "n_min_for_p3": str(n_min), "u_H1_over_f": str(Asol), "u_X24b_over_f": str(Asol_X24b),
                   "Hxx": str(Hxx), "z_acc": z_acc, "z_OmL_eq_Om": z_eqL, "z_milgrom_crossing": z_milgrom,
                   "a0_over_cH0": a0_over_cH0, "PROVISIONAL_Om_OL": [Om, OL]},
       "K2": {"folds_drive": folds_drive, "spread_drive": ptp_drive, "folds_control": folds_well},
       "results": results, "verdict": verdict, "runtime_s": time.time() - T0, "peak_rss_GB": rss}
json.dump(res, open(os.path.join(HERE, f"dh1_results{SUF}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"dh1_derive{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if allok else 1)
