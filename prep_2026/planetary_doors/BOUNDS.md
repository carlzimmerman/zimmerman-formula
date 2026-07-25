# LANE R — Solar-system bounds + prior-work recon (planetary doors)

**Date:** 2026-07-16. **Companion script:** `laneR_bounds_compute.py` (this directory; numpy only; exit 0; every derived number below is printed by it, every measured number carries its citation).

**HONEST CEILING (non-negotiable, applies to everything below):** at planetary accelerations (10⁴–10⁸ × a₀) GR predicts zero anomaly and so, approximately, do healthy MOND-family theories. A solar-system **null discriminates BETWEEN the framework's doors** (A: MG/AeST-class; B: Branch-B elastic medium; C: pure MI kernel), which predict different nonzero residuals — it can **NEVER prove the framework right vs ΛCDM**.

Footings carried throughout: canonical a₀ = 9.36e-11 m/s² (cH_Λ/Z, ρ_DE) and alt a₀ = 1.13e-10 (cH₀, ρ_total).

---

## 1. The measured bounds (real papers, fetched this session)

### 1.1 Cassini / ephemeris EFE quadrupole Q₂ (the sharpest MOND-family observable)

| Measurement | Value (1σ) | 2σ ceiling | Source |
|---|---|---|---|
| Hees, Folkner, Jacobson, Park 2014, PRD 89 102002 | **Q₂ = (3 ± 3)×10⁻²⁷ s⁻²** | 9.0×10⁻²⁷ | [arXiv:1402.6950](https://arxiv.org/abs/1402.6950), Cassini radio tracking, "excludes a large part of the relativistic MOND theories" |
| Park, Hees, Famaey, Desmond, Durakovic 2026 | **Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻²** (40% tighter) | **5.2×10⁻²⁷** | [arXiv:2602.17884](https://arxiv.org/abs/2602.17884), full DE440 dataset, Q₂ fit simultaneously with ephemeris params |

Park+2026 corollaries: MOND boost of the galactic radial acceleration at the Sun ≤ **2% (95% CL)**; RAR-vs-Q₂ discrepancy **3–15σ** depending on MW mass model. Desmond–Hees–Famaey 2024, MNRAS 530 1781 ([arXiv:2401.04796](https://arxiv.org/abs/2401.04796)): AQUAL/QUMOND RAR-vs-Cassini tension **8.7σ fiducial** (1.9σ if bulge galaxies removed); RAR wants a gradual transition, the solar system a sharp one.

Theory values it confronts (Blanchet & Novak 2011, MNRAS 412 2530, [arXiv:1010.1349](https://arxiv.org/abs/1010.1349), Table 1, a₀=1.2e-10, g_e=1.9e-10): Q₂ = 3.8e-26 (μ₁), 2.2e-26 (μ₂ "standard"), 7.4e-27 (μ₅), 2.1e-27 (μ₂₀), 3.0e-26 (μ_exp), 4.1e-26 (μ_TeVeS) s⁻²; range at standard g_e: 2.2e-26 ≲ Q₂ ≲ 4.1e-26 (their eq. 36). Against the Park ceiling these are 7.3×, 4.2×, 1.4×, 0.4×, 5.8×, 7.9× (i.e. +20σ, +11σ, +3σ, +0.3σ, +16σ, +22σ) — only very sharp interpolating functions (μ_n, n>8-ish) survive, which is exactly the DHF24 RAR conflict. The Q₂ dipole is exactly zero (their |Q₁(0)| ~ 9e-14 m/s² numerical noise).

### 1.2 Per-planet anomalous-acceleration bounds (INPOP/EPM)

The modern per-planet numbers are published as 1σ uncertainties on **supplementary perihelion advance** (Fienga & Minazzoli 2024, Living Rev. Relativ. 27:1, [arXiv:2303.01821](https://arxiv.org/abs/2303.01821), Table 10, units **mas/yr**):

| Planet | Pitjeva & Pitjev 2013 (EPM) | Fienga+ 2011b (INPOP10a) | → bound on a constant radial δg [m/s²] (computed, script §1) |
|---|---|---|---|
| Mercury | 0.03 | 0.006 | 4.6×10⁻¹⁴ |
| Venus | 0.016 | 0.015 | 8.0×10⁻¹⁴ |
| Earth | 0.0019 | 0.009 | 8.7×10⁻¹⁵ |
| **Mars** | **0.00037** | 0.0015 | **1.4×10⁻¹⁵** |
| Jupiter | 0.28 | 0.42 | 5.6×10⁻¹³ |
| **Saturn** | **0.0047** | 0.0065 | **7.0×10⁻¹⁵** |

(δg conversion via the Gauss secular-pericenter equation for a constant sunward radial perturbation, orbit-time-averaged; the Saturn value 7.0e-15 reproduces the banked 7.4e-15 "EPM tail sensitivity" used in `branchB_q2_gate_2026/laneB_q2_solve.py` — consistent.) Also Fienga et al. 2018 Mercury 0.02 mas/yr, Park et al. 2017 Mercury 0.015 mas/yr. Older per-planet postfit residuals (BN11 Table 5): Pitjeva 2005 Saturn −6±2 mas/cy; Fienga+2009 Saturn −10±8 (Cassini), **Earth 0±0.016 mas/cy** (Jupiter-VLBI, the tightest of that era); Fienga+2010 (INPOP10a) Saturn 0.15±0.65 mas/cy. FM24 §5 caveat: reading un-refit supplementary-precession residuals as theory bounds is "strongly discouraged" — the direct simultaneous Q₂ fit (H14/P26) is the self-consistent probe.

Monopole/extra-mass gates: Pitjev & Pitjeva 2013 (Astron. Lett. 39 141): ρ_DM(<Saturn) < 1.1×10⁻²⁰ g/cm³; M_extra(<Saturn) < 7.9×10⁻¹¹ M_sun (original paper; the FM24 review text quotes 7.1×10⁻¹¹ — minor discrepancy, both carried).

### 1.3 Mercury / MESSENGER

Genova et al. 2018, Nat. Commun. 9:289 ([link](https://www.nature.com/articles/s41467-017-02558-1)), 7 yr of MESSENGER ranging: Nordtvedt **η = (−6.6 ± 7.2)×10⁻⁵**, **J₂☉ = (2.246 ± 0.022)×10⁻⁷**, |Ġ/G| ≲ 4×10⁻¹⁴ yr⁻¹, Mercury ephemeris good to **< 1 m**. FM24 data table: MESSENGER radio-science range accuracy **5 m** (2011.2–2014.3). Park et al. 2017 (AJ 153:121) perihelion-precession method: Mercury 0.015 mas/yr.

### 1.4 Jupiter / Juno

FM24 data table: **Juno radio-science range 20 m** (2016.65–2020.56); Juno VLBI 0.5 mas. INPOP19a was the first to ingest Juno (9 positions) + Cassini extension 2014–2017 ([INPOP19a, Fienga et al. 2019](https://ui.adsabs.harvard.edu/abs/2019NSTIM.109.....F/abstract)); INPOP21a added 1 more year of Juno normal points + Gaia-DR3-reduced Uranus ([INPOP21a](https://ui.adsabs.harvard.edu/abs/2021NSTIM.110.....F/abstract)). Jupiter remains the weakest inner-ephemeris planet (0.28–0.42 mas/yr perihelion σ → δg ~ 6×10⁻¹³ m/s²).

### 1.5 LLR

Biskupek, Müller, Torre 2021, Universe 7:34 ([arXiv:2012.12032](https://arxiv.org/abs/2012.12032)): **Ġ/G = (−5.0 ± 9.6)×10⁻¹⁵ yr⁻¹**, EP **Δ(m_g/m_i)_EM = (−2.1 ± 2.4)×10⁻¹⁴**, β−1 = (6.2 ± 7.2)×10⁻⁵, γ−1 = (1.7 ± 1.6)×10⁻⁴; mm-class normal points (APOLLO, OCA-IR).

**MOND-EFE on the lunar orbit (computed, script §4):** at the Park+2026 ceiling the EFE quadrupole gives Δ₂(Moon) ≈ 3×10⁻⁴ mas/cy and a range-displacement scale (Q₂/n²)·a ≈ **3×10⁻⁴ mm** — four orders below LLR's mm accuracy. **LLR is not the Q₂ lane; Cassini/ephemerides win by ~10⁴.** Conversely the *naive constant-tail landmine* (below) leaves an O(1–2 cm) synodic-period range signature via the direction-differential a₀/2·(a_moon/AU) ≈ 1.2–1.5×10⁻¹³ m/s² — at LLR's cm residual level, so LLR *independently* disfavors the naive tail, but the planetary perihelion bounds are 3–4 orders stronger and are the load-bearing exclusion.

### 1.6 The Blanchet–Novak 2011 predictions (what they actually are)

BN11 Table 3 (mas/cy, at their Q₂ values): Saturn **5.39 (μ₁) / 3.12 (μ₂) / 4.25 (μ_exp) / 5.81 (μ_TeVeS) / 0.3 (μ₂₀)**; Uranus up to −10.94; Neptune up to 8.56; Earth 0.16; Mercury 0.04. Octupole precessions are μas/cy-level (negligible). Milgrom 2009 (MNRAS 399 474): −q ~ 0.01–0.3, anomalous acceleration ~10⁻⁵a₀ (inner planets) to ~10⁻⁴a₀ (Saturn), Saturn precession ~1.8 mas/cy for sharper μ.

**⚠ TRAP (mis-attribution in the tasking):** Blanchet & Novak 2011 contains **NO lunar-orbit / LLR prediction** — verified by keyword-scanning the full MNRAS 412 2530 PDF and the Moriond proceedings (arXiv:1105.5815): zero mentions of Moon/lunar/LLR/laser. Their tables are planets-only. Any "BN11 MOND-LLR amplitudes" cited anywhere are confabulated; lunar-EFE numbers must be derived by scaling (as in script §4) or taken from other papers.

---

## 2. The landmine, with its published wall

The framework's own ν(y) = √(1+1/y) has tail ν−1 → 1/(2y), so a **naive algebraic circular-orbit reading predicts a constant sunward anomalous acceleration a₀/2 = 4.68×10⁻¹¹ (canonical) / 5.65×10⁻¹¹ (alt) m/s² at every planet.** Published support that this class is dead — Blanchet & Novak 2011 (arXiv:1105.5815, p. 8), for the equivalent μ ~ 1−1/y tail: *"predicts a constant supplementary acceleration directed toward the Sun δg_N = a₀ (i.e. a 'Pioneer' effect), which is ruled out because not seen from the motion of planets."*

Computed per-planet exclusion of a₀/2 (script §1, from Table 10 σ's):

| Planet | δg bound [m/s²] | a₀/2 excluded by (canon / alt) |
|---|---|---|
| Mercury | 4.6e-14 | 1008× / 1217× |
| Earth | 8.7e-15 | 5382× / 6498× |
| **Mars** | **1.4e-15** | **34 000× / 41 000×** |
| **Saturn** | **7.0e-15** | **6712× / 8103×** |

So whatever kills the tail must kill it by ≥ 10³·⁸–10⁴·⁵. Door A kills it via the EFE/nonlinear Poisson (→ the Q₂ tension). Door C must kill it via the kernel's high-frequency/high-a response — **that computation (do the published Herglotz + sum-rule + causality constraints FORCE the suppression at planetary frequencies?) has never been done by anyone and is the center of this workflow.** Milgrom 2009 (p. 2) states the MI folk-expectation to be tested: in non-local MI formulations anomalies attach to trajectories that reach low-acceleration regions (long-period comets, Pioneer), *"without affecting the motions of planets, whose orbits are wholly in the high acceleration regime"* — an expectation, not a theorem; the framework's kernel is the first concrete object it can be checked on.

---

## 3. Prior committed work — what it already computed (all re-run this session, exit 0)

**`real_research/reviews/cassini_quadrupole_framework.py`** (repo, read-only; re-run OK): order-of-magnitude grounding of the DHF tension. g_ext = V²/R = 2.146e-10 m/s² (V=233 km/s, R=8.2 kpc); MOND boost at the Sun: canonical-1.2e-10 → 35.6% (RAR ν) / 40.0% (simple); framework 0.936e-10 → **19.8% on the FRAMEWORK'S OWN ν = √(1+1/y)** (28.2% / 32.8% are McGaugh's RAR / simple fitting functions, **reference values only** — RULE-1 FIX 2026-07-25, flagged F1 by `AUDIT_rule2_foreign_a0_bounds_2026.py`; the 28–33% figures had propagated here as if they were the framework's) — all ≫ the 2% Cassini allowance, so the wall stands on the corrected number (9.9×). Verdict text: framework's lower a₀ helps marginally, does not clear; the AeST realization is MG-class and inherits; MI escape "belongs to a different realization" (superseded by the two scripts below, which built exactly that MI computation).

**`real_research/reviews/cassini_mi_q2_saturn_2026.py`** (untracked; re-run OK): the MI-side derivation at Saturn through the validated non-local kernel A_eff = a_int + θ(y)a_ext (θ₀=√2 forced core, bracket 2). Findings: (i) frequency mapping — the static galactic field appears in the orbit frame as harmonics y_k = k, with k=1 unmodified, k=2 down-weighted; (ii) leading MI secular "Q2-scale" 2.7e-29 (canon) / 3.3e-29 (alt) s⁻² = 0.005–0.006× the Park ceiling, 0.015–0.018σ; (iii) DC-protection holds — θ(k≥2) residual ~5e-35 s⁻² (fraction of the secular quadrupole in θ-touchable harmonics: 3.8e-6); robust across e=0–0.5, all φ_gc, a_ext = 2.0–2.48e-10, both footings.

**`real_research/reviews/cassini_mi_evasion_2026/`** (verify_order.py re-run OK + the banked MD): the corrected multipole bookkeeping. The 2.7e-29 headline above is the **l=1 dipole** scale (first order in a_ext, power 1.000, analytic match a₀a_ext/(2a_int) = 1.55e-16 m/s²); the **true l=2 quadrupole is second order (power 2.22): 7.4e-34 s⁻² ≈ 10⁻⁷× the ceiling**. Load-bearing suppression = deep-Newtonian ν−1 = a₀/(2a_int) = 7.1e-7 at Saturn (forced by the framework's ν, not by kernel tuning). Verdict banked: MI core EVADES; explicitly NOT a general clearance — it holds **at the quasistatic-MI premise** and the covariant MI completion must reproduce it. Gap the landmine targets: this work suppressed the *anisotropic EFE response*; it never computed whether the kernel kills the *isotropic a₀/2 tail* at planetary (a, ω) — the θ(y) kernel used here is the eccentricity/EFE memory kernel, not the published Herglotz K(□_u).

**`real_research/reviews/branchB_q2_gate_2026/`** (decider_q2_crosscheck.py re-run OK, ~3 min): Branch B's own Q₂ via the corrected Milgrom/Desmond eq-(12) kernel (no /√D; calibrated 1.033 on Desmond's published anchors q(1)=0.094, q(1.5)=0.159, q(2)=0.221) + an independent 2-D BVP solver (laneB, agreement <3%). Results (worst g_ext corner 1.9–2.6×a₀, both footings): framework-ν reference **2.50e-26 canon / 3.31e-26 alt = 4.8× / 6.4× ceiling (+13σ / +17.5σ)** — the number Door A inherits; scalar sharp-screen family squeezed — pow p=8 (SPARC winner) FAILS Q₂ ×1.6–2.1; delta d=6 passes Q₂ (1.5–1.9e-27) but fails SPARC canonical (needs Υ=0.83–0.85 > Spitzer edge); **pow p=6 yt=1.0 survives by a needle on canonical only** (4.65e-27 = 0.9× ceiling; alt ×1.19 marginal-FAIL). The elastic two-invariant route (laneC) evades Q₂ by shear-linearity (w ≲ 0.2) at the price of underived posits P5/P6 — the Branch-B w-reduction gate (`vector_elastic_w_2026/synth.py`, re-run OK): natural β=2/7 (w=0.304) **FAILS Q₂ ×1.32–2.69** on every footing/κ_t corner; passing needs β ≥ 0.416 (canon, κ_t=0.5; central band 0.356–0.476) up to β ≥ 1.19 (alt, κ_t=1.0), i.e. outside the natural window [0.18, 0.33]; even the most-favorable admissible corner (β=0.333, κ_t=0.5, canon Q₂-low) is 1.05× ceiling.

**`agentY_quasistatic.out` + `reviews/mi_formal_completion_2026/`** (read-only): the kernel/covariant arc context — lens-only slip sector quasistatics (c_T=1 identically, FRW quietness a_μ=0, slip formulas after branch conditions), one/two-loop dS structure, operator definition of K(□_u) (Herglotz–Nevanlinna, ‖K‖≤1, causal-retarded, v11 sum rule ∫dμ/|t|=1). **Nothing in it evaluates K at planetary frequencies** — confirming the landmine computation is genuinely un-done.

**`prep_2026/mi_fingerprint/`**: empty at recon time (its RB lane's KERNEL_THEORY.md does not exist yet); nothing to import — planetary results here must be derived independently, per the ground rules.

---

## 4. Scoreboard entering the landmine calculation

| Door | Inner-SS status | Number |
|---|---|---|
| A — MG/AeST (own ν) | **WALL, inherited** | Q₂ = 2.5–3.3e-26 = 4.8–6.4× Park ceiling (+13 to +17.5σ); boost 28–33% vs 2% allowed |
| B — Branch-B elastic | **needle / posit-dependent** | scalar route: one marginal thread (canonical only, 0.9× ceiling); vector-elastic natural β=2/7 FAILS Q₂ ×1.3–2.7, pass needs β≥0.42–1.19 (outside natural [0.18,0.33]); elastic two-invariant route safe only via P5/P6 |
| C — pure MI (quasistatic) | **EVADES (derived)** | true l=2: 7.4e-34 ≈ 10⁻⁷× ceiling; dipole scale 1.5e-28 = 0.03× | 
| C — pure MI (dynamic kernel) | **UNCOMPUTED — the landmine** | must suppress a₀/2 = 4.7e-11 by ≥ 3.4×10⁴ (Mars) / 6.7×10³ (Saturn) at planetary (a, ω) |

If the published kernel constraints force the suppression → the Cassini/ephemeris null becomes evidence *preferring Door C over Door A within the framework* (never over ΛCDM). If they cannot → the MI door takes a real, quantified solar-system hit at the table-2 level, and that gets reported straight.
