# High-frequency inverse without small cold mass

Checkpoint ZAR-2026-10-19-11-CX. Analytic derivation by `/root`.
This proof uses the actual kernels and the complete source charts proved in
`BOUNDARY_PAIRING.md`. Assume its (H1), (H2), (H4), and assume the full action
gradient of each `Omega_i` is nonzero on a neighborhood of the entire closed
occupied set. These hypotheses hold for the sufficiently narrow, fixed-positive
warmth cold-dominated family in `GEOMETRY_AND_CAP.md`. No isolated eccentric
Morse subtraction is used in this theorem.

Let `Y_gamma=C^gamma(I)^2`, `0<gamma<1/2`. Choose

    0<beta<gamma^2/(1+gamma),
    p=gamma-(1+gamma)*beta/gamma>0,
    eta=1-beta.

Then the actual full boundary operator satisfies, for `Im z>=0`, including
its upper boundary values,

    ||K(z)||_(Y_gamma -> C^eta) <= C (1+|z|)^(-p).       (1)

The same assertion holds on the lower half-plane. In particular there is a
finite `Z_*`, depending on the fixed equilibrium, for which

    |z|>=Z_*  =>  ||K(z)||_(Y_gamma -> Y_gamma)<=1/2,
    ||(I-K(z))^-1||_(Y_gamma -> Y_gamma)<=2.             (2)

This is a frequency smallness statement for a fixed actual halo, not a
small-mass or small-warmth susceptibility assertion. Constants may depend on
the chosen cold-dominated halo and its fixed warmth.

## 1. Actual shell harmonics gain an inverse harmonic

For one source species and one output species set

    P_n(r,q)=(2*pi)^-1 integral_0^(2*pi)
                     P(r,r(theta,q))*exp(-i*n*theta) dtheta.

At an eccentric radial orbit, choose the angle origin at pericenter. Radius
increases on the first half period and decreases on the second. For `n!=0`,
the indicator coefficient

    A_n(r,q)=(2*pi)^-1 integral 1_(r(theta,q)<r)
                                      *exp(-i*n*theta) dtheta

is zero outside the turning radii, and between them equals
`sin(n theta_r)/(pi n)`. Thus `|A_n|<=1/(pi |n|)`. The circular case has
zero nonconstant indicator harmonics and is also covered.

For the actual kernels, their weak output derivatives are

    partial_r P_ff=partial_r P_ft=partial_r P_tf
                   =(G/r^2)*1_(r'<r),
    partial_r P_tt=-(2 G^2 M_t(r)/(a_0 r^4))*1_(r'<r).

The coefficients are bounded on the fixed hollow shell. Differentiation in
the weak sense followed by integration over the orbit therefore gives

    |P_n(r,q)-P_n(r',q)| <= C |r-r'|/|n|.              (3)

At output radius `R` the kernel is constant on each source orbit, so its
nonzero harmonics vanish. Equation (3) also bounds `||P_n||infinity<=C/|n|`.
No derivative of an action-angle coordinate at `J=0` is involved.

For an arbitrary test field `phi in Y_gamma`, the ordinary receiving estimate
gives `|phi_n(q)|<=C |n|^(-gamma)||phi||Y_gamma` uniformly on the closed
occupied set. Consequently

    ||[P_n(r,.)-P_n(r',.)]*phi_n||infinity
       <= C |r-r'| |n|^(-1-gamma)||phi||Y_gamma.        (4)

## 2. Interpolate action regularity before taking the Cauchy transform

Write `d=|r-r'|`. As a radial source test function,

    f_d(u)=P(r,u)-P(r',u)

has sup norm at most `C d` and a Lipschitz seminorm bounded independently of
`d`. Elementary interpolation gives

    ||f_d||C^gamma <= C d^(1-gamma).                   (5)

The circular product lemma in `BOUNDARY_PAIRING.md` applies to the orbital
product `(f_d)_n phi_n`. It makes that product `C^gamma` in ordinary actions
`(J,L)` with norm at most `C d^(1-gamma)||phi||Y_gamma`, and allows extension
by zero across `J=0`. Multiplication by the fixed smooth susceptibility,
`Omega_i`, and a smooth chart partition preserves the estimate. Flat zero
extension of susceptibility handles the cap and angular-momentum ends.

Interpolate this `C^gamma` action bound with (4). For each source chart the
resulting amplitude `a_n` obeys

    ||a_n||C^beta_(J,L)
      <= C [d |n|^(-1-gamma)]^(1-beta/gamma)
             [d^(1-gamma)]^(beta/gamma)||phi||Y_gamma
      = C d^(1-beta) |n|^(-1-p)||phi||Y_gamma.          (6)

All constants are independent of the harmonic `n`. This step retains both
the output-radius difference and harmonic decay. Using only the source-dual
norm would lose the latter.

The same finite submersion charts work for every harmonic: use frequency
`y=Omega_i(q)`, not `n Omega_i(q)`. The zero-extended amplitude in (6) pushes
forward to a compactly supported `C^beta` density `b_n(y)`, on one fixed
frequency interval bounded away from zero. Its norm has the same bound (6).
This includes circular tangencies because the *product* has the justified
ordinary-action extension. Smooth partitions leave no moving-boundary term.

The `n`th feedback term is, with the appropriate source/output indices,

    K_n(z)phi(r)-K_n(z)phi(r')
        =-integral b_n(y)/(y-z/n) dy.                 (7)

The factor `Omega_i` is already in `a_n`; there is no missing factor of `n`.
For negative `n`, the corresponding Cauchy argument lies in the other half
plane, whose norm estimate is identical.

The Cauchy transform of a compactly supported `C^beta` density is uniformly
bounded on the two closed half-planes. One proves this by subtracting its
value at the real evaluation point: the local difference is bounded by the
integral of `|s|^(beta-1)`, and the constant part is an explicit bounded
logarithm/delta term after a fixed smooth cutoff is inserted. Far from the
support the transform tends to zero. The same proof works for the norm of
the bounded linear operator represented by the density; it uses no positivity.
Equation (7) therefore yields

    ||K_n(z)||_(Y_gamma -> C^(1-beta))
        <= C |n|^(-1-p)                              (8)

uniformly on either closed half-plane. The value at output `R` is zero, so
the output seminorm also controls the full norm. The summation in (8) is
absolutely convergent in this operator norm.

## 3. Decay and inversion at large frequency

If `|n|<=|z|/(2 Omega_+)`, then
`|y-z/n|>=|z|/(2|n|)` on the frequency support. Use that bound directly in
(7) instead of its boundary Cauchy estimate. It improves (8) to

    ||K_n(z)||_(Y_gamma -> C^(1-beta))
       <= C |n|^(-1-p) |n|/|z|.                      (9)

For the other harmonics retain (8). Since `0<p<gamma<1`, splitting the
series at `|z|/(2 Omega_+)` gives

    sum_(|n|<=c|z|) |n|^(-p)/|z|
       +sum_(|n|>c|z|) |n|^(-1-p)
          <= C |z|^(-p).

This proves (1) for large `|z|`; (8) gives the bound for bounded `|z|`.
Because `eta>gamma`, the embedding into `Y_gamma` is bounded, and (2)
follows by the ordinary convergent Neumann series.

For completeness the same density argument gives global boundary frequency
continuity. For every `0<alpha<beta`, the Cauchy transform is `C^alpha` on
each closed half-plane with norm bounded by the density's `C^beta` norm.
The `n`th contribution therefore has seminorm at most
`C |n|^(-1-p-alpha)` when frequency is measured in `z`. Summing proves a
global `C^alpha` bound for `K` into `C^(1-beta)`. This is separate from the
decay bound, and does not assert frequency differentiability.

## 4. Consequences and limits

Combined with a proof that kernel frequencies are locally finite, (2) makes
their union globally finite for each fixed halo satisfying these hypotheses.
All remaining inverse obstructions then lie at finitely many actual mode
frequencies. That kernel-to-energy and local-finiteness argument is supplied
in the separate inverse proof; it is not inferred from (1) alone.

This theorem does not exclude the finite modes, prove their receiving force
traces vanish, or bound the pole-subtracted threshold response. In particular
it does not yet establish uniform closed-support work. It concerns the full
operator with no full-frequency critical point; it does not extend (1) to a
general halo with unremoved eccentric critical logarithms.
