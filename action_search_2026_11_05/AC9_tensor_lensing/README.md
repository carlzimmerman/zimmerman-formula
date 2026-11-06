# AC9: AC2q tensor speed PASS, lensing slip PASS (scoped)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (0111fe2269),
frozen before any graded number. Script: ac9.py (sympy + small numerics, about 6 s, one thread).

What is graded: only AC2q's own changes to v3s's gravitational sector, which are the stiffness pieces
T_on = -2 gamma X D.P (switch on) and T_off = +2 gamma X^2 (switch off), with X = s^2/(2N^2) in unitary gauge.
The clock's own X - V is a canonical scalar (a perfect fluid, with no anisotropic stress), and it leaves the
tensor cone alone. v3s's (D.P)^2 term is already covered by V3W W4a / W3.

## Results (both footings, never pooled)

- **T1a: c_T = c exactly in the principal part.** Neither piece adds a (dh)^2 term at O(h^2). The only h dh
  term is gamma s^2 P_z h d_z h/N, which is a total derivative and folds into the mass.
- **T1b: new tensor masses.** m^2 = 16 pi gamma s^2 (G_xx + G_yy - A_z P0_z) on the on-region side and
  8 pi gamma s^4 on the off-region side. The largest value on V3W W4a's 7,722-point grid, taken at s^2 = 2 rho_DE:
  1.1e-57 m^-2 (canonical), 1.7e-57 (alt). That gives dv/c at 100 Hz of 1.3e-46 / 1.9e-46, against the
  GW170817 band [-3e-15, 7e-16]. v3s's own W4a figure was 5e-32.
- **T2a: lensing equals dynamics at O(GM).** The Psi source is S_Psi = gamma s^2 (grad Phi . P)/(1+Phi)^2, and the
  anisotropic stress has the same form, Pi ~ gamma s^2 (P_(i d_j) Phi)^TF. Both vanish at s = 0 and at
  grad Phi = 0, so they enter beyond O(GM). V3W W1's statement "the Psi equation has no source at O(GM)" therefore
  carries over to AC2q. T_off gives an isotropic pressure -3 gamma s^4/(2 N^3) and no anisotropic stress.
- **T2b: slip bound.** |S_Psi|/rho_tot <= gamma s^2 a0 r. That is 2.4e-23 to 7.4e-21 on the on-region side and at
  most 3.1e-17 off-region (1e11 Msun deep-MOND profile), for r = 30-310 kpc and Lstar up to 90 pc. v3s's W3 bound
  was 6.5e-5.

Physical size of the new coupling: gamma s^2 = 2.4e-17 (canonical, Lstar 21.7 pc) and 4.0e-17 (alt, 22.9 pc).
The AC7 README's "gamma phidot^2 ~ 1e-11" was the fixture value used there, a conservative upper bound,
not this number.

## Known answers and controls

- K1: at s = 0 every new mass is 0, so AC2q reduces to v3s.
- K2: a planted c P_i P_j h^ij term returns its known anisotropic stress exactly (residuals 0). The slip method
  detects anisotropic stress when it is present.
- MUTATE (`AC9_MUTATE=1`, separate outputs ac9_MUTATE.*): a planted c P^2 (d_z h_+)^2 term makes T1a fail
  (exit 1). The control bites.
- Rerun: ac9.json is byte-identical (sha1 4508b3fc28c2).

## What it does not show

All backgrounds are frozen, h is kept to linear order and chi to first order. There is no nonlinear solve, no
Solar-interior solve and no moving-source solve. No new data are graded: KiDS and GW170817 are used only as the
lines v3s already met. X > 0 holds exactly in statics (sigma = 0 gives X = s^2/(2N^2)). Away from statics
it needs |grad sigma| inside the local light cone, which belongs to the nonlinear / moving-Sun obligation.
