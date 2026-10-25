# Continue CCT-009: formation, frames and stars

Read RESULT.md, MECHANISM.md and REVIEW.md. This is the new CCT selectively coupled nonrelativistic wave candidate, not current v3/AeST or SCT-M. No stable observed four-dwarf formation or real-star survival has been demonstrated.

## What the new evidence establishes

- Real finite coherent mode transfer, source-free: matched L=12,nr=512,dt=.02 histories at t=15 put35.74% above l4 with full gravity and only7.6e-26 with monopole-only gravity. Both pass that interval's energy/J gates. The L=4 refined monopole control is NOT evidence about available high-l modes.
- The escape-speed pulse starts with positive total Hamiltonian and leaves a negative-energy remaining field while removing positive energy. Local escape-reference10km/s is NOT a common far-field total-system energy: equivalent collective speeds are62.09/37.10km/s for Draco/Sextans. Initial full-H continuum purity is NOT certified by the monopole projection.
- Finite projection onto sampled occupied CCT-008 radial spans grows from569Msun to14.26million in Draco and303Msun to21.68million in Sextans. This is reference-subspace transfer, not a stationary mixed state or a material-fragment identification.
- Late pulse mass/spin removal: Draco64.27/51.51%; Sextans64.21/71.80%. These fractions are NOT angular/boundary-converged physical predictions.
- Sextans' intermediate radial mass is still missing. At t120 it retains325mMsun overall but only~19m inside972pc and~32m inside1458pc versus reference51m/116m. Well recentering leaves the canonical survey2DeltaNLL~71.66. Both footings/prior beta choices fail to rescue the recorded profile diagnostic.

## The important correction: define the galaxy before scoring it

Draco forms two off-axis potential wells, not one spherical object at the original origin. The well moves from~173pc offset at t60 to~428pc at t120. Well-centred late mass inside193pc is3.39mMsun and its monopole dispersion diagnostic7.74km/s, versus0.786m and6.90 at the old origin. Neither is a full nonspherical stellar fit. High-l power can represent displaced fragments, and J about the old axis includes orbital J. The static fixed-origin probe experiment has strong excitation but DOES NOT prove heating of stars moving with a core.

**Next priority: track material fragments, bulk momentum, recoil and intrinsic spin.** Add core COM/velocity and the sink's linear-momentum ledger. Store enough potential multipole history to evolve stars in a moving frame. Potential-minimum tracking alone is insufficient. Validate translational/recoil behaviour as well as M/E/J, using the saved analytic free-Gaussian benchmark as a first check. Re-score profiles around the actual stellar/material centre; do not replace the old failed criteria silently.

## Remaining physical and numerical obligations

1. Converge m=4,6,8 and radial/dt/boundary response before physical transport percentages. The M6 control changes high-l population materially; radial refinement changes central density even where global high-l mass agrees.
2. Derive/pin a paid incoming mass/total-energy/angular spectrum from an assembly/capture history. The present catchment200Mformed and present-radius scale are postulates. The old bound history overboosts the Fornax/Leo I finite controls. Matched escape-pulse Fornax/Leo I histories have only preflights, not successful production controls.
3. Do not reset into CCT-008 occupations. Pure closed evolution preserves rank; a high-rank statistical field needs a justified time/ensemble bridge, including negative gravitational correlation energy. A coherent stationary alternative is a different possibility requiring its own existence/stability test.
4. Run a live co-moving stellar DF with baryonic backreaction after selecting a physically meaningful remnant. The available circular probes are counterfactual fixed-origin approximation tests only. Do not turn their coherent size changes into irreversible heating or a real-galaxy exclusion.
5. Test the selective Xi coupling in the native host. `host_threshold.json` gives a conservative relative-acceleration condition using actual Galactocentric distances; no Milky Way source mass was adopted. Changing the cold Xi charge requires changing its source and re-scoring, not an extra force patch.

## Canonical executable paths

- `collapse_escape.py`: initial local escape-speed pulse, no gas, original/final fields and monopole initial spectral diagnostic.
- `collapse_half_resume.py`: same finite Hamiltonian with compact even-m Fourier transform and per-radius Chebyshev shifts; optional resume with parent hashes. Child states preserve the complete parent history. Use identical physical/grid parameters; record dt changes explicitly.
- `collapse.py`, `collapse_resume.py`: original dense-grid transform implementation and its resume; kept for equivalence/provenance.
- `collapse_monopole.py`: negative angular-transfer control; two late numerical failures remain preserved.
- `collapse_marginal.py`: total-energy-root history. No gas; not an infinity-capture claim.
- `analyze.py`, `centering.py`, `diagnostic_history.py`, `project_supported.py`, `stellar_robustness.py`, `stellar_probes.py`, `fluctuations.py`: named scoped assays. All posthoc interpretation limits are in their JSONs.
- `compare_runs.py`, `check_angular.py`, `check_fast.py`, `check_half.py`, `free_translation_check.py`: finite operator/control checks. `CLOSEOUT_RECEIPT.json` and the bounded audit manifest reconcile exact bytes.

Fresh-tag reproduction, single-threaded (do not overwrite original tags):

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_envelope_formation_2026_10_24/collapse_escape.py --galaxy Sextans --tag repro_sextans_escape --nr 1024 --lmax 16 --mmax 4 --T 60 --dt .02
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_envelope_formation_2026_10_24/collapse_half_resume.py --galaxy Sextans --tag repro_sextans_long --resume repro_sextans_escape --nr 1024 --lmax 16 --mmax 4 --T 120 --dt .02 --gas none

Draco pulse uses nr768,L12,M4 with the same eta/ref-speed and dt. Fornax/Leo I require their own phase/cutoff convergence; do not promote the L4 preflight into a production result. The measured process RSS in this packet remains below~207MB. The earlier CCT-008 full spectrum fit reached~993MB and should not be enlarged in its current form. Preserve derived outputs before regenerating them with added runs.

Read-only Claude check: X30 cluster sheet result at0f19b6759b matches frozen criteria c6be83f91c and reports OUTER exclusion on both footings; mutation controls fail as recorded. See CLAUDE_READ_ONLY_CHECK.json. Its dependencies were not reexecuted and it is NOT a bridge or a four-dwarf result for CCT. No other chats, automation, shared jobs, publications or remote repository state were changed.
