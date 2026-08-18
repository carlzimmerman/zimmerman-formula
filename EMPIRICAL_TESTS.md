# The framework's empirical tests — complete ledger

**Framework:** a₀ = κc√(Gρ_Λ) = c²√(Λ/32π) = 9.3619×10⁻¹¹ m/s² (canonical) / 1.1279×10⁻¹⁰ (alt).
κ = ½ **fitted, never derived** (measured 0.529 ± 0.034). Operative arm: **modified gravity**
(MI closed by lensing 2026-08-08). Host: AeST (Skordis & Złośnik, PRL 127, 161302).

Compiled 2026-08-18. Every row names the committed script that produces it. Status grades are
the corpus's own, including the adverse ones.

---

## A. PASSED — tests the framework has already survived

| # | Test | Result | Script |
|---|---|---|---|
| A1 | **Radial acceleration relation**, 175 SPARC galaxies, 3389 points | **0.108 dex** at Υ=0.70 | `real_research/rar_framework_a0_mlfit.py` |
| A2 | **Weak-lensing RAR**, KiDS (Mistele+2024), 40 kpc → 2.2 Mpc | **χ²/dof = 2.03** canonical, **0.94** alt — no dark component, no free parameters | `stage12` |
| A3 | **CMB power spectrum** (CLASS, full Boltzmann) | **0.01σ** vs cosmic variance | `nbody_2026/stage19*`, `stage76` |
| A4 | **Gravitational lensing** γ_PPN | **γ_PPN = 1**, residual 0.601σ (pure-MI predecessor died here at 21.2σ) | AeST lensing chain |
| A5 | **Baryonic Tully–Fisher relation** | passes; also yields κ = 0.465 ± 0.076 | BTFR κ estimator |
| A6 | **GW speed** — GW170817, \|c_T−1\| < 10⁻¹⁵ | **c_T = 1 EXACTLY**, derived not fitted, for *any* free function | `real_research/reviews/c14_dictionary_validity_2026.py` |
| A7 | **Solar-system screening** (exponential kernel) | 1 AU residual ~10⁻³⁴⁵⁷ m/s²; 10³⁴⁴⁵ below Sereno–Jetzer | `opt1_gates_2026.py` |
| A8 | **No-ghost / stability** | theorem-grade for the tensor and scalar sectors | `stage75`, `esc_s_window_2026.py` |
| A9 | **Lyman-α forest** b-cutoff | **0.4–0.9σ** (the "6–8σ exclusion" was a real error of mine, withdrawn) | `project_forest_bcut_correction` |
| A10 | **Small-scale power** — Murgia+2018 α < 0.03 | passes by 1.5×; at the boundary | γ=0 two-field sector |
| A11 | **Lorentz violation** — full SME gravity sector | passes every bound; CPT-even-only theorem | `mi_sme_bridge_2026.py` |
| A12 | **Milky Way vertical force** (full AQUAL on McMillan-2017 baryons) | **+0.2σ**; Eilers rotation-curve slope +1.2σ | vertical-force front |
| A13 | **κ discriminability** vs Milgrom 2020's 1/2π | Δχ² 63.9 vs 154.3 — **favours κ=½ at ~2.2σ** | `project_kappa_discriminability` |
| A14 | **Environmental fork** — ρ_local vs ρ_Λ as the a₀ source | ρ_Λ wins; ρ_local excluded **13–34σ** on 175 SPARC | BIG-SPARC pipeline |

## B. ADVERSE — costs the framework carries, stated at full strength

| # | Test | Result | Script |
|---|---|---|---|
| B1 | **Cassini** Q₂ quadrupole | **3–15σ inherited** — the sharpest standing cost | `mi_mg_arm_standing_2026.py` |
| B2 | **α=1 ephemeris liability** | the *exact* law forces a constant a₀/2 sunward anomaly: **1278×** over the Earth/Mars bound (119–189× post-EFE). Cost = withdraw the word "exact", NOT the phenomenology | `project_alpha1_ephemeris_liability` |
| B3 | **Clusters** | kernel removes 74–89% of the dark matter, **leaves 11–26%**. η at R500 = 1.72–2.08 (kernel-dependent). Not closed | `project_cluster_standing` |
| B4 | **The dust problem (2d)** | the dark sector's excitation is pressureless, collapses; endpoint a black hole, **falsified 5.8×10⁵×** vs Sgr A*. M_lens/M_dyn = 29 at the f=1/3 fixed point | `nbody_2026/` stages 1–9 |
| B5 | **PPN preferred-frame** α₁, α₂ | **ADVERSE** | `c14_ppn_sector_2026.py` |
| B6 | **AeST free function, 𝓕(𝒴) form** | ephemerides need s ≤ 1.27e-5, RAR needs s ≥ 0.435: **gap 1.2–3.4×10⁴** | `typeII_*`, DOI 10.5281/zenodo.22002545 |
| B7 | **SN-Ia host step at a₀** | real 6.9σ mass step reproduced and the step *location* coincidence is real, but decisive tests are **underpowered (18%)** — DISFAVOURED, not excluded | `project_snia_hoststep_a0` |
| B8 | **MUSE-DARK III** a₀(z) | measures a₀ **rising**; canonical (declining) reading WEAKENED + CONTESTED, not falsified | `project_a0z_muse_confrontation` |

## C. LIVE — pre-registered, decidable, not yet decided

| # | Test | Prediction | Decided by |
|---|---|---|---|
| C1 | **Gaia DR4 wide binaries** ⭐ | γ_v ∈ **1.1614–1.1814** canonical / **1.1917–1.2267** alt (Amendment 10, in force). Edge 1.23; no-verdict above 1.26. **Hash-frozen — never modify.** A Newtonian 2–30 kAU result is evidence against at 4.74–7.10σ | Gaia DR4 |
| C2 | **Directional EFE** | Branch-B kill switch, ARMED and **fired once**: Â = +2.95, p = 0.029, AQUAL-class sign. Pure MI predicts exactly zero. Needs N ~ 1157 | larger binary sample |
| C3 | **Comet anisotropy / Oort as an EFE instrument** | the **ν₀-correlated pair with DR4** is the framework-specific signature — neither alone is diagnostic | DOI 10.5281/zenodo.21966646 |
| C4 | **a₀(z) evolution** | a₀ **declines**: MOND is OFF at recombination (0.0060 of today's value), maximum today. **Sharp null: any robust a₀ evolution below z ~ 5 falsifies it** | high-z kinematics |
| C5 | **ν₀ environmental bound** | ν₀ ≤ **2.36×10⁻⁶** — no environmental a₀ variation current data could see | RAR flatness, `stage76` |
| C6 | **BIG-SPARC** | pipeline ready and frozen; data not public | BIG-SPARC release |
| C7 | **Wide-binary shape + √M knee** | the only live axes separating a *fluid* from a *particle* (the CMB constrains a fluid — 0σ both ways, theorem) | `project_particle_vs_mode` |

## D. FUTURE — decisive tests the theory cannot dodge

| # | Test | What kills it |
|---|---|---|
| D1 | **α_M from LISA / Einstein Telescope standard sirens** ⭐⭐ | The strongest prediction in the corpus: **α_M = 0 and c_T = 1 exactly**, for any free function, any K_B, both footings — because J^μ = 0, Z = 0, F_μν = 0 and 𝒴 = 0 hold *identically to all orders* on FRW + a TT mode. **A confirmed α_M ≠ 0 falsifies the entire class in one measurement**, absorbable by no choice of free function |
| D2 | **Binary-pulsar decay across a period range** | Any flux-ledger repair must be **period-INDEPENDENT** (0.16% at 7.75 h, 1.3×10⁻⁴ at 2.45 h); a dipole enters at (c/v)² and cannot be. A period-*dependent* deviation from the GR quadrupole formula excludes the repair |
| D3 | **Any solar-system MOND detection** | excludes the 𝓕(Z) class outright — it predicts 10⁻³⁴⁵⁸·⁷ m/s² at 1 AU, s-independent |
| D4 | **Improved ephemerides** | a coherent residual of the form ϖ̇ = s·a₀√(1−e²)/(na), with one s setting every planet, would *revive* the 𝓕(𝒴) class that B6 killed |

---

## The honest summary

**Passed 14, carrying 8 costs, 7 live, 4 future.** No referee-proof kill exists against the
framework, and no front confirms it decisively either. The single sharpest number in its favour
is the weak-lensing RAR (A2): 40 kpc to 2.2 Mpc with **no dark component and no free parameters**.
The single sharpest cost is Cassini (B1) and the α=1 ephemeris liability (B2). The two problems
that would move the most if solved are the **dust** (B4) and the **free function** (B6) — and
they may be the same problem, since both ask whether a second field can carry the pressure.

**Never say the theory is closed.** Every claim above is reproduced by a committed script; where
a claim was withdrawn it is recorded, dated, in `RETRACTIONS.md`.
