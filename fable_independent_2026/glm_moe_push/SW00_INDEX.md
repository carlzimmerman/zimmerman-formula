# SW00_INDEX — glm_moe_push (the nonlocal-door lane)

Swing 1 per the 2026-09-17 swarm brief; swing 2 per the AUTORESEARCH brief (instructions_1452.txt).
Committed and pushed at the owner's request, overriding brief stop rule (iii) ("no commits; leave
files for review"). Lane script mirrors the kappa_slot_2026 convention: check() with computed
booleans only, both a₀ footings, sympy for identities, MUTATE=1 switch, FAILs recorded as
findings. Deviation from the AUTORESEARCH brief's file conventions, at the owner's instruction:
lanes live here (glm_moe_push/), not in kappa_slot_2026/; numbering stays SWnn. No AR00_LOG —
this index is the loop log.

## Swing 1 (SW01) — record

- **SW01 — the environmental-scalar response** (`PROPOSER_SW01_envscalar.md`): the a₀ response
  acts on two nonlocal functionals of the Newtonian field on barycentered Gauss spheres — Γ
  (angular variance, the field's structure) and η (the l=1 component, the environment);
  g_obs = g_N + S(η)(ν_RAR(Γ/a₀)−1)g_N,enc, S = [1+(η/η_c)²]⁻¹. A uniform field is pure l=1 —
  it enters η, never Γ — so the system is defined by the flux structure, no hand-drawn boundary.
- First gate PASS (7.25 / 128.0 vs 6.4); quadrupole gate PASS; BTFR slope PASS (4.0 exact).
- **SW01-A (η_c = 1, no-knob stress balance): KILLED** — Oort 17.7× the budget.
- **SW01-B: OPEN** — declared η_c, three pre-registered falsifiers.

## Swing 2 (SW01b / SW02) — 2026-09-17, after the AUTORESEARCH brief

- **CRITIC_SW01.md landed** (the role skipped in swing 1): C1 real bug — SW01-B calibrated η_c
  on the gate's x = 2.5 instead of the true solar environment η_⊙ = (v_c²/R₀)/a₀; C2 the first
  gate was the ansatz evaluating itself; C3 the sphere center was unspecified; C4 the quadrupole
  check was a ceiling-ratio heuristic, not the P₂ computation; C5 the LSS gate was missing.
  All fixed in SW01b.
- **SW01b — orthogonality by quadrature (18/18 PASS; MUTATE 16/18, hinge verified):**
  - η_⊙ computed from v_c = 233 km/s, R₀ = 8.2 kpc: **2.292 canonical / 1.902 alt**; η_c
    recalibrated on it: **0.203/0.169, DECLARED** (loudly — inherits v_c, R₀, a₀ systematics).
  - Oort pass robust across the v_c/R₀ systematic band: **0.85–1.26×** the budget (E2).
  - Orthogonality theorems now COMPUTED, not asserted: isolated η ≡ 0, Γ = g_N; superposition
    cross term vanishes by quadrature (Γ = g_N, η = g_ext exactly, C1/C2); offset-center hinge
    shows the mixing the centering prevents (C3) — the barycenter is part of the law, fixed by
    the enclosed flux, not drawn.
  - Gate ratios improve to **152.1/220.3** vs 6.4 (D). RAR/LSS gate added: **S(η_LSS) = 0.9979
    ≥ 0.9**, cluster vicinity 0.972 (F) — the gate that would have killed the class had the LSS
    field been a few tenths of a₀.
  - P₂ coefficient of the response field on the phantom shell (r = 2r_M): **−6.1e-14 a₀** →
    tidal 3.4e-39 s⁻², zero by structure — Γ and η are scalars, no direction to align with, no
    l ≥ 2 at any order in η (G). MUTATE (trigger = |g_total|): c₂ = **−4.5e-2 a₀** → tidal
    2.5e-27 s⁻² = 0.48 ceiling — the vector coupling is genuinely Cassini-exposed; full
    axisymmetric propagation is fable's DE01 solver, OPEN, not claimed.
  - Wide binaries: **γ_v = 1.0010** — the three-way DR4 separation: 1.00 (this class /
    mesoscopic / cold) vs 1.09–1.12 (isotropic cap) vs 1.16–1.23 (AQUAL), 2026-12-02.
  - L265 dodge stated in writing: the curvature-order pincer closes curvature-BUILT actions
    (degree ≤ 2 cannot separate Φ from Ψ; degree ≥ 3 cannot reach the linear response; box⁻¹
    preserves ε-degree); Γ/η are matter-framed surface functionals of the Newtonian field,
    outside that class.
  - H₀ audit finding (A2, FAIL is the finding): the record's alt-footing a₀ = 1.1279e-10 implies
    H₀ ≈ 67.2, not 67.4 — README-rule-5 convention item.
- **SW02 — the barycenter Gauss projector (Helmholtz split, no suppression): KILLED as
  pre-registered** — Oort **130.3×/143.1×** the budget (canonical/alt), Cassini-safe (the free
  piece is never modified), so it dies on the Oort horn only. Kill line: *Helmholtz projector
  alone: Cassini-safe, Oort-dead; the sourced deep response needs the declared scalar
  suppression S(η) — which is SW01-B.* Not fixed (re-inserting S(η) is SW01 again).
- **KILLS_SYNTHESIS.md written** (two lane kills + the record's ancestors): the sourced deep
  response must be suppressed ~130× at η_⊙ ≈ 2 while field galaxies at η_LSS ≈ 0.01 keep ≥ 90% —
  a >4-order dynamic range; the suppression must be scalar (L243 kills direction) and no
  closed-space mechanism supplies it (force balance 7.25×, structure 1×, curvature order dead by
  L265). S(η_⊙) ≈ 0.008 is an independent measured input; deriving it is the open theorem lane
  (ANSWER-B material). Numerology control: 1.92/0.015 = 128 = 2⁷ and √127 are empirical ratios,
  KS04-flagged, never structure.
- **Attack-stage rejections (logged, no scripts — the anti-theatre gate working as intended):**
  - BTFR-intersection κ = ½ derivation: kernel-independence of the deep-limit crossing IS the
    deep limit (all kernels converge to g² = a₀g_N; the crossing point is rung 5's Lean-certified
    identity); a₀ sits on the input side through the deep law; a₀ = v⁴/(GM) is the BTFR
    zero-point MEASUREMENT R8 already carries. L261-class relabelling.
  - Rung-4 Jeans shortcut (σ² = C/2 from the phantom profile): L258 B closed it — σ² = C/2 ⟺
    γ = 2 ⟺ the dust profile is assumed to be the phantom's r⁻². Cited, not re-run.
- **FINAL_FRAMEWORK.md** — the coherence ledger: rungs with CLOSURE_MAP status words, numbers on
  record, and the single falsifier per row; G1–G9 scored for SW01-B; the three-way DR4
  separation; the closing statement is the programme's own decision rule. No SW03 enumeration
  script: every ledger number already has a computed home (.out/.json); a re-enumeration would
  be check(True)-theatre.

## STATE: OPEN (of the three terminal states). SIDE: universal-scale (L266 T3: emergent scatter
2.24× on gas dwarfs vs G114's 0.150). Next per the brief's priority: (1) full ΛCDM population
model vs G114 (OPEN spec, > 10 CPU-min); (2) the covariant action for the Γ/η law (ghost theorem
+ α₂ are its kill gates); (3) the globular-cluster anomaly under the live readings.

## Swing 3 (SW03) — the satellite η-sequence: second determination of η_c

The classical dSphs straddle η_c: η(D) = v_c²/(D a₀) spans **0.055–0.210** over D = 66–250 kpc
against the declared η_c = 0.203/0.169 — so their dispersions test the constant from data in
hand (Walker+09 σ; McConnachie-2012 D, r_h, L_V; embedded with provenance; Sgr excluded as
tidally disrupted). Estimator = the record's own L263-E deep-MOND virial σ⁴ = (4/81)GM_b a₀_eff,
same estimator both sides so the virial constant cancels in S_req. M/L_V band [1.5, 3], v_c band
[180, 230] km/s bracketed; η_c frozen from SW01b — NOT tuned to the dwarfs.

- **Gate A PASS**: median residual at frozen η_c = **−0.207 dex** (≤ 0.3 threshold).
- **Gate B PASS**: implied η_c from the suppression-demanding subset (Fornax, the only object
  whose S_req band sits inside (0,1)) = **0.145** vs Oort 0.203 — ratio 0.71, tightening from
  above; Oort and LSS gates both hold at the implied value (ρ = 0.5× budget; S(η_LSS) = 0.996).
- **C5 NOT DISTINCTIVE**: median residual vs isolated S≡1 differs by only **0.061 dex** — the
  σ(D) trend is MOND-generic EFE (inner more suppressed, η ∝ 1/D). The dSph data cannot
  distinguish this class's suppression from none at all at screening level. **Status stays OPEN;
  no new prediction claimed from the dwarfs.** Distinctive content remains direction-blindness
  (γ_v = 1.0010; P₂ = 0) and the squeeze.
- Standing cost reproduced: isolated median **−0.146 dex** vs kimik3's −0.13 dex (the MOND-wide
  dwarf residual; 7 of 8 objects have S_req ≥ 1 and cannot measure suppression).
- MUTATE hinge verified: η_c = 0.5 → Oort 5.8× budget → C3a flips (the only flipped gate; the
  implied-η_c check is mutation-invariant by design — it is data-side).
- Per-object Jeans (L263 E2) remains the registered confirmatory step; a PASS here buys the
  Jeans run, it does not replace it.

## PAPER_DELTA.md — the published paper vs the record

`paper/dark_universe_bridge.tex` (June 2026) maps ~100% onto the repo (bridge framing =
THE_IRREDUCIBLE_FRAMEWORK_2026-06-05 verbatim; CPL numbers = a0kit + EB-E9; five channels =
a0z_crossscale). Zero revelations from it; three maintenance flags FROM the record: (1) the June
CPL-dressed declining prediction is WITHDRAWN in RETRACTIONS.md, superseded by the stage-17
derived flat law; (2) the AeST realization is on the stop-defending list (Cassini quadrupole
~15–25σ); (3) MUSE-DARK III omitted against the "name it, never omit it" rule. Plus F4: the
promised AeST verification scripts are not found in the repo (integrity flag).

## Status

Two candidates killed in this lane (SW01-A, SW02), one standing (SW01-B, declared constant,
dated falsifiers); SW03 is a consistency pass — NOT DISTINCTIVE, no kill, no new prediction.
Stop rule (ii) (three kills → synthesis) not triggered. The words "derived", "closed",
"breakthrough" appear nowhere above because nothing here has earned them yet. Deferred, stated
openly: R3 ghost theorem and the action formulation (G03-class); R6 cluster residual; the
dSph/η ≳ 1 tension (now quantified: NOT DISTINCTIVE at screening level).
