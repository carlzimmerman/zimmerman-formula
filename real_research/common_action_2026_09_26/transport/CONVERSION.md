# A second route: coherent conversion into a transporting charged field

The neutral-field density transition in REPORT.md conserves the original
carrier's charge and did not improve its clearing. This route changes the
field content explicitly: two complex classical fields `Psi,Chi` and one real
field s, totaling **five real canonical pairs**. It derives reversible charge
conversion and resonant moving modes from a globally nonnegative potential.
No quantum particle population or phenomenological decay rate is introduced.

## Action and exact conservation

On the same physical metric, first set the common gate to its controlled
constant value `Z=0`. The matter action is

    L=-|grad Psi|²-|grad Chi|²-(grad s)²/2-V,
    V=M²|Psi|²+m²|Chi+gamma s Psi|²+mu²s²/2,
    M,m>0, mu²>=0, gamma real.

It has canonical Cartesian kinetic terms and `V>=0` everywhere. The cubic
mixing is accompanied by its compulsory positive quartic
`gamma² m² s²|Psi|²`; dropping that term changes boundedness and the resonance
threshold. The full field equations in flat coordinates are

    Psi_tt-Delta Psi+M²Psi+gamma m²s(Chi+gamma s Psi)=0,
    Chi_tt-Delta Chi+m²(Chi+gamma s Psi)=0,
    s_tt-Delta s+mu²s+2gamma m² Re[Psi* (Chi+gamma s Psi)]=0.

The simultaneous phase symmetry `Psi,Chi -> exp(i alpha)(Psi,Chi)` gives
`j_P^mu=-i(Psi* d^mu Psi-Psi d^mu Psi*)`, and similarly for Chi. This convention
makes a positive-frequency wave `Psi=A exp(-iMt)` have `j_P^0=2M A²>0`.
The exact exchange equations are

    div j_P = +2gamma m² s Im(Psi* Chi),
    div j_C = -2gamma m² s Im(Psi* Chi),
    div(j_P+j_C)=0.

The real field carries energy and momentum but no diagonal U(1) charge.
Total stress is obtained by varying this one action and is conserved on its
field equations. The flat energy is

    E=integral[|Psi_t|²+|D Psi|²+|Chi_t|²+|D Chi|²
               +(s_t²+|D s|²)/2+V] >= 0.

Thus charge can leave the original Psi field and enter a moving Chi field;
this is the substantive new possibility absent from the neutral transition.
The complete energy and momentum still remain in the evolved fields.

All five real fields share the projected host's actual carrier argument
`z=Z_raw-<Z_raw>_h`, where `Z_raw` is its independent auxiliary and the mean
is the spatial h-volume mean. In the transport displays in this report,
uppercase Z denotes this physical projected z, not the raw auxiliary. The
common-action factors are `Ld=exp(Z)K-exp(-Z)W`. The same exact exchange with the composite gate is then
`partial_t rho_d+div flux=-Zdot rho_d`, and the action lane must supply the
opposite exchange. Constant Z is an exact time rescaling of this calculation.
No independent second metric is added. The full changing gate, its constraints
and gravity are not solved by the calculations below.

For variable Z in a unit physical-lapse, zero-shift chart, define
`A_Z=exp(Z),B_Z=exp(-Z)` and the unrescaled wave current
`j_X^0=-2 Im(X* X_t)`, `j_X^i=2 Im(X* d_i X)` for each complex field.
The exact projected-host charge equations become

    partial_t(A_Z j_P^0)+div(B_Z j_P^i)
       = +2B_Z gamma m² s Im(Psi*Chi),
    partial_t(A_Z j_C^0)+div(B_Z j_C^i)
       = -2B_Z gamma m² s Im(Psi*Chi).

The sum is conserved even for a varying gate. In general ADM coordinates,
densities include sqrt(h), the current includes the shift advection, and
the covariant kinetic tensor is `C^mn=B_Z h^mn-A_Z n^m n^n`.
The same interaction/source term appears in each equation with the opposite
sign. The physical lapse density at fixed Z is
`rho_d=A_Z K+B_Z W=partial Ld/partial Z`. Its flux in the displayed chart is

    F=-B_Z[2 Re(Psi_t* D Psi+Chi_t* D Chi)+s_t D s],
    partial_t rho_d+div F=-Z_t rho_d.

Varying the raw host auxiliary is distinct from differentiating with respect
to its local exponent argument: its carrier source is
`rho_d-<N rho_d>_h/N`. This projected source has zero lapse-weighted integral;
the physical lapse density is still rho_d, so homogeneous field energy is
not discarded. The mean's spatial-metric and foliation variations remain
the ones specified by the host action.

The projected host therefore receives both the exact carrier source and the
opposite energy exchange when varied as one action. This statement does not
replace the host's metric, normal or constraint variations with a prescribed
external Z. The five matter velocity eigenvalues remain positive at every
finite Z. With ordinary Einstein gravity the regular minimally coupled
count is two tensor modes plus these five scalar modes. Any additional
foliation-clock mode or degeneracy in the actual projected host requires
that host's full constraint count; it is not removed by calling the matter
configuration a clock or a condensate.

## Exact linear pump and Floquet equation

An exact homogeneous solution is

    Psi=A exp(-iMt), Chi=0, s=0.

It remains exact without a classical seed; the instability is not spontaneous
classical particle creation. Linearize Chi and s about this solution and set

    h=gamma m² A, mu_eff²=mu²+2h²/m².

For a Fourier mode k,

    Chi_tt+(k²+m²)Chi=-h exp(-iMt)s,
    s_tt+(k²+mu_eff²)s=-h[exp(iMt)Chi+exp(-iMt)Chi*].

The induced s mass is required by the positive-square potential. Rotating
`Chi=exp(-iMt)(u+i v)` turns these periodic equations into the exact autonomous
system

    u_tt+2M v_t+a u+h s=0,
    v_tt-2M u_t+a v=0,
    s_tt+b s+2h u=0,
    a=k²+m²-M², b=k²+mu_eff².

Therefore the **exact** growth exponents satisfy

    [(lambda²+a)²+4M²lambda²](lambda²+b)-2h²(lambda²+a)=0.

Its unstable pump is consistent with positive total energy: the linearized
problem has access to the pump reservoir. The autonomous rotating-frame
quadratic energy is not the full conserved physical energy of all fields.
Pump depletion and nonlinear backreaction must eventually invalidate an
indefinitely growing linearized solution.

## Resonance, growth band and a slow transporting wave

The sum-frequency resonance is

    M=omega_C+omega_s,
    omega_C=sqrt(m²+k²), omega_s=sqrt(mu_eff²+k²).

It exists at positive momentum exactly when `M>m+mu_eff`, with

    k_star²=[(M²-m²-mu_eff²)²-4m²mu_eff²]/(4M²),
    omega_C=(M²+m²-mu_eff²)/(2M),
    omega_s=(M²-m²+mu_eff²)/(2M).

It is not an assumed kick velocity. The resulting group velocities are
`k_star/omega_C` and `k_star/omega_s`. A denser pump raises mu_eff and can
**close** the resonance; this basic potential does not supply the previous
high-density turn-on gate without additional structure.

For a weak pump, retain only the resonant slow envelopes. With
`delta=M-omega_C-omega_s`, their determinant gives

    sigma_RWA²=h²/(4 omega_C omega_s)-delta²/4.

This is an approximation with `sigma,|delta|` small compared with the mode
frequencies and with small pump depletion. Its band condition is
`|delta|<|h|/sqrt(omega_C omega_s)`. The exact sextic is retained for the actual
linear stability result; the approximate formula is not promoted to an exact
local decay rate.

For `M=3,m=1,mu=.5`, exact and approximate on-resonance growth rates are:

| h | exact growth | weak-pump formula |
|---:|---:|---:|
| .1 | .03343781866 | .03344352757 |
| .03 | .01003458084 | .01003473591 |
| .01 | .003344956057 | .003344961803 |
| .003 | .001003490088 | .001003490244 |

At h=.1 the sampled unstable k interval is 1.2375–1.3125 on a 321-point scan
of [.9,1.7], using growth threshold 1e-7. These endpoints are sample bounds,
not interval-certified exact roots. An independent direct integration of the
original periodic fundamental matrix over one pump period agrees with the
rotating-system Floquet multipliers to `2.37e-14`.

A separate conditional slow-wave witness uses
`M=1,m=.998,mu=0,h=1e-6`. Including the induced mass gives

    mu_eff=1.41704766e-6,
    k_star=.0019979994985,
    v_C=.0020019994935, v_s=.9999997485,
    sigma_exact=1.11969503e-5.

Thus a positive classical field action can produce a transporting charged
mode at approximately .002c, together with almost relativistic real radiation.
These are freely specified dimensionless coefficients, not a fit or a derived
cosmological timescale. Raising h to .01 at the same M,m closes the resonance
through its induced mass. The slow witness and the faster nonlinear packet
experiment must not be treated as the same parameter realization.

At exact weak-pump resonance, the usual three slow amplitudes obey, before
substantial depletion/detuning,

    A_dot=-i gamma m² C D/(2M),
    C_dot=-i gamma m² A D*/(2omega_C),
    D_dot=-i gamma m² A C*/(2omega_s).

Their wave-action balances give
`N_P+N_C=constant`, `N_C-N_s=constant`, with
`N_P=2M|A|²,N_C=2omega_C|C|²,N_s=2omega_s|D|²`. The resonant energy
`M N_P+omega_C N_C+omega_s N_s` is conserved because
`M=omega_C+omega_s`. This supplies a classical energy/charge bookkeeping
interpretation, not a quantum production law. In the full theory the changing
pump also changes mu_eff, and the exact action supersedes these truncations.

## Full nonlinear outgoing packet: actual conversion with an energy ledger

The packet run evolves **all** fields of the nonlinear action, including the
pump, rather than maintaining a prescribed oscillation. Use a periodic box
of length 256, `M=3,m=1,mu=.5,gamma=.2`, initially uniform
`Psi=1,Psi_t=-3i`. A localized paired seed has

    C(x)=.001 exp[-(x/8)²],
    Chi=C exp(i k_star x), Chi_t=-i omega_C Chi,
    D(x)=-i sqrt(omega_C/omega_s) C(x),
    s=2 Re[D exp(-i k_star x)],
    s_t=2 Re[-i omega_s D exp(-i k_star x)].

The seed is near the growing linear phase relation; `k_star=1.2639103783`
includes the induced mass. The initial seed, gradients and uniform pump
are all included in the Hamiltonian. A gamma=0 control uses exactly the
same field and velocity data, with its own explicitly changed interaction
energy. It does not receive a random kick, injected power or prescribed decay.
The initial total charge is `1536.000032318794` in all runs.

The Hamiltonian finite-difference/Verlet evolution reaches t=100. The fields
remain smooth on the sampled grids and the newly generated charge flows
through the fixed region boundary `|x|=20`. A complete semidiscrete ledger
checks **both** the diagonal current and Chi's separate conversion source:

    Delta Q_total(region)=-integrated outward total current,
    Delta Q_Chi(region)=integrated conversion source-integrated outward Chi current.

| Quantity at t=100 | N=1024, gamma=.2 | N=2048, gamma=.2 |
|---|---:|---:|
| Initial Chi charge | .000032318794 | .000032318794 |
| Final total Chi charge | 3.6777488078 | 3.6324146622 |
| Lost total Psi charge | 3.6777164890 | 3.6323823434 |
| Outward Chi charge through fixed region | .02220478886 | .02189150738 |
| Chi conversion source inside region | 2.2306061659 | 2.1873447090 |
| Remaining Chi charge inside region | 2.2084336958 | 2.1654855204 |
| Fraction of initial total region charge exported | .00009951286 | .00009754124 |

The two-resolutions difference in converted charge is approximately 1.25%;
it is a finite refinement check, not a measured asymptotic convergence order.
At the fine grid, relative energy drift is `1.61e-7`, global charge error
`3.56e-15`, total local flux error `2.19e-15`, and separate Chi conversion
ledger error `3.89e-17` relative to initial region charge. The uncoupled control
keeps its total Chi charge at its seed value and merely transports that seed
outward. The nonlinear coupled run transfers additional conserved charge
from the pump and exports some of it.

This is a constructive classical transport result, but its total fixed-region
clearing is only about `9.75e-5`. It is not the L373/L380 clearing threshold.
The pump here is uniform and the wave packet is fast; there is no selfgravity,
evolving auxiliary gate or cold cosmological initial state. It must not be
combined with the distinct .002c Floquet witness as one demonstrated prediction.
The first potential's failed clearing advantage is preserved in REPORT.md;
this second route establishes a different mechanism with a larger explicit
field count, not a retroactive pass for that earlier route.

## Global fixed-background field theorem

There is a meaningful global result beyond a finite homogeneous calculation.
Let `u=(sqrt(2)Re Psi,sqrt(2)Im Psi,sqrt(2)Re Chi,sqrt(2)Im Chi,s)` be the five
canonically normalized Cartesian real fields, on a flat compact three-torus
or R3 with initial data `u0 in H1`, `u1 in L2`. Let V be the displayed
nonnegative polynomial. Then its canonical semilinear wave equation has a
unique global energy-class solution
`u in C(R;H1) intersect C1(R;L2)`. Smooth finite-Sobolev initial data preserve
the corresponding smoothness for every finite time. This claim is for the
fixed background; it is not a theorem about the common gravitational action.

Here is the continuation argument, displaying the analytic ingredients.
The Sobolev bounds `H1 -> L6` and interpolation to L3,L4 imply for this degree
at-most-four polynomial

    ||grad V(u)-grad V(v)||_L2
      <= C_R ||u-v||_H1,  ||u||_H1+||v||_H1<=R.

Each cubic difference has two L6 factors and one L6 difference; each quadratic
difference uses L4 factors. Linear terms use L2. The free-wave propagator maps
`H1 x L2` to itself on every finite time interval and its Duhamel integral
maps `L1_t L2_x` into the same energy space. The displayed Lipschitz bound
therefore gives a local contraction and the continuation criterion that a
finite maximal time requires the `H1 x L2` norm to diverge. No asymptotic
scattering estimate is needed.

For smooth solutions, multiplication by u_t and integration by parts give

    E=||u_t||_2²/2+||Du||_2²/2+integral V(u),  E_dot=0.

Approximate energy-space data by smooth data on the local existence interval.
The same Lipschitz estimate and continuity of the polynomial potential
`H1 -> L1` pass this identity to the energy solution. Positivity then gives

    ||u_t(t)||_2, ||Du(t)||_2 <= sqrt(2E),
    ||u(t)||_2 <= ||u0||_2+|t|sqrt(2E).

Thus the continuation norm cannot diverge at a finite time. The L2 estimate
also treats massless s (`mu=0`); coercivity of every separate mass term is not
needed. Time reversal gives the same argument for negative time.

For H2 persistence, differentiate the equation once. Since the Hessian of V
has degree at most two,

    ||D(grad V(u))||_2 <= C(1+||u||_H1²)||u||_H2.

The cubic term uses `||u||_6² ||Du||_6`, controlled by H1 and H2. The differentiated
energy estimate and Gronwall give finite H2 norm on each finite interval.
Higher regularity then follows by the corresponding differentiated product
estimates with the already controlled lower norms. This proof provides no
uniform-in-time decay or pointwise field bound from H1 alone. It also does
not turn phase charts into global timelike clocks.

The same argument applies to the first bounded quartic potential in REPORT.md.
For any **constant** finite Z the exact time rescaling extends this theorem
to the common-action matter block. For dynamically determined Z, gravity or
moving geometry, the energy/continuation estimates require a new coupled
proof. Positive matter energy by itself is not that proof.

### Extension to a fixed static inhomogeneous projected-host geometry

The global energy-space result also holds without a flat or spatially
constant gate. Fix a smooth compact three-dimensional leaf `(Sigma,h)`, a
smooth positive static physical lapse N, a smooth finite static projected
gate z, and zero shift. These are fixed coefficients, not a claimed solution
of the fully evolving host constraints. The common matter action becomes

    integral dt dvol_h [A |u_t|²/2-B(|Du|²/2+V(u))],
    A=exp(z)/N, B=N exp(-z),
    A u_tt-div_h(B Du)+B grad V(u)=0.

Compactness and the fixed smooth positive inputs give constants
`0<A_min<=A<=A_max`, `0<B_min<=B<=B_max`. The operator
`L=-A^(-1)div_h(BD)` is nonnegative self-adjoint in `L2(A dvol_h)` with form
domain H1. Its wave propagator and Duhamel energy estimate are the same
Hilbert-space construction used above, with equivalent weighted norms.
The nonlinear map `(B/A)grad V` is locally Lipschitz from H1 into this
weighted L2 by the compact three-dimensional Sobolev product estimate.

Because all coefficients and the measure are time independent,

    E=integral dvol_h [A|u_t|²/2+B(|Du|²/2+V)]

is conserved. In the unweighted metric norms,

    ||u_t||_2<=sqrt(2E/A_min), ||Du||_2<=sqrt(2E/B_min),
    ||u(t)||_2<=||u0||_2+|t|sqrt(2E/A_min).

These estimates prevent the local H1 x L2 continuation norm from diverging
at a finite time, proving a unique global energy-class solution on this
fixed static geometry. Fixed smooth-coefficient commutator and elliptic
estimates give the corresponding persistence of smooth initial data.
The positive-weight bounds are hypotheses supplied by the frozen geometry;
this result does not propagate N, z, h, a timelike clock or the auxiliary
constraints. It therefore advances the inhomogeneous matter transport
theorem without asserting global health of the full common action.

## Evidence scope

`run_conversion_001` accepts 19 exact/finite linear-conversion checks. It
verifies the characteristic polynomial, the mass-shifted resonance, charge
exchange and an independently computed periodic monodromy. The nonlinear
packet calculation evolves every field with the full positive-square
potential, and is recorded separately. Algebraic Lean statements and accepted
run hashes are listed in EVIDENCE.md. The global energy-space argument above
is an analytic proof using the displayed Sobolev and wave estimates; it is
not claimed to be formalized in Lean by a few algebraic lemmas.
