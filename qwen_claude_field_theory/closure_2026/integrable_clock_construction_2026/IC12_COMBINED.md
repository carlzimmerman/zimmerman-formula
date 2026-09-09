# IC12: convex pressure combined with the spatial and tensor completion

2026-09-08. **Explicit combined action; transition scalar kinetic test fails.**
This is a new calculation on new homogeneous roots. It includes the
[activated convex pressure](IC11_CLOCK_PRESSURE.md) and the
[IC11 spatial/tensor correction](IC11_TRANSITION.md) together. No matter
reshaping or additional matter coupling is included.

## Action and independently varied homogeneous density

Use IC10's fields and IC11's correction, and add the pressure lift:

    H12 = H10 - eta exp(-4w) f(tilde X)
          -m/2 (A^-1-C_R) Rhat
          -m eta(1-eta)(1+tr(W²))(|Dxi|²+|Du|²),

    f(tilde X)=(5/64)(2 tilde X)^16,
    tilde X=exp(2w)Xphysical,  S=(2-u)xi,
    f(S)=(5/64)exp(-32S).

The full action is `integral sqrt(-g)[2P:Q-H12]+Sm[g,psi]`. All
definitions of `A`, `C_R`, `W`, `eta`, contractions, and boundary conditions
are those in IC11_TRANSITION.md. Numerical units are `m=h0=1`, `kappa=6`.
The static pressure correction and its first jets vanish because `eta=0`
on a neighborhood of `p=0`. On `eta=1`, the spatial/tensor correction
vanishes identically, leaving precisely the independently varied convex
pressure plateau, not the old IC10 pressure.

The canonical density factor is `N sqrt(h)=V exp(xi+3w)`, so

    delta hpressure=-eta exp(xi-w)f=-eta B,
    B=exp(S)f(S)=(5/64)exp(-31S).

Consequently the combined flat homogeneous density is

    h12=hbase+eta(r)[delta h10-B],
    hbase=-E rho²/3+exp((3u-2)xi)[Lambda+a0²U(u²)]
                         -3exp((3u-4)xi),
    delta h10=-E rho²(J^-1-1)/3,
    E=exp((4-3u)xi),  J=exp(-2w-1/6),  r=-E rho/3.

The script differentiates this expression before imposing the auxiliary
equations. Every first and second switch derivative is included. Numerical
differentiation of the raw Hamiltonian independently checks every gradient
and Hessian component at a transition point. The spatial/tensor correction
still vanishes identically on flat homogeneous data.

## Actual roots and preservation

The initial state is recomputed with `ic11_clock_pressure.state('.2')`.
Its changed expansion gives

    rho0=-3 exp(-1/6) Hpressure=-2.39245296036635527032033,
    xi0=0.139901151226159201400473,
    u0=0.570419197789965663436675.

The code solves `h12,xi=h12,u=0` at all 501 values
`rho=rho0+n/1000`, `n=0,...,500`, using the preceding root as the next
initial guess. No old IC10 rho history is reused. All roots remain inside
`0<u<1`; no root loss occurs in this bounded run. The maximum constraint
residual is `5.3522821266e-52` at 60 decimal digits.

For each root the code computes `M=h12,qq`, the actual homogeneous
four-by-four constraint matrix, its singular values and its numerical rank.
The matrix is

    D=[[0,-M],[M,Omega]],
    Omega12=(3/2)(h_xi h_rho,u-h_rho,xi h_u),
    Omega21=-Omega12.

Its rank is four at all samples, using a relative singular-value threshold
`1e-35`. This is a homogeneous constraint calculation, not a full field
Dirac certificate or a physical mode count. The computed preservation
equation is

    rhodot=-3h12/2,  logVdot=3h12,rho/2,
    M qdot+h12,q rho rhodot+logVdot h12,q=0.

The maximum residual of that equation is below `2.23e-59`. The physical
expansion computed from these velocities is positive at all 501 samples.

## Spatial repair survives; convex pressure does not cure the scalar UV sign

The combined pressure term has no spatial gradients. Therefore the
corrected auxiliary pencil remains

    Q12(k)=M+k²G11,
    G11=-2(1-eta)exp(u xi)[W+eta(1+tr(W²))I].

The minimum activation is approximately `0.995746896086`; the IC11 proof
of positive definiteness for the bracketed matrix applies. The largest
eigenvalue of `M` over the sample is `-3.52681974136`. Thus the conditional
matrix argument excludes auxiliary poles for every real wavenumber at
each numerically verified sample. The directly computed positive-pole
lists are empty. The isotropic tensor identity remains `cT²=A A^-1=1`.

The scalar ultraviolet momentum Hessian must use the NEW homogeneous
Hamiltonian:

    aUV=EA/6+h12,rhorho/4
       =-E(J^-1-1)(4r eta_r+r² eta_rr)/12
        -B E² eta_rr/36.

The last term follows because `B` has no rho dependence at fixed `(xi,u)`
and `r_rho=-E/3`. Omitting it would incorrectly import the IC11 formula.
The independent expressions agree to a maximum absolute error below
`1.62e-59` across the full sample.

| n | eta | physical H | aUV |
| ---: | ---: | ---: | ---: |
| 0 | 1 | 0.813795908489 | 0, outside full-rank UV reduction |
| 200 | 0.998768085276 | 0.843722075154 | +0.0575680682531 |
| 205 | 0.998141100037 | 0.859713094253 | +0.0191790702739 |
| 210 | 0.997729876650 | 0.865891322917 | -0.0447954514623 |
| 220 | 0.997264003171 | 0.869581325452 | -0.202971957824 |
| 500 | 0.995746896086 | 0.855926309976 | -7.04063964151 |

The first grid value with `aUV<-1e-30` is `n=207`. A direct finite
wavenumber scalar momentum Schur-complement check at `n=220`, `k²=1e16`,
also has negative sign. Thus this explicit combined candidate fails the
necessary positive scalar kinetic condition in its transition. The
pressure correction improves the plateau clock result and changes the
transition numbers, but does not repair this obstruction.

The formal `aUV=0` on `eta=1` is not a plateau ghost conclusion: there
the auxiliary spatial gradient rank vanishes and the full-rank ultraviolet
elimination used here does not apply. The plateau is checked by its own
algebraic pressure reduction. No conclusion is claimed for all possible
pressure functions or all other Hamiltonian redesigns.

## Reproduction

From this directory:

    python3 -m unittest test_ic12_combined_transition
    python3 ic12_combined_transition.py --require-full-closure

Tests were written before the model and first failed because it was absent.
The strict report contains every computed auxiliary matrix, homogeneous
constraint matrix, singular value, rank, residual, tensor factor, and
scalar UV coefficient; it emits 501 rows and exits **2**, with full theory
`OPEN`. Numerical arithmetic uses Python 3.9.6, mpmath 1.3.0 at 60 decimal
digits, and SymPy 1.14.0 for analytic derivative generation. These finite
results are not interval certificates. Matter-coupled characteristics,
anisotropic backgrounds, nonlinear field constraint closure, strong
coupling, galactic matching, lensing and PPN remain unproved.
