# EUC18 (MASK-APERTURE STELLAR MASS, SECOND RE-READ: THE POPULATION GATE): FROZEN CRITERIA

Committed alone, before the EUC18 driver exists and before any EUC18 number. 2026-11-14.

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. Not "theory
closed". A re-read: it adopts nothing, edits no ledger or scorecard, and no outcome is a pass of the lensing gate.

## 0. What this lane is

EUC17 (`closure_2026_11_13/EUC17_mask_aperture_mass_reread`) showed that the ECLIPSE catalogue's stellar mass is
the mass of the Sérsic model inside the modelling circle, while EUC1 and its children take it as the total of an
infinite body, and re-read three rows (EUC1, EUC4, EUC1-F). This lane re-reads the row those three do not cover:
**EUC13**, the population source gate, which grades the main sample P (3,192 lenses) with source redshifts drawn
from three source populations. It carries the two words that stand on P with realistic source redshifts.

The owner's go (2026-11-14) was to re-read the remaining Euclid lens lanes **with the mask table already fetched**.
No new download is made. Lanes whose lenses the table does not cover are listed in §7 and not graded.

## 1. Method (frozen)

EUC13's committed code is run **unmodified**. A driver wraps EUC1's loader, which EUC13 and every sibling lane use
to read the catalogue, so that each lens's catalogued log mass becomes

    lm_corr = lm − log₁₀ f,     f = M2D_frac(mask_radius, eclipse_effective_radius, eclipse_sersic_index)

exactly EUC17's primary share, from EUC17's committed mask table (`euc17_masks.csv`). The mass errors are left as
catalogued. Every file the source script writes into its own folder is redirected into this lane's folder; the
source folders must be untouched after every run. Data: EUC13's own inputs (same files, same hashes), nothing new.

Every lens of P has a mask record (EUC17), so no lens is dropped and no lens is mixed.

## 2. Rows, words and labels

EUC13's frozen rules, unchanged (its criteria §4), per footing, over its surviving members (M1 AGEL DR2, M2 DESI
Strong Lens Foundry IV, M3 the forward model as an envelope over its surviving settings):

| Row | Statistic | Words | Committed |
|---|---|---|---|
| **Q1** EUC13-P gate | b_med on P, 95 % interval per member | POPULATION GATE HOLDS (every upper bound ≤ 0.15) / POPULATION GATE FAILS (every lower bound ≥ 0.25) / NO VERDICT | NO VERDICT / NO VERDICT |
| **Q2** f₂₅ statistic | fraction of P with b > 0.25, per member | CEILING BROKEN (every lower bound ≥ 0.25) / CEILING HOLDS (every upper bound ≤ 0.10) / NO VERDICT | CEILING BROKEN / CEILING BROKEN |

The words are read from the gate block the source code prints. The source code's own summary line will read NOT
EVALUABLE under the correction, because two of its checks assert uncorrected reference numbers (§4, H2); that line
is not this lane's word.

**Labels, per row and footing:** the word under the corrected mass; UNCHANGED or CHANGED against the committed word;
FRAGILE if bracket F1a or F1b gives a different word, otherwise ROBUST.

**Meaning.** A population gate grades modelled or borrowed source populations, not measured sources; it is weaker
evidence than EUC1-F (EUC13 says so itself). CHANGED toward the law is a hit awaiting a blind re-grade, never a
pass. UNCHANGED means the word survives the correction.

Reported, no word: each member's b_med, f₂₅ and median source redshift; the θ_E-class readings the code prints
against EUC5's sealed bands.

## 3. Brackets (frozen)

**F1a** f with R_e × 0.80; **F1b** f with R_e × 1.25. EUC17 found that these two bound its other brackets (n = 4,
mask-centre offset) on all three of its rows; each EUC13 run takes about eight minutes, so only the two bounding
brackets are run. Bracket F5 (n > 9.5 dropped) is not run: it would change P itself.

## 4. Checks (frozen; a failure of H0–H3 makes Q1 and Q2 NOT EVALUABLE)

- **H0 harness.** With f = 1 the driver reproduces EUC13's committed `euc13_results.json` and `euc13_per_lens.csv`
  byte for byte, and `euc13.out` on every line that carries no elapsed time.
- **H1 source folders untouched.** After every run `git status` shows no change in the folders of EUC13, EUC1 and
  EUC10.
- **H2 the right checks fail.** Under the correction, of EUC13's own checks exactly KA2 and KA3 (M1 and M2) fail:
  they assert EUC1's and EUC10's uncorrected numbers. KA1, KA4, KA5 and KA6 must pass. The M3 settings that survive
  EUC13's validation must be the committed ones (the validation lenses have no stellar masses).
- **H3 shift arrives.** The source-free b_med on P that KA2 prints under the correction equals EUC17's corrected
  value (−0.104 canonical, −0.130 alt) to 0.001.
- **Twin** (mode `invert`, lm + log₁₀ f, separate outputs): every member's b_med must rise on both footings against
  the committed values; the driver exits 1.

## 5. One reading with its own non-voiding check (no word)

**W share.** For EUC8's class W (grades A and B, θ_E ≥ 1.7″, 316 lenses, all with a mask), source at infinity, law
S, stars at the catalogued Salpeter mass: the share of the lensing lower bound that law and stars do not supply,
`s = max(0, 1 − M_2D,law(<R_E) / M_min)`, and the excess mass `max(0, M_min − M_2D,law)`; medians with 16–84 %
ranges, before and after the correction, both footings. It says how much of the wide lenses' mass is still missing,
which is the input the gas lanes (ESZ1, EXR1, EXR2) were built on.

**KW (non-voiding).** With f = 1 the medians reproduce EUC8's committed far-case values for W (share 0.451 /
0.421; excess 3.17e11 / 2.91e11 M☉) to 1 %. If KW fails the reading is not reported; Q1 and Q2 are unaffected.

## 6. Seen before freezing (disclosed)

All of EUC17's numbers, including its conditional reading on P with sources at z_s ≈ 2 (alt f₂₅ 0.435 → 0.272
[0.257, 0.287]). EUC13's committed output in full (members' b_med +0.20 to +0.30, f₂₅ 0.43 to 0.58, M3 envelope
f₂₅ lower bounds 0.437 / 0.408). EUC8's committed class tables. No EUC13 number under the correction exists.
Hand estimate, not verified: Q1 stays NO VERDICT on both footings; for Q2 the members fall to about 0.28–0.40 and
the lowest lower bound lands near the 0.25 line, so Q2 could read either CEILING BROKEN or NO VERDICT.

## 7. Not graded here (open), and why

- **Mask table does not cover the sample** (grade-B lenses below 1.7″ were not fetched): EUC8 Part B (its dispersion
  sample), EUC5 / EUC5R on sample S, EUC6, LNJ1, EUC4's secondary and complement bins, the non-W classes of EUC8
  Part A. Fetching the remaining grade-B masks (about 2,860 lenses, about 0.4 MB) needs the owner's go.
- **Words set by an instrument gate the correction cannot change:** EUC5 and EUC5R (NOT EVALUABLE on their
  dispersion-fit recovery gate).
- **Heavy or dependent:** ESZ1 (map stacks), EXR1 / EXR2 (depend on ESZ1). §5's reading gives the change in their
  input.
- **Blind twins of rows already re-read:** EUC4R (EUC17's R2), EUC13R (this lane's rows; its own code does not use
  EUC1's loader).
- **Not examined:** EUC7 (its word is on SLACS lenses), EUC12.

## 8. Not claimed

No measurement of a₀ or κ. No statement about which source population is right. No pass of the lensing gate under
any outcome. The premise (the catalogue mass is the in-mask mass) rests on the paper's text and on one lens, as in
EUC17.
