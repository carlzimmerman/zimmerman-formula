# CFG344: post-reionisation cold accretion onto reionisation-fossil satellites

**Frozen verdict (primary z_f = 8, z_inf = 2): RESOLVES, but narrowly and conditionally.** Read the caveats before quoting it.

- **Criteria:** `FROZEN_CRITERIA.md` (8cb772fc5), committed before any score.
- **Assumptions:** κ = ½ is FITTED. The cold component's mass is required; no DM particle is added. Nothing here says the theory is closed.

## Method
1. **Start mass:** M_cool(z_f), CFG343's atomic-cooling floor (Barkana & Loeb 2001 eq. 26), imported from its script.
2. **Growth:** the Correa+15 (MNRAS 450, 1521) median accretion history, M(z) = M₀(1+z)^α e^{βz}.
   - α and β come from f(M₀) = [S(M₀/q) − S(M₀)]^{−1/2} and dD/dz|₀.
   - σ(M) comes from colossus (planck18, Eisenstein & Hu 1998).
   - M₀ is solved so that M(z_f) = M_cool. Fossils then get M_c = M(z_inf).
3. **Fossils:** M_V > −7.7 satellites (CFG336's class split): 40 of 40 MW ultra-faints, 0 of 14 MW classicals, 4 of 14 M31 Collins, 7 of 34 M31 LVD, and 0 of 13 LV field dwarfs. Every other object keeps R = 1.
4. **Scoring:** CFG317's script is exec'd read-only up to its scans. Only the per-object M_c hook is replaced, keyed by committed M★ as in CFG317's RESCORE. Scoring uses rule S, V1 and V2, both footings and per-object R.
5. **ΛCDM-specific flags:**
   - (F1) The small-scale P(k) shape and σ₈ are collisionless-CDM's. **The resolution leans on CDM-like small-scale power**, which B shares only if its cold component clusters like CDM below the switch.
   - (F2) Correa's q(z̃) is calibrated on ΛCDM N-body trees.
   - (F3) The history is extrapolated to M₀ ~ 1e9 M☉ and z up to 10.
   - (F4) The formulas were transcribed from memory, so their M⊙ vs h⁻¹M⊙ units are unverified.
   - Only the linear growth D(z) is B-native (CFG324).

## Results (primary: z_f = 8, z_inf = 2)

**Accreted mass and R:**
- M_c(fossil) = 5.75e8 M☉ (M₀ = 1.28e9; α = 0.141, β = −0.477).
- Ultra-faint R_acc median 11,600 (log 4.06; 16-84%: 3.67-4.75).
- That is 0.3-0.4 dex above R_need (3.65-3.74). R_ΛCDM is 4.26 (CFG317), so these are close to ΛCDM-like masses.

**Offsets per population:**

| row | V1 can. | V1 alt | V2 can. | V2 alt |
|---|---|---|---|---|
| MW UFD (2e_law ≈ 0.172) | −0.024 (z −0.13) | −0.024 (z −0.13) | **−0.136** (z −0.30) | **−0.128** (z −0.29) |
| MW classical (z) | +0.32 | +0.09 | +0.32 | +0.09 |
| M31 Collins (z) | +0.77 | +0.55 | +0.74 | +0.54 |
| M31 LVD (z) | +0.70 | +0.45 | +0.59 | +0.40 |
| LV field (z) | −0.60 | −0.85 | −0.60 | −0.85 |

- The ultra-faint baseline at R = 1 was +0.325 canonical / +0.304 alt.
- SPARC clauses still hold, and SLUGGS is unchanged because R = 1 there by construction.

**Reionisation cap** (M(z_re) > 1e9 M☉, Gnedin 2000, PROVISIONAL): 0 of 40 violations at z_re = 6, 7 and 8 (M(7) = 6.1e7).

**Brackets** (reported, one at a time):

| bracket | M_c | V2 can. UFD | verdict |
|---|---|---|---|
| z_f 6 | 3.2e8 | −0.06 | RESOLVES |
| z_f 10 | 1.24e9 | −0.25 | NOT: V2 overshoots |
| z_inf 3 | 3.7e8 | −0.09 | RESOLVES |
| z_inf 1 | 8.8e8 | −0.21 | NOT: V2 overshoots |

The idea moves the ultra-faints from +0.32 to about 0, but **within its own bracket V2 overshoots past −2e**. The window that passes is narrow, about 0.4 dex in M_c.

## Disclosures
- **Run 1 had a plumbing bug.**
  - dD/dz|₀ came from a 1e-4 finite difference that hit colossus's interpolation noise: it gave −0.843 against the true −0.524, which made α negative.
  - That run scored primary **NOT**, from a V2 overshoot (−0.200), with M_c = 7.8e8.
  - The fix uses colossus's analytic derivative and adds check C0, against −Ω_m^0.55. **The fix flipped the verdict.**
  - No criterion was changed.
- **The MUTATE check FAILS, and the failure is kept.**
  - With z_inf = z_f, the verdict is NOT, as required. But the V1 canonical ultra-faint offset is +0.255, not within 0.05 of CFG343's +0.322.
  - Per-object R (median 770; low-M_b objects reach R > 4,000) moves the statistic more than CFG343's population-median approximation did. The other three readings are +0.28 / +0.32 / +0.30.
- **Infall times:** none are on disk (LVD has no such column; CFG327's orbits are not infall times), so the a-priori bracket was used.

## Controls

| check | result |
|---|---|
| C0 dD/dz | −0.5235 vs −0.5261 |
| C1 R = 1 reproduces CFG317 | exact (0.0) |
| C2 Correa dM/dt(1e12, z = 0) | 35.0 M☉/yr vs Fakhouri+10's 46.1 (×1.5 tolerance, PROVISIONAL); z½ = 1.20 |
| C3 inversion | 3.5e-13 |
| MUTATE | FAIL, see above |

## Lean
- `CFG344_certificate.lean` holds 24 decisive interval inequalities (ultra-faint |s| ≤ 2e on all four readings; the other rows have |z| < 2; MUTATE s > 2e).
- It uses Mathlib, has no sorry, and exits 0. The compile log is in `CFG344_certificate.out`.

## Run
```
python3 campaign_fresh_gravity/CFG344_postreion_cold_accretion/cfg344_accretion.py              # ~20 s
CFG344_MUTATE=1 python3 campaign_fresh_gravity/CFG344_postreion_cold_accretion/cfg344_accretion.py
python3 campaign_fresh_gravity/CFG344_postreion_cold_accretion/cfg344_lean_gen.py
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG344_postreion_cold_accretion/CFG344_certificate.lean
```
