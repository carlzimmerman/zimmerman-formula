# Passive periodic peak and post-memory future tail

Let Gamma0 be either the fixed physical neutral width, or the positive SSS
floor when every FFS exit is blocked. For a physical incoming pair, EN is
the parent lab energy, b=M/EN, and the actual source normalization is bounded
by lambda/(4 E1 E2 EN). Let a be the periodic retarded response to v and let
H(t) be any Hermitian periodic detuning matrix. Additional local charged
absorption B(t) is positive and need not commute with Gamma0 or H. The
periodic equation is

    da/dtau = -[iH(t)+(b Gamma0+B(t))/2]a+v.

Its real energy identity and weighted Cauchy inequality imply

    R=<a† b Gamma0 a>
     <=2 Re<a†v>
     <=2 sqrt(R) sqrt(v†(b Gamma0)^-1 v),
    R<=4 v†Gamma0^-1 v/b.

For a stronger positive time-dependent neutral exit matrix, the same proof
uses Gamma0 as a lower form bound. Summing the positive source decomposition
of G and retaining the relativistic source prefactor gives

    sigma v_Moller <= Tr(G Gamma0^-1)/(E1 E2 M)
                    <= Tr(G Gamma0^-1)/(m_min² M).

Thus parent time dilation cancels exactly in the uniform physical pair
bound. At the aligned pole m0=M/2 this is

    sigma_peak=4 Tr(G Gamma0^-1)/M³.

It equals 15741.999837 mu^-2 for the physical vacuum width and
97360.190956 mu^-2 for the all-FFS-blocked bosonic floor. The small charged
mass variation multiplies either by at most m0²/m_min². No momentum tail
or nonrelativistic flux substitution is required for this inequality.
Time-dependent source normalization can also be bounded by its maximum;
the same weighted identity applies to that forcing.

For the scalar detuning/fixed-width model, the Floquet response is a positive
sideband sum. Each shifted resolvent obeys the same peak bound and
sum_n J_n(z)²=1. Therefore memory can redistribute the rate over the orbit
and exceed stationary phase averaging, but it cannot exceed this passive
peak. The energy identity also covers the explicit time-dependent positive
charged absorptive width, where the simple diagonal sideband expression no
longer applies. It does not cover an unspecified active or nonlocal medium.

Let n=n++n- and Y=n/s. In the charge-symmetric factorized sector,
gamma_pair=n²<sigma v>/4, so

    dY/dt=-s<sigma v>Y²/2,
    d(1/Y)/dN=s<sigma v>/(2H).

For the recorded radiation normalization, TSM=Tc*mu/xi, gs=gRho=106.75,
and reduced Planck mass Mbar=2.435e18 GeV,

    s=2pi² gs TSM³/45,
    H=sqrt(pi² gRho/90) TSM²/Mbar.

With a normalized to one at the memory endpoint, TSM=Tend/a, s=s_end/a³
and H=H_end/a². Granting permanent saturation of the uniform peak,

    L_future <= integral_1^infinity s_end sigma_peak/(2H_end) da/a²
             = s_end sigma_peak/(2H_end),
    Y_future >= [1/Y_end+L_future]^-1.

Equivalently integrate s sigma/(2HT) from T=0 to Tend; its integrand is
constant in this declared radiation model. The code evaluates both routes
and a logarithmic-scale integral independently. The scale-factor factor to
today is 1-1/a_today; granting the infinite radiation tail is more favorable
to loss. The optional shrinking harmonic amplitude gives an even smaller
mass-prefactor correction; the conservative result keeps the current inner
turning-point mass forever.

A sufficient condition for the same radiation tail to remain an upper loss
envelope beyond the constant-g model is conserved comoving entropy together
with H(a)>=H_end/a². For example, spatially flat positive-energy components
with rho-3p>=0 obey

    d(rho a^4)/d ln a=(rho-3p)a^4>=0.

They therefore cannot lower H below this radiation continuation. This is a
stated sufficient condition, not a numerical reconstruction of every later
thermal transition or an assumption about an unspecified cosmology.

This bound concerns the passive fixed-pole continuation from the specified
new endpoint. It excludes neither new early histories nor additional pair
losses, altered spectrum/force matching, entropy production, or unspecified
nonlocal/dispersive charged selfenergies. The all-FFS-blocked case is an
optimistic auxiliary positive-width envelope, not an evolved physical bath.

## Computed outcome and local charged absorption

The actual endpoint is TSM=100.00000000000007 GeV,
s=4.68257897696e7 GeV³ and H=1.40512057865e-14 GeV. The recorded orbit's H
normalization agrees with the independently reconstructed RD value. The
current inner-turning mass gives m0²/m_min²=1.000000254938; shrinking the
harmonic amplitude yields an integrated factor 1.000000101975 instead.
This correction cannot materially change the comparison.

| Neutral width model | Future yield floor | Floor / charged gate |
|---|---:|---:|
| Physical vacuum Gamma | 8.09083838e-14 | 142.43492 |
| Every FFS exit blocked, SSS floor | 2.15708537e-14 | 37.97434 |

The gate is 5.680375574e-16 to the requested precision. The actual start is
303.415 times this gate. Reaching it through this continuation would require
multiplying the already maximal peak by 267.576 or 43.264 respectively;
these are total multiplicative factors, not increments added to one.

For the explicit local charged width, the weighted perturbation form norm
epsilon=sup||Gamma0^-1/2 GammaC Gamma0^-1/2|| is .0170778 (vacuum) and
.105622 (SSS floor) at the endpoint. Its response-rate intervals relative to
the corresponding unperturbed Floquet response are [.96614,1.03445] and
[.79991,1.22240]. The passive peak above already permits arbitrary additional
positive local GammaC, so these intervals do not justify increasing that
peak. They only bracket its possible modification of a submaximal response.
The future decreasing-amplitude model makes epsilon smaller.

Eight actual future continuum Floquet averages at a=1,2,10,100 stay below
the peak. Six full-matrix periodic controls include perfect saturation,
the actual local charged width, and noncommuting Hermitian detunings. They
satisfy the passive energy identity within 1.01e-6 of the peak normalization.
These are finite implementation checks of the stated analytic inequality,
not substitutes for it. The temperature, scale-factor and log-scale future
integrals agree below 1e-11 relative in the fresh run.
