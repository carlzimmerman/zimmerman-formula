# CFG838 FROZEN CRITERIA: is the satellite-dwarf excess driven by the host's tides? (committed before any script)

**ID note:** CFG838 is taken from the owner-chat block 830–839 (830–835 and 837 used by the parameter-reduction chat, 836 by
the HOTGAS lane); 838 and 839 were free at the time of writing.

**Why.** CFG829: isolated late-type galaxies sit ON the law at the dwarfs' accelerations (A = 1.02 ± 0.09), so the dwarfs'
+0.44 dex excess (CFG828) is a property of satellite dwarfs, not of the law's deep regime. The first suspect is the host's
tidal field (stripping, heating, out-of-equilibrium dispersions).

## Sample and inputs
- The 29 pressure-supported dwarfs of CFG828 with their residual Δ = log10(g_obs/g_law) at r_1/2 (canonical, ν_e; read from
  `CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json`).
- Satellites: LVD `host` = mw or m_031 with `distance_host` D. Field: no host (reported separately).
- Host baryonic masses (declared): MW 6.0e10 M_⊙ (CFG821's value); M31 1.0e11 M_⊙ primary, 1.5e11 bracket. Point mass at D.
- Host field g_host(D) = the law applied to G M_host/D²; tidal acceleration across the dwarf a_tide = |dg_host/dD| × r_1/2
  (numerical derivative). Dwarf internal field g_int = the law's g at r_1/2 from its own stars (Υ_SFH, as CFG828) —
  NOT g_obs, so the tidal parameter does not contain the excess.
- **Tidal parameter T = a_tide / g_int.** Also reported: the external-field ratio g_host / g_int,N.

## Statistic and classes (satellites, primary host masses)
- One-sided Spearman ρ(Δ, log T).
- **TIDES IMPLICATED** if N ≥ 15 and ρ > 0 with p < 0.05 (and the M31-mass bracket keeps p < 0.10).
- **OPPOSITE** if ρ < 0 with one-sided p < 0.05. **NO TIDAL SIGNAL** otherwise.
- Report the field dwarfs' Δ (gas-free field dSphs Cetus and Tucana flagged; gas-bearing field dwarfs' Δ is an upper bound,
  since CFG827/828 omit gas).

## Controls
- K1: Draco's T and g_host/g_int,N printed and checked by hand against D = 82 kpc, r_1/2 from LVD.
- MUTATE (separate output): (a) Δ_inj = 0.3 log10 T + N(0, 0.1) (seed 838) must class TIDES IMPLICATED; (b) a shuffle of T
  (seed 838) on the real Δ must not.

κ = ½ fitted; cold energy mass required; not theory closed. A TIDES IMPLICATED would say the dwarf excess is environmental
(no new gravity needed there); it would not by itself show that the framework's tidal response is right.
