# Gravitational strain pressure in X48

Date: 2026-10-31. Scope: the exact proposed constitutive law, its Newtonian
fluid equations, and bounded constitutive diagnostics. This is a separate
experimental model under X48. Historical X48 remains the frozen collisionless
dust plus background Lambda experiment.

**Primary audit verdict: refuted, with an explicit counterexample, for the
claimed fixed pressure cap and compulsory regular-core endpoint.** Suppression
of cusp formation from regular initial data and halting of adiabatic
contraction remain unestablished dynamical claims. The pressure law itself
is well defined. It is outside
the displayed premises of the project's Matching Theorem when introduced as
an independent gradient-dependent response. These are different conclusions.

## Constitutive law and dynamical assumptions

Write

\[
 A=\nabla\Phi_{\rm tot},\quad g=|A|,\quad
 S=\frac{g^2}{8\pi G},\quad S_0=\frac{a_0^2}{8\pi G},\qquad
 P_c=(S-S_0)_+ .
\]

The requested law is retained exactly, with no saturation, density threshold,
or smoothing. Its argument is an acceleration magnitude, rather than a strain
tensor. It is non-barotropic: two regions with the same cold-component density
can have different pressures because their gravitational fields differ.

A minimal phenomenological Newtonian model assumes a conserved, clustered
cold component with positive inertial mass-equivalent density \(\rho_c\):

\[
 \partial_t\rho_c+\nabla\cdot(\rho_c v_c)=0,\qquad
 (\partial_t+v_c\cdot\nabla)v_c
 =-\nabla\Phi_{\rm tot}-\frac{\nabla P_c}{\rho_c}.
\]

For isolated Newtonian matter sources plus the X48 background Lambda term,

\[
 \nabla^2\Phi_{\rm tot}=4\pi G(\rho_c+\rho_b+\rho_{\rm other})
                         -3\Omega_\Lambda H_0^2 .
\]

Here the baryonic density and its evolution or prescribed potential must be
supplied to model a disc. X48 itself contains no baryonic disc. The clustered
cold component is not being identified with a homogeneous vacuum: a component
with exactly \(p=-\epsilon\) does not have the positive Newtonian inertia
assumed by these Euler equations. A relativistic completion, an energy
equation, and reciprocal field stresses are not fixed by the proposed scalar
pressure. Adding this response to a field action would require deriving the
resulting gravitational equation and stress rather than assuming them.

On either open branch the exact pressure acceleration is

\[
 a_P=-\frac{\Theta(g^2-a_0^2)}{4\pi G\rho_c}
                 (\nabla\nabla\Phi_{\rm tot})A .
\]

Pressure is continuous at the activation surface. Its derivative need not be:
the formula above is an almost-everywhere relation. The evaluator assigns the
inactive value exactly at equality; this is a numerical convention, not a
classical derivative there. There is no delta-function surface force from
differentiating this continuous positive-part pressure.

## Cosmological field convention and forest scope

The model must specify the frame and which gravitational field is used. In a
preferred cosmological frame with \(A=0\) on homogeneous FRW, every region with
a strict margin \(g<a_0\) has \(P_c=\delta P_c=0\) for sufficiently small
perturbations. There is no linear pressure term about that background.

Linear density contrast alone does not establish that margin. In a Newtonian
plane wave,

\[
 \delta\rho=\bar\rho\,\varepsilon\cos(kx)
 \quad\Longrightarrow\quad
 g_{\rm max}=4\pi G\bar\rho\,|\varepsilon|/k .
\]

Thus \(|\varepsilon|\ll1\) does not imply \(g\ll a_0\) at every wavelength.
Long modes, external fields, and the selected frame affect activation. Forest
viability requires the actual total field distribution and evolution, not
only the zero-pressure linearization.

The local source [Matching Theorem, section 3](../../../opus_48_extended_research/papers/THE_MATCHING_THEOREM.md)
is the author manuscript dated 2026-09-02, lines 81--100. Its H1--H4 relate
charge, lapse, and a sound speed determined by the clock variable alone.
An independently specified \(P_c(|\nabla\Phi|)\) breaks the response-matching
step: equal density or clock variable need not imply equal pressure response.
**Scope verdict: inapplicable to this independently postulated closure.**
This checks the displayed hypotheses and their application; it does not audit
the theorem's proof or authenticate the manuscript's claimed published DOI.

X48's `accel` is a physical isolated-sphere acceleration including homogeneous
matter attraction and \(+\Omega_\Lambda H_0^2x\). Its magnitude is not an
FRW-zero peculiar field. One possible declared peculiar-field convention is

\[
 a_{\rm pec}=a_{\rm X48}-\Omega_\Lambda H_0^2x
                 +\frac{4\pi G\bar\rho_m(t)}3x,
\]

with baryon and external contributions added explicitly. Using this as the
pressure key is a model choice; it changes the literal physical-total-field
reading. The constitutive evaluator takes the supplied gradient unchanged
and performs no hidden background or external-field subtraction.

## Stress scale and force direction

Activation occurs at \(g=a_0\), where \(P_c=0\).
\(P_c=S_0\) occurs at \(g=\sqrt2\,a_0\), and pressure is unbounded as \(g\)
increases. With the project's fitted relation
\(a_0=\kappa c\sqrt{G\rho_{\rm DE}}\), where \(\rho_{\rm DE}\) is a
mass-equivalent density, this scale is
\(S_0=\kappa^2\rho_{\rm DE}c^2/(8\pi)=\rho_{\rm DE}c^2/(32\pi)\)
at \(\kappa=1/2\). It is not equal to the magnitude
\(\rho_{\rm DE}c^2\) of a homogeneous vacuum's negative pressure.
The algebraic identity

\[
 S-P_c=\min(S,S_0)
\]

caps a scalar difference; it is not a cap on pressure or on the gravitational
stress tensor. For example, with the Newtonian momentum-flux convention

\[
 T_g=\frac{A\otimes A-\tfrac12g^2I}{4\pi G},\qquad
 \nabla\cdot T_g=\rho_c\nabla\Phi
\]

in the cold-only Poisson case, the active eigenvalues of \(T_g+P_cI\) are
\(2S-S_0,-S_0,-S_0\). The longitudinal stress is unbounded.

In a spherical attractive well, \(g=\Phi'(r)>0\), and outward-positive radial
pressure acceleration is

\[
 a_{P,r}=-\Theta(g-a_0)\frac{g g'}{4\pi G\rho_c} .
\]

An outward-increasing field gives an inward pressure force; a constant field
gives zero force even when pressure is large. For a self-gravitating power law
\(\rho_c=B r^{-\gamma}\), \(0\le\gamma<3\), with no central point mass,
external sources, or Lambda term, Poisson gives

\[
 g=\frac{4\pi GB}{3-\gamma}r^{1-\gamma},\qquad
 \frac{a_{P,r}}g=\frac{\gamma-1}{3-\gamma}
 \quad (g>a_0).
\]

| Profile in its active region | Pressure force | Consequence |
|---|---|---|
| Constant density, \(\gamma=0\) | \(a_{P,r}=-g/3\) | It reinforces inward gravity locally. |
| \(1/r\) cusp, \(\gamma=1\) | \(a_{P,r}=0\) | A nonzero pressure supplies no support. |
| \(1/r^2\) cusp, \(\gamma=2\) | \(a_{P,r}=+g\) | A singular hydrostatic profile is allowed. |

A regular isolated spherical core has \(g\propto r\to0\), hence an inactive
central neighborhood. A collapsing homogeneous sphere with \(v=-Hr\),
\(H>0\), has inward pressure force in its active annulus, so activation does
not itself stop collapse.

For the NFW form, with \(x=r/r_s\),

\[
 \rho_c=\frac{\rho_s}{x(1+x)^2},\quad
 g=4\pi G\rho_sr_s\frac{\ln(1+x)-x/(1+x)}{x^2}
   =g_0\left(1-\frac43x+O(x^2)\right),\quad
 g_0=2\pi G\rho_sr_s .
\]

If \(g_0>a_0\), \(a_{P,r}/g=2x/3+O(x^2)\to0\). If \(g_0\le a_0\), a
central neighborhood is inactive. The pressure law supplies no leading-order
support against the NFW central cusp in either case. This is an asymptotic
force calculation, not an evolved NFW formation experiment.

More strongly, exact active hydrostatics for a cold-only spherical source
requires \(g'=-4\pi G\rho_c\). Combining with Poisson gives

\[
 g=C/r,\qquad \rho_c=C/(4\pi Gr^2),\qquad
 P_c=\frac{C^2/r^2-a_0^2}{8\pi G},\quad 0<r<C/a_0,
\]

for any \(C>0\). It remains singular at the origin and has unbounded central
pressure. It can be truncated where pressure vanishes and matched to vacuum
with continuous gravitational field. This counterexample refutes a universal
core or finite-stress endpoint; it does not prove that every initial condition
evolves toward this profile.

## Disc response and remaining dynamical question

For a stationary axisymmetric circular cold flow, radial balance is

\[
 \frac{v_{\phi,c}^2}{R}=\partial_R\Phi_{\rm tot}
                        +\frac{1}{\rho_c}\partial_RP_c,
 \qquad \partial_zP_c=-\rho_c\partial_z\Phi_{\rm tot} .
\]

The pressure has no direct force on baryons in the stated model; baryons feel
the changed gravitational field. A settling-disc calculation needs a baryon
potential or baryon dynamics, cold angular momentum, boundary data, and
time evolution. The threshold \(g>a_0\) imposes none of these balances and
therefore does not establish a halt to adiabatic contraction.

## Active branch stability before collapse integration

The bare instantaneous Euler closure also has a short-wavelength problem.
Consider an interior active interval of the exact spherical hydrostatic
solution above. For a radial displacement \(\xi(r,t)\), Eulerian perturbations
with no independent central point-mass perturbation obey

\[
 \delta\rho_c=-\frac1{r^2}\partial_r(r^2\rho_c\xi)=-\rho_c\xi',
 \qquad \delta g=-4\pi G\rho_c\xi=-\frac gr\xi,
 \qquad \delta P_c=\frac{g\delta g}{4\pi G}=-\rho_c g\xi .
\]

Linearizing the radial Euler equation, including the variation of the density
in the pressure-force denominator, gives

\[
 \xi_{tt}=-\delta g-\frac{\partial_r\delta P_c}{\rho_c}
                    +\frac{P_c'}{\rho_c^2}\delta\rho_c
            =2g\xi'-\frac{2g}{r}\xi .
\]

Freezing coefficients locally and taking \(\xi\propto e^{\lambda t+ikr}\)
yields \(\lambda^2=2igk-2g/r\) and
\(\operatorname{Re}\lambda\sim\sqrt{g|k|}\) as \(|k|\to\infty\) for the
growing branch. Thus the unregularized active fluid has unbounded local
short-wavelength growth. This is an interior principal-symbol analysis, not
a global normal-mode spectrum or a stability assertion about a completed
field theory. Ordinary pressure, viscosity, dispersion, or a finite response
length would change the model and must be specified and checked separately.
Plummer softening or a finite grid can conceal this limit by adding a
numerical cutoff; an apparent finite-resolution core would not establish
convergence to the proposed continuum equations. This obstruction must be
resolved before interpreting collapse time integration as a physical test.

## Executable scope and units

`strain_model.py` evaluates the exact scalar pressure and its pressure force
from a supplied potential gradient, Hessian, and positive cold density. It
also evaluates the radial formula. This is a constitutive model and finite
diagnostic, not a replacement particle force, fluid time integrator, or
production collapse result. X48 particles are collisionless samples; adding
pressure requires a density representation and fluid discretization.

All quantities must use consistent units. In X48 these are Mpc, km/s, and
solar masses, with \(G=4.30091\times10^{-9}\) Mpc (km/s)\(^2\)/solar mass.
Acceleration is (km/s)\(^2\)/Mpc, and pressure is
solar masses (km/s)\(^2\)/Mpc\(^3\). Convert an SI acceleration by multiplying
by \(3.085677581491367\times10^{16}\). The two existing acceleration footings
remain distinct; the executable diagnostics use explicitly normalized
\(G=a_0=1\) and do not fit either footing.

Run the constitutive checks from the repository root:

```bash
python3 -m unittest discover -s rebuild_2026_10_22/X48_native_cf_zoom/gravitational_strain -p 'test_*.py' -v
python3 rebuild_2026_10_22/X48_native_cf_zoom/gravitational_strain/strain_model.py
```

The checks cover activation, the pressure scale, force sign, the two singular
power laws, and differentiation away from the threshold. Their finite range
does not measure Lyman-alpha power, formation concentration, nonlinear halo
evolution, disc contraction, or a relativistic dark-energy stress.

`contract.json` fixes the finite computation and its non-claims. The bounded
run in `verification_2026_10_31/` stores the emitted diagnostics, test logs,
source hashes, software versions, and resource limits in a v2 manifest. The
regeneration command and observed result are recorded in `VERIFICATION.md`.

## Obligation status

| Obligation | Status | Evidence or remaining input |
|---|---|---|
| Exact pressure and Euler pressure force | Passed on smooth open branches | Differentiation above; constitutive diagnostics. |
| Zero pressure in a subthreshold forest region | Conditional | Requires a strict field margin in the declared frame. |
| Applicability of density or clock matching | Inapplicable | Independent gradient response lacks the displayed matching premise. |
| Fixed pressure cap at \(S_0\) | Failed | \(P_c/S_0=(g^2/a_0^2-1)_+\) is unbounded. |
| Compulsory regular-core hydrostatic endpoint | Failed | Exact singular hydrostatic family above. |
| Suppression of cusp formation from regular initial data | Incomplete | NFW force asymptote alone does not establish an evolutionary result. |
| Halt of baryon-driven contraction | Incomplete | Missing coupled evolution and force balance; activation alone is insufficient. |
| Bounded short-wavelength growth of the bare active Euler fluid | Failed | Radial displacement equation above has growing rate proportional to \(\sqrt{|k|}\). |
| Covariant stress and energy closure | Not addressed | A scalar constitutive law alone does not supply an action. |

Standing X48 qualifications remain: kappa = 1/2 FITTED; cold dark energy is
not matter; footings are not pooled; not theory closed. These diagnostics
make no claim that data favor the framework.
