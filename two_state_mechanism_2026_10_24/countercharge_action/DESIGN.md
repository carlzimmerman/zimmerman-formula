# Charge-conserving action: derivation and bounded tests

Scope: continue the user's requested microscopic mechanism, reducing parameters
before fitting. Preserve all earlier solver/evidence files. New work stays here.
No claim of a unique fundamental theory, causal relativistic completion, or
successful disk formation is made in advance.

Chosen minimal inventory: neutral F, positive T of mass m, negative C of mass
epsilon*m, and the gauge field. T and C have equal opposite charges. Conversion
must produce/consume T,C together. Baryons are gauge-neutral. A gauge-invariant
reaction vertex specifies charge bookkeeping but does not fix its coupling/gap.
The existing spherical acceleration relation fixes an electric constitutive law;
its Legendre dual supplies the electrostatic action. The 3D equation is derived
from this action, not copied from the older curl-free-displacement approximation.

Inline implementation plan:
1. Derive action, normalization, currents, reaction ledger, cold-equilibrium
   constraints and minimal relativistic consistency checks in ACTION.md.
2. Write tests before implementation: Legendre identity, correct force sign,
   charge conservation, Gauss residual, nonlinear energy conservation.
3. Implement a periodic 3D spectral electrostatic solver of the new action and
   a conservative homogeneous two-carrier plasma response (no frozen negatives).
4. Run bounded checks of spatial refinement, force derivative, exact neutrality,
   plasma energy and time refinement, RAR countercharge bounds and microscopic
   Coulomb/core applicability. Use the same constants for all numeric profiles.
5. Report what works and any obstruction. Do not manufacture a population result
   by holding countercharge fixed, changing reaction parameters by object label,
   equating local force signs with galaxy assembly, or ignoring causal failures.

The 3D test uses neutral periodic manufactured sources; an immobile compensating
background is allowed ONLY for a like-charge force-sign unit test. It is not a
formation model. Plasma tests include both inertias and conserve energy, but
are uniform-mode tests, not a live 3D gravitational galaxy solver. These are
deliberately necessary-condition tests before such a solver is warranted.

Predefined bounds: N=17,25,33 grid points per side, box24, Gaussian source width
1.5, amplitude40, pair separation4; oscillator amplitudes .05,.3,.7 and epsilon
1,.1,.01 over dimensionless time30, two tolerances. Equilibrium scan x=g0/a0
from1e-4 to1e2 (61 values), epsilon1e-4..1 (17 values), tolerance.05dex.
Microscopic applicability scan m=1e-6..1e19GeV (101 values), epsilon1e-4..1
(17 values). Keep only alpha_G<.1 and Bohr radius>10 compulsory core radii for
the Coulomb inference. Flag rather than extrapolate the remaining points.
