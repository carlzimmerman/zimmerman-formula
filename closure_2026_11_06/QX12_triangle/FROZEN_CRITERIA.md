# QX12 frozen criteria: the constraint triangle for any extra gravitating sector

Frozen before any QX12 script or number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane:
the sector is COLD DARK ENERGY (never "cold dark matter"); no particle; no LCDM inputs. Rules: SWARM_BRIEF.md.

## The triangle, as inequalities

The sector X has density rho_X(x, t), gravitates as a source of the a0 law (g = glaw(g_N,b + g_N,X), as in QX7/QX10),
and has a rest-frame pressure p_X(rho_X, k_1..k_n, t). The k_i are local scalars the action can build (rho, Phi,
g/a0, Q - 1, X, Omega_DE, sigma, T).

- **T1 (early, cosmological):** c_s,X^2(z) / c^2 <= (k_J^min / k)^2-level bound for z >~ 10, i.e. cold on the
  CMB-lensing and peak scales. QX3 G1 and QX10 iter_1 J0 show that a cold component with omega_d = 0.120 +- 0.004
  on the footing background meets the shape lines. The cosmic sector-to-baryon ratio is R = omega_d / omega_b =
  5.562 (QX7/QX10 corner background).
- **T2 (isolated galaxies):** inside lensing radii, the sector mass a galaxy keeps must not move KiDS isolated-galaxy
  lensing (Brouwer 2021, 4 mass bins) or the Humphrey ellipticals beyond their lines. In local form: at every data
  radius, M_X(<r) <= M_X,max(r), where g_N,max = inv(g_obs,max) - g_N,b, inv(g) = g^2/(g + a0) (the exact inverse
  of the law, certified in Lean in this lane), and g_obs,max = g_obs + 2 sigma (KiDS) or g_tot 10^0.15
  (ellipticals, the G7 line).
- **T3 (hot systems):** X-COP (7 clusters, 35 points) and the 20 Lovisari groups need
  M_X(<r) in [M_X,min(r), M_X,max(r)], from g_obs -+ 2 sigma through the same inverse.

## Iterations (each has its own frozen file; failures stay on the record)

- iter_1: the general no-go for every barotropic sector in hydrostatic equilibrium with the cosmic sea
  (p_X = p_X(rho_X, t), any equation of state, any time dependence). This covers QX3 iter2/iter3 and QX7/QX10. It
  also covers candidate (d), environmental depth, because the equilibrium density is a function of the total depth
  relative to the sea.
- iter_2: candidate (a)/(e), a host-keyed equation of state. The sector is cold (retained at the cosmic ratio) where
  a key built from the host's temperature, b = p/(rho c^2), exceeds a threshold, and hot (absent) below it. The
  threshold is fixed by galaxy data alone and the amplitude by T1 alone. Clusters and groups are then predicted.

Candidates (b) (sound speed set by the khronon charge D.P) and (c) (decay except where confined) are written up as
arguments in the README, labelled ARGUMENT, not as graded iterations, unless one survives the iter_1 theorem's scope.
