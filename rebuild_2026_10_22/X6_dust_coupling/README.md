# X6_dust_coupling: is there a dust coupling in v3's action family that fixes the hosted systems, the cluster cores and growth at once?

## Verdict: NO-GO FOR THE STATED CLASS

No candidate passes (a)–(e) together at any allowed parameter point. Every graded row has at least one FAIL everywhere. The
rows with the fewest FAILs (two each) are:
- **C1b with BS25's DBI K** (v3 plus a separate geodesic field dust): fails **(b) clusters** and **(d) isolated galaxies**.
  For every share of the cold sector that restores growth, it is **CDM under another name**.
- **C4, AeST's cold sector (v4)**: fails **(b) clusters** (H2) and **(e) health** (H1's theorem: the negative-energy mode is
  the growth mode).

The structural reason is one kinematic identity (X-D1, X-D2). The khronon dust's force relative to free fall is the lapse
gradient ∇Ξ, which is also the field that carries the law (Y = |∇Ξ|²/c⁴). So "the dust coupling" is not a free constant in
the khronon family:
- Making the khronon's own dust feel −∇Φ means ∇Ξ = 0, i.e. no law (C1a, C3α: no action). The khronon at Q ≡ 1 *is* mimetic
  (geodesic) dust with Ξ = 0.
- Giving dust weight in hosts and linear self-gravity therefore needs a second, separate dust (C1b). That dust sources the law
  like baryons, so it double counts in galaxies and over-masses cluster outskirts at its fair-sample abundance.

Stop rule (frozen): no follow-up scans and no new candidates.

κ = ½ FITTED. Footings canonical / alt (9.3603e-11 / 1.1312e-10 m/s²), reported separately, never pooled. No dark-matter
particle species. C1b is a field-sector dust, and is flagged as CDM under another name. Not "theory closed". Nothing here says
the data favour the framework.

## The candidates (frozen in fd303cac8b before any number)

S_v3 = (c³/16πG)∫√−g [R − 2J_x(Y) + 2K(Q)] + S_P,γL + S_m[g], with K = μ_K²(Q−1)². The PN dust force is
Dv/Dt = −∇Φ + α∇Ξ; v3 has α = 1. The linear self-gravity kernel is s = 1 − αk²/((1−f₀)k² + μ²), with f₀ = 1 + J′(0).

| id | coupling | action term | status |
|---|---|---|---|
| C0 | v3: khronon dust feels ψ = Φ − Ξ | S_v3 | graded (control) |
| C1a | the khronon's own charge on −∇Φ (α = 0) | **none**: a_μ = D_μ ln N for the foliation normal (X-D1), so α ≡ 1 by kinematics; α = 0 ⟺ ∇Ξ = 0 ⟺ no law. U1's MUTATE hybrid has Ξ in no force (Newton + geodesic dust) | excluded |
| C1b | v3 + a separate geodesic field dust | S_v3 − ∫√−g λ_d[g^{μν}∂_μφ_d∂_νφ_d + 1] (mimetic constraint field; X-D2, X-D9) | graded over its whole split f_d = Ω_d/Ω_cold ∈ [0, 1]. f_d = 0 is C0. f_d = 1 has zero khronon charge, so Ξ ≡ 0: GR + CDM (X-D6) |
| C2 | J′(0) = 0 (f₀ = 1; M1 R1), x_t → 0⁺ | S_v3 with J_R1 | graded |
| C3α | khronon charge on Φ − αΞ, α ∉ {0, 1} | none (α ≡ 1 by X-D1); the deep law also forces α = 1 (X-D3) | excluded, collapses to C0 |
| C3f | interior f₀ ∈ (0, 1) | J with a free J′(0) | excluded (needs a number); bracketed by C0 and C2 (∂s/∂f₀ < 0, X-D4) |
| C3β | baryons on g̃ = g − (Q^{−2β} − 1)nn (they feel Φ − βΞ) | S_m[g̃] | excluded (needs a number). In a held host the relative acceleration is (1−β)g_host, and baryons feel no host force at β = 1 (X-D7) |
| C4 | AeST cold sector (SZ21 + capped 𝒥 + γ_L = v4) | SZ21 action (on disk outside the repo) | graded from the record (H1, H2, C5) |
| C5 | K-shapes: BS25 DBI, two-scale K, comoving μ_K, H1's floor | add a fitted or postulated number | excluded as candidates. BS25's DBI at its *published* sets (P1, P2) is used only as a K sub-row |

## Grades (main run; JSON keys in `x6_dust_coupling_results.json`; numbers canonical / alt)

| row | (a) hosted | (b) clusters | (c) growth | (d) isolated galaxies | (e) health + radiation era |
|---|---|---|---|---|---|
| **C0** quadratic K | **FAIL**: B0 +2.00 ± 0.08 / +1.99 ± 0.08 dex, every branch ≥ 3 sd (STRUCTURAL); Coma z_sys 5.41 (`a.<foot>.branches`) | **FAIL**: S4 A1 CANNOT, 0 passing cells (`b.S4_verdict_A1`) | **FAIL**: best R = 0.391 at the cap (Boltzmann 0.073); 0.076 at μ_K = 0.03 (`growth.R`) | PASS at μ_K ≤ 0.03 Mpc⁻¹; FAIL at μ_K ≥ 0.1 (S4 guard, `d.d3`) | **FAIL**: no radiation era below μ_K = 1.84e8 h/Mpc (Q6; `e.Q6_mu_K_BBN_hMpc`) |
| C0, DBI P1 / P2 | **FAIL** (T3 is K-independent) | **FAIL** (S4; K″(1)/2 = μ² for DBI, X-D10) | **FAIL**: ODE 0.279 / 0.077; Boltzmann 0.259 / 0.324 (Q7) | FAIL (P1) / UNDECIDED (P2: μ between S4 grid points) | PASS (X-D10 + Q7 BBN) |
| **C2** quadratic K | **FAIL** (T3 is J-independent, X-D5) | **FAIL** (S4) | **FAIL**: 0.121 at the cap (`growth.R.cap_10.C2_ai1e3`) | as C0 | **FAIL**: health PASS (M1 R1c, C5-edge flag), no radiation era |
| C2, DBI P1 / P2 | **FAIL** | **FAIL** | **FAIL**: 0.061 / 0.006 | FAIL / UNDECIDED | PASS |
| **C1b** quadratic K | UNDECIDED (history): needs median M_d/M_b(<r₁₂) = 99 / 96, i.e. **18.5 / 17.9 × the cosmic ratio**; native (cosmic-ratio) line +1.29 / +1.28 dex at f_c (16.8 sd); Coma z_sys 2.70 | **FAIL** for every f_d ≥ f_c: fair-sample dust overshoots OUTER (gas-tracing A_OUTER ≤ 0.58 / 0.57 for f_d ≥ 0.28 / 0.22; NFW c* = 0.40 ≤ 0.66 / 0.61 for f_d ≥ 0.443) | PASS for **f_d ≥ f_c = 0.762** at the cap (a_i 1e-3; 0.816 from 1e-4; 0.854 at μ_K = 0.03) | **FAIL** for every f_d > 0 (double count). At f_c: NGC 3198 off the law by 0.145 / 0.142 dex, BTFR(r_ta) 5.23 / 5.22 vs 1.01; SPARC median Υ falls to 0.42 / 0.37 (P4 line fails; f_d,max(d2) = 0.027) | FAIL unless 1 − f_d ≤ 8.1e-8. At that limit the khronon charge in NGC 3198's catchment is **1.1e7 ×** short of its phantom |
| **C1b** DBI | UNDECIDED (as above) | **FAIL** | PASS (f_c 0.794 / 0.854 at P1 / P2's μ) | **FAIL** | PASS |
| **C4** AeST (v4) | UNDECIDED (no T3 analogue in the record) | **FAIL** (H2 A1 CANNOT) | PASS (H1 column ii) | UNDECIDED (collapsed AeST dust in galaxies not computed) | **FAIL** (H1 T1: E_J/Γ² = −8k²D²/(IQ̄³N²) < 0) |

**C1b at each part of its range.** f_d = 0 is C0, which fails (a). For 0 < f_d < f_c, (c) fails. For f_d ≥ f_c, (d) fails
exactly (any dust in galaxies) and (b) fails. No value passes, so no fitted split is ever chosen.

## The derivations (sympy, residual 0)

- **X-D1.** a_i = ∂_i ln N and n·a = 0 on two general metric families. The khronon charge's acceleration relative to free fall
  is the lapse gradient: kinematics, not a coupling.
- **X-D2.** A unit gradient field is geodesic (mimetic dust feels −∇Φ). At PN order X = −g^{μν}∂τ∂τ = 1 − 2εΞ, so Q = 1 + εΞ:
  the khronon at Q ≡ 1 is exactly the mimetic constraint, Ξ = 0, and then Y = 0.
- **X-D3.** Static held dust with weight α on Ξ gives (α − 1 + μ)X = g_N. Only α = 1 gives the deep law. α < 1 gives a floor
  (1 − α)a₀; α > 1 gives rescaled Newton.
- **X-D4.** s(k; f₀, α) = 1 − αk²/((1−f₀)k² + μ²), which is M1's kernel at α = 1. ∂s/∂f₀ = −k⁴/(…)² < 0.
- **X-D5.** For any J, a static host has Ξ = Φ + C and ∇ψ = 0. A bound unit falls at gM_b/(M_b + M_τ) (T3). Separate dust
  falls at g.
- **X-D6.** In C1b, r²μ(Φ′/a₀)Φ′ = G(M_b + M_d): the separate dust sources the law. The hold flux x/(1+x) is monotone, so
  ρ_τ = 0 gives Ξ = 0.
- **X-D7.** C3β: see the candidate table.
- **X-D8.** 8πGρ̄ = I₀/a³ + I₀²/(4μ²a⁶): the stiff term scales as (1 − f_d)².
- **X-D9.** Mimetic dust about Minkowski: π̇ = 0 is the constraint, H = λ̄|∇π|² ≥ 0, ω = 0 double root, ρ̄ = 2λ̄.
- **X-D10.** DBI K″ = 2μ²(1 − λz²)^{−3/2} > 0, with the same static mass.

## Checks

| run | result | notes |
|---|---|---|
| main | **17/17 PASS**, exit 0 | 406 s, peak RSS 0.177 GB, one thread |
| MUTATE (`X6_MUTATE=1`, khronon dust on −∇Φ) | 15/17, exit 1 | X-D5 and X-K2 FAIL as required: host force −∇Φ_host, fall rate g, R = 1.000 instead of 0.391. Its grades table is the control's output, not a physics result (the mutated coupling has no action, X-D1) |

The reproductions come first:
- **X-K1.** U1's B0 median is reproduced exactly (bootstrap sd 0.077 / 0.075 vs U1's 0.081 / 0.074; different resampling
  order). Coma z_sys is 5.4067.
- **X-K2.** M1/F3's 0.39080 and 0.12055 are reproduced exactly. The three-fluid ODE at f_d = 0 equals the two-fluid one.
- **X-K3.** CFG946's universal D-F BTFR at r_ta, 6.56246 / 6.54428, is reproduced exactly; the deep limit is 6.364.
- **X-K4.** P4's iso_perUps rms 0.05409 / 0.05372 and median Υ 0.52 / 0.44 are reproduced.
- **X-K5.** 17 record files were read; their sha256 are in `reads_sha256`.

## Amendments

- **A1 (POST-RESULT, code only).** RUN1 failed X-R: peak RSS 4.36 GB, because `solve_ivp` stored every step and macOS kept
  the freed buffers resident.
  - Fix: store the endpoint only, release freed memory, and re-exec with `MallocMediumZone=0` (as U1).
  - The rerun reproduces all 165 numeric leaves exactly.
  - RUN1 is kept as `*_RUN1.*`.
  - No line, threshold, candidate or reading changed.

## What this does not show

- **No nonlinear growth.** (c) uses the linear ODE from the optimistic a_i = 1e-3. Boltzmann numbers are lower (Q6, Q7).
  Nonlinear growth is L1's job.
- **C1b's dust contents are record estimators, not simulations:**
  - satellites and UDGs: the cosmic ratio;
  - galaxies: CFG946's D-F;
  - clusters: F1's two shapes.
  A history in which a cold geodesic dust grows on 8 Mpc/h scales yet stays out of galaxy wells is excluded by argument only:
  s ≡ 1 at every k, so it has no Jeans or free-streaming scale.
- **(b) rests on F1's β = 2/3 outskirts gas**, which X0 flags as soft (lane X2). That cannot change the verdict, because (d)
  fails for every f_d > 0.
- **AeST is graded from the record only.** Its hosted systems and its collapsed dust in galaxies are not computed.
- **Outside the stated class:**
  - non-local or higher-derivative couplings;
  - new fields with their own scale (X0's Q- or τ-keyed holds, a two-scale K, a DBI with a fitted λ_D);
  - modified inertia.
- **BS24/BS25 are WebFetch transcriptions (PROVISIONAL).** The mimetic-dust citation is from memory; X-D2 and X-D9 re-derive
  what is used.
- **The alt footing's Υ edge in (d2) is the law's own 0.44.** This is declared in the criteria, so (d2) measures what a
  candidate changes.

## Record items this sharpens or contradicts (suggested fixes; nothing edited)

- **U1 README, "What would have to change: the dust coupling (and J)".** In the khronon family the coupling is kinematics
  (α ≡ 1, X-D1), and J does not enter T3 (X-D5). What can change is the field content: a separate dust. That dust is CDM under
  another name and fails (b) and (d) here. Suggest: "a separate (CDM-like) dust sector, which double counts".
- **X0 D5** ("the dust coupling (−∇Φ) exists only as U1's mutation control"). It has no action at all (X-D1). The hybrid makes
  Ξ a spectator.
- **P4 T1's rms line hardly sees a dust double count.** With one Υ per galaxy, C1b's dust at f_c moves the rms only from 0.054
  to 0.056 / 0.059. Only the median-Υ window catches it (0.42 / 0.37). Any lane that adds mass inside galaxies should report the
  Υ shift, not only the rms.
- **X0 B1 (growth graded at a cap that S4 excludes).** Quantified: R = 0.076 at S4's galaxy-guard edge (μ_K = 0.03 Mpc⁻¹),
  against 0.391 at the cap. The two never pass at a common μ_K.

## Run and files

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X6_dust_coupling/x6_dust_coupling.py              # ~7 min, exit 0
X6_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X6_dust_coupling/x6_dust_coupling.py  # exit 1 by design
```

- **Files.** `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md` (fd303cac8b, committed alone first; A1 appended), the script,
  `.out` and `_results.json` for main, MUTATE and RUN1.
- **Inputs.** One CLASS run (background A). No PM simulation, no downloads. The live L1 run and `compute_queue/` were not
  touched.
