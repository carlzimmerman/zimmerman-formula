# D_kappa: one more attempt at κ (2026-10-14). Hand algebra only, no runs.

**Verdict: κ is NOT derived.** This note adds two closure theorems, one definite wrong-number route, and a reduction of the
target to a single local equation. κ = ½ stays FITTED (CFG493 0.42 ± 0.10; F3 0.465 ± 0.076 / 0.55 ± 0.17). Not "theory closed".
Nothing here was run. The only arithmetic was one `python3 -c` coefficient check. Every statement needs a committed check
script before anyone cites it.

Read first, not repeated here: the additive-offset counterfamily (COEFFICIENT32PI-001: W_C has C-free derivatives); critical
amplitude ratio R_vac = ε W3²/W2³ = 64π (CRITICAL32PI-001, large-N O(N) gives 1/3); the dust-dust ½ is not the vacuum ½ (WEEK32PI);
minimal dynamical a forces C = 0; S⁴ Euler is inert; microscopic exponential ensemble gives C = 1 + E_off/T (MICRO32PI);
scale identity a∂_aW + u∂_uW = 2W holds for every C; coupled hidden fields leave R free (COUPLED32PI); dilaton R = 25/16;
F4–F6, F16 (unimodular tie: κ is its coupling), T001 catalogue (Milgrom 1999/2020, Verlinde cH₀/6, Pikhitsa all ≠ ½).

Notation: K = 4πG, u = K|P|, a = a₀, x = u/a, W_full = (a²/K)[C − x − ln(1 − x)], g = KW′ = au/(a − u), g_N = g − u = g²/(a + g).
Target dictionary (from WEEK32PI §2, premise "W_full(0) is the total vacuum energy"): κ² = 4π/C, q = κ√(3/8π),
κ = ½ ⇔ C = 16π ⇔ q² = 3/(32π) ⇔ ε_Λ = 4a²/G. On the Milgrom footing q = 1/2π ⇔ κ = 0.4607 ⇔ C = 6π² (= 59.2).

---------------------------------------------------------------------------------------------------------------------------
## Route A. Can the cosmic background polarize? (task idea (a)) → CLOSED by a homogeneity theorem

**Premise A.** De Sitter space is a fixed point of the saturating response: P responds to the vacuum's own Newtonian field.
Then a matching condition at the cosmic fixed point fixes a/√(Gρ_DE).

**Calculation.** Around ANY comoving point the vacuum's weak-field potential is Φ = −Λc²r²/6. Its field is outward,
g_N = H_Λ² r, from the active density ρ + 3p/c² = −2ρ_Λ. Take the law at face value, with the sign handled by |P|.
- Inside r < a/H_Λ² = q c/H_Λ ≈ 0.17 R_Λ: y = H_Λ²r/a < 1, so the response is deep. Then g ≈ √(a H_Λ² r) = H_Λ√a · r^{1/2}.
- Implied extra (phantom) density: ρ_ph ∝ ∇·g/(4πG) = (5/2) H_Λ√a r^{−1/2}/(4πG). This diverges at the observer.
- The divergence sits at whichever point you call the centre, so two observers assign different ρ_ph to the same event.
  The response is not a scalar field on FRW, and a homogeneous background cannot carry it.
- A homogeneous vector background P̄ ≠ 0 breaks isotropy, so it is also excluded.

**Theorem A.** On an FRW/de Sitter background with an isotropic vacuum, consistency forces ū = 0. The response must be
blind to the vacuum's own source; this is the existing "switch reads baryons" rule, now forced and not chosen. At ū = 0 every
equation is C-independent and a-independent (the counterfamily). So "de Sitter as a fixed point of the response" holds
identically for every (κ, C) and gives no condition. **Derivation? No: a proof that route (a) is empty.** Not R0-shaped.

---------------------------------------------------------------------------------------------------------------------------
## Route B. Match the P-wave gap to H_Λ (task idea (c)) → CLOSED by a criticality theorem

**Premise B.** The cosmic P background has a mass gap ω_g, and marginal stability sets ω_g = H_Λ (or ω_g² = 2H_Λ², the
conformal/Higuchi-type value).

**Calculation.** For small u, g = K W′(u) ≈ β u with β ≡ K W″(0). Then g_N = (β − 1)u, so g = [β/(β − 1)] g_N.
For β ≠ 1 this is linear: Newton with G_eff = βG/(β − 1), and it has NO deep regime (β < 1 even flips the sign).
The deep law g → √(a g_N) requires β = 1 exactly. That gives W_rem″(0) = W_full″(0) − 1/K = 0: the vacuum is critical and
massless for every C and every a. The CFG760 gap ω_g² ∝ 2|v₀|/s + 2/s² is a gap around a point source. It is induced by
baryons and vanishes as s → ∞, so the cosmic background (Theorem A: ū = 0) has ω_g = 0 ≠ H_Λ.

A curvature coupling ξR P² could give a gap. It enters with the stiffness γ, whose scale L* = 5.75 pc (CFG691) implies
γ-weighted R/W″ ~ (L* / R_Λ)² ~ 10⁻¹⁸. That is far too small to tie a to Λ at O(1), and ξ would itself be a new knob.

**Theorem B.** Inside the class that keeps the deep law, the cosmic P sector is exactly critical. Gap matching to H_Λ is
impossible without destroying the MOND regime. **Closed. Not R0-shaped.**

Variant B′ (stochastic IR fluctuations of a massless P in de Sitter, a Starobinsky–Yokoyama equilibrium in the cubic W):
this needs ħ and the kinetic coefficient c_P (CFG762), and the variance scales with ħ, so the dimensionless result carries
ħGH_Λ²/c⁵ ~ 10⁻¹²² unless it cancels exactly. It cannot produce an O(1) κ; by F1, admitting ħ destroys uniqueness anyway.
Not executed. Closed by power counting.

---------------------------------------------------------------------------------------------------------------------------
## Route C. Tether capacity fills the cosmic horizon (NEW, gives a definite number) → q = ½ or 1, EXCLUDED

**Premise C.** The polarization bound |P| < a/K gives the Gauss-law capacity: the bound charge inside a sphere of radius R is
at most M_cap(R) = ∮|P| dA = a R²/G. That is Σ ≤ a/(πG) in CE-FM form. Physical claim: dark energy is the vacuum's
polarization filled to capacity at its own horizon R_Λ = c/H_Λ. So M_cap(R_Λ) equals the vacuum mass-energy inside R_Λ.

**Calculation.**
- Passive mass (also the Misner–Sharp mass of the dS horizon): M = (4π/3)ρ_Λ R_Λ³ = c³/(2GH_Λ).
  a c²/(GH_Λ²) = c³/(2GH_Λ) ⇒ **a = cH_Λ/2, q = ½, κ = ½√(8π/3) = 1.447**, C = 4π/κ² = 6.0.
- Active (Komar) mass |ρ + 3p| = 2ρ_Λ gives **a = cH_Λ, q = 1, κ = 2.894**.
- Target: q = 0.1727 (Milgrom footing 0.159). Route C is off by ×2.9 (passive) or ×5.8 (active) in a₀.
  Against F3 estimator A, κ = 1.447 is +12.9σ; against estimator B it is +5.3σ. **EXCLUDED by SPARC on both footings.**

**Status.** A genuine derivation from a stated premise, with no target inserted, and it gives the wrong number. It is also
structurally on the rival branch: it fixes a ∝ c²/R_horizon. By astra's theorem (claude_bh_followthrough REPORT §1),
a horizon-set scale and a √ρ_V scale evolve oppositely once vacuum is produced. The capacity route can therefore only
co-exist with the framework's flat-a₀(z) law if R is replaced by the auxiliary curvature length L_V, which is not a horizon.
At that point the "horizon" reading of the premise is lost. **Corollary C:** horizon-based coefficient routes (capacity,
Schwarzschild r_H = c²/2a₀, holographic, Unruh) cannot be the origin of κ inside a theory whose a₀ tracks √ρ_V,
except in exact de Sitter. Every one of them predicts the event-horizon branch (a₀(z = 2)/a₀(0) = 1.44, not 0.85 / flat).

---------------------------------------------------------------------------------------------------------------------------
## Route D. Local energy matching: the only consistent home for κ (reduction plus a catalogue of natural numbers)

From A, B and C: the cosmic background is P-neutral and critical, and horizon routes are on the wrong branch. So κ can only
enter through a LOCAL relation between the vacuum energy density and the response's own energy unit a²/K. In G units:

  **κ = ½ ⇔ ε_Λ = 4 a²/G ⇔ ε_Λ = 16π · (a²/K).**

The response carries a²/K = a²/(4πG), the Gauss-flux-normalized unit. The vacuum must carry 4a²/G, with no 1/4π. That
is the exact content of the missing number: a bulk energy of 4 (G units) against a flux-normalized response.

Natural local candidates, each with its premise, C, and κ = √(4π/C):

| premise for ε_Λ | C | κ | q | vs ½ |
|---|---|---|---|---|
| gravitational field energy at crossover, g_N²/(2K) at g_N = a | ½ | 5.01 | 1.73 | ×10 |
| classical exponential ensemble, E_off = 0 (MICRO32PI) | 1 | 3.54 | 1.22 | ×7 |
| horizon capacity, passive (Route C) | 6.0 | 1.447 | ½ | ×2.9 |
| equipartition over d independent quadratic modes, ε = (d/2)·nT | d/2 | √(8π/d) | — | needs d = 32π = 100.53 |
| Milgrom footing (cH₀/2π) | 6π² | 0.461 | 0.159 | footing-conditional (F7) |
| target | 16π | 0.500 | 0.1727 | — |

**Finding D1 (new, sharp).** Any premise in which ε_Λ/(a²/K) is a rational number (mode counting, equipartition,
classical cumulants) cannot give exactly C = 16π, because 16π is irrational. The only π available locally is the K = 4πG
flux normalization. Getting 16π needs the vacuum energy to be counted in G units (ε = 4a²/G, the integer 4) while the
response is counted in K units. Rational-C families are not excluded OBSERVATIONALLY: d = 100 gives κ = 0.5013 and
d = 101 gives 0.4988, both deep inside 0.465 ± 0.076. So the data cannot tell "κ = ½ exactly" from "C = d/2, d ≈ 100".
A claimed derivation of exactly ½ therefore needs the integer 4 in G units, not a count near 100.

**Finding D2.** The integer-4 statement reads a₀ = ½√(Gε_Λ) (c = 1). Every published way to produce a "½" from Gε is a
horizon or surface-gravity factor (r_s = 2GM, κ_s = 1/4GM, Unruh 2π). Corollary C excludes horizon routes on this branch,
and WEEK32PI excludes the spin-2 ½. **No non-horizon local mechanism producing the bare integer 4 is known to this record.**
Route D is therefore a reduction (it states exactly what a microscopic theory must output), not a derivation.

---------------------------------------------------------------------------------------------------------------------------
## Underivability statement (scoped, conditional)

Take the class: corrected action (W_full or W_rem form) + unimodular or Henneaux–Teitelboim tie a² = κ²c²Gρ_V (F16) +
response blind to the vacuum (Theorem A, forced) + deep law (β = 1, Theorem B, forced) + any additive C. In this class:
1. The local equations, the stiffness, the critical P-wave sector, and the cosmic background are identical for all κ at
   fixed a. κ enters only as the tie's coupling.
2. The background gives no fixed-point condition (A), no gap condition (B), and no finite endpoint energy (the log wall
   diverges, WEEK32PI §1).
3. Hence κ is a free coupling of the class, as F16 says. **Proposition:** no equation internal to this class fixes κ.
   Fixing it needs a microscopic sector that outputs ε_Λ K/a² as a number (Route D), i.e. a theory one level below the action.
This is an obstruction within the stated class, not a universal no-go. A future microscopic sector could still output 16π.

---------------------------------------------------------------------------------------------------------------------------
## Labels

- Route A (cosmic fixed point): CLOSED, theorem (no condition exists). Not R0.
- Route B (gap = H_Λ): CLOSED, theorem (criticality forced by the deep law). Variant B′ closed by power counting.
- Route C (horizon capacity): DERIVATION from a stated premise, giving **κ = 1.447 (q = ½) or 2.894 (q = 1)**. EXCLUDED
  (+12.9σ / +5.3σ, both footings scale together). Also on the rival (event-horizon) branch.
- Route D (local energy matching): REDUCTION. κ = ½ ⇔ ε_Λ = 4a²/G. Rational-C premises cannot hit it exactly, but
  d ≈ 100 equipartition is observationally indistinguishable. Any premise that sets C = 16π by hand is **R0-SHAPED**.
- Nothing here derives κ = ½. Nothing here prefers ½ over 1/2π (F7 stays kernel-conditional).

---------------------------------------------------------------------------------------------------------------------------
## Proposed frozen criteria: the best route (D, local vacuum-energy matching). Commit alone, before any script.

**CFG-D FROZEN CRITERIA (proposed; ID to be assigned from the LEDGER; do not take an ID without asking).**
Question: does a specified microscopic P sector OUTPUT the vacuum-energy-to-response ratio C ≡ ε_Λ K / a² (= 16π for κ = ½)?

Admissibility gates (all required; fail any one ⇒ INADMISSIBLE, not scored):
- G1 Vacuum-blind: the response vanishes identically on the homogeneous background (Theorem A). Check: ū = 0 on FRW.
- G2 Deep law: K W″(0) = 1 exactly, from the model and not set by hand (Theorem B). Check symbolically.
- G3 Shape: rate-potential invariant S = W⁗W″/W‴² = 3/2 at the vacuum (MICRO32PI/COUPLED32PI fingerprint).
- G4 Equation of state: the energy counted as ε_Λ has p = −ε in the SAME state that gives the response (no thermal ε with
  s > 0; MICRO32PI §2).
- G5 No horizon input: no horizon radius, surface gravity, Unruh/Gibbons–Hawking temperature or area enters (Corollary C).
  Exception: a model that also predicts the event-horizon a₀(z) branch must say so and is scored against a₀(z) data.
- G6 No free constant reaches C. Every parameter the model has must cancel from C. Check by MUTATE: vary each parameter
  ×2, and C must be unchanged to 1e-12.

Score (only for admissible models):
- PASS-EXACT iff C = 16π symbolically.
- PASS-DATA iff 33.0 ≤ C ≤ 128.3 (κ ∈ [0.313, 0.617], F3 estimator A ±2σ, canonical footing). Report the alt footing
  separately; never pool.
- Milgrom-footing marker: C = 6π² (κ = 0.461). Report which of 16π and 6π² the output is nearer to, and do not claim a
  preference beyond F7.
- FAIL iff C is outside [33.0, 128.3] (e.g. Route C's C = 6.0 FAILS).
- K1 (tooth): feed Route C's premise through the pipeline and it must FAIL (C = 6.0). Feed C = 16π inserted by hand and
  it must be flagged R0-SHAPED by G6.
- K2: a rational C near 50.3 (d ≈ 100 equipartition) must be reported as PASS-DATA, NOT PASS-EXACT, with the mode count
  disclosed as a knob unless the model derives it.

Kill or close: if no admissible model is found, κ stays FITTED and Route D is recorded as the precise open obligation.
Never write "κ derived" on PASS-DATA alone.
