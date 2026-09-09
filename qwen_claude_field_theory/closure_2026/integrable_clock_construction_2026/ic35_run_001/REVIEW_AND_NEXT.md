# IC35 terminal review and next calculation

Base 2b8d5dd4169a4fa62c87f2ed6ed7d2e50e72a239.
Full original theory target **OPEN**. Self-review, not independent or formal certification.

## Strongest result

The independently varied lapse and unmultiplied w equations have second-jet matrix

    M = 4v exp(-2Q) [[1-u^2,1],[-(2-u^2),-2]],
    det(M)=16v^2 u^2 exp(-4Q).

The first time-preservation equations, after the actual auxiliary and momentum
chain rules, have matrix M1=M diag(1,gamma) for (Sdot'',q''), with

    gamma=A^2/[2(2D+12E4 z^2)]>0,
    det(M1)=gamma det(M).

Both determinants are computed from the varied equations and checked against
these simplified forms. This removes an immediate local algebraic obstruction
on the stated regular u>0, A!=0, Fz>0 branch. These are NOT Poisson matrices
and do not establish a Dirac count.

The resulting ODE construction selects the clock profile by Cdot=Wdot=0,
rather than assuming that an arbitrary spatial interpolation has regular time
derivatives. Tested profiles cross the actual switch while satisfying undivided
initial and first-preservation equations with ell=elldot=0.

## Terminal execution

| Job | Child exit | Runner exit | Wall seconds | Meaning |
|---|---:|---:|---:|---|
| collar | 2 | 1 | 71.280461 | Nine scoped checks true; strict mode retains full-theory OPEN |
| tests | 0 | 0 | 294.719769 | 416 tests; unittest elapsed 294.101 seconds |

Both manifests validated with exit 0 using the repository root. Input and output
hashes match. This establishes provenance, not the mathematical interpretation.
Both jobs are terminal. Caps: 420 seconds wall, 2 MiB logs, one cooperative
numerical-library thread; no hard memory or affinity cap. Exact commands are
in run_index.json.

## Two distinct families: do not pool their claims

1. The prescribed C3 smoothstep family runs from q=0 to the reference
   cosmological q on widths .01 and .02. It solves spatial constraints with
   ell=0 and spans alpha^2 from 0 to 3.9217386545996513.
   Its time extension is NOT established and its inner data are not certified
   as a static MOND galaxy. Actual qdot/shdot are nonzero in general.
2. The first-preservation-selected family determines q'' jointly with
   Sdot''. Its widest collar spans alpha^2 from .24551880406590093 to
   .8603357656612876, reaching both eta=0 and eta=1 plateaus. This family has
   q from -1.2907827763779491 to -.689543315752672, NOT from q=0 to the
   reference cosmology. It satisfies first preservation, not full evolution.

No claim may combine the first family's endpoint values with the second
family's preservation result as if they were one matched solution.

## Numerical evidence

For the widest first-preservation-selected collar (width .006, 801 audit points):

- maximum relative dense-solution spatial ODE defect: 1.1893582164000785e-10;
- maximum independently differentiated initial-constraint defect:
  1.3065753811300118e-9;
- maximum directly solved Cdot/Wdot residual: 1.0018652574217413e-12;
- independently differentiated momentum-preservation defect:
  1.8000634051555652e-9;
- maximum numerical error in the Qdot'' coefficient identity:
  1.4384327062799684e-14;
- minimum singular value of M1: .007909385404375895;
- S interval: [.10247069711874207,.10247765824903533];
- Sdot interval: [0,5.507180873172812e-5].

Other tested first-preservation widths are .002 and .004. All satisfy the
declared checks. The 401/801 comparison changes audit sampling and finite-
difference spacing, NOT the underlying integrator tolerance or step cap.
Some finite-difference errors increase with tighter spacing. No monotone
convergence or interval error enclosure is inferred.

The prescribed .01 collar's independent momentum residual is approximately
2.9e-8 even though its directly solved auxiliary residual is approximately
1.8e-14. These are different diagnostics and must not be conflated.

The formal u=0 second-jet matrix has computed rank 1. That algebraic result
does not supply D(S) at that point or resolve the physical zero-field stratum.

## The crucial near-switch caveat

As eta tends to zero, an absolute W residual divided by eta can be arbitrarily
large. This computation NEVER uses ell=-W/[eta exp(S)] as a numerical
regularity certificate. It specifies ell=elldot=0 and constructs the undivided
equations at the algebraic/ODE level.

The numerical runs approximate that construction; they do not give uniform
relative control down to arbitrarily small eta. The first family samples
positive eta as small as approximately 10^-289.5, illustrating why tiny absolute
residuals alone would be inadequate. Exact continuum regularity, conditioning
of the full mixed-branch evolution, and all higher preservation remain open.

## Verification and self-review

Three tests first failed for missing functionality. A read-only NumPy
broadcast view caused the first collar test to error on an in-place qdot
update; replacement by an ordinary addition repaired that implementation bug.
Targeted tests then passed. The main prototype and the wider .006 pilot ran
before freezing the final contract and reproduce in the recorded results.

Mathbox computation-audit kept the algebraic residuals, independent differential
checks and full-theory requirements separate. Mathematical self-review checked
the q'' cancellations, explicit r-derivative terms, matter response and
multiplier-conditioning caveat. Proofreading covered IC35_SWITCH_COLLAR.md
and these equations; no extra mathematical-token repair was needed.
No independent reviewer, external novelty audit or Lean certificate was used.

## Next unavoidable calculation

Derive SECOND time preservation and test whether these first-jet data have a
regular nonlinear continuation through the moving activation interface.
Check the coefficient representation's differentiability before taking higher
derivatives; the numerical D function is C2, and no higher global regularity
may be assumed at its joins.

Then solve actual mixed-branch time evolution and physical inner/outer matching.
Neither family is yet a galaxy plus FLRW solution. Full functional Dirac
closure, a healthy separately counted clock, PPN/measured G, zero modes and
zero-field limits, causal response/strong coupling, global coefficient
extension, and empirical galaxy/binary/cluster/CMB tests remain requirements.
The original exponential law and vacuum-scale coefficient were not refitted;
the coefficient 1/2 remains input.
