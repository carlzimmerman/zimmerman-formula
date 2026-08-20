# I003 — Disc (non-spherical) correction to the local law

**Verdict:** KILL
**Decisive number:** `s_disc / s_sph = 1.072 – 1.104` over both kernel families and both a0 footings. The full-disc PDE solution needs **MORE** saturation than the spherical algebraic law, by **7.2 %–10.4 %** — the pre-registered PASS (`s_disc < 0.1`) is not met (smallest `s_disc = 0.4662`), and the KILL condition (`|shift| < 20 %`) fires. The framework's ephemeris/galaxy gap goes **232x → 249x–257x**, i.e. *wider*, not narrower.
**Script:** `runs/i003_disc_correction.py`   (checks: 14/14, exit 0, ~236 s)

## Hypothesis

From IDEAS.md: "`u J_Y(u^2) = g_bar` is exact only in spherical symmetry; discs may shift the
RAR requirement on `s`. DO: solve the AQUAL-type equation for a Miyamoto–Nagai disc numerically,
compare `u(r)` with the spherical algebraic answer. PASS: the disc value of `s` needed drops below
0.1. KILL: shift is < 20 %." The implicit bet is that the non-spherical (solenoidal/curl) piece the
local algebraic law throws away *lowers* the saturation needed to reproduce the RAR, and thereby
closes the ephemeris/galaxy incompatibility.

## What I actually did

The solver `runs/i003_disc_correction.py` **pre-existed this session** (dated Aug 17, with no
result file and no LEDGER row written), i.e. a prior session completed the compute but not the
write-up. Consistent with the anti-manufacture discipline stated in `results/I001_efe_factorisation.md`
("a second independent re-derivation of the same 800-line nonlinear solve would only risk
introducing error"), I **ran and verified it rather than re-authoring it**, and reproduced its
exit-0 result independently (`exit code = 0`, 14/14 checks). The script solves the quasi-static
AeST PDE `div[ J_Y(|grad chi|^2) grad chi ] = 4 pi G rho` for a Miyamoto–Nagai disc by an
axisymmetric finite-volume damped-Newton iteration on a log-`r` grid, comparing the in-plane
anomalous field `u(r)` against the spherical algebraic answer `U_alg(y; s)`. Both kernel families
(`J_Y = v/(1-v/s)`, the a0-line at `s=1/2`, and `J_Y = v/(1-v/s)^2`) and both a0 footings
(`a0 = 9.3619e-11` canonical / `1.1279e-10` alt) are carried to the verdict. Three gates (linear
kernel on the full disc, and two spherical sources) prove the non-spherical machinery reproduces
the exact algebraic law to ~0.07 % before any disc number is claimed.

## The math

Local law, spherical symmetry (Gauss collapses the PDE):
```
u J_Y(u^2) = g_bar ,  U = u/a0 ,  y = g_bar/a0
family 1:  J_Y = v/(1-v/s)   ->  U^2 + (y/s) U - y = 0
           =>  U_alg(y;s) = ( -y/s + sqrt((y/s)^2 + 4y) )/2 ,  U->sqrt(y) (y->0), U->s
           at s=1/2:  U = sqrt(y^2+y) - y  (the a0-line),  U(2) = sqrt(6)-2 = 0.449490
family 2:  J_Y = v/(1-v/s)^2  ->  U = s sqrt(y)/(s+sqrt y)
```
Full-disc PDE solved in pure flux form per cell:
```
sum_faces  A_f [ mu_f (dchi/dn)_f - (grad Phi_N . n)_f ] = 0 ,   mu = J_Y(u^2)
Newtonian face fluxes by 4-pt Gauss-Legendre on the EXACT analytic MN gradient
=> exact enclosed mass to quadrature; thin disc need not be a resolved density field.
```
The disc ratio is the geometry correction: `f(R) = u_disc(R) / U_alg( y(R); s )`. To hold the RAR's
`U(y=2) >= 0.4` one inverts `f` at the radius where `y(R)=2` and scans `s`:
```
s_for_target(y, U_target, family=1) = y*U_target / (y - U_target^2)
s_disc  =  interp( 0.4,  {U(y=2; s) over the s-scan} ,  s-scan ) , bracketed strictly inside
ratio   =  s_disc / s_sph   (family-robust, so it does not depend on the kernel-family ambiguity)
```

## Numbers

Dimensional footing: `a0 = 9.3619e-11` (canonical) / `1.1279e-10` (alt) m/s²; the footing enters
only through which radius carries which `y`, and BOTH are reported.

| quantity | value | note |
|---|---|---|
| gates: linear-kernel disc | residual 4.13e-14, accuracy 7.34e-4 | disc machinery exact to ~0.07 % |
| gates: spherical (extended b=4) | 3.07e-4, y in [2.2e-2, 1.8] | reproduces `u J_Y(u^2)=g_bar` |
| gates: spherical (compact b=0.05) | 5.71e-4, y up to 1.1e4 | exercises saturated branch |
| two independent solvers agree | 1.15e-6 over 0.5–60 kpc | Newton vs line relaxation |
| grid/tol spread | 1.43e-3 over 6 variants | f(3)=0.67201 to 5 dp |
| `f(3 kpc)` M1 canonical / alt | 0.6720 / 0.6777 | in-plane u / U_alg |
| `f(8 kpc)` M1 canonical / alt | 0.9201 / 0.9209 | |
| `f(20 kpc)` M1 canonical / alt | 0.9832 / 0.9836 | |
| largest in-plane deficit `|f-1|` | 0.6895 (69.0 %), 0.508 dex | committed RAR scatter = 0.108 dex |
| flux term Gauss discards `|mu grad chi - grad Phi_N|/|grad Phi_N|` | up to 0.976 in plane | O(1), not O(1 %) |
| `s_sph` (RAR U(2)>=0.4), fam 1 / fam 2 | 0.43478 / 0.55776 | gap 181x / 232x |
| `s_disc`, fam1 canon/alt | 0.46619 / 0.47319 | |
| `s_disc`, fam2 canon/alt | 0.60567 / 0.61581 | smallest s_disc = 0.46619 |
| **ratio `s_disc/s_sph`** | **1.072 – 1.104** | **all four > 1 (adverse)** |
| gap re-priced (fam 2) | 232x → 249x–257x | WIDER, not narrower |

## Why this verdict

Pre-registered PASS = "the disc value of `s` needed drops below 0.1." The smallest `s_disc` found
anywhere is **0.4662** — two orders of magnitude above 0.1; PASS does not fire. Pre-registered KILL
= "the shift is < 20 %." The disc-to-spherical shift is **7.2 %–10.4 %**, so the KILL condition
fires. The sign is unambiguously adverse in every family/footing combination: the disc produces
*less* anomalous acceleration than the spherical algebraic law (`f < 1` everywhere in 1–40 kpc), so
reproducing the same RAR requires a *larger* `s`, widening the ephemeris/galaxy gap rather than
closing it. Verdict: **KILL**, in the adverse direction.

A second, independent finding (check 2): the task sheet's two sides of the "233x gap" were priced
with **two different kernels**. `U(2)=0.449` / the a0-line is **family 1** (`J_Y=v/(1-v/s)`, which
needs `s>=0.435`, gap 181x); `s>=0.558` / the 233x is **family 2** (`J_Y=v/(1-v/s)^2`). This does
not rescue the idea — the disc correction moves both the same way — but it means the headline
"233x" is not the a0-line number, and the family-robust `ratio` is the defensible statement.

## Against my own result

1. **The deficit is a thin-disc effect, and real SPARC discs are thin.** Check 13 shows the deficit
   grows monotonically as the disc thins (`f(3)` 0.763 → 0.651 as `b/a` 0.30 → 0.037). Real SPARC
   discs are thinner than the M1 `b=0.3 kpc` used, so the *true* correction is likely *larger* than
   the 10 % quoted — still, by the same sign (more adverse), not the 20 orders the PASS wanted.
2. **The RAR is not measured exactly at y=2 on a clean MN disc.** The inversion pins `s` at the
   radius where `y(R)=2`; the real RAR is a fit over 3389 points across 175 galaxies of varying
   structure, and a per-galaxy 2-D fit would replace the single radius `R(y=2)` by a distribution.
   This could shift the ratio by the size of the inter-galaxy scatter (~0.1 dex), not by 2 orders.
3. **The kernel-family ambiguity is resolved by choice, not by physics.** Both families are legal
   (ghost-free, monotone, `U->sqrt(y)`); I reported the ratio so the verdict does not depend on the
   choice, but a reader who adopts only family 2 would quote 1.086–1.104, and only family 1 would
   quote 1.072–1.088 — both still > 1, so the KILL is robust to it.
4. **The in-plane field is what a rotation curve sees, but the PDE is 3-D.** The verdict uses the
   in-plane `u`; the polar axis is slightly *enhanced* (`f` 1.003–1.006, check 9). If an observable
   sampled off-plane (e.g. a warp or a lopsided galaxy) the picture could differ, but the
   galaxy-average RAR is an in-plane quantity.
5. **The `|curl v|/(|v|/r) = 8.7e-4..4.4e-2` quoted in the task sheet is a different quantity** from
   the flux-level `|mu grad chi - grad Phi_N|/|grad Phi_N|` (up to 0.976) that actually enters the
   algebraic law. The two are not comparable; I used only the flux one. A reader comparing against
   the curl number would understate the geometry effect — but again the *sign* is unchanged.

## Owed / not computed

- **A 2-D per-galaxy RAR fit** (3389 points, 175 SPARC galaxies) instead of the single-radius
  `R(y=2)` inversion on a canonical MN disc. Not done; it would replace one number by a
  distribution and is the natural next step, but cannot close a 2-order gap.
- **Off-plane / warped geometries**, and the effect of a central bar. Not done.
- A **dark-halo (NFW) overlay**, since the RAR is measured against baryons+dark; here the source is
  baryons-only MN. Not done — but a halo would *lower* the RAR's `y`, i.e. push the disc even
  further toward the adverse direction.

## Files touched

- `runs/i003_disc_correction.py` — pre-existing (Aug 17); **run and verified**, not modified (14/14,
  exit 0, ~236 s; re-run confirmed `exit code = 0`).
- `runs/logs/i003_run.out` — run log captured by this session.
- `results/I003_disc_correction.md` — this file (new).
- `LEDGER.md` — one row appended.
