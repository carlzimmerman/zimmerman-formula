# FRM1 forward correction: scope of the ceiling and of prediction

The historical result, frozen criteria, numerical outputs and labels are
preserved. This note corrects their interpretation. **Current safe statement:
retrospective class-level consistency, with a failed restricted baryon-loss
model; no predictive formation mechanism is established.**

## The ceiling has hypotheses

The lane's general ledger is

    X = X_L(g_b,f; a0) F_C/F_b,
    X_L(g;a0) = [sqrt(1+4 a0/g)-1]/2.

Its ceiling `X <= a0/g_bar` requires the fixed-profile relation
`g_b,f=g_bar/F_b` and `F_C<=1` (the plotted baryon-loss budgets set `F_C=1`).
For `u=a0/g_bar>0` and `0<F_b<=1`,

    X(F_C=1) = 2u / [1 + sqrt(1+4u F_b)] <= u,

with equality approached as `F_b -> 0`. This is a valid channel bound, not a
bound on every separately conserved formation/transport history.

The model explicitly allows `F_C>1` from boundary transport/merging
(`RESULT.md`, original lines 23-28), and does not independently fix `g_b,f`
(original lines 90-94 and 224-228). At `u=1`, `F_C=2`, `F_b=1`,
`g_b,f=g_bar`, one gets `X=sqrt(5)-1>1`, exceeding the restricted ceiling
without a source term. Charge supplied across the boundary must be subtracted
from the supplying region. Alternatively `F_C=F_b=1` and
`g_b,f=g_bar/100` give `X=(sqrt(401)-1)/2>1`; the radius/profile assumption has
then changed. These are scope counterexamples, not physically derived halos.

Therefore the cluster excess over the restricted ceiling does not prove that
all transfers fail, that charge creation is necessary, or that the deepest
wells exceed every possible formation-time amount. The observed offsets and
the failure of that restricted channel remain unchanged. A new transport model
must predict both factors and geometry independently; reading them back from
the observed offset is not a solution.

## The class bands were not unseen predictions

The original disclosure says every DD1 and HIS1 number had already been seen
before these new bands were frozen (`RESULT.md`, original lines 262-264).
Committing the bands before running the new script protects the script's
chronology, but does not make those class outcomes out-of-sample predictions.
The 14/16 canonical and 13/16 alternative hits remain descriptive consistency
checks. The retained raw-frozen FAILS and amended HOLDS EXCEPT labels also remain
as written; fixing an impossible significance clause does not remove prior
exposure to the class outcomes.

The table does not establish history as necessary, does not measure per-system
transport, and cannot use absence of a significant within-class trend as
positive evidence for a no-trend prediction. Likewise a future cluster-redshift
ordering is not determined by conservation alone: it needs a specified
formation field, transfer law and source-time convention.

The symbolic channel bound and both scope counterexamples are checked in
[the corrective calculation](../../research_closure_2026_11_12/combined_route/pik1_corrections/RESULT.md).
No numerical class score or frozen criterion was changed. kappa remains FITTED.

*Audit note, 2026-11-12 (lead session):* this notice was written by another session and is committed here on the owner's instruction after an independent check, `reviews/codex_corrections_audit_2026_11_12/C2_pik1_and_frm1.md` (grade: ceiling scope: CORRECT WITH LIMITS; retrospective bands: CORRECT). The auditor checked the ceiling algebra and both counterexamples independently and confirmed the commit order of this lane's criteria and results. The folder `research_closure_2026_11_12/` it links to was not committed with it, so those links may not resolve; the audit file is the checked record. The committed text, labels and outputs below this notice are not edited by this commit.
