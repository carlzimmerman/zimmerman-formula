# A photon bath can cool moving carriers, with recoil and a severe rate constraint

2026-10-13. The contact interaction produces negative mean kinetic-energy drift for sufficiently fast carriers in a prescribed isotropic monoenergetic photon bath. It also heats sufficiently slow carriers by recoil. This supplies a conditional cooling mechanism at the single-particle level. It does not supply an achievable bath, a full stationary distribution, condensate preparation or confinement.

## Assumptions and exact angular kernel

Use the previously derived L_int=-C |phi|² F² contact cross section. Photons are unpolarized, isotropic and monoenergetic in the laboratory, with energy omega and number density n_gamma. The carrier moves at speed beta c along z. Stimulated scattering, bath depletion, many-body response and other interactions are absent. Natural units are used below unless specified.

For incident laboratory direction cosine mu, the carrier-rest-frame incident energy and direction are

\[
\omega_*=\gamma\omega(1-\beta\mu),\qquad
\mu_*=(\mu-\beta)/(1-\beta\mu).
\]

Let x be the rest-frame scattering-angle cosine. Then

\[
\omega_*'=\frac{\omega_*}{1+(\omega_*/m)(1-x)},\quad
t=-2\omega_*\omega_*'(1-x),\quad
\frac{d\sigma_*}{dx}=\frac{C^2t^2}{8\pi m^2[1+(\omega_*/m)(1-x)]^2}.
\]

Averaging the final azimuth, the outgoing laboratory photon energy is gamma omega_*' (1+beta mu_* x). Energy conservation makes the carrier energy increment the incoming minus outgoing photon energy. The laboratory collision rate has relative-flux factor (1-beta mu), giving

\[
\dot K=n_\gamma\int_{-1}^1\frac{d\mu}{2}(1-\beta\mu)
\int_{-1}^1dx\,\frac{d\sigma_*}{dx}
[\omega-\gamma\omega_*'(1+\beta\mu_*x)].
\]

For SI event rates, use the SI cross section and multiply the flux by c. Rest-frame kinematics and the contact cross section are checked in the previous photon-recoil package; this turn adds the incident angular and Lorentz-transformed energy average. The azimuth average is valid because the unpolarized scalar amplitude depends only on x and the outgoing energy is linear in the outgoing z projection. This is the exact single-particle drift within this contact/externally imposed bath model, not the full QFT amplitude.

## Soft-photon, slow-carrier limit

Define sigma0=4 C² omega⁴/(3 pi m²). To the first nonzero recoil and velocity orders,

\[
\dot K=n_\gamma\sigma_0\omega
\left[\frac{3\omega}{2m}-4\beta^2
+O((\omega/m)^2,(\omega/m)\beta^2,\beta^4)\right].
\]

Since K approximately m beta²/2,

\[
\boxed{\dot K=-\nu_K(K-K_*),\qquad
\nu_K=8n_\gamma\sigma_0\frac{\omega}{m},\qquad K_*=\frac{3\omega}{16}.}
\]

Cooling is possible above K_*; recoil heats below it. K_* is a zero of the leading conditional energy drift, **not** a proven sharp energy floor, a temperature, or the full stationary distribution. A momentum-diffusion calculation is needed for that distribution. The leading linear drift also closes the mean-energy equation if its regime is maintained, but that does not provide the missing distribution or quantum-degenerate kinetics.

Independent 48- and 80-point angular quadratures find exact-kernel zero-drift K/omega values 0.187500416, 0.187541601, 0.187915975 and 0.191655960 for omega/m=1e-6, 1e-4, 0.001 and 0.01. Heating below and cooling above each root are checked. The results approach the analytic 3/16 limit.

## Rate and annihilation comparison

In SI, writing u_gamma=n_gamma omega as radiation energy density and m c² as carrier rest energy,

\[
\nu_K=\frac{8c\sigma_0 u_\gamma}{mc^2}.
\]

For the **arbitrary, unmeasured** example m=1 MeV, omega=1 eV, C=1e-19 eV^-2, sigma0=1.6526e-64 m². The relaxation rate is 2.4738e-42 s^-1 per J/m³ of radiation energy density. Formally solving this dilute expression for a one-second relaxation time gives u_gamma=4.0424e41 J/m³. That extrapolated density is not a controlled weak-background or feasible operating point; the number diagnoses failure of this illustrative weak-coupling bath proposal. It is not a universal bound on other matched interactions.

While opposite charge signs overlap, compare the relaxation rate with the cold uncorrelated annihilation rate n_opposite a, a=2 C²m²/pi:

\[
\frac{\nu_K}{\Gamma_{\rm ann}}=
\frac{n_\gamma}{n_{\rm opposite}}\frac{16}{3}
\left(\frac{\omega}{m}\right)^5.
\]

The common coupling cancels at this order. For 1 eV photons and 1 MeV carriers, even equality of relaxation and annihilation rates requires n_gamma/n_opposite approximately 1.875e29. This is more restrictive than merely requiring one scattering event before annihilation. Separation changes the local n_opposite; collective/stimulated cooling or other portals require separate models.

## Verification and next step

Fifteen checks pass: separate symbolic recoil/drag coefficients, four exact stationary-target reductions, four quadrature-refined roots, four drift-sign tests and the soft-limit root. The bounded manifest records input hashes and outputs. No new Lean certificate or empirical validation is claimed.

This calculation makes a physical distinction: the existing photon operator can remove kinetic energy, but the tested weak-coupling route has an unfavorable rate and a recoil scale. It does not close the manufacture-to-storage chain. The next discriminating route is an explicit matched interaction with a resonant or otherwise enhanced energy-transfer channel, or a quantitatively derived collective cooling process, rather than an arbitrary damping term appended to the condensate equations.
