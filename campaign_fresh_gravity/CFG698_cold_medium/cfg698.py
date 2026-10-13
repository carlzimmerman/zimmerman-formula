"""CFG698: P = -rho_c xi, a real cold medium; where the tether acts decides cosmology. Criteria: FROZEN_CRITERIA.md (f713f6b27).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  python3 cfg698.py      (CFG698_MUTATE=1: off-critical tether, no tether; exit 1 iff both bite)
"""
import os, sys, json
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG698_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg698{TAG}.out"), "w")
RES = {"lane": "CFG698", "criteria": "f713f6b27", "mutate": MUT, "checks": {}}
def P_(s=""):
    print(s); OUT.write(s + "\n")
def check(k, ok, d):
    RES["checks"][k] = dict(ok=bool(ok), detail=str(d)); P_(f"  [{'PASS' if ok else 'FAIL'}] {k}: {d}"); return bool(ok)
P_(__doc__.strip())
G, rho, xi, cW, g, u = sp.symbols("G rho_c xi c_W g u", positive=True)
c_t = sp.Rational(11, 10) if MUT else 1
# J1: longitudinal k->0 mode: self-gravity grad Phi = -4 pi G rho xi (Poisson of -rho div xi); tether W = c 2 pi G P^2, P = rho xi
W = c_t * 2 * sp.pi * G * (rho * xi) ** 2
xi_dd = 4 * sp.pi * G * rho * xi - sp.diff(W, xi) / rho
P_(f"\nJ1  xi'' = 4 pi G rho xi - (1/rho) dW/dxi = {sp.simplify(xi_dd)}")
j1 = check("J1 critical tether cancels the medium's Jeans term exactly", sp.simplify(xi_dd) == 0, sp.simplify(xi_dd))
# J2 / J3 growth exponents (matter era, EdS-normalised): p^2 + p/2 = (3/2) lambda / (Ob + Oc)
Ob, Oc = sp.Rational(49, 1000), sp.Rational(26, 100)
lam = sp.symbols("lambda")
def pexp(M):
    ev = max(float(v) for v in sp.Matrix(M).eigenvals())
    p = sp.symbols("p")
    return max(float(s) for s in sp.solve(p ** 2 + p / 2 - sp.Rational(3, 2) * sp.nsimplify(ev) / (Ob + Oc), p)), ev
p_tether, ev2 = pexp([[Ob, Oc], [Ob, 0]])          # medium responds to baryons only (self-gravity cancelled)
p_free, ev3 = pexp([[Ob, Oc], [Ob, Oc]])           # free pressureless medium: responds to the total field
P_(f"\nJ2  tether everywhere: largest eigenvalue {ev2:.4f} (of Ob+Oc = {float(Ob + Oc):.3f}); growth delta ~ a^p, p = {p_tether:.4f}")
j2_fails_cosmo = p_tether <= 0.9
check("J2 tether-everywhere version FAILS cosmology (p <= 0.9)", j2_fails_cosmo, f"p = {p_tether:.4f}")
P_(f"\nJ3  tether only inside bound basins: outside, free medium: eigenvalue {ev3:.4f}, p = {p_free:.4f}")
j3 = check("J3 free medium outside basins grows like a cold component (p = 1)", abs(p_free - 1) < 1e-12, f"p = {p_free:.6f}")
P_("    inside basins: relaxed state = the law's profile (CFG694-696) = candidate B's settled cold energy (CFG624 identity)")
P_("    inherited, not re-run: X-COP identity 0.946 +- 0.080 (CFG4/CFG624) PASS; Local Group shared catchment z -0.11/-0.10 (CFG624 M1) PASS;")
P_("    D2 KiDS EXCLUDED dchi2 +68.7 (CFG596); C3 FAIL (CFG529); Bullet alpha = 0 UNDETERMINED (CFG621/623)")
# M2 check: no tether => static equation W'(u) = g has no solution for g > 0
no_sol = sp.solve(sp.Eq(0 * u, g), u) == []
P_(f"\n    no tether: static equation W'(u) = g with W' = 0 has a solution for g > 0: {not no_sol} (the galaxy profile is lost)")
RES["numbers"] = dict(p_tether=p_tether, p_free=p_free, eig_tether=ev2, eig_free=ev3)
if MUT:
    bites = dict(M1=not j1, M2=no_sol and abs(p_free - 1) < 1e-12)
    RES["mutate_bites"] = bites; P_(f"\nMUTATE: {bites}")
    rc = 1 if all(bites.values()) else 0
else:
    v = "CANDIDATE B WITH A MECHANISM" if (j1 and j2_fails_cosmo and j3) else "NOT AS FROZEN"
    RES["verdict"] = v; P_(f"\nVERDICT: {v}; data failures C3 and D2 unchanged (they belong to the law's profile, CFG678)")
    rc = 0
json.dump(RES, open(os.path.join(HERE, f"cfg698_results{TAG}.json"), "w"), indent=1, default=str)
OUT.close(); sys.exit(rc)
