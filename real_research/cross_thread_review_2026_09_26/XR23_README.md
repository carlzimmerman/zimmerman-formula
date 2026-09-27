# XR23 — how fast do the first massive halos form in the chain, and does it move the JWST ceiling?

The question: in the derivation chain's current model, how fast do the first massive halos form? Does that raise or lower
the ceiling that JWST's earliest massive galaxies press against? The coordinator added a second question: what is the
chain's own collapse threshold at z = 0–1, where FP13's band-pass sets its length, and does it land in FP13's window for
δ_c (1.3–2.6)?

The model is read, not re-derived:
- **Gravity.** FP7's AQUAL-type root with FP13's separator H_S (27faacc84).
  - The MOND sector reads the band-passed field.
  - The band-pass length L(z) is where the actual matter field's Gaussian-smoothed rms reaches δ_c.
  - The yield floor y_th is the web's band-passed rms field. It is on while the leaf decelerates (z > 0.635).
- **The static law.** FP6's `phantom()` with FP9's yield hook (band-pass, yield, output filter). Here it acts on the
  peculiar field of a spherical perturbation.
- **The dark mass.** FL1/FK1's cold coherent field. FP10: "the MOND kernel reads the baryons only; Psi feels Newtonian
  gravity". The kick acts after collapse and is not modelled.

Two readings are scored and never pooled:
- **T**, the linear yardstick's convention (FP6/FP9/FP13 growth). The kernel reads the total matter and the phantom acts
  on all matter. This is the maximal-MOND bracket.
- **B**, the action's content. The kernel reads the baryons, the phantom acts on baryons only, and the dark field falls
  under Newtonian gravity.

Scripts (each writes its own `.out`, `_MUTATE.out`, `_results[_MUTATE].json`; run from the repository root):
- `XR23_common.py`: the machinery.
  - FP13 is exec'd read-only up to its K banner.
  - The Gaussian-smoothed uniform ball is in closed form.
  - Single-shell and Lagrangian multi-shell collapse.
- `XR23_collapse_threshold.py` (XR23a): the chain's threshold δ_c,eff(M, z) at z = 6–20 and z = 0–1. Main rc = 0,
  12/15 checks (the three failures are reported hypotheses); MUTATE rc = 1; 965 s.
- `XR23_mass_function_ceiling.py` (XR23b): reads XR23a's JSON. It computes the linear power, the halo mass function, and
  Boylan-Kolchin's baryon ceiling against Labbé et al. (published and spectroscopically revised) and JADES-GS-z14-0.
  Main rc = 0, 11/12 checks (the one failure is a reported hypothesis); MUTATE rc = 1; 6 s.

Nothing outside this folder was edited. κ = ½ stays fitted (Z = κ = 5.7888). No new constant was added. Not "closed".

## The answer

**The chain inherits ΛCDM's ceiling.** At the halo masses the JWST candidates need, it neither eases nor worsens the
early-galaxy tension.
- **The linear power at z ≥ 6 is ΛCDM's exactly.** FP13's own growth code, run to z = 6–20, differs from ΛCDM's by 0.0
  on every k, in both modes and both footings. While the leaf decelerates, the yield sits at the web's band-passed rms,
  above every linear mode.
- **The MOND sector is exactly off at high z.** The band-pass closes (L = ξ, χ = 0) wherever the state's smallest-scale
  variance can no longer reach δ_c:
  - z ≥ 13.6 on the textbook spectrum (V1);
  - z ≥ 17.4 on the spectrum the chain carries (V0; see "Flagged" below);
  - z ≥ 10.1 / 10.8 once the dark field's own wave cut-off is included (m = 1.9 / 5.2 × 10⁻¹⁹ eV).
- **Below that, L(z) is small.** L(z = 6) = 11.0 kpc (V1) or 17.5 kpc (V0); L(z = 10) = 1.2 / 2.7 kpc. The phantom only
  acts in the last stretch of infall of halos whose virial radius is below ~2L.
- **Reading T (the maximal bracket).** The threshold moves by ≤ 0.57% at M ≥ 10¹¹ M☉ and ≤ 4.2% at 10¹⁰ M☉ (z = 6–14).
  - That raises the abundance of small halos at z = 7: ×1.19 (V0) / ×1.30 (V1) at 10⁹ M☉, ×1.21 (V0) / ×1.05 (V1) at
    10¹⁰ M☉.
  - At M ≥ 10¹¹ M☉ the abundance stays within 2%.
- **Reading B (the action's content).** The dark halo collapses on ΛCDM's schedule to 1.6 × 10⁻⁵. The baryons it holds
  are f_b M to 0.4%.
- **The knob-free test.** The efficiency ε that each data point requires, under ε f_b ρ_h(> M*/(ε f_b)), changes by ≤ 0.08%
  (T) and ≤ 0.01% (B) from ΛCDM's. The sharp-edged top hat, the most MOND the band-pass allows, moves it by ≤ 13%.
- **Where ΛCDM is pressed, so is the chain.** The published Labbé et al. 7 < z < 8.5 bin needs ε = 1.27 (Salpeter
  masses, z = 7.5), and so does the chain.

**The coordinator's question: no single δ_c comes out of the chain.**
- In reading T, the chain's own threshold at the band-pass mass M_L(z) runs from 0.98–1.02 (z = 0) to 1.50–1.52 (z = 1),
  over both spectra and both footings.
  - At fixed z it spreads by up to 1.58 over M = 10¹¹–10¹⁵ M☉ (from 0.08 to 1.63 at z = 0).
  - It is below FP13's window at z = 0–0.25 and inside it at z = 0.5–1.
  - So a threshold that varies this strongly with mass and redshift does not fix δ_c.
- In reading B the dark halos collapse at GR's threshold: 1.633–1.685, within 2.6% of ΛCDM's 1.676–1.685. The baryons'
  MOND infall lowers it slightly at z = 0.
  - That lies inside the window, but it is GR's number.
  - FP13 applies s to the smoothed rms of the nonlinear field, not to a linearly extrapolated contrast. So even here the
    identification s = δ_c stays a postulate.

## The high-z collapse threshold (XR23a, section C)

Reading T, multi-shell, canonical footing. δ_c,eff = δ_c^ΛCDM(z) × A_chain/A_ΛCDM, where A is the growing-mode amplitude
that forms the R_L shell (half its maximum radius) at z. ΛCDM's own δ_c(z) is 1.6876 / 1.6878 / 1.6884 / 1.6893 at
z = 6 / 7 / 10 / 14 (radiation raises it 0.07–0.25% above the EdS 1.68647).

| M [M☉] | V0 z = 6 | V0 z = 7 | V0 z = 10 | V0 z = 14 | V1 z = 6 | V1 z = 7 | V1 z = 10 | V1 z = 14 |
|---|---|---|---|---|---|---|---|---|
| 10⁸ | 1.622 | 1.582 | 1.601 | 1.685 | 1.561 | 1.548 | 1.672 | 1.689 |
| 10⁹ | 1.569 | 1.578 | 1.672 | 1.690 | 1.576 | 1.630 | 1.688 | 1.689 |
| 10¹⁰ | 1.621 | 1.657 | 1.688 | 1.689 | 1.660 | 1.681 | 1.689 | 1.689 |
| 10¹¹ | 1.679 | 1.686 | 1.689 | 1.689 | 1.686 | 1.688 | 1.689 | 1.689 |
| ≥ 10¹² | 1.688 | 1.688 | 1.688 | 1.689 | 1.688 | 1.688 | 1.688 | 1.689 |

- **The alt footing** is lower by ≤ 0.006 everywhere.
- **Reading B:** 1.00000 ± 0.00002 of ΛCDM's at every cell.
- **Single-shell brackets (V1, canonical):**
  - The sharp-edged top hat gives A_chain/A_ΛCDM = 0.90 / 0.92 / 0.97 at 10¹⁰ M☉ (z = 6 / 7 / 10) and 0.95 / 0.96 / 0.99
    at 10¹¹ M☉.
  - The compact profile (FP6 `phantom()`'s own geometry) stays within 2% at M ≥ 10¹⁰ M☉.
  - At z = 14 both are exactly 1: V1 is closed.

## The coordinator's question: the threshold at z = 0–1 (XR23a, section D)

Reading T, multi-shell, V0 canonical (V1 agrees within 0.03). M_L(z) = (2π)^{3/2} ρ̄_m L_com³ is FP13's band-pass mass.
ΛCDM's threshold is 1.676 at z = 0, rising to 1.685 at z = 1.

| z | 10¹¹ | 10¹² | 10¹³ | 10¹⁴ | 10¹⁵ | at M_L(z): M_L | can / alt |
|---|---|---|---|---|---|---|---|
| 0 | 0.078 | 0.460 | 0.938 | 1.398 | 1.633 | 1.5 × 10¹³ | 1.017 / 0.975 |
| 0.25 | 0.632 | 0.960 | 1.220 | 1.530 | 1.663 | 8.5 × 10¹² | 1.202 / 1.176 |
| 0.5 | 1.288 | 1.304 | 1.402 | 1.607 | 1.677 | 4.9 × 10¹² | 1.372 / 1.354 |
| 0.75 | 1.518 | 1.453 | 1.502 | 1.647 | 1.683 | 2.9 × 10¹² | 1.475 / 1.465 |
| 1 | 1.575 | 1.508 | 1.563 | 1.667 | 1.685 | 1.7 × 10¹² | 1.521 / 1.514 |

- **Inside 1.3–2.6:** 12 of 20 cells at M_L (z ≥ 0.5 only).
- **Spread with redshift at M_L:** 0.54.
- **Spread with mass at fixed z:** up to 1.58.
- **Footing dependence:** ≤ 0.042 at M_L (alt is lower); ≤ 0.06 anywhere in the table (10¹², z = 0: 0.460 against
  0.404).
- **Smaller masses at z ≤ 0.25:** 10⁸–10¹⁰ M☉ fall below the amplitude grid at z = 0 (δ_c,eff < ~0.03); at z = 0.25 they
  read 0.03 / 0.15 / 0.35.
- **Why.** With the yield off (z < 0.635) and L ~ 1–3 Mpc, the band-passed peculiar field of every sub-L perturbation is
  deep-MOND (y ~ 10⁻³). Collapse is sped up by an amount that depends on M and z.
- **Reading B** (dark halos, 10⁹–10¹⁴ M☉, V0 canonical): 1.635–1.674 at z = 0, 1.670–1.680 at z = 0.25, and 1.682–1.685
  at z = 0.5–1. Over both spectra and footings the lowest is 1.633.
- **Consequence for FP13.** In reading T the chain's own z < 0.6 collapse is far faster than ΛCDM's. So FP13's reading of
  the state through ΛCDM halofit is not self-consistent in T. In B the dark field collapses as in GR, and the halofit
  reading stands closer to consistency.

## The halo mass function (XR23b, section H)

Sheth–Tormen (A, a, p = 0.3222, 0.707, 0.3) on σ(M, z) from a real-space top-hat filter in Lagrangian radius. The barrier
is B(M, z) = δ_c^ΛCDM(z) × A_chain/A_ΛCDM (XR23a), and the Jacobian carries the barrier's own mass slope. The linear
spectrum is textbook EH98 at σ₈ = 0.811. The table gives dn/dlnM as a ratio, chain/ΛCDM.

| z | reading | 10⁸ | 10⁹ | 10¹⁰ | 10¹¹ | 10¹² | 10¹³ |
|---|---|---|---|---|---|---|---|
| 7 | T V0 can | 1.080 | 1.188 | 1.208 | 1.018 | 0.997 | 0.998 |
| 7 | T V1 can | 1.323 | 1.299 | 1.052 | 0.999 | 0.999 | 0.999 |
| 7 | B (V0, V1, both footings) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 10 | T V0 can | 1.399 | 1.139 | 1.007 | 0.998 | 0.999 | 1.000 |
| 10 | T V1 can | 1.077 | 1.008 | 0.999 | 0.999 | 1.000 | 1.000 |
| 10 | B | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 14 | T V0 can | 1.033 | 0.999 | 0.999 | 1.000 | 1.000 | 1.000 |
| 14 | T V1 can | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 14 | B | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

- **Alt footing:** within 0.03 of canonical everywhere.
- **Top-hat bracket (V1):** ×1.33–1.65 at z = 7 and ×1.18–1.84 at z = 10; exactly 1 at z = 14.
- **Excursion-set cross-check:** the first-crossing ratio for the moving barrier (Sheth & Tormen 2002, first order) agrees
  in sign and size.
- **The dark field's wave cut-off** (Hu, Barkana & Gruzinov 2000):
  - half-mode k = 195 / 305 h/Mpc;
  - M_1/2 = 2.3 × 10⁶ / 5.9 × 10⁵ M☉ at m = 1.9 / 5.2 × 10⁻¹⁹ eV.
  - Halos above 10⁹ M☉ lose < 0.1% (Schive et al. 2016; a sharp-k excursion set). It is a mini-halo effect.
  - Its real effect on the chain is indirect: it closes the band-pass by z ≈ 10–11.

## The knob-free ceiling (XR23b, section B)

The ceiling is ρ*(> M*) ≤ ε f_b ρ_h(> M*/(ε f_b)), with f_b = 0.1571. The headline is ε = 1. Each data point's
required ε is reported (ε > 1 means the point sits above the ceiling).

| data cell | ΛCDM ε | chain T | chain B | top-hat bracket |
|---|---|---|---|---|
| Labbé published, 7 < z < 8.5, Salpeter, at z = 7.5 (at 7.0) | 1.275 (0.942) | 1.275 (0.942) | 1.275 | 1.131 |
| Labbé published, 8.5 < z < 10, Salpeter, at z = 9.1 (8.5) | 1.072 (0.771) | 1.073 | 1.072 | 0.971 |
| Labbé published, Chabrier (×0.61), z = 7.5 / 9.1 | 0.778 / 0.654 | same | same | 0.690 / 0.592 |
| Labbé revised, 7 < z < 8.5, Salpeter, z = 7.5 | 0.273 | 0.273 | 0.273 | 0.239 |
| Labbé revised, 8.5 < z < 10, Salpeter, z = 9.1 | 1.072 | 1.073 | 1.072 | 0.971 |
| JADES-GS-z14-0, z = 14.32, log M* = 8.6 (+1σ 9.3) | 0.234 (1.172) | 0.234 | 0.234 | 0.234 |

How the revised sample is built:
- 13050 is CEERS 3210 at z = 5.624, a broad-line AGN (Kocevski et al. 2023).
- 38094 is at z = 6.98, which takes it out of the bin (Wang et al. 2024).
- 14924 moves to z = 8.35 at RUBIES' medium mass (Wang et al. 2024).
- The z ≈ 9 object 35300 (log M* = 10.40, Salpeter) has no spectroscopy, so the 8.5 < z < 10 bin is unchanged.

The ΛCDM numbers were cross-checked in scratch with colossus's planck18 (1.23 / 0.91 / 1.02 / 0.74 against this lane's
1.28 / 0.94 / 1.07 / 0.77; a 4% cosmology offset).

GS-z14-0's abundance is one object in 58 arcmin² at 13.5 < z < 15 (1.05 × 10⁵ Mpc³). The ΛCDM ceiling would put 53
galaxies of its central mass in that volume, and 0.6 at +1σ mass. The alternatives give ε = 0.21 (z = 14.12) and 0.19
(window 13–16).

**What this means.** The chain's MOND is confined by its band-pass to r ≲ 2L, which is ≲ 35 kpc at z = 6 and is exactly
zero above z_close. It cannot speed the collapse of the 10¹¹–10¹² M☉ halos the Labbé candidates need, nor of GS-z14-0's
~2.5 × 10⁹ M☉ halo at z = 14, where V1 is closed. Two things are left:
- **Galaxy-formation physics.** A mass-to-light or IMF correction: Salpeter gives 1.27 and Chabrier 0.78.
- **Data revisions.** The published 7 < z < 8.5 bin needs ε = 1.27. Revised, it needs 0.27.

## Robustness

- **Reading T at M ≥ 10¹¹ M☉:** the shift stays ≤ 1.7% over every case below; at 10¹⁰ M☉ it is ≤ 7%.
  - FP13's threshold window: s = 1.3 and 2.6, on both spectra.
  - The dark field's mass: 1.9 and 5.2 × 10⁻¹⁹ eV, with their cut-off included.
  - Both footings.
- **The largest mover is V6** (s = 1.3 on V0: the longest L). Its abundance is ×1.39 at 10⁹–10¹⁰ M☉ and ×1.10 at 10¹¹ M☉
  at z = 7. By z = 10 it is within 5% at M ≥ 10¹⁰ M☉ (×1.04 at 10¹⁰ M☉).
- **s = 2.6 and the wave cut-off move the chain toward ΛCDM.** They shorten L or close the band-pass sooner.
- **Reading B is ΛCDM's in every case.**
- **The ceiling verdict (B4) holds in every variant.** All variants leave M ≥ 10¹¹ M☉ within 10%.

## Controls and MUTATE

XR23a:
- **K1:** the ΛCDM threshold (MOND off, matter + Λ) equals Kitayama & Suto's (3/20)(12π)^{2/3}[1 + 0.0123 log₁₀ Ω_m(z)] to
  6.8 × 10⁻⁵ at z = 0–20. That includes 1.67595 against 1.67603 at z = 0, and the EdS 1.68647 at high z.
- **K2:** the force law equals FP6's committed `phantom()` with FP9's yield hook to 1.6 × 10⁻⁴ of the field.
- **K3:** the closed-form smoothed ball equals the quadrature of FP6's `shell_frac` to 3 × 10⁻¹⁵.
- **K4:** the multi-shell code's Newtonian limit equals the single-shell top hat.
  - Formation δ: 1.584139 against 1.584122.
  - Collapse δ: 1.687786 against 1.687785.
  - Reading B equals reading T there to 10⁻¹⁴.
- **K5:** FP13's committed state table (L, y_th at z = 0–3) is reproduced to 4 × 10⁻¹⁵.
- **K6:** doubling the shells or halving the step moves the largest high-z shift by 7 × 10⁻⁵, against a shift of
  4 × 10⁻³.
- **K7:** the refined amplitudes equal an independent root-finding at five cells to 8 × 10⁻⁷.
- **MUTATE** (the band-pass removed, L = 10³ Mpc): C0 fails, rc = 1.
  - A_chain/A_ΛCDM falls to 0.003–0.32 for 10¹² M☉ at z = 9–14 and to 0.014 for 10¹¹ M☉ at z = 14.
  - Every other cell falls below the amplitude grid.
  - The band-pass is what keeps the chain ΛCDM-like at high z.

XR23b:
- **K1:** FP13's committed sub-L power boost is reproduced exactly (difference 0.0). At z = 0 it is +0.0016 / +0.048 /
  +0.235 / +1.922 at k = 0.1 / 0.3 / 0.5 / 1 h/Mpc.
- **K2:** Sheth–Tormen and Press–Schechter equal colossus's to ≤ 1.2 × 10⁻³.
- **K3:** see "Flagged" below.
- **K4:** the chain's linear boost at z ≥ 6 is 0.0.
- **K5:** the cumulative tail equals colossus's integrated sheth99: 10^-5.580 against 10^-5.592 at z = 9.1, and 10^-3.284
  against 10^-3.302 at z = 14.3.
- **MUTATE** (XR23a's no-band-pass barrier for reading T, V1 canonical): B4 fails, rc = 1. With the band-pass removed the
  halo abundance is so large that the ε some cells require falls below the solver's 10⁻⁴ floor (printed as inf).

**The pre-declared hypotheses, as they fell** (reported; FP10's convention):
- **H1 held.** The band-pass closes at 13.6 (V1), 17.4 (V0), and 10.1 / 10.8 with the cut-off.
- **H2 failed on its 10¹⁰ limb.** The limb was ≤ 3%; the run gives 4.2%. The 10¹¹ limb held (0.57%).
- **H3 held.**
- **H4 failed.** The top hat moves by 10.7% (limit 8%) and the compact profile by 1.8% (limit 1%).
- **H5 was mixed.** T held (below 1.3 at z = 0, spread 0.54). B failed: the deviation is 2.6%, not ≤ 1%.
- **H6 held.** M ≥ 10¹¹ M☉ stays within 1.7%.
- **H7 held.**
- **H8 held.**
- **H9 failed on the T limb.** At 10¹⁰ M☉, z = 7, V0 gives ×1.22 against a ≤ 10% limit. B held (0.03%).
- **H10 held.** It is B4, load-bearing.
- **H11 held for GS-z14-0.** It held for the revised 7 < z < 8.5 bin. The revised 8.5 < z < 10 bin still needs ε = 1.07
  with Salpeter masses.

## Flagged for other lanes

- **The chain carries a mis-scaled EH98 spectrum.**
  - Where: FP6's `T_EH98`, from L341, is also in FP3/FP7/FP9, the bs_khronon lanes and others.
  - The error: it is called with k in 1/Mpc but evaluates q = k Θ²/(Ω_m h …) and 0.43 k s/h. EH98's eqs. 28/30 need
    q = (k/h) Θ²/Γ_eff and 0.43 k s.
  - The effect: at fixed σ₈ its spectrum is 0.44× CLASS at 0.01 h/Mpc and 1.29 / 1.50 / 1.64× at 1 / 10 / 100 h/Mpc.
    σ(10¹⁰ M☉) is 4.55 against CLASS's 3.91. The textbook form matches CLASS to 6% (K3).
  - What it drives: FP13's state at high z (V0 against V1 above: z_close 17.4 against 13.6), and FP13's A6
    "linear-spectrum systematic". Ratios to ΛCDM on the same spectrum partly cancel it; absolute scales do not.
  - Not re-scored here.
- **XR18's ill-posedness applies to the z = 0–1 numbers.** XR18 found H_S ill-posed as written at z ≤ 0.635. Its N4 also
  says that the varied y-term screens sub-L Newtonian gravity at z > 0.635 by 1/(1 + κ):
  - κ ≈ 2–2.7 in a Gaussian reading of the web;
  - κ ≈ 3 × 10⁻³ in a halo reading.
  - This lane scores H_S's static law as FP13 does, without that term. FP19's repair is pending. If the Gaussian reading
    held for collapsing halos, sub-L collapse at z > 0.635 would be slowed, not sped up.
- **The kick acts after collapse.** FP10's front already reaches 0.5–0.95 r200 at z = 6. It removes dark mass, not baryons,
  so the f_b ceiling on the reservoir at collapse is unchanged. How lighter halos then accrete is not computed here.

## Disclosures

- **Exploratory scratch runs came first** (not committed):
  - single-shell probes;
  - a multi-shell prototype and its time history;
  - the state on the textbook spectrum and with the cut-off;
  - EH98 against CLASS;
  - this lane's Sheth–Tormen against colossus.
- **Three smoke runs of XR23a and two of XR23b** (reduced grids, outputs outside the repository) preceded the final runs.
  They found two inversion bugs: the ln A interpolation (1.3%) and the shift interpolation (1.1%). Both were replaced by
  per-target refinement (K7: 8 × 10⁻⁷). They also found a whole-cell baryon count (fixed) and a NaN table (fixed).
- **Changes made after the smoke runs** (disclosed in both docstrings):
  - The hypothesis checks were made reported, following FP10's convention.
  - C0 (5%, five times the smoke's largest M ≥ 10¹¹ shift) was added as XR23a's MUTATE target in place of C1.
  - XR23b's K5 was replaced by a colossus control. The figure it first used, ~10^-5.2 per Mpc³ attributed to
    Boylan-Kolchin 2023, could not be verified at source.
- **The Labbé et al. catalogue:** the authors' public file of the published revision (9.3 kB,
  github.com/ivolabbe/red-massive-candidates) was downloaded once to the scratch area and read. Its values are transcribed
  into XR23b with the citation.
- **A usage limit** stopped the web checks before JADES-GS-z14-0's ALMA redshift could be confirmed at source. The lane
  uses Carniani et al. 2024's z = 14.32 and its −1σ value 14.12.
- **Scope:**
  - spherical collapse with a conditional-mean profile: no tides, no angular momentum, no particle-mesh run;
  - the separator's state is read through halofit, including at z ≥ 6 and on the cut-off spectra, where it is not
    calibrated;
  - GS-z14-0's survey window (13.5 < z < 15) is a declared choice; 13–16 is reported.

## References used

- Boylan-Kolchin 2023, Nature Astronomy 7, 731 (the ceiling).
- Labbé et al. 2023, Nature 616, 266 (arXiv:2207.12446 v3).
- Kocevski et al. 2023, ApJL 954, L4.
- Wang et al. 2024, ApJL 969, L13 (RUBIES).
- Carniani et al. 2024, Nature 633, 318.
- Sheth & Tormen 1999, 2002.
- Kitayama & Suto 1996.
- Hu, Barkana & Gruzinov 2000.
- Schive et al. 2016.
- Eisenstein & Hu 1998.
- Madau & Dickinson 2014 (the Salpeter-to-Chabrier factor 0.61).
- Gehrels 1986 (the Poisson bound for N = 1).
