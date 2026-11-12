# ELA1 FROZEN CRITERIA: the law's halo as an elastic solid (2026-11-11)

TEST lane, quarantined. Relabels nothing, adopts nothing, not registered. kappa = 1/2 FITTED; not theory closed.
Footings graded separately, never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2.
Cold dark energy is a gravitating field component, never a particle. **In this lane it is hypothesised to be an elastic
continuum** (a solid with a displacement field); that hypothesis is what is graded. Nothing here says the data favour the
framework. No LCDM-calibrated machinery enters any verdict.

Committed alone, before any ELA1 script exists and before any ELA1 number is computed.

## 0. The premise this lane takes from the crux check

`hy4_preview_push/hy4_crux_check.py` establishes, for the law's static spherical halo:

    J(g)  = (a0^2/K)[u - ln(1+u)],   K = 4 pi G,  u = g/a0
    Pi_ij = J(g) delta_ij - g_i g_j / (K (1+u))            (the law's field stress)
    Pi_rr = J - g^2/(K(1+u)),   Pi_tt = J
    Pi_rr + Pi_tt -> 0 in the deep field (exactly 0 only as u -> 0)
    sigma_r^2 = Pi_rr/rho_c -> -v_inf^2/2 ,  sigma_t^2 = Pi_tt/rho_c -> +v_inf^2/2 ,  v_inf^4 = G M_b a0

**The radial "dispersion" is negative.** A kinetic gas has sigma_r^2 = <v_r^2> - <v_r>^2 >= 0 for every f >= 0, so no
kinetic medium (cold, warm, hot, collisionless, collisional, anisotropic) can carry this stress. A medium with a shear
modulus can: in a solid the stress is not a dispersion, and a radial tension beside a tangential compression is a shear.
This lane asks what that solid must BE, and grades it.

## 1. The candidate, stated once and binding on every reading below

The cold component is an isotropic elastic continuum. Its state is a displacement xi(x) from an unstressed reference
configuration of uniform density rho_ref (the homogeneous cosmological medium). Strain u_ij = sym grad xi (linearised);
in spherical symmetry u_rr = xi', u_tt = xi/r. Constitutive relation (isotropic, local in the strain):

    sigma_ij = 2 mu_s u_ij + lambda u_kk delta_ij ,     W = mu_s u_ij u_ij + (lambda/2) u_kk^2

Static equilibrium: div sigma = rho_c grad Phi, with del^2 Phi = 4 pi G (rho_b + rho_c) (normal self-gravity; no hold,
no cancellation, no tether). The candidate is the member of this family for which

    (C1) the equilibrium stress is exactly the law's field stress:  sigma_ij = Pi_ij(g)
    (C2) the elastic energy density of that state is exactly J(g):  W = J(g)
    (C3) mass is conserved by the deformation:  rho_c(x) = rho_ref / det(F), F = I + grad xi

C1 is forced: M5's S2 proves the stress that makes the law an equilibrium for every baryon profile is unique and is
Pi_ij(g), density-blind. C2 is the brief's "exactly J(g) as its energy". C3 is what makes it a material at all.

**What is put in by hand (binding on every reading).** The law's function enters through Pi_ij and J; C2 and C3 are
postulates about the material. A pass anywhere in this lane is an existence statement about an elastic joint, not a
derivation of the law.

## 2. Hand estimate (written before any script; to be compared with the outcome in RESULT.md)

**Mine.**
- **The deformation is fixed by mass conservation alone, before any constitutive law is chosen.** In the deep field the
  law's halo has M_c(<r) = M_b r/r_M, so a uniform reference gives R = [3 M_c/(4 pi rho_ref)]^{1/3} ~ r^{1/3}, i.e. the
  Eulerian radius grows as the CUBE of the Lagrangian radius: r = R^3/r_M^2 in the normalisation where the Lagrangian
  sphere of radius r_M holds M_b. Then y = R/r and
      u_tt = 1 - y ,  u_rr = 1 - y/3 ,  u_rr - u_tt = (2/3) y > 0.
  With the cosmic reference density (rho_ref = 5.41 rho_b,0 = 34 Msun/kpc^3) and log M_b = 11, y = R/r is 62 at
  r = r_M: the density contrast is y^3/3 = 7.9e4 and **the strain is |u_tt| = 61**. For any assembly redshift from 0 to
  10 (rho_ref up to 4.5e4) y is 5 to 62, so the strain is never small. **A linear elastic solid cannot deliver the
  halo's density contrast at all**: with |u| <~ 1 the contrast is at most of order 1, against 1e5 needed.
- **The sign of the shear modulus comes out negative, and this is a sign argument, not a number.** The stress anisotropy
  is sigma_rr - sigma_tt = -g^2/(K(1+u)) < 0 (radial TENSION beside tangential COMPRESSION). The strain anisotropy in
  the mass-conserving map is u_rr - u_tt = (2/3) y > 0 (stretched MORE radially than tangentially). Since
  sigma_rr - sigma_tt = 2 mu_s (u_rr - u_tt), **mu_s < 0 everywhere**. Both in the deep field (M_c ~ r) and in the
  inner field (M_c ~ r^2, giving u_rr - u_tt = (1/3) y > 0) the sign is the same.
- **Therefore c_T^2 = mu_s/rho_c < 0: the transverse sound speed is imaginary at every radius, and the growth rate of
  the transverse mode is s = |c_T| k, unbounded in k -> Hadamard ill-posed.** This is M5's S4 disease (s^2 = i k g,
  |Re s| ~ sqrt k) returning through the shear sector instead of the compressive one. I expect c_L^2 < 0 over most of
  the halo as well, with a narrow shell near y = 9/7 where it is positive and diverging.
- **The elastic energy does not match J.** For a quadratic energy, 2W = sigma:u, so
  2W = Pi_rr u_rr + 2 J u_tt = J(1 - 5y/3), i.e. W = (J/2)(1 - 5y/3): it equals J only at y = -3/5 (impossible, y>0),
  is 0 at y = 3/5, and is **negative for all y > 3/5**, which is the whole halo at any assembly redshift. So C1 and C2
  and C3 cannot hold together. Independent of rho_ref.
- **The energy condition alone (C1 + C2, dropping C3) integrates to a linear ODE for the displacement:**
  Pi_rr xi' + 2 J xi/r = 2J. In the deep field its solution is xi = 2r + C r^2. C = 0 gives u_rr = u_tt (pure
  dilation) against an anisotropic stress, i.e. mu_s = infinity. C != 0 makes the Lagrangian map R = r - xi fold
  (dR/dr < 0 for r < 1/(2|C|)) and makes rho_c/rho_ref = (|C|r - 1)^2 (2|C|r - 1) negative for |C| r < 1 and growing
  as r^3 for large r, against rho_c ~ 1/r^2. So C3 fails there too.
- **The Bullet.** A solid is defined by resisting shear: its deformation map is a homeomorphism, so its material
  elements keep their neighbours and two solid halos cannot interpenetrate. RB1's gate 4 places the lensing mass with
  the galaxies, which did pass through; DB1's criterion for a component that passes is G Sigma_c^2 >= rho_ICM v^2 at
  v = 4700 km/s. Whatever the solid's own strength, at 4700 km/s it is either stronger than the impact and stops
  (no offset: killed by RB1's offset) or weaker and yields, and a yielded solid is a fluid, which is M5's class.
  I expect this gate to FIRE.
- **Expected label: ELASTIC SOLID FAILS AT S1 (sound speeds) on both footings**, with the strain/energy gates (S0) and
  the Bullet (B1) firing alongside and independently. S2 (recombination), S3 (clusters), S4 (amount) not reached.
- **Where I expect to be wrong:** the strain magnitude depends on rho_ref, which I have bracketed rather than fixed; if
  the reference configuration is allowed to be inhomogeneous the map is not determined by mass conservation alone and
  S0's strain argument weakens (the sign argument does not: it needs only u_rr - u_tt > 0, which follows from
  dR/dr < R/r, i.e. from the medium having gathered mass inward).

**The parent's (quoted from the brief).** The Bullet and the sound speeds are named in advance as the gates most likely
to kill it. The mutation arm must fail.

## 3. Fixed inputs

- Units kpc, km/s, Msun. G = 4.30091e-6 kpc (km/s)^2 / Msun. a0 in (km/s)^2/kpc = a0[SI] x 3.0857e19/1e6
  (canonical 2888.4, alt 3489.9). K = 4 pi G.
- Masses log M_b = 9.4, 10.45, 10.7, 10.9 (the record's four). r_M = sqrt(G M_b / a0).
- Sizes: R_50 from SCS2's relation (Shen et al. 2003 late types, as SCS2 quoted it from memory; read, not re-sourced):
  R_50 = 0.10 kpc M^0.14 (1 + M / 3.98e10)^0.25. Extended spherical profiles set to that R_50: Plummer
  (b = R_50/1.3048) and Hernquist (a = R_50/(1+sqrt2)). Point mass as the third profile.
- The law (spherical, exact): mu(u) g = g_N with mu = u/(1+u); g = (g_N + sqrt(g_N^2 + 4 a0 g_N))/2;
  rho_c = (1/K r^2) d[r^2 (g - g_N)]/dr. Point mass: M_c(<r) = M_b (sqrt(1+4x^2)-1)/2, x = r/r_M.
- Reference density rho_ref: primary the cosmic cold density today, 5.41 x Omega_b x rho_crit with Omega_b = 0.049,
  h = 0.679 (33.9 Msun/kpc^3). Brackets: the same at z = 2, 5, 10 (x27, x216, x1331) and, as an extreme, z = 1100.
- Graded window: r in [0.2, 60] r_M, 80 log-spaced points (60 r_M is the crux's share-59.5 halo edge). The SPARC
  window [0.3, 6] R_50 is reported for the field comparison only.
- SPARC line (dex in g): 0.0660 canonical / 0.0658 alt.
- Sound-speed line: c = 2.99792458e5 km/s.

## 4. Items in order; stop at the first structural failure, but run every gate that does not depend on it

### S0. The deformation (mass conservation alone, no constitutive law)

- **S0a (sympy, exact).** For the point mass, R(r) = [3 M_c(r)/(4 pi rho_ref)]^{1/3}; prove u_rr - u_tt = (2/3)(R/r)
  in the deep field and (1/3)(R/r) in the inner field, i.e. > 0 for every r. (The identity u_rr - u_tt = R/r - dR/dr
  is exact; the two limits are the asymptotics of dR/dr.)
- **S0b (numbers).** For the three profiles, four masses, both footings, and each rho_ref bracket: y = R/r over the
  window; the strain pair (u_rr, u_tt); max |u|; the density contrast rho_c/rho_ref; the value of y at r = r_M.
- **S0 rule.** STRUCTURE FAILS AT S0 if, for any rho_ref bracket in [z=0, z=10], max|u| over the window exceeds 1
  (no linear elastic solid can carry it) or the map R(r) is not strictly increasing on the window (a solid's map is a
  homeomorphism; folding is forbidden).

### S1. The moduli and the sound speeds  (THE PRE-REGISTERED GATE MOST LIKELY TO KILL)

Given sigma = Pi (C1) and the strain from S0:

    mu_s = (Pi_rr - Pi_tt) / (2 (u_rr - u_tt))        [exact, from the difference of the two constitutive equations]
    lambda = (Pi_tt - 2 mu_s u_tt) / (u_rr + 2 u_tt)  [exact]
    c_T^2 = mu_s / rho_c        (transverse)
    c_L^2 = (lambda + 2 mu_s)/rho_c   (longitudinal)

- **S1a (sympy, exact).** Verify the two inversion formulas by back-substitution into sigma = 2 mu u + lambda u_kk d.
- **S1b (numbers).** c_T^2(r) and c_L^2(r) over the window, three profiles, four masses, both footings, every rho_ref
  bracket. Report: sign; min and max; the radius where each first exceeds c^2 if positive; the radius where each first
  goes negative if it does.
- **S1c (locality).** Report mu_s and lambda against the two local scalars (rho_c/rho_ref, u = g/a0) for the three
  profiles at the four masses. If the points collapse onto one curve, state the closed form (I expect
  mu_s = -(3/2) J (rho_ref/(3 rho_c))^{1/3} in the deep field, which is a LOCAL function of (rho_c, g) and therefore
  inside M5's first hypothesis). If they do not, the constitutive relation is not universal; report which profile
  breaks it.
- **S1 rule.** STRUCTURE FAILS AT S1 if, anywhere on the graded window at any mass on either footing, c_T^2 < 0 or
  c_L^2 < 0 (imaginary sound speed: gradient instability, growth rate |c| k unbounded in k, Hadamard ill-posed), or
  c_T^2 > c^2 or c_L^2 > c^2 (superluminal). Both count; a single point fires the gate.

### S2. The energy (C2)

- **S2a (sympy, exact).** For a quadratic elastic energy, 2W = sigma : u (Euler). Hence C2 reads
  Pi_rr u_rr + 2 J u_tt = 2J. In the deep field with S0's strain this is J(1 - 5y/3) = 2J, i.e. y = -3/5.
- **S2b (numbers).** W/J over the window, three profiles, four masses, both footings, every rho_ref bracket. Report
  where W < 0 (a negative elastic energy density: the state can lower its energy by deforming further).
- **S2c (reported, not label-setting).** Drop C3 and integrate the C1+C2 ODE Pi_rr xi' + 2 J xi/r = 2J from a regular
  centre; report xi, the strain, the implied moduli, and whether rho_c/rho_ref = (R/r)^2 (dR/dr) with R = r - xi can
  equal the law's rho_c/rho_ref for any rho_ref.
- **S2 rule.** STRUCTURE FAILS AT S2 if |W/J - 1| > 0.01 anywhere on the window, or W < 0 anywhere on the window.

### B1. The Bullet  (THE PRE-REGISTERED GATE MOST LIKELY TO KILL)

- **B1a (structural).** A solid's map is a homeomorphism. In a 1:1 cluster passage the two halos' media must
  interpenetrate over the overlap volume. State the interpenetrated mass (both clusters' media inside the overlap) and
  note that a homeomorphism cannot deliver it. RB1's gate 4 puts the lensing mass with the galaxies (model peak 14/10
  kpc from the galaxies); the gas sits hundreds of kpc away.
- **B1b (numbers).** DB1's own criterion for a component that passes through, transcribed: (i) Sigma_c >= 3 x the ICM
  column swept in one passage (main-cluster central density, 1 Mpc path); (ii) G Sigma_c^2 >= rho_ICM v^2 at
  v = 4700 km/s. Compute both for the solid's column. Alongside: the solid's elastic Mach number v/|c_T| and
  v/c_L where those are real, and the ratio of the impact energy density (1/2) rho_c v^2 to the solid's own elastic
  energy density |W|. If (1/2) rho_c v^2 >> |W| the solid yields; a yielded solid is a fluid and is M5's class, and
  M5's NO-GO applies to it.
- **B1c (the dilemma, frozen).** Whatever the numbers, the gate fires: if the solid is strong enough not to yield it
  does not pass through and RB1's offset kills it; if it yields it is not a solid. State which horn the numbers pick.
- **B1 rule.** STRUCTURE FAILS AT B1 if the medium cannot both pass through the gas and the other cluster's medium AND
  stay with the galaxies, at v = 4700 km/s.

### S3. Clusters (reported, graded only if S1 and B1 do not fire)

- Can the same solid be hot and at full share. "Hot": the cluster's cold component carries the velocity dispersion the
  data require (~1000 km/s at R500). A solid supports that only while mu_s/rho_c = c_T^2 >~ sigma_v^2; above it, it
  melts. Report c_T^2 and c_L^2 in the cluster regime (log M_b 14-15, r to R500) against sigma_v^2, and the melt
  condition. "Full share": the amount is RB1's gate 1 (f_ret -> 1), which a real-mass medium satisfies by
  construction; report whether the SOLID's equilibrium density in a cluster follows RB1's gate-3 line (ZN4's native
  collisionless shape, 0.10 dex in M(<r)) or whether the elastic equilibrium forces a different shape.

### S4. Recombination and the expanding universe (reported, graded only if S1 does not fire)

- The homogeneous reference state has xi = 0, so sigma = 0 and the background is exactly dust at the background level.
  Report: the elastic Jeans length lambda_J = c_L sqrt(pi/(G rho_c)) in the background at z = 1100 against the comoving
  scales of the acoustic peaks, using the constitutive law S1c fitted in the halo; and whether mu_s -> 0 in the
  background (if mu_s is proportional to a positive power of g, the background is a shear-free dust and the gate passes
  trivially; if mu_s carries the sign found in S1, the background is already unstable).
- Coupling: the solid has no non-gravitational coupling to the plasma by construction, so the drag bound that killed
  MEDIUM_DESIGN section 3's baryon-coupled medium does not arise. Report it as a pass with that stated reason, not as
  evidence for the candidate.

## 5. M5's three hypotheses

Frozen, to be answered explicitly in RESULT.md with the evidence: is this solid (i) LOCAL (stress an algebraic
function of the state at the same point), (ii) MOMENTUM-CONSERVING (symmetric stress, force density div sigma, no
external hold), (iii) NORMALLY SELF-GRAVITATING (rho_c in Poisson, no cancellation)? If all three, M5's NO-GO applies
and its conclusion must show up here as the instability, the missing attractor, or the cancelled self-gravity. State
which of the three it shows up as. If any hypothesis fails, name it and say what the solid buys by dropping it.

## 6. Known answers (must pass before any row is graded)

- **KA1.** Pi_rr + Pi_tt -> 0 in the deep field: the exact expression 2J - g^2/(K(1+u)) has the limit ratio
  (Pi_rr+Pi_tt)/J -> -2u as u -> 0; check numerically at u = 1e-1, 1e-2, 1e-3 to 1e-6 relative.
- **KA2.** sigma_r^2 -> -v_inf^2/2 and sigma_t^2 -> +v_inf^2/2 at x = 1e3, 1e4 to 1e-6 relative (crux A5).
- **KA3.** Point-mass M_c closed form M_b(sqrt(1+4x^2)-1)/2 against the numeric integral of rho_c at
  x = 0.1, 0.3, 1, 3, 10 to 1e-6 relative (crux A1).
- **KA4.** The inversion identities of S1a, checked on 200 random (u_rr, u_tt, mu_s, lambda) draws to 1e-12.
- **KA5.** The Navier-Cauchy dispersion: rho xi_ddot = (lambda+mu)grad div xi + mu del^2 xi gives s^2 = -c_L^2 k^2 for
  longitudinal and s^2 = -c_T^2 k^2 for transverse, symbolically for constant moduli.
- **KA6.** Mass conservation: 4-pi-integral of rho_c over the Eulerian ball equals 4-pi-integral of rho_ref over the
  Lagrangian ball, to 1e-8, for each profile and rho_ref.
- **KA7.** Newtonian limit (a0 x 1e-6): Pi -> 0 and the halo vanishes; rho_c/rho_b -> 0 to 1e-4.
- **KA8.** 2W = sigma:u for a quadratic energy, symbolically on a random symmetric strain.

## 7. MUTATE arms (each must bite; outputs `ela1_MUTATE_<arm>.out/.json`)

- **M1 (sign).** Flip the sign of the field stress (sigma -> -Pi). The equilibrium force balance
  div sigma = rho_c grad Phi must fail (the halo is not the law): report the rms of log10(g/g_law) and require it to
  exceed the SPARC line.
- **M2 (no law).** Newtonian field (a0 x 1e-6) in place of the law's. Pi -> 0, mu_s -> 0, and the halo must miss the
  law by more than the SPARC line in the window.
- **M3 (no shear anisotropy).** Replace Pi_ij by an isotropic pressure P = J (drop the g_i g_j term). This is the
  kinetic reading. The sound speeds must change sign (c_T^2 must become 0 or the gate must change) AND the halo must
  miss the law by more than the SPARC line: report both.
- **M4 (no mass conservation).** Drop C3 and use S2c's ODE branch xi = 2r + C r^2 with C chosen to make c_T^2 > 0.
  Report rho_c/rho_ref from the map against the law's rho_c/rho_ref; require them to disagree by more than a factor 2
  somewhere in the window.
- **M5 (reference density).** rho_ref at z = 1100 (x1.33e9). The strain must fall below 1 somewhere, and the S1 sign
  must NOT change (the sign argument is rho_ref-independent). Report both; if the sign changes, M5 does not bite and
  S1's verdict is not the sign argument.

## 8. What counts AGAINST the candidate (frozen)

- An imaginary sound speed anywhere on the graded window, or a superluminal one (S1).
- A negative elastic energy density, or W not equal to J (S2).
- A strain beyond the linear regime, or a folding Lagrangian map (S0).
- Not passing through in the Bullet, or yielding there (B1).
- Not hot and not at full share in clusters (S3).
- Failing to stay decoupled from the plasma, or an elastic Jeans length above the acoustic scales (S4).
- Falling inside all three of M5's hypotheses with no new escape (section 5).

## 9. Labels (vocabulary frozen)

Per footing: **ELASTIC SOLID FAILS AT <item>** / **ELASTIC SOLID HOLDS (NO GATE FIRES)** / **NO VERDICT** (a known
answer of the item that would set the label fails). The item named is the FIRST of S0, S1, S2, B1, S3, S4 to fire,
with every other gate that fired listed after it. Both footings are always reported. Never "passes".

## 10. Output and process

`ela1.py` writes `ela1.out` and `ela1.json`; MUTATE runs write `ela1_MUTATE_<arm>.*`. One thread, `nice -n 10`, no
downloads. Later changes go in `AMENDMENT_An.md`, each committed alone, marked post hoc if any number has been seen.
`RESULT.md` leads with the label for both footings.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
