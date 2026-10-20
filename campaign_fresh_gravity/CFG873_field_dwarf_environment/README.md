# CFG873 — is the dwarf excess a satellite property or a small-system property? (field dwarfs, gas counted)

Criteria: `FROZEN_CRITERIA.md` (30dd0b297, committed alone before the script; owner block 870–879). Run: `python3 cfg873.py`
(`CFG873_MUTATE=up|down` → `cfg873_MUTATE_up.out` / `cfg873_MUTATE_down.out`). Seconds, numpy only, nothing downloaded.
κ = ½ fitted; footings never pooled; kernel ν_e; Υ from each dwarf's own SFH (CFG827).

## Result — CLASS: **UNDECIDED (GAS-SENSITIVE)**, both footings
Five isolated field dwarfs (Tucana, Cetus gas-free; Leo T, Phoenix, Aquarius HI-bearing) against 24 MW/M31 satellites at
matched g_bar, with the HI-bearing dwarfs' gas inside r½ counted (exponential HI disc, Wang+16 HI size–mass, ×1.33 helium).

| canonical (a0 9.3603e-11) | E_F (field over the law) | D (field − satellites at matched g_bar) | class |
|---|---|---|---|
| **primary** (extended HI disc) | **+0.199 ± 0.068** (2.9 se) | **−0.150 ± 0.097** (−1.6 se) | **UNDECIDED** |
| R_HI × 2 / ÷ 2 (bracket) | +0.227 / +0.240 | −0.136 / −0.129 | SMALL-SYSTEM / SMALL-SYSTEM |
| compact HI disc (post-hoc) | +0.152 ± 0.083 | −0.162 ± 0.096 | UNDECIDED (info) |
| all gas inside r½ (envelope) | +0.129 ± 0.095 | −0.165 ± 0.094 | UNDECIDED (info) |
| no gas (= CFG828 treatment) | +0.336 ± 0.086 | −0.087 ± 0.112 | SMALL-SYSTEM (info) |

Alternative footing (1.1312e-10): primary E_F +0.159 ± 0.068, D −0.150 ± 0.096 → UNDECIDED; bracket UNDECIDED / SMALL-SYSTEM.

Per dwarf (canonical, primary): Tucana Δ +0.17 (satellites at its g_bar +0.32), Cetus +0.13 (+0.49), Aquarius +0.01 (+0.24),
Phoenix +0.47 (+0.34), Leo T +0.22 (+0.36). Gas-free pair: E +0.15, D −0.25. HI-bearing trio: E +0.23, D −0.08.

**Reading.** Isolated dwarfs sit above the law in most variants, but about 0.15 dex below satellites at the same g_bar. Neither
"on the law" nor "the same as satellites" is established with five objects. Counting the gas matters: the HI-bearing dwarfs'
excess falls from +0.46 (stars only) to +0.23 (primary) or +0.12 (all gas inside). Leo T's gas outweighs its stars about 4:1
within r½ in the primary model, and Aquarius's about 2:1.

**Relation to CFG860** (stripping chat; stars only, Υ_V = 2): CFG860 found isolated gas-free dwarfs 0.15 ± 0.12 and
gas-bearing 0.06 ± 0.09 below satellites, with the gas-bearing group +0.37 ± 0.07 over the law (5.1σ). The offsets agree
with CFG873. CFG860's gas-bearing excess did not count those dwarfs' gas in g_bar, and with gas it is substantially smaller.
The two lanes together: isolated dwarfs carry part of the excess, plausibly less than satellites; the difference is not
resolved.

## Controls
- **K1 PASS:** with gas set to zero, per-dwarf Δ reproduces CFG828's rows exactly (max |ΔΔ| = 0 over 29 dwarfs).
- **MUTATE responds both ways:** field σ × 1.45 → SMALL-SYSTEM (E +0.52, D +0.17); field σ ÷ 1.45 → SATELLITE-ONLY
  (E −0.12, D −0.47, −4.9 se).

## Disclosures
- **The frozen bracket turned out one-sided.** The criteria did not say which of the two solutions of Σ_HI(R_HI) = 1 M_⊙ pc⁻²
  to take. The script, written before the run, takes the extended (larger-R_s) one. With R_HI × 2 there is no solution
  (fallback R_s = R_HI/2), and with R_HI ÷ 2 the extended solution is wider still. So both bracket arms put *less* gas inside
  r½ than the primary. The high-gas side is bounded by the compact-disc line (added after the first run, labelled post-hoc) and
  the all-gas envelope, and both stay UNDECIDED.
- Leo T's σ in CFG824 already equals the LVD 2026 value (6.05 km/s), so that sensitivity line is identical by construction.
- N(F) = 5. Tucana and Cetus may be backsplash objects. Phoenix's HI is offset from its stars, so the disc model overestimates
  its inner gas. Antlia B and UGC 4879 (in CFG860) lack an SFH-based Υ and are not used.
- **To decide:** about 20 isolated dwarfs with stellar kinematics would bring se_D to ~0.05 dex.

## For the record
Canonical v3's headline "a satellite property" is corrected (2026-10-19) to "a property of faint pressure-supported dwarfs;
satellite vs isolated difference unresolved" (CFG860 + CFG873).
