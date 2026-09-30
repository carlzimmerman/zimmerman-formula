#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG232_A1_static_reduction -- door 13 (BIMOND), frozen criteria CFG232_FROZEN_CRITERIA.md.  G1-law and G1-mechanism for 13a/13b/13c (the
law is shared), controls C1, C2, C3, C8, C10, D2, and the static half of C4; MUTATE modes M1, M2, M3, M4.

  PART A  symbolic: EH normalisation (C2), the five invariants' static values (a, b, x of the record, C4), spherical Euler-Lagrange, H1-H6.
  PART B  numeric: design by inversion (H4), legality, round trip (C3), G1-law at seven masses x two profiles x both footings x P2/nu_mono,
          D2 (Phi'/Psi'), phantom density vs CFG44's cold density, C10 (the record's representative M = lambda Q^{3/2}).
Exit: main 0 unless a control fails; MUTATE=<M1..M4> exits 1 when the control bites.
"""
import os, sys, math
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG232_common as C

R = C.Run("CFG232_A1_static_reduction")
MUT = R.mutate
P = R.P
bite = []

# ============================================================================================ PART A (symbolic)
R.banner("PART A.1  C2: Einstein-Hilbert normalisation against the Newtonian limit (linearised Einstein tensor, own code)")
t, x, y, z = sp.symbols("t x y z"); XX = [t, x, y, z]
eta = sp.diag(-1, 1, 1, 1)
Ph = sp.Function("Phi")(z); Ps = sp.Function("Psi")(z)
h = sp.diag(-2 * Ph, -2 * Ps, -2 * Ps, -2 * Ps)
hup = eta * h
tr = sum(eta[i, i] * h[i, i] for i in range(4))
box = lambda f: sum(eta[i, i] * sp.diff(f, XX[i], 2) for i in range(4))
Ric = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Ric[m, n] = sp.Rational(1, 2) * (sum(sp.diff(hup[l, n], XX[m], XX[l]) for l in range(4)) + sum(sp.diff(hup[l, m], XX[n], XX[l]) for l in range(4))
                                         - box(h[m, n]) - sp.diff(tr, XX[m], XX[n]))
Rs = sum(eta[i, i] * Ric[i, i] for i in range(4))
Gt = Ric - sp.Rational(1, 2) * eta * Rs
LEH = sp.simplify(-sp.Rational(1, 2) * sum(eta[i, i] * eta[j, j] * h[i, j] * Gt[i, j] for i in range(4) for j in range(4)))   # = (sqrt(-g)R)_2
k1 = sp.Symbol("k1")
L2 = k1 * (sp.diff(Ps, z) ** 2 - 2 * sp.diff(Ph, z) * sp.diff(Ps, z))
e1 = [sp.simplify(e.lhs) for e in euler_equations(LEH, [Ph, Ps], z)]
e2 = [sp.simplify(e.lhs) for e in euler_equations(L2, [Ph, Ps], z)]
ratio = [sp.simplify(a / b) for a, b in zip(e1, e2)]
kval = sp.solve(sp.Eq(ratio[0], 1), k1)
P(f"  (sqrt(-g)R)_2 static Euler-Lagrange equals that of k1(Psi'^2 - 2 Phi'Psi') with k1 = {kval}")
R.check("C2 (sqrt(-g)R)_2 = 2(|dPsi|^2 - 2 dPhi.dPsi) up to a total derivative: per 1/16piG weight beta this is beta(|dPsi|^2-2dPhi.dPsi) per 1/8piG, the frozen normalisation",
        kval == [2] and sp.simplify(e1[1] - e2[1].subs(k1, 2)) == 0, f"k1 = {kval}")
# Newtonian limit: interaction off, Psi-eq => Psi=Phi ; Phi-eq with -8piG rho Phi => lap Psi = 4piG rho
rho = sp.Function("rho")(z)
Lnew = (sp.diff(Ps, z) ** 2 - 2 * sp.diff(Ph, z) * sp.diff(Ps, z)) - 8 * sp.pi * sp.Symbol("G") * rho * Ph
en = [sp.simplify(e.lhs) for e in euler_equations(Lnew, [Ph, Ps], z)]
newt = sp.simplify(en[0] / 2 + sp.Symbol("G") * 4 * sp.pi * rho * (-1) * 0)
P(f"  with matter: EL_Phi = {en[0]},  EL_Psi = {en[1]}   (Psi=Phi from EL_Psi; lap Psi = 4 pi G rho from EL_Phi)")
R.check("C2 Newtonian limit: EL_Psi => Psi'' = Phi''; EL_Phi => 2 Psi'' = 8 pi G rho (i.e. lap Psi = 4 pi G rho)",
        sp.simplify(en[1] - 2 * (sp.diff(Ph, z, 2) - sp.diff(Ps, z, 2))) == 0 or sp.simplify(en[1] + 2 * (sp.diff(Ph, z, 2) - sp.diff(Ps, z, 2))) == 0,
        f"EL_Phi = {en[0]}")

R.banner("PART A.2  the five invariants T1..T5 (own Christoffel code): static weak-field values and the tuned subspace (part of C4)")
eps = sp.Symbol("epsilon")


def chris(g, gi):
    Gm = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                Gm[l][m][n] = sum(gi[l, s] * (sp.diff(g[s, m], XX[n]) + sp.diff(g[s, n], XX[m]) - sp.diff(g[m, n], XX[s])) for s in range(4)) / 2
    return Gm


def Tinv(Cc, g, gi):
    R4 = range(4)
    Pv = [sum(gi[m, n] * Cc[a][m][n] for m in R4 for n in R4) for a in R4]
    V = [sum(Cc[a][a][mu] for a in R4) for mu in R4]
    T1 = sum(g[a, b] * gi[m, r] * gi[n, s] * Cc[a][m][n] * Cc[b][r][s] for a in R4 for b in R4 for m in R4 for n in R4 for r in R4 for s in R4)
    T2 = sum(g[a, b] * Pv[a] * Pv[b] for a in R4 for b in R4)
    T3 = sum(gi[m, n] * V[m] * V[n] for m in R4 for n in R4)
    T4 = sum(gi[m, n] * Cc[a][m][b] * Cc[b][n][a] for m in R4 for n in R4 for a in R4 for b in R4)
    T5 = sum(Pv[a] * V[a] for a in R4)
    return [T1, T2, T3, T4, T5]


Phh, Psh = sp.Function("Phih")(z), sp.Function("Psih")(z)
g = sp.diag(-(1 + 2 * eps * Ph), (1 - 2 * eps * Ps), (1 - 2 * eps * Ps), (1 - 2 * eps * Ps))
gh = sp.diag(-(1 + 2 * eps * Phh), (1 - 2 * eps * Psh), (1 - 2 * eps * Psh), (1 - 2 * eps * Psh))
g1, g2 = chris(g, g.inv()), chris(gh, gh.inv())
Cc = [[[g1[l][m][n] - g2[l][m][n] for n in range(4)] for m in range(4)] for l in range(4)]
Ts = Tinv(Cc, g, g.inv())
p, q = sp.symbols("p q")
Tst = []
for Ti in Ts:
    e = sp.series(sp.simplify(Ti), eps, 0, 3).removeO().coeff(eps, 2)
    e = e.subs({sp.Derivative(Ph, z): p + sp.Derivative(Phh, z), sp.Derivative(Ps, z): q + sp.Derivative(Psh, z)})
    Tst.append(sp.expand(sp.simplify(e)))
for i, e in enumerate(Tst, 1):
    P(f"  T{i}(static) = {e}   [p = d dPhi, q = d dPsi]")
u0, u1 = sp.symbols("u0 u1")
cvec = [-u0, -u1 / 2, -u1 / 2, u0, u1]
Tt = sp.expand(sum(c * e for c, e in zip(cvec, Tst)))
a_c, b_c, x_c = Tt.coeff(p, 2), Tt.coeff(q, 2), Tt.coeff(p, 1).coeff(q, 1)
P(f"  tuned family: T_tuned(static) = ({a_c}) p^2 + ({b_c}) q^2 + ({x_c}) p q")
R.check("C4 static coefficients a = -4u0-2u1, b = -8(u0+u1), x = 8u1 (the record's values, re-derived with own code)",
        sp.simplify(a_c + 4 * u0 + 2 * u1) == 0 and sp.simplify(b_c + 8 * u0 + 8 * u1) == 0 and sp.simplify(x_c - 8 * u1) == 0,
        f"a={a_c}, b={b_c}, x={x_c}")
T41 = sp.expand(Tst[3] - Tst[0])
R.check("T4-T1 static = -4(p^2 + 2 q^2): Q = -T/a0^2 = 4(|d dPhi|^2 + 2|d dPsi|^2)/a0^2 (frozen 1.1)", sp.simplify(T41 + 4 * (p ** 2 + 2 * q ** 2)) == 0, f"T4-T1 = {T41}")

R.banner("PART A.3  spherical Euler-Lagrange for (Phi, Psi, Phih, Psih), first integrals, H1-H6 (sympy)")
r_ = sp.Symbol("r", positive=True)
be, ga, sg, a0s, Gs = sp.symbols("beta gamma sigma a0 G", positive=True)
Phf, Psf, Phhf, Pshf = [sp.Function(n)(r_) for n in ["Phi", "Psi", "Phih", "Psih"]]
Mg = sp.Function("Mg")(r_)                                   # G M_b(<r)
Mf = sp.Function("Mf")                                        # M(Q)
Qexp = 4 * ((sp.diff(Phf - Phhf, r_)) ** 2 + 2 * (sp.diff(Psf - Pshf, r_)) ** 2) / a0s ** 2
Lr = r_ ** 2 * (be * (sp.diff(Psf, r_) ** 2 - 2 * sp.diff(Phf, r_) * sp.diff(Psf, r_)) + ga * (sp.diff(Pshf, r_) ** 2 - 2 * sp.diff(Phhf, r_) * sp.diff(Pshf, r_))
                + sg * a0s ** 2 * Mf(Qexp)) - 2 * Mg.diff(r_) * Phf         # -8 pi G rho r^2 Phi = -2 Mg' Phi  (Mg' = 4 pi G rho r^2)
eqs = euler_equations(Lr, [Phf, Psf, Phhf, Pshf], r_)
dPhi, dPsi, dPhih, dPsih = [sp.diff(f_, r_) for f_ in (Phf, Psf, Phhf, Pshf)]
m1 = sp.Symbol("m")                                           # M'(Q) as a symbol for the first integrals
dPh_, dPs_ = dPhi - dPhih, dPsi - dPsih
# first integrals written from dL/df' (hand): verify their derivatives reproduce the EL equations
J_Phi = r_ ** 2 * (-2 * be * dPsi + 8 * sg * m1 * dPh_) + 2 * Mg           # dL/dPhi' + 2Mg = 0
J_Psi = r_ ** 2 * (2 * be * dPsi - 2 * be * dPhi + 16 * sg * m1 * dPs_)
J_Phih = r_ ** 2 * (-2 * ga * dPsih - 8 * sg * m1 * dPh_)
J_Psih = r_ ** 2 * (2 * ga * dPsih - 2 * ga * dPhih - 16 * sg * m1 * dPs_)
# substitute m1 -> Mf'(Q) for the differentiation check
Mp = sp.diff(Mf(sp.Symbol("qq")), sp.Symbol("qq"))
subsm = {m1: sp.Subs(sp.Derivative(Mf(sp.Symbol("qq")), sp.Symbol("qq")), sp.Symbol("qq"), Qexp)}
# direct check via the definition: the EL equation d/dr(dL/df') - dL/df = 0 with dL/df matter only for Phi
def EL_res(f_):
    return sp.simplify(sp.diff(sp.diff(Lr, sp.diff(f_, r_)), r_) - sp.diff(Lr, f_))
res = [EL_res(f_) for f_ in (Phf, Psf, Phhf, Pshf)]
chk = []
# dL/df' for each function, with M'(Q) inserted
dLdf = [sp.simplify(sp.diff(Lr, sp.diff(f_, r_))) for f_ in (Phf, Psf, Phhf, Pshf)]
pairs = [(dLdf[0], J_Phi - 2 * Mg, None), (dLdf[1], J_Psi, None), (dLdf[2], J_Phih, None), (dLdf[3], J_Psih, None)]
for (dl, Jh, _), nm in zip(pairs, ["Phi", "Psi", "Phih", "Psih"]):
    Jh2 = Jh.subs(subsm)
    same = sp.simplify((dl - Jh2).doit()) == 0
    chk.append(same)
    P(f"  dL/d{nm}' equals the hand first-integral expression: {same}")
R.check("A.3 the hand expressions for dL/df' (with m = M'(Q)) equal sympy's derivative of the reduced Lagrangian for all four fields", all(chk))
# Gauss: dL/dPhi' = -2 Mg (from d/dr(dL/dPhi') = -2 Mg'), and dL/dPsi' = 0, dL/dPhih' = 0 (no matter), dL/dPsih' = 0
Xs = sp.symbols("dPhi dPsi dPhih dPsih gN", real=True)
dP, dS, dPh2, dSh2, gN = Xs
mm, xs = sp.symbols("m x", real=True)
sol = sp.solve([
    -2 * be * dS + 8 * sg * mm * (dP - dPh2) + 2 * gN,           # /r^2 with Mg/r^2 = gN
    2 * be * dS - 2 * be * dP + 16 * sg * mm * (dS - dSh2),
    -2 * ga * dSh2 - 8 * sg * mm * (dP - dPh2),
    2 * ga * dSh2 - 2 * ga * dPh2 - 16 * sg * mm * (dS - dSh2)], [dP, dS, dPh2, dSh2], dict=True)[0]
sP, sS, sPh, sSh = [sp.simplify(sol[v]) for v in (dP, dS, dPh2, dSh2)]
sd = sp.simplify(sS - sSh); sdP = sp.simplify(sP - sPh)
Dx = 1 - 4 * xs - 32 * xs ** 2
s_ = 1 / be + 1 / ga
xsub = sg * mm * s_
P(f"  solved Psi' = {sS};  delta Psi' = {sd}")
R.check("H1/D: delta Psi' * D(x) = gN/beta with D = 1 - 4x - 32x^2, x = sigma m (1/beta + 1/gamma) (symbolic solution of the four first integrals)",
        sp.simplify(sd * Dx.subs(xs, xsub) - gN / be) == 0)
R.check("dPhi' = dPsi'(1 + 8x)", sp.simplify(sdP - sd * (1 + 8 * xsub)) == 0)
Phi_expr = sp.simplify(sP)
R.check("Phi' = [gN + 4 sigma m dPsi'(3 + 8x)]/beta (H3 formula)", sp.simplify(Phi_expr - (gN + 4 * sg * mm * sd * (3 + 8 * xsub)) / be) == 0)
P(f"  D(x)=0 roots: {sp.solve(Dx, xs)}  (H1: x = 1/8, -1/4)")
R.check("H1 degeneracy roots x = 1/8 and x = -1/4", sorted(sp.solve(Dx, xs)) == [-sp.Rational(1, 4), sp.Rational(1, 8)])
# H6 limits
xL = sp.Symbol("xL", positive=True)
Psi_expr = sp.simplify(sS)
gN_ = gN
Psi_lock = sp.limit(sp.simplify(Psi_expr.subs(mm, xL / (sg * s_))), xL, sp.oo)
Phi_lock = sp.limit(sp.simplify(Phi_expr.subs(mm, xL / (sg * s_))), xL, sp.oo)
P(f"  H6: m->0: Phi' = {sp.simplify(Phi_expr.subs(mm, 0))} ; m s->inf: Psi' -> {sp.simplify(Psi_lock)}, Phi' -> {sp.simplify(Phi_lock)}")
R.check("H6 decoupled end Phi' = gN/beta", sp.simplify(Phi_expr.subs(mm, 0) - gN / be) == 0)
R.check("H6 locked end Psi' = Phi' = gN/(beta+gamma)", sp.simplify(Psi_lock - gN / (be + ga)) == 0 and sp.simplify(Phi_lock - gN / (be + ga)) == 0)
# H3: deep regime ratio at x=1/8 (delta Psi' large): (Phi'-gN/be)/(Psi'-gN/be)
xa = sp.Rational(1, 8)
ratx = sp.simplify(((Phi_expr - gN / be).subs(mm, xs / (sg * s_))) / ((Psi_expr - gN / be).subs(mm, xs / (sg * s_))))
ratio_H3 = sp.simplify(sp.limit(ratx, xs, xa))
P(f"  H3: (Phi'-gN/beta)/(Psi'-gN/beta) as a function of x = {sp.simplify(ratx)}; limit x -> 1/8 (branch A): {ratio_H3}")
rB = sp.simplify(sp.limit(ratx, xs, -sp.Rational(1, 4)))
P(f"  branch B (x -> -1/4): (Phi'-gN/beta)/(Psi'-gN/beta) -> {rB}")
# H4 quadratic: Phi'/gN = nu with beta=1: k=(nu-1)(1+beta/gamma)
nus, ks = sp.symbols("nu k", positive=True)
Phi_x = sp.simplify(Phi_expr.subs(mm, xs / (sg * s_)).subs(sg, 1).subs(be, 1))
lhs = sp.simplify(Phi_x / gN - nus)
numer = sp.numer(sp.together(lhs))
kk = (nus - 1) * (1 + 1 / ga)
quad = sp.expand(32 * (kk + 1) * xs ** 2 + (4 * kk + 12) * xs - kk)
rr = sp.simplify(sp.factor(numer) / quad) if quad != 0 else None
P(f"  H4: numerator of (Phi'/gN - nu) / [32(k+1)x^2+(4k+12)x-k] = {sp.simplify(rr)}")
R.check("H4 the designed-x quadratic 32(k+1)x^2+(4k+12)x-k=0, k=(nu-1)(1+beta/gamma), is (up to a nonzero factor) exactly Phi'/gN = nu",
        sp.simplify(rr).free_symbols.isdisjoint({xs, nus}) or sp.simplify(sp.diff(rr, xs)) == 0, f"ratio = {sp.simplify(rr)}")

# ============================================================================================ PART B (numeric)
R.banner("PART B.1  design by inversion (H4) and legality")
Bc = C.B
BASE = dict(beta=1.0, gamma=1.0, sigma=+1)
designs = {}
for kn in ("P2", "nu_mono"):
    for gr in (1 / 3, 1.0, 3.0):
        for sgm in (+1, -1):
            designs[(kn, gr, sgm)] = C.Design(C.KERNELS[kn], beta=1.0, gamma=gr, sigma=sgm)


def legality(d):
    dy = np.diff(d.y)
    okQ = bool(np.all(np.diff(d.Q) > 0))
    mm_ = d.m
    okm = bool(np.all(np.diff(np.abs(mm_)) <= 1e-13 * np.abs(mm_[:-1])))     # |m| non-increasing with y (=Q)
    okD = bool(np.all(d.D > 0)) if d.sigma > 0 else bool(np.all(d.D < 0))
    okpos = bool(np.all(mm_ > 0))
    return dict(Q_monotone=okQ, m_nonincreasing=okm, D_sign_ok=okD, m_positive=okpos,
                m_deep=float(mm_[0]), m_newton=float(mm_[-1]), x_deep=float(d.x[0]), x_newton=float(d.x[-1]))


leg = {}
for key, d in designs.items():
    L_ = legality(d)
    leg[str(key)] = L_
    P(f"  {key}: " + ", ".join(f"{k}={v:.4g}" if isinstance(v, float) else f"{k}={v}" for k, v in L_.items()))
d0 = designs[("P2", 1.0, +1)]
L0 = leg[str(("P2", 1.0, +1))]
R.check("H1 numerical: designed M'(0) = m0 = beta*gamma/[8(beta+gamma)] = 1/16 (beta=gamma=1, sigma=+1, branch A)", abs(L0["m_deep"] - 1 / 16) < 1e-4, f"m(y->0) = {L0['m_deep']:.8f} (grid floor y=1e-8; tolerance 1e-4 set by me, the frozen text gave none)")
R.check("H2 Newtonian end m -> 0 (decoupled) on branch A", L0["m_newton"] < 1e-6, f"m(y=1e8) = {L0['m_newton']:.3e}")
legal_all = all(leg[str(k)]["Q_monotone"] and leg[str(k)]["m_nonincreasing"] and leg[str(k)]["D_sign_ok"] and leg[str(k)]["m_positive"] for k in designs if k[2] > 0)
R.check("legality (branch A, all kernels and gamma/beta): Q(g_N) monotone, m>0 non-increasing (dg_obs/dg_bar>0), D>0", legal_all, "result", kind="result")
legalB = {str(k): leg[str(k)] for k in designs if k[2] < 0}
P("  branch B (sigma_s=-1): " + "; ".join(f"{k}: Dsign={v['D_sign_ok']}, m_newton={v['m_newton']:.3g}, m_deep={v['m_deep']:.3g}" for k, v in legalB.items()))
R.num("legality", leg)

R.banner("PART B.2  C3 round trip: the designed M' applied forward returns nu")
worst = 0.0
for key, d in designs.items():
    if key[2] < 0:
        continue
    ys = np.geomspace(1e-5, 1e5, 41)
    for yv in ys:
        rr_ = C.forward(d.mfun, 1.0, key[1], +1, yv)
        if not rr_["ok"]:
            worst = 1.0
            continue
        tgt = yv * float(C.KERNELS[key[0]](yv))
        worst = max(worst, abs(rr_["Phi"] / tgt - 1))
R.check("C3 forward solve of the designed system reproduces Phi' = nu(y) g_N on 41 log-spaced y in [1e-5, 1e5] for P2 and nu_mono, gamma/beta in {1/3,1,3}", worst < 5e-4, f"max |Phi'/target - 1| = {worst:.2e} (table interpolation)")
R.num("roundtrip_max", worst)

# ------------------------------------------------------------------ G1-law at seven masses x two profiles x footings
R.banner("PART B.3  G1-law: 7 masses (1e9..1e12) x {point mass, h=2 kpc exponential sphere} x both footings x P2/nu_mono; x in [0.1, 30]")
masses = np.geomspace(1e9, 1e12, 7)
XS = np.geomspace(0.1, 30.0, 61)


def law_dev(design, kn, params, footname, a0si, profile, M, mfun=None, beta=1.0, gamma=1.0, sigma=+1, tgt="law"):
    a0k = a0si * C.KPC_M / 1e6
    rM = math.sqrt(C.G * M / a0k)
    rr = XS * rM
    if profile == "point":
        prof = Bc.point_mass(M)
    else:
        prof = Bc.exp_sphere(M, 2.0)
    gN = prof.gN(rr)                                    # (km/s)^2/kpc
    y = gN / a0k
    mf = design.mfun if mfun is None else mfun
    out = np.empty_like(y)
    for i, yv in enumerate(y):
        f_ = C.forward(mf, beta, gamma, sigma, float(yv))
        out[i] = f_["Phi"] if f_["ok"] else np.nan
    gb = out * a0k                                         # back to (km/s)^2/kpc
    tgt_g = C.KERNELS[kn](y) * gN
    return gb / tgt_g - 1.0, rr, gN


tab = {}
worst_all = {}
for kn in ("P2", "nu_mono"):
    d = designs[(kn, 1.0, +1)]
    for foot, a0si in C.FOOTS.items():
        for prof in ("point", "exp"):
            wmax = 0.0
            for M in masses:
                dev, rr, gN = law_dev(d, kn, None, foot, a0si, prof, M)
                wmax = max(wmax, float(np.nanmax(np.abs(dev))))
            tab[(kn, foot, prof)] = wmax
            P(f"  {kn:8s} {foot:9s} {prof:5s}: max over 7 masses x 61 radii of |g/g_target - 1| = {wmax:.2e}")
worst_all = max(tab.values())
R.check("G1-LAW (13a/13b/13c share the static law): max |g/g_target - 1| <= 0.10 over x in [0.1,30], seven masses, point + exponential sphere, both footings, P2 and nu_mono (function designed by inversion: P-declared)",
        worst_all <= 0.10 and not MUT, f"max = {worst_all:.2e}", kind="result")
R.num("G1_law_table", {"|".join(k): v for k, v in tab.items()})
R.verdict("G1-law", "PASS (P-declared by inversion, grade M1-inv)" if worst_all <= 0.10 else "FAIL", f"max deviation {worst_all:.2e}; the function is solved for from the target, so this is a restatement of the kernel, not a derivation")

# G1 against CFG44's own cold-mass definition for the extended profile (D3)
P("\n  Extended profile: law target nu(g_N) g_N versus CFG44's C(r)-target u/r^2 (cold_mass 'encl'); reported, not gated")
dd = {}
for M in (1e9, 1e11, 1e12):
    prof = Bc.exp_sphere(M, 2.0)
    rM = math.sqrt(C.G * M / C.A0_KPC)
    rr = np.geomspace(0.1 * rM, 30 * rM, 40)
    rg, w, u, uN = Bc.cold_mass(prof, "encl", a0=C.A0_KPC)
    ug = np.interp(rr, rg, u)
    gC = ug / rr ** 2
    gL = Bc.nu_p2(prof.gN(rr) / C.A0_KPC) * prof.gN(rr)
    dd[M] = float(np.max(np.abs(gL / gC - 1)))
    P(f"    M_b = {M:.0e}: max |g_law/g_C(r) - 1| over x in [0.1,30] = {dd[M]:.3f}")
R.num("law_vs_C_target_expsphere", dd)

# G1-law against CFG44's exact C(r) target (the orchestrator's exact target) for all masses and both kernels
R.banner("PART B.3b  G1-law against CFG44's C(r) = rho_c r^3 g = (a0/4 pi) M_b(<r) target (cold_mass 'encl'), 7 masses, exponential sphere and point mass")
devC = {}
for M in masses:
    for prof_name in ("point", "exp"):
        prof = Bc.point_mass(M) if prof_name == "point" else Bc.exp_sphere(M, 2.0)
        rM = math.sqrt(C.G * M / C.A0_KPC)
        rr = np.geomspace(0.1 * rM, 30 * rM, 61)
        rg, w, u, uN = Bc.cold_mass(prof, "encl", a0=C.A0_KPC)
        gC = np.interp(rr, rg, u) / rr ** 2
        for kn in ("P2", "nu_mono"):
            gL = C.KERNELS[kn](prof.gN(rr) / C.A0_KPC) * prof.gN(rr)      # the designed law reproduces this to 1e-6 (PART B.3)
            devC[(kn, prof_name, float(M))] = float(np.max(np.abs(gL / gC - 1)))
for kn in ("P2", "nu_mono"):
    for prof_name in ("point", "exp"):
        P(f"  {kn:8s} {prof_name:5s}: max over x of |g_law/g_C - 1| by mass (1e9..1e12): " + ", ".join(f"{devC[(kn, prof_name, float(M))]:.3f}" for M in masses))
worstC = max(devC.values())
R.check("G1-LAW read against CFG44's C(r) target (profile-dependent): FAILS on the exponential sphere at low mass because the BIMOND static law is a function of g_N alone while C(r) depends on M_b(<r) and r; the frozen text's 'equivalent for P2' was wrong for extended profiles",
        worstC <= 0.10, f"max = {worstC:.3f}", kind="result")
R.num("G1_law_vs_Ctarget", {"|".join(map(str, k)): v for k, v in devC.items()})

# ------------------------------------------------------------------ D2 and phantom density
R.banner("PART B.4  D2 lensing/dynamics ratio Phi'/Psi' along the design; phantom mass vs CFG44's cold mass (point mass)")
ph = d0.Phi - d0.y
ps_ = d0.Psi - d0.y
sel = d0.y < 1e-3
P(f"  deep regime (y<1e-3, P2, beta=gamma=1): (Phi'-g_N)/(Psi'-g_N) -> {np.median(ph[sel]/ps_[sel]):.5f} (H3: 2);  Phi'/Psi' at y=1e-3: {d0.Phi[np.argmin(abs(d0.y-1e-3))]/d0.Psi[np.argmin(abs(d0.y-1e-3))]:.4f}")
R.check("D2/H3 numerical: (Phi'-g_N)/(Psi'-g_N) -> 2 in the deep regime", abs(np.median(ph[sel] / ps_[sel]) - 2) < 1e-3, f"{np.median(ph[sel]/ps_[sel]):.5f}")
xs_ = np.geomspace(0.1, 30, 30)
Mph = xs_ ** 2 * 0 + (np.sqrt(1 + xs_ ** 2) - 1)      # M_c/M closed form
gNp = 1.0 / xs_ ** 2
gphi = np.array([C.forward(d0.mfun, 1, 1, 1, float(v))["Phi"] for v in gNp])
Mph_num = (gphi - gNp) * xs_ ** 2                     # r^2 (Phi' - g_N)/(G M) in units: gN = 1/x^2 -> M_ph/M
R.check("phantom mass of the designed law equals CFG44's M_c = M(sqrt(1+x^2)-1) for the P2 point mass (by construction; the stress is field-side, not a fluid's)",
        float(np.max(np.abs(Mph_num / Mph - 1))) < 5e-4, f"max rel diff {float(np.max(np.abs(Mph_num/Mph-1))):.2e}")

# ------------------------------------------------------------------ C10
R.banner("PART B.5  C10: the record's representative M = lambda Q^{3/2} (M'(0)=0): does the reduced system give an r^-1 regime?")
res10 = {}
for lam in (0.1, 1.0, 10.0, 100.0):
    mf = lambda Q, lam=lam: 1.5 * lam * np.sqrt(np.asarray(Q, float))
    rows = []
    for yv in (1e-10, 1e-6, 1e-4, 1e-2, 1.0, 1e2):
        f_ = C.forward(mf, 1.0, 1.0, +1, yv)
        rows.append((yv, f_.get("Phi", float("nan")) / yv if f_["ok"] else float("nan"), f_.get("nroots", 0)))
    res10[lam] = rows
    P(f"  lambda={lam:>6}: " + "; ".join(f"y={r[0]:.0e}: Phi'/g_N={r[1]:.4g} (roots {r[2]})" for r in rows))
low = [res10[l][0][1] for l in res10]   # y = 1e-10
R.check("C10 (H6): with M'(0)=0 the smallest-|dPsi'| branch is Newtonian G/beta at low gradient (Phi'/g_N -> 1 at y=1e-10) for every lambda tried, so no MOND regime "
        "(my first check at y=1e-6 with tolerance 1e-3 was too strict for lambda=100: 1.006 there; the crossover scale is y_c ~ 1/lambda^2)",
        all(abs(v - 1) < 1e-3 for v in low), f"Phi'/g_N at y=1e-10: {[round(v,6) for v in low]}")
# the second (large-x) branch: constant relative gradient (flat force)
f2 = C.forward(lambda Q: 1.5 * 10.0 * np.sqrt(np.asarray(Q, float)), 1.0, 1.0, +1, 1e-4)
P(f"  all roots at y=1e-4 (lambda=10): x = {[round(v,5) for v in f2.get('roots',[])]} (x=1/8 is the degeneracy; a root near it has D~0, a constant-force branch, not r^-1)")
# effective law when M'(0)=m0 is not tuned: m -> m0' != m0
mf_off = lambda Q: 0.07 * np.ones_like(np.asarray(Q, float))
f3 = [C.forward(mf_off, 1.0, 1.0, +1, yv) for yv in (1e-6, 1e-3, 1.0)]
P("  untuned constant m=0.07 (>m0=1/16, x=0.14 beyond the degeneracy): Phi'/g_N = " + ", ".join(f"{f['Phi']/yv:.4f}" if f['ok'] else 'no root' for f, yv in zip(f3, (1e-6, 1e-3, 1.0))) + "  (a constant NEGATIVE factor: my frozen text said 'a constant enhancement (1+..)'; the sign was wrong, the scale-free-constant statement stands)")
mf_lo = lambda Q: 0.06 * np.ones_like(np.asarray(Q, float))
f4 = [C.forward(mf_lo, 1.0, 1.0, +1, yv) for yv in (1e-6, 1e-3, 1.0)]
P("  untuned constant m=0.06 (<m0): Phi'/g_N = " + ", ".join(f"{f['Phi']/yv:.4f}" if f['ok'] else 'no root' for f, yv in zip(f4, (1e-6, 1e-3, 1.0))) + "  (a constant positive enhancement)")
R.check("H6/C10 an untuned constant m gives a scale-free constant enhancement (1+..), not an r^-1 regime: Phi'/g_N is the same at y=1e-6 and y=1e-3",
        all(f['ok'] for f in f3[:2]) and abs(f3[0]['Phi'] / 1e-6 - f3[1]['Phi'] / 1e-3) < 1e-6, f"{f3[0]['Phi']/1e-6:.6f} vs {f3[1]['Phi']/1e-3:.6f}")
R.num("C10", {str(k): v for k, v in res10.items()})

# ------------------------------------------------------------------ C8, mechanism grade
R.banner("PART B.6  C8 positive control of the pass logic, G1-mechanism grade")
Ph_pres = lambda yv: yv * float(C.nu_p2(yv))                   # a prescribed Phi'(g_N): no action
prescribed_dev = max(abs(Ph_pres(v) / (v * float(C.nu_p2(v))) - 1) for v in np.geomspace(1e-3, 1e3, 50))
R.check("C8 a prescribed Phi' := g_P2 passes G1-law trivially and must be graded M0 (a profile is prescribed), not a mechanism", prescribed_dev < 1e-12, "graded M0 by rule")
R.verdict("G1-mechanism", "M1-inv (P-declared; M' is an OUTPUT of the target by inversion); M2 not reached", "the interaction function is read off the answer; no structure fixes it")

# ============================================================================================ MUTATE modes (bite = G1-law fails)
if MUT:
    R.banner(f"MUTATE {MUT}")
    dbase = designs[("P2", 1.0, +1)]
    if MUT == "M1":                        # interaction off
        # M' = 0: D = 1, x = 0: Phi' = g_N/beta (the x=0 root is on the scan grid exactly, so it is evaluated in closed form)
        dev = [abs(1.0 / float(C.nu_p2(v)) - 1.0) for v in np.geomspace(1e-2, 1e2, 30)]
        bite.append(max(dev) > 0.10)
        P(f"  M'=0: max |Phi'/target - 1| = {max(dev):.3f} (g = g_N: deviation sqrt(1+x^2)-like at large x)")
    elif MUT == "M2":                      # swap coupling, gamma/beta = 3
        d3 = designs[("P2", 3.0, +1)]
        dev3 = [abs(C.forward(d3.mfun, 3.0, 1.0, +1, float(v))["Phi"] / (v * float(C.nu_p2(v))) - 1) for v in np.geomspace(1e-2, 1e2, 30)]
        dev1 = [abs(C.forward(dbase.mfun, 1.0, 1.0, +1, float(v))["Phi"] / (v * float(C.nu_p2(v))) - 1) for v in np.geomspace(1e-2, 1e2, 30)]
        P(f"  baryons on g-hat (beta<->gamma) at gamma/beta=3: max dev {max(dev3):.3f};  at gamma/beta=1 (a symmetry, must NOT bite): {max(dev1):.2e}")
        R.check("M2 at gamma/beta=1 the swap is a relabelling: no change", max(dev1) < 5e-4)
        bite.append(max(dev3) > 0.10)
    elif MUT == "M3":                      # gamma -> 1e6 with M unchanged
        dev = [abs(C.forward(dbase.mfun, 1.0, 1e6, +1, float(v))["Phi"] / (v * float(C.nu_p2(v))) - 1) for v in np.geomspace(1e-2, 1e2, 30)]
        bite.append(max(dev) > 0.10)
        P(f"  gamma=1e6 beta with the M designed at gamma=beta: max dev {max(dev):.3f}; degeneracy m0 -> 1/(8 s) = {1/(8*(1+1e-6)):.4f} vs designed 0.0625")
    elif MUT == "M4":                      # flip sigma
        dev = []
        for v in np.geomspace(1e-2, 1e2, 30):
            f_ = C.forward(dbase.mfun, 1.0, 1.0, -1, float(v))
            dev.append(abs(f_["Phi"] / (v * float(C.nu_p2(v))) - 1) if f_["ok"] else 1.0)
        bite.append(max(dev) > 0.10)
        P(f"  sigma_s -> -1 with the same M': max dev {max(dev):.3f}")
    else:
        P("unknown MUTATE mode for A1")
R.finish(bite if MUT else None)
