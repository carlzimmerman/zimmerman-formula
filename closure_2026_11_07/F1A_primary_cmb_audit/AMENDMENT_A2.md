# F1A amendment A2 (after the result; disclosed, not a rewrite): G4's starting state

Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

- **Prompt.** CMB2 (cd1c7c35a3) reported that G4's starting state breaks the Poisson constraint by a factor 10.6.
  Its baryon contrasts therefore depend on the starting a_i; with consistent initial conditions they read
  -25.14 / -90.28. CMB2 said G4's conclusion holds.
- **Check.** g4_ic_check.py -> g4_ic_check.json, on the same equations and the same B2 canonical cold background.
  - G4's start is delta_i = -1.5 (1+w_i) phi.
  - The consistent start is delta_i = (1+w_i)(-1.5 - 0.5 (k tau)^2) phi, the O((k tau)^2) term from the 00 Einstein
    equation in the radiation era.
  - Each start is run at a_i = 1e-7, 1e-6 and 1e-5.
- **Confirmed: G4's printed contrasts depend on a_i.**
  - At k 0.3, G4's start gives a dust (= baryon) contrast of -95.5 / -108.2 / -226.1 at a_i 1e-7 / 1e-6 / 1e-5.
  - The consistent start gives -94.13 / -94.20 / -99.95.
  - At k 0.05: G4's start gives -26.67 / -26.81 / -28.18; the consistent start gives -26.650 / -26.653 / -26.712.
  - My comoving-Poisson residual at G4's start (k 0.05, a_i 1e-6) is 10.58, CMB2's factor. That diagnostic also
    carries the matter fraction that neither start includes. The decisive test is convergence in a_i, which the
    consistent start passes.
- **Corrected G4 dust contrasts at z 1100** (consistent start, a_i 1e-7):

| k (/Mpc) | 0.02 | 0.05 | 0.10 | 0.20 | 0.30 |
|---|---|---|---|---|---|
| dust contrast | -8.79 | -26.65 | -48.60 | -76.26 | -94.13 |

  - CMB2 reports -25.14 / -90.28 for its pair. That is 4-6 % from these, consistent with the difference in model content.
  - This lane does not adopt either set.
- **G4's graded statistic is unchanged in kind.** With consistent starts, Q_X1 <= 3.7e-12 and Q_X2 <= 1.63e-3 for
  k >= 0.05 at every a_i (frozen line 0.05). KA-dust is unaffected, since it is the same start in both runs.
  G4 stays REPRODUCED, and F1 stays CONFIRMED.
- **What changes.** RESULT.md's G4 table printed delta_dust -26.8 / -49.7 / -81.9 / -108.1 and the baryon contrasts
  "without the cold dust". Those printed contrasts carry the a_i-dependent start error (up to 15 % at k 0.3). Read them
  with this amendment. RESULT.md is not rewritten.
- **CMB1.** CMB1 does not touch G4's code path; its fits use CAMB's own initial conditions.
