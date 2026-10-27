# Independent audit of round-2 de Sitter and oblique principal claims

**Primary verdict: proved as written for the corrected raw statement, within its explicitly limited linear/static-principal scope.** Here linear boundedness has its usual initial-value meaning: forward from a finite initial time, for each fixed finite nonzero comoving wavenumber and finite constraint-compatible initial data. It is not boundedness across the entire past-eternal de Sitter chart, nor a uniform norm bound on all k or backgrounds.

The raw action implies the claimed exact de Sitter scalar quadratic action, positive forward scalar energy estimate, homogeneous quadratic endpoint, and full regular static oblique leading block. The angular uniform margin criterion is correct. One literal endpoint implication was false in the initial input and has been corrected by the coordinator; the corrected text was directly re-read and its hash verified. No full S3, PPN, nonlinear, arbitrary-evolving-background, or quantum-cutoff claim is supported by this audit.

## Exact claim card and provenance

- Source: `03_relativity/raw_derivation.md`; exact ADM action with spatial covector P, positive K,beta,eta,gamma, finite a0 and u=K|P|<a0.
- De Sitter domain: P=0, H>0, Lambda=3(2+3beta)H²/2, legitimate timelike unitary clock gauge. Each k>0 treated separately; k=0 rederived from fields.
- Static domain: clock-aligned frozen regular point, E=theta=0; finite background derivatives and potential curvature; high-frequency asymptotics at fixed regular background. Delta!=0 is necessary for shift elimination.
- Initial raw SHA256: `b8bbe82a317018a2182340b92757dc8cb6b733434ea90f3671b8552ec38d6c2f`.
- Corrected raw SHA256: `cdea08d60fb3900b221799e7b4efa1f8e13ce3f529ca55805627fc9ae6cb036c`.
- Requested published base: `8aa3f7046a7ae14a99f3515fd42df5bf061fb1db`. Observed checkout HEAD: `22766173c1985526eb359f809d85a8196401f0ae`; repository has pre-existing untracked/dirty state. No Git modifications were made.
- Independent actor: isolated `round2_independent_reviewer`. Only raw source, skill instructions and Git identity were read before constructing `fresh_derivation.md` and independent code. Author `checks.py` was read only after the independent derivation and independent executable were persisted and the independent run completed. Author report, self-review and coordinator files were not used.
- Fresh derivation SHA256: `7921bdb266017b285eabb4a84050d0fe2a454cc422149104101c1199376fc1da`. It intentionally preserves the initial-input issue and initial provisional verdict; this audit supersedes that verdict for corrected input.

## Dependency graph

ADM definitions -> background lapse/scale equations -> exact second-order scalar geometric expansion -> shift Schur complement -> lapse Schur complement -> weighted integration by parts -> remaining auxiliary elimination -> reduced Q,V -> energy identity and Frobenius recursion -> future reconstruction bounds.

ADM definitions + frozen static covector background -> electric Lie-shift term, divergence/F terms and TT cancellations -> full three-shift Hessian -> determinant/rank locus and Schur complement -> angular margin minimization.

All leaves in these two chains are internal direct calculations, elementary real algebra, or stated background/gauge assumptions. No external theorem/citation is a load-bearing leaf. The late-time recursion is regular singular with analytic coefficients; its two convergent branches are justified in the fresh derivation rather than inferred from finite residual checks alone.

## Obligation matrix

| Obligation | Status | Evidence and limits |
|---|---|---|
| Background includes beta expansion stress | passed | Lapse and scale variation agree; separate stress conserves identically. Bare Lambda versus observed effective density remains distinguished. |
| Actual ADM quadratic, including lapse/shift pieces | passed | Fresh real-mode expansion records every second-order term and cancellation. |
| Time-dependent integration weights | passed | Both d(a³p²)/dt=Ha³p² and d(a³)/dt=3Ha³ are used explicitly. |
| Nonzero-k auxiliary reduction | passed | Divisions require beta,H,p nonzero; exact Q=B+eta p² and V=gamma p⁴+2BH² reproduced. |
| Forward scalar boundedness | passed | E(t)<=E(t0), |sigma|²<=E(t0)/(BH²), |sigmadot|²<=2E(t0)/B. |
| Late-time reconstruction | passed | Both roots 1,2, resonance compatibility, zeta finite, lapse and physical shift decaying. |
| Exact homogeneous scalar/vector/tensor endpoint | passed | Recomputed from homogeneous fields; no artificial longitudinal sigma oscillator at k=0. |
| Transverse/tensor positive quadratic modes | passed | Covector action has a measure, TT action a³ measure; correct damping and tensor speed. |
| Full oblique shift block | passed | Three shifts retained; determinant and inverse independently checked. |
| Potentially omitted TT derivative mixing | passed | General TT matrix has zero trace and k-divergence; electric derivative has no TT term for spatial covector P and Ebar=0. |
| Uniform angular criterion | passed after local correction | Strict > gives positive infimum; equality has pointwise positivity and zero infimum; strict < gives interior negative aligned modes. |
| Delta=0 continuation | passed as exclusion | Rank loss forces qdot=0; no continuation of eta/Delta or regular five-mode count justified. |
| Direct cubic envelope | passed, narrow claim | Only the direct |P|³ term and its sinusoidal averaging factor; not all effective vertices. |
| Uniform k->0 constraint estimate | not addressed | Finite-k reconstruction contains inverse p²; asymptotic boundedness is not a uniform initial-data estimate. |
| All-background degree count, nonlinear well-posedness, halo low frequencies | out of scope | Neither quadratic de Sitter nor static principal reduction settles these. |
| S3 mass/current embedding, PPN/Solar-System, full empirical validation | out of scope | Not supplied by this work. |
| All cubic terms and quantum cutoff | out of scope | Direct potential vertex bound is insufficient. |

## Decisive independent findings

The dangerous scalar signs are resolved only after constraints and both weighted integrations. At fixed k>0 the final positive energy follows analytically; it is not a numerical scan or a frozen-frequency inference. The apparent inverse-p² metric reconstruction is harmless for the two actual late-time solution branches, but cannot be used to assert a k-uniform constraint estimate.

The static covector representation matters: delta E_i=dot(delta P_i)-P_j partial_i shift^j at leading order. With wavevector along z, all three shift components couple to qdot, but TT metric derivatives do not enter this electric term. TT terms in the divergence and lapse coupling vanish separately by k_i h_ij^TT=0 and trace(h^TT)=0. Remaining scalar metric terms are suppressed since zeta=O(q/k); this is fixed-background high-frequency power counting, not uniform control near Delta=0. Thus no load-bearing leading coupling is missing in the stated regular static block.

The original statement 'If the inequality fails ... negative ... inside the cap' included equality and was false: beta=2eta a0²/K gives Delta=1-(u/a0)²>0 at alignment for every u<a0. This was reported immediately. Corrected source now says beta<2eta a0²/K strictly. No change of action or physical convention was required.

## Portable computation and interpretation

Independent executable: `independent_checks.py`, SHA256 `7a39c3810c88a1cfb6b8696daa6b358afee8a9307e5c1d627a0d08df13979aaa`.

Run record: `run/manifest.json`, status **completed**; validated against current inputs using the computation-audit validator. Output `run/results.json`, SHA256 `f69a51a30f86d051cdb19f7e0dd2c253b55c84f639fc5ecfb92b2871b6d1d4a6`.

39 exact identity checks passed under Python and SymPy versions recorded in the manifest. No random samples, numerical tolerance, floating frequency scans, or finite parameter grid were used. Exact scope: rational symbolic ADM/constraint/energy identities; Frobenius coefficients j=0..10 for each root m=1,2; general two-component TT matrix cancellations; complete symbolic 3x3 shift determinant/equations/kinetic complement and angular expression. The finite recurrence checks alone do not establish all-order convergence; that follows from the displayed regular-singular recurrence argument.

Portable rerun, with a new desired output path inside this review directory:

```
python3 core_open_problems_round2_2026_10_20/05_independent_review/independent_checks.py core_open_problems_round2_2026_10_20/05_independent_review/recheck_results.json
```

The original bounded command, exact inputs, limits, elapsed time, hardware and before/after hashes are in the manifest; the declared contract is `contract.json`. The manifest validator returned `valid evidence record (run status: completed)`.

Author-code comparison after independent completion: author `checks.py` SHA256 `ac85902c4e45018a39d0e2d24c9e15051a7aba51524d7028a606dd3d7dc163bc` uses the same correct scalar geometric construction and algebraic static matrix identities. Its static matrix tests start from the proposed block; they do not alone certify absence of omitted TT mixing. The independent derivative calculation above addresses that additional obligation. Author code was inspected but not executed by this reviewer.

Outcome for computation: implementation and exact assertions verified in the stated symbolic domain and finite Frobenius coefficient range. Residual risk is ordinary symbolic-library correctness plus the explicitly restricted physical interpretation. A successful run is supporting evidence, not a claim that all unresolved theory gates are closed.

## Strongest safe conclusion and next obligation

The unchanged candidate passes this exact expanding-de-Sitter quadratic vacuum check, including the homogeneous endpoint, and its regular static oblique principal polarizations have the stated angular coefficients. Strict beta>2eta a0²/K gives a positive uniform Delta margin over the bounded polarization range; equality gives no uniform margin. These are substantive local linear results.

No additional repair is required for these scoped claims after the endpoint wording correction. The cheapest distinct next mathematical obligation is a uniform constraint estimate in a specified function space and domain as k approaches zero; alternatively, a full evolving-background principal calculation would address a different unresolved gate. Neither is silently supplied by this audit.
