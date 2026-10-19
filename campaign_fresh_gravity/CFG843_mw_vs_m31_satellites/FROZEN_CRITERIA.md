# CFG843 FROZEN CRITERIA: does the satellite excess differ between Milky Way and Andromeda satellites at matched g_bar? (before any script)

**Why.** CFG828–842: faint dwarfs carry ~+0.4 dex excess over the law at g_bar < 10⁻¹² m/s²; tides, capture, expelled gas
and own supply do not explain it. If it is environmental (host-driven), MW and M31 satellites — different hosts, different
histories, independent kinematic surveys — should differ at the same internal acceleration. If it is intrinsic to faint
dwarfs (or a shared measurement systematic of faint systems), they should agree.

## Sample and statistic
- The CFG828 rows (canonical, ν_e; Δ = log10 g_obs/g_law at r_1/2, Υ_SFH) for dwarfs with LVD host = mw or m_031.
- Fit Δ = a + b (log10 g_bar + 12.5) + c [host = M31] by unweighted least squares; c = the M31 − MW offset at matched g_bar;
  error from 2000 bootstrap resamples over dwarfs (seed 843).
- **SAME** if |c| < 2 σ_c AND |c| < 0.15 dex (the hosts agree: favours an intrinsic / faint-dwarf property).
- **DIFFERENT** if |c| ≥ 3 σ_c (environmental component).
- **INCONCLUSIVE** otherwise. NOT DIAGNOSTIC if either host has < 6 dwarfs.
- Reported: means per host, b, and the same fit restricted to g_bar < 10^−11.9.

## Controls
- K1: the fit with c forced to 0 reproduces the pooled least-squares slope computed independently with numpy.polyfit.
- MUTATE (separate output): add +0.3 dex to every M31 Δ → must class DIFFERENT.

κ = ½ fitted; cold energy mass required; not theory closed.
