# K1_braneworld_weyl: is cold energy a "dip into another dimension"?

The idea is the owner's: "what if cold energy is kind of like a black hole, a dip into another dimension." The coordinator
mapped it to braneworld gravity. Our 4D world is a brane in a 5D bulk. Bulk gravity reaches the brane as the projected
Weyl tensor E_μν. That acts like a traceless "Weyl fluid" (dark radiation) which gravitates but is not brane matter.

## Verdict: FAILS (frozen rule), on both footings, for every closure

No closure reaches PARTIAL. Both bulk-supplied versions fail the cluster cores. In detail:

- **C0, vanishing anisotropic stress (P = 0).** This is the only closure tied to the cosmological dark radiation.
  - Under the BBN bound it supplies 6e-13 of the law in the cluster MID bins, against 0.54–0.72 needed. That is short
    by about 10¹².
  - Calibrated on MID instead, it needs a Weyl density of 1.3e6 ρ_crit, i.e. ΔN_eff ≈ 1.1e11 against a bound of 0.30.
  - Its profile tracks the potential, so it ramps outward. The cluster outskirts come out at 0.25–0.29 of the
    prediction (Z −26 to −34). Isolated galaxies get +110–150 % at 1.1–2.6 Mpc. The dwarf satellites get nothing
    (residual stays at +0.95 / +0.91 dex).
- **C1, Harko–Cheng isothermal (P = U).** The cluster outskirts come out at 0.64–0.68 (Z −5 to −6). Isolated galaxies
  get +24–33 %. Dwarfs are still short by +0.52 to +0.56 dex. The Sun gets 4e6–1.5e8 × the planetary bounds.
- **C2, tidal charge per mass element (P = −2U).** This is the exact "black hole on the brane" form (DMPR).
  - It is the only compact profile, and it comes closest on the cluster shape. The profile χ² is 7.0–16.0 against a
    line of 11.07. But the outskirts sit at 0.75–0.80 (Z −2.8 to −4.0), and the inner bins are overshot (0.62–0.73).
  - It passes the isolated galaxies (≤ +13 %).
  - The same kernel overshoots the dwarfs by 2.4–2.5 dex. It gives the planets 10²⁰–10²³ × their bounds.
- **Bulk-supplied RS2 (Garriga–Tanaka), with ℓ ≤ 0.1 mm:** about 10⁻⁵³ of the law at 0.8 Mpc, short by about 10⁵¹.
- **Bulk-supplied DGP:** an anti-selector. The fractional boost at 0.8 Mpc is 0.04 for a cluster and 0.11–0.32 for a
  galaxy. Its maximum, 1/(3β) ≤ 0.33, is below the 0.68 needed.

κ = ½ is FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. No dark-matter particle. The
theory is not closed. Nothing here says the data favour the framework.

## Part A: what the brane equations say (sympy, DERIVED; checks K1–K4)

- **One free function.** Take the static spherical metric with matter and the Weyl fluid (U, P).
  - The unknowns are ν, λ, U and P.
  - The independent equations are tt, rr and the Weyl conservation law (U + 2P)′/3 + ν′(4U + 2P)/6 + 2P/r = 0.
  - θθ follows from these by the Bianchi identity (residual 0).
  - So one function is left free. That is the closure problem: only a bulk solution, or a postulate, fixes it.
- **The Weyl amplitude is a bulk datum.** Brane matter sources E_μν only through π_μν ∝ ρ²/λ_b. With λ_b ≥ (1 TeV)⁴ that
  is 8e-56 of the matter source at a cluster centre, 8e-53 at a galaxy centre and 7e-28 at the solar centre. At low
  energy the Weyl sector is source-free on the brane. Nothing on the brane ties the Weyl mass to a cluster's baryons.
- **Universal slip, for any closure.** The Weyl fluid is traceless. To leading order in Φ/c² its dynamical mass grows as
  2U, its lensing mass as (3/2)U and its curvature mass as U. So the **Weyl lensing/dynamics ratio is 3/4.** A
  Weyl-supplied cluster excess would read 4/3 larger in dynamical or hydrostatic masses than in lensing.
- **The closures, solved (K2):**
  - P = 0 gives U ∝ e^{−2ν} exactly. This is radiation in a Tolman equilibrium.
  - P = wU gives U ∝ r^{−6w/(1+2w)}. Flat rotation curves (Harko–Cheng) need w = 1, i.e. U ∝ r⁻². The DMPR case w = −2
    gives U ∝ r⁻⁴.
  - The DMPR metric e^ν = e^{−λ} = 1 − 2GM/rc² + Q/r² solves the vacuum brane equations exactly, with
    U = Qc²/(8πGr⁴) and P = −2U.
- **C0 is an AeST mass term.** Linearised, δU = −4U_∞ψ/c². That gives ∇²ψ + μ_W²ψ = 4πGρ with μ_W² = 32πGU_∞/c², the
  relativistic Jeans wavenumber of the dark radiation (K3). It is H2's μ²Φ dust, with lensing weight 3/4. The calibrated
  μ_W ≈ 0.88–0.92 Mpc⁻¹ is the regime where H2 already failed.
- **C2 tracks the density gradient.** The Fourier transform of 1/r² is 2π²/k. So Φ_W,k = −2π²Gℓ_Q ρ_k/k, i.e.
  ρ_eff = (πℓ_Q/2)(−∇²)^{1/2}ρ_b, the half-Laplacian of the baryon density.
- **On FRW the Weyl term is dark radiation** (ρ_W ∝ a⁻⁴, w = 1/3; K4). It cannot be the CDM-like dust that growth needs
  (H1). **v4's dust is still required.**
- **Point-source C2 lensing.** For Φ = −GMℓ/r² the projected potential is −πGMℓ/R. So M_cyl = πMℓ/(2R) and
  Σ = −Mℓ/(4R³). Then ΔΣ_dyn = 3Mℓ/(4R³), and the lensing value is (9/16)Mℓ/R³.

## Part B: one constant per closure, calibrated on F1 MID only, then no refit

The calibration uses F1 PRIMARY exactly: F1's cache (sha256 961ea4fc…e720), AQUAL, native h 0.672 / 0.686, eRASS1 gas
rescaled, β-model, f* = 0.20, data boost and miscentring. My copy of F1's law reproduces F1's PRIMARY A_MID and A_OUTER
exactly (K5). Values below are for the h 0.672 calibration, canonical / alt. The h 0.686 cells are in the `.out` and lead
to the same verdict.

| | C0 (P = 0, LINK to FRW) | C1 (P = U, Harko–Cheng) | C2 (P = −2U, tidal kernel) |
|---|---|---|---|
| constant | U_∞ = 1.36e6 / 1.27e6 ρ_crit | ξ₁ = 0.40 / 0.32 | ℓ_Q = 1.19 / 1.03 Mpc |
| what the Weyl mass tracks | the potential ψ (flat: 4.8e-5 → 1.7e-5 c² from 0.1 to 2 Mpc) | a fixed r⁻² law, amplitude ∝ √M_b | baryon density gradient |
| F1 OUTER, data/pred | 0.267 / 0.291 (Z −29 / −26) | 0.675 / 0.657 (Z −5.1 / −5.5) | 0.795 / 0.753 (Z −2.8 / −3.5) |
| profile χ², bins 3–7 (line 11.07) | 690 / 571 | 21.7 / 25.3 | 7.0 / 10.5 (h 0.686: 11.5 / 16.0) |
| INNER, data/pred | 2.20 / 2.05 | 0.87 / 0.91 | 0.68 / 0.73 |
| isolated galaxies, Weyl/law, O1 and O2 (line 0.14) | 0.17 and 1.40 / 0.14 and 1.11 | 0.30 / 0.24 | ≤ 0.12 / ≤ 0.10 **PASS** |
| dwarf satellites, residual after (E3 +0.95 / +0.91) | +0.95 / +0.91 (28 M☉ added) | +0.54 / +0.56 | −2.49 / −2.43 (overshoot) |
| Solar System, worst a_W/bound | 1.6e-8 **PASS** | 1.4e8 (Mars) | 5.9e23 (Mars) |
| BBN ΔN_eff (bound 0.30) | 1.1e11 / 1.0e11 | not linked | not linked |
| status | FAILS | FAILS | FAILS |

**Compactness (A2, median cluster, canonical): Weyl lensing mass / gas mass at 0.5 / 1 / 2 / 3 Mpc.** F1 needs about
1.4–1.8 inside 1 Mpc and about 0 outside.
- C0: 3.5 / 9.9 / 23.7 / 24.9. This is a ramp, because the Weyl density follows |ψ|. Its half-mass radius is 1.81 Mpc,
  against 1.59 Mpc for the gas.
- C1: 4.8 / 3.9 / 3.5 / 3.4. The same fraction at every radius.
- C2: 5.5 / 2.7 / 1.4 / 1.7. This is the only one more concentrated than the gas, and it is too concentrated inside
  0.5 Mpc.

None is zero beyond 1 Mpc.

**R4, cosmology.** C0's LINK makes U_∞ today's dark-radiation density. The calibrated value is Ω_W h² ≈ 6e5, so the
universe would be radiation-dominated today. Conversely, the BBN cap |ΔN_eff| ≤ 0.30 (A78's conversion; Ω_γh² from C2)
caps the cluster MID excess at 5.9e-13 of the law. C1 and C2 have no static-to-background link, so BBN does not test
them. On any closure, the FRW Weyl term is dark radiation, so the growth dust must still come from v4.

**Bulk-supplied lines.**
- **B1, RS2.** The correction is 2ℓ²/3r² (dynamics) and ℓ²/2r² (lensing). At 0.808 Mpc with ℓ = 0.1 mm the lensing value
  is 8e-54, or 8e-52 with a generous ×100 extended-source log factor. That is short of the 0.54–0.68 needed by about
  10⁵¹. Making it work needs ℓ ≈ 0.94 Mpc, which is 3e26 × the table-top bound. Gravity would then be five-dimensional
  below that scale, so the Solar System would be off by about ℓ/AU ≈ 2e11.
- **B2, DGP** (r_c = c/H₀, decoupling limit). At 0.808 Mpc the cluster (7e13 M☉, Vainshtein radius 2.3–4.9 Mpc) gets
  δ = 0.037–0.042. The galaxy (10^10.83 M☉, Vainshtein radius 0.23–0.48 Mpc) gets 0.11–0.32. Deep potentials get *less*
  boost.

## J1's lesson, applied (A2)

J1 (3d75573e2c) found that a |Φ| selector overshoots the outskirts, because |Φ| is flat across a cluster. It also found
that satellites sit in shallower host potential than the Sun.
- **C0's Weyl mass tracks Φ.** It inherits both of J1's failures, and the outskirts are worse (0.25–0.29 vs J1's
  0.60–0.62), because a density ∝ |ψ| gives mass ∝ r³.
  - Its boost relative to the law scales as (μ_W r)². That is a radius selector, not a depth selector: isolated galaxies
    at 1–2.6 Mpc get as much as clusters.
  - For satellites its variable is host depth, which J1 showed is the wrong variable: 28 M☉ is added.
- **C1 tracks nothing local.** It is a fixed power law with a per-object amplitude.
- **C2 is the density-like candidate.** It tracks ∇ρ_b through a 1/d² kernel, so it is compact. That is why it comes
  closest on F1's shape and passes the isolated galaxies.
  - Its satellite variable is the system's own size (ℓ_Q/r12 ~ 10⁴), and its Solar System variable is ℓ_Q/AU ~ 10¹¹.
  - A scale selector of this kind always boosts small systems most. It is the opposite of the ordering needed.
- **Conclusion for J1.** The braneworld Weyl term is not a physical origin for a potential-depth selector. Its only
  depth-dependent closure (C0) is BBN-capped 10¹² too weak, and it has the wrong shape.

## The literal reading (one paragraph, as instructed)

The coordinator's check is cited, not recomputed. A population of black holes or compact objects clusters like particle
dark matter. It would build halos around isolated galaxies, which F2's outer stack does not need (A_O2 0.96–1.04 ± 0.07).
The one-object version, one "brane black hole" per system, is the DMPR tidal-charge solution, computed here as C2. It can
partly shape a cluster profile. But the same rule then gives every dwarf and the Sun an enormous extra pull.

## What this does not show

- **No bulk solution exists for an extended static source.** With one free Weyl amplitude per object (a bulk datum), the
  Weyl term can be fitted to anything, the way a halo can. That is a fit, not a prediction, and it is what stays open.
  - A 5D numerical bulk solution for a cluster could in principle supply a closure that is not on this list.
- **A-ADD is a postulate.** Weyl gravity is added to the law and not fed through the AQUAL scalar. A trace-coupled scalar
  would not see the traceless E_μν anyway.
- **Not modelled:** asphericity, a time-dependent bulk, and the high-energy π_μν term (≤ 1e-52).
- **External inputs, not verified on disk:**
  - the SMS equations, RS2/Garriga–Tanaka, DMPR, Mak–Harko / Harko–Cheng, DGP;
  - the (1 TeV)⁴ and 0.1 mm bounds.
  - Their static consequences are re-derived here where possible.
- **The dwarf baseline uses E3's central values** (+0.95 / +0.91), not E3's Monte Carlo (+0.886 / +0.846); K9 shows the gap.
- **The C2 isolated-galaxy line is graded on the analytic point-source formula** (A3), not on the projector.

## Checks, runs, files

Checks 9/9 PASS, exit 0. The run takes 92 s on one thread under nice 15, with a peak RSS of 0.85 GB.
`--mutate` drops the Weyl radial pressure from the rr equation. K1 and K3 then FAIL (7/9, exit 1), as frozen.
- K1: Bianchi, the divergence identity, the TOV limit and Weyl conservation.
- K2: the closures.
- K3: the slip and μ_W².
- K4: a⁻⁴, and A78's 7.4492.
- K5: F1 reproduction (dev 0, sha).
- K6: my signed projector vs F1's (1.3e-4).
- K7: the C0 solver vs sin(μr)/μr (3.6e-6) and the test-fluid limit (1.6e-7).
- K8: the C2 far field (4.3e-4 at ≥ 100 b; 1.4e-3 at 50 b, as A1 predicted).
- K9: E3 baseline (+0.060 / +0.063).

Files:
- `FROZEN_CRITERIA.md`: e78d6d2516, plus amendments A1 and A2 (pre-result, 7d3710054d) and A3 (post-result).
- `ASSUMPTION_LEDGER.md`.
- `k1_braneworld_weyl.py` writes `.out` and `_results.json` (every number above).
- `*_MUTATE.*`, and `*_RUN1.*` (first run, kept; see A3).

Run:
`OMP_NUM_THREADS=1 nice -n 15 python3 k1_braneworld_weyl.py <dir holding F1's f1_meas.pkl> [--mutate]`.

Record checked: W4-01 (DGP, κ only), A34 (dimension route), CFG254 R3 (brane contact, untestable as stated), the Gemini
idea-10 review (DGP leakage), H2 (AeST μ²Φ), J1 (|Φ| selector), F1, F2, E3, C6, A78. None had computed the projected
Weyl term against these data.
