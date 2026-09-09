# L49 — the minimum addition: what must be added, and what does adding it cost

`L49_minimum_addition.py` + `.out` — **41 checks, 26 PASS, 15 FAIL; every one of the eight controls passes
and most of the FAILs are the finding.** Runs in 2 s. Both a₀ footings (9.3619e-11 canonical,
1.1279e-10 alt) on every dimensional number.

`THE_COMPLETE_THEORY_2026-09-08.md` reports a non-empty parameter region and eleven gates passed, and then
fails above a galaxy for one reason: curing the clock tachyon required setting the condensate amplitude to
zero, and that condensate was the action's only dark component. Ten mechanisms have been closed one by one
and L41 assembled them into a specification whose own conclusion is that what satisfies the cluster
constraints is **cold, baryon-tracing matter**, which the theory does not contain.

This lane asks the constructive question instead: **what is the minimum addition, and what does it cost?**

---

## 0. The answer in one line

> **The minimum addition is cold collisionless matter in the matter sector, decoupled from the clock. It
> satisfies the whole cluster specification, leaves the clock tachyon satisfied identically, and repairs the
> CMB and linear growth exactly. It is not free: the action's MOND scalar is sourced by the *total* matter
> potential, so the kernel amplifies the mass added to replace it, and at the abundance the CMB fixes the
> combination overshoots the measured rotation curves by 1.82× in acceleration.**

And the surprise runs against the expected story: **clusters are not the obstacle.** Galaxies and clusters
*can* be reconciled by a partial cold component at f ≈ 0.3 of the ΛCDM halo (N2a **PASS**). It is the CMB
that forbids that solution.

---

## 1. The controls, first — four of L41's anchors, the tachyon rate, and the exhibited point

The risk in a constructive lane is quoting rather than verifying. Eight controls, all PASS.

| control | reproduced here | published |
|---|---|---|
| **X1** cluster amount (R1) | M_dark/M_bar = **5.73 ± 0.68**, f_bar = **0.149**, both footings | 5.73 ± 0.68, 0.149 (L7/L41 K0) |
| **X2** pair amount (R6) | 2MRS rebuilt: N = **1900**, A = **5.645 ± 0.136**, M_dark/M_bar = **30.9 ± 1.5** | 1900, 5.645, 30.9 ± 1.6 (L21/L41 K2) |
| **X3** 3-D source slope (R3) | ρ_X ~ r^**(−1.436)** over 40–750 kpc, 12 clusters | −1.53 (g04a), −1.42 (L41 D2) |
| **X4** shear shape (R4) | NFW gives **−0.851**; the framework's phantom **−0.309**, short by **+0.542 = 9σ** | L24 C11 / L41 P0-P1 |
| **X5** clock-tachyon rate | **282 H₀** today, **2.82e5 H₀** at a = 0.01; gate c₁₄ ≥ **2.533** vs PPN ≤ 2.5e-5 = **1.0e5×** | g03w / THE_COMPLETE_THEORY 3.2 |
| **X6** post-kernel residual | **3.09** (canonical) / **2.76** (alt) M_bar — what the addition must actually supply | THE_COMPLETE_THEORY / L7 |
| **X7** exhibited point | α₂ = **−2.023e-7** (margin **1.98×**), S_eff = **0 exactly**, ceiling **0.4355** | §5 |
| **X8** SPARC machinery | kernel **0.145 / 0.142 dex**, abundance-matched halo **0.171 dex**, medians +0.030 / +0.003 / −0.026 | L16/L28, to the third decimal |

**Two honesty notes attached to the controls, both stated in the `.out`.**

1. **X4 is weaker than it looks.** The "measured" ΔΣ slope is itself an NFW-from-M200 construction
   (Herbonnet's published masses through Dutton–Macciò), so a cold NFW component agreeing with it is close
   to tautological. What is *not* tautological, and is the load-bearing half of R4, is that the framework's
   own near-uniform phantom misses it by 9σ.
2. **X7 flags one documentation item, not resolved here.** The document quotes α₁ = −4.48e-6 (canonical) /
   −4.25e-6 (alt), but α₁ = −4c₁₄ is *footing-independent*, and both the identity and the full
   Foster–Jacobson expression give **−4.00e-6** at the exhibited c₁₄ = 1e-6. The quoted pair is 12% / 6%
   away and looks read off a grid point rather than the exhibited point. The bound is cleared either way by
   22–25×.

---

## 2. The target, stated from the data — R1–R11, plus two entries L41 did not carry

L41's ten requirements are carried unchanged (see `L41_CLUSTER_SPEC.md`). This lane adds the two
**cosmological** entries, which matter because they are what a "theory of the universe" needs and what L41's
cluster-only specification could not see:

| # | requirement | value | source |
|---|---|---|---|
| **R12** | **CMB cold-matter density** | Ω_c h² = **0.1200 ± 0.0012**, i.e. Ω_X/Ω_b = **5.36**; a pressureless component with this density and no photon coupling is what sets the third acoustic peak | Planck 2018 |
| **R13** | **linear growth** | δ must grow from ~1e-5 at recombination to O(1); the action's own linear source is capped at S_eff ≤ 1 − 1/σ = **0.4355** and is **exactly 0** on the closure locus, returning σ₈ ≤ 0.65 with a 20–2000× P(k) deficit at any \|K₂\| | g04h, L29, §5(b) |

**S1 PASS.** The amount clusters require and the density the CMB fixes are the *same number*:
**5.73 ± 0.68** against **5.36**, 0.5σ. That agreement is what makes a single minimum addition possible at
all. *Caveat carried from L18:* it holds at hydrostatic bias b = 0 and degrades to 9.04 by b = 0.33, which
needs ~36% cluster baryon depletion. This is not a measurement of dark matter and is not offered as one.

**S2 FAIL.** The action's own linear MOND source cannot supply R13: S_eff = 0 exactly on the closure locus —
not merely small, zero.

---

## 3. The candidate table, with costs

| candidate | cluster specification | clock tachyon | cost |
|---|---|---|---|
| **A** cold collisionless in S_m | **SATISFIES** R1–R10, R12, R13 | **SAFE, identically** | breaks the galaxy gate at f = 1 (median **−0.259 dex**, **1.82×** overshoot); voids the bounded-boost falsifier; blunts a₀(z); costs the stellar-to-halo-mass relation as a free function of host mass; R2's hydrostatic bias unresolved |
| **B** clock-decoupled condensate | **= A** once m ≥ 1.9e-22 eV | SAFE **only if λ ≤ 3.9e-7, exactly** | every cost of A, plus one new parameter (m) and one exactness assumption that must be enforced by a symmetry rather than by smallness |
| **C** sourced by the MOND scalar | homogeneous piece is **w = −1 exactly** | n/a | the gradient piece **is** the framework's existing phantom: 9σ in shear shape, 1.49–1.99× short at R500, 5.2× over its own ceiling. Not a new candidate |
| **D1** macroscopic / PBH-like | **SATISFIES** the spec; no phase-space floor | SAFE, identically | indistinguishable from A on every requirement and fails the galaxy gate identically; a *realisation* of the minimum addition, not an alternative |
| **D2** undetected baryons | **CLOSED** at cluster scale (f_bar → **1.00**) | n/a | open only at pair scale (L41 B5), so it would need a **second** addition for clusters — not minimal |

### 3.1 Candidate A satisfies the specification — M1–M7

| check | result |
|---|---|
| **M1 [R1]** amount | **PASS.** Cosmic share 5.43 against 5.73 ± 0.68 — **0.4σ** |
| **M2 [R3]** 3-D slope | **PASS.** NFW at M200 = 1e15 (c = 4.11, r_s = 492 kpc) gives **−1.559** against the measured **−1.436**; r_s is inside the ≲750 kpc both descriptions of the residual agree on |
| **M3 [R4]** shear shape | **PASS** (with X4's honesty note) |
| **M4 [R6]** pair anchor | **PASS.** Moster+2013 at the pair's own K-band mass (7.75e10 M⊙ each), Dutton–Macciò concentrations, **nothing fitted**: M200 = 5.63e12 M⊙, predicted M_dark/M_bar inside 132 kpc = **31.0** against the measured **30.9 ± 1.5** — **0.1σ** |
| **M5 [R11]** one host-blind rule | **FAIL — and this is a real cost.** The abundance that works is M200(M_star), a *free function of host mass* fixed by the galaxy stellar mass function. It carries the 5.4× cluster-to-pair ratio that L41's 35-member host-blind search could not. A completion adopting it **inherits ΛCDM's galaxy-formation sector wholesale** |
| **M6 [R8]** phase space | **PASS.** The Tremaine–Gunn floor binds a light thermal relic; a cold component's phase-space density is many orders above it, so R3 is not forced onto a core |
| **M7** verdict on the spec | **PASS** |

### 3.2 Candidate B — the specific question this lane was set, answered by derivation

The tachyon came from the **clock's coupling** to the condensate. Does a component decoupled from the clock
evade it? Derived symbolically rather than asserted. Perturb the clock, τ = t + T, on a flat FRW background,
with Q = n^μ∂_μφ and n_μ = −∂_μτ/√X:

```
Q = Qbar + eps*up + eps^2 * [ Qbar*vT^2/(2 a^2) - vT*vp/a^2 ]        (uT = dT/dt, vT = dT/dx, up/vp likewise for dphi)

K(Q) = K_2 Q^2   contributes, at quadratic order:
    coefficient of (dT/dx)^2       =  K_2 Qbar^2 / a^2      <-- THE CLOCK MASS TERM
    coefficient of (dT/dx)(dphi/dx) = -2 K_2 Qbar / a^2
    coefficient of (dphi/dt)^2      =  K_2
```

**P1 PASS.** The clock's induced gradient-mass coefficient is **exactly K₂Q̄²/a²** — proportional to the
*square of the condensate background*, tachyonic when K₂ = −\|K₂\|, and vanishing **identically** at Q̄ = 0.
Both the clock's kinetic operator and this mass term carry the same k², which is why the rate is
k-independent, reproducing g03w's rate² = \|K₂\|Q̄²(…)/c₁₄ (X5). **This derives, rather than asserts, why
setting Q₀ = 0 cures the tachyon.**

Now give the new component a mixed kinetic function: a fraction λ built from Q_χ = n^μ∂_μχ, and (1 − λ)
built from the fully covariant X_χ = −g^{αβ}∂_αχ∂_βχ. The clock mass coefficient becomes **λK₂Q̄²/a²**, and
X_χ is identically independent of T.

- **P2 PASS.** **Yes — a component decoupled from the clock evades the tachyon by construction.** The
  specific mechanism that killed the original condensate does not act on it, and the evasion is structural
  rather than a tuning.
- **P3 FAIL.** *Approximate* decoupling is not enough. Stability needs λΩ_χ ≤ Ω_m c₁₄/3, i.e.
  **λ ≤ 3.9e-7** at the exhibited c₁₄ = 1e-6 and **λ ≤ 9.9e-6** even at the loosest PPN-allowed c₁₄. The
  decoupling must be **exact to parts in 10⁶–10⁷**, i.e. enforced by a symmetry. Any operator mixing the new
  field with the clock at O(1) reopens the tachyon.
- **P4 FAIL.** The decoupled condensate is **not observationally distinct** from candidate A. The
  specification's own requirements force m ≥ **1.9e-22 eV** (dwarf) and m ≥ 1.1e-26 eV (cluster core), and
  above that the component is pressureless, collisionless, has no phase-space floor and carries an NFW-like
  profile. It is a *realisation* of A costing one extra parameter and one exactness assumption.

### 3.3 Candidates C and D

- **Q1 FAIL.** The MOND sector's homogeneous piece: Y = 0 on a homogeneous slice, so ρ = J(0), p = −J(0),
  **w = −1 exactly**. It is the zero-mode theorem of L32/H-C read as a cosmology. It cannot cluster.
- **Q2 FAIL.** The gradient piece *is* the framework's existing phantom, already measured as failing:
  −0.309 against −0.851, difference +0.542 ± 0.060 = **9σ**. A species whose *mass* depends on φ still has
  to carry the mass itself — the coupling redistributes the source, it does not create it — so it is
  candidate A plus a coupling, strictly more than the minimum.
- **T1 FAIL (on "genuinely different").** Macroscopic dark objects satisfy the specification and are **not
  covered by the recorded no-go**, every branch of which (Pauli, wave, four condensates, thermal relic)
  bounds a *light* species' phase-space density or free-streaming. But they are indistinguishable from A on
  every requirement R1–R11 and fail the galaxy gate identically — a realisation, not an alternative.
- **T2 FAIL.** Undetected baryons: making the cluster residual baryonic drives f_bar from **0.149 to 1.00**
  against the cosmic 0.156, a factor 6.4. L41's B5 door stays open at *pair* scale only, so taking it would
  need a **second** addition for clusters — not a minimum addition.

---

## 4. The cost against the eleven gates

The nine gates a matter-sector addition leaves alone, computed rather than asserted:

| gate | verdict | number |
|---|---|---|
| **N4** clock tachyon (the gate that killed the original condensate) | **PASS, identically** | the induced mass is λK₂Q̄²/a²; a matter-sector component has λ = 0 |
| **N5** mode count and health | **PASS** | gravitational sector unchanged: 2 tensor + 1 clock + 1 scalar, all healthy; +1 matter DOF (0 for a fluid or a macroscopic relic) |
| **N6** Solar-System bounds | **PASS** | a locally-measured cold halo puts **4.37e-15 M⊙** inside Saturn's orbit against Pitjev–Pitjeva's 6.7e-11 — a margin of **15 300×** |
| **N7** preferred-frame α₁, α₂, α₃, γ | **PASS** | functions of (c₁₄, c₂, σ) alone; α₁ = −4.00e-6, α₂ = −2.02e-7 |
| **N8** BBN | **PASS** | ΔN_eff = 0; and it *supplies* Ω_m = 0.315, an input the theory previously had no way to give |
| **N9** CMB and linear growth | **PASS — the payoff** | on the closure locus S_eff = **0 exactly**, so the linear growth equation with a cold component is **algebraically identical to ΛCDM's**. The third peak, σ₈, S₈ and P(k) follow. Nothing here is a prediction: it is ΛCDM's cosmology imported wholesale, and it should be stated as that |

The two it breaks:

**N1 FAIL — the galaxy-scale non-overshoot gate.** The action's MOND scalar is sourced by the *total* matter
potential (statically ∇·J = ∇²Ψ), so adding cold mass does not fill the deficit — **the kernel amplifies the
added mass too.** Solved self-consistently, g_pred = g_N + a₀Δ(g_N/a₀) with g_N = g_bar + f·(the
abundance-matched NFW halo):

| f | kernel+halo rms / median (canonical) | kernel+halo rms / median (alt) | halo only, no kernel |
|---|---|---|---|
| 0.00 | **0.145** / +0.030 | **0.142** / +0.003 | 0.517 / +0.435 |
| 0.05 | 0.142 / +0.002 | 0.146 / −0.022 | 0.455 / +0.383 |
| 0.20 | 0.169 / −0.055 | 0.184 / −0.083 | 0.331 / +0.264 |
| 0.50 | 0.241 / −0.150 | 0.262 / −0.174 | 0.202 / +0.127 |
| **1.00** | **0.338 / −0.259** | **0.360 / −0.283** | **0.171** / −0.026 |

At f = 1 the median RAR residual is **−0.259 dex** — an overshoot of **1.82× in acceleration** — and the rms
goes 0.145 → 0.338. In L21 S6's units: an abundance-matched halo puts **6.12 M_b** inside 10 kpc of a
2e9 M⊙ dwarf against a tolerance of **0.589** (10.4× over) and **0.73 M_b** at L* against **0.408** (1.8×
over). Abundance matching is *worse* than the cosmic share at both ends because it gives low-mass hosts far
more halo than the cosmic share.

**N3 FAIL — the bounded-boost falsifier is voided.** The action predicts g_obs − g_N ≤ C a₀ = 6.06e-11 /
7.30e-11 m s⁻² with no free parameter, and the document calls it the falsifier ΛCDM structurally cannot
make. It is a statement about **g_N**, testable only while g_N = g_bar. With an abundance-matched cold
component present, **36% (canonical) / 30% (alt) of SPARC points have the halo term alone above C a₀**, so
the observed g_obs − g_bar carries no information about the ceiling. The programme's sharpest falsifier
becomes a statement about an unobservable.

### The three-way pincer — and the surprise

| constraint | admissible cold fraction f (canonical / alt) |
|---|---|
| **galaxies** (median RAR shift inside the RAR's own 0.11 dex — the *generous* criterion) | **f ≤ 0.355 / 0.276** |
| galaxies (strict: scatter not degraded by 0.02 dex) | f ≤ 0.185 / 0.120 |
| **clusters**, solved self-consistently through the kernel at 1000 kpc | **f = 0.316 ± 0.100 / 0.261 ± 0.093** at b = 0 |
| clusters at the allowed hydrostatic bias b = 0.20 | f = 0.527 ± 0.134 / 0.455 ± 0.127 |
| **the CMB** | **f = 1.000 ± 0.010** |

- **N2a PASS — a positive result, reported as hard as the negatives.** There *is* a cold fraction admissible
  to galaxies and clusters at once: at **f ≈ 0.3** the kernel plus about a third of the ΛCDM halo satisfies
  the cluster amount self-consistently *and* stays inside the RAR's own scatter. It holds only at b = 0 (it
  closes at b = 0.20) and only on the generous galaxy criterion.
- **N2 FAIL — and the killer is the CMB, not the clusters.** Scaling every halo by f scales Ω_c h² by f, so
  the galaxy ceiling corresponds to Ω_c h² = **0.0426 / 0.0331** against Planck's 0.1200 ± 0.0012 — short by
  a factor **2.8 / 3.6**. (Against Planck's 1% error alone that is 64σ / 72σ, but that figure is
  statistics-only: f_gal carries the ~0.3 dex abundance-matching systematic, so the **factor** is the
  load-bearing statement.) The partial-cold solution N2a exhibits is a cosmology with a third of the
  observed cold-matter density.

---

## 5. The sharp question: with a cold component present, is the MOND sector still doing work?

| check | result |
|---|---|
| **W1** the tightness claim is a discriminant | **FAIL**, reproducing L28: kernel 0.145 dex at zero parameters; abundance-matched halo 0.171 at zero parameters; **a per-galaxy NFW with M200 and c free reaches 0.061 dex.** It must never be written as a discriminant against ΛCDM |
| **W2** the parsimony claim survives | **PASS**, and it is the one thing that does: 0.145 / 0.142 dex at **zero** parameters per galaxy against the halo's 0.171 at zero. But it is a claim that the RAR is *tight*, not that the kernel causes it |
| **W4** a₀(z) survives as a discriminant | **FAIL as a clean one.** The prediction concerns a regime where the kernel sets the dynamics; with a cold component the same z ≈ 2 rotator is halo-dominated and the BTFR zero point is the halo's, with the kernel adding at most C a₀. **The measurement remains worth making** — it discriminates the *no-addition* theory from ΛCDM — but it stops being a test of the theory once the addition is made |
| **W5** the MOND sector does identifiable work | **FAIL** |

**W5, stated plainly, which is what the lane was asked for.** With the addition made at the abundance the
CMB fixes, this is the complete list of what the MOND sector still supplies:

1. **the a₀–Λ tie**, a₀ = κc√(Gρ_Λ), with **κ = 0.4998 / 0.6023 FITTED** — a numerological relation, not a
   derivation, by L32's zero-mode theorem;
2. **a parsimony claim**, 0.145 / 0.142 dex at zero parameters per galaxy — which W1 shows is *not* a
   discriminant, because a per-galaxy halo reaches 0.061 dex;
3. **a bounded-boost ceiling** which N3 shows is no longer testable;
4. the fact that **without** the addition it is a complete, Solar-System-safe, galaxy-correct relativistic
   theory of gravity.

Items 1–3 are a tie, a parsimony claim and a ceiling. **None of them is dynamical work.** The one place the
MOND sector does still do work is the partial-cold cosmology N2a exhibits at f ≈ 0.3 — and that cosmology is
excluded by the CMB.

---

## 6. The recommendation

**PURSUE: candidate A — a cold collisionless component in the matter sector, minimally coupled to g and
decoupled from the clock.** It is the only candidate that satisfies the specification; B and D1 are
realisations of it; C is the failure the theory already has; D2 needs a second addition. The decoupling is
not a detail — P1/P2/P3 show it is the *whole reason* the addition is safe, and that it must be exact to
λ ≤ 3.9e-7, i.e. enforced by a symmetry.

**THE GATE MOST LIKELY TO KILL IT: the galaxy-scale non-overshoot gate (N1), through the CMB (N2).**
Galaxies tolerate f ≤ 0.355 of the ΛCDM halo on top of a kernel the action cannot switch off; the CMB fixes
f = 1.00 ± 0.01, a factor 2.8 away. Note the direction of the surprise: clusters need only f = 0.32 ± 0.10,
so galaxies and clusters *can* be reconciled by a partial cold component. It is the CMB that forbids it.

**THE CALCULATION THAT WOULD DECIDE — one calculation, not a programme.** *Does the action admit a source
for the MOND scalar that is not the total matter potential?* The coupling 2(2 − K_B)J^μ∂_μφ gives
∇·J = ∇²Ψ statically, and Ψ is sourced by everything minimally coupled to g — which is exactly why the
kernel amplifies the added cold mass. Two concrete replacements, both computable with machinery already in
this directory and neither run:

- **(a) source the MOND scalar by the baryon current alone.** The galaxy overshoot then falls from the
  self-consistent factor to g_bar + g_halo + a₀Δ(g_bar/a₀); the price is that matter is no longer
  universally coupled, so it must be run against the equivalence principle, against α₁/α₂ with two matter
  sectors, and against L27's foliation-scalar theorem.
- **(b) let J's argument carry the total density**, so the kernel switches off where the cold component
  dominates. L6's cosmological-ordering theorem already constrains this, and it must be shown *not* to be a
  monotone screening function in disguise.

If (a) survives, the addition is affordable and the MOND sector keeps its galaxy-scale work. If neither
does, the honest conclusion is §7.

---

## 7. Three-sentence verdict

**A minimum addition exists and it is cold collisionless matter in the matter sector:** it satisfies the
full cluster specification (R1 at 0.4σ, R3 at −1.56 against −1.44, R4 at −0.851 against −0.851, R6 at 31.0
against 30.9), leaves the clock tachyon satisfied identically because the mechanism that killed the original
condensate is the clock's *coupling* to it and not its energy density, and repairs the CMB and linear growth
exactly.

**It is not free:** the action's MOND scalar is sourced by the total matter potential, so the kernel
amplifies the mass added to replace it, and the three admissible cold fractions have an empty intersection —
galaxies allow f ≤ 0.355, clusters need 0.32 ± 0.10, the CMB fixes 1.00 ± 0.01 — so at the abundance the CMB
requires the addition overshoots the measured rotation curves by 1.82× in acceleration, and the binding
constraint is the CMB (short by a factor 2.8) rather than the clusters, which can in fact be reconciled with
galaxies by a partial cold component at f ≈ 0.3.

**With the cold component present the MOND sector does no identifiable work in galaxy dynamics:** its
parsimony claim (0.145 dex at zero parameters per galaxy) is not a discriminant because a per-galaxy halo
reaches 0.061 dex, its bounded-boost falsifier is voided because 36% of SPARC points have the halo term
alone above the ceiling, a₀(z) stops being a test of the theory, and what is left is the a₀–Λ tie with κ
still **fitted**.

---

## 8. Caveats, stated rather than buried

1. **Nothing in this lane favours this framework over ΛCDM, and nothing in it constrains ΛCDM.** L41's E1
   shows ΛCDM's own abundance matching predicts the pair anchor to 0.6σ with nothing fitted, and the
   non-monotone ladder *is* the stellar-to-halo-mass relation — an input, not a prediction.
2. **f_gal is the generous of two criteria**, chosen so the candidate is not handed a manufactured deficit.
   The strict criterion gives 0.185 / 0.120, three times smaller. The full f-table is printed so a reader
   can pick another; no choice in the printed range reaches f = 1.
3. **Abundance matching carries ~0.30 dex of systematic** on log M200 (Moster vs Behroozi vs Kravtsov). It
   shifts f_gal and the R7 overshoot by the same factor and cannot close a gap of 2.8×.
4. **The symbolic tachyon derivation is on a flat FRW background with one Fourier direction.** It fixes the
   *structure* of the coefficient (∝ λK₂Q̄²/a²), which is what the lane's question needs, and it reproduces
   g03w's published rate through X5. It is not a full cosmological-perturbation calculation and does not
   claim to be.
5. **R2's hydrostatic bias is the one requirement candidate A does not clear cleanly:** at the allowed
   b = 0.20–0.33 the cluster requirement runs to 9.04, needing ~36% cluster baryon depletion. That is a cost
   of the cold reading and it is not resolved here.
6. **One documentation item handed back, not edited:** THE_COMPLETE_THEORY's α₁ = −4.48e-6 / −4.25e-6 is
   footing-dependent for a footing-independent quantity, and the exhibited point gives −4.00e-6 by both the
   identity and the full Foster–Jacobson expression (X7).

---

## 9. Reproduction

```
python3 fable_independent_2026/L49_minimum_addition.py
```

Exit 0, 2 s. 41 checks: 26 PASS, 15 FAIL. Eight controls (X1–X8) rebuild four of L41's specification
anchors, the framework's own post-kernel residual, the clock-tachyon rate, the exhibited point's PPN
parameters and L16/L28's three parameter-free SPARC numbers, each from its own data with independent code.
Every control passes.
