# FINAL-19 (KAPPA_C) RESULT: the deep-field column does NOT derive kappa (2026-11-11)

TEST lane, quarantined. Adopts nothing, relabels nothing, not registered.
**kappa = 1/2 FITTED; not theory closed.** Footings graded separately, never pooled.
Criteria: `FROZEN_CRITERIA.md` @ commit `0eb6a338d5`, committed **alone** before any number.

---

## 1. The one-line answer

**No.** A static, self-gravitating cold halo carrying the law's own anisotropic stress can
sustain a column **6.0 ± 1.4** (canonical) / **7.3 ± 1.6** (alt) times larger than the universal
column `Sigma_c = a0/(2 pi G)` that halos actually have. The vacuum is not saturated; it is barely
used. Demanding saturation inverts to `kappa = sqrt(2 pi) = 2.5066`, which is **22.1 sigma**
(canonical) / **27.6 sigma** (alt) from the measured `kappa`. To make `kappa = 1/2` come out, the
vacuum's own energy density must be divided by **Einstein's 8 pi** before it can act as the
deployable anisotropic stress — and that factor is exactly the content of the identity the lane
was told not to assume. **`kappa = 1/2` stays FITTED.**

## 2. What was derived, and from what

| step | statement | status |
|---|---|---|
| (J2) | spherical Jeans operator with `Pi_tt = -Pi_rr`: `2/r` doubles; `r^4` is the integrating factor | Lean `jeans_beta2_term`, `jeans_integrating_factor` |
| (P) | `rho_h = (1/K)(g' + 2g/r)`, `K = 4 pi G` | Poisson; the halo gravitates normally (M5 (iii)) |
| (J) | with the law's `Pi_ij` and `rho_h`, the Jeans residual is **identically zero** on the law's own branch `g^2/(g+a0) = g_N` — at every `u`, not only asymptotically | **PASS** (numeric residual 1e-45 … 1e-39 in relative units; `sympy` returns exactly `0`) |
| (K6) | `Pi_rr = -Pi_tt` in the deep field; `(Pi_rr+Pi_tt)/|Pi_tt|` tracks `2u/3` (6.64e-3 at `100 r_M`, matching FINAL-7's quoted 6.6e-3) | **PASS** |
| (C1) | `|Pi|(r) = 2 pi G Sigma(r)^2`, `Sigma(r) = int_r^inf rho_h dr'` | **PASS** (deviation falls as `O(1/x)`: 3.4e-2 at `x=10`, 3.3e-3 at 100, 3.3e-4 at 1000 — the relation is exact in the deep-field limit) |
| (C2) | `Sigma_max = sqrt(Pi_max/(2 pi G))` | inversion of (C1) |

**The one physical input** (pre-registered, named, and the thing the verdict hangs on):
`Pi_vac = f * rho_Lambda c^2` with `f = 1` — the vacuum's energy density is the ceiling the
dominant energy condition allows. Everything else is algebra.

## 3. The numbers (SI; measured `a0` = 7.8105e-11 m/s^2, CFG493; Planck `H0`, `Omega_L`)

| quantity | canonical (`rho = rho_Lambda`) | alt (`rho = rho_crit`) |
|---|---|---|
| `rho` | 5.8450e-27 kg/m^3 | 8.5329e-27 kg/m^3 |
| `eps = rho c^2` | 5.2532e-10 Pa | 7.6689e-10 Pa |
| `Sigma_c = a0/(2 pi G)` | 0.186258 kg/m^2 = 89.17 Msun/pc^2 | same (a0 is footing-free) |
| `Sigma_vac = sqrt(f eps/(2 pi G))` | 1.119233 kg/m^2 = 535.80 Msun/pc^2 | 1.352306 kg/m^2 = 647.38 Msun/pc^2 |
| **R = Sigma_vac/Sigma_c** | **6.009 ± 1.363** | **7.260 ± 1.647** |
| is `R = 1`? | **FAIL, 3.68 sigma** | **FAIL, 3.80 sigma** |
| measured `kappa` (CFG493) | 0.4172 ± 0.0946 | 0.3452 ± 0.0783 |
| `kappa` forced by `R = 1` | `sqrt(2 pi)` = 2.506628 (exact) | same |
| pull | **22.1 sigma** | **27.6 sigma** |

Cross-checks: the record's own footing values reproduce `Sigma_c = 106.85 / 129.13 Msun/pc^2`
against the quoted `106.9 / 129.2` (rel < 1e-3), and the analytic `R = sqrt(2 pi f)/kappa`
reproduces the SI ratio to 1e-4.

## 4. Master formula (all of the lane in one line)

```
|Pi|(r) = 2 pi G Sigma(r)^2          (derived; exact on the deep-field branch)
Sigma_c = a0/(2 pi G)                (definition; the universal column)
=>  |Pi|_c = 2 pi G Sigma_c^2 = a0^2/(2 pi G) = 4 x [a0^2/(8 pi G)]
Pi_vac   = f rho_Lambda c^2          (PRE-REGISTERED input, f = 1)
a0^2     = kappa^2 G rho_Lambda c^2  (definition of kappa)
--------------------------------------------------------------------
R^2 = (Sigma_vac/Sigma_c)^2 = Pi_vac/|Pi|_c = 2 pi f / kappa^2
R = 1  <=>  kappa = sqrt(2 pi f)     (f = 1: kappa = 2.5066, NOT 1/2)
```

## 5. Which input would have to move

* **The named input:** `f = Pi_max/(rho_Lambda c^2)`. `kappa = 1/2` needs
  `f = kappa^2/(2 pi) = 1/(8 pi) = 0.0398`. Measured: `f = 0.0277 ± 0.0126` (canonical)
  — consistent with `1/(8 pi)` at **0.96 sigma**, and inconsistent with the DEC value `f = 1`.
* **In observables:** with `f = 1`, `R = 1` needs `a0` **6.01x larger** (+0.779 dex, 7.9 sigma_log)
  or `rho_Lambda` **36.1x smaller**. Both are excluded by the data.
* **The 8 pi is not derived by anything on the record.** It is Einstein's `8 pi`, the same factor
  `kappa_closure/k05` identified ("every pi in 32 pi is Einstein's 8 pi"), and the record's
  identity `a0^2/(8 pi G) = rho_Lambda c^2/(32 pi)` is **algebraically equivalent to
  `kappa^2 = 1/4`** (Lean: `identity_iff_kappa_half`). Taking it as an input is taking the
  conclusion as an input.

## 6. Gates

| gate | canonical | alt | verdict |
|---|---|---|---|
| G1 unit cross-check vs 106.9 / 129.2 | 106.85 / 129.13 | — | PASS |
| G0 measured kappa vs CFG493 | 0.41714 (rel −1.4e-4) | 0.34525 (rel +1.4e-4) | PASS |
| G2 column sustained (`R >= 1`) | 6.009 | 7.260 | **PASS** (no inconsistency) |
| G2b is `R = 1`? | 3.68 sigma | 3.80 sigma | **FAIL** |
| G3 `kappa_forced` vs measured | 22.1 sigma | 27.6 sigma | **FAIL** |
| G4 `kappa = 1/2` needs `f = 1/(8 pi)` | 0.0398 vs measured 0.0277 ± 0.0126 | — | PASS (as stated) |
| G5 min `R` over column conventions | 6.009 (slab: 12.018) | 7.260 (slab: 14.521) | PASS (robust) |

`FINAL-19 COMPLETE: 14/18 checks PASS.` — the four failures are the four pre-registered kills
(K1, K2, K5 × 2 footings). K3, K4, K6 hold.

## 7. Mutation arms (each bites)

| arm | what is changed | outcome |
|---|---|---|
| **M1** isotropic/kinetic `Pi_ij = J delta_ij` | signature gates: `Pi_tt/Pi_rr` → +1 (not −1); `sigma_r^2 = +v_inf^2/2 > 0` — the radial tension that forces a shear modulus is gone | **FAIL / FAIL** |
| **M2** the record's shortcut (assume `a0^2/8piG = rho c^2/32 pi`) | recovers `1/2` trivially; INDEPENDENCE gate fails (Lean: the assumption ⇔ `kappa^2 = 1/4`) | **FAIL** |
| **M3** Newtonian (`mu = 1`) | no phantom, `Pi = 0`, `Sigma_max = 0`, `kappa` undefined | **FAIL** |
| **M4** isotropic plane-parallel slab `|Pi| = (pi/2) G Sigma^2` | `R` doubles to 12.02 / 14.52; `R = 1` fails at 4.04 sigma | **FAIL** (verdict robust) |

Reported honestly: **J1b — the Jeans balance does NOT discriminate the anisotropy.** Both the
law's `Pi` and the isotropic `J delta_ij` satisfy (J) on the law's branch, because they differ by a
radial-radial stress `tau ∝ g_N ∝ r^-2`, which the spherical Jeans operator annihilates
(`sympy` returns exactly `0` for both residuals). The anisotropy is therefore taken from the
covariant theory, not from the equilibrium; that is why M1 is graded on the signature gates.

## 8. Lean certificate

`Fin19KappaColumn.lean` (symlinked here; the real file is
`fable_independent_2026/lean_2026/Fin19KappaColumn.lean`, compiled inside that Lake project):

```
cd fable_independent_2026/lean_2026 && lake env lean Fin19KappaColumn.lean
EXIT=0    errors: 0    warnings: 0    sorry (proof terms): 0    admit: 0
13 theorems; every #print axioms line reads [propext, Classical.choice, Quot.sound]
```
(build log: `Fin19KappaColumn_build4.out`; the two earlier rounds are recorded and their
failures fixed, not hidden — build1 leaked a `sorryAx` through an unclosed goal in
`identity_iff_kappa_half`, build2 and build3 had two "No goals to be solved" errors.)

| theorem | what it certifies |
|---|---|
| `jeans_beta2_term`, `jeans_integrating_factor` | the beta = 2 Jeans operator and its `r^4` integrating factor |
| `column_stress_identity` | `|Pi| = 2 pi G Sigma^2` on the deep-field branch |
| `column_stress_at_universal_column` | the universal column requires `a0^2/(2 pi G)` = 4 x the pressure scale |
| `master_ratio` | `kappa^2 Sigma_vac^2 = 2 pi f Sigma_c^2`, i.e. `R^2 = 2 pi f / kappa^2` |
| `saturation_forces_kappa` | `Sigma_c = Sigma_vac` ⟹ `kappa^2 = 2 pi f` (the inversion) |
| `identity_iff_kappa_half` | the record's `a0^2/8piG = rho c^2/32pi` ⇔ `kappa^2 = 1/4` (circularity arm M2) |
| `kappa_half_requires_eight_pi` | `kappa = 1/2` ⟺ `f = 1/(8 pi)` |
| `two_pi_pos`, `sqrt_two_pi_sq`, `two_pi_bracket` | `sqrt(2 pi)` is real, positive, and in (2.506, 2.507) |
| `half_is_not_forced` | `(1/2)^2 ≠ 2 pi` |

**Scope, stated in the file's header:** Lean certifies the algebra, not the physics. The
deep-field limit `J -> g^2/(2K)` (i.e. `Pi_rr = -Pi_tt`) is verified in the Python lane (sympy
series + the numeric table tracking `2u/3`), and `Pi_vac = f eps` with `f = 1` is a
pre-registered assumption, not a theorem..

## 9. What this does and does not change

* **Does not change:** the `a0` relation, `Sigma_c = a0/(2 pi G)` as the universal column, the
  anisotropic-stress reading, the ELA1/M5 solid requirement. `kappa = 1/2` stays the fitted value.
* **Does change:** the column route is now a *bound* (`kappa <= sqrt(2 pi f) = 2.5066`), not a
  derivation. The halo deploys `f = kappa^2/(2 pi) ≈ 2.8% ± 1.3%` of its DEC-allowed stress; it is
  nowhere near saturation, and nothing in the equilibrium forces it to be.
* **Consistent with:** `kappa_closure/k01–k05` (no mechanism derives `1/2`; the only coefficient
  not excluded is the horizon value `0.461`, 8.5% away) and with `CFG493` (measured
  `0.417 ± 0.095`, `1/2` at 0.8 sigma, "consistent but not discriminating").
