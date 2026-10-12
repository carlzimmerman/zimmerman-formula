#!/usr/bin/env python3
"""CFG660 (FROZEN_CRITERIA.md): the law as the hydrostatic equilibrium of cold energy's own stress (spherical, round rule).

Isotropic medium (I): Pi = P(g) I, dP/dg = (g/4piG)(1/s - 1).
Anisotropic, field-aligned medium (A): Pi = P_perp I + (P_par - P_perp) g^g^, dP_par/dg = (g/4piG)(1/F' - 1),
  P_perp - P_par = g (g - F^-1(g))/4piG.   F = law g = nu(g_N/a0) g_N (nu_mono), s = dln F/dln g_N, F' = s g/g_N.
Checks S1-S5 (sympy + tables), N1 (Hernquist toy), D1 (raw SPARC via the record's CFG4 harness, Upsilon = 0.61).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not "theory closed".
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg660.py       (CFG660_MUTATE=1 -> _MUTATE outputs, exit 1 iff the teeth bite)
"""
import os, sys, io, json, math, contextlib, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
    import CFG7_common as C7
MUT = os.environ.get("CFG660_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
FOOTS = ("canonical", "alt")
OUT, RES = [], {"lane": "CFG660", "criteria": "7eff02fa3", "mutate": MUT}
T0 = time.time()


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


NU = {"nu_mono": lambda y: np.asarray(C4.nu_mono(np.asarray(y, float)), float),
      "exp": lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(np.asarray(y, float), 1e-300))))}


# ================================================================================================ S1-S3 sympy
P("CFG660: the law as the equilibrium of cold energy's own stress" + (" [MUTATE]" if MUT else ""))
r, Gs = sp.symbols("r G", positive=True)
gN = sp.Function("g_N")(r)
Ff = sp.Function("F")
g = Ff(gN)
Fp = sp.diff(Ff(sp.Symbol("x")), sp.Symbol("x")).subs(sp.Symbol("x"), gN)           # F'(g_N)
rho_b = sp.diff(r ** 2 * gN, r) / (4 * sp.pi * Gs * r ** 2)
rho_c = sp.diff(r ** 2 * g, r) / (4 * sp.pi * Gs * r ** 2) - rho_b
dPpar_dg = (g / (4 * sp.pi * Gs)) * (1 / Fp - 1)                                       # on-shell: F'(F^-1(g)) = F'(g_N)
dPpar_dr = dPpar_dg * sp.diff(g, r)
dPerp_minus_par = g * (g - gN) / (4 * sp.pi * Gs)
aniso = 0 if MUT else dPerp_minus_par                                                  # M1: anisotropy removed
res_A = sp.simplify(dPpar_dr - 2 * aniso / r + rho_c * g)
S1 = bool(res_A == 0)
P(f"\nS1 (A) equilibrium residual along the law, general F and rho_b: {res_A}  -> {'IDENTICALLY ZERO' if S1 else 'NONZERO'}")
s_ = Fp * gN / g
dP_iso = (g / (4 * sp.pi * Gs)) * (1 / s_ - 1)
res_I = sp.simplify(sp.factor(dP_iso * sp.diff(g, r) + rho_c * g))
P(f"S2 (I) equilibrium residual along the law: {res_I}")
res_I_newt = sp.simplify(res_I.subs(Ff(gN), gN).doit())
P(f"   ... with F = identity (Newtonian): {res_I_newt}")
a0 = sp.symbols("a0", positive=True); x = sp.symbols("x", positive=True)            # x = g, deep law g = sqrt(a0 g_N)
gN_deep = x ** 2 / a0; Fp_deep = sp.diff(sp.sqrt(a0 * sp.Symbol("y")), sp.Symbol("y")).subs(sp.Symbol("y"), gN_deep)
dPpar_deep = sp.simplify((x / (4 * sp.pi * Gs)) * (1 / Fp_deep - 1))
Ppar_deep = sp.integrate(dPpar_deep, (x, 0, x))
dperp_deep = sp.expand(x * (x - gN_deep) / (4 * sp.pi * Gs))
S3 = bool(sp.simplify(sp.series(Ppar_deep, x, 0, 3).removeO() + x ** 2 / (8 * sp.pi * Gs)) == 0 and
          sp.simplify(sp.series(dperp_deep, x, 0, 3).removeO() - x ** 2 / (4 * sp.pi * Gs)) == 0)
P(f"S3 deep limit: P_par = {Ppar_deep};  P_perp - P_par = {dperp_deep}  -> leading -g^2/8piG and +g^2/4piG: {S3}"
  "  (= minus the Maxwell stress (g g - g^2 I/2)/4piG up to a constant)")
RES["S1"] = dict(residual=str(res_A), identically_zero=S1)
RES["S2"] = dict(residual=str(res_I), newtonian=str(res_I_newt))
RES["S3"] = dict(P_par=str(Ppar_deep), P_perp_minus_par=str(dperp_deep), maxwell_leading=S3)


# ================================================================================================ tables (units G = a0 = 1)
def tables(nu):
    ly = np.linspace(-10, 7, 34001); yN = 10 ** ly
    gt = nu(yN) * yN; lg = np.log10(gt)
    s = np.gradient(lg, ly); Fp_ = s * gt / yN
    dPpar = gt / (4 * math.pi) * (1 / Fp_ - 1)
    Ppar = np.concatenate([[0.0], np.cumsum(0.5 * (dPpar[1:] + dPpar[:-1]) * np.diff(gt))])
    # zero point: P_par = 0 at the table's smallest g (~1e-5 a0), i.e. P_par(g -> 0) = 0 to O(g_min^2)
    Pperp = Ppar + gt * (gt - yN) / (4 * math.pi)
    return dict(yN=yN, g=gt, lg=lg, s=s, Fp=Fp_, Ppar=Ppar, Pperp=Pperp, mono=bool(np.all(np.diff(lg) > 0)))


TB = {k: tables(v) for k, v in NU.items()}


def at(T, key, gval):
    return np.interp(np.log10(gval), T["lg"], T[key])


# ================================================================================================ S4 kinetic realizability
T = TB["nu_mono"]
sel = T["g"] <= 10.0
neg = bool(np.any(T["Ppar"][sel] < 0))
gs = np.array([0.01, 0.1, 0.5, 1.0, 3.0, 10.0])
beta = 1 - at(T, "Pperp", gs) / at(T, "Ppar", gs)
S4 = "NOT KINETIC" if neg else "KINETIC POSSIBLE"
P(f"\nS4 zero point P_par(g->0) = 0: P_par < 0 somewhere in (0, 10 a0]: {neg} -> {S4}")
P("   g/a0      " + "  ".join(f"{v:8.2f}" for v in gs))
P("   P_par     " + "  ".join(f"{v:+8.4f}" for v in at(T, "Ppar", gs)) + "   (a0^2/G)")
P("   P_perp    " + "  ".join(f"{v:+8.4f}" for v in at(T, "Pperp", gs)))
P("   beta=1-P_perp/P_par " + "  ".join(f"{v:+7.2f}" for v in beta) + "   (a particle gas needs P >= 0 and beta <= 1)")
RES["S4"] = dict(label=S4, g=gs.tolist(), P_par=at(T, "Ppar", gs).tolist(), P_perp=at(T, "Pperp", gs).tolist(), beta=beta.tolist())

# ================================================================================================ S5 local WKB
k, w = sp.symbols("k omega")
rho0, d0, g0, Pp, cs = sp.symbols("rho0 d0 g0 Pp c_s", real=True)
dr_, du_ = sp.symbols("drho du")


def disp(cs2):
    dg = 4 * sp.pi * Gs * sp.I * dr_ / k                         # Poisson: i k dg = -4 pi G drho (sign absorbed; growth is sign-blind)
    mom = -sp.I * w * rho0 * du_ + sp.I * k * (Pp * dg + cs2 * dr_) - rho0 * dg - g0 * dr_
    con = -sp.I * w * dr_ + sp.I * k * rho0 * du_ + d0 * du_
    M = sp.Matrix([[sp.diff(e, v) for v in (dr_, du_)] for e in (mom, con)])
    return sp.expand(M.det())


def max_im(expr, subs, kk):
    roots = sp.Poly(expr.subs(subs).subs(k, kk), w).nroots()
    return max(float(sp.im(z)) for z in roots)


# deep SIS at r = 1 (G = 1, V = 1, a0 = A0R chosen so g/a0 = 0.1): rho0 = 1/(4pi), d0 = -2 rho0, g0 = 1, tau_ff = 1
gr = 0.1
# dP_par/dg is dimensionless in units with G = 1 (P ~ g^2/G), so the table slope at g/a0 = 0.1 applies directly with g0 = 1
Pp_v = float((at(T, "Ppar", gr * 1.0001) - at(T, "Ppar", gr * 0.9999)) / (gr * 0.0002))
sub0 = {rho0: 1 / (4 * math.pi), d0: -2 / (4 * math.pi), g0: 1.0, Pp: Pp_v, Gs: 1.0}
e0 = disp(0)
ims = [max_im(e0, sub0, kk) for kk in (1e1, 1e3, 1e5)]
ill = ims[2] > 5 * ims[1] > 0
e1 = disp(cs ** 2)
sub1 = dict(sub0); sub1[cs] = math.sqrt(0.5)
ims1 = [max_im(e1, sub1, kk) for kk in (1e1, 1e3, 1e5)]
S5 = "ILL-POSED" if ill else ("DUST-LIKE" if max(ims) <= 3 * math.sqrt(4 * math.pi * sub0[rho0]) else "UNSTABLE (bounded)")
P(f"\nS5 local WKB along the field (deep SIS point, g/a0 = {gr}, tau_ff = 1): max Im omega at k = 1e1/1e3/1e5: "
  + "/".join(f"{v:.3g}" for v in ims) + f" -> {S5}")
P("   k perpendicular to g: |g| unchanged at first order, no compressive stress response -> omega^2 = -4 pi G rho0 (Jeans, bounded)")
P("   addendum, + kinetic pressure c_s^2 = V^2/2: max Im omega at k = 1e1/1e3/1e5: " + "/".join(f"{v:.3g}" for v in ims1)
  + "  (bounded; units 1/tau_ff)")
RES["S5"] = dict(label=S5, point=dict(g_over_a0=gr, Pp=Pp_v), max_im_field_only=ims, max_im_with_kinetic=ims1)


# ================================================================================================ N1 Hernquist toy
def hern(Tb, nu, a, mode):
    M = 1.0
    rhob = lambda rr: M * a / (2 * math.pi * rr * (rr + a) ** 3)
    gNr = lambda rr: M / (rr + a) ** 2
    glaw = lambda rr: nu(gNr(rr)) * gNr(rr)

    def f(rr, y):
        gg = 10 ** y[0]; s = at(Tb, "s", gg)
        if mode == "I":
            gp = -s * (2 * gg / rr - 4 * math.pi * rhob(rr))
        else:
            gNl = at(Tb, "yN", gg)
            gp = -s * (2 * gg / rr - 4 * math.pi * rhob(rr) * gg / gNl)
        return [gp / gg / math.log(10)]
    r_out = 300 * max(a, 1.0); rr = np.geomspace(r_out, 0.5 * a, 200)
    sol = solve_ivp(f, (r_out, 0.5 * a), [math.log10(glaw(r_out))], t_eval=rr, rtol=1e-10, atol=1e-12, method="LSODA")
    d = sol.y[0] - np.log10(glaw(sol.t))
    m = sol.t <= 10 * a
    return float(np.max(np.abs(d[m])))


N1 = {}
for kn, nu in NU.items():
    for a in (0.05, 0.3, 1.0, 3.0, 10.0):
        N1[f"{kn}|{a}"] = dict(A=hern(TB[kn], nu, a, "A"), I=hern(TB[kn], nu, a, "I"))
N1_ok = all(v["A"] <= 1e-3 for v in N1.values())
P("\nN1 Hernquist (max |dlog g| vs the law, 0.5-10 a):")
for kk, v in N1.items():
    P(f"   {kk:14s}  A {v['A']:.2e}   I {v['I']:.3f}")
P(f"   N1 (A within 1e-3 dex everywhere): {'PASS' if N1_ok else 'FAIL -> VOID'}")
RES["N1"] = dict(rows=N1, pass_=N1_ok)

# ================================================================================================ D1 raw SPARC
with contextlib.redirect_stdout(io.StringIO()):
    g4, _ = C4.exec_slices(os.path.join(LANES, "CFG4_galaxy_law.py"), [(None, 'banner("K  CONTROLS')], name="cfg4_galaxy_ro")
UPS, Rm, GB, GO, OK, WWr, GI = (g4[kk] for kk in ("UPS", "Rm", "GB", "GO", "OK", "WW", "GI"))
iu = int(np.argmin(np.abs(UPS - 0.61)))
gb4, go4, ok4, ww4 = GB[:, iu], GO[:, iu], OK[:, iu], WWr[:, iu]


def rms(gp):
    r1 = np.log10(np.where(ok4, go4, 1.0)) - np.log10(np.where(ok4, gp, 1.0))
    return float(np.sqrt(np.sum(ww4 * r1 ** 2) / np.sum(ww4)))


def integ_gal(R, gN, a0v, mode, nsub=40):
    """inward from the outermost point; units: g in a0, r in metres; m = r^2 g_N piecewise linear."""
    Tb = TB["nu_mono"]; x = gN / a0v; m = R ** 2 * x
    gout = float(NU["nu_mono"](np.array([x[-1]]))[0] * x[-1])
    y = R[-1] ** 2 * gout; out = np.empty(R.size); out[-1] = gout

    def rhs(rr, yy, mp):
        gg = max(yy / rr ** 2, 1e-12); s = float(at(Tb, "s", gg))
        if mode == "I" or mode == "A_noaniso":
            c = s
        else:
            c = s * gg / float(at(Tb, "yN", gg))
        return 2 * yy / rr * (1 - s) + c * mp
    for i in range(R.size - 1, 0, -1):
        r1, r0 = R[i], R[i - 1]; mp = (m[i] - m[i - 1]) / (r1 - r0)
        h = (r0 - r1) / nsub; rr = r1
        for _ in range(nsub):
            k1 = rhs(rr, y, mp); k2 = rhs(rr + h / 2, y + h / 2 * k1, mp); k3 = rhs(rr + h / 2, y + h / 2 * k2, mp)
            k4 = rhs(rr + h, y + h * k3, mp); y += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); rr += h
        out[i - 1] = y / r0 ** 2
    return out * a0v


D1 = {}
for foot in FOOTS:
    a0v = C7.A0_SI[foot]
    law = np.where(ok4, NU["nu_mono"](np.where(ok4, gb4, 1.0) / a0v) * np.where(ok4, gb4, 1.0), 1.0)
    pred = {"I": law.copy(), "A": law.copy(), "A_noaniso": law.copy()}
    ngal = 0
    for gi in np.unique(GI):
        idx = np.where((GI == gi) & ok4 & (gb4 > 0))[0]
        if idx.size < 3:
            continue
        idx = idx[np.argsort(Rm[idx])]
        ngal += 1
        for md in pred:
            pred[md][idx] = integ_gal(Rm[idx], gb4[idx], a0v, md)
    rl = rms(law); rI = rms(pred["I"]); rA = rms(pred["A"]); rN = rms(pred["A_noaniso"])
    D1[foot] = dict(rms_law=rl, rms_I=rI, rms_A=rA, rms_A_noaniso=rN, d_I=rI - rl, d_A=rA - rl, n_gal=ngal, n_pts=int(ok4.sum()))
    P(f"\nD1 [{foot}] SPARC Upsilon 0.61, {ngal} galaxies integrated: rms law {rl:.4f}  isotropic {rI:.4f} (d {rI - rl:+.4f})  "
      f"anisotropic {rA:.4f} (d {rA - rl:+.1e})  [M2 anisotropy removed {rN:.4f}]")
A_ok = all(abs(D1[f]["d_A"]) <= 0.002 for f in FOOTS)
if all(D1[f]["d_I"] >= 0.03 for f in FOOTS):
    D1lab = "ISOTROPIC EXCLUDED"
elif all(abs(D1[f]["d_I"]) <= 0.005 for f in FOOTS):
    D1lab = "CONSISTENT"
else:
    D1lab = "TENSION"
D1lab = D1lab if A_ok else "VOID (anisotropic does not reproduce the law's rms)"
P(f"D1 label: {D1lab}; anisotropic implementation check |d_A| <= 0.002: {A_ok}")
RES["D1"] = dict(rows=D1, label=D1lab, A_check=A_ok)

# ================================================================================================ label / teeth
if MUT:
    m1 = not S1
    m2 = all(abs(D1[f]["rms_A_noaniso"] - D1[f]["rms_I"]) <= 1e-6 for f in FOOTS)
    RES["MUTATE"] = dict(M1_identity_fails=m1, M2_noaniso_equals_I=m2)
    P(f"\nMUTATE: M1 identity fails without anisotropy: {m1}; M2 anisotropy-removed reproduces isotropic rms: {m2}")
    rc = 1 if (m1 and m2) else 0
else:
    void = not (S1 and N1_ok)
    lab = ("VOID" if void else
           f"LAW = EQUILIBRIUM OF A FIELD-ALIGNED STRESS (spherical): S1 {S1}, N1 {N1_ok}, D1-A {A_ok}; ISOTROPIC: {D1lab}; "
           f"KINETIC: {S4}; DYNAMICS: {S5}")
    RES["label"] = lab
    P(f"\nLANE LABEL: {lab}")
    rc = 1 if void else 0
RES["wall_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, f"cfg660_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg660{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(rc)
