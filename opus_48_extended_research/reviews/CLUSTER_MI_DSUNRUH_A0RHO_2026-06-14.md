# The framework's OWN cluster prediction: modified inertia (dS-Unruh) + the a0=(c/2)√(Gρ) angle — VERDICT (2026-06-14)

**Grade: NO-SAME (framework MI gives the same ~2×, marginally WORSE +12–13%). Angle grade: BREAKS-GALAXY-RAR.**
Code: `cluster_MI_dsunruh_a0rho.py` · Data: real eRASS1 (Bulbul+2024), N=9830 clean, WL-calibrated M500, median z=0.30.

## The question (correctly framed by Carl)
Prior cluster calcs computed normal MOND (universal-constant a0 + standard ν + AeST modified-**gravity** → η~2.15).
That is NOT the distinctive Zimmerman physics. The framework is **modified INERTIA** from the de Sitter–Unruh
temperature `T_eff = (ħ/2πckB)√(a²+(cH)²)`, with a0 DERIVED from ρ_DE. Milgrom proved MI ≠ MG for **non-circular /
pressure-supported** systems (they coincide only for circular orbits). Clusters are pressure-supported (σ~1000 km/s)
— the one place MI and MG can diverge. **Does the framework's own physics reduce the cluster deficit?**

## What was computed (load-bearing, on real eRASS1)

**PART A — the MI virial relation for pressure-supported systems (the genuine MI distinctive).**
Milgrom's MI deep-MOND virial relation is `⟨V²⟩² = (4/9) M G a0`; the MG general virial theorem
(Milgrom 2014, arXiv:1311.2579) is `Σ rₚ·Fₚ = −(2/3)√(Ga0)[(Σm)^{3/2}−Σm^{3/2}]`. For a one-mass-scale isothermal
system **both reduce to the SAME deep-MOND mass `M_dyn = (9/4) σ⁴/(G a0)`** — verified numerically identical
(MI/MG = 1.0000 at σ=1000 km/s). The integrated virial mass descends from a0 + space-time scale invariance, which MI
and MG **share**. The real MI distinctives (a *stronger* external-field effect; the algebraic g_obs=ν(g_bar/a0)g_bar
being *exact* in MI, only approximate in MG; orbit-shape factors) are sub-leading O(1) and **do not touch η(R500)**.

**PART B — the full dS-Unruh floor (cH=5.79 a0) inside the √ is MOOT at R500.** 96% of eRASS1 clusters sit at
g_bar/a0_F ≤ 0.1 (median 0.037) — **deep MOND**, where every kernel → 1/√y. Normalizing every interpolation
(dS-Unruh/simple, McGaugh RAR, standard algebraic) to the SAME deep-MOND a0=a0_F gives **η = 2.149 / 2.153 / 2.149**
— shape-independent to <0.5%. The floor matters only in the transition/Newtonian regime, not at R500. (Note: the
task's "g_bar/a0~0.06, transition" describes the mildest clusters / the core; the median R500 is deeper.)

**PART C — η(R500) on real eRASS1:** framework-MI dS-Unruh (a0=9.36e-11) → **η = 2.149** [IQR 1.99–2.54];
regular MOND (a0=1.20e-10, same simple ν) → η = 1.921 [IQR 1.78–2.27]. Ratio = √(a0_M/a0_F) = **1.132 (exact,
ν- and baryon-independent)** — the framework is **+12–13% WORSE** because its a0 is lower (η ∝ 1/√a0). Against the
task's stated normal-MOND/MG **η~2.15**, the framework-MI is **the same value, very slightly higher**. (The 2.15 vs
1.92 gap is just which a0 the "2.15 baseline" used — at 9.36e-11 the dS-Unruh number IS 2.15.)

**PART D [THE ANGLE] — a0 = (c/2)√(Gρ): is cluster a0 really 9.36e-11?**
- **D1 (rho_local-matter RULED OUT):** a galaxy disk's local matter density ρ~1e-21 kg/m³ is ~1e6× ρ_DE, giving
  a0 ~ **1000× too big** (1.0e-7). The universal galaxy RAR (0.13-dex tight, seen across orders of magnitude of local
  density) would scatter by ~√ρ ~ 100–1000×. **Decisively breaks galaxies.**
- **D2 (no scale-blind reading helps clusters):** every density argument that raises cluster a0 also raises
  (inner-)galaxy a0:
  - **R1 (ρ_eff = ρ_DE + ρ_local):** cluster total ρ inside R500 (median 6.2e-24) is ~1069× ρ_DE → a0 up 33× — but the
    same rule raises a galaxy outskirt (ρ~1e-22) a0 by 131× and the inner galaxy (ρ~1e-21) by 414×. **Breaks the RAR.**
  - **R2 (local de Sitter horizon):** a0 comes from the *cosmological* Λ (global dS horizon), not a local field; the
    cluster's matter curvature G ρ/c² ~ 4.6e-51 m⁻² does dwarf Λ~1.1e-52 — but that IS the ρ_local reading (R1), and
    in GR the cluster's own curvature is just Newtonian gravity (already in g_bar), not a new a0. **Collapses to R1.**
  - **R3 (inverse):** closing η=2.15→1 needs a0_cluster ~ 4.6× a0_F, i.e. ρ ~ 21× ρ_DE — between ρ_DE and the
    cluster's own density, with NO scale-blind law that gives exactly 21× in clusters and 1× in galaxies.
  - **R4 (The & White's "clusters need 4× a0"):** in the framework that's a0_cl/a0_F ~ 4–5.4× = √-restatement of
    η~2.0–2.3 — a relabel of the deficit, not an independent ρ.

## Verdict (both ways, no manufactured cure)
- **reduces_deficit = NO-SAME** (in fact NO-WORSE by +12–13%, the exact √(a0_M/a0_F) penalty). The framework's
  distinctive MI/dS-Unruh physics does **not** rescue clusters. MI ≠ MG is real for pressure-supported systems, but
  the divergence is sub-leading O(1) and **does not appear in the integrated R500 mass**, which both formulations set
  by the SAME deep-MOND virial law M=(9/4)σ⁴/(Ga0). The lower a0 makes clusters marginally HARDER.
- **vs normal-MOND/MG:** essentially identical η (2.15 at matched a0); +12–13% larger only because a0 is lower.
- **angle = BREAKS-GALAXY-RAR:** no density reading raises cluster a0 without breaking the universal galaxy a0. The
  galaxy RAR is the hard constraint — it pins a0 to a single value compatible with ρ_DE, uniform.
- **GATED?** The MI prediction is itself **UNGATED** — there is no CMB-safe covariant MI theory (the X2 theorem /
  the trilemma: of {Cassini-safe, a0(z)-natural, CMB-safe} no MI realization holds all three). So this null is the
  prediction of an *unbuilt* MI theory, computed in the deep-MOND-limit form that MI and MG provably share. The
  covariant realization the framework actually uses (AeST modified gravity) was tested separately and also predicts a
  deficit, not a cure (`CLUSTER_CLOSING_CALC_VERDICT_2026-06-14.md`).

**Bottom line:** the cluster ~2× is a shared-MOND liability the framework INHERITS; neither modified inertia
(this calc) nor the AeST mass term (prior calc) supplies it from first principles, and the framework's lower a0
makes it +13% harder, not easier. Reported straight. Quarantine held: a0/Z flagged posited, never asserted derived.
