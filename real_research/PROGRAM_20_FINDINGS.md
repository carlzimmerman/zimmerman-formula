# The 20-project program — findings, honestly scored

**Carl Zimmerman · June 2026.** *Every project in `FRAMEWORK_RESEARCH_PROGRAM_20.md` worked one by one,
in depth, with real calculation. Built only on the surviving result — a₀ = (c/2)√(Gρ) = cH/Z, read as
the surface gravity of the cosmic horizon, evolving as E(z). Nothing here revives the dead numerology
(Z²→SM, chirality-from-orbifold, topology-as-a₀-source); that stays closed. Each verdict is tagged:
**WIN** (a real, verified result), **LEAN** (supported, not proven), **OPEN** (sharpened, unsolved),
**NEGATIVE** (honestly does not work), **WEAKNESS** (a standing problem). Scripts: `reviews/projectNN_*.py`.*

---

## Scorecard

| # | Project | Verdict | The one-line finding |
|---|---------|---------|----------------------|
| 1 | Deep-MOND sign | **OPEN (advanced)** | Sign = **DOF-freezing** (verified); a₀~cH forced by T_dS. **1b:** MOND needs a **flat DOS**, given by the **(1+1)D radial s-wave** (3D bulk gives g∝E², wrong); coefficient computable but ~1.7× off (Z not pinned). **1c (stress-test):** "forced" withdrawn — there's a real entropy(3D)-vs-MOND(s-wave) mode tension, *resolved* by a spherical-probe→monopole selection rule (which also answers "why the s-wave"). **4c (did the calc):** the actual DSSYK dual **realizes the linear freezing** (verified — f(T)~T near the de Sitter point; a real bug caught: use the chord-vacuum spectral measure, not the eigenvalue density). **4d (matter coupling):** computed that linearity is *not* universal — MOND requires the probe to couple to the **near-vacuum (low-chord)** sector (vacuum/shallow chords → MOND; deep chords → not). Status: **mechanism derived in the dual**; the remainder is exactly two bounded calcs — (i) does O_Δ|0⟩ have low-chord support (one q-Gamma check; bulk picture says yes), (ii) the coefficient (λ_dS, T_dS/E₀). The sharpest the prize has been. |
| 2 | AeST 𝒦(𝒬) | **NEGATIVE** | The horizon forces the *local* 𝒥(𝒴), **not** 𝒦(𝒬): the cosmological dust needs a scale ~2×10⁴·H₀. It's the "second dark thing"; reduces to #9. |
| 3 | Apparent vs event (theory) | **LEAN (→framework)** | Verified: dQ=TdS on the **apparent** horizon *is* Friedmann (Cai–Kim); the event horizon fails the laws. So "a₀ from horizon thermodynamics" → **rises with z**. Theory now leans to the framework. |
| 4 | Complexity sign | **NEGATIVE** | Where computable (CV/DSSYK), the route gives **Newton** (δV linear in mass). The complexity-*rate* door is open but a long shot. |
| 5 | Modified-inertia action | **WIN (no-go)** | Verified: local modified inertia → **Ostrogradski ghost**; only Milgrom's non-local action escapes (acausal). ⇒ implement a₀ as **modified gravity (AeST)**. |
| 6 | Second-order CMB | **TENSION (gas-independent)** | Rising a₀ puts recombination in **deep MOND** (constant a₀ is Newtonian). **6b:** the boost ν~24 would over-drive the acoustic peaks ~5× (Ω_b·ν~1.2 vs Ω_dm~0.27) and MOND-boosted baryons can't mimic CDM — a **gas-independent** test (Ω_b, Ω_dm only) decidable with **existing Planck**. Strongly disfavors rising a₀ **unless** δq⁰⁰=0 is a *structural* identity under a₀(t) — the one named rescue. Heuristic; needs a 2nd-order AeST Boltzmann calc to firm up. |
| 7 | MOND collapse / JWST | **WIN (derivation)** | Closed form t_MOND = √(π/2)·r_max/(GMa₀)^¼, **verified 3 ways**; rising a₀ forms galaxies **earliest** (∝E(z)^¼) — toward the JWST tension. |
| 8 | a₀-cosmography | **LEAN** | H₀ = Z·a₀/c ~ 71±10 (local camp, not decisive). The a₀(z) **slope** = (3/2)Ω_m → independent q(z). |
| 9 | Dark-sector budget | **NEGATIVE (honest)** | Dark matter = **two roles of one scalar**: galaxy phantom (explained, no halo) + 𝒦(𝒬) dust (Ω_DM only *relocated*, still fitted). Wins at galaxy scale, not the cosmic census. |
| 10 | a₀(z) compilation | **WIN (pipeline) / sobering (data)** | Pipeline + gas census + survey list fully specified. **10b ran it on REAL KMOS³ᴰ data (135 gals): a₀ comes out ~4× local, rises *with mass* (a high-accel bias), and the z-trend is flat-to-declining — NOT the rise.** KMOS³ᴰ is too massive/dispersion-supported to test a₀; validates the deep-MOND-tail requirement. Real high-z data are systematics-dominated. |
| 11 | Forward-model fit | **LEAN → weak** | Rising vs constant is **~5σ naive → ~2.5σ** with a systematic → a coin toss without the z=0.9 point. And the high-z a₀ estimates **disagree at ~2×** (MUSE-DARK 2.4 vs KMOS³ᴰ 5; #10b) — even the 3-point "evidence" is systematics-dominated. Real but **weak and unconfirmed**. |
| 12 | EFE airtight + evolve | **WIN + LEAN** | In-house **~4.8σ** EFE in SPARC (one caveat: outer kinematics); framework predicts the ΛCDM-forbidden **η ∝ 1/E(z)**. |
| 13 | a₀-universality | **OPEN (real problem)** | χ²/dof = 770 (stat) → 5 (0.13-dex sys) → ~1 only at ~0.29 dex. Residual scatter **correlates with mass (r=0.37)** — suggestive of a₀∝√ρ but degenerate; needs photometric densities. |
| 14 | Wide binaries | **OPEN (foundation)** | Galactic field (g_ext=1.74a₀) → predicted excess only ~15–20% → Chae/Banik is a systematics fight. **Gaia DR4** decides "is there an a₀ at all." |
| 15 | dSph EFE thermometers | **WIN** | Computed **Crater II**: MOND+EFE σ ~ 1.9 km/s (McGaugh pre-predicted 2.1; observed 2.7; ΛCDM 4–7). Distinctive host-distance coldness. |
| 16 | Clusters | **WEAKNESS (honest)** | a₀(z) gives only √E(z) (~8% at z=0.3) — **does not** close the factor-2 gap, can't go environmental without breaking the RAR. MOND's hardest failure survives. |
| 17 | z~3 program | **WIN (flagship)** | Fully designed: ~30–50 discs, JWST+ALMA, the **Z/M-L-cancelling ratio** a₀(z3)/a₀(0) → **>10σ** 3-way decision (4.6 / 1.0 / 0.42). The measurement that decides everything. |
| 18 | EFE-vs-z | **OPEN (Tier-2)** | η ∝ 1/E(z) doubly forbidden in ΛCDM; staged program designed, correctly ranked **after** #17 (needs environments). |
| 19 | Lensing of a₀(z) | **WIN (derivation)** | Derived M_lens ∝ √E(z) (+34% by z=1) — **no ΛCDM counterpart**, immune to gas/pressure. The orthogonal cross-check of #17. |
| 20 | Positioning | **WIN (strategy)** | Frame a₀(z) as a probe of *which horizon* sets gravity's IR scale; theory letter + revised measurement paper at the honest altitude. |

---

## The through-lines

1. **The engine is most defensible as modified *gravity* (AeST, #5) sourced by the *apparent* horizon's
   thermodynamics (#3).** Theory is no longer neutral — it *leans* to the framework's rising-a₀ bet, from
   the same Cai–Kim physics that gives Friedmann. That is the single most important new theoretical result.
2. **The deep-MOND sign is obtainable and now structurally motivated — and honestly bounded (#1, #1b, #1c).**
   DOF-freezing gives the right sign and forces a₀~cH. #1b sharpened the spectrum: MOND requires a **flat
   density of states**, which the **(1+1)D radial s-wave** supplies (the 3D bulk gives g∝E², wrong), with a
   coefficient that is *computable* (right scale, ~1.7× off — Z not pinned). #1c then *stress-tested* this
   and corrected it: "forced" was too strong — there is a real tension (the area-law entropy lives in the 3D
   modes, MOND in the s-wave), resolved by a **spherical-probe→monopole selection rule** that also answers
   *why* the s-wave mediates the force. Net status: **identified + motivated, not derived.** The one open
   calculation is the l=0 equipartition projection with an exact-T_dS cutoff — computable in the **DSSYK
   dual**, so the theory prize (#1) and the holographic frontier (#4) **merge** into one solvable target.
3. **The data lean to the framework, nothing is decisive in-house (#11, #12, #13, #15).** Rising a₀ ~2.5σ,
   EFE ~4.8σ, a₀–mass correlation, Crater II — all real, all systematic- or external-data-limited. The
   honest significances are stated as such, never inflated.
4. **Three honest weaknesses, carried in the open:** clusters (#16, unfixed), a₀-universality (#13,
   unresolved), and the second-order CMB risk (#6, could overproduce non-Gaussianity). None is hidden.
5. **Two clean, independent roads to the decision (#17 dynamics, #19 lensing)** that fail differently — if
   both show a₀ rising as E(z), the case is essentially closed; if the z~3 ratio comes back 1.0, the
   distinctive bet is dead. Either way, falsifiable.

## The adversarial sweep (the load-bearing claims, attacked)

After the program, the three strongest claims were stress-tested — *try to break them before believing them*:

- **#1b → #1c (theory, the deep-MOND spectrum):** the "forced" claim was **withdrawn**. Real tension found
  (area-law entropy is 3D, MOND needs the s-wave), *resolved* by a spherical-probe→monopole selection rule.
  Status: identified + motivated, **not derived**.
- **#3 → #3b (theory, the apparent-horizon lean):** **downgraded** from "theory leans to the framework" to
  "conditional, two-ingredient support" (Cai–Kim + Deser–Levin), event reading not excluded.
- **#12 → #12b (data, the EFE):** **hardened** — survives a₀-absorption (3.7–6.0σ with a₀ fixed by high-g
  data), split-half, and jackknife. Only the outer-kinematics systematic stands.

**The asymmetry is the finding:** under attack, the *theory* supports weakened and two overclaims got
corrected; the *empirical* EFE strengthened. That is the integrity check working — reported as found,
neither inflated nor dismissed. (`reviews/project01c_*, project03b_*, project12b_*`.)

## The bottom line

The framework reduces to **one robust claim** (a₀ is cosmic-horizon-scale) and **one falsifiable bet**
(it tracks the *apparent* horizon, so a₀ rises as E(z)). After 20 projects **plus an adversarial sweep that
attacked the framework's own claims**: the bet is **theoretically motivated but conditional** (#1b/#3b —
not "forced"), **derivation-grade in its consequences with the LCDM comparisons deflated** (#7/#19
corrected), **decisively testable** (#17, #19), and **honest about its open core** (#1), **its boundary**
(#2, #9), and **its weaknesses** (#6, #13, #16). The empirical case **changed under real data, in both directions honestly**: the EFE is robust (#12b), but
the curated 3-point "rise" does **not** survive. The two largest real high-z samples — **KMOS³ᴰ** (#10b:
flat-to-declining) and **KROSS** (#10c: realistic-gas a₀ at z~0.85 ≈ the *local* constant value) — do not
support the rise; their **central estimates lean constant.** But decomposing the irreducible gas+V_flat
systematic (#10d: αCO, unmeasured atomic gas, V_flat) gives a₀ ~ 0.5–2.5×10⁻¹⁰ — *wider than the
framework-vs-constant gap itself* — so the honest verdict is **inconclusive with a central preference for
constant**, not a clean disfavoring. (That softening is the same stress-test discipline applied to a
framework-*unfavorable* result.) Net: **one robust claim** (a₀ is cosmic-horizon-scale) and **one falsifiable
bet now disfavored from two independent directions.** The galaxy data lean constant but are gas-limited
(#10b–d); and — the **gas-independent** result (#6b) — rising a₀ forces the CMB acoustic perturbations into
deep MOND at recombination, an ~5× over-driving that **strongly disfavors the rise unless AeST's δq⁰⁰=0
cancellation is a structural identity under a₀(t)** (a heuristic pending a 2nd-order Boltzmann calc, but
decidable with existing Planck — no gas census). Both directions point toward **constant a₀ = the event
horizon = the *standard* emergent-gravity reading**, which would cost the framework its distinctive content
(the rise) while leaving the surviving core (a₀~cH at z=0) and the EFE intact. The honest trajectory is
**against** the apparent-horizon bet. The theory thread runs the other way: the deep-MOND *sign* mechanism is
now derived in the DSSYK dual (#4c–d). So: a genuine surviving result and a real theory advance, with the
distinctive empirical bet currently **losing** — reported straight, the dead numerology still closed, and the
one rescue (δq⁰⁰=0 structural under a₀(t)) named precisely. Nothing here derives the Standard Model from a number.

*Companion: `FRAMEWORK_RESEARCH_PROGRAM_20.md` (the program); `reviews/project01..20_*.py` (the work).*
