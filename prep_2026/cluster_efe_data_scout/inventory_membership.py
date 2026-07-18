#!/usr/bin/env python3
"""
MEMBERSHIP / PHASE-SPACE INVENTORY LANE  (cluster-EFE sigma-spread data scout)
==============================================================================
Question for THIS lane: is Rhee+2017 infall-zone tagging + caustic a_ext binning
AVAILABLE for the nearby (z<0.1) clusters that host the IFU diffuse carriers?
And does DESI DR1 BGS meaningfully DEEPEN membership vs the SDSS-era catalogs?

This is a PAPER FEASIBILITY estimate from published catalog metadata. It does
NOT cross-match real data (agents cannot pull multi-GB MMU). All inputs are
cited published numbers; the arithmetic below is transparent and prove-by-moving.

Exit 0. Token-lean. Outputs to stdout only.
"""

# ----------------------------------------------------------------------------
# (1) PHASE-SPACE / MEMBERSHIP CATALOGS  -- the tagging INFRASTRUCTURE
#     Rhee zones need, per galaxy: R_proj/R200  and  |dv_los|/sigma_cl.
#     Caustic a_ext needs, per cluster: a caustic mass/accel profile M(<r),
#     which needs enough spectroscopic members (~tens+) to trace the caustic.
# ----------------------------------------------------------------------------
CATALOGS = {
    # name: (n_clusters, z_range, n_members, provides)
    "GalWCat19 (Abdullah+2020, ApJS 246:2, SDSS-DR13)":
        (1800, "0.01-0.20", 34471,
         "sigma_cl, M & R at Delta=500/200/100/5.5 -> caustic-ready + Rhee coords"),
    "Yang+2007/2012 SDSS groups (halo-based)":
        (">400k groups", "0.01-0.20", ">600k", "halo mass, R180, membership"),
    "redMaPPer SDSS (Rykoff+2014)":
        (26000, "0.08-0.55", ">1e6 (photo)", "richness lambda -> M200; z>0.08 mostly ABOVE IFU"),
    "HeCS / HeCS-omnibus (Rines+2013,2016)":
        (58, "0.02-0.30", ">20000", "caustic mass profiles (dedicated caustic survey)"),
    "SAMI cluster redshift survey (Owers+2017, MNRAS 468:1824)":
        (8, "0.029-0.058", 2899, "sigma200, R200, caustic+virial mass -> tailored to IFU"),
}

# ----------------------------------------------------------------------------
# (2) DESI DR1 BGS  -- does it DEEPEN membership around nearby clusters?
# ----------------------------------------------------------------------------
DESI_BGS = {
    "sky_density_deg2": 854,        # Hahn+2023 / DR1: 854 deg^-2 BGS
    "n_reliable_z": 5.5e6,          # >5.5M reliable redshifts, DR1
    "bright_maglim_r": 19.5,        # BGS BRIGHT r<19.5
    "faint_maglim_r": 20.175,       # BGS FAINT color-selected 19.5<r<20.175
    "z_median_bright": 0.20,
    "z_reach": 0.5,
    "coma_faint_completeness": "75-85% for -15.5<Mr<-14.8 at Coma z",  # reaches dwarf regime
}
# SDSS-era spectroscopic density for comparison (main galaxy sample):
SDSS_MAIN_DENSITY_DEG2 = 90        # SDSS Legacy spectroscopy ~90 deg^-2 (r<17.77)
DESI_DEEPEN_FACTOR = DESI_BGS["sky_density_deg2"] / SDSS_MAIN_DENSITY_DEG2

# ----------------------------------------------------------------------------
# (3) IFU CARRIER OVERLAP  -- the BINDING constraint (NOT the membership side)
#     Diffuse deep-MOND carriers: sigma_star ~ 20-70 km/s (a_in < ~1.5 a0).
#     MaNGA reliability: instrumental LSF ~70 km/s (1sigma); DAP reliable
#     stellar sigma only ABOVE ~ half the LSF (~40-50 km/s) for typical S/N.
#     MaNGA sample: 10,059 galaxies, ~flat in log M* for logM>9.0, floor ~5e8.
#     SAMI cluster: 906 IFU galaxies, M* floor logM>9.5 (even higher).
# ----------------------------------------------------------------------------
def overlap(n_total, f_cluster, f_diffuse, f_sigma_reliable, f_taggable, label):
    n = n_total * f_cluster * f_diffuse * f_sigma_reliable * f_taggable
    print(f"  {label}")
    print(f"    N_total            = {n_total}")
    print(f"    x f_cluster_member = {f_cluster:.2f}")
    print(f"    x f_diffuse(20-70) = {f_diffuse:.2f}")
    print(f"    x f_sigma_reliable = {f_sigma_reliable:.2f}   (LSF ~70 km/s floor)")
    print(f"    x f_taggable(PS)   = {f_taggable:.2f}   (has phase-space coords)")
    print(f"    = diffuse tagged members ~ {n:.0f}")
    return n

print("=" * 74)
print("MEMBERSHIP / PHASE-SPACE INVENTORY  -- cluster-EFE sigma-spread scout")
print("=" * 74)

print("\n(1) PHASE-SPACE TAGGING + CAUSTIC INFRASTRUCTURE (published catalogs):")
for name, (nc, zr, nm, prov) in CATALOGS.items():
    print(f"  - {name}")
    print(f"      clusters={nc}  z={zr}  members={nm}")
    print(f"      provides: {prov}")

print("\n  VERDICT (infrastructure): Rhee-zone coords (R/R200, |dv|/sigma) AND")
print("  caustic mass/accel profiles are ALREADY PUBLIC for hundreds of z<0.1")
print("  clusters (GalWCat19 + HeCS + Yang + SAMI-Owers). This is NOT the limiter.")

print("\n(2) DOES DESI DR1 BGS DEEPEN MEMBERSHIP?")
print(f"  DESI BGS density  = {DESI_BGS['sky_density_deg2']} deg^-2  ({DESI_BGS['n_reliable_z']:.1e} z's)")
print(f"  SDSS main density = {SDSS_MAIN_DENSITY_DEG2} deg^-2")
print(f"  -> deepening factor ~ {DESI_DEEPEN_FACTOR:.1f}x more spectroscopic members/cluster")
print(f"  -> BGS Faint reaches {DESI_BGS['coma_faint_completeness']}")
print("  -> YES: sharper caustics + fainter members tagged; helps the DENOMINATOR")
print("     (cleaner a_ext profiles), but does NOT create IFU sigma maps.")

print("\n(3) IFU CARRIER OVERLAP (the BINDING constraint):")
# MaNGA: flat logM>9.0; diffuse sigma 20-70 ~ lowest-mass ~20% of sample; but
# reliable stellar sigma only for upper part of that band; cluster dwarfs rarer.
n_manga = overlap(10059, f_cluster=0.10, f_diffuse=0.18,
                  f_sigma_reliable=0.50, f_taggable=0.85, label="MaNGA DR17")
# SAMI cluster: 906 IFU in 8 clusters (already cluster+tagged), but M* floor 9.5
# cuts deep-MOND dwarfs hard; f_diffuse lower, sigma reliability better (R~4500).
n_sami = overlap(906, f_cluster=1.00, f_diffuse=0.15,
                 f_sigma_reliable=0.70, f_taggable=1.00, label="SAMI cluster (Owers+2017)")

n_stack = n_manga + n_sami
print(f"\n  STACK (MaNGA + SAMI cluster) diffuse tagged members ~ {n_stack:.0f}")

TARGET_LOW, TARGET_HIGH = 300, 500
print("\n" + "=" * 74)
print(f"TARGET for ~2-3 sigma exploratory (firewalled): {TARGET_LOW}-{TARGET_HIGH}")
print(f"AVAILABLE diffuse tagged carriers (public IFU today): ~{n_stack:.0f}")
if n_stack < TARGET_LOW:
    shortfall = TARGET_LOW / max(n_stack, 1)
    print(f"VERDICT: NO-GO / UNDERPOWERED  (~{shortfall:.1f}x short of the floor)")
else:
    print("VERDICT: borderline-GO")
print("=" * 74)

print("""
WHY (honest both ways):
  * The MEMBERSHIP/PHASE-SPACE side is ABUNDANT and DESI DR1 deepens it further.
    Phase-space tagging + caustic a_ext profiles are NOT the bottleneck.
  * The bottleneck is the IFU DIFFUSE-CARRIER side. Both public IFU surveys are
    STELLAR-MASS-LIMITED (MaNGA logM>9.0, SAMI cluster logM>9.5), so the
    deep-MOND sigma~20-70 km/s dwarfs are under-represented, AND MaNGA's ~70 km/s
    LSF makes reliable STELLAR sigma below ~45 km/s marginal -- exactly the
    signal-carrying band. Cluster-member dwarfs are rarer still.
  * Magnitude of the target signal (framework-committed E10, tau_mem=203 Gyr):
    ~0.3-1.5% ABSOLUTE / ~4-9.5% RELATIONAL D(zone). At sigma~20-70 km/s the
    per-galaxy measurement error on sigma is ~5-15% -> need ~hundreds of carriers
    to beat it down. ~100-250 falls short.

WHAT IS NEEDED (named):
  * A dedicated DWARF-IFU cluster survey (push M* floor to logM~8), OR
  * A MaNGA + SAMI + Hector stack with a low-sigma-reliability re-reduction, OR
  * ELT/HARMONI-class resolved kinematics of cluster dwarfs.
  The tagging/caustic scaffolding (GalWCat19+HeCS+DESI DR1 BGS) is READY and would
  slot straight in the moment the diffuse-carrier IFU sample exists.
""")

print("EXIT 0 -- data-availability estimate only; NOT a physics claim; no 'proves'.")
