# CFG156 — independent re-derivation of CFG131's sound-speed headline (door 8, interacting vacuum). FROZEN CRITERIA

Written 2026-09-29, before any script or number of this lane. This is a referee lane in the CFG84–86 way: my own code, built from CFG131's frozen question and README only. CFG131's numbers below were READ from its README before any code, so they are targets, not blind predictions. Nothing is committed (the run's instruction). The sha256 of this file is printed at the top of every output of this lane, so a later edit is visible.

## The headline under test (CFG131 README, item 3, row R2)

The cold fluid's sound speed that the interacting vacuum can provide is c_s² ≤ 4.6e-12 (in units of c²). The target's hydrostatic support requires 2e-8 to 6e-7.
- **Model side, as quoted.** The Q-consistent fluid needs c_s² ≤ 1.7e-8 (k = 0.5/Mpc), 1.0e-9 (k = 2), 4.2e-11 (k = 10) and 4.6e-12 (k = 30) for 5% growth to z = 0. Read at z = 10, the bound runs from 1.5e-7 (k = 0.5) to 4.3e-11 (k = 30).
- **Target side, as quoted.** c_s² = V_f²/2c², about 2e-8 at M_b = 1e9 M☉ and 6e-7 at 1e12 M☉. It uses the point-mass target with the P2 law.
- **The ordering, as quoted.** The requirement is 4.3e3 above the bound at k = 30.
- **Secondary row (it falls out of the target side).** The required pressure at matched ρ_c differs 32–272x between 1e9 and 1e12 M☉ (point mass, exact). The exponential-sphere range (32–353x) is out of scope.

## Pins (my reading of the README; each is a declared choice)

- **Target.** CFG44's point mass under the P2 law:
  - x = r/r_M and r_M = √(GM_b/a₀);
  - ρ_c = a₀/(4πG r √(1+x²)) and g_tot = √(g_N² + g_N a₀);
  - V_f² = √(G M_b a₀).
- **Range.** Masses 1e9, 1e10, 1e11 and 1e12 M☉, with x in [0.1, 30].
- **Footing.** a₀ = 9.3603e-11 m/s² (canonical) is the pass footing. The alt footing, 1.1312e-10, is reported.
- **The required c_s² is dP/dρ**, from hydrostatic equilibrium dP/dr = −ρ_c g_tot:
  - c_s² = (dP/dr)/(dρ_c/dr), which needs no boundary condition;
  - P/ρ is reported beside it, with P(∞) = 0;
  - both tend to V_f²/2 as x → ∞, which is the README's number. So the README quotes the flat-regime value.
  - I compare the smallest requirement over x in [0.1, 30]. The x → ∞ value and the largest value over the range are reported.
- **Model.** Q = Q(ρ_L, ρ_c) under CFG131's H1–H4.
  - The model's sound speed is c_s² = (ρ+p) Q_ρ/Q.
  - For the declared power law Q = ξ ρ_c^n ρ_L^m, it is n(1+w). That is one number in the background and in every halo.
- **"What the model can provide"** is the largest constant c_s² that passes G2: the total-matter growth ratio to ΛCDM is ≥ 0.95 at z = 0, at k = 0.5, 2, 10 and 30/Mpc. The bound is set by k = 30.
- **R2 is read as the pure sound-speed bound.**
  - The exchange-rate term aΓ(1−n)δ_c in the continuity equation is set to zero (Γ → 0 at fixed n).
  - The background is ΛCDM.
  - The README's four numbers scale as k⁻², as this reading predicts.
- **Growth conventions.** These are taken from CFG131's frozen question; CFG43 itself was not read.
  - Two fluids: Ω_c = 0.265, Ω_b = 0.050 and Ω_Λ = 0.685. The universe is flat, with no radiation.
  - The run starts at z = 1000 with δ_c = δ_b = a and dδ/d ln a = a.
  - Baryons are pressureless and coupled by gravity only.
  - The equations are sub-horizon and Newtonian. In the rest frame δp = c_s² δρ, and gauge terms are of order (aH/k)².
  - k is in Mpc⁻¹, with H₀ = 67.4 km/s/Mpc.
  - The growth ratio is δ_m(model)/δ_m(ΛCDM) at the same k and z, with δ_m = (Ω_c δ_c + Ω_b δ_b)/(Ω_c + Ω_b).

## Method

**(a) Target side.**
- Build ρ_c and g_tot on a log grid of 2001 points in x in [0.1, 30] for each mass.
- Compute P(r) = ∫_r^∞ ρ_c g_tot dr′ by quadrature, so P(∞) = 0.
- Take dP/dρ from the grid by centred differences in ln x, and P/ρ from the same P. Convert both to units of c².
- My closed forms, from CFG44's formulas:
  - P = a₀M_b/(8πr²) and P/ρ_c = V_c²/2;
  - dP/dρ_c = V_c²(1+x²)/(1+2x²), with V_c² = (GM_b/r)√(1+x²);
  - both requirements tend to V_f²/2 as x → ∞.
  - The solver must reproduce these (control CT3).

**(b) Model side.**
- **B1 (sympy, on an explicit metric).** The metric is ds² = −N(t,r)²dt² + A(t,r)²dr² + B(t,r)²dΩ², with the cold fluid comoving, u = N⁻¹∂_t.
  - ∇_μ(−ρ_L g^{μν}) = −∂^ν ρ_L for any ρ_L(t, r).
  - The vacuum equation ∇_μ T_vac^{μν} = −Q u^ν then gives ∂_r ρ_L = 0 and N = −∂_t ρ_L/Q.
  - The fluid's acceleration is a_r = ∂_r ln N.
  - The r-component of ∇_μ T_c^{μν} = Q u^ν is the Euler equation ∂_r p = −(ρ+p) ∂_r ln N. It has no Q term.
  - With ρ_L = ρ_L(t) and Q = Q(ρ_L, ρ), this gives ∂_r p = (ρ+p)(Q_ρ/Q) ∂_r ρ, i.e. c_s² = (ρ+p)Q_ρ/Q.
  - For Q = ξρ^n ρ_L^m, dsolve gives p = nρ/(1−n) + Cρ^n and c_s² = n(1+w).
  - Reported: the static limit (nothing depends on t) forces Q = 0, which is CFG131's A5. The relation is a ratio, independent of the amplitude ξ.
- **B2 (numerics, my own solver).** Sub-horizon two-fluid growth in N = ln a:
  - δ_c″ + (2 + d ln H/dN) δ_c′ = (3/2) Ω_m(a) δ_m − [c_s² k²/(aH/c)²] δ_c;
  - δ_b″ + (2 + d ln H/dN) δ_b′ = (3/2) Ω_m(a) δ_m;
  - solve_ivp with DOP853, rtol 1e-10 and atol 1e-14.
- **B3 (the bound).** For each k, find the smallest c_s² at which the ratio at z = 0 falls to 0.95:
  - scan upward in 0.1-dex steps from 1e-16 to the first crossing;
  - then run brentq in log c_s²;
  - repeat the same at z = 10.

## Pass lines (canonical footing)

- **H1 [headline, model side].** c_s,max²(k = 30/Mpc, z = 0) is within 10% of 4.6e-12.
- **H2 [headline, target side].** The smallest required dP/dρ over x in [0.1, 30] is within 10% of 2e-8 at 1e9 M☉ and within 10% of 6e-7 at 1e12 M☉.
- **H3 [headline, ordering; MUTATE must change it].** The smallest requirement over the four masses and x in [0.1, 30] exceeds c_s,max²(30), by a factor within 10% of 4.3e3.
- **Exit code.** The main run exits 0 iff H1–H3 and every control pass.
- **Secondary rows.** These use the same 10% line. They are reported and not counted in the exit code.
  - **S1.** c_s,max² at z = 0 for k = 0.5, 2 and 10, against 1.7e-8, 1.0e-9 and 4.2e-11. At z = 10 for k = 0.5 and 30, against 1.5e-7 and 4.3e-11. The ordering at each k.
  - **S2.** The ratio P_req(1e12)/P_req(1e9) at matched ρ_c, over the densities both masses reach in x in [0.1, 30], with P(∞) = 0. Its minimum and maximum are compared with 32 and 272. The same ratio for dP/dρ is reported beside it.

## Controls (a failed control is kept and disclosed)

- **CT1 (the target's own identity).** For all four masses and both footings:
  - C(r) = ρ_c r³ g_tot = a₀M_b/4π to 1e-12 at every grid point;
  - M_c(<r), by quadrature of ρ_c, equals M_b(√(1+x²) − 1) to 1e-8;
  - G(M_b + M_c)/r² equals √(g_N² + g_N a₀) to 1e-8.
- **CT2 (the solver on a closed form).** The singular isothermal sphere, ρ = σ²/(2πGr²) and g = 2σ²/r, with σ = 100 km/s. The solver returns P/ρ = σ² to 1e-8 and dP/dρ = σ² to 1e-5.
- **CT3 (the solver on the target).** The numeric P equals a₀M_b/(8πr²) to 1e-8. The numeric dP/dρ equals the closed form to 1e-5.
- **CM1 (ΛCDM).** With c_s² = 0, δ_m(z = 0) equals the growth integral D(a) = (5Ω_m/2) E(a) ∫₀^a da′/(a′E)³, normalised to δ = a at z = 1000, to 1e-6.
- **CM2 (Jeans, closed form).** Einstein–de Sitter, one fluid, constant c_s².
  - The exact growing mode is δ ∝ a^(−1/4) J_(5/2)(2√(βa)), with β = c_s²k²/(H₀/c)².
  - Sympy checks that it solves the equation.
  - Starting from its own initial data, the solver matches it at a = 1 to 1e-6 for β = 0.2, 1 and 5.
- **CM3 (two fluids, closed form).** Einstein–de Sitter with f_c = 0.265/0.315. To first order, δ_m = a[1 − (2f_c/7)βa]. At β = 1e-4, (1 − ratio)/β equals 2f_c/7 to 1e-3.
- **CM4 (convergence).** c_s,max²(30) moves by < 1e-5 (relative) when rtol goes from 1e-10 to 1e-12.
- **CB1 (derivation).** Every sympy step of B1 returns a zero residual.

## MUTATE

- MUTATE=1 multiplies the pressure term of the growth equation by 1e-5, inside the bound search only. The controls run unmutated.
- The bound it returns then rises by 1e5, above the smallest requirement.
- H1 and H3 must then FAIL, and the run exits 1.
- Outputs are named by mode.

## Reported-only rows (declared now; no pass line; nothing tuned)

- **R-alt.** Every target-side row and the H3 factor, on the alt footing.
- **R-z10.** c_s,max² at all four k at z = 10.
- **R-units.** The bound at k = 30 if k is read in h/Mpc, i.e. physical k = 30h.
- **R-h.** The bound at k = 30 with H₀ = 70 and k in Mpc⁻¹.
- **R-rad.** The bound at k = 30 with radiation (Ω_r h² = 4.18e-5, with Ω_Λ reduced to keep flatness) and the same δ = a start.
- **R-w.** The bound at k = 30 for the full constant-w fluid: w = c_s², the background ρ_c ∝ a^(−3(1+w)), and the (1+w) factors in the perturbation equations.
- **R-req.** The growth ratio at k = 0.5, 2, 10 and 30 with c_s² set to the smallest requirement. This gives the size of the miss in growth terms.
- **R-dens (beyond CFG131).** H2 allows any Q(ρ_L, ρ_c), and that makes c_s² a function of density.
  - I take the most favourable halo-consistent choice: at each density, the smallest dP/dρ that any of the four masses requires there, and zero outside the target's density range.
  - The background passes through the halo densities at some epoch. So I apply c_s²(ρ̄_c(z)) in the growth equation, with ρ̄_c = Ω_c ρ_crit,0 (1+z)³.
  - I report the growth ratio at z = 0 at the four k.
- **R-prof.** The x-profile of the requirement for each mass: largest at x = 0.1, smallest at x = 30.
- **R-sub.** The smallest k/(aH/c) over the integration at k = 0.5. This checks the sub-horizon assumption.

## What I read, and where independence stops

- **Read:**
  - CFG131's FROZEN_QUESTION.md and README.md;
  - closure_map/TEN_DOORS_GATES_2026-09-29.md;
  - CFG44's README.md and the Bcommon.py docstrings. These were extracted with an AST pass that gave the module, function and class docstrings and signatures, and no function bodies.
  - For house style: CFG118_FROZEN_CRITERIA.md, and CFG84's frozen spec and README.
- **Literature** (read through a summarising page fetch; quoted phrases are as returned):
  - Wands, De-Santiago & Wang, *Inhomogeneous vacuum energy*, CQG 29, 145017 (2012), arXiv:1203.6776. I read the abstract and, from the HTML v2 page, eq. (6) Q_ν = −∇_ν V and the sentence at eq. (27): if the energy flow follows the fluid four-velocity, "the vacuum is spatially homogeneous on comoving-orthogonal hypersurfaces". This supports B1's first step only.
  - Salvatelli, Said, Bruni, Melchiorri & Wands, PRL 113, 181301 (2014), arXiv:1406.7297. Abstract only: a late-time vacuum–dark-matter interaction fitted in redshift bins. It is not used in any step.
  - Sandvik, Tegmark, Zaldarriaga & Waga, *The end of unified dark matter?*, PRD 69, 123524 (2004), astro-ph/0212114. Abstract only: a dark fluid with a sound speed gives oscillations or blow-up of the matter power spectrum. This is the physics of the model-side bound. No number from it is used.
- **Not read before my frozen runs:**
  - any CFG131 script (D1–D4, Dcommon.py), .out or .json;
  - CFG43, whose growth conventions CFG131 cites;
  - CFG44's code bodies and outputs.
- **Independence stops at five points:**
  1. **The targets.** CFG131's numbers were read before my code.
  2. **The target.** CFG44's point-mass formulas are shared by both lanes, so a flaw in the target would be common to both.
  3. **The framing.** H1–H4 are CFG131's, and so is the chain: vacuum gradient, lapse, Euler equation, c_s² = (ρ+p)Q_ρ/Q, and a cosmological sound-speed bound that also caps the halo's. I re-derive each step with my own code. I search for no escape outside H1–H4, apart from R-dens.
  4. **The conventions.** The growth set-up is CFG131's frozen one. H₀, k in Mpc⁻¹, no radiation, and Γ = 0 in R2 are my readings of what it does not state.
  5. **The target's c_s².** Reading it as dP/dρ is my choice; the README gives only V_f²/2c².

## Untested

- A nonzero exchange rate Γ together with c_s², i.e. the dilution term and the background shift at once. R-req shows how much a k-independent change of growth would have to supply.
- Q forms beyond the power law, except the one R-dens row.
- Horizon-scale GR terms, neutrinos and baryon–photon coupling. Radiation is tested only in R-rad.
- Nonlinear growth. k = 30/Mpc at z = 0 is nonlinear; the linear ratio is the gate's convention.
- The CMB clause of G2.
- The exponential sphere and other baryon profiles for the required c_s².
- Relativistic corrections, of order V²/c², to the target's hydrostatics.
- CFG131's other rows:
  - G1 on the exponential sphere;
  - D2's background and a₀(z);
  - D3's R1, R3 and R4;
  - D4;
  - the epoch channel.

## Files and exits

- The code goes in campaign_fresh_gravity/CFG156_door8_vacuum_referee/. Nothing is imported from the repository.
- `python3 cfg156_referee.py` writes cfg156_referee.out and cfg156_referee_results.json. `MUTATE=1 python3 cfg156_referee.py` writes the _MUTATE versions.
- The main run must exit 0; the MUTATE run must exit 1. Both print this file's sha256 first.
- Only after both runs: open CFG131's scripts and outputs, compare them, and write README.md.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
