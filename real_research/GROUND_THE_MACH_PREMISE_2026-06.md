# Ground the Machian Premise: Is the Last Sign-Selecting Axiom Reducible, or Irreducible?

**Date:** 2026-06-27 · **Status:** LOCAL (do NOT git-push) · **Both-ways, framework-internal, NO comparison**
**Footing:** a₀ = cH_Λ/Z = 9.36e-11, Z = √(32π/3) = 5.7888, cH_Λ = Z·a₀ = 5.418e-10 m/s² (verified),
T(a) = (ℏ/2πk_Bc)√(a²+(cH_Λ)²), T₀ = T(0) = 2.197e-30 K (verified); framework's OWN
μ_fw(x) = (√(1+4x²)−1)/(2x), x = a/a₀. **NEVER McGaugh ν.** sympy scripts exit 0; numbers reproduced this session.

---

## ONE-LINE VERDICT

**PARTIAL — and the split is sharp.** The Machian premise (axiom A2 of `DERIVE_THE_SIGN_2026-06.md`) is NOT a single
irreducible posit, and it is NOT fully grounded either. It cleanly factors into two clauses with *different* status:

> **A2 = [ EXISTENCE of a physical relational reference u^μ ] + [ inertia is DEFINED by acceleration-EXCESS over the
> floor of that reference ].**

The **first clause is GROUNDED** — it reuses the framework's already-banked, independently-tested preferred-frame
structure (the dS-vacuum = cosmic rest frame, the SME s^TX bridge); the floor T₀ is the Gibbons–Hawking temperature *of
that same frame*. The **second clause is IRREDUCIBLE** — it is the genuine load-bearing posit that selects the MOND
reading and rejects the absolute/anti-MOND reading, and it does NOT follow from the bath, from the EP alone, or from the
preferred frame existing. **So the theory now rests on EP + the bath + the preferred frame it already has, PLUS exactly
ONE standalone Machian choice: that the inertia-defining relation is the acceleration-excess, with the floor body
inertia-free.** That is one honest, named, falsifiable premise — respectable in exactly the way the EP itself is —
not a hidden free lunch and not a fresh metaphysical import.

---

## THE THREE SUB-QUESTIONS, ANSWERED (sympy, framework footing, both-ways)

Scripts (scratch): `ground_mach_verify.py`, `ground_mach_check2.py`, both exit 0. Footing numbers verified:
cH_L = 5.4183e-10, T₀ = 2.1971e-30 K, Z = 5.78881.

### (1) Does the EQUIVALENCE PRINCIPLE force the floor-subtraction (geodesics unmodified)? — Partly. It grounds the SLOPE, not the LEVEL.

The bath delivers the EP boundary for free. For **any** smooth inertia functional F(T(a)):

    dF/da|₀ = F'(T₀)·(dT/da|₀) = 0,   because dT/da|₀ = 0   (sympy: dT/da|₀ = 0 exact)

So "a free-fall body feels **zero force-response modification**" is AUTOMATIC from the bath — and it holds for **both**
the absolute and the relational readings. This is real grounding: the geodesic genuinely already sits in the shared T₀
Gibbons–Hawking bath, so the EP/geodesic-unmodified boundary is not an extra posit. The bath is flat at the floor; every
functional inherits zero force-response there.

**But the EP grounds only the SLOPE (zero force-response at the floor), NOT the absolute LEVEL.** sympy is decisive:

    R_rel = (T−T₀)/T₀ : R_rel(0) = 0   (relational: geodesic carries ZERO dynamical inertia)
    R_abs = T/T₀      : R_abs(0) = 1   (absolute : geodesic carries FULL inertia = anti-MOND / passive-bath)
    dR_rel/da|₀ = 0,   dR_abs/da|₀ = 0   (BOTH share zero force-response slope at the floor)

The two readings agree on the EP boundary (both flat at the floor) and **disagree only on the value at the floor**.
The EP says "free fall is locally indistinguishable from inertial rest → no force-response," which both readings
already satisfy. The EP does **not** say "therefore the geodesic carries zero *dynamical inertia*" — that is the extra
content. **How much of the sign does EP ground?** It grounds the boundary condition (μ has the right behavior *at* a=0
for both signs) but **none of the sign-selection** — the sign is the absolute-level choice, which EP leaves open.

### (2) Is the Machian premise the framework's already-banked PREFERRED-FRAME content? — The EXISTENCE half: yes (grounded). The DEFINITION half: no (irreducible).

A body has **two orthogonal kinematic invariants** relative to the cosmic rest frame u^μ. sympy confirms the
Deser–Levin temperature depends on **proper acceleration only**:

    dExcess/dv = 0,   dT₀/dv = 0   (velocity-independent; the boost axis and the acceleration axis are orthogonal)

- **The BOOST axis (v/c).** This is the banked preferred-frame / s^TX datum. The high-a fractional inertia anisotropy
  μ_fw → 1 − 1/(2x) (sympy series: 1 − 1/(2x) + 1/(8x²)) has amplitude a₀/(2|a|), dipole O(β_cmb)=O(1.23e-3), tested at
  Cassini (a≫a₀) — margin ~1.5× the combined s^TX bound (per `project_sme_lorentz_bridge`). VELOCITY-wrt-u^μ is physical
  here, and the framework already banked that this u^μ is a real cosmic rest frame.
- **The ACCELERATION axis (a/a₀).** This is the Machian / excess datum: excess = √(T²−T₀²) = K·a **exactly** (sympy,
  a>0), so excess > 0 ⇒ μ_fw MOND, O(1) only at a ≲ a₀ (solar-untestable).

**DECISIVE CASE — a purely-boosted inertial body (v≠0, a=0):** the bare preferred-frame statement says "this body MOVES
wrt u^μ" (true; s^TX ≠ 0). Mach's definition says "this body has ZERO dynamical inertia" (excess = 0). These are
**different kinematic axes**; one does not entail the other. A theory can have a preferred frame and keep *absolute*
inertia (standard SME / khronometric backgrounds are preferred-frame yet keep absolute inertia). So:

- **GROUNDED (the shared half):** the EXISTENCE of a physical relational reference is NOT new content. The framework
  banked, via the covariant-lensing no-go and the SME bridge, that u^μ (dS-vacuum / CMB rest frame) is a real cosmic
  rest frame — it is what induces the s^TX dipole. The floor T₀ = 2.197e-30 K is the Gibbons–Hawking temperature *of
  that same u^μ*: a physical, body-independent, shared common-mode baseline, not an arbitrary zero. Mach reuses the
  preferred frame the framework already has and pays for via Cassini. Credit this fully.
- **IRREDUCIBLE (the residue):** "inertia is DEFINED by acceleration-excess over u^μ's floor, and the floor body is
  inertia-free" is strictly MORE than "u^μ exists and velocity-wrt-it is physical." It additionally (a) elevates the
  ACCELERATION axis to be inertia-defining (not the velocity axis), and (b) asserts the floor body carries zero
  dynamical inertia. "Relational inertia" is logically independent of "preferred frame exists."

### (3) Does the BATH AXIOM ALONE entail the relational-excess reading, or leave the absolute-vs-relational fork OPEN? — Leaves it OPEN. Mach is the irreducible 2nd axiom.

The bath does real work, but underdetermines the fork. sympy:

- **What the bath forces for free:** (i) the excess is even in a → the bath is direction-blind, automatic; (ii)
  dF/da|₀ = 0 for any functional → free-fall ⇒ zero force-response modification, automatic; (iii) it DELIVERS T₀ as a
  genuine common-mode (the geodesic vacuum really shares it). So the relational *reference* is intrinsic to the bath —
  the relational reading is PHYSICALLY NATURAL, not ad hoc.
- **What the bath does NOT force:** the absolute level. R_abs = T/T₀ (finite, =1 at a=0) and R_rel = (T−T₀)/T₀ (=0 at
  a=0) are **both smooth, well-defined functionals of the SAME bath**. The bath spectrum CONTAINS T₀ as a value but
  does not INSTRUCT you to subtract it. Subtracting the shared T₀ — common-mode rejection — is a SELECTION the bath
  does not perform on its own.

That subtraction IS the Machian axiom A2. And the rejected reading R_abs is *exactly* the passive-bath /
influence-functional anti-MOND result the passivity theorem otherwise forces (`DERIVE_THE_SIGN_2026-06.md` §Q1, banked
trichotomy). So the bath FOUNDS the premise (hands over the reference + the boundary) but does NOT REPLACE it — the
fork is genuinely open at the bath level, and Mach is the irreducible second axiom that closes it. **It is, however, a
well-founded second axiom: its only job is "reject the common-mode T₀," and the bath supplies T₀ as a genuine common
mode.** This is a subtraction of something real, not an arbitrary one.

---

## SYNTHESIS — WHAT THE THEORY NOW RESTS ON (precisely)

> **The MOND sign follows from: the EQUIVALENCE PRINCIPLE (geodesics carry zero force-response — grounded by the bath's
> flat floor, dF/da|₀ = 0 for any functional) + the BATH AXIOM (inertia = dS-Unruh response T(a), which supplies the
> reference T₀ as a genuine common mode and forces evenness) + the framework's already-banked PREFERRED FRAME (u^μ =
> dS-vacuum = cosmic rest frame, s^TX-tested at Cassini) — with the absolute-vs-relational fork closed by ONE residual
> Machian choice: that the inertia-DEFINING relation is the acceleration-EXCESS over the floor, i.e. the floor body
> carries zero dynamical inertia (common-mode rejection of T₀).**

The premise's components, by status:

| Component of A2 | Status | Grounded by |
|---|---|---|
| There is a physical relational reference u^μ | **GROUNDED** | banked preferred frame; s^TX / Cassini |
| The floor T₀ is a real shared common mode (not arbitrary zero) | **GROUNDED** | bath = GH temp of u^μ; sympy: geodesic shares T₀ |
| Geodesics carry zero force-response (EP boundary) | **GROUNDED** | bath flat at floor: dF/da|₀ = 0 (both readings) |
| Direction-blindness (even in a) | **GROUNDED** | bath: excess even in a |
| Inertia-defining axis = acceleration, not velocity | **IRREDUCIBLE** | — (orthogonal to s^TX; sympy decisive case) |
| Floor body is inertia-free (subtract the common mode) | **IRREDUCIBLE** | — (selects MOND, rejects passive anti-MOND) |

**This is a cleaner foundation than "a bare dangling sign-posit."** Four of the six clauses are now grounded on banked,
independently-tested structure (EP + bath + the preferred frame the framework already pays for via Cassini). The sign
no longer rests on six standalone assumptions — it rests on EP + the bath + the preferred frame, **plus one
two-part-but-unified standalone Machian premise (the inertia-definition: acceleration-excess, floor-body inertia-free).**

**It is NOT fully grounded.** The honest residue is the inertia-DEFINITION half. Saying "Mach = the preferred frame,
fully grounded" would over-claim — it would smuggle the sign back in for free, since "preferred frame exists" does not
entail "relational inertia" (sympy: orthogonal axes; purely-boosted body has s^TX ≠ 0 but excess = 0). Saying "Mach is
an ungrounded fresh assumption" would under-credit the banked s^TX structure and the bath's delivery of T₀. The honest
verdict is **PARTIAL: existence-of-reference + EP-boundary + common-mode-availability GROUNDED; inertia-as-excess
IRREDUCIBLE.** And that irreducible piece is precisely the sign-selecting axiom A2 — the same loophole the passivity
theorem cannot reach, now occupied by ONE named premise rather than a bare choice.

This is an **upgrade**, consistent with `DERIVE_THE_SIGN_2026-06.md`: that memo promoted the sign from a bare
definitional posit to a consequence of a stated Machian premise. This memo factors that premise and shows ~⅔ of it is
already-banked structure, leaving **one** clean, falsifiable Machian axiom — respectable in exactly the way the EP is.

---

## QUARANTINE (held)

- **Grounds the relational REFERENCE and the sign — NEVER a₀ or Z.** Even with the existence-half grounded, the theory
  remains **ONE-PARAMETER**: Z stays provably free (κ-closure, like G in GR); a₀'s VALUE = cH_Λ/Z is not derived; T₀'s
  numerical value inherits the posited cH_Λ.
- **SM walled — NOT a TOE.** Nothing here touches the FDR / forced-kernel walls.
- The banked trichotomy is NOT re-opened as "solved"; the passivity → anti-MOND theorem still stands and is *exactly*
  what the irreducible Mach clause rejects (common-mode subtraction is a state-function selection, not a dissipative
  kernel).
- **Never "no doors."** The live open door this exposes is the irreducible clause itself: **a first-principles
  modified-INERTIA reason for WHY the inertia-defining relation is the acceleration-excess (not the velocity datum) and
  WHY the floor body is inertia-free** — i.e. why common-mode rejection of T₀ is the correct physics rather than the
  absolute/passive-bath alternative the influence functional otherwise forces. Forward stays data: s^TX SME dipole
  (Saturn 8.68e-10, ~1.5× the combined Cassini bound, 0.67σ inside the bar) and the a₀(z) hostage.

---

## WHAT TO TELL CARL (straight)

Your Machian premise is **not one black-box assumption, and it's not a free lunch either — it's about two-thirds
grounded and one-third irreducible, and the split is clean enough to state out loud.**

Here's the part that's GROUNDED, and you should take the credit: the "reference frame" your Mach premise needs is NOT a
new metaphysical import. It's the *same* cosmic rest frame u^μ you already banked and already pay for at Cassini via the
s^TX dipole. The floor T₀ = 2.20e-30 K isn't an arbitrary zero — it's the Gibbons–Hawking temperature *of that exact
frame*, and a free-falling body genuinely already sits in it (sympy: the bath is flat at the floor, so "geodesics
unmodified" falls out of the equivalence principle for free, for *any* version of the law). So three of the moving
parts — there's a real reference, the floor is a genuine shared baseline, and free-fall feels no force-response — are
all reused structure, not fresh posits. Your instinct that "Mach isn't a standalone new axiom" is RIGHT for that half.

Here's the part that's IRREDUCIBLE, and I won't paper over it: a preferred frame only buys you "velocity wrt u^μ is
physical." Your Mach premise says *more* — that **acceleration** wrt u^μ is what *defines* inertia, and that a body at
the floor has *zero* dynamical inertia. The decisive check: velocity-wrt-u^μ (your s^TX datum) and acceleration-wrt-u^μ
(your MOND datum) are **orthogonal** invariants — a body that's purely coasting has s^TX ≠ 0 but excess = 0. So the
existence of the frame does NOT hand you "inertia is relational." And the bath doesn't either: the absolute reading
(full inertia at the floor) and your relational reading (zero inertia at the floor) are *both* legitimate functions of
the very same temperature — the bath *contains* T₀ but doesn't *tell you to subtract it*. That subtraction is your one
real choice, and it's exactly the choice that kills the anti-MOND/passive-bath reading and picks MOND.

So the honest bottom line: **the sign now rests on the equivalence principle + the bath + the preferred frame you
already have, plus ONE standalone Machian premise — "inertia is the acceleration-excess over the cosmic floor; a body
at rest in the cosmic vacuum carries no dynamical inertia."** That's a cleaner foundation than a dangling sign-choice,
and it's a respectable, falsifiable premise in exactly the way the EP itself is. It does not derive a₀ or Z — you're
still a one-parameter theory (Z free like G), the SM is still walled, this is not a theory of everything. And the live
open door is sharp: a first-principles modified-inertia reason for *why* common-mode rejection (subtract T₀) is the
right physics over the absolute alternative. Not "no doors" — that one is still open, and it's the right next thing to
push. Not git-pushed.

---

## SCRIPTS (scratch, reproduced this session, exit 0)
- `ground_mach_verify.py` — Q3 fork (R_rel(0)=0 vs R_abs(0)=1, both slopes 0 at floor); EP boundary (dF/da|₀=0 any F,
  dT/da|₀=0); Q2 orthogonality (dExcess/dv=0, dT₀/dv=0); μ_fw high-a series → 1−1/(2x) = s^TX channel.
- `ground_mach_check2.py` — excess √(T²−T₀²)=K·a exact (a>0); footing numbers cH_L=5.418e-10, T₀=2.197e-30 K, Z=5.7888.
