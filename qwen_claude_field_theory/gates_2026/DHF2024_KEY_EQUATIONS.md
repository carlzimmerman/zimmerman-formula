# Imported quantities: Desmond, Hees & Famaey 2024

**Source.** H. Desmond, A. Hees, B. Famaey, *"On the tension between the radial acceleration
relation and Solar system quadrupole in modified gravity MOND"*, MNRAS **530**, 1781 (2024),
arXiv:2401.04796.  Also M. Milgrom, *"MOND effects in the inner solar system"*, MNRAS **399**,
474 (2009), arXiv:0906.4817.

The full paper text is **not** redistributed here.  Only the specific relations and numbers the
scripts in this directory consume are recorded, so the pipeline stays self-verifying.
Retrieve the papers from arXiv to check any of it.

## Definitions used

- **Eq. 1** — quadrupole convention: `dPhi(x) = -(Q2/2) x^i x^j (e_i e_j - delta_ij/3)`, with
  `e = g_ext/|g_ext|` pointing to the Galactic Centre.
- **Eq. 2** — Cassini constraint (from Hees et al. 2014, DE430 + 9 yr Cassini tracking):
  `Q2 = (3 +/- 3) x 10^-27 s^-2`.
- **Eq. 3** — algebraic MOND relation: `g = g_N nu(g_N/a0)`.
- **Eq. 6** — the RAR / McGaugh-Lelli-Schombert IF: `nu_RAR(y) = [1 - exp(-sqrt(y))]^-1`.
- **Eq. 7a** — the n-family: `nu_n(x) = [ (1 + (1+4x^-n)^(1/2))/2 ]^(1/n)`; `n=1` Simple,
  `n=2` Standard.
- **Eq. 10** — `Q2 = -(3/2) a0^(3/2)/sqrt(GM) q(e~)`.  **The 3/2 is theirs, not a convention
  choice made here.**
- **Eq. 11** — `e~ = g_ext/a0` (true external field); `e_N = g_N,ext/a0` (Newtonian), with
  `e_N nu(e_N) = e~`.  Milgrom 2009 Sec. IV states the same as `eta_N = mu(eta) eta`.
- **Eq. 12** (= Milgrom 2009 Eqs. 24-25) — `q(e~) = -3 INT_0^inf dv INT_-1^1 dxi (nu-1)
  [e_N P_3(xi) + v^2 P_2(xi)]`, with `nu` evaluated at `w = (e_N^2 + v^4 + 2 e_N v^2 xi)^(1/2)`.

## Numbers used as reproduction targets

- **Sec. 2.1 sample:** quality flag != 3, inclination >= 30 deg, points with fractional rotation
  velocity uncertainty > 10 per cent removed -> **147 galaxies, 2696 points, 31 with bulges**.
- **Sec. 3.2(i) fiducial M/L priors:** `Upsilon_disk` lognormal mean 0.50 width 0.125;
  `Upsilon_bulge` lognormal mean 0.70 width 0.175; `Upsilon_gas` 10 per cent.
  Uniform priors on `a0`, `sigma_int`, shape.
- **Sec. 3.3 external field:** `g_ext = 2.32 +/- 0.16 x 10^-10 m/s^2` (Gaia EDR3 solar
  acceleration), range `[2.00, 2.48] x 10^-10`; fiducial choice is the value in that range
  giving the lowest `Q2`.  Prior flat on `Q2` with uniform `a0`, matching Hees et al. 2014.
- **Fig. 1 caption:** for `nu_RAR` of Eq. 6, `q(1) = 0.094`, `q(1.5) = 0.159`, `q(2) = 0.221`.
- **Table 1, n-family, fiducial SPARC M/L** (`a0` in `1e-10 m/s^2`, `Q2` in `1e-27 s^-2`):

  | EFE model | n | a0 | Q2 | sigma |
  |---|---|---|---|---|
  | No EFE | 1.02 +- 0.04 | 1.08 +- 0.04 | 28.4 +0.4/-0.4 | 8.4 |
  | AQUAL global | 1.03 +- 0.04 | 1.09 +- 0.04 | 28.4 +0.4/-0.4 | 8.4 |
  | AQUAL local | 1.19 +0.06/-0.04 | 1.31 +- 0.05 | 29.4 +0.5/-0.5 | 8.7 |
  | QUMOND global | 1.03 +- 0.04 | 1.09 +- 0.04 | 28.4 +0.4/-0.4 | 8.4 |
  | QUMOND local | 1.12 +- 0.05 | 1.23 +- 0.04 | 29.1 +0.4/-0.5 | 8.6 |

  `sigma_int` is between 0.033 and 0.035 dex in all cases.
- **Headline:** 8.7 sigma tension under fiducial assumptions, falling to 1.9 sigma on removing
  galaxies with bulges.
- **Milgrom 2009 Table 1**, `-q~` at `eta = 1.5`: `mu_2` 0.11, `mu_3` 0.079.

## Reproduction achieved here
All five Table 1 n-family rows to **0.24%**; Fig. 1 anchors to 0.001-0.76%; Milgrom's `mu_3`
to 0.2%.  No fitted factor at any point.  See `gate0_dhf_reproduction_2026.py`.
