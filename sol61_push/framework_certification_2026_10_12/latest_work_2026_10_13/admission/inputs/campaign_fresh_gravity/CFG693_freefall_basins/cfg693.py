"""CFG693: each system reads its own free-fall basin (equivalence principle + merge tree).

Criteria: FROZEN_CRITERIA.md (committed alone, 45ff137aa). T1-T2 sympy, T3 numbers, T4 reported.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  python3 cfg693.py      (CFG693_MUTATE=1: M1 plain static potential, M2 local |g|; exit 1 iff both bite)
"""
import os, sys, json, math

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG693_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg693{TAG}.out"), "w")
RES = {"lane": "CFG693", "criteria": "45ff137aa", "mutate": MUT, "checks": {}, "numbers": {}}


def P(s=""):
    print(s)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P(__doc__.strip())
x, y, z, X, Y, Z = sp.symbols("x y z X Y Z", real=True)
G, M, ge, r, R, Vs, Vh, al, a0 = sp.symbols("G M g_e r R V_s V_h alpha a_0", positive=True)

# ============================================================================ T1 equivalence principle => EFE-blind
P("\nT1  a uniform external field g_e (along -z): Phi_e = g_e z")
Phi_e = ge * z
flux_div = sp.diff(sp.diff(Phi_e, x), x) + sp.diff(sp.diff(Phi_e, y), y) + sp.diff(sp.diff(Phi_e, z), z)
P(f"    div grad Phi_e = {flux_div}  => zero flux through every closed surface (Gauss): m_b and the flux density 4 pi G m_b/A see no g_e")
# free-fall subtraction for a general external potential: Phi_F = Phi_e - Phi_e(X) - grad Phi_e(X).(x - X): only tides remain
pt = {x: X, y: Y, z: Z}
Phi_F_uniform = sp.simplify(Phi_e - (Phi_e.subs(pt) + ge * (z - Z)))
P(f"    free-fall frame: Phi_F(uniform part) = Phi_e - Phi_e(X) - grad Phi_e(X).(x - X) = {Phi_F_uniform}  (only the tidal, 2nd-order part survives)")
Phi_sat = -G * M / sp.sqrt(x ** 2 + y ** 2 + z ** 2)
if MUT:
    Phi_used = Phi_sat + Phi_e                                   # M1: plain static potential
    # point-mass saddle on the axis: G M / z^2 = g_e
    zs = sp.solve(sp.Eq(G * M / z ** 2, ge), z)
    basin_dep = any(sp.diff(s_, ge) != 0 for s_ in zs)
    P(f"    M1 plain static potential: saddle at z = {zs}; basin depends on g_e: {basin_dep}")
    gbar_blind = not basin_dep
    loc = sp.sqrt(sp.diff(Phi_used, x) ** 2 + sp.diff(Phi_used, y) ** 2 + sp.diff(Phi_used, z) ** 2)
    local_dep = sp.simplify(sp.diff(loc, ge)) != 0                 # M2: local |g| depends on g_e
    P(f"    M2 local |g| depends on g_e: {local_dep}")
    t1 = gbar_blind and not local_dep
else:
    Phi_used = Phi_sat + Phi_F_uniform
    t1 = flux_div == 0 and sp.simplify(Phi_used - Phi_sat) == 0
check("T1 uniform g_e: zero flux and removed from Phi_F (node boost independent of g_e)", t1, f"Phi_F - Phi_sat = {sp.simplify(Phi_used - Phi_sat)}")

# ============================================================================ T2 where the basin ends vs the lensing aperture
P("\nT2  SIS satellite V_s at R in a host rho_h ~ R^-alpha; free-fall saddle V_s^2/r = T_h r; aperture rho_s(r_bg) = rho_h(R)")
Mh = sp.symbols("M_h", positive=True)
T_h = (al - 1) * G * Mh / R ** 3                                  # radial tidal stretch of a power-law host
fourpiGrho = (3 - al) * G * Mh / R ** 3                           # 4 pi G rho_h(R)
r_J = Vs / sp.sqrt(T_h)
r_bg = Vs / sp.sqrt(fourpiGrho)                                    # SIS: 4 pi G rho_s = V_s^2 / r^2
ratio = sp.simplify(r_J / r_bg)
P(f"    r_J = {r_J};  r_bg = {r_bg};  r_J/r_bg = {ratio}")
tab = {str(a): float(ratio.subs(al, a)) for a in (1.5, 1.75, 2, 2.25, 2.5)}
P("    r_J/r_bg by host slope alpha: " + ", ".join(f"{k}: {v:.3f}" for k, v in tab.items()))
static = R * Vs ** 2 / (Vs ** 2 + Vh ** 2)                         # plain static saddle between two SIS (host SIS: r_bg = R V_s/V_h)
st = {str(q): float((static / (R * Vs / Vh)).subs({Vs: q, Vh: 1})) for q in (0.05, 0.1, 0.2, 0.3)}
P("    plain static saddle / r_bg (alpha = 2) at V_s/V_h: " + ", ".join(f"{k}: {v:.3f}" for k, v in st.items()))
if MUT:
    t2_ratio = float((static / (R * Vs / Vh)).subs({Vs: 0.15, Vh: 1}))
    t2 = abs(t2_ratio - 1) < 1e-9
    P(f"    M1: plain static saddle / r_bg at V_s/V_h = 0.15: {t2_ratio:.3f}")
else:
    t2 = sp.simplify(ratio.subs(al, 2)) == 1
check("T2 free-fall basin edge = Sifon aperture for an isothermal host (alpha = 2)", t2, f"ratio(alpha=2) = {ratio.subs(al, 2)}")
RES["numbers"]["T2"] = dict(ratio_by_alpha=tab, static_over_rbg=st)

# ============================================================================ T3 the Sun
P("\nT3  the Sun in the Galaxy: T = g_ext/R (flat curve, radial stretch)")
GMs, PC = 1.32712440018e20, 3.0856775814913673e16
gext, Rsun = 2.146e-10, 8.18e3 * PC
T = gext / Rsun
rJ = (GMs / T) ** (1 / 3)
Q2_CEIL = 5.2e-27
P(f"    T = {T:.3e} s^-2;  Sun's free-fall basin r_J = {rJ:.3e} m = {rJ / PC:.2f} pc;  r_M(Sun) = {math.sqrt(GMs / 1.2e-10) / PC:.4f} pc")
P(f"    wide binaries (<= 0.1 pc) inside the basin: {0.1 < rJ / PC}  => law with the binary's own mass, no EFE (boost as the law; opposite of CFG691)")
P(f"    Cassini: Sun's own node has Q2 = 0; Galaxy node's tidal quadrupole ~ T = {T:.2e} vs ceiling {Q2_CEIL:.1e}: ratio {T / Q2_CEIL:.1e}")
t3 = rJ / PC > 0.1 and T < Q2_CEIL
check("T3 Sun: wide binaries inside its own basin; Galactic tide below the Cassini Q2 ceiling", t3, f"r_J {rJ / PC:.2f} pc; T/ceiling {T / Q2_CEIL:.1e}")
RES["numbers"]["T3"] = dict(T=T, rJ_pc=rJ / PC, T_over_Q2ceil=T / Q2_CEIL)

# ============================================================================ T4 the cost (reported)
P("\nT4  (reported) the jumps")
for q in (0.1, 0.2):
    # at r_J (alpha = 2): satellite's own field V_s^2/r_J = V_s V_h / R; host field V_h^2 / R
    P(f"    V_s/V_h = {q}: across r_J the satellite's own (deep: ~all phantom) field V_s^2/r_J drops to 0; that is {q:.0%} of the host's field there")
P("    merger: a parent node appears when two basins share a closed level surface of the common free-fall potential; its phantom")
P("    switches on from 0 at that moment (CFG48's 'jump at every merger'). Persistence weighting (merge-tree depth / node V^2) is the")
P("    named smoothing; not built here.")

if MUT:
    bites = dict(M1=(not t1) and (not t2), M2=(not t1))
    RES["mutate_bites"] = bites
    P(f"\nMUTATE: {bites}")
    rc = 1 if all(bites.values()) else 0
else:
    ok = t1 and t2 and t3
    RES["verdict"] = "THE GAP IS DEFINED" if ok else "NOT DEFINED"
    P(f"\nVERDICT: {RES['verdict']} (a definition, not an action; R0, B1, M1a unchanged)")
    rc = 0
json.dump(RES, open(os.path.join(HERE, f"cfg693_results{TAG}.json"), "w"), indent=1, default=str)
OUT.close()
sys.exit(rc)
