# L31 — the foliation no-go: a theorem under one named assumption, and the exact place it breaks

2026-09-08. Lane L31 of [CHARTER.md](CHARTER.md).
Script: [L31_foliation_nogo.py](L31_foliation_nogo.py) → [L31_foliation_nogo.out](L31_foliation_nogo.out).
**53 checks, 53 PASS / 0 FAIL, exit 0.**

Method: nothing under `closure_2026/integrable_clock_construction_2026/` was imported, executed or copied.
The curvature machinery (Christoffels → Riemann → Kretschmann) was built from scratch in sympy in this file
and checked against exact Schwarzschild before anything rested on it. Eight controls guard it, four of them
mode-count controls that reproduce the published numbers for GR, GR+scalar, khronometric and Einstein-aether.

---

## The verdict, first

**(b) — a proof under an additional assumption I had to add, and the assumption is LOCALITY.**

Not (a). Not a proof of the conjecture as stated. The conjecture as handed to this lane has exactly one
escape, temporal nonlocality, and this lane does not close it. No counterexample was found among seventeen
known theories, but the one theory that challenges the conjecture — the nonlocal Deffayet–Esposito-Farèse–
Woodard class — sits precisely on a contested degree-of-freedom count, and I am not settling that question
here.

> **THEOREM.** Let a theory satisfy
> **(i)** MOND phenomenology in the static weak field;
> **(ii)** a single physical metric to which matter couples minimally;
> **(iii)** exactly two propagating gravitational degrees of freedom; and
> **(iv)** LOCALITY — the field equations are differential equations of finite order.
> Then the theory contains a distinguished timelike direction `u`: **a preferred frame.**
>
> **COROLLARY.** Add **(v)** — the MOND equation is posed as an elliptic boundary-value problem on
> 3-surfaces, which is how Milgrom's equation is posed (`div[μ ∇Φ] = 4πGρ` with `Φ → 0` at infinity).
> Then `u^⊥` must be integrable, so by Frobenius `u` is hypersurface-orthogonal and the theory has a
> **preferred foliation**; (iii) then forbids `u` from propagating, so the foliation is non-dynamical and
> the MOND field responds **instantaneously** on its leaves.

The one-sentence physical content, which is what makes this worth writing down:

> **MOND makes the acceleration a locally measurable quantity. The equivalence principle says acceleration
> is not locally measurable. The only way to make it measurable is to declare a rest frame — and once two
> gravitational modes are demanded, that frame cannot itself propagate, so it degenerates into a
> non-dynamical foliation with an instantaneous constraint.**

---

## STEP E — the equivalence-principle lemma, proved against an adversarial control

The obvious argument — *"curvature is second derivatives of Φ, a potential is not"* — **is wrong as stated**,
and the lane starts by demonstrating that so the real lemma is not confused with it. In geometric units the
combination

    G_loc ≡ (√3/2) · K^{3/2} / |∇K|,        K = Kretschmann

is the unique dimensionally admissible acceleration built from `K` and its first gradient, it is a fully
covariant **local** scalar, and on exact Schwarzschild it evaluates (symbolically, C6) to

    G_loc = (m/r²) · (1 − 2m/r)^{−1/2}   →   m/r²   exactly in the weak field.

So on a one-parameter solution family a local invariant *does* reproduce the Newtonian acceleration. The
lemma therefore has to be proved by breaking `G_loc`, not by dimensional analysis. It breaks five ways:

| test | result |
|---|---|
| point mass (control) | **exact**, max relative error 3.6e-15 |
| Plummer sphere, r = 0.2 b | `G_loc/|∇Φ| = 10.99` (→ 1.0017 only at r = 20 b) |
| equal-mass binary | worst error **87%**; at the centre the ratio diverges (`∇K → 0`) |
| Miyamoto–Nagai disc, R = a | `G_loc/|∇Φ| = 9.00`; still 1.85 at R = 30 |
| pure uniform field | **0/0** — `K ≡ 0` and `∇K ≡ 0` |

And the sharp form, proved symbolically (E1): adding a uniform field `Φ → Φ + g·x` leaves the **entire**
Hessian `∂_i∂_jΦ` unchanged, hence every curvature tensor, every invariant, and every local functional of
the metric. A uniform field is flat spacetime in disguise. But MOND's `y = |∇Φ|/a₀` **does** change — and
that change is not a technicality, it *is* the external field effect, one of MOND's defining and
most-tested signatures:

    [canonical] a star at 1 pc alone: y = 0.0015  ;  with the Galaxy's g_ext: y = 2.2153   (1488x)
    [alt      ] a star at 1 pc alone: y = 0.0012  ;  with the Galaxy's g_ext: y = 1.8388   (1488x)

**LEMMA 1: `y` is not a diff-invariant local scalar of the metric.**

The physical version, with real Galaxy numbers (E6), is the one worth carrying:

    smooth Galaxy tidal field at R_sun                   |d^2 Phi| = 8.19e-31 s^-2
    the Sun's own tidal field at 1 pc                    |d^2 Phi| = 9.03e-30 s^-2   (11x the Galaxy's)
    distance where a star's curvature = the Galaxy's         d_eq = 2.23 pc
    fraction of solar-neighbourhood volume within d_eq             99.0%
    true galactic y = 2.21 (canon) / 1.84 (alt)   vs   y from local curvature = 1.5e-3 / 1.2e-3

Local curvature in a galaxy is set by the **nearest star**, not by the galaxy. MOND's `y` is the coherent,
coarse-grained field. Over 99% of the solar neighbourhood's volume these differ by a factor ~1500.

---

## STEP Q — the polarization proposition

Lemma 1 forces an extra structure σ carrying `a₀`. Requirement (iii) forbids it from propagating. Can a
field whose gradient enters the action non-trivially fail to propagate, without a preferred timelike
direction?

**Q1 (symbolic).** For `L = L(X)` with `X = g^{μν}∂_μφ∂_νφ`, the kinetic Hessian is exactly

    d^2 L / d(phidot)^2  =  2 L_X g^00  +  4 L_XX (g^{0n} d_n phi)^2

At a static configuration this is `2 L_X g⁰⁰`, and `g⁰⁰ ≠ 0` for any timelike observer, so requiring it to
vanish forces `L_X ≡ 0` — no gradient dependence at all, hence no MOND.

**Q2 (linear algebra, done as an actual solve).** A symmetric `S^{μν}` with `S^{μν}u_μu_ν = 0` for **every**
timelike `u` is identically zero: sampling 60 timelike `u` gives a rank-10 linear system on the 10
components (smallest singular value 2.04), so the solution is unique and is `S = 0`. For a **single**
distinguished `u` the solution space is 9-dimensional — exactly the room needed for the spatial projector.

**Q3.** `h^{μν} = g^{μν} + u^μu^ν` annihilates `u`, is positive semi-definite of rank 3 (eigenvalues
0, 1, 1, 1), and `h^{μν}∂_μφ∂_νφ = |∇φ|²`. **MOND's `y` is exactly a projector contraction.**

**PROPOSITION: a non-propagating MOND scalar requires a distinguished timelike `u`.**

---

## STEP T — the trichotomy, and whether it is exhaustive

The classifier is the principal symbol `S^{μν}k_μk_ν` of σ's own field equation.

| route | principal symbol | N_grav | preferred slicing | verdict |
|---|---|---|---|---|
| **R1** extra field, Lorentz-invariant kinetic term (RAQUAL, TeVeS/AeST scalar) | `a g^{μν}k_μk_ν`, hyperbolic | 3 | no | violates (iii); the DC-013 horn |
| **R2** extra field, degenerate kinetic term (A1, L12) | `h^{μν}k_μk_ν`, degenerate along `u` | 2 | **YES** | Q2 forces `u`; the DC-019 horn |
| **R3** modify the Hamiltonian constraint (A1/MMG/Hořava) | deformed `H_⊥` (a functional of γ, K) | 2 | **YES** | `H_⊥` generates the slicing; L12 measured it |
| **R4** nonlocal `□^{-1}` (DEFW) | none — not a finite-order PDE | contested | no | **THE ESCAPE** |
| **R5** higher-derivative local (f(R), Horndeski, DHOST) | `(g^{μν}k_μk_ν)^p`, hyperbolic | ≥3 | no | degeneracy removes the **ghost**, not the **mode** |
| **R6** matter-built scalar | algebraic | 2 | no | fails in vacuum |

Two supporting numbers. **T1**: a symmetric 2-tensor built from `g` alone is `a·g^{μν}` — and in **vacuum**,
where MOND must work, `R_μν = 0` kills every curvature correction to the symbol, so the symbol is hyperbolic
there with no escape. **T4b**: an exponential disc with `R_d = 3` kpc has `Σ(20 kpc)/Σ(0) = 1.3e-3`, and
lensing is measured entirely in vacuum, so a matter-built scalar has nothing to build from exactly where the
rotation curve is flat.

**Exhaustiveness (T6):** a symmetric form on a Lorentzian manifold is hyperbolic, degenerate, or absent.
There is no fourth case — *for finite-order field equations*. That qualifier is hypothesis (iv), and it is
the whole of what this lane could not remove.

---

## STEP K — the control table. Every known relativistic MOND theory.

A row with (i) + (ii) + (iii) and no preferred frame refutes the conjecture. **There is none.**

| theory | (i) MOND | (ii) one metric | (iii) N=2 | preferred frame / foliation | N_grav |
|---|---|---|---|---|---|
| GR *(control)* | no | yes | yes | none | 2 |
| RAQUAL (Bekenstein–Milgrom 1984) | yes | yes | **no** | **NONE** (Lorentz invariant) | 3 = 2 + scalar |
| Phase-Coupling Gravity (Bekenstein 1988) | yes | yes | **no** | none | ≥3 |
| TeVeS (Bekenstein 2004) | yes | yes | no | **YES** unit timelike vector `A^μ` | ≥4 |
| GEA (Zlosnik–Ferreira–Starkman 2007) | yes | yes | no | **YES** unit timelike aether | 5 |
| AeST (Skordis–Zlosnik 2021) | yes | yes | no | **YES** unit timelike aether | ≥5 |
| Khronometric MOND (repo FC-KH) | yes | yes | no | **YES** khronon = exact foliation | 3 |
| Hořava-type / projectable | yes | yes | no | **YES** foliation | ≥3 |
| BIMOND (Milgrom 2009) | yes | **no** | no | none required | ≥4 |
| MOG / STVG (Moffat) | no* | yes | no | vector with nonzero background | ≥5 |
| f(R), Horndeski, DHOST, Galileon | no | yes | no | none | 3 |
| dRGT / Hassan–Rosen bigravity | no | no | no | none | 5 or 7 |
| Modified inertia (repo MI arm) | yes | yes | no | **YES** passive frame `u` in `K(□_u)` | — |
| **Nonlocal metric MOND (DEFW 2011)** | **yes** | **yes** | **?** | **NONE** (Lorentz invariant) | **contested: 2 nonlocal / ≥4 localised** |
| Lead's IC5–IC7 (L4) | yes | yes | no | **YES** khronon inside the metric sector | 3 |
| Lead's IC8–IC10 (L8) | yes | yes | no | **YES** the clock field `T` | N_grav 2 + N_clock 1 |
| A1 constraint-first, `q = −⅙ ln det γ` (L12) | yes | yes | **yes** | **YES** — the slicing *is* the content | 2 |

\* MOG is MOND-*like*, not MOND: a running `G` and a Yukawa vector, no universal `a₀` interpolation.
No-MOND rows for the Galileon/bigravity families rest on the repository's DC-018 flux-scaling theorem
(spherical Galileon flux gives `r^{1−3/n}`; MOND needs the non-integer `n = 3/2`), cited not re-derived here.

**The pattern is an exclusive OR: Lorentz invariance XOR two modes.** Every frame-free MOND theory pays in
propagating modes (RAQUAL 3, PCG ≥3, DEFW ≥4 localised); every two-mode MOND theory pays in a foliation
(A1, khronometric). No row has both. That is the conjecture's empirical content, and it is why L4/L8's
clock, L12's `det γ`, and the khronometric route are the same object wearing three different hats.

---

## STEP N — the escape, and one obstruction of my own that FAILED

Lemma 1 is a statement about **local** functionals. `□^{-1}` reaches out to the source, which is precisely
what a potential requires, so a nonlocal scalar is **not** uniform-field blind. Quantified (N2): holding
`g_ext = 2.07e-10 m/s²` fixed while pushing the source from 8.2 kpc to 8200 kpc drops the local tidal
invariant by **1000×** (1.64e-30 → 1.64e-33 s⁻²) while `|∇(□^{-1}R)| = 2 g_ext` stays exactly constant.
The escape is real and it is not a technicality.

**My own candidate obstruction, tested and reported as FAILING.** The covariant scalar available to a
Lorentz-invariant construction is `X = g^{μν}∂_μΨ∂_νΨ = |∇Ψ|² − (∂_tΨ)²/c²`, which is sign-indefinite,
while MOND's `y = √X/a₀` needs `X > 0`. If the sign flipped inside real systems the escape would close. **It
does not:** `X > 0` for the Solar System, the Milky Way, galaxy outskirts, a 1 Mpc cluster and a 100 Mpc
supercluster; the flip is at `r ≈ c/H₀ = 4448 Mpc`. **This objection is withdrawn, not banked.**

**What the escape actually turns on.** Localising `S = (1/16πG)∫√−g R[1 + f(□^{-1}R)]` with `ξ = □^{-1}R`
enforced by a multiplier `ψ` gives the cross-term `ψ(□ξ − R)`, whose kinetic matrix in `(ξ, ψ)` is
off-diagonal with eigenvalues **±½** (computed here independently; it reproduces the repository's own C2
number). So:

- **localised reading:** `N_grav = (16 − 8)/2 = 4` — one healthy mode plus one ghost. DEFW is **not** a
  counterexample; it violates (iii), and the conjecture stands.
- **nonlocal reading** (retarded Green function, auxiliary fixed by matter history, no free initial data):
  `N_grav = 2`. DEFW **is** a counterexample and the conjecture is **false as stated**.

The two readings disagree and **this lane does not settle which is right.** The repository's own C2 file
already marks the retarded prescription "a known, contested cost."

---

## Where the argument breaks, stated precisely — this is the deliverable either way

1. **Hypothesis (iv), locality, is load-bearing and I could not remove it.** The single calculation that
   would turn this into (a) a theorem or into a refutation is a definitive Hamiltonian degree-of-freedom
   count for a retarded-nonlocal gravitational theory: *does the retarded prescription genuinely remove the
   localised auxiliary pair's initial data, or does it merely hide it?* Everything else in the chain is
   proved.
2. **Q1 is proved for `L = L(X)`.** The general `L(φ, ∂φ, g)` case is handled only at the level of the
   linearised principal symbol (Q2). That is enough for the mode count, but it is a linearised statement
   and is labelled as one.
3. **The strict conclusion of the theorem is a preferred FRAME, not a foliation.** A non-dynamical
   background `u` need not be hypersurface-orthogonal. Assumption (v) — the elliptic-boundary-value-problem
   form of Milgrom's equation — is what upgrades frame to foliation via Frobenius. It is how MOND is
   actually posed, but it is an assumption and it is named as one.
4. **This lane proves nothing about viability.** It says such a theory *must* have a preferred foliation
   with an instantaneous constraint; it does not re-derive the price. The repository's DC-019 puts that
   price at `α₃ = O(1)` against the pulsar bound `|α₃| < 4e-20`, i.e. ~2.5e19× over — **cited, not
   re-derived here.**
5. **Not claimed:** that the conjecture is original. The strong-equivalence-principle tension in MOND is
   old folklore; what is new here is the chain from it to the *mode count*, and the identification of
   temporal nonlocality as the unique escape.

---

## What this lane adds to the programme's standing record

The single-metric pincer (DC-013 slip-lock + DC-019 `α₃ = O(1)`) asserted its two horns are exhaustive.
This lane supplies the reason from the kinematics rather than from PPN: the horns are *propagating* versus
*instantaneous*, which is exactly *hyperbolic* versus *degenerate* principal symbol, and STEP T shows those
are the only two options for a symmetric form once Lemma 1 has forced an extra structure. The pincer's
exhaustiveness claim is therefore now backed by an argument and not only by case enumeration — **under
locality**, with the nonlocal door left explicitly ajar and its hinge named.

Nothing in the lead's IC-series is contradicted. The IC8–IC10 result that L8 verified — metric sector
exactly Einstein, `N_grav = 2`, one separately-counted healthy clock — is, on this reading, not a near-miss
on requirement 2 but **the generic outcome the theorem predicts**: the clock is the preferred foliation,
counted honestly and made healthy. If the theorem is right, that third mode is not removable by a better
construction inside the local single-metric class; the only place left to look is nonlocality.
