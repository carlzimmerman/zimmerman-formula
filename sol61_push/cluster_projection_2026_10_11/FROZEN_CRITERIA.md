# Exterior mass versus a fixed core law: frozen diagnostic

2026-10-11. Base: 6329883c594ed593b197d702a1dd504c17a5fb47.
Commit this file ALONE before executing new numerical checks. Claude lanes are read-only.

Known before freeze: CFG625 static results (all 16 rows) have been read; their
250-kpc projected deficits are known. Cha+2025 section 3.1 has been read and
reports different aperture masses. Rihtarsic+2026 v2 section 5.3 has been read:
reconstructions agree best near 60 kpc. These are not unseen holdout data.

Question: can nonnegative, spherically distributed exterior cold mass repair
a projected aperture deficit while leaving the interior spherical force fixed?
This is a conditional mathematical feasibility bound, NOT a raw-data verdict,
an action, a derived supply law, or an exclusion of candidate B.

For aperture radius R and shell radius r, use the exact angular fraction
p=1 if r<=R; p=1-sqrt(1-(R/r)^2) otherwise. For support r>=r0>=R,
prove M_projected<=p(R,r0)*M_available. Evaluate R=250 kpc and
r0/R=1,2,4. Report the largest allowed r0 if the required fraction is <=1.

Inputs: unchanged CFG625 static JSON, separately for BASE/B1/B2/B3 and both
footings and hosts. Supply illustrations use 5.364*Mb/f with f=1,.90,.86,
subtracting existing TOTAL Mcold, never its aperture mass. These f values are
declared contextual scenarios, not inferred catchments or new adjustable
parameters. Report negative available budgets explicitly as inconsistent
bookkeeping; never reinterpret them as a physical negative mass.

Primary conditional target is CFG625's recorded P16 central aperture value;
also report the recorded lower 2-sigma threshold (main 2.3e14, sub 1.6e14).
P16 transcription remains provisional until the full primary source is read.
Do NOT substitute Cha's lower values in a success gate. Different epochs,
centres, overlapping apertures and reconstruction assumptions prevent such a
replacement. No observational ALLOWED/EXCLUDED labels from this diagnostic.

Checks (must all pass): (1) exact endpoints and large-radius r^-2 limit;
(2) independent angular midpoint counting, 200000 directions, absolute error
<=2e-5 at r/R=1,1.01,2,4,10; (3) shell bound for fixed deterministic positive
mixtures; (4) inversion recovers fraction within 1e-12; (5) MUTATE missing
second polar cap fails a known r=2R benchmark by >.05; (6) MUTATE assigning
all exterior shell mass to an aperture fails that benchmark by >.5;
(7) conservation budget subtracts TOTAL existing cold mass, and MUTATE using
aperture cold mass instead is detected on every input row. No fitting.

Use Python standard library only, one process, <=30 seconds wall and <=20
seconds CPU. No PM job, no large arrays, no dependency installation. Preserve
input hashes, output and controls. A numerical failure blocks interpretation.

Analytic applicability: shell theorem is Newtonian spherical gravity with
ordinary positive mass. It does not assert that a thin shell is stable, that
merger halos are spherical, or that line-of-sight structures have this bound.
No change to kernel, kappa, sealed predictions, or criteria in other lanes.
