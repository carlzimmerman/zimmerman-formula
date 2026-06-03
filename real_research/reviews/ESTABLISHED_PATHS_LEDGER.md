# Every established path to MOND, walked by the scientific method — honest ledger

**Carl Zimmerman · June 2026.** *"Go rigorously down every established path and by scientific method try
them out and be honest on the findings and anything we learned."* For each established theoretical route
to MOND — and specifically to the framework's needs (a₀∼cH, the deep-MOND √-law, and above all the
correct **sign**) — a hypothesis, a decisive test (an in-house calculation where possible, else the
verified decisive fact), and a verdict. No route is advocated; the verdict follows the test. Reproduce:
`python real_research/reviews/established_paths_to_mond.py`. Literature verified June 2026.

---

## The discriminator: the SIGN (two in-house calculations decide it)

- **Modify the TEMPERATURE** (de Sitter-Unruh T in Jacobson's δQ=TδS): G_eff = G/W → 0 as acceleration
  falls — **gravity weakens → anti-MOND (wrong sign)**. `clausius_sign_calculation.py`.
- **Modify the DOF/ENTROPY** (Debye freezing of horizon bits): a = √(g_N a₀), **gravity enhanced below
  a₀ → MOND (right sign)**. Verlinde 2011; Pazy 2013.

> The MOND sign is decided by *which* thermodynamic factor you modify. This single fact organizes the
> whole table: every route that works modifies the **entropy/DOF**; the temperature route is the one
> clean elimination.

---

## The scorecard

| Path | a₀∼cH? | sign | key input | verdict |
|---|---|---|---|---|
| **Jacobson/Clausius + temperature** | yes | **anti-MOND** | uncontested | **FAILS** (decisive negative) |
| **Entropic + DOF/entropy** (Debye/Pazy/Kaniadakis) | yes (if T_D=T_dS) | MOND | **posited/fitted** | INCOMPLETE |
| **Modified inertia** (Milgrom/Unruh) | yes | MOND | form derived | INCOMPLETE (closed-orbit) |
| **Verlinde 2016** (volume-law dS entropy) | yes (=cH) | MOND | **contested** | CONTESTED |
| **Superfluid DM** (Khoury–Berezhiani) | fitted | MOND | **new matter** | VIABLE, different ontology |
| **Deur** (GR self-interaction) | no | ~MOND | **contested/too weak** | CONTESTED |
| **AeST** (Skordis–Zlosnik 2021) | input | MOND | phenomenological | WORKS as EFT (the home) |
| **TeVeS** (Bekenstein 2004) | input | MOND | — | **FALSIFIED** (GW170817) |
| **de Sitter complexity** (DSSYK-dS) | yes (forced) | **OPEN** | tractable, unproven | FRONTIER |
| **Entanglement/RT/it-from-qubit** | n/a | n/a | AdS only | DIRECTION, not result |

### Per-path notes (the verified specifics)
- **Temperature route — FAILS.** The one clean elimination; tells the whole field the modification must
  live in the entropy sector, not the temperature. `[clausius_sign_calculation.py]`
- **Entropy/DOF route — INCOMPLETE (right answer, posited input).** MOND comes out, but the modification
  is never derived: Pazy 2013 (arXiv:1302.4411) adopts the freezing function *phenomenologically*; the
  Oct-2025 "thermodynamics of spacetime" paper (arXiv:2510.14345) uses an **"inverse approach"** —
  reverse-engineering the entropy *from* MOND; and the Nov-2025 "Relativistic MOND from Modified
  Entropic Gravity" (arXiv:2511.05632), **read in full**, **fits a₀ by MCMC to NGC 3198, never ties the
  Debye temperature to cH, and imposes the sign through a metric ansatz.** None earns the sign from first
  principles. *(This is the answer to "is 2511.05632's sign defensible or smuggled?" — smuggled.)*
- **Modified inertia — INCOMPLETE but genuine.** Fits the SPARC RAR at 0.105 dex with a fixed shape
  `[desitter_unruh_mond.py]`; lacks a complete action (closed-orbit/Ostrogradski). A real partial result.
- **Verlinde 2016 — CONTESTED.** Gives a₀=cH and the √-law `[yphi32_from_entropy.py]`; the volume-law de
  Sitter entropy is rejected by many relativists; dwarf-spheroidal tests are mixed (arXiv:1612.06282).
- **Superfluid DM — VIABLE, different ontology.** Reproduces MOND in galaxies, particle DM in clusters
  (arXiv:1507.01019); but it *adds* eV axion-like dark matter and a₀ is a fitted phonon coupling, not cH.
- **Deur — CONTESTED.** Reproduces MOND-like curves from GR's nonlinear self-interaction and claims to
  fix clusters, but most argue the self-interaction is far too weak in disk galaxies; criticized as
  unphysical. a₀ not from cH.
- **AeST — the home, not a derivation.** CMB- and GW-safe relativistic MOND; the framework *derives*
  ~80% of its field content `[clean_slate_field_theory.py]`, but the 𝒴^{3/2}+𝒦(𝒬) structure and the
  interpolation are posited.
- **TeVeS — FALSIFIED.** Predicted GW speed ≠ c; killed by GW170817.
- **de Sitter complexity — the FRONTIER.** Tracks entropy at leading order (no shortcut to a₀); the
  unclaimed prize is the **sign from the second law of complexity** `[desitter_complexity_sign.py]`.
- **Entanglement/RT — DIRECTION.** The deepest frame, but AdS-only; de Sitter not under control.

---

## Geometric theories — a correction (the class the scorecard under-covered)

The scorecard above covered the emergent-gravity/thermodynamic engines and the relativistic-MOND field
theories, but omitted the explicitly **geometric** modified-gravity class. Filling that gap
(`reviews/geometric_theories_and_siv.py`):

- **Maeder's Scale-Invariant Vacuum (SIV) — the closest cousin.** A geometric theory (scale-invariant
  empty space; Dirac 1973, Bouvier–Maeder 1979, Maeder 2017+) that **contains MOND** ("MOND as a
  peculiar case of SIV", MNRAS 520, 1447, 2023), **derives** a₀ from cosmology
  (2πa₀ ∼ cH₀ ∼ c²√(Λ/3)), and **predicts a₀ evolves** (arXiv:2409.11425, MNRAS-L 535, L13, 2024). So
  the framework's headline "a₀ evolves" is **not unique to it**; it is the same a₀∼cH∼c²√Λ family from a
  geometric *scale-invariance* principle rather than the framework's surface-gravity/density reading.
  Status: serious and published (MNRAS/A&A), but a **minority paradigm** (scale-invariance of the vacuum
  is a strong, non-mainstream gauge). **Crucially, SIV predicts a₀ DECREASES with z** — a₀(z=3) ≈ 0.42
  a₀(0) — **opposite** to the framework's increase, E(3) = 4.57. So the framework is a genuine, *distinct*
  cousin, and the z≈3 test becomes a **3-way discriminator**: framework 4.6 vs SIV 0.42 vs constant 1.0,
  ~10× apart at z=3.
- **Conformal/Weyl gravity (Mannheim–Kazanas)** and **MOG (Moffat, STVG)** are other geometric
  MOND-alternatives, but their acceleration scales are not tied to cH/E(z) (conformal's γ₀ is
  cosmological but distinct; MOG's is fitted), so they are MOND-adjacent, not the same tie.

This does **not** change the meta-finding (no route *derives* the framework's increasing-E(z) trend or
its coefficient), but it corrects the omission and **sharpens** the framework: the distinctive claim is
not "a₀ evolves" (shared) but "a₀ *increases* as E(z), opposite to SIV" — bolder, cleaner, and
discriminating. Honest risk: current data read ~flat, which leans toward SIV/constant, against the
framework's strong increase.

## What we learned (the honest meta-finding)

1. **MOND from fundamental physics is a crowded field, not an exotic one** — entropy-modification,
   modified-inertia, Verlinde, superfluid DM, and AeST all *reach* it.
2. **But no route derives the deep-MOND modification (sign + interpolation) from uncontested first
   principles.** Everywhere the key ingredient is **posited, fitted, contested, or adds new matter.**
   Verified concretely in the 2025 entropic-MOND papers (one fits, one inverse-engineers). **This is the
   field's universal open problem — not the framework's alone.** The framework is not behind; everyone is.
3. **The temperature route uniquely FAILS (anti-MOND)** — a real result that shuts one door and points
   all routes at the entropy/DOF sector.
4. **The framework's distinctive content is NOT the MOND mechanism** (shared, and uniformly "posited"
   across the field). It is **(a)** tying the *scale* a₀∼cH to the de Sitter horizon, and **(b)** the
   *evolution* a₀(z)=a₀(0)E(z) — the one falsifiable, non-inherited prediction no other route on the list
   makes sharply, and the only thing a measurement can use to choose between them.
5. **The real frontier is the same for everyone:** derive the entropy/DOF modification (the sign) from
   first principles. The framework's specific bet — the **second law of complexity** in the now-tractable
   **DSSYK–de Sitter** dual — targets exactly this universal gap, and is more defensible than the
   fitted/ansatz versions because it would *earn* the sign rather than assume it.

**Bottom line:** walking every path does not hand us a TOE. It does something more truthful — it shows
the deep-MOND derivation is unsolved *by everyone*, isolates the one shut door (temperature), confirms
the framework's distinctive content is the **scale-from-horizon** and the **evolution**, and points the
remaining hope at one well-posed problem: the **sign from entropy/complexity, first-principles.** No
route was dismissed unfairly; none was oversold.

---

### Sources (verified June 2026)
Pazy, *Quantum statistical modified entropic gravity as a basis for MOND*, arXiv:1302.4411 (PRD 2013) ·
*MOND Theory and Thermodynamics of Spacetime* (inverse approach), arXiv:2510.14345 (2025) ·
*Relativistic MOND from Modified Entropic Gravity*, arXiv:2511.05632 (2025) ·
Verlinde, arXiv:1611.02269 (2016) · Diez-Tejedor et al. (Verlinde vs MOND in dSph), arXiv:1612.06282 ·
Berezhiani & Khoury, *Theory of Dark Matter Superfluidity*, arXiv:1507.01019 (2015) ·
Deur, gravitational self-interaction (and critiques) · Skordis & Zlosnik, AeST, arXiv:2007.00082 (2021) ·
Bekenstein, TeVeS, astro-ph/0403694 (2004) · de Sitter complexity arXiv:2508.10093; DSSYK-dS arXiv:2310.16994.

*In-repo: `established_paths_to_mond.py`, `clausius_sign_calculation.py`, `desitter_unruh_mond.py`,
`yphi32_from_entropy.py`, `clean_slate_field_theory.py`, `desitter_complexity_sign.py`.*
