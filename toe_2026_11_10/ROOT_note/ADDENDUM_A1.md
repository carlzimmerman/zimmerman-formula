# ROOT note, addendum A1: the symmetry behind alpha = 2, the locality bound, and a correction (2026-11-10, late)

A note, not a graded lane: no criteria were committed before the script. Adopts nothing. kappa = 1/2 FITTED; not theory
closed. Script `root_a1.py` (sympy, exact rational arithmetic; 4 minutes), output `root_a1.out`; twin
`root_a1.py --mutate` -> `root_a1_MUTATE.out`.

## 1. alpha = 2 is a symmetry point (exact)

With a_i = d_i ln N and ghat_ij = N^(2/(D-2)) g_ij in D space dimensions,

    N sqrt(g) ( R[g] + eta a.a )  =  sqrt(ghat) R[ghat]  +  total derivative     exactly when  eta = (D-1)/(D-2).

Checked exactly at D = 3 (eta = 2, a non-diagonal metric, three rational points) and at D = 4 (eta = 3/2). The twin
(eta shifted by 1/10) fails. For general alpha in D = 3:

    N sqrt(g) ( R + alpha a.a )  =  sqrt(ghat) R[ghat]  -  (2 - alpha) sqrt(ghat) |d ln N|^2  +  total derivative .

So:

- **At alpha = 2 the static sector of khronometric gravity is 3-d Einstein gravity of ghat = N^2 g alone.** The
  Newtonian potential ln N does not appear. It is a local symmetry, g_ij -> e^(2w) g_ij with N -> e^(-w) N.
- That is ROOT's result (1) as a symmetry. Matter couples to N (a static mass m enters as -m N), so it sources a
  direction that has no quadratic action: the linear response is infinite, which is G_N = G/(1 - alpha/2) -> infinity.
  QG1's Minkowski row (omega = 0 at every k) is this direction at quadratic order.
- **It is not a protection.** Matter breaks the symmetry, so matter loops move the coefficient of R and not that of
  a.a. That is QG1's eps: 3.5e-32 at T2's cutoff, 1e-3 for a matter cutoff of 8.8e16 GeV. K J''(0) = 1 stays a tuning.
- **The deep-MOND term in the invariant variables** (exact, same script):
  N sqrt(g) |a|^3 = 27 sqrt(ghat) |d psi|^3 with psi = N^(1/3). That is the 3-Laplacian energy, which is conformally
  invariant in three dimensions (Milgrom 1997, Phys. Rev. E 56, 1148; PROVISIONAL). A static mass couples as -m psi^3.

Whether the identity is already in the Horava-gravity literature (anisotropic Weyl symmetry) was not searched. No
novelty is claimed.

## 2. The locality bound (a hand argument with NPJ1's computed numbers)

A_i has the dimension of an inverse length. As a length, a0 is c^2/a0 = **31.1 / 25.8 Gpc** (canonical / alt); as a
time, c/a0 = **101.5 / 84.0 Gyr**.

Take any sector that makes the non-analytic |A|^3 term from modes whose gap closes as A -> 0, coupled to A_i
analytically with a dimensionless coupling g_c. Its correlation length is 1/(g_c |A|) = c^2/(g_c a): the Rindler length
of the local acceleration, divided by g_c. At radius r in a galaxy with circular speed v that is r c^2/(g_c v^2). So the
law is a local function of A only if

    g_c  >=  c^2 / v^2      (the inverse depth of the potential well),

which is **3.29e6 / 3.00e6** on the 6e10 M_sun point mass (v_f = 165.2 / 173.2 km/s): 10^5.42 / 10^5.38 times 4 pi.
This is NPJ1's deciding number, with its reason. It is the a0 ~ cH coincidence read backwards: a sector whose scale is
a0 has modes the size of the Hubble radius. The same sector takes 101.5 Gyr/(g_c x) to equilibrate at x = g/a0.

- A slower mode speed does not help: in the sector's own units the correlation length times |A| is 1/g_c whatever the
  speed (argued, not computed).
- Ways out: a pure number of 10^6.5 or more in the coupling (10^7.9 for a 1e8 M_sun dwarf, NPJ1), or a non-analytic
  term that does not come from modes gapped by A.
- Scope: dimensional analysis plus NPJ1's nine computed sectors. It is not a theorem about every sector.

## 3. Where the law can come from, after tonight

| Origin | State | Source |
|---|---|---|
| A fundamental term | Excluded as a UV term; at a symmetry point with no weakly coupled vacuum | ROOT, HZ1, QG1, section 1 |
| A local sector gapped by the clock's acceleration | Nonlocal by 10^5.4 or more at natural coupling | NPJ1, section 2 |
| A superfluid's phase gradients | No: gradient energy cannot exceed the condensation energy | LSF1 |
| The cold component settling, one single-valued variational clock | Closed by theorem | PAR1 |
| The cold component as a wave, law on a smooth frame | STRUCTURE FAILS (the halo's polarization charge is zero in net) | SMF1 |
| Any local medium that holds the cold mass | Closed | M5, Z1, CFG461 |
| A dissipative (non-variational) clock | Running | AKS1 |

What stands as it is: (A) read as the effective theory of a medium with a conserved charge. Every background that
carries the charge passes T2, and the law's shape is radiatively stable (QG1). It has no empty vacuum, as fluid and
superfluid effective theories have none. That is a reading, not a relabel: T2 as frozen graded Minkowski and stays FAIL.

## 4. A correction to the lead's own claim

Earlier this evening the lead told the owner that an acceleration-keyed sink was "the one class left" for the joint.
That was said before PAR1, SMF1 and the medium-design note were read; they landed the same evening in other sessions.
They close most of what that argument left open. Two more points weaken the sink itself:

- **Equivalence principle.** A free-falling clock has A = 0 exactly, so an acceleration key cannot act on infalling dust.
  Only a medium that is already held reads the local field.
- **Rate.** A sink at the rate a0/c acts once per 101.5 / 84.0 Gyr.

What survives of the argument: CFG461's edge is an acceleration threshold on the total field (0.19 a0 there; 0.22 a0
from the deep-limit form (1 + f)/f^2 with f = 5.41), and no rate or density threshold scales as M_b^(1/2). AKS1 was
re-briefed before it froze criteria: the record's kinematic theorems first, then viscosity as the frame-free form of
dissipation, with the heat kept or removed.
