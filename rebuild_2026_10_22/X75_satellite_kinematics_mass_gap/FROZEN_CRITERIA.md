# X75_satellite_kinematics_mass_gap: FROZEN CRITERIA (committed alone, before any velocity is read)

**Question.** X53/X74: KiDS-1000 lensing wants route E's halos ~0.30–0.50 dex heavier in M200 than EM1's SPARC
relation gives at the same lens baryons. Is that a halo-mass problem, or a lens stellar-mass / lensing systematic? X53
named satellite kinematics as the independent test. This lane measures satellite line-of-sight velocity dispersions
around central galaxies in GAMA G09 (spectroscopic z, GKV stellar masses) and asks which M200 normalisation they
require.

**Feasibility, recorded before freezing (counts only, no velocities):**
- B21-style isolation (no neighbour with > 10 % of the host M★ within 3 Mpc and 2000 km/s): ~140 hosts and 9 pairs.
  Unusable.
- Centrals (most massive within 1 Mpc and 2000 km/s): ~11,000 hosts and ~6,000 pairs at 30–300 kpc.

So the sample is **centrals, not B21-isolated lenses**. Disclosed as the main sample difference.

## Data (on disk, no new fetch)

- **Redshifts:** `_external_data/cfg519_work/G3CGalv10.csv`, the GAMA-II spectroscopic main sample, its `Z` column, for
  hosts and satellites.
- **Stellar masses:** `_external_data/gama_dr4_gkv/gkv_stellarmass_g09.csv` (sha256 in its FETCH_LOG), joined by
  CATAID; hosts are in G09 only.
- **Mass convention:** GKV masses are taken as H0 = 70, Ω_m = 0.3. They are converted to native exactly as F2/X53 do:
  lm_nat = lm70 + 2 log10(0.70/h) + 2 log10(q_DA), with h = 0.679 and Ω_m 0.3085 (F2's native background).
- **Distances:** projected radii use the same native flat background.

## Selection (frozen)

- **Hosts:** G09, 0.05 ≤ z ≤ 0.25, GKV log M★ in the B21 bins [8.5, 10.3), [10.3, 10.6), [10.6, 10.8), [10.8, 11.0]
  (native).
  - A host is the most massive GKV galaxy within R < 1 Mpc and |Δv| < 2000 km/s.
  - It lies at least 1 Mpc from the G09 edge (RA 129–141, Dec −2 to 3, converted at the host's distance).
- **Satellites:** any G3C galaxy at 50 ≤ R ≤ 300 kpc and |Δv| < 2000 km/s, with Δv = c(z_s − z_h)/(1 + z_h).
  - A galaxy within 2000 km/s of two hosts is assigned to the nearer one in R.

## Measurement (frozen)

- **Per bin:** a maximum-likelihood fit of Gaussian(0, σ) plus a constant interloper floor over |Δv| < 2000 km/s, on
  pairs.
- **Velocity errors:** 50 km/s per galaxy, removed in quadrature (σ² − 2·50²).
- **Errors:** 1000 bootstrap resamples of hosts.
- **Statistics:**
  - **PRIMARY:** pair-weighted.
  - **Reported only:** host-weighted, with each host's pairs weighted 1/N_pairs.

## Models (no free parameter)

For each host, M(<r) on X53's grid comes from X53's committed machinery:
- **(H) route E:** X70/X73 smooth core (B_S, η×B1/B_S(1), c_f = 4), M200 from EM1's SPARC relation, truncated at R200,
  with F2 baryons. Burkert is reported only.
- **(L) law:** isolated AQUAL (μ = x/(1+x)), M_eff = M_b ν(g_N/a₀), with the same baryons.

**Prediction:**
- Isotropic Jeans (β = 0) with tracer density n ∝ r^−γ. γ comes from the bin's background-subtracted satellite surface
  density over 50–300 kpc: pairs with |Δv| < 500 minus the 1000–2000 km/s sideband scaled by width, fitted as
  Σ ∝ R^{1−γ}.
- σ_los(R) is projected, then averaged over the aperture with weight Σ_sat(R).
- The bin stack is σ² averaged over hosts, each weighted by its own pair count in |Δv| < 500 km/s.

**Footings:** canonical and alt, never pooled.

## Verdict (frozen)

- **Statistic:** Δ = the common shift in log M200 that makes (H) match the measured σ in all four bins jointly (χ² over
  the bins; bootstrap errors; grid −0.5 to +1.2 in steps of 0.01), with its 1σ range from Δχ² = 1.
- **The class:**
  - **KINEMATICS SIDE WITH SPARC** if |Δ| < 2σ_Δ and Δ < 0.30 − 2σ_Δ;
  - **KINEMATICS SIDE WITH LENSING** if Δ > 2σ_Δ and |Δ − 0.40| < 2σ_Δ + 0.10 (lensing range 0.30–0.50);
  - **KINEMATICS REQUIRE A DIFFERENT MASS** if Δ is more than 2σ_Δ outside both;
  - **NOT DECIDED** otherwise.
- **Reported:** χ² of (L) and of (H) at Δ = 0 over the four bins; per-bin Δ.

## Systematics, reported only

- Anisotropy β = −0.3 and +0.3 (constant);
- γ ± 0.5;
- aperture 50–200 kpc;
- host-weighted σ;
- the Burkert shape;
- the alt EM1 background (B relation).

## Checks

- **K1:** a synthetic Gaussian σ = 150 km/s plus a uniform floor is recovered within 3 %.
- **K2:** the Jeans projection reproduces the singular isothermal sphere σ_los = V_c/√2 within 1 % for γ = 2.
- **K3:** the halo mass at Δ = 0 reproduces X74's smooth M200 for a test lens, exactly.
- **MUTATE:** shuffle Δv across all pairs. The Gaussian amplitude must collapse, or σ must hit the floor of the fit.

κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
not theory closed; nothing here says the data favour the framework. One thread, nice 15.
