# A derived radial lapse equation with a regular flat limit

**The original action has a concrete spherical continuation worth testing.** Preserving its radial momentum relation gives a linear lapse equation at time symmetry. Its highest-derivative coefficient does not depend on the polarization or its potential and is nonzero for beta>0 on a regular radial chart. In the formal flat limit the equation has a unique regular, bounded solution with prescribed asymptotic lapse. This is progress toward a constrained dynamics, not a solved galaxy or a proof of full nonlinear stability.

Base: `c6a0b6f3c74c623eacce284ab3765f480049aee7`. Compared with the previous checkpoint, two unrelated preregistration commits were added; the audited action is unchanged. The preceding turn was progress. This work continues `PRESERVATION_RESULT.md`, with a new pre-run contract in `RADIAL_CONTRACT.md`. Self-review only.

## 1. Retain the radial metric before variation

Use the spherical spatial metric

```
ds_3^2=ell(r)^2 dr^2+R(r)^2 dOmega^2, P_i dx^i=P(r)dr.
```

Both ell and R are independent configuration fields. The angular integral is normalized out of the action consistently; all radial momenta below refer to that normalized action. The canonical pairs are (ell,p_ell), (R,p_R), (P,J). Set

```
c_beta=(1+beta)/(2+3beta), delta=beta/(2+3beta),
v=ell R^2,
d=[(R^2 P/ell)']/v,
t=(ell p_ell+R p_R)/2, p=t/v,
f(d)=d+gamma d^2/2.
```

Here t is the angularly reduced trace momentum density, not time; prime means radial derivative. To avoid ambiguity, the scripts call it `td`. In this report time derivatives are written explicitly as dot. The spatial curvature is

```
R3=2/R^2 [1-(R'/ell)^2-(2R/ell)(R'/ell)'].
```

The Hamiltonian H[N]=integral N(T+U) dr has

```
T=K/(ell R^2) [ell^2 p_ell^2+(R^2/2)p_R^2
               -c_beta(ell p_ell+R p_R)^2]
  +ell J^2/(2eta R^2),

U=v[(2Lambda-R3)/(4K)+w(P/ell)+f(d)].
```

For A33, w(z)=W(K|z|). The symbolic computation allows a general local w; for its derivative formulas use a smooth field patch, with the zero-field limit imposed separately. The radial magnetic term vanishes by spherical symmetry. No areal gauge has been imposed inside this action.

The radial momentum constraint is

```
H_r=p_R R'-ell p_ell'-P J'.
```

An independent Legendre transform of the radial extrinsic-curvature Lagrangian reproduces T exactly. This checks its normalization and the factors associated with the two angular directions.

## 2. Independent radial bracket

Computing canonical functional Euler derivatives of the full radial Hamiltonian gives

```
{H[N],H[M]}=integral V(NM'-MN')dr,

V=(p_R R'-ell p_ell')/ell^2
  +2delta v p'/ell^2
  +4K f'[(1-c_beta)tP/ell^2-p_ell P/ell]
  +f'J/eta.
```

The result equals the spherical restriction of the earlier three-dimensional bracket. It was computed from the radial action first, not assumed from that restriction. The potential w and Lambda cancel from this bracket, as expected for ultralocal terms.

Let

```
A=V-H_r/ell^2
 =2delta v p'/ell^2
  +4K f'[(1-c_beta)tP/ell^2-p_ell P/ell]
  +f'J/eta+P J'/ell^2.
```

A is the angularly reduced flux density. Regular-centre, no-flux preservation requires A=0, as derived in the preceding report. It is linear in the momenta and their first radial derivatives.

## 3. Preserve A rather than assuming it remains zero

On a time-symmetric slice p_ell=p_R=J=0, configuration velocities vanish at zero shift. The term from a nonzero shift is a spatial transformation of A and does not change its on-constraint preservation. At zero shift, Hamilton's equations give

```
dot p_q = -Euler_q[N U], q in {ell,R,P},

dot A = sum_q [(partial A/partial p_q) dot p_q
               +(partial A/partial p_q') (dot p_q)'].
```

This is linear in N and its radial derivatives. Its coefficients depend on the background ell,R,P, their derivatives, the potential and constants. The complete symbolic coefficients are saved in `radial_run/results.json` under `lapse_coefficients`, ordered by derivative of N. They are not replaced by the highest-order coefficient when solving a background.

The leading coefficient is particularly simple:

```
coefficient of N''' in dot A = -beta R^2/[K(2+3beta)ell^3].
```

There is no N'''' term in dot A. Taking the divergence of the flux equation and dividing by the volume gives the fourth-order radial principal part

```
-[beta/(K(2+3beta)ell^4)] N''''.
```

For beta>0, K>0, finite positive ell, and away from a radial coordinate singularity, this principal coefficient does not vanish. It is independent of P, W, eta, gamma and Lambda. The R=0 coordinate degeneracy must be handled with regular-centre conditions, not by treating the coordinate factor as a physical zero. No uniform bound is asserted as beta tends to zero or ell becomes unbounded.

**What this proves:** a nondegenerate spatial principal operator in this spherical, time-symmetric calculation. **What it does not prove:** invertibility under actual halo boundary conditions, positivity of the lapse, stability of perturbations, or a nonlinear Cauchy theorem. Lower-order terms and boundary conditions can still generate a kernel or obstruct a positive solution. A positive principal coefficient alone is insufficient.

## 4. Flat limit taken after variation

Now set ell=1, R=r, P=0, Lambda=0, w(0)=w'(0)=0 only after taking all variations. The exact result is

```
dot A = (r^2/eta) N'
       -[delta r^2/K] [N''+2N'/r]'.
```

Consequently dot A=0 on r>0 integrates once to

```
(1-L_c^2 Laplacian_radial)N = constant,
L_c^2=eta beta/[K(2+3beta)] >0,
Laplacian_radial N=N''+2N'/r.
```

For a smooth radial lapse at the origin, bounded at infinity with N approaching a specified N_infinity>0 and derivatives approaching zero, that constant is N_infinity. Write n=N-N_infinity. Then

```
n''+2n'/r-n/L_c^2=0,
n=(a exp(r/L_c)+b exp(-r/L_c))/r.
```

Regularity at the origin forces a+b=0, leaving a multiple of sinh(r/L_c)/r. Boundedness at infinity forces that multiple to vanish. Thus **N=N_infinity is the unique solution in this class**. On a finite domain a single prescribed outer lapse would not be sufficient to fix the integrated constant; extra appropriate boundary information is required. We do not infer finite-domain uniqueness from the asymptotic result.

This is the formal flat calculation behind the earlier scalar mode, not a claim that a finite-a0, positive-Lambda universe is globally Minkowski. The actual cosmological branch must be treated on its expanding background.

## 5. Link to the surviving scalar mode

The same L_c appears in the already checked flat scalar dispersion:

```
Q=K(2+3beta)/beta+eta k^2,
omega^2=gamma k^4/Q
       =(gamma/eta) L_c^2 k^4/(1+L_c^2 k^2),  c=1.
```

Thus its slow response and the screened lapse equation share a coefficient fixed by the action's parameters. This is a structural consistency relation, not a new parameter prediction. In SI units the low-k response coefficient is c sqrt(gamma/eta)L_c. Under the optional eta=gamma choice, it is c L_c. The ratio eta/gamma and beta remain inputs; neither this relation nor the lapse equation derives kappa.

The practical implication is narrow but useful: one need not introduce a new lapse-gradient repair term merely because the old first-class argument failed. The action already generates an extra constraint and a nondegenerate radial lapse operator. Whether this branch works physically is the next calculation, not an established conclusion.

## 6. Next discriminator

Construct a regular finite-stiffness polarized background satisfying the Hamiltonian and field equations, with declared matter dynamics and cosmological/exterior boundary conditions. Evaluate **all** the saved lapse coefficients there. Check the boundary-value operator for a kernel and obtain a positive lapse; then reduce the dynamical kinetic form and evolve constrained perturbations. A metric or P profile chosen without satisfying the background equations cannot establish stability of a galaxy solution.

Even success would establish only the gravity/polarization sector. The action still lacks a derived conserved interaction selecting which cold energy supplies the law. The successful phenomenological shear engine cannot be imported as that interaction.

## 7. Evidence

`radial_checks.py` performs six exact checks: independent Legendre transform, direct radial bracket comparison, lapse linearity, absence of a fourth derivative in the flux, the third-derivative coefficient, and the flat operator after variation. `radial_contract.json` and `radial_run/manifest.json` record the inputs, commands, versions and output hashes. Deleting the clock term is a deliberate mutation that must break the original bracket and flat-lapse predictions. Numerical evolution has not been run. All results are self-reviewed, and no global novelty or completed mechanism is claimed.

Verification outcome: baseline **6/6**, manifest valid with status `completed`; deleting the clock term gives the expected **4/6**, failing the radial bracket and flat-lapse identities. Mutation log/result are separate diagnostics outside the validated runner. Self-proofreading checked radial versus three-dimensional density conventions, the meaning of the integrated constant, and the scope of asymptotic uniqueness. No positive-lapse claim on a polarized galaxy background has been promoted from these checks.
