# Independent audit of the finite-amplitude homologous diagnostic

Reviewed 2026-10-27. Source: `eos_route/homology.py`, SHA-256
`cf009d7b5d082d5b2656caeb6187ce23cbad7a6c61dc717ec351c53814f4d740`.
Result SHA-256: `09c02f34528c4826f7217379f8940353e7da0363bdb4d972b478081ec13c9292`.
No new experiment performed. The existing manifest validates as a **failed** run:
one asserted sufficient barrier condition is false, although both stored trajectories return.

**Verdict: the reduced energy and inertia normalization are correct. The calculation supports two finite trajectories in a specified variational model; it is not an exact finite-amplitude pressure-confined fluid solution or a general attraction-basin proof.**

## Energy derivation

Write the EOS as

    P(rho) = P_ext + A ln(rho/rho_b),

where rho_b is the equilibrium boundary density. An internal-energy density satisfying
`P=rho du/drho-u` is

    u(rho) = C rho - P_ext - A[ln(rho/rho_b)+1].

The arbitrary conserved rest-energy term C M has no effect on the dynamics. Under
`rho_y(r)=y^-3 rho_eq(r/y)` and `V_y=y^3 V_eq`, direct change of variables gives

    [U(y)+P_ext V_y-CM]/(A V_eq)
       = y^3[-D-1+3 ln y],
    D = (1/V_eq) integral ln(rho_eq/rho_b) dV.

Hydrostatic scalar virial balance is

    W_eq + 3 integral P_eq dV - 3 P_ext V_eq = 0,

so `W_eq=-3 A V_eq D`. Self-gravitational energy scales as `W(y)=W_eq/y`.
Consequently the reported potential is exact on this constrained density family:

    V(y) = -3D/y + y^3(-D-1+3 ln y).

Its derivatives are

    V'(y) = 3D/y^2 + 3y^2[-D+3 ln y],
    V'(1) = 0,
    V''(1) = 9-12D = 5.26657706766 > 0.

The `P_ext V` term must be included in the ledger. It accounts for the work exchanged
with the constant-pressure environment; calling the ledger only “core plus emitted
wave energy” would omit that reservoir. “Reduced enthalpy plus kinetic and exported
energy” is precise.

## Constant inertia is a legitimate unit choice

For homology, the material velocity is `v(r,t)=dot y r/y`. Thus

    T_bulk = (1/2) I_eq dot y^2,
    I_eq = integral rho_eq(r) r^2 dV,

and I_eq is constant. Set `E_*=A V_eq` and `t_*=sqrt(I_eq/E_*)`. In time
`tau=t/t_*`, the dimensionless bulk kinetic energy is `(1/2)(dy/dtau)^2`.
Therefore collective inertia one is a harmless normalization, not a change of mass.

For a physical generalized damping coefficient zeta,

    I_eq y_ddot + zeta y_dot + E_* V'(y)=0,

the dimensionless damping is `gamma=zeta/sqrt(I_eq E_*)`. Choosing gamma=1 is still
a specified coupling, not a derived microscopic relaxation rate. The ideal outgoing
half-line model can realize a positive zeta. Its initial field must be compatible
with the initial boundary displacement; an instantaneous jump from an incompatible
zero field would carry additional singular preparation energy. Constant compatible
initial displacement is allowed for a shift-symmetric massless half-line field.

## Important limitation of the homologous trial family

Away from equilibrium, its surface density is `rho_s(y)=rho_b y^-3`, so

    P_s(y)-P_ext = -3 A ln y.

This is nonzero for both tested initial radii. A material free surface of the full
barotropic Euler system against fixed external pressure must satisfy traction
balance throughout its motion. The homologous family does not do so pointwise.
Its generalized force is obtained by varying the energy along the restricted family,
including external pressure work. It is therefore a collective-coordinate or
Rayleigh–Ritz approximation, with unresolved shape/boundary-layer response.

This does not invalidate the reduced potential or its energy conservation. It does
prevent promoting these trajectories to exact finite-amplitude solutions of the
earlier moving-pressure fluid boundary-value problem. The earlier radial eigenmode
has a nonconstant displacement shape and satisfies `3eta+xi eta'=0`; a purely
homologous displacement does not satisfy that condition.

## Barrier and the failed check

The local collapse barrier is at `y_b=0.676927036532`, with energy
`V(y_b)-V(1)=0.0958686853593`. The potential tends to minus infinity at y→0;
there is no global stability.

- `y(0)=0.8`, zero velocity: excess energy 0.0637384378193 is below the barrier,
  and the initial state lies on its right side. Nonnegative damping then supplies
  an energy barrier against crossing into collapse in this reduced model.
- `y(0)=1.2`, zero velocity: excess energy 0.146219914683 is **above** the barrier.
  Its computed trajectory radiates enough energy to turn around at y≈0.859872 and
  return to one. The stored trajectory establishes this instance, not a general
  super-barrier attraction basin.

The maximal recorded ledger errors are `5.99e-12` and `2.23e-11`. These are the
author's computations, inspected here, not an independent numerical reproduction.
The process exits one because `tested_initial_energy_below_barrier` is false.
Preserving that failure and reporting the two trajectories separately is correct.

The pressure coefficient, damping, EOS retention and boundary/shape response are
still supplied assumptions. The two trajectories neither derive those assumptions
nor show formation from an initially cold multistream field.
