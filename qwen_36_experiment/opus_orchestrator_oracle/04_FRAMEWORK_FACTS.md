# 04 — FRAMEWORK FACTS (locked values and established results)

**Never invent a value listed here. Never contradict a result here without first re-running its script and
showing the number.** This file exists because the experiment folder has already produced four different a₀.

## Locked constants

| symbol | value | note |
|---|---|---|
| `G` | 6.67430e-11 m³/(kg·s²) | |
| `c` | 2.99792458e8 m/s | |
| `Λ` | 1.0908e-52 m⁻² | from Milgrom 1994's a_λ = c²√(Λ/3) = 5.419e-10 |
| `ρ_Λ` | 5.847e-27 kg/m³ | = Λc²/(8πG). **Ω_Λ·3H₀²/(8πG) is the same thing** — the DE mass density |
| `cH_Λ` | 5.4194e-10 m/s² | = c²√(Λ/3). **This is the reference for q_cross.** |
| `a₀` canonical | **9.3614e-11** m/s² | ρ_DE + cH_Λ footing |
| `a₀` ALT | **1.13e-10** m/s² | ρ_total + cH₀ footing; larger by 1/√Ω_Λ = 1.2082 |
| floor `k` | **4.6810e-11** m/s² | = a₀/2 canonical. **a₀ = 2k always.** |
| `Z` | **5.788810036466** | = 2√(8π/3). ⚠️ NOT the EOS lane's `Z = 0.7135` — different object |
| `2Z` | **11.577620072932** | = 4√(8π/3) = 8√(6π)/3 |
| `1/Z` | **0.172747074736** | = a₀/cH_Λ canonical |
| `t_dyn` | 1.6011e18 s | = 1/√(Gρ_Λ) |
| `a₀/c` | 3.1226e-19 s⁻¹ | memory time 1/(a₀/c) = **101.5 Gyr = 7.4× the age of the universe** |

## The exact law and the two forms

```
a₀-line   :  g_obs² = g_bar² + a₀·g_bar
identical :  g_bar  = √(g_obs² + k²) − k        with k = a₀/2
kernel    :  ν(y) = √(1+1/y),  y = g_bar/a₀     [Milgrom 1999 eqs 6–9]
```

## The crossover master formula — use this to price ANY inertia law

For `I = f(T) − f(T_GH)` with `T = √(a²+H²)/2π`:

```
q_cross = 2·c₁′ / f′(T_GH) = 2/r ,   r ≡ f′(T_GH)/c₁′ ,   c₁′ ≡ lim_{T→∞} f(T)/T
```

q_cross is invariant under `f → αf + b`, so **r is the only physical content of f.**

| proposal | q_cross = a₀/cH_Λ | required r |
|---|---|---|
| Milgrom 1999 (`f = T`) | 2 | 1 |
| Milgrom 2020 | 0.15915494 | **4π = 12.566371 exactly** |
| this framework, κ=½ | 0.17274707 | **2Z = 11.577620** |

⚠️ **NAME COLLISION.** This `q_cross` is *not* the NESS coupling `q` in tn14–tn26. Keep them separate.

Script: `real_research/reviews/mi_crossover_master_formula_2026.py` (14/14).

## Established results — do not contradict without re-running

1. **Relabelling theorem.** `Λ = 8πGρ_Λ/c²` identically ⇒ `Gρ_Λ` and `c²Λ` are one scale up to 8π ⇒ no
   combination of the two can select a coefficient or exclude cH_Λ. **Boundary: a SINGLE-scale derivation from
   ρ_Λ alone is NOT excluded**, and would exclude cH_Λ automatically (it cannot make the Friedmann 8π/3).
   → `mi_zeropoint_interference_audit_2026.py` (7/7), `mi_local_floor_target_2026.py` (6/6).
2. **ρ must be ρ_Λ, not ρ_local.** With local baryon density, a₀ is 1076× too large in the solar neighbourhood
   and varies by orders between galaxies. "Local" can only mean the *response* is local. → same scripts.
3. **No standard local rate gives ¼.** Seven candidates; closest is √(Gρ/4π) at 12.84% off — wider than the
   7.87% between the two published coefficients. No near miss.
4. **a₀(z) decides the floor, with no new mechanism.** Local response ⇒ a₀ ∝ √ρ_DE, exactly constant for
   w = −1. Horizon floor ⇒ a₀ ∝ cH₀E(z), rising **1.78 / 3.01 / 4.54×** at z = 1/2/3. **This is the sharpest
   live observational discriminant.**
5. **Deser–Levin is reproduced from a computed response.** On a circular dS worldline at zero rotation the
   Unruh–DeWitt response is *exactly* thermal at `√(a²+H²)/2π` to 1e-15…1e-17. The temperature Milgrom's
   balance posits is obtained, not assumed. → `mi_circular_dS_response_2026.py` (8/8).
6. **Rotation breaks KMS only at O((v/c)²).** Gap-spread of T_eff = 0.166 at v/c = 0.5, falling to
   **8.6e-07 at the galactic v/c ≈ 1e-3**, with spread/(v/c)² constant to 1.34. ⚠️ **If a mechanism needs O(1)
   KMS violation, orbital motion supplies about a millionth of it.** → same script.
7. **The temperature class does NOT close.** `q_cross = 2/r` with r free; an explicit smooth, monotone,
   asymptotically-linear f reaches q_cross = 1/Z exactly. But r is a free number, so it is a reparametrisation.
   → `mi_crossover_master_formula_2026.py` (14/14).
8. **ω_c is a FREE fifth constant.** The suppression verdict for a nonlocal kernel turns entirely on it: at
   ω_c = a₀/c the Milky Way in-phase gain is C = 1.1e-7, but at the committed window
   **ω_c = 1.78e-14 … 2.21e-14** the same formulae give C = 0.997 and no suppression at all.
   → `mi_kernel_axis_separation_omegac_2026.py`, `mi_auxfield_exact_circular_2026.py` (18/18).
9. **A kernel from varying a quadratic nonlocal action is TIME-SYMMETRIC**, hence has zero quadrature (no
   dissipation) — it sits exactly on the passivity boundary. Retarded kernels are *in-in* (CTP) objects, not
   in-out action objects. → `mi_auxfield_exact_circular_2026.py`.

## Published records

- `10.5281/zenodo.21782600` — Two Barriers to the MOND Acceleration Coefficient (v2 correction **pending**,
  not yet live; the live v1 contains two claims since withdrawn).
- `10.5281/zenodo.21792565` — What Can and Cannot Fix the MOND Acceleration Coefficient.

## Withdrawn — never re-assert

- that the dS–Unruh mechanism "cannot be made to yield a smaller" coefficient (it can; q_cross = 2/r),
- that the two MOND limits *jointly force* q_cross = 2 (five scale-free examples, not a theorem),
- that a quadrature torque obstructs circular orbits for any kernel (kernel-shape dependent; a time-symmetric
  kernel has zero quadrature with the gain unchanged),
- that `S(Ω) = 0` on an interval forces `K ∝ δ` (refuted by `K = b·J₀(bs)`),
- that 1/C landing inside 3.8e5–3.8e7 cross-validates two routes (same kinematic (c/v)² twice),
- that 2Z "carries √π that no normalisation supplies" (its √π *is* the Friedmann 8π/3's).
