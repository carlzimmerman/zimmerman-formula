# CFG874 — all isolated Local Group dwarfs, pooled, gas counted: satellite or small-system excess?

Criteria: `FROZEN_CRITERIA.md` (ac12da6c0, committed alone before the script; owner block 870–879). Run: `python3 cfg874.py`
(`CFG874_MUTATE=up|down` → separate outputs). Seconds, numpy only, nothing downloaded. κ = ½ fitted; footings never pooled; ν_e.

## Result — CLASS: **UNDECIDED** (both footings; not gas-sensitive)
All 11 LVD dwarfs with a measured stellar σ at ≥ 300 kpc from both the MW and M31 (Eridanus II, Perseus I, Andromeda XXVIII,
Andromeda XVIII, Cetus, Tucana, Phoenix, Leo T, Antlia B, Aquarius, UGC 4879) against 54 gas-free satellites in the same g_bar
range. Υ_V = 2 for all; HI gas inside r½ counted for every dwarf (Wang+16 discs, extended root).

| canonical | c (isolated − satellites, matched g_bar) | E (isolated over the law) | class |
|---|---|---|---|
| **primary** | **−0.100 ± 0.091** (−1.1 se) | **+0.194 ± 0.077** (+2.5 se) | **UNDECIDED** |
| compact HI disc | −0.105 ± 0.093 | +0.174 ± 0.080 | UNDECIDED |
| half gas inside (CFG860) | −0.100 ± 0.091 | +0.193 ± 0.079 | UNDECIDED |
| no gas / all gas (info) | −0.086 / −0.106 | +0.246 / +0.164 | SMALL-SYSTEM / UNDECIDED |

Alternative footing: c −0.100 ± 0.091, E +0.155 ± 0.077 → UNDECIDED.

Variants (canonical, all UNDECIDED): Υ_SFH where available c −0.093, E +0.225 (2.9 se); satellites M_V ≤ −6 c −0.054;
full-range fit c −0.141 ± 0.097; Antlia B dropped c −0.109; + Leo A and Sagittarius dIrr c −0.102, E +0.145;
**strict isolation ≥ 500 kpc** (Cetus, Tucana, Antlia B, Aquarius, UGC 4879) c −0.126 ± 0.080, **E +0.046 ± 0.048**.

**Reading.** At matched g_bar the isolated dwarfs sit 0.10 ± 0.09 dex below satellites (not significant) and 0.19 ± 0.08 above
the law (2.5 se, short of the 3 se bar). Pooling all 11 did not shrink the error much (0.09 vs CFG873's 0.10), because the
isolated dwarfs scatter widely (Eridanus II +0.71, Andromeda XVIII +0.61, Perseus I −0.08). This is the whole Local Group
supply, so the satellite-vs-isolated question cannot be decided with existing stellar kinematics.

**A hint, not a result (from a variant).** The five dwarfs ≥ 500 kpc from both hosts sit near the law (E +0.05 ± 0.05). The two
largest isolated excesses (Eridanus II, Andromeda XVIII) are among the closest to a host (372 and 427 kpc). The strict group also
sits at higher g_bar, where satellites show less excess too, so at matched g_bar its offset is only −0.13 ± 0.08. A
host-distance trend at fixed g_bar needs its own frozen test.

## Controls
- **K1 PASS:** with gas zero and Υ_V = 2, all 11 isolated Δ equal CFG860's values exactly (max |ΔΔ| = 0).
- **MUTATE responds:** isolated σ ÷ 1.45 → SATELLITE-ONLY (c −0.42, −4.7 se). σ × 1.45 → c +0.22 (+2.4 se), E +0.52. This is
  UNDECIDED, not SMALL-SYSTEM, because the class list has no "isolated above satellites" class (disclosed; allowed by the frozen check).

## Disclosed limits
Stellar rotation is not treated (it would raise isolated Δ). Binary-inflated ultra-faint satellites lower c (variant M_V ≤ −6
moves c to −0.05). Five isolated dwarfs lie 340–430 kpc from a host (possible backsplash). Bootstrap errors with N = 11 are approximate.
