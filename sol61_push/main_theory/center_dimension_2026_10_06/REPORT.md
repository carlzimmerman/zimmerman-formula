# The regular-center obstruction is dimensionally consistent

The prior four-dimensional center theorem is not an accidental coefficient mismatch. It extends to n>=3 spatial dimensions when the acceleration response is normalized to cancel the actual n-dimensional weak Einstein lapse stiffness. This is a sharper obstruction to this local critical-response mechanism, not a derivation of32pi or a no-go for every MOND theory.

## Dimensional dictionary and actual critical coefficient

Take d=n+1, Einstein action K_E R/2, signature(-,+,...,+), K=-c ln(X/Xref), G=-sqrt(2)c/(nH)X^(-1/2). Here c is the scalar-action coefficient, not the speed of light. Define A_n=n(n-1)/2, eta=c/(A_n K_E H²)>0, b=2c/(nH), Veff=A_n K_EH² on the selected normalized rolling vacuum. The scalar action is invariant under the same classical vacuum-rescaling map. [K_E]=mass^(n-1), [c]=mass^(n+1), and H and clock acceleration have dimension inverse length. No hbar enters the center relation.

The weak static Einstein equations give, with B=1+b_weak and N=1+Phi,

`b_weak=rPhi'/(n-2)` and `Delta Phi=(n-2)rho/[(n-1)K_E]`.

Eliminating the radial metric from the weak action gives lapse-gradient density `-K_E lambda_n |grad Phi|²`, where

`lambda_n=(n-1)/[2(n-2)]`.

Thus a normalized-clock response with leading `+K_E lambda_n a²` is critical in the actual n-dimensional Einstein theory. Setting the coefficient to its four-dimensional value1 in every dimension is incorrect. The n=2 logarithmic Newtonian case is excluded from this dictionary.

## Universal necessary center equations

Use the stationary areal metric `ds²=-N²dt²+B²(dr+Vdt)²+r²dOmega_(n-1)²`, regular physical center and regular clock,

`N=N0(1+n2 r²+o(r²)), B=1+b2 r²+o(r²), V=N0 x r+o(r)`.

Matter is a finite static Killing-fluid source with proper rest-frame rho0 and p0, and its actual nonzero ADM momentum is retained. Put R=rho0/K_E, P=p0/K_E, and u0=-A_n H²+2c lnN0/K_E. Assume the covariant response is `K_E lambda_n a²+o(a²)` with derivative remainders controlled; P2 and its high-force cutoff fulfill this local condition in four dimensions.

Vary the radial metric and lapse before inserting the center expansions. Their leading r^(n-1) coefficients are respectively

```
(n-1)(n-2)b2-2(n-1)n2+A_n x²+u0=-P,
n(n-1)b2-4n lambda_n n2+A_n x²+u0
  +2c/K_E+2c x/(K_E H)=R.
```

Multiply the first by n/(n-2) and subtract it from the second. The adjustable n2 term cancels precisely for lambda_n above. The necessary remaining quadratic is

```
x²-(n-2)eta H x-[1+(n-2)eta]H²+2eta H² lnN0
  +[(n-2)rho0+n p0]/[n(n-1)K_E]=0.
```

Its discriminant must satisfy

```
Delta_n=[(n-2)eta+2]²H²-8eta H² lnN0
  -4[(n-2)rho0+n p0]/[n(n-1)K_E] >=0.
```

At n=3 this is exactly the independently audited four-dimensional source bound. For every fixed finite eta and weak normalized lapse |lnN0|<<1, the weighted density/pressure cannot be parametrically larger than K_EH². Critical lapse cancellation removes the center freedom that would have balanced a dense regular source. Changing only the high-force tail of the response cannot repair this small-acceleration condition. A source-free normalized center admits x=-H, consistent with the cosmological benchmark.

The conclusion requires regular metric/clock and static finite fluid; it does not assert every weak or singular solution is impossible. The nonanalytic center and source-momentum caveats are recorded in ../flowing_clock_interior_2026_10_06/REPORT.md. Positive pressure strengthens the bound. A strong central redshift, changed matter, nonstationary data, an external nonspherical clock gradient or a detuned quadratic response changes the premises and needs a new calculation.

## What detuning actually changes

For leading response `(1-epsilon)K_E lambda_n a²`, epsilon>0, the eliminated quadratic gains `-2epsilon n2`. The density equation no longer imposes the same ceiling independently of n2. In the weak radial constitutive balance this introduces a residual linear term, so exact MOND behavior cannot persist to arbitrarily small acceleration in that local response. A regular core can be considered, but epsilon is an additional input until selected by another physical principle. The separate regularized-core investigation tests actual center branches; this observation alone proves neither existence nor32pi selection.

## Evidence and scope

The accompanying script independently varies the general radial action for each n=3..8 and checks the two leading coefficients, their exact elimination, the cosmic center and the detuning term. The universal result follows from the displayed n-dependent action and algebra; finite dimensions are verification controls, not proof for all n. A mutation uses lambda=1 in every dimension and fails the critical cancellation beginning at n=4. Actual tested source normalization remains the Einstein coefficient above; no four-dimensional8pi source convention is silently reused for general n.
