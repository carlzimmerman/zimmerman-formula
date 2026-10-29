# Independent PN28 review: reduced EOS, finite halo and core limit

Reviewer: `/root/theory_audit`, 2026-10-28. This review reconstructs the
equations from their stated assumptions; it does not use agreement between
agents or numerical pass flags as mathematical evidence. The proof-audit and
mathematical self-review workflows were applied. No external theorem or
literature attribution is needed for the arguments below.

## Frozen inputs and scope

Requested base: `66c45c5082f651dd54e171f98c11acd9cb3d9086`.
Observed HEAD when reading and freezing this review:
`7954d48377463cafcae3e8dbb09454134aef384f`. These PN28 inputs are new working-tree
files, not files supplied by that requested commit. Concurrent work was not
modified. SHA256 identifies the actual reviewed text:

| Input | SHA256 |
|---|---|
| `../dispersion_coupling/EOS.md` | `05f919345cb73c8b96e3f07d5fdb421ae8ee1d24a01e177abc9551aab4092274` |
| `../halo/DERIVATION.md` | `aa79f50d4b78ce204a805f4962e53b87778ed7a17d8ec5e30a7be3bea529991a` |
| `../dispersion_coupling/REPORT.md` | `c4046a7d35128321f5d3a7c0fdef0f92b50ab68c2a27a5cb23d82506ef9391ae` |

The first two files are the primary targets. The action report was read later
for a bounded check of its canonical variables, pressure interpretation and
the physical assumptions needed at the halo edge. Its entire kinetic/PDE
program is not certified here. The independent relativistic mixing report
`RESULT.md` was already frozen at
`6bf0e92001dea29a83f01b41f4ba788d8bcfd1bb1d8600eefc1150b7712f7e0d`;
its conclusions are not premises for this review.

**Primary verdict: proved as written, within the declared reduced model.**
The exact EOS, finite radius for every regular central state, and asymptotic
quarter-density column follow analytically. The expansions and continuous
dependence step can be completed as below. This verdict does not turn the
model assumptions into microscopic derivations, certify a finite-gradient
halo, or determine the vacuum-normalized amplitude. The displayed decimal
for the reference crossing is not independently interval-certified here;
the theorem uses the crossing defined by its ODE.

## 1. Reconstructing the pressure rather than importing a kinetic closure

Fix a canonical waterbag level and particle number. In the conventions of
the displayed integrals, momentum is momentum per unit particle mass and
the phase distribution integrates to mass density. Equivalently, fixed
particle-mass factors may be restored throughout. A homogeneous isotropic
compression with linear scale factor `a` gives

    rho proportional to a^-3,  p_F proportional to a^-1,
    K=(1/2) integral f p^2 d^3p=(3/10)rho p_F^2
      =k rho^(5/3).

This is a declared fixed-level isotropic state or canonical affine
compression family. It does not assert that a generic evolving cold-stream
distribution stays a local waterbag or isotropic.

For `W=K exp(-2s)+V+B[exp(3s)-3s-1]`, its second derivative is strictly
positive, and it diverges at both ends of the real s axis. Its unique
minimum has s>0 for K>0 because `W_s(0)=-2K`. With `y=exp(3s)`:

    2K y^(-2/3)=3B(y-1),
    E_rel=(3B/2)(y-1),
    W_min-V=B[(5/2)(y-1)-ln y].

The envelope derivative is `dW_min/dK=exp(-2s)`. If `Q` is the physical
cell volume, the complete cell energy is `Q W_min(K(Q))`. Since
`dK/dQ=-(5/3)K/Q`, its volume derivative gives

    P_total=-d[Q W_min]/dQ
           =(5/3)K W_min,K-W_min
           =(2/3)E_rel-U(s),
    P_total+V=B ln y.

Thus the pressure is indeed the full matter-plus-scalar stress on this
branch. It is not just a redefinition of the bare velocity moment. In the
changed kinetic metric, the conjugate isotropic kinetic stress is
`P_kin=2E_rel/3=B(y-1)`, whereas the ordinary velocity moment would be
`2K_v/3=P_kin/Z`. Neither alone equals `B ln y-V`.

The stationary constraint and waterbag relation give exactly

    rho/rho_*=y^(2/5)(y-1)^(3/5),
    d ln rho/dy=(5y-2)/[5y(y-1)],
    dP_total/d ln rho=5B(y-1)/(5y-2)>0.

The low-density coefficient and the logarithmic high-density limit in
EOS.md follow. Positive compressibility establishes a local reduced
mechanical property, not halo stability or maintenance of the phase state.
The permitted `exp(6s)` deformation balances against `K exp(-2s)` at
`exp(8s) proportional to K`; hence `W_min proportional to K^(3/4)` and
`P+V` has leading power `rho^(5/4)` with positive coefficient. The stated
non-universality of the logarithmic shape is correct.

## 2. Exact enthalpy and regular reduced halo

Set `t=1-1/y`. Direct substitution gives

    rho/rho_*=t^(3/5)/(1-t),
    dP_ex/rho=(B/rho_*) t^(-3/5) dt,
    h=(5B/(2rho_*)) t^(2/5).

Consequently `psi=t^(2/5)` and the length
`ell^2=5B/(8pi G rho_*^2)` give exactly

    psi''+2psi'/r=-f(psi),
    f(psi)=psi^(3/2)/(1-psi^(5/2)),
    0<psi_c<1,  psi(0)=psi_c,  psi'(0)=0.

The scale factors and powers in the source are correct. On `[0,psi_c]`,
f is bounded and continuously differentiable, including at zero. Its
regular integral equation is

    psi(r)=psi_c-integral_0^r (s-s^2/r) f(psi(s)) ds.

Local contraction on a sufficiently short interval proves existence and
uniqueness at the apparent singular center. Substitution gives
`psi=psi_c-f(psi_c)r^2/6+O(r^4)`; positivity of psi_c permits the higher
local smoothness needed for that remainder. With
`m=integral_0^r s^2 f(psi(s)) ds`, one has `psi'=-m/r^2<0` away from
the center. There is no continuation obstruction while psi is positive:
the state lies in the bounded source interval and any positive-radius ODE
point is regular. This covers each fixed central state in the stated open
interval. It does not include the singular endpoint `psi_c=1`, and
`psi_c=0` is the trivial zero-density solution.

## 3. The finite-radius contradiction is valid for every such state

Suppose the regular solution remained positive for all r. Its decreasing
limit L exists. If L>0, then f stays bounded below by a positive number,
so `m(r)` grows at least cubically and `psi'=-m/r^2` forces a zero.
Therefore L=0. Integrating the exact derivative to infinity now yields

    psi(r)=integral_r^infinity m(s)/s^2 ds >= m(r)/r.

No independent assumption about convergence of this improper integral is
needed: the integral equals the finite difference `psi(r)-L`.
For `0<=s<=r`, monotonicity of psi and `f(q)>=q^(3/2)` imply

    m(r)>=r^3 psi(r)^(3/2)/3,
    psi(r)>0  ==>  psi(r)<=9/r^4.

For fixed r0>0, however, `m(r0)>0` and the same integral identity gives
`psi(r)>=m(r0)/r` for all r>=r0. The two bounds contradict one another
for large r. Thus the first zero R is finite. Bounded density implies
finite mass, and `psi'(R)=-m(R)/R^2<0`. The simple zero and the small-psi
EOS give `rho proportional to (R-r)^(3/2)` and
`P_ex proportional to (R-r)^(5/2)` with positive leading constants.

Matching `P_total=-V` to a constant exterior vacuum pressure is consistent
inside this auxiliary, Newtonian model. It is not a matching theorem for
the finite-gradient parent field equations.

## 4. Completing the quarter-core convergence argument

Write `n=rho_c/rho_*=f(psi_c)` and use the central length
`L_c^2=B/(4pi G rho_c^2)`. The stated transformation gives exactly

    v=(5/2)n(psi_c-psi),
    v''+2v'/z=d_n(v),
    d_n(v)=f(psi_c-2v/(5n))/n,
    v(0)=v'(0)=0.

Expansion near psi=1 gives
`psi_c=1-2/(5n)+O(n^-2)`. On each fixed interval `0<=v<=M`,

    d_n(v)=1/(1+v)+O(n^-1),
    d_n'(v)=-1/(1+v)^2+O(n^-1),

uniformly. The second formula follows directly by differentiating f;
its numerator is `(3/2)sqrt(psi)+psi^3`, divided by
`(1-psi^(5/2))^2`, and the chain factor is `-2/(5n^2)`.
Thus the needed Lipschitz bounds are uniform, not merely pointwise.

For any fixed z interval and sufficiently large n, the physical range of
v extends beyond that interval's possible values: its edge is
`v_edge=(5/2)n psi_c -> infinity`, while monotonicity of f gives
`0<d_n(v)<=1` and `0<=v(z)<=z^2/6`. The regular integral equation
therefore permits comparison on any fixed finite z interval. If delta is
the uniform RHS difference and L a common Lipschitz constant, its kernel
`s-s^2/z` is nonnegative and at most s. A Gronwall estimate bounds the
solution difference on `[0,z0]` by
`(delta z0^2/6) exp(L z0^2/2)`. It tends to zero; derivatives also
converge away from zero, and their regular integral expression handles
the center.

The limit `Theta=1+v` consequently satisfies the stated equation
`Theta''+2Theta'/z=1/Theta`. It is globally regular at every finite
positive z, increases strictly, and reaches 4 at a unique finite point
xi_q. Indeed, if v stayed at most 3, the source would be at least 1/4
and `v>=z^2/24`, a contradiction. Its crossing derivative is positive.

For a finite n the quarter-density condition is `d_n(v_n(z))=1/4`,
not exactly `v_n=3`. Uniform convergence of both factors makes this
condition converge to `1/(1+v(z))=1/4`; the limiting derivative is
`-v'(xi_q)/16<0`. Monotonicity and transversality prove convergence of
the unique finite-family crossing to xi_q. Hence

    rho_c r_(1/4) -> xi_q sqrt(B/(4pi G)).

This establishes the column theorem without numerical sampling. Its
finite-central-density coefficient remains state dependent.

## 5. Bounded action check and the physical restrictions

At fixed positive stream densities and scalar gradients, differentiate
the reported action with respect to velocities and scalar time derivative.
This gives exactly

    pi_s=F^2(s_t+u.grad s),
    p_b=u+Z w_b+(pi_s/rho)grad s.

The relative canonical momenta obey `p_b-pbar=Z w_b`. In the Legendre
transform, the two terms `pi_s u.grad s` cancel, leaving precisely the
reported positive squares for center motion, relative motion and scalar
motion. The scalar Euler-Lagrange equation has the reported source
`Z' K_v=2ZK_v`. With zero spatial gradients the conserved canonical
relative momenta give `dot E_rel=-2E_rel dot s`, exactly opposite to
the scalar energy gain. These checks support the stated local transfer
and conjugate-stress interpretation. They do not show generic relaxation
to the waterbag state.

Several restrictions are material when applying the halo result:

1. **Dominant rest mass.** At high density,
   `(W_min-V)/rho -> (5/2)B/rho_*`. Thus treating rho as the dominant
   gravitational mass and using Newtonian dynamics requires this specific
   energy to be small compared with c^2. Positivity of the reduced EOS
   does not supply that scale hierarchy.
2. **Vacuum gravity.** A constant V disappears from the pressure gradient,
   but in a conventional relativistic vacuum completion its Newtonian
   acceleration would be `8pi G V r/(3c^2)`. Its ratio to the enclosed
   matter attraction is `2V/[mean_rho(r)c^2]`. A sufficient halo-wide
   small-force condition is `mean_rho(R) >> 2V/c^2`; the reduced existence
   theorem does not impose it for all central states. This is conditional
   on that conventional vacuum completion, which this action has not
   itself established.
3. **Scalar gradients.** Let `C_s=F^2 c_s^2` be the coefficient of
   `|grad s|^2` in the reviewed action. Its static equation is
   `-C_s Laplacian s+W_s=0`. The local branch has W_s=0 but a nonzero
   spatial residual. In fact its central residual is exactly computable:

       s=-(1/3)ln(1-psi^(5/2)),
       ds/dpsi=(5/6)f(psi),
       Laplacian_phys s at center=-(4pi G/(3B)) rho_c^2.

   The local stiffness is `W_ss=3B(5y_c-2)`. The first formal
   derivative-expansion correction is therefore

       delta s_c approximately
       -4pi G C_s rho_c^2/[9B^2(5y_c-2)]
       ~ -4pi G C_s rho_* rho_c/(45B^2).

   This is a diagnostic expansion, not a solved boundary problem. It
   independently shows that fixed nonzero C_s does not permit taking
   central density to infinity while retaining local scalar elimination.
   The core theorem needs a controlled finite window or a joint limit
   when applied to the full parent. Near the vacuum edge a scalar exterior
   tail and gradient matching must also be treated separately.
4. **Zero-density exterior.** The action uses `u=j/rho` in D and the
   Hamiltonian uses `pi_s/rho`. These are defined in its positive-density
   medium. An exterior prescription or a suitable limiting formulation
   is needed before the full action supplies a halo boundary problem
   across rho=0. The reduced pressure matching alone does not provide it.

The original texts already distinguish the mathematical core limit from
physical control. The exact residual and zero-density issue sharpen the
next required calculation; they do not invalidate the reduced theorem.

## 6. Normalization and disposition

Canonical normalization gives `B=m_phi^2/(9g^2)` in the action's units.
Combining the proven mathematical core limit with the separately adopted
column identification `Sigma=a0/(2pi G)` gives
`a0^2=pi xi_q^2 G B`. Requiring
`a0=(1/2)c sqrt(G rho_Lambda)` and `V=rho_Lambda c^2` would therefore
require `B/V=1/(4pi xi_q^2)`, equivalently the reported
`m_phi^2/(g^2 V)=9/(4pi xi_q^2)`. The factors are correct.

Neither the local action, waterbag state, halo boundary condition nor
regularity singles out that ratio. B and V can still be varied
independently. This route has supplied a consistent conditional pressure
mechanism and a finite reduced halo with a proven asymptotic column; it
has not supplied independent vacuum normalization. Its next physical
test is the coupled finite-gradient halo with a defined exterior and
phase-state dynamics, rather than treating the reduced result as a
completed microscopic theory.

No reviewed input was edited. No computation was used as proof, and no
new expensive job, commit or push was performed.

## Review addendum: clarified action and static vacuum continuation

The author subsequently made the positive-density/exterior restriction
explicit in REPORT.md. I re-read its action and canonical-variable
paragraphs at updated SHA256
`ddf6da56df34842c7631e021d3840645c29a6620e50fc5a95092e752c81e8727`.
The action equations and the bounded checks in section 5 above are
unchanged; the new prose correctly states their domain. The earlier hash
is retained to preserve the review history, while this addendum covers
the clarified text.

A subsequent REPORT.md revision added the explicit high-density energy
asymptote and its density-linear-term discussion; the STATIC_WATERBAG.md
summary was already present in the preceding `ddf6da56...` revision.
The final reviewed SHA256 is
`6deea173491b9c8e4d88b528ac0895faf2c6ec99273aa86c9d6e73d7c7d8537d`.
This chronology was corrected after exact hash reconstruction by the
author; the subject hashes and substantive checks are unchanged. The
static summary accurately limits that branch to the continuation audited
below. Later report edits are outside these frozen hash claims.

I also independently reconstructed the new STATIC_WATERBAG.md equations,
SHA256 `0991516ad7331710c7d00fbfa5e1b198b70cab3220d94f949f4c1dc281760812`.
At positive density and zero mean canonical momentum/scalar momentum,
the first variation of the quadratic current term vanishes. The stated
one-particle Hamiltonian is therefore `h=p^2/(2Z)+Phi`. The global fixed
energy waterbag is stationary because its canonical Poisson bracket with
h is zero, including the distributional boundary. Its integrals give
`E_rel=(3/5)rho(mu-Phi)` in the occupied region and the same fixed-level
relation `K=k rho^(5/3)` used by the reduced EOS.

Differentiating `P_kin=(2/5)rho(mu-Phi)` and
`rho proportional to Z^(3/2)(mu-Phi)^(3/2)` gives directly

    grad P_kin=-rho grad Phi+2E_rel grad s.

The divergence of the displayed scalar stress is
`[C_s Laplacian s-U'(s)] grad s=-2E_rel grad s`. Thus their sum has
the required gravitational force, and finite scalar gradients give an
anisotropic total stress. The dimensionless substitutions also check:

    rho/rho_*=exp(3s) psi_+^(3/2),
    Laplacian_x psi=-exp(3s) psi_+^(3/2),
    alpha Laplacian_x s=exp(3s)[1-psi_+^(5/2)]-1,
    alpha=C_s/(3B L^2).

At alpha=0 these equations recover the reviewed local EOS. At alpha>0
they are a different coupled boundary problem. The explicit zero-mean
static exterior prescription supplies a defined stationary kinetic branch
and is an appropriate response to the exterior issue for that branch.
It does not make the full Hamiltonian directionally independent under
arbitrary vacuum-crossing perturbations: `|j_p|^2/rho` has a first
variation at zero that depends nonlinearly on the direction of added
phase-space mass. The new file explicitly acknowledges this limitation.
No finite-gradient solution, stability theorem or vacuum normalization
is certified by this addendum.
