"""CT8 dust phase tie: candidate relations R1-R6 (FROZEN_CRITERIA.md) and G5 through vanilla CLASS 3.3.4 with the
raw Planck PR3 TT file already on disk (CT3's peak finder). No downloads. Run:
OMP_NUM_THREADS=1 nice -n 10 python3 ct8_dust_tie.py > ct8_dust_tie.out   (a few minutes, < 0.5 GB).
kappa = 1/2 FITTED. Adopts nothing; reinstates nothing; no particle."""
import json, os
import numpy as np
from classy import Class

G = 6.6743e-11; C = 2.99792458e8; HBAR = 1.054571817e-34; MPC = 3.0856775814913673e22; EV = 1.602176634e-19
RHO100 = 3 * (1e5 / MPC) ** 2 / (8 * np.pi * G)          # critical density at h = 1, kg/m^3
KAPPA = 0.5                                               # FITTED
# ---- raw inputs (FROZEN_CRITERIA.md) ----
OL, OL_ERR = 0.666, 0.018                                 # raw SN shape (prep_2026/sne_lambda/VERIFY.md)
H_LO, H_HI = 0.6722, 0.6856                               # native H0 band, C2 K5
H_C = 0.5 * (H_LO + H_HI)
OB_C, OB_LO, OB_HI = 0.0224, 0.0217, 0.0229               # BBN D/H
TCMB, NEFF = 2.7255, 3.046
w_g = 2.4728e-5 * (TCMB / 2.7255) ** 4                    # photons, omega_gamma
w_r = w_g * (1 + 0.22711 * NEFF)
wDE_c = OL * H_C ** 2
wDE_lo, wDE_hi = (OL - OL_ERR) * H_LO ** 2, (OL + OL_ERR) * H_HI ** 2
wDE_sens = {"meas_a0_GLS": 9.307538e-27 / RHO100, "meas_a0_median": 6.307341e-27 / RHO100}
out = {"inputs": {"omega_DE": [wDE_c, wDE_lo, wDE_hi], "omega_b": [OB_C, OB_LO, OB_HI], "omega_r": w_r, "h": H_C,
                  "omega_DE_sensitivity": wDE_sens}}
print(f"inputs: omega_DE {wDE_c:.4f} [{wDE_lo:.4f}, {wDE_hi:.4f}]  omega_b {OB_C} [{OB_LO}, {OB_HI}]  omega_r {w_r:.4e}  h {H_C:.4f}")
print(f"  sensitivity omega_DE from measured a0 at kappa 1/2: GLS {wDE_sens['meas_a0_GLS']:.4f}, median {wDE_sens['meas_a0_median']:.4f}")
print(f"  circular trap (not used): (1.1312/0.93603)^2 = {(1.1312/0.93603)**2:.4f} = 1/{1/(1.1312/0.93603)**2:.4f}")

rel = {}
# ---- R1 shift charge ----
rel["R1"] = {"prediction": None, "note": "rho_x a^3 = Q0 I0/(8 pi G); I0 integration constant; d/da0 = d/dLambda = 0 (C2 K2)"}
print("R1 shift charge: NO PREDICTION (I0 is an initial datum)")

# ---- R2 rate tie ----
def Hz_over_sqrtGrho(z, wDE, wm):   # H(z)/sqrt(G rho_DE)
    return np.sqrt(8 * np.pi / 3) * np.sqrt(1 + (wm * (1 + z) ** 3 + w_r * (1 + z) ** 4) / wDE)
for name, n in [("kappa (a0/c)", KAPPA), ("sqrt(8pi/3) (de Sitter)", np.sqrt(8 * np.pi / 3))]:
    hmin = Hz_over_sqrtGrho(-1 + 1e-9, wDE_c, OB_C) if False else np.sqrt(8 * np.pi / 3)   # H -> H_dS as a -> inf
    reached = n > np.sqrt(8 * np.pi / 3)
    print(f"R2 rate n = {name} = {n:.4f}: H(z) >= H_dS = {np.sqrt(8*np.pi/3):.4f} sqrt(G rho_DE) at all z -> onset {'reached' if reached else 'NEVER (only as a -> infinity)'}")
n_need = Hz_over_sqrtGrho(3e4, wDE_c, OB_C)
n_need_rec = Hz_over_sqrtGrho(1090, wDE_c, OB_C)
print(f"  pure number n needed for onset at z 3e4: {n_need:.3e}; at z 1090: {n_need_rec:.3e}")
rel["R2"] = {"omega_x_rec": 0.0, "ratio": 0.0, "n_needed_z3e4": n_need, "n_needed_z1090": n_need_rec}

# ---- R3 hbar-scale misalignment ----
rhoDE = wDE_c * RHO100
E = (HBAR * C) ** 0.75 * (rhoDE * C ** 2) ** 0.25           # J
m_eV = E / EV
Hosc = E / HBAR
H0 = H_C * 1e5 / MPC
z_osc = (Hosc / (H0 * np.sqrt(w_r / H_C ** 2))) ** 0.5     # radiation era, constant g* (rough)
print(f"R3 misalignment: m c^2 = {m_eV:.3e} eV; onset H = m: z_osc ~ {z_osc:.2e} (constant g*, rough); amount ~ theta_i^2: NO PREDICTION; a boson of definite mass: excluded by the no-particle rule")
rel["R3"] = {"m_eV": m_eV, "z_osc_rough": z_osc, "prediction": None}

# ---- R4 epoch-free invariant ----
def r4(wDE, N=1.0): return (N * w_r ** 3 * wDE) ** 0.25
wx4 = r4(wDE_c)
N_need = (5.36 * OB_C) ** 4 / (w_r ** 3 * wDE_c)
N_need_lo = (4.9 * OB_C) ** 4 / (w_r ** 3 * wDE_c); N_need_hi = (5.4 * OB_C) ** 4 / (w_r ** 3 * wDE_c)
print(f"R4 invariant rho_x^4 = N rho_r^3 rho_DE, N = 1: omega_x {wx4:.3e}, ratio {wx4/OB_C:.4f}; N the data need: {N_need:.3e} (window {N_need_lo:.2e}-{N_need_hi:.2e}); N^(1/4) {N_need**0.25:.1f}")
print(f"  baryons on the same invariant: omega_b^4/(omega_r^3 omega_DE) = {OB_C**4/(w_r**3*wDE_c):.3e}")
rel["R4"] = {"omega_x": wx4, "ratio": wx4 / OB_C, "N_needed": N_need, "N_window": [N_need_lo, N_need_hi]}

# ---- R5 present-epoch equality ----
rel["R5"] = {"omega_x": wDE_c, "ratio": wDE_c / OB_C, "range": [wDE_lo / OB_HI, wDE_hi / OB_LO]}
print(f"R5 rho_x(0) = rho_DE: omega_x {wDE_c:.4f}, ratio {wDE_c/OB_C:.2f} [{wDE_lo/OB_HI:.2f}, {wDE_hi/OB_LO:.2f}]")

# ---- R6 Machian coincidence a0 = G M_m(<c/H0)/(c/H0)^2 ----
c1 = 3 * KAPPA / (4 * np.pi) * np.sqrt(8 * np.pi / 3)
# canonical: m = rho_m/rho_DE solves m = c1 sqrt(1 + m)  (radiation at z 0 neglected, 1e-4)
m_can = (c1 ** 2 + np.sqrt(c1 ** 4 + 4 * c1 ** 2)) / 2
def r6_can(wDE, wb): return m_can * wDE - wb
# x-only reading (disclosed, not graded): x = c1 sqrt(1 + x + b), b = wb/wDE
def r6_xonly(wDE, wb):
    b = wb / wDE; x = (c1 ** 2 + np.sqrt(c1 ** 4 + 4 * c1 ** 2 * (1 + b))) / 2; return x * wDE
# alt footing a0 = kappa c sqrt(G rho_tot): Omega_m = c1 exactly; omega_m = wDE c1/(1 - c1)
def r6_alt(wDE, wb): return wDE * c1 / (1 - c1) - wb
rows6 = {}
for nm, f in [("canonical", r6_can), ("alt", r6_alt), ("x_only_disclosed", r6_xonly)]:
    cen = f(wDE_c, OB_C); lo = f(wDE_lo, OB_HI) / OB_HI; hi = f(wDE_hi, OB_LO) / OB_LO
    rows6[nm] = {"omega_x": cen, "ratio": cen / OB_C, "ratio_range": [lo, hi]}
    print(f"R6 {nm}: omega_x {cen:.4f}, ratio {cen/OB_C:.3f} [{lo:.3f}, {hi:.3f}]")
for k, w in wDE_sens.items():
    print(f"  R6 canonical, sensitivity {k}: ratio {r6_can(w, OB_C)/OB_C:.2f}; R5: {w/OB_C:.2f}")
print(f"  c1 = (3 kappa/4 pi) sqrt(8 pi/3) = {c1:.5f}; canonical rho_m/rho_DE = {m_can:.4f}; alt Omega_m = {c1:.4f}")
rel["R6"] = rows6

# ---- G5: CLASS ----
HERE = os.path.dirname(os.path.abspath(__file__))
def peaks(p, base):
    c = Class(); q = dict(base); q.update(p); c.set(q); c.compute()
    cl = c.raw_cl(2200); ll = cl["ell"][2:]; DD = ll * (ll + 1) * cl["tt"][2:]
    pk = [(ll[i], DD[i]) for i in range(5, len(DD) - 5) if DD[i] == DD[i - 5:i + 6].max() and ll[i] > 100][:3]
    c.struct_cleanup(); return pk[2][1] / pk[1][1], [int(x[0]) for x in pk]
ct3base = {"h": 0.6736, "omega_b": 0.02237, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "YHe": 0.2454, "output": "tCl", "l_max_scalars": 2200}
chk, _ = peaks({"omega_cdm": 0.12}, ct3base)
print(f"CHECK CT3 row omega_c 0.12: H3/H2 {chk:.3f} (CT3 0.992; |d| <= 0.002: {'OK' if abs(chk-0.992) <= 0.002 else 'FAIL'})")
base = dict(ct3base); base.update({"h": H_C, "omega_b": OB_C})
g5 = {"check_ct3": chk}
graded = [("R2", 0.0), ("R4", wx4), ("R5", wDE_c), ("R6_canonical", rows6["canonical"]["omega_x"]),
          ("R6_alt", rows6["alt"]["omega_x"]), ("R6_x_only_disclosed", rows6["x_only_disclosed"]["omega_x"])]
for nm, wx in graded:
    res = {}
    for ns in [0.93, 0.9649, 1.0]:
        r, l = peaks({"omega_cdm": max(wx, 0.0), "n_s": ns}, base); res[ns] = r
    inwin = [0.969 <= v <= 0.989 for v in res.values()]
    ratio = wx / OB_C
    if 4.9 <= ratio <= 5.4 and all(inwin): v = "PASS"
    elif not any(inwin): v = "FAIL"
    else: v = "NO VERDICT"
    g5[nm] = {"omega_x": wx, "ratio": ratio, "H3H2": {str(k): x for k, x in res.items()}, "verdict": v}
    print(f"G5 {nm}: omega_x {wx:.4f} ratio {ratio:.3f}  H3/H2 n_s 0.93/0.9649/1.0 = {res[0.93]:.3f}/{res[0.9649]:.3f}/{res[1.0]:.3f}  -> {v}")
out["relations"] = rel; out["G5"] = g5
json.dump(out, open(os.path.join(HERE, "ct8_dust_tie.json"), "w"), indent=1, default=float)
