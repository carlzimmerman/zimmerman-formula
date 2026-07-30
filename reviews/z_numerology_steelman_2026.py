"""
STEELMAN then TEST.  Two fair objections to the crude density estimate, both answered.

OBJ 1: "An arbitrary-closed-form grammar is an unfair prior. Z has a SPECIFIC form,
        sqrt(a*pi/b).  Within that form the match is tight (only 2 hits)."
   -> TEST: is 2 hits special to Z, or does ANY target admit ~2 hits in that family?

OBJ 2: "The right prior is not arbitrary integers but the primitives that actually
        occur in GR: 8pi (Einstein), 4pi/3 (ball volume), 4pi (area), 1/4 (Bek-Hawking),
        2pi (Unruh), 3 (Friedmann), 2 (Schwarzschild)."
   -> TEST: how dense is THAT grammar near Z?

Plus: the numerical ledger (framework a0 vs Milgrom 2cH_L vs folklore cH/2pi vs cH0/7).
"""
import math, random, bisect
from fractions import Fraction
PI = math.pi
Z  = math.sqrt(32*PI/3)
random.seed(1)

# ============ OBJ 1: is the sqrt(a*pi/b) family tight for ANY target? ============
print("="*74)
print("OBJ 1  sub-family sqrt(a*pi/b), a<=40 b<=12 : hits within 1% of a target")
fam = []
seenr = set()
for a in range(1, 41):
    for b in range(1, 13):
        fr = Fraction(a, b)
        if fr in seenr: continue
        seenr.add(fr)
        fam.append(math.sqrt(a*PI/b))
fam.sort()
print(f"       family size (distinct values, a<=40 b<=12): {len(fam)}")
def nhits(t, arr, tol):
    i = bisect.bisect_left(arr, t*(1-tol)); j = bisect.bisect_right(arr, t*(1+tol))
    return j-i
print(f"       hits within 1% of Z={Z:.6f}                : {nhits(Z,fam,0.01)}")
# distribution of hit counts for random log-uniform targets in the same decade
lo, hi = math.log(4.0), math.log(9.0)
cnts = [nhits(math.exp(random.uniform(lo,hi)), fam, 0.01) for _ in range(200000)]
mean = sum(cnts)/len(cnts)
frac_ge1 = sum(1 for c in cnts if c >= 1)/len(cnts)
frac_ge2 = sum(1 for c in cnts if c >= 2)/len(cnts)
print(f"       for RANDOM targets in [4,9]: mean hits {mean:.2f}, "
      f"P(>=1 hit)={frac_ge1*100:.1f}%, P(>=2 hits)={frac_ge2*100:.1f}%")
print("       => Z's '2 hits' is the MODAL outcome for an arbitrary number. Not special.")

# ============ OBJ 2: the GR-primitive grammar ============
print("="*74)
print("OBJ 2  grammar restricted to primitives that genuinely occur in GR/cosmology")
prim = {
    "8pi":      8*PI,       # Einstein eq / rho_Lambda = Lambda c^2/8piG
    "4pi/3":    4*PI/3,     # volume of unit 3-ball  (mass inside a sphere)
    "4pi":      4*PI,       # area of unit 2-sphere
    "2pi":      2*PI,       # Unruh / Hawking  T = a/2pi
    "pi":       PI,
    "1/4":      0.25,       # Bekenstein-Hawking S = A/4G
    "1/2":      0.5,        # kinetic 1/2, Milgrom Taylor 1/2
    "2":        2.0,        # Schwarzschild r_s = 2m ; Komar rho+3p = -2rho
    "3":        3.0,        # Friedmann 3 / spatial dimension
    "4":        4.0, "6":6.0, "8":8.0, "16":16.0, "32":32.0, "9":9.0, "12":12.0,
}
vals = {}
for n,v in prim.items(): vals.setdefault(round(v/1e-12), (v,1,n))
def add(v, c, e, store):
    if not math.isfinite(v) or not (0.5 <= v <= 200): return
    k = round(v/1e-12)
    if k not in store: store[k] = (v,c,e)
cur = dict(vals)
for depth in range(2, 5):
    new = {}
    for k,(v,c,e) in cur.items():
        add(math.sqrt(v), c+1, f"sqrt({e})", new)
        add(v*v, c+1, f"({e})^2", new)
        add(1/v, c+1, f"1/({e})", new)
    for k1,(v1,c1,e1) in cur.items():
        for n2,v2 in prim.items():
            for op,f in (("*",lambda x,y:x*y),("/",lambda x,y:x/y),("+",lambda x,y:x+y),("-",lambda x,y:x-y)):
                add(f(v1,v2), c1+1, f"({e1}{op}{n2})", new)
    for k,val in new.items():
        if k not in vals: vals[k] = val
    cur = new
band = sorted(v for v,c,e in vals.values() if 4.0 <= v <= 9.0)
hits = sorted(((v,c,e) for v,c,e in vals.values() if abs(v/Z-1) <= 0.01), key=lambda t:t[1])
print(f"       distinct values built from GR primitives (depth<=4): {len(vals)}  ({len(band)} in [4,9])")
print(f"       within 1% of Z: {len(hits)}")
for v,c,e in hits[:12]:
    print(f"         {v:.6f} ({100*(v/Z-1):+.3f}%)  {e}")
cov = sum(1 for _ in range(50000)
          if nhits(math.exp(random.uniform(math.log(4),math.log(9))), band, 0.01) >= 1)/50000
print(f"       coverage of arbitrary targets in [4,9] within 1%: {cov*100:.1f}%")
print("       => even the 'respectable' GR-primitive prior saturates: Z is not picked out.")

# ============ the exact decomposition (this is the real (a) answer) ============
print("="*74)
print("EXACT DECOMPOSITION of Z  (sympy-checkable, no fitting)")
import sympy as sp
kappa = sp.Rational(1,2); pi = sp.pi
Zsym = sp.sqrt(8*pi/3)/kappa
print(f"       Z  =  sqrt(8pi/3)/kappa  with kappa=1/2  ->  {sp.simplify(Zsym)}  = {float(Zsym):.6f}")
print(f"       Z^2 = 32pi/3 = (1/kappa^2) * (8pi/3) = 4 * (8pi/3)          [exact: {sp.simplify(Zsym**2)}]")
print(f"       and 8pi/3 = 2 * (4pi/3):   2 = the 1/2 v^2 kinetic factor in the")
print(f"       Newtonian Friedmann derivation (1/2 Rdot^2 = GM/R),")
print(f"       4pi/3 = volume of the unit 3-ball, because M = (4pi/3) R^3 rho.")
print(f"       So Z^2 = 8 * V_unit-3-ball with 8 = 4 (=1/kappa^2) * 2 (kinetic).")
print(f"       check 32pi/3 == 8*(4pi/3): {sp.simplify(sp.Rational(32,1)*pi/3 - 8*(4*pi/3)) == 0}")
# and the independent GR home of 32pi/3
print("       INDEPENDENT occurrence: a Schwarzschild horizon of radius r_s=2m encloses")
print("       coordinate 3-volume (4pi/3)(2m)^3 = (32pi/3) m^3, hence the textbook mean")
print("       density rho_BH = 3c^6/(32 pi G^3 M^2).  Same integers, 8 = 2^3 from r_s=2m.")
print("       -> a DIFFERENT reason for the same 8; shared ancestor is 'ball volume', not a link.")

# ============ numerical ledger ============
print("="*74)
print("NUMERICAL LEDGER (Planck 2018: H0=67.4 km/s/Mpc, Omega_L=0.6847)")
c = 2.99792458e8; Mpc = 3.0856775814913673e22
H0 = 67.4e3/Mpc; OmL = 0.6847; HL = H0*math.sqrt(OmL)
cH0, cHL = c*H0, c*HL
a0_fw = cHL/Z
rows = [
    ("framework  cH_L / Z        (kappa=1/2)", a0_fw),
    ("Milgrom99  2 cH_L          (forced by dS-Unruh)", 2*cHL),
    ("folklore   cH_L / 2pi", cHL/(2*PI)),
    ("folklore   cH0 / 2pi", cH0/(2*PI)),
    ("           cH0 / 7        (an INTEGER)", cH0/7),
    ("           cH_L / 6", cHL/6),
    ("empirical  standard-MOND a0 (RAR, McGaugh nu)", 1.20e-10),
]
for nm,v in rows:
    print(f"       {nm:46s} = {v:.4e}   ({100*(v/a0_fw-1):+7.1f}% vs framework)")
print(f"       Milgrom/framework ratio = {2*cHL/a0_fw:.4f}  = 2Z = {2*Z:.4f}   (exactly 2Z)")
print(f"       decomposed: 4 (=2 / (1/2), the normalisation) x sqrt(8pi/3)={math.sqrt(8*PI/3):.4f}"
      f" (the scale swap cH -> c sqrt(G rho)) = {4*math.sqrt(8*PI/3):.4f}")
print(f"       Z / 2pi = {Z/(2*PI):.4f}  -> Z is within {abs(100*(Z/(2*PI)-1)):.1f}% of 2pi,")
print(f"       i.e. INSIDE a0's own ~10-20% systematic error bar.")
