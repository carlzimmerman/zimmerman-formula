# CFG837 DERIVATION: what the radial-shell tether dynamics say about the free fraction F(f_loss)

Lane SHELL, 2026-10-18, hand derivation, nothing executed. Criteria: `FROZEN_CRITERIA.md` (written first). kappa = 1/2 FITTED; Omega_c/Omega_b = 5.364;
footings never pooled; no particle species; not "theory closed". Record numbers are quoted with their CFG ids; arithmetic is shown.

**Label under the frozen rules: NO REDUCTION. Lane label: CONSTRAINT TIGHTENED.** The previous round's E-versus-C gap (x19.1) is not closable by this route, and
the reason is a sign, not a size: the dynamics unbind MORE when more baryons are lost, the data need the class that lost LESS (clusters) to carry the larger F.

## 0. Result in eight lines
1. **Tautology (T1).** F is NOT defined as the expelled fraction: the numerator is an observed mass (lensing, X-COP), f_ret enters only the budget S. So F(f_loss) is not
   vacuous. But "tether-unbound = free" is a separate identification, and the record says they differ (CFG749/776 vs CFG812). It is a new postulate.
2. **Sudden loss (T2), exact per shell until shells cross.** Shell released at rest on the old law: E = -(3 - p)/(3 r0) V_flat^2, p = 1/(1 - f_loss). Unbound iff p >= 3,
   i.e. **f_loss >= 2/3**, for every shell radius (scale invariance). A pure number, no a0, no footing, no M_OF.
3. **Any monotone loss history, same assumption.** For p < 3 NO shell can be unbound whatever the loss rate. For p > 3 a shell is unbound iff the weighted mean of r0/r
   over the loss history is >= 2/(3 f_loss). Adiabatic loss: nothing is ever unbound.
4. **Radius dependence.** The only way r/r_M enters is the ratio (loss time)/(r0^(3/2) t0). A fixed loss time unbinds the OUTER shells and keeps the inner ones.
5. **Crossing (T4).** The sum over ranks of the shell energies is conserved exactly; an energetic upper bound on the unbound mass, increasing in p, follows; no lower bound.
6. **Classes (T5).** Record f_loss: early types 0.82-0.90, clusters 0.31-0.36 (0.10 census, 0.40 artefact). Threshold 2/3. Early types sit above it, clusters below it.
   The step formula gives F_E = 1 (needed 0.0114-0.0324) and F_C = 0 (needed 0.619-1.0): both wrong, in opposite directions.
7. **Extra scale.** No mass scale is produced; M_OF is not produced and not needed. The one new number is a TIME ratio (loss time or age over the shell's own dynamical time),
   an external input.
8. **Physical sign.** Unbound shells leave the halo (CFG776: overshoot to a deficit). To give 1-3% unbound in early types they must be the outermost 1-3% of the mass,
   at roughly 100-165 kpc, outside the 50-100 kpc band where the excess lives.

## 1. T1: tautology audit

### 1.1 What F is (read from the E_FREE files)
`PARAMRED_2026-10-16/E_FREE/DERIVATION.md` Step 1: M_free,i = F_i S_i, S_i = (Omega_c/Omega_b)(1/f_i - 1) M_b,i, 0 <= F_i <= 1. Needed F (Step 2):
- E: M_needed = 0.55-0.80 M* (CFG745), S_E = 5.364 (N - 1) M_b with N = 5.6-10 (CFG804).
- C: M_needed = 1.9-4.5 M_b (X-COP, CFG745), S_C = 5.364 (1/f_eff - 1) M_b with f_eff = 0.636-0.686 (CFG814).

So M_needed comes from lensing and X-ray data; f_ret appears only in the denominator S. **F is a ratio of an observed mass to a census-built budget. It is not the expelled
fraction and not a function of it by construction.** The question "F(f_loss)" is not vacuous.

### 1.2 The census-free form of the same targets
Define G = M_free / (5.364 M_b) = (N - 1) F = F f_loss / (1 - f_loss). Then, by hand:
- E: G = 0.55/5.364 = 0.1025 to 0.80/5.364 = 0.1491, at f_loss 0.82-0.90.
- C: G = 1.9/5.364 = 0.3542 to 4.5/5.364 = 0.8389, capped by F <= 1 at N - 1 = 0.458-0.572, at f_loss 0.31-0.36.
G must FALL as f_loss rises from 0.34 to 0.86, while any F <= 1 rule has G <= f_loss/(1 - f_loss), which rises. This is the previous round's gap written without S.

### 1.3 The identification "unbound = free" is not an identity, and is contradicted
- CFG749: cold energy moving relative to the baryons at >= 0.3 V_flat has E > 0 and leaves.
- CFG776: the expelled surplus overshoots into a deficit (early types -0.08 against +0.28 observed); "any persistent core excess must be a component the cubic push does not act on".
- CFG812: freed (untethered) cold energy stays bound, bound fraction 1.000 in 11/12 clusters (min 0.968).

So the tether-unbound mass LEAVES the halo; the free mass of the E-lane STAYS. Setting F := U/S (U = tether-unbound mass) is a definition, not a derivation. A rule that turns
unbound shells into untethered-but-present mass is not in the record. This is a postulate (fails criterion (e) unless derived). I compute U anyway, because it is the
only quantity the record's dynamics define.

## 2. Setup (units G = a0 = M_now = 1)
- Length r_M = sqrt(G M_now/a0); velocity V_flat = (G M_now a0)^(1/4) (so G M_now/r_M = V_flat^2); time t0 = sqrt(r_M/a0); energy per unit mass V_flat^2.
  Dimension check: G M/r_M = G M sqrt(a0/(G M)) = sqrt(G M a0) = V_flat^2. OK (C1).
- Cold energy as radial shells; enclosed cold mass m(<r); the critical tether cancels cold-energy self-gravity; push energy E_push = (1/3) integral m^3/r^4 dr (CFG747).
  Shell equation: **r'' = -1/r^2 + m^2/r^4** (CFG747 README, `cfg747.py` accel(): (m_out^3 - m_in^3)/(3 dm r^4) -> m^2/r^4 as dm -> 0). Static law m = r.
- Peak ratio p = M_peak/M_now = N = 1/f_ret; f_loss = 1 - 1/p. The old law in these units is m = sqrt(p) r (the law's mass scales as sqrt(M_b): m_eq = r sqrt(a0 M_b/G)).
  A shell with enclosed mass mu sat at rest at r0 = mu/sqrt(p) before the loss, i.e. **mu = sqrt(p) r0**. (This is CFG776's initial condition, m = sqrt(p)(r - 0.5) + 0.5.)
- Scale invariance (C5): (r, m, E, t) -> (lam r, lam m, E/lam, lam^(3/2) t) maps solutions to solutions: Phi(lam r; lam m) = Phi(r; m)/lam below.

## 3. T2: sudden loss, one shell

### 3.1 Energy integral
While a shell's enclosed mass mu is constant (no shell crossing), its force is -dPhi/dr with
  Phi_eff(r; mu) = -1/r + mu^2/(3 r^3),   dPhi/dr = (r^2 - mu^2)/r^4.
Properties: minimum at r = mu (Phi'' = -2/r^3 + 4 mu^2/r^5 = 2/mu^3 > 0 there), Phi_min = -2/(3 mu); Phi = 0 at r = mu/sqrt(3); Phi -> +infinity as r -> 0 and
Phi -> 0 from below as r -> infinity; Phi < 0 and monotonically increasing for all r > mu. No barrier outside the minimum. Hence E = v^2/2 + Phi_eff is conserved and
**unbound iff E >= 0** (E = 0 is the parabolic marginal case).

### 3.2 Release
At t = 0+ the baryon mass is 1 and the shell is at rest at r0 with mu = sqrt(p) r0:
  eps0 = Phi_eff(r0; sqrt(p) r0) = -1/r0 + p r0^2/(3 r0^3) = -(3 - p)/(3 r0)           [units V_flat,now^2; r0 in r_M,now].
- **Unbound iff p >= 3 iff f_loss >= 2/3.** Independent of r0 (scale invariance, C5) and of the footing (a0 cancels in these units). Nothing but the coefficient 1/3 of the push
  energy and the Newtonian 1 enters.
- Decomposition (C3 iv): eps_min = -2/(3 mu) = -2/(3 sqrt(p) r0). With s = sqrt(p): eps0 - eps_min = (s - 1)^2 (s + 2)/(3 mu) >= 0. At p = 2: (0.41421)^2 (3.41421)/(3 x 1.41421)
  = 0.585786/4.24264 = 0.13807, and eps0 - eps_min = -0.33333 + 0.47140 = 0.13807. OK. The threshold eps0 = 0 is (s - 1)^2 (s + 2) = 2, solved exactly by s = sqrt(3)
  ((4 - 2 sqrt3)(2 + sqrt3) = 8 + 4 sqrt3 - 4 sqrt3 - 6 = 2).
- Limits. f_loss -> 0 (p -> 1): eps0 -> -2/(3 r0), the bottom of the well; the heating eps0 - eps_min ~ (f_loss/2)^2/mu, quadratic; nothing unbound. f_loss -> 1 (p -> infinity):
  eps0 ~ p/(3 r0) -> +infinity, speed at infinity v_inf^2 = 2 eps0 = 2(p/3 - 1)/r0 (0.59-0.97 V_flat at r0 = 5 for p = 5.6-10: 2 x 0.8667/5 = 0.347, v = 0.589; 2 x 2.3333/5 = 0.933, v = 0.966).

### 3.3 Bound shells: apocentre (r0 is the pericentre because the net force there is (p - 1)/r0^2 > 0 outward)
Set x = r/r0. Phi(x_a) = eps0 gives (3 - p) x^3 - 3 x^2 + p = 0 = (x - 1)[(3 - p) x^2 - p x - p], so
  **x_a = [p + sqrt(3 p (4 - p))] / (2 (3 - p))**.
Checks (C2, C3 ii): p -> 1: x_a = (1 + 3)/4 = 1. p -> 3: x_a -> 3/(3 - p) -> infinity. p = 1.5: x_a = (1.5 + 3.3541)/3 = 1.6180; Phi(1.6180) = -0.61803 + 0.5/4.23607 = -0.61803 + 0.11803
= -0.5000 = eps0 (= -1.5/3). p = 2: x_a = 1 + sqrt3 = 2.7321; Phi = -0.36603 + 2/(3 x 20.392) = -0.36603 + 0.03269 = -0.33334 = eps0. OK.

### 3.4 Second route: direct quadrature of the orbit (C3 iii)
v^2 = 2(eps0 - Phi) = [2(3 - p)/(3 x^3)] (x - 1)(x_a - x)(x - x_b), x_b = [p - sqrt(12 p - 3 p^2)]/(2(3 - p)). With x = mid - hw cos(theta), dt = dx/v:
  half-swing time (units r0^(3/2) t0) = integral_0^pi sqrt(3/(2(3 - p))) x^(3/2)/sqrt(x - x_b) dtheta.
- p = 1.5 (x_b = -0.618): Simpson, 4 intervals: 0.2618 x 12.9608 = 3.393. Midpoint rule, 4 nodes: (pi/4) x 4.3204 = 3.393.
- p = 2 (x_b = -0.732): Simpson 0.2618 x 23.3226 = 6.106. Midpoint (pi/4) x 7.7747 = 6.106.
- p -> 1 limit: small-oscillation period pi sqrt2 r^(3/2) -> half period pi/sqrt2 = 2.221. Sequence 2.22, 3.39, 6.11, infinity (p = 1, 1.5, 2, 3): monotone, diverging at the threshold.
- p = 3: E = 0 gives v^2 = 2(x^2 - 1)/x^3; direct: r'' = -1/r^2 + 3 r0^2/r^4, multiply by r', integrate from rest: r'^2/2 = 1/r - r0^2/r^3. Same. At late times r ~ t^(2/3), the parabolic
  law, independent of r0 (so adjacent marginal shells bunch up).
Two independent quadratures and the root substitutions agree to the digits shown.

### 3.5 Core offset: the only r/r_M dependence in the sudden case
CFG747/776 use m(r) = sqrt(p)(r - c) + c with c = 0.5 (a reflecting wall and a fixed core: set-up devices, CFG747 "Limits"). Then m/r0 = sqrt(p) - (sqrt(p) - 1) c/r0 and
bound iff m/r0 < sqrt3, i.e. sqrt(p) < (sqrt3 - c/r0)/(1 - c/r0):
| r0 (r_M) | 1 | 1.5 | 2 | 5 | 11 | 25 | infinity |
|---|---|---|---|---|---|---|---|
| p_crit | 6.07 | 4.40 | 3.905 | 3.289 | 3.122 | 3.052 | 3.000 |
| f_loss,crit | 0.835 | 0.773 | 0.744 | 0.696 | 0.680 | 0.672 | 0.667 |
(Example r0 = 5: (1.7321 - 0.1)/0.9 = 1.8134, squared 3.289.) KiDS radii are 2.3-16 r_M (CFG776), so the threshold there is f_loss 0.68-0.74. c is not a framework quantity and inside ~r_M the
point-mass deep-regime treatment is not valid anyway; the table is a set-up sensitivity, not a prediction.

### 3.6 Timing against the record (C6, order of magnitude only)
Half-swing p = 1.5: 3.393 r0^(3/2) = 37.9 t0 at r0 = 5 and 123.8 t0 at r0 = 11; p = 2: 68.3 and 222.7 t0. CFG776 quotes "expelled within ~50-100 t0" at 5-11 r_M. Same order. This is a
consistency statement only; the simulation is not reproduced.

## 4. T3: other loss histories and the adiabatic limit

### 4.1 Any monotone history, constant mu (no crossing)
Let q(t) = M_b(t)/M_now fall monotonically from p to 1. H = v^2/2 - q/r + mu^2/(3 r^3), dH/dt = dPhi/dt = -q'/r >= 0, so
  eps_f = eps_i + integral |q'|/r(t) dt,   eps_i = -2p/(3 r0).
**Claim: r(t) > r0 for all t > 0.** At r <= r0 the force is (1/r^2)(p r0^2/r^2 - q) >= (p - q)/r^2 >= 0, so the shell moves out at once. If it returned to r0 at a first time t*,
its kinetic energy there would be integral |q'| (1/r - 1/r0) dt < 0 (since r > r0 before t*), impossible. So 1/r < 1/r0 throughout and
  eps_f <= eps_i + (p - 1)/r0 = eps_0 (the sudden value).
Also eps_f >= eps_min = -2/(3 mu) (bottom of the final well).
- **p < 3: eps_0 < 0, so NO shell is unbound for ANY monotone loss history.**
- **p > 3: unbound iff (p - 1) <1/r> >= 2p/(3 r0), i.e. rho = <r0/r> >= 2/(3 f_loss)** (<> weighted by |q'|; rho <= 1; rho = 1 sudden). As f_loss -> 2/3 only an instantaneous
  loss unbinds; as f_loss -> 1 it suffices that the shell stays within 1.5 r0 on average.

### 4.2 Adiabatic (exact for the whole population)
With mu fixed and q slow, a shell released at rest at the minimum stays at the minimum: r_eq = mu/sqrt(q). All shells scale by the same factor, so no crossings occur: the
no-crossing assumption is exact here (the only exact case). Route 1: eps_ad = Phi_min(q) = -q/r_eq + mu^2/(3 r_eq^3) = -(2/3) q^(3/2)/mu. Route 2 (C3 iv): d eps/dq = -1/r_eq = -sqrt(q)/mu, integrate
from p: eps = -(2/3) p^(3/2)/mu - (2/3)(q^(3/2) - p^(3/2))/mu = -(2/3) q^(3/2)/mu. Same. At q = 1: **eps = -2/(3 mu) < 0 for every p: nothing is unbound at any f_loss < 1.**
Adiabaticity needs |q'/q| << omega, omega^2 = Phi'' = 2 q^(5/2)/mu^3, slowest at the end: omega_end = sqrt2 mu^(-3/2), period
  T_end = pi sqrt2 (r_eq/r_M)^(3/2) t0 = 4.443 (r_eq/r_M)^(3/2) t0.
Hand numbers (r_M = sqrt(G M/a0) at a0 = 9.3603e-11, G M_sun = 1.3275e20 m^3/s^2, 1 kpc = 3.0857e19 m):
- M_b = 10^10.8 M_sun: r_M = 9.69 kpc, t0 = 56.6 Myr. T_end(50 kpc = 5.16 r_M) = 4.443 x 11.72 = 52.1 t0 = 2.95 Gyr; T_end(100 kpc) = 4.443 x 33.15 = 147 t0 = 8.3 Gyr.
- M_b = 10^13 M_sun: r_M = 122.0 kpc, t0 = 0.201 Gyr. T_end(0.48 Mpc = 3.93 r_M) = 34.6 t0 = 7.0 Gyr; T_end(1.24 Mpc = 10.2 r_M) = 144 t0 = 29 Gyr.
The loss duration is NOT in the record (external input). Wherever it is shorter than these times the shell is in the sudden regime; for the cluster MID band that means any loss completed in less
than a few Gyr.

### 4.3 Radius dependence
For a fixed protocol shape, r(t) = r0 X(t/r0^(3/2)), so rho depends on r0 only through nu = tau_loss/(r0^(3/2) t0), and rho decreases with nu (expected, not proven; QUEUED Part B). Unbound iff
nu <= nu_c(f_loss), with nu_c(2/3) = 0 and nu_c increasing. So at fixed loss time the **outer shells r0 >= r_c = (tau_loss/(nu_c t0))^(2/3) r_M are unbound and the inner shells stay bound**.
nu_c(f) needs the shell integrated through the ramp (Part B of the script). The unbound mass fraction of the peak-law profile (mu proportional to r0, coreless) is u = 1 - r_c/R, R = 5.364 sqrt(p) r_M,now
(the edge where m = 5.364 M_peak = 5.364 p).

## 5. T4: shell crossing
For fast loss the flow is not homologous: for the sudden case r = r0 X(tau) with X = 1 + (p - 1) tau^2/2 + ..., so dr/dr0 = X - 1.5 tau X' = 1 - (p - 1) tau^2 + ..., a first caustic near
tau ~ (p - 1)^(-1/2) (crude: 1.4 at p = 1.5 against a half swing of 3.4). After crossing, enclosed masses change and single-shell energies are no longer conserved. What survives exactly:

### 5.1 Rank-energy identity (C4)
With rank mass mu_i (mass strictly inside shell i, core included) the code's discrete push energy is, after Abel summation,
  W = CORE^3 RMIN^-3/9 + sum_j (m_out,j^3 - m_out,j-1^3) r_j^-3 / 9,    (m_out,j^3 - m_out,j-1^3)/(9 dm) = (a^2 + ab + b^2)/9 -> mu^2/3.
(Collecting the coefficient of r_j^-3 from the two adjacent segments of `energy()` in `cfg747.py`/`cfg776.py`; the last term m_out^3 r_N^-3/9 pairs with the last shell; no outer boundary term remains.)
So **H = sum_i dm eps_i + const, eps_i = v_i^2/2 + Phi_eff(r_i; mu_i)** for every configuration. H is conserved, so the mass-weighted rank energy is conserved through crossings. Per rank
eps_i is conserved between crossings, and neighbouring crossings exchange energy.

### 5.2 Upper bound on the unbound mass (p < 3)
Coreless profile mu = sqrt(p) r0 on [c, R], total M_c = sqrt(p) R, L = ln(R/c). Initially sum eps dmu = -(3 - p) sqrt(p) L/3. Bound ranks have eps >= -2/(3 mu); unbound ranks have eps >= 0. Hence the
bound ranks must satisfy integral_B dmu/mu >= kappa(p) L with kappa(p) = sqrt(p)(3 - p)/2 (kappa(1) = 1, kappa(1.5) = 0.919, kappa(2) = 0.707, kappa(3) = 0; dkappa/dp < 0 for p > 1). Choosing the
unbound ranks as the outermost ones (most mass for least log-measure):
  **u_max(p) = 1 - (c/R)^(1 - kappa(p))**, increasing in p.
Clusters, R = 5.364 sqrt(p), c = 0.5 (CFG747's core): f_eff 0.686 (p = 1.4577, R/c = 12.95, 1 - kappa = 0.0690): u_max = 1 - exp(-0.0690 x 2.5617) = 0.162; f_eff 0.636 (p = 1.5723,
R/c = 13.45, 1 - kappa = 0.1049): u_max = 1 - exp(-0.1049 x 2.5993) = 0.239. Needed u_C (section 6): >= 0.243 and >= 0.2253 respectively. So for c = 0.5 the cluster requirement is excluded at f_eff = 0.686,
and allowed at f_eff = 0.636 only if EVERY bound rank sits at the bottom of its well (zero kinetic energy) and every unbound rank leaves at zero speed: a perfect-efficiency limit.
The result depends on the numerical inner cutoff c (c = 0.1 would give u_max(0.686) = 0.250), so this is a necessary-condition bound, not a prediction.
There is NO lower bound: for p > 3 energy conservation only requires that SOME mass be unbound (it can carry any energy at high speed).

### 5.3 Ordering
(i) eps_0 per rank, -(3 - p) sqrt(p)/(3 mu), is increasing in p for p > 1 (derivative (3p - 3)/(2 sqrt p) > 0). (ii) u_max(p) is increasing. (iii) The adiabatic value is independent of p. So for any
history applied equally to both classes, heating and the unbound bound are larger for the class with larger f_loss. That the actual unbound mass is monotone in p is expected, not proven;
QUEUED Part C tests it at p = 1.5, 2, 3, 5.6, 10.

## 6. T5: comparison with the record (inputs from section 2 of `FROZEN_CRITERIA.md`; arithmetic by hand)
Let M_c = 5.364 p M_now (all tethered cold mass), S = 5.364 (p - 1) M_now, u = U/M_c, F_dyn = U/S = u/f_loss.
| | E early types | C clusters |
|---|---|---|
| f_loss (record) | 1 - 1/5.6 = 0.8214 to 1 - 1/10 = 0.9000 (CFG804) | 1 - 0.686 = 0.314 to 1 - 0.636 = 0.364 (CFG814); 0.10 median census, minimum f_ret 0.38 (CFG813); 0.40 pinned artefact (CFG812) |
| p | 5.6-10 | 1.458-1.572 (1.11 on the census median) |
| S / M_b | 24.67-48.28 | 2.455-3.070 |
| M_c / M_b | 30.04-53.64 | 7.819-8.434 |
| F needed | 0.55/48.28 = 0.0114 to 0.80/24.67 = 0.0324 | 1.9/3.070 = 0.619 to 1 (raw 4.5/2.455 = 1.83) |
| u needed | 0.55/53.64 = 0.0103 to 0.80/30.04 = 0.0266 | 1.9/8.434 = 0.2253 (f_eff 0.636) or 1.9/7.819 = 0.243 (0.686), up to f_loss = 0.314-0.364 |
| single shell at t = 0+ | eps0 > 0 for all r0 >= 2 (p_crit <= 3.9): all unbound | eps0 < 0 for all r0: none unbound, for any loss history (section 4.1) |
| step formula F_dyn | u = 1, F_dyn = 1/f_loss = 1.11-1.22 (> the cap 1: it also unbinds the retained baryons' own share, against S4); capped F = 1 | 0 |
| ratio to need | x31 to x88 too large (1/0.0324, 1/0.0114) | needed 0.619-1, formula 0 |

### 6.1 What f_loss would the formula need?
- Clusters need u >= 0.2253, i.e. unbinding. In the no-crossing dynamics that requires **f_loss >= 2/3 (f_ret <= 0.33; 0.68-0.74 once the core offset at 2.3-16 r_M is included)**; with crossing the
  energetic bound (section 5.2) allows it at f_loss ~ 0.36 only in the perfect-efficiency limit. Record: 0.636-0.686 (CFG814), census median 0.90 (CFG806 table: 0.70 at log M_ta = 14; CFG813 median 0.90),
  lowest single cluster 0.38 (CFG813). Needed retention is 1.9-2.1 times below the measured value (0.636/0.333 = 1.9; 0.686/0.333 = 2.1); only the extreme tail of CFG813 approaches it
  (0.38/0.333 = 1.14), and the median cluster does not. And just above the threshold the step gives u = 1, F = 1/f_loss = 1.5: an overshoot of the window u = 0.225-0.364.
- Early types need only u = 1-3%, which this formula produces only (a) in a thin window just above the threshold, f_loss ~ 2/3 (f_ret ~ 0.33, N ~ 3-3.9), against census N = 5.6-10 (1.4-3.3 times
  further in N), or (b) through a long loss time: then the unbound shells must be the outermost 1-3% of the mass, r_c/R = 0.973-0.990, R = 5.364 sqrt(N) r_M = 12.7 (N = 5.6) to 17.0 r_M (N = 10),
  i.e. r_c = 12.4-16.8 r_M = 120-163 kpc at r_M = 9.69 kpc. That is outside or at the edge of the 50-100 kpc band of the excess (W4), and those shells LEAVE.
- The required ordering is f_loss,C > f_loss,E (more unbinding where F is larger). Record: f_loss,E / f_loss,C = 0.8214/0.364 = 2.26 to 0.9/0.314 = 2.87. **Reversed.** This holds for any F that increases with f_loss
  (section 5.3); the gap x19.1 is therefore not closable by a function of f_loss alone.

### 6.2 Late types (A5)
The census is binned in catchment mass, not morphology; CFG811 uses early types retaining only 1.5 times less (r_f = 1.5, PROVISIONAL, quoted from memory there). Then N_late = N_E/1.5 = 3.7-6.7, still above 3:
the step formula gives late types the same F = 1 as early types, so the early-late differential is ~0 (CFG811's +0.013 class result) and A5 (F_late = 0) fails. Independently, the step formula at galaxy scale
is CFG810's F = 1 hypothesis (all-radii dchi2 +443; primary +136), already scored WORSE than the baseline.

## 7. Extra scale and M_OF (C8)
- Sudden case: no dimensionless number other than f_loss. r/r_M drops out (C5); c/r_M and R/c are set-up quantities (section 3.5, 5.2).
- Loss history: one new number of dimension time, tau_loss/(r0^(3/2) t0) (section 4.3), and likewise the age since loss over the half-swing time. Neither is derivable from (G, a0, M_b); consistent with
  E_FREE T5 ((G, a0, M_b) has no dimensionless combination). It is a time, not a mass break.
- **M_OF.** CFG721's M_b,OF = 10^13.03 comes from r_ta/r_M = 5.364 N with N = 10 (53.64) where r_ta is the turnaround radius of the catchment (cosmic density); this derivation contains no turnaround radius and no
  cosmic density, so it neither produces nor needs M_OF.
- **Coincidence guard.** The census crosses f_ret = 1/3 where? CFG806's table (census 0.10/0.325/0.70/0.90 at log M_ta = 12/13/14/15), linear interpolation: log M_ta = 13 + (0.3333 - 0.325)/(0.70 - 0.325)
  = 13.02. M_OF is 13.03 in M_b, not M_ta; with the fixed point M_b = f_ret f_b M_ta (CFG804, f_b = 1/6.364 = 0.1571): log M_b = 13.02 + log10(0.3333 x 0.1571) = 13.02 - 1.28 = 11.74, 1.29 dex below M_OF.
  The matching digits are a unit-mixing artefact (different mass variables) and M_OF was itself built with f_ret = 0.10. Not a finding; dropped.

## 8. Reading
- The previous round's gap is **not closable analytically by the radial-shell dynamics**, and the failure is structural: the unbound fraction is non-decreasing in f_loss (exactly so in the
  no-crossing regime, as an upper bound in general), while the free fraction the data need is larger in the class with the smaller f_loss.
- What the derivation does fix (usable elsewhere): a loss of more than two thirds of the baryons is the only way to unbind tethered cold energy by the loss alone, and it unbinds the outer shells first;
  smaller losses leave the whole tethered population bound for every loss history (no-crossing), they only displace and oscillate it (CFG776's overshoot); adiabatic loss keeps everything.
- The E-lane's "late types F = 0, early types F = 0.01-0.03" needs a variable that is not f_loss. This lane finds none inside the shell dynamics except the loss/age TIMES, which are external inputs.

## 9. What would decide
- Computation (QUEUED behind the live 1024^3 run, `cfg837_shell_check.py`, written, not run, untested): Part A (closed forms, seconds), Part B (nu_c(f_loss), the loss-time dependence), Part C (rank-shell
  population at p = 1.5, 2, 3, 5.6, 10: unbound mass by rank energy and at r > 1000; CFG776 saved no unbound mass and stopped at p = 3, so p = 5.6-10 is outside its grid).
- A rule for tethered-to-untethered conversion (not in the record), and a measured loss duration for early types.
- Per-cluster retention (CFG812 note): the cluster class is only as sharp as f_eff.

## 10. Limits and the strongest objection
- Strongest objection: the premise p = N assumes the lost baryons once sat in the central potential with their cold energy tethered on the peak law. If they never condensed, there is no tethered
  surplus and H-EX is an initial-condition statement (F = 1 for all classes, killed for early types by CFG810). This derivation is then moot, but the E-C gap and the late-type constraint stand without it.
  Second: the shells are radial, point-mass baryons, deep-regime (CFG747's own limits), and the crossing regime is bounded, not solved. Third: F_E, F_C inherit CFG745/814's translations.
- Not verified: the monotonicity of the true unbound mass in p; nu_c(f); the identification; CFG813's minimum f_ret 0.38 and median 0.90 are read from the ledger row, not from a results file;
  r_f = 1.5 is provisional in CFG811; the script.
- Trial count: five derivation items (T1-T5), no parameter scanned. The checks C1-C6 and C8 were done by hand; C7 is queued.
