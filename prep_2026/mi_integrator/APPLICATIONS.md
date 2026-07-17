# APPLICATIONS — Lane A runs of the MI memory-integral orbit integrator

**Date:** 2026-07-16. **Script:** `applications.py` (this directory; **exit 0, all app gates AG-a1..AG-d4 PASS**; full log `applications.out`). The engine's 36-gate suite (`mi_integrator.py`) is **re-run at import time** and must pass before any application executes (`gate_rerun.log`, all PASS this session). Figures: `fig_orbits.png`, `fig_ecc_offset.png`, `fig_wb_gamma.png`, `fig_planetary.png`.

Framework: **de Sitter–Unruh MODIFIED INERTIA** (Zimmerman) — NOT standard MOND. Own interpolation ν(y)=√(1+1/y), μ(x)=K(x²); published covariant kernel K(z)=(√(1+4z)−1)/(2√z), Herglotz–Nevanlinna positive measure, ‖K‖≤1, causal-retarded, v11 sum rule ∫dν=1. Both footings everywhere: **canonical a₀ = cH_Λ/Z = 9.36e-11** (ρ_DE), **alt 1.13e-10** (ρ_total/cH₀).

**What this is:** the first application runs of the first numerical orbit integrator through a concrete MI kernel. Every prediction is a **BAND over the RAR-alive measure class** {CANON, TILT±0.025} × Mode-II memory corners {ultralocal, H_Λ, gap 2c/a₀}; RAR-dead members (POLE/FLAT, 0.37–3.65 dex off, engine Q1) and the secularly unstable orbital-frequency corner (engine X1f) are quarantined. **This instrument makes the published theory's orbital predictions FORCED and falsifiable. It is not a proof of the framework.**

Conventions (stated, gated): adiabatic two-pass startup (slow memory at the steady **orbit-mean** pre-history fixed point — the published quasistatic theorem's own assumption; cold-start systematic quantified in engine gate V4); RAR observables = time averages over integer radial periods (pericenter-windowed); tilts referenced to their own circular law so the eccentricity channel is not confounded with their ~0.02-dex quasistatic tilt.

---

## (a) Eccentric galactic orbits — the RAR offset of non-circular orbits (e = 0…0.9)

Plummer field, y(b)=0.15 (deep regime; y(b)=1.0 transition spot-checked), tangential launches λ·v_circ → measured ε=(r_max−r_min)/(r_max+r_min) from 0 to 0.86. Observable: the orbit's effective RAR point (⟨g_N⟩, ⟨|a|⟩) vs the circular law.

**Total offset D_tot [dex] vs the member's own circular ν** (canonical footing):

| ε | ultralocal | corner=H_Λ | corner=gap | CANON | TILT+ | TILT− |
|---|---|---|---|---|---|---|
| 0.000 | +0.00000 | −0.00000 | −0.00000 | −0.00000 | — | — |
| 0.075 | −0.00002 | −0.00005 | −0.00005 | −0.00005 | +0.00052 | −0.00065 |
| 0.236 | −0.00004 | −0.00015 | −0.00014 | −0.00014 | −0.00017 | −0.00012 |
| 0.415 | −0.00008 | −0.00022 | −0.00023 | −0.00023 | −0.00049 | +0.00002 |
| 0.617 | −0.00084 | −0.00161 | −0.00163 | −0.00164 | −0.00190 | −0.00139 |
| 0.731 | −0.00195 | −0.00338 | −0.00343 | −0.00342 | — | — |
| 0.857 | −0.00381 | −0.00574 | −0.00578 | −0.00580 | −0.00590 | −0.00566 |

- **MEASURE-INDEPENDENT headline:** orbit shape cannot move a system off this RAR by more than **~0.006 dex out to ε≈0.9** — and the offset it does produce is **negative** (below the circular RAR), growing with ε: the dispersion-supported offset, made quantitative. Alt footing: same sign/size at matched λ (AG-a6); transition field y(b)=1 shows the same structure at ~⅓ amplitude.
- Decomposition: **sampling channel** (convexity of ν; the ultralocal column; resolved above the measured ±3.1e-05-dex window-sampling floor for ε≳0.4) + **memory channel** (member − ultralocal): 0 (ultralocal) … −0.002 dex (slow/horizon memory at ε=0.86); at small ε the virial-convention memory channel reproduces the banked rb3 closure-B epicyclic law (−0.000216 vs −0.000209 dex at ε=0.075, **3%**, AG-a3).
- Convention spread quoted: time-average vs virial convention differ at the ~0.001-dex level (both printed); convergence: 2× timestep + longer run moves D_tot by 3.3e-06 dex (AG-a5).

## (b) Wide-binary analog — per-star MI-EFE, γ_v, and the banked-1.09 cross-check

Two 0.75-M☉ stars, banked external field g_ext,obs=1.9a₀ (per-star MI-EFE; the engine's X2b gate verifies the instrument's force law **is** the banked algebraic prescription to 8.9e-16). Coplanar dynamical runs, force-boost observable γ_v=√⟨|a_rel|/g_N⟩, separations 5–30 kAU:

| member | 5 kAU | 10 | 20 | 30 |
|---|---|---|---|---|
| ultralocal | 1.0762 | 1.0929 | 1.0923 | **1.0923** |
| corner=H_Λ / gap / CANON | 1.0922 | 1.1339 | 1.1386 | **1.1389** |
| TILT+ | 1.1017 | 1.1461 | 1.1511 | 1.1514 |
| TILT− | 1.0837 | 1.1228 | 1.1273 | 1.1275 |

**Cross-check vs the banked 1.09 (wb_dr4_prereg_framework_curve.py): AGREEMENT.** The ultralocal member (= the banked prescription) gives **1.0923**, inside the banked 1.05–1.10 band; the static coplanar orientation average of the same banked curve is 1.0814 (residual 1.0% = orbit-shape sampling — the anisotropic per-star force has no circular orbit, r/s wanders 0.6–2.1) and the banked headline 1.1015 is the isotropic average of the same curve (recomputed). All are convention spreads of ONE curve.

**Honest finding (both footings):** the closure fork spans **γ_v ∈ [1.076, 1.151]** (canonical; alt 1.111–1.169), and the horizon-memory end sits **exactly on √ν(y_ext,N) = 1.1389 = the MG/AQUAL asymptote** (WB periods ~Myr are frozen against the kernel's ~200-Gyr memory). **DR4 wide binaries therefore discriminate closure members of this kernel (ultralocal ~1.09 vs horizon-memory ~1.14 = the MG number), not MI-vs-MG per se** — sharpening the banked "MI-vs-MG likely UNDECIDABLE in DR4". A measurement outside ~[1.05, 1.17] cuts against the kernel on both footings at this g_ext.

## (c) Planetary orbits — the a₀/2 landmine, measured through the integrator

Venus-like (0.723 AU, e=0.0068) and Saturn-like (9.583 AU, e=0.0565) orbits through the full memory machinery. Physics forced by the instrument's EOM family (the first-moment closure that carries **all** the published galactic wins): on a bound planetary orbit the memory signal f=|a|²/a₀² is constant up to O(e), so **every measure and every memory corner sees its quasistatic dressing**:

| member | δg (Venus) | δg (Saturn) | note |
|---|---|---|---|
| ultralocal | 4.680e-11 = **1.0000×a₀/2** | 4.680e-11 = 1.0000 | pointwise tracking |
| CANON | 4.680e-11 = 1.0000 | 4.680e-11 = 1.0000 | its deep-UV tail tracks instantaneously |
| corners H_Λ / gap / **2 Myr (laneK window)** | 4.680e-11 = 1.0000 | 4.666e-11 = 0.9969 | frozen at orbit-mean f; factor = ⟨g⟩/g_rms = 0.9968 (O(e²), predicted in-script) |
| TILT+ / TILT− (analytic continuum, α=0 self-check 1.2e-06) | 1.21e-10 / 1.81e-11 | 9.40e-11 / 2.33e-11 | tail scales ~y^2α |
| alt footing (CANON) | 5.650e-11 = 1.0000×a₀_alt/2 | 5.650e-11 | |

**Confrontation** (cited 1σ δg bounds, BOUNDS.md §1.2: Venus 8.0e-14, Saturn 7.0e-15 m/s²):

| planet | member band δg [m/s²] | exclusion CANON (canon/alt) | band floor |
|---|---|---|---|
| Venus | [1.8e-11, 1.2e-10] | **585× / 706×** | 226× (TILT−) |
| Saturn | [2.3e-11, 9.4e-11] | **6686× / 8071×** | 3333× (TILT−) |

- **Cross-check vs planetary_doors laneK: agreement.** CANON = laneK Reading A (a₀/2) to <0.5%; exclusions match laneK's 585×/6687× (canon). Trajectory-level dynamics (not just dressing algebra): circular orbits sit on the full dressed law v²/(rg_N)=ν(y) to 0.00% of the anomaly at both planets (AG-c3).
- **MEASURE-INDEPENDENT within the closure family:** no memory corner rescues the planets — **including a corner placed inside laneK's ~Myr Reading-C window** (run explicitly: still a₀/2). laneK's Reading-C escape gates on the ORBITAL frequency, an evaluation **outside** the first-moment closure family this instrument implements (and outside what carries the galactic ν-recovery); Reading B (spectral) is RAR-dead + drift-excluded per laneK. The tilt freedom moves the tail only as y^2α ∈ [0.39, 2.6]× — every alive member stays ≥ **2.4 orders** above its bound (AG-c5).
- **New instrument finding:** the **strict two-body per-star MI-EFE reading DOUBLES the landmine** — measured relative radial residual 9.355e-11 = **1.999×a₀/2** (equals the static per-star algebra to <0.1%): the Sun's own g_bar is dominated by the planet's pull (y_sun~200), so the Sun's a₀/2 tail points at the planet and adds coherently. In the real multi-planet system the Sun-side term is directionally shared among planets — between a₀/2 and a₀; **either way excluded**.
- **Honest ceiling (inherited from the planetary_doors scoreboard):** at 10⁵–10⁸ a₀ GR predicts zero anomaly; this result discriminates between the framework's own doors/closures — it can never prefer the framework over ΛCDM. What it does establish, instrument-grade: **the covariant MI kernel's first-moment closure family is dead at planets by ≥2.4–3.8 orders, both footings, measure-independently** — reported straight.

## (d) Radial / dSph-like orbits — the effective ν for dispersion-supported systems

Deep Plummer field; isotropic-velocity ensemble (launch speed = published circular speed, cos ψ uniform on (0,1], ψ from near-radial ε≈0.96 to near-circular):

| member | ν_eff/ν_circ | D_iso [dex] |
|---|---|---|
| ultralocal | 0.9968 | −0.00139 |
| corner=H_Λ / gap / CANON | 0.9922–0.9923 | −0.00337…−0.00342 |
| TILT+ / TILT− | 0.9946 / 0.9897 | −0.00236 / −0.00452 |

**MEASURE-INDEPENDENT:** dispersion-supported (dSph-like) systems present **ν_eff/ν_circ ≈ 0.990–0.997 (−0.0014…−0.0045 dex, alive-class width <0.01 dex)** — below the circular RAR (AG-d1), with even ε≈0.96 near-radial orbits within 0.02 dex of the pointwise-ν expectation (AG-d3); alt footing same sign/size (AG-d4). Jeans modeling of dSphs with the published ν is accurate to <0.01 dex for any anisotropy **within this kernel's closure freedom** — the often-invoked "dSphs fall below the RAR because of dispersion support" gets, in this theory, at most ~0.005 dex from orbit shape itself.

---

## Ledger

**Measure-INDEPENDENT (forced by the kernel + sum rule across the alive class, all memory corners, both footings):** (a) |RAR offset| < 0.007 dex out to ε≈0.9, sign negative, quantified; (c) the planetary a₀/2-scale residual and its ≥2.4-order exclusion; (d) ν_eff/ν_circ = 0.990–0.997 for isotropic systems.
**BANDED (the honest closure/measure freedom):** (b) γ_v ∈ [1.076, 1.151] with the ultralocal end = the banked 1.09 (AGREEMENT) and the horizon-memory end = the MG value 1.139; (a) the eccentricity memory channel 0…−0.002 dex reproducing the banked rb3 law at small ε.
**Gate honesty:** three originally-failing app gates encoded wrong bookkeeping, not wrong dynamics, and were replaced by gates on what the dynamics actually does — (i) a strict-monotonicity condition below the measured ±3e-05-dex window-sampling floor; (ii) a squared-mean where the banked convention takes the plain mean (the "6.9% discrepancy" it produced was the bug, not physics); (iii) frozen corners initialized at the launch-point f instead of the adiabatic orbit-mean pre-history (the (1+e)² artifact it produced is now the predicted, gated ⟨g⟩/g_rms factor). All thresholds are computed in-script; no hard-coded results.

*This instrument makes the published theory's orbital predictions forced and falsifiable. It does not prove the framework.*
