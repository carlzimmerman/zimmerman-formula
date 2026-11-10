DOES NOT GO THROUGH

# Route B: horizon lengths (2026-11-10)

One of four parallel attempts to derive the law's shape. A note with checks, not a graded lane: no criteria, no label.
Nothing was committed, pushed or edited. Not registered. Footings never pooled.

**Answer.** I could not derive "horizon distances add" from any horizon or vacuum argument. The known arguments give
other functions (section 3). What is left is an exact re-description of the law: one Rindler frame and one fixed length.
Its third postulate is the law itself. So this is a re-description, not a derivation. It fixes no coefficient.

Symbols: g total field, g_N baryons' Newtonian field, g_c = g - g_N the cold component's pull, u = g/a0,
L_g = c^2/g, L_c = c^2/g_c, L_0 = c^2/a0, K = 4 pi G, ell = c/H the de Sitter radius of a density (H^2 = 8 pi G rho/3).

## 1. The postulates

The set that gives the law exactly:

- **P1 (Rindler).** A static element where the total field is g is given the uniformly accelerated frame of that
  field. The frame's horizon lies L_g = c^2/g behind the element, on the side of the source.
- **P2 (one length).** Dark energy supplies one fixed length, L_0 = c^2/a0 = c / (kappa sqrt(G rho_DE)). kappa is an
  input.
- **P3 (rigid displacement).** The cold component's pull at the element is the acceleration of that same frame at the
  point a rigid length L_0 farther from the horizon.
- **P4 (only for counting and lensing, not for the shape).** That pull is the gravity of a real density.

Arguments I tried in place of P3, hoping one would force it: (D1) the Unruh-de Sitter temperature; (D2) the true horizon
distances of an accelerated observer in de Sitter space; (D3) a first-law ("series") rule for two horizons; (D4) the
dark-energy medium's own response to the frame. None gives P3. Section 3.

## 2. The derivation from P1 to P3, every step

1. The frame of P1 has lapse N(h) = 1 + g h / c^2, with h the proper height along the frame's acceleration (away from
   the source). N = 0 at h = -c^2/g: the horizon is L_g behind. This is special relativity.
2. The acceleration of the frame's worldline at height h is A(h) = c^2 d ln N / dh = g / (1 + g h / c^2)
   = c^2 / (L_g + h) (check A5). A point h higher is exactly h farther from the horizon.
3. P3 puts the cold component at h = L_0: g_c = c^2 / (L_g + L_0). So L_c = L_g + L_0, and 1/g_c = 1/g + 1/a0
   (checks A1, A2, A6).
4. g_N = g - g_c = g^2 / (g + a0). That is the law.

**Step 3 is where the answer goes in.** Steps 1, 2 and 4 are identities. "Add L_0" is P3, and P3 is what was to be
derived.

What the same picture says, all exact (block A of the checks):

- g_c / g = N(0) / N(L_0) = 1 / (1 + u). The cold share of the field is the frame's redshift factor across L_0. The
  baryons' share is the rest.
- g_c / g_N = L_g / L_0 = a0 / g. In a round system the enclosed cold mass over the enclosed baryon mass is the
  horizon distance over the fixed length.
- dg_c/dg = [N(0) / N(L_0)]^2.
- The pressure of the record's point-mass halo is J = (a0^2 / K) [g L_0 / c^2 - ln N(L_0)]: the uniform-field
  potential drop across L_0 minus the frame's exact one. The action's W is (a0^2 / K) [ln(L_c / L_g) - L_0 / L_c].
- g_c g = a0 g_N. Verlinde's point-mass relation is g_D^2 = a_M g_B. The law is that relation with one factor of the
  cold pull replaced by the total field.
- The deep limit alone is additivity to first order: any law with the deep limit has
  L_c = L_g + L_0 + O(L_0^2 / L_g). The law is the case where the first order is exact. Among power means
  L_c = (L_g^n + L_0^n)^(1/n) only n = 1 has the deep limit (block D). n = 2, lengths in quadrature, is the
  field-limited Born-Infeld branch that AG6B already failed (g_N goes as g^3).

## 3. What the stated horizon arguments give instead

**D1. Unruh-de Sitter temperature.** A static-patch observer with acceleration a sees
T = (hbar / 2 pi k c) sqrt(a^2 + a_d^2), a_d = c^2 / ell = c H (check B1; literature: Narnhofer, Peter and Thirring;
Deser and Levin; quoted from memory). Accelerations add in quadrature. The effective horizon is nearer than the
Rindler one, never farther. A law needs one more rule. Milgrom's (1999) is that the Newtonian pull is the excess,
g_N = sqrt(g^2 + a_d^2) - a_d. That is mu(x) = sqrt(1 + 1/(4 x^2)) - 1/(2 x) with a0 = 2 a_d, or g^2 = g_N^2 + g_N a0.
Against the law, at the same a0, over u = 0.01 to 100 (block E):

- mu differs by at most 0.1216 (at u = 1.31); the ratio peaks at 1.2500 (u = 0.667); at u = 1 it is 0.618 against 0.500.
- At fixed g_N the total field differs by at most 0.0625 dex (at g_N = 0.5 a0); 0.0378 dex after the best rescaling
  of a0 (times 1.20). AG6B quotes at most 0.031 dex on its own range.
- The cold pull saturates at a0/2, not a0. Half the column density.
- In lengths: the added length is not constant. It runs from L_0 (u small) to 2 L_0 (u large).
- Its scale is a0 = 2 c H: kappa = 5.79. The record has this excluded (15.6 sigma in the ledger; AG6B E-2 fails SPARC).

**D2. True horizon distances in de Sitter space.** For the same observer the nearer horizon is at proper distance
ell arccot(a ell / c^2), which is less than c^2/a. The farther one is at pi ell minus that. **The sum is pi ell for
every acceleration** (B2 to B4). De Sitter space keeps the sum of the two distances fixed. The law needs the opposite:
one distance fixed at L_0 and the sum growing as L_g + L_0. Used as a rule (g_N = c^2/d(g) - c^2/d(0)), the true
distance has no deep regime at all: g_N / g tends to 4/pi^2 = 0.405 (E5).

**D3. A first-law rule.** A horizon distance is an inverse temperature, so L_c = L_g + L_0 reads
1/T_c = 1/T_g + 1/T_0: the entropy cost of a unit of the cold component's energy is counted on both horizons, with a
plus sign. I found no argument for that. In de Sitter space, energy placed inside the cosmological horizon lowers that
horizon's entropy (Gibbons and Hawking; it is the entropy displacement Verlinde starts from; from memory, not checked
here). With that sign the rule reads 1/g_c = 1/g - 1/a0, which is not the law.

**D4. The medium's response to the frame.** The record did this in VR1: the clock's kinetic density goes as N^-2, so
its response length is c^2 / (2 |A|). The gravitating response is at most 4 rho_DE |Phi| / c^2: 6.9e-8 of the X-COP
need and 7.7e-14 of the CMB need. It tracks depth. It gives no law.

**P1 itself.** A static element in a galaxy's field has no horizon at c^2/g. The Rindler frame is a local picture,
good over lengths much shorter than sqrt(L_g r). At g = a0 and r = 10 kpc the horizon is 1,600 to 1,800 times farther
than that (F3). In the deep regime, where the law matters most, L_g is many times L_0, and L_0 is already 5.79 de Sitter
radii.

## 4. Checks

Python 3 with sympy and numpy, one file, a few seconds. Code as run:

```python
import sympy as sp, numpy as np
g, a0, c, h, K, a, ell, ad, x = sp.symbols('g a0 c h K a ell a_d x', positive=True)
Z = lambda e: sp.simplify(sp.expand_log(sp.simplify(e), force=True))

print("A. the law in horizon lengths (each line must print 0)")
gN = g**2/(g + a0); gc = sp.simplify(g - gN)
Lg, L0, Lc = c**2/g, c**2/a0, c**2/gc
N = 1 + g*h/c**2                              # Rindler lapse built on g at h = 0
A = sp.simplify(c**2*sp.diff(sp.log(N), h))   # acceleration of the frame at height h
J = (a0**2/K)*(g/a0 - sp.log(1 + g/a0))
W = (a0**2/K)*(-gc/a0 - sp.log(1 - gc/a0))
for name, e in [("A1 1/g_c - 1/g - 1/a0", 1/gc - 1/g - 1/a0), ("A2 L_c - L_g - L_0", Lc - Lg - L0),
                ("A3 g_c g - a0 g_N", gc*g - a0*gN), ("A4 g_c/g_N - L_g/L_0", gc/gN - Lg/L0),
                ("A5 A(h) - c^2/(L_g + h)", A - c**2/(Lg + h)), ("A6 A(L_0) - g_c", A.subs(h, L0) - gc),
                ("A7 g_c/g - N(0)/N(L_0)", gc/g - 1/N.subs(h, L0)),
                ("A8 dg_c/dg - [N(0)/N(L_0)]^2", sp.diff(gc, g) - 1/N.subs(h, L0)**2),
                ("A9 J - (a0/(K L_0)) Int_0^L0 [g - A(h)] dh", (a0/(K*L0))*sp.integrate(g - A, (h, 0, L0)) - J),
                ("A10 W - (a0^2/K)[ln(L_c/L_g) - L_0/L_c]", W - (a0**2/K)*(sp.log(Lc/Lg) - L0/Lc))]:
    print("  %-46s = %s" % (name, Z(e)))

print("B. de Sitter static patch, c = 1, radius ell")
r = sp.symbols('r', positive=True); f = 1 - r**2/ell**2
acc = sp.simplify(-sp.diff(f, r)/(2*sp.sqrt(f)))
print("  B1 (2 pi T_local)^2 - (a^2 + 1/ell^2)          =", sp.simplify(1/(ell**2*f) - acc**2 - 1/ell**2))
dn, df = ell*(sp.pi/2 - sp.atan(a*ell)), ell*(sp.pi/2 + sp.atan(a*ell))   # a ell = tan(chi), r = ell sin(chi)
print("  B2 near + far horizon distance                 =", sp.simplify(dn + df))
print("  B3 near distance, a large                      =", sp.series(dn, a, sp.oo, 4))
print("  B4 near distance, a -> 0                       =", sp.limit(dn, a, 0))

print("C. Unruh-de Sitter: g_N = sqrt(g^2 + a_d^2) - a_d")
gNU = sp.sqrt(g**2 + ad**2) - ad
print("  C1 deep limit                                  =", sp.series(gNU, g, 0, 5))
gcU = g - gNU.subs(ad, a0/2)                  # deep limit matched to the law: a_d = a0/2
print("  C2 cold pull as g -> infinity                  =", sp.limit(gcU, g, sp.oo))
add = sp.simplify(((c**2/gcU - Lg)/L0).subs(g, x*a0))
print("  C3 added length / L_0 at u -> 0, u -> infinity =", sp.limit(add, x, 0), ",", sp.limit(add, x, sp.oo))
print("D. power means L_c = (L_g^n + L_0^n)^(1/n): mu at small u =",
      [sp.series(1 - (1 + x**n)**sp.Rational(-1, n), x, 0, n + 1).removeO() for n in (1, 2, 3)])

print("E. numbers, u = g/a0 from 0.01 to 100 (4001 log-spaced points)")
u = np.logspace(-2, 2, 4001); ml = u/(1 + u); mU = np.sqrt(1 + 1/(4*u*u)) - 1/(2*u)
i, j = np.argmax(abs(mU - ml)), np.argmax(mU/ml)
print("  E1 max |mu_UdS - mu_law| = %.4f at u = %.3f ; max mu_UdS/mu_law = %.4f at u = %.3f" % (abs(mU - ml)[i], u[i], (mU/ml)[j], u[j]))
y = u*u/(1 + u); nl = (1 + np.sqrt(1 + 4/y))/2; d = np.log10(np.sqrt(1 + 1/y)/nl); m = np.argmax(abs(d))
print("  E2 same a0, same g_N: max |log10(g_UdS/g_law)| = %.4f dex at g_N/a0 = %.3f" % (abs(d[m]), y[m]))
s = min(np.linspace(0.3, 3, 2701), key=lambda s: np.max(abs(np.log10(np.sqrt(1 + s/y)/nl))))
print("  E3 best rescale of the Unruh-dS a0: x %.3f, max %.4f dex" % (s, np.max(abs(np.log10(np.sqrt(1 + s/y)/nl)))))
print("  E4    u    mu_law  mu_UdS  g_c/a0 law  g_c/a0 UdS  added length/L_0: law  UdS")
for U in (0.01, 0.1, 0.3, 1, 3, 10, 100):
    a_, b_ = U/(1 + U), np.sqrt(1 + 1/(4*U*U)) - 1/(2*U)
    print("     %6.2f  %.4f  %.4f  %.4f      %.4f      %.4f                 %.4f" % (U, a_, b_, U*(1 - a_), U*(1 - b_), 1/(U*(1 - a_)) - 1/U, 1/(U*(1 - b_)) - 1/U))
xs = np.array([1e-3, 1e-2, 0.1, 1, 10, 100])
print("  E5 distance rule g_N = c^2/d_near(g) - c^2/d_near(0): g_N/g at g/a_d =", xs, "->", np.round((1/np.arctan(1/xs) - 2/np.pi)/xs, 4), "(4/pi^2 = %.4f)" % (4/np.pi**2))

print("F. the coefficient: a0 = kappa c sqrt(G rho), ell = c/H, H^2 = 8 pi G rho/3")
k0 = np.sqrt(8*np.pi/3)
print("  F1 kappa for L_0 = ell, pi ell/2, pi ell, 6 ell, 2 pi ell = " + ", ".join("%.4f" % (k0/q) for q in (1, np.pi/2, np.pi, 6, 2*np.pi)))
print("  F2 kappa = 1/2 needs L_0/ell = %.4f" % (2*k0))
for nm, A0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    L = 299792458.0**2/A0
    print("  F3 %-9s L_0 = %.4e m = %.2f Gpc ; at g = a0, r = 10 kpc: L_g/r = %.2e, sqrt(L_g/r) = %.0f" % (nm, L, L/3.0857e25, L/3.0857e20, np.sqrt(L/3.0857e20)))
print("G. law (g_c g = a0 g_N) against Verlinde's point mass (g_D^2 = a_M g_B), same deep normalisation")
for Y in (0.01, 1, 100, 1e8):
    print("  g_N/a0 = %8.2e : g_c/a0 law = %.4f ; g_D/a0 Verlinde = %.4g" % (Y, (-Y + np.sqrt(Y*Y + 4*Y))/2, np.sqrt(Y)))
```

Output:

```
A. the law in horizon lengths (each line must print 0)
  A1 1/g_c - 1/g - 1/a0                          = 0
  A2 L_c - L_g - L_0                             = 0
  A3 g_c g - a0 g_N                              = 0
  A4 g_c/g_N - L_g/L_0                           = 0
  A5 A(h) - c^2/(L_g + h)                        = 0
  A6 A(L_0) - g_c                                = 0
  A7 g_c/g - N(0)/N(L_0)                         = 0
  A8 dg_c/dg - [N(0)/N(L_0)]^2                   = 0
  A9 J - (a0/(K L_0)) Int_0^L0 [g - A(h)] dh     = 0
  A10 W - (a0^2/K)[ln(L_c/L_g) - L_0/L_c]        = 0
B. de Sitter static patch, c = 1, radius ell
  B1 (2 pi T_local)^2 - (a^2 + 1/ell^2)          = 0
  B2 near + far horizon distance                 = pi*ell
  B3 near distance, a large                      = -1/(3*a**3*ell**2) + 1/a + O(a**(-4), (a, oo))
  B4 near distance, a -> 0                       = pi*ell/2
C. Unruh-de Sitter: g_N = sqrt(g^2 + a_d^2) - a_d
  C1 deep limit                                  = -g**4/(8*a_d**3) + g**2/(2*a_d) + O(g**5)
  C2 cold pull as g -> infinity                  = a0/2
  C3 added length / L_0 at u -> 0, u -> infinity = 1 , 2
D. power means L_c = (L_g^n + L_0^n)^(1/n): mu at small u = [x, x**2/2, x**3/3]
E. numbers, u = g/a0 from 0.01 to 100 (4001 log-spaced points)
  E1 max |mu_UdS - mu_law| = 0.1216 at u = 1.312 ; max mu_UdS/mu_law = 1.2500 at u = 0.667
  E2 same a0, same g_N: max |log10(g_UdS/g_law)| = 0.0625 dex at g_N/a0 = 0.500
  E3 best rescale of the Unruh-dS a0: x 1.201, max 0.0378 dex
  E4    u    mu_law  mu_UdS  g_c/a0 law  g_c/a0 UdS  added length/L_0: law  UdS
       0.01  0.0099  0.0100  0.0099      0.0099      1.0000                 1.0100
       0.10  0.0909  0.0990  0.0909      0.0901      1.0000                 1.0990
       0.30  0.2308  0.2770  0.2308      0.2169      1.0000                 1.2770
       1.00  0.5000  0.6180  0.5000      0.3820      1.0000                 1.6180
       3.00  0.7500  0.8471  0.7500      0.4586      1.0000                 1.8471
      10.00  0.9091  0.9512  0.9091      0.4875      1.0000                 1.9512
     100.00  0.9901  0.9950  0.9901      0.4988      1.0000                 1.9950
  E5 distance rule g_N = c^2/d_near(g) - c^2/d_near(0): g_N/g at g/a_d = [1.e-03 1.e-02 1.e-01 1.e+00 1.e+01 1.e+02] -> [0.4055 0.4079 0.4313 0.6366 0.9397 0.9937] (4/pi^2 = 0.4053)
F. the coefficient: a0 = kappa c sqrt(G rho), ell = c/H, H^2 = 8 pi G rho/3
  F1 kappa for L_0 = ell, pi ell/2, pi ell, 6 ell, 2 pi ell = 2.8944, 1.8426, 0.9213, 0.4824, 0.4607
  F2 kappa = 1/2 needs L_0/ell = 5.7888
  F3 canonical L_0 = 9.6018e+26 m = 31.12 Gpc ; at g = a0, r = 10 kpc: L_g/r = 3.11e+06, sqrt(L_g/r) = 1764
  F3 alt       L_0 = 7.9451e+26 m = 25.75 Gpc ; at g = a0, r = 10 kpc: L_g/r = 2.57e+06, sqrt(L_g/r) = 1605
G. law (g_c g = a0 g_N) against Verlinde's point mass (g_D^2 = a_M g_B), same deep normalisation
  g_N/a0 = 1.00e-02 : g_c/a0 law = 0.0951 ; g_D/a0 Verlinde = 0.1
  g_N/a0 = 1.00e+00 : g_c/a0 law = 0.6180 ; g_D/a0 Verlinde = 1
  g_N/a0 = 1.00e+02 : g_c/a0 law = 0.9902 ; g_D/a0 Verlinde = 10
  g_N/a0 = 1.00e+08 : g_c/a0 law = 1.0000 ; g_D/a0 Verlinde = 1e+04
```

B2 uses the map a ell = tan(chi), r = ell sin(chi), done by hand; the code checks the sum and the limits, not the map.

## 5. What it fixes and what it leaves free

Given P3 (that is, given the law): the shape x/(1+x) exactly; the cap a0 on the cold pull; the column density
a0 / (2 pi G); the pressure J.

It does **not** fix kappa. L_0 is an input. The lengths de Sitter space offers give (F1): ell, 2.894 (a0 = c H);
pi ell / 2, the true distance to the horizon, 1.843; pi ell, horizon to horizon, 0.921; 2 pi ell, the thermal
wavelength, 0.4607 (Milgrom's c H / 2 pi). Verlinde's c H / 6 is 0.4824. kappa = 1/2 needs L_0 = 5.7888 ell, which is
none of them: it is the record's pi-free length c / sqrt(G rho) (VR1, KF1: "xi = 1"). KA1 already says 0.461, 0.482
and 0.5 cannot be told apart today and none is forced. Nothing here changes that.

Left free: whether the pull is a real density (P4); how a halo gets into this state (COL1, FLD1); screening (the pull
tends to a0 at high g, so the Solar System still needs the action's stiffness; unscreened it is QX29's G8 failure);
discs and any non-round geometry (P3 speaks of magnitudes along g only); all of cosmology.

## 6. Predictions

- **Clusters.** Nothing beyond the plain law. Enclosed cold over baryons is a0 / g (A4), and the pull is capped at a0.
  A ratio of 5.4 would need g = a0 / 5.4 at every radius. The record's number for the plain law stands: X-COP is
  +0.4675 / +0.4345 dex short. The route supplies no ordinary cold mass. It fails here as the plain law fails.
- **CMB.** Nothing. The mean universe has no static frame and no g: L_g is infinite and g_c = 0. The route gives no
  cold dust at z 1100, where the record needs 5.41 times the baryons. It has no equation of motion, so it cannot say
  how dust becomes this state. That is the record's missing joint (CLOSURE), untouched.
- **Lensing.** P1 to P3 do not say. A7 is a statement about clock rates only. With P4 added, light sees the pull, as in
  the action (QX17: the halo is the sector's own gravitating density). Without P4 the argument is modified inertia
  (Milgrom 1999, McCulloch), where light sees the baryons only: the record has that excluded by galaxy lensing at
  21 sigma, and at 2 to 5 % of the measured CMB lensing (WG5).
- **a0(z).** It depends on what L_0 is, and the route does not choose.
  (i) A length of the medium's density: a0(z) = kappa c sqrt(G rho_DE(z)), the owner's relation, put in, not predicted.
  For constant w it goes as (1+z)^(3(1+w)/2). Then L_0 is not a horizon distance.
  (ii) The Hubble radius: a0 goes as H(z) and rises with z. The record has that failed (KA1 row K017; McCulloch in the
  literature map; the H(z) reading in the Verlinde run).
  (iii) The event horizon: it depends on the whole future. If dark energy decays there is no event horizon and no L_0.
  So with dynamical dark energy only (i) is defined at each epoch, and (i) is not a horizon argument.

## 7. Derivation, re-description, or neither; and Verlinde

**A re-description.** Exact, and it adds one picture: the law is Born rigidity across a fixed length. It is not a
derivation, because P3 is the law.

Verlinde starts from an entropy count (matter displaces de Sitter entropy; the medium responds elastically). Granting
his postulates, he gets the deep relation only, with a forced coefficient 1/6 and no interpolation; his cold pull grows
as sqrt(g_N) without a cap (block G: 1e4 a0 where the law gives a0). This route has no entropy count. It gets the full
interpolation and the cap, but only by putting them in, and it forces no coefficient. The two share what the record
held against Verlinde: no action, no field equation, no cosmology, a borrowed scale.

Which gates Verlinde failed, exactly. Rows K425 and K559 are in
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_ATTEMPTS_LEDGER.md` (both kappa 0.482, "DATA-LEVEL
landing"; K425 "chain contested", K559 "not a derivation"). `qwen_38_experiment/KAPPA_LEDGER.md` holds only T001 to
T009; its T001 lists Verlinde among routes that force a coefficient other than 1/2.

- KA1's screen (`rebuild_2026_10_22/KA1_any_value_screen/README.md`), both rows: pass S1 (c), S2 (counterfactual),
  S3 (d), S5; **fail S4** (second prediction: the apparent-mass profile, CFG117 G1 0 of 16, p34 Dchi2 +1389 / +2216);
  S6 (vacuum) and S8 (local) not shown, which counts as not passed.
- K559's own five gates (`qwen_claude_field_theory/closure_2026/route3_entropic_gravity_2026.py`, verdict block; read,
  not re-run): gate 1, amplitude law at the BTFR value, PASS. Gate 2, screening the force, SPLIT and fatal: no cutoff
  fails; his own cutoff sits at y = 3 and the SPARC relation refutes a step there. Gate 3, the Solar System (Q2 and
  the 1 AU monopole), FAIL on both readings. Gate 4, theoretical health, CANNOT BE POSED (no action, no field equation,
  no cosmology; a0(z) wrong on both readings). Gate 5, no double count, VACUOUS PASS, refused. One of five.

## 8. What the record already says (grep of README.md and RESULT.md under closure_2026_11_0*, rebuild_2026_10_22, fable52_push; and the kappa ledgers)

- **Unruh** (4 files). WG5: the framework's first completion was "de Sitter-Unruh modified inertia", nu = sqrt(1 + 1/y);
  closed 2026-08-08; galaxy lensing excludes it at 21 sigma. VR1: NO IDENTITY; its "Unruh root" gives kappa 11.18.
  KF1 R5: equating the Unruh and de Sitter temperatures gives a = c H; the 0.4607 needs the 2 pi kept by hand; not
  forced. CG1: lists the de Sitter-Unruh paper among files with forced-kernel wording.
- **de Sitter** (7 files). KA1: 0.461 is not a coefficient-free value of the de Sitter tie; four rows repeat one
  reading. KF1: the true gradient of the de Sitter potential gives 2.894. KT7: the de Sitter radius gives 1.447 under
  its rule. The other hits (KT3, X1, GAL1) are background uses.
- **horizon** (13 files). KA1: K017 particle horizon 0.55, uses measured cosmology and a0 rises with z; K528 horizon
  coefficient 0.461, takes 1/2 as adopted. KF1: a uniform density makes a horizon at G rho r^2 / c^2 = 3/(8 pi), the
  routes need 1 (door X7). WG5: the framework's lengths are c/H0 (4.4 Gpc) and c^2/a0 (31 Gpc). The rest are sound
  horizon, sub-horizon growth and black-hole hits.
- **Rindler**: no hit in those files. Elsewhere: ledger row K117 ("Rindler disk" postulate, VOID: the postulate is the
  target); `deepseek_push/DS_FINAL_2026_10_21/A37_three_lengths/report.md` already names c^2/a0 as the Rindler-horizon
  distance at a0 (7.00 c/H0, 5.79 de Sitter radii).
- **entropic**: three hits, all the word "isentropic". Entropic gravity appears only as the Verlinde rows above.
- **The series form is already in the record.** `argon_push/AG6B_saturating_vacuum_microphysics/README.md`: the law is
  "two processes in series (1/u = 1/g + 1/a0)"; the quadrature form is the de Sitter-Unruh one; three media pass SPARC;
  "physics does not pick n"; tying the scale to the horizon fails SPARC (a0 = c H: 0.1786 / 0.2053 dex against a line of
  0.110; 2 c H: 0.2665 / 0.3002); "kappa stays fitted". This note's D1 numbers agree with it.
- **Ledgers.** `qwen_38_experiment/KAPPA_LEDGER.md` T001: every published de Sitter thermodynamic route forces a
  coefficient other than 1/2 or none (Milgrom 1999 2 c H, excluded 15.6 sigma; Milgrom c H / 2 pi the nearest, outside
  the window). T008, a two-temperature interpolation, is ungraded. The CFG894 ledger has 99 lines naming Unruh, Rindler,
  horizon, de Sitter or entropic; KA1 screened the register and found NO ROUTE.
- **McCulloch** (`sonnet55_push/puzzle_32pi/agents/E_literature_a0_coefficient/README.md`): 1 - mu = L_g / (Theta/2),
  a0 1.7 times the data, rising a0(z), marked refuted in the literature map. In lengths the law reads
  1 - mu = L_g / (L_g + L_0): the same ratio with the cavity taken as L_g + L_0. That is P3 again, not a derivation.

New here, as far as the grep shows: the de Sitter sum rule (D2), the first-order reading of the deep limit, the
Born-rigid form with J and W as lapse identities, and the relation g_c g = a0 g_N against Verlinde's.

## 9. The weakest step

P3. It is the law restated, and the geometry it borrows contradicts it. In de Sitter space the two horizon distances
sum to a constant; they do not sum to L_g + L_0. At kappa = 1/2 the added length is 5.79 de Sitter radii, longer than
that whole constant (pi radii). The frame of P1 is used out to its horizon, more than a thousand times beyond where it
holds. A real derivation would have to say why the cold component, and not the baryons, sits on the displaced
worldline; why the displacement is the pi-free length c / (kappa sqrt(G rho_DE)); and why additivity stays exact when
L_g is hundreds of L_0. I have none of the three.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
