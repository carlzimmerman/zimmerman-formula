# A15 — is κ = ½ DERIVED, an IDENTITY, or a DIFFERENT QUANTITY?

**Verdict: `DIFFERENT-QUANTITY`** — with the sub-finding that the quantity GF2 computes is *also* an
identity (the normalisation `C` cancels). Backed by `a15_checks.py` (15 checks, 15/15 PASS, exit 0),
`a15.out`, `a15_results.json`. Both records are read, not paraphrased:

- **GF2** = `deepseek_push/GF2_closure_half/` (README, STATE, script), refereed in
  `qwen38_push/Q010_kappa_referee/`.
- **CFG908** = `campaign_fresh_gravity/CFG908_kappa_derived_claims_audit/` (its C1 row is the one at issue).

## Claim

The GF2 chain is algebraically exact: from Φ = C ln r it derives ρ = C/(4πG)r⁻², γ = 2, σ² = C/2 and
v_flat² = C, with no number imported — all confirmed at residual zero (K1). But the number it produces is

    µ := σ²/v_c² = 1/2 ,  the singular-isothermal-sphere ratio,

and **not** the law's `κ := a₀/(c√(Gρ_DE))`. The two cannot be the same object, and not merely because
the proof is missing: the chain's solution set carries a one-parameter symmetry under which µ is
invariant and κ_law has weight 1 (K9). No function of µ equals κ_law on that set. GF2's algebra and
CFG908's classification are both right; the error is GF2's *register line* ("κ = ½: DERIVED"), and
Q010's own text already concedes the junction ("rung 5, POSTULATED-CARRIED") — which is the same
statement in softer words.

## Derivation

Every symbol: `C` = normalisation of the log potential ([C] = velocity²), `σ²` = isotropic velocity
dispersion, `v_c²` = circular velocity squared, `a₀` = the law's acceleration scale,
`ρ_DE` = ρ_Λ = Λc²/(8πG), `s_DE := c√(Gρ_DE)`, `Λ` = cosmological constant, `ℓ₀ := c²/a₀`.

### 1. The GF2 chain, rebuilt

    (1)  P1  Φ(r) = C ln r                                        [committed static branch]
    (2)      ∇²Φ = (1/r²) d/dr (r² Φ′) = C/r²                      [exact]
    (3)  P2  ∇²Φ = 4πGρ  ⇒  ρ = C/(4πG) r⁻² ,  d lnρ/d ln r = −2   [γ = 2, exact]
    (4)  P3  σ² d lnρ/dr = −dΦ/dr                                  [static, isotropic, σ² const]
    (5)      σ²(−2/r) = −C/r  ⇒  σ² = C/2                          [exact]
    (6)      v_c² = r dΦ/dr = C                                    [exact at every r]
    (7)      κ_dyn := σ²/v_c² = (C/2)/C = 1/2                      [exact — and C cancels]

**Answer to (a) — where σ² = C/2 comes from, in three parts.**

- **It is the Jeans equation.** (4) is the radial Jeans equation of a spherical, static, isotropic
  system with constant dispersion; equivalently the hydrostatic equation of a fluid with the isothermal
  EoS P = ρσ². It is not an entropy argument, not a virial theorem, not an ensemble average.
- **It is not a boundary condition at the origin.** Nothing is imposed at any radius or density. The
  general solution of (4) with σ² free is `σ²(r) = C/2 + K r²` (K2) — one free constant, a radial
  temperature gradient. `C/2` is the member with `K = 0`, i.e. the member whose dispersion does not run;
  the condition used is *global isothermality*, which is premise P3 restated, not an output.
- **It is not a definition of v_flat** — (6) follows from P1 — but the *final* step (7) is a definition:
  κ_dyn is defined as that ratio and then evaluated where both terms are the same `C`. Two occurrences of
  one constant cancel; what remains is the statement `v_c² = 2σ²`, the SIS identity.

**The premise list, complete.** P1 log branch; P2 Newtonian Poisson with the Λ-force dropped; P3 steady state,
spherical symmetry, β = 0, σ² r-independent, P = ρσ²; P4 identification of P/ρ with the tracer
dispersion; P5 v_flat² = C. **None of the five mentions a₀, c or ρ_DE.** That is the finding.

### 2. The uniqueness lemma — tested, and it cuts both ways

GF2's qualified statement: *among power laws with constant σ², γ = 2 is the unique self-sourced
hydrostatic equilibrium.*

With Φ_p = C r^p/p (p = 0 ↦ C ln r): ρ_p = C(p+1)/(4πG) r^(p−2), and the dispersion required by (4) is
`σ²_req(r) = C r^p/(2−p)`, which is r-independent iff p = 0, and the closure defect at σ² = C/2 is
`R(p,r) = C(p + 2r^p − 2)/(2r)` — at r = 1 it is C p/2, zero only at p = 0. Brute force over 2001 values of p on
[−2.5, 2.5]: **exactly one** winner, p = 0; off p = 0 the isothermality defect exceeds 2.811e−2 for
|p| > 0.01; the continuum condition d/dr[C r^p/(2−p)] = −C p r^(p−1)/(p−2) has the single root p = 0 (K4).
The lemma is **true as qualified**.

Two things it does not do:

- **(i) Unqualified, it is false** (K5). The cored isothermal sphere — the regular solution of
  ψ″ + 2ψ′/x = e^(−ψ) — is an exact self-sourced hydrostatic equilibrium with constant σ² whose density is
  nowhere a power law (log-slope −3.333e−5 at x = 0.01, → −1.992 at x = 400, integral-form residual
  4.1e−6). There is a whole one-parameter family of such counterexamples. GF2's README says "among
  power-law configurations"; the shorthand "γ = 2 is the unique self-sourced hydrostatic equilibrium"
  drops the qualifier that carries the proof.
- **(ii) It selects a shape, not a coefficient.** For any p ≠ 0 the configuration is still in equilibrium
  if σ² is allowed to run (K2). What forces p = 0 is the *constancy of σ²*. The lemma therefore says
  "the isothermal sphere is the only power-law isothermal sphere" — a consistency statement.

### 3. Two further premises hidden in the ½

- **Isotropy** (K6). With constant anisotropy β the same Jeans equation on the same log branch gives
  σ_r² = C/(2(1−β)), hence κ_dyn = 1/(2(1−β)): 0.333 at β = −0.5, 0.5 at β = 0, 0.833 at β = 0.4,
  1.0 at β = 0.5. Real halos have β ≈ 0.2–0.4, so the halo-internal number is 0.625–0.833. Even as a
  statement about halos, ½ is the isotropic idealisation.
- **Λ = 0** (K10). With Λ, Φ = C ln r − Λr²/6 keeps the SIS density exactly (∇²Φ = C/r² − Λ = 4πGρ_m − Λ),
  but the force gains +Λr/3, so the isothermal balance leaves the residual −Λr/3. At 10 kpc that is
  1.2e−22 of the force: numerically irrelevant, *logically* fatal — the chain is exact only in the limit
  ρ_Λ → 0, i.e. exactly where κ is undefined. The information about ρ_DE lives in the term GF2 discards.

### 4. Why the output cannot be the law's κ

- **Renaming (K7).** Set κ_law = 2/5. The chain returns ½, unchanged. A derivation of κ_law would have to
  move, or fail, under the rename. CFG908's T1b reproduced exactly.
- **Symbol audit (K8).** The chain's free symbols are {C, C₁, G, β, r}. The intersection with
  {a₀, c, ρ_DE, κ_law, Λ, ρ_Λ} is empty. ρ_DE occurs 0 times in GF2's README/STATE (135 lines scanned);
  the vacuum coupling appears only as border-3, "OUT of scope".
- **Scaling — the proof (K9).** Substitute (a₀, C, σ², v²) → (µa₀, √µ C, √µ σ², √µ v²) at fixed M_b and
  ρ_DE. Every chain equation is invariant (residuals 0); κ_dyn is invariant (½ → ½); κ_law → µ κ_law.
  On one and the same solution set, therefore, κ_dyn is constant while κ_law ranges over all positive
  values. No function of κ_dyn can equal κ_law. κ_law is a **modulus** of the theory — the halo sector
  cannot see it, by construction.
- **The dilemma (K12).** Tie a₀ = k_tie·c√(Gρ_DE). Horn A: dκ_dyn/dk_tie = 0 — the chain is silent about
  k_tie. Horn B: substituting the tie gives κ_law = k_tie — the "derivation" returns its input. There is
  no third horn.
- **Q010's "×3" (K14).** Q001 (c_s² = σ²), Q007 (v_c² = 2σ²) and the definition of κ form a rank-3 system
  in 4 unknowns: the solution set is a ray, `{σ² = v²/2, c_s² = v²/2, κ = ½}` with v² free. Three
  writings of one identity; none of the three contains a₀, c or ρ_DE. "Three independent routes" is a
  count of equations, not of independent physical inputs.
- **GF2's own L1a has no teeth (K15).** Their test is d/dr[(∇²Φ − 4πGA r^(−γ))·r²] = −4πGA(2−γ)r^(1−γ),
  which vanishes at γ = 2 **for every A, including A = 0** — it cannot distinguish "the log sources the
  SIS" from "the log sources nothing". The real closure is the coefficient A = C/(4πG), which GF2's C1
  supplies by *defining* ρ := ∇²Φ/(4πG). The algebra is right; that check proves nothing.

### 5. The identity content, stated plainly

κ_dyn = σ²/v_flat² = (C/2)/C. The only normalisation in the chain cancels identically (∂κ_dyn/∂C = 0).
What is left is the pure number 2 in `v_c² = 2σ²` — the SIS's shape number, the same 2 that sits in
ρ = σ²/(2πGr²) and follows from the r⁻² profile in Newtonian gravity. The law's 2 is the inverse coupling
of the vacuum sector. Nothing in the chain makes them the same integer.

## Status

**`DIFFERENT-QUANTITY`.** In the BRIEF's vocabulary this is `NO-GO(obstruction)`: the obstruction is the
scaling symmetry (K9) plus the absent normalisation equation (M1). Equivalently: an identity internal to
the SIS, mis-labelled as the law's coefficient. Not `DERIVED`, and not merely `CONDITIONAL` — a
conditional derivation would become correct
when its premise is supplied; this one cannot, because the missing premise is the conclusion (K12) and the
two quantities have different scaling weight (K9).

What *is* earned, and should be kept in the record: **the SIS state is derived**, not imported. Given P1,
the closure forces γ = 2 (K4, unique among power laws), the EoS to be isothermal (K3: the only polytropic
index that closes on ρ ∝ r⁻² is γ_eos = 1), and σ² = C/2 (K1). That closes T13's registered item. It
does not close κ.

## Checks

| id | what it measures | value | verdict |
|---|---|---|---|
| K1 | chain rebuilt: Poisson residual, σ², v_c², κ_dyn | 0; C/2; C; 1/2 | PASS |
| K2 | general σ²(r) solution and the one-parameter SIS family | C/2 + K r²; ρ = s/(2πGr²) ∀s | PASS |
| K3 | polytropic index that closes on ρ ∝ r⁻² | γ_eos = 1 only; σ² = C/2 | PASS |
| K4 | brute force over 2001 p: unique constant-σ² power law | p = 0 only; defect > 2.811e−2 off it | PASS |
| K5 | counterexample to the unqualified lemma (cored isothermal sphere) | slope −3.333e−5 → −1.992; resid 4.1e−6 | PASS |
| K6 | anisotropy: κ_dyn = 1/(2(1−β)) | 0.333 … 1.000 over β ∈ [−0.5, 0.5] | PASS |
| K7 | renaming the law's κ to 2/5 | chain stays 1/2 (differs by 1/10) | PASS |
| K8 | a₀/c/ρ_DE audit | symbol intersection ∅; 0 mentions | PASS |
| K9 | scaling symmetry: µ-invariance vs weight 1 | residuals 0; κ_dyn 1/2→1/2; κ_law ×µ | PASS |
| K10 | Λ obstruction | residual −Λr/3; 10 kpc error 1.2e−22 | PASS |
| K11 | footings | κ_law 0.500473; a₀(½) 9.351151e−11; a₀(32π) 9.354173e−11 | PASS |
| K12 | tie dilemma | ∂κ_dyn/∂k_tie = 0; κ_law = k_tie | PASS |
| K13 | missing-step equivalence chain | Λ = 32πa₀²/c⁴; Λℓ₀² = 32π; ρc² = 4a₀²/G | PASS |
| K14 | Q010's three routes | rank 3 of 4; ray with v² free, κ = 1/2 | PASS |
| K15 | GF2's L1a vacuity | 0 at γ=2 for all A, incl. A = 0; A_true = C/(4πG) | PASS |

Numerical context (K11): s_DE = 1.870230e−10 m/s², cH_Λ = 5.414953e−10 m/s², Z = 2√(8π/3) = 5.788810,
1/Z = 0.172747. With the BRIEF footing a₀ = 9.36e−11, κ_law = 0.500473 — 0.095% from ½ because the footing
was *constructed* as ½, and 0.062% from the 32π form. That agreement is a consistency of the footing, not a
derivation of it.

## What this does not do

- It does not claim κ is underivable in general. It claims these premises do not derive it, and gives the
  exact equation that would.
- It does not test the data. κ measured is 0.417 ± 0.095 (CFG493, quoted in CFG908) — consistent with ½ at
  0.87σ, and k05's combined 0.530 ± 0.037 is 0.81σ, so the data cannot decide and the theory must.
- It does not re-audit the other three "κ derived" claims (G031, glm53/G002, gemini38); CFG908 does, and
  nothing here contradicts it.
- It does not re-derive Q010's Lean theorems; K14 shows only that their *content* is one identity.
- It does not claim GF2 is wrong where GF2 is careful. GF2's README and STATE are honest about the vacuum
  border; the over-claim is confined to the register line and V1/V5.
- The Λ obstruction is structural, not numerical (1.2e−22 at 10 kpc); it is not a phenomenological problem.

## Next — the single missing step, as a conjecture

The halo sector supplies two equations for three unknowns (C, σ², a₀): the closure σ² = C/2, and the
deep-MOND normalisation C² = GM_b a₀. Nothing relates a₀ to ρ_Λ. **The system is one equation short, and
κ is exactly the content of the missing equation.** The equation that would have to hold is

    (M1)   a₀² = G ρ_Λ c² / 4     ⇔   ρ_Λ c² = 4 a₀²/G     ⇔   Λ ℓ₀² = 32π     ⇔   κ = 1/2

(exact, K13; the only convention-free content is 1/κ² = 4). Note the shape: M1 says the cold sector's
maximum stress, P_max ≡ a₀²/G, is one quarter of the vacuum energy density.

**Conjecture A15-C1 (vacuum normalisation).** There exists a local functional
`N[g, T^φ; G, c, ρ_Λ]` of the cold sector's rest-frame stress and the metric, containing no dimensionful
parameter and **no dimensionless constant**, whose stationarity on the de Sitter background is equivalent to

    P_max ≡ a₀²/G = ρ_Λ c² / 4 ,

with the factor 4 produced by a count of the sector's internal channels, not inserted. Then κ = 1/2 follows
identically from M1, and the SIS ratio ½ coincides with κ for a reason rather than by name.

**Why it is a conjecture and not a plan.** k01 (`kappa_closure/k01`) proved that in the present action
class no equation relates a₀ and Λ: the static field equations contain the MOND primitive only through J′,
so J → J + C is an exact symmetry and the zero mode is unfixed. A functional of the A15-C1 type must break
that symmetry — it has to live outside the present action class, not inside it. That is the same wall
CFG908's C2–C4 rows hit from three other directions.

**Falsifier / teeth.** Any candidate must return exactly 4 in the convention-free ratio ρ_Λc²/(a₀²/G). A
candidate returning 2, 3, 4π, 8π or 32 is excluded by the exact identity Λℓ₀² = 32π. A candidate that needs
one number fitted is not a derivation — it is the register line "κ = ½ FITTED" with extra steps.

**Register wording this lane supports.** "κ = ½ is FITTED (CFG493). GF2, Q001 and Q007 give the SIS ratio
σ²/v_c² = ½, an identity internal to the isothermal sphere; the bridge from that ratio to a₀/(c√(Gρ_DE)) is
rung 5, POSTULATED-CARRIED. The coefficient remains underived."
