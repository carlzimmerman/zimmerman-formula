# Independent original-Euler and force residual review

Verdict: the stored core/exterior states are consistent with the original lapse, radial metric and shift equations when their derivatives are assigned by core.py's RHS. This holds at50-digit arithmetic and separately when the **original binary64 RHS arithmetic** assigns the derivatives. The static-fluid source signs and exact interior physical-force dictionary are correct. This is an independent algebraic/source/pointwise numerical-conditioning audit, not a certificate that the saved interpolant solves the ODE between samples.

The review examines all61 interior and41 exterior samples at each of the two recorded tolerances in `runs/core_200k_b/results.json`:204 states total. The parent inputs remain frozen. No parent solver import, top-level initialization, or ODE reintegration occurs. Only AST-extracted plain definitions `operator`, `material`, `rhsraw` are compiled. One reconstruction retains original Python/math binary64 arithmetic; the other changes arithmetic to mpmath50 digits and decimalizes literals. The original Euler expressions and exact constitutive response are evaluated independently of those definitions.

## Original equations and proper matter variations

Use M=H*=A=1,eta=.5,epsilon=.01,kappa=.99 and U=−3+6eta lnN. Signed a=N′/(NB), F=N²−B²V², and Pq=Q−aQa. For the detuned uncut response,

 s=sqrt(a²+A²/4)−A/2,
 W(|a|)=[|a|sqrt(a²+A²/4)+(A²/4)asinh(2|a|/A)−A|a|]/2,
 Q=kappa a²−2W,
 Qa=2[kappa a−sign(a)s], Qaa=2[kappa−|a|/sqrt(a²+A²/4)].

The independent Euler residuals, divided by M where appropriate, are

 EN=B−1/B+2rB′/B²+[(B+2rB′)V²+2rBVV′]/N²
 +2eta(Br²V)′/N+Br²[U+6eta+Pq]
 −2rQa−r²Qaa a′−Br² E,

 EB=N(1−B^−2)−2rN′/B²+(V²+2rVV′)/N
 −2rV²N′/N²−2eta r²VN′/N+Nr²[U+Pq]+Nr² Pr,

 EV=−2rV[B′/N+BN′/N²]−2eta Br²N′/N+NB³r²(rho+p)V/F.

Here E=(rho+p)N²/F−p and Pr=p+(rho+p)B²V²/F. The response derivative uses a′=N″/(NB)−a(N′/N+B′/B), not a spatially frozen constitutive value.

The matter terms follow directly from δSm=(sqrt−g/2)T^(mu nu)δg_(mu nu), with Killing-stationary proper fluid u^mu=(1/sqrtF,0,0,0). Varying N,B,V gives respectively −Br²E, Nr²Pr, NB³r²(rho+p)V/F. A stationary fluid with zero coordinate radial velocity still has nonzero ADM momentum when V≠0. Its shift source cannot be dropped. Proper constant density rho=6e6 has p=(6000004)/sqrtF−6000000 and obeys p′=−(rho+p)F′/(2F). Exterior rho=p=0; the duplicated surface sample is correctly evaluated separately with each side's derivatives/source.

For t=lnr and state (lnN,lnB,w,k), the independent derivative dictionary is
 N′=Nk/r, B′=B(dlnB/dt)/r,
 V=−wrN, V′=V[1+k+(dw/dt)/w]/r,
 N″=N[dk/dt+k²−k]/r².

This uses the RHS at each stored state, **not a differentiated saved dense interpolant**. Agreement therefore tests the RHS's consistency with the original action/source equations and its arithmetic at those states. It does not test the interpolation defect or accumulation of integration error.

## Residual size and arithmetic distinction

Each residual is divided by the sum of absolute magnitudes of its original Euler terms; no added unit denominator masks the very small center terms. Across all204 samples, maximum backward relative residuals are:

| Derivatives assigned by | EN | EB | EV |
|---|---:|---:|---:|
| mp50 reconstructed RHS | 1.1125e−34 | 2.9637e−34 | 9.5766e−51 |
| original binary64 RHS | 2.0617e−16 | 1.1403e−16 | 1.2311e−16 |

The tiny mp50 nonzero EN/EB values include the RHS's declared low-a truncated leg series, while the independent Euler response uses the exact closed form. These are backward **equation** residuals, not observational errors or50-digit accuracy of the stored trajectory. The binary64 row separately tests ordinary RHS arithmetic and avoids confusing the mp reconstruction with actual numerical solver precision.

The negative control deletes only the matter shift term from the independent EV residual while retaining the same states and RHS derivatives. Its maximum normalized residual becomes .610283343242, and both tolerance cases fail the EV checks. The other Euler equations remain unaffected. This detects the physically load-bearing proper-fluid momentum source.

## Exact physical force versus the stored exterior diagnostic

The exact stationary-observer force is gphys=F′/(2NB sqrtF). Writing q²=B²r²w² gives the equivalent full dictionary

 gphys=[k(1−q²)−q²(dlnB/dt+1+(dw/dt)/w)]/[rB sqrt(1−q²)].

This identity agrees to the mp precision at every sampled state. The stored interior `physical_force` agrees with this exact expression within4.03e−16 relative rounding. Stored proper pressure differs by at most3.81e−16 absolute.

The exterior field named `physical_leading_g` instead equals a−VV′+H*²r. Its last term subtracts the deSitter background attraction: it is a **cosmologically background-subtracted leading force**, not the unsubtracted exact Killing force. Reconstructing that formula agrees with its stored values within5.65e−16 relative rounding. Comparing it directly to gphys gives a maximum relative difference .00133462005, mostly the deliberately added H*²r. Removing that subtraction before comparing, a−VV′ differs from exact gphys by at most4.84e−9 relative on these samples. These are separate comparisons; the .0013346 is not a numerical RHS failure. Exterior weak_massflux/MOND_ratio retain their reduced/background-subtracted dictionary and are not exact physical mass or observed-force theorems.

## Center-root conditioning: a narrower precision limit

The high-density root sits very close to the trace pole. At50 digits with exact physical parameters,

 x=−.16835016905728099601793949064069696558067695968925,
 xp=−.16835016835016835016835016835016835016835016835017,
 xp−x=7.0711264584958932229e−10,
 n2=50000030.62584319751277948662338691937130937202561.

The serialized decimal x=−.16835016905728112 differs from this root by−1.23982e−16, approximately1.75e−7 of the pole offset. n2, obtained from the density equation, differs only about1.50e−16 relatively. This contrast explains why an accurate n2 does not imply equally accurate relative trace cancellation.

The parent's reported `trace_relative_residual` divides the absolute residual by1+|n2|≈5e7. Its native binary64 value2.93627e−16 corresponds to an absolute trace residual≈1.47e−8. Evaluating the exact stored binary64 x,n2 at50 digits with exact physical coefficients gives absolute residual1.81508e−8 and relative-to-the-two-trace-terms residual8.64e−8. Decimal-versus-exact-binary and ordinary cancellation rounding account for the small difference. The recorded metric is therefore not relative cancellation accuracy. This precision issue does not refute the analytic high-density center branch or the demonstrated RHS/source consistency. It also does not bound the finite-start series remainder. A high-precision initialized trajectory or a controlled start-radius comparison would require separate evidence.

## Evidence scope

`checks.py` and `contract.json` retain exact declared inputs, arithmetic flavors, samples and non-claims; `provenance.json` records hashes and interpreter/library versions. The bounded standard main run and missing-shift control are fresh. Neither the small Euler residuals nor the two tolerance values certify between-node ODE error, finite-start source initialization, a smooth density surface, global normalized cosmic matching, baryonic-force calibration, finite-gradient health or a32pi selector. Global matching is being investigated separately and its files were not touched.
