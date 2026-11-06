# QX4 frozen criteria: can the action, not the plain law, rescue AGC 114905 and Malin 1?

Frozen before any QX4 script exists and before any QX4 number. Kappa = 1/2 FITTED; not theory closed. Adopts
nothing. One galaxy excludes nothing. Shared rules: ../SWARM_BRIEF.md. Both footings, never pooled: canonical
a0 = 9.3603e-11, alt 1.1312e-10 m/s^2.

## Starting point (record, not re-graded)

UD1 (167a274304): on AGC 114905 the algebraic law gives chi2/5 = 844 (canonical) and 996 (alt). The outer V_law is
62-65 km/s against 26.9 +- 1.8. The inclination escape needs i = 12-16 deg against i0 = 31 +- 2: NOT RESCUED.
UD2 (46d8dcd8c5): on Malin 1 it gives chi2/4 = 69 and 132, a shape miss (dip at 62.5 kpc). UD3: the frozen warp is
NOT RESCUED.

Inputs are reused unchanged from UD1/UD2: data, error bars, baryon components, i0, D. They are read by
importing those lanes' committed figure-reading code, never retyped. The UD lanes' files are not edited.

## Label per mechanism, per galaxy, per footing

- RESCUED: chi2 p >= 0.05 at the published i0, D and M/L, with the mechanism's inputs inside their measured
  errors (or derived with no free constant), AND the SPARC/RAR recheck below holds.
- CONDITIONAL: rescues only if an input not on disk takes a stated value. The required value is stated, and the
  data needed are written into NEEDS_OWNER.md.
- NOT RESCUED: no allowed input value reaches p >= 0.05.
A scan over an input is used only to state the requirement. It is never a fit, and the result is never relabelled
as a fit.

## Iteration 1: the action's exact static field (full AQUAL solve) in place of the algebraic law

v3s's static sector (and AC2q's, AC8) is AQUAL: div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho, with
mu(x) = x/(1+x), the inverse of the law's nu. In flattened systems the exact field differs from the algebraic
nu(g_N/a0) g_N by a curl term. This iteration solves the equation and grades the exact midplane V_c.

Method:
- Axisymmetric finite-volume solve in (ln r, theta), with equatorial symmetry.
- Dirichlet outer boundary: the deep-MOND monopole sqrt(G M a0) ln r at r_max >= 300 x the outermost ring.
- Nonlinear iteration (Picard with damping, Newton-Krylov polish if needed) to a relative residual <= 1e-8.
- Convergence ladder of two grid sizes (n_r, n_theta) and (2 n_r, 2 n_theta). The graded V must agree between
  the two rungs to 1 %; a ring that misses this is NO VERDICT.

Baryons:
- AGC 114905: UD1's Sigma forms and vertical profiles (stars sech^2 with z_d from UD1, gas Gaussian with
  h = 1.3 kpc).
- Malin 1: HSB as a sphere with M(<r) = V_hsb^2 r / G, which reproduces its Newtonian curve exactly. LSB and gas
  as thin discs with Sigma from Toomre's thin-disc inversion of UD2's plotted V^2 curves (Keplerian
  extrapolation beyond the plot). Thickness: Gaussian h = 1 kpc primary, 0.5 and 2 kpc reported. Known answer
  K4 below gates the inversion.

Known answers, all of which must pass or there is no label:
- K1 Plummer sphere: exact AQUAL radial g = algebraic nu(g_N/a0) g_N to 1e-3 (exact in spherical symmetry).
- K2 thin Kuzmin disc (h/a = 0.02): midplane exact V = algebraic V to 2 % (Brada & Milgrom 1995: the algebraic
  relation is exact for a Kuzmin disc, up to thickness corrections).
- K3 mu = 1 (Newton): the solver reproduces the ring-sum Newtonian V_c (UD1's method) of the same density to 1 %.
- K4 Malin 1: the inverted Sigma reproduces UD2's plotted Newtonian V_gas and V_lsb at the Table radii to 3 %.
MUTATE (separate outputs): the graded run with mu = 1 must reproduce UD1/UD2's Newtonian-baryon chi2 (55.0 and
1752.6) to 2 %. This shows that the grade sees the interpolation function.

SPARC/RAR recheck: on a grid of exponential discs spanning SPARC (Sigma_0 = 10 to 1000 Msun/pc^2, R_d = 1-5
kpc, thin stellar disc plus an extended gas disc), compute |log10(g_exact/g_alg)| at R = 1-8 R_d. It must stay
<= 0.057 dex, the RAR's intrinsic-scatter bound (Li+2018). Otherwise the SPARC pass needs a regrade, and no
RESCUED label is given.

## Iteration 2: the external field effect on the action's equations

- Requirement: the 1D EFE estimator already used by UD1/UD2,
  g = nu((g_N + g_e)/a0)(g_N + g_e) - nu(g_e/a0) g_e. The smallest g_e with p >= 0.05 at i0 is the requirement
  (none in [0, 3 a0] means NOT RESCUED for any EFE).
- Host requirement, analytic and stated before computing: a host of baryonic mass M at distance d in its deep-MOND
  region gives g_e = sqrt(G M a0)/d. Its tidal acceleration across the disc radius R is about g_e R/d. A regular
  rotating disc needs g_e R/d < g_int = V_obs^2/R at the outer ring. Together these give M_req (the minimum host
  baryonic mass) and d_req.
- Label: CONDITIONAL if g_e,req exists. The neighbour data needed are written into NEEDS_OWNER.md (none on disk).
  NOT RESCUED if no g_e reaches p >= 0.05.
- SPARC recheck: not needed. EFE is environment-specific and does not change isolated SPARC fits. That is stated,
  not graded.

## Iteration 3: everything else the action and the data allow (bounds and requirements)

- Action terms beyond AQUAL: v3s stiffness, -(gamma/2)[max(D.P,0)]^2, relative size <= (Lstar/R)^2 at R. AC2q's
  s^2 terms, relative size <= 2.2e-10 (AC8). Each is a bound, compared with the required relative change in g at
  the worst ring. The required relative change is (V_obs/V_alg)^2 - 1 at i0.
- Non-equilibrium: the time for gas moving below the law's circular speed to fall in, t_ff ~ R/V_law at the outer
  ring. This is compared with the disc's orbital time 2 pi R/V_obs. RESCUE needs the disc to be younger than t_ff,
  and that is stated as a requirement.
- Data-side requirements, each against its measured error:
  - distance (V_law^4 is proportional to M, and M to D^2, in deep MOND, so the D factor needed);
  - gas mass (factor needed);
  - asymmetric-drift sign (the correction raises V_c, so it cannot lower it);
  - beam smearing (it lowers inner points only, and the miss is outer).
  NOT RESCUED if every requirement exceeds 3 sigma of its measured error, or has the wrong sign.

## Overall

If no iteration gives RESCUED, and CONDITIONAL is the best, the lane records the class no-go: "no mechanism in
the v3s/AC2q action rescues galaxy X at its measured inclination without [stated requirement]". The labels are
written into the CLOSURE.md row, and the miss stands on the record.
