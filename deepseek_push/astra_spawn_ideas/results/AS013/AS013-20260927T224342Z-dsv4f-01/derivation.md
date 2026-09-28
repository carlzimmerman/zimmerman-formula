# AS013 — A distance scaling degeneracy of the deep law: derivation and audit

**Run:** `AS013-20260927T224342Z-dsv4f-01` · **Worker:** deepseek/deepseek-v4-flash-0731
(provider openrouter), Hermes Agent focused subagent — identity from the executing
agent's own system context, not inferred from the `deepseek_push/` folder name.
**Started:** 2026-09-27T22:43:42Z · **Finished:** 2026-09-27T22:52:24Z.
**Group:** A01 — Scale, units and independent inputs · **Kind:** audit · **Branch:** CORE
scale identities (v_flat^4 = G M_b a0 area); Q, RAR, MU2, EXP, MONO are evaluated only as
labelled curves, never imported as the mechanism.

## 1. Sources and hash verification

| Source | SHA-256 | Manifest pin | Match |
|---|---|---|---|
| README.md | `91a5fac4…a6b6ed` | same | ✓ |
| qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md | `98d9149f…5d8e3f` | same | ✓ |
| campaign_fresh_gravity_astra/DERIVATIONS.md | `8da8176e…2fb889` | same | ✓ |
| STANDING.md | `660462eb…76bf63` | (manifest row) | ✓ |
| deepseek_push/astra_spawn_ideas/SOURCE_MANIFEST.json | `fe295b80…7f57fba` | (manifest row) | ✓ |
| AS013 task file | `064ff7d0…1963af` | claims file pin | ✓ |
| FRAMEWORK_CONTRACT.md / RESULT_CONTRACT.json | `ca696c7f…0dddf9` / `621fdad0…21517` | — | ✓ |

All checksums computed with hashlib inside `compute_as013.py`; the three pinned task
sources match SOURCE_MANIFEST.json exactly. No source drifted from the pinned base.

## 2. Precise claim under audit (from the task's "Mathematics and principal test")

> `M_b proportional to D^2 for fixed flux; v_flat^4=G*M_b*a0 implies a0 proportional to D^(-2) at fixed velocity.`

Formalized audit question: **which quantity is degenerate and which is pinned** when a
deep-law rotation curve is analysed under rescaled distance and inclination?

### Symbol dictionary

- `G` Newton coupling (SI), `c` speed of light, `M_sun`, `pc` — contract defaults.
- `D` distance to galaxy, `r = Dθ` physical radius at angular radius `θ`.
- `F(θ)` observed flux; `L(θ) = 4πD²F(θ)` luminosity; `M_b(θ) = (M/L)·L(θ)` baryonic
  mass (flux-derived, fixed mass-to-light `M/L`) — hence **M_b ∝ D² at fixed flux**.
- `i` inclination, `v = v_los/sin i` circular velocity from the line-of-sight velocity.
- `a0 = κ c sqrt(G ρ_Lambda)`, `κ = 1/2` **adopted as input** (not derived here).
- `B(θ) = G M_b(θ)/r(θ)²` Newtonian baryonic acceleration; `y = B/a0`.
- `r_M = sqrt(G M_b/a0)`; `θ_M = r_M/D`; `C = sqrt(G M_b a0) = v_flat²`.
- Deep law: `v_flat⁴ = G M_b a0`; deep-MOND acceleration `g = sqrt(a0 B)`.
- Group parameters: `λ` (distance ratio `D' = λD`), `s` (inclination-sine ratio).

### Framework inputs vs conclusions

**Inputs (adopted):** G, c, κ = 1/2, the a0 footings, M_b ∝ D² flux scaling, v = v_los/sin i,
the deep law v⁴ = G M_b a0, r_M = sqrt(G M_b/a0), the kernel labels Q/RAR/MONO/EXP as
defined in FRAMEWORK_CONTRACT (ν_Q(y)=√(1+1/y), ν_RAR(y)=1/(1−e^{−√y}), ν_mono via the
specified h-construction). **Conclusions established here:** the exact invariance group,
the pinned combination, the per-branch break magnitudes and approach rates, and the
internal inconsistency of the frozen-M_b update.

## 3. Step-by-step derivation

### 3.1 The distance scaling degeneracy (task step 2, first half)

**Lemma 1 (flux scaling).** At fixed flux and fixed mass-to-light,
`M_b(θ) = 4π (M/L) D² F(θ)`, so under `D → λD` the inferred baryonic mass obeys
`M_b → λ² M_b`, while the Newtonian baryonic acceleration
`B(θ) = G M_b(θ)/(Dθ)² = 4πG (M/L) F(θ)/θ²` is **exactly distance-free**:
`B'(θ) = B(θ)`.

**Lemma 2 (deep-profile invariance).** In the strict deep regime `g = sqrt(a0 B)`, the
predicted velocity profile as a function of **angle** is

```
v⁴(θ) = r² g² = (Dθ)² · a0 · B(θ) = (Dθ)² · a0 · G M_b(θ) / (Dθ)² = G a0 M_b(θ) .
```

The distance cancels identically. Since `M_b(θ) ∝ D²`, the prediction is exactly invariant
under the one-parameter group

```
R_λ :  (D, M_b, a0) → (λD, λ² M_b, λ^(−2) a0),   v(θ) unchanged,   λ > 0 .
```

Direct substitution (independent of the cancellation argument):
`G·(λ²M_b)·(λ^(−2)a0) = G·M_b·a0 = v_flat⁴`. This is the task's statement in exact form:
**at fixed velocity the inferred scale obeys a0 ∝ D^(−2)** (equivalently the *product*
`M_b·a0` — the only quantity the plateau sees — is preserved). Both statements are exact
field algebra: sympy residual 0 (CK-A1), Lean `deep_product_invariance` (T1), and 60-dps
residuals ≤ 9.3e−61 over λ ∈ {0.5, 0.8, 1.2, 1.5, 2.0, 3.3} on both footings (CK-C).

The logarithmic slope form: along the orbit `d ln a0 / d ln D = −2` exactly (CK-C slope
checks, both footings, residual < 1e−12).

**Dependent scalings** (all exact consequences, CK-E): `r_M → λ² r_M`
(r_M = sqrt(G M_b/a0) is not scale-1, it is scale-2 in λ), the observed transition angle
`θ_M = r_M/D → λ θ_M`, and the interpolation parameter at fixed θ scales as
`y = B/a0 → λ² y`. A distance error therefore *moves the RAR locus vertically*
(g_obs(θ) = v²/(Dθ) ∝ 1/λ) **and stretches the y-axis** (y ∝ λ²), while `B(θ)` stays
fixed — which is why a fitted scale absorbs the error as exactly λ^(−2).

### 3.2 Inclination scaling and the combined invariance (task step 2, second half)

The inclination correction `v = v_los/sin i` multiplies all velocities by the same factor.
With mis-specified inclination sines `s = sin i_assumed / sin i_true`, the analysis uses
`v = v_los/(s sin i_true)`, i.e. the velocity inferred from the same v_los is rescaled by
`1/s`. The deep law then reads, in observed variables,

```
v_los⁴ = sin⁴i · G · M_b · a0 ,
```

so an inclination error enters the inferred scale at the **fourth** power.

**Combined invariance (exact).** For the two-parameter group

```
R_{λ,s} :  (D, sin i, M_b, a0) → (λD, s sin i, λ² M_b, λ^(−2) s^(−4) a0),   v_los → v_los ,
```

`sin⁴i·G·M_b·a0 = v_los⁴` is invariant (CK-A2 exact, CK-D ≤ 2.5e−60); equivalently the
predicted **line-of-sight** rotation curve is exactly unchanged. The group is a genuine
one-parameter-action product: it composes as `R_{λ2,s2}∘R_{λ1,s1} = R_{λ1λ2, s1s2}`
(Lean `orbit_composition`, T4).

### 3.3 What is pinned, what is degenerate (the audit answer; task steps 1 and 5)

From deep-plateau data alone (one or many galaxies, no transition-regime information):

| Quantity | Status | Exact law |
|---|---|---|
| `v_flat⁴/G` and `M_b·a0·sin⁴i = v_los⁴/G` | **PINNED** (inclination-corrected product) | Lean T6: two models with the same plateau differ by exactly one orbit element `(λ²M_b, a0/λ²)` with `λ = sqrt(M_b'/M_b)`; individual `M_b` and `a0` are not identifiable |
| `a0` | **DEGENERATE** along the orbit | `a0 ∝ D^(−2) sin⁴i`; global scale only if the distance ladder and inclinations are right |
| `M_b` | **DEGENERATE** | `M_b ∝ D²` (flux) — the mass scale cannot be separated from D by the plateau |
| `r_M`, `θ_M` | **DEGENERATE** | `r_M ∝ λ²`, `θ_M ∝ λ` |
| `y = B/a0` at fixed θ | **DEGENERATE** | `y ∝ λ²` |
| `B(θ)` | **PINNED** (distance-free) | `B(θ) = 4πG(M/L)F(θ)/θ²` |
| `v(θ)` shape (flatness) | **PINNED** | observed |

The pinning theorem (T6) is the exact statement of "which quantity is degenerate": two
deep-law models sharing one measured flat velocity are related **precisely** by the
one-parameter distance orbit — no other freedom exists at the algebraic level.

### 3.4 The interpolating and Newtonian regimes break the degeneracy (task step 3)

For any branch with kernel ν (g = B·ν(y)), under R_λ at fixed θ the predicted quartic
velocity transforms as (B invariant, y → λ²y, r → λr):

```
v'⁴(θ)/v⁴(θ) = λ² · [ν(λ² y)/ν(y)]² .                                   (∗)
```

- **Deep limit.** All framework kernels satisfy `ν(y) → y^(−1/2)` (Q, RAR, MONO; EXP has
  the same asymptotics), so `(∗) → 1`: the degeneracy is exact in the deep regime for
  every branch — the audit conclusion is branch-common in the deep limit.
- **Q branch (exact finite-y factor).** With `ν_Q(y) = √(1+1/y)`, `(∗) = (λ²y+1)/(y+1)`,
  and exactly
  `v'⁴/v⁴ − 1 = y(λ²−1)/(y+1)`  (Lean `q_break_identity`, T5; sympy/numeric residual
  ≤ 1.2e−60 over y ∈ [1e−4, 1e6], CK-F1). **Leading neglected deep term:** `y(λ²−1)`
  with next term `−(λ²−1)y²/(y+1)`, i.e. the O(y) statement is exact and bounded by
  `(λ²−1)y²` (CK-F2). Numeric log-slope d ln(ratio)/d ln λ = 2y/(y+1) reproduces the
  formula to < 1e−8 by two-sided finite differences (CK-F3, independent representation).
- **RAR and MONO branches.** `(∗)` evaluated numerically: deep limit approached as the
  leading term `(λ−1)√y` (expansion ν_RAR(y) = y^(−1/2)(1 + √y/2 + y/12 + …)), verified
  on three decades y ∈ {1e−9, 1e−7, 1e−5} with relerr ≤ 1.3e−4 vs the leading term
  (CK-G approach rate); at y = 1e−6 the residual |v'⁴/v⁴ − 1| = 5.0e−4.
- **Newtonian limit.** `ν → 1`, so `(∗) → λ²`: at fixed θ the velocity grows as
  `v(θ) ∝ D^(1/2)` — the Keplerian part **pins the distance** to the half power
  (exact for all branches; CK-G Newtonian rows ≤ 1.3e−6).
- **Magnitude of the break.** λ = 1.5 at the knee (y = 1): `v'⁴/v⁴ = 1.625` (Q), 1.490
  (RAR, MONO) — a 50–60% quartic-velocity mismatch at the knee, i.e. the transition/Newtonian
  region is a *strong* distance lever, while the plateau alone is exactly blind.
- **RAR-locus reading.** The knee in the (B, g_obs) locus sits at y = 1, i.e. at
  B-coordinate a0, which is distance-free (B(θ) is D-free); resolving the knee pins a0 up
  to the mass-to-light normalization, independently of D.

### 3.5 Units and signs (task step 3)

`[v⁴] = L⁴T⁻⁴`, `[G M_b a0] = L³M⁻¹T⁻²·M·LT⁻² = L⁴T⁻⁴` ✓; `[r_M] = √(L³M⁻¹T⁻²·M·LT⁻²)⁻¹`
= L ✓; `[θ_M] = L/L` ✓; `[a0 D²] = LT⁻²·L² = L³T⁻² = [v⁴/(G (M/L) 4π F)]` ✓ (F in W/m² =
M T⁻³). All quantities used are strictly positive (λ, s, y, sin i > 0); no sign ambiguity
appears. Dimensional examples are quoted on **both** footings (see §6) — the invariance
itself is dimensionless, so it applies identically to both footings, and each footing's
numbers scale under R_λ with exactly the same exponents.

## 4. Independent checks (task step 4)

1. **Symbolic substitution** (sympy, with positive-symbol assumptions): residuals of the
   deep-product identity, the combined (λ, s) identity, and the r_M-scaling identity are
   each exactly 0 (CK-A1..A3).
2. **High-precision mock** (mpmath, 60 dps): one LSB galaxy, M_b = 1e9 M_sun, D = 10 Mpc,
   i = 60°; every invariance and every break factor evaluated as an actual number;
   all residuals recorded above (all ≤ 2.5e−60 for the exact identities).
3. **Direct differentiation** (independent representation): two-sided finite-difference
   log-slopes vs the analytic 2y/(y+1) to < 1e−8 (CK-F3).
4. **Lean 4 certificate**: six theorems, zero `sorry/axiom` beyond
   {propext, Classical.choice, Quot.sound} (verified by unfiltered `#print axioms`);
   see `AS013_distance_degeneracy.lean` and `lean_axioms_out.txt`.

The exactness status is stated per item: the invariance and the Q break factor are **exact
identities** (proved symbolically and in Lean); the finite-precision evaluations are
consistency probes with actual residuals, never asserted as proofs.

## 5. Negative controls (task step 5; "Controls that must be capable of failing")

**NC1 — change D in a mock while freezing M_b (and a0): the internally inconsistent update.**
Starting from the consistent mock (v_flat = 59.3707 km/s canonical), set D → 1.5 D with
M_b and a0 frozen. The checker measures four consequences:

1. **Flux inconsistency:** a flux-based analyst at the new distance derives
   M_flux = λ²M_b = 2.250 M_b ≠ M_frozen — two prescriptions for the same mass disagree
   by exactly λ² (NC1a, must ≠ 1: PASS-as-failure with factor 2.25).
2. **Velocity inconsistency:** at fixed θ the deep plateau is unchanged but the
   Newtonian prediction grows by √λ = 1.2247 (22.47%) — the same data point cannot be
   simultaneously deep-flat and Keplerian (NC1b, must ≠ 1: PASS-as-failure, 22.47%).
3. **Transition-angle inconsistency:** the frozen update keeps r_M, predicting
   θ_M' = θ_M/λ, while the self-consistent deep law requires θ_M'' = λθ_M — disagree by
   λ² = 2.25 (NC1c).
4. **Scale inconsistency:** the flux-implied scale a0_implied = v⁴/(G M_flux) = a0/λ² =
   0.4444 a0 ≠ the frozen global a0 = κc√(Gρ_Lambda) (NC1d).

Sensitivity proof (capability of failing): the **same** checker applied to the joint,
consistent update (λ²M_b, λ^(−2)a0) returns relative residual 9.239e−61 < 1e−50
(NC1e) — the checker would have passed a consistent update and fails the frozen one with
recorded nonzero magnitudes. **Verdict: the frozen-M_b update is internally inconsistent;
the only consistent reparametrization is the orbit R_λ itself.**

**NC2 — limiting regimes, normalization and boundary case.**
- Deep limit: ratio (∗) → 1 for Q, RAR and MONO (residuals at y = 1e−6: 1.25e−6, 5.0e−4,
  5.0e−4; approach rates exact to the leading term, §3.4).
- Newtonian limit: ratio (∗) → λ² for all three branches (rows ≤ 1.3e−6).
- Boundary r = r_M: B(r_M) = a0 identically (definition of r_M; both footings,
  residual ≤ 1.5e−60) and g_Q(r_M)² = 2a0² (≤ 2.9e−60) — normalization/boundary case.
- y-normalization: y'(θ) = λ²y(θ) with residual exactly 0 (NC2_y_rescaling).
- Deep profile distance-freeness: v⁴(θ) = G a0 M_b(θ) over the angular grid with
  max relative residual 1.5e−60 (NC2_deep_profile_distance_free) — the D-cancellation is
  exact.

## 6. Both footings (framework contract)

All dimensional mock numbers quoted on both footings (canonical 9.3619e−11, alternative
1.1279e−10 m/s²), separately, never sharing a fixed ρ_Lambda with a fixed κ:

| Quantity | canonical | alternative |
|---|---|---|
| ρ_Lambda implied (κ = 1/2) | 5.8444e−27 kg/m³ | 8.4831e−27 kg/m³ |
| v_flat (1e9 M_sun) | 59.3707 km/s | 62.2012 km/s |
| v_los at i = 60° | 51.4165 km/s | 53.8678 km/s |
| r_M | 1.22020 kpc | 1.11167 kpc |
| θ_M at D = 10 Mpc | 25.168 arcsec | 22.930 arcsec |

Footing bookkeeping: a0_alt/a0_can = 1.204776808127; with ρ_Lambda fixed, effective
κ = 0.602388404063 (≠ 1/2); with κ = 1/2 fixed, ρ ratio = 1.451487157400 (consistent with
the sibling AS010 bookkeeping). The degeneracy itself is dimensionless: it applies
identically to both footings (CK-C/D/E pass on both), so no footing-specific statement is
needed beyond reporting the numbers.

## 7. Branches

Q, RAR and MONO (and the historical EXP asymptotics) are used only as labelled curves for
the break factor (∗); the conclusion of §3.3 does not depend on any of them (it is the
deep law itself). The degenerate orbit is also exact for the strictly deep branch
g = √(a0B) of every branch, and the operative target's declared deep content
(g² = a0 g_N ⇒ v⁴ = G a0 M_b, requirement 1 of the amended thirteen) is exactly the object
audited. The MONO construction was rebuilt from the FRAMEWORK_CONTRACT text
(y_p = 2.539638, h_p = 0.647610, y* = 2.337412, δ = 0.05, continuous derivative at the
join: relerr 0) and reproduces the stated ≤ 0.0104 dex agreement with ν_RAR
(max 0.01037 dex at y = 14.4) — informational, not load-bearing. The heat filter S is not
exercised: it is a smoothing operator on the field, not on the pointwise deep asymptotics
that carries the degeneracy.

## 8. Strongest surviving statement

> **Theorem (distance–inclination degeneracy of the deep law).** Let λ, s > 0. For
> flux-derived baryonic masses (M_b ∝ D², fixed M/L) and circular velocities
> v = v_los/sin i, the deep-law prediction v_flat⁴ = G M_b a0 (equivalently the whole
> deep-MOND angular profile v⁴(θ) = G a0 M_b(θ)) is exactly invariant under
> (D, sin i, M_b, a0) → (λD, s sin i, λ²M_b, λ^(−2)s^(−4)a0) with v_los(θ) unchanged.
> The plateau pins exactly the combination M_b·a0·sin⁴i = v_los⁴/G; individually a0 is
> degenerate with a0 ∝ D^(−2) sin⁴i (a0 ∝ D^(−2) at fixed velocity — the task's claim is
> exact), M_b ∝ D², r_M ∝ λ², θ_M ∝ λ. The degeneracy is broken quantitatively at finite
> interpolation parameter — v'⁴/v⁴ = λ²[ν(λ²y)/ν(y)]², exactly (λ²y+1)/(y+1) for Q —
> and by the Newtonian regime v(θ) ∝ D^(1/2), plus external anchors; deep-only data
> cannot do so. Certified in Lean 4 (6 theorems, zero sorry, axioms ⊆
> {propext, Classical.choice, Quot.sound}).

Domain: λ, s, y, sin i > 0; point-mass/spherical-circular idealization for the profile
form; SI units; both a0 footings.

## 9. Limitations

- The degeneracy is an *identifiability* statement about the deep law, not a statement
  about real data quality or about any specific analysis pipeline; no observational fit.
- The profile statement v⁴(θ) = G a0 M_b(θ) uses the spherical/point-mass enclosed-mass
  idealization; realistic disks modify B(θ) but not the algebraic orbit (B stays
  D-free).
- M/L is held fixed in the flux scaling; an unknown M/L adds a third degenerate direction
  (the knee argument pins a0 only up to M/L).
- The break known-to-be-exact formula is derived for Q and verified (finite) for RAR/MONO;
  the MONO break relies on the numeric construction of ν_mono from the contract text.
- Nothing here derives κ = 1/2 or removes the adopted normalization freedom; the
  degeneracy is scale-free and cannot be used to measure κ from deep data alone.
- Numerical residuals ≤ 2.5e−60 are consistency checks of exact identities, not
  independent evidence; the identities themselves are Lean-certified.
- A completed task is not closure of gravity; the relation v⁴ = G M_b a0 is the target's
  declared deep content, not a derivation of the constitutive dynamics.

## 10. Next unresolved implication

The **first missing bridge** is a quantitative identifiability transfer: how much
transition/Newtonian-regime data (per-galaxy knee resolution as a function of (λ, s)
noise, M/L priors and inclination distributions) is required for the operative MONO
branch (through the heat filter) to pin a0 per object and for a population fit to survive
realistic distance-ladder errors — i.e., the exact sensitivity of the a0/κ inference to
the breakers of §3.4. Until then, deep-regime-only determinations of a0 (hence κ) inherit
the exact λ^(−2) degeneracy; interpolating-regime curvature is the mathematical breaker,
external anchors (distance ladder, lensing, wide binaries, the in-repo distance-free κ
measurement) the empirical ones.

## 11. Suggested followup (duplicate-checked)

Catalog search (manifest/INDEX/claims, keyword scan of all AS seeds) found no seed that
targets the distance–inclination degeneracy of the deep law itself; the flagged A17
high-z identifiability seeds (AS1711, AS1765) cite the same
`joint_identifiability/RESULT.md` source but treat redshift-space/velocity-coordinate
identifiability, not the D–a0 orbit. Ready child spec (NOT dispatched — no subagent spawn
mechanism is available in this worker) in `AS013.C01` below; the orchestrator may dispatch
it or attach it to the nearest catalog seed.

**Ready child AS013.C01 — "Distance-degeneracy breaking power of the interpolating
regime (operative MONO, through the heat filter)".** New target: derive a per-object
Fisher-type bound or worst-case error on a0 from knee-region data under Gaussian (λ, s,
M/L) uncertainties, using the exact factor (∗) and the MONO kernel of the operative
target, and state the population-level distance-ladder error budget for the framework's
κ = 0.551±0.043 distance-free claim to survive. Parent: AS013 run
AS013-20260927T224342Z-dsv4f-01 (hashes in result.json). Controls: (i) λ = 1 limit must
give zero bias; (ii) the bound must fail (collapse) as the knee sample → deep-only.
Dependencies: FRAMEWORK_CONTRACT MONO definitions, DERIVATIONS.md §2 moment machinery.
Duplicate check: no existing AS/MY/FGF task found matching this fingerprint.

## 12. Deliverables (this directory)

- `derivation.md` (this file)
- `compute_as013.py` — bounded prototype (≤120 s alarm, single thread, 60 dps; RSS
  reported: 58.9 MB)
- `raw_output.txt` — full run transcript (43 checks, 43 PASS)
- `AS013_distance_degeneracy.lean` — Lean 4 certificate (6 theorems, zero sorry)
- `lean_axioms_out.txt` — compile log + axiom lists
- `result.json` — schema-v2 result record