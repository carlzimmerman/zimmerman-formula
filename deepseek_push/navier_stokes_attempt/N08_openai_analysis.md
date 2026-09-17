# N08 — THE OPENAI FINITE-TIME BLOWUP FOR NAVIER–STOKES: DIGEST + FRAMEWORK CONSISTENCY

Lane: N08 (registered 2026-09-17 in N07_ACTION_DOOR.md as "the OpenAI record").
Sources read directly: OpenAI paper PDF via local clean-text cache (sections 1–3.6 verbatim;
the cache ends at the §3.6 symbol table, i.e. the ~first 19 pages of a 165–166 pp paper —
later sections are digested via the paper's OWN §3 proof outline + alphaXiv summary +
MathOverflow summary + the Lean statements, flagged below where that is so);
github.com/openai/NavierStokesAndEuler (tree via GitHub API, key files read raw);
openai.com/index/navier-stokes-solution/ (2026-09-08); Quanta Magazine (2026-09-08);
Wikipedia "Navier–Stokes priority controversy" (accessed 2026-09-17);
Stanford Tech Review audit "OpenAI vs Buckmaster: The Navier-Stokes Lean Proofs, Audited";
MathOverflow Q515056; alphaXiv 2609.navier-stokes. NOT built: the Lean project was NOT
compiled (task constraint); all formalization facts are from the source listing, raw file
reads, the audit, and the repo's own metadata.

HONESTY KEY: **[V]** = verified directly by me (source read above, or elementary math I
computed). **[OA]** = OpenAI's claim (paper/announcement), unverified by me. **[T]**
= third-party claim/report, attributed. **[ZMF]** = this lane's analysis (labelled as such,
including where it is interpretation). The theorem itself is **[OA]**: it has NOT been
independently refereed as of 2026-09-17 ([T]: Clay status "active", not "solved").

---

## 1. THE THEOREM

### 1.1 Theorem 1.1 (whole space ℝ³) — [OA statement, verbatim from the cache]

For every ν > 0 there exist a force f ∈ C^∞_c(ℝ³ × (0,∞); ℝ³), a compact set K ⊂ ℝ³,
and smooth velocity and pressure fields u, p on ℝ³ × [0, 1) satisfying

    ∂ₜu + (u·∇)u − νΔu + ∇p = f,   ∇·u = 0,   u(·,0) = 0,

such that supp u(·,t) ∪ supp p(·,t) ⊂ K for every 0 ≤ t < 1,

    sup_{0≤t<1} ‖u(t)‖_{L²(ℝ³)} < ∞,        limsup_{t↑1} ‖u(t)‖_{L∞(ℝ³)} = ∞.

Consequently there is no smooth solution (u,P) on ℝ³ × [0,∞) with the same force and
initial datum whose kinetic energy is uniformly bounded. This is Fefferman's alternative
**(C)** (breakdown on ℝ³). Compact support yields the corresponding construction on the
torus 𝕋³ = ℝ³/ℤ³ — alternative **(D)** — via Corollary 10.6 ([OA]; the torus form needs
no bounded-energy clause: on the torus smoothness alone bounds energy).

### 1.2 The C/D alternatives — [V] placement

Fefferman's Clay statement has four alternatives: (A)/(B) = global regularity for all
smooth *unforced* data on ℝ³/𝕋³; (C)/(D) = existence of smooth *forcing* for which no
global smooth solution exists. The OpenAI result claims (C) **and** (D) — the forced
breakdown side. **(A)/(B) (unforced regularity) are untouched by this theorem.** The
result is forced, with f ∈ C^∞_c; the "popular" question — does turbulence blow up on
its own — is not what is claimed.

### 1.3 Energy-bounded statement — [OA] + [ZMF]

Theorem 1.1 includes sup ‖u(t)‖_{L²} < ∞ (bounded kinetic energy on ℝ³ through the
singular time). The energy budget is explicit in §3.5: the concentrating core has
volume ≍ τ^{3/2−h} and velocity ≍ τ^{−1/2−h}, so E_core ≍ τ^{1/2−3h} → 0 (τ = 1−t).
Integrated dissipation D_core ≍ τ^{−1/2−3h} with ∫₀^{τ₀} τ^{−1/2−3h}dτ < ∞ as long as
h < 1/6 (the construction uses 0 < h < 1/100, well inside). Lemma 10.4 ([OA], §3.5)
proves the global energy inequality and integrated dissipation bounds for the localized
fields *from the equation itself*; the Lean library contains the energy + dissipation
theorem verbatim (see §4, `theorem_1_1_with_dissipation`).

### 1.4 Scaling in ν — [V]

A viscosity-one solution gives one at any ν via u_ν(x,t) = √ν·u(x/√ν, t),
p_ν = νp(x/√ν, t), f_ν = √ν·f(x/√ν, t); singular time unchanged (paper (10.22)–(10.23)).
This is a standard NSE self-similar rescaling; the ν-dependence of the theorem is thus
genuine and uniform.

---

## 2. THE CONSTRUCTION'S ANATOMY

(All from the paper's §2–§3, which is the authors' own proof outline, [OA] technical
statement. Later-section specifics (Prop 5.5 body, Appendices) were not read in full —
flagged where relevant.)

### 2.1 The leading axisymmetric self-similar core — [OA]

Singularity forms at the origin at t = 1. Cylindrical coordinates (r, θ, z); τ = 1−t;
two concentration scales:

    ℓ_r ≍ τ^{1/2},        ℓ_z ≍ τ^{1/2−h},        0 < h < 1/100,

so ℓ_z/ℓ_r ≍ τ^{−h} → ∞: the core is an increasingly **slender column** (radius shrinks
faster than height; volume ≍ τ^{3/2−h}). Velocity scales:

    |u_θ|, |u_z| ≍ τ^{−1/2−h},        |u_r| = O(τ^{−1/2}),

with u_θ vanishing on the axis (regularity there); u ≡ 0 at t = 0 and the fluid is at
rest for |t| ≤ 3/8 ([V]: Lean `theorem_1_1_with_initial_rest`).

Similarity coordinates: τ = q(1−η²), z = q^D η, X = r²/2q, with A = 1/2+h, D = 1/2−h;
leading fields u_θ = q^{−A}E(X,η), u_z = q^{−A}U(X,η), ru_r = V₀(X,η), p = q^{−2A}Π(X,η);
E/√(2X), U, V₀/X smooth at X=0 (axis regularity). E > 0 for X > 0, with exterior tail
E(X,η) = c∞·X^{−1/2−h}(1+O(X^{−1})).

### 2.2 The Re_θ → ∞ vs Re_r = O(1) split — [OA]

With length ℓ_r and viscosity ν:

    Re_θ := |u_θ|ℓ_r/ν ≍ τ^{−h} → ∞,        Re_r := |u_r|ℓ_r/ν = O(1).

The radial Reynolds number stays O(1) so viscosity still competes with radial inflow —
this is what makes the problem viscous (not an Euler construction). Transport/diffusion
rates: |u_r|/ℓ_r = O(τ^{−1}), |u_z|/ℓ_z ≍ τ^{−1}, ν/ℓ_r² ≍ τ^{−1} (leading balance);
axial diffusion is a factor ℓ_r²/ℓ_z² ≍ τ^{2h} smaller (it is the background expansion
parameter — the q^{2nh} correction recursion).

### 2.3 The dividing layer — [OA]

The core has a "dividing layer" near z = 0, with axial outflow on opposite sides.
An exact-reflection-symmetric profile would give uz(r,0,t) = 0 and no radial shear of
axial velocity; the construction chooses a **slightly asymmetric axial profile** (small
upward bias, nonzero velocity at z = 0) to separate the layer where rotational
amplification (centrifugal instability from steep ∂(ω)/∂r) is weak from the layer where
axial shear vanishes — the radial shear of axial velocity supplies the extra pulse
amplification near the mid-plane.

### 2.4 The pulse annulus — [OA]

The background solves its leading momentum balance in the inner core and exactly in the
heat exterior; the mismatch is confined to an **annulus** X_a < X < X_b (i.e.
√(2qX_a) < r < √(2qX_b)). The residual of (u^(0), p^(0)) is written as the divergence of
an annular stress T = (T_rθ, T_rz):

    R_θ^(0) = −(∂_r + 2/r)T_rθ,        R_z^(0) = −(∂_r + 1/r)T_rz,

with T = 0 for X ≤ X_a and X ≥ X_b enforced by two zero-moment identities
(∫ r²R_θ^(0)dr = 0, ∫ rR_z^(0)dr = 0) fixed by exterior-moment matching (Lemma A.8,
Lemma 4.4). Profiles are built: exterior + axis pressure datum (Prop A.4/A.6/A.7),
inner analytic solution (Prop B.2, analytic in X,η near the axis), joining + five radial-
moment matching (Cor B.10, Prop B.8), then the admissible-stress-cone condition is forced
on a compact sub-annulus by a radial oscillation with phase N·log X, amplitude O(N^{−1})
(Prop C.2/C.3). The paper's §1.1 credits the wave/hyperbolic-cone technology line:
Daneri–Székelyhidi (oscillation realization of stress), Singh–Sridhar (exact viscous
shearing waves), Billant–Gallaire (generalized centrifugal-instability criterion),
Lifschitz–Hameiri / Friedlander–Vishik (wavevector evolution), Tao (averaged NSE blowup),
Buckmaster–Vicol and Albritton–Brué–Colombo (convex integration / non-uniqueness).
NOTE ([T] + [V]): the cached copy's §1.1 does NOT cite Córdoba–Martínez-Zoroa; Wikipedia
reports Buckmaster's criticism that the initial release omitted their work and that a
166-page revised version added the references. The C–MZ line is the acknowledged source
of the "layered cascade with smooth forcing" strategy ([T]: Quanta — Córdoba: "if their
work had not existed, AI would not have solved the problem").

### 2.5 The two pulse families with averaged-stress realization — [OA]

Pulses: spatially oscillatory, localized in (r, z, t), extending around complete rings,
with zero angular mean velocity but nonzero averaged momentum flux. Scales
(suppressing log factors and edge weights):

    A_wave ≍ q^{−1/2−h/2},        ℓ_wave ≍ q^{1/2+h/2},        A_wave² ≍ q^{−1−h}

so A_wave²/√q ≍ q^{−3/2−h} = the scale of the leading stress divergence it must cancel.
Exact residual identity for a divergence-free increment w:

    R(u_B + w, p_B + π) = R(u_B, p_B) + L_{u_B}(w,π) + ∇·(w⊗w)

with L the linearized operator. Pulses are built on an **auxiliary torus** Y ∈ 𝕋² with a
fixed phase map Y(r,t); overlapping slow supports receive disjoint supports in Y so
cross-products vanish (Lemma 6.1). Physical realization: w = ∇×A_wave (exactly
divergence-free; curl corrections bounded in Cor 7.8). Two pulse families with linearly
independent covariance vectors v₁,v₂ ∈ ℝ² (per-unit-amplitude momentum fluxes); the
profile data are chosen so the target stress lies in the **interior of the cone**:

    T = c₁v₁ + c₂v₂,   c₁,c₂ > 0     (admissible stress cone condition, Lemma 4.5)

and the leading averaged quadratic flux reproduces T: ⟨w̃_r w̃_θ⟩, ⟨w̃_r w̃_z⟩ = T +
higher-order (Prop 7.5, Cor 7.8; the cone is realized via the N·log X shear oscillation
of Prop C.2/C.3 — see 2.4). Amplification: background shear (centrifugal + axial-shear)
grows the pulses (Lemmas 7.1, 7.4); viscous damping grows as the radial wavelength
shortens under differential rotation; net envelope is grow-then-decay (Fig 3b), with the
temporal cutoff acting only in exponentially small tails.

### 2.6 The heat exterior — [OA]

For X ≥ X_ext: purely azimuthal, z-independent, radially decaying flow (A = 0):

    u = K(r,τ) e_θ,  p = −∫_r^∞ K(ρ,τ)²/ρ dρ,   K(r,τ) = r^{−1−2h}·H_ext(τ/r²),

where K solves the **radial swirl heat equation** −∂_τK = ∂_r²K + r^{−1}∂_rK − r^{−2}K
exactly (momentum residual identically zero; no force needed in the exterior). All
derivatives have smooth limits as t↑1 at every fixed r > 0 — this is what makes the
final spatial cutoff smooth through the singular time.

### 2.7 Cutoff / localization — [OA]

Local fields are multiplied by c = χ_x(t)·χ_t(t) (axisymmetric compact spatial support K,
temporal support starting after 1−τ₀); u = curl(cA) + c·B e_θ (each piece divergence-free),
p = c·ploc; the curl term ∇c × A is retained. Cutoff-transition terms are supported away
from (0,1) and are smooth (Thm 3.1(ii) bounds all derivatives on q ≥ c > 0). Near (0,1)
the cutoffs are 1, so the force is just the local flat residual; Lemma 10.2 gives
compatible limits, Lemma 10.3 realizes f ∈ C^∞_c(ℝ³ × (0,∞)) with f = R(u,p) on
0 ≤ t < 1. The growth path (3.6) lies in the cutoff-identity region, so the blowup
survives localization.

### 2.8 The residual-smoothing proposition chain — [OA, outline-level statements]

The paper proves the residual is *flat*: every Cartesian space-time derivative is
O(q^N) for every N ≥ 0 as q↓0 (the concentration parameter), uniformly on bounded X —
eq. (3.4), stated as Theorem 3.1(iii). The chain that produces this:

| step | proposition | content (per §3 outline; exact bodies not read in full) |
|---|---|---|
| background construction | **Prop 5.5** | smooth axisymmetric background (u_B,p_B) with residual R(u_B,p_B) = −(∂_r+2/r)T_phys,θ e_θ − (∂_r+1/r)T_phys,z e_z + E_B, T_phys supported in annulus with leading term T, E_B flat (q^N for all N). |
| oscillatory realization | **Prop 7.5** | two divergenceless pulse families; averaged quadratic flux = T + higher order; radial divergence cancels leading stress divergence (with Cor 7.8 derivative bounds). |
| correction cycle | **Prop 9.6** (+ Props 9.1, 9.3, 9.5; Lemmas 9.2, 9.7) | 4-step cycle: (1) inhomogeneous wave-amplitude equations for nonzero angular Fourier modes; (2) signed amplitude increments via symmetrized cross-covariance; (3) correction of angularly averaged residual by inverting the fast auxiliary-time derivative ((8.20), axial increment via vector potential (8.14)); (4) five radial moment equations (8.25) preserving two zero integrals (9.10) and killing (P, J_θ, J_z). Residual decay exponent σ₀ = 1/5, σ_{j+1} = σ_j + 1/10 → ∞; bound (9.18): |∂^α∂^bR| ≤ C·q^{hσ_j − K_m}·(logs). |
| summation | **Prop 9.9** (+ Lemma 5.4) | sum corrections with cutoffs shrinking in q, equal to 1 near q=0; locally finite for q>0; flat residual (3.4); vector potential representation; regularity up to time one away from origin; leading growth preserved. |
| localization & completion | **Prop 10.1**, Lemmas 10.2–10.3 | (see 2.7): cutoffs, smooth force f ∈ C^∞_c, energy bounds (Lemma 10.4), uniqueness (Lemma 10.5) → Theorem 1.1. Corollary 10.6: torus version. |

This is the correct order of operations and the correct content per the paper's own §3
("Proof outline") — the *bodies* of Props 5.5/7.5/9.6/10.1 and the Appendices were NOT
independently verified in this lane (cache ends at ~p.19; only outline-level and Lean-
statement-level facts are claimed here).

---

## 3. THE MAIN ESTIMATES (what is actually proved)

**[OA, statements per paper §3 + [V] for the Lean mirror]**

1. **All-derivative residual control through the singular time.** Theorem 3.1(iii):
   |∂^α_x ∂^b_t R(u,p)| ≤ C_{α,b,N,X₁}·q^N for 0 ≤ X ≤ X₁, q↓0, every N — the residual
   and ALL its space-time derivatives vanish to every order at the singularity (flatness).
   This is the technical heart: it is what turns the constructed (u,p) into an exact
   solution with a smooth compact force f := R(u,p) on all of ℝ³ × [0,1).

2. **Local regularity of the solution itself.** Theorem 3.1(ii): A, B e_θ, p smooth in
   Cartesian coordinates on compact sets with c ≤ q ≤ c′ < q*, with compatible one-sided
   limits at τ = 0 (i.e., u is smooth in space and time for every t < 1, with high-order
   spatial regularity persisted up to the singular time away from the origin);
   Theorem 3.1(iv): the growth path u_θ(√(2X_in·τ), 0, 0, 1−τ) = τ^{−A}(e₀ + O(τ^{2h})),
   e₀ > 0 → the L^∞ blowup is on an explicit ray to the origin.

3. **Energy and integrated dissipation (Lemma 10.4).** For the localized fields, from
   the equation: E_core ≍ τ^{1/2−3h} → 0, ∫₀^{τ₀}τ^{−1/2−3h}dτ < ∞ (h < 1/6), and the
   global bounds: sup_{0≤t<1}‖u(t)‖_{L²} < ∞ plus integrable dissipation on [0,1).
   [V] Lean: `theorem_1_1_with_dissipation` — IntervalIntegrable(‖f‖_{L²}) on 0..1,
   IntegrableOn(dissipation), and the energy inequality
   ‖u(T)‖_{L²}² + 2ν∫₀^T diss ≤ (cumulative force norm T)² for all T < 1, plus the
   total-dissipation bound at T=1.

4. **Uniqueness (Lemma 10.5).** Any smooth solution with the SAME force and zero
   initial datum whose kinetic energy is uniformly bounded must agree with the
   constructed u on every [0,T], T < 1 (standard uniqueness for the energy class);
   a global smooth solution would therefore coincide with u on [0,1), contradicting
   the L^∞ blowup on the growth path → no global smooth bounded-energy solution.
   [V] Lean: `¬ Nonempty (GlobalFiniteEnergySolution ν f)` in `R3/Theorem.lean`, built on
   `R3/ViscousUniqueness`, `R3/WholeSpaceUniqueness`, `R3/ComparisonGronwall`, etc.

Honest caveat: these are the paper's assertions of what is proved, mirrored by the Lean
theorems; no independent human check of the 165-page argument exists yet ([T]).

---

## 4. THE FORMALIZATION STATE (inventory; NOT built)

**[V]: repo tree via GitHub API 2026-09-17; [V]: raw reads of key files; [T]: Stanford
Tech Review audit numbers (their counts may differ slightly from the live tree — they
reported at a specific commit; both are reported here).**

Repo: **github.com/openai/NavierStokesAndEuler** (Apache-2.0), single squashed commit,
no development history ([T]: both OpenAI and B&A repos are one-commit; all dates rest on
testimony). Toolchain (verified raw): `lean-toolchain` = **leanprover/lean4:v4.34.0-rc2**;
Mathlib + Lake (README: `lake exe cache get; lake build`). This is the SAME Lean 4
toolchain family used in this framework's own lanes (N07 notes it) — the `v4.34.0-rc2`
string matches the repo's own file.

**Live tree counts (my API pull):** 2,659 `.lean` files total —
`NavierStokes/` 817 (incl. `NavierStokes/R3/` 110), `Euler/` 1,840, `ComparatorChallenges/`
2 Lean files + 2 JSON configs; root: `NavierStokes.lean`, `Euler.lean` (importers),
`lakefile.toml`, `lake-manifest.json`, `formalization.yaml`, `lean-toolchain`, `README.md`,
`LICENSE`, `.gitignore`.
[TSTR] audit at release time: 2,484 Lean files / 616,274 lines / 35,731 theorems+lemmas /
0 unproven `sorry` / 4 placeholder `sorry` (in statement files, by design) / 0 extra
`axiom`; claims rest on Lean's standard three axioms {propext, Classical.choice,
Quot.sound} (confirmed by `formalization.yaml`). (For scale: the Buckmaster–Alpöge repo:
3,612 files / 1,684,580 lines / 68,179 theorems+lemmas, toolchain 4.32.2.)

**Declared main results (`formalization.yaml`, [V]):**
- (C) `NavierStokes.Comparator.navier_stokes_breakdown_R3` —
  file `NavierStokes/ComparatorSolution.lean`, sorry_count 0, axioms =
  {propext, Classical.choice, Quot.sound}.
- (D) `NavierStokes.Comparator.navier_stokes_breakdown_periodic` — same file/config.
- Euler (own result): `Euler.euler_breakdown_R3`,
  `Euler.exists_compact_smooth_euler_singularity` — file `Euler/Solution.lean`.
- `review.status: "self-assessed"` — the formalization's own metadata marks it NOT
  independently reviewed. Comparator challenge configs (`ComparatorChallenges/NavierStokes.json`
  / `Euler.json`) are provided so third parties can re-verify with the Comparator tool
  (0-axiom, no-sorry checking pipeline); the comparator reference statements come from
  google-deepmind/formal-conjectures (`related_formalizations.builds-on`).

**Key theorem statements read verbatim:**
- `NavierStokes/ProblemStatement.lean`: exact definitions (unit-period lifts, Fréchet
  derivatives, `navierStokesResidual`, `SpeedUnboundedAtOne`, `CandidateProperties`
  structure: u,p ContDiffOn ∞, f ContDiff ∞ + compact future time support, zero initial
  velocity, divergence-free, NSE on 0<t<1, speed unbounded); `candidateStatement` is
  deliberately a proposition, not an axiom. The paper's whole-space statement is stated
  as an existential over (u,p,f,K) with `¬ Nonempty (GlobalFiniteEnergySolution ν f)`
  (R³: energy-bounded competitor) — exactly alternative (C).
- `NavierStokes/R3/Theorem.lean`: `theorem_1_1` (breakdownStatement, ∀ν>0), plus the
  stronger `theorem_1_1_with_initial_rest` (u = p = 0 for |t| ≤ 3/8) and
  `theorem_1_1_with_dissipation` (energy inequality + integrable dissipation —
  the Lean form of Lemma 10.4).
- `NavierStokes/PeriodicPaperTheorem.lean`: `periodic_corollary : breakdownStatement`
  — periodic lifts, support inside the fundamental cube, `GlobalSmoothSolution` (no
  energy clause needed on torus), theorem `of_compact_candidate` (periodization path:
  compress supports into the central 1/4-cube, discard post-one extensions, lattice-sum).
- Root `NavierStokes.lean` / `Euler.lean` aggregate the namespaces.

**Honest inventory limits:** counts from the live tree may drift (the audit's 2,484 vs
my 2,659 `.lean` files — the audit figure likely excludes the Euler subtree's later
additions or counts differently; both reported). No build was attempted; compile
success is not verified by this lane. Nothing here certifies the *informal↔formal*
equivalence — the classic "formality gap" ([T] Quanta: "The crucial bit of verification
that must still be done by humans is to guarantee that the statement being shown to be
true in Lean is logically equivalent to what mathematicians set out to prove."). The
formalization covers what it covers: (C) and (D) as existential statements with smooth
compact force, zero initial data, speed unboundedness, and non-existence of bounded-
energy global smooth solutions.

---

## 5. THE CONTROVERSY STATE (cited; consensus as of 2026-09-17)

### 5.1 What is verified ([V]/[T])
- The paper exists (PDF, CDN), the Lean repo is public, toolchain pinned, no sorries,
  no extra axioms ([TSTR] audit; `formalization.yaml`).
- CMI status: Wikipedia [T] — Clay (Bridson, 9/11) acknowledges "the Navier–Stokes
  problem has apparently been settled" but requires **peer-reviewed publication** before
  any prize consideration; "the process... is deliberately unhurried"; website status
  "active" (neither unsolved nor solved).
- OpenAI explicitly does not claim the Millennium Prize ([T] Wikipedia; [OA] announcement).
- Timeline/scale claims (all [OA], repeated by [T]): begun 1 Sept after rumors; ~10,000
  agents, ~88 h to the result, +17 h Lean verification via GPT-6 Astra; "almost 5 million
  messages" (Quanta) vs 2.7M messages / 130B tokens (Wikipedia); cost "several million
  dollars" (Bubeck, per Quanta) vs "$15m of AI effort" (New Scientist headline [T]).
- A parallel, independent-ish result: Buckmaster–Alpöge (same day, ~12 h earlier)
  announced smooth-forced blowup for 3D Euler, IPM, Boussinesq, with their own Lean
  formalization ([T] Wikipedia/Quanta). Tao, ~30 min after B's announcement [TSTR]:
  "a remarkable achievement", crediting Córdoba–Martínez-Zoroa; Tao judged separately
  that nothing in principle prevents these methods from reaching NSE (written before
  OpenAI's announcement).

### 5.2 The priority/provenance dispute ([T] Wikipedia, NYT 9/10 "An N.Y.U.
Mathematician Clashed With OpenAI...", Quanta, B&A statement 9/7 eve)
- Buckmaster's claim: their Euler/IPM/Boussinesq work (obtained 15 Aug, Lean-verified
  22 Aug, per their statement) may have leaked to OpenAI via Codex usage; he raised
  concerns about user-data access and about pressure to reframe credit; "I am sorry
  for this" re releasing a paper he calls "AI slop".
- OpenAI's response timeline [T/Wikipedia]: 9/8 — "no specific user data was accessed...
  while unlikely, we cannot rule out that de-identified data... helped improve our
  models"; 9/9 — "categorically impossible" for Buckmaster's Codex prompts (last two
  months); 9/10 — internal investigation, same; 9/13 — "no user inputs past July 3rd
  could have influenced this system in any way". OpenAI cedes Euler priority to B&A,
  claims NSE for itself; says proofs differ (forced vs unforced Euler; NSE methods
  "appear different" — Chandrasekaran) — Alpöge disagrees ("looks more along the lines
  of another Euler blowup proof we had").
- Neither side can be adjudicated from the record: both repos are single squashed
  commits ([TSTR]).

### 5.3 Technical/mathematical criticism
- References: Buckmaster criticized the initial NSE paper for omitting Córdoba–
  Martínez-Zoroa; Wiedemann noted a longer reference list was expected; the released
  version was revised (166 pp) with the lineage added ([T] Wikipedia; [V] the cached
  copy's §1.1 indeed cites the oscillation/convex-integration line but not C–MZ).
- Córdoba: "if their work had not existed, AI would not have solved the problem"
  (credit claim, not an error claim) [T/Quanta]; Fefferman: "I was thrilled that the
  problem was solved... The heroes of the story are Córdoba and Martínez-Zoroa" [T] —
  a credit statement, NOT a line-by-line endorsement (Fefferman has made no public
  detailed scrutiny claim).
- No named mathematician has, as of 2026-09-17, published a substantive error claim
  against the NSE construction. The MathOverflow discussion thread (Q515056, 3k views)
  is [closed] with no mathematical answers; its questions — compatibility with
  Caffarelli–Kohn–Nirenberg partial regularity, Escauriaza–Seregin–Šverák L^∞_t L^3_x,
  Constantin–Fefferman vorticity-direction — are stated for the unforced/restricted-
  forcing setting and remain OPEN questions about the construction, not refutations.
  (One anonymous MO answer claims to have built "sandbox falsification" filters
  alleging a "stealth anti-viscosity" feature of f; unverified, anonymous, and not
  endorsed by any authority — reported here only for completeness.)
- Refereeing process: unprecedented scale (165–166 pp, ~10⁴-agent provenance, ~35k
  formal theorems) — MO Q3 asks whether any normal refereeing process applies; no
  journal has announced peer review as of 9/17 ([T] CMI statement).

### 5.4 Community consensus (as of 2026-09-17, [T]-synthesized)
1. The Lean formalization gives mechanical confidence in the *formal* statements (0
   sorries, 0 extra axioms), and the CMI status moved to "active" — but the informal
   claim is NOT accepted: peer review is pending, the human-checkable statement
   equivalence is unchecked, and the CMI prize process has not started.
2. The intellectual origin of the strategy is universally credited to Córdoba and
   Martínez-Zoroa (Fefferman, Tao, Buckmaster himself: "Luis deserves a Fields Medal");
   that lineage is now also in the revised paper.
3. The public discourse (news, social media) is dominated by the provenance dispute and
   by structural worries about AI research practice (Sarnak, Dancso, Thom, Lee, Harris,
   Strogatz, Escher; Tao on communication-by-press-release and rumor-triggered races) —
   which several commentators note could slow or skew independent verification.
4. (A)/(B) remain open: nobody claims unforced global regularity or unforced blowup for
   NSE; Tao's extension remark concerns the forced-B&A methods.

---

## 6. FRAMEWORK CONSISTENCY ANALYSIS (vs N07_ACTION_DOOR.md)

Read first: N07 doors — D1 cusp, D2 caustic channel (phantom dust is the framework's
singular sector), D3 transfer (K-1 cap a₀/2 kills; K-2 coupling-lives opens), D4 Jeans
time; N05 window theorem (W = 7/2, ceiling 3.5·a₀ = 3.2767e-10 m/s², exit corollary);
N05_VERDICT (Clay on the Newtonian face, N3 completing family, κ→0 = Clay gap).

### 6.1 The N5 window corollary — CONSISTENT, and now witnessed [ZMF]

Corollary (N05): any finite-time singularity of classical 3D periodic NSE forces
|Du/Dt| > 3.5·a₀ at some t₀ < T* — the singular regime, if it exists, lives strictly
ABOVE the measured floor (the Newtonian face). The OpenAI construction (which we may now
take as the existence witness, modulo referee status) satisfies the exit requirement
with unbounded margin. **Scaling verification [V-computed]:**

|Du/Dt| ≍ τ^{−(3/2+2h)} → ∞. Derivation: |u| ≍ τ^{−1/2−h}; the dominant material-
acceleration term is the centripetal piece u_θ²/r ≍ τ^{−1−2h}/τ^{1/2} = τ^{−3/2−2h}
(time-derivative and transport terms are τ^{−3/2−h}, smaller by τ^h > 0 — the h < 1/100
window keeps the centripetal term dominant). Hence for ANY window floor W·a₀:

  |Du/Dt|(t)/a₀ = C·τ^{−(3/2+2h)}  →  ∞,   i.e. η(t) → ∞ as t↑1 ;

the floor 3.5 is crossed at τ_exit = (3.5/C)^{1/(3/2+2h)} — which for the natural
physical normalization (singular time 1 s, core unit speed ~1 m/s at τ = 1, i.e.
C ≈ 1 m/s²) is τ_exit ≈ 5.2e-7 (h = 0.005; 5.8e-7 for h = 0.01): the flow is already
ABOVE the floor for the final ~10⁶ decades of τ while still smooth (|u| ~ 1.5e3 units
at exit, all derivatives finite). The margin |Du/Dt|/(3.5·a₀) → ∞: the construction
exits ANY window floor by an unbounded margin BEFORE t = 1. **The blowup lives above
3.5·a₀ — the Newtonian face — exactly where the framework's law is silent.** Consistent
with the N05 corollary's content and falsifier-F-W3's exit diagnostic (window left while
the field is still smooth).

**The η(t) curve in normalized units [V-computed, honest mapping].** The construction's
own scale has no a₀ (its units are ν = 1, singular time 1); a₀ must be injected as the
physical constant. With the one free realization parameter λ = √ν·c (c = profile
constant), η(τ) = (λ/a₀)·τ^{−(3/2+2h)} (the ν-rescaling u_ν = √ν u(x/√ν,t) preserves
t = 1 and scales accelerations by √ν). Values (h = 0.005, λ = 1 m/s², a₀ = 9.3619e-11
m/s²):

  τ = 1.0      : η ≈ 1.07e10   (|Du/Dt|/ceiling ≈ 3.1e9)
  τ = 0.1      : η ≈ 3.5e11    ("start of the final decade")
  τ = 1e-2     : η ≈ 1.1e13
  τ = 1e-6     : η ≈ 1.2e19

i.e. at the start of the final decade η is **~10¹⁰–10¹¹ class** (1e10 at λ ≈ 2.9e-2 m/s²
core-acceleration scale — a centimeter-scale lab vortex; larger realizations are even
further above the floor). So: in physical lab units the construction's η(t) is ~1e10-
class at the start of the final decade and diverges as τ^{−(3/2+2h)}. The framework
floor (3.5) and even the strongest framework input (a₀/2 cap — see 6.2) are left behind
by 9+ orders of magnitude before the final decade begins.

### 6.2 The bounded-perturbation statement (N2/N4's a₀/2 cap) — CONSISTENT [ZMF]

The OpenAI blowup is a **pure-NSE object**: it needs only classical NSE with f ∈ C^∞_c;
no "extra physics" is used anywhere (the pulses are internal stresses of the SAME
equation — ∇·(w⊗w) inside the residual). The framework's sub-regularizing modifications
are universally bounded: |g_obs − g_N| ≤ a₀/2 ≈ 4.68e-11 m/s² EXACTLY (N2/N4 Lean-
certified `a0cap_bound`). Quantitatively [V]: at τ = 0.1 the singular dynamics run at
|Du/Dt| ≈ 3.5e11·a₀, i.e. ~7e11 times the ENTIRE available framework modification; at
at the floor-exit τ ≈ 5e-7 the dynamics are already at 3.5·a₀ and rising — the ratio
|Du/Dt|/(a₀/2) ≥ 7 and → ∞. A bounded perturbation of size a₀/2 cannot prevent a
blowup whose divergent terms are a power law τ^{−(3/2+2h)}: to kill the mechanism one
would need to modify the dynamics at the scale of its dominant balance, which the cap
forbids by 10+ orders of magnitude.
Also: the framework's own Singular sector (N07 D2) is the **phantom dust** — pressureless,
collapsing on the Jeans/free-fall timescale τ_ff = 1/√(Gρ_ph) ≲ 10⁸ yr at 1 kpc; the
OpenAI singular sector is the **baryon/visible NSE fluid** (viscous, incompressible).
**They are DIFFERENT fluids**: the OpenAI theorem says nothing about the dust, and the
framework's D2 says nothing about visible-fluid NSE blowup. No conflict — the two
singular sectors are disjoint objects, and the OpenAI result is precisely the "Clay
singular regime above the Newtonian face" that N05's corollary (if the regime exists)
predicted the geometry of: it exists, it is forced, it lies at η ≫ 3.5 where the
measured law differs from Newton by ≤ a₀/2 (i.e. is silent). K-1 (bounded cap) is
unaffected by the OpenAI result: the transfer door D3 dies on the MEASURED cap exactly
as registered, and the OpenAI record confirms the complementary face (N07's status
register reading: "the visible-fluid Clay problem is a Newtonian-face question").
Caveat [ZMF]: this consistency is conditional on the OpenAI claim's truth (referee
status pending); the *structure* of the consistency argument does not depend on it, but
the "witness exists" phrasing does.

### 6.3 The singular-sector read (N07 D1/D2/D4) — CONSISTENT [ZMF]

- D1 (cusp): untouched by the OpenAI result (static dust cusp vs dynamic visible-fluid
  blowup; different sectors).
- D2 (caustic channel): the framework's singular sector is the phantom dust forming
  caustics on τ_ff; the OpenAI singular sector is visible-fluid velocity unboundedness
  at t = 1. Different fluids, different singularities (density caustic vs velocity
  blowup), no overlap. There is no claim in the OpenAI paper about pressureless dust,
  and no claim in D2 about NSE; consistency is exact.
- D4 (Jeans time): irrelevant here (dust timescale 10⁶–10⁹ yr vs the NSE singular time
  1 unit) — different clocks, no interaction.

### 6.4 Technique transfer (N07 D3, K-2 branch) — honest assessment [ZMF]

IF the G03 coupling ever opens (the action's phantom–baryon coupling exceeding the
measured a₀/2 cap off equilibrium — K-2), what of the OpenAI toolkit is reusable for
constructing blowup in the framework's two-fluid system (baryon NSE + pressureless dust
interacting via the shared Newtonian potential)? Concrete items and gaps:

**Transferable (high confidence, mechanism-level):**
1. **Oscillatory stress realization** (Prop 7.5 + cone condition Lemma 4.5 + auxiliary-
   torus separation Lemma 6.1): any divergence-free-velocity subsystem can carry the
   pulse families; the averaged-stress machinery lives entirely inside the VISIBLE
   fluid's (u·∇)u structure. Works as-is for a baryon subsystem with a smooth external
   (phantom-induced) force.
2. **Shearing-wave amplification** (Lemmas 7.1/7.4: centrifugal + axial-shear growth,
   wavelength shortening, grow-then-decay envelopes): needs only a shear background;
   the framework's galactic/disk flows provide shear, but at η ≪ 3.5 the measured cap
   applies — transfer only matters in the K-2 regime.
3. **Slender-core self-similar ansatz** (ℓ_r ≍ τ^{1/2}, ℓ_z ≍ τ^{1/2−h}, Re_θ → ∞ /
   Re_r = O(1) split): the scaling architecture is equation-agnostic to first order and
   matches the two-fluid energy budget consideration (volume ≍ τ^{3/2−h}).
4. **The residual-smoothing ladder** (5.5 → 7.5 → 9.6 → 10.1: stress-divergence
   representation, cone-realization, 4-step correction cycle with σ_{j+1} = σ_j + 1/10,
   cutoff summation, flatness-to-C^∞_c-force, energy + uniqueness close): the
   *architecture* (flat residual ⇒ smooth compact force ⇒ uniqueness argument) is
   generic for any PDE system with the same energy class; the *rungs* (wave-amplitude
   equations, auxiliary-time inversion, five radial moments, heat exterior K =
   r^{−1−2h}H_ext(τ/r²), vorticity-direction-free uniqueness) are NSE-specific and must
   be re-derived for the two-fluid system.

**Gaps (honest, no overreach):**
- The framework's two-fluid system is NOT NSE-with-a-force: the phantom is a separate
  pressureless dust with its OWN evolution (G031: J^μ conserved, isothermal/Jeans
  dynamics). The OpenAI construction amortizes ALL residual into f ∈ C^∞_c; in the
  two-fluid system the effective "force" on the baryons is −∇ψ from the dust — and in
  the K-2 regime the dust is simultaneously collapsing (D2), so ψ is NOT C^∞_c at the
  singular space-time point: the two-fluid analogue would be a construction with a
  SINGULAR (or flat-but-uncoupled) effective force, i.e. a DIFFERENT theorem from
  (C)/(D). The OpenAI machinery strictly requires the force to be smooth and compactly
  supported in space-time; a dust caustic at (0,1) violates that hypothesis.
- The stress-cone condition (2.4/2.5) constrains the BACKGROUND shear+pressure profiles:
  re-verifying it in the two-fluid background (dust contribution to −∇ψ entering the
  radial pressure balance) is a new, non-trivial profile problem (Appendix A/B/C work
  would need a two-fluid variant; the analytic-axis machinery (B.2) and the five-moment
  matching (B.8/C.3) do not carry over untouched).
- The uniqueness/energy close (Lemma 10.4/10.5) uses the NSE energy identity with the
  force as given; a two-fluid energy inequality (dust kinetic + Jeans potential +
  baryon energy) and a two-fluid uniqueness class do not exist in this record and would
  have to be PROVED, not assumed.
- Timescales: the framework's dust responds on τ_ff ≲ 10⁸ yr; the NSE blowup span in
  the OpenAI construction is one "unit" of a controllable scale — matching a K-2
  transfer to galactic timescales is a modeling choice the theorem does not constrain.

**Verdict [ZMF]:** The transfer is structurally real (same toolkit family: oscillation
stresses + shearing waves + slender self-similar cores + residual-smoothing ladders —
the very items N07's D3 named), but the K-2 two-fluid program is NOT "apply OpenAI to
ZMF": it requires (i) a two-fluid profile/stress-cone construction, (ii) a flat
effective force in the presence of dust collapse, and (iii) two-fluid energy + uniqueness
— three missing rungs, all first-principles work, none guaranteed by the OpenAI record.
If K-1 holds (the measured cap), the transfer is moot: the cap is 10+ orders below the
divergent dynamics and the two-fluid blowup cannot be driven through baryon NSE.

---

## 7. BOTTOM LINE

- **Verified facts:** public paper + public Lean repo (2,659 .lean files, toolchain
  v4.34.0-rc2, no sorries/axioms beyond the standard three in its own metadata,
  review.status self-assessed); CMI status "active"; no prize claimed; no independent
  refereeing as of 2026-09-17; parallel B&A Euler/IPM/Boussinesq result with their own
  formalization; credit lineage Córdoba–Martínez-Zoroa acknowledged everywhere (revised
  paper included).
- **OpenAI claims:** (C) and (D) — forced finite-time blowup at every ν with C^∞_c
  force, zero initial data, bounded energy; proof + formalization produced by agents,
  88 h, ~10k agents; no unforced (A)/(B) claim.
- **Community state:** high mechanical confidence, zero named expert refutation, zero
  named expert line-by-line endorsement, genuine controversy concentrated on
  provenance/practice rather than mathematics.
- **Framework consistency:** the construction is the N05 corollary's predicted exit
  made real — |Du/Dt| ≍ τ^{−(3/2+2h)} → ∞, η ≳ 1e10 at the start of the final decade,
  singularity strictly above 3.5·a₀ on the Newtonian face; the a₀/2-capped modifications
  cannot touch it; the framework's singular sector (phantom dust) is a different fluid
  and is unaffected. If the OpenAI claim survives refereeing, N05's conditional becomes
  a witnessed statement — the framework's Clay position (Newtonian-face problem, own
  singular sector in the dust) is unchanged; the transfer door D3's K-2 branch gains a
  toolkit but misses three essential rungs.

— N08 lane, 2026-09-17. Registered in N07; complements N08_openai.md (verdict card).