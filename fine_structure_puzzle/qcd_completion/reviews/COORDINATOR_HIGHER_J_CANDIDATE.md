# Candidate generic static angular family

Coordinator research derivation, after seeing the completed J1 result. Not coefficient-blind with respect to J1; the generic-J result has not been supplied to the separate higher_angular_family agent before this file was saved. This is a conditional candidate requiring an actual generic angular spectral check, not a claimed completed angular sum or physical prediction.

For J>=2, coupling orbital L to spatial spin1 and isospin1 gives nine spatial tensors; A4 supplies three more. The orbital multiplicities across l=J-2,...,J+2 are (1,3,4,3,1), hence the free regular-column power is 12(J+1). Three normal Robin derivatives reduce the reference boundary power to 12J+9. The wall is 9D+3R; charge separation gives charged 6D+2R and neutral3D+1R.

The generic charged angular spectrum needs verification from the actual Hessian. The expected spectrum, from the two spin-half factors of a self-dual vector operator coupled to monopole harmonics, is

    charged C: J(J-1) twice, J(J+1) four times,
               (J+1)(J+2) twice.

The four neutral values should be J(J-1), J(J+1) twice, and (J+1)(J+2), the ordinary spatial vector plus A4 spectrum in the asymptotically parallel neutral line. J1 is exceptional in charged multiplicity; it does not suffice to infer the generic list. In particular, simply copying scalar intertwiner centrifugal values without accounting for derivative shifts is not a derivation.

For charged U=1-2/r+C/r², the growing zero-energy solution is

    u=e^r/r [1+(2-C)/(2r)+O(r^-2)].

The mixed Robin u'+u/r has the same first relative coefficient. If the generic spectrum above is correct, the vector charged sum is

    a_vec = 8 - (1/2)[2J(J-1)+4J(J+1)+2(J+1)(J+2)]
          =6-4J(J+1).

No neutral C0 channel exists at J>=2. All non-growing neutral modes are L². The audited whole-space kernel has only J0 and J1, so the growing connection map should be invertible at J>=2; Lagrangian isotropy then gives the required charged/neutral ranks. Neutral scattering is delayed at least to relative r^{-(2J-1)}, starting at r^-3. The actual wall must preserve charge separation and have a nonzero leading neutral boundary determinant.

A check of that last condition is available in ordinary neutral vector harmonics. In radial/electric order the free polar growing vectors are r^J(√J,√(J+1))/√(2J+1) and r^(J+2)(-√(J+1),√J)/√(2J+1). Electric Dirichlet and radial Robin give determinant

    -(J+1)(2J+3)/(2J+1) * r^(2J+1),

which is nonzero. Neutral magnetic and A4 Dirichlet factors give total neutral wall power 4J+3. The six/eight charged-column induced neutral tails require the same explicit Schur remainder control as J1, not the assertion that every exponential off-diagonal perturbation is negligible on a growing column.

The general ghost has two charged centrifugal values C=J(J+1) and one neutral value C. Its candidate log determinant first coefficient is a_ghost=2-C. The resulting Gaussian candidate, including magnetic multiplicity, is

    [1/r] log Z_J = (2J+1)[a_ghost-a_vec/2]
                  =(2J+1)[J(J+1)-1].

For completeness, the same candidate leading powers are

    log Dghost=2r-(2J+4)log r+constant+(2-C)/r+...,
    log Dvector=8r-(8J+14)log r+constant+(6-4C)/r+...,
    log Z_J=(2J+1)[-2r+(2J+3)log r+(C-1)/r]+constant+... .

The J1 inverse coefficient agrees with this expression but its leading exponential is exceptional. That agreement is a consistency check only.

Even if the candidate is proved, its fixed-J coefficients cannot be summed naively. A finite sum of the displayed candidate over J=1,...,N grows as

    N²(N+1)(N+3)/2-N,

of order N^4. The growing-mode correction itself has a1=O(J²); the fixed-J expansion is nonuniform already at J~sqrt(r), before the J~r centrifugal transition. No zeta assignment, fitted cutoff, or termwise infinite angular sum supplies a physical vacuum coefficient. A common angular/radial regulator and uniform asymptotics, followed by the physical subtraction and matching, are required. The separate agent is auditing the generic spectral and summation steps rather than taking this candidate as input.
