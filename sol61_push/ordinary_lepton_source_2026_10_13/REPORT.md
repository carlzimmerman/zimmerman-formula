# Alternative photon source through ordinary lepton loops

2026-10-13. This tests replacing the hypothetical charged scalar messenger in the photon-production vertex with known electrons or muons. The neutral source R and its Yukawa interactions remain hypothetical. The replacement is not Standard Model production of cold energy, and it does not provide a confinement medium.

## Added interactions and matching

Use the alternative low-energy interaction

    L_int = -y_l R lbar l -mu R|Phi|^2,

with a real parity-even R, M_R approximately 2 MeV, and carrier mass m=1 MeV. Retain the stipulated tiny positive pair excess delta=2e-9 eV separately. The isolated-pole source model is the same as before, but the photon vertex now arises from an ordinary charged-lepton loop. No real muon bath is needed for a virtual muon loop.

For tau=M_R^2/(4m_l^2), define

    A_1/2(tau) = 2[tau+(tau-1)f(tau)]/tau^2,
    f(tau) = asin(sqrt(tau))^2                         for tau<=1,
           = -[log((1+sqrt(1-1/tau))/(1-sqrt(1-1/tau)))-i pi]^2/4
                                                            for tau>1.

Then the on-shell width for one lepton species is

    Gamma_gamma = alpha^2 y_l^2 M_R^3 |A_1/2|^2/(256pi^3 m_l^2),
    Gamma_ll = y_l^2 M_R/(8pi) (1-4m_l^2/M_R^2)^(3/2),

with Gamma_ll zero below threshold. The heavy-lepton limit A_1/2->4/3 is checked. Above the electron threshold the photon form factor is complex; it must not be represented as a real local coefficient valid at every momentum.

The source Yukawa alone is a low-energy parameterization. An electroweak completion could use R Lbar H l_R plus its conjugate as a dimension-five operator, but its heavy fields, coefficients and flavor structure are not supplied here. Muon-only couplings require specifying how electron and other couplings are controlled, including radiative mixing and matching. Their absence is not asserted as an exact consequence of the original carrier symmetry.

## Electron loop: a competing decay spoils the old source benchmark

Matching Gamma_gamma=1e-12 eV through electrons requires y_e=1.24442e-6. With the previous Gamma_Phi=1e-12 eV, this gives

    Gamma_ee = 7.82677e-8 eV,
    Br(R -> Phi anti-Phi) = 1.27763e-5,
    lifetime = 8.40953 ns.

The on-pole carrier-production cross section, proportional to Gamma_gamma Gamma_Phi/Gamma_total^2, is only 6.52938e-10 of the original equal-width pole value. This is a peak comparison, not a finite-bandwidth yield. The electron-only replacement therefore fails to preserve the previous source enhancement even though its directly calculated one-loop electron-moment contribution is small, 2.51206e-15.

## Muon loop: a different conditional candidate

At M_R=2 MeV the muon-pair channel is closed. Matching the old photon width requires y_mu=3.42051e-4. The calculated one-loop contribution to the muon magnetic anomaly is 2.14094e-9. It is not justified to advertise this as support from the historical muon anomaly: the cited 2025 theoretical reference differs from older evaluations.

As a weaker-coupling diagnostic, choose y_mu=2e-4 and retune mu to keep the vacuum photon and carrier partial widths equal. The result is

    Gamma_gamma = Gamma_Phi = 3.41884e-13 eV,
    mu = 27.7225 eV,
    rest lifetime = 0.962625 ms,
    Delta a_mu = 7.31955e-10.

Under the same isolated-line, broad-source approximation, the integrated line area is 0.341884 of the previous equal-width area. That is a conditional spectral-area scaling, not a computed inventory or a promise of 34% of the old trapped yield. Actual finite-volume creation, source drift, bandwidth, annihilation and capture have not been recalculated for this alternative.

The magnetic contribution is evaluated from

    Delta a_l = y_l^2/(8pi^2) integral_0^1 dz
                 (1-z)^2(1+z)/[(1-z)^2+(M_R/m_l)^2 z].

Independent double-precision adaptive and 60-decimal integrations agree for each case.

## Dated empirical comparison, not a viability certificate

The [2025 Muon g-2 Theory Initiative update, arXiv:2505.21476v3](https://arxiv.org/abs/2505.21476v3) reports experimental minus Standard Model prediction of 38(63)e-11, using its selected lattice-QCD hadronic-vacuum-polarization average and the final Fermilab result. The reduced y_mu case differs from that reference central value by about 0.56 of its quoted combined uncertainty. This is a one-observable consistency diagnostic; it is neither evidence for R nor a global allowed-region fit. The update itself discusses unresolved differences between hadronic determinations.

No exclusions from vector-mediator NA64 analyses were transferred to this scalar. Applicable scalar beam-dump/missing-momentum searches, radiatively induced electron couplings, stellar production, early-universe thermalization, primordial abundances and photon-coupling bounds remain to be checked. Added invisible carrier decays also change branching fractions assumed in published searches. No cosmological exception is assumed to evade a constraint.

## What changes, and what is lost

This alternative can generate the photon source without a new light electrically charged particle. It avoids the specific charged-scalar vacuum-polarization contribution audited previously. It supplies no replacement for the old messenger wall or cooling reservoir: removing S removes those material assumptions and their useful potential. Confinement must now be independently specified and constrained. The neutral R mass and its tiny positive excess over the carrier pair threshold are still assigned and require radiative matching.

The muon case is a candidate for further constraint checking, not a demonstrated manufacturing route. The electron case is quantitatively disfavored as a drop-in replacement for the narrow source. Neither creates net global carrier charge, produces a verified visible glow, or supplies enhanced gravity.

## Source and execution audit

[Searching for muonphilic dark sectors with proton beams, Phys. Rev. D 106, 035023 (2022)](https://scoap3-prod-backend.s3.cern.ch/media/files/72198/10.1103/PhysRevD.106.035023.pdf), Eqs. (3), (6)–(9), supplies the loop and decay conventions. That paper uses x=1/tau and a loop factor half of A_1/2; the script verifies the translation above and below threshold. Its older phenomenological preference for a muon-anomaly explanation is not imported as present empirical support. The 2025 reference above supplies the separate magnetic-moment comparison.

Nine bounded checks pass: three loop-convention identities, the heavy-lepton limit, two target-width reconstructions, and three independent magnetic-integral comparisons. The run manifest validates. No new Lean certification of QFT, experimental viability, or the overall preparation route is claimed.

Reproduce:

    python3 sol61_push/ordinary_lepton_source_2026_10_13/check.py /tmp/ordinary_lepton_source_results.json

This is a separate model branch from ../charged_messenger_2026_10_13/REPORT.md. Source normalization and the original assigned daughter width are recorded in ../threshold_resonance_2026_10_13/REPORT.md. The research goal remains open.
