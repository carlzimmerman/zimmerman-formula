# CFG579 FROZEN CRITERIA — KiDS North/South split of the CFG529 f30 result

(owner chat 10-09, "do the KiDS north/south split"). Committed alone before any script.

Question: CFG529 found the census edge FAILS on the strictly isolated f30 lenses in a validated environment (both
footings, both constructions) while ΛCDM passes. Is that fail present in BOTH KiDS sky regions, or carried by one?

Regions (lens Dec from lr_lenses.npz): NORTH = Dec > −15°, SOUTH = Dec < −15°. Pre-flight counts (no lensing read):
f30 NORTH 27,593, SOUTH 29,672; jackknife patches 25 / 25, disjoint.

Pipeline: CFG529's cfg529_score.py executed UNEDITED except three run-time string substitutions, each asserted to
apply exactly once: (1) F30 → F30 & region; (2) the f30 covariance (below); (3) output paths → this lane.
The stack-P and ALL samples, environment tables (measured f30 leakage 0.1686) and models are untouched.
Covariance PRIMARY: CFG529's 50-patch f30 jackknife covariance scaled per bin pair by √(r_i r_j), r = (lens-weight
 sum, all f30) / (lens-weight sum, region), per radial bin (keeps the 50-patch precision; assumes the same shape).
VARIANT (reported): region-only 25-patch jackknife with the Hartlap factor for 25 patches.
Per region, construction (A sharp, B smooth), footing:
 ΛCDM PASSES iff p > 0.01 (CFG529's G2f-type check on the region).
 Census edge FAILS iff CFG529's own PASS flag is false (Δ vs best sharp edge > 4 OR p ≤ 0.01).
 A region REPLICATES iff ΛCDM passes and the census edge fails, in BOTH constructions on BOTH footings.
Verdict: REPLICATED IN BOTH REGIONS (not a regional artefact) / ONE REGION ONLY (regional systematic suspected) /
 NEITHER: then LOW POWER if the census edge passes in a region where the full-sample Δχ²(census − ΛCDM) scaled by the
 region's share of lens weight is < 10, else NOT REPLICATED; ENVIRONMENT INVALID for a region where ΛCDM fails.
Reported: χ²/15 and p for every CFG529 model per region; Δχ²(census − ΛCDM); inner-9 χ².
Controls: C1 NORTH ∪ SOUTH covers every f30 lens and the regions are disjoint; C2 identity run (region = all f30,
 primary covariance = CFG529's own) reproduces CFG529's census and ΛCDM χ² to 1e-6; C3 the substitutions each
 apply once.
Tooth (MUTATE-equivalent): the law to r_ta (f_ret = 1 analogue, CFG529 model LAW_RTA) must FAIL (p ≤ 0.01) in both
 regions; if it passes anywhere the split has no power there.
κ = ½ fitted; footings never pooled; cold energy's mass required; not theory closed.
