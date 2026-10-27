# Radial phonon escape into the finite-shell continuum

This computes inelastic escape contributions, rather than diagonal phase noise,
for the first forty radial elastic modes previously calculated. The resolved
rates are very small relative to the assigned source and tunneling rates. They
are partial sums, NOT an upper bound on total material-induced loss.

## Initial and final particle states

Use the thickest candidate shells: inner/outer radii 0.2/2.2 m and 0.02/0.52 m.
The initial radial wave is the normalized infinite-exterior reference orbital
used in the source calculation. Its narrow finite-shell pole was checked in the
preceding retention package. This approximation is not an exactly stationary
bound state of the finite shell; vacuum exists outside the shell.

The final state is a regular l=0 scattering solution of the FINITE potential:
zero for r<a, U for a<r<b, and zero for r>b. Begin with sin(kr) inside. Propagate
u,u' continuously through the wall using trigonometric functions above the barrier
or hyperbolic functions below it. Outside write

    u_raw(r) = u(b) cos[k(r-b)] + u'(b)/k sin[k(r-b)].

Its asymptotic amplitude is A=sqrt(u(b)^2+[u'(b)/k]^2). Multiply the solution by

    sqrt[2m/(pi (hbar c)^2 k)] / A,
    k=sqrt(2mE)/(hbar c),

where E and m are in eV, k in /m. This gives continuum normalization
integral u_E(r)u_E'(r) dr=delta(E-E') with energies measured in eV. The regular
standing-wave scattering basis is equivalent to summing the radial continuum
final channel; no reflecting exterior boundary or arbitrary box size is used.

## Include density and interface motion in the transition matrix element

For mechanical displacement X*f(r), material conservation gives
V'=-U(f'+2f/r) in the shell, with -U f(a) delta(r-a) and
+U f(b) delta(r-b) at its surfaces. The single-particle matrix element is

    C_E = -U [integral_a^b u_E u_i (f'+2f/r) dr
               +u_E(a)u_i(a)f(a)-u_E(b)u_i(b)f(b)].

Using u_i'=-kappa_wall*u_i inside the material, integration by parts gives

    C_E = U integral_a^b u_i [u_E'-(kappa_wall+2/r)u_E] f dr.

Both expressions are evaluated independently. C_E has units sqrt(eV)/m with
the continuum convention above. This is a one-particle transition; there is no
factor two from the diagonal PAIR frequency formula in the previous package.

For elastic mode omega and mass M_eff from the previous normalization,

    X_zp^2=hbar_SI/(2 M_eff omega),
    E_abs=E_i+hbar omega, E_emit=E_i-hbar omega,
    Gamma_abs = (2pi/hbar_eV) X_zp^2 nB |C_(E_abs)|^2,
    Gamma_emit = (2pi/hbar_eV) X_zp^2 (nB+1) |C_(E_emit)|^2.

Emission is included only for E_emit>0; a free exterior particle must have
positive kinetic energy. Thermal occupation uses T=300 K. These are weak-coupling,
on-shell Golden-rule rates at the discrete mode frequencies. The phonon linewidth
is not integrated. The previous Q=100 phase-noise model is not used to supply
uncomputed off-shell transitions here.

## Resolved contributions

| Candidate | First 10 modes, /s | First 20 modes, /s | First 40 modes, /s |
|---|---:|---:|---:|
| Large cavity | 3.07044e-28 | 3.45781e-28 | 3.65684e-28 |
| Small cavity | 1.00568e-24 | 6.52634e-24 | 1.61076e-23 |

All forty large-cavity emission channels are energetically closed. Seven small-
cavity emission channels are open, with summed contribution 4.79039e-36/s. These
lower-energy final states must penetrate the finite barrier and are strongly
suppressed. Absorption dominates the resolved rates; all evaluated absorption
final energies are above the material barrier.

The forty-mode sums divided by the preceding drive frequencies are 1.91e-22
and 1.00e-17. Dividing by the single-particle tunneling rates gives 1.96e-22 and
1.16e-16. Those comparisons apply ONLY to the resolved radial channels. The
small-cavity sum grows by a factor about 2.47 from twenty to forty modes; it
must not be described as converged, however small its current value is.

## Validation and limits

261 numerical checks pass: inner matching, 384-to-768-point quadrature refinement,
and agreement of full density-plus-interface and integrated-by-parts matrix
elements for all 87 open transitions. The continuum normalization is derived
analytically from the asymptotic scattering amplitude; these checks do not turn
that derivation into a formal proof. Input mode masses, frequencies and geometry
are pinned in the bounded-run manifest. No new Lean certification is claimed.

Unlike the diagonal phase problem, angular symmetry does NOT restrict all loss
to radial mechanical modes. A mechanical mode of angular momentum l can connect
the initial s-wave to final particle partial wave l. Those channels, higher radial
modes, finite phonon linewidths, real material defects and nonthermal fluctuations
are absent. Approximating the initial narrow resonance by a normalized reference
orbital is another stated limitation, especially for exponentially small channels.

This advances the loss calculation from a bulk reference to finite-shell particle
scattering states. It does not establish total storage lifetime or a realized
creation apparatus. The next required extension is an angularly complete elastic
response or a justified bound on its omitted contribution. The optical setup,
readout and identification with the repo's cosmological cold component also
remain unresolved. The overall creation objective stays open.
