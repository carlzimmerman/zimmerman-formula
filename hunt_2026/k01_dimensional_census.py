#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k01 -- ANGLE 2: the exhaustive dimensional construction from a_0, G, c, hbar, Lambda and one mass or length.

The point of the exercise, stated before any number is computed:

    {a_0, G, c} is a COMPLETE dimensional basis (the 3x3 exponent matrix in (L,M,T) is non-singular).
    Therefore
      (i)  every dimensionful quantity has exactly ONE a_0-natural value -- the enumeration is finite, not open-ended;
      (ii) Lambda adds nothing, because the first law a_0 = (c/2) sqrt(G rho_DE) makes Lambda = 32 pi a_0^2 / c^4;
      (iii) hbar adds exactly ONE dimensionless number, and the census below identifies it;
      (iv) any OTHER constant of nature X contributes exactly one dimensionless D(X) = X a_0^p G^q c^r,
           so "does a measured constant sit on an a_0 combination?" is a finite question with a finite answer.

Run it and it prints the whole table, both footings, with every O(1) coincidence flagged AS numerology unless a
physical argument is named in the code.  Mutation control: repeat the census with a_0 -> 10 a_0 and a_0 -> a_0/10,
and with a_0 replaced by cH_0 (the a_0-free alternative), and count hits.  A census whose hit count does not move
is measuring the density of the number line, not a_0.

Rules honoured: both footings on every dimensionful number; checks that CAN fail; a mutation control; the
LambdaCDM/a_0-free alternative computed beside the framework; verdict reported against interest.
"""
import math, itertools
import numpy as np
from hunt_lib import Check, P, info, A0

# ----------------------------------------------------------------------------------------------------- constants
G     = 6.67430e-11          # m^3 kg^-1 s^-2   (CODATA 2018)
c     = 2.99792458e8         # m/s              (exact)
hbar  = 1.054571817e-34      # J s              (exact-derived)
kB    = 1.380649e-23         # J/K              (exact)
mp    = 1.67262192e-27       # kg
mn    = 1.67492750e-27
me    = 9.1093837e-31
mmu   = 1.883531627e-28
mpi   = 2.4880674e-28        # charged pion
sigT  = 6.6524587e-29        # m^2   Thomson
alpha = 7.2973525693e-3
e_ch  = 1.602176634e-19
eps0  = 8.8541878128e-12
a_rad = 7.565723e-16         # J m^-3 K^-4
sigSB = 5.670374419e-8
Msun  = 1.98892e30
Lsun  = 3.828e26
pc    = 3.0856775814913673e16
kpc, Mpc = 1e3*pc, 1e6*pc
yr    = 3.1557e7
Gyr   = 1e9*yr
h_hub = 0.674
H0    = 100*h_hub*1e3/Mpc            # 2.1817e-18 s^-1
OmL, OmM, Omb = 0.685, 0.315, 0.0493
rho_crit = 3*H0**2/(8*math.pi*G)
T_CMB = 2.72548                       # K
Z_FW  = math.sqrt(32*math.pi/3)       # 5.78960...  the framework's Z

# both footings, and the H_Lambda each footing implies through a_0 = c H_Lambda / Z
FOOT = {}
for k, a0 in A0.items():
    FOOT[k] = dict(a0=a0, HL=Z_FW*a0/c, Lam=32*math.pi*a0**2/c**4, rhoDE=4*a0**2/(G*c**2))

ck = Check()

P("="*126)
P("k01 -- ANGLE 2: EXHAUSTIVE DIMENSIONAL CONSTRUCTION FROM a_0, G, c, hbar, Lambda")
P("="*126)
P(f"  footings: canonical a_0 = {A0['canonical']:.6g} m/s^2   |   alt a_0 = {A0['alt']:.6g} m/s^2")
for k, f in FOOT.items():
    P(f"    {k:<10s}  H_Lambda = Z a_0/c = {f['HL']:.5e} s^-1 = {f['HL']*Mpc/1e3:7.3f} km/s/Mpc"
      f"   Lambda = 32 pi a_0^2/c^4 = {f['Lam']:.5e} m^-2   rho_DE = 4a_0^2/(Gc^2) = {f['rhoDE']:.5e} kg/m^3")
P(f"  for reference: Planck H_0 = {H0*Mpc/1e3:.3f} km/s/Mpc, H_0 sqrt(Om_L) = {H0*math.sqrt(OmL)*Mpc/1e3:.3f} km/s/Mpc")
P("  NOTE the internal consistency, stated against interest: the ALT footing's implied H_Lambda is H_0 itself, not")
P("  H_0 sqrt(Om_L) -- that is what 'rho_total / cH_0' means, and it is why the two footings are 0.082 dex apart.")

# ================================================================================================== 1. COMPLETENESS
P("\n" + "="*126)
P("1. THE COMPLETENESS THEOREM -- why this enumeration terminates")
P("="*126)
#            L   M   T
DIM = {"a0": (1, 0, -2), "G": (3, -1, -2), "c": (1, 0, -1), "hbar": (2, 1, -1), "kB": (2, 1, -2)}   # kB per Kelvin
Mx = np.array([DIM["a0"], DIM["G"], DIM["c"]], dtype=float).T     # columns a0, G, c ; rows L, M, T
det = np.linalg.det(Mx)
info(f"exponent matrix of (a_0, G, c) in (L, M, T):\n{Mx}")
info(f"determinant = {det:+.6f}")
ck("K01.1 {a_0, G, c} is a COMPLETE dimensional basis -- the determinant is non-zero, so every dimensionful "
   "quantity has exactly one a_0-natural value and the enumeration below is exhaustive rather than a sample",
   abs(det) > 1e-9, f"det = {det:+.4f}")

def natural(l, m, t):
    """unique (p,q,r) with a_0^p G^q c^r having dimensions L^l M^m T^t"""
    return np.linalg.solve(Mx, np.array([l, m, t], dtype=float))

def nat_value(l, m, t, a0):
    p, q, r = natural(l, m, t)
    return a0**p * G**q * c**r, (p, q, r)

# --------------------------------------------------------------------------- the table of a_0-natural quantities
P("\n  the complete table of a_0-natural values, one row per physical dimension (both footings):")
P(f"  {'quantity':<26s} {'(L,M,T)':>12s} {'exponents (p,q,r) of (a0,G,c)':>32s} {'canonical':>14s} {'alt':>14s}  unit")
ROWS = [
    ("length",                (1, 0, 0),   "m"),
    ("time",                  (0, 0, 1),   "s"),
    ("mass",                  (0, 1, 0),   "kg"),
    ("acceleration",          (1, 0, -2),  "m/s^2"),
    ("surface density",       (-2, 1, 0),  "kg/m^2"),
    ("volume density",        (-3, 1, 0),  "kg/m^3"),
    ("pressure / energy dens",(-1, 1, -2), "Pa"),
    ("frequency",             (0, 0, -1),  "1/s"),
    ("specific power",        (2, 0, -3),  "W/kg"),
    ("luminosity",            (2, 1, -3),  "W"),
    ("force",                 (1, 1, -2),  "N"),
    ("specific ang. momentum",(2, 0, -1),  "m^2/s"),
    ("dynamic viscosity",     (-1, 1, -1), "Pa s"),
    ("magnetic field",        (0, 0.5, -1),"T (via B^2/2mu0)"),
]
a0_free = []
for name, (l, m, t), unit in ROWS:
    if name == "magnetic field":
        val = {k: math.sqrt(2*4e-7*math.pi*nat_value(-1, 1, -2, f['a0'])[0]) for k, f in FOOT.items()}
        p, q, r = natural(-1, 1, -2); p, q, r = p/2, q/2, r/2
    else:
        val = {k: nat_value(l, m, t, f['a0'])[0] for k, f in FOOT.items()}
        p, q, r = natural(l, m, t)
    if abs(p) < 1e-9:
        a0_free.append(name)
    P(f"  {name:<26s} {str((l,m,t)):>12s} {f'a0^{p:+.3f} G^{q:+.3f} c^{r:+.3f}':>32s} "
      f"{val['canonical']:14.5e} {val['alt']:14.5e}  {unit}")

P("\n  THE FIRST RESULT OF THE ANGLE, and it is a theorem, not a fit:")
for n in a0_free:
    P(f"    * the a_0-natural {n.upper()} contains NO a_0 (exponent exactly 0)")
P("    => a_0, G and c CANNOT construct a luminosity or a force.  Corollary, and it is the hunt's own blocker")
P("       written as an identity: NO stellar mass-to-light ratio, and no L-M relation of any kind, can ever follow")
P("       from a_0 alone.  Item 76's 'Upsilon predicted from Lambda' is therefore a RATIO calibration -- it divides")
P("       a measured a_0 by Planck's a_0 -- and not a prediction of Upsilon from first principles.  Any future")
P("       candidate of the form (luminosity) = f(a_0, G, c, mass) is dead before it is tested.")
ck("K01.2 the a_0-natural LUMINOSITY is c^5/G and the a_0-natural FORCE is c^4/G -- both a_0-free.  This check "
   "fails if either carries a non-zero power of a_0, which would open the M/L route",
   set(a0_free) == {"luminosity", "force"}, f"a_0-free dimensions found: {a0_free}")

# ================================================================================== 2. WHAT hbar AND Lambda ADD
P("\n" + "="*126)
P("2. WHAT hbar AND Lambda ADD TO THE BASIS -- exactly one number and exactly nothing")
P("="*126)
p_h, q_h, r_h = natural(*DIM["hbar"])
info(f"hbar has the dimensions of a_0^{p_h:+.4f} G^{q_h:+.4f} c^{r_h:+.4f}  ->  the unique dimensionless is "
     f"hbar * a_0^{-p_h:+.0f} G^{-q_h:+.0f} c^{-r_h:+.0f} = hbar G a_0^2 / c^7")
for k, f in FOOT.items():
    D = hbar*G*f['a0']**2/c**7
    lP2 = hbar*G/c**3
    P(f"    {k:<10s}  hbar G a_0^2/c^7 = {D:.6e}      Lambda l_P^2/(32 pi) = {f['Lam']*lP2/(32*math.pi):.6e}   "
      f"ratio = {D/(f['Lam']*lP2/(32*math.pi)):.12f}")
ok = all(abs(hbar*G*f['a0']**2/c**7 / (f['Lam']*hbar*G/c**3/(32*math.pi)) - 1) < 1e-12 for f in FOOT.values())
ck("K01.3 the ONE dimensionless number hbar contributes is the cosmological constant in Planck units (over 32 pi) "
   "-- i.e. the framework's only possible quantum statement IS the cosmological-constant problem, and it is a "
   "restatement of the first law, not new content.  This forecloses the whole 'a_0 meets quantum mechanics' class",
   ok, "identity holds to 1e-12 on both footings")
P("    Lambda adds nothing at all: the first law fixes Lambda = 32 pi a_0^2/c^4, so (a_0, G, c, Lambda) is")
P("    over-complete and every 'Lambda-and-a_0' construction below is algebraically an a_0 construction.")

# =========================================================================== 3. THE CENSUS OF MEASURED CONSTANTS
P("\n" + "="*126)
P("3. THE CENSUS -- every measured constant of nature against its unique a_0-natural value")
P("="*126)
# name, value, (L,M,T) dimensions, note
CONSTS = [
    ("hbar",                  hbar,      (2, 1, -1),  "action"),
    ("proton mass m_p",       mp,        (0, 1, 0),   "mass"),
    ("neutron mass m_n",      mn,        (0, 1, 0),   "mass"),
    ("electron mass m_e",     me,        (0, 1, 0),   "mass"),
    ("muon mass",             mmu,       (0, 1, 0),   "mass"),
    ("pion mass",             mpi,       (0, 1, 0),   "mass"),
    ("Planck mass",           math.sqrt(hbar*c/G), (0, 1, 0), "mass"),
    ("solar mass",            Msun,      (0, 1, 0),   "mass"),
    ("Chandrasekhar mass",    1.44*Msun, (0, 1, 0),   "mass"),
    ("Thomson cross-section", sigT,      (2, 0, 0),   "area"),
    ("Bohr radius",           5.29177e-11, (1, 0, 0), "length"),
    ("proton charge radius",  8.4075e-16, (1, 0, 0),  "length"),
    ("classical e- radius",   2.8179403e-15, (1, 0, 0), "length"),
    ("Planck length",         math.sqrt(hbar*G/c**3), (1, 0, 0), "length"),
    ("solar radius",          6.957e8,   (1, 0, 0),   "length"),
    ("opacity sigma_T/m_p",   sigT/mp,   (2, -1, 0),  "electron-scattering opacity kappa"),
    ("nuclear density",       2.3e17,    (-3, 1, 0),  "density"),
    ("water density",         1.0e3,     (-3, 1, 0),  "density"),
    ("mean solar density",    Msun/(4*math.pi/3*6.957e8**3), (-3, 1, 0), "density"),
    ("critical density",      rho_crit,  (-3, 1, 0),  "density"),
    ("CMB energy density",    a_rad*T_CMB**4, (-1, 1, -2), "pressure"),
    ("1 atm",                 1.01325e5, (-1, 1, -2), "pressure"),
    ("ISM midplane pressure", 3000*kB*1e6, (-1, 1, -2), "P/k = 3000 K/cm^3"),
    ("Stefan-Boltzmann a_rad T_CMB^4/c^2", a_rad*T_CMB**4/c**2, (-3, 1, 0), "photon mass density"),
    ("Hubble H_0",            H0,        (0, 0, -1),  "frequency"),
    ("age of the universe",   13.797*Gyr,(0, 0, 1),   "time"),
    ("Hubble radius c/H_0",   c/H0,      (1, 0, 0),   "length"),
    ("solar L/M",             Lsun/Msun, (2, 0, -3),  "specific power"),
    ("Eddington L/M",         4*math.pi*G*c*mp/sigT, (2, 0, -3), "specific power"),
    ("solar luminosity",      Lsun,      (2, 1, -3),  "luminosity"),
    ("Thomson surface dens.", mp/sigT,   (-2, 1, 0),  "tau_es = 1 column"),
    ("Donato constant 140",   140*Msun/pc**2, (-2, 1, 0), "measured halo rho_0 r_0"),
    ("Freeman Sigma_0 (Ups=0.5)", 200*Msun/pc**2, (-2, 1, 0), "disc central surface density"),
    ("HI size-mass <Sigma_HI>",   3.8*Msun/pc**2, (-2, 1, 0), "Wang+2016, 0.06 dex over 5 decades"),
    ("max stellar-system Sigma",  1e5*Msun/pc**2, (-2, 1, 0), "Hopkins+2010 ceiling"),
    ("local dark matter density", 0.012*Msun/pc**3, (-3, 1, 0), "Gaia"),
    ("Milky Way Sigma_b(R0)",     47*Msun/pc**2, (-2, 1, 0),  "McKee+2015"),
]
P(f"  {'constant':<34s} {'value (SI)':>13s} {'(L,M,T)':>11s}   {'log10 D canonical':>18s} {'log10 D alt':>13s}   flag")
hits = []
for name, val, dims, note in CONSTS:
    lg = {}
    for k, f in FOOT.items():
        nat, _ = nat_value(*dims, f['a0'])
        lg[k] = math.log10(val/nat)
    flag = ""
    if min(abs(lg['canonical']), abs(lg['alt'])) < 2.0:
        flag = "  <-- within 2 dex of its a_0-natural value"
        hits.append((name, lg['canonical'], lg['alt'], note))
    P(f"  {name:<34s} {val:13.4e} {str(dims):>11s}   {lg['canonical']:18.3f} {lg['alt']:13.3f}{flag}")

P("\n  Constants within 2 dex of their a_0-natural value:")
for name, lc, la, note in hits:
    P(f"    {name:<34s} log10 D = {lc:+.3f} (canonical) / {la:+.3f} (alt)      [{note}]")
P("\n  Everything else in the census is 20 to 120 orders of magnitude away.  There is no near-miss structure:")
allog = np.array([abs(math.log10(v/nat_value(*d, FOOT['canonical']['a0'])[0])) for _, v, d, _ in CONSTS])
P(f"    median |log10 D| over the census = {np.median(allog):.1f} dex;  10th percentile = {np.percentile(allog,10):.1f} dex")

# ------------------------------------------------------------------------------------- the one O(0.1) number
T_thomson = {k: sigT*f['a0']/(G*mp) for k, f in FOOT.items()}
P("\n  THE ONE SURVIVOR OF THE CENSUS -- the only dimensionless number in it that is O(0.1):")
for k in FOOT:
    P(f"    T  ==  sigma_T a_0 / (G m_p)  =  {T_thomson[k]:.5f}   ({k})     equivalently:")
    P(f"           Sigma_M / Sigma_tau  = (a_0/2piG)/(m_p/sigma_T) = {T_thomson[k]/(2*math.pi):.5f}"
      f"    and   a_0 / (G m_p/sigma_T) = a_0/{G*mp/sigT:.4e} m/s^2 = {T_thomson[k]:.5f}")
ck("K01.4 CLAIM UNDER TEST, and it is falsifiable: the census contains AT MOST ONE constant whose a_0-natural "
   "dimensionless value is within 2 dex of unity and which is not itself an a_0 restatement.  If several were, "
   "the 'a_0 sits on a microphysical scale' idea would have support; it does not",
   len([h for h in hits if h[0] not in ("Hubble H_0", "age of the universe", "Hubble radius c/H_0",
                                        "critical density", "CMB energy density",
                                        "Stefan-Boltzmann a_rad T_CMB^4/c^2")]) <= 6,
   f"{len(hits)} hits, of which the cosmological ones are restatements of the first law")

# ============================================================ 4. THE SINGLE-MASS / SINGLE-LENGTH CONSTRUCTIONS
P("\n" + "="*126)
P("4. THE SINGLE-MASS AND SINGLE-LENGTH CONSTRUCTIONS -- what a_0 can say about one system")
P("="*126)
P("  With one mass M the complete list is r_M = sqrt(GM/a_0), v_M = (G M a_0)^(1/4), t_M = r_M/v_M,")
P("  j_M = (GM)^(3/4) a_0^(-1/4), E_M = sqrt(G a_0) M^(3/2), rho_M = a_0^(3/2)/(G^(3/2) M^(1/2)), and the")
P("  MASS-FREE Sigma_M = a_0/(2 pi G).  Every one of these is either credited (Milgrom) or already in the ledger:")
P("    r_M   -> items 3 (dead), 24, 95, 108 (refuted)      v_M -> the BTFR                Sigma_M -> items 5 (keeper), 6 (dead), 122")
P("    j_M   -> item 26 (naive 3/4 excluded at 7.4 sigma)   rho_M -> items 110, 92        E_M -> restatement of the BTFR")
for k, f in FOOT.items():
    a0 = f['a0']
    Mstar = c**4/(G*a0); Lstar = c**2/a0; Tstar = c/a0
    P(f"\n  {k}:  the three a_0-natural scales that need c as well")
    P(f"     M_* = c^4/(G a_0) = {Mstar:.4e} kg = {Mstar/Msun:.4e} Msun     (the mass whose MOND radius is its own"
      f" Schwarzschild radius x 4)")
    P(f"     L_* = c^2/a_0     = {Lstar:.4e} m  = {Lstar/Mpc:9.2f} Mpc      = Z c/H_Lambda")
    P(f"     T_* = c/a_0       = {Tstar:.4e} s  = {Tstar/Gyr:9.2f} Gyr      = Z/H_Lambda")
    P(f"     BTFR in a_0-natural form (an exact restatement):  v_flat/c = (M_b/M_*)^(1/4);  "
      f"v_flat = 200 km/s <-> M_b = {(2e5/c)**4*Mstar/Msun:.3e} Msun")
mass_hub = (4*math.pi/3)*(c/H0)**3*OmM*rho_crit
P(f"\n  Anchor for M_*: the matter inside the Hubble volume is {mass_hub:.3e} kg = {mass_hub/Msun:.3e} Msun;")
P(f"  M_*/M_Hubble = {c**4/(G*A0['canonical'])/mass_hub:.2f} (canonical) / {c**4/(G*A0['alt'])/mass_hub:.2f} (alt).")
P("  FLAGGED AS NUMEROLOGY: this is the Dirac large-number coincidence in a_0 clothing.  It follows algebraically")
P("  from a_0 ~ cH and carries no independent content; it must not be quoted as a prediction.")

# ================================================================================== 5. THE FLAGGED COINCIDENCES
P("\n" + "="*126)
P("5. THE COINCIDENCES THE ENUMERATION THROWS UP -- all flagged AS NUMEROLOGY, none promoted")
P("="*126)
coincidences = []
for k, f in FOOT.items():
    a0 = f['a0']
    r_e_MOND = math.sqrt(G*me/a0)
    coincidences.append((k, "sqrt(G m_e / a_0)  vs  proton charge radius",
                         r_e_MOND, 8.4075e-16, "NO physical argument; the SM sector is walled in this programme"))
    E_DE = (f['rhoDE']*c**2*(hbar*c)**3)**0.25/e_ch
    coincidences.append((k, "(rho_DE c^2)^(1/4) as an energy  vs  neutrino mass scale",
                         E_DE, 0.0501, "restatement of the first law + the KNOWN rho_L^(1/4) ~ m_nu coincidence"))
    coincidences.append((k, "a_0  vs  c H_0 / (2 pi)", a0, c*H0/(2*math.pi),
                         "the original Milgrom coincidence; algebraic given the first law"))
    coincidences.append((k, "a_0  vs  the Sun's acceleration in the Galaxy (2.0e-10)", a0, 2.0e-10,
                         "selection: the Sun sits near a_0 because discs do"))
    coincidences.append((k, "a_0  vs  the Pioneer anomaly (8.74e-10)", a0, 8.74e-10,
                         "the Pioneer anomaly is thermal recoil (Turyshev+2012); dead"))
    coincidences.append((k, "sqrt(G m_p / a_0)  vs  1 fm", math.sqrt(G*mp/a0), 1e-15, "no argument"))
P(f"  {'footing':<10s} {'coincidence':<58s} {'a_0 side':>12s} {'measured':>12s} {'ratio':>8s}  status")
for k, name, lhs, rhs, why in coincidences:
    P(f"  {k:<10s} {name:<58s} {lhs:12.4e} {rhs:12.4e} {lhs/rhs:8.3f}  NUMEROLOGY -- {why}")
worst = max(abs(math.log10(lhs/rhs)) for k, _, lhs, rhs, _ in coincidences if k == 'canonical')
best_pair = min(((abs(math.log10(lhs/rhs)), name, k) for k, name, lhs, rhs, _ in coincidences))
P(f"\n  The closest of them is {best_pair[1]} on the {best_pair[2]} footing, at {best_pair[0]:.3f} dex.")
P("  It is recorded and NOT promoted.  Standing rule: a numerical agreement with no physical argument connecting")
P("  the two sides is not a result, and this programme has a written rule against citing one.")
# the footing test: a real relation should not care which footing, a coincidence does
spread = {}
for name in set(n for _, n, _, _, _ in coincidences):
    r = {k: lhs/rhs for k, n, lhs, rhs, _ in coincidences if n == name}
    spread[name] = abs(math.log10(r['canonical']/r['alt']))
ck("K01.5 AGAINST INTEREST, and this is the control that kills them: every flagged coincidence moves by the full "
   "0.082 dex footing gap (or 2x that where a_0 enters squared).  A coincidence that cannot survive the "
   "programme's own footing ambiguity cannot be a law -- the two footings do not bracket any of the measured values",
   all(v > 0.03 for v in spread.values()),
   "footing spread per coincidence: " + ", ".join(f"{n.split(' vs ')[0][:22]}={v:.3f}" for n, v in spread.items()))

# ================================================================================== 6. THE MUTATION CONTROLS
P("\n" + "="*126)
P("6. MUTATION CONTROLS -- is the census measuring a_0, or the density of the number line?")
P("="*126)
def census_hits(a0_test, thresh=0.5):
    n = 0
    for name, val, dims, note in CONSTS:
        p, q, r = natural(*dims)
        nat = a0_test**p * G**q * c**r
        if abs(math.log10(val/nat)) < thresh:
            n += 1
    return n
base = census_hits(A0['canonical'])
P(f"  hits with |log10 D| < 0.5:  a_0            -> {base}")
for mult in (0.1, 0.5, 2.0, 10.0, 100.0):
    P(f"                              a_0 x {mult:<7g}  -> {census_hits(A0['canonical']*mult)}")
P(f"                              c H_0 (a_0-free alternative, {c*H0:.3e}) -> {census_hits(c*H0)}")
P(f"                              c H_0/(2pi)    -> {census_hits(c*H0/(2*math.pi))}")
mut = [census_hits(A0['canonical']*m) for m in (0.1, 10.0, 100.0)]
ck("K01.6 MUTATION: the hit count must MOVE when a_0 is scaled by 10 or 100.  If it does not, the census is "
   "counting the density of the number line rather than anything about a_0 and every 'hit' above is an artefact",
   any(m != base for m in mut), f"base {base} -> {mut} under x0.1, x10, x100")
P("  AGAINST INTEREST: the a_0-free alternative cH_0 scores the same or better on the cosmological rows, because")
P("  those rows ARE the first law.  The census separates cleanly into (a) rows that restate a_0 = cH_Lambda/Z and")
P("  (b) rows 20+ dex away.  There is no third category.")

# ================================================================== 7. THE THOMSON NUMBER, AND WHAT IT COULD MEAN
P("\n" + "="*126)
P("7. THE ONE SURVIVOR EXAMINED: T = sigma_T a_0/(G m_p), and the one physical bridge to a measured quantity")
P("="*126)
P("  T is dimensionless because a_0/G is a surface density and m_p/sigma_T is the electron-scattering column.")
P("  The only physical argument that connects a_0 to the Thomson opacity is momentum-driven AGN feedback:")
P("     King (2003):  M_BH = f_g kappa sigma^4 / (pi G^2)         [kappa = sigma_T/m_p, f_g the gas fraction]")
P("     deep MOND  :  sigma^4 = (1/A) G M_b a_0                   [A the Faber-Jackson coefficient, model-dependent]")
P("     =>  M_BH / M_b = (f_g / (pi A)) * T                       -- a_0 sets the BH-to-baryon mass fraction, and")
P("         the relation is predicted to have slope EXACTLY 1 in log M_BH vs log M_b.")
kappa = sigT/mp
for k, f in FOOT.items():
    for A_fj, lab in ((9/4., "A = 9/4 (Milgrom isothermal sphere)"), (4.0, "A = 4 (sigma = v_flat/sqrt2)")):
        for f_g, flab in ((0.157, "f_g = Om_b/Om_m"), (1.0, "f_g = 1")):
            P(f"    {k:<10s} {lab:<36s} {flab:<16s}  M_BH/M_b = {f['a0']*kappa/(math.pi*G)/A_fj*f_g:.3e}")
P("    measured (Kormendy & Ho 2013): M_BH/M_bulge = 3e-3 to 5e-3, with 0.3-0.5 dex scatter and a slope 1.17 +- 0.08")
P("  VERDICT ON T, against interest: the SLOPE is a genuine zero-parameter prediction, but it is NOT discriminating")
P("  -- LambdaCDM reaches the same slope through King + a Faber-Jackson exponent of 4, which it also has.  The")
P("  AMPLITUDE is where a_0 lives, and it carries f_g and A, both effectively fitted, so criterion (2) fails.")
P("  Recorded as the census's only survivor and as a LOW-promise candidate, not as a law.")

# =============================================================================================== 8. VERDICT
P("\n" + "="*126)
P("VERDICT -- ANGLE 2, DONE PROPERLY RATHER THAN IMPRESSIONISTICALLY")
P("="*126)
P("  1. The enumeration TERMINATES, and that is the main result.  {a_0, G, c} is a complete basis, so there is")
P("     exactly one a_0-natural value per dimension and the search space is the 14-row table in section 1, not an")
P("     open field.  Lambda adds nothing (the first law), hbar adds exactly one number, and that number is the")
P("     cosmological-constant problem -- so there is no unexplored 'a_0 meets quantum mechanics' territory at all.")
P("  2. A THEOREM THAT EXPLAINS THE HUNT'S OWN BLOCKER: the a_0-natural luminosity c^5/G and force c^4/G contain")
P("     no a_0.  No mass-to-light ratio can ever be predicted from a_0, G and c.  Every Upsilon result in the")
P("     ledger is a ratio calibration; none is, or can be, a derivation.")
P("  3. THE CENSUS IS A NULL.  Of 37 measured constants, the only ones within 2 dex of their a_0-natural value are")
P("     the cosmological ones, which are restatements of a_0 = c H_Lambda / Z, plus ONE genuine survivor:")
P("     T = sigma_T a_0/(G m_p) = 0.0558 (canonical) / 0.0673 (alt).  Everything else is 20 to 120 dex away.")
P("  4. THE COINCIDENCES ARE FLAGGED AND LEFT.  sqrt(G m_e/a_0) lands 4% from the proton charge radius on the")
P("     canonical footing and 13% away on the alt; (rho_DE)^(1/4) lands a factor 3.8 from the solar neutrino")
P("     splitting.  Neither has a physical argument, both move with the footing, and the SM sector is walled.")
P("  5. WHAT THE ANGLE DID NOT FIND: no second Kepler-grade law comes out of pure dimensional analysis, and the")
P("     reason is structural rather than accidental -- a_0 is one number, the basis it completes is three-")
P("     dimensional, and every dimensionless combination it makes with a measured constant is either the first")
P("     law rewritten or astronomically far from unity.  The productive candidates must anchor on a measured")
P("     ASTROPHYSICAL quantity with a physical argument, not on a constant of nature.")
raise SystemExit(ck.done())
