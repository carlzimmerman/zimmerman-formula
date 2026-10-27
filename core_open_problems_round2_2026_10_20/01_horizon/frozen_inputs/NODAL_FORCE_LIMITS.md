# Force predictions from the generated fermion interaction

12 October 2026. Continuation of NODAL_RING_ORIGIN.md. Two controlled static limits now distinguish this candidate from the originally imposed mass–velocity law. The weak-source limit gives V^4 proportional to M_b^2. The gapped, slowly varying limit gives V^4 proportional to M_b minus a positive mass offset at leading gradient order. Neither limit is a full solution through the crossover. This is a theoretical prediction under explicit medium assumptions, not a fit to or rejection by galaxy data.

## Medium assumptions and spatial anisotropy

Retain the specified fermion Hamiltonian at T=mu=0 and the critical quadratic matching of the scalar-polarization sector. Let A=N m_*/(2 pi v), beta=A h^3. The radial band velocity at the ring is v_r=k0/m_*. The leading momentum transfer at a patch of azimuth theta is

    Q_theta^2 = v_r^2 (kx cos theta+ky sin theta)^2 + v^2 kz^2.

At zero background gap, the previous susceptibility gives a polarization Hessian A h^2 pi <Q_theta>/4. For v_r=v, the factor multiplying v|k| is 1 along the ring axis and 2/pi in its plane. A single ring is spatially anisotropic; its homogeneous |P|^3 potential did not remove this anisotropy.

For an explicit isotropic comparison, assume a uniform distribution of otherwise identical ring orientations with equal radial and axial speeds. This is an added physical assumption, not a derived state. A includes the total species weight in this ensemble. Uniform tangent directions give <sqrt(1-u^2)>=pi/4. The resulting gapless static Hessian is

    K_P(k)-K_P(0) = eta |k|,
    eta = A h^2 pi^2 v/16.

This corresponds to positive spatial energy eta P dot |grad| P /2. Here |grad| is the operator with Fourier multiplier |k|; it is nonlocal. The underlying fermion differential Hamiltonian remains local. The nonlocality results from eliminating gapless modes.

## Weak-source force, including a finite source

At small source amplitude, use the leading linearized field equations

    D=a grad phi-P,
    div D=alpha rho_b,
    eta |grad| P=D/a.

For a point source M, Fourier transformation gives

    phi(k) = -alpha M (1+a eta |k|)/(a^2 eta |k|^3).

With the inverse transform convention integral d^3k/(2pi)^3, the attractive scalar force is

    g_s(r) = alpha^2 M/(4 pi a r^2)
              + alpha^2 M/(2 pi^2 a^2 eta r).

The potential's logarithmic additive infrared ambiguity drops out of this force. This is a local static-region expression; the cosmological infrared boundary is not supplied.

For a Gaussian baryon density whose Fourier transform is M exp(-b^2 k^2/2), the extra inverse-radius contribution becomes

    g_extra(r) = alpha^2 M/(2 pi^2 a^2 eta r) F(r/b),
    F(z)=1-(sqrt(2)/z) Dawson(z/sqrt(2)).

Near the centre F(z)=z^2/3+O(z^4), so this contribution is regular and proportional to r. At large z it approaches 1. Direct Fourier quadrature confirms this analytic expression; F(1)=0.27522, F(10)=0.98990, and F(30)=0.99889 approximately. The exact computed values are retained in nodal_force_run/results.json.

The asymptotic speed consequently satisfies

    V_infinity^2 = alpha^2 M/(2 pi^2 a^2 eta),
    V_infinity^4 proportional to M^2.

Flat rotation by itself does not establish the desired baryonic normalization. This mismatch in mass exponent follows from linear response, not from a point-source singularity. The amplitude proportional to M is also a general feature of the weak-source linearized problem with fixed coefficients; isotropization supplies the simple radial formula, not the linearity in M.

Validity is essential. In this weak solution, P approximately B/r with B=alpha M/(2 pi^2 a eta). The gap-to-spatial-energy ratio is hB/v. The gapless expansion requires this ratio much less than one. The calculated weak law must not be extrapolated to large source masses.

An independent Fourier identity checks the vector normalization:

    |grad| [B r_hat/r] = (pi B/2) r_hat/r^2.

It follows by applying |grad| to grad ln(r). With an Abel momentum regulator exp(-epsilon |k|), |grad| ln(r)=-atan(r/epsilon)/r, which yields the displayed expression as epsilon tends to zero. The numerical audit checks the regulated sine integral and radial derivative.

## Large-gap limit with generated gradient coefficients

For q much less than the homogeneous gap Delta, the previously computed interband responses are

    delta K_parallel/A = q^2/(6 Delta) + O(q^4/Delta^3),
    delta K_perp/A = q^2/(4 Delta) + O(q^4/Delta^3).

For the same isotropic equal-speed ensemble, <Q_theta^2>=(2/3)v^2 |k|^2. Write P=p n, |n|=1. The corresponding leading two-derivative energy is

    E_grad = A h v^2 [ |grad p|^2/(18 p)
                        + p |grad n|^2/12 ].

This uses the rotationally invariant two-derivative terms inferred from the constant-background Hessians; possible ultraviolet analytic gradient terms are additional. Such terms with finite coefficients do not share this singular 1/p coefficient. No finite-frequency kinetic term has been inferred here.

For radial n=r_hat, |grad n|^2=2/r^2. Defining c=A h v^2, the radial energy density is c[p'^2/(18p)+p/(6r^2)]. Its variational force at p=B/r is

    delta E_grad/dp = 2c/(9r^2).

Both symbolic Euler–Lagrange differentiation and a compact-support finite variation verify this coefficient. Combining it with the cubic derivative beta p^2 yields

    beta B^2 + 2c/9 = alpha M/(4 pi a).

Since the scalar inverse-radius acceleration has coefficient alpha B/a,

    V_infinity^4 = K (M-M_offset) + higher-gradient corrections,
    K=alpha^3/(4 pi a^3 beta),
    M_offset=8 pi a c/(9 alpha).

This is a large-gap asymptotic expansion, not a threshold theorem. The apparent zero at M=M_offset lies outside its regime and must not be interpreted as a minimum galaxy mass. The gradient-to-cubic ratio is 2/[9(hB/v)^2]; it is 0.02469, 0.002222 and 0.0002469 for hB/v=3,10,30. Higher derivatives must still be controlled, and the central region where the gap closes is not covered.

## Common scale and observational decision

Define the model's free mass scale

    M_s=4 pi a beta v^2/(alpha h^2),
    x=M/M_s,
    y=V_infinity^4/(K M_s).

The limiting results read

    weak gap: y approximately (32/pi^3)^2 x^2,
    large gap: y approximately x-2/9.

These are separate asymptotes. Adding the gapless |k| kernel and the cubic potential as a purported exact interpolation would double-count or misrepresent parts of the determinant at intermediate gap. No such interpolation was used. A full sourced fermion calculation is needed there.

This provides a candidate observational test: once the medium parameters fix M_s, its mass–velocity relation should curve away from the linear-in-mass target at sufficiently small mass. Current calculations do not fix M_s. It can therefore lie below the measured galaxy range, and these results alone do not exclude the model. They also do not validate it. Distances, inclinations, stellar mass estimates and noncircular motion would have to enter any comparison with observations; no assumption-free mass–velocity catalogue was presumed.

The constructive advance is a force prediction calculated from generated spatial response, including its failure to preserve the target scaling in one controlled regime. Remaining obligations are critical matching, a physical isotropic medium and state, a sourced solution through the crossover, dynamical response, and the independent vacuum-normalization relation. The previous fixed-source stability proof for a constant-gamma phenomenological action does not certify this fermionic completion.

## Evidence

nodal_force.py, nodal_force_contract.json and nodal_force_run/ contain the angular averages, Gaussian-source Fourier checks, regulated vector identity and weak-source scaling diagnostic. nodal_gapped.py, nodal_gapped_contract.json and nodal_gapped_run/ contain the low-q coefficients, symbolic radial variation and three independent finite-energy variations. Both bounded runs completed successfully; their manifests validate provenance. The mass-exponent diagnostic checks the implementation of an analytic linear-response result and is not independent empirical evidence.
