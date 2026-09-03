# What the hunt taught — synthesis after 41 items (2026-09-03)

Written before the two background sweeps (items 7–99 and 101–125) return, so that the lesson is on record independently of
what they find. Every claim here points at a committed script in `hunt_2026/` with checks that can fail.

## ⚠️ CORRECTION, 2026-09-03 (later the same day): SECTION 1 BELOW IS WITHDRAWN

The veins workflow (38 agents, `hunt_2026/h102_*`, `h103_*`, `h123_h125_the_ladder.py`) overturned the sentence this
document called "the whole story of the hunt in one sentence." **Both halves of it fail:**

* **Neither of the two "M/L-free" rungs was M/L-free.** The deep-tail rung carries d log a₀/d log Υ = −0.647 and the
  KiDS dwarf lens stack −1.046 (deep-MOND lensing a₀ is degenerate with the assumed baryonic mass at exponent 1, not 2).
* **Their 0.08 dex agreement was an artefact of an estimator bias.** Item 25 fixes the RAR slope at 1/2 and reads
  a₀ = ⟨g_obs²/g_bar⟩, but g_bar < 1e-11 is not deep enough for the exact deep-MOND limit: ν(y)y = √y(1 + √y/2 + …) and
  ⟨√y⟩ = 0.231 there, so the estimator returns a₀ high by 2log₁₀(1+⟨√y⟩/2) = **+0.095 dex** analytically. Synthetic curves
  built to obey the kernel *exactly* at 9.36e-11 are read back as 1.174e-10 by that estimator and as 9.360e-11 by the
  full-kernel one. **Item 25's headline "a₀ = 1.14e-10, the alt footing to 0.004 dex" is WITHDRAWN; corrected, it is
  9.04e-11 — the canonical footing to 0.015 dex.** Items 64, 70, 76 and 100 all inherit the shift; κ = 0.512 ± 0.076
  becomes **0.482 ± 0.081**, so 1/(2π) is excluded at **4.0σ, not 4.6σ**.

**And the diagnosis in section 1 is itself wrong.** Item 103 decomposed the error budget analytically and by Monte Carlo:
the stellar M/L is *not* the sole blocker. **Distance leads the random budget** (38% of the variance once Υ is cut), and
removing Υ takes the total from 0.073 to 0.074 dex — it buys almost nothing, because the distance term grows as the
sample shrinks. **The floor with Υ removed is 10.5%, not 3%**, set by the distance scale; 3% in a₀ would need the distance
ladder to 1.3%, which nobody has. Worse, removing Υ *trades one calibration for a worse one*: on the same points
d log a₀/d log Υ = −0.15 but **d log a₀/d log M_gas = −1.11**, because gas then supplies 85% of g_bar.

**What replaces the section-1 story:** the ladder's organiser is no longer the mass-to-light ratio. It is the **velocity
measurement**. Resolved rotation curves sit **+0.24 dex above unresolved HI line widths**, the direction and size of an
independently measured width-selection bias (+0.25 dex per dex of baryonic mass across three decades, item 124), which
also accounts for the almost-dark "deficit" of item 31. And **M/L-freedom and dynamic range are in direct conflict**:
dropping the stellar mass forces gas-rich selection, which forces low mass, which forces the same acceleration — the
load-bearing rungs span **1.1 decades of mass, not the nine the item promised**, and every one is a gas-rich dwarf.

Section 1 is left below unedited as the record of what was believed, and is superseded by this block.

---

## 1. ~~The finding that reorganised everything: the blocker is Υ, not a₀ and not the data~~ (WITHDRAWN, see above)

Nine separate items converged on the same wall. The stellar mass-to-light ratio caps the precision of κ (item 64, 15% not 3%);
it explains the dwarf-versus-L\* lensing split, the red-versus-blue split and the lensing Tully-Fisher intercept (items 2, 65, 66),
each of which is a 0.15–0.25 dex statement about Υ dressed as a 0.3–0.5 dex statement about a₀; it caps the formation-epoch null
(item 89, which can only see the ΛCDM-predicted trend at 1.7σ); and it is what keeps the a₀ ladder from closing (item 100: a
0.16 dex intrinsic spread, organised entirely by Υ). **The two rungs that do not use Υ at all — the gas-dominated deep tail and
the KiDS dwarf lens stack — agree to 0.08 dex.** That is the whole story of the hunt in one sentence.

## 2. The structural pattern: the framework turns fitted parameters into predicted ones

This, and not any single number, is what the framework does that its rivals do not. With a₀ fixed by Planck's ρ_Λ:

| normally fitted | here predicted | result |
|---|---|---|
| the stellar M/L at 3.6 μm | from Λ, via the deep tail | 0.504 (alt) / 0.656 (canonical) vs SPS 0.5 ± 0.1 — item 76 |
| the halo surface-density constant ρ₀r₀ | = a₀/(2πG), the phantom's own | 177 vs 107–129 M☉/pc², within 0.14 dex — item 5 |
| the angular-momentum slope | = size-mass slope + ¼, from the BTFR alone | 0.569 ± 0.024 vs measured 0.582 ± 0.023 — item 26 |
| the inner rotation-curve diversity | from the baryonic profile, no halo freedom | r = 0.79 across the full observed range — item 23 |
| the local slope of every rotation curve | from g_bar and the kernel's local slope | r = 0.62, regression 0.84 vs 1.0 — item 22 |
| the dark-energy equation of state | from a₀(z), since a₀² ∝ ρ_DE | w₀ = −1.17 ± 0.10 from rotation curves — item 79 |
| the cosmological constant | = 32πa₀²/c⁴ | within ×1.5 of Planck — item 70 |

A theory with one fitted constant that converts seven other free parameters into predictions is doing something. Whether the
constant is *right* is what December and z ≈ 2.5 decide.

## 3. What is new this session, as method

**The closed-form inversion.** Where a survey tabulates a dark-matter fraction inside a radius, g_bar = (1−f_DM)g_obs and the
Route A kernel inverts exactly:

    a₀ = (1 − f_DM) · g_obs / [ln(1/f_DM)]²

No mass model, no geometry factor, no gas scaling relation — every input measured. Applied to RC100 it gives the sharpest
existing-data constraint the programme has: d log a₀/dz = −0.112 ± 0.063, **disfavouring the ΛCDM-native emergent rise at 3.9σ**,
with the caveat that it restates those galaxies' own falling dark-matter fractions (item 16).

**The proof that a pair-versus-sum difference cannot be faked.** Two NFW halos give *exactly* the sum of their parts, because
Newtonian gravity is linear — verified numerically, not argued (item 71b). So any measured departure from additivity is a
signature of nonlinear gravity. The effect is unfortunately only 0–2% in the observable.

**A bound on every completion.** The lensing boost does not end anywhere inside the KiDS reach: endings are excluded at 3σ below
1.67–3.44 Mpc across four mass bins, which is roughly ten times tighter than the same data without the mass split (item 72).

## 4. Nothing outside galaxies survived

Every extra-galactic test either failed, was underpowered by orders of magnitude, or was non-diagnostic: the Local Group timing
(over-predicts 2×), escape velocity (inherits the Milky Way normalisation liability), the saddle-point deficit (washes out in the
observable), merger speeds (non-diagnostic), cluster gravitational redshift (needs a real gas profile), the LMC dwarf pattern
(×100 underpowered), wide binaries versus radius (6% lever against a 2% floor). **Every keeper is galactic and rests on the
acceleration relation.**

## 5. Two liabilities the hunt added to the ledger

* **Local Group dwarfs** need Υ_V ≈ 20 to centre the external-field prediction; +0.36 dex overall, Milky Way (+0.64) far worse
  than M31 (+0.29). This reproduces the known Angus-2008 tension rather than discovering it, but it is now ours (item 8).
* **The cluster residual evolves.** η at fixed mass rises +0.187 ± 0.013 dex per unit z in eRASS1, where constant a₀ requires
  zero and even the ΛCDM-native scale predicts +0.13. Selection and a ΛCDM-calibrated mass proxy plausibly produce all of it;
  it needs a controlled sample. It points the same way as the MUSE apparent rise (item 68).

## 6. The methodological lesson, which is the most transferable thing here

**Ten of my own errors were caught by the rules, not by inspection.** A covariance reshaped in the wrong index order (caught by
positive-definiteness, not by the diagonal, which passed). A total mass used where an enclosed mass belongs — twice, in two
different items. A spherical formula for a disc — twice. An aperture centred on a saddle, making a ratio meaningless. An angular
scale off by 17×. A naive 3/4 exponent that assumed fixed surface density the data reject. A trivial 1/3 that was geometry, not
physics. Each was found because the script had to carry a mutation control, both footings, and the alternative computed beside
the framework — and because a claimed *win* was verified as hard as a claimed *kill*.

Two of those errors would have produced headline claims: a "67% pair-midpoint deficit" and a "KiDS excludes a dark halo at
Δχ² = +4091". Both are retracted in the same files that made them.

## 7. Is there a second Kepler-grade result?

**No. The hunt did not find one, and the answer is now settled rather than pending.** Item 125 rebuilt the ladder from
seven M/L-free rungs and found that the criterion **cannot even be evaluated**: the median quoted error is 0.13 dex against
the 0.05 dex agreement the item asked for, so identical central values could not have demonstrated it. The rungs are in
mild tension anyway (χ² = 16.6/6, p = 0.011), and the three SPARC rungs that *do* agree to 0.016 dex are three estimators
on one sample sharing one distance scale, one inclination convention and one hydrogen calibration — that is one rung, not
three. A 3σ decision between the footings needs the distance scale to 1.4%, the HI mass scale to 3%, and about 518
gas-dominated resolved discs against SPARC's 23. The first two are not sample-size problems.

The earlier reading of this section is left below for the record: What it has found is a candidate and the exact
conditions for it. Item 125: rebuild the a₀ ladder from rungs that use no stellar mass-to-light ratio — the gas-dominated deep
tail, the dwarf lens stack, hydrogen-only systems, the closed-form high-redshift inversion. **If a₀ measured that way across nine
decades of mass agrees to better than 0.05 dex, that is one acceleration scale measured five independent ways with no free
parameter anywhere in the chain, and it is Kepler-shaped.** The data are on disk. That calculation is running now.

The first law remains what it was: a₀ = ½c√(Gρ_Λ), with κ fitted, tested in December by Gaia DR4 and at z ≈ 2.5 by a measurement
nobody has made.
