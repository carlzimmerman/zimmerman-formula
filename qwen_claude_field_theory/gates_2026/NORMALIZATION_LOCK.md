# NORMALIZATION LOCK — Solar-System MOND quadrupole
**Frozen 2026-08-21. Do not re-derive silently. Any script that touches Q2 must import these.**

## 1. The three quantities, and they are three different things

| symbol | defined by | definition |
|---|---|---|
| `c2` | this repo | coefficient of `r^2 P_2(cos t)` in the anomalous potential: `dPhi = c2 * r^2 * P_2` |
| `q_zz` | Milgrom 2009 (arXiv:0906.4817) | `g_i = -q_ij x^j`, `q_ij` traceless axisymmetric, `-2q_xx = -2q_yy = q_zz` |
| `Q2` | Desmond, Hees & Famaey 2024 (MNRAS 530, 1781) | `dPhi = -(Q2/2) x^i x^j (e_i e_j - d_ij/3)` |

## 2. The conversions — both are true, they are NOT the same statement

**Milgrom -> P2 coefficient.** `dPhi = (1/2) q_ij x^i x^j`. With tracelessness,
`q_ij x^i x^j = q_zz r^2 [(3cos^2 t - 1)/2] = q_zz r^2 P_2`. Hence

    c2 = q_zz / 2                                     (FACTOR 2)

**DHF -> P2 coefficient.** `x^i x^j (e_i e_j - d_ij/3) = r^2(cos^2 t - 1/3) = (2/3) r^2 P_2`. Hence

    dPhi = -(Q2/3) r^2 P_2      =>      c2 = -Q2 / 3   (FACTOR 3)

**Therefore, composing the two:**

    Q2 = -(3/2) q_zz            |Q2| = (3/2) |q_zz| = (3/2) q(eta) * (a0/R_M)     (FACTOR 3/2)

`R_M = sqrt(GM_sun/a0)`, so `a0/R_M = sqrt(a0^3 / GM_sun)`.

## 3. The historical error, named so it cannot recur
The 1.45x discrepancy was **the 3/2**. The earlier correction "A = 2, not 3" was the `c2 <-> q_zz`
relation ONLY and was correct as stated; it was then wrongly carried over to `c2 <-> Q2`, where the
factor is 3. **Both factors are real and they apply to different pairs.** In code:

    q_milgrom(eta) = 2 * |c2|          # compare to Milgrom's published q(eta)
    |Q2|           = 3 * |c2| * (a0/R_M) = (3/2) * q_milgrom * (a0/R_M)   # compare to Cassini

## 4. External field and the implicit relation
QUMOND consumes the **Newtonian** external field. Milgrom tabulates `q` against the **true** field.
They are related by `eta = eta_N * nu(eta_N)`, which must be inverted numerically. Feeding `eta`
where `eta_N` belongs corrupts the log-SLOPE of q(eta) (0.814 instead of 1.237) and no constant
calibration can repair it.

## 5. Numbers frozen for this project
- Cassini bound (DHF's own): `Q2 = (3 +/- 3) x 10^-27 s^-2`.
- Galactic external field at the Sun: `g_ext = V0^2/R0`, **value adopted from DHF once retrieved**;
  the placeholder used before literature return is `V0 = 233 km/s`, `R0 = 8.20 kpc`
  -> `g_ext = 2.1456e-10 m/s^2`.  **FLAGGED AS PLACEHOLDER.**
- a0 footings: canonical `9.3619e-11`, alt `1.1279e-10`. Standard MOND `1.2e-10` for DHF comparison.

## 6. Validation status of the machinery
Reproduces Milgrom 2009's published `q(eta)` anchors {1.0: 0.094, 1.5: 0.159, 2.0: 0.221} to
**3.2%**, log-slope **1.224 vs 1.237**, with **no fitted factor**. See `gate3_nSS_2026.py` Part B.
