# W4-18: exact numbers borrowed from outside gravity (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-18 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Theory lane. **κ = ½ is FITTED.** Not theory closed.

## Why this lane

The owner asked for equations from the rest of physics that might bear on the 4. The record already maps the obvious
borrowings: free-fall c/2 and horizon readings (K345/K352/K375), maximal force (K357; 32π chat lane Y), Isaacson 32π (K081),
the trace share and one-sided ¼ flux (K602), Nariai (K110/K440), Higuchi and the conformal scalar (W4-07), plasma/Jeans/Debye
analogies (32π chat lane X2), nonlinear-eigenvalue thresholds (lane N2), d-dimension continuation (lane F), about 35
published a₀–Λ papers (lane E), and the deep-MOND virial 4/81 (hunt f14/f15). This lane takes the exact numbers that
**no row has tried**, together with the 32π chat's two **unrun** briefs, X4 (Λ thresholds × MOND) and the light part of X5
(lattices of horizons). It uses `agents/W_fresh_ideas/LANE_BRIEFS.md` and edits nothing there.

Lane E's structural result applies to every item: κ² is π-free only if a₀² comes out **linear in a density with no Gauss
or Friedmann factor**. Each item is therefore read for (i) its κ, (ii) the π content of κ², (iii) whether a free parameter or
a menu enters.

## Items and their single declared mapping (fixed now)

Notation: H ≡ H_Λ = √(8πGρ_Λ/3); R* = c/√(Gρ_Λ); κ = a₀/(c√(Gρ_Λ)).

- **B1 parametric resonance (Mathieu).** The first instability tongue of ẍ + (δ + ε cos t)x = 0 sits at δ = ¼, so a mode
  resonates at half the pump frequency.
  - Mapping: the pump is the vacuum's only rate, H (a w = −1 medium has no Jeans or sound frequency, lane X2), and
    a₀/c is the resonant mode at half the pump.
  - Report κ and its π content.
  - Check: Floquet monodromy at ε = 0.02 brackets the tongue edge around δ = ¼, computed numerically rather than assumed.
- **B2 Fisher–KPP pulled front.** v* = 2√(Dr), checked as min_k (Dk² + r)/k.
  - Mapping: the vacuum has no transport coefficient D, so the item is FREE.
  - Secondary reading, declared now: front speed c with growth r = H forces D = c²/(4H); the front's own acceleration scale
    is c²/w with width w = √(D/r).
- **B3 Hardy / BF / complementary-series ¼.**
  - The Hardy constant ((d−2)/2)² = ¼ at d = 3 is the double root of the inverse-square indicial equation s(s−1) + α = 0.
  - The dS₄ complementary-series edge is m = (3/2)H.
  - Mapping: a ¼ of Hardy type needs an inverse-square slot. Check whether the deep-MOND point-mass perturbation operator
    supplies one (its exponents are computed).
  - Edge reading: a₀/c = (3/2)H.
- **B4 Thomson/Eddington π cancellation.** The 8π/3 of σ_T cancels the 4π of a flux, so L_Edd is π-free.
  - Mapping: a₀ is the balance of gravity against the vacuum's momentum transfer to matter. Transfer ∝ (ρ + p/c²).
  - Report it as a function of w.
- **B5 Newton–Hooke duality (Bohlin, Arnold, Kasner).** (a+3)(A+3) = 4 for the force exponents of dual power laws; deep
  MOND (a = −1) is the self-dual point.
  - Mapping: does the duality fix an amplitude? Check whether the dual Kepler coupling k depends on the free
    time-reparametrisation scale s (sympy), and integrate one Hooke orbit through w = z² as a numerical check.
- **B6 mean-field and critical-damping ratios.** Landau Γ₊/Γ₋ = 2, Ginzburg–Landau self-dual κ_GL = 1/√2, critical
  damping γ = 2ω₀.
  - Mapping: these ratios join two branches of one system. κ joins a₀ to ρ_Λ across two sectors with no shared order
    parameter, so the reading is NO SLOT unless a common order parameter is named.
  - Critical-damping reading: a scalar mode in dS is critically damped at m = (3/2)H, the same as B3's edge.
- **B7 lattices of touching horizons (brief X5, light part).** For point masses m on a Bravais lattice with
  nearest-neighbour distance d and volume per site V_s:
  - The single-neighbour pull a_nn = Gm/d² obeys a_nn² = Gρ c² · (V_s/d³) · (Gm/(dc²)).
  - "Touching horizons" means d = 2r_s = 4Gm/c², so the compactness Gm/(dc²) equals ¼.
  - Lattices: simple cubic, bcc, fcc/hcp (V_s/d³ = 1, 4/(3√3), 1/√2).
  - **Declared principles, both reported:** P-cube (the brief's "cubic Wigner–Seitz cell") and P-dense (the brief's
    "densest packing of touching horizons" = Kepler, fcc/hcp).
  - The exact-GR critical compactness of H2 (an elliptic solve and a horizon finder) is NOT run here: it is too heavy
    beside the live 1024³ job and is deferred.
- **B8 Λ thresholds × MOND (brief X4, static part).**
  - Thresholds: zero-force radius and outermost stable circular orbit (OSCO).
  - Laws: Newton, deep MOND, simple μ, standard μ, RAR.
  - For each: the acceleration g(r_thr) and the mean enclosed baryonic density in units of a₀ and ρ_Λ, as M → 0 and
    M → ∞ (mpmath, 30 digits).
  - Is any of them M-independent and equal to a rational multiple of c√(Gρ_Λ)?
  - Turnaround and the Λ-Roche limit are dynamical or tidal and are left to the brief's owner.
- **B9 Maxwellian √π parity flip.** The effusion flux ¼ n v̄ with v̄ = √(8/π)σ shows how Gaussian averages move π by ½.
  - Mapping: a kinetic reading needs a velocity distribution of the source. The w = −1 vacuum has none (no rest frame),
    so the item is VOID.

## Checks (K, must pass)

- **K1:** Friedmann identity κ² = 8π/(3Z²), giving ¼ at Z² = 32π/3 (sympy, exact).
- **K2:** Newton zero-force mean density = 2ρ_Λ and OSCO mean density = 8ρ_Λ, exact.
- **K3:** Bravais volumes per site / d³ = 1, 4/(3√3), 1/√2 (computed from basis vectors).
- **K4:** the Mathieu tongue edge at ε = 0.02 lies within ±0.02 of ¼ (numerical Floquet).
- **K5:** KPP minimum = 2√(Dr) (sympy).
- **K6:** Bohlin duality: a Hooke ellipse maps to a Kepler ellipse with the origin at a focus (numeric, 1e-6), and the dual
  exponents satisfy (a+3)(A+3) = 4 for a = 1 → A = −2 and a = −1 → A = −1.
- **I1:** a forbidden-token scan of the compute block. No literal 0.5, 1/2, 0.25, 1/4, Rational(1, 2), Rational(1, 4) or
  S.Half may appear as a κ input.

## Verdict (frozen)

- **SELECTS:** an item gives κ = ½ exactly from a principle fixed above, with no free parameter and no menu.
- **MENU:** π-free values appear, but only through a choice among declared principles or conventions. Report the members,
  P_LEE with CFG894's rule, and which members lie in W_data (κ_Λ ∈ [0.227, 0.607]).
- **NONE:** neither.
- **Lane verdict:** "AN OUTSIDE NUMBER FIXES THE 4" if any item is SELECTS; "MENU ONLY" if the only π-free route is a menu;
  otherwise "NO OUTSIDE NUMBER FIXES THE 4".
- Every κ is reported against W_data. The data window is one band from CFG493; the footing enters κ only through a₀ and is
  stated for each in-window value.

**Hand expectation (disclosed; most items were estimated mentally before freezing):**
- B1: κ = √(2π/3) = 1.447 (π-odd).
- B2: FREE; the secondary reading gives 2cH, κ = Z = 5.79.
- B3: no inverse-square slot (exponents ±√(l(l+1)/2)); edge κ = (3/2)√(8π/3) = 4.34.
- B4: VOID at w = −1.
- B5: exponent-only.
- B6: NO SLOT.
- B7: P-cube ½ exactly, P-dense 2^(−5/4) = 0.4204, bcc 0.4387. These form a π-free menu of a dust lattice (w = 0), not the
  vacuum.
- B8: Newton gives 2ρ_Λ and 8ρ_Λ with M-dependent accelerations; deep MOND gives g ∝ M^(1/4); no M-independent
  acceleration.
- B9: VOID.
- **Expected lane verdict:** MENU ONLY. B7 is the record's only π-free ½ and comes with its own rival at 0.420.

## Controls (`W4_18_MUTATE=1`, separate outputs, exit 1 when all bite)

- **MU1:** w = −0.9. B4's transfer becomes nonzero, so the item stops being VOID.
- **MU2:** time scale s → 2s. B5's dual coupling changes, showing the amplitude is not fixed.
- **MU3:** touching d = 2r_s → d = r_s. B7's P-cube value moves off ½, so the ½ is a definitional choice.
- **MU4:** Λ → −Λ. B8's zero-force radius and OSCO disappear.
- **MU5:** pump H → 2H. B1's κ doubles.

## Register

One row per item B1–B9, with live ids and classes from CFG894's list, then a `kappa_campaign_lee.py` rerun. Light only
(sympy, mpmath and one small ODE; seconds, one core) while NC2x runs. Nothing downloaded.
