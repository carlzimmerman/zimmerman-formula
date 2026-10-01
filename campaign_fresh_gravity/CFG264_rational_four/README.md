# CFG264 -- a constrained attempt to DERIVE the rational 4 in G ρ_Λ = 4 a₀²/c² (κ = ½)

**Bottom line.** Nothing derived. **κ = ½ stays FITTED.** I ran three routes: the top two of the five untried routes in the frozen ranking, plus the OWNER-DIRECTED route. Each ends in a scoped no-go with a named binding failure, and none of them outputs k2 := a₀²/(c² G ρ_Λ) = ¼ from its own dynamics. The two places where ¼ does appear are restatements:
- R1's C2+C4+C6, the Schwarzschild surface gravity evaluated at R* (the gemini reading);
- the "8π × entropy-quarter" conversion, where the ¼ goes in as a number.

No Lean sketch and no independent re-derivation is needed, because no derivation landed.

Criteria were frozen before any script: `CFG264_FROZEN_CRITERIA.md`, sha256 ff8657eb…c769, 2026-10-01T21:53:16Z. Addendum 1 was written before any script and Addendum 2 before the OD script. Addendum 3 is a POST-RUN check requested by the coordinator after CFG263; it is labelled as post-run below and changes no verdict rule. All hashes are in `CFG264_FROZEN_CRITERIA.sha256`. Re-run everything with `./run_all.sh` (≈ 95 s, exit 0). The tallies are:

| script | main run | MUTATE run |
|---|---|---|
| R1 | 19/19 | 3/3 |
| R2 | 15/15 | 4/4 |
| OD | 20/20 (16 frozen + 4 post-run, Addendum 3) | 4/4 |

## Frozen ranking (P(derivation) frozen before any calculation; run = top two by P/cost + the owner's route)
| route | mechanism (one line) | P | cost (h) | P/cost | run? | verdict |
|---|---|---|---|---|---|---|
| R1 | deep-MOND virial theorem + the vacuum's virial term + declared relativistic closures | 0.3 % | 1.0 | 0.30 | yes | **SCOPED NO-GO** (Buckingham; π-weight) |
| R2 | two-sided (in/out averaged) Israel junction of a MOND-critical wall with the vacuum | 0.4 % | 1.5 | 0.27 | yes | **SCOPED NO-GO** (Gauss 2π in the σ-closure) |
| R3 | two independent halvings (Tolman 2 × virial 2) in one equation | 0.2 % | 2.0 | 0.10 | no; its equation is inside R1 | closed within R1's menu |
| R4 | extremum of a ρ-linear field + vacuum functional (4 = 2² as a quadratic maximum) | 0.3 % | 3.0 | 0.10 | no | -- |
| R5 | dimensional reduction / π-free cubic cell (W09/W10) | 0.1 % | 4.0 | 0.025 | no | -- |
| **OD (OWNER-DIRECTED)** | ½ as the ratio of the entropy quarter (S = A/4) to the bulk 8π | 0.2 % | 1.5 | 0.13 | yes (owner's request) | **SCOPED NO-GO** (ħ-cancellation) **+ RESTATEMENT** (the conversion reading) |

The frozen file gives each route's "why not closed" note (with the lanes it cites) and its cheapest decisive check.

## R1 -- deep-MOND virial theorem with the vacuum (`r1_virial_lambda.py`)
**Mechanism.** The base relation is 2K = (2/3)√(G a₀) M^{3/2} − α H² M R², with H² = (8π/3) G ρ_Λ.
- The first term is Milgrom's exact deep-MOND virial.
- The second term is the vacuum's weak-field force, sourced by the Tolman active density ρ + 3p/c² = −2ρ_Λ.
- α ∈ {3/5, 2/3, 1}.

A system is that relation plus three conditions from the frozen pool:
- **S1–S4**: binding edge, half-binding, marginal mass;
- **C1–C6**: virial speed = c, R = 2GM/c², R = c²/a₀, R = R*, R = c/H, GMa₀ = c⁴/4;
- **D1–D2**: mean density ρ_Λ or 2ρ_Λ.

That gives 495 systems, all solved exactly as log-linear monomial systems, with a substitution for C1.

**Ingredients re-derived** (all pass):
- the 2/3 coefficient: exact for a uniform sphere, numerically for a Plummer profile;
- the N-body relation's test-particle limit, −m√(GMa₀);
- the Tolman source −2ρ_Λ, and the vacuum field (8π/3)Gρ_Λ r from Poisson;
- the polar moments.

**Results.**
- **Buckingham.** The c-free set {G, a₀, ρ_Λ, M, R} has exactly two Π-groups, G³Mρ²/a₀³ and GRρ/a₀. Every c-free condition is invariant under (a₀, R, M) → (λa₀, λR, λ³M). So no Newton + Λ + MOND principle (virial theorem, threshold, zero-force, hydrostatic) can fix k2, which carries c⁻². In the menu, 30/30 c-free systems leave k2 free or are inconsistent.
- **Admissible systems** use the vacuum dynamics (S1/S2/S4) and not R*. 129 of them have a unique k2: 120 are (rational) × π and 9 are (algebraic) × π. **None is π-free; none is ¼.** The vacuum enters only as H² = (8π/3)Gρ_Λ, and no declared closure cancels that π. My pre-run expectation (HE1) was that D1/D2/C5 might cancel it; they don't, because the volume brings π^{1/2} against the vacuum term's π.
- **k2 = ¼ appears only in C2+C4+C6** (R = 2GM/c², R = R*, GMa₀ = c⁴/4), at every α: a₀ = c²/(2R*). This is the Schwarzschild surface gravity at R*, i.e. the gemini reading. It uses R* and no vacuum dynamics, so by the frozen rule it is a **RESTATEMENT**. It is also unchanged by all three mutations, which is the signature of carrying no dynamical content.
- **Decoy check.** k2 = 1 (the record's forced kernel κ = 1) is hit 24 times, always through C3+C4 (Rindler length = R*). That is the same restatement class.

**R3 reported against R1.** The S-conditions contain the product of the vacuum's Tolman 2 and the kinetic/virial 2 in one equation. Within this menu that product never gives a π-free k2. This is a scoped statement, not a general one.

**Binding failures (scoped to the frozen menu):**
- c-free sub-class: Buckingham;
- relativistic closures: π-weight (Lindemann).

**Circularity audit.** For each input:
- S1/S2/S4: Milgrom's virial plus the Tolman-sourced vacuum force, with Einstein's 8πG and no puzzle.
- C1–C3, C5, C6: relativistic identifications with no ρ–a₀ relation.
- C4 = R*: contains ρ_Λ but not a₀. Excluded from admissibility by the frozen rule.
- D1, D2: densities.

The programmatic guard confirms that no single condition forces k2 = ¼ (11/11 ok). No input contains κ, 32π or Λ = 32πa₀²/c⁴.

**MUTATE** (separate outputs). Each mutation changes the table:

| mutation | systems changed | of which admissible |
|---|---|---|
| M1: virial 2/3 → 1 | 168 | 117 |
| M2: Tolman 2 → 1 | 171 | 120 |
| M3: d = 3 → 4 | 222 | 129 |

In all three, the k2 = ¼ restatement rows are unchanged. M3 leaves 15 systems with only numeric roots; none is used for a verdict.

## R2 -- two-sided junction of a MOND-critical wall with the vacuum (`r2_two_sided_junction.py`)
**Mechanism.** A pure-tension spherical wall separates a de Sitter interior (ρ_Λ) from a Minkowski exterior. a₀ is identified with a wall acceleration:
- J1: the two-sided average;
- J2: the inner side;
- J3: the outer side;
- J4: their geometric mean;
- J5: half the jump.

σ is fixed by a declared closure:
- Sg1: Milgrom's Σ_M = a₀/(2πG);
- Sg2: a₀/(4πG);
- Sg3, Sg4: one side unaccelerated;
- Sg5: wall mass = enclosed vacuum mass;
- Sg6: wall mass = Schwarzschild mass of its radius.

**Derived from the metric** (not imported):
- the proper acceleration of a radial worldline, from the Christoffels;
- the unit normal;
- the umbilic de Sitter wall R(τ) = cosh(wτ)/w with K^τ_τ = K^θ_θ = k, w² = k² + H² (exact identities plus 12 numeric spots);
- the Israel jump 8πGσ/(D−2), from the trace algebra in general D;
- **the two-sided average ā = Δρ c²/((D−1)σ)**, which is the shell's normal-force equation (D−1)σ ā = Δp.

At D = 4, ā = ρ_Λc²/(3σ). It is exactly π-free in Gρ_Λ, carries c, and does not depend on R or H. It reproduces the record's audit H1, (A, B) = ΔP/(3σ) ∓ 2πGσ. Z2 control: ā = 0, and each side accelerates at 2πGσ for every ρ.

**Results** (35 pairs). **No pair gives ¼; every solved pair carries π.**
- The natural MOND-critical wall (J1 + Sg1) gives **k2 = 2π/3**, i.e. a₀ = cH_Λ/2 (κ = 1.447). That matches my pre-run expectation HE2.
- The outer-side conditions J3 + Sg2 and J3 + Sg3 give 8π/3, i.e. a₀ = cH_Λ.

**Where the π enters** (M3 control, σ = q a₀/G with a free number q):
- The two-sided J1 gives the π-free **k2 = 1/(3q)**. So κ = ½ ⟺ **q = 4/3**: the wall would need σ = (4/3)a₀/G, i.e. its own Z2 acceleration would be (8π/3) a₀. No Gauss, Israel or MOND condition supplies that.
- Every one-sided condition re-introduces π through the 2πGσ self-gravity term.

So two-sidedness does remove the wall's own π, and the σ-closure puts it back: Gauss's law fixes any field-determined surface density with a 1/π.

Coincidence flag, not a result: q = 4/3 equals the record's "memory moment 4/3" (the radiation enthalpy ratio). Many rationals sit near any target, and I attach no meaning to it.

**Binding failure.** The σ-closure: the Gauss 2π in Σ_M (π-weight).

**Circularity audit.** The inputs are:
- the Israel junction (GR);
- de Sitter with H² = (8π/3)Gρ_Λ (Einstein's coupling);
- the identifications J and closures Sg.

The guard passes for all 12 conditions. None contains κ, 32π, the law or R*.

**MUTATE:**
- M1 (one-sided instead of two-sided) changes every J1 row. J1+Sg1 then has no solution.
- M2 (D = 4 → 5) changes 15 systems; for example J1+Sg1 → π/3.
- M3 (the π-free σ control above) shows where the π enters.

## OD -- OWNER-DIRECTED: is ½ the ratio of the entropy quarter to the bulk 8π? (`od_horizon_quarter.py`)
**Question tested.** Is there an equilibrium, extremum or matching condition between a horizon's entropy budget S = k_B A c³/(4Għ) and the vacuum energy it encloses, ħ cancelling, that outputs a₀ = ½c√(Gρ_Λ)?

**Menu.** Three horizons × eight budgets.

Horizons, with a₀ := the horizon's surface gravity:
- HdS: the de Sitter horizon;
- HS: a Schwarzschild flat probe, κ = c²/2r;
- HR: a Rindler sphere, r = c²/a.

Budgets:
- B1: TS = E_vac
- B2: 2TS = E_vac (Smarr)
- B3: TS = E_Komar
- B4: Padmanabhan's N_sur k_B T/2 = E_Komar
- B5: (S/k_B) k_B T/2 = E_Komar
- B6: T dS/dr = dE_vac/dr
- B7: fixed-T stationary point
- B7′: stationary point along the horizon family

**The five obstacles the owner listed, addressed one by one:**
- **(a) the killed lead.** README line 65 says: "Its "32π = 8π × 4 as Einstein × entropy-quarter" lead was killed as numerology (a literal second Bekenstein-Hawking quarter gives Z = 11.58)." DERIVE_Z strike 3 adds that the single quarter is already spent inside the 8π (Jacobson: 8π = 2π × 4). This lane confirms it with a computation. Read as a conversion factor, a₀² = ¼ × (Λc⁴/8π), the relation is k2 = ¼ by construction: the quarter is inserted as the number (check E1, a RESTATEMENT). Counting the quarter a second time (S → A/16) still leaves every budget at (rational) × π (check E2).
- **(b) GHY vs Einstein–Hilbert.** The normalisation ratio GHY/EH is **2**, not ¼ (B1). The Euclidean Schwarzschild action computed from GHY with flat subtraction is I_E = βM/2 (B2), so S = βM − I_E = A/4G (B3). The quarter needs the thermal period β = 2π/κ. It is an entropy normalisation, not an action normalisation (B4).
- **(c) ħ must cancel.** Among T^a S^b, exactly the a = b products are free of ħ and k_B (A1). So the quarter can enter a classical budget **only together with the thermal 1/(2π)**, as TS = κAc²/(8πG) (A2). It does cancel in all 16 solved budgets (D1).
- **The binding failure.** In TS/E_vac with ρ_Λ = Λc²/(8πG), the entropy's 8π **cancels** Einstein's 8π: TS/E_vac = κA/(Λc²V) (A4). The target needs the two to multiply (32π = 8π × 4). Hence every HS/HR budget gives **k2 = (rational) × π¹**: 4π/3, 2π/3, 8π/3, 16π/3, 2π, 4π, 32π/3, 8π (D5). None is ¼.
- **(d) how this differs from N and X3.** N is the local Clausius chain. The vacuum carries no null heat flux (T_kk = ρ + p = 0), so Λ is invisible to it. My B6/B7 count the enclosed vacuum energy as heat, which is an inserted premise in Jacobson's terms. X3 part A already covered "TS vs |PV|", and |PV| = ρ_Λc²V. OD reproduces X3's flat-probe entries exactly (4π/3 and 2π/3; D3, a cross-lane check). So OD **mostly does not differ from X3**. Its additions are the Rindler sphere, the Komar/holographic-equipartition budgets, B6/B7′, the ħ lemma and the GHY placement. None changes X3's conclusion.
- **(e) circularity audit, per step.**
  - Inputs: Unruh/Hawking T, Bekenstein–Hawking S, ρ_Λc²V, the Komar/Tolman 2, Padmanabhan's N_sur, and the horizon surface gravities.
  - The owner's "¼ ÷ 8π" is never inserted as a number, except in check E1, which exists to show that inserting it is the restatement.
  - The guard passes for all 16 HS/HR budgets.

**(f) POST-RUN check (Addendum 3, requested by the coordinator after CFG263, whose structural lesson is that a mechanism with only the scales a and H cannot give κ = ½, so a derivation must couple the a₀ sector's ENERGY DENSITY with a rational coefficient).** The owner's balance falls in the excluded class:
- **F1.** Rewritten with ρ_Λ = 3H²/(8πG), every HS/HR budget contains only {r, c, G, H, ħ, k_B}. No a₀-sector energy density occurs; a₀ enters only as the label on κ_h.
- **F1b.** Every solved k2 is (8π/3) × q, with q ∈ {1/4, 1/2, 3/4, 1, 3/2, 2, 3, 4}. So a₀/(cH) is algebraic, which is the class signature.
- **F2.** Coupling an a₀-sector energy density explicitly does not rescue it. Take the vacuum to be ε = W a₀²/G. On the de Sitter horizon, TS = εV then holds for every W (it is an identity), so the horizon fixes nothing. W = 4, i.e. k2 = 1/W = ¼, would have to come from the a₀ sector itself, which is lane K's open target.
- **F2b.** On the HS probe with κ_h = a₀, the same budget fixes W = 3/(4π), i.e. k2 = 4π/3: the π comes back.

So the horizon-entropy route cannot supply the rational coefficient CFG263 identifies as necessary.

**What the owner's idea does get right.**
- On the de Sitter horizon, TS = E_vac is an **exact identity** (D2). So is Padmanabhan's holographic equipartition, N_sur k_B T/2 = E_Komar.
- So a 2D-horizon-to-4D-bulk conversion with ħ cancelling exists exactly, and it is Friedmann's equation.
- Its acceleration is cH_Λ, which gives k2 = 8π/3. That is a₀ = cH (Z = 1, κ = 2.894; lane N's member (ii)), not ½.

**MUTATE:**
- **M1 (remove the thermal 2π)** changes 18 rows and makes every HS/HR budget π-free (M1b). So the π in the main run *is* the thermal 2π paired with the quarter. Even then the values are {1/3, 2/3, 1, 4/3, 2, 8/3, 4, 16/3}, never ¼. In this family ¼ would need a budget weight of 8/3, which no declared or natural budget has.
- **M2 (quarter → ½)** changes 16 rows.
- **M3 (D = 5)** changes 17 rows. The de Sitter identity is then lost (TS/E_vac = 2/3), so it is a D = 4 fact.

**Verdict.**
- **SCOPED NO-GO**, binding failure ħ-cancellation: the quarter is welded to the thermal 1/(2π), and the resulting 8π divides out Einstein's 8π.
- The conversion-factor reading 32π = 8π × (1/quarter) is a **RESTATEMENT**.

## Side findings (for the orchestrator; nothing outside this folder was edited)
1. **Label inconsistency in X3's README.** Its bottom line calls the T_b = T_dS point, a₀²/(Gρ_Λ) = 8π/3 (that is a₀ = cH), "the record's forced kernel kappa = 1".
   - By the definition in the puzzle README (sections 6–7), the forced kernel is κ = 1, i.e. k2 = 1, Z = 2.894.
   - a₀ = cH is Z = 1, κ = 2.894. Lane N's own numbers are consistent with that.
   - X3's value is right; its label is not. My frozen hand estimate HE3 repeated the label ("the forced kernel"), and that is corrected here and in the OD script.
2. **The gemini SPIN2 projection, (D−3)/(D−2) = ½.** This is the trace-reversal factor that turns 16πG into 8πG in the Newtonian limit (X1's BIA atom, already inside 8π). Using it again double-counts. I only read the first 60 lines of that file and did not script this.
3. **The two-sided average of a pure-tension wall is the shell's normal-force equation**, ā = Δρc²/((D−1)σ). It is the only exactly π-free, c-carrying object I found linking a surface to ρ_Λ. The π it avoids comes back through any field-fixed σ.

## Relation to CFG263 (the audit of the 32π no-gos, 35058745f; received while this lane ran, used only for the post-run check)
- No route here re-runs one of CFG263's rejected near misses:
  - G_cosm = 4G_N via a preferred-frame coupling;
  - the u-unit Noether condition;
  - the area-first horizon route.
- OD is the closest of the three to that last one. Its failure (F1–F2b) is consistent with CFG263's.
- CFG263's exact RAR offset, c = 4π⁴/15 (so Gρ/a₀² = π³/30), means a thermal (Bose-shaped) ν cannot supply W = 4 either. That closes the obvious way to fill in F2's "W must come from the a₀ sector".
- Taken together, the open target is unchanged: an a₀-sector energy density coupled to gravity with a rational coefficient that a principle fixes at 4.

## Errors of mine, fixed openly
- **Addendum 1:** my frozen α = 2/3 "shell" was the axial moment. α = 1 for a shell was added before any script ran.
- **Addendum 2:** my frozen OD B7 is identical to B6. B7′ was added before the OD script ran.
- **R1 solver:** the C1 path labelled parallel contradictory pairs (S1+S2, C4+C5, D1+D2) "underdetermined". It now tests consistency. A degenerate identity (α = 1, S2+C1+C5) was mis-sent to a numeric root scan. No k2 changed.
- **R1 check D2:** it was non-failable, so it is now an INFO line.
- **R2, Sg6:** it had a factor 2 wrong (4πGRσ = c² instead of c²/2). I caught this on re-reading, before the first run.
- **R2, A3/A4/A9:** these first failed because sympy cannot take √cosh² without positivity. They were replaced by exact squared identities plus numeric spots, which can still fail.
- **R2, M3:** this first failed because of a sympify symbol mismatch.
- **OD, check D2:** the label was fixed (side finding 1).

## Not established
- Anything outside the frozen menus. R1 covers three stationarity conditions, six relativistic closures, two densities and three α values. R2 covers five identifications and six σ-closures. OD covers three horizons and eight budgets. A principle outside these is not excluded.
- R3, R4 and R5 were not run. R3 is covered only to the extent that its product appears in R1's equations.
- The deep-MOND virial relation is used in its continuum, isolated, stationary form. The external-field effect is not treated.
- Whether a wall's acceleration is the MOND a₀ at all (lane J's open question) is not decided here. R2 assumes the identification and still fails.

## Files
- `CFG264_FROZEN_CRITERIA.md` and `.sha256`
- `cfg264_lib.py`
- `r1_virial_lambda.py`, with `.out`, `_results.json`, `_MUTATE.out`, `_MUTATE_results.json`
- `r2_two_sided_junction.py`, with the same four outputs
- `od_horizon_quarter.py`, with the same four outputs
- `cfg264_collect.py` → `results.json` (lane summary)
- `run_all.sh`
- `README.md`

Not committed and not pushed.
