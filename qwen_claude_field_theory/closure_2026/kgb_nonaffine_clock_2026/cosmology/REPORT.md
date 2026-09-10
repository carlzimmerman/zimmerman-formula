# Same-action cosmology gate: global a0, mapped matter, and CMB limits

2026-09-10. **CMB safety is unresolved.** Exact background identities and
conditional coupling exclusions are obtained below; no CMB likelihood, early
P/G extension, or globally healthy cosmological solution is invented. One
global constant a0 is used as the acceleration unit, never a separate value per
halo. The clock remains an explicit scalar; no dark-matter particles are added.

## 1. Background equations of the same physical action

Start from the current action

\[
 \sqrt{-g}\left[FR+\frac{3F_X^2}{2F}(\nabla X)^2+P-G\Box\phi\right]
 +\mathcal L_m[g],\qquad X=-\tfrac12(\nabla\phi)^2.
\]

For a physical spatially flat FLRW metric, let t be physical proper time,
H=dot(a)/a, and use C=2F/m, Delta=C-X C_X. On C>0, Delta nonzero,

\[
 d\tau=\sqrt C\,dt,\quad \widetilde a=\sqrt C\,a,\quad
 \widetilde H=\frac{H+\dot C/(2C)}{\sqrt C},\quad
 \chi=X/C,\quad \chi_{,\tau}=\Delta\dot X/C^{5/2}.
\]

Write u=dphi/dtau, so chi=u^2/2. Ptilde and Gtilde are exactly the transformed
functions in `../dictionary/REPORT.md`, not functions borrowed from a previous
cosmological model. Their homogeneous current, energy and pressure are

\[
 J_\phi=u\widetilde P_\chi+6\widetilde H\chi\widetilde G_\chi,
\]
\[
 \rho_\phi=2\chi\widetilde P_\chi-\widetilde P
             +6\widetilde H u\chi\widetilde G_\chi,
 \qquad p_\phi=\widetilde P-2\chi\widetilde G_\chi u_{,\tau}.
\]

The matter terms must be mapped as well. Define

\[
 \kappa=\frac{d\log C}{d\chi}=\frac{CC_X}{\Delta},
 \qquad T_m=-\rho_m+3p_m.
\]

Varying physical minimal matter with respect to the EF metric and clock gives

\[
 \boxed{\widetilde\rho_m
 =\frac{\rho_m-\kappa\chi T_m}{C^2}
 =\frac{C\rho_m-3XC_Xp_m}{C^2\Delta}},\qquad
 \widetilde p_m=\frac{p_m}{C^2},\qquad
 \boxed{J_m=-\frac{u\kappa T_m}{2C^2}}.
\]

In particular physical dust has rho_m/(C Delta), **not** rho_m/C^2, as EF
energy density. Radiation with zero trace has no extra clock-current term.
For separately conserved physical constant-w fluids, the mapped homogeneous
matter Routhian is

\[
 L_m=-\widetilde N\widetilde a^3\mathfrak f(\chi,\widetilde a),\quad
 \mathfrak f=C^{-2}\rho_m(\widetilde a/\sqrt C)
 =\rho_{m0}\widetilde a^{-3(1+w)}C^{(3w-1)/2}.
\]

The code varies its lapse, scale factor and clock before imposing unit lapse.
All three resulting expressions agree with the boxed map. It also verifies
the energy-exchange identity

\[
 \widetilde\rho_{m,\tau}
 +3\widetilde H(\widetilde\rho_m+\widetilde p_m)
 =u(J_{m,\tau}+3\widetilde HJ_m).
\]

Consequently the actual background system is

\[
 3m\widetilde H^2=\rho_\phi+\sum_m\widetilde\rho_m,
 \quad -2m\widetilde H_{,\tau}
 =\rho_\phi+p_\phi+\sum_m(\widetilde\rho_m+\widetilde p_m),
\]
\[
 \partial_\tau[\widetilde a^3(J_\phi+\sum_mJ_m)]=0,
 \qquad \dot\rho_m+3H(\rho_m+p_m)=0.
\]

The scalar equation and the two metric equations have the expected conservation
dependence. The conserved **homogeneous** charge is an initial/boundary datum;
the galaxy condition J^r_total=0 does not set this temporal charge to zero.

## 2. A useful kinetic gate, with explicit limits

After the cubic integration by parts, define B(u) by B_u=u^2 Gtilde_chi.
The EF homogeneous Lagrangian, retaining the lapse, is

\[
 L=-3m\widetilde a\dot{\widetilde a}^{2}/\widetilde N
 +\widetilde N\widetilde a^3(\widetilde P-\mathfrak f)
 +3\widetilde a^2\dot{\widetilde a}B(u).
\]

The actual two-velocity Hessian and its scale-factor Schur complement give

\[
 \mathcal D_{\rm hom}=
 \widetilde P_\chi+2\chi\widetilde P_{\chi\chi}
 +6\widetilde H u(\widetilde G_\chi+\chi\widetilde G_{\chi\chi})
 +\frac{6\chi^2\widetilde G_\chi^2}{m}
 -\mathfrak f_\chi-2\chi\mathfrak f_{\chi\chi}.
\]

This supplies a homogeneous kinetic diagnostic at fixed conserved fluid
numbers. It is **not** the full scalar-fluid perturbation kinetic matrix, a
gradient-speed certificate, or a Dirac count. The vacuum static helper cannot
be applied to a matter-filled FLRW background without its missing matter modes.
For physical dust, the extra coefficient reduces to

\[
 \mathcal D_{m,\rm dust}
 =\frac{\rho_m[C_X\Delta+2XCC_{XX}]}{2\Delta^3}.
\]

The general extra matter coefficient vanishes for trace-free radiation. At the quadratic seed X=.5,C=1.05,
C_X=.1,C_XX=2j, this dust coefficient is rho_m(.05+1.05j). A negative value
is a potentially large matter-induced kinetic correction, not automatically a
cosmological ghost: the other terms and the actual evolving solution are still
needed. Lean verifies this coefficient's conditional sign implication; it does
not promote it to a CMB exclusion.

## 3. What fixed quadratic F can already exclude

The diagnostic deliberately extends **only F**, not P and G:

\[
 F=.525+.05(X-.5)+\tfrac12j(X-.5)^2,\quad
 C=1+.1X+j(X-.5)^2,\quad \Delta=1+j(.25-X^2).
\]

Here Q_clock=2X is the squared physical proper-time clock rate on FLRW; it is
not H/a0, not a spatial acceleration, and not the different Q notation in other
papers. On the seed-connected branch with increasing X>=.5:

| Fixed j | First excluded Q_clock | Cause |
|---:|---:|---|
| -100000 | 1.00648174077556 | F=0 |
| -10000 | 1.02050390397167 | F=0 |
| 0 | no finite F/map zero | tensor normalization still runs |
| 10000 | 1.00019998000400 | Delta=0 |
| 100000 | 1.00001999980000 | Delta=0 |

For j>0 the exact map boundary is Q_clock=sqrt(1+4/j); every negative j
eventually makes this fixed quadratic F negative. The executable samples also
include Q_clock=1,1.001,1.01,10,10^6. Points beyond a zero are marked disconnected
from the seed even if Delta becomes nonzero again. F_X=0 alone is not a
cosmological field-map singularity, although it obstructs the chosen static
inverse chart.

This does not prove early cosmology drives X upward or to large Q_clock. A
cosmological solution could stay near the seed or enter a different range.
It excludes the stated quadratic extrapolation **if** a proposed history must
cross those boundaries; it does not exclude nonquadratic completions.

For j=0, the tensor-sector normalization ratio is
G_tensor(X)/G_tensor(.5)=1.05/(1+.1X). At Q_clock=10^6 it is about 2.10e-5.
G_tensor=1/(16 pi F) is not automatically the experimentally measured Newton
constant: scalar mixing, source normalization and physical perturbation
response still have to be computed. A varying F is a different parameter from
varying a0; fixing global a0 does not freeze the gravitational coupling.

## 4. Exact L121 audit: neither a kill nor a rescue

The literal script from `727af1f7a99d729366bbfc66266c67a4c15d25f3` was inspected
and rerun read-only. Its six PASS labels reproduce, but support less than the
surrounding claims:

- Lines 64-67 check only .1<a0/(cH0)<.25; this does not derive the claimed
  exact dark-energy normalization.
- Lines 72-91 use a Lambda-CDM expansion benchmark and compare two different
  hypotheses: constant a0 and a0 proportional to H(z). The latter is not a
  consequence of constant Lambda or a correction to the former.
- Lines 82-91 infer MOND off/on from a horizon-scale ratio. The perturbation
  amplitude and wavelength, and this theory's perturbation equations, are absent.
- Lines 97-104 compute equality redshifts using assigned density fractions;
  they do not evolve this no-particle-DM action's fields or compute CMB peaks.
- Lines 105-109 and 135-139 pass literal True. They do not calculate clustering,
  a Boltzmann hierarchy, ghost bounds, or a likelihood. Earlier branch-specific
  ghost/BBN assertions cannot be imported into the current action by a label.

The arithmetic itself gives H_rec/H0=23225.0006582 and, for the fixed global
a0 used there, a0/(cH_rec)=6.1556006714e-6. For an illustrative physical metric
potential mode, g_mode/a0 is of order

\[
 [ck/(aH)]\,|\Psi|\,[a_0/(cH)]^{-1}.
\]

At ck/(aH)=1, amplitudes 1e-5 and 1e-6 give respectively about 1.62 and .162,
despite the identical horizon ratio. These are scaling controls, not a
recombination solution or a prescription for applying the galaxy law to CMB
modes. Thus neither categorical off nor on follows from that ratio alone.

Globality (spatial universality) and time constancy are distinct. This task
holds a0 fixed globally; a separately specified universal time-dependent a0
would be another model, not a per-halo parameter. Replacing a0 by local density,
local curvature or H(z) has not been derived from this action.

The cited AeST paper computes spectra from its own background and linearized
equations and explicitly notes a0 is absent from its linear cosmological
regime. Its different scalar-vector dynamics are not this model's missing
cosmology. Exact primary versions and convention checks are in `SOURCES.md`.

## 5. What is still needed for genuine CMB accuracy

Local galaxy jets cannot fix early cosmology. A simple executable witness adds
lambda(X-.5)^3 to P: its value and first two derivatives at the galaxy seed are
unchanged, while at X=2 its EF energy changes by (585/32)lambda for the affine
control. This is an underdetermination witness, not a proposed completion.

The next necessary inputs and checks are:

1. One global F,P,G over the entire cosmological X interval; its vacuum term,
   global normalization and homogeneous charge/initial branch. No fresh fitted
   functions per epoch, mass, galaxy, or observable.
2. Solve the displayed physical/EF background system with ordinary baryons,
   radiation and specified standard neutrinos. Obtain physical H(a), X(a),
   source calibration and gravitational response; do not insert the LCDM
   H(z) benchmark as the solution.
3. Maintain F>0 and invertibility, then derive and test the full coupled
   clock/metric/matter kinetic and gradient operators. Check early gravitational
   normalization, strong coupling and fluid perturbations; positive local static
   coefficients and the homogeneous coefficient above are insufficient.
4. Evolve physical scalar potentials, clock fluctuations, baryon-photon and
   neutrino perturbations with specified primordial conditions and recombination.
   Compute TT, TE, EE and lensing spectra before claiming CMB safety. The same
   functions must also retain the sourced galaxy/lensing and time-dependent tests.

No numerical early-G observational bound or fake CMB likelihood is assigned.
These obligations narrow the next calculation without claiming that CMB data
already falsify or certify the current local construction.

## Reproduction and limits

`python3 -B cosmology/test_cosmology.py` from the package root runs eight tests;
all pass. `cosmology/run_cosmology.py` reruns those tests, five conditional Lean
lemmas, and the literal L121 program, recording actual commands and outputs.
The current bounded evidence is in `run_002/` (superseding `run_001/` after a
notation correction and an explicit Mathlib revision pin); it separates successful execution from
the unsupported physics assertions in L121. An initial broad Mathlib import
failed because an unrelated cached object was absent; specific installed
imports then compiled the five lemmas successfully. No library or old file was
modified to achieve that result.

Computation-audit guided exact checks and provenance; literature-check used two
authenticated primary versions, and proofread-math covered the new derivation.
Only new `cosmology/` files were written. No commits, index changes or pushes.
