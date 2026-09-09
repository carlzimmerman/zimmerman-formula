# L12 — A1 "constraint-first dynamics": the DOF count and its three open checks

2026-09-08. Lane L12 of [CHARTER.md](CHARTER.md).
Script: [L12_constraint_first.py](L12_constraint_first.py) → [L12_constraint_first.out](L12_constraint_first.out).
25 checks, 12 PASS / 13 FAIL; exit 0.

The target is the one entry in `CRISPY_FRIED_CHICKEN_RECIPE.md` section 3 claimed to deliver requirement I3a
(N_grav = 2) exactly:

> **A1 — Constraint-first dynamics:** MOND as a gravitational constraint (q = −⅙ ln det γ,
> C_M = D_i[μ(y) D^i q] − source ≈ 0); generic branch gives a second-class pair + 2 tensor DOF.
> Branch-restricted; never promote to a global theorem without the open checks (foliation, matter, cosmology).

Method: the construction was set up in sympy from that sentence and the frozen ingredients alone. Nothing was
imported, executed or copied from `closure_2026/integrable_clock_construction_2026/` or any other agent's
directory. Six controls (C0–C5) guard the machinery — the determinant variation, the ADM identity
δH[N]/δπ^ij = −2N K_ij, flat-space curvature in two coordinate systems, the Newtonian limit, the DOF counting
rule returning 2 for ADM GR, and the Painlevé–Gullstrand slice satisfying the vacuum Hamiltonian constraint.
All six pass, so a failure below is A1's, not the toolkit's.

One convention had to be fixed because A1 does not fix it: q = −⅙ ln det γ is **dimensionless**, so the kernel
argument must be y = c²|Dq|/a₀. Control C4 verifies this is the right choice — γ_ij = (1 − 2Φ/c²)δ_ij gives
q = Φ/c² exactly at O(Φ), so c²|Dq| = |∇Φ| = g.

---

## 1. The count is right. That part of A1 checks out.

C_M contains no gravitational momentum, so the only non-weakly-vanishing brackets sit in its row of the
constraint matrix: `B = {C_M, H_⊥}` and `A_i = {C_M, H_i}`. A 5×5 antisymmetric matrix with one nonzero
row/column has **rank 2**, i.e. exactly one second-class pair and three surviving first-class combinations:

    (2N − n_2nd − 2 n_1st)/2 = (12 − 2 − 6)/2 = 2          [control: the same rule gives 2 for ADM GR]

And the removed mode really is the conformal one. Every variation of C_M carrying **two** derivatives flows
through δq = −⅙ γ^kl δγ_kl, which is pure trace. Checked explicitly on γ = diag(e^{2A}, e^{2B}, e^{2C}) with
A, B, C functions of x: the coefficients of a″, b″ and c″ in δC_M come out identically equal (difference
exactly 0 symbolically; common value −0.187556 on the test background with the frozen kernel). So the survivors
are the two tensor polarisations.

**Degree-of-freedom count: 2, as claimed — on the generic branch.** That is a genuine confirmation, and it is
the reason the rest of this file matters: the count is not where A1 fails.

Two structural facts about the algebra that A1's sentence does not mention:

- **`{C_M, H_⊥}` is exactly proportional to K_ij** (from control C1, δH[N]/δπ^ij = −2N K_ij, and δC_M/δπ = 0).
  On time-symmetric vacuum data it vanishes *identically*, for every smearing and every lapse. The
  second-class pair does not exist there. With matter the bracket also picks up the flow of the source itself,
  so the precise statement is: the gravitational part is exactly ∝ K_ij.
- **`{C_M, H_i}` does not close.** q is the log of a density, and
  `δ_ξ q = ξ^k ∂_k q − ⅓ ∂_k ξ^k` (computed, matches the predicted anomaly exactly). C_M is therefore second
  class with one combination of the *momentum* constraints too — the count still lands on 2, but the surviving
  three first-class generators are a mixture, not the spatial diffeomorphism group.
- **C_M cannot be the Hamiltonian constraint.** δC_M/δπ^ij = 0 means it generates zero evolution of γ_ij. It
  can only be imposed *in addition* to H_⊥ — unless the unspecified source carries π (see §4).

---

## 2. OPEN CHECK 1 — FOLIATION: **FAIL**, and this is the one that decides it

Four independent tests, all on vacuum configurations where the answer is unambiguous.

**F2 — C_M is not even spatially covariant.** Empty flat space:

| coordinates | det γ | q | C_M = D_i[μ D^i q] |
|---|---|---|---|
| Cartesian | 1 | 0 | **0** |
| spherical | r⁴ sin²θ | −⅙ ln(r⁴sin²θ) | **−1/(3r²)** |

With S = 4πGρ/c², the second line demands a fictitious **ρ = −1.6×10³ kg/m³ at 1 AU** (denser than granite)
and −3.8×10⁻¹⁶ kg/m³ at 10 kpc (~10⁵× a galaxy's mean baryon density) — in *empty* space. And the artefact is
not a deep-MOND curiosity: c²|Dq|/a₀ = 4.3×10¹⁵ at 1 AU, and y = 1 is only reached at r = 6.4×10²⁶ m ≈ 20.7 Gpc,
so the spurious source sits in the μ = 1 (Newtonian) regime everywhere in the observable universe. Both footings
give the identical number because μ = 1 in both.

**F3 — the standard repair does not make q unique.** Take q = −⅙ ln(det γ / det γ̄) with a fiducial flat γ̄ (the
BSSN conformal factor). q is then a true scalar and F2's anomaly is gone. But nothing in A1 fixes γ̄, and the
answer depends on it. One slice of Schwarzschild, two admissible flat fiducials:

    areal      : q = ⅙ ln(1 − 2M/r) = −M/(3r) + O(M²)   →   c²|Dq| = g_Newton / 3
    isotropic  : q = −2 ln(1 + M/2r̄) = −M/r̄ + O(M²)     →   c²|Dq| = g_Newton

A **factor 3** in the predicted MOND acceleration — equivalently a factor 9 in a₀ — decided by an unfixed
background structure.

**F1 — the MOND field is a property of the cut, not of the spacetime.** Vacuum Schwarzschild, two slicings:

    static slicing (isotropic fiducial) :  c^2|Dq| = g_Newton
    Painleve-Gullstrand slicing         :  gamma_ij is EXACTLY FLAT, so q = 0 and c^2|Dq| = 0

Same spacetime, same mass, no matter. PG is a legitimate global slicing of the Schwarzschild geometry (control
C5 confirms it satisfies R + K² − K_ijK^ij = 0 exactly), and on it A1's MOND field is identically zero. There
is no gauge-invariant content in q at all.

**F4 — what fixes the foliation, and how weakly.** Preservation dC_M/dt ≈ 0 turns into an elliptic equation for
the lapse with principal part ⅓ D_i[μ K D^i N]. The lapse is *determined*, which is the preferred foliation, and
the equation is elliptic, so N responds instantaneously across the slice. Its coefficient is μK, and K = −3H
cosmologically:

    Solar System, 1 AU   |K|/omega = 3.3e-11
    galaxy, 10 kpc       |K|/omega = 1.0e-02
    cluster, 1 Mpc       |K|/omega = 2.0e-01

The second-class pairing that buys the 2-DOF count is nearly degenerate precisely in the regimes the theory has
to work in. This is warning P7's pattern reached from the constraint side.

**Verdict: a preferred foliation is not merely smuggled in — it is the entire content.** Once the slicing is
fixed, q is a khronon written as a conformal factor, which is what I3a exists to prevent.

---

## 3. OPEN CHECK 2 — MATTER: **FAIL** (but not where the recipe's warnings point)

Matter conservation itself is fine (**M3, PASS**): ∇_μ T^μν = 0 follows from the diffeomorphism invariance of
S_m[g, ψ] alone and is untouched by anything in the gravity sector. The break is **compatibility**.

*Scope of that PASS, so it is not read as contradicting the historical record.* It is a statement about the
matter sector only. In the supplement branch the gravity side carries S_GR + ∫λ C_M, whose multiplier term is
not diffeomorphism covariant (check Q4), so ∇_μT^μν = 0 does not propagate into a consistent gravitational
field equation — it becomes an integrability condition on λ and the geometry, which is the same
over-determination M1 exhibits seen from the Ward-identity side. In the other branch, where H_⊥ is deleted, it
is the *effective source* that fails to be conserved — which is what the 2026-08-27 MMG withdrawal reports at
Newtonian order. Both records are consistent; they are statements about different objects.

Control C4 established that in the static weak field the ADM Hamiltonian constraint *already* fixes q:

    H_perp = 0 :  lap q                = 4 pi G rho / c^2
    C_M    = 0 :  div[ mu(y) grad q ]  = 4 pi G rho / c^2

Both are imposed (that is what a second-class pair means). Subtracting, `div[e^{−y} grad q] = 0` with
e^{−y} > 0 strictly. In spherical symmetry this integrates exactly to e^{−y} g r² = C, and since
max_g [g e^{−g/a₀}] = a₀/e (3.44×10⁻¹¹ canonical, 4.15×10⁻¹¹ alt), no nonzero C can be maintained as r → 0 near
a mass. Hence C = 0 and **g ≡ 0 everywhere**: the coupled system has no solution with a gravitational field at
all. Equivalently, ∫ e^{−y}|∇q|² = 0 with q → 0 at infinity.

Numerically, for 10¹⁰ M_⊙ at 10 kpc the two constraints demand accelerations differing by a factor **2.87**
(canonical) / **3.12** (alt).

The source S is not specified by A1 (**M2, FAIL as missing input**). If it is 4πGρ/c², the above applies. If it
carries extrinsic-curvature terms, then C_M *replaces* H_⊥ — warning P3 — and M1 evaporates, but F1 has already
decided that branch, and the Hojman–Kuchař–Teitelboim uniqueness theorem (1976) says the same thing from the
algebra: a μ(y)-deformed H_⊥ cannot close the hypersurface-deformation algebra with the standard H_i, so
foliation invariance is lost there too. (HKT is cited as a cross-check, not as a load-bearing claim of this
lane; the load-bearing claims here are the computed ones.)

This programme's own record reached the same wall empirically: the MMG constraint-first chassis was withdrawn
on 2026-08-27 for γ_PPN = 0, α₁ = +4, α₃ = −1 and Newtonian-order matter non-conservation, with the note that
*deleting the Hamiltonian constraint is simultaneously what buys the 2-DOF count and what kills lensing and
conservation* (`RETRACTIONS.md`). That record also flagged the "6 first-class" hypothesis in its 20-12-4 count
as **unverified pending {D²q, H_i} closure**. Check Q4 above settles that bracket: it does **not** close; the
anomaly is exactly −⅓ ∂_k ξ^k.

---

## 4. OPEN CHECK 3 — COSMOLOGY: **FAIL**, and it forces rather than trivialises

On FLRW, γ_ij = a(t)²δ_ij gives q = −ln a, which is **spatially constant**, so D_i q = 0, y = 0 and
μ(0) = 1 − e⁰ = 0. The whole operator vanishes and

    C_M = 0 - S = 0    =>    S = 0    =>    rho = 0

The constraint is not harmlessly trivial on a homogeneous background: **it forces an empty universe.** a₀ does
not appear in this statement, so it holds identically on both footings.

Perturbations are worse, and for the same reason. Because μ(y) ≈ y for small y, D_i[μ D^i q] is *quadratic* in
Dq — a degenerate (3-Laplacian-type) operator whose linearisation about any background with |Dq| = 0 vanishes.
Symbolically the O(ε¹) coefficient is exactly 0; numerically, for a single mode at k = 1/(10 kpc),
d log|C_M| / d log ε = **2.0000**. So at linear order the constraint contains no metric perturbation at all and
reduces to δρ = 0 — no linear structure growth, and the conformal mode that §1 showed C_M removes is *not*
removed on exactly the backgrounds cosmology uses.

---

## 5. The two phenomenology gates: both PASS

- **P1.** With q = Φ/c² and S = 4πGρ/c², C_M = 0 is exactly `div[μ(|∇Φ|/a₀)∇Φ] = 4πGρ` — Milgrom's equation
  with the frozen kernel μ = 1 − e^{−y}, not a substitute. Solving the full kernel numerically, v →(GMa₀)^¼ to
  <0.05% by 1000 kpc: v_flat = 105.58 km/s (canonical) / 110.62 km/s (alt) for 10¹⁰ M_⊙, i.e. BTFR
  M_b = A v⁴ with A = 80.5 / 66.8 M_⊙(km/s)⁻⁴. **Conditional**: this holds only in the conformally-flat spatial
  gauge — F3's areal fiducial would move a₀ by a factor 9.
- **P2 (I4).** Screening is by the local acceleration, not a potential or an environment label. At Saturn
  y = 6.9×10⁵ (canonical) / 5.7×10⁵ (alt) and 1 − μ = e^{−y} < 10⁻³⁰⁰, while the ambient galactic field
  (y ≈ 2.1 / 1.8) never enters because y is built from the total local |Dq|, which the Sun dominates by
  3.2×10⁵ at Saturn. I4 is satisfied exactly as intended.
- **P3 (I5).** 1 − μ = e^{−y} is entire in y; no 1/y is used anywhere.

These three passes are worth keeping. They are properties of the *kernel placed in an elliptic constraint*, and
they survive independently of how q is built.

---

## 6. What is not determined by what is published

Stated precisely rather than guessed:

1. **The source S.** 4πGρ/c² alone, or with extrinsic-curvature terms? This decides whether C_M supplements
   H_⊥ (over-determined, M1; empty FLRW, K1) or replaces it (P3 territory, closed by F1/HKT instead).
2. **The fiducial density.** Without one, C_M is not coordinate-covariant (F2). With one, its value depends on
   which one (F3).
3. **The slicing condition.** q is a slice quantity (F1); A1 needs one, and supplying one supplies a khronon.
4. **The action.** A1 gives a constraint, not a Lagrangian. Without it there is no lensing calculation (Φ vs Ψ),
   no PPN, and no multiplier structure — gates G6/G7 cannot even be posed from A1's sentence. This lane claims
   nothing about them in either direction. (The historical MMG record reports γ_PPN = 0 and α₁ = +4 for *its*
   realisation; that is not re-derived here and is not assumed here.)

---

## 7. Verdict

**A1's arithmetic is correct and its phenomenology gates pass; all three open checks fail, and they fail for a
single reason.** q = −⅙ ln det γ is a property of the slice and of the spatial coordinates, not of the
spacetime: the same vacuum Schwarzschild geometry yields g_Newton, g_Newton/3, or exactly zero depending on the
fiducial and the slicing, and empty flat space in spherical coordinates demands 1.6×10³ kg/m³ of fictitious
matter at 1 AU. The recipe's own hedge — *branch-restricted; never promote to a global theorem without the open
checks* — is vindicated in the strongest available way: the "generic branch" (K ≠ 0, |Dq| ≠ 0) is precisely the
complement of the regimes the theory must work in, namely quasi-static galaxies (|K|/ω ≈ 10⁻²), the Solar System
(3×10⁻¹¹), and homogeneous cosmology (|Dq| = 0 identically).

**Status: KILL for A1 as written** — as a route to N_grav = 2 without a preferred foliation. What survives and
should be carried forward is narrower and real: (a) an elliptic constraint whose principal part acts on the
conformal mode does leave exactly the two tensor polarisations, and that is now verified rather than asserted;
(b) the exponential kernel inside such a constraint screens the Solar System by a local acceleration with no
1/y, satisfying I4 and I5 exactly. What A1 does not establish is that such a constraint can be built out of
det γ. Any successor needs a scalar, foliation-independent quantity to put in q's place — and no such object was
found in this lane, which is a construction obligation, not a closed door.
