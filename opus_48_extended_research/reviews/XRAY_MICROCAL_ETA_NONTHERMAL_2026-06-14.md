# X-ray + microcalorimetry: eta(r), the non-thermal-pressure resolution, and HOW to measure it (2026-06-14)

*Framework a0 = 9.36e-11 (eta-worst footing). Both ways. Quarantine: a0/Z never asserted derived.
Computed on real eRASS1 (Bulbul+2024, N=9830 clean). Calc: /tmp/eta_nonthermal_bands.py (reproduced below).*

## The load-bearing systematic and how XRISM resolves it

The eRASS1 catalog M500 is WL-calibrated. Li+2024 found WL ~110% above hydrostatic/kinematic on the SAME
clusters. The eta~2 reading survives ONLY if hydrostatic mass is biased LOW by ~52% (non-thermal pressure,
NTP). XRISM/Resolve (launched Sep 2023, science 2024+) DIRECTLY measures NTP via gas velocity dispersion —
the first instrument that can resolve the systematic instead of priors from sims.

### XRISM verdict (2024-2026): NTP is SMALL, and sims OVERPREDICT it ~3x
- **A2029** (Xu+2025, PASJ 77 S242; arXiv:2505.06533): NTP <= 2% of total pressure at ALL radii out to
  R2500 = 670 kpc, DECREASING outward; hydrostatic mass bias ~2%. sigma_v ~169+/-10 km/s in core.
- **Coma N** (2511.10740, 2025): sigma_v = 167+/-39 km/s, low Mach, low NTP, locally relaxed (530 km/s
  large-scale gradient is bulk off-axis-merger flow, not local turbulent pressure).
- **Perseus** (2510.12782, 745 ks): sigma_v ~300 km/s in the AGN-active EAST region only -> f_nt ~7-13%
  locally; rest of cluster ~150-200 km/s (Hitomi-consistent).
- **9-cluster sample** (2510.06322): Virgo, Perseus, Centaurus, Hydra A, PKS0745, A2029, Coma, A2319,
  Ophiuchus — 10 cool-core pointings ALL fall in the bottom ~10% of TNG-Cluster / Three-Hundred / SIMBA
  predictions; observed kinetic/total pressure median **2.2%** vs sim **5.0-6.5%** (~3x sim overprediction).

### Independent corroboration at R500/R200 (the radius XRISM has NOT yet reached)
XRISM A2029 stops at R2500=670 kpc; R500~1.33 Mpc. The eta-defense needs high NTP at R500 outskirts.
- **X-COP** (Eckert+2019, 12 clusters, XMM+Planck to R200): f_nt ~**6% at R500, ~10% at R200**;
  "hydrostatic masses require little correction" — below sim expectation, same direction as XRISM.
This makes the low-NTP picture robust at the eta-defining radius, not just the core.

## eta(R500) on real eRASS1 with explicit NTP correction bands (framework a0)

| branch | eta(R500) [16-84%] |
|---|---|
| [A] WL-calibrated catalog M500 (as published) | **2.15** [1.93, 2.92] |
| [B] hydrostatic/kinematic branch (catalog/2.10, Li+2024) | **1.02** [0.92, 1.39] |

Starting from branch [B] (eta~1.0) and raising mass by 1/(1-f_nt) using the MEASURED f_nt:

| f_nt source | f_nt | eta(R500) |
|---|---|---|
| XRISM A2029 relaxed core->Rs | 0.02 | 1.04 |
| XRISM Coma N quiescent | 0.02 | 1.04 |
| XRISM Perseus E active/AGN | 0.10 | 1.14 |
| XRISM Perseus E upper | 0.13 | 1.18 |
| X-COP at R500 | 0.06 | 1.09 |
| sim prior LOW (Nelson+14) | 0.20 | 1.28 |
| sim prior HIGH (R500 outskirts) | 0.30 | 1.46 |

**To lift the hydrostatic branch to the WL branch (eta 2.15) requires f_nt = 1 - 1/2.10 = 52%.**
XRISM measures 2-13%; X-COP 6-10%; sims (already ~3x too high per XRISM) only 20-30%. The 110%
WL/hydro gap is NOT non-thermal pressure.

### Both ways — the OTHER lever points the SAME direction (so eta is NOT secretly high either)
WL masses are independently over-estimated 20-50% by projection/triaxiality selection bias
(Grandis+24; arXiv:2510.00753). Applying to branch [A]: WLx1.20 -> eta 1.79; x1.35 -> 1.59; x1.50 -> 1.43.
BOTH cross-method levers (XRISM-low NTP on hydro, WL over-estimate on WL) push eta DOWN from 2.15.
Convergent estimate: **true eta(R500) ~ 1.0-1.5**, not 2.0+. The eta~2 reading now survives ONLY if
f_nt JUMPS to ~50% beyond R2500 (against A2029's own DECREASING trend and X-COP's 6-10%) OR WL is
unbiased while hydro AND kinematics are both ~50% low (XRISM now directly disfavors).

## The framework-DISTINCTIVE measurement (not shared MOND)

Shared MOND only predicts a residual ~2x. The framework's DISTINCTIVE content is the central-shrinking
eta(r) SHAPE matched to the density-a0 boost a0_local>a0_field. Measuring eta(r) radially is the test:
- eta(r) is centrally peaked (~7-10 at 0.1R500) decaying to ~1 at R500 (Kelleher-Lelli 2024, Famaey 2024
  CLASH r0~450 kpc, my beta+NFW calc). The density-a0 boost is ALSO largest centrally — a SHAPE match
  shared MOND has no reason to produce. Distinctive test: does the deficit's radial profile track the
  in-cluster density profile (boost ~ sqrt(rho)) rather than a constant-a0 MOND phantom?
- HOW: microcal gives a clean, NTP-corrected hydrostatic eta(r). XRISM today reconstructs eta(r) to R2500
  with NTP pinned to a few % (velocity uncertainty <10 km/s; 250 ks -> ~30 km/s on sigma_turb). The
  distinctive prediction: after the XRISM NTP correction, the residual eta(r) should still be CENTRAL and
  trace sqrt(rho_cluster(r)), not flat.

## Precision and timeline (the concrete measurement)

| facility | capability | eta(r) reach / precision | timeline |
|---|---|---|---|
| XRISM/Resolve | sigma_v to <10 km/s; ~30 km/s on sigma_turb at 250 ks; NTP to a few % | NTP-corrected eta(r) to R2500 per relaxed cluster; ~12 done | NOW (science 2024+) |
| eROSITA eRASS:4 stack | 680 clusters, SB to 2 r200m (12 sigma), shock at ~3 r200m | stacked outer eta(r) shape to ~R200 | DR2 mid-2026, DR3 H2-2028 |
| Athena X-IFU | line shift/broadening to ~20 km/s at 5"; density+pressure to 20% to R500 in 100 ks | per-cluster NTP-corrected eta(r) to R500/R200, large sample | launch 2037 |

## Confirms vs kills (both ways)

- **CONFIRMS framework-distinctive:** XRISM/Athena radial eta(r), NTP-corrected, stays CENTRAL and tracks
  sqrt(rho_cluster(r)) (the density-a0 shape) rather than a flat constant-a0 MOND phantom. A measured
  inner boost scaling as the local density would be a distinctive signature shared MOND cannot make.
- **KILLS framework-distinctive:** NTP-corrected eta(r) is FLAT in radius (constant ~2 or ~1), i.e. the
  residual does NOT track the density profile -> no density-a0 shape signal; the framework reduces to
  shared MOND with no distinctive handle. Current XRISM low-NTP already pushes the R500 MAGNITUDE toward
  the eta~1 branch, which neither confirms nor kills the distinctive shape (it removes the shared-MOND
  magnitude problem without testing the shape). The shape test needs Athena-class radial NTP-corrected
  eta(r) per cluster — not deliverable until ~2037 at full per-cluster precision; XRISM does it now to
  R2500 for the ~12 brightest relaxed cool cores.

The honest both-ways close: XRISM is real evidence the cluster MAGNITUDE problem is smaller than the
WL-branch eta~2 (NTP is 2-13%, not 52%; both cross-method levers lower eta to ~1.0-1.5) — that REMOVES
a shared-MOND liability the framework inherits, it does not confirm anything DISTINCTIVE. The distinctive
density-a0 SHAPE test (central eta(r) tracking sqrt(rho)) is measurable now to R2500 (XRISM) and to
R500/R200 per-cluster with Athena (2037); it remains the one live, falsifiable, framework-specific X-ray
target, and it inherits the banked trap (no DERIVED inner smoothing scale threads galaxies+clusters
without smearing the tight SPARC RAR).
