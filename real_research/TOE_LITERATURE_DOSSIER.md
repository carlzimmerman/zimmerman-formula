# Emergent-Horizon TOE — Literature Dossier

**The organized reading list behind `TOE_EMERGENT_HORIZON.md`, with a one-line honest status for each paper.**
*Compiled June 2026. Tag key: ✅ supports a pillar · ⚠️ challenges / open · ⚔️ contested · 🔭 the framework's own.
Every entry is a real, published (or arXiv) paper; the **unification** of them is the conjecture, not any single
result.*

---

## A. Emergent / thermodynamic gravity (the foundation — Pillars 1–2)

- **Jacobson 1995**, *Thermodynamics of Spacetime* (gr-qc/9504004) — ✅ Einstein's equation = δQ=TdS on local
  Rindler horizons. The cornerstone: gravity has thermodynamic structure.
- **Padmanabhan 2010**, *Equipartition of energy in the horizon DOF and Newton's law*; *Emergence of Cosmic
  Space* (arXiv:1206.4916, 1207.0505) — ✅ cosmic expansion = drive to holographic equipartition (N_bulk =
  N_surface at the Hubble radius); S=E/2T + equipartition → Newton + Friedmann.
- **Padmanabhan / Senovilla, MOND from equipartition** (arXiv:1410.3433, 1511.02108) — ✅ a₀ = cH₀ appears
  naturally; the MOND-modified Friedmann eq. follows from emergent gravity. (Pillar 2.)
- **"MOND Theory and Thermodynamics of Spacetime"** (arXiv:2510.14345, 2025) — ✅ recent restatement linking
  MOND to spacetime thermodynamics.
- *Critique:* Gao, *Is Gravity an Entropic Force?* (arXiv:1002.2668) — ⚠️ argues entropic-gravity derivations
  are not watertight; the thermodynamic structure may be compatible with gravity being fundamental.

## B. The a₀–cosmology connection (Pillar 6, the link)

- **Milgrom 2020**, *The a₀–cosmology connection in MOND* (arXiv:2001.09729) — ✅🔭 a₀ ~ cH₀ ~ c²√Λ; the
  "FUNDAMOND" conjecture that **MOND and dark energy are the same action term controlled by a₀**. The keystone
  for the DESI cross-prediction. **(The "same term" is conjecture.)**
- **"A Fundamental Scale for Acceleration from the Holographic Principle"** (physics/0505175) — ✅ a₀ from the
  holographic principle.

## C. Verlinde emergent gravity / the dark sector (Pillar 3)

- **Verlinde 2017**, *Emergent Gravity and the Dark Universe* (arXiv:1611.02269, SciPost Phys. 2,016) — ✅🔭 de
  Sitter volume-law entanglement entropy; matter displaces it → elastic "dark" response = MOND for a point
  mass. The closest published cousin to this framework.
- **Hossenfelder, A Covariant Version of Verlinde's EG** (arXiv:1703.01415) — ✅ covariant completion.
- **Verlinde EG vs dwarf spheroidals / clusters** (arXiv:1612.06282) — ⚠️ fails at clusters by ~2×; the Zwicky
  residual survives. (The "relocated dark matter" honesty.)

## D. DSSYK / de Sitter holography — the microscopic dual + matter element (Pillar 4)

- **Berkooz, Narayan, Simon**, *Chord diagrams, exact correlators in spin glasses…* (arXiv:1806.04380) — ✅🔭
  the exact DSSYK 2-point function from chord combinatorics. The matter-element foundation.
- **Okuyama 2023**, DSSYK matter two-point function (eq. 18 used in `project04e/04f`) — ✅🔭 the exact element
  the framework's sign-derivation rests on; q→1 → Schwarzian (verified analytically + numerically in-repo).
- **Narovlansky–Verlinde 2023**, *Double-scaled SYK and de Sitter holography* (arXiv:2310.16994; JHEP 05 2025
  032) — ✅🔭 de Sitter = pair of DSSYK at infinite temperature (the *center* / flat-DOS reading the framework
  uses); 2-pt fn = massive scalar Green's fn in 3D dS. **Load-bearing assumption.**
- **DSSYK chords and de Sitter gravity; SYK correlators from 2D Liouville–dS gravity** (JHEP 03 2025 076; JHEP
  05 2025 053) — ✅ independent confirmations the DSSYK correlator = 3D dS massive-scalar Green's fn.
- **Rahman–Susskind**, *The Many Temperatures of de Sitter Space* (arXiv:2401.08555) — ⚠️🔭 four discrete
  temperatures + a Tolman blue-shift; questions the single-"infinite-temperature" center reading. Both a threat
  to the sign-closure's foundation and the source of the interpolation-broadening + two-horizon fixes.
- **Aguilar-Gutierrez**, *Deforming DSSYK & Reaching the Stretched Horizon from Finite Cutoff* (arXiv:2602.06113,
  Feb 2026); *de Sitter JT from DSSYK* (arXiv:2505.08116) — ✅ T²-deformations move the dual off exact de
  Sitter toward the stretched horizon — the first tool for an **evolving-Λ dual** (the key open problem).

## E. Dark energy from generalized horizon entropy → evolving DE (Pillar 5, the DESI bridge)

- **Modified cosmology through generalized mass-to-horizon entropy** (arXiv:2406.17301, 2508.13260) — ✅ a
  non-area-law horizon entropy → effective dark energy with a *dynamical* EOS (quintessence/phantom).
- **Barrow / Tsallis holographic dark energy vs DESI DR2** (arXiv:2504.12205, 2506.03019, 2601.02567) — ✅
  generalized-entropy DE fits the DESI DR2 BAO evolving-DE signal. **(That DSSYK *specifically* gives the DESI
  w(z) is the conjecture.)**

## F. DESI — the evolving dark energy result

- **DESI DR2 2025** BAO + CMB + SNe — ⚠️ evolving DE (w₀ > −1, wₐ < 0) preferred over Λ at **2.8–4.2σ**
  (SNe-dependent: Pantheon+, Union3, DES-Y5). Berkeley Lab / arXiv:2503.xxxxx + many follow-ups (2508.10514,
  2512.07281). **Not settled; could revert to Λ.** Turns a₀(z) into a prediction (`project_desi_a0z_crossprediction.py`).
- DESI 2024 full-shape: Ωm ≈ 0.296, σ8 ≈ 0.84; Σmν < 0.071 eV — ⚠️ tight; constrains modified-gravity growth.

## G. Local MOND tests (Layer 3 — is MOND real)

- **Chae et al. 2020**, *Detection of the External Field Effect* (arXiv:2009.11525) — ✅🔭 EFE detected 8–11σ in
  strong-field "golden" galaxies, >4σ blind across 153 SPARC. The strongest local signature; SEP-violating, no
  ΛCDM analogue. **Top in-repo to-do: re-verify independently.**
- **Lelli et al. 2016/2017**, SPARC + the RAR (arXiv:1606.09251) — ✅ the tight radial acceleration relation;
  the data the derived interpolation matches to ~6% (`precision_rar_test.py`).
- **Wide binaries (Gaia DR3):** Chae 2023–2025, Hernandez 2022–2024 (arXiv:2402.xxxxx, ApJ adce09/ad61e9) —
  ⚔️ find a ~40% low-acceleration boost (MOND) beyond ~3 kAU. **vs** Pittordis–Sutherland 2023, Banik et al.
  2024 (MNRAS 533,729) — ⚔️ find GR preferred at high significance. **Genuinely contested; methodological
  (contaminants, sample selection). Could be decisive either way.**

## H. The a₀(z) rate question (high-z — the framework's central bet)

- **MUSE-DARK III 2026** (A&A; arXiv:2604.22613) — ⚔️ RAR a₀(z)=1.0+1.59z, *faster* than H(z) (rising). The
  main support for a rise; indirect RAR fit.
- **Naidu/Weibel et al. 2025**, the *Big Wheel* z=3.25 disk (arXiv:2409.17956; Nature Astron.) — ⚔️🔭 a₀^eff ≈
  local; excludes a ×5 rise (`project_highz_bigwheel_a0.py`). Direct disk.
- **Milgrom 2017**, *High-redshift rotation curves and MOND* (arXiv:1703.06110) — ⚔️ z~2 disks at g=(3–11)a₀;
  "all but excludes ~4a₀ at z~2," kills a₀∝(1+z)^1.5.
- **Nestor Shachar et al. 2023 (RC100)**, **Genzel/Lang 2017**, **Übler 2017 (KMOS³ᴰ)** — ⚔️ massive high-z
  disks baryon-dominated, declining RCs (upper bounds; ~local a₀).
- **TF at 0.6<z<2.5** (arXiv:2406.08934, 2024) — ⚔️ faster V at fixed M_bar → mild rise. *Contested sign.*
- *Net:* strong ∝E(z) rise disfavored; mild rise / mild decline (DESI event-horizon branch) alive. See
  `project_highz_a0_synthesis.py`, `project_a0z_rate_theory.py`.

## I. Relativistic MOND cosmology + structure formation (the open completion)

- **Skordis–Zlosnik AeST** (arXiv:2007.00082; quasistatic 2304.05134) — ⚠️ fits CMB + low-z P(k) via a
  dust-like K(Q) mode (the relocated Ω_DM≈0.27); but cross-scale parameter tension.
- **"Consistent structure formation on all scales in relativistic MOND"** (arXiv:2303.00038) — ⚠️ MONDian
  galaxies ≠ MONDian cosmology; the scales can decouple (evades some constraints, not a single clean theory).
- **CMB third peak** — ⚠️ favors CDM ~200:1 over no-CDM models; AeST survives only via the dust mode. Structure
  forms too late (z<5), as in ΛCDM. **The cosmological completion is genuinely unfinished.**

## J. Clusters (where MOND/EG fails)

- **Sanders 2008**, *X-ray group & cluster mass in MOND* (MNRAS 387,1470) — ⚠️ unexplained mass ~factor 2,
  worse in cores. **Eckert+2022 (X-COP, arXiv:2205.01110)** — clusters near the galaxy RAR with careful gas;
  magnitude method-dependent. **Chae+2020 (CLASH), Tian+2024** — cluster RAR a₀ ~10× galaxy.
- *In-repo:* `project_cluster_erass1_a0z.py` — eRASS1 R500 masses reproduce the factor-2 but cannot test a₀(z)
  (overdensity kinematics); needs resolved profiles.

---

## One-screen status of the program

| Pillar | Best support | Honest status |
|---|---|---|
| Gravity = horizon thermo | Jacobson, Padmanabhan | ✅ structural, widely accepted |
| a₀ ≈ cH₀ scale | Padmanabhan equipartition | ✅ scale solid; coefficient open |
| DM = MOND (Verlinde) | Verlinde 2017 | ⚠️ fails clusters ×2; covariant version strained |
| **DSSYK sign + interpolation** | Okuyama, Narovlansky–Verlinde | 🔭 the new piece; ✅ lit-verified; ⚠️ center-assumption |
| DE from generalized entropy | Barrow/Tsallis + DESI | ✅ mechanism; ⚠️ DSSYK-specific is conjecture |
| a₀ ~ c√Λ link + DESI cross-pred | Milgrom + DESI DR2 | ⚠️ conjecture-dependent but falsifiable |
| MOND is real (local) | EFE 8–11σ | ✅ EFE strong; ⚔️ wide binaries contested |
| a₀ rises ∝ E(z) | MUSE-DARK III | ⚔️ disfavored by high-z disks; mild rise/decline alive |
| Cosmological completion | AeST | ⚠️ CMB ok via dust mode; structure/third-peak open |

**Bottom line:** every row is published physics; the framework's distinctive contribution is one row (the DSSYK
sign + derived interpolation); the unification across rows is the open conjecture; and the program is now
anchored to a live cosmological measurement (DESI) with a sharply falsifiable a₀(z) cross-prediction. Not a
finished TOE — a real, falsifiable, *organized* research program.
