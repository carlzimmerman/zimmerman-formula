# Heavy messenger: photon coupling, perturbative control and charged-particle searches

2026-10-13. Raising the messenger mass can reduce the electron-moment contribution, but cannot preserve the old source and wall calculations without changing other parameters. This audit combines a necessary tree partial-wave screen with a conditional comparison to a primary collider result. It does not provide a global exclusion or a viable heavy-messenger apparatus.

## Fixed photon coupling in the chosen scalar family

The previous leading one-loop matching for a single unit-charge complex scalar is

    g_gamma = alpha A/(12pi M_S^2).

The explicitly chosen nonnegative messenger potential imposes

    lambda_RS >= A^2/(2M_S^2).

This inequality is sufficient for that chosen square-completed family, not necessary for every stable scalar theory. For high-energy elastic R S -> R S scattering, the contact term gives Mcal=-lambda_RS. R and S are distinguishable; in the convention Mcal=16pi sum_l (2l+1) a_l P_l,

    a_0 = -lambda_RS/(16pi).

Imposing the usual necessary tree perturbative-unitarity screen |Re a_0|<=1/2 yields lambda_RS<=8pi. Cubic exchange contributions vanish in the asymptotic contact limit. This is one necessary channel check, not a full coupled-channel or finite-energy unitarity proof; couplings at this ceiling need not be weak. Running couplings and a finite ultraviolet cutoff can change how an asymptotic tree diagnostic should be applied.

Combining these assumptions at fixed g_gamma gives

    lambda_RS >= 72pi^2 g_gamma^2 M_S^2/alpha^2,
    M_S <= alpha/(3 sqrt(pi) |g_gamma|).

For the old g_gamma=5.013256549e-15 eV^-1, the resulting necessary ceiling is 273.7469 GeV.

| M_S | Required minimum lambda_RS | Absolute contact a_0 |
|---:|---:|---:|
| 100 GeV | 3.354 | 0.0667 |
| 200 GeV | 13.42 | 0.2669 |
| 300 GeV | 30.18 | 0.6005 |
| 520 GeV | 90.69 | 1.804 |
| 600 GeV | 120.7 | 2.402 |
| 1000 GeV | 335.4 | 6.672 |

Thus keeping the old photon coefficient while moving to several hundred GeV is outside this perturbative screen for this model family. This is not a statement that quantum mechanics fundamentally forbids heavier particles or a weaker source.

## Relevant collider result and the mapping that would be required

[CMS, arXiv:2410.09164v2](https://arxiv.org/pdf/2410.09164), published in JHEP 04 (2025) 109, reports an ionization-method mass reach of 0.52 TeV for stable, directly produced right-handed tau sleptons; the mass-method value is 0.51 TeV. The discussion following Fig. 6 distinguishes these from left-handed, mass-degenerate and cascade-production cases. No significant excess is reported. The numerical reach is a 95% confidence result within that signal model.

For comparison, S could be embedded as a colorless SU(2) singlet of unit electric charge (or its conjugate), with the same photon and Z gauge couplings as a right-handed charged slepton. The displayed S interactions conserve S number and introduce no decay channel. Under matching stability, production kinematics and charged-track response, the direct slepton search is pertinent. The repository previously specified only a QED-level scalar, so this electroweak embedding and detector mapping are additional assumptions. No detector recast has been performed. Extra interactions or different lifetimes require reassessment.

The CMS signal samples discussed in the paper start at 200 GeV. Do not extend the quoted reach into a blanket exclusion of every mass from MeV to 520 GeV. Lower-mass collider and fixed-target coverage has not been assembled here. The point is narrower: moving above the quoted 520 GeV reach cannot preserve the original g_gamma within our chosen tree perturbative screen. Even a point above 520 GeV is not certified allowed by all other searches.

## A weaker photon source changes the wall as well

One may lower A to keep lambda_RS modest. At eta=0 in the square completion, A=sqrt(2lambda_RS) M_S. Then g_gamma scales as sqrt(lambda_RS)/M_S and the photon partial width scales as lambda_RS/M_S^2. Retuning mu so that the vacuum daughter and photon partial widths remain equal gives the following diagnostics at M_S=600 GeV:

| lambda_RS | Gamma_gamma (eV) | mu (eV) | Equal-width broad-spectrum line area / old area |
|---:|---:|---:|---:|
| 0.1 | 8.2824e-16 | 1.3645 | 8.2824e-4 |
| 1 | 8.2824e-15 | 4.3149 | 8.2824e-3 |

The area ratio assumes an isolated narrow line, the same pole energy and a photon spectrum approximately constant across it. It is not a calculation of captured production. Finite density, source motion and finite-volume modes are not folded into these rows.

The source tadpole also modifies the carrier potential. Reusing the leading stationary-constituent result,

    U_Phi = n/[4mM_S] (h-mu A/M_R^2),
    h_eff = h-mu A/M_R^2.

For positive mu*A and h=1, the two rows give h_eff=0.90847 and 0.08467. With the latter choice most of the original repulsive potential cancels. Keeping the old nominal wall height then requires approximately 6.60e29 or 7.09e30 messenger cores per m^3, respectively, rather than the 1e25 benchmark. These are formal density requirements, not prepared neutral-atom phases. The sign of mu*A is a model choice; reversing it changes this cancellation. The earlier width measurements/assignments alone fixed only magnitudes.

The result shows why increasing M_S and changing A cannot be analyzed only through the electron magnetic moment. Source width, source tadpole, wall potential and the material density change together. No previous dilute-atom or thermal calculation is automatically valid at these densities.

## Evidence and research decision

Nine checks pass: three symbolic partial-wave/matching identities and six independent numerical evaluations of the equivalent mass/coupling ceiling. The validated runner manifest pins code and outputs. The lower-width rows are explicit scaling evaluations, not additional experimentally verified points. No new Lean certification of unitarity or collider limits is claimed.

The chosen single-messenger construction has not passed the combined viability problem. A responsible continuation must either analyze a demonstrably compatible parameter region with all coupled changes, or investigate a distinct production/confinement sector. Merely replacing 10 MeV by a heavy mass is insufficient, and none of the illustrative heavy rows is declared allowed. The overall cold-energy manufacturing goal remains unresolved.

Reproduce:

    python3 sol61_push/heavy_messenger_tradeoff_2026_10_13/check.py /tmp/heavy_messenger_tradeoff_results.json

Source scope: the CMS original paper above and its official EXO-18-002 results page were inspected for right-handed direct production, stability and mass-range qualifications. Search results for multi-charged particles, promptly decaying sleptons and cascade-production limits were not applied to S. Earlier theoretical matching, the chosen potential and tadpole derivation are recorded in ../charged_messenger_2026_10_13/REPORT.md, ../stable_source_completion_2026_10_13/REPORT.md and ../source_medium_shift_2026_10_13/REPORT.md.
