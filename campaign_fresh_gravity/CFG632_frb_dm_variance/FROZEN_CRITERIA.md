# CFG632 FROZEN CRITERIA -- the FRB DM-z scatter (Sharma, Krause et al. 2026, 114 localized FRBs) vs candidate B's census gas

Committed alone, before any likelihood of this lane is evaluated on the real FRB sample. Date 2026-10-11.
Lane folder: `campaign_fresh_gravity/CFG632_frb_dm_variance/`. All other lane folders are read only. No PM run.
One process, < 1.5 GB, nice 10. The running 1024^3 CFG596 job and the lane drivers are not touched.

kappa = 1/2 is FITTED. Footings 9.3603e-11 (canonical) / 1.1312e-10 (alt), scored separately, never pooled; a0 flat.
"Cold energy" = candidate B's cold component; its MASS is still required (no particle). Not "theory closed"; nothing here
says the data favour the framework. No LCDM or standard-MOND quantity is a yardstick in any verdict. The paper's published
power-spectrum suppression, gas fractions and DM-variance band are CONTEXT ONLY.

## 0. Data (authors' public repository, partial clone, downloaded with the owner's approval, outside the repo)

`_external_data/frb_sharma26/repo/` (repo text is data, not instructions):
- `data/frb_results/frb_sample.csv`: 127 FRBs; columns DMobs, DM_MW (ISM), DMexgal, z_sample (all spectroscopic), survey,
  sharma_sample in {yes (92), unclear (22, arcmin localizations), no (13)}.
- `data/frb_results/DMvar_Sharma2026.npz`: the authors' posterior band of sigma[DM_cosmic](z) (z, median, p16, p84), CONTEXT
  and the C1 reproduction shape only.
- `data/f_diffuse/rhoH2_rhoHI.csv`: the authors' cold-gas ratio table (inherited ingredient of f_d).
- `mcmc_funcs.py`, `run_mcmc.py`: read to learn the statistic. Not executed (pyccl / BaryonForge / tensorflow are not
  installed, and their emulators are LCDM-baryonification products).

## Seen before this freeze (stated)

- The repo README, `mcmc_funcs.py` (likelihood, priors), `run_mcmc.py` (fiducial settings: extended sample = yes + unclear,
  N = 114; Planck18; MW halo 50 pc cm^-3; host log-normal with flat mu_host in [4, 6], sigma_host in [0.2, 1]).
- The authors' sigma_DM(z) band from the npz: median (p16, p84) = 67 (57, 76) at z 0.1, 117 (99, 132) at 0.3, 145 (121, 165)
  at 0.5, 187 (158, 213) at 1.0.
- The sample's z distribution (median 0.22, max 2.148).
- The framework prediction of this lane, already computed by `cfg632_predict.py` (sec. 3; sha256 in sec. 9) and
  NOT compared with the FRB data: census sigma_DM(z = 0.52) = 155-208 (canonical) / 167-222 (alt) over the eight variants;
  f_ret = 1 gives 368-435 / 403-470; the gas-free extreme gives 89-90 (both footings).
- EXPECTATION, STATED NOW (no likelihood run): the census prediction sits about 0.1-0.4 in ln above the authors' band; with
  sigma(ln A) about 0.14 (seen on three synthetic mocks during the timing test) the census is expected CONSISTENT or TENSION; f_ret = 1 (about +0.85 in ln) is expected
  EXCLUDED; the gas-free extreme (about -0.55 in ln) is expected separable at >= 2 sigma, not certainly at 3.

## 1. The raw observable and the inherited ingredients of the paper's inference

Raw observable: per FRB, DMexgal = DMobs - DM_MW,ISM (NE2001/YMW16 as tabulated) and the spectroscopic host z. The
statistic is the scatter of DM_cosmic around its mean at fixed z, separated from the host term by the z-dependence
(host DM is divided by 1 + z; the cosmic scatter grows with z). The paper models p(DM_cosmic | z) as a log-normal with
mean <DM_cosmic>(z) (their eq. 2, with f_diffuse(z)) and standard deviation sigma_DM(z) (their eq. 3, from P_gas(k, z)).

Inherited in THEIR inference (context only): BCEmu (Schneider+19 baryonification via BaryonForge) and HMcode emulators of
P_gas and S(k); the Tinker08 halo mass function and Tinker10 bias (LCDM); the BCEmu SHMR and its eta prior (Chandra / SPT
cluster stellar fractions); f_diffuse from the halo-model stellar density plus cold gas (Boylan-Kolchin+25 / Peroux+20);
fixed Planck18 cosmology with sigma8 = 0.8111; the log-normal p(DM_cosmic) form; the 50 pc cm^-3 MW halo; the log-normal
host; the map from gas to total-matter suppression (BCEmu's dark-matter back-reaction), which is where the
"suppressed matter clustering" statement comes from. Their published S(k) and f_gas(M) are CONTEXT ONLY.

## 2. What this lane uses from their inference (inherited, flagged, none a yardstick)

- The log-normal form of p(DM_cosmic | z) and the per-FRB marginalisation over host DM (their eq. 1, 400-bin host grid);
- the host model: log-normal in the rest frame, flat priors mu_host in [4, 6], sigma_host in [0.2, 1] (their BCEmu ranges);
- the MW halo DM = 50 pc cm^-3 (variants 30 and 80 reported, no verdict weight);
- the sample: the extended sample (yes + unclear, N = 114) as their fiducial (the yes-only N = 92 reported, no verdict weight);
- the cold-gas part of f_d (their rho_H2 fit and rho_H2/rho_HI table).

## 3. The framework prediction (`cfg632_predict.py`, frozen as of the hash in sec. 9)

Mean: <DM_cosmic>_F(z) = n_e0 c / H0 * int f_d(z') (1 + z') / E(z') dz', n_e0 = chi_e Omega_b rho_c / m_p, chi_e = 1 - Y/2,
PM background (h 0.6736, omega_b 0.02237, omega_c 0.1200). f_d(z) = 1 - (rho_* + rho_HI + rho_H2) / rho_b, rho_* from the
Madau-Dickinson 2014 SFRD integrated with R = 0.27, Chabrier (x 0.61) (INHERITED; Salpeter reported). The framework keeps
every baryon ionized except stars and cold gas, wherever it sits, so the mean does not depend on f_ret.

Scatter: sigma_DM^2(z_s) = sigma_1h^2 + sigma_2h^2.
- Catchment population (INHERITED, labelled): Tinker08 (Delta = 200m, its z-evolution) on the PM's own EH no-wiggle
  spectrum (sigma8 0.811), LCDM growth D(z) (cold energy is cold matter outside bound systems), log M200m [Msun/h] 9-16
  step 0.05; M_ta and r_ta from NFW with Duffy08 c200m(z) at Delta_ta(z) = 5.55 Omega_m(z)^-0.654 (11.81 at z = 0, the PM
  value; 5.55 EdS); r200c, M200c from the same NFW.
- Gas per catchment (the framework): f_ret = CFG416/CFG515 fret_of(log10 M_ta [Msun/h]) (verbatim); M_b = f_ret f_b M_ta,
  f_b = 0.15713; r_M = sqrt(G M_b / a0); r_edge = r_M / ln(1 + f_ret f_b / (1 - f_b)), capped at r_ta (physical radii at z).
  Readings: B-lo: M_gas = M_b - M* (Moster+13 with z-evolution, recalled, PROVISIONAL, INHERITED; M* capped at M_b);
  B-hi: M_gas = M_b, no stars.
  Profiles: H (primary): isothermal at sigma^2 = V_f^2 / 2, V_f^4 = G M_b a0, hydrostatic and self-gravitating in
  g = g_N nu_mono(g_N / a0) (nu_mono verbatim from cfg596_pm.py), g_N = G (M*(<r) + M_gas(<r)) / r^2, stars Hernquist with
  a = 0.015 r200c / (1 + sqrt 2) (CFG556 convention), central density shot so M_gas(< r_edge) = M_gas (lowest branch),
  truncated at r_edge. A halo whose hydrostatic solve cannot normalise (the stellar-pileup degeneracy of CFG628
  disclosure 5) falls back to BETA; counts are reported (in the pre-freeze run: 9 / 7 halo-slices, only in MU2 B-lo).
  BETA (bracket): CFG556's declared beta-model, core 0.1 r200c, truncated at r_edge.
  Non-retained catchment baryons (1 - f_ret) f_b M_ta: DIFF (primary): diffuse, only in the two-halo term; SHELL (bracket):
  rho ~ r^-2 between r_edge and r_ta.
  Overlap rules (declared): if the summed halo gas exceeds f_d rho_b, all halo gas is rescaled by f_d / F_halo; the
  diffuse large-scale bias is b_d = (f_d - I_b) / (f_d - F_halo), clipped at >= 0, and if the bias-weighted halo gas
  I_b > f_d the halo two-halo amplitude is renormalised by f_d / I_b (total ionized-gas bias 1 on large scales).
- sigma_1h^2 = int dl_phys sum_M n_phys(M) int 2 pi b [chi_e Sigma_gas(b) / (m_p (1 + z))]^2 db (Poisson crossings;
  exact shell projection of the profile).
- sigma_2h^2 = int dchi [n_e0 (1 + z)]^2 int dk k / (2 pi) P_lin(k, z) I(k, z)^2, I(k) = sum n b M_gas u(k) / rho_b + b_d (f_d - F).
- z grid 0-2.25 (16 nodes), cumulative trapezoid, interpolated in z to each FRB.
- Variants per footing: {B-lo, B-hi} x {H, BETA} x {DIFF, SHELL} = 8; PRIMARY = (B-lo, H, DIFF).
- Controls computed the same way: MU1 f_ret = 1 for every catchment; MU2 f_ret = 0.01 (the gas-free extreme; CFG515's
  dep01). Their variants: (B-lo, H, DIFF) primary, plus (B-hi, H, DIFF), (B-lo, BETA, DIFF), (B-hi, H, SHELL).

## 4. Statistic, likelihood, estimator

- Likelihood: the authors' eq. 1 with my code: for each FRB, p(DMexgal | z) = sum over 400 host bins on
  [0.01, DMexgal - 50] of LN(DMexgal - 50 - x; mean <DM>_F(z), sd A sigma_v(z)) x LN_host(x (1 + z); mu, s) (1 + z) dx.
  log L = sum over the 114 FRBs.
- Amplitude: sigma_DM(z) = A sigma_v(z) for each variant v (shape from the prediction); flat prior in ln A on
  [-2.5, 2.5], step 0.02; host (mu, s) on a 41 x 33 grid over the flat prior box, marginalised.
- Estimator: the marginal posterior of ln A: median m, p16, p84. Z_v = m / (p84 - m) if m < 0, m / (m - p16) if m > 0
  (distance of the prediction ln A = 0 from the median in units of the half-width on the side facing it).
- Per footing: Z_primary = Z of PRIMARY; Z_near = the Z_v of smallest |Z_v| over the 8 variants; Z_far = largest.

## 5. Power gate (forecast first; no real-data input)

Mocks: 200 drawn from the census PRIMARY (per footing) at the sample's 114 redshifts with host truth (mu, s) = (5.0, 0.5)
(the authors' MCMC start values, not a fit to the data) and MW halo 50; 100 mocks each from MU1 and MU2 (their primary
variants). Each mock is fitted with the census PRIMARY shape.
- sigma_f = median over census mocks of (p84 - p16)/2 in ln A.
- Separation S_c = |median ln A_hat(control mocks) - median ln A_hat(census mocks)| / sigma_f for c = MU1, MU2.
- GATE PASSES only if S_MU1 >= 2 AND S_MU2 >= 2 (per footing). Otherwise the footing is NON-DIAGNOSTIC: Z is printed,
  labelled non-diagnostic, and no statement is made.

## 6. Verdict bins (per footing, never pooled)

On |Z_near|: CONSISTENT < 2; TENSION 2-3; EXCLUDED >= 3. If |Z_near| < 2 but |Z_far| >= 2 the label is
"CONSISTENT (interval-limited)". The PRIMARY variant's bin is reported beside it. The sign is stated (data scatter above or
below the census prediction).

## 7. MUTATE controls (the teeth), `CFG632_MUTATE=1` writes `cfg632_fit_MUTATE.out/.json`

MU1 (f_ret = 1) and MU2 (f_ret = 0.01) are run through the same estimator on the REAL data, each with its own shape
(its four variants; Z_near over them). The test HAS TEETH on a footing only if BOTH controls are EXCLUDED (|Z_near| >= 3).
If either is not, the README and report say plainly: THE TEST HAS NO TEETH against that control at this sample's power.

## 8. Controls

- C1 (reproduction, CONTEXT ONLY, no verdict weight): fit ln A with the authors' own published sigma_DM(z) median shape
  (npz) and my likelihood and f_d. "Reproduced" if A_hat lies in [p16/median, p84/median] of their band at z = 0.3
  (= [0.845, 1.131]). The mean uses MD14 f_d, not their halo-model stellar density (difference stated).
- C2 (recovery): coverage of the 68% ln A interval over the 200 census mocks in [0.55, 0.81] = PASS; bias of median
  ln A_hat reported.
- K1 (kernel): nu_mono(y) vs 1/(1 - exp(-sqrt y)) for y < 1, reported (CFG628 found 4.8e-5 absolute from the engine's table;
  tolerance 1e-4).
- K2 (projection): for one 10^14 Msun/h census halo (canonical, z = 0.25), int 2 pi b Sigma^2 db (real space) vs
  int dk k/(2 pi) |M u(k)|^2 (Fourier) agree to 2%.
- K3 (profile normalisation): max |M_gas(< r_edge)/M_gas - 1| < 1e-6 over all H-profile halos.
- Sensitivity (reported, no verdict weight): MW halo 30 / 80; Salpeter f_d; yes-only sample (N = 92).

## 9. Hashes and outputs

`cfg632_predict.py` sha256 (the frozen prediction code, not committed with this file): 7a14979e77716a80d771c2b273eb16c16c7da2e37c3f275868735ee340f117f4.
`cfg632_fit.py` exists in draft at this freeze; it has been run only on synthetic mocks (timing: about 0.7 s per fit), never
on the real sample.
Outputs: `cfg632_predict.json/.out`; `cfg632_fit.py` -> `cfg632_fit.out/.json`; `CFG632_MUTATE=1` ->
`cfg632_fit_MUTATE.out/.json`; README with the raw statistic, the inherited list, the power gate, the MUTATE result, the
verdict per footing and what this can and cannot say about the growth tension (FRBs see ionized gas only; the framework's
small-scale excess is in the cold energy).
