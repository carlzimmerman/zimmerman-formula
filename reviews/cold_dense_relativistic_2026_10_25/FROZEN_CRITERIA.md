# Dense relativistic averaged-fluid gate

Base e8b0beff16. Use d=0, real scalar, same potential and positive vacuum.
A preliminary oscillator probe found a positive-pressure dense branch above
E/D ~.497. Formalize it using full-cycle Gauss-Legendre quadrature, compare
256/512 nodes, and check the scalar virial average. This is a time-averaged
perfect-fluid surrogate, not an exact real-scalar stellar solution.

Integrate TOV with excitation density E, pressure P(E), and vacuum density 1.6 D.
Use 61 central densities from 1.001 times the zero-pressure density to 1e6 D,
EOS table to 1e10 D. Stop on pressure zero, metric factor 1e-5, EOS upper bound,
or dimensionless radius 3. Record central pressure increasing cases separately.
Repeat at two EOS resolutions (800/1600) and integration tolerances. Compare
terminal classification; for surfaces require radius/mass agreement <.01.
Zero-vacuum gravity is a numerical comparison only, not a permitted retuning.
Do not claim radial stability from positive sound speed or a mass curve alone.
No abundance, formation history, galaxy switch or clump mass is chosen.
Mutation flips the vacuum-force term and must fail the constant-density TOV
algebraic check. Any missing surface, field matching or stability must be stated.
