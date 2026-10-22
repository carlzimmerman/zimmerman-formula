# A62 — WHY THE VACUUM SWITCHES AT ONE TWELFTH OF THE HORIZON SCALE

Lane A62. `a62_checks.py` — 25 checks, **25/25 PASS**, exit 0, 0.7 s, deterministic, no network,
stdlib + numpy + scipy + sympy; `a62.out` is its stdout and `a62_results.json` holds every number
below. Constants: BRIEF §4 (c, G, ħ CODATA, k_B, Λ, H0, a0_can, Mpc); nothing fitted.
Read first: A1 (report + A8 Lean), A27, A34. A1's results, used throughout: 2Z = √(128π/3) =
11.577620 is irrational, so no integer count works; the literal "1/12" gives κ = Z/12 = 0.4824008
(3.52 % below ½); and a0/(cH0) = 1/7 to 5.6e-4. A1 closed counting, dimensional analysis, strain
saturation (4√(π/3), 8.19× off), and the dimension route. This lane asks what A1 left open: why
1/(2Z)?

## Claim

**11.5776 is not a coefficient of nature. It is `2Z = Z/κ` with κ = ½ — the Einstein 8π/3 times
a square root times two 2's — so "why 11.5776" is exactly "why κ = ½" (A1, A27, A34, now confirmed
from the energy-balance side rather than from counting).** None of the three named routes produces
it. Route (a), horizon-capacity saturation of the vacuum stress, is **algebraically the Friedmann
equation** and returns `a_crit = cH` exactly, i.e.
κ = Z/2 = **2.894405** (5.79× the canonical value, empirically dead); the field's *own*
zero-point stress instead saturates at the **Planck acceleration** (4.458e61 × cH), and a
conformal field at **0** (conformal vacuum) or 1.67e-63 (anomaly). Route (b), holographic
equipartition, is also identically Friedmann, so its deficit is **zero in de Sitter by
construction**; it returns the surface gravity cH (κ = 2.894), or, in its volume-law variant,
the integer **6** — which is 2√(8π/3) *with π replaced by 27/8*, the same substitution that turns
2Z into 12. Jacobson's Clausius route is the same Einstein equation again: the only acceleration
it supplies is the horizon surface gravity, so it returns 1 (κ = 2.894), 2Z times the target.
Route (c), a Langevin/Brillouin medium with a quantum carrier, returns **exactly cH/2π**
(κ = Z/4π = **0.460659**, 7.87 % below ½) and fails on *shape* (analytic slope 1, not the
deep-MOND ½). The exact Langmuir gate the theory uses has its scale at the capacity a0, so it
returns a0/(cH_Λ) = **1/Z = 2 × 1/(2Z)**, exactly twice the target — the factor 2 is the
radius/diameter convention, and a0 itself is an input. **Look-elsewhere: 223 closed forms lie within 1 % of 11.5776** in a 156 210-value
pool, the simplest being **√134 (2 symbols, 1.5e-4)** — so even before the derivation question, a
match is not evidence. Exact arithmetic: `2cH_Λ/a0 = Z/κ` identically; κ = ½ ⟺ a0/(cH_Λ) = 1/Z
⟺ a0/(2cH_Λ) = 1/(2Z); "1/12" is exact **iff π = 27/8**; and a0/(cH0) = √Ω_Λ/Z, so A1's 1/7 hit
is the statement Ω_Λ = 32π/147. Status: **NO-GO(obstruction)**.

## Derivation

Symbols: Λ > 0; H_Λ = c√(Λ/3); Z := 2√(8π/3); a0 = κc√(Gρ_Λ); R := c/H_Λ; ℓ_P² = Għ/c³;
T_dS = ħH/2πk_B; S_dS = k_BA/4ℓ_P²; g := 2cH_Λ/a0. Two inherited errata are corrected in §1.2–1.3.

### 1. Exact arithmetic — the whole content of 11.5776

**(1.1) One number, four dresses (K1, exact).** `2√(32π/3) = 4√(8π/3) = 8√(2π/3) =
√(128π/3) = 2Z = 11.577620073`, all four symbolic residuals 0; the 4 under the root is the only
content and it is exact (32 = 4·8).

**(1.2) The ratio law (K2, exact).** With `a0 = κc√(Gρ)` and `H² = 8πGρ/3`,

    (2.1)  g ≡ 2cH_Λ/a0 = Z/κ = 5.788810/κ ,   hence κ = Z/g  —  identically.

κ = ½ ⟺ g = 2Z = 11.5776: **the answer to "why 11.5776" is that it is Z divided by κ**, the 2 in
the numerator being the diameter/radius convention that A27 showed carries no information.
*Erratum inherited from A1 eq. (2.1):* it prints `κ = (Z/2)/g`, contradicting its own (2.2)–(2.3),
which use κ = Z/g (g = 12 → κ = Z/12 = 0.4824008); (2.1) is a typo.

**(1.3) The three normalisations (K3, K4, K23, exact).**

    (2.2)  κ = ½  ⟺  a0/(cH_Λ) = 1/Z = 0.1727471  ⟺  a0/(2cH_Λ) = 1/(2Z) = 0.0863735
                  ⟺  a0 = c²√(Λ/32π) = 9.354173e-11 m/s².
    (2.3)  a0/(cH0) = √Ω_Λ/Z = 0.142937 (1/7 = 0.142857, rel 5.62e-4);  = 1/(2Z) ⟺ Ω_Λ = 1/4.
           1/7 exactly ⟺ Ω_Λ = 32π/147 = 0.683884, vs the BRIEF's Ω_Λ = 0.68380 (0.01 %).

So **the task's "a0/(cH0) = 1/11.5776" is false as written**: 1/(2Z) is a0/(2cH_Λ) at κ = ½
(equivalently a0/(cH_Λ) at κ = ¼), while a0/(cH0) is 1/7, a statement about Ω_Λ.
*Erratum inherited from FINAL_THEORY §1:* the chain `a0/(cH_Λ) = κ√(3/8π) = (κ/2)√(8π/3) =
1/(2Z)` is false in its second and third links: κ√(3/8π) = 2κ/Z, and at κ = ½ it equals
**1/Z = 0.172747**, twice 1/(2Z). BRIEF §1 and `A8.a0_over_cH_eq_inv_two_sqrt` are right; the
theory document is not (K23).

**(1.4) "One twelfth" is exact iff π = 27/8 (K5, K6).** `2Z = 12 ⟺ 8π/3 = 9 ⟺ π = 27/8 = 3.375`
(a rational; |π − 27/8| = 0.2334, so it is false by Lindemann, not by rounding). The Lean bracket
`1/12 < 1/(2Z) < 1/11` is exactly `363/128 = 2.83594 < π < 27/8` — a window 0.54 wide, i.e. it
certifies only that 1/12 sits 3.65 % below 1/(2Z). The gap is exactly
`1/(2Z) − 1/12 = (6 − Z)/(12Z) = 3.0402e-3`. Reading 2Z ≈ 12 is therefore the substitution
**π → 27/8**, nothing else. And a0 = 2cH_Λ/12 puts the MOND length at `L = c²/a0 = 6R` — **six
horizon radii**, not one twelfth of one.

**(1.5) Transcendence, not merely irrationality (K19).** `(2Z)² = 128π/3`; were 2Z algebraic, so
would be π = 3(2Z)²/128, contradicting Lindemann — so κ = ½ is unreachable by any exact counting
argument (A1's no-go, strengthened).

### 2. Route (a) — QFT in curved spacetime: saturation against horizon capacity

**(2.1) The capacity (K7, exact).** An acceleration a defines a Rindler horizon at L_a = c²/a with
T_U = ħa/2πck_B and S_U = k_BA/4ℓ_P², A = 4πL_a²:

    (3.1)  E_cap(a) = T_U S_U = c⁶/(2Ga)      [= ħ a/(2πc k_B)·πk_Bc⁷/(Għa²) — exact]
    (3.2)  E_vac(a) = ρ_vac c² (4π/3)(c²/a)³
    (3.3)  E_vac = E_cap  ⟺  a² = (8πG/3) ρ_vac c²  ⟺  κ_route = a/(c√(Gρ)) = √(8π/3) = Z/2.

**(3.3) is algebraically the Friedmann equation with H → a/c**: it says "the vacuum saturates
where the acceleration horizon encloses the critical density for its own expansion rate a/c", so
the criterion has no independent content. With ρ_vac = ρ_Λ: `a_crit = cH_Λ = 5.414953e-10 m/s²`,
i.e. **κ = Z/2 = 2.894405**, a0 5.79× the canonical value (26σ against the measured
κ = 0.417 ± 0.095, A15). The result is independent of the solid angle used for (A, V) — both scale
as L², L³ and the cone factor cancels — but it cannot be pushed to ½: κ = ½ needs the capacity to
be **1/Z² = 3/32π = 0.029842** of T_U S_U, i.e. an effective entropy `A/(4Z²ℓ_P²) = A/(134.0 ℓ_P²)`
instead of A/4ℓ_P². That is the target restated, not derived.

**(2.2) The field's own zero-point stress (K10).** Cutting the modes at the Rindler scale
k_max = a/c², ρ_zp = ħc k_max⁴/16π² = ħa⁴/(16π²c⁷); the same balance (3.3) then gives

    (3.4)  a_crit = √(6π) c²/ℓ_P = 2.414e52 m/s²,  a_crit/(cH_Λ) = 4.458e61   (m ≪ m_P),

mass-independent for every sub-Planckian mass, and `9πc⁴/(2Gm)` above it. (The general case is
the standard zero-point integral with cutoff k_max = a/c² and mass μ = mc/ħ; (3.4) is its μ → 0
limit.) The target 1/(2Z) is reached only at **m = 1.68e63 m_Pl = 3.3e63 GeV** — a black hole
larger than the horizon.

**(2.3) The conformal field (K9).** A conformally coupled massless field in the conformal vacuum
has ⟨T_μν⟩ = 0 identically: **no stress, no saturation, no critical acceleration at all**. The trace
anomaly is ρ = c_a H⁴ with c_a = O(1/2880π²), giving a_crit/(cH) = 1.672e-63: the conformal case is
not a near miss, it is a different power of H.

**Route (a) verdict:** the ratio is either **1** (capacity with the dS density; κ = 2.894) or
**4.5e61 / 1.7e-63** (the field's own stress). 1/(2Z) = 0.0864 appears nowhere except through a
tuned mass. The reason is structural: (3.3) is a *linear* energy balance, so a² ∝ Gρ and the
square root cancels, leaving κ² = (8π/3)λ with λ a rational bookkeeping number.

### 3. Route (b) — horizon information limits: equipartition and Clausius are Friedmann

**(3.1) The identity (K11, exact).** N_sur = A/ℓ_P² = 4πc⁵/(GħH²); N_bulk = 2E_K/k_BT with the
Komar energy E_K = (ρ+3P)V and T = ħH/2πk_B:

    (4.1)  N_bulk = (32π²/3) ρc⁵/(ħH⁴)   ⟹   N_sur = N_bulk ⟺ H² = 8πGρ/3  (residual 0).

Holographic equipartition **is** the Friedmann equation, so it cannot fix an acceleration: it holds
identically on every Friedmann background. The deficit N_sur − N_bulk is zero for pure Λ (K12:
3e-16) and, for matter+Λ, `1 − ½|3Ω_m − 2|`:

    (4.2)  ΔN/N_sur = 0 (dS);  = 0.4743 at Ω_m = 0.3162.

Turning the deficit into an acceleration needs a normalisation, and the only one available is
a_Δ = cH·ΔN/N_sur — a *choice*, which is the point. It gives **0.4743 cH0** at the measured Ω_m
(5.49× the target) and needs **Ω_m = 0.0576** to equal 1/(2Z), i.e. 37σ from 0.316 ± 0.007: the
deficit is not a vacuum quantity at all, it is a function of Ω_m vanishing at Ω_m = 0 and 4/3.

**(3.2) The coefficient, and where 6 comes from (K13).** The scale the equipartition *does* supply
is the surface gravity, a0 = cH → **κ = Z/2 = 2.894405**. The volume-law variant (Verlinde 2016,
a0 = cH0/6) gives κ = (Z/12)(H0/H_Λ) = **0.583369** — one of the four κ values circulating in the
record (A15). And the integer 6 is not innocent: `6² = 36 = 4·(8π/3) ⟺ π = 27/8`. So the folklore
pair (6, 12) is one substitution, **π → 27/8**, applied once and twice.

**(3.3) Jacobson's Clausius route (K24, exact).** On a local Rindler horizon at proper distance
L, the surface gravity is a = c²/L, the Unruh temperature T = ħa/(2πck_B), and the entropy is
S = k_BA/(4ℓ_P²). The Clausius relation dQ = T dS with the matter heat flux is Jacobson's
derivation of Einstein's equation. The acceleration it supplies is not a new scale: substituting
A = 4πL² gives T dS = ħc dL/ℓ_P², independent of a, and the only acceleration in the problem is
the horizon's own surface gravity. For the Hubble horizon L = c/H,

    (4.3)  a_Jacobson = cH,  a/(cH) = 1,  κ = Z/2 = 2.894405,  a/(cH) = 2Z × 1/(2Z).

So the Jacobson route gives coefficient **1**, 11.58× the target, exactly as the capacity route.

**Route (b) verdict:** coefficient **1** (surface gravity, deficit-free dS; also Jacobson's
Clausius route), **0.4743** (deficit at our epoch) or **1/6** (volume law) — none is
1/(2Z) = 0.0864.

### 4. Route (c) — saturating media: Langevin, Brillouin, Langmuir

**(4.1) The scale (K14, exact).** A saturating medium saturates when the field does work k_BT over
the carrier's dipole length; for a quantum carrier the only length available is the Compton length
ℓ = ħ/mc, so

    (5.1)  a_sat = k_BT/(mℓ) = k_BT_dS·c/ħ = cH/2π = 0.159155 cH   — mass-independent,

i.e. **exactly** the Unruh-equals-de-Sitter condition (a = 2πT_dS). In κ units κ = Z/4π =
**0.460659**, A1's "Milgrom entry", 7.87 % below ½ (the familiar 8.5 % tension). A Brillouin
two-level medium P = P_max tanh(pE/k_BT) has the same pE ~ k_BT condition, hence the same scale
a_sat = k_BT/p = cH/2π.

**(4.2) The shape fails before the scale can matter (K15).** Langevin L(x) = coth x − 1/x and
Brillouin tanh x are analytic at the origin: d ln A/d ln x = **1** for both, with Langevin
A ≈ g_N/3 and Brillouin A ≈ g_N, i.e. Newton with a renormalized G_eff (1/3 or 1). The framework
needs d ln A/d ln g_N = **½** (A = √(a0g_N)), which is non-analytic. No
Langevin/Brillouin medium reproduces MOND even qualitatively; the framework's gate is the exact
Langmuir isotherm θ(x) = x/(1+x) (A63), whose scale is the capacity A_max = a0 — an input.

**(4.3) The exact Langmuir gate (K25, exact).** The theory's gate is the Langmuir isotherm
θ(x) = x/(1+x) with x = a/a0 (A63). Half occupancy is at x = 1, so the natural scale is the
capacity a0 itself. At κ = ½, a0/(cH_Λ) = 1/Z, hence

    (5.2)  a_Langmuir/(cH_Λ) = a0/(cH_Λ) = 1/Z = 0.172747 = 2 × 1/(2Z).

The coefficient is **1/Z**, exactly twice the target; the factor 2 is the same radius/diameter
convention that separates 1/Z from 1/(2Z). The capacity a0 is an input, not an output.

**Route (c) verdict:** ratio **1/(2π) = 0.159155** (= 1.8426 × 1/(2Z)) for Langevin/Brillouin,
**1/Z = 0.172747** (= 2 × 1/(2Z)) for the exact Langmuir gate. The scale k_BT/p has two free
parameters; only the quantum-carrier identification makes it universal, and that lands on
Milgrom's number, not on κ = ½.

### 5. Look-elsewhere: 223 hits, and a 2-symbol rival

Pool: closed forms from π, e, small integers and √ (families k·π^p·e^q, k√n·π^p, k√(nπ/m),
√(kπ^p e^q), integer offsets ±1..3, and reciprocals), deduplicated by value — **156 210 distinct
values** (K16). The full 223-entry list is written to `a62_results.json` under
`lookelsewhere_all_1pct_hits`.

| window | 1 % | 0.1 % | 0.01 % |
|---|---|---|---|
| hits near 2Z = 11.5776 | **223** | 37 | 18 |

The simplest hits are `√134 = 11.575837` (**−1.54e-4, two symbols**), `√135 = 11.618950` (+3.6e-3)
and `√133 = 11.532563` (−3.9e-3): **√134 matches 11.5776 to 1.5e-4 — 240× tighter than the integer
12 does — with a third of the symbols** (K16). Calibration (K17): 300 random reals in [8,16] give
236.5 ± 12.7 hits at 1 % against the target's 223, **z = −1.06**, so 11.5776 is not distinguished
by the pool at all. The same holds for every ratio in play (K18: 1/(2Z) 223, 1/Z 241, 1/7 243,
1/6 248, 1/(2π) 258 hits), and even in the target's own shape k√(nπ/m) **9** members are within
1 % — "exactly one closed form matches" is false in every family tested.

### 6. What would be needed

The target is the pure number `1/(2Z) = √(3/128π) = 0.0863735`, whose square is 3/128π. Every
principle in the tested class is a *linear* energy balance, and a linear balance gives
κ² = (8π/3)λ with λ rational (1 for the Bekenstein capacity, 4 for A/ℓ_P², ½ for one degree of
freedom). κ = ½ needs **λ = 3/(32π) = 1/Z²**, irrational: the balance must contain 1/π, i.e. it
cannot be a balance at all. Concretely, per route:

| route | number it must insert to reach κ = ½ |
|---|---|
| (a) capacity | ρ_sat/ρ_Λ = 1/Z² = 3/32π = 0.029842 (S = A/134ℓ_P², not A/4ℓ_P²) |
| (b) deficit | ΔN/N_sur = 1/(2Z) = 0.086374 ⇒ Ω_m = 0.0576 (measured 0.316) |
| (b) Jacobson | the only scale is cH, so it gives 1; reaching 1/(2Z) needs a factor 1/(2Z) = 0.0864 inserted |
| (c) carrier | tuning by Z/π = 1.8426 (Langevin/Brillouin: 1/(2π) = 1.8426/(2Z)) |
| (c) Langmuir | the capacity is a0, so it gives 1/Z = 2 × 1/(2Z); needs a0 = cH/2 |

Equivalently, in length: a0 = c²/(2ℓ₀) with ℓ₀ = √(8π/Λ) is an identity of the theory
(K21, residual 0), so κ = ½ is exactly the statement `L = c²/a0 = 2ℓ₀ = Z r_H` — the MOND length is
the **diameter of the Euler cell** (A27's candidate iii, a renaming). What is missing is a
**variational principle quadratic in a0** whose stationarity gives `Λc⁴/a0² = 32π = 8π·4`
(8π from G, 4 from κ²) and which is *not* a total derivative in a0 — the failure mode A19 found
for the Euler charge. No such functional exists in the class tested here, and the three named
physical principles all replace the square root with a linear balance.

## Status

**NO-GO(obstruction).** §1 **DERIVED** (exact identities; two errata corrected); §2 **NO-GO**
(capacity saturation = Friedmann → κ = Z/2; the field's own stress → Planck acceleration;
conformal → 0); §3 **NO-GO** (equipartition = Friedmann, deficit ≡ 0 in dS → 1; Jacobson → 1;
volume law → 6); §4 **NO-GO** (Langevin/Brillouin exactly 1/(2π), Langmuir exactly 1/Z = 2×1/(2Z),
wrong shape/scale); §5 **NO EVIDENCE** (223 hits, √134 simpler and closer). The number
11.5776 remains **unexplained**, for the same reason as κ = ½: it *is* κ = ½.

## Checks (a62_checks.py, 25/25 PASS, exit 0, 0.7 s)

- K1 four closed forms of 11.5776 identical (residuals 0); K2 `2cH/a0 = Z/κ` exact, κ = Z/g;
  K3 κ=½ ⟺ a0/(cH)=1/Z ⟺ a0/(2cH)=1/(2Z) ⟺ a0 = c²√(Λ/32π), residuals 0; K4 a0/(cH0) = √Ω_Λ/Z,
  1/7 ⟺ Ω_Λ = 32π/147 (0.01 %), 1/(2Z) ⟺ Ω_Λ = 1/4
- K5 2Z=12 ⟺ π = 27/8 (solved exactly); K6 A8 bracket ⟺ 363/128 < π < 27/8, gap (6−Z)/(12Z);
  K19 (2Z)² = 128π/3 ⟹ transcendental; K23 FINAL_THEORY §1 erratum proved symbolically
- K7 E_cap = c⁶/(2Ga) exact, balance ⟺ a² = 8πGρc²/3; K8 κ_route = Z/2 = 2.894405, a = cH,
  ρ_sat/ρ_Λ = 3/32π; K9 conformal 0 / 1.672e-63; K10 massive 4.458e61, crossing at 1.68e63 m_Pl
- K11 equipartition ⟺ H² = 8πGρ/3 (residual 0, N_bulk/N_sur = 1.000000000000); K12 deficit 0 in
  dS, 0.4743 at Ω_m = 0.3162, target needs Ω_m = 0.0576; K13 κ(cH) = 2.894, κ(cH0/6) = 0.583369
- K14 a_sat = cH/2π exact, mass-independent; K15 slopes 1, 1, ½ and amplitude 1/3;
  K16 pool 156 210, 223 within 1 %, simplest √134; K17 z = −1.06 vs 300 random targets;
  K18 every candidate ratio has ≥ 223 hits
- K20 κ set {2.894, 2.894, 0.583, 0.461} vs ½; K21 a0 = c²/(2ℓ₀) exact, ℓ₀ = (Z/2)R;
  K22 the three inserted numbers 3/32π, 1/(2Z), Z/π
- K24 Jacobson dQ = T dS: T dS = ħc dL/ℓ_P² (no acceleration scale), a = cH, κ = Z/2,
  ratio to 1/(2Z) = 2Z; K25 Langmuir θ = x/(1+x): half occupancy x = 1, a_sat = a0,
  a0/(cH_Λ) = 1/Z = 2 × 1/(2Z)

Mutation control: `--mutate=m1..m5` breaks only its targets and prints MUTATION CONFIRMED; MUTATE.md.

## What this does not do

- Does not prove no principle can produce 1/(2Z). It proves four classes cannot: linear
  energy-capacity balances (κ² ∈ ℚπ), holographic deficit arguments (deficit ≡ 0 in dS), analytic
  saturating media (slope 1), and horizon counting (A1).
- Uses the sharp-cutoff zero-point estimate and the anomaly's order of magnitude, not a
  renormalised Bunch–Davies ⟨T_μν⟩ for arbitrary m/H; interacting fields, strong coupling and
  back-reaction are not tested.
- Quotes Verlinde's 1/6 rather than re-deriving it; only its relation to Z (6/Z = 1.0365 ⟺ π = 27/8)
  is used. The hit count is pool-dependent; the ordering by description length is not.
- Does not re-fit a0 or adjudicate the alt footing; a0_can is BRIEF §4, and its 3 s.f. rounding is
  why a0_can/(cH_Λ) = 0.172855 rather than exactly 1/Z.

## Next

1. **The only surviving shape** is a variational functional quadratic in a0 whose stationarity
   gives Λc⁴/a0² = 32π and which is not a total derivative in a0 (A19's failure mode). Everything
   else in this lane reduces to a linear balance, and a linear balance cannot carry 1/π.
2. **Fix the two errata before the register is built on them**: A1 eq. (2.1) should read κ = Z/g;
   FINAL_THEORY §1's `(κ/2)√(8π/3) = 1/(2Z)` should read `2κ/Z = 1/Z`. The Lean file and BRIEF §1
   are already correct, so the certificate and the prose currently disagree. Register wording:
   "1/(2Z) = 1/11.5776 of the *doubled* horizon", which in length is L = 6R.
3. **Discriminator**: route (c)'s κ = Z/4π = 0.4607 is 7.87 % below ½, so σ(κ)/κ ≤ 2.85 % separates
   them at 3σ — A1's test against the Milgrom menu entry, here also against the only close route.