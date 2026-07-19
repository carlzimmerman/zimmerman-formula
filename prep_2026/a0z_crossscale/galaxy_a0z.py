#!/usr/bin/env python3
"""
GALAXY-SIDE a0(z) LANE  --  the Lambda-BLIND acceleration-scale measurement.
=============================================================================
Cross-scale a0(z) test for the de Sitter-Unruh MODIFIED-INERTIA framework
(Carl P. Zimmerman). The framework FORCES the galaxy acceleration scale to
track the cosmic dark-energy density:  a0(z) = c^2 sqrt(rho_DE(z)/32pi),
so on the GALAXY side  a0(z)/a0(0) = (V_z/V_0)^4 / (M_bar,z/M_bar,0)  read
off the baryonic Tully-Fisher relation (BTFR) zero-point at each redshift.
This lane assembles that galaxy-observed a0(z) and asks: does it track the
cosmic track (flat-Lambda -> 1.0  vs  DESI-evolving -> ~0.70 by z~3)?

  a0 = V^4 / (G M_bar)   is EXACT ONLY in the deep-MOND regime (g << a0),
  where the BTFR slope is forced to 4. That is the crux caveat below.

Deep-MOND clean probes (slope->4 guaranteed):  SPARC dwarfs at z=0, and the
Big Wheel at z=3.25 (large, low-acceleration outer RC). The massive
intermediate-z rotators (KMOS3D etc.) sit at g >~ a0 (NOT deep-MOND), their
fitted TFR slope is 3.0-3.85 (NOT 4), so their zero-point is NOT a clean a0
readout -- and its sign flips with the slope treatment (see below).

Footings (both run): the canonical rho_DE/cH_Lambda a0=9.36e-11 vs the alt
rho_total/cH0 a0=1.13e-10; and the SPARC-measured a0=1.181e-10 (Lambda-blind).
Because we report RATIOS a0(z)/a0(0), the footing largely cancels; it re-enters
only in the absolute Big-Wheel comparison, shown all three ways.

Exit 0. numpy/scipy only. Outputs to this directory. Frozen repo READ-ONLY.

Credits: Milgrom 1999 (the nu-kernel + BTFR, a0 propto sqrt(rho_vac));
McGaugh/Lelli (SPARC BTFR); Ubler+2017, Tiley+2019, Di Teodoro+2016,
Sharma+2024 (high-z TFR); Big Wheel arXiv:2409.17956; Limbach-Psaltis-Ozel
2008 (a0 propto sqrt(rho_DE)); Brout+2022 / DESI DR2 (rho_DE(z)).
"""
import numpy as np
from scipy.stats import norm

np.random.seed(0)
G, Msun, c = 6.67430e-11, 1.98892e30, 2.99792458e8

# --------------------------------------------------------------------------
# 0.  z=0 ANCHOR  --  SPARC, Lambda-blind, clean deep-MOND gas-dominated dwarfs
# --------------------------------------------------------------------------
A0_SPARC, A0_SPARC_E = 1.181e-10, 1.90e-11        # banked a0-line GLS gas-dom (16%)
A0_CANON, A0_ALT     = 9.355e-11, 1.1305e-10       # framework footings
print("="*76)
print("GALAXY-SIDE a0(z):  the Lambda-blind BTFR-zero-point measurement")
print("="*76)
print(f"z=0 anchor (SPARC, Lambda-blind, clean deep-MOND):  a0 = {A0_SPARC:.3e} +/- {A0_SPARC_E:.2e}")
print(f"  framework footings for the ABSOLUTE compare: canonical {A0_CANON:.3e}, alt {A0_ALT:.3e}\n")

# --------------------------------------------------------------------------
# 1.  COSMIC REFERENCE TRACKS  (what the galaxy a0(z) is confronted against)
#     a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0).  CPL: rho_DE ratio =
#       (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z)).
# --------------------------------------------------------------------------
def rhoDE_ratio(z, w0, wa):
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
def a0_track(z, w0, wa):
    return np.sqrt(rhoDE_ratio(z, w0, wa))
TRACKS = [("flat-Lambda (w=-1)",      -1.00,  0.00),   # -> 1.0 at all z
          ("DESI-DR2 evolving",       -0.75, -0.90)]   # -> ~0.70 by z~3 (declining)
# the ALT cH0 footing RISES: a0 propto cH(z)=cH0 E(z); shown for contrast.
Om = 0.315
def E(z): return np.sqrt(Om*(1+z)**3 + (1-Om))
zref = np.array([0.5, 1.0, 2.0, 3.0, 3.25])
print("COSMIC reference a0(z)/a0(0) the galaxy data must be checked against:")
print(f"  {'z':>5} | {'flat-Lambda':>11} | {'DESI-evolve':>11} | {'alt cH0 (rise)':>14}")
for z in zref:
    print(f"  {z:5.2f} | {a0_track(z,*TRACKS[0][1:]):11.3f} | {a0_track(z,*TRACKS[1][1:]):11.3f} | {E(z):14.3f}")
print("  framework DISTINCTIVE prediction: a0(3)/a0(0) ~ 0.60-0.75 (declining;")
print("  z~3 BTFR V ~ -7% / -0.03 dex below the z=0 relation at fixed M_bar).\n")

# --------------------------------------------------------------------------
# 2.  GALAXY-SIDE MEASUREMENTS  --  the high-z BTFR/TFR compilation.
#     Map to a0 via the deep-MOND BTFR (slope 4): at fixed V,
#       Delta log a0 = -(Delta log M_bar|_fixed V) = -Delta_b .
#     A BTFR zero-point BELOW local (galaxies rotate FAST for their mass,
#     i.e. LOWER M_bar at fixed V, Delta_b<0) maps to a0 ABOVE local (RISING).
#     >>> CRUX: this map is only valid if the fitted slope is 4. High-z fits
#     give 3.0-3.85, and the offset SIGN FLIPS with the slope/pivot choice.
#     So intermediate-z is NOT a clean a0 probe; we carry a huge systematic.
# --------------------------------------------------------------------------
# Each entry: (label, z, Delta_b_dex, err_dex, slope_used, clean_deepMOND?, note)
# Delta_b = offset in log10(M_bar) at fixed V, relative to the z=0 local BTFR.
LIT = [
    # Ubler+2017 KMOS3D -- FIXED local slope (3.75). High-z BELOW local bTFR:
    #   at fixed V lower M_bar (Delta_b<0) => naive a0 ABOVE local (rising).
    ("Ubler+2017 KMOS3D bTFR", 0.9, -0.44, 0.04, 3.75, False,
        "massive rotators g>~a0, NOT deep-MOND; fixed-slope zero-point"),
    ("Ubler+2017 KMOS3D bTFR", 2.3, -0.27, 0.05, 3.75, False,
        "non-monotonic vs z~0.9; still below local"),
    # Sharma+2024 (aa48667) -- FREE slope 3.21 (bTFR), much shallower than 4:
    #   quotes zero-point +1.17 dex ABOVE local at their pivot -> OPPOSITE sign
    #   of Ubler. Demonstrates the offset is slope-artifact, not a0.
    ("Sharma+2024 bTFR (free slope 3.21)", 1.5, +1.17, 0.61, 3.21, False,
        "SLOPE 3.21!=4 -> sign of 'evolution' flips vs Ubler; NOT an a0 readout"),
    # Di Teodoro+2016 / Miller+ / Contini+ -- NO or weak zero-point evolution.
    ("Di Teodoro+2016 (tilted-ring, null)", 1.0, 0.00, 0.15, 3.8, False,
        "finds NO significant TFR zero-point evolution -> a0 ~ constant"),
    # Tiley+2019 KROSS -- strong STELLAR (-0.41 dex z~1->0) but NULL in K-band
    #   / dynamical once V/sigma>3 imposed; stellar offset is mass-growth, not a0.
    ("Tiley+2019 KROSS sTFR (V/sig>3)", 1.0, 0.00, 0.10, 4.0, False,
        "stellar -0.41dex is M*-growth; K-band/dynamical NULL -> a0 ~ constant"),
]
def a0ratio_from_db(db, slope):
    """naive a0(z)/a0(0) from a bTFR zero-point offset, treating it as deep-MOND.
       Delta log a0 = -db when slope=4. We DO NOT rescale by slope (the mapping
       is simply invalid off slope 4); we flag it instead."""
    return 10.0**(-db)

print("-"*76)
print("INTERMEDIATE-z BTFR/TFR  (naive deep-MOND a0 map -- NONE are clean):")
print("-"*76)
for lab, z, db, dbe, slp, clean, note in LIT:
    r  = a0ratio_from_db(db, slp)
    rlo, rhi = a0ratio_from_db(db+dbe, slp), a0ratio_from_db(db-dbe, slp)
    lean = "RISING" if r>1.15 else ("declining" if r<0.87 else "~constant")
    print(f"  z={z:<4} {lab:38s}")
    print(f"        Delta_b={db:+.2f}+/-{dbe:.2f} dex (slope {slp}) -> a0/a0_0 ~ "
          f"{r:.2f} [{rlo:.2f},{rhi:.2f}]  ({lean}, deep-MOND? {clean})")
    print(f"        ^ {note}")
print()
print("  READ: the SIGN of the intermediate-z 'a0 evolution' is CONTESTED --")
print("  Ubler (fixed slope) -> a0 rising ~2-3x; Sharma (free shallow slope) ->")
print("  opposite; Di Teodoro/Tiley -> null. The scatter across analyses (factor")
print("  ~2-3 EITHER way) dwarfs the 0.70-vs-1.0 signal. These massive rotators")
print("  are g>~a0 (NOT deep-MOND) so their TFR zero-point is NOT a clean a0.\n")

# --------------------------------------------------------------------------
# 3.  z=3.25 BIG WHEEL  --  the one CLEAN deep-MOND high-z probe (single object)
#     a0_eff = V_circ^4/(G M_bar), Monte-Carlo over V and M_bar systematics.
#     (banked BIG_WHEEL_A0Z_2026; arXiv:2409.17956.)
# --------------------------------------------------------------------------
V_rot, V_err, sig_int = 280.0, 31.0, 61.0            # km/s (incl-corr max, asym-drift)
Mstar, Mstar_e = 1.7e11, 0.7e11                      # M_dyn-capped fair central (SED 3.7e11 over-est)
Mgas,  Mgas_e  = 1.8e11, 0.9e11                      # CO H2, x1.36 He
HE, n = 1.36, 400000
V   = np.random.normal(V_rot, V_err, n)*1e3
Vc2 = V**2 + 3.4*(sig_int*1e3)**2                    # asym-drift, small (V/sig~4.5)
Ms  = np.clip(np.random.normal(Mstar, Mstar_e, n), 0.05e11, None)
Mg  = np.clip(np.random.normal(Mgas,  Mgas_e,  n), 0.05e11, None)
a0BW = Vc2**2/(G*(Ms+HE*Mg)*Msun)
bw_lo, bw_med, bw_hi = np.percentile(a0BW, [16,50,84])
print("-"*76)
print("z=3.25 BIG WHEEL  --  the one CLEAN deep-MOND high-z datum (single object):")
print("-"*76)
print(f"  a0_eff = {bw_med*1e10:.2f} (+{(bw_hi-bw_med)*1e10:.2f}/-{(bw_med-bw_lo)*1e10:.2f}) e-10 m/s^2")
for lab, a00 in [("SPARC 1.181e-10", A0_SPARC), ("canonical 0.936e-10", A0_CANON), ("alt 1.131e-10", A0_ALT)]:
    r = np.percentile(a0BW/a00, [16,50,84])
    print(f"    a0(3.25)/a0(0) vs {lab:20s} = {r[1]:.2f} (+{r[2]-r[1]:.2f}/-{r[1]-r[0]:.2f})")
print("  -> consistent with CONSTANT (1.0); DISFAVORS the alt-cH0 5x rise (~2sigma,")
print("     banked P~1-3%); CANNOT distinguish the DESI 0.70 decline from flat")
print("     (the ~2x M_bar systematic is itself larger than the 0.30 decline signal).\n")

# --------------------------------------------------------------------------
# 4.  VERDICT  --  does the galaxy a0(z) distinguish DECLINING from FLAT?
# --------------------------------------------------------------------------
print("="*76)
print("VERDICT: does galaxy-side a0(z) DISTINGUISH declining (0.60-0.75) from flat?")
print("="*76)
# assemble the honest galaxy a0(z)/a0(0) points with realistic (systematic) errors.
# z=0 solid; z~1-2.3 systematics-dominated (we set +/-0.3 dex, sign-contested,
# centred on ~constant since the analyses straddle it); z=3.25 Big Wheel.
gz   = np.array([0.0, 1.0, 2.3, 3.25])
gr   = np.array([1.00,
                 np.median([a0ratio_from_db(-0.44,3.75), a0ratio_from_db(+1.17,3.21),
                            1.0, 1.0]),                          # straddle -> ~1
                 a0ratio_from_db(-0.27,3.75),
                 bw_med/A0_SPARC])
# errors in dex: z0 from SPARC 16%; z1/z2.3 huge systematic (sign-contested);
# z3.25 from Big Wheel MC.
gerr_dex = np.array([A0_SPARC_E/A0_SPARC/np.log(10),
                     0.35, 0.30,
                     0.5*(np.log10(bw_hi)-np.log10(bw_lo))])
print(f"  {'z':>5} | {'a0(z)/a0(0)':>11} | {'+/- dex':>8} | vs flat(1.0) | vs DESI-decl")
for z, r, ed in zip(gz, gr, gerr_dex):
    dflat = a0_track(z,*TRACKS[0][1:]); ddesi = a0_track(z,*TRACKS[1][1:])
    sflat = abs(np.log10(r/dflat))/ed if ed>0 else np.inf
    sdesi = abs(np.log10(r/ddesi))/ed if ed>0 else np.inf
    print(f"  {z:5.2f} | {r:11.2f} | {ed:8.2f} | {sflat:5.1f}sig     | {sdesi:5.1f}sig")
print()
print("  BOTTOM LINE (honest both ways):")
print("   * z=0 SOLID at 1.0; z=3.25 (clean, single object) ~1.0-1.3, consistent")
print("     with flat, DISFAVORS the 5x rise, cannot see the 0.70 decline.")
print("   * z~1-2.3 BTFR is systematics-dominated & SIGN-CONTESTED (slope!=4):")
print("     fixed-slope reads RISING (mildly AGAINST the decline), free-slope &")
print("     null analyses read constant. NOT a clean a0 -- envelope +/-0.3 dex.")
print("   * The predicted DECLINE (a0(3)/a0(0)~0.70, -0.15 dex) is NOT DETECTED;")
print("     the data are consistent with BOTH flat and the decline, and if")
print("     anything the naive intermediate-z lean is the WRONG sign (rising).")
print("   * NO galaxy-side detection of a0 tracking rho_DE. The test is currently")
print("     UNDERPOWERED, not passed and not failed.\n")

# --------------------------------------------------------------------------
# 5.  FORECAST  --  what it takes to detect the 0.70 decline at 3 sigma.
# --------------------------------------------------------------------------
sig_decl = -np.log10(0.70)   # = 0.155 dex, the target signal at z~3
for sper, lab in [(0.10, "clean deep-MOND rotators, M_bar to 0.10 dex (SPARC-like)"),
                  (0.25, "realistic high-z per-object (mass systematics ~0.25 dex)")]:
    N3 = (3.0*sper/sig_decl)**2
    print(f"  FORECAST ({lab}):")
    print(f"    to detect a0(3)/a0(0)=0.70 ({sig_decl:.2f} dex) at 3sigma vs flat,")
    print(f"    need sigma_mean={sig_decl/3:.3f} dex -> N ~ {np.ceil(N3):.0f} clean gas-traced")
    print(f"    deep-MOND rotators per z~2-3 bin.")
print("  Feasibility: JWST/ALMA now yield ~tens of z~2-3 gas-traced rotators;")
print("  ELT/HARMONI resolves individual outer (deep-MOND) RCs. A sample of")
print("  ~20-40 CLEAN deep-MOND z~2-3 disks (like the Big Wheel), with M_bar to")
print("  ~0.1 dex, reaches 3sigma on the declining track -- the decisive future test.")
print("\nEXIT 0")

# --------------------------------------------------------------------------
# 6.  FIGURE
# --------------------------------------------------------------------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    zz = np.linspace(0, 3.6, 200)
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    ax.plot(zz, a0_track(zz,*TRACKS[0][1:]), 'k-',  lw=2, label="cosmic: flat-$\\Lambda$ (=1.0)")
    ax.plot(zz, a0_track(zz,*TRACKS[1][1:]), 'b--', lw=2, label="cosmic: DESI-evolving ($\\to$0.70)")
    ax.fill_between(zz, 0.60*np.ones_like(zz), 0.75*np.ones_like(zz), color='b', alpha=0.10,
                    label="framework prediction band (z$\\to$3)")
    ax.plot(zz, E(zz), 'r:', lw=1.6, label="alt cH0 (rising, disfavored)")
    ax.errorbar(gz, gr, yerr=gr*np.log(10)*gerr_dex, fmt='o', ms=8, color='darkgreen',
                capsize=4, lw=1.8, label="galaxy-side a0(z) (this lane)", zorder=5)
    ax.annotate("SPARC\n(clean, z=0)", (0.0, 1.0), textcoords="offset points", xytext=(6,-30), fontsize=8)
    ax.annotate("Big Wheel z=3.25\n(clean, 1 object)", (3.25, gr[-1]), textcoords="offset points",
                xytext=(-95,8), fontsize=8)
    ax.annotate("KMOS3D massive rotators\n(NOT deep-MOND; sign-contested)", (2.3, gr[2]),
                textcoords="offset points", xytext=(-60,18), fontsize=7.5, color='gray')
    ax.set_xlabel("redshift  z"); ax.set_ylabel("a0(z) / a0(0)")
    ax.set_ylim(0.4, 5.5); ax.set_yscale('log'); ax.set_xlim(-0.1, 3.6)
    ax.set_title("Cross-scale a0(z): galaxy BTFR-zero-point vs cosmic $\\rho_{DE}(z)$")
    ax.legend(fontsize=8, loc='upper left'); ax.grid(alpha=0.25, which='both')
    fig.tight_layout()
    fig.savefig("galaxy_a0z.png", dpi=130)
    print("wrote galaxy_a0z.png")
except Exception as e:
    print(f"(figure skipped: {e})")
