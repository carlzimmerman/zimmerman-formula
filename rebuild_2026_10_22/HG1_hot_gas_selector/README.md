# HG1_hot_gas_selector — RESULT: UNDERPOWERED (model-free, footing-independent)

Frozen criteria 25bb540d4d (committed alone). Amendment A1 (`AMENDMENT_A1.md`): a K3 check-definition fix made before
any graded number. κ = ½ FITTED; nothing here says the data favour the framework or ΛCDM; not "theory closed".

**Question.** At matched σ, do KT2017 groups with an eRASS1 hot atmosphere sit further above the model-free matched-SPARC
disc reference (the matched-clumping rule) than groups without one, once their hot gas is counted?

## Result

| item | value |
|---|---|
| K1 (X-COP reproduced) | +0.4162 dex vs +0.416 ✓ |
| K2 (Galactic transform) | ✓ |
| K3 (g_bar distance-free, flags held fixed per A1) | 4.3e-10 ✓ |
| groups built (Nm ≥ 5, footprint, HRV ≥ 600) | 190: 14 X-BRIGHT, 176 X-FAINT |
| groups inside SPARC's g_bar support (≥ 8 reference galaxies) | **8** (4 BRIGHT, 4 FAINT) |
| shared σ bins | **none** |
| pre-flight power for D = +0.20 dex | **0.00** |
| D (primary) | undefined (no shared bin) |
| **class** | **UNDERPOWERED** |
| MUTATE (a) shuffle | 0.970 not HOT-TRACKS-sized ✓ |
| MUTATE (b) plant +0.30 | UNDERPOWERED, not HOT TRACKS ✗ (as frozen; follows from zero shared bins) |

**Why it is underpowered.** The groups' stars-only half-mass g_bar has a median of 10^−13.0 m/s² (5–95%: −13.7 to −11.9).
SPARC's disc segments rarely reach below ~10^−12, so 182 of 190 groups have no model-free disc reference. That is the
same wall the matched-clumping lane hit for 29 of 33 dwarfs.

**The four supported X-BRIGHT systems are clusters, not groups.** They have σ 163–800 km/s (σ 800 and 639 are cluster
scale). The supported X-FAINT groups have σ 11–156. Unstratified medians (+0.38 BRIGHT, n 4; +0.06 FAINT, n 4) compare
clusters with small groups. They are **not evidence** for or against hot-gas tracking, and are never quoted as such.

## What it means

The hot-gas selector is **not tested** at group scale by a model-free disc reference. That is a data-coverage result, not
a null. Ways to test it that remain open (each would need its own frozen criteria):

1. A low-acceleration reference that reaches 10^−13: isolated-disc weak lensing (KiDS, CFG829), the only data on the record
   there. The comparison is then not purely rotation-curve-model-free.
2. Groups with measured HI and X-ray at higher g_bar (inner radii): needs per-group profiles not on disk.
3. Cool-core vs non-cool-core clusters at matched mass, which tests "hot plasma" inside the cluster class (X-COP has 7 with
   stars, which is too few to grade).

Ellipticals were not rerun: cm05–cm07's result (the L_X signal is environment, not hot gas at galaxy scale) stands.

Files: `hg1_hot_gas_selector.py`, `.out`, `.json`, `_MUTATE.out`, `_MUTATE.json`. Run:
`python3 hg1_hot_gas_selector.py`; `MUTATE=1 python3 hg1_hot_gas_selector.py` (exits 1 only if the controls behave; here
it exits 0, disclosed above).
