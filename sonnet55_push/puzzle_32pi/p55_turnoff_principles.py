"""p55: can a natural principle fix the turn-off y_t WITHOUT inserting 32 pi?  alpha = 1 (p54): L(y_t) := Lambda c^4/a0^2 = int (nu_fix - 1) y dy,
turn-off shape 1/(1+(y/y_t)^k).  A principle "works" only if it yields y_t with L(y_t) = 32 pi (kappa = 1/2) or inside the data window
kappa = sqrt(8 pi / L) in [0.44, 0.56] (gas points 8.3e-11 .. MeerKAT 1.05e-10), AND y_t >= 20 (SPARC, p36), y_t <= 7.7e5 (Mars, p35).
P1 self-reflection (turn-off energy = vacuum energy, sqrt(a0 g_t) = c^2 sqrt(Lambda), i.e. y_t = L(y_t)): needs leading slope c_k = (pi/2k)/sin(pi/k) >= 1.
P2 Unruh wavelength c^2/g_t equals a cosmic length (dS radius sqrt(3/Lambda), a0 horizon r* = c^2/2a0): y_t = sqrt(L/3) or 2.
P3 self-consistent P2: y_t = sqrt(L(y_t)/3) solved jointly.
Plus the forecast: if a turn-off exists at y_t, the Sun's anomalous acceleration is (a0/2)/(1+(y/y_t)^2) (vs a0/2 for the exact law).
Run: python3 p55_turnoff_principles.py | MUTATE=1 uses c_k = pi/k (wrong slope; check S must fail)
"""
import os, sys, math
from mpmath import mp, quad, sqrt, inf, pi, sin, findroot
MUTATE = os.environ.get("MUTATE") == "1"
mp.dps = 20
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
def L(yt, k=2): return quad(lambda y: (sqrt(1 + 1 / y) - 1) / (1 + (y / yt)**k) * y, [0, 1, yt, 10 * yt, inf])
def ck(k): return pi / k if MUTATE else (pi / (2 * k)) / sin(pi / k)
for k in (2, 3, 4):
    print(f"   k={k}: slope c_k = {mp.nstr(ck(k),5)}, numeric L(1e4)/1e4 = {mp.nstr(L(1e4,k)/1e4,5)}")
check("S leading slope L ~ c_k y_t with c_k = (pi/2k)/sin(pi/k) (numeric agreement < 0.2% at y_t = 1e4, k = 2,3,4)", all(abs(L(1e4, k) / 1e4 / ck(k) - 1) < 2e-3 for k in (2, 3, 4)))
kap = lambda Lv: math.sqrt(8 * math.pi / float(Lv))
rows = []
# P1
p1 = [k for k in (2, 3, 4, 6, 10) if ck(k) >= 1]
print(f"   P1 y_t = L(y_t): slope >= 1 only for k < 1.657 (pi/k = 1.8955); among k = 2,3,4,6,10 roots exist for {p1}")
rows.append(("P1 self-reflection", len(p1) > 0))
# P2
for name, yt in (("P2a dS radius", None), ("P2b r*", 2.0)):
    if yt is None:
        yt = math.sqrt(32 * math.pi / 3)   # on the kappa = 1/2 footing (non-self-consistent version)
    Lv = L(yt)
    print(f"   {name}: y_t = {yt:.3f} -> L = {mp.nstr(Lv,5)}, kappa = {kap(Lv):.3f}; SPARC needs y_t >= 20")
    rows.append((name, yt >= 20 and 0.44 <= kap(Lv) <= 0.56))
# P3 joint
f = lambda t: t - sqrt(L(t) / 3)
try:
    t3 = findroot(f, 2.0); Lv = L(t3)
    print(f"   P3 joint y_t = sqrt(L/3): y_t = {mp.nstr(t3,5)}, L = {mp.nstr(Lv,5)}, kappa = {kap(Lv):.3f}")
    rows.append(("P3 joint", float(t3) >= 20 and 0.44 <= kap(Lv) <= 0.56))
except Exception as e:
    print("   P3 no root", e); rows.append(("P3 joint", False))
for n, ok in rows: print(f"   {n}: {'WORKS' if ok else 'fails'}")
check("V verdict: none of P1-P3 yields an allowed y_t (recorded as the honest negative)", not any(ok for _, ok in rows))
# forecast
a0, yt = 9.3603e-11, 128.915; GM, AU = 1.32712440018e20, 1.495978707e11
for r in (100, 300, 700, 1500):
    gN = GM / (r * AU)**2; y = gN / a0
    print(f"   Sun at {r:5d} AU: y = {y:8.1f}, anomaly exact a0/2 = {a0/2:.2e}, with turn-off {a0/2/(1+(y/yt)**2):.2e} m/s^2")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
