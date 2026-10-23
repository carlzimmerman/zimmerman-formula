# F2_outer_lensing: rebuild of the isolated-galaxy outer-lensing shortfall (CFG804 → CFG902 → CFG903)

## Verdict

**Frozen rule: REAL FAILURE** on both footings and at all three external-field values.
**Not robust.** A post-result diagnostic (AMENDMENT A1) shows that my frozen strict sample still leaks about 38 % of
satellites' hosts. With a cleaner host veto, the 0.4–1.1 Mpc shortfall goes away. Beyond 1.1 Mpc the strictest stack
turns negative, which is the isolation hole of the selection. On that reading the outer data cannot test an isolated
galaxy's own profile: **UNDECIDABLE**. The frozen class is reported first and is unchanged.

Three findings hold on any reading:
1. **The record's +100 is a catchment-edge artefact.** The covariant theory has no supply edge: the phantom is a field
   response (C4). Removing the edge takes the record's far-outer amplitude A_O2 from 2.45 ± 0.17 to 0.96 ± 0.07
   (canonical). Δχ² goes from +100.1 to 0.
2. **Any measured external field makes the theory's own outer prediction far too small** on B21's sample. This is
   true with the AQUAL equation solved exactly. Even the weakest on-disk field (Chae+21 "noclu", y_e = 7.8e-4) gives
   A_O2 = 4.45 ± 0.31; "maxclu" gives 12.2 ± 0.8. B21's sample allows only y_e ≲ 3e-5 (x_e ≲ 0.006).
3. **The "isolated" stack's outer signal is set by the environment.**
   - From the base sample to the strict sample, the outer amplitude falls by 0.74 ± 0.09 (8.6σ; y_e = 0 units).
   - B21's own spectroscopically isolated GAMA lenses sit at 0.64 ± 0.15 of the photo-z isolated KiDS lenses at
     g_bar < 3e-14 m/s².
   - B21's "all" sample sits at 1.46 ± 0.06 of the isolated one.

κ = ½ FITTED. Footings are never pooled. No dark-matter particle. Not theory closed. Nothing here says the data favour
the framework.

## What was done

Criteria `FROZEN_CRITERIA.md` and ledger `ASSUMPTION_LEDGER.md` were committed alone first (e9816b47d2).
Script `f2_outer_lensing.py` (solver `f2_aqual.py`) passes 9/9 checks and exits 0 in 224 s. It runs on one thread with
a peak RSS of 0.84 GB. `--mutate` multiplies the B21 data by 1.10. K0 then fails and the run exits 1
(`*_MUTATE.*`).

- **K0, cross-check.** My own re-implementation of CFG804 with CFG902's convention reproduces the record exactly:
  χ²_B 163.13 / 155.33; Δχ²(D_der − B) +100.10 / +123.12 all radii; primary +0.84 / −0.27.
- **Model T (the screened covariant theory).**
  - Field equation: AQUAL with μ = x/(1+x), solved by my own axisymmetric solver for a point mass in a uniform
    external field. Lensing uses the orientation-averaged M_eff(<r).
  - Solver checks: the isolated limit agrees to 1e-4 and the far field to 4e-4. K2: against the record's independent
    E2 solver it agrees to 3.4e-4.
  - Baryons per lens: M★ (record lens catalogue, LePhare + 0.15), cold gas (B21 relation), and hot CGM at 0.5 M★
    inside 100 kpc (from CFG580's emissivities and the recorded eRASS:4 L_X; bracket 0–1).
  - Background: native h 0.679 and Ω_m 0.3085.
  - No dust term: the theory predicts no galaxy-bound dust profile.
- **Track A** uses B21 Fig. 3 with the released covariance. **Track B** uses the record's per-lens re-measurement with
  a 50-patch jackknife and nested isolation samples: S10 (181,477), S20, S30, and S_strict (40,576).

## Track A ladder (canonical; alt in the .out). A = data / model; O1 = 0.4–1.1 Mpc, O2 = 1.1–2.6 Mpc

| step | χ²_all | Δχ² vs B | A_in | A_O1 | A_O2 |
|---|---|---|---|---|---|
| L0 record D_der | 263.2 | +100.1 | 0.89 ± 0.03 | 1.23 ± 0.05 | 2.45 ± 0.17 |
| L1 no catchment edge (= B, masses profiled) | 163.1 | 0 | 0.93 | 1.29 ± 0.05 | 0.96 ± 0.07 |
| L2 native h, Ω_m | 162.3 | 0 | 0.94 | 1.30 | 0.97 |
| L3 inventory M★ + cold gas, no profiling | 256.1 | +93.8 | 1.23 | 1.65 | 1.23 |
| L4 + hot CGM 0.5 M★ | 160.7 | −1.6 | 1.13 ± 0.04 | 1.39 ± 0.06 | 1.04 ± 0.07 |
| L5 + EFE, primary y_e (= T_central) | 428.0 | +265.6 | 1.14 | 2.01 ± 0.09 | 4.45 ± 0.31 |

One at a time from T_central (Δχ²):

| change | Δχ² |
|---|---|
| y_e = 0 | −1.6 |
| y_e maxclu | +637.6 |
| f_hot 0 | +419 |
| f_hot 1 | +165 |
| f_cold −0.2 dex | +286 |
| f_cold +0.2 dex | +239 |
| M★ −0.2 dex (E1) | +386 |
| M★ +0.2 dex | +172 |
| h 0.672 | +260 |
| h 0.686 | +271 |
| Σ_crit −3 % | +251 |
| Σ_crit +3 % | +281 |

The most generous envelope (y_e = 0, f_hot 1, M★ and cold gas +0.2 dex) gives Δχ² −19.9, with A_O1 1.06 ± 0.04 and
A_O2 0.79 ± 0.06. It overshoots inside (A_in 0.86).

## Track B isolation test (canonical, T_central with y_e = 0 / primary)

| sample | A_O1 (y_e = 0) | A_O2 (y_e = 0) | A_O1 (primary) | A_O2 (primary) |
|---|---|---|---|---|
| S10 | 1.59 ± 0.07 | 1.40 ± 0.08 | 2.38 ± 0.11 | 5.44 ± 0.33 |
| S30 | 1.46 ± 0.12 | 0.64 ± 0.15 | 2.21 ± 0.19 | 2.56 ± 0.59 |
| S_strict (frozen) | 1.31 ± 0.14 | 0.06 ± 0.16 | 1.95 ± 0.23 | 0.57 ± 0.62 |
| S_x300 (post hoc) | 0.82 ± 0.16 | −0.74 ± 0.23 | 1.25 ± 0.25 | −2.4 ± 0.8 |

The record's re-measurement runs 1.15× B21 (K4b). The frozen verdict uses S_strict. It is REAL FAILURE through
"over" in O2 at y_e = 0, and through "short" in O1 at the primary and maxclu fields.

## Audit of the two-halo terms

- **CFG502:** ΛCDM halo model. Excluded.
- **CFG805:** T1x P_grav with a free bias per bin, which is 4 knobs. Excluded.
- **CFG903:** catalogue neighbours with catchment-supplied cold energy (census f_ret, which is untraceable; CFG886).
  This is not the covariant theory's neighbour term. Used as an upper-bound proxy on top of T_central, it still gives
  A_O2 2.51 ± 0.18 (post hoc (c)).

## What this does not show

- It does not compute the theory's own nonlinear neighbour or hole term (an AQUAL many-body problem). That is what a
  verdict beyond 1 Mpc would need.
- The external field is bracketed with SPARC-local environments (Chae+21), not measured for the KiDS lenses.
- The hot-CGM fraction comes from one quiescent eROSITA stack, as recorded, and was not verified from the paper.
- B21's isolated sample (259k) is not public; Track B uses the record's 181k reconstruction.
- No boost correction is applied (none is released).

## Next step

A spectroscopically isolated lens sample large enough for 1–3 Mpc lensing (GAMA-like, with spec-z host vetoes).
Alternatively, the theory's own neighbour and hole term from a native AQUAL N-body stack. Either would make the outer
range decidable.
