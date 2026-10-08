# CFG487 FROZEN CRITERIA: the cold fluid's SETTLED FRACTION as candidate B's switch (Gap 1), tested in two versions

Written 2026-10-08 and committed alone, before any CFG487 script exists and before any CFG487 number is computed.
Nothing below may change after a result is seen; any later departure goes in the README as a disclosed deviation.

**Owner instruction (2026-10-08, relayed by the orchestrator):** test the idea, "test both" versions.
**Standing:** κ = ½ is FITTED (the only declared constant; it enters through a0). Kernel ν_mono. Both footings,
a0 = 9.3603e-11 and 1.1312e-10 m/s², scored separately and never pooled. a0 flat in z. No dark-matter particle: the
cold fluid's MASS is still required. Never "theory closed"; never "the data favour the framework".

**Not blind (disclosed).** Before writing this file I read CFG337, CFG346, CFG349, CFG351, CFG352, CFG413, CFG423,
CFG424 (README and engine), CFG464, CFG485's criteria and CFG486's committed output, and STANDING_2026-09-29. A
mental estimate (no script) puts the edge at x = r_edge/r_ta of about 0.03-0.06 for KiDS lenses on reading E1 below
and about 0.15-0.22 on reading E2, i.e. near or below CFG413's free-two-halo floor. It also suggests that at 256³ the
edge balls are about one cell, so the growth leg may not see the switch at all. Both are why the MUTATE design below
has an explicit "not diagnostic" outcome.

## 1. The object (both versions)

- **Settled fraction m in [0, 1]**, a comoving label of a fluid parcel:
  D m / Dt = Γ · L · (1 − m),  m = 0 at z_i = 49.
  - L is the binding LATCH: L = 1 from the first time the parcel's volume expansion rate θ ≤ 0 (turnaround: the parcel
    has stopped expanding), and L = 0 before. L never resets (CFG349's memory, without CFG349's duty gating: once
    latched, the clock runs continuously).
  - Γ = λ √(4πG ρ_X), λ = 1 (zero constants; CFG464: the corrected cluster budget does not exclude λ = 1).
  - Exact step update used everywhere: m' = 1 − (1 − m) exp(−Γ Δt L).
- **V1 (labelled MS1 EXCEPTION):** the parcel is a cold-fluid element. θ = the cold flow's expansion; ρ_X = the total
  matter density (CFG464 / CFG485's t_dyn convention, t_dyn = 1/√(4πGρ)). Reads the cold fluid, so under the original
  MS1 it is the matter door and NOT ADMISSIBLE; the owner's 10-06 relaxation (CFG351) and 10-08 "test both" make it
  testable here. Every table carries the column "under original MS1".
- **V2 (strict MS1):** the parcel is a baryon element. θ = θ_b, the baryon flow's expansion; ρ_X = ρ_b / f_b. Reads
  baryons only.
- **The switch:** the MOND sector's phantom DENSITY is multiplied by f = m · Θ(r_edge − r), with the mass-conserving
  edge r_edge = r_M / ln(1/(1 − f_b)) = 5.850 r_M, r_M = √(G M_b / a0) (CFG423/CFG424, PAPER45 v2.1).
- **Inputs:** κ (via a0, per footing) and f_b = 0.02237/0.14237. No other constant is added by this lane.
  Inherited and disclosed (not counted as new, not tuned): the spherical-collapse Δ_ta(z) on the ΛCDM background; the
  engine's MIX-A baryon filter (the phantom's source, and V2's baryon field in the PM); the engine's in_cover peak
  finder, whose peak threshold still contains the T1 width ε = 0.077 (the switch value itself no longer uses ε).

### Edge readings (fixed now)
- **E1 (PRIMARY, scored):** M_b = the system's present baryonic mass (the record's galaxy reading, CFG461/CFG485).
- **E2 (REPORTED only):** M_b = f_b · M_ta,law, the original baryons of the law's turnaround sphere,
  M_ta,law = (4π/3) r_ta³ (1 + δ_ta(z)) ρ̄_m(z) with r_ta = cfg100's r_ta_law (the PM-consistent reading, where the PM
  never depletes baryons). E2 cannot change a verdict.
- In the PM the edge is the engine's own x_supply edge balls (unchanged; there present = original baryons).

## 2. Implementations (fixed now)

### 2a. Analytic shell-history model (SPARC, KiDS, (d))
- ΛCDM top-hat shells (cfg100's Ω_m = 0.3153, h = 0.6736): integrate R'' = −GM/R² + Ω_Λ H0² R from a_i = 1e-3 to the
  turnaround event (Ṙ = 0, time t_ta, mean density ρ_ta), then on to R = R_ta/2 (time t_c, "virialised"); after t_c
  the mean enclosed density stays 8 ρ_ta.
- A shell observed at a_obs with mean enclosed density ρ̄_X(r) is mapped to its turnaround epoch by inverting the
  shell's present density (8 ρ_ta if t_c ≤ t_obs, the top-hat path density if t_ta ≤ t_obs < t_c). If
  ρ̄_X(r) < (1 + δ_ta(a_obs)) ρ̄_m(a_obs), the shell has not turned around: L = 0, m = 0.
- Exponent E(r) = ∫_{t_ta}^{t_obs} λ √(4πG ρ(t)) dt along that path (mean enclosed density); m = 1 − exp(−E).
  Shells denser than the table's earliest turnaround get that row's E (m = 1 to machine precision there).
- **V1:** ρ̄_X from the total (law) mass. **V2:** ρ̄_X = M_b(<r)/(f_b · 4π r³/3), from the baryon mass model
  (KiDS: point-mass M_gal; SPARC rotmod: V_bar² r / G at the measured radii; SPARC P3 rows: the point mass M_b).
- Conservative bracket (REPORTED): Γ frozen at the turnaround density (CFG349's lowest-on-path bound), no duty factor.

### 2b. PM engine (growth)
- `cfg487_pm.py` is a copy of CFG424's `cfg424_pm.py` (RES, RC = 0: edge balls x_supply + per-catchment
  mass-conserving compensation in the turnaround catchments; FB, MIX-A, ICs, seed 359, steps, k_J all unchanged).
  The ONLY change in the scored runs: the T1 switch value fsw = clip(0.5 + (l2 − τ)/2ε, 0, 1) is replaced by the
  settled-fraction grid SW (the mass-weighted CIC mean of the particles' m in each cell). The edge mask and the
  catchment compensation multiply SW exactly as they multiplied T1.
- Per-particle clock: latch L_p (bool), exponent E_p; Δτ per step = ∫ da/(a E(a)); Γ_p evaluated at the step's end;
  a particle latched during a step starts accumulating at the next step (conservative by ≤ 1 step).
- **V1 latch:** the particle's Lagrangian volume element, a³ |J|, with J = det ∂x/∂q from central differences over
  the initial particle lattice (minimum image); L_p fires when Δ ln(a³|J|) ≤ 0 over a step (θ ≤ 0 over the step).
  Γ_p from the total CIC density at the particle: Γ/H0 = λ √(1.5 Ω_m (1 + δ)/a³).
- **V2 latch:** the Eulerian baryon field: v_b = (W ⋆ j)/(W ⋆ n) with j, n the CIC momentum and count fields and W the
  engine's MIX-A filter at the current a; θ_b = 3E(a) + ∇·v_b / a² (central differences), interpolated to the
  particle; L_p fires when θ_b ≤ 0. Γ_p from ρ_b/f_b = ρ̄_m (1 + W ⋆ δ). Approximation (disclosed): the V2 clock rides
  on the matter tracers while reading only baryon fields (baryon parcels co-located with the tracer at mesh scale).
- **MUTATE-A (the frozen growth control, canonical):** the FRW-firing switch: L_p = 1 for every particle from z_i
  (no turnaround trigger; nonzero background m_bg(a)), V1's rate, same edge and catchment.

## 3. Tests per version

**(a) SPARC** (the record's switch-lane tolerance, CFG346's S clauses, harness copied from CFG346 and exec'ing CFG45
and CFG4_galaxy_law read-only; data SPARC_Lelli2016c.mrt + rotmod, never SPARC_table.txt), edge E1, both footings:
- S-A3: |½ log10(M_mod/M_law)| < 0.03 at R_HI for ≥ 90% of galaxies, spirals and dwarfs separately;
- S-rms: the rotmod RAR rms (Υ 0.61) changes by |Δrms| < 0.005 dex against the law.
- PASS iff all four (2 classes × 2 footings) A3 clauses and both rms clauses pass.

**(b) KiDS** (CFG413's stack P copied: CFG377's primary stack, 181,477 lenses, 15 g_bar bins, 50-patch jackknife,
Hartlap; free R^-0.8 two-halo amplitude profiled, sign free), edge E1, per lens group: phantom density × m(r) out to
r_edge, mass frozen beyond. PASS iff χ²(version) − χ²_best(CFG413) ≤ 4 on BOTH footings, where χ²_best is CFG413's
committed best grid fit (x = 0.5: 8.9479 canonical / 9.7704 alt, read from `cfg413_kids_results.json`).
Reported: Δχ² against CFG413's x = 1 row (its own frozen reference), the drop-one-bin range, the fitted A against
CFG486's plausibility range, the trusted 9 bins (R ≤ 0.3/h Mpc).

**(c) Growth** at 256³, seed 359, CFG424 engine copy, both footings, against CFG359's S0 (CFG361 cuts):
GROWTH OK iff |σ8 ratio − 1| ≤ 0.05 AND max_{k ≤ 1 h/Mpc} |P ratio − 1| ≤ 0.10; TENSION if the σ8 shift is in
(5%, 20%] or P > 10% with σ8 within 20%; FAIL if the σ8 shift > 20%.
- **MUTATE-A must NOT be GROWTH OK.** If MUTATE-A is GROWTH OK, the growth leg is declared NOT DIAGNOSTIC of the switch
  (the edge/catchment confinement, not the switch, controls growth; CFG424's own INCONCLUSIVE clause).
- **512³ rule:** a 512³ canonical run of a version is made ONLY if (i) that version is GROWTH OK at 256³ on both
  footings with MUTATE-A detected, (ii) the version passes (a), (b) and (d), so that 512³ could change its verdict,
  and (iii) no other 512³ job is running (`pgrep -f "N512\|512 0 MIXA\|cfg4[0-9][0-9]_pm.py .* 512"` empty). Otherwise
  it is not run and the README says why.

**(d) CFG337-style well-posedness** on DE12's 24 transitions (z ∈ {0.25, 1, 2.5, 4}, M_b ∈ {1e10, 1e11, 1e12}, both
footings; DE12's transition() exec'd read-only, as CFG337), gas at 1e5 and 1e6 K, k ∈ [1e-3, 1e3]/kpc:
- linear system of the gas displacement ξ and δm (quasi-static, Newtonian, WKB, latch fixed where L = 1):
  s² ξ = (Γ_g² − c_s² k²) ξ + i (4πG ρ_ph / k) F δm,  (s + Γ) δm = −i k (1 − m) (Γ/2) χ ξ,
  with Γ_g² = 4πG(ρ_b/f_b + ρ_ph) (CFG337), F = Θ(r_edge − r) (the edge, prescribed), χ = ρ_b/ρ_tot (V1) or 1 (V2);
- H1 no ghost (gas inertia ρ > 0; the label has no kinetic term); H2 real characteristic speeds with |v| ≤ c
  ({0 for the label, ±c_s}); H3 the maximum real growth rate is bounded uniformly in k (value at k = 1e3/kpc no larger
  than 1.01 × the value at k = 1e-3/kpc); H4 the extra growth over the no-switch rate, s_max − s_max(F = 0), is
  ≤ Γ_g at every radius, with no switch length needed.
- (d) PASS iff H1-H4 hold at every point of all 24 transitions, both versions' χ, both temperatures.
- Reported: the same with the edge removed (switch-only, the infall shells where 0 < m < 1); CFG349's principal-symbol
  speeds; the legality reading (below).

**(e) Lean** (Lean 4 + Mathlib, no sorry, standard axioms; compiled with `lake env lean` from
fable_independent_2026/lean_2026), if feasible in reasonable time, else stated skipped: step monotonicity and [0, 1]
invariance; FRW-off (never latched ⇒ m ≡ 0); MUTATE (latched with Γ Δt > 0 ⇒ m > 0); the edge identity
1/(exp(ln(1/(1 − f_b))) − 1) = (1 − f_b)/f_b; f = m Θ ∈ [0, 1]; the (d) bound: a positive root s of
s²(s + Γ) = G2 (s + Γ) + C with G2, Γ > 0, C ≥ 0 obeys s² ≤ G2 + C/Γ (k-independent).

## 4. Verdict per version (frozen)
- **PASS:** (a) and (b) pass, (c) GROWTH OK on both footings with MUTATE-A detected, and (d) passes.
- **PASS, GROWTH NOT DIAGNOSTIC:** as PASS, but MUTATE-A is GROWTH OK.
- **FAIL (legs):** any of (a), (b), (c), (d) fails; the failing legs are named.
- V1 additionally carries "MS1 EXCEPTION; NOT ADMISSIBLE under original MS1" whatever its result.
- **Legality suffix (reported, cannot raise a verdict):** the composition-label reading (m a comoving label of a
  two-state fluid; ordinary action for the advected part; irreversible conversion source whose energy f'(m) L_M ṁ must
  go into the parcel's internal energy). Reported ratio: R_conv = B/(ρ_c v_c²/2) (V1, cold fluid) and
  B/(ρ_b c_s²) (V2, gas), B = DE12's MOND-sector energy density, at 30 kpc and at r_edge on the 24 transitions; the edge
  is bilocal (it needs the host's M_b, CFG48-type) and this is said.

## 5. Reported diagnostics (cannot change a verdict)
- SPARC and KiDS rows for: switch only (m(r) out to r_ta, no edge), edge only (m ≡ 1 inside r_edge), E2 edge, the
  conservative bracket.
- Switch-alone growth (SA, canonical, 256³): the edge balls removed; SW confined to, and compensated within, the
  periodic 6-connected components of the cells whose latched mass fraction is ≥ 0.5 (V1-SA), and its FRW-firing
  control (MUTATE-B-SA). These show whether the switch can confine the excess by itself.
- PM z = 0 diagnostics: latched mass fraction overall, in voids (δ < −0.5), and in the l3 classes; mean SW in edge
  cells; overlap with T1 (cells with SW > 0.5 vs T1 > 0.5); m_bg of MUTATE-A.

## 6. Controls (a failed control is reported and kept, never silently fixed)
- **C1 engine reproduction:** the copied engine with the switch set back to T1 (mode T1REPRO, canonical) reproduces
  CFG424 TA-can (σ8 ratio 1.0033, max|P − 1| 0.0273 from `cfg424_results.json`) within 1e-3 on both numbers.
- **C2 KiDS harness:** m ≡ 1 with sharp edges at x = 0.5 and x = 1.0 reproduces CFG413's committed χ² within 0.01.
- **C3 SPARC harness:** m ≡ 1 and no edge gives Δrms = 0 and A3 = 100% (the law's own scores; rms0 equals CFG39's).
- **C4 shell model:** with Ω_m = 1, Ω_Λ = 0 the integrator gives t_c/t_ta = 1.5 + 1/π within 0.5%, and in ΛCDM its
  turnaround density matches cfg100's one_plus_delta_ta within 1% at z = 0, 0.25 and 1.
- **C5 (d) detector:** the no-coupling limit returns s_max = Γ_g at small k (Jeans), and an injected slaved
  k-linear term (CFG337 R1 type, ω² ∋ −c_g² k²) is flagged unbounded by the H3 test.
- **C6 PM clock:** m stays in [0, 1] and never decreases along any particle (max drop exactly 0).
- **MUTATE (analytic script, CFG487_MUTATE=1, outputs *_MUTATE.*):** the FRW-firing clock; A1 (m = 0 on FRW and in
  linear parcels) must FAIL and the run must exit 1.
- **(a)-type properties, analytic:** A1 m = 0 exactly on FRW and in linear parcels with δ ≤ 0.1 (θ/3H ≥ 0.967);
  A2 turnaround thresholds δ_lin = 1.062 (sphere, sympy) and 3/(3 + f) (Zel'dovich sheet) reported.

## 7. Protocol
No downloads. Large arrays go to `../_external_data/cfg487_work/` and are never committed. Compute niced
(`nice -n 10`), at most 6 threads in total (two 256³ runs at 3 threads each). No names or home paths in any file.
Only this folder is git-added. Commits are local; nothing is pushed. Other lanes' files are read-only.
