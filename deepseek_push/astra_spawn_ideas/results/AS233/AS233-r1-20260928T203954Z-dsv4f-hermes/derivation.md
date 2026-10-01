# AS233 — High-acceleration preferred-frame vector response (Tier-0b)

**Run:** `AS233-r1-20260928T203954Z-dsv4f-hermes`
**Branch:** CA5-GNC-R physical-metric branch (FINAL_ACTION.md eq. (4), pinned `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`)
**Task:** AS233_derive_the_high_acceleration_preferred_frame_vector_response.md
**Task SHA-256:** `09b8f90719ee5bf44d25517e0f9e63fffb43460ab2d7d8fab819947438d584cd` (verified before execution)

---

## 1. Pinned conventions and displayed target (seed step 1)

Action: CA5-GNC-R (FINAL_ACTION eq. (4)), units `M_P^2/2`, flat leaf, dust,
inactive heat gate (`f = G'(Y_h) = 0` on the compact leaf at high acceleration),
mean-normalized nonzero modes, `k = (k_x, 0, 0)`. Coefficients fixed before
numerics: `c_N = 1 - alpha/2` (action definition), `kappa = 1/2` adopted.

Static weak-field metric (AS226 spelling, pinned in as226_derive.py):
`ds^2 = -(1+2 Phi_F) dt^2 + (1-2 Psi) dx^2`, `Phi_F = -Phi_t = -Psi` on shell.
In the k-space ladder (`Phi` = spatial coefficient `g_ii = 1 - 2 Phi`,
`Psi` = temporal coefficient `g_00 = -(1 + 2 Psi)`; no-slip `Psi + Phi = 0`),
the certified Einstein density is

    E_A = 2 |D Phi|^2 + 4 D Psi . D Phi                (AS226 line 41)

with the flat leaf gradient `D` (mode picture: `|D f|^2 = k^2 f^2`).

**Displayed target** — the transverse shift of the physical metric:
`B2 = g_02` at first order in the source velocity `w_b` (moving baryon
current `J_i = rho_b w_i`), normalized by the measured Newton constant:

    alpha_1 = 2 * coeff(g_02, w_2) / U_amp,    U_amp = -Psi_k / R_k

(Will dictionary, identical spelling to f31_ppn_k4_alpha1.py and
gen_aest_alpha1_c2c4.py: `alpha_1 = 2 * coeff(g_02, w_2) / U_amp`).

## 2. Transverse shift equation from CA5-GNC-R (seed step 2)

The shift is NOT imported from another scalar architecture. It is sourced at
`O(w_b)` through the clock normal of the current action:

- The clock feeding `V_a` and the compensator uses the unit normal
  `n = -tau / sqrt(X_tau)`, `tau_mu = (1, w_b w_1, w_b w_2, 0)`,
  `X_tau = -g^{mu nu} tau_mu tau_nu`. Because `X_tau` contains
  `-2 w_b g^{0 i} w_i`, the metric couples into the normal through `g^{0i} w_i`
  — the channel through which a source moving across the preferred foliation
  sources `g_02`. The sqrt is expanded in a polynomial series kept to the
  retained orders `(eps^2, w_b^1)`; unit consistency `n . n = -1` is enforced
  to that order (script unit check = 0, Lean-certified, see §6).

- The full action density (units `M_P^2/2`) at `(eps^2, w_b^1)`:

      L2 = E_A + V_a + c_N ell a . D W_b - c2 Q_K^2 + |D B2|^2 - 2 Lambda
         - 16 pi G_T rho (-H_00/2)

  with `V_a = alpha |a - DZ|^2 + 4 a . DZ - 2|DZ|^2 - 4 c_N DZ . DU`,
  a = `D ln N` (lapse acceleration, built from Christoffel symbols of the
  metric including the boosted normal), the Z/U ties of FINAL_ACTION at
  `f = 0`:

      Z = (ell S_k/4) F,   U = F - Z,

  the heat-saddle compensator `c_N ell a . D W_b`, `W_b = S_h U`, the
  trace-mixing block `-c2 Q_K^2`, `Q_K = K` (extrinsic curvature of the
  boosted foliation; `K = 0` on the flat background), and dust matter.

- **Window** `S_k -> 0` (high acceleration, AS226): `Z -> 0`, `DZ -> 0`,
  the F/U sector decouples from the brackets at `(eps^2, w_b^1)`, and the
  compensator vanishes with `S_h`. This is recorded, not silently assumed:
  `alpha_1` is verified independent of `ell` at three values (see §4).

- The bracket equations `delta L2 / delta(bra)` are projected to the
  diagonal (Es/Eis-balanced) mode sector and solved as a two-rung ladder:
  static rung `(wb^0)` for `{Psi, Phi, s22}` and `wb^1` rung for
  `{d1_Psi, d1_Phi, d1_B2, d1_s22}` (the shift amplitude `d1_B2` is the
  unknown that carries `alpha_1`).

**Derived shift equation** (the `B2b` bracket at `wb^1`, cell
`alpha = 3/10, ell = 1/25, c2 = 1/2`, `S -> 0`, after substitution back):

    the solved fields satisfy all five original brackets to zero residual
    at (wb^0, wb^1) — see §5 residuals.

## 3. PPN gauge and the alpha_1 combination (seed step 3)

The ladder is already in the f31 PPN gauge conventions (harmonic-ish gauge,
`H[0,1] = 0`, boost `tau = (1, w_b w_i)` with `w_3 = 0`; `B3 = s23 = 0`
identically, `s22` solved live in both rungs). The alpha_1-sensitive
combination is the transverse shift amplitude

    c2t = coeff(d1_B2k, w_2) / R_k

and the measured-G-normalized ratio is read with `U_amp = -Psi_k / R_k`
(Wil dictionary; `G_N = G_bare / c_N` scalings cancel in the ratio, AS226).

**Main result.** At exact rational cells, `alpha_1` over the full tested
grid `alpha in {0, 1/10, 3/10, 1/2, 3/4, 1}`, `c2 in {0, 1/4, 1/2}`
(18 cells, all exact rational arithmetic):

    alpha_1(alpha, c2) = 4 (alpha + 2 c2) / (2 - c2)

Verified: (i) by direct symbolic-c2 solve at `alpha = 3/10` giving
`-2(20 c2 + 3)/(5(c2 - 2)) = 4(3/10 + 2 c2)/(2 - c2)`; (ii) by matching all
18 cells; (iii) c2 -> 0 recovers `2 alpha` (pure clock-origin response,
khronon-like); (iv) alpha -> 0 recovers `8 c2/(2 - c2)` (trace-mixing
channel alone); (v) Einstein limit `alpha = c2 = 0` gives `alpha_1 = 0`.

Reference cell C1 `(3/10, 1/25, 1/2)`:
`alpha_1 = 52/15 ≈ 3.4667`, with ladder amplitudes
`c2t = 416 pi / 51`, `U_amp = 80 pi / 17`.

**Ell-independence in the window:** `ell in {1/25, 1/2, 1}` all give
`52/15` at C1 (compensator vanishes with `S_h`; recorded, not assumed).

**Dimensionless statement:** `alpha_1` is a dimensionless shift-to-Newtonian-
potential ratio; both footings `a0 = 9.3619e-11` and `a0 = 1.1279e-10 m/s^2`
give the same coefficient (each separately fixes `rho_Lambda` such that
`kappa_back = a0/(c sqrt(G rho_Lambda)) = 1/2` exactly, verified:
`rho_Lambda = 5.844412e-27` and `8.483090e-27 kg/m^3`).

## 4. Controls (capable of failing)

- **Anchor A (capability gate):** pure Einstein `alpha = ell = c2 = 0`:
  no-slip `Psi_k + Phi_k = 0` (PASS), `alpha_1 = 0` exactly (PASS —
  preferred-frame response requires the clock sector).
- **Substitution-back:** all five original brackets (Psib, Phib, B2b, s22b,
  Fb) evaluated with the solved fields give residuals `(0, 0)` at
  `(wb^0, wb^1)` (PASS; residuals measured, not booleans).
- **N1 (negative control, trace-mixing branch value `alpha_1 = -4E` without
  an action dictionary):** at C1, `alpha_1 + 4 E = 4E + 52/15`, nonvanishing
  for every `E > 0` (residuals `3.5067`, `4.4667`, `7.4667` at
  `E = 1/100, 1/4, 1`): REJECTED.
- **N2 (falsifiable substitution-back):** forcing `coeff(g_02,w_2) = -2 E U_amp`
  (i.e. `alpha_1 = -4E`), the original B2 bracket is NOT annihilated:
  residual `16 pi rho_k w_2 (-15 E - 13)/17 != 0` (≈ `-38.882` at
  `E = 1/100`): REJECTED.
- **Unit-normal consistency:** `Aup . Adn + 1 = 0` at `(eps^2, w_b^1)`
  (PASS), Lean-certified (see §6).

## 5. Measured residuals and amplitudes (reference cell C1)

    Psi_k = -80 pi rho_k / 17        (static; U_amp = 80 pi / 17)
    Phi_k = +80 pi rho_k / 17        (no-slip Psi + Phi = 0)
    s22_k = 0, F_k = 0
    d1[B2k] = 416 pi rho_k w_2 / 51  (c2t = 416 pi / 51)
    alpha_1 = 2 c2t / U_amp = 52/15

Brackets with solved fields: all five zero at both orders (C1b checks).

## 6. Lean 4 certificate

`as233_closed_form.lean` (verified `lake env lean`, exit 0, zero `sorry`):

- `sqrt_series_unit_identity`: `(1+t)(1 - t/2 + 3 t^2/8)^2 - 1 = (5/8)t^3 - (15/64)t^4 + (9/64)t^5` (ring_nf)
- `alpha1_closed_form_cell`: `4(3/10 + 2(1/2))/(2 - 1/2) = 52/15` (norm_num)
- `alpha1_dictionary_cell`: `2 c2t / U = 52/15` given `c2t = 416 pi / 51`,
  `U = 80 pi / 17` (field_simp + norm_num)
- `alpha1_clock_limit`: `4(alpha + 0)/(2 - 0) = 2 alpha` (ring)
- `alpha1_trace_limit`: `4(0 + 2 c2)/(2 - c2) = 8 c2/(2 - c2)`, `c2 != 2` (field_simp + ring)
- `alpha1_einstein_limit`: `= 0` (norm_num)
- `negative_control_residual`: `4(3/10 + 2(1/2))/(2 - 1/2) + 4 E != 0` for `E > 0` (norm_num + linarith)

`#print axioms` for every theorem: subseteq `{propext, Classical.choice,
Quot.sound}` (verified on the compile host; nothing written into
`fable_independent_2026/lean_2026/`).

## 7. Domain, limitations, next steps

**Tested domain:** one weak baryonic dust source moving uniformly relative to
the preferred foliation, first order in velocity, high-acceleration window
`S_k -> 0`, massless cold dust `rho_d = 0`, plane-wave nonzero modes, gauge
`H[0,1] = 0`, `w_3 = 0`. Exact rational algebra; all residuals measured.

**Limitations:** (i) the `S_k -> 0` window freezes the Z/U/F sector — the
`S_k != 0` corrections and the compensator channel are not in this result;
(ii) `alpha_2`, `alpha_3` (second order in velocity) are out of scope;
(iii) `Q`, `RAR`, `MU2`, historical EXP and unfiltered MONO branches were not
used — this is a CA5-GNC-R statement only; (iv) the Einstein sector uses the
certified AS226 density spelling (E_A), not a re-derived Ricci tower — the
full-4D Ricci route reproduces `alpha_1 = 0` in the Einstein limit but broke
the no-slip static identity and was abandoned as the certified route; (v) the
physical-metric ≈ numeric coefficient `52/15` at the reference cell is
O(1)-large; whether parameters must be restricted to make `alpha_1` fit
constraints (e.g. solar-system bounds) is a parameter-space question outside
this derivation; (vi) both footings apply identically because the result is
dimensionless; no footing-specific numerics were needed.

**Classification:** the same-action vector response coefficient is **derived**
(with explicit residuals); it is not promoted to complete gravity closure.

## 8. Files (hashes in result.json)

    as233_derive.py         runnable derivation (v6, canonical)
    derive_raw.out          raw output of the bounded run
    time_mem_derive.txt     /usr/bin/time -l record
    as233_closed_form.lean  Lean 4 certificate
    lean_check.out          lake env lean output (exit 0)
    as233_derive_v3/4/5/6.py  preserved failed/iterative attempts
    this file, result.json