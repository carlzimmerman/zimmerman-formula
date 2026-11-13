# CP02 outer matching and the bounded-piece repair

This continuation goes beyond the successful inner annulus. It gives an analytic obstruction to a globally nonnegative static polarization principal coefficient for the **literal** flat gate, and a quantitative failure of the proposed Q-independent stabilizing repair with unchanged QX17 polarization potential. Neither result is a universal no-go for every modified action or every constrained-GR healthy branch.

## 1. A deformed, compensated outer state on the nonnegative-coefficient branch

Assume a regular static clock orthogonal to static slices and the literal gate

\[
H=\frac{\mu_K^2}{2K}(Q-1)^2e^{-(\Pi/\Pi_c)^3},\quad \mu_K>0,\quad\Pi_c>0,
\]

with QX17's one-sided stiffness `gamma Pi_+²/2` and strictly convex W, minimized only at P=0. Define the scalar coefficient

\[
\mathcal C=\gamma\mathbf1_{\Pi>0}-H_{\Pi\Pi}.
\]

It is the coefficient of the divergence-gradient term in the static polarization equation; it is **not by itself** the full constrained-GR kinetic eigenvalue. Suppose `C>=0` everywhere on the proposed static matching branch.

**Claim 1. Pi cannot be negative anywhere on such a regular static solution.**

Proof: for u<0,

\[
S''(u)=(9u^4-6u)e^{-u^3}>0.
\]

On the open set where Pi<0, stiffness is inactive, so `C>=0` implies `(Q-1)²=0`. Thus Q=1 throughout that open set. Staticity then gives A=-D ln Q=0 there, while H_Pi and its spatial derivative vanish identically. The exact leaf equation reduces to W_P=0, hence P=0. That implies Pi=0 on that open set, a contradiction. A single Q=1 crossing does not evade this open-set argument. Q=1, Pi<0 points would have an open negative-Pi neighborhood by continuity.

This argument uses the **actual static equation**, not an arbitrary independent assignment of Q and Pi.

**Claim 2. Starting from the positive radial polarization of the solved inner annulus, a regular spherical compensated exterior cannot stay on this branch.**

In a spherical static spatial geometry, integrating Pi=D_i P^i between spheres gives the change in outward polarization flux. Pi>=0 therefore makes that flux nondecreasing. In the weak-field dimensionless variables of the executed solve,

\[
(x^2p)'=x^2Z\ge0.
\]

At x=60 the accepted annulus has `x²p=59.5021...>0`. Any proposed regular compensated asymptotic state in which the polarization response decays faster than 1/r² would instead have flux tending to zero. This contradicts monotonicity. The argument does not assume that the intermediate gravitational density contrast is positive; a compensating negative contrast cannot remove this polarization-flux constraint while Pi remains nonnegative.

For the other ordinary finite-flux possibility, a nonzero finite limiting polarization flux gives P~P2/r². A regular restored-gate exterior with finite mass, decaying derivative corrections and nonzero limiting constitutive coefficient then has g proportional to P at leading order. The potential has a nonzero 1/r term. The restored quadratic clock contributes a source proportional to that potential, of order 1/r, incompatible with the finite-mass Laplacian/polarization asymptotics. This is the finite-Gauss-tail argument in the parent `RESULT.md`, with the needed asymptotic regularity stated rather than inferred from flux monotonicity alone.

Therefore the literal-gate physical annulus cannot be completed into a regular spherical finite-mass or compensated decaying exterior while retaining `C>=0` everywhere. A proposed completion must abandon at least one of these explicit conditions: the literal negative-Pi gate, the nonnegative static principal coefficient, regular static matching, the retained positive inner polarization, or the ordinary decaying asymptotics.

This is an analytic matching obstruction, not an inference from a solver exceeding its mesh cap. It allows deformation and compensation inside its stated branch class.

### Limits and the clamp escape

`C>=0` is a strong auxiliary coercivity condition. The health lane confirms that it is sufficient in the studied regular sectors, but has **not** proved it necessary for every finite-P static solution after all GR constraints. Positive H_PiPi-gamma can in some reductions have a positive high-frequency constrained kinetic coefficient. Consequently these claims must not be relabeled “no healthy static solution of any kind.” They identify exactly which branch must be left.

The clamped gate `exp[-(max(u,0))³]` has S''=0 for negative u. It escapes Claim 1. The clamp therefore requires its own matching and health analysis; the argument cannot be copied to it. The separate positive-Pi transition obstruction and positive-Pi health counterexamples do not depend on this negative-Pi feature.

For additional sign information: the decaying negative-potential Yukawa mode derived with active stiffness has negative Pi and is inconsistent with that active branch. The opposite positive-potential Yukawa mode has inward P and positive Pi. It cannot be reached from the positive inner polarization without a decline and reversal of polarization flux, hence without negative Pi somewhere. This reinforces the flux obstruction, but is a local asymptotic mode observation rather than an independent global existence theorem.

## 2. The bounded-piece Q-independent stabilizer

The health lane proposed, with `x=Q-1` and a new dimensionless clock scale L_Q,

\[
F=C_Qx^2,\quad B=C_QL_Q^2(1-e^{-x^2/L_Q^2}),\quad
C_Q=\mu_K^2/(2K),
\]
\[
H=F-B+B S-\Gamma(\Pi),\qquad
\Gamma''=\frac{9C_QL_Q^2}{\Pi_c^2}u^4e^{-u^3},
\quad \Gamma(0)=\Gamma'(0)=0.
\]

The health purpose is explicit: H_QQ stays positive and the chosen stabilizer makes H_PiPi nonpositive. The present question is whether that repair also preserves the physical force law.

The exact fractional clock density derivative is

\[
\frac{H_Q}{2C_Qx}=1-(1-S)e^{-x^2/L_Q^2}.
\]

Requiring it to be at most delta gives, when S<delta,

\[
L_Q^2\ge \frac{x^2}{\log(1-S)-\log(1-\delta)}.
\]

Deep inside the off-gate region this becomes `L_Q²>=x²/[-log(1-delta)]`. Meanwhile

\[
\Gamma'(\Pi)=\frac{C_QL_Q^2}{\Pi_c}
\int_0^u9v^4e^{-v^3}\,dv,
\]
\[
\Gamma'_\infty=\frac{C_QL_Q^2}{\Pi_c}\,3\Gamma_{\rm Euler}(5/3),
\quad 3\Gamma_{\rm Euler}(5/3)=2.70823587885\ldots.
\]

Thus the desired suppression forces a large asymptotic slope. This is not harmless just because its spatial derivative tends to zero. Covariantly,

\[
\int\sqrt{-g}\,\Pi=-\int\sqrt{-g}\,P\cdot A+\text{boundary},
\]

so `-alpha Pi` adds `alpha P.A`. In the off-gate region define `beta=1+Gamma'_infinity`. The full static constitutive relation contains beta A. The leading normal density also contains beta Pi; omitting that density change would repeat the earlier partial-variation error.

With the unchanged QX17 W, elimination of P yields

\[
p=\frac{\beta y}{1+\beta y},\qquad
\mu_{\rm eff}(y)=1-\frac{\beta^2}{1+\beta y},\quad y=g/a_0.
\]

This cannot reproduce the desired simple-mu law for the large mandatory beta. For the values below it is negative throughout the reference annulus. This diagnoses the Q-independent repair with unchanged W; it does not forbid changing additional parts of the action.

The finite parameter calculation is in `run01/results.json`, manifest status **completed**, validated against its pinned script and the accepted physical-annulus result. Its inputs are the same canonical `Mb=1e11 Msun`, `rM=.01220427284 Mpc`, outer u=4, `KPi_c=1.82857418e-7/Mpc²`, and delta=(1/mu_K)^2 from the stated effective-mass ceiling. To suppress the whole x=1..60 annulus, the inner clock offset `abs(x)=2.21794508e-6` sets the strongest bound.

| mu_K / Mpc^-1 | required L_Q² | minimum K B_star / Mpc^-2 | minimum Gamma'_infinity |
|---:|---:|---:|---:|
| 198.25 | 1.93340e-7 | 0.00379943 | 56272.1 |
| 25120 | 0.00310414 | 979377.5 | 1.45052e13 |

Here `B_star=C_Q L_Q²`. At the outer reference point, y=.0168061, the latter beta gives `mu_eff=-8.63090e14`, a gross force-law and static ellipticity failure. Even using only the outer point to set L_Q would give `Gamma'>=4.61199e11` for mu_K=25120.

Subtracting `Gamma'_infinity Pi` to remove the galaxy slope changes the cosmological endpoint coupling. The health lane independently notes that it changes the FRW mixing coefficient from 1 to `1-Gamma'_infinity`; it cannot be declared a boundary-only correction. The later Q-dependent compensation repair is a distinct candidate, handled by that lane.

## 3. Conditional scale conversion for the Q-dependent compensation repair

The frozen numerical table contains a provisional scale conversion `J_trial=1.54025 C_Q L_Q²`. Its field named `K_Bstar_min_Mpc_inverse2` means exactly `K C_Q L_Q²`. **It is not a certified pressure floor for the original bounded B:** for the subsequent Q-dependent compensation, the relevant sharp constant is `sup_Q(B/Q)`, which is smaller than `C_Q L_Q²` for that original B. Independent review by the health lane identified this distinction before synthesis. At mu_K=25120 the conversion is:

\[
KJ_{\rm trial}=1.50848619\times10^6\ {\rm Mpc}^{-2}.
\]

This trial scale divided by the reference polarization energy density is `6.40e8` at x=1 and `2.06e12` at x=60. At mu_K=198.25 the corresponding outer ratio is about 8000.87. These numbers quantify the size of the proposed counterterm; they do not establish the original candidate's pressure bound. The health lane develops a separate perspective-form B for which `sup(B/Q)=C_Q L_Q²` exactly and recomputes the suppression requirement for that changed candidate. Its report, rather than these provisional columns, controls any final pressure-floor claim. The executed Q-independent force-slope bound in section 2 is unaffected.

## 4. Completed independent perspective-repair audit

The final perspective/Q-Gamma candidate is independently audited in [`perspective_audit/REVIEW.md`](perspective_audit/REVIEW.md), with accepted v2 evidence in `perspective_audit/run04`. That review supersedes the provisional pressure conversion above for this changed candidate. It verifies the exact energy suppression identity, finite-u compensator moment, and complete static on-shell spatial stress via a fixed-J metric variation.

The apparent covariant polarization-gradient stress is not an independent cancellation mechanism once the polarization equation is imposed. Mean pressure is bounded below by the compensator moment, with nonnegative additional QX17 W and stiffness contributions. Even requiring concavity only on the target's finite rectangular Q band leaves a high-mu lapse-flux requirement 3330.16 times the supplied target value. The exact identity retains Lambda; the numerical annulus comparison explicitly shares the benchmark's negligible-background assumption. The analogous low-mu finite-band ratio is .207306 and does not exclude that case.

This closes the current repair test on its stated static target and domain. It is not a claim against every possible action or a derived correlated Q–Pi state restriction.

## 5. Evidence and review boundary

- Matching Claims 1-2 are analytic and use the actual static constitutive equation plus flux monotonicity. No negative result is inferred from a failed numerical matching run.
- The nonnegative-principal-coefficient restriction is explicit and is not promoted to a necessary full-GR health criterion. The independent health agent reviewed Claims 1–2 and confirmed the stated logic, including the regular-asymptotics qualification, on 2026-11-12.
- The physical annulus is accepted only as a finite boundary-value solution; it supplies positive inner polarization flux and reference numbers, not global formation or an outer completion.
- The bounded-repair table is a finite computation with exact suppression inequality and explicit constants. The pressure columns are provisional scale conversions; the sup(B/Q) distinction above prevents treating them as a verified floor.
- The clamped gate is excluded from the negative-Pi matching theorem and must be considered separately.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
