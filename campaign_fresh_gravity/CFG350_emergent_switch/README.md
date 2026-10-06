# CFG350: an emergent switch from the coarse-grained phase-space state (velocity dispersion / entropy)?

Criteria: `FROZEN_CRITERIA.md` (commit e3e17f0fc, committed alone before any script). kappa = 1/2 fixed (fitted);
nu_mono; the switch reads baryons only (MS1-MS5); no DM particle (the cold mass is still required).

**Verdict (frozen rule): NO-GO.** Every scored (MS-allowed) route passes at most 2 of the 4 tests. Conservation is
not the obstruction: a switch that is a function of the coarse-grained state has an ordinary action, which fixes
CFG349's legality problem. The obstruction is the baryons themselves. This is a scoped result, not a closure.

## The state variable and the switch
- sigma_ij = P_ij/rho is the second moment of the distribution function. It obeys the 10-moment (Gaussian) closure of
  Levermore 1996 and Brown, Roe & Groth 1995, with heat flux 0: D sigma/Dt = -(L sigma + sigma L^T).
- Its smooth-flow solution is the congruence sigma = G sigma0 G^T with det G = rho/rho0. So sigma = 0 stays 0,
  sigma > 0 stays > 0, and s = ln(sqrt(det sigma)/rho) is the conserved adiabat (Lean E1-E4).
- Irreversible change happens only at caustics and shocks (weak solutions).
- Scored routes:
  - R-b0: f = H(sigma_b^2), 0 constants;
  - R-b1: f = S(sigma_b^2/sigma_ref^2 - 1), 1 constant;
  - R-s: f = H(s_b - s_IGM), 0 constants.

## MS-rule check
- The cold component's dispersion sigma_c is the MS1 matter/carrier door, so it is NOT allowed.
- B's S_cold is also pressureless dust, which has no sigma at all.
- So only the baryons' sigma is scored. sigma_c is reported (R-c).

## Results (24 DE12 hosts, both footings, r = 30 kpc)
| route | (a) FRW | (b) bound | (c) transition | (d) conservation | constants | tier |
|---|---|---|---|---|---|---|
| R-b0 sigma_b > 0 | FAIL | PASS | FAIL (no edge) | PASS | 0 | NO-GO |
| R-b1 sigma_b > sigma_ref | PASS | FAIL (disc OFF) | FAIL (WHIM ON; chi 4e2-1e4) | PASS | 1 | NO-GO |
| R-s s above the IGM adiabat | FAIL (voids ON) | FAIL (8/24, disc OFF) | FAIL | PASS | 0 | NO-GO |

- **(a) FRW and linear perturbations.**
  - Baryons are never cold. sigma_IGM is 4.5 km/s at z = 1100 and at least 0.096 km/s at its minimum (z ~ 8). After
    reionisation it is 11.8 km/s (T0 = 1e4 K).
  - So R-b0 is ON on FRW, and the L341 growth is x28.8 / x33.9 (sigma_8 23.3 / 27.5).
  - R-b1 needs sigma_ref >= 12.17 km/s. That includes delta = 0.1 parcels on the gamma = 1.6 temperature-density relation.
  - R-s: after reionisation, s - s_IGM = (1.5(gamma - 1) - 1) ln Delta. Voids sit above the adiabat for every
    gamma < 5/3 (Lean E8), so R-s is ON in voids.
  - Single-stream cold matter: the 1D Zel'dovich test gives sigma = 0 exactly before crossing (D A = 0.9, 1 stream). After
    crossing (D A = 1.5) the maximum sigma is 0.73 in a multi-stream zone of half-width 0.26.
  - With f = 0, L341 gives D/D_LCDM = 1.00000000 and sigma_8 = 0.8101.
- **(b) bound systems and fidelity.**
  - Host gas at 1e6 K has sigma = 117 km/s.
  - Under a 10% compression, sigma^2 responds by exactly 1.1^(2/3) - 1 = 0.0656 (adiabat error 5e-14). The response is
    reversible, with no hysteresis.
  - R-b0: ON 24/24 and in the disc, dev = 0, max drop 0, no flicker.
  - R-b1: the hosts are ON (saturated, dev 0), but a local gas disc (sigma_HI = 10 km/s) is OFF. 0 of the 6 classical
    dSphs (6.6-11.7 km/s) clear sigma_ref.
  - **Empty window (Lean E5/E5n):** the post-reionisation IGM (12.17 km/s) is hotter than the gas discs B must turn ON
    (10 km/s). So no constant sigma_ref passes both (a) and (b).
  - R-s: s - s_IGM at 30 kpc is -3.8 to +2.4 (8/24 ON). The local disc is at -16.0.
- **(c) transition.**
  - The 10-moment system is strongly hyperbolic for sigma > 0. On 1000 random states, the speeds u, u +- sqrt(s_xx)
    (x2) and u +- sqrt(3 s_xx) are exact to 1e-14, with 10 eigenvectors (Levermore's result).
  - At sigma = 0 the rank is 6/10. That is dust's own Jordan block, and it is exactly where a "sigma > 0" switch flips.
  - R-b1's consistent switch stress gives chi = 2|L_M| S'/(rho sigma_ref^2) = 4e2 to 1e4 at the edge. The switch
    stress swamps the gas pressure at the transition.
  - Edge:
    - R-b0 has no edge.
    - R-b1 is ON in every unbound WHIM state (37-374 km/s).
    - R-s is ON in voids and in 5/6 WHIM states.
    - Shell crossing in bound hosts happens at the first caustic / accretion shock, 0.364 / 0.347 r_ta = 64-1206 kpc
      (Bertschinger 1985, quoted). That is inside B's turnaround edge (r_ta 177-3312 kpc) and outside 30 kpc. But
      shell crossing also happens in unbound Zel'dovich sheets (delta_lin = 1), so it does not mark "bound".
- **(d) conservation.**
  - sympy: the conservative 10-moment momentum and energy residuals are 0, and the 1D adiabat p/rho^3 is conserved.
    Total conservation in conservative form is certified as a periodic telescoping sum (Lean E7).
  - With f a state function, the parcel action L = M V'^2/2 - U(V) + f(sigma(V)) L_M(V) is ordinary. Energy is
    conserved and contains no multiplier, unlike CFG349's L-ord, whose energy was linear in lambda.
  - H-theorem-like behaviour: the RH entropy jump at gamma = 5/3 is >= 0 for all M (Lean E9 at M = 2), and a caustic
    raises sigma from 0.
  - But radiative cooling from 1e6 to 1e4 K changes s by -11.5. For collisional baryons, cooling erases the record:
    sigma_b and s_b are not monotone.

## Reported routes (cannot raise the verdict)
- **R-c (cold sigma_c):**
  - (a) PASS: 0 exactly on single-stream FRW.
  - (b) PASS: ON inside the first caustic, with no flicker.
  - Strongly hyperbolic for sigma > 0, and conservation PASS.
  - C3 FAIL: it is ON in every unbound shell-crossed sheet.
  - Its equivalent tier would be PARTIAL, but it is MS-forbidden, and B's dust has no sigma.
- **R-q (a "shocked" label):**
  - It is legal as an advected scalar (Brown-type action).
  - After cooling, though, the local state carries no record. So the label is a memory field (CFG349's class), not a
    coarse-grained state.
  - It is ON in shocked WHIM, and cold-mode streams leave CGM gas OFF.
- **R-* (stellar sigma):** this reads "stars present". It needs a coarse-graining scale L (1 constant), its edge is the
  stellar extent, and it puts GCs ON.

## Ownership classes
A local sigma reads a system's OWN dispersion only where that system dominates the local density.
- **GC cores:** rho_own/rho_host ~ 1e6, so the local sigma_b is about 7 km/s, the GC's own. But GCs (class E, Newtonian)
  and dSphs (class A, ON) share the same 6-12 km/s range, so no threshold on sigma separates them.
- **Wide binaries:** at any coarse-graining L larger than the separation, the local distribution is the field's
  (about 30 km/s), so they inherit the host's ON state.
- **R-c** reads the host halo everywhere.

FG001's E/A classes are NOT reproduced.

## Constants
- R-b0, R-s, R-c: 0.
- R-b1: 1 (sigma_ref).
- R-*: 1 (L).

## Controls
- **K1:** the FRW closure keeps sigma0 = 0 exactly at 0, and sigma0 > 0 follows a^-2 to 2.9e-12.
- **K2:** for the singular isothermal sphere, the Jeans integral gives sigma = v_c/sqrt2 to 1e-16.
- **MUTATE:** the instantaneous theta_b reader (CFG347 R1) flips 19 times in 10 cycles (max drop 1). It flickers, and
  the run exits 1.

## Lean
`CFG350_emergent_certificates.lean` has 11 theorems, no sorry and standard axioms only (rc 0; output in `.out`):
- E1 / E1 positivity: sigma = 0 invariance and positivity;
- E2 det congruence; E3 adiabat; E4 PosDef congruence (no flicker);
- E5 / E5n empty window; E6 IGM sigma bound;
- E7 conservative telescoping; E8 voids above the adiabat; E9 RH jump at M = 2.

## Run
```
python3 campaign_fresh_gravity/CFG350_emergent_switch/cfg350_emergent_switch.py > campaign_fresh_gravity/CFG350_emergent_switch/cfg350_emergent_switch.out                 # rc 0, ~8 s
CFG350_MUTATE=1 python3 campaign_fresh_gravity/CFG350_emergent_switch/cfg350_emergent_switch.py > campaign_fresh_gravity/CFG350_emergent_switch/cfg350_emergent_switch_MUTATE.out   # rc 1
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG350_emergent_switch/CFG350_emergent_certificates.lean
```
DE12's `transition()` and L341's growth harness are exec'd read-only.

**Scope:**
- The IGM T0 (1e4 K), the HI disc sigma (10 km/s), the dSph dispersions and Bertschinger's caustic/shock radii are
  quoted literature values, not re-read here.
- With a lenient T0 = 5e3 K at z = 0 only, the post-reionisation maximum over z <= 4 still comes from the z ~ 2-4
  epoch at T0 >= 1e4 K.
- |L_M| ~ g_ph^2/(8 pi G) and the edge gas density 4 f_b 5.55 rho_m-bar are approximations.
- The ownership densities are order-of-magnitude.
