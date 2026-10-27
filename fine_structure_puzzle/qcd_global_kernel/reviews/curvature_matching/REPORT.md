# Independent curvature-matching audit

**Primary verdict: incomplete, with the smallest missing implication being the
common off-shell operator/source-basis map from the collective-background pion
contribution to the published full curvature running.** The partial contraction
is correct. Its potential-only beta assignment is coordinate dependent. The
source's full `1/2+2Z/3` is **not disproved**, and no source error is established.

## Claim and scope

At a smooth S4 background, use the canonical SU(2) LO Euclidean action with
mass potential `-F2 M2 a0` and aligned-subtracted electromagnetic potential
`u C s`, where `s=a1 squared+a2 squared`, `u=e2`, `C=Z F4`. The nonconstant
pions are minimally coupled canonical scalars, with their constant harmonic
removed. This review concerns the first Gaussian source contraction, its local
curvature UV pole and the counterterm-basis transfer. It is not a calculation
of the complete NLO QCD+QED partition, global response, full R, or alpha.

The isolated review saved PRETARGET_DERIVATION.md before reading the new
chiral_zero_mode or compact_chiral targets. It then authenticated the primary
source and saved SOURCE_RECEIPT.json before opening those targets. The old
kernel_flavor review and all prior science files were left unchanged.

## Decisive independent result

The right-exponential split gives

    <a0>_pi=a0[1-3 Gbar/(2F2)],
    <s>_pi=s+(2-4s)Gbar/F2.

Equivalently, the potential Hessian traces are

    Tr H_mass=3 M2 a0,
    Tr H_EM=(uC/F2)(4-8s).

For d=4-2eps, the local scalar heat kernel fixes

    Gbar_div=(R/6-Mref2)/(16pi2 eps).

Omitting one constant harmonic does not change this UV coefficient. The
curvature pole of the first source contraction is therefore

    L_div,R=R/(16pi2 eps)[M2 a0/4+(uC/F2)(1/3-2s/3)].

This independently agrees with the new packet's source contraction and
curvature residue. In particular the U-independent EM term is indispensable.
It is not removed by having aligned-subtracted the classical potential.

With the ordinary trace and physical quark charges,

    Tr(Q U Q Udag)=u(5/9-s), Q=e diag(2/3,-1/3),

the EM pole is

    R/(16pi2 eps)[(2C/(3F2))Tr(Q U Q Udag)-uC/(27F2)].

Thus even this partial sector requires an independent purely gravitational
charge-spurion contact as well as the orientation-dependent invariant. The
source explicitly omits some pion-independent renormalization terms from its
displayed basis. Such a contact cannot alone repair an orientation-dependent
coefficient mismatch.

In the common bare convention `lambda_div=-1/(32pi2 eps)`, the mass pole is
canceled by `beta13=1/8` for `l13 R Tr(chi Udag+U chi dagger)`. This checks
the strong normalization and the d-4 versus eps conversion. Directly assigning
the **geodesic potential-only** orientation pole to
`k15 F2 R Tr(Q U Q Udag)` would instead give `beta15,pot=4Z/3`, with an
additional gravitational spurion counterterm. This is not a derivation of the
published full beta.

## Explicit coordinate/EOM bridge and its limit

The source uses sigma-model pion coordinates `U=sqrt(1-r2)+i tau.r`. In that
patch

    g^ij=delta_ij-r_i r_j,  g^ij Gamma^k_ij=3r_k,
    Tr H_cov-Tr H_plain= -3r_i partial_i V/F2.

For the EM potential, the plain sigma-coordinate Hessian gives
`(uC/F2)(4-2s)`, while its covariant completion gives `(uC/F2)(4-8s)`.
The plain potential-only assignment would be `Z/3`, not `4Z/3`. The source's
printed full Z-dependent coefficient is `2Z/3`. These three numbers concern
different incomplete/off-shell assignments and cannot be equated without a
complete basis calculation.

The difference of the potential curvature poles is the constant-background
part of the explicit local field redefinition

    delta r_i=-R r_i/(64pi2 eps F2).

Varying the full LO action also generates curvature-kinetic operators and,
away from constant R, derivatives of R. The exact derivative partners are
displayed in COORDINATE_EOM_BRIDGE.md. Source/background definitions and the
measure/collective-coordinate representation must transform as well. It is
invalid to retain only the change of the s coefficient. The source's nonzero
curvature-kinetic running `beta11=1/6` further makes an on-shell extraction
different from reading a constant-background potential alone.

This supplies a concrete partial EOM bridge and rules out treating the
potential-only coefficient as a coordinate-independent full beta. It does
**not** compute the complete derivative/kinetic, redundant-operator, photon,
mixing, ghost, source and measure completion that reproduces the source's
running. No simple charge-trace or epsilon-normalization error was identified;
the charged mass splitting and strong beta13 check fix those normalizations.
The remaining transfer is unresolved rather than rescued by assumption.

## Audit of the new targets and changed admission condition

The frozen chiral_zero_mode derivation correctly calls its result a first
nonconstant-pion contribution. Its formulas `delta W=gT` and, after removing
the aligned massive-Gaussian insertion, `delta W_extra=gB`, agree with this
review at the source-contraction level. Its warning about the distinct zeta
finite part versus the determinant's decoupling scheme is necessary.
The compact_chiral ancestry/RG note likewise correctly leaves the published
k15 transfer open. Neither is certified here as a closed RG-invariant NLO
global calculation.

The admission condition is therefore precise: the partial pion expression can
be used as a specified bare/common-regulator sector, but it cannot be combined
numerically with the global determinant or have its scale dependence canceled
by inserting the printed k15 beta alone. First provide the complete common
off-shell basis, its EOM/field-coordinate map to the form-factor convention,
the metric/source contacts and the finite scheme conversion. Independent finite
curvature LECs remain inputs. A charge difference does not remove a general
u-dependent gravitational contact; it also need not remove a mass-curvature
term because the compact charge tilt changes <a0>.

## Evidence, obligations and provenance

| Obligation | Verdict |
|---|---|
| Canonical pion/charge normalization and first contraction | Passed |
| Scalar curvature heat-pole and strong beta13 cross-check | Passed |
| U-independent gravitational spurion retention | Passed; required |
| Geodesic versus plain-sigma potential/EOM identity | Passed |
| Exact transfer to full printed beta15 | Incomplete |
| Finite common-scheme metric/source matching | Not supplied |
| Full QCD/global response or alpha claim | Out of scope |

The exact bounded run has 35 checks: global SU2 tangent Laplacians, ordinary
charge trace, charged mass normalization, heat-kernel gamma residues, pole
normalization, sigma metric/inverse, contracted Christoffels and EOM-gradient
identities. It completed within a 30-second wall/20-second per-process CPU cap,
with no RLIMIT_AS or installation. Its current mathbox v2 manifest validates.
No target's manifest command was executed. The current chiral_zero_mode and
compact_chiral manifests were separately validated, both completed.

The source is Kubis-Meissner, arXiv:hep-ph/9908261v2 (2001-05-15), equations
(2.2),(2.3),(2.5)-(2.7),(4.1),(4.5),(4.7),(4.8). Its PDF SHA-256 is
`6c4267db298d51fdf8df0205edeaa5dede792b4b014eb88cd2397e58025bdb72`.
SOURCE_RECEIPT.json records exact PDF pages, bytes, streamed extraction hash,
fresh primary version-history authentication and its limits. No broader source
search, remote PDF-byte comparison or erratum-content audit is claimed.

TARGET_HASHES_BEFORE.json and TARGET_HASHES_AFTER.json pin the reviewed target
revision and any concurrent changes; FINAL_PROVENANCE.json records current
validation and exact review-artifact hashes. These pins, rather than a mutable
directory name, identify the audited evidence. No frozen science, old review,
index, author message or Git state was modified.
