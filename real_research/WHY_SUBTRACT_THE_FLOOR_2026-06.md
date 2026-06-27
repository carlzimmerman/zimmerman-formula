# Why Subtract the de Sitter Floor? Is Common-Mode Rejection of T₀ DERIVED from Renormalization/Thermo, or the One Irreducible Machian Axiom?

**Date:** 2026-06-27 · **Status:** LOCAL (do NOT git-push) · **Both-ways, framework-internal, NO comparison**
**Footing (sympy-verified this session):** a₀ = cH_Λ/Z = 9.36e-11, Z = √(32π/3) = 5.78881, cH_Λ = Z·a₀ = 5.4183e-10 m/s²,
T(a) = (ℏ/2πk_Bc)√(a²+(cH_Λ)²), T₀ = T(0) = ℏ·cH_Λ/(2πk_Bc) = 2.1971e-30 K; framework's OWN
μ_fw(x) = (√(1+4x²)−1)/(2x), x = a/a₀. **NEVER McGaugh ν. No comparison.** Script `why_subtract_verify.py`, exit 0.

---

## ONE-LINE VERDICT

**RELABEL, ruthlessly confirmed.** Renormalization and equilibrium thermodynamics do NOT independently force the
floor-subtraction. They are GENUINE, physics-mandated principles — but each one fires only on the **gauge** sector
(energy / free-energy / work, where the observable enters dynamics through *differences*, so the shared constant T₀
cancels and "subtract the a=0 value" is content-free and forced). Inertial mass is **not** a gauge quantity — it enters
as F = m·a, so its absolute level at a=0 is a physical fact, not a scheme choice. On the one channel where the
subtraction actually carries content (the inertia channel, the actual claim), renormalization does **not** fire and
thermo forces only the negative half. **The common-mode rejection of T₀ therefore stays the ONE irreducible Machian
axiom (A2 of `DERIVE_THE_SIGN`), now confirmed NOT renormalization-forced and NOT thermo-forced.** The theory rests on
**EP + the bath + the already-banked preferred frame + that one named premise.** Still one-parameter (Z free, like G);
SM walled; not a TOE. Live door stays open.

---

## THE THREE QUESTIONS, ANSWERED (sympy, framework footing, both-ways)

Three probes were run independently this session (`renorm_probe{,2,3}.py`, `probe2_thermo_operational.py`,
`probe2_crux.py`, `probe3_*.py`), all sympy-clean. Their crux re-verified here in `why_subtract_verify.py` (exit 0):
footing exact (cH_Λ=5.4183e-10, T₀=2.1971e-30 K, Z=5.78881); dT₀/da=0; T(0)=T₀; excess=√(T²−T₀²)=K·a exact;
d(excess)/da|₀=K (finite, responds). All three probes converged. Two returned **SMUGGLES-relabel**; one returned
**partial** (negative half forced, positive half not) — which is the same split, read from the thermodynamic side.

### (1) Is T₀ genuinely the universal vacuum/zero-point piece that renormalization MANDATES subtracting? — **NO. "T₀ = the vacuum" smuggles the subtraction.**

Renormalization fixes that *some* constant is subtracted; it does **not** fix *which* reference point. Write the
renormalized inertial self-energy m_ren(a) = g(T(a)) − g(T(a_ref)). The reference a_ref is a **free renormalization
point** — sympy: m_ren(a_ref) = 0 by construction for *any* a_ref. Choosing a_ref = 0 (subtract the floor) and asserting
m_ren(0) = 0 (floor body inertia-free) is a **scheme choice**, not a forced one.

The three structural properties that make vacuum-subtraction a FORCED operation in QFT all **FAIL** for T₀:

- **(i) Not a divergence.** Normal-ordering's "remove the infinite zero-point" mechanism applies to a *divergence*. T₀ is
  **FINITE** (2.20e-30 K). There is no infinity to subtract, so that license does not apply.
- **(ii) The absolute value COUPLES to observable dynamics.** Vacuum energy is renormalizable-away precisely because its
  absolute value couples to nothing. Here it couples: R_abs = T/T₀ gives m_I(0) = m_rest (a Newtonian/anti-MOND low-a
  regime); R_rel = (T−T₀)/T₀ gives m_I(0) = 0 (MOND). Sympy: the two **DIFFER at every a>0** (their difference is the
  constant 1 — R_abs − R_rel = 1 — so it shifts the *entire* a≳a₀ curve, e.g. at a=a₀: R_abs=1.0148 vs R_rel=0.0148).
  The subtraction **changes the a>0 observable**, so it is not the content-free gauge move.
- **(iii) The a=0 "vacuum" is NOT a non-responding ground state.** A UDW detector at rest in the dS vacuum still sees the
  Gibbons–Hawking bath and clicks at rate n(ω,T₀) > 0. T₀ is *real thermal response* (the non-removable category), not a
  subtractable detector self-energy c-number.

So "T₀ = the vacuum, subtract it" borrows the *word* "vacuum" but none of the three properties that make
vacuum-subtraction forced. It is the Machian common-mode-rejection axiom in renormalization costume.

### (2) Does equilibrium / operational thermodynamics force it independently? — **PARTIAL: forces the negative half only.**

Equilibrium thermo + the operational m = F/a force the **negative half**: detailed balance gives the floor zero NET
heat/force at a=0 (KMS current J(T_body=T₀)=0), and an isotropic equilibrium bath exerts zero NET push on a body at rest
(∮cosθ dΩ = 0). So the floor sources no SUSTAINED force-response, and the force-responsive / work-doing piece is the
anisotropic EXCESS = K|a| (sympy: d(excess)/da = K finite vs d(T₀)/da = 0). That much is REAL grounding — the floor
genuinely *is* the no-net-work / no-net-force / detailed-balance baseline.

It does **not** force the **positive half** — that the floor body carries *zero dynamical inertia*. Inertia is a
**reactive** response that does zero net work over a cycle *by its very nature*. Sympy: for any periodic motion,
∮ m₀·(ẍ)(ẋ) dt = 0 for **any** m₀. So "the floor does zero net work/heat" does **not** exclude a floor reactive mass m₀
— the anti-MOND R_abs=T/T₀ reading carries a reactive floor inertia m₀ that is *equally* net-work-free yet still shifts
F/a. Equating "force-responsive" with "net-work-doing" smuggles the conclusion. The thermo route REACHES, but does not
dissolve, the same A2 clause.

### (3) RUTHLESS TEST: is "subtract the a=0 reference" a genuine universal principle physics mandates, or the Machian choice renamed? — **GENUINE for the GAUGE sector; RENAMED for the NON-GAUGE (inertia) sector that is the actual claim.**

This is the decision, and it is sympy-decisive. Renormalization *is* real physics — but it forces "subtract the a=0
value" **only where that value is GAUGE**, i.e. where the observable enters dynamics through DIFFERENCES so the shared
constant cancels from every prediction:

- **GAUGE sector (energy / free-energy / work) — FORCED, genuine.** Energy enters as dF/dx. Sympy: the force read off
  from E and from E_ren = E − T₀ is **identical** (d(E−T₀)/da − dE/da = 0). The zero-point/equilibrium constant cancels
  from every force. Here "subtract T₀" is content-free, forced, gauge. Renormalization is **not a fiction** — applied to
  energy it correctly fires. Credit this fully.
- **NON-GAUGE sector (inertial mass) — NOT FORCED.** Inertia does not enter through differences: it enters as F = m·a,
  so its *absolute* level is observable (a coasting body either has inertia 1 or 0 — a physical fact, not a gauge
  choice). Sympy: R_abs and R_rel give DIFFERENT inertia at a>0 (differ by the constant 1). Applied to a non-gauge
  quantity, the renormalization principle **simply does not fire**.

The framework subtracts anyway — and that single, **SELECTIVE** firing is the tell. The framework subtracts the a=0
value of *exactly one* thing: the acceleration-channel inertia (m_I(0)=0). It **KEEPS** the a=0 value of everything else
— the s^TX boost dipole (s^TX(v,a=0)≠0 is the Cassini-tested datum), velocity/position wrt u^μ, and **decisively, T₀
itself** (the framework reports T₀ = 2.20e-30 K as a REAL temperature — the exact OPPOSITE of renormalizing it to zero).
If "subtract a=0" were the universal renormalization principle it claims to be, it would also have to zero s^TX(a=0) and
T₀. It does not. The subtraction fires on the one channel where it is **not** gauge — and that firing IS the common-mode
rejection of T₀, the Machian axiom A2, renamed.

The thermo "equilibrium does no work" angle collapses identically: "no work" genuinely forces only that *work* uses
(T−T₀) [gauge]; to get m_I(0)=0 you must ADDITIONALLY assert m_I = the work-doing part only — and that extra
identification IS A2.

---

## THE DECISION — IS THE SUBTRACTION DERIVED, OR THE ONE IRREDUCIBLE AXIOM?

**It stays the ONE irreducible Machian axiom — now confirmed NOT renormalization-forced and NOT thermo-forced.**

Probes 1 (renorm) and 2 (thermo) do **not** add an independent instruction to subtract. They **smuggle** the Machian
choice through the equivocation between **gauge** and **non-gauge** subtraction: both "renormalization subtracts the
vacuum" and "the equilibrium part does no work" reduce to "subtract the a=0 value," which is genuine for the gauge
(energy/work) sector and a relabel for the non-gauge (inertia) sector that is the actual claim. This is fully consistent
with `GROUND_THE_MACH_PREMISE` (the bath supplies T₀ as a real common mode but does not instruct the subtraction) and
`DERIVE_THE_SIGN` (A2 is the irreducible sign-selecting premise) and `INFLUENCE_FUNCTIONAL_DELTAT_INERTIA` (the rejected
R_abs reading IS the passive-bath anti-MOND result the EOS reading escapes only by the A2 choice).

This work does **advance** the grounding by **naming the smuggle precisely**: we now know exactly *why* the
renormalization/thermo framings feel forcing (they ARE forced — on the gauge sector) and exactly *where* they fail to
fire (the non-gauge inertia channel, which is the whole claim). That is a sharper foundation than a bare dangling
sign-posit, but it is **not** a derivation — do not fake one.

### The genuine residue both ways (not papered over)

- **CREDIT (real work the principles do):** Renormalization establishes that common-mode reference subtraction is a
  legitimate, ubiquitous operation, and it genuinely FORCES "subtract T₀" in the energy/work ledger (sympy: forces
  unchanged). Thermo genuinely forces the negative half (the floor is the zero-net-work / detailed-balance / zero-net-
  push baseline; J(T₀)=0; isotropic-bath F_net=0). So the relational reading R_rel is a subtraction of something
  **REAL** (the bath supplies T₀ as a shared common mode) — a real upgrade over a bare dangling sign.
- **WHAT THEY DO NOT SUPPLY (the forcing):** Renormalization never singles out a_ref=0 over any other a_ref, never
  forces m_ren(0)=0 over m_abs(0)=m_rest. Thermo never forbids a net-work-free floor reactive mass m₀ (the anti-MOND
  branch). The decisive disanalogy: inertia's absolute value couples to dynamics (the a≲a₀ regime) whereas vacuum
  energy's does not — so the subtraction is a *physical claim about the low-a regime*, exactly the choice that kills the
  passive-bath/anti-MOND reading and selects MOND.

---

## QUARANTINE (held)

- **Grounds the SIGN only — NEVER a₀ or Z.** The theory stays provably **ONE-PARAMETER**: Z free by κ-closure (like G in
  GR); a₀'s VALUE = cH_Λ/Z is not derived; T₀'s numerical value inherits the posited cH_Λ. Nothing here touches the
  *value*; this is entirely about the *sign-selecting subtraction*.
- **SM walled — NOT a TOE.** No FDR / forced-kernel wall is touched.
- The banked passivity→anti-MOND theorem still stands and is *exactly* what the irreducible A2 clause rejects
  (common-mode subtraction is a state-function selection on a non-gauge observable, not a dissipative kernel).
- **Never "no doors."** The live open door is unchanged and sharp: a first-principles **modified-inertia** reason WHY
  inertia is the work-doing / excess (gauge-like) part over the floor — i.e. why common-mode rejection of T₀ is the
  correct physics over the absolute / passive-bath anti-MOND alternative. Renormalization and thermo do **not** supply
  it; they name it to the millimeter. Forward stays data: the s^TX SME dipole (Saturn 8.68e-10, ~1.5× the combined
  Cassini bound) and the a₀(z) hostage.

---

## WHAT TO TELL CARL (straight)

I pushed the last door — *can renormalization or thermodynamics FORCE the floor-subtraction, so the MOND sign needs zero
standalone Mach axioms?* — and I ran it ruthlessly, both ways, on your own footing (a₀=9.36e-11, your μ_fw, no McGaugh,
no comparison). **The honest answer is: it does not force it. The subtraction stays your one irreducible Machian axiom —
but I can now show you exactly why it kept *looking* forced, and that's a real sharpening.**

Here's the genuine credit, and it's worth taking. Renormalization is real physics, and it DOES fire in your theory — on
the *energy* ledger. Subtract T₀ from the energy and every force is literally unchanged (sympy: zero difference). Same
with the thermo "equilibrium does no work" argument: your floor genuinely IS the zero-net-work, zero-net-push,
detailed-balance baseline — that half is forced and real. So R_rel isn't an arbitrary subtraction; you're subtracting
something the bath actually supplies as a shared common mode.

Here's where it stops, and I won't fake past it. All of those principles force "subtract the a=0 value" **only where
that value is gauge** — where the quantity enters through *differences* and the constant cancels. Energy is gauge.
**Inertial mass is not** — it enters as F = m·a, so whether the floor body has inertia 1 or 0 is a physical fact, not a
bookkeeping choice. Sympy is decisive: the absolute reading and your relational reading give *different* inertia at every
a>0 (they differ by exactly 1). And the tell is that your theory subtracts the a=0 value of *exactly one* thing — the
inertia — while it KEEPS the a=0 value of your s^TX dipole, of velocity-wrt-u^μ, and even of T₀ itself (you report
2.20e-30 K as a real temperature, the opposite of renormalizing it away). A universal "subtract the vacuum" principle
would have to zero those too. It doesn't. So the subtraction fires on the one channel where it's *not* gauge — and that
firing just IS your common-mode rejection of T₀, in renormalization costume.

So the bottom line, straight: **your MOND sign rests on the equivalence principle + the bath + the preferred frame you
already pay for at Cassini, plus ONE named, falsifiable Machian premise — "physical inertia is the excess over the
cosmic floor; the floor body carries none."** That premise is NOT derived from renormalization or thermodynamics — those
fire on energy, not on the non-gauge inertia channel that is the actual claim. It's a cleaner, better-named foundation
than a dangling sign-choice, and it's respectable in exactly the way the EP itself is. It does **not** derive a₀ or Z —
you're still a one-parameter theory (Z free like G), the SM is still walled, this is not a theory of everything. And the
live door is exactly named: a first-principles modified-inertia reason *why* inertia is the work-doing excess (why
common-mode rejection beats the absolute/passive-bath alternative). Renormalization didn't open it — but it's still
open, and it's still the right next thing to push. Not git-pushed.

---

## SCRIPTS (scratch, exit 0)
- `why_subtract_verify.py` — footing (Z=5.78881, a₀=9.36e-11, cH_Λ=5.4183e-10, T₀=2.1971e-30 K); dT₀/da=0; T(0)=T₀;
  excess=K·a exact; d(excess)/da|₀=K. GAUGE: dE/da−d(E−T₀)/da=0 (forced). NON-GAUGE: R_abs(0)=1, R_rel(0)=0,
  R_abs−R_rel=1 (differs at a>0). Reactive cyclic work ∮m₀ẍẋ dt=0 for any m₀ (floor m₀ not excluded by "no net work").
  m_ren(a_ref)=0 for any a_ref (reference point free → a_ref=0 is a scheme choice).
- Prior probes (this session): `renorm_probe{,2,3}.py`, `probe2_thermo_operational.py`, `probe2_crux.py`, `probe3_*.py`.
