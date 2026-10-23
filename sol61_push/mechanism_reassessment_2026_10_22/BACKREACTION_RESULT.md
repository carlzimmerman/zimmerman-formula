# Radiation backreaction: damping and static softening must be tested together

The outgoing reduced field has a positive dissipative susceptibility for the two computed source frequencies. A reciprocally coupled weak mechanical mode can therefore lose energy to radiation. But the same coupling reduces the source's static restoring force. The combined system can be unstable even though the forced outgoing solution has positive radiated power. This provides a concrete stability condition for any proposed matter completion, not a completed dynamical mechanism.

## Reciprocal diagnostic, not a new matter theory

Let A be the positive radial field stiffness operator and M its positive kinetic operator from RADIAL_WAVE_RESULT.md. Use the radial inner product integral dr, with the common4pi angular factor omitted consistently. Introduce a diagnostic coordinate Q with bare inertia m>0, stiffness k>0 and reciprocal interaction lambda Q<f,u>:

    L = m Qdot²/2-k Q²/2
        +<udot,M udot>/2-<u,A u>/2+lambda Q<f,u>.

Then the field and source equations are

    M uddot+A u=lambda Q f,
    m Qddot+k Q=lambda<f,u>.

The source shape f is the Gaussian breathing perturbation used in the prior calculation. This construction specifies how reciprocal coupling would work; m, k, lambda and the existence of such a matter mode have not been derived from A33 or a cold-sector action. It must not be adopted as a new fundamental mechanism merely because it can damp.

The conserved full-domain energy includes -lambda Q<f,u>. For a finite inner region, its loss equals outward field flux. Thus dissipation of the local source need not violate conservation of the combined source-plus-field system.

## Static stability is a separate gate

Define chi0=<f,A^(-1)f> on the compatible decaying static problem. Completing the square gives

    V = <u-lambda Q A^(-1)f,
           A(u-lambda Q A^(-1)f)>/2
        +(k-lambda² chi0) Q²/2.

Consequently k>lambda² chi0 is the positive static-stiffness condition in this diagnostic model. At equality a zero direction appears; below it the quadratic energy has a negative direction. The positive radiation flux does not repair this negative static curvature. Turning this energy statement into a full PDE spectral theorem would require its domain and evolution analysis.

The computed static radial vector response p=sigma' obeys

    h p-gamma(p''+2p'/r-2p/r²)
      =-r exp(-r²/2)/(2pi)^(3/2).

With regular centre and finite outer p=0, reconstruct sigma(outer)=0 and compare <f,u> with integral r²[h p²+gamma(p'+2p/r)²]dr. Results:

| Outer radius | chi0 from source-response | quadratic-energy integral |
|---|---:|---:|
| 30 | 0.001629899462 | 0.001629899483 |
| 60 | 0.001629899399 | 0.001629899483 |

The largest relative identity mismatch is5.18e-8; domain change is3.88e-8. The mismatch also includes reconstruction quadrature and negligible finite-inner-boundary terms. This is numerical evidence in the reduced model, not an exact infinite-domain theorem. The diagnostic threshold is k/lambda²>approximately0.00162990 in this normalization.

## Outgoing susceptibility and weak-coupling damping

For the outgoing frequency-domain problem define

    chi(omega)=<f,(A-omega² M)^(-1)_out f>.

The coupled resonance equation is

    k-m omega²-lambda² chi(omega)=0.

Our convention exp(-i omega t) gives radiated power=lambda² |Q|² omega Im chi/2. Recomputing the accepted global response yields:

| Dimensionless omega | Re chi | Im chi |
|---|---:|---:|
| 0.3 | 0.00172055936 | 0.0000143232876 |
| 1 | 0.00227086192 | 0.000892994053 |

The imaginary parts are positive and reproduce outgoing power. To leading order in weak coupling, near a positive bare frequency omega0=sqrt(k/m), the amplitude damping rate is

    Gamma=lambda² Im chi(omega0)/(2m omega0).

The frequency shift at that order is -lambda² Re chi/(2m omega0). If the real shift is included nonperturbatively but the imaginary part is small, the denominator of Gamma becomes 2m omega+lambda² d(Re chi)/domega. That derivative and the actual complex pole have not been computed. Positivity of Im chi alone is not sufficient near an arbitrary strongly coupled pole.

For the two trial frequencies the leading Gamma coefficients are2.38721e-5 and4.46497e-4 times lambda²/m in the stated time units. These are conditional formulas, not halo damping times: no physical source inertia, stiffness, coupling or frequency has been supplied.

## Frequency relevance and what to do next

The earlier response uses time unit R sqrt(b)/c with b=(2+3 beta)/beta, beta=0.02798. A hypothetical material motion with angular frequency v/R corresponds to dimensionless omega=sqrt(b) v/c. For the explicitly chosen illustrative ratio v/c=0.001, omega is approximately0.00863, much lower than0.3 or1. This is a dimensional comparison, not a measurement of any galaxy. It shows why the two successfully computed higher frequencies cannot certify the rate of slow material relaxation. The low-frequency response must be computed with its much longer exterior, rather than extrapolated from these points.

A useful completion must derive a matter perturbation and its inertia/restoring force, satisfy the static-stability condition, and calculate its frequency-dependent radiation reaction. It must also preserve the law and pass the independent Solar-System/galaxy gates. The cold-density selector and kappa coefficient are still not derived.

## Evidence

Eight checks pass in backreaction_run2/manifest.json, which validates. The incoming-boundary mutation makes Im chi negative and fails positive dissipation while retaining energy balance, as expected. The helper backreaction_response.py copies the accepted solver definitions and adds susceptibility output; original source and previous manifest inputs were preserved. An unused double-sign mutation override was removed before mutation execution; BACKREACTION_CONTRACT.md records this correction. backreaction_run is historical because the script hash subsequently changed. Numerical checks and algebra were self-reviewed, not independently certified. The square-completion and oscillator response are standard mechanisms, not claims of new physics.
