# CONTEXT DIGEST for the Hermes push (state of the programme as of 2026-09-11)

Read this first. Everything here is backed by a committed script or a Lean theorem in the repository; paths are relative to the repository root.

## Authoritative sources (read on demand, not all at once)
- `FRIED_CHICKEN.md` — the gate specification (the 13 gates a complete theory must pass).
- `README.md`, section "The gems" and the standing blocks (rev. 10, rev. 9) — the map of what survives and what is closed.
- `fable_independent_2026/FINDINGS.md` — the exclusion map, entries L129–L187 (one entry per lane; each names its script and checks).
- `fable_independent_2026/lean_2026/Mondlean.lean` — 105 theorems, zero sorry (build with Lean 4 / Mathlib; `Real.pi` unavailable: pass pi as a parameter).
- `RETRACTIONS.md`, `INTEGRITY_AUDIT.md` — retracted claims; never re-cite them.
- `qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/REPORT.md` — the lead field-theory candidate
  (cuscuton clock + dynamical scalar + cubic coupling), its finite-k transfer operator (`transfer_evolve.py: mode_system`), its branches. Read-only.
- Papers (Zenodo, all not peer reviewed): PAPER13 candidate status 10.5281/zenodo.22699828; PAPER14 observing case 22700993; PAPER15 Hubble-kernel
  equation 22706925; PAPER16 DESI check 22708060; PAPER17 clock stability theorem 22717950; PAPER18 ledger geometry 22718357.

## The equations
- Kernel: g = nu(x) g_N, x = g_N/a0, nu_RAR(x) = 1/(1 - e^{-sqrt x}); QUMOND form: grad^2 phi = div(nu grad phi_N).
- Scale: a0 = kappa c sqrt(G rho_DE); kappa = 1/2 fitted (measured 0.465 +/- 0.076 BTFR, 0.551 +/- 0.043 distance-free). Footings 9.3619e-11 / 1.1279e-10 m/s^2.
- Flat a0(z) (w = -1). Hubble-kernel growth: G_eff(z)/G = nu(cH(z)/a0), (cH0/a0)^2 = 8 pi/(3 kappa^2 Omega_Lambda) = 49, Lean `hubble_kernel_identity`.
- Lead candidate action (signature -+++, c = 1): S = int sqrt(-g)[ M^2/2 (R - 2 Lambda) + P(X,tau) - V(tau) + s W(Y,tau) + gamma X box chi ] + S_r + S_b,
  s = sqrt(-(d tau)^2), n = -d tau/s, Q = n.d chi, Y = (g + n n) d chi d chi, X = Q^2 - Y. Clock is a cuscuton (linear in s). Closure on the branch:
  W = U, W_Y = d, P_X = U d/m, P_XX = 2 U d^2/m^2, m = U - 2 d q^2 (logarithm margin), m_rel = m/U.

## The certified necessity (L166, Lean) and the ledger (L172, L187)
Any completion passing galaxies + clusters + CMB + forest must contain: (i) a real clustering cold component with retained fraction f rising with
host mass; (ii) a non-barotropic effective fluid; (iii) a locally screened preferred-frame source.
Ledger anchors: SPARC spiral (1.2e10 Msun baryons, M200 ~ 3e11, r = 3 R_d = 7.5 kpc = 0.50 r_s): f <= 0.105 strict (0.58 loose, kick-redistributed
profile); Milky Way (M200 1e12, r = 30 kpc = 1.19 r_s): 0.14; X-COP cluster (M200 1e15, R500 = 1.38 Mpc = 2.71 r_s): 0.576; CMB: >= 0.988.
GEOMETRY (L187, PAPER18): one universal NFW concentration c* = 0.40 gives 0.086 / 0.165 / 0.704 — the mass dependence is the measurement window,
not physics. Cost: c* = 0.4 << 3-4 (any collapsed halo) => no structure below ~Mpc => k_cut <~ 1 h/Mpc => forest dead (see kills).

## Gates and their current numbers (both footings unless stated)
- Rotation curves / RAR: reproduced by the kernel (this is the fit, not a prediction). dSph external-field effect ~1.9x across radius (hunt_2026/g06*).
- Milky Way decline (Gaia DR3 slope -0.47 +/- 0.15): kernel + LMC external field gives -0.35 to -0.20 (L172) — undecided.
- Clusters: kernel undershoots by ~2x at R500; real component 0.576 required (X-COP); residual profile rho ~ r^-1.53, not cored.
- CMB: third peak needs >= 0.988 of a clustering cold budget at recombination (L129/L165 smooth-dust deficit 0.55 vs 0.99). A mean-field kernel in
  CLASS (L183/L184) does not restore it (restoration -0.00) and adds an ISW-borne low-l excess x578/x785 at l = 30 (intrinsic ISW rate (aH/2) u/(e^u-1),
  Lean `mean_field_isw_rate_*`). Kernel on linear scales is excluded at the CMB on both prescriptions.
- Lyman-alpha forest: dark-matter power at k = 5 h/Mpc, z = 2-3 within 10% (L168 convention). Kernel-boosted baryons alone: 0.04-0.14 of LCDM (L176).
- S8 / growth: Hubble kernel gives S8 = 0.843-0.847 (+1.1-1.5%), fsigma8 +2.7-3.8% at z = 0.3; DESI DR1 consistent (chi^2/bin 0.65-0.73), needs ~1%.
- Lensing: a kernel on the peculiar field on linear scales gives potential power 9-25x LCDM (L179, dead); galaxy-galaxy lensing (KiDS) allows <= 14% of a
  CDM-like halo around galaxies; clusters need 32-46%.
- PPN / Cassini / wide binaries: strict AQUAL fails Cassini 4-5x; a double-filter (Helmholtz-smoothed) kernel survives statically with xi >= 0.03-0.04 pc;
  boosted PPN: a cuscuton clock is dragged (dead), a stiff K^2 clock passes at the cost of c2 <= 0.043 G-shift (L170/L171). Gaia DR4 arms preregistered
  (gamma_v band 1.16-1.23 vs covariant ceilings 1.045/1.030) — frozen, append-only, do not touch `prep_2026/gaia_dr4_prep/`.
- Stability: gradient instability throughout deep MOND for the earlier scalar (L60); the lead candidate's clock is gradient-stable iff s0 <= 1 (L185/L186).
- BBN / N_eff: two-body decay daughters excluded (Delta N_eff); stiff-partner theorem for shift-symmetric k-essence dust.

## Closed doors (do not reopen without a NEW mechanism type; each has a script)
- Acoustic depletion (sound speed): clock stability theorem, c_s^2 = (1 - s0) m_rel/(2 - m_rel); forest needs c_s^2 <= 1e-9 -> lambda_J < 7 kpc (L185/L186).
- Decay/kick depletion: lifetime pincer forest tau >= 41 Gyr vs galaxies tau <= 20 (L167 N-body kicks eta(3R_d) = 0.58 at v_k = 1.8-2.2 v_flat; L168 exact linear response, plateau (1 - f_d)^2).
- Late collapse / top-down: regeneration at k = 5, z = 2.2 = 0.04 / 0.45 / 0.81 for k_cut = 1 / 2 / 4 h/Mpc (L187).
- Velocity filter / internal-clock fluid: small-scale shear C_l(1000) 0.27-0.76 (L173/L174). Potential-depth threshold: forest (L175). Time-dependent
  coupling: S8 0.48-0.54 (L177), knife-edge only with full peculiar-kernel credit, which itself overshoots (L178 S8 1.22-1.25).
- Thermal relic (pincer, no interior), wave/fuzzy DM, condensates (superfluid/BEC/ghost/DBI), Pauli, environment-switched medium (KiDS interleaving):
  all closed in `hunt_2026/g03*-g04*` and `closure_2026/`.
- Single-metric kinetic-mixing action: right static theory (double filter derived, Cassini safe), certified to fail cosmology (uniform dark fraction) (L169).
- Two-mode MOND forces a preferred frame (foliation theorem); canonical MOND scalar cannot close the constraint algebra (cuscuton classification).
- kappa = 1/2 is provably underivable by the candidate actions (zero-mode theorem); do not attempt to "derive" it from dS-Unruh (excluded 15.6 sigma).

## The one open door, stated exactly
Find dynamics (from an action) under which the real cold component is depleted inside ~2 scale radii of every halo to the ledger's values, with its
megaparsec-scale power intact at z >= 2 and its linear growth intact, that is NOT a sound speed, NOT a decay/kick with a universal lifetime, and NOT
a suppressed primordial spectrum. Candidates worth a first look (none tested): conversion of the component into the MOND scalar's configuration
energy inside halos with explicit energy bookkeeping against the late-time Omega_m budget (BAO/SN at 3%); a component whose coupling to gravity is
screened by the MOND scalar's local state (must not screen the linear regime or the forest: check S8 first); dynamics that make halos of the
component unrelaxed (c* ~ 0.4) without cutting linear power (e.g. late, halo-gated energy injection with mass conserved — check clusters and Omega_m).
Kill order for any candidate: forest (z = 2-3) -> S8/shear -> clusters (0.576) -> KiDS (<= 14%) -> Omega_m budget -> CMB -> PPN.

## Tools you may reuse (import read-only, copy into hermes_push/ if you need to modify)
- QUMOND cosmological PM code: `fable_independent_2026/L176_framework_pk_baseline.py` (validated vs halofit to 26-35%); higher-resolution variant with
  bincount CIC in `L187_late_puffy_component_topdown.py` (box 25, 192^3; absolute floor 50%, phase-matched ratios robust).
- Exact linear response for kicked/decaying dark matter: `fable_independent_2026/L168_flux_power_two_body_decay.py`.
- N-body kick retention in galaxy hosts: `fable_independent_2026/L167_nbody_kick_test.py`.
- Patched CLASS 3.3.4.0 with a mean-field kernel: `fable_independent_2026/L183_class_mond_kernel/` (site build; inputs mond_a0, mond_zmin, mond_nuprime ...).
- The lead candidate's operator and branches: `.../cosmological_bridge_2026/{transfer_evolve.py, radiation_probe.py, background_evolve.py, branch_kinetic.py}`.
- Lean: Mathlib v4.34-era; useful lemmas `lt_div_iff₀`, `div_le_iff₀`, `le_div_iff₀`, `Real.add_one_le_exp`, `Real.add_one_lt_exp`, `mul_inv_cancel₀`,
  `linear_combination`; `field_simp` often closes goals (a following `ring` then errors with "no goals").
- Check harness: `hermes_push/harness.py` (check() with no literal-True, both footings, nu_RAR, commit guard).
