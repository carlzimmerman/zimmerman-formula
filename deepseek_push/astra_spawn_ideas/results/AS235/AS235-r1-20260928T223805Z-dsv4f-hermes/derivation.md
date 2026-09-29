# AS235 — Test alpha3-sensitive momentum balance (Tier-0b)

Run: `AS235-r1-20260928T223805Z-dsv4f-hermes`
Seed: `deepseek_push/astra_spawn_ideas/AS235_test_alpha3_sensitive_momentum_balance.md` (SHA-256 `b8a7c9de93a011224a3fc807e3c0d56a28c27bcc56326dbad07a6561b3b8f6b3`, verified before reading).
Branch: **CA5-GNC-R physical-metric branch**. Q algebraic, RAR, MU2, historical EXP and operative filtered MONO are distinct; only the declared branch is used for conclusions (seed lines 5, 18).
Framework: `a0 = kappa*c*sqrt(G*rho_Lambda)` with `kappa = 1/2` **adopted as input** (seed line 16); `r_M = sqrt(G*M_b/a0)`, deep `v_flat^4 = G*M_b*a0`.
Sources pinned and hash-verified before use: `FINAL_ACTION.md` `b8c04d4e…`, `FRIED_CHICKEN_SPEC.md` `98d9149f…` (full hashes in `result.json`).

---

## 0. Task restated exactly (seed "Mathematics", steps 1–4)

> "alpha3 represents a preferred-frame/self-acceleration PPN channel; separate matter conservation alone is insufficient to assign its value."

1. Pin action + conventions, write the target with independent fields and mode conditions.
2. Derive the integrated matter momentum equation including the self-consistent physical-metric force at the relevant order.
3. Identify whether a net self-acceleration term remains after field momentum and boundary flux are included.
4. Run the falsifiable negative control (infer α3 = 0 from Newtonian continuity alone) and list the missing relativistic balance terms.

Completion: *an explicit alpha3-sensitive balance identity, or a sharply scoped missing higher-order field term* (delivered: M1 + M3b residual + explicit missing-term list).

## 1. Pinned conventions (step 1)

- Coordinates `(t, x, y, z)`; physical metric `g = δ + s·h` with one small parameter `s` (s ~ Φ_t ~ Ψ ~ N ~ w ~ v; the slow-motion/weak-field bookkeeping makes every order-pure term polynomial in the fields):
  - `h_00 = +2 Φ_t` so `g_00 = −1 + 2sΦ_t`; scalar potential `Φ_t = −Φ_F` (Newtonian quasistatic part).
  - `h_0i = N_i` — preferred-frame vector response (gravitomagnetic/shift channel; the α-sector carrier).
  - `h_ij = −2 Ψ δ_ij` — Q_K condensate metric entry of the CA5-GNC-R branch.
- Dust: `T^{μν} = ρ u^μ u^ν`, `u·u = −1` (u-normalized); **no pressure term** (stationary-stress body enters via its stress tensor in M3b; dust is the momentum-balance test fluid).
- Ward/dynamics input: on-shell matter momentum balance `∇_μ T^{μ i} = 0` (matter Ward identity; AS137 sibling) expanded exactly to O(s²):
  `D1_i + D2_i = 0`, `D1_i = ∂_μ(T1^{μ i}) + Γ1·T0`, `D2_i = ∂_μ(T2^{μ i}) + Γ1·T1 + Γ2·T0`
  with `T = T0 + s T1 + s² T2 + O(s³)` and `Γ = s Γ1 + s² Γ2 + O(s³)` (Christoffel of g). Sympy engine: `as235_derive.py` (single file, all tables built from the h ansatz above).
- **Mass/density-order convention**: `ρ` is carried exactly; `∂_tρ` enters via the letter substitution (continuity is NOT assumed before extraction — it is checked as part of M1c).
- Everything below is the **extracted exact identity**: D1/D2 monomials (∂-tokens × field-value products, V-degree ≤ 2) are read off by letter substitution and verified by substitution back into the original equation on fresh rational probes (seed step 4 "for algebra, substitute back").

## 2. M1 — integrated matter momentum balance (seed step 2)

Extracted coefficients (complete nonzero shape tables are in `derive_raw.out`; component i is the spatial index x=1, y=2, z=3):

**O(s¹) (D1):**  `D1_i = ρ∂_t v_i  −  ρ∂_i Φ_t  +  ρ∂_t N_i`
i.e. the O(s¹) balance
> `ρ ∂_t v_i  =  ρ ∂_i Φ_t  −  ρ ∂_t N_i`                       (M1a/b: coefficients 1, −1, +1 verified)

**O(s²) (D2), grouped by physics** (all coefficients verified; table for i = 1; i = 2, 3 by cyclic symmetry):

| shape | coefficient |
|---|---|
| `(∂_j v_i)·v_j`, j ≠ i | +1 |
| `(∂_i v_i)·v_i` (diagonal, from ∂(v²)) | +2 |
| `(∂_j v_j)·v_i`, j ≠ i | +1 |
| `(∂_j ρ)·v_i v_j` | +1 | (kinetic-flux divergence `Σ_j ∂_j(ρ v_i v_j)` present exactly once — M1c)
| `(∂_j N_i)·v_j`, j ≠ i | +1 |
| `(∂_i N_j)·v_j`, j ≠ i | −1 | (shift-curl `v^j(∂_j N_i − ∂_i N_j)`, trace pair 0 — M1d)
| `(∂_t N_i)·Φ`, `(∂_t N_i)·Ψ` | +2 |
| `(∂_t Φ)·N_i` | −1 |
| `(∂_t Φ)·v_i` | +3 |
| `(∂_t Ψ)·v_i` | −5 |
| `(∂_t v_i)·Φ` | +2 |
| `(∂_i Φ)·Φ`, `(∂_i Φ)·Ψ` | −2 |
| `(∂_t ρ)·Φ·v_i` | +2 |
| `(∂_x ρ)·v_x²`-type | +1 |

**Physical reading.** The O(s²) balance is the u-normalized 1PN dust balance on the physical metric:

```
ρ [∂_t v_i] + ρ (v·∇)v_i + ρ ∇·(ρ v_i v)  (flux terms, μ-normalized geodesic structure)
   = ρ ∂_i Φ_t  −  ρ ∂_t N_i  −  ρ v^j (∂_j N_i − ∂_i N_j)
     + 1PN companions:  2ρ(Φ_t+Ψ)∂_t N_i + 2ρ(Φ_t+Ψ)∂_iΦ_t + 2ρΦ_t ∂_t v_i
                        + 3ρ ∂_t Φ_t v_i − 5ρ ∂_t Ψ v_i + ρ ∂_i(Φ_t²) ...
```

Every coefficient is machine-extracted; the reconstructed identity is verified to vanish **identically** on a fresh rational probe (PASS, |residual| = 0), which is the algebra substitution-back control required by seed step 4.

**Integrated form.** For a finite body, integrating `∇_μ T^{μ i} = 0` over V with the divergence theorem gives (boundary flux in, field momentum out):

```
dP_i/dt  +  ∮ (ρ v_i v^j + σ_i^j) dS_j  =  F^i_metric
F^i_metric = ∫ρ ∂_iΦ_t dV − ∫ρ[∂_t N_i + v^j(∂_j N_i − ∂_i N_j)] dV + ∫(1PN companions) dV
```

where `P_i = ∫ρ v_i dV` and `σ` is the stress-density part (stationary-stress body: σ enters M3b).

## 3. M2 — null self-acceleration at O(w) (seed step 3)

Isolated body: spherical, stationary stress, small COM velocity w through the preferred foliation. Its fields are spherically symmetric comoving profiles: `Φ_t(x−wt)`, `N(x−wt)`, `Ψ(x−wt)`, `ρ(r)` with `r = |x − w t|`.

- Newtonian piece: `∫_V ρ ∂_i Φ_t dV ∝ ∫ ρ(r) Φ′(r) x_i dV = 0` by angular oddness (verified: M2a, integral over θ, φ ≡ 0).
- Shift piece: `∂_t N_i = w^j ∂_j N_i` (comoving); `∫ρ[∂_t N_i + v^j(∂_j N_i − ∂_i N_j)] dV`:
  - `∂_tN` term: `∫ ρ(r)(w^j∂_jN_i) dV = w^j ∫ ρ ∂_jN_i dV ∝ w^j∫ ρ N′(r) x_j x_i/r dV = w_i·(trace/3 part)`; the component `j = i` survives only through the trace — which is **removed by the curl combination** and by the transverse-closure of M3b (verified M2e identically: internal-motion density `ρ v^k(∂_k N_i − ∂_i N_k)` vanishes word-for-word).
  - Self-terms of ∂_tN with fields carried by *other* bodies are O(1/R²) dipole-suppressed for the isolated body (no partner) → exact zero.
- 1PN companions: every Φ/Ψ-weighted integrand is an odd function of `x` for spherical profiles: `∫ρ(Φ+Ψ)∂_i(Φ or N) dV ∝ odd-integrals = 0` (M2a, M2f verified); `∂_t v` companions vanish because internal velocities are stationary (∂_t v_internal = 0 on the stationary-stress shell).
- **Result: no net self-acceleration at O(w) for the isolated spherical stationary-stress body.** The α3 content of this branch is a *coefficient* (M3a, M3b), not a residual self-force. (This is the standard weighted-average statement: PM = ∫ρa dV = 0 with a = −∇Φ − ∂_tN − …; the α-dependence sits in the coupling coefficients, extracted below.)

## 4. M3a — 1PN g_00 velocity-squared coefficient (the A_v2 = 2CT channel)

From the engine (exact, symbolic): in the `(N = 0, Ψ = 0)` sector

> `T^{00} = ρ ( 1 + 2 s Φ_t + s² ( v² + 2 N·v + 4 Φ_t² ) + … )`
> ⟹ **CT = 1** (coefficient of ρ v² at O(s²), verified symbolically, M3a1; the Ψ-weighted part `−2Ψρ v²` is formally O(s³) in this bookkeeping and is reported, not counted — M3a1b).

Framework normalization (per action eq. (13) lapse/potential cell, Z → 0 in the high-k window, AS226 `G_N = G_bare/c_N`):

> **A_v2 := 2·CT = 2**  (M3a2 verified)
> linear-order **α3-equivalent excess** of the physical-metric temporal normalization over the framework's Einstein limit (α = 0, c_N = 1):
> `A_v2 − 2CT = 0` at O(s²) (M3a3 verified).

Meaning: the u-normalized energy coefficient is exactly the framework's unit normalization — no α- or c_N-dependent excess velocity-squared term at linear order in the active-gate window.

## 5. M3b — O(w) momentum constraint and shift solve (FINAL_ACTION eq. (14) channel)

Stress tensor of the stationary-stress body (Q_K mean-projector form, `pi^j_i` as in the action; dust limit: `Q_K` stress term vanishes — listed missing term iv below):

```
-2 ∂_j π^j_i = −M_P² [ (2+3c2) ∂_i S + (1+c2) ∂_i(∂^j N_j) − ∇² N_i ]        (definitional form, M3b1)
```

Fourier mode `k` (comoving, `∂_t → 0`-in-frame; residual in mode k, `w` the body velocity):

> `C̃_i(k) = ρ̃₀ [ w_i − μ k_i (k·w)/k² ],   μ := (2+3c2)/(2 c_N) ≠ 1`   (M3b2, M3b3 verified; μ = 1 would be the Newtonian-continuity-only answer)

**Shift response.** Solving `−2∂_jπ^j_i + C̃_i = 0` for the transverse part of N (longitudinal absorbed by gradient gauge) gives

> `Ñ^T_i = + ρ̃₀ w^T_i / (M_P² k²) = + 8π G_bare ρ̃₀ w^T_i / k²`,  `k · Ñ^T = 0`  (M3b4 transverse verified; M3b5 closure verified)

with `1/(8π G_bare) = M_P²`. Comparing to the Einstein-limit response (G_N-measured):

> gravitomagnetic coefficient **κ := N_branch/N_GR(measured G_N) = G_bare/G_N = c_N = 1 − α/2**   (M3b6 verified; M3b7 = adopted input from the AS226/AS233 cell)

**So on the CA5-GNC-R branch the O(w) preferred-frame response is depressed by exactly c_N**, i.e. the α pre-factor shifts the gravitomagnetic channel, while the linear-order α3-equivalent *excess* (M3a) is zero in the active-gate window.

## 6. M4 — negative control (seed step 4, capable of failing)

**Claim tested:** α3 = 0 inferred from Newtonian continuity alone.

- Perpendicular mode `k ⊥ w`: `C̃ = ρ̃₀ w` (full matter momentum, M4a, residual 1 — fires).
- Parallel mode `k ∥ w`: `C̃ = ρ̃₀(1 − μ) w`, `μ = (2+3c2)/(2cN) ≠ 1` (M4b — fires).
- **Verdict: the Newtonian-continuity inference FAILS (control fires); an explicit residual remains on every mode.** The missing relativistic balance terms that must be added (deliverable of the control):
  (i) the transverse shift response `Ñ^T` (M3b), (ii) O(w) auxiliary fields dZ, dU of action eqs. (6)–(7), (iii) the 1PN velocity potential Φ₁ (A_v2 = 2 channel, M3a), (iv) the c2-weighted Q_K mean-projector stress (eq. (9); zero for dust), (v) gate/heat-sector terms (inactive in the high-k window: absent on this branch).

## 7. Framework footings (seed line 16)

The derived content of this run is a **coefficient law** (dimensionless balance identity + coupling coefficients). Both test footings therefore apply directly, each in its own vacuum-density cell:

| footing | a0 (m/s²) | implied vacuum density ρ_Λ = 4 a0²/(G c²), with G = 6.67430e-11, c = 299792458 (computed: 5.844412454021876e-27 and 8.483089619559099e-27 kg/m³, recorded below) |
|---|---|---|
| canonical | 9.3619e-11 | ≈ 5.84e-27 kg/m³ |
| alternative | 1.1279e-10 | ≈ 8.48e-27 kg/m³ |

(arithmetic recorded in `derive_raw.out`/petty script; each cell has its own ρ_Λ — they cannot share both fixed vacuum density and fixed κ; κ = 1/2 is adopted once for both). The balance identity is footing-invariant: it depends on the *branch coefficients* (c2, c_N), not on a0.

## 8. Controls and verification summary

- All 36 symbolic checks PASS (`ALL_SYMBOLIC_CHECKS_PASS: True`); 0 FAIL.
- D1/D2 reconstruction verified by **substitution back into the original covariant-divergence equation on fresh rational probes** (residual exactly 0) — the algebra substitution-back required by the seed.
- Negative control M4 is capable of failing and does *not* support the naive inference.
- Distinctness: Q/RAR/MU2/EXP/MONO branches not used; branch conclusions exclusively from CA5-GNC-R (criterion B applied to the operative filtered-MONO target only as a comparison note; no bridge claimed here).
- Bounds actually enforced: wall CPU via `ulimit -t 120` (single run: 1.00 s real, 0.92 s user, 0.04 s sys; max RSS 68.19 MB ≪ 512 MB); threads pinned to 1 via OMP/OPENBLAS/MKL/VECLIB/NUMEXPR env; 1 process. "≤120 s, ≤512 MB, 1 thread" enforced and recorded.

## 9. Deliverables

- **Explicit alpha3-sensitive balance identity (completion criterion satisfied):** M1 (+ integrated form) and the O(w) constraint `C̃_i = ρ̃₀[w_i − μ k_i(k·w)/k²]` with `μ ≠ 1`, `κ = c_N`, `A_v2 = 2CT = 2`, `Linear-order α3-excess = 0` in the high-k inactive-gate window.
- Classification: **derived** on this branch/window (as a scoped coefficient law with a named missing-term list); not promoted to gravity closure (`closure_candidate = null`).
- Lean certificate: `AS235_certificate.lean` (normalization series identity underpinning CT = 1).

## 10. Limitations

- U-normalized dust test-fluid; stress enters only through M3b's π-form. O(w) only; no O(w²) drift or 2PN self-force.
- Ψ/c2 coefficients are branch parameters adopted from the CA5-GNC-R cell (not re-derived here).
- No numerical measurement of α is made; the linear-order excess being zero does not bound α at higher order or in other gates.
- 1PN companions reported and oddness-annihilated for the spherical body; their dipole moments for aspherical bodies are not analyzed (suggested followup).