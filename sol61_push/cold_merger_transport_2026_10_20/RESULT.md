# Actual ARGON merger-energy reservoir and dwarf transport gates

20 October 2026. **A candidate stationary branch in the actual ARGON action has a positive merger-energy gap. Its size can cover the optimistic dwarf outflow energy requirements while respecting the declared mass allocation. The transfer of galactic orbital angular momentum, selective escape and stellar survival remain unconstructed.** This is a substantial energy-supply checkpoint, not a completed formation mechanism.

## 1. New microscopic calculation

We solved coupled spherical isolated profiles of the exact ARGON11 two-field action, M=100, Lq=1.99, a=200. Both field gradients are retained. The charge convention and Hamiltonian match `frag3d.c` at `07546091c`. This is a new stationary calculation, independent of the periodic-box fragmentation medians.

| Charge | Stationary energy | E/Q |
|---:|---:|---:|
| 80,000 | 76,157.983363 | 0.9519747920 |
| 160,000 | 149,338.139064 | 0.9333633691 |

The candidate-branch gap is

    2 E_stat(80000) - E_stat(160000) = 2977.827663,
    gap / initial pair energy = 0.01955033164.

Thus two such reference fragments could release **1.955% of their initial profile energy if they reach the tested combined stationary state**. This is stronger evidence than simply E/Q<1: the function E(Q)=0.95 Q has zero merger increment despite being bound relative to free particles.

The isolated calculation passes box/tolerance, integrated-charge, virial and dE/dQ=omega checks. It does not prove a global minimum, nonlinear/nonradial stability, a merger rate or the emitted energy/J/Q spectrum. An excited or rotating remnant can retain part or all of the stationary-state gap. The ratio is invariant under a common dimensional energy scaling; identifying the galactic cold stock with these ARGON lumps is still a separate model bridge. ARGON is also distinct from the original charged-daughter production theory.

Full equations, conventions and diagnostics: [isolated binding report](isolated_binding/RESULT.md). The profiles can be regenerated from `isolated_binding/solve.py` and `solve_v2.py` with their saved contracts and manifests.

## 2. Why compact mergers need more than ordinary cold outflow energy

Use the same four pinned reference endpoints as the preceding collision packet: canonical B0/G1/C, phiK=1/lambda_c=1 diagnostics from CFG918 `bb9b20525`; Fornax/Leo I use the previous global stellar-upper-guard receivers. These are fixed conditional targets, not an observationally fitted assembly history.

For matter with total escaping rest mass m, all relevant nonrelativistic orbital kinetic energy K, and positions within radius r about the dwarf centre,

    |J_orb| <= r sqrt(2 m K).

The relativistic capacity used in the code is r sqrt(2mK + K^2/c^2). This concerns orbital J carried by matter; intrinsic fragment spin and radiation need separate ledgers. The bound deliberately favors perfectly aligned transport.

The saved K_B is at the outer receiver, so a launch calculation must include the potential climb. In the explicitly assumed static surviving spherical field and expanding thin-wind-shell closure, for r >= core cutoff R,

    Phi_b(r) = -G Mstar/sqrt(r^2+a_star^2)
               -G(s Mstar+Mcore)/r -G M_A/max(r,r_A),
    K(r) = K_B + m[Phi_b(r_B)-Phi_b(r)]
                    + G m^2/2 [1/r-1/r_B].

No later torque, radiative loss or time-dependent work is included in this propagation model. The potential difference is independently checked by enclosed-mass quadrature.

| Dwarf | Core cutoff R, kpc | Minimum last-torque radius under static old-energy closure, kpc | Compact-core orbital J capacity / required |
|---|---:|---:|---:|
| Draco | 0.258 | 2.171 | 0.2004 |
| Sextans | 0.648 | **13.485** | **0.04856** |
| Fornax | 0.927 | 13.084 | 0.1368 |
| Leo I | 0.305 | 6.213 | 0.1026 |

Sextans' reference escaping mass is 291,026.63 solar masses. Its residual J is 5.04005e11 solar-mass pc km/s and outer K_B=2.39871e9 solar-mass (km/s)^2. Transporting that J at the core edge requires tangential speed about **2673 km/s**, compared with the reference outer wind speed 128.39 km/s. The potential correction raises available launch kinetic energy by only 2.24%.

Consequently a compact merger supplying only the old gravitational outflow energy cannot implement the earlier large-radius J capacity. It needs outward angular-momentum transfer at halo scales, additional directed kinetic power, or another explicitly accounted channel. This is not a no-go for evolving potentials, coherent field torques, intrinsically spinning escapers or a new binding-energy source.

## 3. Include binding release without double counting mass or energy

Merger binding changes rest energy. We therefore tested an explicitly extended, optimistic ledger rather than adding power while keeping the old wind K and masses unchanged. Hold the final core and receiver A fixed; let a total rest-energy defect delta reduce the noncore rest allocation:

    m_new = m_old - delta,
    E_orb,new = E_orb,old + eta delta c^2,

where eta is the fraction going to wind orbital kinetic energy. Any remaining energy must leave in another accounted channel. The retained core/charge allocation is assumed compensable; the actual field process must establish it.

At ideal eta=1, Sextans' orbital capacity at the core edge requires a minimum defect of approximately **11.54 solar masses**, leaving about **291,015.09 solar masses** of material wind. The defect is 4.55e-7 of the initial free cold mass. This is a necessary best-case capacity threshold, with optimal matter-J alignment, not an actual merger yield.

If the tested stationary gap were fully available, about **590 solar masses** of initially bound fragments would have to participate to provide that lower-bound energy. Their merger remnant, charge, radiation and mass loading must still be accounted for. Randomly releasing the energy does not establish the required directed J.

The finite noncore budget also limits inefficient channels. Allowing an arbitrary defect within that budget gives an ideal orbital-efficiency floor near 1.588e-4, attained by consuming about half the noncore rest allocation. This is a mathematical budget extremum, not a proposed physical operating point. Its uniqueness follows from the positive second derivative of the threshold numerator; an independent stationary-root calculation checks the numerical minimizer.

## 4. A shared budget example across all four dwarfs

We tested the same hypothetical rest-defect fraction epsilon in every dwarf on the declared grid 1e-8, 1e-7, 1e-6, 2e-6, 1e-5. No separate release efficiency was fitted per dwarf. All release goes to wind orbital energy, retained profiles stay fixed, and added stellar heating is set to zero. This is intentionally a capacity example.

For a uniform spherical shell with constant momentum magnitude, the optimally signed azimuthal contribution carries J=(pi/4)r P_t. Using that more restrictive angular factor, epsilon=2e-6 is the first tested common point passing the mass and instantaneous launch-J gates in all four systems. Conditional on the full stationary gap becoming usable, it corresponds to processing 0.01023% of the initial free mass in every dwarf.

| Dwarf | Rest defect, solar masses | Remaining wind rest mass, solar masses | Powered launch speed, km/s |
|---|---:|---:|---:|
| Draco | 55.45 | 13,486,711 | 860 |
| Sextans | 50.79 | 290,976 | 5602 |
| Fornax | 1980.58 | 390,936,606 | 957 |
| Leo I | 376.87 | 78,837,278 | 929 |

This example demonstrates room in the common energy/rest-mass budget. It does not predict those speeds or that processed fraction. The spherical launch state and the later spherical thin-shell propagation closure are not a demonstrated trajectory; an evolving wind can become nonspherical. The required angular bias, merger processing, energy partition and charge flux are still assumed.

Holding core/A profiles fixed while slightly reducing distant B mass cannot increase the static stellar gravity. Thus the example does not add a new static mass enhancement to Fornax or Leo I. **It does not prove non-overboosting during formation:** the old global upper guards were close to saturation, actual stellar heating/re-equilibration is not computed, and the half-light-aperture projections already exceed catalogue central values. The separate Sextans global C-profile stock ceiling also remains. These observational-profile issues must be resolved before any budget example is called a four-dwarf fit.

## 5. Isotropic cooling is insufficient to supply galactic orbital J

If an entire escaping ensemble has zero net momentum and zero intrinsic J in each emitter's COM frame, Lorentz transformation gives

    P_escape = (E_escape,lab/c^2) V_emitter,
    J_orb,escape = (E_escape,lab/c^2) R_emitter cross V_emitter.

This applies to energetic matter as well as radiation under those hypotheses. At emitter radii <=R and bulk speeds <=2 sigma, Sextans' isotropic outflow in the common epsilon=2e-6 example carries only about **0.55%** of the needed orbital J. All four isotropic cases fail across the tested energy grid. The process must generate an escaping-subset bias, anisotropic recoil, intrinsic/multipole J or a separate torque; those possibilities are not excluded by this branch test.

For cold escapers, the conditional positive-energy causal size bound S<=E a/c would require a spin-carrying radius at least about **5.78 pc** to store all Sextans' residual J intrinsically in its allowed wind mass. The illustrative ARGON R1 radius at m_h=1 MeV is microscopic, about 3.6e-29 pc. That comparison does not exclude all mass spectra or extended rotating states, and the source's geometric core radius is not a rigorous support radius.

The saved radiation budget J<=rE/c applies only to particle-like freely propagating packets whose orbital J is set at that radius. **It is not a universal bound on radiation from a compact coherent emitter.** Multipole waves and extended near fields require a mode-resolved J/E calculation. In particular, a wave mode can have J/E=m/omega. The raw directed-packet number, about 2595 solar-mass rest-energy equivalent for Sextans, must not be used to exclude those wave channels.

Related literature supplies useful analogies, not an ARGON transport coefficient. A distinct SU(N) model exhibits vortex-dependent energy retention and vortex ejection in mergers; this makes remnant spin and emitted J essential observables. [Dvali et al., PRL 132, 151402 (2024)](https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.132.151402). A separate MSSM study measures fusion and geometric cross sections separately, reinforcing that geometric area alone is not the merger kernel. [Multamaki and Vilja, hep-ph/0005162](https://arxiv.org/abs/hep-ph/0005162).

## 6. Claude check, evidence and next physical test

ARGON11's pinned source/result files are unchanged: its periodic-box lumps coarsen, but it has no matched isolated-pair merger flux, angular-momentum ledger or phase/impact-averaged kernel. The new isolated stationary calculation in this packet is the relevant additional evidence. CFG926 finalized at `a15a87fb7`: its conditional red-lens IMF correction leaves the primary dwarf masses unchanged; its framework fossil-a0 choices do not rescue them.

**Fresh arrival during this calculation:** CFG928 results `82a69be8f`, README `ecf49d770`, conditionally revive P2's **galaxy-scale static score** after applying the full red-lens IMF correction and withholding the cluster facts. P2 still fails on all facts, is FRAGILE under the V7 reading and C1-DEPENDENT on the canonical footing under weaker IMF corrections. P4 becomes galaxy-scale UNDERDETERMINED. This revises the selector assessment from the earlier uncorrected CFG921 framing; it is not new physical capture evidence.

CFG928 reuses the dwarf calibration exactly: maximum calibration change zero, v2 about 6.95/6.46 km/s. It changes red-lens scoring and the facts included in the galaxy-scale grade. Its dwarf mass-to-light, gas and Wolf conventions do not refit our SFH/capped-retained endpoints. No measured merger kernel, cooling, charge/J flux or retention dynamics was added. A percent-level stationary binding gap alone does not derive a capture cutoff at several km/s: that scale requires the actual phase/impact-dependent dissipation/capture process. The sealed UDG prediction is a future static-selector test. No new source result closes the four-dwarf formation mechanism.

Five bounded runner-v2 records complete and validate: root runs 001/002/003 have 61/49/20 checks; isolated runs 001/002 have 23/19. Total **172 checks**, peak measured RSS **126.7 MB**. Checks support the stated finite calculations and identities, not a theorem about every merger or a proof of stable physical formation. Source revisions and hashes are in `sources.json`; the complete statements and caps are in the contracts. A separate peer reconstructed the orbital/rest-defect bounds and the static solver's action normalization was checked against the source Hamiltonian.

The best next discriminating work is a matched isolated-pair experiment using the saved action/profile conventions. Vary relative phase and impact parameter independently. Measure E, Q, vector orbital J, intrinsic J, remnant excitation and outward flux separately, including coherent angular modes. Report the branching efficiency from the stationary gap into escaped matter/radiation and the correlation of that flux with the parent orbital direction. Do not infer a torque from declining lump counts.

If direct mergers remain isotropic, test the two-scale route explicitly: transfer J outward through fragment encounters or gravitational/field stresses while the envelope is extended, then use merger energy for escape. The fixed old-energy case supplies a quantitative last-torque target near 13.5 kpc for Sextans. Recompute that target only after the stellar-selection likelihood and permissible core/outer mass profile are fixed.

No 3D field evolution, live Claude experiment, frozen criterion, publication, shared CE-FM-093 pointer, external push or message to another chat was changed. The physical formation and full theory remain open.
