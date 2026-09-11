# Same-action cosmological bridge — OPEN, 2026-09-11

## Result and boundary

Newest checkpoint: [joint high-precision evolution](COUPLED_PRECISION_REPORT.md)
obtains decreasing original-Euler residuals across six step refinements in
the short low-k test. This is bounded numerical progress, not full closure.

Latest checkpoint: [precision isolation and backward radiation continuation](PRECISION_RADIATION_REPORT.md)
isolates evaluation roundoff and reaches a radiation-majority homogeneous
branch without refitting. Differentiated transfer convergence and CMB
viability remain open.

Subsequent checkpoint: [finite-wavelength Python evolution](TRANSFER_REPORT.md)
now implements the reduction and records three wavenumbers with six initial
basis modes each. Its limited numerical agreement is not a CMB or convergence
certificate; the original report below records the preceding derivation.

The frozen cubic clock action now has an unrestricted scalar metric/matter
variation, independently checked stress/current sources, exact off-shell
energy and momentum identities, and a short matter-containing homogeneous
trajectory preserving both constraints. A separate stock CLASS run supplies
a GR positive control. No coefficient function was reconstructed or refitted.

This is **not a complete relativistic MOND theory or a CMB prediction**.
This clock sector has not derived the exponential MOND law.
The radial solver's fine-grid tangency failure remains unresolved; this
homogeneous calculation does not rehabilitate its late-time galaxy results.

Carl Zimmerman supplied the primordial-clock direction, the insistence on a
global acceleration scale, and the same-action closure target. These are
credited research motivations, not claims that the operators below are new.
No priority or universal no-go claim is made here.

Started at commit 4dc6e9c79133f9b71ea8835df20739cf5d26fb1e. Concurrent commits
8b5f0a7cc and 9b9974e69 were inspected, not overwritten.
See [the L183 review](CLAUDE_L183_REVIEW.md) and [commands](COMMANDS.md).

## One frozen action

Use signature \((-+++)\), \(c=1\), and \(M^2>0\):

\[
 S=\int d^4x\sqrt{-g}\left[
 \frac{M^2}{2}(R-2\Lambda)+P(X,\tau)-V(\tau)
 +sW(Y,\tau)+\gamma X\Box\chi\right]+S_r+S_b,
\]
\[
 s=\sqrt{-\nabla_\mu\tau\nabla^\mu\tau}>0,\quad
 n_\mu=-\partial_\mu\tau/s,\quad Q=n^\mu\partial_\mu\chi,\quad
 Y=(g^{\mu\nu}+n^\mu n^\nu)\partial_\mu\chi\partial_\nu\chi,\quad
 X=Q^2-Y=-\nabla_\mu\chi\nabla^\mu\chi.
\]
\[
 S_r=\int\sqrt{-g}\,C_rX_r^2\,d^4x,\quad
 X_r=-\nabla_\mu r\nabla^\mu r,\qquad
 S_b=\frac12\int\sqrt{-g}\,\rho_b(X_\theta-1)\,d^4x,\quad
 X_\theta=-\nabla_\mu\theta\nabla^\mu\theta.
\]

The last action is ordinary irrotational baryon dust; the radiation action
is a perfect-fluid surrogate, not free-streaming photons/neutrinos or
recombination microphysics. Both couple minimally to this same metric.
No particle-CDM component is inserted into the candidate.

The numerical coefficient functions are imported unchanged from
[constitutive.py](../nonlinear_evolution_2026/constitutive.py):

\[
 P=-\frac{U}{2}\log\frac{U-2dX}{U-2d\bar q^2}
       +3\gamma\bar q\bar H(X-\bar q^2),\quad V=U,
\]
\[
 W=U+2d\ell\big(\sqrt{1+Y/\ell}-1\big)-2\gamma\bar q^2\bar q'.
\]

Here \(U,d,\ell,\bar q,\bar H\) are already fixed functions of \(\tau\);
primes on barred functions mean derivatives with respect to \(\tau\).
Their earlier reconstruction is a limitation, not a first-principles
derivation. In particular, \(\bar H(\tau)\) is **not** replaced with the
new matter-containing physical \(H(t)\).

This action contains no established MOND \(a_0\) operator. Carl's global
\(a_0=\tfrac12c\sqrt{G\rho_\Lambda}\) remains an input to the broader
framework, not a derived result here. No local \(a_0\), newly fitted kernel,
or proof of \(\kappa=1/2\) is introduced.

## Variation, gauges, and sectors

Use background proper time \(N_{\rm bg}=1\), uniform-clock gauge
\(\delta\tau=0\), and solved physical clock rate \(s_0=\dot{\bar\tau}>0\),
**not fixed to one**. Equivalently, \(\tau=t\) coordinates have background
lapse \(1/s_0\). For \(k\ne0\), expand to second order in \(\epsilon\)
and average over one spatial period:

\[
\begin{split}
 N&=1+\epsilon\alpha\cos kx,\quad N^x=\epsilon b\sin kx,\\
 h_{xx}&=a^2e^{2\epsilon(z+2e)\cos kx},\quad
 h_{yy}=h_{zz}=a^2e^{2\epsilon(z-e)\cos kx},\\
 \chi&=\bar\chi+\epsilon\sigma\cos kx,\quad
 r=\bar r+\epsilon r_1\cos kx,\\
 \theta&=t+\epsilon\theta_1\cos kx,\quad
 \rho_b=\bar\rho_b+\epsilon\delta_b\cos kx.
\end{split}
\]

Longitudinal shear \(e\) is retained until variation.
[derive.py](derive.py) exports the quadratic density and all eight scalar
Euler equations for \(z,e,\sigma,r_1,\theta_1,\delta_b,\alpha,b\).
It expands the raw Einstein ADM curvature and cubic clock density,
not a phenomenologically assigned modified Poisson equation.
The cubic ADM integration-by-parts form is also checked by the existing
current/finite-wavelength tests listed in [COMMANDS.md](COMMANDS.md).

The true homogeneous *isotropic* calculation instead sets
\(\cos kx=1,\sin kx=0,e=\dot e=0\) before the spatial average.
Its quadratic normalization is twice the finite-period \(k\to0\) expression.
The shift constraint disappears at \(k=0\). No division by \(k\), no-slip
conclusion, or finite-\(k\) constraint count is carried into that sector.
Homogeneous anisotropy is outside this scalar-isotropic calculation.

## Independently derived clock stress and current

Evaluate unbarred derivatives of \(P,W,V\) at
\((X,Y,\tau)=(q^2,0,\bar\tau)\), with \(q=\dot{\bar\chi}\). Define

\[
 v=\delta Q=\dot\sigma-q\alpha,\quad
 {\cal L}=a^{-2}\Delta=-k^2/a^2,\quad
 \delta K=3\dot z-3H\alpha-kb,\quad
 B=2P_X+4q^2P_{XX},\quad d=W_Y(0,\tau).
\]
\[
 \rho=2q^2P_X-P+V-6\gamma Hq^3,\quad
 p=P-V+s_0W+2\gamma q^2\dot q,\quad
 j=2qP_X-6\gamma Hq^2.
\]

Varying lapse, shift and volume independently gives

\[
\boxed{
\begin{split}
 \delta\rho&=(qB-18\gamma Hq^2)v-2\gamma q^3\delta K
                    +2\gamma q^2{\cal L}\sigma,\\
 \delta p&=(2qP_X+4\gamma q\dot q)v+2\gamma q^2\dot v
                   -\alpha(s_0W+2\gamma q^2\dot q),\\
 \delta T^0{}_i&=\partial_i[m(t)\cos kx],\qquad m=-j\sigma-2\gamma q^2v.
\end{split}}
\]

All other perturbations below also denote Fourier amplitudes.
The code's momentum variable is \(-m\). The clock has zero linear
traceless stress on this homogeneous background. Independent covariant
stress variation and raw ADM variation agree exactly.
The clock and shift-current equations are

\[
 E_\tau=P_\tau-V_\tau-3HW,\qquad
 \delta E_\tau=2qP_{X\tau}v-W\delta K+2qd{\cal L}\sigma,
\]
\[
 D j=\dot j+3Hj,\qquad
 \delta j=(B-12\gamma Hq)v-2\gamma q^2\delta K+2\gamma q{\cal L}\sigma,
\]
\[
 \delta D j=\dot{\delta j}+3H\delta j+j\delta K-\alpha\dot j
 +[-2P_X+2s_0d+2\gamma(\dot q+3Hq)]{\cal L}\sigma
 -2\gamma q{\cal L}v.
\]

Here \(Dj\) names a current divergence, not a new field times \(j\).
The on-shell conditions are \(E_\tau=Dj=\delta E_\tau=\delta Dj=0\).
The \(\chi\), radiation and dust Euler equations independently match their
current-divergence expressions.

## Off-shell conservation — retaining both clock equations

These residuals reduce to exact symbolic zero without substituting a
chosen background history:

\[
\begin{split}
 \dot{\delta\rho}-\alpha\dot\rho
 +3H(\delta\rho+\delta p)+(\rho+p)\delta K+{\cal L}m
 &=q\,\delta Dj+v\,Dj-s_0\delta E_\tau+s_0\alpha E_\tau,\\
 \dot m+3Hm+(\rho+p)\alpha+\delta p&=-Dj\,\sigma .
\end{split}
\]

Dropping \(E_\tau\) while retaining only the \(\chi\) equation would not
establish energy conservation. Separately, with
\(E_f=(\sqrt{-g})^{-1}\delta S_m/\delta f\), diffeomorphism invariance
of the minimally coupled matter actions gives

\[
 \nabla^\mu T^m_{\mu\nu}
   =E_r\partial_\nu r+E_\theta\partial_\nu\theta
                         +E_{\rho_b}\partial_\nu\rho_b=0
\]

on the ordinary matter equations themselves. This is not merely conservation
of a phenomenological combined matter-plus-clock fluid.

## Two independently obtained potentials

The gauge-invariant metric potentials are

\[
 S=a^2(3\dot e/k^2-b/k),\qquad
 \Phi=\alpha+\dot S,\qquad \Psi=e-z-HS.
\]

The independently varied shear equation is

\[
 E_e=-M^2ak^2(\Phi-\Psi)=0.
\]

Thus \(\Phi=\Psi\) on this linear finite-\(k\), perfect-fluid branch.
Neither potential was assigned to the other. This does **not** compute
the galactic MOND branch or any PPN coefficient.
Free-streaming radiation has anisotropic stress and must be added explicitly;
this does not assert no slip for the full CMB hierarchy.

## What happens to the proposed Hubble acceleration?

The projected-gradient invariant gives, directly,

\[
 Y_{\rm bg}=0,\qquad Y^{(1)}=0,\qquad
 Y^{(2)}=\frac{k^2\sigma^2}{a^2}\sin^2 kx .
\]

There is no \(cH\) contribution in this invariant's argument even when
\(H\ne0\). This follows from the projector, not a phenomenological choice.
Expansion still enters other terms, including the cubic interaction,
the current, and fixed coefficient histories. Since this action has no
derived exponential MOND kernel, neither a \(\nu(cH/a_0)\) prescription
nor a guessed peculiar-field modified-Poisson prescription follows.

## Same-coefficient sourced homogeneous evolution

Write \(\rho_r=3C_rq_r^4\), \(q_r=\dot{\bar r}\). Initial data must satisfy

\[
 3M^2H^2-M^2\Lambda-\rho-\rho_b-\rho_r=0,\qquad E_\tau=0.
\]

Raychaudhuri, current conservation and preservation of \(E_\tau\) give
the computed matrix equation

\[
\boxed{
\begin{pmatrix}
 2M^2&2\gamma q^2&W\\
 -6\gamma q^2&B-12\gamma Hq&2qP_{X\tau}\\
 -3W&2qP_{X\tau}&P_{\tau\tau}-V_{\tau\tau}-3HW_\tau
\end{pmatrix}
\begin{pmatrix}\dot H\\\dot q\\s_0\end{pmatrix}
=
\begin{pmatrix}-qj-\rho_b-\tfrac43\rho_r\\-3Hj\\0\end{pmatrix}.}
\]
\[
 \dot a=aH,\qquad \dot{\bar\tau}=s_0,\qquad
 \dot\rho_b=-3H\rho_b,\qquad \dot\rho_r=-4H\rho_r.
\]

Friedmann preservation is checked symbolically, not imposed by resetting
the numerical constraint. The determinant is computed, never supplied as
an expected rank; its nonzero value is not a ghost/gradient-stability test.

[background_evolve.py](background_evolve.py) solves both initial constraints,
then evolves these equations with the old coefficient histories fixed.
Dimensionless choices are \(M^2=1,\Lambda=0.7,\gamma=10^{-6},a(0)=1,\tau(0)=0,
\rho_b(0)=0.001,\rho_r(0)=0.01\).
These are numerical initial conditions, not a cosmological parameter fit.
DOP853 relative/absolute tolerances are \(2\,10^{-11},2\,10^{-13}\).

| Quantity | \(t=0\) | \(t=0.02\) |
|---|---:|---:|
| \(a\) | 1 | 1.0104251304 |
| \(H\) | 0.5191118192 | 0.5180104810 |
| \(q\) | 0.9078321506 | 0.9069972677 |
| \(\tau\) | 0 | 0.0206264636 |
| \(s_0\) | 1.0317810693 | 1.0308700298 |
| matrix determinant | −0.0231174593 | −0.0214716418 |
| matrix condition number | 413.44 | 411.53 |
| logarithm margin \(U-2dq^2\) | 0.0008493170 | 0.0008376129 |

Seventeen samples have maximum Friedmann residual \(9.02\,10^{-16}\),
clock residual \(3.47\,10^{-17}\), relative baryon charge drift
\(4.44\,10^{-16}\), radiation charge drift \(6.66\,10^{-16}\), and
\(\chi\)-charge drift \(8.55\,10^{-15}\).
These float64 residuals are numerical evidence, not rigorous error bounds
on an entire interval. This short late-epoch history is not an early-universe
extension, perturbation stability test or galaxy result.

## GR control and Lean scope

A subsequent [Lean constraint-identity certificate](CONSTRAINT_PROOF.md)
formalizes the finite-k reduction's exact real-jet algebra and its zero-mode
exception. It is not a CMB, MOND or whole-theory proof.

The stock classy v3.3.4 installation in Python 3.13.9 runs the separate
Einstein–Lambda–baryon–CDM–radiation comparator: three raw-TT smoothed
peak positions \(221,537,816\), peak ratios 0.45414682 and 0.99180775,
and \(\sigma_8=0.82277553\). CDM belongs only to this labelled comparator.
This verifies the reference solver's availability, not GR recovery of
the clock action, a likelihood fit, or a clock-to-CLASS implementation.
Setting \(\gamma=0\) leaves \(P,W,V\); it does not remove the clock.

[MetricWard.lean](MetricWard.lean) compiles two **conditional algebra**
implications: nonzero \(M^2,a,k\) plus the shear equation imply no slip;
the off-shell energy identity plus both clock equations imply conservation.
Printed dependencies contain only propext, Classical.choice and Quot.sound.
The variation, gauge mapping, PDE existence, stability and empirical
validity are not formalized by these leaves. No sorry, new physical axiom,
or full-theory certificate is used.

## Gate decision and next unavoidable calculation

**OPEN.** This checkpoint passes the finite-\(k\) scalar action/stress/Ward
identities, a short sourced background test, and a separate GR control.
It neither establishes nor falsifies a full MOND theory.

The next executable calculation is the finite-\(k\) transfer system in
[FIRST_ORDER_HANDOFF.md](FIRST_ORDER_HANDOFF.md), on this sourced background.
It must reproduce every eliminated Euler equation and conserved constraint,
including the lapse equation, with time-dependent coefficients. Do not
reconstruct coefficient functions in response to a failed transfer test.

Then the fixed functions must possess an admissible early-time extension,
and the same stress equations must be coupled to the full photon/baryon/
neutrino hierarchy and compared with the stock reference. Until then there
is no clock CMB result. MOND construction, nonlinear two-tensor-plus-healthy-
matter counting, caustic/strong-coupling control, galactic lensing, PPN,
dust depletion and radial convergence remain separate open gates.

The Mathbox computation-audit and independent proof-audit workflow shaped
this checkpoint: separate derivations, explicit domains, hashed inputs,
retained failures/limits, and a concrete dependency-aware handoff.
