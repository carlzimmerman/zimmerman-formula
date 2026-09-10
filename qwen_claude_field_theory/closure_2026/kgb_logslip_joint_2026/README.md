# Corrected no-slip target: finite common-action checkpoint

Status: **OPEN theory; this reconstructed joint point is REJECTED by local scalar stability.**

The same action is
S = integral sqrt(-g) [ F(X) R + 3 F_X^2/(2 F) (grad X)^2 + P(X) - G(X) box phi ] + S_m[g].
Here X=-(grad phi)^2/2; G(X) is not Newton's constant. One explicit clock
phi=-t+psi(r), global a0=1 units, no particle dark-matter sector and no
independent per-halo acceleration are introduced. The fitted kappa=1/2
vacuum-scale relation is an input, not derived here.

## New mathematical content

For an areal static metric, imposing equality of logarithmic lapse and
isotropic spatial potentials gives B=(1+rg)^2, g=A'/(2A). Direct geometric
Einstein components give the exact identities

    pr = -g^2/B,       pt = +g^2/B.

This corrects the stronger previous pr=0 target. It is an imposed inverse
geometry, not an independent forward derivation of physical Phi, Psi,
gamma_PPN or a baryonic MOND source equation. Log potentials coincide with
the usual physical weak potentials only at leading order.

For an arbitrary spherical geometry the original three-equation inverse
also simplifies exactly to

    Q=2X+U, p=sqrt(BU), b=B'/(2B), w=F_X X',
    S=4F(rho+pt)/r + 4w(rg-1)/(B r^2),
    Gamma=p r S/(2 Q w),
    W=(B/2)[2F(rho+pr)+2w(g+b)/B+3w^2/(FB)-2Xw Gamma/p].

Here W=w' and Gamma=G_X/F_X. These are action reconstruction coefficients,
not Poisson brackets or scalar kinetic eigenvalues. The original matrix
and actual total derivatives independently check the accelerated kernel.

At eps=(1e-6,2e-6), common X=.5,F=.525, fixed y1=.1, an independently
refined 65-digit solution has

    y2=.180073380202878
    U1=.004754976363819875, U2=.006115565806792504
    F_X=3.299925877810424, F_XX=38.55121961907284.

All seven matching/preservation residuals and both physical third-action
jet gaps are below 9e-62 relatively. This is numerical finite-jet
compatibility, not interval-certified existence or continuation closure.
The original coupled EF principal gives positive time coefficients but

    angular cs^2 = -0.10147060065748, -0.10025492616677.

Thus the tested local scalar branch has an angular gradient instability.
The regular invertible exterior EF diagnostic rejects promotion; a full
matter-coupled physical-frame Hamiltonian analysis is not claimed.
No broader family is excluded by this one point.

## Previously omitted constant-F sector

F_X=0 makes the normalized inverse chart singular but does NOT make the
physical field map singular. The independent direct reconstruction gives

    c=(pt-pr)/(rho+pr), U=2Xc,
    X'=-X[2g+c'/(1+c)],
    P=2F pr, P_X=2F pr'/X', G_X=F p(rho+pr)/(X X').

These follow from undivided current, Einstein and constitutive equations,
with actual radial differentiation for P_XX,G_XX. One regular 65-digit
control is on shell but fails local scalar health. This sector as a whole
remains OPEN; see constant_f/REPORT.md for domains and exceptional cases.

## Evidence and correction

run_001/results.json records every executed suite command, output and exit
status; its manifest pins sources and dependencies. All newly added Python
entrypoints have been run. There are 12 distinct new unit tests and seven
existing general-pressure regression tests. Execution exit zero does not
mean the candidate passes physics.

During verification an mpmath negative matrix index silently returned
zero and temporarily replaced F_XX by zero in post-solve diagnostics.
The final code uses explicit index 6 and converts the root to a tuple.
The earlier apparent higher-preservation failure is withdrawn: the
corrected point passes that finite gate and fails the angular stability gate.

Reproduce from repository root:

    python3 -B qwen_claude_field_theory/closure_2026/kgb_logslip_joint_2026/run_suite.py --result-file /tmp/kgb_logslip_results.json

COMMANDS.json contains the exact audited runner/validator argument arrays.
The source executable checks and generated evidence are confined to this
directory; unrelated concurrent changes are not part of this work.

## Next unavoidable calculation

Search for common-action matching AND a healthy principal simultaneously
over the remaining geometry/clock data, including the direct constant-F
sector; do not spend a large blind scan rediscovering this unstable root.
Any survivor still needs radial and mass-family continuation and a
baryonic interior with common clock boundary normalization. Only then
can the same action be tested for Dirac constraints, matter Ward identity,
full physical stability, PPN, GW and FLRW/CMB. No new Lean certificate
or empirical prediction is claimed in this checkpoint. There is no
defensible percentage reduction of unrestricted theory space.

