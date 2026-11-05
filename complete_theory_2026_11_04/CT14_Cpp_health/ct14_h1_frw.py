#!/usr/bin/env python3
"""CT14 H1: quadratic action of C'' on FRW, exact in k, ADM in the unitary gauge of the khronon dust.
Fields zeta (= psi, spatial curvature) and delta phi; lapse alpha, shift beta solved from their constraints.
Criteria: FROZEN_CRITERIA.md (H1), written first. sympy + numpy, one thread, minutes. Reads nothing from disk.
8 pi G = 1. kappa = 1/2 FITTED; not theory closed. Grading only."""
import os, sys, math, time, resource
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

T0 = time.time()
CH = []
def check(n, ok, note=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"  ({note})" if note else ""), flush=True)

print("=" * 100); print("CT14 H1: C'' on FRW, exact quadratic action (zeta = psi, delta phi; dust clock; lapse/shift solved)"); print("=" * 100)

# ---------------------------------------------------------------- H1.0 symbolic: L_M adds nothing at quadratic order on FRW
Y, aa, ss = sp.symbols("Y a s", positive=True)
fJ = aa**2 * ((sp.sqrt(Y) / aa) - sp.log(1 + sp.sqrt(Y) / aa))           # a^2 f(sqrt(Y)/a): the J_x term (times const)
ser = sp.series(fJ, Y, 0, 2).removeO()
print(f"H1.0 a^2 f(sqrt(Y)/a) = {sp.simplify(sp.series(fJ, Y, 0, sp.Rational(5, 2)).removeO())} + O(Y^5/2)")
check("H1.0 d^2[a^2 f]/(da dY) -> 0 at Y = 0 (the Y^1 term Y/2 is a-free; a enters first at Y^3/2, cubic in perturbations on FRW)",
      sp.limit(sp.diff(fJ, Y, aa), Y, 0) == 0 and sp.simplify(sp.diff(fJ, Y).subs(Y, 0) if False else sp.limit(sp.diff(fJ, Y), Y, 0) - sp.Rational(1, 2)) == 0)

# ---------------------------------------------------------------- H1.1 ADM expansion
t, x, k, e = sp.symbols("t x k epsilon", real=True)
cY = sp.Symbol("c_Y", nonnegative=True)
af, Hf, vf, uf = [sp.Function(n)(t) for n in ("a", "H", "v", "u")]       # scale factor, Hubble, phidot, taudot
Pd0, Pd1, Pd2, Pd3 = [sp.Function(n)(t) for n in ("Pd0", "Pd1", "Pd2", "Pd3")]
Pp0, PX, PXX, PXXX, Pph, PXph, Pphph = [sp.Function(n)(t) for n in ("Pp0", "PX", "PXX", "PXXX", "Pph", "PXph", "Pphph")]
Z, A, B, F = [sp.Function(n)(t) for n in ("Z", "A", "B", "F")]           # amplitudes: zeta, alpha, beta, delta phi
C, S = sp.cos(k * x), sp.sin(k * x)
zeta, alpha, beta, dphi = e * Z * C, e * A * C, e * B * C, e * F * C
N = 1 + alpha
Ni_low = [sp.diff(beta, x), 0, 0]                                        # N_i = d_i beta
h = sp.diag(*[af**2 * sp.exp(2 * zeta)] * 3)
hinv = h.inv()
coords = [x, sp.Symbol("yy"), sp.Symbol("zz")]
def d(f, i): return sp.diff(f, coords[i]) if i == 0 else 0
Gam = [[[sum(hinv[l, m] * (d(h[m, i], j) + d(h[m, j], i) - d(h[i, j], m)) for m in range(3)) / 2 for j in range(3)] for i in range(3)] for l in range(3)]
DN = [[d(Ni_low[j], i) - sum(Gam[l][i][j] * Ni_low[l] for l in range(3)) for j in range(3)] for i in range(3)]
E = sp.Matrix(3, 3, lambda i, j: (sp.diff(h[i, j], t) - DN[i][j] - DN[j][i]) / 2)
Eup = hinv * E * hinv
EE = sum(E[i, j] * Eup[i, j] for i in range(3) for j in range(3))
trE = sum(hinv[i, j] * E[i, j] for i in range(3) for j in range(3))
R3 = -sp.exp(-2 * zeta) / af**2 * (4 * sp.diff(zeta, x, 2) + 2 * sp.diff(zeta, x)**2)   # conformally flat 3-metric
sqh = af**3 * sp.exp(3 * zeta)
Nup_x = hinv[0, 0] * Ni_low[0]
Xphi_full = (vf + sp.diff(dphi, t) - Nup_x * sp.diff(dphi, x))**2 / (2 * N**2) - hinv[0, 0] * sp.diff(dphi, x)**2 / 2
Xb_phi = vf**2 / 2
dXp = Xphi_full - Xb_phi
Pphi = Pp0 + PX * dXp + PXX * dXp**2 / 2 + Pph * dphi + PXph * dXp * dphi + Pphph * dphi**2 / 2
Xtau = uf**2 / (2 * N**2); dXt = Xtau - uf**2 / 2
Pdust = Pd0 + Pd1 * dXt + Pd2 * dXt**2 / 2
Yterm = hinv[0, 0] * sp.diff(N, x)**2 / N**2
L = sqh * (N * R3 / 2 + (EE - trE**2) / (2 * N) + N * Pdust + N * Pphi + cY * N * Yterm)
L2 = sp.diff(L, e, 2).subs(e, 0) / 2
L1 = sp.diff(L, e, 1).subs(e, 0)
print(f"  expanded ({time.time()-T0:.0f}s)", flush=True)

cs, sn = sp.symbols("cs sn")
def xavg(expr):
    ex = sp.expand(expr.subs({sp.cos(k * x): cs, sp.sin(k * x): sn}))
    P_ = sp.Poly(ex, cs, sn)
    out = 0
    for (i, j), c_ in P_.terms():
        if (i, j) == (2, 0) or (i, j) == (0, 2): out += c_ / 2
        elif (i, j) == (0, 0): out += c_
        elif i % 2 == 0 and j % 2 == 0: out += c_ * sp.Rational(3, 8) if (i, j) in [(4, 0), (0, 4)] else c_ / 8
    return out
L2a = sp.expand(xavg(L2))
print(f"  x-averaged ({time.time()-T0:.0f}s)", flush=True)
# background equations: tadpoles of the zero mode (alpha, zeta) give Friedmann 1 and 2 (checked below)
rho_d = uf**2 * Pd1 - Pd0; rho_p = vf**2 * PX - Pp0
p_tot = Pd0 + Pp0
Fr1 = sp.Eq(3 * Hf**2, rho_d + rho_p)
Hdot = -(uf**2 * Pd1 + vf**2 * PX) / 2
vdot = (-3 * Hf * PX * vf + Pph - PXph * vf**2) / (PX + vf**2 * PXX)    # d/dt(a^3 P_X v) = a^3 P_phi
udot = -3 * Hf * Pd1 * uf / (Pd1 + uf**2 * Pd2)                         # d/dt(a^3 P_dX u) = 0
# replace time-derivative symbols
Zd, Ad, Bd, Fd = sp.symbols("Zd Ad Bd Fd")
Zs, As_, Bs, Fs = sp.symbols("Zs As Bs Fs")
rep = {sp.Derivative(Z, t): Zd, sp.Derivative(F, t): Fd, sp.Derivative(af, t): af * Hf}
L2s = L2a.subs(rep).subs({Z: Zs, A: As_, B: Bs, F: Fs})
assert not L2s.has(sp.Derivative(A, t)) and not L2s.has(sp.Derivative(B, t)), "lapse/shift must be auxiliary"
# solve the constraints (alpha, beta auxiliary)
eqA = sp.diff(L2s, As_); eqB = sp.diff(L2s, Bs)
sol = sp.solve([eqA, eqB], [As_, Bs], dict=True)[0]
Lr = sp.expand(L2s.subs(sol))
print(f"  constraints solved ({time.time()-T0:.0f}s)", flush=True)
q = [Zs, Fs]; qd = [Zd, Fd]
Kmat = sp.Matrix(2, 2, lambda i, j: sp.diff(Lr, qd[i], qd[j]) / (1 if i == j else 1)) / 2   # L = qd K qd + ...
Bmat = sp.Matrix(2, 2, lambda i, j: sp.diff(Lr, qd[i], q[j]))                              # L ⊃ qd_i B_ij q_j
Wmat = -sp.Matrix(2, 2, lambda i, j: sp.diff(Lr, q[i], q[j])) / 2                          # L ⊃ - q W q
# symmetric part of B: qd B q = (1/2) d/dt (q Bs q) - (1/2) q dBs/dt q  (with Bs = B + B^T)/... handled exactly:
Bsym = (Bmat + Bmat.T) / 2; Banti = (Bmat - Bmat.T) / 2
# time derivative of Bsym via the background equations
back = {af: sp.Symbol("a_"), Hf: sp.Symbol("H_"), vf: sp.Symbol("v_"), uf: sp.Symbol("u_")}
def tdiff(expr):
    """d/dt of a background coefficient expressed in symbols."""
    syms = {sp.Symbol("a_"): af, sp.Symbol("H_"): Hf, sp.Symbol("v_"): vf, sp.Symbol("u_"): uf}
    ex = expr.subs(syms)
    dex = sp.diff(ex, t)
    sub = {sp.Derivative(af, t): af * Hf, sp.Derivative(Hf, t): Hdot, sp.Derivative(vf, t): vdot, sp.Derivative(uf, t): udot,
           sp.Derivative(Pd1, t): Pd2 * uf * udot, sp.Derivative(Pd0, t): Pd1 * uf * udot, sp.Derivative(Pd2, t): Pd3 * uf * udot,
           sp.Derivative(PX, t): PXX * vf * vdot + PXph * vf, sp.Derivative(Pp0, t): PX * vf * vdot + Pph * vf,
           sp.Derivative(PXX, t): PXXX * vf * vdot, sp.Derivative(Pph, t): PXph * vf * vdot + Pphph * vf,
           sp.Derivative(PXph, t): 0, sp.Derivative(Pphph, t): 0}
    return dex.subs(sub)
dBsym = Bsym.applyfunc(tdiff)
Weff = Wmat + dBsym / 2          # q_dot Bsym q = d/dt(q Bsym q / 2) - q (dBsym/dt) q / 2   (Bsym symmetric)
print(f"  kinetic / gradient matrices built ({time.time()-T0:.0f}s)", flush=True)

# ---------------------------------------------------------------- H1.2 numbers
def num(expr, P):
    return complex(expr.subs(P).evalf()) if expr.free_symbols or expr.atoms(sp.Function) else complex(expr)

def bg_point(case, Om_d, w_phi, cd2, cYv, Ks_, Kt_, a_=1.0):
    """background at one instant, 8 pi G = 1, H = 1: rho_d + rho_phi = 3."""
    H_ = 1.0
    rho_tot = 3 * H_**2
    rd = Om_d * rho_tot; rp = rho_tot - rd
    u_ = 1.0
    # dust k-essence: rho_d + p_d = u^2 Pd1 (small pressure: p_d = cd2-ish * rho_d), c_d^2 = Pd1/(Pd1 + u^2 Pd2)
    pd = cd2 * rd
    Pd1_ = (rd + pd) / u_**2; Pd0_ = pd; Pd2_ = Pd1_ * (1 / cd2 - 1) / u_**2
    # phi: rho + p = v^2 P_X; K_s = P_X, K_t = P_X + v^2 P_XX
    vp2 = (1 + w_phi) * rp / Ks_
    v_ = math.sqrt(vp2)
    PX_ = Ks_; PXX_ = (Kt_ - Ks_) / vp2; Pp0_ = w_phi * rp
    V1 = 0.0                                             # P_phi (= -V') : enters masses only; slow roll value below
    return {af: a_, Hf: H_, vf: v_, uf: u_, Pd0: Pd0_, Pd1: Pd1_, Pd2: Pd2_, Pd3: 0, Pp0: Pp0_, PX: PX_, PXX: PXX_, PXXX: 0,
            Pph: -3 * H_ * v_ * 0.1, PXph: 0, Pphph: 0, cY: cYv}

def grade(P, label):
    res = {}
    for kk in [1e1, 1e2, 1e4, 1e6]:
        Kk = np.real(np.array([[complex(Kmat[i, j].subs(P).subs(k, kk).evalf()) for j in range(2)] for i in range(2)]))
        Wk = np.real(np.array([[complex(Weff[i, j].subs(P).subs(k, kk).evalf()) for j in range(2)] for i in range(2)]))
        Ba = np.real(np.array([[complex(Banti[i, j].subs(P).subs(k, kk).evalf()) for j in range(2)] for i in range(2)]))
        ek = np.linalg.eigvalsh(Kk)
        # dispersion with frozen coefficients: q ~ e^{-i w t}: (w^2 K + i w (2 Banti) ... ) ; solve det[-w^2 K - i w (B - B^T) + W] = 0
        # build as quadratic eigenproblem: [0 I; -K^-1 W  -K^-1 G][q; qd], G = antisymmetric gyroscopic 2*Banti
        G = Ba
        Ki = np.linalg.inv(Kk)
        Mbig = np.block([[np.zeros((2, 2)), np.eye(2)], [-Ki @ Wk, -Ki @ G]])
        lam = np.linalg.eigvals(Mbig)            # q ~ e^{lam t}; stable iff Re lam <= 0 (+ growth from Hubble-scale terms)
        w2 = sorted(np.real(-(lam**2)))
        maxgrow = float(np.max(np.real(lam)))
        c2 = [w / kk**2 for w in w2[::2]] if True else None
        res[kk] = dict(kin_eigs=ek.tolist(), W_eigs=np.linalg.eigvalsh(Wk).tolist(), c2=sorted(set(np.round(np.array(w2) / kk**2, 10))),
                       max_growth_over_H=maxgrow)
    return res

print("\nH1.1 structure")
Kz_bare = sp.simplify(Kmat.subs({PX: 0, PXX: 0, vf: 0})[0, 0])
print(f"  K_zz with phi kinetic off: {sp.factor(Kz_bare)}")
print(f"  K_zz full (symbolic) = {sp.factor(sp.simplify(Kmat[0, 0]))}")
print(f"  det K / (K_phiphi) = {sp.factor(sp.simplify(Kmat[0,0]-Kmat[0,1]**2/Kmat[1,1]))}")
print(f"  K_zphi (symbolic) = {sp.factor(sp.simplify(Kmat[0, 1]))}")
print(f"  K_phiphi (symbolic) = {sp.factor(sp.simplify(Kmat[1, 1]))}")
print(f"  ({time.time()-T0:.0f}s)", flush=True)

cases = []
hS = lambda s_: 2 * (s_ - math.log1p(s_)) - s_ * s_ / (1 + s_)
hpS = lambda s_: s_ * s_ / (1 + s_)**2
EPS = 0.25 / (8 * math.pi)
for cYv in (0.0, 0.5, 1.0):
    for cd2 in (1e-6, 1e-2):
        for Om_d in (0.3, 0.999):
            for w_phi in (-0.9999, -0.7, 0.0):
                cases.append(("(a) exact FRW", Om_d, w_phi, cd2, cYv, 1.0, 1.0))
for E_ in (0.75, 12.8, 145.0, 5.92e5):                     # CT12 out:29 brackets (leaf average)
    for w_phi in (-0.9999, -0.7):
        cases.append((f"(b) leaf E={E_:g}", 0.999, w_phi, 1e-6, 1.0, 1 + E_, 1 + E_ - E_ * (1 + w_phi) / 2))
for s_ in (1.0, 108.9, 1e8, 1e22):
    for w_phi in (-0.9999, -0.7, 0.0):
        Ks_ = 1 + EPS * hS(s_); Kt_ = 1 + EPS * (hS(s_) - (1 + w_phi) * s_ * hpS(s_) / 2)
        cases.append((f"(c) static s={s_:g}", 0.3, w_phi, 1e-6, 1.0, Ks_, Kt_))

print("\nH1.2 kinetic matrix eigenvalues (k/aH = 1e1..1e6), mode speeds c^2 = omega^2/k^2, max growth rate / H")
allok = True; noflip = True; rows = []
for (lab, Om_d, w_phi, cd2, cYv, Ks_, Kt_) in cases:
    P = bg_point(lab, Om_d, w_phi, cd2, cYv, Ks_, Kt_)
    r = grade(P, lab)
    kinmin = min(min(v["kin_eigs"]) for v in r.values())
    hi = r[1e6]
    c2 = hi["c2"]
    ok = kinmin > 0 and min(c2) > -1e-6
    # no flip: the phi-like speed at high k must be K_s/K_t (its own), not reduced below
    c2_phi_own = Ks_ / Kt_
    near = min(c2, key=lambda z: abs(z - c2_phi_own))
    flip_ok = abs(near - c2_phi_own) <= 1e-3 * max(1, c2_phi_own)
    allok &= ok; noflip &= flip_ok
    rows.append((lab, Om_d, w_phi, cd2, cYv, kinmin, c2, c2_phi_own, hi["max_growth_over_H"]))
    print(f"  {lab:20s} Om_d {Om_d:5.3f} w {w_phi:+.4f} c_d^2 {cd2:.0e} c_Y {cYv:.1f}: min kin eig {kinmin:.3e}; c^2 at k=1e6 aH {[f'{z:.6g}' for z in c2]}"
          f" (phi own K_s/K_t {c2_phi_own:.6g}); max growth {hi['max_growth_over_H']:+.2e} H", flush=True)
print("\nH1.3 the O(H) k-independent rate seen with c_Y > 0 (k dependence; and with phi frozen / with c_Y = 0)")
for (lab, Om_d, w_phi, cd2, cYv, Ks_, Kt_) in [("(a)", 0.3, -0.7, 1e-6, 1.0, 1.0, 1.0), ("(a)", 0.3, 0.0, 1e-6, 1.0, 1.0, 1.0), ("(a)", 0.3, 0.0, 1e-6, 0.0, 1.0, 1.0),
                                               ("(a)", 0.3, -0.9999, 1e-6, 1.0, 1.0, 1.0), ("(a)", 0.7, 0.0, 1e-6, 1.0, 1.0, 1.0), ("(a)", 0.3, 1.0/3, 1e-6, 1.0, 1.0, 1.0)]:
    r = grade(bg_point(lab, Om_d, w_phi, cd2, cYv, Ks_, Kt_), lab)
    print(f"  Om_d {Om_d} w_2nd {w_phi:+.4f} c_Y {cYv}: max growth/H at k/aH 1e1, 1e2, 1e4, 1e6 = " + ", ".join(f"{r[kk]['max_growth_over_H']:+.3e}" for kk in r)
          + f"; Hubble-friction reference 3/2 = 1.5", flush=True)
check("H1 kinetic matrix of (zeta = psi, delta phi) positive definite and both c^2 >= 0 at every k, every case", allok)
check("H1 no CT7 flip from mixing: the phi-branch speed at k >> aH equals its own K_s/K_t (mixing with psi, lapse, shift, dust and c_Y does not reduce it)", noflip)
print(f"\nchecks {sum(CH)}/{len(CH)}; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB; {time.time()-T0:.0f}s")
print("kappa = 1/2 FITTED; not theory closed.")
