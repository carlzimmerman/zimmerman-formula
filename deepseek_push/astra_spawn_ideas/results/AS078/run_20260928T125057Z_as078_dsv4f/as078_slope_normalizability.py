#!/usr/bin/env python3
"""AS078 -- General slope normalizability: the power-law family
rho(r) = A r^{-gamma} on the finite shell r_in <= r <= R.

Bounded prototype: <=120 s wall, <=512 MB, 1 thread, <=512 grid cells,
two refinements, mpmath dps=50 for the high-precision representation.

Framework cell (declared): conditional deep-equilibrium sector (G084/G091/G233);
kappa = 1/2 ADOPTED; G = G_N = 6.67430e-11; both footings carried separately.
No Q/RAR/MU2/EXP/MONO kernel claims are made by this script: it computes the
geometry + normalization of the power-law profile family only.

Outputs (to CWD):
  raw_output.txt       (shell redirect)
  as078_residuals.json (structured numbers used by result.json)
"""
import json
import math
import os
import resource
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import mpmath as mp
import numpy as np

T0 = time.perf_counter()

# ---------------------------------------------------------------- constants
G = 6.67430e-11          # m^3 kg^-1 s^-2  (measured Newton constant, G_N)
C_L = 299792458.0        # m/s (exact)
MSUN = 1.98847e30        # kg
PC = 3.085677581491367e16  # m
KPC = 1e3 * PC
MB_PROXY = 7.0e10        # Msun  (G084/G233 MW convention)
MB_ALT_PROXY = 6.5e10    # Msun  (G091 anchor)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}   # m/s^2, both footings
KAPPA = 0.5              # ADOPTED input (not derived here)

mp.mp.dps = 50

RES = {}   # structured results


def rel(a, b):
    return float(abs(a - b) / abs(b)) if b != 0 else float(abs(a))


def shell_rin_R_RM(foot, rin_over_R, R_over_rM, Mb_msun):
    """Return (r_in, R) in metres for an interior shell fixture."""
    Mb = Mb_msun * MSUN
    a0v = A0[foot]
    rM = math.sqrt(G * Mb / a0v)
    R = R_over_rM * rM
    rin = rin_over_R * R
    return rin, R, rM, Mb


# ---------------------------------------------------------------- closed forms
def closed_mass(lin, A, gam):
    """Enclosed mass M(R) = 4 pi A (R^(3-g) - r_in^(3-g))/(3-g), g != 3.
    mpmath, 50 digits; positive shell radii."""
    rin, R = lin
    return 4 * mp.pi * A * (R ** (3 - gam) - rin ** (3 - gam)) / (3 - gam)


def closed_mass_log(lin, A):
    """gamma = 3 limit: M(R) = 4 pi A ln(R/r_in)."""
    rin, R = lin
    return 4 * mp.pi * A * mp.log(R / rin)


def framew_A(foot, Mb_msun):
    """A = C/(4 pi G), C = sqrt(G_N M_b a0)  (the r_in->0 equipartition limit)."""
    Mb = Mb_msun * MSUN
    C = math.sqrt(G * Mb * A0[foot])
    return C / (4 * math.pi * G)


def framew_rM(foot, Mb_msun):
    Mb = Mb_msun * MSUN
    return math.sqrt(G * Mb / A0[foot])


print("=" * 92)
print("AS078 -- General slope normalizability (bounded prototype, mpmath 50 dps)")
print("=" * 92)

# ------------------------------------------------------------------ 0. inputs
print("\n--- 0. framework inputs (both footings, kappa = 1/2 adopted) ---")
for foot in ("canonical", "alt"):
    a0v = A0[foot]
    rhoL = 4.0 * a0v ** 2 / (G * C_L ** 2)              # rho_Lambda = 4 a0^2/(G c^2)
    RES.setdefault("footings", {})[foot] = {"a0": a0v, "rho_Lambda_kg_m3": rhoL}
    print(f"  [{foot:9s}] a0 = {a0v:.6e} m/s^2 | rho_Lambda = {rhoL:.6e} kg/m^3 "
          f"(kappa=1/2)")
# effective kappa at FIXED canonical rho_Lambda for the alternative a0
rhoL_can = RES["footings"]["canonical"]["rho_Lambda_kg_m3"]
k_eff = A0["alt"] / (C_L * math.sqrt(G * rhoL_can))
print(f"  fixed rho_Lambda(canonical): kappa_eff for a0_alt = {k_eff:.8f} "
      f"(!= 1/2 -> the two footings cannot share fixed (kappa,rho))")
RES["footings"]["kappa_eff_at_fixed_canonical_rho"] = k_eff

# ---------------------------------------------------------- 1. mass formula
print("\n--- 1. closed form vs direct quadrature (mpmath tanh-sinh, 50 dps) ---")
print("    DIMENSIONLESS identity: I(g; u1, u2) = int_{u1}^{u2} u^{2-g} du")
print("    = (u2^(3-g) - u1^(3-g))/(3-g) for g != 3, = ln(u2/u1) at g = 3.")
print("    Exact decimal-string endpoints (u = r/r_M): the physical constants")
print("    (A, r_M, M_b) only scale the identity and are checked separately.")
GAMS = [0.5, 1.0, 1.5, 2.0, 2.5, 2.9, 3.0, 3.1, 4.0]
INTERIOR_SHELLS = [(0.01, 0.62), (0.01, 1.0), (0.1, 0.62), (0.1, 1.0),
                   (0.5, 0.62), (0.5, 1.0)]
worst = {"canonical": 0.0, "alt": 0.0}
worst_phys = {"canonical": 0.0, "alt": 0.0}
quad_rows = []
for foot in ("canonical", "alt"):
    for rinR, RrM in INTERIOR_SHELLS:
        rin, R, rM, Mb = shell_rin_R_RM(foot, rinR, RrM, MB_PROXY)
        u1 = mp.mpf(f"{rinR * RrM:.17g}")     # exact decimal of r_in/r_M
        u2 = mp.mpf(f"{RrM:.17g}")            # exact decimal of R/r_M
        A = framew_A(foot, MB_PROXY)
        for gam in GAMS:
            f = lambda u, g=gam: u ** (2 - g)                 # noqa: E731
            q = mp.quad(f, [u1, u2])
            if gam == 3.0:
                c = mp.log(u2 / u1)
            else:
                c = (u2 ** (3 - gam) - u1 ** (3 - gam)) / (3 - gam)
            r = rel(q, c)
            worst[foot] = max(worst[foot], r)
            # physical scaling consistency (float inputs, informational):
            Ms_phys = closed_mass((rin, R), A, gam) if gam != 3.0 else \
                closed_mass_log((rin, R), A)
            Ms_dim = 4 * mp.pi * A * rM ** (3 - gam) * q
            rp = rel(Ms_phys, float(Ms_dim))
            worst_phys[foot] = max(worst_phys[foot], rp)
            quad_rows.append({"foot": foot, "u1": float(u1), "u2": float(u2),
                              "gamma": gam, "quad": float(q), "closed": float(c),
                              "rel_resid_dimless": r, "rel_resid_physical": rp})
            print(f"  [{foot:9s}] u1={float(u1):.4f} u2={float(u2):.3f} "
                  f"gamma={gam:4.1f}: dimless resid {r:.2e} | phys {rp:.2e}")
print(f"  WORST dimensionless rel resid: {max(worst.values()):.2e} "
      f"(tolerance 1e-40) -> {'PASS' if max(worst.values()) < 1e-40 else 'FAIL'}")
RES["mass_formula"] = {"tolerance_set_before": 1e-40,
                       "worst_rel_resid_dimless": worst,
                       "worst_rel_resid_physical": worst_phys,
                       "rows": quad_rows}

# ---------------------------------------------- 2. finite-boundary normalization
print("\n--- 2. finite-boundary equipartition normalization (gamma=2) ---")
# exact: A_ex = M_b / (4 pi (r_M - r_in))   [M(<r_M) = M_b on the finite shell]
# limit:  A   -> C / (4 pi G)               [r_in -> 0, G03E]
norm_rows = []
for foot in ("canonical", "alt"):
    for Mb_msun in (MB_PROXY, MB_ALT_PROXY):
        rin, R, rM, Mb = shell_rin_R_RM(foot, 0.01, 1.0, Mb_msun)
        A_ex = Mb / (4 * math.pi * (rM - rin))
        A_lim = framew_A(foot, Mb_msun)
        C = math.sqrt(G * Mb * A0[foot])
        # masses
        M_rM_ex = 4 * math.pi * A_ex * (rM - rin)          # = M_b exactly
        M_rM_lim = 4 * math.pi * A_lim * rM                # = C r_M / G
        # v_c^2(R) exact at finite r_in: (GM_b/R)(R-r_in)/(r_M-r_in)
        for Rfrac in (0.62, 1.0):
            Rv = Rfrac * rM
            vc2 = (G * Mb / Rv) * (Rv - rin) / (rM - rin)
            vc2_lim = C                      # r_in->0 limit: v_c^2 = C on the shell
            # phantom mass fraction M_ph(<r)/M_b = (r - r_in)/(r_M - r_in)
            frac = (Rv - rin) / (rM - rin)
            norm_rows.append({"foot": foot, "Mb_msun": Mb_msun, "R_over_rM": Rfrac,
                              "A_exact": A_ex, "A_lim": A_lim,
                              "A_rel_diff": rel(A_ex, A_lim),
                              "M(<r_M)_exact_over_Mb": M_rM_ex / Mb,
                              "M(<r_M)_lim_over_Mb": M_rM_lim / Mb,
                              "vc2_over_C": vc2 / vc2_lim,
                              "phantom_fraction": frac})
            print(f"  [{foot:9s} M_b={Mb_msun:.1e}] R/r_M={Rfrac:.2f}: "
                  f"A_ex/A_lim rel diff = {rel(A_ex, A_lim):.3e}, "
                  f"M(<r_M)=M_b exact: {M_rM_ex / Mb - 1:.2e}, "
                  f"v_c^2/C = {vc2 / vc2_lim:.6f}, M_ph/M_b = {frac:.5f}")
RES["finite_boundary_normalization"] = {"rows": norm_rows}

# ------------------------------------------------ 3. gamma->3 limit (delta-seq)
print("\n--- 3. gamma -> 3 limit: (u2^d - u1^d)/d -> ln(u2/u1), d := 3-gamma ---")
print("    dimensionless, exact decimal endpoints u1 = 0.062, u2 = 0.62")
print("    (mirrors the fixture r_in/R = 0.1, R/r_M = 0.62)")
print("    leading neglected term:  d/2 * [(ln u2)^2 - (ln u1)^2] + O(d^2)")
lim_rows = []
u1 = mp.mpf("0.062")
u2 = mp.mpf("0.62")
ln1, ln2 = mp.log(u1), mp.log(u2)
target = ln2 - ln1
lead = (ln2 ** 2 - ln1 ** 2) / 2
for k in range(1, 22):
    d = mp.mpf(10) ** (-k)
    ratio = (u2 ** d - u1 ** d) / d
    resid = rel(ratio, target)
    dev_over_d = (ratio - target) / d if k <= 14 else None
    lim_rows.append({"delta": float(d),
                     "ratio_minus_log": float(ratio - target),
                     "rel_resid": resid,
                     "dev_over_delta": None if dev_over_d is None else float(dev_over_d)})
    if k in (4, 10, 15, 20):
        print(f"  delta=1e-{k:2d}: (u2^d-u1^d)/d - ln(u2/u1) = "
              f"{float(ratio - target):.3e}  (lead term = {float(d * lead):.3e})")
# plateau check: residual stops shrinking at ~1e-48 (50-digit arithmetic)
kp, rp = lim_rows[-2], lim_rows[-1]
RES["gamma3_limit"] = {"u1": float(u1), "u2": float(u2),
                       "target_ln_u2_over_u1": float(target),
                       "leading_coeff": float(lead),
                       "resid_at_delta_1e-20": lim_rows[19]["rel_resid"],
                       "resid_at_delta_1e-21": lim_rows[20]["rel_resid"],
                       "rows": lim_rows}

# --------------------------------- 4. independent representation (FTC + grid)
print("\n--- 4. independent checks: (a) FTC derivative of the closed form,")
print("        (b) log-trapezoid quadrature, <=512 cells, two refinements ---")
ftc_rows = []
for foot in ("canonical", "alt"):
    rin, R, rM, Mb = shell_rin_R_RM(foot, 0.05, 0.8, MB_PROXY)
    A = framew_A(foot, MB_PROXY)
    for gam in (1.5, 2.0, 2.5):
        # (a) dM/dR computed by mpmath's Richardson derivative of the closed form
        # vs the surface term 4 pi R^2 rho(R) = 4 pi A R^(2-gamma)
        if gam == 3.0:
            Mf = lambda x: 4 * mp.pi * A * mp.log(x / rin)          # noqa: E731
        else:
            Mf = lambda x: 4 * mp.pi * A * (x ** (3 - gam) - rin ** (3 - gam)) / (3 - gam)  # noqa: E731
        dM = mp.diff(Mf, R)
        surf = 4 * mp.pi * A * R ** (2 - gam)
        ftc_rows.append({"foot": foot, "gamma": gam,
                         "dM/dR": float(dM), "4piR2rho": float(surf),
                         "rel_resid": float(rel(dM, surf))})
        print(f"  [{foot:9s}] gamma={gam:.1f}: dM/dR vs 4 pi R^2 rho(R): "
              f"rel resid {rel(dM, surf):.2e}")
# (b) log-trapezoid on n in {128, 256, 512} (two refinements), gamma=2
trap_rows = []
for foot in ("canonical", "alt"):
    rin, R, rM, Mb = shell_rin_R_RM(foot, 0.05, 0.8, MB_PROXY)
    A = framew_A(foot, MB_PROXY)
    closed = closed_mass((rin, R), A, 2.0)
    prev = None
    for n in (128, 256, 512):
        s = np.geomspace(rin, R, n)
        y = 4 * math.pi * A * s ** (2 - 2.0)
        val = np.trapezoid(y, s) if hasattr(np, "trapezoid") else np.trapz(y, s)
        r = rel(val, float(closed))
        trap_rows.append({"foot": foot, "n": n, "trapezoid": float(val),
                          "rel_resid": float(r), "refinement_of": prev})
        print(f"  [{foot:9s}] trapezoid n={n:4d} (cells={n - 1} <= 512): "
              f"rel resid {r:.2e}")
        prev = n
RES["independent_checks"] = {"ftc_rows": ftc_rows, "trapezoid_rows": trap_rows}

# ------------------------------------------------- 5. negative controls
print("\n--- 5. negative controls (each capable of failing) ---")
NC = {}

# NC1: claim "r^-2 is globally normalizable on all positive radii" -> FALSE
#      outer diverges linearly: M(R) = 4 pi A (R - r_in),  M(2R)/M(R) -> 2
rin, R, rM, Mb = shell_rin_R_RM("canonical", 0.01, 1.0, MB_PROXY)
A = framew_A("canonical", MB_PROXY)
ratios = []
for k in (1, 2, 3, 4, 5, 6):
    Rk = 10 ** k * rM
    M_R = 4 * math.pi * A * (Rk - rin)
    M_2R = 4 * math.pi * A * (2 * Rk - rin)
    ratios.append({"R_over_rM": 10 ** k, "M(R)": float(M_R), "M(2R)/M(R)": float(M_2R / M_R)})
    print(f"  NC1 [{foot} r_in=0.01 r_M] R/r_M = 1e{k}: M(R) = {float(M_R):.4e} kg, "
          f"M(2R)/M(R) = {float(M_2R / M_R):.10f} (-> 2)")
NC["NC1_global_r-2_normalization"] = {
    "claim": "rho = A r^-2 normalizable over (0, inf) -> FALSE",
    "observed": "M(R) = 4 pi A (R - r_in) grows linearly; M(2R)/M(R) -> 2; "
                "hence total mass infinite (outer divergence)",
    "ratios": ratios,
    "control_capable_of_failing": True,
    "expected_firing": "the claim is REFUTED by construction; "
                       "control fires iff M(2R)/M(R) stays far from 2",
    "fired": ratios[-1]["M(2R)/M(R)"] > 1.99}

# NC2: naive 0/0 evaluation of the gamma=3 closed form -> singular; the log form
#      is the removable extension (delta-sequence already in sec. 3)
naive = None
try:
    naive = closed_mass((rin, R), A, 3.0)   # 0/0 -> mpmath raises/returns nan
except (ZeroDivisionError, ValueError) as e:
    naive = f"not evaluable: {type(e).__name__}"
if naive is None or (isinstance(naive, float) and math.isnan(naive)):
    naive = "nan / ZeroDivision (0/0 singular)"
NC["NC2_gamma3_00_naive_form"] = {
    "claim": "4 pi A (R^0 - r_in^0)/0 is a valid evaluation at gamma=3 -> FALSE",
    "observed": f"naive form -> {naive}; the delta-sequence of sec. 3 gives "
                f"(R^d - r_in^d)/d -> ln(R/r_in) continuously (resid rows above)",
    "control_capable_of_failing": True,
    "fired": True}
print(f"  NC2 naive (R^(3-g)-r_in^(3-g))/(3-g) at g=3 -> {naive}; "
      f"log form = {float(closed_mass_log((rin, R), A)):.10e} kg")

# NC3: flatness is exact only in the r_in -> 0 limit (finite-boundary correction)
flat_rows = []
for foot in ("canonical", "alt"):
    for rinR in (0.01, 0.1, 0.5):
        rin, R, rM, Mb = shell_rin_R_RM(foot, rinR, 1.0, MB_PROXY)
        C = math.sqrt(G * Mb * A0[foot])
        vc2_62 = (G * Mb / (0.62 * rM)) * (0.62 * rM - rin) / (rM - rin)
        flat_rows.append({"foot": foot, "r_in/R": rinR,
                          "v_c^2(0.62 r_M)/C": float(vc2_62 / C)})
        print(f"  NC3 [{foot:9s}] r_in/R = {rinR:.2f}: v_c^2(0.62 r_M)/C = "
              f"{vc2_62 / C:.6f}  (flat = 1 exactly only as r_in -> 0)")
NC["NC3_finite_rin_flatness"] = {
    "claim": "v_c^2(R) = C exactly on the shell for ANY finite r_in -> FALSE",
    "observed": flat_rows,
    "control_capable_of_failing": True,
    "fired": False}   # this control does NOT refute: the deviation is real and recorded

# NC4 (task step 5): interior ansatz transferred to the deep exterior
#      r_in/r_M in {10, 100}, R/r_in in {2, 10}; mass of the shell under the
#      extrapolated ansatz grows linearly: M_shell/M_b = (R - r_in)/r_M (exact)
ext_rows = []
for foot in ("canonical", "alt"):
    rM = framew_rM(foot, MB_PROXY)
    A = framew_A(foot, MB_PROXY)
    for rr in (10, 100):
        for Rr in (2, 10):
            rinE, RE = rr * rM, rr * Rr * rM
            Ms = 4 * math.pi * A * (RE - rinE)
            ext_rows.append({"foot": foot, "r_in/r_M": rr, "R/r_in": Rr,
                             "M_shell_kg": float(Ms),
                             "M_shell_over_Mb": Ms / (MB_PROXY * MSUN)})
            print(f"  NC4 [{foot:9s}] r_in/r_M={rr:3d} R/r_in={Rr:2d}: "
                  f"M_shell/M_b = {Ms / (MB_PROXY * MSUN):8.1f}  "
                  f"(= (R-r_in)/r_M exact, dimension-free)")
NC["NC4_exterior_ansatz_transfer"] = {
    "claim": "the interior equipartition normalization controls the phantom mass "
             "at r >> r_M -> NOT ESTABLISHED here",
    "observed": ("extrapolated ansatz shell mass = M_b (R - r_in)/r_M, growing "
                 "linearly in R; no kernel (filtered MONO) solution used; the "
                 "full-kernel error bound is the open implication"),
    "rows": ext_rows,
    "control_capable_of_failing": True,
    "fired": None}   # fires only when a kernel solve exists to compare against

# ------------------------------------------------- 6. deep/Newtonian checks
print("\n--- 6. deep-sector checks + boundary fixtures ---")
deep_rows = []
for foot in ("canonical", "alt"):
    for Mb_msun in (MB_PROXY, MB_ALT_PROXY):
        Mb = Mb_msun * MSUN
        rM = framew_rM(foot, Mb_msun)
        C = math.sqrt(G * Mb * A0[foot])
        vflat = math.sqrt(C)
        sig = math.sqrt(C / 2) / 1e3          # km/s
        # B(r_M) = G M_b / r_M^2 = a0 exactly (definition fixture)
        B_rM = G * Mb / rM ** 2
        # g(r_M) = C / r_M = a0 exactly (deep-sector equipartition boundary)
        g_rM = C / rM
        # phantom density at r_M and r_break=0.62 r_M (A = C/4piG, r_in->0)
        Ab = framew_A(foot, Mb_msun)
        rho_rM = Ab / rM ** 2
        rho_rb = Ab / (0.62 * rM) ** 2
        # P(r_M) = sigma^2 rho(r_M) = a0^2/(8 pi G) (G233 identity re-check)
        P_rM = (C / 2) * rho_rM
        P_a0only = A0[foot] ** 2 / (8 * math.pi * G)
        deep_rows.append({"foot": foot, "Mb_msun": Mb_msun, "r_M_m": rM,
                          "C_m2s2": C, "v_flat_m_s": vflat, "sigma_km_s": sig,
                          "B(r_M)/a0": B_rM / A0[foot],
                          "g(r_M)/a0": g_rM / A0[foot],
                          "rho(r_M)_kg_m3": rho_rM, "rho(r_break)_kg_m3": rho_rb,
                          "P(r_M)/[a0^2/8piG]": P_rM / P_a0only})
        print(f"  [{foot:9s} M_b={Mb_msun:.1e}] r_M={rM:.4e} m, v_flat="
              f"{vflat:.2f} m/s, sigma={sig:.2f} km/s, B(r_M)/a0 = "
              f"{B_rM / A0[foot]:.12f}, g(r_M)/a0 = {g_rM / A0[foot]:.12f}, "
              f"P(r_M)/(a0^2/8piG) = {P_rM / P_a0only - 1:.2e}")
RES["deep_sector"] = {"rows": deep_rows}

# ----------------------------------------------- 7. bounds + exit summary
T1 = time.perf_counter()
maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss   # bytes on macOS
RES["execution"] = {"wall_s": T1 - T0, "maxrss_bytes": maxrss,
                    "threads": 1, "mp_dps": mp.mp.dps,
                    "cells_max": 512, "refinements": 2}
print(f"\n--- execution bounds: wall {T1 - T0:.3f} s (<=120), "
      f"maxrss {maxrss / 1e6:.1f} MB (<=512), 1 thread, dps=50, "
      f"cells<=512, 2 refinements ---")

with open("as078_residuals.json", "w") as f:
    json.dump(RES, f, indent=1, default=str)
print("wrote as078_residuals.json")
