"""p21: BIMOND's vacuum term vs Lambda = 32 pi a0^2 (c = 1).  Source: Milgrom, PRD 80 123536 (2009), arXiv:0912.0790v2 (PDF read 2026-10-04,
sha256 067e8560dd15e78be6dd93333930a03e41dc6176142ceb1e91fc966875360027; not vendored).
 - action eq (15) [alpha + beta = 0, beta = 1]; vacuum term eq (24): Lambda_m = -(1/2kappa)[kappa f(kappa)]' a0^2 M;  f(1) = 1 is the only normalisation
   stated (f'(1) is not fixed); at kappa = 1:  Lambda = -(1/2)(1 + f'(1)) a0^2 M(0).
 - NR limit eq (3): Laplacian phi = div[(1 + M') grad phi*], phi* Newtonian, so g = (1 + M') g_N:  M'(z) = nu(sqrt z) - 1, z = (g_N/a0)^2;
   M'(z) -> 0 at large z gives Newton. Normalising M(inf) = 0 (no vacuum constant in strong fields, as lane K's I2):
   M(0) = -I_nu,  I_nu = int_0^inf (nu(sqrt z) - 1) dz = int_0^inf 2y (nu(y) - 1) dy  >  0  ->  Lambda > 0 automatically (de Sitter).
 - symmetric subclass eq (86)-(87): Lambda = -a0^2 Mbar(0), M = (alpha + beta) Mbar (another free normalisation).
Puzzle: Lambda = 32 pi a0^2  <=>  (1 + f'(1)) I_nu = 64 pi = 201.06 ; with the minimal f = 1 (f'(1) = 0): I_nu = 64 pi.
Run: python3 p21_bimond_vacuum.py  |  MUTATE=1: use nu - 1 -> (nu - 1)/2 for RAR (check B must fail)
"""
import os, sys, math
import numpy as np
from scipy.integrate import quad
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
T = 64 * math.pi
nus = {
 "framework / Milgrom-1999  nu = sqrt(1 + 1/y)": lambda y: math.sqrt(1 + 1 / y),
 "simple  nu = 1/2 + sqrt(1/4 + 1/y)":           lambda y: 0.5 + math.sqrt(0.25 + 1 / y),
 "standard  nu^2 = (1 + sqrt(1 + 4/y^2))/2":     lambda y: math.sqrt((1 + math.sqrt(1 + 4 / y**2)) / 2),
 "RAR (McGaugh)  nu = 1/(1 - exp(-sqrt y))":     lambda y: 1 / (-math.expm1(-math.sqrt(y))),
}
def I(nu, ymax):
    fac = 0.5 if (MUTATE and "RAR" in name) else 1.0
    g = lambda y: 2 * y * (nu(y) - 1) * fac
    return quad(g, 0, min(ymax, 1.0), limit=400)[0] + (quad(g, 1.0, ymax, limit=800)[0] if ymax > 1 else 0)
out = {}
for name, nu in nus.items():
    vals = [I(nu, Y) for Y in (1e2, 1e3, 1e4)]
    out[name] = vals
    conv = abs(vals[2] - vals[1]) < 1e-6 * max(1, abs(vals[2]))
    print(f"   {name:46s} I(y<=1e2, 1e3, 1e4) = {vals[0]:10.3f} {vals[1]:10.3f} {vals[2]:12.3f}  {'CONVERGED' if conv else 'DIVERGES'}"
          + (f"  -> Lambda/a0^2 (f=1) = {vals[2]/2:.3f}; needed 32 pi = {32*math.pi:.3f}; factor {T/vals[2]:.2f}" if conv else ""))
fw = out["framework / Milgrom-1999  nu = sqrt(1 + 1/y)"]
check("A the framework kernel's integral DIVERGES (grows ~ linearly with the cutoff): BIMOND gives no finite Lambda from it without a cutoff",
      fw[2] / fw[1] > 5 and fw[1] / fw[0] > 5)
rar = out["RAR (McGaugh)  nu = 1/(1 - exp(-sqrt y))"]
check(f"B the RAR kernel converges: I = {rar[2]:.4f} (= lane K's independent AQUAL value c = 25.976), Lambda = {rar[2]/2:.3f} a0^2 with f = 1 -- {T/rar[2]:.2f}x short of 32 pi a0^2",
      abs(rar[2] - rar[1]) < 1e-6 * rar[2] and abs(rar[2] - 25.976) < 1e-3)
# what the framework kernel needs: the cutoff y_c where I = 64 pi; and f'(1) for RAR
yc = None
lo, hi = 1.0, 1e4
for _ in range(80):
    mid = math.sqrt(lo * hi)
    if I(nus["framework / Milgrom-1999  nu = sqrt(1 + 1/y)"], mid) < T: lo = mid
    else: hi = mid
yc = math.sqrt(lo * hi)
fp = T / rar[2] - 1
print(f"   framework kernel: I reaches 64 pi only with a strong-field cutoff at g_N = {yc:.1f} a0 (a free number); RAR: needs f'(1) = {fp:.2f} (f is free in BIMOND beyond f(1) = 1)")
check("C either way the 32 pi is put in: a cutoff (framework kernel) or the free f'(1) / (alpha + beta) normalisation (RAR): INSERTION", yc > 10 and fp > 0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
