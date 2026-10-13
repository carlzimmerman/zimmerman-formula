"""CFG699: can CFG698's cold medium settle in time? Criteria: FROZEN_CRITERIA.md (d16b81262).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  python3 cfg699.py      (CFG699_MUTATE=1: rho_c x 1e4; exit 1 iff T drops 100x)
"""
import os, sys, json, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import CFG4_common as C4  # noqa: E402
MUT = os.environ.get("CFG699_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg699{TAG}.out"), "w")
def P_(s=""):
    print(s); OUT.write(s + "\n")
P_(__doc__.strip())
# gamma from L*: l_gamma = gamma/(beta B), B = sqrt(G M/beta), beta = (4 pi G)^2/a0; L*^2 = 2 r_M l_gamma
G_, M_, a0_, gam, Ls = sp.symbols("G M a_0 gamma L_s", positive=True)
beta = (4 * sp.pi * G_) ** 2 / a0_
ell = gam / (beta * sp.sqrt(G_ * M_ / beta))
gsol = sp.solve(sp.Eq(Ls ** 2, 2 * sp.sqrt(G_ * M_ / a0_) * ell), gam)[0]
P_(f"\ngamma(L*) = {sp.simplify(gsol)}  (mass-independent: {sp.simplify(sp.diff(gsol, M_)) == 0})")
G, C, PC, YR = 6.6743e-11, 2.99792458e8, 3.0856775814913673e16, 3.15576e7
Ls_m, r, kappa = 5.75 * PC, 10e3 * PC, 0.5
res, ok_all = {}, True
for f in C4.FOOTS:
    a0 = C4.A0[f]
    rho_L = (a0 / (kappa * C)) ** 2 / G
    rho_c = 0.26 / 0.686 * rho_L * (1e4 if MUT else 1.0)
    gamma = 2 * math.pi * G * Ls_m ** 2
    P_(f"\n{f}: a0 {a0:.4e}; rho_Lambda {rho_L:.3e} kg/m^3; rho_c {rho_c:.3e}; gamma k^2 term at r = 10 kpc: rho_c gamma/r^2 = {rho_c * gamma / r ** 2:.2e} s^-2")
    res[f] = {}
    for y in (0.01, 0.1, 1.0, 10.0):
        g = 0.5 * (y + math.sqrt(y * y + 4 * y)) * a0
        x = (g - y * a0) / a0
        om2 = rho_c * 4 * math.pi * G * ((1 - x) ** -2 - 1) + rho_c * gamma / r ** 2
        T = 2 * math.pi / math.sqrt(om2) / YR / 1e9
        res[f][str(y)] = dict(u_over_a0=x, T_Gyr=T, factor_over_bar=T / 1.38)
        P_(f"    y = {y:5}: u/a0 = {x:.3f}; element period T = {T:.3g} Gyr  ({T / 1.38:.2g} x the 1.38-Gyr bar; I_req/I = {(1.38 / T) ** 2:.2g})")
    ok_all &= res[f]["0.1"]["T_Gyr"] <= 1.38 and res[f]["1.0"]["T_Gyr"] <= 1.38
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg699_results.json")))
    ratio = base["canonical"]["1.0"]["T_Gyr"] / res["canonical"]["1.0"]["T_Gyr"]
    P_(f"\nMUTATE: T drops by {ratio:.1f}x (expect 100)"); rc = 1 if abs(ratio - 100) < 1e-6 * 100 else 0
else:
    res["verdict"] = "PASS" if ok_all else "FAIL"
    P_(f"\nVERDICT T1: {res['verdict']} (period at y = 0.1 and 1 vs 1.38 Gyr, both footings)"); rc = 0
    json.dump(res, open(os.path.join(HERE, "cfg699_results.json"), "w"), indent=1)
OUT.close(); sys.exit(rc)
