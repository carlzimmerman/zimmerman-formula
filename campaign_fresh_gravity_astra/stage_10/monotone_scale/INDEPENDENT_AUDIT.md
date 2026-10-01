# Independent audit: monotone scale weighted-square criterion

**Primary verdict: proved as written**, under the candidate's stated regularity, positive coefficients, strictly increasing scale, and fixed-wall hypotheses. This is an exact conditional theorem for the unfiltered Q/R SD1 diagnostic action, not physical or observational acceptance of the framework. No new numerical calculation was performed.

Auditor `/root/metric_intake`, 2026-09-30. Inputs are the root-origin `ROOT_CANDIDATE.md`, the completed FGF023 equilibrium/Hessian derivation and the earlier Dirichlet reduction; exact hashes are recorded in `audit_result.json`. The FGF025 author's new result was not read or used. This audit independently reconstructed the equilibrium derivative and all integrations rather than taking author agreement as evidence.

## Normalized claim and dependency graph

Let I=[l,r] be a compact interval, D=r−l>0. Assume a smooth static Q/R hydrostatic solution satisfying B'=C rho, cs²rho'=−rho g, g=F(B,a_ref exp chi)>0, and Jchi''=U'−T. The constants C,J,cs² and kinetic coefficients are positive. Assume rho, lambda=b_g and q=g lambda−B are positive and w=chi'>0 throughout the **closed** interval. Thus w,rho,lambda,q have positive minima and finite maxima; required coefficient derivatives are bounded. Define R=rho q/lambda and M=U''−T_chi−q²/lambda, with T_chi taken at fixed g.

For real H¹₀ triples (xi,psi,eta), the claim is exact factorization of the FGF023 quadratic potential into four nonnegative squares plus an endpoint derivative, and coercive positivity on each such fixed interval. It removes the previous explicit short-interval determinant criterion; it does not prove any chosen data admit a long increasing solution or a lower spectral gap uniform in interval length.

Dependencies: assumed constitutive action -> exact hydrostatic and scale equilibrium -> derivative identity for w -> FGF023 constrained Hessian -> weighted-square identity -> boundary cancellation -> positive/coercive energy. The local IVP gives nonemptiness only. None of these implications requires a numerical spectrum, an imported gravitational mechanism or measured observations.

## Independent algebra and signs

Differentiate the scale equilibrium with respect to x:

Jw''=(U''−T_chi)w−T_g g'=(U''−T_chi)w−qg'.

The constitutive flux derivative is lambda g'−q w=C rho. Substituting g'=(C rho+q w)/lambda yields

Jw''=(U''−T_chi−q²/lambda)w−C rho q/lambda=Mw−CR.

The sign before CR is negative. All chi derivatives of T here hold g fixed; replacing a total derivative by T_chi alone would omit qg'. Constant J is essential to the displayed form.

Set v=eta/w, well defined on the closed interval. A pointwise expansion gives

Jw²v'^2 = Jeta'^2−2J(w'/w)eta eta'+J(w'/w)²eta²,

[J(w'/w)eta²]' = 2J(w'/w)eta eta'+J[w''/w−(w'/w)²]eta².

Their sum is Jeta'^2+J(w''/w)eta². Adding (CR/w)(eta+wxi)² gives

Jeta'^2+[Jw''/w+CR/w]eta²+2CRxi eta+CRwxi²
=Jeta'^2+Meta²+CR(wxi²+2xi eta).

This verifies every coefficient and shows that the total derivative has the **positive** sign displayed in the root candidate. Dividing by C and inserting the FGF023 factorization gives exactly its equation (3), with endpoint term

[cs²rho'xi²−2rho xi psi+(J/C)(w'/w)eta²]_l^r.

No other scale integration-by-parts term is missing. The original FGF023 square has not been statically cancelled or eliminated. Dirichlet xi=psi=eta=0 makes the endpoint term vanish; no extra derivative or field-flux condition is imposed.

## Strict positivity and coercivity

Every integral term in equation (3) is nonnegative because cs²rho, lambda/C, Jw²/C and R/w are positive. Zero energy first forces xi'=0 and then xi=0 by its traces. The last square then forces eta=0, and the psi square implies psi'=0, hence psi=0. This proves strict positivity; no hypothesis M>0 is used.

The candidate's stronger coercivity statement also holds. Here is an explicit route that does not infer coercivity from strict positivity alone. Let E denote the sum of the four integrals. Since eta=0 at both ends and w>0, v=eta/w belongs to H¹₀. Write w_min>0, w_max<infinity and W1=||w'||_infinity. Then

||xi'||² <= E/(cs²rho_min),
||v'||² <= CE/(J w_min²),
||v|| <= (D/pi)||v'||,
||eta|| <= w_max(D/pi)||v'||,
||eta'|| <= [w_max+W1 D/pi]||v'||.

For s=psi'+(C rho xi−q eta)/lambda, the second square gives ||s||²<=CE/lambda_min. Consequently

||psi'|| <= ||s||+||C rho/lambda||_infinity||xi||
                    +||q/lambda||_infinity||eta||,

and Poincare supplies ||xi|| and ||psi||. Combining these inequalities yields a finite positive c_I with E>=c_I(||xi||²_H¹+||psi||²_H¹+||eta||²_H¹) on this fixed patch. Constants can deteriorate with D, w_min, coefficient extrema and w derivatives. This is **not** a spectral gap or coercivity constant uniform in length, nor a uniform statement as w_min tends to zero.

With the specified positive kinetic form and fixed endpoints, the conservative linearized system has positive perturbation energy and the corresponding positive self-adjoint longitudinal quadratic-form problem. The factorization gives no claim of nonlinear, 3D, relativistic or free-boundary stability.

## Boundary domain, zeros and existence

Strict positivity of w at all closed-interval points is a material hypothesis. An interior or endpoint zero may make eta/w or w'/w singular. The stated proof cannot be used there without another domain analysis, even if the unfactored Hessian remains regular. With w<0 the CR/w term has the opposite sign; this proof provides no sign conclusion. Neither loss of this hypothesis alone proves instability.

The completed FGF023 IVP supplies a nonempty family: take initial B,rho>0, chi finite, w_i>0. Smooth local existence away from B=0, followed by restriction to a compact sufficiently short interval, preserves these strict signs. Endpoint values and total mass are those induced by the solution, not arbitrary separately imposed values. Every longer continuation segment must independently retain regularity, rho>0 and w>0. The root text correctly makes no arbitrarily-long existence claim and no claim of an already demonstrated longer example where the old determinant bound fails.

The background is supported by boundary field values and wall pressures but contains no distributed force canceler or matter-source subtraction. That distinction remains intact. Setting eta=0 leaves the w-dependent matter contribution; it does not freeze the background scale.

## Optional static eta operator: consistency check only

For xi=0, static minimization over Dirichlet psi leaves

C(2V_reduced)=integral[Jeta'^2+Meta²]dx
 +(integral(q/lambda)eta dx)²/Z,  Z=integral 1/lambda dx.

Thus the reduced operator is L=−J d²/dx²+M+(q/lambda) tensor (q/lambda)/Z, with the outer product interpreted in the ordinary real L² inner product and Dirichlet domain. This is the stated rank-one term with its positive sign and normalization. It has not been discarded. In the current w>0 regime the local part alone already has

integral[Jeta'^2+Meta²]
=integral[Jw²((eta/w)')²+(CR/w)eta²]>0

for nonzero admissible eta. The nonlocal term only adds nonnegative energy. This static check is consistent with the full proof but is not a dynamical elimination of psi when its inertia is nonzero, and is not needed for equation (3).

## Symbolic controls and verdict limits

The proposed controls are valid as symbolic checks: adding delta to M without changing the equilibrium leaves delta eta² unmatched; dropping a nonzero endpoint eta boundary contribution fails the integrated identity; dividing by w through a zero leaves the stated domain; eta=0 leaves background w terms. These were checked algebraically, not reported as executed numerical tests.

| Obligation | Status |
|---|---|
| Differentiated equilibrium and −CR sign | Passed |
| Weighted-square expansion and endpoint sign | Passed |
| Dirichlet cancellation without zero-flux conditions | Passed |
| Strict positivity and fixed-patch coercivity | Passed |
| Treatment of w zeros and negative w | Correctly excluded, no instability inferred |
| Nonempty local IVP family | Passed conditionally on specified smooth model |
| Arbitrarily-long backgrounds or uniform gap | Not claimed or proved |
| Static Dirichlet rank-one term | Passed and retained |
| Numerical, observational or filtered-MONO acceptance | Not performed or implied |

Both registered positive a_ref normalizations remain independent inputs. A frozen H(z) reference labels a separate stationary comparison and does not solve time-dependent cosmology. Since actual a=a_ref exp chi varies, the literal pointwise constant-vacuum identification is still not repaired. No registered M action, physical metric or photon coupling follows. No source-discrepancy calculation is performed; the source identity continues to use MOND flux B'=C rho.

The earned result is a stronger exact sufficient positivity theorem on every existing regular increasing-scale wall patch. The remaining physical and mathematical questions include independently admissible global boundaries, continuation to relevant sizes, turning-scale profiles, and transfer to the operative metric theory. No counterexample to the precisely scoped root candidate was found.

## Final supplemental turning-point control: passed

The separately pinned `TURNING_POINT_CONTROL.md` is correct under the same Q/R and cosh-potential assumptions. At x=0 choose B0,rho0>0, chi0=w0=0. Then g0>0 and T(g0,a_ref)>0, while U'(0)=0, so w'(0)=−T/J<0. The smooth ODE admits a two-sided local solution remaining in B,rho>0. Since w(x)=w'(0)x+o(x), w is positive to the immediate left, negative to the immediate right, and has a transverse zero at the interior point. The original Hessian coefficients remain smooth because they involve w, not 1/w.

For I=[−epsilon,epsilon], the earlier FGF023 general determinant condition has D=2epsilon. Its rho_min approaches rho0>0; the lower-order bounds involving M and rho q w/lambda, and the mixing supremum, remain finite. Both positive diagonal estimates diverge as D^-2 and their product as D^-4. Therefore the sufficient general positivity condition holds for all sufficiently small epsilon, with the solution-induced field endpoint values, impermeable walls and corresponding fixed mass. This supplies an actual local boundary-maintained positive-energy patch containing a sign change in w, independently of the singular weighted representation.

The control refutes the implication that failure of the w>0 criterion alone certifies instability. It does not extend the weighted identity through the zero, follow the same arbitrarily chosen long-slab boundary data, or establish stability after a turning point for a previously fixed long solution. This is a separate analytic local family; no numerical crossing or spectrum was executed.
