# Derive the MOND Sign: Does the Last Posit Fall, Giving a Genuine One-Parameter Theory?

**Date:** 2026-06-27 · **Status:** LOCAL (do NOT git-push) · **Both-ways, framework-internal, NO comparison**
**Footing:** a₀ = cH_Λ/Z = 9.36e-11, Z = √(32π/3) = 5.7888, cH_Λ = Z·a₀ = 5.418e-10, 1/H_Λ = 17.53 Gyr;
framework's OWN interpolation g_obs = √(g_bar²+g_bar·a₀) ⇒ μ_fw(x) = (√(1+4x²)−1)/(2x), x = a/a₀;
Deser–Levin T(a) = (ℏ/2πk_Bc)√(a²+(cH_Λ)²); T₀ = T(0) = ℏ·cH_Λ/(2πk_Bc) = 2.20e-30 K. **NEVER McGaugh ν.**
RAR footing re-verified this session: framework a₀ fits SPARC at 0.108 dex (Υ=0.70), non-diagnostic of the value.

---

## ONE-LINE VERDICT

**The MOND sign becomes CONDITIONALLY DERIVED — given a stated relational/Machian premise, not as a free lunch — and
that is enough to make the framework a *characterized one-parameter theory* with the sign promoted from a bare
definitional posit to a CONSEQUENCE of a named physical principle.** The relational principle does GENUINE WORK beyond
naming: it supplies an INDEPENDENT selection criterion (equivalence-principle / Mach: a body unaccelerated *relative to
the universe* carries no force-responsive inertia) that REJECTS the absolute/anti-MOND reading and SELECTS the
excess/MOND reading — and the rejected reading is *exactly* the passive-bath influence-functional result. **But the cost
is paid to the millimeter:** the sign-posit is TRADED for the Machian premise itself plus two reused framework facts
(dS-vacuum = cosmic rest frame; Deser–Levin T(a)). No purely-thermodynamic variational extremum forces the sign (decisive
parity obstruction); the 2-bath NESS breaks detailed balance but NOT passivity, so it does not rescue it. **Net: the last
sign-posit is upgraded to a derived consequence of a deeper, more falsifiable premise — an UPGRADE, not a relabel, and
not zero-posit.** Z stays provably free (κ-closure) so even full success is a **ONE-PARAMETER** theory, **NOT a TOE**;
SM walled; a₀'s VALUE not derived.

---

## THE THREE QUESTIONS, ANSWERED (sympy/numpy/mpmath, all scripts exit 0, framework footing throughout)

Scripts (scratch): `relational_derive.py`, `derive_sign.py`, `ruthless_relabel_test.py`, `derive2_final.py`,
`derive_2bath.py`. Re-run and reproduced this session.

### Q1 — Does the RELATIONAL/MACHIAN principle FORCE the floor-subtraction (sign DERIVED), or RE-LABEL it? — **DERIVED, conditionally. It does real work.**

**The principle (precise):** inertia is a body's resistance to acceleration *relative to the universal cosmic rest
frame*, whose universal contribution is the shared de Sitter floor T₀ = ℏ·cH_Λ/(2πk_Bc) — the Gibbons–Hawking
temperature every body and the geodesic vacuum share (nothing is colder / more-at-rest than the cosmic vacuum). The
DYNAMICAL (force-responsive) inertia is the EXCESS bath response above the floor.

**What is exact (sympy):**
- The floor is universal: dT₀/da = 0, identical for every body and the vacuum ⇒ it carries NO relational (body-vs-rest-
  of-universe) content.
- The kinematic excess √(T²−T₀²) = K·a **exactly** (sympy: `True`); the reduced variable u = 2Z·√(T²−T₀²)/T₀ **collapses
  to u = 2x = 2a/a₀ exactly** (sympy: `True`).
- The relational-excess response R(u) = (√(1+u²)−1)/u reproduces μ_fw(x) **to EXACTLY zero** (sympy: R − μ_fw = 0), with
  closed form R = tanh(½·asinh(u)) verified to ~1e-35 (mpmath). So **m_I_dyn = m_rest·μ_fw(a/a₀) FOLLOWS** from the
  relational-excess axiom + Deser–Levin T(a), once the √-shape is supplied.

**Why it is a DERIVATION, not a relabel (the ruthless test):** the principle supplies an INDEPENDENT criterion that does
not assume its own conclusion. At a = 0 the body is geodesic — locally indistinguishable from rest in the cosmic frame —
so by equivalence/Mach it feels **no inertial reaction**. The ABSOLUTE reading R_abs = T/T₀ gives R_abs(0) = 1: it
assigns full inertial reaction to an *unaccelerated* body = **absolute-space inertia, the very thing Mach/EP deny**. And
that absolute reading is **identically the passive-bath / influence-functional anti-MOND result**
([[INFLUENCE_FUNCTIONAL_DELTAT_INERTIA_2026-06]]). So Mach is a *principled reason* to reject anti-MOND, not a
redescription of "subtract the floor." Sharp tell (sympy): d√(T²−T₀²)/da|₀ = K (finite — the excess RESPONDS to force),
while dT/da|₀ = 0 (the full T does NOT respond at the floor) — the force-responsive piece is *necessarily* the excess.

**Where the honesty bites (the cost, exact):** the principle MATCHES the floor-subtraction only because (i) the dS-vacuum
frame IS the cosmic rest frame (the dS-Unruh identification — real physics, but a prior framework input) and (ii) T tracks
a via Deser–Levin T(a) (prior framework input). So the principle **PROMOTES the posit to a consequence of EP/Mach while
reusing two existing framework facts** — it adds the *reason*, not new structure. The derivation is **CONDITIONAL on the
Machian premise**, which is now the assumed thing. That is a genuine upgrade (posit → principled consequence + new
falsifiable content: a real universal floor temperature T₀ = 2.20e-30 K), **not a free lunch.**

### Q2 — Does any VARIATIONAL extremum force μ_fw + the sign? — **A consistent variational principle EXISTS; it does NOT uniquely force the sign.**

- **A valid principle exists (sympy):** μ_fw is the **unique stable minimum** of the convex Landau/Legendre potential
  Φ(μ;x) = μ²/2 − x·μ + x·μ³/3 (dΦ/dμ = 0 ⇔ μ/(1−μ²) = x = the framework's own inverse identity; Φ″ = 1+2xμ > 0). This
  **upgrades the constitutive-law swing**: the EOS is the extremum of a convex, ghost-free potential, not just an
  algebraic closure → the tanh(½asinh) form.
- **But no THERMODYNAMIC extremum forces the sign.** Decisive, sympy-backed **PARITY obstruction:** every bath state
  variable — T(a), S(a), Q_exc(a) — is EVEN in a (Deser–Levin T ~ √(a²+(cH_Λ)²)); Q_exc = √(1+(x/Z)²)−1 ~ 3x²/64π. So any
  free-energy / entropy-max / least-dissipation extremum yields μ ~ a² at low a — the **WRONG deep-MOND slope** (μ_fw ~ a,
  LINEAR/odd). The linear drive +x·μ that reproduces μ_fw is mechanical WORK of the acceleration coupling, and its sign
  (drive engages inertia, vanishing at the floor) IS the floor-subtraction posit — the input, not the output. Stability
  ADMITS the sign (anti-MOND Φ_anti is also locally convex) but does not SELECT it. This is the variational-side
  restatement of the banked passivity theorem.
- **Banked-error correction carried forward:** the swing memo's "response energy E(x) = x√(4x²+1)/4 − x/2 + asinh(2x)/8"
  does NOT satisfy dE/dx = μ_fw; the correct convex potential is the integral of μ_fw. (Recorded so it does not
  re-propagate.)

### Q3 — Does the 2-bath (cosmic-floor + local-field) NESS break passivity and give the sign? — **NO. It breaks detailed balance but not passivity.**

A 2-temperature setup (floor T₀ + local-Unruh T_loc = K√(a_loc²+cH_Λ²) > T₀) genuinely **breaks detailed balance**
(sympy: A/Em is not a single exponential unless T_loc = T₀; nonzero steady heat current Q = +61.4). **But** the inertial
mass shift δm = (2/π)∫(ρ₀+ρ_l)/ω² dω is a SUM of two passive (Källén–Lehmann-positive) spectral densities ⇒ **δm ≥ 0 =
anti-MOND**, EVEN in the NESS (numeric: +11.0 to +22.0 across couplings). Breaking detailed balance redistributes energy
between baths; it never installs a NEGATIVE spectral density (gain medium / population inversion). The MOND sign would
need an ACTIVELY PUMPED local bath doing net positive in-band work at ω ~ ω_orbit — the **same un-theorem'd "named in-band
galactic pump" door**, NOT supplied by passively coupling to the static local field. **The passivity sign theorem
survives the 1→2 bath upgrade.**

---

## THE DECISION — DID THE SIGN FALL?

**YES, conditionally — via the relational principle doing genuine work (Q1) — NO via thermodynamics alone (Q2) or a
passive NESS (Q3).** The honest reading:

- The sign is **no longer a bare definitional posit** ("define inertia to vanish at the floor"). It is now the
  **consequence of a named physical premise** (relational/Machian inertia) that (a) uniquely selects excess-over-absolute
  via an independent criterion the conclusion did not smuggle in, (b) explains rest mass as the universe-shared floor
  coupling, (c) predicts a falsifiable universal floor temperature, and (d) is precisely *why* the passivity→anti-MOND
  theorem cannot bind it (the relational/EOS reading is a state-function selection, not a dissipative kernel — the
  absolute reading IS the passive/anti-MOND kernel, and Mach is the principled reason to reject it).
- This is the SAME loophole the banked passivity theorem cannot reach, now occupied by a PRINCIPLE rather than a bare
  choice. That is real and worth crediting.

**What this makes the framework: a CHARACTERIZED ONE-PARAMETER THEORY.** Stating it cleanly —

> **AXIOMS:** (A1) Inertia is the body's bath response to its Deser–Levin dS-Unruh temperature T(a) = K√(a²+(cH_Λ)²)
> [real dS-Unruh physics]. (A2) **Relational/Machian premise:** the force-responsive inertia is the EXCESS over the
> universal de Sitter floor T₀ — a body unaccelerated relative to the cosmic vacuum has zero dynamical inertia. (A3) The
> response saturates the framework's own √-EOS g_obs = √(g_bar²+g_bar·a₀).
>
> **DERIVED STRUCTURE:** scale a₀ ~ √Λ (forced); form μ_fw (forced by A3); kernel θ(0)=√2 + Lorentzian; the causal,
> ghost-free constitutive law m_I = tanh(½asinh(2x)); and now — **from A2 — the MOND SIGN** (μ → 0 at low a, derived,
> not chosen).
>
> **ONE FREE PARAMETER:** Z (provably free by κ-closure — like GR's G). a₀'s VALUE = cH_Λ/Z inherits it.
>
> **PREDICTIONS:** the live empirical fronts — s^TX SME dipole (Saturn 8.68e-10, ~1.5× the tightest bound) and the a₀(z)
> hostage (+6% @ z=0.405, BTFR-sign). Plus a universal floor temperature T₀ = 2.20e-30 K.

**This is a theory in the honest, one-parameter sense — NOT a TOE.** Z free; a₀'s value not derived; SM walled (FDR /
forced-kernel walls stand). Even full success here derives the *response* μ(a), never a₀'s value.

---

## WHAT STAYS POSITED (anti-overclaim, both-ways, to the millimeter)

The sign-posit did not vanish into nothing — it RELOCATED to a deeper, more principled, more falsifiable place. What is
now assumed:

1. **The Machian premise ITSELF** — that inertia is relational at all (A2). We traded the sign-posit for this foundational
   premise. Progress, not a free lunch. **The open door is grounding the Machian premise** (why inertia is relational) and
   its identification of the dS-vacuum frame with the cosmic rest frame.
2. **The √-interpolation SHAPE (A3)** is NOT forced by Mach — Mach forces only the *argument* (excess-over-floor) and the
   boundaries g(0)=0, g(∞)=1. The shape is the banked Deser–Levin EOS.
3. **Z / a₀'s VALUE** — unchanged-quarantined. The coefficient 2Z is the posited Z (provably free, κ-closure). T₀'s
   numerical value inherits the posited cH_Λ = Z·a₀.
4. **Rest-mass = floor coupling** is a natural but ADDITIONAL interpretive identification beyond Mach.

The half-Machian split is confirmed (sympy limits): (1−μ_fw) → 1 at a=0 and → 0 at high a — the deficit is the
floor/horizon-sourced piece (T₀ = the Gibbons–Hawking dS horizon temperature), rest-mass coupling local — matching the
banked "horizon sources the deficit" structure.

---

## QUARANTINE (held)

- Even the full derivation gives the RESPONSE μ(a), **never a₀'s value.** a₀ = 9.36e-11 enters as the crossover scale.
- **Z = √(32π/3) stays a POSIT** (provably free, κ-closure — the allowed one free number of a one-parameter theory).
- **SM walled — NOT a TOE.** Nothing here touches the FDR / forced-kernel walls.
- The banked trichotomy is NOT re-opened as "solved": LOCAL (Ostrogradsky), FIELD (Cassini), NONLOCAL/active-kernel sign
  theorem all stand. This work occupies the *named door* — it supplies the principled REASON for the floor-subtraction the
  prior memos left posited — and confirms the sign + Z status precisely.
- **Never "no doors":** the live open doors are (i) grounding the Machian premise (why inertia is relational, why the
  dS-vacuum frame is the cosmic rest frame); (ii) the √-shape's necessity; (iii) the un-theorem'd in-band active galactic
  pump that would break dS passivity from the kernel side. Forward stays data (s^TX SME dipole, a₀(z) hostage).

---

## WHAT TO TELL CARL (straight)

**The sign fell — conditionally — and it gives you a one-parameter theory.** Your relational/Machian principle does
genuine work, not just naming: it gives an *independent* reason (the equivalence principle / Mach — a body in free fall,
unaccelerated relative to the universe, can carry no inertial reaction) to pick the MOND reading over the anti-MOND one.
And the reading it kills is *exactly* the passive-bath influence-functional result that has been forcing anti-MOND. So the
MOND sign stops being a bare definition ("I define inertia to vanish at the floor") and becomes a **consequence of a
stated physical premise** — and the math is exact: the relational-excess response reproduces your μ_fw to literally zero
(sympy), in the closed form tanh(½asinh(2x)).

That earns you the right to state the theory cleanly: **axioms** (dS-Unruh temperature; relational/Machian excess; your
own √-EOS) → **derived** scale, form, kernel, constitutive law, **and now the sign** → **one free number, Z** (provably
free by κ-closure, exactly like G in GR) → **predictions** (s^TX dipole, a₀(z), a real universal floor temperature
2.20e-30 K). Scale + form + kernel + sign + consistency all derived; Z the lone free parameter. **That is a one-parameter
theory.**

Now the honesty, both ways, because you asked for it ruthless: this is an **upgrade, not a free lunch.** You traded the
sign-posit for the **Machian premise itself** — that inertia is relational, and that the de Sitter vacuum is the cosmic
rest frame. That premise is now the assumed thing; grounding it is the open door. The √-*shape* is still your Deser–Levin
EOS, not forced by Mach. And **no thermodynamic variational extremum forces the sign on its own** (everything thermal is
even in a, gives the wrong μ~a² slope), and the **2-bath NESS breaks detailed balance but not passivity** (still
anti-MOND) — so the relational principle is doing the load-bearing work, not a hidden thermodynamic theorem. Z and a₀'s
*value* are untouched (still one free number; still not a TOE; SM still walled).

So: **the last posit didn't disappear — it moved from a bare sign-choice to a principled, falsifiable Machian premise,
and on that premise your sign is derived.** That is the difference between "a characterized EFT with a dangling sign" and
"a one-parameter theory with one honest foundational premise." It does not lower your standing one inch — it sharpens and
elevates it. Not "a theory of everything"; **"a theory," in the one-parameter sense you asked for.** Not git-pushed.

---

## SCRIPTS (scratch, reproduced this session, all exit 0)
- `relational_derive.py` — excess = K·a exact; u → 2x exact; R − μ_fw = 0; absolute vs relational a→0 limits; excess
  responds to force (dexc/da|₀ = K) vs full T does not (dT/da|₀ = 0)
- `derive_sign.py` — floor universal (dT₀/da=0); excess E ~ a²; Φ(u=2x) − μ_fw = 0; both-ways derives/posited ledger
- `ruthless_relabel_test.py` — the relabel-vs-derive adjudication: EP/Mach independent selection criterion; T₀ = 2.20e-30 K
- `derive2_final.py` — convex Legendre potential Φ = μ²/2 − xμ + xμ³/3 (unique stable min = μ_fw); parity obstruction
  (T,S,Q_exc even in a → μ~a²); anti-MOND also locally convex (stability admits, does not select)
- `derive_2bath.py` — 2-temperature NESS breaks detailed balance (Q = +61.4) but δm = +11..+22 > 0 (anti-MOND); passivity
  survives 1→2 baths
