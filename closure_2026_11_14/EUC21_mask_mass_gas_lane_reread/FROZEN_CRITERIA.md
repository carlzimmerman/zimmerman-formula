# EUC21 (MASK-APERTURE STELLAR MASS, FOURTH RE-READ: THE GAS LANE ESZ1): FROZEN CRITERIA

Committed alone, 2026-11-14, before any EUC21 script exists and before any EUC21 number. Owner's go of 2026-11-14:
"Yes, re-read ESZ1".

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. Not "theory
closed". A re-read: it adopts nothing, edits no ledger or scorecard, and no outcome is a pass.

## 0. What this lane is

ESZ1 (`closure_2026_11_12/ESZ1_wide_lens_gas_pressure`) asked whether the hot gas that law S would need to supply
Euclid's wide lenses from an extended gas body is there, by stacking the ACT Compton-y map on 237 wide lenses and
comparing with the least pressure each gas family needs. The gas each lens needs is what the lens lacks after the
law and the stars. EUC17 showed the catalogue's stellar mass is the mass inside the modelling circle, and EUC18
and EUC20 found that this lowers the wide lenses' missing mass by about 40 % with the source at infinity. ESZ1's
predictions were built on the uncorrected mass. This lane re-reads ESZ1 on the corrected mass. The measurement (the
stack) does not use the stellar mass; the predictions and the control matching do.

## 1. Method (frozen)

**The correction** is EUC17's primary share, unchanged: `f = M2D_frac(mask_radius, eclipse_effective_radius,
eclipse_sersic_index)`, `lm_corr = lm − log₁₀ f`; masks from EUC17's and EUC19's tables (every lens of sample S has
one). No new download: the maps and catalogues are ESZ1's own, already on disk.

**Route.** ESZ1's committed text is executed under its own path, with EUC1's loader wrapped (as in EUC18) and with
**one exact substitution, which must match exactly once**: the gate that stops the run before the stack when any
instrument check has failed is made to ignore checks K6 and K7. Those two assert EUC4's and EUC8's uncorrected
numbers and must fail under the correction; ESZ1 itself skips them in its mutation runs for the same reason.
Nothing else is changed. Every file the source writes into its own folder is redirected into this lane's folder.

## 2. Rows, words and labels

ESZ1's rules, unchanged (its criteria Parts G and C). Family word: NO POWER if the family's least predicted stack
is below 3 σ of the measurement; EXCLUDED if measured + 2 σ is below it; ALLOWED otherwise.

| Row | Rule | Committed (canonical / alt) |
|---|---|---|
| **Y1** Part G lane word, with its family words (B30, B100: cored gas bodies; G2: r⁻² cusp) | HOT GAS DOES NOT SUPPLY THE WIDE LENSES (all three EXCLUDED) / ONLY A CUSP IS LEFT (B30 and B100 EXCLUDED) / HOT GAS NOT EXCLUDED (B30 or B100 ALLOWED) / NO VERDICT; tag [BRACKET-DEPENDENT] by ESZ1's five brackets | ONLY A CUSP IS LEFT / ONLY A CUSP IS LEFT, no tag |
| **Y2** Part C word: wide lenses against controls matched in redshift and stellar mass | ESZ1's rule; tag if the CIB-deprojected map gives another word | NO EXCESS DETECTED [BRACKET-DEPENDENT: CIB-deprojected map] |

ESZ1's own lane words will read NOT EVALUABLE in the corrected run, because its final gate also counts K6 and K7.
This lane's words are ESZ1's rules applied to the family words (Y1) and to the Part C words before that gate (Y2)
that the corrected run produced. The collector must show that the same rules return the committed words from the
committed family words.

**Labels, per row and footing:** the word under the corrected mass; UNCHANGED or CHANGED; FRAGILE if bracket F1a
(R_e × 0.80 in f) or F1b (R_e × 1.25) gives a different word, otherwise ROBUST.

**Meaning.** EXCLUDED says the gas is not there at hydrostatic pressure. A family that moves from EXCLUDED to
ALLOWED or NO POWER is a row where an extended hot-gas body is no longer ruled out by this map; that is a hit
awaiting a blind re-grade and not a pass, and it says nothing about whether such gas exists. UNCHANGED means the
exclusion survives the correction.

**Reported, no word:** each family's least predicted stack, its distance from the measurement in σ and its factor
f_T; the Salpeter-star and central-source settings; Part D as the code prints it.

## 3. Checks (frozen; a failure of H0–H4 makes Y1 and Y2 NOT EVALUABLE)

- **H0 harness.** With f = 1 and the substitution in place, the run reproduces ESZ1's committed results file and
  per-lens file byte for byte and its log on every line that carries no elapsed time.
- **H1 source folders untouched** in git after every run.
- **H2 the right checks fail.** Under the correction exactly K6 and K7 fail; K1 to K5, K8 and K9 pass.
- **H3 the shift arrives.** For every lens in the corrected run's per-lens file, its log stellar mass minus the
  committed one equals −log₁₀ f to 0.001.
- **H4 the measurement does not move.** The stack of the wide lenses (N, mean, σ) on both maps is the committed one
  to 1e-9 relative.
- **Twin** (mode `invert`, lm + log₁₀ f, separate outputs, driver exits 1): the least predicted stack of B100 rises
  on both footings against the committed value.

## 4. Seen before freezing (disclosed)

ESZ1's committed output in full (measured +3.83 ± 1.47; least predicted stacks 37.2 / 32.4 for B30, 171 / 145 for
B100, 2.03 / 1.86 for G2, in 10⁻⁶ arcmin²). EUC18's and EUC20's numbers, including the wide lenses' excess mass
with the source at infinity (3.17 → 1.98 and 2.91 → 1.75 × 10¹¹ M☉) and the share of wide lenses that need no extra
mass (0.3 % → 8.5 %, 0.9 % → 12 %). No ESZ1 number under the correction exists.
Hand estimate, not verified: the cored families' least predicted stacks fall by roughly half and stay EXCLUDED by
several σ; G2 stays NO POWER; Y1 unchanged. Y2 is not predictable from what is on the page.

## 5. Not graded here

EXR1, EXR1R, EXR2 (the X-ray lanes, both NOT EVALUABLE as frozen for their own design reasons). CJ1's row 39 is not
edited.

## 6. Not claimed

No measurement of a₀ or κ. No statement that hot gas exists or does not exist around these lenses beyond what
ESZ1's own rule says. No pass under any outcome. The premise (catalogue mass = in-mask mass) rests on the paper's
text and on one lens, as in EUC17.
