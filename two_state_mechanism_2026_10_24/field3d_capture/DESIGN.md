# Three-dimensional field and fixed-range capture: authorized experiment

The user requests full 3D tether forces, separate T/F transport, local capture,
conservation, and rotation selection without object-type switches. This checkpoint
implements and tests a specified effective extension; it does not claim that the
spherical constitutive law uniquely determines that extension.

1. Let u be the isolated curl-free Coulomb field of Gaussian-smoothed positive T
   mass, with G=1. Use U_T=kappa²/(4pi) integral w(|u|/kappa) d³x,
   w(z)=-log(1-z)-z. This recovers the earlier radial functional in spherical
   symmetry, but restricts the field to its longitudinal sector. It is NOT the
   minimum over all vector fields with the same divergence. No spherical averaging
   or baryonic center reaction is used.
2. Evaluate the quadratic part analytically over all space (Gaussian self and
   pair energies). Evaluate the nonlinear remainder on a fixed Cartesian grid.
   Differentiate this same finite energy analytically. The mesh and finite box
   break exact translation/rotation invariance; measure those errors and refine.
   The pointwise saturation domain is only sampled numerically, an open caveat.
3. Each medium packet has its own position, velocity and state. Live Newtonian
   softened gravity is inherited. A collision can change state only if the actual
   separation from a baryonic packet is below 0.1 kpc. All profiles use the same
   physical radius and cross section per baryonic mass (1 cm²/g). The rate is
   sigma_per_mass*m_b*incoming_normal_speed/(4pi h³/3). The energy jump is the
   full finite U_T difference. Incoming pair kinetic energy pays it. F->T emits
   91% of remaining normal kinetic energy to an explicit receiver; T->F does not.
   This is an assumed Newtonian radiative interaction, not a microscopic derivation.
4. No noisy expanding-neighbor vorticity barrier, no global density pump, no
   baryon cooling through distant pairs. Baryon cooling uses the same finite-range
   encounter kernel with restitution .5. These changes are explicit new model
   assumptions, not a direct one-variable comparison with the previous scan.
5. Spatially local events need temporal resolution as well: swept-segment checks
   subdivide steps with near encounters and relative motion exceeding 0.2h, and
   event intervals limit the sum of active hazard to 0.1. Check interval refinement.
   This is a finite-rate volume kernel, not exact hard-sphere contact dynamics.
6. Test analytic quadratic limits, force finite differences, nonspherical response,
   field resolution/box size, reaction energy/P/L, a deliberately close encounter,
   and crossed rotating/unordered live initial conditions at all four numeric
   mass/size inputs. Refine packet count and event interval for selected cases.
   Record empty local neighborhoods: zero events with poor sampling is not a
   prediction that a continuum halo remains free.

Engineering gates: force finite-difference relative error <1e-4; total-energy
relative error <1e-3; field U and forces stable to 5% in refinement fixtures;
encounter energy/P/L roundoff. Formation 95% T, free retention90%, RAR residual
.05dex are inherited illustrative targets, not observational likelihoods.

The baryon acceleration diagnostic now samples actual 3D Newtonian acceleration
in the initial disk plane at multiple radii and azimuths, compared with the same
algebraic law applied to the baryon-only radial force. The spherical algebraic
law is NOT guaranteed in a nonspherical equilibrium; this comparison tests it.
