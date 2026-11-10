RE-DESCRIPTION ONLY

# Route C: the inverse problem for a medium (2026-11-10)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not registered. A derivation attempt with checks, not a graded
lane: no criteria, no label on any data. One of four parallel routes; the other routes' files were not read. Footings
canonical (a0 9.3603e-11 m/s^2) and alt (1.1312e-10) are never pooled. The cold component is cold dark energy, a
gravitating medium, never a particle.

## Answer first

The law is not derived here. The route asks what a real medium must be for its equilibrium to be the law. The answer
is unique in the classes examined, and it is the law written a second time.

1. **No barotropic fluid P(rho) gives the law for all baryon masses.** Proved (step 1). The one near-exception is a
   family with one number per halo, and that number has to be set by hand to the Tully-Fisher value.
2. **With one more local variable the answer is forced.** The variable is the local field. The stress is
   J(g) delta_ij - g_i g_j / (4 pi G (1 + u)). It may not depend on the medium's density or on any conserved label
   (step 2). This is the record's M5 result again, extended here to a label.
3. **For one conserved scalar medium coupled by gravity only, the inverse problem has one solution:**
   L = P(X) + J(|grad X|), with P'(X) = 0 across galaxy depths (step 3). That is the Newtonian limit of the record's
   action (A). So the route lands on the action the owner already has, and inherits its closed walls (MK1, MK2, COL1,
   FLD1).
4. **The literature's contact-coupled superfluid class also has an exact solution for mu = x/(1+x).** There the extra
   pull is a phonon force, not the medium's gravity. It does not lens, the medium's own mass comes on top, the medium
   is not conserved, and the branch has c_s^2 < 0. It is not form B.
5. **Nothing found selects the function J, and nothing here fixes kappa** (step 4).

So the function mu(x) = x/(1+x) is put in (as J, its Legendre partner) and comes back out. What the route adds is one
proof (item 1) and two uniqueness statements (items 2, 3).

## Postulates

- **P1. One real medium.** The cold component is one conserved medium with density rho_c >= 0. It sources Newtonian
  gravity like any mass (weak field). Light sees its mass. No particle claim.
- **P2. Gravity only.** It couples to baryons through gravity alone. Step 3b drops this once, to show what the
  literature's contact coupling gives.
- **P3. Locality.** Its internal physics is local: a stress or a Lagrangian built from fields at a point and finitely
  many derivatives.
- **P4. The target.** Its static equilibrium around any baryon distribution is the law. Spherical:
  g_N = g^2/(g + a0), that is g_c = g - g_N = a0 g/(g + a0). General geometry (the FB1 note's reading):
  div[mu(g/a0) g] = -4 pi G rho_b with rho_c = -div[g/(1 + u)]/(4 pi G), u = g/a0.
- **P5. Equivalence principle for the medium.** A free-falling piece of the medium cannot measure g. Its local physics
  can depend on its own proper acceleration and on tides, not on g. Used in step 3 only.
- **P6. a0 is an input.** a0 = kappa c sqrt(G rho_DE), kappa = 1/2 fitted. Steps 1 to 3 never use rho_DE.

Notation: K = 4 pi G. J(g) = (a0^2/K)[u - ln(1 + u)]. Point mass: r_M = sqrt(G M_b/a0), x = r/r_M, u = U(x) with
u^2/(1 + u) = 1/x^2.

## Step 1. Barotropic fluid P(rho): no

**The halo to be held.** For a point mass the law gives (check C1)

    M_c(<r) = M_b a0 / g(r),        rho_c = (a0 / (K r_M)) R(x),     R(x) = -U'(x) / (U^2 x^2).

Strong field: rho_c = a0/(2 pi G r). Weak field: rho_c = sqrt(G M_b a0)/(4 pi G r^2), an isothermal halo with
sigma^2 = (1/2) sqrt(G M_b a0).

**Balance.** Isotropic pressure and gravity only: dP/dr = -rho_c g. If P = P(rho), write F(rho) = dP/drho. Then

    F(rho_c) = g / (-d ln rho_c / dr) = a0 r_M S(x),        S(x) = -U R / R'.

**Theorem 1.** No function P(rho) satisfies this on the point-mass halos of all masses.

**Proof.** Fix x and vary M_b. Then rho_c = a0 R(x)/(K r_M) sweeps every density, so
F(rho) = (a0^2/K) S(x) R(x) / rho for all rho. The left side does not depend on x. So S(x) R(x) must be one constant.
It is not: x^2 S R tends to 2 in the strong field and to 1/2 in the weak field, and S R is 1.999e4, 190.7, 0.804,
5.26e-3, 5.03e-5 at x = 0.01, 0.1, 1, 10, 100 (C1). End of proof.

**In words.** The law's halos have a similarity: r -> lambda r, M_b -> lambda^2 M_b keeps g and P and divides rho by
lambda. A barotropic fluid would then need dP/drho proportional to 1/rho, that is P = A ln rho (the logotropic fluid
of the literature, from memory). That single candidate fails on the radial shape: it needs dP/drho to grow as r^2 in
the weak field, where the law's halo is isothermal.

**Plain version.** In the weak field the halo's dispersion is 53 / 97 / 125 km/s (canonical) and 55 / 101 / 131 km/s
(alt) at log M_b 9.4 / 10.45 / 10.9. Two galaxies reach the same cold density at different radii and need different
dispersions there. In C1: the same density, with dP/drho 0.508 against 2.065 for r_M 1 against 4.

**Remarks.**
- A barotropic medium in equilibrium has rho = H(depth of the potential), one function for every system (the
  record's `baro_order`, QX12). The law's halos are not one function of depth.
- Steady radial flow does not help. In the weak field rho goes as r^-2, so the flow speed is constant, and Bernoulli
  gives the same condition (hand argument).
- Scope: isotropic pressure, gravity only, the law for a continuum of baryon masses.

**The exception: one number per halo.** Let each halo carry one uniform number T (a temperature, or one adiabat
across the halo). Then there is one equation of state for every point-mass halo:

    P = (a0^2/K) f(zeta),   zeta = K rho T / a0^2,   given by   zeta = u^2/((u + 2) sqrt(1 + u)),  f = u - ln(1 + u).

f = zeta for small zeta (an ideal gas, P = rho T) and f = zeta^2 for large zeta (P = K T^2 rho^2 / a0^2). It holds on
the law's halos if and only if T = (1/2) sqrt(G M_b a0) (C1). Three things are wrong with it as physics.
1. T has to know M_b. T^2 = G M_b a0 / 4 is the baryonic Tully-Fisher relation, put in halo by halo. Nothing local
   sets it. For any other T the inner pull of the medium is a0 (G M_b a0 / 4 T^2), not a0 (hand). So "the pull
   saturates at a0" and "T is on the Tully-Fisher relation" are one statement.
2. It is exact only outside the baryons (step 2c).
3. One medium in contact with itself (a satellite's halo inside a host's) would need two values of T.

## Step 2. One more local variable

**2a. A conserved label (entropy): not local.** With isotropic P(rho, s) and s carried by the flow, any static
profile can be held by some s(r). Nothing is predicted. For the law the needed profile is not universal. Weak field,
gamma = 5/3, at enclosed cold mass m (C2):

    P / rho^(5/3) = 2^(1/3) pi^(2/3) G^2 m^(4/3) / sqrt(G M_b a0).

Each galaxy needs its own entropy profile, set by its own M_b. That is a statement about formation history, not a
law (the record's M5 row e says the same of collisionless relaxation).

**2b. The local field: local, and unique.** Take the stress Pi_ij = A delta_ij + B ghat_i ghat_j with A and B
functions of (rho, s, g). Radial balance on a sphere: d(A + B)/dr + 2B/r = -rho_c g. The law must hold for every
baryon profile. So at a point r, g, g', g'' and s, s' are independent. Then (C2):
- the coefficient of g'' gives (A + B)_rho = 0, and the coefficient of s' gives (A + B)_s = 0. So A + B = F(g);
- then B = -(r/2)(F' g' + rho g). At fixed (rho, g) it cannot depend on r. That fixes F' and B.

**Theorem 2.** In this class the stress is unique:

    A = J(g) + const,     B = -g^2 / (K (1 + u)),     no dependence on rho, none on s.

If the label is uniform in a halo it can add a constant to A and nothing else, so it exerts no force. Step 1's
one-number family is not a counterexample: it holds around point masses only, where g' is tied to r and g, and
theorem 2 asks for every baryon profile. On those halos the two pressures are the same numbers. Necessity is
shown here in spherical symmetry. Sufficiency with no symmetry is the FB1 check. The record's M5 (S2) has the same
result without a label, also in three dimensions.

**What it means.**
- The minimal extra variable is one vector, the local field. The required relation is local.
- The stress is blind to the medium's own density. So it is not an equation of state. In the weak field
  A -> g^2/(2K) and B -> -g^2/K: the stress is minus the Newtonian field stress. The medium's stress cancels
  gravity's own (M5's H2).
- Along the field the pressure is negative: -0.0044, -0.193, -1.489 in units a0^2/K at u = 0.1, 1, 10. It is not a
  kinetic pressure (CFG660 said so).

**2c. Where the non-isotropic part acts.** For any spherical baryon profile (C2):

    dJ/dr = -rho_c g + a0 rho_b.

Outside the baryons the scalar pressure P = J(g) alone holds the halo. Inside them the non-isotropic part supplies an
outward force on the medium of a0 per unit baryon mass. An isotropic fluid cannot supply that without a direct
coupling. The record already excludes the isotropic form on SPARC (CFG660: rms 0.177 / 0.187 against 0.100 / 0.101).

**2d. A medium cannot feel g.** By P5 a stress that depends on g is not something a medium can have by itself. What
equals g, for a medium held static, is the size of its own proper acceleration. That leads to step 3.

## Step 3. A scalar medium with a Lagrangian

**3a. Gravity only.** One conserved medium in potential flow, v = grad phi. Its Galilean-invariant scalar (chemical
potential per unit mass, constant dropped) is

    X = -(d_t phi + |grad phi|^2/2 + Phi),        grad X = g - Dv/Dt        (C3).

grad X is minus the proper acceleration: zero in free fall, g when the medium is static. Take L(X, s), s = |grad X|,
with Newtonian gravity -|grad Phi|^2/(2K) - rho_b Phi. The conserved density is N = L_X - div(L_s grad X / s). In the
static state X = X0 - Phi, s = g, and the Phi equation is

    div[(1 - K L_s/g) grad Phi] = K (rho_b + L_X).

**Theorem 3.** The static state is exactly the law for every baryon distribution if and only if

    K L_s(X, s) = a0 s/(s + a0) for every X,   and   L_X = 0 on the values of X reached.

So L = P(X) + J(|grad X|), with J(s) = (a0^2/K)[s/a0 - ln(1 + s/a0)], and P'(X) = 0 wherever the law is to be exact
(C3). For a general mu the same steps give K J'(s) = s (1 - mu(s/a0)): J and mu determine each other. Where P' is
not zero the equation is div[mu grad Phi] = K (rho_b + P'(X0 - Phi)): the law, with a pool of the medium that depends
on depth alone as an extra source. That is MK1's action-exact form.

**This is the record's action.** COL1 Part 1 reduces action (A) to
L = L_K(h) + J(|grad h|) - |grad Phi|^2/(2K) - rho_b Phi with h = -(phi_t + |grad phi|^2/2 + Phi). X is h, P is L_K.
The inverse problem for a medium returns the owner's action in its Newtonian limit. The medium reading adds nothing
to it.

**3b. The literature's class: P(X) with a contact coupling.** L = P(X) - lam phi rho_b, with
X = mu_hat - m Phi - d_t phi - |grad phi|^2/(2m). Baryons feel a phonon pull a_phi = lam |grad phi|. On the branch
where the gradient dominates, X = -|grad phi|^2/(2m) < 0, the static equation is div(P'(X) grad phi / m) = lam rho_b.
Ask for the law with g = g_N + a_phi. Then a_phi = a0 g/(g + a0), g_N = a_phi^2/(a0 - a_phi), and with
w = a_phi/a0 = (lam/a0) sqrt(2 m |X|) (C4):

    P'(X) = (lam^2 m / K) w/(1 - w),        P(X) = (a0^2/K) [ w + w^2/2 + ln(1 - w) ].

For small w, P = -(a0^2/3K) w^3, proportional to -|X|^(3/2). That is the literature's X sqrt|X| form. Matching its
constants gives a0 = alpha^3 Lambda^2 / M_Pl (hand check; the literature's formula as I remember it). The same capped
form was found in the record inside BIMOND (UX1, K1). As a reading of form B it fails five ways.
1. The pull is a force on baryons carried by phonons. It is not the medium's gravity. Light does not feel it (the
   record: AX1 "conformal"; PC2 gate 4, lens ratio 4.35 at 40 kpc and 233 at 2.2 Mpc).
2. The medium's own mass gravitates on top of it. Nothing is counted once (QX28).
3. The contact term breaks the medium's conservation: d_t n + div(n v) = lam rho_b. Baryons are a source of the
   medium, at a mass rate lam m M_b. This is my reading of the equation; the literature calls the breaking soft
   (from memory).
4. On this branch c_s^2 = P'/(m P'') = -(a0^2/(lam^2 m^2)) w^2 (1 - w) < 0 (C4). The record found the same sign for
   the X^(3/2) form (CFG122 G5.1, PC2 gate 7).
5. Its a0 is a product of the coupling and the fluid's scale. It has no link to rho_DE.

**3c. What 3a's Lagrangian does in three other regimes.**

*Homogeneous cosmology.* grad X = 0, so J = 0 (TPA1 item 2: isotropy forces the polarization to zero). The
background is P(X) alone: rho = Q P' - P, p = P, c_s^2 = P'/(Q P'') in the record's variable Q (MK2 section 1). The
inverse problem leaves P free, so dust is a choice, not an output. But the exact law in galaxies restricts it. A well
of depth phi holds n = P'(Xbar_0 + phi), and ln[n/nbar_0] is the integral of dX/c_s^2 over that depth. Keeping the
pool below 216 times the mean in a well of depth 4e-6 c^2 needs c_s >= 259 km/s (in the mean of 1/c_s^2); below 10
times the mean it needs 395 km/s (C5). Those densities are the cosmic mean between today and z = 5. So the medium can
be dust in the background (w of order c_s^2/c^2, about 1e-6), but it is warm. This is DT1's trade-off, certified in
MK2 under MK2's three conditions.

Small waves on the uniform medium, with gravity (C3):

    omega^2 = -4 pi G rho_bar k_J^2/(k_J^2 + k^2),      k_J^2 = K P'' = 4 pi G rho_bar / c_s^2.

There is no sound at any k. Below k_J the medium grows like dust. Above k_J the growth rate falls as k_J/k: it
stalls, it does not oscillate. TPA1 item 3 has this for the quadratic P; the form holds for any P. With c_s 300 to
500 km/s, k_J today is 0.141 to 0.085 per Mpc and the growth-rate-squared factor at k = 1 per Mpc is 0.020 to 0.007
(C5). So at late times the medium stays smooth below tens of Mpc, and the CMB-lensing, growth and forest rows are not
carried by it (MK2 row b). The other choice, a cold P with k_J >= 2.5e4 per Mpc, floods every galaxy well (MK1: NO
VALUE). By the record's trade-off no P(X) does both (DT1 section 2; MK1's requirement; MK2's certified statement).

*A galaxy cluster.* In a static state nothing in L tells a cluster from a galaxy. The law applies there too, and with
the law alone X-COP is +0.4675 / +0.4345 dex short (QX2). The only extra cold mass is the pool P'(X0 - Phi). It
depends on depth alone and it is itself a source of the law. On the record no pool passes: the quadratic has no value
(MK1 row 3, closest rms 0.263 / 0.255 against 0.10), the exponential has none (MK2 row c, 0.464 / 0.429, and no
static capped state below 750 to 1000 km/s), the isothermal sea fails on shape (QX12 iter_3). If the medium is not
static it is in free fall, grad X = 0, the law is off and it is ordinary cold mass. But one scalar cannot describe
crossed streams: it folds, and the equations stop (COL1). So "ordinary cold mass at about 5.4 times the baryons in
clusters" is not a state of this Lagrangian. The data side is on the record: the law plus the cosmic ratio comes
close on X-COP with no cluster input (QX12 iter_2: -0.075 / 0.110 and -0.097 / 0.127, FAIL, groups get too much).

*Light.* The medium's pull is the gravity of a real density N, and light sees it. The slip between the two metric
potentials is of the order of stress over rho c^2, that is sigma^2/c^2: 3e-8 to 2e-7 for 53 to 125 km/s (hand
estimate). The record has this from the action: the FB1 note section 1 item 1 (QX17), V3W W1 (gamma - 1 = 0) and W3
(M_lens/M_dyn 1.13 +- 0.21 / 1.03 +- 0.19). In 3b's class the phonon pull does not lens.

*Two things not asked that bind.* (i) The static limit is AQUAL with the law's mu. It fails Cassini (Q2 2.44 to
4.55 / 2.85 to 5.15 times Hees) and the planets unless a screening length is added (AX1; QX29 G8). A first-gradient
medium has no such length; the record's gamma_L term is extra. (ii) Conservation. The halo needs M_c(<r) = M_b a0/g:
59.5 M_b by 116 / 389 / 653 kpc (canonical) and 106 / 354 / 594 kpc (alt) at log M_b 9.4 / 10.45 / 10.9 (C5; the
canonical values equal FLD1's cap column). A static medium has no inflow. FLD1 finds that cold infall delivers 1.6
to 5.1 % of that.

## Step 4. Is the function selected? Is kappa fixed?

**4a. The similarity selects the variable, not the function.** r -> lambda r, M_b -> lambda^2 M_b at fixed G and a0
maps law halos to law halos. It keeps accelerations and pressures and rescales densities and velocities. A local
relation that holds on every halo must be built from what it keeps. So the variable has to be an acceleration. P5
then makes it the medium's own: grad X. That is all the symmetry gives.

**4b. The two ends are fixed by the law, not by a principle.**
- Weak field: J -> s^2/(2K) exactly. The medium cancels the Newtonian field energy with coefficient exactly 1. Any
  other coefficient gives Newton with a rescaled G at low acceleration. I found no reason inside a medium for
  "exactly 1". In the literature this end goes with the scale invariance of the weak-field law (from memory).
- The next term, -s^3/(3 K a0), defines a0.
- Strong field: J' -> a0/K. The pull saturates at a0, and rho_c r -> a0/(2 pi G) = 106.9 (canonical) / 129.2 (alt)
  Msun/pc^2 (C5).

**4c. Between the ends the function is free.** The law's choice is 1/g_c = 1/g + 1/a0. It has several names: the
fractional-linear bridge between a linear response and a cap; a pure logarithmic barrier in the polarization; the
steady occupancy g/(g + a0) of a two-state exchange. These are the same function. Two remarks, neither a derivation.
- A two-state exchange with rates g/c and a0/c has a relaxation time c/(g + a0). At g <= a0 that is at least 50.7 Gyr
  (canonical) / 42.0 Gyr (alt). It would never be reached. M5 row b said the same of c/a0.
- A thermal medium of polarizable units responds analytically in the field (its free energy is even in g). It
  cannot make the |g|^3 term. This is an argument, not a theorem.

**4d. kappa.** The inverse problem never meets rho_DE. a0 enters only as the scale where J saturates. In this
language kappa = 1/2 is the statement (a0^2/K)/(rho c^2) = 1/(16 pi) = 0.01989, and no step here produces that number.
Candidate identities, tried (C5): a0 = cH/(2 pi) gives 0.4607; cH/6 gives 0.4824 (the emergent-gravity value, from
memory); cH gives 2.894; a0^2/K = rho c^2 gives 3.545. None is 1/2. The record already has this: KF1 (NOTHING FORCED;
0.4607 is its R5) and VR1 (NO IDENTITY). kappa is not fixed.

**4e. Plainly.** The outcome is a re-description. Inside it there is one proof that a sub-route cannot work (the
barotropic fluid) and two uniqueness statements (the stress; the scalar Lagrangian). It is not a derivation: P4 is
the law, and J is the law's own function.

**4f. How this differs from the literature's superfluid model** (Berezhiani and Khoury; their name for it is
superfluid dark matter; everything in this paragraph is from memory).
- Theirs: particles of eV mass that condense in galaxies and stay normal in clusters. The Lagrangian is
  P(X) ~ X sqrt|X|. Baryons couple to the phonon through a contact term. The extra pull is a phonon force. Lensing
  comes from the medium's mass, not from the phonon. a0 is set by the coupling and the fluid's scale. Their
  interpolation is not mu = x/(1+x). They cure the wrong-sign sound speed with finite-temperature terms.
- Here (3a): no particle, no phase change, no extra force. The Lagrangian depends on grad X, not on a power of X. The
  extra pull is the medium's own gravity and it lenses. The medium is conserved. The cluster shortfall is not cured
  by a normal phase; it stays.
- Here (3b): their class with the exact mu. It keeps their problems and is not form B.
- The record graded their class as built: QX28, CFG122, PC2, UX1 K10, AX1. All fail.

## Sympy checks

Run from a scratch folder, outside the repo; nothing but this file was written to the repo. sympy 1.13.1, mpmath
1.3.0, about 2 s, one thread.

```python
# Route C checks. sympy 1.13.1, mpmath 1.3.0; about 2 s, one thread. Units inside: K = 4 pi G.
import sympy as sp, mpmath as mp, math
a0, K = sp.symbols('a0 K', positive=True)

print("== C1  barotropic P(rho): point mass on the law, x = r/r_M, u = g/a0")
x = sp.symbols('x', positive=True)
u = (1 + sp.sqrt(1 + 4*x**2))/(2*x**2)
print("law residual u^2/(1+u) - 1/x^2 :", sp.simplify(u**2/(1+u) - 1/x**2))
print("M_c(<r)/M_b - a0/g             :", sp.simplify(x**2*u/(1+u) - 1/u))
R = sp.simplify(sp.diff(1/u, x)/x**2)                 # rho_c in units a0/(K r_M)
S = sp.simplify(u/(-sp.diff(sp.log(R), x)))           # dP/drho needed, in units a0 r_M
print("isotropic P = J(g) balances the point-mass halo, dJ/dx + R u :", sp.simplify(sp.diff(u - sp.log(1+u), x) + R*u))
print("S*R at x = 0.01, 0.1, 1, 10, 100:", [f"{float((S*R).subs(x, v)):.4g}" for v in (sp.Rational(1,100), sp.Rational(1,10), 1, 10, 100)])
print("x^2 S R -> ", sp.limit(S*R*x**2, x, 0), "(strong field),", sp.limit(S*R*x**2, x, sp.oo), "(weak field);  S ->", sp.limit(S, x, sp.oo), "(weak field)")
zc = R/2 - u**2/((u + 2)*sp.sqrt(1 + u))            # zeta = K rho T/a0^2 with T = a0 r_M/2
print("one-label family, zeta - u^2/((u+2) sqrt(1+u)) at x = 0.01 ... 100 (40 digits):", max(abs(sp.N(zc.subs(x, v), 40)) for v in (sp.Rational(1,100), sp.Rational(1,7), 1, 9, 100)))
for rM in (1.0, 4.0):                                 # two masses, the same density, a0 = K = 1
    xs = mp.findroot(lambda xx: float(R.subs(x, xx))/rM - 1e-3, 5.0)
    print(f"   r_M = {rM}: rho = 1e-3 sits at x = {float(xs):.3f}; dP/drho needed = {rM*float(S.subs(x, xs)):.4f}")

print("== C2  local stress A(rho,s,g) delta_ij + B(rho,s,g) ghat_i ghat_j, s a conserved label; jets r, g, g', g'', s, s'")
r, g, g1, g2, s, s1, rh = sp.symbols('r g g1 g2 s s1 rho', positive=True)
rho = (2*a0*g/(r*(g + a0)) + a0**2*g1/(g + a0)**2)/K   # cold density on the law
drho = sp.diff(rho, r) + sp.diff(rho, g)*g1 + sp.diff(rho, g1)*g2
A = sp.Function('A')(rh, s, g); B = sp.Function('B')(rh, s, g)
E = (sp.diff(A, rh) + sp.diff(B, rh))*drho + (sp.diff(A, s) + sp.diff(B, s))*s1 + (sp.diff(A, g) + sp.diff(B, g))*g1 + 2*B/r + rho*g
print("coefficient of g'':", sp.factor(sp.diff(E, g2)))
print("coefficient of s' :", sp.diff(E, s1))
Fp = sp.Symbol('Fp')                                   # so A + B = F(g); Fp = F'(g)
Bx = sp.expand(-(r/2)*(Fp*sp.solve(sp.Eq(rho, rh), g1)[0] + rh*g))
Fps = sp.solve(sp.diff(Bx, r), Fp)[0]; Bs = sp.simplify(Bx.subs(Fp, Fps)); As = sp.integrate(Fps, (g, 0, g)) - Bs
J = (a0**2/K)*(g/a0 - sp.log(1 + g/a0))
print("B =", Bs, ";  A - J(g) =", sp.simplify(sp.expand_log(As - J, force=True)))
print("weak field: A ->", sp.series(J, g, 0, 3).removeO(), ", B ->", sp.series(Bs, g, 0, 3).removeO(), " (minus the Newtonian field stress)")
print("along-field pressure (A+B) K/a0^2 at u = 0.1, 1, 10:", [f"{v - math.log(1+v) - v*v/(1+v):.4f}" for v in (0.1, 1.0, 10.0)])
gf = sp.Function('g')(r); uu = gf/a0                   # where the non-isotropic part acts
rc = sp.diff(r**2*a0*gf/(gf + a0), r)/(K*r**2); rb = sp.diff(r**2*gf**2/(gf + a0), r)/(K*r**2)
print("dJ/dr + rho_c g - a0 rho_b :", sp.simplify(sp.diff((a0**2/K)*(uu - sp.log(1 + uu)), r) + rc*gf - a0*rb))
GM, mm = sp.symbols('GM m', positive=True)             # weak field, gamma = 5/3: the adiabat each halo would need
G_ = K/(4*sp.pi); rofm = mm*G_/sp.sqrt(GM*a0); rhod = sp.sqrt(GM*a0)/(K*rofm**2)   # r(m) and rho(m) on the weak-field halo
print("adiabat P/rho^(5/3) at enclosed cold mass m:", sp.simplify((sp.sqrt(GM*a0)/2)*rhod**sp.Rational(-2, 3)), " (depends on GM = G M_b)")

print("== C3  one conserved scalar medium, gravity only, L(X, |grad X|)")
xx, yy, zz, t = sp.symbols('x y z t', real=True); X3 = (xx, yy, zz)
ph = sp.Function('phi')(xx, yy, zz, t); Ph = sp.Function('Phi')(xx, yy, zz); v = [sp.diff(ph, c) for c in X3]
Xs = -(sp.diff(ph, t) + sum(c**2 for c in v)/2 + Ph)
print("grad X - (g - Dv/Dt):", [sp.simplify(sp.diff(Xs, X3[i]) + sp.diff(Ph, X3[i]) + sp.diff(v[i], t) + sum(v[j]*sp.diff(v[i], X3[j]) for j in range(3))) for i in range(3)])
Xv, q = sp.symbols('X q', positive=True); L = sp.Function('L')(Xv, g); Ls = sp.diff(L, g)
N = sp.diff(L, Xv) + 2*Ls*q - g*sp.diff(Ls, Xv) + sp.diff(Ls, g)*g1          # static: X = X0 - Phi, |grad X| = g, q = 1/r
gc = a0*g/(g + a0); E3 = sp.expand(K*N - 2*gc*q - sp.diff(gc, g)*g1)        # K N must be the law's halo for every profile
print("coefficient of 1/r:", sp.simplify(sp.diff(E3, q)), "  -> K L_s = a0 g/(g + a0), for every X")
print("left over         :", sp.simplify(E3 - q*sp.diff(E3, q) - g1*sp.diff(E3, g1)), "  -> with L_s free of X: L_X = 0")
print("mu = 1 - K J'/g   :", sp.simplify(1 - K*sp.diff(J, g)/g))
k, nb, m2 = sp.symbols('k nbar m2', positive=True); w, W, dph, dPh = sp.symbols('omega W dphi dPhi')
def disp(law):
    dh = sp.I*w*dph - dPh; dN = (m2 + (k**2 if law else 0))*dh/K
    e1 = -k**2*dPh - K*dN; e2 = -sp.I*w*dN - nb*k**2*dph
    M = sp.Matrix([[sp.diff(e1, dph), sp.diff(e1, dPh)], [sp.diff(e2, dph), sp.diff(e2, dPh)]])
    return sp.factor(sp.solve(sp.expand(M.det()).subs(w**2, W), W)[0])
print("waves on a uniform medium, m2 = K P'' = k_J^2:  omega^2 =", disp(True), "(J on);", disp(False), "(J off)")

print("== C4  the literature's class: P(X) with a contact coupling -lam phi rho_b; the extra pull is a phonon force")
lam, m, wv = sp.symbols('lam m w', positive=True)      # w = a_phi/a0 = (lam/a0) sqrt(2 m |X|), 0 < w < 1
gN = (wv*a0)**2/(a0 - wv*a0); gt = gN + wv*a0
print("law residual with g = g_N + a_phi:", sp.simplify(gN - gt**2/(gt + a0)))
Pp = sp.simplify((lam*m/K)*gN/(wv*a0/lam)); Pc = (a0**2/K)*(wv + wv**2/2 + sp.log(1 - wv))
print("P'(X) =", Pp, ";  check dP/dw:", sp.simplify(sp.diff(Pc, wv) - Pp*(-(a0**2/(lam**2*m))*wv)), ";  P(0) =", Pc.subs(wv, 0))
print("small w:", sp.series(Pc, wv, 0, 4), ";  c_s^2 = P'/(m P'') =", sp.simplify(Pp/(m*sp.diff(Pp, wv)/(-(a0**2/(lam**2*m))*wv))))

print("== C5  numbers, SI, each footing on its own")
G = 6.67430e-11; c = 2.99792458e8; Msun = 1.98847e30; pc = 3.0856775814913673e16; kpc = 1e3*pc; Mpc = 1e6*pc
for name, av in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    print(f"{name}: a0/(2 pi G) = {av/(2*math.pi*G)/(Msun/pc**2):.1f} Msun/pc^2;", "radius holding 59.5 M_b at log M_b 9.4 / 10.45 / 10.9:",
          " / ".join(f"{math.sqrt(G*10**lM*Msun/av)*59.5*math.sqrt(1 + 1/59.5)/kpc:.0f}" for lM in (9.4, 10.45, 10.9)), "kpc;",
          "sigma:", " / ".join(f"{math.sqrt(0.5*math.sqrt(G*10**lM*Msun*av))/1e3:.0f}" for lM in (9.4, 10.45, 10.9)), "km/s")
print("kappa if a0 = cH/(2 pi), cH/6, cH (H^2 = 8 pi G rho/3):", [f"{f*math.sqrt(8*math.pi/3):.4f}" for f in (1/(2*math.pi), 1/6, 1.0)],
      "; if a0^2/(4 pi G) = rho c^2:", f"{math.sqrt(4*math.pi):.3f}", "; at kappa 1/2 that ratio is 1/(16 pi) =", f"{1/(16*math.pi):.5f}")
for f, d in ((216, 4e-6), (10, 4e-6), (216, 1e-7)):
    print(f"pool <= {f} x mean in a well of depth {d:.0e} c^2 needs c_s >= {c*math.sqrt(d/math.log(f))/1e3:.0f} km/s")
H0 = 67.4e3/Mpc; nbar = 0.264*3*H0**2/(8*math.pi*G)
for cs in (300e3, 500e3):
    kJ = math.sqrt(4*math.pi*G*nbar)/cs*Mpc
    print(f"c_s {cs/1e3:.0f} km/s: k_J today {kJ:.3f} per Mpc; growth-rate^2 factor at k = 1 per Mpc: {kJ**2/(kJ**2 + 1):.4f}")
```

Output:

```
== C1  barotropic P(rho): point mass on the law, x = r/r_M, u = g/a0
law residual u^2/(1+u) - 1/x^2 : 0
M_c(<r)/M_b - a0/g             : 0
isotropic P = J(g) balances the point-mass halo, dJ/dx + R u : 0
S*R at x = 0.01, 0.1, 1, 10, 100: ['1.999e+04', '190.7', '0.804', '0.005256', '5.025e-05']
x^2 S R ->  2 (strong field), 1/2 (weak field);  S -> 1/2 (weak field)
one-label family, zeta - u^2/((u+2) sqrt(1+u)) at x = 0.01 ... 100 (40 digits): 0.e-171
   r_M = 1.0: rho = 1e-3 sits at x = 31.621; dP/drho needed = 0.5080
   r_M = 4.0: rho = 1e-3 sits at x = 15.807; dP/drho needed = 2.0653
== C2  local stress A(rho,s,g) delta_ij + B(rho,s,g) ghat_i ghat_j, s a conserved label; jets r, g, g', g'', s, s'
coefficient of g'': a0**2*(Derivative(A(rho, s, g), rho) + Derivative(B(rho, s, g), rho))/(K*(a0 + g)**2)
coefficient of s' : Derivative(A(rho, s, g), s) + Derivative(B(rho, s, g), s)
B = -a0*g**2/(K*(a0 + g)) ;  A - J(g) = 0
weak field: A -> g**2/(2*K) , B -> -g**2/K  (minus the Newtonian field stress)
along-field pressure (A+B) K/a0^2 at u = 0.1, 1, 10: ['-0.0044', '-0.1931', '-1.4888']
dJ/dr + rho_c g - a0 rho_b : 0
adiabat P/rho^(5/3) at enclosed cold mass m: 2**(1/3)*K**2*m**(4/3)/(16*pi**(4/3)*sqrt(GM)*sqrt(a0))  (depends on GM = G M_b)
== C3  one conserved scalar medium, gravity only, L(X, |grad X|)
grad X - (g - Dv/Dt): [0, 0, 0]
coefficient of 1/r: 2*(K*(a0 + g)*Derivative(L(X, g), g) - a0*g)/(a0 + g)   -> K L_s = a0 g/(g + a0), for every X
left over         : K*(-g*Derivative(L(X, g), X, g) + Derivative(L(X, g), X))   -> with L_s free of X: L_X = 0
mu = 1 - K J'/g   : g/(a0 + g)
waves on a uniform medium, m2 = K P'' = k_J^2:  omega^2 = -K*m2*nbar/(k**2 + m2) (J on); K*nbar*(k**2 - m2)/m2 (J off)
== C4  the literature's class: P(X) with a contact coupling -lam phi rho_b; the extra pull is a phonon force
law residual with g = g_N + a_phi: 0
P'(X) = -lam**2*m*w/(K*(w - 1)) ;  check dP/dw: 0 ;  P(0) = 0
small w: -a0**2*w**3/(3*K) + O(w**4) ;  c_s^2 = P'/(m P'') = a0**2*w**2*(w - 1)/(lam**2*m**2)
== C5  numbers, SI, each footing on its own
canonical: a0/(2 pi G) = 106.9 Msun/pc^2; radius holding 59.5 M_b at log M_b 9.4 / 10.45 / 10.9: 116 / 389 / 653 kpc; sigma: 53 / 97 / 125 km/s
alt: a0/(2 pi G) = 129.2 Msun/pc^2; radius holding 59.5 M_b at log M_b 9.4 / 10.45 / 10.9: 106 / 354 / 594 kpc; sigma: 55 / 101 / 131 km/s
kappa if a0 = cH/(2 pi), cH/6, cH (H^2 = 8 pi G rho/3): ['0.4607', '0.4824', '2.8944'] ; if a0^2/(4 pi G) = rho c^2: 3.545 ; at kappa 1/2 that ratio is 1/(16 pi) = 0.01989
pool <= 216 x mean in a well of depth 4e-06 c^2 needs c_s >= 259 km/s
pool <= 10 x mean in a well of depth 4e-06 c^2 needs c_s >= 395 km/s
pool <= 216 x mean in a well of depth 1e-07 c^2 needs c_s >= 41 km/s
c_s 300 km/s: k_J today 0.141 per Mpc; growth-rate^2 factor at k = 1 per Mpc: 0.0196
c_s 500 km/s: k_J today 0.085 per Mpc; growth-rate^2 factor at k = 1 per Mpc: 0.0071
```

What the checks do not cover. Theorems 2 and 3 are shown necessary in spherical symmetry only. The wave check is
Newtonian, on a uniform static background (the Jeans swindle). The hand items are marked "hand" in the text: the
steady-flow remark, the inner pull at a wrong T, the matching to the literature's constants, the slip estimate, the
relaxation times. The check C1 line with "0.e-171" is a 40-digit zero.

## What is fixed and what is free

Fixed, once the law is given:
- the stress, J(g) delta_ij - g_i g_j/(K (1 + u)), and that it ignores the medium's density and any label;
- the scalar Lagrangian's gradient part J(|grad X|), the same for every X;
- no pool in galaxy wells: P'(X) = 0 across galaxy depths;
- the halo: M_c(<r) = M_b a0/g; rho_c r = a0/(2 pi G) in the strong field; sigma^2 = (1/2) sqrt(G M_b a0) in the weak
  field.

Free, or put in by hand:
- the function mu itself. The route returns J for any mu. It cannot prefer x/(1+x) over another mu with the same two
  ends;
- a0, so kappa;
- P(X) outside galaxy depths: the whole cosmology and the cluster pool;
- where the halo ends (the cap), and how the medium gets there (conservation, inflow);
- the Solar-System screening term;
- how the static state is reached at all.

## Predictions

| regime | what L = P(X) + J(\|grad X\|) gives | status on the record |
|---|---|---|
| cosmology, background | J is zero. P(X) alone: dust if P is chosen so | free function |
| cosmology, waves | growth rate squared 4 pi G rho_bar k_J^2/(k_J^2 + k^2); no sound; exact galaxies need c_s >= 259 to 395 km/s at late times, so the medium is smooth below tens of Mpc | CMB-lensing, growth and forest rows not carried (MK2 row b); the cold choice floods galaxies (MK1) |
| galaxies | the law, exactly, where the medium is static and P' = 0 | static state stable (SCS1, SCS2); not reached from cold dust (COL1); warm clock static above about 500 km/s (MK2 row i) |
| clusters | the law again, plus a pool that depends on depth alone; not ordinary cold mass at 5.4 times the baryons | law alone +0.47 / +0.43 dex short; no pool passes (MK1, MK2, QX12 iter_3) |
| light | the medium's pull lenses like its dynamical pull; slip of order 1e-7 | QX17; V3W W1, W3; ONE1 passes host-free KiDS at the widest veto |
| Solar System | unscreened AQUAL unless a length is added | AX1, QX29 G8 fail; the record's gamma_L passes |
| amount | 59.5 M_b needed by 116 to 653 kpc (canonical), 106 to 594 kpc (alt) | cold infall delivers 1.6 to 5.1 % (FLD1) |

None of these is new against the record. The route predicts what action (A) already predicts.

## What the record already says

Searched README.md and RESULT.md under closure_2026_11_0*, rebuild_2026_10_22 and fable52_push, before anything was
proposed. Two older lanes those files point to (CFG122, CFG660) were read from their lines in
`campaign_fresh_gravity/LEDGER.md`.

- **superfluid, condensate, phonon.**
  - `closure_2026_11_06/QX28_superfluid_two_phase`: the Berezhiani-Khoury class as built FAILS at G3, G4, G5, G6, G8
    on both footings. Clusters sit between its two phases. Cosmology is stiff. Cassini is inherited from AQUAL.
  - CFG122 (ledger): a scoped no-go for both branches. The law-carrying X < 0 branch has c_s^2 < 0. The phonon force
    is 0.414 off the law at x = 1.
  - `rebuild_2026_10_22/PC2_one_field_phase`: killed at gate 1 as a derivation. A rate that thermalises halos
    thermalises the background first.
  - `rebuild_2026_10_22/UX1_action_class` K10 and `AX1_action_for_law`: fail. AX1: the phonon field is conformal and
    gives no extra lensing.
  - `rebuild_2026_10_22/CA1_covariant_self_coupling`: a condensate fails twice (slope 0; mean free path long).
  - `rebuild_2026_10_22/PH1_two_phase_cold_energy`: NO-GO. `closure_2026_11_08/WD1_cvwd_condensate`: FAIL / FAIL.
    `closure_2026_11_09/SS4_late_pressure_halves`: FAIL / FAIL.
- **k-essence.** `fable52_push/TPA1_two_phase_action`: the law-off phase is a healthy k-essence clock.
  `rebuild_2026_10_22/X60_acceleration_dependent_cold_sector`: a P(X, Y) keyed on the clock's acceleration is
  excluded on every escape. `X14`, `X17`: caustics are generic; the sound-speed term has the wrong sign.
  `M1_trilemma`: a J with J'(0) = 0 fails linear growth.
- **polytrope.** `closure_2026_11_06/QX3_cmb_growth`: the quadratic K(Q) is an n = 1 polytrope with a fixed Jeans
  number; every barotropic K(Q) fails growth or galaxies. MK1 and MK2: no single dust constant, quadratic or
  exponential. COL1: the cold clock folds.
- **equation of state.**
  - `rebuild_2026_10_22/M5_equilibrium_law`: NO-GO for every candidate. Exactly one local stress makes the law the
    equilibrium for every baryon profile, it cannot depend on rho_c, and as an independent-density medium it is
    ill-posed and cancels its own nonlinear self-gravity. Steps 1 and 2 above are inside M5's result. What is added
    here: a proof for all barotropes that needs point masses only, the one-number family with its closed form, and
    the extension to a conserved label.
  - CFG660 (ledger): the law as cold energy's own hydrostatic equilibrium. Exact with a field-aligned stress for
    spheres; isotropic excluded on SPARC; not kinetic; ill-posed.
  - `closure_2026_11_06/QX12_triangle` iter_1 to iter_3: a barotropic sector is not excluded statically by depth
    ordering (clusters are 32 to 33 times deeper than any galaxy point), but the isothermal one fails on cluster
    shape, and the temperature-keyed one is a near miss that fails.
- **dipolar medium.** `closure_2026_11_06/QX29_dipolar_medium`: fails. Not re-proposed. 3a's polarization is tied to
  the medium's own acceleration, not to a separate dipole field; its static content is the same.
- **the owner's medium with a polarization.** `rebuild_2026_10_22/TM1_tethered_medium` scores PAPER49's action
  (rho_c = rho_bar + div P, with a remainder W): "the law side of the split"; it does not resolve law against
  clumping.
- **the action itself.** The FB1 note, QX17, COL1 Part 1: the reduced Lagrangian L_K(h) + J(|grad h|). SCS1, SCS2:
  the static state is stable. M5 calls the density-blind stress ill-posed as an independent medium. The two are
  different dynamics for the same static stress; this route did not adjudicate.
- **kappa.** `rebuild_2026_10_22/KF1_argon_kappa_routes`: NOTHING FORCED.
  `closure_2026_11_08/VR1_vacuum_response_identity`: NO IDENTITY.

Not found on the record by this search: the words "logotropic" and "Langmuir". Nothing above depends on them.

## The weakest step

**Step 3, the passage from "the stress depends on g" to "the medium is one scalar with L(X, grad X)".** It rests on
P5 and on taking the smallest class.
- Theorem 3 is a uniqueness statement inside that class only: one conserved scalar, potential flow, first gradients,
  gravity only.
- A medium with more internal structure is not covered by it: two components with a relative acceleration between
  them, a vector with its own dynamics, an elastic reference state, higher gradients. The record has graded the
  cases it tried (dipoles QX29; the baryons' acceleration REL1; the tethered medium TM1, which M5's scope note sets
  aside without re-scoring). It has not shown that every such medium fails.
- Even inside the class, the result is static. The dynamics are quoted from the record's lanes (COL1, FLD1, MK1,
  MK2, SCS1, TPA1), which were not re-run here.

Second weakest: step 4. "No principle found" is the outcome of a short search by one session, not a proof that none
exists.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
