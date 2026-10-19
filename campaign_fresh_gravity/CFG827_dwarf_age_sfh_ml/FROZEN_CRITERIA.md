# CFG827 FROZEN CRITERIA (= "CFG824b"): the age test with each dwarf's own SFH-based stellar M/L (committed before any script)

**Why.** CFG824's out-of-sample age trend passed with Υ_V = 2 (ρ +0.42, p 0.012) but fell to p 0.11 under a crude M/L scaling
(C-ML), so it was NO SIGNAL. CFG826 found the trend, extrapolated, matches the binary-corrected UFDs. The open question is
only the stellar M/L. Here every dwarf gets the M/L its own published star-formation history implies.

## M/L per dwarf
- Models: E-MILES SSP photometric predictions v11.0, Kroupa universal IMF, Padova 2000 isochrones, base [α/Fe]
  (`real_research/data/dsph/emiles_ml_dl/UBBVRIJHK_ku_iPp0.00.MAG`, sha256 8b516912c37b99cf…, downloaded 2026-10-18 from the
  IAC MILES site). Per unit initial mass: M_now(t) = M(*+remn); L_V(t) = M(*+remn) / ML(V_Buser).
- SFH: Weisz+14 cumulative fractions f(log t) (table 6 combined fields where given, else table 5), exactly as CFG824 reads
  them. Mass formed in each grid bin = f(younger edge) − f(older edge); mass formed before the oldest grid point (log t = 10.1)
  is placed at 13.3 Gyr. Each bin's age = the geometric mean of its edges, clipped to the model age range [0.0631, 17.78] Gyr;
  ML and M_now interpolated linearly in log age between model nodes.
- Υ_SFH = Σ dM_i M_now(t_i) / Σ dM_i L_V(t_i).
- **Metallicity (declared, one value for all dwarfs):** primary [M/H] = −1.31; brackets −1.71 and −0.71 (model grid nodes).
- UFDs (for the CFG826 re-check): a single burst at 13.3 Gyr.
- Stars only (gas omitted, as in CFG821/824; declared: this omission raises E for gas-rich young dwarfs, AGAINST the trend).

## Statistic and classes (out-of-sample 28 of CFG824, canonical a0; alt reported)
- E_SFH = ln(σ_obs / σ_law(Υ_SFH)), σ_law = CFG821's isolated law unchanged. One-sided Spearman ρ(E_SFH, τ90) and CFG824's
  weighted slope.
- **SUPPORTS** if ρ > 0 with one-sided p < 0.05 at [M/H] = −1.31 AND p < 0.10 at both brackets.
- **OPPOSITE** if ρ < 0 with one-sided p < 0.05 at −1.31. **NO SIGNAL** otherwise. NOT DIAGNOSTIC if N < 8.
- Report beside it: the training MW 8 (not a verdict), and the CFG826 UFD re-check with Υ_SFH (same statistic as CFG826:
  the SFH-trend extrapolated to 12.5 Gyr vs the 7 binary-corrected UFDs; z vs trend and vs flat).

## Controls
- K1: an SFH entirely in the bin containing 12.59 Gyr reproduces the table's ML(V) at that node within the interpolation
  (|ΔΥ/Υ| < 0.05).
- MUTATE (separate output): every dwarf's SFH replaced by a 1-Gyr burst → Υ must collapse to the 1-Gyr model value for all
  (bites), and a τ90 shuffle (seed 827) on the real E_SFH must NOT class SUPPORTS.

κ = ½ fitted; cold energy mass required; not theory closed. A SUPPORTS would make H-FOSSIL a hypothesis worth deriving from
the action, not a result.
