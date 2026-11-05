# Universal-length discriminator results

The analytic incremental Solar bound and its constant-external-field
specialization pass the frozen Cassini quadrupole cut at all three tested
physical lengths. The ratios below are conservative upper bounds, checked
with exact rational inequalities; the displayed decimals are rounded summaries.

| ell (kpc) | Canonical: arbitrary background increment | Alternate: arbitrary background increment | Canonical: constant external field | Alternate: constant external field |
|---:|---:|---:|---:|---:|
| 2.5 | 2.16135e-8 | 2.37601e-8 | 1.65558e-13 | 1.24615e-13 |
| 3.0 | 1.50094e-8 | 1.65001e-8 | 9.58105e-14 | 7.21158e-14 |
| 3.5 | 1.10273e-8 | 1.21225e-8 | 6.03341e-14 | 4.54143e-14 |

Every column is divided by 5.2e-27 s^-2. The first two columns bound the
added Solar anomalous field in any fixed background, not the total background
tide. The final columns use KT34's uniform 45/epsilon_sun^3 theorem under its
original constant external field. Neither is a full ephemeris fit.

`run_001/manifest.json` completed and validates against current input hashes.
The arithmetic uses the actual MW solver's kpc conversion. All analytical
constant slack and the conservative integer upper bounds on sqrt(GM_sun a0)
are checked using exact fractions. No random sampling or large-width Solar
quadrature is involved.

The parent independently reconstructed the Holder factor and the trace-free
projection. The sibling `cassini_interval_route` additionally reviewed the
written proof and independently reconstructed the constants. The proof's
scope is the whole-space Gaussian operator and the simple constitutive law.

## Milky Way witness read-through

The parent-owned completed `../mw/universal_refine_001/results.json` contains
two different allowed baryon cells under the same ell=3 kpc law, one per
acceleration footing. Their finest spatial checks are:

| Footing and original population index | v_c (km/s) | K0 | K-profile chi-square | Ou chi-square | h_K (kpc) | Four primary cuts |
|---|---:|---:|---:|---:|---:|---|
| canonical 1374 | 226.38354 | 69.80799 | 42.81148 | 49.05954 | 3.25983 | pass |
| alternate 1227 | 225.93338 | 69.22720 | 45.31890 | 36.91775 | 3.26736 | pass |

Both remain passing in all six saved refinements (2x, 3x, 4x, 5x spatial,
doubled filter radius, and doubled outer domain). Both fail the separately
retained strict h_K cut; it must not be folded silently into the primary pass
or discarded. This section is a read-through of the parent's results, not a
second PDE implementation. The sibling reviewer independently replayed the
scores and cuts; the parent owns the solver provenance and final qualification.

## Remaining discriminators

This is a cheap two-system candidate with one phenomenological dimensional
parameter and an unsplit static energy. It is not yet a broadly viable law.
The prior source-only universal-2-kpc route had a substantial dwarf deficit;
the corrected source-plus-outer map must earn new dwarf results. The next
low-cost observational discriminator should preserve the original dwarf
sample, mass-to-light range, external-field conventions, and grading while
using the exact new reciprocal operator. SPARC and strict h_K remain separate
liabilities. No galaxy mass, observed cut, or acceleration footing was refitted.

The independent total-phantom-tide corollary is recorded in
`../alternative/TOTAL_PHANTOM_BOUND.md`, with exact arithmetic in
`../alternative/total_bound_001/`: it uses the global bound |A|<=a0 and the same integrable
third-derivative kernel. That distinct statement can bound the full anomalous
tidal field without assuming a constant Galactic background; it does not
include the ordinary Newtonian Galactic tide.

The written proof audit is `../alternative/UNIVERSAL_REVIEW.md`. Two scope
clarifications leave the hash-pinned proof unchanged: its strict incremental
inequality assumes M>0 (for M=0 the increment is exactly zero), and the
effective energy variation is literal for regular densities or an appropriately
renormalized Newtonian point-source action. A point source also has the usual
Newtonian ultraviolet self-energy divergence, distinct from the documented
MOND infrared qualification. The phantom response bound itself admits a point
measure of positive mass and remains valid.
