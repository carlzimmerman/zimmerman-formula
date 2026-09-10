# Pressure, isotropic potentials, and lensing in the ticking KGB branch

2026-09-10. Repository base: `de6b2c1a948c043a3a3c7130f88051db66c6bc46`.
This is a bounded metric diagnostic. The full shared, healthy gravity action
remains open. The clock is an explicit physical field; no dark matter particles
are added. No empirical tolerance, measured Newton constant, PPN coefficient,
or novelty claim is supplied.

The main result, for the static weak-field exterior and conventions below, is

\[
 \Phi'=g,\qquad \Psi'=g-\frac{rP}{2m},\qquad
 \Phi_W':=\frac{\Phi'+\Psi'}2=g-\frac{rP}{4m}.
\]

These are first-order relations, with areal and isotropic radii identified only
to that order. A large value of \(P/\rho\), or a negative local clock density,
does not by itself specify the size of the pressure-induced lensing change.
It can still reject a separately imposed positive-density requirement.

## Assumptions and inherited action identities

The same action and physical matter metric are retained:

\[
 S=\int d^4x\sqrt{-g}\left[\frac{mR}{2}+P(X)-G(X)\Box\phi\right]+S_m[g],
 \quad X=-\tfrac12(\nabla\phi)^2,\quad m=(8\pi G_b)^{-1}>0.
\]

Units are \(c=1\), the signature is \((-+++)\), and
\(\phi=qt+\psi(r)\), \(q\ne0\), \(p=\psi'\), \(X>0\).
The raw action variation in `ticking_kgb_inverse_2026/kgb_inverse.py` gives,
on the zero-current branch,

\[
 J^r=0,\quad T^r{}_t=qJ^r=0,\quad p_r=P,\quad
 \rho=\frac{2X\,G_X\,X'}p-P,\quad
 p_t=P+\beta(\rho+P),\quad \beta=\frac{p^2}{2BX}>0.
\]

These action identities are inherited raw inputs, not a fresh covariant
variation. The Einstein tensor and coordinate transform are recomputed here.
The exterior has no baryonic radial pressure; otherwise replace \(P\) by total
radial pressure in the metric relation. Photon propagation follows the minimally
coupled physical metric.

On a smooth finite interval let

\[
 ds^2=-A(r)dt^2+B(r)dr^2+r^2d\Omega^2,\quad
 A,B>0,\quad g=\frac{A'}{2A},\quad
 B=\frac{1+2rg}{1+r^2P/m}.
\]

The last identity follows from the radial Einstein equation and is also checked
against an independently constructed Einstein tensor. Ratios below require
\(g\ne0\). The linear expansion assumes small metric potentials,
\(|rg|\ll1\), \(|r^2P/m|\ll1\), and smooth radial derivative power counting.
Small \(rg\) alone does not control an arbitrarily large integrated logarithmic
potential. No asymptotically flat completion of an infinite MOND logarithmic
halo is assumed.

## Independent isotropic-coordinate derivation

Define isotropic radius \(R\) and first-order potentials by

\[
 ds^2=-(1+2\Phi(R))dt^2
       +(1-2\Psi(R))(dR^2+R^2d\Omega^2)+O(\varepsilon^2).
\]

The angular metric gives \(r=R(1-\Psi)\). Setting \(B=1+b\), its radial part
then gives

\[
 B\left(\frac{dr}{dR}\right)^2
 =1+b-2\Psi-2R\Psi'=1-2\Psi,
 \quad b=2R\Psi'.
\]

Independently, the lapse gives \(g=\Phi'+O(\varepsilon^2/r)\).
Expanding the exact radial Einstein solution gives
\(b=2rg-r^2P/m\), proving the result at the top of this report.
With a common outer reference radius \(R_o\), one may write

\[
 \Phi(R)=\Phi(R_o)-\int_R^{R_o}g(s)\,ds,
 \quad
 \Psi(R)=\Psi(R_o)-\int_R^{R_o}
       \left[g(s)-\frac{sP(s)}{2m}\right]ds.
\]

The constants require boundary matching; a local slope identity does not fix
the ratio of the potentials. At this order, equality of the potential slopes
through an interval requires \(P=0\) at that order. It does not require the
exact nonlinear pressure to vanish at every higher order.

There is also an exact coordinate control. Define logarithmic metric potentials
by \(A=e^{2\Phi_{\log}}\) and \(r=Re^{-\Psi_{\log}}\). On the positive
\(dr/dR\) branch,

\[
 \frac{d\Phi_{\log}}{dR}=\frac{gr}{R\sqrt B},\quad
 \frac{d\Psi_{\log}}{dR}=\frac{1-B^{-1/2}}R,\quad
 \eta_{\log}:=\frac{d\Psi_{\log}/dR}{d\Phi_{\log}/dR}
 =\frac{\sqrt B-1}{rg}.
\]

This finite-radius ratio is not \(\gamma_{\rm PPN}\). At fixed areal radius
and lapse, put \(T=1+2rg\), \(h=r^2P/m\); then the exact pressure contribution
to that ratio is

\[
 \eta_{\log}(P)-\eta_{\log}(0)
 =-\frac{\sqrt T\,h}{rg\sqrt{1+h}\,(1+\sqrt{1+h})}.
\]

This rationalized form avoids subtracting nearly equal square roots. It also
separates pressure effects from the nonlinear corrections already present at
\(P=0\). A first-order pressure signal below those corrections must not be
presented as a precision prediction of the full observed slip.

## What photons measure

The null condition gives the first-order optical index
\(dt/d\ell=1-\Phi-\Psi\). Varying that path length gives the transverse
ray acceleration \(-\nabla_\perp(\Phi+\Psi)\). For a Born ray with impact
parameter \(b_{\rm imp}>0\), \(r^2=b_{\rm imp}^2+z^2\), the signed inward
deflection is therefore

\[
 \alpha=b_{\rm imp}\int_{\rm ray}
       \left[\frac{2g(r)}r-\frac{P(r)}{2m}\right]dz,
 \qquad
 \Delta\alpha_P=-\frac{b_{\rm imp}}{2m}\int_{\rm ray}P(r)\,dz.
\]

These expressions assume the usual weak static ray geometry and a specified
complete path or matched finite segment. A profile known only on a finite
radial interval determines only that part of the integral. Positive pressure
suppresses this contribution at fixed temporal force; negative pressure
enhances it. A pointwise useful diagnostic is

\[
 D_P(r):=\frac{rP}{4mg},\qquad
 \frac{\Phi_W'}g=1-D_P,\qquad
 \frac{\Psi'}{\Phi'}=1-2D_P.
\]

For \(g>0\) along the complete relevant ray, a uniform bound \(|D_P|\le d\)
bounds the fractional pressure correction to its baseline deflection by \(d\).
The bound must cover all relevant segments; a single local value cannot do so.
No numerical observational tolerance has been chosen here.

For bookkeeping with bare \(G_b\), define slope masses
\(M_{\rm dyn}=r^2g/G_b\), \(M_{\rm space}=r^2\Psi'/G_b\), and
\(M_W=r^2\Phi_W'/G_b\). Then

\[
 M_{\rm space}=M_{\rm dyn}-4\pi r^3P,\qquad
 M_W=M_{\rm dyn}-2\pi r^3P.
\]

These are spherical slope quantities, not independently fitted particle masses.
Measured Newton \(G\) has not been identified with \(G_b\).

## Why density ratios do not decide the metric test

The separately computed temporal Einstein equation gives, to first order,

\[
 \rho=2m\left(g'+\frac{2g}{r}\right)-3P-rP',\qquad
 \rho_{\rm dyn}:=2m\left(g'+\frac{2g}{r}\right).
\]

The Weyl-potential Laplacian is

\[
 2m\nabla^2\Phi_W
 =\rho_{\rm dyn}-\frac{3P+rP'}2
 =\frac{\rho_{\rm dyn}+\rho}2.
\]

Consequently pressure gradients and density sign still matter for the spatial
profile, projected convergence, and boundary matching. They must be tested in
the complete solution. They are not interchangeable with the local slope ratio.
The force curvature scale relevant for that ratio is
\(\rho_{\rm curv}=2mg/r\), for which \(D_P=P/(2\rho_{\rm curv})\).
The residual density can be tiny because \(g'+2g/r\) cancels in a nearly
Newtonian exterior.

For the exact target parametrization in the raw inputs,
\(\mu=1-e^{-y}\), \(\lambda=\mu+ye^{-y}\),
\(r=\epsilon/\sqrt{y\mu}\), \(g=y/(1-2ry)\), \(m=a_0=1\), the
zero-pressure density is \(\rho_0=4y^2e^{-y}/(r\lambda)\). Thus

\[
 \frac{\rho_0}{\rho_{\rm curv}}
 =\frac{2ye^{-y}(1-2ry)}{\lambda}.
\]

At \(y=20\), \(\epsilon=10^{-6}\), this ratio is
\(8.2445404\times10^{-8}\). Two exact-input local controls give:

| Constant local pressure choice | \(P/\rho\) | \(D_P\) | Density sign |
| --- | ---: | ---: | --- |
| Tune \(\rho=10^{-6}\rho_0\) | 333334.99 | \(1.37410\times10^{-8}\) | positive |
| \(P=10^{-6}\rho_{\rm curv}\) | -0.342755 | \(5.0\times10^{-7}\) | negative |

The full local metric uses \(B=T/(1+r^2P)\), not a zero-pressure \(B\).
The exact pressure changes to \(\eta_{\log}\) are respectively
\(-2.7482061\times10^{-8}\) and \(-1.0000045\times10^{-6}\).
These probes are geometric controls, not healthy global action solutions.

There is an additional exact local clock control within the same KGB inverse.
Take \(A=1-2M/r\), constant \(P>0\),
\(B=[A(1+r^2P/m)]^{-1}\), and \(r>2M\). Then

\[
 \rho=P\left(-3+\frac{4M}{r}\right)<0,\quad
 p_t=P\left(1-\frac Mr\right),\quad
 \beta=\frac{rg}{2}>0,\quad
 X=\frac{q^2r}{2r-3M},\quad X'=-\frac{3Mq^2}{(2r-3M)^2}\ne0.
\]

Choose \(p^2=2BX\beta\), \(P(X)=P\), and locally
\(G_X=p(\rho+P)/(2XX')\). The scalar current and all three stress components
agree with the independently computed Einstein tensor. Monotone \(X\) makes
this a local single-profile function \(G(X)\). The pressure-induced metric
change tends to zero as \(P\to0^+\), while density remains negative for every
positive \(P\). No health, universality across masses, or global matching is
claimed. It is a counterexample only to the proposed implication from negative
local density to necessarily large pressure-induced lensing slip.

The earlier large ratios or negative densities therefore do not automatically
falsify the temporal-force/lensing target or the whole action class. They can
falsify the particular trajectory under a positive-density gate, and complete
ray and source-profile checks can impose further restrictions. A constrained
joint inverse should use the derived \(D_P\), ray integral, and density equations
together with its separately derived clock-health conditions.

## Reproduction and limits

`lensing.py` constructs the Einstein tensor, performs the coordinate and optical
index expansions, and builds exact controls. `test_lensing.py` runs nine checks,
including the point-mass \(4M/b_{\rm imp}\) result and an independently integrated
finite flat-force ray with nonzero pressure. No solver scan or external source
lookup is performed. The raw action files are pinned as inputs and left intact.

The bounded run is `run_001/manifest.json`; its output `run_001/results.json`
contains the exact expressions, zero residuals, numerical controls, and test
counts. Python 3.9.6 and SymPy 1.14.0 were used. Re-run the checks from the
repository root with:

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/lensing/test_lensing.py
```

The manifest records the full bounded-run argument vector, source hashes,
result hash, exit status, dirty worktree state, and effective limits. Only new
files in this `lensing/` directory were authored by this task. Existing dirty
files were preserved; no commit or push was made.

Computation-audit was used for the exact algebra, controls, and provenance.
Proofread-math self-review covered this new report and its equation conventions.
There are no external mathematical theorem dependencies or literature claims.
