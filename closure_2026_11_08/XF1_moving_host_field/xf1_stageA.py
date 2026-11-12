#!/usr/bin/env python3
"""XF1 Stage A: the stationary-pattern equations of the full screened v3s action for a body moving at V through a
uniform host khronon (background charge rho_h, host law field g_ext), with the known answers A2-A4.

Criteria: FROZEN_CRITERIA.md (8b99d12c42). Run from the repo root:
  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 -B closure_2026_11_08/XF1_moving_host_field/xf1_stageA.py
Writes xf1_stageA.out / xf1_stageA.json. kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.

Starting point (PAPER70 Eq. A, Legendre form, PN order, mu_K = 0): the leaf Lagrangian density
    L = P . grad Xi - W(K|P|) - gamma_L F(Pi),   Xi = phi - sigma_t + |grad sigma|^2/2,   Pi = div P,
    W(p) = (a0^2/K)[-p/a0 - ln(1 - p/a0)],  gamma_L = K L*^2/2,  F = the Pi^6 blend (F(Pi) = Pi^2/2 for Pi >= rho_DE),
plus the Newtonian potential equation with the foliation energy density rho_b + Pi (W and gamma_L F are 1PN-small, A1h).
AC15 is this Lagrangian with W dropped (its S1a: the term is <= 1.2e-10 of the stiffness term at 10 AU) and F raw.
Here W is kept: at galaxy scales it is the dominant term (2 M_theta (r/L*)^2 ~ 1e5 at 10 kpc) and the deep-law
nonlinearity of J (W's Legendre dual) is live.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import xf1_cells as XC                                                       # noqa: E402
OUT, RES = [], {"lane": "XF1_moving_host_field", "criteria": "8b99d12c42", "checks": {}, "statements": {}}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    RES["checks"][name] = dict(ok=bool(ok), detail=str(detail)); P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


def state(name, text):
    RES["statements"][name] = text; P(f"{name}: {text}")


t, x, y, z = Xs = sp.symbols("t x y z", real=True); xs3 = (x, y, z)
K, gam, a0, V = sp.symbols("K gamma_L a0 V", positive=True)
sig = sp.Function("sigma")(*Xs); phi = sp.Function("phi")(*Xs)
Pf = [sp.Function(f"P{i}")(*Xs) for i in range(3)]
Wf, Ff = sp.Function("W"), sp.Function("F")
Xi = phi - sp.diff(sig, t) + sum(sp.diff(sig, v) ** 2 for v in xs3) / 2
q = sum(sp.diff(Pf[i], xs3[i]) for i in range(3))
Pabs = sp.sqrt(sum(p_ ** 2 for p_ in Pf))
L = sum(Pf[i] * sp.diff(Xi, xs3[i]) for i in range(3)) - Wf(K * Pabs) - gam * Ff(q)

P("XF1 Stage A: stationary-pattern equations of the screened v3s action (W live, F general). kappa = 1/2 FITTED; not theory closed.")
# ------------------------------------------------------------------ A1a: the P equation with W live
els = euler_equations(L, Pf, Xs)
# target: grad(Xi + gamma F'(q)) - K W'(K|P|) P/|P| = 0
tgt = []
s_ = sp.Symbol("s_")
Fprime = sp.diff(Ff(s_), s_).subs(s_, q)                   # F'(q) as a Subs object (chain rule then gives F''(q) d_i q)
for i in range(3):
    dW = sp.diff(Wf(K * Pabs), Pf[i])                     # = W'(K|P|) K P_i/|P|
    dF = gam * sp.diff(Fprime, xs3[i])                     # gamma d_i [F'(q)]
    tgt.append(sp.diff(Xi, xs3[i]) + dF - dW)
res = [sp.simplify(els[i].lhs - tgt[i]) for i in range(3)]
res2 = [sp.simplify(els[i].lhs + tgt[i]) for i in range(3)]
okA1a = all(r == 0 for r in res) or all(r == 0 for r in res2)
check("A1a", okA1a, "P equation: grad(Xi + gamma_L F'(q)) = K W'(K|P|) P/|P|  (residuals " + str(res if all(r == 0 for r in res) else res2) + ")")

# ------------------------------------------------------------------ A1b: the khronon equation (charge continuity)
els_s = euler_equations(L, [sig], Xs)
cont = sp.diff(q, t) - sum(sp.diff(q * sp.diff(sig, v), v) for v in xs3)       # d_t q + div(q v), v = -grad sigma
r1b = sp.simplify(sp.expand(els_s[0].lhs) - cont); r1b2 = sp.simplify(sp.expand(els_s[0].lhs) + cont)
check("A1b", r1b == 0 or r1b2 == 0, "khronon equation: d_t q + div(q v) = 0 with v = -grad sigma, q = div P (charge advected by the frame, conserved)")

# ------------------------------------------------------------------ A1c: W is the Legendre dual of the certified J (PAPER70 Eq. A)
p, u = sp.symbols("p u", positive=True)
W = (a0 ** 2 / K) * (-p / a0 - sp.log(1 - p / a0))
Wprime = sp.simplify(sp.diff(W, p))
sol = sp.solve(sp.Eq(K * Wprime, a0 * u), p)                                   # K W'(K|P|) = |grad chi| = a0 u
leg = sp.simplify((a0 * u) * sol[0] / K - W.subs(p, sol[0]) - (a0 ** 2 / K) * (u - sp.log(1 + u)))
check("A1c", len(sol) == 1 and sp.simplify(sol[0] - a0 * u / (1 + u)) == 0 and leg == 0,
      f"W'(p) = {Wprime}; K W' = a0 u  <->  K|P| = a0 u/(1+u); max_P [P.A - W] = (a0^2/K)[u - ln(1+u)] (PAPER70's J, residual {leg})")

# ------------------------------------------------------------------ A1d: elimination of P: q = (1/K) div[ grad chi / (1 + |grad chi|/a0) ]
c1, c2, c3 = cs = sp.symbols("c1 c2 c3", real=True)                            # components of grad chi
cn = sp.sqrt(c1 ** 2 + c2 ** 2 + c3 ** 2)
Pel = [ci / (K * (1 + cn / a0)) for ci in cs]
Pn = sp.sqrt(sum(pi ** 2 for pi in Pel))
rhs = [sp.simplify(K * Wprime.subs(p, K * Pn) * Pel[i] / Pn - cs[i]) for i in range(3)]
check("A1d", all(r == 0 for r in rhs), "with P = grad chi/(K(1 + |grad chi|/a0)), K W'(K|P|) P/|P| = grad chi identically: "
      "the P equation inverts to the AQUAL-type constraint  div[grad chi/(1 + |grad chi|/a0)] = K q,  chi = Xi + gamma_L F'(q)")

# ------------------------------------------------------------------ A1e: no first integral while W is live
r = sp.symbols("r", positive=True); pr = sp.Function("p")(r)
dchi = K * Wprime.subs(p, K * pr)                                             # d chi/dr for a radial P = p(r) r^
state("A1e", "Bernoulli-type integral: Xi + gamma_L F'(q) = chi, and grad chi = K W'(K|P|) P^. chi is constant iff W' = 0, i.e. "
      "P = 0 or W dropped (AC15's screened PN regime). With W live, chi is fixed nonlocally by div[grad chi/(1+|grad chi|/a0)] = K q "
      f"(A1d): an elliptic constraint, not an algebraic integral along streamlines. Radial example: dchi/dr = {sp.simplify(dchi)} != 0 for p != 0. "
      "HE-a (Bernoulli only in the unscreened/PN limit; screened system = coupled PDE): HIT.")

# ------------------------------------------------------------------ A1f: stationary pattern in the body frame
s0 = sp.Function("s0"); sig_st = s0(x, y, z - V * t)
Xi_st = phi - sp.diff(sig_st, t) + sum(sp.diff(sig_st, v) ** 2 for v in xs3) / 2
vv = [-sp.diff(sig_st, v) for v in xs3]; w = [vv[0], vv[1], vv[2] - V]
r1f = sp.simplify(Xi_st - (phi + (sum(c ** 2 for c in w) - V ** 2) / 2))
q0 = sp.Function("q0"); qst = q0(x, y, z - V * t)
contst = sp.diff(qst, t) + sum(sp.diff(qst * vv[i], xs3[i]) for i in range(3)); divqw = sum(sp.diff(qst * w[i], xs3[i]) for i in range(3))
r1f2 = sp.simplify(contst - divqw)
check("A1f", r1f == 0 and r1f2 == 0, "stationary pattern sigma(x - V t), w = v - V z^: Xi = phi + (w^2 - V^2)/2 (AC15 S1b) and the khronon "
      "equation is div(q w) = 0 (AC15 KA2); both with W live, since neither touches the P equation")
state("A1 system", "CLOSED SYSTEM (body frame, aligned g_ext along z^; perpendicular: same equations with e^ = x^, not axisymmetric):\n"
      "   (1) div(q w) = 0,  w = -grad psi (irrotational),  w -> -V z^ at infinity\n"
      "   (2) Xi = phi + (w^2 - V^2)/2\n"
      "   (3) chi = Xi + gamma_L F'(q);   P = grad chi / (K (1 + |grad chi|/a0));   q = div P   (equivalently div[grad chi/(1+|grad chi|/a0)] = K q)\n"
      "   (4) lap phi = K (rho_b + q),  phi -> -g_ext . x far away;  grad chi -> A_h = x_e a0 e^ (the host's static khronon, A_h balances g_ext), q -> rho_h\n"
      "   Time-dependent form evolved in Stage B (the frame's momentum equation, the gradient of (2)-(3)):\n"
      "   Dw/Dt = -grad phi + grad chi - gamma_L grad F'(q),   d_t q + div(q w) = 0.\n"
      "   grad chi is the Legendre (W) force on the frame, absent from AC15; -grad phi includes the charge's own gravity, also absent from AC15.")

# ------------------------------------------------------------------ A1g: linear response about the host state (the force kernel used in Stage B)
A1, A2_, A3 = As = sp.symbols("A1 A2 A3", real=True); xe = sp.symbols("x_e", positive=True)
An = sp.sqrt(A1 ** 2 + A2_ ** 2 + A3 ** 2); Pvec = [Ai / (K * (1 + An / a0)) for Ai in As]
Jac = sp.Matrix([[sp.diff(Pvec[i], As[j]) for j in range(3)] for i in range(3)]).subs({A1: 0, A2_: 0, A3: xe * a0})
Jac = sp.simplify(Jac)
Dpar, Dperp = 1 / (K * (1 + xe) ** 2), 1 / (K * (1 + xe))
okg = sp.simplify(Jac - sp.diag(Dperp, Dperp, Dpar)) == sp.zeros(3)
Mth = sp.simplify(K ** 2 * sp.diff(W, p, 2).subs(p, a0 * xe / (1 + xe)))
check("A1g", okg and sp.simplify(Mth - K * (1 + xe) ** 2) == 0,
      f"dP/dA at A = x_e a0 e^: 1/(K(1+x_e)^2) along e^, 1/(K(1+x_e)) across (D10 Route F's mpar/mper); K^2 W''(K|P_h|) = {Mth} = AC15's K M_theta, M_theta = (1+x_e)^2")

# ------------------------------------------------------------------ A1h: static linear EFE response (the HEDGEHOG start of the galaxy cells) + PN orders
Sp, Sq = sp.symbols("S_par S_perp", positive=True); Gs, M = sp.symbols("G M", positive=True)
phit = -Gs * M / (sp.sqrt(Sp * Sq ** 2) * sp.sqrt(x ** 2 / Sq + y ** 2 / Sq + z ** 2 / Sp))
divS = sp.simplify(sp.diff(Sq * sp.diff(phit, x), x) + sp.diff(Sq * sp.diff(phit, y), y) + sp.diff(Sp * sp.diff(phit, z), z))
# flux through the ellipsoid x^2/Sq + y^2/Sq + z^2/Sp = R^2 -> change variables x = sqrt(Sq) X etc.: standard Coulomb, total 4 pi G M
check("A1h", divS == 0, "static linear EFE: K dq = div[D grad phi_t], lap phi_t = K(rho_b + dq)  =>  div[(I - D) grad phi_t] = K rho_b; "
      "for a point mass phi_t = -GM/(sqrt(S_par) S_perp sqrt(x^2/S_perp + y^2/S_perp + z^2/S_par)), S = I - D, is a vacuum solution "
      f"(div[S grad phi_t] = {divS} for r != 0; flux 4 pi G M by the change of variables x_i = sqrt(S_i) X_i); dq = lap phi_t / K outside the mass "
      "(the anisotropic EFE phantom). Stage B builds the HEDGEHOG start of B1-B4 as the discrete fixed point of this linear system on the grid.")
lapt = sp.simplify(sp.diff(phit, x, 2) + sp.diff(phit, y, 2) + sp.diff(phit, z, 2))
RES["statements"]["A1h_phantom_density"] = str(lapt) + "  / K"

# ------------------------------------------------------------------ A2: V = 0 reduces to the static screened law with external field (X1/SE2's solver, D10)
# D10 (doors_push_2026_10_22/D10_native_Lstar/d10_solver.py):  (L) lap Phi = K rho + div p,  (P_L) grad Phi + (Lam^2/2) grad(div p) = p/(1 - |p|),
# units a = 1 (Plummer scale), a0 = 1, p = K P / a0, Lam = L*/a.  Mine at V = 0: w = 0 -> Xi = phi; chi = phi + gamma_L F'(q); F'(q) = q (raw / blend branch q >= rho_DE).
pv = sp.symbols("p_v", positive=True); a_ = sp.symbols("a", positive=True)
KWp = sp.simplify(K * Wprime.subs(p, a0 * pv))                               # K W'(a0 p) = a0 p/(1 - p)
Lam = sp.symbols("Lambda", positive=True)
# (P_L): divide my P equation by a0 with lengths in a: gamma_L q / a0 = (K L*^2/2)(a0/K)(div_a p / a)/a0 ... = (L*^2/(2 a^2)) div_a p
gam_term = sp.simplify((K * (Lam * a_) ** 2 / 2) * (a0 / K) * (1 / a_) / a0 / a_ * a_ ** 0)   # coefficient of div_hat p in units of a0 after 1/a per gradient
okA2 = sp.simplify(KWp - a0 * pv / (1 - pv)) == 0 and sp.simplify(gam_term - Lam ** 2 / 2) == 0
check("A2", okA2, f"V = 0: w = 0, Xi = phi; the system (1)-(4) becomes  grad phi + gamma_L grad q = K W'(K|P|) P^,  q = div P,  lap phi = K(rho_b + q). "
      f"With p = K P/a0, lengths in a, accelerations in a0: K W'(a0 p) = {KWp} = p/(1-p) a0 and gamma_L q -> (Lambda^2/2) div p with Lambda = L*/a: "
      "exactly D10's (L) + (P_L), the solver X1 and SE2 graded with (AQUAL + EFE + screening at the floor; external field as the far-field "
      "boundary grad chi -> x_e a0 e^). Identical for the raw kink; the Pi^6 blend differs only where Pi < rho_DE (the switch surface; AC21/BL3: no label moved).")

# ------------------------------------------------------------------ A3: gravity off: the uniform wind is exact
# (i) rho_h = 0 trivially; (ii) any static host solution boosted is an exact stationary pattern: Galilean invariance of Xi and of continuity.
tp, xp, yp, zp = sp.symbols("tp xp yp zp", real=True); X1_, X2_, X3_, X4_ = Xd = sp.symbols("X1 X2 X3 X4", real=True)
sg = sp.Function("sg"); ph = sp.Function("ph"); qh = sp.Function("qh")
args = (xp + V * tp, yp, zp, tp)                                             # host-frame point of the body-frame point (x', t'); body at +V x^
def host(expr):                                                              # a host-frame expression in (X1..X4), as Subs at the mapped point
    return sp.Subs(expr, Xd, args)
d = lambda f_, k: sp.Derivative(f_(*Xd), Xd[k])
Xi_host = host(ph(*Xd) - d(sg, 3) + sum(d(sg, k) ** 2 for k in range(3)) / 2)
sig_b = sg(*args) + V * xp + V ** 2 * tp / 2; phi_b = ph(*args)              # sigma' = sigma + V x' + V^2 t'/2
Xi_body = phi_b - sp.diff(sig_b, tp) + sum(sp.diff(sig_b, v) ** 2 for v in (xp, yp, zp)) / 2
r3 = sp.simplify(sp.expand(Xi_body - Xi_host.doit()))
q_body = qh(*args); vb = [-sp.diff(sig_b, v) for v in (xp, yp, zp)]
cont_b = sp.diff(q_body, tp) + sum(sp.diff(q_body * vb[i], (xp, yp, zp)[i]) for i in range(3))
cont_h = host(d(qh, 3) + sum(sp.Derivative(qh(*Xd) * (-d(sg, k)), Xd[k]) for k in range(3)))
r3b = sp.simplify(sp.expand(cont_b - cont_h.doit()))
check("A3", r3 == 0 and r3b == 0, "gravity off (M = 0): (i) rho_h = 0: q = 0, P = 0, chi = const, w = -V is exact trivially; (ii) rho_h != 0: Xi and the "
      "khronon equation are Galilean invariant (sigma' = sigma + V.x' + V^2 t/2), so the static host solution (q_h = rho_h, A_h, P_h) boosted to "
      "w = -V is an exact stationary solution of (1)-(4) with the host's own P_h carrying div P_h = rho_h. The 'uniform rho_h with g_ext constant' "
      "cell is the local approximation of that host state; Stage B advects rho_h as the background and evolves dq = q - rho_h with the body's forces (KB3).")

# ------------------------------------------------------------------ A4: PN limit (W dropped, F raw) = AC15 S1b term by term
C_ = sp.symbols("C", real=True); rr, GM, rho_h, wmag = sp.symbols("r GM rho_h w", positive=True)
# W dropped: grad chi = 0 -> Xi + gamma q = C; far field q -> rho_h, w -> -V (w^2 -> V^2), phi -> 0: C = gamma rho_h = c_gal^2
q_pat = (C_ - (-GM / rr) - (wmag ** 2 - V ** 2) / 2) / gam                    # from Xi = phi + (w^2 - V^2)/2 with phi = -GM/r
Cval = gam * rho_h
S1b = (gam * rho_h + GM / rr + (V ** 2 - wmag ** 2) / 2) / gam                # AC15: gamma q = c_gal^2 + Phi_N + (V^2 - w^2)/2
r4 = sp.simplify(q_pat.subs(C_, Cval) - S1b)
check("A4", r4 == 0, "W -> 0 (screened PN regime, 2 M_theta (r/L*)^2 <= 1e-9) and F raw: grad chi = 0, so Xi + gamma q = C with C = gamma rho_h from the "
      "far field; with (2) and phi = -GM/r: gamma q = c_gal^2 + Phi_N + (V^2 - w^2)/2, AC15 S1b term by term (c_gal^2 = gamma rho_h, Phi_N = GM/r)")

# ------------------------------------------------------------------ A5 (reported): the cells' scales, from xf1_cells
C = XC.build()
json.dump(C, open(os.path.join(HERE, "xf1_cells.json"), "w"), indent=1, default=float)
P("\nA5 (reported, not a known answer): the cells' dimensionless scales (xf1_cells.json). gpar = GM/(L0 V^2) (deflection, = R_A/(2 L0)), "
  "M_inf = V/c_s (c_s^2 = gamma_L rho_h / (K/4piG)... = 2 pi G L*^2 rho_h), restoring/inertia = 4 pi G rho_h (1+x_e)^2 r^2/V^2 at the readout "
  "(the Legendre + self-gravity force of the background charge against V^2/r), stiff/Legendre = (L*/r)^2/(2(1+x_e)^2), gN/gext = the body's "
  "Newtonian field at the readout over the host field (linear-response validity).")
P(XC.table(C))
# PN orders of the dropped energy-density terms, per footing at the B1 readout (worst case: largest a0 r and c_s)
CL = XC.CL
pn = {}
for f in XC.FOOTS:
    rmax = max(r_["r_read_pc"][0] for r_ in C["cells"][f]["B1"]["rows"]) * XC.PC
    cs = max(d["c_s_kms"] for r_ in C["cells"][f]["B1"]["rows"] for d in r_["derived"]) * 1e3
    pn[f] = dict(W_over_Pi=XC.A0[f] * rmax / CL ** 2, gammaF_over_Pi=cs ** 2 / (2 * CL ** 2))
RES["PN_orders"] = pn
P(f"A1h PN orders of the foliation energy density n.n.T = Pi + W + gamma_L F (PAPER70 E5): W/(Pi c^2) ~ a0 r/c^2 = {pn['canonical']['W_over_Pi']:.1e} / "
  f"{pn['alt']['W_over_Pi']:.1e}, gamma_L F/(Pi c^2) = c_s^2/(2c^2) = {pn['canonical']['gammaF_over_Pi']:.1e} / {pn['alt']['gammaF_over_Pi']:.1e} "
  "at the farthest B1 readout: Pi alone sources the Newtonian potential at PN order, as in (4).")

ok = all(c["ok"] for c in RES["checks"].values())
RES["verdict"] = "A1 CLOSED SYSTEM: Stage B runs" if ok else "Stage A FAIL"
P(f"\nStage A overall {'PASS' if ok else 'FAIL'}: {RES['verdict']}. HE-a HIT (no first integral with W live; Bernoulli only in AC15's PN limit). "
  "Perpendicular g_ext: equations written (e^ = x^), not axisymmetric -> Stage B NOT RUN for it (declared). kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, "xf1_stageA.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, "xf1_stageA.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok else 1)
