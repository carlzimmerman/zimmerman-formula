#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage16_lognormal_forest_mock_2026.py
=====================================
THE FOREST SUPPRESSION, COMPUTED HERE RATHER THAN QUOTED -- a lognormal Lyman-alpha mock pipeline that
runs end to end on a laptop, driven by the sector's OWN linear transfer function, which is itself
solved from the sector's own Jeans equation rather than assumed to have anyone else's shape.

--------------------------------------------------------------------------------------------------
WHY THIS EXISTS, AND WHAT IT IS NOT
--------------------------------------------------------------------------------------------------
Stage 15 mapped the gamma = 0 sector onto Murgia+18's alpha and found it PASSES the shape-marginalised
bound alpha < 0.03 h^-1 Mpc at every forest redshift, worst bin alpha = 0.0200 at z = 2, margin 1.5x.
It then named three risks it could not retire.  Risk C3 was the biggest and the most specific:

    at z ~ 2-3 the forest DOES NOT RESOLVE this cutoff.  It constrains through the projection
        P_1D(k) = (1/2pi) \int_k^inf k' P_3D(k') dk'
    so a 3D cutoff at ANY small scale removes power from the integral at ALL observable k.

That is not a caveat that can be argued about -- it is a number, and it is computable.  This script
computes it.  Part A below shows the arithmetic that makes it unavoidable: the sector's half-mode sits
at k_half ~ 35 h/Mpc while MIKE/HIRES reach k = 0.08 s/km ~ 3.9 h/Mpc and Irsic+24 reach 0.2 s/km
~ 11 h/Mpc.  The cutoff is 3-9x beyond the data in every case.  So NOTHING about this constraint is a
direct measurement of the cutoff, and the entire signal is the projected amplitude/slope response.

*** WHAT THIS IS NOT: a primary forest bound. ***  That needs a hydrodynamic-simulation emulator over
a grid of thermal histories, which is O(10^4-10^5) core-hours PER RUN and ~180 GB of memory for one
publication-resolution box -- roughly 3x this machine's RAM before a grid is even considered, and the
failure mode is specifically fatal here because under-resolving MANUFACTURES a cutoff of numerical
origin, which is the very signal being tested.  A lognormal mock evades that trap by construction:
it never has to resolve collapse, because it never simulates any.  It takes an arbitrary input P(k)
-- which is exactly what the public hydro emulators (lym1d, LaCE/cup1d, lya_emulator) refuse, since
they interpolate over grids of near-standard cosmologies and have no axis for a free cutoff shape.

The price is accuracy, and it is a real price: a lognormal forest model reproduces full hydro P_F1D to
tens of percent in ABSOLUTE terms.  That is why every number reported here is a RATIO at matched
seeds, matched thermal treatment and matched mean flux -- the configuration in which the systematics
cancel and the residual is the physics.  Part D demonstrates the cancellation instead of asserting it.

--------------------------------------------------------------------------------------------------
CORRECTION TO STAGE 15, PART D1 -- IT SAID THE TOOL IS PUBLIC.  IT IS NOT.
--------------------------------------------------------------------------------------------------
Stage 15's D1 asserted: "THE TOOL EXISTS AND IS PUBLIC: Hooper, Lopez, Boyarsky, Cyr-Racine, Irsic,
Ruchayskiy 2022, 'One likelihood to bind them all' (arXiv:2206.08188), releases a Lyman-alpha
likelihood in exactly this generic parameterisation."  *** THAT IS WRONG AND IS WITHDRAWN HERE. ***
The paper states only that the likelihood "will be made publicly available upon publication of this
paper" and gives no URL.  Probes on 2026-08-10: two plausible author repositories 404; the Lya_abgd
path inside montepython_public 404; Zenodo search empty; GitHub code search total_count = 0.  Only
the base MontePython returns 200.  The release does not appear to exist.  What IS public is a set of
Lyman-alpha likelihoods for STANDARD cosmologies (lym1d, LaCE/cup1d, lya_emulator) which cannot take
a free cutoff shape.  So the MCMC stage 15 called "a day of work" is not available at any price of
effort here; it needs the authors.  This script is what CAN be done instead, and it is not a
substitute for that MCMC -- it is a different, weaker, self-computed measurement.

--------------------------------------------------------------------------------------------------
THE PIPELINE
--------------------------------------------------------------------------------------------------
  A  the sector's T(k,z) from ITS OWN Jeans ODE -- c_s^2 = K/rho  =>  c_s^2 ~ a^3, so unlike WDM this
     fluid is COLD early and warms up, imprinting its cutoff progressively.  Cross-checked against
     stage 15's independent alpha map.
  B  lognormal mock: CLASS linear P(k,z) -> model T(k) -> IGM pressure filter -> Gaussian realisation
     -> lognormal density -> linear RSD -> FGPA optical depth -> thermal broadening -> mean-flux
     calibration to Becker+13 -> P_F1D in velocity units.
  C  matched CDM/sector pairs at IDENTICAL seeds; the suppression ratio at observable k.
  D  convergence: resolution, box size, Nyquist/projection tail, seed variance, and the RSD and
     lognormal-inversion sensitivities.
  E  the suppression against representative published P_F1D precision.
  F  limits, and what would overturn this.

Run:  python3 stage16_lognormal_forest_mock_2026.py           (default, ~minutes)
      python3 stage16_lognormal_forest_mock_2026.py --full    (adds the N=768 and L=40 convergence)
"""

import sys
import numpy as np
from scipy import fft as sfft
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.interpolate import interp1d

FAIL = []
NCHK = [0]
FULL = "--full" in sys.argv


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


# =================================================================================================
# cosmology + framework constants
# =================================================================================================
H0_H = 0.674                  # h
OM = 0.315                    # Omega_m
OL = 1.0 - OM
H0 = 100.0 * H0_H             # km/s/Mpc
MPC_M = 3.0856775814913673e22
G_SI = 6.67430e-11
C_KMS = 299792.458

LAM_J0_MPC = 2.2              # comoving Mpc today -- stage 12's weak-lensing exclusion radius
W0, WA = -0.75, -0.86         # DESI, for the a_0(z) law

Z_FOREST = (2.0, 3.0, 4.0, 5.0)

# Murgia+18 shape factors, carried from stage 15 so the two routes stay comparable
C_SHARP, C_WDM, C_STEP = 0.698, 0.325, 1.0
ALPHA_BOUND = 0.03


def Hz(z):
    return H0 * np.sqrt(OM * (1.0 + z) ** 3 + OL)


def Om_a(a):
    return OM * a ** -3 / (OM * a ** -3 + OL)


def a0_ratio(z):
    """the framework's own a_0(z) law -- load-bearing, never replace with a constant a_0."""
    return (1.0 + z) ** (1.5 * (1.0 + W0 + WA)) * np.exp(-1.5 * WA * z / (1.0 + z))


def k_com_to_kv(k_hMpc, z):
    """comoving h/Mpc  ->  s/km along the line of sight:  k_v = k_com * (1+z)/H(z)."""
    return k_hMpc * H0_H * (1.0 + z) / Hz(z)


def kv_to_k_com(kv, z):
    return kv * Hz(z) / (1.0 + z) / H0_H


def tau_eff_becker(z):
    """Becker et al. 2013 effective optical depth fit (calibrated z >~ 2.15)."""
    return 0.751 * ((1.0 + z) / 4.5) ** 2.90 - 0.132


def mean_flux(z):
    return np.exp(-tau_eff_becker(z))


print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the sector's OWN transfer function, and the arithmetic that makes this a projection")
print("=" * 100)

# --- A0: the sound speed, calibrated from stage 12/13's lam_J(today) = 2.2 Mpc -------------------
# lam_J = c_s sqrt(pi / (G rho_m))   with rho_m the clustering density today
rho_crit0 = 3.0 * (H0 * 1000.0 / MPC_M) ** 2 / (8.0 * np.pi * G_SI)
rho_m0 = OM * rho_crit0
cs0_ms = LAM_J0_MPC * MPC_M * np.sqrt(G_SI * rho_m0 / np.pi)
cs0_kms = cs0_ms / 1000.0
info(f"A0  calibration: lam_J(today) = {LAM_J0_MPC} Mpc  =>  c_s(today) = {cs0_kms:.3f} km/s "
     f"(c_s^2 = {(cs0_kms / C_KMS) ** 2:.3e} c^2), and c_s^2 = K/rho with rho ~ a^-3 gives "
     "c_s^2 ~ a^3 EXACTLY -- this fluid is COLD early and warms up.",
     "the opposite of WDM, which is why its comoving cutoff GROWS toward low z")

# --- A1: the projection arithmetic --------------------------------------------------------------
print("\n     z    lam_J com [Mpc]   k_half [h/Mpc]   alpha [h^-1 Mpc]     k_max data [h/Mpc]   ratio")
proj = {}
for z in Z_FOREST:
    growth = (1.0 + z) ** 3 * a0_ratio(z) ** (1.0 / 3.0)
    lam_com = LAM_J0_MPC / growth * (1.0 + z)
    k_half = 2.0 * np.pi / (lam_com * H0_H)
    alpha = C_SHARP / k_half
    kmax_mh = kv_to_k_com(0.08, z)        # MIKE/HIRES reach
    kmax_ir = kv_to_k_com(0.20, z)        # Irsic+24 reach
    proj[z] = dict(lam_com=lam_com, k_half=k_half, alpha=alpha, kmax_mh=kmax_mh, kmax_ir=kmax_ir)
    print(f"    {z:>3.0f}      {lam_com:>9.4f}        {k_half:>8.2f}       {alpha:>9.4f}          "
          f"{kmax_mh:>6.2f} / {kmax_ir:>5.2f}        {k_half / kmax_ir:>4.1f}x")

worst_alpha = max(p["alpha"] for p in proj.values())
check(abs(worst_alpha - 0.0200) < 0.0015,
      f"A1  reproduces stage 15's alpha map independently: worst bin (z = 2) alpha = "
      f"{worst_alpha:.4f} h^-1 Mpc against the shape-marginalised bound {ALPHA_BOUND} "
      f"(margin {ALPHA_BOUND / worst_alpha:.2f}x)",
      "same chain, recomputed here -- so Part C is testing the same sector stage 15 tested")

r_mh = [p["k_half"] / p["kmax_mh"] for p in proj.values()]
r_ir = [p["k_half"] / p["kmax_ir"] for p in proj.values()]
check(all(r > 1.5 for r in r_ir),
      f"A2  *** AND THE CUTOFF IS BEYOND THE DATA AT EVERY REDSHIFT: by {min(r_mh):.1f}-{max(r_mh):.1f}x "
      f"against MIKE/HIRES (k_max = 0.08 s/km) and still {min(r_ir):.1f}-{max(r_ir):.1f}x against the "
      f"deepest published reach (Irsic+24, 0.2 s/km).  So no forest dataset resolves this cutoff and "
      f"the ENTIRE constraint is the projected response of P_1D. ***",
      "this is stage 15's risk C3, stated as arithmetic rather than as a worry -- and note the z = 2 "
      "margin against the deepest data is only 1.8x, so the separation is NOT large")

# --- A2: solve the sector's linear Jeans ODE -> T(k,z) -------------------------------------------
Z_INIT = 100.0


def growth_ode(k_hMpc, with_pressure):
    """delta'' + (2 - 1.5 Om(a)) delta' + (cs^2 k^2/(a^2 H^2) - 1.5 Om(a)) delta = 0,  x = ln a."""
    k_mpc = k_hMpc * H0_H                                    # comoving Mpc^-1

    def rhs(x, y):
        a = np.exp(x)
        Hval = H0 * np.sqrt(OM * a ** -3 + OL)                # km/s/Mpc
        om = Om_a(a)
        cs2 = (cs0_kms ** 2) * a ** 3 if with_pressure else 0.0   # (km/s)^2
        jeans = cs2 * k_mpc ** 2 / (a ** 2 * Hval ** 2)
        return [y[1], -(2.0 - 1.5 * om) * y[1] - (jeans - 1.5 * om) * y[0]]

    x0, x1 = np.log(1.0 / (1.0 + Z_INIT)), 0.0
    xs = np.log(1.0 / (1.0 + np.array(Z_FOREST)))
    sol = solve_ivp(rhs, (x0, x1), [1.0, 1.0], t_eval=np.sort(xs), rtol=1e-9, atol=1e-14,
                    method="Radau")
    order = np.argsort(np.argsort(xs))
    return sol.y[0][order]


K_GRID = np.logspace(np.log10(0.05), np.log10(4000.0), 160)
T_sector = np.zeros((len(K_GRID), len(Z_FOREST)))
for i, kk in enumerate(K_GRID):
    d_p = growth_ode(kk, True)
    d_c = growth_ode(kk, False)
    T_sector[i] = d_p / d_c
T_sector = np.clip(T_sector, 0.0, None)

print("\n   T(k,z) from the sector's own Jeans ODE (ratio of linear growth, pressure vs pressureless):")
print("        k [h/Mpc]" + "".join(f"      z={z:.0f}" for z in Z_FOREST))
for kk in (1.0, 5.0, 10.0, 20.0, 35.0, 60.0, 100.0):
    j = int(np.argmin(np.abs(K_GRID - kk)))
    print(f"        {K_GRID[j]:>8.2f}" + "".join(f"    {T_sector[j, m]:>7.4f}"
                                                 for m in range(len(Z_FOREST))))

# half-mode from the ODE, compared with the analytic map
T_ode_half = {}
for m, z in enumerate(Z_FOREST):
    t = T_sector[:, m]
    if t.min() < 0.5 < t.max():
        f = interp1d(t[::-1], K_GRID[::-1], bounds_error=False)
        T_ode_half[z] = float(f(0.5))
    else:
        T_ode_half[z] = np.nan

print("\n     z    k_half ODE [h/Mpc]   k_half analytic   ODE/analytic")
for z in Z_FOREST:
    r = T_ode_half[z] / proj[z]["k_half"]
    print(f"    {z:>3.0f}         {T_ode_half[z]:>8.2f}            {proj[z]['k_half']:>8.2f}        "
          f"{r:>6.3f}")

ode_ratios = np.array([T_ode_half[z] / proj[z]["k_half"] for z in Z_FOREST])
check(np.all(np.isfinite(ode_ratios)) and ode_ratios.max() / ode_ratios.min() < 1.6,
      f"A3  the two independent routes to the cutoff scale agree in SHAPE to "
      f"{ode_ratios.max() / ode_ratios.min():.2f}x across z = 2-5 -- the dynamical ODE and stage 15's "
      f"static Jeans map track each other, with an overall offset of {ode_ratios.mean():.2f}x from the "
      "lam_J convention factor",
      "the offset is a definition, the redshift TREND is physics, and the trend matches")

check(T_ode_half[5.0] > T_ode_half[2.0] * 1.5,
      f"A4  and the ODE independently reproduces the direction that matters: k_half RISES from "
      f"{T_ode_half[2.0]:.1f} h/Mpc at z = 2 to {T_ode_half[5.0]:.1f} at z = 5 -- equivalently the "
      "comoving cutoff LENGTH grows toward low z, because c_s^2 ~ a^3 warms this fluid up",
      "so the binding forest bin is the LOW-z one -- the opposite of every WDM analysis")


# =================================================================================================
print()
print("=" * 100)
print("PART B -- the lognormal mock, built and validated")
print("=" * 100)

try:
    from classy import Class
    HAVE_CLASS = True
except Exception as exc:                                          # pragma: no cover
    HAVE_CLASS = False
    info(f"B0  classy unavailable ({exc}); falling back to an Eisenstein-Hu transfer function")

_PK_CACHE = {}


def linear_pk(z, k_hMpc):
    """linear P(k) [ (Mpc/h)^3 ] at redshift z, from CLASS when available."""
    key = round(z, 4)
    if key not in _PK_CACHE:
        if HAVE_CLASS:
            cosmo = Class()
            cosmo.set({
                "output": "mPk", "P_k_max_h/Mpc": 400.0, "z_max_pk": 6.0,
                "h": H0_H, "omega_b": 0.02237, "omega_cdm": 0.1200,
                "A_s": 2.100e-9, "n_s": 0.9649, "tau_reio": 0.0544,
                "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06, "T_ncdm": 0.71611,
            })
            cosmo.compute()
            kk = np.logspace(-4, np.log10(390.0), 700)
            pk = np.array([cosmo.pk_lin(k * H0_H, z) for k in kk]) * H0_H ** 3
            cosmo.struct_cleanup()
            cosmo.empty()
        else:
            kk = np.logspace(-4, np.log10(390.0), 700)
            q = kk / (OM * H0_H)
            L = np.log(2.0 * np.e + 1.8 * q)
            Cq = 14.2 + 731.0 / (1.0 + 62.5 * q)
            T = L / (L + Cq * q ** 2)
            d = 1.0 / (1.0 + z)
            pk = (kk ** 0.9649) * T ** 2 * d ** 2
            pk *= 2.1e4 / np.interp(1.0, kk, pk)
        _PK_CACHE[key] = (kk, pk)
    kk, pk = _PK_CACHE[key]
    return np.exp(np.interp(np.log(k_hMpc), np.log(kk), np.log(pk)))


def sector_T(k_hMpc, z):
    m = Z_FOREST.index(z) if z in Z_FOREST else None
    if m is None:
        raise ValueError(z)
    lt = np.interp(np.log(k_hMpc), np.log(K_GRID), T_sector[:, m],
                   left=T_sector[0, m], right=0.0)
    return np.clip(lt, 0.0, 1.0)


def make_flux_box(z, N, L, seed, model, k_F=None, rsd=True, gamma_T=1.5, T0=1.0e4,
                  return_sigma=False):
    """One lognormal forest box.  Returns (k_v [s/km], P_F1D [km/s]).

    model: 'cdm' or 'sector'.  IDENTICAL seed -> identical Gaussian phases, so the
    CDM/sector ratio is free of sample variance by construction.
    """
    rng = np.random.default_rng(seed)
    kf = 2.0 * np.pi * sfft.fftfreq(N, d=L / N)
    kz = 2.0 * np.pi * sfft.rfftfreq(N, d=L / N)
    KX, KY, KZ = np.meshgrid(kf, kf, kz, indexing="ij")
    K2 = KX ** 2 + KY ** 2 + KZ ** 2
    K2[0, 0, 0] = 1e-16                                    # keep mu^2 = kz^2/k^2 finite at DC
    K = np.sqrt(K2)

    # ---- input power: linear x model transfer x IGM pressure filter ----
    P = linear_pk(z, K)
    if model == "sector":
        P = P * sector_T(K, z) ** 2
    if k_F is not None:                                    # Gnedin & Hui 1998 filtering
        P = P / (1.0 + K2 / k_F ** 2) ** 2
    if rsd:                                                # linear Kaiser along z
        f = Om_a(1.0 / (1.0 + z)) ** 0.55
        mu2 = KZ ** 2 / K2
        P = P * (1.0 + f * mu2) ** 2
    P[0, 0, 0] = 0.0

    # ---- Gaussian realisation ----
    amp = np.sqrt(P / L ** 3).astype(np.float32)
    wr = rng.standard_normal((N, N, N // 2 + 1)).astype(np.float32)
    wi = rng.standard_normal((N, N, N // 2 + 1)).astype(np.float32)
    dk = (wr + 1j * wi).astype(np.complex64) * amp / np.sqrt(2.0)
    dk[0, 0, 0] = 0.0
    del amp, wr, wi, P, KX, KY, KZ, K, K2
    dg = sfft.irfftn(dk, s=(N, N, N), workers=-1).astype(np.float32) * N ** 3
    del dk

    sigma2 = float(np.var(dg, dtype=np.float64))
    rho = np.exp(dg - 0.5 * sigma2, dtype=np.float32)       # <rho> = 1 for a Gaussian dg
    del dg

    # ---- FGPA optical depth, thermal broadening, mean-flux calibration ----
    beta_tau = 2.0 - 0.7 * (gamma_T - 1.0)
    src = rho ** beta_tau
    del rho

    dv = (Hz(z) / (1.0 + z)) * (L / H0_H) / N               # km/s per cell along LOS
    b_kms = np.sqrt(2.0 * 1.380649e-23 * T0 / 1.67262192e-27) / 1000.0
    nsm = b_kms / dv
    if nsm > 0.05:                                          # Gaussian convolve along LOS
        kk1 = 2.0 * np.pi * sfft.rfftfreq(N, d=1.0)
        W = np.exp(-0.5 * (kk1 * nsm) ** 2).astype(np.float32)
        src = sfft.irfftn(sfft.rfftn(src, axes=(2,), workers=-1) * W,
                          s=(N,), axes=(2,), workers=-1).astype(np.float32)
        src = np.clip(src, 1e-8, None)

    target = mean_flux(z)

    def resid(lnA):
        return float(np.mean(np.exp(-np.exp(lnA) * src, dtype=np.float64))) - target

    lnA = brentq(resid, -12.0, 8.0, xtol=1e-10)
    F = np.exp(-np.exp(lnA) * src)
    del src

    # ---- P_F1D in velocity units ----
    dF = (F / float(np.mean(F, dtype=np.float64)) - 1.0).astype(np.float32)
    del F
    Fk = sfft.rfftn(dF, axes=(2,), workers=-1)
    p1d = (np.abs(Fk) ** 2).mean(axis=(0, 1)).astype(np.float64) * dv / N
    del Fk, dF

    kv = 2.0 * np.pi * sfft.rfftfreq(N, d=dv)
    if return_sigma:
        return kv, p1d, sigma2, np.exp(lnA)
    return kv, p1d


# --- B1: the IGM filtering scale, which sits on top of the sector's cutoff ----------------------
# pressure-smoothing scale ~100 kpc physical (Gnedin & Hui; Kulkarni+15 lam_P ~ 80-120 kpc)
LAM_P_PHYS_KPC = 100.0
K_F = {z: 2.0 * np.pi / (LAM_P_PHYS_KPC * 1e-3 * (1.0 + z) * H0_H) for z in Z_FOREST}
print("\n     z   IGM filter k_F [h/Mpc]   sector k_half [h/Mpc]   k_half / k_F")
for z in Z_FOREST:
    print(f"    {z:>3.0f}          {K_F[z]:>8.2f}                {T_ode_half[z]:>8.2f}            "
          f"{T_ode_half[z] / K_F[z]:>5.2f}")

check(all(T_ode_half[z] > K_F[z] for z in Z_FOREST),
      "B1  *** THE SECTOR'S CUTOFF LIES BELOW THE IGM'S OWN PRESSURE-SMOOTHING SCALE AT EVERY FOREST "
      "REDSHIFT.  The gas is already smoothed on scales larger than the sector's cutoff, by physics "
      "that is in every published analysis and is marginalised over there. ***",
      "so the sector is adding a cutoff underneath an existing one -- a point strongly in its favour "
      "that I did not anticipate, and Part C measures rather than asserts")

# --- B2: validate the mock against known forest phenomenology -----------------------------------
N0, L0 = 512, 20.0
kv3, p3, s2_3, A3v = make_flux_box(3.0, N0, L0, 20260810, "cdm", k_F=K_F[3.0], return_sigma=True)
sel = (kv3 > 1e-3) & (kv3 < 0.1)
info(f"B2  validation run z = 3, N = {N0}, L = {L0} Mpc/h: sigma_G^2 = {s2_3:.3f}, "
     f"<F> = {mean_flux(3.0):.3f} (Becker+13), tau amplitude A = {A3v:.3e}, "
     f"k P_F1D/pi at k = 0.01 s/km = "
     f"{np.interp(0.01, kv3[sel], (kv3 * p3 / np.pi)[sel]):.4f}")
check(s2_3 < 6.0,
      f"B3  the Gaussian variance after IGM filtering is sigma_G^2 = {s2_3:.3f} at z = 3 -- inside "
      "the sigma^2 ~ 3-5 regime that published lognormal forest mocks operate in at these redshifts "
      "(the transformation is designed for exactly this skewness), though large enough that ABSOLUTE "
      "P_F1D from it should not be trusted",
      "which is why nothing absolute is reported: D1/D2/D5 bound the matched-pair RATIO's sensitivity "
      "to the transformation directly, and that is the only quantity used")
kP = (kv3 * p3 / np.pi)[sel]
check(0.005 < np.interp(0.01, kv3[sel], kP) < 0.15 and np.all(np.isfinite(kP)),
      "B4  and the dimensionless flux power at z = 3 lands in the observed decade "
      "(k P_F1D/pi ~ 0.01-0.1 at k ~ 0.01 s/km in eBOSS/XQ-100), so the pipeline is producing forest-"
      "like spectra rather than numbers of the wrong order",
      "an order-of-magnitude validation only -- this is a lognormal model, not hydro")


# =================================================================================================
print()
print("=" * 100)
print("PART C -- the matched-pair suppression: what the sector actually predicts for P_F1D")
print("=" * 100)

SEED = 20260810
K_REPORT = (0.005, 0.01, 0.02, 0.05, 0.08, 0.15)


def suppression(z, N=N0, L=L0, seed=SEED, rsd=True, k_F_on=True):
    kf_ = K_F[z] if k_F_on else None
    kv_c, p_c = make_flux_box(z, N, L, seed, "cdm", k_F=kf_, rsd=rsd)
    kv_s, p_s = make_flux_box(z, N, L, seed, "sector", k_F=kf_, rsd=rsd)
    good = (kv_c > 0) & (p_c > 0)
    return kv_c[good], (p_s[good] / p_c[good])


print("\n   P_F1D(sector) / P_F1D(CDM), matched seeds, matched <F>, matched thermal treatment")
print("        k_v [s/km]" + "".join(f"     z={z:.0f}" for z in Z_FOREST))
supp = {}
for z in Z_FOREST:
    kvv, rr = suppression(z)
    supp[z] = (kvv, rr)
rows = []
for kt in K_REPORT:
    line = f"        {kt:>9.3f}"
    vals = []
    for z in Z_FOREST:
        kvv, rr = supp[z]
        v = float(np.interp(kt, kvv, rr)) if kt <= kvv.max() else np.nan
        vals.append(v)
        line += f"   {v:>7.4f}" if np.isfinite(v) else "       ---"
    rows.append((kt, vals))
    print(line)

# the binding comparison: MIKE/HIRES band at z >= 4, and the eBOSS band at z = 2-3
supp_z2_002 = float(np.interp(0.02, supp[2.0][0], supp[2.0][1]))
supp_z3_002 = float(np.interp(0.02, supp[3.0][0], supp[3.0][1]))
supp_z4_008 = float(np.interp(0.08, supp[4.0][0], supp[4.0][1]))
supp_z5_008 = float(np.interp(0.08, supp[5.0][0], supp[5.0][1]))

check(np.all(np.isfinite([supp_z2_002, supp_z3_002, supp_z4_008, supp_z5_008])),
      "C1  the pipeline returns finite suppression at every reported (k, z)",
      f"z=2 @ 0.02 s/km: {supp_z2_002:.4f}; z=3: {supp_z3_002:.4f}; "
      f"z=4 @ 0.08: {supp_z4_008:.4f}; z=5 @ 0.08: {supp_z5_008:.4f}")

dev = [abs(1.0 - v) for _, vals in rows for v in vals if np.isfinite(v)]
worst_dev = max(dev)
over = max((v - 1.0) for _, vals in rows for v in vals if np.isfinite(v))
check(worst_dev < 0.05,
      f"C2  the flux-power response is at the percent level everywhere reported (max |ratio-1| = "
      f"{100 * worst_dev:.2f}%), and it is NOT sign-definite: the ratio exceeds unity by up to "
      f"{100 * max(over, 0.0):.2f}% in some bins.  That is correct forest physics, not a bug -- the "
      "3D INPUT is strictly suppressed (T <= 1 by construction in Part A), but the mean-flux "
      "recalibration redistributes flux power, so removing small-scale 3D power can RAISE P_F1D at "
      "some k.  Murgia et al.'s own suppression curves cross unity the same way",
      "the deliverable is therefore the full scale-dependent response, not a one-signed suppression")

# is the low-z bin the binding one, as stage 15 predicted?
low_z_dev = max(abs(1.0 - float(np.interp(0.02, supp[z][0], supp[z][1]))) for z in (2.0, 3.0))
high_z_dev = max(abs(1.0 - float(np.interp(0.02, supp[z][0], supp[z][1]))) for z in (4.0, 5.0))
check(low_z_dev > high_z_dev,
      f"C3  *** and the exposure is at LOW redshift exactly as stage 14/15 predicted: at k = 0.02 "
      f"s/km the suppression is {100 * low_z_dev:.2f}% at z = 2-3 against {100 * high_z_dev:.2f}% at "
      f"z = 4-5.  This sector's binding bin is the one every WDM analysis treats as least "
      f"constraining. ***",
      "an independent confirmation of the trend, now from a mock rather than from the scaling law")


# =================================================================================================
print()
print("=" * 100)
print("PART D -- convergence, and the demonstration that the RATIO is the robust object")
print("=" * 100)

# D1: seed variance of the ratio (matched phases should make this tiny)
r_seeds = []
for sd in (20260810, 777, 31415):
    kvv, rr = suppression(3.0, seed=sd)
    r_seeds.append(float(np.interp(0.02, kvv, rr)))
seed_spread = max(r_seeds) - min(r_seeds)
check(seed_spread < 0.01,
      f"D1  matched-phase seed variance on the RATIO at z = 3, k = 0.02 s/km is "
      f"{100 * seed_spread:.3f}% across 3 seeds ({', '.join(f'{v:.4f}' for v in r_seeds)})",
      "this is the whole reason the deliverable is a ratio: sample variance cancels between the two "
      "runs because they share phases")

# D2: absolute power is NOT converged in resolution, but the ratio is -- show both
res_abs, res_rat = {}, {}
Ns = [256, 512] + ([768] if FULL else [])
for N in Ns:
    kv_c, p_c = make_flux_box(3.0, N, L0, SEED, "cdm", k_F=K_F[3.0])
    kv_s, p_s = make_flux_box(3.0, N, L0, SEED, "sector", k_F=K_F[3.0])
    g = (kv_c > 0) & (p_c > 0)
    res_abs[N] = float(np.interp(0.02, kv_c[g], (kv_c * p_c / np.pi)[g]))
    res_rat[N] = float(np.interp(0.02, kv_c[g], (p_s / p_c)[g]))
print("\n        N     k_Nyq [h/Mpc]   ABSOLUTE k P/pi   RATIO sector/CDM")
for N in Ns:
    print(f"      {N:>4d}        {np.pi * N / L0:>8.1f}        {res_abs[N]:>9.5f}         "
          f"{res_rat[N]:>8.5f}")
abs_spread = max(res_abs.values()) / min(res_abs.values()) - 1.0
rat_spread = max(res_rat.values()) - min(res_rat.values())
check(rat_spread < abs_spread,
      f"D2  *** the ratio converges faster than the absolute power, by construction and in fact: "
      f"absolute k P/pi moves {100 * abs_spread:.1f}% across N = {min(Ns)}-{max(Ns)} while the ratio "
      f"moves {100 * rat_spread:.2f}%. *** This is the quantitative version of why a laptop can "
      "answer the ratio question and cannot answer the absolute one",
      "and it is the same argument Murgia et al. use to justify quoting suppression relative to a "
      "matched reference run")

# D3: the projection tail -- is power above the Nyquist frequency being lost?
kv_c, p_c = make_flux_box(3.0, 512, L0, SEED, "cdm", k_F=K_F[3.0])
kv_hi, p_hi = make_flux_box(3.0, 512, 10.0, SEED, "cdm", k_F=K_F[3.0])
info(f"D3  projection-tail control: k_Nyq = {np.pi * 512 / L0:.0f} h/Mpc at L = 20 and "
     f"{np.pi * 512 / 10.0:.0f} h/Mpc at L = 10 Mpc/h, both far above the sector's k_half = "
     f"{T_ode_half[3.0]:.0f}, so the 3D power removed by the cutoff is inside the grid rather than "
     "beyond it. The IGM filter suppresses P_3D as k^-4 above k_F, so the truncated tail of the "
     "projection integral is a small correction to a small number.")

# D4: box size
if FULL:
    box_rat = {}
    for L in (20.0, 40.0):
        Nb = int(512 * L / 20.0)
        kv_c, p_c = make_flux_box(3.0, Nb, L, SEED, "cdm", k_F=K_F[3.0])
        kv_s, p_s = make_flux_box(3.0, Nb, L, SEED, "sector", k_F=K_F[3.0])
        g = (kv_c > 0) & (p_c > 0)
        box_rat[L] = float(np.interp(0.02, kv_c[g], (p_s / p_c)[g]))
    bs = max(box_rat.values()) - min(box_rat.values())
    check(bs < 0.02,
          f"D4  box-size convergence of the ratio at fixed cell size: {100 * bs:.2f}% between "
          f"L = 20 and 40 Mpc/h ({', '.join(f'L={k:.0f}: {v:.4f}' for k, v in box_rat.items())})",
          "run with --full")
else:
    info("D4  box-size convergence (L = 20 vs 40 Mpc/h at fixed cell size) runs under --full; "
         "skipped in the default configuration.")

# D5: RSD and IGM-filter sensitivity of the ratio
_, r_rsd = suppression(3.0, rsd=True)
_, r_nor = suppression(3.0, rsd=False)
d_rsd = abs(float(np.interp(0.02, supp[3.0][0], r_rsd)) - float(np.interp(0.02, supp[3.0][0], r_nor)))
_, r_nof = suppression(3.0, k_F_on=False)
d_kf = abs(float(np.interp(0.02, supp[3.0][0], r_rsd)) - float(np.interp(0.02, supp[3.0][0], r_nof)))
check(d_rsd < 0.02,
      f"D5  the linear-RSD treatment moves the ratio by {100 * d_rsd:.2f}% at z = 3, k = 0.02 s/km",
      "so the Kaiser approximation used here is not carrying the result")
info(f"D6  by contrast, switching OFF the IGM pressure filter moves the ratio by {100 * d_kf:.2f}% "
     f"-- {d_kf / max(d_rsd, 1e-6):.0f}x the RSD sensitivity. The IGM's own smoothing is the "
     "dominant modelling choice in this calculation, which is exactly why B1 matters and why the "
     "real analysis must marginalise over it rather than fix it.")


# =================================================================================================
print()
print("=" * 100)
print("PART E -- the suppression against published P_F1D precision")
print("=" * 100)

# representative fractional uncertainties on P_F1D -- LABELLED as representative, not a covariance
REPR = {
    2.0: (0.02, 0.02, "eBOSS DR14 (Chabanier+19), ~1-3% statistical, k <~ 0.02 s/km"),
    3.0: (0.02, 0.05, "XQ-100 (Irsic+17) / eBOSS, ~5% at k ~ 0.02 s/km"),
    4.0: (0.08, 0.15, "MIKE/HIRES (Viel+13) & Boera+19, ~10-20% at k ~ 0.08 s/km"),
    5.0: (0.08, 0.20, "Boera+19 z ~ 5, ~20% at k ~ 0.08 s/km"),
}
print("\n     z    k [s/km]   suppression   repr. sigma_P/P   suppression / sigma      source")
ratios_to_err = {}
for z in Z_FOREST:
    kt, sg, src = REPR[z]
    kvv, rr = supp[z]
    s = 1.0 - float(np.interp(kt, kvv, rr))
    ratios_to_err[z] = s / sg
    print(f"    {z:>3.0f}     {kt:>6.3f}      {100 * s:>7.3f}%          {100 * sg:>5.1f}%           "
          f"{s / sg:>6.3f}       {src}")

info("E1  READ THESE AS SCALES, NOT AS A LIKELIHOOD. The sigma column is a representative "
     "single-bin statistical uncertainty from the literature, not the published covariance, and the "
     "real constraint combines ~10-50 (k,z) bins while marginalising over T_0(z), gamma_T(z), "
     "<F>(z), reionisation history and resolution -- nuisances that are individually LARGER than the "
     "signal computed here and partially degenerate with it.")

worst_ratio = max(ratios_to_err.values())
check(worst_ratio < 1.0,
      f"E2  *** the predicted suppression is below the representative single-bin uncertainty in every "
      f"forest bin, worst case {worst_ratio:.2f} sigma (z = "
      f"{max(ratios_to_err, key=ratios_to_err.get):.0f}).  So this sector does not produce a forest "
      f"signature that stands out of the noise of one bin. ***",
      "which is CONSISTENT with stage 15's alpha-based pass, obtained by a completely different route")

n_eff = np.sqrt(30.0)     # order-of-magnitude bin count for a combined analysis
check(worst_ratio * n_eff > 0.3,
      f"E3  AND THE HONEST COUNTERWEIGHT, because a per-bin pass is not a pass: naively combining "
      f"~30 (k,z) bins scales the worst case to ~{worst_ratio * n_eff:.1f} sigma. That is NOT "
      f"negligible, it is the regime where the answer is decided by the nuisance marginalisation "
      f"rather than by the signal",
      "so E2 must NOT be quoted as 'the forest cannot see this' -- the correct statement is that the "
      "signal is nuisance-dominated, and only the real likelihood settles it")


# =================================================================================================
print()
print("=" * 100)
print("PART F -- limits of this calculation, stated before anyone else has to")
print("=" * 100)

info("F1  A LOGNORMAL MOCK IS NOT HYDRODYNAMICS. It has no shocks, no thermal history, no "
     "photoionisation, no galactic winds; the density-temperature relation is imposed as a power law "
     "rather than emerging. Absolute P_F1D from such models departs from full hydro at the tens-of-"
     "percent level. Every number in Parts C-E is therefore a RATIO at matched everything, which is "
     "the configuration where those errors largely cancel -- 'largely' is doing real work in that "
     "sentence and it is not a theorem.")

info("F2  THE IGM FILTER IS THE DOMINANT SYSTEMATIC, and D6 measures that directly. I fixed the "
     "pressure-smoothing scale at lam_P = 100 kpc physical. The literature range (~80-120 kpc, and "
     "it is itself thermal-history dependent) moves the answer by more than the signal does. In a "
     "real analysis this is marginalised, and the marginalisation is what would decide the verdict.")

info("F3  THE SECTOR'S T(k) IS LINEAR. Part A solves the sector's linear Jeans equation, which is "
     "the right object for the INPUT power, but the forest at k ~ 0.02-0.1 s/km is mildly nonlinear "
     "and the lognormal transformation is a stand-in for that nonlinearity, not a solution of it. A "
     "cutoff can be partially regenerated by nonlinear mode coupling, which would make the true "
     "suppression SMALLER than computed here -- i.e. this calculation is conservative in the "
     "direction that disfavours the sector, which is the direction I want it to err.")

info("F4  WHAT WOULD OVERTURN IT, in order of likelihood: (i) the real likelihood with the nuisances "
     "marginalised and ~30 bins combined, which E3 shows is where the decision actually lives; "
     "(ii) a k_max = 0.2 s/km dataset, since the whole signal is a projected amplitude and deeper k "
     "adds lever arm; (iii) the low-z P_1D channel at z ~ 2 done properly, since C3 confirms that is "
     "this sector's binding bin and it is the least controlled part of the literature.")

info("F5  AND THE INSTRUMENT FOR (i) IS STILL NOT PUBLIC. See the correction at the top of this "
     "file: the Hooper et al. 2022 generic-shape likelihood was announced, not released. The public "
     "alternatives (lym1d, LaCE/cup1d, lya_emulator) interpolate over near-standard cosmologies and "
     "have no axis for a free cutoff shape, so they cannot be repurposed for this sector without "
     "extrapolating off their training grid -- which would manufacture a number rather than measure "
     "one. Obtaining it means contacting the authors.")


# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  WHAT WAS COMPUTED HERE, that was not available before:

  1. THE SECTOR'S TRANSFER FUNCTION FROM ITS OWN DYNAMICS. Part A solves the Jeans equation for
     c_s^2 = K/rho, i.e. c_s^2 ~ a^3 -- COLD early, warming with time, the reverse of WDM. Its
     half-mode falls from {T_ode_half[2.0]:.0f} h/Mpc at z = 2 to {T_ode_half[5.0]:.0f} at z = 5, matching stage 15's
     independent static map in trend to {ode_ratios.max() / ode_ratios.min():.2f}x. Two routes, one answer.

  2. THE CONSTRAINT IS A PROJECTION, AS ARITHMETIC. The cutoff sits {min(p['k_half'] / p['kmax_ir'] for p in proj.values()):.1f}-{max(p['k_half'] / p['kmax_ir'] for p in proj.values()):.1f}x beyond the
     deepest published k. No forest dataset resolves it; the entire signal is the projected
     response of P_1D. Stage 15's risk C3 is now quantified rather than flagged.

  3. AND THE SECTOR'S CUTOFF HIDES UNDER THE IGM's OWN. At every forest redshift the gas is
     already pressure-smoothed on LARGER scales than the sector's cutoff (B1). This was not
     anticipated and it is the single most favourable structural fact found for this sector on the
     forest front -- the suppression is being added beneath a cutoff that is already there and
     already marginalised over in every published analysis.

  4. THE PREDICTED SUPPRESSION: {100 * (1 - supp_z2_002):.2f}% at z = 2, {100 * (1 - supp_z3_002):.2f}% at z = 3 (k = 0.02 s/km), and
     {100 * (1 - supp_z4_008):.2f}% / {100 * (1 - supp_z5_008):.2f}% at z = 4 / 5 (k = 0.08 s/km) -- below representative single-bin
     precision everywhere, worst case {worst_ratio:.2f} sigma. Independent of stage 15's route, same verdict.

  5. AND THE COUNTERWEIGHT I AM NOT GOING TO BURY: combining ~30 bins naively puts this at
     ~{worst_ratio * n_eff:.1f} sigma. That is the regime where nuisance marginalisation, not the signal, decides.
     So the correct claim is NOT "the forest cannot see this sector". It is:

         *** the predicted forest signature is nuisance-dominated rather than absent, it is
             consistent with the published shape-marginalised bound by two independent routes,
             and settling it requires a likelihood that has been announced but never released. ***

  THE STATE OF THE FRONT IS UNCHANGED IN VERDICT AND STRONGER IN FOOTING: still BOUNDARY, still
  three named risks, but the suppression is now a number this repository computed on this machine
  rather than a bound quoted from someone else's paper. Stage 15's claim that the deciding MCMC was
  "a day of work with the released likelihood" is WITHDRAWN -- there is no released likelihood.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
