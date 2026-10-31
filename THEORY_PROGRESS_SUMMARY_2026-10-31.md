# THEORY PROGRESS SUMMARY, 2026-10-31, with instructions for the re-footing pass (RF1–RF6)

Written for the next agent (Opus 5.5). Read this whole file, then `STANDING.md`, `LEDGER.md`,
`rebuild_2026_10_22/THEORY_STATEMENT_2026-10-26.md` and the memory index rules before any lane.
κ = ½ FITTED. Footings (canonical ρ_Λ, alt ρ_total) graded separately, never pooled. Not "theory closed".
Nothing in this file says the data favour the framework.

## 1. Where the theory stands (owner-adopted flagship, 2026-10-25)

Flagship = the a0 law (a0 = κc√(Gρ_DE), κ = ½ fitted, a0 tracking dark energy, native band a0(z) ≈ 0.91–0.94 local
to z 2.33 from raw BAO, CFG689) + the cold dark energy core law (route E, Σ ∝ σ^q, q fitted on SPARC).
v3s is the covariant attempt and is frozen (V3S_FINAL_VERDICT_2026-10-24.md). Cold dark energy is a gravitating
field component, never "cold dark matter" and never a particle.

What holds on the framework's own footing:
- SPARC rotation curves under the a0 law (Υ within the stellar-population range on canonical; alt needs κ ≤ 0.44, X78).
- a0(z) tracking from raw BAO geometry (CFG680–685, CFG689), pre-registered ALMA (CFG570/571, CFG806/809) and
  Gaia DR4 (frozen) tests.
- Route E passes the 15 cluster keys only with external c_f ≈ 4 or stipulated η; native zoom cores are NFW cusps through
  the softening cut (X81) and converged η fails route E on both footings (CE1/BE1).

## 2. The review that triggered this pass (2026-10-31)

The six "failures" below were quoted as failures of the framework. A read of the lanes' own ledgers shows that four of
them are measured partly against the rival model (ΛCDM-processed inputs) or against unledgered astrophysics.
None of them may be quoted as a failure of the framework until redone on the framework's own footing.

| front | current verdict | what is baked in that is not ours | ledger status |
|---|---|---|---|
| Milky Way under route E | FAIL on McMillan 2017 (GD1); short disc passes, wide priors only (GD2) | McMillan 2017 disc normalisations come from a joint fit with an NFW halo (X5 and S3 ledgers: "partly ΛCDM-PROCESSED"); Portail+17 bulge mass has a dark halo in the fit; 2M++ external field is ΛCDM-processed | ledgered, flagged, never acted on |
| IC 1613 under the law | FAIL (IN1 frozen falsifier, IN2 MUSE i = 36° ± 11°) | Read+16 inclination formalism; one number with an 11° error | ledgered; weak evidence either way |
| cluster excess Z 4.1–5.5 and the 15 keys | excess stands; route E passes only at external c_f | hydrostatic equilibrium for the comparison masses; f★ 0.034/0.0615 from stellar M/L; Planck 5.364 inherited until X73; grader defect in 4 outer keys since X71/GS1 | partly ledgered |
| lensing (KiDS, satellites, kSZ) | shortfall; satellite +0.78 is a method systematic (GH1) | GH11: two-halo template "inherits ΛCDM initial conditions", unusable; miscentring correction unmeasured; shape misfit, not a settled number | partly ledgered |
| covariant completions: growth / CMB | FAIL (v3s §F3, X4, L1) | σ₈ scored as σ₈/σ₈,ΛCDM; cold-component timing in patched CLASS on a ΛCDM-style background; only the SN+BAO exchange bound is marked "no ΛCDM-derived inputs" | the growth row is measured against the rival's yardstick |
| core mechanisms (BH1/2, CM1–3, CL5, SH1) | NOT REACHED | SN energy per event, IMF, cooling functions, zoom softening (X81: cores are the ε cut); the "need" is route E's η, which depends on SPARC's Υ | NO ASSUMPTION LEDGER in any of these lanes |

Cleanest of the six: IC 1613 and the cluster excess (outside inputs present but labelled).
Least clean: Milky Way, growth/CMB, core mechanisms.

## 3. Standing rules for every RF lane (owner rules; do not relax)

1. RAW DATA or FRAMEWORK-NATIVE inputs only. No Planck parameters, no ΛCDM background, no ΛCDM σ₈ or growth
   factor, no halo-fitted baryon normalisations, no "passes by construction". Where a published input was produced
   inside a fit that contained a dark halo, it is ΛCDM-PROCESSED and may enter only as a labelled bracket, never as
   the graded value.
2. Every lane ships, in this order, each as its own commit: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (classes
   RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT, as in
   X5), then the script, then `README.md` with the verdict. Criteria are frozen before any number is seen.
3. Before taking a lane id: `ls rebuild_2026_10_22 | grep RF` and `git log --oneline | grep RF`. The RF prefix is
   unused as of this commit. Do not reuse X, GD, GH, CM, BH, CL, SH ids.
4. Scripts run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I`, exit 0 on the result, and ship a
   MUTATE mode (`<ID>_MUTATE=1`) that must fail the intended checks. Outputs named by mode. Margins read from JSON;
   tolerances stated in the criteria.
5. Both footings, graded separately. Report canonical and alt in every verdict table.
6. Compute: while a 1024³ run is live (check `compute_queue`), jobs stay under 1 GB RSS, one thread, minutes.
   Anything heavier is preemptible: checkpoint on SIGTERM, resume via `compute_queue`.
7. Verify a fail as hard as a win. A verdict that flips from FAIL to PASS because an outside input was removed is
   reported as "not a framework failure", not as "the framework passes".
8. No personal references in committed files. Commit locally; push only finished lanes, batched.
9. Every README ends with: κ = ½ FITTED; c_f EXTERNAL where used; cold dark energy is a gravitating field component,
   never a particle; not theory closed; nothing here says the data favour the framework.
10. If a lane's clean footing does not exist in the record or the literature (for instance a Milky Way baryon census
    that was never fitted with a halo), say so and stop; do not substitute a ΛCDM-processed value and grade on it.

## 4. The six lanes

### RF1_mw_halo_free_baryons: Milky Way under route E on baryons never fitted with a halo

Question. Does route E (OS1-cored cold dark energy halo on Newtonian baryons) miss V_c(R₀), K_z(R₀, 1.1 kpc) and the
Ou+24 curve when the baryons carry no halo in their derivation?

Build the baryon field from these only: McKee, Parravano & Hollenbach 2015 Σ_b(R₀) = 47.1 ± 3.4 (star counts + gas,
no dynamics; already in the record at `hunt_2026/g02_vertical_vs_planar_frequency_split.py`); star-count disc scale
lengths (Bland-Hawthorn & Gerhard 2016 review range; Licquia & Newman 2016); HI/H₂ surface densities from the gas
surveys directly, not McMillan's fit; a bulge/bar mass from photometry or microlensing (label the source class; if
only made-to-measure values with a dark halo exist, as Portail+17, bracket them and say so). Candidate halo-free bulge
sources to verify from the papers themselves (LITERATURE-INPUT, PROVISIONAL until read): Kent 1992 (2.4 μm Spacelab
maps), Dwek et al. 1995 (COBE/DIRBE photometry with an assumed M/L), pre-M2M clump-giant counts; each enters as a row
with its own M/L assumption stated, never as a single adopted value. Hold McMillan's vertical
shapes only where the ledger shows they come from star counts. External field: e_N = 0 and a Newtonian LMC + M31
estimate from their own masses, not the 2M++ reconstruction.

Grade. GD1's three keys at GD2's thresholds (cite the commit hashes). Scan only the published-prior box; nothing
fitted. Report the fraction of the box that passes and whether the GD2 short disc lies inside the halo-free priors.

Verdict wording. "FAIL on halo-free baryons" or "PASS on halo-free baryons" or "UNDETERMINED: no halo-free bulge
mass exists". The GD1 McMillan verdict is then re-labelled in LEDGER.md as "FAIL against ΛCDM-processed baryons".

### RF2_ic1613_inclination_footing: IC 1613 without the single MUSE number

Question. How much of IN2's failure rests on the Read+16 stellar-kinematic inclination?

Do. (a) Re-derive the law's prediction for both tracers across i = 15°–50° with the HI and stellar velocity data
IN1 used (no new data). (b) Replace the MUSE 36° ± 11° with each independent inclination estimate that does not go
through a mass model: HI morphological axis ratio from the moment-0 map, optical isophote axis ratio, tip-of-the-RGB
geometry if published. Each estimate is a row; state its class. (c) Give the likelihood of IN1's frozen band
(18.5–26.5°) under each estimate.

Verdict wording. "FAILS under every halo-free inclination", "FAILS only under the MUSE kinematic value", or
"UNDETERMINED (no independent inclination better than ±10°)". No new falsifier is frozen here; IN1's stands.

### RF3_cluster_keys_hse_free: the 15 cluster keys without hydrostatic masses, Planck, or the old grader

Question. With the comparison masses taken from caustics and weak lensing instead of hydrostatic equilibrium, the
baryon fraction from the framework's own Ω_c/Ω_b and the measured gas, and the grader rebuilt, what is the cluster
excess and do route E's 15 keys still need external c_f?

Do. (a) Fix the grader defect in the four outer keys (noted 10-31, template inherited from X71/GS1) and re-score
X73, GS1, ZN1 and MA1 with the fixed grader before anything else; report what changed. (b) Comparison masses: X-COP
caustic and weak-lensing masses where published, Zwicky-style caustic masses from the record's X14 machinery
otherwise; HSE masses as a labelled bracket only. (c) Gas: X-COP and eRASS1 raw profiles to r_ta as in X73.
(d) f★: from the measured BCG + ICL + satellite light with a stated Υ range, not the two fixed values; carry the
range through as a band. (e) No 5.364 anywhere; confirm by grep of the script.

Verdict wording. Z excess as a band per footing; keys passed at native c_f (from X77's smooth-core fit to the zooms)
and at external c_f = 4, separately. The grader fix is its own commit before the physics.

### RF4_lensing_native_template: KiDS and kSZ with no ΛCDM-conditioned template

Question. What is the lensing and kSZ shortfall of route E when the one-halo profile, miscentring and the two-halo
term are all built from data or from the framework, not from an N-body-calibrated halo model?

Do. (a) One-halo: route E's own Σ(σ) profile with the X73 gas, no NFW. (b) Miscentring: measured from the lens
sample's BCG-to-X-ray or BCG-to-satellite-centroid offsets (GH11 has the satellite fraction 0.28; use it, do not
model it from simulations). (c) Two-halo: a data-built template from the stacked galaxy-galaxy clustering of the
same lens sample times a linear bias measured in the same sample, with the framework's own growth (from RF5, or if
RF5 is not done, state the growth as an input band). No ΛCDM initial conditions. (d) Re-grade GH1's matched-host
lensing, GH9/GH10's kSZ A(1.8) and A(1), and the KiDS stack of TL1 (law 66, route E 141) with this template.

Verdict wording. Shortfall per footing as a band; separate "normalisation" from "shape" as GH9/GH10 did. If the
two-halo cannot be built from the sample's own clustering at the needed scales, say "two-halo UNSEPARABLE" and grade
only inside the scale where it is negligible (GH1's 300 kpc).

### RF5_growth_native_yardstick: linear growth and the CMB on a background built from raw BAO and SN

Question. Does the cold dark energy sector of v3s (and the flagship's cold core law treated as a cosmological
component) fail growth and the CMB when the background and the yardstick are the framework's own?

Do. (a) Background: H(z) from raw BAO (CFG680–685) and DES-SN5YR (the exchange-bound machinery in the v3s verdict is
marked ΛCDM-free; reuse it). ρ_DE(z) and hence a0(z) from CFG689's native band. No Planck parameters. (b) Yardstick:
raw observables only. Ly-α forest flux power with the record's b-cutoff correction (never the withdrawn 6–8σ); the
CMB TT/TE/EE spectra as data, with the framework's own transfer function from the patched CLASS branch, scored by χ²
against the spectra, not by σ₈/σ₈,ΛCDM; KiDS/DES shear two-point functions as data with the framework's own growth,
not their published S₈. (c) The cold component's turn-on epoch is a free parameter scanned, with its energy
conservation as in v3s §234; report the raw-data χ² surface, not Δχ² relative to ΛCDM.

Verdict wording. "FAILS on raw forest + CMB spectra + shear at every turn-on epoch" or "a window exists at
z_on ∈ [..]" per footing. The v3s F3/X4/L1 rows are then re-labelled "measured against ΛCDM σ₈" in the verdict file,
in a dated addendum; committed lane text is not rewritten.

### RF6_core_mechanism_ledgers: assumption ledgers for BH1/BH2, CM1–CM3, CL5, SH1, then one re-grade

Question. Which of the "NOT REACHED" core-mechanism verdicts survive when the astrophysical inputs are ledgered and
the need is stated on the framework's footing?

Do. (a) Write an ASSUMPTION_LEDGER.md for each of the seven lanes, after the fact and dated, classing every input: SN
energy per event and the IMF behind the SN rate, cooling function and metallicity, zoom softening ε and the X81
convergence result, black hole mass scalings, closed-box assumption, and the η "need" (route E's η at SPARC's Υ, with
X78's Υ range). (b) Identify the single input in each lane whose plausible range moves the verdict most. (c) Re-run
only CM1 and CL5 (the SPARC and cluster anchors) with that input scanned over its ledgered range and the η need
carried as a band over Υ 0.44–0.57 (X78, LS1). No new mechanisms. No knob scans beyond the ledgered range.

Verdict wording. For each lane: "NOT REACHED, robust to the ledgered ranges" or "NOT REACHED only at the fiducial
input; reached at <input> = <value>, which is <inside/outside> its published range". The converged-η failure of route
E (CE1/BE1) is not touched by this lane and remains the governing result.

## 5. Order and stopping rule

Run RF3(a) (grader fix) first, since it changes numbers other lanes read. Then RF1, RF2, RF6 (small, local, under
1 GB). RF4 and RF5 last; RF5 is the only heavy lane and must be preemptible. After the six verdicts, update
`FAILURES_EXECUTIVE_SUMMARY` with a dated section that separates "fails on the framework's footing" from "failed only
against ΛCDM-processed inputs" from "undetermined". Open no seventh lane. If a lane's clean footing does not exist,
record UNDETERMINED and move on; that is a result.

κ = ½ FITTED. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing in
this file says the data favour the framework.
