#!/usr/bin/env python3
"""CFG661 (FROZEN_CRITERIA.md, abd99a242): can a stress that responds to compression keep the law as cold energy's exact
equilibrium (spherical, local, first-order, field-aligned)?  T1/T2 sympy, T3 dimensions + WKB, T4 with c.
kappa = 1/2 FITTED; cold energy mass required; no particle species; not "theory closed".
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg661.py    (CFG661_MUTATE=1 -> _MUTATE outputs, exit 1 iff the teeth bite)"""
import os, sys, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG661_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT, RES = [], {"lane": "CFG661", "criteria": "abd99a242", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


r, G = sp.symbols("r G", positive=True)
gN = sp.Function("g_N")(r)
q1, q2 = sp.symbols("q1 q2")                     # stand-ins for g_N', g_N''


def to_q(e):
    return e.subs(sp.Derivative(gN, (r, 2)), q2).subs(sp.Derivative(gN, r), q1)


# ------------------------------------------------------------------------------------------- general law F (T1, T2 necessity)
F = sp.Function("F")
y = sp.Symbol("y")
g = F(gN)
Fp = sp.diff(F(y), y).subs(y, gN)
rho_b = sp.diff(r ** 2 * gN, r) / (4 * sp.pi * G * r ** 2)
rho_c = sp.diff(r ** 2 * g, r) / (4 * sp.pi * G * r ** 2) - rho_b
if MUT:   # M1: pretend rho_c' carries no g_N'' (drop it after differentiation)
    pass
Rv, Bv, Gv = sp.symbols("Rv Bv Gv")              # arguments rho_c, rho_b, g of the stress functions
Ppar2 = sp.Function("Ppar")(Rv, Gv)
Pper2 = sp.Function("Pper")(Rv, Gv)
on = {Rv: rho_c, Gv: g}
dPdr = (sp.diff(Ppar2, Rv).subs(on) * sp.diff(rho_c, r) + sp.diff(Ppar2, Gv).subs(on) * sp.diff(g, r))
res1 = dPdr + 2 * (Ppar2.subs(on) - Pper2.subs(on)) / r + rho_c * g
res1q = to_q(sp.expand(res1))
if MUT:
    res1q = res1q.subs(q2, 0)
coef1 = sp.simplify(sp.diff(res1q, q2))
target1 = sp.diff(Ppar2, Rv).subs(on) * (Fp - 1) / (4 * sp.pi * G)
T1 = bool(sp.simplify(coef1 - to_q(target1)) == 0) and coef1 != 0
P("CFG661" + (" [MUTATE]" if MUT else ""))
P(f"T1 coefficient of g_N'' for P_par(rho_c, g): {coef1}")
P(f"   equals dP_par/drho_c (F'-1)/4piG: {T1}  -> exactness forces dP_par/drho_c = 0 wherever F' != 1")

Ppar3 = sp.Function("Ppar")(Rv, Bv, Gv)
on3 = {Rv: rho_c, Bv: rho_b, Gv: g}
dP3 = (sp.diff(Ppar3, Rv).subs(on3) * sp.diff(rho_c, r) + sp.diff(Ppar3, Bv).subs(on3) * sp.diff(rho_b, r)
       + sp.diff(Ppar3, Gv).subs(on3) * sp.diff(g, r))
coef3 = sp.simplify(sp.diff(to_q(sp.expand(dP3)), q2))
target3 = (sp.diff(Ppar3, Rv).subs(on3) * (Fp - 1) + sp.diff(Ppar3, Bv).subs(on3)) / (4 * sp.pi * G)
T2a = bool(sp.simplify(coef3 - to_q(target3)) == 0)
P(f"T2a coefficient of g_N'' for P_par(rho_c, rho_b, g) = [P_rho_c (F'-1) + P_rho_b]/4piG: {T2a}")

# ------------------------------------------------------------------------------------------- explicit law (T2 family identity)
a0 = sp.symbols("a0", positive=True)
gs = sp.Symbol("gs", positive=True)
gN_of = gs ** 2 / (gs + a0)                      # inverse of the 'simple' law g = g_N/2 + sqrt(g_N^2/4 + a0 g_N)
Fp_of = 1 / sp.diff(gN_of, gs)                   # F'(g) = dg/dg_N
s_of = sp.simplify(Fp_of * gN_of / gs)
h_of = sp.simplify(gs * (1 - s_of) / (2 * sp.pi * G))
dPA_of = gs / (4 * sp.pi * G) * (1 / Fp_of - 1)
gr = sp.Function("gr")(r)                        # g(r), with g_N(r) = gN_of(g(r)) on-shell (arbitrary profile through gr)
gNr = gN_of.subs(gs, gr)
rho_b_e = sp.diff(r ** 2 * gNr, r) / (4 * sp.pi * G * r ** 2)
rho_c_e = sp.diff(r ** 2 * gr, r) / (4 * sp.pi * G * r ** 2) - rho_b_e
ucoef = (Fp_of if MUT else Fp_of - 1).subs(gs, gr)     # M2: F' instead of F'-1
u_e = rho_c_e - ucoef * rho_b_e
w_e = u_e / h_of.subs(gs, gr)
Psi = sp.Function("Psi")
wv = sp.Symbol("wv")
Ppar_e = sp.Function("PA")(gr) + Psi(w_e)
dPpar_dr = dPA_of.subs(gs, gr) * sp.diff(gr, r) + sp.diff(Psi(wv), wv).subs(wv, w_e) * sp.diff(w_e, r)
dP_du = sp.diff(Psi(wv), wv).subs(wv, w_e) / h_of.subs(gs, gr)
Pper_minus_par = -u_e / 2 * dP_du + gr * (gr - gNr) / (4 * sp.pi * G)
res2 = dPpar_dr - 2 * Pper_minus_par / r + rho_c_e * gr
res2s = sp.simplify(sp.together(sp.expand(res2)))
T2b = bool(res2s == 0)
P(f"T2b family P_par = P_A(g) + Psi(u/h(g)), u = rho_c - (F'-1) rho_b, arbitrary Psi, explicit law: residual {res2s if not T2b else 0}"
  f" -> {'IDENTICALLY ZERO' if T2b else 'NONZERO'}")
w_on = sp.simplify(w_e.subs(sp.Derivative(gr, r), sp.Symbol("gp")))
P(f"   on-shell u/h = {sp.simplify(w_on)}  (expected 1/r for any g' — the invariant is 'radius', local off-shell)")

# ------------------------------------------------------------------------------------------- T3 dimensions, WKB
# exponents (kg, m, s): w = [0,-1,0]; G = [-1,3,-2]; a0 = [0,1,-2]; c = [0,1,-1]
Mdim = sp.Matrix([[0, -1, 0], [-1, 3, -2], [0, 1, -2]]).T           # columns: w, G, a0
ns = Mdim.nullspace()
T3i = len(ns) == 0
Mdim_c = sp.Matrix([[0, -1, 0], [-1, 3, -2], [0, 1, -2], [0, 1, -1]]).T
ns_c = Mdim_c.nullspace()
P(f"\nT3(i) dimensionless groups of w = u/h with {{G, a0}}: {len(ns)} -> Psi must be constant: {T3i}")
P(f"      with c added: {[list(v) for v in ns_c]}  (w c^2/a0)")
k, om = sp.symbols("k omega")
rho0, d0, g0, Pp, c2 = sp.symbols("rho0 d0 g0 Pp c2", real=True)
dr_, du_ = sp.symbols("drho du")
dg = 4 * sp.pi * G * sp.I * dr_ / k
mom = -sp.I * om * rho0 * du_ + sp.I * k * (Pp * dg + c2 * dr_) - rho0 * dg - g0 * dr_
con = -sp.I * om * dr_ + sp.I * k * rho0 * du_ + d0 * du_
D = sp.expand(sp.Matrix([[sp.diff(e, v) for v in (dr_, du_)] for e in (mom, con)]).det())
# CFG660's deep test point (g = 0.1 a0, SIS, tau_ff = 1); P_A' from the simple law at g/a0 = 0.1
Ppv = float(dPA_of.subs({gs: 0.1, a0: 1, G: 1}))
base = {rho0: 1 / (4 * math.pi), d0: -2 / (4 * math.pi), g0: 1.0, Pp: Ppv, G: 1.0}
wkb = {}
for lab, c2v in (("Psi1=0", 0.0), ("Psi1>0 (c_eff^2=0.01)", 0.01), ("Psi1>0 (c_eff^2=0.5)", 0.5)):
    row = []
    for kk in (1e1, 1e3, 1e5):
        rts = sp.Poly(D.subs(base).subs({c2: c2v, k: kk}), om).nroots()
        row.append(max(float(sp.im(z)) for z in rts))
    wkb[lab] = row
    P(f"T3(ii) {lab:22s}: max Im omega at k = 1e1/1e3/1e5 = " + "/".join(f"{v:.3g}" for v in row))
T3ii = wkb["Psi1=0"][2] > 5 * wkb["Psi1=0"][1] and all(v[2] < 2 * v[1] + 1e-9 for kk, v in wkb.items() if kk != "Psi1=0")
P(f"      sqrt(k) growth iff Psi1 = 0, bounded for Psi1 > 0: {T3ii}")

# ------------------------------------------------------------------------------------------- T4 with c: Jeans mimic
rr_, gg_, ss_ = sp.symbols("rr gg ss", positive=True)
req = gg_ ** 2 * rr_ * (1 - ss_) / (4 * sp.pi * G)          # required Psi'(1/r) = h * g r / 2
T4 = sp.diff(req, gg_) != 0
P(f"\nT4 required Psi'(1/r) for c_eff^2 = V^2/2: {req}; d/dg at fixed r = {sp.diff(req, gg_)} -> depends on g: {T4}"
  " (no universal Psi; with c, f is a free function)")

RES.update(T1=dict(coef=str(coef1), confirmed=T1), T2=dict(necessity=T2a, family_identity=T2b, residual=str(res2s)),
           T3=dict(dimless_groups_G_a0=len(ns), with_c=[list(map(str, v)) for v in ns_c], wkb=wkb, ill_iff_flat=T3ii),
           T4=dict(required=str(req), depends_on_g=bool(T4)))
if MUT:
    m1 = not T1                                   # coefficient vanished when g_N'' dropped
    m2 = not T2b
    RES["MUTATE"] = dict(M1=m1, M2=m2)
    P(f"\nMUTATE: M1 (no g_N'' in rho_c') coefficient vanishes: {m1}; M2 (u with F') residual nonzero: {m2}")
    rc = 1 if (m1 and m2) else 0
else:
    nogo = T1 and T2a and T2b and T3i and T3ii
    lab = ("NO-GO (local, first-order, spherical, {G, a0})" if nogo else
           ("DOOR OPEN" if not T3i else "INCOMPLETE (a check failed)"))
    lab += "; with c: NEEDS A FREE FUNCTION; no universal Jeans mimic" if T4 else ""
    RES["label"] = lab
    P(f"\nLANE LABEL: {lab}")
    rc = 0
json.dump(RES, open(os.path.join(HERE, f"cfg661_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg661{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(rc)
