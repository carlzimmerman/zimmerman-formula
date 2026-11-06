# QX2 frozen criteria (common gate): clusters from the action on the table

Frozen before any QX2 script exists. Rules: closure_2026_11_06/SWARM_BRIEF.md. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. No LCDM inputs.

## Actions graded

v3s (PAPER68, closure_2026_11_05/CLOSURE.md section 1) and AC2q (AC7). Their static, spherically symmetric
field equation (V3_FULL_PICTURE section 1, AC8) is

    div[ mu(|grad psi|/a0) grad psi ] + mu_K^2 psi + (gamma_L stiffness terms) = 4 pi G (rho_b + rho_s),

with mu(x) = x/(1+x). rho_s is AC2q's clock source (s^2 = phidot^2 <= 2 rho_DE; zero in v3s). Matter couples
minimally (S_m[g]). So the static extra source can only come from four terms: the law's phantom (a function of
g alone), the K(Q) dust term mu_K^2 psi, the switched stiffness (scale Lstar), and the clock (s^2, gamma s^2).
QX2 grades each term on its own (iterations 1-5). Each iteration has its own criteria file. Together they cover
every static term of both actions.

## Gate G-X (the same for every iteration; both footings, never pooled)

- Data: X-COP (real_research/data/xcop), the clusters that have hydro_mass, fgas_profile and mstar FITS (LW1's
  builder: M_b = MGAS + MSTAR, M_HSE = M_FORW, interpolated in log at x = r/R500 in {0.1, 0.2, 0.3, 0.5, 0.7}).
- Delta = log10(M_HSE / M_model); positive means the model is short.
- PASS: |mean Delta| <= 0.05 and rms <= 0.10 (HO1's line, as XH1 and LW1 used).
- Error check: X-COP's own EM_FORW is reported per point. A failure counts only if mean Delta exceeds 5 times the
  standard error of the mean of the per-point log errors combined with HO1's 0.05 line.
- a0 per footing: canonical 9.3603e-11, alt 1.1312e-10 m/s^2. rho_DE = a0^2 / (kappa^2 c^2 G), framework-native,
  kappa = 1/2.

## Gates applied only after G-X passes

Groups and lensing (CC2's harness), SPARC/RAR rms (<= 0.054 + 0.01 dex) and Cassini (C6P line), all on the
candidate's own equations. A candidate that fails G-X is FAIL with no further gate.

## Known answers (every iteration)

- K-LW1: iteration 1's plain law reproduces LW1's committed X-COP numbers (lw1_xcop.json fits builder:
  mean, rms) to 1e-3 dex, per footing.
- Each iteration's MUTATE has a separate output and must move the gate as stated in its file.

## Closing label for the door

- FAIL (action on the table) if every iteration 1-5 fails G-X. Being exhaustive over the static terms, this is
  a no-go for v3s and AC2q statics. The algebraic bounds are certified in Lean (QX2_cluster_nogo.lean + MUTATE twin).
- Otherwise the passing mechanism goes on to the later gates, and the label waits on them.
- Scope: hydrostatic masses (XRISM/Eckert non-thermal bias <= 0.03 dex, reported); statics only. Nothing about
  non-static or non-minimal extensions; those would be new actions, not this one.
