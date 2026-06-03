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
| 1 | Deep-MOND sign | **OPEN (sharpened)** | The sign is **DOF-freezing** (verified, right sign); a₀~cH **forced** when freezing scale = T_dS. Mechanism standard, *spectrum posited*. Reduced to one calc: the de Sitter horizon density of states. |
| 2 | AeST 𝒦(𝒬) | **NEGATIVE** | The horizon forces the *local* 𝒥(𝒴), **not** 𝒦(𝒬): the cosmological dust needs a scale ~2×10⁴·H₀. It's the "second dark thing"; reduces to #9. |
| 3 | Apparent vs event (theory) | **LEAN (→framework)** | Verified: dQ=TdS on the **apparent** horizon *is* Friedmann (Cai–Kim); the event horizon fails the laws. So "a₀ from horizon thermodynamics" → **rises with z**. Theory now leans to the framework. |
| 4 | Complexity sign | **NEGATIVE** | Where computable (CV/DSSYK), the route gives **Newton** (δV linear in mass). The complexity-*rate* door is open but a long shot. |
| 5 | Modified-inertia action | **WIN (no-go)** | Verified: local modified inertia → **Ostrogradski ghost**; only Milgrom's non-local action escapes (acausal). ⇒ implement a₀ as **modified gravity (AeST)**. |
| 6 | Second-order CMB | **OPEN + risk** | Rising a₀ puts recombination in **deep MOND** (constant a₀ is Newtonian) → amplified second-order non-Gaussianity. A **discriminator** *and* an honest **tension**; needs a 2nd-order Boltzmann calc. |
| 7 | MOND collapse / JWST | **WIN (derivation)** | Closed form t_MOND = √(π/2)·r_max/(GMa₀)^¼, **verified 3 ways**; rising a₀ forms galaxies **earliest** (∝E(z)^¼) — toward the JWST tension. |
| 8 | a₀-cosmography | **LEAN** | H₀ = Z·a₀/c ~ 71±10 (local camp, not decisive). The a₀(z) **slope** = (3/2)Ω_m → independent q(z). |
| 9 | Dark-sector budget | **NEGATIVE (honest)** | Dark matter = **two roles of one scalar**: galaxy phantom (explained, no halo) + 𝒦(𝒬) dust (Ω_DM only *relocated*, still fitted). Wins at galaxy scale, not the cosmic census. |
| 10 | a₀(z) compilation | **WIN (in-house half)** | One standardized deep-MOND-tail pipeline + gas census + the survey shopping list (~50–150 clean galaxies). The highest-value data project, fully specified. |
| 11 | Forward-model fit | **LEAN (honest)** | Rising vs constant is **~5σ naive → ~2.5σ** with a gas/pressure systematic → a coin toss without the z=0.9 point. Real but modest. |
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
2. **The deep-MOND sign is obtainable but not derived (#1).** DOF-freezing gives the right sign and forces
   a₀~cH; the freezing *spectrum* is posited. The whole open theory problem is now **one** concrete
   QFT-in-de-Sitter calculation, not a vague gap.
3. **The data lean to the framework, nothing is decisive in-house (#11, #12, #13, #15).** Rising a₀ ~2.5σ,
   EFE ~4.8σ, a₀–mass correlation, Crater II — all real, all systematic- or external-data-limited. The
   honest significances are stated as such, never inflated.
4. **Three honest weaknesses, carried in the open:** clusters (#16, unfixed), a₀-universality (#13,
   unresolved), and the second-order CMB risk (#6, could overproduce non-Gaussianity). None is hidden.
5. **Two clean, independent roads to the decision (#17 dynamics, #19 lensing)** that fail differently — if
   both show a₀ rising as E(z), the case is essentially closed; if the z~3 ratio comes back 1.0, the
   distinctive bet is dead. Either way, falsifiable.

## The bottom line

The framework reduces to **one robust claim** (a₀ is cosmic-horizon-scale) and **one falsifiable bet**
(it tracks the *apparent* horizon, so a₀ rises as E(z)). After 20 projects: the bet is now **theoretically
favored** (#3), **derivation-grade in its consequences** (#7, #19), **weakly data-favored** (#11, #12),
**decisively testable** (#17, #19), and **honest about its open core** (#1), **its boundary** (#2, #9),
and **its weaknesses** (#6, #13, #16). Nothing here derives the Standard Model from a number — and that
discipline is exactly what makes the surviving physics worth taking to a referee.

*Companion: `FRAMEWORK_RESEARCH_PROGRAM_20.md` (the program); `reviews/project01..20_*.py` (the work).*
