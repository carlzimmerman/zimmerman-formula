# IC13: positive transition kinetic term, then a derived spatial repair

2026-09-08. **Two explicit constructive steps; full theory remains OPEN.**
Starting from [the combined IC12 action](IC12_COMBINED.md), this calculation
first repairs the negative scalar ultraviolet kinetic coefficient without
changing the homogeneous solution. Its actual scalar quadratic variation
reveals a quartic gradient instability. An additional, explicitly varied
curvature-square term removes that quartic instability at the tested
isotropic state, but leaves a scalar cone far wider than the physical
light cone. Neither partial result is labeled full closure.

## Action-level shear repair and smooth extension

Use IC12's definitions, normalized units `m=h0=1`, and put

    d=eta(1-eta),  a=aUV,12,
    delta A=(6/E)(d+a²/d),  As=A+delta A,  Cs=As^-1

inside a transition component (`0<eta<1`). Set `delta A=0` directly on
the static and expanding plateau neighborhoods. The proposed physical
Hamiltonian change is

    delta H13 = (2/m) delta A P_TF²
                -(m/2)(As^-1-A^-1) Rhat.

Here the displayed `delta A` formula uses the normalized scalar coefficient
`a` and `m=1`; all numerical claims use those units. The full covariant phase
action is `integral sqrt(-g)[2P:Q-H12-delta H13]+Sm[g,psi]`. In canonical
variables the same change is

    delta Hcanonical = (2E/V) delta A pi_TF²
                       -(V/2)exp(u xi)(As^-1-A^-1) Rbar.

Indeed `P_TF²=exp(-6w)pi_TF²/V²`, `Rhat=exp(-2w)Rbar`, and
`N sqrt(h)=V exp(xi+3w)`. These factors fix the momentum normalization;
the action is not defined by substituting a desired eigenvalue afterward.
Both new terms and their first variations vanish on flat isotropic
homogeneous data. The IC12 roots and their actual background velocities
therefore remain the correct solutions for this revision.

The apparent division by `d` has a smooth extension for this specific
activation. To see it without assuming that a ratio of flat functions is
smooth, define on a transition component

    D=(r²-1)²,  L=1/(1/4-D)-1/(D-1/16),
    eta=1/(1+exp(L)),
    eta_r=-d L_r,
    eta_rr=d[(1-2eta)L_r²-L_rr].

IC12's exact identity then gives `a=d v`, where

    T=(1-2eta)L_r²-L_rr,
    v=E(J^-1-1)(4r L_r-r² T)/12 - B E² T/36,
    B=(5/64)exp(-31S).

Thus the implementation evaluates `delta A=(6/E)d(1+v²)` without dividing
two tiny numbers. At each finite switch boundary, `L_r` and `L_rr` have
only finite-order rational poles in the boundary distance. The same holds
for every fixed derivative of `v`. Meanwhile `d` and its derivatives are
an exponentially decaying factor times finite-order poles. Consequently
`d(1+v²)` and every derivative tend to zero. This proves the claimed
`C-infinity` zero extension locally on the original field chart, where
`E`, `J`, `B`, and their derivatives are regular. In particular the static
and plateau action restrictions and all correction jets there survive.

Since `A>0`, `As>0`. The scalar UV kinetic coefficient is now

    a13=E As/6+h12,rhorho/4
       =a+d+a²/d=d[(v+1/2)²+3/4]>=3d/4>0.

The isotropic tensor coefficient is still exactly luminal:
`cT²=As Cs=1`. This is a uniform algebraic kinetic repair on the transition
chart, not merely a positive number at one sample. It does not establish
the rest of the scalar characteristic conditions.

## Actual scalar variation, including curvature momentum dependence

The witness is IC12's newly solved `n=220` root, not an old IC10 root:

    (rho,xi,u)=(-2.17245296036635527032033,
                .224889240489975978802992,
                .625215911238655994231839).

The new coefficients there are

    a12=-.202971957823611117238279,
    d=.00272851115059057722994634,
    As=57.1926934776727930786356,
    a13=14.8986927089782702139305.

The homogeneous density used for the metric/momentum Hessian is exactly

    Hhom=V h12((lambda1+lambda2+lambda3)/V,xi,u)
           +(2E As/V)[sum(lambda_i²)-(sum lambda_i)²/3].

The code differentiates this raw action independently to check the
constructed six-by-six Hessian in `(ln V,lambda1,lambda2,lambda3,xi,u)`.
After varying the spatial shift, its scalar constraint gives
`delta lambda3=(2rho V/3)zeta`. The spatial gauge then leaves canonical
variables `(zeta,p_zeta)` with `delta lambda1=delta lambda2=p_zeta/4`,
`delta ln V=2zeta`, and auxiliaries `(delta xi,delta u)`.

Define `c=exp(u xi)/As` at `V=1`, and differentiate it with respect to the
canonical density `rho` and the two auxiliaries before imposing their
equations. The curvature density variation is

    delta C=(2c-4rho c_rho/3)zeta
                 +(c_rho/2)p_zeta+c_xi delta xi+c_u delta u.

Its scalar gradient Hessian has base entry `Hgradient,zeta zeta=6c`
before adding the symmetric cross entries `-2 delta C`; in particular

    Hgradient,zeta p=-c_rho,
    Hgradient,zeta q=-2c_q,
    Hgradient,qq=G11.

The code retains these momentum-dependent curvature terms and eliminates
the actual two-by-two auxiliary pencil `M+k²G11`. It does not reuse an
old scalar speed or omit the curvature response. At the witness,

    c=.0201244090033529016339433,
    c_rho=4.13359626516056721277916.

Writing the reduced scalar Hamiltonian Hessian as `[[Ck,Bk],[Bk,Ak]]`,
full-rank `G11` implies

    Ak=a13+O(k^-2),
    Bk=-c_rho k²+O(1),
    Ck=O(k²).

Hence `det(Hreduced)=-c_rho² k^4+O(k²)`. This is a scalar gradient
instability despite the repaired kinetic sign. Direct computation gives
`det(Hreduced)=-1.7085570452e21` at `k=100000`, with positive momentum
Hessian `14.8986929399`. The leading growing rate is proportional to `k²`.
This conclusion concerns this action on the tested local background; it
does not rule out further action corrections.

## Additional bounded construction: cancel the quartic term

Revisit the curvature-square mechanism of [IC7](IC7_CURVATURE_SQUARE.md),
but derive the coefficient for this full-rank transition auxiliary block.
On the chart `a13>0`, add

    delta Hsquare,canonical = V dR Rbar²,
    dR=c_rho²/(32a13).

The equivalent physical Hamiltonian addition is
`exp(w-xi)dR Rhat²`. It contains no inverse differential operator. No
global extension of this additional quotient is asserted here; the
candidate is explicitly restricted to its positive-kinetic chart.

At barred scale `B3`, the linear curvature is
`delta Rbar=4k² zeta/B3²`. Thus second variation adds
`32 V dR k^4/B3^4` to `Ck`. At unit volume and scale,
`a13(32dR)-c_rho²=0`, which cancels the entire quartic determinant term.
The coefficient at the witness is `dR=.0358391723042179850639016`.
This term vanishes, with its first variation, on the same flat homogeneous
solution and does not change the linear isotropic tensor sector.

For the actual evolving scalar equation, the script retains the background
derivatives, including `Vdot/V=logVdot` and `B3dot/B3=logVdot/3`. The equation is

    zeta_ddot-(Adot/A)zeta_dot+Omega² zeta=0,
    Omega²=A C-B²-Bdot+(Adot/A)B.

Derivatives of the reduced Hamiltonian are taken along the independently
computed IC12 background flow and checked against centered differences.
The physical light factor is `exp(2S)/B3²`. With the square correction:

| k | scalar momentum Hessian | Omega²/(k² exp(2S)) |
| ---: | ---: | ---: |
| 1000 | 14.9009884079 | 5610195.53918 |
| 100000 | 14.8986929399 | 5645645.66901 |

The quartic instability has been removed and the tested scalar frequency
is real, but the remaining scalar speed is vastly superluminal. These
finite-wavenumber numbers indicate a speed-squared limit of order
`5.64565e6`; no interval certificate or exact limit evaluation is claimed.
The next constructive condition is to control the remaining quadratic
spatial stiffness and its background-derivative terms while preserving
the kinetic and tensor identities. A successful cancellation of the
quartic term alone does not solve that condition.

## Reproduction and evidence limits

    python3 -m unittest test_ic13_shear_repair
    python3 ic13_shear_repair.py --require-full-closure

Tests were written first and initially failed because the model was absent.
They check the kinetic completion, exact plateau values, independently
differentiated homogeneous Hessian, actual curvature response, auxiliary
elimination residual, quartic failure and cancellation, physical-cone
failure, and evolving coefficient derivatives. The report emits both
candidates' scalar matrices and dispersion data and exits **2** because
full closure is still open. Arithmetic is mpmath at 60 decimal digits.

The kinetic and smooth-extension identities are algebraic/local analytic
arguments. The dispersion evidence is a bounded calculation at one actual
vacuum transition background. No all-background scalar/tensor cone,
matter-coupled characteristic matrix, global field constraint count,
strong-coupling estimate, MOND/PPN/lensing result, or viable cosmological
history is claimed. Only the three new IC13 files belong to this work.
