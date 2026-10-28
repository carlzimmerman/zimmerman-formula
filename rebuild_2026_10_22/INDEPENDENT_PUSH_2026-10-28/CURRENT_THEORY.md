# Current phenomenological theory: what the code actually scores

Checkpoint IP28, based on git `7954d48377463cafcae3e8dbb09454134aef384f`
and the separately hashed dirty-tree inputs in the accompanying reports.
This is a new audit checkpoint, not a modification of historical lane results.
It distinguishes CL2/CL3, BS1's primary configuration, and BS1's reported
CL3_L3.75 variant rather than merging their verdicts.

The framework is a phenomenological gravity law plus a gravitating cold-energy
field component with w approximately zero. No covariant action that passes all
required tests has been established. **Kappa = 1/2 remains fitted.**

The acceleration normalization and baryonic law are

\[
a_0=\kappa c\sqrt{G\rho_{\rm DE}},\qquad
g_{\rm law}=\left(\frac12+\sqrt{\frac14+\frac{a_0}{g_N}}\right)g_N.
\]

Here rho_DE is mass-equivalent energy density. Canonical a0 is
9.3603e-11 m/s²; the separately reported alt footing replaces rho_DE by
rho_crit and uses 1.1312e-10 m/s².
For a halo-bearing system the scored branch instead uses g_N + g_halo.
These branches are a phenomenological prescription; the formula for g_law
alone is not a general solution of nonspherical AQUAL.

Define C = 4/[3(3 ln 2 - pi/2)] and Sigma0 = a0/(2 pi G). The core prescription
used for SPARC, optical groups, clusters and isolated lenses is

\[
c_f(M)=L\frac{c_{\rm nat}(M)}{c_{\rm nat}(10^{14}M_\odot)},\qquad
\Sigma_{\rm core}(M)=\max\{\Sigma_0,
 C[c_f(M)]^{5/4}\Sigma_{\rm coll}(M)\}.
\]

CL3 computes its threshold with a **different function**:

\[
C L^{5/4}\Sigma_{\rm coll}(T_f)=\Sigma_0.
\]

CL3 compares each system's own inferred mass to this threshold; its dwarf
branch is assigned by satellite status. BS1's primary instead uses L=4 and
fixed logT=12.3. BS1's **reported, not frozen-primary** CL3_L3.75 variant uses
the threshold above and a basin flag 1{M_basin > T_f(L)} for SPARC, the Milky
Way and dwarfs. Optical groups and clusters retain own-mass flags; isolated
lensing scores are carried from CL3. This variant is the source of the earlier
one-page equation claim. Basin membership changes flags, not every system's
core mass.

Mass budgets also differ by pipeline. Clusters use the GS1 background ratio
Omega_c/Omega_b = 5.2715 times baryons counted to turnaround. SPARC, optical
groups and isolated lenses use the empirical EM1 baryon-to-M200 relation.
Dwarfs use X51's cooling-floor construction; the displayed core formula and
cluster budget are not universal dwarf prescriptions.
Sigma_coll and c_nat depend on the fixed background, collapse prescription,
concentration estimator and numerical resolution. In these runs the formation
spectrum is background A, a CMB refit including fitted amplitude and tilt; the
GS1 budget uses the separate BAO+BBN background. Basin selection is a posit.

At L=3.75, the implemented switch has log10(T_f/Msun)=12.23568 canonical and
12.57388 alt. Using the mass-dependent core coefficient in the X43/background-A
EPS crossover calculation gives 11.22322 and 11.54919 under the S9
interpolation/clamp. The isolated-lensing scorer interpolates a coarser
collapse table and has slightly different core crossings.
Thus the scored switch is **not** the point where the scored core term first
beats the floor. The calibration results cannot be transferred to that literal
single-rule interpretation without a new grade. See
[the scalar audit](native_l_t/README.md).

NL1 and its existing follower await the ng64 zooms. Its primary grade fixes
log10(T/Msun)=12.3; a primary pass cannot by itself remove T as an empirical
input. Its reported CL3 threshold also needs a separate alt-footing root.
L remains data-located pending native convergence. T_f is a specified function
of L under the reported CL3/BS1 linkage, not a field-derived condensation mass.
The assertion that only kappa remains fitted is therefore premature.

The implemented canonical model passes its selected calibration lines in a
finite region. Held-out tensions remain: X-COP radial shape, X-ray-bright
group sign, SLUGGS kinematics, and IC 1613. The latter needs an updated joint
stellar/HI comparison: Taibi et al. (2024) measure stellar rotation and
inclination 32±11 degrees, so the earlier fixed-inclination significance and
dispersion-only interpretation are not a complete uncertainty treatment.
See [the observational evidence](observations/README.md).

Alt has no combined pass in the 72 recounted configuration evaluations; its
SPARC residual scatter passes while its preferred stellar mass-to-light ratio
misses the frozen calibration range. Preserve it as a separate diagnostic;
this checkpoint does not rewrite the standing two-footing rule. See
[the footing audit](footing_audit/README.md).

No result here establishes a condensation field equation, derives kappa, closes
the theory, or shows that the data favor the framework over a comparison model.
