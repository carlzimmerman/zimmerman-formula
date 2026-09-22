# MAP — the weak-coupling frontier: what "control across the scaling window" requires (R5–R6)

Lane: `opus_49_doorC/` (audit + attempt, 2026-09-22). Companion: `AUDIT.md` (gate
verdict on YM05/YM07/I15), `LEMMA_doorC.md` (the sharpest attempted lemma), `verify_doorC.py`
(15/15 machine checks). House rule honoured: nothing here is claimed beyond what is proven
or registered; the strong-coupling constants audit is in AUDIT.md; the front line is mapped
exactly as the literature stands.

---

## 1. What the frontier actually is

The Clay object (Jaffe–Witten): a non-trivial quantum Yang–Mills theory on ℝ⁴ for a
compact simple gauge group, with a strictly positive lowest nonzero energy above the
vacuum. In the lattice route the regime picture (**YM_ROADMAP.md** R1–R7) is:

- **R4 — strong coupling, fixed spacing: PROVEN-ish.** Single plaquette: the general-N
  certified bound `gap_N(x) = x(N²−1)/N − 2N/x = 2xC_F − 2N/x > 0` for `N ≥ 2, x ≥ 2`,
  `gap_N(2) = (N²−2)/N` (SU(2)=1, SU(3)=7/3) — Lean-certified (`I15_suN_lattice_gap.lean`,
  exit 0, zero sorry) with the operator comparison in
  `real_research/reviews/spectral_spine_closure_2026_09_22/i15/PROOF.md`. Full lattice:
  an application of Yarotsky (math-ph/0411042) as an external theorem gives
  `Δ ≥ 3x/16` for `x ≥ X_d`, `X_d` **finite but numerically unspecified**; the bound is
  uniform in N and volume (PROOF.md §4). The operator theorem and X_d are NOT
  Lean-formalized; the repo's R4 correction (2026-09-22) registers exactly this.
- **R5 — lattice, weak/intermediate coupling ("the scaling window"): OPEN.**
- **R6 — continuum limit a→0, g²(a)→0 with gap persisting: OPEN — the Clay wall.**

So the honest three missing items (roadmap's own list, confirmed by this audit):

1. a continuum construction of the Euclidean YM measure (OS axioms) on ℝ⁴;
2. **uniformity of the spectral gap across the lattice sequence** a→0, g²(a)→0 (multi-scale
   non-perturbative bounds surviving weak coupling) — *this is the "weak-coupling control
   across the scaling window"*;
3. uniqueness/stability of the vacuum in that limit.

## 2. What rigorous technology exists, regime by regime (with the state of each)

**Lattice, strong coupling.** Reflection positivity + transfer matrix (Osterwalder–Seiler,
Commun. Math. Phys. 1978; Driessler–Fröhlich; Fröhlich's area law) give, at large β
(=1/g² small), exponential clustering and hence (OS reconstruction) a positive lattice
mass. The convergence technology is the **cluster/polymer expansion** (Glimm–Jaffe–Spencer
for lattice models; Kotecký–Preiss polymer expansion; Seiler's book). The repo's R4 uses
this frontier. **Status: closed for the lattice gap at strong coupling; does not reach
intermediate coupling.**

**Lattice, expanded/intermediate regimes (recent, real).** The probability/large-N route
improved the strong-coupling area law substantially: Chevyrev (Commun. Math. Phys. 372,
2019) solved large-N strongly coupled SO(N); Chatterjee–Jafarov (2016–) master-loop /large-N;
and **Cao–Nissim–Sheffield (2025–2026)**: *Expanded regimes of area law* (arXiv:2505.16585)
and *Dynamical approach to area law* (arXiv:2509.04688) prove Wilson area law in expanded
regimes including part of the 't Hooft regime for U(N), SU(N), SO(2(N−1)) (nontrivial
center), via the Durhuus–Fröhlich mass-gap condition. **All are fixed-spacing lattice
statements (area law / clustering), not continuum constructions.** They move R5's *lattice*
boundary, not R6.

**2+1 dimensions.** Superrenormalizable; the gap scale is dimensionally fixed (m ∝ g²).
Physics-level constructions: Karabali–Nair (hep-th/9602155) and Karabali–Kim–Nair
(hep-th/9705087) — Hamiltonian/loop-space, "physics-level rigor" (Witten's own
characterization). Balaban's renormalization-group machinery controls the 3D small-coupling
lattice. A fully axiomatic continuum OS construction with a theorem-grade proof is not
standard-form even in 3D; the roadmap's "physics-level, not the problem's axiom standards"
register stands.

**4D — the germane literature on the weak-coupling side.** Everything below is
*partial*: each piece solves a piece and stops before the object.

- **Balaban's renormalization group program** (Balaban 1984–1992, Commun. Math. Phys.
  series; with Imbrie–Jaffe/Brydges, e.g. *Ann. Phys.* 158 (1984) 281 for abelian U(1)
  Higgs mass gap on a unit lattice at weak coupling — the migration of the GJS cluster
  expansion to the weak-coupling/Gaussian neighbourhood). The program: **block-spin
  (decimation) transformations** that take the Wilson action toward the scale-invariant
  fixed point; control of the **effective action at every scale** (locality + boundedness,
  small-field propagator estimates), **large-field renormalization** and Gaussian-dominant
  small-field expansions; average gauge transformations; explicitly the **ultraviolet
  (small-distance) end**. Balaban's own contemporaneous caveats (quoted by MRS, below) and
  the community's view: the ultraviolet limit of lattice gauge theory along block-spin
  decimation was *claimed*; the **numerical value and full control of the effective scale
  X_d, the infrared (large–volume, strongly coupled) end, and the crossover are not part of
  a completed accepted theorem**. No finished, accepted construction of continuum SU(3)
  Schwinger functions with mass gap comes out of the program.
- **Magnen–Rivasseau–Sénéor** (Commun. Math. Phys. 155 (1993) 325): construction of SU(2)
  YM₄ *with an infrared cutoff* (finite box, trivial topological sector), axial gauge with
  large-field positivity, background-field-dependent gauge/propagator at small field,
  and a stability theorem for the UV-cutoff counterterms + Slavnov identities. Explicitly:
  *"we never try to lift the infrared cutoff … this would lead to large values of the
  coupling constant, presumably non-perturbative confinement effects … out of the realm of
  our constructive methods."* So MRS controls **finitely many scales** (a UV-end theorem);
  it is the blueprint for what Balaban-style control buys and where it terminates.
- **Federbush's phase-cell program** (*A phase cell approach to Yang–Mills*, I–VII,
  1986–1995, Commun. Math. Phys. 107 + Ann. Inst. H. Poincaré): lattice–continuum duality,
  small/large-field decomposition into "modes" and "chunks", the equations-of-motion route
  to the mass gap. Never completed into an accepted construction.
- **Reflection positivity / OS reconstruction** as a *transfer*: OS positivity on the
  hypercubic lattice (Osterwalder–Seiler), transfer-matrix ⇒ lattice Hamiltonian ⇒ gap from
  exponential clustering. This is the only strictly rigorous bridge from Euclidean bounds
  to a spectral gap, and it is lattice-side and strong-coupling-side.
- **Recent claimed 4D constructions (2023–2026)** — public claims on the record (Zenodo
  "Volume-Uniform Functional Inequalities"; "Lattice Coercivity and a Symmetry-Forced Haar
  measure"; the celestial/WZW holonomy route; a currents/Willmore-energy route; a
  reflection-positive multiscale route in IJGMMP) — are **not accepted mathematics**; the
  roadmap's register ("retracted / unverified / explicitly conditional") is unchanged by
  this audit. No independent verification against the problem's own standards exists.

## 3. The precise obstruction in 4D (why the pieces do not assemble)

Control of the mass gap across the scaling window needs all of the following at once,
and each is individually unsolved at the required uniformity:

1. **Many scales.** The continuum limit runs the coupling through
   g²(a) ~ 1/(b₀ ln(aΛ)), so the effective theory must be controlled across
   O(log(1/aΛ)) block-spin steps while g² runs from ~0 (short distance) to O(1)
   (confinement scale). Every *convergent-expansion* control known is a *small-parameter*
   control; the parameter (the running coupling, or the density of large-field regions)
   is NOT small over the whole window. This is the concrete meaning of "the strong-coupling
   expansion ends where the magnetic term overtakes the electric one" (R5): the
   **electric-vs-magnetic ratio has no uniform smallness**.
2. **Large-field ↔ small-field matching.** Balaban/MRS show the small-field (Gaussian)
   regime is controllable with a background-dependent gauge; the functional integral over
   large-field regions must be dominated by an *independent* convergent expansion
   (cluster-type), and the two must match under block-spin with constants that do not
   degrade with the number of steps. MRS proves this **with an infrared cutoff** (finite
   steps); the constants' summability over log(1/aΛ) steps at the strongly coupled end is
   exactly the missing uniform bound.
3. **The crossover itself.** The physical mass gap is a statement about the *long-distance*,
   strongly coupled sector (confinement); the perturbative/small-field machinery dies
   precisely there, and the strong-coupling machinery (area law, polymer expansions) has
   been pushed only toward *larger* β (Cao–Nissim–Sheffield et al.: area law in the 't Hooft
   regime), i.e. **away** from the crossover. There is no rigorous bridge across the
   weak→strong crossover at a fixed physical scale in d=4 — for SU(3), a theorem.
4. **Gauge-invariant, gauge-covariant technology.** Every expansion must respect (or
   compensate) gauge invariance: axial/background gauges break it, and the counterterm
   analysis (MRS) is a tour de force precisely because the compensation is hard.
5. **Uniformity + OS.** The repo's own corrected R4 shows the shape of the obtainable
   statements: a strong-coupling *uniform* gap (Yarotsky) exists but only for x ≥ X_d with
   X_d *numerically unspecified* — so even on the strong-coupling side the repo's
   many-plaquette window has no used number. The requirement for R5/R6 is a *used* uniform
   coupling window that survives volume → ∞ and then survives a → 0.

**Honest summary of the map:** the lattice strong-coupling gap (R4) is the only *certified*
rung; everything at intermediate coupling on the lattice has been pushed only at the
area-law level (R5's lattice face, partially), and **no accepted rigorous mechanism
transports a positive mass across the scaling window in 4D** (R5/R6). The single-plaquette
toy below is where the certified-bound technology ends and where an honest lemma is
actually writable (LEMMA_doorC.md), with the explicit caveat that the toy does *not*
transfer to the bulk.

## 4. The toy-model frontier (what this opus adds, scoped honestly)

For the **single-plaquette SU(2) model** the physical space is L²(class functions on SU(2))
and H is *exactly* a half-line Jacobi (tridiagonal) matrix — proven in LEMMA_doorC.md (L1),
a new in-repo structural fact. Consequences, all machine-checked in `verify_doorC.py`:

- the certified bound `gap ≥ 3x/2 − 2N/x` (β=2 lane display: `3x/2 − 2/x`) is a valid lower
  bound but the **true gap is much larger**: at x=2 the exact gap is 3.114 (β=2), and
  numerically `gap ≥ 2.196` for **all** x>0 (min at x≈0.99) — the single-plaquette gap never
  closes, even at weak coupling (the magnetic operator is bounded on a compact group and
  the character ladder is discrete);
- rigorously (L2): at strong coupling the magnetic shift **cancels to first order** —
  `gap = 3x/2 + O(x⁻³)` with explicit constants, i.e. the bound `3x/2 − β/x` underestimates
  the truth by ~β/x;
- the uniform-coupling lower bound (gap ≥ c for all x) is *within reach but not completed
  here*; the precise obstruction and the required (Mathieu/continuant) argument are in
  LEMMA_doorC.md L3.

**Why the toy does not transfer** (must be stated plainly): the single plaquette is a
zero-volume "universe" with finitely many degrees of freedom per character level and a
*bounded* magnetic operator; the bulk crossover is governed by volume-entropic and
many-loop effects exactly where the toy's discreteness saves it. The toy is therefore a
controlled warm-up that (i) sharpens what R4's certified numbers mean (lower bounds, not
gaps — PROOF.md already says this; here it is quantified) and (ii) shows the shape of a
rigorous statement one level harder than the certified one. It is **not** a step on the
R5/R6 path.

## 5. The frontier, in one line

R4 = the certified strong-coupling lattice gap (single plaquette + Yarotsky-with-unnamed-X_d);
R5 = open, and the only recent rigorous movement is fixed-spacing *area law* in expanded
regimes; R6 = open, with the exact missing object being **scale-uniform, used-constant,
gauge-covariant spectral control across the weak→strong crossover in d=4** — no accepted
mechanism of that kind exists, and no claimed proof in the 2023–2026 record satisfies the
problem's standards (registered, not adjudicated). Nothing in this opus changes R5/R6.