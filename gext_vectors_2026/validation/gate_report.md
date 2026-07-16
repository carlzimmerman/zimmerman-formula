# GATE REPORT — reconstructed g_ext environment vectors for SPARC (Phase 1)

Date: 2026-07-16. All numbers below are COMPUTED, none hard-coded.
Phase 2 re-run 2026-07-16: full pipeline re-executed end-to-end (`run_pipeline.py ks115
--write`, exit 0), CSV regenerated, and `check_gates.py` re-verified every number below
from the delivered CSV alone (exit 0) — GATE-A maxclu r=0.889 / +0.100 dex / 0.127 dex,
noclu r=0.860 / +0.117 dex / 0.146 dex; GATE-B Virgo median 11.6 deg (n=106), Coma
median 40.2 deg (n=3). Identical to the Phase 1 values.
Reproduce with:
- `python3 src/gext_estimator.py` (unit test: synthetic point mass, machine precision)
- `python3 src/run_pipeline.py ks115 --write` (full pipeline + both gates)
- `python3 validation/check_gates.py` (recomputes both gates from the delivered CSV alone)

Deliverable: `data/gext_vectors.csv` (175 rows, one per SPARC galaxy).
Method + every load-bearing convention with its Chae Sec. 3 citation or [OURS] flag:
`src/METHOD_NOTES.md`.

## Estimator in one line

2M++ (Ks<=11.5, D<=200 Mpc; stellar mass 0.64 x L_Ks per Chae Sec. 3.1; gas via Chae
Eqs. 7-8; ZoA clones kept) + MCXC clusters (M_MOND via Chae Eqs. 3-4; (d/R500)^3 interior)
-> Newtonian vector sum at each SPARC position (VizieR SIMBAD coords, SPARC distances).
"noclu" = raw visible sum. "maxclu" = per-galaxy 1/f(D) K-band-LF completeness up-weight
(analog of Chae's satellite max-clustering) x8 cosmological missing baryons (Chae Sec. 3.2.4).
NSA and Karachentsev catalogs NOT used (see Gaps).

## Catalog counts / match rates

| item | ours | reference |
|---|---|---|
| SPARC galaxies with coordinates | 175/175 | VizieR J/AJ/152/157 (SIMBAD positions) |
| 2M++ total rows parsed | 72,973 (69,160 real + 3,813 ZoA clones) | LH11 |
| 2M++ after Ks<=11.5 & D<=200 (primary mode) | 27,630 | — |
| 2M++ after D<=200 only ('full' mode) | 54,488 | Chae quotes 54,483 |
| MCXC clusters, D<=200 Mpc | 234 of 1,743 | Piffaretti+ 2011 |
| Chae Table-3 galaxies matched by name | 109/109 | chae21_env.csv |

Catalog-selection discrepancy (documented, both modes run): Chae's text says he removed
Ks>11.5 AND cut at 200 Mpc leaving "54,483 out of 69,160", but 54,483 is numerically the
D<=200 cut alone (we get 54,488 including ZoA clones); the joint cut gives 27,630. We ran
both; the text-faithful ks115 mode gates marginally better and is the primary.

## GATE-A — amplitude correlation vs Chae's published Table 3 (109 galaxies)

Primary (ks115 mode, gas ON, E(z) as written, delivered CSV):

| column | Pearson r | global offset (Chae − ours) | scatter after 1 global offset |
|---|---|---|---|
| **maxclu (primary target)** | **0.889** | **+0.100 dex** | **0.127 dex (std), 0.107 (MAD-robust)** |
| noclu | 0.860 | +0.117 dex | 0.146 dex (std), 0.134 (MAD-robust) |

Targets were r >~ 0.8 and scatter <~ 0.3 dex: **PASS on both columns, with margin.**
The single global offset (+0.10 dex, i.e. our raw sum is ~20% low — expected, since we
omit NSA-depth structure, Karachentsev, and the outside-footprint grid) is the ONE allowed
global calibration; it is REPORTED, not applied to the CSV. No per-galaxy tuning anywhere.

Robustness (all satisfy the gate):

| variant | maxclu r / offset / scatter | noclu r / offset / scatter |
|---|---|---|
| ks115 baseline | 0.889 / +0.100 / 0.127 | 0.860 / +0.117 / 0.146 |
| full catalog (54,488 srcs) | 0.881 / +0.112 / 0.133 | 0.855 / +0.105 / 0.143 |
| E(z) with sqrt (std convention) | 0.888 / +0.099 / 0.127 | 0.860 / +0.116 / 0.146 |
| gas OFF | 0.896 / +0.147 / 0.135 | 0.867 / +0.159 / 0.153 |
| 1/c11.5 incompleteness weight ON | 0.886 / +0.101 / 0.127 | 0.858 / +0.114 / 0.145 |

Direction stability across the bracket: median cos(noclu-vector, maxclu-vector) = 0.999
(min 0.876) — the DIRECTION is essentially insensitive to the clustering bracket (the x8
is isotropic by construction; only the LF up-weight re-balances contributors).

## GATE-B — dominant-attractor direction sanity (delivered vectors)

- **Virgo**: 106 SPARC galaxies lie within 20 Mpc of Virgo (RA 187.7, Dec +12.3, D 16.5).
  Median angle between the reconstructed g_ext vector and the direction to Virgo:
  **11.6 deg** (random expectation 90 deg). Dominant contributor = the Virgo cluster
  (MCXC J1230.7+1220) for ~100 of them.
- **Coma**: the 3 SPARC galaxies within 30 Mpc of Coma (IC4202, F574-1, F574-2) all have
  the Coma cluster (RXC J1259.7+2756) as dominant contributor; angles 20.9-40.4 deg,
  median **40.2 deg** (these sit inside the Coma-A1367 wall, so a pure-Coma pointing is
  not expected even physically).
- Physically-correct fine structure (not imposed anywhere): M81-group members IC2574 and
  NGC2976 are dominated by M81 (2MASS 09555243+6940469) and point AWAY from Virgo;
  Perseus-Pisces-region galaxies (NGC0801, UGC02885, UGC02916...) are dominated by the
  Perseus cluster (RXC J0319.7+4130).
- WEAK check (declared weak up front): D > 60 Mpc galaxies vs the Great Attractor/Norma
  direction — median 52.7 deg, individually 16-133 deg. Expected: far SPARC galaxies are
  mostly northern, where CfA2/Coma/Perseus-Pisces legitimately beat the (southern) GA.
  This check neither passes nor fails cleanly; it is not load-bearing.

**Verdict: GATE-A PASS + GATE-B PASS → the direction table is fit for the pre-registered
aligned-asymmetry statistic**, with the caveats below.

## Direction-robustness flags in the CSV

`dom_share` = |g| of the single largest contributor / |g_total| (maxclu weighting).
`flag` = robust if dom_share >= 0.5 else soft. Counts: **94 robust / 81 soft**.
Dominant contributor is a cluster for 162/175 (Virgo dominates most of the SPARC-north sky).
For the directional-EFE statistic, the soft rows carry direction uncertainty that this
point-estimate pipeline does not quantify — treat robust/soft as a stratification variable.

## Gaps (honest impact estimate)

1. **NSA not fetched** (~2.7 GB) and Karachentsev not used. Chae's published Table 3 IS
   the NSA-based SDSS-footprint calculation, so GATE-A directly measures what our
   2M++/MCXC sum misses: a +0.10 dex global deficit and 0.127 dex per-galaxy scatter
   against his maxclu column. I.e. the 2M++/MCXC sum captures the per-galaxy amplitude to
   ~30% rms after one global constant. For DIRECTIONS the missed component is faint/local
   structure; where it matters most (soft-flag rows) it is flagged.
2. Outside-SDSS-footprint homogeneous grid (Chae 3.2.3) not added: isotropic homogeneous
   mass contributes ~zero net vector in an all-sky sum (it partly explains our +0.10 dex
   amplitude deficit, not direction).
3. No Monte Carlo uncertainty propagation (Chae 3.2.5): point estimates only; Chae's own
   published per-galaxy sigmas (~0.24-0.38 dex) exceed our scatter against him.
4. E(z) convention in Chae Eq. 3 ambiguous in ar5iv rendering; both conventions run,
   difference negligible (see table).
5. MCXC redshifts used heliocentric as-catalogued (CMB correction <~300 km/s, < 5% in D
   for D > 30 Mpc; degenerate with the global offset for the nearest clusters).
