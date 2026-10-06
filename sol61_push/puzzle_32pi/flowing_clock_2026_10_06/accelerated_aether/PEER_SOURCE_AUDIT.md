# Independent source-asymptotics audit

Verdict: the exact stationary Euler and current dependency equations are consistent with the stated covariant action. The leading P2 exterior is a supported formal balance, not an exact solution or a proved baryon-normalized MOND force. No blocking algebra error found. This is a reconstructed proof audit; I did not execute peer scripts or perform new astronomy.

## Covariant reduction and exact Euler checks

In unitary phi=qt, sqrt(-g)=NBr², g^rt=V/N², and G=-2cN/(3Hq). Therefore the integrated -G boxphi term becomes -2c Br²V Nprime/(3HN), as stated. The spatial Ricci scalar 2(1-B^(-2))/r²+4Bprime/(rB³) reduces the EH spatial action to M[N(B+1/B)+2rNprime/B]. KijKij-theta² gives -MrV²[Bprime/N+B Nprime/N²] after integrating the V Vprime term. The physical matter metric is therefore the same varied metric, with no extra scalar fifth force assumed.

Differentiating this reduced action reproduces the report's V equation and B,N Euler equations. In particular variation of N in NBr²U gives Br²(U+N Uprime)=Br²(U+2c); variation of a=Nprime/(NB) gives Br²(Q-aQ_a)-(r²Q_a)prime in the N equation and Nr²(Q-aQ_a) in B. The braiding N variation gives +2c(Br²V)prime/(3HN), fixing its sign. Unit-clock stationary acceleration a must not be identified with stationary metric-observer force.

## Independent Noether reconstruction

A stationary radial-dependent time diffeomorphism xi^t=epsilon(r), preserving areal r, produces

    delta N=NV epsilonprime,
    delta B=-BV epsilonprime,
    delta V=(N²/B²+V²)epsilonprime,
    delta phi=-q epsilon.

With canonical current j^r=-Euler momentum/sqrt(-g), scalar Euler variation contributes +qNBr²j^r epsilonprime after integration by parts. Covariant invariance therefore gives

    qBr²j^r+V E_N-(VB/N)E_B+(V²/N+N/B²)E_V=0.

This reconstructs the exact reported identity without borrowing its symbolic check. All three stationary vacuum metric Euler equations imply current zero pointwise in this ansatz. The identity is stronger than mere radial charge conservation. With actual matter, its source-weighted counterpart must include the physical matter energy/momentum/stress; it does not establish interior matching by itself.

The response-current variation also checks: delta a=(NV psiprime)prime/(qNB) gives deltaL=M r²Q_a(NV psiprime)prime/q, whose integrated scalar momentum is -MNV(r²Q_a)prime/q. Thus j_response=M V(r²Q_a)prime/(qBr²), including the same sign as the metric Noether relation.

## Physical force and leading source hierarchy

Diagonalizing the stationary metric gives F=N²-B²V² and g_rr=N²B²/F. Its observer proper acceleration is Fprime/(2NB sqrt F). At weak order, subtracting the de Sitter force gives g=a-Sprime/2 with S=V²-H²r². The exact action's leading B and N equations yield

    2b-2ra+(rS)prime=0,
    r²[g-a+W_a+eta H v]=m.

The momentum equation, using b=rg-S/2, implies V(rgprime+2g)+eta Hra=0. Thus physical-force identity, nonzero flow and source balance are mutually consistent. One cannot independently choose V=-eta Hr in the full transition.

Under the declared omissions relative to m/r², g approximately a and W_a=m/r² imply a=sqrt[s(s+A)], s=m/r²; the radial equation and momentum fix V=-eta Hr(1+s/A). Its deep leading force has exactly mass exponent1/2 and radial exponent-1. Those exponents are not produced merely by mistaking a for exact physical g: the g-a difference is explicitly estimated and can be smaller than the retained mass flux in the stated overlap. The hierarchy Ar<<1 controls post-Newtonian L²/r relative to m/r², while r<<r_cos controls H²r relative to that flux. These conditions can have a formal small-m overlap; they do not guarantee a matched solution or finite-gradient health.

The remaining caveat is substantive. Exterior m is an integration constant; identifying it with G_N,b M_b requires a regular conserved-source interior with its true ADM momentum and no extra homogeneous metric/clock data. A is prescribed in the response action, not selected from H. The leading exterior tends V=-eta Hr rather than outer de Sitter V=-Hr, so an outer connection is still required. Its small current residual is a combination of subleading metric residuals under the exact identity, not an extra independent charge obstruction or a proof that corrections exist. Thus the report's formal-exterior advance and its missing implication are appropriately bounded.

Observed HEAD: `c9d9a1d7b7a7accbf773424a5180f35ac85896f4`. Inspected source SHA256:

- `sol61_push/puzzle_32pi/flowing_clock_2026_10_06/source_asymptotics/REPORT.md`: `f4b7408899ed34271f974db637b038a8dbe60c936ebd4f0b93a2dab670ff0ea1`
- `sol61_push/puzzle_32pi/flowing_clock_2026_10_06/source_asymptotics/checks.py`: `19d5f3c694f9dc590fa281b15567587c81af69871ff2ef3c06399bf1f2f9730c`
- `sol61_push/puzzle_32pi/dynamical_sector_2026_10_06/kinetic_braiding/REPORT.md`: `f60cc5a4940fbd311e4cab34f1be7e60db186b51e3344cb92048c394e8596a1b`
