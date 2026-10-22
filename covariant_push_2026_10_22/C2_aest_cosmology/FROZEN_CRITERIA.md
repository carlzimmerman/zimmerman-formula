# C2_aest_cosmology: FROZEN CRITERIA (written before any script or number)

Lane of the covariant push (`covariant_push_2026_10_22/BRIEF.md`); `doors_push_2026_10_22/BRIEF.md` and
`BRIEF_E_AUDIT.md` apply. kappa = 1/2 is FITTED. Footings never pooled. No "theory closed". Nothing here
can say the data favour the framework over LCDM.

## Question

What does an AeST-type covariant completion of the screened theory predict for the cosmological
background and linear growth; what sets its dust abundance; does it change the native-H0 tension; and what
tooling and raw data on disk would a native CMB / P(k) confrontation need?

## External inputs (flagged; not re-derivable here)

- E-AeST: the AeST action and background relations of Skordis & Zlosnik, arXiv:2007.00082 (PRL 127, 161302),
  as transcribed in the record `real_research/bridge1_aest_equations.md` (stated there to be verbatim from the
  arXiv LaTeX source, 2026-08-14). The paper itself is NOT on disk (checked `_external_data/arxiv_src`,
  `arxiv_pdf`); re-verification needs the owner's OK to fetch it. Used: Y = q^{mu nu} d_mu phi d_nu phi with
  q = g + A A; Q = A^mu d_mu phi; the a0 term sits in the Y-dependence of F; the background relations
  dK/dQ = I_0/a^3, 8 pi G~ rho = Q dK/dQ - K, 8 pi G~ P = K; and G~ = (1 - K_B/2) G^_qs.
- E-A78: the record's BBN bound on the screened theory's clock coupling, beta < 0.0280, i.e.
  G_cosmo/G_N > 0.9611 (`deepseek_push/DS_FINAL_2026_10_21/A78_beta_closure/`), and G_cosmo/G_N = 2/(2+3 beta).
- E-886: CFG886 primary (DESI DR2 BAO + BBN, GR, no CMB): h = 0.6856 +- 0.0052, Omega_m = 0.2976
  (`campaign_fresh_gravity/CFG886_ratio_fret_without_planck/cfg886_results.json`).
- E-ladder: 73.0 +- 1.0 km/s/Mpc, the value E1 used (A51 on disk). Reported with the same convention as E1
  (ladder sigma only) and also with the native error added in quadrature.

## Checks (script `c2_aest_cosmology.py`, one line each, exit 0 iff all pass)

- K1 (DERIVED, sympy). On FRW with A^mu the unit normal and phi = phi(t) + eps*dphi(t,x): Y vanishes at
  order eps^0 and eps^1 exactly. PASS iff both residuals are identically 0. Meaning: the a0-carrying Y-sector
  is absent from the background and from linear perturbations of an AeST-type action.
- K2 (DERIVED, sympy). Minisuperspace L = a^3 N K(Q), Q = phidot/N: the phi-equation is d/dt(a^3 K'(Q)) = 0,
  so a^3 K'(Q) = I_0 is a free integration constant; the dust density at a = 1 is Q_0 I_0 / (8 pi G~)
  (late-time limit) and has zero derivative with respect to a0 and to Lambda. PASS iff the EOM residual is 0,
  d rho_dust/d I_0 != 0, and d rho_dust/d a0 = d rho_dust/d Lambda = 0. Meaning: Omega_c is set by an
  initial datum (FITTED), so Omega_c/Omega_b = 5.36 stays an import unless a premise not in the action ties I_0.
- K3 (COMPUTED). Cosh-K background (record's L137 form) solved numerically: the dust share drifts between
  z = 1090 and z = 0 by a fraction D(Z_0/Q_0). PASS iff the numerical drift matches the analytic estimate
  (Z_0/Q_0) * ln(n_1090/n_0) to within 10 % at Z_0/Q_0 = 1e-3. Reported, not scored: E(z) deviation from the
  dust limit.
- K4 (DERIVED + COMPUTED). Any background equal to GR with G_cosmo = g G_N for every species maps onto the
  GR fit with H0 = sqrt(g) H0_GR at fixed physical densities: D_M/r_d and D_H/r_d agree to < 1e-6 at
  g = 0.9611 and at g = 0.6845. PASS iff both residuals < 1e-6.
- K5 (COMPUTED). Native H0 band under A78 (g in (0.9611, 1]) with E-886: H0 in [sqrt(0.9611) h_GR, h_GR]*100.
  Tension with E-ladder reported. PASS iff the band's upper end is above 60 km/s/Mpc (i.e. the 55-57.5 band of
  E1 is not the BBN-allowed native background). FAIL means E1's band stands.
  Outcome lines: if PASS, E1's "15.5-18 sigma" flag is reported as resting on the beta = 0.21 background that
  A78 excludes (a record error, reported, not edited).
- K6 (COMPUTED). AeST map: if G_N = G^_qs, g_AeST = 1 - K_B/2, and the A78 BBN line gives K_B < 2(1 - 0.9611).
  PASS iff the computed bound equals 0.0778 +- 0.001. The G_N vs G^_qs relation is OPEN (not on disk).
- K7 (COMPUTED). Linear growth on the dust-limit background (GR growth, G_eff = G_cosmo): growth index gamma
  from f(z=0) = Omega_m^gamma at E-886. Cross-check: on A46's beta = 0.21 background the same solver gives
  f(0) within 0.005 of A45's 0.452. PASS iff the cross-check holds.
- K8 (COMPUTED). CLASS (classy) cross-check of r_d at E-886 physical densities against this script's
  quadrature: PASS iff |diff| < 1.5 %. (Proves the tool runs; the dust limit of AeST is vanilla LCDM in CLASS.)
- K9 (INVENTORY). Tools and data on disk listed with presence flags and sha256 prefixes; PASS iff each listed
  "present" item exists and each listed "absent" item (hi_class, AeST-CLASS, clik/plik, cobaya, Planck
  TT/TE/EE spectra or likelihood files, the AeST paper source) is absent.

## Verdict lines

- COMPUTED if K1-K9 pass and the background, abundance and H0 questions are answered with numbers.
- DATA-GATED (exact list) for the native CMB / P(k) confrontation if K9 shows the gap; the list names
  packages and data products for the owner's approval; nothing is fetched.
- NO-GO only if K1 or K2 fails (the AeST sector would then not be a dust + Lambda background).

## Mutation

`C2_MUTATE=1` replaces the spatial projector q by the full metric g in K1 (Y no longer vanishes on FRW) and
drops the sqrt in K4's H0 map. K1 and K4 must fail; outputs go to `*_MUTATE.out`, `*_results_MUTATE.json`.

## Budget

`OMP_NUM_THREADS=1 nice -n 10`, < 1 GB RSS, minutes. No downloads, no installs.

## AMENDMENT A1 (POST-RESULT, 2026-10-22; written after the first scored run, which gave 7/9)

The first run failed two frozen lines. Both failures stand in the record and are printed by the script as
`K8-orig` and `K9-orig`. Two replacement checks drive the exit code from now on:

- **K8 FAILED (+2.50 %).** The script's quadrature used the uncalibrated Eisenstein–Hu z_d = 1020. CLASS
  gives 1059. The failure is in the cross-check tool, not in K4/K5: z_d cancels in the K4 ratios, and K5
  uses CFG886's fitted h. **K8b** reruns the same quadrature with CLASS's z_d and keeps the same 1.5 % line.
- **K9 FAILED, and the inventory claim was wrong.** A Planck PR3 TT unbinned spectrum *is* on disk:
  `_external_data/cmb_lensing_raw/planck_PR4_lensing/planckpr4lensing/data_pr4/iswliks/COM_PowerSpect_CMB-TT-full_R3.01.txt`.
  It has ℓ = 2–2508 and diagonal errors only. There is no covariance and no TE/EE.
  The pattern `*clik*` also matched unrelated names (`rclike`, `multiplikat…`).
  **K9b** fixes the pattern. It counts the TT file as present and requires that hi_class/AeST-CLASS, clik and cobaya are absent and that no other hit remains.
- Not a check change: the reported (unscored) β-branch line in K5 used A42's β = 0.2109 (Ω_m = 0.316). The
  record's native branch is A46's β = (2/3)·0.461 = 0.307, g = 0.6845, H₀ = 56.7. The line now reports that,
  with A42's value alongside. K5's pass line does not change.
- A1 detail (same day, before any further scored use): the first K9b run also matched `*plik*` inside
  `grouplike`/`multiplikation` (147 Lean/mathlib and citation files). K9b's patterns are `plik_*` and `*.clik`
  (Planck's own file names), plus the other names listed in the frozen K9 line.

## AMENDMENT A2 (PRE-RESULT, 2026-10-22; written before any new number, after the owner-approved fetches)

The owner approved, via the coordinator, the fetch of four items: the two AeST papers, the Planck 2018 TE/EE spectra,
and cobaya with plik-lite. Provenance is in `PROVENANCE.md`. A new script, `c2b_native_cmb.py`, adds the checks below.
K1–K9 are unchanged.

**The papers replace E-AeST.** They are now on disk:
- arXiv:2007.00082 (`newRMONDLett.tex`);
- arXiv:2304.05134 (`main.tex`, VSZ 2023).

**How the likelihoods are evaluated.** A classifier denied importing the downloaded cobaya code into the analysis
Python, so cobaya's code is not executed for any number here. The three likelihoods are reimplemented with numpy
from the installed data files (read with `python3 -I`) and from cobaya's source, which was read as text:
- plik-lite TTTEEE native;
- low-ℓ TT (Gaussianised splines);
- low-ℓ EE (probability table).
The reimplementation is not validated against cobaya's own output. That is a stated limit.

- **P1 VERIFY.** These snippets must be present in the paper sources:
  - the action (Eq. 5) with its terms;
  - J_μ = A^α∇_αA_μ;
  - Q and Y;
  - K(Q̄) = −½F(0, Q̄);
  - the λ_s coefficient 2λ_s/(3(1+λ_s)a₀);
  - G̃ = (1 − K_B/2)Ĝ;
  - G_N = (1 + 1/λ_s)Ĝ (PRL);
  - Ĝ = G_N/(1+β₀), with λ_s = 1/β₀ (VSZ);
  - μ = √(2K₂/(2−K_B))·Q₀;
  - the stability conditions 0 < K_B < 2, λ_s > −1, K₂ > 0, λ_s > 0.
  PASS iff all are found. Discrepancies against the record and against C1 are listed and do not affect the pass.
- **P2 DERIVED.** g ≡ G̃/G_N = (1 − K_B/2)·λ_s/(1+λ_s), from the two relations (sympy residual 0). The A78 line
  g > 0.9611 then gives K_B < 0.0778 (at λ_s → ∞) and λ_s > 24.71 (at K_B → 0). PASS iff the residual is 0 and both bounds match to 1e-3.
- **P3 SOURCE.** PASS iff the paper's linear δ is normalised with G̃ and its Einstein equations are stated in GR form.
  Meaning: linear growth feels G_cosmo = G̃, not G_N. K7's "G_N variant" (+16 % σ₈) is then withdrawn as not AeST's linear behaviour.
- **P4 COMPUTED (emulation; NOT the AeST prediction).** Vanilla CLASS emulation of G_cosmo = g·G_N at fixed physical densities:
  - CLASS omega_b = ω_b, so baryon microphysics stays physical;
  - omega_cdm = g·ω_c − (1−g)·ω_b;
  - N_ur = g·(N_γ + 3.044) − N_γ, with N_γ = 1/0.22711;
  - h = √g·h₁.
  The background is exact. The perturbation sourcing of photons, baryons and neutrinos is approximate, O(1−g).
  PASS iff |Δθ_s/θ_s| < 1e-3 at g = 0.9611 versus g = 1 (the acoustic scale is blind to g).
- **P5 COMPUTED (emulation).** Likelihood setup:
  - plik-lite TTTEEE plus low-ℓ TT and EE;
  - A_planck with a prior of 1 ± 0.0025;
  - the low-ℓ part enters the Gauss–Newton refit as a τ prior measured natively from a τ scan at fixed A_s e^{−2τ}.
  Steps:
  - refit ΛCDM (g = 1) by Gauss–Newton in 6 parameters plus A_planck;
  - form the Fisher σ(g), marginalised;
  - compute the profile Δχ² (refit, exact evaluation of all three likelihoods) at g = 0.9611 and g = 0.6845.
  PASS iff the refit's plik-lite χ² lies in [500, 750] for 613 bins (sanity).
  Outcome lines:
  - g = 0.6845 is "disfavoured by plik-lite + low-ℓ in this emulation" if Δχ² > 25;
  - the BBN band is "not distinguishable" if Δχ²(0.9611) < 4.
  Neither is an AeST verdict.
- **Mutation `C2B_MUTATE=1`.** It drops the λ_s factor in P2 and leaves N_ur unscaled in the emulation. P2 must fail.
- **Budget.** About 60 CLASS runs at about 2 s each, single thread, < 1 GB.
