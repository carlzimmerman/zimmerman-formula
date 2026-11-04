# AZ26: branch crossing permits every width; the cosmic side is unstable

κ = ½ FITTED; not theory closed

**PASS** for algebraic branch crossing; **FAIL** for inhomogeneous continuum stability of the AZ25 cosmic branch, for every positive width; **FAIL** for selection of a unique width by these health gates; **NOT EVALUABLE** for physical κ or an unspecified finite-cutoff completion. Both canonical and alt receive these separate grades. Zero whole requirement and RQ3 rows earned. Criteria commit 2ccd1692eb.

The necessary stability test fails before a full galaxy simulation can be justified. We derived the constrained short-wavelength mode of the original action, rather than inferring stability from homogeneous attraction. No full nonlinear galaxy evolution was simulated. The result applies to galaxies embedded in AZ25's positive-density expanding branch, not all conceivable isolated vacuum solutions or all alternative actions.

## 1. Exact nonlinear crossing does not select a width

Use AZ24's integrated momentum constraint and AZ25's signed cusp. With J=K0−C1 E/C2 and A>0,

    K=J(1+q),
    P(q)=C1 A² q|q|+C2 J²(1+q)²−C2 K0²−C1 g²=0,
    q>−1, K0>0.

This retains the nonlinear momentum functional E, including its connection integral; it is not the static approximation F'K=constant. The one-sided derivatives are

    P'(q)=−2C1 A² q+2C2 J²(1+q)>0,  −1<q<0,
    P'(q)=+2C1 A² q+2C2 J²(1+q)>0,   q>0.

P(−1)=−C1 A²−C2 K0²−C1 g²<0 and P tends to infinity at large q. Therefore the continuous function has a unique root throughout the declared domain. At a crossing q=0,

    J²=K0²+(C1/C2)g²,
    P'(0)=2(C2 K0²+C1 g²)>0.

P and P' are continuous across zero, so the implicit constraint root is locally continuously differentiable there. Its second derivatives need not be continuous. Crucially, the crossing condition contains no A. This proves regularity of the **algebraic constraint inversion**, not existence or uniqueness of the complete time-dependent PDE or differentiability of the original F'' at the cusp. The momentum boundary assumptions remain those of AZ24.

## 2. Derive the physical scalar principal action

At a homogeneous time-dependent background with q strictly between −1 and 0, all F derivatives are finite. Work locally on scales short compared with the background variation. Define

    alpha=C1 F',
    Q=F'+2I F'',
    lambda=1+C2 Q.

These follow by expanding the original trace kinetic function G(K)=−2K²/3+m²F(−C2 K²/m²): G_KK=−4/3−2C2 Q. The scalar shear supplies the remaining kinetic terms. Expansion of spatial Ricci curvature and the lapse acceleration gives the gradient terms. Before constraint elimination, the principal scalar bracket is

    −3(3lambda−1) ζdot² + 2(3lambda−1) ζdot beta
      +(1−lambda) beta²
      +k_phys²(2ζ²+4nζ+alpha n²).

Here beta is the shift divergence, **not** the normalization b. Background Hn terms and time derivatives of coefficients have lower differential order; they are not discarded from an exact finite-wavelength evolution equation, which is not being claimed. This is a local principal-symbol calculation on an evolving background, not the exact de Sitter finite-k formula copied onto it. Minimal dust has zero pressure sound speed and no competing gravitational highest-derivative term; its density and background-curvature corrections do not change this high-frequency scalar sign.

The lapse and shift equations give

    beta=(3lambda−1)ζdot/(lambda−1),  n=−2ζ/alpha.

The reduced principal bracket is

    C ζdot² − G k_phys² ζ²,
    C=2(3lambda−1)/(lambda−1),
    G=2(2−alpha)/alpha,
    c_s²=G/C=(lambda−1)(2−alpha)/[alpha(3lambda−1)].

This is a retained physical scalar with its constraints eliminated. A positive tensor kinetic term or homogeneous convergence does not remove it.

## 3. The cosmic side fails for every positive width

On the AZ25 negative-q branch,

    alpha=2/(1+q)>2,
    Q=2(I0+xa q)/[C1 xa q(1+q)²]>0,
    lambda=1+C2 Q>1,
    c_s²=q(lambda−1)/(3lambda−1)<0.

The sign is rigorous for every −1<q<0 and every C1,C2,H0,A,m>0: I0<0 and q<0 make numerator and denominator of Q both negative. No chosen width can change these inequalities. The script independently substitutes q=−u/(1+u), u>0, covering the entire interval and turning Q and −c_s² into ratios of positive polynomials.

The kinetic coefficient C is positive; this is a **gradient instability**, not a negative-kinetic-energy ghost. For locally frozen coefficients the scalar equation has exponentially growing solutions with rate |c_s| k_phys. Its characteristic frequency is imaginary. Arbitrarily short wavelengths grow arbitrarily quickly in the declared continuum action, so a regulator-free, stable inhomogeneous initial-value evolution cannot be inferred from the homogeneous attractor. A grid would supply an undeclared cutoff, with its fastest-growing modes moving as resolution changes.

This is a necessary failure on the prescribed cosmic background. It does not prove that every isolated solution with q>=0 is unstable, nor does it classify anisotropic source-side principal symbols. Such a restriction would, however, omit AZ25's positive-density cosmic history and would not select A.

## 4. Expansion does not repair the continuum problem

Near the late-time endpoint, c_s²=q/3+o(q) and AZ25 gives q approximately −q_a exp(−3H0 t). A fixed comoving wavenumber has k_phys=k_com exp(−H0 t). Its leading local growth rate is consequently

    Gamma(t) approximately k_com sqrt(q_a/3) exp(−5H0 t/2).

The late-time WKB exponent over an interval of length T is

    2 k_com sqrt(q_a/3)/(5H0) [1−exp(−5H0 T/2)].

It is finite at infinite time for each fixed mode. We do **not** claim endless late-time growth of every mode. But it remains proportional to k_com: the continuum amplification is unbounded as wavenumber increases. More directly, any finite-time interval on which q<0 has the wrong-sign local principal symbol. Redshift cannot turn that into a stable continuum initial-value problem.

The formula above is an asymptotic high-frequency estimate, not a simulated exact mode trajectory. A finite EFT cutoff, higher-spatial-derivative stabilizer or strong-coupling resolution might change the question. None has been specified or derived. Their physical timescales and predictions are therefore NOT EVALUABLE here. It would be incorrect to assume an unspecified cutoff removes the instability, or to claim this argument excludes every possible completion.

## 5. Consequence for b and κ

The conditional dictionary still reads b=(H0/(2A))sqrt(3/(8pi)), κ=1/(2b). The constraints allow every positive A to cross; the cosmic stability condition rejects every A in this completion. There is no surviving isolated value, including the value that would give b=1. The calculation therefore gives a failure of this proposed selection mechanism, not a derivation of a number and not a universal impossibility theorem.

The signed continuation was an explicitly unselected choice in AZ25. Changing it or adding gradient operators is a new action and must get its own criteria; silently modifying it until the numerical evolution behaves would not establish physical selection. The next research dependency is a physically justified stable opposite-side action with a well-posed source evolution. The full galaxy initial/boundary-value problem and observed force calibration remain unsolved. Repeating an unregulated simulation of the rejected branch is not a route to a reliable κ.

## Evidence

`results.json`: **25/25 checks**, including branch continuity, exact Jacobian, independent lapse/shift elimination, positive and negative sound-speed controls, all-interval sign reparameterization, near-cusp limit and WKB-integral identities. The gradient-sign mutation disagrees with the reduced action; Lean verifies finite rational controls and rejects the false nonnegative-speed control. Lean does not certify the full nonlinear PDE, interval proof or physical κ. Exact zero residuals are the algebraic margins; the unstable finite witness is c_s²=−1/10. No observational significance or error bars are assigned to that control.

Reproduce: `python3 astra_goal_2026_11_03/P3/AZ26_branch_crossing_stability/run.py`. Input hashes and versions are recorded. The interval arguments and scope restrictions are self-reviewed, not independently audited. All A,B,m,C1,C2,H0, initial/boundary data and any proposed cutoff remain unselected/FITTED. No external data, new species, cold component, width scan, heavy run or push.
