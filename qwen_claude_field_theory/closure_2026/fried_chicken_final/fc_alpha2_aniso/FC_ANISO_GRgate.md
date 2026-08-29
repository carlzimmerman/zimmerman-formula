# FC-AeST preferred-frame program -- PHASE 1: the GR-validation gate

**File:** `fc_aniso_grgate.py` (14/14 certificates, exit 0). Run: `python3 fc_aniso_grgate.py`.
**Date:** 2026-08-28. **Scope:** build the full **anisotropic O(w^2) 1PN machinery** and prove it
reproduces the GR anchors **gamma_PPN = 1, alpha_1 = alpha_2 = 0** before it is trusted for any AeST
preferred-frame number. This is the trust anchor the previous attempts skipped.

---

## 1. Why this gate exists (what broke before)

`fc_alpha2_preferred_frame_2026.py` used the **isotropic** spatial ansatz `h_ij = -2 Phi delta_ij`
and failed its own internal checks: the extracted `alpha_1 != -4 K_B` [D1] and the two `alpha_2`
extractions disagreed [D2]. Diagnosis (FINAL_PPN.md): a moving/preferred source carries a preferred
direction `w`, so it sources a genuinely **anisotropic** spatial stress; the traceless-ij equations
are then non-trivial and the isotropic ansatz is not a solution, so its `alpha`'s are meaningless.

**The fix, and the order-counting fact that makes it clean.** In PPN bookkeeping `U ~ eps^2`,
`w ~ eps`. The anisotropic spatial terms are `~ w^2 U ~ eps^4` = **2PN**, i.e. BEYOND the `O(eps^2)`
truncation of `g_ij`. So:

- the machinery must **keep the full anisotropic `h_ij`** (`A w^2 delta + B w_i w_j + d_i d_j chi +
  d_(i V_j)`) so the field equations actually close -- this is exactly what the isotropic ansatz
  could not do;
- but `gamma_PPN` is read from `g_ij` at `O(eps^2) = 2 U delta_ij` (=> `gamma = 1`), and `alpha_1,
  alpha_2` live in `g_0i` (`O(eps^3)`) and `g_00` (`O(eps^4)`).

The gate proves both halves on pure GR.

---

## 2. The machinery (the same pipeline AeST will use)

Built in Fourier, mostly-plus `eta = diag(-1,1,1,1)`, exactly the
`sec11_alpha12_preferred_frame.py` pipeline that is validated there against Blas-Pujolas-Sibiryakov --
re-used here with a **fluid** source instead of a field stress.

| ingredient | implementation |
|---|---|
| moving source | rigid motion at `w`: every field `~ f(x - w t)`, so `d_t = -(w.grad)`, i.e. **omega = k.w EXACTLY** (rigid retardation). `d_mu -> i K_mu`, `K = (-omega, k)`. |
| boosted perfect fluid | dust `T^{mu nu} = rho' u^mu u^nu`, `u^mu = gamma(1, w^i)`, `rho' = k^2 Uhat/(4 pi G)` fixed by the `O(w^0)` Newton limit `lap U = -4 pi G rho'`. |
| metric | GENERIC 10-component `h_{mu nu}` (no ansatz imposed anywhere before extraction). |
| field equations | full linearized Einstein tensor `G1_{mn}[h]`; **harmonic gauge imposed AFTER** via the trace-reversed propagator `hbar_{mn} = 16 pi G T_{mn}/(k^2 - omega^2)`, `h = hbar - (1/2) eta hbar`. |
| extraction | `g_0i = a V_i + b W_i`, `g_00^(w^2) = c w^2 U + d (w.x)^2 U/r^2`, via the position dictionary `(k.w)k_i/k^2 Uhat <-> (1/2)(V_i - W_i)` and `(k.w)^2/k^2 Uhat <-> (1/2)w^2 U - (1/2)(w.x)^2 U/r^2`. |

`V_i = w_i U`, `W_i = (w.x) x_i U/r^2` (the moving point-mass PPN potentials).

---

## 3. The certified result (GR)

The harmonic solution (linear in `U`, `O(w^2)`), position form:

```
g_00 = -1 + 2U + [ 4 w^2 U - (w.x)^2 U/r^2 ]        (rest-mass source convention; +w^2 U in the
                                                     lab-potential convention -- see note below)
g_0i = -4 w_i U
g_ij = (1 + 2U) delta_ij  +  O(eps^4) anisotropic   (2PN: 4 w_i w_j U - (w.x)^2 U/r^2 delta_ij)
```

**Extraction** (`gamma = 1` verified first):
```
(a, b) = (-4, 0)      (c, d) = (4 or 5, -1)
alpha_1 = -2(a + b) - (4 gamma + 4) = -2(-4) - 8 = 0        [E1]
alpha_2 = -(2b + d) - 1             = -(-1)   - 1 = 0        [E2]
```

### Certificates (all pass, sympy `== 0`)

- **[B1]** conservation `K^mu T_{mu nu} = 0` -- holds because `omega = k.w` exactly (rigid motion);
  a harmonic solution therefore exists. **[COMPUTATION/THEOREM]**
- **[C1]** full linearized Einstein `G1_{mn}[h] = 8 pi G T_{mn}` satisfied for **ALL 10 components**
  by the anisotropic harmonic solution (gauge imposed after `G1` is built). **[COMPUTATION]**
- **[C2]** harmonic gauge `K^mu hbar_{mu nu} = 0` holds (`= 16 pi G K^mu T_{mu nu}/(k^2-omega^2) = 0`
  by [B1]). **[THEOREM]**
- **[D1]** `O(w^0)` Newton normalisation `h00 = 2 Uhat`. **[COMPUTATION]**
- **[D2]** `g_ij = (1 + 2U) delta_ij` at `O(eps^2)` => **gamma_PPN = 1**. **[COMPUTATION]**
- **[E1]/[E2]** **alpha_1 = 0, alpha_2 = 0**. **[COMPUTATION]**
- **[F1]** an **independent** construction -- the exact Lorentz boost of static 1PN Schwarzschild --
  reproduces the Fourier `(a,b,d)` EXACTLY; the only difference is `c` (the `w^2 U`/Phi_1 sector),
  a rest-mass-vs-lab-potential source convention that does **not** enter `alpha`. **[COMPUTATION]**
- **[F2]** the oracle gives `alpha_1 = alpha_2 = 0` independently. **[COMPUTATION]**
- **[G1-G3]** gauge robustness: the residual gauge `xi_0 = kappa (w.x) U` shifts
  `(a,b,c,d) -> (a-kappa, b+kappa, c+2kappa, d-2kappa)`, but `alpha_1 = -2(a+b)-8` and
  `alpha_2 = -(2b+d)-1` are built from the **gauge-invariant** combinations `a+b` and `2b+d` and
  stay identically 0. So the extraction is gauge-clean -- it does not matter which gauge the AeST
  solution arrives in. **[THEOREM]**
- **[H1]** the extraction **inverts Will's standard-PPN definition exactly** for symbolic
  `(alpha_1, alpha_2)` -- so the GR zero is a genuine measurement, not a trivial always-zero output,
  and the extraction **slope is correct**. **[COMPUTATION]**
- **[H2]** a physical `W_i` deformation `delta` shifts `alpha_2 -> -2 delta` (nonzero): the machine
  **detects** preferred-frame effects. **[COMPUTATION]**
- **[I1]/[I2]** the diagnosis of the old `[D2]` disagreement (see below). **[COMPUTATION]**

---

## 3a. The methodological correction the gate exposes ([I1], [I2]) -- the real cause of [D2]

The earlier attempts read `alpha_2` from the **`g_00` anisotropic sector alone** (the `P_A /
P_Aparallel` channel on `Psi = g_00`). The gate proves that on the **exact GR** metric this gives a
**spurious, self-inconsistent** answer:

```
g_00-ALONE, channel 1 (from d):  alpha_2^naive = d   = -1        <- nonzero (WRONG; GR has alpha_2=0)
g_00-ALONE, channel 2 (from c):  alpha_2^naive = -c  = -4 or -5  <- nonzero AND != channel 1
```

`g_00` alone is **gauge-dependent** -- the residual gauge `xi_0 = kappa(w.x)U` shifts both `c` and `d`
(`[G1]`), so no PPN parameter can live in `g_00` by itself. **This -- not only the isotropic ansatz --
is why the two `alpha_2` extractions disagreed in `[D2]`.** The fix is to fold in the `g_0i` `W_i`
coefficient `b` and use the **gauge-invariant** combination `2b + d`:

```
alpha_2 = -(2b + d) - 1  (gauge-invariant; g_0i + g_00)   =>  GR: -(0 - 1) - 1 = 0.   [I2]
```

Now the two determinations agree because they are the **same** invariant. **Action item for PHASE 2:**
the AeST solve must extract `alpha_2` from `2b + d` (or equivalently first gauge-fix to standard PPN),
never from the `g_00` `(w.x)^2` coefficient alone.

---

## 4. Honesty ledger

- **gamma_PPN = 1, alpha_1 = alpha_2 = 0 for GR** -- **COMPUTATION**, two independent constructions
  (Fourier fluid solve + Lorentz-boost oracle), gauge-invariant, 14/14 certificates.
- **Extraction slopes** `-2(a+b)-(4gamma+4)` and `-(2b+d)-1` come from Will's standard-PPN metric
  (2018, "Theory and Experiment in Gravitational Physics" 2nd ed., eq. 8.2:
  `g_0j = -(1/2)(4gamma+3+alpha_1-alpha_2)V_j - (1/2)(1+alpha_2)W_j`, and the standard-gauge
  `A`-potential coefficient `= 0`, i.e. `d_std = 0`). That is the **DEFINITION** of `alpha_1,alpha_2`
  -- unavoidable **EXTERNAL-INPUT**. The gate validates: (i) the **offset** (GR gives 0), (ii) that
  my algebra **inverts** the definition correctly [H1], (iii) gauge-independence [G]. The definition
  itself is textbook and is not re-derived.
- **Not claimed:** no `alpha_2` number for AeST is produced here. This is only the GR gate.
- **PHASE 2 slope re-anchor.** Before any AeST `alpha_2` is cited, the slope is independently
  re-anchored by the **established `alpha_1 = -4 K_B`** (fc_ctensor_map_2026.py); a recommended extra
  guard is to run the SAME machinery on Einstein-aether (add the boosted aether field + its stress)
  and match the Foster-Jacobson `alpha_1(c_i), alpha_2(c_i)` closed forms -- a nonzero known-answer
  anchor for the `alpha_2` slope, of which GR is the `c_i -> 0` sub-limit.

## 5. Verdict

**GR-VALIDATION GATE: PASSED.** The full anisotropic `O(w^2)` machinery -- boosted fluid source,
retardation `omega = k.w`, generic 10-component metric solved in harmonic gauge (imposed after the
field equations), gauge-invariant PPN extraction -- reproduces `gamma_PPN = 1` and
`alpha_1 = alpha_2 = 0`. The machine is trustworthy; the isotropic-ansatz failure mode is diagnosed
and fixed. Ready for PHASE 2 (the AeST + J_10 + c_2* scalar-retained solve).
