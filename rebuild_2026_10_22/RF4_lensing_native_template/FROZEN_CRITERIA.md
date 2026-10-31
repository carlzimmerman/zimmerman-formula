# RF4_lensing_native_template: FROZEN CRITERIA (committed alone with the ledger, before any script or any number from this lane)

**Question (THEORY_PROGRESS_SUMMARY_2026-10-31 §4).** What is the lensing and kSZ shortfall of route E when the one-halo profile, the miscentring and the two-halo term are built from data or from the framework, not from an N-body-calibrated halo model?

**Disclosed, already seen.** X53, FC1, KN1 (+434, +366 canonical), TL1 and GH2 (law 66.2, route E 140.6), GH1 (+0.17), SI3 and SC2 (Δ_c tables, clone noise), GH9, GH10, GH11 (A(1.8) 0.24, 0.45, 0.54; the two-halo template's hole dependence, 0.54 to 0.84). So kSZ points and KiDS stacks are not blind. No data-built KiDS template has been made; I do not know its shape or amplitude. I expect the kSZ part to come out UNSEPARABLE again, and I do not know the KiDS answer.

**Standing.** κ = ½ FITTED. Footings graded separately. Cold dark energy is a gravitating field component, never a particle. No Planck parameter, no ΛCDM background, no CFG805 template in any graded line. No downloads. Nothing here says the data favour the framework. Not theory closed.

## Arms (one-halo)
All arms carry the same baryons: stars and cold gas as in X78/GH2, hot gas Zhang's profile cut at k R_vir, and M★ R0 and R2 (SI3's +0.295 on red lenses, gas at catalogue M★).
- **E(k): the summary's route E profile.** GH2's `mass_route_e` unchanged: Σ(σ) smooth core, c_f 4 (EXTERNAL) with its a₀ floor, fair-share cold mass to r_ta with the gas to r_ta. No NFW. k = 1 measured gas, k = 3 the closure case that plays X73's gas to r_ta on this mass scale.
- **N: the working no-floor rule** (OWNER_DECISION_2026-10-31_NO_FLOOR, RG1's table `rg1_rule_table.json`): S_cold = f_c η(M_t) Σ_coll(M_t), no floor, EM1's M200 (background A), truncated at R200. Reported: truncated at r_ta; fair-share mass as in E.
- **Z: the native shape.** ZN1 `zn1_shapes.json`, z = 0.25 tag for KiDS, KN1's frozen rule: M_c(r) = f_c M_t m(r/R_t), interpolated between 10¹², 10¹³, 10¹⁴, clamped outside, EM1's masses. Reported: fair-share mass; the z = 0 tag.
- **Law:** GH2's `mass_law` with the same baryons at each footing's a₀.
N and Z have no footing; they stand against each footing's law. E's floor gives it a footing.

## Miscentring (no simulation)
- ΔΣ_obs = (1 − f) ΔΣ(R) + f ΔΣ_off(R; σ_off), for every arm and the law, as a linear operator on each table's Σ(R).
- **f = 0.28** (GH11's satellite fraction, as the summary orders), band 0.12 to 0.49 from its published errors, f = 0 reported. G3C's own satellite fraction at the lens masses is reported beside it. f = 0.28 comes from a paper's HOD fit and from another sample; ledgered as such.
- **σ_off measured:** √(⟨R²⟩/2) over G3C members in G09 with GKV lg M★ 10.5–11, N_fof ≥ 3, not the iterative centre, R = projected distance to the group's iterative centre, native D_A. The BCG-to-iterative-centre offset is reported.

## Two-halo: built from the sample's own clustering, or UNSEPARABLE
**Template.** Tracers: KiDS-bright, `masked == 0`, 1.24M rows. Pairs: |z_t − z_l| ≤ 0.1, physical R from the lens's native D_A, 0.03–15 Mpc. E(R) = weighted tracer count per area around lenses minus around comparison centres of the same lenses' z and mass: per-lens isolated clones I_c for Δ_c = L − I_c, per-lens plain randoms R for L − R. Lens weight = its total source weight (WW), a clone takes its parent's. E(R < R_x) = 0, with R_x = 150 kpc, removing the lens's own faint satellites. T(R) = mean E inside R minus E(R). Per mass bin, 50-patch jackknife.

**Amplitude.** ΔΣ_2h = a T. For a matter-tracing tracer a = ρ̄_m/(b_t n̄₃), so a is a tracer property and doesn't depend on the lens's bias: one pooled a, not four b's. **a is measured from the shear itself at 3–15 Mpc on S10 L − R,** outside every graded radius, after subtracting each arm's own one-halo there, by inverse-variance fit with jackknife errors. So no matter P(k), no σ₈, no growth factor and no ΛCDM initial condition enters; the growth band the summary allows is not needed and is not used. The far-range shear uses the same point-z rule (Z_B > z_l + 0.2) on a pixelised source map.

**Separability tests, all on S10, frozen:**
- **TS1:** a/σ_a ≥ 3 on arm E(1).
- **TS2:** the four per-bin a's agree with the pooled a, p ≥ 0.01.
- **TS3 (scale-independent bias):** T of the bright half of tracers (split at median magnitude) over T of the faint half, averaged over 0.5–3 Mpc, relative to the same ratio from a at 3–15 Mpc, within 30 % or within 2σ.
- **TS4 (GH11's failure):** R_x 400 kpc in place of 150 kpc moves a T by less than 1σ of the data at every O2 cell, stacked per mass bin.
- **TS5 (nulls):** cross shear at 3–15 Mpc gives |a_×|/σ < 3; tracers with RA shifted by 5° give E(R) with max |z| < 3 at R ≥ 0.3 Mpc against comparison centres.
- **TS6 (sanity):** implied b_t = ρ̄_m/(a n̄₃) in 0.3–4, n̄₃ from the tracers' own z histogram and native volume.
**Any failure: the word is "two-halo UNSEPARABLE"** and the grade uses R ≤ 300 kpc only, with no template. Template lines may then be printed labelled "reported, not graded". Footings can't make it differ except through the law's own a, which is reported: the separability status is read on E(1) at canonical and alt.

**If TS1–TS6 pass,** the same a is applied to all samples. a from S_strict and S_x300's own L − R is reported.

**kSZ two-halo.** GH11's method, lens-neighbour template from DESI DR1 BGS with same-halo holes (|Δv| < 500 km/s) of 0.25, 0.5 and 1 Mpc; b free ≥ 0. **Built only if A(1.8) moves by less than 1σ across the three holes and the fit has b/σ_b ≥ 2 at 1 Mpc.** Otherwise "two-halo UNSEPARABLE" for kSZ and the grade is θ ≤ 3′, no template. Bias on kSZ has no far-range lensing analogue here, so an amplitude is free in any kSZ template line.

## Grades (each per footing)
**G1, TL1's stack, B21's bins, GH2's harness.** k = 1, 1.5, 2, 3, 5. χ² on bins 3–4 (TL1's statistic) and "all", arms and law. With a fixed (no parameter) and with free b ≥ 0 per bin using T in place of CFG805's (the like-for-like comparison with 66.2 and 140.6). Class Δχ²(arm − law) ≥ +9 LAW, ≤ −9 ROUTE E, otherwise NOT DIAGNOSTIC. Crossover k* per arm, if any. B21's stack isn't S10 (F2 K4b, ×1.15); T is S10's, disclosed.

**G2, SI3's Δ_c with enough clones.** S10, S20, S30, S_strict, S_x300, R0 and R2, SI3's frozen estimator, block-diagonal 50-patch jackknife with Hartlap, 59 cells. Per-lens clones, no draw-then-veto: new seed, **8 clones per lens on S10, 4 on S20, 12 on S30, 16 on S_strict and S_x300.** With and without a T. χ², p, Δχ²(arm − law), and SI3's A_in, A_O1, A_O2 data/model. Halves of I_c give catalogue noise.

**G3, GH1's matched hosts.** GH1's stacks (`gh1_esd.npz`), 4 bins, 50–300 kpc, its covariance. G09 clones of the template are not built; GH1's frozen statement that a two-halo term is negligible there is checked: T from G09 spec-z GAMA tracers against uniform box randoms, |Δv| ≤ 2000 km/s, R_x = R200's scale 150 kpc, a measured from GH1's own 1.1–2.5 Mpc cells on the bins pooled. **Negligible if |a T| < 0.5σ of the data in every bin's stacked 50–300 kpc mean.** If not negligible, it enters the fit, and the line is labelled. Grade: χ², A_h = amplitude on the cold halo only (baryons fixed), lg A_h against GH1's +0.17 (not the same operation, disclosed).

**G4, kSZ.** GH10's published DR2 points, its bin, its covariance, GH9's offset. f = 0.28, σ_off measured. A(1) and A(1.8), and A(k*) if G1 gives an arm a k*. Band: f 0.12–0.49, 10 % r uncertainty. A + 2σ < 1 BELOW; A − 2σ > 1 ABOVE; otherwise CONSISTENT, with NOT DETECTED if A/σ < 3.

## Verdict wording
Per footing, per arm, a **shortfall as a band** over: f; R0 or R2; a ± σ_a; T bright or faint; catalogue halves. Reported as:
- **Normalisation:** A_all (data/model, template removed) on the graded range, in G2's S10, S_strict and S_x300 and in G3. NORMALISATION SHORT where A − 2σ > 1, HEAVY where A + 2σ < 1, otherwise OK.
- **Shape:** χ² after fitting that one A, p. SHAPE MISFIT where p < 0.01. A_in, A_O1, A_O2 printed.
- A read that goes from FAIL to OK because an outside input was removed is reported as "not a framework failure", never as "the framework passes".
- **Rule 7 of the summary:** a fail or a win gets the same checks. No third arm, no fitted slope, no re-tuning of a or R_x after seeing a grade. Deviations go in the README as post-result.

## Checks (any failure: no verdict for the part it serves, exit 1)
- **K1:** at k = 1, 3 GH2's E and law with CFG805's T reproduce TL1's/GH2's 437.9, 66.2, 140.6, 757.8 within 0.1, canonical.
- **K2:** SI3's frozen estimator: S10's L and its law table reproduce SI3's raw L amplitudes; the old 4-clone a2 sums read through this path reproduce SI3's R2 Δ_c χ² for S_strict, canonical, within 0.5 on FC1's rule.
- **K3:** clones: lens/I source weight per centre in O2 within 0.10 of 1, per-lens counts exact, cross-shear null and halves p ≥ 0.001 (SI3's K_H3–K_H5).
- **K4:** the far-range pixel estimator against the record path on S10 L − R at 1.1–3 Mpc: pooled ratio within 15 % or 2σ.
- **K5:** miscentring operator: point mass offset by a Gaussian against the closed form, within 1 % at R ≥ 0.1 σ_off; f = 0 is the identity.
- **K6:** GH1's stack and GH2's G09 χ² (17.7, 10.1 at k = 1, bins 3–4) within 0.1. GH10 A(1.8) 0.448 and GH11's 0.54 reproduced within 0.005.
- **K7:** template injection: counts drawn at a known E(R) through the pipeline returns it within 2 %.
- **K8:** grep: no 5.364, no `esd2h` in a graded line, no home path in committed files.
- **MUTATE** (`RF4_MUTATE=1`, separate outputs): sources rotated 45° for far range and tracers shifted 5° and halos × 0.5. It must fail TS1 or TS5, change χ² of E by more than 5, and exit nonzero.

## Compute
One thread, `nice -n 15`, at most two processes. Scratch work in the session scratchpad, not committed. κ = ½ FITTED; c_f EXTERNAL where used; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.
