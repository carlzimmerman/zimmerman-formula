# A77 — mutations

Ten dials. Each changes **one** input of `a77_checks.py` (a single key of the `BASE`
dict — the `rho_c_x2` dial moves the two representations of the one density together),
each is invoked as

```bash
A77_MUTATE=<name> python3 a77_checks.py          # equivalently --mutate <name>
```

each breaks at least one **named** check, and each run exits **1** (recorded below).
Baseline: `python3 a77_checks.py` → **40/40 PASS, exit 0, 1.3 s**, `a77.out`.

| # | name | the one input changed | exit | checks broken |
|---|---|---|---|---|
| 1 | `ct_light` | `ct_mode: "sigma" → "light"`, i.e. `c_T = c` (η = γ) instead of `c_T = σ_c` | **1** | K22, K27, K28, K29, K32b, K33 |
| 2 | `a0_thermal` | `a0 = 9.36e-11 → 8.620e-11 m/s²` (the A72 thermal footing) | **1** | K12, K13, K19, K22, K29, K33 |
| 3 | `rho_c_x2` | `ρ_c × 2` | **1** | K7, K8, K36 |
| 4 | `lstar_25` | `L* = 24 → 25 pc` | **1** | K7, K8, K19, K22, K29, K33, K36 |
| 5 | `gamma_x2` | `γ × 2` (the dial that `α = γ` follows) | **1** | K7, K8, K21, K22, K32, K33, K35, K36 |
| 6 | `soft_equipartition` | `eq_dof: 3 → 1` in `(1/2)m<v²> = (dof/2)k_BT` | **1** | K12, K16 |
| 7 | `no_pressure` | `pressure: True → False` (drop `−(c_s²k²/a²)δ` from the growth ODE) | **1** | K26, K28, K29 |
| 8 | `no_shear` | `shear: True → False` (drop the `F_ijF^ij` term from the quadratic action) | **1** | K1, K2, K5 |
| 9 | `eos_half` | `eos_factor: 1 → 0.5` (halve the Γ = 2 polytrope stiffness) | **1** | K6, K7, K8, K9, K10, K11, K35, K36 |
| 10 | `hlam_x3` | `hlam_factor: 1 → 3` (measured `H_Λ`, hence `T_dS` and `cH_Λ/2π`, tripled) | **1** | K12, K13, K14, K15, K16 |

26 of the 40 checks are broken by at least one dial. What the mutated runs return, i.e. that
they bite on the physics and not on a print statement:

| dial | the number that moves |
|---|---|
| `ct_light` | `γ/η = 1.000000`, `λ_C = 1.697056e+01 pc` (0.0170 kpc), `S(0.2) = 1.045e-35` |
| `a0_thermal` | `σ_c = 7.989775 km/s`, `3k_BT/m_P σ_c² = 3.001334`, `γ/η = 7.102768e-10`, `λ_C = 636.7697 kpc` |
| `rho_c_x2` | `c_s,el = 1.018748 m/s`, `c_s,el² = 1.154762e-17` (vs A16's 0.519081 m²/s², 0.720473 m/s) |
| `lstar_25` | `σ_c = 8.497344 km/s`, `λ_C = 623.6810 kpc`, `M_J,el = 2.391181e-02 M☉` |
| `gamma_x2` | `c_s,el = 1.018748 m/s`, `η = 1539.611347 eV⁻⁴`, `λ_C = 864.1977 kpc` |
| `soft_equipartition` | `3k_BT/m_P σ_c² = 0.921350`, implied `κ = 0.381181`, tension `0.09σ` (was 6.49σ) |
| `no_pressure` | `S(0.2) = 1.000000` at `c_s² = 1e-7` (A69's table: 0.9737), so `1−S = 0` |
| `no_shear` | `ω²(k) = K/η` with no `k²` term: the E-L slope `0.0` against `γ/η = 0.2529` |
| `eos_half` | `dp/dρ = 0.5 γρ`, `c_s,el = 0.509374 m/s`, `c_T²/c_s,el² = 2.671553e+08` |
| `hlam_x3` | `a0(cH_Λ/2π) = 2.587150e-10`, `κ = 3.430627`, tension `25.71σ` |

Why each dial is the right one:

* **`ct_light`** negates the closure's second half and keeps its first: it shows that the
  *identification* `c_T = σ_c` — not the equipartition — is what sets λ_C (4.6 decades) and
  the growth (35 decades).
* **`a0_thermal`** moves `a0` to the value at which per-dof equipartition is exact (A72). It is
  the cleanest demonstration that the candidate's numerical success *is* `a0 = cH_Λ/2π`:
  at that footing `3k_BT/m_P = 3.0013 σ_c²` and λ_C moves 611 → 637 kpc.
* **`rho_c_x2` / `gamma_x2`** are the two places γ enters — the elastic EOS (`c_s² = γρ_c`) and
  the transverse stiffness (`c_T² = γ/η`) — and they break different checks (K7/K8/K36 vs
  K21/K35), which is the lane's point: one γ feeds two speeds that are not the same speed.
* **`soft_equipartition`** isolates the dof count: it is the dial that separates the task's
  stated `3k_BT/m` from the per-dof `k_BT/m` that the numbers actually satisfy.
* **`no_shear`** removes the only term that produces a `k²` in the transverse dispersion, so the
  three checks that derive `c_T² = γ/η` (E-L, symbolic limit, finite-difference slope) must fail.
* **`eos_half`** halves the polytrope stiffness, which is the single input shared by
  `c_s,el² = γρ_c` and the `1/(ηρ_c)` ratio — it breaks the whole EOS family at once (K6–K11).
* **`hlam_x3`** is the one dial that moves the temperature: it breaks the three equipartition
  ratios and both `a0 = cH_Λ/2π` checks.

## Checks no dial can break, and why they are kept

Fourteen checks are **two-route identities**: both sides are the same algebraic object computed
twice (a symbolic derivation against its closed form, a root-find against its analytic solution,
a scaling law evaluated at two densities). No input dial can split them, because moving an input
moves both routes together; they fail only if one route is mis-coded, which is exactly what they
are for. They are listed here with the route each one guards:

| check | the two routes |
|---|---|
| K3, K4 | the gap `ω²(0) = K/η` from the E-L equation vs the `W`-series coefficient `d²W/dP² = K` |
| K17 | `m_P/T_dS` from the ratio vs the closed form `2π/(H_ΛL*)` |
| K18 | `L*(m_P = T_dS)` from `2π/H_Λ` vs `1/T_dS` |
| K20 | `η = γ/c_T²` vs `η = K/m_T²` |
| K24 | the bound margin in `c_T²` vs the same margin in `η` |
| K25 | the growth ODE at `c_s = 0` vs the exact ΛCDM integral `2.5Ω_m E(1)∫da/(aE)³` |
| K30, K31 | `λ_J` and `M_J` in the `2πc/√(4πGρ)` form vs the `c√(π/Gρ)` / `πλ³ρ/6` forms |
| K34 | the elastic `k_J` closed form vs a Brent root of `c_s²k² = 4πGρ` |
| K37, K38 | the density scalings `dlnλ_J/dlnρ = 0` and `−1/2`, evaluated at ρ and 200ρ |
| K39, K40 | `ρσ²/p_el` vs `(σ/c_s,el)²`; and the temperature implied by `c_s,el` by two routes |

Two further checks that were both unbreakable **and** redundant were deleted, and this is the
record of it:

* **the old K23** (`m_T/H0` from `m_T` and from `1/λ_C`) — a pure unit conversion of a number
  already printed in the HEADLINE block, with no independent content;
* **the old K41** (`λ_C(1/3)/λ_C(1) = √3`) — a ratio of two `σ_c`-scaled lengths, invariant under
  every dial; the band itself (1058.42 / 819.85 / 611.08 kpc) is still printed.

No other check was deleted.

## Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A77_eta_gamma
python3 a77_checks.py --json-out a77_results.json > a77.out          # 40/40, exit 0
for m in ct_light a0_thermal rho_c_x2 lstar_25 gamma_x2 \
         soft_equipartition no_pressure no_shear eos_half hlam_x3; do
  A77_MUTATE=$m python3 a77_checks.py > a77_MUTATE_$m.out; echo "$m exit=$?"
done
```

Recorded exit codes: all ten **1**; baseline **0**. The mutated outputs are
`a77_MUTATE_<name>.out` in this directory.
