# IN PROGRESS — catalogue power forecast not yet computed

The point-source law-S Fisher upper bound in FROZEN_CRITERIA is verified:
11/11 checks pass, including Newtonian and deep-MOND projection limits,
the two-lens triangle inequality and an independent noise-only SIS mock.
The mock/analytic SNR ratio is0.9977876100, within the frozen10% line.
This validates the bound's mathematical machinery, not the actual sample's
power. Kappa=1/2 FITTED; not theory closed.

The bound uses a constant component shape-noise forecast and ordinary
geometry with0<=Dls/Ds<=1. It is conditional on the stated point-baryon
law and catalogue distance/mass assumptions. Its triangle form includes
shared-source coherence and bounds any selected lens subset under those
assumptions. It must not be called an exact isolated-lens forecast or a
measurement of the law's amplitude.

Header-only inspection confirms the requested local catalogues exist.
The supplied DESI BGS table has no stellar-mass column, so the requested
mass-threshold isolation cannot simply be read from it. The old FN4c
distance helper uses LambdaCDM and is not reused. If the optimistic
information bound still fails the stage0 precision gate, stage1 cannot
qualify in this forecast. If the bound can pass, missing isolation and
exact distance inputs must be resolved rather than treating the bound
as a stage0 success.

Run the completed mathematical validation from the repository root:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ44_hi_lensing_power/validate_bound.py

The deterministic scientific checks are in bound_validation.json. Runtime
is incidental metadata. No catalogue count, footprint area, Fisher value,
RA-rotation mutation or final stage0 verdict has been computed yet.
The existing conda environment supplies astropy/healpy for the forthcoming
raw chunk reader; the default interpreter has no astropy. Nothing was
installed or downloaded. Large FITS data must never be materialized via
the .data property.
