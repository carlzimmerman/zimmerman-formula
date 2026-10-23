#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
U1_v3_dust_content -- what range of dust content and total gravity v3's own equations allow (frozen: FROZEN_CRITERIA.md).

v3's PN system (L1 FROZEN_CRITERIA s1; BS24 via BSK1):
    Xi = Phi - sigma_t + |grad sigma|^2/2 ;  4 pi G rho_tau = -[div(J_Y grad Xi) + muK^2 Xi],  J_Y = mu(x) - 1,  mu = x/(1+x),
    x = |grad Xi|/a0 ;  lap Phi = 4 pi G (rho_b + rho_tau) ;  dust: Dv/Dt = -grad psi, psi = Phi - Xi ;  baryons: -grad Phi.
LIT = literal single-stream khronon; MS = posited multi-stream particle dust (rho_tau >= 0).

Run (repository root):  OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/U1_v3_dust_content/u1_v3_dust_content.py
Mutate:                 U1_MUTATE=1 ...   (dust feels -grad Phi: no hold force on dust; D4, D7, N1 must FAIL)
"""
import os, sys, json, math, time, csv, resource, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1")
if sys.platform == "darwin" and os.environ.get("MallocMediumZone") != "0":
    # macOS's medium malloc zone keeps freed 0.1-8 MB FFT buffers resident (N4 reached ~1.1 GB RSS with < 0.1 GB live);
    # disabling it keeps the run under the 1 GB rule. Deterministic re-exec, no effect on any number.
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, MallocMediumZone="0"))
import numpy as np
import sympy as sp
from scipy.special import erf, ellipk, ellipe
warnings.filterwarnings("ignore", category=RuntimeWarning)
np.seterr(all="ignore")

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RB = os.path.join(REPO, "rebuild_2026_10_22")
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("U1_MUTATE", "0") == "1"
SFX = "_MUTATE" if MUT else ""
OUT, CHK = [], {}
RES = dict(lane="U1_v3_dust_content", mutate=MUT, frozen="edb372c22d", numbers={})


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


def check(name, ok, val, thr, note=""):
    CHK[name] = dict(ok=bool(ok), value=str(val), threshold=str(thr), note=note)
    P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}  {note}")


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)


G, MSUN, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
R12 = 4.0 / 3.0
HB = 0.6856                                             # F3/L1 model-B h for the BS cap
MUK = {"cap_14.8h/Mpc": 14.8 * HB / (1e3 * KPC), "BS24_own_0.015637/Mpc": 0.015637 / (1e3 * KPC)}   # 1/m

P("=" * 116)
P("U1_v3_dust_content: v3's own dust range (bounds, velocity, consequences)" + ("   *** MUTATE: dust feels -grad Phi ***" if MUT else ""))
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled; cold energy, no particle")
P("=" * 116)

# =====================================================================================================================
#  PART 1: DERIVATIONS (sympy)
# =====================================================================================================================
P("\n--- D1: the psi equation and the single-stream Bernoulli identity ---")
x, y, z, t = sp.symbols("x y z t", real=True)
a0s, Gs, muK, C = sp.symbols("a_0 G mu_K C", positive=True)
Phi = sp.Function("Phi")(x, y, z, t)
sig = sp.Function("sigma")(x, y, z, t)
Xf = sp.Function("Xi")(x, y, z, t)
Mf = sp.Function("M")                                    # generic interpolating function mu(.)
X3 = (x, y, z)
grad = lambda f: [sp.diff(f, v) for v in X3]
div = lambda V: sum(sp.diff(V[i], X3[i]) for i in range(3))
lap = lambda f: div(grad(f))
nrm = lambda V: sp.sqrt(sum(c ** 2 for c in V))
mu_X = Mf(nrm(grad(Xf)) / a0s)
four_pi_G_rho_tau = -(div([(mu_X - 1) * c for c in grad(Xf)]) + muK ** 2 * Xf)
four_pi_G_rho_b = lap(Phi) - four_pi_G_rho_tau
psi = Phi - Xf
d1a = sp.simplify(sp.expand(lap(psi) - (four_pi_G_rho_b - div([mu_X * c for c in grad(Xf)]) - muK ** 2 * Xf)))
Xi_def = Phi - sp.diff(sig, t) + sum(c ** 2 for c in grad(sig)) / 2
v = [-c for c in grad(sig)]
Dv = [sp.diff(v[i], t) + sum(v[j] * sp.diff(v[i], X3[j]) for j in range(3)) for i in range(3)]
d1b = [sp.simplify(Dv[i] + sp.diff(Phi - Xi_def, X3[i])) for i in range(3)]
ok_d1 = d1a == 0 and all(r == 0 for r in d1b)
check("D1", ok_d1, f"psi-eq residual {d1a}; Bernoulli residuals {d1b}", "all 0",
      "lap psi = 4piG rho_b - div[mu grad Xi] - muK^2 Xi ; Dv/Dt = -grad(Phi - Xi) for v = -grad sigma")

P("\n--- D2: literal statics (uniqueness at muK = 0; zero-point freedom at muK != 0) ---")
xs = sp.symbols("x", positive=True)
mu = xs / (1 + xs)
Xi_static = Phi + C                                     # sigma = -C t
rt_static = -(div([(Mf(nrm(grad(Xi_static)) / a0s) - 1) * c for c in grad(Xi_static)]) + muK ** 2 * Xi_static)
eq35 = div([Mf(nrm(grad(Phi)) / a0s) * c for c in grad(Phi)]) + muK ** 2 * (Phi + C)
d2i = sp.simplify(sp.expand((lap(Phi) - rt_static) - eq35))
fl_aq = sp.simplify(sp.diff(xs * mu, xs)); fl_hold = sp.simplify(sp.diff(xs * (1 - mu), xs))
d2ii = bool(sp.simplify(fl_aq - (xs ** 2 + 2 * xs) / (1 + xs) ** 2) == 0 and fl_aq.is_positive and fl_hold.is_positive)
d2iii_a = sp.simplify(sp.expand(rt_static - rt_static.subs(C, 0) + muK ** 2 * C))
r_ = sp.symbols("r", positive=True)
fh = sp.sin(muK * r_) / r_
d2iii_b = sp.simplify(sp.diff(r_ ** 2 * sp.diff(fh, r_), r_) / r_ ** 2 + muK ** 2 * fh)
ok_d2 = d2i == 0 and d2ii and d2iii_a == 0 and d2iii_b == 0
check("D2", ok_d2, f"Eq35 residual {d2i}; d(x mu)/dx = {fl_aq} > 0, d(x(1-mu))/dx = {fl_hold} > 0; "
      f"K-dust shift residual {d2iii_a}; Helmholtz mode residual {d2iii_b}", "residuals 0, fluxes increasing",
      "static LIT: Xi = Phi + C => BS24 Eq.35 (unique at muK=0); muK != 0: C shifts uniform K-dust by -muK^2 C/4piG, regular sin(muK r)/r mode")

P("\n--- D3: the hold cap ---")
lim = sp.limit(xs * (1 - mu), xs, sp.oo)
gap = sp.simplify(1 - xs * (1 - mu))
gg, gN = sp.symbols("g g_N", positive=True)
d3_id = sp.simplify((gg - gg * mu.subs(xs, gg)) - gg / (1 + gg))   # a0 = 1: phantom flux = r^2 (g - g_N), g mu(g) = g_N
ok_d3 = lim == 1 and gap.is_positive and d3_id == 0
check("D3", ok_d3, f"lim x(1-mu) = {lim}; 1 - x(1-mu) = {gap} > 0; phantom-flux identity residual {d3_id}", "lim 1, gap > 0, residual 0",
      "G M_tau(V) < a0 |dV|/4pi ; sphere G M_tau(<r) < a0 r^2 ; sheet Sigma_tau < a0/2piG ; spherical g < g_N + a0")

P("\n--- D4: spherical dust force and the sign of the held dust's self-interaction ---")
n_, m_ = sp.symbols("n m", positive=True)
h_ = m_ / (1 - m_)                                       # hold: h/(1+h) = m
g_tot = n_ + m_
psi_p = (g_tot - h_) if not MUT else g_tot               # MUTATE: dust feels -grad Phi
d4_form = sp.simplify(psi_p - (n_ - m_ ** 2 / (1 - m_)))
mph = (-n_ + sp.sqrt(n_ ** 2 + 4 * n_)) / 2
d4_aq = sp.simplify((n_ + mph) ** 2 / (1 + n_ + mph) - n_)
d4_zero = sp.simplify((n_ - mph ** 2 / (1 - mph)))
dself = sp.simplify(sp.diff(psi_p, m_))
mgrid = np.linspace(1e-6, 1 - 1e-6, 20001)
dsel_num = sp.lambdify(m_, dself, "numpy")(mgrid) * np.ones_like(mgrid)
ok_d4 = d4_form == 0 and d4_aq == 0 and d4_zero == 0 and float(np.max(dsel_num)) <= 0
check("D4", ok_d4, f"psi' form residual {d4_form}; AQUAL residual {d4_aq}; psi'(m_ph) {d4_zero}; d(psi')/dm = {dself} (max {np.max(dsel_num):.3e})",
      "residuals 0; d/dm <= 0", "-psi' = -a0[n - m^2/(1-m)]; held dust self-repulsive for m > 0, neutral at m -> 0 (D-T)")

P("\n--- D5: geometry-free virial: W_self >= 0 ---")
p = sp.Function("p")(r_)
Aof = lambda q: 1 / (1 + q)
Lam = lambda q: q - sp.log(1 + q)
lhs = r_ * p * sp.diff(r_ ** 2 * Aof(p) * p, r_)
rhs = sp.diff(r_ ** 3 * Aof(p) * p ** 2 - r_ ** 3 * Lam(p), r_) - r_ ** 2 * Aof(p) * p ** 2 + 3 * r_ ** 2 * Lam(p)
d5_der = sp.simplify(sp.expand(lhs - rhs))
u_ = sp.symbols("u", positive=True)
fu = 3 * (u_ - sp.log(1 + u_)) - u_ ** 2 / (1 + u_) - u_ ** 2 / (2 * (1 + u_) ** 2)
ser0 = sp.series(fu, u_, 0, 6).removeO()
lead_inf = sp.limit(fu / u_, u_, sp.oo)
ug = np.geomspace(1e-8, 1e8, 4000)
fnum = sp.lambdify(u_, fu, "mpmath")
import mpmath
mpmath.mp.dps = 40
fvals = np.array([float(fnum(mpmath.mpf(float(uu)))) for uu in ug])
ok_d5 = d5_der == 0 and float(np.min(fvals)) >= -1e-12 and sp.Poly(ser0, u_).coeffs()[-1] > 0 and lead_inf == 2
check("D5", ok_d5, f"Derrick residual {d5_der}; f(u) series {sp.expand(ser0)}; f/u -> {lead_inf}; min f on grid {np.min(fvals):.3e}",
      "residual 0; min f >= -1e-12", "W_self = W_N + (1/4piG) Int[3 Lambda - A y^2] >= (a0^2/4piG) Int f(u) >= 0 (Thomson)")
RES["numbers"]["D5_min_f"] = float(np.min(fvals))

P("\n--- D6: linear response in a uniform host field ---")
k, mk, f_, rb, rhob, chi, kV = sp.symbols("k mu_k f rhobar rho_b chi kV", positive=True)
c_th = (f_ * k ** 2 - mk ** 2) / ((1 - f_) * k ** 2 + mk ** 2)
psi_lin = lambda drho, c: -4 * sp.pi * Gs * rhob / k ** 2 + 4 * sp.pi * Gs * c * drho / k ** 2
dr_ = sp.symbols("drho")
c0 = c_th.subs(mk, 0)
cold = sp.solve(sp.Eq(psi_lin(dr_, c0), 0), dr_)[0]
d6ii = sp.simplify(cold - rhob * (1 / f_ - 1))
hot = sp.solve(sp.Eq(dr_, -rb * chi * psi_lin(dr_, c0)), dr_)[0]
kD2 = 4 * sp.pi * Gs * c0 * rb * chi
d6iii = sp.simplify(hot - rhob * (1 / f_ - 1) * kD2 / (k ** 2 + kD2))
stream = sp.solve(sp.Eq(dr_, rb * k ** 2 * psi_lin(dr_, c0) / kV ** 2), dr_)[0]
wp2 = 4 * sp.pi * Gs * rb * f_ / (1 - f_)
d6iv = sp.simplify(stream - 4 * sp.pi * Gs * rb * rhob / (wp2 - kV ** 2))
fth, rho0, ksym = sp.symbols("f_theta rho_0 kk", positive=True)
bsk1 = 4 * sp.pi * Gs * rho0 * (ksym ** 2 * fth - mk ** 2) / (ksym ** 2 * (1 - fth) + mk ** 2)
d6iv_b = sp.simplify(sp.limit(bsk1, ksym, sp.oo) - 4 * sp.pi * Gs * rho0 * fth / (1 - fth))
xe_g = np.geomspace(1e-4, 1e3, 400)
fth_max = (xe_g / (1 + xe_g)) * (1 + 1 / (1 + xe_g))
fth_min = xe_g / (1 + xe_g)
ok_fgrid = bool(np.all(fth_max < 1) and np.all(fth_min > 0))
ok_d6 = d6ii == 0 and d6iii == 0 and d6iv == 0 and d6iv_b == 0 and ok_fgrid
check("D6", ok_d6, f"cold {d6ii}; hot {d6iii}; stream {d6iv}; BSK1 M4 k>>mu {d6iv_b}; 0<f_theta<1 on x_e grid {ok_fgrid} (max f {fth_max.max():.6f})",
      "residuals 0, f in (0,1)", "c_theta >= 0 for k^2 >= muK^2/f; cold = EFE phantom; hot isotropic = phantom x kD^2/(k^2+kD^2); stream pole at omega_p")

P("\n--- D7 (T3): held dust is weightless in a static host ---")
Phi_h = sp.Function("Phi_h")(x, y, z)
psi_host = sp.diff(Phi_h - (Phi_h + C), x)              # static host: Xi_host = Phi_host + C
# (b) stress tensor of a linear medium: point charge q (source of Xi) in a uniform field E z; force on the enclosed charge
th, ph_, Rs, q_, E_ = sp.symbols("theta phi R q E", positive=True)
xx, yy, zz = sp.symbols("xx yy zz", real=True)
rr_ = sp.sqrt(xx ** 2 + yy ** 2 + zz ** 2)
Xi_c = E_ * zz - q_ / rr_                               # lap(-q/r) = 4 pi q delta  -> hold "charge" q (units 4piG rho = lap Xi)
gXi = [sp.diff(Xi_c, s) for s in (xx, yy, zz)]
T = [[(gXi[i] * gXi[j] - (sp.Rational(1, 2) if i == j else 0) * sum(c ** 2 for c in gXi)) / (4 * sp.pi) for j in range(3)] for i in range(3)]
sub = {xx: Rs * sp.sin(th) * sp.cos(ph_), yy: Rs * sp.sin(th) * sp.sin(ph_), zz: Rs * sp.cos(th)}
nvec = [sp.sin(th) * sp.cos(ph_), sp.sin(th) * sp.sin(ph_), sp.cos(th)]
Fz_int = sp.simplify(sum(T[2][j].subs(sub) * nvec[j] for j in range(3)) * Rs ** 2 * sp.sin(th))
Fz = sp.simplify(sp.integrate(sp.integrate(Fz_int, (ph_, 0, 2 * sp.pi)), (th, 0, sp.pi)))
d7b = sp.simplify(Fz - q_ * E_)                         # force on the charge = q grad(Xi_ext) = q E (z)
Mb_, Mt_, gh = sp.symbols("M_b M_tau g", positive=True)
a_, F_ = sp.symbols("a F", real=True)              # real, not positive: the MUTATE solution has F = 0
host_on_dust = 0 if not MUT else Mt_ * gh               # MUTATE: dust feels the host's Phi
sol = sp.solve([sp.Eq(Mb_ * a_, Mb_ * gh - F_), sp.Eq(Mt_ * a_, F_ + host_on_dust)], [a_, F_], dict=True)[0]
d7c = sp.simplify(sol[a_] - gh * Mb_ / (Mb_ + Mt_))
ok_d7 = psi_host == 0 and d7b == 0 and d7c == 0
check("D7", ok_d7, f"grad psi_host = {psi_host}; stress-tensor force - qE = {d7b}; a_CM - g Mb/(Mb+Mtau) = {d7c}", "all 0",
      "T3: host exerts no force on held dust; a bound unit falls at a = g M_b/(M_b + M_tau)")

# =====================================================================================================================
#  PART 2: shared helpers (units a0 = 1, a = system scale; q = G M(<r)/(a0 a^2))
# =====================================================================================================================
def law(gNv):
    gNv = np.asarray(gNv, float)
    return 0.5 * (gNv + np.sqrt(gNv * gNv + 4.0 * gNv))


def mph_n(n):
    n = np.asarray(n, float)
    return 0.5 * (-n + np.sqrt(n * n + 4.0 * n))


def nu_e(yv):
    return 1.0 / (-np.expm1(-np.sqrt(np.asarray(yv, float))))


def qb_fun(prof, yv):
    if prof == "plummer":
        return lambda r: yv * r ** 3 / (1 + r * r) ** 1.5
    if prof == "uniform":
        return lambda r: yv * np.minimum(r, 1.0) ** 3
    raise ValueError(prof)


def qph_fun(prof, yv):
    qb = qb_fun(prof, yv)
    return lambda r: r * r * mph_n(qb(r) / (r * r))


def rhoph_grid(prof, yv, r):
    """phantom density (units a0/(G a)) on grid r by differentiating q_ph = r^2 m_ph(n)."""
    qp = qph_fun(prof, yv)
    lr = np.log(r); h = 1e-5
    dq = (qp(np.exp(lr + h)) - qp(np.exp(lr - h))) / (2 * h) / r
    return dq / (4 * np.pi * r * r)


# =====================================================================================================================
#  N0: reproduce first
# =====================================================================================================================
P("\n--- N0: reproduce S1 / P4 from the on-disk inputs ---")
S1D = os.path.join(RB, "S1_v3_hosted_small")
SAT = [r for r in csv.DictReader(open(os.path.join(S1D, "s1_per_system.csv")))]
for r in SAT:
    for kk in list(r.keys()):
        if kk not in ("footing", "name", "host"):
            r[kk] = float(r[kk])
COMA = [r for r in csv.DictReader(open(os.path.join(S1D, "s1_coma_per_galaxy.csv")))]
for r in COMA:
    for kk in list(r.keys()):
        if kk not in ("footing", "name"):
            r[kk] = float(r[kk])
d_iso = 0.0
for r in SAT:
    yv = r["y_plummer"]; gNr = yv * R12 / (1 + R12 ** 2) ** 1.5
    lg = math.log10(2 * R12 ** 2 * float(law(gNr)) / yv)
    d_iso = max(d_iso, abs(lg - r["logG_iso0"]))
# P4 K9 from raw inputs
G936, MSUN936, KPC936, PC936 = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
TDG = []
for r in csv.DictReader(open(os.path.join(DATA, "tidal_dwarfs", "lelli2015_tdg.csv"))):
    fv = lambda kk: float(r[kk])
    TDG.append(dict(name=r["object"].replace(" ", ""), V=fv("V_circ_kms"), eV=fv("e_V_circ_kms"), M=fv("M_bar_1e8") * 1e8,
                    eM=fv("e_M_bar_1e8") * 1e8, R=fv("R_out_kpc"), eR=fv("e_R_out_kpc"), LK=fv("host_LK_1e10Lsun") * 1e10, Dp=fv("D_p_kpc")))
DFG = {"DF2": dict(Ms=2.0e8, Re=2.0, D=20.0, obs=(8.5, 2.3, 3.1), pos=(40.4451, -8.4028)),
       "DF4": dict(Ms=1.5e8, Re=1.6, D=20.0, obs=(6.3, 2.5, 1.6), pos=(39.8128, -8.1160))}
src657 = open(os.path.join(CFG, "CFG657_trail_capture_rule", "cfg657_capture.py")).read()
ok_src = all(s in src657 for s in ('"DF2":  dict(Ms=2.0e8', '"DF4":  dict(Ms=1.5e8', 'obs=(8.5, 2.3, 3.1)', 'obs=(6.3, 2.5, 1.6)',
                                    '"NGC1052": (40.2700, -8.2558)', '"NGC1035": (39.8713, -8.1328)'))
HOSTS = {"NGC1052": (40.2700, -8.2558), "NGC1035": (39.8713, -8.1328)}
k9 = {}
for f in FOOTS:
    a0 = A0[f]
    dl = []
    for o in TDG:
        Rm = o["R"] * KPC936; gb = G936 * o["M"] * MSUN936 / Rm ** 2; go = (o["V"] * 1e3) ** 2 / Rm
        dl.append(math.log10(go / (gb * float(nu_e(gb / a0)))))
    k9[f"T|{f}"] = float(np.mean(dl))
    for nm, gg_ in DFG.items():
        r12 = R12 * gg_["Re"] * 1e3 * PC936; gb = G936 * (gg_["Ms"] / 2) * MSUN936 / r12 ** 2
        sl = math.sqrt(r12 * gb * float(nu_e(gb / a0)) / 3) / 1e3
        k9[f"{nm}|{f}"] = 2 * math.log(gg_["obs"][0] / sl)
REF9 = {"T|canonical": -0.6903781917632702, "T|alt": -0.7276095405858052, "DF2|canonical": -1.7090797992538782,
        "DF4|canonical": -2.1700940800879236, "DF2|alt": -1.7973858933111546, "DF4|alt": -2.2578864586814924}
d_k9 = max(abs(k9[kk] - REF9[kk]) for kk in REF9)
med_emb = {f: float(np.median([r["log_gobs_gbar"] - r["logG_emb0"] for r in SAT if r["footing"] == f])) for f in FOOTS}
S1REF = {"canonical": 1.130, "alt": 1.075}
d_emb = max(abs(med_emb[f] - S1REF[f]) for f in FOOTS)
nsat = {f: sum(1 for r in SAT if r["footing"] == f) for f in FOOTS}
check("N0", d_iso <= 1e-3 and d_k9 <= 1e-3 and d_emb <= 0.10 and ok_src and nsat == {"canonical": 45, "alt": 46},
      f"S1 iso law max {d_iso:.1e} dex; P4 K9 max {d_k9:.1e}; S1 EFE central medians {med_emb['canonical']:+.3f}/{med_emb['alt']:+.3f} "
      f"(S1 +1.130/+1.075); N {nsat['canonical']}/{nsat['alt']}; CFG657 constants found {ok_src}",
      "<=1e-3, <=1e-3, <=0.10", "same data as S1/P4")
RES["numbers"]["N0"] = dict(d_iso=d_iso, d_k9=d_k9, med_emb=med_emb, k9=k9)
P(f"   [peak RSS so far {rss_gb():.2f} GB, {time.time() - T0:.0f} s]")

# =====================================================================================================================
#  N1 / N2: self-consistent spherical dust equilibria (vectorised RK4 in s = ln r)
# =====================================================================================================================
def king_shape(W):
    W = np.maximum(np.asarray(W, float), 0.0)
    ex = np.exp(np.minimum(W, 700.0)) * erf(np.sqrt(W)) - np.sqrt(4 * W / np.pi) * (1 + 2 * W / 3)
    ser = (8.0 / (15.0 * math.sqrt(math.pi))) * W ** 2.5 * (1 + 2 * W / 7 + W * W / 21)
    return np.where(W < 1e-3, ser, ex)


def dust_force(nn, mm):
    """psi' (positive = net inward pull on dust), a0 units."""
    if MUT:
        return nn + mm
    return nn - mm * mm / (1.0 - mm)


def solve_equilibria(prof, yv, rho_of, nconf, aniso_beta=None, smin=math.log(1e-4), smax=math.log(1e4), nst=5000, Psi0=None):
    """Integrate dPsi/ds = -r psi'(n, m), dq/ds = 4 pi r^3 rho(r, Psi) for nconf configurations at once.
    Returns dict with status (0 edge, 1 cap, 2 unfinished), the max ratio q/q_ph inside the dust, q at r12, r_edge, excess starts."""
    qb = qb_fun(prof, yv); qp = qph_fun(prof, yv)
    ds = (smax - smin) / nst
    s = smin; r = math.exp(s)
    Psi = Psi0.copy()
    rho0 = rho_of(r, Psi)
    if aniso_beta is None:
        q = 4 * np.pi / 3 * rho0 * r ** 3
    else:
        q = 4 * np.pi * rho0 * r ** 3 / (3 - 2 * aniso_beta)
    status = np.full(nconf, 2, int)
    alive = np.ones(nconf, bool)
    maxratio = np.zeros(nconf); q12 = np.full(nconf, np.nan); redge = np.full(nconf, np.nan); maxgain = np.full(nconf, -np.inf)
    in_exc = np.zeros(nconf, bool); exc_start = [[] for _ in range(nconf)]
    lr12 = math.log(R12)

    def rhs(s_, Ps, qq):
        rr = math.exp(s_)
        nn = qb(rr) / rr ** 2
        mm = np.minimum(qq / rr ** 2, 0.999999)
        rho = rho_of(rr, Ps)
        return -rr * dust_force(nn, mm), 4 * np.pi * rr ** 3 * rho

    for it in range(nst):
        k1a, k1b = rhs(s, Psi, q)
        k2a, k2b = rhs(s + ds / 2, Psi + ds / 2 * k1a, q + ds / 2 * k1b)
        k3a, k3b = rhs(s + ds / 2, Psi + ds / 2 * k2a, q + ds / 2 * k2b)
        k4a, k4b = rhs(s + ds, Psi + ds * k3a, q + ds * k3b)
        Pn = Psi + ds / 6 * (k1a + 2 * k2a + 2 * k3a + k4a)
        qn = q + ds / 6 * (k1b + 2 * k2b + 2 * k3b + k4b)
        s_old = s; s = s + ds; r = math.exp(s)
        Psi = np.where(alive, Pn, Psi); q = np.where(alive, qn, q)
        if s_old < lr12 <= s:
            q12 = np.where(alive | np.isnan(q12), q, q12)
        mm = q / r ** 2
        cap = alive & (mm >= 0.999)
        status[cap] = 1; alive &= ~cap
        rat = q / qp(r)
        live = alive & (Psi > 0)
        maxratio = np.where(live, np.maximum(maxratio, rat), maxratio)
        qbr = qb(r); gain = np.log10((qbr + q) / (qbr + qp(r)))
        maxgain = np.where(live, np.maximum(maxgain, gain), maxgain)
        # excess bookkeeping (start radii of each excess interval)
        exc = live & (rat > 1 + 1e-3)
        newst = exc & ~in_exc
        for i in np.nonzero(newst)[0]:
            exc_start[i].append(r)
        in_exc = exc
        edge = alive & (Psi <= 0)
        status[edge] = 0; redge[edge] = r; alive &= ~edge
        if not alive.any():
            break
    q12 = np.where(np.isnan(q12), q, q12)
    return dict(status=status, maxratio=maxratio, q12=q12, redge=redge, exc_start=exc_start, maxgain=maxgain)


def system_list():
    """(label, footing, profile, y, sigmaN2_r12, r_eval) for every system in N1/N2 (isolated)."""
    L = []
    for r in SAT:
        L.append((f"sat|{r['name']}", r["footing"], "plummer", r["y_plummer"]))
    for r in COMA:
        L.append((f"coma|{r['name']}", r["footing"], "plummer", r["y_plummer"]))
    for f in FOOTS:
        for o in TDG:
            gb = G * o["M"] * MSUN / (o["R"] * KPC) ** 2 / A0[f]
            L.append((f"tdg|{o['name']}|uniform", f, "uniform", gb))
            L.append((f"tdg|{o['name']}|plummer", f, "plummer", gb * 4.0))        # Plummer scale R/2: y = GM/((R/2)^2 a0)
        for nm, gg_ in DFG.items():
            r12 = R12 * gg_["Re"] * KPC; aP = r12 / 1.30477
            L.append((f"dfg|{nm}", f, "plummer", G * gg_["Ms"] * MSUN / aP ** 2 / A0[f]))
    return L


SYS = system_list()
P(f"\n--- N1: T1 verified (isotropic spherical dust, muK = 0) on {len(SYS)} system-footing cases ---")
W0S = np.array([0.3, 1.0, 3.0, 6.0, 10.0])
RHOF = np.geomspace(1e-3, 1e4, 8)
SIGF = np.geomspace(0.03, 30.0, 6)
NPOLY = (1.5, 3.0, 5.0)
n1_rows = []; n1_max = {"frozen": 0.0, "A1": 0.0}; n1_case = {"frozen": None, "A1": None}; n1_gain = -np.inf
n1_mono_bad = 0; n1_counts = np.zeros(3, int)
t1 = time.time()
for (lab, f, prof, yv) in SYS:
    rgrid = np.geomspace(1e-3, 1e3, 3000)
    rp = rhoph_grid(prof, yv, rgrid)
    mono_ok = bool(np.all(np.diff(rp) <= 1e-9 * np.abs(rp[:-1])))
    n1_mono_bad += (not mono_ok)
    rho_ref = float(rhoph_grid(prof, yv, np.array([0.01]))[0])
    sN2 = float(qb_fun(prof, yv)(R12) / R12)              # r12 g_N(r12)
    allres = []
    for grid_lab, W0set, Sset, Nset in (("frozen", W0S, SIGF, NPOLY), ("A1", np.array([10.0, 20.0, 30.0]), np.array([1e-4, 1e-3, 1e-2]), (2.0, 2.5))):
        W0g, Sg, Rg = np.meshgrid(W0set, Sset * sN2, RHOF * rho_ref, indexing="ij")
        W0g, Sg, Rg = W0g.ravel(), Sg.ravel(), Rg.ravel()
        Kn = king_shape(W0g)
        rho_k = lambda rr, Ps, Sg=Sg, Rg=Rg, Kn=Kn: Rg * king_shape(Ps / Sg) / Kn
        allres.append((grid_lab, solve_equilibria(prof, yv, rho_k, len(W0g), Psi0=W0g * Sg)))
        for npoly in Nset:
            Pg, Rp = np.meshgrid(W0S * sN2, RHOF * rho_ref, indexing="ij"); Pg, Rp = Pg.ravel(), Rp.ravel()
            rho_p = lambda rr, Ps, Pg=Pg, Rp=Rp, npoly=npoly: Rp * (np.maximum(Ps, 0.0) / Pg) ** npoly
            allres.append((grid_lab, solve_equilibria(prof, yv, rho_p, len(Pg), Psi0=Pg.copy())))
    for grid_lab, o in allres:
        for st in (0, 1, 2):
            n1_counts[st] += int(np.sum(o["status"] == st))
        sel = o["status"] == 0
        if sel.any():
            mr = float(np.max(o["maxratio"][sel]))
            if mr > n1_max[grid_lab]:
                n1_max[grid_lab] = mr; n1_case[grid_lab] = lab + "|" + f
            n1_gain = max(n1_gain, float(np.max(o["maxgain"][sel])))
    caps_exc = sum(int(np.sum((o["status"] == 1) & (o["maxratio"] > 1 + 1e-3))) for _, o in allres)
    n1_rows.append(dict(case=lab, footing=f, y=yv, rho_ph_monotone=mono_ok,
                        max_ratio_edge=max([float(np.max(o["maxratio"][o["status"] == 0])) for _, o in allres if (o["status"] == 0).any()] + [0.0]),
                        n_edge=int(sum(np.sum(o["status"] == 0) for _, o in allres)), n_cap=int(sum(np.sum(o["status"] == 1) for _, o in allres)),
                        n_cap_with_excess=caps_exc))
P(f"   {len(SYS)} cases, {int(n1_counts.sum())} equilibria: edge {n1_counts[0]}, cap {n1_counts[1]}, unfinished {n1_counts[2]}; "
  f"rho_ph non-increasing fails in {n1_mono_bad} cases; {time.time() - t1:.0f} s")
P(f"   cap-reached runs that had passed the phantom first: {sum(r['n_cap_with_excess'] for r in n1_rows)} "
  f"(T1's proof: any excess runs away to the cap)")
P(f"   max ratio: frozen grid {n1_max['frozen']:.6f} ({n1_case['frozen']}); A1 near-cold/n=2-2.5 grid {n1_max['A1']:.6f} ({n1_case['A1']}); "
  f"max gravity gain log10[(M_b+M_tau)/(M_b+M_ph)](<r) over all r and all finite equilibria {n1_gain:+.5f} dex")
n1_all = max(n1_max.values())
ok_n1 = n1_all <= 1 + 1e-3 and n1_mono_bad == 0 and n1_counts[0] > 0
check("N1", ok_n1, f"max M_tau(<r)/M_ph(<r) over {n1_counts[0]} finite equilibria = {n1_all:.6f}", "<= 1.001",
      "T1: isotropic held dust never exceeds the phantom (any radius)")
RES["numbers"]["N1"] = dict(max_ratio=n1_max, case=n1_case, max_gain_dex=n1_gain, counts=n1_counts.tolist(), mono_bad=n1_mono_bad, rows=n1_rows)
P(f"   [peak RSS so far {rss_gb():.2f} GB, {time.time() - T0:.0f} s]")

P("\n--- N2: counterexample search -- anisotropic f = L^(-2 beta) g(E), rho = K r^(-2 beta) Psi^n ---")
BETAS = (-1.0, -0.5, 0.1, 0.25, 0.35, 0.45, 0.49)
NANI = (0.5, 1.5, 3.0, 4.5)
n2 = {b: dict(max_ratio=0.0, max_gain_r12=-np.inf, max_gain_any_r=-np.inf, n_edge=0, n_cap=0, viol=0, n_exc=0, case=None, case_gain=None) for b in BETAS}
t2 = time.time()
for (lab, f, prof, yv) in SYS:
    rgrid = np.geomspace(1e-4, 1e4, 20000)
    rp = rhoph_grid(prof, yv, rgrid)
    sN2 = float(qb_fun(prof, yv)(R12) / R12)
    rho12 = float(rhoph_grid(prof, yv, np.array([R12]))[0])
    qb = qb_fun(prof, yv); qp = qph_fun(prof, yv)
    for b in BETAS:
        prof_b = rgrid ** (2 * b) * rp
        istar = int(np.argmax(prof_b)); rstar = float(rgrid[istar])
        for npoly in NANI:
            if npoly <= 0.5 - b + 1e-12:
                continue
            Pg, Rp = np.meshgrid(W0S * sN2, RHOF * rho12 * 1e-1, indexing="ij"); Pg, Rp = Pg.ravel(), Rp.ravel()
            rho_a = lambda rr, Ps, Pg=Pg, Rp=Rp, npoly=npoly, b=b: Rp * (rr / R12) ** (-2 * b) * (np.maximum(Ps, 0.0) / Pg) ** npoly
            o = solve_equilibria(prof, yv, rho_a, len(Pg), aniso_beta=b, Psi0=Pg.copy(), nst=4000)
            sel = o["status"] == 0
            n2[b]["n_edge"] += int(sel.sum()); n2[b]["n_cap"] += int(np.sum(o["status"] == 1))
            for i in np.nonzero(sel)[0]:
                mr = float(o["maxratio"][i])
                if mr > 1 + 1e-3:
                    n2[b]["n_exc"] += 1
                    if any(rs >= rstar for rs in o["exc_start"][i]):
                        n2[b]["viol"] += 1
                if mr > n2[b]["max_ratio"]:
                    n2[b]["max_ratio"] = mr; n2[b]["case"] = f"{lab}|{f}|n{npoly}"
                gain = math.log10((qb(R12) + o["q12"][i]) / (qb(R12) + qp(R12)))
                n2[b]["max_gain_r12"] = max(n2[b]["max_gain_r12"], gain)
                if float(o["maxgain"][i]) > n2[b]["max_gain_any_r"]:
                    n2[b]["max_gain_any_r"] = float(o["maxgain"][i]); n2[b]["case_gain"] = f"{lab}|{f}|n{npoly}"
for b in BETAS:
    d = n2[b]
    P(f"   beta {b:+.2f}: finite {d['n_edge']:6d}, cap {d['n_cap']:6d}; max M_tau/M_ph {d['max_ratio']:.4f}; "
      f"max gain at r12 {d['max_gain_r12']:+.4f} dex, any r {d['max_gain_any_r']:+.4f} dex [{d['case_gain']}]; excess configs {d['n_exc']}, starting beyond r* {d['viol']}  [{d['case']}]")
ok_n2a = all(n2[b]["max_ratio"] <= 1 + 1e-3 for b in BETAS if b <= 0)
ok_n2b = all(n2[b]["viol"] == 0 for b in BETAS if b > 0)
check("N2", ok_n2a and ok_n2b, f"beta<=0 max ratio {max(n2[b]['max_ratio'] for b in BETAS if b <= 0):.5f}; "
      f"beta>0 excess starts beyond r* = {sum(n2[b]['viol'] for b in BETAS if b > 0)}; "
      f"max beta>0 ratio {max(n2[b]['max_ratio'] for b in BETAS if b > 0):.4f}, max gain at r12 {max(n2[b]['max_gain_r12'] for b in BETAS):+.4f} dex, any r {max(n2[b]['max_gain_any_r'] for b in BETAS):+.4f} dex",
      "beta<=0: <=1.001; beta>0: 0 starts beyond r*", f"generalised T1 ({time.time() - t2:.0f} s)")
RES["numbers"]["N2"] = {str(b): n2[b] for b in BETAS}
P(f"   [peak RSS so far {rss_gb():.2f} GB, {time.time() - T0:.0f} s]")

# =====================================================================================================================
#  N3: time-dependent infall (spherical shells with angular momentum; exact energy-consistent hold force)
# =====================================================================================================================
P("\n--- N3: counterexample search -- time-dependent infall (shell code, muK = 0) ---")


def Hfun(u):
    u = np.asarray(u, float)
    small = u < 1e-4
    ex = u * u / (1 + u) - u + np.log1p(u)
    ser = u ** 2 / 2 - 2 * u ** 3 / 3 + 3 * u ** 4 / 4
    return np.where(small, ser, ex)


def u_of(Q, r):
    return Q / np.maximum(r * r - Q, 1e-300)


GL_X, GL_W = np.polynomial.legendre.leggauss(6)


def E_hold(rs, qs):
    """Int_0^inf r^2 H(u(Q(r), r)) dr for sorted shell radii rs (masses qs)."""
    Qc = np.cumsum(qs)
    a_ = rs[:-1]; b_ = rs[1:]; Qk = Qc[:-1]
    mid = 0.5 * (a_ + b_); half = 0.5 * (b_ - a_)
    rr = mid[:, None] + half[:, None] * GL_X[None, :]
    val = np.sum(GL_W[None, :] * rr ** 2 * Hfun(u_of(Qk[:, None], rr)), axis=1) * half
    Qt = Qc[-1]; s1 = 1.0 / rs[-1]
    sm = 0.5 * s1 * (GL_X + 1); rr2 = 1.0 / np.maximum(sm, 1e-300)
    tail = 0.5 * s1 * np.sum(GL_W * rr2 ** 4 * Hfun(u_of(Qt, rr2)))     # dr = -dr/s^2 ... r^2 dr = ds / s^4
    return float(np.sum(val) + tail)


def shell_run(yv, lam, ft, N=3000, ndyn=40.0):
    qb = qb_fun("plummer", yv); qp = qph_fun("plummer", yv)
    rg = np.geomspace(1e-6, 60.0, 200000)
    if lam > 0:
        Qt = lam * float(qp(10.0)); tgt = (np.arange(N) + 0.5) / N * Qt
        r = np.interp(tgt, lam * qp(rg), rg)
    else:
        Qt = float(qp(10.0)); r = 20.0 * ((np.arange(N) + 0.5) / N) ** (1 / 3)
    qs = np.full(N, Qt / N)
    gA = law(qb(r) / r ** 2)
    j = r * ft * np.sqrt(r * gA)
    v = np.zeros(N)
    r0_init = r.copy()
    v12 = math.sqrt(R12 * float(law(qb(R12) / R12 ** 2)))
    tdyn = R12 / v12; Ttot = ndyn * tdyn

    def accel(r_):
        o = np.argsort(r_); rs = np.abs(r_[o]); qq = qs[o]
        Qlt = np.cumsum(qq) - qq
        aN = -(qb(rs) + Qlt + 0.5 * qq) / rs ** 2
        if MUT:
            ah = 0.0
            capf = False
        else:
            u1 = u_of(Qlt + qq, rs); u0 = u_of(Qlt, rs)
            capf = bool(np.any(Qlt + qq >= rs * rs))
            u1 = np.minimum(u1, 1e6)
            ah = rs * rs * (Hfun(u1) - Hfun(u0)) / qq
        a = np.empty_like(r_)
        a[o] = aN + ah + j[o] ** 2 / rs ** 3
        return a, capf, o

    def energy(r_, v_):
        o = np.argsort(r_); rs = np.abs(r_[o]); qq = qs[o]; Qlt = np.cumsum(qq) - qq
        KE = np.sum(qs * (v_ ** 2 + j ** 2 / r_ ** 2)) / 2
        PEb = -np.sum(qq * yv / np.sqrt(1 + rs * rs))
        WN = -np.sum(qq * (Qlt + 0.5 * qq) / rs)
        EH = 0.0 if MUT else E_hold(rs, qq)
        return KE + PEb + WN + EH

    def ratio12(r_):
        return float(np.sum(qs[np.abs(r_) < R12]) / qp(R12))

    E0 = energy(r, v); a, capf, o0 = accel(r)
    tt = 0.0; ncap = int(capf); first_cross = None; rat = [ratio12(r)]; times = [0.0]
    order0 = np.argsort(r)
    nstep = 0
    while tt < Ttot:
        dt = min(0.02 * float(np.min(np.sqrt(np.abs(r) / (np.abs(a) + 1e-30)))), tdyn / 50.0)
        dt = max(dt, tdyn / 4000.0)
        v = v + 0.5 * dt * a
        r = r + dt * v
        neg = r < 0
        r[neg] = -r[neg]; v[neg] = -v[neg]
        a, capf, o = accel(r)
        v = v + 0.5 * dt * a
        tt += dt; nstep += 1; ncap += int(capf)
        if first_cross is None and not np.array_equal(o, order0):
            first_cross = tt / tdyn
        if nstep % 20 == 0:
            rat.append(ratio12(r)); times.append(tt)
    E1 = energy(r, v)
    rat = np.array(rat); times = np.array(times)
    late = rat[times >= 0.75 * Ttot]
    vesc0 = np.sqrt(2 * yv / np.sqrt(1 + r0_init ** 2))                     # baryonic Newtonian escape speed at each shell's start
    vt_over_vesc = float(np.median(np.abs(j / r0_init) / vesc0))
    return dict(lam=lam, ft=ft, y=yv, vt_over_vescN_median=vt_over_vesc, E_rel_drift=abs(E1 - E0) / max(abs(E0), 1e-300), first_cross_tdyn=first_cross,
                ratio_t0=float(rat[0]), ratio_max=float(np.max(rat)), ratio_late=float(np.mean(late)), cap_steps=ncap, steps=nstep)


ysat = float(np.median([r["y_plummer"] for r in SAT if r["footing"] == "canonical"]))
ytdg = float(np.median([G * o["M"] * MSUN / (o["R"] / 2 * KPC) ** 2 / A0["canonical"] for o in TDG]))
n3 = []
t3 = time.time()
for lab_, yv in (("satellite", ysat), ("TDG", ytdg)):
    for lam in (1.0, 0.0, 0.5, 1.5, 3.0):
        for ft in (0.0, 0.5):
            rr = shell_run(yv, lam, ft)
            rr["system"] = lab_
            n3.append(rr)
            P(f"   {lab_:9s} y {yv:.2e} lambda {lam:3.1f} f_t {ft:3.1f}: ratio(r12) t0 {rr['ratio_t0']:.3f} max {rr['ratio_max']:.3f} "
              f"late {rr['ratio_late']:.3f}; first crossing {rr['first_cross_tdyn'] if rr['first_cross_tdyn'] is None else round(rr['first_cross_tdyn'], 3)} t_dyn; "
              f"cap steps {rr['cap_steps']}; |dE/E| {rr['E_rel_drift']:.1e}; {rr['steps']} steps; v_t/v_esc,N(baryons) {rr['vt_over_vescN_median']:.2f}")
ctrl = [rr for rr in n3 if rr["lam"] == 1.0 and rr["ft"] == 0.0]
ok_n3 = all(rr["E_rel_drift"] <= 1e-2 and abs(rr["ratio_late"] - 1) <= 0.02 and abs(rr["ratio_max"] - 1) <= 0.02 for rr in ctrl)
check("N3", ok_n3, "controls (lambda 1, cold): " + "; ".join(f"{rr['system']} |dE/E| {rr['E_rel_drift']:.1e}, ratio late {rr['ratio_late']:.4f}" for rr in ctrl),
      "|dE/E| <= 1e-2, |ratio-1| <= 0.02", f"shell code sane ({time.time() - t3:.0f} s)")
RES["numbers"]["N3"] = n3
P(f"   [peak RSS so far {rss_gb():.2f} GB, {time.time() - T0:.0f} s]")

# =====================================================================================================================
#  N4: T3 in the nonlinear regime (3-D periodic box) + negative mass of the linear-EFE phantom
# =====================================================================================================================
P("\n--- N4: nonlinear hold in a uniform host field: the hold self-force on a dust blob ---")
NG, LB, BB = 64, 40.0, 2.0
dx = LB / NG
xg = (np.arange(NG) - NG // 2) * dx
X, Y, Z = np.meshgrid(xg, xg, xg, indexing="ij")
kx = 2 * np.pi * np.fft.fftfreq(NG, d=dx)
kz = 2 * np.pi * np.fft.rfftfreq(NG, d=dx)
KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij")                    # real-FFT half grid (memory: N8)
K2 = KX ** 2 + KY ** 2 + KZ ** 2
nyq = (np.abs(np.abs(KX) - np.pi / dx) < 1e-9) | (np.abs(np.abs(KY) - np.pi / dx) < 1e-9) | (np.abs(np.abs(KZ) - np.pi / dx) < 1e-9)
K2s = np.where(K2 == 0, 1.0, K2)
KEEP = (~nyq).astype(float)
R2 = X ** 2 + Y ** 2 + Z ** 2
SHP = (NG, NG, NG)


def dspec(fh, Kc):
    return np.fft.irfftn(1j * Kc * KEEP * fh, s=SHP)


def make_plum(bb):
    pl = (3 / (4 * np.pi * bb ** 3)) * (1 + R2 / bb ** 2) ** -2.5
    return pl / (pl.sum() * dx ** 3)


def hold_solve(Q, xe, pl, phi0=None, tol=1e-8, maxit=4000, depth=6):
    S = 4 * np.pi * Q * (pl - pl.mean())
    Sh = np.fft.rfftn(S)
    phi = np.zeros_like(S) if phi0 is None else phi0.copy()

    def G_(ph):
        phh = np.fft.rfftn(ph)
        Ex = dspec(phh, KX); Ey = dspec(phh, KY); Ez = dspec(phh, KZ); Ez += xe
        muv = np.sqrt(Ex * Ex + Ey * Ey + Ez * Ez); muv /= (1 + muv)
        dv = np.fft.rfftn(muv * Ex) * (1j * KX)
        dv += np.fft.rfftn(muv * Ey) * (1j * KY)
        dv += np.fft.rfftn(muv * Ez) * (1j * KZ)
        dv += Sh; dv *= KEEP; dv /= -K2s; dv[0, 0, 0] = 0.0
        return np.fft.irfftn(dv, s=SHP)
    Xh, Fh = [], []
    it = 0; res = 1.0
    while it < maxit:
        g_ = G_(phi); f_ = g_ - phi
        res = float(np.linalg.norm(f_) / max(np.linalg.norm(g_), 1e-300))
        if res < tol:
            phi = g_
            break
        Xh.append(phi.copy()); Fh.append(f_.copy())
        if len(Xh) > depth:
            Xh.pop(0); Fh.pop(0)
        if len(Xh) > 1:
            dF = np.array([(Fh[i + 1] - Fh[i]).ravel() for i in range(len(Fh) - 1)]).T
            dX = np.array([(Xh[i + 1] - Xh[i]).ravel() for i in range(len(Xh) - 1)]).T
            Am = np.einsum("ij,ik->jk", dF, dF); gam = np.linalg.solve(Am + 1e-14 * np.trace(Am) * np.eye(len(Am)), np.einsum("ij,i->j", dF, f_.ravel()))
            phi = (phi.ravel() + f_.ravel() - np.einsum("ij,j->i", dX + dF, gam)).reshape(phi.shape)
        else:
            phi = phi + 0.5 * f_
        it += 1
    phh = np.fft.rfftn(phi)
    Ex = dspec(phh, KX); Ey = dspec(phh, KY); Ez = dspec(phh, KZ)
    rho = Q * pl
    F = np.array([np.sum(rho * Ex), np.sum(rho * Ey), np.sum(rho * Ez)]) * dx ** 3
    yint = float(np.max(np.sqrt(Ex ** 2 + Ey ** 2 + Ez ** 2)))
    return F / (Q * xe), it, res, yint, phi


def hold_target(xe, target, pl, Qhi):
    """bisection in log Q so that the internal hold-field maximum equals target (to 1 %)."""
    lo, hi = math.log(1e-4), math.log(Qhi); phi = None; best = None
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        Fn, it, res, yint, phi = hold_solve(math.exp(mid), xe, pl, phi0=phi)
        best = (math.exp(mid), Fn, it, res, yint)
        if abs(yint / target - 1) < 0.01:
            break
        if yint < target:
            lo = mid
        else:
            hi = mid
    return best


plum = make_plum(BB)
QCAP_B2 = 0.995 / float(np.max((lambda r: r ** 3 / (r * r + BB * BB) ** 1.5 / (r * r))(np.geomspace(0.01, 50, 20000))))
n4 = []
for xe in (0.03, 0.3, 3.0):
    for ratio_ in (0.1, 1.0, 10.0):
        Q, Fn, it, res, yint = hold_target(xe, ratio_ * xe, plum, QCAP_B2)
        n4.append(dict(xe=xe, Q=Q, y_int_max=yint, y_int_over_xe=yint / xe, Fz_self_over_Mxe=float(Fn[2]), Fperp=float(np.hypot(Fn[0], Fn[1])),
                       iters=it, res=res))
        P(f"   x_e {xe:5.2f}  Q {Q:8.4f}  internal hold field max {yint:8.4f} ({yint / xe:6.2f} x_e)  self-force/(M x_e) {Fn[2]:+.2e}  "
          f"(perp {np.hypot(Fn[0], Fn[1]):.1e})  iters {it} res {res:.1e}")
# reported (A1): resolution test of the strongest case with a smoother blob (b = 3)
plum3 = make_plum(3.0)
QCAP_B3 = 0.995 / float(np.max((lambda r: r ** 3 / (r * r + 9.0) ** 1.5 / (r * r))(np.geomspace(0.01, 50, 20000))))
Q3, F3_, it3, res3, y3 = hold_target(3.0, 30.0, plum3, QCAP_B3)
P(f"   [reported, A1] resolution test x_e 3, 10 x_e, blob b = 3 (vs 2): self-force/(M x_e) {F3_[2]:+.2e} (internal max {y3:.2f}, iters {it3})")
ok_n4 = all(abs(d["Fz_self_over_Mxe"]) <= 1e-3 and d["res"] < 1e-8 for d in n4)
check("N4", ok_n4, f"max |self-force|/(M x_e) = {max(abs(d['Fz_self_over_Mxe']) for d in n4):.2e}; worst residual {max(d['res'] for d in n4):.1e}",
      "<= 1e-3, converged", "total hold force on a blob = M grad(Xi_host); with D7(a) the static host's net force on held dust is 0")
# linear-EFE AQUAL phantom of a Plummer: negative mass fraction
negfr = {}
for xe in (0.03, 0.3, 3.0):
    mue = xe / (1 + xe); Le = 1 / (1 + xe)
    cos2 = np.where(K2 == 0, 1 / 3, KZ ** 2 / K2s)
    fth = mue * (1 + Le * cos2)
    fac = 1 / fth - 1
    fac[0, 0, 0] = float(np.mean(1 / (mue * (1 + Le * np.linspace(0, 1, 100001) ** 2)) - 1))
    dph = np.fft.irfftn(np.fft.rfftn(plum) * fac, s=SHP)
    negfr[str(xe)] = float(-dph[dph < 0].sum() / dph[dph > 0].sum())
P(f"   linear-EFE AQUAL phantom of a Plummer: negative/positive mass = {negfr} (allowed for LIT, forbidden for MS dust)")
RES["numbers"]["N4"] = dict(runs=n4, negative_mass_fraction=negfr, resolution_test_b3=dict(Q=Q3, self_force=float(F3_[2]), y_int=y3, iters=it3))
P(f"   [peak RSS so far {rss_gb():.2f} GB, {time.time() - T0:.0f} s]")

# =====================================================================================================================
#  N5: velocity and acceleration -- the hosted tiles
# =====================================================================================================================
P("\n--- N5: v3's own dynamics for the hosted tiles (B0 dust-free; B1-MS acceleration-held; B1-LIT also streaming-limited) ---")
A_H = 3.0 * KPC
MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}


def g_host_S1(R_m, Mb, a0):
    gNh = G * Mb * MSUN / (R_m + A_H) ** 2
    return 0.5 * gNh * (1 + math.sqrt(1 + 4 * a0 / gNh))


def held_radius(prof, yv, xe):
    """largest r with g_int(r) >= x_e (isolated law internal field); 0 if none."""
    rg = np.geomspace(1e-4, 1e4, 40000)
    gi = law(qb_fun(prof, yv)(rg) / rg ** 2)
    idx = np.nonzero(gi >= xe)[0]
    return float(rg[idx[-1]]) if len(idx) else 0.0


def follow_radius(prof, yv, V2):
    """largest r with 2 q_b(r)/r >= V^2 (units a0 a); 0 if none."""
    rg = np.geomspace(1e-4, 1e4, 40000)
    w = 2 * qb_fun(prof, yv)(rg) / rg
    idx = np.nonzero(w >= V2)[0]
    return float(rg[idx[-1]]) if len(idx) else 0.0


def branch_gain(prof, yv, rev, r_hold):
    """(q_b(rev) + q_ph(min(rev, r_hold)))/q_b(rev): held-dust boost of g at the evaluation radius."""
    qb = qb_fun(prof, yv); qp = qph_fun(prof, yv)
    qh = float(qp(min(rev, r_hold))) if r_hold > 0 else 0.0
    return (float(qb(rev)) + qh) / float(qb(rev)), qh / max(float(qp(rev)), 1e-300)


# LVD speeds for MW satellites
try:
    from astropy.coordinates import SkyCoord, Galactocentric, CartesianDifferential
    import astropy.units as au
    HAVE_ASTROPY = True
except Exception:                                              # pragma: no cover
    HAVE_ASTROPY = False


def fl(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
        LVD[r["name"]] = dict(ra=fl(r.get("ra")), dec=fl(r.get("dec")), dist=fl(r.get("distance")), pmra=fl(r.get("pmra")),
                              pmdec=fl(r.get("pmdec")), vsys=fl(r.get("vlos_systemic")))


def v3d_mw(nm):
    d = LVD.get(nm)
    if not HAVE_ASTROPY or d is None or None in (d["ra"], d["dec"], d["dist"], d["pmra"], d["pmdec"], d["vsys"]):
        return None
    c = SkyCoord(ra=d["ra"] * au.deg, dec=d["dec"] * au.deg, distance=d["dist"] * au.kpc, pm_ra_cosdec=d["pmra"] * au.mas / au.yr,
                 pm_dec=d["pmdec"] * au.mas / au.yr, radial_velocity=d["vsys"] * au.km / au.s)
    gc = c.transform_to(Galactocentric(galcen_distance=8.122 * au.kpc, z_sun=20.8 * au.pc,
                                       galcen_v_sun=CartesianDifferential([12.9, 245.6, 7.78] * au.km / au.s)))
    vv = np.array([gc.v_x.to(au.km / au.s).value, gc.v_y.to(au.km / au.s).value, gc.v_z.to(au.km / au.s).value])
    return float(np.linalg.norm(vv))


rng = np.random.default_rng(23)


def boot_med(arr, n=4000):
    arr = np.asarray(arr, float); N = len(arr)
    meds = np.array([np.median(arr[rng.integers(0, N, N)]) for _ in range(n)])
    return float(np.median(arr)), float(np.std(meds))


N5 = dict(satellites={}, coma={}, tdg={}, dfg={})
n5_ok = True
sat_rows = []
for f in FOOTS:
    a0 = A0[f]
    rows = [r for r in SAT if r["footing"] == f]
    D = {"static_v3_Lfloor": [], "static_EFE_L0": [], "iso_law": [], "B0": [], "B1_MS": [], "B1_LIT": []}
    fr_ms, fr_lit, aratio = [], [], []
    nPM = 0
    for r in rows:
        yv = r["y_plummer"]; a_m = r["rh_pc"] * PC; xe = r["x_e_mid"]
        V = v3d_mw(r["name"]) if r["host"] == "MW" else None
        src = "LVD-3D"
        if V is None:
            Rh = r["d_host_kpc"] * KPC
            V = math.sqrt(Rh * g_host_S1(Rh, MHOST.get(r["host"], 6e10), a0)) / 1e3; src = "PROXY"
        else:
            nPM += 1
        V2 = (V * 1e3) ** 2 / (a0 * a_m)
        rh_ = held_radius("plummer", yv, xe); rf_ = follow_radius("plummer", yv, V2)
        gB0 = math.log10(2 * float(qb_fun("plummer", yv)(R12)) / yv)
        gain_ms, fms = branch_gain("plummer", yv, R12, rh_)
        gain_lit, flit = branch_gain("plummer", yv, R12, min(rh_, rf_))
        lb = r["log_gobs_gbar"]
        D["static_v3_Lfloor"].append(lb - r["logG_v3_Lfloor"]); D["static_EFE_L0"].append(lb - r["logG_emb0"]); D["iso_law"].append(lb - r["logG_iso0"])
        D["B0"].append(lb - gB0); D["B1_MS"].append(lb - (gB0 + math.log10(gain_ms))); D["B1_LIT"].append(lb - (gB0 + math.log10(gain_lit)))
        qbt = 1.0                                                   # held-dust / baryon mass ratio for the fall rate
        qhold = float(qph_fun("plummer", yv)(rh_)) if rh_ > 0 else 0.0
        aratio.append(1.0 / (1.0 + qhold / yv))
        fr_ms.append(fms); fr_lit.append(flit)
        if not (gain_ms >= 1.0 and gain_lit >= 1.0):
            n5_ok = False
        sat_rows.append(dict(footing=f, name=r["name"], host=r["host"], V_kms=V, V_src=src, x_e=xe, y=yv, r_h_over_a=rh_, r_f_over_a=rf_,
                             held_frac_ph_r12_MS=fms, held_frac_ph_r12_LIT=flit, a_over_ghost_B1=aratio[-1],
                             Delta_static=D["static_v3_Lfloor"][-1], Delta_B0=D["B0"][-1], Delta_B1_MS=D["B1_MS"][-1], Delta_B1_LIT=D["B1_LIT"][-1]))
    st = {kk: boot_med(vv) for kk, vv in D.items()}
    N5["satellites"][f] = dict(stats=st, N=len(rows), N_LVD_3D=nPM, median_held_frac_MS=float(np.median(fr_ms)),
                               median_held_frac_LIT=float(np.median(fr_lit)), median_fall_ratio_B1=float(np.median(aratio)),
                               median_V=float(np.median([s["V_kms"] for s in sat_rows if s["footing"] == f])))
    P(f"   satellites [{f}] N {len(rows)} (LVD 3-D speeds {nPM}, others PROXY), median V {N5['satellites'][f]['median_V']:.0f} km/s")
    for kk, (m_, s_) in st.items():
        P(f"      Delta {kk:18s} {m_:+.3f} +- {s_:.3f}  ({m_ / s_:+.1f} sd)")
    P(f"      held dust inside r12 / static isolated phantom: median MS {np.median(fr_ms):.3e}, LIT {np.median(fr_lit):.3e}; "
      f"B1 fall rate a/g_host median {np.median(aratio):.3f}")

# Coma UDGs
KEV, MP = 1.602176634e-16, 1.67262e-27
BETA = dict(kT=8.6, rc=276.0, beta=0.71, mu=0.6)
CB = 3 * BETA["beta"] * BETA["kT"] * KEV / (BETA["mu"] * MP)


def g_beta(d_kpc):
    rr = d_kpc * KPC; rc = BETA["rc"] * KPC
    return CB * rr / (rr * rr + rc * rc)


def coma_E(c, a0, mode, mfac=1.0, sfac=1.0, dfac=1.0):
    Ms = c["Mstar"] * mfac * dfac ** 2; Re = c["Re_kpc"] * dfac; sg = c["sigma"] * sfac
    a_m = Re * KPC; r12 = R12 * a_m
    yv = G * Ms * MSUN / (a_m ** 2 * a0)
    qb = qb_fun("plummer", yv)
    if mode == "B0":
        gpred = float(qb(R12)) / R12 ** 2 * a0
    else:
        xe = c["x_e_dmean"]
        rh_ = held_radius("plummer", yv, xe)
        if mode == "B1_LIT":
            V = math.sqrt(c["d_mean_kpc"] * KPC * g_beta(c["d_mean_kpc"]))
            rh_ = min(rh_, follow_radius("plummer", yv, V * V / (a0 * a_m)))
        qh = float(qph_fun("plummer", yv)(min(R12, rh_))) if rh_ > 0 else 0.0
        gpred = (float(qb(R12)) + qh) / R12 ** 2 * a0
    s2 = r12 * gpred / 3
    return 2 * math.log(sg * 1e3 / math.sqrt(s2)), 2 * c["esig"] / c["sigma"]


for f in FOOTS:
    a0 = A0[f]; rows = [c for c in COMA if c["footing"] == f]
    out = {}
    for mode in ("B0", "B1_MS", "B1_LIT"):
        Es = [coma_E(c, a0, mode) for c in rows]
        E = np.array([e for e, _ in Es]); sE = np.array([s for _, s in Es])
        mE = float(E.mean()); se = max(float(E.std(ddof=1) / math.sqrt(len(E))), float(math.sqrt(np.sum(sE ** 2)) / len(E)))
        mv = lambda **kw: float(np.mean([coma_E(c, a0, mode, **kw)[0] for c in rows]))
        sM = abs(mv(mfac=10 ** 0.2) - mv(mfac=10 ** -0.2)) / 2; sA = abs(mv(sfac=1.15) - mv(sfac=1 / 1.15)) / 2
        sD = abs(mv(dfac=1.05) - mv(dfac=0.95)) / 2; ssys = math.sqrt(sM ** 2 + sA ** 2 + sD ** 2)
        out[mode] = dict(meanE=mE, dex=mE / math.log(10), se=se, z_stat=mE / se, s_M=sM, s_A=sA, s_D=sD, sigma_sys=ssys,
                         z_sys=mE / math.sqrt(se ** 2 + ssys ** 2))
    out["static_v3_dmean_S1"] = dict(meanE=float(np.mean([c["E_v3_dmean"] for c in rows])))
    out["isolated_law_S1"] = dict(meanE=float(np.mean([c["E_old"] for c in rows])))
    N5["coma"][f] = out
    P(f"   Coma UDGs [{f}] N {len(rows)}: " + "; ".join(f"{m_} <E> {out[m_]['meanE']:+.3f} ln ({out[m_]['dex']:+.3f} dex) z_stat {out[m_]['z_stat']:+.1f} "
                                                      f"z_sys {out[m_]['z_sys']:+.1f}" for m_ in ("B0", "B1_MS", "B1_LIT"))
      + f"; S1 static <E> {out['static_v3_dmean_S1']['meanE']:+.3f}")


# TDGs and DF2/DF4
def stats5(rv, sv):
    rv = np.asarray(rv, float); sv = np.asarray(sv, float); n = len(rv)
    se = max(float(np.std(rv, ddof=1) / math.sqrt(n)), float(math.sqrt(np.sum(sv ** 2)) / n))
    return dict(n=n, rbar=float(np.mean(rv)), se=se, z=float(np.mean(rv)) / se)


def tdg_r(o, a0, mode, prof="uniform", M=None, R=None):
    M = o["M"] if M is None else M; R = o["R"] if R is None else R
    a_m = R * KPC if prof == "uniform" else R / 2 * KPC
    rev = 1.0 if prof == "uniform" else 2.0
    yv = G * M * MSUN / (a_m ** 2 * a0)
    gNe = G * 0.6 * o["LK"] * MSUN / (o["Dp"] * KPC) ** 2 / a0
    xe = float(law(gNe))
    qb = qb_fun(prof, yv)
    if mode == "B0":
        qh = 0.0
    else:
        rh_ = held_radius(prof, yv, xe)
        if mode == "B1_LIT":
            V = math.sqrt(o["Dp"] * KPC * xe * a0)
            rh_ = min(rh_, follow_radius(prof, yv, V * V / (a0 * a_m)))
        qh = float(qph_fun(prof, yv)(min(rev, rh_))) if rh_ > 0 else 0.0
    gpred = (float(qb(rev)) + qh) / rev ** 2 * a0 / a_m * a_m           # a0 units * a0 -> SI accel (a cancels)
    go = (o["V"] * 1e3) ** 2 / (R * KPC)
    return math.log10(go / gpred), xe


def df_r(nm, a0, mode, V=179.0):
    gg_ = DFG[nm]
    r12 = R12 * gg_["Re"] * KPC; aP = r12 / 1.30477; rev = 1.30477
    yv = G * gg_["Ms"] * MSUN / (aP ** 2 * a0)
    vec = np.zeros(2)
    for h, Mh in (("NGC1052", 1e11), ("NGC1035", 5e9)):
        p, q = gg_["pos"], HOSTS[h]
        ra1, d1, ra2, d2 = map(math.radians, (p[0], p[1], q[0], q[1]))
        cc = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(ra1 - ra2)
        dxv = (ra2 - ra1) * math.cos(d1); dyv = d2 - d1; nrm_ = math.hypot(dxv, dyv)
        Rk = gg_["D"] * 1000 * math.acos(min(1.0, cc)) * KPC
        vec += G * Mh * MSUN / Rk ** 2 / a0 * np.array([dxv / nrm_, dyv / nrm_])
    xe = float(law(float(np.linalg.norm(vec))))
    qb = qb_fun("plummer", yv)
    if mode == "B0":
        qh = 0.0
    else:
        rh_ = held_radius("plummer", yv, xe)
        if mode == "B1_LIT":
            rh_ = min(rh_, follow_radius("plummer", yv, (V * 1e3) ** 2 / (a0 * aP)))
        qh = float(qph_fun("plummer", yv)(min(rev, rh_))) if rh_ > 0 else 0.0
    g12 = (float(qb(rev)) + qh) / rev ** 2 * a0
    sp_ = math.sqrt(r12 * g12 / 3) / 1e3
    so, up, lo = gg_["obs"]
    e = lo if so > sp_ else up
    return 2 * math.log(so / sp_), 2 * e / so, sp_, xe


LN10 = math.log(10)
for f in FOOTS:
    a0 = A0[f]
    out = {}
    for mode in ("B0", "B1_MS", "B1_LIT"):
        rv, sv, xes = [], [], []
        for o in TDG:
            r0, xe = tdg_r(o, a0, mode)
            sV = 2 * o["eV"] / (o["V"] * LN10)
            dM = (tdg_r(o, a0, mode, M=o["M"] * 1.01)[0] - r0) / 0.01 * o["eM"] / o["M"]
            dR = (tdg_r(o, a0, mode, R=o["R"] * 1.01)[0] - r0) / 0.01 * o["eR"] / o["R"]
            rv.append(r0); sv.append(math.sqrt(sV ** 2 + dM ** 2 + dR ** 2)); xes.append(xe)
        st = stats5(rv, sv); st["x_e"] = xes
        st_pl = stats5([tdg_r(o, a0, mode, prof="plummer")[0] for o in TDG], sv)
        st["plummer_variant_rbar"] = st_pl["rbar"]
        out[f"TDG_{mode}"] = st
        U = [df_r(nm, a0, mode) for nm in DFG]
        out[f"DF_{mode}"] = dict(stats5([u[0] for u in U], [u[1] for u in U]), sigma_pred=[u[2] for u in U], r=[u[0] for u in U], x_e=[u[3] for u in U])
        if mode == "B1_LIT":
            for Vb in (125.0, 225.0):
                Ub = [df_r(nm, a0, mode, V=Vb) for nm in DFG]
                out[f"DF_B1_LIT_V{int(Vb)}"] = dict(r=[u[0] for u in Ub])
    N5["tdg"][f] = out
    P(f"   TDGs [{f}]: " + "; ".join(f"{m_} rbar {out['TDG_' + m_]['rbar']:+.3f} +- {out['TDG_' + m_]['se']:.3f} dex ({out['TDG_' + m_]['z']:+.1f} se)"
                                      for m_ in ("B0", "B1_MS", "B1_LIT")) + f"; x_e {np.round(out['TDG_B0']['x_e'], 3).tolist()}")
    P(f"   DF2/DF4 [{f}]: " + "; ".join(f"{m_} r = {np.round(out['DF_' + m_]['r'], 3).tolist()} ln, sigma_pred {np.round(out['DF_' + m_]['sigma_pred'], 2).tolist()} km/s"
                                         for m_ in ("B0", "B1_MS", "B1_LIT")))
# reported (A1): the dust's binding is at most the baryons' Newtonian well (D4: psi' <= g_N,b): v_esc,N(centre) vs observed speeds
ESC = {}
for f in FOOTS:
    a0 = A0[f]
    rs_ = []
    for r in (rr for rr in SAT if rr["footing"] == f):
        M = 10 ** r["logMstar"] * MSUN; a_m = r["rh_pc"] * PC; r12 = R12 * a_m
        gobs = 10 ** r["log_gobs_gbar"] * G * 0.5 * M / r12 ** 2
        rs_.append(math.sqrt(2 * G * M / a_m) / math.sqrt(gobs * r12 / 3))
    rc_ = [math.sqrt(2 * G * c["Mstar"] * MSUN / (c["Re_kpc"] * KPC)) / (c["sigma"] * 1e3) for c in COMA if c["footing"] == f]
    rt_ = [math.sqrt(3 * G * o["M"] * MSUN / (o["R"] * KPC)) / (o["V"] * 1e3) for o in TDG]
    rd_ = [math.sqrt(2 * G * g_["Ms"] * MSUN / (R12 * g_["Re"] * KPC / 1.30477)) / (g_["obs"][0] * 1e3) for g_ in DFG.values()]
    ESC[f] = dict(sat_median=float(np.median(rs_)), coma_median=float(np.median(rc_)), tdg_median=float(np.median(rt_)), df=rd_)
    P(f"   [{f}] baryonic Newtonian escape speed from the centre / observed sigma (or V): satellites median {np.median(rs_):.2f}, "
      f"Coma {np.median(rc_):.2f}, TDGs {np.median(rt_):.2f}, DF2/DF4 {np.round(rd_, 2).tolist()}  (held dust must move slower than this)")
N5["escape_ratio"] = ESC
check("N5", n5_ok and all(len(N5[t_]) == 2 for t_ in ("satellites", "coma", "tdg")), f"branches computed for {len(sat_rows)} satellite cases, "
      f"{len(COMA)} Coma, {2 * len(TDG)} TDG, 4 DF cases; B1 >= B0 everywhere {n5_ok}", "all computed; B1 >= B0", "")
RES["numbers"]["N5"] = N5
P(f"   [peak RSS so far {rss_gb():.2f} GB, {time.time() - T0:.0f} s]")
with open(os.path.join(HERE, f"u1_satellites_per_system{SFX}.csv"), "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=list(sat_rows[0].keys())); wr.writeheader(); wr.writerows(sat_rows)

# =====================================================================================================================
#  N6: Milky Way -- the most round hot dust v3 can hold (T1 bound on the baryon monopole)
# =====================================================================================================================
P("\n--- N6: Milky Way: round dust at the T1 bound (McMillan17 baryons) ---")
R0_MW = 8.122
PC2, PC3 = 1e6, 1e9
S0_THIN, RD_THIN, ZD_THIN = 896.0 * PC2, 2.50, 0.300
S0_THICK, RD_THICK, ZD_THICK = 183.0 * PC2, 3.02, 0.900
RHO0_B, ALPHA_B, R0_B, RCUT_B, Q_B = 98.4 * PC3, 1.8, 0.075, 2.1, 0.5
R_FID = 8.33
S0_HI = 10.0 * PC2 / math.exp(-4.0 / R_FID - R_FID / 7.0)
S0_H2 = 2.0 * PC2 / math.exp(-12.0 / R_FID - R_FID / 1.5)


def rho_mcm(R, zq):
    zq = np.abs(zq)
    thin = (S0_THIN / (2 * ZD_THIN)) * np.exp(-zq / ZD_THIN - R / RD_THIN)
    thick = (S0_THICK / (2 * ZD_THICK)) * np.exp(-zq / ZD_THICK - R / RD_THICK)
    rp = np.maximum(np.sqrt(R * R + (zq / Q_B) ** 2), 1e-7)
    bulge = RHO0_B / (1 + rp / R0_B) ** ALPHA_B * np.exp(-(rp / RCUT_B) ** 2)
    Rs = np.maximum(R, 1e-6)
    hi = (S0_HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(np.minimum(zq / (2 * 0.085), 300)) ** 2
    h2 = (S0_H2 * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(np.minimum(zq / (2 * 0.045), 300)) ** 2
    return thin + thick + bulge + hi + h2                                # Msun / kpc^3


def load_tsv(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.startswith("#")]
    hdr = rows[0]; arr = np.array([[float(xv) for xv in rr] for rr in rows[1:]])
    return {h: arr[:, i] for i, h in enumerate(hdr)}


EIL = load_tsv(os.path.join(DATA, "mw_rc_eilers2019_table1.tsv"))
EIL_R, EIL_V = EIL["R_kpc"], EIL["vc_kms"]; EIL_E = np.hypot(0.5 * (EIL["sig_minus"] + EIL["sig_plus"]), 0.02 * EIL_V)
BR = load_tsv(os.path.join(DATA, "mw_kz11_bovyrix2013_table3.tsv"))
BR_R = BR["R_kpc"] + (R0_MW - 8.0); BR_K, BR_E = BR["Kz11_o2piG"], BR["dKz11_o2piG"]; BR_E5 = np.hypot(BR_E, 0.05 * BR_K)
Gk = 4.30091e-6                                                          # kpc (km/s)^2 / Msun
# ring quadrature for the baryons (my own): rings (R', z') with dm = 2 pi R' rho dR' dz'
Rr = np.arange(0.00625, 40.0, 0.0125)
zq = np.concatenate([-np.geomspace(1e-4, 25.0, 700)[::-1], np.geomspace(1e-4, 25.0, 700)])
dzq = np.gradient(zq)


def ring_field(Rp, zp):
    """(g_R inward, g_z toward plane-from-above) in (km/s)^2/kpc at (Rp, zp) from the McMillan baryons."""
    gR = 0.0; gz = 0.0
    for k0 in range(0, len(Rr), 400):
        Ra = Rr[k0:k0 + 400][:, None]; Za = zq[None, :]
        dm = 2 * math.pi * Ra * rho_mcm(Ra, Za) * 0.0125 * dzq[None, :]
        h = zp - Za; den = (Ra + Rp) ** 2 + h * h; mk_ = 4 * Ra * Rp / den
        Ek, Kk = ellipe(mk_), ellipk(mk_)
        dd = (Ra - Rp) ** 2 + h * h
        gz += float(np.sum(dm * (2 / math.pi) * h * Ek / (dd * np.sqrt(den))))
        gR += float(np.sum(dm * (1 / (math.pi * Rp)) * (Kk - Ek * (Ra * Ra - Rp * Rp + h * h) / dd) / np.sqrt(den)))
    return Gk * gR, Gk * gz                                               # inward positive, toward plane positive (A1 fix)


# sanity of the g_R ring formula against a finite-difference of the ring potential for one ring
def ring_phi(Ra, Za, Rp, zp):
    h = zp - Za; den = (Ra + Rp) ** 2 + h * h
    return -(2 / math.pi) * ellipk(4 * Ra * Rp / den) / np.sqrt(den)


hh = 1e-5
fd = -(ring_phi(5.0, 0.2, 8.0 + hh, 0.3) - ring_phi(5.0, 0.2, 8.0 - hh, 0.3)) / (2 * hh)
h_ = 0.3 - 0.2; den_ = (5 + 8.0) ** 2 + h_ * h_; m__ = 4 * 5 * 8.0 / den_; dd_ = (5 - 8.0) ** 2 + h_ * h_
an = (1 / (math.pi * 8.0)) * (ellipk(m__) - ellipe(m__) * (25 - 64 + h_ * h_) / dd_) / math.sqrt(den_)
ring_formula_err = abs(an + fd) / abs(fd)                               # an is the inward magnitude: an = -(-dPhi/dR)
gR0, _ = ring_field(R0_MW, 0.0)
_, gz11 = ring_field(R0_MW, 1.1)
Kb = gz11 / (2 * math.pi * Gk) / 1e6                                     # Msun/pc^2
KRING_P4 = 61.995816632575654
# baryon monopole M_b(<r)
rr_m = np.geomspace(1e-3, 300.0, 1500)
cgrid = np.concatenate([np.geomspace(1e-7, 1e-2, 400), np.linspace(1e-2, 1.0, 600)[1:]])
dc = np.gradient(cgrid)
rho_avg = np.array([np.sum(rho_mcm(rv * np.sqrt(1 - cgrid ** 2), rv * cgrid) * dc) for rv in rr_m])
Mb_r = np.concatenate([[0.0], np.cumsum(0.5 * (4 * np.pi * rr_m[1:] ** 2 * rho_avg[1:] + 4 * np.pi * rr_m[:-1] ** 2 * rho_avg[:-1]) * np.diff(rr_m))])
N6 = {}
for f in FOOTS:
    a0k = A0[f] * KPC / 1e6                                              # (km/s)^2 / kpc
    n_m = Gk * Mb_r / np.maximum(rr_m, 1e-30) ** 2 / a0k
    Mph = mph_n(n_m) * a0k * rr_m ** 2 / Gk
    Mph_at = lambda rv: float(np.interp(math.log(rv), np.log(rr_m), Mph))
    vc = math.sqrt(R0_MW * (gR0 + Gk * Mph_at(R0_MW) / R0_MW ** 2))
    sB = math.hypot(R0_MW, 1.1)
    Kd = Gk * Mph_at(sB) / sB ** 2 * (1.1 / sB) / (2 * math.pi * Gk) / 1e6
    # chi2 over the 43 MAPs
    if f == FOOTS[0]:
        KB43 = np.array([ring_field(Rv, 1.1)[1] / (2 * math.pi * Gk) / 1e6 for Rv in BR_R])
    KD43 = np.array([Gk * Mph_at(math.hypot(Rv, 1.1)) / math.hypot(Rv, 1.1) ** 2 * (1.1 / math.hypot(Rv, 1.1)) / (2 * math.pi * Gk) / 1e6 for Rv in BR_R])
    Kall = KB43 + KD43
    chi2 = float(np.sum(((Kall - BR_K) / BR_E5) ** 2))
    lam_scan = {}
    for lam_ in (0.0, 0.25, 0.5, 0.75, 1.0):                             # reported: round dust at a fraction of the bound
        lam_scan[str(lam_)] = dict(chi2_Kz=float(np.sum(((KB43 + lam_ * KD43 - BR_K) / BR_E5) ** 2)), Kz_R0=Kb + lam_ * Kd,
                                   vc_R0=math.sqrt(R0_MW * (gR0 + lam_ * Gk * Mph_at(R0_MW) / R0_MW ** 2)))
    vE = float(np.interp(R0_MW, EIL_R, EIL_V)); eE = float(np.interp(R0_MW, EIL_R, EIL_E))
    # reported (not frozen): scale the round dust by lambda so K_z(R0) = 66.4, and v_c there
    Kdat = 66.4
    lam_fit = (Kdat - Kb) / Kd
    vc_fit = math.sqrt(R0_MW * (gR0 + lam_fit * Gk * Mph_at(R0_MW) / R0_MW ** 2))
    N6[f] = dict(vc_R0_bound=vc, Kz_R0_bound=Kb + Kd, Kz_baryons=Kb, Kz_dust_bound=Kd, chi2_Kz_bound=chi2, vc_Eilers_R0=vE, e_vc_Eilers=eE,
                 vc_deficit_sigma=(vE - vc) / eE, lambda_for_Kz_data=lam_fit, vc_at_Kz_data=vc_fit, lambda_scan=lam_scan, Mph_R0=Mph_at(R0_MW), Mb_R0=float(np.interp(math.log(R0_MW), np.log(rr_m), Mb_r)))
    P(f"   [{f}] T1 bound (round dust = monopole phantom): v_c(R0) {vc:.1f} km/s (Eilers {vE:.1f} +- {eE:.1f}: {(vE - vc) / eE:+.1f} sigma short); "
      f"K_z(R0,1.1) {Kb + Kd:.1f} (baryons {Kb:.1f} + dust {Kd:.1f}) vs 66.4 +- 2.2; chi2_Kz {chi2:.1f} (line 67.5); "
      f"dust scaled to K_z = 66.4 (lambda {lam_fit:.2f}) gives v_c {vc_fit:.1f}")
    P(f"      [reported] round dust at lambda x bound: " + "; ".join(f"lambda {k_}: chi2_Kz {v_['chi2_Kz']:.1f}, K_z(R0) {v_['Kz_R0']:.1f}, v_c {v_['vc_R0']:.1f}" for k_, v_ in lam_scan.items()))
ok_n6 = abs(Kb / KRING_P4 - 1) <= 0.01 and ring_formula_err < 1e-4
check("N6", ok_n6, f"my baryon K_z(R0,1.1) {Kb:.3f} vs P4 ring {KRING_P4:.3f} ({abs(Kb / KRING_P4 - 1):.2e}); g_R ring formula vs FD {ring_formula_err:.1e}",
      "<= 1%", "MW computed on both footings")
RES["numbers"]["N6"] = N6
P(f"   [peak RSS so far {rss_gb():.2f} GB, {time.time() - T0:.0f} s]")

# =====================================================================================================================
#  N7: when can muK be dropped?
# =====================================================================================================================
P("\n--- N7: the muK^2 term: eps_K = muK^2 r^3 |Xi_ref| / (3 G M_ph(<r)) ---")
N7 = {}
for f in FOOTS:
    a0 = A0[f]
    out = {}
    for mk_lab, mkv in MUK.items():
        eps = []; dXi = []
        for r in (rr for rr in SAT if rr["footing"] == f):
            yv = r["y_plummer"]; a_m = r["rh_pc"] * PC
            Rh = r["d_host_kpc"] * KPC
            vch2 = Rh * g_host_S1(Rh, MHOST.get(r["host"], 6e10), a0)
            Mph12 = float(qph_fun("plummer", yv)(R12)) * a0 * a_m ** 2 / G
            r12 = R12 * a_m
            eps.append(mkv ** 2 * r12 ** 3 * 3 * vch2 / (3 * G * Mph12))
            gobs = 10 ** r["log_gobs_gbar"] * G * (0.5 * 10 ** r["logMstar"] * MSUN) / r12 ** 2
            gv3 = 10 ** r["logG_v3_Lfloor"] * G * (0.5 * 10 ** r["logMstar"] * MSUN) / r12 ** 2
            rho_need = max(gobs - gv3, 0.0) * r12 ** 2 / G / (4 / 3 * math.pi * r12 ** 3)
            dXi.append(4 * math.pi * G * rho_need / mkv ** 2)
        epsC = []
        for c in (cc for cc in COMA if cc["footing"] == f):
            a_m = c["Re_kpc"] * KPC; yv = G * c["Mstar"] * MSUN / (a_m ** 2 * a0)
            vch2 = c["d_mean_kpc"] * KPC * g_beta(c["d_mean_kpc"])
            Mph12 = float(qph_fun("plummer", yv)(R12)) * a0 * a_m ** 2 / G
            epsC.append(mkv ** 2 * (R12 * a_m) ** 3 * 3 * vch2 / (3 * G * Mph12))
        clu = {}
        for rk in (0.3, 1.0):
            rm = rk * 1e3 * KPC; Mc = 1e14
            gNc = G * Mc * MSUN / rm ** 2 / a0; gl = float(law(gNc)) * a0
            Mphc = (gl * rm ** 2 / G) - Mc * MSUN
            clu[f"{rk}Mpc"] = mkv ** 2 * rm ** 3 * 3 * gl * rm / (3 * G * Mphc)
        out[mk_lab] = dict(sat_eps_median=float(np.median(eps)), sat_eps_max=float(np.max(eps)), coma_eps_max=float(np.max(epsC)),
                           cluster_1e14=clu, sat_dXi_needed_over_c2_median=float(np.median(dXi)) / 2.998e8 ** 2)
        P(f"   [{f}] {mk_lab:24s}: satellites eps median {np.median(eps):.1e} max {np.max(eps):.1e}; Coma max {np.max(epsC):.1e}; "
          f"cluster 1e14 at 0.3/1 Mpc {clu['0.3Mpc']:.2e}/{clu['1.0Mpc']:.2e}; zero-point offset needed (median) {np.median(dXi) / 2.998e8 ** 2:.1e} c^2")
    N7[f] = out
check("N7", all(len(N7[f]) == 2 for f in FOOTS), "computed", "computed", "reported quantity (eps_K <= 0.01 = negligible)")
RES["numbers"]["N7"] = N7
P(f"   [peak RSS so far {rss_gb():.2f} GB, {time.time() - T0:.0f} s]")

# =====================================================================================================================
rss = rss_gb()
check("N8", rss < 1.0, f"{rss:.3f} GB", "< 1 GB", "peak RSS")
npass = sum(v_["ok"] for v_ in CHK.values())
P(f"\nU1_V3_DUST_CONTENT COMPLETE: {npass}/{len(CHK)} checks PASS.  ({time.time() - T0:.0f} s, peak RSS {rss:.2f} GB)")
RES["checks"] = CHK
RES["runtime_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, f"u1_v3_dust_content_results{SFX}.json"), "w"), indent=1, default=lambda o: o if not isinstance(o, np.generic) else o.item())
open(os.path.join(HERE, f"u1_v3_dust_content{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
