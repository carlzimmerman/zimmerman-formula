# AS142 — Derive the carrier Legendre transform without freezing t_c

**Run:** `AS142_20260928T151335Z` (Tier-0 seed, group A06)
**Branch:** CA5-GNC-R (reciprocal carrier barrier) with inherited CA4-GNC host.
**Worker:** subagent runtime model `deepseek/deepseek-v4-flash-0731` (openrouter).
**Task sha256 (verified at start):** `a719f15d3cd7da819b57dd1a5b4723369b3cd0693512c28dd14c53446ebd2775`
**Source hashes (all match SOURCE_MANIFEST.json):**
- `real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md` = `290e5cbe83eca682fb68888375bb60f9230f677cbb3176ae6ec27557e777211d`
- `real_research/common_action_2026_09_26/action/PERSPECTIVE_VARIANT.md` = `36efa45459468d22c1f2553cbcd5d2a2349bef56c6df1e03a5b9fefb9806d78b`
- `real_research/breakthrough_review_2026_09_26/vacuum/BARRIER_PROOF.md` = `7bb45b3a4f2c43e0f6370a50515f48e1eb1178c8d5eea3084df13cadbb7b0dda`
- (host conventions additionally cross-checked against `real_research/common_action_2026_09_26/action/FINAL_ACTION.md`, hash `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`)

---

## 1. Pinned conventions and stated target

**Carrier action (CA5-GNC-R, ACTION.md R1).** The carrier sector of the common action (host: FINAL_ACTION (4)) is

```
L_d = t_c K_d - W_exc/t_c - V0 F(t_c),            F(t) = 1 + (t-1)^4/t^2 = 1 + (t + 1/t - 2)^2
t_c = 1 + Z - <Z>_h  >  0,   <Z>_h = (1/V_h) ∫_Σ sqrt(h) Z d³x
K_d = (1/2) Σ_A n(φ_A)^2,    W_exc = (1/2) Σ_A |D φ_A|^2 + Vmix
```

- `t_c` is the projected carrier lapse factor (`t_c = 1+z`, `z = Z - <Z>_h`); **it is a dynamical composite field and is NOT frozen** in this calculation.
- `V0 > 0` constant (vacuum floor); `F(t)` the reciprocal barrier; `F'(t)=2(t-1)³(t+1)/t³`; `F(1)=1`, `F'(1)=F''(1)=F'''(1)=0`.
- ADM decomposition with lapse `N`, shift `N^i`; the physical-time derivative is the normal derivative `n(φ_A)`, with `φ̇_A = N n(φ_A) + N^i ∂_i φ_A` (shift retained).
- The displayed mathematical target (seed):

```
Pi_A = sqrt(h) t_c n(phi_A),     H_R = N sqrt(h)[ (Σ_A p_A²/2 + W_exc)/t_c + V0 F(t_c) ]  plus shift term
p_A = Pi_A/sqrt(h)
```

**Boundary/mode conditions:** compact connected closed leaf `Σ` without boundary, smooth data, `N > 0`, `t_c > 0`, fixed carrier coordinates and spatial gradients; `W_exc ≥ 0` fixed (positive-square five-field potential, FINAL_ACTION (1)). All coefficients fixed symbolically; the result is an exact algebraic identity, no parameters fitted.

## 2. Velocity solve and explicit Legendre transform (step 2)

The carrier Lagrangian density (per unit spatial volume, inside `N sqrt(h) d³x`) is

```
L_d = t_c K_d - W_exc/t_c - V0 F(t_c),   K_d = (1/2)Σ_A n_A² ,   n_A := n(φ_A)
```

The momentum conjugate to `φ_A`:

```
Pi_A = ∂(N sqrt(h) L_d)/∂φ̇_A = N sqrt(h) t_c n_A · (1/N) = sqrt(h) t_c n_A        (matches display)
p_A := Pi_A/sqrt(h) = t_c n_A.
```

**Solve each velocity** (shift retained):

```
n_A = p_A / t_c ,      φ̇_A = N n_A + N^i ∂_i φ_A = N p_A/t_c + N^i ∂_i φ_A .
```

**Explicit `Pi·φ̇ − L`:** with `K_d = (1/2) Σ n_A² = (1/(2t_c²)) Σ p_A²`,

```
Σ_A Pi_A φ̇_A = sqrt(h) Σ_A p_A (N p_A/t_c + N^i ∂_i φ_A)
              = N sqrt(h) Σ_A p_A²/t_c + sqrt(h) Σ_A p_A N^i ∂_i φ_A

H = Σ_A Pi_A φ̇_A − N sqrt(h) L_d
  = N sqrt(h)[ Σ_A p_A²/t_c − t_c K_d + W_exc/t_c + V0 F(t_c) ] + sqrt(h) Σ_A p_A N^i ∂_i φ_A
  = N sqrt(h)[ Σ_A p_A²/t_c − Σ_A p_A²/(2 t_c) + W_exc/t_c + V0 F(t_c) ] + sqrt(h) Σ_A p_A N^i ∂_i φ_A
  = N sqrt(h)[ (Σ_A p_A²/2 + W_exc)/t_c + V0 F(t_c) ] + sqrt(h) Σ_A p_A N^i ∂_i φ_A .
```

The last line is **exactly the displayed `H_R` plus the shift (momentum-constraint) term**
`sqrt(h) Σ_A p_A N^i ∂_i φ_A = Σ_A Pi_A N^i ∂_i φ_A`, which matches the momentum-constraint coupling
`Σ_A π_A D_i φ_A` of FINAL_ACTION (14). Verified symbolically: residual of `H_Legendre − H_displayed` = `0`
(exact), and over 50 000 random samples the float residual is `4.5e-13` on magnitudes ~1e5 (machine epsilon level).

**Frozen-t_c comparison (why the seed title matters):** the canonical momentum is `Pi_A = sqrt(h) t_c n_A`
with `t_c` kept symbolic; if one froze `t_c = t̄` before transforming, the momentum would be solved as
`n_A = p_A/t̄` but the Z-dependence of the kinetic block would be lost: the Z-variation of `(Σp²/2+W)/t_c`
with `t_c = 1+Z−<Z>_h` would not exist. Freezing removes exactly the term the seed is required to derive
(see §3).

## 3. Canonical Z-stationarity vs velocity-form source (step 3)

At **fixed canonical data** (`p_A`, `W_exc` fixed) the Z-derivative of the carrier Hamiltonian density
(all factors per unit `N sqrt(h)`):

```
∂/∂t_c [ (Σ p_A²/2 + W_exc)/t_c + V0 F(t_c) ]|_{p fixed}
      = −(Σ p_A²/2 + W_exc)/t_c² + V0 F'(t_c)      =: σ_H .
```

Now substitute the Legendre image `Σ p_A²/2 = t_c² K_d`:

```
σ_H |_image = −K_d − W_exc/t_c² + V0 F'(t_c).
```

The **velocity-form source** (ACTION.md R3) is

```
σ_R = K_d + W_exc/t_c² − V0 F'(t_c)   ⟹   σ_H|_image = − σ_R,   i.e.  σ_H + σ_R = 0 (exact).
```

The full common-action Z-stationarity (fixed-data form, PERSPECTIVE_VARIANT P6 + BARRIER_PROOF B1,
and ACTION.md R4) is

```
2 M_P² c_N div_N(DZ − a + DU) + σ_R − <N σ_R>_h / N = 0 .
```

The carrier block contributes `σ_R − <Nσ_R>_h/N` via the projected variation `δt_c = δZ − <δZ>_h`
(exactly as in R4); the host gradient block supplies `2 M_P² c_N div_N(DZ−a+DU)`.
Consequently the canonical stationarity obtained by differentiating the *transformed* Hamiltonian
with respect to Z at fixed Π **equals the velocity-form source after substitution — with no residual**
(symbolic `0`; float max `2.3e-13` over 50 000 samples). This is the "consistent canonical carrier
energy and fixed-data auxiliary derivative" requested by the completion criterion.

### Subtleties kept explicit

- **Averaging measure:** the projector uses the h-volume mean `<·>_h = (1/V_h)∫ sqrt(h) (·) d³x` (not lapse-weighted), inherited from FINAL_ACTION §1. The projected source `σ_R − <Nσ_R>_h/N` has zero `N sqrt(h)`-integral, matching the zero-integral property required in FINAL_ACTION (7).
- **Signs:** `σ_H = −σ_R` is required and obtained; a sign error would produce `2V0F' − 2W/t²` type residuals, which the numeric check would catch at `~1e-1`; observed residual is at machine epsilon.
- **Dimensions:** `t_c` dimensionless; `p_A` has the dimension of a velocity-of-field (same as `n(φ_A)`); every term in the bracket is an energy density (in `c=1` action units; `V0` has energy-density dimension), and `H_R` has dimension action/(time·volume)−consistent energy. Footing-dependent examples are computed separately in §5; the identity itself is footing-independent (no `a0` appears), so it holds on both footings verbatim.

## 4. Negative control (step 4) — must be capable of failing

**Procedure under test:** after the transform, differentiate the Hamiltonian at **fixed velocities**
`n_A` instead of fixed momenta `p_A`. Substituting `p_A = t_c n_A` into `H_R` gives the
velocity-form image `N sqrt(h)[ t_c K_d + W_exc/t_c + V0 F(t_c) ]`; differentiating at fixed `n`:

```
σ|_{n fixed} = K_d − W_exc/t_c² + V0 F'(t_c).
```

The correct fixed-Π derivative at the *same phase point* is

```
σ_H|_image = −K_d − W_exc/t_c² + V0 F'(t_c).
```

**Mismatch:**

```
σ|_{n fixed} − σ_H|_image = 2 K_d = Σ_A n_A²  ≠ 0  for any moving carrier (any n_A ≠ 0).
```

- Symbolic residual of `(mismatch − 2K_d)`: **0** (exact).
- Numeric: over 50 000 random samples, `|(σ|_n − σ_H) − Σ n_A²| ≤ 2.6e-13` (machine epsilon), while `2K_d` itself ranges up to `|Σ n²| ~ 24` in the sample box — the mismatch is **detected at relative 1e-13**, never silently zero.
- The control **can fail**: if the transformed Hamiltonian had been re-differentiated in velocity variables (or if `t_c` had been frozen, killing the `Z`-dependence), the two derivatives would coincide in the frozen case (both zero in Z) or differ by the wrong amount; the residual test would then exceed tolerance and the construction would be flagged. It did not: the exact `2K_d` law holds.
- Static limit: at `K_d = 0` (inactive branch) the mismatch vanishes and both sources equal `−W/t_c² + V0F'`, the same value — consistent with the control going quiet exactly when there is no kinetic carrier excitation (physically correct degeneracy, not a failure).

## 5. Limiting cases and framework footings

**Inactive branch `t_c = 1` (z = 0):** `F(1)=1`, `F'(1)=0` ⇒

```
H_R → N sqrt(h)[ Σ p_A²/2 + W_exc + V0 ],   σ_R → K_d + W_exc ,   ρ_R → K_d + W_exc + V0 .
```

This matches PERSPECTIVE_VARIANT P8 (`ρ_{V0} = V0`, `P_{V0} = −V0` on the homogeneous inactive branch)
and the R-variant floor stress `−V0 g` at `t=1` (ACTION.md). All F checks pass symbolically (`F(1)=1`,
`F'(1)=F''(1)=F'''(1)=0`; `(F−1)t² = (t−1)⁴`; `ρ_R − t σ_R = V0(F + tF')`).

**Footings (kappa = 1/2 ADOPTED, both reported separately, never conflated):**

| quantity (SI) | canonical a0 | alternative a0 |
|---|---|---|
| a0 | 9.3619e-11 m/s² | 1.1279e-10 m/s² |
| ρ_Lambda = 4a0²/(G c²) | 5.8444e-27 kg/m³ | 8.4831e-27 kg/m³ |
| ε_Lambda = ρ c² | 5.2527e-10 J/m³ | 7.6242e-10 J/m³ |
| Λ_eff = 32π a0²/c⁴ | 1.0908e-52 m⁻² | 1.5833e-52 m⁻² |
| r_M = √(G M_b/a0), M_b = 1e11 M_sun | 3.7651e20 m (12.20 kpc) | 3.4303e20 m (11.12 kpc) |
| v_flat⁴ = G M_b a0, M_b = 1e11 M_sun | 1.8775e5 m/s | 1.9670e5 m/s |
| kappa implied if rho fixed at canonical value | 0.5 (definition) | 0.6024 |

The two footings share neither fixed density nor fixed kappa: with `kappa=1/2` fixed they imply different
`ρ_Lambda` (5.84e-27 vs 8.48e-27 kg/m³); with the canonical density fixed, the alternative a0 would imply
`kappa = 0.6024`. The carrier Legendre identity contains no `a0` and holds identically on both footings;
the `G_N`, `G_bare`, `G_cosmo` distinction does not enter the carrier block (the host gradient term uses
`m = M_P² c_N` with `M_P² = 1/(8π G_bare)`; high-k `G_N = G_bare/c_N` per FINAL_ACTION §5 — recorded, not
used for a claim).

## 6. Verification summary

| check | method | result |
|---|---|---|
| C1 Legendre identity incl. shift | sympy exact simplify | residual = 0 |
| C1 numeric (50k samples, t_c ∈ (0.2,3)) | float64 | max |Δ| = 4.5e-13 |
| C3 σ_H + σ_R = 0 (fixed Π vs velocity form) | sympy | residual = 0; numeric 2.3e-13 |
| C4 negative control: mismatch = Σ n_A² = 2K_d | sympy + numeric | exact 0; numeric 2.6e-13; mismatch detected at rel 1e-13 |
| C5 F(1),F'(1),F''(1),F'''(1), t=1 limiting H_R, ρ_R−tσ_R | sympy | all 0 / expected values |
| Lean certificate (7 theorems) | lake env lean, Lean 4.34.0-rc2 | exit 0, zero errors; axioms exactly {propext, Classical.choice, Quot.sound} |

**Bounds actually enforced:** CPU `ulimit -t 120` (wall 0.5–0.7 s used); `OMP_NUM_THREADS=1`
(single-threaded python/sympy); peak memory footprint 1 327 392 bytes ≈ 1.27 MB (measured via
`/usr/bin/time -l`); no memory cap was set — the 512 MB target was not needed (declared target
recorded, actual footprint far below).

## 7. Conclusion, scope and next implication

**Result (scoped claim):** on the CA5-GNC-R carrier action with inherited CA4-GNC host, for compact
closed leaves, `N>0`, `t_c>0`, fixed smooth carrier data, the Legendre transform *without freezing `t_c`*
is exact and equal to the displayed `H_R` plus the shift term; the canonical fixed-Π Z-derivative
reproduces the velocity-form source `σ_R` (exact, `σ_H + σ_R = 0`), and the negative control detects
exactly `2K_d` when a fixed-velocity differentiation is attempted. The fixed-data auxiliary derivative
is therefore consistent: the canonical stationarity is `2 M_P² c_N div_N(DZ−a+DU) + σ_R − <Nσ_R>_h/N = 0`,
identical to the velocity-form R4 equation after substitution.

**What this does NOT establish:** it is not gravity closure; it is a Tier-0 identity in the carrier
sector of one candidate action. It does not prove joint U/Z existence, evolution, the Dirac count,
PPN, filtered-MONO matching, or that `V0` or `a0` are derived (kappa = 1/2 remains an adopted input;
`V0` remains an input parameter of the action). The mean-projected equation is stated at the level of
the fixed-data functional (BARRIER_PROOF scope); propagation of its constants in the coupled
gravitational evolution remains open.

**Next unresolved implication:** the *joint* canonical U/Z problem — the carrier block is exactly
consistent here, but the seed does not treat the coupled functional
`∫ N {m|Dt−b|² + (Σp²/2+W)/t + V0F(t)}` as a saddle problem with both `U` and `Z` varied, which is
the prerequisite for the coupled constraint/evolution gate (BARRIER_PROOF: "the coupled U/Z problem
is a saddle problem, not the raw jointly convex Hamiltonian; its separate dual analysis is required").
Suggested follow-up: AS142.C01 — saddle-point analysis (dual function/strong duality) of the joint
U/Z fixed-data functional on a compact leaf, using the exact `σ_R` derived here as the Z-source.

## 8. Artifacts

- `compute_as142.py` (first version `compute_as142.py` has a shift-symbol bug and is retained as
  `failed_attempt`; `compute_as142_v2.py` is the executed one) — symbolic + numeric verification.
- `run_stdout.txt`, `raw_output.json` — raw outputs.
- `AS142_carrier_legendre.lean` — Lean 4 certificate (7 theorems), compiled with `lake env lean`
  from `fable_independent_2026/lean_2026` (no files written into the Lean project).
- `lean_compile.txt` — Lean axiom audit (`#print axioms`), all 7 theorems: exactly
  `[propext, Classical.choice, Quot.sound]`.
- `derivation.md`, `result.json` — this report and the contract result.
