DOES NOT GO THROUGH

# Route D: the cold component as the clustered part of a dark-energy field, and the column-density reading (2026-11-10)

Neither task gives a derivation.

- **Task 1 (the column): re-description only.** The fraction f is kappa under another name. No argument tried here fixes it.
- **Task 2 (a dark-energy field that clusters): neither a derivation nor a new description.** It reaches the record's
  amounts only when the field is "a constant plus dust", which is the record's cold reference restated with the amount
  put in. With a dark-energy-like equation of state it is short by 19 to 1700. In no case does it give either half of
  the law's shape.

A search note. No criteria, no label, not a lane, not registered. Adopts nothing. Footings never pooled.
kappa = 1/2 FITTED; not theory closed.

## 0. Inputs, and one correction to the brief

- G = 6.67430e-11, c = 2.99792458e8 (SI). H0 = 67.4 km/s/Mpc and Omega_Lambda = 0.6847: the record's canonical pair.
  With kappa = 1/2 they return a0 = 9.3603e-11 on rho_DE (canonical) and 1.1312e-10 on rho_crit (alt), to five digits
  (check C1).
- rho_crit = 8.5329e-27 and rho_DE = 5.8424e-27 kg/m^3. H_Lambda = H0 sqrt(Omega_Lambda). c/H_Lambda = 5375 Mpc.
- Cold share: 5.41 times the baryons (the form B decision table). Then Omega_b = 0.0492 and Omega_c = 0.2661.
- The dark-energy curves used in section 3 are the record's three DESI sets (w0, wa) = (-0.838, -0.62), (-0.752, -0.86),
  (-0.667, -1.09), from `campaign_fresh_gravity/CFG223_a0_over_cosmic_time/`. That lane says they were not re-checked
  against the DESI paper. Neither were they here.
- All of these are the record's numbers and are fitted outside this note. H0, Omega_Lambda and 5.41 come from the rival
  model's fit to the CMB. Nothing below turns on their third digit.
- **Correction.** The brief gives Sigma_0 as "about 140 Msun/pc^2". That is the value for a0 = 1.2e-10. On the two
  footings Sigma_0 = a0/(2 pi G) is 106.9 and 129.2 Msun/pc^2, as the record has it (X47).

## 1. Postulates

- **P0 (the owner's inputs, kept).** The law g_N = g^2/(g + a0). Form B: g = g_N + g_c, so g_c = a0 g/(g + a0).
  a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED.
- **P1.** The dark sector is one field Q, coupled to everything else only through gravity. It has a mean density
  rhobar(t) and a mean pressure pbar(t). It is not a particle.
- **P2.** Its sound speed is zero. In the field's own frame the pressure has no gradient: p = pbar(t) everywhere. Its
  elements move on geodesics.
- **P3.** The cold component is the clustered part of Q: rho_c = rho_Q - rhobar.
- **P4.** a0 follows the field. Two readings: (a) the part that does not cluster, -pbar, which is the same everywhere in
  space by P2; (b) the field's mean density.
- **T1 (the target of task 1, not a postulate).** Sigma_0 = f rho_DE c/H_Lambda, with f a number that an argument fixes.

## 2. Task 1: the column

**2.1 The identity.** H_Lambda^2 = 8 pi G rho_DE/3, so rho_DE c/H_Lambda = c sqrt(3 rho_DE/(8 pi G)). Then

    f = Sigma_0 / (rho_DE c / H_Lambda) = kappa sqrt(2/(3 pi)) = 0.4607 kappa.

At kappa = 1/2, f = 1/sqrt(6 pi) = 0.2303. The same statement in two other forms: a0 = (3/4) f c H_Lambda, and
a0^2/(8 pi G) = (kappa^2/(8 pi)) rho_DE c^2 = rho_DE c^2/(32 pi).

**2.2 On each footing** (check C1).

| | canonical (a0 9.3603e-11) | alt (a0 1.1312e-10) |
|---|---|---|
| Sigma_0 = a0/(2 pi G) | 106.9 Msun/pc^2 | 129.2 Msun/pc^2 |
| over rho_DE c/H_Lambda (464.0 Msun/pc^2) | 0.2303 | 0.2784 |
| over rho_crit c/H0 (560.8 Msun/pc^2) | 0.1906 | 0.2303 |
| rho_DE c^2 over a0^2/(8 pi G) | 100.53 (= 32 pi) | 68.83 |

Each footing returns 0.2303 against its own density and its own Hubble length. That is kappa = 1/2 coming back out. It
is not a measurement of f. For scale: the kappa ledger's own fit (0.551 +- 0.043, `qwen_38_experiment/KAPPA_LEDGER.md`)
would be f = 0.254 +- 0.020. The record's Burkert products (Donato 141, Li+2020 176.8 Msun/pc^2) would be f = 0.30 and
0.38, but those depend on the profile convention by up to 0.69 dex (X47).

**2.3 Why "a fixed fraction" is automatic.** From c, G and rho_DE there is one surface density, c sqrt(rho_DE/G). The
de Sitter radius is built from the same three. So in any theory with a0 proportional to c sqrt(G rho_DE), Sigma_0 is a
pure number times rho_DE c/H_Lambda. T1 has no content beyond that number, and the number is kappa.

**2.4 Five attempts to fix f. None does.**

1. *Clustering by gravity.* A halo of mass M that forms when its fluctuation reaches the collapse threshold has mean
   column proportional to sigma_8^2 M^(-(n+2)/3), for a power-law spectrum of slope n (check C2). It is flat in mass
   only at n = -2. Its size goes as the square of the primordial amplitude. Hand estimate at sigma_8 = 0.812: 4.6
   Msun/pc^2 inside the virial radius, 0.010 of the horizon column (check C5). So in the clustering picture the
   fraction carries the primordial amplitude. Dark energy does not set it.
2. *Pressure balance.* The law's pressure scale is a0^2/(8 pi G) = rho_DE c^2/(32 pi). The natural statement, "the cold
   stress saturates at the dark-energy pressure", gives kappa = sqrt(8 pi) = 5.01. That is ten times too large. The
   record found the same from the two-phase action (W4-24: kappa at least 5.20).
3. *Static response of the field.* A field with sound speed c_s around a mass M holds an excess
   (1 + w) rho_DE G M/(c_s^2 r). That is a 1/r profile, like the law's strong field. But its column goes as M, so it
   is not universal. For c_s = c and 6e10 Msun it is 2.3e-12 (1 + w) of Sigma_0 (check C5). It equals Sigma_0 only for
   a mass whose gravitational radius is 0.23/(1 + w) of the de Sitter radius.
4. *Horizon temperature.* The published routes give other numbers. a0 = c H_Lambda/6 is f = 2/9 = 0.2222 (kappa 0.482).
   a0 = c H_Lambda/(2 pi) is f = 2/(3 pi) = 0.2122 (kappa 0.461). Both are already rows in the record's register and
   neither is forced. The record's data floor on kappa is about 9 %, so data cannot tell 0.2303 from 0.2222 or 0.2122.
5. *The de Sitter ball's own column.* The vacuum inside the horizon, spread over the horizon's area, is rho V/A =
   rho_DE (c/H_Lambda)/3. That is a stated argument with a fixed number: f = 1/3. With the field of a sheet,
   2 pi G Sigma, it gives a0 = c H_Lambda/4 and kappa = 0.724. With both sides, 4 pi G Sigma, kappa = 1.447. Neither
   is 1/2 (check C1; 1.447 is the record's own number for the de Sitter radius). The record listed this route and did
   not run it (CFG264 R5, frozen at 0.1 %); its own note says Gauss's law puts the pi back.

**2.5 What "column" means for this law.** In the strong field g_c tends to a0, and rho_c r tends to a0/(2 pi G)
(check C2). The constant is the product of density and radius. The mean column inside r is a0/(pi G), twice Sigma_0.
The column along a line through the centre is not finite for a point mass: it grows by 2 ln 10 = 4.6 Sigma_0 for each
decade of radius. So "a universal column through the galaxy" should read "a universal density times radius".

**2.6 The weak-field half.** The column statement does not give it. Two more statements do.
(i) Outside the saturated zone the halo is isothermal.
(ii) The joint is where the cold mass a0 r^2/G equals the baryon mass. That is also where the baryon pull equals a0.
Then sigma^2 = a0 r_M/2 = (1/2) sqrt(G M_b a0), the law's value exactly (check C2). Both statements are put in by hand,
and the curve between the two limits stays open. In the action's language the weak-field half is the closure
P = g^2/(8 pi G). With force balance and Poisson's equation that closure gives g proportional to 1/r with any amplitude
(check C2). The amplitude comes from the joint. This is the law in other words, not a derivation of it.

## 3. Task 2: a dark-energy field that clusters

**3.1 Lemma (exact, from P2).** In a region with local expansion rate h, d rho/dt = -3h (rho + pbar). Subtract the
background. With delta rho = rho - rhobar and n = rhobar + pbar = (1 + w) rhobar,

    d(delta rho)/dt + 3h delta rho = -3 (h - H) n.

The clustered part moves like dust. It is fed by n wherever matter contracts faster than the background (check C2).
Integrate over a collapsing region that holds baryon mass M_b:

    M_c / M_b = Integral X(a) (-dv),      X(a) = (1 + w) rhobar_Q / rhobar_b,

where v is the region's comoving volume as a fraction of its starting value. The collapse runs confirm this to five
digits (check C3, "identity"). In the linear matter era it reduces to delta_Q/delta_m = (1 + w)/(1 - 3w).

**Corollary.** The cold mass that gathers is linear in (1 + w). The field clusters exactly as a dust of density
(1 + w) rhobar_Q would. If pbar is constant, n is conserved, and the field is exactly "a constant plus dust" at every
order until streams cross.

**3.2 Amounts** (check C3). Gathered cold mass per baryon mass at virialisation, for collapse at z = 0 and z = 0.5.

| field | z = 0 | z = 0.5 | against the 5.41 the record needs |
|---|---|---|---|
| constant pressure, dust part equal to the cold share (1 + w today = 0.280) | 5.39 | 5.38 | reaches it: the cold reference restated |
| constant pressure, dust part halved; a tenth | 2.70; 0.54 | 2.69; 0.54 | linear in the dust part |
| dust part plus each of the record's three DESI curves | 5.32 | 5.29 to 5.32 | within 2 % of the row above |
| baryons and one fluid, constant w = -0.99 | 0.0060 | 0.0032 | short by 900; 1672 |
| the same, w = -0.95 | 0.032 | 0.018 | short by 168; 306 |
| the same, w = -0.90 | 0.070 | 0.040 | short by 77; 136 |
| the same, w = -0.80 | 0.170 | 0.101 | short by 32; 54 |
| the same, w = -0.20 | 5.39 | 4.33 | reaches it, but the field is then nearly dust, not dark energy |
| a separately counted dust collapses and the fluid rides along, w = -0.99 to -0.80 | 0.011 to 0.29 | not run | short by 492 to 19; form B does not allow the second dust |

- The route reaches the cluster amount only if the field already holds dust of the cosmic amount. Then (1 + w) is not
  small. The field's w is -0.72 today, -0.24 at z = 1 and -0.06 at z = 2.5 (check C4).
- The amount is an initial condition of the field, as it is in the record's own action (n_* in DT1). Nothing fixes it.
- Galaxies. The law's halo holds M_c/M_b = 0.62, 2.54, 9.51 and 59.5 at r = 1, 3, 10 and 60 r_M (check C5). It passes
  the cosmic share at 5.89 r_M, which is 56 / 51 kpc for 6e10 Msun. Beyond that the gathered share covers the law's halo
  only if the galaxy holds a small part of its patch's baryons. That is form B's bookkeeping (PD1's share is 59.5).
  With a dark-energy-like w the gathered mass is 0.006 to 0.17 M_b in all. Against the law's halo at 10 r_M that is
  short by 56 to 1600.

**3.3 Profile.** The lemma gives a mass. It does not give a shape.

- In linear order the cold excess around a compact mass has no profile. The displacement goes as 1/q^2 and has no
  divergence. The excess sits at the centre and grows with the expansion. In a matter era it is of order
  [X/(1 + X)] (3/5) (1 + z_i) M_b: 4 to 5 M_b today for a mass in place at z = 9 (hand level, not run).
- Past linear order a cold single stream falls in. A steady cold inflow has density proportional to r^(-3/2)
  (check C2). At 10 kpc around 6e10 Msun it is 85 / 95 times below the law's halo (hand level, check C5). It reaches
  the centre in a free-fall time and folds. This is COL1 and FLD1 again, reached from the dark-energy side (their
  numbers: advected charge short by 20 to 60; the equations stop at the fold).
- If streams could cross, infall onto a point mass would settle near r^(-9/4) (from memory, not re-derived). A field
  cannot cross its own streams.
- The law needs r^(-1) with a size that does not depend on M_b (strong field), and r^(-2) with a size that goes as
  sqrt(M_b) (weak field). Clustering gives neither. It gives v^3 = 10 G M H0 where the law gives v^4 = G M_b a0. With
  the cosmic share the two meet at one speed only, 669 / 808 km/s (check C5).

**3.4 P2 against the law's state.** In the law's static state the cold component carries the stress
J(g) = (a0^2/(4 pi G)) [u - ln(1 + u)], u = g/a0 (FB1 note). At kappa = 1/2 that is (rho_DE c^2/(16 pi)) [u - ln(1 + u)].
It varies from place to place. It is larger than rho_DE c^2 itself wherever g is above 54 a0 (check C5). P2 says the
field's pressure does not vary in space at all. So a field that obeys P2 cannot sit in the law's state. It can only
fall. The law's stress then has to come from a second sector (the action's P.A - W term), and the field supplies the
amount and nothing else.

**3.5 a0(z) and w(z).**

- *Constant pressure.* The smooth part is a constant. In the usual split its w is -1 exactly. That is not dynamical
  dark energy.
- *Changing pressure.* The cold comoving charge is then not conserved: d(n a^3)/dt = a^3 dpbar/dt. For the record's
  three DESI curves the charge per baryon X is 5.0 to 5.3 at z = 0.5 to 2 and 7.7 to 10.1 today (check C4). What a halo
  holds is the collapse-weighted mean, 5.32 for collapse today (check C3). In one fluid n stays positive throughout, so
  the curves' past with w below -1 is a feature of the split and not a ghost.
- *a0 under P4a* (a0^2 proportional to -pbar). Flat for constant pressure. For the three DESI curves +0.063, +0.102 and
  +0.143 dex at z = 1, and +0.007, +0.030 and +0.057 dex at z = 2.5 (check C4). This is the record's own "pressure law"
  (L273 part 4). It also makes a0 the same everywhere in space. The record has a line against a0 moving inside a galaxy
  (CFG541 excludes 2e-3 at r_M).
- *a0 under P4b* (the field's mean density). +0.24 dex at z = 1, +0.55 at z = 2.5, +0.91 at z = 5.2. It runs within 6 %
  of the a0 proportional to H(z) law. kappa becomes 0.424 (canonical a0) or 0.513 (alt a0).
- *The owner's density reading.* The record's curve for a0 proportional to sqrt(rho_DE) with the DESI sets is -0.085,
  -0.099 and -0.111 dex at z = 2.5 (check C4 reproduces it). Route D does not lead to it. One field defines three mean
  quantities: its density, its pressure and their sum. "The dark-energy density" is not one of them unless the pressure
  is constant, because the split into a dust part and a smooth part is otherwise a choice. That reading needs the split
  put in by hand.

## 4. Checks run

One script, pasted in full with its output. It was run from a scratch directory and is not committed. Python 3 with
numpy, scipy and sympy; about 40 s, one process, peak memory about 120 MB. No download.

```python
# Route D checks. SI where units matter; collapse in units H0 = 1, densities in rho_crit0. About 40 s, one process.
import math, numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
G=6.67430e-11; c=2.99792458e8; Mpc=3.0856775814913673e22; pc=Mpc/1e6; kpc=Mpc/1e3; Msun=1.98847e30
H0=67.4e3/Mpc; OL=0.6847; XC=5.41                       # inputs: the record's canonical pair and its cold share
Ob=(1-OL)/(1+XC); Oc=XC*Ob; rho_cr=3*H0**2/(8*math.pi*G); rho_DE=OL*rho_cr; HL=H0*math.sqrt(OL); U=Msun/pc**2
A0={"canonical":9.3603e-11,"alt":1.1312e-10}

print("C1 column. rho_DE %.4e kg/m3, c/H_L %.1f Mpc, rho_DE c/H_L %.1f, rho_crit c/H0 %.1f Msun/pc2"%(rho_DE,c/HL/Mpc,rho_DE*c/HL/U,rho_cr*c/H0/U))
for k,a0 in A0.items():
    S=a0/(2*math.pi*G)
    print("  %-9s Sigma_0 %.1f Msun/pc2; f against rho_DE c/H_L %.4f; against rho_crit c/H0 %.4f; kappa on rho_DE %.4f, on rho_crit %.4f; rho_DE c^2 / (a0^2/8piG) = %.2f"
          %(k,S/U,S/(rho_DE*c/HL),S/(rho_cr*c/H0),a0/(c*math.sqrt(G*rho_DE)),a0/(c*math.sqrt(G*rho_cr)),rho_DE*c*c/(a0*a0/(8*math.pi*G))))
for lab,q in (("a0 = c H_L / 6",1/6),("a0 = c H_L / (2 pi)",1/(2*math.pi))):
    print("  %-20s f %.4f kappa %.4f"%(lab,4*q/3,q*math.sqrt(32*math.pi/3)/2))
print("  de Sitter ball's own column rho V/A = rho r/3: f %.4f, kappa %.4f (field 2 pi G Sigma) or %.4f (4 pi G Sigma)"%(1/3,(1/3)/math.sqrt(2/(3*math.pi)),(2/3)/math.sqrt(2/(3*math.pi))))
print("  Burkert rho0 r0 from the record: Donato 141 -> f %.3f; Li+2020 176.8 -> f %.3f (convention-dependent)"%(141/(rho_DE*c/HL/U),176.8/(rho_DE*c/HL/U)))

print("C2 identities (sympy)")
Gs,cs,rho,kap,a0,M,r,gN,w=sp.symbols('G c rho kappa a0 M r g_N w',positive=True)
f=sp.simplify((kap*cs*sp.sqrt(Gs*rho)/(2*sp.pi*Gs))/(rho*cs/sp.sqrt(8*sp.pi*Gs*rho/3)))
print("  f =",f,"=",sp.N(f.subs(kap,sp.Rational(1,2)),6),"at kappa 1/2; pressure scale a0^2/(8 pi G rho c^2) =",sp.simplify((kap*cs*sp.sqrt(Gs*rho))**2/(8*sp.pi*Gs*rho*cs**2)))
g=(gN+sp.sqrt(gN**2+4*gN*a0))/2; gc=g-gN
print("  law residual",sp.simplify(gN-g**2/(g+a0)),"; g_c - a0 g/(g+a0) =",sp.simplify(gc-a0*g/(g+a0)))
Mc=sp.simplify(gc.subs(gN,Gs*M/r**2)*r**2/Gs); rc=sp.simplify(sp.diff(Mc,r)/(4*sp.pi*r**2))
print("  strong field: rho_c r ->",sp.limit(rc*r,r,0),"; weak field: 2 pi G rho_c r^2 ->",sp.simplify(2*sp.pi*Gs*sp.limit(rc*r**2,r,sp.oo)))
C=sp.symbols('C'); print("  c_s = 0 matter-era attractor delta_Q/delta_m =",sp.simplify(sp.solve(sp.Eq(C,3*w*C+1+w),C)[0]))
t=sp.symbols('t'); h,H,ri,rb,pb=[sp.Function(n)(t) for n in ('h','H','rho_in','rhobar','pbar')]
print("  d(rho_in - rhobar)/dt + 3h(rho_in - rhobar) + 3(h-H)(rhobar+pbar) =",sp.simplify((-3*h*(ri+pb)+3*H*(rb+pb))+3*h*(ri-rb)+3*(h-H)*(rb+pb)))
rj=sp.solve(sp.Eq(a0*r**2/Gs,M),r)[0]
print("  saturated core joined to an isothermal halo where M_c = M: sigma^2 - sqrt(G M a0)/2 =",sp.simplify(a0*rj/2-sp.sqrt(Gs*M*a0)/2))
gf=sp.Function('g')(r); print("  weak field, P = g^2/(8 pi G) + balance + Poisson:",sp.dsolve(sp.Eq(sp.diff(r**2*gf,r)/r**2,-sp.diff(gf**2,r)/(2*gf)),gf))
Md,n,Mh,s8,dc,Dl,rm,M8=sp.symbols('Mdot n M_h sigma8 delta_c Delta rho_m M_8',positive=True)
rin=Md/(4*sp.pi*r**2*sp.sqrt(2*Gs*M/r)); print("  cold inflow: dln rho/dln r =",sp.simplify(r*sp.diff(rin,r)/rin))
rh=Dl*rm*((s8/dc)*(Mh/M8)**(-(n+3)/6))**3; Sg=Mh/(sp.pi*(3*Mh/(4*sp.pi*rh))**sp.Rational(2,3))
print("  clustered halo column: dln Sigma/dln M =",sp.simplify(Mh*sp.diff(Sg,Mh)/Sg),"; dln Sigma/dln sigma8 =",sp.simplify(s8*sp.diff(Sg,s8)/Sg))

def tophat(Om,rho,p,a_c,ai=1e-3):
    """Matter Om (dust) + one c_s = 0 fluid (rho(a), p(a)). Returns M_exc/M_m at R = R_ta/2 and the identity integral."""
    Hb=lambda a: math.sqrt(Om*a**-3+rho(a)); wi=p(ai)/rho(ai)
    def rhs(t,y,d):
        a,R,Rd,x,I=y; rmi=Om*ai**-3*(1+d)/R**3; hh=Rd/R; Ha=Hb(a)
        return [a*Ha,Rd,-0.5*(rmi+x+3*p(a))*R,-3*hh*(x+p(a)),-((rho(a)+p(a))/(Om*a**-3))*3*(hh-Ha)*R**3*(ai/a)**3]
    def go(d):
        e1=lambda t,y,d: y[1]-1e-3; e1.terminal=True; e1.direction=-1
        e2=lambda t,y,d: y[0]-3.0; e2.terminal=True
        return solve_ivp(rhs,[0,50],[ai,1.0,Hb(ai)*(1-d/3),rho(ai)*(1+(1+wi)/(1-3*wi)*d),0.0],args=(d,),events=[e1,e2],rtol=1e-10,atol=1e-14)
    d=brentq(lambda d: (lambda s: s.y[0][-1] if len(s.t_events[0]) else 3.0)(go(d))-a_c,1e-6,0.9,xtol=1e-13); s=go(d)
    R=s.y[1]; k=np.argmax(R); j=k+np.argmax(R[k:]<=R[k]/2); a,Rr,Rd,x,I=s.y[:,j]; rmi=Om*ai**-3*(1+d)/Rr**3
    return (x-rho(a))/rmi, (rho(ai)*(1+wi)/(1-3*wi)*d)/(Om*ai**-3*(1+d))+I/(1+d)
print("C3 top-hat: gathered cold mass per baryon mass at virialisation (collapse at z = 0 | z = 0.5)")
for s in (1.0,0.5,0.1):
    L=1-Ob-s*Oc; r_=lambda a: L+s*Oc*a**-3; p_=lambda a: -L
    m0,i0=tophat(Ob,r_,p_,1.0); m5,_=tophat(Ob,r_,p_,2/3)
    print("  constant pressure, dust part %.2f x Oc (1+w0 = %.4f): %.4f | %.4f   identity %.4f   X = %.3f"%(s,s*Oc/(L+s*Oc),m0,m5,i0,s*XC))
for wv in (-0.99,-0.95,-0.90,-0.80,-0.50,-0.20):
    r_=lambda a: (1-Ob)*a**(-3*(1+wv)); p_=lambda a: wv*r_(a)
    m0,i0=tophat(Ob,r_,p_,1.0); m5,_=tophat(Ob,r_,p_,2/3)
    print("  baryons + one fluid, constant w %.2f: %.5f | %.5f   identity %.5f   short of 5.41 by %.0f | %.0f"%(wv,m0,m5,i0,XC/m0,XC/m5))
for wv in (-0.99,-0.95,-0.90,-0.80):
    r_=lambda a: OL*a**(-3*(1+wv)); p_=lambda a: wv*r_(a); e,_=tophat(1-OL,r_,p_,1.0)
    print("  separate dust (0.3153) collapses, c_s = 0 fluid w %.2f rides along: M_exc/M_dust %.5f, per baryon %.4f, short by %.0f"%(wv,e,e*(1+XC),XC/(e*(1+XC))))

E=lambda z: math.sqrt((1-OL)*(1+z)**3+OL); CPL={"Pantheon+":(-0.838,-0.62),"DESY5":(-0.752,-0.86),"Union3":(-0.667,-1.09)}
fde=lambda z,w0,wa: (1+z)**(3*(1+w0+wa))*math.exp(-3*wa*z/(1+z))
for k,(w0,wa) in CPL.items():
    r_=lambda a: Oc*a**-3+OL*fde(1/a-1,w0,wa); p_=lambda a: (w0+wa*(1-a))*OL*fde(1/a-1,w0,wa)
    m0,i0=tophat(Ob,r_,p_,1.0); m5,_=tophat(Ob,r_,p_,2/3)
    print("  one fluid = dust part + the record's CPL set %-9s: %.4f | %.4f   identity %.4f"%(k,m0,m5,i0))
print("C4 w(z), a0(z)/a0(0), cold share X(z)")
print("  z: w of (Lambda + dust) fluid | a0 on -pbar | a0 on the field's mean density | a0 ~ H(z)")
for z in (0,0.5,1,2,2.5,5.2):
    print("  %-4g %.4f | 1.000 | %.3f (%+.3f dex) | %.3f (%+.3f dex)"%(z,-OL/(OL+Oc*(1+z)**3),math.sqrt((OL+Oc*(1+z)**3)/(OL+Oc)),0.5*math.log10((OL+Oc*(1+z)**3)/(OL+Oc)),E(z),math.log10(E(z))))
for k,(w0,wa) in CPL.items():
    dn=lambda z: 0.5*math.log10(fde(z,w0,wa)); pr=lambda z: 0.5*math.log10((w0+wa*z/(1+z))/w0*fde(z,w0,wa))
    print("  %-9s a0 on density %+.3f, %+.3f dex at z = 1, 2.5; on -pbar %+.3f, %+.3f dex; X(z = 0, 0.25, 0.5, 1, 2) = %s"%(k,dn(1),dn(2.5),pr(1),pr(2.5),
          " ".join("%.2f"%(XC+(1+w0+wa*zz/(1+zz))*OL*fde(zz,w0,wa)/(Ob*(1+zz)**3)) for zz in (0,0.25,0.5,1,2))))
print("  kappa if rho_DE means the whole field: canonical %.4f, alt %.4f"%(0.5*math.sqrt(OL/(OL+Oc)),0.5/math.sqrt(OL+Oc)))

print("C5 sizes")
print("  law's halo M_c/M_b at r/r_M = 1, 3, 5.89, 10, 60:"," ".join("%.2f"%((math.sqrt(1+4*x*x)-1)/2) for x in (1,3,5.89,10,60)))
print("  law-state stress J = rho_DE c^2 at g/a0 = %.1f (kappa 1/2)"%brentq(lambda u:(u-math.log(1+u))/(16*math.pi)-1,1,1e4))
Mb=6e10*Msun
for k,a0v in A0.items():
    rM=math.sqrt(G*Mb/a0v); rr=10*kpc; gcf=lambda rv:(lambda gn:(gn+math.sqrt(gn*gn+4*gn*a0v))/2-gn)(G*Mb/rv**2); hh=rr*1e-4
    rl=((rr+hh)**2*gcf(rr+hh)-(rr-hh)**2*gcf(rr-hh))/(2*hh)/(4*math.pi*G*rr*rr); md=(2/3)*XC*Mb/(13.8e9*3.15576e7)
    print("  %-9s 6e10 Msun: r_M %.2f kpc, sigma %.1f km/s; law's density at 10 kpc over a cold inflow of %.1f Msun/yr: %.0f; field with c_s = c: column/Sigma_0 = %.1e (1+w)"
          %(k,rM/kpc,math.sqrt(0.5*math.sqrt(G*Mb*a0v))/1e3,md*3.15576e7/Msun,rl/(md/(4*math.pi*rr*rr*math.sqrt(2*G*Mb/rr))),rho_DE*G*Mb/c**2/(a0v/(2*math.pi*G))))
for k,a0v in A0.items(): print("  %-9s clustering gives v^3 = 10 G M H0; with M = 6.41 M_b this meets v^4 = G M_b a0 only at v = %.0f km/s"%(k,a0v/(10*(1+XC)*H0)/1e3))
h=0.674; S=(4/3)*178**(2/3)*(1-OL)*2.775e11*h*h*(8/h)*(0.812/1.686)**2/1e12
print("  clustered halo, n = -2, sigma8 0.812: mean column inside the virial radius %.2f Msun/pc2 = %.4f of rho_DE c/H_L; goes as sigma8^2"%(S,S/(rho_DE*c/HL/U)))
```

Output:

```
C1 column. rho_DE 5.8424e-27 kg/m3, c/H_L 5375.4 Mpc, rho_DE c/H_L 464.0, rho_crit c/H0 560.8 Msun/pc2
  canonical Sigma_0 106.9 Msun/pc2; f against rho_DE c/H_L 0.2303; against rho_crit c/H0 0.1906; kappa on rho_DE 0.5000, on rho_crit 0.4137; rho_DE c^2 / (a0^2/8piG) = 100.53
  alt       Sigma_0 129.2 Msun/pc2; f against rho_DE c/H_L 0.2784; against rho_crit c/H0 0.2303; kappa on rho_DE 0.6043, on rho_crit 0.5000; rho_DE c^2 / (a0^2/8piG) = 68.83
  a0 = c H_L / 6       f 0.2222 kappa 0.4824
  a0 = c H_L / (2 pi)  f 0.2122 kappa 0.4607
  de Sitter ball's own column rho V/A = rho r/3: f 0.3333, kappa 0.7236 (field 2 pi G Sigma) or 1.4472 (4 pi G Sigma)
  Burkert rho0 r0 from the record: Donato 141 -> f 0.304; Li+2020 176.8 -> f 0.381 (convention-dependent)
C2 identities (sympy)
  f = sqrt(6)*kappa/(3*sqrt(pi)) = 0.230329 at kappa 1/2; pressure scale a0^2/(8 pi G rho c^2) = kappa**2/(8*pi)
  law residual 0 ; g_c - a0 g/(g+a0) = 0
  strong field: rho_c r -> a0/(2*pi*G) ; weak field: 2 pi G rho_c r^2 -> sqrt(G)*sqrt(M)*sqrt(a0)/2
  c_s = 0 matter-era attractor delta_Q/delta_m = (-w - 1)/(3*w - 1)
  d(rho_in - rhobar)/dt + 3h(rho_in - rhobar) + 3(h-H)(rhobar+pbar) = 0
  saturated core joined to an isothermal halo where M_c = M: sigma^2 - sqrt(G M a0)/2 = 0
  weak field, P = g^2/(8 pi G) + balance + Poisson: Eq(g(r), C1/r)
  cold inflow: dln rho/dln r = -3/2
  clustered halo column: dln Sigma/dln M = -n/3 - 2/3 ; dln Sigma/dln sigma8 = 2
C3 top-hat: gathered cold mass per baryon mass at virialisation (collapse at z = 0 | z = 0.5)
  constant pressure, dust part 1.00 x Oc (1+w0 = 0.2799): 5.3871 | 5.3802   identity 5.3871   X = 5.410
  constant pressure, dust part 0.50 x Oc (1+w0 = 0.1399): 2.6964 | 2.6919   identity 2.6964   X = 2.705
  constant pressure, dust part 0.10 x Oc (1+w0 = 0.0280): 0.5399 | 0.5391   identity 0.5399   X = 0.541
  baryons + one fluid, constant w -0.99: 0.00601 | 0.00324   identity 0.00601   short of 5.41 by 900 | 1672
  baryons + one fluid, constant w -0.95: 0.03217 | 0.01769   identity 0.03217   short of 5.41 by 168 | 306
  baryons + one fluid, constant w -0.90: 0.07021 | 0.03965   identity 0.07021   short of 5.41 by 77 | 136
  baryons + one fluid, constant w -0.80: 0.16978 | 0.10099   identity 0.16978   short of 5.41 by 32 | 54
  baryons + one fluid, constant w -0.50: 0.90321 | 0.61798   identity 0.90321   short of 5.41 by 6 | 9
  baryons + one fluid, constant w -0.20: 5.39242 | 4.33424   identity 5.39242   short of 5.41 by 1 | 1
  separate dust (0.3153) collapses, c_s = 0 fluid w -0.99 rides along: M_exc/M_dust 0.00171, per baryon 0.0110, short by 492
  separate dust (0.3153) collapses, c_s = 0 fluid w -0.95 rides along: M_exc/M_dust 0.00905, per baryon 0.0580, short by 93
  separate dust (0.3153) collapses, c_s = 0 fluid w -0.90 rides along: M_exc/M_dust 0.01950, per baryon 0.1250, short by 43
  separate dust (0.3153) collapses, c_s = 0 fluid w -0.80 rides along: M_exc/M_dust 0.04554, per baryon 0.2919, short by 19
  one fluid = dust part + the record's CPL set Pantheon+: 5.3218 | 5.3161   identity 5.3218
  one fluid = dust part + the record's CPL set DESY5    : 5.3221 | 5.3009   identity 5.3221
  one fluid = dust part + the record's CPL set Union3   : 5.3238 | 5.2868   identity 5.3238
C4 w(z), a0(z)/a0(0), cold share X(z)
  z: w of (Lambda + dust) fluid | a0 on -pbar | a0 on the field's mean density | a0 ~ H(z)
  0    -0.7201 | 1.000 | 1.000 (+0.000 dex) | 1.000 (+0.000 dex)
  0.5  -0.4326 | 1.000 | 1.290 (+0.111 dex) | 1.322 (+0.121 dex)
  1    -0.2434 | 1.000 | 1.720 (+0.236 dex) | 1.791 (+0.253 dex)
  2    -0.0870 | 1.000 | 2.877 (+0.459 dex) | 3.033 (+0.482 dex)
  2.5  -0.0566 | 1.000 | 3.566 (+0.552 dex) | 3.769 (+0.576 dex)
  5.2  -0.0107 | 1.000 | 8.211 (+0.914 dex) | 8.708 (+0.940 dex)
  Pantheon+ a0 on density -0.005, -0.085 dex at z = 1, 2.5; on -pbar +0.063, +0.007 dex; X(z = 0, 0.25, 0.5, 1, 2) = 7.67 5.70 5.21 5.16 5.31
  DESY5     a0 on density +0.004, -0.099 dex at z = 1, 2.5; on -pbar +0.102, +0.030 dex; X(z = 0, 0.25, 0.5, 1, 2) = 8.86 6.01 5.23 5.09 5.29
  Union3    a0 on density +0.013, -0.111 dex at z = 1, 2.5; on -pbar +0.143, +0.057 dex; X(z = 0, 0.25, 0.5, 1, 2) = 10.05 6.36 5.26 5.02 5.26
  kappa if rho_DE means the whole field: canonical 0.4243, alt 0.5128
C5 sizes
  law's halo M_c/M_b at r/r_M = 1, 3, 5.89, 10, 60: 0.62 2.54 5.41 9.51 59.50
  law-state stress J = rho_DE c^2 at g/a0 = 54.3 (kappa 1/2)
  canonical 6e10 Msun: r_M 9.45 kpc, sigma 116.8 km/s; law's density at 10 kpc over a cold inflow of 15.7 Msun/yr: 85; field with c_s = c: column/Sigma_0 = 2.3e-12 (1+w)
  alt       6e10 Msun: r_M 8.60 kpc, sigma 122.5 km/s; law's density at 10 kpc over a cold inflow of 15.7 Msun/yr: 95; field with c_s = c: column/Sigma_0 = 1.9e-12 (1+w)
  canonical clustering gives v^3 = 10 G M H0; with M = 6.41 M_b this meets v^4 = G M_b a0 only at v = 669 km/s
  alt       clustering gives v^3 = 10 G M H0; with M = 6.41 M_b this meets v^4 = G M_b a0 only at v = 808 km/s
  clustered halo, n = -2, sigma8 0.812: mean column inside the virial radius 4.62 Msun/pc2 = 0.0099 of rho_DE c/H_L; goes as sigma8^2
```

How to read it.

- C1 is section 2.2. C2 is every identity quoted in sections 2 and 3.
- C3: "identity" is the right-hand side of the lemma's integral, computed along the same run. It matches the direct
  count to every printed digit in all 12 rows where it is printed.
- C3's constant-w rows use a universe of baryons and one fluid only. That background is not the observed one. The rows
  show the scaling with (1 + w); the size of each shortfall belongs to that background.
- C3's ride-along rows put a second dust in by hand. They are an upper bracket and form B does not allow them.
- C5's inflow line and clustered-column line are hand-level estimates, not solutions.

## 5. What is fixed and what is free

| item | status |
|---|---|
| f | not fixed. f = kappa sqrt(2/(3 pi)) is an identity |
| kappa | free. Nothing here moves it. Under P4b it is only renamed (0.424 / 0.513) |
| strong-field half, rho_c r = Sigma_0 | assumed with the law. Clustering does not produce it |
| weak-field half, sigma^2 = (1/2) sqrt(G M_b a0) | assumed with the law. It follows from two added statements (2.6), both by hand. Clustering gives M proportional to v^3 instead |
| the curve between the two halves | free |
| the cold amount, 5.41 | an initial condition of the field. Not fixed |
| the clustering rule, M_c/M_b = Integral X (-dv) | fixed by P2. The one derived statement in this note |
| a0 the same everywhere in space | fixed by P2 with P4a |
| w(z) of the field | follows from the amount and the pressure history. Not predicted |

## 6. Predictions

**Clusters.** In the best case every collapsed region holds 5.38 to 5.39 times its baryons in cold mass at
virialisation, whatever its mass or epoch; 5.29 to 5.32 with the DESI curves. That is the record's cosmic share and
adds nothing to it. There is no statement about cores (X40b: cluster cores need 3 to 5 times Sigma_0), none about
groups, and none about a collision, because a collision is streams crossing and the lemma stops there.

**CMB.** In the best case the linear equations are those of the record's cold reference: dust and a constant. The
peaks row passes as F1's row passes, and no new number comes out. With a dark-energy-like w and no dust-like past the
field holds no cold part at z = 1100, and the peaks fail by F1's own count.

**a0(z).** P4a: flat; or, with the DESI curves, +0.06 to +0.14 dex at z = 1 and +0.01 to +0.06 at z = 2.5. P4b: +0.24
dex at z = 1 and +0.55 at z = 2.5.

**w(z).** With constant pressure: the field's w is -Omega_Lambda/(Omega_Lambda + Omega_c (1 + z)^3), which is -0.72
today; the smooth part has w = -1. Dynamical dark energy needs a changing pressure, and then the cold charge per
baryon moves with it as in 3.5.

**Against the record's a0(z) constraints.**

- P4a sits inside everything the record holds. That is not support. The record's standing line is "untested, not
  unsupported", and AT2 found all 52 cells of the 22 on-disk samples BLOCKED.
- P4b is the a0 proportional to H(z) law to within 6 %. CFG223 has that law 2.6 and 5.7 statistical sigma above RC100's
  two highest-redshift bins and 3.4 to 3.6 above CRISTAL's fit-route points, with baryon-mass bands that cover the gap.
  The Jeanneau refit (`prep_2026/jeanneau_refit/`) sits 1.41 sigma from it and 0.51 from flat, and calls itself still
  underpowered. L37's 27 sigma kill of a0 proportional to H was for a law that acts in the linear CMB equations. Form B
  has no a0 there, so that kill does not carry over without a check. So the record leans against P4b and does not
  decide it.

## 7. What the record already says

**Column and surface density.**
- `opus_48_extended_research/papers/THE_HORIZON_FORM_OF_THE_BTFR.md`, sections 1 and 2: writing a0 through the de
  Sitter radius is called "a change of variables" there, one that derives nothing kappa = 1/2 did not already
  assume. The mean column inside r_M is a0/(pi G) = 213.8 Msun/pc^2. The cold mass equals M_b at r_M (Lean-certified
  there). Priority for the universal column goes to Milgrom 2009.
- `campaign_fresh_gravity/CFG0_own_findings_inventory.md` F25: Burkert rho0 r0 = 176.8 Msun/pc^2 from 162 fits,
  against 106.9 (+0.22 dex) and 129.0 (+0.14 dex). `campaign_fresh_gravity/closure_map/GATES.md` row 1.06: met, but
  failed as declared (0.89 against a declared 0.4 to 0.8).
- `rebuild_2026_10_22/X47_vacuum_tethered_core_floor/README.md`: a floor at fixed Sigma is "a restatement of X38, not
  a result"; the content sits in a coefficient that carries kappa. A local threshold fails growth and data.
- `rebuild_2026_10_22/X40b_core_surface_density_scaling/README.md`: cores at a0/(2 pi G) pass SPARC and cluster
  outskirts; cluster cores need 3 to 5 times that; no framework-native rule supplies it. Letting a0 follow the DESI
  curve changes the column by at most 1.34.
- "column density": seven files. Two bear on this. `campaign_fresh_gravity/CFG264_rational_four/`, route R5: the
  vacuum's column on a horizon as a route to the 4; frozen at 0.1 %, not run. `rebuild_2026_10_22/NQ1_near_miss_census/`
  batch 4, row IC1: a column rule for cluster cores; inactive, about 6.4 times short. The other five are gas, target or
  lensing columns.

**Clustering dark energy, quintessence.**
- `campaign_fresh_gravity/CFG541_cold_energy_equations_precise/EQUATIONS.md`: the settled state needs an energy sink.
  Exchange with dark energy is allowed only if the dark energy does not cluster; for a clustering one a0 would move by
  2e-3 at r_M. CFG542, CFG544 and CFG620 freeze the same condition.
- `opus_48_extended_research/papers/THE_COMPLETION.md`: one free w(z) with baryons alone reproduces the background
  (the dark degeneracy); the binding constraint is CMB lensing, which needs clustering down to z below 0.30.
- `why_4_puzzle/W4_09_dark_energy_models/README.md`: no dark-energy model fixes kappa. Each gives a number times its
  own free amplitude.
- `campaign_fresh_gravity/closure_map/ACTIONS_AND_NOGOS.md`, the XR20 row: five a0-Lambda ties, a quintessence one
  among them. The tie that works has kappa written in by hand. The row gives no verdict for the quintessence tie.
- The record's own action (A) already holds cold dust beside a constant: the clock's K(Q) term has
  w = w0/(w0 + a^3), dust in its cold limit (QX17 limits table; FB1 note, item 2.1). So Route D's best case is that
  sector under another name, and MK1 (no one dust constant), COL1 (the fold) and FLD1 (the reach) apply to it
  unchanged.
- (One pointer to a quarantined folder was struck here by the lead before this note was committed. The redo in C3
  stands on its own.)

**kappa.**
- `campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CLOSURE_2026-11-03.md`: every route reduces to one
  missing length; none derives 1/2; data cannot separate 1/2 from 0.461 (floor about 9 %).
  `why_4_puzzle/W4_24_two_phase_vacuum_constant/README.md`: kappa FREE.
- `qwen_38_experiment/KAPPA_LEDGER.md`: T002, 1/(32 pi) is not special (3 matches against 2.23 expected). T001, no
  published de Sitter route lands in the fit window.
- Verlinde: `rebuild_2026_10_22/KA1_any_value_screen/README.md` row K559 (kappa 0.482 on H_Lambda; 1 of 5 gates; DEAD)
  and CFG117 (0 of 16 shape cases).

**a0(z).**
- `rebuild_2026_10_22/AT2_a0z_on_disk_samples/README.md`: 52 of 52 cells BLOCKED. No public sample decides whether a0
  follows rho_DE or H(z).
- `campaign_fresh_gravity/CFG223_a0_over_cosmic_time/README.md`: flat a0 lies inside the statistical interval of 7 of
  8 points; the baryon-mass bands span the plot; the numbers for H(z) are quoted in section 6.
- `fable_independent_2026/A0Z_FLAT_LAW_TEST_LEDGER_2026-09-18.md` and the L37, L273 scripts beside it: three a0(z) laws
  circulate (pressure, density, total density). The density reading with DESI gives 0.87 at z = 2. The pressure
  reading stays within about 0.1 dex of flat.
- The kappa closure note says the flat band of CFG689 is the law's prediction, not a measurement of a0 in galaxies.

**This push.** `fable52_push/CLOSURE.md`: the action holds the law only in a static state and cannot reach it (COL1,
FLD1); no one-variable dust term works (MK1, MK2); a law keyed to the baryons' acceleration is unstable (REL1).
`fable52_push/DT1_dust_term_design/ACTION.md` keeps the dark-energy field and the clock's dust as two things. Route D
asked whether they can be one. With zero sound speed they can, and the result is the clock's cold dust again.

## 8. The weakest step

The negative on the shape rests on P2 taken exactly: zero sound speed, one stream, gravity only. That is what makes
the field's pressure uniform and so unable to carry the law's stress. A field whose stress answers to the local
gravitational field would carry it, but that is the action's law sector and not clustering, and a sound speed or dust
term that depends on one local variable is MK1 and MK2. So the result is firm inside Route D as posed and says nothing
about a field outside P2.

Three smaller weaknesses.

- "No argument fixes f" covers the five arguments tried here and the record's register. It is not a no-go theorem.
- The shortfall factors for constant w belong to a baryons-and-one-fluid universe that is not the observed one. The
  linear scaling with (1 + w) is exact. The factors 19 to 1700 are brackets.
- Zero-sound-speed collapse, the dark degeneracy, the r^(-9/4) slope and Milgrom's central column are quoted from
  memory. No paper was opened. The lemma and every number above were derived or run here and do not rest on them.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
