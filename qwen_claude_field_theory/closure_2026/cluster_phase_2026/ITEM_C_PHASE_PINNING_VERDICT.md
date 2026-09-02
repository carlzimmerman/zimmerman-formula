# Item C — the cluster Helmholtz phase PINS, and what it delivers (2026-09-01)

**Script:** `itemC_phase_pinning_dynamics_2026.py` (rc=0, 27 checks; output in `.out`; `MUTATE=1` flips the lapse relation and the Helmholtz
sign and breaks A4/A5/C1/D3–D5). Builds on items A and B (same DS24 solver, same A2029-type cluster, same μ⁻¹ = 1 Mpc).

## The new equation (from the action, sympy, Part A)
With K(Q) = K₂(Q−Q₀)², Q = Q₀ + u, and the k-essence identities p = L, ρ = Q L′ − L, the AeST Q-sector dust obeys

    p_d = (2πG/μ²) ρ_d²          c_s² = 4πG ρ_d/μ² = u/(Q₀+u) = 2w          (a γ = 2, Lane–Emden n = 1 polytrope)

and in a static well, where Q = (1−Ψ)Q₀ (bridge-1), **c_s² = |Ψ| c²** and ρ_d = −μ²Ψ/(4πG) — exactly DS24's phantom, with SZ2021's
μ² = 2K₂Q₀²/(2−K_B) and G̃ = (1−K_B/2)G. Hydrostatic equilibrium of that polytrope gives ρ_d = μ²(C−Ψ)/(4πG): **DS24's Helmholtz
"oscillation phase" is the polytrope's Bernoulli constant, i.e. its captured mass.** The n = 1 radius π/μ is mass-independent: the
polytrope holds any mass, which is the whole freedom. The v9 DBI K(Q) has the same quadratic term, so the result transfers.

Consequence for the record: the published no-go's premise "c_s² → 0, so the dust is pressureless and clumps by density" holds only on
the cosmic background; inside any well the dust's pressure equals the potential depth. The ordering is by |Φ|, as item B found.

## Why the June "no pin" was the wrong branch (Part B)
The three June solves evolved χ_tt − c_s²∇²χ + (μc)²χ = S. Its static limit is Yukawa (e^{−μr}/r solves it, sin(μr)/r does not).
The phase belongs to the Helmholtz (dust) branch, not the gapped one. The "undamped free mode at ω = μc" is a different mode.

## The pin (Parts B–D, F)
- sign(ρ_d) = sign(u) = sign(c_s²). A static branch with ρ_d < 0 anywhere (dust on a potential hill) has c_s² < 0 there: a gradient
  instability at rate |c_s|k, already 4.5 e-folds per Hubble time at k = μ for |Ψ| = 1e-6, unbounded in k. Not an end state.
- Every one of item A's ten r_ta-matched branches (μr_ta = 8.5 > π) carries a negative-dust region → **all excluded** (C1).
- The physical family is the positive polytrope with a free surface R_s < π/μ (2.9–3.1 Mpc), pure MOND outside; one parameter, the
  captured mass; core yield monotone in it (D1–D3).
- The time-dependent solve in the correct form — 1-D Lagrangian γ = 2 hydro of the dust falling into the growing MOND well — reaches
  hydrostatic equilibrium (force residual 1%, residual motions Mach 0.10), lands on the static polytrope at the same captured mass
  (ratio 1.00), and a ±50% sin(μr)/(μr) free-mode admixture in the initial density changes the core mass by ≤ 3% (F1–F3). **The phase
  is erased by the dynamics, not tracked 1:1.**

## What the pinned configuration delivers — both edges
Captured mass = cosmic dust share f_d M_b(<R500) = 7.6e14 M☉ (f_d = 5.39). Core residual target 1e14 M☉ inside 420 kpc.

| footing / kernel | core dust (<420 kpc) | % of 1e14 | η(R500) predicted | observed η(R500) |
|---|---|---|---|---|
| canonical / DS24 | 3.2e13 | 32% | 3.17 | 2.33 raw, 1.7 WL-corrected |
| canonical / framework | 2.3e13 | 23% | 2.57 | " |
| alt / DS24 | 3.4e13 | 33% | 3.14 | " |
| alt / framework | 2.4e13 | 24% | 2.56 | " |

- **For:** with zero tuning the polytrope reproduces the raw R500 discrepancy to 10% on the framework's own kernel (2.57 vs 2.33) — the
  no-go's "the abundance is not the problem", now with the right profile — and it is galaxy-safe by geometry: a MW-like galaxy holding its
  whole cosmic share has 9e7 M☉ of dust inside 20 kpc against 7e10 of baryons, acceleration shift 1e-4 dex (E1).
- **Against:** the same configuration overshoots the WL-corrected η(R500) = 1.7 on every kernel and undershoots the core. Normalising the
  captured mass to the observed R500 instead leaves the core at 20–25% (raw) / 14–18% (WL). The core share of the captured dust is 3%:
  **the profile ρ_d ∝ C − Ψ is too shallow to concentrate into a 420-kpc core — the shape, not the amount, is the binding limit.**
- The lever scales as (μR)²: at BS24's μ⁻¹ = 22 Mpc it is 0.2% of itself, at the framework's own Q-sector mass (4392 Mpc) nil (D11). It
  exists only at AeST's phenomenological 1 Mpc.

## Standing
The |Φ| Helmholtz lever is **real, predictive (no per-cluster tune), galaxy-safe, and not a closure**: the cluster core gap stays ≥ 65%
open. This corrects two statements in the published cluster no-go (Zenodo 20779562): the pressureless-dust density-ordering premise,
and "the single un-closed branch is a 3-D N-body phase-pinning run" (closed here, in the right dynamics, without an N-body). Layer A untouched; a₀, κ, I₀ never derived here.

## Literature priority (checked 2026-09-01; arXiv + journal texts read, not abstracts only)
| piece of item C | prior art | status |
|---|---|---|
| quadratic shift-symmetric k-essence near its minimum ⟺ dust + Λ with c_s² ≪ 1 | Scherrer 2004 (PRL 93, 011301; astro-ph/0402316); Guendelman–Nissimov–Pacheva 2016 (EPJC 76, 90; 1511.07071, explicit duality) | **known** |
| quadratic kinetic Lagrangian ⟺ γ = 2 (n = 1) polytrope, p ∝ ρ² | Chavanis 2021 (2109.05963) eq. (89): for γ = 2 the k-essence Lagrangian is L = P = (1/4K)[θ̇ + ½(∇θ)²]², quadratic in the kinetic variable | **known** (BEC/Madelung context) |
| n = 1 polytrope: sin(kr)/kr profile, radius π/k independent of mass | Böhmer & Harko 2007 (JCAP 06, 025), Thomas–Fermi BEC dark matter | **known** |
| AeST oscillatory regime carries negative energy density / negative mass; "condensates with negative energy density are unstable"; stability analysis in a galactic background not done; "typical for condensate models"; SFDM analogy (condensate continued by a normal phase); solutions **truncated where the condensate density first drops to zero** | Mistele, McGaugh & Hossenfelder 2023 (A&A 676, A100; 2301.03499) §3, Fig. 4 | **known** — the free-surface prescription of Part D has this priority (as a conservative truncation, flagged speculative there) |
| the μ²(Q−1)² term's k < μ instability is Jeans-type, Hamiltonian positive for k ≥ μ | Blanchet & Skordis 2024 (JCAP 11, 040; 2404.06584) §5 | **known** |
| ghost-condensate stability requires the P′ ≥ 0 side of the minimum (c_s² ≥ 0); positive-energy dust ⇒ Q > Q₀ | Arkani-Hamed–Cheng–Luty–Mukohyama 2004 (hep-th/0312099); in-repo Door A (2026-06-19, Serra–Trombetta positivity) | **known** |
| DS24 / VSB24 treat the boundary constant χ_out as "a free parameter"; DS24 speak of "apparent χ condensates"; neither identifies the scalar as a polytrope, a hydrostatic fluid, or gives a sound speed inside wells; DS24's "isothermal" is the baryonic gas | Durakovic & Skordis 2024 (2312.00889); Verwayen, Skordis & Bœhm 2024 (2304.05134) — full texts searched for polytrope / Lane-Emden / Bose / Thomas-Fermi / hydrostatic / sound speed: 0 hits on the scalar | confirms the gap |
| **the identification itself**: DS24's Helmholtz equation for Ψ IS the Lane–Emden n = 1 hydrostatic equation of the AeST Q-sector dust, p_d = (2πG/μ²)ρ_d², with the free constant = captured mass, and c_s² = \|Ψ\|c² inside a well (the AeST ↔ Thomas–Fermi-BEC mapping, μ ↔ polytropic constant) | none found (searched AeST 2021–2026, BEC/SFDM, k-essence halo literature incl. Armendariz-Picon & Lim 2005) | **new as stated** — assembled from known pieces, not previously assembled |
| the cluster application: every r_ta-matched Helmholtz branch excluded by positivity; the phase pinned to the unique positive polytrope by the captured mass; the γ = 2 hydro landing on it IC-blind; the 23–33% core yield with the R500 overshoot; the (μR)² fork | none found | **new** |

Net: the equation is a re-derivation in AeST variables of known condensate physics (Chavanis/Böhmer–Harko), and the "cut at the first zero" is Mistele et al. 2023's prescription; what is new is the mapping being made explicit for AeST, the instability made quantitative (rate |c_s|k), and the consequence for the cluster phase problem. Cite all of the above when writing it up. "Mistele & Durakovic 2024" (a search-summary artefact) does not exist; the only AeST cluster paper is DS24.
