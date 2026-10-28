# Exhaustive MW-ultra-faint two-state obstruction: frozen before new arithmetic

Coordinator authorized this proof check after source inspection. It adds no candidate L and no observational
model run. The fixed X51 cooling-floor halo profile has no L input. In corrected heldout source, L enters X51
only through CSM_DFLAG, which chooses either the fixed halo pull or the fixed law pull. All MW ultra-faint
class members have host MW, hence share one fixed LG parent mass, background A, S9 function and footing floor.
Their switches therefore all agree at every L, including the equality/floor convention. They cannot form
an arbitrary mixture as L varies. There are exactly two class predictions per footing.

Before claiming an all-L obstruction, verify the actual finite class contains only MW-host members, each
recorded selector uses the same LG mass/floor, and the complete gN/gh/gobs/error data for the class are identical
across all three existing L cells. Source-audit the X51 executed prefix: its cooling mass and floor/profile
construction do not receive L, and the callback only reaches branch choice. The raw geometry and membership
remain inherited fixed inputs; no statement about a revised dwarf model is made.

Reconstruct both residual arrays directly from the saved physical pulls: Ehalo=log10(gobs/(gN+gh));
Elaw=log10(gobs/[gN*(1/2+sqrt(1/4+a0/gN))]). Recompute the inherited median and Gaussian-noise bootstrap
standard deviation using numpy PCG64 seed20261026,10000 resamples, original row order. MW-ultra-faint is the
first inherited class, so the seed needs no prior-class RNG advancement. All calculations are per footing.
Compare halo Z to completed normal heldout result and law Z to original BS1 all-law flag-inversion result
within1e-10. The actual strict criterion is |Z|<2. Report both states even if only one fails.

If both states fail on a footing, its frozen MW-ultra-faint criterion excludes every positive L in this
fixed one-parameter scorer. That conclusion is exhaustive by the two-state reduction, not by an L grid.
If only the law state fails, retain only the necessary LG-on lower threshold; do not infer global failure.
Check source/data hashes stable. Deterministic repeated results must match.
