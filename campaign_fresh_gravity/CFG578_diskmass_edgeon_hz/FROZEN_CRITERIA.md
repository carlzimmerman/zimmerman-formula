# CFG578 FROZEN CRITERIA — DiskMass σ_z with MEASURED edge-on disc thicknesses (S4G 3.6 μm)

(owner chat 10-09, "use measured edge-on disc thicknesses"). Committed alone before any script.

DiskMass galaxies are face-on; their h_z cannot be measured directly. DMS used log(h_R/h_z) = 0.367 log(h_R/kpc) +
0.708 (DMS II, arXiv:1004.5043, I-band edge-on compilation, z0 = 2 h_z convention; verified in source TeX).
Independent calibration used here (source TeX, arXiv:2410.09762, 46 S4G edge-ons at 3.6 μm, old-star tracer):
 log10(h_z/kpc) = 0.90 log10(h_R/kpc) − 0.81, scatter 0.11 dex, same z0 = 2 h_z convention.
 (Bizyaev et al. 2014 was NOT used: only a search summary was seen, its definitions are unverified.)

Pipeline: CFG577's script functions by execution, unedited (grid solver, exact LOS-weighted Jeans integral, Υ_K
fitted per galaxy and model, ν_mono, both footings never pooled, κ = ½ fitted); the only change is h_z per galaxy
from the S4G relation with DMS VII's h_R.
Gates:
 G-Υ (from CFG577): ≥ 25/30 fittable and median Υ_K ∈ [0.3, 1.0].
 CONSISTENT iff median r ∈ [0.85, 1.15] AND G-Υ.
 CFG577's G-cal is DROPPED (declared now, before scoring): CFG577 showed its window was mis-anchored to Angus+15
 fits with free h_z. Replaced by a pipeline control P1: with DMS's own h_z the run reproduces CFG577's primary
 RM and PD medians (canonical, 1.5 h_R) to 0.5%.
Verdict per footing (primary R = 1.5 h_R): ROUND FAVOURED / PD FAVOURED / NOT DIAGNOSTIC as in CFG577; overall =
 same call on both footings, else SPLIT.
Reported (not gates): the S4G ±0.11 dex scatter (h_z × 10^±0.11); 2.2 h_R; Newtonian reference; median h_z ratio
 S4G/DMS over the sample.
MUTATE (CFG578_MUTATE=1): a0 × 10 in RM; RM must NOT be consistent.
Disclosed limits: as CFG577 (TF inclinations, DMS σ_z fits, Jeans closure, gas/bulge shapes); the S4G relation is
 a population mean for Sb–Sdm applied to individual galaxies; κ fitted; cold energy's mass required; not theory closed.
