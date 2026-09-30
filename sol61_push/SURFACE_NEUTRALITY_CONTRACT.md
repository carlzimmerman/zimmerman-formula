# Surface neutrality audit

Test the free, zero-temperature, uniform two-dimensional Dirac branch previously used for the surface cubic. Set c=hbar=1, m=y|p|, speed v>0, positive-band degeneracy nu and chemical potential zeta>=0 measured relative to the cone. Retain the prior subtraction of the analytic vacuum quadratic term. This subtraction remains a matching assumption.

Exact symbolic integration tests the grand potential, its first derivative at m=zeta, and the density. Independent momentum quadrature tests zeta=1, nu=2, v=0.3 and m in {0,0.2,0.8,1,1.5}, absolute tolerance 1e-11. Exact four-dimensional Pauli matrices test a candidate time reversal and the central-product obstruction to a canonical particle-hole operation leaving p unchanged. No random sampling; timeout 30 seconds, one numerical-library thread.

A pass verifies these free-band identities and these specified matrix actions. It cannot prove a microscopic symmetry, an interacting phase, covariant vacuum stress, critical quadratic matching, observational viability or 32pi. A numerical discrepancy requires investigation before use. The ensemble is fixed chemical potential; an identity energy shift does not itself imply doping at fixed charge.
