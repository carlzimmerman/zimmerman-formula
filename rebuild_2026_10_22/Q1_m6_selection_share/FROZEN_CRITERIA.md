# Q1_m6_selection_share: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** What share q of the local galaxy stellar-mass inventory (and, bracketed, of stars + cold gas) sits in
galaxies that need M6, i.e. galaxies that must be cold-dark-energy-poor under the record's environment rule? M6N1 only
bracketed q (0.30 ungrouped marginal to 0.69 = all galaxies 1e9–1e11 M☉). This lane measures it on a real group
catalogue with 1/Vmax survey weights, then re-evaluates M6N1's verdict at the measured q with M6N1's own formula and
inputs.

κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 / alt 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating
w ≈ 0 field component, not matter and not a particle. No ΛCDM input: no Planck parameter, no ΛCDM halo mass, no
abundance matching, no group dynamical mass calibrated on ΛCDM mocks (G3C's MassA is NOT read). Not "theory closed".
No result here may be described as the data favouring the framework.

## 1. The predicate: which galaxies need M6 (derived from the record)

**Record rule (X62_environment_keyed_switch, hypothesis ENV; X58 machinery).** A system carries a route-E halo if it is a
satellite or lies above X43's crossover; every other system follows the law on its baryons with no halo. A system on the
law with no halo is a system that must be cold-dark-energy-poor, i.e. a system that needs M6 (M6N1 §1, X57 class M5;
V3S_FINAL_VERDICT §8: isolated galaxies leave no room for a captured cold component).

**Operational predicate (per galaxy, per footing):**

    needs_M6  ⇔  (galaxy is NOT a satellite)  AND  (log M_b,sys < log M_b,x[footing])

- **System.** A G3C v10 FoF group (GroupID > 0) or, for an ungrouped galaxy (GroupID = 0), the galaxy alone.
- **Satellite.** A grouped galaxy with RankIterCen ≠ 1 (not the iterative central). Satellites carry halos regardless of
  the host's mass (X62 applies the satellite key to MW and M31 satellites; the MW itself maps below the c_f = 4 crossover,
  so the satellite key is not tied to an above-crossover host).
- **Isolated / central.** An ungrouped galaxy, or the iterative central (RankIterCen = 1) of a group.
- **M_b,sys (primary).** Σ over the system's G3C members of M★ (native-h, §3). Stars only: a lower bound on the system's
  baryons.
- **Mass range.** All galaxies with log M★ ≥ 8.0 (native) and 0.01 ≤ z ≤ 0.10. There is no upper mass cut: massive
  centrals fall above the crossover by the predicate itself.

**Mapping the crossover to an observable (framework-native, no ΛCDM).** X58/X62 key the flag on M200, and assign M200 to
SPARC, group and lensing systems through EM1's R1 route-E relation, log₁₀M200 = a + b (log₁₀M_b − 10), fitted on SPARC
rotation curves with route-E dust halos. Inverting it:

    log M_b,x = 10 + (log M200,x − a) / b,   a = 11.18, b = 0.90

(EM1 `em1_emergent_results.json`, rows/A_c2b_refit/R1, the background X58 uses). No abundance matching enters. This
mapping is a FITTED relation whose own Υ leg FAILED in EM1, and EM1 R2 shows 0.51 dex of halo scatter about it; both are
carried as the mapping band (§4).

**Crossover (read at run time from X58's committed JSON `x58_x53copy_law_x48_results.json`, key crossover_logM):**

| role | canonical | alt | why |
|---|---|---|---|
| **PRIMARY: c_f = 4** | `canonical\|cf4` (12.0945) | `alt\|cf4` (12.4339) | The only crossover in the record at which the galaxies M6 exists for stay on the law: X58 lensing +22.5 / 0.0 at c_f = 4, against +432 / +452 at native c_f |
| variant NAT-X48 (X58 primary c_f) | `canonical\|x48` | `alt\|x48` | Native c_f, unconverged; puts lens galaxies on halos, which the lensing line rejects |
| variant NAT-A2 (X62 primary c_f) | from `X62_environment_keyed_switch/x62_x53copy_law_a2_results.json` `canonical\|x48` | `alt\|x48` | Same, X48 A2 nine-seed table |

No converged framework-native c_f exists (X48 unconverged; X58 §1). The crossover is therefore **bracketed**, not
derived. The verdict is graded at PRIMARY; the native variants are reported with their own (labelled) verdicts.

## 2. Data

All untracked under `_external_data/q1_gama/` (repo root), never committed.

| file | source | bytes | sha256 |
|---|---|---|---|
| G3CGalv10.csv | GAMA DR4 G3C v10 (copied from the existing CFG471 download, not re-downloaded) | 20,695,642 | 051950e193e447ebf8bf7a9458c3ffe4ea368596b8042732ee933fc95f6ad9f8 |
| G3CFoFGroupv10.csv | GAMA DR4 G3C v10 (same) | 5,099,088 | eb81594ad6994e3fb44d2ee7c2e4eac4a99e3c7c27750bbf620d9f103a5b96c7 |
| StellarMassesLambdarv20.fits | https://www.gama-survey.org/dr4/data/cat/StellarMasses/v20/StellarMassesLambdarv20.fits (downloaded 2026-10-27 with the owner's approval) | 87,474,240 | 731170b792f26470ce3d35dffe397979465a16251fe4958f1a6ab8d5c053ca7e |

**Sample.** G3CGal galaxies in G09/G12/G15 (RA 129–141, 174–186, 211.5–223.5), Rpetro ≤ 19.8, matched by CATAID to
Lambdar with nQ ≥ 3, SURVEY_CLASS ≥ 4, finite logmstar and zmax_19p8 > 0; 0.01 ≤ z ≤ 0.10. Group membership and
M_b,sys are computed on the full G3C catalogue (all members, any z, any mass) before the sample cut.

## 3. Measurement

- **Native masses.** M★,nat = 10^logmstar × (0.7 / h_nat)², h_nat = 0.6856427 (L1). The catalogue's H0 = 70 is undone,
  nothing else.
- **Weights.** w = 1/V_max, V_max = V_c(min(zmax_19p8, 0.10)) − V_c(0.01), with V_c from the comoving distance on the
  native L1 background (h 0.6856427, Ω_m 0.2976016, flat, constant dark-energy density, which CFG689 does not reject).
  The survey solid angle is common and cancels in q. Galaxies with zmax_19p8 ≤ 0.01 are dropped and counted.
- **q_star = Σ w M★ [needs_M6] / Σ w M★**, over the sample.
- **Tail below 1e8.** The fraction of the inventory below 1e8 M☉, t = 1 − `gsmf/mass_ranges/above_1e8/fraction_of_fitted_stellar_mass`
  (closure population run, sha256 0131d5da…6323, as in M6N1), is assigned bracketed: q_full ∈ [(1−t) q, (1−t) q + t].
- **Statistical error.** Delete-one jackknife over 15 RA strips (each field cut into 5 equal-RA strips, by the galaxy's
  own RA).
- **Selection systematics (each reported; σ_sys = quadrature of the half-differences from primary):**
  - SZ: z-split, q(0.01–0.06) vs q(0.06–0.10) (isolation depth falls with z; half the difference).
  - SF: fluxscale applied (M★ × fluxscale where 1 ≤ fluxscale ≤ 10, else unchanged).
  - SU: unseen group members, M_b,sys × 1.25 for grouped systems.
  - SG: cold gas in M_b,sys, M_b,sys × 1.3 for every system.
  - SC: Hubble-law distances (D = cz/H0) in place of the L1 background.
- **Reported, not in σ:** NAT-X48 and NAT-A2 crossovers; the mapping band (crossover ±0.5 dex in M200, EM1 R2 scatter);
  SAT-LOW (satellites of below-crossover systems also need M6); floor log M★ ≥ 8.5; the ungrouped-only share (compare
  Alpaslan+2015's 0.30); q per mass decade.
- **Stars + cold gas.** GAMA has no per-galaxy HI. Using the closure census split
  F_cold = F_star + F_gas (F_gas = F_cold_baseline − F_star), q_cold = (F_star q_star + F_gas q_gas)/F_cold with q_gas
  **bracketed** in [q_star, 1]: the lower edge assumes the needs-M6 galaxies hold at least their stellar share of cold gas
  (satellites and massive centrals are gas-poor; ASSUMPTION_LEDGER A6).

**Interval used for the verdict:** q_star,lo/hi = q_full edges ∓/± 2 σ_tot, σ_tot = √(σ_jk² + σ_sys²), clipped to [0, 1].
q_cold,lo = q_cold(q_star,lo, q_gas = q_star,lo); q_cold,hi = q_cold(q_star,hi, q_gas = 1).

## 4. Re-evaluating M6N1 (its formula, its inputs, from its committed JSON)

Read from `M6N1_minimum_patch_need/m6n1_need_results.json` (commit 3ab6a1bf44): x_min, eps_ref, F_allowed per footing
(0.835 / 0.977, 0.191 / 0.163, 0.06132 / 0.04895) and F_inv stellar / stars+cold gas (0.046987 / 0.059787).

F_need(q, ε) = x_min · q · F_inv / ε. Corners: (q_star,lo, q_star,hi) × stellar, (q_cold,lo, q_cold,hi) × stars+cold gas.
Verdict classes exactly as M6N1 §4:

| verdict | condition |
|---|---|
| **M6 OVER BUDGET EVEN AT FULL RETENTION** | F_need(ε = 1) > F_allowed at all four corners |
| **BUDGET BINDS AT RECORD RETENTION** | F_need(1) ≤ F_allowed at all four, F_need(ε_ref) > F_allowed at all four |
| **BUDGET DOES NOT BIND** | F_need(ε_ref) ≤ F_allowed at all four corners |
| **MIXED** | anything else; the flipping corners are named |

Also reported per footing: ε_crit at each corner, q_crit(ε_ref) = F_allowed ε_ref / (x_min F_inv) for each inventory,
and the verdict at each reported variant crossover (labelled; not the graded verdict). F_allowed remains X57's
provisional budget, not a measured forest limit.

## 5. Step 0 (stop rule) and checks

**S0 (exit 2 before any q if it fails):** the three data sha256s match; M6N1 JSON values reproduce the numbers in §4 to
3 decimals; X58 crossovers reproduce 12.0945 / 12.4339 to 4 decimals; EM1 R1 (a, b) = (11.18, 0.90); closure sha256
matches.

- **K1 match:** ≥ 95 % of G3C galaxies passing the RA/Rpetro/z cuts have a Lambdar match with nQ ≥ 3.
- **K2 GSMF shape:** the Vmax-weighted mass fraction above 1e9 relative to above 1e8 agrees with the closure GSMF's
  (0.9544 / 0.9848) within 0.05.
- **K3 partition:** needs + not-needs weighted mass = total to 1e-12 relative; every sample galaxy classified exactly once,
  per footing.
- **K4 predicate unit tests (per footing):** ungrouped 1e10 → needs; satellite 1e10 in a 2-member group → not; central of a
  system with Σ M★ = 1e12.5 → not; ungrouped 10^(log M_b,x + 0.1) → not; ungrouped 10^(log M_b,x − 0.1) → needs.
- **K5:** peak RSS < 1 GB.
- **Reported (not graded):** Vmax-weighted ρ★ over the 180 deg² against the closure ρ★ = 2.909e8 M☉ Mpc⁻³ (GAMA z < 0.1
  is known to be under-dense).

**MUTATE (`Q1_MUTATE=1`, separate outputs `*_MUTATE.*`):** m1 inverts the satellite key (satellites need M6, centrals
do not); m2 alters the expected Lambdar sha256. The twin must fail S0 and K4.

Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I q1_share.py`. Amendments only in `AMENDMENTS.md`, each
committed before the run it affects.
