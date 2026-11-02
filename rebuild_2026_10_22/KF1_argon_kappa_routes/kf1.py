# KF1: grade Argon's kappa routes. MUTATE=1 sets Einstein's coupling to 4 pi G. Outputs named by mode.
import json, os
import sympy as sp

MUT = os.environ.get("MUTATE") == "1"
tag = "_MUTATE" if MUT else ""
here = os.path.dirname(os.path.abspath(__file__))
G, c, rho, r, g, gN, a0 = sp.symbols("G c rho r g g_N a_0", positive=True)
coupling = (4 if MUT else 8) * sp.pi * G
kappa = lambda a: sp.simplify(a / (c * sp.sqrt(G * rho)))
res = {"mode": "MUTATE" if MUT else "normal"}

# T1, R2's formula at each declared length
R_dS = c / sp.sqrt(coupling * rho / 3)
lengths = {"c/sqrt(G rho)": c / sp.sqrt(G * rho), "de Sitter radius": R_dS,
           "c/sqrt(4 pi G rho)": c / sp.sqrt(4 * sp.pi * G * rho)}
res["T1_menu"] = {k: str(kappa((c**2 / 2) / L)) for k, L in lengths.items()}
res["T1_menu_num"] = {k: float(kappa((c**2 / 2) / L)) for k, L in lengths.items()}

# T2, the radius where uniform rho makes a horizon, with the mutation in the coupling
M = sp.Rational(4, 3) * sp.pi * rho * r**3
sols = sp.solve(sp.Eq((coupling / (4 * sp.pi)) * M / (c**2 * r), 1), r)
res["T2_horizon_radius"] = str(sols[0])
res["T2_equals_L_DE"] = bool(sp.simplify(sols[0] - lengths["c/sqrt(G rho)"]) == 0)
res["T2_J_at_horizon"] = str(sp.simplify(G * rho * sols[0]**2 / c**2))

# T3, gradient against Phi/R at the de Sitter horizon
R = sp.symbols("R", positive=True)
Phi = c**2 * r**2 / (2 * R**2)
res["T3_gradient_at_R"] = str(sp.diff(Phi, r).subs(r, R))
res["T3_Phi_over_R"] = str(Phi.subs(r, R) / R)
res["T3_kappa_true_gradient"] = str(kappa((c**2 / R).subs(R, R_dS)))

# T4, R2's output is independent of Einstein's coupling
res["T4_R2_output"] = str(kappa((c**2 / 2) / lengths["c/sqrt(G rho)"]))
res["T4_uses_coupling"] = bool(lengths["c/sqrt(G rho)"].has(sp.pi))

# T5, any density gives 1/2: the formula has no slot for which density
rho2 = sp.symbols("rho_any", positive=True)
res["T5_any_density"] = str(sp.simplify((c**2 / 2) / (c / sp.sqrt(G * rho2)) / (c * sp.sqrt(G * rho2))))

# T6, the law's algebra with a0 free
root = gN / 2 + sp.sqrt(gN**2 / 4 + gN * a0)
res["T6_residual"] = str(sp.simplify(root**2 / (root + a0) - gN))
res["T6_a0_free"] = not sp.simplify(root**2 / (root + a0) - gN).has(rho)
res["T6_high_g_excess"] = str(sp.limit(root - gN, gN, sp.oo))

res["labels"] = {"R1": "NO NUMBER", "R2": "VOID, X7 and MENU", "R3": "NO NUMBER, holds for every a0"}
for k, v in res.items():
    print(k, v)
with open(os.path.join(here, f"kf1{tag}.json"), "w") as f:
    json.dump(res, f, indent=1)
