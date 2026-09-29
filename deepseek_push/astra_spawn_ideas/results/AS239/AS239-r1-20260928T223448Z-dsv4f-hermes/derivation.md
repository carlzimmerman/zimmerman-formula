# AS239 — Tensor propagation through an inhomogeneous carrier region (Tier-0b)

**Run:** `AS239-r1-20260928T223448Z-dsv4f-hermes`
**Cell:** CA5-GNC-R physical-metric branch of `FINAL_ACTION.md`
(sha `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`), occupied branch of AS238/AS240.
**Task sha256 (pinned and verified):** `154a242ce3ccba4b8189ee7bd80a91efb05e5d8798b745d4c3f0536ed163347d`

---

## 1. Pinned action, conventions, and the target (seed step 1)

Action branch: CA5-GNC-R physical-metric branch (= CA4-GNC equation (4) of the pinned
action) with the AS238 occupied conventions used verbatim:

- `M = M_P^2 = 1/(8π G_bare)`,  `Λ = 0`,
- `3 M H^2 = T + V + V0` (occupation), `M Ḡ = -T`, `ρ_d = T + V + V0`, `P_d = T - V - V0 ≡ L_d` (carrier Lagrangian density),
- carriers couple minimally to the **physical metric** `g` (`S_b[g]`), photons on `g`.

Q, RAR, historical EXP and MU2 laws are not used anywhere in this derivation; the
operative filtered-MONO thirteen-item target is only referenced through its causality
criterion **B** (signal speed = physical light cone) in the closure implication below.

**Background (declared domain).** One slowly varying weak carrier overdensity,
physical metric in the adapted foliation (zero shift),

```
ds^2 = -N(x)^2 dt^2 + b(x)^2 (dx^2 + dy^2 + dz^2),
z = z(x),  t_c = e^z bounded positive (samples 1.3, 1.0, 0.7),
static carrier: K_d = 0, W_d = W_d(x), P_d(x) = -e^{-z} W_d(x) < 0  (static clump),
heat gate closed: Y_h(x) < 0 pointwise -> f = G = G' = G'' = 0 at the background,
Z = Z(x), U = U(x) (projected source response), W_b = W_b(x), L = L(r,x) heat multiplier.
```

**Probe (independent fields, mode conditions).** Transverse-traceless (TT) plane
polarization along `x`:

```
γ_ij = q(t,x) e_ij ,  e_ij = diag(0,1,-1),  e^i_i = 0,  k^i e_ij = 0,  e_ij e^ij = 2,
q a real free field, x-mode: plane-wave / WKB ansatz q ~ α(x) exp(i(θ(x) - ω t)).
```

Because everything varies only with `x` and `e_xx = e_x· = e_·x = 0`, the transverse
gradients of `Z, U, W_b, φ` never contract against the probe: the Z/U sector, the
compensator sector and the heat sector couple to this probe only through isotropic
`q²`-mass terms whose coefficients vanish identically at the declared background
(verified zero for the x-propagating TT probe). The homogeneous sector on FRW was
established by AS238/AS240 (EOM, cone, amplitude law, Lean-verified transport) and is
used as the cross-check.

## 2. Leading WKB tensor principal block (seed step 2)

Test-field prescription (all other fields frozen at the background): the quadratic
tensor action is the covariant (M/8) form (textbook linearized-Einstein kinetic,
indices raised with `g`, measure `√-g = N b³`):

```
L_T^(2)  =  (M/8) N b^3 [ (-g^00) γ̇_ij γ̇^ij  -  h^kl ∂_k γ_ij ∂_l γ^ij ]
         =  A q̇² + C q'² + D q²        (E (q q') = 0 : e_xx = 0, x-only background)

A  =  M/(4 N b)          > 0   (no ghost;  [-g^00 γ̇γ̇] = 2 q̇²/(N²b⁴), ×(M/8)Nb³ = (M/4)q̇²/(Nb))
C  =  -M N/(4 b^3)       < 0   (no gradient instability)
D  =  D_EH + D_car
D_car = -N P_d/(2b)   (exact measure coupling: δ²√-g L_d = √-ḡ·(-¼)(γ_ij γ^ij) P_d
                      with γ_ij γ^ij = 2q²/b⁴)
D_EH = (M/2)√-ḡ·(-¼)γ_ijγ^ij·(R̄ - 2Λ) : the background-curvature measure piece.
```

`D_EH` is **not** modeled at leading order: on FRW it cancels against the intrinsic
LSW piece (Friedmann cancellation — the AS238/240 EOM `q̈ + 3H q̇ + (k/a)² q = 0`
has no mass term), and on the declared slowly varying background it is
`O((λ_T/L)²)`-small by the curvature scaling (section 5, bound; slab numerics set
it to zero at the declared order and re-verify insensitivity in the refraction run).

## 3. Local tensor cone and amplitude-vs-speed separation (seed step 3)

Eikonal from the principal symbol of the linearized EOM `2A q̈ + 2C q'' - 2D q = 0`
(WKB `O(ω²)`):

```
θ'(x) = ω · N(x)/b(x) · (1 + O(m_T²/ω²)),   ω² = -C/A θ'²  =>  c_T² ≡ -C/A = N²/b² .
```

**Local tensor cone = null cone of the physical metric g, coefficient by coefficient;
`t_c = e^z` does not enter the principal symbol** (checked: flat limit `N=b=1` gives
`c_T² = 1`; the cone identity is symbol-verified and Lean-certified).

**Amplitude transport (WKB O(ω)):** the leading transport equation

```
2 C θ' α' + (C θ'' + C' θ') α = 0      (static),   α = α₀ b(x)²/N(x)   [exact solution]
∂_t(2 A ω α²) + ∂_x(2(-C) θ' α²) = 0   (general current form)
2(-C) θ' α² = 2 (M/4) ω α₀²            (conserved static current)
```

- Static slab: amplitude changes with the carrier profile, speed does not:
  `α(x) = α₀ b(x)²/N(x)`; proper flux conserved.
- FRW limit (cross-check AS238/240): current with `A = M/4a, ω = k/a`
  `2Aωα² = M k α₀²/2` constant → `α ∝ a` in the metric-perturbation normalization,
  i.e. **strain normalization `q = α/a² ∝ a⁻¹` — identical invariant to the
  AS238/240 amplitude law `A ~ a⁻¹`**; numeric time-domain speed `0.9966` (residual
  ≤ 0.004 pre-set tolerance 0.01).

**Tensor mass (sub-leading, refractive):** `m_T² = -D/A = 2N² P_d/M`
(proper units `2 P_d/M_P²`); at finite frequency the carrier clump gives
`|δc/c| ~ |m_T²|/(2ω²)` — a low-frequency dispersion shift, **not** a cone change.
Static clump: `P_d < 0` ⇒ tachyonic window at comoving `k² < 2|W_d|/M`; the WKB
domain (`k² ≫ 2|W_d|/M`) is safe (see next_unresolved_implication).

## 4. Falsifiable negative controls (seed step 4)

**NC1 — photons compared on the carrier composite metric `g_d`:** if the photon
action were evaluated on `g_d = g + (1-e^{-2z}) n⊗n`
(`ds_d² = -N² e^{-2z} dt² + b² dx²`) instead of the physical `g`, one would extract
the false speed `(N/b) e^{-z}`:

| t_c | z = ln t_c | false speed² mismatch `e^{-2z} - 1` | false speed ratio |
|---|---|---|---|
| 1.3 | +0.2624 | **-0.4083 (≠ 0)** | 0.7692 |
| 1.0 | 0 | 0 | 1.0000 |
| 0.7 | -0.3567 | **+1.0408 (≠ 0)** | 1.4286 |

Numeric (slab, `t_c` up to 1.3): measured tensor speed vs `g`-cone residual
**4.4e-5** (passes), vs `g_d`-cone "mismatch" **0.30** (fires). **Verdict: the
`g_d` comparison is identified as a false speed mismatch** — it fires off for every
`t_c ≠ 1` even though the full action on `g` is propagation-invariant. Lean-certified:
`1/t_c² - 1 ≠ 0` for `t_c = 13/10, 7/10`, `= 0` for `t_c = 1`.

**NC2 — shear-squared diagnostic (the extraction is capable of failing):** with a
shear-modified kinetic `A → A + κ/8·N b³·(γ̇γ̇)` (a wrong-but-dimensionally-allowed
coefficient), the extracted speed shifts to `M/(M+κ) N²/b²` and the pure-Einstein
cone check fails: numeric fit to the shear law **4.0e-5**, pure-Einstein residual
**0.18** — the control would have detected the modified theory.

**Dimensional controls (capable of failing):** `[A q̇²] = M_P² L³ T⁻²` (action
density); `A > 0`, `C < 0` signs from the original (M/8) form; measure factor
`δ²√-g/√-g = -¼·tr(A²) = -¼γ²` for traceless TT is exact (`det(1+A) = 1 - tr A²/2`);
FRW/flat limits substituted back into the original quadratic action (speed 1,
friction/amplitude invariant matching AS238/240, mass `2P_d/M`).

## 5. Numeric validation (finitely many points; not a new law)

| check | measurement | residual / tolerance | status |
|---|---|---|---|
| C1 local cone (WKB, ω=40) | max \|c_meas/(N/b) − 1\| | 4.4e-5 (tol 1e-3) | PASS |
| C2 static amplitude | leading law `αN/b²` | 6.2e-2 (WKB order, tol 0.1) | PASS (leading order) |
| C2 exact current \|ψ\|²θ'·\|C\| | 4.4e-5 (tol 1e-3) | PASS |
| C3 mass refraction Δφ = ∫δκ dx | 1.6e-4 (tol 1e-3) | PASS |
| C4 NC1 false mismatch detection | g: 4.4e-5; g_d: 0.30 | mismatch > 1e-2, g < 1e-3 | PASS (fires) |
| C5 NC2 shear diagnostic | fit 4.0e-5; Ein-only 0.18 | fit < 1e-3, Ein > 1e-2 | PASS (fires) |
| C6 FRW time-domain | speed 0.9966; \|env/a\| residual 1.3e-2 | \|1-s\| < 1e-2 | PASS |
| C7 dimensioned footings | both r_M, λ_T/r_M = 2.5e-15 / 2.8e-15 | ≪ 1 | PASS |

Domain: slab `x ∈ [-7, 7]` masked, `Nx = 12001`, profiles `N = 1+0.06·G(x;2.5)`,
`b = 1-0.05·G`, `z = ln(1.3)·G`, `P_d = -0.02·G` (max |N'|/N ≈ 1.5e-2, κ ≈ 42); FRW
`t ∈ [1, 61]`, `k = 30`, `m² = -0.05`, `ω·dt ≤ 0.03`. Bounds actually enforced:
1 thread (OMP/OPENBLAS/MKL/VECLIB/NUMEXPR=1), wall 0.2 + 0.1 s, peak RSS with
`/usr/bin/time -l`: derive 57 MB, numeric 54 MB (declared ≤ 120 s, ≤ 512 MB — both
met), single-threaded.

## 6. Dimensional examples (both footings; κ = 1/2 adopted as input)

`a0 = (c/2)·√(G_bare·ρ_Λ)`: with κ = 1/2 the vacuum density is fixed by the
footing; the alternative footing is then a **different** ρ_Λ (they cannot share both
fixed ρ and fixed κ).

| | canonical | alternative |
|---|---|---|
| a0 (m/s²) | 9.3619e-11 | 1.1279e-10 |
| ρ_Λ = (2a0/c)²/G_bare (kg/m³) | 5.844e-27 | 8.483e-27 |
| r_M(1e12 M_sun) = √(G_bare M_b/a0) | 1.1906e21 m = 38.6 kpc | 1.0847e21 m = 35.2 kpc |
| v_flat = (G_bare M_b a0)^{1/4} (km/s) | 333.9 | 349.8 |
| λ_T(100 Hz)/r_M | 2.52e-15 | 2.76e-15 |

The result **c_T = c is dimensionless**: it applies identically to both footings;
only the dimensioned scales (r_M, ρ_Λ) shift. (Interpreted as changed κ with ρ fixed:
κ_eff = 1/2 · a0_alt/a0_can = 0.6024 — stated, not used.)

## 7. Classification and closure implication

**The local photon–tensor cone comparison is DERIVED on the declared domain.**
Classified per the completion criterion: *derived, scoped* — not promoted to complete
gravity closure (open gates remain, section 8). Closure implication for the common
action: on the CA5-GNC-R occupied physical-metric branch, the tensor principal
symbol equals the photon null cone of the physical metric `g` on the declared static
inhomogeneous carrier background (`c_T = c`), amplitude changes decouple from speed
changes, and the false `g_d` speed mismatch is identified by NC1 — i.e. the
thirteen-item causality criterion **B** is *consistent* with the tensor sector of the
single action on this domain; AS658's "fluctuation gate open" status is untouched by
this static-regime result.

## 8. Limitations, next unresolved implication, children

**Not established:** the full nonlinear/mixed system; the sector-coupling masses
beyond the zero-coefficient argument for the x-propagating TT probe; the
long-wavelength regime at the static clump (`k² ≲ 2|W_d|/M` where `m_T² = 2P_d/M < 0`
opens a tachyonic window — the coupled (γ, z, U, W_b) block must be rederived there,
the background-curvature mass `D_EH` is bounded `O((λ/L)²)` on the slab, not computed
to full order; two-dimensional/oblique propagation; time-dependent carrier.

**next_unresolved_implication:** the coupled reduction of the mixed (γ, z, U) block
at the static clump, where the scalar response mediated by the projected equation (7)
renormalizes `m_T² = 2P_d/M` and decides the sign/light-mass regime near the
tachyonic window `k² < 2|W_d|/M`.

**Child proposals (written for the orchestrator, not dispatched):**
- `AS239.C01` — coupled (γ,z,U) reduction at the clump: new target
  `m_T²_eff = (2/M)(P_d + (M/2)δz-response)`; controls: NC1 rerun on the coupled
  sector, FRW-limit mass; deps AS191, AS238, AS239.
- `AS239.C02` — refraction time-delay: `Δτ = ∫ m_T²/(2ω² N/b) dx` for a binary
  inspiral GW through a galaxy-scale clump at both footings; controls: C3-style
  wave-code residual for two polarizations; deps AS238, AS239.
- `AS239.C03` — extend domain: piecewise-smooth `b(x)` step (slab boundary), WKB
  matching conditions; controls: transmitted/reflected amplitude ratios vs
  current conservation; deps AS239, AS240.

## 9. Files

- `as239_derive.py` / `derive_raw.out` — symbolic derivation (A, C, D, cone,
  amplitude law, mass, NC1/NC2, dimension checks).
- `as239_numeric.py` / `numeric_raw.out` — wave-code checks C1–C7.
- `as239_cert.lean` — Lean 4 certificate (compiles; zero sorry; axioms ⊆
  {propext, Classical.choice, Quot.sound}).
- `as239_debug_flat.py`, `as239_debug_components.py` — failed-attempt artifacts
  (see result.json).
- `time_mem_derive.txt`, `time_mem_numeric.txt` — recorded bounds.
- `result.json` — contract result.