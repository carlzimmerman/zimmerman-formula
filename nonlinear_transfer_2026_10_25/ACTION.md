# Nonlinear transfer without a supplied front trajectory

This phase solves a specified canonical completion of the existing radial
energy. It does not derive that completion microscopically or replace the
previous unresolved F-state and population tests. Scalar speed is c and the
coupling is the previously normalized binding-prototype coupling, not a new fit.

## Coordinates and Hamiltonian

Use dV=r²dr, sigma=sqrt(kappa), kappa=(0.25 kpc/rM)², J=30. The covariant T
field is psi_T=exp(i g chi/sigma) phi_T. Its derivative coupling is removed
from the kinetic term by this exact field redefinition. With phi_F=psi_F,

    rho_s=|phi_s|²,
    B=cos(alpha) exp(i g chi/sigma) phi_T-sin(alpha) phi_F,
    H=E_density(rho_T,rho_F,alpha)
      +kappa/2 integral (|grad phi_T|²+|grad phi_F|²)dV
      +J integral |B|²dV
      +integral p_alpha²/(2 Z_alpha) dr
      +1/2 integral [Pi_chi²+c² |grad chi|²]dV.

In the implementation the cell-integrated alpha inertia is

    Z_i=(2/pi)² vol_i [ell² F(u_i)+(vacuum_length/rM)²]/c²,
    u=A m_T, F(u)=u²/(1-u).

The same existing response coefficient is used in carrier spatial and time
gradients. This is the stated Lorentz-type kinetic completion, not a unique
consequence of the static energy. The old barotropic K30 F pressure, binding,
gravity, response, volume and stiffness terms are retained. Material edge
kinetics uses the exact positive complex-field difference, replacing the old
finite-angle arithmetic-mean approximation. Its static benchmark is prepared
separately; optimizer preparation is never entered in the radiation ledger.

The carrier alpha is an unwrapped real angular variable during full evolution;
there is no radius pin or enforced angle equality. Only sin/cos enter the
onsite energy. Initial prepared data use the original principal angular branch.

## All forces, including the carrier-inertia density force

The material equations are i sigma phi_s,t=delta H/delta phi_s*. The T equation
contains J cos(alpha) exp(-i g chi/sigma) B and the F equation contains
-J sin(alpha) B. Both have their own spatial currents and density forces.

The density dependence of Z is load-bearing. At fixed carrier momentum,

    mu_T^(Z)=-1/2 sum_i (p_i/Z_i)² partial Z_i/partial m_T,
    mu_T^(Z)=-(2/pi)² ell²/c² A^T[vol F'(u) (p/Z)²/2].

Dropping this force would destroy the nonlinear energy balance. NT-FULL-AUDIT
tests its independent directional derivative and the scalar-source sign.

The remaining equations are

    alpha_t=p_alpha/Z_alpha,
    p_alpha,t=-delta E_density+alignment+spatial /delta alpha,
    chi_t=Pi_chi,
    Pi_chi,t=c² Delta chi-g Gamma,

where the carrier force is the derivative of the sum of the three indicated
energy terms, not a difference of unrelated forces. In explicit notation this
means -delta(E_density+E_alignment)/delta alpha, with carrier spatial energy
already included in E_density. The actual conversion source is

    Gamma=(2J/sigma) sin(alpha)cos(alpha)
           Im[exp(i g chi/sigma) phi_F* phi_T].

There is no imposed conversion rate. The continuity laws are

    rho_T,t+div j_T=Gamma, rho_F,t+div j_F=-Gamma,
    j_s=(kappa/sigma) Im(phi_s* grad phi_s).

Thus density is independently mobile in every material cell; neither a global
lambda nor an endpoint interpolation appears in full.py.

## What transfers energy

Gravity and pressure generate material phases and currents. Spatially changing
carrier alignment mixes these currents and the internal relative phase,
which determines Gamma. Reciprocal scalar feedback changes that same phase.
The exact continuum exchange is

    dH_material+carrier/dt=+g integral Gamma chi_t dV,
    dH_wave/dt=-g integral Gamma chi_t dV-P_out.

Accordingly the measured material-to-wave work is

    W=-g integral dt integral Gamma chi_t dV.

This is measured from each actual coupled midpoint state in adaptive.py.
It must equal wave energy plus escaped energy for initially zero wave data.
The complete energy ledger is an additional independent check. Mass and
Q=integral Pi_chi dV+g M_T obey their own ledgers, including sponge charge flux.
Redistribution with exactly conserved T current still has no direct scalar
source; the nonlinear calculation must actually populate the relative-phase
conversion channel. The equation does not guarantee that it does so efficiently.

## Numerical method and scope

Full.py solves the material block-banded Crank-Nicolson equations, scalar
finite-volume midpoint equations and the carrier momentum midpoint equations
together. At each iteration the carrier solves

    E_alpha(alpha_mid)+4 Z_mid(alpha_mid-alpha_0)/dt²-2 p_0/dt=0.

This is a dynamical root, not carrier minimization. Alpha_1=2alpha_mid-alpha_0
and p_1=4Z_mid(alpha_mid-alpha_0)/dt-p_0 retain carrier momentum. Infall,
conversion and wave reaction are iterated to joint residual tolerances.

The method preserves material norm and global shift charge to solver accuracy.
Implicit midpoint is not an exactly energy-conserving method for this
nonlinear Hamiltonian. Adaptive.py rejects inaccurate steps rather than
assigning their energy error to radiation. It reports the actual error and
the separately measured field-work identity. Very stiff carrier frequencies
are not automatically resolved merely because a midpoint solve converges.
Time, spatial and absorber comparisons remain necessary.

The static benchmark is not strictly force-certified: its preparation reports
maximum optimization gradient 6.36e-7 and relative-energy stopping. Its direct
unperturbed evolution and force checks are therefore reported separately.
No success flag alone proves the simultaneous galaxy conditions.
