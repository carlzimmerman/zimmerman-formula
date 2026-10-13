# CFG721 FROZEN CRITERIA: which galaxy property carries the KiDS early-type lensing excess?

Date: 2026-10-13. Written and committed ALONE, before any CFG721 code or score. Block CFG720–729. Nothing below may be edited after
this commit.

Raw lensing only (owner's 10-10 rule); no ΛCDM ingredient; no law, κ or footing in any score. Not "theory closed". Nothing will be
phrased as "the data favour the framework".

## 0. What has been seen (stated before any choice below)

- CFG669: at matched near-IR (Ks) baryonic mass, early types carry ×1.9 the lensing of late types (+0.280 ± 0.083, Z 3.4); robust to
  isolation (CFG96: amplitude 0.97 ± 0.19 at |Δχ| < 20 Mpc); the old/young signal inside early types is not robust (CFG667, CFG669).
- In our lens table "early type" is a colour cut (TYP = 1 ⇔ u−r > 2.0, asserted in CFG585's head); no morphology or velocity dispersion
  is on disk for these lenses.
- B21's release has isolated-lens RAR stacks split by Sérsic index (n_2dphot < 2 / ≥ 2) and by colour (u−r < 2.5 / ≥ 2.5), each with a
  joint covariance across its two bins; the files' g_bar ranges were seen (15 bins, 1.38e-15 to 3.92e-12), no offset computed.
- **Author's expectation, before any score:** colour and Sérsic are correlated, so both splits will show an offset; which is larger is
  open. Part B may come out undecided.

## 1. Part A (B21 released stacks; structure vs colour at the same g_bar)

For each split X ∈ {Sérsic, colour}: g_obs = 4G·ESD/bias per bin (record loader); the per-g_bar-bin log-ratio ℓ_i = log10(ESD_2,i /
ESD_1,i) with its covariance propagated linearly from the split's joint 30 × 30 covariance (bias-corrected); use the bins with
g_bar ≤ 1e-12 m/s² where both ESDs are positive; Δ_X = GLS mean of ℓ_i (weights from that covariance).
- **COLOUR CARRIES IT** if Δ_colour − Δ_Sérsic ≥ 2σ_d; **STRUCTURE CARRIES IT** if Δ_Sérsic − Δ_colour ≥ 2σ_d;
  **BOTH / UNDECIDED** otherwise. σ_d = √(σ_c² + σ_s²) (the two splits' cross-covariance is not released; treated as independent,
  which is conservative for a difference of positively correlated quantities).
- Reported: each Δ_X with its Z. Stated limit: the splits have different purities and B21's own (optical) stellar masses.

## 2. Part B (own stacks at matched Ks baryonic mass; step vs continuous colour trend)

f30 lenses, both types (CFG585's head and CFG531's `esd_loo`, executed unedited), Ks baryonic masses as CFG669 (c_K global, per-type
f_cold). Six u−r sextiles over the whole f30 sample. Each sextile is re-weighted, per decile of log M_b,K, to the whole sample's M_b,K
distribution (weights WG, WW scaled). A_k = log10(W·ΔΣ_k / W·ΔΣ_all) over K9 (CFG700 weights), with the patch-jackknife covariance of
the six A_k.
- M_step: A_k = a + b·[median u−r of sextile k > 2.0]; M_slope: A_k = a + c·(median u−r of sextile k − 2.0). Both GLS with the
  jackknife covariance.
- **STEP PREFERRED** if χ²_slope − χ²_step ≥ 4; **CONTINUOUS PREFERRED** if ≤ −4; **UNDECIDED** otherwise. Reported: b, c with errors.

## 3. MUTATE (`CFG721_MUTATE=1 CFG721_M=M1|M2`, each exits 1 iff its tooth bites)

- M1 (Part A): bins 1 and 2 swapped → each Δ_X flips sign exactly (within 1e-9).
- M2 (Part B): u−r shuffled within each M_b,K decile → |b| < 2σ_b and |c| < 2σ_c.

## 4. Machine rules

Light: one process, `nice -n 10`; precomputed stacks; B21 tar extracted into a fresh temp directory and read with numpy.
