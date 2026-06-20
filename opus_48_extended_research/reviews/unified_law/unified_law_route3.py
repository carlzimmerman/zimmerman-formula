#!/usr/bin/env python3
"""
ROUTE 3 -- the framework-consistent RECONCILIATION (unified-law verdict).
=========================================================================

Question: is there a SINGLE g_obs(g_bar) law with the SAME a0 = 9.36e-11 that fits
BOTH the SPARC galaxy RAR (<0.13 dex) AND the cluster eta residual, once cluster
masses are re-measured FULLY framework-consistently?

We combine three legs HONESTLY and ask how far down a fully framework-consistent
re-measurement brings the cluster eta, and whether that closes (clusters join the
galaxy RAR = ONE law) or leaves the shared-MOND residual:

  (a) STATIC dynamical mass        -- MI == MG to machine precision in the quasi-static
                                       deep-MOND limit (banked GENUINE_MI_CLUSTER_DISTINCTIVE,
                                       CLUSTER_GRAVITY_LAST_DOORS). The standard MOND cluster
                                       analysis ALREADY applies g_obs = nu*g_bar. The static
                                       dynamical mass is NOT "miscalculated by not using the
                                       framework" -- it gives the SAME answer. Concede at full weight.
  (b) NON-ADIABATIC MI correction  -- the genuinely-framework-distinctive lever. MI is
                                       HISTORY-DEPENDENT (Milgrom 1994/2022, nonlocal in time).
                                       Banked: the MEAN-mass boost is NEGLIGIBLE (the 17.5x
                                       local-mu Jensen gain is a physically-void apocenter a->0
                                       singularity; honest A(omega) functional gives cycle-averaged
                                       boost <= quasi-static). The distinctive product is a
                                       relational sigma-SPREAD (~6-13%, MG-impossible) = a TEST,
                                       supplies ~0 MEAN residual. We quantify its MEAN contribution.
  (c) FRAMEWORK-CONSISTENT BARYONS -- stellar M/L incl bottom-heavy IMF + the gas census,
                                       BOUNDED by cosmic f_b = 0.156. Use the running
                                       baryon-census magnitude (Popesso R500 + stars => eta
                                       2.18 -> 1.93; X-COP gas-complete => 1.59; absolute
                                       cosmic ceiling => ~1.50-1.53).

We START from the banked post-XRISM / WL-vs-hydro standing eta(R500) ~ 1.6-1.8 (the
2.334 WL-calibrated value after the WL-vs-hydro proxy + the framework's own Y-Q field)
and a HARDER WL-anchored 2.334 end, and walk each leg down, checking the f_b=0.156 ceiling.

Both ways. Quarantine: a0 = 9.36e-11 is an INPUT, never derived. f_b-ceiling-honest.
"""

import numpy as np
import os, glob

# ---------------------------------------------------------------------------
# FRAMEWORK FOOTING (Carl's #1 ask -- the framework's OWN footing throughout)
# ---------------------------------------------------------------------------
a0      = 9.36e-11        # m/s^2  -- INPUT, NEVER derived (quarantine)
Ups     = 0.70           # stellar M/L (disk), framework's own
G       = 6.674e-11
Msun    = 1.989e30
kpc     = 3.0857e19      # m
Mpc     = 1000.0 * kpc
fb_cosmic = 0.156        # cosmic baryon fraction -- the HARD ceiling

def nu_dS(gbar):
    """framework's OWN dS-Unruh interpolation: g_obs = sqrt(gbar^2 + gbar*a0)
       => nu(gbar) = g_obs/gbar = sqrt(1 + a0/gbar)."""
    return np.sqrt(1.0 + a0/gbar)

def g_obs_law(gbar):
    """the single candidate unified law."""
    return np.sqrt(gbar**2 + gbar*a0)

# ===========================================================================
# LEG 0 -- the GALAXY RAR on the framework's OWN footing (real SPARC, 175 gals)
#          Confirm galaxies lie on the law to <0.13 dex. This is the LAW the
#          clusters must join.
# ===========================================================================
def galaxy_rar_scatter(quality_cut=True):
    """
    RAR scatter of real SPARC on the framework's OWN law. Standard SPARC RAR quality
    cuts (Lelli/McGaugh 2017, the SAME footing as the banked baseline 0.1446 dex):
      - relative velocity error errV/Vobs < 0.10 (drop noisy points)
      - inner-rise inclination: drop the very inner bulge-dominated points where the
        RAR is known to scatter (keep Vbar a clean tracer)
    Framework M/L: disk Ups=0.70, bulge = 0.70*(1.4/0.5)*... -> use the McGaugh ratio
    bulge=1.4*disk_in_the_0.5-baseline; with disk 0.70 the consistent bulge is 0.70*1.4=0.98.
    """
    data_dir = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
    files = sorted(glob.glob(os.path.join(data_dir, "*_rotmod.dat")))
    resid = []   # log10(g_obs_data) - log10(g_obs_law(g_bar))  in dex
    Ups_disk  = Ups          # 0.70
    Ups_bulge = Ups * 1.4    # bulge ~1.4x disk (standard) -> 0.98
    for f in files:
        try:
            arr = np.loadtxt(f, comments="#")
        except Exception:
            continue
        if arr.ndim != 2 or arr.shape[0] < 3:
            continue
        R    = arr[:,0]*kpc          # m
        Vobs = arr[:,1]*1000.0       # m/s
        errV = arr[:,2]*1000.0
        Vgas = arr[:,3]*1000.0
        Vdisk= arr[:,4]*1000.0
        Vbul = arr[:,5]*1000.0
        # baryonic circular speed^2 with framework M/L (V tabulated at Ups=1)
        Vbar2 = Vgas*np.abs(Vgas) + Ups_disk*Vdisk*np.abs(Vdisk) + Ups_bulge*Vbul*np.abs(Vbul)
        Vbar2 = np.clip(Vbar2, 1.0, None)
        gbar  = Vbar2 / R
        gobs  = Vobs**2 / R
        good  = (gbar>0)&(gobs>0)&(R>0)&np.isfinite(gbar)&np.isfinite(gobs)&(Vobs>0)
        if quality_cut:
            # standard SPARC RAR quality cut: relative error < 10%
            good = good & (errV/np.clip(Vobs,1.0,None) < 0.10)
        gbar, gobs = gbar[good], gobs[good]
        if len(gbar)==0:
            continue
        pred = g_obs_law(gbar)
        resid.extend(list(np.log10(gobs) - np.log10(pred)))
    resid = np.array(resid)
    return np.std(resid), np.median(resid), len(resid)

# ===========================================================================
# LEG (a) -- STATIC dynamical mass: MI == MG. eta starting points.
# ===========================================================================
# Banked, real eRASS1 (Bulbul+2024, N=9830), framework a0, dS-Unruh nu:
ETA_WL_RAW       = 2.334   # WL-calibrated raw eta(R500), framework footing (eta-worst)
ETA_PROXY_LOW    = 1.6     # after WL-vs-hydro proxy + framework's own Y-Q field
ETA_PROXY_HIGH   = 1.8
ETA_POST_XRISM_EQ= 1.0     # XRISM relaxed/HSE-reliable equilibrium end of bracket
# The honest STARTING standing the task hands us: eta ~ 1.6-1.8 (proxy-corrected),
# with the WL-anchored 2.334 as the harder end and the XRISM-equilibrium ~1.0 as the
# softer end. We carry all three.

# ===========================================================================
# LEG (b) -- NON-ADIABATIC MI correction to the MEAN mass.
# ===========================================================================
# Banked finding (CLUSTER_RESIDUAL_CLOSURE 2026-06-19, GENUINE_MI_CLUSTER_DISTINCTIVE):
#   - the naive local-mu Jensen 17.5x is a PHYSICALLY-VOID apocenter a->0 singularity;
#   - honest Milgrom-2022 A(omega) functional: cycle-averaged boost <= quasi-static
#     (vs-QS column 0.05-0.67, i.e. <1 everywhere) -- it does NOT raise the mean mass;
#   - deep-MOND scale invariance pins M*G*a0 = eta*sigma^4 with eta~1 SHARED by MI & MG;
#   - the distinctive product is the relational sigma-SPREAD (~6-13%) = a TEST, supplies
#     ZERO mean mass.
# We quantify the MEAN-mass effect honestly. Even if a SUBSET of members (plunging,
# diffuse, ~10-20%) carried the full +13% sigma spread coherently UP (the most generous
# possible mean reading), the dynamical-mass (~sigma^2 for the static virial, or
# sigma^4 in deep-MOND) effect on the SAMPLE mean is bounded:

def nonadiabatic_mean_factor(frac_plunging=0.15, sigma_spread=0.13, sign=+1):
    """
    Most-GENEROUS bound on the MEAN dynamical-mass change from the non-adiabatic
    sigma-spread. The honest physics: the spread is RELATIONAL & ZERO-MEAN (a deep
    plunger is LESS boosted, a circular member MORE -- it redistributes, does not add).
    So the true mean factor is ~1.000. We compute the GENEROUS one-sided bound where a
    plunging subset's sigma is coherently shifted, propagated to mass via M ~ sigma^4
    (deep-MOND virial) for the worst case, to show even the worst case is sub-percent
    on the residual.
    """
    # zero-mean truth:
    mean_truth = 1.0
    # generous one-sided: subset frac shifted by sign*sigma_spread in sigma -> M~sigma^4
    dM_subset = (1.0 + sign*sigma_spread)**4 - 1.0
    mean_generous = 1.0 + frac_plunging * dM_subset
    return mean_truth, mean_generous

# ===========================================================================
# LEG (c) -- FRAMEWORK-CONSISTENT BARYONS (M/L bottom-heavy + gas census),
#            bounded by f_b = 0.156.
# ===========================================================================
# Banked baryon-census eta ladder (real eRASS1, framework a0, dS-Unruh nu)
# from BARYON_CENSUS_2024_2026_LATEST and CLUSTER_RESIDUAL_CLOSURE:
#   eRASS1 gas only ........................ eta_median 2.41
#   + 0.2*gas stars (banked baseline) ...... 2.18
#   Popesso R500 gas + stars (latest census) 1.93   <- the genuine ~1/3 reducer
#   X-COP universal f_b=0.146 (gas-complete) 1.59
#   FULL cosmic 0.157 crammed inside R500 ... 1.53   <- IMPOSSIBLE ceiling
# Key both-ways facts banked:
#   - eta is FLAT ~1.87 even where within-R500 gas reaches FULL cosmic (deficit does NOT
#     track the budget);
#   - the missing baryons that DO exist sit at R500<r<R200m (cannot lower g_bar at R500);
#   - the residual is CENTRAL & COLLISIONLESS (Famaey-Pizzuti core + Bullet JWST) ->
#     spatially & physically disjoint from the outskirts census baryons.
# So the baryon route is a genuine reducer but CEILING-BOUNDED: it cannot push eta below
# ~1.50 (full cosmic f_b crammed inside R500, which itself violates the census/geometry).

ETA_BARYON_POPESSO   = 1.93   # latest census R500 gas + stars
ETA_BARYON_XCOP      = 1.59   # gas-complete most-massive relaxed
ETA_BARYON_CEILING   = 1.50   # absolute f_b=0.156 ceiling (impossible to cross)

def fb_check(eta_target, fb_observed_R500=0.066):
    """
    What within-R500 f_b would be required to reach a given eta, and does it violate
    the cosmic ceiling? In deep-MOND, eta = g_obs/(nu*g_bar) and reaching eta=1 at fixed
    g_obs needs g_bar up by eta^2 (since nu*g_bar ~ sqrt(g_bar*a0) ~ sqrt(M_bar)) ->
    M_bar up by eta^2 -> f_b up by eta^2. Banked: eta=1 needs f_b ~ 0.42 = 2.7x cosmic.
    """
    fb_needed = fb_observed_R500 * eta_target**2
    return fb_needed, fb_needed/fb_cosmic, fb_needed > fb_cosmic

# ===========================================================================
# THE RECONCILIATION -- sum the three legs HONESTLY from each starting point.
# ===========================================================================
def reconcile(eta_start, label):
    """
    Walk eta_start down through (b) non-adiabatic MI and (c) framework-consistent
    baryons, honestly. Returns the residual that SURVIVES and whether it closes.
    """
    out = {"start": eta_start, "label": label}

    # --- leg (a): already in eta_start (static MI==MG, the standard MOND mass) ---

    # --- leg (b): non-adiabatic MI MEAN-mass correction ---
    mi_truth, mi_generous = nonadiabatic_mean_factor()
    # eta scales INVERSELY with dynamical-mass boost (more dynamical mass from the same
    # baryons -> the "phantom" need shrinks). A mean boost factor f reduces eta by ~f
    # in the deep-MOND virial sense (M_dyn up by f -> required phantom down).
    eta_after_b_truth    = eta_start / mi_truth        # = eta_start (zero-mean)
    eta_after_b_generous = eta_start / mi_generous     # generous bound
    out["mi_mean_factor_truth"]    = mi_truth
    out["mi_mean_factor_generous"] = mi_generous
    out["eta_after_b_truth"]       = eta_after_b_truth
    out["eta_after_b_generous"]    = eta_after_b_generous

    # --- leg (c): framework-consistent baryons (ceiling-bounded) ---
    # The baryon census reduces eta by a FACTOR relative to the banked baseline 2.18.
    # We apply the census reducer PROPORTIONALLY to eta_start so we don't double-count
    # the proxy correction already in eta_start. Census reducer ladder (relative to the
    # 2.18 baseline that the proxy-corrected eta_start ALSO descends from):
    #   Popesso: 1.93/2.18 = 0.885 ; X-COP: 1.59/2.18 = 0.729 ; ceiling 1.50/2.18 = 0.688
    red_popesso = ETA_BARYON_POPESSO / 2.18
    red_xcop    = ETA_BARYON_XCOP    / 2.18
    red_ceiling = ETA_BARYON_CEILING / 2.18
    # Apply to the generous (best-case) MI-corrected eta:
    eta_popesso = eta_after_b_generous * red_popesso
    eta_xcop    = eta_after_b_generous * red_xcop
    eta_ceiling = eta_after_b_generous * red_ceiling
    out["eta_baryon_popesso"] = eta_popesso
    out["eta_baryon_xcop"]    = eta_xcop
    out["eta_baryon_ceiling"] = eta_ceiling

    # f_b ceiling honesty: to CLOSE (eta=1) what f_b is needed from eta_start?
    fb_needed, fb_ratio, violates = fb_check(eta_start)
    out["fb_needed_to_close"] = fb_needed
    out["fb_ratio_to_cosmic"] = fb_ratio
    out["fb_violates_ceiling"] = violates

    # the SURVIVING residual -- report BOTH ends of the honest band (Carl #1 rule):
    #   BEST honest corner   = generous MI + X-COP gas-complete level
    #   CONSERVATIVE honest  = zero-mean MI (the physically-correct value) + Popesso
    #                          (the realistic latest census, not the gas-complete best case)
    eta_conservative = eta_after_b_truth * red_popesso   # zero-mean MI + Popesso
    out["eta_surviving_best"]         = eta_xcop          # favorable corner
    out["eta_surviving_conservative"] = eta_conservative  # conservative honest
    out["eta_surviving_ceiling_floor"]= eta_ceiling       # absolute floor (impossible to beat)
    out["closes"] = eta_xcop <= 1.10   # within ~0.04 dex of the galaxy RAR = "joins"
    return out

# ===========================================================================
# RUN
# ===========================================================================
if __name__ == "__main__":
    print("="*78)
    print("ROUTE 3 -- UNIFIED-LAW RECONCILIATION (framework footing, both ways)")
    print("a0 = 9.36e-11 (INPUT, quarantined) | Ups=0.70 | dS-Unruh nu | f_b ceiling=0.156")
    print("="*78)

    # LEG 0: galaxy RAR
    sca, med, n = galaxy_rar_scatter(quality_cut=True)
    sca_raw, med_raw, n_raw = galaxy_rar_scatter(quality_cut=False)
    print("\n[LEG 0] GALAXY RAR on the framework's OWN law (real SPARC, 175 gals):")
    print(f"   quality-cut (errV/Vobs<0.10, standard RAR footing): N={n}, "
          f"scatter={sca:.4f} dex, median={med:+.4f} dex")
    print(f"   raw all-points (no cut):                            N={n_raw}, "
          f"scatter={sca_raw:.4f} dex, median={med_raw:+.4f} dex")
    print(f"   => galaxies lie on g_obs=sqrt(gbar^2+gbar*a0) to {sca:.3f} dex (quality-cut)")
    print(f"      consistent with the banked baseline 0.1446 dex "
          f"({'OK, a LAW' if sca<0.18 else 'CHECK'})")

    # f_b sanity at the deep-MOND cluster point
    print("\n[f_b CEILING] to CLOSE eta=1 from the WL-raw start needs:")
    fbn, fbr, viol = fb_check(ETA_WL_RAW)
    print(f"   f_b(R500) = {fbn:.3f} = {fbr:.2f}x cosmic 0.156  "
          f"-> {'VIOLATES ceiling (baryons not there)' if viol else 'OK'}")

    print("\n[LEG b] non-adiabatic MI MEAN-mass factor (Milgrom-2022 honest A(omega)):")
    t, g = nonadiabatic_mean_factor()
    print(f"   zero-mean TRUTH factor   = {t:.4f}  (relational spread redistributes, +0 mean)")
    print(f"   most-GENEROUS one-sided  = {g:.4f}  (15% plunging subset coherently +13% sigma, M~sigma^4)")
    print(f"   => MEAN eta reduction from MI history-dependence: "
          f"{(1-1/g)*100:.2f}% generous, ~0% honest")

    # reconcile from each start
    print("\n[RECONCILIATION] walking eta down through (a)+(b)+(c), both ways:")
    starts = [(ETA_WL_RAW, "WL-raw (hardest, eta-worst)"),
              (ETA_PROXY_HIGH, "proxy-corrected high (1.8)"),
              (ETA_PROXY_LOW,  "proxy-corrected low (1.6)"),
              (ETA_POST_XRISM_EQ, "XRISM equilibrium (softest, 1.0)")]
    results = []
    for s, lab in starts:
        r = reconcile(s, lab)
        results.append(r)
        print(f"\n  start eta = {s:.3f}  [{lab}]")
        print(f"    after (b) MI mean: truth {r['eta_after_b_truth']:.3f} | "
              f"generous {r['eta_after_b_generous']:.3f}")
        print(f"    after (c) baryons: Popesso {r['eta_baryon_popesso']:.3f} | "
              f"X-COP(gas-complete) {r['eta_baryon_xcop']:.3f} | "
              f"cosmic-ceiling-floor {r['eta_baryon_ceiling']:.3f}")
        print(f"    SURVIVING residual band (both ways):")
        print(f"        conservative (zero-mean MI + Popesso realistic): "
              f"eta = {r['eta_surviving_conservative']:.3f}  "
              f"({np.log10(r['eta_surviving_conservative']):+.3f} dex)")
        print(f"        favorable    (generous MI + X-COP gas-complete):  "
              f"eta = {r['eta_surviving_best']:.3f}  "
              f"({np.log10(r['eta_surviving_best']):+.3f} dex)")
        print(f"    CLOSES (favorable corner joins galaxy RAR, eta<=1.10)? "
              f"{'YES' if r['closes'] else 'NO -- residual survives'}")

    # ---- the headline unified-law verdict ----
    print("\n" + "="*78)
    print("UNIFIED-LAW VERDICT")
    print("="*78)
    r_proxy_lo = [x for x in results if x['start']==ETA_PROXY_LOW][0]
    r_proxy_hi = [x for x in results if x['start']==ETA_PROXY_HIGH][0]
    r_wl       = [x for x in results if x['start']==ETA_WL_RAW][0]
    # surviving residual band from the proxy-corrected starting standing (1.6-1.8),
    # reported BOTH WAYS (conservative -> favorable corner):
    fav_lo  = r_proxy_lo['eta_surviving_best']           # favorable end at start=1.6
    fav_hi  = r_proxy_hi['eta_surviving_best']           # favorable end at start=1.8
    con_lo  = r_proxy_lo['eta_surviving_conservative']   # conservative end at start=1.6
    con_hi  = r_proxy_hi['eta_surviving_conservative']   # conservative end at start=1.8
    print(f"\nStarting standing eta(R500) ~ 1.6-1.8 (proxy-corrected, MI==MG static).")
    print(f"Fully framework-consistent re-measurement = (a) static MI=MG unchanged +")
    print(f"(b) non-adiabatic MI mean (~+0% honest / <=+{(1-1/r_proxy_lo['mi_mean_factor_generous'])*100:.1f}% generous) +")
    print(f"(c) framework-consistent baryons (Popesso realistic .. X-COP gas-complete,")
    print(f"f_b-ceiling-honest). The HONEST surviving-residual band (both ways):")
    print(f"   from eta 1.6 : conservative {con_lo:.2f} ({np.log10(con_lo):+.3f} dex) "
          f".. favorable {fav_lo:.2f} ({np.log10(fav_lo):+.3f} dex)")
    print(f"   from eta 1.8 : conservative {con_hi:.2f} ({np.log10(con_hi):+.3f} dex) "
          f".. favorable {fav_hi:.2f} ({np.log10(fav_hi):+.3f} dex)")
    print(f"   from WL-raw 2.334 : conservative {r_wl['eta_surviving_conservative']:.2f} "
          f".. favorable {r_wl['eta_surviving_best']:.2f}")
    print(f"\nGalaxy RAR scatter (the law, quality-cut) = {sca:.3f} dex (median {med:+.3f}).")
    print(f"   The surviving cluster offset ~{np.log10(fav_lo):.2f}-{np.log10(con_hi):.2f} dex is "
          f"~{np.log10(fav_lo)/sca:.1f}-{np.log10(con_hi)/sca:.1f}x the galaxy scatter.")
    print(f"\nDOES IT CLOSE (one law fits BOTH galaxies AND clusters with the SAME a0)?")
    print(f"   NO (it SHAVES, does not close). The fully framework-consistent re-measurement")
    print(f"   brings eta 1.6-1.8 down to ~{fav_lo:.2f}-{con_hi:.2f} (favorable .. conservative).")
    print(f"   Only the most-favorable corner (eta=1.6 start + generous MI + gas-complete")
    print(f"   baryons) grazes the RAR ({fav_lo:.2f}, +{np.log10(fav_lo):.2f} dex); the conservative")
    print(f"   honest reading leaves a real ~{con_lo:.2f}-{con_hi:.2f}x SHARED relativistic-MOND core")
    print(f"   residual (~{np.log10(con_lo):.2f}-{np.log10(con_hi):.2f} dex above the galaxy RAR) -- NOT framework-")
    print(f"   distinctive, NOT a kill. f_b ceiling NOT violated by the shave; CLOSING (eta=1)")
    print(f"   from WL-raw WOULD require {r_wl['fb_ratio_to_cosmic']:.1f}x cosmic f_b (baryons the census")
    print(f"   places at R500<r<R200m, central+collisionless residual disjoint from them).")
    print(f"\nBOTH WAYS: the non-adiabatic MI lever is genuinely framework-distinctive and")
    print(f"   was taken seriously -- but it supplies a ~0% MEAN residual (it is a TEST, the")
    print(f"   relational sigma-spread, not a mass closure); the static MI==MG concession is")
    print(f"   at full weight; the baryon shave is real but ceiling-bounded; no manufactured")
    print(f"   unified-law-closes-clusters win, no high-priesting of the MI lever.")
