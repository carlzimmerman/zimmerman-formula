# FGF035: coupled zero-flux crossing review

Accepted in the stated diagnostic Q action: for each finite central chi,w,phi,
positive rho_* and fixed positive a_ref,C=4piG,J,cs²,S0, there is a unique
local two-sided solution in the specified positive-density regular class,
with signed MOND flux B crossing zero and genuinely hydrostatic matter.
It has finite local energy and no delta source. Its phi and rho are not H2
across zero, and the full form has no standard product-H1 coercivity bound.
This is an exact local result and a failed applicability gate, not an
observational result or a nonlinear instability theorem.

Signed flux is B=sgn(g)b(|g|,a), a=a_ref exp(chi), g=phi_x,
g=sgn(B)sqrt(B²+a|B|). Varying the even energy gives B_x=C rho,
rho_x=-rho g/cs² and J chi_xx=U'-T, T=|g|b-2W. B is therefore an admissible
coordinate through zero when rho_*>0. The transformed density equation is drho/dB=-g/(C cs²), with rho cancelling
against B_x=C rho.
The square-root singularity belongs to the independent coordinate; state
chi derivatives of g and T remain bounded. A short-interval contraction
constructs a unique C1 flux-coordinate solution, and x_B>0 reconstructs
space. No smooth spatial ODE theorem at g=0 is silently assumed.

For k=sqrt(a_* C rho_*), g~k sgn(x)sqrt(|x|),
phi-phi_*~(2k/3)|x|^(3/2), rho=rho_* exp[-(phi-phi_*)/cs²].
The exact off-center derivative, on both sides, is
[(2|B|+a)C rho+B a_x]/(2|g|)~k/(2sqrt(|x|)). Thus phi and rho are
C1,1/2 and W2,p for p<2 but not H2. This conclusion is not obtained by
improperly differentiating a little-o asymptotic. B is C2,1/2; the scale
source is C1,1/2 and chi is C3,1/2. The gradient cusp changes neither the
continuous positive density nor the actual source equation into a central
point mass: B has no jump. Local energy contains W=O(|x|^(3/2)), not g_x²,
and is finite with bounded scale and matter terms.

The full Hessian retains matter density variation d=-(rho xi)_x, its
cs²d²/rho+2d psi terms, scale gradient/potential, and signed mixed coefficient
q_s=sgn(g)(|g|b_g-b). For Q, q_s=aB/(a+2|B|) and
A=b_g=2sqrt(B²+a|B|)/(a+2|B|)~2k sqrt(|x|)/a_*.
This is a continuous directional second variation on smooth triples, extending
to H1_0; no blanket twice-Frechet differentiability claim on H1 is needed.
Taking xi=eta=0 and psi_delta=sqrt(delta) f(x/delta) gives fixed nonzero
psi-gradient norm but energy O(sqrt(delta)). Hence no positive standard-H1
lower bound holds. Each such energy is positive, and the calculation leaves
weighted coercivity, L2 spectral sign and nonlinear well-posedness unresolved.

Author, root and independent auditor fixed derivations before inspecting the
other new proofs; all start from the task's suggested flux-coordinate route,
so route diversity is not claimed. A separate agent audited root only. Root
then compared the author proof term by term, including both-side signs and
regularity. The root-only audit supplies the explicit factorization
T=|B|^(3/2)F(|B|,a) with smooth F needed for the Holder claim; a continuous
O(sqrt(|x|)) derivative bound alone would be insufficient. Root source bytes
are preserved, and the clarification is credited to that audit. All declared
source/artifact pins were checked. Proof-only: zero
mathematical computation runs/manifests; no numerical solution or spectrum.
Administrative preflight errors (a nonexistent catalog tasks path and a legacy
review missing review_sha256) were corrected and are recorded in the coordinator
receipt; they were not failed mathematical calculations or source mismatches.

The local walls and total mass are induced by the solution. This is not an
arbitrary endpoint BVP, global isolated object, FGF034's fixed-wall H2 branch,
or an autonomous physical-V equilibrium. Both a0 normalizations remain valid
separate positive-reference hypotheses; frozen-H references remain distinct
from constant-vacuum and time-evolving H. The spatial scale response is an
added diagnostic premise, not a derived pointwise vacuum identity. Q alone
is proved here; no RAR/M/filtered-MONO/metric/photon/DOF transfer is accepted.
No missing mass or calibrated empirical result, historical novelty or theory
closure is claimed. Primary AS228 repair ownership remains unchanged.

FGF036 is the next distinct child: construct and audit the weighted closed
coupled form/operator on sufficiently short crossings, retaining fluid/scale
response and center transmission. The integrability of 1/A motivates the
question but is not itself a positivity or well-posedness theorem. It is a
ready specification, not a launched run or accepted conclusion. FGF031 finite
pressure robustness remains stopped pending actual instrument calibration.

## Evidence pins

- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/result.json` SHA256 `a92f785e1642c43d1b9df4030add980ca621b484e20b5d6980a33bb620c4a747`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/DERIVATION.md` SHA256 `5aa9e64b81a9dcaac14926f43c680a82d44d57be838423ccc4b0ebeee1cb1d3b`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/REPORT.md` SHA256 `cf15d52faf8204c4c7a2c8d8c4327b89687d84751f0186d0906935fc0f992950`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/input_sha256.json` SHA256 `b36b28ef156d9500ba7b5e8c8b90a7c82034e9cef1d1d9cf7c2c7abda16e9d7b`.
- `campaign_fresh_gravity_astra/stage_22/zero_crossing/INDEPENDENT_AUDIT.md` SHA256 `982f8975c2fe75190aa569b1f8e45b4c8791f002692c968eca542183d5f81241`.
- `campaign_fresh_gravity_astra/stage_22/zero_crossing/PROOF_COMPARISON.json` SHA256 `c7c90b85bb2a747eddffd4d70272b279ea4969216caeabeaaebc90fa1a99d01f`.
- `campaign_fresh_gravity_astra/stage_22/zero_crossing/PROOF_RECORD.json` SHA256 `69cf27d5011cc82fcb0ba30df8d3f59697ff0900937775e521e94613bc4e3013`.
- `campaign_fresh_gravity_astra/stage_22/zero_crossing/ROOT_DERIVATION.md` SHA256 `3631b24829052f30e1d2935615ec5f9316b4773f54b9e8b9330e59fd3cc286a6`.
- `campaign_fresh_gravity_astra/stage_22/zero_crossing/audit_result.json` SHA256 `d32d36846e911641fcd6fc24ba8c2f98a90931281826fea93988810f5c7f399a`.
- `campaign_fresh_gravity_astra/stage_22/independent_audit/DERIVATION_FROZEN.json` SHA256 `bc7fa7932e12ebb7e1789140a9be1bf9b5d49e58c7e4b9982a92416927cdaf27`.
- `campaign_fresh_gravity_astra/stage_22/independent_audit/FROZEN_CROSSING_DERIVATION.md` SHA256 `2b604f5cb3e1672fbd3407b1559e025b2869da7042338886387a3a8c347eccc5`.
- `campaign_fresh_gravity_astra/stage_22/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `32dc34bf2a829e44d790bd60920c753b204f96511af89405dd42bbc9d7881192`.
- `campaign_fresh_gravity_astra/stage_22/independent_audit/audit_result.json` SHA256 `11463472b5520cede6440823923bd1d44e76035eec7716c9507e56d3e658b553`.

Reconciled 2026-09-30T16:41:19.125576+00:00.
