# CFG873 — FROZEN CRITERIA: is the dwarf excess a satellite property or a small-system property?

Frozen before any script (owner block 870–879). κ = ½ fitted; not theory closed.

## Question
CFG828 found an excess of ~+0.44 dex in g over the law for pressure-supported dwarfs at g_bar < 10⁻¹² m/s². Canonical v3
(2026-10-18) called it "a satellite property" from CFG829 (isolated large-galaxy lensing at the same g_bar sits on the law);
its own clarification notes that only N = 2 gas-free isolated dwarfs (Cetus, Tucana) were a same-scale comparison. Five
isolated (host = field) dwarfs have SFH-based stellar M/L in CFG827: Tucana, Cetus (gas-free) and Leo T, Phoenix, Aquarius
(HI-bearing). CFG828 and CFG870 treated all dwarfs as stars-only; for the HI-bearing three that understates g_bar.
This lane asks, with gas included: do isolated field dwarfs carry the satellites' excess at matched g_bar?

## Inputs (all already in the repo; no download)
- Stellar dispersion σ: CFG824 rows (`so`), as used in CFG828. Half-light radius, M_V, HI mass: LVD csvs (`rhalf_sph_physical`,
  falling back to `rhalf_physical`; `M_V`; `mass_HI` in log M_⊙; an upper limit `mass_HI_ul` counts as zero gas).
- Stellar mass: M* = Υ_SFH L_V with Υ_SFH from CFG827 (`ups`), L_V from M_V with M_V,⊙ = 4.83 (as CFG828).
- Samples: F (field) = CFG827 dwarfs with LVD host = field, minus CFG828's EXCL list unchanged (the rotation-supported
  gas-rich dIrrs WLM, NGC 6822, IC 1613, Leo A, Sagittarius dIrr, Pegasus dIrr, and M 32). This gives Tucana, Cetus, Leo T,
  Phoenix, Aquarius. S (satellites) = the remaining CFG827 dwarfs with host MW or M31. Antlia B (host NGC 3109; no Υ_SFH) is
  not used.

## Estimators (identical to CFG828 except the gas term, applied to F and S alike)
- r12 = (4/3) r_h; g_obs = 3σ²/r12 (Wolf); g_bar = G (M*/2 + M_gas,in)/r12².
- Gas: M_gas = 1.33 M_HI (helium). Exponential HI disc Σ(R) = Σ0 exp(−R/R_s), M_gas = 2π Σ0 R_s², with the HI radius
  R_HI = D_HI/2 at Σ_HI = 1 M_⊙ pc⁻² from log D_HI[kpc] = 0.506 log M_HI − 3.293 (Wang et al. 2016; also cross-checked in
  hunt_2026/k03). R_s solved from Σ_HI(R_HI) = 1 M_⊙ pc⁻² (HI only, before the helium factor). M_gas,in = M_gas × [1 − (1+x) e^−x],
  x = r12/R_s (cylindrical enclosed fraction). If no R_s solution exists (Σ0 < 1), use R_s = R_HI/2 (disclosed if used).
- Law: g_law = g_bar ν(g_bar/a0), ν_e(y) = 1/(1 − e^−√y). Δ = log10(g_obs/g_law). Footings 9.3603e-11 and 1.1312e-10, never pooled.

## Statistic
- E_F = mean Δ over F (field excess over the law); se by bootstrap over F objects (4000 draws, seed 873).
- Satellite reference at each field dwarf: mean Δ of S members with |log g_bar,S − log g_bar,i| ≤ 0.4 (need ≥ 5; else widen to
  0.6). D_i = Δ_i − ref_i; D = mean D_i; se_D by joint bootstrap over F and S (4000 draws).

## Classes (canonical primary; the alternative footing must agree, else the overall class is UNDECIDED)
- NOT DIAGNOSTIC: se_D > 0.20 dex.
- SMALL-SYSTEM: E_F/se_E ≥ 3 and |D|/se_D < 2 (field dwarfs carry the excess, consistent with satellites).
- SATELLITE-ONLY: E_F/se_E < 2 and D/se_D ≤ −3 (field dwarfs on the law, below satellites).
- PARTIAL: E_F/se_E ≥ 2 and D/se_D ≤ −2 (field dwarfs carry less excess than satellites).
- UNDECIDED: anything else.

## Gas bracket (reported; flags the verdict, does not replace it)
Recompute with R_HI × 2 and R_HI ÷ 2 (a ±0.3 dex bracket, five times the relation's 0.06 dex scatter). If the class differs
anywhere in the bracket, the verdict carries the flag GAS-SENSITIVE. Envelopes with M_gas,in = 0 and = M_gas are printed
for information only.

## Subsets (diagnostic, not decision)
Gas-free F (Tucana, Cetus) and HI-bearing F (Leo T, Phoenix, Aquarius) reported separately: E and D for each.

## Controls
- K1 (code identity): with gas set to zero for every object, the per-dwarf Δ (canonical, ν_e) must reproduce CFG828's rows
  to |ΔΔ| < 1e-9 for all common dwarfs. FAIL ⇒ lane INVALID.
- MUTATE (`CFG873_MUTATE=up|down`): field σ × 1.45 (up) or ÷ 1.45 (down), real data otherwise. The statistic responds if
  MUTATE-down does not give SMALL-SYSTEM and MUTATE-up does not give SATELLITE-ONLY. Outputs written separately by mode.

## Disclosed limits (fixed now)
- N(F) = 5; Tucana and Cetus are possible backsplash objects (may once have passed through a host). The HI-bearing three
  are unlikely to have passed pericentre with a large host (ram pressure would strip the gas).
- The HI disc model ignores Phoenix's HI offset from the stars (overestimates its inner gas → lowers its Δ; conservative for
  SMALL-SYSTEM) and extrapolates Wang+16 below its main calibration range (covered by the ±0.3 dex bracket).
- Leo T's σ is taken from CFG824 for K1 continuity; the LVD lists a 2026 value (6.05 km/s), reported as a sensitivity line.
