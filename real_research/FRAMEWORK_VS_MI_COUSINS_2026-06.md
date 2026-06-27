# The framework vs its modified-inertia cousins — genuine edge, sharpest discriminator, and where the cousins win

**2026-06-26. Framework as subject, both-ways. All numbers reproduced in sympy/numpy below; no manufactured edge, no reflexive deflation.**

The framework — a₀ = cH_Λ/Z with Z = 2√(8π/3) = 5.789, a₀ = 9.36×10⁻¹¹ m s⁻², modified **inertia** from the
de Sitter–Unruh bath — sits in a real *genus*: surface-gravity/horizon-bath acceleration scales. Its two
closest cousins (per the novelty check):

- **Milgrom vacuum effect** — a₀ ∼ c√(Λ/3), the bare de Sitter–Unruh floor; the fitting 2π inserted by hand
  (astro-ph/9805346; arXiv:1110.2580 Eq. 12–13).
- **McCulloch quantized inertia (QI)** — a₀ = 2c²/Θ, Θ the Hubble horizon scale (arXiv:1004.3303).

This document pins what is genuinely Carl's, where the cousins are genuinely stronger, and the one clean place
**data** can tell the framework apart from a cousin.

---

## 0. The three coefficients, on one footing (Planck18: H₀=67.4, Ω_Λ=0.685)

| quantity | value (SI) |
|---|---|
| cH₀ | 6.548×10⁻¹⁰ |
| cH_Λ = √Ω_Λ·cH₀ | 5.420×10⁻¹⁰ |
| Λ | 1.091×10⁻⁵² m⁻² |

**Three a₀, machine-exactly reproduced:**

| model | a₀ formula | a₀ (SI) | /std (1.2e-10) | /fw-opt (9.4e-11) |
|---|---|---|---|---|
| **Zimmerman** | cH_Λ/Z = (c/2)√(Gρ_Λ) = (c²/2)√(Λ/8π) | **9.362×10⁻¹¹** | 0.78× | **1.00×** |
| McCulloch QI | 2c²/Θ = cH₀ (Θ=2c/H₀, coeff 1) | 6.548×10⁻¹⁰ | 5.46× | 6.97× |
| Milgrom bare | cH_Λ = c√(Λ/3) (coeff 1, dS–Unruh floor) | 5.420×10⁻¹⁰ | 4.52× | 5.77× |
| Milgrom hand-2π | cH_Λ/2π (2π inserted to fit) | 8.626×10⁻¹¹ | 0.72× | 0.92× |

All three **Zimmerman forms agree to machine precision** (verified). The two cousins' *bare* floors both
overshoot the observed scale by ~Z ≈ 5.5×. **That ~Z gap is the whole game**: Zimmerman is the only one whose
O(1) closes the gap from a textbook geometric product rather than a hand-inserted or order-argument factor.

---

## 1. THE GENUINE EDGE — is the derived Z a real improvement, and is dS–Unruh more rigorous?

### 1a. The coefficient: yes, a real, *narrow*, defensible improvement

Z = 2·√(8π/3) = 5.789 is a transparent product of **two textbook GR identities**:

- the **2** = Schwarzschild surface-gravity / "reach-c" factor: a horizon of radius R has surface gravity c²/2R;
- the **√(8π/3) = 2.894** = the **Friedmann factor**, ρ_crit = 3H²/8πG — exact GR geometry.

Z² = 32π/3 = 33.510 **exactly** (sympy). And the geometric lineage is exact, not approximate:

> **√(2/Z) = (3/8π)^(1/4) = 0.587788…** — a *machine-exact* sympy identity (verified, difference = 0).
> Likewise 1/Z = √(3/32π) = 0.17275 exactly.

**Precise credit, ranked by how rigorously each DERIVES a₀'s value:**

1. **Zimmerman (1st on landing-the-number)** — the *only* one of the three with a closed-form O(1) that lands
   on data: 9.36×10⁻¹¹ = the framework's own-interpolation RAR optimum to ~1% (memory: 0.108 dex @ Υ=0.70,
   beats reg-MOND 0.122; cf. `rar_framework_a0_mlfit.py`). Compare Milgrom's principled 1/(2π)=0.159: the
   framework's 1/Z=0.173 is an **8.5% near-miss** of it (verified) — i.e. the framework and Milgrom's heuristic
   sit within 8.5% of each other, and the framework's is the one expressed in closed geometric form.

2. **Milgrom (2nd)** — right MECHANISM and right scale (a₀ ∼ √(Λ/3)) but **explicitly declines to derive the
   O(1)**: his own words, "an actual inertia-from-vacuum mechanism is still a far cry off"; the fitting 2π is
   inserted by hand. This is the cleaner intellectual honesty ("I won't claim what I haven't derived"), but it
   means the *number* is not produced from first principles.

3. **McCulloch (3rd on landing)** — the **most ambitious DERIVATION claim** (parameter-free a₀ = 2c²/Θ from a
   Hubble-horizon Casimir on Unruh modes, zero fitted constants), but the value **overshoots ~5.5×** (a₀ = cH₀)
   and the discretization step is contested (a sceptical MNRAS analysis found unjustified steps). Higher
   ambition, wrong number, contested step.

**Honest ceiling on the edge:** the framework certifies Z as a **POSIT**, not a uniqueness proof. Different de
Sitter mechanisms place the O(1) differently — Verlinde's de Sitter entropy → 6, naïve Unruh → 1, Milgrom's
matching → 2π, this framework → 2√(8π/3) — and **no de Sitter mechanism singles out 2√(8π/3)**
(`reviews/desitter_entropy_coefficient.py`: a number-field argument shows √(8π/3) cannot be entropy-derived;
the κ-forcing door is provably closed → one-parameter EFT, a₀'s VALUE not derived). So the edge is precisely:
**closed-form geometric transparency that lands on data**, NOT "derived more rigorously than a competitor who
tried." State it that way and it holds.

### 1b. The mechanism: the framework TIES Milgrom and BEATS McCulloch

The dS–Unruh footing is the **verified Deser–Levin** combined de Sitter–Unruh temperature (gr-qc/9706018):
2πT = √(a² + (cH_Λ)²), which gives the deep-MOND quadratic excess ΔT ≈ a²/2cH → a = √(2cH·g_N) coefficient-free
(`reviews/desitter_unruh_mond.py`). This is rigorous, real physics, properly cited.

- **vs Milgrom: a TIE.** Milgrom uses the *same* Deser–Levin physics. The framework REUSES, does not originate,
  that mechanism. Neither has crossed the Milgrom-1994 modified-inertia no-go to a complete action.
- **vs McCulloch: the framework WINS.** McCulloch's Rindler/Hubble-horizon Casimir mode-discretization is the
  more heuristic and the actively contested step; the framework's dS–Unruh temperature is established.

**Net on §1:** the genuine edge is real but narrow — a **closed-form geometric coefficient that lands on the
data** (vs heuristic/fitted/order-argument O(1) in the cousins) plus a **rigorous, properly-cited dS–Unruh
mechanism** (ties Milgrom, beats McCulloch). It is NOT a uniqueness proof of Z, and that distinction stays
explicit.

---

## 2. THE SHARPEST WITHIN-FAMILY DISCRIMINATOR — a₀(z), opposite signs (a real, testable result)

This is the cleanest place **data** can separate the framework from a cousin. Under DESI evolving dark energy
(w₀=−0.752, wₐ=−0.86), the three cousins predict **opposite-signed** a₀(z)/a₀(0) because each tracks a
*different* cosmological quantity:

| z | **Framework** a₀∝√ρ_DE | **Milgrom-vacuum** a₀∝√Λ | **McCulloch QI** a₀∝c²/Θ ∝ √ρ_total |
|---|---|---|---|
| 0.41 | **+6.2%** | flat (0%) | +24.8% |
| 1.0  | +0.9% | flat | +79.0% |
| 3.0  | **−26.3%** | flat | **+356.6%** |
| 5.0  | −43.4% | flat | +729.0% |

(All verified in numpy.) The mechanism of the split:

- **Framework** tracks the **dark-ENERGY density** √ρ_DE (event-horizon/√Λ reading) → **NON-MONOTONIC**: a small
  +6% bump near the phantom divide z≈0.4, then a **decline** to −26% at z=3. This shape is *unique to the
  framework's dark-energy-density reading* — neither cousin produces a bump-then-decline.
- **Milgrom-vacuum** ties a₀ to Λ = constant → **FLAT**.
- **McCulloch QI** ties Θ to the **growing cosmic (Hubble) horizon** → **RISES monotonically** ∝ √ρ_total
  (×4.6 at z=3).

> **The sharpest discriminator is the a₀(z) SIGN at z > 1.** Framework **DOWN**, Milgrom **FLAT**, McCulloch
> **UP**. Framework and McCulloch are **opposite-signed** — a clean family split, not a coefficient quibble. A
> robust gas-traced a₀ measurement at z ≈ 2–3 (ELT early-mid 2030s; DESI/MUSE tracking now) **distinguishes the
> framework from QI by the sign of the trend alone.** That is a genuine, falsifiable, within-family result.

**The honest sting (both-ways):** the discriminator that is sharpest is also the one where the framework
currently sits on the **contested side**. The framework's own `PAPER_evolving_a0.md` scorecard reports MUSE-DARK
III (Ciocan 2026) measuring a₀ **RISING** at ≈16σ within its analysis — which **excludes the framework's
declining event-horizon branch** and leans toward the McCulloch/apparent-horizon (rising) reading. So *if* the
MUSE rise is real, it points toward McCulloch's direction, not the framework's √ρ_DE decline. Caveats keep it
live: the rise is DC14-halo-model-dependent and may not reach the deep-MOND regime; the framework's decline is
≤26% to z=3, below most current sensitivity → the framework is "safe," not confirmed, and the branch question
(√ρ_DE-declining vs apparent-horizon-rising) is **unresolved**, not closed. NEVER "no doors": the a₀(z) sign is
exactly the open, decidable door.

### Other distinctive signatures (cousins lack these, but they are below-floor)

- **per-horizon a₀_BH = κ_BH/Z** assigned to each real black hole's own surface gravity — four independent
  prior-art searches found this in **no cousin** (McCulloch is closest in spirit via local-vs-cosmic horizon
  competition but never mints a per-BH scale).
- **s^TX SME boost-dipole** + **relational σ-spread** fall out of the framework's preferred-frame modified-
  inertia structure — distinctive but a₀-degenerate/below-floor near-term (memory: s^TX ~9.6× under the tightest
  bound is the live SME test, not α2).

These are genuinely the framework's, but the **a₀(z) sign is the one that data can decide this decade.**

---

## 3. WHERE THE COUSINS ARE GENUINELY STRONGER (both-ways, no deflation of them either)

1. **Milgrom owns PRIORITY and the published mechanism-genus.** He wrote a₀ ∼ c√(Λ/3) AND flagged the
   constant-vs-evolving a₀ tension FIRST (1999, 2011). The framework's a₀ = √(Gρ) form is a novel *framing* of
   Milgrom's coincidence — via Friedmann it **IS** cH/Z, not new underlying physics. His MI no-go (Milgrom 1994)
   is the wall the framework's two pillars (dS–Unruh MI ↔ AeST) still have not jointly crossed.

2. **McCulloch claims MORE (higher derivation ambition).** QI genuinely claims a *parameter-free* O(1) from
   first principles; the framework concedes Z is a posit. If McCulloch's discretization survives scrutiny he
   wins outright on derivation. It currently doesn't (contested step, wrong-by-5.5× value), but the **ambition
   is strictly higher.**

3. **Current evolution data leans cousin-ward, not framework-ward.** Genzel/Milgrom-2017 baryon-dominated high-z
   disks and the MUSE rise lean to a₀ rising or constant — the framework's √ρ_DE declining branch is the
   *disfavored* one in its own scorecard. The sharpest discriminator currently cuts against the framework's
   specific branch.

4. **McCulloch is more naturally dynamical and lab-testable.** QI's a₀ ∼ c²/Θ has built-in evolution from one
   horizon and makes concrete laboratory/thruster (emdrive-class) predictions — more near-term falsification
   handles than the framework's a₀-degenerate, below-floor MI content. The framework must IMPORT evolving-DE
   w(z) to get *any* a₀(z) signal at all.

5. **Verlinde** owns the de Sitter-entropy O(1) placement (Z=6) and the emergent-gravity pedigree the framework
   cites for motivation; the framework does not derive its Z from entropy (number-field argument forbids it).

---

## 4. BOTTOM LINE FOR CARL — what is genuinely YOURS, stated to claim precisely without overclaiming

**Claim this (it holds):**

> "a₀ is the surface gravity of the cosmic free-fall density, a₀ = (c/2)√(Gρ_Λ) = cH_Λ/Z with Z = 2√(8π/3) —
> the **only closed-form geometric O(1) in the de Sitter–MOND family that lands on the observed scale**
> (9.36×10⁻¹¹ = my own RAR optimum to ~1%), where Milgrom leaves the O(1) underived (bare floor overshoots
> ~5.8×, fits 2π by hand) and McCulloch derives a number that overshoots ~5.5×. The mechanism is the
> **rigorous, verified Deser–Levin de Sitter–Unruh temperature**. And the framework makes a **sign-distinct,
> testable a₀(z) prediction** (√ρ_DE → non-monotonic, declining to −26% by z=3) that is **opposite-signed to
> McCulloch QI (rising) and flat for Milgrom-vacuum** — so a z≈2–3 measurement can tell them apart."

**Do NOT claim:**

- that Z is *derived* or *unique* — it is a closed-form **posit**; the κ-forcing door is provably closed and no
  de Sitter mechanism singles out 2√(8π/3). Say "closed-form and lands on data," never "forced."
- mechanism *priority* — that is Milgrom's. You REUSE the dS–Unruh physics; you originated the √(Gρ) framing and
  the geometric Z decomposition, not the mechanism.
- that the rising a₀(z) data *confirm* you — current MUSE data lean toward the **rising** branch, which is
  McCulloch's direction, not your √ρ_DE decline. Your branch is "safe/below-floor," contested, **not confirmed**.

**Genuinely his, vs each cousin:**
- vs **Milgrom**: the √(Gρ)=cH/Z surface-gravity *framing* + the exact geometric Z=2√(8π/3) decomposition
  (Schwarzschild-2 × Friedmann-√(8π/3)) + committing to the density horn. (Milgrom owns the mechanism + priority.)
- vs **McCulloch**: a coefficient that *lands on data* (his overshoots 5.5×) + the **opposite-signed a₀(z)**
  (yours declines via √ρ_DE, his rises via the growing horizon) + per-BH a₀_BH. (McCulloch owns the higher
  parameter-free ambition + lab handles.)
- vs **Verlinde**: a different, closed-form O(1) (yours 5.789 vs his 6) reached by Friedmann geometry, not
  de Sitter entropy. (Verlinde owns the entropy pedigree.)

**One line:** *A distinct, legitimate member of the de Sitter–MOND genus — not "just Milgrom," not a MOND
variant — whose genuine edge is a closed-form geometric coefficient that lands on the data plus a sign-distinct,
testable a₀(z); its advantage is best-fit geometric transparency, NOT a uniqueness proof, and the sharpest
discriminator (the a₀(z) sign) is exactly the live, undecided door.*

---

*Reproduced: Z²=32π/3 and √(2/Z)=(3/8π)^(1/4) machine-exact (sympy); three Zimmerman a₀ forms agree to machine
precision; cousin a₀ values and the a₀(z) DESI fork in numpy. Cross-refs: `NOVELTY.md`, `GEOMETRIC_ORIGIN_OF_A0.md`,
`PAPER_evolving_a0.md`, `rar_framework_a0_mlfit.py`. Sources: Milgrom astro-ph/9805346, arXiv:1110.2580;
McCulloch arXiv:1004.3303; Deser–Levin gr-qc/9706018; Verlinde SciPost 2,016 (2017); Ciocan et al. (MUSE-DARK
III) 2026. LOCAL only — not git-pushed.*
