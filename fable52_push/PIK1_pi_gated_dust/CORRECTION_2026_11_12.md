# PIK1 forward correction: the quadratic action was missing

This correction supersedes the **present interpretation**, not the historical
frozen criteria or historical label, of `RESULT.md`. The original NO VALUE / NO
VALUE verdict remains visible as history. **Current status: the claimed universal
linear invisibility is REFUTED; universal NO VALUE is NOT ESTABLISHED.**

The executed derivation and its scope are in
[the corrective result](../../research_closure_2026_11_12/combined_route/pik1_corrections/RESULT.md).

The old argument expanded the action only to first order. A linear action term
being a spatial boundary does not remove quadratic action terms; it is the latter
that determine the linearized equations. For
`F(Q) = C (Q-1)^2`, `C = mu_K^2/(2K)`, unitary clock gauge gives
`Q=q/N`, `P^0=0`, and `Pi=(sqrt(h))^-1 d_i(sqrt(h) P^i)` exactly. At a fixed FRW
time the new bulk quadratic density is

    Delta L2 = B alpha div(P) + (D/2) [div(P)]^2,
    B = C (1-q^2) S'(0)/Pi_c,
    D = C (q-1)^2 S''(0)/Pi_c^2,

where `alpha=N-1`; the overall `a^3` volume factor is understood. Metric-trace
terms combine into a spatial boundary. Both terms generally change linear
equations. Direct variation of the exact exponential gate and variation of this
quadratic action agree identically in the new check.

For `S=exp(-u)`, the fixed-metric, frozen-background principal sector has a
negative-kinetic / negative-frequency-squared band for generic parameters just
above `k^2=K/D` when `q>1`, `gamma_L=0`. **This is not a full coupled-gravity
instability theorem.** The metric constraints, the physical threshold/cutoff and
the original one-sided stiffness still have to be treated.

A flat gate such as `exp(-u^3)` has `S'(0)=S''(0)=0`, so it avoids that quadratic
FRW correction. It does **not** automatically avoid the obstruction in a halo:
its curvature is positive for `u>(2/3)^(1/3)`. The finite-density calculation
proves loss of positivity/invertibility of the fixed-clock polarization block
if `F(Q) S''(u)/Pi_c^2` exceeds the active stiffness and the relevant wavelength
is inside the theory's domain. It does not prove the full constrained system
has a ghost; the coupled constraints remain the next obligation.

Fixed finite stiffness cannot keep that P block positive for unrestricted
independent `Q>1` and Pi, because `F=C(Q-1)^2` is unbounded. A proposed rescue
must derive a joint allowed-state domain A and satisfy
`Pi_c^2 >= sup_A {F(Q)[S''(Pi/Pi_c)]_+}/gamma_L` for an all-wavelength block
guarantee, or provide the applicable physical wavelength bound. The current
action and frozen criteria supply no such preserved joint domain. This is a
design condition, not a full-system instability conclusion; correlated
physical states could restrict the product. See the executed continuation in
the corrective result.

The original dominant-radius ordering argument is a heuristic until it orders
the actual weighted radial distributions. Its two endpoint values do not alone
order averages with different profiles and weights. The stated nonmonotone
shape failure was not computed. The original numeric table also misstates
`r_M` at `10^13` and `10^14 Msun`: the displayed formula gives about 122 and
386 kpc, not 387 and 1220 kpc. This does not reverse the qualitative endpoint
density ordering, and supplies no successful static model.

**Still not evaluated:** the promised 7-cluster / 35-point builder, groups,
self-consistent capped galaxy solves, revised cosmological clustering bound,
and full covariant stress/current checks. The historical source called these
algebraic statements certified despite disclosing an unfinished pipeline.
They must not be carried as executed certification.

The malformed `pik1_var.py` and incomplete `pik1.py` drafts are unchanged in this
folder, as first committed. The bounded quadratic check is
`correction_2026_11_12/check_quadratic.py`, with its output and two mutation outputs beside it.
The frozen criteria have not been edited. No old result has been promoted to a pass.

Adopts no new theory. kappa = 1/2 remains FITTED.

*Audit note, 2026-11-12 (lead session):* this notice was written by another session and is committed here on the owner's instruction after an independent check, `reviews/codex_corrections_audit_2026_11_12/C2_pik1_and_frm1.md` (grade: CORRECT on linear invisibility, the flat-gate curvature lemma and the stiffness bound; CORRECT WITH LIMITS on the negative-kinetic band (fixed metric) and on NO VALUE not being established). The finite-density and stiffness-bound checks this file relies on are in the uncommitted folder; the auditor reproduced them on copies and redid the quadratic action independently. The audit adds that the density column of the original table is also wrong, which strengthens the ordering. The folder `research_closure_2026_11_12/` it links to was not committed with it, so those links may not resolve; the audit file is the checked record. The committed text, labels and outputs below this notice are not edited by this commit.
