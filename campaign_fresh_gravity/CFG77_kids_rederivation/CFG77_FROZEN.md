# CFG77 -- independent re-derivation of the KiDS-1000 early/late lensing colour-split chi2   (FROZEN before any run)

QUESTION. Starting from the READMEs' stated model and the committed data files only (my own code; no exec/import of CFG61/CFG67
analysis code), do I reproduce (i) B's colour-blind law's early-minus-late chi2 = 28.1/7 (canonical, and 28.1 alt), (ii) the f_hot
ladder 28.1, 18.2, 10.0, 4.8, 4.1 at f_hot = 0, 0.25, 0.5, 1, 1.5, (iii) CFG67's LCDM control chi2 = 6.5/7?

DATA (read directly): real_research/data/lensing_rar/brouwer2021_rar/Fig-8_RAR-KiDS-isolated_Colorbin_{1,2}.txt (bin 1 late u-r<2.5,
bin 2 early), ..._Colorbins_covmatrix.txt (900 rows [m,n,i,j]; cov / col-7 bias product; ESD, err / bias col 5), Sersic files (not
needed). Lenses: real_research/data/lensing_rar/lr_lenses.npz (z, logM, Mgal, typ 1 early). Mandelbaum+2016 table:
real_research/data/mandelbaum2016_lbg_halo_mass.tsv.
DEFINITIONS TAKEN FROM THE REPO (read, not executed; disclosed): the kernel is nu_mono (FP1_static_sector.py's monotone repair of
nu_RAR; I re-implemented it from its 8-line definition), a0 canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, flat LCDM Om=0.3153,
h=0.6736 for rho_m(z), and the recipe for the LCDM comparator (Dutton-Maccio c, Om=0.315, H0=67.4 for 200c, M200m/0.673 conversion).
The top-hat turnaround contrast 1+delta_ta(a) is my own spherical-collapse solution (no repo code).

MODEL (README). Lens i, g_bar bin k (edges logspace(1e-15, 5e-12, 16)): R = sqrt(G M_gal,i / g); within-bin average uniform in ln g
with weight 1/g times lens weight M_gal,i (pairs per ln g ~ M_gal/g). Dark+baryon model: point mass M_gal + spherical dark profile.
LAW: M_L(<r) = M_gal nu_mono(G M_gal/(r^2 a0)) for r <= r_e = 0.4 r_ta, frozen beyond; r_ta = radius where the UNTRUNCATED law's mean
enclosed density = (1+delta_ta(a)) rho_m(a), a = 1/(1+z_lens). DeltaSigma of the enclosed-mass profile by my own projector.
K1 = bins where the (unweighted) lens median R of BOTH classes < 0.3 Mpc (expected: bins 8..14, 7 bins).
STAT. D_obs = d_early - d_late on K1; C_D = C_ee + C_ll - C_el - C_le; chi2_L = (D_obs - D_L)^T C_D^-1 (D_obs - D_L), dof 7.
LCDM (CFG67): DeltaSigma = point mass M_gal + NFW(M200c), M200c = M200m->200c conversion of Mandelbaum(logM*, red early / blue late)
at h=0.673, interpolated in log M* with clamping at the table ends; NFW density truncated at 5 R200c. chi2_Lambda same statistic.
f_hot ladder: early lenses only, true baryon point mass M_true = M_gal (1+f_hot) drives the law (nu argument and amplitude); the pair
radius R stays sqrt(G M_gal/g) (bin coordinate is Brouwer's g_bar, which excludes hot gas). (Ambiguity declared: alternative reading
R from M_true is reported as a bracket only.)

PASS LINES (set now; no tuning after results).
 CONTROLS (all must pass; a failure invalidates the corresponding downstream number):
  K1  covariance: chi2 with the stated covariance (via np.linalg.solve) equals an explicit Cholesky whitening and an explicit
      inverse to 1e-8 relative; the C_D block algebra equals the direct 15-bin-slice construction; sqrt(diag C) equals col-5 error/bias
      to 1e-3; all-15-bin early-vs-late chi2 = 119.9 +-0.5 (u-r) and 69.1 +-0.5 (Sersic) [the committed C1 target].
  K2  projector: point mass DeltaSigma = M/(pi R^2) exact; singular isothermal sphere M = k r (r <= r_max large): DeltaSigma = k/(4R)
      to 1e-3 in the interior; NFW vs the Wright & Brainerd closed form to 1e-3.
  K3  the law at fixed g_bar in the deep regime (1e-13, 1e-12) is mass-independent between M_gal=1e10 and 1e11 to 3%, and equals
      sqrt(a0 g)/(4G) (SIS) to the extent nu_mono is y^-1/2 there (reported); delta_ta EdS limit 9 pi^2/16=5.552 to 1e-3.
  K4  gridded lens stacking agrees with an exact per-lens calculation on 400 random lenses to 1% in the stack.
  K5  SWAP (early/late DATA swapped, models kept with their classes): the law chi2 barely moves (|delta| < 0.5, because D_L ~ 0) and
      the LCDM chi2 rises steeply (README: 6.5 -> 124.1; pass = > 100).
  K6  MUTATE=1 (early-type lens M_* and M_gal x2): LCDM chi2 must move by > 1.0. The law chi2 is PREDICTED not to move (K3's mass
      independence): |delta| < 1.0 expected; if it does not move that is the framework's structure, reported, not counted as a
      pipeline failure; if it moves by >1.0 that contradicts K3 and is reported as a failure.
 REPRODUCTION (compare to CFG61/CFG67, tolerance = displayed digits):
  R-A chi2_L canonical = 28.1 +-0.15; alt = 28.1 +-0.15.  R-B ladder each entry +-0.15.  R-C LCDM chi2 = 6.5 +-0.15 (also give Ahat).
  "Approximate" (0.15 < diff <= 1.0) and "non-reproduction" (> 1.0) are reported as such, with cause.
ATTACK RUNS (reported, not pass/fail): the zero-model chi2 D_obs^T C_D^-1 D_obs; dependence on the K1 choice; on the M* floor (early
M_* +-0.1 dex), the IMF/M_gal scale (x0.7, x1.5 on both / on early only), and the isolation cut (lens subsamples by chi / z thresholds,
if the lens file's chi column supports it).
Programme rules: no claim the data favour the framework; kappa=1/2 fitted; non-reproduction is a valid outcome.
