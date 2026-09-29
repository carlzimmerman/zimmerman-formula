# -*- coding: utf-8 -*-
"""CFG176 -- the nature of dark energy in the owner's flowing-vacuum picture (door 11): the equation of state and w(z)
each reading implies, and whether that is consistent with LambdaCDM (w = -1) and with CFG6's committed DESI DR2 fits.

Frozen: FROZEN_QUESTION.md (body + Addendum 1, both written before this script).  Run from anywhere; ~1 min.
  MUTATE=1  the flow's momentum inertia (rho + p) is replaced by rho (dust-like; the assumption implicit in CFG174's
            'swept column').  H1 and H2 must fail (rc = 1).
  MUTATE=2  the accumulation reading is replaced by a steady deposit (a0 constant).  H3 and H4 must fail (rc = 1).
Reads (read-only): CFG6_common.py (the DESI DR2 chains and CPL helpers), CFG6_a0z_branches_results.json,
CFG174_door11_vacuum_column/CFG174_vacuum_column_results.json.  Writes only into this directory.
kappa = 1/2 FITTED.  Nothing here says the theory is closed."""
import os, sys, math, json
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
sys.path.insert(0, CFGDIR)
import CFG6_common as C6                                   # noqa: E402  (read-only helpers; no bytecode written)

MUTATE = int(os.environ.get("MUTATE", "0"))
TAG = "" if MUTATE == 0 else "_MUTATE%d" % MUTATE
OUTF = open(os.path.join(HERE, "CFG176_de_flow%s.out" % TAG), "w", encoding="utf-8")
RES = {"lane": "CFG176", "mutate": MUTATE, "checks": [], "numbers": {}}
N = RES["numbers"]
FAILS = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUTF.write(s + "\n")


def banner(t):
    P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)


def check(cid, statement, measured, ok, lb=True):
    ok = bool(ok)
    RES["checks"].append(dict(id=cid, ok=ok, load_bearing=lb, statement=statement, measured=str(measured)))
    if lb and not ok:
        FAILS.append(cid)
    P("  [%s] %s  %s" % ("PASS" if ok else ("FAIL" if lb else "FAIL(reported)"), cid, statement))
    P("         measured: %s" % measured)
    return ok


def z0(e):
    return sp.simplify(e) == 0


def fl(x):
    return float(x)


# ---------------------------------------------------------------------------------------------------- constants
G = 6.6743e-11; C = 299792458.0; MSUN = 1.98847e30; PC = 3.0856775814913673e16; KPC = 1e3 * PC; MPC = 1e6 * PC
GYR = 3.15576e16
RHO_L = 5.8424e-27                        # FP0's rho_Lambda (H0 = 67.4, Omega_L = 0.6847), as CFG174
OL_FP0 = 0.6847
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
H0 = 67.66e3 / MPC; OM = 0.3111; OL = 1.0 - OM      # CFG174's t(z) cosmology (Planck18)
R174 = json.load(open(os.path.join(CFGDIR, "CFG174_door11_vacuum_column", "CFG174_vacuum_column_results.json")))
CFG6R = json.load(open(os.path.join(CFGDIR, "CFG6_a0z_branches_results.json")))


def inertia(onepw):
    """the momentum inertia of a w-medium per unit energy density: (rho + p)/rho = 1 + w.  MUTATE=1: dust-like, 1."""
    return np.ones_like(np.asarray(onepw, float)) if MUTATE == 1 else np.asarray(onepw, float)


P("CFG176 (MUTATE=%d): the nature of dark energy in the flowing-vacuum picture.  kappa = 1/2 FITTED." % MUTATE)
P("Signature (-,+,+,+), c = 1 in the algebra.  Cosmology for t(z): flat, H0 = 67.66, Omega_m = 0.3111 (CFG174);"
  " rho_Lambda = 5.8424e-27 kg/m^3 (FP0, CFG174).")

# ================================================================================================ controls
banner("CONTROLS  (CFG174's committed R and a0(z); CFG6's committed B5 crossing fractions)")


def age(z):
    f = lambda a: 1.0 / (a * H0 * math.sqrt(OM / a ** 3 + OL))
    return quad(f, 0, 1.0 / (1 + z), limit=200)[0]


T0 = age(0.0)
R = {}
for fn, a0 in A0.items():
    R[fn] = a0 / (2 * math.pi * G) / (RHO_L * C * T0)
dR = max(abs(R[f] / R174["Q1"][f]["R"] - 1) for f in A0)
P("  t0 = %.4f Gyr;  R = Sigma_M/(rho_L c t0): canonical %.4f, alt %.4f (CFG174 JSON %.4f / %.4f)"
  % (T0 / GYR, R["canonical"], R["alt"], R174["Q1"]["canonical"]["R"], R174["Q1"]["alt"]["R"]))
check("C1", "CFG174's column ratio R reproduces from its committed JSON (both footings)", "max rel diff %.1e" % dR, dR < 1e-9)
dz = {}
for zs in ("0.85", "1.5", "2.5"):
    dz[zs] = math.log10(age(float(zs)) / T0) - R174["Q3"][zs]["dlog_a0"]
check("C2", "CFG174's accumulation a0(z)/a0(0) = t(z)/t0 reproduces at z = 0.85, 1.5, 2.5",
      ", ".join("%s: %+.1e" % (k, v) for k, v in dz.items()), max(abs(v) for v in dz.values()) < 1e-9)
CH = {k: C6.load_chain(k) for k in C6.DESI_ORDER}
b5d = {}
for k in C6.DESI_ORDER:
    wt, w0s, was, oms = CH[k]
    w25 = w0s + was * 2.5 / 3.5
    cross_ = ((w0s > -1) & (w25 < -1)) | ((w0s < -1) & (w25 > -1))
    b5d[k] = float(np.sum(wt[cross_]) / np.sum(wt)) - CFG6R["numbers"]["B5"][k]["p_cross"]
check("C3", "CFG6's B5 crossing fractions reproduce from the committed thinned chains (same code)",
      ", ".join("%s %+.1e" % (k, v) for k, v in b5d.items()), max(abs(v) for v in b5d.values()) < 1e-12)

# ================================================================================================ geometry helpers
def christoffel(g, X):
    n = len(X)
    gi = sp.simplify(g.inv())
    Gm = [[[sp.simplify(sum(gi[l, s] * (sp.diff(g[s, m], X[k]) + sp.diff(g[s, k], X[m]) - sp.diff(g[m, k], X[s]))
                             for s in range(n)) / 2) for k in range(n)] for m in range(n)] for l in range(n)]
    return Gm, gi                                             # Gm[l][m][k] = Gamma^l_{mk}


def ricci(Gm, X):
    n = len(X)
    Ric = sp.zeros(n, n)
    for m in range(n):
        for k in range(n):
            Ric[m, k] = sp.simplify(sum(sp.diff(Gm[l][m][k], X[l]) for l in range(n))
                                    - sum(sp.diff(Gm[l][m][l], X[k]) for l in range(n))
                                    + sum(Gm[l][l][s] * Gm[s][m][k] for l in range(n) for s in range(n))
                                    - sum(Gm[l][k][s] * Gm[s][m][l] for l in range(n) for s in range(n)))
    return Ric


# ================================================================================================ Q1 sympy
banner("Q1  CAN A MOVING MEDIUM STAY VACUUM-LIKE (w = -1)?  sympy")
rho, p, w, q = sp.symbols("rho p w q", real=True)
be = sp.symbols("beta", positive=True)
gam = 1 / sp.sqrt(1 - be ** 2)
eta = sp.diag(-1, 1, 1, 1)


def Tpf(r_, p_, u):
    return (r_ + p_) * (u * u.T) + p_ * eta               # upper indices; eta^{-1} = eta


u_rest = sp.Matrix([1, 0, 0, 0])
u_b = sp.Matrix([gam, gam * be, 0, 0])
dT = sp.simplify(Tpf(rho, p, u_b) - Tpf(rho, p, u_rest))
nz = [sp.factor(e) for e in dT if not z0(e)]
sol_u = sp.solve(nz, p, dict=True)
P("  T(u_beta) - T(u_rest), nonzero entries: %s" % sorted(set(str(e) for e in nz)))
check("S1a", "T^{mu nu}(u) is the same for a moving and a resting u iff rho + p = 0 (a vacuum's 'flow' is invisible in T)",
      "solve -> %s" % sol_u, sol_u == [{p: -rho}])
Lb = sp.Matrix([[gam, gam * be, 0, 0], [gam * be, gam, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
T0m = sp.diag(rho, p, p, p)
dB = sp.simplify(Lb * T0m * Lb.T - T0m)
sol_b = sp.solve([sp.factor(e) for e in dB if not z0(e)], p, dict=True)
check("S1b", "the rest-frame stress diag(rho, p, p, p) is invariant under every boost iff rho + p = 0 (only then no rest frame)",
      "solve -> %s" % sol_b, sol_b == [{p: -rho}])
M35 = (Tpf(rho, p, u_b) * eta).subs(be, sp.Rational(3, 5))
ev = {sp.simplify(k): v for k, v in M35.eigenvals().items()}
ev_v = {sp.simplify(k): v for k, v in M35.subs(p, -rho).eigenvals().items()}
check("S1c", "eigenstructure of T^mu_nu (beta = 3/5): generic fluid {-rho: 1 (along u), p: 3}; w = -1 {-rho: 4} -- every "
      "timelike vector is an eigenvector, so there is no Landau rest frame", "generic %s; vacuum %s" % (ev, ev_v),
      ev == {-rho: 1, p: 3} and ev_v == {-rho: 4})
Tb = Tpf(rho, w * rho, u_b)
e_, g_, Ppar, Pperp = Tb[0, 0], Tb[0, 1], Tb[1, 1], Tb[2, 2]
ok = (z0(g_ - (1 + w) * rho * gam ** 2 * be) and z0(e_ - rho * (1 + (1 + w) * gam ** 2 * be ** 2))
      and z0(Ppar - rho * ((1 + w) * gam ** 2 * be ** 2 + w)) and z0(Pperp - w * rho))
check("S1d", "a w-fluid moving at beta in the CMB frame: momentum density g = (1+w) rho gamma^2 beta (zero for beta != 0 iff "
      "w = -1); e = rho[1 + (1+w) gamma^2 beta^2]; P_par = rho[(1+w) gamma^2 beta^2 + w]; P_perp = w rho",
      "g = %s" % sp.factor(g_), ok)

# ---- S2 energy equation, vacuum rigidity, compaction law
t, x = sp.symbols("t x", real=True)
rf = sp.Function("rho")(t, x)
vf = sp.Function("v")(t, x)
gf = 1 / sp.sqrt(1 - vf ** 2)
X2 = [t, x]
uU2 = [gf, gf * vf]
uL2 = [-gf, gf * vf]
eta2 = sp.diag(-1, 1)
T2 = [[(1 + w) * rf * uU2[m] * uU2[n] + w * rf * eta2[m, n] for n in range(2)] for m in range(2)]
div2 = [sum(sp.diff(T2[m][n], X2[m]) for m in range(2)) for n in range(2)]
E2 = -sum(uL2[n] * div2[n] for n in range(2))
tgt2 = sum(uU2[m] * sp.diff(rf, X2[m]) for m in range(2)) + (1 + w) * rf * sum(sp.diff(uU2[m], X2[m]) for m in range(2))
ok_e = z0(E2 - tgt2)
ok_v = z0(div2[0].subs(w, -1) - sp.diff(rf, t)) and z0(div2[1].subs(w, -1) + sp.diff(rf, x))
nn = sp.symbols("n", positive=True)
rn = sp.Function("r")
sol_n = sp.dsolve(sp.Eq(rn(nn).diff(nn), (1 + w) * rn(nn) / nn))
ok_n = sp.simplify(sol_n.rhs / nn ** (w + 1)).free_symbols.isdisjoint({nn})
check("S2", "-u_nu d_mu T^{mu nu} = u.grad(rho) + (rho + p) div u exactly (1+1, any v(t,x)): compaction along the flow is "
      "proportional to 1 + w; for w = -1 conservation reads d_t rho = d_x rho = 0 (a Lambda-vacuum cannot be compacted "
      "anywhere); for constant w, rho ~ n^(1+w) (n = volume-compression density)",
      "identity %s; vacuum rigid %s; rho(n) = %s" % (ok_e, ok_v, sol_n.rhs), ok_e and ok_v and ok_n)

# ---- S3 NEC bound on momentum, and the w = -1 + flux medium
e, gg, Pp = sp.symbols("e g P", real=True)
Tlow = sp.Matrix([[e, -gg], [-gg, Pp]])                      # lowered from T^{00}=e, T^{0x}=g, T^{xx}=P
kp, km = sp.Matrix([1, 1]), sp.Matrix([1, -1])
Tkp, Tkm = sp.expand((kp.T * Tlow * kp)[0]), sp.expand((km.T * Tlow * km)[0])
okA = z0(Tkp - (e + Pp - 2 * gg)) and z0(Tkm - (e + Pp + 2 * gg))
okB = z0((e_ + Ppar - 2 * g_) - (1 + w) * rho * gam ** 2 * (1 - be) ** 2) and \
    z0((e_ + Ppar + 2 * g_) - (1 + w) * rho * gam ** 2 * (1 + be) ** 2)
Mq = sp.Matrix([[rho, q], [q, -rho]]) * sp.diag(-1, 1)
evq = sorted([sp.simplify(k) for k in Mq.eigenvals()], key=str)
Tlq = sp.diag(-1, 1) * sp.Matrix([[rho, q], [q, -rho]]) * sp.diag(-1, 1)
Tkq = [sp.expand((k_.T * Tlq * k_)[0]) for k_ in (kp, km)]
okC = set(evq) == {-rho + sp.I * q, -rho - sp.I * q} and set(Tkq) == {2 * q, -2 * q}
check("S3", "NEC along +-n gives |T^{0n}| <= (T^{00} + T^{nn})/2 for ANY stress, i.e. g/e <= (1 + w_par)/2; a boosted perfect "
      "fluid has T_kk = (1+w) rho gamma^2 (1 -+ beta)^2; a w = -1 medium given an energy flux q has eigenvalues -rho +- i q "
      "(Hawking-Ellis type IV) and T_kk = -+2q: it violates the NEC", "T_k+ = %s; eigenvalues %s; T_kk %s" % (Tkp, evq, Tkq),
      okA and okB and okC)

# ---- S4 FRW tilt: a homogeneous flow relative to the CMB frame decays
tt = sp.symbols("t", real=True)
xs_ = sp.symbols("x y z", real=True)
XF = (tt,) + xs_
af = sp.Function("a", positive=True)(tt)
gF = sp.diag(-1, af ** 2, af ** 2, af ** 2)
GmF, giF = christoffel(gF, XF)
rt, pt, vt = sp.Function("rho")(tt), sp.Function("p")(tt), sp.Function("v")(tt)
gt = 1 / sp.sqrt(1 - vt ** 2)
uUF = [gt, gt * vt / af, 0, 0]
uLF = [sum(gF[i, j] * uUF[j] for j in range(4)) for i in range(4)]
TmF = sp.Matrix(4, 4, lambda m, n: (rt + pt) * uUF[m] * uLF[n] + (pt if m == n else 0))
nu = 1
divF = (sum(sp.diff(TmF[m, nu], XF[m]) for m in range(4)) + sum(GmF[m][m][l] * TmF[l, nu] for m in range(4) for l in range(4))
        - sum(GmF[l][m][nu] * TmF[m, l] for m in range(4) for l in range(4)))
ok_t = z0(divF - sp.diff(af ** 3 * TmF[0, 1], tt) / af ** 3) and z0(TmF[0, 1] - (rt + pt) * gt ** 2 * vt * af)
check("S4", "a homogeneous tilted w-fluid in FRW: nabla_mu T^mu_x = a^-3 d/dt(a^3 T^0_x), T^0_x = a (rho+p) gamma^2 v, so "
      "a^4 (rho+p) gamma^2 v is conserved and gamma^2 v ~ a^(3w-1) (~ a^-4 near w = -1): a flow of the dark energy "
      "relative to the CMB frame decays unless driven, with force density (1 - 3w) H g", "identity %s" % ok_t, ok_t)
Rs_F = sp.simplify(sum(giF[i, j] * ricci(GmF, XF)[i, j] for i in range(4) for j in range(4)))
check("C4", "geometry sanity: the helper's Ricci scalar for flat FRW is 6(a''/a + a'^2/a^2)", str(Rs_F),
      z0(Rs_F - 6 * (sp.diff(af, tt, 2) / af + sp.diff(af, tt) ** 2 / af ** 2)))

# ---- S5 boosted-fluid CMB-frame quantities and the column requirement
weff1 = sp.simplify((e_ + (Ppar + 2 * Pperp) / 3) / e_)       # 1 + w_eff (isotropic average)
Dl = sp.simplify((Ppar - Pperp) / e_)                           # anisotropic stress fraction Delta
act = sp.simplify(e_ + Ppar + 2 * Pperp)                        # active (Tolman) density
Rsym = sp.symbols("R", positive=True)
Xsub = Rsym * (1 - be ** 2) / (be * (1 - Rsym * be))
ok5 = (z0(weff1 - (1 + w) * (1 + sp.Rational(4, 3) * gam ** 2 * be ** 2) / (1 + (1 + w) * gam ** 2 * be ** 2))
       and z0(act - rho * ((1 + w) * gam ** 2 * (1 + be ** 2) + 2 * w))
       and z0((g_ / e_).subs(w, Xsub - 1) - Rsym)
       and z0(weff1.subs(w, Xsub - 1) - Rsym * (1 / be + be / 3))
       and z0(Dl.subs(w, Xsub - 1) - Rsym * be))
check("S5", "CMB-frame view of a w-fluid at beta: 1 + w_eff = (1+w)(1 + 4/3 g^2b^2)/(1 + (1+w) g^2b^2); active density "
      "rho[(1+w) g^2 (1+b^2) + 2w]; if it carries the column fraction g/e = R then rest-frame 1+w = R(1-b^2)/[b(1-Rb)], "
      "1 + w_eff = R(1/b + b/3) >= 4R/3 (at b -> 1) and Delta = R b", "all identities %s" % ok5, ok5)

# ================================================================================================ Q1 numbers
banner("Q1 NUMBERS  the minimum departure from w = -1 for a flow that carries CFG174's column; compaction; active density")
bet = [600e3 / C, 0.01, 0.1, 0.3, 0.5, 0.9, 0.99, 0.999]
tab1 = {}
for fn in A0:
    Rf = R[fn]
    rows = []
    P("  %s: R = %.3f.  Any NEC-respecting medium: 1 + w_par >= 2R = %.3f.  Perfect fluid at beta:" % (fn, Rf, 2 * Rf))
    P("      beta        rest-frame 1+w     CMB-frame 1+w_eff   Delta (anisotropic)")
    for b in bet:
        X = Rf * (1 - b * b) / (b * (1 - Rf * b)); W = Rf * (1 / b + b / 3); D = Rf * b
        rows.append(dict(beta=b, onepw_rest=X, onepw_eff=W, Delta=D))
        P("      %-10.4g  %-17.4g  %-18.4g  %.4f" % (b, X, W, D))
    bmin = brentq(lambda b: Rf * (1 - b * b) / (b * (1 - Rf * b)) - 2.0, 1e-6, 0.9999)
    P("      dominant energy condition (w_rest <= 1) needs beta >= %.3f; CMB-frame 1 + w_eff >= 4R/3 = %.3f (beta -> 1)"
      % (bmin, 4 * Rf / 3))
    tab1[fn] = dict(R=Rf, NEC_min_onepw_par=2 * Rf, pf_min_onepw_eff=4 * Rf / 3, beta_min_DEC=bmin, rows=rows)
N["Q1_table"] = tab1

# compaction / active density at r_M (P2 point mass: rho_c = a0/(4 pi G r sqrt(1+x^2)), CFG44)
comp = []
P("\n  The law's phantom density at r_M (P2 point mass), in units of rho_Lambda, and the volume compression a DE-like")
P("  medium needs to present it (rho ~ n^(1+w)):  log10(n/n_inf) = log10(C)/(1+w)")
onepw_list = [0.04, 0.162, 0.248, 0.333, 1.0]
P("    footing    log M_b  r_M [kpc]   C = rho_c/rho_L   log10 compression at 1+w = " + ", ".join("%.3g" % v for v in onepw_list))
for fn, a0 in A0.items():
    for lm in (9, 10, 11, 12):
        M = 10 ** lm * MSUN; rM = math.sqrt(G * M / a0); rc = a0 / (4 * math.pi * G * rM * math.sqrt(2)); Cc = rc / RHO_L
        lc = [math.log10(Cc) / v for v in onepw_list]
        comp.append(dict(footing=fn, logM=lm, rM_kpc=rM / KPC, C=Cc, log10_compression=dict(zip(map(str, onepw_list), lc))))
        P("    %-9s  %-7d  %-10.2f  %-16.3g  %s" % (fn, lm, rM / KPC, Cc, ", ".join("%.3g" % v for v in lc)))
N["Q1_compaction"] = comp
slopeC = np.polyfit([d["logM"] for d in comp[:4]], [math.log10(d["C"]) for d in comp[:4]], 1)[0]
thr = {}
for w0v in (-0.667, -0.752, -0.838, -0.95, -0.99):
    Kk = -2 * w0v / (1 + w0v)
    thr[str(w0v)] = math.sqrt((Kk - 1) / (Kk + 1))
P("  active density rho(1+3w) at rest: repulsive for w < -1/3.  Speed above which a w-fluid's active density turns "
  "attractive: " + ", ".join("w = %s: beta > %.3f" % (k, v) for k, v in thr.items()))
N["Q1_attraction_threshold_beta"] = thr
check("R-Q1f", "(reported) the law's density at r_M is 10^3-10^5 rho_Lambda and scales as M^-1/2; a DE-like medium "
      "(1+w <= 0.333) must be volume-compressed by >= 10^10 to present it; at rest a w < -1/3 medium repels",
      "C = %.3g .. %.3g; slope %.3f; min log10 compression at 1+w = 0.333: %.1f"
      % (min(d["C"] for d in comp), max(d["C"] for d in comp), slopeC,
         min(d["log10_compression"]["0.333"] for d in comp)),
      1e3 <= min(d["C"] for d in comp) and max(d["C"] for d in comp) <= 1e5 and abs(slopeC + 0.5) < 1e-9
      and min(d["log10_compression"]["0.333"] for d in comp) >= 10, lb=False)

# tilt decay
tilt = {}
for w0v in (-0.667, -0.752, -0.838, -0.95):
    ex = 3 * w0v - 1
    tilt[str(w0v)] = dict(exponent=ex, log10_decay_from_z1100=ex * math.log10(1101), log10_decay_from_z2p5=ex * math.log10(3.5),
                          efold_Gyr=1 / ((1 - 3 * w0v) * H0) / GYR)
P("  a free DE flow decays as gamma^2 v ~ a^(3w-1): " + "; ".join(
    "w %s: z=1100->0 %.1f dex, z=2.5->0 %.2f dex, e-fold %.1f Gyr" % (k, v["log10_decay_from_z1100"], v["log10_decay_from_z2p5"],
                                                                     v["efold_Gyr"]) for k, v in tilt.items()))
N["Q1_tilt_decay"] = tilt

# H1 (numeric, the MUTATE=1 target)
gH1 = float(inertia(0.0)) * (1 / (1 - 0.25)) * 0.5            # (1+w) gamma^2 beta at w = -1, beta = 0.5 (inertia(1+w=0))
check("H1", "a w = -1 medium flowing at beta = 0.5 carries zero momentum density and zero energy flux (and, S2, cannot be "
      "compacted): every flow observable is proportional to 1 + w", "g/rho = %.3g" % gH1, gH1 == 0.0)

# ================================================================================================ Q2
banner("Q2  THE 11C TIME-DIRECTION READING  (flow = the Hubble flow)")
P("  2a. For T = -rho_Lambda g the flow can be identified with the Hubble flow or any other u (S1a): no new content;")
P("      the background is LambdaCDM, w = -1, and a0 = kappa c sqrt(G rho_Lambda) is flat (CFG6 branch A).")
Nf = sp.Function("N", positive=True)(tt)
gM = sp.diag(-Nf ** 2, af ** 2, af ** 2, af ** 2)
GmM, giM = christoffel(gM, XF)
RicM = ricci(GmM, XF)
RsM = sp.simplify(sum(giM[i, j] * RicM[i, j] for i in range(4) for j in range(4)))
uUM = [1 / Nf, 0, 0, 0]
DU = sp.Matrix(4, 4, lambda m, k: sp.diff(uUM[k], XF[m]) + sum(GmM[k][m][l] * uUM[l] for l in range(4)))   # nabla_m u^k
DL = DU * gM                                                                                                # nabla_m u_k
DUU = giM * DU                                                                                              # nabla^m u^k
K1 = sp.simplify(sum(DL[m, k] * DUU[m, k] for m in range(4) for k in range(4)))
K2 = sp.simplify(sum(DU[m, m] for m in range(4)) ** 2)
K3 = sp.simplify(sum(DL[m, k] * DUU[k, m] for m in range(4) for k in range(4)))
accv = [sp.simplify(sum(uUM[m] * DU[m, al] for m in range(4))) for al in range(4)]
K4 = sp.simplify(sum(accv[i] * accv[j] * gM[i, j] for i in range(4) for j in range(4)))
c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
Gs, Lam, rm0 = sp.symbols("G Lambda rho_m0", positive=True)
Kt = c1 * K1 + c2 * K2 + c3 * K3 - c4 * K4
Lmini = Nf * af ** 3 * (RsM - 2 * Lam - Kt) / (16 * sp.pi * Gs) - Nf * rm0
ELs = sp.euler_equations(Lmini, [Nf, af], tt)
A_, ad, add = sp.symbols("A ad add", positive=True)


def at_N1(expr):
    e2 = expr.subs(Nf, sp.Integer(1)).doit()
    return sp.simplify(e2.subs(sp.Derivative(af, (tt, 2)), add).subs(sp.Derivative(af, tt), ad).subs(af, A_))


EN = at_N1(ELs[0].lhs)
Ea = at_N1(ELs[1].lhs)
bsum = c1 + 3 * c2 + c3
rho_tot = rm0 / A_ ** 3 + Lam / (8 * sp.pi * Gs)
H2_t = 8 * sp.pi * Gs * rho_tot / (3 * (1 + bsum / 2))
solad = sp.solve(EN, ad)
ok_F = len(solad) > 0 and z0(solad[0] ** 2 / A_ ** 2 - H2_t)
soladd = sp.solve(Ea, add)
acc_t = -(4 * sp.pi * Gs / (3 * (1 + bsum / 2))) * (rm0 / A_ ** 3 - 2 * Lam / (8 * sp.pi * Gs))
ok_A = len(soladd) > 0 and z0(soladd[0].subs(ad, A_ * sp.sqrt(H2_t)) / A_ - acc_t)
rho_ae = 3 * H2_t / (8 * sp.pi * Gs) - rho_tot
w_ae = -1 - A_ * sp.diff(sp.log(rho_ae), A_) / 3
w_tot = (-Lam / (8 * sp.pi * Gs)) / rho_tot
ok_W = z0(rho_ae + (bsum / 2) * 3 * H2_t / (8 * sp.pi * Gs)) and z0(w_ae - w_tot) and z0(K4)
P("  2b. Einstein-aether terms on FRW for the comoving (Hubble-flow) unit vector: K1 = %s, K2 = %s, K3 = %s, K4 = %s"
  % (K1, K2, K3, K4))
check("S6", "minisuperspace (sympy Euler-Lagrange in the lapse N and a, N -> 1): with a unit timelike flow along the Hubble "
      "flow, H^2 = 8 pi G (rho_m + rho_Lambda) / [3 (1 + beta/2)], beta = c1 + 3 c2 + c3, and a''/a = -(4 pi G_cos/3)"
      "(rho_m - 2 rho_Lambda): the flow's energy is rho_flow = -(beta/2) rho_crit(t), tracking H^2 with w_flow = w_total",
      "Friedmann %s; acceleration %s; tracking %s" % (ok_F, ok_A, ok_W), ok_F and ok_A and ok_W)
check("H5", "the 11C reading implies no w(z) of its own: the shape of H(z) is LambdaCDM's exactly (w_DE = -1); the only new "
      "content of a dynamical time-flow is G_cos = G/(1 + (c1 + 3c2 + c3)/2)", "from S6", ok_F and ok_A and ok_W)
# 2c theta channel
th2c = []
for d in comp:
    if d["footing"] == "canonical":
        th2c.append(dict(logM=d["logM"], beta_needed=2 * d["C"] * OL_FP0))
P("  2c. theta-channel (scoped to the homogeneous beta H^2 term): stopping the expansion inside a bound region changes the")
P("      flow's energy by at most (|beta|/2) rho_crit, so presenting the law's density at r_M needs |beta| >= 2 C Omega_L: "
  + ", ".join("M_b 1e%d: %.3g" % (d["logM"], d["beta_needed"]) for d in th2c))
N["Q2_theta_channel_beta_needed"] = th2c
check("R-Q2c", "(reported) the theta-channel needs |c1 + 3c2 + c3| >= 10^3 (G_cos/G would be ~10^-3); gradient terms around "
      "masses (the generalized-aether MOND route, CFG172's lane) are not scored here",
      "min %.3g" % min(d["beta_needed"] for d in th2c), min(d["beta_needed"] for d in th2c) >= 1e3, lb=False)

# ================================================================================================ Q3
banner("Q3  THE CFG174 ACCUMULATION READING: a0(z) ~ t(z)/t0")
NACC = 0 if MUTATE == 2 else 2                          # rho_DE ~ t^NACC under the density tie (a0 ~ sqrt(rho_DE) ~ t)
AI = 1e-5


def solve_tpow(n, Om=OM):
    OD = 1 - Om
    ti = 2 / (3 * math.sqrt(Om)) * AI ** 1.5

    def run(t0):
        f = lambda a, y: [1 / (a * math.sqrt(Om / a ** 3 + OD * (max(y[0], 0.0) / t0) ** n))]
        return solve_ivp(f, (AI, 1.0), [ti], rtol=1e-11, atol=1e-15, dense_output=True)
    t0 = brentq(lambda t0: run(t0).y[0, -1] - t0, 0.3, 3.0, xtol=1e-13)
    return t0, run(t0)


agr = np.linspace(1 / 3.5, 1.0, 400)                    # uniform in a over z <= 2.5 (CFG6's cpl_equivalent convention)
zgr = 1 / agr - 1
t0I, solI = solve_tpow(NACC)
tI = solI.sol(agr)[0]
EI = np.sqrt(OM / agr ** 3 + OL * (tI / t0I) ** NACC)
wI = -1 - (NACC / 3.0) / (EI * tI)
w0I, waI = C6.cpl_equivalent(zgr, wI)
a0I = {zs: 0.5 * NACC * math.log10(solI.sol(1 / (1 + zs))[0] / t0I) for zs in (0.85, 1.5, 2.5)}
Hrat = {zs: math.sqrt(OM * (1 + zs) ** 3 + OL * (solI.sol(1 / (1 + zs))[0] / t0I) ** NACC) / math.sqrt(OM * (1 + zs) ** 3 + OL)
        for zs in (0.5, 1.0, 2.5)}
w_at = {zs: float(np.interp(zs, zgr[::-1], wI[::-1])) for zs in (0.0, 0.5, 1.0, 2.5)}
P("  3-I (density tie, rho_DE ~ t^%d, self-consistent): H0 t0 = %.4f (LambdaCDM %.4f); w(z) = -1 - %d/(3 H t):" %
  (NACC, t0I, T0 * H0, NACC) + " " + ", ".join("z=%.1f %.3f" % (k, v) for k, v in w_at.items()))
P("       CPL-equivalent (w0, wa) = (%.3f, %.3f); a0(z)/a0(0): %s dex; H/H_LCDM: %s" % (
    w0I, waI, ", ".join("z=%.2f %+.3f" % (k, v) for k, v in a0I.items()), ", ".join("z=%.1f %.3f" % (k, v) for k, v in Hrat.items())))
chainI = {}
for k in C6.DESI_ORDER:
    wt, w0s, was, oms = CH[k]
    W = wt / wt.sum()
    mu = np.array([np.sum(W * w0s), np.sum(W * was)])
    d = np.vstack([w0s - mu[0], was - mu[1]])
    cov = np.array([[np.sum(W * d[i] * d[j]) for j in range(2)] for i in range(2)])   # explicit sums (no BLAS)
    ci = np.linalg.inv(cov)
    dm = np.array([w0I - mu[0], waI - mu[1]])
    dl = np.array([-1 - mu[0], 0 - mu[1]])
    chainI[k] = dict(p_w0_le_model=float(np.sum(W[w0s <= w_at[0.0]])), mahal_model=float(math.sqrt(dm @ ci @ dm)),
                     mahal_LCDM=float(math.sqrt(dl @ ci @ dl)), p_w0_lt_m1=float(np.sum(W[w0s < -1])))
    P("       %-10s p(w0 <= %.3f) = %.2e;  Gaussian-equivalent distance of the model's (w0, wa): %.1f sigma (LambdaCDM's "
      "(-1, 0): %.1f sigma); p(w0 < -1) = %.4f" % (k, w_at[0.0], chainI[k]["p_w0_le_model"], chainI[k]["mahal_model"],
                                                   chainI[k]["mahal_LCDM"], chainI[k]["p_w0_lt_m1"]))
N["Q3_I"] = dict(n_power=NACC, H0t0=t0I, w=w_at, cpl=[w0I, waI], dlog_a0=a0I, H_over_LCDM=Hrat, chains=chainI)
check("H3", "the density-tie accumulation (a0 ~ t, so rho_DE ~ t^2) is phantom, w0 < -1.3, and lies outside every committed "
      "DESI DR2 chain (weighted p(w0 <= model) < 1e-3 for DESY5, Pantheon+, Union3)",
      "w0 = %.3f; p = %s" % (w_at[0.0], ", ".join("%.1e" % v["p_w0_le_model"] for v in chainI.values())),
      w_at[0.0] < -1.3 and all(v["p_w0_le_model"] < 1e-3 for v in chainI.values()))

# CFG6's band at z = 2.5 (all dark-energy branches, three combinations, 16-84%)
pred = CFG6R["numbers"]["P"]["pred"]
lo, hi = 0.0, 0.0
for br, dd in pred.items():
    if br.startswith("rival"):
        continue
    for k, v in dd.items():
        trip = v["2.5"]
        lo, hi = min(lo, trip[0]), max(hi, trip[2])
a0acc25 = a0I[2.5]
P("  CFG6's band at z = 2.5 (every dark-energy branch, all three combinations, 16-84%%): [%+.3f, %+.3f] dex" % (lo, hi))
check("H4", "the accumulation reading's a0(2.5) lies more than 0.3 dex below CFG6's DESI band", "a0(2.5) %+.3f vs band low %+.3f "
      "(gap %.3f dex)" % (a0acc25, lo, lo - a0acc25), lo - a0acc25 > 0.3)
N["Q3_band_CFG6_z2p5"] = [lo, hi]

# 3-II the vacuum pays
fdeps = [0.01, 0.1, 0.3, 1.0]
steady = MUTATE == 2
res3 = []
for fdep in fdeps:
    OV0 = (1 - OM) / (1 + fdep); Od0 = fdep * OV0

    def rhs(a, y, t0):
        tt_, rV = y
        tt_ = max(tt_, 0.0)
        rdep = Od0 / a ** 3 if steady else Od0 * (tt_ / t0) / a ** 3
        E = math.sqrt(max(OM / a ** 3 + rdep + rV, 1e-300))
        Q = 0.0 if steady else Od0 / (t0 * a ** 3)
        return [1 / (a * E), -Q / (a * E)]

    def run(t0):
        return solve_ivp(lambda a, y: rhs(a, y, t0), (1.0, AI), [t0, OV0], rtol=1e-11, atol=1e-15, dense_output=True)
    t_early = 2 / (3 * math.sqrt(OM)) * AI ** 1.5
    t0b = brentq(lambda t0: run(t0).y[0, -1] - t_early, 0.3, 3.0, xtol=1e-13)
    s = run(t0b)
    tt_a, rV_a = s.sol(agr)
    rdep_a = Od0 / agr ** 3 if steady else Od0 * (tt_a / t0b) / agr ** 3
    E_a = np.sqrt(OM / agr ** 3 + rdep_a + rV_a)
    Q_a = np.zeros_like(agr) if steady else Od0 / (t0b * agr ** 3)
    w_a = -1 + Q_a / (3 * E_a * rV_a)
    w0c, wac = C6.cpl_equivalent(zgr, w_a)
    a0_25 = 0.0 if steady else math.log10(s.sol(1 / 3.5)[0] / t0b)
    pwa = {k: float(np.sum(CH[k][0][CH[k][2] >= wac]) / np.sum(CH[k][0])) for k in C6.DESI_ORDER}
    res3.append(dict(f_dep=fdep, H0t0=t0b, w0=float(w_a[-1]), cpl=[w0c, wac], dlog_a0_z2p5=a0_25,
                     rhoV_z2p5_over_0=float(s.sol(1 / 3.5)[1] / OV0), p_wa_ge_model=pwa))
    P("  3-II f_dep = %-5g H0 t0 = %.4f; w0 = %.4f; CPL (w0, wa) = (%.3f, %+.3f); rho_V(2.5)/rho_V0 = %.3f; a0(2.5) %+.3f dex;"
      " p(wa >= model): %s" % (fdep, t0b, w_a[-1], w0c, wac, s.sol(1 / 3.5)[1] / OV0, a0_25,
                               ", ".join("%s %.3f" % (k, v) for k, v in pwa.items())))
pwa0 = {k: float(np.sum(CH[k][0][CH[k][2] > 0]) / np.sum(CH[k][0])) for k in C6.DESI_ORDER}
N["Q3_II"] = dict(rows=res3, p_wa_gt_0=pwa0)
check("R-Q3II", "(reported) the vacuum-pays accumulation has wa > 0 (w rising into the past) for every f_dep, while every "
      "committed chain has p(wa > 0) < 0.05", "wa: %s; p(wa>0): %s" % (", ".join("%+.3f" % r_["cpl"][1] for r_ in res3),
                                                                     ", ".join("%.4f" % v for v in pwa0.values())),
      all(r_["cpl"][1] > 1e-6 for r_ in res3) and all(v < 0.05 for v in pwa0.values()), lb=False)   # 1e-6: float-noise guard (added after the MUTATE=2 run)

# ================================================================================================ Q4
banner("Q4  WHAT BOUNDS 1 + w TODAY, AND SO THE FLOW  (committed CFG6 numbers + the committed chains, no download)")
pc = CFG6R["numbers"]["P"]["posterior_conditioned"]
P("  committed (CFG6): DESI DR2 CPL (w0, wa) " + "; ".join("%s (%.3f, %.2f)" % (k, *C6.DESI[k]) for k in C6.DESI_ORDER))
P("                    crossing w = -1 in 0 < z < 2.5: " + "; ".join("%s %.4f at z %.2f" % (k, CFG6R["numbers"]["B5"][k]["p_cross"],
                                                                        CFG6R["numbers"]["B5"][k]["z_cross_med"]) for k in C6.DESI_ORDER))
P("                    healthy thawing, posterior-conditioned: best-node w0_eff " + "; ".join(
    "%s %.3f (<w0_eff> %.3f)" % (k, pc[k]["best"][2], pc[k]["mean_w0eff"]) for k in C6.DESI_ORDER) + "; LambdaCDM: 1 + w = 0")
Q4 = {}
agrid = np.linspace(1e-4, 1.0, 3000)
for k in C6.DESI_ORDER:
    wt, w0s, was, oms = CH[k]
    op = 1 + w0s
    pct = C6.wpct(op, wt, [2.5, 16, 50, 84, 97.5])
    wapct = C6.wpct(was, wt, [2.5, 16, 50, 84, 97.5])
    carried = np.empty(len(w0s))
    for i0 in range(0, len(w0s), 1500):
        sl = slice(i0, i0 + 1500)
        zz = 1 / agrid - 1
        fde = C6.f_DE(zz[None, :], w0s[sl, None], was[sl, None])
        E = np.sqrt(oms[sl, None] / agrid[None, :] ** 3 + (1 - oms[sl, None]) * fde)
        dtda = 1 / (agrid[None, :] * E)
        t0s = np.trapz(dtda, agrid, axis=1) + 2 / (3 * np.sqrt(oms[sl])) * agrid[0] ** 1.5
        wz = w0s[sl, None] + was[sl, None] * (1 - agrid[None, :])
        integ = 0.5 * np.clip(inertia(1 + wz), 0, None) * fde * dtda
        carried[sl] = np.trapz(integ, agrid, axis=1) / t0s
    ci_ = C6.wpct(carried, wt, [50, 84, 97.5])
    today_iso = 0.5 * inertia(op)
    Q4[k] = dict(onepw0_pct=list(map(fl, pct)), wa_pct=list(map(fl, wapct)),
                 today_iso_pct=list(map(fl, C6.wpct(today_iso, wt, [50, 97.5]))),
                 today_pf_pct=list(map(fl, C6.wpct(1.5 * today_iso, wt, [50, 97.5]))),
                 p_today_pf_ge_R={fn: float(np.sum(wt[1.5 * today_iso >= R[fn]]) / np.sum(wt)) for fn in A0},
                 carried_iso_pct=list(map(fl, ci_)), carried_pf_pct=list(map(fl, 1.5 * ci_)))
    P("  %-10s 1+w0 [2.5,16,50,84,97.5] = %s; wa = %s" % (k, ", ".join("%.3f" % v for v in pct), ", ".join("%.2f" % v for v in wapct)))
    P("             momentum today g/rho_DE <= (1+w0)/2: median %.3f, 97.5%% %.3f (perfect fluid at beta -> 1: %.3f, %.3f);"
      " p(3(1+w0)/4 >= R) can/alt %.4f/%.4f" % (Q4[k]["today_iso_pct"][0], Q4[k]["today_iso_pct"][1], Q4[k]["today_pf_pct"][0],
                                             Q4[k]["today_pf_pct"][1], Q4[k]["p_today_pf_ge_R"]["canonical"], Q4[k]["p_today_pf_ge_R"]["alt"]))
    P("             column carried over the cosmic age / (rho_DE0 c t0): isotropic [50,84,97.5] %s; perfect fluid %s"
      % (", ".join("%.4f" % v for v in ci_), ", ".join("%.4f" % v for v in 1.5 * ci_)))
# the healthy thawing best nodes (CFG6 P3), from the thawing solver itself
thaw = {}
zt = np.concatenate([np.linspace(0, 3, 601), np.linspace(3.01, 30, 2700)])
for k in C6.DESI_ORDER:
    om_b, lam_b = pc[k]["best"][0], pc[k]["best"][1]
    tr = C6.thaw_tracks(lam_b, om_b, zt)
    E = 10 ** tr["logE"]; rde = 10 ** (2 * tr["dens"]); wz = tr["w"]
    dtdz = 1 / ((1 + zt) * E)
    t0t = np.trapz(dtdz, zt) + (2 / 3) * (1 + zt[-1]) ** -1.5 / math.sqrt(om_b)
    car = np.trapz(0.5 * np.clip(inertia(1 + wz), 0, None) * rde * dtdz, zt) / t0t
    thaw[k] = dict(Om=om_b, lam=lam_b, w0=float(tr["w0"]), carried_iso=float(car), carried_pf=float(1.5 * car))
    P("  thawing best node %-10s (Om %.2f, lambda %.2f): w0 %.3f; carried column iso %.4f, perfect fluid %.4f" %
      (k, om_b, lam_b, tr["w0"], car, 1.5 * car))
N["Q4_chains"] = Q4
N["Q4_thawing_best_nodes"] = thaw
worst = max(max(v["carried_pf_pct"][2] for v in Q4.values()), max(v["carried_pf"] for v in thaw.values()))
check("H2", "the committed dark-energy fits cannot carry CFG174's column: the time-integrated NEC-limited column (perfect-fluid "
      "bound, 97.5th percentile, every DESI combination; and the healthy thawing best nodes) is below R on both footings "
      "(LambdaCDM: exactly 0)", "largest carried fraction %.4f vs R %.3f / %.3f" % (worst, R["canonical"], R["alt"]),
      worst < min(R.values()))
# shear the anisotropic stress would need
Scoef = 2 * OL * quad(lambda a: a * a / math.sqrt(OM / a ** 3 + OL), 0, 1)[0]
eps_max = max(v["onepw0_pct"][4] for v in Q4.values())
Dreq = {fn: 1.5 * (2 * R[fn] - eps_max) for fn in A0}
P("  Bianchi I (S7): sigma/H0 = 2 Omega_DE Delta int_0^1 a^2/E da = %.3f Delta.  Making up the NEC shortfall at today's most"
  " generous 1+w0 (97.5%%, %.3f) needs Delta = %.3f / %.3f -> sigma/H0 = %.3f / %.3f (can/alt): a %.0f-%.0f%% anisotropy of"
  " today's expansion" % (Scoef, eps_max, Dreq["canonical"], Dreq["alt"], Scoef * Dreq["canonical"], Scoef * Dreq["alt"],
                          100 * Scoef * Dreq["canonical"], 100 * Scoef * Dreq["alt"]))
N["Q4_shear"] = dict(coef=Scoef, eps_max=eps_max, Delta_req=Dreq, sigma_over_H0={fn: Scoef * v for fn, v in Dreq.items()})
A1f, A2f, A3f = [sp.Function(n_, positive=True)(tt) for n_ in ("A1", "A2", "A3")]
gB = sp.diag(-1, A1f ** 2, A2f ** 2, A3f ** 2)
GmB, giB = christoffel(gB, XF)
RicB = ricci(GmB, XF)
Rm = [sp.simplify(giB[i, i] * RicB[i, i]) for i in range(4)]
Vb = A1f * A2f * A3f
Hs = [sp.diff(A_i, tt) / A_i for A_i in (A1f, A2f, A3f)]
Hb = sum(Hs) / 3
ok7 = z0(Rm[1] - (Rm[1] + Rm[2] + Rm[3]) / 3 - sp.diff(Vb * (Hs[0] - Hb), tt) / Vb)
check("S7", "Bianchi I: R^1_1 - (1/3) R^i_i = V^-1 d/dt[V (H_1 - H_bar)], so (Einstein) V^-1 d(V sigma_1)/dt = 8 pi G pi_1 with "
      "pi_1 = (2/3) Delta rho_DE for a flow along x", "identity %s" % ok7, ok7)
# flow-speed table (perfect fluid)
spd = []
P("  flow speed allowed for a perfect fluid with rest-frame 1+w = X under a CMB-frame ceiling eps (97.5% 1+w0):"
  " gamma^2 beta^2 <= (eps - X)/[X (4/3 - eps)]  (X -> 0: unbounded -- a vacuum's speed is unobservable)")
for k in C6.DESI_ORDER:
    eps = Q4[k]["onepw0_pct"][4]
    row = {}
    for X in (0.01, 0.05, 0.1, 0.2):
        if X >= eps:
            row[str(X)] = None
        else:
            Gg = (eps - X) / (X * (4 / 3 - eps)); row[str(X)] = math.sqrt(Gg / (1 + Gg))
    spd.append(dict(combo=k, eps=eps, beta_max=row))
    P("    %-10s eps %.3f: " % (k, eps) + ", ".join("X %s: beta <= %s" % (kk, "n/a" if v is None else "%.3f" % v) for kk, v in row.items()))
N["Q4_speed"] = spd
check("R-Q4", "(reported) the requirement 1 + w_par >= 2R exceeds the largest committed 97.5th-percentile 1 + w0",
      "2R = %.3f / %.3f vs %.3f" % (2 * R["canonical"], 2 * R["alt"], eps_max), 2 * min(R.values()) > eps_max, lb=False)

# ================================================================================================ Q5 (Addendum 1)
banner("Q5  (ADDENDUM 1) A MEDIUM WITH NO REST MASS: WHICH STRESS-ENERGY EACH READING NEEDS")
trT = sp.simplify((Tpf(rho, p, u_b) * eta).trace())
sol_tr = sp.solve(trT, p)
w13 = sp.simplify(((Ppar + 2 * Pperp) / (3 * e_)).subs(w, sp.Rational(1, 3)))
Phi = sp.symbols("Phi", positive=True)
kk = sp.Matrix([1, 1, 0, 0])
Tn = Phi * kk * kk.T
okN = Tn[0, 0] == Phi and Tn[0, 1] == Phi and Tn[1, 1] == Phi and Tn[2, 2] == 0 and z0((Tn * eta).trace())
Phif = sp.Function("Phi")(tt)
kUF = [1, 1 / af, 0, 0]
TU = sp.Matrix(4, 4, lambda m, n: Phif * kUF[m] * kUF[n])
divN = [sum(sp.diff(TU[m, n], XF[m]) for m in range(4)) + sum(GmF[m][m][l] * TU[l, n] for m in range(4) for l in range(4))
        + sum(GmF[n][m][l] * TU[m, l] for m in range(4) for l in range(4)) for n in range(4)]
Cn = sp.symbols("C_n", positive=True)
okNF = all(z0(dv.subs(Phif, Cn / af ** 4).doit()) for dv in divN)
check("S8", "a medium with no rest mass (traceless T): the trace -rho + 3p is frame-invariant, so T^mu_mu = 0 forces the "
      "isotropic w_eff = 1/3 in EVERY frame; a null flow (Phi k k) has e = g = P_par = Phi, P_perp = 0 (w_par = 1, NEC "
      "saturated) and in FRW dilutes as a^-4 (radiation: rho ~ a^-3(1+w) = a^-4); its active density is 2e > 0",
      "trace %s -> p = %s; w_eff(1/3 fluid, any beta) = %s; null dust %s; FRW a^-4 %s" % (trT, sol_tr, w13, okN, okNF),
      z0(trT - (-rho + 3 * p)) and sol_tr == [rho / 3] and w13 == sp.Rational(1, 3) and okN and okNF)
# the PG 'river' (11A): what medium does a steady inflow need?
T_, th_, ph_ = sp.symbols("t theta phi", real=True)
r_ = sp.symbols("r", positive=True)
vr = sp.Function("v")(r_)
gPG = sp.Matrix([[-(1 - vr ** 2), vr, 0, 0], [vr, 1, 0, 0], [0, 0, r_ ** 2, 0], [0, 0, 0, r_ ** 2 * sp.sin(th_) ** 2]])
XP = (T_, r_, th_, ph_)
GmP, giP = christoffel(gPG, XP)
RicP = ricci(GmP, XP)
RsP = sp.simplify(sum(giP[i, j] * RicP[i, j] for i in range(4) for j in range(4)))
Gmix = sp.simplify(giP * RicP - RsP / 2 * sp.eye(4))
rv2 = r_ * vr ** 2
okPG = (z0(Gmix[0, 0] + sp.diff(rv2, r_) / r_ ** 2) and z0(Gmix[1, 1] + sp.diff(rv2, r_) / r_ ** 2)
        and z0(Gmix[2, 2] + sp.diff(rv2, r_, 2) / (2 * r_)) and z0(Gmix[3, 3] - Gmix[2, 2])
        and z0(Gmix[0, 1]) and z0(Gmix[1, 0]))
mG, Hh = sp.symbols("m H", positive=True)
Gsub = lambda vexpr: sp.simplify(Gmix.subs(vr, vexpr).doit())
Gsum = Gsub(-sp.sqrt(2 * mG / r_ + Hh ** 2 * r_ ** 2))            # v^2 = 2m/r + H^2 r^2 (GR's superposition in v^2)
okSum = all(z0(Gsum[i, i] + 3 * Hh ** 2) for i in range(4))
Glin = Gsub(-sp.sqrt(2 * mG / r_) + Hh * r_)                         # linear superposition: infall + Hubble outflow
rho_x = sp.simplify(-Glin[0, 0] / (8 * sp.pi * Gs) - 3 * Hh ** 2 / (8 * sp.pi * Gs))
pr_x = sp.simplify(Glin[1, 1] / (8 * sp.pi * Gs) + 3 * Hh ** 2 / (8 * sp.pi * Gs))
pt_x = sp.simplify(Glin[2, 2] / (8 * sp.pi * Gs) + 3 * Hh ** 2 / (8 * sp.pi * Gs))
okLin = (z0(rho_x + 3 * Hh * sp.sqrt(2 * mG) / (8 * sp.pi * Gs * r_ ** sp.Rational(3, 2))) and z0(pr_x + rho_x)
         and z0(pt_x + rho_x / 4))
check("S9", "11A's river (PG metric, any steady v(r)): G^t_t = G^r_r = -(r v^2)'/r^2, G^th_th = -(r v^2)''/(2r), no flux: the "
      "medium is radially vacuum-like (p_r = -rho) with rho = (r v^2)'/(8 pi G r^2); v^2 = 2m/r + H^2 r^2 is pure Lambda "
      "(the river is a frame, not a medium); the LINEAR superposition v = -sqrt(2m/r) + H r needs an extra medium "
      "rho_x = -3H sqrt(2m)/(8 pi G r^1.5) < 0 (WEC violated) with p_r = -rho_x, p_perp = -rho_x/4",
      "general %s; superposition in v^2 %s; linear %s (rho_x = %s)" % (okPG, okSum, okLin, rho_x), okPG and okSum and okLin)
# numbers: the linear cross-term medium at r_M, and the null flow's cosmology
HL = math.sqrt(8 * math.pi * G * RHO_L / 3)
pgn = []
for lm in (9, 10, 11, 12):
    M = 10 ** lm * MSUN; a0 = A0["canonical"]; rM = math.sqrt(G * M / a0)
    pgn.append(dict(logM=lm, rho_x_over_rhoL=-math.sqrt(2 * G * M / rM ** 3) / HL,
                    g_cross_over_a0=HL * math.sqrt(2 * G * M) / (2 * math.sqrt(rM)) / a0))
P("  11A linear-superposition medium at r_M (canonical): " + "; ".join(
    "1e%d: rho_x/rho_L = %.3g, g_cross/a0 = %.2e" % (d["logM"], d["rho_x_over_rhoL"], d["g_cross_over_a0"]) for d in pgn))
N["Q5_PG_linear"] = pgn
null = {}
kB, hbar, TCMB, NEFF = 1.380649e-23, 1.054571817e-34, 2.7255, 3.044          # standard values (not committed; reported only)
rho_gam = (math.pi ** 2 / 15) * (kB * TCMB) ** 4 / (hbar * C) ** 3 / C ** 2
Om_r = rho_gam * (1 + 0.2271 * NEFF) / (3 * H0 ** 2 / (8 * math.pi * G))
for fn in A0:
    On = R[fn] * OL
    zeq = OM / On - 1
    Hr = {zs: math.sqrt(OM * (1 + zs) ** 3 + On * (1 + zs) ** 4 + (1 - OM - On)) / math.sqrt(OM * (1 + zs) ** 3 + OL)
          for zs in (0.5, 1.0, 2.5)}
    null[fn] = dict(Omega_null0=On, z_eq_matter=zeq, H_over_LCDM=Hr, over_Omega_r=On / Om_r)
    P("  M2 null flow carrying the column today at c (%s): Omega_null,0 = R Omega_L = %.3f; dominates matter before z = %.2f;"
      " H/H_LCDM %s; %.0f x the CMB+neutrino radiation density (T_CMB, N_eff standard, not committed)"
      % (fn, On, zeq, ", ".join("z=%.1f %.3f" % (k, v) for k, v in Hr.items()), On / Om_r))
N["Q5_null_flow"] = null
check("H6", "a massless (null or radiation-like) flow cannot be the dark energy (w_eff = 1/3, S8); carrying the column today "
      "it would dominate matter before z < 1 and raise H(2.5) by > 20% over LambdaCDM on both footings",
      ", ".join("%s z_eq %.2f, H(2.5) x%.2f" % (fn, v["z_eq_matter"], v["H_over_LCDM"][2.5]) for fn, v in null.items()),
      all(v["z_eq_matter"] < 1 and v["H_over_LCDM"][2.5] > 1.2 for v in null.values()))

stress = [
    dict(reading="11A inflow (control)", needs="M1 (Lambda) if the river is GR's v^2 = 2GM/r + H^2 r^2: a frame, no medium, no new "
         "content; the linear superposition needs a negative-energy medium (S9)",
         bound="WEC violated; |rho_x| = %.3g-%.3g rho_L at r_M, and its pull there is only %.1e-%.1e a0" % (
             min(abs(d["rho_x_over_rhoL"]) for d in pgn), max(abs(d["rho_x_over_rhoL"]) for d in pgn),
             min(d["g_cross_over_a0"] for d in pgn), max(d["g_cross_over_a0"] for d in pgn))),
    dict(reading="11B' directional, compressible", needs="momentum and compaction, both prop. to (rho + p): M3 (1+w > 0, a "
         "field flow) or M2 (massless, w_eff = 1/3)", bound="M3: DESI 1+w0 (Q4) -> carried column <= %.4f of the vacuum column "
         "vs R = %.3f; M2: not dark energy, H(z) (H6)" % (worst, R["canonical"])),
    dict(reading="11C time direction", needs="M1 or M4 (preferred-frame vacuum, T ~ g on the background)",
         bound="w = -1 exactly; G_cos = G/(1+beta/2) (S6); PPN alpha1/alpha2 (door gate G6, not scored here)"),
    dict(reading="CFG174 accumulation", needs="3-I: phantom rho_DE ~ t^2; 3-II: a non-HT decaying vacuum",
         bound="3-I outside the chains (H3); 3-II wa > 0 against the chains; a0(2.5) off CFG6's band (H4)"),
]
N["Q5_stress_by_reading"] = stress
for s_ in stress:
    P("  %-32s needs: %s\n  %-32s bound: %s" % (s_["reading"], s_["needs"], "", s_["bound"]))

# ================================================================================================ summary
banner("SUMMARY")
nlb = sum(1 for c in RES["checks"] if c["load_bearing"])
npass = sum(1 for c in RES["checks"] if c["ok"])
P("CFG176 (MUTATE=%d): %d/%d checks pass; load-bearing failures: %s" % (MUTATE, npass, len(RES["checks"]),
                                                                         ", ".join(FAILS) if FAILS else "none"))
RES["summary"] = dict(n_checks=len(RES["checks"]), n_pass=npass, n_load_bearing=nlb, load_bearing_failures=FAILS)
json.dump(RES, open(os.path.join(HERE, "CFG176_de_flow_results%s.json" % TAG), "w"), indent=1, default=str)
OUTF.close()
sys.exit(1 if FAILS else 0)
