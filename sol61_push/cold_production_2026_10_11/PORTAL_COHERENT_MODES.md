# The coherent density-wave speed follows from the two-field action

Status: a phase-locked homogeneous classical branch and its long-wavelength
phase mode are derived directly from the fixed-flux action. This replaces
an assumed pressure closure for that branch. It does not establish that
the produced multimode mixture occupies or approaches the branch.

## Stationary branch with both fields present

Retain the full potential

    V=m^2 |phi|^2+(4m^2+Delta)|chi|^2
      +g(chi* phi^2+chi phi*^2)+lambda_total |phi|^4+U(S),
    S=|phi|^2+4|chi|^2,
    U(S)=A_*[sqrt(S^2+S_0^2)-S_0].

The constant vacuum term is excluded from material quantities. Choose
phi=r exp(-i omega t), chi=s exp(-2i omega t), with r>0 and s<0 for g>0.
Let n=r^2 and delta=omega^2-m^2-U'(S). The exact stationary equations are

    delta=2g s+2lambda_total n,
    (Delta-4delta)s+g n=0,
    S=n+4s^2.

The aligned U' shifts cancel from the relative mass-squared gap. Thus the
weak-source branch can be solved without subtracting the much larger
m^2 terms. Define beta=2lambda_total n/Delta and gamma=2g^2 n/Delta^2.
The small root is

    delta/Delta=2(beta-gamma)/
        [1+4beta+sqrt((1-4beta)^2+16gamma)],
    s=-g n/(Delta-4delta).

This is the branch continuously connected to a daughter condensate at low
density; it is not a claim of uniqueness or global thermodynamic selection.
Exactly setting chi=0 would not solve the original coupled equations when
phi is nonzero. The small induced source has therefore been retained.

## Phase action and compressibility

For slow common phase variations, phi=r exp(-i theta) and
chi=s exp(-2i theta), define X=-g^ab partial_a theta partial_b theta;
X=omega^2 in the homogeneous rest frame. At leading derivative order,
eliminate the stationary amplitudes from

    L=X S-V.

By stationarity, the resulting phase Lagrangian P(X) satisfies P_X=S.
The charge density is Q/V=2omega S, consistent with the original charge
weights. Expanding the phase action around X=omega^2 gives

    c_phase^2/c^2=P_X/(P_X+2X P_XX)
                =S (dX/dS)/[2X+S(dX/dS)].

This is a low-frequency, long-wavelength amplitude-elimination result.
Derivative corrections from amplitude propagation and additional finite-
frequency modes are not included. It is not a complete Bogoliubov spectrum.

The derivative is available directly from the exact stationary equations.
With D=Delta-4delta and derivatives here taken with respect to n,

    delta'=(2lambda_total-2g^2/D)/(1+8g^2 n/D^2),
    s'=-g/D-4g n delta'/D^2,
    S'=1+8s s',
    dX/dS=U''(S)+delta'/S'.

The same equations yield the thermodynamic identity
c_phase^2/c^2=dP/dE along this stationary branch. No Maxwellian or local
thermal equilibrium was inserted to obtain the response.

## Local branch checks

At fixed omega, the real-amplitude Hessian of V-omega^2 S is

    H_rr=8lambda_total n+4n U'',
    H_ss=2D+64s^2 U'',
    H_rs=4g r+16r s U''.

The relative-phase curvature is -2g s n>0. The sampled amplitude Hessians
are positive definite; dX/dS>0 gives a positive phase kinetic coefficient
and positive sound-speed-squared. These are local classical checks, not a
nonlinear gravitational stability theorem or quantum naturalness analysis.

Using the unchanged illustrative parameters:

| S/S_0 | Source charge fraction | Action-derived phase speed, km/s | Earlier NR pressure speed, km/s |
|---|---:|---:|---:|
| 0.01 | 4.44e-17 | 33.6333335 | 33.6333341 |
| 0.1 | 4.44e-16 | 105.575071 | 105.575090 |
| 1 | 4.44e-15 | 199.999777 | 200.000000 |
| 10 | 4.44e-14 | 33.3857330 | 33.3857750 |
| 100 | 4.44e-13 | 3.36332919 | 3.36333341 |

The source charge fraction is 4s^2/S. At the crossover the relative
correction to sound-speed-squared is about -2.23e-6. Hence the large
coherent restoring response survives the exact stationary two-field
calculation; neglecting the induced source was not hiding a cancellation.

## Verification and scope

portal_coherent_modes.py checks both stationary equations, positive
amplitude Hessian eigenvalues, relative-phase curvature, positive subluminal
phase speed, and the implicit derivative against finite differences of
the chemical-potential shift. Subtracting m^2 before differencing avoids
loss of precision in the small shift. All 30 checks pass; the manifest
validates provenance. The phase-action and stationary-branch derivations
are self-reviewed. The equations provide the general reduction; the finite
samples do not prove global stability or uniqueness of the branch.

The production simulation had source charge fraction about 0.364 and a
spatially fluctuating multimode state. That is very different from the
small-source coherent branch above. Replacing the produced state by this
branch without a relaxation and energy-transport calculation would be an
unjustified change of state.

This turn establishes the pressure response from the microscopic action
for one identifiable branch. It strengthens the coherent cosmological
screen while leaving the actual mixture's time-dependent response open.
A successful cold-energy construction must still connect formation to the
appropriate state and derive the repo's halo profile and acceleration law.
Those requirements are not yet satisfied.
