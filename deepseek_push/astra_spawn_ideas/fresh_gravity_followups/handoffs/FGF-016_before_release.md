# FGF-016: Kinetic-parameter conditioning against nuisance errors

Status: `awaiting_audit`. This is a proposed child task from an actual returned agent result, not an executed result.

Read `../FRAMEWORK_AND_EXECUTION.md` and `../RESULT_CONTRACT.json`. Preserve the core scale, two normalizations and separate gravity branches.

## Dependencies

Required scoped reviews: FGF-011. Verify that they cover this task's premises; a generic PASS is insufficient. Source proposal: `campaign_fresh_gravity_astra/stage_04/matter_stability/FOLLOWUP_TASKS.md`, SHA256 `f7612247c4867fd8f96ae25a85e6d16717975cff4816676abf85b3f86500a2c4`.

## Worker proposal, retained with its declared assumptions

F3 — quantify when a dynamic rate can identify K

**Question:** how much calibration precision is needed to distinguish K=2
from K=8 using a slow coupled mode, compared with a resolved scalar branch?
Use only MS1's explicitly supported/subtracted toy model.

For each Q/R branch, B/a in {.001,.01,.1,1}, theta in {0,pi/2}, cs/c in
{1e-4,1e-3,.1}, K in {2,8}, and k/kJ in {.3,.5,2}, compute x_± from (M2)
using a cancellation-safe root. Keep 4piG rho0 fixed in a declared time unit.
At fixed physical k, perturb rho0, cs² and L independently by ±1e-4 and
compare finite-difference sensitivities with implicit differentiation of

    (x−cs²k²)(Kx/c²−Lk²)=4piG rho0 k².

Do not change k when differentiating a nuisance parameter just because its
derived kJ changes. Compare hypothetical independent 0.1%,1%,10% calibration
errors, explicitly as synthetic scenarios. For two resolved modes use the
trace inversion K=c²L/[(x_++x_-)/k²−cs²]; for a single nonzero mode also
include density calibration as in (M10).

**Decisive controls:** static threshold and static susceptibility must have
zero K derivative; direct K inversion on noiseless pairs must recover inputs;
finite-difference derivatives must converge when step is halved; reject
threshold modes x=0 as singular single-mode inversion cases.

**Pass criterion:** a compact conditioning table separating formal
identifiability from sensitivity overwhelmed by declared nuisance uncertainty.
Do not describe these invented precision scenarios as observational priors,
a forecast, or a measured bound on K.


## Return and limits

Use a unique claimed run directory under `results/FGF-016/`. Each numerical process has a 120-second wall bound and one numerical-library thread, with actual enforcement recorded. Split larger work into separately bounded runs if necessary. Return the result contract, exact derivation, controls, input/output hashes and failed attempts. No automatic theory acceptance follows from a passing finite computation.
