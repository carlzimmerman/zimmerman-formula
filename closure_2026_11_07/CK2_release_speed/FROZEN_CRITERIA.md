# CK2: does the action release a kick when its switch changes branch? FROZEN CRITERIA (committed alone, before any script or number)

Brief: RESOLUTION_2026_11_07.md section 3 (CK2), the owner's 09-26 rule applied: derive the release speed, do not scan
it. Lane id checked free (`ls closure_2026_11_07 | grep CK`, `git log origin/main | grep CK2`: only the brief).
Adopts nothing. Kappa = 1/2 FITTED; not theory closed. Both footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2),
never pooled. No LCDM input.

## The action and the term
Adopted v3s with the blend stiffness (QX17D, 6b16322464): the only switched term is -gamma_L F(Pi), Pi = D.P,
F = b^2 f(Pi/b), b = rho_DE, F = 0 for Pi <= 0 (off branch), F = Pi^2/2 for Pi >= b; gamma_L = K Lstar^2/2. AC2q
(not adopted; read for completeness): the same blend on Sigma = D.P + 2X with b = X. No other term in either action
switches. The only cold component in the v3s action is the K(Q) dust (mu_K^2 (Q-1)^2); AC2q has no K(Q) term. The
September carrier (L365-L390) is route E's retired cold sector, not a field of either action; CK2 states this and
grades whether the action could nevertheless supply its kick.

## Derivation plan (three steps; every number from ck2.py and ck2.json)
- **D1 Branch-change census.** The switch changes branch only where Pi (v3s) or Sigma (AC2q) crosses 0. In the static
  weak field Pi = rho_ph c^2 (QX17 K5; the law's phantom density), and Sigma/X = 2 + rho_ph/rho_DE (TC1 N2, read).
  Compute rho_ph(r) = (1/4 pi G r^2) d/dr[ G M(<r) (nu(y) - 1) ], y = G M/(r^2 a0), simple nu, for spherical hosts:
  point mass, Plummer, Hernquist, and a Hernquist + extended-gas two-component, M_b in 1e8-1e15 Msun (0.5 dex steps),
  scale radii from the record's size-mass range (1-30 kpc galaxies, 100-500 kpc groups / clusters), r from 1e-3 to
  1e3 r_M (r_M = sqrt(G M/a0), the acceleration crossover). Report min over the grid of rho_ph/rho_DE (v3s branch
  change iff < 0; AC2q iff < -2), and specifically its value at r_M and at the halo turnaround 1-3.7 Mpc (WL1's range).
  Virialisation: the start state is the FRW background (on branch, q = 2, QX19) and the end state is the static host;
  D1 grades both endpoints. A transient branch change during collapse is not proved absent; D2 and D3 bound it.
- **D2 Latent energy at a branch change.** sympy, exact: from AC21 iter_6's form.json (f'' pieces), integrate to f with
  f(0) = f'(0) = 0 and check continuity of F and F' across Pi = 0 against the off branch (F = 0); the raw F too. The
  energy released per unit volume by a branch change itself is the jump [gamma_L F] across Pi = 0.
- **D3 Stored-energy bound.** The most any switch-off can release is the stored stiffness energy, eps = gamma_L F(Pi) c^2
  = pi G Lstar^2 rho_ph^2 (raw form; the blend differs from it only below b, by at most Delta0 = 0.082 b^2, QX19).
  Per unit carrier mass, E/m <= eps / rho_c, so v_k <= Lstar rho_ph sqrt(2 pi G / rho_c). Evaluate on D1's grid at
  r_M and at the radius maximising rho_ph^2/rho_c, with two carrier densities: (a) the most favourable floor, the
  cosmic-mean carrier at z = 0, rho_c = 5.4 x Omega_b h^2 x rho_crit/h^2 with Omega_b h^2 = 0.02166 (BBN D/H, as NA2,
  PROVISIONAL); (b) the carrier at the cosmic share of the local mean baryon density inside r, rho_c = 5.4 rho_b(<r).
  Lstar at the record's lower bound 21.7 / 22.9 pc and at 90 pc (X27: no upper bound to 90 pc). Also report the Lstar
  that would make max v_k = 500 km/s.

## Labels (one per footing, then overall)
- **NO RELEASE TERM**: D1 finds no branch change at r_M, at turnaround or anywhere on the isolated-host grid
  (min rho_ph/rho_DE >= 0 for v3s; >= -2 for AC2q), AND D2 finds zero latent energy. Then the action supplies no kick
  at virialisation or the crossover; the carrier and its v_k are a postulate, not the action's. D3 is reported as the
  bound on any continuous exchange, with its v_k range, and decides nothing.
- **RELEASE IN RANGE**: a branch change occurs at the event on both footings AND the energy released at it gives
  v_k in 500-650 km/s for the action's own cold component, with Lstar inside its allowed range.
- **RELEASE OUT OF RANGE**: a branch change occurs, but v_k falls outside 500-650 km/s.

## Controls
- KA1: the point-mass deep-MOND phantom rho_ph = sqrt(G M a0)/(4 pi G r^2) is recovered by the numerical rho_ph at
  r >> r_M to 1e-3. KA2: rho_DE = 4 a0^2/(c^2 G) gives 5.84e-27 kg/m^3 canonical (NA1's eta row), to 1e-2.
- MUTATE M1 (wrong branch): flip the phantom's sign (rho_ph -> -rho_ph, the off branch everywhere); D1 must then report
  branch changes on the grid. MUTATE M2 (kinked stiffness): F = b Theta(Pi) (a jump); D2 must report a nonzero latent
  energy b gamma_L per volume. Each must bite; otherwise NO VERDICT.
