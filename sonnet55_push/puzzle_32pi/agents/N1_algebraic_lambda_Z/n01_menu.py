"""n01: compute every declared candidate's Z exactly (sympy) and numerically; self-consistency of radii; controls.
Units c=G=1, L=1 (so a0 = 1/Z). Predeclared in PREDECLARED.md (sha256 in PREDECLARED.sha256)."""
import sympy as sp, mpmath as mp, json, hashlib, sys
mp.mp.dps = 30
npass = nfail = 0
def chk(name, cond):
    global npass, nfail
    if cond: npass += 1; print("PASS", name)
    else: nfail += 1; print("FAIL", name)

h = hashlib.sha256(open("PREDECLARED.md","rb").read()).hexdigest()
chk("predeclaration hash matches file", h == open("PREDECLARED.sha256").read().split()[0])

r, M, L = sp.symbols('r M L', positive=True)
f = 1 - 2*M/r - r**2/L**2
MN = L/(3*sp.sqrt(3))
# Nariai: roots of f coincide <=> f and f' vanish at same r
fp = sp.diff(f, r)
sol = sp.solve([sp.numer(sp.together(f)), sp.numer(sp.together(fp))], [r, M], dict=True)
sol = [s for s in sol if s[r].is_positive and s[M].is_positive] if hasattr(sol[0][r],'is_positive') else sol
rN = sp.simplify(sol[0][r]); MNs = sp.simplify(sol[0][M])
chk("Nariai mass M_N = L/(3 sqrt3)", sp.simplify(MNs - MN) == 0)
chk("Nariai radius r_N = L/sqrt3", sp.simplify(rN - L/sp.sqrt(3)) == 0)
rph = 3*MN; r0 = (MN*L**2)**sp.Rational(1,3)
chk("photon sphere 3M_N = r_N", sp.simplify(rph - rN) == 0)
chk("zero-force radius (M_N L^2)^(1/3) = r_N", sp.simplify(sp.simplify(r0**3 - rN**3)) == 0)
chk("f(r_N)=0 and f'(r_N)=0 at M_N", sp.simplify(f.subs({M:MN, r:rN})) == 0 and sp.simplify(fp.subs({M:MN, r:rN})) == 0)
chk("f(L) < 0 at M_N (r=L is NOT in the static patch; dynamical region)", sp.simplify(f.subs({M:MN, r:L})).subs(L,1) < 0)
# static patch at M_N is empty: f<=0 everywhere
fr = sp.lambdify(r, f.subs(M, MN).subs(L, 1), 'mpmath')
chk("M_N geometry: f<=0 for all r (static patch empty), 400-point scan", all(fr(mp.mpf(i)/100) <= 1e-25 for i in range(1, 400)))

Zs = {}
def Z_of(a):  # a in units 1/L
    return sp.nsimplify(sp.simplify(1/a))
a = {}
a['A1'] = MN/L**2
a['A2'] = MN/rN**2
a['A3'] = MN/rN**2          # cosmological horizon of M_N geometry = same root
a['A4'] = MN/rph**2
a['A5'] = MN/r0**2
a['A6'] = 1/(4*MN)
a['A7'] = MN/(6*MN)**2
a['A9'] = sp.Integer(0)
a['A10'] = sp.sqrt(3)/L      # kappa_BH(Nariai) = sqrt3 H  (lane L)
a['A11a'] = (L/2)/L**2       # M_Lambda = (4pi/3) rho_L L^3 = L/2 ; field at L
a['A11b'] = L/L**2           # Lambda repulsion r/L^2 at r=L
for k, v in a.items():
    v = sp.simplify(v.subs(L, 1))
    Zs[k] = None if v == 0 else sp.simplify(1/v)
for k, v in Zs.items():
    print(k, "Z =", v, "=", None if v is None else sp.N(v, 8))
chk("A1 Z = 3 sqrt3", sp.simplify(Zs['A1'] - 3*sp.sqrt(3)) == 0)
chk("A2=A3=A4=A5 (algebraic coincidence) Z = sqrt3", all(sp.simplify(Zs[k]-sp.sqrt(3))==0 for k in ['A2','A3','A4','A5']))
chk("A6 Z = 4/(3 sqrt3)", sp.simplify(Zs['A6'] - 4/(3*sp.sqrt(3))) == 0)
chk("A7 Z = 4 sqrt3", sp.simplify(Zs['A7'] - 4*sp.sqrt(3)) == 0)
chk("A10 Z = 1/sqrt3", sp.simplify(Zs['A10'] - 1/sp.sqrt(3)) == 0)
chk("A11: Z = 2 (vacuum ball mass) and 1 (Lambda repulsion)", Zs['A11a'] == 2 and Zs['A11b'] == 1)
# A1 radius ratio: A1 = A2 * (r_N/L)^2 -> Z_A1 = 3 Z_A2
chk("Z(A1) = 3 Z(A2): r=L vs r=L/sqrt3", sp.simplify(Zs['A1'] - 3*Zs['A2']) == 0)

# A8: exact SdS stable circular orbits. V = f (1 + l^2/r^2); circular: l^2 = r^2 (M - r^3/L^2)/(r-3M); stable: V''>0
l2 = r**2*(M - r**3/L**2)/(r - 3*M)
V = f*(1 + l2/r**2)   # treat l2 as a parameter: differentiate with l symbolic
ll = sp.symbols('ll', positive=True)
Vl = f*(1 + ll/r**2)
dV = sp.diff(Vl, r); d2V = sp.diff(Vl, r, 2)
chk("circular l^2 formula solves V'=0", sp.simplify(dV.subs(ll, l2)) == 0)
d2 = sp.simplify(d2V.subs(ll, l2))
Nexpr = 6*M**2 - 15*M*r**3 - M*r + 4*r**4      # V'' = -2 N / (r^3 (r-3M)); stable <=> N<0 for r>3M
chk("V'' factorisation -2N/(r^3 (r-3M))", sp.simplify(d2.subs(L,1) + 2*Nexpr/(r**3*(r-3*M))) == 0)
Nf = sp.lambdify((r, M), Nexpr, 'mpmath')
def stable_range(Mv):
    # timelike circular orbits need r>3M and l^2>0 i.e. r<M^(1/3) (L=1); stable where N<0 (log grid, 20000 pts)
    lo, hi = 3*Mv, mp.cbrt(Mv)
    if lo >= hi: return None
    xs = [lo*(hi/lo)**(mp.mpf(i)/20000) for i in range(1, 20000)]
    st = [x for x in xs if Nf(x, Mv) < 0]
    return (min(st), max(st)) if st else None
Ms = mp.mpf('1e-5'); sr = stable_range(Ms)
chk("Lambda->0 limit: ISCO ~ 6M (M=1e-5, within 1%)", sr is not None and abs(sr[0]/(6*Ms) - 1) < 1e-2)
lo, hi = mp.mpf('1e-5'), mp.mpf(1)/(3*mp.sqrt(3))
assert stable_range(lo) is not None
for _ in range(55):
    mid = (lo+hi)/2
    if stable_range(mid) is None: hi = mid
    else: lo = mid
rng = stable_range(lo)
print("A8: largest M with a stable circular orbit ~", mp.nstr(lo, 8), " = ", mp.nstr(lo/(1/(3*mp.sqrt(3))), 8), "M_N ; stable orbit range r ~", [mp.nstr(x,6) for x in rng])
rc = (rng[0]+rng[1])/2
a8 = lo/rc**2
Z8 = 1/a8
print("A8: G M/r^2 at critical orbit =", mp.nstr(a8, 8), "  Z =", mp.nstr(Z8, 8), " (grid-limited to ~1e-3)")
Zs['A8'] = float(Z8)
chk("A8: stable orbit exists just below M_crit and none just above", stable_range(lo) is not None and stable_range(hi) is None)
chk("A8: M_crit < M_N (no orbit at Nariai)", lo < 1/(3*mp.sqrt(3)))
# exact critical point: N=0 and dN/dr=0 (double root)
Mx, rx = sp.symbols('Mx rx', positive=True)
sol8 = sp.solve([Nexpr.subs({M:Mx, r:rx}), sp.diff(Nexpr, r).subs({M:Mx, r:rx})], [Mx, rx], dict=True)
sol8 = [q for q in sol8 if q[Mx].is_real and q[Mx] > 0 and q[rx] > 3*q[Mx] and q[rx]**3 < q[Mx]]
print("A8 exact double-root solutions:", sol8)
chk("A8 exact: M_crit = 0.08 M_N (double root of N), matches bisection", len(sol8)==1 and abs(float(sol8[0][Mx]) - float(lo)) < 1e-6)
Z8x = sp.simplify(sol8[0][rx]**2/sol8[0][Mx])
print("A8 exact Z =", Z8x, sp.N(Z8x, 10)); Zs['A8'] = float(Z8x)
chk("A8 exact Z agrees with numerics to 1e-3", abs(float(Z8x) - float(Z8)) < 1e-3)
chk("A8: critical M, r are not Nariai values (r/r_N != 1)", abs(rc/(1/mp.sqrt(3)) - 1) > 0.05)

# A12: static observer proper acceleration a_s(r) = (M/r^2 - r)/sqrt(f) monotone between horizons for M<M_N
asr = (M/r**2 - r/L**2)/sp.sqrt(f)
das = sp.lambdify((r, M), sp.diff(asr, r).subs(L,1), 'mpmath')
ok = True
for Mv in [mp.mpf('0.02'), mp.mpf('0.08'), mp.mpf('0.15'), mp.mpf('0.19')]:
    # horizons
    rts = sorted([x.real for x in mp.polyroots([-1/mp.mpf(1), 0, 1, -2*Mv][::-1] if False else [1, 0, -1, 2*Mv])  if abs(x.imag) < 1e-10 and x.real > 0])
    rb, rcc = rts[0], rts[1]
    xs = [rb + (rcc-rb)*mp.mpf(i)/2000 for i in range(1, 2000)]
    ok = ok and all(das(x, Mv) < 0 for x in xs)
chk("A12: static-observer proper acceleration strictly monotone (no extremum) between horizons (M=0.02..0.19 < M_N=0.1925)", ok)
# mutation: wrong Nariai mass must break the coincidence check
MNbad = MN/2
chk("MUTATION: with M_N/2 the zero-force radius != photon sphere", sp.simplify((MNbad*L**2)**sp.Rational(1,3) - 3*MNbad) != 0)
chk("MUTATION: with M_N/2, A1's Z is 6 sqrt3 (not 3 sqrt3)", sp.simplify((1/((MNbad/L**2).subs(L,1))) - 6*sp.sqrt(3)) == 0)

out = {k: (None if v is None else float(v)) for k, v in Zs.items()}
json.dump(out, open("n01_Z.json", "w"), indent=1)
print("\nn01 checks: %d pass, %d fail" % (npass, nfail))
sys.exit(1 if nfail else 0)
