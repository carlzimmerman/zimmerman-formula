RE-DESCRIPTION ONLY

# Route A: saturation statistics (SHAPE search, 2026-11-10)

Adopts nothing. Not registered. A note with checks, not a graded lane: no criteria, no label. Every number below is
hand-level arithmetic from the script pasted in section 4. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10),
never pooled. The cold component is cold dark energy, a gravitating field component, never a particle.

## Answer first

- The law does follow, exactly and in two lines, from a two-state site model. But the model's balance equation,
  a0 theta = g (1 - theta), **is the law rearranged**. The postulates hold the same content as the law: one shape
  choice, one tuned equality, one scale. So this is a re-description, not a derivation.
- **The record already has it.** Lanes A2, A35 and A63 of the 10-21 push, CFG695, AG6A and AG6B built this model,
  checked it, and labelled it a postulate (section 7). Nothing in section 3 steps 1 to 5 is new.
- kappa is not fixed. The model gives a0 as a ratio of two rates and says nothing about either.
- Where the model says more than the law, it fails or is empty:
  - with the release rate a0/c, equilibrium takes 102 / 84 Gyr in weak fields. It is not reached;
  - in clusters it gives the plain law, with a hard cap, and no inertia;
  - in the smooth universe it gives exactly nothing, so it is not the CMB's cold dust;
  - "counted once" cannot be kept: if the sites capture the conserved cold component, a0 stops being universal.

## 1. The postulates

Units: K = 4 pi G, u = g / a0, g the magnitude of the total field (baryons plus cold component).

- **P1, sites.** On each leaf of the clock there is a medium of independent cells. A cell is empty or full. A full
  cell carries one unit of gravitational polarization along the local total field. With a fraction theta of cells
  full, K P = C theta g_hat. C is the capacity.
- **P2, capture.** An empty cell fills at the rate k_c g: linear in the magnitude of the total field at the cell.
- **P3, release.** A full cell empties at a constant rate k_r, the same everywhere, independent of g.
- **P4, criticality.** The capacity equals the half-filling field: C = k_r / k_c. Call it a0.
- **P5, dark-energy tie.** k_c = 1 / c and k_r = (1/2) sqrt(G rho_DE). Then a0 = (1/2) c sqrt(G rho_DE), and the
  release rate is a0 / c.
- **P6, what the cold component is.** Its density is the bound density of the polarization, rho_c = - div P (the
  record's D.P), and it gravitates like any density. In a round system that is g_c = K |P|.
- **P7, work.** The field does work P . dg on the medium (the record's P^m A_m term). Needed only for W and J.

What the brief asked for, and what I could not supply:

- *Why the capture rate is linear in g.* No reason found. g / c is the only rate that g and c make. An Unruh-type
  pump has a rate proportional to a temperature proportional to g. The record took that as an assumption, "not
  derived" (AG6B, C-1), and its de Sitter versions give the wrong scale or a different law (AG6B C-5, E-1, E-2).
- *Why the release rate is set by dark energy.* No reason found. P5 is the owner's relation written as a rate.
- *P4* sets two unrelated numbers equal. Without it there is no law at all (check C2).

**The share reading**, which the brief words it in, needs no P4: every unit of the total pull is either
baryon-sourced or cold-sourced; a cold-sourced unit turns baryon-sourced at the rate g / c, and back at a0 / c. The
shares are then theta and 1 - theta, and they add to one by construction. But by Gauss's law a unit of pull that
changes its source is mass that appears or disappears. That is not a mechanism, so I use P1 to P6.

## 2. Why the label is not DERIVED FROM STATED POSTULATES

A derivation should start from less than it ends with, or fix something the result leaves open. Count:

| | the law | the site model |
|---|---|---|
| shape | one function, x / (1 + x) | two choices (one occupant per cell; capture first order in g) |
| tuning | none | one: capacity = half-filling field (P4) |
| scale | a0 | a0 = k_r / k_c |
| kappa | fitted | free |
| new, checkable | | the relaxation rate; fails at a0 / c (section 3, step 10) |

## 3. The derivation, every step

1. Rate equation for the full fraction: d theta / dt = k_c g (1 - theta) - k_r theta.
2. Stationary state: theta = k_c g / (k_c g + k_r) = u / (1 + u), with a0 = k_r / k_c (P4, P5). This is the Langmuir
   form. The same theta comes from the grand-canonical statistics of independent two-state sites at fugacity z = u:
   the site's partition function is 1 + z and its mean occupation is z / (1 + z).
3. Polarization: K P = a0 theta g_hat = [a0 g / (g + a0)] g_hat.
4. Round system (P6): g_c = K |P| = a0 g / (g + a0). So 1 / g_c = 1 / g + 1 / a0, and g_N = g - g_c = g^2 / (g + a0).
   That is the law, exactly (check C1).
   - Cold share of the pull: g_c / g = a0 / (g + a0) = 1 - theta, the empty fraction.
   - Cold pull in units of its capacity: g_c / a0 = theta, the full fraction. Also g_N / g = theta.
   - Written with the baryon field: g_c^2 = g_N (a0 - g_c). Same equation.
5. Any static geometry: Gauss's law div g = - K (rho_b + rho_c) with P6 gives div[mu g] = - K rho_b with
   mu = 1 - a0 theta / g = u / (1 + u). This is the record's static equation with mu_K = 0 and no stiffness (FB1 note,
   section 1 item 3).
6. **What steps 1 to 4 amount to.** Step 2 with P4 reads a0 g_c = g (a0 - g_c). Put g_N = g - g_c into the law
   g_N (g + a0) = g^2 and the same line comes out. The balance equation is the law.

**(i) Does the model give W, or only the response?** Only the response (checks C3, C4, C5).

7. The site model's own potentials are the grand potential, ln(1 + z) per site, and the free energy of filling,
   y ln y + (1 - y) ln(1 - y). Neither is J or W. In the site model the partner of the filling y is ln u, not u. The
   record said so already: W "is conjugate to the activity, not to a chemical potential" and is "not an equilibrium
   free energy" (A2).
   - With P7 added, J is the integral of P dg and W is its Legendre partner. Then J = (a0^2 / K)[u - ln(1 + u)] and
     W = (a0^2 / K)[- y - ln(1 - y)] exactly. But P7 gives the Legendre pair of any response at all. The FB1 note's
     caution applies: this is not evidence that this J is the right one.
   - A dictionary, for what it is worth. In units of kT per site, J(u) is the grand potential of a site with no
     occupation limit minus that of a one-occupant site, at the same fugacity u. W(y) is the lattice-gas pressure
     minus the ideal-gas pressure, at the same filling y. Among all responses, "W = pressure minus ideal pressure"
     holds only for the two-state one (C5). It is an identity. It does not say why a gravitational energy should be
     an excess pressure.

**(ii) Not static, not spherical.**

8. Not spherical, static: step 5. Nothing new. The one-line form 1 / g_c = 1 / g + 1 / a0 then holds for K |P|, not
   for |g_c|, and the cap is on K |P|. If capture were driven by the baryon field instead (the last line of step 4),
   the two readings agree in round systems and differ elsewhere; the record marks the baryon-driven law unstable
   (REL1), so only the total-field reading is kept.
   - Not static: d theta / dt = Gamma0 [u (1 - theta) - theta]. The filling relaxes at the rate Gamma0 (1 + u) (C6;
     the record has this line with Gamma0 free, AG6B S-d). The model is first order in time and dissipative. The
     record's action is second order and conservative. They are different theories once anything moves.
   - A lagging polarization pulls back on whatever moved. The energy goes to a bath the model does not name. A2
     found the same from the other side: no two-level system in thermal equilibrium with a field-linear coupling
     gives this response, so it is a driven steady state, or an equilibrium with a reservoir whose activity is
     proportional to g. Neither the power source nor the reservoir is identified.
   - Fast limit (Gamma0 far above every rate of change): the static equation at each instant. The halo is slaved
     to the baryons' present field. It has no inertia.
   - Slow limit: the halo is left where the field used to be, and decays there.
   - For a bar turning in 30 Myr to see a settled halo, the rate must be 1.7e4 / 1.4e4 times a0 / c.

**(iv) Is there a conserved quantity, so that the component is counted once?** Not the one form B needs.

9. What is conserved:
   - The number of cells. That is the capacity, not the cold component.
   - The bound density, trivially: d rho_c / dt + div(- dP / dt) = 0 for any P. Its total over a large volume is a
     surface term. For a statistically isotropic universe the mean is zero: halos are positive, the space between
     them negative (the record's SCS2 saw negative phantom density only with an external field; same thing).
   - Around one isolated mass the bound mass inside R is a0 theta R^2 / G, which grows without limit. This is "the
     law with no end" (ONE1's wording), not form B. Nothing in the model knows the cosmic share of 5.4.
   - Forcing the link: let a capture draw one unit from the free cold component, of density n_f. Mass action then
     gives theta = g n_f / (g n_f + a0 n_star) (C7). The half-filling field becomes a0 n_star / n_f. It varies with
     the free density from place to place and with epoch. A universal a0 is lost.
   - The only way out is a capture rate that does not depend on how much free component is present, until it runs
     out. That is form B's cap put in by hand. The captured material also has to arrive as dust first, which is the
     record's closed joint (COL1, FLD1; PD1 and PD2 graded "the halo is captured dust": FAIL / FAIL).
   - The record's action keeps one charge another way: one conserved current whose charge is the dust plus D.P
     (QX17 E3). That is a property of the action. The site statistics do not reproduce it.

**(v) Time to equilibrium, against galaxy ages.** With P5 as written it is not reached.

10. From empty, theta(t) = theta_eq [1 - exp(- (a0 / c)(1 + u) t)]. c / a0 is 101.5 / 84.0 Gyr.

    | fraction of equilibrium reached | u 0.01 | 0.1 | 1 | 10 | 100 |
    |---|---|---|---|---|---|
    | after 13.8 Gyr, canonical | 0.128 | 0.139 | 0.238 | 0.776 | 1.000 |
    | after 13.8 Gyr, alt | 0.153 | 0.165 | 0.280 | 0.836 | 1.000 |
    | after 3.0 Gyr, canonical | 0.029 | 0.032 | 0.057 | 0.278 | 0.949 |
    | after 3.0 Gyr, alt | 0.035 | 0.039 | 0.069 | 0.325 | 0.973 |

    - At a0 and below, where the law is measured, the cold pull would be 0.24 / 0.28 of the law's value or less
      after 13.8 Gyr, and under 0.07 after 3 Gyr.
    - To reach 95 % in weak fields the rate must be 22 / 18 times a0 / c within 13.8 Gyr, and 101 / 84 times within
      3 Gyr (discs at redshift 2). To follow a bar, 1e4 times.
    - So "a0 / c is 0.14 of the Hubble rate" (0.143 / 0.173 of H0 at 67.4) is the wrong way round for an
      equilibrium. It says equilibrium takes seven Hubble times. Only the ratio k_r / k_c can be a0; the rates
      themselves must be far faster, and are then a free number with no tie to dark energy.

## 4. Sympy checks (run once, about 3 s; the script is pasted here and is not saved in the repository)

```python
import sympy as sp, math
g, a0, kc, kr, th, t, G0, C, s = sp.symbols('g a0 k_c k_r theta t Gamma0 C s', positive=True)
u, y, z, x, nf, ns = sp.symbols('u y z x n_f n_star', positive=True)
Z = lambda e: sp.simplify(e)

print("C1 rate balance")
th_eq = sp.solve(sp.Eq(kc*g*(1-th), kr*th), th)[0]
print("  theta_eq =", Z(th_eq))
th_eq = th_eq.subs(kr, a0*kc); gc = a0*th_eq; gN = g - gc
print("  g_c - a0 g/(g+a0) =", Z(gc - a0*g/(g+a0)), "| g_N - g^2/(g+a0) =", Z(gN - g**2/(g+a0)))
print("  1/g_c - 1/g - 1/a0 =", Z(1/gc - 1/g - 1/a0), "| g_c/g - a0/(g+a0) =", Z(gc/g - a0/(g+a0)))
print("  g_N/g - g_c/a0 =", Z(gN/g - gc/a0), "| g_c^2 - g_N(a0-g_c) =", Z(gc**2 - gN*(a0-gc)))

print("C2 capacity C and half-filling field s kept apart")
print("  g_N =", sp.series(g - C*g/(g+s), g, 0, 3))

print("C3 Legendre pair")
J = u - sp.log(1+u); W = -y - sp.log(1-y); yu = u/(1+u); uy = y/(1-y)
print("  J' - y =", Z(sp.diff(J,u)-yu), "| W' - u =", Z(sp.diff(W,y)-uy),
      "| W + J - u y =", Z(W.subs(y,yu)+J-u*yu), "| J - int y du =", Z(J-sp.integrate(yu,(u,0,u))))

print("C4 the two-state site's own thermodynamics (units kT per site)")
lnxi = sp.log(1+z)
print("  z dlnxi/dz - z/(1+z) =", Z(z*sp.diff(lnxi,z) - z/(1+z)))
print("  J(z) - lnxi =", Z(J.subs(u,z)-lnxi), "| J(z) - (z - lnxi) =", Z(J.subs(u,z)-(z-lnxi)))
f = y*sp.log(y) + (1-y)*sp.log(1-y); mu = sp.diff(f,y)
print("  exp(df/dy) - y/(1-y) =", Z(sp.exp(mu) - uy), " (conjugate of y is ln u, not u)")
p_lat = Z(y*mu - f)
print("  p_lattice + ln(1-y) =", Z(p_lat + sp.log(1-y)), "| W - (p_lattice - y) =", Z(W-(p_lat-y)))
print("  W - f at y=1/2 =", sp.N((W-f).subs(y, sp.Rational(1,2)), 6), " (W is not the site free energy)")

print("C5 which responses have W = pressure - ideal pressure?")
zf = sp.Function('z')
print("  ", sp.dsolve(sp.Eq(x*zf(x).diff(x), zf(x)*(zf(x)+1)), zf(x)))

print("C6 relaxation from empty")
thf = sp.Function('theta')
sol = sp.dsolve(sp.Eq(thf(t).diff(t), G0*(u*(1-thf(t)) - thf(t))), thf(t), ics={thf(0):0})
print("  theta(t) - y(1-exp(-Gamma0(1+u)t)) =", Z(sol.rhs - yu*(1-sp.exp(-G0*(1+u)*t))))

print("C7 capture from a conserved free reservoir of density n_f")
print("  theta_eq =", Z(sp.solve(sp.Eq(kc*g*(nf/ns)*(1-th), kr*th), th)[0].subs(kr, a0*kc)))

print("C8 point mass under the law")
r, GN, M = sp.symbols('r G M', positive=True)
gNr = GN*M/r**2; gr = (gNr + sp.sqrt(gNr**2 + 4*a0*gNr))/2; gcr = gr - gNr
print("  lim r->0 of rho_c r =", Z(sp.limit(sp.diff(r**2*gcr, r)/(4*sp.pi*GN*r**2)*r, r, 0)))
print("  M_c/M_b - a0/g at a test point =", sp.N((gcr/gNr - a0/gr).subs({GN:1,M:1,a0:1,r:sp.Rational(7,3)}), 20))

print("SI numbers")
c, Gn, Gyr, Mpc, Msun = 2.99792458e8, 6.67430e-11, 3.15576e16, 3.0856775814913673e22, 1.98892e30
for name, A in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    k = A/c
    print(f" [{name}] a0/c = {k:.4e} /s = {k/(67.4e3/Mpc):.3f} H0(67.4); c/a0 = {c/A/Gyr:.1f} Gyr;"
          f" rho_DE implied = {(2*k)**2/Gn:.4e} kg/m^3")
    for age in (13.8, 3.0):
        print(f"   reached after {age} Gyr at u = 0.01, 0.1, 1, 10, 100: " +
              ", ".join(f"{1-math.exp(-age*Gyr*k*(1+uu)):.3f}" for uu in (0.01, 0.1, 1, 10, 100)))
        print(f"   speed-up for 95% at u -> 0 in {age} Gyr: x{3/(age*Gyr*k):.0f}")
    print(f"   speed-up for rate(1+u) = 10 x a bar's 1/(30 Myr), at u = 1: x{10/(0.03*Gyr*k*2):.0f}")
    print(f"   cap a0 r^2/G: {A*(0.1*Mpc)**2/Gn/Msun:.3e} Msun at 100 kpc, {A*Mpc**2/Gn/Msun:.3e} Msun at 1 Mpc;"
          f" column a0/(2 pi G) = {A/(2*math.pi*Gn)/Msun*(Mpc/1e6)**2:.1f} Msun/pc^2")
print(" kappa if the release rate (capture g/c) were: H_L %.4f, H_L/2pi %.4f, sqrt(4 pi G rho) %.4f,"
      " 1/t_ff %.4f, sqrt(4 pi G rho)/2pi %.4f, sqrt(G rho) 1" % (math.sqrt(8*math.pi/3),
      math.sqrt(8*math.pi/3)/(2*math.pi), math.sqrt(4*math.pi), math.sqrt(32/(3*math.pi)), math.sqrt(4*math.pi)/(2*math.pi)))
print(" law: M_c/M_b = a0/g = 5.4 at g = %.3f a0 (g_N = %.4f a0); at g = 0.3, 1, 3 a0 it is %.2f, %.2f, %.2f"
      % (1/5.4, (1/5.4)**2/(1+1/5.4), 1/0.3, 1.0, 1/3))
print(" H(z=2)/H0 for Omega_m 0.315: %.2f ; (1+z)^3 at z=2: %d" % (math.sqrt(0.315*27+0.685), 27))
```

Output:

```
C1 rate balance
  theta_eq = g*k_c/(g*k_c + k_r)
  g_c - a0 g/(g+a0) = 0 | g_N - g^2/(g+a0) = 0
  1/g_c - 1/g - 1/a0 = 0 | g_c/g - a0/(g+a0) = 0
  g_N/g - g_c/a0 = 0 | g_c^2 - g_N(a0-g_c) = 0
C2 capacity C and half-filling field s kept apart
  g_N = g*(-C/s + 1) + C*g**2/s**2 + O(g**3)
C3 Legendre pair
  J' - y = 0 | W' - u = 0 | W + J - u y = 0 | J - int y du = 0
C4 the two-state site's own thermodynamics (units kT per site)
  z dlnxi/dz - z/(1+z) = 0
  J(z) - lnxi = z - 2*log(z + 1) | J(z) - (z - lnxi) = 0
  exp(df/dy) - y/(1-y) = 0  (conjugate of y is ln u, not u)
  p_lattice + ln(1-y) = 0 | W - (p_lattice - y) = 0
  W - f at y=1/2 = 0.886294  (W is not the site free energy)
C5 which responses have W = pressure - ideal pressure?
   Eq(z(x), -x*exp(C1)/(x*exp(C1) - 1))
C6 relaxation from empty
  theta(t) - y(1-exp(-Gamma0(1+u)t)) = 0
C7 capture from a conserved free reservoir of density n_f
  theta_eq = g*n_f/(a0*n_star + g*n_f)
C8 point mass under the law
  lim r->0 of rho_c r = a0/(2*pi*G)
  M_c/M_b - a0/g at a test point = 0.e-138
SI numbers
 [canonical] a0/c = 3.1223e-19 /s = 0.143 H0(67.4); c/a0 = 101.5 Gyr; rho_DE implied = 5.8424e-27 kg/m^3
   reached after 13.8 Gyr at u = 0.01, 0.1, 1, 10, 100: 0.128, 0.139, 0.238, 0.776, 1.000
   speed-up for 95% at u -> 0 in 13.8 Gyr: x22
   reached after 3.0 Gyr at u = 0.01, 0.1, 1, 10, 100: 0.029, 0.032, 0.057, 0.278, 0.949
   speed-up for 95% at u -> 0 in 3.0 Gyr: x101
   speed-up for rate(1+u) = 10 x a bar's 1/(30 Myr), at u = 1: x16915
   cap a0 r^2/G: 6.714e+12 Msun at 100 kpc, 6.714e+14 Msun at 1 Mpc; column a0/(2 pi G) = 106.9 Msun/pc^2
 [alt] a0/c = 3.7733e-19 /s = 0.173 H0(67.4); c/a0 = 84.0 Gyr; rho_DE implied = 8.5328e-27 kg/m^3
   reached after 13.8 Gyr at u = 0.01, 0.1, 1, 10, 100: 0.153, 0.165, 0.280, 0.836, 1.000
   speed-up for 95% at u -> 0 in 13.8 Gyr: x18
   reached after 3.0 Gyr at u = 0.01, 0.1, 1, 10, 100: 0.035, 0.039, 0.069, 0.325, 0.973
   speed-up for 95% at u -> 0 in 3.0 Gyr: x84
   speed-up for rate(1+u) = 10 x a bar's 1/(30 Myr), at u = 1: x13997
   cap a0 r^2/G: 8.114e+12 Msun at 100 kpc, 8.114e+14 Msun at 1 Mpc; column a0/(2 pi G) = 129.1 Msun/pc^2
 kappa if the release rate (capture g/c) were: H_L 2.8944, H_L/2pi 0.4607, sqrt(4 pi G rho) 3.5449, 1/t_ff 1.8426, sqrt(4 pi G rho)/2pi 0.5642, sqrt(G rho) 1
 law: M_c/M_b = a0/g = 5.4 at g = 0.185 a0 (g_N = 0.0289 a0); at g = 0.3, 1, 3 a0 it is 3.33, 1.00, 0.33
 H(z=2)/H0 for Omega_m 0.315: 3.03 ; (1+z)^3 at z=2: 27
```

Reading the less obvious lines:

- C2: with capacity C and half-filling field s kept apart, g_N starts as g (1 - C / s). The law's weak-field limit
  needs C = s exactly. Below that the weak field is Newtonian with a larger G; above it g_N is negative.
- C4, first pair: J is not the site's grand potential; it is z minus it.
- C5: the solution is z / (1 + z) = const times theta. Only the two-state response has W = pressure - ideal pressure.
- C8: the column a0 / (2 pi G) is 106.9 / 129.1 Msun/pc^2, the record's Sigma_M (107 / 129). A cross-check on units.
- The kappa row reproduces VR1's list (2.894, 3.545, 1.843, 0.564, 0.4607) from the rate side.

## 5. What it fixes and what it leaves free

Fixes, inside its own class only:

- The interpolation. One occupant per cell, capture first order in g, and a weak-field limit that exists: together
  these force x / (1 + x) with no free exponent. The record has this (A63 K15, K26; AG6B "A1 forces p = 1").
- The class is a choice. AG6B found two other natural media, the quadrature (n = 2) and exponential cells, that also
  pass raw SPARC. Its label: "physics does not pick n".

Leaves free:

- **kappa.** a0 = k_r / k_c is a ratio. With capture at g / c, kappa = 1/2 needs a release rate of exactly
  (1/2) sqrt(G rho_DE). No rate that gravity builds from rho_DE has that coefficient (row above; every one carries
  pi). A degeneracy of 2 for the full state would supply a factor 1/2, but only on top of a base rate sqrt(G rho_DE)
  with coefficient exactly 1, which is VR1's known posit: a restatement.
- **The absolute rate.** Statics fix only the ratio. Step 10 needs it at least 18 to 101 times a0 / c.
- **The equality C = s** (P4). Put in.
- **The site density and the unit each cell carries.** Only their product, a0, enters.
- **What the sites are, what powers the cycle, and which frame the rates are counted in.**
- **The Solar System.** The model as stated is unscreened. The record's stiffness term is not part of it.

## 6. Predictions: clusters, the CMB, a0(z)

**Clusters.** The model gives the plain law and nothing else.

- The law's cold mass is M_c / M_b = a0 / g. It reaches the record's 5.4 only where g = 0.185 a0. At g = a0 it is
  1.0; at 3 a0 it is 0.33.
- The cap is hard: K |P| cannot exceed a0, so the cold mass inside r is at most a0 r^2 / G: 6.7e12 / 8.1e12 Msun
  inside 100 kpc, 6.7e14 / 8.1e14 inside 1 Mpc. Waiting does not help. Saturation is the model.
- The record's number for the plain law on X-COP is +0.4675 / +0.4345 dex short (QX2; QX29 rule A).
- "Acting as ordinary cold mass": no. The bound density has no inertia. In a merger it follows the baryons'
  present field (fast limit) or stays behind and fades (slow limit). Neither moves with the galaxies. Not computed.

**The CMB.** The model gives nothing.

- In the smooth background g = 0, so theta = 0, P = 0, rho_c = 0 and J = 0. The site medium adds no density and no
  pressure. The cold dust the CMB needs is not in it.
- In perturbations the bound density is the divergence of a vector capped at a0 / K. Its pull is bounded by about
  a0. It has no density of its own to grow as dust. Hand-level; not graded.
- So a separate dust term is needed. Then there are two things. They are one component only if one conserved charge
  ties them, and that is the record's action, with its open joint (CLOSURE.md), not the statistics.

**a0(z).** The model gives a0(z) = k_r(z) / k_c(z) and stops.

- The owner's a0 proportional to sqrt(rho_DE(z)) is P5. It is put in.
- An equally natural reading of "a rate of 0.14 H0" is release by expansion, k_r proportional to H(z). Then a0 is
  3.03 times larger at redshift 2.
- With capture from the free cold component (C7) and its density at the cosmic mean, a0 is 27 times smaller at
  redshift 2.
- These three differ by large factors. The record's high-redshift rotation curves could tell them apart. Not
  graded here.
- Whatever a0(t) is, the filling follows it only if the rate is far above H. At a0 / c it is not.

## 7. What the record already says

Searched README.md and RESULT.md under closure_2026_11_0*, rebuild_2026_10_22 and fable52_push, and
qwen_38_experiment/KAPPA_LEDGER.md, for Langmuir, Michaelis, occupancy, two-state, grand canonical, detailed balance,
capture rate, release rate, saturation, Verlinde. In those folders the only direct hit is NQ1's census. The idea
itself sits in three earlier pushes, found by a wider grep.

| Where | What it found |
|---|---|
| `deepseek_push/DS_FINAL_2026_10_21/A2_medium/report.md` | The law "is the stationary condition of a lattice of independent bistable gates", capture linear in the total g, capacity and affinity both a0. Exact. It "does not derive a0", which is "consumed twice"; it "does not supply a Hamiltonian"; W is not an equilibrium free energy. No Gibbs state with a field-linear coupling gives the response |
| `.../A35_series_parallel/report.md` | 1 / A = 1 / g + 1 / a0 read as two compliances in series |
| `.../A63_saturating_medium/report.md` | Mass action and grand canonical give the same form. One occupant, linear capture and an activity drive are each forced. "Identifies the class, not the material." Status CONDITIONAL on those three |
| `campaign_fresh_gravity/CFG695_saturating_vacuum/README.md` | Saturating vacuum PASSES raw SPARC (0.1009 / 0.0994 dex). "R0-SHAPED": "saturation is a postulate chosen to give a law shape". Post hoc |
| `argon_push/AG6A_vacuum_capacity_factor/README.md` | SCOPED NO-GO: "a capacity can explain that the polarization saturates. It cannot explain where." kappa stays fitted |
| `argon_push/AG6B_saturating_vacuum_microphysics/README.md` | CANDIDATE: "physics does not pick n". Langmuir cells give n = 1; the pump proportional to g is "not derived"; both horizon-tied versions fail SPARC; relaxation proportional to 1 + x with a free rate, "no data path now". "Not a derivation" |
| `rebuild_2026_10_22/NQ1_near_miss_census` (D1_skew_preflight) | The occupancy-noise test of the site picture: SCOPED NO-GO on any rotation-curve data |
| `closure_2026_11_08/VR1_vacuum_response_identity/RESULT.md` | NO IDENTITY: no premise forces kappa = 1/2 except the known posit; every natural length carries pi |
| `closure_2026_11_06/QX29_dipolar_medium/README.md` | A polarizable medium with this same W, plus cold dust under five host rules: FAILS at Cassini on every rule (unscreened), fails its own dipole-continuum gate, X-COP +0.467 / +0.434 with weak clustering |
| `two_state_mechanism_2026_10_24/README.md` | A different two-state model (tethered and free cold mass, thermal selector): the common-gap selector fails |
| `campaign_fresh_gravity/CFG117_verlinde`, `rebuild_2026_10_22/KA1_any_value_screen` | Verlinde: profile gate 0 of 16; "clears 1 of 5 gates, DEAD". Sites placed on surfaces around the mass, instead of in the volume, are that family |
| `closure_2026_11_08/SA1_settling_age_cold_component/REDUCTION.md`; PD1, PD2 | Capture of the cold component by galaxies, by age or as the halo itself: every route closed, FAIL / FAIL |
| `qwen_38_experiment/KAPPA_LEDGER.md` T004 | Response-function scan: no Boltzmann, Wigner or Gaussian-linear response gives an untuned 1/2 (ungraded) |
| `fable52_push/FB1_form_b_from_the_action/NOTE.md` | The force-balance identity holds for any J: "not evidence that this J is the right one" |

What this note adds to that record: the count in section 2; the time to equilibrium at the rate a0 / c (step 10);
the conservation fork (step 9, C7); the statement that the site medium is absent from the smooth universe; and the
pressure dictionary for W and J (step 7), which is an identity and no more.

## 8. The weakest step

**What is captured (P6 with P2).** For the law to come out, the supply must be unlimited and the capture rate must
not depend on how much free cold component is nearby. Then what fills the cells is not the conserved cold component,
the bound density averages to zero over the universe, and "counted once" is lost: the model describes the law with no
end, with no cosmic abundance, no cap, no dust and no inertia. If instead the cells capture the conserved component,
a0 varies with the free density and the law is lost. I found no reading that keeps both.

Second: P5 as a rate. With release at a0 / c the state the derivation rests on is not reached in the age of the
universe below about 10 a0.

Third: P4 and P2 are the law's shape stated as two assumptions. Neither has a reason behind it.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
