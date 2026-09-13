# Door 04 — one-metric curvature action gate

Date: 2026-09-09. Status: **tested subclass closed**.

This door tests the minimal local, frame-free metric-only route capable of
nonlinear curvature response:

\[
 S=\int d^4x\sqrt{-g}\,[F R+aR^2]+S_m,
\]

with an optional Weyl-squared term \(b C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}\).
The script varies the action at the equation level and solves \(\Phi\) and
\(\Psi\) independently in a static Fourier mode. It does not insert a
desired PPN value, pole count, or source scaling.

## Derived obstruction

Variation of \(F R+aR^2\) gives

\[
 F G_{\mu\nu}+2aR R_{\mu\nu}-aR^2g_{\mu\nu}
 +2a(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu)R=T_{\mu\nu},
\]

and its linear trace has operator \(-F+6a\Box\). For \(K=|\mathbf k|^2>0\),
the independently varied static equations produce

\[
 \Phi=-{\rho(F+8aK)\over2FK(F+6aK)},\qquad
 \Psi=-{\rho(F+4aK)\over2FK(F+6aK)},
\]

so

\[
 \gamma_{\rm PPN}={\Psi\over\Phi}={F+4aK\over F+8aK},\qquad
 \gamma-1={-4aK\over F+8aK}.
\]

Exact no-slip for every nonzero \(K\) therefore forces \(a=0\). For
\(a\ne0\), the trace has a scalar pole \(\Box=F/(6a)\), and the exact
Legendre transform \(\varphi=F+2aR\) gives the Einstein-frame scalar kinetic
coefficient \(3/(2\varphi)\) when \(\varphi>0\). Health of this scalar does
not remove the extra mode: the metric sector is not two tensor modes.

The static response is homogeneous of degree one in \(\rho\), while exact
deep MOND requires degree one-half under \(\rho\mapsto s\rho\). Thus a fixed
linear curvature operator cannot equal the exact MOND constitutive law.

If the Weyl-squared term is added, the varied TT principal symbol is

\[
 P_{TT}(z)=Fz+bz^2=z(F+bz),
\]

and the calculated propagator is

\[
 {1\over P_{TT}}={1\over Fz}-{b\over F(F+bz)}.
\]

The massless and massive pole residues are \(1/F\) and \(-1/F\), so any
nonzero \(b\) adds an opposite-residue spin-2 mode.

## Scope

This is not a universal no-go for all nonlocal, preferred-frame, nonanalytic,
or matter-field constructions. It closes only the explicit local analytic
metric-only curvature subclass tested here. The scripts do not certify the
full user target and do not claim that the submitted AeST branch is revived.

## Reproduction

From the repository root:

```text
python3 qwen_claude_field_theory/closure_2026/door04_metric_curvature_2026/metric_curvature_gate.py
python3 qwen_claude_field_theory/closure_2026/door04_metric_curvature_2026/test_metric_curvature_gate.py
```

Both commands completed with exit status 0 and nine diagnostic checks passed
in the gate. The output is intentionally a successful reproduction of a
falsification, not a successful gravity theory.
