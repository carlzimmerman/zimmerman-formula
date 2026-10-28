# SP2_sealed_basin_lensing: sealed. At fixed stellar mass, galaxies in a massive basin should lens *less* beyond about 0.1 Mpc than isolated ones

Criteria: `FROZEN_CRITERIA.md` (bfd2b9ac3a, committed alone, before any SP2 number). Machinery: SP1's code, copied
with the grid and the observable changed.

**Seal:** `sp2_predictions.json`, sha256 `75b5fcdb3a8c2857906601d975ebc7bf38d5dc2d5254f82ba838513d160f8b3d`
(`SEAL.md`). It is byte-reproducible.

κ = ½ FITTED. Not "theory closed". This is a prediction **for** future data; it makes no claim about current data.

## The prediction

Q_env = ΔΣ(central in a basin above T) / ΔΣ(isolated central), at the same M★:

| log M★ | Q_env at 0.1 / 0.3 / 0.5 / 1.0 Mpc (canonical) |
|---|---|
| 10.0 | 0.71 / 0.28 / 0.17 / 0.08 |
| 10.4 | 0.81 / 0.37 / 0.22 / 0.11 |
| 10.8 | 0.93 / 0.50 / 0.30 / 0.15 |
| 11.2 | 1.03 / 0.69 / 0.42 / 0.21 |

**S_env = 0.484 canonical, 0.442 alt** (mean Q_env at 0.3 Mpc over log M★ 10.5–11.0).

**The sign is counter-intuitive, and that is what makes it a sharp test.**
- The law's lensing signal from an isolated galaxy keeps growing with radius.
- A route-E cold dark energy halo is a cored halo truncated at R200, which is about 0.2 Mpc here.
- So the galaxy's *own* lensing profile beyond about 0.1 Mpc is predicted to be **weaker** for a basin member than for
  an isolated galaxy of the same M★.
- ΛCDM halo models predict the opposite trend for group centrals.

**Disclosed:**
- Q_env is the central's own profile. In a real group the neighbours' mass adds lensing, so the test needs an analysis
  that isolates the central's own term: inner radii, satellite masking, or a halo-model fit of the one-halo term.
- The falsifier is frozen in §2 of the criteria.

## Checks

- **K2 (SP1's law stack):** the law stack reproduces X53's χ² (160.70 / 127.60).
- **K2 (agreement with SP1):** at log M★ 11.5 the basin branch equals SP1's halo branch, to 1e-9.
- **K3:** peak RSS 0.23 GB.
- **K4:** |S_env − 1| ≥ 0.05.
- **MUTATE twin** (halo branch replaced by the law): S_env = 1.000, so K4 fails and the run exits 1.
