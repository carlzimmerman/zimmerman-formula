# CFG844 FROZEN CRITERIA: H-PRIM — early-collapse free cold energy as the faint-dwarf excess (committed before any script)

## Hypothesis H-PRIM (new; framework-native ingredients only)
Small systems assemble first. The free (untethered, H-EX) share of a dwarf's catchment cold energy collapses WITH the system
at its collapse epoch z_c and, being free, is neither expelled by the tether (CFG776/837 concern tethered surplus) nor spread
to r_ta (CFG822's Method A): it keeps the density of the universe at z_c. CFG827 tested STELLAR age only; assembly epoch is set
by mass, not star formation. Predictions: (i) the needed extra inner density tracks the collapse-epoch density
(ρ_need ∝ (1 + z_c)³ in mean); (ii) the amplitude is that of a collapsed object at z_c times an inner-profile factor.

## Inputs (all framework-native or from the record)
- Dwarfs: the 24 MW/M31 satellites of CFG843 plus the 5 field dwarfs of CFG838 (Cetus, Tucana, Aquarius, Phoenix, Leo T).
  M_b = Υ_SFH L_V (CFG827); Δ from CFG828; ρ_need = 3 M_extra / (4π r_1/2³), M_extra = g_law (10^Δ − 1) r_1/2²/G (as CFG842);
  dwarfs with Δ ≤ 0.05 dex have no excess to explain and are excluded from the trend (listed).
- Catchment: f_ret = 0.10 (census floor, CFG822), baryons bc = M_b/f_ret, cold supply 5.364 bc, total M_cat = 6.364 bc.
  Free share of the cold supply f_free = 1 − f_ret = 0.90 (H-EX: the expelled baryons' cold share).
- Native cosmology: `CFG654_independent_inputs/cfg654_ics_tables_cmb.npz` (the addendum-A1 primary native set): h, ω_b, ω_c,
  P_lin0(k) (native A_s normalisation), growth lnD(ln a). σ(R) = top-hat at z = 0 from P_lin0;
  R_L = (3 M_cat/(4π ρ̄_m0))^{1/3}; collapse when σ(R_L) D(z_c)/D(0) = δ_c = 1.686.
- Collapsed mean density (EdS spherical collapse, valid in the matter era at z_c ≳ 2; declared): ρ_vir,free =
  Δ_c f_free (ω_c/(ω_b+ω_c)) ρ̄_m(z_c), Δ_c = 178; r_vir from M_cat.

## Statistic and classes
- T1 (trend): Spearman ρ and the log-log slope s of ρ_need vs ρ_vir,free over dwarfs with an excess.
- T2 (amplitude): P = median of ρ_need/ρ_vir,free (an inner-profile factor; must be ≥ 1 because r_1/2 ≪ r_vir is denser than the
  mean) and the check r_1/2 < r_vir for every dwarf.
- **SUPPORTS** if T1 ρ > 0 with one-sided p < 0.05 AND 0.5 ≤ s ≤ 1.5, AND 1 ≤ P ≤ 300.
- **AMPLITUDE ONLY** if 1 ≤ P ≤ 300 but T1 fails (the needed densities are reachable but not ordered by z_c).
- **FAILS** if P < 1 (collapse-epoch free cold energy too dilute even at the virial mean... i.e. cannot reach) or P > 300
  (would need an implausible profile), whatever T1 says.
- Report z_c, ρ_vir,free, r_vir, P per dwarf; the field dwarfs separately.

## Controls
- K1: native σ8 from P_lin0 printed and compared with the CFG654 record value (if stated) — informational; and D(0) = 1.
- MUTATE (separate output): z_c forced to 0 for all (no early collapse) → P must rise by (1 + z_c)³ (bites).

κ = ½ fitted; cold energy mass required; not theory closed. A SUPPORTS would make H-PRIM a candidate to derive (free-share
collapse in the native PM runs), not a result.
