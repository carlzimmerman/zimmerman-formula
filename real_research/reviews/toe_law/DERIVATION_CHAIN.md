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
- **LINK 5'S FINAL FORM (agents X + V, convergent, 2026-06-11):** the mechanism is an **ACTIVE, dS-invariance-
  breaking medium — the khronon sector itself — pumped by the Λ/dS energy budget.** Two independent proofs converge:
  Theorem X2 (causality + vacuum passivity force μ̂(0) ≥ μ̂(∞); deep MOND forces the inversion ⇒ no passive vacuum
  closes any causal MI; the channel is irreducibly active, and the invoice names the Λ/dS bath as the only reservoir
  with ×10²–10⁴ to spare) and agentV's positivity theorem (the required kernel exists uniquely but every
  dS-INVARIANT carrier is killed by Källén–Lehmann positivity ⇒ the carrier must break dS invariance = the khronon
  medium, which inherits the computed spectral fingerprint σ_req as its derivation target). **What remains underived:
  one object, one property — the khronon medium's σ_req.** Corollary (NEW PREDICTION): no kernel produces the
  √(a/a₀) onset — μ flattens to const + O(a²) below some a★ (deep-MOND flattening; falsifiable in future deep-RAR
  data). **First data confrontation (agentCC, 2026-06-11): NO-FLATTENING-DETECTED + DATA-INSUFFICIENT in the
  allowed window.** SPARC's deep decade (1179 pts, y < 0.1, reaching y = 2.5×10⁻³) prefers a★ = 0 in every variant
  (both footings, both baseline shapes, shape-only, 87% of galaxy bootstraps); 95% bound a★ ≤ 1.0×10⁻¹¹ = 0.107 a₀
  — a factor ~2 WEAKER than agentBB's band line (a★ < 0.05 a₀), which remains the binding constraint: the allowed
  window is untested by existing kinematics (1 SPARC point below where a 0.05 a₀ floor bites). Below SPARC: dSphs
  sit ON the √ law; the published UFD/MUSE-Faint deviations go UPWARD (wrong sign for the floor); the one
  floor-shaped object (AGC 114905, −0.90 dex, isolated) is inclination-hostage. The only published deep downturn
  (Chae+2021) is environment-keyed = EFE-shaped, not acceleration-keyed = floor-shaped. Decisive test named:
  isolated ultra-deep rotators (e_N ≲ 0.005, g_obs = 0.01–0.05 a₀) — floor ⇒ universal downturn at one g_obs;
  EFE ⇒ none in isolation. **THE SIGMA_REQ SCOPING (agentEE, 2026-06-11): STRUCTURALLY-CAPABLE — for the
  PUMPED khronon (the X2 object); the MINIMAL/free khronon CANNOT, by machine theorem.** Link 5 is now a DEFINED
  CALCULATION. (i) V's positivity kill does NOT re-enter: the khronon admits NO dS Kallen-Lehmann representation
  at all (machine-quantified O(1) irreducible residual on Z-level sets, any measure class, signed included); the
  replacement two-variable spectral representation over E(3)⋊dilatation is derived, with positivity a per-k kernel
  condition and NO rigid basis — V's load-bearing step has no analog at the worldline even though stationarity,
  Bochner positivity, and free-member KMS at κ/2π all survive family-wide. (ii) NEW b-FAMILY THEOREM (sympy-exact):
  dilatation orbits ARE the Deser–Levin family (a = bκ, κ² = a²+H²); the free pullback on every member is
  −H²/[16π²c_χ(c_χ²−b²)sinh²(κτ/2)] — anchored at c_χ=1 on N1's banked conformal kernel. (iii) The free khronon's
  cut tail is IDENTICALLY ZERO (conformal class — an absent object, not a wrong exponent), and the Bogoliubov lemma
  (exact to 1e-30) shows occupations/squeezing cannot touch the dissipation channel: THE PUMP MUST MODIFY THE
  DYNAMICS — X2 re-derived from the worldline side, third convergence. (iv) The required pump fingerprint is
  computed and saddle-verified (contour vs direct 1e-18): Δρ̃_c(ω) ~ A·ω^(−1/3) e^(−c̃ω^(1/3)) cos(√3·c̃·ω^(1/3)+φ̃),
  one-sided, c̃ = (3/4)·2^(2/3)·ζ̃^(2/3) = 2.139/1.969/2.279 (fw/canon/hostile footings; ζ raw from V, the
  (16π/3)^(1/4) quarantine intact); positivity window A_max ≈ 5.7 with the oscillation intact. Matching conditions
  (C1)–(C5) written; the remaining derivation: the scale-invariant gain/dispersion profile g(k_phys/H) of the
  Λ-pumped khronon, checked against (C1)–(C5). HOSTILE NEGATIVE KEPT: the j₀ factor is even-entire in b ⇒
  a²-analyticity at a=0 extends to the WHOLE scale-invariant khronon class — the deep-MOND flattening floor a★ is
  now this route's OWN prediction (agentCC's watch entry 11 is decisive both ways). Bug log: the prior agent's
  STEP-1 script verified nothing (3 bugs: regulator-mismatched trapezoid, collapsed level-set scan, unreduced sympy
  difference) — all repaired, claims survived; episode recorded in the memo. ALL FLAGS CLOSED: the legal-mixture escape is DATA-CLOSED (agentBB: best legal mixture +0.026 dex past the SPARC line AND ×21 over the solar reflex via a forced-positive variance pincer that never opens — no sweet spot exists; V's predicted failure fingerprint observed in the data fit). The boundary theorem is now THEOREM + DATA: no linear field-bath, legal/tuned/balanced, carries the rotation curves. Link 5 = the khronon medium, the only object standing. The sign question is CLOSED (agentAA, 26/26 checks): DEFICIT ⟺ M² < 2H² confirmed — the deficit channel is intrinsically de Sitter (flat space gives an excess); V's contrary flag traced to a vector-vs-scalar Yukawa anchor error; V's theorems untouched.

**Link 6 — the effective law (the matter sector).** NAMED: **Milgrom-2022 (time-nonlocal MI) + the exponential
μ-tail** — the first published object to clear every nonrelativistic wall the program has built (agentM: reflex
passed >10¹³ where power-law tails die ×6–10⁹; precession sign-flipped and suppressed; p≡0 acceleration-keyed;
SPARC = baseline; the DR4 fork reshaped with a +4–8% positive-selection branch). The filter is inert; the
exponential tail carries everything — and is therefore what Link 5's mechanism must derive.
**Covariant home (agentU → agentX): BUILT AT THE EOM LEVEL** — the Galley/SK causal conserving equation of motion
exists (validated to 0.03% against every banked number; energy ledger closed at 10⁻¹⁴; zero pre-acceleration; the
khronon forced twice), conditional on the X2 pumped reservoir = Link 5's medium. **HOSTILE-AUDITED (agentFF):
X2 independently re-derived AND extended to NONLINEAR passive media (energy-conservation proof; 30 adversarial
baths); the EOM survives step/pulse/sign attacks (byte-identical reruns; machine-zero pre-acceleration at the
impulsive limit); the SIGNED ledger shows the reservoir draining SECULARLY at 2.63× the external work in deep
MOND — the X2 invoice direction, independently exhibited by the dynamics. Three framings corrected, no verdict
changes (per-event transient cost is geometry-specific ×7–34 not ~1%; the 0.03% "validation" was a shared-source
regression test — the anchor separately CONFIRMED via a fully independent DE440/JPL/GRAVITY/Planck chain to <0.2%;
the "+15 orders" horizon line is ~8 orders per-galaxy-honest). Residual single-source: the agentE budget 2.47e-15.** Originally:** — the khronon/aether lift with the MOND nonlinearity on the
INERTIA side: Cassini Q₂ absent BY ARCHITECTURE (Einstein gravity), PPN passes in pinned corners (α ≲ 8×10⁻⁷),
WEP three-layer verified, no singular-surface analog, agentM's battery transfers <1%, and the MINIMAL cosmological
writing is a₀ = const ≡ the framework's pure-Λ √ρ_DE branch. Inherited opens, named: conservation/causality of the
retarded worldline functional (the MI field's shared death-spot; Schwinger–Keldysh = the route) and lensing
delegated to Link 7.
**TRANSIENT FINGERPRINT CONFRONTED (agentJJ, 2026-06-11):** R3's "×2.32, unconstrained by current data" is
patched twice — (i) the ×2.32 is the IMPLICIT-μ reading only; the literal (X-4) action EOM gives SUPPRESSION on
the same step (0.70× settled, rising from below; quasi-Newtonian for ~2.6 N_cyc/⟨d(xμ)/dx⟩ orbits from an empty
window): the (X-4) "⟺" breaks off resolved content — an unfixed OPERATOR-FORM convention alongside N_cyc;
(ii) the six Lelli-2015 TDGs (0.2–0.8 internal orbits old) now constrain the EFE-embedded regime: −0.63…−0.68 ±
0.09 dex vs the isolated RAR (the naive "+0.37 dex above" transplant dead ~11σ), −0.13 ± 0.10 vs settled
QUMOND-EFE — consistent with the construction's own EFE-regulated prediction (+0.02…+0.07 dex: the external
line erases the enhancement), NON-DIAGNOSTIC between the two operator readings (0.1–3.1σ across EFE-convention
× zero-point forks). The positive branch lives only in ISOLATED young rotators (+0.3…+1.9 dex vs the COMP
quasi-Newtonian floor vs settled on-RAR: a three-way split, one clean object decides) = watch entry 13.

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
**SCALAR CARRIER CLOSED (agentY): OBSTRUCTED by four machine-derived walls** (the kill is the Hamiltonian-constraint
pollution at 10⁷×, NOT ghosts); survivors: c_T ≡ 1 / α_M ≡ 0 identically; the timelike-only reach of published c_T
classifications (new boundary); and the field-line-bending generators = the morphology dial with agentZ's sign built
in. The unique class narrows again: a VECTOR/SPIN-2 carrier on the same u, or nonlocal operators.
**VECTOR CARRIER CLOSED (agentDD, 2026-06-11): SAME-WALLS — and the closure is sharper than the scalar's.**
Wall 1 genuinely EVADED (the condensate/hedgehog vector slips — a structural capability no scalar has); Wall 2
evaded by construction (c_T ≡ 1, α_M ≡ 0 identically, machine, in-halo with the spacelike condensate present).
But Wall 3 TRANSFERS measured (+2.3×10⁶…+4.5×10⁷ × g_bar at slip-matched amplitude — opposite sign, ×3 smaller
than the scalar's, equally dead 5–7 orders over the double-counting bar) and Wall 4 TRANSFERS in closed form
(the exact lens-only condition's geometric class is α⁶·(slip/Φ′) = 0 — the pollution's irreducible core IS the
slip). **THE KEYING THEOREM (the constructive yield):** the root is not the carrier's spin or stress — it is the
KEYING: any LOCAL Y_a-keyed (y²-keyed) MOND-amplitude Ψ-slip carrier on the u-frame, scalar or vector, sourced or
condensate, pollutes the matter channel at (a₀r/c²)⁻¹ × phantom; δY_a/δΦ — the keying's own lapse response — feeds
the Hamiltonian constraint no matter what field carries the operator. **The carrier must read y NONLOCALLY** —
converging with the matter sector from the opposite direction (M22's filter is time-nonlocal on the same u; X2
forced the matter channel active and history-dependent). *The program's two missing-physics slots have collapsed
into one structural demand: u-frame nonlocality, in both channels.* Surviving candidate space: NONLOCAL/HISTORY
slip operators (the M22-echo — the convergent prime candidate from BOTH sectors), the singular-surface route
(logged, low prior), non-b⊗b spin-2 condensates (keying-argument disfavored, not machine-closed). Banked residue:
the S-counterterm family (zero slip, pure matter-channel feed — a tool no scalar basis had); the GW170817 in-halo
boundary now covers the vector KINETIC sector ((Db)² at unit norm = Δc_T ~ O(1)); the morphology dial is
TWO-CARRIER-ROBUST (the (D·b)-keyed divergence/bending engine carries agentZ's TYPE-IRREDUCIBLE sign with the same
geometric range — a design principle of the operator geometry, independent of the final carrier). Bug log: 2
illegal-normalization dead-ends caught by internal gates (dimensional audit + total-derivative check) before
banking; the matched legal realization reproduced the W-row to all printed digits.
**COSMOLOGICAL BOUNDARY (agentII, 2026-06-11): the naive linear-scale extension of the slip law is KILLED —
convention-robustly** (the framework's own footing gives the SMALLEST kill: ⟨Σ²⟩ = 57 vs the Planck φφ amplitude;
E_G 73σ; Σ₀ᵉᶠᶠ ~230σ; ISW sign-flipped; EFE-regulation short ×112–777; and the required global cap ν ≤ 1.03–1.14
sits below the entire measured galactic range ν = 4.4–306 at overlapping g_bar — the charge's own kill criterion).
The constructive yield CONVERGES with the keying theorem: S_slip needs a second discriminant beyond g_bar
(suppress Σ−1 by ≥50–800× at linear scales, preserve halo ν) — and a HISTORY/FREQUENCY-keyed nonlocal carrier is
precisely the object that can carry one (linear-mode field histories are Hubble-rate; halo histories are
orbital-rate — the same filter that evades the keying wall supplies the discriminant). Three independent results
(DD's keying, II's boundary, Z's dial) now point at the SAME structure. Honest residue: II's near-miss is real
(CDM-like shape, ×4–6 over, wrong z-evolution) and the growth debt (μ = 1 without CDM at linear scales) is a
named open of the assembly, distinct from the slip sector.
**THE NONLOCAL/HISTORY DOOR CLOSED (agentKK, 2026-06-11): OBSTRUCTED — upgraded to a class theorem.** The
make-or-break computed hostilely as charged: on a static background the constraint's response to a filtered key
IS the window's DC weight, and tracking normalization forces it to 1 — the key's value and its constraint
sensitivity are the same number; the pollution reinstates at FULL amplitude. **Theorem KK-1 (static
equivalence):** any time-translation-invariant history key with a differentiable static read gives static field
equations IDENTICAL to the local theory (C_eff = F∘K_static) — DD's keying theorem, the pollution tables, and
the wall-4 slip≡0 closure transfer VERBATIM to the entire time-nonlocal class (certified on the banked agentY
equations: the −2.695e7 row reproduced to 0 / 2.2e-16 for two nontrivial filtered reads). No frequency middle
ground: 1e-7 suppression needs t_w = 111× the age of the universe (the window never fills — no slip); a tracking
window leaves 72–99.6% of the pollution. All three structured escapes fail: derivative-coupled keys read NOTHING
static (K_d ≡ 0 on static fields and circular orbits — 100% tracking error); the S-counterterm family cannot
reach the S-free r⁰ core (new closed form: floor = (slip/Φ′)/[r²(1+slip/Φ′)], identity 1.000000; the
S-irreducible floor +1.1e6…+2.2e7 — 5–7 orders over the bar); spectral/filter-bank keys read statics through
θ(0) = O(few) and the matched pollution is filter-invariant (the θ(0)=0 corner is the derivative key in
disguise). **CORRECTION (supersedes the wording above): the 'u-frame nonlocality in both channels' line is
RETIRED** — X2's nonlocality is a dynamics/causality demand; the lensing job is STATIC, where history is
invisible; the convergence framing dissolved under computation (the DD-block and II-block convergence sentences
above are kept for the record and superseded here). **Link 7 final state:** scalar (agentY), local
vector/condensate (agentDD), and history/filter-keyed (agentKK) realizations ALL machine-obstructed; remaining:
the singular-surface exact route (low prior — KK-1 shows nonlocal dressing cannot assist it), SPATIAL
nonlocality (scoped honestly: NOT closed, but carries no M22-echo or convergence argument), and non-b⊗b spin-2
(unchanged). The lensing exposure stands UNEXPLAINED by every construction route explored to date — a major
narrowing, stated plainly. Both-ways: the filtered class inherits every static success unchanged (ν-tracking,
Cassini ×1.3e7, FRW quietness — the W(0)=0 'tension' was a name collision between the operator function and the
window DC gain, reconciled — and the morphology dial); it is exactly as capable and exactly as dead as the local
class. KK-1 is symbolic — no a₀/footing/weighting enters. 5-item bug log incl. two caught spurious results (one
would have faked the equivalence FAILING, one would have faked the derivative key POLLUTING).

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
