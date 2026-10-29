# X69_soft_floor_sparc: FROZEN CRITERIA (committed alone, before any script or graded number)

**Source:** the external model's T2 (relayed by the owner, 10-29). The floor softens only in low-acceleration galaxies.
Its own rule of engagement is to run the frozen form once and keep it only if it helps the low-X₀ galaxies without
hurting the rest. The owner said "keep pushing on your own".

**Standing:**
- κ = ½ FITTED. Footings never pooled.
- Route E (X43's machinery). c_f = 4 is EXTERNAL.
- Not "theory closed". Nothing here may say the data favour the framework.

## Hypothesis SF

X43's rule with the floor scaled by a function of the galaxy's own peak baryonic acceleration:

Σ_core = max( Σ_M · F(X₀), η Σ_coll(M200) ),  F(X₀) = 4X₀ / √(1 + 16 X₀²),  X₀ = max_r g_bar(r) / a₀.

- g_bar is SPARC's tabulated baryonic acceleration (gas + disc + 1.4 × bulge), evaluated at Υ = 0.50 so X₀ does not move
  with the fitted Υ. a₀ is the footing's value.
- The form is frozen exactly as the proposal gave it. No other form is run except MUTATE.
- **Scope:** SPARC only. Groups and clusters keep X43's grades unchanged, because X₀ is not defined in their data.
  Leo T and Phoenix are not in SPARC and are out of scope; the README flags this.

## Checks (all must pass, else UNDECIDED, exit 1)

- **K0:** with F ≡ 1, the SPARC rms reproduces X43's committed values on both backgrounds and both footings, to 1e-6.
- **K1:** F(X₀) → 1 as X₀ → ∞, and F(0.08) = 0.305 ± 0.001.

## Statistics

Per footing and background:
- **LOW** = galaxies with X₀ < 0.32 (the proposal's own threshold); **REST** = all others.
- Pooled rms on LOW and REST under SF, compared with X43 (hard floor), computed with EM1's fit_one / pooled (best Υ per
  galaxy).

## Verdict (per footing; the class needs both footings to agree)

- **SOFT FLOOR PREFERRED:** in both backgrounds the SPARC line passes, LOW rms falls by ≥ 5 % relative to X43, and REST
  rms rises by ≤ 2 %.
- **HARD FLOOR PREFERRED:** LOW rms rises by ≥ 5 % in both backgrounds, or the SPARC line fails.
- **NOT DECIDED:** anything else.

**Reported:**
- the number of LOW galaxies;
- the 10 largest per-galaxy improvements and worsenings, with names;
- whether any SPARC galaxy named in the record as a dwarf problem moves.

MUTATE: F uses 2X₀ in place of 4X₀, with separate outputs. It must change the LOW rms by more than 1e-4, otherwise the
harness is insensitive.
