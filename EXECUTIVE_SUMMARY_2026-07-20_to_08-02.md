# Executive Summary — two weeks, 2026-07-20 → 2026-08-02

**Framework.** de Sitter–Unruh **modified inertia**. One claim: **a₀ = κ·c·√(Gρ_Λ) with κ = ½**, i.e.
a₀ = cH_Λ/Z, Z = √(32π/3) = 5.78881 → **9.36×10⁻¹¹ m/s²**. Own kernel g_obs = √(g_bar² + g_bar·a₀).
**κ = ½ is fitted, not derived.** Prior art concession: the kernel ν = √(1+1/y) is Milgrom 1999 PLA 253:273
Eq. 9 identically; the distinctive content is the **coefficient**. Every number below is backed by a
committed, runnable script that exits non-zero on a failed check.

---

## 1. THE HEADLINE RESULT — κ = ½ is testable, and it beats its nearest rival

`mi_a0_profile_likelihood_sparc_2026.py` (11/11). Profile a₀ on all 175 SPARC galaxies with **Υ free per
galaxy**, so any global stellar-population offset is absorbed by construction:

| | a₀ | Δχ² | vs best fit |
|---|---|---|---|
| **κ = ½ (framework)** | 9.36e-11 | **63.9** | −2.40σ |
| κ = 1/2π (Milgrom 2020) | 8.62e-11 | **154.3** | −3.67σ |
| alt footing ρ_tot/cH₀ | 1.13e-10 | **7.0** | +0.91σ |
| free best fit | **1.077e-10** | 0 | — |

σ(a₀) = **1.24%** (points independent) / **5.44%** (galaxy-clustered) against the **8.20%** κ gap →
Z_disc = 6.6 / 1.5. **First time the distinctive coefficient is separated from its nearest published rival by
data rather than argument (~2.2σ).** Forecast-grade: no distance/inclination treatment, and the kernel's
shape is part of the lever while being assumed.

**Mechanism, verified by mutation:** the lever is the **gas** (HI carries no mass-to-light ratio, so
rescaling Υ cannot mimic a₀ at any depth — invariance residual ≠ 0, → 0 only as g_gas → 0), and the
**transition shape** second (Newtonian limit gives the full factor L). Let Υ scale the gas too and the
constraint dies 10×.

---

## 2. THE FORKS, AND WHERE EACH HAS TENSION

### Fork A — a₀ footing: ρ_DE/cH_Λ vs ρ_tot/cH₀
Both are **κ = ½**; they differ by exactly one factor √Ω_Λ = 0.8276. `mi_a0_footing_selection_2026.py` (8/8).
**TENSION: two independent estimators bracket the ALT footing and both sit above canonical.** SPARC profile
→ 1.077e-10; a₀-line GLS → 1.181e-10. Bracket is informative (they agree to 9.2%, tighter than the 20.8%
fork, 0.44×). Canonical sits −2.81σ from the combination, ALT +0.76σ.
*Against interest:* empirical g† = 1.20e-10 sits +2.01σ — better than nothing but the estimators only say
"the scale is near 1.1e-10", which every MOND-family value says. The two estimators are **not independent**
(the a₀-line's gas-dominated sample is a subset of the 175). **Unresolved, leaning ALT.**

### Fork B — MI vs MG (realization)
`mi_realization_ladder_2026.py` (6/6). **Three rungs, not two:**

| | variational | galaxies | solar system | light | GW = c |
|---|---|---|---|---|---|
| the recipe (algebraic law as a force) | ✗ | ✓ | ✗ (α=1) | ✗ | ✗ |
| **MI** — Milgrom 1994 nonlocal | ✓ | ✓ | ✓ | ✗ | ✗ |
| **MG** — AQUAL → AeST | ✓ | ✓ | ✓ | ✓ | ✓ |

**TENSION: the mechanism is MI (dS–Unruh is about a body's inertial response), but MI has no relativistic
completion, so light + GW force MG.** Exactly one rung meets all five requirements. The rung the corpus
actually *fits* with is **neither** — it's a recipe, non-variational in a disc.
**a₀ is an INPUT on every rung**, so the choice costs the claim nothing — and an action wouldn't derive κ
either. **Data cannot decide it:** separations are 2.35σ_sys (α=1: 1.090 vs 1.137) and 1.92σ_sys
(α=2: 1.0246 vs 1.0631), both inside the frozen undecidable band [1.083, 1.145], declared in advance.

### Fork C — kernel α=1 vs α=2
α=1 makes g_obs² = g_bar² + a₀g_bar **exact**; α=2 (μ = x/√(1+x²)) is in force.
**TENSION — the sharpest open liability, and it got WORSE this fortnight:** `mi_alpha2_sun_reflex_2026.py`
(7/7). The α=2 residual is a **1/g tail**, so it binds at the **lowest**-acceleration body — the **Sun**
(Jupiter-dominated reflex 2.09e-7 = 2233 a₀), not the planets. After the corpus's own LM ephemeris fit
(36 ICs + GM_☉ + GM_J free, kitchen-sink absorption variant): **Mars carries 8.5× (canonical) / 12.4× (alt)
the ranging budget**, 6.2× kitchen-sink. Survival line s_max = 0.34 a₀ / 0.28 — **both footings sit above
it.** GM_J absorption closed by Juno.
**"DISCHARGED on both footings" is WITHDRAWN.** It contradicted a *published* corpus paper
(WHITEPAPER_TOE_MAP §4.3.2, "12.7 m, ×8.5, Mars-carried") from seven weeks earlier. The switch bought a real
3.35 orders (1278× → 8.5×) — **not a pass.**
**Escapes, priced:** the exponential/McGaugh-RAR tail (the whitepaper's own template) clears by >1e13;
frequency dressing needs p ≥ 0.069 at ≤0.010 dex SPARC cost. **This prices a kernel-SHAPE choice; it does
not kill the framework.** SPARC does not require α=1 (0.0084 dex across α = 1, 2, ∞).

### Fork D — particle vs mode (is dark matter a fluid or a particle?)
GDM degeneracy **theorem**: the CMB constrains a *fluid*, not a *particle* (0σ both ways).
**TENSION:** w₀ squeeze 5.85 orders, footing-independent; substructure **leans particle**. Live axes: the
wide-binary shape and the √M knee.

### Fork E — a₀(z) evolution
Correct closed form: a₀(z)/a₀(0) = (1+z)^{1.5(1+w₀+w_a)}·exp(−1.5 w_a z/(1+z)) = **bump-then-decline**.
**TENSION:** MUSE-DARK III (Ciocan 2026) measures a₀ **rising** — that is a *tension*, not a confirmation.
**And this front is EXACTLY κ-blind** — κ cancels in the ratio, d/dκ ≡ 0 identically. The most interesting
front in the corpus can never test the number; it tests the ρ_Λ tie.

### Fork F — the covariant MI action (form class)
Three no-goes had closed it. **The audit reopened all three.** The (v/c)² amplitude no-go measured the
modification against the **rest mass** instead of the kinetic term it dresses → required |K| is O(1)
(0.29–0.62), **inside** ‖K‖ ≤ 1, not the 3.8e5–3.8e7 published. Disc circulation is **3.2–4.4 km/s**, not
38.8 (from-rest conversion error). "Not the EL equation of ANY action" holds only for **natural** Lagrangians.
**Surviving wall:** an **argument mismatch** — the kernel is sampled at w = γΩc/a₀ ≈ 2854 where the closure
needs x = |a|/a₀ ≈ 2. E1–E5 Frenet/spectral math independently confirmed; |a|/B = v/c exactly.

---

## 3. FRONTS THAT CHANGED STATUS

| front | was | now | script |
|---|---|---|---|
| **σ-spread (MI-distinctive)** | dead, N(3σ) ~ 2e7 | **ALIVE** — priced at a_ext = 2a₀, the signal *minimum*; at its own frozen 0.3–1 a₀ shell N(3σ) = **5.0e3–2.6e5**, clearing CHANCES by 1.1×–60×; the load-bearing check **fails everywhere in-shell** | `mi_sigma_spread_aext_scan_2026.py` (9/9) |
| **SN-Ia host step** | "lever CLOSED, null" | **UNDERPOWERED** — **18% power** at the observed 0.06 mag; 80% needs D = 0.142 mag (2.4×) or N ~ 2505 vs 449 (5.6×). Disfavoured, **not excluded** | `mi_snia_power_curve_2026.py` (10/10) |
| **cluster η** | 4.05σ tension | **1.35–4.05σ** — the ladder was truncated at the tight end of the corpus's own 0.1–0.3 dex floor; at 0.30 dex it is **not a tension** | `clusters_eta_audit.py` |
| **s^TX SME dipole** | live, margin 1.50× | **NOT LIVE** — α=2 collapses it to 1.03e6× / 7.09e5×; three stale STANDING rows struck | Amendment 5 |
| **wide-binary gate** | trap narrowed 2→1 | **stays 2** — the hybrid S(\|a\|/a₀)×L(ω/ω_c) branch survives the withdrawal. In-force α=2 target is **γ_v = 1.0310** (1.0218–1.0472), not the 1.02 Amendment 6 registered | audit lane |
| **Ly-α forest** | 0.4–0.9σ, all bins <3σ | **0.4–0.9σ on the calibration channel only** — the statistical channel has bins at 5.1/7.9/6.0σ. The *withdrawal* of the old 6–8σ exclusion stands | audit lane |
| **directional EFE** | "not confrontable" | **FIRED** — Â = +2.95, p = 0.029, AQUAL-class sign at n=16, **kills Branch B**; n=237 pipeline exists | `FIRST_FIRING.md` |

---

## 4. THE METHODOLOGICAL FINDING — and it is the most important one

Three of these reversals share **one defect: using the wrong quantity as an error bar**, always in the
dismissive direction.

1. **Scatter ≠ parameter error.** I graded the SPARC RAR by its 0.108 dex per-point scatter. Those differ by
   ~√N, N = 3380. MLS16's own **random** error is 1.7% — five times *smaller* than the κ gap. That single
   substitution turned a front that resolves the question at 1.5–6.6σ into "not falsifiable."
2. **Don't truncate a systematic range at its tight end.** The cluster ladder stopped one rung short of the
   corpus's own floor; the missing rung turns 4.05σ into 1.35σ.
3. **Per-object ≠ ensemble.** The a₀-line row used the **per-galaxy** ±16% budget; the averaging **floor** is
   13% (11–14%, robust — and it cannot be beaten by sample size: N = 2000 still leaves 12.8%).

Symmetrically, **three manufactured wins withdrawn** (`mi_efe_escape_and_ch23_withdrawn_2026.py`, 8/8):
the **EFE escape does not exist** (scalar-adding g_ext pointed the Galactic field permanently sunward and
reported the orbit's phase *minimum*; done as vectors ⟨g_ext·r̂⟩ = 0 and post-EFE = **bare**, 1279×/1544×);
the stale s^TX rows; and **Ch.23's figure hard-normalized 0.5 in place of 0.5878** (17.56%, load-bearing —
it moved the SM point from *outside* the figure's own band to *on* it), plus **the two "roads" are one road**:
√(2/Z) = √(2κ)·(3/8π)^¼ identically, so the match *requires* κ = ½ as input.

**Audit scale:** 8 lanes, 17 agents, every finding adversarially verified — **47 survived, ~24 refuted.**
Refutations included several of my own proposed findings, and two audit numbers that **did not reproduce**
and were not banked (the σ-spread "suppression reverses" claim; a max-min/pop-RMS conflation).

---

## 5. HONEST STANDING

**What is established:** a₀ = ½c√(Gρ_Λ) is a compact, correct, prior-art-conceding re-expression of the
measured acceleration scale, **and it is now discriminable from its nearest published rival at ~2σ using data
already on disk** — the first time that has been true.

**What is not:** κ = ½ is **fitted, not derived**, and no realization forces it (the "provably unforceable"
verdict is itself overstated — Z and κ are in bijection, and the **κ-linear spectral class is untried**). The
solar-system liability is real at **6–12×** on both footings and prices a kernel-shape choice. The mechanism
question (MI vs MG) is open and **not observationally decidable** in DR4. Two independent estimators pull a₀
**15–26% high** of the canonical footing.

**Never say:** "theory closed", "no open doors". **Never re-open** the TOE/SM overclaims retracted publicly
2026-06-23 — the true position is the a₀ reframing only.

**Two real prizes, neither an MI-vs-MG question:** (1) a **relativistic modified-inertia theory** — nobody
has one, and the torsion result is the one concrete clue why (bound orbits carry torsion; the obstruction is
kinematic, not a bad kernel); (2) **deriving κ**.
