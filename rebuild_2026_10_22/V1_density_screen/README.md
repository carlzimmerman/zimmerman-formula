# V1_density_screen: can a well-posed, one-constant density screen replace γ_L / L★?

## Verdict (frozen rule, FROZEN_CRITERIA §3): NO-GO. Reading: SCOPED NO-GO (CRISP FINDING)

The owner asked: "open a lane testing a well-posed density-type screen that replaces gamma_L/L* one-for-one (no extra
constant): Cassini, outer globulars, dwarfs, WB prediction, and well-posedness at saddles."

**The screen tested (one line).** v3 with γ_L → 0, its P sector (the only part of the action that makes the MOND response)
multiplied by s = ψ², and a symmetron ψ coupled to the matter trace:
L ⊃ ψ²[P^μA_μ − W(K|P|)] − (v²/2)[(∂ψ)² + (μ_ψ²/2)(ψ²−1)²], with matter on A(ψ)g, A = 1 + v²ψ²/(2M²).
For a uniform s the static equation is AQUAL with μ_S = 1 − s/(1+x). At s = 1 it is the law; at s = 0 it is Newton.

- **Constant count: not one.** The screen has three constants: ρ_* = μ_ψ²M² (the one swapped for L★), λ_C = 1/μ_ψ and v²/M².
  - **λ_C does not decouple (I1 FAIL).** It decides whether stars are seen by ψ (Regime A) or hidden by their own thin
    shells (Regime B). The globular fit exists in B and not in A.
  - **v²/M² has no window (I2 FAIL).** If the MOND sector's back-reaction on ψ is to stay ≤ 10 %, the screen's fifth-force
    potential step must be ≥ 10 L_P⁰/ρ_gas at the globular sites. Keeping that step ≤ (300 km/s)² needs halo gas
    ≥ 6.9e-5 / 8.3e-5 M☉/pc³ (n_H ≥ 2.0 / 2.4e-3 cm⁻³) at 104 kpc. That means ≥ 3.3e11 / 3.9e11 M☉ of gas inside 104 kpc,
    or **2.6 / 3.4 × the Galaxy's whole baryon mass** (E_hi). This is a factor-3 result at the frozen thresholds. It scales
    as 1/(tolerance × allowance), so it is not a factor-100 result.
- **The fitted constant.** Using D10's data and statistic, with s at the clusters as the parameter:
  - the globulars need **S_GC ≤ S_95 = 0.602 (canonical) / 0.588 (alt)** (P1, E_mid, self-consistent field). D10's AQUAL
    row is reproduced: Δχ² = 19.26 / 21.09 at s = 1.
  - In Regime B that means **ρ_* ≤ ρ_gas,halo(104 kpc) / (1 − S_95) = 2.5 / 2.4 × the halo gas density at Pal 4's
    radius**. That density is not on disk.
  - In Regime A no ρ_* works.

**Results (a)–(e):**

| test | Regime A (stars seen by ψ) | Regime B (stars thin-shell screened; the only regime with a fit) |
|---|---|---|
| fit to the outer globulars | **none**: screening a cluster needs its central Newtonian potential (the MW's included) ≥ (1 − √S_95)·GM☉/R☉. Short by **×5.2–9.6** in every P1 E_mid cell | exists only through the halo's diffuse gas. The clusters cannot screen themselves (capacitance bound: short by ×3.5–458) |
| (a) Cassini Q₂ / planets | **FAIL**: the Sun's ambient keeps s ≥ 0.564 (the MW's baryonic potential at R₀ is at most (218 km/s)² against (436 km/s)² needed, ×4.0 short). Q₂ needs s ≤ 0.236 / 0.212 (Hees, all four fields); the planets need s ≤ 1.50e-5 / 1.24e-5 | **PASS under premise P-mono** (the local ISM is denser than halo gas at 100 kpc, so s_Sun = 0) |
| (b) dwarfs (S1's 45 / 46 satellites) | — | **FAIL (marginal, frozen line 0.05 dex)**. The 19 MW satellites inside 104 kpc are newly screened. Median Δ = +1.337 / +1.299 dex against v3's +1.282 / +1.281: a shift of **+0.055 / +0.018**. At s = 0 the shift is +0.258 / +0.101. Unscreened without γ_L they would sit at +1.108 / +1.038 |
| (c) wide binaries, 20 kAU | γ_v − 1 ≥ 0.083 / 0.097 (primary g_ext) | **γ_v − 1 = 0**: medium-first, like v3's 8e-6. DR4 Arm A floor 1.1614 / 1.1917 |
| (d) SPARC RAR guard (P4's statistic) | — | **FAIL**. At s = S_95 the rms is 0.126 / 0.125 dex (P4: 0.054 / 0.054) and the median Υ is 1.11 / 1.08. Screening only the gas slab moves in-plane g by −0.010 to −0.039 dex (bright disc, slab 0.1 R_d) and up to −0.244 dex (low-Σ disc, 0.3 R_d) |
| (e) well-posedness | **BOUNDED** | **BOUNDED** |

**More on (e).** γ_L's Hadamard instability is gone:
- Γ(1e8)/Γ(1e5) = 1.000001 without γ_L, against 1039 with it (H2 reproduces H4).
- The khronon rate is capped at √(4πG|D·P|(M_θ − s)). The ψ mixing never raises it.
- On H4's saddles at s = 1 it gives H4's bounded e-folds: median 0.006–0.20, max-depth cell ≤ 4.3.
- Around every star in a Galactic-strength field (x_e = 1.15–2.6), dropping γ_L leaves would-be phantom lobes of −340 to
  −1800 M☉/pc³. There the rate gives 450–1430 e-folds per 60 Myr. The mode's coupling to the metric and its kinetic term
  both scale as s, so where s → 0 the khronon is strongly coupled rather than healthy.

**What the screen does not touch.**
- **The dust sector.** Satellites under U1's T3 (+2.0 dex structural), cluster cores and linear growth (the μ_K cap) are
  untouched. The screen multiplies only the P sector, so GR and the BS dust are unchanged.
- **It makes two things worse.**
  - Cluster cores, in Regime B: the ICM is screened, so the prediction becomes Newtonian baryons, F1's A_MID 9.82 ± 0.63
    against the law's 1.68–1.85.
  - The MW rotation curve: v_c(R₀) is 200 / 202 km/s at S_95 against 215 / 220 for v3, χ²_RC 2120 / 1898 against 270 / 94.
- **One tile it improves:** the MW K_z(R₀, 1.1 kpc) falls from 92.3 / 96.9 to 79.3 / 81.1 against 66.4 ± 2.2. χ² goes from
  178 / 251 to 59 / 69, against a line of 67.5 (canonical passes the line).

κ = ½ FITTED. Footings canonical 9.36e-11 / alt 1.13e-10 m/s² (record values 9.3603e-11 / 1.1312e-10 where reused),
never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

## The regime conditions (the owner's physics point, made exact)

- **A compact body cannot screen its surroundings (A3, B1).** Outside a body of radius R in an ambient with screening level
  s_a, u = ψ_a − ψ is subharmonic, so 1 − s(r)/s_a ≤ 2R/r. This holds for a linear body and for a thin-shell body
  (B1: max r·u/(ψ_a R) = 0.03–0.97 ≤ 1).
  - For the Sun this is ≤ 9.7e-4 at Saturn and ≤ 1.2e-6 at r_M ≈ 0.04 pc.
  - So the Sun cannot hide its own phantom, its Q₂ source or the planets' a₀ tail. **The Solar System is screened only if
    its ambient is**, to s ≤ 1.2–1.5e-5 for the planets (Q₂ alone needs ≤ 0.21–0.24).
- **Regime A: stars are seen by ψ (ρ_*λ_C² ≥ M☉/(4πR☉)).** ψ sees the λ_C-smoothed baryon density. In linear theory, with
  the Yukawa factor dropped (both favour screening), a site reaches s ≤ s_t only if |Φ_N| ≥ (1 − √s_t)·GM★/R★. Screening
  is therefore keyed on potential depth (as M1 R2b1 found statically). The Sun's ambient and the outer clusters both fall
  short.
- **Regime B: stars are hidden (thin shells, B2).** A thin-shell body's ψ-charge is ≤ 4πM²R (its "capacitance"). B2 gives
  charge fraction q = 0.003 at ρR²/M² = 1e3.
  - Stellar systems are therefore transparent, and ψ sees only diffuse gas.
  - The Sun is screened if the local ISM exceeds ρ_*. A gas-free cluster is screened only if its halo gas exceeds
    (1 − S_95)ρ_*.
  - If halo gas does not rise outward (P-mono), the same holds for every satellite and the whole MW halo inside 104 kpc. That
    is what costs the RAR, the MW rotation curve and the satellites.
- **A steep multiplier is no escape.** A step-like s(ψ) could stretch the Sun's screened zone to r ~ R☉/δψ. Reaching r_M
  needs δψ ≤ 6e-7, which adds a constant (the switch point) and tunes the solar ambient to it to 1e-6.

## Numbers (all in `v1_density_screen_results.json`)

**S_95 by cell.**
- Canonical: P1 0.599–0.663; all 18 cells × 2 field treatments 0.599–0.975.
- Alt: P1 0.585–0.642; all cells 0.585–0.946.
- P2/P3 (MF-slope M/L) prefer s ≈ 0.5–0.7 and allow up to 0.93–0.98.
- All four clusters (with Pal 3): 0.703 / 0.683.
- Per cluster, Pal 4 sets it: Δχ²(s = 1) = 12.8 / 13.4.

**Cassini Q₂(s) (Richardson, G1/G1.5).**
- At s = 1: 2.19–4.07e-26 (canonical) / 2.55–4.60e-26 (alt), within 0.7 % of E2.
- Q₂(0.3)/(0.3·Q₂(1)) = 0.87–0.94: nearly linear in s.
- S_C (Hees, all four fields) 0.236 / 0.212; Park 0.138 / 0.124.
- Planets at s = 1: Earth / Mars / Saturn 1.1e4 / 6.7e4 / 1.3e4 × their bounds (alt 1.3e4 / 8.1e4 / 1.6e4).

**Wide binaries.** γ_v − 1 at the primary field is 0.167 / 0.199 at s = 1 (E2 anchor), 0.072 / 0.084 at s = 0.5, 0.027 / 0.031
at s = 0.2, and 0 at s = 0. The linear-response anchoring error at s = 1 is 0.010.

**H4 regions.**
- e-folds at s = 1: median 0.006–0.20, max-depth cell 0.07–4.26.
- If a saddle were screened (s → 0): median 0.04–0.82, max 0.31–24.6.

## Checks: 17/19 PASS, exit 1

The two FAILs are frozen physics lines and are the NO-GO legs: **I1** (λ_C does not decouple) and **I2** (no v²/M² window).

Every validation passes:
- **Part A.** A1–A4 sympy identities: μ_S; L_P⁰ = (a₀²/K)(x − ln(1+x)); ψ's v-independence; the subharmonic comparison; the
  coupled dispersion. With no mixing, A4 equals H4's γ_L = 0 relation at s = 1, with a finite UV limit Kρ_τ(M − S)/S.
- **Part B.** B1 (exterior bound) and B2 (thin-shell charge) on the own symmetron BVP.
- **Part C.** C1 reproduces D10's AQUAL and Newton σ_p to 1.8e-14 on 720 nodes. C2 reproduces D10's band-cell Δχ² to 1.3e-13.
- **Part D.** D1 reproduces D7d's BN11 AQUAL anchor to 9e-6. D2 reproduces E2's Q₂ to 0.7 %.
- **Parts E–H.**
  - E1 reproduces S1's logG_emb0 to 5e-14 (91 systems).
  - F1: anchoring 0.010.
  - G1 reproduces P4's iso_perUps rms to 3e-8.
  - H1 is bounded in every case. H2 reproduces H4's γ_L instability. H3 reproduces H4's 60 bounded rates exactly.
- **K-RSS.** 0.43 GB parent, 0.89 GB worst child.

**Mutation (`--mutate`: s multiplies source and phantom).**
- C1 fails (s = 0 is no longer Newton) and H1 fails (γ_L restored, unbounded): 13/15, exit 1.
- The frozen expectation that D1 and G1 also fail was wrong. Q₂ vanishes at s = 0 under both insertions, and G1 tests
  s = 1 only (AMENDMENT A2).

**Run history.**
- Run 1 is kept as `*_RUN1.*`. It gave 16/19, and K-RSS failed because the Q₂ child peaked at 1.018 GB.
- AMENDMENT A2 (post-result, b7fb82fd8d) split Part D into one child per job and fixed the fit-existence rule to the frozen
  P1 E_mid cells. The outcome was the same.
- Run 2 reproduces every physics line of run 1 (diffed).
- Runtime 570 s, one thread, nice 15. The heavy queue was untouched. No downloads.

## Record cross-check

`rebuild_2026_10_22/M1_trilemma/` R2b1–R2b3 had already scored static keying for v4: potential/thin-shell ordering,
body-density (Hui–Nicolis–Stubbs) and pointwise ambient density. All three came out NO-GO, R2b3 conditional on the
solar-wind density and the HI thickness.

M1 was not read before this lane froze (disclosed in A2). This lane is the dynamical version for v3:
- a field with Compton length λ_C;
- the exact exterior bound and the capacitance bound;
- the actual D10-statistic fit;
- out-of-sample numbers;
- the v²/M² window;
- the coupled dispersion.

It agrees with M1 on every overlapping point. Nothing in the record was found wrong.

One reading for H4/BSK1, an estimate from the A4 formula and not a scored check: the γ_L = 0 khronon is bounded, but around
stars in a Galactic-strength external field its bounded rate is not small. It is ≥ 0.87 of the s → 0 values above, since
M_θ ≥ 4 there.

## Input ledger (full: `ASSUMPTION_LEDGER.md`)

| input | class |
|---|---|
| v3 action, AQUAL μ = x/(1+x), BS24 PN system | FRAMEWORK-NATIVE / EXTERNAL (transcribed) |
| s = ψ² insertion, symmetron potential and coupling, matter-trace-only coupling | POSTULATED (this lane) |
| globular σ, likelihoods, Υ priors, MW brackets (D10) | RAW + SURVEY-CALIBRATION |
| Cassini fields, Hees/Park, planet bounds (D7b/D7d), E2 values | SURVEY-CALIBRATION / record |
| satellites (S1 CSV, LVD), SPARC (P4 loader), McMillan17, Bovy–Rix K_z, Eilers v_c, F1 clusters | RAW + SURVEY-CALIBRATION |
| H4 region medians | FRAMEWORK-NATIVE (illustrative systems) |
| premise P-mono (halo gas does not rise outward; ISM denser than halo gas at 100 kpc) | EXTERNAL physical premise, not on disk |

No ΛCDM-processed input, no QUMOND, no EFE recipe and no halo model enters a verdict.

## What this does not show

- **Only the symmetron class with the s = ψ² insertion was solved.** The structural legs hold for any scalar whose
  effective potential restores it toward its ambient value: the exterior bound, the capacitance bound and potential keying
  in Regime A. These include chameleons. The numbers (S_95, S_C, shifts) would differ for a₀ → s·a₀ or another s(ψ).
- **No circumgalactic or IGM density is on disk.** Regime B's fitted ρ_* is a ratio to unmeasured halo gas, and its out-of-
  sample consequences rest on P-mono.
- **Simplifications.**
  - Uniform s over each system (premise P-uniform), except the slab test.
  - Satellites scored on S1's central values, not its MC bootstrap. v3's central median is +1.282, against S1's bootstrap
    +1.331.
  - The slab test uses two idealised exponential discs.
  - The SPARC halo-screened row uses the spherical algebraic law.
- **The wide-binary γ_v(s) is linear response anchored to E2.** No nonlinear two-body solve was run at s < 1.
- **Well-posedness is linear and WKB** (as H4), with one mixing channel. Symmetron domain walls and the strong coupling at
  s → 0 are named, not computed. The symmetron's tachyonic rate (c/λ_C)√(1 − ρ/ρ_*) is k-independent and saturates at the
  VEV.

## Files and run

- `FROZEN_CRITERIA.md` (28ee4db0a8; A1 f21753f370 pre-result; A2 b7fb82fd8d post-result) and `ASSUMPTION_LEDGER.md`.
- `v1_solvers.py`: wrappers around D10's, D7d's and P4's solvers (imported read-only) and the own symmetron BVP.
- `v1_density_screen.py` writes `.out` and `_results.json` (run 2); `_MUTATE.*` (mutation); `_RUN1.*` (run 1).
- Run: `OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/V1_density_screen/v1_density_screen.py [--mutate]`.
