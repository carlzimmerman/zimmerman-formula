#!/usr/bin/env python3
"""X6_dust_coupling (criteria fd303cac8b, committed alone first): the owner's stop-ruled design lane on the dust coupling.

Finite candidate list (FROZEN_CRITERIA.md §1), each with its action term; graded on (a) hosted systems, (b) cluster cores,
(c) linear growth, (d) isolated galaxies, (e) health + a radiation era, with the record's machinery read-only and cheap
estimators. sympy for the derivations (X-D1..X-D10), reproductions first (X-K1..X-K5), then the grades table and the verdict.

  OMP_NUM_THREADS=1 nice -n 15 python3 x6_dust_coupling.py              -> x6_dust_coupling.out, x6_dust_coupling_results.json
  X6_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 x6_dust_coupling.py  -> *_MUTATE.out / *_results_MUTATE.json (exit 1 by design)

MUTATE: C0's dust coupling switched to -grad Phi (alpha = 0; U1's mutation): X-D5 and X-K2 must FAIL.
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle species; not theory closed; no PM run; no downloads."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
if sys.platform == "darwin" and os.environ.get("MallocMediumZone") != "0":
    # AMENDMENT A1 (post-result, code only): macOS's medium malloc zone kept freed ODE buffers resident (RUN1 peak 4.36 GB);
    # deterministic re-exec with it disabled (as U1). No effect on any number.
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, MallocMediumZone="0"))
import json, math, time, hashlib, resource, csv, gc, ctypes
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
MUT = os.environ.get("X6_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
ALPHA = 0.0 if MUT else 1.0                  # weight of grad Xi in the khronon dust force (v3: 1, kinematic identity X-D1)
OUT, CHK = [], {}
RES = {"lane": "X6_dust_coupling", "criteria": "fd303cac8b", "date": "2026-10-23", "mutate": MUT, "alpha_khronon": ALPHA,
       "settings": "kappa = 1/2 FITTED; footings never pooled; no dark-matter particle species; not theory closed"}
np.seterr(all="ignore")


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=str(val), threshold=str(thr)); P(f"{name} {'PASS' if ok else 'FAIL'} {val} [{thr}]")


READS = {}


def rd(rel):
    p = os.path.join(REPO, rel); READS[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return json.load(open(p)) if rel.endswith(".json") else open(p).read()


try:
    _LIBC = ctypes.CDLL(None); _LIBC.malloc_zone_pressure_relief.restype = ctypes.c_size_t
except Exception:
    _LIBC = None


def relieve():                                    # macOS: hand freed blocks back to the OS (RSS hygiene only; A1)
    gc.collect()
    if _LIBC is not None and sys.platform == "darwin":
        _LIBC.malloc_zone_pressure_relief(None, ctypes.c_size_t(0))


def rss_gb():
    pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; return pk / 1e9 if sys.platform == "darwin" else pk / 1e6


A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
P("X6_dust_coupling" + (" [MUTATE: khronon dust on -grad Phi, alpha = 0]" if MUT else "") +
  ": criteria fd303cac8b; kappa = 1/2 FITTED; footings never pooled; no particle species; not theory closed")

# =====================================================================================================  D: sympy derivations
P("\n=== D: derivations (sympy) ===")
t, x, y, z = sp.symbols("t x y z", real=True); X4 = [t, x, y, z]


def christoffel(g, gi, X):
    dg = [[[sp.diff(g[a, c], X[d]) for d in range(4)] for c in range(4)] for a in range(4)]
    return [[[sp.together(sum(gi[l, s] * (dg[s][m][n] + dg[s][n][m] - dg[m][n][s]) for s in range(4)) / 2)
              for n in range(4)] for m in range(4)] for l in range(4)]


N_ = sp.Function("N", positive=True)(*X4); ZE = sp.Function("zeta")(*X4)
BE = [sp.Function(n)(*X4) for n in ("beta_x", "beta_y", "beta_z")]
g1 = sp.diag(-N_ ** 2, sp.exp(2 * ZE), sp.exp(2 * ZE), sp.exp(2 * ZE)); g1i = sp.diag(-1 / N_ ** 2, sp.exp(-2 * ZE), sp.exp(-2 * ZE), sp.exp(-2 * ZE))
g2 = sp.zeros(4); g2i = sp.zeros(4); g2[0, 0] = -N_ ** 2 + sum(b_ ** 2 for b_ in BE); g2i[0, 0] = -1 / N_ ** 2
for i in range(3):
    g2[0, i + 1] = g2[i + 1, 0] = BE[i]; g2[i + 1, i + 1] = 1; g2i[0, i + 1] = g2i[i + 1, 0] = BE[i] / N_ ** 2
    for j in range(3):
        g2i[i + 1, j + 1] = (1 if i == j else 0) - BE[i] * BE[j] / N_ ** 2
inv_ok = all(sp.simplify(e) == 0 for e in (g1 * g1i - sp.eye(4))) and all(sp.simplify(e) == 0 for e in (g2 * g2i - sp.eye(4)))
GAM = {}
d1_res = {}
for lab, (g, gi) in {"conformally_flat_zero_shift": (g1, g1i), "flat_with_shift": (g2, g2i)}.items():
    Gm = christoffel(g, gi, X4); GAM[lab] = Gm
    nlo = [-N_, 0, 0, 0]; nup = [sum(gi[m, n] * nlo[n] for n in range(4)) for m in range(4)]
    a_ = [sum(nup[n] * (sp.diff(nlo[m], X4[n]) - sum(Gm[l][n][m] * nlo[l] for l in range(4))) for n in range(4)) for m in range(4)]
    r_ = [sp.simplify(a_[i] - sp.diff(sp.log(N_), X4[i])) for i in (1, 2, 3)] + [sp.simplify(sum(nup[m] * a_[m] for m in range(4)))]
    d1_res[lab] = [str(v) for v in r_]
ok_d1 = inv_ok and all(v == "0" for vv in d1_res.values() for v in vv)
RES["D1"] = dict(residuals=d1_res, inverse_ok=inv_ok,
                 meaning="a_mu = D_mu ln N for the unit normal n_mu = -N d_mu tau: the khronon charge's acceleration relative to free fall "
                         "is the lapse gradient (= grad Xi at PN order in unitary gauge). 'Charge on -grad Phi' (alpha = 0) <=> grad Xi = 0 <=> "
                         "Y = 0 <=> no law; alpha is kinematics, not a coupling constant (C1a, C3alpha have no action).")
check("X-D1", ok_d1, f"a_i - d_i ln N and n.a for 2 metric families: {d1_res}", "all residuals 0")

# X-D2 mimetic dust: geodesic identity on metric (ii); PN limit Q = 1 + eps Xi
PHI = sp.Function("phi")(*X4); Gm = GAM["flat_with_shift"]
ulo = [sp.diff(PHI, X4[m]) for m in range(4)]; uup = [sum(g2i[m, n] * ulo[n] for n in range(4)) for m in range(4)]
norm = sum(g2i[m, n] * ulo[m] * ulo[n] for m in range(4) for n in range(4))
geo = [sp.expand(sp.together(sum(uup[n] * (sp.diff(ulo[m], X4[n]) - sum(Gm[l][n][m] * ulo[l] for l in range(4))) for n in range(4))
                             - sp.diff(norm, X4[m]) / 2) * N_ ** 4) == 0 for m in range(4)]
eps, Ph, Sd = sp.symbols("epsilon Phi S", real=True); W = sp.symbols("w_x w_y w_z", real=True); w2 = sum(v ** 2 for v in W)
Xn = (1 + eps * Sd) ** 2 / (1 + 2 * eps * Ph) - eps * w2 / (1 - 2 * eps * Ph)        # -g^{mu nu} d tau d tau, tau = t + sigma
XI = Ph - Sd + w2 / 2                                                                  # BS's Xi = Phi - sigma_dot + |grad sigma|^2/2
resX = sp.simplify(sp.series(Xn, eps, 0, 2).removeO() - (1 - 2 * eps * XI))
resQ = sp.simplify(sp.series(Xn ** sp.Rational(-1, 2), eps, 0, 2).removeO() - (1 + eps * XI))
ok_d2 = all(geo) and resX == 0 and resQ == 0
RES["D2"] = dict(geodesic_identity=geo, PN_X_residual=str(resX), PN_Q_residual=str(resQ),
                 meaning="u = d phi with g^{mu nu} d phi d phi = -1 is geodesic (mimetic dust feels -grad Phi); X = 1 - 2 eps Xi, Q = 1 + eps Xi: "
                         "the khronon at Q == 1 IS the mimetic constraint (Xi = 0), so geodesic khronon dust <=> Xi = 0 <=> no law")
check("X-D2", ok_d2, f"geodesic identity {geo}; X residual {resX}; Q residual {resQ}", "identity True x4; residuals 0")

# X-D3 alpha-family statics (a0 = 1 units): (alpha - 1 + mu(x)) x = yN, g = alpha x
al, yN, xs = sp.symbols("alpha y_N x", positive=True)
quad_ = sp.expand((al - 1) * xs * (1 + xs) + xs ** 2 - yN * (1 + xs))               # x (alpha - 1 + x/(1+x)) = yN, times (1+x)
xr = (-(al - 1 - yN) + sp.sqrt((al - 1 - yN) ** 2 + 4 * al * yN)) / (2 * al)
root_ok = sp.simplify(quad_.subs(xs, xr)) == 0
lims = {}
for av in (sp.Rational(1, 2), sp.Integer(1), sp.Integer(2)):
    lims[str(av)] = str(sp.limit((av * xr.subs(al, av)) ** 2 / yN, yN, 0, "+"))
floor = sp.simplify(sp.limit(al * xr, yN, 0, "+").subs(al, sp.Rational(1, 2)))
ok_d3 = root_ok and lims == {"1/2": "oo", "1": "1", "2": "0"} and floor == sp.Rational(1, 2)
RES["D3"] = dict(deep_BTFR_limits=lims, floor_at_half=str(floor),
                 meaning="only alpha = 1 gives the deep law (V^4 -> G M a0); alpha < 1: acceleration floor (1 - alpha) a0; alpha > 1: rescaled Newton")
check("X-D3", ok_d3, f"lim g^2/(g_N a0): {lims}; floor at alpha=1/2: {floor} a0", "{1/2: oo, 1: 1, 2: 0}, floor 1/2")

# X-D4 kernel s(k; f0, alpha) from the linearised hold
k_, mu_, f0_, a_s, drho = sp.symbols("k mu f_0 alpha delta_rho", positive=True)
XIk = sp.symbols("Xi_k")
XIsol = sp.solve(sp.Eq(drho, -(-k_ ** 2 * (f0_ - 1) * XIk + mu_ ** 2 * XIk)), XIk)[0]  # 4piG drho = -[div(J_Y grad Xi) + mu^2 Xi], J_Y(0) = f0 - 1
PHk = -drho / k_ ** 2
s_k = sp.simplify((PHk - a_s * XIsol) / PHk)
m1_form = (mu_ ** 2 - f0_ * k_ ** 2) / ((1 - f0_) * k_ ** 2 + mu_ ** 2)
ok_d4 = (sp.simplify(s_k.subs(a_s, 1) - m1_form) == 0 and sp.simplify(sp.diff(m1_form, f0_) + k_ ** 4 / ((1 - f0_) * k_ ** 2 + mu_ ** 2) ** 2) == 0
         and sp.simplify(s_k.subs(a_s, 0)) == 1)
RES["D4"] = dict(s=str(s_k), M1_form=str(m1_form), ds_df0=str(sp.simplify(sp.diff(m1_form, f0_))))
check("X-D4", ok_d4, f"s(k; f0, alpha) = {s_k}; ds/df0 = {sp.simplify(sp.diff(m1_form, f0_))}; s(alpha=0) = {sp.simplify(s_k.subs(a_s, 0))}",
      "M1 form at alpha = 1, ds/df0 = -k^4/(...)^2 < 0, s(alpha=0) = 1")

# X-D5 T3 statics for any J (the khronon dust weight ALPHA: 1 main, 0 MUTATE)
PhiH = sp.Function("Phi_host")(x, y, z); Cc, Mb_, Mt_, gh = sp.symbols("C M_b M_tau g", positive=True)
sig = -Cc * t
XIh = PhiH - sp.diff(sig, t) + sum(sp.diff(sig, v) ** 2 for v in (x, y, z)) / 2
psi_h = PhiH - ALPHA * XIh
gradpsi = [sp.simplify(sp.diff(psi_h, v)) for v in (x, y, z)]
a_unit = (Mb_ * gh + Mt_ * (1 - ALPHA) * gh) / (Mb_ + Mt_)                           # host force per unit dust mass = (1 - ALPHA) g
a_sep = (Mb_ * gh + Mt_ * gh) / (Mb_ + Mt_)                                          # separate geodesic dust (C1b): a = g
ok_d5 = sp.simplify(XIh - PhiH - Cc) == 0 and all(v == 0 for v in gradpsi) and sp.simplify(a_unit - gh * Mb_ / (Mb_ + Mt_)) == 0
RES["D5"] = dict(Xi_host=str(sp.simplify(XIh)), grad_psi_host=[str(v) for v in gradpsi], fall_rate=str(sp.simplify(a_unit)),
                 fall_rate_separate_dust=str(sp.simplify(a_sep)))
check("X-D5", ok_d5, f"Xi_host = {sp.simplify(XIh)}; grad psi_host = {gradpsi}; bound-unit fall rate = {sp.simplify(a_unit)}; separate dust: {sp.simplify(a_sep)}",
      "Xi = Phi + C, grad psi = 0, a = g M_b/(M_b + M_tau) (T3 for any J)")

# X-D6 C1b statics: separate dust sources the law like baryons; zero khronon charge => Xi = 0
r_, Gs, a0s, Php, Md_ = sp.symbols("r G a_0 Phi_p M_d", positive=True)
muX = (Php / a0s) / (1 + Php / a0s)
Mt_sol = (r_ ** 2 * Php - Gs * (Mb_ + Md_)) / Gs                                      # Poisson: r^2 Phi' = G (M_b + M_d + M_tau)
hold = sp.simplify(Gs * Mt_sol - r_ ** 2 * (1 - muX) * Php)                           # hold with Xi = Phi + C, mu_K = 0
law = sp.simplify(r_ ** 2 * muX * Php - Gs * (Mb_ + Md_))
flux_d = sp.simplify(sp.diff(xs * (1 - xs / (1 + xs)), xs))
rr, mk = sp.symbols("r mu_K", positive=True)
lin_modes = [sp.simplify(sp.diff(rr * f_, rr, 2) / rr - mk ** 2 * f_) for f_ in (sp.sinh(mk * rr) / rr, sp.exp(-mk * rr) / rr)]
ok_d6 = sp.simplify(hold - law) == 0 and sp.simplify(flux_d - 1 / (1 + xs) ** 2) == 0 and all(v == 0 for v in lin_modes)
RES["D6"] = dict(static_law=str(law) + " = 0", hold_flux_derivative=str(flux_d), linear_modes_residual=[str(v) for v in lin_modes],
                 meaning="r^2 mu(Phi'/a0) Phi' = G (M_b + M_d): the separate dust enters the law's source (universal, CFG946 O2a-3); the hold flux "
                         "x/(1+x) is strictly increasing and the linear hold operator (lap - mu_K^2) has only sinh(mu r)/r (growing) as a regular "
                         "homogeneous mode, so rho_tau = 0 gives Xi = 0: no khronon charge, no law (C1b at f_d = 1 = GR + mimetic dust)")
check("X-D6", ok_d6, f"hold - law = 0; d/dx[x(1-mu)] = {flux_d}; radial modes residual {lin_modes}", "0; 1/(1+x)^2 > 0; 0, 0")

# X-D7 C3beta
be = sp.symbols("beta", positive=True)
f_bar = sp.simplify(-sp.diff(PhiH - be * XIh, x)); f_dust = sp.simplify(-sp.diff(PhiH - XIh, x))
rel = sp.simplify(f_bar - f_dust); ok_d7 = sp.simplify(rel - (1 - be) * (-sp.diff(PhiH, x))) == 0 and sp.simplify(f_bar.subs(be, 1)) == 0
RES["D7"] = dict(baryon_force=str(f_bar), dust_force=str(f_dust), relative=str(rel))
check("X-D7", ok_d7, f"held host: baryon force {f_bar}, dust force {f_dust}, relative {rel}", "(1 - beta) g_host; 0 at beta = 1")

# X-D8 quadratic K background; X-D10 DBI K
Qs, I0, aa, lam = sp.symbols("Q I_0 a lambda_D", positive=True); zq = sp.symbols("z", real=True)
Kq = mu_ ** 2 * (Qs - 1) ** 2
Qsol = sp.solve(sp.Eq(aa ** 3 * sp.diff(Kq, Qs), I0), Qs)[0]
rho8 = sp.simplify((Qs * sp.diff(Kq, Qs) - Kq).subs(Qs, Qsol))
ok_d8 = sp.simplify(rho8 - (I0 / aa ** 3 + I0 ** 2 / (4 * mu_ ** 2 * aa ** 6))) == 0
RES["D8"] = dict(rho_8piG=str(rho8))
check("X-D8", ok_d8, f"8 pi G rho = {rho8}", "I0/a^3 + I0^2/(4 mu^2 a^6): stiff term ~ I0^2 ~ (1 - f_d)^2")
Kd = (2 * mu_ ** 2 / lam) * (1 - sp.sqrt(1 - lam * zq ** 2))
Kd2 = sp.simplify(sp.diff(Kd, zq, 2))
ok_d10 = (sp.simplify(Kd2 - 2 * mu_ ** 2 * (1 - lam * zq ** 2) ** sp.Rational(-3, 2)) == 0 and sp.diff(Kd, zq).subs(zq, 0) == 0
          and sp.simplify(Kd2.subs(zq, 0) / 2 - mu_ ** 2) == 0)
RES["D10"] = dict(K2=str(Kd2))
check("X-D10", ok_d10, f"DBI K'' = {Kd2}; K'(1) = 0; K''(1)/2 = mu^2", "K'' > 0 on |Q-1| < lambda^-1/2, same static mass")

# X-D9 mimetic dust about Minkowski: L = -lambda (g^{mu nu} d phi d phi + 1), phi = t + e pi, lambda = lb + e dl
e_, lb, om, kk_ = sp.symbols("e lambda_bar omega k", positive=True)
pid, pix, dl = sp.symbols("pi_t pi_x delta_lambda", real=True)
Lm = -(lb + e_ * dl) * (-(1 + e_ * pid) ** 2 + (e_ * pix) ** 2 + 1)
L2 = sp.expand(sp.series(Lm, e_, 0, 3).removeO().coeff(e_, 2))
pmom = sp.diff(L2, pid); Hm = sp.expand(pmom * pid - L2)
H_on = sp.simplify(Hm.subs(pid, 0))
# Fourier system for (pi, dl) ~ exp(-i w t + i k x): constraint (dL2/d dl) and pi EOM
Mx = sp.Matrix([[-2 * sp.I * om, 0], [-2 * lb * om ** 2 + 2 * lb * kk_ ** 2, -2 * sp.I * om]])
det = sp.factor(Mx.det())
T00 = sp.simplify(2 * lb)                                                            # T_mu nu = 2 lambda d phi d phi + g L, L = 0 on shell
ok_d9 = (sp.simplify(L2 - (lb * pid ** 2 - lb * pix ** 2 + 2 * dl * pid)) == 0 and sp.simplify(H_on - lb * pix ** 2) == 0
         and sp.simplify(det + 4 * om ** 2) == 0)
RES["D9"] = dict(L2=str(L2), H_on_constraint=str(H_on), dispersion_det=str(det), rho_bar=str(T00))
check("X-D9", ok_d9, f"L2 = {L2}; H on pi_t = 0: {H_on}; det = {det} (omega = 0 double root); rho_bar = {T00}",
      "constraint pi_t = 0, H = lambda_bar |grad pi|^2 >= 0 for lambda_bar > 0, no gradient term")

# =====================================================================================================  K: reproductions, reads
P("\n=== K: reproductions and record reads ===")
U1J = rd("rebuild_2026_10_22/U1_v3_dust_content/u1_v3_dust_content_results.json")
U1C = os.path.join(RB, "U1_v3_dust_content", "u1_satellites_per_system.csv")
READS["rebuild_2026_10_22/U1_v3_dust_content/u1_satellites_per_system.csv"] = hashlib.sha256(open(U1C, "rb").read()).hexdigest()
ROWS = list(csv.DictReader(open(U1C)))
rng = np.random.default_rng(23)


def boot_med(arr, n=4000):
    arr = np.asarray(arr, float); Nn = len(arr)
    meds = np.array([np.median(arr[rng.integers(0, Nn, Nn)]) for _ in range(n)])
    return float(np.median(arr)), float(np.std(meds))


SAT = {}
k1 = []
for f in FOOTS:
    rr_ = [r for r in ROWS if r["footing"] == f]
    D = {c: np.array([float(r[c]) for r in rr_]) for c in ("Delta_B0", "Delta_B1_MS", "Delta_B1_LIT", "Delta_static")}
    st = {c: boot_med(v) for c, v in D.items()}
    ref = U1J["numbers"]["N5"]["satellites"][f]["stats"]
    k1.append(abs(st["Delta_B0"][0] - ref["B0"][0]) <= 1e-9 and abs(st["Delta_B0"][1] - ref["B0"][1]) <= 0.01)
    SAT[f] = dict(N=len(rr_), stats=st, D=D, ref=ref)
COMA = {}
for f in FOOTS:
    cb = U1J["numbers"]["N5"]["coma"][f]["B0"]
    zz = cb["meanE"] / math.sqrt(cb["se"] ** 2 + cb["sigma_sys"] ** 2)
    k1.append(abs(zz - cb["z_sys"]) <= 1e-6); COMA[f] = dict(meanE=cb["meanE"], se=cb["se"], sigma_sys=cb["sigma_sys"], z_sys=zz)
check("X-K1", all(k1), "; ".join(f"{f}: B0 median {SAT[f]['stats']['Delta_B0'][0]:+.4f} +- {SAT[f]['stats']['Delta_B0'][1]:.4f} "
                                 f"(U1 {SAT[f]['ref']['B0'][0]:+.4f} +- {SAT[f]['ref']['B0'][1]:.4f}, N {SAT[f]['N']}); Coma z_sys {COMA[f]['z_sys']:.4f}"
                                 for f in FOOTS), "median <= 1e-9, sd within 0.01, Coma z_sys <= 1e-6")

# ---- the growth ODE (copy of F3/M1, generalised to three fluids and the kernel s(k, a; f0, alpha))
from classy import Class
C2B = rd("covariant_push_2026_10_22/C2_aest_cosmology/c2b_native_cmb_results.json")["P5"]["lcdm_refit"]
wbA, wcA, thA, lnAA, nsA, tauA = C2B["params"]; hA = C2B["chi2"]["H0"] / 100.0
OmA = (wbA + wcA) / hA ** 2; ObA = wbA / hA ** 2; OcA = OmA - ObA
cl = Class(); cl.set({"omega_b": wbA, "omega_cdm": wcA, "h": hA, "ln10^{10}A_s": lnAA, "n_s": nsA, "tau_reio": tauA, "N_ur": 3.044,
                      "T_cmb": 2.7255, "output": "mPk", "P_k_max_h/Mpc": 60.0, "z_max_pk": 4.0}); cl.compute()
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
KS = np.geomspace(1e-4, 50.0, 1500); PK = np.array([cl.pk_lin(kv * hA, 0.0) for kv in KS]) * hA ** 3
W8 = lambda q: 3 * (np.sin(q) - q * np.cos(q)) / q ** 3


def sig8(T=None):
    Pk = PK if T is None else PK * T ** 2
    return math.sqrt(TRAPZ(Pk * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))


KT = np.geomspace(1e-3, 3.0, 36)
Or_ = 4.18e-5 / hA ** 2; OL_ = 1.0 - OmA - Or_
Ek = lambda a: math.sqrt(OmA * a ** -3 + Or_ * a ** -4 + OL_)


def _dlnE(a, eps_=1e-6):
    return (math.log(Ek(a * math.exp(eps_))) - math.log(Ek(a * math.exp(-eps_)))) / (2 * eps_)


def kern(a, mu_h, f0, alpha):
    if mu_h is None:
        return np.ones(len(KT))
    x2 = (KT / (a * mu_h)) ** 2
    return 1.0 - alpha * x2 / ((1.0 - f0) * x2 + 1.0)


def solve3(mu_h, f0, alpha, fd, a_i):
    """three fluids (b, separate dust d, khronon tau); baryons and d feel all mass; tau feels b, d and s x itself. delta_m(k, a=1)."""
    n = len(KT); Od = fd * OcA; Ot = (1.0 - fd) * OcA

    def rhs(lx, st):
        a = math.exp(lx); E = Ek(a); dens = 1.5 * a ** -3 / E ** 2; dl_ = _dlnE(a)
        db, gb, dd, gd, dt_, gt = (st[i * n:(i + 1) * n] for i in range(6))
        s = kern(a, mu_h, f0, alpha)
        sb = dens * (ObA * db + Od * dd + Ot * dt_); st_ = dens * (ObA * db + Od * dd + Ot * s * dt_)
        return np.concatenate([gb, -(2 + dl_) * gb + sb, gd, -(2 + dl_) * gd + sb, gt, -(2 + dl_) * gt + st_])
    sol = solve_ivp(rhs, [math.log(a_i), 0.0], np.full(6 * n, a_i), method="DOP853", rtol=1e-7, atol=1e-12, t_eval=[0.0])  # A1: endpoint only
    yv = sol.y[:, -1].copy(); del sol; relieve()
    return (ObA * yv[:n] + Od * yv[2 * n:3 * n] + Ot * yv[4 * n:5 * n]) / OmA


def solve2(mu_h, f0, alpha, a_i):
    """F3/M1's two-fluid form, kept separately (X-K2 compares it with solve3 at f_d = 0)."""
    n = len(KT)

    def rhs(lx, st):
        a = math.exp(lx); E = Ek(a); dens = 1.5 * a ** -3 / E ** 2; dl_ = _dlnE(a)
        db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
        s = kern(a, mu_h, f0, alpha)
        return np.concatenate([gb, -(2 + dl_) * gb + dens * (ObA * db + OcA * dk), gk, -(2 + dl_) * gk + dens * (ObA * db + OcA * dk * s)])
    sol = solve_ivp(rhs, [math.log(a_i), 0.0], np.full(4 * n, a_i), method="DOP853", rtol=1e-7, atol=1e-12, t_eval=[0.0])  # A1: endpoint only
    yv = sol.y[:, -1].copy(); del sol; relieve(); return (ObA * yv[:n] + OcA * yv[2 * n:3 * n]) / OmA


REF = {}


def Rsig(mu_h, f0=0.0, alpha=ALPHA, fd=0.0, a_i=1e-3, two=False):
    if a_i not in REF:
        REF[a_i] = solve2(None, 0.0, 1.0, a_i)
    T = (solve2(mu_h, f0, alpha, a_i) if two else solve3(mu_h, f0, alpha, fd, a_i)) / REF[a_i]
    Tf = np.interp(np.log(KS), np.log(KT), T, left=T[0], right=T[-1])
    return sig8(Tf) / sig8()


M1J = rd("rebuild_2026_10_22/M1_trilemma/m1_trilemma_results.json")
MU_CAP = 10.0 / hA                                                     # h/Mpc (mu_K^-1 = 100 kpc physical)
r_f0 = Rsig(MU_CAP, 0.0, two=True); r_f1 = Rsig(MU_CAP, 1.0, two=True)
r3_0 = Rsig(MU_CAP, 0.0, fd=0.0); r3_1 = Rsig(MU_CAP, 0.0, fd=1.0)
m1r = M1J["R1b_iii"]["ratios"]
ok_k2 = (abs(r_f0 / m1r["f0=0|ai=0.001"] - 1) <= 1e-3 and abs(r_f1 / m1r["f0=1|ai=0.001"] - 1) <= 1e-3
         and abs(r3_0 - r_f0) <= 1e-6 and abs(r3_1 - 1) <= 1e-6)
RES["K2"] = dict(mu_cap_hMpc=MU_CAP, h=hA, Om=OmA, R_f0_0=r_f0, R_f0_1=r_f1, M1_f0_0=m1r["f0=0|ai=0.001"], M1_f0_1=m1r["f0=1|ai=0.001"],
                 three_fluid_fd0=r3_0, three_fluid_fd1=r3_1, sigma8_dust=sig8())
check("X-K2", ok_k2, f"mu {MU_CAP:.5f} h/Mpc, a_i 1e-3: f0=0 {r_f0:.5f} (M1 {m1r['f0=0|ai=0.001']:.5f}), f0=1 {r_f1:.5f} (M1 {m1r['f0=1|ai=0.001']:.5f}); "
      f"3-fluid f_d=0 {r3_0:.6f}, f_d=1 {r3_1:.6f}", "<= 1e-3 rel; 3-fluid = 2-fluid <= 1e-6; f_d = 1 -> 1")

# ---- CFG946 reproduction (NGC 3198, D-F, universal) -- its constants
G_SI, KPC946, MSUN946, PC946 = 6.67430e-11, 3.0856775814913673e19, 1.98847e30, 3.0856775814913673e16
H0_946 = 67.4e3 / (1e6 * PC946); RHOC_946 = 3 * H0_946 ** 2 / (8 * math.pi * G_SI)
OB946 = 0.0493; OC946 = 5.364 * OB946; OM946 = OB946 + OC946; RHOM946 = OM946 * RHOC_946; DTA = 5.55


def r_ta(Mb_kg):
    return (3 * (OM946 / OB946) * Mb_kg / (4 * math.pi * DTA * RHOM946)) ** (1.0 / 3.0)


def law_g(gN, a0):
    gN = np.asarray(gN, float); return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


C946 = rd("campaign_fresh_gravity/CFG946_option2_phantom_not_cold/cfg946_results.json")
_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
READS["real_research/data/sparc_data/NGC3198_rotmod.dat"] = hashlib.sha256(open(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), "rb").read()).hexdigest()
R_N = _d[:, 0] * KPC946
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3) + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MB_N = GN_N[-1] * R_N[-1] ** 2 / G_SI; RTA_N = r_ta(MB_N)
gbt = G_SI * MB_N / RTA_N ** 2; gdt = G_SI * 5.364 * MB_N / RTA_N ** 2
k3 = []; BT = {}
for f in FOOTS:
    a0 = A0[f]; mine = (RTA_N * law_g(gbt + gdt, a0)) ** 2 / (G_SI * MB_N * a0); rec = C946["a_O2a"][f]["btfr_rta"]["a3_DFDU"]
    BT[f] = dict(mine=float(mine), record=rec, law=float((RTA_N * law_g(gbt, a0)) ** 2 / (G_SI * MB_N * a0)))
    k3.append(abs(mine / rec - 1) <= 1e-3)
gq = sp.symbols("g_N", positive=True)
deep = sp.limit((((1 + sp.Rational(5364, 1000)) * gq + sp.sqrt(((1 + sp.Rational(5364, 1000)) * gq) ** 2 + 4 * (1 + sp.Rational(5364, 1000)) * gq)) / 2) ** 2 / gq, gq, 0, "+")
k3.append(deep == sp.Rational(6364, 1000))
check("X-K3", all(k3), f"NGC 3198 M_b {MB_N / MSUN946:.3e} Msun, r_ta {RTA_N / KPC946:.1f} kpc; universal D-F BTFR at r_ta: " +
      "; ".join(f"{f} {BT[f]['mine']:.5f} (CFG946 {BT[f]['record']:.5f})" for f in FOOTS) + f"; deep limit {deep}", "<= 1e-3 rel; 6.364")

# ---- P4 SPARC reproduction (law, per-galaxy Upsilon)
P4J = rd("rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_v3_galaxy_tiles_results.json")
KPC_S = 3.0857e19; UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
SD = os.path.join(REPO, "real_research", "data", "sparc_data"); GALS = []
for fn in sorted(os.listdir(SD)):
    if not fn.endswith("_rotmod.dat"):
        continue
    try:
        dd = np.genfromtxt(os.path.join(SD, fn), comments="#")
    except Exception:
        continue
    if dd.ndim != 2 or dd.shape[1] < 6:
        continue
    q = dict(name=fn.replace("_rotmod.dat", ""), R=dd[:, 0], Vobs=dd[:, 1], eV=dd[:, 2], Vgas=dd[:, 3], Vdisk=dd[:, 4], Vbul=dd[:, 5])
    Rm = q["R"] * KPC_S
    VB2 = np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None] ** 2 + UPS[None, :] * q["Vdisk"][:, None] ** 2 + 1.4 * UPS[None, :] * q["Vbul"][:, None] ** 2
    GB = VB2 * 1e6 / Rm[:, None]; GO = ((q["Vobs"] * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
    OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (q["Vobs"] > 0)[:, None]
    Wt = 1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None)) ** 2
    Mb = np.maximum(VB2[-1, :], 0.0) * 1e6 * Rm[-1] / G_SI                         # M_b(Upsilon) from the last point (CFG946 style)
    rta = np.array([r_ta(m) if m > 0 else 1.0 for m in Mb])
    q.update(Rm=Rm, GB=GB, GO=GO, OK=OK, Wt=Wt, Mb=Mb, rta=rta); GALS.append(q)
READS["real_research/data/sparc_data/*_rotmod.dat"] = f"{len(GALS)} files read"


def nu1(yv):
    yv = np.maximum(np.asarray(yv, float), 1e-300); return 0.5 + np.sqrt(0.25 + 1.0 / yv)


def sparc_stats(a0, fd):
    wr2 = wsum = 0.0; U = []
    for q in GALS:
        gd = G_SI * fd * 5.364 * q["Mb"][None, :] * np.minimum(q["Rm"][:, None] / q["rta"][None, :], 1.0) / q["Rm"][:, None] ** 2
        GBt = q["GB"] + gd
        lgp = np.log10(np.where(q["GB"] > 0, nu1(np.maximum(GBt, 1e-300) / a0) * np.maximum(GBt, 1e-300), 1e-300))
        r = np.where(q["OK"], np.log10(np.where(q["OK"], q["GO"], 1.0)) - lgp, 0.0)
        Wm = np.where(q["OK"], q["Wt"][:, None], 0.0)
        mse = (Wm * r * r).sum(0) / np.maximum(Wm.sum(0), 1e-300); i = int(np.argmin(mse))
        wr2 += float((Wm[:, i] * r[:, i] ** 2).sum()); wsum += float(Wm[:, i].sum()); U.append(UPS[i])
    return dict(rms=math.sqrt(wr2 / wsum), U_median=float(np.median(U)), N=len(GALS))


LAWSP = {f: sparc_stats(A0[f], 0.0) for f in FOOTS}
k4 = [abs(LAWSP[f]["rms"] - P4J["tiles"]["T1"]["footings"][f]["iso_perUps"]["rms"]) <= 1e-4
      and LAWSP[f]["U_median"] == P4J["tiles"]["T1"]["footings"][f]["iso_perUps"]["U_median"] for f in FOOTS]
check("X-K4", all(k4), "; ".join(f"{f}: rms {LAWSP[f]['rms']:.5f} U {LAWSP[f]['U_median']:.2f} (P4 {P4J['tiles']['T1']['footings'][f]['iso_perUps']['rms']:.5f} "
                                 f"{P4J['tiles']['T1']['footings'][f]['iso_perUps']['U_median']:.2f}), N {LAWSP[f]['N']}" for f in FOOTS), "|drms| <= 1e-4, same U median")

# ---- record reads
S4J = rd("rebuild_2026_10_22/S4_v3_muK_clusters/s4_v3_muk_clusters_results.json")
F1J = rd("rebuild_2026_10_22/F1_cluster_cores/f1_cluster_cores_results.json")
Q6J = rd("rebuild_2026_10_22/Q6_v3_class/q6_native_results.json")
Q7J = rd("rebuild_2026_10_22/Q7_bs25_cosmology/q7_native_results.json")
H1J = rd("rebuild_2026_10_22/H1_aest_F/h1_aest_f_results.json")
H2J = rd("rebuild_2026_10_22/H2_aest_clusters/h2_aest_clusters_results.json")
C5J = rd("covariant_push_2026_10_22/C5_health/c5_health_results.json")
C5R = rd("covariant_push_2026_10_22/C5_health/README.md")
U1R = rd("rebuild_2026_10_22/U1_v3_dust_content/README.md")
NFW1 = F1J["addendum_L187"]["ADD h0672 cold c*=0.40 u=1 sourced"]; NFW4 = F1J["addendum_L187"]["ADD h0672 cold c*=0.40 u=0.443 (DS_FINAL) sourced"]
F1B0 = F1J["rows"]["C5b data boost"]
H1K2 = [c for c in H1J["checks"] if c["id"] == "K2"][0]
reads_ok = (S4J["verdict_A1"] == "CANNOT" and S4J["knob_passes"] == [] and S4J["single_cells_passing"] == []
            and all(k_ in F1J["dust"][f] for f in FOOTS for k_ in ("f_needed", "A_needed", "A_cosmic_5364"))
            and "mu_K_BBN_hMpc" in Q6J["stepB"] and all(Q7J["stepB"]["rows"][s]["reading"] == "BBN-VIABLE" for s in ("P1", "P2"))
            and H1J["verdict"] == "NONE IN THE FAMILY" and H1K2["pass"] and H2J["verdict_A1"] == "CANNOT"
            and "CONDITIONALLY HEALTHY" in C5R and all(M1J["R1c"][f]["health_grid_pass"] for f in FOOTS) and "CRISP FINDING" in U1R
            and all(f"{m}|{f}|0.0" in S4J["galaxy"] for m in ("0.015637", "0.03", "0.1", "10.0") for f in FOOTS))
check("X-K5", reads_ok, f"{len(READS)} record files hashed; S4 {S4J['verdict_A1']}, H2 {H2J['verdict_A1']}, H1 {H1J['verdict']}, "
      f"Q6 mu_K,BBN {Q6J['stepB']['mu_K_BBN_hMpc']:.4g} h/Mpc, Q7 P1/P2 {Q7J['stepB']['rows']['P1']['reading']}/{Q7J['stepB']['rows']['P2']['reading']}",
      "all quoted values found")
RES["reads_sha256"] = READS

# =====================================================================================================  G: grades
P("\n=== G: grades ===")
ORDER = {"PASS": 0, "UNDECIDED": 1, "FAIL": 2}


def worst(*v):
    return max(v, key=lambda s: ORDER[s])


def foot_combine(d):                      # PASS iff both, FAIL iff both, else COND -> UNDECIDED
    v = list(d.values())
    return "PASS" if all(s == "PASS" for s in v) else ("FAIL" if all(s == "FAIL" for s in v) else "UNDECIDED")


G = {}
# ---------- (c) growth numbers first (C1b's f_c is needed by (a), (b), (d))
MU_SET = {"BS24_own_0.015637": 0.015637 / hA, "S4_guard_edge_0.03": 0.03 / hA, "cap_10": MU_CAP,
          "DBI_P1_4.484": 4.484304932735426 / hA, "DBI_P2_0.04484": 0.04484304932735426 / hA}
RC = {}
for lab, mh in MU_SET.items():
    RC[lab] = dict(C0_ai1e3=Rsig(mh, 0.0), C0_ai1e4=Rsig(mh, 0.0, a_i=1e-4), C2_ai1e3=Rsig(mh, 1.0), C2_ai1e4=Rsig(mh, 1.0, a_i=1e-4))
    P(f"  R = sigma8/sigma8_dust at mu_K {lab} ({mh:.5g} h/Mpc): C0 {RC[lab]['C0_ai1e3']:.4f} (a_i 1e-4: {RC[lab]['C0_ai1e4']:.4f}); "
      f"C2 {RC[lab]['C2_ai1e3']:.4f} ({RC[lab]['C2_ai1e4']:.4f})")


def fc_of(mh, a_i):
    fn = lambda fd: Rsig(mh, 0.0, fd=fd, a_i=a_i) - 0.95
    lo, hi = fn(0.0), fn(1.0)
    if lo >= 0:
        return 0.0
    if hi < 0:
        return float("nan")
    return float(brentq(fn, 0.0, 1.0, xtol=1e-5))


FC = {}
for lab in ("cap_10", "S4_guard_edge_0.03", "DBI_P1_4.484", "DBI_P2_0.04484"):
    FC[lab] = dict(ai1e3=fc_of(MU_SET[lab], 1e-3), ai1e4=fc_of(MU_SET[lab], 1e-4))
    P(f"  C1b f_c (R = 0.95) at {lab}: a_i 1e-3 {FC[lab]['ai1e3']:.4f}; a_i 1e-4 {FC[lab]['ai1e4']:.4f}")
RES["growth"] = dict(R=RC, f_c=FC, Q6_boltzmann_cap=0.073, Q7_RB={k_: Q7J["fixed"][k_]["R_B"] for k_ in ("P1", "P2", "C1", "C30")},
                     note="ODE from a_i = 1e-3 is F3's optimistic start (upper bound on R); Boltzmann numbers are lower (Q6, Q7)")
fc = FC["cap_10"]["ai1e3"]

# ---------- (a) hosted systems
A = {}
for f in FOOTS:
    st = SAT[f]["stats"]
    br = {b: st[c] for b, c in (("B0", "Delta_B0"), ("B1_MS", "Delta_B1_MS"), ("B1_LIT", "Delta_B1_LIT"))}
    struct = all(v[0] / v[1] >= 3 for v in br.values())
    A[f] = dict(branches={b: list(v) for b, v in br.items()}, khronon_class=("STRUCTURAL" if struct else ("NATIVE" if abs(br["B0"][0]) <= 2 * br["B0"][1] else "TENSION/HIST")),
                coma_zsys=COMA[f]["z_sys"])
    need = 10 ** SAT[f]["D"]["Delta_B0"] - 1
    A[f]["C1b_needed_Md_over_Mb_median"] = float(np.median(need)); A[f]["C1b_needed_over_cosmic"] = float(np.median(need) / 5.364)
    A[f]["C1b_native"] = {}
    for lab, fd in (("f_c", fc), ("1", 1.0)):
        dlt = br["B0"][0] - math.log10(1 + 5.364 * fd); zc = (COMA[f]["meanE"] - math.log(1 + 5.364 * fd)) / math.sqrt(COMA[f]["se"] ** 2 + COMA[f]["sigma_sys"] ** 2)
        A[f]["C1b_native"][lab] = dict(f_d=fd, sat_median=dlt, sat_sd=br["B0"][1], sat_nsd=dlt / br["B0"][1], coma_E=COMA[f]["meanE"] - math.log(1 + 5.364 * fd), coma_zsys=zc)
    A[f]["coma_needed_Md_over_Mb"] = math.exp(COMA[f]["meanE"]) - 1
a_khr = {f: ("FAIL" if (A[f]["khronon_class"] == "STRUCTURAL" and A[f]["coma_zsys"] >= 3) else "UNDECIDED") for f in FOOTS}
G["a"] = dict(C0=foot_combine(a_khr), C2=foot_combine(a_khr), C4="UNDECIDED",
              C1b_fd0=foot_combine(a_khr),
              C1b_fd_pos=foot_combine({f: ("PASS" if (abs(A[f]["C1b_native"]["f_c"]["sat_median"]) <= 2 * A[f]["C1b_native"]["f_c"]["sat_sd"]
                                                       and abs(A[f]["C1b_native"]["f_c"]["coma_zsys"]) <= 2) else "UNDECIDED") for f in FOOTS}))
RES["a"] = A
for f in FOOTS:
    P(f"  (a) {f}: khronon branches B0/B1-MS/B1-LIT " + ", ".join(f"{b} {v[0]:+.3f}+-{v[1]:.3f}" for b, v in A[f]["branches"].items()) +
      f" -> {A[f]['khronon_class']}; Coma z_sys {A[f]['coma_zsys']:.2f}; C1b needs median M_d/M_b(<r12) {A[f]['C1b_needed_Md_over_Mb_median']:.1f} "
      f"({A[f]['C1b_needed_over_cosmic']:.1f} x cosmic); C1b native at f_c {A[f]['C1b_native']['f_c']['sat_median']:+.3f} dex "
      f"({A[f]['C1b_native']['f_c']['sat_nsd']:.1f} sd), Coma z_sys {A[f]['C1b_native']['f_c']['coma_zsys']:.2f}; at f_d = 1 "
      f"{A[f]['C1b_native']['1']['sat_median']:+.3f} dex, Coma z_sys {A[f]['C1b_native']['1']['coma_zsys']:.2f}")

# ---------- (b) clusters
B = {}
for f in FOOTS:
    dd = F1J["dust"][f]; thr_gas = dd["f_needed"] / (5.364 * 1.20)
    out_need = dd["A_needed"]["OUTER"]; out_cos = dd["A_cosmic_5364"]["OUTER"]
    mono_gas = F1B0[f]["OUTER"][0] > out_need[0] > out_cos[0]
    fail_gas = out_need[0] < 1 - 2 * out_need[1] and mono_gas
    o4, o1 = NFW4[f]["OUTER"], NFW1[f]["OUTER"]
    fail_nfw = o4[0] < 1 - 2 * o4[1] and o1[0] < o4[0]
    B[f] = dict(thr_gas=thr_gas, A_OUTER_at_needed=out_need, A_OUTER_cosmic=out_cos, A_OUTER_d0_C5b=F1B0[f]["OUTER"], monotone_gas=mono_gas,
                fail_gas=fail_gas, thr_nfw=0.443, A_OUTER_nfw_0443=o4, A_OUTER_nfw_1=o1, fail_nfw=fail_nfw,
                C1b_fail_on_fc_1=bool(fail_gas and fail_nfw and fc >= max(thr_gas, 0.443)))
    P(f"  (b) {f}: gas-tracing fair-sample threshold f_d >= {thr_gas:.4f} (A_OUTER there {out_need[0]:.3f}+-{out_need[1]:.3f}; cosmic {out_cos[0]:.3f}); "
      f"NFW c*=0.40: f_d >= 0.443 -> A_OUTER <= {o4[0]:.3f}+-{o4[1]:.3f} (u=1: {o1[0]:.3f}); f_c {fc:.4f} -> C1b FAIL on [f_c, 1]: {B[f]['C1b_fail_on_fc_1']}")
G["b"] = dict(C0="FAIL" if S4J["verdict_A1"] == "CANNOT" else "UNDECIDED", C2="FAIL" if S4J["verdict_A1"] == "CANNOT" else "UNDECIDED",
              C4="FAIL" if H2J["verdict_A1"] == "CANNOT" else "UNDECIDED",
              C1b_fd_ge_fc=foot_combine({f: ("FAIL" if B[f]["C1b_fail_on_fc_1"] else "UNDECIDED") for f in FOOTS}))
RES["b"] = dict(per_footing=B, S4_verdict_A1=S4J["verdict_A1"], S4_knob_passes=S4J["knob_passes"], H2_verdict_A1=H2J["verdict_A1"])

# ---------- (c) grades
G["c"] = {}
for lab in MU_SET:
    G["c"][f"C0@{lab}"] = "PASS" if RC[lab]["C0_ai1e3"] >= 0.95 else "FAIL"
    G["c"][f"C2@{lab}"] = "PASS" if RC[lab]["C2_ai1e3"] >= 0.95 else "FAIL"
G["c"]["C4"] = "PASS" if all(v["ii"] for v in H1J["scorecard"].values()) else "UNDECIDED"
G["c"]["C1b_fd_ge_fc"] = "PASS"; G["c"]["C1b_fd_lt_fc"] = "FAIL"

# ---------- (d) isolated galaxies
Dd = {}
FD_EVAL = {"f_c": fc, "1": 1.0}
for f in FOOTS:
    a0 = A0[f]; gl = law_g(GN_N, a0); Dd[f] = {}
    for lab, fd in FD_EVAL.items():
        gd = G_SI * fd * 5.364 * MB_N * np.minimum(R_N / RTA_N, 1.0) / R_N ** 2
        g3 = law_g(GN_N + gd, a0); dev = float(np.max(np.abs(g3 / gl - 1)))
        bt = float((RTA_N * law_g(gbt + fd * gdt, a0)) ** 2 / (G_SI * MB_N * a0))
        sp_ = sparc_stats(a0, fd)
        Dd[f][lab] = dict(f_d=fd, ngc3198_maxdev=dev, ngc3198_dex=float(np.max(np.abs(np.log10(g3 / gl)))), btfr_rta=bt, btfr_rta_law=BT[f]["law"],
                          d1=("PASS" if (dev < 1e-6 and abs(bt - BT[f]["law"]) < 1e-6) else "FAIL"), sparc=sp_)
U_EDGE = {f: min(0.50, LAWSP[f]["U_median"]) for f in FOOTS}


def line_d2(fd):
    out = {}
    for f in FOOTS:
        s_ = sparc_stats(A0[f], fd); out[f] = bool(s_["rms"] <= 0.110 and U_EDGE[f] <= s_["U_median"] <= 0.80)
    return out


d2_law = line_d2(0.0)
if all(line_d2(1.0).values()):
    fdmax = 1.0
elif not all(d2_law.values()):
    fdmax = float("nan")
else:
    lo, hi = 0.0, 1.0
    for _ in range(20):
        md = 0.5 * (lo + hi)
        (lo, hi) = (md, hi) if all(line_d2(md).values()) else (lo, md)
    fdmax = lo
for f in FOOTS:
    for lab in FD_EVAL:
        s_ = Dd[f][lab]["sparc"]; Dd[f][lab]["d2"] = "PASS" if (s_["rms"] <= 0.110 and U_EDGE[f] <= s_["U_median"] <= 0.80) else "FAIL"
    P(f"  (d) {f}: law SPARC rms {LAWSP[f]['rms']:.4f} U {LAWSP[f]['U_median']:.2f} (edge {U_EDGE[f]:.2f}); C1b at f_c {fc:.4f}: NGC 3198 max dev "
      f"{Dd[f]['f_c']['ngc3198_maxdev']:.3f} ({Dd[f]['f_c']['ngc3198_dex']:.3f} dex), BTFR(r_ta) {Dd[f]['f_c']['btfr_rta']:.3f} vs law {BT[f]['law']:.4f}, "
      f"SPARC rms {Dd[f]['f_c']['sparc']['rms']:.4f} U {Dd[f]['f_c']['sparc']['U_median']:.2f} -> d1 {Dd[f]['f_c']['d1']}, d2 {Dd[f]['f_c']['d2']}; "
      f"f_d = 1: SPARC rms {Dd[f]['1']['sparc']['rms']:.4f} U {Dd[f]['1']['sparc']['U_median']:.2f}")
P(f"  (d2) largest f_d passing the adapted P4 line on both footings: f_d,max = {fdmax:.4f}")
GUARD = {m: {f: S4J["galaxy"][f"{m}|{f}|0.0"]["guard"] for f in FOOTS} for m in ("0.015637", "0.03", "0.1", "10.0")}
d3 = {m: foot_combine({f: ("PASS" if v else "FAIL") for f, v in GUARD[m].items()}) for m in GUARD}
P(f"  (d3) S4 isolated-lens guard (Delta = 0): " + ", ".join(f"mu_K {m}: {d3[m]}" for m in GUARD))
D2LAW = foot_combine({f: ("PASS" if d2_law[f] else "FAIL") for f in FOOTS})
GE01 = [k_ for k_ in S4J["galaxy"] if k_.endswith("|0.0") and float(k_.split("|")[0]) >= 0.1 and float(k_.split("|")[0]) <= 10.0]
guard_ge01_fail = all(not S4J["galaxy"][k_]["guard"] for k_ in GE01)
G["d"] = dict(C0_mu_le_0p03=worst("PASS", D2LAW, d3["0.03"]), C0_cap=worst("PASS", D2LAW, d3["10.0"]),
              C2_mu_le_0p03=worst("PASS", D2LAW, d3["0.03"]), C2_cap=worst("PASS", D2LAW, d3["10.0"]),
              C1b_fd_pos=foot_combine({f: Dd[f]["f_c"]["d1"] for f in FOOTS}), C4="UNDECIDED",
              DBI_P1="FAIL" if guard_ge01_fail else "UNDECIDED", DBI_P2="UNDECIDED")
RES["d"] = dict(per_footing=Dd, law_sparc=LAWSP, U_edge=U_EDGE, f_d_max_d2=fdmax, S4_guard=GUARD, d3=d3, d2_law=d2_law, S4_guard_all_ge_0p1_fail=guard_ge01_fail,
                d1_C0_C2="PASS by U1 D2/T1 (held dust = the AQUAL phantom; no extra dust)",
                U1_A2_frame="field galaxies KEPT at the BS cap; DEPENDS at BS24's own mu_K (U1 README A2)",
                DBI_P2_note="mu_K = 0.0448 Mpc^-1 lies between S4's grid points 0.03 (guard PASS) and 0.1 (FAIL): UNDECIDED")

# ---------- (e) health + radiation era
muBBN = Q6J["stepB"]["mu_K_BBN_hMpc"]; one_minus_fd_max = 10.0 / Q6J["stepB"]["mu_K_BBN_per_Mpc"]   # physical: cap 10 /Mpc over mu_K,BBN
MPH_N = float(law_g(GN_N[-1], A0["canonical"]) / GN_N[-1] - 1.0)       # NGC 3198 phantom inside its last radius, in M_b (canonical)
supply_short = MPH_N / (one_minus_fd_max * 5.364)                      # phantom / khronon charge of its fair catchment at that f_d
G["e"] = dict(C0_quadratic="FAIL", C2_quadratic="FAIL", C0_DBI="PASS" if ok_d10 else "UNDECIDED", C2_DBI="PASS" if ok_d10 else "UNDECIDED",
              C1b_quadratic_fd_lt=f"FAIL for f_d < 1 - {one_minus_fd_max:.3g}", C1b_quadratic_fd_ge="PASS" if ok_d9 else "UNDECIDED",
              C1b_DBI="PASS" if (ok_d9 and ok_d10) else "UNDECIDED", C4="FAIL" if H1K2["pass"] else "UNDECIDED")
RES["e"] = dict(C5_conditionally_healthy=True, M1_R1c_health={f: M1J["R1c"][f]["health_grid_pass"] for f in FOOTS},
                Q6_mu_K_BBN_hMpc=muBBN, C1b_one_minus_fd_max_at_cap=one_minus_fd_max,
                C1b_khronon_supply_shortfall_NGC3198=supply_short, NGC3198_phantom_over_Mb_canonical=MPH_N, Q7_BBN={s: Q7J["stepB"]["rows"][s]["reading"] for s in ("P1", "P2")},
                H1_T1=H1K2["value"][:160])
P(f"  (e) quadratic K: no radiation era below mu_K,BBN = {muBBN:.4g} h/Mpc (Q6) -> FAIL; C1b needs 1 - f_d <= {one_minus_fd_max:.3g} at the cap "
  f"(then the khronon charge in NGC 3198's catchment is {supply_short:.2g} x short of its phantom); DBI P1/P2 BBN "
  f"{Q7J['stepB']['rows']['P1']['reading']}/{Q7J['stepB']['rows']['P2']['reading']}; AeST: H1 T1 ({H1K2['value'][:60]}...) -> FAIL")

# ---------- the grades table (best point per row) and the verdict
TAB = {}
TAB["C0 [quadratic K]"] = dict(point="any mu_K <= cap (best: (c) at the cap, (d) at mu_K <= 0.03)",
                               a=(G["a"]["C0"], f"B0 {A['canonical']['branches']['B0'][0]:+.2f}/{A['alt']['branches']['B0'][0]:+.2f} dex; Coma z_sys {A['canonical']['coma_zsys']:.1f}", "a.<foot>.branches"),
                               b=(G["b"]["C0"], "S4 A1: CANNOT (0 passing cells)", "b.S4_verdict_A1"),
                               c=(worst(*[G['c'][f'C0@{l}'] for l in ('BS24_own_0.015637', 'S4_guard_edge_0.03', 'cap_10')]), f"best R {RC['cap_10']['C0_ai1e3']:.3f} at the cap (Boltzmann 0.073)", "growth.R.cap_10.C0_ai1e3"),
                               d=(G["d"]["C0_mu_le_0p03"] + " at mu_K <= 0.03; " + G["d"]["C0_cap"] + " at the cap", "d1 theorem; SPARC = law; S4 guard", "d.d3"),
                               e=(G["e"]["C0_quadratic"], f"no radiation era below {muBBN:.3g} h/Mpc", "e.Q6_mu_K_BBN_hMpc"))
TAB["C0 [BS25 DBI, P1/P2]"] = dict(point="published sets (mu^-1 223 kpc / 22.3 Mpc)",
                                   a=(G["a"]["C0"], "as C0 (T3 is K-independent)", "a"), b=(G["b"]["C0"], "S4 statics (K''(1)/2 = mu^2)", "b"),
                                   c=(worst(G['c']['C0@DBI_P1_4.484'], G['c']['C0@DBI_P2_0.04484']), f"ODE {RC['DBI_P1_4.484']['C0_ai1e3']:.3f}/{RC['DBI_P2_0.04484']['C0_ai1e3']:.3f}; Boltzmann (Q7) {Q7J['fixed']['P1']['R_B']:.3f}/{Q7J['fixed']['P2']['R_B']:.3f}", "growth.R.DBI_*"),
                                   d=(f"{G['d']['DBI_P2']} (P2) / {G['d']['DBI_P1']} (P1)", "S4 guard (P2's mu between grid points; P1's mu >= 0.1 fails)", "d.d3"), e=(G["e"]["C0_DBI"], "C5 conditions hold (X-D10); BBN-VIABLE (Q7)", "e.Q7_BBN"))
TAB["C2 [quadratic K]"] = dict(point="J'(0) = 0, x_t -> 0+", a=(G["a"]["C2"], "T3 J-independent (X-D5): as C0", "a"), b=(G["b"]["C2"], "S4 statics (J = J_x above x_t)", "b"),
                               c=(worst(*[G['c'][f'C2@{l}'] for l in ('BS24_own_0.015637', 'S4_guard_edge_0.03', 'cap_10')]), f"best R {RC['cap_10']['C2_ai1e3']:.3f} at the cap", "growth.R.cap_10.C2_ai1e3"),
                               d=(G["d"]["C2_mu_le_0p03"] + " at mu_K <= 0.03; " + G["d"]["C2_cap"] + " at the cap", "as C0", "d.d3"),
                               e=(G["e"]["C2_quadratic"], "M1 R1(c) health PASS (C5 edge flag); no radiation era (Q6)", "e"))
TAB["C2 [BS25 DBI, P1/P2]"] = dict(point="published sets", a=(G["a"]["C2"], "as C0", "a"), b=(G["b"]["C2"], "S4", "b"),
                                   c=(worst(G['c']['C2@DBI_P1_4.484'], G['c']['C2@DBI_P2_0.04484']), f"ODE {RC['DBI_P1_4.484']['C2_ai1e3']:.3f}/{RC['DBI_P2_0.04484']['C2_ai1e3']:.3f}", "growth.R.DBI_*"),
                                   d=(f"{G['d']['DBI_P2']} (P2) / {G['d']['DBI_P1']} (P1)", "S4 guard", "d.d3"), e=(G["e"]["C2_DBI"], "X-D10 + Q7", "e"))
c1b_e_q = "FAIL" if fc < 1 - one_minus_fd_max else "PASS"
TAB["C1b [quadratic K] (CDM under another name for f_d >= f_c)"] = dict(
    point=f"f_d in [f_c = {fc:.3f}, 1] (f_d = 0 is C0; 0 < f_d < f_c fails (c))",
    a=(G["a"]["C1b_fd_pos"], f"needs M_d/M_b(<r12) ~ {A['canonical']['C1b_needed_Md_over_Mb_median']:.0f} ({A['canonical']['C1b_needed_over_cosmic']:.0f} x cosmic); native {A['canonical']['C1b_native']['f_c']['sat_median']:+.2f} dex", "a.<foot>.C1b_native"),
    b=(G["b"]["C1b_fd_ge_fc"], f"fair-sample dust overshoots OUTER (gas-tracing A_OUTER <= {B['canonical']['A_OUTER_at_needed'][0]:.2f}; NFW <= {B['canonical']['A_OUTER_nfw_0443'][0]:.2f})", "b.per_footing"),
    c=(G["c"]["C1b_fd_ge_fc"], f"R >= 0.95 for f_d >= {fc:.3f} (a_i 1e-3; {FC['cap_10']['ai1e4']:.3f} from 1e-4)", "growth.f_c.cap_10"),
    d=(G["d"]["C1b_fd_pos"], f"double count: NGC 3198 {Dd['canonical']['f_c']['ngc3198_dex']:.2f} dex, BTFR(r_ta) {Dd['canonical']['f_c']['btfr_rta']:.2f}; SPARC f_d,max {fdmax:.3f}", "d.per_footing"),
    e=(c1b_e_q + f" unless 1 - f_d <= {one_minus_fd_max:.2g}", f"stiff khronon remainder; supply shortfall {supply_short:.1g}x at that limit", "e.C1b_one_minus_fd_max_at_cap"))
TAB["C1b [BS25 DBI]"] = dict(point=f"f_d in [f_c, 1]", a=(G["a"]["C1b_fd_pos"], "as above", "a"), b=(G["b"]["C1b_fd_ge_fc"], "as above", "b"),
                             c=(G["c"]["C1b_fd_ge_fc"], f"f_c(P1 mu) {FC['DBI_P1_4.484']['ai1e3']:.3f}, f_c(P2 mu) {FC['DBI_P2_0.04484']['ai1e3']:.3f}", "growth.f_c"),
                             d=(G["d"]["C1b_fd_pos"], "as above", "d"), e=(G["e"]["C1b_DBI"], "X-D9 + X-D10 + Q7", "e"))
TAB["C4 AeST cold sector (v4)"] = dict(point="record (cap-n1 + gamma_L)", a=(G["a"]["C4"], "no T3 analogue computed in the record", "-"),
                                       b=(G["b"]["C4"], "H2 A1: CANNOT", "b.H2_verdict_A1"), c=(G["c"]["C4"], "H1 (ii): every member grows", "-"),
                                       d=(G["d"]["C4"], "static law identical; collapsed dust not computed", "-"),
                                       e=(G["e"]["C4"], "H1 T1: the negative-energy mode is the growth mode", "e.H1_T1"))


def first_word(s):
    return s.split()[0] if isinstance(s, str) else s


nfail = {}
for row, d in TAB.items():
    nfail[row] = sum(1 for k_ in "abcde" if first_word(d[k_][0]) == "FAIL")
    P(f"  {row:58s} | " + " | ".join(f"({k_}) {d[k_][0]}" for k_ in "abcde"))
# every-point logic (frozen §4): a row fails everywhere if a parameter-independent test FAILS, or (C1b) every f_d interval has a FAIL
fails_everywhere = {}
for row, d in TAB.items():
    if row.startswith("C1b"):
        # f_d = 0 is C0 (fails (a)); 0 < f_d < f_c fails (c); f_d >= f_c fails (d1) exactly (any dust in galaxies)
        fails_everywhere[row] = (G["a"]["C1b_fd0"] == "FAIL") and (fc > 0) and (G["d"]["C1b_fd_pos"] == "FAIL")
    else:
        fails_everywhere[row] = any(first_word(d[k_][0]) == "FAIL" for k_ in "ab") or first_word(d["e"][0]) == "FAIL" or first_word(d["c"][0]) == "FAIL"
any_pass_all = any(all(first_word(d[k_][0]) == "PASS" for k_ in "abcde") for d in TAB.values())
any_no_fail = any(not fails_everywhere[r] for r in TAB)
if any_pass_all:
    VERDICT = "A CANDIDATE PASSES ALL FIVE"
elif any_no_fail:
    VERDICT = "BEST CANDIDATE FAILS " + ", ".join(r for r in TAB if not fails_everywhere[r])
else:
    VERDICT = "NO-GO FOR THE STATED CLASS"
best = min(nfail.values()); BEST = [r for r in TAB if nfail[r] == best]
RES["grades"] = {r: {k_: dict(grade=d[k_][0], number=d[k_][1], key=d[k_][2]) for k_ in "abcde"} | {"point": d["point"], "n_FAIL": nfail[r],
                                                                                                        "fails_at_every_point": fails_everywhere[r]} for r, d in TAB.items()}
RES["excluded"] = {"C1a": "no action: a_mu = D_mu ln N (X-D1); alpha = 0 removes the law; U1's MUTATE hybrid has Xi in no force (Newton + geodesic dust)",
                   "C3alpha": "no action (alpha = 1 kinematic) and the deep law forces alpha = 1 (X-D3): collapses to C0",
                   "C3f": "needs a number; bracketed by C0 (f0 = 0) and C2 (f0 = 1) since ds/df0 < 0 (X-D4)",
                   "C3beta": "needs a number; beta = 0 is C0; relative host acceleration (1 - beta) g, no baryon gravity in held hosts at beta = 1 (X-D7)",
                   "C5": "K-shapes, not couplings; each needs a fitted/postulated number (BS25 DBI used only at its published sets as K sub-rows)"}
RES["verdict"] = VERDICT; RES["best_rows"] = BEST; RES["best_n_FAIL"] = best
ok_g = all(isinstance(d[k_][0], str) and d[k_][0] for d in TAB.values() for k_ in "abcde")
check("X-G", ok_g, f"{len(TAB)} rows x 5 tests graded; verdict: {VERDICT}; fewest FAILs ({best}): {BEST}", "every cell graded")
P(f"\nVERDICT: {VERDICT}")
P(f"  best rows ({best} FAIL each): " + "; ".join(f"{r}: fails " + ", ".join(k_ for k_ in 'abcde' if first_word(TAB[r][k_][0]) == 'FAIL') for r in BEST))
P("  Stop rule (frozen): no follow-up scans, no new candidates.")

RES["runtime_s"] = time.time() - T0; RES["peak_rss_GB"] = rss_gb()
check("X-R", RES["peak_rss_GB"] < 1.0, f"peak RSS {RES['peak_rss_GB']:.3f} GB, {RES['runtime_s']:.0f} s", "< 1 GB")
RES["checks"] = CHK; npass = sum(v["ok"] for v in CHK.values())
P(f"\nchecks {npass}/{len(CHK)} PASS" + (" (MUTATE: X-D5 and X-K2 must FAIL)" if MUT else ""))
with open(os.path.join(HERE, f"x6_dust_coupling{SUF}.out"), "w") as fo:
    fo.write("\n".join(OUT) + "\n")
with open(os.path.join(HERE, f"x6_dust_coupling_results{SUF}.json"), "w") as fo:
    json.dump(RES, fo, indent=1, default=lambda o: (o.tolist() if hasattr(o, "tolist") else str(o)))
sys.exit(0 if npass == len(CHK) else 1)
