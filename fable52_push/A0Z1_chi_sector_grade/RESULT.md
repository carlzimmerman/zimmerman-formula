# A0Z1 RESULT: the chi sector and a0(chi) of DT1's action

**LABEL: EOM CERTIFIED; a0(chi) FAILS / a0(chi) FAILS** (canonical / alt).
Criteria d9adb0feaa (committed alone, before any script or number). Script `a0z1.py`; output `a0z1.out` / `a0z1.json`;
pipeline copies `a0z1_hm.py`, `a0z1_forest.py` (FRZ2's, one edit: `fz`). TEST lane, quarantined. Adopts nothing,
relabels nothing, registers nothing. Footings graded separately, never pooled. kappa = 1/2 FITTED; not theory closed.
Not pushed; record the local id only.

## The one-line summary

The action's hand algebra for chi is **right** — the certified variation reproduces
`box chi = V'(chi)[1 - S(u) kappa^2/(8 pi)]` term by term. But the bracket **does** go negative in the deep-Newtonian
places (the Solar System, u ~ 6e7 at 1 AU; stellar surfaces, u ~ 1e12), it is **not** screened there in the sense that
matters and it is not screened at all in a galaxy; and the a0(z) the action predicts **fails FRZ2's frozen forest gate by
600 to 1800 times** on both footings. The a0(chi) branch is dead on the forest row; the dust term it was meant to rescue
was already graded dead by MK2.

## Q1: the chi equation of motion — CERTIFIED

sympy, exact, residual 0 at every step (certified variation of `L = -(1/2)(dchi)^2 - V(chi) + J(|A|; a0(chi))` in 1+1,
the smallest setting where the sign of the d'Alembertian is visible):

| step | result | residual |
|---|---|---|
| (i) K0 Legendre map: `max_P [P.A - W(K|P|)]` | `J = (a0^2/K)[u - ln(1+u)]`, attained at `K|P| = a0 u/(1+u)` | 0 (and 0) |
| (ii) `dJ/da0` at fixed `|A|` (`u = A/a0`) | `(a0/K) S(u)`, `S = 2(u - ln(1+u)) - u^2/(1+u)` | 0 |
| (iii) `da0/dchi` from `a0 = kappa sqrt(G V)` | `kappa^2 G V'/(2 a0)` | 0 |
| (iv) the Euler-Lagrange equation | `box chi - V' + dJ/dchi = 0`, i.e. `box chi = V'[1 - kappa^2 S(u)/(8 pi)]` (K = 4 pi G) | 0 (and 0) |

So ACTION.md's line is **confirmed term by term**: the same `S(u)`, the same coefficient `kappa^2/(8 pi)`
(`1/(32 pi)` at kappa = 1/2), the same minus sign. The sign of the bracket is fixed by the sign of the
on-shell J, which is QX17's K0 (`+J`); MU1 (J -> -J) turns it into `1 + kappa^2 S/(8 pi)`, never negative:
the mutation bites, so the sign is doing real work. Verified against ACTION.md's own words too:
`S = u^3/3 - u^4/2 + ...`, `S(3) = 0.977` ("about 1 at u = 3"), `S(u) = 32 pi` at `u = 108.9` ("about u > 100"),
`S ~ u` for large u.

## Q2: the sign of the bracket — it goes negative, and the consequences are bounded

u = A/a0 with A the law's acceleration (the record's spherical static law `g^2 = g_N (g + a0)`):

| place | u (canonical / alt) | bracket 1 - S/(32 pi) |
|---|---|---|
| Solar System, 1 AU | 6.33e7 / 5.24e7 | **-6.3e5 / -5.2e5** |
| Solar System, 10 AU | 6.34e5 / 5.24e5 | **-6.3e3 / -5.2e3** |
| Earth surface (g given) | 1.05e11 / 8.67e10 | **-1.0e9 / -8.6e8** |
| solar surface | 2.93e12 / 2.42e12 | **-2.9e10 / -2.4e10** |
| galaxy log M_b 11 @ 1 kpc | 150 / 124 | **-0.40 / -0.15** (point-mass bound) |
| galaxy log M_b 10 @ 1 kpc | 15.8 / 13.3 | +0.89 / +0.91 |
| galaxy @ 10 kpc (log 10 / 11) | 0.47 / 2.17 | +0.9998 / +0.995 |
| galaxy @ 100 kpc | 0.039 / 0.130 | +1.000 |
| cluster 1e15 Msun @ 50/100/300 kpc | 3.3 / 3.1 / 2.3 | +0.988 / +0.990 / +0.994 |

**The bracket is negative in 10 of the 26 place/footing rows**: everywhere in the Solar System and on/inside stars,
and — under the point-mass bound frozen in the criteria — in the core of a log M_b 11 galaxy. It is **positive** in cluster
cores (u 2-3) and everywhere a galaxy is in its MOND regime (u ≲ 1). (Reported, not graded: with the record's Hernquist
softening, a galaxy's central u is only 7.5 (log M_b 10) to 17.5 (log M_b 11), so the bracket stays positive; the
point mass is a deliberate upper bound.)

**What follows, and on what timescale:**
- **chi does NOT run away.** Where the bracket is negative the effective mass is tachyonic,
  `|m_eff| = lambda sqrt(K V |bracket|)`, but the unstable mode has to fit inside the region:
  `|m_eff| L` is 8.8e-13 (Sun), 2.8e-7 (galaxy nucleus) and 1.1e-5 (cluster) — against the bound pi. The Compton
  wavelengths are 44 kpc, 362 Mpc and 4414 Mpc against regions of 7e8 m, 100 pc and 50 kpc. The gradient energy wins
  everywhere by 5 to 15 orders of magnitude, so there is no exponential growth.
- **a0 varies by a static, negligible amount**, relaxing on the light-crossing time of the region (~8 min at 1 AU,
  ~3e2 yr for a 100 pc nucleus, not a cosmological time): `da0/a0 = (lambda^2 a_geo^2/4) Int S(u(r)) r dr`
  gives 5.3e-24 (Sun), 1.7e-13 (log M_b 11 galaxy), 1.2e-14 (log M_b 10), 3.1e-10 (cluster), times lambda^2.
  The `(a0 R)^2` suppression — not any accident of S — is what makes it small.
- So ACTION.md's hand estimate ("negligible") **holds**, but not for the reason it gives: the bracket really is
  negative and large in the Solar System; what saves it is that the source is suppressed by (r / Hubble radius)^2
  and the tachyonic mode does not fit in the region.

## Q3: a0(z) against FRZ2's frozen gate — FAILS / FAILS (the graded row)

The action's prediction is closed: `a0 = kappa sqrt(G V)` gives `f(z) = a0(z)/a0(0) = sqrt(V(z)/V(0))`, with V(z)
from the action's own FRW scalar equation for `V = V0 exp(-lambda chi sqrt(K))` (matter + scalar, flat; in 8 pi G = 1
units the exponent is `-lambda_std chi`, `lambda_std = lambda/sqrt(2)`). Thawing from rest at z_i = 100 with
Omega_phi(0) = 1 - Om of the footing's form B fit leaves **one** free parameter, lambda; freezing lambda to each of
FRZ2's three observed w0 fixes it completely.

| case | lambda_std (lambda) | w0 fitted | Omega_phi0 | f(z=3) | R_cold(z3, k3/k5) can | **Delta chi^2 can / alt** | gate <= 4 |
|---|---|---|---|---|---|---|---|
| X-Pan | 1.03395 (1.46223) | -0.8380 | 0.6846 | 1.1771 | 0.863 / 0.711 | **7316.1 / 6035.2** | **FAILS / FAILS** |
| X-DES5 | 1.26876 (1.79430) | -0.7520 | 0.6846 | 1.2971 | 0.877 / 0.744 | **5750.8 / 4332.0** | **FAILS / FAILS** |
| X-Uni | 1.45707 (2.06060) | -0.6670 | 0.6846 | 1.4402 | 0.895 / 0.787 | **4116.2 / 2678.4** | **FAILS / FAILS** |

Every X case fails on both footings, by 670 to 1829 times the gate. The reason is structural, not a matter of tuning:
**a0 tracks sqrt of the dark-energy density, so a0 rises with z** (f(3) = 1.18 to 1.44) — but FRZ2's own scan
shows the forest's zero point needs f(3) ≈ 2 (P0.5, the best power law, still 252 / 167, i.e. 42-63 times over).
The exponential potential cannot give more: a canonical scalar has w >= -1 at every z, so its density can only fall
with time, and the cross-over the forest wants sits outside the family. Worse, the observed CPL that the fits assume has
wa < 0 and crosses w = -1 at z = 0.35 (Pan), 0.41 (DES5) and 0.44 (Uni) — a phantom crossing no canonical
scalar can make, so this action cannot reproduce the background its own a0(z) is calibrated against. (Reported.)

Pipeline validation (KA5): this lane's copy of FRZ2's `frz2_hm.py` / `frz2_forest.py`, run with `f = 1`,
gives **9916.246 / 9008.690** against FRZ2's printed 9916.2 / 9008.7; run with FRZ2's own D-Pan `f(z) = sqrt(F)`
it gives **13657.671 / 13418.074** against 13657.7 / 13418.1. Inherited checks: KA2 (R = 1 -> 0) 0.0,
KA3 (CO1 z = 0 held) 160.74 / 1025.57 — all PASS.

## Q4: screening in a galaxy — NO

The record's diagnostic (`QX17 (E2)`: `(1 + gamma_L Pi_+) A + gamma_L D Pi_+ = K W' Phat`), the two additions to A sized on
the unscreened on-shell P (`K|P| = a0 u/(1+u)`, Lstar 21.7 / 22.9 pc):

| place | `gamma_L Pi_+` (can) | `gamma_L |grad Pi_+|/|A|` (can / alt) | screened? |
|---|---|---|---|
| Solar System, 1 AU | 3.1e-3 | 3.2e5 / 4.3e5 | **YES** (the gradient term) |
| Earth surface | 7.3 | 1.1e11 / 1.4e11 | **YES** |
| galaxy log M_b 10 @ 1 kpc | 1.3e-11 | 3.2e-5 / 4.3e-5 | **no** |
| galaxy log M_b 11 @ 1 kpc | 1.5e-11 | 3.2e-6 / 4.3e-6 | **no** |
| galaxy @ 10 / 100 kpc | ~1e-13 / ~1e-15 | 2.0e-6 / 4.4e-8 | **no** |
| cluster core @ 100 kpc | 1.1e-13 | 1.2e-8 / 1.5e-8 | **no** |

The scale is set by `(Lstar/r)^2 / u` (Newtonian regime) and `(Lstar/r)^2` (MOND regime): with Lstar ~ 22 pc the stiffness
is 4 to 11 orders of magnitude too small to act in a galaxy or a cluster, and 5 to 11 orders too large to ignore in the Solar
System. **So the chi coupling is live at full strength in galaxies**, which is exactly why the sign of the bracket there
matters rather than being academic. (A full PDE re-solve of the screened P equation has not been done anywhere in the record;
QX17 says the same about its own estimate.)

## Kill conditions: what fired

| kill | pre-registered in the criteria | result |
|---|---|---|
| **K1** EOM refuted by certified variation | yes | did **not** fire — every residual 0 |
| **K2** every X case fails Delta chi^2 <= 4 on both footings | yes | **FIRED** — 4116-7316 / 2678-6035, gate 4 |
| **K3** runaway: `|m_eff| L >= pi` anywhere observed | yes | did not fire — max 1.4e-5 |
| **K4** a0 varies: `|da0/a0| > 1e-2` anywhere observed | yes | did not fire — max 3.4e-10 |
| **K5** not screened in a galaxy | yes | **FIRED** — ratio 3e-6 to 4e-8 |

**`kill_that_fired` = K2 (the a0(chi) branch fails the forest gate on both footings), with K5 (no screening in a
galaxy) also fired.** K2 is the lane's grading row; K5 is the reason the chi sector cannot hide behind the stiffness
where it matters.

## Known answers (all PASS) and mutations (all bite)

- KA1 (law sector removed): `box chi = V'` — residual 0. **PASS**
- KA4 (ACTION.md's own words about S): series, S(3), u(S = 32 pi), S ~ u. **PASS**
- KA6 (point-mass closed form vs the numerical Poisson integral, 20 %): worst 14 %. **PASS**
- KA5 (this lane's copy of FRZ2's pipeline vs FRZ2's printed numbers, 0.1): P0 9916.246 / 9008.690; D-Pan 13657.671 /
  13418.074. **PASS**
- KA2 (R = 1 -> 0) and KA3 (CO1 z = 0 held 160.74 / 1025.57), inherited. **PASS**
- MU1 (on-shell law term with the wrong sign): the bracket becomes `1 + kappa^2 S/(8 pi)`, never negative. **bites**
- MU2 (S = u^3/3 used at all u): `da0/a0` moves by 1.3e22x (Sun), 3e6x (galaxy). **bites**
- MU3 (f = V/V0, the square root dropped): Delta chi^2 4708.8 / 3260.5 against 7316.1 / 6035.2. **bites**

## What this lane does and does not do

- It grades **only** the chi sector and a0(chi) of DT1's action. **The dust term remains failed** (MK2: NO VALUE /
  NO VALUE; clusters and groups at no sound speed). Nothing here repairs it, and a pass here would not have either.
- Q2's static response is the leading Poisson integral on the homogeneous background; it ignores the back-reaction of
  the shifted chi on the halo layout and the external field effect. Both are named, not computed.
- Q3 takes Om from the footing's form B fit and does **not** refit the CMB or the background with the scalar; the
  CPL crossing above is reported, not graded. The forest numbers are the forest's response to this a0(z) through
  FRZ2's own pipeline.
- Q4's numbers are the two gamma_L additions to the constitutive law evaluated on the unscreened on-shell P, the
  same perturbative sizing QX17 section 3 does by hand; no PDE re-solve exists in the record.
- Not computed: SCS1/SCS2 stability with a dynamical a0 (ACTION.md section 4 item 3), the structure-growth gate
  (item 1), and hosted dwarfs (RB2).

Files: `FROZEN_CRITERIA.md`, `a0z1.py`, `a0z1_hm.py`, `a0z1_forest.py`, `a0z1.out`, `a0z1.json`,
`a0z1_fz.json`, `hm/`, `logs/`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
