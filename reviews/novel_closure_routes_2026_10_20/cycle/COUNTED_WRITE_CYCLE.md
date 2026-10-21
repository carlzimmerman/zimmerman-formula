# A finite receiver can reopen a latch during the act of writing it

20 October 2026. Claim NCR-CYCLE-01. This is an exact result for the declared
nearest-neighbor write protocol below. It is not a universal lower bound for
all memory protocols or a microscopic explanation of dwarf retention.

## Target and closest prior

The prior simple-site reaction already has a binding/bath/source energy
ledger. The deep-cubic conversion gap is already in
`sol61_push/partition_spin_audit_2026_10_19/RESULT.txt`; general reaction
chemical potentials and compensating charge stocks already occur in
`sol61_push/multicurrent_continuation_2026_10_15/conversion/REPORT.md`.
The exterior full-R artanh primitive is also prior work. None of those is
claimed new here.

The new joint discriminator is finite cooperative memory **plus preparation**:
does a receiver that can accept the write heat leave the post-write state
energetically isolated? An endpoint memory barrier by itself cannot answer
that question. The local overlap report gives the inspected scope, rather
than a global novelty claim.

## A counted finite-state model

Let n=0,1,2 denote occupancies of declared extended collective modes, with
one parcel per site. H(0)=0,H(1)=H1,H(2)=H2 are their diagonal effective
mechanical field energies. They can be specified from the full-R spherical
energy; they are not the field Hamiltonian of one or two literal point
particles. At fixed ordinary total mass the gravitational term is counted
once. A one-parcel self-energy subtraction H(n)->H(n)-nH1 merely shifts the
binding bias and leaves the barrier combinations below invariant.

Use the internal cooperative energy

    E_n(B)=H(n)-B n-J n(n-1)/4.

B is an externally driven binding bias, not baryonic mass; J is a chosen
cooperative interaction. Both have energy units. Put

    B0=H2/2-J/4,
    Delta=H1-H2/2+J/4>0.

At B=B0 the energies are exactly

    (E0,E1,E2)=(0,Delta,0).

The receiver has actual energy Q>=0 and an upper capacity Qmax. Only
nearest-neighbor transitions n<->n+1 are admitted. On an allowed jump it
changes by `Q_new=Q_old-(E_new-E_old)`, provided 0<=Q_new<=Qmax. Changing B
at fixed n supplies external work

    dW_source = partial_B E_n dB = -n dB.

With no additional heat sink, E_n+Q changes only by that work. Assume
allowed elementary transitions have a nonzero rate. The model supplies no
rate magnitude, tunneling exclusion for a real material or microscopic
proof that direct 0<->2 channels are absent.

For `Q0<Delta`, both endpoints are energetically separated from the middle
state at B0: a jump from either endpoint to n=1 requires more energy than
the receiver contains. This is a finite-energy accessibility statement,
not a claim about an infinite canonical heat bath. A direct two-parcel
channel, quantum tunneling, an extra bath or source noise changes it.

## The exact write pulse

Start at `(n,B,Q)=(0,B0,Q0)` with `0<=Q0<Delta`.
Raise B to `B1=B0+Delta=H1` while n=0. The source does zero work, since
`partial_B E0=0`. At this bias the energies are

    (E0,E1,E2)=(0,0,-2Delta).

Allow the sequence 0->1->2. Its first jump has zero energy cost. The second
releases exactly 2Delta into the receiver. It can occur only if

    Qmax >= Q0+2Delta

when no export takes place during the pulse. Then restore B0 while holding
n=2. The source work is `-2(B0-B1)=2Delta`, which raises E2 from -2Delta
to zero. The final state is

    (n,B,Q)=(2,B0,Q0+2Delta).

The mechanical/binding field energy is restored to its endpoint value,
and the source work is stored entirely as receiver heat. The final receiver
has **more** than the middle-state barrier energy, so energetic isolation
has been lost. This does not prove rapid release: rates and other barriers
remain inputs. It proves that the original finite-energy prohibition no
longer protects the written state.

**Protocol-specific dichotomy.** Without heat export, a receiver too small
to hold Q0+2Delta blocks this write; a receiver large enough to allow it
leaves the middle state energetically accessible afterward. The two
requirements cannot be met by that same closed receiver in this pulse.
Other drive paths, reversible preparation or additional controls are not
excluded by the result.

## An admissible counted repair

Export Qout of heat to a separately counted sink after the pulse. To recover
strict isolation one needs

    Q0+2Delta-Qout < Delta,
    Qout > Q0+Delta.

The final receiver must also remain nonnegative. Exporting exactly 2Delta
restores its original Q0 and supplies an explicit allowed construction if
the sink has that available capacity and a physical transfer channel. The
sink is an extra resource, not a derived cooling mechanism. Concurrent
export can alter the intermediate capacity requirement; it must still be
included in the energy ledger.

An explicit erase pulse uses `Bminus=B0-Delta`, reached while n=2. It costs
source work 2Delta. At Bminus, E2=E1=2Delta and E0=0, so 2->1->0 releases
2Delta. Returning B0 at n=0 costs zero. With 2Delta exported per pulse,
the full write/erase cycle returns the occupancy, bias, receiver and field
to their initial values, consumes source work 4Delta and deposits heat
4Delta in the sink. It is not a cyclic source of free energy.

These statements are algebraic energy accounting on the admitted transition
graph. They do not guarantee that a physical write succeeds with probability
one, that a specified rate is fast, or that a real halo has this graph.

## Why the control protocol is part of the result

The separate review supplies an explicit counterexample to any universal
positive write-heat claim under arbitrary conditional occupation holding.
Write x=B-B0, so E=(0,Delta-x,-2x). The following energy-admissible path is
different from the pulse above:

1. Raise x from 0 to Delta at n=0, with zero work; take the neutral 0->1 jump.
2. Hold n=1 while sweeping x from Delta to -Delta. Work +2Delta raises E1
   from zero to 2Delta without changing Q.
3. At x=-Delta the states n=1 and n=2 have equal energy 2Delta; take 1->2.
4. Restore x=0 while holding n=2. Work -2Delta extracts its 2Delta energy.

This path ends in n=2 with Q=Q0<Delta and zero net energy work or heat.
It shows that the graph and endpoint barrier alone cannot imply an
unconditional positive heat cost for every path. Conditional state holding
and correctly timed jumps are additional control assumptions. This is an
admissible path, not a deterministic writer with a counted measurement,
feedback or controller-reset cost. The original positive-heat pulse is
likewise an admitted protocol, not a claim of unit success probability.
Deriving the actual kinetic control is therefore essential: energy
accessibility alone does not select which preparation a physical system
executes. This counterexample preserves the protocol-specific receiver
dichotomy and limits its scope.

## The actual full-R energy and why the ordinary baryon cycle cannot pay silently

For the zero-stiffness two-population energy, co-located conversion changes
T by +dm and F by -dm at fixed total mass and velocity. Its field affinity
per unit mass is the already-known type of functional-derivative difference,
now for the full force:

    mu_switch(r)=Phi_t-Phi_f
      =integral_r^infinity [G T(s)/s^2+R(GT(s)/s^2)] ds >=0.

The inequality is strict when T(s)>0 on a set of positive measure beyond r.
With zero tethered stock the initial marginal is zero; a finite nonzero
conversion still has a positive integrated field cost.

It belongs in H(n), or equivalently in every forward/reverse reaction
affinity. Excluding it would turn a new physical state into the same old
cost-free tag. The cooperative binding energy can pay that positive field
cost, but its own origin and reciprocal coupling must then be specified.

For a spherical shell of fixed radius r and total tethered shell mass T,
put x=sqrt(GT/(a0 r^2))<1. The exact extra field energy is

    H_field(T)=a0^2 r^3/(3G)
      [2x^3 artanh(x)+x^2+ln(1-x^2)],
    dH_field/dT=a0 r x artanh(x).

This supplies one explicit effective input `H(n)=H_field(n m)` with
`2m<a0 r^2/G`. It assumes extended spherical charge/mass modes and zero
stiffness. A delta shell is not admissible under nonzero density-squared
stiffness. The self-energy convention is an effective-mode choice; no
microscopic point-particle energy is inferred from the classical density.

The shell expression also makes a useful distinction explicit: as x tends
to one, its marginal conversion affinity diverges while its total energy
approaches the finite value

    Hcap=a0^2 r^3(1+ln(4))/(3G).

Finite saturation energy already occurs implicitly in prior uniform-start
series. The contribution here is the explicit shell conversion-energy bound
and its use in a finite receiver contract. A total-energy budget at or above
Hcap therefore cannot by itself give a uniform saturation margin. A finite
affinity, stress, regularity or rate condition is a separate obligation.
This limiting statement does not admit the exact singular wall as a regular
state.

Finally, if total cold mass N(r) is held fixed in space, the ordinary
baryonic cross energy is `-G integral M_b(r)N(r)/r^2 dr`. A closed baryonic
loading/unloading cycle then has zero net work through this term. Driving
the internal B as above consequently needs an explicit additional coupling
or resource; it cannot be charged to an unchanged ordinary-gravity ledger.
Moving matter or a changing stress/charge coupling falls outside that
fixed-density statement and needs its own counted work.

## What this adds and what it does not

The result is a protocol-level requirement joining cooperative memory,
actual mechanical field energy and finite preparation resources. It gives
both an excluded closed-receiver pulse and a counted conditional witness
with heat export. It replaces neither the nearest priors nor the missing
microscopic binding action. It supplies a sharper question for that action:
what writes B, where does the write heat go, and which channel prevents it
from immediately reopening the release path?

No galaxy fit, particle species, measured retention time, parameter origin,
full kinetic/metric theory or universal memory-cost theorem is claimed.
Exact-case controls and the separately recorded review check the specified
energy graph and source work, not those absent physical inputs.
