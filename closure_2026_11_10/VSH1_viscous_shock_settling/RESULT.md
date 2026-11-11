# VSH1 RESULT: AKS1's estimate T7, computed (2026-11-11)

**Label, canonical and alt: NO VERDICT / NO VERDICT as frozen. Under AMENDMENT A1 (post hoc): SETTLES BY SHOCK / SETTLES BY
SHOCK.**

- **As frozen** the lane has no verdict: known answer KA3 fails, and the two log M_b 11.5 runs stopped at the script's
  step cap before z = 0. KA3 was mis-specified (it assumed the fluid terms leave the turnaround radius alone; they do
  not), and the cap was a script guard. A1 replaces KA3 by KA3' and raises the cap. A1 was written after every first-run
  output had been read. The first run is kept in `first_run/`.
- **Under A1** every known answer passes, every MUTATE arm bites, and all six graded runs reach z = 0 SETTLED.

**Answer in plain words.** AKS1 Part T closed its branch D-V(h) (a viscous clock with the heat kept) on an estimate: to
settle a halo out to CFG461's edge r_e* by today the viscosity must be at least r_e*^2/t0, and the forest allows 8.2 / 6.8
times less than that at log M_b 11.5. Computed, that bound does not hold. With the largest viscosity the forest allows,
the clock's charge is at rest and in pressure balance inside r_e* at every mass, and has been since z = 5.0 / 3.5 / 1.5
(log M_b 9 / 10.5 / 11.5; alt 5.1 / 3.7 / 1.7). A flow that folds settles behind a shock, not by diffusion across the halo.

**So D-V(h) does not close on T7.** This lane does not say the branch is open. One reported number points at what closes
it instead: the amount. The charge inside the whole settled region is 1.4 M_b at every mass, which is 1.1 to 3.5 % of the
law's halo mass at that radius (39 to 139 M_b). A settled clock "with charge equal to the phantom" is short by 28 to 95
times in FLD1's infall model. That is COL1's and FLD1's supply shortfall again. It is reported here, not graded.

TEST lane, quarantined. Adopts nothing, relabels nothing (AKS1's labels stand as recorded), registers nothing. Footings
never pooled. Cold dark energy is a field, never a particle. Criteria `FROZEN_CRITERIA.md`, committed alone before any
script or number; `AMENDMENT_A1.md`, post hoc, committed alone. Because the label rests on a post hoc amendment, it needs
an independent regrade before any paper quotes it as a verdict.

## Graded runs (nu = nu_F, N = 600, gamma = 5/3, z = 0; `vsh1_grade.out`)

| footing | log M_b | r_e* (kpc) | R_sh (kpc) | S inside r_e* (line 0.10) | SETTLED | shock past r_e* at z | R_ta (kpc) | charge inside R_sh / law's halo there |
|---|---|---|---|---|---|---|---|---|
| canonical | 9 | 7.2 | 153.9 | 4.0e-5 | yes | 4.96 | 57.9 | 1.45 / 126 M_b = 0.012 |
| canonical | 10.5 | 40.5 | 410.3 | 2.2e-5 | yes | 3.45 | 259.6 | 1.41 / 59.8 = 0.024 |
| canonical | 11.5 | 127.9 | 836.6 | 1.7e-4 | yes | 1.46 | 565.0 | 1.37 / 38.6 = 0.035 |
| alt | 9 | 6.5 | 153.9 | 3.2e-5 | yes | 5.08 | 57.9 | 1.45 / 139 = 0.011 |
| alt | 10.5 | 36.8 | 410.3 | 1.6e-5 | yes | 3.65 | 259.5 | 1.41 / 65.7 = 0.021 |
| alt | 11.5 | 116.4 | 836.5 | 1.3e-4 | yes | 1.65 | 564.9 | 1.37 / 42.4 = 0.032 |

Hydrostatic residual inside r_e* (median |pressure force + gravity| / |gravity|): 1.5e-5, 2.4e-8, 8.6e-9. AKS1's T7 margins
nu_S/nu_F at these masses are 0.03 / 0.82 / 8.17 (alt 0.02 / 0.68 / 6.77): the run at 11.5 settles with a viscosity 8.2 /
6.8 times below nu_S.

## What the hot region is at nu_F (read this before quoting R_sh)

At nu_F the hot region reaches beyond the turnaround radius at every mass (R_sh/R_ta 2.66 / 1.58 / 1.48). There the frozen
"hot" rule is met by viscous heating of the whole converging flow, where r|g| is small, not by a thin shock. The physical
viscosity supplies 79 % / 28 % / 13 % of all the heat at log M_b 9 / 10.5 / 11.5; shock capture and compression supply the
rest. So at the two lower masses the settling is partly diffusive, as AKS1's small margins there say, and at 11.5 it is a
shock. The viscosity also changes the outer flow: R_ta is 57.9 / 259.6 / 565.0 kpc against 87.7 / - / 597.0 with every
fluid term off. The graded statement uses only the region inside r_e*, where S is 1e-4 or less in every run.

First run, shock capture only (nu = 0), stopped at the old cap before z = 0 (`first_run/vsh1_scan.out`): the hot region
ended at 0.47 / 0.41 / 0.36 of R_ta, and had passed r_e* at z 3.45 and 2.22 for log M_b 9 and 10.5. The amended scan
(nu = 0 and 0.1 nu_F to z = 0, 10 nu_F and gamma = 4/3 at 11.5) was still running when this was written and will be added
in a later commit. It is reported only.

## Known answers and MUTATE (`vsh1_ka.out`, `vsh1_MUTATE.out`)

| item | result |
|---|---|
| KA1 Noh (spherical, gamma 5/3) | PASS: shock at 0.2036 (exact 0.2000), post-shock density 60.9 (64), energy drift 3.6e-3 |
| KA2 Hubble flow, no baryons | PASS: max (gamma - 1) e = 3.5e-16 (km/s)^2, no hot zone |
| KA3 as frozen (R_ta with the fluid on against FLD1) | **FAIL**: 57.9 against 88 at log M_b 9; the 11.5 run had not reached z = 0 |
| KA3' (A1): fluid terms off against FLD1's R_ta | PASS: 87.7 (88) and 597.0 (600) |
| KA4 resolution, log M_b 10.5 | PASS: R_sh 397.0 (N 300) against 410.3 (N 600), both SETTLED |
| M1 heat removed | BITES: no hot zone; two masses tangle within 500 steps |
| M2 no baryons | BITES: nothing turns around |
| M3 stopped at z 6, log M_b 11.5 | BITES: R_sh 16.3 kpc against r_e* 127.9, S 0.57 |

## Hypotheses and limits

- The model is FLD1's shell equation as written, with the clock's charge given a pressure (gamma = 5/3), a traceless shear
  viscosity and shock capture. The force law is not changed inside the settled region. "Settled" means at rest and in
  pressure balance. Whether a settled clock then carries the law for the baryons' field is AKS1's premise, not tested.
- Spherical symmetry; a regular centre; no cooling.
- nu_F, r_e* and R_cap are AKS1's, read from `aks1_t.json`. The forest bound itself is AKS1's conversion, an estimate.
- The amount (1.4 M_b inside the settled region) is in FLD1's infall model, where a galaxy is a seed of mass M_b in a
  smooth universe. PD1's counted-once share (59.5 M_b) assumes a much larger region; the two pictures differ.
- Not re-run by anyone else. No Lean file: no structural claim is made.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `vsh1.py` (modes ka, grade, mutate, scan; about 35 min for the two 11.5 runs),
`vsh1_ka.*`, `vsh1_grade.*`, `vsh1_MUTATE.*`, `first_run/` (the first run's outputs, as frozen), this file.
Re-run: `python3 vsh1.py ka && python3 vsh1.py grade && python3 vsh1.py mutate` from this folder.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
