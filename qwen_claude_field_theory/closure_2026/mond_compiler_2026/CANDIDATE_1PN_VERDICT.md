# CANDIDATE 1PN VERDICT — the `chi` + TT-carrier `Q_ij` MOND candidate

**Date:** 2026-08-29
**Subject:** single-metric ADM MOND candidate with auxiliary scalar `chi` (lapse-tied,
`phi = ln N`) and auxiliary traceless tensor carrier `Q_ij`, frozen at
`V'(chi) = -[ln(1-chi)]^2`, `f(chi) = (1-chi) sqrt(V'(chi))`.
**Question put:** compute `alpha_1`, `alpha_2` at 1PN for a source moving at velocity `w`
relative to the preferred foliation; classify PASS / KILL / INCONCLUSIVE.

---

## VERDICT

# KILL — but *not* by the preferred-frame bounds.

`alpha_1 = alpha_2 = 0` **EXACTLY** at the candidate's own locus. Three independent engines
agree, each GR-validated, each anchored to published khronometric PPN. Neither bound is
violated, so the preferred-frame gate is **not** what kills this candidate.

It is a **vacuous pass**. The same solve that returns the zeros also returns
`a_mu == 0` on-shell, `G_eff/G = 1`, and no MOND force at all. The candidate passes the
preferred-frame gate for the same reason a rock passes it.

The candidate dies on three *other* results, all PROVEN, all reached in the course of
answering the alpha question, and none of which is a bound comparison:

| # | Kill | Status |
|---|---|---|
| K1 | **The literal spec is not a MOND theory.** `mu_eff = 1 ± chi/2 ∈ [1/2, 3/2]`, never → 0. No deep-MOND limit for either sign, and `G_eff/G_N = 2/3` or `2` at high acceleration. | PROVEN |
| K2 | **The carrier is void.** Eliminating a local `Q_ij` returns `(f²/3M)A²` — a pure redefinition `F(A) → F(A) − f²A²/(3M)`. No new tensor structure, so hypothesis (H4) is never violated and Part-I applies verbatim. | PROVEN |
| K3 | **GR-with-no-MOND is an exact branch.** `(any GR solution, any geodesic slicing, chi = 0, Q = 0)` solves every field equation exactly, for every source. Nothing selects the MOND branch. | PROVEN |

And the alpha zeros themselves are structurally worthless: the locus `bet = lam = 0` is
`c_123 = 0` ⟺ `c_s² = 0` ⟺ the `lambda_Horava → 1` **strong-coupling point**. `alpha_1` and
`alpha_2` are **discontinuous** there. The value *at* the point is 0; every neighbourhood of
it contains theories with `alpha_1 → -4·alp` and `alpha_2 → ∞`.

---

## ALPHA VALUES

### At the candidate's own locus (`bet = lam = 0`, forced exactly)

```
alpha_1 = 0        EXACTLY     [COMPUTATIONALLY_VERIFIED, 3 independent engines]
alpha_2 = 0        EXACTLY     [COMPUTATIONALLY_VERIFIED, 3 independent engines]
gamma_PPN = 1                  G_eff/G_N = 1        alpha_3 = 0
```

VACUOUS — obtained together with `a_mu ≡ 0` on-shell (exact in `w`, not `O(w²)`-suppressed)
and no MOND force. The MOND force that survives is `(w/c)^4 ~ 1e-12` suppressed.

### On the named OPEN DOOR (`lambda_K ≠ 1`, a *different* theory)

The static gates force the `a·a` coefficient to be `alp_kh(y) = 2(1 − mu(y))`. Then:

```
alpha_1 = -4 alp_kh                                = -8 (1 - mu(y))
alpha_2 = -alp_kh/2 + alp_kh²/(2 c₂) + (3/4) alp_kh²
        = -(1-mu) + 2(1-mu)²/c₂ + 3(1-mu)²
```

`|alpha_1| = 8(1 − mu(y))`, against `|alpha_1| < 1e-4` (LLR) / `~4e-5` (binary pulsars):

| location | y = g/a₀ | FROZEN `1−e^−y` | framework canonical | simple `y/(1+y)` |
|---|---|---|---|---|
| Sun surface | 2.93e12 | <1e-300 | 1.37e-12 | 2.73e-12 |
| Earth 1 AU | 6.34e07 | <1e-300 | 6.31e-08 | 1.26e-07 |
| Saturn 9.5 AU | 7.02e05 | <1e-300 | 5.70e-06 | 1.14e-05 |
| Neptune 30 AU | 7.04e04 | <1e-300 | 5.68e-05 | 1.14e-04 |
| 100 AU | 6.34e03 | <1e-300 | 6.31e-04 | 1.26e-03 |

`|alpha_2| ≈ (1 − mu(y))` (leading term for `|alp_kh| ≪ |c₂|`), against `|alpha_2| < 4e-7`
(solar spin-axis alignment). At the Sun's own field, `y ~ 2.9e12`, `1−mu ~ 1.7e-13`: passes
comfortably for every kernel tried.

**The kernel fork matters and is reported both ways** (framework rule 4). With the *frozen
exponential* `mu = 1−e^{−y}` the suppression is structural: `e^{−y}` underflows every float
format inside 100 AU (`~1e-2751`). With the *framework's own canonical* kernel
`g_obs = sqrt(g_bar² + g_bar a₀)` the suppression is only power-law, `1−mu ≈ 1/(2y)`, and the
margins are `1e2–1e3`, **not** `1e2700`. The 1e-2751 figure is a property of `e^{−y}`, not of
the architecture.

---

## THE CRUX QUESTION, ANSWERED

> *Does the carrier switch off in the Solar System (`f(chi) → 0`), giving `alpha_1 = alpha_2 = 0`
> there? Or does the lapse-tied MOND sector generate preferred-frame terms independently?*

**Neither option as posed. The question contains a false premise, and the answer splits.**

1. **`f(chi) → 0` is a red herring.** The carrier never had anything to do with the alphas. Its
   on-shell stress is `O(a^4)` while `Sigma_P` is `O(a^2)` — two PN orders below. The carrier
   cannot contribute to `alpha_1` or `alpha_2` at *any* value of `y`, large or small.

2. **The lapse-tied MOND sector does generate them on its own — but only OFF the candidate's
   locus.** `chi(D phi)²` *is* the khronometric `a_mu a^mu` operator (proven on explicit
   components, not assumed), so it is exactly the structure that gives khronometric theories
   their nonzero alphas. It yields `alpha_1 = -8(1−mu(y))` with **zero** carrier involvement.
   The Solar-System suppression is `(1 − mu(y))` — a property of the **interpolation function**,
   not of the architecture.

3. **At the candidate's OWN locus, even that is empty.** `K_ijK^ij − K² + R3` is *exactly* the
   Einstein-Hilbert scalar (Gauss–Codazzi at `lambda_K = 1`), so `bet = lam = 0` EXACTLY and the
   khronon has no kinetic term. Every non-GR term is then at least quadratic in `a_mu`, so
   `a_mu = 0` is an exact stationary point with nothing to obstruct it. `alpha_1 = alpha_2 = 0`
   there **because MOND itself is gone**, not because any symmetry protects it.

So the honest one-line answer: *the alphas vanish, the crux premise is wrong on both branches,
and the vanishing is a symptom of the disease rather than a clean bill of health.*

---

## CERTIFICATES

All scripts committed, self-checking, exit 0. **Rule applied:** a route that fails its own GR
validation is discarded. None did.

| script | checks | GR validation | literature anchor |
|---|---|---|---|
| `routeA_alpha12_ppn_2026.py` | 41/41 | `alpha_1 = alpha_2 = 0`, `gamma = 1` exactly [P7] | Blas–Pujolas–Sibiryakov 1007.3503 Eq. (5.34) @ β=0, to 1 part in 1e3 |
| `ppn_khronon_routeB_*.py` | see `.out` | `gamma = 1`, all alphas 0, `G_N/G = 1` | Foster–Jacobson → HO limit, 4 exact-rational points, digit-for-digit |
| `adv_refute_ppn_2026.py` | 19/19 | [V2b] exact | Foster–Jacobson → HO limit derived **in-script**, 5 exact-rational points |
| `adv_refute_static_carrier_2026.py` | 21/21 | n/a (static) | — |
| `synth_1pn_independent_checks_2026.py` | **26/26** | n/a (structural) | pole structure + discontinuity, re-derived |

### Independent-agreement ledger

Two independent routes agreeing **and** surviving refutation = CONFIRMED. Here there are
**three** engines plus a fourth structural arm:

* **Route A** (ADM → Stueckelberg khronon, exact in `w`, Laurent-expanded): `alpha_1 = alpha_2 = 0`
  at `lam2 = 0`; two independent `alpha_1` extractions (`h_0i` and `h_00`) agree identically.
* **Route B** (covariant khronon from scratch, full 6×6, `tau` not gauge-fixed): same zeros;
  `shat = 0` on-shell for `w ≠ 0`.
* **Refuter** (independent engine, imports nothing from either route): reproduces both,
  reproduces Route B's approach table **digit-for-digit**
  (`alpha_1 = -16/5, -16/11, -88/101, -808/1001`;
  `alpha_2 = -2/5, -50/99, -6424/4545, -5135749/450450`).
* **Stage 2B** (separate adversarial arm, degenerate Palatini branch): independently exhibits
  the *same pattern* — `alpha_1 = alpha_2 = 0` exactly on a branch with a timelike
  boost-breaking VEV, explicitly labelled a **vacuous pass** because `mu ≡ 1`, no MOND. That a
  second, structurally unrelated branch reproduces the identical "zeros because the theory is
  secretly GR" signature is strong corroboration that the zeros here are degeneracy, not symmetry.

### What this synthesis pass verified itself

`synth_1pn_independent_checks_2026.py` (26/26), written from scratch, importing nothing:

* **A1–A4** — the literal spec's constitutive law: `mu_eff ∈ [1, 3/2]` (or `[1/2, 1]`), never 0.
  Deep MOND needs `F' → −2`, i.e. `|F'| = O(1)` and **negative**; no sign choice of
  "coefficient = `chi`" can do it. **PROVEN.**
* **B0–B4** — carrier elimination reproduced independently: `A_ij A^ij = (2/3)A²`,
  `Q = (f/M)A_ij`, `L_on = (f²/3M)A²`, degree 4 in `a`. Confirms the refuter's C1.
* **C1–C4 — a gap I found and closed** (see below).
* **D0–D6** — pole structure and the discontinuity, plus regeneration of both routes' approach
  table from the formulas alone. Sign dictionary re-confirmed: routes' `(alp,bet,lam)` =
  literature `(alpha, −beta, −lam)`.
* **E1–E3** — the GR-branch theorem's arithmetic core: `V'(chi) = 0` only at `chi = 0`;
  `V' ~ −chi²` is integrable there so `V(0) = 0` is available; carrier vanishes at `A_ij = 0`.

---

## A GAP I FOUND IN THE REFUTATION (recorded; it is not a rescue)

The spec says `Q_ij` is "spatially-**transverse**-traceless (`Q^i_i = 0`)". Those are **two
different constraints** and the parenthetical states only the trace one. The refuter's C1
varied 5 traceless components with **no transversality constraint**.

* For the **traceless-only** reading (what the parenthetical literally says), C1 is correct and
  I reproduce it exactly: `L_on = (f²/3M)A²`, a pure redefinition of `F(A)`. [B3]
* For the **strictly transverse-traceless** reading it does **not** hold. Eliminating a TT `Q`
  returns `A_ij (P^TT A)^ij`, which I verified is **not** proportional to `A²` and carries
  explicit angular dependence on the wavevector — i.e. it is **nonlocal** in position space.
  [C3, C4]

**Why it is still not a rescue:**
1. That is an **(H1) nonlocality** escape, not the advertised (H3)/(H4) degenerate-tensor-carrier
   escape — the same verdict the refuter already reached for `M = -D²` and `M = Δ^{-1}`. The
   tensor carrier *per se* buys nothing; every escape is really nonlocality or higher derivatives.
2. Enforcing `D^i Q_ij = 0` is a **differential** constraint requiring its own Lagrange
   multiplier, so `Q` stops being an algebraic auxiliary and the Dirac/DOF count would have to be
   redone from scratch (it is already 3, not 2).
3. It changes **nothing** about K1 and K3, which hold with `Q = 0` identically.

---

## REMAINING OPEN GATES (none closed by this pass)

* **OPEN DOOR — the real successor.** `lambda_K ≠ 1` restores a healthy khronon, keeps MOND, and
  passes `alpha_1`, `alpha_2`. **This is a different theory** (the candidate's gravity sector is
  *exactly* Einstein–Hilbert, which is what forces `lam2 = 0`). Its own gates are **UNTESTED**:
  `c_T`, BBN `lambda_K ∈ [0.923, 1.100]`, cosmology, ghost/gradient stability, and the DOF count.
  This is where the interesting alpha numbers actually live, and it is not closed.
* **Dirac / DOF count.** `N_dof = 3`, not 2 (`dirac_chi_Q_frozen_candidate_2026.py`). The leak is
  the **lapse**, not `Q`. Verdict EXTRA_MODES + STRONG_COUPLING. The DOF count *jumps* between
  the vacuum (`y = 0`, where the theory is GR with 2 DOF) and every excited state (`y > 0`, 3 DOF).
* **`c_T`.** Not computed for this candidate. Untouched.
* **Cosmology.** Not computed. FLRW background, perturbations, CMB all untested.
* **Nonlinear / strong field.** Only 1PN and linearised static were done.
* **The `alpha_2` bound assignment (honest caveat, flagged not hidden).** Standard PPN assumes
  **constant** alphas. Here `alp_kh` depends on position through `y`, so the table entries are
  **local** values of position-dependent PPN parameters. Which `y` the solar-spin-axis bound
  actually probes is *not* settled: at the Sun's own field (`y ~ 3e12`) `alpha_2 ~ 1.7e-13` and
  passes hugely; evaluated instead at Neptune's `y ~ 7e4` the framework kernel gives
  `alpha_2 ~ 7.1e-6`, which would **exceed** the `4e-7` bound by ~18×. A proper bound needs the
  y-dependent analysis. **This is an unresolved gate on the open door, not a pass.**
* **Part-I's magnitude, re-examined (cuts FOR the class).** The traceless stress is real, but the
  metric slip it induces is `v_flat²/c² ~ 1e-8 – 1e-6` relative. `Sigma_P ≠ 0 ⇒ cannot lens` is a
  statement about a formally nonzero, **physically negligible** slip. Worth re-checking before
  Part-I is used to kill any future metric-carried candidate.

---

## SCOPE CAVEATS

1. **The kill is of the candidate as specified**, plus its named minimal repairs. It is **not** a
   no-go for lapse-tied MOND in general — the `lambda_K ≠ 1` door is explicitly open.
2. **No literature formula was recited from memory.** The Foster–Jacobson → hypersurface-orthogonal
   reduction is derived in-script in two places and cross-checked against BPS in a third. My own
   Section D deliberately checks only *pole structure and discontinuity* of those in-script
   formulas rather than re-asserting them; I flag this because my first attempt to reconstruct
   Foster–Jacobson from recall was **wrong** and its checks failed — the failure is recorded here
   rather than quietly repaired.
3. **The alpha zeros are COMPUTATIONALLY_VERIFIED, not PROVEN.** Three engines agree, but all
   three solve a linear system *at* a rank-deficient point. The discontinuity (D4/D5) is the
   proven part.
4. **The repaired constitutive branch was not carried through the full 1PN solve.** The repair
   (`coefficient 2(1−chi)`, `V' = −2[ln(1−chi)]²`) is the branch on which MOND actually works,
   and on it the advertised `f = (1−chi)sqrt(V')` is **imaginary**. The one "exactly verified,
   residual 0" identity of the original design was computed on the constitutive law that does
   **not** do MOND.
5. **Both-ways discipline.** This pass produced findings cutting *for* the candidate class
   (Part-I's magnitude is negligible; the TT gap is real) and reported them as prominently as the
   kills. Two of the routes' own sub-results were corrected, and one of Route A's was refuted.

---

## ONE-LINE SUMMARY

`alpha_1 = alpha_2 = 0` exactly — a **vacuous pass at a strong-coupling point**, where the
zeros mean "no MOND" rather than "protected by a symmetry"; the candidate dies instead on three
proven results (the literal spec is not MOND, the carrier is a pure redefinition of `F(A)`, and
GR-with-no-MOND is an exact branch), while the `lambda_K ≠ 1` successor stays open and untested.
