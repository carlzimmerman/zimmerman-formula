# CFG360 FROZEN CRITERIA: is the cold fluid a byproduct of dark energy? (fresh lane)

Committed alone, before any script or machine-computed number. Owner decision (2026-10-06): reopen the question as a FRESH lane.
kappa = 1/2 FITTED and fixed. No dark-matter particle species: the cold MASS is still required and is kept. "Cold fluid" = B's cold
component. No knob scans; no new fitted constant may be tuned to pass G-AMOUNT. Never "theory closed". A FAIL is a valid outcome.

ID note: the directory `campaign_fresh_gravity/CFG360_baryon_tie/` (commit 581291e38, a parallel session) also uses the CFG360 number.
This lane is `CFG360_cold_fluid_from_dark_energy`; the orchestrator owns any renumbering. Neither lane edits the other.

## 0. Read before freezing (not blind), cited only to avoid repeating known failures
- The Lambda-triggered carrier chain (`real_research/dark_sector_2026/L319_*`, L320) was STOPPED by the owner (Sept 2026). Its
  constructions are not continued; L368 is not cited. L319 header read only: a decay switched on by Omega_Lambda(a).
- CFG288 (`campaign_fresh_gravity/CFG288_one_field_dark_sector/README.md`): V = rho_Lambda + m^2|Phi|^2 passes behaviour gates, but
  the AMOUNT is free (theorem A1: dust present before z_eq needs a potential height >= ~1.5e10 rho_Lambda, a second scale; rho_Lambda
  never enters the dust dynamics); seeding at z <= 1e4 excluded, z >~ 1e5 required.
- PAPER42 abstract (`qwen_claude_field_theory/papers_2026/PAPER42_mond_vacuum_dark_energy_2026.tex`): dark energy = zero-field
  energy of the MOND field; predicts w = -1 with time-constant a0, or a0 proportional to sqrt(rho_DE) if dark energy evolves.
- `sonnet55_push/cold_mass/README.md`: cm01 (retention cannot be a function of local MOND activity y); cm02 (C003 escape-speed
  kick consistent, non-diagnostic).
- p60 (`sonnet55_push/puzzle_32pi/README.md` sec. 69): a grammar of standard balances hits simple targets at a base rate.
- DESI DR2 chains on disk (`../_external_data/desi_dr2_chains/{cmb,pantheonplus,union3,desy5}`, w0waCDM, columns w, wa).

## 1. Gates (frozen)
- **G-AMOUNT.** Omega_c/Omega_b = 5.36 +- 0.07 (Planck 2018; omega_c = 0.120, omega_b = 0.02237) from {a0 = kappa c sqrt(G rho_Lambda),
  kappa = 1/2, Lambda, baryon content, c, G, hbar} with ZERO new fitted constants AND a stated mechanism. A number without a mechanism
  does not count. If the amount is set by any undetermined quantity (amplitude, rate, efficiency, transition scale), the verdict for
  that class is "amount FREE".
- **G-TIMING.** The cold fluid is pressureless adiabatic dust before z = 3000: (i) |w| <= 1e-2 and its Jeans wavenumber at z = 3000
  k_J >= 1 Mpc^-1 (well beyond the third acoustic peak, k ~ 0.2 Mpc^-1); (ii) >= 99% of omega_c (0.120 +- 0.0012, the Planck 1% level)
  already in place by z = 3000 (CMB fixes omega_c at recombination); (iii) produced before z = 1e5 or from an adiabatic source
  (CFG288's seeding rule), else isocurvature is flagged.
- **G-EXPANSION.** Any vacuum -> cold transfer Q = Gamma rho_Lambda (Gamma >= 0 const, units H0) keeps the background within DESI DR2 +
  SN. Method (declared, PROVISIONAL): integrate rho_Lambda, rho_c with omega_c fixed at early times (CMB), H0 = 67.4; build the
  effective dark-energy density an observer infers when extrapolating today's dust as a^-3, project onto CPL (w0, wa) by least
  squares over 0 <= z <= 2.5 in w_eff(a); compare to each chain's (w, wa) mean + covariance (Gaussian). Allowed: the model lies inside
  the 2D 95% contour (chi^2 <= 6.18) of ALL FOUR chain combinations; the bound Gamma_max is the largest such Gamma. A second,
  framework-internal bound is also reported: the framework's own FLAT a0(z) law (a0 proportional to sqrt(rho_Lambda), flat < 1% for
  z <= 5) requires |Delta rho_Lambda / rho_Lambda| <= 2% over z <= 5.
- **G-SORTING (reported, not required).** Does the mechanism explain spirals <= ~10% vs clusters ~58% retained (cm01/C003)?

## 2. Classes (at most 5, frozen before computing)
1. C1 Interacting vacuum Q = Gamma rho_Lambda (Gamma free, constrained only by G-EXPANSION).
2. C2 A field whose potential minimum shifts with the khronon clock (V(phi - v(tau))).
3. C3 A condensate fraction of the vacuum sector (FL1 order parameter: dust density = fraction f of rho_Lambda).
4. C4 Horizon / thermodynamic production tied to a0: zero-parameter rate Gamma = a0/c (premise-A-like) acting on rho_Lambda, and the
   horizon (Gibbons-Hawking) energy density hbar H^4/c^3 as a reservoir.
5. C5 Early production at a phase transition of the vacuum sector; the transition scale tied to rho_Lambda^(1/4) (zero-parameter) or free.

## 3. Base-rate null (any closed form for 5.36)
Grammar: products c * x1^p1 * x2^p2 with x in {pi, 2, 3, e, kappa=1/2, Omega_Lambda=0.6847, Omega_b=0.0493, Omega_m=0.3153, sqrt2,
sqrt3}, exponents p in {-2,-1,-1/2,1/2,1,2}, prefactor c in {1, 2, 3, 4, 1/2, 1/3, 1/4, 2/3, 3/2, 3/4, 4/3}, plus single-symbol
forms; the definitional identity Omega_m/Omega_b - 1 is excluded as circular. Window: |X/5.36 - 1| <= 1.3%. p = hits / (distinct forms).
A closed form survives only if p < 0.01. MUTATE-null: planted target 3.00 must give a comparable rate.

## 4. Decision (frozen)
- MECHANISM FOUND: a class passes G-AMOUNT, G-TIMING, G-EXPANSION with 0 new constants and its amount survives the null at p < 0.01.
- PARTIAL: passes timing and expansion with the amount free, or the amount fits but fails the null.
- NO-GO: obstruction stated per class; certified in Lean where it is a theorem.

## 5. Controls
- K1 plain LambdaCDM (Gamma = 0) returns omega_c as input exactly and (w0, wa) = (-1, 0) from the projection.
- K2 a transfer violating the DESI bound (Gamma = 1 H0) must be flagged by G-EXPANSION.
- MUTATE (CFG360_MUTATE=1, separate outputs `*_MUTATE*`): the cold fluid gets c_s^2 = w = 1/3. G-TIMING must FAIL (exit 1).

## 6. Lean (Lean 4 + Mathlib, no sorry)
Certify: constant rho_Lambda => Q = 0 (Bianchi); the flat-a0 transfer bound arithmetic; the zero-parameter C4/C5 obstructions
(Gamma = a0/c vs the bound; T* = rho_Lambda^(1/4) gives z_* < 3000); the base-rate count arithmetic (hits/N vs 0.01).

## 7. Expectations (hand, before machines; the scripts decide)
All five classes NO-GO or amount-FREE; C1 Gamma bound O(0.01-0.1) H0; C4 Gamma = a0/c ~ 0.14 H0 fails the flat-a0 bound; C5 z_* ~ 10.
