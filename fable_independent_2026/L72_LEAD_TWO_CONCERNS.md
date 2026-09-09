# L72 — the lead's two uncleared concerns are NOT kills: one is an eliminated-auxiliary artefact, the other an open window

**Both concerns L66 raised against the last surviving construction and left unresolved come back cleared on
everything this lane can reach. CONCERN 1 (the indefinite auxiliary gradient Hessian, `det G = −4u²ξ² < 0`
at π = 0) is an ARTEFACT: the indefinite determinant belongs to the CLOCK's own auxiliary pair `(ξ,u) =
(ln N, u)`, which the constraint algebra `{χ_a, p_b} = −|k|²H_gg` makes second-class and eliminates
(0 propagating modes) — a negative determinant is the ordinary signature of a healthy second-class
elimination, not a gradient ghost — while the PROPAGATING scalar is the Schur complement M, positive-definite
at the witness for every wavenumber (`det M = 3(4T−27)(8T+x)/(2T) > 0`). CONCERN 2 (the "adjacent coefficient
already gives IR ω² < 0" knife-edge) is a genuine but OPEN window: health is set by a single number, the IR
scalar speed² `cIR = c₀ + κ_flow/H_SS`, whose healthy set is the open interval `H_SS ∈ (−5.30, 0)` with the
design point `H_SS = −3` sitting interior at factor ≈1.76 margin — a modest bounded design freedom, not a
tuning. Neither concern is L69's transmission-channel root, and neither is a new class-level mechanism. The
only surviving gap is the uncomputed deep-MOND propagating sector — L66-4b / L69's open item 1 — which is
L71's lane, not something these two concerns settle against the construction.**

2026-09-09. Lane L72 of [CHARTER.md](CHARTER.md), discharging the two flags recorded in
[L66_LEAD_ACTION_HEALTH.md](L66_LEAD_ACTION_HEALTH.md) (18/18) against the lead's integrable-clock action
(`integrable_clock_construction_2026/ACTION.md` door 4; `AUXILIARY_SYMBOL.md`; `IC20_JOINT_COMPLETION.md`).
Script: [L72_lead_two_concerns.py](L72_lead_two_concerns.py) → [L72_lead_two_concerns.out](L72_lead_two_concerns.out).
**23 checks, 23 PASS / 0 FAIL; exit 0; runtime 1 s.**

**Polarity.** Each check asserts a *statement* and PASS means the statement is true; several PASSes are
negative for a construction — read the statement. Both a₀ footings: 9.3619×10⁻¹¹ (canonical) /
1.1279×10⁻¹⁰ (alt) m s⁻². **Both concerns are symbol-level** (a principal symbol; a coefficient-space map),
and the a₀-dependent witness value `a₀² = 27h²e^{−1/2}/(8ℓ²)` **cancels** from both `det G` and the
dispersion ratio, so the two footings give the identical verdict — flagged at each check rather than left
implicit.

**Provenance.** Nothing under `closure_2026/` was imported or executed as this script's evidence. The IC-4
auxiliary symbol is **rebuilt** in exact SymPy from the scalar coefficients in `IC4_ACTION.md` (𝒯 = −27/16 +
(54/5)/ln(9/5), e = 1/8, d = −9e/𝒯, α = 81e/𝒯², β, γ) and the Hamiltonian structure in `AUXILIARY_SYMBOL.md`;
the lead's reference symbols (det G, G₀, det M, the three witness determinant derivatives, det M’s factored
form) were read once, offline, and hard-coded as targets the rebuild must hit — all reproduced exactly. For
CONCERN 2 the lead's `design()`/`dispersion()` — which **is** "the coefficient box the lead's own files
permit" — was run once offline as an oracle over a coefficient sweep; the resulting IR-speed ingredients
(c₀ = −0.457840, κ_flow = −2.423638, both exactly H_SS-independent) and the sweep boundary are hard-coded,
and the script INDEPENDENTLY proves the dispersion sign law, reproduces cIR from the closed form, and locates
the boundary. The Dirac counter is `fable_independent_2026`'s own machinery (2/3/5/3 controls PASS).

---

## 1. Controls (PART 0) — nothing below counts without them

| control | required | got |
|---|---|---|
| CTRL-1 ADM general relativity | 2 | **2** (4 primary + 4 secondary, all first class) |
| CTRL-2 GR + one minimally coupled scalar | 3 | **3** |
| CTRL-3 Einstein-aether (c₁…c₄ = 1/5,1/7,1/11,1/13) | 5 | **5** |
| CTRL-4 khronometric | 3 | **3** |
| C1-a1 flagged #1: `det G(π=0)` | −4u²ξ² | **−4u²ξ²** (rebuilt, matches `AUXILIARY_SYMBOL.md`) |
| C2-b design-point positivity (L66 LEAD-4a) | cIR = 0.350, speeds 0.350→0.200 | **0.350039, 0.350→0.200 all k** |
| C2-c flagged #2: adjacent H_SS = −1000 | IR ω² < 0 | **cIR = −0.4554 < 0 ⇒ IR ω² < 0** (IC20 §7) |

The rebuild also reproduces the lead's rank-one witness matrix G₀ (det = 0, null vector (−b,1), b = −𝒯/9−3/8),
its three witness determinant derivatives, and its physical-sector determinant `det M = 3(4𝒯−27)(8𝒯+x)/(2𝒯)`
— all exact in the symbol 𝒯 = 16.6865.

---

## 2. CONCERN 1 — the indefinite auxiliary gradient Hessian (PART 1)

`AUXILIARY_SYMBOL.md` gives the transverse gradient Hessian in `(∂_iξ, ∂_iu)`,
`H_gg = −D₊[[2ρA_J, ρB_J+4uξ],[ρB_J+4uξ, 2ρC_J+4ξ²]]`, normalized to
`G = [[2αλ, βλ+2uξ],[βλ+2uξ, 2γλ+2ξ²]]` with `λ = ρ/ρ₀ ∝ π²`. At **π = 0 (λ = 0)**, `det G = −4u²ξ² < 0`.

**(a) π = 0 is a locus the theory occupies — not measure-zero.** π is the trace (scale-factor) momentum,
∝ the extrinsic-curvature trace K. The expanding witness has `π₀ = −3mVe^{−1/2}h ≠ 0`; **π = 0 is a
momentarily-static slice, K = 0**, which is exactly `ACTION.md`'s static branch (K = W = 0, Q = 0, on which
`u² = 1 − e^{−|a|/a₀}` is the MOND relation). A static galaxy / the solar system has K ≈ 0 and, being weak
field, `ξ = ln N ≈ Φ/c² ≠ 0`, `u ∈ (0,1)` nonzero ⇒ `uξ ≠ 0` ⇒ **det G < 0 strictly** there. So the concern
is real at a physically central locus and **cannot be waved away as "never reached"**; it must be settled by
the constraint algebra (C1-b). *(This is the honest correction to any "π = 0 is an exact field zero the
background avoids" reading — it is not.)*

**(b) The indefinite direction does NOT propagate — constraint algebra.** The fields carrying G are
`φ = (ξ,u) = (ln N, u)`: in this action `N = (2X)^{−1/2}` is a **functional of the varied clock T** (not an
independent ADM lapse) and u is a pure auxiliary — **neither carries a kinetic term** in the reduced
Hamiltonian. `AUXILIARY_SYMBOL.md`'s secondary constraints `χ_a = −δH/δφ_a` have principal part
`χ_a = H_gg,ab (Δ̄) δφ_b`, giving

>     {χ_a, p_b}_principal = −|k|² H_gg,ab .

When `det H_gg ≠ 0` this 2×2 bracket is **invertible**, so `(χ_ξ, χ_u)` and their momenta `(p_ξ, p_u)` are a
**second-class** set: both auxiliary fields and both momenta are eliminated → **0 propagating DOF** from the
auxiliary sector. The **sign** of det H_gg is irrelevant to second-class-ness; only det ≠ 0 matters, so a
negative determinant is the ordinary signature of a healthy elimination, **not** a gradient ghost. A faithful
toy — one physical scalar with a normal kinetic term coupled through gradients to two auxiliaries whose
gradient block is the indefinite `G(π=0)` (det = −1/9 < 0) — runs through the Dirac counter to **DOF = 1**
(only the physical field propagates; the auxiliary pair is 4 second-class constraints, C1-c1). The physical
field's effective gradient stiffness after elimination is the **Schur complement** `s_pp − cᵀG⁻¹c`, whose
sign is set by the elimination, not by det G (C1-c2).

**(c) The propagating scalar is positive-definite at the witness.** The genuinely dangerous case is the
rank-drop `det H_gg = 0` (the witness, G₀ rank one), where a direction could leak into physics. Exactly
there, the lead's Legendre-transformed physical Hessian `M = M₀ + xG₀` has
`det M = 3(4𝒯−27)(8𝒯+x)/(2𝒯) > 0` for all wavenumbers (`4𝒯−27 = 39.75 > 0`, C1-c3): the rank-one marginal
direction enters M with a **positive** x-coefficient. This is the L44/L52/L54 resolution — "an auxiliary's
Schur complement replaced a marginal zero." det G stays negative for a finite neighbourhood of π = 0 and
passes through the rank-one zero only at λ = 1 (C1-d), but it lives entirely in the eliminated auxiliary
sector throughout.

> **VERDICT — CONCERN 1 = ARTEFACT (non-propagating).** The indefinite gradient direction is the eliminated
> second-class auxiliary `(ξ,u)`; it does not propagate. The propagating mode is the Schur complement M,
> positive-definite at the witness for every k. **RESIDUAL, stated honestly:** M is verified only at the
> expanding witness (π ≠ 0). At π = 0 / a static galactic background the physical propagating sector is
> **uncomputed** (no such background exists yet) — but that is the *same* L66-4b / L69 deep-MOND gap, which
> is **L71's lane**, not a new instability introduced by this concern.

---

## 3. CONCERN 2 — the design-point knife-edge (PART 2)

The lead's exact all-wavelength dispersion (`IC20 §5`, checked against `dispersion()` to < 10⁻⁴⁰) is

>     ω²/(e^{2S}k²) = (M·cIR − 2Bk²·cUV)/(M − 2Bk²),   M = H_SS < 0, B > 0, cUV ∈ (0,1).

**Sign law (proved symbolically, C2-a).** For M < 0, B > 0, cUV > 0 the ratio → cIR as k → 0, and is positive
for **all** k² ≥ 0 **iff cIR ≥ 0**: its only numerator zero sits at `k²* = M·cIR/(2B·cUV)`, which is positive
(an in-range sign flip) exactly when cIR < 0. So IR stability is controlled by the **single number cIR**.

**The whole knife-edge collapses to one closed form.** Reading the design-point ingredients once
(S = 0.1, a = K = 0.126387, e = H_SR = −0.963451, B = 0.584039, cUV = 0.2, Cdot = 1.536268) gives

>     cIR(H_SS) = c₀ + κ_flow/H_SS,   c₀ = cUV − 4ae²/(BE) = −0.457840,   κ_flow = 2·Cdot·e/E = −2.423638,

with **c₀ and κ_flow both exactly independent of the H_SS design target** (verified: identical at H_SS = −3
and −1000; only K, B, cUV are also fixed). This closed form reproduces the entire offline oracle sweep
(H_SS = −0.5 … −1000) to < 3×10⁻⁷, reproduces L66's design-point positivity (cIR = 0.350039, speeds
0.350→0.200, C2-b), and reproduces the lead's adverse control (H_SS = −1000 ⇒ cIR = −0.455 < 0 ⇒ IR ω² < 0
while UV stays +0.2, C2-c).

**Boundary and classification (C2-d, C2-e).** cIR = 0 at `H_SS* = −κ_flow/c₀ = −5.2936`. The healthy set is
the **open interval `H_SS ∈ (−5.29, 0)`**; the design point H_SS = −3 sits **interior**, factor **1.76** from
the boundary. The design point is interior in **all four** design directions — A_* healthy on (0, ≈0.21)
[design 0.1, margin ≈2.1×], cUV healthy across the entire subluminal range (0,1), E_* healthy up to
construction validity ≈0.3 [design 0.1] — so the window is a genuine **multi-dimensional open set**, not a
lower-dimensional locus.

> **VERDICT — CONCERN 2 = OPEN WINDOW (not a knife-edge).** Health is one number cIR = c₀ + κ_flow/H_SS; the
> healthy region is open with the design point interior at ≈1.76–2.1× margin — a **modest bounded design
> freedom, not a fine-tuning**. **L66's "adjacent coefficient already gives IR ω² < 0" overstated the
> fragility:** the true boundary is H_SS ≈ −5.30 (factor 1.76 from the design point), whereas L66 cited
> H_SS = −1000 (factor 333) as "adjacent." The quantity that crosses the boundary is the **IR scalar speed²
> cIR = cbase + 2·Cdot·H_SR/(e^{2S}·H_SS)**, a self-coupling within the clock/curvature scalar sector,
> evaluated in vacuum FLRW with **no matter source**.

---

## 4. Relation to L69's theorem (PART 3)

L69's root is the single matter→MOND transmission channel that "MOND from one metric" forces: the lapse
coupling `λ = C[n,φ]` of a **separate** MOND scalar to a clock's acceleration (H2). **Neither concern is that
channel.** CONCERN 1 is a fixed-metric **vacuum** principal symbol of the clock's own auxiliary block — no
separate scalar, no matter sourcing, no λ (L69-1). CONCERN 2 is the clock scalar's own IR speed² in vacuum
FLRW — again no separate scalar and no λ (L69-2). So neither is a face of L69's transmission-channel root,
and neither is a new class-level mechanism: they are, respectively, an eliminated-auxiliary artefact and an
ordinary scalar-stability design constraint (satisfied with margin). This is consistent with L66/L69: the
integrable-clock action escapes the L60/L69 kill by **violating H2**, and the price of that escape is *not*
paid in either of these two concerns.

---

## 5. Verdicts (PART 4)

| concern | verdict | mechanism / margin |
|---|---|---|
| **1 — indefinite auxiliary Hessian** | **ARTEFACT (non-propagating)** | det G < 0 is the eliminated second-class auxiliary `(ξ,u)`; propagating Schur complement M positive-definite at the witness (`det M > 0` ∀k). Residual = uncomputed physical mode at π = 0 (= L66-4b/L69 gap, L71's lane), not a new kill. |
| **2 — design-point knife-edge** | **CURABLE / OPEN WINDOW** | Health = cIR = c₀ + κ_flow/H_SS > 0; open interval `H_SS ∈ (−5.30, 0)`, design interior at ≈1.76× margin; multi-dimensional open box. A modest design freedom, not a tuning. |

**Combined verdict, three sentences.** With L71 deciding the galactic deep-MOND health separately, these two
concerns do **not** kill the lead's construction: concern 1 is a non-propagating eliminated-auxiliary
artefact (the indefinite determinant never reaches a physical mode, and the physical Schur complement is
positive at the witness), and concern 2 is a real but **open** coefficient window with ≈1.76–2.1× margin, not
a knife-edge. Neither is L69's transmission-channel root nor a new class-level mechanism, so the honest status
of the construction is unchanged by this lane except that two of L66's flags are now resolved in its favour.
The one gap these concerns leave standing is the *same* one L66-4b and L69 already named — the physical
propagating scalar has been verified positive only at the cosmological witness (π ≠ 0), and its deep-MOND
(π = 0, galactic) health is still uncomputed — which is L71's job, not something L72 can or does turn against
the construction.

---

## 6. What is open, named

1. **The deep-MOND propagating mode still does not exist to test.** C1-c3's positivity of the physical Schur
   complement M is at the expanding witness only; the static/quasi-static (π = 0) physical scalar sector — the
   one that actually carries galaxy phenomenology — is uncomputed because the lead has produced no galactic
   quasi-static background. This is the L66-4b / L69 open item, handed to L71. **Until it exists, "concern 1
   is an artefact" is established for the eliminated-auxiliary reading of the flag, not a full deep-MOND
   health pass.**
2. **The window is modest.** The open interval `H_SS ∈ (−5.30, 0)` is a genuine design freedom, but a bounded
   one (factor 1.76 to the near boundary). If a future deep-MOND or matter-coupled calculation pushes the
   required H_SS (or A_*) past its boundary, cIR flips and concern 2 becomes live again. The window should be
   carried as a *constraint the coupled theory must respect*, not as unlimited freedom.
3. **c₀ < 0 is the structural fact behind the window.** The design point is IR-stable only because the
   background-flow term κ_flow/H_SS (positive at H_SS = −3) offsets a **negative** frozen base c₀ = −0.458.
   Any modification that suppresses the flow term (large |H_SS|, or a static/slow background where the flow
   contribution shrinks) exposes c₀ < 0. Whether the deep-MOND background keeps the flow term large enough is
   part of item 1.

κ = ½ remains **fitted**; this lane never says otherwise. Nothing here is closed.
