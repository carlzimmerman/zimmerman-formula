#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
a24_checks.py -- Lane A24: the wide-binary contradiction (Arm A 1.1614-1.1814 vs
the October record's gamma_v = 1.20 @10 kAU / 1.51 @20 kAU).

What this script decides
------------------------
(1) It computes, from the frozen law g_N = g^2/(g+a0) with NO external field, the
    isolated wide-binary velocity boost at 10 and 20 kAU for a 1+1 Msun pair, on
    both footings, in the total-mass composition and in the exact two-body
    composition obtained by direct quadrature of the QUMOND phantom source.
(2) It imposes a Galactic external field (1.8 a0 observed; and the repo's own
    closed-loop value 1.8996 a0) inside the same law and re-computes the boost,
    then compares the size of the EFE effect with the size of the solver fork
    (QUMOND vs AQUAL) that the repo already measured.
(3) It reproduces the October record's 1.20 / 1.51 exactly, which identifies
    the recipe that produced them (quadrature law, 1.5 Msun, total mass, NO EFE).
(4) It computes the decisive measurement: the pair count and separation bin at
    which the two candidate predictions separate at 4.2 sigma_tot.

Deterministic, no network.  Usage:
    python3 a24_checks.py            # normal run, exit 0 iff every check passes
    python3 a24_checks.py --mutate   # one mutation that MUST break a check
"""

import json
import sys

import numpy as np

MUTATE = "--mutate" in sys.argv

# ------------------------------------------------------------------------------
# Constants.  Every one is either from the push BRIEF (B) or a labelled external
# input with its source (S).
# ------------------------------------------------------------------------------
C_LIGHT = 2.99792458e8        # B
G_N = 6.67430e-11             # B
MSUN = 1.98892e30             # S: IAU nominal solar mass (GM_sun/G)
KAU = 1.495978707e14          # S: 1 kAU = 1000 AU, AU = 1.495978707e11 m
PC = 3.0856775814913673e16    # B
A0_CAN = 9.36e-11             # B
A0_ALT = 1.13e-10             # B

# Registered arms and scoring constants (PREREGISTRATION_DR4.md Amd 10, and
# CFG943 section 1: sigma_fit = 0.019 sqrt(30000/N), sigma_sys = 0.020).
ARM_A_LO, ARM_A_HI = 1.1614, 1.1814
ARM_A_ALT_LO, ARM_A_ALT_HI = 1.1917, 1.2267
GUARD_ZONE = 1.23             # > 1.23 = no verdict for any arm (Amd 10(d), CFG943)
NO_EFE_BENCH = 1.33           # "the unchanged no-EFE/full-MOND benchmark" (Amd 10(d))
N_FROZEN = 30000              # frozen DR4 pair count (prereg section 1.5)
SIG_FIT_30K = 0.019           # prereg section 1.5
SIG_SYS = 0.020               # prereg section 1.5, irreducible
SIG_TOT_30K = float(np.hypot(SIG_FIT_30K, SIG_SYS))       # 0.0276
FORECAST_SIGMA = 4.2          # the repo's own arm-to-arm forecast: 0.116 = 4.2 sig_tot

# External field.  Two numbers, both labelled:
#  * 1.8 a0 -- the standard local value named in the task, as an OBSERVED
#    (MOND) acceleration; its Newtonian counterpart follows from the closure
#    x = y nu(y) below.
#  * 1.8996 a0 -- the repo's own closed-loop x_ext (canonical) used by the
#    registered AQUAL solve (aqual_efe_full_solve_2026.py, line 45).
XEXT_STD = 1.8
XEXT_REPO_CAN = 1.8996
XEXT_REPO_ALT = 1.5764

# The October record's own numbers (Zenodo 23251278, quoted in PAPER44
# qwen_claude_field_theory/papers_2026/PAPER44_efe_blind_mond_2026.tex line 29/59).
PAPER44 = {2.0: 1.01, 5.0: 1.06, 10.0: 1.20, 20.0: 1.51}

CHECKS = []


def check(cid, ok, value, threshold, detail=""):
    CHECKS.append({"id": cid, "pass": bool(ok), "value": value, "threshold": threshold})
    label = "PASS" if ok else "FAIL"
    print(f"{cid} {label} {value} {threshold}" + (f"   [{detail}]" if detail else ""))


def info(msg):
    print(f"      {msg}")


# ------------------------------------------------------------------------------
# The laws
# ------------------------------------------------------------------------------
def nu_can(y):
    """Canonical law g_N = g^2/(g+a0) inverted: nu(y) = (1+sqrt(1+4/y))/2,
    y = g_N/a0 (BRIEF section 1)."""
    y = np.asarray(y, dtype=float)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))


def dnu_can(y):
    y = np.asarray(y, dtype=float)
    return -1.0 / (y * y * np.sqrt(1.0 + 4.0 / y))


def nu_quad(y):
    """n=2 'a0-line' half-capacity variant g^2 - g_N^2 = a0 g_N: nu = sqrt(1+1/y).
    This is the law PAPER44 tests and the one that produced 1.20/1.51."""
    y = np.asarray(y, dtype=float)
    return np.sqrt(1.0 + 1.0 / y)


def nu_rar(y):
    """Route-A / RAR kernel nu = 1/(1-exp(-sqrt y)) -- the kernel the registered
    AQUAL solve and the frozen pipeline actually use (kernel conflict, A5 tension 1)."""
    y = np.asarray(y, dtype=float)
    s = np.sqrt(np.maximum(y, 1e-300))
    return 1.0 / (1.0 - np.exp(-s))


def dnu_rar(y):
    y = np.asarray(y, dtype=float)
    s = np.sqrt(np.maximum(y, 1e-300))
    u = 1.0 - np.exp(-s)
    return -(np.exp(-s) / (2.0 * s)) / u ** 2


def y_of_x(x, nu=nu_can):
    """Invert the closure x = y*nu(y) (observed field -> Newtonian field)."""
    from scipy.optimize import brentq
    f = lambda ly: np.exp(ly) * float(nu(np.exp(ly))) - x
    return float(np.exp(brentq(f, np.log(1e-8), np.log(1e8), xtol=1e-14, rtol=1e-15)))


def y_tot_of(Mtot_msun, s_kau, a0):
    return G_N * Mtot_msun * MSUN / (s_kau * KAU) ** 2 / a0


# ------------------------------------------------------------------------------
# Exact two-body composition by direct quadrature of the QUMOND phantom source.
#
#   lap Phi_N = 4 pi G rho                       (baryonic)
#   lap Phi   = div[ nu(|grad Phi_N|/a0) grad Phi_N ]
#   => g = g_N + g_ph,
#      g_ph(r) = -(1/4pi) Int d3x' div'[(nu-1) g_N](x') (r-x')/|r-x'|^3
#   and, with S = -nu'(y) (grad|g_N| . g_N),
#      a_ph,z(z*) = -(1/2) Int Int S(rho,z) (z*-z) rho / [rho^2+(z*-z)^2]^{3/2} drho dz
#   (axisymmetric: the two stars sit on the z axis; the external field, when
#    present, is along +z, i.e. theta = 0 relative to the separation).
#
#   a_rel = G M_tot/r0^2 + [a_ph,z(z1) - a_ph,z(z2)];  gamma_v = sqrt(a_rel/a_N).
# ------------------------------------------------------------------------------
def two_body(y_tot, q=1.0, y_ext=0.0, nu=nu_rar, dnu=dnu_rar, nrho=480, nz=960,
             rmin_fac=1e-3, y_cap=None):
    Mt = 1.0
    M1, M2 = Mt / (1.0 + q), q * Mt / (1.0 + q)
    r0 = np.sqrt(Mt / y_tot)
    z1, z2 = -r0 / 2.0, r0 / 2.0
    rmax = 3.0e3 * max(r0, 1.0)
    rho = np.logspace(np.log10(rmin_fac * r0), np.log10(rmax), nrho)
    zp = np.logspace(np.log10(rmin_fac * r0), np.log10(rmax), nz // 2)
    z = np.concatenate([-zp[::-1], zp])
    RHO, Z = np.meshgrid(rho, z, indexing="ij")
    d1r, d1z = RHO, Z - z1
    d2r, d2z = RHO, Z - z2
    s1 = np.sqrt(d1r ** 2 + d1z ** 2)
    s2 = np.sqrt(d2r ** 2 + d2z ** 2)
    gr = -(M1 * d1r / s1 ** 3 + M2 * d2r / s2 ** 3)
    gz = -(M1 * d1z / s1 ** 3 + M2 * d2z / s2 ** 3) + y_ext
    gm = np.hypot(gr, gz)
    if y_cap is not None:
        gm = np.minimum(gm, y_cap)
    Jrr = -(M1 * (1 / s1 ** 3 - 3 * d1r ** 2 / s1 ** 5) + M2 * (1 / s2 ** 3 - 3 * d2r ** 2 / s2 ** 5))
    Jzz = -(M1 * (1 / s1 ** 3 - 3 * d1z ** 2 / s1 ** 5) + M2 * (1 / s2 ** 3 - 3 * d2z ** 2 / s2 ** 5))
    Jrz = -(M1 * (-3 * d1r * d1z / s1 ** 5) + M2 * (-3 * d2r * d2z / s2 ** 5))
    dgm_r = (gr * Jrr + gz * Jrz) / np.maximum(gm, 1e-300)
    dgm_z = (gr * Jrz + gz * Jzz) / np.maximum(gm, 1e-300)
    S = -dnu(gm) * (dgm_r * gr + dgm_z * gz)

    def a_ph(zstar):
        dz = zstar - Z
        ker = dz * RHO / np.maximum(RHO ** 2 + dz ** 2, 1e-300) ** 1.5
        return -0.5 * np.trapz(np.trapz(S * ker, rho, axis=0), z)

    eps = (a_ph(z1) - a_ph(z2)) / (Mt / r0 ** 2)
    return eps


def efe_tensor(y_e, nu=nu_can):
    """Leading-order EFE response of a small system in a uniform external field.
    AQUAL (Milgrom 1986; the form the repo's solver uses, Aqu. line 55):
        B_par = nu(y_e),  B_perp = nu(y_e)/sqrt(1+L0),  L0 = -dln nu/dln y.
    QUMOND reproduces the same tensor at this order (the repo's own fork check:
    'the QUMOND formulation as a fork agreeing to 0.005')."""
    nu0 = float(nu(y_e))
    h = 1e-5
    L0 = -float(np.log(nu(y_e * np.exp(h))) - np.log(nu(y_e * np.exp(-h)))) / (2 * h)
    B_par = nu0
    B_perp = nu0 / np.sqrt(1.0 + L0)
    return B_par, B_perp, L0


def main():
    print("=" * 96)
    print("A24 -- the wide-binary contradiction: 1.51 (October) or 1.18 (September registration)?")
    print("=" * 96)

    # ---------------------------------------------------------------- K1
    print("\n[K1] the frozen law is the canonical one and its closure inverts exactly")
    ys = np.array([1e-3, 1e-2, 1e-1, 1.0, 3.16, 100.0])
    g = (nu_can(ys) * ys)                     # observed field in a0 units
    gN_back = g ** 2 / (g + 1.0)               # g_N = g^2/(g+a0), a0=1
    err = float(np.max(np.abs(gN_back / ys - 1.0)))
    # the same law in AQUAL form: mu(x) = y/x with y = x^2/(x+1)  => mu = x/(1+x)
    x = np.array([1e-4, 1e-2, 0.5, 1.0, 3.0, 30.0])
    y_of_x_exact = x * x / (x + 1.0)
    mu_err = float(np.max(np.abs(y_of_x_exact / x - x / (1.0 + x))))
    check("K1", err < 1e-12 and mu_err < 1e-15, f"{err:.2e}/{mu_err:.2e}", "<1e-12/<1e-15",
          "g_N=g^2/(g+a0) <=> g=(g_N/2)(1+sqrt(1+4a0/g_N)) <=> AQUAL mu(x)=x/(1+x)")

    # ---------------------------------------------------------------- K2
    print("\n[K2] the October numbers 1.20/1.51 are REPRODUCED, and the recipe identified")
    # PAPER44: quadrature law (n=2), 1.5 Msun, 3-D separation, total-mass, NO EFE.
    rep = {}
    for s in (2.0, 5.0, 10.0, 20.0):
        y = y_tot_of(1.5, s, A0_CAN)
        rep[s] = float(np.sqrt(nu_quad(y)))
    dmax = max(abs(rep[s] - PAPER44[s]) for s in PAPER44)
    check("K2", dmax < 5e-3, f"{dmax:.4f}", "<0.005 (half-unit of the paper's 2 d.p.)",
          "repro 2/5/10/20 kAU = " + ", ".join(f"{rep[s]:.4f}" for s in (2.0, 5.0, 10.0, 20.0))
          + " vs paper 1.01/1.06/1.20/1.51")
    info(f"y(20 kAU, 1.5 Msun) = {y_tot_of(1.5,20.0,A0_CAN):.5f}, nu_quad = {float(nu_quad(y_tot_of(1.5,20.0,A0_CAN))):.4f}")

    # ---------------------------------------------------------------- K3
    print("\n[K3] the quadrature is controlled (q->0 must return nu(y)-1)")
    ctrl = []
    for yv in (0.3169, 1.0, 10.0):
        e = two_body(yv, q=1e-6)
        ctrl.append(abs(e / (float(nu_rar(yv)) - 1.0) - 1.0))
    check("K3", max(ctrl) < 0.05, f"{max(ctrl):.4f}", "<0.05",
          "single-mass limit of the phantom quadrature vs nu_RAR(y)-1")

    # ---------------------------------------------------------------- K4
    print("\n[K4] (task 1) NO external field: the isolated boost of the frozen law")
    # Kernel bookkeeping, stated once and used everywhere below:
    #  * the canonical law (BRIEF) sets the TOTAL-MASS numbers;
    #  * the exact two-body phantom quadrature is run in the RAR kernel, the only
    #    one whose point-mass phantom is regular (the canonical nu -> 1 + 1/y has a
    #    non-integrable near-source tail: a point-mass artefact, see report);
    #  * the composition factor f2 = eps_exact/eps_totalmass measured in that same
    #    kernel is then applied to the canonical excess -- declared CONDITIONAL.
    rows = {}
    for foot, a0 in (("canonical", A0_CAN), ("alt", A0_ALT)):
        for s in (10.0, 20.0):
            y = y_tot_of(2.0, s, a0)
            g_tm = float(np.sqrt(nu_can(y)))
            e_tm_rar = float(nu_rar(y)) - 1.0
            e_ex = two_body(y, q=1.0)
            f2 = e_ex / e_tm_rar
            g_ex = float(np.sqrt(1.0 + f2 * (float(nu_can(y)) - 1.0)))
            a_ex = (2.0 / 3.0) * (1.0 - 2.0 * 0.5 ** 1.5) / 0.25   # Milgrom deep q=1
            g_deep = float(np.sqrt(1.0 + a_ex * (float(nu_can(y)) - 1.0)))
            rows[(foot, s)] = dict(y=float(y), total_mass=g_tm, exact=g_ex, deep_limit=g_deep,
                                   f2_composition=float(f2), exact_rar_kernel=float(np.sqrt(1.0 + e_ex)))
            info(f"{foot:9s} s={s:4.0f} kAU  y={y:.5f}  total-mass {g_tm:.4f}  "
                 f"exact {g_ex:.4f} (f2={f2:.3f})  deep-limit-form {g_deep:.4f}")
    ok4 = (1.50 < rows[("canonical", 20.0)]["total_mass"] < 1.55
           and 1.20 < rows[("canonical", 10.0)]["total_mass"] < 1.26
           and 1.38 < rows[("canonical", 20.0)]["exact"] < 1.44)
    check("K4", ok4,
          f"{rows[('canonical',20.0)]['total_mass']:.4f}/{rows[('canonical',20.0)]['exact']:.4f}",
          "1.50-1.55 / 1.38-1.44",
          "canonical 1+1 Msun, 20 kAU: total-mass / exact two-body")

    # ---------------------------------------------------------------- K5
    print("\n[K5] (task 2) WITH the Galactic field: the EFE, imposed in the same law")
    efe = {}
    for lab, xext, a0 in (("std1.8", XEXT_STD, A0_CAN),
                          ("repo1.9", XEXT_REPO_CAN, A0_CAN),
                          ("alt_repo", XEXT_REPO_ALT, A0_ALT)):
        ye = y_of_x(xext)
        for s in (10.0, 20.0):
            y = y_tot_of(2.0, s, a0)
            e = two_body(y, q=1.0, y_ext=ye)
            Bp, Bq, L0 = efe_tensor(ye)
            f2e = e / (float(nu_rar(ye)) - 1.0)          # composition factor, same kernel
            e_can = f2e * (float(nu_can(ye)) - 1.0)
            efe[(lab, s)] = dict(y=float(y), y_ext=float(ye), exact=float(np.sqrt(1.0 + e)),
                                 exact_canonical=float(np.sqrt(1.0 + e_can)), f2_efe=float(f2e),
                                 B_par=float(Bp), B_perp=float(Bq), L0=float(L0),
                                 par=float(np.sqrt(Bp)), perp=float(np.sqrt(Bq)),
                                 avg=float(np.sqrt((Bp + 2 * Bq) / 3.0)))
            info(f"{lab:9s} s={s:4.0f} kAU  x_ext={xext:.4f} -> y_ext={ye:.4f}  "
                 f"gamma_exact(theta=0) {np.sqrt(1.0+e):.4f}   sqrt(B_par) {np.sqrt(Bp):.4f}  "
                 f"sqrt(<B>) {np.sqrt((Bp+2*Bq)/3.0):.4f}")
    # declared sensitivity: 1.8 a0 read as the NEWTONIAN external field (y_ext = 1.8
    # directly) instead of the observed one.  The repo's closure uses the observed
    # field (Amd 4b), so this variant is NOT the operative reading.
    y20v = y_tot_of(2.0, 20.0, A0_CAN)
    eV = two_body(y20v, q=1.0, y_ext=XEXT_STD)
    efe[("stdN1.8", 20.0)] = dict(y=float(y20v), y_ext=float(XEXT_STD),
                                  exact=float(np.sqrt(1.0 + eV)),
                                  exact_canonical=float(np.sqrt(1.0 + (eV / (float(nu_rar(XEXT_STD)) - 1.0)) * (float(nu_can(XEXT_STD)) - 1.0))),
                                  B_par=float(nu_can(XEXT_STD)), B_perp=float("nan"), L0=float("nan"),
                                  par=float(np.sqrt(nu_can(XEXT_STD))), perp=float("nan"), avg=float("nan"))
    info(f"variant    s=  20 kAU  y_ext=1.8000 (Newtonian reading)  gamma {efe[('stdN1.8',20.0)]['exact']:.4f}"
         f" / canonical {efe[('stdN1.8',20.0)]['exact_canonical']:.4f}")

    # declared sensitivity: invert the closure with nu_RAR (the kernel of the quadrature
    # and of the repo's own y_extN) instead of nu_can.  Moves the 20 kAU number by 0.004.
    from scipy.optimize import brentq as _bq
    _f = lambda ly: np.exp(ly) * float(nu_rar(np.exp(ly))) - XEXT_STD
    ye_rar = float(np.exp(_bq(_f, np.log(1e-6), np.log(1e6), xtol=1e-14, rtol=1e-15)))
    eR = two_body(y20v, q=1.0, y_ext=ye_rar)
    inversion = {"y_ext_rar_closure": ye_rar,
                 "gamma_rar_inversion": float(np.sqrt(1.0 + eR)),
                 "gamma_rar_inversion_canonical": float(np.sqrt(1.0 + (eR / (float(nu_rar(ye_rar)) - 1.0)) * (float(nu_can(ye_rar)) - 1.0)))}
    info(f"variant    s=  20 kAU  y_ext(RAR closure)={ye_rar:.4f}  gamma {inversion['gamma_rar_inversion']:.4f}"
         f" / canonical {inversion['gamma_rar_inversion_canonical']:.4f}")

    g20 = efe[("std1.8", 20.0)]["exact"]              # RAR kernel (Arm A's kernel)
    g20c = efe[("std1.8", 20.0)]["exact_canonical"]   # canonical law, same EFE
    g20r = efe[("repo1.9", 20.0)]["exact"]
    ok5 = (abs(g20 - ARM_A_HI) < 0.005 and abs(g20c - ARM_A_HI) < 0.015
           and ARM_A_LO - 0.005 < g20r < ARM_A_HI + 0.005)
    check("K5", ok5, f"{g20:.4f}/{g20c:.4f}/{g20r:.4f}", f"|g-{ARM_A_HI}|<0.005 (RAR) / <0.015 (canonical)",
          "EFE-present boost at 20 kAU vs Arm A top 1.1814")

    # ---------------------------------------------------------------- recipe decomposition
    # Every step from the October number to the registered one, one choice at a time.
    y15 = y_tot_of(1.5, 20.0, A0_CAN)
    y20d = y_tot_of(2.0, 20.0, A0_CAN)
    decomp = {
        "paper_quad_1p5_tm_noEFE": float(np.sqrt(nu_quad(y15))),
        "canonical_1p5_tm_noEFE": float(np.sqrt(nu_can(y15))),
        "canonical_2p0_tm_noEFE": float(np.sqrt(nu_can(y20d))),
        "canonical_2p0_exact_noEFE": rows[("canonical", 20.0)]["exact"],
        "canonical_2p0_exact_EFE": g20c,
        "step_kernel_1p5": float(np.sqrt(nu_can(y15)) - np.sqrt(nu_quad(y15))),
        "step_mass_2p0": float(np.sqrt(nu_can(y20d)) - np.sqrt(nu_can(y15))),
        "step_composition": float(rows[("canonical", 20.0)]["exact"] - np.sqrt(nu_can(y20d))),
        "step_EFE": float(g20c - rows[("canonical", 20.0)]["exact"]),
        "nu_ratio_20kAU": float(nu_can(y20d) / nu_can(efe[("std1.8", 20.0)]["y_ext"])),
        "deep_limit_axy_q1": float((2.0 / 3.0) * (1.0 - 2.0 * 0.5 ** 1.5) / 0.25),
        "sigma_tot_30k": SIG_TOT_30K,
        "delta_10kAU_documents": float(PAPER44[10.0] - ARM_A_HI),
        "z_10kAU_documents": float((PAPER44[10.0] - ARM_A_HI) / SIG_TOT_30K),
    }
    print("\n[recipe] from the October number to the registered one, one choice at a time, 20 kAU:")
    for k in ("paper_quad_1p5_tm_noEFE", "canonical_1p5_tm_noEFE", "canonical_2p0_tm_noEFE",
              "canonical_2p0_exact_noEFE", "canonical_2p0_exact_EFE"):
        info(f"    {k:32s} {decomp[k]:.4f}")
    for k in ("step_kernel_1p5", "step_mass_2p0", "step_composition", "step_EFE"):
        info(f"    {k:32s} {decomp[k]:+.4f}")

    # ---------------------------------------------------------------- K6
    print("\n[K6] (task 2, the decision) EFE effect vs solver fork")
    d_efe = rows[("canonical", 20.0)]["total_mass"] - g20
    d_solver_repo = 0.016   # profile-level QUMOND-vs-AQUAL spread measured by the repo solver
    d_solver_here = abs(g20 - np.sqrt((efe[("std1.8", 20.0)]["B_par"] + 2 * efe[("std1.8", 20.0)]["B_perp"]) / 3.0))
    z_efe = d_efe / SIG_TOT_30K
    z_sol = max(d_solver_repo, d_solver_here) / SIG_TOT_30K
    check("K6", d_efe / max(d_solver_repo, d_solver_here) > 10.0,
          f"{d_efe/max(d_solver_repo,d_solver_here):.1f}x", ">10x",
          f"EFE Delta gamma {d_efe:.3f} ({z_efe:.1f} sig_tot) vs solver {max(d_solver_repo,d_solver_here):.3f} ({z_sol:.1f} sig_tot)")

    # ---------------------------------------------------------------- K7
    print("\n[K7] (task 3) where 1.51 sits in the framework's own scoring")
    check("K7", (PAPER44[20.0] > GUARD_ZONE) and (NO_EFE_BENCH > GUARD_ZONE),
          f"1.51>{GUARD_ZONE}, bench {NO_EFE_BENCH}>{GUARD_ZONE}", "both above the guard edge",
          "the October number and the registered no-EFE benchmark are both UNSCOREABLE")

    # ---------------------------------------------------------------- K8
    print("\n[K8] (task 4) the decisive measurement")
    d20 = PAPER44[20.0] - ARM_A_HI                 # the two documents' own numbers
    d20_like = rows[("canonical", 20.0)]["exact"] - efe[("std1.8", 20.0)]["exact_canonical"]
    z20 = d20 / SIG_TOT_30K
    # pairs needed for FORECAST_SIGMA at 20 kAU (pooled sigma convention)
    def pairs_for(delta):
        s_need = delta / FORECAST_SIGMA
        s_fit = np.sqrt(max(s_need ** 2 - SIG_SYS ** 2, 0.0))
        return N_FROZEN * (SIG_FIT_30K / s_fit) ** 2, s_need
    n_need, sig_need = pairs_for(d20)
    n_need_like, sig_need_like = pairs_for(d20_like)
    sig_need_fit = float(np.sqrt(max(sig_need ** 2 - SIG_SYS ** 2, 0.0)))
    z20_like = d20_like / SIG_TOT_30K
    # bin occupancy: frozen N log-uniform over 2-30 kAU, 18-22 kAU bin
    frac = np.log10(22.0 / 18.0) / np.log10(30.0 / 2.0)
    n_bin = frac * N_FROZEN
    sig_fit_bin = SIG_FIT_30K * np.sqrt(N_FROZEN / n_bin)
    sig_tot_bin = float(np.hypot(sig_fit_bin, SIG_SYS))
    z_bin = d20 / sig_tot_bin
    # 10 kAU: can it ever reach 4.2 sigma given the irreducible 0.020?
    d10 = rows[("canonical", 10.0)]["total_mass"] - ARM_A_HI
    d10_like = rows[("canonical", 10.0)]["exact"] - efe[("std1.8", 10.0)]["exact_canonical"]
    z10_inf = d10_like / SIG_SYS
    check("K8", (n_need < n_bin) and (z20 > 10.0) and (z10_inf < FORECAST_SIGMA) and (z_bin > 4.0),
          f"N{int(round(n_need))}<Nbin{int(round(n_bin))}, z20={z20:.1f}, zbin={z_bin:.1f}, z10inf={z10_inf:.1f}",
          "Nneed<Nbin, z20>10, zbin>4, z10inf<4.2",
          f"20 kAU bin decides at {z_bin:.1f} sigma; 10 kAU cannot at any N")

    # ---------------------------------------------------------------- K9
    print("\n[K9] kernel sensitivity of the registered arm (declared systematic)")
    ye = y_of_x(XEXT_REPO_CAN)
    g_can = float(np.sqrt(nu_can(ye)))
    g_rar = float(np.sqrt(nu_rar(1.28903)))
    dk = abs(g_can - g_rar)
    check("K9", dk < 0.025, f"{dk:.4f}", "<0.025",
          f"canonical sqrt(nu(y_ext)) {g_can:.4f} vs RAR {g_rar:.4f} ({dk/SIG_FIT_30K:.1f} sig_fit)")

    # ---------------------------------------------------------------- K10
    print("\n[K10] (task 1, the stated assumption) what 'internal acceleration' can and cannot do")
    R_SUN = 6.957e8
    g_self = G_N * MSUN / R_SUN ** 2                 # 274 m/s^2
    y_self = g_self / A0_CAN
    gam_self = float(np.sqrt(nu_can(y_self)))        # surface-self-field reading
    f2_20 = rows[("canonical", 20.0)]["f2_composition"]
    info(f"g_self = {g_self:.1f} m/s^2 = {y_self:.3e} a0 -> gamma_v - 1 = {gam_self-1:.2e}")
    info(f"mutual-field composition factor f2(20 kAU) = {f2_20:.3f}")
    extra = {"g_self_ms2": float(g_self), "y_self_a0": float(y_self),
             "nu_minus_1_surface": float(nu_can(y_self) - 1.0),
             "gamma_minus_1_surface": float(gam_self - 1.0), "nu_self": float(nu_can(y_self))}
    check("K10", (gam_self - 1.0 < 1e-9) and (0.65 < f2_20 < 0.80),
          f"{gam_self-1:.1e}/{f2_20:.3f}", "<1e-9 / 0.65-0.80",
          "surface-self-field reading kills ALL MOND (excluded); the live suppression is f2")

    # ---------------------------------------------------------------- mutation
    if MUTATE:
        print("\n[MUTATE] drop the external field from the EFE check (y_ext -> 0)")
        e_mut = two_body(y_tot_of(2.0, 20.0, A0_CAN), q=1.0, y_ext=0.0)
        g_mut = float(np.sqrt(1.0 + e_mut))
        ok = abs(g_mut - ARM_A_HI) < 0.005
        check("K5m", ok, f"{g_mut:.4f}", f"|g-{ARM_A_HI}|<0.005",
              "MUTATED: EFE removed; K5 must fail")
        print("\nMUTATION BIT: K5 FAILED as required." if not ok else "\nMUTATION DID NOT BITE.")

    # ---------------------------------------------------------------- summary
    npass = sum(1 for c in CHECKS if c["pass"])
    ntot = len(CHECKS)
    print("\n" + "=" * 96)
    print(f"A24 COMPLETE: {npass}/{ntot} checks PASS.")
    print("=" * 96)

    out = {
        "lane": "A24_wide_binaries",
        "status": "DERIVED",
        "checks": CHECKS,
        "numbers": {
            "isolated": {f"{k[0]}_{int(k[1])}kAU": v for k, v in rows.items()},
            "efe": {f"{k[0]}_{int(k[1])}kAU": v for k, v in efe.items()},
            "paper44_reproduction": {f"{s}kAU": v for s, v in rep.items()},
            "delta_gamma_efe_20kAU": d_efe,
            "delta_gamma_solver": max(d_solver_repo, d_solver_here),
            "z_efe_sig_tot": z_efe,
            "z_solver_sig_tot": z_sol,
            "z_20kAU_paper_vs_armA": z20,
            "delta_20kAU_documents": float(d20),
            "arm_gap_top_rar": float(ARM_A_HI - g20),
            "arm_gap_top_canonical": float(g20c - ARM_A_HI),
            "sigma_fit_bin_20kAU": float(sig_fit_bin),
            "n_cat_like_for_like": float(N_FROZEN * n_need_like / n_bin),
            "surface_self_field": extra,
            "inversion_variants": inversion,
            "efe_bracket_20kAU": [float(inversion["gamma_rar_inversion"]), float(g20c)],
            "z_20kAU_like_for_like": z20_like,
            "delta_20kAU_like_for_like": d20_like,
            "recipe_decomposition": decomp,
            "sigma_fit_need_4p2": sig_need_fit,
            "delta_10kAU_published": d10,
            "delta_10kAU_like_for_like": d10_like,
            "z_10kAU_at_infinite_N": z10_inf,
            "pairs_for_4p2sigma_20kAU": n_need,
            "pairs_for_4p2sigma_20kAU_like_for_like": n_need_like,
            "sigma_need_4p2": sig_need,
            "bin_frac_18_22kAU": frac,
            "pairs_in_18_22kAU_bin": n_bin,
            "sigma_tot_bin_20kAU": sig_tot_bin,
            "z_bin_20kAU": z_bin,
            "kernel_shift_armA": dk,
        },
        "constants_used": [
            "G=6.67430e-11 (BRIEF)", "Msun=1.98892e30 (IAU nominal)",
            "kAU=1.495978707e14 m", "a0_can=9.36e-11 (BRIEF)", "a0_alt=1.13e-10 (BRIEF)",
            "Arm A 1.1614-1.1814 / 1.1917-1.2267 (PREREG Amd 10)",
            "guard 1.23, no-EFE bench 1.33 (PREREG Amd 10(d))",
            "sigma_fit=0.019, sigma_sys=0.020, N=30000 (PREREG 1.5)",
            "4.2 sigma forecast = 0.116/sigma_tot (PREREG Amd 11 line 1152)",
            "x_ext=1.8996/1.5764 (aqual_efe_full_solve_2026.py line 45)",
            "1.20/1.51 (PAPER44 tex lines 29/59 = Zenodo 23251278)",
            "QUMOND-vs-AQUAL fork 0.005 / 0.016 (PREREGISTRATION_DR4.md Amd 10(a) note)",
            "nu_RAR = 1/(1-exp(-sqrt y)) (the kernel Arm A and the frozen pipeline use)",
        ],
        "mutate": bool(MUTATE),
    }
    with open("a24_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("wrote a24_results.json")
    return 0 if npass == ntot else 1


if __name__ == "__main__":
    sys.exit(main())
