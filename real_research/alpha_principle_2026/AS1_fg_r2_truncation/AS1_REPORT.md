# Lane AS1: report

## Verdict: NOT COMPLETED. The lane stopped at gate G1.

The pre-registration requires the script's own derivation, with b = 0, to reproduce Eichhorn-Versteegen's Einstein-Hilbert beta
functions (4.8)-(4.9) exactly in one of the four declared gauge/convention combinations. None of the four does, so the lane stops here,
as the pre-registration requires. As a result:

* no R^2 fixed point was searched for;
* no f_g*, g_Y* or P = alpha^-1(0) exists;
* no class was assigned;
* gate G2, gate G3 and the MUTATE_2 control were not run.

**This says nothing about alpha.** The asymptotic-safety route was not tested at the R^2 step: it is neither supported nor excluded.
kappa and Z enter nowhere.

| item | result |
|---|---|
| verdict class | NOT COMPLETED (G1 fails for all 4 declared combinations) |
| P = alpha^-1(0) | none (not computed) |
| f_g* | none (not computed) |
| fixed point (g*, lambda*, b*) | none (the R^2 search was not run) |
| G0 | PASS. Lane B's chain was reproduced by import: f_g = 0.04795 gives 92.91525 and f_g = 0.009805 gives 137.03410 (both within relative 1e-4); lane B's own C5 and C6 are reproduced to 1e-9 |
| G1 | FAIL in all 4 combinations, so no gauge/convention was selected |
| G2 | not run (the lane stopped before it) |
| G3 | not run |
| classifier controls | PASS. 0.009805 gives AGREES; 0.04795 gives NO IMPROVEMENT, with \|P - 137.036\| = 44.12075, which is >= 44.12 |
| MUTATE_3 | the controls FAIL as required (exit 1) |
| MUTATE_1 | G1(iii) FAILS in every combination as required (exit 1) |
| MUTATE_2 | not run (it needs the R^2 flow and G2, which were not reached) |

## Why G1 fails (all numbers from `as1_g1_eh_betas.out` and `as1_g1_fg_flat.out`)

### 1. The gravity part cannot be reproduced in any declared combination

The cleanest single fact is the vacuum term of the gravity sector in beta_Lambda, at Lambda = 0 and first order in G:

* **Derived:** +G/(2 pi) in every declared combination. This is the counting of two graviton polarisations x 1/2.
* **E-V (4.8)-(4.9):** -G/(2 pi).

E-V's whole Lambda dependence, (G/2 pi)(3/(1-2 Lambda) - 4), equals 5 TT modes plus 1 scalar mode at mass -2 Lambda (times 1/2), minus
the full vector ghost (4), with the gauge-mode and Jacobian contribution absent. Comparing with the derived values:

* alpha = 0 gives (3/(1-2L) - 2): its gauge modes and Jacobians add +2;
* alpha = 1 gives (5/(1-2L) - 4).

The R-coefficients differ as well. In beta_G = 2G + (G^2/pi)[...], the gravity part is:

| combination | gravity part of the bracket |
|---|---|
| (0,1), no eta (derived) | -(100L^2 - 132L + 81)/(24(1-2L)^2) |
| (1,1), no eta (derived) | -(200L^2 - 212L + 105)/(24(1-2L)^2) |
| E-V (4.8) | -(56L^2 - 68L + 29)/(6(1-2L)^2) |

Diagnostic D2: E-V's constant 14 matches the vector ghost traced *undecomposed* (type Ia: 6 x 7/3). The York-decomposed type-I trace
that the pre-registration fixes gives 25/2.

E-V state that they took (4.8)-(4.9) from an unpublished single-metric computation ("S. Lippoldt, to appear") with alpha = 0, beta = 1
and eta_h = 0. Its regularisation of the gauge modes and ghosts is not stated, and it is not the scheme frozen here, in which every
-D^2 of Gamma^(2) is regulated, including the gauge-fixing term.

### 2. One combination has no finite flow

With alpha = 0, beta = 1 and the eta_N terms included, the limit alpha -> 0 of d_t Gamma_k diverges. The divergent term is proportional
to eta_N/alpha and arises in the (h, sigma) sector. This is consistent with Codello-Percacci-Rahmede's remark that for rho = 1 the
infinite-gauge-parameter limits cannot be taken.

### 3. The matter part fails under the frozen regulator

E-V's matter terms are those of Dona-Eichhorn-Percacci, who regulate the natural operators (type II). Under the frozen "type I"
regulator the a_1 coefficients per species are:

| species | frozen type I | E-V (type II) |
|---|---|---|
| scalar | 1/6 | 1/6 |
| Dirac | -1/6 | 1/3 |
| vector | -1/6 | -2/3 |

The a_0 (vacuum) coefficients agree.

### 4. G1(ii), the fixed points

The SM fixed points of the derived systems, with the frozen matter, are:

| combination | SM fixed point |
|---|---|
| (0,1), no eta | (0.97371, -1.24522) |
| (1,1), no eta | (0.84486, -1.12484) |
| (1,1), with eta | (0.87059, -1.11901) |
| (0,1), with eta | none (no finite flow) |
| E-V | (2.726, -3.758) |

Diagnostic D4 swaps in E-V's type-II matter, which is not the frozen choice. The fixed points then become (6.8682, -8.97488) for
(0,1) and (3.1999, -4.39112) for (1,1). This is still not E-V's point, so the gravity part alone already moves it.

### 5. G1(iii), the one part that does pass

f_g was derived from scratch: flat background, constant field strength, the graviton-photon trace, and the Litim type-I regulator.

* **(0,1), no eta:** the result is exactly E-V's f_g = G(1 - 4 Lambda)/(4 pi (1 - 2 Lambda)^2). The difference simplifies to 0. The
  result is independent of xi, and the parity check passes.
* **(0,1), with eta:** the result is G(4(1 - 4 Lambda) + eta_N)/(16 pi (1 - 2 Lambda)^2). This is E-V's eq. (3.6) with eta_h = eta_N.
* **(1,1):** the result is twice the alpha = 0 value.

So G1(iii) holds only in E-V's own gauge, but G1(i) and G1(ii) fail there.

## Checks of the machinery (all PASS)

| check | what it verifies |
|---|---|
| V1 | CPR's f(R) York Hessian at the EH point equals CPR's EH York operators |
| V2 | On shell, the f-part annihilates the pure-gauge directions |
| V3 | The S^4 heat-kernel coefficients for transverse vectors and TT tensors, derived from the unconstrained ones, equal CPR's table: (3, R/4) and (5, -5R/6) |
| V4 | The machinery reproduces CPR's published type Ib, alpha = 1 EH coefficients exactly: A0 = (1+8L)/(1-2L), A1 = -(105-212L+200L^2)/(24(1-2L)^2) |
| V5 | The type Ia (Reuter) coefficient -(11-18L+28L^2)/(3(1-2L)^2) is reproduced |
| V6 | The symbolic transcription of (4.8)-(4.9) equals lane B's numeric `b1.betas` at 20 random points (8.9e-15) |
| I1-I4 | The flat-space action: Fierz-Pauli gauge invariance, photon block, Hermiticity, and how the regulator acts |

One cross-check I added myself, and which was not pre-registered, was **not** reproduced: the TT-only f_g against E-V's TT formula in
their section 3.2. I derived 5G(4 - 16 Lambda + eta)/(72 pi (1-2 Lambda)^2); the paper prints
(5G/36 pi)(8/(1-2 Lambda) + (8 - eta_h)/(1-2 Lambda)^2). I have not identified the reason. It is reported as informational (see the
Amendment).

## What the outcome means (pre-registered wording)

NOT COMPLETED means the lane stops. There is no claim about the full theory and no claim about alpha.

Any change that could make an EH gate pass would be a NEW trial in a NEW lane, with its own pre-registration. Examples:

* another gauge;
* regulating matter with natural operators;
* not regulating, or dropping, the gauge modes;
* a type Ia ghost.

This is standard quantum-gravity physics, not a framework result.

## What was read

**Eichhorn-Versteegen, arXiv:1709.07252** (LaTeX source).
* Read in full: section 2; section 3.1, the FRG setup including the truncation, gauge fixing and regulator; section 3.2, the TT
  approximation; section 3.3, the quantum-gravity contribution to the gauge coupling; section 4 including (4.8)-(4.9) and their source
  statement; the conclusions; appendix B on gauge dependence; the "Lippoldt, to appear" bibliography entry.
* Read in part: appendix D on vertices.
* Not read: appendix A (beta functions for general gauge parameters) and appendix C (scalar QED).

**Codello-Percacci-Rahmede, arXiv:0805.2909** (LaTeX source).
* Read in full: section IV intro and IV.A-C (EH with cutoff types Ia, Ib, II); section VII (the f(R) Hessian, ghosts, insertion into
  the flow equation, gauge choices, result tables including the n = 2 fixed point, the UV critical surface, scheme dependence); the
  appendix on S^4 spectra, excluded modes and the heat-kernel table.
* Not read: sections I-III, V, VI and VIII; the type III subsection; the other appendices.
* G2 would have compared with Table 1, n = 2: Lambda* = 0.1294, G* = 1.5633, g_2* = 1.514e-3 (gauge rho = 0, beta -> infinity,
  type Ib, eta terms on). It was not run.

**Dona-Eichhorn-Percacci, arXiv:1311.2898** (LaTeX source).
* Read in full: section II (method: truncation, regulators, type II for matter), section III (beta functions), and the start of the
  perturbative-approximation section.
* Read only at grep level: the statements on type Ia and type II.

**Alkofer-Saueressig, arXiv:1802.00498**: downloaded, not read (G3 was not reached).

**Riabokon-Schiffer-Wagner, arXiv:2508.03563**: downloaded, not read in this lane. It is used only through lane B's reading.

**Recalled rather than read**, and not load-bearing:
* The general structure of Reuter's EH flow. It was re-derived, and V4 and V5 check it against CPR.
* The guess that "Lippoldt" refers to Gies-Knorr-Lippoldt-type York computations.

The downloaded sources sit in `as1_scratch/` and are not committed.

## Files

* Shared code: `as1_common.py`. It runs lane B's `b3` and `b1` as modules, by import, with their stdout captured; lane B is not modified.
* `as1_g0_downstream.py`, with outputs `.out` and `_MUTATE_3.out`.
* `as1_g1_fg_flat.py`, with outputs `.out`, `_MUTATE_1.out` and `_FIRSTRUN.out`.
* `as1_g1_eh_betas.py`, with outputs `.out`, `_FIRSTRUN.out` and `_RUN2.out`. Its normal mode exits 1: that is the G1 outcome, not a
  crash in the final run.

All runs were single-thread at `nice -n 19`; the total compute was about 1 minute.
