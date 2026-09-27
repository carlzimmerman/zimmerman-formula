# Independent empirical-window replay

This calculation preserves an interior phenomenological witness and independently
reproduces a failed boundary cell. It tests the existing L352/L359 threshold
model, **not** the new varied action or global gate in this campaign.

The source DE2 JSON was being revised in another task. `DE2_snapshot.json` is the
frozen input; `snapshot_provenance.json` records its SHA-256. The replay evaluates
the unchanged L352 model/data prefix and does not rerun the unrelated 3D mock.
The script, snapshot, model and five data/covariance inputs are hash-pinned in
`run1/manifest.json`. All five finite checks passed.

| Cell | Effective KiDS threshold | Δχ² canonical | Δχ² alternate | Criterion, both ≤4 |
|---|---:|---:|---:|---|
| p=1, x0=2.5 | 3.2477265625 | −6.078914952 | −0.955628542 | passes |
| p=0.5, x0=3.395 | 3.8695414484 | 2.599062083 | 4.591406821 | fails |

Thus the older stored failed corner must not be counted as jointly passing.
For p=1, combining the supplied shear/forest thresholds with the conservative
sampled KiDS upper bound 3.86 gives conditional arithmetic windows

- vk=600: 2.004764979 ≤ x0 ≤ 2.971309257;
- vk=650: 1.680611025 ≤ x0 ≤ 2.971309257.

Both contain the explicitly replayed x0=2.5 cell. The shear redshift factor was
known to ±5e−7 from the source's rounded value; that interval was propagated in
the conservative direction. These intervals do not prove that every intervening
KiDS point passes, nor that a continuous joint likelihood has been fitted.

The constant-gate supplied forest floor 5.430614259 exceeds the sampled KiDS cap
3.86, reproducing the conditional constant-threshold conflict. Redshift-dependent
activation remains an empirical lead. There is no fresh shear, forest, growth,
CMB or nonlinear simulation in this replay. The positive witness must be rerun
only after the common covariant action fixes the gate, its normalization and its
backreaction; parameters from distinct actions cannot be pooled.
