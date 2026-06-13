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
(√(a²+H²)·|ξ| = H exactly) — the two temperatures in the framework's story are one object. **THE QUANTUM-MECHANICAL FOUNDATION (agentWW, 2026-06-13, a 5-agent adversarial workflow — Carl's QM-bridge directive): STRUCTURAL-BRIDGE (both routes CONFIRMED).** The framework HAS a genuine quantum-mechanical foundation — it is NOT ad hoc — and it is named precisely: the **type II₁ de Sitter observer algebra** (the Witten crossed product, arXiv:2112.12828; CLPW arXiv:2206.10780), whose modular flow of the Gibbons-Hawking state IS the static-patch Killing boost (KMS at β=2π/H). The LOAD-BEARING IDENTITY (machine-verified, independently re-checked): **T_modular − T_DL = 0 symbolically on all a∈(0,∞)** — the Link 1→2 chain T_dS=ħH/2π → T_DL=(ħ/2πck_B)√(a²+(cH)²) IS the boost-KMS modular temperature of the GH state Tolman-blueshifted onto a boost orbit of acceleration a (limits: a→0 gives H/2π Gibbons-Hawking, H→0 gives a/2π Unruh — both reproduced). DSSYK (Xu arXiv:2403.09021) is a concrete 1d quantum-mechanical microscopic model in the SAME type II₁ class — the framework's candidate UV quantum completion via agentUU's φ. **THE HONEST GRADE: STRUCTURAL, not DERIVATIONAL** — the algebra REPRODUCES Deser-Levin/Gibbons-Hawking (a quantum FOUNDATION), it does NOT derive a₀ (H is input = the dS radius/Λ; the acceleration a is a worldline choice; Z is untouched, quarantine held; c_χ and the whole MOND/acceleration sector are absent from the dictionary). KEY ASYMMETRY: Route 1 (modular) reaches Link 2 (the full Deser-Levin temperature) and stands WITHOUT φ; Route 2 (DSSYK) reaches Link 1 only and is φ-conditional. **So the framework's semiclassical spine is the SHADOW of a genuine quantum operator-algebra structure (the type II₁ observer algebra) — a real QM foundation — but deriving the a₀ SCALE from it remains open.** The named next calc (the only known route to a derivational upgrade): the dressed observer's crossed-product free energy / relative entropy along a boost orbit — does its variation single out a∼cH as a thermodynamic extremum WITHOUT φ (forcing the inertial transition scale), or is the scale external? **ANSWERED (agentYY, 2026-06-13, a 5-agent adversarial workflow): STRUCTURAL-CEILING-CONFIRMED — the type II_1 QM foundation REPRODUCES but cannot DERIVE the a0 scale.** Both thermodynamic objects along the boost orbit are strictly MONOTONE in the acceleration a, with NO interior extremum and NO transition at a~cH (machine-verified, both routes CONFIRMED): (Route 1, free energy) F(a) = -S0 sqrt(a^2+H^2)/2pi, dF/da = -S0 a/(2pi sqrt(a^2+H^2)) has its only zero at a=0 (the Witten observer-energy term E/T is a-invariant — proper E and T blueshift by the IDENTICAL Tolman factor and cancel); theorem: F(a)=Phi(T(a)), so an interior extremum needs Phi'(T)=0, but H is supplied only ONCE (the modular offset) and cannot also place Phi'=0 at a~H (holds across 3 energy/entropy assignments + a hostile a-dependent bath; F'' smooth across a=H, no transition). (Route 2, relative entropy) S_rel(rho_a || rho_GH) is strictly monotone increasing, global min at a=0, no turnover; its lone inflection at a*/H = 1/sqrt(2) is EXACTLY the convex algebraic crossover of sqrt(a^2+H^2) (~8x from a~cH at Z=5.789), and the algebra-level Jacobson dQ=TdS INHERITS agentQ's worldline no-go (reduces to the pure Tolman factor), it does NOT evade it. **So the a~cH feature is the ALGEBRAIC CROSSOVER of sqrt(a^2+H^2) reproduced descriptively, NOT a thermodynamic extremum: WW's STRUCTURAL ceiling stands, now sharpened from BOTH thermodynamic sides, and the a0 scale remains an external input (the modular offset H + the worldline choice a).** Crucial convergence: the ONLY remaining derivational candidate for the a0 scale is the modular RESPONSE/DISSIPATION kernel (the modified-inertia/Langevin lane) — NOT any entropy or dQ=TdS object — which is EXACTLY the mechanism (X2's active pump), so deriving the a0 scale and delivering the mechanism are the SAME open problem (the phi dictionary + the c_chi<->H scale-lock). Quarantine held (no extremum at a~cH => no coefficient question arose; q=1/4, Z never asserted; phi never invoked).

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
  difference) — all repaired, claims survived; episode recorded in the memo. **THE LINK 5 CALCULATION RUN
(agentHH, 2026-06-11/12): PROFILE-FOUND (BY TRANSCRIPTION) + GENERATION-OBSTRUCTED (Theorem HH-1) — the mechanism
slot is FILLED but not GENERATED.** The constructive half: an explicit closed-form pump profile EXISTS —
F_req(w) ∝ (c_χw)^(−5/3) e^(−c̃(c_χw)^(1/3)) cos(√3·c̃·(c_χw)^(1/3)+φ̃+π/3) — scale-invariant (C5), b-independent
(C4), and it passes every physical gate with margin (stability A_stab = 1481–2319 vs the 5.716 window — two orders
of headroom; UV-off at 10^(−164000) for solar-system modes; both Cherenkov corners safe; coefficient quarantine
clean, NO Z claims). Machine-record grades (independent re-fit; the saved fitter died mid-edit and is void):
the transcribed response is in the index-1/3 class DECISIVELY (rival indices 599×/1120× worse); c̃ consistent at
1% under the class fit (±12% identifiability systematic at the banked 16-point window); the √3 lock unidentifiable
from disk; the agent's sub-1% precision claim downgraded to UNREPRODUCED (in-flight grids not banked). The
obstruction half, fully machine-backed: THEOREM HH-1 — the khronon's scale-invariant dynamics cannot GENERATE the
fingerprint (the measured read law −ν[(3/2)F + ½sF′]; gain envelopes cancel — an index-1/3 GAIN leaves no
index-1/3 response; every structureless class lands outside (C1) at all orders and couplings; nonlinearity
ε-linear to 0.6%): the only preimages already carry the locked Gevrey-3 pair — **the pump TRANSCRIBES σ_req; it
does not produce it. Link 5's remaining target, final form: THE GENERATOR — what dS-bath/horizon mechanism outputs
the locked pair (ζ̃^(2/3)c_χ^(1/3), the 1/√3 lock, the phase)? The 2π/3 lock angle is cube-root/Airy geometry —
suggestive of horizon heat-kernel structure (direction, NOT banked).** **THE GENERATOR QUESTION SCOPED
(agentLL, 2026-06-12): DIRECTION-NARROWED — the question now has a unique mathematical shape.** Lemmas
(machine-verified, 0 tracebacks): the √3 lock ⟺ the cubic class UNIQUELY (the ratio tan(π/(2(k+1))) is strictly
monotone in the exponent class k — no other class can fake it); the fingerprint class is EXACTLY the Laplace
image of a one-sided NEGATIVE-ARGUMENT AIRY DENSITY (the classical Airy connection formula IS the √3 lock;
closed-form pair verified to 1e-31); the kill list armed (KMS-thermal → index 1, dead; quadratic saddles →
ratio 1, dead; two-sided support → dead). CANDIDATE KILLS AND SALVAGE: the bare b-family caustic is KILLED
honestly (the edge pole cancels exactly; the coalescence is Watson-class linear-endpoint → power law, slope
test 2.000001, robust across κ-readings); the bare dS QNM ladder is killed (pure-imaginary pin). THE SALVAGE
IS THE RESULT: a conversion theorem — a family-edge measure e^(−γx^(−q)) outputs response index 2q/(2q+1),
so index 1/3 ⟺ q = 1/4 UNIQUELY — and the Deser–Levin √x map then converts a FOURTH-ROOT oscillatory edge
measure into the complete fingerprint (end-to-end numeric ratio → 1). q = 1/4 is exactly agentV's σ_req input
class — flagged as REQUIREMENT-MATCH ONLY (the firewall held; not a derivation). **Link 5's generator question,
final form: derive the khronon b-family edge measure ρ(b) — PASS ⟺ ρ carries cos(γ(c_χ−b)^(−1/4)) with
γ_req = 2^(1/4)√H·ζ̃/(4√π·c_χ^(1/4)) (raw, quarantined). The calculation is ANALYTIC (no long compute needed);
survivors ranked: (d)-dressed primary, (b)-as-Airy-spectral-edge folds in, (a)/(c) secondary with fold tests.**
Bug honesty: a factor-3 hand-slip in a closed form caught by the agent's own quadrature gate and corrected. **THE GENERATOR DERIVATION ATTEMPTED (agentMM, 2026-06-12, a 9-agent
adversarial workflow: 2 understand + 3 independent derive routes + 3 hostile verifiers + synthesis):
NEEDS-NEW-INPUT — hostile-verified, all three routes converging, no smuggle surviving.** The bulk specification
does NOT force the fourth-root edge: the generic/free pump on the Deser-Levin b-family produces only a kinematic
simple-pole / Watson-thermal (Rayleigh-Jeans) edge in EVERY route. (A, direct, OBSTRUCTED/CONFIRMED) the raw
amplitude edge is a simple pole, residue -H^2/(32pi^2 c_chi^2); the generic-pump forward density slope converges
to -1, never -1/4 (machine: -0.039/-0.0004/-4e-6/-4e-8 -> 0 for the density, -1.000000 for the amplitude). (B,
resurgence, OBSTRUCTED/CONFIRMED) the free Stokes data is a Gevrey<=1 double-pole Matsubara tower — a DIFFERENT
universality class from the Gevrey-4 ((4n)! ) partner of e^(-zeta u^(-1/4)); an analytic edge map provably cannot
upgrade a linear pole tower into a confluent fourth-root branch. (C, anomaly/modular, NEEDS-NEW-INPUT/CONFIRMED)
the foliation/conformal-anomaly sector is SILENT on the edge (Paneitz Delta_4 is rational -> no branch point; the
modular density is 1/u Rayleigh-Jeans from the boost generator's flat two-sided spectrum) — it relocates the answer
to the untouched free pump kernel Psi and is the source of the overall verdict. THE FIREWALL HELD: the dangerous
u ~ sqrt(c_chi-b) -> u^(-1/2) 'fourth-root' laundering was machine-FALSIFIED in all three routes (the forward
density returns -1, not -1/4); zeta-tilde and (16pi/3)^(1/4) quarantine intact; **the q=1/4 / sigma_req agreement
is therefore a QUARANTINED RESTATEMENT, not an independent consistency check** (the one forward computation lands
non-Airy). **Link 5's TRUE final form after this round: sigma_req ~ e^(-zeta u^(-1/4)) is FREE INPUT — Link 5 stands
as a consistent-but-underivable TRANSCRIPTION awaiting a banked physical mechanism (dS-bath / horizon heat-kernel)
that forces the negative-argument Airy normal form on the pump's own fluctuation kernel Psi; the generic operator
lands non-Airy.** The single surviving next calculation: classify the edge spectral-density normal form of the
pump's OWN fluctuation operator Psi = |phi-tilde(nu)|^2 at b -> c_chi and test for the negative-argument Airy edge
(PASS forces the fourth-root with gamma = gamma_req) — but the mechanism that would supply the Airy ramp is now the
named, unbanked input, NOT a calculation on existing machinery. **THE NEW INPUT SHAPED then TESTED (agentNN +
agentOO, 2026-06-12, two adversarial workflows): MECHANISM-CANDIDATE — the sign axis is now FORCED, a controlled
fold still needs a peaked horizon response.** agentNN named the operator: the fingerprint = a negative-argument
Airy density (LL-2), Airy is the universal connection across a linear turning point / cubic fold, and the sonic
edge b->c_chi is the khronon's own sound horizon; the free khronon is strictly convex (omega''=(k^2+1)^(-3/2)>0,
no fold — MM/NN firewall, re-verified), so the active pump must carry a SIGN-INDEFINITE ROTON higher-derivative
kinetic term creating a dispersion fold (omega''(k*)=0, omega'''!=0; existence machine-verified) to promote the
free thermal simple-pole edge to negative-argument Airy. agentOO then RAN the decisive test — the in-medium
khronon self-energy from the dS horizon bath (Gibbons-Hawking T_dS=H/2pi) — across two routes (one-loop + spectral)
with hostile verification: **FOLD-POSSIBLE-COUPLING-DEPENDENT (both routes CONFIRMED).** The bend SIGN sigma4 < 0
is REAL and, for any passive bath with a super-luminal derivative coupling, FORCED by level-repulsion (the IR
khronon omega^2=c_chi^2 k^2 -> 0 sits below the gapped bath; spectral route sigma4 = -I2 c_chi^2 < 0 reproduced to
~1% by three independent methods; loop route generic over a 12/13 contraction-angle scan, NOT cherry-picked) —
so MM/NN's free-convex kill is DOWNGRADED on the sign axis: the active dS pump DOES bend the dispersion. BUT a
CONTROLLED bounded fold is NOT forced: the smooth Gibbons-Hawking continuum gives sigma6 < 0 (unbounded runaway,
no stabilizer — forced by Cauchy-Schwarz I2^2 <= I1*I3 on the spectral moments, independently re-verified: 0/20000
random positive spectra violate, GH ratios 0.94-0.97 < 1), the edge-coincidence k* is cutoff-free-floating, and
the one thing the spectrum DOES force — a positive thermal mass / gap — works AGAINST a gapless fold; a scalar
trilinear coupling or a sub-luminal khronon lands convex (the firewall). Smuggle guards held (q=1/4 never asserted;
the scalar operator reported convex; coefficient quarantine intact). **Link 5 update: the roton operator is no
longer free on the SIGN axis (the dS horizon bath forces sigma4 < 0), but it is NOT yet delivered — the bare
thermal continuum gives an unbounded, non-edge-pinned fold, so a controlled bounded Airy fold now hinges on ONE
named unbanked input: a PEAKED / internal-scale horizon response (the dS QUASINORMAL-MODE resonance), not on any
further computation with the smooth thermal bath.** Next calc: test whether the dS QNM-resonant (peaked) horizon
response supplies sigma6 > 0 AND pins k* at the b->c_chi edge on the Ai(-w) side; PASS then derives rho(b)/q=1/4
with gamma_req, a featureless-only response leaves the fold unbounded and the generator open. **THE QNM RESONANCE TESTED
(agentPP, 2026-06-12, a 5-agent adversarial workflow): STILL-UNBOUNDED — and the kill ESCALATES to a THEOREM.**
agentOO named the peaked dS quasinormal-mode horizon resonance as the missing stabilizer source; agentPP tested
it (the dS QNM ladder is banked from agentS: purely DAMPED, Re omega=0, Gamma_n=sinh((Delta+n)lambda)) and refuted
it on the merits, both routes CONFIRMED. The QNM response is BROAD/zero-centered, not peaked at finite k: its
Cauchy-Schwarz moment ratio sits at 0.33-0.6 (and <=0.993 even at the infinitely-sharp delta limit; a single mode
saturates at 1.000 but a genuine >=2-rung tower cannot) — the SAME unbounded band as OO's smooth continuum; the
purely-damped modes have quality factor Q(k)≡0 and the only extremum k*=H·Delta/sqrt(c_chi^2+1) tracks the HORIZON,
not the sonic edge; and the self-consistent physical khronon branch SATURATES to a plateau with group velocity
v_g >= 0 in every cell — the dS bath GAPS/FLATTENS the dispersion by level repulsion, it does NOT fold it. **THE
NO-FOLD THEOREM (method-independent, the escalation):** any PASSIVE (rho>=0) self-energy S(x)=sum w_n/(x-W_n^2)
is Herglotz/Pick, so dk^2/d(omega^2) > 0 STRICTLY for any positive spectrum and any bare speed — monotone to all
orders => NO passive bath, QNM or thermal continuum, can fold the khronon dispersion (independently re-verified:
dS/dx>0 over 5000 random positive baths, 0 violations; the branch-end loophole closed). So the controlled fold
provably CANNOT come from the passive response. **The convergence with X2:** this is the SAME conclusion the
causality theorem reached from the other side — X2 forced the medium to be ACTIVE/non-passive, and PP now shows the
FOLD specifically lives in the non-passive sector: the passive part only gaps/flattens. **Link 5 update: sigma4<0
stays bend-FORCED (OO), but a controlled bounded Airy fold provably requires a NON-PASSIVE / squeezed horizon
response with negative effective spectral weight (population inversion) that violates I2^2<=I1 I3 — exactly X2's
mandated active channel — not the passive dS QNM spectrum, which is refuted as the stabilizer source.** Next calc:
test whether the squeezed/pumped dS horizon response (the X2 active reservoir) supplies the Cauchy-Schwarz-violating
weight that bounds the fold and pins k* at b->c_chi; a passive-only completion leaves the generator open by theorem. **THE ACTIVE-RESPONSE TEST (agentQQ, 2026-06-12, a 5-agent
adversarial workflow): PARTIAL-NEEDS-MORE — SELF-CONSISTENT-BUT-UNDELIVERED; the feared OBSTRUCTED outcome is
RULED OUT.** PP's no-fold theorem said the fold must live in the non-passive sector; QQ tested whether the X2
active pump can supply it WITHOUT contradicting X2's own passivity/stability premises. THE KEY RESULT (verified
3 ways): **ACTIVE != ANTI-DAMPED** — passivity is broken by the spectral-weight SIGN (a negative residue / gain,
which CAN violate Cauchy-Schwarz I2^2>I1 I3 to give sigma6>0; independently re-verified, sign-indefinite spectra
violate CS 422/2000 while passive never do), while STABILITY is set by the pole LOCATION (which the residue sign
does NOT move — the pole stays in the lower-half plane, causal, no runaway). So a STABLE, causal, bath-limited
CS-violating window provably EXISTS: the controlled fold is NOT obstructed by X2, and the convergence holds. The
threshold is exact: sigma6* = 1/16, and AT sigma6* the inflection cubic factorizes to 3(u-4)^3/128 — a triple
root at u*=4 with omega^2(k*)=0 (the soft edge), the fold's existence point. BUT delivery is NOT yet shown: the
fold is forced only in DIRECTION (sigma4<0), not MAGNITUDE — and the simple LTI active-gain temporal channel is
BOUNDS-BUT-UNSTABLE (a visible fold needs gain e~O(1) >> the instability onset e_inst~0.015-0.018~O(gamma), putting
a growing mode in the upper-half plane), so that channel is exhausted. **Link 5 update: the controlled-fold
mechanism is SELF-CONSISTENT-BUT-UNDELIVERED — the X2 active pump is provably compatible with X2's passivity
(active != anti-damped; a stable bounded-fold window exists) and the fold is no longer obstructed by any theorem,
but its delivery hinges on ONE named unbanked input: a PEAKED spectral function on the STABLE negative-residue
(active, not anti-damped) branch landing sigma6 >= sigma6* with k* pinned at the b->c_chi edge, plus a
saturated/non-Markovian gain to escape the LTI temporal instability.** Smuggle guards held (q=1/4 never asserted;
the sigma6=0.10 showcase honestly flagged as having no soft edge — identity asserted not derived, caught by the
verifier). Next calc: construct the saturated (non-LTI) peaked active spectral function and test sigma6>=sigma6*
+ edge-coincidence + temporal stability together. **THE SATURATED-GAIN ('maser') TEST (agentRR, 2026-06-12,
a 5-agent adversarial workflow): FOLD-DELIVERED-MODEL-DEPENDENT — buildable + X2-consistent, NOT forced (4 free
knobs); one NEW forced result.** The maser hook delivers exactly two things, both verified: (1) NEW FORCED RESULT —
saturated gain CLAMPS to loss at steady state (g_eff(I*)=kappa exactly, a steady-state identity, machine-verified)
which TAMES QQ's LTI amplitude runaway: the runaway objection is RETIRED, and this is forced not a knob; (2) the
k* SCALE k*~(c_chi/sqrt(a0))H is forced from pre-banked {H, c_chi, a0} (zero new knobs — a clean scale-grade
prediction). BUT the controlled fold is NOT delivered forced: it rests on N=4 FREE dimensionless knobs none of
which the dS pump fixes (the pump sets SCALES ~H; the fold needs RATIOS): (a) a narrow gain-peak ratio k0^2/Gamma
in [0.10,0.30] (the smooth GH continuum is broad, gives sigma6<0 — the narrow peak is the QNM input PP's theorem
constrains); (b) the fold-strength magnitude y=A/(c_chi^2 Gamma) in [1.0,1.3] (pump fixes the SIGN not the
threshold-crossing magnitude); (c) the edge-coincidence k0 = b->c_chi (saturation pins the operating point at the
LASING threshold, NOT the dispersion soft edge — the two pins roam apart 10-266x); (d) a k-RESOLVED/non-Markovian
clamp (scalar laser saturation provably leaves the off-center fold pole in the UHP = unstable). Honesty catch: a
route's verdict word 'DELIVERED' overstated its own body (which says undelivered); the synthesizer banked at the
body's honest reading. **Link 5 update: the controlled roton fold stays SELF-CONSISTENT-BUT-UNDELIVERED — the
saturated-gain construction tames the runaway (forced) and predicts the k* SCALE (forced), but delivery of the
bounded edge-pinned fold needs 4 ratios the pump does not fix; the framework PREDICTS the k* scale and merely
ACCOMMODATES the edge coincidence via one tuned line-shape ratio. The residual burden is now fully concentrated
on a single object: a peaked dS QNM horizon spectral function (PP-constrained: must be active/non-passive) plus a
k-structured saturation — genuinely new physics input, not a calculation on banked machinery.** **THE LAST QNM
DOOR — THE GENERATOR ARC CLOSES (agentSS, 2026-06-12, a 5-agent adversarial workflow): NEEDS-NEW-INPUT, both routes
CONFIRMED; HONESTLY NOT CIRCULAR.** Tested whether the dS horizon's own heat-kernel symmetry FORCES the gain shape
onto the edge surface. A REAL hidden symmetry is found and named precisely — the static-patch SL(2,R)~SO(2,1) /
Tomita-Takesaki MODULAR structure of the Gibbons-Hawking state (the QNM ladder is its lowest-weight discrete-series
rep) — but it PERMITS, it does not FORCE: it is a scale-free DILATION, and (i) the target moment ratio
4 j3/j2^2 = 8*Delta SLIDES with the free rep label Delta (dR/dDelta = 8 != 0, machine-verified — not fixed by the
rep), (ii) under modular flow that ratio carries scaling weight -1 against a scale-DECOUPLED external G_sat
(c_chi-set, not H-set), and a dilation can only force WEIGHT-0 invariants (verified: invariant-for-all-flow <=>
weight 0; here weight = -1 != 0), so NO zero-parameter forcing exists; (iii) it supplies no spatial-k to resolve
RR's clamp (the heat-kernel scale k_H sits ~10^5 BELOW the fold band, k0/k_H ~ c_chi^2/sqrt(a0), re-verified). NOT
CIRCULAR vs PP's killed passive QNM: the 8*Delta ratio is from the passive descendant measure but used ONLY for
the moment-ratio coincidence; the weight-(-1) obstruction is residue-sign-independent so it applies to the ACTIVE
deliverer too — no passive->active smuggle, no manufactured win (the verifier independently reproduced all six
load-bearing numbers). **END-OF-ARC STATEMENT (honest): the generator arc MM->SS is MONOTONE and CLOSED — MM/NN
named the roton operator, OO forced the bend (sigma4<0), PP proved no passive bath folds (theorem, converges with
X2), QQ showed the deliverer must be active-but-stable (active != anti-damped; obstruction ruled out), RR reduced
it to N=4 free ratios + tamed the runaway + predicted the k* SCALE, SS found the last forcing candidate REAL but a
permits-not-forces dilation. THE FOURTH-ROOT FOLD MECHANISM IS BUILDABLE AND SELF-CONSISTENT BUT NOT FORCED BY THE
BANKED MACHINERY: the residual is a peaked, k-resolved, scale-LOCKED active line requiring genuinely new physics —
specifically a c_chi<->H scale-lock (tying the khronon sound speed to a power of H) or a single-scale active
k-resonance — NOT a calculation on existing machinery.** The one external dependency, flagged both ways: the
verdict hinges on c_chi<->H decoupling (structural, not a convention artifact); a future input tying c_chi to a
power of H would shift SS toward PERMITS-MODEL-DEPENDENT. Quarantine held (only signs/ratios/scaling-weights/
pole-locations; q=1/4 never asserted). Quarantine held
(q=1/4, zeta-tilde, (16pi/3)^(1/4) never asserted).
Process record: agent died post-verdict
pre-flush; 5 print-path crashes fixed (prints only, zero compute edits); the keystone scan byte-identical across
2 regenerations; the verifier's own first fitter caught by its own self-validation gate and fixed — the bug-log
culture held through the last layer. ALL FLAGS CLOSED: the legal-mixture escape is DATA-CLOSED (agentBB: best legal mixture +0.026 dex past the SPARC line AND ×21 over the solar reflex via a forced-positive variance pincer that never opens — no sweet spot exists; V's predicted failure fingerprint observed in the data fit). The boundary theorem is now THEOREM + DATA: no linear field-bath, legal/tuned/balanced, carries the rotation curves. Link 5 = the khronon medium, the only object standing. The sign question is CLOSED (agentAA, 26/26 checks): DEFICIT ⟺ M² < 2H² confirmed — the deficit channel is intrinsically de Sitter (flat space gives an excess); V's contrary flag traced to a vector-vs-scalar Yukawa anchor error; V's theorems untouched.

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
NOT unlocked: Z, a₀, the unconditional sign — the gate's derivation step remains with the field. **THE MODULAR KEY APPLIED (agentTT, 2026-06-12, a 5-agent adversarial workflow): CENTER-FAVORED-STRENGTHENED — it moved the wound, not the verdict.** Tonight's agentSS finding (the static-patch SL(2,R)~SO(2,1) / Tomita-Takesaki modular structure of the GH state, QNM ladder = its discrete-series rep) was applied as a fresh key to the placement contest. Both routes (rep-matching + modular/KMS), hostile-verified: the modular/SL(2,R) structure FAVORS the DSSYK CENTER — the center uniquely and exactly fits the discrete-series / KMS-at-fixed-T_dS modular structure (the unique discrete root θ_v=π/2, λ/Δ/n-independent, re-verified; ladder norm (n+1)(2Δ+n)>0), and the EDGE cannot (a new negative result: the edge ring grows ~cosh, NOT principal series). This DEEPENS agentS's edge-wound from a DYNAMICAL t^(−3/2) mismatch to a clean STATE-LEVEL rep-class / forbidden-modular-weight mismatch. BUT it does NOT FORCE the center: (i) the boost is inner/diagonal on the placement label θ_v=cos⁻¹E_v so it cannot rotate edge→center; (ii) the placement label β_w=ln((1−A)/A) SLIDES continuously (re-verified 0.00/1.10/2.94/7.60, edge at the A→0 endpoint) — a writable non-GH chord-algebra edge sector survives (agentR's U_q(su(1,1)) continuum intact). Honesty catches banked: Re ω=0 is a no-ringing FILTER (spans complementary+discrete series), NOT a discrete-series selector; the 'not-a-slide' framing was corrected. **Link 8 update: EDGE-WOUNDED-LEANS-CENTER, still terminal at the algebra — the modular structure FAVORS the MOND-relevant center placement (the contest leans further center, the edge-wound now state-level) but does not exclude the edge; the gate's derivation step remains with the field.** Next calc to convert favored→forced: an algebra-internal Tomita-Takesaki uniqueness statement closing DSSYK↔dS at the state level (forces matter-modular = GH-boost only at the center) — the same structural lock agentSS flagged for the mechanism. Quarantine held (q=1/4, Z, a₀ never asserted). **THE LOCK PROBED — THE TWO DEEPEST GAPS ARE PROVABLY ONE PROBLEM (agentUU, 2026-06-13, a 5-agent adversarial workflow): LOCK-CONDITIONAL-ON-DICTIONARY.** The shared key both SS (the mechanism gain shape) and TT (the quantum-gate placement) named — an algebra-internal Tomita-Takesaki uniqueness closing DSSYK↔dS at the state level — was set up and tested. The machine-checked chain: (P1) the DSSYK double-scaled chord algebra is type II_1 (PROVEN — Xu arXiv:2403.09021, Cao-Gao 2511.01978); (P2) the dS static-patch observer algebra is type II_1 with modular flow = the boost (PROVEN — Chandrasekaran-Longo-Penington-Witten arXiv:2206.10780); (P4) Tomita-Takesaki gives a UNIQUE modular flow per (algebra, cyclic-separating vector) — KMS residual = 0 exact; ⇒ GIVEN a state-level *-isomorphism φ (chord vacuum ↔ GH state, intertwining the flows), TT-uniqueness FORCES both (C1) the center placement θ_v=π/2 (sympy {π/2}) AND (C2) the matter moment ratio R = 4j3/j2^2 = 2141.96 TRANSLATION-INVARIANT — removing agentSS's sliding R=8Δ knob. **The unification (both routes CONFIRMED): the mechanism gap and the quantum-gate gap are NOT two problems — they are ONE single open object, the state-level DSSYK↔dS *-isomorphism φ; one iso forces both (the nondegenerate center fixes first, then the multiplicity-1 discrete-series boost spectrum rigidly locks the weights).** Type-obstruction is RULED OUT (both II_1). BUT φ itself is UNPROVEN at the state level: type-match + spectrum-match at an ASSUMED placement is necessary-not-sufficient (uncountably many non-isomorphic II_1 factors; the published DSSYK↔dS is correlator/entropy/action matching — Marini-Qi-Verlinde arXiv:2604.21014, agentR contested-terminal — never a vector-matching iso; the crossed-product/observer-dressing intertwining is the deep open gap). Two hostile residuals kept: (1) GAP B imports strictly more dictionary than GAP A (KMS+β=2π alone leave a Lorentzian knob, R∈[11,147]); (2) even granting φ, the edge coincidence R=G_sat is NOT forced — R is H-intrinsic, G_sat c_χ-intrinsic, scale-decoupled — a separate c_χ↔H scale-lock remains (the SAME residual SS/RR/TT all hit). **NET: a genuine UNIFICATION (two open problems → one named dictionary φ + one scale-lock), not a closure.** Quarantine held (q=1/4, Z, the coefficient never asserted). **THE SCALE-LOCK RESOLVED (agentXX, 2026-06-13, a 5-agent adversarial workflow): FREE-PARAMETER — the c_chi<->H lock is NOT forced by the khronon EFT; it is genuinely new physics.** UU left the unification resting on phi PLUS one residual — the c_chi<->H scale-lock that would make the edge coincidence R=G_sat automatic. XX tested whether the khronon/Einstein-aether EFT in dS forces c_chi=f(H); both routes CONFIRMED FREE-PARAMETER. (i) c_chi^2 = c123(2-c14)/[c14(1-c13)(2+c13+3c2)] is a scale-free coupling RATIO, d(c_chi^2)/dH = 0 EXACTLY (sympy, H-free) — a protected modulus. (ii) The dS radiative lever is 30-120 decades too weak: dS gives only delta(c_chi^2)~(H/M)^2 (the one-power K-enhancement is T-odd/forbidden), and (H/M)^2 = 1.4e-60 (M=meV) to 1e-123 (M=M_Pl) — an O(1) lock would need M~few*H, absurd; not even RADIATIVE-PARTIAL. (iii) Every symmetry-forced value is luminal c_chi=1, which HURTS (a_edge->inf, the sonic edge DECOUPLES from the fold band); the SL(2,R)/modular ladder is c_chi-blind (khronon massless); GW170817 fixes spin-2 not spin-0. **THIRD ORTHOGONAL ROUTE TO THE SAME RESIDUAL: SS/RR/TT, UU (Tomita-Takesaki), and now XX (the khronon EFT) ALL independently land the identical R-vs-G_sat scale-decoupling — STRUCTURAL, not a convention artifact.** Closing it requires a postulated IR Lorentz-violation scale M~H forcing c_chi=f(H/M) that must survive PPN/Cherenkov — genuinely new Hubble-scale physics, NOT banked-machinery-derivable. UU's two open objects are now phi (unproven, type-compatible) + the c_chi<->H scale-lock (XX-confirmed free/new-physics); the boundary holds, the residual irreducible on existing machinery.

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
