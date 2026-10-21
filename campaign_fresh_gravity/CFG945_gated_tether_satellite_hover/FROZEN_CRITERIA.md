# CFG945: the satellite hover (F2) in the collapse-gated tether (frozen criteria, committed alone)

Block CFG940–949 (owner, 2026-10-20 ~23:45: "launch agents on option 1" = the collapse-gated tether, CFG941 R3θ). This file is
written and committed **before** any derivation output, script or number of this lane. It fixes the questions, the candidate
resolutions, the tests, the bound derivation, the controls and the class rules. Any later change is a dated, labelled amendment
in this directory. The parallel lane CFG944 (ghost cure of R3θ) is not touched or read for results.

**Settings.** κ = ½ FITTED (never derived). Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt), never pooled.
The extra mass is cold energy, never a dark-matter particle; no species is added. Framework-native inputs only; no ΛCDM or
standard-MOND yardstick in any verdict. Not "theory closed"; never "the data favour the framework". NO-GO is reported as plainly
as a resolution.

**Inputs (read only).** CFG938 (README, DERIVATION, cfg938.py: the parent action, K1, the conditions of its §10); CFG941
(README, DERIVATION, cfg941.py, cfg941_results.json: R3θ, the hover lemma, `satellite_hover`, its 18 hover ratios and EFE factors,
M4); CFG925 R3 (README, results JSON: E0/E1/E2 satellite statistics); CFG874 (cfg874.py logic, results JSON: primary c, se_c),
CFG873 (D, se_D), CFG860 (c0, cG and their se, README), CFG875 (k, se_k); CFG882's Plummer dwarfs H1 (1e4 M⊙, 30 pc),
H2 (3e5 M⊙, 200 pc), H3 (2e7 M⊙, 700 pc); CFG938 S8's 6e10 M⊙ host at 50 / 100 / 250 kpc; the record's SPARC file for NGC 3198
(Υ = 0.61); the record's LVD dwarf files (`real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv`, as CFG874);
`CFG4_common.A0`; CFG925's nominal host baryonic masses (MW 6e10 M⊙, M31 1e11 M⊙); declared cosmology as CFG941 (Ω_b 0.0493,
Ω_c/Ω_b 5.364, H₀ 67.4). Nothing is downloaded. No other lane's file is edited.

**Gated parent (R3θ, CFG941).**
S = ∫√−g [c⁴R/16πG − mc²n − s(θ)(W_full(u) + (3γ/4K²)τ_μντ^μν) + λ(D²χ − Kmn)] + S_b, u = |Dχ|,
W_full = [−a₀u − a₀² ln(1 − u/a₀)]/K, s = 1 for θ ≤ 0, 0 for θ ≥ θ_s = H₀, quintic smootherstep between, θ = ∇_μu^μ.

## 1. The hover in the gated theory (questions answered in DERIVATION.md, each with a sympy or numeric check)

- **Q1 (static lemma, nested).** The satellite sits inside the host's collapsed region (host gate on) and its own collapsed
  region is nested inside. For a satellite medium that is static or translating uniformly, what is s(θ), and what is the net
  host force on it? K: CFG941's 18 ratios Δa/g_host (H1–H3 × 50/100/250 kpc × 2 footings) must be reproduced (K2).
- **Q2 (Theorem S, "same point").** State and check: if the force on a cold medium element depends on the element only through
  its position, weakly on its velocity, and on gate scalars of its own flow that take the settled value for a stationary
  medium (no membership label), then the host's own medium equilibrium at a point forces zero host force on any stationary
  medium at that point, including a satellite's. List the escape clauses.
- **Q3 (dynamics, estimates declared now).** (i) For a satellite medium whose stars move off it, the time t_gate for parts of it
  to reach θ = θ_s (where R3θ's gate turns off and its transition-band ghost lives). (ii) A correction check of CFG941's
  separation estimate: does the medium's own pull on the stars (not only the stars' pull on the medium) bind the stars to their
  medium in any case, and if so how fast does the composite fall?

## 2. Candidate resolutions (declared now, before any computation)

Each is minimal; its action change, new fields and new constants are stated here.

- **H1 — domain-local (per-label) tether.** The medium carries a membership label Q (a scalar on the label manifold, conserved
  along the flow, u^μ∂_μQ = 0, between label changes). One auxiliary pair (χ_q, λ_q) per label value:
  S_H1 = ∫√−g [c⁴R/16πG − mc²n − s(θ) Σ_q (W_full(|Dχ_q|) + (3γ/4K²)τ_q²) + Σ_q λ_q(D²χ_q − Kmn_q)] + S_b,
  n_q = n·[Q = q], D² in the mass-weighted mean medium frame. Label rules: re-latch **L2** (an element takes the label whose χ
  tidal tensor |τ_q| dominates at its position; threshold 1, no constant), declared alternative **L1** (the label whose |Dχ_q|
  dominates). Seeding at collapse: open (any rule that leaves each settled galaxy single-label); the single-label requirement is
  tested (§3a). New constants: 0. Questions: is it a local action; is D²χ = Kmn compatible with nesting.
- **H2 — tether anchored to baryons.** W(|Dχ|) and λ(D²χ − Kmn) are replaced by a coupling +m n ψ to ψ, the potential whose
  gradient is the law's total field of the anchoring baryons (QUMOND form ∇²ψ = ∇·[ν(|∇Φ_b|/a₀)∇Φ_b], ν the law's kernel), so
  a cold medium settles where its Newtonian field is the law's phantom. Variants: **H2v** variational (the coupling acts back
  on the baryons), **H2n** non-variational (the medium feels ∇ψ, the baryons feel nothing back), **H2g** anchoring to all
  baryons, **H2o** anchoring to own baryons (requires H1's labels on baryons and medium). New constants: 0.
- **H3 — equivalence-principle restoration.** (i) An internal gradient-shift symmetry χ → χ + b_μx^μ that would make a uniform
  external χ gradient unobservable: is it compatible with the law? (ii) The medium's passive gravitational mass in a settled
  host's field vs its inertial mass. (iii) Is the hover an artefact of static equilibrium: instantaneous forces on a moving
  satellite medium, including CFG941's χ̄ boost term βV and O(v²/c²); a rigid two-component orbit integration. New constants: 0.
- **H4 — dispersion-supported settled medium.** In settled regions a share f_T of the medium's support is the tether and
  1 − f_T is the stream's own velocity dispersion (multistream pressure, specific to the stream). One new constant (f_T, or a
  function f_T(R)).
- **Corollaries of Theorem S (reported, not graded separately):** a velocity-gated tether; a filtered (high-pass, one constant ℓ)
  tether reading.

## 3. Tests per candidate

- **(a) Static law.** The candidate's static, spherical, cold, γ → 0 limit on NGC 3198 (43 radii): max |g/g_law − 1| < 1e-6 on
  both footings, for the acceleration the baryons actually feel, plus the deep BTFR (lim V⁴/(GM_b a₀) = 1, sympy; numeric
  y = 1e-14 within 1e-6, as CFG941 A1). For H1 the single-label galaxy is graded; reported alongside: two equal labels, and free
  (re-latch-failed) debris at q = M_debris/M_settled ∈ {1e-6, 1e-3, 0.1, 1} in the phantom's shape.
- **(b) Satellite free fall.** ε = |Δa|/g_host, Δa = a_medium(CoM) − a_stars, for H1–H3 in the host's settled field at
  50/100/250 kpc, both footings, from the candidate's force law with CFG941's CoM machinery (64-point angle, shells). For H1 the
  host field is the full point-mass law field (tides included) and the satellite domain is truncated at its L2 radius (capped to
  [a, 100a]). **PASS iff ε ≤ ε_B on every case of that footing.**
  - **Bound ε_B (derived from the record's numbers).** A differential acceleration ε g_host strips a dwarf's stars from its medium
    iff ε g_host > κ_r g_int, g_int = 3σ²/r₁₂ (CFG874's own numerator, r₁₂ = 4/3 r_h), g_host = the law field of the nearer host
    (MW 6e10 M⊙ at distance_gc, M31 1e11 M⊙ at distance_m31; nearer host only, which is generous to the hover). A stripped dwarf's
    prediction is Newtonian, so its residual rises by log₁₀ ν_e(g_bar/a₀). CFG874's primary statistic (its sample, Υ_V = 2,
    gas "disc", restricted window, seed 874, 4000 bootstrap draws) is recomputed against these predictions for every dwarf
    (satellites and isolated). ε_B = the largest ε with c(ε) ≥ −2 se_c(ε) ("satellites not significantly above field").
    κ_r = 1 graded; κ_r = 2 reported (sensitivity). c at ε = the hover's ratio is reported.
  - If ε_B ≥ 1.11 on a footing, the record's σ data cannot see a hover-size differential through stripping; this is stated
    plainly, and (b) is then graded on that footing against CFG941's frozen line 0.01.
  - Reported, not graded: CFG941's 0.01 line on every candidate; the composite free fall a_cm/g_host where stars stay bound;
    the deficit bounds implied by CFG873 (D + 2se_D), CFG860 (c0 + 2se, cG + 2se) and CFG875 (k + 2se_k).
- **(c) No EFE on the internal law.** The uniform-field EFE shift of the satellite's phantom at its Plummer scale radius on the
  host-facing axis (CFG941's construction). **PASS iff |shift| ≤ δ_c = c + 2se_c of CFG874's primary (reproduced, per
  footing) for every case.** The tidal term (host field gradient) is reported separately; CFG941's 0.01 dex line is reported.
- **(d) Well-posedness (settled sector, s = 1).** CFG938's conditions (γ > 0; ρ_c c² > D(u)u/K) per label/stream; WKB min ω²
  bounded below independent of k (Jeans-type growth allowed), including two co-located labels with a relative velocity;
  energy-momentum: diffeomorphism-invariant action (PASS), conserved only between label changes (PASS with that cost listed),
  or no action / non-reciprocal force (FAIL). R3θ's transition-band ghost (CFG941 d) is inherited by every candidate, is
  CFG944's subject, and is listed as a condition, not regraded.
- **(e) Report (not graded).** What the candidate implies for F1 (linear self-gravity, growth) and for tethered–tethered gravity:
  the two-component mode-average cross term, the linear-regime growth exponent, the settled-state stability.

## 4. Classes (frozen)

Per candidate:
- **RESOLVED:** (a)–(d) pass within a local, variational action with at most one new constant.
- **RESOLVED-WITH-COST:** (a), (b), (c) pass and (d) passes on CFG938's conditions, but only with at least one cost: a
  non-variational (latching or label) rule, a rule not stated as a local field equation, extra auxiliary field content beyond
  one χ, or a second constant. Every cost and open condition is listed.
- **NOT RESOLVABLE:** a theorem or analytic argument (with a sympy or numeric check) shows that within the declared structure no
  choice of its free functions or constant passes (a), (b), (c) and (d) together.

Overall:
- **HOVER RESOLVED:** at least one candidate is RESOLVED.
- **CONDITIONAL:** none RESOLVED, at least one RESOLVED-WITH-COST; its costs and conditions are listed.
- **NO-GO:** every candidate NOT RESOLVABLE, with the proof stated.

## 5. Controls

**K (must pass, else VOID until fixed and disclosed):**
- K1: NGC 3198 law from CFG938's reduced Euler–Lagrange equation, < 1e-6 both footings (CFG938: 2.2e-16).
- K2: CFG941's 18 hover ratios reproduced to 1e-9 relative (cfg941_results.json).
- K3: CFG941's M4: tether off gives |Δa|/g_host ≤ 1e-12.
- K4: CFG874's primary c and se_c reproduced to 1e-12 on both footings from the record's LVD files.
- K5: R3θ gate s(0) = 1, s′(0) = s″(0) = 0; θ = 0 for a uniformly translating medium (sympy, covariant).
- K6: CFG941's 18 EFE factors reproduced to 1e-9 relative.

**MUTATE (separate `_MUTATE` outputs; each tooth must bite; exit 1 by design, 2 if a tooth fails):**
- M1 labels removed in H1 (the satellite medium reads the total χ): the hover returns (ratios = K2 to 1e-9).
- M2 tether off: universal free fall, |Δa|/g_host ≤ 1e-12 (P0/R3θ and H1 paths, uniform host field).
- M3 H2 reaction switched off: NGC 3198 baryon law < 1e-6; on: > 1e-6.
- M4 single-label requirement violated in H1 (two equal labels): NGC 3198 law deviation > 1e-6.
- M5 bound statistic: ε = 0 gives CFG874's c; ε = 100 (every dwarf stripped) gives c(ε) < −2 se_c(ε).
- M6 H3 dynamics: tether off, stars and medium co-move (separation < 1e-6 r_t over 1 Gyr, a_cm = g_host to 1e-9).

## 6. Hand expectations (disclosed before any script; not results)

- Q1: settled or uniformly translating satellite media have θ = 0, s = 1, so R3θ's satellite sector is CFG938's and the hover
  is unchanged (K2). Q2: Theorem S holds; its escapes are a membership label, stream-specific (non-cold) support, O(1) velocity
  dependence at satellite speeds, or a non-stationary satellite medium. Q3: an abandoned medium probably crosses θ_s within a
  few Myr (inside R3θ's ghost band); including the medium's pull may bind the stars in the cases where the satellite's own
  field exceeds the host's, and then the composite falls at roughly its baryon fraction of g_host.
- H1: resolves (b) and (c) (Δa = 0 in a uniform field; tidal residual small), passes (a) for a single-label galaxy, needs a
  non-variational label sector: RESOLVED-WITH-COST. Two labels in one galaxy miss the law.
- H2: H2v fails (a) by a reaction of order a₀/2 on the baryons in the deep regime; H2n fails (d) (no reaction); H2g hovers
  (Theorem S); H2o needs H1's labels and still meets the H2v/H2n dichotomy: NOT RESOLVABLE.
- H3: a gradient-shift symmetry is incompatible with W′(u) ≠ 0 (forced by the law); the medium's passive gravitational mass in
  a settled host's field is zero at leading order; dynamic corrections are percent-level: NOT RESOLVABLE (the hover is real).
- H4: (a)'s cold limit forces f_T = 1, which is the hover: NOT RESOLVABLE (a warm theory is a different theory).
- ε_B may be O(1): the record's σ data see a differential only through stripping. If so, (c) carries the CFG925 R3 contradiction.
- Expected overall: CONDITIONAL (labels necessary by Theorem S and sufficient by H1). These may be wrong; results are reported
  as they fall.

## 7. Compute

One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, in-script RSS guard aborting above 1 GB, plus a memory guard
(start only if free+inactive ≥ 12 GB; exit 75 if swap grows > 1 GB above its start or free+inactive < 8 GB). sympy + small
numpy/scipy; seconds to minutes. A live 1024³ job runs beside this lane; nothing touches it.
