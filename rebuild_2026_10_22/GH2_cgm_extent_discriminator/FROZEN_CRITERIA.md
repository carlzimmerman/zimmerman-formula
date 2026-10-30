# GH2_cgm_extent_discriminator: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** In X78_cgm_closure_regrade the lensing preference between the isolated law (L) and route E (H, fair-share
smooth-core halos) **reversed with the hot-CGM extent.**
- With F2's small hot gas, KiDS bins 3–4 gave L2H 95 vs SPARC-H 385.
- With Zhang+24's gas cut at 3 R_vir, they gave L 758 vs H 141.

GH1 showed the satellite line is method-limited, so lensing alone is the clean probe.

If the reversal holds on both lensing samples, then **the hot gas at 1–3 R_vir, a measurable quantity, is the
discriminator between the two theories.** This lane maps Δχ²(H − L) against the CGM cut k (in R_vir) and grades the
measured-only case.

## Models (both get identical baryons at every k; nothing fitted)

- **Baryons:** X78's model. Stars and cold gas as F2.
  - Hot CGM: Zhang's MW-mass profile (β 0.43, r_c 6 kpc, M_hot(<R_vir) = 1.84 M★, R_vir from their Table 1), cut at
    k R_vir.
  - **k = 0** means F2's own 0.5 M★ (r/100 kpc)³ hot gas instead.
- **(H):** X76/X78 fair share to the self-consistent r_ta.
- **(L):** the isolated law, M_eff = M_b ν(g_N/a₀).
- **k grid:** 0, 1, 1.5, 2, 3, 5.

## Samples and statistics (bins 3–4, log M★ 10.6–11.0, inside Zhang's MW-mass bin)

- **KiDS isolated lenses (B21; X53 harness):** sum of block-diagonal per-bin χ² over bins 3–4, all radii, with 2h
  (b fitted), as X78. z_ta = 0.285.
- **GAMA G09 centrals (GH1 data):** the 50–300 kpc points of bins 3–4 (10 points), with GH1's jackknife covariance
  (Hartlap). z_ta = 0.1797. Each host's model is stacked with its measured lens weight, as GH1.
- **Class at each k:** X53's rule on Δ = χ²_H − χ²_L: ≥ 9 LAW, ≤ −9 HALOS, else NOT DIAGNOSTIC.

## Verdict (frozen)

**PRIMARY: k = 1, i.e. measured gas only (Zhang detect the CGM to R_vir), on each sample and footing.** Report the class.

**Discriminator statement, also frozen:**
- **CGM EXTENT DECIDES:** on both samples, the class at k = 0 or 1 differs from the class at k = 3, and the k at which
  Δ crosses zero (k*, linear interpolation on the grid) agrees between samples within 1 grid step. Report k* per sample.
- **NOT A CLEAN DISCRIMINATOR:** otherwise; say which part fails.

**Reported:** all four bins at every k (bins 1–2 use the same CGM ratio, an extrapolation below Zhang's range), and the
absolute χ² of H and L.

## Checks

- **K1:** at k = 0, the KiDS numbers reproduce X78's machinery identities. H equals X76's fair-share per-bin χ²; L
  equals X53's L2H per-bin χ², bins 3–4, to 1e-6.
- **K2:** at k = 3, the KiDS bins 3–4 numbers reproduce X78's committed central_k3 (H2H 140.6, L2H 757.8) to 1e-6.
- **K3:** the G09 data vector equals GH1's committed ΔΣ (bins 3–4, 50–300 kpc) exactly.
- **MUTATE:** zeroing all hot gas (no CGM, no F2 hot) must lower both models' ΔΣ at 100 kpc.

κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
not theory closed; nothing here says the data favour the framework. One thread, nice 15. Zhang's M★/R_vir are taken
as published (disclosed, as in X77_cgm_budget).
