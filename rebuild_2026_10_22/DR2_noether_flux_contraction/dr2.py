#!/usr/bin/env python3
"""DR2 (FROZEN_CRITERIA.md 6c46933963): does a shift-symmetric charge flux forbid Blumenthal pile-up?
S1-S6 sympy, N1-N4 Newtonian toys, K checks, labels. DR2_MUTATE=1: separate outputs, must fail."""
import os, json, math, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import erf
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUT = os.environ.get("DR2_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = []; R = {"frozen": "6c46933963", "mutate": MUT, "checks": {}}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def chk(k, ok, msg=""): R["checks"][k] = bool(ok); P(f"  {k}: {'PASS' if ok else 'FAIL'} {msg}")
# ---------------- S1-S6
P("=== S: analytic")
t, r = sp.symbols("t r", positive=True); A = sp.Function("A")(t, r); B = sp.Function("B")(t, r); ph = sp.Function("phi")(t, r)
th = sp.Symbol("theta", positive=True); fi = sp.Symbol("varphi"); co = [t, r, th, fi]
g = sp.diag(-sp.exp(2 * A), sp.exp(2 * B), r ** 2, r ** 2 * sp.sin(th) ** 2); gi = g.inv()
def Gam(a, b, c): return sum(gi[a, d] * (sp.diff(g[d, b], co[c]) + sp.diff(g[d, c], co[b]) - sp.diff(g[b, c], co[d])) for d in range(4)) / 2
sqg = sp.exp(A + B) * r ** 2 * sp.sin(th)
dph = [sp.diff(ph, x) for x in co]; X = -sum(gi[i, i] * dph[i] ** 2 for i in range(4)) / 2; Q = sp.sqrt(2 * X)
# S1: Euler-Lagrange equals the conservation law, on explicit P
mu, n_s = sp.symbols("mu n", positive=True); pht, phr = sp.symbols("pht phr", real=True)
X_f = (sp.exp(-2 * A) * pht ** 2 - sp.exp(-2 * B) * phr ** 2) / 2
s1 = True
for Pf in (lambda x: x ** 2, lambda x: mu ** 2 * (sp.sqrt(2 * x) - 1) ** 2):
    Lg = sqg * Pf(X_f); PX = sp.diff(Pf(sp.Symbol("x", positive=True)), sp.Symbol("x", positive=True)).subs(sp.Symbol("x", positive=True), X_f)
    res_t = sp.simplify(sp.diff(Lg, pht) - sqg * PX * sp.exp(-2 * A) * pht); res_r = sp.simplify(sp.diff(Lg, phr) + sqg * PX * sp.exp(-2 * B) * phr)
    s1 &= (res_t == 0 and res_r == 0)
chk("S1 EL momenta = sqrt(-g) J^m, J^m = -P_X g^{mn} d_n phi; EOM is d_t(sqrt(-g)J^t)+d_r(sqrt(-g)J^r)=0", s1, "(continuity: flux = -dN/dt, not a constant)")
# S3: exact acceleration identity
u_lo = [-d / Q for d in dph]; u_up = [gi[i, i] * u_lo[i] for i in range(4)]
sgn = -1 if MUT else 1
def cov_u(m, n): return sp.diff(u_lo[m], co[n]) - sgn * sum(Gam(l, m, n) * u_lo[l] for l in range(4))
lnQ = sp.log(Q); s3 = []
pt_ = {A: sp.sin(r) * t / 7 + r ** 2 / 50, B: sp.cos(t) * r / 9, ph: 1.3 * t + sp.sin(r + t) / 5}
for m in (0, 1):
    a = sum(u_up[n] * cov_u(m, n) for n in range(2)); hdQ = sum(((1 if m == n else 0) + u_lo[m] * u_up[n]) * sp.diff(lnQ, co[n]) for n in range(2))
    ex = (a + hdQ).subs(pt_).doit(); vals = [abs(float(ex.subs({t: tv, r: rv, th: 1.1}).evalf())) for tv, rv in ((0.3, 0.9), (1.1, 0.4), (0.7, 1.7))]; s3 += vals
    # exact simplification as well
    s = sp.simplify(a + hdQ); P(f"  S3 m={m}: symbolic residual {s if not MUT else '(mutated)'}; numeric {max(vals):.2e}")
    R[f"S3_sym_{m}"] = str(s)[:80]
chk("S3 u^n nabla_n u_m = -h_m^n d_n ln Q, general spherical metric", max(s3) < 1e-10)
# dust limit
Qs, nn, gradn = sp.symbols("Q n gradn", positive=True); K = mu ** 2 * (Qs - 1) ** 2; Qn = 1 + nn / (2 * mu ** 2)
acc = gradn / (2 * mu ** 2) / Qn; lim = sp.limit(acc, mu, sp.oo); cs2 = sp.simplify((sp.diff(K, Qs) / (Qs * sp.diff(K, Qs, 2)))); w = sp.simplify(K / (Qs * sp.diff(K, Qs) - K))
chk("S3b K=mu^2(Q-1)^2 at fixed n, mu->inf: |grad ln Q| -> 0, geodesic", lim == 0, f"c_s^2 = {cs2}, w = {w}")
P("  Static: phi = Q0 t gives Q = Q0 exp(-A), so a_r = A' = dPhi/dr (holding force). Q e^{Phi} uniform needs Q-1 ~ |Phi| ~ 1e-6, so grad ln Q = -grad Phi is not -> 0: a static fluid in a gradient is NOT the dust limit.")
# S2
C, Csym = sp.symbols("C Csym"); Ar = sp.Function("Ar")(r); Br = sp.Function("Br")(r); Jr = sp.Function("Jr")(r)
sol = sp.dsolve(sp.Eq(sp.diff(sp.exp(Ar + Br) * r ** 2 * Jr, r), 0), Jr).rhs; C1_ = list(sol.free_symbols - {r})[0]
reg = sp.limit((sol * r ** 2 * sp.exp(Ar + Br)).subs({Ar: 0, Br: 0}).doit(), r, 0)
chk("S2 static: sqrt(-g) J^r = C; finite J^r at r=0 forces C=0", sp.simplify(reg - C1_) == 0, "flux at r->0 equals C, integral of div J over a ball = 4 pi C, so C != 0 needs a source at the centre; then P_X g^{rr} chi' = 0")
# S4
GM, rr_, Cf, E = sp.symbols("GM rr Cf E", positive=True); v = sp.sqrt(2 * GM / rr_); nS4 = Cf / (4 * sp.pi * rr_ ** 2 * v)
chk("S4 C != 0: n = C/(4 pi r^2 v); point mass, E=0: rho ~ r^-3/2", sp.simplify(sp.diff(sp.log(nS4), rr_) * rr_) == sp.Rational(-3, 2), "(sink at centre)")
# S5
a_, Nn, x_ = sp.symbols("a N x", positive=True); s = sp.Function("s")(t); F = sp.Function("F")
n1 = Nn * sp.exp(-rr_ / a_) / (8 * sp.pi * a_ ** 3); n2 = Nn * sp.exp(-rr_ / (a_ / 3)) / (8 * sp.pi * (a_ / 3) ** 3)
T1, T2 = [sp.integrate(4 * sp.pi * rr_ ** 2 * q, (rr_, 0, sp.oo)) for q in (n1, n2)]
rt = sp.Symbol("rt", positive=True); hom = F(rt / s) / s ** 3; vh = sp.diff(s, t) / s * rt
cont = sp.simplify(sp.diff(hom, t) + sp.diff(rt ** 2 * hom * vh, rt) / rt ** 2)
chk("S5 same charge, different radial law, C=0 both; homologous n = F(r/s(t))/s^3, v = s'r/s solves continuity for ANY s(t)", sp.simplify(T1 - T2) == 0 and cont == 0, f"central density ratio n2/n1 = {sp.simplify(n2 / n1).subs(rr_, 0)}; charge exact, any compression allowed")
# S6
Jp = sp.Symbol("Jp"); KB, K2, Q0, Gt, rho = sp.symbols("K_B K_2 Q0 Gt rho", positive=True); chip, Psip, Phip, Psi, chid = sp.symbols("chip Psip Phip Psi chid"); Jf = sp.Function("J")
y = chip ** 2; Lst = 2 * Phip ** 2 - 4 * Phip * Psip + KB * Psip ** 2 + 2 * (2 - KB) * Psip * chip - (2 - KB) * chip ** 2 - (2 - KB) * Jp * y + K2 * (chid - Q0 * Psi) ** 2 - 16 * sp.pi * Gt * rho * Psi
fl2 = sp.simplify(sp.diff(Lst, chip) / (2 * (2 - KB)))  # chain rule: J(y) with J'(y) = Jp at this point
s6sol = sp.solve(fl2, Psip)[0]; P(f"  S6 chi flux / 2(2-K_B) = {fl2}; C=0 gives Psi' = {sp.simplify(s6sol)} (no rho in it: the algebraic law relation)")
J0 = sp.diff(Lst, chid); P(f"  S6 J^0 = dL/d(chi_t) = {J0}; static chi_t=0: {J0.subs(chid, 0)} (set locally by Psi, deeper well more charge; AeST's Q0 is dphi/dt, NOT a flux constant)")
chk("S6 AeST: static C=0 flux is the algebraic law, contains no rho; J^0 ~ K_2 Q0 Psi", not fl2.has(rho) and sp.simplify(s6sol - (1 + Jp) * chip) == 0 and J0.subs(chid, 0).has(Psi))
# ---------------- numerics
G = 4.30091e-6; KMS = 1.02271e-3  # kpc (km/s)^2/Msun; kpc/Myr per km/s
GK = G * KMS ** 2  # kpc^3 / Msun / Myr^2
M200, R200, CC, Md, Rd = 1e12, 200.0, 10.0, 6.7187942657e10, 3.565; RDG = np.array([1, 2, 3, 4, 6, 8, 10.0]); RR = RDG * Rd; F_ = Md / (M200 - Md)
mnfw = lambda x: (np.log(1 + x) - x / (1 + x)) / (np.log(1 + CC) - CC / (1 + CC)); Mn = lambda r: M200 * mnfw(np.asarray(r) * CC / R200); Mbf = lambda r: Md * (1 - Rd / np.sqrt(np.asarray(r) ** 2 + Rd ** 2))
_x39 = open(os.path.join(REB, "X39_baryonic_contraction", "x39_contraction.py")).read(); CN = dict(np=np, SGN=1.0); exec(_x39[_x39.index("def contract(r, Mb, M0, F, gnedin=None):"):_x39.index('P("\\n=== checks")')], CN)
rg = np.geomspace(1e-5, R200, 6000); M0g = (1 - Md / M200) * Mn(rg)
def blum_mine(rg, M0g):
    rf = np.array([brentq(lambda y: y * (Mbf(y) + m) - x * m * (1 + F_), 1e-8, 1e4, xtol=1e-14, rtol=1e-13) for x, m in zip(rg, M0g)]); o = np.maximum.accumulate(rf); return np.interp(np.log(rg), np.log(o), M0g, left=0.0, right=M0g[-1])
Mx, cv, cr = CN["contract"](rg, Mbf(rg), M0g, F_); Mm = blum_mine(rg, M0g)
M0r = np.interp(np.log(RR), np.log(rg), M0g); QB = np.interp(np.log(RR), np.log(rg), Mx) / M0r; Qm = np.interp(np.log(RR), np.log(rg), Mm) / M0r
chk("K1 own Blumenthal vs X39 contract", np.max(np.abs(QB - Qm)) <= 1e-6, f"max |d| {np.max(np.abs(QB - Qm)):.2e}; Q_B {np.round(QB, 3).tolist()}")
def shells(N, L_frac, T_rel, T_grow, T_hold, dt, eps, Md_on=True, leak=0.0, track=(2 * Rd, 4 * Rd), w=0.3):
    """Spherical shells: r'' = L^2/r^3 - G M_tot(<r) F_soft. M_tot = cold (1 + (1-g)F) + g M_b. Charges m_i constant."""
    edges = np.geomspace(0.1, R200, N + 1); m = (1 - Md / M200) * np.diff(Mn(edges)); m[0] += (1 - Md / M200) * float(Mn(edges[0])); ri = np.sqrt(edges[1:] * edges[:-1]); r = ri.copy(); vr = np.zeros(N)
    Mc_i = (1 - Md / M200) * Mn(ri); L = L_frac * np.sqrt(GK * Mc_i * (1 + F_) * ri ** 4 / (ri * ri + eps * eps) ** 1.5); m0tot = m.sum()
    Nt = int((T_rel + T_grow + T_hold) / dt); g_of = lambda tt: (lambda s: s * s * (3 - 2 * s))(np.clip((tt - T_rel) / T_grow, 0, 1)) if Md_on else 0.0
    def acc(r, g):
        o = np.argsort(r); Mc = np.empty(N); Mc[o] = np.cumsum(m[o]) - 0.5 * m[o]; Mt = Mc * (1 + (1 - g) * F_) + g * Mbf(r)
        return L ** 2 / r ** 3 - GK * Mt * r / (r * r + eps * eps) ** 1.5
    a = acc(r, 0.0); hist = []; acc0 = np.zeros(len(RR)); acc1 = np.zeros(len(RR)); n0 = n1 = 0; t_av = 5000.0 if L_frac < 1 else 500.0; bad = 0.0; every = max(1, int(20 / dt))
    def smooth(r, rc): return (m * 0.5 * (1 - erf((r - rc) / (np.sqrt(2) * w)))).sum()
    def flux(r, v, rc): return (m * np.exp(-0.5 * ((r - rc) / w) ** 2) / (np.sqrt(2 * np.pi) * w) * v).sum()
    prev = None
    for i in range(Nt):
        tt = i * dt; vh = vr + 0.5 * dt * a; r = r + dt * vh; neg = r < 0.01
        if neg.any(): r[neg] = 0.02 - r[neg]; vh[neg] = np.abs(vh[neg])
        a = acc(r, g_of(tt + dt)); vr = vh + 0.5 * dt * a
        if leak: m = m * (1 - leak)
        if (i % every) == 0:
            Mn_ = [smooth(r, rc) for rc in track]; Fl = [flux(r, vr, rc) for rc in track]
            hist.append((tt, *Mn_, *Fl))
        if T_rel - t_av <= tt < T_rel and (i % every) == 0: so = np.sort(r); acc0 += np.array([m[np.argsort(r)][so <= x].sum() for x in RR]); n0 += 1
        if tt >= Nt * dt - t_av and (i % every) == 0: so = np.sort(r); acc1 += np.array([m[np.argsort(r)][so <= x].sum() for x in RR]); n1 += 1
    hist = np.array(hist); charge = abs(m.sum() / m0tot - 1)
    Mi = acc0 / n0 if n0 else np.array([m[np.sort(ri) <= x].sum() for x in RR]) ; Mf = acc1 / max(n1, 1)
    # flux identity
    nt = len(track); dN = np.gradient(hist[:, 1:1 + nt], hist[:, 0], axis=0); Fx = hist[:, 1 + nt:]; pk = np.abs(Fx).max(0); res = np.abs(dN + Fx)[2:-2].max(0) / pk
    return dict(Q=(Mf / Mi).tolist(), Mi=Mi.tolist(), charge=float(charge), flux_res=res.tolist(), peak_flux_Msun_Gyr=(pk * 1e3).tolist(), hist=hist, r=r)
t0 = time.time()
if MUT:
    o = shells(800, 1.0, 0.0, 4000.0, 300.0, 0.5, 1.0, leak=1e-3)
    chk("K3 shell charge conserved (<=1e-10)", o["charge"] <= 1e-10, f"{o['charge']:.2e}"); chk("K4 flux identity <= 5% of peak", max(o["flux_res"]) <= 0.05, f"{o['flux_res']}")
    R["all_checks"] = all(R["checks"].values()); P(f"MUTATE done: {sum(R['checks'].values())}/{len(R['checks'])} pass; failing {[k for k, v in R['checks'].items() if not v]}")
    json.dump(R, open(os.path.join(HERE, f"dr2_results{TAG}.json"), "w"), indent=1); open(os.path.join(HERE, f"dr2{TAG}.out"), "w").write("\n".join(OUT) + "\n"); raise SystemExit(1)
# N1 field vs geodesic, fixed potential (NFW total, softened, baryons at their final mass), rest start, n uniform
P("=== N1 pressureless single-stream field vs geodesic shells")
eps1 = 1.0; Mt1 = lambda r: Mn(r) * (1 - Md / M200) + Mbf(r); gP = lambda r: GK * Mt1(np.abs(r)) * r / (r * r + eps1 * eps1) ** 1.5
r00 = np.linspace(2.0, 60.0, 4001); rs, vs = r00.copy(), np.zeros_like(r00)
def geo(tend, dt=0.2):
    rs, vs = r00.copy(), np.zeros_like(r00); tc = None; tt = 0.0; a = -gP(rs)
    while tt < tend:
        v_ = vs + 0.5 * dt * a; rs = rs + dt * v_; a = -gP(rs); vs = v_ + 0.5 * dt * a; tt += dt
        if tc is None and np.any(np.diff(np.abs(rs)) <= 0): tc = tt
    return rs, vs, tc
_, _, tc = geo(3000.0); tcheck = 0.5 * tc; rs, vs, _ = geo(tcheck); P(f"  first caustic of the single stream started 2-60 kpc: t_c = {tc:.0f} Myr (shell crossing; scalar flow not single-valued after this)")
xg = np.linspace(0.05, 62.0, 6001); dx = xg[1] - xg[0]; u = np.zeros_like(xg); n = np.ones_like(xg); tt = 0.0; Ntot0 = (n * xg ** 2).sum(); inner_flux = 0.0
while tt < tcheck:
    dt = min(0.4 * dx / max(np.abs(u).max(), 1e-6), tcheck - tt, 0.2)
    ul, ur = u[:-1], u[1:]; fl_ = np.where(ul > ur, np.where(ul + ur > 0, 0.5 * ul ** 2, 0.5 * ur ** 2), np.where(ul > 0, 0.5 * ul ** 2, np.where(ur < 0, 0.5 * ur ** 2, 0.0)))
    uf = 0.5 * (ul + ur); mf = np.where(uf > 0, n[:-1], n[1:]) * uf * (0.5 * (xg[:-1] + xg[1:])) ** 2
    un = u.copy(); un[1:-1] = u[1:-1] - dt / dx * (fl_[1:] - fl_[:-1]) - dt * gP(xg[1:-1]); n[1:-1] = n[1:-1] - dt / dx * (mf[1:] - mf[:-1]) / xg[1:-1] ** 2; u = un; u[0] = u[1]; u[-1] = u[-2]; n[0] = n[1]; n[-1] = n[-2]; tt += dt
sel = (rs > 3) & (rs < 40); uf_ = np.interp(rs[sel], xg, u); dv = np.abs(uf_ - vs[sel]).max() / np.abs(vs[sel]).max(); nexact = (r00[sel] ** 2 * np.gradient(r00, rs)[sel] / rs[sel] ** 2); nf_ = np.interp(rs[sel], xg, n); dn = np.median(np.abs(nf_ / nexact - 1))
chk("N1 field velocity = geodesic before the caustic (<=1 %); density from charge + Jacobian (<=5 %)", dv <= 0.01 and dn <= 0.05, f"max dv/v {dv:.2e}, median dn/n {dn:.2e}, central piling n(r=3..)/n0 up to {nexact.max():.2f}")
R["N1"] = dict(t_caustic_Myr=tc, dv=dv, dn=float(dn), n_max=float(nexact.max()))
# N2
P("=== N2 circular shells (frozen eps 1 kpc)")
o2 = shells(3000, 1.0, 0.0, 20000.0, 500.0, 0.5, 1.0); nd = shells(3000, 1.0, 0.0, 2000.0, 500.0, 0.5, 1.0, Md_on=False); i234 = [1, 2, 3]
Q2 = np.array(o2["Q"]); ratio = float(np.mean((Q2[i234] - 1) / (QB[i234] - 1)))
P(f"  r/R_d {RDG.tolist()}\n  Q shells {np.round(Q2, 3).tolist()}\n  Q Blum   {np.round(QB, 3).tolist()}\n  mean (Q-1)/(Q_B-1) at 2,3,4 R_d = {ratio:.3f}")
oe = shells(3000, 1.0, 0.0, 20000.0, 500.0, 0.5, 1e-3); Qe = np.array(oe["Q"]); re = float(np.mean((Qe[i234] - 1) / (QB[i234] - 1))); P(f"  reported, eps 0: Q {np.round(Qe, 3).tolist()}, ratio {re:.3f}")
chk("K2 M_d=0 stays Q=1 within 0.01", np.max(np.abs(np.array(nd["Q"]) - 1)) <= 0.01, f"max {np.max(np.abs(np.array(nd['Q']) - 1)):.2e}")
chk("K3 shell charge conserved (<=1e-10)", o2["charge"] <= 1e-10, f"{o2['charge']:.2e}"); chk("K4 flux identity <= 5% of peak", max(o2["flux_res"]) <= 0.05, f"res {np.round(o2['flux_res'], 4).tolist()}")
h = o2["hist"]; mid = np.argmin(np.abs(h[:, 0] - 10000)); end = -1
P(f"  flux 4 pi r^2 J^r at 2 R_d: start {h[5, 3] * 1e3:.3e}, t=10 Gyr {h[mid, 3] * 1e3:.3e}, end {h[end, 3] * 1e3:.3e} Msun/Gyr; at 4 R_d t=10 Gyr {h[mid, 4] * 1e3:.3e}. Not fixed in time, not uniform in r, zero before and after growth.")
R["N2"] = dict(Q=Q2.tolist(), QB=QB.tolist(), ratio=ratio, Q_eps0=Qe.tolist(), ratio_eps0=re, charge=o2["charge"], flux_res=o2["flux_res"], flux_2Rd_mid=float(h[mid, 3] * 1e3), flux_4Rd_mid=float(h[mid, 4] * 1e3))
F4 = ratio >= 0.8 and o2["charge"] <= 1e-10
# N2b
P("=== N2b nearly radial shells (L = 0.1 L_circ), reported, not in a label")
ob = shells(2000, 0.1, 20000.0, 20000.0, 5000.0, 0.25, 1.0); Qb = np.array(ob["Q"]); ob0 = shells(2000, 0.1, 20000.0, 20000.0, 5000.0, 0.25, 1.0, Md_on=False); Qb0 = np.array(ob0["Q"])
Mi = np.array(ob["Mi"]); rb_ = np.geomspace(RR[0] / 30, R200, 1500); M0b = np.exp(np.interp(np.log(rb_), np.log(RR), np.log(Mi))); M0b = np.where(rb_ > RR[-1], Mi[-1] * (M0g[-1] / Mi[-1]) ** ((np.log(rb_) - np.log(RR[-1])) / (np.log(R200) - np.log(RR[-1]))), M0b); Mxb, _, _ = CN["contract"](rb_, Mbf(rb_), M0b, F_); QBb = np.interp(np.log(RR), np.log(rb_), Mxb) / Mi
P(f"  Q radial {np.round(Qb, 3).tolist()}\n  Q no disc control {np.round(Qb0, 3).tolist()}\n  Blumenthal on its relaxed profile {np.round(QBb, 3).tolist()}\n  response Q/control {np.round(Qb / Qb0, 3).tolist()} (the same-time control is the fair baseline: outer shells are still phase-mixing); charge {ob['charge']:.1e}. Flux identity not read here: sampled every 20 Myr against crossing times of that order.")
R["N2b"] = dict(Q=Qb.tolist(), Q_control=Qb0.tolist(), response=(Qb / Qb0).tolist(), QB=QBb.tolist())
# N3 static polytrope
P("=== N3 finite sound speed, K=mu^2(Q-1)^2, static (rho = k^2/(4 pi G) (C-Phi)), R=R200, charge fixed")
Kk = (math.pi / R200) ** 2 / (1 + F_); fG = 4 * math.pi * G; Mc = M200 - Md
rho_b = lambda r: Md * Rd / (4 * math.pi) / (r * r + Rd * Rd) ** 1.5
def prof(th0, with_b):
    def rhs(r, y): return [y[1], -2 / r * y[1] - Kk * y[0] * (1 + (0 if with_b else F_)) - (fG * rho_b(r) if with_b else 0.0), 4 * math.pi * r * r * Kk / fG * y[0]]
    ev = lambda r, y: y[0]; ev.terminal = True; ev.direction = -1
    return solve_ivp(rhs, (1e-4, 5 * R200), [th0, 0.0, 0.0], events=ev, rtol=1e-9, atol=1e-6, dense_output=True)
s0 = prof(1.0, False); th00 = 1.0 * Mc / s0.y[2][-1]; s0 = prof(th00, False)
th1 = brentq(lambda z: prof(z, True).y[2][-1] - Mc, th00 * 0.2, th00 * 30, xtol=1e-3 * th00); s1 = prof(th1, True)
Mi3 = s0.sol(RR)[2]; Mf3 = s1.sol(RR)[2]; Q3 = Mf3 / Mi3; rhoc0, rhoc1 = Kk / fG * th00, Kk / fG * th1; vc0 = math.sqrt(G * (Mi3[4] * (1 + F_)) / RR[4]); vc1 = math.sqrt(G * (Mf3[4] + Mbf(RR[4])) / RR[4]); M3b, _, _ = CN["contract"](rg, Mbf(rg), np.maximum(s0.sol(np.minimum(rg, s0.t[-1]))[2], 1e-3), F_); QB3 = np.interp(np.log(RR), np.log(rg), M3b) / Mi3
P(f"  radius initial {s0.t[-1]:.1f}, final {s1.t[-1]:.1f} kpc; central density response rho_c,f/rho_c,i = {rhoc1 / rhoc0:.4f}; Q(r) {np.round(Q3, 4).tolist()}; Blumenthal on same start {np.round(QB3, 3).tolist()}\n  v_c at 6 R_d, cold plus baryon: {vc0:.0f} -> {vc1:.0f} km/s; cold charge in r<10 R_d: {Mf3[-1]:.3e} Msun")
P(f"  sound speed at the centre, c_s^2 = Q-1 = C-Phi in (km/s)^2: {math.sqrt(th00):.0f} -> {math.sqrt(th1):.0f} km/s; w = (Q-1)/(Q+1) = {th00 / 2 / 299792.458 ** 2:.1e} -> {th1 / 2 / 299792.458 ** 2:.1e}: w ~ 0 holds, yet this fluid is hydrostatic, so w does not separate dust from a held fluid")
R["N3"] = dict(c_s_i=math.sqrt(th00), c_s_f=math.sqrt(th1), rho_c_ratio=rhoc1 / rhoc0, Q=Q3.tolist(), QB=QB3.tolist(), R_i=float(s0.t[-1]), R_f=float(s1.t[-1]))
# N4 steady flow
P("=== N4 C != 0 steelman: steady inflow")
V = 220.0; r8 = 8.0; v_in = V * math.sqrt(2 * math.log(R200 / r8)); Mdot = V * V * v_in / G; Mdot_Msun_Gyr = Mdot * KMS * 1e3; deliv = Mdot_Msun_Gyr * 10 / M200; rho_need = V * V / (fG * r8 * r8); Mdot_t = M200 / 10.0; rho_t = Mdot_t / (4 * math.pi * r8 * r8 * v_in * KMS * 1e3); tcr = r8 / (v_in * KMS)
def v_at(r, with_b): rs_ = np.geomspace(r, R200, 4000); Mt_ = (M200 - Md) * mnfw(rs_ * CC / R200) + (Mbf(rs_) if with_b else Md * mnfw(rs_ * CC / R200)); return math.sqrt(2 * np.trapz(G * Mt_ / rs_ ** 2, rs_))
vb, va = v_at(r8, False), v_at(r8, True)
P(f"  to hold rho(r)=V^2/(4 pi G r^2) by flow, V 220: Mdot = {Mdot_Msun_Gyr:.3e} Msun/Gyr, independent of r; mass delivered to the sink in 10 Gyr = {deliv:.1f} x M200; drains r<8 kpc in {tcr:.0f} Myr\n  conversely Mdot = M200/10 Gyr gives rho(8 kpc) = {rho_t:.3e} Msun/kpc^3 vs needed {rho_need:.3e} ({rho_t / rho_need:.1e} of it)\n  what survives: at fixed C and r, baryons deepen the well, v {vb:.0f} -> {va:.0f} km/s at 8 kpc, so n falls by {vb / va:.3f}. A real sign, only for a flow with a sink.")
R["N4"] = dict(Mdot_Msun_Gyr=Mdot_Msun_Gyr, delivered_over_M200=deliv, drain_Myr=tcr, rho_ratio=rho_t / rho_need, n_factor=vb / va)
F1 = R["checks"]["S2 static: sqrt(-g) J^r = C; finite J^r at r=0 forces C=0"]; F2 = R["checks"]["S5 same charge, different radial law, C=0 both; homologous n = F(r/s(t))/s^3, v = s'r/s solves continuity for ANY s(t)"]; F3 = R["checks"]["S3 u^n nabla_n u_m = -h_m^n d_n ln Q, general spherical metric"] and R["checks"]["S3b K=mu^2(Q-1)^2 at fixed n, mu->inf: |grad ln Q| -> 0, geodesic"]
allok = all(R["checks"].values()); R["F"] = dict(F1=bool(F1), F2=bool(F2), F3=bool(F3), F4=bool(F4)); R["all_checks"] = bool(allok)
label = "NO VERDICT (failed check)" if not allok else "ARGUMENT FAILS" if ((F1 or F2) and F3 and F4) else "ARGUMENT SURVIVES" if not (F1 or F2 or F4) else "UNCLEAR"
R["label"] = label; P(f"\nF1 {F1} F2 {F2} F3 {F3} F4 {F4}; checks {sum(R['checks'].values())}/{len(R['checks'])}\nVERDICT: {label}. Run {time.time() - t0:.0f} s.")
json.dump(R, open(os.path.join(HERE, f"dr2_results{TAG}.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"dr2{TAG}.out"), "w").write("\n".join(OUT) + "\n")
