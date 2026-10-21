# Scoped independent review and exact-check record

2026-10-20. Final raw-proof verdict: **proved as written within the
explicitly restricted scopes of PROOF.md**. The frozen microscopic
normalization target remains unestablished. This review supports the
partial constructions and the diagnosed failures of particular
completions, not a universal exclusion or a complete quantum theory.

## Raw proof review

The main reviewer independently reconstructed A-C from the raw artifact:
the band integrals, critical cancellation, derivative asymptotes, static
Hessians, paired amplitude and reciprocal minimum, sheet-pressure boundary
term, direct continuum bubble, gradient factors and source-scale ratio.
It checked the Clifford mass implementation and the distinction between
a dynamical Gross-Neveu order parameter and an imposed gradient mass.

A fresh isolated reviewer `two_field_raw`, supplied raw proof and primary
source identifiers with `fork_turns=none`, reconstructed D. This included
the entire radial/phase L2 expansion, time Hessian, completed V2, canonical
H2, finite-cutoff saddle derivative, charge susceptibility, characteristic
polynomial, source-force dictionary, stress and timelike radial sign.
It authenticated Mistele v3 Eq. 37 and Appendix B Eqs. 60-64. It never
saw checker code or author route narratives.

A separate fresh isolated reviewer `constraint_raw`, also
`fork_turns=none`, reconstructed E from its action without code or author
route narratives. It checked the saddle, reduced energy, both Hessians,
constraint matrix and physical bracket, exact force, kinetic-regulator
tachyon and J-deformed infrared expansion.

Review forced these substantive qualifications before final evidence:

- The empty-vacuum value V0 belongs to the regular finite-positive-cutoff
  amplitude parent. The fractional EFT has a different constant value;
  the zero-cutoff parent origin is singular. None fixes V0.
- The continuum bubble requires a continuum or sufficiently smooth local
  UV realization. A homogeneous finite band does not define its unique
  nonuniform response; hard projection can produce nonanalytic boundary
  terms. This correction narrows a formerly excessive finite-band claim.
- The source flux in D is explicitly spherical, its phase direction is
  defined by grad theta_+, and its susceptibility holds q fixed with
  radial modes relaxed.

The corrected D was reviewed at whole-proof hash `bbd3ecd654d9c9f67ca264fdedb43174f5cbb24a665cca72729b5fcafa043f7f`;
E was reviewed at `1c3584faa4be82103e9578d0f95e2c869eb4cf686cbfcf719ef412a7a46e8710`.
Those sections did not change afterward. The main reviewer reread the
final C correction and issued the hash-specific final verdict below.

## Computation and its limits

The reviewer inspected the checker but did not execute it or see its
outputs during the audit. Review replaced a manually assigned stiffness
control by the derivative limit of an actual changed energy, added the
pressure total-derivative/endpoints check, and added the continuum bubble
limit. The 53 assertions check exact bounded algebra, not all analytical
or physical implications in the proof.

Coordinator execution: final normal **53/53**, exit 0; final mutant
**49/53**, exit 1, precisely K19,K22,K36,K50 failing. The controls change
a physical gap, critical quadratic coefficient, matter-source coupling
and same-sector vacuum term. All remaining checks still pass. Final v2
manifests in `runs/final_normal` and `runs/final_mutate` validate against
the current input hashes. Initial `runs/normal` and `runs/mutate` preserve
the earlier run at the proof hash preceding the final C restriction;
they are historical records and are not current-proof corroboration.

The raw matrix expansion, general-dimensional flux, continuum integral,
threshold and physical-state interpretation are independently audited
analytic/source inputs. K47 implements the n=3 force representative.
No count of passing assertions establishes microscopic health. No scan,
fit, target root search, randomness or source download occurred.

## Exact final artifact hashes

    PROOF.md
    dc9ef43a2e60b0a1f156b06b2091aff4ab6aef7770bdb96b550dc80c3350d6ab
    FROZEN_CRITERIA.md
    9728f282e94cdb579e44fdc2cf9a8f37ed5f07c24cf2b1fcedda4808da0a5e86
    VERIFICATION_SCOPE.md
    09fa68c6da4e858905691308c820cd61f1790566f9119fdda59f5d5a4b968055
    checks.py
    d69d0c79748b3490b8701ce02245f2f5a75a523ace8641e8dbc855bd1cc75f38
    contract.json
    bd84dedb104dcd3a1720a27f1cc350c744632fac59a3a16442d263aabbe6304d

Review-time HEAD was `61f0feb931f8c54897b53ce4677ffc4b995990e6`, with
uncommitted lane artifacts and unrelated concurrent repository work.
Hashes pin the reviewed input; HEAD alone does not. Reviewers made no
edits or source downloads. Agreement is not a formal proof certificate.

Final conservative mathematical self-proofreading covered this lane's
new proof and report: no additional mathematical-token changes, no
unresolved local notation issue. Substantive scope corrections above
belong to proof audit, not proofreading. This was Markdown; no LaTeX
compiler or document build was needed.
