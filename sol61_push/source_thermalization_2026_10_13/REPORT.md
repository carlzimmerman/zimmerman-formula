# Source thermalization and an entropy diagnostic

2026-10-13. This audits a cosmological consequence of the source couplings
already assigned in ../ordinary_lepton_source_2026_10_13/REPORT.md and
../electron_material_wall_2026_10_13/REPORT.md. It does not assume that the
hypothetical source or carrier has been discovered.

## Explicit background assumptions

Assume a hot radiation-dominated universe described by the ordinary Friedmann
equation, reheating above 3 MeV, a thermal electromagnetic bath, and no additional
large energy component or entropy injection. Take the previously calculated
vacuum source widths and neglect their finite-temperature corrections. The
source has MR=2 MeV; the electron-wall branch uses |ye|=1e-8, while a separate
comparison sets ye=0 and retains only the muon-induced photon width.

These are physical assumptions, not assumption-free consequences of data.
The analysis is conditional on them. It does not establish the repository's
alternative gravitational/cosmological completion or silently rule it out.

## Relaxation against cosmic expansion

For a Maxwell-Boltzmann distribution of the parent, averaging its time-dilated
vacuum decay rate gives

    Gamma_relax(T)=Gamma_channel*K1(MR/T)/K2(MR/T).

The Bessel ratio is independently obtained by averaging MR/E over the momentum
distribution. Detailed balance relates this decay average to the inverse-decay
term driving R toward the electromagnetic equilibrium distribution. In a kinetic
equilibrium approximation the channel contributes

    dnR/dt+3H*nR = -Gamma_relax*(nR-nR_eq).

Other dark-sector channels add terms; this equation is not the full coupled
system. Its ratio to H tests whether the electromagnetic interaction may be
neglected, not whether every species has a thermal distribution.

Using the unreduced Planck mass M_Pl=1.220890e28 eV,

    H=sqrt(8pi^3*g_rho/90)*T^2/M_Pl.

The diagnostic g_rho includes photons, finite-mass electrons/positrons, three
massless neutrino species at the same temperature, and an equilibrium real R.
Including R makes the expansion estimate self-consistent with the proposed
near-equilibrium state; omitting it changes H modestly. No phi population is
included in this diagnostic expansion rate.

| T | H | Photon channel, ye=0: Gamma_relax/H | Electron channel alone, coupling magnitude 1e-8: Gamma_relax/H |
|---:|---:|---:|---:|
| 1.5 MeV | 1.579/s | 146.1 | 2160 |
| 2 MeV | 2.817/s | 68.30 | 1010 |
| 3 MeV | 6.357/s | 22.58 | 333.8 |

The electron channel alone reaches rate equality at |ye| about 3.15e-10 at
2 MeV. This is NOT a decoupling bound for the whole source: the muon-loop photon
channel remains even at ye=0. Smaller electron coupling therefore does not by
itself make the assigned source cosmologically inert.

For the weak-electron, retuned benchmark, its tiny carrier partial width does
not invalidate the fast electromagnetic replenishment conclusion. For the
original muon-only equal-width source, carrier production and inverse reactions
must be solved together: the electromagnetic rate above does not prove that
R independently follows its equilibrium density while continuously losing
particles into an initially empty dark sector.

## Size of the entropy effect in an explicitly simplified model

To expose a possible observable consequence, assume neutrinos decouple
instantaneously at a chosen Td and subsequently receive no entropy. Assume R
stays equilibrated with the electromagnetic bath and its entropy ultimately
returns entirely to photons/electrons. Omit the carrier bath in this toy model.
Define s_i=(2pi^2/45)*g_s,i*T^3. Bose-Einstein and Fermi-Dirac momentum integrals
give g_s,R and g_s,e including masses. Electromagnetic entropy conservation then
implies

    (Tnu/Tgamma)^3_final=2/[2+g_s,e(Td)+g_s,R(Td)],
    Neff_inst=3*{5.5/[2+g_s,e(Td)+g_s,R(Td)]}^(4/3).

The factor 5.5 follows from the conventional (4/11)^(1/3) neutrino temperature
used to define Neff. The same approximation without R provides the comparison
baseline; finite electron mass makes that baseline slightly larger than 3.

| Assigned Td | g_s,R | Instantaneous baseline without R | Instantaneous result with R only |
|---:|---:|---:|---:|
| 1.5 MeV | 0.7832 | 3.0321 | 2.5356 |
| 2 MeV | 0.8633 | 3.0180 | 2.4828 |
| 3 MeV | 0.9321 | 3.0080 | 2.4404 |

This temperature scan is a sensitivity diagnostic, not a uncertainty interval
or a precision prediction. The additional electromagnetic entropy lowers the
neutrino-to-photon temperature in this model. It is a concrete reason to solve
the full thermal history rather than assume the small laboratory coupling makes
the source invisible to cosmology.

For dated observational context, [Planck 2018 cosmological parameters](https://arxiv.org/abs/1807.06209)
reports Neff=2.99+-0.17 with BAO in its stated model extension. That is a
model-dependent cosmological inference, not a direct assumption-free count of
neutrinos. No significance or confidence limit is computed by comparing this
precision result with the instantaneous-decoupling numbers above.

## What must replace the toy model

[Escudero, arXiv:1812.05605v4](https://arxiv.org/pdf/1812.05605v4), 6 September
2019, develops coupled electromagnetic/neutrino temperature evolution and
explains why instantaneous entropy estimates are inadequate for precision work.
Its general discussion supports this workflow; its published thermal dark-matter
mass limits are not directly applied to our unstable mediator and nonequilibrium
carrier sector.

A valid constraint calculation must include continuing neutrino-electron energy
transfer, the source's finite-temperature rates and spectral changes, carrier
production and inverse reactions, their energy density, and any declared
nonstandard expansion or initial conditions. Source thermalization is not by
itself proof of a forbidden cosmology. Nor may a low reheating temperature,
new neutrino coupling or entropy injection be assumed solely to evade it.

The standard hot-history benchmark cannot presently be advertised as viable.
The new evidence is that even the retained weak source has fast electromagnetic
interactions at the relevant epoch, and an equilibrium source can alter the
entropy accounting substantially. This remains a conditional constraint screen,
not a verified exclusion or a manufacturing mechanism.

## Numerical audit

Eleven checks pass: two massless thermodynamic normalizations, Bose/Fermi
entropy integrals compared to independent Bessel sums at three temperatures,
and three direct momentum averages reproducing K1/K2. Integrals stop at
momentum/T=100; Bessel sums contain 400 terms. The stated masses keep the
truncated tails negligible relative to the 1e-10 comparison tolerance. The
manifest hashes both inherited model inputs. No new Lean theorem or empirical
certification is claimed.

Reproduce:

    python3 sol61_push/source_thermalization_2026_10_13/check.py /tmp/source_thermalization_results.json
