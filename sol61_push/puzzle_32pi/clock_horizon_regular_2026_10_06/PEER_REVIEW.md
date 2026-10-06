# Independent raw-action audit: local horizon regularity

Verdict: accepted in its stated local vacuum scope. The action's derivative matrix is invertible at a finite F=0 horizon whenever Q_gg is nonzero, and the actual positive-gradient detuned P2 family supplies simple horizons for every finite A>0. This disproves selection of A/H by local smooth horizon crossing alone. It does not establish global source/cosmology matching or full physical health.

## Reconstructed determinant, independent of prototype response

Write C=M(n-1)/2, lambda_n=(n-1)/[2(n-2)]. From the literal displayed action,

    partial L/partial Bprime=-C r^(n-2)V²/N,
    partial L/partial Nprime=2C r^(n-2)/B
      -C r^(n-2)BV²/N²+M lambda_n r^(n-1)Q_g
      -b B r^(n-1)V/N.

Thus E_V has coefficient -2C r^(n-2)V/N in Bprime and no Vprime,Nsecond; E_B has +2C r^(n-2)V/N in Vprime and no Nsecond. Only differentiating Q_g contributes Nsecond to E_N, with coefficient -M lambda_n r^(n-1)Q_gg/(NB). Their triangular diagonal product is positive

    M³(n-1)²lambda_n r^(3n-5)V²Q_gg/(N³B).

The exponent is 2(n-2)+(n-1)=3n-5, not a four-dimensional extrapolation. At F=0 the replacement V²=N²/B² gives the stated M³(n-1)²lambda_n r^(3n-5)Q_gg/(NB³). No F factor arises. This calculation applies directly to a generic smooth Q; its validity does not depend on the script's cubic prototype or pass count.

The action dimensions are consistent in units c_light=hbar=1: M has dimension n-1, c and Veff dimension n+1, b=2c/(nH) dimension n, and each per-solid-angle radial L term dimension2. lambda_n is dimensionless and equals1 only at n=3. No missing dimensional n or n-2 factor was found. The report's distinction between vacuum and static-fluid F-denominators is essential and correct.

## Reconstructed actual P2 horizon data and lapse derivative

For n=3,M=H=N=B=r=1,V=-1,c=1.5,b=1, put P=Nprime. Direct shift variation gives E_V=2(Bprime+P)-P, hence Bprime=-P/2. The radial Euler equation gives Vprime=-1-3P/2+J/2, J=Q-PQ_g. Differentiating F=N²-B²V² gives Fprime=2P-2Bprime+2Vprime=-2+J.

I also reconstructed the remaining lapse equation, which the report handles through invertibility. At these data its exact expression is

    E_N=3Bprime-Vprime-1+J-2Q_g
        +(Bprime P+P²-Nsecond)Q_gg.

After the shift/radial solutions it becomes

    E_N=J/2-2Q_g+(P²/2-Nsecond)Q_gg.

Therefore

    Nsecond=P²/2+[J/2-2Q_g]/Q_gg.

This explicit expression independently confirms a finite lapse second derivative for each finite A in the stated family; it does not rely only on a formal determinant.

For actual P2, W_g=g²/[sqrt(g²+A²/4)+A/2] <= g²/A, W_gg=g/sqrt(g²+A²/4)<=2g/A, and W(0)=0 imply gW_g-W=integral_0^g sW_gg(s)ds<=2g³/(3A). With epsilon=.01,kappa=.99,g=.01A,

    J<=g²[4g/(3A)-kappa]<0,
    Q_gg=2[kappa-.01/sqrt(.2501)]>0.

Hence Fprime<-2 for every A>0. The response is smooth on an open neighborhood because g is strictly positive for each such datum. The interval may depend on A; no uniform-radius or uniformly bounded-curvature family is asserted. The A->0 limit itself has g=0 and is excluded from this positive-gradient open-family argument.

## Regularity, interpretation and residual limits

The t-r metric determinant is -N²B², so F=0 is not metric-coordinate degeneracy in the flowing chart. X=q²/(2N²) remains finite. With smooth Q and nonzero Q_gg the implicit solved vacuum vector field is locally smooth and supplies smooth metric and clock fields. Finite Nsecond,Bsecond,Vsecond and physical curvature follow locally. C² response alone would need an explicit local regularity/existence discussion if uniqueness were claimed; the report states smooth response and its actual g>0 P2 family satisfies that premise.

The surface gravity |Fprime|/(2NB) is finite for the chosen stationary Killing generator. Its absolute normalization as a global physical temperature would require specifying that generator's normalization in a completed global spacetime. The report does not make that identification.

No constraint secretly reintroduces F in the lapse principal rank within the declared radial action: all three Euler equations are solved before horizon substitution. The frozen radial equations are the premise here; a separate covariant reduction/current audit remains a dependency if their equivalence were challenged. This review does not assert a theorem for other actions, F-singular matter, response-rank zeros, unit-clock breakdown, or a full propagating-mode Hamiltonian.

No concrete algebraic error was found. The decisive statement is local and should remain local: an open set of regular horizon data for arbitrary A/H defeats that particular local selector, while the unbuilt global boundary-value condition can still restrict parameters.

## Inspected provenance

Observed HEAD: `6988a2ecbab63393c26a160f81ee15a4391d6a0a`.

- `REPORT.md` SHA256 `06ef8672ddecd3ddaeb5b8ce91ab3407557f05e4b88790bf6fa5a6b23f29dd08`.
- `checks.py` SHA256 `e20b1e4c608bf91e0291a7e475757c56d2dad4db96b464a5e27258537e6b5316`.


Read-only inspection of report and checks; no peer runner inputs edited. One independent exact symbolic extraction of the raw four-dimensional E_N corroborated the displayed reconstructed expression; no astronomical or global numerical analysis was performed. Check counts in the parent package were not used as proof.
