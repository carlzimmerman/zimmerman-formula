# L27 — is there a scalar, foliation-independent replacement for `q = −(1/6) ln det γ`?

2026-09-08. Lane L27 of [CHARTER.md](CHARTER.md), the constructive lane opened by L12's closing sentence.
Script: [L27_foliation_scalar.py](L27_foliation_scalar.py) → [L27_foliation_scalar.out](L27_foliation_scalar.out).
40 checks, 19 PASS / 21 FAIL; exit 0.

**The answer is no, and the failure is a theorem rather than an obstacle.**

---

## 0. What was inherited, and what was asked

[L12](L12_CONSTRAINT_FIRST.md) tested recipe item A1 and found its arithmetic right: `C_M = D_i[μ(y) D^i q] − S ≈ 0`
is momentum-free, removes exactly the conformal mode, leaves **exactly two tensor degrees of freedom**, and its
static weak-field limit is Milgrom's equation with the frozen kernel `μ = 1 − e^{−y}`, screening the Solar System
by a local acceleration and recovering Newton exponentially. It died on one thing: `q = −(1/6) ln det γ` is a
property of the slice. L12's obligation was to find something else to put in q's place.

The acceptance test used here, stated before the search:

| | requirement |
|---|---|
| (a) | a genuine spatial scalar — no anomaly |
| (b) | its value on a given spacetime does not depend on the slicing |
| (c) | reduces to the Newtonian potential in the static weak field, **for a general source** — i.e. it superposes |
| (d) | vanishes in genuinely empty flat space in every coordinate system |
| (e) | the constraint stays momentum-free, so the count stays at 2 |
| (f) | does not force ρ = 0 on FLRW, and does not over-determine GR's own Hamiltonian constraint |

Requirement (b) was applied first, and applied harder than L12 applied it. **L12 used two slicings; two is not
enough.** The test here is a one-parameter family of cuts of the *same* vacuum Schwarzschild spacetime,

    ds² = −f dT² + 2λ√u dT dr + [(1 − λ²u)/f] dr² + r² dΩ²,   f = 1 − 2M/r,  u = 2M/r,

with λ = 0 the static slicing, λ = 1 Painlevé–Gullstrand (γ exactly flat, N = 1), and λ = 1/2 a legitimate third
cut. Control C1 verifies all three are one spacetime (R_μν = 0, Kretschmann = 48M²/r⁶ on each); the areal radius r
labels the same 2-sphere on every cut, so comparing at fixed r compares the same geometry. **The third cut earns
its keep immediately: R3 vanishes on the static *and* the PG slice by coincidence and would have passed a
two-slicing test.**

Eight controls guard the toolkit — flat-space R3 = 0 in two charts, the family's Ricci-flatness, the family's
genuine distinctness, L12's PG kill reproduced, L12's fictitious-density anomaly reproduced (−1.596×10³ kg/m³ at
1 AU), the linearised Ricci scalar validated against the full nonlinear one and against gauge invariance, the
vacuum ADM Hamiltonian constraint satisfied on every cut, and the curvature-ratio construction verified exact for
a point mass. All eight pass, so a failure below is the candidate's.

---

## 1. The table of candidates, and how each died

| candidate | dies on | how |
|---|---|---|
| `q_det = −(1/6) ln(det γ/det γ̄)` | **(b)** | slice-dependent: g_N/3 (areal fiducial) / g_N/4 / **0** across the three cuts; g_N with the isotropic fiducial |
| `R3`, spatial Ricci scalar | **(b)** | 0 on static **and** PG by coincidence; −6M²/(r²(M−2r)²) on the third cut |
| `K`, the York time | **(b)** | 0 on static, (3/2)√(2M/r³) on PG |
| `K_ij K^ij` | **(b)** | 0 on static, 9M/(2r³) on PG |
| `A_ij A^ij`, trace-free part | **(b)** | 0 on static, 3M/r³ on PG |
| `ln N`, the ADM lapse | **(b)** | the khronometric choice; N *is* the slicing, and it is 0 on PG |
| `c²|D ln N|`, normal-observer acceleration | **(b)** | g_N on static, exactly 0 on PG — free-fallers feel nothing |
| `R4`, spacetime Ricci scalar | (c) | survives (b); = 0 in **all** vacuum, so no field outside the baryons |
| `I1 = R_abcd R^abcd` (Kretschmann) | (c) | survives (b) at 48M²/r⁶; tidal, and the only combination with the right fall-off scales as M^(1/3)/r |
| `I2 = ∇_e R_abcd ∇^e R^abcd` | (c) | survives (b) at 720M²(r−2M)/r⁹; same tidal disease |
| `E_ij E^ij`, electric Weyl | (c) | survives (b) at 6M²/r⁶ **non-trivially** (the normal observer is static at λ=0 and free-falling at λ=1; type-D E_ij is radial-boost invariant); tidal, and 0 inside uniform density |
| `T = T^μ_μ`, matter scalar | (c) | survives (b) vacuously; = 0 in vacuum |
| `q_ratio = −(720/48^{3/2})√(I1³)/I2` | (c), (d) | survives (b) and equals **−M/(r−2M) → Φ_N/c² exactly**; does not superpose; 0/0 in flat space |
| `ln √(−ξ·ξ)`, Killing norm | (e), (f) | survives **(a), (b), (c), (d)**; no timelike ξ on FLRW or any evolving system; not a functional of (γ, π), so removes no mode |

**7 of 14 die on requirement (b) alone.** The 7 that survive (b) die on (c) or (d). One reaches (e).

### The two candidates that deserved a real fight

**`q_ratio`, the honest strong case for "yes".** A dimensionless local curvature scalar *can* be built that
reproduces the Newtonian potential, contrary to the naive dimensional argument, because a ratio of invariants
supplies its own length. Exactly, on Schwarzschild:

    -(720/48^{3/2}) sqrt(I1^3)/I2  =  -M/(r - 2M)  ->  -M/r  =  Phi_N/c^2      [control C5, exact]

This is a genuine spacetime scalar, so (a) and (b) are automatic and were verified on all three cuts. It dies on
what (c) actually demands — a *general* source. For two equal 10¹⁰ M⊙ masses 10 kpc apart, `q_ratio/Φ` runs from
0.894 to 16.50 across the field and the predicted acceleration runs from **0.56× to 3383×** the Newtonian one,
agreeing only in the far field where the two-body system looks like the single point mass it was tuned on. And in
genuinely empty flat space I1 = I2 = 0, so the expression is **0/0 — undefined, not zero**, failing (d). Every
curvature-ratio construction has this disease, because the ratio exists only where curvature does.

**The Killing norm, the only candidate to pass (a)–(d).** `ln√(−ξ·ξ)` is *not* the ADM lapse: ξ is a property of
the spacetime, so the quantity is slicing-blind, and it was verified equal to (1/2)ln(1−2M/r) on all three cuts
with ∇_(a ξ_b) = 0 confirmed in all three coordinate systems. It equals Φ/c² at linear order, so it superposes
exactly, and it vanishes in flat space in any chart. It dies on two counts, both fatal:

- **existence.** FLRW has no timelike Killing vector — ∇_(a ξ_b) for ξ = ∂_t is a(t)ȧ(t) ≠ 0 — so the candidate is
  *undefined* on cosmology and on any evolving galaxy. The conformal Killing vector that does exist gives ln a,
  spatially constant, which is L12's cosmology failure verbatim.
- **count.** ξ is fixed by the whole spacetime, not by (γ, π) on one slice, so C_M is not a constraint on the
  gravitational phase space at all. It removes **no** mode and merely over-determines the lapse. And where ξ does
  exist, `ln√(−ξ·ξ)` **is** the static lapse — candidate b06, the khronometric choice, arriving in geometric
  clothing.

---

## 2. The structural tension is a theorem. Four of them.

The assignment asked whether the tension — foliation-independent objects are curvatures, potential-like objects are
slice properties — is a theorem or an obstacle. It is a theorem, on four independent counts.

### T1 — the derivative-count theorem

A natural scalar's part linear in h_μν must be invariant under h → h + ∂_(μ ξ_ν) (control C4 verifies this for the
linearised Ricci scalar), and the complete set of such invariants is the **linearised Riemann tensor**, which is
exactly two derivatives of h. Computed: in vacuum the linearised Ricci tensor vanishes identically, so every
Ricci-built scalar is zero there, and the one surviving piece is `R^(1)_{0i0j} = ∂_i∂_jΦ` — the tidal tensor, of
dimension 1/L². Making it dimensionless needs either an external length (giving ℓ²∇²Φ, **not** Φ) or a ratio of
invariants, which is not linear at all — and the ratio branch is `q_ratio`, killed on superposition and on 0/0.
**Requirement (c) asks for the zeroth-derivative object; (a)+(b) force at least the second. Nothing sits in
between. Both horns closed.**

### T4 — the slice-metric no-go

**No functional of the spatial metric alone can satisfy (b), (c) and (d) simultaneously.** Proof, on objects
computed in the script:

1. the PG slice of vacuum Schwarzschild has γ_ij **exactly flat** (control C2), i.e. isometric to a slice of Minkowski;
2. requirement (d) then forces `F[γ_PG] = F[flat] = 0` — F cannot tell the PG slice of a black hole from a slice of
   empty space, because it sees only γ;
3. requirement (b) propagates that zero to every slice of the same spacetime, so `q̃ = 0` on the static slice too;
4. requirement (c) demands `c²|Dq̃| = g_Newton ≠ 0` there. Contradiction. ∎

This kills A1's **entire structure** — a MOND constraint acting on the conformal mode of γ — not merely its choice
of `ln det γ`. L12's PG counterexample is hereby promoted from a refutation of one choice to a no-go for the class.

### T5 — the curvature pincer

A local curvature scalar splits into Ricci and Weyl parts, and the two halves fail on **opposite** sides:

- **Ricci half** (R4, R_μνR^μν, T, ρ): proportional to T_μν, hence exactly zero in vacuum — no field outside a
  galaxy's baryons, which is where the rotation curve is;
- **Weyl half** (I1, I2, E², C², and every ratio built from them): exactly zero wherever the spacetime is
  conformally flat. Verified here for FLRW (Weyl ≡ 0) and for the **interior Schwarzschild solution**, a
  uniform-density star (max|Weyl| = 4.1×10⁻¹⁴³ against max|Riemann| = 2.3×10⁻²), where |∇Φ| = (4πGρ/3)r ≠ 0.
  Newtonianly: inside any homogeneous region the traceless part of ∂_i∂_jΦ vanishes while the force does not.

**No local curvature scalar works on both sides.**

### T3 — the homogeneity theorem, and it needs no search at all

This is the sharpest result of the lane, and it is **independent of what q is**. On an exactly homogeneous slice
*every* spatial scalar is spatially constant, so D_i q̃ = 0, y = 0, and the frozen kernel gives μ(0) = 1 − e⁰ = 0:
the whole operator vanishes identically (verified symbolically, C_M = 0), leaving C_M = −S and therefore **ρ = 0**,
against ρ_m = 2.688×10⁻²⁷ kg/m³ today. a₀ does not appear, so the statement is **identical on both footings**
(9.3619×10⁻¹¹ and 1.1279×10⁻¹⁰).

**A1's cosmology failure was never about `ln det γ`. It is a property of the constraint form, and no replacement
for q can repair it.**

### f1 — and (c) fights (f) directly

L12's matter failure is inherited by *any* candidate that satisfies (c): a q̃ that reduces to Φ/c² already obeys
∇²q̃ = 4πGρ/c² by GR's own H_⊥. Imposing C_M as well leaves `div[e^{−y} ∇q̃] = 0` with e^{−y} > 0 strictly, whose
only decaying solution is q̃ = const, i.e. g ≡ 0. The two constraints demand accelerations differing by **2.87×
(canonical) / 3.12× (alt)** for 10¹⁰ M⊙ at 10 kpc. Requirement (c) and requirement (f) are in direct conflict for
any q whatsoever.

### e1 — and (b) fights (e) directly

On the PG slice R3 = 0 exactly, while K = (3/2)√(2M/r³) and K_ijK^ij = 9M/(2r³): by Gauss–Codazzi the whole of
I1 = 48M²/r⁶ there is built out of K_ij, i.e. out of the gravitational **momentum** π^ij. So on that slice every
(b)-survivor is a function of π alone, δC_M/δπ^ij ≠ 0, and **A1's rank-2 argument — the sole source of its 2-DOF
claim — no longer has its hypothesis.** A constraint on π alone is a slicing condition of the CMC/York type: the
preferred foliation arriving by the other door.

---

## 3. The two escapes, named

Both are exactly what requirement I3a exists to forbid, which is why they are reported rather than pursued:

1. **supply a preferred time direction** — a khronon, or a Killing vector where one happens to exist — and read the
   potential off the lapse. That is candidates b06/b12, and it is the khronometric theory;
2. **make q̃ nonlocal**: solve an elliptic equation for it, i.e. introduce an auxiliary potential field. That is
   AQUAL/QUMOND, whose constraint is a condition on the auxiliary field and **not** on the gravitational phase
   space, so it removes no conformal mode and A1's 2-DOF count does not apply to it at all.

And T3 stands over both: even a perfect q̃ forces ρ = 0 on FLRW.

---

## 4. Verdict

**V1 FAIL — no such replacement exists.** 7 of 14 candidates die on requirement (b) alone; the 7 that survive (b)
die on (c) or (d); the one that reaches (e) is the Killing norm, which does not exist on the backgrounds the theory
must describe and removes no gravitational mode. L12's construction obligation is not merely unmet — **it is
unmeetable in this class**.

**V2 PASS — the failure is generic.** Four independent theorems (T1 derivative count, T4 slice-metric no-go,
T5 curvature pincer, T3 homogeneity), each proved on computed geometry rather than asserted.

**Status: A1's whole class is closed, not just A1 as written.** The recipe's A1 entry should now record that its
three open checks were run and failed (L12), and that the successor L12 called for has been searched for and
proved not to exist (this lane).

What survives, unchanged from L12 and independent of q, is still worth carrying: an elliptic constraint whose
principal part acts on the conformal mode does leave exactly two tensor polarisations, and the exponential kernel
inside such a constraint screens the Solar System by a local acceleration with no 1/y. **What is now settled is
that the object the kernel acts on cannot be built out of the geometry of a slice.**

---

## 5. Scope, stated so it is not over-read

- The no-go is about **local** scalars built from the metric, curvature and matter fields at a point, plus the
  Killing-norm case. A nonlocal q̃ (escape 2) is not covered and is not claimed to be dead here — it is claimed to
  be a different theory, one to which A1's degree-of-freedom argument does not apply.
- T1's step "the linearised Riemann tensor is the complete set of linear gauge invariants" is standard linearised
  gravity, cited rather than re-proved; what is computed here is its consequence (vacuum R^(1)_μν ≡ 0, the sole
  surviving invariant being ∂_i∂_jΦ), and the gauge invariance of the linearised scalar (control C4).
- The (b) test is run on vacuum Schwarzschild with a three-member slicing family. That is enough to kill, never
  enough to certify: a candidate passing (b) here is reported as "survives (b)", never as "foliation-independent".
  Every such survivor was then killed on a later requirement anyway.
- Both a₀ footings are carried on every dimensional number. T3 and T4 are a₀-independent and hold identically on
  both.
