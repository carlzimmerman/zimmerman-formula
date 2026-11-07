# QX17B: v3s field equations in 3+1 form, Lean kernels, and solutions (2026-11-06)

Criteria: FROZEN_CRITERIA.md (9684f63ba8). Adopts nothing. kappa = 1/2 FITTED. Not theory closed.

**Labels as frozen:**
- **B1 (ADM form):** FAIL as frozen. B1-N (`adm_check.out`): rho and S_ij match the covariant forms to <= 1.3e-40 and the on-shell momentum density vanishes to <= 2.8e-41 on all 3 seeds, but the off-shell momentum density row reads 2.0 on every seed (the checker's ADM J carries the opposite sign to J_a = -n^m h_a^n T_mn); see §5.
- **B2 (Lean):** PASS.
- **S-sph (solutions):** FAIL. The known-answer run and the Sun's full nonlinear solve did not converge; see §3.
- **Lane: NOT CERTIFIED.**

The equations themselves are certified in QX17 (v3s) and QX17A (AC2q) by direct variation. This lane adds the 3+1 form,
Lean kernels, and solutions.

## 1. ADM form, c restored (B1)

Foliation by the clock: tau = t, N = lapse, gamma_ij = leaf metric, K_ij = extrinsic curvature, D_i = leaf derivative.
The P field is purely spatial (n.P = 0), and A_i = c^2 d_i ln N.

- **No new dynamics.** P and N carry no time derivatives, so the P equation and the lapse equation are constraints on
  each leaf.
- **Momentum constraint is GR's.** Using the normal P equation (lambda), the P sector's momentum density vanishes on
  shell (Lean `momentum_density_zero`):

      D_j (K^ij - gamma^ij K) = (8 pi G / c^3) J^i_matter .

- **Hamiltonian constraint:**

      3R + K^2 - K_ij K^ij - 2 Lambda = (16 pi G / c^4) [ rho_m c^2 + c^2 Pi + W + gamma_L F + (c^4 mu_K^2 / 8 pi G)(Q^2 - 1) ]

- **P equation (leaf constraint):**

      (1 + gamma_L Pi_+ / c^2) A_i + gamma_L D_i Pi_+ = K W'(K|P|) Phat_i ,      K = 4 pi G,  gamma_L = K Lstar^2 / 2

  At gamma_L = 0 this is the a0 law: mu = x/(1+x) (Lean `mu_from_P`, `legendre_stationary`, `legendre_value`).

- **On-shell spatial stress** (Lean `stress_contraction` for the contraction step):

      S_ij = gamma_ij [ K W'|P| - W + gamma_L F + (c^4 mu_K^2 / 8 pi G)(Q - 1)^2 ] - K W' P_i P_j / |P|

- **Evolution equation** for K_ij: GR's, with S_ij above added.
- **Tensor sector:** the principal part is GR's, so tensor modes propagate at c_T = c.
- **Lapse equation:** the K(Q) term's N-derivative is -(Q^2 - 1) at Q = 1/N (Lean `KQ_lapse_deriv`).

**B1-N** checks numerically that rho, J_i and S_ij above equal QX17's covariant T_mn projected on 3 random 3+1
configurations. The first run (196 min) crashed while writing its output: the output path was relative and wrong, and the
rows had been piped through `tail`, so no number survived. The path is fixed and the check is rerunning (`adm_check.out`).
The 3+1 jet variation (`qx17b_jet4.py`) passed its frozen 3 h cap (stopped at 3 h 35 min, still evaluating) and is
**NOT RUN**. As frozen, B1-N carries the 3+1 statement.

## 2. Lean (B2): PASS

`fable_independent_2026/lean_2026/QX17B_field_equations.lean` has 12 theorems, standard axioms only, 0 sorry:
legendre_stationary, legendre_value, mu_from_P, lambda_solve, momentum_density_zero, stress_contraction (vectors in R^3),
Trr_on_shell, KQ_lapse_deriv, frw_dust, ac2q_frw_stress_zero, ac2q_nn_on, ac2q_nn_continuous.

**MUTATE twin** (`QX17B_field_equations_MUTATE.lean`): each of the four mutated statements (M1 legendre_value, M2
momentum_density_zero, M3 Trr_on_shell, M4 ac2q_nn_continuous) fails, so each depends on sorryAx. That is required.

Lean certifies only algebraic steps; the physical premises are hypotheses.

## 3. Solutions (S-sph): FAIL as frozen

**Static spherical system.** Areal gauge, ds^2 = -N^2 dt^2 + B^2 dr^2 + r^2 dOmega^2, P = p dr, c = 1:

    m'  = 4 pi r^2 (rho_b + Pi + W + gamma F)
    Phi' = [ (B^2 - 1)/r + 2 K r B^2 (gamma F - W + p_m) ] / 2           (T_rr = B^2 (gamma F - W) on shell; Lean Trr_on_shell)
    (1 + gamma Pi) Phi' + gamma Pi' = B K W'(K p / B)
    (r^2 p / B)' = B r^2 Pi
    TOV pressure p_m inside the body.

`sph_reduce.py` shows the Euler-Lagrange equations of the reduced Lagrangian equal QX17's covariant E2/E4 on the ansatz.
Residual is exactly 0 on 4 random profiles (sympy, 40 digits).

**Solver results** (`sph_solve.py`, scipy solve_bvp, x = ln(r/Lstar)). Both footings, not pooled:

| row | canonical (a0 9.3603e-11, Lstar 21.7 pc) | alt (a0 1.1312e-10, Lstar 22.9 pc) | gate | verdict |
|---|---|---|---|---|
| Sun: y/g* at 1 / 10 / 100 AU | 1.0000056 / 1.0000098 / 1.0000098 | 1.0000056 / 1.0000098 / 1.0000097 | hedgehog <= 1 % | PASS (maxdev 9.9e-6 / 9.8e-6) |
| Sun: full nonlinear GR remainder | 1.4e-3 (not converged: mesh-node limit) | 1.6e-2 (not converged) | <= 10 U_max = 2.1e-5 | **FAIL as frozen** |
| Sun retry, tol 1e-6 (post-freeze, labelled) | 8.4e-3, not converged | 6.1e-3, not converged | same | not converged |
| Galaxy 1e10 Msun: law S at 1-30 kpc | maxdev 2.5e-6 | 2.7e-6 | <= 1e-2 | PASS |
| Galaxy: full GR remainder | 5.4e-7 | 5.5e-7 | <= 10 U = 9.6e-6 | PASS |
| KNOWN: Lstar = 1e-3 pc gives law S | not converged (mesh-node limit), maxdev 5.8e6 | not converged, maxdev 2.5e13 | <= 1e-3 | **FAIL** |
| MUTATE gamma = 0: Sun y(10 AU)/g* | 3.2e5 | 4.3e5 | >= 1e3 | PASS (bites) |

**What fails is the solver, not a physics gate.**
- Both FAILs are solve_bvp runs that hit the mesh-node limit. Their outputs are not solutions, so they say nothing about
  the theory either way.
- The known answer was meant to validate the solver; it does not, so the PASS rows above are not validated by it.
- The Sun's weak-field (hedgehog) solve and both galaxy solves converged.
- The fix is a better solver: continuation in Lstar, or a shooting method in the screened core. That is not done here.

**Physics observation (isolated Sun, converged weak solve; not a gate).** The Sun stays screened far beyond Lstar:

| r / Lstar | 1 | 3 | 10 | 30 | 100 |
|---|---|---|---|---|---|
| g / g_lawS, canonical | 0.0036 | 0.0059 | 0.018 | 0.051 | 0.156 |
| g / g_lawS, alt | 0.0031 | 0.0051 | 0.015 | 0.045 | 0.137 |

(Corrected in QX17C: the converged solve gives only 0.71 / 0.67 of law S at 1e3 Lstar, ~22 kpc; the earlier "law reached around 1e3 Lstar" was an extrapolation.) This is a point Sun with no Galactic field and no other stars.
Whether a galaxy built from screened stars still shows law S is **open**. The smooth-ball galaxy above does show it, but
granularity was not tested. Do not cite this as a result about real galaxies.

**FRW and tensor sector** (analytic, from the equations):
- **v3s FRW:** at P = 0, Pi = 0. The K(Q) dust gives rho = (mu^2/2K)(Q^2 - 1) = I0 (1 + w0/a^3)/(2K a^3) with
  w0 = I0/(4 mu^2) (Lean `frw_dust`).
- **AC2q FRW:** the stiffness stress is identically zero (Lean `ac2q_frw_stress_zero`), so the background is the
  canonical scalar's.
- **Tensors:** c_T = c in both.

## 4. Follow-up

QX17C (closure_2026_11_06/QX17C_fd_spherical_solver) re-solved this problem with a finite-difference Newton solver: all gates PASS converged on both footings, MUTATE bites. S-sph here stays FAIL as frozen.

## 5. B1-N result (rerun, 126 min)

| seed | rho rel | S_ij rel | on-shell J abs | off-shell J rel |
|---|---|---|---|---|
| 11 | 8.5e-41 | 2.6e-41 | 2.3e-42 | 2.0 |
| 22 | 1.3e-40 | 2.9e-41 | 2.8e-41 | 2.0 |
| 33 | 4.2e-41 | 4.2e-41 | 1.2e-41 | 2.0 |

**B1 FAIL as frozen** (line 1e-10). The off-shell momentum expression in `adm_check.py`, P_a [n.dl + lambda - gamma (n.dPi - Pi n.dl)],
has the opposite sign to the covariant J_a = -n^m h_a^n T_mn; a relative residual of exactly 2.0 on the worst component is what
J_adm = -J_cov gives. Not verified component by component (that needs a rerun with the sign flipped; not run).
**What survives:** the Hamiltonian-constraint density and the spatial stress are numerically certified, and the P-sector momentum
density vanishes on shell (sign-independent), so "the momentum constraint is GR's" holds. Lean `momentum_density_zero` uses the same
sign convention as the checker; it proves only the on-shell vanishing, which is unaffected.
