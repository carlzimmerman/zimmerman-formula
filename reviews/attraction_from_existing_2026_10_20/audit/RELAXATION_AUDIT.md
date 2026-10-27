# Independent audit of existing gravitational relaxation

20 October 2026. Normalized target: starting with the specified reciprocal
two-population energy, can eliminating the retained stable orbital radii make
the exact three-occupation energy difference negative enough for the declared
`(1,4,2)` finite-state count, after all canonical field costs are counted?
Does that construction identify an actual physical memory?

**Primary verdict: incomplete, with the smallest missing implication being a
physical occupation dictionary and its conversion/receiver law.**
The narrower spatial-control calculation in `relaxation/RESULT.md` §§1–6
passes the independent analytic reconstruction below. It establishes a
negative finite energy difference for an imposed inner profile with two
stable retained orbital radii. Its later supported continuation, audited in
§8, additionally supplies genuine stationary inner radial minima with fixed
rank actions, removes the artificial support reaction, and proves an exact
finite energy threshold. Neither construction supplies a physical transition
between different tethered-mass sectors or the required Gibbs state count.

The exact relaxation bytes audited have SHA256
`e2e2d6223851737defd65ca5c7ec67b46711e16c5a182cf97ee3f090ca4165af`.
The supplemental scalar and conservation-join reviews below have separate
hashes. `provenance.json` records read inputs and review scope. No source,
campaign, job, or Git state was changed by this auditor.

## 1. Claim card and dependency graph

The coefficient domain is real, with `G,a0,m,M0,M_h,j_h,j_f,a,theta>0`,
`L*>0`, `n=0,1,2`, and outward-positive acceleration. The inner prescribed
tethered mass is `mn`; the outer free stock is `m(2-n)`. The geometry must
satisfy `a<q_n<R_n` wherever the free shell is present; the empty-stock
endpoint has no `R` responder. The uniform inner source must satisfy
`2epsilon=2Gm/(a0 a²)<1`. The controlled energy uses a single polarization
field and counts each ordinary gravitational pair once.

The implication graph is:

1. Canonical S2 stiffness convention and the separately declared reciprocal
   two-population energy → the mechanical functional (2).
2. That energy and strict shell ordering → the host/free radial potentials.
3. Conserved positive orbital actions and interior radial minima → the
   exactly minimized shell energies and their finite second differences.
4. The imposed uniform-ball source and canonical branch → exact nonzero
   stiffness and convergent full-remainder energies.
5. The sum of those three energy differences → (15), with no extra critical
   self-energy or separately counted free-halo term.
6. Declared multiplicities and a freely available linear bias → the exact
   thermal energy hurdle `U_pair<-3theta ln 2`.
7. The continued convex rank-action functional, shifted barriers, and exact
   finite bounds → stationary supported radial states meeting the energy
   hurdle; see §8.
8. An inherited occupation dictionary, conversion law, receiver, state count,
   and full required stability → actual memory. This final leaf is absent.

Leaves 1–7 are source conventions or internal derivations. Leaf 8
is an unchecked physical assumption, not supplied by the earlier leaves. The reciprocal
extension itself is a model declaration beyond frozen S2, correctly labeled
as such in the reviewed note. No external theorem or numerical experiment is
load-bearing in this audit.

## 2. Obligation matrix

| Obligation | Status | Decisive reason |
|---|---|---|
| Fixed-total-density cancellation and zero static mixed block | passed | Only `-G(B+N)²/2` depends on ordinary total density; only the canonical terms depend on `T` at fixed `N`. |
| Canonical tether Hessian, including stiffness | passed | Its radial coefficient is `G[1+R'(u)]/r²>0`; stiffness is positive. |
| Stable passive Schur reduction | conditional | Valid for a differentiable nondegenerate minimizing branch on the actual constrained response space. The explicit shell blocks satisfy this. General operator statements also require a defined inverse/range, not positivity alone. |
| Host potential, self-energy factor, minimum, and finite difference | passed | Independent minimization gives exactly (6)–(8). |
| Outer free-stock cost and empty-stock endpoint | passed | Direct evaluation gives the positive (10); no zero-mass block is inverted. |
| Uniform-ball stiffness | passed | The interior and exterior gradients together give `3m²n²/(4pi a³)`. |
| Full rational remainder and its bound | passed | Positive convergent series and a unit-area second-difference weight give (13)–(14). |
| Complete controlled `U_pair` and analytic parameter region | passed | The independently reconstructed sum is (15); (17) has the stated strict margin. |
| Exact finite-state threshold | passed | The two strict endpoint inequalities have a common bias iff `U_pair<-3theta ln2`. |
| Inner stationary support in the uniform source control | not addressed | The uniform source is imposed and has no established balancing stress. The separate continuation passes a narrower rank-action radial construction; see §8. |
| Supported inner radial minima with the specified common rank actions | passed | The exact convex functional and variational sandwich supply the stated minima and curvature. |
| Removal of artificial support reaction | passed | Shifted cumulative barriers, scalar-obstacle monotonicity, and global obstacle signs prove exact compact support and no endpoint force. |
| Exact finite supported energy hurdle | passed | An upper bound on `E_inner(2m)` and lower bound on `E_inner(m)` give `U_pair<-.44279Gm²/a` in the specified finite configuration. |
| Exact common-support stiffness ceiling | passed | Convex perspective and variance decomposition give `Delta²E_inner>=gamma m²/V_ball` under fixed common actions and support. |
| Full nonspherical/phase-space stability | not addressed | The two positive radial Hessian entries certify only retained radial modes. |
| Physical conversion, receiver, finite rates, lifetime, and state count | not addressed | Those objects are absent from the mechanical functional. |
| Actual memory closure | conditional | It cannot be inferred before the preceding missing obligations are supplied. |

## 3. Independent reconstruction from the energy

### 3.1 Cancellation, coordinates, and finite-state threshold

With `N=T+F`, write the static energy as

```
H_static = -G/2 integral (B+N)^2/r^2 dr + C[T],
C[T] = G/2 integral T^2/r^2 dr
       +integral 4pi r^2 W_rem(GT/r^2) dr
       +gamma/2 integral |grad P_t|^2 d^3x.
```

Thus the `N,T` and `B,T` static Eulerian cross derivatives are exactly zero.
For radial variations preserving the canonical branch,

```
delta² C = G integral [1+R'(u)](delta T)^2/r^2 dr
           +gamma integral |grad delta P_t|² d³x,
1+R'(u) = (1-u/a0)^(-2).
```

This does not set every material-coordinate cross derivative to zero:
moving a parcel across the host shell changes the actual ordinary enclosed
mass. The source-map chain rule in §2 correctly distinguishes the two
statements. Pulling an Eulerian Hessian back along a nonlinear profile map
also needs its first-variation/second-profile-derivative term unless the
relevant constrained first variation vanishes.

Independently let `E_n-bn` be the biased finite-sector energies. The conditions
`w0>w1` and `w2>w1` for multiplicities `(1,4,2)` respectively require

```
b < E1-E0-theta ln4,
b > E2-E1+theta ln2.
```

The open interval is nonempty exactly when
`E2-2E1+E0<-3theta ln2`. The theorem concerns those multiplicities and a
freely available bias. It says nothing about their microscopic realization.

### 3.2 Host and free-shell minima

Directly integrating the ordinary enclosed-mass energy of the ordered shells
gives the host-dependent terms

```
E_h = M_h j_h²/(2q²)-G M_h(M0+mn+M_h/2)/q.
```

The host self-energy is `-G M_h²/(2q)`, explaining the factor `1/2`.
Terms involving the outer free shell are constant in `q`. With
`A_n=M0+mn+M_h/2`, differentiation gives

```
q_n=j_h²/(G A_n),
E_h,qq(q_n)=G M_h A_n/q_n³>0,
E_h,nq(q_n)=G M_h m/q_n²,
E_h*(n)=-G² M_h A_n²/(2j_h²).
```

It follows, without a local-quadratic approximation, that

```
Delta² E_h* = -G² M_h m²/j_h².
```

Its magnitude is `Gm²(M_h/A0)/q0<2Gm²/q0`. Consequently the necessary
stiffness scale inequality (8a) is correct. It prevents an arbitrarily large
negative curvature from being obtained by increasing the host mass at fixed
geometry.

The complete outer-shell energy is

```
E_f = m(2-n)[j_f²/(2R²)-G(D+mn/2)/R],
D=M0+M_h+m.
```

For `n<2` its minimum occurs at `R_n=j_f²/[G(D+mn/2)]` with positive radial
Hessian. Its three minimized values are

```
E_f*(0)=-G²mD²/j_f²,
E_f*(1)=-G²m(D+m/2)²/(2j_f²),
E_f*(2)=0.
```

Hence `Delta² E_f*=G²m²(D+m/4)/j_f²>0`. The last value is the energy of an
empty stock, not a radius minimum of a zero-mass oscillator. At a common
fixed `R`, direct differentiation instead gives `+Gm²/R`, also as stated.
The ordered-shell radial Hessian is diagonal in `(q,R)` because the outer
shell potential is constant throughout its interior.

The local free-shell mixed derivative is independently
`B_f=Gm²(2-n)/(2R_n²)`. Its Schur subtraction yields

```
E_f*''(n) = G²m²[D-m/2+3mn/4]/j_f²,
```

which agrees both with differentiating the exact cubic minimized energy and
with (19a). This checks an additional finite/local consistency condition.

### 3.3 Stiffness and full remainder

For the uniform ball, the polarization field is `C r/a³` inside and
`C rhat/r²` outside, with `C=mn/(4pi)`. It is continuous at `r=a`; its weak
gradient has no delta function. The interior integral of `|grad P|²` is
`m²n²/(4pi a³)` and the exterior integral is `m²n²/(2pi a³)`. Their sum is

```
integral |grad P|² d³x = 3m²n²/(4pi a³)
                      = integral rho_t² d³x.
```

Using the independently read canonical value `gamma=2pi G L*²` gives
`Delta² E_stiff=(3/2)Gm²L*²/a³`. Dropping the exterior gradient would give
the wrong coefficient. A thin tethered mass shell would instead make `P`
discontinuous and would not belong to this finite-stiffness domain.

Integration of `K W_rem'=u²/(a0-u)` with `W_rem(0)=0` gives
`a0²[-ln(1-x)-x-x²/2]/K`. Inside the ball `x=epsilon n r/a`; outside,
`x=epsilon n a²/r²`. Integrating the positive powers of the logarithmic
series gives exactly

```
E_rem(n)=a0² a³/G sum_(k>=3) (epsilon n)^k/k
                       [1/(k+3)+1/(2k-3)].
```

Uniform convergence is available on `0<=n<=2` when `2epsilon<1`.
The `k=3` term has second difference `G²m³/(a0 a³)`. Every later term has
positive second difference. Also

```
E_rem''(n)=Gm² integral R'(GmnH_a/r²) H_a²/r² dr,
integral H_a²/r² dr=6/(5a).
```

The exact finite second difference is the integral of this derivative with
weight `n` on `[0,1]` and `2-n` on `[1,2]`. That weight has area one.
Bounding `R'` by its maximum at `r=a,n=2` gives precisely (14). Neither
the remainder nor the stiffness is set to zero in the existence criterion.

### 3.4 Complete difference and parameter region

The tethered Newtonian self-energy and positive critical term cancel before
taking any difference. The central-baryon/tethered cross energy is linear in
`n` at fixed prescribed shape. The remaining exact controlled difference is

```
U_pair = Delta² E_rem +(3/2)Gm²L*²/a³
         +G²m²(D+m/4)/j_f² -G²M_hm²/j_h².
```

This is (15). Adding another positive critical pair cost to this geometry
would double-count the canceled tethered self-energy. Adding another
tether/free or free self-energy would likewise double-count (9).

In (17), `M_h=2M0` and `q0=2a` give the exact negative coefficient
`-Gm²/(2a)`. The three positive costs are bounded respectively by
`0.005`, `0.015`, and `0.01001`, in units `Gm²/a`. The bound on the first
cost follows from `(6/5)[(1-.002)^(-2)-1]<.005`. Therefore
`U_pair<-0.46999Gm²/a`, with the stated thermal margin. The ordered geometry
also holds: `q2=2a/(1+m/M0)>a`, `q_n<=2a`, and every nonempty free orbit is
outside `99a`.

The dimensionless version (16a), the condition
`lambda>1+2m/A0`, and the necessary bound
`a³>(3/4)L*² q0` have the correct factors and dimensions. They are conditions
on physical state inputs, not parameter-free predictions for a supplied
memory site.

## 4. What does not follow

An imposed extended density with zero inner kinetic support is not generally
a stationary solution. The supplied calculation minimizes only `q,R`; it
does not minimize the inner source shape and actions. Strict energy margins
can survive smoothing of the prescribed profiles, but smoothing alone does
not supply missing stationary support or full stability. The later
continuation supplies radial support by explicitly retaining conserved
circular actions; this is an additional proved construction, not a
retroactive stationary interpretation of the uniform source.

Separate collisionless tethered/free inventories cannot change merely
because their different-sector energies are favorable. The mapping from a
spatial transfer to an occupation reaction, the receiver of released energy
and any transferred response charge/actions, and the correct internal count
remain absent. At finite temperature, tracing orbital responders also adds
their occupation-dependent density of states; their minimum energies alone
are not the completed constrained free energy. The note explicitly leaves
this measure and the empty-stock limit open.

The supported radial continuation in §8 discharges that specific mechanical
gap for a constructed action family. The cheapest remaining physical check
is to identify the occupation projectors and transition/receiver in a single
inherited model and count their actual states and free energies. No universal
sign no-go follows from the co-located Eulerian cancellation, and no actual
latch follows from the constructed spatial-binding sign.

## 5. Supplemental independent scalar audit

The reviewed `scalar/RESULT.md` SHA256 is
`5594de2366e5509160a682a41f2765eff091b04847d5a17601c9fef617a311b2`.
This supplemental check reconstructed the finite-mode claims from the raw
normal-ordered Hamiltonian, rather than treating the author's verdict or
symbolic runner as evidence of the physical identification.

For `h=Delta n_b+eta(b†a²+a†²b)+kappa a†²a²`, the bosonic ladder factors give
exactly the stated `Q=2` matrix with diagonals `(2kappa,Delta)` and off-diagonal
`sqrt(2)eta`, and the `Q=4` matrix with diagonals
`(12kappa,2kappa+Delta,2Delta)` and off-diagonals
`(sqrt(12)eta,2eta)`. No mode-independent daughter/source multiplicities
`(1,4,2)` arise from those three bare Fock vectors.

For `kappa>0`, real `Delta`, and `eta!=0`, write `e=min eig(h2)`. Then
`e<min(2kappa,Delta)` and `2eta²=(2kappa-e)(Delta-e)`. The endpoint pivots of
`h4-2eI` are positive, and direct scalar elimination gives

```
S = (Delta-e)[1-3(2kappa-e)/(6kappa-e)]
  = 2e(Delta-e)/(6kappa-e),
det(h4-2eI)=8e(Delta-e)².
```

Completing the endpoint squares shows two positive inertia directions and
one direction with sign `e`. Thus the exact sign theorem holds also when
`Delta<=0`; a determinant sign alone would not have been enough. The
decoupled `eta=0` exception is correctly excluded. The proposed trial vector
has Rayleigh quotient `S/[1+12eta²/A²+4eta²/C²]`, so (7) is a valid upper
bound on `E4-2E2` when `e<0`.

The contact matching identity follows directly by subtracting the retained
positive-frequency exchange once and the analytic negative-frequency
correction once. At the same finite regulator,
`kR-c3²/delta=lambda_rep/(4m²)>0`. For flat space and `z<=0`, the source
resolvent is bounded above by `1/delta`, giving (2). This excludes a negative
flat pair eigenvalue in that stated finite-regulator NR model.

Independent elementary radial integration of normalized Coulomb 1s functions
gives `I4=1/(8pi ad³)`,
`I3=8ab^(3/2)/[sqrt(pi)(ad+2ab)³]`, and
`rho=512beta³/(beta+2)^6`. Together with the stated one-body energies, the
interval (9) follows. These are exact formulas for that projected Coulomb
control; they do not instantiate an inherited physical host. The final text
correctly qualifies the full-Q2 variational transfer: a common finite
regulator, its exact daughter ground orbital, its consistent matrix elements,
and a checked strict negative margin are required. The continuum overlap
formulas alone are not a definition of a 3D contact Hamiltonian. The final
text also correctly refrains from transferring projected charge-addition
curvature to the full-mode `E4-2E2` difference by separate upper bounds.

At fixed `Q=4`, direct subtraction of the bare diagonal source-count energies
gives `8kappa>0`. The additional zero-temperature endpoint test also passes.
After making off-diagonals negative, the irreducible tridiagonal ground
vector has positive components `A0,A1,A2`. If both endpoint probabilities
exceeded the middle probability, its endpoint equations would give
`(d0+d2)/2-E<(t0+t1)/2`, while the middle equation would give
`d1-E>t0+t1`. This contradicts
`d1=(d0+d2)/2-4kappa`. The statement is only for those literal projectors at
zero temperature, as the text says.

Accordingly the finite-mode algebra passes; the full-field host transfer is
conditional on the stated regulated input; and memory closure is still
missing the occupation dictionary and transition/receiver. No finite-
temperature projector theorem is inferred.

## 6. Supplemental conservation-join check

`CONVERSION_JOIN.md` SHA256
`152acee6832f0b9aaa6ee5b88be3c8c3cd04cdea355c641945b537d85526ea94`
passes its scoped conservation argument. Under the stated regularity and
no-flux boundary assumptions, each phase-space Poisson bracket integrates
to zero even for self-consistent density-dependent Hamiltonians. An added
reciprocal density attraction changes the Hamiltonian, not the separate
Vlasov number-conservation identities. Number-preserving elastic collision
operators preserve the same conclusion.

In the displayed static density-bath model, the mutually commuting `n_i`
commute with all bath operators and with `E_loc(n1,n2)`, so `[n_i,H]=0`.
Eliminating that bath cannot produce a missing occupation-changing operator.
An original mode-exchange kinetic term would change this conclusion and must
be retained; the note expressly allows that case. It also correctly allows
subregion mass flux and orbital memory, to which separate total-species
conservation is no obstruction. The scalar reaction preserves a different
`Q`; it does not by itself provide the missing canonical label map.

## 7. Source, computation, and review provenance

This is a separate-agent independent reconstruction from actual energy and
Hamiltonian definitions. It is not a blind external referee certificate: the
auditor could read the submitted notes and later received coordinator
messages identifying additional scalar claims and regulator concerns. Those
claims were recomputed from the raw matrices/equations. The relaxation
derivation was reconstructed before the scalar sign summary was supplied.

Sources were inspected with `cat`, `sed`, and `rg`; SHA256 was computed with
Python standard-library `hashlib`. No simulation, parameter scan, fit,
symbolic calculation, scientific run, or owner-job operation was executed by
this auditor. The scalar author's completed `run_002` manifest and source
were inspected only as supplementary provenance; the displayed analytic
derivations carry this audit. The successful run's exact algebra checks do
not test occupation identification, stability, a regulated host, or memory.

No applicable `AGENTS.md` or `.mathbox` ledger was found along the workspace
and review ancestry inspected. The project worktree is shared and dirty;
the assessment commit is historical context, while the hashes above identify
the actual reviewed proofs. Earlier draft wording was corrected by the
author before the pinned relaxation review: the Schur criterion now states
a sufficient stable-branch condition, and the endpoint geometry correctly
uses `q_n<=2a`.

## 8. Supported continuation, support removal, and exact bounds

The supplemental reviewed files are `SUPPORTED_CONTINUATION.md`,
`BARRIER_PROOF.md`, and `BOUNDS.md`. Their exact hashes are recorded in
`provenance.json`. These files close the initially missing radial support
step, without closing the physical memory join. The following checks are
analytic and independent of any numerical experiment.

### 8.1 Convex radial functional and variational sandwich

For noncrossing circular shells labeled by enclosed-mass rank, direct
integration by parts gives

```
K_t = z integral_0^1 j(s)^2/[2r(s)^2] ds
    = z integral J(H(r))/r^3 dr,
J(s)=integral_0^s j(v)^2 dv.
```

The outer `H=1` tail is necessary for this identity. Cancellation of the
tethered Newtonian self-energy against its critical term then gives exactly
`E_z=zA+z²S+V_z` in the continuation. Variation gives its (3), including the
coefficient `-gamma z(rH''-2H')/(4pi)` and the corresponding material force
`-gamma partial_r rho_t`. Its second variation is the stated sum of positive
action, stiffness, and rational-remainder terms.

For the actual quantile choice `j(s)²=GM0 r0(s)`,
`j²'(s)=GM0/H0'(r0(s))>=GM0/max H0'>0` in the interior, understood by
limits at the endpoints. This supplies the strong convexity used in the
proof. The generic phrase that strict increase alone makes a derivative
strictly positive needs this qualification; strict increase by itself is
not such a derivative theorem. It does not affect the chosen quantile
family, and positive stiffness already supplies strict finite-mass radial
shape energy for nonzero fixed-endpoint variations.

On the fixed finite annulus, the direct-method existence argument is valid:
the positive gradient term bounds the `H1` norm, constraints are weakly
closed, all potentials are convex and continuous below a common saturation
margin, and strict convexity gives uniqueness. Uniformly for small `z`,
the remainder is `O(z³)`, including its outer tail.

The sandwich proves more than a formal perturbation:

```
zA0+z²S[H_z] <= E_inner(z) <= zA0+z²S0+O(z³).
```

First it bounds `A[H_z]-A0=O(z)` and `S[H_z]<=S0+O(z)`. The strong convexity
gap gives `H_z -> H0` in `L2`; bounded gradients give weak `H1` compactness.
Lower semicontinuity then gives `S[H_z]->S0`. Substitution into the same
sandwich yields `A[H_z]-A0=o(z)` and
`E_inner(z)=zA0+z²S0+o(z²)`. Hence
`Delta²E_inner=2m²S0+o(m²)`, with no unjustified differentiation of the
minimizer or singular implicit-function argument. These steps pass.

### 8.2 Exact support by shifted barriers

For `Hplus=H0(r+e)` and `Hminus=H0(r-e)`, the endpoint extension of the rank
action gives

```
j(Hplus)²-GM0r >= GM0e       where Hplus<1,
j(Hminus)²-GM0r <= -GM0e     where Hminus>0.
```

The stiffness residual is bounded by `gamma z M/(4pi)`, and the full
remainder residual multiplied by `r³` is bounded by
`G²z²/[l(a0-Gz/l²)]`. The explicit smallness condition (2) therefore gives
the correct strict super/subsolution signs, including the relevant obstacle
plateaus. Its dimensions are those of specific angular momentum squared.

The weak positive-part comparison is valid. The difference of gradient
pairings contributes `gamma z integral |w'|²/(4pi r²)`, and both local
nonlinear terms have nonnegative difference pairing. The comparison test is
admissible already in the larger scalar obstacle class, without presuming
monotonicity of the unknown minimizer. Thus
`Hminus<=H_z<=Hplus`, and this proves exact flat neighborhoods, not only norm
convergence:
`H_z=0` for `r<=a/2-e`, and `H_z=1` for `r>=a+e`.

The larger-class monotonicity check also passes. In the one-dimensional
uniformly elliptic obstacle problem, bounded continuous reaction gives the
stated smooth fit; on active intervals the Euler equation gives ordinary
second derivatives. The function

```
F(r,H)=j(H)²-GM0r+r³R(GzH/r²)
```

increases strictly in `H` and decreases strictly in `r`, because
`3R(v)-2vR'(v)=-v²(a0+v)/(a0-v)²`. A downward segment would force a preceding
maximum with `F<=0` and a later smaller minimum with `F>=0`. Strict
monotonicity instead gives the maximum's `F` larger, a contradiction.
The scalar minimizer is therefore a physical monotone cumulative.

Outside the finite annulus, the constant extension has a positive
lower-obstacle variation and negative upper-obstacle variation under the
same smallness condition. The flat neighborhoods exclude a boundary
distribution from the stiffness derivative. The local scalar obstacle
inequality and these exterior signs imply a global obstacle variational
inequality even for variations changing the old annulus traces. Convexity
then proves the unique global radial minimum with the fixed rank actions.
Exterior spherical shells have constant potential over the inner support;
beyond them their additional inward force reinforces the required upper-
obstacle sign. The resulting shape/exterior-radius mixed blocks vanish
locally as long as the proved strict separation is retained.

This closes the mathematical support/reaction gap. It certifies the retained
rank-preserving spherical directions, not nonspherical modes, shell crossing,
or action redistribution.

### 8.3 Exact finite sufficient bound

The finite upper bound uses the correct directions of variational bounds:
`E_inner(m)>=mA0`, while the common tracer trial gives
`E_inner(2m)<=2mA0+4m²S0+V_(2m)[H0]`. Therefore

```
Delta²E_inner <= 4m²S0+V_(2m)[H0].
```

For the tracer supported outside `a/2`, `u(2m)/a0<=8epsilon`. Positivity of
the exact remainder series gives
`W_rem(u)<=u³/[3Ka0(1-8epsilon)]` and
`integral H0³/r⁴<=8/(3a³)`. Consequently

```
V_(2m)[H0] <= 64G²m³/[9a0a³(1-8epsilon)].
```

Since `S0<G L*²/a³`, these imply the exact finite bound (4) in `BOUNDS.md`.
With its stated finite-configuration convention
`j_f²=100G(M0+M_h+m)a`, the free cost is less than `0.01001Gm²/a`.
At `a>=10L*`, `epsilon<=.001`, and `m/M0<=.01`, the inner cost is less than
`(.04+.0072)Gm²/a`. Combining the exact host curvature `-.5Gm²/a` gives
`U_pair<-.44279Gm²/a`, as stated. This survives the positive temperature
range in that note. The barrier condition at `z=2m` enforces actual support
separation and is simultaneously satisfiable by sufficiently small `m`.

For the finite convention just displayed, the outer action is set after
choosing `m`. For a family with the outer action held instead at its `m=0`
value, the free bound at `m/M0<=.01` is `0.010042` rather than `0.01001`;
the weaker displayed `U_pair<-.442Gm²/a` still holds. These two conventions
must not be mixed in the stronger numerical bound.

### 8.4 Exact shape-relaxed stiffness ceiling

The perspective argument in `BOUNDS.md` also passes. With common fixed
`J`, common support ball of volume `V`, and `T=zH`, the orbital term
`zJ(T/z)` is jointly convex. The central potential is linear in `T` and the
full remainder is convex in `T` on its convex canonical domain. Moreover,
under the linear mass constraint `integral rho=z`,

```
gamma/2 integral rho² - gamma z²/(2V)
  = gamma/2 integral_ball (rho-z/V)²
```

is jointly convex in `(z,rho)`. Partial minimization over the jointly convex
density constraints preserves convexity. The zero-mass perspective endpoint
is its closed value at `(z,T)=(0,0)`. Therefore

```
Delta²E_inner >= gamma m²/V
               = (3/2)Gm²L*²/a_s³.
```

Using the exact host bound and positive free-stock curvature gives

```
U_pair > Gm²[-2/a_s+(3/2)L*²/a_s³] >= -8Gm²/(9L*).
```

The scalar minimum occurs at `a_s=3L*/2`. Thus the necessary condition
`theta<8Gm²/(27 ln2 L*)` and, if `theta=m sigma²` is additionally declared,
the mass bound in (10) follow with the stated strictness.

This ceiling requires the same action function, common compact support, and
complete inner energy across the compared sectors. It is not a theorem for
changing action distributions, added nonconvex interactions, or a different
occupation dictionary. The barriers provide the required common ball for
the specific small-mass constructed family. No collisionless dispersion is
automatically a Gibbs temperature.

The supported continuation and its exact finite bounds strengthen the
mechanical result substantially. The remaining gap is now physical: the
constructed action families do not identify a microscopic memory occupation,
the `(1,4,2)` trace, a conversion and receiver, a finite rate, or a lifetime.
