# CFG897 FROZEN CRITERIA: κ door D1, the stiffness term's own vacuum on an expanding background

Written before any script of this lane exists. Committed alone. Block CFG890–899 (orchestrator reservation; CFG897 = κ door
D1 per `campaign_fresh_gravity/LEDGER.md` and commit d6cf5ade0). Rules: `campaign_fresh_gravity/CFG894_kappa_campaign_ledger/
KAPPA_CAMPAIGN_RULES.md`; door text: `KAPPA_DOORS.md` §D1.

Standing facts (rules §0). κ = ½ is FITTED: κ_Λ = 0.417 ± 0.095 (ρ_DE footing), κ_crit = 0.345 ± 0.078 (ρ_crit footing), CFG493.
The two footings are never pooled. Z ≡ κ (Z = √(8π/3)/κ). No de Sitter–Unruh argument is used or cited. GF2's "κ derived" is the
SIS ratio, not the law's κ (AUDIT_GF2, a755b66ca). No knob scans. Identities are checked by construction. Not "theory closed".
Cold energy is real gravitating mass, no particle species. This lane does not touch the 32π chat's empirical-provenance or
Lean work, and it does not overlap p63-C1 (registered, unrun): p63-C1 identifies ρ_Λ with the LINEAR bound charge ∇_μP^μ; D1
computes the QUADRATIC stiffness energy (∝ γ). The ledger register (`kappa_attempts_register.csv`) is NOT edited by this lane;
its row is returned to the orchestrator.

## 0. Disclosure (read, and estimated by hand, before freezing)

Read: KAPPA_CAMPAIGN_RULES.md, KAPPA_DOORS.md, CFG893 README, CFG770 README and FROZEN_CRITERIA, CFG807 README, CFG820 and
CFG821 READMEs, FRAMEWORK_EQUATIONS_2026-10-15.md §1–4, p63 FROZEN_CRITERIA (C1 text only), the LEDGER rows for CFG890–899.

Hand estimates (expectations, not results; the script decides). With the proper norm φ = |P| of a timelike homogeneous
P^μ held fixed, flat FRW, n = d − 1 space dimensions, γ > 0:
- (a) −(γ/2)∇_μP_ν∇^μP^ν gives ε_a = −(γ/2c²)(φ̇² + nH²φ²) ≤ 0;
- (b) −(γ/2)(∇_μP^μ)² gives ε_b = −(γ/2c²)(φ̇ + nHφ)² ≤ 0;
- (c) −(γ/4)F_μνF^μν gives ε_c ≡ 0 (F ≡ 0 for P_μ = (P_0(t), 0, 0, 0));
- at fixed norm the stiffness pressure gives w_s = −1 − 2Ḣ/(3H²) = w_total: the term renormalises G in the Friedmann
  equation (an Einstein-aether-type H² term), by δ = (A/3)(a₀L*/c²)² ≈ 1e-19–1e-15 at |KP| = a₀ (A = 3/2, 9/2 for a, b);
- so a positive dark energy cannot come from (a) or (b) (sign), and even the magnitude alone would need
  κ ≈ √(3Ω_H/A)·c/(L*√(Gρ_DE)) ≈ 1e7–1e9 over L* ∈ [24 pc, 1 kpc] (door's estimate was 1e6–1e8);
- (b) without a constraint has the first integral ∇_μP^μ = C: a w = −1 piece ε = −(γ/2)C² (negative, C free).
The door's own expectation (KAPPA_DOORS D1) was "κ ~ 10⁶–10⁸, EXCLUDED, or vanishing (IDENTITY)".

## 1. Mechanism and assumptions

**Principle (door D1).** The stiffness term that rescues Cassini (CFG770: without it the action fails by 2557× / 3091×) needs
a covariant completion. On FRW the only isotropic background of a vector is timelike, P^μ = (P⁰(t), 0, 0, 0). If its
stiffness energy were the dark energy, T₀₀ = ρ_DE c² with w ≈ −1 would fix a₀ (hence κ) from γ (i.e. L*), H and c.

**Equations taken from the record.**
- Static action (CFG770 FROZEN_CRITERIA; FRAMEWORK_EQUATIONS §1):
  L = −|∇Φ − K P|²/(2K) − ρ_b Φ − W_rem(u) − (γ/2)|∇P|², K = 4πG, u = K|P|, K W_rem′ = u²/(a₀ − u).
- Λ² ≡ γ/K and L*² = 2Λ² (CFG770 K1), so γ = K L*²/2 = 2πG L*².
- Saturation 4πG|P| ≤ a₀ (CFG695; the W_rem wall; u → a₀ only as g_N → ∞) and p63's convention 4πG P⁰ = a₀ for the cosmic state.
- L* window (independent bounds, used to TEST a predicted range, not as an input to κ): L* ≥ 24 pc (CFG820, 95%), allowed up to
  ≳ 1 kpc (CFG691); the old floor 5.75 pc (CFG691/770) reported. CFG821's dSph ≤ 22 pc is conditional and only reported.
- a₀ = κ c √(G ρ_DE) (the law, κ symbolic).

**Added hypotheses (named).**
- H1 (covariant completion): the stiffness is one of the declared covariant structures (§3), minimally coupled unless a
  non-minimal coefficient is named; γ > 0 (required by the static limit's positive gradient energy and by CFG770's real
  screening length Λ² = γ/K > 0).
- H2 (cosmic state): the cosmological P is timelike and homogeneous; its proper norm φ = |P| is set by one of the declared
  normalisations (§3, N1–N4).
- H3 (split): the γ-term's own T_μν is evaluated with the proper norm held fixed (V1). With a norm constraint (Lagrange
  multiplier, Einstein-aether construction) this IS the on-shell T_μν, and any scalar function of the norm (W_rem, the
  multiplier) contributes only a separate −g_μν·W piece. The coupling term −|∇Φ − KP|²/2K and W_rem at the cosmic state are NOT
  re-evaluated: they are the excluded slot class (X2: energy ~ a₀²/G at g = a₀) and the kernel-vacuum class (X10/CFG807:
  ill-defined, free additive constant). D1 asks only whether the new structure γ supplies the dark energy.
- H4 (background): flat FRW, ds² = −N²c²dt² + a²dx², lapse N for the metric variation; H in the matching condition is either the
  de Sitter value H_Λ² = 8πGρ_DE/3 (attractor) or the present H₀ (Ω_H ≡ ρ_DE/ρ_tot = Ω_Λ). Measured H₀ = 67.4 km/s/Mpc and
  Ω_Λ = 0.685 (Planck 2018) enter only at the very end, to turn the finished symbolic κ(L*) into numbers.

## 2. Inputs, footing, ħ, π-parity

- Inputs: G, c, ρ_DE (symbolic), γ = 2πG L*² (L* symbolic, then the independent window), K = 4πG, a₀ = κc√(Gρ_DE) symbolic.
  Pure numbers: only those the covariant algebra produces (n, n², O(1) non-minimal coefficients if named).
- Footing: **ρ_DE (primary)**. The ρ_crit footing is reported separately as κ_crit = κ_Λ √Ω_Λ (same a₀); never pooled.
- ħ: does not enter (classical field theory). Printed ħ-power must be 0.
- π-parity (rules §1.5): the route does NOT use only a₀ and H; it uses γ, i.e. L*. Any κ it returns has the form
  κ = (pure number) × c/(L*√(Gρ_DE)), so it is a TRADE (κ ↔ L*). An exact ½ would need L* = 2√(3Ω_H/A)·c/√(Gρ_DE), a
  horizon-scale constant that no record relation supplies. Declared now: **exact ½ is impossible as a pure number on this route.**
- Forbidden inputs (§2): none used. The script must not contain the footing a₀ values, measured κ values, Z, 0.1727, A₀, or the
  32π premises (I1 grep).

## 3. Option space Ω (declared in full)

**Structures** (door D1 list, plus the general family that reproduces the record's static stiffness):
- (a) L = −(γ/2) ∇_μP_ν ∇^μP^ν  (direct covariantisation of −(γ/2)∂_iP_j∂_iP_j);
- (b) L = −(γ/2) (∇_μP^μ)²  (longitudinal part only);
- (c) L = −(γ/4) F_μν F^μν  (transverse part only; alone it does not stiffen curl-free modes, so it cannot carry CFG770's
  longitudinal screening; listed because the door lists it);
- (G) the general family whose flat static limit is exactly −(γ/2)|∇P|² for all modes:
  L = −(γ/2)[½F_μνF^μν + (∇_μP^μ)² + ξ R_μνP^μP^ν + ζ R P_μP^μ], with (a) = (G) at ξ = −1, ζ = 0 (via the identity
  ∇_μP_ν∇^μP^ν = ½F² + (∇·P)² − R_μνP^μP^ν + total derivative, checked in K3) and "(b)+(c)" = (G) at ξ = ζ = 0.
  ξ and ζ are NOT fixed by the static limit. They are not scanned: the script computes ε(ξ, ζ) symbolically and the coefficient
  that the matching would REQUIRE, and grades O(1) coefficients (|ξ|, |ζ| ≤ 10, declared "natural" bound) separately from
  "a coefficient of 1e15 or more", which is a new hand-set horizon-scale constant (TRADE).

**Normalisations of the cosmic norm φ = |P|:**
- N1: saturated, K φ = a₀ (p63 convention; the maximum CFG695 allows, so N1 bounds |ε| from above at given H for every
  N1b: K φ = u_cos < a₀);
- N2: tether 4πG P = −g_c: on FRW g_c = 0 by isotropy ⇒ P = 0;
- N3: the law's own vacuum R(u) = g_N = 0 ⇒ u = 0 ⇒ P = 0;
- N4: no constraint, no potential: P obeys the stiffness EOM alone ((b): ∇_μP^μ = C, a free integration constant;
  (a): f̈ + nHḟ − nH²f = 0, solved in de Sitter).

**H choice:** Ω_H ∈ {1 (de Sitter, H_Λ), Ω_Λ (today, H₀)}. **L*:** [24 pc, 1 kpc] primary; 5.75 pc reported; L*_needed reported.

**Option-space masses (for the LEE register):** p_data = mass of Ω inside W_data; p_exact = mass at exactly ½.
Expected p_exact = 0 (TRADE form, §2), p_data = 0.

## 4. Computation (sympy, then numbers)

1. Minisuperspace with x⁰ = ct, metric diag(−N², a², …, a²) in n space dimensions (n = 2, 3, 4, 5 explicitly; n = 3 for d = 4),
   P^μ in three parametrisations: V1 P⁰ = φ/N (proper norm φ fixed, primary), V2 P⁰ = q (contravariant fixed), V3 P_0 = −s
   (covariant fixed). Christoffels, Ricci, the scalars of (a), (b), (c), R_μνP^μP^ν, RP².
2. ε = −a^{−n} δS/δN|_{N=1}, p = δS/δa /(n a^{n−1})|_{N=1}, with full Euler–Lagrange derivatives (up to second derivatives).
3. Fixed norm (φ̇ = 0): ε_s and p_s for every structure, w_s, the Friedmann renormalisation δ_s = (A_s/3)(a₀L*/c²)² at N1.
4. Matching (only where ε_s > 0): A_s γ φ² H²/c² = ρ_DE c² at N1 ⇒ a₀² = 3Ω_H c⁴/(A_s L*²),
   κ_needed = √(3Ω_H/A_s) · c/(L*√(Gρ_DE)). Where ε_s ≤ 0 the result is NO SOLUTION (sign); the magnitude-only κ_|.| (same
   formula with |A_s|) is reported for information.
5. N4: (b) first integral and its w; (a) de Sitter growth exponent.
6. Numbers at the end only: κ_|.| and a₀,needed over L* ∈ {5.75, 24, 100, 1000} pc, both Ω_H, both footings (κ_crit = κ_Λ√Ω_Λ);
   L*_needed for κ = 0.607 and 0.227 (W_data edges, ρ_DE footing); the non-minimal coefficient |A|_req that would put κ in
   W_data at L* = 24 pc and 1 kpc.

## 5. Checks (all reported; any FAIL ⇒ VOID)

- **K1** scalar-field sanity of the ε/p extraction (ε = φ̇²/2c² + V, p = φ̇²/2c² − V).
- **K2** static flat limit (Minkowski, spatial P(x)): (a) → −(γ/2)∂_iP_j∂_iP_j; (b) + (c) equals (a) up to a total
  derivative; positive gradient energy for γ > 0.
- **K3** the covariant identity: (a) − ½F² − (b) + R_μνP^μP^ν has identically vanishing Euler–Lagrange derivatives w.r.t.
  N, a, φ (a total derivative) for general N(t), a(t), φ(t).
- **K4** conservation: on the stiffness EOM (N4) and at fixed norm, ε̇ + nH(ε + p) = 0 for (a), (b) and the Ric/R terms.
- **K5** held-fixed convention: V2 and V3 with the norm constraint (multiplier λ fixed by the P EOM) reproduce V1's ε and p
  exactly; the naive V2/V3 values without the multiplier are printed (off-shell, not used).
- **K6** general d: ε_a = −(γ/2)nH²φ²/c², ε_b = −(γ/2)n²H²φ²/c², ε_c = 0 at n = 2, 3, 4, 5 (fixed norm).
- **K7** literature cross-check (consistency only, not an input): the fixed-norm results take the Einstein-aether form
  ε = −3αm²H², p = αm²(2Ḣ + 3H²), α = β₁ + 3β₂ + β₃ (Carroll & Lim 2004, "Lorentz-violating vector fields slow the universe
  down"), with β₁ = γ/2 for (a), β₂ = γ/2 for (b), β₃ = γ/2 for ∇_μP_ν∇^νP^μ.
- **K8** dimensions of κ_needed, a₀,needed, δ_s (SI units cancel).
- **I1** self-grep for the §2 forbidden constants (fail on any hit). **I2** κ_needed symbolic: print its dependence on G, c,
  ρ_DE, L*, ħ (non-zero L* dependence ⇒ TRADE). **I3** scaling G → λG, ρ → μρ, c → νc at fixed L*: κ_needed is invariant only if
  L* scales as c/√(Gρ) (printed). **I4** rename test: law's κ set to 0.4: a₀,needed and κ_needed must not move; the fraction
  ε_s/ρ_DE c² ∝ κ² must move (consistency relation). **I5** no Friedmann tautology: the result is not Z² = 32π/3 and depends on
  L*. **I6** declared footing only. **I7** ħ-power 0. **I8** π-weight of κ_needed²'s numeric prefactor printed (TRADE class).

## 6. Mutation control (`CFG897_MUTATE=1`, separate outputs `cfg897_MUTATE.out`, `cfg897_results_MUTATE.json`)

Each tooth must move as stated; the run exits 1 when all bite (chain6 convention) and 2 (VOID) if any does not.
- **M1** γ → 0 (stiffness dropped, CFG770's M1/C0): every ε_s → 0, no κ of any kind (κ_|.| → ∞).
- **M2** d = 4 → 5 (n = 3 → 4): |A_a| 3/2 → 2, |A_b| 9/2 → 8; κ_|.| × √(3/4) (a) and × 3/4 (b); signs unchanged.
- **M3** saturation at 2a₀ (Kφ = 2a₀): |ε_s| × 4 at fixed a₀; κ_|.| × ½.
- **M4** γ → −γ (the sign the static limit forbids): ε_a, ε_b turn positive, so NO SOLUTION becomes a real (huge) κ of the
  same magnitude. Shows the sign verdict is computed, not hard-coded.
- **M5** K = 4πG → 8πG in u = K|P| and γ = K L*²/2: γφ² ∝ 1/K, so |ε_s| halves and κ_|.| × √2.

## 7. Second prediction (S4)

The same fixed-norm stiffness fixes G_cosmo/G_N = 1/(1 + δ_s), δ_s = (A_s/3)(a₀L*/c²)² = (A_s/3)κ²(L*√(Gρ_DE)/c)², testable
against BBN/CMB bounds on G_cosmo (|ΔG/G| of order 0.1). Expected δ ≈ 1e-19–1e-15: consistent and untestable, p_second ≈ 1.

## 8. Entry screen (rules §3), as assessed before computing

S1 c enters through the covariant completion (∇₀ = ∂_t/c) and the expansion (H/c): PASS. S2 counterfactual: the matching
would move with κ through φ = a₀/K: PASS (N1); N2/N3/(c) are identities by construction and are graded so. S3 stated for general
d (K6, M2). S4 §7. S5 not a one-parameter reparametrisation. S6 the γ-term has no additive constant; the N4 (b) branch's C is a
free zero mode (graded CONDITION). S7 not in an excluded class (stiffened action, not the unstiffened QUMOND/BIMOND class; the
slot and kernel-vacuum pieces are explicitly not used). S8 the condition reads ρ_DE(z); whether the stiffness energy does is an
output (expected: it tracks H(z)², the rival's scaling).

## 9. Outcome classes (frozen)

Per variant (first that applies):
- **VOID** a check fails or a tooth does not bite.
- **IDENTITY (vanishing)** ε_s ≡ 0 for every κ ((c), N2, N3, or a tuned zero of ε(ξ, ζ)).
- **CONDITION** the energy is set by a free integration constant (N4 (b)).
- **NO SOLUTION (sign)** ε_s ≤ 0 for every history at γ > 0, so T₀₀ = +ρ_DE c² cannot hold.
- **MISS (TRADE, magnitude)** ε_s > 0 possible but κ_needed > 0.607 for every L* ≤ 1 kpc with O(1) coefficients; additionally
  EXCLUDED outright if L*_needed > 1 Mpc (any L* that large screens every galaxy, CFG820 K1: L* → ∞ gives Newton).
- **CONSISTENT (TRADE)** κ_needed ∈ W_data = [0.227, 0.607] (ρ_DE) for some L* in [24 pc, 1 kpc] with O(1) coefficients.
  Never a derivation (κ depends on L*).

Overall label (rules §7 class):
- **CLOSURE** iff no variant is CONSISTENT (expected: "the stiffness term is the dark energy" excluded on sign, equation of
  state and magnitude);
- **CONSISTENT (not significant, TRADE)** iff any variant is CONSISTENT;
- **VOID** iff any check or tooth fails.
EXACT CANDIDATE is unreachable on this route (§2). κ = ½ stays FITTED in every case.

## 10. Kill / stop conditions and resources

Single core (`OMP_NUM_THREADS=1 nice -n 10`), one process, < 1 GB, seconds. No downloads. Inputs are symbolic plus the end
conversion constants. Commits touch only this lane dir. Not "theory closed".
