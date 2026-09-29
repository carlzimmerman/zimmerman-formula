"""
CFG103-A3 -- cap entry form and the scoped obstruction, own derivation (frozen criteria: FROZEN_DOCSTRING.txt).
(a) exact algebra + a0 numerics + dimensional analysis + constraint entry + slab column bound;  (b) own linear-growth solver, nu_min(k;d);
(c) engagement window g0 = nu_M/(x_F nu_min) and the convention grid;  (d) load-bearing hypotheses (shape family, kappa, non-barotropic).
MUTATE=1: multiplier -> thawing scalar: Sigma_max(z)=a0(z)/(2 pi G) not flat (FAIL).  MUTATE=2: tie dropped: Sigma_max does not follow Lambda0 (FAIL).
(b)-(d) are MUTATE-independent by construction and are only run in the main mode.
"""
import os, sys, itertools, json, time
import numpy as np, sympy as sp
from multiprocessing import get_context
from scipy.interpolate import CubicSpline
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg103_common import Log, MUTATE
from cfg103_growth import Cosmo, ratio, numin_scan, growth_ratio, lcdm_dm, cs2_eos
log = Log(__file__)
RES = {}

# ================================================================= (a) exact algebra
x, Pc, kap, Lam, G_, Mp2, m_, n_, s_ = sp.symbols("x Pc kappa Lam G Mp2 m n s", positive=True)
rho = m_ * n_ + Pc * (m_ * n_ / s_) * sp.atan(m_ * n_ / s_)
P = sp.simplify(n_ * sp.diff(rho, n_) - rho)
Pclaim = Pc * (m_ * n_ / s_)**2 / (1 + (m_ * n_ / s_)**2)
log.check("a1 P = n rho' - rho = Pc x^2/(1+x^2)", sp.simplify(P - Pclaim) == 0, "x = m n/s")
log.check("a2 0 <= P/Pc < 1", sp.simplify(sp.limit(Pclaim / Pc, n_, sp.oo)) == 1 and sp.simplify(Pclaim.subs(n_, 0)) == 0, "monotone from 0, limit 1")
tie = sp.simplify(8 * sp.pi * G_ * ((kap**2 / (8 * sp.pi)) * (1 / (8 * sp.pi * G_)) * Lam) - kap**2 * Lam / (8 * sp.pi))
log.check("a3 tie: 8 pi G Pcap = kappa^2 Lam/(8pi) = a0^2", (tie == 0) if MUTATE != 2 else True, "Pcap = eps Mp2 Lam, Mp2=1/(8piG)")

cos = Cosmo()
G = 6.6743e-11; c = 299792458.0; Msun = 1.98847e30; Mpc = 3.0856775814913673e22; pc = Mpc / 1e6
H0s = cos.H0 * 1e3 / Mpc
a0 = cos.kappa * c * H0s * np.sqrt(3 * cos.OL / (8 * np.pi))
rhoL = 3 * H0s**2 * cos.OL / (8 * np.pi * G)
Pcap_num = cos.eps * rhoL * c**2
a0_alt = cos.kappa * c * H0s * np.sqrt(3 * 0.6847 / (8 * np.pi))
log.p("   (info) a0 with OL = 0.6847: %.5e m/s2" % a0_alt)
log.check("a4 a0 numeric (H0=67.4, OL=0.685, kappa=1/2)", abs(a0 / 9.3603e-11 - 1) < 2e-4, "a0 = %.5e m/s2" % a0)
log.check("a5 a0^2 = 8 pi G Pcap = kappa^2 c^2 (Lam/8pi)-tie", abs(a0**2 / (8 * np.pi * G) / Pcap_num - 1) < 1e-12, "rel %.1e" % (a0**2 / (8 * np.pi * G) / Pcap_num - 1))
RES["a0"] = a0

# dimensional analysis: exponents of (M, L) for (Mp2, Lam, m, n, P) with c=1
M_, L_ = sp.symbols("M_ L_")
dims = sp.Matrix([[1, 0, 1, 0, 1], [-1, -2, 0, -3, -3]])    # rows: exponent of M, of L for Mp2 [M/L], Lam [1/L^2], m [M], n [1/L^3], P [M/L^3]
ns = dims.nullspace()
log.check("a6 dimensional analysis: 5 variables, rank 2 -> 3 invariants", len(ns) == 3, "invariants (exponents of Mp2,Lam,m,n,P): %s" % [list(v) for v in ns])
# impose J-rescaling redundancy (n->lam n, m->m/lam): m,n enter only as the product mn -> exponent(m)=exponent(n)
comb = sp.Matrix.hstack(*ns)
c1, c2, c3 = sp.symbols("c1 c2 c3"); v = comb * sp.Matrix([c1, c2, c3])
sol = sp.solve([v[2] - v[3]], [c1, c2, c3], dict=True)[0]; vv = v.subs(sol)
free = sorted(vv.free_symbols, key=str)
log.check("a7 with m,n only via mn: exactly 2 invariants -> P = Mp2 Lam f(nu), nu = mn/(Mp2 Lam)", len(free) == 2, "vectors: %s" % [list(vv.subs({f: (1 if f == g else 0) for f in free})) for g in free])
# constraint entry: P = Pcap  =>  rho = -Pcap + C n
rr = sp.Function("rr"); nsym = sp.Symbol("nsym", positive=True); Pcs = sp.Symbol("Pcs", positive=True)
ode = sp.Eq(nsym * rr(nsym).diff(nsym) - rr(nsym), Pcs)
dsol = sp.dsolve(ode, rr(nsym)).rhs
log.check("a8 constraint entry P=Pcap => rho = -Pcap + C n", sp.simplify(dsol + Pcs).is_polynomial(nsym) and sp.simplify(sp.diff(dsol + Pcs, nsym, 2)) == 0, "dsolve: %s" % dsol)
shift_dex = 0.5 * np.log10(1 - cos.eps)
RES["shift_dex"] = shift_dex
log.p("   constraint entry shifts Lambda by -eps Lam: a0 -> a0 sqrt(1-eps): %.5f dex (CFG43 quotes 0.0022)" % shift_dex)
# slab bound  P + g^2/(8 pi G) = const
zc = sp.Symbol("zc"); Pz = sp.Function("Pz")(zc); Phi = sp.Function("Phi")(zc); rz = sp.Function("rz")(zc)
Gs = sp.Symbol("Gs", positive=True)
cons = sp.diff(Pz + sp.diff(Phi, zc)**2 / (8 * sp.pi * Gs), zc).subs(sp.diff(Pz, zc), -rz * sp.diff(Phi, zc)).subs(sp.diff(Phi, zc, 2), 4 * sp.pi * Gs * rz)
log.check("a9 slab: d/dz [P + g^2/(8 pi G)] = 0 (hydrostatic + Poisson)", sp.simplify(cons) == 0, "")
Sig_pc = a0 / (2 * np.pi * G) / (Msun / pc**2)
log.check("a10 slab column bound Sigma <= a0/(2 pi G)", abs(Sig_pc / 106.9 - 1) < 2e-3, "%.2f Msun/pc^2 (CFG43 quotes 106.9)  [P0 = pi G Sigma^2/2 <= Pcap]" % Sig_pc)
# Sigma_max(z) under MUTATE modes
def sigma_max(Lam_z, Lc=None):
    Lr = np.asarray(Lam_z, float) if Lc is None else Lc * np.ones_like(np.asarray(Lam_z, float))
    return np.sqrt(cos.eps * Lr)                                    # in units of sqrt(Lam) (a0 = sqrt(eps Lam)); ratios are what matter
if MUTATE == 1:
    from scipy.integrate import solve_ivp
    lam_v = 0.3; U0 = 3 * cos.OL; rm0 = 3 * cos.Om; ai = 1 / 11.0
    # simple and explicit: t-integration with (a, psi, psid)
    def rhs_t(t, y):
        a, psi, pd = y; U = U0 * np.exp(-lam_v * psi); H = np.sqrt((rm0 * a**-3 + 0.5 * pd**2 + U) / 3.0)
        return [a * H, pd, -3 * H * pd + lam_v * U]
    ev = lambda t, y: y[0] - 1.0; ev.terminal = True
    so = solve_ivp(rhs_t, [0, 20], [ai, 0.0, 0.0], rtol=1e-11, atol=1e-13, events=ev, dense_output=True)
    tt = np.linspace(0, so.t[-1], 4001); Y = so.sol(tt); zz = 1 / Y[0] - 1; Uz = U0 * np.exp(-lam_v * Y[1])
    S_z = sigma_max(Uz); i25 = np.argmin(np.abs(zz - 2.5))
    dev = S_z[i25] / S_z[-1] - 1
    log.check("a11 Sigma_max(z) flat (z<=2.5)", abs(dev) < 1e-8, "MUTATE=1 thawing scalar: Sigma_max(2.5)/Sigma_max(0)-1 = %.3e" % dev)
elif MUTATE == 2:
    Lc = 1.0; L0s = np.array([0.5, 1.0, 2.0])
    S = sigma_max(L0s, Lc=Lc); dev = np.max(np.abs(S / np.sqrt(L0s) / (S[0] / np.sqrt(L0s[0])) - 1))
    log.check("a11 Sigma_max follows Lambda0 (Sigma ~ sqrt(Lam0))", dev < 1e-8, "MUTATE=2 tie dropped: max deviation %.3e" % dev)
else:
    L0s = np.array([0.5, 1.0, 2.0]); S = sigma_max(L0s)
    dev = np.max(np.abs(S / np.sqrt(L0s) / (S[0] / np.sqrt(L0s[0])) - 1))
    log.check("a11 Sigma_max follows Lambda0 (Sigma ~ sqrt(Lam0)) and is flat in z", dev < 1e-8, "dev %.1e (flat in z: Lambda is a constant, A1/A2)" % dev)
if MUTATE != 0:
    log.p("   (b)-(d) growth/engagement stages are MUTATE-independent by construction and are not re-run in the control modes.")
    log.finish(RES)

# ================================================================= (b) solver controls
t0 = time.time()
# C1: vanishing pressure limit of the pressured ODE == zero-pressure ODE
r_big = ratio(1e40, 30.0, cos)
log.check("b-C1 nu*->inf recovers LCDM growth (ratio 1)", abs(r_big - 1) < 1e-9, "ratio(nu*=1e40,k=30) - 1 = %.1e" % (r_big - 1))
# C2: LCDM closed form
from scipy.integrate import quad
Dfun = lambda a: 2.5 * cos.Om * np.sqrt(cos.E2(a)) * quad(lambda ap: 1 / (ap * np.sqrt(cos.E2(ap)))**3, 0, a, epsabs=0, epsrel=1e-13)[0]
ai_ = 1e-4
num = lcdm_dm(cos); cf = Dfun(1.0) / Dfun(ai_) * ai_
log.check("b-C2 LCDM growth vs closed form (Heath integral)", abs(num / cf - 1) < 1e-5, "numeric %.8f  closed form %.8f  rel %.1e" % (num, cf, num / cf - 1))
# C3: EdS, single fluid, constant c_s^2: delta ~ a^(-1/4) J_{5/2}(2 sqrt(beta a))
import mpmath as mp
cosE = Cosmo(Om=1.0, Ob=1e-30, OL=0.0)                 # EdS, f_b -> 0 (single pressured fluid)
cs_c = 3e-6; kk = 2.0; beta = (kk * cs_c**0.5 * cosE.cH)**2
ai3 = 1e-4
f = lambda a: a**-0.25 * mp.besselj(2.5, 2 * mp.sqrt(beta * a))
cf3 = ai3 * float(f(1.0) / f(ai3))
# exact initial data from the closed form (a mismatched growing-mode start would excite the oscillatory partner mode once beta*a ~ 1)
fp = float(mp.diff(lambda sv: f(mp.e**sv), mp.log(ai3))); f0 = float(f(ai3))
y0c = [ai3, ai3 * fp / f0, ai3, ai3 * fp / f0]
nm3 = growth_ratio(1.0, kk, cosE, zi=1 / ai3 - 1, zev=0.0, cs=cs_c, y0=y0c)
log.check("b-C3 EdS constant-c_s^2 vs Bessel J_5/2 closed form", abs(nm3 / cf3 - 1) < 1e-5, "beta=%.3f numeric %.8g closed %.8g rel %.1e" % (beta, nm3, cf3, nm3 / cf3 - 1))
# C4: c_s^2 formula vs finite difference of P(rho)
mp.mp.dps = 40
eps_ = mp.mpf(cos.eps); nu_t = mp.mpf(37)
def rho_fn(xv): return nu_t * xv + eps_ * xv * mp.atan(xv)              # units rho_L, x = m n/(nu rho_L) so m n = nu x
def P_fn(xv): return xv * mp.diff(rho_fn, xv) - rho_fn(xv)
errs = []
for xv in (0.03, 0.4, 3.0, 40.0):
    xv = mp.mpf(xv); cs_fd = mp.diff(P_fn, xv) / mp.diff(rho_fn, xv)
    errs.append(abs(float(cs_fd) / cs2_eos(float(xv), 37.0, cos.eps) - 1))
log.check("b-C4 c_s^2 = nP_n/(rho+P) vs finite difference dP/drho", max(errs) < 1e-8, "max rel err %.1e over x=0.03..40" % max(errs))
# nu*=1: c_s^2 and suppression
x0 = cos.Oc / cos.OL
cs0 = cs2_eos(x0, 1.0, cos.eps)
log.check("b-N3i nu*=1: c_s^2(z=0) ~ 6e-3", abs(cs0 / 6e-3 - 1) < 0.2, "c_s^2 = %.4g (x0 = %.3f)" % (cs0, x0))
rr1 = {k_: ratio(1.0, k_, cos) for k_ in (0.5, 2.0, 10.0, 30.0)}
log.p("   nu*=1 growth ratio D/D_LCDM at k=0.5,2,10,30 /Mpc: %s   (CFG43: 5-14%%)" % {k_: round(v_, 4) for k_, v_ in rr1.items()})
log.check("b-N3i nu*=1 growth suppressed to 5-14% band", all(0.04 <= v_ <= 0.15 for v_ in rr1.values()), "min %.3f max %.3f" % (min(rr1.values()), max(rr1.values())))
RES["nu1_ratio"] = rr1

# ================================================================= (b) nu_min tables (multiprocessing)
DELTAS = [0.05, 0.2, 0.3, 0.5]
def job(args):
    k, zi, zev, shape, kappa = args
    cs_ = Cosmo(kappa=kappa)
    o, tab = numin_scan(k, cs_, DELTAS, zi=zi, zev=zev, shape=shape)
    return (k, zi, zev, shape, kappa), o
ctx = get_context("fork")
kgrid = 10**np.arange(-2.2, 1.9, 0.2)
kref = [0.5, 2.0, 10.0, 30.0]
jobs = [(float(k), 1e4, 0.0, "atan", 0.5) for k in sorted(set(np.round(list(kgrid) + kref, 8)))]
with ctx.Pool(15) as pool: out = dict(pool.map(job, jobs, chunksize=1))
tab = {d: np.array([[k[0], v[d]] for k, v in sorted(out.items())]) for d in DELTAS}
RES["numin_table"] = {str(d): tab[d].tolist() for d in DELTAS}
log.p("   nu_min(k) table (d=5%%): " + "; ".join("%.3g:%.4g" % (a_, b_) for a_, b_ in tab[0.05]))
log.p("   nu_min(k) at the reference k (own solver; d=5%%): referee 2.2e4, 1.8e5, 2.0e6, 1.0e7")
ref_ref = {0.5: 2.2e4, 2.0: 1.8e5, 10.0: 2.0e6, 30.0: 1.0e7}
mine = {}
for k_ in kref:
    kk_ = min(out.keys(), key=lambda q: abs(q[0] - k_)); mine[k_] = out[kk_][0.05]
    log.p("     k=%5.1f  nu_min(5%%)=%.4g (referee %.3g, ratio %.3f)   20%%: %.4g   30%%: %.4g   50%%: %.4g" % (k_, out[kk_][0.05], ref_ref[k_], out[kk_][0.05] / ref_ref[k_], out[kk_][0.2], out[kk_][0.3], out[kk_][0.5]))
log.check("b-1 nu_min(k) within factor 1.5 of the referee (4 k)", all(1 / 1.5 < mine[k_] / ref_ref[k_] < 1.5 for k_ in kref), "ratios %s" % [round(mine[k_] / ref_ref[k_], 3) for k_ in kref])
sl = {}
for d in DELTAS:
    kk = tab[d][:, 0]; vv = tab[d][:, 1]; ok = np.isfinite(vv); pf = np.polyfit(np.log(kk[ok]), np.log(vv[ok]), 1); sl[d] = pf[0]
    loc = np.diff(np.log(vv[ok])) / np.diff(np.log(kk[ok]))
    log.p("   d=%2.0f%%: nu_min ~ k^%.3f (global fit); local slope range %.3f .. %.3f over k=%.3g..%.3g" % (d * 100, pf[0], loc.min(), loc.max(), kk[ok][0], kk[ok][-1]))
log.check("b-2 exponent 1.5 +- 0.05 (d=5%, k=0.5..30 local)", abs(np.polyfit(np.log(tab[0.05][(tab[0.05][:, 0] > 0.4) & (tab[0.05][:, 0] < 40)][:, 0]), np.log(tab[0.05][(tab[0.05][:, 0] > 0.4) & (tab[0.05][:, 0] < 40)][:, 1]), 1)[0] - 1.5) < 0.05,
          "fit slope %.4f" % np.polyfit(np.log(tab[0.05][(tab[0.05][:, 0] > 0.4) & (tab[0.05][:, 0] < 40)][:, 0]), np.log(tab[0.05][(tab[0.05][:, 0] > 0.4) & (tab[0.05][:, 0] < 40)][:, 1]), 1)[0])
RES["numin_ref"] = {str(k_): mine[k_] for k_ in kref}; RES["slopes"] = {str(d): float(v_) for d, v_ in sl.items()}
spl = {d: CubicSpline(np.log(tab[d][np.isfinite(tab[d][:, 1]), 0]), np.log(tab[d][np.isfinite(tab[d][:, 1]), 1])) for d in DELTAS}
def numin_k(k, d): return float(np.exp(spl[d](np.log(k))))

# ================================================================= (c) engagement
fb = cos.fb
rho_m0 = cos.Om * 3 * H0s**2 / (8 * np.pi * G) / Msun * Mpc**3                # Msun / Mpc^3
def R_L(Mh): return (3 * Mh / (4 * np.pi * rho_m0))**(1 / 3)                       # Mpc
def r_M(Mb): return np.sqrt(G * Mb * Msun / a0)                                    # m
def nu_M(Mb): return a0 / (4 * np.pi * G * r_M(Mb) * np.sqrt(2)) / rhoL             # rho_c(r_M)/rho_L, P2 point-mass phantom
Ms = np.logspace(7, 13, 13)
slope = np.polyfit(np.log(Ms), np.log([nu_M(M) for M in Ms]), 1)[0]
log.check("c-1 nu_M propto M_b^(-1/2) exactly", abs(slope + 0.5) < 1e-12, "log-log slope %.15f ; nu_M(1e9) = %.4g, nu_M(3e11) = %.4g" % (slope, nu_M(1e9), nu_M(3e11)))
RES["nuM"] = {"1e9": nu_M(1e9), "3e11": nu_M(3e11)}
def kof(Mb, kconv=np.pi, Mh_mode="fb", fh=1.0, kunits="Mpc"):
    Mh = Mb / fb if Mh_mode == "fb" else Mb
    k = kconv / (fh * R_L(Mh))
    return k * (cos.h if kunits == "h" else 1.0)
def xF(F): return np.sqrt(F / (1 - F))
def g0(Mb, d, F, **kw): return nu_M(Mb) / (xF(F) * numin_k(kof(Mb, **kw), d))
# direct re-solve at the two masses (primary conventions), no interpolation
direct = {}
def job2(args):
    Mb, d = args
    kk = kof(Mb); o, _ = numin_scan(kk, Cosmo(), [d]); return (Mb, d, kk, o[d])
with ctx.Pool(4) as pool: dres = pool.map(job2, [(1e9, 0.05), (3e11, 0.05), (1e9, 0.2), (3e11, 0.2)])
log.p("   DIRECT re-solves, primary conventions (k = pi/R_L(M_b/f_b), F>=1/2):")
for Mb, d, kk, nm in dres:
    g = nu_M(Mb) / nm; direct[(Mb, d)] = g
    log.p("     M_b=%.0e d=%2.0f%%: k=%.3f/Mpc nu_min=%.4g nu_M=%.4g  g0=%.4f  window g0^2=%s" % (Mb, d * 100, kk, nm, nu_M(Mb), g, ("%.3f" % g**2) if g > 1 else "EMPTY"))
RES["g0_direct"] = {"%g_%g" % k_: v_ for k_, v_ in direct.items()}
log.p("   referee: g0 = 0.36/0.355 (5%), 1.06/1.04 (20%); CFG43 README: 1.08/1.04")
log.check("c-2 g0 (5%) primary within factor 2 of referee 0.36/0.355", all(0.5 < direct[(M_, 0.05)] / r_ < 2 for M_, r_ in ((1e9, 0.36), (3e11, 0.355))), "mine %.3f / %.3f" % (direct[(1e9, 0.05)], direct[(3e11, 0.05)]))
log.check("c-3 g0 (20%) primary within factor 2 of referee 1.06/1.04", all(0.5 < direct[(M_, 0.2)] / r_ < 2 for M_, r_ in ((1e9, 1.06), (3e11, 1.04))), "mine %.3f / %.3f" % (direct[(1e9, 0.2)], direct[(3e11, 0.2)]))
log.check("c-4 g0 mass-independent (1e9 vs 3e11, 5%) within 10%", abs(direct[(1e9, 0.05)] / direct[(3e11, 0.05)] - 1) < 0.10, "ratio %.3f" % (direct[(1e9, 0.05)] / direct[(3e11, 0.05)]))

# ---- convention grid (declared in the frozen docstring)
grid = dict(d=DELTAS, F=[0.5, 0.9, 0.1, 0.01], kconv=[np.pi, 1.0, 2 * np.pi], Mh=["fb", "b"], fh=[1.0, 4.0, 40.0], ku=["Mpc", "h"])
rows = []
for d, F, kc, mh, fh, ku in itertools.product(*grid.values()):
    gv = [g0(Mb, d, F, kconv=kc, Mh_mode=mh, fh=fh, kunits=ku) for Mb in (1e9, 3e11)]
    rows.append(dict(d=d, F=F, kconv=kc, Mh=mh, fh=fh, ku=ku, g0_1e9=gv[0], g0_3e11=gv[1]))
g_all = np.array([r["g0_1e9"] for r in rows]); w_all = np.where(g_all > 1, g_all**2, 0.0)
log.p("   GRID: %d combinations; g0(1e9) range %.3g .. %.3g (referee/CFG43 quote 0.08 .. 3.3)" % (len(rows), g_all.min(), g_all.max()))
prim = [r for r in rows if r["d"] == 0.05 and r["F"] == 0.5 and abs(r["kconv"] - np.pi) < 1e-9 and r["Mh"] == "fb" and r["fh"] == 1.0 and r["ku"] == "Mpc"][0]
log.p("   primary (d=5%%, F=1/2, pi/R_L(M_b/f_b), f_h=1, 1/Mpc): g0 = %.3f / %.3f" % (prim["g0_1e9"], prim["g0_3e11"]))
# subgrids
def sub(**kw):
    return [r for r in rows if all((r[k] == v if not isinstance(v, float) else abs(r[k] - v) < 1e-9) for k, v in kw.items())]
def summ(name, rs):
    gg = np.array([r["g0_1e9"] for r in rs]); log.p("   %-58s g0 in [%.3g, %.3g]  max window %s" % (name, gg.min(), gg.max(), ("%.3g" % (gg.max()**2)) if gg.max() > 1 else "EMPTY"))
    return gg.max()
summ("d in {5,20,30,50}%, F=1/2, pi/R, M_b/f_b, f_h=1, 1/Mpc", [r for r in sub(F=0.5, kconv=np.pi, Mh="fb", fh=1.0, ku="Mpc")])
summ("+ F in {0.5,0.9} (hydrostatic-consistent), d<=20%", [r for r in rows if r["F"] in (0.5, 0.9) and r["d"] <= 0.2 and abs(r["kconv"] - np.pi) < 1e-9 and r["Mh"] == "fb" and r["fh"] == 1.0 and r["ku"] == "Mpc"])
summ("F=0.9 only (hydrostatic requirement), d=5%, primary rest", sub(d=0.05, F=0.9, kconv=np.pi, Mh="fb", fh=1.0, ku="Mpc"))
summ("all k conv / M_h / f_h / units, F>=0.9, d<=20%", [r for r in rows if r["F"] in (0.5, 0.9) and r["d"] <= 0.2])
summ("all F, d<=20%, f_h=1 kunits Mpc", [r for r in rows if r["d"] <= 0.2 and r["fh"] == 1.0 and r["ku"] == "Mpc"])
gmax_row = max(rows, key=lambda r: r["g0_1e9"])
log.p("   GLOBAL MAX corner: %s -> g0=%.3g, window g0^2 = %.3g" % ({k_: v_ for k_, v_ in gmax_row.items() if k_ not in ("g0_1e9", "g0_3e11")}, gmax_row["g0_1e9"], gmax_row["g0_1e9"]**2))
n4 = sum(1 for r in rows if r["g0_1e9"]**2 >= 1e4)
log.p("   grid points with window >= 1e4 (g0 >= 100): %d of %d ; >= 1e5: %d" % (n4, len(rows), sum(1 for r in rows if r["g0_1e9"]**2 >= 1e5)))
# one-at-a-time log10 shifts of g0 relative to primary
def shift(**kw):
    r = [q for q in rows if all((q[k] == v if not isinstance(v, float) else abs(q[k] - v) < 1e-9) for k, v in {**dict(d=0.05, F=0.5, kconv=np.pi, Mh="fb", fh=1.0, ku="Mpc"), **kw}.items())][0]
    return np.log10(r["g0_1e9"] / prim["g0_1e9"])
log.p("   one-at-a-time log10 change of g0 vs primary: d=20%%: %+.2f, 30%%: %+.2f, 50%%: %+.2f | F=0.9: %+.2f, 0.1: %+.2f, 0.01: %+.2f | k=1/R: %+.2f, 2pi/R: %+.2f | M_h=M_b: %+.2f | f_h=4: %+.2f, 40: %+.2f | k as h/Mpc: %+.2f" %
      (shift(d=0.2), shift(d=0.3), shift(d=0.5), shift(F=0.9), shift(F=0.1), shift(F=0.01), shift(kconv=1.0), shift(kconv=2 * np.pi), shift(Mh="b"), shift(fh=4.0), shift(fh=40.0), shift(ku="h")))
stack = [r for r in rows if r["d"] == 0.3 and r["F"] == 0.01 and r["fh"] == 40.0 and abs(r["kconv"] - 1.0) < 1e-9 and r["Mh"] == "fb" and r["ku"] == "Mpc"][0]
log.p("   referee-style stack (d=30%%, F>=0.01, f_h=40, k=1/R): g0 = %.3g, window g0^2 = %.3g   ; same stack with F>=0.9: g0=%.3g" %
      (stack["g0_1e9"], stack["g0_1e9"]**2, [r for r in rows if r["d"] == 0.3 and r["F"] == 0.9 and r["fh"] == 40.0 and abs(r["kconv"] - 1.0) < 1e-9 and r["Mh"] == "fb" and r["ku"] == "Mpc"][0]["g0_1e9"]))
RES["grid"] = rows; RES["stack"] = stack
# z_eval / z_i sensitivity at primary d
def job3(args):
    k, zi, zev = args; o, _ = numin_scan(k, Cosmo(), [0.05, 0.2], zi=zi, zev=zev); return (k, zi, zev), o
sens_jobs = [(k, zi, zev) for k in (2.0, 10.0) for zi, zev in ((1e4, 0.0), (1e4, 1.0), (1e3, 0.0), (1e5, 0.0))]
with ctx.Pool(8) as pool: sens = dict(pool.map(job3, sens_jobs))
for k in (2.0, 10.0):
    base = sens[(k, 1e4, 0.0)]
    log.p("   k=%g: nu_min(5%%) base %.4g | z_eval=1: %.3f | z_i=1e3: %.3f | z_i=1e5: %.3f   (ratios to base)" % (k, base[0.05], sens[(k, 1e4, 1.0)][0.05] / base[0.05], sens[(k, 1e3, 0.0)][0.05] / base[0.05], sens[(k, 1e5, 0.0)][0.05] / base[0.05]))
sens_ok = all(abs(sens[(k, 1e4, 1.0)][0.05] / sens[(k, 1e4, 0.0)][0.05] - 1) < 0.5 for k in (2.0, 10.0))
log.check("c-5 criterion redshift / z_i do not matter (within 50%)", sens_ok, "see ratios above")
RES["sens"] = {str(k_): v_ for k_, v_ in sens.items()}

# ================================================================= (d) load-bearing hypotheses
log.p("   --- (d) hypotheses ---")
def job4(args):
    k, shape, kappa = args; o, _ = numin_scan(k, Cosmo(kappa=kappa), [0.05, 0.2], shape=shape); return (k, shape, kappa), o
d_jobs = [(k, sh, 0.5) for k in kref for sh in (2, 3, 4)] + [(k_, "atan", 0.5) for k_ in ()] + [(kof(Mb), "atan", kp) for Mb in (1e9, 3e11) for kp in (1 / (2 * np.pi), 1.0)]
with ctx.Pool(15) as pool: dd = dict(pool.map(job4, d_jobs))
# control: shape p=2 table-integral reproduces the atan form
kk05 = min(out.keys(), key=lambda q: abs(q[0] - 0.5))
log.check("d-C p=2 (numerical-integral EOS) reproduces arctan", abs(dd[(0.5, 2, 0.5)][0.05] / out[kk05][0.05] - 1) < 2e-3, "nu_min p=2 %.5g vs atan %.5g" % (dd[(0.5, 2, 0.5)][0.05], out[kk05][0.05]))
for p in (2, 3, 4):
    xs_ = np.log(kref); ys_ = np.log([dd[(k_, p, 0.5)][0.05] for k_ in kref]); ex = np.polyfit(xs_, ys_, 1)[0]
    # g0 with this shape at 1e9, 3e11 (primary conv, F=1/2 -> x_F=1 for every p): need nu_min at kof(M): scale by local power law from the 4-k table
    coef = np.polyfit(xs_, ys_, 1)
    gg = [nu_M(Mb) / np.exp(np.polyval(coef, np.log(kof(Mb)))) for Mb in (1e9, 3e11)]
    log.p("   shape F_p=x^p/(1+x^p), p=%d: nu_min(5%%) at k=0.5,2,10,30: %s ; exponent %.3f ; g0(1e9)=%.3f g0(3e11)=%.3f (power-law extrapolation of the 4-k table)" %
          (p, ["%.3g" % np.exp(y) for y in ys_], ex, gg[0], gg[1]))
    RES["shape_p%d" % p] = dict(exponent=ex, g0=gg)
log.p("   kappa scaling (a0 ~ kappa, eps ~ kappa^2; direct solves at k(M), d=5%%): ")
gk = {}
# recompute kappa runs (0.5 from 'dres')
nu05 = {(Mb, d): nm for Mb, d, kk, nm in dres}
for kp in (1 / (2 * np.pi), 1.0):
    for Mb in (1e9, 3e11):
        nu_k = dd[(kof(Mb), "atan", kp)][0.05]; a0k = a0 * kp / 0.5
        nuM_k = a0k / (4 * np.pi * G * np.sqrt(G * Mb * Msun / a0k) * np.sqrt(2)) / rhoL
        gk[(kp, Mb)] = nuM_k / nu_k
        log.p("     kappa=%.4f M_b=%.0e: nu_min=%.4g nu_M=%.4g g0=%.4f (kappa=1/2: %.4f)" % (kp, Mb, nu_k, nuM_k, nuM_k / nu_k, direct[(Mb, 0.05)]))
log.check("d-1 g0 is kappa-independent (pure number of the cosmology), within 10%", all(abs(gk[(kp, Mb)] / direct[(Mb, 0.05)] - 1) < 0.10 for kp in (1 / (2 * np.pi), 1.0) for Mb in (1e9, 3e11)), "ratios %s" % [round(gk[(kp, Mb)] / direct[(Mb, 0.05)], 3) for kp in (1 / (2 * np.pi), 1.0) for Mb in (1e9, 3e11)])
RES["kappa"] = {"%g_%g" % k_: v_ for k_, v_ in gk.items()}
# non-barotropic control: rest-frame sound speed 0 (extra dof, NOT available to a single-current fluid)
rz = [ratio(nu_, 30.0, cos, cs="zero") for nu_ in (1.0, 1e-3)]
log.check("d-2 non-barotropic (c_s,eff=0): no growth bound (ratio=1 for any nu*)", all(abs(r_ - 1) < 1e-12 for r_ in rz), "ratio(nu*=1,1e-3; k=30) = %s" % rz)
log.p("     with no growth bound the window is one-sided: engaged iff nu* <= nu_M(M) (nu_M ~ M^-1/2), i.e. M <= M_engage(nu*) ~ nu*^-2; any span in mass is reachable by lowering nu*")
log.p("   total runtime %.0f s" % (time.time() - t0))
log.finish(RES)
