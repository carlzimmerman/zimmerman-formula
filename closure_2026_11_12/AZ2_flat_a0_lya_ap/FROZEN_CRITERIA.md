# AZ2: flat a0(z) at z 2.33 with the DESI DR2 Lya Alcock-Paczynski pair in place of CFG681's (FROZEN, before any script or graded number)

TEST lane, 2026-11-12. Scope: `reviews/hy4_codex_audit_2026_11_12/A6_desi_euclid_scope.md`, top-five item 1. Theory under test:
a0 = (1/2) c sqrt(G rho_DE), mu(x) = x/(1+x), cold dark energy at 5.41 x baryons counted once. Kill test named by the record:
"a flat a0(z) out to z 2.33". Tracking reading (owner rule, CFG681): a0(z)/a0(0) = sqrt(X(z)), X = rho_DE(z)/rho_DE(0).

## 1. Statistic, exactly as CFG681 defined it (criteria fe91fd3bc6, result e6d43c49a7)

- Model: flat, E(z)^2 = Om (1+z)^3 + Or (1+z)^4 + (1 - Om - Or) X(z); X piecewise-linear on nodes {0, 0.4, 0.7, 1.0, 1.5, 2.33},
  X(0) = 1, 5 free nodes, constant beyond 2.33. Nuisance q = c/(H0 r_d) solved analytically (BAO); SN absolute magnitude
  marginalised analytically (shape only). Om in [0.15, 0.45]. No CMB, no CPL, no LCDM model, r_d free (inside q).
- Data kept unchanged: DESI DR2 BAO (arXiv 2503.14738) BGS D_V/r_d and the five anisotropic galaxy/QSO pairs LRG1, LRG2,
  LRG3+ELG1, ELG2, QSO with their correlations, as typed in `campaign_fresh_gravity/CFG681_bao_raw_geometry/cfg681_bao.py`;
  Pantheon+ STAT+SYS, non-calibrators, zHD > 0.01 (files already on disk, outside the repo; nothing downloaded).
- Graded statistic: sqrt(X(2.33)) = a0(2.33)/a0(0) at the fixed Om grid 0.25 / 0.30 / 0.35 (CFG681's frozen a0 statement), for
  T1 = BAO only and T2 = BAO + Pantheon+ shape. Reported beside: CFG681's T1/T2 Delta chi^2 (X = 1 vs free X, 5 dof) and T3 AP
  chi^2 at the six tracers. T4 (distance duality, z <= 1.5) does not use the Lya pair; it is not re-run.
- Uncertainty: CFG681's penalised profile bands were disclosed as unreliable and not used. Here the profile is taken directly:
  X(2.33) is itself the fifth node, so it is fixed on a grid and the other four nodes are re-minimised (warm-started, Nelder-Mead
  then Powell). Delta chi^2_prof(X5) relative to the free minimum at that Om; 1 dof.

## 2. The one input replaced

| | D_M/r_d | D_H/r_d | r | source |
|---|---|---|---|---|
| OLD (CFG681, DR2 BAO Lya, removed) | 38.988 +- 0.531 | 8.632 +- 0.101 | -0.431 | arXiv 2503.14738 |
| NEW (DR2 Results IV, joint Lya AP + BAO, Eq. 26, z_eff 2.33) | 39.32 +- 0.33 | 8.600 +- 0.066 | 0.225 | PROVISIONAL, read 2026-11-12 from https://arxiv.org/html/2607.27410v3 (abstract https://arxiv.org/abs/2607.27410) |

The NEW pair REPLACES the OLD pair (same Lya data); it is never added. The new pair keeps CFG681's independence assumption
between the Lya pair and the galaxy/QSO tracers. The paper's revised BAO systematic budget is inside its quoted errors as read.
Nothing else from that paper is used (its LCDM Om 0.325 +- 0.018 is NOT used).

## 3. Footings (never pooled)

The ratio sqrt(X) is a normalised quantity; the footing enters through rho_DE(0) = (2 a0 / c)^2 / G, which at each fixed Om sets
h = sqrt(rho_DE(0) / ((1 - Om) rho_crit,100)) and so the radiation term Or(h) = 2.469e-5 (1 + 0.2271 x 3.046) / h^2.
Canonical a0 9.3603e-11 gives rho_DE(0) = 5.842e-27 kg/m^3, h = 0.644 / 0.667 / 0.692 at Om 0.25 / 0.30 / 0.35; alt a0 1.1312e-10
gives 8.533e-27, h = 0.778 / 0.806 / 0.836 (computed before freezing; no graded number). Expected footing effect: <= 1 % on
sqrt X(2.33). Absolute a0(2.33) = a0_footing x sqrt X(2.33) is reported per footing.

## 4. What "flat" means, and the labels (per footing)

- Flat band: a0(2.33)/a0(0) in [0.90, 1.10] (X5 in [0.81, 1.21]; +-0.04 dex). D_band = min of Delta chi^2_prof over X5 in the band.
- Named alternatives (from the record's standing wording): RIVAL a0 proportional to H(z), i.e. sqrt X(2.33) = E(2.33) with E taken
  at X = 1 and the fixed Om (X5 = E^2, about 12); D_rival = Delta chi^2_prof there. The T reading a0 proportional to t(z)/t0 is
  reported only (sqrt X about 0.2), no label.
- Headline cell per footing: T2 (BAO + SN) at Om = 0.30 (CFG681's central grid point). Every (T1/T2) x (Om) cell gets its own
  label, reported beside.
  - NO POWER: D_band < 4 AND D_rival < 4 (the measurement cannot tell flat from a0 proportional to H(z)).
  - FLAT FAILS: D_band >= 9 (flat excluded at 3 sigma, 1 dof).
  - FLAT HOLDS: D_band < 4 and D_rival >= 4. If 4 <= D_band < 9: FLAT HOLDS with a HINT flag (CFG681's 2-3 sigma convention).
  - NO VERDICT: any known answer below fails.
- Expansion-model dependence: the result is conditional on the flat piecewise-X model and on Om, which raw BAO does not fix
  (CFG681's dark degeneracy). If the Om 0.25 or 0.35 label differs from the Om 0.30 label the headline carries the flag
  EXPANSION-MODEL DEPENDENT. An Om-profiled row (Om free) is reported only.
- A FLAT HOLDS is NOT a pass for the theory: it says the tracking law plus this expansion model allow a flat a0 at z 2.33; LCDM's
  constant dark energy gives the same sqrt X = 1, so nothing here separates the framework from LCDM, and it says nothing about a
  kinematic a0 measurement at z 2.33.

## 5. Known answers (grading stops on a fail -> NO VERDICT)

- KA1 (reproduce CFG681 with its original pair, h = 0.68): T1 Delta chi^2 7.41 +- 0.10; T2 12.08 +- 0.10; T3 chi^2 5.98 +- 0.05;
  fixed-Om sqrt X(2.33) T1 1.93 / 1.14 / 0.00 and T2 1.97 / 1.24 / 0.00 each within 0.05 (optimizer jitter).
- KA2 (flat injection): replace every BAO point by its own X = 1 model at Om 0.30 (q from the X = 1 fit), new-pair errors; T1 at
  Om 0.30 must give D_band < 0.05 and best sqrt X(2.33) within 0.03 of 1.
- KA3 (profile sanity): the profile minimum over the X5 grid lies within Delta chi^2 0.1 of the free fit at each Om.

## 6. Mutation (separate `_MUTATE` outputs)

MUTATE = shift the NEW D_H/r_d down by 5 sigma (8.600 -> 8.270), D_M/r_d unchanged. Hand estimate before any number: D_H ~ 1/H, a
3.8 % rise in H(2.33) raises E^2 (~11.8 at Om 0.3) by ~0.9, so X5 rises by ~1.3 and sqrt X(2.33) moves from about 1.2 to about
1.6. Must bite: T2 Om 0.30 best sqrt X(2.33) rises by >= 0.2 and D_band rises by >= 4 relative to the unmutated run.

## 7. Already seen before freezing

CFG681 README and results (T1 7.41/5, T2 12.08/5, T3 5.98/5, fixed-Om sqrt X(2.33) 1.93/1.14/0.00 and 1.97/1.24/0.00, failed
penalised bands); CFG682 README (sigma_X(2.33) 1.7-2.0 BAO only, 0.43-0.51 BAO+SN at fixed Om; flat a0 implies Om 0.3085 +- 0.0075);
CFG689 README (native-ruler band 0.91 [0.33, 1.21] at z 2.33; rival 3.49); the scout's A6 note; the Codex branch
`codex/euclid-desi-review-2026-11-12` REPORT section 5, which quotes the same new and old pairs and says the new one must replace
the old, but RAN nothing (no AP refit exists there; this lane extends it, it does not grade a run). The paper's abstract, Eq. 26,
and Eq. 25 (F_AP 4.572 +- 0.046, not used). My own hand estimate: sqrt X(2.33) about 1.2-1.3 at Om 0.30 (T2), sigma_X about 0.35.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
