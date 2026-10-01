# FGF031: uniform finite response-error certificate

Accepted as a conditional uniform theorem and two exact-arithmetic certificates
for the fixed saved15x16 cluster pressure response. The changed premise is
uncertain U,c, with L, basis, support, row convention and zero offset held fixed.
No additional response map, annulus, support extension or data fit was computed.

For arbitrary real E,e use induced matrix infinity norm (maximum absolute
row sum) on E and vector infinity norm on e. U+E stays invertible if
M epsilon<1, M=||U^-1||infinity. With w=U^-1c, W=||w||infinity,
mu=-Lw and K=||L U^-1||1, the exact inverse identity gives
||w_tilde-w||infinity<=M(eta+epsilon W)/(1-M epsilon), and
|mu_tilde-mu|<=K(eta+epsilon W)/(1-M epsilon).
The worker uses the valid coarser ||L||1 bound. A positive target margin,
not invertibility alone, keeps augmented target rank16 with response rank15.

Exact constants agree across independent Gauss-Jordan and pivoted LU methods:
M approximately297.369429595522, W approximately10.707177661800,
mu approximately0.16303084957824435. The author radius is approximately
1.170742196159423e-6 for both norms, with target lower bound approximately
0.12225894273220218. The independent sharper bound K approximately50.269483560944
certifies the exact simple radius1e-5, target lower bound approximately
0.15712815903088392. All exact endpoints live in the rational output, not
rounded prose. Entrywise E bounds must include the factor15; e has no such
row-sum factor. These are sufficient mathematical radii, not optimized or
measured instrument tolerances.

A strictly positive decreasing baseline and uniform norm/gap control give
one common positive step for every allowed operator's own null direction.
Every gap including the last free node to the fixed zero endpoint remains
strict. The independent rational inverse-square baseline has step approximately
5.366049012969053e-9 and target-separation lower bound approximately
1.6863148053546381e-9. Author's exponential baseline gives a different
step1.572632500085328e-9 and lower separation3.845367735334641e-10.
These are different synthetic witnesses, not sharp feasible widths, actual
pressure error bars or conflicting observational estimates.

Each pair uses the SAME perturbed operator. Synthetic bins can vary across
operators; neither numerical certificate fixes one observed vector throughout
the ball. Root additionally derived a corrected baseline for fixed nominal
synthetic bins with extra gate2A<m. A separate root-only proof audit accepts
that conditional theorem, but no numerical radius is asserted for that stronger
version. At a sufficient-bound threshold the verdict is inconclusive, not
restored identification. The zero-error case and strict endpoint controls pass.

Two bounded manifests validate current immutable input/output bytes:120s wall,
110s CPU, cooperative one-library-thread cap,1MiB logs, no memory cap. Author
reports26 exact controls. Auditor checks its own constants, null/dual relations,
nominal witnesses and the author's coarse-radius formula independently.
Root read both codes and compared exact rational results. Root proof was fixed
before new author output and separately audited. The independent auditor
records receipt of author formula preview after its own algebraic reasoning
but before filesystem freeze; this limits the stronger independence claim.
No random error sampling or continuum convergence inference is used.

## Preserved units correction

The independent auditor's frozen plan incorrectly labelled the saved pressures
keV/cm3 and used r/R500. Root briefly relayed that label; the author traced the
original FGF019 convention and root verified it. The actual dimensionless
p(x)=C_SZ R_t P_e(R_t x), x=r/R_t, C_SZ=sigma_T/(m_e c²), maps to dimensionless y.
The target dp/dx becomes physical electron-pressure gradient only after dividing
by C_SZ R_t². The frozen error, correction, and original source hashes remain
visible. The completed computation contained no physical-unit conversion;
its code, results and historical manifest were not silently rewritten.
Neither this radius nor agreement between implementations authenticates the
actual calibration, distance, beam, geometry, target error or continuum response.

The finite robustness route stops here as task031 requires. No new radius,
annulus or support-sweep child is created. An actual response-error budget and
an outer-pressure datum sensitive to the null mode remain empirical gaps.
FGF034's constrained equilibrium response is next. Related primary AS1755
concerns spectral scale identification, not this particular fixed cluster
matrix/target; no active matching claim/result was observed. AS228 retains its
primary owner. No primary catalog files or claims were edited.

No force or mass is calculated. Later conversion must preserve density and
composition, both a0 normalizations, separate vacuum/H histories and distinct
Q/RAR/registered M source inversions. No physical metric, empirical fit or
common-theory closure is inferred from this conditional finite result.

## Evidence pins

- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/result.json` SHA256 `64f61a66a79f13d99d6623b5b80aff3fa736576142feec08614a1827a94ba26e`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/DERIVATION.md` SHA256 `7800758d6ca6269a3f75235cad4c2d3c40a77a3342b049165dac053c9233637f`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/REPORT.md` SHA256 `1d1ea99c735d6097e3242aea2185425d1d04f783641cc9f41ba6406374794735`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/robustness.py` SHA256 `957c7a36b04979f6f069e63a1e998934b4f74109055037c59035dbb0976a797d`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/numeric_001/results.json` SHA256 `093e653c258fad76a5f78857063b6337625421656cddfb8ceb4250be478b389c`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-031/fgf031_run_001/numeric_001/manifest.json` SHA256 `6ed7f7db48a6b22caaa704dfc988184204db2449a35f1552b88740bdd127ae2d`.
- `campaign_fresh_gravity_astra/stage_19/operator_audit/CROSS_IMPLEMENTATION.json` SHA256 `374fa190681e1a723172d16ba459ae1012e6a943f6ecfbccffd668defa9f194f`.
- `campaign_fresh_gravity_astra/stage_19/operator_audit/INDEPENDENT_AUDIT.md` SHA256 `4a935729ee3f778e2e4ebd1be555ed18a44e5ff084cfb69f2a329c18c0ff5bc4`.
- `campaign_fresh_gravity_astra/stage_19/operator_audit/PROOF_RECORD.json` SHA256 `2162affa6d82a8aed6fb728cf6bf343b1a931f90128c3b8772fe275ca1dfd07d`.
- `campaign_fresh_gravity_astra/stage_19/operator_audit/ROOT_DERIVATION.md` SHA256 `ce83162cd2f45f2f938af4a00c8d4e5ea9ef670e562b53c3d013d678397efa8b`.
- `campaign_fresh_gravity_astra/stage_19/operator_audit/UNITS_RECONCILIATION.md` SHA256 `49e0a449260044d35ac0458b2025d5b3429b2577009df3d66905ad308475d5ab`.
- `campaign_fresh_gravity_astra/stage_19/operator_audit/UNITS_SOURCE_PINS.json` SHA256 `c7bc22d46fa02f78697142c7f466f19ddff03eafc61b3e70b2e2bf46faf1c23e`.
- `campaign_fresh_gravity_astra/stage_19/operator_audit/audit_result.json` SHA256 `33d7a1d77d090bf4ee7cc0ee51b5f42362a1201f8d5ac9531d49f1655d5d57ff`.
- `campaign_fresh_gravity_astra/stage_19/independent_audit/DERIVATION_FROZEN.json` SHA256 `ab96a8063dfa87aef53a5ab9f4b47bd1ecf575e09f5e5234be24baa9126e9fd3`.
- `campaign_fresh_gravity_astra/stage_19/independent_audit/FROZEN_PERTURBATION_DERIVATION.md` SHA256 `4ffd59d48f567f9c856f1690ccbe63837afd334b2e7c17d522852607e288346e`.
- `campaign_fresh_gravity_astra/stage_19/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `922e0019086e0131820d64dcf5d0f1d0982ebc64f0c1f242ca88ee6959fc6ee5`.
- `campaign_fresh_gravity_astra/stage_19/independent_audit/UNITS_CORRECTION.md` SHA256 `bddd8e6f5eb5cb470663e12bdfc52458cd745f2242241906f2e9dcc1933be61b`.
- `campaign_fresh_gravity_astra/stage_19/independent_audit/audit_result.json` SHA256 `d6cd484cc3a143d72159d6f872df48a6865bba2f18c3bef377a5666e41a56889`.
- `campaign_fresh_gravity_astra/stage_19/independent_audit/check.py` SHA256 `eb73f7ae6115c9a2700b9341187794445ed00fb179f022849ed33600515dae3d`.
- `campaign_fresh_gravity_astra/stage_19/independent_audit/contract.json` SHA256 `482078a789df3bc49d1a245dfac8acd8c6411311770591408cc40c4f22214d2a`.
- `campaign_fresh_gravity_astra/stage_19/independent_audit/run_001/results.json` SHA256 `07ff92af756fb9099975edcfddfd84e53b772ad293a705c2719915b92e9adfc5`.
- `campaign_fresh_gravity_astra/stage_19/independent_audit/run_001/manifest.json` SHA256 `0510f92bea8d7b3219a0a3713665e6349372199debea61384098ea67386c6d05`.

Reconciled 2026-09-30T13:39:45.478145+00:00.
