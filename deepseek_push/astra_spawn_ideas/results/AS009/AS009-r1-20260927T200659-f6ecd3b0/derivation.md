# AS009 — Surface-density dimensions and coefficient bookkeeping (audit seed)

**Run:** `AS009-r1-20260927T200659-f6ecd3b0`
**Worker:** deepseek-v4-flash-0731 (OpenRouter) — actual model identity; no DeepSeek inference from the folder name.
**Branch:** CORE scale identities; Q / RAR / MU2 / EXP / MONO remain labelled. No branch is silently identified.
**Date:** 2026-09-27. **Kind:** audit. **Priority:** P1. **Group:** A01.

---

## 0. Sources inspected and hashes

| source | SHA-256 (current bytes) | pinned in SOURCE_MANIFEST.json | status |
|---|---|---|---|
| `README.md` | `91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed` | same | match |
| `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` | `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f` | same | match |
| `campaign_fresh_gravity_astra/DERIVATIONS.md` | `8da8176e3daeaeeaf9e42edb1585f271c92a50c0d9fdd842aa10caee462fb889` | same | match |
| `STANDING.md` | `660462ebe8f98844c418e173a1dada90b9df3800c4d445fd5a0556eb9476bf63` | (contract read-order file) | match |
| `deepseek_push/astra_spawn_ideas/AS009_*.md` (this task) | `7c3141e63420d8201a0581426bf3aed2cb12862d88589da0673a1362324adc2f` | — | task_id hash |
| `FRAMEWORK_CONTRACT.md` | `ca696c7fe7cccbe21d754eff833a4c59df6dee962ea61f50f04b5d20d80dddf9` | — | contract |

Extra audit sources (not in the manifest; quoted as evidence, not scope): `deepseek_push/ZD07_halo_saturation.py` (the slab ceiling `Sigma_phi,tot < a0/(4 pi G)` and its coded footing `A0 = 1.2e-10`), `hy4_push/H037_H033_CORRECTED.py` (the corpus's own documented factor-2 correction a0/(πG) → a0/(2πG)), `hy4_push/H043_dimension_scan.py` (D-dimensional projected-density conventions), `STANDING.md` §§ 310–337 (MW vertical surface-density determinations).

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

### 1.1 Claim (as specified)

> `Sigma0 = a0/G` has units `kg/m^2`; `Sigma_pi = a0/(pi*G)`; the slab/disk ceilings of the corpus (e.g. `Sigma_phi,tot < a0/(4 pi G)`, ZD07) are conditional equilibrium targets whose coefficients must be derived, not filled in; the framework must be dimensionally consistent and give the same prediction in equivalent variables without adding independent fitted inputs; dimensional examples must carry the canonical and alternative a0 footings separately.

The audit delivers: **(i)** the dimensional theorem for the whole a0/G family; **(ii)** which geometry fixes which π and which 1/2; **(iii)** a branch audit of the ceiling premise `g_phi < a0/2`; **(iv)** the footing audit of ZD07's quoted 68.4 M☉/pc²; **(v)** the negative control (volume-density vs surface-density rejection).

### 1.2 Symbol dictionary (SI units)

| symbol | meaning | units |
|---|---|---|
| `a0` | vacuum acceleration scale | m s⁻² |
| `G` | Newton coupling (measured; G_N) | m³ kg⁻¹ s⁻² |
| `c` | speed of light | m s⁻¹ |
| `k_Lambda`, `rho_Lambda` | 4 a0²/(G c²); mass density of the vacuum | kg m⁻³ |
| `k` | `kappa = 1/2` **adopted input** (never derived here) | 1 |
| `r_M` | sqrt(G M_b/a0) — MOND radius | m |
| `C` | sqrt(G M_b a0) — deep force scale | m² s⁻² |
| `B` | baryonic radial acceleration g_N | m s⁻² |
| `y` | B/a0 | 1 |
| `g` | total radial acceleration | m s⁻² |
| `g_phi` | halo (phantom) part g − B | m s⁻² |
| `rho_ph` | phantom density C/(4πG r²) — **conditional deep-equilibrium input** | kg m⁻³ |
| `M_ph(r)` | enclosed phantom mass | kg |
| `Sigma_b / Sigma_phi` | surface-mass densities (columns) | kg m⁻² |
| `M_b` | baryonic mass | kg |

### 1.3 Assumptions and boundary conditions

1. **Inputs (adopted):** kappa = 1/2; a0 values 9.3619e-11 (canonical) and 1.1279e-10 (alternative) m/s² — separate footings, carried separately; G = 6.67430e-11 (SI), c = 299792458 m/s; CORE relations r_M = sqrt(G M_b/a0), C = sqrt(G M_b a0), v_flat⁴ = G M_b a0.
2. **Conditional equilibrium inputs/targets** (FRAMEWORK_CONTRACT §Mandatory scale): `rho_ph = C/(4 pi G r^2)`, `sigma^2 = C/2`, `P = sigma^2 rho_ph`. These are NOT derived dynamics; every consequence below is conditional on them (contract: equilibrium relations are inputs, not solutions of the time-dependent equations).
3. **Branch labelling:** Q (`g²=B²+a0B`), RAR (`nu=1/(1−exp(−√y))`), MU2, EXP (`mu=1−e^{−x}`), MONO (operative, filtered, criterion B). The ceiling statements are derived per-branch; nothing transfers between branches without a labelled bridge.
4. **Boundary conditions:** positive reals for all dimensionless witnesses; no observational fit requested or performed; the solar-circle anchor uses the committed MW values V_flat = 171.7 km/s, V_bar(R0) = 120 km/s, R0 = 8.2 kpc, quoted with their provenance (G03E barrel; ZD07).
5. **Geometry conventions that fix the coefficients** (§2) are the point of the audit, not hidden assumptions.

---

## 2. Which geometry fixes which coefficient (step 2 of the work order)

### 2.1 The 4π of the phantom density — spherical shells

Deep-MOND equilibrium target: `g = C/r` (deep law, `v_flat⁴ = G M_b a0` at the flat asymptote, with the RAR/MONO deep limit `g → B/nu ≈ sqrt(a0 B) = C/r` — see §4.1 for the expansion). The phantom is the Newtonian-equivalent enclosure:

```
G M_ph(r)/r^2 = g = C/r   =>   M_ph(r) = C r/G.
dM_ph/dr = C/G = 4 pi r^2 rho_ph(r)   =>   rho_ph(r) = C/(4 pi G r^2).
```

The 4π is **fixed by the spherical-shell area 4πr²** — this is a derived recast of the equilibrium input, not a new number. Residual of the shell-integral identity `∫ ρ_ph 4πr′² dr′ = C r/G`: **≤ 1.0e-08 relative** over [10⁻⁹ r_M, 10 r_M] in the first run; after adding the analytic singular-tip term (the 1/r² integrand's tip at r → 0), the residual over [10⁻¹² r_M, 10 r_M] is **≤ 1e-12** (checks B1, both footings in `AS009_audit_results.json`).

### 2.2 The π of the projected surface density — ambient convention

Projecting the phantom inside radius r onto the plane: `Sigma_proj(r) = M_ph(r)/(π r^2)`. The π is the **projected-disk convention** (area πr²). At r = r_M:

```
Sigma_proj(r_M) = M_b/(π r_M^2) = M_b · a0/(π G M_b) = a0/(π G)   [M_b cancels exactly]
```

This is the "universal" surface density of the corpus (H033/H043 `Sigma_pi = a0/(πG)`). The mass cancellation is pure bookkeeping at the chosen radius: at 2 r_M the same convention gives **exactly half** (B4). The universality is a *convention identity*, not a new law. It is **exact arithmetic given the equilibrium input** — checked to 1e-16 relative on both footings (B3).

### 2.3 The 2π of the slab/disk transition — plane-parallel Gauss law

For a plane-parallel stratum (density stratified in z only, any vertical profile), Gauss' law for the vertical field: `g_z = 2π G Sigma`, where Σ is the total column. This is the classical Milgrom critical surface density argument:

```
g_z = a0  at  Sigma_m := a0/(2 pi G)     (slab transition surface density)
```

The 2π here is **fixed by plane-parallel geometry** (the 4πG of the flux integral across the two faces of a slab box). This is a physical-derivation premise (requires div g = 4πGρ as a field law), so in the Lean certificate it is stated as an input; the **consequence** `Sigma_phi,tot = g_phi,z/(2πG) < a0/(4πG)` is derived in §3.

### 2.4 The 4π of the ZD07 slab ceiling — the derived double factor

ZD07 states `Sigma_phi,tot < a0/(4 pi G)` ("total phantom column of a disk"). Derivation from the audit's premises:

```
g_phi,z = 2 pi G Sigma_phi,tot        (plane-parallel Gauss, phantom column)
g_phi,z < a0/2                        (the ZD01 halo saturation ceiling — branch audit §3.3)
=>  Sigma_phi,tot < a0/(4 pi G) = (a0/(2 pi G))/2 = Sigma_m/2.
```

The 4π = **2π (slab Gauss) × 2 (the 1/2 ceiling)**. Both factors are now explicit; the 1/2 factor is **not** geometry but the branch's halo-field cap, and §3.3 shows that cap is Q-branch truth, RAR-branch false (peak 0.6476 a0), and MONO-branch false pointwise (logarithmic growth). **The slab ceiling is a conditional Q-branch statement; it does not transfer to the operative filtered-MONO target without a filtered-operator argument.**

### 2.5 What has no geometry: `Sigma0 = a0/G`

`Sigma0 = a0/G` (kg/m², check: [a0/G] = (m s⁻²)/(m³ kg⁻¹ s⁻²) = kg m⁻²) is the **raw bookkeeping unit** of the family: `Sigma0 = π Sigma_pi = 2π Sigma_m = 4π Sigma_quad`. It is not realized by any known geometry at this level; it is the basic column unit against which every ceiling is a rational multiple. If a source claims `Sigma0` itself is a physical ceiling, the π-free normalization is an unproved assumption (task: "If no geometry fixes π, leave it as an unproved normalization").

### 2.6 Dimensional consistency of the scale identity (principal test)

```
[a0] = [kappa] [c] sqrt([G][rho_Lambda])
     = 1 · (m s^-1) sqrt((m^3 kg^-1 s^-2)(kg m^-3))
     = (m s^-1)(s^-1) = m s^-2          ✓
rho_Lambda = 4 a0^2/(G c^2):  [a0^2/(G c^2)] = (m^2 s^-4)/(m^5 kg^-1 s^-4) = kg m^-3  ✓
```

Same prediction in equivalent variables: `C = a0 r_M` (since `(a0 r_M)² = a0² GM_b/a0 = GM_b a0 = C²`; positive roots), i.e. `r_M`, `C`, `v_flat`, `Sigma_*` are all bookkeeping re-expressions of the single adopted scale a0 and M_b — **no additional fitted input appears** in any surface-density member (each member is a rational multiple of a0/G). This remains true because kappa stays adopted; nothing here re-derives kappa (task constraint; §5.3).

---

## 3. The ceiling family on both footings (step 3: intermediate algebra, signs, units)

All members (kg/m² → M☉/pc² × `MSUN_PC2 = M_☉/pc² = 2.088341e-3 kg/m²`):

| quantity | canonical a0 = 9.3619e-11 | alternative a0 = 1.1279e-10 | ZD07 legacy a0 = 1.2e-10 (unregistered) | units |
|---|---|---|---|---|
| rho_Lambda | 5.84441e-27 | 8.48309e-27 | 9.60230e-27 | kg/m³ |
| **Sigma0 = a0/G** | 1.40268 (671.6 M☉/pc²) | 1.68992 (809.2) | 1.79794 (860.9) | kg/m² |
| **Sigma_pi = a0/(πG)** | 0.44649 (213.79) | 0.53792 (257.57) | 0.57230 (274.04) | kg/m² |
| **Sigma_m = a0/(2πG)** | 0.22324 (106.90) | 0.26896 (128.79) | 0.28615 (137.02) | kg/m² |
| **Sigma_quad = a0/(4πG)** | 0.11162 (53.45) | 0.13448 (64.39) | 0.14308 (68.51) | kg/m² |

**Zero-sign remark:** all members positive on both footings; the phantom boost g_phi is positive (g > B) on RAR/Q/MONO in their domains; only the EXP branch is everywhere below 1/2 (§3.3). No sign cancellations are hidden — every quantity is a product/ratio of positive constants.

**ZD07 footing audit (A4/A5):** ZD07 quotes "68.4 M☉/pc²" but codes `A0 = 1.2e-10` — that value is **68.51 M☉/pc²**, i.e. +6.4% above the alternative footing's 64.39 and +28.2% above the canonical 53.45. The registered footings do not reproduce the quoted number at the 1% level.

**MW solar-circle saturation (C10):** with V_flat = 171.7 km/s, V_bar(R0) = 120 km/s, R0 = 8.2 kpc:

```
g_phi(R0)/a0 = (1.16505e-10 - 5.69322e-11)/a0  =  0.637 canonical / 0.528 alternative / 0.497 (1.2e-10)
```

The claim "the solar circle sits at 99.4% of the halo ceiling (0.497 < 1/2)" holds **only on the unregistered footing**. On both registered footings the Q-branch ceiling (1/2) is **exceeded** at the solar circle (0.528, 0.637) — with the RAR peak (0.6476) not exceeded on canonical (98.8% of the RAR cap). All of this is conditional on the committed MW anchor values and pointwise-limit interpretation; EFE and vertical-structure effects are explicitly out of this audit's domain (§5.1).

---

## 4. Branch audit of the cap `g_phi < a0/2` and the limiting regimes

### 4.1 Deep expansion of RAR (leading neglected term)

```
nu_RAR(y) = 1/(1 - e^{-sqrt y})
          = y^{-1/2} + 1/2 + y^{1/2}/12 + y/8·...   (sympy series, residual recorded)
g = B nu = sqrt(a0 B) [1 + sqrt(y)/2 + y/12 + ...]
```

Deep limit `g → sqrt(a0B) = C/r` with leading neglected term **B/2** (relative size √y/2). Checked numerically (D1, both footings): at r = 100 r_M (y = 1e-4) the residual `r g_RAR/C − 1 = +5.0083e-03` vs prediction `√y/2 = +5.0000e-03` — agreement 0.17%; at r = 10 r_M, 5.0833e-02 vs 5.0000e-02. The expansion domain is y ≲ 0.1 (r ≳ 3 r_M).

### 4.2 Newtonian limit

`nu_RAR − 1 = e^{-√y}/(1 − e^{-√y}) ≈ e^{-√y}` — exponential; ratio (nu−1)/e^{−√y} = 1.000045 at y = 100 and → 1 (mpmath 50-digit; float64 loses y = 1e4 to 1 + e^{−100}, recorded as a representation artifact). MONO recovers: nu_mono − 1 = 7.46e-3 (y = 10²), 8.94e-5 (10⁴), 1.04e-6 (10⁶) — the boost `a0 h_mono(y)` is bounded? **No — grows logarithmically** (§4.4), but g_phi/B → 0, so the Newtonian recovery holds as a *ratio* statement.

### 4.3 The caps per branch (pointwise kernel law)

| branch | halo boost g_phi = g − B | sup/peak | vs a0/2 |
|---|---|---|---|
| Q | a0(√(y²+y) − y); strictly increasing; sup a0/2 as y→∞ (strictly below at every finite y) | **a0/2 (sup, unattained)** | holds strictly |
| RAR | a0·h_RAR(y), h_RAR = y/(e^{√y}−1); unique peak at y_p = 2.5396, value **0.6476 a0** (bounded-boost theorem; reproduced to 5 digits) | 0.6476 a0 | **violated** (+29.5%) |
| EXP (historical) | a0 x e^{−x}, x = g/a0 implicit; peak at x = 1 | a0/e = 0.3679 a0 | holds (0.368 < 0.5) |
| MONO (operative) | a0 h_mono(y); h_mono(y) = h_RAR(y*) + δ h_p ln((y+y_p)/(y*+y_p)); splice y* = 2.3374 (reproduced); δ = 0.05, y_p = 2.5396, h_p = 0.6476 | **unbounded** (∝ ln y); h_mono(10⁴) = 0.8939 | **violated** at the splice itself (h_mono(y*) = 0.6470 > 1/2) |

Q cap, exact algebra (Lean-certified, `q_branch_halo_cap`):

```
sqrt(B^2 + a0 B) - B < a0/2    for all a0, B > 0,
  because  (sqrt(B²+a0B))² = B²+a0B < (B+a0/2)² = B²+a0B+a0²/4.
Gap:   a0/2 - g_phi = a0^2/(8B) + O(a0^3/(16B^2)),  (1/2 - g_phi/a0)·8y -> 1.   (C2)
```

**The ZD01/ZD07 ceiling therefore survives exactly on Q, fails on RAR by construction (peak 0.6476 > 0.5), fails on EXP? No — EXP holds; and fails pointwise on the operative MONO continuation.** The slip in the corpus is that the ceiling family's 1/2 was quoted without the branch qualification; the value 0.6476 > 0.5 (bounded-boost theorem, README) is itself recorded in the repository, so the audit's finding is a consistent reading of the existing record, not new physics.

### 4.4 Numerical controls that had to be able to fail

- **C1 (Q monotone-to-1/2):** stable evaluation `g_phi/a0 = y/(√(y²+y)+y)`; at y = 10⁸ the naive form loses the gap in float64 (catastrophic cancellation at `√(y²+y) − y`), recorded — the check is written in the stable representation and PASSES; the naive representation FAILS as documented (failed attempt, preserved in raw_output.txt of run 1: values 0.500000 at 10⁶–10⁸).
- **C5 (RAR violates the cap):** 0.6476 > 0.5 — the control is written so that a wrong claim "RAR is bounded by a0/2" fails the check.
- **C9 (MONO violates the cap):** h_mono(10⁴) = 0.8939 > 0.5 — same logic.
- **B5 (volume vs surface density):** `rho_ph(r_M)/Sigma0 = 1/(4π r_M²)` = 5.61e-42 (canonical, M_b = 10¹⁰ M☉) — a quantity with dimension 1/m². The naive equality rho = Sigma0 is **rejected on units** (kg/m³ vs kg/m²) and numerically fails by 41 orders. The correct pairing, derived and checked exactly (B6, Lean `phantom_density_bookkeeping`):

```
rho_ph(r) · (4 pi r^2) = Sigma0 · r_M        [true identity; units: [m]]
=> rho_ph(r) = (a0/G) · r_M/(4 pi r^2)        [volume density = surface density × length/area]
```

- **D1/D2 (limits):** deep-limit residual matches the leading term to 0.17% at r = 100 r_M; Newtonian ratio → 1; both are exact-identity limits, not finite consistency checks — the identity is `g_ptr = C/r` in the asymptotic sense with the explicitly derived next term, and `nu − 1 = e^{−√y}(1 + e^{−√y} + …)`.

---

## 5. Strongest surviving statement, domain, limitations

### 5.1 Strongest statement (scoped)

> **On the CORE scale identities with kappa = 1/2 adopted, all corpus surface-density ceilings are rational multiples of the single bookkeeping unit Sigma0 = a0/G (kg/m²). The coefficient map is: Sigma_pi = a0/(πG) (phantom projected at r_M; π = projected-disk convention), Sigma_m = a0/(2πG) (slab transition; 2π = plane-parallel Gauss), Sigma_quad = a0/(4πG) (ZD07 slab ceiling; 4π = 2π Gauss × 2 from the halo-field cap). The phantom density recast rho_ph(r)·4πr² = Sigma0·r_M is exact, so rho_ph can never equal Sigma0 — the unit-category control rejects it by 41 orders. The ceiling's 1/2 premise `g_phi < a0/2` holds exactly on Q (strict; sup unattained), holds on EXP (0.368 a0), fails on RAR (peak 0.6476 a0) and fails pointwise on the operative MONO continuation (0.8939 a0 at y = 10⁴, logarithmic growth). The ZD07 quoted value 68.4 M☉/pc² is a0/(4πG) at the unregistered a0 = 1.2e-10; the registered footings give 53.45 (canonical) and 64.39 (alternative) M☉/pc², and the MW solar-circle saturation fraction is 0.637 / 0.528 / 0.497 on canonical / alternative / legacy footings — above the Q cap on both registered footings.**

**Domain:** pointwise radial-limit laws and their bookkeeping, positive variables, both a0 footings, M_b = 10¹⁰ M☉ representative sample (the identities are M-independent where claimed). Approximation errors are quantified in §4; the RAR deep expansion holds for y ≲ 0.1 to the stated orders; the MONO logarithmic-growth numbers carry the contract's rounded landmarks (y_p = 2.5396, y* = 2.3374, δ = 0.05).

### 5.2 What this does NOT establish (limitations)

1. The ceiling's premise is pointwise-kernel truth/falsity. The **operative MONO target is filtered** (`nu_mono(|grad S u|/a0)` with the heat filter S); whether the *filtered operator* bounds g_phi — restoring a cap after smoothing — is **not** settled by this audit and is the single missing bridge (next implication).
2. `Sigma_phi,tot < a0/(4πG)` presumes the plane-parallel slab idealization for the phantom column and the vertical-field reading; real disks have radial gradients, warps, and EFE — out of domain.
3. The MW anchor numbers inherit the committed G03E/ZD07 values; a vertical-structure re-derivation is a different task.
4. Nothing in this file derives kappa = 1/2, nor the equilibrium relations (they remain conditional inputs per the contract — H037's 0.4893 transition-discrepancy factor and H033's 213.8 M☉/pc² are corpus history; the audit treats the bookkeeping conventions, not the historical fits).
5. The slab Gauss coefficient 2π is a physical-integration premise (div g = 4πGρ over a slab box), not re-derived inside Lean; it is named as an input in the certificate.
6. No observational fit, no data ingestion, no claim about actual galaxy surface densities beyond the stated bookkeeping identities.

### 5.3 Next unresolved implication (exact statement)

**Bridge B1:** Let `u` be a static solution of the operative filtered-MONO field equation `Δu = 4πGρ_b + S* div[(nu_mono(|grad S u|/a0) − 1) grad S u]` (contract MONO cell). The pointwise law gives `g_phi = a0 h_mono(y) → ∞` (logarithmically), so the ZD07 slab ceiling's column bound `Σ_phi,tot < a0/(4πG)` can only hold if the filter S (its measure, domain, boundary data, and the criterion-B leafwise time) converts the logarithmic growth into a bounded field — i.e., `‖S* div[(nu_mono − 1)∇(S u)]‖_z(Σ-box) < a0/2`-equivalent. **No derivation of that filtered bound exists; this audit shows the unfiltered premise is false, so the ceiling cannot be quoted on the operative branch by the old (Q-branch) argument.** The minimum discriminating computation: the z-column of the filtered MONO operator for the Milky-Way baryon model of G092/ZD07 on the two registered footings, against the two caps (53.45 / 64.39 M☉/pc²).

---

## 6. Lean 4 certificate

`AS009Coefficients.lean` (self-contained; only `import Mathlib`) certifies the algebraic core:

- `phantom_amplitude_identity` — C·r_M = G·M_b from the two defining squared relations (coefficient 1 of the amplitude law);
- `amplitude_law_ratios` — (C r/G)/M_b = r/r_M for every r > 0;
- `phantom_surface_density_at_rM` — M_b/(π r_M²) = a0/(πG) (mass cancellation);
- `phantom_density_bookkeeping` — (a0 r_M)/(4πG r²) = (a0/G)(r_M/(4πr²)) (the negative-control pairing);
- `ceiling_bookkeeping_half`, `sigma_milgrom_half_pi`, `sigma_pi_doubles_sigma_half` — the 1/2, 1/2, 2 coefficient relations of the ceiling family;
- `halo_gap_bound`, `q_branch_halo_cap` — √(B²+a0B) − B < a0/2 strictly for all positive B, a0 (the exact Q-branch cap: the only branch where the 1/2 premise is a theorem).

Compile: `cd fable_independent_2026/lean_2026 && lake env lean <run_dir>/AS009Coefficients.lean` — **exit 0, zero `sorry`**; `#print axioms` for all nine results yields exactly `[propext, Classical.choice, Quot.sound]` (recorded in `lean_axioms.txt`). Not certified in Lean (state changes are in the derivation): the RAR/MONO/EXP peaks (transcendental numerical analysis, mpmath 50 digits), the slab-Gauss 2π (physical premise), and kappa (adopted).

---

## 7. Reproduction

- Code: `AS009_audit.py` (single-threaded, stdlib + sympy 1.13.1 + mpmath 1.3.0; record: wall 0.55 s, user 0.52 s — `time_bounds.txt`; maxrss recorded in `AS009_audit_results.json`).
- Raw output: `raw_output.txt` (39/39 checks PASS; exit 0; failures from the first prototype — quadrature tip cutoff, float64 cancellation and underflow, check-expression scoping — are preserved as the honest first-pass record in `raw_output_attempts/` of the conversation summary §8; the final script fixes representation, not physics).
- Script exit code is 0 iff all checks pass; it fails loudly otherwise (no hard-coded verdicts).