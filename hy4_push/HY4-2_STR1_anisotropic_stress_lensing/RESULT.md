# STR1 — LANE HY4-2 (2026-11-11)

## LABEL

    STRESS CANNOT PAY / STRESS CANNOT PAY          (canonical / alt — one label, both footings)

Footings never pooled. `str1.py` exit 0, `str1.out` 343 lines, 65 s.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.

---

## The question, and the one-line answer

The law's static halo is held by Pi_ij = J(g) delta_ij - g_i g_j/(K(1+u)); in the deep field
**Pi_rr = -Pi_tt exactly**, so sigma_r^2 = -v_inf^2/2 < 0 and the halo is a medium under **radial
tension**. Can that stress carry the lensing signal so that KiDS's outer amplitude needs no 30 to 100 M_b of
cold mass?

**No.** The anisotropic-stress correction to the convergence is a *post-Newtonian* correction of relative
order sigma_t^2/c^2 — **1.1e-07 to 2.3e-06** on the two footings at all radii inside 10 r_M — while
what has to be covered is a **factor 5 to 20**. The two differ by **five to eight orders of magnitude**.
The stress tells you what the medium is; it does not pay the amount. **The lensing signal is mass.**

---

## 1. The derivation (Part A of `str1.py`, sympy, exact in the source)

Gauge (Newtonian / isotropic; static; spherically symmetric; Phi and Psi have units of m^2/s^2, so Phi/c^2
and Psi/c^2 are the dimensionless metric perturbations):

    ds^2 = -(1 + 2 Psi/c^2) c^2 dt^2 + (1 - 2 Phi/c^2)(dr^2 + r^2 dOmega^2)

Source:  T^mu_nu = diag(-rho c^2, p_r, p_t, p_t), i.e. T^i_j = diag(p_r, p_t, p_t).

Linearized Einstein tensor, mixed components (all three residuals certified exactly 0 by sympy):

    G^0_0                       = -2 lap(Phi)/c^2
    G^r_r - G^theta_theta       = (1/c^2)[(Phi-Psi)'' - (Phi-Psi)'/r]
    G^r_r + 2 G^theta_theta     = -(2/c^2) lap(Phi - Psi)

With G^mu_nu = (8 pi G/c^4) T^mu_nu:

    (i)    lap(Phi)                   = 4 pi G rho                        [Poisson]
    (ii)   (Phi-Psi)'' - (Phi-Psi)'/r  = (8 pi G/c^2)(p_r - p_t)           [traceless: anisotropy alone splits the potentials]
    (iii)  lap(Phi - Psi)             = -4 pi G (p_r + 2 p_t)/c^2           [trace]

Adding (i) and (iii), and writing D = Phi - Psi:

    (iv)  lap[(Phi + Psi)/2] = 4 pi G [ rho + (p_r + 2 p_t)/(2 c^2) ]     <-- THE LENSING SOURCE
    (v)   lap(Psi)           = 4 pi G [ rho + (p_r + 2 p_t)/c^2     ]     <-- THE TOLMAN / ACTIVE SOURCE

**The photon.** For the null cone of this metric, c dt = n dl with
n = sqrt((1 - 2 Phi/c^2)/(1 + 2 Psi/c^2)) = 1 - (Phi + Psi)/c^2 + O(c^-4), so

    kappa = Sigma_eff / Sigma_crit,      Sigma_eff = INT [ rho + (p_r + 2 p_t)/(2 c^2) ] dz.

The factor **1/2**, not 1, is the one that belongs to lensing; the Tolman/active channel carries the
factor 1. (Cross-check, independent of the linearized step: the GR PPN metric for a static perfect fluid,
-g_00 = 1 - 2U + 2U^2 - 6 Phi_4 + 2 Phi_2 and g_ij = (1+2U) delta_ij, gives
n - 1 = 2U + 3 Phi_4 - U^2 - Phi_2 + ..., i.e. pressure 3p against density 2rho, ratio 3p/(2 rho c^2).
Formula (iv) specialized to p_r = p_t = p gives exactly (p_r+2p_t)/(2 rho c^2) = 3p/(2 rho c^2). MATCH.)

**Tolman / active mass.** M_T = INT [ rho + (p_r + 2 p_t)/c^2 ] sqrt(-g) d^3x, and for a static
asymptotically flat configuration M_T = M_ADM exactly. (Bookkeeping, stated honestly: for a
self-gravitating system p/(rho c^2) ~ |Phi_N|/c^2 ~ eps, so the pressure term is formally of
1PN order in the metric — of the same order as the U^2 and Phi_2 terms that the strict linear step
drops. That is why the PPN cross-check above is load-bearing: it fixes the coefficient in the
combination that lensing actually sees. The conclusion does not depend on it, because *every* 1PN
channel is O(eps) ~ 1e-6.)

**With p_r = -p_t:**  p_r + 2 p_t = + p_t = rho sigma_t^2 > 0, so

    lensing source      = rho [ 1 + sigma_t^2/(2 c^2) ]
    active/Tolman source = rho [ 1 + sigma_t^2/c^2     ]

The sign favours the exit: the tension ADDs to the lensing. The magnitude kills it.

---

## 2. Exact algebra for the law's halo (Part B)

With x = r/r_M, r_M = sqrt(G M_b/a0), v_inf^4 = G M_b a0, the point-mass law gives the closed form

    u(x) = g/a0 = (1 + sqrt(1 + 4 x^2)) / (2 x^2)

and therefore, in units of v_inf^2/(4 pi) (sympy, exact):

    sigma_t^2 = Pi_tt/rho_h :  2 pi + (2 pi/3)(1/x) + (pi/4)(1/x^2) + (pi/30)(1/x^3) + ...
    sigma_r^2 = Pi_rr/rho_h : -2 pi + (2 pi/3)(1/x) - (pi/4)(1/x^2) + (pi/30)(1/x^3) + ...

so in the deep field

    sigma_t^2 -> + v_inf^2/2 ,   sigma_r^2 -> - v_inf^2/2 ,   (Pi_rr + Pi_tt)/Pi_tt -> 2/(3x) -> 0 .

**The equilibrium identity (KA1):**

    d Pi_rr/dr + (2/r)(Pi_rr - Pi_tt) + rho_h g = 0     identically in x (sympy: exactly 0).

That is momentum conservation, nabla_mu T^{mu nu} = 0, with the gravitational field only. Its
corollary is the sharpest form of the kill: **given Pi_ij, momentum balance fixes rho_medium = rho_h.** The
stress and the density are not independent knobs — you cannot dial the stress up without the mass.

---

## 3. The pre-registered kill (Part D), and the numbers

**K1 (graded, the task's kill).** The exit lives only if

    R_max = max over 0 < r <= 10 r_M of [ (1/2c^2) INT_0^r (p_r + 2 p_t) 4 pi r'^2 dr' ] / M_c(<r)  >  0.10

on a footing. It is not:

| footing | R_max, baryons resolved (Hernquist, a_h/r_M = 0.02 / 0.05 / 0.1 / 0.2 / 0.5) | x at max | line |
|---|---|---|---|
| canonical (a0 = 9.3603e-11) | **2.3054e-06** | 0.031 r_M | 1.0e-01 |
| alt (a0 = 1.1312e-10) | **2.5344e-06** | 0.031 r_M | 1.0e-01 |

Missed by **4.3e4** (canonical) / **3.9e4** (alt). The most generous reading of
R (numerator C = (|p_r|+2|p_t|)/c^2, denominator 3 = excess over the charge VSH1 delivers) reaches
**8.63e-05** — still a factor **1.16e3** under the line. All nine (numerator, denominator) combinations
were computed; the exit is given every one and still fails by 1.2e3 to 4.3e4.

**K2 (dominant energy condition).** Read the other way: a stress can carry at most the mass it is the stress
*of* (|p| <= rho c^2 forces sigma^2 <= c^2, i.e. at most 1x). Carrying F x M_b with a medium of mass
M_med needs sigma_t^2/c^2 = 2 F M_b / M_med:

| what must be carried | M_med = 5.41 M_b (whole cosmic budget) | M_med = 1.4 M_b (what falls in) |
|---|---|---|
| M_c at 10 r_M = 9.51 M_b  | 3.52 c^2  | 13.59 c^2 |
| M_c at 30 r_M = 29.50 M_b | 10.91 c^2 | 42.14 c^2 |
| KiDS share X_s = 59.5 M_b | 22.00 c^2 | 85.00 c^2 |

Every entry is far above 1: a factor **3.5 to 85** violation of |p| <= rho c^2, i.e. a superluminal
medium. The 5x to 20x is outside the theory, not outside this lane.

**The asymptotic value.**

    sigma_t^2/c^2 = v_inf^2/(2 c^2) = sqrt(G M_b a0)/(2 c^2)

This is the correction to the **Tolman / active** source (v). The correction to the
**convergence** (iv) is **half** of it, sigma_t^2/(2 c^2) = v_inf^2/(4 c^2), because lensing sees
(Phi + Psi)/2 and the anisotropic part enters the sum with a factor 1/2 that the g_00 potential does not.
Both columns are given below; the verdict is identical either way.

| log M_b | v_inf [km/s] can / alt | sigma_t^2/c^2 can / alt | lensing corrn can / alt |
|---|---|---|---|
| 9  | 59.4 / 62.3   | 1.961e-08 / 2.156e-08 | 9.805e-09 / 1.078e-08 |
| 10 | 105.6 / 110.7 | 6.201e-08 / 6.817e-08 | 3.101e-08 / 3.409e-08 |
| 11 | 187.8 / 196.9 | 1.961e-07 / 2.156e-07 | 9.805e-08 / 1.078e-07 |
| 12 | 333.9 / 350.1 | 6.201e-07 / 6.817e-07 | 3.101e-07 / 3.409e-07 |
| 13 | 593.7 / 622.5 | 1.961e-06 / 2.156e-06 | 9.805e-07 / 1.078e-06 |
| 15 | 1877.5 / 1968.5 | 1.961e-05 / 2.156e-05 | 9.805e-06 / 1.078e-05 |

At **v_inf = 200 km/s**: sigma_t^2/c^2 = **2.23e-07**, and the convergence correction (the factor 1/2)
= **1.11e-07**. (The task brief's "about 1e-6 for a 200 km/s galaxy" is ten times this at the asymptotic
value; 1e-6 is reached in the *inner* halo — x <~ 0.3, see the profile table in `str1.out` — or at
log M_b ~ 13. Both are reported; neither is within five orders of 10 per cent.)

**The missing mass, for scale** (M_c/M_b = X(x) = (sqrt(1+4x^2)-1)/2): 0.618 at 1 r_M, 2.54 at 3 r_M,
5.41 (= the whole cosmic cold budget) at 5.8888 r_M, 9.51 at 10 r_M, 29.50 (5.45x) at 30 r_M,
99.50 (18.4x) at 100 r_M; the KiDS share ONE1 needs is 59.5 M_b = 11.00x the budget.

**Active (Tolman) mass, computed, log M_b = 11** (M_T(<r) = M_c(<r) + (1/c^2) INT (Pi_rr+2 Pi_tt) dV):

| x | M_c/M_b | dM_active/M_b can / alt | dM_conv/M_b can / alt |
|---|---|---|---|
| 1  | 0.6180 | 5.402e-07 / 5.939e-07 | 2.701e-07 / 2.970e-07 |
| 3  | 2.5414 | 1.142e-06 / 1.255e-06 | 5.709e-07 / 6.276e-07 |
| 10 | 9.5125 | 2.750e-06 / 3.023e-06 | 1.375e-06 / 1.512e-06 |

The stress carries 1.4e-06 M_b in the convergence at 10 r_M against a missing mass of 9.51 M_b
there: **short by a factor 6.9e+06**.

---

## 4. What sigma_r^2 < 0 requires of the medium

1. **A KINETIC GAS IS EXCLUDED, exactly.** For any f >= 0, p_r = INT f v_r^2 d^3v >= 0. A negative radial
   dispersion is unreachable by any gas, collisionless or collisional, relativistic or not.
2. **A FLUID AT REST IS EXCLUDED, exactly.** A perfect fluid at rest has p_r = p_t. Anisotropy held at rest
   and for ever needs a **static shear stress**: a shear modulus **mu != 0** — i.e. **an elastic solid**
   (viscous shear stress is proportional to the rate of strain and vanishes at rest; sustaining it would
   dissipate without end).
3. **The stress state.** With p_r = -p_t the mean is p_bar = +p_t/3 (a net pressure) and the deviator is
   (2 p_t/3) diag(-2, 1, 1): **uniaxial tension along r held against tangential compression**. That is
   a pressure-vessel / tensegrity state — **radial cables in tension, tangential hoops in compression**, i.e.
   a **network of radial filaments** (or a solid with the equivalent anisotropic moduli). Gas, liquid and dust are
   all excluded.
4. **How soft.** mu ~ p_t/3 ~ rho_h v_inf^2/6, so the transverse sound speed c_T = sqrt(mu/rho_h) ~ 0.41 v_inf
   (computed at x = 10, log M_b = 11: mu = 1.80e-14 Pa canonical / 2.63e-14 Pa alt, c_T = 78.0 / 81.7 km/s).
   No acausality — but c_T^2 is ~6x below 4 pi G rho_h r^2 (Jeans ratio 5.79, both footings), so the
   "solid" is **Jeans-unstable on every scale >= r_M**: it fragments rather than stands.
5. **The anchor.** The inward force transmitted across a sphere is 4 pi r^2 |Pi_rr| -> **0.5000 M_b a0** in the
   deep field — a **constant, independent of r** (computed: 0.4833 M_b a0 at x = 10, 0.5000 asymptotically).
   It equals the baryons' own weight M_b g(r) at x = **2.7297** r_M (~33 kpc at log M_b = 11). A cable can only
   pull, so the network must be anchored at its inner end; if it is anchored on the baryons, it applies a constant
   inward pull of half a M_b a0 to them — **a new, non-gravitational force on baryons** that the law does not
   contain and that the record's media do not couple through (M5's scope: media coupling to baryons only
   through gravity).

---

## 5. Checked against M5's three hypotheses

M5: *any* **LOCAL**, **MOMENTUM-CONSERVING**, **NORMALLY SELF-GRAVITATING** medium whose equilibrium is
the law — NO-GO by theorem (the stress that does it for every baryon profile is unique, AQUAL's, and is
density-blind, ill-posed along the field, and cancels the medium's own nonlinear self-gravity).

| hypothesis | verdict for the elastic-solid reading |
|---|---|
| **H1 local** | **HOLDS.** Pi_ij = J(g) delta_ij - g_i g_j/(K(1+u)) is a function of the local field g and its local direction — a local constitutive law. Numerically verified: (M_b, r) = (1e11, 20.0 kpc) and (1e12, 63.2 kpc) have the same g = 7.7147e-11 m/s^2 and give identical Pi_rr = -1.559890e-12 and Pi_tt = 2.330089e-12. |
| **H2 momentum-conserving** | **HOLDS.** The equilibrium residual is exactly 0 symbolically and <= 1e-9 numerically at every radius: the medium balances its own weight against the stress divergence and nothing else. |
| **H3 normally self-gravitating** | **HOLDS.** The halo's density enters lap(Phi) = 4 pi G rho unscreened: g(r) = G(M_b + M_c(<r))/r^2 by construction, and INT rho_h 4 pi r^2 dr = M_b X(x) to 12 digits (KA6). |

**All three hold, so M5 bites.** The elastic reading is *inside* the theorem, not outside it. The three
exits, and what the record says about each:

- **drop locality** → FA3; "no candidate survives" (`MEDIUM_DESIGN` §2).
- **drop momentum conservation** → a medium that exchanges momentum with something else; the one class the
  record had not tried, and it dies on arithmetic (recombination drag 0.73 / 0.61 of H at z = 1100; the
  Bullet's gas column is 0.1 to 0.7 optical depths).
- **drop normal self-gravity** → TM1's tethered medium: no self-gravity, so no growth; satellites and
  cluster cores fail.

None of the three pays the amount. This lane says the amount is the whole problem. The elastic solid's own
gates (Bullet pass-through, recombination decoupling) belong to ELA1 (HY4-7) and are not graded here.

---

## 6. Known-answer checks

| KA | statement | result |
|---|---|---|
| KA1 | equilibrium: dPi_rr/dr + (2/r)(Pi_rr-Pi_tt) + rho_h g = 0 | exactly 0 symbolic, <= 1e-9 numeric — PASS |
| KA2 | deep-field identity (Pi_rr+Pi_tt)/Pi_tt -> 0 as 2/(3x) | 6.644e-03 at x = 100 (line 1e-2), agrees with the record's 6.6e-3 — PASS |
| KA3 | sigma_t^2 -> v_inf^2/2 | ratio 1.003346 at x = 100 (line 1e-2) — PASS |
| KA4 | PPN/1PN cross-check of the pressure coefficient | 3p/(2 rho c^2), matches formula (iv) — PASS |
| KA5 | dust limit (p=0 -> Phi=Psi) and isotropic-Schwarzschild limit | PASS |
| KA6 | mass closure INT rho_h dV = M_c(<r) | ratio 1.000000000000 — PASS |
| locality | same g from different (M_b, r) gives the same Pi | identical to 7 digits — PASS |

## 7. MUTATE

- **M1** gas instead of a solid (p_r = +p_t): the correction becomes 3 sigma^2/(2c^2), i.e. at most 3x the
  tabulated column (**<= 6.7e-06** at log M_b = 11). The **sign** of p_r is not what carries the verdict; the
  magnitude is. BITES.
- **M2** Tolman factor 1 instead of 1/2: 2x — still fails. **M3** (|p_r|+2|p_t|)/c^2: 3x — still fails. BITES.
- **M4** narrower denominators (excess over the 5.41 M_b budget; over the 1.4 M_b delivered): 1.9x and
  3.2x larger than the widest at x = 10 — still 4 orders short. BITES.
- **M5** extended baryons (Hernquist a_h/r_M = 0.02 / 0.05 / 0.1 / 0.2 / 0.5): removes the point-mass
  1/x artefact; R -> 0 at the centre; maximum 2.3054e-06 / 2.5344e-06. BITES (does not rescue).
- **M6** footing swap: canonical and alt give the same label. BITES.

## 8. Caveats, stated plainly

- **The point-mass inner artefact.** For a point baryon mass g_N ~ 1/r^2 diverges at the centre, so
  sigma_t^2 ~ 1/r and the ratio diverges as 1/x. The grid maximum there is a grid artefact, not
  physics. The resolved-baryon (Hernquist) runs bound the true inner value; the scan is monotone in a_h
  and a_h/r_M = 0.02 (0.24 kpc at log M_b = 11) is far more concentrated than any real galaxy.
- **PN bookkeeping.** The pressure term is formally 1PN (O(eps^2) in the metric, O(eps) relative to the
  mass). The strict linear step isolates it but drops other 1PN terms (U^2, Phi_2) of the same order. The
  PPN cross-check fixes the coefficient; the verdict does not depend on the coefficient, because *every*
  1PN channel is O(|Phi_N|/c^2) ~ 1e-6 against a factor 5 to 20.
- **What is not graded here.** The amount budget (HY4-1/GAS1), ELA1's gates (HY4-7), the conservation-law
  escape (HY4-4/VCC1), and the share X_s = 59.5 M_b, which is an input rule in the record, not an output of
  this lane. This lane grades one thing: whether the anisotropic stress can carry the convergence.
