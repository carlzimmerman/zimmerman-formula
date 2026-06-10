# THE DERIVATION CHAIN — consolidated status (2026-06-11)

*The chain from the cosmological constant to galactic dynamics, link by link, with each link's epistemic status,
its supporting computation (commit-anchored), and — where a gap stands — the theorem that bounds it and the named
calculation or experiment that would close it. This is the framework's full chain as of tonight; the whitepaper's
second edition carries it as its spine. Status legend: **EXACT** (machine-verified theorem/identity) · **DATA**
(empirically certain, convention-audited) · **CONDITIONAL** (derived given named postulates) · **CONTESTED** ·
**CLOSED-NEGATIVE** (a proven boundary) · **PENDING** (computation in flight).*

## The chain

**Link 0 — Λ exists and is measured.** DATA. ρ_DE from Planck/DESI; the framework's footing is ρ_DE (not ρ_total),
a choice independently converged upon by Verlinde's own §8 caveat and the quasi-dS EG literature (agentP).

**Link 1 — Λ sets a temperature: T_dS = ħH_Λ/2πk_B.** EXACT (Gibbons–Hawking; re-verified in-repo via the Γ_th
blind run, Γ = λ²H/2π²).

**Link 2 — accelerated matter in dS sees T_eff = (ħ/2πck_B)√(a² + (cH)²).** EXACT (Deser–Levin; N1's closed-form
commutator extends it: the massive-field tail is irreducibly two-variable in (κ,β) — trajectory-blindness broken
for every M² ∉ {0, 2H²}). **New theorem (agentQ): T_DL ≡ the Tolman-shifted Gibbons–Hawking temperature**
(√(a²+H²)·|ξ| = H exactly) — the two temperatures in the framework's story are one object.

**Link 3 — the bath knows WHERE a₀ is.** EXACT: κ bends at cH (N3's verdict line); μ_F4 = a/κ has now emerged
spontaneously TWICE as the natural dS interpolating function (the bath susceptibility, agentB/F; the Tolman/Clausius
balance, agentQ). The length scale is not inserted — it appears.

**Link 4 — the coefficient: a₀ = cH_Λ/Z with Z = √(32π/3).** DATA + a live two-candidate contest:
- The framework's Z: data-certain (SPARC-optimal within 0.3% under the locked unweighted metric), π-bearing, underived.
- Verlinde's 6: **CONDITIONAL-derived** (dimension-forced, (d−3)/((d−2)(d−1)) at d=4, zero tunable freedom — given
  five named postulates; agentP). 6 vs 5.789 = 3.65%: empirically degenerate at RAR precision forever.
- **RESOLVED (agentT): O(1)-NULL.** Geometry does NOT force 32π/3: no symbolic match under any of three independent
  breakdown definitions; the candidate spread is ×39 and threshold-set (the spread is the answer); the Killing-failure
  route yields a strengthening theorem instead (the O(x²·Riemann) terms vanish IDENTICALLY in exact dS, so agentQ's
  identity is exact on bookkeeping grounds alone). At a ≲ a₀ the construction ceases to be local — it becomes GH
  thermodynamics of the cosmological horizon (the Λ sector). Z stays data-selected; Verlinde's conditional 6 remains
  the only derivation-flavored candidate; the two are empirically degenerate. Echo #3 recorded: Hr(a) = a/κ = μ_F4.

**Link 5 — the mechanism: how T_eff becomes inertia.** CLOSED-NEGATIVE at the worldline, by theorems, exhaustively:
- δQ = TδS **cannot** do it (agentQ: Clausius consumes T; MOND needs dT/da — the lanes are provably disjoint).
- No bath-coupled worldline does it at ANY order/coupling/size: point (agentF lemma), composite/extended (agentL:
  ε = GMH/c³ = r_g/2R_H — the N² gain IS the WEP violation; 21–28 dex short regardless), non-Huygens tails (N2/N3:
  right SIGN exists — the deficit channel, m²<2H² — but amplitude walls 10⁵–10⁸⁶ and the sign/knee one-field
  contradiction), every coupling route (matter: fifth-force; conformal/clock: Cassini-PPN, 6.7 dex; agentI + inline).
- **What survives as the mechanism target (the spec, sharpened to a sentence):** a FIELD-LEVEL structure coupling
  to dT_eff/da on the inertia side, producing the EXPONENTIAL μ-tail, with an amplitude source outside any
  fraction-limited carrier's energy budget. No published structure supplies it; the repo's construction attempt
  died pre-assembly with the numbers (agentI).

**Link 6 — the effective law (the matter sector).** NAMED: **Milgrom-2022 (time-nonlocal MI) + the exponential
μ-tail** — the first published object to clear every nonrelativistic wall the program has built (agentM: reflex
passed >10¹³ where power-law tails die ×6–10⁹; precession sign-flipped and suppressed; p≡0 acceleration-keyed;
SPARC = baseline; the DR4 fork reshaped with a +4–8% positive-selection branch). The filter is inert; the
exponential tail carries everything — and is therefore what Link 5's mechanism must derive.
**Covariant home (agentU): BUILDABLE, unbuilt** — the khronon/aether lift with the MOND nonlinearity on the
INERTIA side: Cassini Q₂ absent BY ARCHITECTURE (Einstein gravity), PPN passes in pinned corners (α ≲ 8×10⁻⁷),
WEP three-layer verified, no singular-surface analog, agentM's battery transfers <1%, and the MINIMAL cosmological
writing is a₀ = const ≡ the framework's pure-Λ √ρ_DE branch. Inherited opens, named: conservation/causality of the
retarded worldline functional (the MI field's shared death-spot; Schwinger–Keldysh = the route) and lensing
delegated to Link 7.

**Link 7 — the lensing partner.** PROVEN NECESSARY (the 40.5σ metric-passive wall, our own data) and
PHENOMENOLOGICALLY EXISTENCE-PROVED (the superfluid condensate carries lensing as mass and predicted our measured
type-split sign, +0.261 in [+0.119,+0.401] — agentH3) but UNREALIZED: every published covariant carrier fails a
gate (AeST/DEW: Cassini, computed; B-K: Cassini face-value 24–39σ with q_ph = −3/7 exact; the fraction-limited
ultralight carrier: the agentI walls; the sharp phase mechanism: refuted 7.3σ, agentJ — a smooth 2.0σ mass trend
survives with the control inverted).
**UNIQUENESS PROVEN (agentW):** the double-counting theorem holds at 8.7–21.6σ on our own SPARC pipeline (exact
lemma: monotone μ + MI dynamics forces the real partner density to ZERO; lensing demands nonzero at 40.5σ — the
class cannot have both; every ordering/λ escape closed) ⇒ **real-mass partners are excluded as a class for MI
dynamics**. The unique survivor: a METRIC-LEVEL Ψ-channel slip ((μ,Σ)=(1,ν)) — photon-sector realizations are
executed by GW170817's differential-Shapiro test, so the slip lives in the metric (the c_T-preserving
beyond-Horndeski/DHOST branch); solar slip auto-passes ×10⁷; clusters re-fail ×1.97 by construction; the type
split requires a second smooth variable (consistent with agentJ); no published realization exists.

**Link 8 — the quantum derivation (the gate).** CONTESTED-TERMINAL at the algebra level (agentR: 60-paper sweep,
nothing derives the placement) — **now EDGE-WOUNDED at the observable level (agentS, the repo's own unpublished
discriminator):** the center placement reproduces the dS QNM ladder exactly (purely damped, Γₙ = sinh((Δ+n)λ),
4-digit matches, Re ω = 0 selecting θ = π/2 uniquely); the edge FAILS structurally under both dimensional
matchings (t^(−3/2) locked at coefficient level, Δ- and q-independent; one-sided/zero-temperature spectral
support vs required dS thermality; rungs exit the spectrum below ε_c = Δλ). The contest collapses toward the
MOND-favorable center for the sign-relevant object; the edge camp's sole rescue severs its own anti-MOND reading.
NOT unlocked: Z, a₀, the unconditional sign — the gate's derivation step remains with the field.

**Link 9 — the empirical perimeter (what the chain must survive, all ours, all owned end-to-end).** DATA:
SPARC 0.105 dex at the framework a₀; the lensing split at **6.8σ from our own 181k-lens re-measurement**
(validation gate passed both classes); wide binaries degeneracy-limited with the DR4 fork pre-registered three
ways; the solar system as the great filter (it killed F1/Milgrom-99, instantaneous-F4, the B-K face value, and
selected the exponential tail); eight dated falsifiable predictions in the whitepaper.

## The closure statement (honest, both ways)
The chain is **continuous from Λ to the named effective law** — with two links carried by theorems (2, 5-negative),
one by data (4, 9), one conditional-published (4-Verlinde), one named-template (6) — and **broken in exactly three
places**, each now bounded by a theorem or a contest rather than by ignorance: the coefficient (4: two candidates,
degenerate; T pending), the mechanism (5: target specified to a sentence; every worldline route closed), and the
quantum gate (8: contested; S pending). A complete TOE claim requires closing 5 and 8 and adjudicating 4. Nothing
published or computed tonight closes them — and everything computed tonight makes them *smaller and sharper* than
they have ever been. All chain slots are now resolved; the sole remaining in-flight computation (agentV, the mechanism's kernel fingerprint) refines Link 5 when it lands.
