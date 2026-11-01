# Fresh final four-fermion/collision review

**Claim:** At the explicit1MeV,e=.003 cold benchmark, the displayed leading heavy four-fermion, light phase/radial, Ward and crossed-vector classes have an interference-safe local loss upper bound2.46270682950e-64GeV at rho=.3GeV/cm³. This is a leading NR vacuum bound in the stated rigid model, not all-order/thermal kinetics.

**Primary verdict: correct only after a stated correction.** `FOUR_FERMION_CORRECTION.md` and `run_four_fermion_v2` implement both corrections identified in review: pin the actual same-vacuum e=.003 slopes, and replace the sum of class cross sections by the Hilbert-norm bound(sum sqrt(class bound))². The original class-sum record is preserved and is not a strict inclusive upper bound. The corrected leading claim passes the proof review below.

## Reconstructed obligations

1. All external photinos, Goldstinos and unbroken gauginos are neutral under residual U1. Starting at a photino insertion, charge conservation forces the entire one-loop trace into the massive charged block. A neutral radial or Goldstino pole is not being assigned M. Feynman xi1 supplies the genuine charged Goldstone mass as in the independently checked hard-transition proof.

2. Four external-fermion insertions switch boson/fermion blocks four times: exactly2boson+2fermion resolvents, with norm r^-6. The positive integral is1/(2LM²), L=16pi². At most24 ordered fourth-log words are overcounted by64; the real/vector/four-component bundle is smaller than512. Together with continuation factor2 this gives32768/(LM²), before the vertex product. There is no renormalizable four-fermion seagull or additional ghost-gaugino cycle. Charge-conjugate/Majorana directions are included in the declared bundle and external-word count.

3. Contracting the raw symmetric superpotential tensor against a normalized chiral source gives Frobenius eigenvalues24e²,6.2e²,2.1e² in the X,A,B blocks. The X eigenvalue bounds the Goldstino projection; gauge source blocks are safely bounded by30g². The external pure gaugino's40g² is also below24e²+30g² at the actual g²=.145e². The factor32 real/spin embedding is generous. Therefore Ymax=32sqrt(24e²+30g²) bounds each normalized insertion without a small-F or inverse-mass enhancement, and C6<=32768Ymax4/(LM²) is a valid loose hard coefficient bound. Unitary mass rotations cannot enlarge it.

4. Four external spinor norms have product<=4m². For a fixed final pair there are4spin labels. Dropping the identical-final factor gives sigma v<=2C6²m²/pi per ordered label pair. Summing13² labels gives338C6²m²/pi. This includes forbidden and elastic pairs; it safely bounds their number-loss subset. The coefficient338 is not an unrecorded species fit.

5. Phase exchange has s=4m² and each pseudoscalar bilinear<=2m, so its per-label amplitude is<=m²/a² when mi<=m. The radial-to-gaugino amplitude is smaller by at most4|kappa_s kappa_i|m²/(mrad²-4m²). With actual |kappa|<1 and mrad/m>498, this factor is<1.7e-5. Overcounting13² labels and4spins gives about21.13m²/(pi a4); adding the separate phase-pair contact/t/u bound remains below22m²/(pi a4). Thus the declared100m²/(pi a4) cap is ample, including phase/radial interference within this class.

6. The separate scalar-Goldstino exchange uses y_sigma_GG=mrad²/(sqrt2F) and the actual source y_sigma_chichi=kappa_s m/a. Direct spinor/propagator multiplication gives the stated amplitude2sqrt2|kappa_s|m3/[aF(1-4m²/mrad²)]. Its bound100kappa_s²m4/(pi a²F²) is far above the direct phase-space result and is safe. It must remain separate from two-Ward-dipole exchange; the author does so.

7. The two-Ward-vertex threshold exchange and crossed hard-vector bounds were separately reconstructed in `SOFT_AND_COLLISION_REVIEW.md`. They have no threshold light pole, and their continuation/flux factors remain valid in the declared NR domain. No threshold expression is being advertised as a finite-temperature average.

8. Different graph classes can have the same final state, so their positive cross-section bounds cannot simply be added as a strict total. Treat amplitudes as vectors in the final-state/phase-space Hilbert space: ||sum A_i||<=sum||A_i||. Therefore sigma_total<=(sum sqrt(sigma_i_bound))², and with common n the same formula applies to local rates. This remains conservative when classes are actually orthogonal. The v2 code uses this expression exactly. It does not rely on a cancellation or infer absence of interference from separate numerical files.

## Numerical/source check and implication

The v2 finite profiles directly evaluate all three mass slopes at the declared vacuum, using h=.001,.0005 five-point log-field stencils. The finer values are SU3:-.99064278010,SU2:-.99030127559,U1:-.99037918172, with relative stencil changes below2.5e-8. Thus the required same-state local source cap is now supported; nearby-coupling shifted-vacuum values are no longer its evidence.

The author obtains Ymax=.51114929326,C6=3.15112897773e-11GeV^-2, and the inclusive hard four-fermion sigma v bound1.06831465631e-25GeV^-2. The interference-safe rate is2.46270682950e-64GeV, or4.35315255173e-20 times the Ward decay. The original sum2.46252048704e-64GeV is only a diagnostic. The correction changes the rate by about7.57e-5relative, while making the logic strict. The computed collisions remain negligible at the stated local density.

This review reconstructs the contact topology, norms, inclusive count, separate light exchanges and interference inequality. It uses the author's finite same-vacuum slope computation as a checked computational leaf rather than claiming a new independent threshold run. The earlier independently reconstructed charged spectrum/unit conversion is in `run_bound_review`; soft/flux arithmetic is in `run_soft_review`. The source/manifest hashes for this final review are in `FOUR_FERMION_REVIEW_INPUTS.json`. The current v2 manifest validates.

The safe conclusion is conditional cold-gas survival against these named leading loss mechanisms. A specified early thermal bath, abundance preparation, higher-order/nonperturbative effects, UV/gravity interactions and a photon identification remain distinct physical inputs. The hard contact proof does not control an arbitrary thermal history or every higher-body process. No claim of those kinds is earned by the small local rate.

## Review provenance

I did not author the four-fermion proof or code. I raised the missing direct same-benchmark slopes and class-interference issues after reconstructing the initial claim; the author preserved its run and supplied v2. I previously authored radial/angular matching and supplied the charged-loop structural observation during the collaboration, so this is a fresh constrained review rather than a blind session. The independent mathematical reviewer was also asked to examine the four-insertion bundle counting; agreement is not substituted for the explicit argument above.
