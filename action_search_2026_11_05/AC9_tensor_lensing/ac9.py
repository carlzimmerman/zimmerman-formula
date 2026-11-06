#!/usr/bin/env python3
"""AC9: AC2q's tensor principal part / mass and lensing slip, on its own terms.

Criteria: FROZEN_CRITERIA.md (0111fe2269). Method of V3W W4a (tensor) on the AC2q-only stiffness pieces
T_on = -2 gamma X D.P and T_off = +2 gamma X^2, X = s^2/(2 N^2) (unitary gauge, sigma = 0 in statics).
Geometric units G = c = 1, K = 4 pi. s^2 <= 2 rho_DE = 8 a0^2 (framework-native: G rho_DE / c^2 = a0^2/(kappa^2 c^4)).
Run from the repo root:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 action_search_2026_11_05/AC9_tensor_lensing/ac9.py
AC9_MUTATE=1 plants c P^2 (d_z h_+)^2 (T1a must then fail). kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

MUT = os.environ.get("AC9_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT, CHK = [], {}
RES = {"lane": "AC9_tensor_lensing", "criteria": "0111fe2269", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


P("AC9  AC2q tensor speed and lensing slip" + ("  [MUTATE: planted c P^2 (d_z h_+)^2]" if MUT else ""))
cl = 2.99792458e8; PC = 3.0857e16; KPC = 1e3 * PC; GMs = 1.32712440018e20; RSUN = 6.957e8
FOOT = {"canonical": (9.3603e-11, (21.7, 24.0, 90.0)), "alt": (1.1312e-10, (22.9, 24.0, 90.0))}
kGW = 2 * math.pi * 100.0 / cl
GW_BAND = (-3e-15, 7e-16)

# ============================================================ T1: tensor modes
t, x, y, z, eps = sp.symbols("t x y z epsilon", real=True)
K, gLs, s2, cpl = sp.symbols("K gamma_L s2 c_plant", positive=True)
Ax, Az = sp.symbols("A_x A_z", real=True)
P0x, P0z = sp.symbols("P0x P0z", real=True)
Gxx, Gxz, Gzx, Gzz, Gyy = sp.symbols("G_xx G_xz G_zx G_zz G_yy", real=True)
hp = sp.Function("hp")(t, z); hx = sp.Function("hx")(t, z)
Xc = (x, y, z)
lnN = Ax * x + Az * z
Pj = [P0x + Gxx * x + Gxz * z, Gyy * y, P0z + Gzx * x + Gzz * z]
H = sp.Matrix([[hp, hx, 0], [hx, -hp, 0], [0, 0, 0]])
hmat = sp.eye(3) + eps * H
hinv = sp.Matrix(3, 3, lambda i, j: sp.series(hmat.inv()[i, j], eps, 0, 3).removeO())
sqh = 1 - eps ** 2 * (hp ** 2 + hx ** 2) / 2                   # sqrt(det h) to O(eps^2), TT
N = 1 + lnN
Xcl = s2 / (2 * N ** 2)                                        # unitary-gauge clock kinetic term
Pup = [sum(hinv[i, j] * Pj[j] for j in range(3)) for i in range(3)]
DP = sum(sp.diff(sqh * Pup[i], Xc[i]) for i in range(3)) / sqh
dsyms = [sp.Symbol(f"d{i}") for i in range(4)]
dterms = [sp.diff(hp, t), sp.diff(hp, z), sp.diff(hx, t), sp.diff(hx, z)]


def tensor_part(Lterm, label):
    L2 = sp.expand(sp.series(sp.expand(Lterm), eps, 0, 3).removeO().coeff(eps, 2))
    L2s = L2
    for i, dt_ in enumerate(dterms):
        L2s = L2s.subs(dt_, dsyms[i])
    quad = [sp.simplify(sp.diff(L2s, a_, b_)) for a_ in dsyms for b_ in dsyms]
    lin = [sp.simplify(sp.diff(L2s, a_).subs({d_: 0 for d_ in dsyms})) for a_ in dsyms]
    no_quad = all(q == 0 for q in quad)
    cp = sp.simplify(lin[1] / hp); cx = sp.simplify(lin[3] / hx)
    lin_total = (lin[0] == 0 and lin[2] == 0 and not cp.has(hp) and not cp.has(hx) and not cx.has(hp)
                 and not cx.has(hx) and not cp.has(t) and not cx.has(t))
    at0 = {x: 0, y: 0, z: 0}
    L0 = L2s.subs({d_: 0 for d_ in dsyms})
    m_pp = sp.simplify(sp.diff(L0, hp, 2).subs(at0) / 2 - sp.diff(cp, z).subs(at0) / 2)
    m_xx = sp.simplify(sp.diff(L0, hx, 2).subs(at0) / 2 - sp.diff(cx, z).subs(at0) / 2)
    m2p = sp.simplify(-32 * sp.pi * m_pp); m2x = sp.simplify(-32 * sp.pi * m_xx)
    P(f"  [{label}] (dh)(dh) coefficients all zero = {no_quad}; h*dh coefficients {[str(c) for c in lin]}")
    P(f"  [{label}] m_+^2 = {m2p};  m_x^2 = {m2x}")
    return no_quad, lin_total, m2p, m2x


Ton = N * sqh * (-2 * gLs * Xcl * DP)
Toff = N * sqh * (2 * gLs * Xcl ** 2)
if MUT:
    Ton = Ton + eps ** 2 * cpl * (P0x ** 2 + P0z ** 2) * sp.diff(hp, z) ** 2
nq_on, lt_on, m2p_on, m2x_on = tensor_part(Ton, "T_on")
nq_off, lt_off, m2p_off, m2x_off = tensor_part(Toff, "T_off")
check("T1a", nq_on and lt_on and nq_off and lt_off,
      "AC2q pieces add no (dh)^2 term and only total-derivative h*dh terms at O(h^2): principal part is GR's, c_T = c exactly")
RES["T1_symbolic"] = dict(m2p_on=str(m2p_on), m2x_on=str(m2x_on), m2p_off=str(m2p_off), m2x_off=str(m2x_off))
k1 = [sp.simplify(e.subs(s2, 0)) for e in (m2p_on, m2x_on, m2p_off, m2x_off)]
check("K1_tensor", all(v == 0 for v in k1), f"known answer: s = 0 gives new masses {k1} (all 0: AC2q = v3s)")

args = (K, gLs, s2, Ax, Az, P0x, P0z, Gxx, Gxz, Gzx, Gzz, Gyy)
fns = [sp.lambdify(args, e, "math") for e in (m2p_on, m2x_on, m2p_off, m2x_off)]
T1b = {}
for f, (A0, Ls) in FOOT.items():
    ag = A0 / cl ** 2; Kn = 4 * math.pi; s2v = 8 * ag ** 2      # s^2 = 2 rho_DE (bound), geometric units
    worst = 0.0; npts = 0
    for gb in (A0, 9.81):
        Ab = gb / cl ** 2
        for Lpc in Ls:
            L = Lpc * PC; gl = Kn * L ** 2 / 2
            Gh = GMs / cl ** 2 / L ** 2 / RSUN
            for uf in np.linspace(0.03, 0.99, 33):
                for th in np.linspace(0.0, math.pi, 13):
                    p0 = uf * ag
                    Pv0 = (p0 * math.sin(th) / Kn, p0 * math.cos(th) / Kn)
                    for (gx, gz) in ((Ab, 0.0), (0.0, Ab), (Ab / math.sqrt(2), Ab / math.sqrt(2))):
                        G0 = (Gh / Kn,) * 5
                        for fn in fns:
                            worst = max(worst, abs(fn(Kn, gl, s2v, gx, gz, *Pv0, *G0)))
                        npts += 1
    dv = worst / (2 * kGW ** 2)
    T1b[f] = dict(max_abs_m2_new=worst, dv_over_c_100Hz=dv, points=npts, s2_geo=s2v,
                  gamma_s2_Lstar_min=Kn * (Ls[0] * PC) ** 2 / 2 * s2v)
    P(f"  T1b [{f}]: max |m^2| (AC2q pieces) = {worst:.3e} m^-2 over {npts} points; dv/c at 100 Hz = {dv:.3e}; "
      f"gamma s^2 at Lstar {Ls[0]} pc = {T1b[f]['gamma_s2_Lstar_min']:.2e}")
RES["T1b"] = T1b
check("T1b", all(GW_BAND[0] <= -r["dv_over_c_100Hz"] and r["dv_over_c_100Hz"] <= GW_BAND[1] for r in T1b.values()),
      f"dv/c within GW170817 band {GW_BAND} on both footings")

# ============================================================ T2: lensing slip (static)
Phi = sp.Function("Phi")(x, y, z); Psi = sp.Function("Psi")(x, y, z)
Pf = [sp.Function(f"P{i}")(x, y, z) for i in range(3)]
c11, c22, c12, c13, c23 = [sp.Function(n)(x, y, z) for n in ("chi11", "chi22", "chi12", "chi13", "chi23")]
chi = sp.Matrix([[c11, c12, c13], [c12, c22, c23], [c13, c23, -c11 - c22]])
hS = (1 - 2 * Psi) * sp.eye(3) + eps * chi
NS = 1 + Phi
# first order in eps: h^{-1} = (1-2Psi)^{-1}(I - eps chi/(1-2Psi)), sqrt(det h) = (1-2Psi)^{3/2} (chi traceless)
hinvS = (sp.eye(3) - eps * chi / (1 - 2 * Psi)) / (1 - 2 * Psi)
sqhS = (1 - 2 * Psi) ** sp.Rational(3, 2)
XS = s2 / (2 * NS ** 2)
PupS = [sum(hinvS[i, j] * Pf[j] for j in range(3)) for i in range(3)]
DPS = sum(sp.diff(sqhS * PupS[i], Xc[i]) for i in range(3)) / sqhS


def static_sources(Lterm, label):
    fields = [Psi, c11, c22, c12, c13, c23]
    out = {}
    zero = {c11: 0, c22: 0, c12: 0, c13: 0, c23: 0}
    for f_ in fields:
        if not Lterm.has(f_):
            out[str(f_.func)] = sp.Integer(0)              # field absent: its Euler-Lagrange expression is 0
            continue
        (e,) = euler_equations(Lterm, [f_], Xc)             # one field at a time (no zip misalignment)
        ex = e.lhs.doit()
        ex = ex.subs(eps, 1)
        ex = sp.simplify(ex.subs(zero).doit())
        out[str(f_.func)] = ex
    P(f"  [{label}] S_Psi = {out['Psi']}")
    for k_ in ("chi11", "chi12"):
        P(f"  [{label}] dL/d{k_} = {out[k_]}")
    return out


Ton_S = sp.expand(NS * sqhS * (-2 * gLs * XS * DPS))
Ton_S = sp.series(Ton_S, eps, 0, 2).removeO()
src_on = static_sources(Ton_S, "T_on")
Toff_S = NS * sqhS * (2 * gLs * XS ** 2)
src_off = static_sources(sp.series(Toff_S, eps, 0, 2).removeO(), "T_off")

flat = {Phi: 0}
vals_s0 = [sp.simplify(v.subs(s2, 0)) for v in src_on.values()]
vals_flat = [sp.simplify(v.subs(Phi, sp.Integer(0)).doit()) for v in src_on.values()]
check("T2a", all(v == 0 for v in vals_s0) and all(v == 0 for v in vals_flat),
      f"T_on Psi source and anisotropic stress vanish at s = 0 {vals_s0} and at grad Phi = 0 {vals_flat}: "
      "O(s^2 grad Phi P), beyond O(GM)")
off_aniso = [sp.simplify(src_off[k_]) for k_ in ("chi11", "chi22", "chi12", "chi13", "chi23")]
check("T2_off_aniso", all(v == 0 for v in off_aniso), f"T_off anisotropic stress {off_aniso} (0: isotropic pressure only)")
P(f"  T_off Psi source: {sp.simplify(src_off['Psi'])}")

# coefficient: S_Psi at Psi = 0 against s^2 gamma (grad Phi . P)
Psi0 = {Psi: 0}
SPsi0 = sp.simplify(src_on["Psi"].subs(Psi0).doit())
dotg = sum(sp.diff(Phi, Xc[i]) * Pf[i] for i in range(3))
coef = sp.simplify(SPsi0 / (gLs * s2 * dotg))
P(f"  S_Psi(Psi=0) / (gamma s^2 gradPhi.P) = {coef}")
aniso11 = sp.simplify(src_on["chi11"].subs(Psi0).doit())
P(f"  Pi from chi11 at Psi = 0: {aniso11}")
coef_ok = not coef.has(x) or sp.simplify(coef.subs(Phi, 0)) != sp.nan
c_at0 = sp.simplify(coef.subs(Phi, 0).doit()) if coef.has(Phi) else coef
RES["T2_symbolic"] = dict(S_Psi_on=str(src_on["Psi"]), coef=str(coef), aniso11=str(aniso11), S_Psi_off=str(src_off["Psi"]))

# K2: planted vector-kinetic term c P_i P_j h^{ij} N sqrt(h) -> Pi_ij = -c (P_i P_j)^TF
LK2 = NS * sqhS * cpl * sum(PupS[i] * Pf[i] for i in range(3))
srcK2 = static_sources(sp.series(sp.expand(LK2), eps, 0, 2).removeO(), "K2 plant")
k2_11 = sp.simplify((srcK2["chi11"].subs({Psi: 0, Phi: 0}).doit()) - (-cpl * (Pf[0] ** 2 - Pf[2] ** 2)))
k2_12 = sp.simplify((srcK2["chi12"].subs({Psi: 0, Phi: 0}).doit()) - (-2 * cpl * Pf[0] * Pf[1]))
check("K2", k2_11 == 0 and k2_12 == 0, f"planted term returns Pi_11-Pi_33 = -c(P1^2-P3^2), 2 Pi_12 = -2c P1 P2: residuals {k2_11}, {k2_12}")

# T2b numbers: |S_Psi| / rho_tot <= |coef| gamma s^2 |gradPhi| |P| / (g/(4 pi r)), |P| <= a0/K, gradPhi = g
cnum = float(sp.Abs(c_at0)) if not c_at0.free_symbols else None
P(f"  |coef| at Phi -> 0: {c_at0}")
T2b = {}
for f, (A0, Ls) in FOOT.items():
    ag = A0 / cl ** 2; Kn = 4 * math.pi; s2v = 8 * ag ** 2
    rows = []
    for Lpc in (Ls[0], 90.0):
        gl = Kn * (Lpc * PC) ** 2 / 2
        for rk in (30.0, 100.0, 310.0):
            r = rk * KPC
            ratio = (cnum if cnum is not None else 1.0) * gl * s2v * (ag / Kn) / (1.0 / (4 * math.pi * r))
            # T_off isotropic: |S_Psi_off| ~ 6 gamma X^2 N -> (3/2) gamma s^4; rho_tot for a 1e11 Msun deep-MOND profile
            gN = 6.674e-11 * 1e11 * 1.989e30 / r ** 2; g = math.sqrt(gN * A0) / cl ** 2
            rho_geo = g / (4 * math.pi * r)
            off = 1.5 * gl * s2v ** 2 / rho_geo
            rows.append(dict(Lstar_pc=Lpc, r_kpc=rk, slip_bound_on=ratio, slip_off_1e11Msun=off))
            P(f"  T2b [{f}] Lstar {Lpc:5.1f} pc r {rk:5.0f} kpc: |S_Psi|/rho_tot <= {ratio:.2e} (T_on); T_off {off:.2e}")
    T2b[f] = rows
RES["T2b"] = T2b
check("T2b", cnum is not None and all(r["slip_bound_on"] < 1e-6 and r["slip_off_1e11Msun"] < 1e-6 for v in T2b.values() for r in v),
      "slip bound < 1e-6 on both footings (W3 v3s bound 6.5e-5; KiDS amplitude error ~0.2)")

# X > 0 structural statement (not graded): X = s^2[(1+sigma_t)^2/(1+Phi)^2 - |grad sigma|^2]/2 > 0 iff |grad sigma| < (1+sigma_t)/(1+Phi)
RES["X_positive_note"] = "statics sigma = 0 (AC8): X = s^2/(2N^2) > 0 exactly; moving/nonlinear X > 0 needs |grad sigma| below the local light cone, open"

tensor_lab = "PASS" if (CHK["T1a"] and CHK["T1b"] and CHK["K1_tensor"]) else "FAIL" if not CHK["T1a"] else "UNDECIDED"
lens_lab = "PASS" if (CHK["T2a"] and CHK["T2b"] and CHK["K2"] and CHK["T2_off_aniso"]) else "FAIL"
RES["labels"] = dict(tensor=tensor_lab, lensing=lens_lab)
P(f"LABELS: tensor {tensor_lab}; lensing {lens_lab}" + ("  (MUTATE: T1a must FAIL)" if MUT else ""))
with open(os.path.join(HERE, f"ac9{TAG}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
with open(os.path.join(HERE, f"ac9{TAG}.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
