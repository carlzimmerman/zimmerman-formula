# SRJ3 FROZEN CRITERIA: does the reference layout fit the cluster-regime discs?

Written and committed alone, before any script of this lane exists and before any SRJ3 number is computed or seen.
TEST lane. kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings canonical / alt, never pooled.
Cold dark energy is a gravitating field component; no particle. SRF1 and SRF1R are not opened.

## Question

SRJ2 (criteria b8a99499ad, outputs 7671345425) found 31 / 22 of the 100 RC100 discs cluster-regime (v_vir > v_stiff,
265.8 / 288.1 km/s), so the regime-split joint gives them the reference layout at every radius. G2 was coverage only.
SRJ3 asks: does the joint's own layout for those discs (baryons + the reference cold dark energy halo) reproduce their
observed circular speed at R_e?

## Samples

- **Primary:** the RC100 galaxies SRJ2 calls cluster-regime, recomputed by executing SRJ2's `srj2_rc.py` read-only
  from its own path up to its `json.dump(RES` line (nothing written in SRJ2's folder). Expected 31 / 22 (K1).
- **Data:** `data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv` (FLD1's and DD1's input, paper
  values of Nestor Shachar et al. 2023 Table 3): z, logMbar_Msun, Re_kpc, Vc_Re_kms (observed, pressure-corrected
  circular speed at R_e), fDM_within_Re (author decomposition, REPORTED only, never graded).
- **Secondary (reported, not graded):** SPARC cluster-regime galaxies (3 / 0 FLD1 M_b; 9 / 2 PD1 M_b). SRJ2's own
  reference reading (rms 0.0640, massive 0.0387 canonical; 0.0559 / 0.0332 alt, f = 1.00) is reproduced as check K2.

## Model (the joint's layout for a cluster-regime disc) and inputs

- Halo: FRZ1's (`closure_2026_11_10/FRZ1_forest_redistribution_at_z/frz1_hm.py`, via SRH1's / SRJ2's loaders):
  M_ta = X M_b h / (1 - FB), X = XTAB[foot]["z0.0"] if z < 1 else ["z1.0"] (PD1 share medians, SRJ2's rule),
  `halo_basics_z` with `set_z(z)` concentration (Duffy), Delta_ta = `dta_of(z)`, Omega_m(z). Radii comoving Mpc/h;
  physical r = r / (1 + z) / h (the convention in FRZ1's `v_vir`).
- Cold mass inside r: C_R(r) = X M_b m_nfw(r / r_s) / m_nfw(c_ta), r capped at r_ta (SRH1's `CR`, generalised to z by
  the halo at z above; identical at z = 0).
- Baryons at R_e: g_bar = G (M_b / 2) / R_e^2 (DD1's construction; thin exponential disc gives the same to 1 %).
- Prediction: g_mod = g_bar + G C_R(R_e) / R_e^2. Observed: g_obs = V_c(R_e)^2 / R_e.

## Statistic and line (inherited from DD1, `fable52_push/DD1_deduce_from_data/FROZEN_CRITERIA.md`, 2a3f76f295)

Y = log10(g_obs / g_bar), F = log10(g_mod / g_bar), d = Y - F per galaxy (one point per system). e = sqrt(0.087^2 +
0.20^2) = 0.218 dex (DD1's RC100 errors). Class: off = median(d); se = max(1.2533 x 1.4826 MAD(d) / sqrt(n),
sqrt(sum e^2) / n). **Line, per footing: |off| <= 0.10 dex AND |off| <= 3 se.** No earlier frozen RC100 line grades a
cold halo; DD1's class line is the record's RC100 fit line, so it is inherited unchanged.

Reported, not graded: per-galaxy count with |d| <= e; off in two z halves and two M_b halves (shape); the author
f_DM against the model's f_cold = C_R / (C_R + M_b / 2); the same statistic on the 69 / 78 galaxy-regime discs under
the law glaw(g_bar, a0) as context.

## Labels (per footing, "canonical / alt")

- **REFERENCE FITS**: line holds. The joint's G2 miss is then a coverage technicality; its only real miss is KiDS
  early-type lensing (0.012 / 0.037 sigma).
- **REFERENCE FAILS**: line fails. The joint is dead on rotation curves for a physical reason; the sign of off says
  whether the reference halo puts too much (off < 0) or too little (off > 0) mass inside R_e.
- **NO VERDICT (no power)**: n < 5, or a required twin does not bite.
- **NOT EVALUABLE**: the observed V_c cannot be read for the sample (not expected: it is on disk).
Neither FITS nor FAILS is a pass of the theory.

## Bracket

X: each footing re-run with X = XTAB[foot]["z0.0"] and with X = XTAB[foot]["z1.0"] for every galaxy (the two values
the record holds, "about 56 to 59"), sample fixed at K1's. **FRAGILE** if the word changes inside the bracket. No
bracket on v_stiff or c (none frozen in the record); not explored.

## Checks (must pass, else NO VERDICT)

- **K1:** SRJ2's counts reproduced exactly: 31 / 22 cluster-regime, covered 69 / 78 at f 0.75, 1.00, 1.25; names
  equal srj2_rc.json's.
- **K2:** SRJ2's reported SPARC reference reading reproduced to 1e-4 (0.0640 / 0.0387; 0.0559 / 0.0332).
- **K3:** loader: 100 rows; every primary galaxy has finite V_c, R_e > 0.
- **K4:** at z = 0 the generalised C_R equals SRH1's CR to 1e-10 (one galaxy mass, X0).
- **K5 (SI, second route):** for the median primary galaxy, recompute r_200c from rho_c(z) = 3 H(z)^2 / (8 pi G) in SI
  and g_mod in SI from scratch; agree with the script to 1 %.

## Mutation twins (outputs `srj3_MUTATE_<name>.json / .out`)

A twin bites if |off_twin - off| >= 0.05 dex or the word changes. **Must bite: TW-N, TW-H.** TW-L reported.
- **TW-N:** no cold component (g_mod = g_bar).
- **TW-H:** halo mass halved (X -> X / 2).
- **TW-L:** law restored in the cluster-regime discs (g_mod = glaw(g_bar, a0), SRH1's glaw and A0).

## Seen before freezing

This brief; SRJ2 RESULT.md; srj2_rc.py; the K1 counts 31 / 22 from srj2_rc.json (SRJ2's numbers); srh1_rc.py lines
1-62 and srh1_hm.py lines 1-40; FRZ1 frz1_hm.py's halo_basics_z, v_vir, Xsh, dta_of lines; fld1_compare.py's rc100();
the RC100 CSV header and its first two rows (U4 38210, U4 20688); the provenance README's first 15 lines; DD1
FROZEN_CRITERIA lines 40-75 and 104-117; grep hits of RC100 in other criteria files; parts of paper_numbers.py's
rc100_run and CFG237_common.py. No SRJ3 number and no V_c of a primary galaxy.

## Hand estimate (before any number)

A z ~ 2 disc with log M_b ~ 11.2: halo ~ 10^13 Msun, r_200c ~ 210 kpc physical, c ~ 3.5, r_s ~ 60 kpc; R_e ~ 6 kpc
gives x ~ 0.1, m_nfw(0.1) / m_nfw(3.5) ~ 0.006, cold mass ~ 0.35 M_b inside R_e against M_b / 2 baryons: F ~ +0.23.
RC100's massive discs have low dark fractions (~0.2), Y ~ +0.1. Expect off ~ -0.10 to -0.15 (reference too heavy
inside R_e). P(REFERENCE FAILS, off < 0) 0.50; P(REFERENCE FITS) 0.40; P(FAILS, off > 0) 0.05; NO VERDICT 0.05.
Alt (22 discs, the most massive) similar. TW-L: probably bites (law at g_bar ~ a0 adds ~0.2 dex).
