# Expansion through vacuum growth and spatial conversion

2026-10-11. This joins the two stages of QUANTUM_HANDOFF with the same
imposed radiation background. It remains a Gaussian-to-classical envelope
prescription with the stated matching limitations, not full quantum FLRW.

## Consistent background and early stage

Use x=m epsilon t and a(x)^2=1+2h x, with
h=H_initial/(m epsilon)=0.00013781994828129018. Fourier labels are comoving:
physical momentum is m u_* q/a. Source and daughter envelopes are rescaled
by a^(3/2), so their integrated charge normalization remains fixed.

The early finite-box Gaussian stage uses G=a^(-3/2), k(x)=k_0 a^(-3), and
pair detuning 2L_A(q,a). The comoving vacuum pair weight is fixed by the
initial source count, not diluted a second time. Both normal and anomalous
quartic terms are retained. In the dq=0.4 box, the mean fraction 1e-4 occurs
at x=75.27088003, compared with 73.76850999 without expansion. The earlier
1e-5 and later 1e-3 events are also saved.

[expanding_handoff.py](expanding_handoff.py) uses the tightened tolerances
from QUANTUM_HANDOFF. Covariance, charge and sampling checks pass; the
largest recorded relative pure-covariance projection is below 2.76e-10.
[Results](expanding_handoff_run/results.json) retain the state used below.

## Spatial equations and work identity

The moving-source equations become

\[
 iA'=L_A(q,a)A+G(x)B A^*+k(x)|A|^2A,\qquad
 iB'=L_B(q,a)B+G(x)A^2.
\]

L_A and L_B are the earlier relativistic free detunings evaluated at q/a.
The leading nonrelativistic interaction vertices remain approximations.
In particular the a^(3/2) rescaling also produces curvature-frequency terms
of order H^2/m^2, omitted here in the adiabatic envelope. The initial H/m is
about 1.38e-11; this observation alone is not a global quantum-error proof.
The imposed background does not include the field's Friedmann backreaction.

Charge <|A|^2+|B|^2> stays conserved. The reduced energy now satisfies an
explicit work identity rather than constant-energy conservation:

\[
 E_r=\langle2A^*L_AA+B^*L_BB+2G\operatorname{Re}(B^*A^2)+k|A|^4\rangle,
\]

\[
 E_r'=2\langle A^*L_A'A\rangle+\langle B^*L_B'B\rangle
 +2G'\operatorname{Re}\langle B^*A^2\rangle+k'\langle|A|^4\rangle.
\]

The derivatives are explicit background derivatives, holding the fields
fixed: G'=-(3h/2a^2)G, k'=-(3h/a^2)k,

\[
 L_A'=-{h u_*^2q^2\over\epsilon a^4\sqrt{1+u_*^2q^2/a^2}},\qquad
 L_B'=-{h u_*^2q^2\over\epsilon a^4\sqrt{R^2+u_*^2q^2/a^2}}.
\]

[expanding_spatial.py](expanding_spatial.py) uses midpoint background
coefficients in the symmetric kinetic/nonlinear splitting and trapezoidal
integration of this work at every time step. Reconstructed energy minus
initial energy is compared with the integrated work. This checks the
explicitly time-dependent Hamiltonian, not a phenomenological damping law.

The correlated sample and per-realization source-charge adjustment follow
QUANTUM_HANDOFF. The spatial runs use N=24, seed 471901, the 1e-4 handoff,
and two maximum steps, 0.005 and 0.0025, to absolute x=100. Results belong
to one small box and one draw. They are not an expanding ensemble average.

## Results

Both spatial runs complete and all four charge/work diagnostics pass.

| Maximum step | Daughters at x=100 | Moving source charge | Max energy-work residual |
|---|---:|---:|---:|
| 0.005 | 0.591914845 | 0.260411361 | 1.322e-5 |
| 0.0025 | 0.591914792 | 0.260405112 | 3.303e-6 |

The finer run's charge drift is below 1.0e-11, and endpoint outer-mode charge
is about 1.07e-8. The work residual falls by a factor of four when the step
halves, consistent with the time-dependent second-order splitting. This
supports the numerical work accounting; it does not certify the omitted
quantum terms. [Spatial results](expanding_spatial_run/results.json),
[spatial manifest](expanding_spatial_run/manifest.json), and
[handoff manifest](expanding_handoff_run/manifest.json) preserve the records.

At the endpoint a=1.01368831. The reduced energy has changed by approximately
-0.03353, accounted for by expansion work. Treating energy as constant would
have been wrong. The daughter fraction differs from the corresponding
nonexpanding sampled case (about 0.62767), but remains substantial. That
comparison includes expansion's effect on the earlier quantum growth and
handoff phase as well as on the spatial stage.

The energy-square check also has a time-dependent version: replace the
coupling 1 by G and quartic k by k(x) in SPATIAL_ENERGY_BOUND. Completing
the square gives remainder k(x)-G(x)^2/d_0. Both terms scale as a^-3, so
the positive margin is retained during this imposed expansion. E_r itself
is no longer conserved; its recorded work must enter the kinetic budget.
The exact full-classical FLRW comparison theorem remains a separate result,
not a theorem for the Gaussian quantum state.

**Conclusion:** substantial conversion and moving-source population persist
when this approximation consistently includes expansion through both
stages. The result is one realization in the original small comoving box;
no expanding ensemble, large-box convergence or relic abundance is claimed.
No global quantum-error bound has been supplied. The initial charged source
is still an input, and halo/vacuum selection remains absent.
