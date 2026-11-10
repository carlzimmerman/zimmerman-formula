"""AKD1 decoupling-limit checks (independent of K4's unitary-gauge code). Criteria d88d310eb1.
(a) KA4 decoupling side: Minkowski, tau = Q0 (t + pi(t,x)), F(Q,Y) expanded: L2 = I(k) pi-dot^2 - B k^2 pi^2 with
    I(k) = FQQ Q0^2/2 + FY k^2 and B = FQ Q0/2 (read off by sympy from the covariant Q and Y).
(b) KA5: Newtonian gauge, quasi-static phi (psi = phi), SCS1's order counting: L2 = -k^2 phi^2/(2K) + (FQQ Q0^2/2 + FY k^2) chi^2
    - (FQ Q0/2) k^2 pi^2, chi = phi - pi-dot, where the chi^2 coefficient is read from the covariant expansion of Q and Y;
    the dispersion must equal SCS1's omega^2 = K G[(1 - K m) k^2 - mu^2 Q^2]/(mu^2 Q^2 + K m k^2), G = Q n, K m = 2 K FY,
    mu^2 Q^2 = K FQQ Q0^2 (relative 1e-12 at three k), hence TPA1 4.4 at K m = 1.
Env AKD1_MUTATE = MU3 drops FY (the KA4 ratio must then lose its k dependence).
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, json
import sympy as sp
MUT = os.environ.get("AKD1_MUTATE", "")
HERE = os.path.dirname(os.path.abspath(__file__))
out = {"mutate": MUT}
t, x = sp.symbols("t x", real=True)
eps, kk, Q0, Kg = sp.symbols("epsilon k Q0 K", positive=True)
FQ, FQQ, FY, F0 = sp.symbols("FQ FQQ FY F0")
FYuse = 0 if MUT == "MU3" else FY

def covariant_QY(gmat, tau):
    """Q and Y = h^{mn} d_m lnQ d_n lnQ for a 4D metric (coordinates t, x, y, z; fields depend on t, x)."""
    X = [t, x, sp.Symbol("y"), sp.Symbol("z")]
    gi = gmat.inv()
    du = [sp.diff(tau, X[i]) for i in range(4)]
    Q = sp.sqrt(-sum(gi[i, j]*du[i]*du[j] for i in range(4) for j in range(4)))
    nl = [-du[i]/Q for i in range(4)]
    nu = [sum(gi[i, j]*nl[j] for j in range(4)) for i in range(4)]
    h = [[gi[i, j] + nu[i]*nu[j] for j in range(4)] for i in range(4)]
    dl = [sp.diff(sp.log(Q), X[i]) for i in range(4)]
    Y = sum(h[i][j]*dl[i]*dl[j] for i in range(4) for j in range(4))
    return Q, Y, sp.sqrt(-gmat.det())

def second_order(expr):
    return sp.expand(sp.simplify(sp.diff(expr, eps, 2).subs(eps, 0)/2))

# ---------------- (a) Minkowski decoupling
pi = sp.Function("pi")(t, x)
g_mink = sp.diag(-1, 1, 1, 1)
Qa, Ya, sqa = covariant_QY(g_mink, Q0*(t + eps*pi))
Fa = F0 + FQ*(Qa - Q0) + FQQ*(Qa - Q0)**2/2 + FYuse*Ya
L2a = second_order(Fa)
pt, px, ptx = sp.diff(pi, t), sp.diff(pi, x), sp.diff(pi, t, x)
c_pt2 = sp.simplify(L2a.coeff(pt, 2)); c_px2 = sp.simplify(L2a.coeff(px, 2)); c_ptx2 = sp.simplify(L2a.coeff(ptx, 2))
rest_a = sp.simplify(L2a - c_pt2*pt**2 - c_px2*px**2 - c_ptx2*ptx**2)
print("(a) Minkowski decoupling, L2 = %s pi_t^2 + %s pi_x^2 + %s pi_tx^2 + [%s]" % (c_pt2, c_px2, c_ptx2, rest_a))
I_k = c_pt2 + c_ptx2*kk**2            # plane wave: pi_tx^2 -> k^2 pi_t^2
B_ = -c_px2
out["dec_inertia"] = str(I_k); out["dec_gradient_B"] = str(B_); out["dec_rest"] = str(rest_a)
ka4_dec = sp.simplify(I_k - (FQQ*Q0**2/2 + FY*kk**2)) if MUT != "MU3" else sp.simplify(I_k - (FQQ*Q0**2/2 + FY*kk**2))
ka4_B = sp.simplify(B_ - FQ*Q0/2)
print("    KA4 decoupling side: I(k) - (FQQ Q0^2/2 + FY k^2) =", ka4_dec, "; B - FQ Q0/2 =", ka4_B)
# K4 ratio from akd1_k4.json (unitary gauge, exact on FRW): A_z(k)/A_z(0) = 1 + 2 FY (k/a)^2 N0^2 / FQQ, N0 = 1/Q0, k/a -> k
k4 = json.load(open(os.path.join(HERE, "akd1_k4%s.json" % ("_MUTATE_MU3" if MUT == "MU3" else ""))))
dec_ratio = sp.simplify(I_k/I_k.subs(kk, 0))
k4_ratio_flat = 1 + 2*FYuse*kk**2/(FQQ*Q0**2)   # K4's printed ratio with k/a -> k, N0 -> 1/Q0
ka4_res = sp.simplify(dec_ratio - k4_ratio_flat)
out["KA4_dec_ratio"] = str(dec_ratio); out["KA4_ratio_residual"] = str(ka4_res)
out["KA4_K4_side_residual"] = k4.get("KA4_residual")
out["KA4_pass"] = (ka4_dec == 0 and ka4_B == 0 and ka4_res == 0 and k4.get("KA4_residual") == "0"
                   and sp.sympify(dec_ratio).has(kk))
print("    KA4: decoupling ratio", dec_ratio, " vs K4 ratio (flat):", k4_ratio_flat, " residual", ka4_res,
      " K4-side residual", k4.get("KA4_residual"), " -> PASS" if out["KA4_pass"] else " -> FAIL")

# ---------------- (b) Newtonian gauge, quasi-static phi, psi = phi
phi = sp.Function("phi")(x)      # quasi-static: no time dependence of the metric perturbation
g_newt = sp.diag(-(1 + eps*phi)**2, 1 - 2*eps*phi, 1 - 2*eps*phi, 1 - 2*eps*phi)
Qb, Yb, sqb = covariant_QY(g_newt, Q0*(t + eps*pi))
X1 = sp.simplify(sp.diff(sp.log(Qb/Q0), eps).subs(eps, 0))
Y2 = second_order(Yb)
chi = phi - pt
print("(b) Newtonian gauge: delta ln Q =", X1, ";  Y at second order - (d_x chi)^2 =", sp.simplify(Y2 - sp.diff(chi, x)**2))
out["newt_X1"] = str(X1); out["newt_Y2_minus_dchi2"] = str(sp.simplify(Y2 - sp.diff(chi, x)**2))
# SCS1 order counting: clock's chi^2 coefficient from FQQ (Q-Q0)^2/2 -> FQQ Q0^2 X1^2 / 2, FY Y -> FY (d chi)^2,
# gradient -(FQ Q0/2)(d pi)^2 (the n_d term), GR -|grad phi|^2/(2K); FQ-weighted terms without k^2 dropped (order q).
Ich = (FQQ*Q0**2/2) + FYuse*kk**2
w = sp.symbols("omega")
ph, pv = sp.symbols("ph pv")
# plane wave: phi = ph e^{ikx}, pi = pv e^{i(kx - w t)}; build the Hermitian quadratic form for (ph, pv)
chi_amp = ph - (-sp.I*w)*pv
Lpw = -kk**2*ph*sp.conjugate(ph)/(2*Kg) + Ich*chi_amp*sp.conjugate(chi_amp) - (FQ*Q0/2)*kk**2*pv*sp.conjugate(pv)
Lpw = sp.expand(Lpw.subs({sp.conjugate(ph): sp.Symbol("phc"), sp.conjugate(pv): sp.Symbol("pvc")}).subs(sp.conjugate(w), w))
phc, pvc = sp.symbols("phc pvc")
Mx = sp.Matrix([[sp.diff(Lpw, phc, ph), sp.diff(Lpw, phc, pv)], [sp.diff(Lpw, pvc, ph), sp.diff(Lpw, pvc, pv)]])
roots = sp.solve(sp.Eq(sp.simplify(Mx.det()), 0), w**2) if True else None
detw = sp.simplify(Mx.det())
w2 = sp.solve(detw.subs(w, sp.sqrt(sp.Symbol("W2"))), sp.Symbol("W2"))
w2 = [sp.simplify(r) for r in w2]
print("    dispersion omega^2 =", w2)
Gs = FQ*Q0                      # G = Q n (n = FQ)
Km = 2*Kg*FYuse
mu2Q2 = Kg*FQQ*Q0**2
scs1 = Kg*Gs*((1 - Km)*kk**2 - mu2Q2)/(mu2Q2 + Km*kk**2)
out["KA5_dispersion"] = [str(r) for r in w2]
rel = []
import mpmath as mp
mp.mp.dps = 40
vals = {Kg: mp.mpf(1.5), FQQ: mp.mpf("2.3e3"), FQ: mp.mpf("4.1e-4"), Q0: 1 + mp.mpf("1.7e-7"), FY: mp.mpf(1)/(2*mp.mpf(1.5))}
for kv in ("0.3", "30", "3e4"):
    vv = dict(vals); vv[kk] = mp.mpf(kv)
    a_ = [sp.N(r.subs(vv), 30) for r in w2]
    b_ = sp.N(scs1.subs(vv), 30)
    best = min(abs(complex(ai) - complex(b_)) for ai in a_)/abs(complex(b_))
    rel.append(float(best))
out["KA5_rel_at_k_0.3_30_3e4"] = rel
out["KA5_pass"] = max(rel) < 1e-12 and MUT != "MU3"
tpa = sp.simplify(scs1.subs(FY, 1/(2*Kg)) - (-Kg*Gs*(1 - kk**2/(mu2Q2 + kk**2))))
out["KA5_TPA1_4.4_residual_at_Km_1"] = str(tpa)
print("    KA5 vs SCS1 at K m = 1 (law, A = 0), k = 0.3 / 30 / 3e4: relative", ["%.1e" % r for r in rel],
      "; SCS1 at K m = 1 minus TPA1 4.4:", tpa, " -> PASS" if out["KA5_pass"] else " -> FAIL")
# the candidate in the same flat reading: K m -> 1 - R (unscreened law plus candidate); printed symbolically
R = sp.symbols("R", positive=True)
cand = sp.simplify(scs1.subs(FY, (1 - R)/(2*Kg)))
out["flat_dispersion_with_candidate"] = str(cand)
print("    flat (Newtonian, A = 0) dispersion with law + candidate, K m = 1 - R:", cand)
hk = sp.limit(cand/1, kk, sp.oo)
out["flat_high_k_limit"] = str(sp.simplify(hk))
print("    its high-k limit:", sp.simplify(hk), "(negative for R > 1: growth at rate^2 = K Q n R/(R - 1))")
json.dump(out, open(os.path.join(HERE, "akd1_dec%s.json" % ("_MUTATE_" + MUT if MUT else "")), "w"), indent=1, default=str)
