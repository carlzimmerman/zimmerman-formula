#!/usr/bin/env python3
"""QX19: one-action scorecard. AC2q + AC21 iter_6 Pi^6 blend (b = X); v3s + blend (b = rho_DE) as column 2.

Criteria: FROZEN_CRITERIA.md (d65980ffcd). Method for C1/C2 = AC9's (ac9.py, 0111fe2269), with the stiffness written as a
GENERIC function F of the charge Sigma (AC2q: D.P + 2X; v3s: D.P). Geometric units G = c = 1, K = 4 pi.
Run from the repo root:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 closure_2026_11_06/QX19_one_action_scorecard/qx19.py
QX19_MUTATE=1 : MUTATE-1 plants c P^2 (d_z h_+)^2 (C1a must fail); MUTATE-2 swaps the blend's near-zero power to m = 4
(C6 must fail). Outputs qx19[_MUTATE].{json,out}. kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

MUT = os.environ.get("QX19_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
OUT, CHK = [], {}
RES = {"lane": "QX19_one_action_scorecard", "criteria": "d65980ffcd", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


P("QX19  one-action scorecard: AC2q + Pi^6 blend (b = X); v3s + blend (b = rho_DE)" + ("  [MUTATE]" if MUT else ""))
cl = 2.99792458e8; PC = 3.0857e16; KPC = 1e3 * PC; GMs = 1.32712440018e20; RSUN = 6.957e8
FOOT = {"canonical": (9.3603e-11, (21.7, 24.0, 90.0)), "alt": (1.1312e-10, (22.9, 24.0, 90.0))}
kGW = 2 * math.pi * 100.0 / cl
GW_BAND = (-3e-15, 7e-16)

# ============================================================ the blend f(q) from AC21 iter_6 (exact rationals)
q = sp.Symbol("q", nonnegative=True)
import glob
form = json.load(open(glob.glob(os.path.join(REPO, "action_search_2026_11_05/AC21_smooth_3d/iter_6*/form.json"))[0]))
pieces = [(sp.Rational(a), sp.Rational(b), sp.sympify(e, locals={"q": q})) for a, b, e in form["pieces"]]
if MUT:   # MUTATE-2: near-zero power m = 4 (f'' ~ q^2 on [0,1/2]); same layer otherwise (C6 must FAIL)
    a0_, b0_, e0_ = pieces[0]
    pieces[0] = (a0_, b0_, sp.Rational(form["A"]) * q ** 2 / 4)
fpp_pieces = pieces + [(sp.Integer(1), sp.oo, sp.Integer(1))]
# integrate exactly: f'(0) = f(0) = 0
fp_pieces, f_pieces = [], []
c1 = sp.Integer(0); c0 = sp.Integer(0)
for a, b, e in fpp_pieces:
    F1 = sp.integrate(e, (q, a, q)) + c1
    F0 = sp.integrate(F1, (q, a, q)) + c0
    fp_pieces.append((a, b, sp.expand(F1))); f_pieces.append((a, b, sp.expand(F0)))
    if b != sp.oo:
        c1 = F1.subs(q, b); c0 = F0.subs(q, b)


def piece_val(pcs, qq):
    for a, b, e in pcs:
        if qq <= float(b) if b != sp.oo else True:
            if qq >= float(a):
                return float(e.subs(q, qq)) if isinstance(e, sp.Basic) else float(e)
    return float(pcs[-1][2].subs(q, qq))


lam = {name: [(float(a), float(b) if b != sp.oo else math.inf, sp.lambdify(q, e, "math")) for a, b, e in pcs]
       for name, pcs in (("f", f_pieces), ("fp", fp_pieces), ("fpp", fpp_pieces))}


def ev(name, qq):
    for a, b, fn in lam[name]:
        if a <= qq <= b:
            return fn(qq)
    return lam[name][-1][2](qq)


qg = np.linspace(0.0, 2.0, 20001)
fv = np.array([ev("f", v) for v in qg]); fpv = np.array([ev("fp", v) for v in qg]); fppv = np.array([ev("fpp", v) for v in qg])
lay = qg <= 1.0
Delta0 = float(np.max(np.abs(fv[lay] - qg[lay] ** 2 / 2))); Delta1 = float(np.max(np.abs(fpv[lay] - qg[lay])))
fpp_max = float(np.max(fppv)); fpp_min = float(np.min(fppv))
P(f"blend: Delta0 = max|f - q^2/2| = {Delta0:.4f}; Delta1 = max|f' - q| = {Delta1:.4f}; f'' in [{fpp_min:.4g}, {fpp_max:.4g}] on [0,2]")
RES["blend"] = dict(Delta0=Delta0, Delta1=Delta1, fpp_max=fpp_max, fpp_min=fpp_min)

# ============================================================ C4 / C7: FRW exactness (sympy)
f_last = f_pieces[-1][2]; fp1 = fp_pieces[-2][2].subs(q, 1); f1 = f_pieces[-2][2].subs(q, 1)
Sg, bb = sp.symbols("Sigma b", positive=True)
F_hi = sp.simplify(bb ** 2 * f_last.subs(q, Sg / bb))
c4 = (sp.simplify(f_last - q ** 2 / 2) == 0, sp.simplify(F_hi - Sg ** 2 / 2) == 0, sp.diff(F_hi, bb) == 0, fp1 == 1, f1 == sp.Rational(1, 2))
P(f"C4: f = q^2/2 on q >= 1: {c4[0]}; F = b^2 f(Sigma/b) = Sigma^2/2 there: {c4[1]}; dF/db = 0: {c4[2]}; "
  f"moments f'(1) = {fp1}, f(1) = {f1}")
P("C4: FRW has P = 0 so Sigma = 2X, q = Sigma/X = 2 (> 1); perturbations with |dSigma| < X and any dX keep q > 1 "
  "(|dq| <= |dSigma|/X + 2|dX|/X < 1 + small for linear modes)")
check("C4", all(c4), "FRW point q = 2 lies where F = gamma Sigma^2/2 exactly and independent of b: AC2q's FRW quadratic action unchanged (AC7 Q1 72/72 carries)")
check("C7", CHK["C4"], "linear FRW operator unchanged, so AC23 PASS (HARMLESS, scoped, eps_phi <= 0.5) carries")

# ============================================================ C5 / C6 / C9: shape facts
f_low = sp.simplify(f_pieces[0][2]); m_pow = sp.degree(sp.Poly(f_low, q)) if f_low.is_polynomial(q) else None
pure = f_low.is_polynomial(q) and len(sp.Poly(f_low, q).terms()) == 1
P(f"C6: f on [0, 1/2] = {f_low}  (pure power: {pure}, m = {m_pow})")
check("C5", float(f_pieces[0][2].subs(q, 0)) == 0 and float(fp_pieces[0][2].subs(q, 0)) == 0 and fpp_min >= 0,
      f"f(0) = f'(0) = 0 exactly and f'' >= 0 (min {fpp_min:.3g}) on 20001 points: convex, so AC21 T7 gives B >= s (PN sign carries AC17)")
check("C6", bool(pure) and m_pow is not None and m_pow > 5,
      f"pure power q^{m_pow} near 0, m > d + 2 = 5 required (AC21 theorem); AC22 curved-2D C1/C2 PASS carries" +
      ("  [MUTATE-2: m = 4 must FAIL]" if MUT else ""))
check("C9", fpp_min >= 0 and math.isfinite(fpp_max),
      f"layer stiffness F'' = gamma f'' in [0, {fpp_max:.3g} gamma]: positive and bounded, so no Gamma ~ k branch (AC7 Q2 carries)")

# ============================================================ C1: tensor modes with generic F
t, x, y, z, eps = sp.symbols("t x y z epsilon", real=True)
K, gLs, s2, cpl = sp.symbols("K gamma_L s2 c_plant", positive=True)
Ax, Az = sp.symbols("A_x A_z", real=True)
P0x, P0z = sp.symbols("P0x P0z", real=True)
Gxx, Gxz, Gzx, Gzz, Gyy = sp.symbols("G_xx G_xz G_zx G_zz G_yy", real=True)
Fv0, Fp0, F2c = sp.symbols("Fv0 Fp0 F2c", real=True)
hp = sp.Function("hp")(t, z); hx = sp.Function("hx")(t, z)
Xc = (x, y, z)
N = 1 + Ax * x + Az * z
Pj = [P0x + Gxx * x + Gxz * z, Gyy * y, P0z + Gzx * x + Gzz * z]
H = sp.Matrix([[hp, hx, 0], [hx, -hp, 0], [0, 0, 0]])
hmat = sp.eye(3) + eps * H
hinv = sp.Matrix(3, 3, lambda i, j: sp.series(hmat.inv()[i, j], eps, 0, 3).removeO())
sqh = 1 - eps ** 2 * (hp ** 2 + hx ** 2) / 2
Xcl = s2 / (2 * N ** 2)
Pup = [sum(hinv[i, j] * Pj[j] for j in range(3)) for i in range(3)]
DP = sp.expand(sum(sp.diff(sqh * Pup[i], Xc[i]) for i in range(3)) / sqh)
DP = sp.series(DP, eps, 0, 3).removeO()
dsyms = [sp.Symbol(f"d{i}") for i in range(4)]
dterms = [sp.diff(hp, t), sp.diff(hp, z), sp.diff(hx, t), sp.diff(hx, z)]
F0f, F1f, F2f = [sp.Function(n)(x, y, z) for n in ("F0", "F1", "F2")]


def tensor_part(Lterm, label):
    L2 = sp.expand(sp.series(sp.expand(Lterm), eps, 0, 3).removeO().coeff(eps, 2))
    L2s = L2
    for i, dt_ in enumerate(dterms):
        L2s = L2s.subs(dt_, dsyms[i])
    quad = [sp.simplify(sp.diff(L2s, a_, b_)) for a_ in dsyms for b_ in dsyms]
    lin = [sp.simplify(sp.diff(L2s, a_).subs({d_: 0 for d_ in dsyms})) for a_ in dsyms]
    no_quad = all(qq == 0 for qq in quad)
    cp = sp.simplify(lin[1] / hp); cx = sp.simplify(lin[3] / hx)
    lin_total = (lin[0] == 0 and lin[2] == 0 and not cp.has(hp) and not cp.has(hx) and not cx.has(hp)
                 and not cx.has(hx) and not cp.has(t) and not cx.has(t))
    at0 = {x: 0, y: 0, z: 0}
    L0 = L2s.subs({d_: 0 for d_ in dsyms})
    m_pp = sp.simplify(sp.diff(L0, hp, 2).subs(at0) / 2 - sp.diff(cp, z).subs(at0) / 2)
    m_xx = sp.simplify(sp.diff(L0, hx, 2).subs(at0) / 2 - sp.diff(cx, z).subs(at0) / 2)
    m2p = sp.simplify(-32 * sp.pi * m_pp); m2x = sp.simplify(-32 * sp.pi * m_xx)
    P(f"  [{label}] (dh)(dh) coefficients all zero = {no_quad}; h*dh total-derivative form = {lin_total}")
    return no_quad, lin_total, m2p, m2x


C1 = {}
for model, Xterm in (("AC2q", Xcl), ("v3s", sp.Integer(0))):
    Sig = sp.expand(DP + 2 * Xterm)
    S0 = Sig.subs(eps, 0); dS = sp.expand(Sig - S0)
    # generic F: C1a must hold for ANY F (F0, F1, F2 arbitrary functions of position)
    Fgen = F0f + F1f * dS + F2f * dS ** 2 / 2
    Lgen = -gLs * N * sqh * (Fgen - (2 * Xterm) ** 2 / 2)
    if MUT:
        Lgen = Lgen + eps ** 2 * cpl * (P0x ** 2 + P0z ** 2) * sp.diff(hp, z) ** 2
    nq, lt, _, _ = tensor_part(Lgen, f"{model} generic F")
    # local quadratic model at the origin (exact for the mass at x = 0: only F1, F2, dF1 = F2 dS0 enter)
    Sc = S0.subs({x: 0, y: 0, z: 0})
    Floc = Fv0 + Fp0 * (Sig - Sc) + F2c * (Sig - Sc) ** 2 / 2
    Lloc = -gLs * N * sqh * (Floc - (2 * Xterm) ** 2 / 2)
    _, _, m2p, m2x = tensor_part(Lloc, f"{model} local F")
    C1[model] = dict(no_quad=nq, lin_total=lt, m2p=m2p, m2x=m2x)
check("C1a", all(v["no_quad"] and v["lin_total"] for v in C1.values()),
      "generic F(Sigma): no (dh)^2 term, only total-derivative h dh terms, both models: c_T = c" + ("  [MUTATE-1: must FAIL]" if MUT else ""))

args = (K, gLs, s2, Ax, Az, P0x, P0z, Gxx, Gxz, Gzx, Gzz, Gyy, Fv0, Fp0, F2c)
qs = np.linspace(0.0, 1.0, 41)
T1b = {}
for model in ("AC2q", "v3s"):
    fns = [sp.lambdify(args, C1[model][k_], "math") for k_ in ("m2p", "m2x")]
    for f, (A0, Ls) in FOOT.items():
        ag = A0 / cl ** 2; Kn = 4 * math.pi; s2v = 8 * ag ** 2; bv = s2v / 2      # b = X (AC2q) = rho_DE-scale (v3s)
        worst = 0.0; npts = 0
        for gb in (A0, 9.81):
            Ab = gb / cl ** 2
            for Lpc in Ls:
                L = Lpc * PC; gl = Kn * L ** 2 / 2
                Gh = GMs / cl ** 2 / L ** 2 / RSUN
                for uf in np.linspace(0.03, 0.99, 17):
                    for th in np.linspace(0.0, math.pi, 7):
                        p0 = uf * ag
                        Pv0 = (p0 * math.sin(th) / Kn, p0 * math.cos(th) / Kn)
                        for (gx, gz) in ((Ab, 0.0), (0.0, Ab), (Ab / math.sqrt(2), Ab / math.sqrt(2))):
                            G0 = (Gh / Kn,) * 5
                            for qq in qs:
                                Fl = (bv ** 2 * ev("f", qq), bv * ev("fp", qq), ev("fpp", qq))
                                for fn in fns:
                                    worst = max(worst, abs(fn(Kn, gl, s2v, gx, gz, *Pv0, *G0, *Fl)))
                            npts += 1
        dv = worst / (2 * kGW ** 2)
        T1b[f"{model}/{f}"] = dict(max_abs_m2=worst, dv_over_c_100Hz=dv, points=npts)
        P(f"  C1b [{model}/{f}]: max |m^2| over the layer = {worst:.3e} m^-2 ({npts} points x {len(qs)} q); dv/c at 100 Hz = {dv:.3e}")
RES["C1b"] = T1b
check("C1b", all(GW_BAND[0] <= -r["dv_over_c_100Hz"] and r["dv_over_c_100Hz"] <= GW_BAND[1] for r in T1b.values()),
      f"blend-layer tensor mass: dv/c inside GW170817 band {GW_BAND}, both models and footings")

# ============================================================ C2: lensing slip, generic F (structure + bound)
Phi = sp.Function("Phi")(x, y, z); Psi = sp.Function("Psi")(x, y, z)
Pf = [sp.Function(f"P{i}")(x, y, z) for i in range(3)]
NS = 1 + Phi
hinvS = sp.eye(3) / (1 - 2 * Psi)
sqhS = (1 - 2 * Psi) ** sp.Rational(3, 2)
XS = s2 / (2 * NS ** 2)
PupS = [hinvS[i, i] * Pf[i] for i in range(3)]
DPS = sum(sp.diff(sqhS * PupS[i], Xc[i]) for i in range(3)) / sqhS
SigS = DPS + 2 * XS
u = sp.Symbol("u")
Fg = sp.Function("F")
Lst = -gLs * NS * sqhS * Fg(SigS)
dpsi = [sp.Derivative(Psi, v) for v in Xc]
Ci = [sp.simplify(sp.diff(Lst, d_)) for d_ in dpsi]                      # dL/d(d_i Psi)
Fp_of = sp.Subs(sp.Derivative(Fg(u), u), u, SigS).doit()
ratio = [sp.simplify(c_ / Fp_of) if c_ != 0 else sp.Integer(0) for c_ in Ci]
structure_ok = all(not r_.has(Fg) for r_ in ratio)
Cpsi0 = [sp.simplify(r_.subs({Psi: 0, Phi: 0}).doit()) for r_ in ratio]
P(f"C2 structure: dL/d(d_i Psi) = F'(Sigma) * C_i with C_i free of F: {structure_ok}; C_i at Psi = Phi = 0: {Cpsi0}")
# non-divergence part: F and F' terms; |dSigma/dPsi| at Psi = 0 for the bound
dSig_dPsi = sp.simplify(sp.diff(SigS.subs({d_: sp.Symbol(f"dd{i}") for i, d_ in enumerate(dpsi)}), Psi).subs({Psi: 0}))
P(f"C2: dSigma/dPsi|_(Psi=0, explicit) = {dSig_dPsi}")
C2rows = {}
for model in ("AC2q", "v3s"):
    for f, (A0, Ls) in FOOT.items():
        ag = A0 / cl ** 2; Kn = 4 * math.pi; s2v = 8 * ag ** 2; bv = s2v / 2
        rows = []
        for Lpc in (Ls[0], 90.0):
            gl = Kn * (Lpc * PC) ** 2 / 2
            for rk in (30.0, 100.0, 310.0):
                r = rk * KPC
                gN = 6.674e-11 * 1e11 * 1.989e30 / r ** 2; g = math.sqrt(gN * A0) / cl ** 2
                rho = g / (4 * math.pi * r); Pm = ag / Kn
                # non-divergence part: |dF| d(N sqrt h)/dPsi (= 3) + |dF'| |dSigma/dPsi| (<= 3|D.P| + 6 X + |P| g:
                # in the layer |D.P| <= 2b, X <= b) ; dF <= Delta0 b^2, dF' <= Delta1 b
                nondiv = gl * (3 * Delta0 * bv ** 2 + Delta1 * bv * (3 * 2 * bv + 6 * bv + Pm * g)) / rho
                # divergence part: |grad(Phi - Psi)| <= 4 pi |C| |dF'|, |C| <= 2 |P| (C_i = -2 P_i at Psi = Phi = 0)
                div = 4 * math.pi * gl * 2 * Pm * Delta1 * bv / g
                rows.append(dict(Lstar_pc=Lpc, r_kpc=rk, nondiv_rel=nondiv, div_deflection_rel=div))
        C2rows[f"{model}/{f}"] = rows
        worst = max(max(r_["nondiv_rel"], r_["div_deflection_rel"]) for r_ in rows)
        P(f"  C2 [{model}/{f}]: worst blend slip (non-div / rho_tot, divergence deflection / g) = {worst:.2e}")
RES["C2"] = C2rows
check("C2", structure_ok and all(max(r_["nondiv_rel"], r_["div_deflection_rel"]) < 1e-6 for v in C2rows.values() for r_ in v),
      "blend changes S_Psi by an F/F' part and a total divergence F'(Sigma) C_i; both < 1e-6 relative on AC9 T2b profiles")

# ============================================================ C3, C8: bounds from the record
cass_rel = 2.0e-5; cass_margin = 4.8e7
check("C3", cass_margin * (1 - cass_rel) > 1,
      f"Cassini: AC21 statics change <= {cass_rel} (b = rho_DE; AC2q b = X <= rho_DE) on C6P margin {cass_margin:.1e}: "
      f"margin stays {cass_margin * (1 - cass_rel):.4e} > 1; PPN gamma = beta = 1 at O(GM) carries (stiffness beyond O(GM), V3W W1)")
st_bound = 5e-5 * max(1.0, fpp_max); dex = math.log10(1 + st_bound)
check("C8", dex < 1e-3,
      f"galaxy phantom change <= QX2 stiffness bound 5e-5 x max(1, max f'' = {fpp_max:.3g}) = {st_bound:.2e} -> {dex:.2e} dex < 1e-3: "
      "QX8 exact-field SPARC PASS (0.0560 / 0.0558) carries")

# ============================================================ labels
lab = {k_: ("CARRY" if v else "FAIL") for k_, v in CHK.items()}
RES["labels"] = lab
P("LABELS: " + ", ".join(f"{k_} {v}" for k_, v in lab.items()) + ("  (MUTATE: C1a and C6 must FAIL)" if MUT else ""))
with open(os.path.join(HERE, f"qx19{TAG}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
with open(os.path.join(HERE, f"qx19{TAG}.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
