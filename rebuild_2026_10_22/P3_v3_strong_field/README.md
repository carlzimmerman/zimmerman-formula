# P3_v3_strong_field: v3 (Khronon + P) at black holes, in ringdown, in neutron stars, and its strong coupling

## Verdicts (frozen rules, FROZEN_CRITERIA section 3 + amendments A1, A2)

| tile | verdict | the number that decides it | bound used (strict floor) |
|---|---|---|---|
| Black holes (EHT) | **PASS** (static, non-rotating) | Regular stationary horizons exist for every benchmark. Largest shift: 1.25e-3, which is the law's offset on M87*'s 100 pc dynamical mass. The strong-field shape (shadow, photon sphere, ISCO) moves by at most 2.9e-11. | 1e-2 (EHT ~10%) |
| Ringdown (LIGO) | **PASS** | Eikonal QNM shifts are at most 2.8e-11 (M87*) and about 1e-24 for 10-63 Msun. Energy leakage into the khronon pair is at most 5.5e-18 per cycle. | 1e-2 (GW250114 "few percent") |
| Neutron stars | **PASS** | dR/R at 1.4 Msun is at most 2.7e-28; dM_max/M_max at most 5.6e-28; the timing-mass offset (orbit 1e9 m) at most 2.6e-18. The cap is never reached (u/a0 <= 2.6e-5). | 1e-2 (NICER ~10%) |
| Strong coupling | **PASS (estimate)** | Worst loop factor is eps = 1.3e-3, for Eot-Wash (38.6 um) at L* = 90 pc. In the lab the strong-coupling momentum is 1.4-2.9e5 m^-1, i.e. 3.5-7 um. Every other declared system is below 1e-40. | eps <= 1e-2 |
| Leaf/lapse condition, strong field (static spherical) | **PASS** | On every regular BH exterior and both SLy stars, N > 0 and u < a0 strictly, so the leaf operator stays elliptic. | C8's conditions |

- **Checks: 17/18 PASS, exit 1.** The one FAIL is B1, a frozen line kept FAIL; amendment A1(a) recorded it before the script existed.
  - B1 expected T^r_r to diverge like e^(-1/2) on the static branch. It does not. The static branch is still singular, but through its tangential stress and the K(Q) dust (see finding 2).
- **Mutation.** `P3_MUTATE=1` sets xi = 2. It breaks A1, A3 (as frozen) and A4 (14/18).
- **Run cost.** 173 s, 0.15 GB RSS, one thread, nice 15, no downloads. Runs are deterministic: the script re-executes itself with PYTHONHASHSEED = 0.
- **Commits.** Criteria frozen first (f28b8c6a92). A1 (c58afc3b20) and A2 (988eb4940d) were added before the lane script existed.

kappa = 1/2 FITTED. Footings 9.36e-11 / 1.13e-10 m/s^2, never pooled. No dark-matter particle. Not "theory closed".
Nothing here says the data favour the framework.

## Findings

1. **PG-Schwarzschild is an exact v3 solution (DERIVED, A2; residual 0).**
   - Schwarzschild with the khronon on Painleve-Gullstrand leaves and P = 0 solves all five reduced field equations exactly, for any gamma_L, mu_K and any W with W(0) = W'(0) = 0.
   - It is the only stationary P = 0 foliation of Schwarzschild. The p equation forces N' = 0, and the khronon equation with mu_K > 0 then forces N = 1.
   - So a regular black hole with zero deviation exists. Its foliation, though, carries no MOND field.
2. **The foliation the weak-field law uses is singular at the horizon (COMPUTED, B1 reading).**
   - On the static foliation Q = 1/N grows without bound at r = 2M. The Killing horizon is then a universal horizon of that foliation.
   - The BS dust stress mu^2 Q^2 grows like 1/e. The tangential clock stress and the on-shell scalar L_P grow like e^(-1/2) (exponents -0.96 to -0.50).
   - The invariant T.T diverges, with exponents down to -1.95 for the SMBHs.
   - The cap is reached at the horizon (1 - u/a0 <= 5e-18 at e = 1e-8).
   - **So a v3 black hole needs the khronon tilted (infalling) near the horizon.**
3. **Regular stationary families that match a static exterior exist (COMPUTED, B2-B4, A4, C3).** These are linear response on Schwarzschild, exact in the a_hat -> 0 limit.
   - **Screened, sigma = a0 L*^2/(2GM) >= 1/2.** This covers stellar BHs and Sgr A* at 90 pc.
     - The static-like and PG-like branches cross at an X-point. There kappa* = 1.493801, r_c = 3.6514 M and N_c = 0.7676.
     - The transonic solution is regular at the horizon, with N(2M) = 0.6265.
     - Its khronon charge is fixed: c = kappa* (1/sigma + eps_mu).
   - **Capped, sigma < 1/2.** This covers M87* and Sgr A* at 20/24 pc.
     - Here u -> a0 near the hole: the cap is approached, with 1 - u/a0 = a_hat/(w + a_hat) <= 4e-10, but never reached.
     - There is no critical point, so the charge c is free. Every c up to 1.35-1.40 gives a regular exterior.
   - **Checks on these solutions.**
     - The stress tensor is conserved to 1.3e-7.
     - The khronon integral is constant to 1e-12.
     - r^2 T^r_t = c exactly.
     - T^v_v and T_rr(EF) stay finite at r -> 2M.
4. **Clock identity (DERIVED, A1).**
   - P.A = div P - D.P holds for any P orthogonal to n. So the clock term is -xi D.P up to a total divergence.
   - P therefore enters v3 only through its leaf divergence D.P and |P|.
   - The divergence-free q/r^2 mode drops out of every field equation at O(a0). That is why the shifts do not depend on p(2M).
5. **The khronon/dust pair propagates where the phantom density D.P > 0 (COMPUTED, A2: first order in background gradients).** This corrects the reading of C5/C8 that "only tensor modes propagate".
   - C5's frozen-coefficient matrix drops every background-gradient term. The pair's gradient energy is entirely such a term: G = D.P (1 + gamma_L D.P) + mu_K^2 (Qbar - 1)/(K Qbar). It comes from the exact spherical first integral.
   - The kinetic term is Z = k^2/(Qbar^2 (K M_L + gamma_L k^2)) + mu_K^2/K. E1 and E2(i) check it against C5's unitary gauge: residual 0.
   - **Speeds c_pi = sqrt(G/Z):**

     | where | c_pi (units of c) |
     |---|---|
     | Solar System and lab | 1.0e-4 |
     | double pulsar | 2.1e-3 |
     | stellar BH at 3M | 0.33 |
     | NS surface | 0.44 |
     | capped SMBHs | 6.7 (M87*) and 260 (Sgr A*), superluminal |

   - **Coupling to metric perturbations is tiny.** The mixing eps is at most 2.4e-9 for BHs and 2.0e-9 for the double pulsar, so the leakage is about 4e-18. That is far below Pdot_b's 6.3e-5 precision. C8's binary-pulsar conclusion survives.
6. **A new reading: regular v3 black holes accrete khronon-sector energy (COMPUTED from r^2 T^r_t = c).**
   - The rate is dM/dt / M = c a0/c_light. Per Gyr that is 9.9e-3 c for the canonical footing.
   - Sgr A* at 90 pc (transonic, c = 2.36): 2.3% per Gyr.
   - M87* / Sgr A* in the capped family: c is free, so anywhere from 1e-4 to 1.4% per Gyr.
   - Stellar BHs: below 1e-5 per Gyr.
   - Not scored: c is not fixed for SMBHs, and the flux needs a khronon reservoir at large r.

## Numbers

**Black holes.** Each shift is the coefficient times a_hat. "Local" means the mass is normalised at 50 M, so it includes the
phantom a0-tail between 3 M and 50 M.

| benchmark | sigma (24 pc, canonical) | a_hat | member type | local shadow / QNM shift | dynamical-mass shadow shift |
|---|---|---|---|---|---|
| M87* 6.5e9 Msun | 3.0e-5 | 1.0e-14 | capped, c 0.01-1 | <= 2.3e-11 (2.8e-11 alt) | 1.03e-3 (1.25e-3 alt): the law's offset a0/g_N at 100 pc |
| Sgr A* 4.3e6 Msun | 0.045 (0.63 at 90 pc) | 6.6e-18 | capped (transonic at 90 pc) | <= 1.5e-14 (1.8e-14 alt) | 1.5e-8 (1.8e-8 alt) at 2000 AU |
| 10 Msun | 1.9e4 | 1.5e-23 | transonic | <= 1.3e-24 | n/a |
| 63 Msun | 3.1e3 | 9.7e-23 | transonic | <= 5.3e-23 | n/a |

- **The old chassis for comparison** (CFG318: alpha_c khronometric): shadow 3.85e-12, QNM damping 2.04e-10, NS M_max 2.9e-9.
- v3's strong-field shape shifts are of similar size (<= 2.9e-11). Its NS shift is about 1e19 times smaller, because P is screened and v3 has no a^2 term.
- The largest BH number, 1.25e-3, is not a strong-field effect. It is the law acting on M87*'s stellar-dynamics mass at r_dyn = 100 pc (illustrative).

**Strong coupling** (A69-style estimate). The dominant vertex is the clock nonlinearity pidot (grad pi)^2, with
lambda_3 = Z_P/2 (exact coefficients c_tt = c_zz = c_tilt = 1). The scale is Lambda^2 = Z^(3/2) c_pi^(7/2)/lambda_3 and the loop factor is
eps = (c_pi k/Lambda)^4.

| system | c_pi | k_sc (m^-1) | eps (worst vertex) |
|---|---|---|---|
| Eot-Wash 38.6 um, L* 20 / 24 / 90 pc | 1.0e-4 | 2.9e5 / 2.6e5 / 1.4e5 | 6.5e-5 / 9.3e-5 / 1.3e-3 |
| planets, 1 AU | 9.9e-5 | 2.6e5 | 5e-67 |
| double pulsar | 2.1e-3 | 2.5e6 | 4e-62 |
| NS surface | 0.44 | 1.3e8 | 6e-48 |
| BH 10 Msun at 3M | 0.33 | 9.6e7 | 2e-49 |
| galaxy, cosmology | 1.6e-4, 1.2e-5 | 3e4, 1e3 | < 1e-96 |

- The scale goes as k_sc ~ L*^(-1/2). It does not depend on the footing.
- The tightest margin is Eot-Wash at L* = 90 pc: a factor 1.7 in k, 7.6 in eps.
- **Gravity tests below about 5 um would probe the pair's strong coupling.**

**Neutron stars (SLy).** M_max = 2.04845 Msun (CFG318 2.0485).

| L* | dR/R (1.4 Msun) | dM_max/M_max | (R/L*)^2 | timing-mass offset |
|---|---|---|---|---|
| 24 pc | -1.9e-28 | -3.9e-28 | 2.5e-28 | 1.8e-18 |
| 90 pc | -1.3e-29 | -2.8e-29 | 1.8e-29 | 1.3e-19 |

## Replacement tiles for the board (`explainers/make_status_board.py`, column 0; evidence lane `P3`)

| tile | colour | note |
|---|---|---|
| "Black holes (EHT, LIGO ringdown)" | PASS | regular horizons need a tilted khronon; shifts <= 3e-11 (shape), 1.2e-3 via M87*'s dynamical mass; moving/rotating BHs open |
| "Strong coupling" | PASS (estimate) | khronon pair weakly coupled at every declared system; tightest Eot-Wash 38.6 um, eps 1.3e-3 (L* 90 pc); breaks down below ~5 um |
| "Lapse condition, realistic matter" | PASS (static spherical) | leaf operator elliptic on BH exteriors and SLy stars (N > 0, u < a0); non-spherical strong fields open |
| new: "Neutron stars (NICER, 2 Msun)" | PASS | dR/R <= 2.7e-28, dM_max/M_max <= 5.6e-28, cap not reached |

## What this does not show

- **Moving and rotating v3 black holes are not computed.**
  - This is CFG319's "hidden inner-horizon defect" question (Ramos-Barausse type).
  - v3's effective khronometric alpha near a hole is O(a_hat), so any such singularity would have amplitude of order a_hat v. That is an estimate, not a computation.
- **Solution families and interiors.**
  - The interior r < 2M of the regular members is not computed. Neither is any universal horizon there; the BS dust diverges at a universal horizon, Q -> infinity.
  - Junction-type members (screened outside, capped inside) are not computed (A1(b)).
  - The SMBH khronon charge c is not fixed. The observables vary by about 1% across c.
- **The strong-coupling result is an estimate.** It rests on the decoupling limit, first order in background gradients, and O(1) loop factors.
- **G < 0 regions are untested.** Where the phantom density is negative (AQUAL saddles between masses), G < 0 at this order, so the pair would be gradient-unstable. No declared system has G <= 0 (E4); a dedicated non-spherical lane is needed.
- **Bounds and inputs.**
  - The EHT, GW250114, NICER and Cromartie bounds are record transcriptions or memory (PROVISIONAL). The 1e-2 floors make the PASS lines insensitive to them.
  - The benchmark masses, r_dyn values and the galactic phantom density are ILLUSTRATIVE.

## Input ledger

| input | class | source |
|---|---|---|
| v3 action (beta = eta = gamma_F = 0, xi = 1, capped W, gamma_L = K L*^2/2) | FRAMEWORK-NATIVE | C4, C5, C8, THEORY_V3_DRAFT |
| K(Q) = mu_K^2 (Q-1)^2, mu_K^-1 = 100 kpc | literature via C4 (BS24 Eq. 7, 39), not on disk | C4 README |
| a0 footings, L* 20/24/90 pc | FITTED (kappa = 1/2) | doors BRIEF, D10, C5/C8 grids |
| SLy piecewise polytrope | external EOS, CFG318's recalled parameters (PROVISIONAL) | CFG318 script |
| EHT ~10%, GW250114 few %, NICER ~10%, 2-Msun ~5%, Lee+2020 38.6 um | record transcriptions / PROVISIONAL | FROZEN_CRITERIA section 4 |
| masses, r_dyn, galactic phantom 0.01 Msun/pc^3, Omega_K = 0.26 | ILLUSTRATIVE | this lane |
| eikonal light-ring QNM map; A69 loop-factor method | ADOPTED methods | CFG318; A69 section 4 |

No LambdaCDM-processed or standard-MOND machinery carries a verdict. The unscreened strong-field law offset is the
theory's own AQUAL limit.

Files: `p3_v3_strong_field.py`, `.out`, `_results.json` (main); `_MUTATE.out`, `_results_MUTATE.json` (mutation).
Run: `OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/P3_v3_strong_field/p3_v3_strong_field.py`.
