# CD26-2: a covariant amplitude–phase completion and its field cost

**Constructive result:** a canonical complex classical scalar, written as an
amplitude and a phase, gives an explicit generally covariant completion of the
previous healthy gyroscopic system. It uses one physical metric and has two
scalar canonical pairs. Nonzero phase charge provides a rigorous, globally
timelike, node-free homogeneous FRW branch under finite homogeneous changes
of initial data. Neither field counting nor the global branch proves a MOND
embedding or satisfies a requirement forbidding an independent matter sector.

This is a separate candidate action. No original specification is relaxed,
no cosmological abundance is imposed, and kappa remains an allowed input.

**Scope reconciliation:** during this checkpoint, external commit
`9092fc0fd02b904e87c708971335cd63adb18151` recorded the author's amended target:
the filtered nu_mono law and causality criterion B. The metric-cone completion
here is a sufficient local causal property, not a newly imposed acceptance
criterion. Historical AQUAL matching is not claimed to satisfy the amended
target. The independent matter data, clock-domain bounds, and common-action
source obligations survive that change of target.

## 1. The covariant action and what is being added

Use signature (-,+,+,+), c=hbar=1, and Mpl^2=(8pi G)^-1:

\[
S=\int\sqrt{-g}\,d^4x\left[
\frac{M_{\rm Pl}^2}{2}\mathcal R-\rho_\Lambda
-\frac12\nabla_\mu R\nabla^\mu R
-\frac12R^2\nabla_\mu T\nabla^\mu T-V(R)\right]+S_b[g,\Psi_b].
\]

There is one metric, including for ordinary matter in S_b. R is an amplitude
with mass dimension one, T is dimensionless, and rhoLambda has dimension four.
For a literal constant vacuum term, rhoLambda=Mpl^2 Lambda. In a node-free
patch this is the Cartesian two-scalar theory
phi1=R cos T, phi2=R sin T; their kinetic terms are canonical. Quantization,
particle states, thermal production, and a relic abundance are not assumed.
The phase can instead be lifted to a real variable on a chosen branch.

The matter equations and stress tensor are

\[
\Box R-R(\nabla T)^2-V'(R)=0,\qquad
\nabla_\mu(R^2\nabla^\mu T)=0,
\]
\[
T_{\mu\nu}=\nabla_\mu R\nabla_\nu R+
R^2\nabla_\mu T\nabla_\nu T
-g_{\mu\nu}\left[\frac12(\nabla R)^2+
\frac12R^2(\nabla T)^2+V+\rho_\Lambda\right].
\]

Taking the future-oriented current to be
\(j^\mu=-R^2\nabla^\mu T\) makes j^0=R^2 Tdot in cosmic time.
Its sign is a convention; conservation and the independent charge are not.

The action has a constant phase-shift symmetry. It does **not** have the
arbitrary monotone clock relabeling T -> F(T) of a pure foliation label.
Identifying T with an existing khronon therefore requires this additional
physical rate structure to be declared. R is an independently dynamical
amplitude; calling it the clock's modulus does not eliminate its initial data.

## 2. Canonical count and local causal health

In ADM variables, put
\(v_R=\dot R-N^iD_iR\), \(v_T=\dot T-N^iD_iT\).
The scalar velocity Hessian is

\[
\frac{\sqrt h}{N}\begin{pmatrix}1&0\\0&R^2\end{pmatrix},
\qquad \det=\frac{hR^2}{N^2}>0\quad(R>0,N>0).
\]

The scalar part of the Hamiltonian constraint is

\[
\mathcal H_m=\frac{p_R^2+p_T^2/R^2}{2\sqrt h}
+\sqrt h\left[\frac12(DR)^2+\frac12R^2(DT)^2+V+\rho_\Lambda\right],
\qquad \mathcal H_i^m=p_RD_iR+p_TD_iT.
\]

It has nonnegative matter energy if V+rhoLambda>=0. This is not a claim
that the unconstrained gravitational Hamiltonian density is positive.
Six spatial-metric configurations plus R,T give eight canonical pairs;
the four diffeomorphism constraints are first class and remove four pairs.
The regular theory therefore has four physical configurations: two tensor
polarizations and **two scalar modes**. Lapse and shift are multipliers.
Choosing T as the time coordinate transfers a scalar mode to the metric; it
does not remove that physical pair. At R=0 the polar coordinates fail, but
Cartesian fields remain regular and still have two scalar pairs.

The Cartesian scalar equations have principal operator g^{mu nu} partial_mu
partial_nu on each field. Together with the Einstein equations in a
hyperbolic coordinate gauge, the principal propagation cone is that of this
same metric; the potential and amplitude–phase mixing contain no extra
highest derivatives. This states the local characteristic and kinetic health
of the minimal Einstein–scalar system, not stability against every long-wave
gravitational or background-dependent instability.

## 3. Recovering the gyroscopic action, including all factors

On a prescribed Minkowski metric, a circular matter solution is
R=R0>0, T=Omega t, with

\[
V'(R_0)=R_0\Omega^2,\quad
\chi=\delta R,\quad z=R_0\delta T,\quad
\mu^2=V''(R_0)-\Omega^2.
\]

Dropping the first-order total derivative R0 Omega zdot, direct expansion gives

\[
\mathcal L_2=\frac12[\dot z^2-|\nabla z|^2+
\dot\chi^2-|\nabla\chi|^2-\mu^2\chi^2]+2\Omega\chi\dot z.
\]

Thus the previous g is **2 Omega**, and its m^2 is mu^2. For mu^2>0,

\[
\mathcal H_2=\frac12[(p_z-2\Omega\chi)^2+p_\chi^2+
|\nabla z|^2+|\nabla\chi|^2+\mu^2\chi^2]\ge0.
\]

Writing A=mu^2+4 Omega^2,

\[
(\omega^2-k^2)(\omega^2-k^2-\mu^2)-4\Omega^2\omega^2=0,
\]
\[
\omega_\pm^2=k^2+\frac A2\pm\frac12\sqrt{A^2+16\Omega^2 k^2},
\qquad
\omega_-^2=\frac{\mu^2}{A}k^2+
\frac{16\Omega^4}{A^3}k^4+O(k^6).
\]

The roots have positive sum and product k^2(k^2+mu^2)>0 for k!=0.
The high-frequency theory retains its metric cone; it is the complete local
two-field system, not a fundamental k^4 truncation. The quadratic energy
flux is -zdot grad z-chidot grad chi. Its magnitude normal to a surface is
at most the positive quadratic energy density, giving the same unit-cone
energy estimate as the prior gyroscopic completion.

An explicit bounded-below potential is

\[
V(R)=\frac12m_0^2R^2+\frac\lambda4R^4,\qquad m_0^2\ge0,\quad\lambda>0.
\]

It gives Omega^2=m0^2+lambda R0^2, mu^2=2 lambda R0^2 and

\[
c_s^2=\frac{\lambda R_0^2}{2m_0^2+3\lambda R_0^2},\qquad
d_4=\frac{16(m_0^2+\lambda R_0^2)^2}
{(4m_0^2+6\lambda R_0^2)^3}>0.
\]

This positive-mass quartic family only realizes 0<cs^2<=1/3. The general
gyroscopic mapping realizes any 0<cs^2<1 by an appropriate V'' and Omega;
a symmetry-broken quartic with a negative quadratic coefficient, a positive
quartic coefficient, and a constant chosen to bound V below also reaches
1/3<cs^2<1 on its rotating branch. That is a different declared potential,
not a property of the positive-mass example. No potential parameters here
have been fitted or derived from the Zimmerman action.

The circular solution is an exact matter solution on prescribed Minkowski
space. A positive condensate is not an exact Minkowski solution of the full
Einstein equations: rho+p=R0^2 Omega^2>0 cannot be removed by a constant
vacuum counterterm. On a slowly evolving FRW background these coefficients
can be used as a local frozen-background approximation; the next section
gives the actual homogeneous equations instead of silently imposing a circle.

## 4. Homogeneous Einstein evolution and an exact global clock branch

For the flat FRW metric ds^2=-dt^2+a(t)^2 dx^2, with no additional S_b
background source for this construction,

\[
\ddot R+3H\dot R-R\dot T^2+V'=0,\qquad
J=a^3R^2\dot T=\text{constant},
\]
\[
\rho=\frac12\dot R^2+\frac{J^2}{2a^6R^2}+V+\rho_\Lambda,
\quad p=\frac12\dot R^2+\frac{J^2}{2a^6R^2}-V-\rho_\Lambda,
\]
\[
3M_{\rm Pl}^2H^2=\rho,\qquad
\dot H=-\frac{\dot R^2+J^2/(a^6R^2)}{2M_{\rm Pl}^2}.
\]

In particular, a constant nonzero R and Tdot is incompatible with H!=0:
charge conservation would require 3HJ=0. For general homogeneous histories,
the fixed-metric quadratic scalar action in chi=delta R, pi=delta T is

\[
\frac{\mathcal L_2}{a^3}=\frac12[\dot\chi^2-a^{-2}|\nabla\chi|^2]
+\frac12R^2[\dot\pi^2-a^{-2}|\nabla\pi|^2]
+2R\dot T\chi\dot\pi-\frac12(V''-\dot T^2)\chi^2.
\]

This displays positive kinetic and gradient blocks for R>0. Lapse and shift
constraints must still be included for full finite-wavelength gravitational
perturbations; the ADM count above already includes their gauge reduction.
The local mass term need not stay positive along every radial oscillation,
so global clock existence below is not an all-perturbations stability theorem.

Here is a nonlinear global result that does include homogeneous backreaction.
Choose the positive-mass quartic V above, rhoLambda>=0, expanding H0>0,
a0>0, R0>0, finite radial velocity, and any nonzero J. Define
E=rho-rhoLambda and E0=E(0)>0. Directly from the equations,

\[
\dot E=-3H(\dot R^2+J^2/(a^6R^2))\le0,\qquad
0<H\le H_0,\qquad a_0\le a(t)\le a_0 e^{H_0t}.
\]

Positivity of each contribution to E then gives, for every finite t>=0,

\[
\boxed{\frac{|J|}{a(t)^3\sqrt{2E_0}}\le R(t)\le
R_{\max}:=\left(\frac{4E_0}{\lambda}\right)^{1/4}},
\]
\[
\boxed{|\dot T(t)|=\frac{|J|}{a(t)^3R(t)^2}\ge
\frac{|J|}{a_0^3e^{3H_0t}R_{\max}^2}>0.}
\]

These bounds prevent a node or a finite-time coefficient singularity. The
Cartesian field and its velocities are bounded by the coercive energy; a and
H are bounded on every finite interval. The smooth homogeneous ODE therefore
extends for all finite future cosmic times. The lifted phase has a fixed sign
of Tdot and a timelike gradient throughout. This is an open family in
homogeneous initial-data space, not just the exactly circular trajectory.
It permits finite radial and phase-rate changes as long as J remains nonzero.
There is no uniform lower radius bound as t tends to infinity in this proof.

The numerical controls evolve the two Cartesian fields and their velocities,
with H determined by the Friedmann equation, so conservation of J is an
independent check rather than an identity hard-coded into the evolution.
Three finite initial-data choices were integrated through t=40; all conserved
J to less than 1.0e-12 relative error and respected the displayed bounds.
The smallest observed radius was 4.44e-4, with positive phase rate throughout.
These finite outputs check the implementation; the global conclusion uses
the analytic coercive bounds above.

## 5. A uniform nonlinear timelike family and the spatial limitation

On a prescribed Minkowski metric the interacting homogeneous equations have
constant charge j=R^2 Tdot and energy

\[
E=\frac12\dot R^2+\frac{j^2}{2R^2}+\frac12m_0^2R^2+
\frac\lambda4R^4.
\]

For any j!=0 and finite E, the same argument now yields uniform bounds

\[
R\ge\frac{|j|}{\sqrt{2E}}>0,\quad
R\le(4E/\lambda)^{1/4},\quad
|\dot T|\ge|j|\sqrt{\lambda/(4E)}>0
\]

for all positive and negative times. These are finite-amplitude interacting
radial oscillations, not a free-wave superposition. Lorentz boosting the
entire solution via tau=gamma(t-vx) gives an exact, spatially varying matter
solution with -(partial T)^2=(dT/dtau)^2>0 and the same node-free bound.
The family has finite energy density, not finite total energy on infinite
space, and its Minkowski metric is prescribed rather than self-consistently
sourced. The FRW family above addresses homogeneous Einstein backreaction.

For the concrete Minkowski data m0^2=1, lambda=.5, j=1.2, R(0)=1.1,
Rdot(0)=.4, the proven bounds are R>=.70151 and Tdot>=.35076. An integration
through t=50 has relative energy error 5.01e-13 and remains well inside them.

No result here makes the clock condition invariant for arbitrary spatial
perturbations. R>0 and -grad(T)^2>0 are local open C1 conditions, and smooth
local evolution preserves strict margins for a short time by continuity.
They do not follow from positive total charge or small energy alone. In
three spatial dimensions, a smooth radial dip of size R0 on a ball of radius
epsilon costs gradient energy O(R0^2 epsilon) and potential energy
O(epsilon^3); its central radius can be arbitrarily close to zero. A localized
phase bump likewise can have a spatial gradient exceeding Tdot while its
energy cost tends to zero as its support shrinks. These initial-data examples
rule out an energy-only lower-margin argument; they are not a proof that
initially timelike arbitrary perturbations must later fail.

A literal complex phase also needs a real lift to define a global clock.
Node-free data with nonzero winding on spatial loops do not admit that lift.
The homogeneous and boosted simply connected constructions above use the
zero-winding lifted branch explicitly. General topology, defects, and a
nonlinear inhomogeneous invariant-region theorem remain separate obligations.

## 6. Vacuum stress and independent matter data

A constant rhoLambda contributes precisely -rhoLambda g_mu_nu, with
pLambda=-rhoLambda. In the Einstein sector it can source accelerated
expansion when the total rho+3p is negative. It changes H and thus the
friction in the scalar equations, but supplies no radial force, no phase
current, and no value of the integration constant J. The branch J=0 remains
J=0 for any rhoLambda. Positive vacuum density cannot replace a clustering
charge mode: it has no independent density perturbation or rho+p contribution.

For a circular positive-mass quartic state,

\[
\rho=m_0^2R_0^2+\frac34\lambda R_0^4+\rho_\Lambda,
\qquad p=\frac14\lambda R_0^4-\rho_\Lambda.
\]

Without rhoLambda its pressure is nonnegative. In the dilute adiabatically
rotating regime m0>0, rho-rhoLambda is approximately m0 |J|/a^3. That is a
classical matter-like density with a freely specified amplitude and charge;
the approximation requires rotation fast enough for the radial tracking
assumption, not just the algebraic circular formula. It can play the role of
dark matter phenomenologically even if no particles are assumed. It therefore
cannot be counted as satisfying a stricter no-independent-dark-sector
requirement merely by renaming R a clock amplitude. No abundance was chosen
to match LCDM or observational density fractions in these calculations.

An exact diagnostic distinguishes vacuum support from spinning negative
pressure. For the circular monomial V=gamma R^p with gamma,p>0 and no added
constant,

\[
w=\frac{p-2}{p+2}=c_s^2,\quad
\mu^2=(p-2)\Omega^2.
\]

Thus the negative-pressure circular range 0<p<2 has a long-wavelength
gradient instability in this matter-sector calculation. For p=1/2,
cs^2=-3/5 exactly. Adding a genuinely independent constant vacuum term can
make the total pressure negative without forcing this unstable stiffness;
it does not predict that constant, the phase charge, or the MOND scale.

## 7. Can the amplitude be only the existing clock rate?

Let X=-(partial T)^2. Dropping the radial kinetic term and solving its
algebraic equation for the quartic potential gives, on X>m0^2,

\[
R_*^2(X)=\frac{X-m_0^2}{\lambda},\qquad
P(X)=\frac{(X-m_0^2)^2}{4\lambda}-\rho_\Lambda.
\]

This is a genuine one-scalar first-derivative theory with healthy timelike
kinetic coefficients on that branch. Its sound speed
P_X/(P_X+2X P_XX) agrees with the circular low-k coefficient, but its
constant-background dispersion has no independent positive k^4 term.

Retaining the original radial kinetic term while substituting R=R_*(X)
instead produces

\[
-\frac12(\partial R_*)^2=-\frac{(\partial X)^2}
{8\lambda(X-m_0^2)}.
\]

Around T=Omega t+pi this includes
Omega^2 pi_ddot^2/[2 lambda(Omega^2-m0^2)], with nonzero acceleration
Hessian. Taken as a standalone flat-space higher-derivative theory it adds
an extra pair rather than removing the amplitude mode. As a derivative
expansion obtained by integrating out a healthy radial field it must be
used perturbatively, with omitted radial initial excitations specified and
derivatives small compared with the radial response scale; it is not a new
fundamental one-clock causal completion. A specifically degenerate covariant
constraint construction would require a separate proof.

The minimal unresolved bridge is consequently concrete: either identify and
justify this second canonical amplitude within the original action and its
allowed matter content, or exhibit a different constraint structure that
keeps one scalar pair while reproducing the required dispersion and static
MOND response. This report provides neither identification by fiat.

## 8. Known-theory comparison, bounded evidence, and next implication

The amplitude–phase route is established scalar-field physics, not a new
fundamental theory. Boyle, Caldwell and Kamionkowski,
[Spintessence!, arXiv:astro-ph/0105318v2](https://arxiv.org/abs/astro-ph/0105318v2)
(17 September 2002), give the circular condition R Omega^2=V'(R), conserved
FRW charge, and homogeneous density and pressure in their discussion and
equations (1)–(3). Their R and Theta map to this R and T. The primary PDF was
checked for those statements; no validation of its full phenomenology or
global novelty claim is made. The action calculations and global bounds here
were derived directly, independently of that comparison.

`check_clock.py`, `contract.json`, and `run1/` contain **30 passing checks**:
28 exact symbolic identities/control calculations and two grouped finite ODE
checks. Python 3.9.6, SymPy 1.14.0, NumPy 1.26.2, SciPy 1.11.4; runtime
1.629204 s, 90 s wall cap, 75 s CPU cap, one cooperative numerical-library
thread. The manifest validator accepted current source and output hashes.
The assigned base was `c8bb508131a7cc72d0cfbb0313c5b79db7189ed2`; an external
task advanced HEAD to `3151d88f29f751df4f599d489f8dac1cbbb77774` during work,
which is the dirty revision pinned by the run. This task made no commit or
merge and wrote only its new `covariant_clock/` artifacts.

Regenerate into a fresh output directory using the computation-audit bounded
runner and this child command; the manifest records the complete invocation:

```text
python3 real_research/closure_push_2026_09_26/covariant_clock/check_clock.py --output NEW_RUN_DIRECTORY/results.json
```

The next necessary calculation is a same-action MOND and metric-response
embedding with the declared two-pair count, or an explicitly different
one-pair constraint construction. Healthy canonical matter, a causal local
cone, and a controlled homogeneous clock branch do not establish the original
13-condition theory, its empirical gates, or its no-dark-matter interpretation.
