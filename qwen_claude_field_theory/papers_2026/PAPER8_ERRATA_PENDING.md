# PAPER8 — pending errata for a version 2

> **⚠️⚠️ 2026-09-09, SUPERSEDES EVERYTHING BELOW: THE CENTRAL CLAIM IS FALSE.** `L60_anisotropic_health.py`
> (64/64 PASS, three independent routes) finds the deposited scalar sector carries a **gradient instability
> at every acceleration below ~0.4 a₀** — e-folding in 760 years at 0.7 pc, 0.74 Myr at 1 kpc, unbounded
> beyond ~19 kpc in a normal galaxy, both footings, **no parameter escape** (BBN pins the threshold; ξ
> would need 1.9 kpc; the AQUAL fork fails in the complementary regime). To within the 12.5% K_B can
> buy, **the sector is healthy only where g_φ ≤ g_N, i.e. only where MOND is not operating.** The gate
> table's "DOF health: PASS" was evaluated at solar-neighbourhood acceleration and never in deep MOND.
> **"A complete theory of gravity below the galaxy scale" is therefore FALSE, and the version two is not
> an erratum but a retraction-level correction of the headline.** The theorems the paper cites (the
> foliation theorem, the excess-spent-once theorem) are class-level and unaffected; the static
> rotation-curve phenomenology is unaffected because it does not depend on dynamical stability; the
> action as a healthy field theory is dead as deposited.



**Status: NOT PUBLISHED. This is a tracking list, not a deposit.** The live record is
[DOI 10.5281/zenodo.22667688](https://doi.org/10.5281/zenodo.22667688) (concept 22667687), deposited
2026-09-08. Issuing a version 2 mints a new version DOI under the same concept and requires the owner's
explicit go, as every prior deposit has.

**None of these four flips a verdict in the gate table.** Three are corrections to *reasoning* behind
rows that remain correct, and one is a wrong physical address. All were found by lanes in
`fable_independent_2026/` within a day of deposit, and each names the script that found it.

---

## E1 — the two quoted mode speeds are not eigenvalues (`L46_mode_floor.py`, 59/59 PASS)

The paper quotes two speeds for the coupled clock-scalar sector as though they were the system's
eigenvalues. **They are not: their SUM is the fast one**, verified over three decades. The slow
eigenvalue is

> **c₋ = 1.46e-3 c (canonical) / 1.30e-3 c (alt)** — not the 1.68 c the paper implies.

**Two consequences, both verified.**
1. **The gravitational-Cherenkov row's premise is false.** It reasons that the bound constrains slow
   modes and that the theory has none. It has one. The row's **verdict still holds** at the theory's own
   parameter values, but for a reason the paper does not give.
2. **The sector carries a health condition the paper does not list**, with a stated critical value. It
   **passes** at the theory's own values, so again no verdict moves. It would fail below a stated
   acceleration — but that regime has a non-vanishing background gradient where the flat-background
   linearisation used here does not apply. **The anisotropic calculation is named and NOT done**, and
   the v2 must say so rather than implying the condition is safe everywhere.

## E2 — the saturated branch is in the wrong place (`L53_saturated_cores.py`, 13/13 controls PASS)

The paper (following L30 §7) locates the saturated branch in "the inner few kpc of every galaxy and the
cores of clusters". **Both halves are wrong.**

- **Only 37 of 175 SPARC galaxies reach it at all**, to a median 3.91 kpc; **138 never saturate
  anywhere**; NGC 3198 never reaches it; **dwarfs never do** (DDO 154 is a factor 40 short).
- **It is realised at NO radius the cluster audit tabulates** — 0 of 12 clusters, both footings. Adding
  a central galaxy puts it inside ~5 kpc, **inside the audit's innermost radius**.
- **The 9σ lensing-shape failure does not sit on it either**, being 15× below saturation.

**And the pathology itself was misdiagnosed, in the theory's favour.** Infinite longitudinal stiffness
is a **constraint** on the gradient, not a loss of ellipticity: the problem is a gradient-constrained
variational inequality, **strictly convex, unique and Lipschitz stable**. What fails is C² regularity at
the free boundary and the cubic action — nothing more. **The v2 should say the branch is well posed.**

**One gain to add rather than remove:** in variational form the bounded-boost ceiling is a **pointwise,
geometry-free** constraint, so **triaxiality cannot rescue the cluster failure** — an axis ratio of 0.6
gives the same fraction of the ceiling as a sphere, and misalignment only worsens it.

## E3 — a preferred-frame parameter is quoted footing-dependent (`L49_minimum_addition.py`)

The paper gives α₁ as −4.48e-6 / −4.25e-6, i.e. one value per footing. **α₁ = −4c₁₄ is an exact
identity in the couplings and carries no a₀**, so it is **footing-independent**. Both the identity and
the published formula give **−4.00e-6** at the exhibited point. The gate passes either way.

## E4 — a cone figure is a speed squared (`L54_repair_constraints.py`, 73/73 PASS)

The longitudinal cone figure in §4.3 is a **speed squared**, not a speed. Cosmetic; no verdict moves.

## E5 — the no-slip error bar has the wrong functional form (`L58_anisotropic_stress.py`, 30 checks)

**The result stands; the error bar does not.** Prompted by an exact planar identity from the lead agent,
an independent rebuild confirms `Φ = Ψ to better than 1e-4 out to 1 Mpc` on both footings and both
kernels, with a **3.6× margin** at the genuine worst case. Median disc slip 7.4e-9, worst of 175 discs
5.2e-7, worst cluster 2.4e-6.

Two statements need fixing. **The quoted bound `a₀L/(6c²)` has the wrong functional form** — the slip
tracks the **potential depth** and is **mass-dependent**, not `a₀L` — and it is **exceeded 4.26×** by the
most massive clusters at 1 Mpc. And **"exactly" should not be attached to no slip** in a paper whose
metric sector is Einstein's: the correct statement is *no slip at Newtonian order, with a second-order
residual of at most Φ_N/4, exactly as in general relativity* — a scope statement of the same standing as
γ_PPN = 1.

**One result to ADD rather than correct, and it runs in the theory's favour:** kept exactly, the MOND
sector's anisotropic stress **partially cancels general relativity's own second-order term**, so the
scalar makes the slip **smaller** than GR's by a factor g_N/g. No gate changes; the lensing-versus-
dynamics agreement moves by 1.6e-5 σ.

---

## Two things a v2 should ADD rather than correct

- **The locality hypothesis is discharged** (`L39_nonlocal_modes.py`, 40/40). The paper records it as
  open. It is not: it can be dropped against the entire known nonlocal class, with a **mechanism** — with
  no preferred timelike vector there is exactly one transverse symmetric operator, so the rotation-curve
  and lensing equations are locked together, and the inverse d'Alembertian is included, so nonlocality
  buys nothing.
- **The stiffness repair** (`L52`, 68/68; `L54`, 73/73) is counted, classified and gated: mode count
  stays at four, the auxiliary contributes three second-class pairs and no first-class constraint, and
  the new parameter carries a **two-sided** window whose upper edge is provisional. It discharges three
  of the paper's own recorded liabilities. **Carry it as a proposal with its named open item — the
  screened fourth-order solve — not as a closure.**
