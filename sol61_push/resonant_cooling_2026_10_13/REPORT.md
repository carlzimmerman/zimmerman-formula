# Radiative recycling: two emission stages and the low-temperature limit

2026-10-13. **The glow-plus-gravity mechanism remains open.** This checkpoint derives conditional collision rates for the already hypothetical photon portal. It identifies radiative source formation as a second cooling channel, and distinguishes the exponentially suppressed on-shell contribution from a power-law off-shell tail. Neither is evidence that the carrier or photon interaction exists.

Base publication: `8286c5061b4821d71f2c4ba298a2312e8c337c11`. The prior derivation is pinned in `INPUT_RADIATIVE_REPORT.md`.

## Regime and target

The intended microscopic link is loss of carrier kinetic energy to escaping photons, potentially reducing pressure support and permitting ordinary self-gravity to concentrate existing matter. The force would arise from changed mass distribution. Emitting light does not create mass or an enhanced gravitational coupling.

Use natural units, daughter mass \(m\), source mass \(M=2m+\delta\), ordinary vertex \(g\chi^*\phi^2+\mathrm{h.c.}\), and the added interaction

\[
-\frac{\zeta}{4\Lambda^3}(\chi^*\phi^2+\mathrm{h.c.})F_{\mu\nu}F^{\mu\nu}.
\]

Assume \(T,\delta\ll m\), a dilute Maxwell–Boltzmann daughter gas, weak coupling, narrow source width, negligible source inventory, and sufficiently rapid elastic rethermalization. Photons escape without significant inverse absorption or stimulated emission. These are conditions to be established for an apparatus, not measured facts. In particular, this gas calculation cannot simply be applied to the coherent high-occupation simulations in earlier packages.

The gas degeneracy parameter is
\(\eta=n(2\pi/(mT))^{3/2}\ll1\).
At fixed density it increases as the gas cools. All extrapolations must stop or change kinetic descriptions when that assumption fails.

## Ordinary formation followed by radiative decay

For \(\phi\phi\to\chi\to\phi\phi\gamma\gamma\), detailed balance in the nonrelativistic dilute limit gives the source-formation event rate per volume

\[
R_{\rm form}=n^2K(T)\Gamma_0,\qquad
K(T)=\left(\frac{2\pi}{T}\right)^{3/2}\frac{M^{3/2}}{m^3}e^{-\delta/T}.
\]

The corresponding identical-pair cross-section convention is
\(R_{\rm form}=n^2\langle\sigma v\rangle/2\).
The factor 1/2 is not an additional factor to insert after using detailed balance.

For ordinary and radiative widths \(\Gamma_0,\Gamma_\gamma\), and no other channels, define

\[
\lambda=\frac{\Gamma_0\Gamma_\gamma}{\Gamma_0+\Gamma_\gamma},\qquad
R_d=n^2K(T)\lambda,\qquad
\mathcal P_d=n^2K(T)\lambda\frac{16\delta}{19}.
\]

The prior spectrum supplies mean radiated energy \(16\delta/19\) per radiative decay. In this *completed collision cycle*, that energy comes from the incoming pair's kinetic energy; ordinary source formation requires relative energy near \(\delta\). To leading order recoil does not change the center-of-mass kinetic energy significantly.

For this channel,

\[
0\le\lambda\le\min(\Gamma_0,\Gamma_\gamma).
\]

Making \(g\) small raises the radiative branching fraction but reduces formation. It does not produce unlimited recycling. Quasi-steady elimination of the intermediate population additionally requires fast source relaxation and \(nK\Gamma_0/(\Gamma_0+\Gamma_\gamma)\ll1\).

For thermal energy density \(u=3nT/2\), the decay-side cooling time is

\[
t_d=\frac{57}{32}\frac{T}{nK\lambda\delta}.
\]

An independent finite numerical check compares the nonrelativistic thermal factor with the exact classical relativistic expression

\[
K_{\rm rel}(T)=\frac{2\pi^2M^2}{m^4T}
\frac{K_1(M/T)}{K_2(m/T)^2},
\]

which includes thermal time dilation. Scaled Bessel functions avoid exponential underflow. This verifies the stated limiting normalization; it does not establish a Maxwellian gas experimentally.

## A second channel: photons emitted during formation

The same operator also permits
\(\phi\phi\to\chi\gamma\gamma\), followed by ordinary \(\chi\to\phi\phi\). It must not be omitted from the cooling analysis. Let \(E\) be incoming relative kinetic energy and \(\Delta=E-\delta>0\). Neglecting heavy-source recoil, phase-space integration gives

\[
\boxed{\sigma v_{\rm assoc}(E)
=\frac{\zeta^2\Delta^7}{1680\pi^3M m^2\Lambda^6}}.
\]

The normalization includes the two identical-photon factor and incident flux. One can reproduce it from the contact polarization sum \(8\zeta^2E_1^2E_2^2(1-\mu)^2/\Lambda^6\), the angular integral \(64\pi^2/3\), and \(\int_0^\Delta E_1^3(\Delta-E_1)^3dE_1=\Delta^7/140\). Relativistic phase-space conventions are as in the [PDG kinematics review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf). That source does not establish this hypothetical interaction.

The Maxwellian relative-energy density is
\(p_T(E)=2\sqrt E\,e^{-E/T}/(\sqrt\pi T^{3/2})\).
Multiplying by the probability that the new source returns through ordinary decay gives

\[
\mathcal P_a=\frac{n^2}{2}\frac{\Gamma_0}{\Gamma_0+\Gamma_\gamma}
\int_\delta^\infty p_T(E)\,\sigma v_{\rm assoc}(E)(E-\delta)\,dE.
\]

If the source instead undergoes radiative decay, another emission occurs. That higher radiative contribution is not included in this two-channel approximation. The numerical benchmarks with ordinary branching approaching one suppress that correction. The result is not a general branching-cascade solution.

Writing \(\theta=T/\delta\), using \(M\simeq2m\) in the leading thermal prefactor, and \(\mathcal B_3=\Gamma(4)^2\Gamma(3/2)/\Gamma(19/2)\),

\[
\frac{\mathcal P_a}{\mathcal P_d}
=\frac{19}{2240\mathcal B_3}
\int_0^\infty y^8\sqrt{1+y}\,e^{-y/\theta}\,dy.
\]

| \(T/\delta\) | Association cooling / decay-side cooling |
|---:|---:|
| 1 | \(3.9991\times10^6\) |
| 0.5 | 5804.09 |
| 0.2 | 1.08946 |
| 0.1 | 0.0017573 |
| 0.02 | \(7.11\times10^{-10}\) |

This substantial correction is a consequence of integrating the warm high-energy tail against a rapidly increasing radiative matrix element. It is not a new measured enhancement. At \(T=\delta\), association photons carry a mean total energy \(8.4416\delta\), rather than \(16\delta/19\). For a 5 eV gap much of that output is above visible photon energies. More cooling power does not automatically mean a comfortable visible glow.

The two narrow resonances correspond to distinct intermediate invariants. Summing their factorized contributions is a leading narrow-width approximation. The fully coherent intermediate-temperature amplitude, including interference and off-shell contributions, has not been integrated here.

## Off-shell cooling does not stop exponentially

Away from either on-shell source, the same tree process has two attachments: the photon portal at decay and at formation. In the leading nonrelativistic notation their propagator sum is proportional to

\[
\frac{1}{E-\delta+i\Gamma(E)/2}
+\frac{1}{E_f-\delta+i\Gamma(E_f)/2},
\]

where \(E_f\) is final daughter relative kinetic energy, with recoil corrections neglected. At \(E,E_f\ll\delta\), the amplitudes add and give approximately four times the rate of the decay-side attachment alone. The separate subthreshold integration confirms approach to that factor: at \(E/\delta=10^{-5}\), the cooling-weighted ratio is 3.9999657. Dropping one attachment is not a full scattering calculation.

For diagnostic purposes `kernel_cases` in the results integrates the **decay-side attachment only** over all incoming energies, with running widths proportional to \(\sqrt E\) and \(E^{17/2}\). The JSON names `full_over_narrow_*` mean the full energy integral of that one attachment, not the full two-diagram process. Its cross section is

\[
\sigma v_d(E)\simeq
\frac{g^2\Gamma_\gamma(E)}{4m^3[(E-\delta)^2+\Gamma(E)^2/4]}.
\]

At low temperature the off-shell limit yields

\[
R\propto T^{17/2},\qquad
\mathcal P\propto T^{19/2},\qquad
\langle E_{\gamma\gamma}\rangle\simeq\frac{160}{19}T.
\]

The second attachment changes the leading normalization by four, not these powers or the leading energy ratio. The rate becomes very small but has a power-law tail rather than the on-shell Boltzmann exponential. At \(T/\delta=0.002\), the decay-side numerical mean emitted pair energy is \(0.016911\delta\), close to the limiting \(0.016842\delta\). For \(\delta=5\) eV, the mean photon energy is about 0.042 eV: far infrared. This is a mean, not a hard spectral cutoff.

## Physical benchmarks with the classical regime enforced

Choose \(\delta=T=5\) eV, \(\zeta=1\), \(\Lambda=10M\), and \(\eta=10^{-4}\). Density is derived from that small phase-space occupancy, rather than taking an inadmissibly dense gas and applying classical rates. Let ordinary branching approach one to obtain the most optimistic rate within these two factorized pole contributions. The resulting conditional lower cooling times are:

| Daughter rest energy | Mass density, kg/m³ | Two-pole cooling time, s | Cooling time / \((4\pi G\rho)^{-1/2}\) |
|---:|---:|---:|---:|
| 1 keV | \(5.2083\times10^{-13}\) | \(1.4596\times10^{15}\) | \(3.05\times10^4\) |
| 12.5 keV | \(2.8772\times10^{-10}\) | \(2.4214\times10^{23}\) | \(1.19\times10^{14}\) |
| 1 MeV | \(1.6470\times10^{-5}\) | \(4.5357\times10^{37}\) | \(5.33\times10^{30}\) |

These improve substantially on a decay-only estimate, yet remain much slower than the quoted gravitational timescale. That timescale alone does not prove a cloud is unstable or collapses: size, pressure, confinement and geometry also matter. The table is not a universal lower bound including all diagrams, arbitrary couplings, quantum stimulation or other interactions. There is no experimentally established parameter selection here.

## Verification and remaining gap

The script passes 40 finite checks, including refinement of 12 decay-side thermal kernels, nine exact-classical versus nonrelativistic thermal comparisons, the low-energy two-attachment limit and width-bottleneck checks. Association thermal integrals and physical tables are evaluated in the same recorded run; their formula normalization is analytically self-reviewed, not independently certified by those 40 checks.

Three Lean statements certify the algebraic bottleneck bounds and branching-factor identity. The collision kernel, matrix elements, spectra, detailed balance and integrals are **not** Lean-certified. Both damaged controls were rejected, and both successful run manifests validate against their current inputs and outputs. This is self-reviewed work with no independent agent review.

The surviving candidate is radiative collisional cooling followed by ordinary gravitational redistribution, under an unvalidated photon interaction. The next unresolved physical regime is the high-occupation gas: it requires Bose factors, coherence/dephasing and photon escape in a conserving kinetic description. The dilute formula cannot be scaled to arbitrarily large density. A full two-diagram thermal integral would refine intermediate temperatures, but cannot by itself establish the missing dense-state dynamics or a macroscopic force.

Reproduction: run `check.py` with an output JSON path. Contracts and `run/manifest.json` and `lean_run/manifest.json` pin actual inputs, commands, bounds, software versions and outputs. No new interaction was silently added beyond the explicitly hypothetical portal inherited from the prior report.
