# DT1 candidate action, written out in full (2026-11-10)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not registered. **A candidate, not a result. It has passed no gate.
Nothing below was derived by a certified variation; the equations marked "hand" are the lead's hand algebra.** Written at
the owner's request for one action that is meant to explain the CMB, structure growth, and the a0 relation with a
dynamical dark energy. Read `DESIGN.md` first for the dust term and `../CLOSURE.md` for why action (A) cannot be completed.

**Added 2026-11-10 evening: the dust term of this action has been graded and fails.** MK2
(`../MK2_exponential_dust_term/RESULT.md`, origin 6bbfd8697b): NO VALUE / NO VALUE; clusters and groups pass at no sound
speed. So this action, as written, fails on clusters. The dark-energy field and a0(chi) below were not graded by MK2.
The text is left as written.

## 1. The action

Units c = 1, K = 4 pi G, signature and symbols as in QX17 (`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md`):
clock tau with unit normal n, Q its rate, A the acceleration of the clock congruence, P the law's polarization on the
clock's leaves, Pi = D_m P^m.

    S = Int sqrt(-g) { R / (4K)
                       - (1/2) g^{mn} d_m chi d_n chi - V(chi)                         (dark energy: a field)
                       + L_K(Q)                                                         (the clock's dust)
                       + P^m A_m - W(K|P| ; a0(chi)) - gamma_L F(Pi) + lambda n^m P_m   (the law)
                     } + S_matter[g, baryons, photons, neutrinos]

    L_K(Q)   = (n_* x_T / K) exp( (Q - 1) / x_T )                 one constant x_T = c_s^2
    a0(chi)  = kappa sqrt( G V(chi) )                             kappa = 1/2, FITTED
    W(p; a0) = (a0^2 / K) [ -p/a0 - ln(1 - p/a0) ]                the record's W, with a0 now a function of chi
    F(Pi)    = [max(Pi, 0)]^2 / 2,   gamma_L = K Lstar^2 / 2      the record's stiffness, unchanged

Compared with action (A) three things change and nothing else:

1. The constant Lambda becomes a field chi with a potential V. Dark energy is dynamical.
2. The law's scale is no longer a number. It is a0 = kappa sqrt(G V(chi)): the owner's relation, as a term of the action.
3. The dust term is exponential instead of quadratic: the clock's dust has a fixed sound speed c_s.

Constants and functions: G; kappa (fitted, 1/2); c_s (new, a few hundred km/s); Lstar (the record's screening length);
V(chi) (a function; the smallest example is V0 exp(-lambda chi sqrt(K)), two numbers); n_* (the dust abundance, an
initial condition as before).

## 2. What each piece is meant to do

| Requirement | Piece | How (claimed, not graded) |
|---|---|---|
| CMB | L_K exponential | w = c_s^2 = x_T at every epoch, about 1e-6 to 1e-5; comoving Jeans k 1.5 to 4 per Mpc at z 1100 (`dt1_design.out`) |
| Galaxies follow the law, counted once | law sector with a static clock | unchanged from QX17 and the FB1 note: the halo is the sector's own density D.P |
| The clock is static where the law is seen | L_K exponential | warm dust is pressure-supported around a galaxy, so it should not fall in and fold (the cold clock's failure in COL1 and FLD1); being checked as an added row of MK2 |
| Galaxies hold almost no dust; clusters hold their share | L_K exponential | a well of depth phi holds n_mean exp(phi / x_T): deep wells first |
| a0 and dark energy | a0(chi) | a0(t) = kappa sqrt(G V(chi(t))): a0 follows the dark-energy density at every epoch |
| Dynamical dark energy | chi, V | w_DE = (chi'^2/2 - V) / (chi'^2/2 + V), set by V |
| Structure growth | baryons + the law's halos + dust on large scales | **not shown by anything**; see section 4 |

## 3. The equations that change (hand)

- **Law.** Eliminating P gives J(|A|; a0) = (a0^2 / K)[u - ln(1 + u)], u = |A| / a0, as before, with a0 = a0(chi). For a
  static clock the weak-field equation is the record's, div[mu(|grad Phi| / a0(chi)) grad Phi] = K (rho_b + static dust).
- **Clock.** The conserved current keeps its form with n_d = L_K'(Q) = (n_* / K) exp((Q - 1) / x_T). FRW: n_d a^3
  constant, w = x_T. Static well: n_d = n_mean exp(phi / x_T).
- **Dark energy.** box chi = V'(chi) [ 1 - S(u) kappa^2 / (8 pi) ], with S(u) = 2 (u - ln(1 + u)) - u^2 / (1 + u). S is u^3 / 3
  for small u, about 1 at u = 3, and grows as u for large u. With kappa = 1/2 the bracket is 1 - S(u) / (32 pi).
- **Gravity.** Einstein's equation with the stress of chi added and the law's stress evaluated at a0(chi).

## 4. Where it can fail (the gates it must be put through)

1. **Structure growth, the forest and CMB lensing.** The dust does not clump below tens of Mpc at late times
   (`DESIGN.md` section 2: forced for any dust term that keeps galaxies empty). The record's CMB-lensing Jeans line
   (MK1 row 2) fails as written. Small, late structure would have to come from baryons and the law's halos. **This is
   the gate most likely to kill it, and it needs a structure computation that does not exist.**
2. **The coupling of chi to the law.** The bracket in the chi equation turns negative where S(u) > 32 pi, about u > 100:
   inside galaxies' inner parts and in the Solar System unless the stiffness screens it. Hand estimate: chi's shift is of
   order (r / Hubble radius)^2 times S and so negligible, and a0 stays uniform to that accuracy. Not checked. If wrong,
   a0 varies inside galaxies or chi runs away.
3. **Health.** The stability results (SCS1, SCS2) were for the quadratic term and constant a0. Both must be redone.
   The exponential L_K has L_K'' > 0 and no minimum at Q = 1.
4. **Dust rows.** MK2 is grading the exponential term on MK1's rows: X-COP's radial shape, groups against clusters with
   one c_s, SPARC, KiDS with the cap, the Solar System.
5. **a0(z).** The action predicts a0 follows V(chi(z)). The record's a0(z) constraints and the z about 2.5 zero-point
   test apply directly, and chosen V must also fit the record's dark-energy rows.
6. **Hosted dwarfs** (RB2's FAIL under form B) are untouched by any of these changes.
7. **kappa is not derived.** The action states the relation; it does not explain the 1/2.

## 5. What grading it means

After MK2: (i) the action's equations by certified variation, with the Bianchi identity; (ii) FRW with chi, the dust and
a0(t) against the record's background and CMB rows; (iii) the chi equation in a galaxy and in the Solar System; (iv)
SCS1's stability with both changes; (v) the structure-growth gate, which needs a new computation.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
