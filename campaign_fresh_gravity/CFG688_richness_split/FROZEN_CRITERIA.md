# CFG688 — is CFG687's M^0.9 outer scaling real or X-ray selection? Re-bin by optical richness (FROZEN, before any number)

Block CFG680–689. Owner "figure out clusters" (2026-10-13). CFG687 T2: ΔΣ_OUTER ∝ Mgas500^0.90±0.21 vs the law's 0.47 (Newton 0.84),
binned by Mgas500 itself. In a flux-limited X-ray sample, low-Mgas clusters are preferentially up-scattered (Malmquist), which
STEEPENS a slope measured against the selection variable. Binning by an X-ray-independent proxy removes that.

## Data
CFG687's 318 clusters with per-cluster ΔΣ and law predictions (`cfg687_percluster.npz`, unchanged). Match to SDSS redMaPPer DR8
(λ ≥ 5 catalogue positions in `CFG668_count_magnification/redmapper_all_z01_06.tsv` plus a fresh VizieR pull of λ ≥ 5 down to z 0.05
if needed): nearest redMaPPer centre within 2' and |z_λ − z_X| < 0.04. Only clusters in the SDSS footprint can match (KiDS-N).

## Tests
- T1 instrumental-variable slope: bin MATCHED clusters in λ terciles; in each, stacked ΔΣ_OUTER (CFG687 weights) and the MEAN
  Mgas500 of the same clusters; s_IV = slope of log ΔΣ_OUTER vs log ⟨Mgas500⟩. Same procedure on the law's and Newton's predictions
  gives s_law,IV and s_N,IV. Errors: bootstrap over clusters (jackknife if ≥ 30 per tercile).
- T2 selection signature: ⟨Mgas500/λ^1.0⟩ in Mgas500 terciles of the matched set (Malmquist predicts the low-Mgas tercile inflated).
- Reported: A_OUTER per λ tercile; matched fraction; the CFG687 Mgas-binned slope on the matched subset (to compare like with like).
## Decision rules
- SELECTION ARTEFACT: |s_IV − s_law,IV| < 2σ and the matched-subset Mgas-binned slope reproduces the steep value.
- REAL √M FAILURE: |s_IV − s_law,IV| ≥ 2σ with s_IV within 2σ of s_N,IV.
- NOT DECIDED otherwise (e.g. too few matches: if < 60 matched clusters, the verdict is NOT DECIDED by construction).
MUTATE: shuffle λ among matched clusters → s_IV must lose its mass dependence (consistent with 0 within 2σ).
κ fitted; cold energy mass required; not theory closed.
