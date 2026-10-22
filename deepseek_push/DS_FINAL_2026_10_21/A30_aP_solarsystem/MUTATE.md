# A30 — mutation record

`python3 a30_checks.py --mutate <NAME>` alters **one term or one premise** and must break the checks it
targets, exiting 1. Nine mutations, nine bites. Captured stdout below (long `value=` fields truncated at
230 chars with `...`; the full text is reproducible with the command).

Clean run for comparison:

```
K1   PASS value=residuals=['0', '0', '0', '0']  thr=all exactly 0
...
A30 COMPLETE: 11/11 checks PASS.          exit 0
```

---

## 1. `drop_linear` — remove the `(GM/L*²) r` term from `Φ` (the "no anomaly" reading)

Only the linear potential is dropped; the Newtonian `−GM/r` and `ψ` are untouched.

```
K1   FAIL value=residuals=['-2*G*M/(L**2*r)', '-2*G*M/(L**2*r)', '0', '0']  thr=all exactly 0
A30 COMPLETE: 10/11 checks PASS.          exit 1
```

K1's residual is exactly `−2GM/(L*²r)` in *both* the lapse equation and the P equation — the linear term
is not optional: without it the charge has no counterterm and (4) fails. (The Fourier residuals stay 0
because the delta part is unchanged, which is why both spaces are checked.)

## 2. `outward` — flip the sign of `a_P` (make the anomaly repulsive)

```
K2   FAIL value=a_nonNewton=G*M/L**2  d/dr=0  u_P=G*M/L**2  thr=-GM/L^2, d/dr=0, u_P=a_P, sunward
A30 COMPLETE: 10/11 checks PASS.          exit 1
```

The constant and `d/dr=0` halves still pass; the **sunward** assertion fails. A repulsive constant term
would be a different theory (and would add to `Λ` rather than compete with it).

## 3. `Lstar_1kpc` — move the stiffness length to 1000 pc

```
K3   FAIL value=aP(Sun)=1.393832e-19 aP(Earth)=4.1864e-25 aP(1kg@1m)=7.0098e-50 aP/a0=1.4891e-09
K7   FAIL value=Mercury: 1.855e-08 mas/yr vs 0.006 -> 323501.7x ... || binding=Mars 9883.29x
A30 COMPLETE: 9/11 checks PASS.          exit 1
```

`a_P ∝ L*⁻²`: at 1000 pc the anomaly is `1.39e-19` (1736× smaller), the prefactor check fails and every
precession margin grows by the same factor. This is the mutation that shows the number is *not*
`L*`-independent — the prediction is only as sharp as A20's `[24, 90] pc` window.

## 4. `identity_blind` — assert the tasking's `L* = c²/a0`

The physics is unchanged; the check is told to accept the identity.

```
K4   FAIL value=c^2/a0=9.602e+26 m (31.1 Gpc) = 1.297e+09 L*; aP(then)=1.439e-34;
          A20 L*(sigma_c^2/a0)=23.45 pc  thr=ratio>1e6 and A20 recovers 24 pc
A30 COMPLETE: 10/11 checks PASS.          exit 1
```

K4 is deliberately written *against* the tasking: it passes only if the identity is refuted at `>1e6`.
Imposing it would report `a_P = 1.44e-34 m/s²`, i.e. erase the anomaly by 18 orders of magnitude.

## 5. `no_drift` — set `a_P = 0` inside the orbital response

```
K5   FAIL value=rad_amp=0.000000e+00 (pred 0.000000e+00) along=0.000000e+00 (pred 0.000000e+00)
          err=inf/inf  thr=both < 5e-3
K6   FAIL value=Mercury: dR(10yr)=0.000m(max 0.00) ... Saturn: dR(10yr)=0.000m(max 0.00)
A30 COMPLETE: 9/11 checks PASS.          exit 1
```

Both the analytic-vs-numerical cross-check and the drift table go to zero. K6's monotonicity/positivity
assertion fails. This proves the drift numbers are *produced* by `a_P`, not by the fitting machinery.

## 6. `fisher_forced` — declare the Fisher result unacceptable

```
K8   FAIL value=sigma(aP)=1.437e-15 (aP/sigma=0.168) sigma(k)=8.94e-28 (k/sigma=3.65e-09) rho=-0.524
A30 COMPLETE: 10/11 checks PASS.          exit 1
```

No number changes; the check's acceptance window (a `0.17σ` effect, `|ρ|<0.9`) is what fails. This
mutation guards the *conclusion* — a future recalculation that pushed `a_P/σ` above 50 would trip it.

## 7. `tide_claim` — claim the `a_P` field is tideless

```
K9   FAIL value=aLam(1AU)=4.881e-25 ... tide_ratio=4.081e-14 EMdisp=15.7um
          thr=ratio=4.96e8, r_cross=2404 pc, tide_ratio=4.08e-14
A30 COMPLETE: 10/11 checks PASS.          exit 1
```

A constant-*magnitude* radial field is not a uniform field: `∇a = −(a_P/r)(δ_ij − r̂ᵢr̂ⱼ)`, a `1/r` tide of
relative size `r²/L*²` = `4.08e-14`. The mutation is the (tempting) wrong statement "constant force ⇒ no
tide" and it is caught by the `4.08e-14` assertion.

## 8. `llr_blind` — declare the lunar range insensitive

```
K10  FAIL value=aP(Earth)=7.268e-22 bound_offset=0.10nm (freefall 36um) dmu/mu=2.69e-19
          aP(1kg@1m)=1.217e-46 (aP/g)=1.82e-36
A30 COMPLETE: 10/11 checks PASS.          exit 1
```

K10 passes only if the Earth–Moon offset is `a/ω_m²` (0.10 nm, the *bound* response) rather than the
free-fall `½at²` (36 μm). The mutation is the `½at²` confusion — the same error D8 warns about for the
planets, at laboratory scale.

## 9. `falsifier_flip` — invert the falsifier's logic

```
K11  FAIL value=prediction=2.4198e-16 (vs 0)  need sigma_dg<=2.420e-16  margin bracket=[5.69,151]x
A30 COMPLETE: 10/11 checks PASS.          exit 1
```

Numbers unchanged; the assertion "prediction below every bound, bracket > 1" is forced false. Guards
against a future edit that would report the anomaly as *excluded* while the arithmetic says otherwise.

---

**Summary.** 9/9 mutations break at least one declared check and exit 1; the clean run is 11/11 and
exit 0. The three that change no arithmetic (`identity_blind`, `fisher_forced`, `falsifier_flip`) guard
*premises and conclusions* rather than numbers, which is where this lane's real risk sits.
