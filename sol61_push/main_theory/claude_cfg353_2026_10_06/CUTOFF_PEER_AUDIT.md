# Independent audit: Claude cutoff kernel as a clock response

Read-only pinned inputs: claude_cutoff_clock_2026_10_06/REPORT.md SHA256 431b048a18a77ccf8a6832facecaf8b5ef76a1afe31a8ec9a1d1416b6b54f95e; checks.py eb0ae11901b9fb8064e78a2d37589065971a45ec7f37281d9fd5fbb9b867778c; main_a results 9b572a23faa3ddf883618bf6fb8c80bb54ece7acf875b5adf4d34d893846a75e. I reconstructed the mathematical dictionary and stationary coefficient from the already audited full ADM action. No peer/Claude source was executed or modified.

**Primary verdict:** the sign-crossing theorem, kernel-specific root/invertibility bound, stationary rank loss, necessary critical compatibility and conditional high-force flow exponents are correct. Their restricted interpretation is essential. Rank loss is not a demonstrated physical ghost or a global no-go, and the formal forced flow is not the only possible exact sourced branch. One cosmological-quadratic wording qualification is recorded below.

## Independent reconstruction of the constitutive signs

For y=s/A and h(y)=b(y)/D(y), b=1/[√(1+1/y)+1], D=1+(y/T)^k, the prescribed g=A[y+h(y)] has dg/ds=1+h′. A regular monotone inverse therefore gives W_gg=ds/dg=1/(1+h′), not its reciprocal reversed. With response L=K_E U, U=g²−2W,

U_gg=2h′/(1+h′), U_g/g=2h/(y+h)>0.

Dimensions agree: U and W have acceleration squared, U_gg is dimensionless, and K_E supplies the four-dimensional action density. The physical gradient Hessian is K_E U_gg longitudinally and K_E U_g/g transversely; the quadratic Taylor term carries the usual one-half. The positivity of the latter does not fix the former.

If the positive acceleration excess is C¹, tends to zero at both endpoints and is positive somewhere, the mean-value theorem gives a positive derivative before some positive value and a negative derivative later. Continuity forces a zero. If dg/ds>0 throughout, U_gg crosses through zero and is negative on at least part of the return. If that inverse ceases to be regular, the source-to-response construction fails earlier. The uncut P2 excess tends to A/2 and does not satisfy the decaying-tail premise. This proves a property of the response operator, not that every physical source trajectory reaches its negative side.

Independently simplifying b as √[y(y+1)]−y gives yb′/b=1/{2[y+1+√(y(y+1))]}. It decreases from one-half to zero, while yD′/D increases from zero to k, so their equality has exactly one root. For k=2 the equation is T²=y_c²[4y_c+3+4√(y_c(y_c+1))], with large-T y_c≈T^(2/3)/2. The global bound follows from b≤1/2 and b′>0: h′≥−(1/T)max_x x/(1+x²)²=−9/(16√3 T). Hence the stated inherited T values retain dg/ds>0 even after U_gg becomes negative. The tabulated critical g/A near13 for T≈128.915 is consistent with these equations.

## Stationary derivative rank and critical condition

Use φ=qt, fixed A, nonzero finite V,N,r and N′>0. In the previously independently derived exact Euler equations, taking derivative unknowns (B′,V′,a′) with N′=aNB gives the momentum coefficient −2K_ErV/N in the B′ column, the radial coefficient +2K_ErV/N in the V′ column, and the lapse coefficient −K_Er²U_gg in the a′ column. Remaining off-diagonal entries do not change the triangular determinant. Their product is 4K_E³r^4V²U_gg/N², agreeing with the report. The script's displayed matrix is a compressed representation of these actual Euler coefficients, not an independent proof by itself; this action-based reconstruction supplies that link.

At U_gg=0 the inverse chart still has dg/ds=1, so a↔s is a nonsingular transformation and cannot restore the reduced system rank. This does not prove that the full covariant/time-evolution symbol is singular: the result concerns this stationary reduction with fixed A and the stated ansatz. A=βθ, other constraints/operators or a different background require a new coefficient matrix.

Direct variation of the normalized clock gives the current already verified in the ADM audit. Since (r²U_g)′=2rU_g+r²U_gg a′, the exact zero-current condition loses a′ at the critical surface and becomes j_KGB^r+2K_E VU_g/(qBr)=0. This is the stated necessary algebraic compatibility. It need not be contradictory. The exact metric-current identity makes zero current a consequence of all stationary exterior metric equations; it is not an independently selectable exterior charge.

## Formal source branch and normalization limits

Assuming the leading source-to-clock balance W_g(a)=s=m/r², a=g(s) gives ra′=−2s g′(s). The retained zero-current relation therefore requires

V≈−ηHr g/[2(g−sg′)]
=−ηHr[y+h]/[2(h−yh′)].

The denominator is positive because b−yb′>0 and D′>0. At h′=0 it is 2h, so the leading flow is finite and satisfies the leading critical condition. It does not prove that the exact higher-order lapse/radial equations or boundary data admit a smooth crossing.

For high y, h≈T^k/(2y^k) yields V≈−ηHr y^(k+1)/[(k+1)T^k]. With y=m/(Ar²), the mass exponent is k+1 and radial exponent −(2k+1); k=2 indeed gives m³r^−5. This is conditional on that source-to-clock branch, not a universal force law of the action. Flow-dominated or nearly geodesic clock branches need not obey W_g(a)=m/r², and their physical force is determined by F=N²−B²V².

The Solar numbers are dimensionally consistent: m_geom=GM/c_light² and A_geom=A_SI/c_light², so y=GM/(r²A_SI), while H_geom=A_geom/(A/H). For inherited T≈128.915,η=.5 the displayed formal dimensionless shifts at1AU range from roughly−1324 to−132 as A/H varies .3→3. This invalidates the assumed weak-flow branch and, with N≈B≈1, the assumed static patch. It is not a physical-superluminality theorem: V is an ADM coordinate shift. The insertion m_source=GM_sun/c_light² is itself a conditional source calibration; a completed interior has not established it. The report correctly avoids interpreting this benchmark or p56's imposed-force orbit summaries as an observational exclusion of the full completion.

## Required qualification about the cosmological quadratic sector

The final section says that the original “cosmological quadratic branch survives.” Its safe interpretation is survival of the geodesic rolling background, vacuum map and a positive *modified* quadratic scalar branch. It must not mean an unchanged original quadratic action. Because W=O(g³/A), Lresp=K_E g²+… contributes +K_E|∇ν|² on the geodesic background. Full constraint elimination, independently established in log_braiding_extension, adds K_E p²/[H²(1+z)²] to G_S while F_S remains unchanged. The first variation vanishes but the second variation does not. The author acknowledged this wording and is carrying the explicit qualification in a separate addendum so the original execution inputs stay frozen.

With that qualification the principal claims are accepted at their stated scope. The next actual physical obligation remains the full finite-acceleration constrained symbol and a matched source/critical crossing, including alternative clock-flow branches. Neither the constitutive sign theorem, finite determinant check nor formal Solar breakdown closes those obligations or selects32π.
