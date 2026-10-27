# Constrained mediator continuation: power law, not logotropic closure

2026-10-27; observed HEAD `eee9769579834ae78531ee37adc3970090ac81da`, with concurrent work elsewhere. This continuation writes only this directory and leaves the parent field-route report unchanged.

**Verdict:** the positive-kinetic, quartic mediator in `../REPORT.md` does not generate a globally or asymptotically logotropic equation of state when eliminated locally. It gives a power-law response along a specified canonical adiabatic family. A stable scalar minimum also does not guarantee positive reduced compressibility. This closes the proposed constitutive check; it does not exclude a tuned approximation over a short finite interval or another parent action.

## Exact local minimum and threshold

Put $K=K_p$, $y=\chi^2\geq0$, and assume $a,m^2,\lambda>0$:

\[
 W(K,y)=\frac{K}{1+ay}+\frac{m^2y}{2}+\frac{\lambda y^2}{4}.
\]

An additive $V_0$ is omitted here. It adds $V_0$ to the minimized energy and $-V_0$ to pressure, with no effect on activation or compressibility. This remains an independent vacuum normalization.

The unique constrained minimum is $y=0$, $W_{\min}=K$ for $K\leq K_*=m^2/(2a)$. Above threshold it obeys

\[
 K(y)=\frac{(m^2+\lambda y)(1+ay)^2}{2a},\qquad
 K_y=\frac{(1+ay)(D+3a\lambda y)}{2a}>0,
 \quad D=\lambda+2am^2.
\]

The scalar minima are the two signs of $\chi=\sqrt y$. Their curvature is positive at fixed $K$. The convexity in $y$, together with growth at infinity, establishes the constrained global minimum in this local scalar sector. For $\Delta K=K-K_*\downarrow0$,

\[
 y=\frac{2a}{D}\Delta K+O(\Delta K^2),\qquad
 W_{\min}=K-\frac{a^2}{D}(\Delta K)^2+O(\Delta K^3).
\]

The envelope theorem gives $W_K=(1+ay)^{-1}$. The function is continuously differentiable across activation, but its second derivative changes from zero to $-2a^2/D$.

## The ensemble required for a density pressure

At fixed $K$, elimination produces a constitutive function of canonical kinetic density. It does **not** by itself identify $K$ with a unique function of mass density or turn the trace-stress trigger into a density-only state variable. Different stream distributions can have the same density and different $K$.

For a concrete check, specify canonical affine compression $x\mapsto b x$, $p-\bar p\mapsto(p-\bar p)/b$. Then $\rho\mapsto\rho/b^3$, $K\mapsto K/b^5$, and along this family

\[
 K=k\rho^{5/3},\qquad
 P=\rho\frac{dW_{\min}}{d\rho}-W_{\min}
   =\frac53 K W_K-W_{\min}
   =\frac{2K}{3(1+ay)}-\frac{m^2y}{2}-\frac{\lambda y^2}{4}.
\]

Here $k$ is held fixed; scalar kinetic and gradient energy are neglected and the scalar is assumed to follow its local minimum. The first term is the isotropic conjugate kinetic pressure. Scalar potential pressure must also be included. Once $\chi\neq0$, neither bare canonical trace pressure $2K/3$ nor bare physical velocity dispersion alone equals this total pressure. Anisotropic states require tensor stress, and nonadiabatic evolution requires the full kinetic/field equations.

## Asymptotic obstruction to the logotropic EOS

At large $K$, the exact stationarity relation implies

\[
 y\sim\left(\frac{2K}{a\lambda}\right)^{1/3},\qquad
 W_{\min}\sim\frac34\lambda^{1/3}\left(\frac{2K}{a}\right)^{2/3}.
\]

Consequently, at fixed $k$,

\[
 W_{\min}\sim B\rho^{10/9},\qquad
 P\sim\frac{B}{9}\rho^{10/9},\qquad
 B=\frac34\lambda^{1/3}(2k/a)^{2/3}.
\]

This differs from $u_{\log}=-A[\ln(\rho/\rho_{\rm ref})+1]$, $P_{\log}=A\ln(\rho/\rho_{\rm ref})$. The high-density logarithmic pressure slope tends to $10/9$ here, whereas $d\ln P_{\log}/d\ln\rho$ tends to zero for positive large logotropic pressure. The inactive branch is also a power law: $P=2K/3\propto\rho^{5/3}$. No choice of positive finite $a,m^2,\lambda$ changes these asymptotic exponents.

## Reduced compressibility is an additional condition

On the active branch the pressure can be written exactly as

\[
 P(y)=\frac{m^2}{3a}+\left(\frac{\lambda}{3a}-\frac{m^2}{6}\right)y
             +\frac{\lambda y^2}{12},
\]
\[
 \frac{dP}{dK}
 =\frac{2\lambda-am^2+a\lambda y}
 {3(1+ay)(\lambda+2am^2+3a\lambda y)},\qquad
 \frac{dP}{d\rho}=\frac{5K}{3\rho}\frac{dP}{dK}.
\]

Therefore $\lambda\geq am^2/2$ ensures nonnegative reduced compressibility on this entire active branch. For $0<\lambda<am^2/2$, it is negative for

\[
 0<y<\frac{am^2-2\lambda}{a\lambda}.
\]

For $a=m^2=1,\lambda=0.1$, the interval is $0.5<K<72.9$, despite a stable scalar minimum throughout its interior. This is a static reduced-curvature warning within the specified family, not a complete dynamical mode-spectrum calculation. Scalar response becomes slow at activation; gradients, finite response, kinetic anisotropy, and gravity are absent from this elimination.

## Reproducible bounded check

`check_constitutive.py` uses exact SymPy identities, an independent scalar energy minimizer, finite volume derivatives, threshold checks, and large-$K$ checks. The run completed successfully in about 2 seconds under a 10-second wall limit, 8-second CPU limit, and one-thread limit. `run/manifest.json` passed the mathbox manifest validator. Sixteen finite parameter points cover $a=m^2=1$, $\lambda\in\{0.1,0.5,1,3\}$, $K\in\{0.25,1,10,100\}$.

- Maximum scaled pressure error: $2.18\times10^{-10}$.
- Maximum absolute compressibility-derivative error: $1.21\times10^{-11}$.
- Maximum scaled independent-minimizer discrepancy: $1.70\times10^{-8}$.
- At $K=10^{12}$, $a=m^2=\lambda=1$, $d\ln W/d\ln\rho=1.11111111344$ and $P/W=0.11111111344$, approaching $10/9$ and $1/9$.

The proof of the general exponents is algebraic; the final asymptotic numerical slice is an illustration, not a sweep over all parameters. No new literature claim is used. The source model is `../REPORT.md`, section 1, SHA256 `1b04ae408fe0d088cf101f17028ffd1d6ae0d980ad375e0cc9b5ca9274129110`.

Reproduction uses the mathbox bounded runner with `contract.json`, `check_constitutive.py` as its sole execution input, and a fresh output directory; pass the new results-file path as the script's optional first argument. Exact argv and execution hashes are in `run/manifest.json`.

Evidence SHA256:

- Script: `5932afb2e64a725b5e684faa8b3cdba9c7fb9abee9b92edcfc03ec3ef4499998`.
- Results: `bd1246d901bcca88cc665cd950801510244016578744fae79c3c21debfd6c9b9`.
- Manifest: `a44d73ccd99fe4ca86b01da3cf4973cb34f6e328e93117c3b0d2933a824fb982`.

No phase formation, cold-field-to-kinetic derivation, Lambda coefficient, or halo stopping mechanism is established by this continuation.
