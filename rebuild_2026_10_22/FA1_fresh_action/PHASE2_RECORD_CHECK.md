# FA1 Phase 2: the ten Phase 1 ideas against the record

Read after Phase 1 was committed (825da66d06). Sources grepped:
rebuild_2026_10_22/*/README.md, campaign_fresh_gravity/LEDGER.md,
covariant_push_2026_10_22/ (read only), rebuild_2026_10_22/AX1_action_for_law/,
opus_48_extended_research/. Commit hashes are the last commit touching each folder.

## What the record says a successor needs
V3S_FINAL_VERDICT_2026-10-24.md, "What a successor needs": a gravitating cold
sector that clusters like dust from z ~ 1100, weighs in hosts and clusters, and
adds nothing in isolated galaxies. Section 7 (X19, a9ec701f5b): no single
catalogue variable or axis-aligned pair separates the classes. Section 8 (X22,
a2b532e3c6): a forest-passing cold component falls into galaxies (median capture
0.76 of fair share against a tolerance of 0.20), so a window opens only with
non-gravitational exclusion; late heating then fails (X23). X24 recasts the
hosted-dwarf excess as a ~4-5 km/s velocity floor, not a selector problem.
X57 (436ff03cb9) adds the mu-pincer (a local key in x, rho_b, theta acts in the
linear universe or never forms) and CFG944's Theorem G (no local L(theta, u) does
the static law, growth, ghost freedom and slip together), leaving only (a) a
phase-space key, (b) a retarded nonlocal operator, (c) a constraint functional.

## Idea by idea

| id | idea | status | where |
|---|---|---|---|
| I1 | tidal isotropy of the baryonic source, zeta = rho_b / rho_bar_b (Weyl-electric over Ricci) | **UNTESTED as a dust-weight selector**; neighbours PARTLY | X67_tidal_screened_aqual (036af115dd) used the same ratio, C^2 = (rho_bar/rho)^2, but on the cold component's own profile, to gate an AQUAL pull: FAIL (raises, no floor). KT30_tracefree_tidal_rule (f49e2e77bb) and KT27-KT32 used trace-free tidal norms for the MOND response, not for dust: FAIL on the MW midplane. X19's eleven variables do not include the baryon profile slope. |
| I2 | mean-flow vorticity / rotation support | **PARTLY TESTED** | DR5_rotation_support_gate (40d43dbb8a): rotation-support gate S_rot ~ 1 - sigma^2/V^2 reduces to existing rows; dwarfs are rotation-supported too; clusters read the failing response row. Keyed through sigma (a banned selector). two_state_mechanism_2026_10_24/vorticity_gate (folder not committed as a lane): small rotating objects stay protected, beta and L selected. The ETG/dSph kill named in Phase 1 was not run there. |
| I3 | fixed Jeans length / k^4 dispersion | **TESTED, FAIL** | X22_cosmic_dust_window (a2b532e3c6): forest needs clustering to 0.42 Mpc/h (M_hm ~ 5e9 Msun); median SPARC galaxy collapses from 10x that mass, capture 0.76. X57 M4 (436ff03cb9): wave term -(nu_w^2/4) k^4, nu_w,max 97.3 kpc km/s from the forest; cores largest in the smallest objects. |
| I4 | staticity (AeST (Q-dot - Q0)^2 dust) | **TESTED, FAIL / NO VERDICT** | H1_aest_F (1654b84f78), H2_aest_clusters (385f61a14c): static term wrong shape, CANNOT supply cluster lensing; AN1_aest_nonlinear_dust (a3ce1814c5): rows fold, no hydrostatic settling, v3 rerun NO VERDICT; AN2 unrun. Relaxed X-COP clusters need the dust, as Phase 1 expected. |
| I5 | disformal bulk-motion selector | **UNTESTED** (selector); disformal TeVeS FAIL | AX1_action_for_law/AUDIT.md: TeVeS's disformal metric fails GW170817. Bulk velocity relative to the khronon frame as a selector is not in the record; Phase 1's order of magnitude (LG 600 km/s vs clusters 300-1000 km/s) already gives no separation. |
| I6 | Galileon determinant (dimensionality) | **UNTESTED** (as dust selector); galileons PARTLY | M1_trilemma (836cc3661f) R2a: cubic and quartic galileons of the AeST scalar for the planets need r3 >= 900 Gpc or r4 >= 0.67 Mpc; L5 drops out of the spherical law. As a dust switch: not tested. Phase 1 order of magnitude: the far field of a disc is nearly spherical where rotation curves are measured. |
| I7 | defect network | **UNTESTED** | V1_density_screen (0429deb416) mentions symmetron domain walls only as a well-posedness caveat. Dead on paper: strings and walls are not w = 0. |
| I8 | Weyl/Ricci fill factor of the full metric | **PARTLY TESTED** | K1_braneworld_weyl (83d3592c87): a Weyl fluid as the cold sector FAILS every closure (cluster cores short by ~1e12 under BBN; profile tracks the potential). As a switch it reads as a gas-density selector in clusters (banned). |
| I9 | nonlocal curvature history (box^-1 R) | **TESTED, FAIL** | DR4_orbit_count_memory (552b98907e): box^-1 R is a potential plus a cosmic calendar, not an orbit count; clusters are not N <= 1. TM2_time_lag_memory (c5bae4c406): fixed-frame memory dead on the Bullet; scalar worldline memory dead. X57 (b) lists a retarded nonlocal operator quadratic in shear or vorticity as not excluded and not derived. |
| I10 | condensate coherence length set by rho_DE | **TESTED, FAIL** (as I3) | X57 M4 (436ff03cb9): coherence length r_w = 2 pi nu_w / V shrinks with mass; cores largest in the smallest objects. Same forest wall as X22. |

Counts: 10 ideas. TESTED 4 (I3, I4, I9, I10). PARTLY TESTED 3 (I2, I8, and I1's
neighbours). UNTESTED as stated 4 (I1, I5, I6, I7).

## Which untested idea to grade
- I5 and I7 fail on order of magnitude in Phase 1; grading them would only
  restate that.
- I6 needs a field solve to say anything, and its GW-speed status
  (quintic Galileon) is already bad.
- **I1 is the one untested idea that can be graded cheaply on the record's own
  data**: the selector zeta = rho_b / rho_bar_b(<r) (for a sphere,
  (d ln M_b / d ln r) / 3) can be read off SPARC mass models, X-COP gas and
  stellar profiles, and UX6's Bullet baryon model, with no new data.

Two warnings from the record that bear on I1 before any number:
1. X22: the cold component is captured by galaxies (0.76 of fair share). I1 does
   not keep the dust out of galaxies; it can only switch its weight. A weight
   switch on a gravitating component is not a standard field-theory object (it
   breaks the equivalence principle for that component unless the switch is in
   how the dust couples to the metric). Phase 3 grades the selector's
   separation only, which is necessary, not sufficient.
2. The mu-pincer: zeta is local. In the linear universe zeta = 1 + O(delta), so
   the dust is on there, as required. The pincer bites if a galaxy-scale value
   of zeta is cluster-like, which is exactly the Phase 3 test.

kappa = 1/2 FITTED; not theory closed. Nothing adopted.
