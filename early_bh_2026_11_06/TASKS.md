# Early black holes in the framework: task list (2026-11-06)

Owner ask: "come up with a task list based on all this and do the work we can do now, building off what we have,
without duplicate work". The question is *when* in cosmic history black holes can form under v3s / the a0 law,
against the earliest weighed black holes. Kappa = 1/2 FITTED; not theory closed. No dark-matter particle.
Lane prefix EB (no EB ids on the record before this file).

## What the record already settles (not redone)

| Item | Where | What it says |
|---|---|---|
| Static BH / NS strong field | rebuild_2026_10_22/P3_v3_strong_field | GR to <= 2.9e-11; regular holes need an infalling khronon; screened X-point at 3.65 M; capped SMBHs have free charge |
| BH / horizon / a0 geometry | campaign_fresh_gravity/CFG775 | every relation is q = 1/Z; stellar BHs cannot be dark energy's source |
| BH contribution to galaxy/cluster gravity | horizon_cluster_2026_11_05 (HC-001..011) | BHs are 0.1 % of host monopole; horizon areas do not touch 32 pi |
| BH* / LRD regime coincidence | real_research/bhstar_audit_2026 | NOT a framework result |
| A2744-QSO1 phantom bound on a0 at z 7.04 | L324 / Lean I18 (bhstar audit) | flat a0 passes at 10^7.7, fails at 10^6.9; mass-reading limited |
| High-z galaxy dynamics, flat vs rival a0 | campaign_fresh_gravity/CFG269 | no bin separates the laws with public data |
| Early-galaxy formation / abundance | opus_48 review 2026-06-19 | "structurally silent": a0 absent from linear growth in the completion used then |
| Linear growth + CMB-lensing shape in the action | closure_2026_11_06/QX3, WG1-WG6 | FAIL for every mechanism; baryons-only start is Silk-damped; law boosts largest scales |
| Baryons-only CLASS start + QUMOND web rule | rebuild_2026_10_22/WG2 | the record's one rule for the law on the web (R1), with engine checks |
| Nonlinear khronon-dust collapse | rebuild_2026_10_22/AN1, AN2 | NO VERDICT (clock fold, not baryon collapse) |

## Tasks

| id | task | status | why / blocker |
|---|---|---|---|
| EB0 | Record inventory and dedupe (this file) | DONE | |
| EB1 | Seed epoch: baryons-only sigma_b(M) to 1e6 Msun; spherical collapse z of baryon clumps under R0 (Newton) and R1 (WG2's QUMOND rule), both footings, EFE bracket; Eddington seed-time requirement for A2744-QSO1 from the record's masses; timing gate | DOABLE NOW | reuses WG2 inputs; small single-thread job |
| EB2 | Abundance: number density of clumps that collapse in time vs the observed density of z 4-8 broad-line AGN / LRDs | NEXT | needs a published number density (page read, provisional until checked) |
| EB3 | Add UHZ1 (z 10.1) and GN-z11 (z 10.6) to the timing gate | NEXT | masses not on the record; needs page reads checked against the papers |
| EB4 | Gas physics: Jeans and cooling mass of baryon clumps under the law (atomic / H2 cooling at z 10-30) | NEXT | analytic; follows EB1's collapse masses |
| EB5 | Fragmentation: does the first (Silk-scale) collapse fragment into seed-mass pieces? | LATER | needs a 3D run; heavy compute waits until AC24 / QX17A are off the machine |
| EB6 | Clock during collapse: does the khronon foliation tilt smoothly (P3's infalling branch) or fold (AC10 / AC14) as a star collapses? | LATER | joins the open fold lanes (AC14 RUNNING); do not start a parallel fold solver |
| EB7 | a0(z) lever: flat (TIE) vs rival a0 E(z) on seed timing | IN EB1 | reported row, not a discrimination |

Caveat carried into every row: the R1 web rule fails the CMB-lensing shape (WG2-WG6) and growth inside the action
fails (QX3). EB1 is therefore conditional on a rule the record already grades FAIL elsewhere; it asks only whether
that rule could form seeds in time, not whether the framework does.
