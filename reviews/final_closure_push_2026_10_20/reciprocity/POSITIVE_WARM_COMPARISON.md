# A positive warm distribution for the retained baryon-only profile

20 October 2026. Continuation of `SOURCE_RESPONSE.md`, Section 4. Analytic
comparison only: this example has infinite tethered mass and does not meet
the finite-stock halo target. It closes a narrower question left by a
pressure-only Jeans construction: a nonnegative distribution can realize
this particular warm support in the formal untruncated two-population model.

## The actual force, not an assigned potential

Use the reciprocal zero-stiffness energy in the parent note, with positive
fixed central point baryon mass M_b and positive central free mass M_f. The
point sources are fixed; a finite dynamical source is a separate obligation.
Let the tethered enclosed mass equal the baryon-only cold-rest target,

    T_b(r)=M_b/2 [sqrt(1+4 a0 r^2/(G M_b))-1].

It satisfies `R(G T_b/r^2)=G M_b/r^2`. The actual tethered acceleration is
therefore exactly `-G M_f/r^2`, including its ordinary gravity and the
specified critical repulsion. Thus its relative one-particle potential can
be taken as `psi=G M_f/r`; the cancellation removes the otherwise divergent
tethered gravitational potential from its own equation. This is a statement
of the effective forces, not separately finite total gravitational and
repulsive energies.

The density differentiated from T_b is

    rho_t(r)=a0/[2 pi G r sqrt(1+4 a0 r^2/(G M_b))].

Put A=G M_f, d=A sqrt(4 a0/(G M_b)), and C=a0/(2 pi G A). Then

    rho_t(psi)=C psi^2/sqrt(psi^2+d^2).

The same tracer force on ordinary stars would be the baryon-only simple-law
force **plus** the central Newtonian free-mass force. This is possible
because the tethered component is warm rather than at rest.

## Direct Abel construction and positivity

Let binding energy be `e=psi-|v|^2/2`, and set f(e)=0 for e<=0. An isotropic
distribution has

    rho(psi)=4 pi sqrt(2) integral_0^psi f(e) sqrt(psi-e) de.

This follows directly by changing variables in `4 pi integral f v^2 dv`.
For our smooth density with rho(0)=rho'(0)=0 define

    f(e) = 1/(sqrt(8) pi^2) d/de
           integral_0^e rho'(psi)/sqrt(e-psi) dpsi.

To verify inversion, differentiate the density integral once, apply the
Abel integral again, and exchange the integrals. The inner integral is
`integral_e^E [(psi-e)(E-psi)]^(-1/2) dpsi=pi`, by
`psi=e+(E-e)sin^2(theta)`. The resulting identity is
`J(E)=2 sqrt(2) pi^2 integral_0^E f(e) de`; differentiating gives precisely
the normalization above. Equivalently applying this double integral to
rho' proves the constructed f recovers the given rho with its zero boundary
value. All endpoint singularities are locally integrable here.

Substitute psi=e x before differentiating:

    f(e)=1/(sqrt(8) pi^2 sqrt(e))
         integral_0^1 [rho'(e x)/2 + e x rho''(e x)]/sqrt(1-x) dx.

For `h(psi)=psi^2/sqrt(psi^2+d^2)`, elementary differentiation gives

    h'(psi)/2+psi h''(psi)
      = psi(psi^4+d^2 psi^2+6d^4)
        /[2(psi^2+d^2)^(5/2)] > 0       (psi>0).

Consequently f(e)>0 for every e>0. It depends only on the exact conserved
one-particle energy of the static force above, so it satisfies the stationary
collisionless equation. The density, and therefore both collective forces,
are the same ones used in its construction. No independent prescribed halo
potential has been substituted for the reciprocal force.

The pressure also agrees directly with the parent note:

    p(r)=integral_r^infinity rho_t(s) G M_f/s^2 ds.

It is positive and finite at every fixed r>0. Each local velocity moment
is finite because `|v|<sqrt(2 psi(r))`.

## Exact limitations and next discriminating construction

At large r, T_b grows proportional to r. The total tethered mass diverges;
the total kinetic energy also diverges logarithmically. At r=0 the fixed
point potential is singular. Neither the isolated finite-system virial
theorem nor an energy-stability theorem may be applied to this comparison
as though those divergences were absent. It is a stationary force/density
comparison with well-defined moments on each compact annulus, not a
finite-energy global state of the unrenormalized action.

Positivity does not establish the physical energy derivative sign needed
by the existing finite-halo stability theorem. In fact f scales as
`e^(1/2)` for small positive binding and as `e^(-1/2)` at large binding.
These limits follow from the last positive integral by dominated convergence:
its bracket is proportional to psi near zero and tends to C/2 at infinity.
Since f is positive yet tends back to zero at large binding, it cannot
increase monotonically with binding throughout. This does not prove instability,
but prevents importing that theorem unchanged.

The next task is therefore precise: construct a finite regular inner source
and outer energy cutoff with a positive distribution **and** the required
energy slope, while retaining the measured law on its admitted annulus and
counting the changed baryon/free forces. Simply clipping this density changes
enclosed masses and the reciprocal cancellation, so is not that construction.
The mass, free-core origin, response times, abundance and metric remain open.

This positive comparison establishes that the cold-rest obstruction is not
a universal equilibrium obstruction. It does not repair the frozen cold
capture prescription or validate a new dwarf fit.
