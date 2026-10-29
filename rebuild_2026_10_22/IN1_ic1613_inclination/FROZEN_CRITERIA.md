# IN1_ic1613_inclination: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "lets work on the failures then".

**Why.** IC 1613 fails the law on two tracers:
- HO3: stellar σ, E −0.535, Z −6.75;
- RT1: HI rotation, E_rot −0.593, Z −7.90.

The literature check (2c6b17d683) found one assumption **common to both**, the **inclination**:
- **HI tracer.** V_rot ∝ 1/sin i. Oh+15 fixed i = 48° ± 0°, but their free tilted-ring fits scatter from 15° to 85°.
  Independent work argues i ≈ 20° and shows 3D BAROLO over-estimates low inclinations (i_true ≈ 15° possible).
- **Stellar-σ tracer.** The record reads σ_los with a **spherical, isotropic** estimator, ⟨v²⟩ = 3σ_los². IC 1613 is a
  rotating disc (MUSE 2024 detects stellar rotation). For a flattened disc seen near face-on, σ_los samples mainly σ_z,
  which is the smallest component, so 3σ_los² under-counts the kinetic energy.

If IC 1613 is near face-on, both tracers are biased low together.

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.
- **Literature values used here are PROVISIONAL** (web summaries).

## 1. Model (frozen)

**Baryons.** LITTLE THINGS (Oh+15 Table 2, as parsed by RT1): M★,SED = 2.88e7 M☉ and M_gas = 5.93e7 M☉. The gas
includes helium (×1.4, Oh's convention).

**(a) Stellar σ tracer** (r₁₂ = 4/3 r_h, r_h = 1439.78 pc and σ_los = 10.8 km/s from X1, with X51's b = 1 for
IC 1613):
- **Disc kinematics:** σ_φ = σ_R and σ_z = q_σ σ_R.
  - σ_los² = σ_R² (q_σ² cos² i + sin² i), neglecting the rotation term.
  - ⟨v²⟩ = σ_R² (2 + q_σ²) + v_rot,★², with v_rot,★ = UNGC vAmp 13 km/s as in FD1.
- **g_obs** = ⟨v²⟩ / r₁₂.
- **Baryons inside r₁₂:** ½ M★ + ½ M_gas, the record's half-mass convention for both components.
- **Grade:** E_σ(i) = log g_obs − log[ν(g_N/a₀) g_N], with s = HO3's 0.0792.
- **PRIMARY:** q_σ = 0.6. Variants: 0.4 and 0.8.

**(b) HI tracer:**
- V_rot(i) = 16.9 × sin 48° / sin i km/s at R_max = 2.71 kpc.
- M_b = M★ + M_gas inside R_max (RT1's convention).
- **Grade:** E_HI(i), with s = RT1's 0.075.

**Scan:** i from 10° to 60° in steps of 0.5°.

## 2. Verdict (frozen, canonical primary)

Let I_σ = {i : |Z_σ(i)| < 2} and I_HI = {i : |Z_HI(i)| < 2}.

| verdict | condition |
|---|---|
| **INCLINATION RESOLVES IC 1613** | I_σ ∩ I_HI is non-empty and lies inside [15°, 48°], the range in the literature |
| **INCLINATION RESOLVES ONLY IF i < 15°** | the intersection is non-empty but entirely below 15° |
| **INCLINATION DOES NOT RESOLVE IC 1613** | the intersection is empty |

**Reported:**
- I_σ, I_HI and their intersection for each q_σ and both footings;
- E at the literature values i = 48°, 39°, 20° and 15°.

**Disclosed:**
- An inclination is a nuisance parameter here. A RESOLVES verdict says the failure is **consistent with a data
  geometry**, not that the law is confirmed.
- An independent stellar-tracer inclination exists (MUSE 2024) but is not on disk. It would make this a real test.

## 3. Checks and twin

- **K0.** At i = 48° with the spherical estimator (⟨v²⟩ = 3σ_los²), X1's baryons and no rotation, E_σ reproduces HO3's
  −0.535 to 0.01.
- **K0b.** At i = 48° the HI tracer reproduces RT1's E_rot −0.593 to 0.001.
- **K1.** For q_σ = 1 (isotropic) the disc estimator gives ⟨v²⟩ = 3σ_los² at every i, to 1e-12.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`IN1_MUTATE=1`, separate outputs).** The disc estimator's sin²i and cos²i are swapped, so K1 still holds
  at q_σ = 1 but a K2 check fails. K2 requires E_σ(i) to rise as i falls for q_σ < 1, the face-on direction.

**Run:** `PYTHONHASHSEED=0 python3 -I in1_ic1613_inclination.py`
