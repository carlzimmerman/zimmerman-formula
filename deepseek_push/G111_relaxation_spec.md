# G111 — THE RELAXATION N-BODY SPEC (the formation gate's executable problem statement)

**Status: PRE-REGISTERED SPEC (frozen before any G111 run; nothing here is fitted).**
**Verdicts on the spec itself: `G111_results.json` (V1 completeness, V2 parameter sources, V3 the decision statement).**
**Sources: G081 (the equilibrium-stability verdict), G035 (the Newtonian kill), G084 (the max-entropy law),
G093 (the free-dust window), G103 (the phase timescale), G091 (the virial closed forms), g03e (equipartition),
THE_THEORY.md Lemma 2/3, STATE.md.**

---

## 1. THE QUESTION (precise, as G081's verdict left it)

G081's verdict: the capped isothermal phantom — ρ = A/r² on (0, r_break], σ² = C/2, Φ = C ln r, cap at
r_break = 0.62 r_M, Sigma² = C/2 with C = sqrt(G M_b a0) — is a **CRITICAL (marginal) fluid equilibrium**:
the radial fundamental mode is ω² = 0 EXACT, the exact zero modes are pure homology (ξ ∝ r, ξ ∝ r²,
rearrangements ALONG the isothermal family at fixed σ²), cap-invariant under both BCs; the linear relaxation
problem is WELL-POSED (no exponential collapse, no exponential dispersion); it is NOT a strict attractor. The
formation gate's requirement, in G081's V3 words, is: **bounded neutral-family excursions, no radial runaway
on ≥ 100 crossing times** — and G035's dust-attainment kill stands as the Newtonian control.

**G111's question (the executable N-body statement):** the collisionless, gravitationally-interacting
free-dust phase (> 98% of the dark sector; G093), placed in the baryon well **with the sector's own
sigma** — σ² = C/2 = sqrt(G M_b a0)/2, the law's virial temperature — does it **relax onto** (and stay on)
the phantom equilibrium ρ ~ A/r² (capped at 0.62 r_M) within ~100 crossing times, with

- **(a)** bounded neutral-family excursions — no radial runaway (G081's gate verbatim),
- **(b)** the equipartition M_ph(<r_M) = M_b reached (g03e: exact at the reading; G035's S2 measured ≤ 0.30 in the Newtonian control),
- **(c)** the ω² = 0 margin preserved (the end-state's radial spectrum still marginal: no compressive root).

Two dynamical laws are run — the **scalar-mediated** reading (the theory's channel) and the
**Newtonian-with-profile** control (G035's registered test). The mediator question — the G035 lesson's
other half — is the spec's decisive variable: *the Newtonian free-dust DOES NOT relax (G035's kill); does
the scalar-mediated channel?* Any difference in outcome between the arms is attributable to the well's
deep form alone (everything else is held identical).

---

## 2. THE NUMBERS THE SIM NEEDS (all committed)

### 2.1 The system (G081's own constants, verbatim)

| Quantity | Value | Source |
|---|---|---|
| a0 (canonical) | 9.3619e-11 m/s² | STATE.md / G081 / G099 (alt footing 1.1279e-10, secondary) |
| M_b | 7.0e10 M☉ (max-enclosed, G033 pipeline convention) | G081_results.json `Mb_msun` |
| C = sqrt(G M_b a0) | 2.9493938990e10 m²/s² | G081_results.json `C` |
| σ² = C/2 | 1.4746969495e10 m²/s² | G081_results.json `sigma2` |
| σ (the sector's sigma) | 121.4371 km/s (σ² = C/2) | G081/G084 (G084: 121.43710098335232) |
| r_M = G M_b/C | 10.2098235 kpc (= sqrt(G M_b/a0)) | G081_results.json `r_M_kpc` |
| r_break = 0.62 r_M | 6.3300906 kpc | G081_results.json `r_break_kpc` (α_break = 0.62) |
| v_c = sqrt(C) (deep flat) | 171.738 km/s | derived, C as above (the law's BTFR amplitude) |
| A (phantom amplitude, ρ = A/r²) | 3.51685e19 kg/m | derived: A = C/(4πG); G081 V1: Laplace(C ln r) = 4πG A/r², coefficient 1 |
| ρ(r_M) / ρ(r_break) | 5.23e-3 / 1.36e-2 M☉/pc³ | derived (G084's 0.008 M☉/pc³ sits at ~8.1 kpc, its own grid) |
| M_ph(<r_M) | = M_b to 7e-6 (the equipartition identity; g03e exact to 2.2e-16) | g03e / G081 |

G implied by the closure: G = C²/(a0 M_b) = 6.6737e-11 m³ kg⁻¹ s⁻² (the pipeline-consistent value; the
G035 unit identity G M_b = 2 σ² r_M = C r_M holds exactly — G035 V1, residual 0.00).

### 2.2 The force laws (the committed dichotomy)

Both arms share: the baryon mass distribution — the G033-pipeline profile shape as G035's (interior solid
body below x_first: g(0.01 r_M)/g(0.02 r_M) = 0.500; flat-v_b tail g ∝ 1/x beyond; **no softening of the
well**; normalized so max M_enc = M_b = 7e10 M☉ — G035 V2's M_b convention), the dust self-gravity (the
G035-certified Newtonian kernel — V8: numba ≡ numpy to 1.7e-15, softening ε = 0.08 r_M = 0.817 kpc), the
integrator (leapfrog, dt_max = 0.02 t_cross), the instruments (exact closed-form log-tail PE at ALL radii,
no clamp; φ(60 r_M) = 0 reference — the G035 instrument-fix), the ICs and the diagnostics.

**ARM S — SCALAR-MEDIATED (the theory's channel; THE_THEORY.md Lemma 3; G081 V1; G084; G091).**
The baryon well is the deep-modified field (the mediator is the scalar, not Newtonian gravity — Lemma 3's
gloss on the G035 kill):

- **Deep regime r ≥ r_M:** g_well(r) = −C r̂/r — the law's exact 1/r force, constant C = sqrt(G M_b a0),
  c_deep = 1 EXACT (G031 rung 1; G081 V1: conservative, curl-free, self-source closed). This is the field
  G084's max-entropy functional takes as "the fixed baryon well Φ = C ln r", and G091's virial chain lands
  σ² = C/2 EXACTLY at r_b = r_break in this well.
- **Transition to Newtonian inside r_M (r < r_M):** g_well(r) = −G M_b(<r) r̂/r² (the true interior
  profile). The transition at r = r_M is the a0-crossing of the flat-v_b tail (C/r_M = G M_b/r_M² = a0
  exactly — the unit identity); the junction is continuous. The smooth RAR-interpolant
  g = g_N μ₂(g_N/a0), μ₂(x) = 1 − (1 + x/2)⁻² (Lemma 2, zero parameters), is the registered refinement
  with the same deep limit; the piecewise form above is the committed executable law.
- Dust self-gravity: Newtonian softened kernel — **identical to Arm N and to G035** (the relaxation
  channel is the same in both arms; the arm's only difference is the well's deep form).
- Rung-4 note: the virial temperature of the committed well is σ² = C/2 at r_break (G091 V1c/V2b closed
  forms: σ² = (C/2)[1 + ln(r_M/r_b)/λ] → C/2 exactly at r_b = r_break; kappa = 1/2 = 1/n, gamma = 2 pinned).

**ARM N — NEWTONIAN-WITH-PROFILE (G035's registered test; THE CONTROL).**
g_well(r) = −g_N,real(r) r̂ everywhere (the pure Newtonian field of the same profile; tail falls as the
registered curve, g(2 x_last)/g(x_last) = 0.500 at x_last = 4.57 r_M), dust self-gravity identical.
**Expected: the G035 KILL** (this arm is A4's object, not a bet).

The equilibrium target (both arms): ρ = A r⁻² on [r_fit_min, r_break], σ² = C/2, M_ph(<r_M) = M_b, cap at
0.62 r_M — the fixed-well hydrostatic + max-entropy state (G084: second variation strictly negative,
unique global max in the well), with the fluid's radial fundamental ω² = 0 (G081). The sim decides
whether the full N-body dynamics (well + self-gravity) attain and hold it.

### 2.3 The particle count (N)

- **N_sim = 2000** (primary): G035's certified kernel scale (its full suite ran 58 cells at this N; V8
  kernel validation; dt-convergence twins; the A4 clone must be byte-comparable to G035's numbers).
- **N_sim = 8000** (size check, 1 cell at t_end = 150 t_cross): t_relax(N) = N/(8 ln N) t_cross — 33 t_cross
  at N = 2000, 111 t_cross at N = 8000 (G103's formula): the size-check brackets the relaxation-timescale
  adequacy of the primary N.
- **N_phys** (the sector's true particle number; registered, not simulated): from m_sec's TG bound —
  G084 landed: m > 23.25 eV (22.45 eV alt) clears the equilibrium sector's phase-space cap at
  ρ = 0.008 M☉/pc³, σ = 119–121 km/s; G093 landed: the free dust's forest window m ≥ 3.3–5.7 keV (95% CL):
  - N_phys = M_sec/m_sec with M_sec = M_b = 7e10 M☉ (the equipartition normalization): **3.36e75** at
    23.25 eV; **2.37e73** at 3.3 keV; **1.37e73** at 5.7 keV.
  - Elementary 2-body relaxation: t_relax = N/(8 ln N) t_cross = **1.0e70–2.4e72 t_cross** — dead by
    56–72 orders at galaxy scale (G103's cluster-scale statement, transferred; the free dust is
    collisionless as a particles fact).
  - Consequence (committed): the relaxation the sim can exhibit is the fluid-level (super-particle)
    relaxation; the equilibrium statement is N-independent (fluid: G081/G084); each sim particle carries
    M_sec/N_sim = 3.5e7 M☉ (the coarse-graining ratio N_phys/N_sim ~ 1e69–1e72 on the record). The sim
    decides the **fluid-level attainment**; whether the elementary sector can relax is answered by the
    timescale column (dead), not by the sim.

### 2.4 The crossing time and the run length

- **t_cross = r_M/σ = 2.5943e15 s = 82.21 Myr** (committed). 100 t_cross = **8.22 Gyr** (0.60 Hubble;
  the run is physically realizable in cosmic time), ≈ 22.5 orbits at r_M.
- Run length: t_end = 100 t_cross = 5000 integration steps at dt = 0.02 t_cross (G035's dt_max).
- dt-convergence twins at dt = 0.01 (≥ 4 cells); energy gate |dE/E| ≤ 1e-4 throughout (G035's worst cell:
  2.7e-5); xmax = 60 r_M with the exact log-tail bookkeeping.

### 2.5 The initial conditions (identical in both arms)

- **The C2 cell (the primary, the decisive one):** the phantom placement itself — ρ = A/r² on
  [0.05, 0.62] r_M, isotropic Maxwellian σ = σ_target = 121.44 km/s (σ² = C/2), dust total mass
  μ M_b with **μ = 1.0** (the equipartition normalization — the theory's own landing; G035's C2 control
  was the same placement at μ = 0.3 and it EVAPORATED in the Newtonian well: f_esc 0.37–0.51, r50 4.9–10.4
  r_M, σ²/σ_target² ≈ 0.32–0.33 at 100 t_cross — the transplant of that control into Arm S is the gate's X-ray).
- **The neutral-family suite (reading (a) — G081's zero modes):** the phantom compressed/stretched along
  the homology direction: ρ(r) → ρ(r/(1+ξ)), ξ ∈ {−0.2, +0.2, +0.4}, at σ² = C/2, μ = 1.0, R0 = 1.0 r_M.
- **The IC ladder (G035-format transfer matrix):** σ_start ∈ {0.3, 0.5, 0.7, 1.0, 1.5} × R0 ∈ {0.5, 1.0,
  2.0} r_M at μ = 1.0 (primary; 15 cells) — diagnostics σ_inf²/σ_target², r50/r_M, f_esc, M_d(<r_M)/M_b,
  exactly G035's deliverable format so Arm S ↔ Arm N are compared matrix-to-matrix and to G035's μ = 0.3
  block.
- **The A4 clone cells:** the G035 primary system (M_b = 6.2501e10 M☉ NGC3198-bundle, r_M = 9.65 kpc,
  σ_target = 118.05 km/s), μ = 0.3, (σ_start, R0) = (0.5, 1.0), (1.0, 1.0), (1.5, 1.0), run under Arm N
  only — must reproduce G035's registered transfer (σ-ratio 0.474/0.391/0.894; r50 0.588/1.095/22.3 r_M).

Budget: Arm S 18 cells + Arm N 18 cells + 3 A4 clones + 4 dt-twins + 1 N = 8000 ≈ 44 runs (~G035's 58).

---

## 3. THE ACCEPTANCE CRITERIA (pre-registered; evaluated on the end-state t = 100 t_cross unless noted)

The fit window: r_fit ∈ [0.12, 0.62] r_M (above the softening scale, below the cap).

- **A1 — the phantom profile achieved to 10% (Arm S, C2 cell + all 3 neutral cells):** fit
  ρ(r) = A_fit r^(−γ) over r_fit: |γ − 2| ≤ 0.20 (10% of the exponent) **and** |A_fit/A − 1| ≤ 0.10
  (amplitude to 10%), with the fit's rms scatter ≤ 0.10 dex.
- **A2 — the equipartition within 30% (same cells):** M_sec(<r_M)/M_b ∈ [0.70, 1.30] at t_end
  (the dust's enclosed mass at r_M; the reading's M_ph(<r_M) = M_b; G035's Newtonian S2 landed ≤ 0.30 — the
  control sits at/below the bar's lower edge).
- **A3 — no runaway (same cells + all 15 ladder cells at μ = 1.0):**
  (i) virial ratio 2T/|W| ∈ [0.80, 1.20] at t_end; (ii) r50(t_end) ≤ 2.5 r_M (G035's healthy cells sat
  ≤ 1.9 r_M; its runaway cells reached 4.8–86 r_M); (iii) f_esc(t_end) ≤ 0.10 (G035's C2: 0.37–0.51).
  These operationalize reading (a): bounded neutral-family excursions, no radial runaway, on ≥ 100
  crossing times.
- **A4 — the control does NOT relax (reproducing G035):** Arm N on the C2 cell must FAIL A1–A3 in the
  registered pattern: σ_inf²/σ_target² ∉ [0.8, 1.25] AND (f_esc ≥ 0.30 OR r50_end ≥ 2.5 r_M); and the
  μ = 0.3 clone (σ_start = 1.0, R0 = 1.0) must land σ_inf²/σ_target² ∈ [0.31, 0.47] (the registered 0.3906
  ± 20%) and r50/r_M ∈ [0.8, 1.4] (registered 1.095). A4 verifies the instruments separate the arms.
- **Reading (c) — the ω² = 0 margin preserved (Arm S, C2 + neutral cells):** on the end-state profile and
  measured σ²(r), re-run G081's fixed-well radial probe F(Ω²) on [0, 64]: F(0) > 0 AND zero sign changes
  (G081's registered structure: F(0) = 4.9998, min 4.9998, max 681.17 — the neutral continuum), and the
  self-consistent mode-equation residual of the end-state on the neutral family ≤ 1e-6 (G081's finite-
  difference level 1.8e-12 with the closed forms). The margin is "preserved" iff the end-state's radial
  spectrum is still marginal (no compressive root), i.e. the run did not move the equilibrium class.
- **Temperature-attainment branch (the ladder at R0 = 1.0, μ = 1.0):** σ_inf²/σ_target² ∈ [0.8, 1.25] for
  ≥ 3 of the 5 σ_start cells (G035's own window; its Newtonian cold starts cooled to 0.33–0.52 — the
  control fails this branch by construction). This branch decides whether the sector's sigma is
  dynamically attained (from cold/warm starts) or merely placed (PAPER29's postulate status).

---

## 4. VERDICTS — V1, V2, V3 (what the sim, when run, decides)

- **V1 (spec completeness):** the spec is complete and executable as written iff every quantity of §2 is
  fixed without free parameters, every arm's law is a closed expression, every acceptance criterion's
  inequality is computable from the listed diagnostics, and the instrument gates (energy, dt-convergence,
  numba≡numpy) carry over from G035. Checked in `G111_results.json` against this file.
- **V2 (parameter sources):** each committed number's source line (G081/G084/G093/G103/G091/g03e/G035/
  THE_THEORY/derived) — the table in `G111_results.json`.
- **V3 (the statement — the decision function):**
  - **OPEN (strong):** Arm S passes A1 ∧ A2 ∧ A3 on the C2 and all neutral cells ∧ reading (c) holds ∧
    Arm N reproduces A4 ∧ the ladder attains the temperature window (≥ 3/5 at R0 = 1.0). Then: *the
    scalar-mediated channel relaxes the free dust ONTO the phantom at the law's virial temperature within
    100 t_cross, holds the neutral family, and attains the temperature dynamically — G035's kill is
    specific to the Newtonian-with-profile reading; the formation gate OPENS with the temperature's
    dynamical origin supported for this system.*
  - **OPEN (weak):** A1–A3 ∧ reading (c) ∧ A4 hold, but the ladder's temperature attainment fails (cold
    starts still cool below 0.8). Then: *the phantom is dynamically MAINTAINED given the sector's sigma
    (G081's marginal reading confirmed at the N-body level — the gate opens on the stability leg), but the
    temperature remains PAPER29-postulated; the cold-state outcome does not re-derive σ² = C/2.*
  - **CLOSED:** Arm S fails any of A1/A2/A3 on the C2 or a neutral cell. Then: *the scalar-mediated
    reading joins G035's kill — neither mediator attains the phantom dynamically; the phantom is a theorem
    of the fixed well (G081/G084), not a dynamical state of the certified N-body system; the formation
    gate CLOSES, and the reading's dynamical status is the honest finding.*
  - Any failure of A4 (the control relaxing, or not reproducing the registered numbers) is an instrument
    verdict first: the comparison is void until A4 reproduces the kill.

---

## 5. SOURCES (committed, all on the record)

- G081 (deepseek_push/G081_equilibrium_stability.out + G081_results.json): marginal verdict, ω² = 0,
  homology zero modes, both-cap BCs, well-posed relaxation, the formation gate, all constants.
- G035 (glm53_push/G035_results.md + G035_results.json): the Newtonian KILL — "a definition of the
  temperature, not an equilibrium state of the certified N-body system"; the transfer matrices, the C2
  control's evaporation (f_esc 0.37–0.51), the ~0.35·σ_target² relaxed-temperature law, S2 ≤ 0.30; kernel
  certification (V1–V8), instrument history (the log-tail PE fix).
- G084 (deepseek_push/G084_maxentropy_law.out + G084_results.json): the law as max entropy in the fixed
  well Φ = C ln r at σ² = C/2 (ρ = A r^(−C/σ²) → A/r²), strictly negative second variation, the LBW and
  G081 notes stated; TG floor 23.25/22.45 eV; T = 1.835 mK/eV.
- G091 (deepseek_push/G091_virial_triad.out): σ² = C/2 EXACT at r_b = r_break (closed forms), gamma = 2,
  the virial+hydrostatic pin.
- g03e (deepseek_push/g03e_equipartition_results.json): M_ph(<r_M) = M_b exact (max dev 2.2e-16).
- G093 (deepseek_push/G093_results.json): free dust ≥ 3.3–5.7 keV (95% CL), share 98.7–99.2% of Ω_dm
  (G079), the TG non-binding ladder, the phase line.
- G103 (deepseek_push/G103_results.json): t_relax = N_enc/(8 ln Λ) t_cross, the elementary-sector
  timescales, the coarse-grained relaxation bracket.
- THE_THEORY.md Lemma 2 (μ₂), Lemma 3 (deep force EXACTLY 1/r, C = sqrt(G M_b a0), σ² = C/2, "the mediator
  is the scalar"), STATE.md (the board, rung 4's honest-postulated status).