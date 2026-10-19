# FSP010 independent global/sea review

The normalized claim audited is the finite Wilson SU(3) vacuum on
K_n=boundary[0,n]^5 and the separately specified integer-flavor ambient-phase
charged hopping model. **Primary verdict: computationally verified only in a
stated range.** The analytic first coefficients and Hodge identity pass. The
complete pure-gauge series through beta^9 is accepted only on K1, where the
author's exhaustive no-free-edge support search applies. Physical round-S4
QCD A, its charge derivative, R, and alpha remain unevaluated.

One wording restriction is necessary throughout: the pure-gauge phrase
"all connected supports of at most nine distinct plaquettes" means connected
supports **with no singly occupied edge**, after the trivial character is
factored out. Unqualified, that sentence is false: any one plaquette is a
connected support. The code implements the qualified population, and its
mathematical use is correct for that population. This is a precision issue in
REPORT/CONTRACT prose, not an omitted SU(3) branch in the actual search.

## Independent provenance

PRETARGET.md and pretarget_pins.json were saved before opening either target's
proof, code, verdict, or results. The independent calculation began solely
from task definitions. Source identities and the SU(3) center/epsilon
selection rule were checked next, and source_checkpoint.json was saved while
target contents were still unopened. Target metadata hashes supplied by the
coordinator had been exposed; this is recorded, not called proof exposure.
The first target-content read followed target_pins_before.json at
2026-10-19T17:53:47.760961+00:00. A pretarget timestamp typo and stray plus were
corrected before any target read, with original and final hashes retained.

After target exposure, independent_check.py was newly written without author
imports. Its code, contract and inputs were frozen before the bounded v2 run.
Thus the first critical derivation is independent before exposure; the later
numerical implementation is an independent construction after exposure. It is
not a wholly blind implementation, and shared-model error remains possible.

## Dependency and obligation matrix

| Obligation/arrow | Evidence | Audit disposition |
|---|---|---|
| Cubical definition -> cell counts | Direct combinatorial formula; target cells n1,2,3; primary Appendix | Passed for formula and stated finite ranges |
| Topology -> rank d1=N1-N0+1 | K_n homeomorphic S4, H1=0, connected; finite rank controls | Passed analytically; prime/F2 checks are consistency controls |
| Nonlocal minimum -> cube beta6 | Pretarget geometric free-edge argument and exact Haar pair integral | Passed; triple-link epsilon allowed, no global mod2 claim |
| All closed candidates <=9 on K1 -> forty cubes | Target exhaustive constraint recursion, code audit, retained run | Computationally verified only at n=1, cap9 |
| Cube -> full beta9 K1 series | Character orthogonality and irrep onset; exact moments | Passed conditional on that finite support classification |
| P9 -> rigorous absolute endpoint interval | |V|<=80, Taylor theorem, Jensen, rational arithmetic | Passed at beta=10^-6 on K1 |
| Defined hopping -> beta kappa4 cosine | Direct length-four loop signs and multiplicities | Passed for exact graph definition |
| Cosine -> u beta kappa4 W coefficient | Haar pair contraction, normalized Gaussian | Passed; includes current/contact sum |
| Photon covariance -> weighted trace rank | Exact projector identity; independent rational inversions | Passed for positive common weights; finite controls at K1 |
| Finite coefficient -> physical continuum QCD | No smooth-spin/taste/light-mass/renormalization bridge supplied | Not addressed, and correctly excluded by targets |
| Missing n3 term -> global zero physical A | Requires all orders and controlled common physical limits | Out of scope; no such implication accepted |

The dependency graph has definition leaves (geometry, actions, integer
determinants), elementary Haar/Gaussian algebra leaves, primary-source
convention checks, and a finite support-enumeration leaf. No physical
conclusion is permitted to bypass the last row's missing bridge.

## Critical coefficients and SU(3) completeness

The counts are
N0=10n^4+20n^2+2, N1=40n^4+40n^2, N2=60n^4+20n^2,
N3=40n^4, N4=10n^4. For normalized Haar and exponent
(beta/6)(Tr U_p+Tr U_pdagger), one oriented six-face cube integrates to
3^(8-12)=1/81. Both coherent orientations give beta^6/1889568 per cube in
log Z. No factorial is missing: the six distinct plaquette choices cancel
the exponential's 6!.

The SU(3) invariant integral UUU=epsilon epsilon/6 directly disproves a
general parity-only rule. PRETARGET.md instead establishes a geometric bound:
a no-free-edge square support has at least four squares in some axial slab
and two distinct end caps; equality is an elementary cube. At degree six,
the six distinct faces each occur once and every edge has two insertions, so
only the coherent pair contractions survive. This argument gives the first
nonlocal coefficient for every n; it does not claim general-n completeness
through beta9 or classify higher branched networks.

The author search at compute_closed_v2.py:104-137 uses each minimal occupied
face as a root and bans smaller roots. For a dangling edge it branches over
every nonempty subset of its remaining incident faces, and bans the omitted
ones. A target solution is retained on the branch choosing exactly its own
remaining faces; no branch forces edge valence two. When a support closes,
the recursion also adds adjacent faces to reach possible connected supersets.
Induction on the remaining target faces proves coverage for the explicitly
bounded connected no-free-edge population. The retained run visits 45,076
nodes and returns forty elementary cube boundaries through cap9 on K1.

After factoring c0 per plaquette, a degree<=9 contribution has at most nine
nontrivial-character faces. Each cube edge has two such faces, so irreducible
orthogonality makes the representation common, up to duality, over the cube.
Only fundamental/antifundamental start at degree one; other nontrivial irreps
start at degree>=2 and hence cube degree>=12. Two separate cubes also start
at degree12. Thus on K1 the accepted result is
log Z=80 log c0+720 v^6+O(beta^10), with v as defined by the target.
The coefficient and full rational series agree with the independent Weyl
constant-term calculation through the exact tested degrees.

## Endpoint, sea coefficient and geometry scope

Let V=sum_p ReTr U_p/3 on K1. Then |V|<=80 and Haar mean V=0.
For beta=10^-6, x=80 beta<1, Taylor's theorem bounds the exact ninth-degree
partition polynomial P9 by |Z-P9|<=x^10/[10!(1-x)]. Jensen gives Z>=1,
and exact rational arithmetic gives P9>=1. Since log has derivative<=1 on
[1,infinity), the same bound controls |log Z-log P9|. The independently
recomputed bound is about 2.95918e-48, approximately 1.39789e-7 times the
leading collective beta6 term. This is a valid tiny-coupling finite-lattice
interval, not a physical-QCD truncation bound or a uniform large-n estimate.

For the separate sea definition, each plaquette contributes
kappa^4[Tr U_p exp(i e q_f F_p)+h.c.] in log det. The first color term and
Gaussian characteristic function therefore give

  [u beta kappa^4](-log Z)=(sum_f q_f^2)/6 * sum_p w_p C_pp
                        =(sum_f q_f^2)/6 * (30n^4+20n^2-1).

Here C=d1(d1^T Wd1)^+d1^T; W^(1/2)CW^(1/2) is an orthogonal projector.
The theorem needs positive weights and the same weights in color and photon
actions; independent color/photon weights would not cancel in this way.
The current-current and contact contributions are combined by the second
derivative of a complete loop. The target's direct matrix control explicitly
contains H'' and both H' factors. Its four controls are on a single square
with diagonal SU(3) color phases, not a full dense K_n fermion determinant
evaluation. The analytic loop reduction supplies the full coefficient.
No flat Wilson spinor factor16 or physical taste multiplicity is admissible.

At fixed a,beta,kappa, the displayed count-polynomial dilation stresses
differentiate consistently. In the sea sector the constant -1 differentiates
away and the resulting density is beta kappa^4 S_Q/a^4[1/2+1/(6n^2)].
In the shown pure-gauge local/cube sectors only n4 and n2 appear. The absence
of n3 in these coefficients implies absence of a formal n^-1 term there.
The radius is discrete before interpolation, curvature is polyhedral, and
fixed bare parameters are not a matched continuum physical trajectory.

## Execution audit and remaining gap

The author run ranges were checked against actual iterators: pure-gauge
counts n1,2,3; chain and ranks n1,2 over primes1009,1013; supports only K1
through9; moments all66 pairs of total degree<=10. Sea code enumerates
n1,2,3 with F2 ranks, all square starts/orientations; it inverts two n1
tree-gauge Gaussians at 40 decimal digits with1e-30 tolerances. Its direct
hopping controls are four charge/flux pairs. These numerical controls are
conditional on their stated tolerances; the analytic statements do not rely
on interpreting F2 or prime rank equality as a real-coefficient proof.

All three retained author v2 manifests validate with current input/output
hashes and completed status. They were audited and validated, not rerun by
this reviewer. The fresh independent v2 run completed 233 exact checks in
0.551449s, Python3.9.6 standard library, macOS arm64, no RNG or external
dependencies. Caps were55s wall,45s CPU,64KiB output, one conventional thread,
and no RLIMIT_AS. Its manifest validates unchanged inputs and output hash.
It checks all66 trace moments by a separate Weyl-Laurent method, reconstructs
the rational series with a different logarithm recurrence, and exactly
inverts two49-coordinate K1 photon Gram matrices (all weights1, then one
plaquette weight2). Both weighted traces are49; uniform variances are49/80.
All80 independent square phase products are-1. Formula values for n2,n3 are
explicitly not fresh cell enumeration. No fresh independent cap9 enumerator
was executed; the finite-support result rests on the reviewed author search.

No mathematical counterexample was found in the normalized finite claims.
The smallest remaining physical implication is a controlled identification
of these actions and their normalized metric/charge trajectory with physical
curved QCD, including quark spin/taste, light masses, local matching, scale
setting and continuum/radius limits. The cheapest checks for the present
packet are the manifest commands in REPRODUCE.md; extending beta/n bounds
does not close that physical bridge. Primary-source applications and their
limits are recorded in SOURCE_CHECK.md and SOURCE_TARGET_CHECK.md.
