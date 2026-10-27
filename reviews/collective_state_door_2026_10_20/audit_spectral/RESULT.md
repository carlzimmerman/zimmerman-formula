# Independent audit of winding response and the spectral matching test

20 October 2026. Reviewed proofs: `../topology/RESULT.md` and
`../SPECTRAL_RECEIPT.md`. Actual source and proof bytes are recorded in
`provenance.json`; no Git state was inspected or inferred.

**Normalized claim and primary verdict: proved as written.** This verdict is
for the bounded mathematical claims: the stated periodic-product control of
the original retained-source NR action has the displayed locked branch,
hydrodynamic density response and finite fixed-Q winding homotopy; the frozen
canonical action has the displayed material Hessian and conditional spectral
matching requirement. No exact error was found in those formulas. This is
not a proof of the physical collective-state target. The operator map,
physical occupied geometry, preparation, transition receivers and retention
remain explicitly unprovided.

The proof-audit checklist was applied to definitions, signs, exceptional
modes, admissible homotopies, source normalization and dependency scope.
The author's status labels were not used as evidence. No external theorem or
scientific numerical assertion is needed for the audited implications.

## 1. Claim card and dependencies

The raw action is the scalar/source Hamiltonian in MASTER, equations at
lines 98–125 and the mean-field supplement, with
`M=2m+delta`, `delta>0`, `g=c3>0`, `lambda=kc`, and
`lambda delta>g^2`. It is not the separate mediator or nodal-fermion action.
The fields are complex NR fields, `Q=int(|psi|^2+2|b|^2)`, in natural units.
The leading imposed gravity source is specifically `rho_Q=mq`; it is not
asserted to be the exact relativistic gravitational source.

The winding calculation is on the externally selected finite product
`S1_L x Sigma`, with a uniform transverse Neumann mode. Its occupied branch
obeys (6)'s inequalities and the NR validity restriction. The response claim
is only for nonzero allowed Fourier modes below relative/composition and
transverse gaps, in the positive energetic domain
`A>0`, `D_h>0`, `A D_h>B^2`. The phase-slip bound constrains Q alone.

The canonical comparison is frozen S2 in
`campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md:16`; the .16 revision
explicitly leaves S2 unchanged and .18 retains those unamended statements.
Its parameters and domain remain `K=4piG`, `gamma=K L*^2/2`,
`u=K|P|<a0`. No relationship between its P and the scalar fields is presumed.
The spectral ratio additionally requires the stated passive reciprocal
ground-state representation and the sum rule for that very source operator.

Dependency graph:

`MASTER H -> field equations/Noether charge -> locked ring -> F(q,n,p)`
`-> composition minimum/Schur Hessian -> common-phase action -> chi_rho`.

Independently:
`MASTER H + allowed field zeros -> fixed-Q Fourier homotopy -> finite
energetic upper bound`.

Separately:
`frozen S2 -> integral of W_rem -> material Hessian -> source-specific
longitudinal susceptibility`; then `actual density commutator + passive
spectral expansion -> conditional harmonic-mean requirement`.

The two branches are a comparison, not a derivation identifying their fields.
The leaves are action definitions, geometry/source conventions and explicitly
named state restrictions. There is no circular use of the desired canonical
response to derive the scalar response.

## 2. Obligation matrix

| Obligation | Audit result | Evidence and limit |
|---|---|---|
| Original coefficients, source convention and positive square | Passed | MASTER gives `lambda=kc`, not threshold-rematched `kR` |
| Locked winding branch and flow detuning | Passed | Direct substitution in both field equations |
| Charge, species balances, current and angular momentum | Passed | Conversion signs, `J_Q=Cp`, `Jz=ell Q` reproduce |
| Fixed-q composition, energy bounds and Hessian/current reduction | Passed | Strict `F_nn`, envelope derivative and Schur complement |
| Convective density response and stability restriction | Passed | Both first-order equations give (13)–(15); k=0 is excluded |
| Longitudinal P kernel and canonical mismatch | Passed | Derivative material kernel remains proportional to k squared |
| Admissible fixed-Q Fourier phase-slip path and energy bound | Passed | Exact Fourier norms, normalization and finite energy |
| Trial notch cost | Passed | Both displayed integrals reproduce its coefficient |
| Fixed-Q/fixed-J dynamical escape and lifetime | Not addressed | The path changes J; no receiver or rate is supplied |
| Canonical nonlinear integral, Hessian and density kernel | Passed | Differentiation of frozen S2 gives receipt (1)–(2) |
| Actual selected-versus-total density sum rule | Passed | Receipt conditions (4); actual retained-action moments differ |
| Harmonic-mean ratio and single-coordinate frequency | Passed | Receipt (5) is conditional; (6) has the attractive sign |
| Physical halo/ring existence and operator map | Conditional | These are named missing inputs, not claimed deductions |
| General exclusion of other phases or extra-force operators | Out of scope | Neither proof establishes such an exclusion |

## 3. Raw reconstruction of the winding calculation

Variation of MASTER gives

\[
i\dot\psi=-{\nabla^2\psi\over2m}+2g b\psi^*+2\lambda|\psi|^2\psi,
\qquad
i\dot b=-{\nabla^2b\over2M}+\delta b+g\psi^2.
\]

The positive conversion coupling minimizes its real phase term at
`theta_b=2theta_a+pi`. Writing b0 for the signed coefficient of the source
harmonic, substitution of the two stationary harmonics gives
`(delta+y-2mu)b0=-gn` and
`mu=x+2lambda n-2g^2 n/(delta+y-2mu)`. Hence

\[
\delta_p=\delta+{2p^2\over M}-{p^2\over m}
=\delta\left(1-{p^2\over mM}\right),\quad
\Delta_p=\delta_p-2\alpha,\quad
\alpha=2\left(\lambda-{g^2\over\Delta_p}\right)n.
\]

This reproduces all factors in topology (6), including the detuning change
that would be lost by silently setting `M=2m` in the kinetic coefficients.
The branch inequalities have the stated equivalent interval.

The canonical phase one-form is `-q dot theta`. Direct species variation
gives `dot n+div j_a=2R`, `dot n_b+div j_b=-R`, with
`R=2g Im(b psi*^2)`. Thus `J_Q=j_a+2j_b=C grad theta` and
`C=n/m+4n_b/M`. The azimuthal generator gives
`Jz=ell n V+2ell n_b V=ell Q`. The rest inventory instead obeys
`rho_rest=mq+delta n_b` and a source `-delta R`; in the locked chart
`j_rest=q grad theta`. These distinctions and the bound
`0<=(rho_rest-mq)/rho_rest<=delta/M` are correct. They do not identify rest
inventory with total stress-energy.

Putting `n_b=(q-n)/2` gives precisely F in (7). Differentiation gives (8),
and `F_n(0)=-delta_p/2-sqrt(2)g sqrt(q)<0` for the specified domain while
`F_n(q-)` diverges positively. Thus the mixed composition is unique. The
flow coefficient is between `q/M` and `q/(2m)` pointwise; minimizing preserves
the two bounds in (9). Strict increase with p squared also follows directly
from the positive lower pointwise coefficient.

For a useful independent Hessian check, at the minimizing n let
`s=q-n`, `c=sqrt(2)g` and `a=1/m-2/M`. Then

\[
F_{qq}={cn\over4s^{3/2}},\quad
F_{qn}=-{c(2q-n)\over4s^{3/2}},\quad
F_{pn}=ap,\quad F_{pq}={2p\over M},\quad F_{pp}=C.
\]

Consequently the actual reduced Hessian is

\[
A=F_{qq}-{F_{qn}^2\over F_{nn}},\quad
B={2p\over M}-{F_{qn}ap\over F_{nn}},\quad
D_h=C-{a^2p^2\over F_{nn}},\qquad h_p=Cp.
\]

These are derivatives of the energy being used, rather than separately
inserted response coefficients. At zero flow,

\[
F_{qq}F_{nn}-F_{qn}^2
={c\over2s^{3/2}}\left[\lambda n-g\sqrt{s/2}\right]>0
\]

on the stated grand branch, since `g sqrt(s/2)=g^2 n/Delta` and
`lambda-g^2/Delta>0`. Thus A is positive, `B=0`, `D_h=C>0`; continuity
supplies the stated sufficiently small-flow energetic domain. This does
not prove full finite-wavelength or gravitational stability.

Varying the displayed quadratic common-phase action produces exactly the
two convective equations in topology section 4. Eliminating the phase gives

\[
\delta\rho_Q=-{m^2D_hk^2\over
AD_hk^2-(\omega-Bk+i0)^2}\Phi_N.
\]

The poles are `omega=Bk +/- sqrt(A D_h)|k|` and the static response is
positive in the imposed energetic domain. It is even under reversing p,
although the circulation reverses. Fixed Q removes the uniform density
mode; a single finite ring has discrete k. The proof explicitly respects
both restrictions. Relative/composition dynamics and amplitude gradients
would supply higher derivative corrections, so this is not a claim about
the full Bogoliubov spectrum at their gaps.

For `partial_s P_L=m delta q`, solving the continuity equation with the
uniform integration current separated gives topology (16). At zero
frequency its relaxed material coefficient is
`(A-B^2/D_h)k^2/m^2`. The nonzero positive static density response and this
derivative kernel do not yield a local positive `K|P_L|^2/2` material term.
Uniform winding is a harmonic current; its background delta q and the
chosen longitudinal P representative both vanish. This establishes the
response-versus-circulation distinction in this control only.

## 4. The homotopy is admissible, with the stated conservation limit

For topology (17), the two daughter harmonics and the three source harmonics
are mutually orthogonal within their respective species. Their norms are

\[
\langle|u_t|^2\rangle=d,
\qquad \langle|u_t|^4\rangle=I_4,
\qquad q=d z_t+2\beta^2 I_4z_t^2.
\]

Solving this quadratic gives exactly (18). Since `d>=1/2`, the positive
normalization remains finite and continuous. At `t=1/2`, the two Fourier
terms cancel at one circle point, and `b=-beta psi^2` vanishes there too.
This is an allowed field zero of the original action, not an excluded point
of a permanently nonvanishing phase chart. All actual fields and gradients
are finite. Their Fourier energies reproduce all three terms of (19).

The last coefficient is the positive square
`lambda-g^2/delta+delta(beta-g/delta)^2`. The first endpoint has the actual
stationary composition. The last endpoint is in the neighboring winding
sector, and strict convexity of F permits composition relaxation to that
sector minimum without raising the energy. This verifies the finite bound
(20) for the fixed-Q min–max problem, including its nonnegative lower bound
from the initial endpoint. It does not determine the optimal saddle.

For the notch, substitution into `H-mQ-mu Q` gives
`f'^2/(2m)+2 beta^2 f^2 f'^2/M+kappa(f^2-n0)^2` above its uniform value.
With `w=(m mu)^(-1/2)`, integration of `sech^4` gives `4/3` and integration
of `tanh^2 sech^4` gives `4/15`; (21) follows. The finite notch charge deficit
can be compensated by an O(1/L) uniform charge-density change on a long ring;
the leading fixed-Q energy cost then equals the grand-energy cost. Adjusting
the background twist is still required for a complete periodic slip. The
proof calls (21) a trial scale, correctly, rather than the proved barrier.

The neighboring uniform endpoints differ by `Delta Jz=Q`. Path (17) does
not conserve this angular momentum. The proof explicitly separates its
fixed-Q energetic statement from an isolated fixed-Q/fixed-J dynamics.
No allowed receiver excitations, transition matrix element or irreversible
time follows from the homotopy. This is a substantive limit, not an error
in the stated fixed-Q result.

## 5. Canonical kernel and spectral normalization

Frozen S2 says `K W_rem'(u)=u^2/(a0-u)`. Integrating with zero constant gives
the logarithm in the receipt. Adding `K|P|^2/2=u^2/(2K)` cancels its quadratic
subtraction. For `r=|P|` the resulting material energy obeys

\[
e'(r)={a_0u\over a_0-u}=g,\quad
e''(r)={K a_0^2\over(a_0-u)^2},\quad
{e'(r)\over r}={K a_0\over a_0-u}.
\]

These are the radial and transverse Hessian eigenvalues in receipt (1).
They tend to K at the origin; the transverse formula is understood by its
limit there. Here the source vector called g is the vector conjugate to P,
`grad phi` in the canonical action; physical acceleration is `-grad phi`.
No sign ambiguity changes the positive Hessian or density response.

For a longitudinal eigenvector, `delta rho=ik P_L` divides the quadratic
material coefficient by k squared, giving exactly receipt (2). General
angles require the stated constrained matrix inverse. This susceptibility
is irreducible material response; attraction has not yet been eliminated.

For the spectral representation, let `E_n=hbar Omega_n>0`. Expansion in
energy eigenstates gives spectral numerator
`F_n=2 E_n |<n|rho_k|0>|^2/(V hbar^2)` in a reciprocal channel. Thus the
sum of F is precisely the double commutator divided by `V hbar^2`, with
no missing factor of two. The actual operator still decides that moment.

To verify the important retained-source exception directly, write
`H3=g int(b^dagger psi^2+psi^dagger^2 b)` and
`rho_w,k=int exp(-ikx)(w_a n_a+w_b n_b)`. The local conversion monomial
`X=b^dagger psi^2` satisfies
`[rho_w,k,X(x)]=(w_b-2w_a)exp(-ikx)X(x)`. Therefore, with
`d_w=w_b-2w_a`,

\[
\left\langle[\rho_{w,-k},[H,\rho_{w,k}]]\right\rangle
=\hbar^2 k^2\left({w_a^2\langle N_a\rangle\over m}
                  +{w_b^2\langle N_b\rangle\over M}\right)
 -d_w^2\langle H_3\rangle.
\]

Local detuning and quartic terms commute. Hence the `rho_Q` moment is
`m^2 C k^2` per volume in natural units, not `bar rho_Q k^2` at retained
`M>2m` and occupied b. For rest inventory it is

\[
{D_{\rm rest}(k)\over V\hbar^2}
=\bar\rho_{\rm rest}k^2
 -{\delta^2\langle H_3\rangle\over V\hbar^2}.
\]

Rest inventory is not conserved under conversion. Daughter-only density has
its own conversion term; other selections need their actual commutators.
The receipt expressly
does not apply its Galilean conserved-mass identity (4) to these operators
without the required hypotheses. Thus the distinction is handled correctly,
not an error to be repaired by replacing M with 2m. The continuum local
commutator also requires the declared field algebra; a hard momentum cutoff
does not inherit it automatically. The cited phase note separately states
the spatial-lattice and continuum restrictions. No exact lattice coefficient
or continuum-renormalization theorem is inferred here.

When the sum rule in receipt (4) actually applies to the density in (2),
division of `sum F=bar rho k^2` by the static response gives (5) exactly.
It is a weighted harmonic mean of squared frequencies, not a claim that
every mode has that gap. For `rho_Q`, the corresponding substituted numerator
would instead be `m^2 C k^2`; the receipt's `bar rho` formula is not an
unconditional prediction of the retained-source theory.

Finally, Poisson elimination in a translation-invariant 3D patch gives
`-K|delta rho|^2/(2k^2)=-K|P_L|^2/2`. This attraction is counted once.
With an actual single-coordinate kinetic term `|dot P|^2/(2 bar rho)`,
the material frequency squared is `bar rho(A_alpha+gamma k^2)` and the
total frequency squared is `bar rho(A_alpha-K+gamma k^2)`. The signs and
zero-background cancellation in receipt (6) are correct. The static
subtraction does not require a single pole; the dynamical scalar frequency
does. The topology proof correctly declines to use this 3D kernel as the
uncomputed gravitational Green function of its finite ring.

## 6. Source checks, exact gap and safe use

All 18 input pins and the topology output pin in
`../topology/source_hashes.json` match the actual bytes at audit time.
The two reviewed proofs and raw action/canonical sources are additionally
hashed in this audit's provenance. Some historical references were checked
only for byte identity; that is distinguished from content reconstruction.
The prior-log novelty assertions were not re-audited and are not part of
this mathematical verdict.

Checks used bounded `cat`, `sed`, `nl`, `rg`, direct analytic differentiation
and Fourier orthogonality. A Python standard-library helper computed SHA-256
and byte counts only. No spectral simulation, parameter scan, external
theorem, process inspection, Git operation or author-proof edit was used.

The smallest missing physical implication remains: identify one source-
calibrated microscopic operator in a specified existing-field state whose
material action has the canonical local restoring term, remainder and
stiffness, while a reachable released state loses the stated additional
response and preserves ordinary mass. Fixed-Q winding memory supplies
neither that operator nor its fixed-J release/receiver dynamics.

The strongest safe statement is that these exact conditional ring sectors
store circulation while retaining the computed longitudinal response, and
their fixed-Q field space contains a finite-energy winding-changing path.
The spectral receipt supplies a necessary operator-sensitive matching test,
not a physical realization. The cheapest next check is the same absolute
source response in an actual supplied finite state before release, after
release and after restoration, including its conserved stock and receivers.

Review provenance: fresh independently dispatched audit of raw action and
proofs, with a separate read-only spectral sub-check. That sub-check derived
the conversion commutator from MASTER independently; agent agreement is not
itself evidence. Final mathematical/prose self-review covers this audit file;
author files are unchanged. Exact audited revisions are their SHA-256 pins
in `provenance.json`.
