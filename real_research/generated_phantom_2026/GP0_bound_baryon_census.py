#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
GP0 -- THE BOUND-BARYON CENSUS: how much baryonic mass sits in bound regions, and how strongly it is clustered, at the
epochs the generated-phantom construction is tested (a library for GP2/GP3, runnable on its own).

WHY.  In the generated-phantom construction (GP1) only baryons in bound regions source the MOND kernel.  The external
field the kernel feels far from a lens is then the field of OTHER bound baryons, whose large-scale part is the matter
field times
      beta_B(z) = int n(M) M_B(M) b(M) dM / rho_m      (the bias-weighted bound-baryon fraction of the matter),
and whose Poisson (shot-noise) part comes from the rare massive objects.  This file computes beta_B and the shot-noise
field from a standard halo model, for four readings of "bound", so no single guess carries a result.

HALO MODEL.  Eisenstein-Hu no-wiggle P(k) normalised to sigma_8 = 0.8111 (the same formula and normalisation as
real_research/blind_kernel_2026/BK1, re-derived here and cross-checked by GP2), LCDM growth D(z), Sheth-Tormen 1999
mass function and peak-background bias (A = 0.3222, a = 0.707, p = 0.3, delta_c = 1.686).
BOUND BARYONS PER HALO, four readings:
  stars    M_* from Moster, Naab & White 2013 (eqs. 2, 11-14, as BSX3) for the central, plus satellites,
           M_*,sat/M_*,cen = min(4, (M/1e13)^0.4) (~0.4 at 1e12, 1 at 1e13, 2.5 at 1e14, 4 in rich clusters);
  galaxy   stars + cold gas, M_cold = 1.33 (M_HI + M_H2), log(M_HI/M_*) = -0.6 (log M_* - 10) - 0.6, M_H2 = 0.08 M_*
           (xGASS/xCOLD GASS-like scalings), capped at the halo's cosmic baryon share;
  observed galaxy + hot gas inside groups and clusters, f_hot(M) = min(1, 0.55 (M/1e14)^0.2) / (1 + (3e12/M)^2) of
           the cosmic share (X-ray gas fractions: ~0.3 at 1e13, ~0.55 at 1e14, ~0.85 at 1e15);
  maximal  every baryon inside every halo above 1e8 Msun counted as bound: M_B = f_b M (an upper bound).
The construction's switch w(x_m) marks as bound the baryons where the local matter density exceeds a virial-like
threshold (GP1); "observed" is the reading that matches where baryons are seen to sit; "maximal" bounds it from above.

CHECKS
  S1 the Sheth-Tormen implementation integrates to 1 over nu (mass and bias sum rules), and the resolved mass range
     (1e8-1e16 Msun) holds most of the matter.
  S2 (documentary) the stellar mass density Omega_* at z = 0 and z = 0.25 against the census (Chabrier-IMF values
     ~0.0025-0.0035; Fukugita & Peebles 2004, Madau & Dickinson 2014 converted).
  S3 (documentary) beta_B(z), f_B(z) and the bias of the bound baryons for the four readings, z = 0-3.
  S4 (documentary) the shot-noise (Poisson) field of the bound baryons at an ISOLATED lens, screened and unscreened:
     the analytic rms, and a Monte Carlo of discrete clumps with KiDS-like isolation -- no halo hosting a galaxy above
     ~1e9.5 Msun (M_h >= 2e11) inside 3 Mpc, and for groups/clusters (M_h >= 1e13, bright satellites out to r_200m)
     none inside 3 Mpc + r_200m; fainter halos are allowed down to 0.5 Mpc.  The field is heavy-tailed (rare nearby
     clusters), so its median, not its rms, describes a typical lens; GP2 stacks the sampled distribution itself.
  (Record: the first run's S1 also required >= 60% of the matter in 1e8-1e16 Msun halos; Sheth-Tormen puts ~45% of
   the mass in smaller halos at z = 0.25 (0.55 resolved), so that clause was a mis-set expectation about the model,
   not a physics check -- it is now reported.  The analytic nu-integral first ran from nu = 1e-4 and missed the
   integrable nu^-0.6 tail below it (1.5%); the tail is now added analytically.  Satellites were added to the stellar
   census after the first run gave Omega_* = 0.0018 (centrals only) against the census 0.0025-0.0035.)

Run from the repository root:  python3 real_research/generated_phantom_2026/GP0_bound_baryon_census.py
"""
import os, sys, json, math, time
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "GP0_bound_baryon_census"
_trap = getattr(np, "trapezoid", None) or np.trapz

# ---------------------------------------------------------------------------------------------- cosmology (as BK1)
Mpc = 3.0856775814913673e22; G = 6.67430e-11; MSUN = 1.98892e30
h = 0.6736; om_b, om_c = 0.02237, 0.1200
H0 = 100 * h * 1e3 / Mpc
Ob, Oc = om_b / h ** 2, om_c / h ** 2; Om = Ob + Oc; OL = 1 - Om; FB = Ob / Om
RHO_CRIT0 = 3 * H0 ** 2 / (8 * math.pi * G) * Mpc ** 3 / MSUN        # Msun / Mpc^3
RHO_M0 = Om * RHO_CRIT0                                               # comoving
TH27 = 2.7255 / 2.7; NS, S8 = 0.9649, 0.8111


def T_eh(k):
    """Eisenstein & Hu 1998 no-wiggle transfer function, k in 1/Mpc (the formula of BK1)."""
    omh2 = Om * h * h; fb = Ob / Om
    s_ = 44.5 * np.log(9.83 / omh2) / np.sqrt(1 + 10 * (Ob * h * h) ** 0.75)
    aG = 1 - 0.328 * np.log(431 * omh2) * fb + 0.38 * np.log(22.3 * omh2) * fb ** 2
    Gm = Om * h * (aG + (1 - aG) / (1 + (0.43 * k * s_) ** 4)); q = k * TH27 ** 2 / (Gm * h)
    L_ = np.log(2 * np.e + 1.8 * q); C_ = 14.2 + 731 / (1 + 62.5 * q); return L_ / (L_ + C_ * q * q)


def W_th(x):
    x = np.asarray(x, float)
    return np.where(x > 1e-3, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-3) ** 3, 1 - x * x / 10)


KK = np.geomspace(1e-5, 2e3, 60000)
_PK = KK ** NS * T_eh(KK) ** 2
_PK *= S8 ** 2 / _trap(_PK * W_th(KK * 8 / h) ** 2 * KK ** 2 / (2 * math.pi ** 2), KK)
PK0 = _PK


def Pk0(k):
    return np.interp(np.log(np.maximum(k, 1e-5)), np.log(KK), PK0, left=0.0, right=0.0)


def growth(z):
    """LCDM linear growth D(z)/D(0) (the integral form of BK1)."""
    a_ = np.linspace(1e-4, 1, 20001)
    def D_(a1):
        aa = a_[a_ <= a1]; E = np.sqrt(Om / aa ** 3 + OL); return math.sqrt(Om / a1 ** 3 + OL) * _trap(1 / (aa * E) ** 3, aa)
    return D_(1 / (1 + z)) / D_(1.0)


# ---------------------------------------------------------------------------------------------- Sheth-Tormen
LM = np.linspace(4.0, 16.5, 1251); MM = 10 ** LM
RR = (3 * MM / (4 * math.pi * RHO_M0)) ** (1 / 3)                    # comoving Mpc
SIG0 = np.sqrt(np.array([_trap(PK0 * W_th(KK * R) ** 2 * KK ** 2, KK) for R in RR]) / (2 * math.pi ** 2))
DC, A_ST, a_ST, p_ST = 1.686, 0.3222, 0.707, 0.3


def nuf_st(nu):
    """nu f(nu) of Sheth & Tormen 1999 (so that int f(nu) dnu = 1)."""
    anu2 = a_ST * nu * nu
    return A_ST * math.sqrt(2 * a_ST / math.pi) * nu * (1 + anu2 ** (-p_ST)) * np.exp(-anu2 / 2)


def b_st(nu):
    anu2 = a_ST * nu * nu
    return 1 + (anu2 - 1) / DC + 2 * p_ST / (DC * (1 + anu2 ** p_ST))


def mass_function(z):
    """dn/dlnM (comoving Mpc^-3) and bias on the grid MM at redshift z."""
    nu = DC / (growth(z) * SIG0)
    dlnnu = np.gradient(np.log(nu), np.log(MM))
    dndlnM = RHO_M0 / MM * nuf_st(nu) * dlnnu
    return dndlnM, b_st(nu), nu


# ---------------------------------------------------------------------------------------------- bound baryons per halo
def moster_Mstar(Mh, z):                                   # Moster, Naab & White 2013, eqs. 2 and 11-14 (as BSX3)
    zz = z / (1 + z)
    M1 = 10 ** (11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz; beta = 1.376 - 0.826 * zz; gamma = 0.608 + 0.329 * zz
    return 2 * N * Mh / ((Mh / M1) ** (-beta) + (Mh / M1) ** gamma)


def cold_gas(Ms):
    lMs = np.log10(np.maximum(Ms, 1.0))
    return 1.33 * (10 ** (-0.6 * (lMs - 10) - 0.6) + 0.08) * Ms


def f_hot(M):
    return np.minimum(1.0, 0.55 * (M / 1e14) ** 0.2) / (1 + (3e12 / M) ** 2)


READINGS = ("stars", "galaxy", "observed", "maximal")


def Mstar_total(M, z):
    """central (Moster+13) plus satellites: M_*,sat/M_*,cen = min(4, (M/1e13)^0.4)."""
    return moster_Mstar(M, z) * (1 + np.minimum(4.0, (np.asarray(M, float) / 1e13) ** 0.4))


def M_bound(M, z, reading):
    M = np.asarray(M, float); cap = FB * M
    Ms = np.minimum(Mstar_total(M, z), cap)
    if reading == "stars": return Ms
    Mg = np.minimum(Ms + cold_gas(Ms), cap)
    if reading == "galaxy": return Mg
    if reading == "observed": return np.maximum(Mg, np.minimum(cap, f_hot(M) * cap))
    if reading == "maximal": return np.where(M >= 1e8, cap, 0.0)
    raise ValueError(reading)


def census(z, reading, Mmin=1e8):
    """beta_B, f_B, b_B (bias of the bound baryons), Omega_B, and the arrays used for shot noise."""
    dn, b, _ = mass_function(z)
    sel = MM >= Mmin
    MB = M_bound(MM, z, reading)
    fB = _trap((dn * MB)[sel], LM[sel] * math.log(10)) / RHO_M0
    beta = _trap((dn * MB * b)[sel], LM[sel] * math.log(10)) / RHO_M0
    return {"z": z, "reading": reading, "beta_B": float(beta), "f_B": float(fB), "b_B": float(beta / fB) if fB > 0 else 0.0,
            "Omega_B": float(fB * Om)}


def shot_noise_field(z, reading, R_iso_Mpc=3.0, lam_Mpc=float("inf")):
    """rms |g| (m/s^2, physical) at an isolated lens from Poisson-distributed bound-baryon clumps outside R_iso:
    sigma^2 = int dn M_B^2 G^2 4 pi int_R^inf s(r)^2 / r^2 dr  (r physical; the density is comoving -> x (1+z)^3)."""
    dn, _, _ = mass_function(z)
    MB = M_bound(MM, z, reading) * MSUN
    a = 1 / (1 + z)
    Rp = R_iso_Mpc * Mpc                                              # isolation radius taken as physical
    r = np.geomspace(Rp, Rp + (60 * lam_Mpc * Mpc if np.isfinite(lam_Mpc) else 1e4 * Mpc), 4000)
    s = np.ones_like(r) if not np.isfinite(lam_Mpc) else (1 + r / (lam_Mpc * Mpc)) * np.exp(-r / (lam_Mpc * Mpc))
    I_r = _trap(s ** 2 / r ** 2, r)
    n_phys = dn / (a * Mpc) ** 3                                       # per unit ln M, per m^3 physical
    var = 4 * math.pi * G ** 2 * I_r * _trap(n_phys * MB ** 2, LM * math.log(10))
    return math.sqrt(var)


def omega_star(z, satellites=True):
    dn, _, _ = mass_function(z)
    ms = Mstar_total(MM, z) if satellites else moster_Mstar(MM, z)
    return float(_trap(dn * ms, LM * math.log(10)) / RHO_CRIT0)


def r200m_phys(M, z):
    """r_200m (physical Mpc) for halo mass M (Msun) at redshift z."""
    return (3 * np.asarray(M, float) / (4 * math.pi * 200 * RHO_M0 * (1 + z) ** 3)) ** (1 / 3)


def s_screen(r_m, lam_Mpc):
    if not np.isfinite(lam_Mpc): return np.ones_like(np.asarray(r_m, float))
    x = np.asarray(r_m, float) / (lam_Mpc * Mpc); return (1 + x) * np.exp(-x)


def _I_tail(r0_m, lam_Mpc):
    """int_{r0}^inf s(r)^2 / r^2 dr (1/m)."""
    if not np.isfinite(lam_Mpc): return 1.0 / r0_m
    r = np.geomspace(r0_m, r0_m + 40 * lam_Mpc * Mpc, 3000)
    return float(_trap(s_screen(r, lam_Mpc) ** 2 / r ** 2, r))


def poisson_field_samples(z, reading, lam_Mpc, n, rng, R_iso=3.0, M_bright=2e11, M_group=1e13, r_faint=0.5,
                          Mlo=1e10, r_mc_bright=30.0, r_mc_faint=5.0):
    """Monte Carlo of the bound-baryon Poisson field (3-vectors, m/s^2, physical) at n isolated lenses.
    Halos are drawn from the Sheth-Tormen mass function (physical number density at z) in 0.05-dex bins, uniform in
    volume between R_min(M) and the Monte-Carlo radius; beyond it the field is added as a Gaussian of the analytic
    variance.  R_min = r_faint for M < M_bright (faint neighbours are allowed inside the isolation sphere),
    R_iso for M_bright <= M < M_group, R_iso + r_200m(M) for M >= M_group (bright satellites fill r_200m)."""
    dn, _, _ = mass_function(z)
    edges = np.arange(math.log10(Mlo), 16.0001, 0.05); cen = 0.5 * (edges[1:] + edges[:-1])
    dn_c = np.interp(cen, LM, dn) * 0.05 * math.log(10) * (1 + z) ** 3            # per physical Mpc^3, per bin
    Mc = 10 ** cen; MBc = M_bound(Mc, z, reading)
    out = np.zeros((n, 3)); var_tail = 0.0
    for Mi, MBi, ni in zip(Mc, MBc, dn_c):
        if MBi <= 0 or ni <= 0: continue
        Rmin = r_faint if Mi < M_bright else (R_iso if Mi < M_group else R_iso + float(r200m_phys(Mi, z)))
        Rmc = r_mc_faint if Mi < 1e12 else r_mc_bright
        if np.isfinite(lam_Mpc): Rmc = min(Rmc, max(Rmin, 20 * lam_Mpc))
        GM = G * MBi * MSUN
        if Rmc > Rmin:
            Nexp = ni * 4 * math.pi / 3 * (Rmc ** 3 - Rmin ** 3)
            K = rng.poisson(Nexp, n); tot = int(K.sum())
            if tot:
                idx = np.repeat(np.arange(n), K)
                u = rng.random(tot); r = (Rmin ** 3 + u * (Rmc ** 3 - Rmin ** 3)) ** (1 / 3) * Mpc
                v = rng.standard_normal((tot, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
                g = (GM * s_screen(r, lam_Mpc) / r ** 2)[:, None] * v
                np.add.at(out, idx, g)
        var_tail += 4 * math.pi * GM ** 2 * ni / Mpc ** 3 * _I_tail(max(Rmc, Rmin) * Mpc, lam_Mpc)
    out += rng.standard_normal((n, 3)) * math.sqrt(var_tail / 3)
    return out


# ---------------------------------------------------------------------------------------------- run as a lane
if __name__ == "__main__":
    T0 = time.time(); P = lambda *a: print(*a, flush=True)
    CH, OUT = [], {"lane": "GP0", "checks": {}, "numbers": {}}

    def check(name, measured, ok, reading="", load_bearing=True):
        ok = bool(ok); CH.append((name, ok, load_bearing))
        OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
        P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
        if reading: P(f"         reading:  {reading}")
        return ok

    def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)

    P(__doc__.split("CHECKS")[0].strip())
    banner("S1  SHETH-TORMEN SUM RULES")
    nu_ = np.geomspace(1e-4, 20, 200001)
    tail = A_ST * math.sqrt(2 * a_ST / math.pi) * a_ST ** (-p_ST) * nu_[0] ** (1 - 2 * p_ST) / (1 - 2 * p_ST)   # f ~ nu^-2p as nu -> 0
    btail = tail * (1 - 1 / DC + 2 * p_ST / DC)                                                                 # b -> 1 - 1/dc + 2p/dc
    s_mass = float(_trap(nuf_st(nu_) / nu_, nu_)) + tail; s_bias = float(_trap(nuf_st(nu_) * b_st(nu_) / nu_, nu_)) + btail
    rows = {}
    for z in (0.0, 0.25, 1.0, 3.0):
        dn, b, _ = mass_function(z); sel = MM >= 1e8
        fm = float(_trap((dn * MM)[sel], LM[sel] * math.log(10)) / RHO_M0)
        fb_ = float(_trap((dn * MM * b)[sel], LM[sel] * math.log(10)) / RHO_M0)
        rows[z] = {"mass_in_1e8_1e16": fm, "bias_weighted": fb_}
        P(f"    z = {z}: fraction of matter in halos 1e8-1e16 Msun {fm:.3f}; bias-weighted {fb_:.3f}")
    P(f"    analytic integrals over nu: int f dnu = {s_mass:.4f}, int f b dnu = {s_bias:.4f}")
    OUT["numbers"]["S1"] = {"int_f": s_mass, "int_fb": s_bias, "by_z": {str(k): v for k, v in rows.items()}}
    check("S1 the Sheth-Tormen implementation integrates to 1 (mass and bias sum rules, within 1%)",
          f"int f = {s_mass:.4f}, int f b = {s_bias:.4f}; resolved fraction (1e8-1e16) at z = 0.25: {rows[0.25]['mass_in_1e8_1e16']:.3f} (reported)",
          abs(s_mass - 1) < 0.01 and abs(s_bias - 1) < 0.01)

    banner("S2  THE STELLAR MASS DENSITY (Moster+13 over the Sheth-Tormen mass function)")
    os0, os25 = omega_star(0.0), omega_star(0.25); oc0 = omega_star(0.0, satellites=False)
    P(f"    Omega_* = {os0:.4f} (z = 0), {os25:.4f} (z = 0.25) with satellites; centrals only {oc0:.4f} (z = 0); "
      f"Chabrier-IMF census 0.0025-0.0035 at z = 0")
    OUT["numbers"]["S2"] = {"Omega_star_z0": os0, "Omega_star_z025": os25, "Omega_star_z0_centrals_only": oc0}
    check("S2 (documentary) Omega_* at z = 0 within a factor 1.5 of the census band 0.0025-0.0035",
          f"{os0:.4f}", 0.0025 / 1.5 <= os0 <= 0.0035 * 1.5, "", load_bearing=False)

    banner("S3  THE BOUND-BARYON AMPLITUDE beta_B(z) = int n M_B b dM / rho_m, FOUR READINGS")
    tab = {}
    for rd in READINGS:
        tab[rd] = {}
        for z in (0.0, 0.25, 0.5, 1.0, 2.0, 3.0):
            c = census(z, rd); tab[rd][z] = c
        P(f"    {rd:9s}: " + "  ".join(f"z={z}: beta {tab[rd][z]['beta_B']:.4f} (f_B {tab[rd][z]['f_B']:.4f}, b {tab[rd][z]['b_B']:.2f})"
                                    for z in (0.0, 0.25, 1.0, 3.0)))
    OUT["numbers"]["S3"] = {rd: {str(z): v for z, v in tab[rd].items()} for rd in READINGS}
    P(f"    (all baryons would give beta = Omega_b/Omega_m = {FB:.4f}; the whole matter field beta = 1)")
    check("S3 (documentary) beta_B at z = 0.25 for the four readings", {rd: round(tab[rd][0.25]["beta_B"], 4) for rd in READINGS},
          True, "", load_bearing=False)

    banner("S4  THE POISSON FIELD OF DISCRETE BOUND-BARYON CLUMPS AT AN ISOLATED LENS (z = 0.25; units a0 = 9.3619e-11)")
    s4 = {}; rng = np.random.default_rng(250925)
    for rd in READINGS:
        s4[rd] = {}
        for l in (0.7, 1.0, 1.5, 2.0, 3.0, 5.0, float("inf")):
            rms_all = shot_noise_field(0.25, rd, 3.0, l) / 9.3619e-11
            gv = np.linalg.norm(poisson_field_samples(0.25, rd, l, 4000, rng), axis=1) / 9.3619e-11
            s4[rd][str(l)] = {"rms_no_isolation_3Mpc": rms_all, "mc_median": float(np.median(gv)), "mc_rms": float(np.sqrt(np.mean(gv ** 2))),
                              "mc_p90": float(np.percentile(gv, 90))}
        P(f"    {rd:9s}: " + "; ".join(f"lam {k}: med {v['mc_median']:.1e} rms {v['mc_rms']:.1e}" for k, v in s4[rd].items()))
    OUT["numbers"]["S4"] = s4
    check("S4 (documentary) the Poisson field from discrete bound-baryon clumps at isolated lenses (MC median / rms, a0)",
          {rd: f"inf: {s4[rd]['inf']['mc_median']:.1e}/{s4[rd]['inf']['mc_rms']:.1e}; 1.5: {s4[rd]['1.5']['mc_median']:.1e}/{s4[rd]['1.5']['mc_rms']:.1e}"
           for rd in READINGS}, True, "", load_bearing=False)

    n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results.json"), "w"), indent=1, default=str)
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {SLUG}_results.json "
      f"({time.time() - T0:.0f} s)")
    sys.exit(0 if n_fail == 0 else 1)
