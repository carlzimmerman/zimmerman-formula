# Exact exponential MOND: central Kepler law and regular-center obstruction

Status: **proved under the assumptions stated below; no global literature-novelty claim**.

## 1. Claim and scope

Consider the exact quasistatic equation

\[
\nabla\!\cdot\!\left[\left(1-e^{-\lvert\nabla\Phi\rvert/a_0}\right)\nabla\Phi\right]
=4\pi G\rho.
\]

The executable calculation proves two linked results.

1. A new repository-level central-orbit law follows for a smooth spherical core.
2. If the physical no-slip metric is required to be classical and at least \(C^2\), the same exact law is singular at any force-free point with positive density.

The obstruction assumes that the exact equation applies inside smooth matter. It does not prove that finite-action weak solutions are absent; in fact, the script constructs one. A nonzero external field makes the geometric center non-force-free and breaks the isolated spherical-center expansion, but it does not necessarily eliminate every critical point; the existence and regularity of displaced critical points are not analyzed here. Taking \(\rho(0)=0\), accepting a non-\(C^2\) weak metric, or modifying the law at \(y=0\) evades the corresponding stated assumption.

## 2. Constitutive-rank theorem

Let

\[
A_i(p)=\mu(\lvert p\rvert/a_0)p_i,
\qquad \mu(y)=1-e^{-y}.
\]

For \(p\neq0\), the Jacobian has transverse and longitudinal eigenvalues

\[
\lambda_\perp=1-e^{-y},\qquad
\lambda_\parallel=1+(y-1)e^{-y}.
\]

Both tend to zero as \(y\to0^+\), and the computed continuous extension is

\[
DA(0)=0,\qquad \operatorname{rank}DA(0)=0.
\]

If \(\Phi\in C^2\) and \(\nabla\Phi(x_0)=0\), then

\[
\nabla\!\cdot A(\nabla\Phi)(x_0)
=DA(0):D^2\Phi(x_0)=0.
\]

The exact field equation therefore forces \(\rho(x_0)=0\). A classical \(C^2\) potential, a force-free point, and positive density cannot coexist. The same conclusion holds if the equation is initially imposed almost everywhere, because the left side is continuous for \(C^2\) \(\Phi\) and continuous \(\rho\).

## 3. Smooth spherical core

For

\[
\rho(r)=\rho_0+O(r^2),\qquad C=\frac{4\pi G\rho_0}{3},
\]

the integrated field equation is

\[
\mu(g/a_0)g=Cr+O(r^3),\qquad g=\Phi'(r)>0.
\]

Put \(t=\sqrt{Cr/a_0}\) and \(u=g/a_0\). Exact rational-arithmetic series reversion gives

\[
u=t+\frac14t^2+\frac7{96}t^3+\frac1{48}t^4
+\left(\frac q2+\frac{491}{92160}\right)t^5+O(t^6),
\]

where \(q\) first records the \(O(r^2)\) density-profile correction. Thus the first four displayed coefficients are universal for smooth cores. In particular,

\[
g(r)=\sqrt{a_0Cr}+\frac C4r+O(r^{3/2}),
\]

\[
\Phi(r)-\Phi(0)=\frac23\sqrt{a_0C}\,r^{3/2}
+\frac C8r^2+O(r^{5/2}).
\]

The positive inverse branch is unique: for \(f(u)=u(1-e^{-u})\),

\[
e^u f'(u)=e^u+u-1,
\qquad \frac{d}{du}(e^u+u-1)=e^u+1>0,
\]

and \(f(0)=0\), \(f(u)\to\infty\).

## 4. Central Kepler-grade law

For a circular orbit, \(v_c^2=rg\) and \(T=2\pi r/v_c\). The leading core laws are

\[
\boxed{\lim_{r\to0}\frac{v_c^4}{\rho_0r^3}
=\frac{4\pi}{3}Ga_0},
\]

\[
\boxed{\lim_{r\to0}\frac{T^4}{r}
=\frac{12\pi^3}{Ga_0\rho_0}}.
\]

This is the central-core counterpart of the exterior baryonic Tully–Fisher law. It predicts \(v_c\propto r^{3/4}\) and \(T\propto r^{1/4}\). A Newtonian uniform-density core instead has \(v_c\propto r\) and a radius-independent period.

The exact exponential interpolation fixes the first corrections:

\[
\frac{v_c^4}{a_0Cr^3}
=1+\frac12t+\frac5{24}t^2+\frac5{64}t^3+O(t^4),
\]

\[
\frac{T^4/r}{16\pi^4/(a_0C)}
=1-\frac12t+\frac1{24}t^2+\frac1{192}t^3+O(t^4).
\]

An independent 80-decimal-digit root solve of \(u(1-e^{-u})=t^2\) checks the fifth-order acceleration series:

| \(t\) | exact \(u\) | series \(u\) | relative error |
|---:|---:|---:|---:|
| 0.1 | 0.10257505432236393 | 0.10257505327690972 | \(1.02\times10^{-8}\) |
| 0.03 | 0.030226985755223246 | 0.03022698575446289 | \(2.52\times10^{-11}\) |
| 0.01 | 0.010025073125533811 | 0.010025073125532769 | \(1.04\times10^{-13}\) |
| 0.003 | 0.0030022519704387953 | 0.0030022519704387945 | \(2.53\times10^{-16}\) |

These are equation-level checks, not a fit to astronomical data. Applying the law observationally requires a genuinely spherical, isolated, deep-MOND core and a separately measured \(\rho_0\).

## 5. Curvature and phantom-density consequences

The Hessian eigenvalues are

\[
\Phi''\sim\frac{\sqrt{a_0C}}{2\sqrt r},\qquad
\frac{\Phi'}r\sim\frac{\sqrt{a_0C}}{\sqrt r},
\]

so

\[
\lVert D^2\Phi\rVert_F^2\sim\frac94\frac{a_0C}{r},
\qquad
\nabla^2\Phi\sim\frac52\frac{\sqrt{a_0C}}{\sqrt r}.
\]

For the no-slip weak metric,

\[
ds^2=-(1+2\Phi/c^2)c^2dt^2
+(1-2\Phi/c^2)\delta_{ij}dx^idx^j,
\]

the linear Ricci scalar is

\[
R^{(1)}=\frac{2\nabla^2\Phi}{c^2}
\sim\frac{5\sqrt{a_0C}}{c^2\sqrt r}.
\]

The executable also derives the full Ricci scalar of the displayed isotropic metric directly from its Christoffel symbols, with the locally irrelevant constant set by \(\Phi(0)=0\). It finds

\[
\lim_{r\to0}\frac{\sqrt r\,c^2R}{\sqrt{a_0C}}=5,
\qquad
\lim_{r\to0}\frac{R}{R^{(1)}}=1.
\]

Thus the nonlinear terms of this displayed weak-metric ansatz do not cancel the invariant divergence.

If ordinary Einstein curvature equations are retained and MOND is represented as an effective or phantom density, then

\[
\rho_{\rm ph}(r)
\sim\frac{5\sqrt{a_0C}}{8\pi G\sqrt r}-\rho_0.
\]

The cusp is integrable—\(M_{\rm eff}\sim\sqrt{a_0C}\,r^{5/2}/G\)—but the effective stress and physical curvature are not regular. This directly obstructs the proposed Einstein-plus-elliptic-phantom architecture at a smooth positive-density center.

The action density remains locally integrable. Since the exact primitive obeys \({\cal G}(y)\sim\tfrac23y^3\) and \(y\sim r^{1/2}\), the radial action integrand scales as \(r^{7/2}\). The result is therefore a regularity/curvature no-go, not nonlinear nonexistence.

## 6. A mutation that isolates the cause

For

\[
\mu_\epsilon(y)=\epsilon+1-e^{-y},\qquad \epsilon>0,
\]

the origin Jacobian is \(\epsilon I\), the central solution is \(g\sim Cr/\epsilon\), and the Hessian is finite. This removes the singularity only by changing \(\mu(0)=0\), so it fails the exact target.

More generally, \(\mu(y)\sim c y^s\) with \(s>0\) gives

\[
g\sim r^{1/(s+1)},\qquad D^2\Phi\sim r^{-s/(s+1)}.
\]

The obstruction is tied to any constitutive law whose ellipticity vanishes as a positive power at zero field.

## 7. RAR/AQUAL translation correction

The fitted algebraic relation

\[
\nu_{\rm RAR}(y_N)=\left(1-e^{-\sqrt{y_N}}\right)^{-1}
\]

is not the exact spherical inverse of \(\mu_{\exp}(x)=1-e^{-x}\). The exact inverse satisfies

\[
\nu_{\rm AQUAL}(y_N)
\left[1-e^{-\nu_{\rm AQUAL}(y_N)y_N}\right]=1.
\]

At \(y_N=1\), the executable audit finds

\[
\nu_{\rm RAR}=1.5819767068693265,
\qquad
\nu_{\rm AQUAL}=1.3499764854011254,
\]

and substituting \(\nu_{\rm RAR}\) into the exact inverse equation leaves residual \(0.2567723687288992\). They share limiting behavior but are not the same finite-acceleration law.

## 8. Literature-search boundary

The leading central scaling is **not globally novel**. It follows immediately from the standard deep-MOND relation reviewed by [Milgrom (2002)](https://arxiv.org/abs/astro-ph/0207231). Hernández, *Central MONDian spike in spherically symmetric systems* ([2017 preprint](https://arxiv.org/abs/1701.03473), [published version](https://doi.org/10.1093/mnras/stx1003)), explicitly inserted the constant-density mass law and developed both the central MONDian region and its Newtonian-inferred extra mass. Related later work includes equivalent-Newtonian-system and MOND core/cusp studies by [Re & Di Cintio (2023)](https://arxiv.org/abs/2307.08865) and [Eriksen, Frandsen & From (2019)](https://arxiv.org/abs/1906.07823).

The narrow primary-source search did not locate the exact exponential correction coefficients in §4, the rank-zero \(C^2\) theorem, or the invariant Ricci coefficient in §5. That failed search is not proof of novelty. Accordingly this report claims only that those sharpenings are new to this repository; a comprehensive novelty claim requires a dedicated literature review.

## 9. Reproduction

From this directory:

```bash
python3 -m unittest -v test_exact_mond_regular_center_no_go_2026.py
python3 exact_mond_regular_center_no_go_2026.py
```

The program uses exact SymPy arithmetic for the load-bearing identities and 80-digit `mpmath` roots only as an independent numerical check. No randomness is used.
