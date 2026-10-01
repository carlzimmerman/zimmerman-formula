# Independent FGF031 finite operator-uncertainty audit

**Verdict: implementation and finite assertion verified in the stated range.** The exact finite constants independently reproduce the worker's certificate. The separately checked norm proof makes the result uniform over all real response errors in the declared ball; it is not inferred from sampled perturbations. The independent reviewer also certifies a conservative decimal radius 1e-5 using a sharper dual-row bound. Neither radius is an authenticated instrument or continuum error budget.

## Independence and correction record

The reviewer derived its perturbation and componentwise witness argument from task031 and pinned029 sources before reading any new worker code or stage19 root proof. A worker formula-preview message arrived after that algebraic reasoning but before the filesystem freeze at 2026-09-30T13:33:05.123985+00:00; this limits any claim of complete informational isolation and is recorded in DERIVATION_FROZEN.json. The implementation was independently written as pivoted Fraction LU plus triangular solves. The worker uses Fraction Gauss-Jordan inversion. No new worker implementation was read until the reviewer run had completed. The reviewer did not read or audit the new root proof, including its optional common-data extension.

The frozen reviewer prose mistakenly labels coefficients keV/cm³ and radial coordinate r/R500. The author caught the normalization issue and the coordinator relayed it. Inspection of original019 confirms dimensionless p(x)=C_SZ Rt Pe(Rt x), x=r/Rt, Rt=1252 kpc, C_SZ=sigma_T/(m_e c²). These erroneous frozen labels are explicitly withdrawn by UNITS_CORRECTION.md. The physical electron-pressure derivative is (dp/dx)/(C_SZ Rt²); no equality Rt=R500 is asserted. Original frozen bytes and the manifest are preserved. The code and contract perform no physical-unit conversion and contain neither incorrect unit label, so the mathematical output needs no rerun. This is a corrected reviewer metadata mistake, not a changed operator.

## Objects, norms and exact finite computation

The audited operator is the one pinned saved15x16 response [U,c], with fixed offset, sixteen free nodes through5 and fixed zero endpoint6. Its binary64 entries are interpreted as exact rational numbers. Original029 construction stores old_pressure as the first15 columns and new_column as the last; its source was checked to establish the worker/reviewer schema correspondence. The target is L5=-5,L6=+5 (zero-based), all other old entries zero, and final coefficient Llast=0. It is the dimensionless dp/dx on (.9,1.1). The node5 coefficient is not part of this target row.

The reviewer independently solved the exact inverse and nominal null vector v=(q,1), q=-U^-1c, and checked U U^-1=I, H v=0, the dual row rU=L, and exact agreement with pinned029's target/null data. The load-bearing constants are

 a=||U^-1||infinity,induced =297.36942959552186,
 b=||q||infinity =10.707177661799811,
 R=||L U^-1||1 =50.26948356094382,
 ||L||1=10,
 mu=Lq =0.16303084957824435.

Displayed decimals are summaries; exact fractions are saved in run_001/results.json. The target sign is positive. This check would fail if the target sign or outer target entry changed. It does not authenticate a continuum response or measured pressure gradient.

## Uniform real-error proof

Assume ||E||infinity,induced<=delta and ||e||infinity<=delta. Induced infinity means maximum row sum, not maximum entry. If a delta<1, U+E=U(I+U^-1E) is invertible by a convergent operator geometric series. With q'=-(U+E)^-1(c+e), the exact difference gives

 ||q'-q||infinity <=eta=a delta(1+b)/(1-a delta).

This holds for arbitrary real E,e in the ball. The worker uses |L(q'-q)|<=||L||1 eta and its exact radius min(1/(4a),mu/[4a||L||1(1+b)]). The reviewer independently reproduced that rational radius and its bound exactly:

 worker delta ~=1.170742196159423e-6,
 worker target lower ~=0.12225894273220218.

The reviewer additionally uses L(q'-q)=-L U^-1(e+E q'), giving the sharper bound B=R delta(1+b)/(1-a delta). Downward decimal rounding of min(1/(4a),mu/[4R(1+b)]) yields one certified radius delta=1/100000. This is rounding one sufficient threshold, not an operator/parameter scan. It gives

 eta ~=0.034917401111142235,
 B ~=0.005902690547360418,
 mu'>=mu-B ~=0.15712815903088392>0.

Entrywise |Eij|<=delta/15 is sufficient for the induced matrix bound, while |ei|<=delta suffices for the vector. Applying delta/15 to both is a stronger sufficient combined entrywise convention. The worker states that distinction correctly. Treating a full matrix with each entry delta as if its induced norm were delta would miss the factor15; the negative control detects this.

## Common strict step and exact witness checks

The reviewer uses its own rational baseline p_i=1e-5/(1+x_i)^2. Let m_i=p_i-p_(i+1), including p16=0 at the fixed endpoint. All16 gaps are positive. With nominal v=(q,1) and v16=0, each perturbed gap change obeys

 |v'_i-v'_(i+1)|<=M_i=|v_i-v_(i+1)|+d_i+d_(i+1),
 d_i=eta for i<15, d15=d16=0.

The common step t=(1/2)min_i m_i/M_i is positive, giving every perturbed witness gap at least m_i/2. The independent exact run obtains t~=5.366049012969053e-9 and a uniform target separation lower bound 2t(mu-B)~=1.6863148053546381e-9. The actual nominal pair's exact pressures, bins, gaps and target difference were checked. Positive gaps through the last free-node-to-zero pair ensure nonnegative pressure through the whole finite support and strict positivity in its interior.

The worker's baseline is a different saved binary64 exponential profile interpreted rationally. Its coarser bound max(1,b+eta) on all null coordinates and step m0/[4max(1,b+eta)] are mathematically valid including the endpoint. The worker reports its own smaller step ~=1.572632500085328e-9 and lower separation ~=3.84536773533e-10. Those differing witness sizes reflect distinct baselines and bounds; they are not disagreement or optimized extrema. The reviewer independently computed its own full witness and checked the worker's coarse-step inequality with the reviewer's baseline, while auditing the worker's saved-baseline implementation by source review rather than a second duplicate run.

The quantifier is important: for every permitted operator there exists its own null pair, sharing one baseline and one common step. The directions and equal synthetic data vector depend on that operator. The result does not give one unchanged pair or one fixed observed vector valid for every E,e. Non-identification persists because mu' remains nonzero and the augmented target adds rank to the15-row response.

## Controls, provenance and execution

The reviewer run checks the exact inverse/null/dual, nominal029 agreement, all16 pressure gaps, missing-last-gap rejection, induced/entrywise distinction, cancellation from an intentionally changed outer target coefficient, and a zero-margin inverse threshold classified only as inconclusive. Worker code's separate threshold mu/[a(||L||1(1+b)+mu)] makes its sufficient target margin exactly zero while still certifying invertibility. The code correctly calls that inconclusive; it does not claim identification is restored. Zero perturbation remains ambiguous inside that larger ball. No error sampling occurs.

The independent run completed in0.196999 seconds and worker run in0.203217 seconds, each with120-second wall,110-second CPU and1MiB log bounds plus a cooperative one-thread library cap. No memory/affinity limit is claimed. Both manifests passed the computation-audit validator with current inputs, and all before/after input/output hashes were independently checked. Seven load-bearing exact worker constants and the entire nominal null vector match the reviewer's independently computed results; final worker input/artifact hashes also match. Successful execution alone is not the uniform theorem: the norm and strict-gap inequalities above provide that step.

## Limits and route stop

The ball leaves target row, pressure normalization, basis, support, annuli and offset fixed; it does not cover uncertainty in those objects. No actual response/calibration/beam/geometry error bound has been established, and agreement between implementations is not such a bound. No covariance, likelihood, real-data fit, physical pressure-gradient significance, density/composition conversion or force/mass inference follows. Both a0 normalizations, distinct vacuum/H histories and Q/RAR/M laws remain separate for future source inference.

The finite robustness route stops after this checked certificate. The remaining empirical obligations are an authenticated response error budget and an independent scalar outer-pressure constraint sensitive to the surviving mode. The stronger conditional radius does not replace either obligation or close the theory.

## Exact pins

- `campaign_fresh_gravity_astra/stage_19/independent_audit/FROZEN_PERTURBATION_DERIVATION.md`: `4ffd59d48f567f9c856f1690ccbe63837afd334b2e7c17d522852607e288346e`
- `campaign_fresh_gravity_astra/stage_19/independent_audit/DERIVATION_FROZEN.json`: `ab96a8063dfa87aef53a5ab9f4b47bd1ecf575e09f5e5234be24baa9126e9fd3`
- `campaign_fresh_gravity_astra/stage_19/independent_audit/UNITS_CORRECTION.md`: `bddd8e6f5eb5cb470663e12bdfc52458cd745f2242241906f2e9dcc1933be61b`
- `campaign_fresh_gravity_astra/stage_19/independent_audit/check.py`: `eb73f7ae6115c9a2700b9341187794445ed00fb179f022849ed33600515dae3d`
- `campaign_fresh_gravity_astra/stage_19/independent_audit/contract.json`: `482078a789df3bc49d1a245dfac8acd8c6411311770591408cc40c4f22214d2a`
- `campaign_fresh_gravity_astra/stage_19/independent_audit/run_001/results.json`: `07ff92af756fb9099975edcfddfd84e53b772ad293a705c2719915b92e9adfc5`
- `campaign_fresh_gravity_astra/stage_19/independent_audit/run_001/manifest.json`: `0510f92bea8d7b3219a0a3713665e6349372199debea61384098ea67386c6d05`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/DERIVATION.md`: `7800758d6ca6269a3f75235cad4c2d3c40a77a3342b049165dac053c9233637f`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/robustness.py`: `957c7a36b04979f6f069e63a1e998934b4f74109055037c59035dbb0976a797d`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/contract.json`: `070783172b7d3a6361bbca231a560bd70f0f0d58777b42d3c0eed5dd30c43443`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/REPORT.md`: `1d1ea99c735d6097e3242aea2185425d1d04f783641cc9f41ba6406374794735`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/result.json`: `64f61a66a79f13d99d6623b5b80aff3fa736576142feec08614a1827a94ba26e`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/numeric_001/results.json`: `093e653c258fad76a5f78857063b6337625421656cddfb8ceb4250be478b389c`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/numeric_001/manifest.json`: `6ed7f7db48a6b22caaa704dfc988184204db2449a35f1552b88740bdd127ae2d`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/DERIVATION.md`: `1df5bae016cc214764dbaf26ddbca7ebec3df2af7a052cf6aa182c599cb47e30`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/project.py`: `5ecada23fa8ca823d02425655f33f37288e868d5e51d7172764576643147fb2c`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-029/fgf029_run_001/extend_support.py`: `bfa2121121121f5acb718e7bf757693139242addabb6ded6492db2abf4d483bf`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-029/fgf029_run_001/numeric_001/extended_response.npz`: `cd6a739967c228624d3f3dd7927030a4cf612ba8dc2191a1a1eef776ec87dc1c`
