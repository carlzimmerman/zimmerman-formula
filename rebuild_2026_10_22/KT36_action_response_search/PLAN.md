# KT36: new action-consistent response search

The user explicitly authorized a new response law on 2026-11-04 while keeping
the baryons and observational cuts fixed. Base checkpoint:
`48b7492c0ab8062f6566aa7cd2b2baa71492d940`; scientific input hashes in each run
are authoritative because unrelated work continues in the shared checkout.

Target: obtain a single specified response law with a numerical Milky Way
witness in the existing 1375-cell baryon population and a passing Cassini
quadrupole under the same law. Retain both existing a0 footings, the external
field, solar mass, all four primary cuts and the separate strict Lh diagnostic.
A finite witness establishes only this two-system result, not a viable general
theory, a derived law, or a global fit. New parameters must be counted.

The corrected map remains a derivative of a specified energy. In particular,
an independently chosen outer width is not an allowed shortcut. No edits to
KT33/KT34 or existing scientific inputs are needed.

## Route portfolio and ownership

1. **Constitutive response:** replace simple nu by a small parameter family in
   the same scalar energy, with its mandatory adjoint filter. Owner:
   response_obstruction, `response/`. First discriminator: Cassini plus
   nu>=1, nu'<=0 and nu+y nu'>0, followed by the unchanged MW cuts. Power
   steepening, exponential and rational attenuation are constructions within
   this one route, not independent research mechanisms.
2. **Positive mixture of energies:** sum reciprocal filtered energies at
   different widths with common nonnegative weights. Owner:
   cassini_interval_route, `alternative/`. Test the convex tradeoff in forces
   and the signed solar quadrupole, with honest extra parameters.
3. **Universal physical length:** keep the simple response, but use one fixed
   physical Gaussian width for all matter. This defines an unsplit nonlocal
   energy and introduces a length parameter in place of object-specific
   epsilon*rM. Owner: cassini_sign_route, `universal_length/`; root executes
   independent MW computations in `mw/`. First discriminator: full original
   baryon grid at sigma=2.5,3,3.5 kpc and a uniformly bounded solar response.

Root integrates records and audits candidates. KT35 contains the bounded
Gaussian closure attempts, including failed bounds; these do not supersede
KT34 or imply new-law exclusion. All route returns retain exact input hashes,
finite ranges, numerical limitations, and plausible next checks.

## Numerical contract

New MW runs reuse the KT33 discrete energy, Gaussian and observations, and the
KT34 exact density basis. Constant physical widths are not mass-dependent or
quantized: they are the same specified number of kpc for every cell and object.
Initial full-grid search uses refinement 2 and even angular lmax=128. Negative
source mass fraction <=1e-5 and relative source-mass error <1e-10 are numerical
acceptance gates. Selected witnesses require angular/spatial/filter-domain
refinement and the full original scores recomputed from their profiles.

Runs have explicit wall, CPU, thread and log bounds and v2 manifests. No
relativistic health, cosmology, dwarf-galaxy, lensing, or all-galaxy claim follows
from a two-system pass. A static action and numerical reciprocity do not prove
full dynamical health.
