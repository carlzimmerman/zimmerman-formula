# The missing preservation equation, and what survives it

**Result:** the A33 gravity/polarization action has a nontrivial lapse-preservation condition. Its previously asserted eight first-class constraints do not close. A smooth periodic counterexample satisfies that old constraint list but admits no smooth positive lapse. Nevertheless, the recorded flat scalar quadratic model has one healthy scalar after a correct second-class reduction, with the same dispersion as before. These findings narrow the repair; they do not establish a complete nonlinear theory or a new physical mechanism.

Base: `05a3bfdb73fd9194954dbcdb90602d2c2f979b83`; continuation of `RESULT.md` R1. Self-review only. No canonical theory file changed.

## 1. Canonical Hamiltonian

Work in the pure gravity/polarization sector. Standard minimally coupled matter would add its usual momentum contribution; no unprovided cold-sector bridge is assumed. Let

```
K=4piG, c_beta=(1+beta)/(2+3beta),
Pi^i = momentum conjugate to P_i (a weight-one vector density),
pi^ij = momentum conjugate to h_ij (a weight-one tensor density),
pi = h_ij pi^ij, d=D_i P^i, f(d)=d+gamma d^2/2, f'=1+gamma d.
```

The spatial covector P_i is the canonical configuration variable. D acts on densities with their density weight. In particular D_i pi=sqrt(h) partial_i(pi/sqrt(h)). Exclude beta=-2/3 and eta=0, where the Legendre map changes.

The full Hamiltonian density from the displayed A33 action is

```
H_perp = 4K/sqrt(h) [pi_ij pi^ij-c_beta pi^2]
       + h_ij Pi^i Pi^j/(2 eta sqrt(h))
       + sqrt(h) [(2Lambda-R3)/(4K)+W(K|P|)+f(d)+gamma F_ij F^ij/4].

H_i = -2 h_ij D_k pi^jk + Pi^j F_ij - P_i partial_j Pi^j.
```

The F^2 term must be retained even though the earlier A54 display omitted it. Define H[N]=integral N H_perp. On a compact boundaryless slice, or with boundary terms controlled,

```
{H[N],H[M]} = integral V^i (N partial_i M - M partial_i N),
```

where the vector density is

```
V^i = -2 D_j pi^ij
    + 2 beta/(2+3beta) D^i pi
    + 4K f' [(1-c_beta) pi P^i - 2 pi^ij P_j]
    + (f'/eta) Pi^i
    + (gamma/eta) F^ij Pi_j.
```

Here Pi_j=h_jk Pi^k. This is a formal analytic derivation for the displayed Hamiltonian. Independent symbolic checks cover the full plane-dependent diagonal/longitudinal sector and the three-dimensional P-gradient variation; they are not a machine certification of all 3D metric components.

Subtract the raised momentum constraint H^i=h^ij H_j. On H_i=0, V^i equals

```
A^i = 2 beta/(2+3beta) D^i pi
    + 4K f' [(1-c_beta) pi P^i - 2 pi^ij P_j]
    + (f'/eta) Pi^i
    + (gamma/eta-1) F^ij Pi_j
    + P^i partial_j Pi^j.
```

This A is a vector density, not a new field or free coefficient. It must not be confused with the A=2+3beta shorthand in A68.

## 2. Derivation by contributions

Only terms with spatial derivatives of the configuration variables can leave derivatives of the smearing functions. Ultralocal potential and kinetic cross terms cancel by antisymmetry; W's detailed nonlinear shape and Lambda do not enter V.

1. The gravity curvature/kinetic bracket supplies `-2D_j pi^ij + 2 beta/(2+3beta) D^i pi`. Its beta coefficient matches the pure lambda-R result under lambda=1+beta.
2. The P Euler derivative of the divergence potential is
   `delta H_f[N]/delta P_i = -sqrt(h) D^i[N f']`.
   Pairing it with `delta H_T[M]/delta Pi^i = M Pi_i/(eta sqrt(h))` gives `(f'/eta)Pi^i` in V.
3. The magnetic derivative is `-gamma sqrt(h) D_j(N F^ji)`. The same kinetic pairing gives `(gamma/eta)F^ij Pi_j` in V.
4. The metric variation of d must not be omitted. Its derivative-of-smearing term is

```
(delta H_f[N]/delta h_ab)|dN
 = -sqrt(h) f' [h^ab P^i/2 - h^{i(a} P^{b)}] partial_i N.
```

Contracting with `delta H_Tg[M]/delta pi^ab = 8KM(pi_ab-c_beta pi h_ab)/sqrt(h)` gives
`4K f'[(1-c_beta)pi P^i-2pi^ij P_j]`. This term is absent from the P-only calculation and is needed on nonzero P backgrounds.

The independent check starts with the full scalar curvature of `diag(A(x),B(x),C(x))`, not the proposed bracket. It computes canonical functional Euler derivatives for A,B,C,p and their momenta, extracts first and second derivatives of the smearing functions, integrates the second-derivative coefficient by parts, and obtains V^x. The residual against the formula above is identically zero for symbolic nonconstant fields. A separate Christoffel calculation verifies the scalar curvature used. Removing contribution 4 from the predicted expression is the mutation.

## 3. Preservation is a weighted-flux equation

For an arbitrary test function epsilon,

```
{H[epsilon],H[N]} = integral epsilon [2V^i partial_i N + N partial_i V^i].
```

On the constraints and for N>0, preservation therefore requires

```
2A^i partial_i N + N partial_i A^i = 0,
                 equivalently partial_i(N^2 A^i)=0.
```

No new constitutive freedom has been added. This equation follows from the action. One must decide, with boundary conditions, whether it imposes further phase-space constraints or fixes parts of the lapse. Merely noting that H_perp contains no N does not end the Dirac algorithm.

A useful mathematical reading is that N^2 weights the flux A to give zero divergence. Along a closed integral curve of a nonzero vector field (in flat coordinates here), a necessary condition for a smooth positive periodic weight is that the accumulated divergence over that orbit vanish. The next example violates that condition explicitly.

## 4. An exact smooth positive-lapse obstruction

On a flat three-torus, take x,y of period 2pi, unit z period, and choose

```
P_i=0,
Pi^i=J(sin x, cos x, 0), J != 0,
pi^ij=q delta^ij,
q^2=(2+3beta)/(12K) [J^2/(2eta)+Lambda/(2K)],
pi_N=pi_shift=0.
```

Take K,eta,beta,Lambda>0. All fields are smooth and |Pi|^2=J^2 is constant. Thus all eight previously asserted constraints vanish pointwise, exactly as in the constant-current witness: H_i=0 because P=0 and pi^ij is constant; H_perp=0 by the displayed q. The cap u<a0 is satisfied.

Here A=Pi/eta and partial_i A^i=J cos x/eta. On the closed orbit x=0, the preservation equation reduces to

```
2 partial_y N + N = 0,
N(0,y,z)=C(z) exp(-y/2).
```

A circuit y -> y+2pi multiplies N by `exp(-pi)=0.043213918...`. Periodicity forces C(z)=0. Consequently no smooth everywhere-positive lapse exists on these data. Allowing y- and z-dependent lapse does not evade the result.

J can be arbitrarily small. Choosing the expanding sign of q, these old-constraint data approach homogeneous expanding vacuum data as J goes to zero (the q shift is order J^2). The obstruction is not a strong-field or cap effect, and is independent of the acceleration footing and W beyond W(0)=W'(0)=0.

**Scope:** these are inadmissible data for any correctly completed constraint system. That does not by itself prove that no admissible data or no consistent branch exists. The theorem refutes sufficiency of the old constraint list and rules out a claim that every nearby datum on that list admits regular evolution. It is a periodic-domain result, not an exclusion of asymptotically isolated galaxies. Additional constraints, or a modified action, may remove the obstructed family.

## 5. Constructive check: the flat scalar mode survives with second-class constraints

This is a calculation for A68's stated quadratic flat-vacuum scalar model, after the shift has been eliminated, for one nonzero real Fourier mode k. It is not a proof that flat vacuum with finite a0 is the actual cosmological background; the physical positive-Lambda branch expands.

Write

```
a=(2+3beta)/(K beta), b=eta k^2,
L= a zdot^2/2 + b sigmadot^2/2
 + k^2 z^2/(2K) - (Kk^2+gamma k^4)sigma^2/2
 + n k^2(z/K+sigma).
```

All of K,beta,eta,gamma,k are positive. Let p_z,p_sigma,p_n be canonical momenta and

```
H0=p_z^2/(2a)+p_sigma^2/(2b)
   -k^2 z^2/(2K)+(Kk^2+gamma k^4)sigma^2/2,
C=k^2(z/K+sigma), H=H0-nC,
D={C,H0}=k^2[p_z/(Ka)+p_sigma/b],
S={C,D}=k^4[1/(K^2 a)+1/b]>0,
E={D,H0}=k^4[z/(K^2 a)-(K+gamma k^2)sigma/b].
```

The full scalar constraint chain is

```
p_n -> C -> D -> F=E+nS.
```

The four-constraint bracket matrix has determinant `S^4`, strictly positive. Preservation of F then determines the multiplier dot n. Thus these are four second-class constraints in the six-dimensional scalar phase space, leaving **one** scalar degree of freedom.

Pull back the canonical one-form to z=-K sigma: the reduced momentum is `p_reduced=p_sigma-Kp_z`. Solving D=0 yields exactly

```
H_reduced = p_reduced^2/(2Q) + gamma k^4 sigma^2/2,
Q=K(2+3beta)/beta+eta k^2,
omega^2=gamma k^4/Q.
```

This independently recovers the quadratic dispersion and positive Hamiltonian. It supports the restricted scalar calculation; it does not certify the global nonlinear five-mode assertion. The k=0 sector is excluded from this calculation and must be treated separately. No nonlinear first-class closure is inferred from a linear count.

## 6. What this changes about the route forward

The useful part of the previous response-scale calculation survives as a property of the flat quadratic model. What fails is its promotion into a certified complete parent based on eight first-class constraints.

The next mathematical obligation is precise: find a nonlinear admissible branch satisfying `partial_i(N^2 A^i)=0`, derive the rest of its preservation chain, and establish that the branch includes both an expanding background and finite-stiffness polarized galaxy solutions. The zero vector A=0 is sufficient but cannot be imposed by hand as a new three-component constraint without checking its preservation and mode cost. Likewise, a divergence-free A at one time does not prove it stays so.

This separates two distinct tasks:
- a consistent dynamical gravity/polarization sector;
- a conserved interaction that selects the cold-sector sourcing fraction.

Even a successful constraint repair would not supply the second task automatically. No result here derives kappa or transfers the phenomenological shear fit to a physical parent.

## 7. Source check and overlap

Primary source read in full relevant section: Bellorin and Restuccia, *On the consistency of the Horava Theory*, arXiv:1004.0055v3, 27 February 2012, equations (8)-(18), https://arxiv.org/html/1004.0055v3.

The notation dictionary is lambda=1+beta; their trace momentum is a density as ours is. Their pure-gravity preservation equation (11) is div(N^2 grad pi)=0. Their boundary assumptions permit a positive integral argument reducing this to a trace constraint, followed by a separate lapse equation. This verifies the pure-gravity part of our formula after the normalization mapping. Their theorem does not include P or the clock-charge term, so its reduction to the pure trace constraint cannot be imported into this model. The general method and pure-gravity obstruction are known. The P-coupled flux and explicit rotating-current witness are derived here; no comprehensive novelty claim is made.

## 8. Evidence and limits

- `preservation_checks.py`: symbolic Euler-derivative comparison, independent curvature, full 3D P-gradient derivative, exact constraint-satisfying witness and orbit multiplier.
- `linear_dirac_checks.py`: complete finite-mode scalar constraint chain, Dirac determinant, canonical reduced Hamiltonian.
- Frozen scope and post-probe scope extension: `PRESERVATION_CONTRACT.md`.
- Validated-run manifests and logs are in `preservation_run/` and `linear_dirac_run/`.
- Mutation removes the metric/divergence cross contribution; expected to fail the bracket identity.

This is self-reviewed mathematics with explicit symbolic checks. It is not independent referee approval, a full nonlinear existence proof, or an observed new force. The overall research objective remains open.

## 9. A constructive spherical continuation

There is a useful restriction stronger than merely announcing a missing calculation. Let a regular spherically symmetric slice have areal metric

```
h_ij dx^i dx^j = ell(r)^2 dr^2 + r^2 dOmega^2,
P_i dx^i=P_r(r) dr.
```

Write the ordinary (weight-zero) momentum fields as `p^ij=pi^ij/sqrt(h)`, `p=h_ij p^ij`, `e^i=Pi^i/sqrt(h)`, and `a^i=A^i/sqrt(h)`. Spherical symmetry gives only a^r. Preservation becomes

```
partial_r [N^2 ell r^2 a^r]=0.
```

A smooth regular centre, finite positive lapse, and no central point source/sink require the integration constant to vanish. Therefore **a^r=0** throughout the connected positive-lapse region. This is a consequence of preservation plus the boundary condition, not a discretionary three-component constraint. It does not extend automatically to nonspherical geometries or singular centres.

Since F_ij=0 in this sector, the exact relation is

```
P^r partial_r e^r
 + [f'/eta + P^r partial_r ln(ell r^2)] e^r
 = -[2beta/(2+3beta)] ell^(-2) partial_r p
   -4K f'[(1-c_beta)p P^r-2p^rr P_r].
```

It is a first-order radial equation for the polarization momentum on a nonzero-P background. At P=0 it reduces smoothly as an equation to the algebraic relation

```
e^r = -eta [2beta/(2+3beta)] ell^(-2) partial_r p.
```

Time-symmetric static data with all momenta zero satisfy this preservation condition automatically. That is a necessary check only; H_perp and the static field equations must also hold. The equation's differential order changes at zeros of P^r, so existence/uniqueness across such points is a real next obligation, not a solved one.

This gives a more economical next route than adding an arbitrary repair term: construct regular spherical initial data satisfying this relation and the ordinary constraints, preserve it once more to obtain the lapse equation, and test the resulting reduced kinetic energy about a finite-stiffness galaxy solution. Only after that can one assess whether the original action itself has a useful evolving branch. The cold-sector selector remains an additional missing mechanism.

Verification completed: preservation suite **9/9**, linear Dirac suite **9/9**; both manifests validate with run status `completed`. The metric-cross-term deletion mutation fails exactly the full reduced bracket identity (**8/9**, expected exit 1). Mutation output is an explicitly separate diagnostic, not a validated-run manifest. The spherical relation is an analytic consequence of the displayed divergence equation and regular-centre boundary condition; it has not been used in a numerical evolution. Self-proofreading checked symbol distinctions (density Pi versus weight-zero e, beta coefficient, lapse versus smearing), signs, assumptions and scope. No final nonlinear mode count is asserted.
