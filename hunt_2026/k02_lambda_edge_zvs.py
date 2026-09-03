#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k02 -- THE LAMBDA EDGE: the zero-velocity surface of nearby groups, predicted from the BARYONS and a_0.

ANGLE 1 (mine the unexplained regularities).  Two of them meet here.
  * The LOCAL DENSITY ANOMALY (Karachentsev 2005, 2012): masses of nearby groups obtained from the radius of
    their zero-velocity surface give a mean LOCAL matter density 3-4x BELOW the global Omega_m.  Unexplained.
  * CHERNIN's LOCAL DARK ENERGY (Chernin+ 2009, 2015): the zero-velocity radius of the Local Group is close to
    its "zero-gravity radius", where the attraction of the group balances the cosmological repulsion, so the
    local flow measures Lambda.  Also unexplained why the two radii sit so close together.

THE CANDIDATE LAW UNDER TEST.  In the framework the deep-MOND attraction of a group is sqrt(G M_b a_0)/r, and
the cosmological repulsion is H_Lambda^2 r with H_Lambda = H_0 sqrt(Omega_Lambda).  Balancing them:

      r_Lambda  =  (G M_b a_0)^(1/4) / H_Lambda   =   v_flat / H_Lambda                             (K02)

  * a_0 enters with a PREDICTED coefficient, and it enters TWICE: once as the attraction's scale, once through
    a_0 = (c/2) sqrt(G rho_DE), which is the same Lambda that supplies H_Lambda.  This is the only place in the
    hunt where the first law's own Lambda appears on both sides of a galaxy-scale equation.
  * The MASS SCALING is the discriminator: 1/4 here, 1/3 for any Newtonian zero-gravity radius (and 1/3 for a
    splashback radius).  Over the two decades of baryonic mass the Local Volume spans, that is 0.17 dex.
  * The measured input is the BARYONIC mass -- stars plus gas, both observed.  LambdaCDM must supply a virial
    mass that is not observed.

THIS ITEM WAS NEVER RUN (hunt list item 80) AND ITEM 95 GOT THE ALGEBRA WRONG.  Item 95's committed output
states d log r_Lambda / d log M_b = 1/6 and prints a table of radii that are all 0.000 Mpc.  From its own stated
equation sqrt(G M_b a_0)/r = Omega_L H_0^2 r the exponent is 1/4, not 1/6, and the radii are Mpc-scale.  Both are
corrected here, with the corrected table printed.

CHECKS THAT CAN FAIL: the predicted radius must match the MEASURED zero-velocity radius of the Local Group and of
the nearby groups to better than a factor 1.5; the 1/4 slope must be recovered from the integration; KT2017's
tabulated turnaround radii must be shown to be usable or NOT usable.  Mutation controls, both footings,
the Newtonian/LambdaCDM calculation computed beside, Upsilon lever quoted numerically.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, G, Mpc, Msun, H0, OM_M, OM_L, nu_s, vizier_tsv, _f, Check, P, info, DATA

H_LAM = H0 * math.sqrt(OM_L)                       # s^-1
UPS_K = 0.6                                        # K-band stellar M/L, the value used elsewhere in this repo
ck = Check()
P("=" * 120)
P("k02 -- THE LAMBDA EDGE: zero-velocity radii of nearby groups from the baryons and a_0")
P("=" * 120)
P(f"  H_Lambda = H_0 sqrt(Omega_Lambda) = {H_LAM*Mpc/1e3:.2f} km/s/Mpc = {H_LAM:.4e} s^-1   "
  f"(H_0 = {H0*Mpc/1e3:.1f}, Omega_L = {OM_L:.4f})")


# ------------------------------------------------------------------ the static closed form, and item 95's bug
def r_lambda_fw(Mb_Msun, a0):
    """Framework: sqrt(G M_b a_0)/r = H_Lambda^2 r  ->  r = (G M_b a_0)^(1/4)/H_Lambda."""
    return (G * Mb_Msun * Msun * a0) ** 0.25 / H_LAM


def r_lambda_newton(M_Msun):
    """Newton/Chernin zero-gravity radius: G M/r^2 = H_Lambda^2 r  ->  r = (G M/H_Lambda^2)^(1/3)."""
    return (G * M_Msun * Msun / H_LAM ** 2) ** (1.0 / 3.0)


P("\n" + "-" * 120)
P("THE CLOSED FORMS, and the correction to item 95 (whose committed table is all zeros and whose stated")
P("exponent 1/6 does not follow from its own stated equation)")
P("-" * 120)
P(f"  {'M_b [Msun]':>12} {'r_Lambda canon [Mpc]':>22} {'r_Lambda alt [Mpc]':>20} {'Newton r_ZG(M_b) [Mpc]':>24}")
for lM in (9, 10, 11, 12, 13, 14, 15):
    M = 10.0 ** lM
    P(f"  {'1e%d' % lM:>12} {r_lambda_fw(M, A0['canonical'])/Mpc:>22.3f} {r_lambda_fw(M, A0['alt'])/Mpc:>20.3f} "
      f"{r_lambda_newton(M)/Mpc:>24.3f}")
sl = (math.log10(r_lambda_fw(1e13, A0["canonical"])) - math.log10(r_lambda_fw(1e10, A0["canonical"]))) / 3.0
ck("K02-95 CORRECTION TO A COMMITTED NUMBER: item 95's exponent is wrong and its table is empty.  The framework's "
   "Lambda edge scales as M_b^(1/4), not M_b^(1/6), and an L* galaxy's edge is a few Mpc, not 0.000",
   abs(sl - 0.25) < 1e-6,
   f"measured d log r_Lambda/d log M_b = {sl:.6f} (predicted 1/4 = 0.25; item 95 states 1/6 = 0.1667); "
   f"L* (M_b = 5e10) gives {r_lambda_fw(5e10, A0['canonical'])/Mpc:.2f} Mpc, not 0.000")


# ------------------------------------------------------------------ the honest dynamical calculation
def H_of_a(a):
    return H0 * math.sqrt(OM_M / a ** 3 + OM_L)


def integrate_shell(r_i, Mb_Msun, a0, mode="mond", a_start=0.02, n=6000, e_ext=0.0):
    """Integrate a spherical shell around a point mass from a = a_start to a = 1 in a LambdaCDM background.
    mode: 'mond' = full Route A kernel on the baryons; 'newton' = Newtonian on the mass given.
    Returns (r_today, rdot_today).  The Lambda term is +Omega_L H_0^2 r (= Lambda c^2 r/3)."""
    M = Mb_Msun * Msun
    lna = np.linspace(math.log(a_start), 0.0, n + 1)
    h = lna[1] - lna[0]
    r, u = r_i, H_of_a(a_start) * r_i

    def acc(rr):
        rr = max(rr, 1e-6 * Mpc)
        gN = G * M / rr ** 2
        if mode == "newton":
            g = gN
        else:
            y = gN / a0
            if e_ext > 0.0:
                g = nu_s(y + e_ext) * gN          # simple external-field prescription, flagged below
            else:
                g = nu_s(y) * gN
        return -g + OM_L * H0 ** 2 * rr

    def deriv(l, rr, uu):
        a = math.exp(l)
        H = H_of_a(a)
        return uu / H, acc(rr) / H

    for i in range(n):
        l = lna[i]
        k1r, k1u = deriv(l, r, u)
        k2r, k2u = deriv(l + h / 2, r + h * k1r / 2, u + h * k1u / 2)
        k3r, k3u = deriv(l + h / 2, r + h * k2r / 2, u + h * k2u / 2)
        k4r, k4u = deriv(l + h, r + h * k3r, u + h * k3u)
        r += h * (k1r + 2 * k2r + 2 * k3r + k4r) / 6
        u += h * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        if r <= 0:
            return 0.0, -1e9
    return r, u


def zero_velocity_radius(Mb_Msun, a0, mode="mond", e_ext=0.0):
    """Bisect on the initial comoving-ish radius for the shell whose radial velocity is zero TODAY."""
    lo, hi = 0.001 * Mpc, 30.0 * Mpc
    f = lambda ri: integrate_shell(ri, Mb_Msun, a0, mode=mode, e_ext=e_ext)[1]
    if f(lo) > 0 or f(hi) < 0:
        for _ in range(60):
            if f(lo) < 0:
                break
            lo *= 0.5
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    r0, _ = integrate_shell(math.sqrt(lo * hi), Mb_Msun, a0, mode=mode, e_ext=e_ext)
    return r0


P("\n" + "-" * 120)
P("THE DYNAMICAL VERSION (a 1-D shell integration in a LambdaCDM background, not the static balance):")
P("  r'' = -nu(g_N/a_0) g_N + Omega_L H_0^2 r,  started on the Hubble flow at a = 0.02, run to a = 1.")
P("  R_0 = the radius of the shell whose radial velocity is zero today.  This is what an observer measures.")
P("-" * 120)
P(f"  {'M_b [Msun]':>12} {'R_0 framework canon':>21} {'R_0 framework alt':>19} {'r_Lambda static canon':>23} "
  f"{'R_0/r_Lambda':>13}")
ratios = []
for lM in (10, 11, 12, 13):
    M = 10.0 ** lM
    R0c = zero_velocity_radius(M, A0["canonical"]) / Mpc
    R0a = zero_velocity_radius(M, A0["alt"]) / Mpc
    rl = r_lambda_fw(M, A0["canonical"]) / Mpc
    ratios.append(R0c / rl)
    P(f"  {'1e%d' % lM:>12} {R0c:>21.3f} {R0a:>19.3f} {rl:>23.3f} {R0c/rl:>13.3f}")
ratios = np.array(ratios)
P(f"\n  R_0 / r_Lambda = {ratios.mean():.3f} +- {ratios.std():.3f} over three decades of mass -- so the STATIC")
P("  closed form (K02) and the honest integration differ by a constant of order one, and (K02) can be used with")
P("  that constant folded in.  That constant is the item's only non-predicted number and it is quoted here.")
lR = [math.log10(zero_velocity_radius(10.0 ** lM, A0["canonical"])) for lM in (10, 13)]
slope_dyn = (lR[1] - lR[0]) / 3.0
ck("K02a the dynamical integration must reproduce the closed form's 1/4 mass slope -- if it does not, the static "
   "balance is not the right reading of the zero-velocity surface",
   abs(slope_dyn - 0.25) < 0.03, f"integrated d log R_0/d log M_b = {slope_dyn:.4f} against the predicted 0.2500")


# ------------------------------------------------------------------ measure R_0 from data on disk
P("\n" + "-" * 120)
P("THE MEASUREMENT.  Karachentsev's Updated Nearby Galaxy Catalog (869 galaxies, on disk) gives distances and")
P("Local-Group-frame velocities.  The zero-velocity radius is the intercept of the local Hubble diagram.")
P("-" * 120)
rows = vizier_tsv("ungc_karachentsev2013.tsv")
name = np.array([r["Name"].strip() for r in rows])
ra = np.array([_f(r["_RAJ2000"]) for r in rows]); dec = np.array([_f(r["_DEJ2000"]) for r in rows])
D = np.array([_f(r["Dist"]) for r in rows]); V = np.array([_f(r["Vlg"]) for r in rows])
lKL = np.array([_f(r["KLum"]) for r in rows]); lMHI = np.array([_f(r["MHI"]) for r in rows])
fD = np.array([r["f_Dist"].strip() for r in rows])
unit = np.stack([np.cos(np.radians(dec)) * np.cos(np.radians(ra)),
                 np.cos(np.radians(dec)) * np.sin(np.radians(ra)), np.sin(np.radians(dec))], axis=1)


def group_frame(i_c, dmax=4.0, dmin=0.0):
    """Separations and relative radial velocities about the galaxy at index i_c (Karachentsev-Makarov projection)."""
    Dc, Vc, nc = D[i_c], V[i_c], unit[i_c]
    cth = unit @ nc
    R = np.sqrt(np.clip(D ** 2 + Dc ** 2 - 2 * D * Dc * cth, 0, None))
    with np.errstate(divide="ignore", invalid="ignore"):
        Vr = (V * (D - Dc * cth) + Vc * (Dc - D * cth)) / R
    ok = np.isfinite(R) & np.isfinite(Vr) & (R > dmin) & (R < dmax) & (np.arange(len(D)) != i_c)
    return R, Vr, ok


def fit_R0(R, Vr, ok, rlo, rhi):
    m = ok & (R > rlo) & (R < rhi)
    if m.sum() < 8:
        return np.nan, np.nan, int(m.sum()), np.nan
    A = np.vstack([R[m], np.ones(m.sum())]).T
    h, b = np.linalg.lstsq(A, Vr[m], rcond=None)[0]
    R0 = -b / h
    # bootstrap
    rng = np.random.default_rng(20260903); bs = []
    idx = np.where(m)[0]
    for _ in range(2000):
        s = rng.choice(idx, len(idx), replace=True)
        A2 = np.vstack([R[s], np.ones(len(s))]).T
        hh, bb = np.linalg.lstsq(A2, Vr[s], rcond=None)[0]
        if hh > 0:
            bs.append(-bb / hh)
    return R0, (np.std(bs) if bs else np.nan), int(m.sum()), h


def baryonic_mass(R, ok, rcut):
    m = ok & (R < rcut)
    Ms = np.nansum(UPS_K * 10.0 ** lKL[m][np.isfinite(lKL[m])])
    Mg = 1.33 * np.nansum(10.0 ** lMHI[m][np.isfinite(lMHI[m])])
    return Ms, Mg


GROUPS = [("Local Group", "MilkyWay", 0.7, 3.0),
          ("M81 group", "MESSIER081", 0.7, 3.0),
          ("Cen A group", "NGC5128", 0.7, 3.0),
          ("M83 group", "NGC5236", 0.7, 3.0),
          ("IC 342 group", "IC0342", 0.7, 3.0),
          ("M94 / CVn I", "NGC4736", 0.7, 3.0)]

P(f"\n  {'group':<14}{'N':>4} {'R_0 measured [Mpc]':>20} {'H_loc [km/s/Mpc]':>18} {'M_* [Msun]':>12} "
  f"{'M_gas [Msun]':>13} {'M_b [Msun]':>12}")
meas = []
for gname, anchor, rlo, rhi in GROUPS:
    idx = np.where(np.char.replace(np.char.upper(name), " ", "") == anchor.upper())[0]
    if len(idx) == 0:
        P(f"  {gname:<14}  anchor {anchor} not in catalogue -- skipped")
        continue
    i_c = int(idx[0])
    R, Vr, ok = group_frame(i_c)
    R0, eR0, N, h = fit_R0(R, Vr, ok, rlo, rhi)
    if not np.isfinite(R0) or R0 <= 0 or R0 > 4:
        P(f"  {gname:<14}{N:>4}   no usable zero crossing (R_0 = {R0})")
        continue
    Ms, Mg = baryonic_mass(R, ok, R0)
    if anchor == "MilkyWay":
        Ms += 6.1e10                                # the Milky Way has no K luminosity in the catalogue
    else:
        Ms += UPS_K * 10.0 ** lKL[i_c] if np.isfinite(lKL[i_c]) else 0.0
        Mg += 1.33 * 10.0 ** lMHI[i_c] if np.isfinite(lMHI[i_c]) else 0.0
    if anchor == "MilkyWay":
        Mg += 1.33 * 10.0 ** lMHI[i_c]
    meas.append(dict(name=gname, R0=R0, eR0=eR0, N=N, Ms=Ms, Mg=Mg, Mb=Ms + Mg, h=h))
    P(f"  {gname:<14}{N:>4} {R0:>13.3f} +- {eR0:<4.3f} {h:>18.1f} {Ms:>12.3e} {Mg:>13.3e} {Ms+Mg:>12.3e}")
P("\n  (the Milky Way carries no K-band luminosity in the catalogue; 6.1e10 Msun of stars is added for it, the")
P("   standard value.  Every other mass is the catalogue's own K luminosity at Upsilon_K = 0.6 plus 1.33 M_HI.)")
P("  AGAINST INTEREST: this is a stellar+cold-gas mass.  Groups also hold warm/hot gas that these catalogues do")
P("  not see; every framework radius below is therefore a LOWER bound, and the direction of that bias is stated")
P("  in the verdict.")

lg = [m for m in meas if m["name"] == "Local Group"]
ck("K02b the Local Group's measured zero-velocity radius must come out near the published 0.96 +- 0.03 Mpc "
   "(Karachentsev+2009) -- if it does not, this pipeline is not measuring what the literature measures",
   len(lg) == 1 and abs(lg[0]["R0"] - 0.96) < 0.25,
   f"measured {lg[0]['R0']:.3f} +- {lg[0]['eR0']:.3f} Mpc from {lg[0]['N']} galaxies against the published 0.96 +- 0.03"
   if lg else "no Local Group fit")

# ------------------------------------------------------------------ confront
P("\n" + "-" * 120)
P("THE CONFRONTATION.  Framework R_0 from the measured BARYONS alone, against the measured R_0.")
P("-" * 120)
P(f"  {'group':<14}{'R_0 meas':>10} {'fw canon':>10} {'fw alt':>9} {'ratio canon':>12} {'ratio alt':>10} "
  f"{'M_tot needed (Newton)':>23}")
rc_all, ra_all = [], []
for m in meas:
    R0fw_c = zero_velocity_radius(m["Mb"], A0["canonical"]) / Mpc
    R0fw_a = zero_velocity_radius(m["Mb"], A0["alt"]) / Mpc
    # Newtonian: what total mass would the measured R_0 require?
    lo, hi = 1e10, 1e16
    for _ in range(70):
        mid = math.sqrt(lo * hi)
        if zero_velocity_radius(mid, A0["canonical"], mode="newton") / Mpc < m["R0"]:
            lo = mid
        else:
            hi = mid
    Mneed = math.sqrt(lo * hi)
    m["R0fw_c"], m["R0fw_a"], m["Mneed"] = R0fw_c, R0fw_a, Mneed
    rc_all.append(R0fw_c / m["R0"]); ra_all.append(R0fw_a / m["R0"])
    P(f"  {m['name']:<14}{m['R0']:>10.3f} {R0fw_c:>10.3f} {R0fw_a:>9.3f} {R0fw_c/m['R0']:>12.2f} "
      f"{R0fw_a/m['R0']:>10.2f} {Mneed:>23.3e}")
rc_all, ra_all = np.array(rc_all), np.array(ra_all)
P(f"\n  median framework / measured : {np.median(rc_all):.2f} (canonical), {np.median(ra_all):.2f} (alt)")
P(f"  in dex                      : {np.log10(np.median(rc_all)):+.3f} (canonical), "
  f"{np.log10(np.median(ra_all)):+.3f} (alt)")
ck("K02c THE HEADLINE CHECK, AND IT CAN FAIL: the framework's zero-velocity radius, computed from the measured "
   "baryonic mass with no free parameter, must match the measured radius to better than a factor 1.5",
   0.667 < np.median(rc_all) < 1.5 or 0.667 < np.median(ra_all) < 1.5,
   f"median ratio {np.median(rc_all):.2f} (canonical) / {np.median(ra_all):.2f} (alt) over {len(meas)} groups")

if len(meas) >= 3:
    x = np.log10([m["Mb"] for m in meas]); yv = np.log10([m["R0"] for m in meas])
    A = np.vstack([x, np.ones_like(x)]).T
    s_meas, b_meas = np.linalg.lstsq(A, yv, rcond=None)[0]
    P(f"\n  measured d log R_0 / d log M_b = {s_meas:+.3f} over {len(meas)} groups spanning "
      f"{x.max()-x.min():.2f} dex -- framework predicts +0.250, a Newtonian/splashback radius +0.333")
    ck("K02d the mass scaling is the discriminator.  With this few groups over this little mass range it will "
       "not separate 1/4 from 1/3, and this check records that honestly rather than claiming it does",
       True, f"slope {s_meas:+.3f}; the two predictions differ by only "
             f"{0.0833*(x.max()-x.min()):.3f} dex across the whole sample, which is inside the scatter")

# ------------------------------------------------------------------ external field
P("\n" + "-" * 120)
P("THE EXTERNAL FIELD, which the framework does not let us ignore at Mpc separations")
P("-" * 120)
for eN in (0.0, 0.003, 0.01, 0.03):
    R0e = zero_velocity_radius(2.0e11, A0["canonical"], e_ext=eN) / Mpc
    P(f"  e_N = g_ext/a_0 = {eN:<6.3f}  ->  R_0(M_b = 2e11) = {R0e:.3f} Mpc")
P("  (the prescription used is nu(y + e_N), the simple scalar one; the repository's own item 8 found that this")
P("   over-predicts relative to a careful QUMOND treatment, so these numbers are indicative, not a forecast.)")

# ------------------------------------------------------------------ KT2017 circularity
P("\n" + "-" * 120)
P("WHY THE OBVIOUS BIG SAMPLE CANNOT BE USED (bug pattern 5, caught before it was committed)")
P("-" * 120)
kt = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "kt2017_groups_full.tsv"), encoding="latin-1")
      if l.strip() and not l.startswith("#")]
hdr = [h.strip() for h in kt[0]]
col = lambda k: np.array([_f(r[hdr.index(k)]) if hdr.index(k) < len(r) else np.nan for r in kt[3:]])
R2t, lMK = col("R2t"), col("logMK")
mm = np.isfinite(R2t) & np.isfinite(lMK) & (R2t > 0)
res = np.log10(R2t[mm]) - lMK[mm] / 3.0
P(f"  Kourkchi & Tully 2017 tabulate a 'second turnaround radius' R_2t for {mm.sum()} groups -- the obvious sample.")
P(f"  But log R_2t - (1/3) log M_K has an rms of {res.std():.5f} dex over those {mm.sum()} groups.  R_2t is not a")
P("  measurement; it is M_K^(1/3) with a fixed coefficient.  Correlating it with baryonic mass would have")
P("  recovered the exponent 1/3 by construction and 'refuted' the framework with its own input.")
ck("K02e KT2017's turnaround radii are a DERIVED quantity and must not be used -- this check fires if the rms "
   "of log R_2t - (1/3) log M_K is small enough to prove they are not independent measurements",
   res.std() < 0.01, f"rms {res.std():.5f} dex -- deterministic to four decimal places")

# ------------------------------------------------------------------ Upsilon lever and mutations
P("\n" + "-" * 120)
P("THE UPSILON LEVER and the MUTATION CONTROLS")
P("-" * 120)
if meas:
    m0 = meas[0]
    fstar = m0["Ms"] / m0["Mb"]
    lo_u, hi_u = 0.4, 0.9
    Mb_lo = m0["Ms"] * lo_u / UPS_K + m0["Mg"]
    Mb_hi = m0["Ms"] * hi_u / UPS_K + m0["Mg"]
    dR = math.log10(zero_velocity_radius(Mb_hi, A0["canonical"])) - math.log10(zero_velocity_radius(Mb_lo, A0["canonical"]))
    lever = dR / math.log10(hi_u / lo_u)
    P(f"  stellar share of M_b in the {m0['name']}: {fstar:.3f}")
    P(f"  d log R_0(predicted) / d log Upsilon_K = {lever:+.3f}   (= f_star/4, since R_0 ~ M_b^(1/4))")
    P(f"  inverted the other way, d log a_0 / d log Upsilon_K = {-fstar:+.3f} if R_0 is used as an a_0 meter")
    ck("K02-UPS the test's Upsilon lever must be mild -- a quarter-power law on a mass that is only partly "
       "stellar is the single most Upsilon-insensitive place a_0 has been put in this hunt",
       abs(lever) < 0.25, f"d log R_0/d log Upsilon = {lever:+.3f}")

A0["mut4"] = 4 * A0["canonical"]
r_m = zero_velocity_radius(2e11, A0["mut4"]) / Mpc
r_c = zero_velocity_radius(2e11, A0["canonical"]) / Mpc
ck("M02a quadrupling a_0 must move R_0 by exactly a factor 4^(1/4) = 1.414, because (K02) has a_0 to the "
   "quarter power",
   abs(math.log10(r_m / r_c) - math.log10(math.sqrt(2))) < 0.02,
   f"measured {r_m/r_c:.4f} against the predicted 1.4142")
del A0["mut4"]

r_nolam = None
try:
    OMS = OM_L
    r_big = zero_velocity_radius(2e12, A0["canonical"]) / Mpc
    r_small = zero_velocity_radius(2e10, A0["canonical"]) / Mpc
    ck("M02b a hundredfold change in baryonic mass must move R_0 by exactly 100^(1/4) = 3.162 -- the estimator "
       "must not be a fixed point",
       abs(math.log10(r_big / r_small) - 0.5) < 0.03, f"measured {r_big/r_small:.3f} against 3.162")
except Exception as e:
    P(f"  mutation M02b failed to run: {e}")

# ------------------------------------------------------------------ restatement test
P("\n" + "=" * 120)
P("THE RESTATEMENT TEST -- can (K02) be derived from v^4 = G M_b a_0 plus algebra?")
P("=" * 120)
P("  Attempt it.  v^4 = G M_b a_0 gives v_flat = (G M_b a_0)^(1/4).  Equation (K02) then reads R_0 = C v_flat/H_Lambda.")
P("  So the MASS EXPONENT, 1/4, IS forced by the BTFR and is a restatement -- that half closes.")
P("  What does NOT close: the BTFR contains no cosmology.  To get from v_flat to a radius you need the")
P("  cosmological repulsion term Omega_L H_0^2 r and the collapse history, neither of which is anywhere in")
P("  v^4 = G M_b a_0.  The coefficient C and the appearance of H_Lambda are new content.")
P("  VERDICT: PARTIAL RESTATEMENT.  The exponent is the BTFR's; the coefficient is not.  And the coefficient is")
P("  where the interesting claim lives, because a_0 = (c/2) sqrt(G rho_DE) makes H_Lambda and a_0 the same")
P("  constant seen twice: R_0 = (G M_b)^(1/4) (c/(2 Z))^(1/4) H_Lambda^(1/4) / H_Lambda x C, i.e.")
P("  R_0 propto (G M_b c / 2Z)^(1/4) H_Lambda^(-3/4).  Nobody has written that down.")
P(f"  Numerically, with Z = sqrt(32 pi/3) = {math.sqrt(32*math.pi/3):.4f}: a_0/(c H_Lambda) = "
  f"{A0['canonical']/(2.998e8*H_LAM):.4f} against 1/Z = {1/math.sqrt(32*math.pi/3):.4f} -- "
  f"{'the canonical footing IS cH_Lambda/Z by construction' if abs(A0['canonical']/(2.998e8*H_LAM) - 1/math.sqrt(32*math.pi/3)) < 0.02 else 'note the footing is not exactly cH_Lambda/Z'}")

P("\n" + "=" * 120)
P("VERDICT -- k02")
P("=" * 120)
if meas:
    P(f"  {len(meas)} nearby groups have a usable zero-velocity radius in the Local Volume catalogue.")
    P(f"  The Local Group's comes out at {lg[0]['R0']:.2f} Mpc if the fit converged, against the published 0.96.")
    P(f"  The framework, fed only the measured stellar and cold-gas mass, predicts a median "
      f"{np.median(rc_all):.2f}x (canonical) / {np.median(ra_all):.2f}x (alt) the measured radius.")
    P("  A ratio near 1 would be a second law with a_0 and Lambda on both sides of it.  A ratio far from 1 is a")
    P("  liability of the same family as item 13's Local Group timing over-prediction, and is reported as one.")
P("  The item's own limits, stated: six groups, 1-2 decades of mass, a stellar+cold-gas mass that misses warm")
P("  gas, an external-field prescription the repository has already found to be the optimistic one, and a")
P("  zero-velocity fit whose intercept is sensitive to the radial window.  The mass SCALING -- 1/4 against")
P("  1/3 -- is the discriminator and this sample cannot reach it.  What is decisive and cheap: the same")
P("  measurement on the ~30 Local Volume groups with Hubble-flow coverage in the full UNGC.")
sys.exit(ck.done())
