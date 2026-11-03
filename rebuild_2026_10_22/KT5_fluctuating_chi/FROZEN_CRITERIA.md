# KT5_fluctuating_chi: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: work out the fluctuating route from KT4. κ = 1/2 FITTED. Footings never pooled. Not theory closed. No cold component; no particle adopted, and the mode below isn't claimed as one. **Not blind:** the algebra was worked by hand first, knowing the target, and κ² = 2/n³ was noticed before its mechanism.

## Mechanism
L = -(1 - P(chi)) g²/(8πG) - V(chi), with V from N classical fluctuating real modes psi of mass m = m0 (1 - chi) at effective energy T: V = -N T m³/(12π) in the high-T limit.

Named hypotheses:
- **H1, portal:** P = chi^n.
- **H2, linear mass:** m = m0 (1 - chi), massless at the vacuum chi = 1.
- **H3, cell:** T m0³ = c_E rho c². **c_E = 1 is the suspicious input.** It says energy T per volume m0^-3, with no 4π/3. It's the same pi-free premise moved again unless it's derived.
- **H4, classical limit:** T >> hbar c m0.

Result to confirm: V' = c_E N (rho c²/4π)(1-chi)², so g²/s² = 2 c_E N (1-chi)²/P' and **κ² = 2 N c_E / n³**.

## Part 1: option space, CFG894 §1 and §4
N in {1, 2}; n in {1, 2, 3, 4}; c_E in {1, 2 (T/2 per dof), 3/(4π) (ball cell), 12π (|V(m0)| = rho c², the loop's own self-consistency)}. Equal weights. Print all kappas, mass in rho_DE window [0.227, 0.607], mass at exactly 1/2. If values differ, the route is a **MENU**, and by §4 a menu containing 1/2 counts as a spurious 1/2 unless a named selector removes the other entries. State whether H3's T is the de Sitter temperature; check H4 for T_dS numerically.

## Part 2: new kernel, second prediction S4
For N = 1, n = 2, c_E = 1: t = sqrt(chi), Y = g/s = 1/t - t, so mu = 1 - exp(-4 asinh(Y/2)). Slope 2, tail exponent 4. No free parameter. Sympy check.

**Gate S, SPARC:** L232's loader, galaxy-equal statistic as KT1, s from each footing, Upsilon as stated. Pass if rms <= OR mu_2's rms + 0.005 dex and |median residual| <= 0.05 dex. Upsilon x 0.8, x 1.25 reported, not graded.

**Gate C, Cassini:** the committed DHF integral `q_direct2D` and constants from `fc_cassini_CORRECTED_2026.py`, copied unchanged. Guard: routeA must reproduce 0.221. Pass if q < that script's Q_PASS on the canonical footing. Alt reported with its own a0. Also report OR mu_2 and mu_n Milgrom n = 3, 4, as the script's anchors.

## Labels
Part 1: **MENU, 1/2 SPURIOUS** or **SELECTED**. Part 2: **SECOND PREDICTION PASSES S AND C**, or names the one that fails. A pass doesn't derive κ: H3 stays, and it says the kernel is usable. Not a detection.

## Controls
MUTATE: H2 mass (1 - chi)^2, so V' differs. Expected: slope no longer linear in Y at the vacuum, and κ from this formula doesn't hold. Separate `_MUTATE`, exit 1. Planted: synthetic data from the new kernel with real scatter must rank it above OR mu_2 on the same statistic. No download. Single thread, minutes.
