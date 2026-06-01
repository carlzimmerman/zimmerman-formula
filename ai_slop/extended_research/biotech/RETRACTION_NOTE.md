# Retraction note for bioscience colleagues

**The one sentence:**

> The proposed "Z² = 32π/3 ≈ 5.79 Å protein resonance" was an artifact of backbone
> stereochemistry rather than a real length scale — the Cα(i, i+2) distance it relied on
> is the trivial ~5.4–6.7 Å consequence of two ~3.8 Å Cα–Cα virtual bonds at the standard
> chain angle that is present in *every* polypeptide; our own PDB analysis placed 5.79 Å at
> **z = −0.59σ** (below background, i.e. not even a preferred distance); and the
> "falsification" script never loaded real structures — its reference distribution was a
> Gaussian (`np.random.normal`) hard-coded at 5.89 Å — so there was no biological signal,
> only a geometric inevitability mislabeled as a cosmological constant.

**Evidence (in this folder, now quarantined):**
- `project_protogonos/computational_abiogenesis/sqrt_z2_validator.py` → z = −0.59σ on 2,583 real PDB aromatic pairs.
- `project_protogonos/computational_abiogenesis/decoy_proteome_falsification.py:322` → reference is `np.random.normal(5.893, 0.31)`, never real proteins.
- `project_protogonos/computational_abiogenesis/EARTH_ABIOGENESIS_HONESTY_ASSESSMENT.md` → the author's own audit (the "25 million× catalysis" factor and "life is inevitable, Ω_Z = 1.0" result are conceded to be made-up and circular).
- Full systematic audit: `../../real_research/reviews/DATA_AUDIT.md`.

The docking/MD tooling (AutoDock Vina, OpenMM) is real and runs correctly, but carries no
Z²-specific content — the connection was post-hoc. No drug/peptide claim here should be
treated as validated.
