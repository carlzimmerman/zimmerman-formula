# Repair attempt: exact health construction, then force and pressure costs

This new lane does not modify the accepted principal calculation. Target: retain the FRW quadratic clock and flat density-gate derivatives, remove the positive-D obstruction by an actual action change, and check the force/stress that the change introduces. All formulas below concern Q>0 and Pi>=0 unless an extension is stated. Constants C,L,Pi_c are positive; L is a new dimensionless clock scale, not a derived parameter. Set x=Q-1, u=Pi/Pi_c, F=Cx² and S=exp(-u³).

## 1. Two precise impossibility statements

A convex clock function matching F'(1)=0 and F''(1)>0 cannot be bounded above on Q>=1: its derivative becomes positive and cannot decrease afterward, so its value grows at least linearly. Strict convexity alone on Q>0 is insufficient for that assertion (exp(-Q) is a counterexample); the quadratic clock's minimum is essential.

For each fixed Q, a nonnegative concave function of Pi on the entire half-line, with initial derivative zero, cannot decrease nontrivially while staying nonnegative. Once its derivative is negative, concavity keeps it negative and the function eventually crosses zero. Thus globally nonnegative H, flat H_Pi(Q,0)=0, nontrivial suppression and H_PiPi<=0 are incompatible on an unbounded Pi domain. An action can nevertheless contain a negative potential with positive energy, so this does not rule out the repairs below.

Similarly, if a concave total Pi potential has identical initial and asymptotic slopes, it must be affine. That statement cannot be promoted to a force-preservation theorem without checking the Q dependence: a term proportional to Q Pi is an exact spatial boundary, while one proportional to Pi alone is not.

## 2. First construction: bounded gated part and Q-independent stiffness

Let B0=C L²[1-exp(-x²/L²)] and define

```text
H0 = F-B0+B0 S-Gamma(u),
Gamma(0)=Gamma_u(0)=0,
Gamma_uu = 9 C L² u⁴ exp(-u³).
```

B0<=F and B0<=CL². Since `B0_QQ=2C exp(-x²/L²)(1-2x²/L²)<=2C`, H0_QQ>0 at every finite Pi. Also

```text
H0_PiPi = exp(-u³)/Pi_c² [9u⁴(B0-CL²)-6uB0] <= 0.
```

H0(Q,0)=F, and H0_Pi=H0_QPi=H0_PiPi=0 at Pi=0. Gamma starts as `.3 C L² u^6`. The clock derivative is suppressed by the exact factor `1-(1-S)exp(-x²/L²)` in the small-offset band; high Q returns toward the ungated quadratic clock.

The repair fails its unchanged-force test. Write

```text
Gamma(Pi) = lambda Pi-J+o(1),
lambda = [3 Gamma_Euler(5/3)] C L²/Pi_c,
J = 3 C L²,
3 Gamma_Euler(5/3) = 2.708235878852801... .
```

Because `integral sqrt(-g) Pi = -integral sqrt(-g) P.A + boundary`, the asymptotic law sector becomes `(1+lambda)P.A-W+J`. The normal source also has `(1+lambda)Pi`. With beta=1+lambda and unchanged QX17 W, elimination gives

```text
mu_eff(g/a0) = 1-beta²/[1+beta g/a0].
```

For beta>1 its deep-field limit is negative; for the physical suppression bounds it is grossly different from the intended law. Subtracting lambda Pi changes the FRW endpoint coefficient instead of being a harmless boundary. The numerical force comparison is independently recorded by `../../static_gate/matching/RESULT.md`.

## 3. A genuine next repair: Q-dependent compensation

To restore the force coefficient, use the following perspective form of the gated piece:

```text
t=x²/(L² Q),
B(Q)=C L² Q [1-exp(-t)],
H1(Q,Pi)=F-B+B S-Q Gamma(u),
Gamma_uu=9 C L² u⁴ exp(-u³),  Gamma(0)=Gamma_u(0)=0.           (1)
```

This is a nonmultiplicative construction satisfying the requested convex/concave conditions. In fact

```text
0<=B<=min(F,QCL²),
B_QQ=C exp(-t)[2-(Q²-1)²/(L² Q³)]<=2C,
H1_QQ=2C-(1-S)B_QQ>0,
H1_PiPi=exp(-u³)/Pi_c² [9u⁴(B-QCL²)-6uB]<=0.               (2)
```

These hold for every Q>0 and finite Pi>=0; H1_PiPi<0 for u>0. This is global convexity/concavity, not global physical health: the original quadratic clock already has negative energy/enthalpy on portions of Q<1. Positive-energy principal statements require the corresponding energy/enthalpy conditions, including the studied Q>=1 branch. There is no uniform positive lower bound on H1_QQ as Q approaches1 and u increases without bound. The Q-linear compensator does not alter H_QQ. At Pi=0, H1=F and H1_Pi=H1_QPi=H1_PiPi=0. If a C2 extension to negative Pi is desired, taking S=1 and Gamma=0 there preserves these algebraic convexity/concavity properties; it is a changed negative-Pi gate and still needs its own physical analysis.

The normal clock energy is unaffected by the Q Gamma term. The key identity is

```text
Q B_Q-B = C(Q²-1) exp(-t),
[Q H1_Q-H1]/[C(Q²-1)] = 1-(1-S)exp(-t),       Q>1.           (3)
```

Thus this candidate has an exact positive clock-energy suppression factor, not merely a claim about H_Q. For a required fraction delta and S<delta,

```text
L² >= x² / { Q [log(1-S)-log(1-delta)] }.                   (4)
```

In the off-gate region it is x²/{Q[-log(1-delta)]}. This is a different bound from the non-perspective first candidate; numerical inputs are not silently pooled.

The asymptotic term `-lambda Q Pi` is a spatial boundary exactly: in unitary gauge NQ=q(t), so its action is `-lambda q(t) integral partial_i J^i`. Consequently the off-gate action has the original P.A coefficient and W, but it contains

```text
H1_off equivalent to R(Q)+QJ,       R=F-B>=0.                (5)
```

This resolves the first repair's force-normalization problem but exposes a stress cost. QJ has zero lapse energy and positive pressure QJ; it is not a cosmological constant. The total leading center/off-gate stresses are

```text
rho = Q R_Q-R+Pi+W,
p = R+QJ + polarization corrections,
rho+p = Q R_Q+Pi+QJ + corresponding corrections.            (6)
```

Thus the repaired clock energy can be suppressed while a large pressure remains. Omitting that pressure is a partial-variation error. Removing QJ globally changes the FRW clock pressure/charge; a cosmological constant cannot cancel a zero-energy, nonzero-pressure term while preserving the original background.

## 4. The pressure cannot be tuned to zero within this class

Allow any C2 Gamma with Gamma(0)=Gamma_u(0)=0 that makes (1) concave in Pi for all Q>=1. At Q=1, B=0, so Gamma_uu>=0. At any u with S''(u)>0, taking the supremum over Q gives

```text
Gamma_uu(u) >= B_star S''(u),
B_star = sup_(Q>=1) B(Q)/Q = CL².                           (7)
```

The supremum is exact for the perspective B. If Gamma has an asymptotically linear part with a finite intercept, its intercept is

```text
J = integral_0^infinity u Gamma_uu(u) du
  >= B_star integral_(2/3)^(1/3)^infinity u S''(u) du
  = 3 exp(-2/3) B_star
  = 1.540251357097776... B_star.                             (8)
```

The boundary evaluation uses S'= -3u²S and u0³=2/3. Divergent first moment gives an even worse non-finite pressure limit. The explicit Gamma in (1) has J=3B_star; optimizing its shape can reduce that numerical factor, but cannot remove it. A function chosen to cancel the intercept needs negative Gamma_uu somewhere, contradicting (7)'s Q=1 requirement. This obstruction is specific to this compensation class and its global concavity/FRW conditions, not every possible modified action.

The pressure bound also holds at finite gate argument, so no uniform off-gate limit is needed. For u>=u0,

```text
u Gamma_u-Gamma >= B_star[3 exp(-2/3)-(3u³+1)exp(-u³)].       (9)
```

The explicit compensator has `u Gamma_u-Gamma=3B_star[1-(u³+1)exp(-u³)]`. The complete repaired-clock pressure is `R+B(S-uS')+Q(u Gamma_u-Gamma)`, and its first two terms are nonnegative. Thus Q times (9) is a lower bound on this actual isotropic clock pressure, before any separately added compensation sector. At u=4 the omitted dimensionless tail in (9) is `193 exp(-64)=3.09536e-26`.

## 5. Physical size on the specified matching target

`check_repair.py` reads and hashes the static lane's canonical annulus inputs, but recalculates (4) for the perspective candidate and uses the physical energy fraction (3). The comparison assumes the same target annulus and effective clock-mass suppression ceiling; it is not a new galaxy fit or an assertion that this repaired action generates that annulus.

In geometrical units C=mu_K²/(2K), Q,L are dimensionless, Pi and H have energy-density units, KPi and KJ have inverse-length-squared units, and lambda is dimensionless. On the supplied Mb=1e11 Msun target, the largest weak clock offset is about2.217945e-6 and KPi_c=1.82857418e-7/Mpc². For mu_K=25120/Mpc and delta=1.5847498884e-9, (4) requires L² about.00310413 and (8) requires KJ about1.50848e6/Mpc². At the outer point this pressure is about2.06238e12 times the target polarization density. For mu_K=198.25/Mpc the corresponding ratio is about8000.86. Exact executed values and the weak-potential mapping Q=1+abs(Phi) are in `run_001/result.json`.

The radius `(Kp_clock,min)^(-1/2)` is about.814 kpc in the larger-mu case, compared with the .732 Mpc reference outer radius. In Einstein gravity isotropic pressure contributes to the active source through rho+3p. Such a pressure cannot be silently retained in the same weak, low-curvature galaxy target; an added compensating stress or a changed action/background would need an explicit calculation. The numerical contradiction is conditional on the stated matching target and its suppression ceiling, not a new observational exclusion. The reference table's largest and smallest clock offsets use a weak-potential mapping; the fractional corrections from changing that mapping are far too small to account for the displayed pressure ratios.

## Outcome and next surviving obligation

There is an explicit globally convex-Q/concave-positive-Pi repair with the requested FRW derivatives. It therefore refutes an unconditional mathematical impossibility claim for nonmultiplicative H. The first version changes the force law; the Q-compensated version restores the asymptotic force coefficient but has an irreducible pressure incompatible with the specified small-field target unless another stress mechanism is supplied.

Within this class, the new obligation is a jointly varied compensation sector or a derived restricted state domain that relaxes global concavity while preserving the full constrained spectrum. Merely declaring the extra slope a boundary, subtracting the pressure without varying the action, or choosing an unproved cutoff does not satisfy it. No such additional sector, transport solution, coefficient normalization or complete theory is claimed here.
