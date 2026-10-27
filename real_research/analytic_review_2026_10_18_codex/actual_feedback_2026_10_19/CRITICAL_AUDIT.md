# Independent audit: actual zero-scalar critical receiving work

19 October 2026. Reviewer: `/root/audit_critical_work`, a fresh delegated analytic audit. Only this new scratch file is written. No scientific script, numerical integration, array calculation, or process inspection/control was used.

**Normalized claim.** At one isolated positive interior Morse minimum of an actual species frequency, assume the complete regular boundary inverses exist and are Hölder in frequency, the forcing has the actual aligned leading critical vector, the optical coarea limits exist, and the receiving family has the stated compact eccentric regular/Morse geometry. If the dressed critical scalar vanishes, the local frequency contribution to receiving work is uniformly bounded in time and over that receiving family. An actual causal boundary formula, or an independently justified jump formula, is required to identify the frequency integral with work.

**Primary verdict: conditional on a named input.** The analytic conditional theorem in Section 6 passes this audit. Its named inputs are the complete regular boundary inverses and regularity, the optical boundary/coarea limits, the stated receiving geometry, and the actual local work representation. I find no counterexample to the uniform-in-receiver conclusion under these hypotheses. This is stronger than a statement only at the exact critical receiver. It does not establish the complete regular inverse for the actual halo, nor any global work or confinement conclusion.

The precise transform qualification matters: a norm expansion of a field resolvent does not, by itself, produce a spectral jump representation. The memo recognizes this in its proof. Its alternative using the actual upper causal transform is the appropriate route when working with the damped Parseval identity in `full_feedback/RESULT.md`, Theorem C, Step 3. Passing that identity to the boundary requires the stated boundary to be the actual transform boundary, with local integrability/convergence. The displayed logarithmic expansion supplies the required local integrability once that boundary passage is justified. There is no reason to impose equality of upper and lower leading field vectors.

## 1. Exact artifacts and conventions audited

Main artifact: `/private/tmp/halo_actual_dressed_20261019.md`, SHA-256 `dfe7f9b8577f428ba44ba9ffb68e11f76e35ac05050b10f2057757fe70697436` at reading. Priority was Sections 1, 3, and 6; Section 4 block algebra was also checked. Section 5's interpretation is addressed only to the extent indicated below.

Coordinator's corrected repository copy: `/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/analytic_review_2026_10_18_codex/actual_feedback_2026_10_19/CRITICAL_RECEIVER_CANCELLATION.md`, SHA-256 `aa89494c7e6e50c8eb04f11d62925fdc4e9f5eb836000b47989a5b4ab18779fe`. A direct `diff -u` confirms exactly two localized prose replacements, both correcting the necessary/sufficient wording identified below; no proof equation or hypothesis changed. The analytic audit therefore applies unchanged to this corrected copy.

Actual model source: `/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/analytic_review_2026_10_18_codex/claude_continuation_2026_10_19/full_feedback/RESULT.md`, SHA-256 `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`. The relevant raw definitions are Sections 1.1–1.8, the shell identities in B2, the optical discussion in B3, and the damped Parseval identity in Theorem C. The screening source `/Users/carlzimmerman/new_physics/zimmerman-formula/reviews/latest_results_push_2026_10_19_codex/KINETIC_SCREENING.md` was read for the exact local leading-coefficient and representation claims.

Species order is `(t,f)`; `L` in `q=(J,L)` means squared specific angular momentum. The action measure is `dm=2*pi*C_Gamma*dJ*dL`, with `C_Gamma=4*pi^2`. The feedback sign is

    T(z) phi = pushforward of
      -w_i(q) sum_(k != 0) nu_ik/(nu_ik-z) phi_i,k(q) exp(i*k*theta),
    K(z)=P T(z),   nu_ik=k*Omega_i,   w_i=-F_i,E.

Here `w_i>0` on the open occupied set and vanishes at its boundary. Fourier extraction uses `exp(-i*k*theta)`. The source orbit angle starts at a turning point, so the orbital radial function is even. Its critical harmonic measure `e_c` is a real zero-mass measure; consequently `ell(phi)=integral phi de_c` is a real linear functional on real fields and `v=P e_c` is the actual real source-angle vector.

No applicable `AGENTS.md` was located by the text-file search used for this audit. No ledger modification is authorized or performed. No external theorem or numerical evidence is load-bearing in this audit; the Morse normalization, rank-one algebra, and oscillatory estimates below are checked analytically.

## 2. Dependency graph

The exact dependency chain is:

1. Actual reciprocal shell kernel and feedback sign, plus the action measure.
2. Eccentric interior Morse minimum and smooth orbit map, giving the actual rank-one coefficient `v_0=-beta*P e_c` with `beta>0`.
3. Complete regular inverse and its norm boundary limit, plus coarea trace hypotheses, giving the optical identity.
4. Zero dressed scalar, positivity of the open-channel weights, and continuity of receiving extraction, giving vanishing receiving traces on the critical level `Z`.
5. Hölder receiving extraction and the geometric distance bound, giving an algebraic detuning factor in the logarithmic and step coefficients.
6. Exact rank-one inversion and Hölder frequency coefficients, giving a constant + logarithm + step + Hölder remainder expansion.
7. Shifted oscillatory integral bounds, giving logarithmic losses in detuning. The algebraic factor from item 5 absorbs these losses.
8. An actual local causal or jump work representation, identifying that bounded integral with the corresponding local contribution to receiving work.

Items 1, 2, 5, 6, and 7 are direct internal deductions under the specified geometric hypotheses. Items 3 and 8 are analytic operator/representation inputs. Nothing in this chain proves their actual global validity. There is no circular appeal to the desired work bound.

## 3. Morse coefficient and reciprocal optical sign

At the minimum of `nu=n*Omega_j`, the pushforward density of `dJ*dL` tends to

    2*pi / sqrt(det D^2 nu(q_c))
      = 2*pi / (n*sqrt(det D^2 Omega_j(q_c))).

Multiplying by `dm` and by the feedback numerator `-w_j*nu_c` gives exactly

    beta = 4*pi^2*C_Gamma*nu_c*w_j(q_c)
             /(n*sqrt(det D^2 Omega_j(q_c))),
    K(z) = Lambda(z)*v_0 tensor ell + R(z),
    v_0=-beta*v,   v=P e_c,
    Lambda=log(nu_c+eta-z)-log(nu_c-z).

The bare identities `ell(v)<0` for the free species and `ell(v)>0` for the tethered species agree with the actual shell kernels. They do not imply nonzero dressed scalar after regular inversion. The field form is indefinite: for `H=[[h,-g],[-g,-g]]`, `det H=-g(h+g)<0`, and its inverse gives the memo's difference of two positive derivative squares. A positive-inner-product replacement would be invalid.

For completeness, the finite-epsilon optical identity can be reconstructed without a field inverse. Put

    T_reg=T+beta*Lambda*e_c tensor ell,
    V_epsilon=(I-R(nu_c+i*epsilon))^-1 v,
    S_epsilon=e_c+T_reg(nu_c+i*epsilon)V_epsilon.

Then `V_epsilon=P S_epsilon`. The sources can be complex finite measures; reciprocity makes `integral conjugate(S_epsilon).P S_epsilon` real. Expanding the anti-linear first pairing gives

    Im ell(V_epsilon)
      = -sum_(i,k) integral
          w_i*nu_ik*epsilon*|V_epsilon,i,k|^2
            /((nu_ik-nu_c)^2+epsilon^2) dm
        + beta*Im Lambda*|ell(V_epsilon)|^2.

Both signs are correct. Indeed conjugating `-w*nu/(nu-z)` gives imaginary part `+w*nu*epsilon/((nu-nu_c)^2+epsilon^2)` in the paired source term; conjugating the subtraction gives `-beta*Im Lambda*|ell V_epsilon|^2`.

On the isolated critical chart its coarea density is

    beta*|ell(V_epsilon)|^2 + O(s^a),   s=nu-nu_c>0,

for some positive `a`, uniformly for a bounded family in `Y_gamma`. Smooth eccentric orbit dependence gives this from the `Y_gamma` norm: `V_epsilon,n(q)-ell(V_epsilon)=O(|q-q_c|^gamma)`. The constant density is canceled exactly by the last term since

    Im Lambda(nu_c+i*epsilon)
      = integral_0^eta epsilon/(s^2+epsilon^2) ds.

The error tends to zero. The remaining regular resonant curves give their positive-frequency Poisson traces. Negative harmonics are nonresonant at `nu_c>0`; large harmonic tails have the summable bound `epsilon*sum |k|^(-1-2*gamma)` using the actual receiving Fourier estimate. Thus, under the explicit boundary/coarea hypotheses,

    Im ell((I-R_+)^-1 v)
      = -pi*nu_c sum_regular integral_(nu_ik=nu_c)
           |V_i,k|^2*w_i*(2*pi*C_Gamma) d sigma/|grad nu_ik| <= 0.

For the scalar with `v_0=-beta*v`, the imaginary sign reverses. Its being zero is equivalent to the scalar with `v` being zero. No positive field form was used.

## 4. Zero-scalar response and its actual jump coefficients

Use the memo's frequency-dependent quantities

    p=A(x)^-1 r(x), V=A(x)^-1 v_0,
    a=ell(V), c=ell(p), A=I-R,

separately on the upper and lower boundaries. Solving the rank-one equation gives exactly

    U = p + V*Lambda*(b+c)/(1-a*Lambda),
    ell(U)=(c+b*a*Lambda)/(1-a*Lambda).

If `a(0)=0` and all these regular quantities are `C^alpha`, then `a(x)=O(|x|^alpha)` and `1-a(x)*Lambda(x)` stays bounded away from zero on a sufficiently small fixed neighborhood. Writing `D=V(0)*(b+c(0))`, the remainder after subtracting `p(0)+D*Lambda` is a sum of

    p-p(0),
    Lambda*[V*(b+c)-D]/(1-a*Lambda),
    D*a*Lambda^2/(1-a*Lambda).

The numerator coefficients of the last two terms are Hölder and vanish at zero. Multiplication of such a coefficient by a fixed logarithmic power, including its bounded one-sided imaginary jump, gives `C^alpha'` for every `0<alpha'<alpha`. The inverse denominator is also Hölder after slightly lowering the exponent. Therefore the claimed expansion with a uniformly Hölder, vanishing error is valid; a pointwise big-O estimate is not being misused as a Dini estimate.

For a minimum, after shrinking away from the artificial upper endpoint,

    Lambda_+(x)=lambda(x)+log(eta-x)+i*pi*1_(x>0),
    Lambda_-(x)=lambda(x)+log(eta-x)-i*pi*1_(x>0),
    lambda=log(1/|x|).

Consequently the jump observation is exactly of the form

    m_q(U_+-U_-)/(2*pi*i)
      = C(q)+A(q)*lambda+B(q)*1_(x>0)+rho(q,x),
    A(q)=m_q(D_+-D_-)/(2*pi*i),
    B(q)=m_q(D_++D_-)/2.

These coefficients have the correct signs and factors. The bounded smooth term involving `log(eta-x)` contributes a constant at zero plus a Hölder remainder. Equality `D_+=D_-` is unnecessary. The upper causal boundary alone has coefficients proportional to `m_q(D_+)` and `i*pi*m_q(D_+)`, so the same receiving cancellation applies to the actual causal transform formulation.

At the exact critical receiver, `m_q=ell`. The displayed exact formula for `ell(U)` already yields a Hölder/Dini boundary when `a(0)=0`. This exact-critical-only observation does not establish uniformity at other receivers; that additional conclusion depends on the next optical step.

## 5. Why both amplitudes vanish, and their detuning rate

Let `Z={q:k*Omega_i(q)=nu_c}` and `delta(q)=k*Omega_i(q)-nu_c`. The optical identity applied to the upper regular inverse with zero scalar forces its positive weighted resonant square integrals to vanish. Since `w_i>0` on each regular open resonant curve and the extracted coefficient is continuous, `m_q(V_+(0))=0` at every such point. At a boundary point that is a limit of positive-weight points **on the same resonant level**, continuity gives the same conclusion. The lower boundary satisfies the analogous identity; alternatively real operator symmetry gives its vanishing scalar.

At the designated Morse point, the receiving functional equals `ell`, so the scalar-zero assumption itself gives the missing critical trace. The geometric hypothesis excludes any other singular receiver level point requiring a separate argument. Thus

    m_q(V_+(0))=m_q(V_-(0))=0 on Z,
    A(q)=B(q)=0 on Z.

Uniform Hölder extraction supplies, for these fixed fields,

    |A(q)|+|B(q)| <= C*dist(q,Z)^gamma.

The stated regular/Morse geometric error bound then gives

    |A(q)|+|B(q)| <= C*|delta(q)|^(gamma/2).

At regular levels the stronger exponent `gamma` is available locally, but it is unnecessary. This step is the needed source of uniformity over moving receivers. It supplies an algebraic rate, rather than merely pointwise convergence to zero.

**Weight and boundary scope.** Optical cancellation has no force at a zero-weight level component that is not approached by positive-weight resonances on that same level. In particular a regular level merely touching a flat support cap need not satisfy this argument. Flatness of `w` does not produce a zero receiving trace there. A cap point satisfying the explicit same-level approximation condition is covered, but no blanket cap conclusion follows. The compact eccentric hypotheses likewise do not verify the full circular-line endpoint. No uniform lower bound for `w` on the whole family is needed once exact vanishing on the positive-weight curves is proved; pointwise positivity and continuity suffice.

## 6. Uniform shifted oscillatory integrals

Let `chi` be a fixed smooth cutoff supported sufficiently close to zero and equal to one near zero. For `d=|delta|>0` small, put `y=x-delta` and split at `|y|=d/2`. This inner interval is symmetric in `y` and does not meet the logarithmic singularity `x=0`.

For the logarithm, subtract `lambda(delta)` on the inner interval. There `|lambda'(x)|<=2/d`. The residual divided by `y` has uniformly bounded integral, while the constant term equals a multiple of a sine integral and is bounded by `C*(1+log(1/d))` uniformly in time. On the exterior with `|x|<=2d`, the denominator is at least `d/2`, so its absolute integral is bounded by

    C/d * integral_(|x|<=2d) (1+|log|x||) dx
      <= C*(1+log(1/d)).

On `|x|>2d`, `|x-delta|>=|x|/2`, giving the bound

    C*integral_(2d)^eta (1+log(1/x))/x dx
      <= C*(1+log^2(1/d)).

For the step, it is constant on the inner interval, so the same sine-integral cancellation is uniform. The near exterior has bounded integral and the far exterior gives at most `C*(1+log(1/d))`. Smooth cutoff terms are harmless. The proof works for either sign of `delta`.

Therefore the two displayed shifted estimates in Section 6 are valid. Combining them with the coefficient rate gives bounds by constants times

    d^(gamma/2)*(1+log^2(1/d)),
    d^(gamma/2)*(1+log(1/d)),

which remain bounded as `d` tends to zero. At `delta=0` both amplitudes are exactly zero, so the singular displayed pieces are absent. This does not evaluate a divergent integral and then multiply it by zero. The bounded constant term and uniformly Hölder remainder have uniformly bounded work by the elementary Dini/sine-integral estimate. Receivers a fixed positive distance in frequency from zero are covered by the ordinary smooth-away-from-zero estimate and compactness. The finite number of potentially resonant harmonics on the compact family causes no further summation issue for this local statement.

## 7. Bordered criterion and qualifications

The block algebra in Section 4 passes. With `B_0=[[A,-v_0],[ell,0]]`, compactness of `R` makes `B_0` Fredholm of index zero. If `A` is invertible, its Schur complement is exactly `ell(A^-1 v_0)`, so border invertibility is equivalent to nonzero scalar. The change of variable `eta=Lambda*(ell(U)+b)` gives the exact bordered system with bottom-right entry `-1/Lambda`. A Neumann expansion about an invertible border yields the stated common-in-`sign(x)` constant and inverse-log terms. Finite-part shifts act by the stated row operation.

For `B_0^-1=[[E,f],[g,h]]`, the formula

    (A+d*v_0 tensor ell)^-1 = E-f*g/(d+h)

has the correct sign when `d+h!=0`; `ell(f)=1` shows singularity when `d+h=0`. The fractional-linear dressed-scalar transformation is also correct.

The border criterion itself does not prove its invertibility for the actual operator. Its optical interpretation in Section 5 additionally needs the relevant boundary reciprocal pairing/limit to exist for a constrained threshold solution. The ordinary-inverse construction used in Section 3 is not available when `A` is singular, so that interpretation should not be justified merely by reusing `V_epsilon=(I-R(z))^-1 v`. This does not affect the Section 6 theorem, which explicitly assumes the regular inverse. I do not certify a new singular-`A` optical boundary construction here.

The Section 5 energy-space warning is sound: if a threshold numerator has a nonzero linear term in action displacement, division by a Morse quadratic denominator creates amplitude comparable to `1/r` on an angular sector; its weighted square integral diverges as `integral dr/r`. Thus trace cancellation at the single critical point is insufficient for energy-space membership. This is not evidence for existence of an actual threshold obstruction.

## 8. Obligation matrix and exact remaining work

| Obligation | Audit result |
|---|---|
| Actual shell signs, action measure, and source harmonic | Passed |
| Critical coefficient `v_0=-beta*P e_c` | Passed |
| Finite-epsilon optical identity | Passed |
| Optical boundary limit | Conditional on the named regular inverse/coarea hypotheses |
| Rank-one zero-scalar expansion as a Hölder remainder | Passed under the stated Hölder hypotheses |
| Upper/lower jump coefficients | Passed |
| Pointwise receiving cancellation on `Z` | Passed with positive weight or the stated same-level limit condition |
| Algebraic rate in receiver detuning | Passed with the explicit distance-to-level estimate |
| Shifted logarithm and step work integrals | Passed; uniform in time and either sign of detuning |
| Uniform local receiving-work conclusion | Conditional on the actual causal/jump work representation and the other named inputs |
| Border algebra and finite-part invariance | Passed |
| Actual complete regular inverse or actual border injectivity | Not established; not assumed proved by this audit |
| Optical limit for singular-`A` constrained solutions | Not certified here |
| Arbitrary cap/circular receiver extension | Not addressed beyond the explicit geometry/weight assumptions |
| Global work or confinement | Out of scope |

The smallest remaining analytic obligation for using Section 6 on a fixed actual equilibrium is to establish the **complete** regular inverse and its boundary regularity, with all other channels included, and to identify its locally integrable upper transform boundary with the local frequency contribution in the actual work formula. The theorem does not require a nonzero dressed scalar. The cheapest next analytic discriminator is the complete regular boundary problem, followed by checking which actual receiving level sets satisfy the same-level positive-weight approximation at the support boundary.

One forced wording correction was identified in the raw scratch: its opening sentence of Section 6 says zero scalar is “not a necessary condition for failure.” The theorem instead shows that zero scalar is **not sufficient for failure**, or, equivalently, that nonzero scalar is **not necessary for bounded local receiving work**. These are different logical statements. The coordinator's repository copy, checked above, correctly changes this to “A zero scalar does not force failure of receiving work” and corrects the final sentence to “zero a_0 alone is insufficient to obstruct bounded local receiving work.” This wording issue is resolved in that copy.

Commands used were text reads/searches (`cat`, `sed`, `rg`, `ls`/`head`), `diff -u` for the two localized prose corrections, and `shasum` for provenance, followed by creation/update of this one new scratch audit file. No supplied script or numerical result was run or used as evidence. This is an independent reconstruction in a fresh delegated session, not a formal proof certificate.
