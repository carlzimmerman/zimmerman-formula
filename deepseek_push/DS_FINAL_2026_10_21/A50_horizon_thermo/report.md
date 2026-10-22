# A50_horizon_thermo — the first law of horizon mechanics, and why it cannot fix κ

## Claim

The thermodynamic door is real and it opens onto an empty room. Written at the apparent horizon of the
theory's own FRW background with `T = ħH/2πk_B` and `S = A/4ℓ_P²`, the Clausius relation is **two exact
identities**: `T dS = (c⁴/G) dr_A` (K1, residual 0) and `dE + P dV = ((1+3w)/2)·T dS` (K2, residual 0).
Both sides are proportional to `Ḣ`, so `Ḣ` cancels and the first law is **not an equation of motion** — its
entire content is the algebraic condition `λ = (1+3w)/2` on the temperature normalisation `T = λT_dS`. With
the literal de Sitter temperature (`λ = 1`) it closes **iff w = 1/3** (K3); for dust it fails by exactly 2;
for vacuum it is degenerate. The surface-gravity coefficient it implies is therefore not 1 and not 1/2 but
the **function** `κ_sg/cH = (1+3w)/2`, running from −1 to 1.25 over w ∈ [−1, 1/2] (K4). The 1/2 does appear —
twice — and both times it is Einstein bookkeeping: as the dust-era value of that running coefficient, and as
the ratio `(4πG/3)/(8πG/3)` in `N_bulk/N_surf` (K7). Neither is the κ of `a0 = κc√(Gρ_bare)`, because **no
horizon functional contains κ or a0 at all** (K11: symbolic absence, plus a 400-point scan with drift
1.7e-16). Converting the thermodynamic 1/2 into κ requires the map `a0 ↔ horizon acceleration`, which carries
the Einstein factor `√(3/8π) = 2/Z = 0.3454941`: doing it honestly gives `κ = λZ/2 = Z/4 = 1.447203`, 2.894×
the canonical value and 2.894× the observed acceleration scale (K16). To reach κ = 1/2 the first-law
coefficient would have to be `1/Z = 0.1727471 = (1/2)√(3/8π)`, i.e. an equation of state `w* = −0.2181686`
that the theory does not contain. The factor standing between the thermodynamic 1/2 and κ = 1/2 is
`√(3/(8π))`, **not** `2√(32π/3) = 11.5776`, which overshoots the requirement by 33.5× (K15). Status:
**NO-GO(obstruction)** — the first law is the Friedmann equation's integrated form and is κ-free; it supplies
a 1/2 in the wrong slot, and the κ = 1/2 statement additionally needs an Einstein input.

## Derivation

### 1. Setup

Flat FRW, `H = ȧ/a`, apparent horizon at the Hubble radius `r_A = c/H` (for flat FRW the apparent and Hubble
horizons coincide). Horizon area `A = 4πr_A²`, Planck area `ℓ_P² = Għ/c³`,

    (1.1)  S = A/(4ℓ_P²) = π c⁵/(G ħ H²) k_B ,        T = ħ H/(2π k_B) .

Matter: a perfect fluid with `P = w ρ c²`, energy inside the horizon `E = ρc²V`, `V = (4π/3)r_A³`. The
theory's own sector is collisionless cold matter (P4, dust: w = 0) plus the bare vacuum (P3: w = −1), so the
two λ values that matter for it are 1/2 and −1.

### 2. Two exact identities

    (2.1)  T dS = (c⁴/G) dr_A .

*Proof.* `dS/dH = −2πc⁵k_B/(GħH³)`, so `T dS = −(c⁵/G)H⁻²dH`; and `dr_A/dH = −c/H²`, so
`(c⁴/G)dr_A = −(c⁵/G)H⁻²dH`. Identical. (K1, sympy residual exactly 0, ratio 1.000000000000000.) The
horizon's heat flow is one entropy unit per Planck length of radius — nothing else.

    (2.2)  dE + P dV = ((1+3w)/2) · (c⁴/G) dr_A = ((1+3w)/2) · T dS .

*Proof.* Along any flat FRW solution `ρ = 3H²/(8πG)`, hence `E = ρc²V = c⁵/(2GH)` (Misner–Sharp), so
`dE/dt = −(c⁵/2G)Ḣ/H²`, while `dV/dt = −4πc³Ḣ/H⁴` and `P dV/dt = −(3/2)w(c⁵/G)Ḣ/H²`. Adding,
`dE/dt + P dV/dt = −(c⁵/G)(Ḣ/H²)(1+3w)/2 = ((1+3w)/2)T dS/dt`. (K2: λ ≡ (dE+PdV)/(T dS) = (1+3w)/2 exactly,
∂λ/∂Ḣ = 0, λ(0) = 0.5, λ(1/3) = 1.)

### 3. The equation of state the first law derives

Both sides of (2.2) carry one factor of `Ḣ`; it cancels. So `T dS = dE + P dV` is **not** an equation for the
expansion rate: it is the single algebraic statement

    (3.1)  λ = (1+3w)/2 ,   T ≡ λ T_dS .

With the literal de Sitter temperature (`λ = 1`) the Clausius relation closes **iff w = 1/3** (K3: `solve`
returns exactly 1/3). Read as an equation of state, that is the result: **the first law at a conformal horizon
is exact for radiation and only for radiation.** Consequences:

- **Dust (w = 0):** `T dS = 2(dE + P dV)` — the law misses by exactly 2 (K3, `dust_failure_factor` = 2.000).
  Equivalently, imposing the law with `T = T_dS` under-predicts `Ḣ` by 2, i.e. it behaves like `G_eff = G/2`
  (K5, `G_eff/G` = 2.000000). This is the "factor 2 problem" of the horizon first law, as an effective `G`.
- **Vacuum (w = −1):** `λ = −1` and both sides vanish on-shell (`Ḣ = 0` for exact de Sitter): 0 = 0 (K3).
- **No constant works:** over w ∈ [−1, 1/2], λ runs −1 → 1.25, a spread of 2.25 (K4).

### 4. The coefficient of the horizon's surface gravity — neither 1 nor 1/2

`T = λT_dS` is, in acceleration units, `κ_sg = λc²/r_A = λcH`. So the first law forces

    (4.1)  κ_sg/(cH) = (1+3w)/2  ∈ [−1, 1.25] .

It is **forced to be a function of w, not a constant**, and therefore cannot be the theory's constant κ (P3
ties κ to today's `ρ_bare` once and for all). 1/2 occurs only in the dust era and 1 only in the radiation era;
neither is universal. Direct answer to "is the coefficient forced to 1 or 1/2 by the first law itself":
**neither — it is forced to (1+3w)/2.**

### 5. The three candidate identities: efficiency, equipartition, surface/bulk

Padmanabhan's template: `N_surf = A/ℓ_P² = 4S/k_B`, `N_bulk = 2|E_K|/(k_BT)`. At H0 the horizon carries
`N_surf = 9.0616e122` degrees of freedom, `T_dS = 2.6554e-30 K`, `S = 3.1277e99 J/K`, `E = 8.3053e69 J`
(note `T·S = E` exactly — K6 confirms both `T·S/E = 1.000000000000` and the trap that `d(TS) ≠ T dS`: the
heat form is `2.000000000032` × dE by finite difference on an integrated dust FRW).

    (5.1)  N_bulk/N_surf = (4πG/3) ρ/H² = (1/2)|1+3w| (ρ/ρ_crit)        [K9, residual 0]

- **Naive energy** (`E = ρc²V`, w = 0): ratio `= (1/2)(ρ/ρ_crit)`, exactly **1/2** at `ρ = ρ_crit` (K7:
  `N_bulk = 4.5308e122`, ratio 0.500000000000000). The 1/2 is nothing but `(4πG/3)/(8πG/3)`, Einstein's.
- **Komar energy** (`|ρ+3P| = 2ρ` for vacuum): ratio exactly **1** (K8). The Komar energy removes the 1/2.
- **Saturation:** `N_surf = N_bulk^Komar` ⟺ `ρ = 3H²/(8πG)` ⟺ **P3** (K10). The theory's vacuum *is* saturated
  holographic equipartition — exactly, for free. P3 rewritten, not κ derived. Surface/bulk is 1 (Komar) or 2
  (naive); the 1/2 is bulk/surface in the naive count. None of these is κ.

**The efficiency reading.** The law's share variable is `ε ≡ 1 − g_N/g = a₀/(g+a₀)`. At the horizon
acceleration `g = cH` this is `ε = x/(1+x)` with `x = a₀/(cH) = 2κ/Z`, i.e. `ε(cH) = 1/(1+Z) = 0.1473012`
at κ = 1/2 (K17). Demanding that the medium supply exactly half the acceleration at the horizon (`ε = 1/2`)
forces `x = 1`, `a₀ = cH`, `κ = Z/2 = 2.894405` — 5.79× too large in both κ and a0. And where the theory
*does* carry an exact 1/2 — the Langmuir half-saturation `μ = 1/2` at `g = a₀` — it is a tautology of the
definition `x = g/a₀`: it holds for every κ (K17, drift 0 over the κ scan).

### 6. The structural obstruction, stated exactly

    (6.1)  T, S, E, P, V, N_surf, N_bulk  are all functionals of (H, ρ, G, ħ, c, w) only.
           ∂/∂κ = ∂/∂a0 = 0 for every one of them.        [K11: True; scan drift 1.7e-16 over 400 κ]

No identity among quantities that do not contain κ can output κ. The step from "coefficient 1/2" to "κ = 1/2"
requires an extra map, and there is only one available:

    (6.2)  a0 = κ c √(G ρ_bare),  ρ_bare = ρ_crit = 3H²/(8πG)
           ⇒ a0/(cH) = κ √(3/8π) = κ·(2/Z) ⇒ κ = λ Z/2 .

That map's normalisation `√(3/8π)` is the Einstein `ρ ↔ H` conversion — an independent postulate, not a
thermodynamic output. The first law can give you `λ`; the translation of `λ` into κ is not thermodynamic.

### 7. The factor question: √(3/8π), not 2√(32π/3)

    (7.1)  κ = 1/2 ⟺ a0/(cH) = (1/2)√(3/8π) = √(3/32π) = 1/Z = 0.1727470747 .     [K12, residual 0]

So the number κ = 1/2 requires is the coefficient `(1/2)√(3/8π)` in the `a0/(cH)` normalisation, while the
thermodynamic 1/2 arrives **without** `√(3/8π)`. The factor between the two is therefore

    (7.2)  √(3/(8π)) = 2/Z = 0.3454941 ,       (1/2)·(2/Z) = 1/Z ,                 [K14, all residuals 0]

and **not** `2√(32π/3)`. That number is the reciprocal-flavoured one: `2√(32π/3) = 2Z = 4/√(3/8π) = 11.5776`
(K14) — the "2cH/a0 = 2Z" of the brief, not a thermodynamic factor. The candidate "1/2 × 2√(32π/3)" = Z =
5.7888 overshoots the required 0.1727 by **33.51×** (K15). Of the two named candidates the correct one is
`√(3/(8π))`; the other is excluded by a factor 33.5.

### 8. The two readings, and what each gives

**(A) Physical reading — a0 *is* the horizon's acceleration.** Then `a0 = λ c²/r_A = λcH`, and (6.2) gives
`κ = λZ/2`:

| λ (EOS) | κ = λZ/2 | a0 (m/s²) | vs canonical | vs 1/2 |
|---|---|---|---|---|
| 1/2 (dust) | **Z/4 = 1.447203** | 3.2742e-10 | 2.894× | 2.894× |
| 1 (radiation) | Z/2 = 2.894405 | 6.5484e-10 | 5.789× | 5.789× |

(K16: κ_A(1/2) = 1.447202509, κ_A(1) = 2.894405018; `a0_at_Z4` = 3.2742e-10 against `a0_canon` = 1.1312e-10.)
Both land on Lane A1's menu entries `Z/4` (g=2) and `Z/2` (g=1); neither is 1/2. Reading (A) is the physically
meaningful one — a0 is an acceleration and the horizon has an acceleration — and it is **falsified**:
κ = Z/4 would put a0 at 2.894× the RAR scale.

**(B) Numerical reading — identify κ with λ.** This gives 1/2 at w = 0, but it is a category slip: λ multiplies
a temperature and κ multiplies `c√(Gρ)`. It is admissible only as a pure-number match, and it is exactly the
step that assumes the answer. Under (B) the first law "derives" κ = 1/2 by *defining* κ to be the coefficient
— and the coefficient is (1+3w)/2, i.e. κ would run with w. The equation of state that would make reading (A)
give κ = 1/2 exactly is

    (8.1)  (1+3w*)/2 = 1/Z ⇒ w* = (2/Z − 1)/3 = −0.2181686 ,                        [K16]

neither dust (0), radiation (1/3) nor vacuum (−1). It is the effective w during the matter→Λ transition, so a
thermodynamic κ = 1/2 would be a transient coincidence of one brief epoch — the definition of an accident.

### 9. Verdict and the one-line derivation that fails

**κ = 1/2 is not derivable from horizon thermodynamics.** The nearest one-line derivation is

    κ = λ Z/2  with  λ = (1+3w)/2   ⇒   κ_dust = Z/4 = 1.447203   (not 1/2),

i.e. "the first law's dust-era coefficient 1/2, transported to the acceleration scale, gives Z/4". To get 1/2
one must instead write `κ = λ` — the assumption restated — or insert `1/Z` by hand.

**The exact obstruction.** The unmatched term is the **temperature normalisation λ**: the first law matches
`T dS` to `dE + P dV` only up to `λ = (1+3w)/2`, and there is no term in either side that references `a0`,
`ρ_bare`, or κ. Formally the first law is a map `(H, ρ, w) → λ`; κ is not in its domain (K11). The physical
input needed is **not** a better entropy or temperature — it is the identification `a0 ↔ horizon acceleration`
together with its normalisation `√(3/8π)`, i.e. the Einstein `ρ_bare = ρ_crit` postulate — the same input
Lane A1 identified as underivable, arriving here by a different route.

**Third independent failure mode.** A1's obstruction was algebraic (one free function of `x = ħGΛ/c³`); this
one is structural (κ outside the functional domain). They agree, and neither supplies what A1 named as the
missing premise: an integer count `n = 1/κ = 2`. Note where the 2 lands here: `1/λ_dust = 2` exactly (K3) — the
integer A1 wanted — but as the reciprocal of a *temperature* coefficient. Inverted into κ it gives κ = 2, which
is 4× the canonical value and not even a ladder member. The thermodynamic route produces the right integer in
the wrong slot.

### 10. Does the thermodynamic route predict anything different?

Yes, one thing, and it is fatal rather than helpful: **the thermodynamic coefficient runs with w.** A
thermodynamic κ would be epoch-dependent, with `κ_rad/κ_dust = 2` (λ = 1 vs 1/2), whereas the algebraic route's
κ is a constant. The theory's κ is constant by P3. So the thermodynamic reading either (i) yields a running κ,
contradicting P3, or (ii) yields a constant κ only by freezing w, in which case its value is Z/4 = 1.447203 and
a0 is 2.894× too large. No viable new prediction distinguishes it from the algebraic route; the distinct
prediction it does make is excluded by the RAR scale. Otherwise it reproduces A1's ladder exactly (Z/4, Z/2),
so it adds no new number — only a thermodynamic reason for where the ladder sits, and an independent proof
that κ is not on it.

## Status

**NO-GO(obstruction).** Sub-results: §2 (K1, K2), §4 (K4), §5 (K7–K10, K17), §7 (K12, K14) are **DERIVED**
exact identities/values. §3 (K3) DERIVED: the first law closes iff w = 1/3. §6 (K11) is the NO-GO: κ is not an
argument of any horizon functional. §8–§9: the honest identification gives Z/4, and κ = 1/2 requires
`λ = 1/Z`, i.e. `w* = −0.2182`. The missing premise, named exactly: **the map a0 ↔ horizon acceleration and its
Einstein normalisation √(3/8π) = 2/Z** — equivalently, P3's `ρ_bare = ρ_crit`, an input, not a thermodynamic
consequence.

## Checks (a50_checks.py, 17/17 PASS, exit 0, 1.0 s, cold start verified under `env -i`)

| id | proves | value |
|---|---|---|
| K1 | `T dS = (c⁴/G)dr_A` exactly | residual 0.0e+00, ratio 1.000000000000000 |
| K2 | λ ≡ (dE+PdV)/(TdS) = (1+3w)/2, Ḣ-independent | λ(0)=0.5, λ(1/3)=1.0, ∂λ/∂Ḣ=0 |
| K3 | literal law closes iff w=1/3; dust fails by 2; vacuum 0=0 | w=1/3, factor 2.000, λ(vac)=−1 |
| K4 | no constant λ fits all epochs | spread 2.25 over w∈[−1,1/2] |
| K5 | law fixes λ, not Ḣ; G_eff = 2G for dust | residual 0, ∂/∂Ḣ 0, G_eff/G=2.000000 |
| K6 | numeric FRW: T dS = 2 dE while T·S = E | 2.000000000032 and 1.000000000000 |
| K7 | naive equipartition ratio = 1/2 at ρ_crit | 0.500000000000000 |
| K8 | Komar equipartition ratio = 1 at vacuum | 1.000000000000000 |
| K9 | one formula (1/2)\|1+3w\|(ρ/ρ_crit) covers both | residual 0 |
| K10 | N_surf = N_bulk ⟺ ρ = 3H²/8πG (= P3) | ρ_sol = 3H²/(8πG) |
| K11 | κ, a0 absent from every horizon functional | True, drift 1.7e-16 over 400 κ |
| K12 | κ=1/2 ⟺ a0/(cH) = 1/Z exactly | 0.172747074735668, identity residual 0 |
| K13 | no physical coefficient gives κ=1/2 | min\|κ(cand)−1/2\| = 0.2236 (κ=0.7236 from λ=1/4) |
| K14 | factor is √(3/8π)=2/Z, not 2√(32π/3) | all four identities residual 0 |
| K15 | "1/2 × 2√(32π/3)" overshoots by 33.5× | 33.510322 |
| K16 | honest identification gives Z/4; κ=1/2 needs w* | κ_A=1.447202509, w*=−0.218168617 |
| K17 | efficiency at the horizon is 1/(1+Z), not 1/2 | 0.1473012; half-share needs κ=2.894405 |

Mutation control: `--mutate=m1` (λ forced constant) breaks K3, K4, K5 → 14/17; `--mutate=m2` (naive energy in
the Komar slot) breaks K8 → 16/17; `--mutate=m3` (wrong geometric factor in the κ map) breaks K12 → 16/17.
All three exit 1. See MUTATE.md.

## What this does not do

- Does not prove κ ≠ 1/2 in nature. It proves κ = 1/2 is outside the reach of the first law of horizon
  mechanics as written, for the reasons in §6 and §9.
- Does not use the full non-equilibrium entropy-production term. The equilibrium form was imposed; a
  non-equilibrium `dS = dS_eq + d_iS` would add a term to (2.2) and could in principle change λ — but the
  added term is unconstrained here and cannot manufacture κ, since κ is still absent from the domain (K11).
- Does not go beyond a perfect fluid with constant w. The corpus's cold sector is collisionless, not a single
  perfect fluid; a w(z) treatment would make λ redshift-dependent but would not introduce κ.
- Does not run any data fit (the 2.894× is a comparison to the quoted RAR scale, not a likelihood), and does
  not touch Lane A1's algebraic no-go, its `1/12` arithmetic, or the turn-off `y_t` question.

## Next

1. The one place a κ could still hide is a **non-equilibrium entropy production** term with a coefficient fixed
   by the theory's own transport (the cold sector's `div P = ρ − ρ̄`). That would put a new functional argument
   into (2.2); the test is whether its coefficient is `1/Z` rather than O(1). Nothing in the corpus fixes it.
2. The `w* = −0.2182` result is a sharp, if unwelcome, prediction: any thermodynamic derivation of κ = 1/2 must
   either produce that equation of state or explain why the first law is evaluated at w = 0 while the
   acceleration is set today. Worth checking against the corpus's `w(z)`.
3. Reading (A) predicts a0(Z/4) = 3.2742e-10, excluded by 2.894× — a clean falsification of "κ is the
   first-law coefficient", independent of any κ prior. Worth recording as a closed door in the κ ledger.