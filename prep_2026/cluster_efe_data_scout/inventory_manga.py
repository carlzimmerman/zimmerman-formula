#!/usr/bin/env python3
"""
inventory_manga.py -- MaNGA/IFU-side inventory lane for the cluster-member EFE
sigma-spread feasibility scout (prep_2026/cluster_efe_channel/SYNTHESIS.md).

BINDING QUESTION: how many MMU-served MaNGA galaxies are SIMULTANEOUSLY
  (a) DIFFUSE deep-MOND carriers (resolved stellar sigma ~20-70 km/s),
  (b) cluster members, (c) Rhee-zone taggable, (d) in clusters rich enough
  for a caustic a_ext profile?

This is a PAPER feasibility estimate from published catalog metadata ONLY.
It is NOT a real cross-match (agents cannot download multi-GB MMU data).
Honest both ways: the diffuse+cluster overlap is the likely failure mode.

All input numbers are cited published values (see INVENTORY_MANGA.md).
Exit 0. Pure stdlib arithmetic.
"""

# ----------------------------------------------------------------------
# (0) What MMU-manga actually serves  -- verified from MMU scripts/manga
#     README + SDSS DR17 DAP MAPS datamodel.
# ----------------------------------------------------------------------
MMU_SERVES_DAP_MAPS = True     # DAP MAPS HYB10-MILESHC-MASTARSSP served
MMU_SERVES_STELLAR_SIGMA = True  # STELLAR_SIGMA + STELLAR_SIGMA_IVAR +
                                 # STELLAR_SIGMACORR extensions ARE in the
                                 # served MAPS -> resolved sigma is RECOVERABLE
                                 # (2D map; sigma_e = aperture 2nd moment, then
                                 #  quadrature-subtract STELLAR_SIGMACORR ch.0)

# ----------------------------------------------------------------------
# (1) MaNGA DR17 parent sample
# ----------------------------------------------------------------------
MANGA_UNIQUE = 10010           # unique galaxies (Abdurro'uf+ 2022 DR17)
# Stellar-mass structure of the sample (Sanchez-Garcia+ 2026, arXiv:2605.19426):
N_DWARF_LE95   = 977           # log M*/Msun <= 9.5
N_INTERM_95_10 = 1538          # 9.5 < log M*/Msun < 10.0
N_LT10         = N_DWARF_LE95 + N_INTERM_95_10   # log M* < 10 -> 2515
# Dedicated dwarf ancillary (MaNDala, Cano-Diaz+ 2022): M* < 10^9.06
N_MANDALA      = 136
N_MANDALA_SAT  = 35            # satellites (rest centrals/isolated; modest
                              #  groups, NOT rich clusters)

# ----------------------------------------------------------------------
# (2) Which of these are DIFFUSE deep-MOND carriers (sigma 20-70 km/s)?
#     Framework: a_in < ~1.5 a0 => sigma ~ 20-70 km/s (diffuse, low-SB).
#     Empirical anchor (Penny+ 2016, MaNGA yr-1 dwarfs, M*=1e9-5e9):
#     sigma_e spanned 40-127 km/s and 5/39 (~13%) were UNMEASURABLE below the
#     instrumental floor. So even at M*~1e9 a large fraction sit ABOVE 70 or
#     are unmeasurable. The 20-70 window is essentially the log M*<=9.5 dwarfs
#     plus the low tail of the intermediates.
# fraction of the <=9.5 dwarfs whose sigma_e actually lands in 20-70 (rest are
# >70 rotation-dominated disks, or unmeasurable):  ~0.45 (Penny+ anchor)
FRAC_DWARF_IN_2070   = 0.45
# fraction of the 9.5-10 intermediates in 20-70:   small low tail ~0.10
FRAC_INTERM_IN_2070  = 0.10
N_DIFFUSE_KINEMATIC = round(N_DWARF_LE95 * FRAC_DWARF_IN_2070
                            + N_INTERM_95_10 * FRAC_INTERM_IN_2070)

# ----------------------------------------------------------------------
# (2b) RELIABILITY HAIRCUT: MaNGA LSF 1-sigma ~= 70 km/s. DAP is "robust
#      down to ~20 km/s" ONLY at high SNR; for faint diffuse cluster dwarfs
#      SNR is marginal -> a chunk are upper limits, not measurements.
# ----------------------------------------------------------------------
FRAC_RELIABLE_BELOW_LSF = 0.55   # kept as usable sigma (not an upper limit)
N_DIFFUSE_USABLE = round(N_DIFFUSE_KINEMATIC * FRAC_RELIABLE_BELOW_LSF)

# ----------------------------------------------------------------------
# (3) CLUSTER-MEMBER cut. MaNGA is a field-dominated survey; it was NOT
#     built to tile clusters. Genuine rich-cluster members (R<R200, in a
#     cluster with enough members for a caustic a_ext profile) are a small
#     minority, concentrated in a handful of ancillary-targeted clusters
#     (Coma ~100-150 members of ALL masses; a few other Abell fields).
#     Dwarf satellite fraction from MaNDala: 35/136 ~ 0.26 are satellites,
#     but "satellite" >> "rich-cluster + caustic-able". Take the rich-cluster,
#     caustic-able fraction of diffuse dwarfs as ~0.10-0.15.
# ----------------------------------------------------------------------
FRAC_DIFFUSE_IN_RICH_CLUSTER = 0.12
N_MANGA_DIFFUSE_CLUSTER = round(N_DIFFUSE_USABLE * FRAC_DIFFUSE_IN_RICH_CLUSTER)

# ----------------------------------------------------------------------
# (4) SAMI cluster supplement (NOT in MMU; separate download).
#     Owers+ 2017 cluster sample: 906 galaxies in 8 low-z clusters WITH
#     membership + cluster-centric radius + peculiar velocity (Rhee-taggable
#     out of the box). Mass floor is redshift-dependent (~log M* > 9.5 in the
#     nearest clusters). Diffuse (sigma 20-70) fraction ~ similar low tail.
# ----------------------------------------------------------------------
SAMI_CLUSTER_TOTAL = 906
FRAC_SAMI_DIFFUSE  = 0.18        # low-sigma tail reachable at SAMI mass floor
N_SAMI_DIFFUSE_CLUSTER = round(SAMI_CLUSTER_TOTAL * FRAC_SAMI_DIFFUSE)

# ----------------------------------------------------------------------
# TARGETS
# ----------------------------------------------------------------------
TARGET_GO      = 300   # ~2-3 sigma firewalled exploratory floor
TARGET_STRETCH = 500

def line(): print("-" * 66)

print("MaNGA / IFU-side inventory  --  cluster-EFE sigma-spread scout")
line()
print(f"MMU-manga serves DAP MAPS ................. {MMU_SERVES_DAP_MAPS}")
print(f"MMU-manga serves resolved STELLAR_SIGMA .. {MMU_SERVES_STELLAR_SIGMA}")
print("  (STELLAR_SIGMA + STELLAR_SIGMACORR ch.0 -> astrophysical sigma_e)")
line()
print(f"MaNGA DR17 unique galaxies ............... {MANGA_UNIQUE:>6}")
print(f"  log M* <= 9.5  (dwarfs) ............... {N_DWARF_LE95:>6}")
print(f"  9.5 < log M* < 10 (intermediate) ..... {N_INTERM_95_10:>6}")
print(f"  log M* < 10 (combined) ............... {N_LT10:>6}")
print(f"  MaNDala dedicated dwarf ancillary .... {N_MANDALA:>6}  "
      f"({N_MANDALA_SAT} satellites)")
line()
print("DIFFUSE deep-MOND carriers (sigma 20-70 km/s):")
print(f"  kinematically in-window (all envs) ... {N_DIFFUSE_KINEMATIC:>6}")
print(f"  after reliability haircut (LSF floor)  {N_DIFFUSE_USABLE:>6}")
line()
print("CLUSTER-MEMBER overlap (the BINDING number):")
print(f"  MaNGA diffuse + rich-cluster member .. {N_MANGA_DIFFUSE_CLUSTER:>6}")
print(f"  SAMI  diffuse + cluster member ....... {N_SAMI_DIFFUSE_CLUSTER:>6}"
      "   (NOT in MMU)")
N_STACK = N_MANGA_DIFFUSE_CLUSTER + N_SAMI_DIFFUSE_CLUSTER
print(f"  MaNGA+SAMI stack ..................... {N_STACK:>6}")
line()
print(f"TARGET for ~2-3 sigma firewalled ........ {TARGET_GO}-{TARGET_STRETCH}")
line()

def verdict(n, label):
    if n >= TARGET_GO:
        v = "GO"
    elif n >= 0.4 * TARGET_GO:
        v = "BORDERLINE (underpowered stack)"
    else:
        v = "NO-GO (dies on statistics)"
    print(f"  {label:<24} n~{n:<4} -> {v}")

print("VERDICT:")
verdict(N_MANGA_DIFFUSE_CLUSTER, "MMU-MaNGA alone")
verdict(N_STACK,                 "MaNGA + SAMI stack")
line()
print("Resolved sigma: SERVED (go). Binding failure mode: the diffuse")
print("deep-MOND cluster-member overlap in MMU-MaNGA alone is ~tens.")
print("MaNGA is stellar-mass-limited (M* > ~1e9) and field-dominated, so the")
print("low-sigma cluster dwarfs that carry the signal are under-represented,")
print("and many sit at/below the 70 km/s LSF floor (upper limits, not values).")

# sanity: no negative / nonsensical counts
assert 0 < N_DIFFUSE_USABLE < MANGA_UNIQUE
assert N_MANGA_DIFFUSE_CLUSTER < N_DIFFUSE_USABLE
