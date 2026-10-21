# Focused independent in-session audit of the cooperative latch

20 October 2026. Audited author artifact: `RESULT.md`, SHA-256
`cf6f2ea2924c6662b7a7148b23acd4befadb1587633cab4438b948216113453d`
(20,704 bytes). The exact finite construction is in **Section 3**, not
Sections 6–7. Section 6 is a different kinetic-only example.

**Normalized claim.** For the declared diagonal effective Hamiltonian of
extended collective occupancy modes, with two distinguishable particles,
two distinguishable one-place sites, one free internal state per free
particle, positive `G,m,a0,r,theta,kappa`, `t_sat>2`, and an independently
added cooperative interaction `J`, there is a nonempty parameter region
with two strict endpoint modes of a unique Gibbs occupancy distribution
and a finite, exactly specified mean switching time.

**Primary verdict: proved as written within that declared finite model
(pass).** No missing mathematical hypothesis was found for this scoped
claim. It is conditional as a physical mechanism on the stated effective
energies, multiplicities, bath and transition operator. In particular this
audit does not derive any of them from canonical S2 or interpret `H(1)` and
`H(2)` as energies of one and two literal point particles.

The important physical discriminator is the required *negative occupation
pair curvature*. In this model ordinary label-independent gravity and the
convex full-remainder conversion cost do not provide it. The extra
interaction must do so. This is an additional consequence derived below,
not a claim of a universal microscopic exclusion.

## Dependencies and exact scope

The dependency graph is:

1. The displayed reciprocal spherical energy and `R(u)=u^2/(a0-u)`
   determine the fixed-position conversion difference `H`.
2. The declared extended-mode interpretation and equal reference weights,
   together with injections of labelled particles into labelled sites,
   determine the diagonal energies and multiplicities.
3. Those definitions determine the Gibbs weights, coexistence bias and
   bimodality threshold by finite algebra.
4. The separately declared nearest-neighbor Metropolis generator determines
   detailed balance and the backward first-passage equations.

Items 1–4 are not circular. The mode Hamiltonian, `J`, reference-state
counting and generator are inputs rather than consequences of canonical
S2. The separately declared continuous free energy in Section 4 has its
own calculus proof; it is not used to justify the small-count result.

The source actually checked for item 1 is
`reviews/final_closure_push_2026_10_20/reciprocity/SOURCE_RESPONSE.md`,
Sections 1–2, SHA-256
`6deb1b415ac7f5a1713754ea5526a05b878445fa8d6c7e98888114815401e173`.
It explicitly omits stiffness and states the zero-stiffness scope.
The frozen canonical statement, SHA-256
`30aa143ee1d8d2179e68d66a0b9f9e5d9437e69e5598b04a76b0d5770c649019`,
contains a nonzero stiffness term in S2. Thus “full cost” here means the
full rational remainder plus critical counterterm of the **displayed
reduced reciprocal functional**. It is not verification that a literal
thin shell has the same finite energy after every term of full S2,
including gradients, is restored. The author's collective effective-mode
qualification is essential.

All 13 working-tree files listed in the author's `source_hashes.json`
matched their declared SHA-256 values when checked. Hash agreement verifies
identity, not those sources' mathematical claims. The prior-art inventory,
original microscopic theory, empirical claims and old computation packets
were not re-audited. No external theorem is load bearing in the focused
derivations below.

## Reconstruction of the finite ensemble

An occupancy microstate consists of a subset of `n` particles, a subset of
`n` sites and a bijection between them. Free labelled particles each have
one specified free state. Consequently

```text
Omega_n = binomial(N,n) binomial(C,n) n!
        = binomial(C,n) N!/(N-n)!.
```

For `N=C=2`, the empty assignment is unique, the one-bound assignments are
the four particle/site pairs, and the two-bound assignments are the two
bijections. Thus `(Omega_0,Omega_1,Omega_2)=(1,4,2)`, not `(1,2,1)` or
`(1,4,1)`. These counts need the author's distinguishability and equal-weight
assumptions; quantum indistinguishability or additional free orbitals would
change the object.

With `H0=0`, the diagonal energies are exactly

```text
E0 = 0,
E1 = H1 - B_d,
E2 = H2 - 2 B_d - J/2,
w_n = Omega_n exp(-E_n/theta).
```

The `J/2` in `E2` follows from `C=2`; replacing it by `J` would change the
threshold. Requiring `w2=w0=1` gives

```text
E2 = theta ln 2,
B_d = H2/2 - J/4 - (theta/2) ln 2.
```

Then, with `D=J/4+H1-H2/2`,

```text
E1 = D + (theta/2) ln 2,
w1 = 2 sqrt(2) exp(-D/theta) = epsilon,
Z = 2+epsilon,
pi = (1,epsilon,1)/(2+epsilon).
```

Each endpoint has only the middle state as a neighbor, so both are strict
occupancy-probability maxima exactly when `epsilon<1`. This is equivalent
to

```text
J > 2 H2 - 4 H1 + 6 theta ln 2.
```

At equality the occupancy distribution is flat; there are no strict
endpoint maxima. Bimodality alone does not imply a long lifetime relative
to `kappa^-1`; that requires `epsilon` small. This finite distribution has
no thermodynamic phase transition.

The author's positive-bias witness also checks. Set
`B_d=H1/2` and `J=2H2-2H1-2theta ln 2`. It gives
`epsilon=4 exp[-H1/(2theta)]<1` if
`0<theta<H1/(4ln 2)`. Here `H1>0` and `H2>2H1` ensure `J>0`.
All energies remain finite for finite parameters and `t_sat>2`; an overall
constant can make the three energies nonnegative. The Newtonian gap
restriction remains a separate stated physical restriction.

For general admissible integer `N,C`, the same count gives

```text
w_(n+1)/w_n = (N-n)(C-n)/(n+1)
    * exp[(B_d + Jn/C - H_(n+1)+H_n)/theta],
```

which agrees with the author's equation (4). No continuous approximation
was needed for these results.

## The full-remainder cost and its invariant pair sign

At fixed total cold shell mass and fixed positions, the ordinary
gravitational term depending on `T+F` is unchanged by conversion. The
`+G T^2/2` critical counterterm and the remainder do change. For shell
occupation `t`, outside the shell `u(s)=Gmt/s^2`; hence

```text
H_t = m integral_r^infinity [u+R(u)] ds,
u+R(u) = a0 u/(a0-u),
H_t = m a0 b artanh(b/r),   b^2=Gmt/a0.
```

There is no separate baryon attraction in this *label-conversion*
derivative. It is not the derivative for mechanically moving the shell.
Differentiating the author's primitive (1) with respect to `b` leaves
`(2a0^2/G) b^2 artanh(b/r)`; using `db/dt=Gm/(2a0b)` reproduces `H_t`
and `H(0)=0`. Thus both the primitive and its normalization check.

Differentiating the integral gives

```text
H_tt = Gm^2 integral_r^infinity [1+R'(Gmt/s^2)]/s^2 ds,
R' = a0^2/(a0-u)^2 - 1,
R'' = 2a0^2/(a0-u)^3 > 0,
R''' = 6a0^2/(a0-u)^4 > 0.
```

It follows that `H_tt(0)=Gm^2/r`, `H_tt>Gm^2/r` for `t>0`, and
`H_tt` is increasing and strictly convex on `0<t<t_sat`. In particular

```text
H2-2H1 = integral_0^1 [H_t(1+s)-H_t(s)] ds
       = integral_0^1 integral_s^(1+s) H_tt(v) dv ds
       > Gm^2/r.
```

The integration region has unit area and positive measure with `v>0`, so
the inequality is strict. This verifies the necessary lower bound
`J>2Gm^2/r+6theta ln2` without treating it as sufficient.

Define the bias-independent energy curvature

```text
U_pair = E2-2E1+E0 = H2-2H1-J/2 = -2D.
```

At coexistence, `epsilon^2=8 exp(U_pair/theta)`. Therefore strict endpoint
bimodality is exactly

```text
U_pair < -3 theta ln 2.
```

More generally, for any bias,
`w0 w2/w1^2 = exp(-U_pair/theta)/8`. Having both endpoints strictly above
the middle implies the same necessary sign inequality; conversely a
coexistence bias realizes both maxima when that inequality holds. For
`J=0`, the full-remainder cost gives `U_pair>Gm^2/r>0`, so **no choice of
linear binding bias yields both strict endpoint modes**. Adding only a
nonnegative occupation pair cost cannot help. Ordinary gravity at fixed
total mass is label independent and cancels from this conversion
curvature. This conclusion is restricted to these diagonal effective
energies; it does not exclude virtual mixing, additional modes or other
microscopic channels.

Two convention checks pass, with their qualifications:

- If `H_n` is replaced by `H_n-a n`, set `B_d` to `B_d-a`. Every `E_n`
  is then unchanged. In particular `H2-2H1` and the barrier criterion are
  unchanged. Subtracting a linear self-energy while holding `B_d` fixed is
  a different Hamiltonian, not this invariance.
- Multiplying each free-particle reference by a positive constant `z_f`
  gives weights `Omega_n z_f^(N-n) exp(-E_n/theta)`. After removing the
  common factor `z_f^N`, these are the old formula with
  `B_eff=B_d-theta ln z_f`. To retain a given physical distribution after
  changing the reference, increase the input `B_d` by `theta ln z_f`.
  A genuine orbital spectrum, occupancy-dependent factor, or
  coordinate-dependent `z_f` is additional physics; a coordinate-dependent
  factor also has to be varied in the source force.

## Reversible dynamics and exact mean first passage

For the declared *occupancy* generator,
`k_ij=kappa min(1,w_j/w_i)` on adjacent states, both directed rates are
positive and finite. The identity

```text
pi_i k_ij = kappa min(w_i,w_j)/Z = pi_j k_ji
```

establishes detailed balance. The three-state chain is connected, so its
stationary distribution is unique. This generator is an additional
effective choice; a microscopic capture kernel or universal attempt rate
has not been derived.

For `epsilon<1`, the generator has
`k01=k21=kappa epsilon` and `k10=k12=kappa`. Setting `tau2=0`, conditioning
on the first jump yields

```text
tau0 = 1/(kappa epsilon) + tau1,
tau1 = 1/(2kappa) + tau0/2,
tau0 = (1+2/epsilon)/kappa.
```

The reverse hitting mean is equal by the exact `0 <-> 2` symmetry. All
holding and hitting means are finite for finite parameters. The residence
clock grows exponentially with the declared energy barrier, within the
stated physical energy-gap regime. This is finite metastability, not
permanent absorption or multiple stationary Gibbs measures.

## Additional checks and qualifications

**Section 4: passed for its separately declared free energy.** For
`0<y<min(nu,1,t_sat/C)`, positive `N,C,theta` and the stated `H`, direct
differentiation gives `F_tt=(K-J)/C`. The three inverse terms in `Q_nu`
have positive second derivatives. Together with convex `H_tt`, this makes
`K` strictly convex. It diverges at both endpoints: the mixing term does
so at a particle/site endpoint, and `H_tt` does so at a saturation
endpoint. Thus it has exactly one attained interior minimum, with two
roots of `K=J` precisely for `J>Jcrit`.

Also `h'=K-J`, while `h` tends to `-infinity` at the lower endpoint and
`+infinity` at the upper endpoint. At an upper saturation endpoint the
last limit uses divergence of **`H_t`**, not just divergence of `H_tt`.
The `artanh` formula supplies it. These facts give exactly the stated
one/three-stationary-point alternatives and their stability signs.
At `J=Jcrit`, `h` remains strictly increasing because its derivative
vanishes only at one point. For `nu=1`, minimizing `1/y+2/(1-y)` gives
`y=sqrt(2)-1` and minimum `3+2sqrt(2)`. The strict lower bound (7) then
follows at the attained minimum from `H_tt>Gm^2/r`. The author's
Stirling-bias relation
`B=B_d-J/(2C)+theta ln C` also checks. None of this supplies a finite-C
equivalence or a microscopic derivation of the mixing entropy.

**Section 5: core discrete ledger and variations passed, with two wording
qualifications.** With multiplicity entropy
`S=-k_B sum p_n ln(p_n/Omega_n)`, differentiating on an edge and adding
the heat entropy `-(E_j-E_i)I_ij/T_bath` gives exactly
`k_B I_ij ln[p_i k_ij/(p_j k_ji)]>=0`. The degeneracy factors are
therefore counted rather than dropped.

Differentiating the diagonal energies gives equation (9), with the stated
positive binding-force signs. Since `H` is a conversion difference, this
is the **latch-dependent contribution** to a full force. If the previously
cancelled source energy is `U0(q)`, the absolute total force additionally
contains `-U0_q`. No force independence can be inferred by dropping that
common term when it depends on the mechanical coordinate. With this
qualification, `B_d'(r)=H_r(2)/2` at fixed `J,theta` and the cancellation
of the `n=2` conversion force check exactly.

The two distinct positive-occupancy conditions in (10), divided by their
occupancies and subtracted, give `J_q=0`, then `B_q=0`. The zero-occupancy
exception is correctly stated. On a smooth stable branch, equation (11)
is the correct scalar Schur formula. Its subsequent singularity sentence
needs the smallest qualification **`F_qt` tends to a finite nonzero value
as `F_tt` tends to zero from above** (or an equivalent condition that
`F_qt^2/F_tt` diverges). Mere nonzero coupling at each pre-spinodal point
does not suffice if it tends to zero. This qualification does not affect
the finite-latch construction.

## Obligation matrix and remaining gap

| Obligation | Verdict and exact extent |
|---|---|
| Counted finite Gibbs trace, endpoint bias, criterion, positive parameter witness | Passed, Section 3 as declared |
| Full rational-remainder conversion affinity and convexity penalty | Passed for displayed zero-stiffness reciprocal functional; not a full-S2 microscopic shell calculation |
| Linear convention and constant free-reference shifts | Passed only with the compensating bias transformation |
| Finite nearest-neighbor rates, detailed balance, unique Gibbs law, exact hitting mean | Passed for declared occupancy generator |
| Negative pair-curvature corollary and failure of `J=0` to yield both endpoints | Passed for the diagonal effective ensemble, for any linear bias |
| Continuous curvature minimum and spinodal threshold | Passed for separate declared Section 4 model and its domain |
| Discrete isothermal energy/entropy ledger and binding-force signs | Passed within effective isothermal contract; full force includes common source energy |
| Schur stiffness and its divergence wording | Formula passed; divergence conditional on nonvanishing limiting mixed derivative |
| Section 6 kinetic-only stochastic witness | Not addressed by this focused audit |
| Prior-art completeness, physical receiver construction, microscopic capture and `J`, actual observational closure | Not addressed / not established here |

The smallest missing physical implication is a derivation of an actual
occupation interaction with
`E2-2E1+E0 < -3theta ln2`, along with the declared state count and a
consistent receiver/transition mechanism. Supplying a linear binding
energy cannot replace that inequality. Restoring a regular collective
source shape and any omitted stiffness is necessary before transferring
the displayed `H` to a physical mode. The report establishes no ordinary
gravity-only free population and supplies no S4/O4 closure.

The strongest safe statement is an exact, counted, reversible finite
effective latch whose extra attractive occupation interaction pays a
positive field-conversion curvature. The cheapest next physical check is
to identify the actual operator responsible for that negative curvature
and calculate its source work before transferring any lifetime or rest
profile prediction to a physical candidate.

## Verification and review provenance

This was an analytic reconstruction using the proof-audit and
computation-audit scopes. No stochastic simulation, scientific numerical
run, symbolic package, production job or old verification program was
executed. There is no finite sampling being presented as a proof. The
only machine execution beyond reading files was standard-library byte
hashing of the author artifact and its 13 declared sources; all matched.
There is consequently no numerical/simulation reproduction command or
computation manifest to imply a stronger result.

The reviewer was a separately tasked in-session agent and derived the
finite ensemble, conversion derivative and backward equations directly
from the raw definitions. The author claim text and `SELF_REVIEW.md` were
available to the reviewer. This is a fresh in-session cross-check, **not
blind external peer review**, formal certification, or evidence that
separate agents cannot share an error. Only this audit file was written;
author text, old packets, criteria, campaign state, jobs and Git state were
not modified.
