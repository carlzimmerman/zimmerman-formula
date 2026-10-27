# Cold-dominated halo: regular inverse and closed-support linear work

Checkpoint ZAR-2026-10-19-11-CX, 19 October 2026. **The regular inverse after
mode poles and the full uniform linear work bound are proved for an open
dense class of exact warm distribution choices in a nonempty actual
cold-dominated halo family.** The result does not certify every prescribed
DF, and nonlinear all-time confinement remains open.

The [combined theorem](COMBINED_THEOREM.md) fixes the quantifiers. Take the
original smooth profile at radii `D r_M(1,2,3,4)`, fraction `f=1/64`, generic
sufficiently large scale `D`, and then one sufficiently small **fixed positive**
warmth. On the law annulus, `M/M_b>=2D`, which can be arbitrarily large.
The good DF choices can be arbitrarily close to the original exact inverse
and retain each species' density, mass, support and potential exactly.
They are actual equilibria of the same two-species kernel, not tracers.

For each such fixed equilibrium, the full boundary inverse has finitely many
actual neutral-mode poles. Subtract those poles and the remainder is bounded
and Holder through the entire real receiving-frequency set. Every smooth
compact fixed-`L` canonical generator has

    sup_(t>=0,i,theta_0,q in CLOSED occupied actions) |W_i(t;theta_0,q)|
        <= C_halo N(g_0)<infinity.

Here `N` uses finitely many smooth-source seminorms and the initial energy
norm. The estimate includes circles, the flat energy cap and physical radial
endpoints. It also bounds the linear label through its endpoint identity.
It is a bound along equilibrium receiving trajectories. Constants can depend
on the selected halo and warmth; no cold-limit uniformity is asserted.

The new step is [generic circular force cancellation](GENERIC_FORCE_CANCELLATION.md).
The actual density right inverse supplies exact density-null DF variations.
If a bad circular threshold mode were insensitive to all of them, its
variation functional would factor through density, forcing a radial orbital
average. The actual kinetic threshold and that orbital average have
incompatible blow-up profiles. This gives scalar transversality. A finite
Fredholm-nullity argument then forces the mode's radial force trace to vanish
on an open dense class of the admissible exact DF choices. This condition is
derived for that class, rather than left as a spectral assumption.

The rest of the proof is linked by its mathematical obligation:

- [Actual cold geometry and cap control](GEOMETRY_AND_CAP.md) and
  [complete boundary source pairing](BOUNDARY_PAIRING.md).
- [Kernel reconstruction and finite-frequency inverse](REGULAR_INVERSE.md),
  plus the [high-frequency inverse](HIGH_FREQUENCY_INVERSE.md). Together these
  leave only finitely many genuine mode frequencies, without small cold mass.
- [Actual eigenfield bootstrap and modal criterion](THRESHOLD_MODES.md), then
  the [pole-subtracted inverse](REDUCED_INVERSE.md).
- [Smooth forcing, actual spectral residues and full work summation](CONDITIONAL_WORK.md).

Fresh independent audits cover the [geometry and modes](GEOMETRY_MODES_AUDIT.md),
[source pairing and inverse](INVERSE_AUDIT.md),
[high frequency](HIGH_FREQUENCY_AUDIT.md),
[reduced inverse](REDUCED_INVERSE_AUDIT.md),
[force transversality and genericity](FORCE_CANCELLATION_AUDIT.md),
[density-variation functional details](DENSITY_VARIATIONS_AUDIT.md), and
[full work transfer](WORK_AUDIT.md). Each report pins the exact raw proof
and retains its hypotheses; these are independent reasoning reviews, not a
formal proof certificate. The [final dependency and scope audit](COMBINED_AUDIT.md)
passes the combined theorem, with the inherited equilibrium/energy inputs and
all stated scope restrictions retained. CHECKPOINT.json records the exact pins.

The [route record](ROUTES.md), [source reconciliation](SOURCE_NOTES.md) and
[continuation](CONTINUATION.md) preserve the limits and next decisions. For an
independently fixed DF, membership in the good class or a direct mode
certificate is still required. No actual bad-force mode was constructed.
Degenerate or broader halo geometries require separate source normal forms.
Nonlinear trajectory transfer and label-gradient control remain unproved.

All work was analytic. Only text, proof and provenance operations were run.
Previous proofs, ledgers, manuscripts, sealed records, scientific jobs and
other researchers' work were left untouched. INPUTS_SHA256.json and
PACKET_SHA256.json authenticate the input and delivered files.
