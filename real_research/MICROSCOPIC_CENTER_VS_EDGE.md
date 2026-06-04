# The Microscopic Crux: Flat Rotation Curves Require de Sitter = the DSSYK Center

**C. Zimmerman, June 2026.** *Pushing the microscopics. The framework's most contested input — de Sitter = the
DSSYK spectral center — is shown to be the **data-favored** reading: flat rotation curves exclude the competing
spectral-edge proposal. Numbers: `reviews/project_center_vs_edge.py`.*

---

## The question

Everything in the framework's deep-MOND derivation traces to one contested identification
(`reviews/project_the_wall.py`): **de Sitter = the DSSYK spectral *center*** (E=0, Narovlansky–Verlinde), where
the density of states is *flat*. The leading competitor — Rahman (2025, arXiv:2505.08116) — derives de Sitter-JT
gravity at the spectral *edge* (E=E₀), where the DSSYK density of states *vanishes* as a square root (the
Schwarzian edge). The whole field is split on this (the center-vs-edge dispute). The decisive question: **does
the observed MOND phenomenology need the center, or does the edge work too?** If only the center works, a
contested *assumption* becomes a *data-favored* conclusion.

## The calculation

The DSSYK q-Gaussian density of states ρ(E) on E ∈ [−E₀, E₀] (E = E₀cos θ) has two qualitatively different
locales, both confirmed numerically:

| locale | ρ(E) behaviour | numerical exponent |
|---|---|---|
| **center** (E→0) | ρ ~ \|E\|⁰ — **flat**, finite nonzero DOS | −0.01 ✓ |
| **edge** (E→E₀) | ρ ~ (E₀−E)^{1/2} — **square-root**, DOS vanishes | +0.53 ✓ |

The framework maps the MOND interpolation μ(x) to the cumulative "freezing" measure — the integral of ρ over the
energy window (∝ the acceleration ratio x) *around the de Sitter spectral state*. By calculus the cumulative
exponent is m = (local DOS exponent) + 1, and then μ(x) = x^m with μ(x)·g_obs = g_bar gives g_obs ~ g_bar^p,
p = 1/(m+1), and a point-mass rotation curve V(r) ~ r^{(1−2p)/2}:

| de Sitter = | DOS | m | g_obs ~ g_bar^p | rotation curve | BTFR |
|---|---|---|---|---|---|
| **center** (N–V) | flat | 1 | **p = 0.50** | V(r) ~ r⁰ = **FLAT** | **V⁴ ~ M** |
| **edge** (Rahman) | √ | 3/2 | p = 0.40 | V(r) ~ r^{+0.10} = **RISING** | none (curves not flat) |

## The result

**Observed:** flat rotation curves and the baryonic Tully–Fisher relation V⁴ ~ M (i.e. g_obs ~ g_bar^{0.50}).
This **requires the flat-center DOS** (p = 0.50). The **edge reading gives g_obs ~ g_bar^{0.40} and *rising*
rotation curves** (V ~ r^{+0.10}) — excluded by the single most basic galactic fact. So, given the framework's
emergent-gravity / DSSYK bridge,

> **the very existence of flat rotation curves is evidence that de Sitter = the DSSYK spectral *center*
> (Narovlansky–Verlinde), not the edge (Rahman).**

## What it buys, and what it does not

- **The wall becomes data-favored.** The framework's single most contested assumption is no longer merely
  *assumed*: of the two live de Sitter-holography proposals, **only the center reproduces galaxy dynamics.** That
  is a genuine discrimination — and a striking (if conditional) bridge from galaxy rotation curves to a frontier
  quantum-gravity dispute.
- **It strengthens the sign and the coefficient's *foundation*.** The deep-MOND *sign* (flat DOS → √-law) and the
  conditional coefficient result Z = 4·ρ₀(q)/√(1−q) both need the central DOS; that foundation is now
  data-supported.
- **It does *not* by itself fix Z.** The DSSYK coupling q remains free, so Z is forced only *given* q; q ≈ 0.926
  is then a *prediction* (read off the observed a₀). Pinning q independently — e.g. from the de Sitter entropy —
  would close the coefficient.
- **Honest caveat (loud).** The discrimination is *conditional on the framework's mapping* — MOND interpolation =
  cumulative chord-vacuum DOS, deep-MOND = the neighbourhood of the de Sitter spectral state. It is a clean
  *implication of that structure*, not an unconditional theorem. If the mapping is wrong, the test says nothing.
  And the result is, in part, "the framework's chosen reading is the one consistent with the data it was built to
  match" — but the *new* content is real: the **competing** (edge) proposal is *excluded*, which it need not have
  been.

## Where this leaves the microscopic programme

The center-vs-edge question was the one thread that could turn the coefficient from "natural packaging" into
"forced." Pushing it gives a clear partial win: **the center is the data-favored reading**, so the framework's
foundation is firmer than "contested assumption" — but the coefficient remains tied to the free coupling q.

**Update — pinning q (the move that would have *forced* Z) instead *refutes* the microscopic coefficient**
(`reviews/project_pin_q.py`). The de Sitter entropy *does* fix q, via the Narovlansky–Verlinde dictionary:
λ = 4π²/S_dS, so q = exp(−4π²/S_dS). But our de Sitter has S_dS ~ 10¹²², so **q → 1 (the semiclassical limit)** —
and there the framework's relation Z = 4ρ₀(q)/√(1−q) ~ (2ρ₀/π)√S_dS **diverges** (Z ~ 2.5×10⁶⁰, a₀ ~ 2.6×10⁻⁷⁰
m s⁻², off by ~60 orders of magnitude). The value Z = 5.79 (a₀ ~ 1.2×10⁻¹⁰) requires **S_dS ~ 520 — a
Planck-scale de Sitter (R_dS ~ 23 l_P), not ours.** So the s = Z match at q ≈ 0.925 was a coincidence at an
unphysical point; pinning q to the *actual* de Sitter breaks the coefficient relation. **The coefficient is
therefore not forced from below** — neither geometrically (the deep-geometry result: simple criteria give Z = 1
or 2, the extra Friedmann factor isn't uniquely fixed) nor microscopically. Z = 2√(8π/3) stands as a natural
geometric packaging that fits to ~6%, honestly open.

**What survives the refutation:** the deep-MOND **sign** is q-*independent* — the flat-center DOS gives the
√-law and flat rotation curves for *any* q — so the SIGN derivation and the center-is-data-favored result are
untouched. Only the COEFFICIENT's microscopic derivation fails. The remaining decidable move is now just **(2)**:
watch whether the DSSYK literature resolves center-vs-edge — if the center, the framework's *sign* closes; the
*coefficient* will need either a 6% a₀ measurement (to pick 2√(8π/3) vs 2π) or a genuinely different mechanism.
Galaxy dynamics still has a vote — on the sign, not the coefficient.
