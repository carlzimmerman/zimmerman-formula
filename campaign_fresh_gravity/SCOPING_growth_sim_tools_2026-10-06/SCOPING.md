# SCOPING: simulation tools for a nonlinear structure-growth test of candidate B (2026-10-06)

Scoping only. Nothing downloaded, installed, run or committed. Web summaries (arXiv abstracts, READMEs, search
snippets) are PROVISIONAL: a summariser is not the source. Repo sizes are GitHub-API `size` values (git history
included, so an upper bound on a shallow clone or tarball). Every download listed in section 5 needs the owner's
explicit yes in chat.

## 1. What has to be simulated

- Candidate B: GR + khronon chassis + nu_mono kernel, a0 = kappa c sqrt(G rho_Lambda) with kappa = 1/2 FITTED
  (both footings: 9.36e-11 / 1.13e-10) + a cold component (Omega_c h^2 ~ 0.12; the MASS is required, no DM
  particle) + the bound-only switch, now CFG354 T1: f = H_eps(l_2 - tau_ta), l_2 = middle eigenvalue of
  t_ij = D_i D_j psi, psi = Phi_d/(4 pi G rho_bar) (MASTER_LAGRANGIAN_2026-10-05).
- Known: bare chassis ~7x too fast (L341, AUDIT_SIGMA8). With T1 OFF on linear modes, B = LCDM growth (CFG324;
  T1 ON in 0 of 4e6 linear samples). Open: the NONLINEAR regime, where T1 fires in hosts AND in dense filament
  cores (delta_f >= 2 tau_ta; Lean theorem for eigenvalue-only readers).
- So the needed code must: (i) evolve cold + baryon particles in an expanding box; (ii) compute the tidal tensor of
  the Newtonian potential on the mesh each step; (iii) apply a per-cell gate f; (iv) solve a QUMOND-type second
  Poisson equation with nu_mono where f = 1. Items (ii)-(iv) are a few FFTs per step in a particle-mesh (PM) code.

## 2. Tool table

Legend: (b) built-in LCDM assumptions; (c) can it host nu_mono / EFE / T1 switch / khronon; (e) feasibility on an
M4 Max, 64 GB, 64-128 Mpc/h, 128^3-256^3.

| tool | (a) solves | (b) built-in LCDM | (c) hosts B's pieces? | (d) licence, lang | (e) M4 feasibility | (f) size |
|---|---|---|---|---|---|---|
| **PySCo** (Breton 2025, arXiv 2410.20501; github mianbreton/pysco) | Cosmological PM N-body: Newton, f(R), QUMOND (∇²φ_N = 4πGρ; ∇²φ = ∇·[ν ∇φ_N]), multigrid or FFT; 1-3LPT ICs | LCDM(+w0wa) Friedmann background computed internally; ICs from a user P(k) file (paper used CAMB LCDM); a0 constant physical (optional a^N scaling); peculiar-field convention for the MOND source NOT verified | nu: 5 families (simple, n, beta, gamma, delta); nu_mono NOT included but is a numba function to add. EFE: inside the box, automatically (QUMOND on the full periodic field); super-box modes absent. T1: not present; tidal tensor = k_i k_j/k² on the existing FFT grid, ~50 lines. Khronon: no (frame = box frame, quasi-static) | MIT, Python + numba | Yes. Paper: ~1 CPU-hour for a Newtonian 512³ run on a laptop. 256³ is minutes-hours | repo 6.4 MB; pip `pysco-nbody` pulls numba+llvmlite (~40-50 MB), pandas, rich; pyfftw optional |
| **MONDPMesh** (Visser, Eijt, de Nijs, arXiv 2312.02968; github Joost987/MONDPMesh) | AQUAL PM via two linear FFT steps, with EFE | Not cosmological (no expansion) | AQUAL, EFE yes; no cosmology, no switch | MIT, Python; FFT on CuPy (CUDA: no Mac GPU path) | Would need a NumPy port; useful only as an AQUAL cross-check | repo 0.3 MB |
| **Phantom of RAMSES (PoR)** (Lüghausen, Famaey, Kroupa 2015, arXiv 1405.5963; bitbucket SrikanthTN/bonnPoR) | QUMOND AMR N-body + hydro in RAMSES (2015 version) | Cosmological mode used for nu-HDM (Wittenburg+23, arXiv 2305.05696: z_i = 199, ICs from CAMB + MUSIC, up to 600 Mpc boxes); RAMSES integrates a Friedmann background from its own Omega params | nu: fixed in Fortran (editable); EFE yes; switch would be a Fortran edit in the phantom-density step; khronon no | GPL (RAMSES CeCILL/GPL-type; PoR licence not read: bitbucket page did not render), Fortran 90 + MPI | Builds with gfortran (present) + open-mpi; 128³ cosmological run is hours on 14 cores | RAMSES repo ~100 MB; PoR size unknown |
| **RAyMOND** (Candlish+15, arXiv 1410.3844; ifa.uv.cl/sites/graeme/codes.html) | RAMSES patch: AQUAL (FAS multigrid) and QUMOND | QUMOND patch supports cosmological runs (RAMSES Friedmann background, CDM-style ICs); AQUAL patch not cosmological; "beta, not tested with current RAMSES" | as PoR; also used for MOND velocity fields (Candlish 2016, arXiv 1605.03192) | licence not stated; Fortran | as PoR; risk of RAMSES-version incompatibility | tarball `raymond_patches.tgz`, size not shown (patch, likely < 1 MB) + RAMSES |
| **N-MODY** (Londrillo & Nipoti, ASCL 1102.001) | AQUAL PM in spherical coordinates | none: isolated systems | not cosmological; no switch | licence/download not found (contact authors) | n/a for growth | unknown |
| **Llinares+08 MOND solver** (AMIGA/MLAPM, MNRAS 391, 1778) | AQUAL multigrid in a cosmological AMR code | Friedmann background; CDM/"MOND-cosmology" ICs | no public MOND branch found | not public (AMIGA itself is) | n/a | n/a |
| **Angus & Diaferio QUMOND PM** (arXiv 1104.5040, 1309.6094) | Cosmological QUMOND PM; 11 eV sterile nu-HDM, 256³ in 512 Mpc/h | LCDM expansion with CDM replaced by HDM | private code (not found public) | n/a | n/a | n/a |
| **AeST Boltzmann code** (Skordis & Zlosnik 2021, arXiv 2007.00082) | Linear CMB + matter P(k) in AeST | the abstract does not name the code; no public modified CLASS/CAMB found in this survey | linear only; not B's chassis | not found | n/a | n/a |
| **hi_class** (github hiclass-code/hi_class_public) | Linear Horndeski in CLASS | Friedmann; Horndeski alpha-functions; no MOND, no switch | no | licence field null (CLASS-style), C | yes | repo 82 MB |
| **CLASS / classy** | Linear Boltzmann | LCDM by default (any fluids settable) | only for linear ICs where B = LCDM (CFG324) | C/Python | **INSTALLED** classy 3.3.4 | 0 |
| **CAMB** | Linear Boltzmann | as CLASS | as CLASS | Fortran/Python | **INSTALLED** camb 1.6.6 | 0 |
| **colossus** | Halo model, mass function, concentration, P(k) fits | NFW/Einasto, Tinker/Despali HMF, c(M) calibrated on LCDM sims | DO NOT use for scoring B; use only for LCDM reference curves, labelled as such | BSD-type, Python | **INSTALLED** 1.4.0 | 0 |
| **GADGET-4** (Springel+21) | TreePM/FMM N-body + SPH; FoF/SUBFIND; merger trees | Friedmann background; Newtonian Poisson; N-GenIC ICs (LCDM P(k) input) | MOND would mean rewriting the PM force step (the tree part is Newtonian-only); switch possible in PM only | GPL, C++ + MPI-3, FFTW3, GSL, HDF5 | runs on macOS with Homebrew libs; overkill here | tens of MB + brew deps |
| **RAMSES** (ramses-organisation) | AMR N-body + hydro, multigrid Poisson | Friedmann background (Omega params); Newtonian | host for PoR/RAyMOND | CeCILL-type, Fortran | yes | repo ~100 MB |
| **CONCEPT** (github jmd-dk/concept) | PM/P3M N-body, linear species via CLASS | uses CLASS for background and linear species | Newtonian; MOND = new force term | GPL-3, Python/Cython | yes, but heavy install (bundles its own CLASS, MPI) | repo 18 MB + deps |
| **pkdgrav3** (Potter+17, bitbucket) | FMM N-body, GPU | Friedmann; Newtonian; CLASS-backed ICs | no MOND; CUDA path useless on Mac | GPL-3, C++ | CPU build possible; overkill | not queried |
| **FastPM** (github fastpm/fastpm) / **pmesh** (MP-Gadget/pmesh) / **nbodykit** (bccp) | FastPM: few-step PM; pmesh: MPI FFT mesh; nbodykit: P(k), FoF, catalogues | FastPM: Friedmann LCDM growth factors baked into the stepping (the "FastPM" kick-drift factors assume a growth model); nbodykit: halo-model/HOD tools LCDM-calibrated | pmesh could host the solver but needs mpi4py; nbodykit is unmaintained and hard to build on arm64 | all GPL-3; C / Python | possible but install friction | 22 / 4 / 22 MB + mpi4py, open-mpi |
| **COLA**: MG-PICOLA (GPL-2, C) / FML (C++) by Winther | COLA with scale-dependent MG growth | COLA splits LPT (LCDM-like growth) + PM residual; MG via linear growth + screening recipes | wrong structure for a local nonlinear gate (COLA's LPT frame assumes the large-scale growth law) | GPL-2 / unstated | yes | 8 / 16 MB |
| **Pylians3** (MIT, Cython) | P(k), bispectrum, void finder, correlation functions | estimators are model-free; void finder spherical-underdensity | analysis only | MIT | yes | 1.5 MB |
| **Halo finders** (Rockstar, AHF, SUBFIND, FoF) | Bound-object catalogues | FoF b = 0.2 and SO Delta = 200c/vir are LCDM conventions; unbinding uses Newtonian potential (wrong in MOND-on regions) | FoF is model-free (linking only); unbinding/SO masses must be redone with B's potential | various | own scipy cKDTree FoF suffices at 128³; 256³ is heavier but fits in RAM | 0 (own code) |
| **Filament finder** DisPerSE | Morse-theory skeleton | model-free | T1 already IS a tidal-eigenvalue classifier (T-web) on the mesh; DisPerSE not needed | CeCILL, C++ | builds with CGAL/GSL | not queried |

**In the repo (on disk, no download):**
- `sonnet55_push/puzzle_32pi/qumond_efe_multipole.py`: exact QUMOND of one point mass in a uniform external field
  (Legendre multipoles, spherical grid). Validated kernel + EFE logic; not a 3D mesh solver, not cosmological.
- `nbody_2026/`: stages 1-49 are 1D/semi-analytic (khronon-dust settling, spherical collapse, forest mocks, CLASS
  re-runs). README records that the 3D PM stage was never built (stage 3 no-go for the dust-condensate question).
  No 3D PM N-body code exists in the repo.
- FFT-based helpers exist in `campaign_fresh_gravity/CFG324_candidate_B_growth/cfg324_velocities.py`,
  `CFG4_switch.py`, `CFG288.../cfg288_construction_gates.py` (Gaussian fields, linear switch tests), and `nu_mono` is
  defined in `campaign_fresh_gravity/CFG3_common.py:116` / `CFG5_common.py:233` (shape from L340: y_p = 2.540,
  h_p = 0.6476 a0, delta = 0.05).

**Installed Python (checked 2026-10-06):** numpy 1.26.4, scipy 1.14.1, astropy 7.2, h5py 3.15, healpy 1.19,
Cython 3.2, torch 2.6 (has FFTs; MPS backend possible), **classy 3.3.4, camb 1.6.6, colossus 1.4.0**. Toolchain:
gfortran (Homebrew), gcc. MISSING: nbodykit, pmesh, pyccl, jax, numba, pyfftw, mpi4py, Pylians3, halotools, hmf,
pynbody, yt, treecorr, fastpm; no MPI library found.

## 3. Recommendation

**Best route (one small download): PySCo + a local QUMOND-with-gate patch.** It is the only public, cosmological,
QUMOND, pure-Python PM code found; it is MIT, fits the M4 trivially at 128³-256³, and its FFT mesh already gives
everything T1 needs. Patch (new file in the repo, not an edit of PySCo upstream):
1. nu_mono imported from `CFG3_common.py`, in place of PySCo's families; both a0 footings as separate runs.
2. Each step: delta on the mesh -> t_ij = k_i k_j delta_k/k² (this is D_i D_j psi with psi = Phi_d/(4 pi G rho_bar))
   -> eigenvalues per cell -> f = H_eps(l_2 - tau_ta(z)), eps = 0.077 (CFG355 eps_min), tau_ta from Delta_ta(z).
3. Second Poisson: ∇²φ = ∇·[(1 + f (nu_mono - 1)) ∇φ_N]; curl part dropped (QUMOND, as in the repo's multipole code).
4. Controls, frozen before any run: f ≡ 0 must reproduce Newtonian/LCDM P(k) to <1% (the CFG324 limit); f ≡ 1
   must reproduce L341's "too fast" growth qualitatively; MUTATE runs write separate outputs.
5. A grid-convergence rule (as in CFG358: N = 128/256/(512) with a frozen ratio test), because the mesh scale is an
   implicit smoothing of t_ij and T1's ON-fraction depends on it. The smoothing scale must be declared, not tuned.

**Minimal-download alternative (zero downloads):** write the same PM in numpy/scipy (or torch on MPS) in the repo:
2LPT ICs from installed classy/camb, CIC deposit, FFT Poisson, KDK leapfrog in a, the gate as above, scipy cKDTree
FoF, numpy P(k). ~400-600 lines; 128³ in 128 Mpc/h is minutes per run on CPU. Slower to validate than PySCo, but
every line is committed and verifiable. PySCo could later serve as the cross-check (f ≡ 0 and f ≡ 1 limits).

**RAMSES-based codes (PoR, RAyMOND):** the right cross-check for the published nu-HDM literature, not the first
route: Fortran edits for the gate, MPI install, and RAyMOND's version risk.

**Stripping each LCDM assumption (state each in the criteria file):**
- Background: a Friedmann LCDM background is B's own background (cold component + Lambda); state it as an input,
  not a result. Do not inherit any w0wa.
- Linear ICs: CLASS/CAMB P(k) at z_i ~ 100, where B = LCDM by CFG324 (T1 OFF in all linear samples). Stated as such.
  Baryons + cold component evolved as one fluid at first (a stated simplification).
- Newtonian Poisson: replaced by the gated QUMOND step; f = 0 recovers it exactly.
- a0: constant in physical units (B's a0 is set by rho_Lambda, which is constant); convert to comoving each step.
- Halo definitions: FoF linking only; masses via B's potential (or report lensing-mass proxies Σ-based), never
  Delta = 200c SO masses or Newtonian unbinding; no NFW fits used as data.
- Halo-model tools (colossus HMF, c(M), halofit, HMcode): reference curves only, never in a B score.
- Khronon: not evolved; quasi-static, preferred frame = box frame. This is an approximation and must be stated;
  it is consistent only where MASTER_LAGRANGIAN's khronon coefficients make the khronon non-dynamical on these scales.
- EFE: included by the full-box solve; super-box modes absent (bias for small boxes; test with box size).

**Observables to score that are not LCDM-model outputs:**
- Raw cosmic-shear 2-point (KiDS-1000 xi+/-, measured values + covariance), via Born-approximation projection
  through replicated boxes. A 64-128 Mpc/h box limits this to small angles; a 256-500 Mpc/h box is needed for a
  real score (256³ still fits in RAM).
- Cluster counts with weak-lensing masses (e.g. KiDS/DES/HSC WL-calibrated samples): needs >= 500 Mpc/h; the small
  box only gives the mass-function RATIO B/LCDM.
- Void statistics: void size function and void-lensing profiles with the same finder applied to sim and data.
- Filament lensing stacks (Epps & Hudson 2017, arXiv 1702.08485; Xia+20, arXiv 1909.05852) and a filament
  velocity-dispersion stack, per `SCOPING_filament_constraints_2026-10-06/SCOPING.md`. This is where T1's
  filament-core firing is directly tested; a small box suffices here.
- Mechanism diagnostics (not data scores): T1 ON volume/mass fraction vs z, P(k)_B / P(k)_LCDM, filament-core
  Sigma ratio.

## 4. Caveats

- PySCo's QUMOND source convention in comoving coordinates (total vs background-subtracted field inside nu) is
  NOT verified here; read its source before use. The repo's choice must follow the master Lagrangian, not PySCo.
- PoR and RAyMOND licences not read; the bitbucket page did not render.
- No public AeST/RMOND cosmology code was found; this is a search result, not proof of absence.

## 5. Downloads needing the owner's approval (none made)

| item | what | size (provisional) |
|---|---|---|
| PySCo (`pip install pysco-nbody` or GitHub source) | QUMOND cosmological PM | repo 6.4 MB; + numba/llvmlite ~40-50 MB, pandas, rich |
| pyfftw (optional) | faster FFTs | ~1-5 MB + Homebrew fftw ~10 MB |
| Pylians3 (optional) | P(k), void finder | repo 1.5 MB |
| RAMSES + RAyMOND patch or PoR (cross-check, later) | AMR QUMOND | RAMSES repo ~100 MB; patch small; + Homebrew open-mpi ~50 MB |
| Zero-download route | own numpy PM + installed classy/camb | 0 |
