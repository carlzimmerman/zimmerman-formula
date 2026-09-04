# HPI-Delta weak-static, orbit, and lensing predictions — 2026-09-03

## Verdict

**Bounded weak-static gate: PASS. Candidate status: OPEN.**

The symbolic audit starts from the HPI-Delta ADM action's frozen weak-static
reduction. It independently varies `Phi` and `Psi`, relates the `Psi` equation
to preservation of the trace-momentum constraint, and then derives the AQUAL,
spherical, orbit, epicycle, and lensing consequences. It does not establish a
full nonlinear functional Dirac theorem, a covariant clock completion, full
PPN parameters, global stability, or novelty. The full ADM-to-weak expansion
is not repeated here; that reduction remains an explicit assumption of this
bounded prediction audit.

The Laplacian trace-momentum mechanism is prior MMG machinery; see
Yao--Oliosi--Gao--Mukohyama, arXiv:2011.00805, and
Sangtawee--De Felice--Karwan, arXiv:2607.26031.

## One action and normalization

The input first-order action is

\[
S=\int dt\,d^3x\left[
 \pi^{ij}\dot h_{ij}+p_\psi\dot\psi
 -N({\cal H}_{\rm GR}+{\cal H}_{\exp}+{\cal H}_m)
 -N^i({\cal H}^{\rm GR}_i+{\cal H}^m_i)
 -\sqrt h\,\lambda_\pi D^2\!\left({\pi\over\sqrt h}\right)
 \right],
\]

with

\[
{\cal H}_{\exp}={M_{\rm Pl}^2\over\ell_0^2}\sqrt h\,F_{\exp}(y),
\quad
F_{\exp}(y)=2[(1+y)e^{-y}-1],
\quad
y=\ell_0|D\ln N|,
\quad \ell_0={c^2\over a_0}.
\]

On the attractive radial branch `g=Phi'(r)>0`, using `c=1` for action
normalization, the reduced weak-static density divided by `M_Pl^2` is

\[
{\cal L}_{\rm ws}=-2\nabla\Phi\!\cdot\!\nabla\Psi
 +|\nabla\Psi|^2-a_0^2F_{\exp}(|\nabla\Phi|/a_0)
 -8\pi G\rho_b\Phi.
\]

Conditional on standard minimally coupled nonrelativistic dust, whose leading
term is `-rho_b Phi`, the source coefficient is not simply named `G`: the
script checks `M_Pl^2=(8 pi G)^-1`, so division by `M_Pl^2` gives exactly
`-8 pi G rho_b Phi`. In the high-acceleration limit the derived equation is
`Laplacian(Phi)=4 pi G rho_b`; this identifies `G` as the measured weak-field
Newton constant under those conventions. The script does not vary an explicit
dust action or independently repeat the full ADM-to-reduced normalization.

The action primitive is

\[
{\cal G}(y)=y^2+F_{\exp}(y)
=y^2+2(1+y)e^{-y}-2,
\qquad {\mathcal G'(y)\over2y}=1-e^{-y}\equiv\mu(y).
\]

## Independent potential equations and preservation

Direct Euler--Lagrange variation gives

\[
E_\Phi=2\nabla^2\Psi
-2\nabla\!\cdot(e^{-y}\nabla\Phi)-8\pi G\rho_b=0,
\]

\[
E_\Psi=2\nabla^2(\Phi-\Psi)=0.
\]

The three-component Cartesian fluxes and the spherical-measure equations are
both differentiated by SymPy. `Phi=Psi` is not substituted before variation.

Independently, the finite-`k` scalar Legendre transform gives

\[
C_\pi=-k^2p_\Psi,
\qquad
\dot C_\pi=2A k^4(\Phi-\Psi)=-A k^2E_\Psi.
\]

Thus preservation gives `Phi=Psi` for `k != 0`. The calculation also evaluates
`k=0` separately: the preservation equation then vanishes identically, so this
local result is not promoted to a homogeneous theorem. On the regular isolated
spherical branch the integration constant in
`r^2(Phi'-Psi')=constant` is zero.

Substitution into `E_Phi` yields exactly

\[
{1\over r^2}{d\over dr}\left[r^2
 \left(1-e^{-\Phi'/a_0}\right)\Phi'\right]
=4\pi G\rho_b.
\]

## Spherical, circular, and epicyclic predictions

Defining `M_b'(r)=4 pi r^2 rho_b`, the script verifies the exact identity

\[
{E_\Phi\over2}\bigg|_{\Phi=\Psi,\,\rho_b=M_b'/(4\pi r^2)}
= {d\over dr}\left[r^2\mu(g/a_0)g-GM_b(r)\right].
\]

Regular-origin and isolated-source boundary conditions set the integration
constant to zero. For an exterior constant mass,

\[
\boxed{\left(1-e^{-g/a_0}\right)g={GM_b\over r^2}}.
\]

It gives `g -> GM_b/r^2` at high acceleration and

\[
g={\sqrt{GM_ba_0}\over r},\qquad v_\infty^4=GM_ba_0
\]

in deep MOND. Circular kinematics `g=4 pi^2 r/T^2` gives the exact generalized
Kepler law

\[
\boxed{
{4\pi^2r^3\over T^2}
\left[1-\exp\!\left(-{4\pi^2r\over a_0T^2}\right)\right]=GM_b(r)}.
\]

Here “deep MOND” is the one-sided asymptotic `g -> 0+` along the nonzero-field
branch. It is not a certification of the exact `y=0` endpoint. The core
HPI-Delta quadratic gate has a constraint-rank bifurcation there and does not
exclude strong coupling. More specifically, on its exact-`y=0` finite-`k`
quadratic background, retaining the linear source makes the lapse constraint
force `J_rho=0`. This is a rank/strong-coupling warning, not a general claim
that a point with `g=0` cannot have finite nonlinear AQUAL flux divergence.
Thus the BTFR limit is controlled as an asymptotic formula, while
exact-zero-field nonlinear closure remains open.

The code next differentiates the exact mass flux rather than assigning an
orbit slope. With

\[
L(y)={d\ln\mu\over d\ln g}={y\over e^y-1},
\qquad m={d\ln M_b\over d\ln r},
\]

it obtains

\[
{d\ln g\over d\ln r}={m-2\over1+L},
\qquad
{\kappa_{\rm ep}^2\over\Omega^2}={1+3L+m\over1+L}.
\]

For an exterior orbit (`m=0`),

\[
{d\ln v\over d\ln r}={L-1\over2(1+L)}
={1+y-e^y\over2(e^y-1+y)},
\]

and the apsidal shift per radial period is

\[
\boxed{\Delta\varpi=2\pi\left[
\sqrt{{1+L\over1+3L}}-1\right]}.
\]

Its Newtonian limit is zero. Its formal deep-MOND limit is retrograde,
`2 pi (1/sqrt(2)-1)`, while `kappa_ep^2/Omega^2 -> 2` and the rotation-curve
slope tends to zero.

## Lensing

For

\[
ds^2=-(1+2\Phi/c^2)c^2dt^2+(1-2\Psi/c^2)d\mathbf x^2,
\]

and assuming minimally coupled photons/test particles follow this same metric,
the leading null-geodesic deflection is

\[
\alpha(b)={1\over c^2}\int_{-\infty}^{\infty}
\partial_b(\Phi+\Psi)\,dz
={2b\over c^2}\int_{-\infty}^{\infty}
{g(\sqrt{b^2+z^2})\over\sqrt{b^2+z^2}}\,dz.
\]

The Newtonian limit evaluates to `4 G M_b/(b c^2)`. In the formal deep-MOND
exterior, `g=sqrt(G M_b a_0)/r`, and SymPy evaluates

\[
\boxed{\alpha_{\rm deep}={2\pi\sqrt{GM_ba_0}\over c^2}}.
\]

This is exactly twice the deflection of a one-potential metric retaining only
`Phi`. Relative to the baryon-only Newtonian result it is
`(pi/2) b/r_M`, with `r_M=sqrt(G M_b/a_0)`.

The isolated `1/r` acceleration is scale-free, so its constant deflection is a
formal exterior limit. A finite physical system, cosmological embedding, or
external field must supply a large-distance cutoff. This script does not
derive that cutoff.

## Live negative controls

The audit recomputes four mutations:

- removing `F_exp` produces `mu=1`, not the exponential law;
- changing the EH `|grad(Psi)|^2` coefficient from 1 to 2 produces
  `Psi/Phi=1/2` and shifts the MOND modulus by `-1/2`;
- dropping `Psi` from the null-geodesic integral halves the deep deflection;
- ignoring `d ln mu/d ln g` changes the deep epicyclic ratio from 2 to 1 and
  erases the retrograde apsidal shift.

## Reproduction

```bash
python3 qwen_claude_field_theory/closure_2026/hpi_delta_predictions_2026/test_hpi_delta_predictions_2026.py
python3 qwen_claude_field_theory/closure_2026/hpi_delta_predictions_2026/hpi_delta_predictions_2026.py
```

At the recorded run both commands exited 0: 12 unit tests passed and all 14
CLI checks passed.
