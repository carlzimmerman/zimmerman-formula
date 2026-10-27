# Physical electric coupling and energy transport

The requested disk/dwarf/cluster mechanism is **not established**. This stage
makes two concrete electric couplings testable and replaces a damping coefficient
with a conservative 3D elastic carrier. It does not simulate galaxy formation.

- **Bond interaction:** charged ionic displacement produces an electric bond
  operator. Its dipole coefficient, induced bond attraction and ionic
  susceptibility obey a relation, reducing independent parameters. In the
  tested real two-band nodal-line class it moves nodes rather than opening a
  mass; its free energy lacks the required positive cubic nonanalytic term.
- **Opposite-parity orbital interaction:** a physical s-p position matrix element
  does open an electric mass with the desired local cubic term. This escapes
  the preceding obstruction. But the complete position operator also moves
  the charged particles across the material. Keeping only the internal dipole
  omits that transport. A stable self-consistent response has not been shown.
- **Energy carrier:** exact harmonic evolution on a 3D lattice exports 34.79%
  of the initial energy outside radius6 by time12 in the coupling1.5 test.
  The energy remains elsewhere in the box; total relative error is at most
  1.12e-15. A 64/96-site-per-axis box check agrees to 3.4e-16 in core fraction.
  This is elastic propagation, not irreversible radiation or orbital cooling.
- **Population selector:** common size-only ballistic/diffusive transport cannot
  cool a3kpc object while leaving .3 and1kpc objects uncooled. Two1001-threshold
  scans confirm the analytic ordering. Thin geometry could alter it, but no
  disk thickness was assigned to obtain a claimed separation.

## Quantitative evidence

[run/results.json](run/results.json): four elastic runs (three64^3 and one96^3),
six small-field points for both electric operators, independent Cartesian
versus elliptic quadrature agreement1.38e-13. The cubic estimator at h=.002 is
.3325833 for an anticommuting mass (limit1/3), .00009374 for node translation
(limit0). This is a necessary static-law distinction, not an observational fit.

[run_orbital_v2/results.json](run_orbital_v2/results.json): eighteen finite slabs,
32/64/128sites, fields .01/.03/.1, full or internal-only electric position.
At128sites and field.03 the full operator transfers22.0355 charges to the
positive half relative to fixed compensating ions, versus -0.1241 in the
internal-only model. Net total charge remains zero. The ionic background is
fixed and self-consistent Coulomb forces are not included; these numbers are
not a screening timescale or an actual galaxy charge fraction.
Energy derivatives match the full conjugate dipole within6.66e-7 absolute.
The independently integrated hydrogenic orbital length is .744935539 a_B.

## Interpretation and remaining task

The orbital route is a positive construction of the missing *local* electric
mass, conditional on an engineered band and filling. It has not derived that
material, isotropy, a0, or a charged tethered state. Its carriers are mobile;
ionic countercharge and Maxwell/Poisson backreaction must be evolved before
using its local response. Neutral emergent fermions might avoid monopole drift,
but their electric operator cannot simply be copied from charged orbitals.

The elastic carrier proves local energy export is possible without deleting
energy. It is not yet coupled to orbital occupations, nor to live gravity.
No present result justifies adding a hand-set capture rate or calling cooled
neutral material a positive tethered population.

Derivations: [electric bond and transport](DERIVATION.md),
[orbital mass and full charge coupling](ORBITAL_ROUTE.md).
Review and correction record: [AUDIT.md](AUDIT.md).
Continuation: [HANDOFF.md](HANDOFF.md).
