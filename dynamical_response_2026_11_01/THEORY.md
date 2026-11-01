# PN28 canonical quadrupole response in the declared fast-scalar limit

**Scope.** This is the actual linear canonical kinetic response of the
specified PN28 waterbag parent, retaining its reciprocal mean-current term,
in the explicitly declared limit `F^2 -> 0` at fixed `C_s=F^2 c_s^2`.
It is not the isotropic fluid model, and a fluid Hessian plus a shear penalty
is not used as a kinetic equation of motion. The base states are FR01's
`psi_c=0.2, epsilon=0.01` dilute halo and its existing compact spherical-baryon
endpoint, with the same phase-space level and parent coefficients.

This analytic derivation was independently reconstructed by
`/root/core_gap_check`, 2026-11-01, from
`field_response_2026_11_01/inputs/PARENT.md`, its static-gradient snapshot,
and `field_response_2026_11_01/STATIC_DERIVATION.md`. No numerical experiment
was performed for this derivation. Static source and endpoint provenance
must be pinned by the execution manifest.

## 1. Full canonical parent and its linearization

Use physical canonical momentum per unit mass `p`. Define

```text
rho = integral f dp,
j = integral p f dp,
K_raw = integral (p^2/2)f dp,
K = K_raw-|j|^2/(2rho),
A(s)=exp(-2s),        g=grad s.
```

The full Hamiltonian density, with scalar momentum `pi`, is

```text
H = |j-pi grad s|^2/(2rho)
    + A(s)[K_raw-|j|^2/(2rho)]
    + pi^2/(2F^2) + (C_s/2)|grad s|^2 + U(s)
    + rho Phi_d/2 + rho Phi_b,
U(s)=B[exp(3s)-3s-1],       Delta Phi_d=4pi G rho.
```

The uniform vacuum baseline is subtracted. The static spherical background
has `j_0=pi_0=0` and

```text
h_0(x,p)=A_0(r)p^2/2+Phi_d,0(r)+Phi_b,0(r),
f_0=f_* 1_(h_0<mu).
```

Functional differentiation, rather than extrapolation of the static
single-orbit Hamiltonian, gives the first-order orbit Hamiltonian

```text
h_1 = Phi_d,1+Phi_b,1-A_0 p^2 sigma
      + {[(1-A_0)j_1-pi_1 grad s_0]/rho_0}.p.
```

The current term is essential. It ensures that the perturbed mass current
is `j_1-pi_1 grad s_0`, whereas retaining only the static kinetic metric
would incorrectly give `A_0 j_1`. In particular, even when `pi_1=0`, the
term `(1-A_0)j_1.p/rho_0` survives.

Let `D_0={.,h_0}` be transport along the background canonical orbit, with
`{a,b}=grad_x a.grad_p b-grad_p a.grad_x b`. The equations are

```text
partial_t f_1+D_0 f_1+{f_0,h_1}=0,

partial_t sigma
  = (F^(-2)+|grad s_0|^2/rho_0)pi_1
    -grad s_0.j_1/rho_0,

partial_t pi_1
  = C_s Delta sigma-[4E_rel,0+9B exp(3s_0)]sigma+2A_0 K_raw,1.
```

Terms `div(u pi)` are quadratic about this zero-current static state and
therefore do not appear at linear order. The displayed current/scalar
coupling follows from the parent's canonical Hamiltonian; it is not a
phenomenological drag.

## 2. A one-level waterbag closes on its energy surface at linear order

Write the perturbation as a distribution on the occupied boundary:

```text
f_1 = f_* delta(mu-h_0) eta.
```

Since `f_0'(h_0)=-f_* delta(mu-h_0)` and `D_0 h_0=0`, the exact linear
equation becomes

```text
(partial_t+D_0)eta = -D_0 h_1.
```

Thus a zero initial perturbation driven by a smooth Hamiltonian forcing
remains on this five-dimensional phase-space surface at linear order.
Interior velocity-space sampling is unnecessary for the linear moments.
This is not a claim that the finite-amplitude distribution stays isotropic
or that arbitrary nonlinear waterbags have a closed moment hierarchy.

At fixed position let
`p_F=[2(mu-Phi_d,0-Phi_b,0)/A_0]^(1/2)`. Then

```text
rho_1 = f_* (p_F/A_0) integral eta(x,p_F nu) dOmega_nu,
j_1   = f_* (p_F^2/A_0) integral nu eta(x,p_F nu) dOmega_nu,
K_raw,1 = (p_F^2/2)rho_1.
```

The last relation holds exactly for these surface perturbations, including
anisotropic ones. It simplifies the scalar source; it does not turn the
transport equation into a barotropic fluid equation.

The surface measure is invariant under background orbit transport. An
initially zero canonical perturbation has zero orbit-average component;
the zero-frequency component of `D_0` cannot be driven. It must remain fixed
at zero, rather than being assigned unit static susceptibility. In particular,
the zero-frequency causal response need not reproduce a neighboring isotropic
hydrostatic equilibrium, which can have different orbit populations.

## 3. Dimensionless units, including the temporal parameter

Use the FR01 units

```text
rho_*=[3B/(2k)]^(3/5),         h_*=5B/(2rho_*),
ell^2=h_*/(4pi G rho_*),       t_*=ell/sqrt(h_*),
epsilon=C_s/(3B ell^2).
```

Below `r,p,t,n,j,phi` are in units `ell,sqrt(h_*),t_*,rho_*,
rho_*sqrt(h_*),h_*`. Energies use `rho_* h_* ell^3`; angular normalization
is stated separately by the numerical basis. Define

```text
alpha = F^2/(B t_*^2) = 3epsilon/(c_s^2/h_*),
Pi = pi/(B t_*),             beta=B/(rho_*h_*)=2/5.
```

The stationary density is `n=exp(3s_0)psi_+^(3/2)` and on the occupied
surface `A_0 p^2=2psi`. The dimensionless waterbag level is fixed:
`f_*=3/[4pi 2^(3/2)]`, when `n=integral f dp`.

The finite-speed linear equations are therefore

```text
h_1 = phi_d,1+phi_b,1-2psi sigma
      + {[(1-A_0)j_1-beta Pi grad s_0]/n}.p,

sigma_dot = Pi/alpha-grad s_0.(j_1-beta Pi grad s_0)/n,

Pi_dot = 3epsilon Delta sigma
         -[6npsi+9exp(3s_0)]sigma+5psi n_1,

Delta phi_d,1 = n_1.
```

These equations show exactly which temporal coefficient was absent from
the static FR01 calculation. Fixing `epsilon` does not select `alpha` or
`c_s`. Any finite-speed investigation must declare that extra dimensionless
parameter and must not fit it silently to the desired response.

## 4. Declared fast-scalar calculation

Set `F^2 -> 0` with `C_s` fixed, so `alpha -> 0` and propagation speed tends
to infinity. In the declared constrained Hamiltonian model the scalar has
no independent propagating degree of freedom: `Pi=0` and it minimizes the
instantaneous scalar energy. Define, in the energy units above,

```text
A_s = -(6/5)epsilon Delta + (18/5)exp(3s_0)+(12/5)npsi,
A_s sigma = 2psi n_1,

h_1 = phi_d,1+phi_b,1-2psi sigma+(1-A_0)j_1.p/n.
```

These are the root implementation's coefficients
`-1.2epsilon, 3.6, 2.4`. The scalar operator is positive on the specified
static background and boundary conditions. Its inverse gives a reciprocal
attractive response, not dissipation. The retained current term supplies the
correct physical mass current `j_1` and continuity equation
`n_1_dot+div j_1=0`.

This is a singular limit and a declared model restriction. Interior
adiabaticity requires forcing/orbit frequencies small compared with the
relevant finite-speed scalar frequencies. The limit is not automatically
uniform at the free matter edge, because the finite-speed system contains
`alpha |grad s_0|^2/n`. A finite-speed extrapolation would require a separate
edge analysis or convergence in `alpha`, not just a fast interior frequency.
The present calculation makes neither assertion. It has no scalar radiation,
outgoing-wave cooling or scalar-mediated friction. It also does not provide
a general nonlinear prescription for the parent's vacuum denominators.

Only `n>0` carries kinetic surface degrees of freedom. At the edge
`n=O((R-r)^(3/2))`, `p_F=O((R-r)^(1/2))`; regular driven currents have finite
`j_1/n`. No arbitrary density floor should replace this regularity condition.
The exactly radial orbit reaching `p_F=0` at the boundary has zero measure
in the orbit ensemble; its limiting treatment must not manufacture a finite
population. These are numerical domain obligations, not a license to omit
near-edge orbit quadrature.

## 5. Quadrupole decomposition and boundary conditions

For one spherical harmonic with `integral |Y_lm|^2 dOmega=1`, set
`l=2` and write `n_1=N(r)Y_2m`, `sigma=S(r)Y_2m` and
`phi_d,1=V(r)Y_2m`. The radial operator is

```text
Delta_2 = d^2/dr^2+(2/r)d/dr-6/r^2.
```

Replace `Delta` by `Delta_2` in Poisson and `A_s`. At the center both scalar
fields are regular and proportional to `r^2`. Outside the matter, self-gravity
decays as `r^(-3)`, so its exact exterior condition is
`V'(L)+3V(L)/L=0`.

For a sufficiently remote scalar boundary, set `kappa=sqrt(3/epsilon)`.
The decaying constant-vacuum solution is proportional to

```text
k_2(kappa r) = exp(-kappa r)
              [(kappa r)^2+3kappa r+3]/(kappa r)^3.
```

Its exact logarithmic derivative gives

```text
S'(L)+b_2(L)S(L)=0,
b_2(L) = kappa+3/L
         -kappa(2kappa L+3)/[(kappa L)^2+3kappa L+3].
```

This is the exact `l=2` Robin condition for the constant-vacuum tail, not
the monopole condition `kappa+1/L`. It is asymptotic when the background
scalar tail is nonzero. The scalar quadratic energy must retain the exterior
boundary contribution `(6/5)epsilon L^2 b_2(L)|S(L)|^2` in its Hessian,
or use an explicitly integrated exterior. Longer-domain refinement checks
the remaining background-tail approximation.

The current can be decomposed into radial, poloidal and toroidal vector
harmonics. With
`j_1=J_rY_2m e_r+J_t grad_Omega Y_2m+J_o e_r cross grad_Omega Y_2m`,
continuity in the fast limit is

```text
N_dot+(r^2 J_r)'/r^2-6J_t/r=0.
```

The vector current vertex in `h_1` must be represented consistently with
these angular components. Scalar forcing on the isotropic spherical state
does not justify replacing the current vertex by a radial-only monopole.

## 6. Causality and orbit Fourier response

For zero initial perturbation, the exact retarded surface solution is

```text
eta(z,t) = -integral_0^t [D_0 h_1](z_(-(t-tau)),tau) dtau,
```

where `z_t` is the unperturbed canonical orbit. For an orbit Fourier component
with `D_0=i nu`,

```text
eta_n_dot = -i nu [eta_n+h_1,n],
eta_n(t) = -i nu integral_0^t exp[-i nu(t-tau)]h_1,n(tau) dtau.
```

The same equations apply after closing the density, scalar and current
feedback. A frequency-domain retarded convention uses time dependence
`exp(-i omega t)` and the limit `Im omega -> 0+`:

```text
eta_n(omega) = -nu h_1,n(omega)/(nu-omega).
```

Using `Im omega<0` would select the advanced prescription. Setting the
denominator's imaginary part to zero before controlling resonances is not
a causal calculation. A finite orbit/Fourier discretization can instead
integrate the conservative matrix system directly, avoiding a phenomenological
damping coefficient. Finite resolution then causes recurrences; apparent
phase mixing on a finite time interval is not an irreversible heating proof.

## 7. Conserved quadratic Hamiltonian and the correct finite stability test

On the surface define

```text
<a,b> = integral f_* delta(mu-h_0) a* b d^3x d^3p.
```

The first term in the second-order energy is `<eta,eta>/2`. It comes from
the energy cost of displacing the occupied phase-space boundary at fixed
waterbag level and mass. It is not an imposed fluid compressibility.
After minimizing the fast scalar, the reduced energy is

```text
E_2 = (1/2)[ <eta,eta>
       + integral n_1* phi_d,1 d^3x
       - <2psi n_1, A_s^(-1)(2psi n_1)>_x
       + integral (1-A_0)|j_1|^2/n d^3x ].
```

Gravity and the scalar term are negative semidefinite. The current term is
nonnegative on the stated backgrounds because `s_0>=0`, hence `A_0<=1`.
It vanishes when `s_0=0`, as required for an ordinary canonical kinetic gas.
All kernels are reciprocal/self-adjoint with the declared tail conditions.

An independent normalization check uses the exact shell moment
`integral f_* delta(mu-h_0) p_i p_j dp=(n/A_0)delta_ij`.
The least shell norm at specified local current is therefore
`A_0 |j_1|^2/n`. Adding the reciprocal current term restores
`|j_1|^2/n`, the correct bulk-velocity inertia. Omitting that term would
give the wrong mean kinetic energy even before any gravitational response.

In a correctly weighted finite surface/Fourier basis write
`E_2=z^dagger H z/2`, `H=I+K`, and

```text
z_dot = -i Omega(H z+b_ext),
Omega = diag(real orbit Fourier frequencies).
```

For zero external drive the matrix evolution preserves this quadratic
energy. If finite `H` is positive definite, its generator is similar to
`-i H^(1/2) Omega H^(1/2)`, an anti-Hermitian matrix. Thus that finite
discretization has no exponentially growing modes. Positivity in a finite
basis does not prove continuum stability. Conversely negative `H` alone
does not prove a growing kinetic mode: the signed transport operator matters.
This is why FR01's accessible energy saddles were not called kinetic
exponential instabilities.

Numerical tests should distinguish weighted Hermiticity, source/response
reciprocity, conservation of the unforced quadratic energy, and convergence
of the driven response. A positive matrix after dropping the required
current or angular components would test a different model.

## 8. External work and angular momentum

With `b_ext` representing the prescribed potential, the exact linear-system
work identity is

```text
d/dt [E_2+Re<eta,phi_b,1>]
    = Re<eta,partial_t phi_b,1>
    = Re integral n_1* partial_t phi_b,1 d^3x.
```

The interaction energy must be included for a time-varying source. After
the source has returned to zero, `E_2` is the work retained in the
perturbation, not a demonstrated thermalized component.

The parent's total canonical rotation generator in physical units is
`integral x cross (j-pi grad s) d^3x`, using the active-rotation convention
`delta s=-(theta cross x).grad s`. In the present fast limit it reduces to
`integral x cross j d^3x`. Its external torque is

```text
T_z = -integral rho partial_phi Phi_b d^3x.
```

For a rigidly rotating quadrupole with fixed envelope and pattern speed
`Omega_p=omega/m`, `partial_t Phi_b=-Omega_p partial_phi Phi_b`; hence
the externally supplied power satisfies `P=Omega_p T_z`. A growing or
decaying envelope adds its own amplitude-change work. About a spherical
background the quadrupole's net work and torque first appear at second
order in forcing amplitude, from the linear density response times the
linear source. This gives a measurable response/work ledger without
inserting a torque efficiency or drag by hand.

The full finite-speed model can exchange energy and angular momentum with
scalar radiation. The specified fast-scalar experiment cannot; neither a
radiative cooling mechanism nor a cosmological state-selection result may
be inferred from it. It is a bounded causal baryonic-response calculation
in a precisely stated limit of the existing action.
