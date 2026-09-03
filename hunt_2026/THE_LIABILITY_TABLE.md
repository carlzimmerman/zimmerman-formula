# The liability table: every failure of the framework in one currency (2026-09-03)

Produced by the unification workflow (`u01_*`–`u0N_*` scripts in this directory). For the first time the programme's
failures are on **one axis** instead of scattered across scripts. Each row's numbers come from a committed script's
`.out`, re-derived into a common currency: the **missing boost**, i.e. the factor by which the observation exceeds the
framework's zero-parameter prediction in *acceleration*, and the **acceleration** g_bar/a₀ where it is measured.

## The table, sorted by missing boost

| boost | g/a₀ | support | system |
|---|---|---|---|
| **44.7** | 0.001 | pressure | MW ultra-faint dwarfs, 31 satellites |
| 6.40 | 0.185 | rotation | HI warp onset, 16 WHISP edge-on discs |
| 6.19 | — | pressure | *(contrast row)* Coma UDGs with the EFE on |
| 6.00 | 0.049 | pressure | Pal 4 (outer-halo globular) |
| 5.32 | — | pressure | *(contrast row)* Local Group dwarfs with the EFE on |
| 4.63 | 0.730 | pressure | SLUGGS globular systems, log M* ≥ 11.3 |
| 4.60 | 0.010 | pressure | Pal 14 (outer-halo globular) |
| 3.57 | 0.012 | two-body | isolated major galaxy pairs, 2MRS |
| 3.45 | 0.361 | lensing | CLASH, 20 clusters, 14–600 kpc |
| 3.17 | 0.414 | lensing | Bullet BCG1, 300 kpc projected |
| 3.15 | 0.382 | lensing | Bullet BCG3, 300 kpc projected |
| 2.91 | 0.520 | pressure | X-COP cluster cores, 30–100 kpc |
| 2.76 | 0.259 | pressure | X-COP at 0.2 R500 |
| 2.63 | 0.004 | pressure | eRASS1 groups 10^12.5–13.5 at R500 |
| 2.56 | 0.059 | pressure | eRASS1 at fixed mass 1–3e14, z = 0.7–1.0 |
| 2.48 | 0.038 | rotation | six tidal dwarf galaxies |
| 2.24 | 0.041 | pressure | X-ray groups at R2500 |
| 2.17 | 0.113 | pressure | eRASS1 rich clusters 10^15–15.6 at R500 |
| 2.13 | 0.036 | pressure | eRASS1 clusters 10^14–14.5 at R500 |
| 2.09 | 0.175 | pressure | X-COP at 0.5 R500 |
| 1.93 | 0.110 | pressure | the a₀ ladder's cluster rung |
| 1.92 | 0.031 | pressure | eRASS1 at fixed mass 1–3e14, z < 0.15 |
| 1.69 | 0.800 | pressure | X-ray ellipticals, 5–70 kpc |
| 1.50 | 0.353 | rotation | DiskMass, 22 discs at 2.2 scale lengths |
| 1.48 | 0.111 | pressure | X-COP at 0.9 R500 |
| 1.45 | 0.023 | pressure | X-ray groups at R500 |
| 1.30 | 1.640 | pressure | SLUGGS globular systems, log M* < 11.3 |
| 1.30 | 1.390 | rotation | Milky Way vertical force K_z at 1.1 kpc |

28 of the 42 characterised rows carry a boost factor; the rest are slopes, nulls or non-measurements.

## What the table says, and it is not what a mis-normalised kernel would say

**1. The residual barely knows about acceleration.** Regressing the boost on g_bar/a₀ across 26 rows gives a slope of
**−0.206 with r = −0.53**. If the framework were simply wrong by a constant factor the slope would be zero; if a₀ were
mis-normalised the slope would be a definite, steep function set by the kernel. Neither is what is there. And the
X-COP radial run — 2.76, 2.09, 1.48 going from 0.2 to 0.9 R500 — is monotone in **radius**, which is why η(r) organises
by r/R500 (0.102 dex) better than by g_bar/a₀ (0.167 dex), winning **0 of 500** cluster bootstraps.

**2. It is a pressure-support table.** Twenty of 28 rows are pressure-supported, median boost 2.40; three are lensing,
median 3.17; four are rotation-supported, median 1.99, and those four are the mildest failures in the set. **The
framework's kernel is stated for a circular orbit, and the relation between it and a velocity dispersion is an
assumption, not a derivation.** That is the single most likely common cause and it is a theory question.

**3. The extremes are the informative rows, in both directions.** The Milky Way's ultra-faint dwarfs at ×44.7 are three
decades below a₀ in acceleration and one decade above everything else in boost — that row is either the deepest test in
the table or a measurement artefact, and it cannot be both. At the other end, the two mildest rows (×1.45 and ×1.48)
are both hydrostatic R500 measurements, and undoing a standard 20% hydrostatic bias multiplies them to 1.83, most of
the way to the weak-lensing-calibrated rows at the same radius.

**4. There is no single second acceleration scale.** CLASH prefers a₀ = 1.72e-9; X-COP over a wider radial range prefers
6.07e-10. A factor 2.8 apart. The best one-parameter description of all fifteen cluster rows is not a second scale at
all but **rescaling the first**: λ = 6.63 canonical / 5.46 alt, both landing on 6.19e-10, which is footing-independent
and therefore a property of the data. It fits eight of fifteen rows inside 0.10 dex — and it moves the deep-tail a₀ by
0.821 dex against a 0.10 bar, **22σ on that measurement's own bootstrap**. So what the cluster data ask for is a
**broken first constant**, which the galaxies forbid, not an extra one.

## Two zero-parameter corrections now owed to this table

Both were derived while the table was being built and **neither has been applied across the programme**:

* **The exact QUMOND flux theorem.** div g = div S with S = ν(|g_N|/a₀)g_N, so div(g − S) = 0 everywhere and the
  divergence theorem gives ⟨g_r⟩_sphere = ⟨S_r⟩_sphere **exactly, for any geometry, with no linearisation**. It implies
  the correct external-field-dominated coupling is ν(x_e)(1 + L_e) — **half the naive ν(x_e)G in the deep limit.**
* **The argument of ν.** In QUMOND, ν takes the **Newtonian** field sourced by the **actual matter**. Two committed
  scripts fed it a total dynamical field including a dark-matter halo, which is circular and inflates the prediction.

Together with two earlier catches — the naive prescription over-predicting NGC 1052-DF2 by a factor 2 against the
published calculation, and one script using a non-standard maximal-binding form — that is **four independent signs that
this repository's external-field treatment errs in exactly the direction that would manufacture these liabilities.**

Whether the pressure-supported block *is* one wrong prescription is now being computed. Until it reports, every
external-field-dependent row above should be read as **provisional**, and that includes the ~5σ external-field-slope
negative reported earlier the same day.
