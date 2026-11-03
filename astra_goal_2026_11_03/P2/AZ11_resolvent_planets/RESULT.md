# AZ11 — FAIL of the planetary diagnostic, both footings

κ = ½ FITTED; not theory closed

The angular monopole follows directly from the divergence source and Gauss' law. At h/e small, expand nu about y=e/a0: A/h=nu(y)-1+y nu'(y)/3. The odd constant-external-field term integrates to zero; integral mu² dmu/2=1/3 produces the derivative term. This coefficient is positive for the simple nu here. The independent angular quadrature agrees to relative 2.47e-10/2.64e-10 on the frozen known-answer test.

Saturn is the limiting row in results.json: A=4.483326840844306e-14 / 7.273219954185815e-14 m/s²; sigma=9.680851063829787e-15. Z=4.631128824608404 / 7.5129964361919415, line 2, margins -2.631128824608404 / -5.5129964361919415. Alt Mars also narrowly misses (Z=2.0419890004718515). All ten controls pass; removing the filter gives a maximum Z above 16000/19000 and MUTATE bites. No width was tuned to remove the miss.

**Scope restriction frozen BEFORE numbers (AMENDMENTS.md):** the quoted ephemeris acceleration bounds assume a constant radial perturbation. Here A is approximately proportional to radius. Therefore these are RQ3's direct-radius diagnostic failures, not a full likelihood-based exclusion of a force law. For a strictly linear radial perturbation the secular pericentre response is 3/2 that of a constant acceleration evaluated at semimajor axis, so the leading shape correction strengthens rather than removes this tension. Exact orbit averaging, other multipoles and fitted planetary initial conditions are still outstanding. No certified full C1 row or closure is claimed.

The sixth P2 lane ends with no rule passing all gates. Next possible change must alter the core response without fitting a bigger xi or scanning higher resolvent powers. Alternatively obtain native full-orbit residuals and evaluate the declared force, with priors fixed independently. The existing approximation should not be rebranded a pass while that work is absent.
