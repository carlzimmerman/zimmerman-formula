# Conditional No-Go for Exact Exponential MOND in Standard Single-Function GEA

## Abstract

We audit the standard generalized Einstein–æther (GEA) construction in which a single free function \(F(\mathcal K)\) controls the MOND modification. The target weak-field interpolation is

\[
\mu(y)=1-e^{-y},\qquad y=g/a_0.
\]

The standard GEA reconstruction relates the weak-field MOND function to the derivative of the free function and the æther couplings. Under the conventional normalization used in the GEA MOND literature, the relation may be written

\[
\mu=1-\frac{c_4-c_1}{2}F_{\mathcal K}
\]

for the relevant MOND branch.

We assume \(F_{\mathcal K}(0)\) is finite and nonzero and define effective quadratic couplings

\[
\bar c_i\equiv F_{\mathcal K}(0)c_i.
\]

Since the exponential law obeys \(\mu(0)=0\), the reconstruction requires

\[
\boxed{\bar c_4-\bar c_1=2}.\tag{1}
\]

The tensor-speed condition in Einstein–æther theory is

\[
c_T^2=\frac{1}{1-c_{13}},\qquad c_{13}=c_1+c_3,
\]

so GW propagation requires \(c_{13}\simeq0\). In the effective normalization this is \(\bar c_{13}\simeq0\).

Define

\[
\epsilon\equiv\bar c_{14}=\bar c_1+\bar c_4.
\]

Combining this with (1) gives

\[
\boxed{\bar c_1=-1+\frac{\epsilon}{2}},\qquad
\boxed{\bar c_4=1+\frac{\epsilon}{2}}.\tag{2}
\]

For the spin-1 mode, the standard Minkowski propagation speed may be written

\[
c_V^2=\frac{2c_1-c_{13}(2c_1-c_{13})}
{2c_{14}(1-c_{13})}.
\tag{3}
\]

Equivalently, one often encounters the algebraically identical form

\[
s_1^2=\frac{2c_1-c_1^2+c_3^2}{2c_{14}(1-c_{13})}.
\tag{4}
\]

At \(c_{13}=0\), Eq. (3) reduces to

\[
c_V^2=\frac{c_1}{c_{14}}.
\]

Because the common rescaling by \(F_{\mathcal K}(0)\) cancels in this ratio,

\[
\boxed{c_V^2\simeq\frac{\bar c_1}{\bar c_{14}}
=\frac{-1+\epsilon/2}{\epsilon}}.\tag{5}
\]

A positive spin-1 kinetic sector requires positive denominator/sign conventions corresponding to \(c_{14}>0\) in the standard Einstein–æther normalization. Then for the observationally relevant regime \(0<\epsilon\ll1\),

\[
-1+\epsilon/2<0,
\]

and therefore

\[
\boxed{c_V^2<0}.\tag{6}
\]

Thus the standard one-function GEA realization cannot simultaneously satisfy the exact exponential deep-MOND normalization, the near-luminal tensor condition, and a healthy propagating spin-1 mode, under the assumptions above.

## What survives

The target phenomenology itself is internally consistent:

\[
\boxed{\mu(y)=1-e^{-y}}.
\]

The corresponding AQUAL primitive can be chosen as

\[
\boxed{F(y)=\frac{y^2}{2}+(y+1)e^{-y}-1},\tag{7}
\]

because

\[
F'(y)=y(1-e^{-y})=y\mu(y).
\]

Therefore the negative result concerns the **specific relativistic architecture**, not the phenomenological interpolation law.

## Black-hole implication

The present result does not require a separate nonlinear black-hole instability calculation. A 2024 Einstein–æther perturbation analysis found that, in the short-wavelength limit and in an æther-orthogonal frame, black-hole no-ghost conditions and propagation speeds coincide with the corresponding Minkowski vector/tensor perturbation conditions. Therefore a failure already present in the asymptotic spin-1 sector is sufficient to obstruct that branch before a full nonlinear black-hole analysis becomes decisive.

## Scope and caveats

1. The proof is conditional on the standard GEA weak-field reconstruction relation.
2. The step \(\bar c_i=F_{\mathcal K}(0)c_i\) assumes finite \(F_{\mathcal K}(0)\). A singular or nonanalytic construction is outside this audit and must be treated separately.
3. The argument targets the standard single free function \(F(\mathcal K)\). It does not rule out theories with additional independent operators/functions, additional fields, different matter couplings, or different relativistic completions.
4. Sign conventions in the literature vary. The symbolic script checks the algebra in the convention used here; any new candidate must first map its conventions explicitly onto a canonical Einstein–æther normalization.
5. A tiny but nonzero \(c_{13}\) can be retained in a full numerical bound analysis; the leading obstruction is already order unity in \(c_1\) once (1) is imposed, so a \(|c_{13}|\ll1\) correction does not change the qualitative conclusion in the stated regime.

## Bottom line

\[
\boxed{
\mu(0)=0
\;+
\text{standard single-function GEA}
\;+
 c_T\simeq1
\;+
Q_V>0
\;\Longrightarrow\;
\text{incompatible spin-1 gradient stability}
}
\]

This closes the standard branch sufficiently to justify moving to a construction with **independent MOND constitutive and vector-kinetic control**, provided that construction passes a fresh quadratic-action audit.
