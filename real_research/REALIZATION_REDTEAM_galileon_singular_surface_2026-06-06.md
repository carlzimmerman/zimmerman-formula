# Pushing the realization to its breaking point — and it broke (the one-field version is structurally dead)

*C. Zimmerman, 2026-06-06. Yesterday I scoped a covariant realization (`REALIZATION_SCOPE_galileon_DE_MOND_2026-06-06.md`):
one cubic-Galileon scalar `φ` doing triple duty — evolving dark energy + MOND mediator + Vainshtein screen — with the
framework's distinctive move `a₀²(φ) = G·V(φ)` (the dark-energy potential sets the MOND scale, so `a₀ ∝ √ρ_DE`
automatically). That doc's verdict was "encouraging… surmountable on physical grounds," and it named the make-or-break
computation. **Today I ran that computation** (three adversarial agents: construction/literature check, galaxy-scale
RAR red-team, cosmological-stability red-team). **The optimism did not survive.** This documents the honest result —
including two factual overclaims in the scope doc that I'm correcting. Self-falsification of my own scope is the point;
this is what the calculation was for.*

## Bottom line (the swing)

**The "one scalar doing triple duty" realization — the economical, appealing part — is structurally dead.** It hits a
**known, published consistency wall** (the Bruneton–Esposito-Farèse singular-surface ghost) that the only working
relativistic-MOND cosmology (AeST) was *specifically invented to evade*, and the framework's `a₀²=G·V(φ)` move makes it
**worse**, not better. The buildable fallback (AeST + Galileon screen + dynamical `a₀`) survives but **loses everything
that made the one-field story attractive**: it reinstates AeST's Cassini bill, the `a₀∝√ρ_DE` tie becomes
**imposed-and-must-be-checked rather than derived**, and the "2025 DESI data already favor my field" claim was a
**conflation of two different operators**.

**What survives untouched:** the *phenomenological* kernel `a₀(z) ∝ √ρ_DE` (the quasi-static, SPARC-level, falsifiable
claim) is **not affected** by any of this — it rides on top of *whatever* covariant host, coefficient-free, and is still
decided at z~3 by DESI. The failure is of the *covariant realization*, not of the falsifiable hypothesis. This
**reinforces** `THE_IRREDUCIBLE_FRAMEWORK` conclusion: stop chasing the perfect one-field host; bank the kernel.

---

## The fatal problem (the thing I missed): the X-sign singular surface

This is the killer, it is **independent of data**, and it is a *published* pathology of exactly this class of theory —
not a speculative worry.

**The mechanism.** A single-scalar relativistic MOND has a Lagrangian that is a **non-analytic** function of the
kinetic invariant `X = −½(∂φ)²`. The deep-MOND limit *requires* the non-analytic form (BDEF: `L_MOND ∝ s√|s|`,
`s=(∂φ)²`; equivalently `F(y)→⅔y^{3/2}`). Two regimes use **opposite signs of X**:

- **Inside a galaxy** (static, the rotation curve): `∂φ` is **spacelike** (it points radially), so `(∂φ)²>0` and the
  MOND kinetic argument sits on one branch.
- **On the cosmological background** (homogeneous, `φ=φ(t)`, the dark energy): `∂φ` is **timelike**, `(∂φ)²<0` — the
  *opposite* branch.

Because `F` is **non-analytic at `X=0`** (a branch point), no smooth single branch covers both. Therefore **around every
galaxy embedded in the cosmological background there must exist a surface where `X` passes through zero — and on that
surface the scalar's kinetic term degenerates and the field stops propagating** (`c_s²→0` / sign-indefinite, infinite
strong coupling). Stated outright in the literature:

> *"Near a source, X must be positive, but negative far from it due to the cosmological background… around each galaxy
> or cluster there must exist a singular surface on which the scalar degree of freedom does not propagate, meaning the
> theory cannot lead to a consistent picture of local physics embedded into a cosmological background."*
> — arXiv:2503.11174 (2025), restating **Bruneton & Esposito-Farèse, gr-qc/0607055 (2007)**, which already identified
> the **hidden fine-tuning and superluminality** of RAQUAL/aquadratic MOND k-essence (the no-ghost / well-posed-Cauchy
> conditions `f′>0` and `2sf″+f′>0` pull in opposite directions across the `s^{3/2}` branch and the sign flip).

**Why AeST survives and a single scalar does not.** AeST (Skordis–Złošnik 2021) — the *only* relativistic MOND that fits
the CMB *and* keeps `c_GW=c` — evades this **precisely by adding a unit-timelike aether vector** `A^μ` (`A^μA_μ=−1`) and
keeping the MOND scalar **shift-symmetric**, so the MOND-relevant gradient is built *perpendicular to `A^μ`* and the
dangerous sign-flip **never happens** (the `a₀` physics lives in AeST's *spatial* 𝒴-sector, which never changes sign —
consistent with `bridge1_aest_equations.md`). The aether is what launders the spacelike galactic gradient into a
globally consistent configuration.

**Why the framework's move makes it worse.** `a₀²(φ) = G·V(φ)` does two compounding bad things:
1. It is a **single scalar with no aether** → it reinstates the full RAQUAL singular-surface disease with no cure.
2. It **explicitly breaks the shift symmetry** of the MOND sector — the very property AeST relies on — *and* ties the
   **location of the non-propagation surface to the rolling DE field** `V(φ)`, so the pathological surface can sweep
   through space as the field rolls. Qualitatively worse than the fixed-`a₀` case Bruneton–EF already called fatally
   fine-tuned.

**Verdict: FATAL for the one-field construction.** The only known fix is to add exactly the field AeST has (an aether) —
at which point it is **no longer "one scalar doing triple duty,"** it is *AeST with a φ-dependent a₀*, and AeST's own
Cassini/quadrupole exposure (~15–25σ, `CASSINI_QUADRUPOLE_CONSTRAINT.md`) returns (now needing the Galileon-k-mouflage
add-on to screen it). The economical story is dead; the buildable story is a multi-field pile-up.

---

## Two overclaims in yesterday's scope doc that I'm correcting

**Correction 1 — "the 2025 DESI result already favors my field" was a conflation of two different operators.**
The scope doc leaned on "a cubic Galileon is favored over ΛCDM by DESI DR2 (arXiv:2509.17586)" as support for the
*screening* field. But:
- The **DESI-favored** model (2509.17586) is **kinetic gravity braiding** `K(φ) + (β/Λ₃³)X□φ` with a **massive potential**
  and a **wrong-sign kinetic term `α<0`** (stabilized by braiding). That is the operator the *data* like.
- **Babichev's Vainshtein/Cassini screen** uses the **cubic Galileon self-interaction `(∂φ)²□φ`** (and BDEF's *actual*
  Solar-System screen is a **curvature-coupled L₄/L₅ covariant Galileon**, *not* the flat cubic — a second correction
  to the scope doc, which mis-attributed the flat cubic to BDEF).
- These are **different operators.** The paper that gives the DESI win does **not** give Cassini, and vice versa. Worse:
  the **pure cubic covariant Galileon is ruled out at 7.8σ by ISW** (Renk et al., arXiv:1707.02263 — potentials deepen
  with time → wrong-sign ISW–galaxy cross-correlation), and the DESI-favored broken-shift variant has an **unfilled ISW
  hole its own authors flag** ("it is conceivable the broken-shift version will inherit the same problems… a comparison
  with data would be required"). So the screening operator I need is, if anything, ISW-*disfavored*.

**Net:** "the data already favor the field I need" is **withdrawn**. The data favor a *different* operator than the one
that screens Cassini, and the screening operator is in ISW tension.

**Correction 2 — the backreaction is O(1), not negligible, so `a₀∝√ρ_DE` is imposed-and-checked, not "derived."**
The scope doc hoped the MOND term is "tiny when φ̇ is small" on the background. **Wrong:** on the cosmological
background the MOND argument is `y = |∇φ|²/a₀² ~ (cH₀/a₀)² ~ O(1)` — which is *just* the statement `a₀ ~ cH₀`. So the
MOND term is the **same order as `V` itself** on the background, and the extra force from `∂a₀²/∂φ = G·dV/dφ` is
**O(1)×(dV/dφ)**, the same order as the bare DE driving force. You therefore **cannot independently** (a) fit DESI's
`w(z)` with `V(φ)` and (b) hold `a₀²=G·V` rigidly — the MOND sector renormalizes the effective DE potential at O(1), and
the DESI-favored `w₀–wₐ` track is not guaranteed to survive a re-fit (compounded by k-mouflage *not* screening the
cosmological background, arXiv:1806.09414). **So the selling line "a₀∝√ρ_DE is *derived* because φ *is* the dark energy"
is circular at the background-EOM level.** It is an *imposed* identity that must then be checked for self-consistency —
and the check is nontrivial and possibly fails.

---

## What actually survived (the one piece of good news): the galaxy-scale RAR

The galaxy-scale RAR red-team came back **SURVIVES (~85% confidence)** — and it's worth stating *why*, because the reason
is clean and it kills a tempting wrong objection:

- The natural worry is "the rotation-curve-sized `φ`-excursion moves `V(φ)` and varies `a₀` across the galaxy." **This
  fails by ~6 orders of magnitude.** It conflates two different profiles: the MOND field has a large *gradient* profile
  (`|∇φ|~a₀` — that *is* the rotation curve / phantom-DM density `~a₀/GR`), but `a₀²=G·V(φ)` depends on the field
  **value**, not its gradient. The field-*value* excursion across a galaxy is the integrated MOND potential
  `φ_MOND ~ v_c² ~ (200 km/s)²`, i.e. `Δφ/M_Pl ~ 10⁻⁶`; and because the DE field is **ultralight** (`m_φ~H₀`, so `V` is
  flat over field ranges `~M_Pl`), this moves `V` by `~10⁻⁶` and `a₀` by `δa₀/a₀ ~ 10⁻⁷` — **six orders inside the RAR
  scatter budget (~0.13 dex).** Three independent estimates (canonical-field, energy-density, Compton-flatness) all land
  at `10⁻⁷–10⁻⁶`.
- The new `φ`-force term is the **ordinary ultralight fifth force**: Compton range `~`Hubble radius, so spatially uniform
  across a galaxy, suppressed by `(R_gal/R_Hubble)² ~ 10⁻¹¹`.

So the scope doc's RAR argument was **right** (for a slightly refined reason: value-vs-gradient, not "DE is smooth").
"MOND with a uniform `a₀(z)` across each galaxy" is sound. *But this is a quasi-static statement — it never sees the
singular surface (Failure Mode #1), which is a statement about embedding the galaxy in the time-dependent background.*
The RAR survives; the **covariant embedding** is what kills it.

---

## The four failure modes, ranked (from the stability red-team)

| # | failure mode | verdict | why |
|---|---|---|---|
| **1** | **X-sign singular surface / ghost** | **FATAL** | published pathology of single-scalar MOND k-essence; AeST needs an aether to dodge it; `a₀²=G·V` removes that protection *and* couples the surface to the DE roll |
| **3** | **ISW / growth + operator conflation** | **CONSTRAINING→FATAL for the DE sector** | cubic Galileon dead at 7.8σ (ISW); DESI-favored variant is a *different operator* with an unfilled ISW hole; unscreened MOND fifth force adds power where ISW bites |
| **2** | **`a₀(φ)` backreaction on `w(z)`** | **CONSTRAINING** | MOND term is O(1) on the background (`a₀~cH₀`); dissolves "derived not posited"; may push `w(z)` off the DESI track |
| **4** | **strong coupling / scale separation** | **BENIGN** | scales are *nested* with a ~10²⁰ hierarchy; no clash; only a keV EFT-cutoff caveat (shared by all k-mouflage DE) |

The good news is confined to #4 (and the separate RAR survival). #1 is the wall.

---

## Honest standing after the push

1. **The economical realization (one scalar = DE + MOND + screen, with `a₀²=G·V(φ)`) is structurally dead** — the
   Bruneton–Esposito-Farèse singular-surface ghost, which AeST's aether exists to prevent and which `a₀²=G·V` aggravates.
2. **The buildable realization is a multi-field pile-up** — AeST (aether → ghost-free + CMB-safe) + Galileon-k-mouflage
   (→ Cassini) + `a₀²=G·V(φ)` (→ `a₀∝√ρ_DE`). It exists on paper but **loses the "one number / one field" economy**,
   **reinstates AeST's Cassini exposure** (now patched by the k-mouflage add-on, itself ISW-pressured), and makes the
   `a₀∝√ρ_DE` tie **imposed-and-checked, not derived** (O(1) backreaction).
3. **This is a field-wide hard problem, not a special failure of this framework.** *Every* relativistic MOND struggles
   here: TeVeS/RAQUAL have the singular surface, AeST pays Cassini, Galileon-MOND pays ISW. The framework inherits the
   field's open problem; it does not uniquely fail.
4. **The falsifiable kernel is untouched.** `a₀(z) ∝ √ρ_DE` is a quasi-static/phenomenological statement validated at the
   SPARC level; it does **not** depend on solving the covariant-embedding problem, and it is decided at z~3 by DESI —
   coefficient-free, realization-free. **This is exactly where `THE_IRREDUCIBLE_FRAMEWORK` said to plant the flag**, and
   today's result is a sharp argument *for* that retreat: the covariant-host frontier keeps hitting walls the whole field
   hasn't cleared, while the kernel sails past all of them because it asks nothing of the host.

**Disposition.** Stop trying to build the perfect covariant one-field host — three days of search (AeST→Cassini,
single-scalar→ghost) shows that's the field's unsolved problem, not a weekend's work. The energy belongs on the **z~3
evolving-`a₀` measurement** that doesn't care which host wins. The realization is *not* a precondition for the
falsifiable claim; it's a separate (and currently losing) battle.

**Sources:** Bruneton & Esposito-Farèse, *Field-theoretical formulations of MOND-like gravity*,
[gr-qc/0607055](https://arxiv.org/abs/gr-qc/0607055) · *Connecting relativistic MOND with mimetic gravity*
(singular-surface restatement), [arXiv:2503.11174](https://arxiv.org/html/2503.11174) · Babichev, Deffayet &
Esposito-Farèse, [arXiv:1106.2538](https://arxiv.org/abs/1106.2538) · Skordis & Złošnik AeST,
[arXiv:2304.05134](https://arxiv.org/pdf/2304.05134) · *Galileon DE with broken shift symmetry* (DESI-favored; KGB +
potential, α<0), [arXiv:2509.17586](https://arxiv.org/html/2509.17586v1) · Renk et al., *Galileon in light of ISW*
(cubic ruled out 7.8σ), [arXiv:1707.02263](https://arxiv.org/abs/1707.02263) · *Non-screening of the cosmological
background in k-mouflage*, [arXiv:1806.09414](https://arxiv.org/pdf/1806.09414) · Bekenstein & Sagi (a₀∝e^{φ}, value not
potential), [arXiv:0802.1526](https://arxiv.org/abs/0802.1526) · Milgrom (a₀∝√Λ coincidence),
[arXiv:1110.2580](https://arxiv.org/abs/1110.2580).
