# AS236 — Derivation: cosmological versus local G for the centered clock

**Run:** `AS236-r1-20260928T203554Z-dsv4f-hermes` · **Task hash:** `99b632e5e85942f5aa8082c5a7764485a41c2501d2da9cad6770900c99f0e883`
**Worker:** deepseek/deepseek-v4-flash-0731 via openrouter (Hermes subagent, macOS host)
**Branch:** CA5-GNC-R physical-metric branch; Q, RAR, MU2, historical EXP, filtered MONO never interchanged; criterion B operative.

This file derives the seed's target from the pinned action variation only —
every factor, sign and unit below is obtained from the exact homogeneous
projection of eq. (13) of
`real_research/common_action_2026_09_26/action/FINAL_ACTION.md` (SHA-256
`b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`), never by
identifying bare constants with observations.

---

## 1. Pinned conventions and the target

Homogeneous reciprocal branch: coordinate `t_c = t = 1`, trace-fluctuation
source `Q_K = 0`, `A_K = <N Q_K>_h = 0`, dust `rho_b` at `t_c = 1`, and the
reciprocal density `rho_d = rho_R(t=1) = T1 + V0 + Vmix` with `T1 = K_d(t=1)`
(kinetic `(1/2)|v|^2`), `Vmix = W_exc`, `V0` (as laid down upstream in
results/AS127).  Metric: FRW physical metric

```
ds^2 = -N(t)^2 dt^2 + a(t)^2 (dx^2 + dy^2 + dz^2),   n_mu = (-N, 0, 0, 0)
```

Displayed target (as in the seed and FINAL_ACTION eq. 18):

```
3 M_P^2 H^2 = M_P^2 Lambda + rho_b + rho_d,    G_N = G_bare/c_N,   c_N = 1 - alpha/2
```

bare-Lambda = 0 branch of CA5-GNC-R:  `3 M_P^2 H^2 = rho_b + T1 + Vmix + V0` with
`G_cosm/G_N = c_N`.

## 2. Geometry of the centered clock (exact sector, sympy lane)

On the FRW metric with lapse, the exact three-plus-one computations give
(`a' = da/dt`, `H = a'/a`, everything in the 3+1 sector):

- **Scalar curvature (closed form):**
  `R4 = 6 (H/N)^2 + 6 (a''/a - (a'/a)(N'/N)) / N^2` — full exact residual 0
  (symbolic lane residual `R4_FRW_closed_form` verified to 0; numeric lane N1
  re-derives `R4` from finite-difference Christoffel symbols independently,
  rel. residual 5.9e-7 on a 41-point grid, see Section 8).
- **Leaf extrinsic curvature:** `K_ij = (H/N) h_ij` exactly
  (`Kij_vs_HN_hij_residual = 0`-matrix), hence
  `K = tr_h K_ij = 3 H/N` (residual 0).
- **Trace fluctuation:** `T_K = K_ij K^ij - K^2 = -6 H^2/N^2` (residual 0).
- **Intrinsic 3-curvature of flat slices:** `R3 = 0`.
- **Static weak-field check:** on `ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2`,
  `K_ij = 0` identically — the `c2`-block has no static source
  (`static_K_allzero = true`).

## 3. Homogeneous projection of the exact unitary lapse equation (13)

FINAL_ACTION eq. (13) (exact, fixed-h lapse equation, heat-imposed):

```
(M_P^2/2) { R3 - T_K - 2 Lambda + c2[-Q_K^2 + 2 K Q_K - 2 K A_K/N]
            + V_a - div_N[...] + c_N[G(Y_h) - ell Delta_h W_b] } = rho_b + rho_d
```

Homogeneous sector with `V_a = 0` (all `a, DZ, DU` gradient terms vanish),
`Q_K = 0`, `A_K = 0`, gate inactive (`f = G'(Y_h) = 0`), the `c2`-bracket and
the `c_N`-compensator vanish identically, and `R3 = 0` leaves exactly

```
(M_P^2/2) (0 - T_K - 2 Lambda) = (M_P^2/2)(6 H^2/N^2 - 2 Lambda)
                               = 3 M_P^2 (H/N)^2 - M_P^2 Lambda
```

With `H` the physical rate, residual 0 against
`3 M_P^2 H^2 - M_P^2 Lambda` (`eq13_homogeneous_vs_3MP2H2_minus_MP2Lam = 0`).
So the centered-clock Friedmann law is

```
3 M_P^2 H^2 = M_P^2 Lambda + rho_b + rho_d,     rho_d = T1 + V0 + Vmix        (A)
```

and in the bare-Lambda = 0 branch

```
3 M_P^2 H^2 = rho_b + T1 + V0 + Vmix                                        (A0)
```

both with residual 0 (`target_residual_general`, `target_residual_bare_Lam0`).

## 4. Both couplings from their action variations (not by identification)

- **Cosmological coupling (this Friedmann sector):** the exact lapse equation
  in the form `M_P^2 (3H^2 - Lambda) = rho_b + rho_d` carries the action's
  `(M_P^2/2)` normalization, i.e. `M_P^2 = 1/(8 pi G_bare)` as in
  FINAL_ACTION.  Solving for the cosmological Newton constant:

  ```
  G_cosm = 1/(8 pi M_P^2) = G_bare        (G_cosm_from_Friedmann = G_bare, residual 0)
  ```

- **Local (measured) coupling (high-k weak-field experiment, upstream
  results/AS226):** the same action, separately solved Cavendish sector, gives
  `G_N = G_bare/c_N` (`G_N_from_action`, residual 0); `c_N = 1 - alpha/2`.

## 5. The ratio

```
G_N / G_cosm = (G_bare/c_N) / G_bare = 1/c_N = 1/(1 - alpha/2)          (B)
G_cosm / G_N = c_N = 1 - alpha/2
```

which is FINAL_ACTION eq. (18) `G_cosm/G_N = c_N` re-obtained as the ratio of
two independently varied action couplings.  In alpha form
`G_N/G_cosm = -2/(alpha-2)` with residual 0 against `1/(1 - alpha/2)`.

**Clock-centering assumption necessary for the result:** the mean-subtracted
trace `Q_K = K - <K>_h = 0` on the homogeneous leaf, i.e. the centered clock
(`<K>_h = K`).  A different uncentered variant `-c2 K^2` (Section 7) changes
the Friedmann coefficient and the ratio — this is the negative control.

## 6. Dimensional footing (both footings, separately)

Mandated footing `a0 = (c/2) sqrt(G_N rho_Lambda)`, `kappa = 1/2` adopted as
input (seed).  With `rho_Lambda = a0^2/(kappa^2 G_N c^2) = 4 a0^2/(G_N c^2)`:

| footing | a0 [m/s^2] | rho_Lambda [kg/m^3] | kappa back-check |
|---|---|---|---|
| canonical    | 9.3619e-11 | 5.84441245e-27 | 0.5 |
| alternative  | 1.1279e-10 | 8.48308962e-27 | 0.5 |

The coupling ratio (B) contains no `a0`; it is identical on both footings
(`footing_independent_ratio`). Sample at alpha = 3/10:
`G_N/G_cosm = 20/17`, `G_cosm = 5.673155e-11 m^3 kg^-1 s^-2` from
`G_N = 6.67430e-11`; `rho_Lambda` and the absolute `G_cosm` scale with the
footing but the ratio does not.

## 7. Negative control (fires, capable of failing)

Replace `Q_K` by `K` (uncentered variant `-c2 K^2`, the explicitly compared
variant of FINAL_ACTION after eq. 18).  Lapse variation of `(M_P^2/2)(-c2 K^2)`
at fixed geometry, `delta(K^2)/delta ln N = 0` for `Q_K = 0` but
`delta ln(N sqrt(h) K^2) = K^2`-source for the uncentered term:

```
uncentered lapse source = (M_P^2/2) c2 K^2 = (9/2) c2 M_P^2 H^2        (residual 0)

3 M_P^2 (1 + 3 c2/2) H^2 = M_P^2 Lambda + rho      (uncentered Friedmann)
G_cosm/G_N = c_N/(1 + 3 c2/2)                       (in alpha: 2 c_N/(3 c2 + 2))
```

- The homogeneous Friedmann coefficient **changes** from `3 M_P^2` to
  `3 M_P^2(1 + 3 c2/2)`: factor `1 + 3 c2/2`, control residual factor
  `3 c2/2 != 0` for `c2 != 0` — the control fires as required.
- The **local** high-k normalization remains `G_N = G_bare/c_N`: the
  `c2`-block is exactly absent from static metrics (`K_ij = 0`, Section 2,
  numeric lane N3), so the local experiment is unchanged.  This is the
  falsifiable statement of the seed: centering changes the cosmology, not the
  local law.

## 8. Numeric lane (independent of sympy, all checks pass)

`as236_numeric.py` (single-threaded, `ulimit -t 110`, 0.10 s wall, 42.6 MB
peak RSS):

- **N1** — `R4` by direct finite-difference Christoffel symbols on a 41-point
  t-grid with lapse wiggle `N = 1 + 0.3 sin(2t)`, `a = 1.7 e^{0.8 t}`, vs the
  closed form: rel. residual **5.9e-7** (threshold 1e-6).  Refinement to 81
  points (N7): residual 3.7e-8, ratio 16.0 ~ O(h^4) — the FD machinery
  converges onto the closed form.
- **N2** — leaf extrinsic curvature from FD Christoffel symbols:
  `K_ij - (H/N) h_ij` abs. residual **0.0**; `tr K - 3 H/N` = **0.0**.
- **N3** — static weak-field metric: max |K_ij| = **0.0** (exact to machine
  precision on analytic gradients).
- **N4** — eq. (13) homogeneous balance: untuned source
  `rho_b + rho_d = 1.4` leaves residual `-1.344299` (off-shell, visible);
  tuned `rho = 3 M_P^2 H^2 - M_P^2 Lambda` closes to **0.0**.
- **N4b/N4c** — FD of `delta/delta ln N (-c2 Q_K^2)` = **0.0** (centered);
  FD of `delta/delta ln N (-c2 K^2)` = `(M_P^2/2) c2 K^2 N a^3 h` to rel.
  3.2e-11 — the uncentered source is real and correctly located.
- **N5** — negative control numeric: uncentered vs centered Friedmann LHS
  differ by `(9/2) c2 M_P^2 H^2` = 0.091801 (abs.), rel. 1.648 — **the control
  fires**; uncentered-tuned RHS closes to 0.0.
- **N6** — ratio table for alpha in {0.05,0.1,0.2,0.3,0.5,1.0,1.5}:
  `G_N/G_cosm = 1/c_N` exactly; `kappa` back-check 0.5 for both footings;
  `rho_Lambda` 5.8444e-27 (canonical) / 8.4831e-27 (alternative) kg/m^3.

## 9. Lean certificate (zero sorry)

`AS236_ratio_certificate.lean` (verified with
`cd fable_independent_2026/lean_2026 && lake env lean <run>/AS236_ratio_certificate.lean`,
exit 0, zero `sorry`):

1. `ratio_in_alpha`: `1/(1 - alpha/2) = -2/(alpha - 2)` for `alpha != 2`;
2. `uncentered_coeff_factor`: `3(1 + 3 c2/2) = 3 + (9/2) c2`;
3. `control_fires`: `c2 != 0 -> 3(1 + 3 c2/2) != 3`;
4. `ratio_chain`: `G_N = G_bare/c_N, G_cosm = G_bare -> G_N/G_cosm = 1/c_N`;
5. `ratio_chain_alpha`: same chain through `c_N = 1 - alpha/2`.

`#print axioms` (unfiltered) for all five: exactly
`[propext, Classical.choice, Quot.sound]` — no additional axioms, no sorry.

## 10. Outcome, scope and limits

**Claim (supports_scoped_claim):** On the CA5-GNC-R branch, homogeneous
reciprocal centered-clock sector `t_c = 1, Q_K = 0, A_K = 0`, flat slices,
dust, gate inactive, the exact fixed-h lapse equation (13) of FINAL_ACTION
gives `3 M_P^2 H^2 = M_P^2 Lambda + rho_b + rho_d` (bare-Lambda = 0 branch:
`3 M_P^2 H^2 = rho_b + T1 + V0 + Vmix`), and with the separately derived
local high-k normalization of results/AS226 the coupling ratio is
`G_N/G_cosm = 1/c_N = 1/(1 - alpha/2)`, `G_cosm = G_bare`,
footing-independent; the uncentered variant `-c2 K^2` changes the Friedmann
coefficient to `3(1 + 3 c2/2) M_P^2 H^2` and the ratio to
`c_N/(1 + 3 c2/2)` — negative control fires as required — while the local
normalization `G_N = G_bare/c_N` is unchanged (static `K_ij = 0`).

**Not established:** the value of `alpha` (equivalently `c_N`); `kappa = 1/2`
remains an adopted input, not derived; `rho_Lambda` values scale with the
adopted footings; no empirical calibration of `G_cosm` against cosmic
observables is performed here; this is a coupling-ratio prediction for later
bounds, not a full gravity closure.  No claims files were created or
modified; no shared status files were touched.