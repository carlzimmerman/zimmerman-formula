#!/usr/bin/env python3
"""D9_uv_parent: causality of U(1)-dielectric parents of the law vs DSF-21's foliated Proca P.

Frozen criteria: FROZEN_CRITERIA.md (committed alone first).  kappa = 1/2 FITTED.  Footings never pooled.
Deterministic, no network, sympy + numpy.  D9_MUTATE=1 replaces the law's D(E) by the linear D = E.
"""
import json
import os
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("D9_MUTATE", "") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"d9_uv_parent{TAG}.out")
JS = os.path.join(HERE, f"d9_uv_parent_results{TAG}.json")

lines, results = [], {"mutate": MUTATE, "checks": {}, "numbers": {}}


def say(s=""):
    print(s)
    lines.append(s)


def check(cid, ok, value, line):
    results["checks"][cid] = {"pass": bool(ok), "value": str(value), "line": str(line)}
    say(f"{cid} {'PASS' if ok else 'FAIL'} {value} {line}")


# constants (sources in FROZEN_CRITERIA.md)
c = 2.998e8
GMsun = 1.32712e20
AU = 1.495979e11
pc = 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
LSTAR = {"24pc": 24 * pc, "1kpc": 1000 * pc}

# ---------------------------------------------------------------- symbols
E, g, a0, u, k, w = sp.symbols("E g a0 u k omega", positive=True)
Ev = sp.Matrix(sp.symbols("E1 E2 E3", real=True))
Bv = sp.Matrix(sp.symbols("B1 B2 B3", real=True))
bg = {Ev[0]: 0, Ev[1]: 0, Ev[2]: E, Bv[0]: 0, Bv[1]: 0, Bv[2]: 0}

# the law's constitutive relation (AG6C S0.1): D = a0 E/(a0+E), g = E, u = D
D_law = E if MUTATE else a0 * E / (a0 + E)


def hessians(L):
    """M = d2L/dEdE, C = d2L/dEdB, N = -d2L/dBdB at the background (E e_z, B = 0)."""
    M = sp.Matrix(3, 3, lambda i, j: sp.diff(L, Ev[i], Ev[j]).subs(bg))
    C = sp.Matrix(3, 3, lambda i, j: sp.diff(L, Ev[i], Bv[j]).subs(bg))
    N = sp.Matrix(3, 3, lambda i, j: -sp.diff(L, Bv[i], Bv[j]).subs(bg))
    return sp.simplify(M), sp.simplify(C), sp.simplify(N)


def disp_matrix(M, C, N, kvec, om):
    """A(om) dE = 0 from k x (N dB - C^T dE) + om (M dE + C dB) = 0, dB = k x dE / om (times om)."""
    cols = []
    for j in range(3):
        e = sp.zeros(3, 1)
        e[j] = 1
        dB_om = kvec.cross(e)  # om * dB
        col = kvec.cross(N * dB_om - om * C.T * e) + om**2 * M * e + om * C * dB_om
        cols.append(col)
    return sp.Matrix.hstack(*cols)


kx = sp.Matrix([k, 0, 0])  # k perpendicular to the background field e_z

say("D9_uv_parent: U(1)-dielectric parents vs DSF-21 Proca P (decoupling / principal-symbol limit)")
say(f"mode: {'MUTATE (linear D = E)' if MUTATE else 'primary'}")
say("")

# ---------------------------------------------------------------- U1 control
gN = sp.simplify(g - D_law.subs(E, g))
resU1 = sp.simplify(gN - g**2 / (g + a0))
check("U1", resU1 == 0, f"g-u-g^2/(g+a0)={resU1}", "residual exactly 0")

# ---------------------------------------------------------------- U2 Lorentz-invariant L(X,Y)
LX, LY, LXX, LXY, LYY, X0 = sp.symbols("L_X L_Y L_XX L_XY L_YY X0", real=True)
Xs = (Ev.dot(Ev) - Bv.dot(Bv)) / 2
Ys = Ev.dot(Bv)
dX = Xs - X0
L_LI = LX * dX + LY * Ys + LXX * dX**2 / 2 + LXY * dX * Ys + LYY * Ys**2 / 2
M, C, N = hessians(L_LI)
M, C, N = [m.subs(X0, E**2 / 2) for m in (M, C, N)]
A = disp_matrix(M, C, N, kx, w)
detA = sp.factor(sp.simplify(A.det()))
vX2_LI = LX / (LX + 2 * (E**2 / 2) * LXX)
resU2 = sp.simplify(detA.subs(w, k * sp.sqrt(vX2_LI)))
# eigenvector of the X mode: dE along e_z
vecres = sp.simplify(A.subs(w, k * sp.sqrt(vX2_LI)) * sp.Matrix([0, 0, 1]))
free_of = not any(s in vX2_LI.free_symbols for s in (LY, LXY, LYY))
okU2 = resU2 == 0 and all(sp.simplify(x) == 0 for x in vecres) and free_of
say(f"   M = {list(M)}\n   C = {list(C)}\n   N = {list(N)}")
say(f"   det A(omega) = {detA}")
check("U2", okU2, f"det(v_X^2=L_X/(L_X+2X L_XX))={resU2}; A*e_z={list(vecres)}; free of L_Y,L_XY,L_YY={free_of}",
      "residual 0, independent of L_Y, L_XY, L_YY")
results["numbers"]["U2_det_factored"] = str(detA)

# ---------------------------------------------------------------- U3 NG2 with the law's D
# L_X = D/E, L_X + 2X L_XX = dD/dE  (D = L_X E along the background, X = E^2/2)
eps_perp = sp.simplify(D_law / E)
eps_par = sp.simplify(sp.diff(D_law, E))
vX2_law = sp.simplify(eps_perp / eps_par)
resU3 = sp.simplify(vX2_law - (1 + E / a0))
check("U3", resU3 == 0, f"v_X^2={vX2_law}; minus (1+g/a0) = {resU3}", "residual exactly 0 (NG2 reproduced)")

# ---------------------------------------------------------------- U4 foliated L(E^2, B^2, E.B)
La, Lb, Lc, Laa, Lab, Lac, Lbb, Lbc, Lcc, a_0 = sp.symbols("L_a L_b L_c L_aa L_ab L_ac L_bb L_bc L_cc a_bg", real=True)
aa, bb, cc = Ev.dot(Ev) - a_0, Bv.dot(Bv), Ev.dot(Bv)
L_F = (La * aa + Lb * bb + Lc * cc + Laa * aa**2 / 2 + Lbb * bb**2 / 2 + Lcc * cc**2 / 2
       + Lab * aa * bb + Lac * aa * cc + Lbc * bb * cc)
MF, CF, NF = hessians(L_F)
MF, CF, NF = [m.subs(a_0, E**2) for m in (MF, CF, NF)]
AF = disp_matrix(MF, CF, NF, kx, w)
epsF_par, epsF_perp, NF_perp = MF[2, 2], MF[0, 0], NF[1, 1]
vX2_F = sp.simplify(NF_perp / epsF_par)
resU4_root = sp.simplify(AF.det().subs(w, k * sp.sqrt(vX2_F)))
vecF = sp.simplify(AF.subs(w, k * sp.sqrt(vX2_F)) * sp.Matrix([0, 0, 1]))
Lam = epsF_perp / NF_perp
# (a) Lorentz-invariant embedding: L(X,Y) as L(a,b,c) with X=(a-b)/2, Y=c
LI_map = {La: LX / 2, Lb: -LX / 2, Lc: LY, Laa: LXX / 4, Lbb: LXX / 4, Lab: -LXX / 4,
          Lac: LXY / 2, Lbc: -LXY / 2, Lcc: LYY}
resU4a = sp.simplify(Lam.subs(LI_map) - 1)
# cross-check the embedding reproduces U2's Hessians
emb_ok = all(sp.simplify(x) == 0 for x in list(MF.subs(LI_map) - M) + list(NF.subs(LI_map) - N)
             + list(CF.subs(LI_map) - C))
# (b) v_X^2 <= 1  <=>  Lambda_LV >= eps_perp/eps_par ; with the law, eps_perp/eps_par = 1 + g/a0
resU4b = sp.simplify(vX2_F * Lam - epsF_perp / epsF_par)  # v^2 = (eps_perp/eps_par)/Lambda exactly
okU4 = (resU4_root == 0 and all(sp.simplify(x) == 0 for x in vecF) and resU4a == 0 and emb_ok and resU4b == 0)
check("U4", okU4,
      f"root={resU4_root}; A_F*e_z={list(vecF)}; Lambda_LV(L(X,Y))-1={resU4a}; embedding={emb_ok}; v^2*Lambda-eps_perp/eps_par={resU4b}",
      "v_X^2 = N_perp/eps_par; Lambda_LV = 1 for L(X,Y); v_X^2<=1 <=> Lambda_LV >= 1+g/a0")
say(f"   foliated: eps_par={epsF_par}, eps_perp={epsF_perp}, N_perp={NF_perp}, Lambda_LV={sp.simplify(Lam)}")

# ---------------------------------------------------------------- U5 numeric cross-check
rng = np.random.default_rng(20261022)
syms = [La, Lb, Lc, Laa, Lab, Lac, Lbb, Lbc, Lcc, E, k]
detF = sp.lambdify([w] + syms, AF.det(), "numpy")
vfun = sp.lambdify(syms, vX2_F, "numpy")
worst = 0.0
ndraw = 0
while ndraw < 20:
    vals = list(rng.uniform(-1.0, 1.0, 9))
    vals[0] = abs(vals[0]) + 0.2  # L_a > 0 (positive eps_perp)
    vals[1] = -(abs(vals[1]) + 0.2)  # L_b < 0 (positive N)
    Eval, kval = rng.uniform(0.3, 2.0), rng.uniform(0.5, 3.0)
    v2 = vfun(*vals, Eval, kval)
    if not (v2 > 0):
        continue
    ndraw += 1
    # det is a polynomial in omega: find its roots numerically, pick the one closest to k*sqrt(v2)
    om = sp.Symbol("om")
    poly = sp.Poly(sp.expand(AF.det().subs(dict(zip(syms, vals + [Eval, kval]))).subs(w, om)), om)
    roots = np.roots([float(x) for x in poly.all_coeffs()])
    target = kval * np.sqrt(v2)
    best = min(abs(r - target) for r in roots) / target
    worst = max(worst, best)
check("U5", worst <= 1e-10, f"max rel diff {worst:.3e} over 20 draws", "<= 1e-10")

# ---------------------------------------------------------------- U6 numbers
g1AU = GMsun / AU**2
nums = {}
okU6 = True
for name, a0v in A0.items():
    lam_1AU = float(vX2_law.subs({E: g1AU, a0: a0v}))
    lam_a0 = float(vX2_law.subs({E: a0v, a0: a0v}))
    nums[name] = {"g_1AU": g1AU, "Lambda_LV_min_1AU": lam_1AU, "Lambda_LV_min_at_g_eq_a0": lam_a0,
                  "slow_bound_v_over_c_if_LV_minimal_1AU": 1 / np.sqrt(lam_1AU)}
    okU6 &= abs(lam_1AU - 1 - g1AU / a0v) / (1 + g1AU / a0v) <= 1e-12
    say(f"   {name}: a0={a0v:.3e}  required Lambda_LV >= {lam_1AU:.4e} at 1 AU (g={g1AU:.4e}); = {lam_a0:.4f} at g=a0")
results["numbers"]["U6"] = nums
check("U6", okU6, f"canonical {nums['canonical']['Lambda_LV_min_1AU']:.4e}, alt {nums['alt']['Lambda_LV_min_1AU']:.4e}",
      "Lambda_LV - 1 - g/a0 <= 1e-12 rel")

# ---------------------------------------------------------------- P1 A33-family principal reduction (round-2 sec. 4 L_pr)
eta, gam, beta, K, th = sp.symbols("eta gamma beta K theta", positive=True)
qd, PL, PT1, PT2 = sp.symbols("qdot P_L P_T1 P_T2", real=True)
y = sp.Matrix(sp.symbols("y1 y2 y3", real=True))
P = sp.Matrix([PL, PT1, PT2])
S0 = sp.diag(-beta / (2 * K), 1 / (4 * K), 1 / (4 * K))
Lkin = eta / 2 * (qd - P.dot(y))**2 + (y.T * S0 * y)[0] / 2
ysol = sp.solve([sp.diff(Lkin, yi) for yi in y], list(y), dict=True)[0]
Lred = sp.simplify(Lkin.subs(ysol))
Delta = 1 + eta * (P.T * S0.inv() * P)[0]
resP1a = sp.simplify(Lred - eta * qd**2 / (2 * Delta))
r0 = 2 * eta * u**2 / (K * beta)
Delta_u = Delta.subs({PL: u / K * sp.cos(th), PT1: u / K * sp.sin(th), PT2: 0})
resP1b = sp.simplify(sp.expand_trig(Delta_u - (1 - r0 + (1 + 2 * beta) * r0 * sp.sin(th)**2)))
check("P1", resP1a == 0 and resP1b == 0, f"L_red-(eta/2Delta)qdot^2={resP1a}; Delta(theta)-form={resP1b}",
      "residual 0 (reproduction of round-2 sec.4 algebra)")

# ---------------------------------------------------------------- P2 sup of the cone
v2_L = gam / eta * Delta_u
dv = sp.simplify(sp.diff(v2_L, th))
sup_theta = sp.simplify(v2_L.subs(th, sp.pi / 2))
okP2a = sp.simplify(sup_theta - gam / eta * (1 + 4 * eta * u**2 / K)) == 0
# Delta(theta) - Delta(pi/2) = -(1+2beta) r0 cos^2 <= 0  => max at pi/2 ; increasing in u => sup at u -> a0
diffmax = sp.simplify(Delta_u - Delta_u.subs(th, sp.pi / 2) + (1 + 2 * beta) * r0 * sp.cos(th)**2)
sup_all = sp.limit(sup_theta, u, a0)
okP2 = okP2a and diffmax == 0 and sp.simplify(sup_all - gam / eta * (1 + 4 * eta * a0**2 / K)) == 0
check("P2", okP2, f"sup v^2 = {sup_all}", "= (gamma/eta)(1+4 eta a0^2/K), finite")

# ---------------------------------------------------------------- P3 numbers at eta = gamma = K L*^2/2
excess_sym = sp.simplify((4 * eta * a0**2 / K).subs(eta, K * sp.Symbol("Ls")**2 / 2))
okP3 = True
p3 = {}
for ln, Ls in LSTAR.items():
    for fn, a0v in A0.items():
        ex = 2 * (Ls * a0v / c**2)**2
        p3[f"{ln}_{fn}"] = ex
        okP3 &= ex < 1e-12
        say(f"   A33 cone excess at eta=gamma, L*={ln}, {fn}: 2(L* a0/c^2)^2 = {ex:.3e}")
results["numbers"]["P3"] = p3
check("P3", okP3 and sp.simplify(excess_sym - 2 * sp.Symbol("Ls")**2 * a0**2) == 0,
      f"max {max(p3.values()):.3e}", "< 1e-12 at all four (L*, footing)")

# ---------------------------------------------------------------- P4 structural contrast in u
gu = sp.solve(sp.Eq(u, a0 * g / (a0 + g)), g)[0]  # law: u = a0 g/(a0+g)
U1factor = sp.simplify((1 + g / a0).subs(g, gu))
limU1 = sp.limit(U1factor, u, a0, dir="-")
limA33 = sp.limit(1 + 4 * eta * u**2 / K, u, a0)
okP4 = sp.simplify(U1factor - a0 / (a0 - u)) == 0 and limU1 == sp.oo and limA33.is_finite
check("P4", okP4, f"U(1): {U1factor} -> {limU1};  A33: -> {limA33}", "U(1) diverges at the cap; A33 finite")

# ---------------------------------------------------------------- G1 A33's P_T is physical
x1, x2, x3, epsl = sp.symbols("x1 x2 x3 epsilon", real=True)
Pg = sp.Matrix([1 + x2, x1 * x3, sp.Rational(1, 2) + x1**2])
Cg = sp.Matrix([x2 * x3, 0, x1 * x2])
curlC = sp.Matrix([sp.diff(Cg[2], x2) - sp.diff(Cg[1], x3), sp.diff(Cg[0], x3) - sp.diff(Cg[2], x1),
                   sp.diff(Cg[1], x1) - sp.diff(Cg[0], x2)])
Wf = lambda uu: (a0**2 / K) * (-uu / a0 - sp.log(1 - uu / a0))
Wshift = Wf(K * sp.sqrt((Pg + epsl * curlC).dot(Pg + epsl * curlC)))
dW = sp.simplify(sp.diff(Wshift, epsl).subs(epsl, 0))
dW_num = dW.subs({x1: sp.Rational(1, 3), x2: sp.Rational(1, 5), x3: sp.Rational(1, 7), a0: 10, K: 1})
check("G1", dW_num != 0, f"dW/d(eps) at a test point = {sp.nsimplify(dW_num)} (= {float(dW_num):.4e})",
      "not identically 0 => P_T physical in A33")

# ---------------------------------------------------------------- G2 counts (record-derived)
counts = {"A33 (A68 C6: 5 - 2 tensor)": 3, "AG6C C1 (massless U(1))": 2, "CFG938/CFG938' (chi, lambda elliptic)": 0}
results["numbers"]["G2_counts"] = counts
check("G2", len(set(counts.values())) == len(counts), f"{counts}", "pairwise distinct (record-derived, low weight)")

# ================================================================ AMENDMENT A1 (POST-RESULT) checks
say("")
say("--- AMENDMENT A1 (post-result): lower bounds that survive parity-odd mixing ---")
s = sp.Symbol("s", positive=True)


def bracket_check(AA, ep, eo, Np, Na, mix, pref):
    """det(A) at omega^2 = s k^2 equals pref*k^6*s*c*[(ep s - Np)(eo s - Na) - mix^2 s] for a constant c > 0."""
    d = sp.expand(AA.det().subs(w, k * sp.sqrt(s)))
    T = sp.expand((ep * s - Np) * (eo * s - Na) - mix**2 * s)
    cfac = sp.simplify(d / (pref * k**6 * s * T))
    return cfac, sp.simplify(T.subs(s, Np / ep) + mix**2 * Np / ep)


# V2: Lorentz-invariant L(X,Y); mixing m = E^2 L_XY
cV2, atX = bracket_check(A, M[2, 2], M[0, 0], N[1, 1], N[2, 2], E**2 * LXY, LX)
okV2 = cV2.is_constant() and cV2 > 0 and atX == 0 and sp.simplify(N[1, 1] / M[2, 2] - vX2_LI) == 0
say(f"   V2: det = L_X k^6 s * {cV2} * [(eps_par s - L_X)(L_X s - N_par) - (E^2 L_XY)^2 s];"
    f" bracket at s=L_X/eps_par = -(E^2 L_XY)^2 s (residual {atX})")
check("V2", okV2, f"const={cV2}; s_max >= L_X/eps_par = {vX2_law} with the law's D",
      "identity residual 0; s_max >= 1+g/a0, equality iff L_XY = 0")

# V4: foliated L(a,b,c); mixing m = 2 E^2 L_ac
cV4, atXF = bracket_check(AF, MF[2, 2], MF[0, 0], NF[1, 1], NF[2, 2], 2 * E**2 * Lac, 4 * La)
okV4 = cV4.is_constant() and cV4 > 0 and atXF == 0
check("V4", okV4, f"const={cV4}; s_max >= N_perp/eps_par = (eps_perp/eps_par)/Lambda_LV",
      "identity residual 0; causality needs Lambda_LV >= 1+g/a0 (necessary)")

# V5: numeric lower bound on the largest root
worst5 = np.inf
nd = 0
while nd < 20:
    vals = list(rng.uniform(-1.0, 1.0, 9))
    Eval, kval = rng.uniform(0.3, 2.0), rng.uniform(0.5, 3.0)
    sub = dict(zip(syms, vals + [Eval, kval]))
    ep_, eo_, Np_, Na_ = [float(x.subs(sub)) for x in (MF[2, 2], MF[0, 0], NF[1, 1], NF[2, 2])]
    if min(ep_, eo_, Np_, Na_) <= 0:
        continue
    nd += 1
    om = sp.Symbol("om")
    poly = sp.Poly(sp.expand(AF.det().subs(sub).subs(w, om)), om)
    roots = np.roots([float(x) for x in poly.all_coeffs()])
    om2 = max((r**2).real for r in roots if abs(r.imag) < 1e-9 * (1 + abs(r)))
    worst5 = min(worst5, om2 / (kval**2 * Np_ / ep_))
check("V5", worst5 >= 1 - 1e-10, f"min over 20 draws of omega_max^2/(k^2 N_perp/eps_par) = {worst5:.6f}", ">= 1 - 1e-10")

# ---------------------------------------------------------------- summary
FROZEN = ["U1", "U2", "U3", "U4", "U5", "U6", "P1", "P2", "P3", "P4", "G1", "G2"]
npass = sum(v["pass"] for v in results["checks"].values())
ntot = len(results["checks"])
nf = sum(results["checks"][c_]["pass"] for c_ in FROZEN)
nv = npass - nf
say("")
say(f"frozen checks: {nf}/{len(FROZEN)} PASS (U2/U4/U5 FAIL as frozen = parity-odd mixing, AMENDMENT A1); "
    f"post-hoc A1 checks: {nv}/{ntot - len(FROZEN)} PASS")
say(f"D9_UV_PARENT COMPLETE: {npass}/{ntot} checks PASS.")
results["summary"] = {"pass": npass, "total": ntot, "frozen_pass": nf, "frozen_total": len(FROZEN),
                      "A1_pass": nv, "A1_total": ntot - len(FROZEN)}
with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
with open(JS, "w") as f:
    json.dump(results, f, indent=1, default=str)
sys.exit(0 if npass == ntot else 1)
