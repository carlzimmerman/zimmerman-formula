# Independent audit of the dynamical co-Plummer core and its negative radial trial

VC3-CORE-AUDIT-001, 15 October 2026. Read-only reconstruction of the author's
equilibrium, full radial density/Gauss energy, trial and family bound. Only
this audit file was written by the reviewer. This is an independent derivation
by another agent using the same tool/model environment, not external peer
review, a formal certificate or an audit of the entire physical theory.

**Verdict: the exact hybrid two-fluid equilibrium and universal negative-energy
claim are correct with the explicit EOS-domain qualification in AMENDMENT.md.**
The result defeats positive coupled radial energy for the stated critical-charge
weak-neutral co-Plummer family. It neither excludes all dynamical charged cores
nor proves a full nonlinear/spectral instability theorem.

## 1. Frozen artifacts and actual evidence

| Artifact | SHA256 |
|---|---|
| `PROOF.md` | `e718b62e8b70b5fff1869d952d0b20e072bc273fc7963f17a454fc4930fbd11f` |
| `check_core_v3.py` | `cbcbdac8a43c7f215b8cb7f38606e75c3268f815218a0ff186172e2f399adc74` |
| `AMENDMENT.md` | `6bb12035cc089c9bde7f0fe1a2319f08dc05922751454e4c7f747ea278d1ee03` |
| `run_v3/manifest.json` | `323caf7384569bd12f977270a1fa3a6f52e0d51be8be2ea7fd488c32ee5ab0cb` |

The final version-2 manifest was independently validated against current input
and output bytes. It reports 27 exact checks and a separate 60-digit numerical
quadrature. The earlier implementation-only failure is preserved by the author;
it is not evidence against the mathematical claim or a successful check.

## 2. Equilibrium and Hessian independently reconstructed

The gravity source in this comparison is exactly the two rest densities. The
electromagnetic and internal energies are not inserted into Poisson's source.
This convention is essential to the claim, and it is stated in the proof.
For the specified Plummer profiles, direct differentiation gives

\[
 P_s'/\rho_s=-(1+f)g_c,\qquad
 P_c'/\rho_c=-g_c\left(1+f-b_q^2/(1-x)\right).
\]

The inverse barotrope has density derivative
`c_c,N^2=psi_c[1+f-b_q^2/(1-x)]/5`; its minimum bracket occurs at x_max.
The stated charge/compressibility condition is consequently the correct
everywhere condition for this constructed EOS. It is a new continuum input,
not microphysics. The endpoint regularity limitations are retained.

For mass-preserving radial density tangents eta_a, let
`delta m_a=4*pi*integral_0^r eta_a(s)s^2 ds`. The internal Hessian is

\[
 Q_U=\sum_a\int\frac{c_{a,N}^2}{4\pi\rho_a r^2}
                         (\delta m_a')^2dr.
\]

Integrating the Poisson Green energy gives

\[
 Q_G=-G\int\frac{(\delta m_c+\delta m_s)^2}{r^2}dr.
\]

Gauss gives `delta D=b_q*sqrt(4*pi*G)*delta m_c/(4*pi*r^2)` and the
electric Legendre Hessian is `dE/dD=(1-x)^-2`. Therefore

\[
 Q_A=G b_q^2\int\frac{\delta m_c^2}{r^2(1-x)^2}dr.
\]

There is no extra factor one half in these second derivatives. There is no
omitted neutral/core gravitational cross term. This is not the incorrect
operation of differentiating H as a function of the background E while
holding Gauss-fixed D unconstrained.

The chemical/electrostatic first integrals, with potentials and specific
enthalpies zero at infinity, make the first constrained energy variation
vanish. They cancel second-order density-path terms. At b_q=1, normalized
rho_c=3/[4*pi*(1+r^2)^(5/2)] gives exactly
`A=(1+r^2)^2/(15*r^2)` and equation (6) of the proof. Radial velocities are
parallel to the background field, so no missing transverse frame boost term
changes this potential-energy test. Other positive kinetic terms cannot turn
a negative potential direction into a positive energy functional.

## 3. Trial admissibility, including the EOS endpoint

The trial is
`u=Y=25*r^3/[(1+r^2)^2*(25+r^2)]`, `v=(8/5)Y`, and the actual neutral
mass tangent is `delta m_s=fv`. Both conserved masses vanish at each endpoint.
At the center the displacements are O(r). At infinity they tend to constants:
in normalized units `xi_c -> -25/3`, and `xi_s -> -(8/5)*25/3`.
The inertia integrand is O(r^-3), so it is integrable. The draft's O(r^-2)
displacement claim was corrected before the final frozen run; its incorrect
power did not invalidate finite inertia.

Positive densities alone do not suffice for the stated EOS domain
`rho_c<=rho_*`: a positive linear path parameter raises the center above
rho_*. This was the second audit correction, supplied after the run as the
explicit frozen-proof amendment. It is resolved without assuming an EOS
extension. Direct differentiation gives

\[
 \eta_c/\rho_c=
 \frac{25(25-8r^2-r^4)}{\sqrt{1+r^2}(25+r^2)^2},
 \quad |\eta_c/\rho_c|\le25,
 \quad \eta_s/\rho_s=(8/5)\eta_c/\rho_c.
\]

Choose `-1/40<tau<0`. Both linear density paths remain strictly positive.
Where eta_c>=0, charged density decreases. Where eta_c<0, one has
`r^2>sqrt(41)-4>1`, hence background rho_c<rho_*/4; its path factor is
below two, keeping rho_c(tau)<rho_*/2. Thus the entire charged path remains
within its declared EOS domain. Also

\[
 \delta D/D=Y/M_c(<r)=25/[\sqrt{1+r^2}(25+r^2)]\in(0,1],
\]

so the negative-parameter path stays between zero and the original D. Both
mass constraints and the electric constitutive domain are preserved. This
one-sided path already decreases energy as `tau^2 Q/2+o(tau^2)` when Q<0.
A two-sided PDE neighborhood would require the additional EOS continuation
explicitly excluded from the present counterexample.

## 4. Exact family bound independently checked

For 0<f<=1/1000 and the charged compressibility condition,
`x_max<f/(1+f)<1/1000` and `q0<(13/5)f`. Expanding only with inequalities,

\[
 (1-x)^{-1}\ge1+x,\qquad
 (1-x)^{-2}\le1+2x+3x^2/(1-1/1000)^2,
\]

gives the author's equation (9). The first inequality makes the core
derivative contribution more negative; its sign has not been reversed.
The exact positive T permits replacing q0 by its upper bound, and positive B
permits replacing f by 1/1000 in the last upper bound.

The three rational integrals I_A,I_B,I_B2 match direct independent quadrature.
The combined T was also integrated independently in one operation, rather
than subtracting the author's two separately integrated moments. With
`z=sqrt(1+r^2)`, its exact rational integrand is

\[
 -\frac{125(z^2-1)
 [3z^8+26z^6-554z^4-6432z^2+8832]}
 {z^{10}(z^2+24)^4},\qquad 1<z<\infty.
\]

Its integral simplifies to the author's T with exact difference zero.
Independent 45-digit controls gave

```
I_A  = 0.04629297302261194383237027
I_B  = 0.07890847674308854062335842
I_B2 = 0.006927324028892668757270528
T    = 0.03279942632303404005428341
L+B/1000 = -0.0023683613414311289715030139364180728
```

The decimal controls are not the uniform sign proof. The author's exact
rational interval implementation uses alternating arctangent remainders,
Machin's pi identity with its branch specified, and integer square-root
bounds. Its interval arithmetic encloses every constant in L+B/1000 and
certifies the stated strictly negative interval. Hence the uniform family
conclusion is supported by an analytic reduction and exact finite constants,
not by accumulating successful parameter scans.

The assigned witness's very small local `hcrit/h_*` bound is also consistent
with the harmonic effective-inertia formula and actual mass weights. It
illustrates why principal propagation and a restricted homology test cannot
certify the full radial density form.

## 5. Exact conclusion and remaining scope

Every member of the stated critical-charge co-Plummer family with
`0<f<=1/1000` and positive charged compressibility fails positive coupled
radial energy. An admissible energy-decreasing path exists even without
extending the inverse EOS above its central endpoint.

This does not prove a full current/gauge/Einstein spectral-domain theorem,
exclude other density shapes, exclude larger neutral populations or
subcritical charge ratios, or derive the inverse EOS from a carrier. The old
fixed-source neutral theorem remains valid under its own fixed-source
hypotheses. Replacing its central source by a dynamical charged species is a
substantive new coupled problem; this audit identifies the explicit negative
direction rather than declaring that replacement closed.
