#!/usr/bin/env python3
"""C1_aest_embedding: is the screened theory's static sector a limit of an AeST-type action?

Run: OMP_NUM_THREADS=1 nice -n 10 python3 c1_aest_embedding.py       (C1_MUTATE=1 for the mutation)
Writes c1_aest_embedding.out / c1_aest_embedding_results.json (or *_MUTATE.*). Deterministic, no network.

AeST action (Skordis & Zlosnik, PRL 127 161302 (2021), arXiv:2007.00082, Eq. 5; external input, taken from the
record's transcription real_research/bridge1_aest_equations.md, NOT verified against a file on disk):
  S = int sqrt(-g)/(16 pi Gt) [ R - (K_B/2) F^2 + 2(2-K_B) J.dphi - (2-K_B) Y - F(Y,Q) - lambda(A.A+1) ] + S_m[g]
  J^mu = A^nu nabla_nu A^mu,  Y = q^{mu nu} d phi d phi,  q = g + A A,  Q = A^mu d_mu phi,
  F(Y,Q) = (2-K_B) Jf(Y) - K_2 (Q-Q_0)^2   (Lambda and the dust charge I_0 dropped: static, at the minimum).
Target (record): A33 MASTER_ACTION.md static weak field, p = K P, K = 4 pi G:
  L33 = -|grad Phi|^2/2K + P.grad Phi - W_full(u) - rho Phi - (gL/2)(div P)^2 - (gF/2)|curl P|^2,
  W_full = (a0^2/K)[-u/a0 - ln(1-u/a0)], u = K|P|, A33 has gL = gF = gamma = K L*^2/2.
"""
import json, os, sys, time
import sympy as sp
import numpy as np

MUT = os.environ.get("C1_MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUT else ""
OUT, RES = [], {"mutate": MUT, "checks": {}}
cJ = sp.Integer(1) if MUT else sp.Integer(2)   # coefficient of (2-K_B) J.dphi; AeST has 2


def say(s=""):
    print(s); OUT.append(s)


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": str(value), "threshold": str(thr)}
    say(f"{name} {'PASS' if ok else 'FAIL'} {value} {thr}")


t0 = time.time()
say("C1_aest_embedding" + ("  [MUTATE: J coefficient (2-K_B) instead of 2(2-K_B); +(gL/2)(lap chi)^2 in K5]" if MUT else ""))

# ---------------------------------------------------------------- K1: static weak-field limit of AeST
t, x, y, z = sp.symbols('t x y z'); X = [t, x, y, z]; S3 = [x, y, z]
e, Q0, KB, K2, Gt = sp.symbols('epsilon Q_0 K_B K_2 Gtilde', positive=True)
psi, phi, chi, a1, a2, a3, rho = [sp.Function(n)(x, y, z) for n in ['psi', 'phi', 'chi', 'a1', 'a2', 'a3', 'rho']]
avec = [a1, a2, a3]


def tr(ex, n=2):
    ex = sp.expand(ex)
    return sum(ex.coeff(e, k) * e**k for k in range(n + 1))


def ser(ex):
    return tr(sp.series(ex, e, 0, 3).removeO())


g = sp.diag(-(1 + 2*e*psi), *(3*[1 - 2*e*phi]))
gi = sp.diag(-ser(1/(1 + 2*e*psi)), *(3*[ser(1/(1 - 2*e*phi))]))
sqg = ser(sp.sqrt((1 + 2*e*psi)*(1 - 2*e*phi)**3))
d = lambda f, m: 0 if m == 0 else sp.diff(f, X[m])
Gam = [[[tr(sum(gi[l, s]*(d(g[s, m], n) + d(g[s, n], m) - d(g[m, n], s)) for s in range(4))/2)
         for n in range(4)] for m in range(4)] for l in range(4)]


def Ric(b, dd):
    r = sum(d(Gam[l][b][dd], l) for l in range(4)) - sum(d(Gam[l][b][l], dd) for l in range(4))
    r += sum(Gam[l][l][s]*Gam[s][b][dd] - Gam[l][dd][s]*Gam[s][b][l] for l in range(4) for s in range(4))
    return tr(r)


R = tr(sum(gi[b, b]*Ric(b, b) for b in range(4)))
asq = tr(sum(gi[i+1, i+1]*(e*avec[i])**2 for i in range(3)))
A0 = -ser(sp.sqrt((1 + 2*e*psi)*(1 + asq)))
Al = [A0] + [e*ai for ai in avec]
Au = [tr(gi[m, m]*Al[m]) for m in range(4)]
unit = sp.simplify(tr(sum(Au[m]*Al[m] for m in range(4))) + 1)
F = [[d(Al[n], m) - d(Al[m], n) for n in range(4)] for m in range(4)]
F2 = tr(sum(gi[m, m]*gi[n, n]*F[m][n]**2 for m in range(4) for n in range(4)))
J = [tr(sum(Au[n]*(d(Au[m], n) + sum(Gam[m][n][l]*Au[l] for l in range(4))) for n in range(4))) for m in range(4)]
dphi = [Q0] + [e*sp.diff(chi, s) for s in S3]
Jdphi = tr(sum(J[m]*dphi[m] for m in range(4)))
Q = tr(sum(Au[m]*dphi[m] for m in range(4)))
Y = tr(sum(gi[m, m]*dphi[m]**2 for m in range(4)) + Q**2)
V = [sp.diff(chi, S3[i]) + Q0*avec[i] for i in range(3)]
Yres = sp.simplify(Y - e**2*sum(v**2 for v in V))
B = tr(sqg*(R - KB/2*F2 + cJ*(2 - KB)*Jdphi - (2 - KB)*Y + K2*(Q - Q0)**2))
Bx = sp.expand(B)
fs = [psi, phi, chi, a1, a2, a3]
L0, L1, L2 = Bx.coeff(e, 0), Bx.coeff(e, 1), Bx.coeff(e, 2) - 16*sp.pi*Gt*rho*psi
grad = lambda f: [sp.diff(f, s) for s in S3]
dot = lambda u, v: sum(i*j for i, j in zip(u, v))
curla = [sp.diff(a3, y) - sp.diff(a2, z), sp.diff(a1, z) - sp.diff(a3, x), sp.diff(a2, x) - sp.diff(a1, y)]
# claimed reduced form (x 16 pi Gt); the Jf(Y) term rides on Y = eps^2 |V|^2 (MOND ordering: Jf counted O(eps^2))
Lclaim = (2*dot(grad(phi), grad(phi)) - 4*dot(grad(phi), grad(psi)) + KB*dot(grad(psi), grad(psi))
          - KB*dot(curla, curla) + 2*(2 - KB)*dot(grad(psi), V) - (2 - KB)*dot(V, V)
          + K2*Q0**2*psi**2 - 16*sp.pi*Gt*rho*psi)
from sympy.calculus.euler import euler_equations
E_act = euler_equations(L2, fs, S3); E_cl = euler_equations(Lclaim, fs, S3)
resK1 = [sp.simplify(p.lhs - q.lhs) for p, q in zip(E_act, E_cl)]
L1_is_divergence = all(sp.simplify(eq.lhs) == 0 for eq in euler_equations(L1, fs, S3))
nK1 = sum(1 for r in resK1 if r != 0)
say("  K1 reduced form (x16 pi Gt): 2|grad phi|^2 - 4 grad phi.grad psi + K_B|grad psi|^2 - K_B|curl a|^2"
    " + 2(2-K_B) grad psi.V - (2-K_B)|V|^2 - (2-K_B)Jf(|V|^2) + K_2 Q_0^2 psi^2 - 16 pi Gt rho psi,  V = grad chi + Q_0 a")
say(f"  K1 unit constraint residual {unit}; Y - eps^2|V|^2 = {Yres}; O(1) term {sp.simplify(L0)}; O(eps) term a divergence: {L1_is_divergence}")
check("K1", nK1 == 0 and unit == 0 and Yres == 0 and sp.simplify(L0) == 0 and L1_is_divergence,
      f"nonzero_EL_residuals={nK1}/6", "0/6 and unit=Yres=L0=0")
RES["K1_EL_residuals"] = [str(r) for r in resK1]
RES["K1_mass_term"] = "K_2 Q_0^2 psi^2 -> Poisson mass m^2 = K_2 Q_0^2/(2-K_B) (record transcription writes mu^2 = 2 K_2 Q_0^2/(2-K_B): K_2 convention, not load-bearing)"

# ---------------------------------------------------------------- K2: AQUAL mu = x/(1+x)
a0, gg, v, Yv, lam = sp.symbols('a_0 g v Y lambda_s', positive=True)
yv = sp.sqrt(Yv)/a0
Jf = 2*a0**2*(-yv - sp.log(1 - yv) - yv**2/2)          # the F we propose: F(Y,Q_0) = (2-K_B) Jf(Y)
Jp = sp.simplify(sp.diff(Jf, Yv).subs(Yv, v**2))
Jp_target = v/(a0 - v)
# phi = psi on shell; V algebraic (curl stiffness -> 0): grad psi - V = Jf'(|V|^2) V  =>  g = v (1 + Jf')
vsol = sp.solve(sp.Eq(gg, v*(1 + Jp_target)), v)
vsol = [s for s in vsol if sp.simplify(s.subs({gg: 1, a0: 1})) > 0][0]
mu = sp.simplify(1 - vsol/gg)
xg = gg/a0
res_mu = sp.simplify(mu - xg/(1 + xg))
J32 = sp.limit(Jf/Yv**sp.Rational(3, 2), Yv, 0)
J1 = sp.limit(Jf/Yv, Yv, 0)
res_SZ = sp.simplify(J32 - sp.limit(2*lam/(3*(1 + lam)*a0), lam, sp.oo))
G_N_over_Gt = 2/(2 - KB)   # Psi eq: div(grad Psi - V) = 8 pi Gt rho/(2-K_B) = 4 pi G rho
say(f"  K2 Jf(Y) = 2 a0^2[-y - ln(1-y) - y^2/2], y = sqrt(Y)/a0;  Jf'(v^2) - v/(a0-v) = {sp.simplify(Jp - Jp_target)}")
say(f"  K2 |V| = {vsol};  mu - x/(1+x) = {res_mu};  Jf ~ {J1}*Y + {J32}*Y^(3/2): SZ coefficient at lambda_s->inf residual {res_SZ}")
say(f"  K2 Newton's constant G = 2 Gt/(2-K_B) (the record transcription's Gt = (1-K_B/2) G_qs); cap Y < a0^2 = hard boundary (as A33's u < a0)")
check("K2", sp.simplify(Jp - Jp_target) == 0 and res_mu == 0 and res_SZ == 0 and J1 == 0,
      f"mu_res={res_mu},SZ_res={res_SZ},linear_Y_coeff={J1}", "all 0")
RES["K2"] = {"Jf": "2 a0^2 [-y - ln(1-y) - y^2/2], y=sqrt(Y)/a0", "lambda_s": "infinity (Newtonian regime is the cap)",
             "G": "2 Gt/(2-K_B)", "mu": str(mu)}

# ---------------------------------------------------------------- K3: map to A33 static Lagrangian
K, gL, gF, rr = sp.symbols('K gamma_L gamma_F rho0', positive=True)
P = [sp.Function(f'P{i}')(x, y, z) for i in (1, 2, 3)]
Ph = sp.Function('Phi')(x, y, z)
u = K*sp.sqrt(sum(p**2 for p in P))
Wfull = a0**2/K*(-u/a0 - sp.log(1 - u/a0))
divP = sum(sp.diff(P[i], S3[i]) for i in range(3))
curlP = [sp.diff(P[2], y) - sp.diff(P[1], z), sp.diff(P[0], z) - sp.diff(P[2], x), sp.diff(P[1], x) - sp.diff(P[0], y)]
L33 = (-dot(grad(Ph), grad(Ph))/(2*K) + dot(P, grad(Ph)) - Wfull - rho*Ph
       - gL/2*divP**2 - gF/2*dot(curlP, curlP))
# AeST reduced, phi = psi on shell, mass term dropped (r << 1/m), V = K P, curl a = curl V / Q_0
VK = [K*p for p in P]
JfV = Jf.subs(Yv, sum(w**2 for w in VK))
curlV = [K*c for c in curlP]
LA = ((-(2 - KB)*dot(grad(Ph), grad(Ph)) + cJ*(2 - KB)*dot(grad(Ph), VK) - (2 - KB)*dot(VK, VK)
       - (2 - KB)*JfV - KB*dot(curlV, curlV)/Q0**2)/(16*sp.pi*Gt) - rho*Ph)
Ksol = 8*sp.pi*Gt/(2 - KB)
gF_A = sp.simplify(Ksol*KB/((2 - KB)*Q0**2))
Dk = sp.Symbol('D_K', positive=True)                       # D_K = 2 - K_B > 0 (AeST requires K_B < 2)
diff3 = sp.simplify(sp.expand_log(sp.simplify((LA - L33).subs({gL: 0, gF: gF_A}).subs(K, Ksol).subs(KB, 2 - Dk)), force=True))
say(f"  K3 map: K P_i = d_i chi + Q_0 a_i (= q_i^mu d_mu phi),  Phi = Psi,  K = 8 pi Gt/(2-K_B) = 4 pi G")
say(f"  K3 AeST supplies gamma_F = K K_B/((2-K_B) Q_0^2) = {gF_A}  [=> L*_F^2 = 2 gamma_F/K = 2 K_B/((2-K_B) Q_0^2)],  gamma_L = 0")
say(f"  K3 L_AeST - L_A33(gamma_L=0, gamma_F as above) = {diff3}   (AeST mass term K_2Q_0^2 Psi^2 dropped: relative size (m r)^2)")
check("K3", diff3 == 0, f"residual={diff3}", "0")
RES["K3"] = {"gamma_F": "K K_B/((2-K_B) Q_0^2)", "Lstar_F^2": "2 K_B/((2-K_B) Q_0^2)", "gamma_L": "0",
             "field_map": "K P_i = q_i^mu d_mu phi ~ d_i chi + Q_0 a_i ; Phi = Psi ; clock D_i lnN <-> J^mu (aether acceleration)"}

# ---------------------------------------------------------------- K4: clock coefficient
# W''(0) = 1/K fixes P's normalisation from the Y term; the EH term fixes K; the J term then gives xi = cJ/2
xi = sp.simplify(cJ/2)
gN_xi = sp.simplify(gg*(a0 + xi*gg - xi**2*a0)/(a0 + xi*gg))   # A33 K5 deformed law
say(f"  K4 xi = (J.dphi coefficient)/(2 x Y coefficient) = {xi};  law at xi: g_N - g^2/(g+a0) = {sp.simplify(gN_xi - gg**2/(gg+a0))}")
check("K4", xi == 1, f"xi={xi}", "1 exactly")

# ---------------------------------------------------------------- K5: longitudinal stiffness theorem
k, c1, c2, c3, ps, VL, VT, aL, aT, ch, gLm = sp.symbols('k c1 c2 c3 psi_k V_L V_T a_L a_T chi_k gL_m', real=True)
lamL, lamT = sp.symbols('lambda_L lambda_T', real=True)   # generic algebraic (local) curvature of Jf about any background
sL, sT = c1 + c2 + c3, KB + c1
chi_of = (VL - Q0*aL)/k                                    # V_L = k chi + Q_0 a_L (Fourier, i absorbed)
Lk = (-(2 - KB)*((k*ps - VL)**2 + VT**2 + lamL*VL**2 + lamT*VT**2)
      - sL*k**2*aL**2 - sT*k**2*aT**2)
if MUT:
    Lk += -gLm/2*(k**2*chi_of)**2                          # mutation: (lap chi)^2
aLs = sp.solve(sp.diff(Lk, aL), aL)
LkL = sp.simplify(Lk.subs(aL, aLs[0]) if aLs else Lk)
LkL = sp.simplify(LkL.subs(aT, VT/Q0))
kerL = sp.simplify(-sp.diff(LkL, VL, 2)/2)
kerT = sp.simplify(-sp.diff(LkL, VT, 2)/2)
k2L = sp.simplify(sp.series(kerL, k, 0, 3).removeO().coeff(k, 2))
k2T = sp.simplify(sp.series(kerT, k, 0, 3).removeO().coeff(k, 2))
kdepL = sp.simplify(sp.diff(kerL, k))
say(f"  K5 longitudinal kernel (coefficient of V_L^2): {kerL};  k^2 coeff {k2L};  d/dk {kdepL}")
say(f"  K5 transverse kernel: {kerT};  k^2 coeff {k2T}  (pure AeST c1=0: K_B/Q_0^2)")
check("K5", k2L == 0 and kdepL == 0 and k2T != 0, f"k2_long={k2L},k2_trans={k2T}", "k2_long=0 and k2_trans!=0")
RES["K5"] = {"kernel_long": str(kerL), "kernel_trans": str(kerT)}

# ---------------------------------------------------------------- K6: consequence for the isolated Sun (record numbers)
d7d = json.load(open(os.path.join(ROOT, "doors_push_2026_10_22/D7d_screened_q2/d7d_screened_q2_results.json")))
def find(o, key):
    if isinstance(o, dict):
        if key in o: return o[key]
        for w in o.values():
            r = find(w, key)
            if r is not None: return r
    return None
bounds = find(d7d, "planet_bounds")
GM = 1.32712440018e20
foot = {"canonical": 9.36e-11, "alt": 1.13e-10}
k6, worst = {}, 0.0
for fn, A in foot.items():
    for pl, (r, bnd) in bounds.items():
        gN = GM/r**2
        gtot = 0.5*(gN + np.sqrt(gN**2 + 4*A*gN))
        anom = gtot - gN
        rec = find(d7d, f"{fn}|unscreened|{pl}")["no_turnoff"]
        rel = abs(anom/rec - 1); worst = max(worst, rel)
        k6[f"{fn}|{pl}"] = {"anomaly": anom, "D7d_no_turnoff": rec, "bound": bnd, "ratio_to_bound": anom/bnd}
        say(f"  K6 {fn:9s} {pl:6s} radial a_anom = {anom:.4e} m/s^2 (D7d {rec:.4e}); bound {bnd:.1e}; ratio {anom/bnd:.3e}")
check("K6", worst < 1e-3, f"max_rel_diff={worst:.2e}", "<1e-3")
RES["K6"] = k6

# ---------------------------------------------------------------- K7: hypersurface-orthogonal aether is not AQUAL off symmetry
r1 = sp.sqrt(x**2 + y**2 + z**2); r2 = sp.sqrt((x - 1)**2 + y**2 + z**2)
PhiT = -1/r1 - sp.Rational(3, 10)/r2 + sp.Rational(1, 5)*x            # non-symmetric test field, a0 = 1 units
gv = grad(PhiT); gm = sp.sqrt(dot(gv, gv)); muT = gm/(1 + gm)
VA = [(1 - muT)*c for c in gv]
cV = [sp.diff(VA[2], y) - sp.diff(VA[1], z), sp.diff(VA[0], z) - sp.diff(VA[2], x), sp.diff(VA[1], x) - sp.diff(VA[0], y)]
pt = {x: sp.Rational(1, 2), y: sp.Rational(7, 10), z: sp.Rational(3, 10)}
cnum = [float(c.subs(pt)) for c in cV]
cmag = float(np.linalg.norm(cnum)); Vmag = float(np.linalg.norm([float(c.subs(pt)) for c in VA]))
e2 = json.load(open(os.path.join(ROOT, "doors_push_2026_10_22/E2_field_equation/e2_field_equation_results.json")))
tfrac = find(e2, "transverse_fraction")
say(f"  K7 |curl V_AQUAL| = {cmag:.4e} at test point (|V| = {Vmag:.4e}); khronometric AeST forces curl V = 0. E2 transverse fraction (record) = {tfrac:.4f}")
check("K7", cmag > 1e-6, f"curlV={cmag:.3e}", ">0 (1e-6)")
RES["K7"] = {"curl_V_test": cmag, "E2_transverse_fraction": tfrac}

# ---------------------------------------------------------------- K8: static field content
Jac = sp.Matrix([[k, Q0, 0, 0], [0, 0, Q0, 0], [0, 0, 0, Q0]])    # (chi, a_L, a_T1, a_T2) -> (V_L, V_T1, V_T2)
null = 4 - Jac.rank()
say(f"  K8 static map (chi, a_L, a_T1, a_T2) -> V: rank {Jac.rank()}, nullity {null} (chi <-> a_L); content 3 = A33's P_i")
check("K8", null == 1, f"nullity={null}", "1")

npass = sum(1 for c in RES["checks"].values() if c["pass"]); ntot = len(RES["checks"])
RES["n_pass"], RES["n_checks"] = npass, ntot
RES["verdict"] = ("EMBEDS WITH EXTRA TERM: AQUAL mu=x/(1+x), the clock term (xi=1) and the curl stiffness gamma_F are AeST's static "
                  "limit (F(Y,Q0)=(2-K_B)Jf, lambda_s->inf, twisting aether); the longitudinal stiffness gamma_L(div P)^2 is "
                  "identically absent in AeST's class and must be added: one coefficient, a second-derivative operator "
                  "(q^{mu nu} nabla_mu nabla_nu phi + theta Q)^2 outside F(Y,Q). Without it the Sun is unscreened.") if (npass == ntot) else "see checks"
RES["runtime_s"] = round(time.time() - t0, 1)
say(f"C1_AEST_EMBEDDING COMPLETE: {npass}/{ntot} checks PASS.")
open(os.path.join(HERE, f"c1_aest_embedding{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"c1_aest_embedding_results{TAG}.json"), "w"), indent=1, default=str)
sys.exit(0 if npass == ntot else 1)
