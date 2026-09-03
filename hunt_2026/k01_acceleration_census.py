#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k01 -- ANGLE 5, step 1: the systematic acceleration census.

QUESTION.  a_0 is an acceleration.  Enumerate every astrophysical system class whose characteristic
INTERNAL acceleration passes through a_0, and -- crucially -- the EXTERNAL field it is embedded in,
because MOND-class gravity is governed by max(g_int, g_ext), not by g_int alone.  The census is the map
that tells us where a second law could live, and it is computed from catalogues on disk wherever a
catalogue exists rather than from remembered numbers.

WHY THE EXTERNAL FIELD IS THE WHOLE POINT.  The programme's own QUMOND solver (hunt_efe_lib.py, V3) gives
the enclosed-mass boost of a system deeply embedded in a uniform external field:

    M_dyn / M_bar  ->  nu(e) [ 1 + L(e)/3 ],   L = dln nu/dln y,   nu(e) e = g_ext/a_0            (*)

i.e. a number that depends ONLY on the external field, NOT on the system's own acceleration.  The
isolated deep-MOND law v^4 = G M_b a_0 gives instead a boost sqrt(a_0/g_int) that depends only on g_int.
For a Galactic molecular cloud those two differ by a factor of about 100.  So the census's job is to
separate the classes into: (A) isolated, g_int > g_ext -- the RAR's home turf, already mined; and
(B) EFE-saturated, g_int << g_ext -- where the theory makes a DIFFERENT, untested, parameter-free
prediction (*) that no algebra on the BTFR can produce.

CHECKS THAT CAN FAIL are marked; a mutation control (a_0 x 10) must reclassify the census.

Run:  python3 k01_acceleration_census.py       (exit 0 = all checks pass)
"""
import os, sys, math, re
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import (A0, G, Msun, kpc, Mpc, c_light, DATA, load_sparc, vizier_tsv, _f,
                      nu, nu_s, Check, P, info)
from hunt_efe_lib import dlnnu_dlny

pc = 3.0857e16
AU = 1.495978707e11
VC_MW = 233.0e3          # local circular speed, Gaia/Eilers-class value (m/s)


# ----------------------------------------------------------------------------------- the EFE coefficient
def e_from_true_field(x_true, foot):
    """Invert nu(e) e = x_true to get the NEWTONIAN-equivalent external field e = g_N,ext/a_0."""
    lo, hi = 1e-8, 1e8
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        if nu_s(mid)*mid < x_true:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo*hi)


def efe_boost(x_true):
    """M_dyn/M_bar for a system with g_int << g_ext, from hunt_efe_lib's solved far-field limit."""
    e = e_from_true_field(x_true, None)
    n = nu_s(e)
    L = float(dlnnu_dlny(np.array([e]))[0])
    return n*(1.0 + L/3.0), e, n, L


def g_ext_mw(R_kpc, vc=VC_MW):
    """True (observed) external field at Galactocentric radius R for a flat rotation curve."""
    return vc**2/(R_kpc*kpc)


# ----------------------------------------------------------------------------------- catalogue loaders
def gc_table():
    """Baumgardt & Hilker N-body-fit Galactic globular clusters (ON DISK)."""
    p = os.path.join(DATA, "globular_clusters", "baumgardt_gc_parameters.tsv")
    lines = [l.rstrip("\n") for l in open(p, encoding="latin-1") if not l.startswith("#")]
    hdr = lines[0].split("\t")
    rows = [l.split("\t") for l in lines[1:] if l.strip()]

    def num(s):
        s = s.strip()
        if not s or s.startswith("—"):
            return float("nan")
        m = re.search(r"10(\d)\s*$", s)          # VizieR-style "8.53 +- 0.05 . 105" == 8.53e5
        e = int(m.group(1)) if m else 0
        try:
            return float(s.split("+-")[0].strip())*10**e
        except ValueError:
            return float("nan")

    col = lambda k: np.array([num(r[hdr.index(k)]) for r in rows])
    return dict(name=[r[0] for r in rows], M=col("Mass[Msun]"), rh=col("rh_m[pc]"),
                Rgc=col("R_GC[kpc]"), ML=col("M/L_V"), sig0=col("sigma0[km/s]"),
                rt=col("rt[pc]"), rc=col("rc[pc]"), Nrv=col("N_RV"), mf=col("MFSlope"),
                Rsun=col("R_sun[kpc]"), V=col("V[mag]"))


def gmc_table():
    """Miville-Deschenes+2017 8107 Galactic CO clouds (fetched this session)."""
    rows = vizier_tsv("gmc_mivilledeschenes2017.tsv")
    col = lambda k: np.array([_f(r[k]) for r in rows])
    far = col("INF") > 0.5
    return dict(Sigma=col("Sigma"), sigv=col("SigV"), Rgal=col("Rgal"),
                R=np.where(far, col("Rfar"), col("Rnear")),
                M=np.where(far, col("Mfar"), col("Mnear")), far=far)


def dsph_table():
    import csv
    p = os.path.join(DATA, "dsph", "mcconnachie2012_dsph.csv")
    with open(p, encoding="latin-1") as f:
        return list(csv.DictReader(f))


# ----------------------------------------------------------------------------------- the census
def main():
    ck = Check()
    P("=" * 118)
    P("k01 -- ANGLE 5: the acceleration census.  Which system classes have g_int crossing a_0, and what")
    P("      external field are they sitting in?  a_0 canonical 9.36e-11 / alt 1.13e-10 m/s^2.")
    P("=" * 118)

    a0c, a0a = A0["canonical"], A0["alt"]
    P(f"\nSanity: a_0 = (c/2) sqrt(G rho_DE).  Sigma_M = a_0/(2 pi G) = "
      f"{a0c/(2*math.pi*G)*pc**2/Msun:.1f} (canonical) / {a0a/(2*math.pi*G)*pc**2/Msun:.1f} (alt) Msun/pc^2")
    P(f"        the Sun's MOND radius r_M = sqrt(GM_sun/a_0) = {math.sqrt(G*Msun/a0c)/AU:.0f} / "
      f"{math.sqrt(G*Msun/a0a)/AU:.0f} AU")

    rows = []          # (class, g_int/a0 canonical, g_ext/a0 canonical, N, note)

    # ---------- 1. protoplanetary discs and the solar system -------------------------------------
    P("\n" + "-"*118)
    P("A.  SOLAR-SYSTEM-SCALE SYSTEMS  (external field = the Milky Way at R_sun)")
    P("-"*118)
    x_ext_sun = g_ext_mw(8.122)/a0c
    x_ext_sun_alt = g_ext_mw(8.122)/a0a
    P(f"  Milky Way field at the Sun: g_ext = {g_ext_mw(8.122):.3e} m/s^2 = {x_ext_sun:.3f} a_0 (canonical) "
      f"/ {x_ext_sun_alt:.3f} a_0 (alt)")
    B_sun, e_sun, n_sun, L_sun = efe_boost(x_ext_sun)
    B_sun_a, e_sun_a, _, _ = efe_boost(x_ext_sun_alt)
    P(f"  => Newtonian-equivalent e = {e_sun:.4f} (canonical) / {e_sun_a:.4f} (alt);   nu(e) = {n_sun:.4f}, "
      f"L(e) = {L_sun:.4f}")
    P(f"  => the EFE-saturation boost M_dyn/M_bar = nu(e)[1+L/3] = {B_sun:.4f} (canonical) / {B_sun_a:.4f} (alt)")
    info(f"cross-check: the frozen Gaia DR4 wide-binary band gamma_v = 1.1614-1.1814 canonical means a FORCE "
         f"boost gamma_v^2 = {1.1614**2:.4f}-{1.1814**2:.4f}; alt 1.1917-1.2267 -> "
         f"{1.1917**2:.4f}-{1.2267**2:.4f}")
    # RECONCILIATION with the frozen pre-registration.  PREREGISTRATION/Amendment 8-10 adopt a local field
    # x_ext = 1.89929 a_0 (canonical), i.e. g_ext = 1.778e-10 m/s^2, equivalent to V_c = 211 km/s at 8.12 kpc.
    # Straight V_c^2/R with the Gaia value V_c = 233 km/s gives 2.314 a_0 instead.  Both are carried: the
    # spread between them is the dominant systematic on the law's NORMALISATION (not on its shape).
    X_EXT_REG = 1.89929
    B_reg, e_reg, n_reg, L_reg = efe_boost(X_EXT_REG)
    B_reg_a, e_reg_a, _, _ = efe_boost(X_EXT_REG*a0c/a0a)
    P(f"  RECONCILIATION: the frozen registration adopts x_ext = {X_EXT_REG:.5f} a_0 (= {X_EXT_REG*a0c:.3e} m/s^2,")
    P(f"    i.e. V_c = {math.sqrt(X_EXT_REG*a0c*8.122*kpc)/1e3:.0f} km/s at R_0 = 8.122 kpc).  With it,")
    P(f"    e = {e_reg:.5f}, nu(e) = {n_reg:.5f} (registration quotes nu(y_extN) = 1.47342 -- matches),")
    P(f"    B = nu(e)[1+L/3] = {B_reg:.4f} canonical / {B_reg_a:.4f} alt.")
    ck("the e-inversion reproduces the registration's own nu(y_extN) = 1.47342 at x_ext = 1.89929  [CAN FAIL]",
       abs(n_reg/1.47342 - 1) < 1e-4, f"nu(e) = {n_reg:.6f}")
    d_wb = B_reg/(0.5*(1.1614**2 + 1.1814**2)) - 1.0
    P(f"    AGAINST INTEREST: B (the g_int -> 0 asymptote) sits {100*d_wb:+.2f}% from the midpoint of the frozen")
    P(f"    wide-binary band gamma_v^2 = 1.3488-1.3957.  It is inside the band's lower edge but not at its centre,")
    P(f"    because the registered band comes from a full nonlinear TWO-BODY AQUAL solve at finite internal field,")
    P(f"    not from the point-mass asymptote.  {100*abs(d_wb):.1f}% is therefore the irreducible mismatch between")
    P(f"    the two rungs' own definitions, and it is a floor on how well this law can ever be tested.")
    P(f"    => NORMALISATION SYSTEMATIC on the law: B(R_sun) = {B_reg:.3f} (registered field) to {B_sun:.3f} "
      f"(V_c = 233 km/s), canonical; {B_reg_a:.3f} to {B_sun_a:.3f}, alt.")

    for label, r_AU, Mcen in [("protoplanetary disc @ 100 AU", 100.0, 1.0),
                              ("Neptune", 30.07, 1.0),
                              ("Kuiper belt @ 50 AU", 50.0, 1.0),
                              ("Sedna aphelion (937 AU)", 937.0, 1.0),
                              ("inner Oort cloud @ 3000 AU", 3000.0, 1.0),
                              ("Sun's r_M (7960 AU)", math.sqrt(G*Msun/a0c)/AU, 1.0),
                              ("outer Oort cloud @ 50 kAU", 5.0e4, 1.0),
                              ("wide binary @ 5 kAU", 5.0e3, 1.0),
                              ("wide binary @ 30 kAU", 3.0e4, 1.0)]:
        gi = G*Mcen*Msun/(r_AU*AU)**2
        rows.append((label, gi/a0c, x_ext_sun, 1, "solar neighbourhood"))
        P(f"  {label:32s} g_int/a_0 = {gi/a0c:11.4g} (canon) {gi/a0a:11.4g} (alt)   "
          f"g_int/g_ext = {gi/g_ext_mw(8.122):9.4g}")

    # ---------- 2. star clusters -----------------------------------------------------------------
    P("\n" + "-"*118)
    P("B.  STAR CLUSTERS  (Baumgardt & Hilker N-body-fit catalogue, ON DISK; g_int at the half-mass radius)")
    P("-"*118)
    gc = gc_table()
    ok = np.isfinite(gc["M"]*gc["rh"]*gc["Rgc"])
    g_h = G*(gc["M"]*Msun/2.0)/(gc["rh"]*pc)**2
    g_e = g_ext_mw(gc["Rgc"])
    P(f"  {ok.sum()} clusters.  g_int(r_h)/a_0 canonical: "
      f"min {np.nanmin(g_h[ok]/a0c):.4g}, median {np.nanmedian(g_h[ok]/a0c):.3g}, max {np.nanmax(g_h[ok]/a0c):.4g}"
      f"   -> {math.log10(np.nanmax(g_h[ok])/np.nanmin(g_h[ok])):.1f} decades")
    n_below = int(np.nansum(g_h[ok] < a0c)); n_above = int(np.nansum(g_h[ok] > 10*a0c))
    n_efe = int(np.nansum(g_h[ok] < g_e[ok]))
    P(f"  {n_below} clusters below a_0 internally, {n_above} above 10 a_0, {n_efe} with g_int < g_ext "
      f"(EFE-saturated)")
    ck("GCs straddle a_0 from both sides with >= 20 systems each side  [CAN FAIL]",
       n_below >= 20 and n_above >= 20, f"{n_below} below a_0, {n_above} above 10 a_0")
    rows.append(("globular clusters (157)", float(np.nanmedian(g_h[ok]/a0c)),
                 float(np.nanmedian(g_e[ok]/a0c)), int(ok.sum()), "M/L_V,dyn measured -- k02"))

    # open clusters: literature scalars, stated as such
    for label, M, rh in [("open cluster (Hyades-like)", 400.0, 4.0),
                         ("open cluster (Pleiades-like)", 800.0, 4.0),
                         ("young massive cluster", 1.0e4, 1.5)]:
        gi = G*(M*Msun/2.0)/(rh*pc)**2
        P(f"  {label:32s} (M = {M:.0f} Msun, r_h = {rh:.1f} pc)  g_int/a_0 = {gi/a0c:.4g} (canon), "
          f"g_int/g_ext = {gi/g_ext_mw(8.122):.4g}")
        rows.append((label, gi/a0c, x_ext_sun, 1, "literature scalar"))

    # ---------- 3. molecular clouds ---------------------------------------------------------------
    P("\n" + "-"*118)
    P("C.  MOLECULAR CLOUDS  (Miville-Deschenes+2017, 8107 CO clouds; fetched this session)")
    P("-"*118)
    gm = gmc_table()
    okm = np.isfinite(gm["M"]*gm["R"]*gm["Sigma"]*gm["sigv"]*gm["Rgal"]) & (gm["M"] > 0) & (gm["R"] > 0)
    g_c = G*gm["M"]*Msun/(gm["R"]*pc)**2
    g_ce = g_ext_mw(np.maximum(gm["Rgal"], 0.5))
    P(f"  {okm.sum()} clouds.  g_int/a_0 canonical: 1st pct {np.nanpercentile(g_c[okm]/a0c,1):.4g}, "
      f"median {np.nanmedian(g_c[okm]/a0c):.4g}, 99th {np.nanpercentile(g_c[okm]/a0c,99):.4g}")
    frac_efe = float(np.mean(g_c[okm] < g_ce[okm]))
    P(f"  fraction with g_int < g_ext (EFE-saturated): {100*frac_efe:.1f}%")
    P(f"  median surface density {np.nanmedian(gm['Sigma'][okm]):.1f} Msun/pc^2;  "
      f"Sigma_M = a_0/(2 pi G) = {a0c/(2*math.pi*G)*pc**2/Msun:.0f} / {a0a/(2*math.pi*G)*pc**2/Msun:.0f}")
    ck("molecular clouds are internally sub-a_0 but EFE-saturated: >90% have g_int < g_ext  [CAN FAIL]",
       frac_efe > 0.90, f"{100*frac_efe:.1f}% of {okm.sum()} clouds")
    rows.append(("molecular clouds (8107)", float(np.nanmedian(g_c[okm]/a0c)),
                 float(np.nanmedian(g_ce[okm]/a0c)), int(okm.sum()), "alpha_vir measured -- k03"))

    # ---------- 4. dwarfs, discs, ellipticals, groups, clusters -----------------------------------
    P("\n" + "-"*118)
    P("D.  GALACTIC AND EXTRAGALACTIC")
    P("-"*118)
    ds = dsph_table()
    MB_HOST = {"MW": 6.0e10, "M31": 1.0e11}            # baryonic host masses (Msun)
    gs, ges = [], []
    for r in ds:
        try:
            VMag = float(r["VMag"]); rh_pc = float(r["R2"]); Dh = float(r["D"])
        except (ValueError, KeyError, TypeError):
            continue
        if not (rh_pc > 0 and Dh > 0) or r["SubG"] not in MB_HOST:
            continue
        Lv = 10**(-0.4*(VMag - 4.83))                  # V-band luminosity, M_V,sun = 4.83
        M = 1.6*Lv                                     # Upsilon_V = 1.6 (stellar populations)
        gi = G*(M*Msun/2.0)/(rh_pc*pc)**2
        gs.append(gi/a0c)
        ges.append(math.sqrt(G*MB_HOST[r["SubG"]]*Msun*a0c)/(Dh*kpc)/a0c)   # deep-MOND host field
    gs = np.array(gs); ges = np.array(ges)
    P(f"  Local Group dwarf spheroidals ({len(gs)}): g_int/a_0 median {np.median(gs):.4g} "
      f"[{np.percentile(gs,5):.3g}, {np.percentile(gs,95):.3g}];  host field/a_0 median {np.median(ges):.3g}")
    rows.append(("Local Group dSph", float(np.median(gs)), float(np.median(ges)), len(gs),
                 "LIABILITY item 8/43/44"))

    gal = load_sparc()
    g_out = np.array([g["gbar"][-1]/a0c for g in gal])
    g_in = np.array([g["gbar"][0]/a0c for g in gal])
    P(f"  SPARC disc galaxies ({len(gal)}): innermost g_bar/a_0 median {np.median(g_in):.3g}, "
      f"outermost median {np.median(g_out):.4g}  -- every disc crosses a_0")
    rows.append(("disc galaxies, outer (SPARC)", float(np.median(g_out)), 0.02, len(gal), "the RAR itself"))

    for label, gi_over_a0, ge_over_a0, note in [
            ("elliptical at R_e", 30.0, 0.01, "FP tilt: framework cannot be it (item 52)"),
            ("galaxy group at R500", 0.4, 0.01, "eta = 1.8-2.1, item 7"),
            ("galaxy cluster at R500", 0.35, 0.005, "eta ~ 2 unexplained, items 18/55/56"),
            ("intracluster light @ 100 kpc", 3.0, 0.01, "UNTESTED HERE"),
            ("SMBH sphere of influence, outer edge", 1e6, 30.0, "stars dominate long before a_0"),
            ("cosmic void wall (R ~ 15 Mpc)", 0.003, 0.0, "framework's linear regime is Newtonian (item 85)")]:
        rows.append((label, gi_over_a0, ge_over_a0, 0, note))
        P(f"  {label:38s} g_int/a_0 ~ {gi_over_a0:.3g}   (literature scalar) -- {note}")

    # ---------- 5. the classification -------------------------------------------------------------
    P("\n" + "=" * 118)
    P("THE CENSUS, sorted by internal acceleration.  ISOLATED = g_int > g_ext (the RAR's regime);")
    P("SATURATED = g_int < g_ext (the external-field regime, where the boost is nu(e)[1+L/3] and does NOT")
    P("depend on g_int at all -- the corner the BTFR cannot reach).")
    P("=" * 118)
    P(f"  {'system class':40s} {'g_int/a0':>12s} {'g_ext/a0':>10s} {'regime':>10s}  note")
    n_sat = 0
    for label, gi, ge, N, note in sorted(rows, key=lambda t: -t[1]):
        reg = "SATURATED" if gi < ge else "isolated"
        n_sat += (gi < ge)
        P(f"  {label:40s} {gi:12.4g} {ge:10.4g} {reg:>10s}  {note}")
    ck("the census finds at least six EFE-SATURATED classes (a corner the RAR literature does not test) "
       "[CAN FAIL]", n_sat >= 6, f"{n_sat} saturated classes of {len(rows)}")

    # ---------- 6. the law, and its lever ---------------------------------------------------------
    P("\n" + "=" * 118)
    P("THE CANDIDATE LAW THAT THE CENSUS POINTS AT")
    P("=" * 118)
    P("  M_dyn/M_bar = nu(e)[1 + L(e)/3],   nu(e) e = g_ext/a_0,   g_ext = V_c^2/R,   a_0 = (c/2) sqrt(G rho_DE)")
    P("  for every self-gravitating system with g_int << g_ext inside a galaxy.  ONE number per Galactocentric")
    P("  radius, the same for a wide binary and a molecular cloud -- 15 decades of mass, no free parameter.\n")
    P(f"  {'R_gal (kpc)':>12s} {'g_ext/a0 (c)':>13s} {'e (c)':>8s} {'B canonical':>12s} {'B alt':>8s}")
    Bs = []
    for R in (2.0, 4.0, 6.0, 8.122, 10.0, 12.0, 16.0, 20.0, 25.0):
        x, xa = g_ext_mw(R)/a0c, g_ext_mw(R)/a0a
        B, e, _, _ = efe_boost(x); Ba, _, _, _ = efe_boost(xa)
        Bs.append(B)
        P(f"  {R:12.2f} {x:13.3f} {e:8.3f} {B:12.4f} {Ba:8.4f}")
    ck("the law has a real Galactocentric lever: B rises by >= 25% from R = 4 to R = 20 kpc  [CAN FAIL]",
       Bs[-2]/Bs[1] - 1 > 0.25, f"B(20)/B(4) - 1 = {Bs[-2]/Bs[1]-1:.3f}")

    # restatement test, computed
    P("\n  RESTATEMENT TEST (computed, not asserted).  What does v^4 = G M_b a_0 predict for the same systems?")
    P("  The isolated deep-MOND boost is sqrt(a_0/g_int).  The saturation law says nu(e)[1+L/3].  If these")
    P("  agree the candidate is a restatement of the BTFR; if they differ the candidate is new content.")
    P(f"  {'class':32s} {'g_int/a0':>11s} {'BTFR boost':>11s} {'saturation B':>13s} {'ratio':>8s}")
    worst = 0.0
    for label, gi, ge in [("wide binary @ 30 kAU", G*Msun/(3e4*AU)**2/a0c, x_ext_sun),
                          ("open cluster (Hyades-like)", G*(200*Msun)/(4*pc)**2/a0c, x_ext_sun),
                          ("globular cluster Pal 3", 0.018, g_ext_mw(98.2)/a0c),
                          ("molecular cloud (median)", float(np.nanmedian(g_c[okm]/a0c)),
                           float(np.nanmedian(g_ce[okm]/a0c)))]:
        b_btfr = math.sqrt(1.0/gi)
        b_sat, _, _, _ = efe_boost(ge)
        worst = max(worst, b_btfr/b_sat)
        P(f"  {label:32s} {gi:11.4g} {b_btfr:11.3f} {b_sat:13.3f} {b_btfr/b_sat:8.2f}")
    ck("the derivation from v^4 = G M_b a_0 DOES NOT CLOSE: the BTFR boost and the saturation boost differ "
       "by >= 3x in at least one class, so the candidate is NOT a restatement  [CAN FAIL]",
       worst >= 3.0, f"worst ratio {worst:.1f}x")

    # ---------- 7. mutation control ---------------------------------------------------------------
    P("\n  MUTATION CONTROL: multiply a_0 by 10 and by 1/10 and re-classify.")
    for mult in (0.1, 10.0):
        a0m = a0c*mult
        nb = int(np.nansum(g_h[ok] < a0m)); ne = int(np.nansum(g_c[okm] < a0m))
        Bm, _, _, _ = efe_boost(g_ext_mw(8.122)/a0m)
        P(f"    a_0 x {mult:5.1f}:  GCs below a_0 = {nb:4d} (true {n_below}),  "
          f"clouds below a_0 = {ne:5d}/{okm.sum()},  B(R_sun) = {Bm:.4f} (true {B_sun:.4f})")
    Bm_lo, _, _, _ = efe_boost(g_ext_mw(8.122)/(a0c*0.1))
    Bm_hi, _, _, _ = efe_boost(g_ext_mw(8.122)/(a0c*10.0))
    ck("mutation control bites: a wrong a_0 by x10 moves the predicted boost B(R_sun) by > 15%  [CAN FAIL]",
       abs(Bm_lo/B_sun - 1) > 0.15 or abs(Bm_hi/B_sun - 1) > 0.15,
       f"B = {Bm_lo:.4f} / {B_sun:.4f} / {Bm_hi:.4f} for a_0 x0.1 / x1 / x10")

    # ---------- 8. the law run backwards: a baryonic mass from a velocity ratio ---------------------
    P("\n" + "=" * 118)
    P("THE LAW RUN BACKWARDS -- the Milky Way's baryonic mass from a stellar velocity ratio alone")
    P("=" * 118)
    P("  B is monotone in e, so a MEASURED boost inverts:  e = B^-1(B_hat),  M_b,MW = e a_0 R_0^2 / G.")
    P("  With B_hat = gamma_v^2 from Gaia DR4 wide binaries this measures the Galactic baryonic mass with")
    P("  NO photometry, NO stellar M/L and NO rotation curve -- only a velocity ratio and Lambda.")
    Bof = lambda e: efe_boost(nu_s(e)*e)[0]

    def e_of_B(Bt):
        lo, hi = 1e-4, 1e4
        for _ in range(300):
            m = math.sqrt(lo*hi)
            if Bof(m) > Bt:
                lo = m
            else:
                hi = m
        return math.sqrt(lo*hi)

    P(f"\n  {'gamma_v':>9s} {'B = gamma_v^2':>14s} {'e':>8s} {'M_b,MW canonical':>18s} {'M_b,MW alt':>14s}")
    for gv in (1.10, 1.1614, 1.1814, 1.1917, 1.20, 1.2267, 1.25):
        Bt = gv*gv
        e = e_of_B(Bt)
        P(f"  {gv:9.4f} {Bt:14.4f} {e:8.4f} {e*a0c*(8.122*kpc)**2/G/Msun:18.3e} "
          f"{e*a0a*(8.122*kpc)**2/G/Msun:14.3e}")
    e0 = e_of_B(1.3414); e1 = e_of_B(1.3414*1.01)
    lev = math.log(e1/e0)/math.log(1.01)
    P(f"\n  SENSITIVITY: d log M_b / d log B = {lev:.2f}, i.e. d log M_b / d log gamma_v = {2*lev:.1f}.")
    P(f"  A 2% measurement of gamma_v therefore gives M_b,MW to {abs(2*lev)*0.02*100:.0f}%.")
    P("  The published Galactic baryon census is 6.2-6.7e10 Msun.  If December returns gamma_v in the frozen")
    P("  band, the canonical footing infers 4.9-5.6e10 (10-25% LOW) and the alt footing 5.9-6.7e10 (on the")
    P("  census).  That is a FOOTING DISCRIMINATOR that costs nothing extra -- but it is only non-circular")
    P("  once gamma_v is MEASURED, because the frozen band was itself computed from an assumed local field.")
    ck("the backward inversion is well-posed: B is strictly monotone decreasing in e  [CAN FAIL]",
       Bof(0.3) > Bof(1.0) > Bof(3.0) > Bof(10.0),
       f"B(0.3) = {Bof(0.3):.3f} > B(1) = {Bof(1.0):.3f} > B(3) = {Bof(3.0):.3f} > B(10) = {Bof(10.0):.3f}")

    P("\n  UPSILON LEVER of the census itself: zero.  Every acceleration above is computed from a catalogued")
    P("  mass and radius, and the two classes the census promotes (globular clusters via M/L_V,dyn, molecular")
    P("  clouds via alpha_vir) carry dynamical masses, not photometric ones.  The stellar M/L enters only the")
    P("  GC rung's ABSOLUTE normalisation (lever -1), never the shape tests, and not at all for the clouds.")
    return ck.done()


if __name__ == "__main__":
    sys.exit(main())
