# CFG331 FROZEN CRITERIA: does the framework's own treatment of the host environment remove the four SLUGGS centrals' excess?

**Lane:** orchestrator (re-runs and commits). Written before any CFG331 code or number.

**Starting point.** CFG330 K0 (frozen 514b5ec8c): centrals M87 = NGC 4486, NGC 4365, NGC 4374, NGC 5846 at +0.2236 (canonical) / +0.2134 (alt); the other 12 at +0.0558 / +0.0468. CFG330 ruled out intracluster-GC contamination. The remaining candidate is the environment.

## Base code
A copy of CFG330's `cfg330_icgc.py` in K0 mode (raw Forbes+17 GC velocities, ATLAS3D JAM calibration, γ = 3, isotropic, outer bins R > max(R_e, 2 kpc), ν_mono, both footings 9.36e-11 / 1.13e-10, κ = ½ FITTED). Nothing is imported from other lanes' folders except the frozen kernel (CFG4_common, read-only).

## Inputs (on disk only; no downloads)
- **Host hot gas:** `real_research/data/cfg57_gas_sources/` (Lakhchaura+18 profiles for NGC 4486, 4374, 5846; Fukazawa+06 Table 4 for NGC 4365) with CFG57's D1 convention (upturned outermost shell dropped, outer power law of the three points before it). For M87 the outer profile is CFG323's transcribed Churazov+08 β-model to its measured edge, then Urban+11's Virgo slope (−1.21) to 1.2 Mpc, zero beyond (CFG323's `urban_trunc`). Values read from `CFG323_sluggs_measured_tracers/cfg323_transcribed_values.tsv`.
- **Member galaxies:** `real_research/data/2mrs_huchra2012.tsv` (2MRS table 3: RA, Dec, cz, K_t). A member is any 2MRS galaxy other than the central with projected separation R_p < the galaxy's outermost GC bin radius (at the SLUGGS distance) and |cz − cz_central| < 3 σ_V(host), σ_V from `kt2017_groups_full.tsv` (Virgo PGC 41220: 794 km/s for NGC 4486, 4374, 4365; NGC 5846 group PGC 53932: 320 km/s). Member stellar mass = the central's JAM-calibrated law mass × 10^(−0.4 (K_member − K_central)) (no new M/L constant). Each member enters M(<r) as a step at r = R_p (minimum 3D distance, so this is an upper bound on its enclosed contribution).
- **Gas inside r12** is subtracted from the JAM calibration (CFG323's `calib_mass` rule), so the total baryonic law mass inside r12 still matches the JAM mass.

## Readings (scored separately, never pooled)
- **R-own, hierarchical ownership** (PAPER35 §2 `qwen_claude_field_theory/papers_2026/PAPER35_hierarchical_ownership_dr4_2026.tex`, lane FG001 = `campaign_fresh_gravity/CFG7_hierarchy_fg001.py`): only the outermost bound system carries the phantom. For a central the outermost system is the host, so g = law of the host's enclosed baryons: stars + host gas + members inside r. A cluster *member* that is not at the host centre is an accreted system (FG001 class A): the isolated law of its own baryons (stars + its own measured gas), members excluded, host field as a tide only (neglected). Class per central: NGC 4486 = Virgo centre (the ICM profile is centred on it); NGC 5846 = group principal galaxy (KT17 PGC1 53932); NGC 4374 = Virgo member ~1.4° from M87 (class A); NGC 4365 = Env G, not a KT17 principal galaxy, so class A (own baryons).
- **R-bar, host gas as extra baryons in the same law:** g = law(stars + measured gas), members not added, for all four. (Reported alongside: R-barN, law(stars) + Newtonian g of the gas.)
- **R-efe, external field of the host:** g = ν(|g_N + g_e|/a0)(g_N + g_e) − ν(g_e/a0) g_e (1D Famaey–McGaugh form), stars only. g_e = 0 for an exact centre (NGC 4486, NGC 5846). NGC 4374: g_e = law field of Virgo's enclosed baryons (M87 stars + the M87/Virgo gas profile above) at its projected distance from M87. NGC 4365: g_e = deep-law field of Virgo's KT17 dynamical mass (log M_d = 14.867) at the 3D separation from the SLUGGS distances and positions (an upper bound: dynamical mass > baryons).

## Scorable
A central is scorable for R-own / R-bar if a measured gas profile for it is on disk (all four have one: Lakhchaura or Fukazawa); the measured-field radius vs the outer GC bins is reported, and beyond it the gas is the frozen extrapolation. If a reading needs a host table that is not on disk, that galaxy is "not scorable" for that reading and the missing table is named.

## Decision (per reading, both footings)
Baseline others' mean = CFG330 K0 (+0.0558 canonical / +0.0468 alt; the 12 are left at K0).
- **ENVIRONMENT EXPLAINS:** the scorable centrals' mean offset is within 0.05 dex of the others' mean on both footings.
- **PARTIAL:** the centrals' excess over the others drops by ≥ 50% on both footings.
- **NOT SUPPORTED:** otherwise.
Reported, not scored: the others with their own measured gas (NGC 4649, 3607, 4697), per-galaxy offsets.

## Controls
- **C1:** with host mass set to zero (gas × 0, members × 0, g_e = 0) every reading reproduces CFG330 K0 per galaxy to 1e-9 dex.
- **C2:** R-own applied to the 12 non-centrals as top-level systems (their own outermost system, no host baryons added) leaves each unchanged to 1e-9 dex.
- **C3:** R-efe with g_e = 0 equals the baseline (exact centre), and R-efe never lowers an offset (EFE can only lower the prediction).
- **MUTATE** (CFG331_MUTATE=1, separate outputs `_MUTATE`): host mass × 10 (gas and members). It must flag an over-correction: the scorable centrals' R-own mean goes negative on the canonical footing. If it does not, the check FAILS and is kept as it falls.

No knob scans. No fitted constant beyond κ = ½. At most 4 processes.
