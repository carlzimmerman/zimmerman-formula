"""p19: flux-through-the-horizon readings of A Lambda = 32 pi^2 (G = c = 1; r = horizon radius, rho = rho_Lambda, Lambda = 8 pi rho).

(1) Gauss-Bonnet of the horizon 2-sphere: oint K dA = 2 pi chi = 4 pi for every radius (K = 1/r^2).
(2) GR's horizon balance (MOTS stability / Hawking-Gibbons-Woolgar area bound): for a black-hole cross-section in a Lambda vacuum,
    oint K dA >= oint Lambda dA, i.e. Lambda A <= 4 pi, equality at Nariai. Checked here on the whole SdS family numerically.
(3) The puzzle as a flux balance: A Lambda = 32 pi^2  <=>  oint (Lambda/8 pi) dA = oint K dA  <=>  oint G rho dA = 4 pi:
    the SAME Gauss-Bonnet balance with the vacuum entering as G rho instead of 8 pi G rho (= Lambda).
(4) Ordinary flux identities (Newtonian Gauss flux, Smarr with Lambda) for comparison: they reduce to point conditions (p17 values).

Run: python3 p19_horizon_flux.py   |   MUTATE=1: horizon curvature set to 2/r^2 (wrong), checks A and B must fail
"""
import os, sys
import numpy as np
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
pi = sp.pi
r, th, ph, rho, M, L = sp.symbols("r theta phi rho M Lambda", positive=True)
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)

# (1) Gauss curvature of the round 2-sphere from its metric (Brioschi via sympy's 2D Ricci scalar / 2)
g = sp.diag(r**2, r**2 * sp.sin(th)**2)
x = [th, ph]; gi = g.inv()
Gam = [[[sum(gi[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b]) - sp.diff(g[b, c], x[d])) / 2 for d in range(2))
         for c in range(2)] for b in range(2)] for a in range(2)]
def Riem(a, b, c, d):
    return sp.diff(Gam[a][b][d], x[c]) - sp.diff(Gam[a][b][c], x[d]) + sum(Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c] for e in range(2))
Ric = sp.Matrix(2, 2, lambda b, d: sum(Riem(a, b, a, d) for a in range(2)))
K = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(2) for j in range(2)) / 2)
if MUTATE: K = 2 / r**2
GB = sp.simplify(sp.integrate(sp.integrate(K * r**2 * sp.sin(th), (th, 0, pi)), (ph, 0, 2 * pi)))
check(f"A Gauss-Bonnet on the horizon sphere: K = {K}, oint K dA = {GB} = 4 pi for every r", sp.simplify(GB - 4 * pi) == 0)

# (2) SdS family: f = 1 - 2M/r - Lambda r^2/3; black-hole horizon r_b; check Lambda A_b <= 4 pi, equality at Nariai (M = 1/(3 sqrt Lambda))
Lv = 1.0; worst = 0.0
for m in np.linspace(1e-4, 1 / (3 * np.sqrt(Lv)) * 0.999999, 4000):
    rts = np.roots([-Lv / 3, 0, 1, -2 * m]); rts = np.sort(rts[(abs(rts.imag) < 1e-12) & (rts.real > 0)].real)
    worst = max(worst, Lv * 4 * np.pi * rts[0]**2)
area_bound = float(GB) if not MUTATE else 4 * np.pi
# exact Nariai point: f and f' vanish together at r = 1/sqrt(Lambda), M = 1/(3 sqrt(Lambda)); there Lambda A = 4 pi exactly
fS = 1 - 2 * M / r - L * r**2 / 3; rN = 1 / sp.sqrt(L); MN = 1 / (3 * sp.sqrt(L))
nar = [sp.simplify(fS.subs({r: rN, M: MN})), sp.simplify(sp.diff(fS, r).subs({r: rN, M: MN})), sp.simplify(L * 4 * pi * rN**2)]
print(f"   Nariai: f = {nar[0]}, f' = {nar[1]}, Lambda A = {nar[2]};  numeric SdS scan max Lambda A_b = {worst:.6f} (grid stops at 0.999999 M_N; r_b approaches as sqrt(eps), so 0.16% short)")
check(f"B GR's horizon balance oint Lambda dA <= oint K dA: every SdS black-hole horizon has Lambda A_b <= {GB}, equality only at Nariai",
      nar[0] == 0 and nar[1] == 0 and sp.simplify(nar[2] - GB) == 0 and worst <= float(GB) + 1e-9 and abs(worst / float(GB) - 1) < 5e-3)

# (3) the puzzle as the same balance with G rho in place of Lambda = 8 pi G rho
A = 4 * pi * r**2
puz = sp.solve(sp.Eq(A * 8 * pi * rho, 32 * pi**2), rho)[0]
check("C A Lambda = 32 pi^2 is exactly  oint G rho_Lambda dA = oint K dA  (rho r^2 = 1): the GR balance with 8 pi G -> G",
      sp.simplify(puz * r**2 - 1) == 0 and sp.simplify(sp.integrate(sp.integrate(puz * r**2 * sp.sin(th), (th, 0, pi)), (ph, 0, 2 * pi)) - GB) == 0)
ratio = sp.simplify((32 * pi**2) / (4 * pi))
check(f"D the puzzle's horizon is past GR's bound by Lambda A / 4 pi = {ratio} (the missing Einstein coupling), so no GR horizon satisfies it",
      sp.simplify(ratio - 8 * pi) == 0)

# (4) ordinary flux identities reduce to point conditions
newton = sp.solve(sp.Eq(8 * pi * rho / 3 * r * A, 4 * pi * (r / 2)), rho)[0] * r**2          # vacuum Gauss flux = 4 pi M_hole
smarr = sp.solve(sp.Eq((1 / (2 * r)) * A / (4 * pi), 8 * pi * rho * r**3 / 3), rho)[0] * r**2   # Smarr: kappa A/4pi term = Lambda r^3/3 term
print(f"   Newtonian flux of the vacuum field through r = 4 pi M_hole: rho r^2 = {sp.simplify(newton)};  Smarr horizon term = vacuum term: rho r^2 = {sp.simplify(smarr)}")
check("E these flux identities give p17-type values (3/(16 pi)), not 1", sp.simplify(newton - 3 / (16 * pi)) == 0 and sp.simplify(smarr - 3 / (16 * pi)) == 0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
