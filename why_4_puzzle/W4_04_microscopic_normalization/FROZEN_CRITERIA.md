# W4-04: microscopic normalization selector

Date: 2026-10-20. Base supplied to independent routes:
`e8bb2ae70ad6b2c86790b9312861ac2269227f71`. Concurrent unrelated work exists.
This criteria file must be committed alone before any checker is created.

## Target

Find a physical principle that actually selects xi=1/4 in
`a0^2=xi G epsilon_DE`, epsilon_DE=rho_DE c^2. The operational definition
is the deep-MOND force coefficient `g^2=a0 g_N` in spherical isolation;
a Compton acceleration, Born-Infeld saturation threshold, or a differently
named half does not satisfy this definition without a derived bridge.
No measured a0, kappa, cosmological ratio, cutoff fit, or target-derived
scale enters upstream. No scans of dimensionless knobs.

Standing status: kappa=1/2 FITTED; CFG493 reports kappa_Lambda=0.417+/-0.095
and kappa_crit=0.345+/-0.078 on distinct footings, never pooled. This lane
uses the dark-energy footing and no measured input to select a coefficient.
The campaign significance rule is inherited, not reinterpreted.

Authorities: why_4_puzzle/README.md;
W4_02_independent_portal_audit/PROOF.md, REVIEW.md and HANDOFF.md;
campaign_fresh_gravity/CFG894_kappa_campaign_ledger/
KAPPA_CAMPAIGN_RULES.md, KAPPA_DOORS.md and KAPPA_ATTEMPTS_LEDGER.md.
W4-02's restricted pi-grammar correction applies; no unrestricted H-only
parity no-go is invoked. No duplication of reserved p63/four-form/Lean work.

## Mechanisms and decisive tests

R1 LOCAL SUSY: replace the prior fixed-metric symmetry premise by local
supersymmetry, whose transformations include the metric. Work explicit
positive-vacuum nilpotent SUGRA and locally supersymmetric BI/FI models.
Derive their absolute vacuum versus nonlinear tension relation, retain the
superpotential/gravitino parameter, canonically normalize the matter
source, and solve the sourced static force. A locked tension is creditable
partial progress but not MOND or a coefficient selection. Test whether an
admissible fixed-vacuum deformation or an independent canonical source
coupling survives.

R2 COMMON MICROSCOPIC INDUCTION: compute vacuum, gravity and response from
one specified field content/state/measure. This strengthens generic
heat-kernel moment approaches (K169,K181,K356), rather than repeating
regulator freedom. First determine whether the exact low-gradient action
contains the required nonanalytic cubic. A massive four-dimensional
determinant is analytic near zero; test massless and thermal zero-mode
escapes instead of assuming their dimensional powers are interchangeable.
If a cubic exists, retain the source/dispersion couplings and signs.

R3 STRING/BRANE UV NORMALIZATION: replace independently chosen BI couplings
by actual D3 DBI+CS+bulk-gravity coefficients. Derive the physical force
using the canonical source and its actual mass; retain compactification
volume, string coupling, separation, moduli and uplift data. The total
four-dimensional vacuum is not automatically a brane tension. Test whether
BPS cancellation or stabilized dS removes rather than hides these freedoms.

R4 OPERATIONAL AMPLITUDE RATIO: for a single static mediator with source
q rho phi, physical acceleration q|grad phi|, high-gradient energy C2 g_phi^2
and low-gradient energy C3 |g_phi|^3, derive force-calibrated G and a0 in
n spatial dimensions. The candidate invariant is

    G_n=q^2/(2 Omega_(n-1) C2),
    a0=2q C2/(3C3),
    xi=8 Omega_(n-1) C2^3/(9 epsilon C3^2).

These must be checked by flux integration, not assigned by naming a
threshold. A common overall factor (species number or hbar) should cancel
from the invariant. This is a sufficient calculation target for microscopic
models, not itself a selecting principle. Do not import it into a model
where the measured G includes an independent tensor sector without deriving
the modified dictionary.

## Option spaces and inputs

All dimensions/couplings remain symbolic. R1, R2 and R3 start `free`; there
is no probability assigned to their continuous parameter space and no
determinate trial until all operational bridges exist. R4 is a conditional
reduction (`audit`), not an exact candidate. Canonical field redefinitions
must not change any physical result. The laws of a named microscopic action
are inputs with exact primary-source equation/version provenance; any added
matter or MOND dictionary is explicitly a hypothesis. No source downloads.

pi/hbar: R4 carries Omega_(n-1) unless actual microscopic coefficients
cancel it. Common hbar factors can cancel in its amplitude ratio; display
remaining hbar powers rather than declaring quantum mechanisms excluded
solely because they were obtained by a loop. R1 and R3 are dimension-specific
where their supersymmetry/duality requires it; the dimensional limitation
must be explicit. R4 and the determinant power law supply general-d tests.

## Success, failure and independent observables

Success requires an operational a0, force-calibrated G, physical vacuum
epsilon and a unique xi=1/4 after every admissible physical coupling/state
variation. The same mechanism must fix another independently measurable
quantity, not just density tracking common to all xi. A source-connected
force-law shape, spectrum or additional force amplitude may qualify only
if fixed by the selector and not selected afterward.

Wrong force exponent, unfixed source coupling/modulus, adjustable vacuum
parameter, an independent counterterm, or a cubic with unsuitable sign
means the tested model is not the requested selector. Do not conclude all
microscopic physics impossible. Preserve an actual tension-vacuum lock or
shared-factor cancellation even if the operational bridge fails.

## Declared checks and mutations

Check exact canonical normalizations and static flux laws; positive signs
when claimed; fixed-vacuum SUSY deformation; D3 force/volume dictionary;
the operational amplitude invariant and its field-normalization invariance;
the common hbar/species cancellation; general-d determinant powers.

M1: double the canonical charge-to-mass ratio of a BI probe with tension
and vacuum fixed. Its squared threshold/vacuum ratio must quadruple.
The same rescaling of the single-mediator source q must leave R4's xi
unchanged when both measured G and a0 are recomputed. A single actual force
normalization must be used throughout each model.

M2: keep the locally supersymmetric vacuum V fixed while increasing the
gravitino mass parameter. In the BI/FI model with V=2T-3Mp^2 m32^2,
T must rise by (3/2)Mp^2 delta(m32^2). A claim T=V/2 must fail off the
explicit m32=0 restricted branch.

M3: spatial n=3 -> n=4. The amplitude prefactor Omega changes from 4pi
to 2pi^2; holding C2,C3,epsilon fixed moves xi by pi/2. There is no claim
that a special four-dimensional SUSY theory has an unchanged d=5 extension.

M4: vary the thermal/gapless coupling entering m_eff^2(g). A determinant
power alone must not keep a cubic coefficient fixed if its source coupling
changes. Quantitative sign/power checks will be declared from the explicit
source equations before checker implementation, with any supplement dated.

Separate normal and MUTATE outputs; controls must bite with nonzero exit.
Use bounded exact single-process scripts with one library thread; no heavy
jobs or scans. Record contracts, input/output hashes, software and actual
exit statuses. An independent reviewer must reconstruct a candidate or the
main algebra before a success claim.

Deliver proofs/source checks/route status and a current handoff. Append one
scoped register row per actual attempt, regenerate CFG894 statistics, and
commit only this lane and its own append-only registration/navigation edits.
