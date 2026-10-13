"""CFG741: can P-wave heating be the two-sector selector? Criteria: FROZEN_CRITERIA.md (c659126e2).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  python3 cfg741.py      (CFG741_MUTATE=1: quadratic (non-SI) W_nl; exit 1 iff the ln Lambda form breaks)
"""
import os, sys, json
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG741_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg741{TAG}.out"), "w")
def P_(s=""):
    print(s); OUT.write(s + "\n")
P_(__doc__.strip())
u, gN, a0, G, M, r, Rin, Rout, c = sp.symbols("u g_N a_0 G M r R_in R_out c", positive=True)
Wnl = c * u ** 2 / (8 * sp.pi * G) if MUT else u ** 3 / (12 * sp.pi * G * a0)     # in u = 4 pi G P
dens = Wnl - gN * u / (4 * sp.pi * G)                                              # H[P] - H[0] density
umin = [s for s in sp.solve(sp.diff(dens, u), u) if s.is_positive is not False][0]
dmin = sp.simplify(dens.subs(u, umin))
P_(f"\nT1  u_min = {umin};  energy density at the minimum = {dmin}")
dH = sp.simplify(sp.integrate(4 * sp.pi * r ** 2 * dmin.subs(gN, G * M / r ** 2), (r, Rin, Rout)))
Vf2 = sp.sqrt(G * M * a0)
target = -sp.Rational(2, 3) * M * Vf2 * sp.log(Rout / Rin)
t1 = sp.simplify(sp.expand_log(dH - target, force=True)) == 0
P_(f"    Delta H (point mass, R_in..R_out) = {dH}")
P_(f"    == -(2/3) M V_f^2 ln(R_out/R_in): {t1}")
res = {"T1": bool(t1), "DeltaH": str(dH)}
if not MUT:
    lnL, Cb = sp.symbols("lnLambda Cb", positive=True)
    Q = sp.simplify((sp.Rational(2, 3) * lnL) / (sp.Rational(3, 2) * Cb))
    P_(f"\nT2/T3  Q = E_rad/E_need = {Q}  (no M_b, no a0: scale-free {not Q.has(M) and not Q.has(a0)})")
    table = {}
    for L in (2, 4, 6):
        row = {"galaxy_Cb5.3": float(Q.subs({lnL: L, Cb: 5.3})), "galaxy_Cb10": float(Q.subs({lnL: L, Cb: 10})), "cluster_Cb5.3": float(Q.subs({lnL: L, Cb: 5.3}))}
        table[str(L)] = row
        P_(f"    ln Lambda = {L}: Q galaxy (C/b 5.3) {row['galaxy_Cb5.3']:.3f}; galaxy (C/b 10) {row['galaxy_Cb10']:.3f}; cluster (C/b 5.3) {row['cluster_Cb5.3']:.3f}")
    viable = any(table[k]["galaxy_Cb5.3"] >= 1 and table[k]["cluster_Cb5.3"] < 1 for k in table) or \
             any(table[k]["galaxy_Cb10"] >= 1 and table[k]["cluster_Cb5.3"] < 1 for k in table)
    res.update(T2=table, scale_free=bool(not Q.has(M) and not Q.has(a0)), verdict="VIABLE" if (t1 and viable) else "CLOSED")
    P_(f"\nVERDICT: {res['verdict']}  (with perfect absorption: Q <= {max(v['galaxy_Cb5.3'] for v in table.values()):.2f} for galaxies, and clusters get the same or more)")
    json.dump(res, open(os.path.join(HERE, "cfg741_results.json"), "w"), indent=1)
    rc = 0
else:
    P_(f"\nMUTATE: ln Lambda form broken: {not t1}"); rc = 1 if not t1 else 0
OUT.close(); sys.exit(rc)
