# OUT-5 (BOOTSTRAP CARRIER) — FROZEN CRITERIA, committed alone before any OUT-5 script or number

Lane family OUT, arm 5. TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
Footings graded separately and **never pooled** (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2).
Cold dark energy is a **gravitating field component**, never a particle. **kappa = 1/2 FITTED; not theory
closed.** This lane edits nothing outside its own folder.

Id check: `git log --all --oneline | grep -ci out5` = 0; `ls hy4_preview_push` has no OUT5.

---

## Honesty flag

This file is written **after** reading, and it reuses numbers from:
`hy4_preview_push/CRUX.md` (the reach-amount lock; T4 + LFS1),
`closure_2026_11_10/AMT1_amount_budget/AMOUNT_BUDGET.md` (the demand table, X_s = 59.5 M_b, budget 5.41),
`closure_2026_11_11/VCC1_sourced_charge_current/` (the sourcing route: C-I..C-VII, payment line
rho_cre <= 0.1 rho_Lam, C-III's eps = 2c^2/v_flat^2 with a 5.62x universality spread),
`closure_2026_11_10/LFS1_leafwise_flux_supply/RESULT.md` (A1's lambda_n/lambda_s in [-5.0e-6, -1e-8]),
`fable52_push/MK1_one_dust_constant/RESULT.md` (w(a) = w0/(w0+a^3), the mu_K >= 198.25/Mpc line),
`closure_2026_11_10/CLS1..CLS2` (form B's mu_K gives no cluster state; M_dust/M_nonbaryonic = 3.78e3),
`covariant_push_2026_10_22/V3_FULL_PICTURE.md` (the static dust delta-rho_K = -mu_K^2 psi/(4 pi G)),
`closure_2026_11_11/FINAL16_kappa_real/` (kappa is a flat direction of the formation physics).
**This is therefore not a blind pre-registration.** What is clean and frozen here: the carrier's term
list (§1), the eight gates and their lines (§4), and the mutation arms (§5). What is not clean: I have
already computed, in scratch outside this repository, the three exact identities of §2 (all residual 0)
and the four kill numbers of §3. Those are *hand results* H1–H6 below; the lane's job is to confirm or
refute them with committed scripts. If a script refutes a hand result, the label follows the script.

---

## 0. The question

T4 (SMF1 S0b, exact): the net **polarization** charge inside any ball whose boundary free-falls (P = 0)
is 0 at all times, for any momentum equation. LFS1 (exact): for a **static** clock the polarization is
frozen, so the halo's charge changes only by O(|Phi|/c^2) ~ 1e-6. Together: the halo's charge equals the
dust charge carried in, 0.9–1.4 M_b (VSH1, COL1), against a demand of 41.5 M_b at FLD1's KiDS inner
window edge and 97.8 M_b at the middle edge, and a cosmic budget of 5.41 M_b (AMT1).

This lane asks: **can a carrier be written whose halo charge is neither the clock's polarization (so T4
does not apply) nor frozen in a static clock (so LFS1 does not apply), while still (i) reproducing the
a0-line exactly with the charge counted once and (ii) being cold dust on FRW at mu_K >= 198/Mpc?**

The carrier proposed here is a **constituted free charge (CFC)**: a sector whose rest-mass density is
not transported and not the divergence of the clock's polarization, but is *pinned algebraically* to the
local gravitational field. It is called a bootstrap because the halo does not fall in — it is made where
it is needed, out of the field that is already there.

---

## 1. The action, one term per line

Action (A) is QX17 section 0 with c = 1, K = 4 pi G (restore c: K -> 4 pi G/c^2):

    S = Int d^4x sqrt(-g) { L } + S_m[g; baryons]

| # | term | mark | what it is |
|---|---|---|---|
| 1 | `[R - 2 Lambda] / (4K)` | **FROM (A)** | Einstein–Hilbert + the vacuum |
| 2 | `+ mu_K^2 (Q - 1)^2 / (2K)` | **FROM (A)** | the clock's dust (K-matter); the FRW cold component |
| 3 | `+ P^m A_m - W(K\|P\|)` | **FROM (A)** | the clock's polarization (Legendre pair) |
| 4 | `- gamma_L F(Pi)` | **FROM (A)** | blending / screening |
| 5 | `+ lambda n^m P_m` | **FROM (A)** | the unitarity (norm) constraint |
| 6 | `+ S_m[g; baryons]` | **FROM (A)** | baryons |
| 7 | `- rho_c c^2` (the carrier's rest energy; `rho_c` a worldscalar, **no kinetic term**) | **NEW** | the carrier's mass. Non-dynamical: the carrier has no propagator and no pressure |
| 8 | `+ zeta ( rho_c - N(g_b, g, partial_s g) )` | **NEW** | the **pinning**: a Lagrange multiplier `zeta` tying the carrier's density to the local field |
| 9 | `- (1/2) m_zeta^2 zeta^2` | **NEW** | a regulator for the multiplier (the pinning is soft at `m_zeta < inf`; `m_zeta -> 0` is the exact-constraint limit) |

Notation (Newtonian limit, static, spherical; `g` = |acceleration|, inward; `s` = arc length inward):
`Q = sqrt(-g^{mn} d_m tau d_n tau)`, `n_m = -d_m tau/Q`, `A_m = -h^n_m d_n ln Q`,
`partial_s g := -dg/dr` (the derivative along the inward field direction),
`mu(u)` the kernel, `u = g/a0`, and

    N  :=  [ (1 - mu)/mu ] rho_b  +  [ mu' g / (4 pi G mu) ] partial_s g            (the PINNING)

with `mu' = d mu/dg`. Term 8 is the whole mechanism: it is a constraint, not a force, so the carrier
carries no momentum of its own and there is no (1+eps) rescaling of the P-block — **VCC1's C-III double
count cannot arise here** (structural, gate G3).

**New ingredients beyond (A): one field (rho_c), one multiplier (zeta), one constant (m_zeta), and one
function (mu, already in (A)).** No new mass scale, no new particle, no new gauge symmetry.

---

## 2. Hand results to be checked (the lane's job is to confirm or refute)

**(H1) The pinning is an identity, not an approximation.** Let `mu(u)` be any kernel and `g(r)` any
field. Define, in a static spherical configuration,

    rho_b := (1/4 pi G)(1/r^2) d_r[ r^2 mu g ]        (the law)
    rho_c := (1/4 pi G)(1/r^2) d_r[ r^2 (1-mu) g ]    (the carrier)

Then, as an algebraic consequence of the product rule and Gauss's law,

    rho_c = [ (1-mu)/mu ] rho_b + [ mu' g / (4 pi G mu) ] partial_s g .

The right-hand side is **local**: it contains `rho_b`, `g` and `partial_s g` at the same point and no
integral. So the halo's density is a *constitutive* function of the field, not a divergence. Expected:
residual exactly 0, for a generic `mu(g/a0)` and a generic `g(r)`, and for both kernels below.
(Kernels: **law S**, `mu = u/(1+u)`, the kernel of action (A); **law B**, the a0-line
`g^2 = g_N^2 + a0 g_N`, `mu = (sqrt(1+4u^2)-1)/(2u)`.)

**(H2) Kernel-specialised pinning.**
- Law S: `(1-mu)/mu = a0/g` and `mu' g/mu = a0/(g+a0)`, so `rho_c = (a0/g) rho_b + [a0/(4 pi G (g+a0))] partial_s g`.
- Law B: `(1-mu)/mu = (a0 + sqrt(a0^2+4g^2) - 2g)/(2g)`.

**(H3) The enclosed mass, and that it is the law, counted once.**
`M_c(<R) = [(1-mu(R))/mu(R)] M_b` exactly (Gauss on the pinning). On the S-kernel field this gives
`X_S(x) = (sqrt(1+4x^2)-1)/2` (AMT1's demand); on the B-kernel field it gives
`X_B(x) = sqrt(1+x^2) - 1` (the a0-line's own demand). Both `~ x` at large `x`, so the demand at FLD1's
KiDS radii (x = 42 to 98) differs by under 2 % between kernels: **no conclusion of this lane is
kernel-dependent.** Expected: residual 0 for both.

**(H4) The deep-regime pinning contains no a0 — so kappa is a flat direction of this carrier.**
As `u -> 0`, `mu ~ u`, so `(1-mu)/mu -> a0/g` and `mu' g/mu -> 1`, giving

    rho_c -> (a0/g) rho_b + partial_s g / (4 pi G) ,

whose second term — the one that dominates outside the baryons — is **independent of a0**. Under
`a0 -> lambda a0` with `g` fixed, the halo density outside the baryons is invariant. Expected: residual 0
in the limit; **kappa = a0/(c sqrt(G rho_Lam)) reported, not derived.**

**(H5) Universality is automatic in the pinning and impossible in the source route.**
At fixed `x = r/r_M`, `u(x)` is kernel-fixed and carries no galaxy dependence, while
`partial_s g = a0 u'(x)/r_M ∝ a0/v_flat^2`, so the pinned density scales as `v_flat^{-2}` — exactly the
scaling the law's demand has (for a universal accretion history). By contrast, let a *source* route be
`S = A(tau) F(u, w)` with `w := Q - 1` the second independent dimensionless invariant (`w ~ -Phi/c^2`
in a static weak field, `w = 0` on FRW). If `F` is regular at `(u,w) = (0,0)` its leading monomial has
`F ~ u^p w^q` with `p, q >= 0`, so `S ∝ v_flat^{2p+2q}` at fixed `x`; the law needs `S ∝ v_flat^{-2}`,
i.e. `p + q = -1`. **No regular F reproduces the law; the unique monomial that does is `q = -1`, i.e.
`F ∝ u^2/(Q-1)`, which is irregular.** This is VCC1's V5e universality failure (`eps = 2c^2/v_flat^2`,
spread 5.62) promoted to an exact statement. Expected: the pinning's `v_flat^{-2}` confirmed; the
source route's `p+q = -1` confirmed.

**(H6) T4 and LFS1 do not apply, and by how much.**
- T4: the carrier's charge is `rho_c`, a distinct variable with its own current; it is not
  `D_m[(1+gamma_L Pi_+)P^m]/Q`. The pinning is keyed to `g`, which does **not** vanish where the clock
  free-falls, so T4's boundary premise (`P = 0` on `partial V`) has no purchase on it.
- LFS1: in a static clock the clock's charge moves by `Y dX`, a fraction `~ |Phi|/c^2 ~ 1e-6`
  (LFS1 A1 measures the allowed/demanded ratio at `-5.0e-6` to `-1e-8`). The carrier's charge moves at
  `d ln C/dt ~ d ln M_b/dt`, i.e. ratio **+1** by construction. Expected: the carrier turns LFS1's A1
  from FAIL to PASS by 5 to 6 orders of magnitude.

---

## 3. The four kills I expect, with their numbers (hand estimates; scripts decide)

**K1 — the FRW/halo mu_K fork (this is the one I expect to be decisive).** The carrier must be the FRW
cold component, so it carries the K-matter scale `mu_K`. Cold by z 3400 needs `mu_K >= 198.25/Mpc`
(MK1 row 1, KD1 B1a, `w(a) = w0/(w0+a^3)`, `w0 = I0/(4 mu_K^2)`, `I0 = 4.037e-8 Mpc^-2`). In a static
halo the same sector contributes `delta rho_K = mu_K^2 |Phi|/(4 pi G)` (V3 §4.4). Setting that equal to
the pinned density gives, at every radius and for **every** mass and footing,

    mu_K^match(r) = 1 / ( r sqrt( ln(R_max/r) ) )      [kpc^-1],  R_max the potential's zero

= **46.6 /Mpc at 10 kpc, 6.59 /Mpc at 100 kpc, 2.34 /Mpc at 637 kpc** (R_max = 1 Mpc): a 20x radial
spread, and 4.3x to 85x **below** the CMB line. Conversely at `mu_K = 198.25/Mpc` the K-matter's own
halo density exceeds the pinned density by **18x at 10 kpc, 9.0e2x at 100 kpc, 7.2e3x at 637 kpc**, with
the wrong profile (`∝ Phi`, logarithmic, instead of `∝ partial_s g ~ 1/r^2`).

**K2 — the payment wall.** The constituted charge is created in place, so it must be paid for. Local
density: `rho_pin/rho_Lam` = 4.0e4 (10 kpc) to 1.2e1 (637 kpc), log M_b 10.45 canonical
(`rho_Lam = 86.2 Msun/kpc^3`). Integrated: `M_c(<R) / (rho_Lam * 4 pi R^3/3)` = **1164 at 100 kpc, 161
at 272 kpc, 78.8 at 389 kpc, 29.5 at 637 kpc**. Against VCC1's line `rho_cre <= 0.1 rho_Lam` this fails
by 1.2e2 to 4.0e5. Other payers are worse: the halo's own gravitational binding energy is
`U/(M_c c^2) = 1.03e-7` (log M_b 10.45, R = 389 kpc); the clock's polarization energy `J/c^2` is
`~ 3.6e-3 Msun/kpc^3` at 100 kpc against `rho_pin = 3.5e4`.

**K3 — positivity.** For a *real component* `rho_c >= 0` is required. The pinning gives `rho_c < 0`
wherever `partial_s g < 0` and `rho_b` is small — i.e. in underdensities and voids, where the field
decreases inward. A modified-gravity phantom may be negative; a component may not.

**K4 — the Bullet.** A constituted halo tracks its baryons, so in a dissociative merger the lensing mass
should follow the **dominant** baryon component (the intracluster gas, ~85–90 % of the baryons), not the
galaxies. The measured lensing peaks in the Bullet sit on the galaxies. (Inputs PROVISIONAL, from
memory — **reported, not graded**.)

---

## 4. Gates and their lines

Footings graded separately. A gate FAILS if the worst graded point on that footing misses its line.
`rho_Lam = 86.2`, `rho_c0 = 33.6 Msun/kpc^3` (VCC1's values, canonical; the alt footing rescales `r_M`
only, and every ratio here is a density or mass ratio, so the ratios are footing-independent — that is
itself a check, gate G9).

| id | gate | line | graded on |
|---|---|---|---|
| **G1** | H1: the pinning identity | residual **0** | generic `mu(g/a0)`, generic `g(r)`; both kernels |
| **G2** | H3: `M_c = [(1-mu)/mu] M_b` gives `X_B(x) = sqrt(1+x^2)-1` and `X_S(x) = (sqrt(1+4x^2)-1)/2` | residual **0** | both kernels |
| **G3** | counted once: no term in §1 rescales the P-block's stress tensor | structural; no factor `> 1` may appear in front of `T^W + T^P` | the term list |
| **G4** | T4 evasion: the carrier's charge is not `D.P`; net charge in a free-fall-bounded ball `!= 0` | exact, and `rho_c(g) != 0` where `P = 0` | §1 + H6 |
| **G5** | LFS1 evasion: static-clock charge change | `\|d ln C/dt\| / (d ln M_b/dt) >= 0.1` against LFS1's `1e-8 … 5e-6` | H6 |
| **G6** | FRW: cold dust, `w(1/3401) <= 0.01` | `mu_K >= 198.25/Mpc` | MK1/KD1 B1a |
| **G7** | **the same `mu_K` must also give the law's halo**: `\|rho_K(mu_K)/rho_pin - 1\| <= 0.10` | at 10, 30, 100, 272, 389, 637 kpc, all four masses | K1 |
| **G8** | payment: `rho_pin/rho_Lam` and `M_c/(rho_Lam V)` | `<= 0.10` (VCC1's line) | K2 |
| **G9** | footing-independence of every density and mass ratio | identical to 1e-6 | both footings |
| **G10** | positivity: `rho_pin >= 0` at every graded radius | `>= 0` | haloes; voids reported separately |
| **G11** | kappa derived? | a derivation or an explicit flat-direction proof | H4 |
| **G12** | Solar System: constituted mass inside Saturn's orbit | `<= 1e-10 Msun` (VCC1's bound) | reported: VCC1 found this gate does not bite |

G6, G7, G8, G10 are the load-bearing gates: any one of them failing sets the label.
G11 is graded as DERIVED or NOT DERIVED, and never as PASS/FAIL.

## 5. Labels

- **CARRIER WORKS**: G1–G5 and G7, G8, G10 all PASS on a footing.
- **BOOTSTRAP KILLED (FRW/HALO)**: G1–G5 PASS and **G7 FAILS** on that footing.
- **BOOTSTRAP KILLED (PAYMENT)**: G1–G5 PASS and **G8 FAILS** on that footing.
- **BOOTSTRAP KILLED (POSITIVITY)**: G1–G5 PASS and **G10 FAILS** on that footing.
- **CONSTRUCTION FAILS**: G1, G2, G4 or G5 fails (the carrier does not even do what it was built to do).
- **NO VERDICT**: a known answer it rests on fails, or a mutation arm does not bite.

## 6. Known answers

- KA1 `sqrt(M_sun a0/G) = 25,914 Msun/kpc` (LFS1 KA4): reproduce to 1e-4.
- KA2 `mu_K` solving `w(1/3401) = 0.01` = **198.25 / 198.24 per Mpc** (MK1 KA7, KD1 B1a): to 1e-6.
- KA3 `r_M = sqrt(G M_b/a0)` = 1.934 / 6.479 / 8.640 / 10.878 kpc (canonical, FLD1's four masses): to 1e-3.
- KA4 the deep-regime pinned density `rho_pin = v_flat^2/(4 pi G r^2)` equals `(1/4 pi r^2) d M_c/dr`
  for `M_c = M_b X_S(x)`, to 1e-6 over `x` in [1, 100].
- KA5 `mu_K^match(r) = 1/(r sqrt(ln(R_max/r)))` is independent of `M_b`, `a0` and the footing: to 1e-9.

## 7. MUTATE (each must bite)

- **MU1** drop the gradient term: pin `rho_c = [(1-mu)/mu] rho_b` only. G1, G2 and KA4 must fail.
- **MU2** replace the pinning by the source route `F = u^2` (regular). G7's universality must fail, with
  the required `F ∝ u^2/(Q-1)`.
- **MU3** halve `mu_K` to 99.1/Mpc. G6 must fail.
- **MU4** set `rho_Lam -> 10 rho_Lam`. G8 must improve by exactly 10x and no other gate may move.
- **MU5** flip the sign of `partial_s g` in the pinning. G10 must fail in the halo.

## 8. Disclosed inputs and what is not checked

- Point-mass baryons; graded radii >= 10 kpc; `R_max = 1 Mpc` for the potential's zero (the
  zero-point is the lane's weakest input; `mu_K^match` depends on it as `1/sqrt(ln(R_max/r))`, so a
  factor 10 in `R_max` moves it by 1.5x at 100 kpc — reported, and it cannot close a 4.3x-to-85x gap).
- The law's demand radii and the four masses are FLD1's canonical table, used on both footings.
- No fully nonlinear time-dependent solve; no Boltzmann; `w(a)` is KD1's background line, not a
  likelihood (MK1's own caveat).
- The covariant completion of terms 7–9 is **not** derived here: the pinning is specified and graded at
  Newtonian order only, and §1's `N(g_b, g, partial_s g)` is the Newtonian form of the invariant. This is
  a disclosed gap, not a result.
- The Bullet (K4) and the Solar System (G12) are reported, not graded.
