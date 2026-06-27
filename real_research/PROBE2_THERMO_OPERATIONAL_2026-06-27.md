# Probe 2 — Thermodynamic / Operational: does equilibrium thermo + F=ma FORCE the floor-subtraction?

**Date:** 2026-06-27 · **Status:** LOCAL (do NOT git-push) · **Both-ways, framework-internal, NO comparison**
**Footing:** a₀ = cH_Λ/Z = 9.36e-11, Z = √(32π/3) = 5.7888, cH_Λ = Z·a₀ = 5.418e-10; T(a)=(ℏ/2πk_Bc)√(a²+(cH_Λ)²),
T₀ = T(0) = 2.20e-30 K; framework's OWN μ_fw. **NEVER McGaugh ν.** sympy scripts exit 0.

## ONE-LINE VERDICT
**PARTIAL — same split as the GROUND memo, reached from the operational side.** Equilibrium thermodynamics and the
operational m=F/a force the *negative* half (the floor sources no sustained net force/heat at rest) but NOT the
*positive* half (that the floor carries zero **inertia**). The decisive obstruction: **inertia is a REACTIVE response
that does zero net work over a cycle by its very nature** — so "the equilibrium piece does no net work / no net heat"
cannot discriminate the excess-inertia (MOND) reading from a floor reactive-inertia m₀ (anti-MOND/R_abs) reading.
Both do zero net cyclic work. The subtraction of the floor LEVEL stays the irreducible Machian A2 clause.

## (a) EQUILIBRIUM / DETAILED BALANCE — forces the SLOPE/exchange, not the LEVEL/inertia
- sympy: net heat current J(T_body=T₀)=0 at a=0 (KMS detailed balance, zero NET flux). **Real.**
- dJ/dT_body|_eq ≠ 0 → heat exchange genuinely ENGAGES off the floor. **Real.**
- d(T₀)/da = 0 (floor non-force-responsive in slope); d(excess)/da = K sign(a), finite → excess RESPONDS to force.
- **THE TRAP (carried from GROUND memo, re-verified):** R_abs=T/T₀ and R_rel=(T−T₀)/T₀ are BOTH flat at the floor
  (dR/da|₀ = 0 for both). "Flat at floor / zero net work" is SHARED → non-diagnostic of the sign.
- **REACTIVE-INERTIA COUNTEREXAMPLE (the crux, new this probe):** a purely reactive (inertial) force −m·ẍ does
  ∮F·v dt = 0 over a cycle (sympy: 0). Inertia ALWAYS does zero net work. So "the equilibrium/floor piece does zero
  net work" is the signature of EVERY reactive inertial term, **not a reason to drop the floor's inertia.** A floor
  reactive mass m₀ (the anti-MOND R_abs reading) would ALSO do zero net cyclic work while shifting F/a. Detailed
  balance kills the floor's *dissipative exchange*, not its *reactive inertia bookkeeping*. ⟹ does NOT force the sign.

## (b) OPERATIONAL F = m a — forces "no net push at rest," not "no inertia at rest"
- sympy: net force from an ISOTROPIC equilibrium bath = 0 (∫cosθ dΩ symmetry). A body at rest in the cosmic vacuum
  feels NO net push. **Real, genuine.** The work-doing anisotropy scales with excess = K|a| (vanishes iff a=0).
- BUT inertia is the REACTIVE coefficient in F=ma, not the net force from the bath. "No net force at rest" is about
  the SUSTAINED/dissipative push; it does not fix the reactive m₀. So F=ma forces the floor to source no sustained
  force — it does NOT force the floor body to be inertia-free.
- Velocity orthogonality (sympy: dT/dv=0): a coasting body (a≠0... a=0, v≠0) sits AT the floor, excess=0. F=ma asks
  about a, not v — consistent with the acceleration axis being the inertia-defining one, but this is the Machian
  identification being *used*, not *derived*.

## (c) FORCE vs RELABEL — adjudication
- **FORCED (genuine, sympy-backed):** (i) J(T₀)=0 detailed balance; (ii) isotropic-bath net force = 0 at rest;
  (iii) d(excess)/da = K finite while d(T₀)/da = 0 — the force-responsive/work-doing piece IS the excess.
- **NOT FORCED (the residual relabel):** that the floor LEVEL carries zero **dynamical inertia**. This equates
  "force-responsive inertia" with "net-work-doing," which a reactive term refutes (∮=0 for ANY inertial term). The
  anti-MOND reading keeps a reactive floor inertia m₀ that is equally net-work-free.
- **Where it lands:** the operational/thermo route reaches — but does not dissolve — the SAME irreducible A2 clause
  from GROUND_THE_MACH_PREMISE ("inertia = force-response relative to the cosmic rest frame; floor body inertia-free").
  Probe 2 is a SOPHISTICATED RELABEL that genuinely *founds* the choice (the floor really is the no-net-work, no-net-
  force, detailed-balance baseline) but does not *force* it (reactive inertia is exactly the zero-net-work exception
  the argument cannot exclude). This is an UPGRADE of the founding, not a closure of the door.

## QUARANTINE (held)
- Grounds the SIGN-founding ONLY — never a₀ or Z. Still ONE-PARAMETER (Z free, κ-closure); a₀'s value not derived;
  T₀'s value inherits posited cH_Λ. SM walled — NOT a TOE. **Never "no doors":** the live door is still a
  first-principles modified-INERTIA reason the floor reactive m₀ is zero (why common-mode rejection beats the
  reactive-floor anti-MOND alternative). Forward = data (s^TX SME dipole, a₀(z) hostage). Not git-pushed.

## SCRIPTS (scratch, exit 0)
- `probe2_thermo_operational.py` — J(T₀)=0, dJ/dT_body≠0, d(T₀)/da=0, d(excess)/da=K, isotropic Fnet=0, dT/dv=0,
  R_abs/R_rel both flat at floor.
- `probe2_crux.py` — reactive-inertia ∮F·v=0 counterexample; force-vs-relabel ledger; lands on A2.
