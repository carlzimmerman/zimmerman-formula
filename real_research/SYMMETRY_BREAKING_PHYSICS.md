# The Newton→MOND Transition as a Symmetry-Breaking / Critical Phenomenon

**C. Zimmerman, June 2026.** *Developing the result that **a₀ is the scale at which deep-MOND
conformal symmetry breaks** into its observable structure. Every claim is tagged
`[DERIVABLE]` (with the argument) or `[ANALOGY]` (and labelled as such). Verification:
`reviews/project_symmetry_breaking.py` (six checks, all pass) and the empirical RAR fit in
`reviews/desitter_unruh_RAR_test.py`. Built on `ANHARMONIC_AND_32PI.md`,
`FORCING_ROUTES_REWORKED.md`, `GEOMETRIC_ORIGIN_OF_A0.md`.*

> **Headline, stated up front so the document cannot be over-read.** Treating Newton→MOND as
> symmetry-breaking is an **illuminating re-description, not a new theory**. It explains
> *why* three already-known things are true; it produces **no new falsifiable number**. The
> four verdicts are: **(a) smooth crossover**, not a sharp phase transition; **(b) order
> parameter = |∇φ|/a₀**, broken (deep-MOND, cubic, conformal) phase below, symmetric
> (Newtonian, harmonic) phase above; **(c) NO Goldstone** — the breaking is *explicit*, not
> spontaneous; **(d) no genuinely new observable** falls out. Each is argued below.

---

## 0. The setup (from the anharmonic result)

The deep-MOND limit has an exact **SO(4,1) conformal symmetry** in d=3 spatial dimensions
(Milgrom 2009, arXiv:0810.4065 — a theorem, verified this program), and that symmetry
*forces the cubic* AQUAL Lagrangian:

$$\mathcal{L} = -\frac{1}{8\pi G}\,a_0^2\,F\!\left(\frac{|\nabla\phi|^2}{a_0^2}\right),\qquad
F(y)\to\begin{cases} y & y\gg1 \ \ (\text{Newton, harmonic }|\nabla\phi|^2)\\[2pt]
\tfrac{2}{3}\,y^{3/2} & y\ll1 \ \ (\text{deep-MOND, cubic }|\nabla\phi|^3/a_0)\end{cases}$$

`[DERIVABLE]` **The cubic is forced; a₀ must drop out of the deep limit.** In d spatial
dimensions the deep-MOND field equation div(|∇φ|^{p−1}∇φ) ∝ ρ gives a point-mass field
g(r) ∼ r^{−(d−1)/p}; a flat rotation curve (g ∼ 1/r) forces p = d−1, hence **p=2 in d=3**,
i.e. the Lagrangian is |∇φ|^{p+1} = **|∇φ|³**. Demanding the action ∫d³x |∇φ|³ be invariant
under the dilatation x→λx, φ→λ^s φ gives action-weight λ^{3s}, so **s=0**: φ is dimensionless
under scaling, and therefore **the only dimensionful constant, a₀, cannot appear in the
deep-MOND limit at all.** That is the precise sense in which *a₀ is the conformal-breaking
scale*: it lives only in the *crossover*, never in the symmetric (deep) phase.
(CALC 1, `project_symmetry_breaking.py`.)

This single fact — a₀ is absent from the symmetric theory and present only where the harmonic
term re-enters — is what every section below unpacks.

---

## 1. Crossover vs phase transition → **SMOOTH CROSSOVER** `[DERIVABLE]`

**Verdict: a smooth (analytic) crossover, with the only non-analytic point sitting *at* the
symmetric fixed point g_N→0, not at the crossover scale g_N∼a₀. This is the structure of a
*quantum-critical* / zero-temperature crossover, not a finite-T first-order transition.**

### The argument (analyticity)
A phase transition is a **non-analyticity** (a kink, a branch point, a discontinuous
derivative) of an observable at a *finite* value of the control parameter. A crossover is a
**smooth** interpolation with no such singular point. The control parameter here is the
Newtonian acceleration g_N (equivalently |∇φ|), and the observable is g_obs(g_N).

Take the framework's own *derived* interpolation (the de Sitter–Unruh / "simple-ν" form,
`desitter_unruh_mond.py`):
$$g_\text{obs} = \sqrt{g_N^2 + g_N\,a_0}.$$
The radicand g_N(g_N + a₀) vanishes **only at g_N = 0** (and the unphysical g_N = −a₀). So:

- For **all finite g_N > 0** the function is analytic — no kink, no divergence. The local
  log-log slope runs *continuously* from 1 (Newton) through ≈0.75 at g_N=a₀ to 1/2
  (deep-MOND), with no discontinuity (CALC 2 verifies the slope is finite and smooth
  through the crossover).
- The **only** non-analyticity is the √g_N branch point **at g_N = 0** — the deep-MOND IR
  limit, which is exactly the **scale-invariant (conformal) fixed point** where a₀ has
  dropped out.

The same is true of McGaugh's empirical RAR function g_N/(1−e^{−√(g_N/a₀)}): its sole branch
point is again at g_N=0. **Every standard interpolating function is analytic across the
transition; the non-analyticity is pushed to the symmetric fixed point.**

### Why this is the *right* structure, and why it matches the data
This is the signature of a **second-order/continuous crossover governed by an IR fixed
point**, the gravitational analogue of a **quantum critical point**: the singular point is
the symmetric phase itself (the conformal deep-MOND limit), and any finite a₀ "rounds off"
the approach to it into a smooth crossover — precisely as a relevant perturbation rounds a
quantum-critical point at finite coupling. There is **no order-parameter discontinuity**
because a₀ is an **IR scale**, not a free-energy non-analyticity.

The observed RAR is exactly a smooth interpolating μ-function with tight scatter, and the
framework's *derived* μ fits SPARC at **0.105 dex** vs McGaugh's **0.101 dex** (3389 points;
`desitter_unruh_RAR_test.py`). So the symmetry-breaking picture **predicts the qualitative
fact that the transition must be smooth** — and the data agree.

**Honest caveat — is this predictive or just re-descriptive?** Standard MOND *already* uses a
smooth μ-function; the smoothness is not a new datum. What the symmetry-breaking picture
*adds* is an **explanation of why** it must be smooth (an IR fixed point has no order-parameter
discontinuity), and a structural statement (the non-analyticity is at g_N=0, the conformal
point). That is genuine understanding, but it is `[DERIVABLE re-description]`, **not a new
prediction**: nothing here forbids a μ-function the data could already have ruled in or out.

---

## 2. The order parameter and the two phases `[DERIVABLE structure / ANALOGY in naming]`

**Order parameter:** the **dimensionless field gradient**
$$\boxed{\;\eta \equiv \frac{|\nabla\phi|}{a_0} = \sqrt{y}\;}$$
(equivalently the Newtonian acceleration in units of a₀, g_N/a₀, since |∇φ|=g). It is the
unique dimensionless local quantity that the AQUAL function F depends on, and it is what
distinguishes the two regimes.

| | "Symmetric" phase | "Broken" phase |
|---|---|---|
| **regime** | Newtonian (UV / high accel) | deep-MOND (IR / low accel) |
| **order parameter** | η = \|∇φ\|/a₀ ≫ 1 | η = \|∇φ\|/a₀ ≪ 1 |
| **Lagrangian** | harmonic \|∇φ\|² | cubic \|∇φ\|³/a₀ (conformal) |
| **scale invariance** | **broken** (the harmonic term carries a dimension) | **restored** (a₀ drops out) |
| **field equation** | linear (Poisson) | nonlinear (√-law) |

Two points of precision, and one honest correction to loose "phase" language:

- **Which phase is "symmetric" is the counter-intuitive part, and it is correct.** The
  *deep-MOND* (broken-looking, nonlinear, "exotic") phase is the one where the **conformal
  symmetry is restored** (a₀ absent, scale-invariant). The *Newtonian* phase is where the
  symmetry is **broken** (the harmonic term re-introduces the scale a₀). So in the
  Landau-style table the labels are: **Newtonian = symmetry-broken**, **deep-MOND =
  symmetry-restored**. Calling deep-MOND the "broken phase" because it is the unusual one
  would be backwards. `[DERIVABLE]`

- **The order parameter is a *local* control field, not a thermodynamic order parameter.**
  η = |∇φ|/a₀ is set externally (by the baryon distribution and radius), not selected
  dynamically by minimizing a free energy. So "order parameter" is **`[ANALOGY]`** in the
  Landau sense: there is no spontaneous choice, no symmetry-breaking *direction* picked by a
  vacuum. It is the **control parameter** of a crossover (like the field h in a paramagnet
  above T_c that smoothly polarizes the spins), not the spontaneous magnetization. This is
  the same conclusion that forces "no Goldstone" in §3.

**What is genuinely derivable here:** that there *is* a clean dimensionless variable η whose
two limits are the two field theories, that the symmetric limit is the *deep-MOND* one, and
that a₀ is the value of |∇φ| where they cross. **What is analogy:** the word "phase" and
"order parameter" in their thermodynamic, spontaneous sense.

---

## 3. Goldstone / light scalar → **NO Goldstone. The breaking is EXPLICIT.** `[DERIVABLE]`

**Verdict: there is no exact Goldstone boson, no light MOND dilaton, no associated fifth
force or extra gravitational-wave polarization — because the conformal symmetry is broken
*explicitly* (a dimensionful term in the action), not *spontaneously* (a vacuum VEV).
Goldstone's theorem does not apply. This is the honest, deflationary answer to the most
seductive item.**

### The argument
Goldstone's theorem requires a **continuous symmetry of the action** that is broken by the
**ground state** (a non-invariant VEV). Then — and only then — a massless mode appears.
Examine how a₀ enters the AQUAL action under the dilatation x→λx, φ→φ:

$$\int d^3x\;\frac{|\nabla\phi|^3}{a_0}\ \xrightarrow{\ \lambda\ }\ \lambda^{3}\lambda^{-3}=\lambda^0\quad(\textbf{invariant; }a_0\textbf{ an inert prefactor})$$
$$\int d^3x\;|\nabla\phi|^2\ \xrightarrow{\ \lambda\ }\ \lambda^{3}\lambda^{-2}=\lambda^{1}\quad(\textbf{NOT invariant — this term breaks scale invariance})$$

The symmetry is broken by the **Newtonian harmonic term itself** — a term *in the Lagrangian*
with a fixed dimensionful coefficient. It is present in the UV, absent in the IR, and a₀ is
the value of |∇φ| at which it overtakes the cubic. This is the textbook definition of
**explicit breaking**: a non-invariant operator sits in the action. There is **no
order-parameter VEV** that breaks a symmetry of an otherwise-invariant action.

**Therefore Goldstone's theorem simply does not apply, and there is no exact Goldstone
boson.** (CALC 3.)

### Two SO(4,1)s — and why neither rescues a fifth force
The label SO(4,1) appears in two *distinct* places, and conflating them is the trap:

1. **SO(4,1) = the conformal group of Euclidean ℝ³** (dilatations + special conformal +
   Poincaré of 3-space) — the symmetry of the |∇φ|³ field theory on flat space (Milgrom's
   theorem). a₀ breaks **this**, *explicitly* → no Goldstone, as just shown.
2. **SO(4,1) = the isometry group of de Sitter spacetime dS₄** — the background the framework
   ties a₀ ∼ c√Λ to. A de Sitter background **is maximally symmetric**: SO(4,1) is the
   *unbroken* group (all 10 generators survive). The only would-be dilaton of broken 4D
   conformal symmetry is the **cosmic scale factor** a(t) — already in the FRW metric — **not
   a new galaxy-sourced scalar**.

So **neither** route gives a new light scalar with observable galaxy-scale effects (CALC 4).
The coincidence that the *same group label* appears in (1) and (2) is exactly the *content*
of the framework's posit a₀ = c²√(Λ/32π) — it welds (1)'s breaking scale to (2)'s curvature
— but that is a **`[hypothesis/posit]`**, not a theorem that the two SO(4,1)s are the same
group acting the same way. Milgrom's theorem is only (1).

### Could there be a *pseudo*-Goldstone? (the one place to be careful)
If the conformal symmetry were *spontaneously* broken with a *small explicit* piece, one
would get a **light dilaton** (a pseudo-Nambu-Goldstone boson) whose m² ∝ the explicit
breaking — and *that* would be an observable light scalar. **This does not happen here**,
because the breaking is *purely* explicit (the harmonic term), with no spontaneous component
to provide the Goldstone in the first place. There is no symmetric vacuum that
"spontaneously" picks deep-MOND; the regime is selected locally by the baryons (§2). Hence
**no pNGB, no MOND dilaton.** This is consistent with — and "predicts" — the **null** results
of all fifth-force and dilaton searches and the GR-consistency of GW170817 (no anomalous
scalar GW polarization). It is a *negative* statement, honestly the strongest thing item 3
can say: **the framework should NOT be expected to contain a light MOND scalar, and looking
for one is the wrong experiment.**

> **Caveat on scope.** This is the verdict for the *non-relativistic AQUAL* picture that
> Milgrom's theorem and the anharmonic result actually concern. A *covariant* completion
> (AeST/RMOND, Blanchet's dipolar medium) does contain extra fields by construction — but
> those are introduced *explicitly* to build the theory, are *not* Goldstones of the
> deep-MOND conformal symmetry, and are constrained (mass, coupling) by the CMB and
> GW170817 in those papers, not by this symmetry argument. So "no Goldstone" is a statement
> about the symmetry, not a claim that the covariant theory has no scalars.

---

## 4. Universality and the 0.069-dex scatter → **partly apt, partly over-reach** `[ANALOGY]`

**Verdict: the *rigid deep-MOND slope of 1/2* is legitimately critical-exponent-like (it is
fixed by the conformal weight and is system-independent). But ascribing the *tight scatter*
(≤0.069 dex) to *universality* is an over-reach: the mechanism that makes scatter small in
critical phenomena — a diverging correlation length that washes out microphysics — is
*absent* here (the crossover is smooth, ξ stays finite, §1). The scatter is small for the
mundane reason that the RAR is a deterministic force law.**

### What is genuinely apt
- **Data collapse.** 153–175 galaxies, ~2700–3400 points, collapse onto one curve
  g_obs = g_bar·ν(g_bar/a₀) — a single scaling variable x = g_bar/a₀, system-independent ν.
  Data collapse onto a one-parameter scaling function *is* the phenomenology of universality.
  `[ANALOGY, apt]`
- **A rigid exponent.** The deep-MOND slope is **exactly 1/2** (g_obs ∼ g_bar^{1/2}), fixed
  by the SO(4,1) conformal weight of the cubic term (§0/CALC 1) — *independent* of galaxy
  mass, size, surface brightness, or gas fraction. A single exponent governing every galaxy
  is genuinely **critical-exponent-like**. This much is `[DERIVABLE → ANALOGY]`: the exponent
  is derivable; calling it a "critical exponent" is the (apt) analogy.

### What is over-reach (the honest deflation)
- **No diverging correlation length.** In real critical phenomena the scatter shrinks because
  ξ→∞ makes microscopic detail irrelevant. At a₀ the crossover is **smooth** and the relevant
  length (the radius where g∼a₀) is **finite, system-sized** — *not* divergent (§1). **The
  scatter-shrinking mechanism is simply not present.** `[the analogy fails here]`
- **The scatter is small for a different reason.** If g_obs is a deterministic function of
  g_bar — a *force law*, not a statistical fixed point — then the residual scatter is just
  measurement error + M/L variation. Lelli+2017 find the RAR's intrinsic scatter is
  **consistent with ~0** (≤0.06–0.069 dex, error-dominated). That is **a law being obeyed**,
  not a universality class emerging from fluctuations.
- **No anomalous dimension, no RG fixed-point spectrum.** The exponent 1/2 comes from
  *dimensional analysis* of the cubic term, not from an RG calculation; there is no
  nontrivial fixed-point operator spectrum to give "universal corrections." So the
  vocabulary of universality classes does not buy a calculation it didn't already have.

### The discriminator
Universality would be doing real work only if it predicted something the force-law reading
does *not*. It does not: "ν depends only on g_bar/a₀" is already the MOND statement, and
"intrinsic scatter →0" is already what a deterministic law predicts. **The two readings make
the same prediction**, so universality adds *no new content* on the shape or the scatter.

**Bottom line for §4:** universality is an **apt analogy for the rigid exponent**, a
**misleading one for the tightness**. The 0.069-dex scatter is **not** a fingerprint of
critical universality; it is the fingerprint of a deterministic acceleration law.

---

## 5. Does anything genuinely NEW fall out? — **No.** (audited, CALC 6)

Five candidate "predictions" were each tested for *novelty* and for whether they *follow from
the symmetry-breaking structure specifically*:

| candidate | status |
|---|---|
| smooth crossover (not sharp) | **explains why**, but std MOND is already smooth → **not new** |
| rigid deep-MOND slope 1/2 | **follows** from conformal weight, but = BTFR since 1983 → **not new** |
| light dilaton / fifth force / extra GW mode | **killed** (explicit breaking, no Goldstone) → a *negative* result, agrees with all nulls |
| running critical acceleration a₀(z) | **re-meanings** the framework's existing a₀(z)=cH(z)/Z; same number, same test → **not new** |
| universality bound on RAR scatter | scatter≈0 also predicted by a force law; the ξ→∞ mechanism is absent → **not new** |

**There is no genuinely new falsifiable number.** The symmetry-breaking picture is an
**illuminating re-description** with three *explanatory* (not predictive) payoffs:

1. **It explains why the transition is a smooth crossover** rather than sharp: a₀ is an IR
   scale tied to a conformal fixed point, so there is no order-parameter discontinuity (§1).
2. **It explains the repo's standing coefficient verdict in one line.** "Symmetry fixes the
   *form* (the cubic) but never the *breaking scale* (a₀)" *is* the statement that a₀ is a
   symmetry-breaking scale — and symmetry-breaking scales are never fixed by the symmetry
   they break. This is the structural reason behind the four worked forcing-route negatives
   in `FORCING_ROUTES_REWORKED.md`, now stated as a principle rather than a coincidence.
3. **It makes a clean negative statement** — no Goldstone, no MOND dilaton, no new fifth
   force (§3) — which is consistent with every null search and tells you *not* to look.

The one *existing* distinctive prediction, a₀(z) = cH(z)/Z, is **re-meaning-ed** by this
picture (the conformal-breaking scale tracks the de Sitter curvature, so the *location of the
crossover migrates with cosmic time*) but **not changed or extended**. Its test is unchanged:
halo-free high-z rotation curves (JWST/ALMA), framework ↑ vs constant-√Λ flat vs SIV ↓
(`FALSIFICATION_MATRIX.md`).

---

## 6. Honest ledger — derivable vs analogy, line by line

| claim | status |
|---|---|
| deep-MOND has exact SO(4,1) conformal symmetry; it forces the cubic \|∇φ\|³ in d=3 | **`[DERIVABLE]`** (Milgrom 2009 theorem; CALC 1) |
| a₀ is absent from the symmetric (deep) theory; appears only in the crossover | **`[DERIVABLE]`** (s=0 scaling; CALC 1) |
| the Newton→MOND transition is a **smooth crossover**, analytic for all g_N>0 | **`[DERIVABLE]`** (CALC 2) |
| the sole non-analyticity is at g_N=0, the conformal IR fixed point (quantum-critical-like) | **`[DERIVABLE]`** (CALC 2) |
| order parameter = η = \|∇φ\|/a₀; deep-MOND = symmetry-**restored**, Newton = **broken** | **`[DERIVABLE]`** structure; **`[ANALOGY]`** in the word "order parameter" (it is a control field, no VEV) |
| breaking is **explicit** (harmonic term), not spontaneous | **`[DERIVABLE]`** (CALC 3) |
| **no Goldstone**, no MOND dilaton, no new fifth force / GW scalar | **`[DERIVABLE]`** (CALC 3–4) |
| the two SO(4,1)s are the same group → a₀↔Λ | **`[POSIT / hypothesis]`** (the framework's welding, not a theorem) |
| rigid deep-MOND slope 1/2 is "a critical exponent" | **`[DERIVABLE exponent]` + `[ANALOGY label]`** (CALC 5) |
| the 0.069-dex scatter is a **universality** signature | **`[OVER-REACH]`** — ξ does not diverge; it is a deterministic force law (CALC 5) |
| "phase transition" framing yields a **new** prediction | **NO** — illuminating re-description, no new number (CALC 6) |

---

## Bottom line

Treating Newton→MOND as a symmetry-breaking phenomenon is **correct and clarifying, and it is
honest only if sold as such**. The transition is a **smooth crossover** governed by an **IR
conformal fixed point** (the non-analyticity is *at* the symmetric deep-MOND limit g_N→0, not
at the crossover); the order parameter is the dimensionless gradient |∇φ|/a₀, with **deep-MOND
the symmetry-restored phase** and **Newton the symmetry-broken one**; the breaking is
**explicit**, so there is **no Goldstone, no light MOND dilaton, no new fifth force** — a clean
negative that matches all null tests. The tight RAR scatter is **not** a universality
fingerprint (no diverging correlation length); only the *rigid slope-1/2* is legitimately
exponent-like. And **no new falsifiable prediction falls out**: the value of this picture is
that it *explains* (i) why the crossover must be smooth, (ii) why the cubic form is forced but
the scale a₀ is not — which is exactly the repo's four-route coefficient verdict, restated as
the principle that *a symmetry never fixes the scale that breaks it* — and (iii) why one should
*not* expect a MOND scalar. That is real understanding. It is not a new prediction, and this
document does not pretend otherwise.

---

### References
Milgrom, *MNRAS* / arXiv:0810.4065 (2009) — SO(4,1) conformal invariance of deep-MOND, forcing
the cubic. Bekenstein & Milgrom, *ApJ* 286, 7 (1984) — AQUAL. McGaugh, Lelli & Schombert,
*PRL* 117, 201101 (2016); Lelli et al. (2017) — the RAR and its intrinsic scatter. Deser &
Levin, *Class. Quantum Grav.* 14, L163 (1997) — the de Sitter–Unruh temperature underlying the
derived μ. Blanchet (2009) — dipolar dark matter (the polarization-field version of the
floor/harmonic/anharmonic structure). Internal: `ANHARMONIC_AND_32PI.md`,
`FORCING_ROUTES_REWORKED.md`, `GEOMETRIC_ORIGIN_OF_A0.md`, `FALSIFICATION_MATRIX.md`;
scripts `reviews/project_symmetry_breaking.py`, `reviews/desitter_unruh_RAR_test.py`.
