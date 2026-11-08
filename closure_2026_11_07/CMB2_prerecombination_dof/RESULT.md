# CMB2 RESULT: nothing in the action other than the clustering dust supplies a still potential before recombination. NO, both footings; one open item on the law at large a0(z)

Criteria: FROZEN_CRITERIA.md (6b3161c3b0), committed and pushed alone before any script or number. One subagent was run
per degree of freedom (DoF); their scripts and outputs are listed below. The Field equations session graded them.
Adopts nothing. Kappa = 1/2 FITTED; not theory closed. Both footings, never pooled. No LCDM input: the background is
F1A's footing background B2.

## Label: NO (every DoF fails the frozen pre-screen, both footings)

The pre-screen asks for a still Weyl potential of at least 0.5 of the dust's at R 5.41, somewhere in k 0.03-0.3
Mpc^-1, with the action's own parameters in range and no galaxy capture beyond f 0.33 / 0.19.

| DoF | equation (sympy) | largest still share of the dust's Weyl potential | canonical / alt |
|---|---|---|---|
| **D1** khronon / clock, dust removed (`d1_khronon.*`) | v3s: pi'' + 2H pi' + (1 - 1/Qb) k^2 pi = 3(Qb-1) a Phi' + Qb a Psi' + 3a' Psi, a barotropic fluid with c_s^2 = (Q-1)/Q, w = (Q-1)/(Q+1). AC2q clock: Klein-Gordon, with the stiffness identically 0 at P = 0 | khronon capped at the galaxy allowance f 0.33 / 0.19: 0.043 / 0.024 still (0.081 / 0.047 of any kind). Clock about 1e-20. Non-dust w0 term at the BBN mu_K below 2e-7 | **FAIL / FAIL** |
| **D2** P sector (`d2_psector.*`) | no propagating mode: the Hessian in the P velocities has rank 0, the Dirac chain closes with 0 DoF, and the dispersion determinant has degree 0 in omega. The response is instantaneous, an odd function of g_N at the same instant, with quadrature at most 5e-12 and time mean at most 8e-13 of the amplitude. Stiffness gamma_L Pi at most 4.0e-9 / 4.8e-9 (Lstar to 90 pc, a0 x up to 100) | 0 of its own | **FAIL / FAIL** |
| **D3** preferred frame in the matter equations (`d3_frame.*`) | S_m has no khronon field; matter is conserved separately (Noether identity); tight coupling gives c_s^2 = 1/(3(1+R)) exactly, so r_s changes only through H(z); no Q factor enters recombination. Finding: a linear slip -\|P\|\|E\|(k k - delta/3) for x >~ 1, with \|Phi - Psi\|/Psi at most 5.8e-4 / 7.1e-4, locked to the acoustic gradient | at most 7e-4 ("follows") | **FAIL / FAIL** |
| **D4** a0 law at z 1100, a0(z) = x a0, x 1-100 (`d4_law.*`) | phantom div[(nu(g/a0) - 1) g]/4 pi G on the realised acoustic field (112^3 box, 1078 Mpc), CAMB transfers on the B2 baryons-only model. It correlates with Psi_N at r 0.992-0.997, lag -0.07 to -0.11 rad: "follows" in every cell | k 0.1 at most 0.05 / 0.05; k 0.3 at most 0.009 / 0.009; k 0.03 at most 0.28 / 0.30 (at x 100) | **FAIL / FAIL** at every x |

## Open item, stated plainly: the law at large a0(z) raises the odd peaks in a toy oscillator

The criteria expected a following potential to rescale G only. D4's tight-coupling oscillator, with G -> (1 + beta_k)G
following the gradient's history, says otherwise at large x:

| model | H1/H2 | H3/H2 |
|---|---|---|
| baryons only | 0.873 | 1.006 |
| dust R 5.41 | 1.220 | 1.447 |
| law, x 1 / 3 / 10 | 0.87 | 1.008 / 1.011 / 1.025 |
| law, x 30 (canonical [alt]) | 0.97 [1.00] | 1.08 [1.09] |
| law, x 100 | 1.71 [1.99] | 1.30 [1.36] |

- At x >= 30 the following phantom raises the odd peaks, approaching the dust at x 100. It also moves the first peak
  from k 0.0154 to 0.022-0.024 Mpc^-1, away from where the data put it.
- The frozen pre-screen is defined on the still potential, so this does not change the label. It does mean the NO does
  not yet cover the peak ratios at x >= 30.
- **What x means.** The action's a0 is (1/2) c sqrt(G rho_DE). x = 100 at z 1100 needs rho_DE 1e4 times today's then,
  and x = 30 needs about 900 times. With rho_DE constant, as CFG689's a0(z) reads to z 2.33, x = 1. At x = 1 the law's
  peak ratios equal the baryons-only ones (H3/H2 1.008 vs 1.006).
- **What is owed.** A full Boltzmann treatment of the law at x 30-100 on PR4 + ACT DR6, in coordination with CMB1, with
  the first-peak position graded too. It is required only if a framework-native history puts a0(z 1100) at x >= 30;
  none in the record does.

## Controls
- **KA-dust: PASS.** D1 and D4, each with its own code, reproduce F1A G4's baryon contrasts: -26.809 / -108.150 at
  k 0.05 / 0.3, frozen -26.8 / -108.1.
- **MUTATE-phase: PASS.** A planted source equal to the dust's amplitude but phase-locked to the fluid reads "follows",
  with still/dust at most 2e-16. It fails the pre-screen in D1 and D4.
- **MUTATE-gravity: PASS.** Adding beta n_m u^m to the baryon worldline puts tau into the baryon Euler equation (D3).
- D2's mode-count MUTATE also bites: a hand-added (n.grad P)^2 gives a Hessian of rank 3 and 3 DoF, with
  c_s^2 = gamma_L F''/m.

## Finding for F1A (reported; F1A's label is unaffected)
- D1 found that F1A G4's starting state (theta = k^2 tau_i / 2) breaks the Poisson constraint by a factor of 10.6 at
  a_i, so its baryon contrasts depend on a_i.
- With starting values that satisfy the constraint, the contrasts are -25.14 / -90.28 and no longer depend on a_i.
- KA-dust passes as frozen, because it was frozen on F1A's numbers. The physically consistent values differ by 6.2 % /
  16.5 %.
- F1A G4's conclusion holds under both: the clock cannot cluster (Q <= 3.4e-11), and a stiff field reaches <= 0.16 %.
- The D1 ratios barely move (0.080 / 0.043 / 0.036 with F1A's starting values).

## Disclosures
1. The DoFs were computed by four subagents, each writing only in this directory. The grading here reads their JSON and
   reports.
2. D1:
   - photons and baryons tight-coupled to z 1100;
   - neutrinos treated as a fluid without shear;
   - integration starts at a = 1e-6;
   - the tracker-clock row is a stress test, not AC2q's (unfixed) potential.
3. D2: the Dirac totals (10 / 10) are entered by hand from the constraint chain. The Hessian ranks and determinants are
   computed. The source amplitude is scanned, not solved.
4. D3:
   - the absence of tau from S_m holds by construction;
   - the Noether identity was checked for scalar matter in a diagonal (t, x) metric;
   - the Thomson term was inserted as the standard collision term, not derived;
   - the slip is pointwise, for a plane wave, first order in the tilt.
5. D4:
   - one realisation;
   - the k 0.01 band has 4 box modes and is outside the frozen k 0.03-0.3 range. There, near the horizon, the phantom's still/dust ratio exceeds 0.5 for x >= 3-10 (0.17-5.5 across variants and x), and some cells read "mixed". It is not graded, and is stated so that it is not hidden;
   - CAMB's Psi_N did not compile, so the Weyl potential was used as the source;
   - the oscillator is a toy (no damping, projection, Doppler or ISW);
   - peak RSS 1.12 / 1.19 GB, over the 1 GB line; the physical footprint was 0.20-0.22 GB, and no 1024^3 run was live.
6. The D4 subagent was stopped after it reported, so that its outputs are the ones graded.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
