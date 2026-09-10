# General derivative-conformal Einstein-frame dictionary

2026-09-10. Implementation and finite controls verified in the stated range.
The general formulas are exact chain/connection identities on their regular
chart; the numerical health checks are local controls, not a solved non-affine
gravity model. No dark matter particles are introduced; the scalar clock is
explicit.

## Conventions and action derivatives

Take the physical action

\[
 \sqrt{-g}\left[F(X)R+\frac{3F_X^2}{2F}(\nabla X)^2
                  +P(X)-G(X)\Box\phi\right]+\mathcal L_m[g],
 \qquad X=-\tfrac12(\nabla\phi)^2.
\]

The constant EF Ricci coefficient is \(m/2\). Set
\(\widetilde g_{\mu\nu}=C(X)g_{\mu\nu}\), \(C=2F/m\);
the parent inverse uses \(m=1\), hence \(C=2F\). Write

\[
 C_1=C_X,\quad C_2=C_{XX},\quad
 \Delta=C-XC_1,\quad \chi=X/C,\quad
 \frac{d\chi}{dX}=\frac{\Delta}{C^2},\quad
 \frac d{d\chi}=\frac{C^2}{\Delta}\frac d{dX}.
\]

The field-map conditions are \(C>0\), \(\Delta\ne0\), equivalently
\(F>0\), \(F-XF_X\ne0\). The sign of \(\Delta\) is not restricted.
This Jacobian must not be confused with the radial-coordinate Jacobian below.

The transformed action is EF KGB in vacuum, with

\[
 \widetilde P=\frac P{C^2},\qquad
 \widetilde P_\chi=\frac{P_X-2C_1P/C}{\Delta},
\]
\[
 \boxed{\widetilde P_{\chi\chi}
 =\frac{C^2\Delta P_{XX}
        +C(CXC_2-2C_1\Delta)P_X
        +2(C_1^2\Delta-C^2C_2)P}{\Delta^3}},
\]
\[
 \widetilde G_\chi=\frac{CG_X}{\Delta},\qquad
 \boxed{\widetilde G_{\chi\chi}
 =\frac{C^2[(CG_{XX}+C_1G_X)\Delta+CXC_2G_X]}{\Delta^3}}.
\]

The cubic transformation includes integration by parts. Its two terms before
combining are \(-G\widetilde\Box\phi/C\) and
\((G/C)\widetilde\nabla\log C\cdot\widetilde\nabla\phi\).
After integration by parts their gradient coefficient is
\(d(G/C)/d\chi+(G/C)d\log C/d\chi=CG_X/\Delta\).
Thus \(\widetilde G\) is not obtained merely by setting it equal to \(G/C\).

Independent SymPy differentiation uses arbitrary functions \(C(X),P(X),G(X)\)
and verifies the displayed action jets. Setting \(C=1+\sigma X\),
\(C_1=\sigma\), \(C_2=0\), \(\Delta=1\) recovers all affine formulas.

## Physical and EF static jets

Use \(ds^2=-A\,dt^2+B\,dr^2+r^2d\Omega^2\),
\(\phi=qt+\psi(r)\), \(p=\psi'\),
\(g=A'/(2A)\), and \(b=B'/B\). Primes here mean physical \(r\)
derivatives. Put

\[
 h=\frac{C_1X'}C,\quad D=1+\frac{rh}{2},\quad R=\sqrt C\,r.
\]

On the chosen \(D>0\) orientation chart,

\[
 \widetilde A=CA,\quad \widetilde B=B/D^2,\quad
 \widetilde g=\frac{g+h/2}{\sqrt C D},\quad
 \widetilde p=\frac p{\sqrt C D},\quad
 \partial_R=\frac1{\sqrt C D}\partial_r.
\]

If coordinate derivatives are needed separately, use

\[
 h'=\left(\frac{C_2}C-\frac{C_1^2}{C^2}\right)(X')^2
       +\frac{C_1}C X'',\qquad D'=h/2+rh'/2,
\]
\[
 \widetilde p_R=\frac{p'-p(h/2+D'/D)}{CD^2},\qquad
 \frac{\widetilde B_R}{\widetilde B}
 =\frac{b-2D'/D}{\sqrt C D}.
\]

All \(D'\), hence \(X''\) and \(C_2\), cancel from the scalar Hessian
in an EF orthonormal frame:

\[
 v_a=\left(\frac q{\sqrt{CA}},\frac p{\sqrt{CB}},0,0\right),
\]
\[
 H_{00}=-\frac{(g+h/2)p}{CB},\quad
 H_{01}=-\frac{q(g+h/2)}{C\sqrt{AB}},\quad
 H_{11}=\frac{p'-(b+h)p/2}{CB},\quad
 H_{22}=H_{33}=\frac{pD}{CBr}.
\]

These entries independently agree with the general conformal-connection
identity. The helper reports the consistency residuals for
\(2X=q^2/A-p^2/B\) and
\(X'=-q^2g/A-pp'/B+p^2b/(2B)\), rather than assuming unrelated supplied
jets obey those identities.

## Complete direct F-jet dependence and the conditional inverse variation

For fixed physical action jets \((P,P_X,P_{XX},G_X,G_{XX})\) and fixed
physical background jets \((r,A,B,g,b,p,p',q,X,X')\):

| EF object | Direct conformal-function jets |
|---|---|
| Metric, scalar gradient and orthonormal Hessian | \(C,C_1\) |
| \(\widetilde P,\widetilde P_\chi,\widetilde G_\chi\), EF stress | At most \(C,C_1\) |
| \(\widetilde P_{\chi\chi},\widetilde G_{\chi\chi}\), coupled reduced scalar principal | At most \(C,C_1,C_2\) |

Therefore **no \(F_{XXX}\) enters this direct EF principal at fixed physical
jets**. This is structural, not an inference from a small scan. A numeric
control changes the third derivative by replacing
\(C=1+X/10+X^2/50\) with \(C+7(X-3/2)^3\) at \(X=3/2\), while
holding the other jets fixed; the matrices are identical. Changing \(C_2\)
at the same fixed physical jets produces a nonzero principal change, so its
second-derivative dependence is genuine in general.

This conclusion does **not** remove indirect dependence: differentiating an
inverse solution's \(P_X,G_X\) can produce \(F_{XXX}\) in its actual
\(P_{XX},G_{XX}\). Those must be derived from the same trajectory, not assigned
freely. This is a general possibility, not a claim that it occurs in the
current static inverse. If that inverse's exact coefficient functions are
independent of \(j=F_{XX}\), as the separate variation calculation reports,
their total derivatives have no \(F_{XXX}\) channel through \(j\); that
particular indirect dependence is absent too. Nor is the present EF calculation a derivation of the unreduced
higher-order physical-frame principal or its full constraint algebra.

A conditional exact check also implements the separate inverse derivation's
premise, for \(m=1\), \(f=F_X=C_1/2\ne0\), \(j=F_{XX}\):

\[
 \partial_j P_{XX}=P_X/f,\quad \partial_jG_{XX}=G_X/f,
 \quad \partial_jC_2=2,
\]

with the lower physical action and background jets fixed. The dictionary then
gives

\[
 \partial_j\begin{pmatrix}\widetilde P_{\chi\chi}\\
                          \widetilde G_{\chi\chi}\end{pmatrix}
 =\frac{2C^3}{C_1\Delta^2}
   \begin{pmatrix}\widetilde P_\chi\\\widetilde G_\chi\end{pmatrix}.
\]

This test verifies the implication, not the premise supplied by the separate
inverse calculation. It must not be read as an independent adjustable
second-action-jet direction.

## Executable API and local diagnostic limits

`general_ef.py` supplies:

- `action_dictionary(X,C,C1,C2,P,PX,PXX,GX,GXX)`;
- `background_dictionary(r,A,B,g,BrB,p,pr,X,Xr,C,C1,q=-1)`, where `pr` means
  \(dp/dr\), not radial pressure;
- `evaluate(m,background,physical_jet,C2)`, returning the actual original KGB
  principal and stress after transforming both action and background.

`evaluate` enforces positive \(m,A,B,C,r,X,D\) and nonzero \(\Delta\).
Its singular-map test and negative-\(\Delta\) canonical control distinguish
the field and coordinate gates. Numeric inputs should be real; use mpmath
inputs inside a `workdps` context for high precision. Near singular maps or a
zero principal margin, raw floating-point signs are not a rigorous certificate.

For the imported principal convention, the local EF static quadratic-energy
flag tests \(K=M_{00}>0\), \(M_{11}<0\), \(M_{22}<0\). The strict-cone
flag additionally tests \(K>|M_{01}|\) and positivity of

\[
 \min_{0\le t\le1}
 [K+M_{22}-2|M_{01}|t+(M_{11}-M_{22})t^2].
\]

The code evaluates this minimum at both endpoints and any interior minimum.
The existing KGB coupled expression includes metric mixing/Ricci elimination;
it is reused rather than independently rederived here. A physical solution
claim additionally needs on-shell background equations and the regular
invertible equivalence of constrained modes. The two conformal metrics share
the photon null cone, but that does not prove a bounded full physical-frame
Hamiltonian under a derivative-dependent field transformation.

Physical minimal matter becomes derivative-clock-coupled in the EF. This
vacuum helper omits those terms and cannot be reused inside baryonic matter
without them. The known conformal class and its conditional two-tensor-plus-
clock interpretation are documented in the prior verified
`kgb_mass_compatibility_2026/extension/SOURCES.md`; this extension of the
dictionary does not supply a new Hamiltonian theorem. Full Dirac/Ward closure,
physical constrained energy and boundary terms, global sourcing, FLRW,
strong coupling, and PPN remain outside this helper.

## Tests and provenance

Ten tests passed. Exact arbitrary-function and connection checks are paired
with 70-digit numerical controls, tolerance \(10^{-60}\). The non-affine
canonical control uses \(P=XC\), hence \(\widetilde P=\chi\), and recovers
\(M=\operatorname{diag}(1,-1,-1,-1)\). It is correctly not strictly inside
the photon cone. Its supplied metric is an operator-control fixture, **not an
on-shell vacuum solution**. Separately, the previously checked affine exact
flat-force halo recovers the same on-shell stress and healthy principal; it is
not a new non-affine MOND solution.

Run from repository root:

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/dictionary/test_general.py
```

The initial test-first run failed eight tests because the helper did not yet
exist; its standalone Hessian-cancellation identity passed. After implementation
and adding the conditional inverse-variation check, all ten passed. The formal
run and exact argv are recorded in `run_001/manifest.json`, with its declared
result in `run_001/results.json`. Manifest validation exited 0. The manifest
records the actual concurrent HEAD, dirty state, versions, unchanged hashes of
all four execution inputs, and bounded runtime. Requested base:
`583fdf69a597ef9ed57b4f9ced48dd457c8ef2de`; concurrent Fable-only HEAD changes
were not modified or treated as part of this dictionary's evidence.

The recorded HEAD is `1b1041234bc939466717eaacef2726c2df844ac5`; the run exited
0 in 0.946553 seconds. SHA-256 of `general_ef.py` is
`f7deab8dfc04a04cba8d9c047061663acd53987013b7d346ec782ad05a6b9125`, and of
`run_001/results.json` is
`55c2760917f6c6215fe9db9ec133875ddb8643e74bd34f10f9e101a8fdfe72b1`.

Computation-audit guided exact/numerical separation and provenance;
proofread-math self-review covered the new equations and notation. Only new
`dictionary/` files were written; no old/root files, commits or pushes.
