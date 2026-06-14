# Cluster eta a0-footing forensic — did any cluster analysis use a LOCAL/canonical a0?

Date 2026-06-14. Data: real eRASS1 primary (Bulbul+2024), 9830 clean clusters on disk.
Scripts audited: real_research/reviews/clusters_eta_audit.py, real_research/clusters_framework_a0.py,
real_research/reviews/cluster_a0_from_density_HIS_FORMULA.py, the project*cluster* family.

## 1. The forensic — what a0 did each banked analysis literally use?

The CANONICAL banked eta~2.15 claim comes from `clusters_eta_audit.py` and `clusters_framework_a0.py`.
BOTH set `A0_FRAME = 0.5*c*np.sqrt(G*RHO_DE0)` with `RHO_DE0 = OmL*RHO_CRIT0` => **9.361e-11 m/s^2**,
which equals `c^2*sqrt(Lambda/32pi)` exactly. This is the framework's OWN pure-dark-energy a0 — the LOWER value,
NOT 1.2e-10, NOT a local a0. Verified by re-running on disk. The standing ledger (sec 3a) reports eta from this footing.

No mixed/local a0 inflated the headline. The OLDER project scripts (cluster_residual_evolution.py: `A0=1.2e-10`;
project16, project_cluster_evolving_a0, project_cluster_a0z_xray) used a0=1.2e-10 AND the rising a0(z)=a0(0)E(z) law —
but these are explicitly labeled the WRONG/rival branch the framework superseded; they are NOT the banked eta claim.

A SEPARATE framework branch (cluster_a0_from_density_HIS_FORMULA.py) uses a0=(c/2)sqrt(G rho_AMBIENT) — clusters are
Mpc overdensities => in-cluster a0 ~10-14x larger => residual closes. The eta=2.15 audit does NOT apply this branch
(it uses cosmic-density a0 everywhere). This is the framework's own largest reducer, left on the table.

## 2. eta recomputed on the real data — the footing spread (dS-Unruh interp, WL masses, fstar=0.20)

| a0 footing | a0 (m/s^2) | eta_med (dS-Unruh) | eta_med (simple) |
|---|---|---|---|
| framework Lambda (pure DE) | 9.361e-11 | **2.33** | 2.15 |
| rho_total / cH0 | 1.131e-10 | 2.13 | 1.97 |
| McGaugh canonical | 1.200e-10 | 2.07 | 1.92 |

The a0 footing moves eta by only ~13%. **The framework a0 is the eta-WORST end** (lowest a0 => largest deep-MOND
deficit, since eta ~ 1/sqrt(a0)). Using canonical 1.2e-10 would LOWER eta to ~1.92-2.07. So the banked deficit is NOT
inflated by a footing error — it is computed at the framework's own least-favorable a0, honestly.

## 3. Reducers (shrink eta) and inflaters (grow eta), with sizes

REDUCERS (each defensible on the framework's/literature's own terms; NONE applied in the banked eta=2.15):
- **Hydrostatic-mass footing**, eta 2.33 -> ~1.80 (deflate /1.3) to ~1.1-1.4 (deflate /1.7-2.1). LARGEST inflater-as-
  reducer. Bulbul M500 are WEAK-LENSING-calibrated and run ~110% above hydrostatic (WL treated as upper limits).
  The foundational MOND-cluster lit (Sanders 99/03, Angus+08, Pointecouteau-Silk, Eckert/Famaey 2024) used HYDROSTATIC
  X-ray masses. So eta=2.33 vs the literature "factor ~2" is partly apples-to-oranges: same M_dyn footing => eta ~1.8.
- **Density-law a0** (framework's own branch): a0 x sqrt(5) -> eta 1.58; x sqrt(14) (B&B Mpc-ambient) -> eta 1.23;
  full closure needs a0 x ~4.6 (sqrt-overdensity ~30, vs B&B's ~10-14x). A genuine framework mechanism the audit omits.
- **EFE + hydrostatic bias** (Eckert/Famaey 2024, a0=1.2e-10): with bias+EFE the missing/baryon ratio drops to 0.4-1.1
  at 2-3 Mpc for relaxed clusters — i.e. clusters can largely close in the OUTSKIRTS. (Caveat: at R500/inner radii the
  EFE can INCREASE required mass; the reduction is radius- and relaxation-dependent, not a blanket R500 fix.)
- **Baryon budget**: fstar 0.20 -> 0.50 moves eta 2.15 -> 1.90 (simple). Modest.
- **Stacked, all defensible**: density a0 x2.2 AND hydro /1.3 => eta ~1.2. Either large reducer alone gets to ~1.6-1.8.

INFLATERS (grow eta; baked into the banked number):
- **Framework's own lower a0** 9.36e-11 vs 1.2e-10: +13% on eta (2.07->2.33). The framework footing is the worst case.
- **WL mass scale** used as M_dyn: the single biggest inflater (factor up to ~2 vs hydrostatic). Honest both ways:
  WL mass is arguably the MORE correct M_dyn (hydrostatic is biased low ~30% by non-thermal pressure), so this is the
  conservative/correct choice, not a bug — but it means eta=2.33 is NOT comparable to the classic hydrostatic "factor 2".
- **R500 (cosmic-a0) only**: the audit evaluates at one overdensity radius with cosmic a0; ignores the density-law a0
  rise toward dense cores that B&B's required-a0(r) trend actually favors.

## 4. Literature a0 census

| Source | a0 used | finding |
|---|---|---|
| Sanders 1999/2003 | canonical (1.2e-10-class) | clusters need ~2x extra mass; proposed 2 eV neutrinos |
| Angus-Famaey-Buote 2008 | 1.2e-10 | residual ~2x; centrally-concentrated missing mass |
| Eckert/Famaey 2024 (A&A) | **1.2e-10** | with bias+EFE, missing/baryon 0.4-1.1 (2-3 Mpc, relaxed) |
| Famaey-McGaugh 2012 review | 1.2e-10 | the standing ~2x cluster residual |
| Bulbul+2024 / Ghirardini+2024 | n/a (LCDM) | M500 WL-calibrated, ~110% above hydrostatic, WL = upper limits |

NONE of the foundational MOND-cluster literature mixed in the framework's lower 9.36e-11 — they all use canonical
1.2e-10 (the eta-FAVORABLE end). The banked eRASS1 audit, by contrast, used the framework's worst-case 9.36e-11.

## VERDICT: FOOTING-ROBUST (a0), but the deficit MAGNITUDE is INFLATED by the WL-mass footing, not the a0 footing.

- On the a0 question Carl raised: **no analysis sneaked in a local/canonical a0 to inflate the deficit.** The banked
  eta=2.15-2.33 uses the framework's OWN a0=9.36e-11, which is the LEAST favorable footing (canonical 1.2e-10 would
  LOWER eta ~13%). FOOTING-ROBUST on a0.
- BUT Carl's broader instinct ("the ~2x is a methodology artifact") has real support from a DIFFERENT footing the audit
  did not vary: the WL (not hydrostatic) mass scale inflates eta by up to ~2x vs the classic hydrostatic comparison,
  and the framework's OWN density-law a0 (a0~sqrt(rho_ambient), clusters overdense) plus the EFE/outskirt reductions can
  pull eta from 2.33 down to ~1.2-1.6. So the residual is real and SHARED with all MOND at R500, but its published
  ~2x magnitude is methodology-sensitive (mass footing + omitted density-law a0), not robust at face value.
