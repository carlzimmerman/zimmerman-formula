# A shared phase–pool–baryon interaction: explicit construction and limits

2026-11-07. Base e9ee97959a2b00de3f14e5663ec6225b6fdd8c1e.

**The requested 1/2 remains underived.** A repulsive complex scalar gives an
actual pressure law and can be trapped by a phase-dependent mass. Coupling it
to baryonic charge gives a candidate inventory mechanism, but also a force that
cannot be discarded. Even granting inventory proportional to baryonic mass,
the conditional phase-confined condensate family has the wrong universal
edge-speed scaling. An explicit coupling-identifying symmetry loses the wall.
These results concern the constructions below, not every possible pool theory.

## 1. An interaction rather than an imposed pressure

In natural units and signature (+---), consider the exploratory action density

    L = (partial phi)^2/2 + |D chi|^2 - U(phi)
        - m_chi(phi)^2 |chi|^2 - lambda_chi |chi|^4/2
        - F_mu_nu F^mu_nu/4 + L_baryons[A,phi] + L_Einstein.

phi is a real phase field; chi is complex, of charge -q; baryons carry charge
q_b per reference particle. Gauge consistency, an ultraviolet completion and
observational viability are not established. This is not the adopted action.
For example, m_chi(phi)^2=m0^2+y^2*phi^2 makes phi=0 the light-particle phase
and phi=v a heavy-particle exterior. A biased quartic U can have these two
local minima, with B=U_inside-U_outside>0, in the thin-wall regime. B is a
vacuum ENERGY-density contrast, not automatically rho_DE*c^2.

For a cold condensate in the interior, write chi=exp(-i*m*t)*psi/sqrt(2*m).
At leading nonrelativistic order, n=|psi|^2 and

    g = lambda_chi/(4*m^2),
    e(n) = m*n + g*n^2/2,
    mu = m+g*n,  P = n*mu-e = g*n^2/2.

Here g>0, gradients of the condensate amplitude are neglected in the bulk
(Thomas-Fermi limit), and g*n << m is required. Pressure is now derived from
an interaction. The wall force is P_edge=B+2*Sigma/R, provided gauge stresses
and other omitted stresses are negligible at the interface. Sigma is obtained
from the phase profile; for the earlier degenerate quartic it is
sqrt(lambda_phi/2)*v^3/6 at leading thin-wall order. Large density backreaction
requires solving the joint wall profile instead of using that vacuum formula.

Relaxing a local massive phase fluctuation z makes the connection explicit:

    f(n,z) = g*n^2/2 + k*z^2/2 + h*n*z,    k>0,
    z_eq=-h*n/k,
    f_eff=(g-h^2/k)*n^2/2.

The phase contributes an ATTRACTION, so positive compressibility requires
k*g>h^2. This local expansion is generic; at the special phi=0 endpoint of
the even mass function above, h=0 and this correction vanishes. The pressure
and relaxation identities are certified in Lean with explicit hypotheses.

The same-field connection does not fix all couplings. Under the previous
physical width deformation, potential and mass functions at fixed phi/v stay
fixed while the canonical field range increases by s. Then h -> h/s,
k -> k/s^2, and h^2/k stays fixed, whereas Sigma -> s*Sigma. Lean certifies
the induced-coupling invariance. More generally, homogeneous free-energy
minima at each fixed density stay unchanged under that deformation; a canonical
planar wall integral scales with the field range. Thus even local phase
relaxation can leave pressure unchanged while changing wall tension. This is
a family of different actions, not an extra symmetry of one action.

## 2. Does the baryon interaction actually select the particle inventory?

There are three different physical choices; they cannot be interchanged:

* With exact chi charge and no exchange, its inventory is an initial conserved
  datum. Equilibrium in R does not license varying that charge.
* Number-changing reactions can impose zero chemical potential only for a
  nonconserved species in a specified equilibrium bath. At zero temperature,
  in an empty stable phase with m>0 and g>0, e(n)=m*n+g*n^2/2 is minimized at
  n=0. Finite temperature, binding, pair separation or a driven source changes
  this problem and requires its own state and energy supply. This is a local
  empty-phase statement, not a theorem about every gravitational configuration.
* Gauge attraction could capture opposite charge until screening suppresses
  further attraction. Granting global neutrality gives q*N=q_b*N_b and hence
  M_pool/M_b=(m/m_b)*(q_b/q). The mass and charge ratios still remain physical
  inputs. The system needs an accessible charged reservoir, or production of
  compensating charge elsewhere, and a way to shed capture energy. The static
  action alone does not specify that formation history or reservoir.

There is a further consistency requirement. Outside a compact baryonic core,
Gauss' law in rationalized units gives

    E(r) = [q_b*N_b-q*N(r)]/(4*pi*r^2).

The force per pool particle is

    f_r = -G*m*[m*N(r)+M_b]/r^2 - q*E(r)
        = -[G*m^2-q^2/(4*pi)]*N(r)/r^2
          -[G*m*M_b+q*q_b*N_b/(4*pi)]/r^2.

Neutrality at the OUTER edge does not remove the electric force throughout
the halo. Stars carrying q_b also feel this field. Its mass-force identity
is Lean-certified. For a locally compressible condensate, neglecting gravity
just to identify the screening scale,

    mu=m+g*n-q*A0,  -laplacian A0=q_b*n_b-q*n,
    ell_screen=sqrt(g)/|q|.

Where density is positive and variations are slow compared with this length,
strong screening tends toward LOCAL neutrality n approximately (q_b/q)*n_b.
That tends to make the pool track the baryons instead of building an extended
halo. Weak screening does not give a parameter-free global inventory rule.
Neither limiting statement solves the full capture/transport problem.

## 3. Solve the conditional pressure-supported family anyway

To distinguish the pressure law from the inventory problem, grant N proportional
to M_b and omit gauge forces, baryonic gravity, wall gravity and vacuum gravity
in a pool-dominated Newtonian region. This is an explicitly conditional model,
NOT a self-consistent solution of the full charged action. Treat B,Sigma,g,m
as fixed positive microscopic data (Sigma=0 is also allowed). Thin walls,
nonrelativistic matter and negligible amplitude-gradient pressure are required.

With rho=m*n, hydrostatics gives

    g*n'=-G*m^2*N(r)/r^2,     N'=4*pi*r^2*n,
    a^2=g/(4*pi*G*m^2),
    n(r)=n_c*sin(r/a)/(r/a).

The regular, positive solution has x=R/a in (0,pi). The finite-pressure edge
sets both density normalization and inventory as functions of R:

    n_R=sqrt[2*(B+2*Sigma/R)/g],
    n_c=n_R*x/sin(x),
    N=4*pi*a^3*n_R*x*(1-x*cot(x)),
    v_edge^2=G*m*N/R.

The n=1 polytropic bulk profile is established prior art: C. G. Boehmer and
T. Harko, *Can dark matter be a Bose-Einstein condensate?*,
[arXiv:0705.4158v4](https://arxiv.org/pdf/0705.4158v4), equations (29), (40)–(42),
uses the quartic-condensate Thomas-Fermi profile and its mass/velocity curves.
Here the specific addition is a nonzero phase-pressure boundary and the
fixed-parameter family-slope test below. No novelty claim is made.

### A uniform analytic scaling bound

Write

    I(x)=(1-x*cot(x))/x^2,
    N=4*pi*n_R*R^3*I(x),
    t=2*Sigma/(B*R+2*Sigma),  j=x*I'(x)/I(x).

For B>0 and Sigma>=0, 0<=t<=1. Also I>0 and I'>0 throughout (0,pi).
Here is an elementary proof, rather than relying on a numerical scan:

    I'(x)=h(x)/[x^3*sin(x)^2],
    h(x)=x^2+x*sin(x)*cos(x)-2*sin(x)^2,
    h''(x)=4*sin(x)*[sin(x)-x*cos(x)].

The bracket is zero at zero and has derivative x*sin(x)>0 on (0,pi), so
h''>0. Since h(0)=h'(0)=0, h>0 and therefore I'>0. The same positive bracket
shows I>0. Differentiating the edge density and total inventory then gives

    L = d log N/d log R = 3-t/2+j >= 5/2,
    b = d log(v_edge^4)/d log N = 2-2/L >= 6/5.

For N proportional to M_b and fixed particle mass this is also the baryonic
mass exponent. Thus v_edge^4/M_b increases with mass; its logarithmic slope
is at least 1/5. It cannot be a constant, including the requested coefficient
1/2, over this fixed-parameter family. Lean certifies the ordered-field algebra
from t<=1, j>=0 and the two derivative identities to b>=6/5 and b!=1.
The sine calculus and its interpretation as a physical family are analytically
proved here and symbolically checked, not formalized in Lean.

Small-radius limits provide independent checks: bulk-pressure dominance gives
N proportional to R^3 and b -> 4/3; tension dominance gives N proportional to
R^(5/2) and b -> 6/5. Formally R approaches pi*a at large N and b -> 2, though
the Newtonian/nonrelativistic assumptions can fail before that limit.
The rotation curve is proportional to sin(r/a)/(r/a)-cos(r/a) in v^2; it is
not exactly flat on an open interval. A locally flat portion can exist. The
bound is specifically for edge velocity, not every observational definition
of a fitted flat velocity and not a no-go theorem for all condensate halos.

### What stability has actually been checked

For a fixed-shape, fixed-N homologous trial family, the energy has the form

    E(R)=constant + A/R^3-D/R+C*R^3+S*R^2,

with positive interaction A, self-gravity D, volume C and surface S. At a
stationary point,

    E''=6*A/R^5+12*C*R+6*S > 0.

Its denominator-cleared identity is Lean-certified. This tests one dilation
mode only. It is not a proof of stability to all radial perturbations, gauge
modes, phase conversion, nonspherical deformations or quantum leakage.
The earlier warm radiative fluid and this cold condensate are different
models; their stability evidence must not be combined.

## 4. Try to identify couplings through symmetry

A genuine symmetry is stronger than declaring unrelated couplings equal.
The simplest candidate combines the three real components into

    U_sym=lambda*(phi^2+2*|chi|^2-v^2)^2/4.

In the ungauged symmetric limit its vacua form a connected sphere. The path
phi=v*cos(theta), chi=v*sin(theta)/sqrt(2) connects phi=+v to phi=-v while
U_sym stays zero. Across a slab of thickness L, choose theta increasing
linearly from 0 to pi. Its gradient energy per area is

    Sigma_trial = pi^2*v^2/(2*L).

This approaches zero as L increases. Hence this symmetric model has no
positive minimum wall tension between those vacua; the needed phase wall is
not supplied. Also the two endpoints have the same pool fluctuation spectrum,
so they do not provide the required asymmetric mass barrier. Anisotropy,
gauging or explicit phase bias can change these statements, but breaks the
proposed simple coupling-identification argument and must be specified.
This analytic trial-path construction was not certified in Lean.

## 5. Recorded evidence, review and next dependency

Original run: coupled_condensate_evidence/manifest.json, status failed,
117/120 checks. The only failures were the three finite-difference comparisons
at x=3.1. At step 1e-5 their relative errors were about 1.86e-7. Halving the
step reduced these by approximately four; Richardson extrapolation brought
them to about 1.1e-11. The tolerance was not loosened.

Refined run: coupled_condensate_refined_evidence/manifest.json, status completed,
121/121 checks. This includes exact symbolic differential identities, direct
mass quadratures and derivative/scaling checks at 27 dimensionless fixtures,
and eight Lean theorem/axiom reports. Fixture values G=m=a=B=1, g=4*pi are
mathematical checks, not selected galaxy parameters. Valid physical ranges
must additionally satisfy the approximations above.

Negative control: coupled_condensate_mutation/ replaces 2*Sigma/R with Sigma/R
in the density construction; the genuine force-balance tests reject it.
Original and corrected code, data, logs and manifests are retained separately.

All eight Lean theorems compile with only propext, Classical.choice and
Quot.sound, without sorryAx. They prove algebra over arbitrary fields, with
order assumptions for the last three. The hypotheses are explicit; the full
field theory, real analysis, positivity of physical constants, capture process
and all-mode stability are not certified by them. Reproduce with:

    lean action_scale_investigation_2026_11_05/joint_phase/lean/CoupledCondensate.lean

Self-review: checked the complex-field normalization g=lambda_chi/(4*m^2),
thermodynamic pressure, induced-interaction sign, Gauss-law force signs,
Laplace factor, profile mass integral, h'' positivity argument, logarithmic
slope conversion and the fixed-shape stability limitation. No independent
review is claimed. The mutation failure and convergence recovery are evidence
about the implementation, not replacements for the analytic argument.

Disposition: the simple repulsive-quartic, constant-parameter conditional
family cannot supply universal edge MOND scaling; the simple O(3) identification
cannot supply the required wall. The full charged model remains unsolved and
requires a reservoir, capture dynamics and simultaneous force constraints.
Density-dependent interactions, a thermal component or another symmetry could
change the pressure law, but need a microscopic reason and cannot borrow this
family's proof or earlier warm-halo stability. An extended exact self-gravitating
r^-2 tail needs effectively isothermal pressure, whereas the present repulsive
condensate has P proportional to rho^2. Returning to a thermal pool without a
derived temperature would restore the earlier unresolved input. No physical
interaction fixing mass, pressure, tension AND the uncalibrated 1/2 has yet
been established.
