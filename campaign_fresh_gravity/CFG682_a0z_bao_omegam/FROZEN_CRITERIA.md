# CFG682 — a0(z) + raw BAO → Ω_m without the CMB (FROZEN, before any number)

Block CFG680–689. Owner "yes" (2026-10-12) to the CFG681 follow-up. CFG681 (e6d43c49a): raw BAO (+SN shape) fits any Ω_m equally,
but ρ_DE(z), and so the owner's tracking a0(z) = κ c √(G ρ_DE(z)), changes completely with Ω_m. Run it backwards: a measured
a0(z*)/a0(0) plus raw BAO fixes Ω_m with no CMB. Compare with the CMB's Ω_m: a late/early consistency test of the tracking law.

## P1 map (same data and X(z) model as CFG681: DESI DR2 table + Pantheon+ STAT+SYS shape; 5 nodes; no CMB, no CPL)
Ω_m grid 0.24–0.36, step 0.0025. At each Ω_m: best-fit nodes and χ²(Ω_m), for BAO only and BAO + SN; X(z*) at z* = 1.0, 1.5, 2.33
with σ_X from the numerical Hessian of χ² in (q or M, nodes) at fixed Ω_m. Report the Ω_m(r) curve for r = √X(z*).

## P2 inversion (forecast; lognormal measurement)
Measurement r = a0(z*)/a0(0) with total error e (dex, INCLUDING the shared baryon-calibration term; e = 0.02–0.30).
Posterior on Ω_m (flat prior 0.24–0.36) ∝ exp(−χ²(Ω_m)/2) · N(log10 √X(z*; Ω_m) | log10 r, √(e² + σ²_log√X)).
Report σ(Ω_m) vs e, and e* where σ(Ω_m) = 0.0073 (Planck 2018 Ω_m = 0.3153 ± 0.0073). Report Ω_m implied by FLAT a0 (r = 1).

## P3 existing record (no new data)
Effective e for the record's best in-regime samples, from committed numbers only: deep-MOND leverage |d log a0 / d log M_b| ≈ 1 (record
lever for g_bar/a0 = 1–4: 2.5–4.8); shared gas calibration 0.128 dex at z ~ 1.2 and none above 1.6 (CFG224); stars ~0.1 dex.
Samples considered: KURVS-CDFS z ~ 1.5 (CFG140/160), the z ~ 1.2 multi-tracer set (CFG224), RC100 / CRISTAL (CFG223).

## Decision rules
- A sample REACHES CMB PRECISION if its e ≤ e*; INFORMATIVE if σ(Ω_m) ≤ 0.03; else NOT INFORMATIVE.
- FLAT-a0 consistency: if the r = 1 Ω_m interval (BAO + SN, e = e*) excludes 0.3153 at ≥ 3σ, tracking + flat a0 + CMB are
  mutually inconsistent (report which); else consistent.
- MUTATE: replace BAO with its own X ≡ 1 best fit (CFG681 M1) → the r = 1 inversion must return that fit's Ω_m.
κ fitted; cold energy mass required; not theory closed.
