# 📝 AMENDMENT 12 — **DRAFT, NOT FILED** (2026-09-09)

**Status: drafted at the owner's instruction, "draft it, don't file". Nothing has been appended to
`PREREGISTRATION_DR4.md`; no `*_HASH.txt` file has been created or touched. This document is a
proposal for the owner to read. Filing requires an explicit go, and the append-only rule is
unchanged.**

Source: `fable_independent_2026/L47_xi_collision.py` / `.out` / `L47_XI_COLLISION.md` (31 checks,
13 FAIL, **all 10 controls pass**), corroborating `fable_independent_2026/L30_saturated_branch.py`.

---

## Why this amendment exists

Amendment 11(b) registered Arm B — the covariant candidate — at a coherence length of
**ξ ≥ 0.10 pc canonical / 0.15 pc alt**, citing `g03d_exact_fourth_order_solar.py`. That floor is
**wrong for the structure Amendment 11(b) names**, and the error is one of scope rather than
arithmetic: the machinery that produced it never evaluates the fourth-order coherence operator on the
point mass at all.

**The finding, reproduced three independent ways** — an exact symbolic Green's function verified for
arbitrary background stiffness, a 3-D FFT solve, and a Newton boundary-value solve in a different
variable from L30's. Solving the registered structure's own scalar equation drives the scalar gradient
onto the **biharmonic cone**, giving an enclosed phantom-mass fraction of exactly **r²/(2ξ²)** —
kernel-free, a₀-free and mass-free. The Pitjev–Pitjeva Saturn phantom-mass bound then forces

> **ξ ≥ 4.00 pc** (Saturn gate), or **ξ ≥ 1.38 pc** on the sunward gate alone, **identical on both
> footings.**

Two robustness checks that were not run before and that both strengthen it: the law survives a
**realistic** Solar-System source to 0.24% across six mass models from a point through a polytropic
Sun to the planets, interstellar medium and local Oort density, **and every departure raises the
phantom mass**; and the bound **does not depend on the repair of the kernel past saturation**, since
no solve reaches even half the boost ceiling.

**Why the standing floor is blind, quantified.** Three screening laws share the observable and the
ξ-scaling but differ in normalisation by **1 : 262 : 5.37e5**. The factor to the deposited paper's
formula is *exactly* g_N(Saturn)/(2Ca₀): the paper suppresses the **saturated residual**, the equation
suppresses the **Newtonian source**. `g02_filtered_efe.py` and `g03x`, which produced the standing
floor, contain **no fourth-order operator**. `g03d` and `g03g` do, but apply it to a field whose source
is suppressed by **9.3e-7** at Saturn.

---

## (a) Corrected Arm B prediction

Evaluated with **the same frozen estimator Amendment 11 registers** (control: it reproduces both
published numbers, `g03g` 1.0325/1.0400 and `g03y` 1.0450/1.0300).

| | canonical | alt |
|---|---|---|
| Amendment 11(b) as registered | 1.0450 | 1.0300 |
| **corrected, at ξ ≥ 4.00 pc (Saturn gate)** | **1.0000 ± 0.0025** | **1.0000 ± 0.0025** |
| corrected, at ξ ≥ 1.38 pc (sunward gate only) | 1.0025 ± 0.0037 | 1.0025 ± 0.0037 |

γ_force = 1 + r²/(2ξ²): mass-free, orientation-free, external-field-free and a₀-free. The boost at
20 kAU is **2.876e-4** against the registered ceiling's 9.2e-2, a factor **320**.

**The registered ceilings are NOT falsified — the corrected value stays below them.** They are
**vacuous**: 320× too loose, excluding nothing. Stated against interest, this makes Arm B **weaker**
than registered, not stronger.

**There is no coherence length inside the registered structure that both passes the Solar System and
returns 1.0450.** That needs ξ = 0.226 pc, excluded by **313×** on the Saturn phantom mass.

## (b) Corrected decision rule — the operative change

Amendment 11(d)'s kill-from-above threshold must move:

> **≥ 1.129 → ≥ 1.084.**

**As registered, a DR4 result in [1.084, 1.129] would kill Arm B and the table would not say so.**
Amendment 11(d)'s row "1.007–1.056 → decided for B" is also wrong at the supported ξ, since the
corrected prediction is 1.0000 and that interval no longer contains it.

## (c) Structure declaration — carrier, decided 2026-09-09

The deposited paper (DOI 10.5281/zenodo.22667688) and `THE_ACTION_2026-09-05.md` both display the
coherence operator **inside** the MOND function with a **carrier** source, and Amendment 11(b) names
that structure verbatim. The registered γ_v was nonetheless computed by a solver using the **outside**
placement **and** an **AQUAL** source. Those placements give floors of **4 pc and 585 pc** and are not
interchangeable.

**The owner has decided the programme is the CARRIER reading.** This amendment registers that
declaration so the ambiguity cannot be resolved after the data.

## (d) What is NOT corrected here

**Arm A is untouched.** Its band (1.1614–1.1814 / 1.1917–1.2267) comes from the frozen kernel taken as
modified gravity with **no** coherence length, so nothing above bears on it. Every clause of Amendments
10 and 11(a) stands.

## (e) Declared cost

Arm B was already the arm DR4 cannot confirm over Newton. At the corrected ξ it becomes
**indistinguishable from Newton by this estimator**. Combined with the separate finding that the frozen
systematic caps Arm B at 2.25σ / 1.50σ **at infinite N**, **Arm B is not a testable arm of this
preregistration**, and this amendment says so rather than leaving it to be discovered after the data.
