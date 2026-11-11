#!/usr/bin/env python3
"""NBC1: can a0 be a contact strength between cold dark energy and neutral baryons?

Criteria: FROZEN_CRITERIA.md (committed alone first). SI throughout. One thread.
Usage: python3 nbc1.py            -> base run (nbc1.out via redirect, nbc1.json)
       python3 nbc1.py M1|M2|M3   -> mutation twin (separate json: nbc1_MUT_<id>.json)
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import json
import math
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import erf

MUT = sys.argv[1] if len(sys.argv) > 1 else None
assert MUT in (None, "M1", "M2", "M3")

# ---- constants (SI) ----
G = 6.67430e-11
C_LIGHT = 2.99792458e8
KB = 1.380649e-23
H_PLANCK = 6.62607015e-34
M_E = 9.1093837015e-31
M_H = 1.6735575e-27
EV = 1.602176634e-19
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
MPC = 1e6 * PC
GYR = 3.15576e16
R_SUN = 6.957e8
MSUN_PC2 = MSUN / PC**2            # kg/m^2

FOOTINGS = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
K_VALUES = {"1": 1.0, "pi": math.pi, "2pi": 2.0 * math.pi}
if MUT == "M1":
    K_VALUES = {name: v / 100.0 for name, v in K_VALUES.items()}

out = {"mutation": MUT, "footings": {}}


def p(*a):
    print(*a)


# ---------------------------------------------------------------- drag average
# Run 1 used 400-node Gauss-Hermite and 200-node Gauss-Laguerre rules, whose weights overflow in numpy
# (KA1 came out nan; nbc1_run1_KA1_quadrature_overflow.out). Gauss-Legendre on a finite box is used instead.
_LG_X, _LG_W = np.polynomial.legendre.leggauss(600)


def drag_quad(v, sigma):
    """D = < |v - w| (v - w).vhat > for Maxwellian w of 1-d dispersion sigma (quadrature)."""
    t = 10.0 * _LG_X[:, None]                      # (z - v) / sigma on [-10, 10]
    wt = 10.0 * _LG_W[:, None] * np.exp(-0.5 * t * t) / math.sqrt(2.0 * math.pi)
    s = 20.0 * (_LG_X[None, :] + 1.0)              # r_perp^2 / (2 sigma^2) on [0, 40], density exp(-s)
    ws = 20.0 * _LG_W[None, :] * np.exp(-s)
    z = v + sigma * t                              # relative velocity along vhat
    f = np.sqrt(z * z + 2.0 * sigma * sigma * s) * z
    return float((wt * ws * f).sum())


def drag_closed(v, sigma):
    """Free-molecular closed form: D = v^2 C_D / 2."""
    s = v / (math.sqrt(2.0) * sigma)
    cd = (2 * s * s + 1) / (math.sqrt(math.pi) * s**3) * math.exp(-s * s) \
        + (4 * s**4 + 4 * s * s - 1) / (2 * s**4) * erf(s)
    return 0.5 * v * v * cd


# ---------------------------------------------------------------- the law's halo (units a0 = r_M = 1)
def halo(x):
    X = (math.sqrt(1 + 4 * x * x) - 1) / 2
    g = (1 + X) / x**2                    # u = g / a0
    vc2 = g * x
    j = g - math.log1p(g)                 # J in units a0^2 / (4 pi G)
    root = math.sqrt(1 + 4 * x * x)
    sig2 = 0.5 * x * j * root             # J / rho_c in units a0 r_M
    return X, g, vc2, j, root, sig2


X_T = math.sqrt(5.41 * 6.41)
J_T = halo(X_T)[3]


def n_orb_times_k(x, cut=False):
    X, g, vc2, j, root, sig2 = halo(x)
    if cut:
        sig2 = 0.5 * x * max(j - J_T, 0.0) * root
    D = drag_closed(math.sqrt(vc2), math.sqrt(sig2)) if sig2 > 0 else vc2
    return vc2 / D * root, sig2 / vc2


# ---------------------------------------------------------------- known answers
ka = {}
sig = 1.0
ka1_slow = drag_quad(0.01, sig) / ((4.0 / 3.0) * math.sqrt(8 / math.pi) * sig * 0.01)
ka1_fast = drag_quad(100.0, sig) / 100.0**2
ka["KA1"] = abs(ka1_slow - 1) < 0.01 and abs(ka1_fast - 1) < 0.01
cross = max(abs(drag_quad(v, 1.0) / drag_closed(v, 1.0) - 1) for v in (0.03, 0.1, 0.3, 1, 1.414, 3, 10, 30))
c0 = 1.0 / drag_closed(1.0, math.sqrt(0.5))            # v_c^2 / D at sigma^2 = v_c^2 / 2
ka2_a = n_orb_times_k(1e-3)[0] / c0
ka2_b = n_orb_times_k(300.0)[0] / (2 * 300.0) / c0
ka["KA2"] = abs(ka2_a - 1) < 0.01 and abs(ka2_b - 1) < 0.01
ka5 = []
for x in (0.1, 1.0, 3.0):
    h = 1e-5 * x
    dj = (halo(x + h)[3] - halo(x - h)[3]) / (2 * h)
    rhs = -2 * halo(x)[1] / (x * math.sqrt(1 + 4 * x * x))
    ka5.append(abs(dj / rhs - 1))
ka["KA5"] = max(ka5) < 1e-5

p("NBC1 (SI). kappa = 1/2 FITTED; not theory closed. Mutation:", MUT)
p(f"KA1 drag limits: slow ratio {ka1_slow:.5f}, fast ratio {ka1_fast:.5f} -> {'PASS' if ka['KA1'] else 'FAIL'}")
p(f"    quadrature vs closed form, max relative difference {cross:.2e}")
p(f"KA2 c0 = v_c^2/D at sigma^2 = v_c^2/2: {c0:.5f}; N k at x 1e-3 / c0 = {ka2_a:.5f}; "
  f"N k/(2x) at x 300 / c0 = {ka2_b:.5f} -> {'PASS' if ka['KA2'] else 'FAIL'}")
p(f"KA5 dJ/dr = -rho_c g, max relative error {max(ka5):.2e} -> {'PASS' if ka['KA5'] else 'FAIL'}")

# ---------------------------------------------------------------- recombination
OMB, SHARE, HLITTLE, OMR, T0, YHE = 0.02237, 5.41, 0.674, 4.18e-5, 2.7255, 0.245
RHO_CRIT_H2 = 1.87834e-26
H100 = 1e5 / MPC
RHO_B0 = OMB * RHO_CRIT_H2
RHO_C0 = SHARE * RHO_B0
OMM = OMB * (1 + SHARE)
OML = HLITTLE**2 - OMM - OMR
F_HE = YHE / (4 * (1 - YHE))
B1, B2, E_ALPHA, CHI_HE = 13.5984 * EV, 13.5984 * EV / 4, 13.5984 * EV * 0.75, 24.5874 * EV
LAM_ALPHA, LAM_2G = 121.5670e-9, 8.22458


def hubble(z):
    return H100 * math.sqrt(OMM * (1 + z)**3 + OMR * (1 + z)**4 + OML)


def n_h(z):
    return (1 - YHE) * RHO_B0 * (1 + z)**3 / M_H


def saha(z):
    T = T0 * (1 + z)
    pref = (2 * math.pi * M_E * KB * T / H_PLANCK**2)**1.5 / n_h(z)
    s_h = pref * math.exp(-B1 / (KB * T))
    s_he = 4 * pref * math.exp(-CHI_HE / (KB * T))
    lo, hi = 1e-30, 1 + F_HE
    for _ in range(200):
        xe = 0.5 * (lo + hi)
        f = s_h / (s_h + xe) + F_HE * s_he / (s_he + xe) - xe
        lo, hi = (xe, hi) if f > 0 else (lo, xe)
    xe = 0.5 * (lo + hi)
    return s_h / (s_h + xe), s_he / (s_he + xe)        # x_p, x_HeII


def alpha_b(T):
    t = T / 1e4
    return 1.14e-19 * 4.309 * t**-0.6166 / (1 + 0.6703 * t**0.5300)


def peebles_rhs(z, y):
    xp = min(max(y[0], 1e-12), 1.0)
    T = T0 * (1 + z)
    nh, Hz = n_h(z), hubble(z)
    al = alpha_b(T)
    beta = al * (2 * math.pi * M_E * KB * T / H_PLANCK**2)**1.5 * math.exp(-B2 / (KB * T))
    Kf = LAM_ALPHA**3 / (8 * math.pi * Hz)
    n1 = nh * (1 - xp)
    Cr = (1 + Kf * LAM_2G * n1) / (1 + Kf * (LAM_2G + beta) * n1)
    return [Cr * (xp * xp * nh * al - beta * (1 - xp) * math.exp(-E_ALPHA / (KB * T))) / (Hz * (1 + z))]


# Saha half-ionisation redshift
zlo, zhi = 1000.0, 2000.0
for _ in range(60):
    zm = 0.5 * (zlo + zhi)
    zlo, zhi = (zm, zhi) if saha(zm)[0] < 0.5 else (zlo, zm)
z_half = 0.5 * (zlo + zhi)
# start Peebles where Saha x_p = 0.99
zlo, zhi = 1000.0, 2500.0
for _ in range(60):
    zm = 0.5 * (zlo + zhi)
    zlo, zhi = (zm, zhi) if saha(zm)[0] < 0.99 else (zlo, zm)
z_start = 0.5 * (zlo + zhi)
sol = solve_ivp(peebles_rhs, (z_start, 20.0), [0.99], method="LSODA", rtol=1e-8, atol=1e-12, dense_output=True)


def x_p(z):
    return saha(z)[0] if z >= z_start else float(sol.sol(z)[0])


ka["KA4"] = (1340 <= z_half <= 1410) and (0.08 <= x_p(1100) <= 0.22) and (1e-4 <= x_p(200) <= 1e-3)
p(f"KA4 Saha half-ionised at z = {z_half:.0f}; Peebles from z = {z_start:.0f}; x_e(1100) = {x_p(1100):.4f}; "
  f"x_e(800) = {x_p(800):.5f}; x_e(200) = {x_p(200):.2e} -> {'PASS' if ka['KA4'] else 'FAIL'}")


def t_gas(z):
    return T0 * (1 + z) if z >= 150 else T0 * 151 * ((1 + z) / 151.0)**2


def v_bc(z):
    return 3.0e4 if z >= 1100 else 3.0e4 * (1 + z) / 1101.0


def neutral_flux(z, all_baryons=False):
    """sum over neutral species of rho_n * relative speed (kg m^-2 s^-1), and the neutral mass fraction."""
    T = t_gas(z)
    xp, xhe = x_p(z), saha(z)[1]
    if z < 1500:
        xhe = 0.0
    fh, fhe = ((1.0, 1.0) if all_baryons else (1 - xp, 1 - xhe))
    rho_h = fh * n_h(z) * M_H
    rho_he = fhe * F_HE * n_h(z) * 4 * M_H
    vh = math.sqrt(v_bc(z)**2 + 8 * KB * T / (math.pi * M_H))
    vhe = math.sqrt(v_bc(z)**2 + 8 * KB * T / (math.pi * 4 * M_H))
    rho_b = RHO_B0 * (1 + z)**3
    return rho_h * vh + rho_he * vhe, (rho_h + rho_he) / rho_b


Z_GRID = [2500, 2000, 1800, 1500, 1300, 1100, 1000, 900, 800, 500, 200, 100, 30]

# ---------------------------------------------------------------- per footing
R0, V0, SIG_GAS = 8.2 * KPC, 2.33e5, (0.0 if MUT == "M2" else 13.0) * MSUN_PC2
BUDGET, BUDGET_ERR = 21.0, math.hypot(4.0, 3.4)
X_GRID = np.logspace(math.log10(0.1), math.log10(3.0), 30)
nk = np.array([n_orb_times_k(x)[0] for x in X_GRID])
nk_cut = np.array([n_orb_times_k(x, cut=True)[0] for x in X_GRID])
p(f"\nK1 shape (footing-free in units of G/a0): N_orb * k on x in [0.1, 3]: min {nk.min():.4f} at x = "
  f"{X_GRID[nk.argmin()]:.2f}, max {nk.max():.4f} at x = {X_GRID[nk.argmax()]:.2f}; "
  f"with the halo cut at x_t = {X_T:.3f}: min {nk_cut.min():.4f}, max {nk_cut.max():.4f}")
p("   x      N_orb*k   sigma^2/v_c^2")
for x in (0.1, 0.3, 1.0, 2.0, 3.0):
    a, b = n_orb_times_k(x)
    p(f"   {x:4.1f}   {a:7.4f}   {b:6.4f}")
p(f"   largest k with N_orb >= 10 on the grid: {nk.min() / 10:.4f}; with N_orb >= 50: {nk.min() / 50:.5f}")
p(f"   stars: geometric opacity of the Sun pi R^2 / M = {math.pi * R_SUN**2 / MSUN:.3e} m^2/kg")

for name, a0 in FOOTINGS.items():
    fo = {"a0": a0, "k": {}}
    kap1 = G / a0
    p(f"\n[{name}] a0 = {a0:.4e} m/s^2; G/a0 = {kap1:.4f} m^2/kg = {kap1 * 10:.2f} cm^2/g")
    # KA3 (MEDIUM_DESIGN): all baryons, k = pi, 30 km/s, z 1100
    ka3 = math.pi * kap1 * RHO_B0 * 1101**3 * 3.0e4 / hubble(1100)
    target = {"canonical": 0.73, "alt": 0.61}[name]
    ka3_ok = abs(ka3 / target - 1) < 0.03
    p(f"  KA3 all-baryon drag / H at z 1100, k = pi, 30 km/s: {ka3:.3f} (MEDIUM_DESIGN {target}) -> "
      f"{'PASS' if ka3_ok else 'FAIL'}")
    # local numbers
    g = V0**2 / R0
    g_c = a0 * g / (g + a0)
    sig_flat = g_c / (2 * math.pi * G) / MSUN_PC2
    rho_c = g_c * (2 - a0 / (g + a0)) / (4 * math.pi * G * R0)
    sig_round = rho_c * 2.2 * KPC / MSUN_PC2
    ka6_ok = 10 <= sig_round <= 30
    t_orb = 2 * math.pi * R0 / V0
    p(f"  Sun: g = {g:.3e}, g_c = {g_c:.3e} m/s^2, rho_c = {rho_c:.3e} kg/m^3 = {rho_c / MSUN * PC**3:.4f} Msun/pc^3, "
      f"T_orb = {t_orb / GYR:.3f} Gyr")
    p(f"  KA6 round-halo column inside 1.1 kpc: {sig_round:.1f} Msun/pc^2 -> {'PASS' if ka6_ok else 'FAIL'}; "
      f"rotation-supported layer for the same g_c: {sig_flat:.1f} Msun/pc^2; budget {BUDGET:.0f} +- {BUDGET_ERR:.1f}")
    ka_all = all(ka.values()) and ka3_ok and ka6_ok
    fo["KA"] = {**ka, "KA3": ka3_ok, "KA6": ka6_ok, "all": ka_all}
    verdicts = []
    for kname, k in K_VALUES.items():
        kap = k * kap1
        r = {"kappa_m2_kg": kap}
        # K1
        n = nk / k
        tau_gas = {s: kap * s * MSUN_PC2 for s in (5, 10, 13)}
        thin = max(tau_gas.values()) < 1
        k1 = "NO VERDICT" if not thin else ("FAIL" if n.min() < 10 else ("PASS" if n.min() >= 50 else "NO VERDICT"))
        # K2
        n_sc = kap * SIG_GAS * 2 * 10 * GYR / t_orb
        s = 1 - math.exp(-n_sc)
        sig_h = s * sig_flat + (1 - s) * sig_round
        k2 = "FAIL" if sig_h > BUDGET + 3 * BUDGET_ERR else ("PASS" if sig_h <= BUDGET + BUDGET_ERR else "NO VERDICT")
        # K3
        rows = []
        for z in Z_GRID:
            flux, fn = neutral_flux(z, all_baryons=(MUT == "M3"))
            Hz = hubble(z)
            rows.append((z, fn, kap * flux / Hz, kap * RHO_C0 * (1 + z)**3 * flux / (RHO_B0 * (1 + z)**3) / Hz))
        gc_max = max(row[2] for row in rows if row[0] >= 900)
        k3 = "PASS (by hand)" if gc_max < 1e-3 else ("FAIL (by hand)" if gc_max > 1 else "NOT DECIDED BY HAND")
        # K4
        k4 = {col: kap * col * 10 for col in (0.006, 0.0181, 0.0302)}     # g/cm^2 -> kg/m^2 is x10
        # K5
        heat = kap * rho_c * drag_closed(V0, V0 / math.sqrt(2)) * V0 * 1.4 * M_H * 1e7     # erg/s per H
        r5 = heat / 2.65e-26
        # verdict
        if not ka_all:
            v = "NO VERDICT (known answer failed)"
        elif (k1 == "FAIL" and k2 == "FAIL") or k3.startswith("FAIL"):
            v = "KILLED" + (" (K2 PROVISIONAL)" if not k3.startswith("FAIL") else "")
        elif (k1 == "PASS" or k2 == "PASS") and not k3.startswith("FAIL"):
            v = "SURVIVES THE HAND TESTS"
        else:
            v = "NO VERDICT"
        verdicts.append(v)
        p(f"  k = {kname:>3} ({k:.4f}): kappa_c = {kap:.4f} m^2/kg = {kap * 10:.2f} cm^2/g")
        p(f"    K1 {k1}: N_orb min {n.min():.3f}, max {n.max():.3f} on x in [0.1, 3]; gas-layer optical depth "
          f"{tau_gas[5]:.3f} / {tau_gas[10]:.3f} / {tau_gas[13]:.3f} at 5 / 10 / 13 Msun/pc^2")
        p(f"    K2 {k2} (PROVISIONAL inputs): N_sc = {n_sc:.2f} in 10 Gyr, settled fraction {s:.3f}, dark column "
          f"{sig_h:.1f} Msun/pc^2 against {BUDGET:.0f} +- {BUDGET_ERR:.1f} (fail above {BUDGET + 3 * BUDGET_ERR:.1f})")
        p(f"    K3 {k3}: max G_c at z >= 900 = {gc_max:.3e}")
        p("       z     neutral mass fraction   G_c = cold drag / H   G_b = baryon drag / H")
        for z, fn, gc, gb in rows:
            p(f"       {z:5d}   {fn:10.3e}              {gc:10.3e}            {gb:10.3e}")
        p(f"    K4 (not a test): optical depth of a FULLY NEUTRAL column 0.006 / 0.0181 / 0.0302 g/cm^2: "
          f"{k4[0.006]:.3f} / {k4[0.0181]:.3f} / {k4[0.0302]:.3f}; the Bullet's gas is ionised, so none")
        p(f"    K5 (reported): dissipation {heat:.2e} erg/s per H nucleus = {r5:.1f} x the [C II] cooling 2.65e-26 "
          f"(PROVISIONAL)")
        p(f"    => {v}")
        r.update({"K1": k1, "N_orb_min": float(n.min()), "N_orb_max": float(n.max()), "K2": k2, "N_sc": n_sc,
                  "dark_column": sig_h, "K3": k3, "Gc_max_z900": gc_max, "K5_ratio": r5, "verdict": v,
                  "K3_rows": rows})
        fo["k"][kname] = r
    if all(v.startswith("KILLED") for v in verdicts):
        label = "KILLED (K2 PROVISIONAL)" if any("PROVISIONAL" in v for v in verdicts) else "KILLED"
    elif any(v.startswith("SURVIVES") for v in verdicts):
        label = "SURVIVES THE HAND TESTS"
    else:
        label = "NO VERDICT"
    fo["label"] = label
    p(f"  LANE LABEL [{name}]: {label}")
    out["footings"][name] = fo

fn_json = "nbc1.json" if MUT is None else f"nbc1_MUT_{MUT}.json"
with open(__file__.rsplit("/", 1)[0] + "/" + fn_json, "w") as fh:
    json.dump(out, fh, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
p("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
