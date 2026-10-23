# Slow radiation is strongly suppressed by the polarized halo

The reduced spherical model radiates at slow source frequencies, but its power approaches an omega^5 law for the mass-conserving breathing source. This is substantially more suppressed than the homogeneous vacuum's omega^(5/2) law. Combining the measured susceptibility with the previous weak-coupling backreaction formula gives millions of source periods or more for amplitude damping in the diagnostic stable weak-coupling regime. Thus an open radiation channel is not enough to establish rapid settling.

These conclusions remain scoped to the formal reduced field, prescribed Plummer background, Gaussian breathing source and diagnostic reciprocal oscillator. They neither prove a no-go for all dynamical completions nor supply a cold-density selector.

## Global low-frequency solves

The equations, normalization and boundary branches are unchanged from FORCED_RADIAL_RESULT.md. Frequencies0.01 and0.03 were solved at2,4,8 times r_cross=20/omega; the largest domain was16000. The initial tolerance2e-7 failed the frozen1e-4 source-work criterion at0.01. Refinement to2e-9 passes without changing the acceptance threshold. A further point0.003 used outer radius53333.33 and the same refined tolerance.

| omega | largest outer radius | angular-normalized power | Re chi | Im chi (approximately) |
|---|---:|---:|---:|---:|
| 0.003 | 53333.33 | 2.83685e-16 | 0.00162990766 | 1.89132e-13 |
| 0.01 | 16000 | 1.14512e-13 | 0.00162999037 | 2.29026e-11 |
| 0.03 | 5333.33 | 2.68590e-11 | 0.00163072041 | 1.79061e-9 |

The final outer doubling changes power by0.185% and0.211% for0.01 and0.03. The0.003 point has no independent outer doubling and should not be assigned the same convergence evidence. Its work/flux mismatch is4.41e-5 and exterior flux variation1.65e-5. All eight current checks pass. The absolute-tolerance refinement changes the0.01 power at largest radius by approximately0.030%; small imaginary susceptibilities require more care than apparent solver convergence alone.

The static susceptibility is approximately0.0016298994, consistent with the real response tending to the static limit. All powers are per unit prescribed source amplitude squared and omit the common4pi solid angle, as before. They are not absolute luminosities of a real galaxy.

## Why a fifth power appears

This is a formal matched low-frequency argument, developed after the numerical trend was observed. It has not been promoted to a rigorous uniform scattering theorem.

In a large-radius acoustic region, h~H/r, B=1, and the bending and eta terms are subleading. The radial scalar equation becomes

    sigma''+sigma'/r+(omega²/H) r sigma=0.

Set z=2 omega r^(3/2)/(3 sqrt(H)). The equation is the order-zero Bessel equation, with outgoing solution C H_0^(1)(z). For small z its logarithmic derivative gives

    H r sigma' ~ 3 i H C/pi.

Let sigma0 be the decaying static response to the same source and

    S0=integral_0^infinity r² sigma0(r) dr.

The source has zero total mass. Integrating the driven field equation over an intermediate radius therefore gives the leading dynamic flux relation

    H r sigma' ~ -omega² S0,
    C ~ i pi omega² S0/(3H).

This matching needs a region outside the localized static response but with omega² r³ small. The static Gaussian response decays, and such an overlap expands as omega tends to zero. The ultimate acoustic-to-bending transition is farther out, at r~omega^(-1). Assuming its reflected component vanishes in the low-frequency matching limit, the outgoing acoustic flux carries through to the exterior. The numerical domain studies test this behavior at finite frequencies; they do not prove the assumed uniform limit.

Using the Hankel Wronskian, the angular-normalized acoustic power is

    P = H r² omega Im(sigma* sigma')/2
      = 3H omega |C|²/(2pi)
      ~ pi S0² omega^5/(6H).

The static calculation gives S0=0.0673044195 for the outer60 problem, compared with0.0673044129 at outer30. With H=2, the predicted coefficient of omega^5 is0.00118592109. No coefficient was fitted to the radiation powers.

| omega | numerical power / asymptotic prediction |
|---|---:|
| 0.03 | 0.93203 |
| 0.01 | 0.96559 |
| 0.003 | 0.98441 |

The approach toward one supports this mechanism for the suppression. The trend is not evidence of exact equality at these finite frequencies. Homogeneous vacuum lacks this long-range acoustic region, so its omega^(5/2) result is not a contradiction.

## Consequence for a stable weakly coupled material mode

Use only the diagnostic oscillator of BACKREACTION_RESULT.md. Define the fractional static softening

    epsilon_c=lambda² chi0/(m omega0²), omega0²=k/m.

Static stability requires epsilon_c<1 in that model; the weak-coupling expansion additionally needs epsilon_c small and a regular near-bare pole. To leading order,

    Gamma/omega0 = epsilon_c Im chi(omega0)/(2 chi0),
    amplitude e-folding periods = chi0/[pi epsilon_c Im chi(omega0)].

The measured ratios imply:

| omega0 | Gamma/omega0 divided by epsilon_c | amplitude e-folding periods times epsilon_c |
|---|---:|---:|
| 0.003 | 5.802e-11 | 2.743e9 |
| 0.01 | 7.026e-9 | 2.265e7 |
| 0.03 | 5.493e-7 | 2.897e5 |

For example, at0.01 a genuinely small epsilon_c lengthens the already-large2.265e7-period coefficient. These are conditional dimensionless damping estimates, not measured galaxy lifetimes. Taking epsilon_c near1 is outside the simple weak-coupling estimate and risks a nearly soft mode; it is not an established way around the suppression. A changed source shape, frequency, collective mode or matter action needs a new calculation.

This narrows the radiation proposal: the studied slow, stable, weakly coupled breathing source does not settle quickly through this channel. Faster field modes may behave differently, but cannot be substituted for the actual material dynamics without deriving their coupling.

## Evidence and remaining obligations

low_frequency_run/manifest.json validates and its eight checks pass. LOW_FREQUENCY_CONTRACT.md records the failed initial tolerance and post-probe analytic extension. The prior incoming-boundary mutation in the same response helper already established the sign sensitivity of outgoing dissipation; no new low-frequency mutation was run. The new special-function check verifies Hankel flux normalization at three arguments. The matched asymptotic argument is self-reviewed and its remainder/reflection assumptions remain unproved.

The long domains are mathematical isolated-halo domains. Their physical compatibility with a cosmological exterior has not been demonstrated. Neither this nor the higher-frequency response resolves the finite-background constraint reduction, the live cold-matter selector, observational screening, or derivation of kappa. The next substantive task should derive an actual matter/collective mode and its conservation laws, or identify a different relaxation interaction consistent with the static law, rather than assume that adding radiation closes the theory.
