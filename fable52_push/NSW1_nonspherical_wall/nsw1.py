#!/usr/bin/env python3
"""NSW1 (non-spherical wall): driver. Criteria 052f87daad (FROZEN_CRITERIA.md), amendment A1 0dfa03d257 (AMENDMENT_A1.md). TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.

    python3 nsw1.py                 -> nsw1.json / nsw1.out          (known answers, graded cases, B3, labels)
    python3 nsw1.py --mutate M1     -> nsw1_MUTATE_M1.json / .out    (M1 | M2 | M3 | M4)

One thread. Checkpoints after every graded case (nsw1_ckpt.json) and yields on SIGTERM; a restart resumes from the checkpoint.
Units inside: lengths r_M = sqrt(G M_b / a0), fields a0, masses M_b. In these units the spheroid family does not depend on the
footing; the footings enter through the frozen lines, the physical sizes and B3's exterior pressure.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
import sys, json, math, time, signal, warnings
import numpy as np
from scipy.optimize import brentq
warnings.filterwarnings("ignore", message=".*encountered in matmul")     # spurious on this BLAS; results are checked by the known answers
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nsw1_solver as S

MUT = sys.argv[sys.argv.index("--mutate") + 1] if "--mutate" in sys.argv else None
TAG = f"_MUTATE_{MUT}" if MUT else ""
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()
STOP = {"flag": False}
def _term(sig, frm): STOP["flag"] = True
signal.signal(signal.SIGTERM, _term)

# ------------------------------------------------------------------ constants (transcribed from swt1.py)
G, MS, PC = 6.6743e-11, 1.98847e30, 3.0856775814913673e16
MPC, KPC = 1e6 * PC, 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
OB, OD, H0 = 0.0215, 0.11958060485606123, 65.0
RHOC = 3 * (H0 * 1e3 / MPC) ** 2 / (8 * math.pi * G); RHO_D0 = OD / (H0 / 100) ** 2 * RHOC
LINE_F = {"canonical": 3.8, "alt": 4.9}; LINE_C = {"canonical": 10.9, "alt": 11.2}
KIDS = (9.4, 10.45, 10.7, 10.9)
QS = (0.2, 0.35, 0.5, 0.7, 1.0, 1.4, 2.0, 3.0); AS = (3.0, 10.0, 30.0, 100.0); RDS = (0.1, 0.3, 1.0)
PROD = (96, 0.03); FINE = (144, 0.02)                                   # (M, ds): production grid and the KA8 refinement
EDGES = 10 ** np.arange(-1.0, 3.0001, 0.05)                              # annuli of 0.05 dex from 0.1 r_M
MID = np.sqrt(EDGES[1:] * EDGES[:-1])
R_FAR = 3000.0                                                           # law-everywhere references reach at least this far

RES = dict(lane="NSW1", criteria="052f87daad", amendment_A1="0dfa03d257", mutate=MUT, KA={}, cases={}, B3={}, labels={})


# ------------------------------------------------------------------ references on spheres (closed forms)
_rl, _ml, _ml0 = S.law_shells(1e7)
_, DS_LAW = S.delta_sigma(EDGES, _rl, _ml, _ml0)
def sphere_reach(Rs):
    r, m, m0 = S.sphere_shells(Rs); _, ds = S.delta_sigma(EDGES, r, m, m0)
    return S.reach(MID, ds / DS_LAW)
RS_TAB = 10 ** np.linspace(-0.2, 2.9, 125)                              # reach up to about 520 r_M, inside the annuli
RLEN_TAB = np.array([sphere_reach(x) for x in RS_TAB])
def sphere_of_reach(Rlen):
    """radius of the spherical wall around point baryons whose lensing reach is Rlen (the table is monotone; checked below)."""
    return float(math.exp(np.interp(math.log(Rlen), np.log(RLEN_TAB), np.log(RS_TAB))))
def F_sph(Rs): y = 1.0 / Rs ** 2; return float(S.Wsph(S.u_in(y)) / y)
def Va_sph(Rs): return 4 * math.pi / 3 * Rs ** 3 * abs(S.alpha_law_y(1.0 / Rs ** 2))


# ------------------------------------------------------------------ solves
def solve_point(geom, M, ds, ext="conf", **kw):
    amax = float(np.max(geom.coef(np.linspace(-1, 1, 201))["Xabs"]))
    b = S.Bubble(geom, S.s_grid(min(1e-3, 1e-2 * amax) / amax, ds), M=M, ext=ext, **kw)
    b.solve(S.initial_guess(b)); return b

def solve_disc(geom, Rd, M, ds, ext="conf", with_ref=True):
    """a disc inside the wall, and the law-everywhere reference for the same disc on the same lattice extended to R_FAR."""
    cc = geom.coef(np.linspace(-1, 1, 201)); amax, amin = float(np.max(cc["Xabs"])), float(np.min(cc["Xabs"]))
    s = S.s_grid(0.01 * Rd / amax, ds); dse = s[1] - s[0]
    b = S.Bubble(geom, s, M=M, ext=ext, point=False)
    b.mass, fout = S.expdisc_mass(b, Rd, 0.1 * Rd); b.solve(S.initial_guess(b))
    if not with_ref: return b, None, fout, 1.0
    K = int(math.ceil(math.log(R_FAR / amin) / dse)); f = math.exp(K * dse)
    sr = np.concatenate([s - K * dse, (np.arange(1, K + 1) - K) * dse])
    br = S.Bubble(geom.scaled(f), sr, M=M, ext="far", point=False)
    br.mass, _ = S.expdisc_mass(br, Rd, 0.1 * Rd, rtrunc_m=1.0 / f); br.solve(S.initial_guess(br))
    return b, br, fout, f

def ref_signal(br, f, geom):
    """orientation-averaged lensing signal of the law-everywhere reference: the solve inside r_cut, the point law beyond."""
    if br is None: return DS_LAW
    rcut = float(np.min(br.c["Xabs"]))
    r, m, _, mc = br.eff_mass(); keep = r <= rcut
    e = 10 ** np.arange(math.log10(rcut), 7.0001, 1.0 / 400); Me = S.nu(1 / e ** 2)
    rt, mt = np.sqrt(e[1:] * e[:-1]), np.diff(Me)
    inside = float(m[keep].sum() + mc)
    r_all = np.concatenate([r[keep], [rcut], rt]); m_all = np.concatenate([m[keep], [float(Me[0]) - inside], mt])
    return S.delta_sigma(EDGES, r_all, m_all, mc)[1]

def stats(b, geom, a_eq, ds_ref, gref=None, Rmin=0.02):
    """B2's statistics for one converged sharp-wall solve."""
    wq = b.wall(mutate_W=(MUT == "M1"))
    p0, _ = b.response(0); p1, _ = b.response(1)
    Vpar, Vperp = 4 * math.pi / 3 * p0, 4 * math.pi / 3 * p1; Vbar = (Vpar + 2 * Vperp) / 3
    r, m, cth, mc = b.eff_mass()
    _, dsig = S.delta_sigma(EDGES, r, m, mc); ratio = dsig / ds_ref; Rlen = S.reach(MID, ratio)
    Q2 = float(np.sum(m * r * r * 0.5 * (3 * cth * cth - 1))) / a_eq ** 2
    R, gR = b.inplane()
    if gref is None: gref = S.u_in(1.0 / (R * R))
    sel = (R <= 9.0) & (R >= Rmin)
    dev = float(np.max(np.abs(gR[sel] / gref[:len(R)][sel] - 1))) if sel.any() else float("nan")
    Rs = sphere_of_reach(Rlen); V = geom.volume(); Rv = (3 * V / (4 * math.pi)) ** (1 / 3)
    return dict(conv=bool(b.converged), res=float(b.res), M_ext=wq["M_ext"], Q2=Q2, Fn=wq["Fn"], Dil=wq["Dil"], Gamma_w=wq["Gamma_w"],
                col_max=wq["col_max"], d_min=float(wq["d"].min()), d_max=float(wq["d"].max()), et_over_d_max=float(np.max(np.abs(wq["et"]) / wq["d"])),
                d_pole=float(wq["d"][-1]), d_eq=float(0.5 * (wq["d"][b.M // 2] + wq["d"][b.M // 2 - 1])),
                A3b_margin=float(np.min(wq["gout"] - wq["p"])), sqrt_d_flux=float(np.sum(np.sqrt(wq["d"]) * wq["d"] * b.cout["Sarea"] * b.w)
                                                                             / np.sum(wq["d"] * b.cout["Sarea"] * b.w)),
                Va_par=Vpar, Va_perp=Vperp, Va_bar=Vbar, alpha_par=Vpar / V, alpha_perp=Vperp / V, V=V,
                R_len=Rlen, R_sph=Rs, inplane_dev=dev, admissible=bool(a_eq >= 9.0 and dev <= 0.05),
                Gamma_F=wq["Fn"] / F_sph(Rs), Gamma_C=Va_sph(Rs) / abs(Vbar),
                Gamma_F_eqvol=wq["Fn"] / F_sph(Rv), Gamma_C_eqvol=Va_sph(Rv) / abs(Vbar),
                Gamma_F_eqrad=wq["Fn"] / F_sph(a_eq), Gamma_C_eqrad=Va_sph(a_eq) / abs(Vbar),
                wall=dict(mu=b.mu.tolist(), d=wq["d"].tolist(), et=wq["et"].tolist(), p=wq["p"].tolist()))

def run_case(src, q, a, grid):
    M, ds = grid; geom = S.Spheroid(a, q)
    if src == "P":
        b = solve_point(geom, M, ds); st = stats(b, geom, a, DS_LAW)
    else:
        Rd = float(src[1:]); b, br, fout, f = solve_disc(geom, Rd, M, ds)
        _, gref = br.inplane()
        st = stats(b, geom, a, ref_signal(br, f, geom), gref=gref, Rmin=0.05 * Rd)
        st["disc_outside"] = fout; st["ref_conv"] = bool(br.converged)
    return st


# ------------------------------------------------------------------ known answers
def Lz(q):
    if q < 1:
        e = math.sqrt(1 - q * q); return (1 / e ** 2) * (1 - (math.sqrt(1 - e * e) / e) * math.asin(e))
    e = math.sqrt(1 - 1 / q ** 2); return ((1 - e * e) / e ** 2) * ((1 / (2 * e)) * math.log((1 + e) / (1 - e)) - 1)

def smooth_bubble(q, a, wdt, M, ds, nfine, **kw):
    g = S.Spheroid(a, q)
    s = S.s_grid_smooth(1e-3 / (a * max(1, q)), ds, wdt, nfine=nfine)
    b = S.Bubble(g, s, M=M, ext="conf", S_of_m=lambda m: 0.5 * (1 - np.tanh((m - 1) / wdt)), **kw)
    b.solve(S.initial_guess(b)); return b
WIDTHS = (0.04, 0.02, 0.01)
def extrap0(vals): return float(np.polyfit(WIDTHS, vals, 2)[-1])

def quad_J(d, et, n1):
    """integral of J(u(S)) over S from 0 to 1 at fixed (d, et), adaptive quadrature; u(S) from (1 - S / (1 + u)) n = d by root finding.
    No closed form enters."""
    from scipy.integrate import quad
    def f(Sv):
        g = lambda n: (1 - Sv / (1 + math.sqrt(n * n + et * et))) * n - d
        n = d if g(d) >= 0 else brentq(g, d, n1 * (1 + 1e-12) + 1e-300, xtol=1e-300, rtol=1e-15)
        u = math.sqrt(n * n + et * et); return u - math.log1p(u)
    return quad(f, 0.0, 1.0, epsabs=0.0, epsrel=1e-13, limit=2000)[0]

def ka6():
    """A2's closed form against the quadrature of J over S, and against the slab Lagrangian."""
    worst = 0.0; worst_slab = 0.0; rows = []
    for d in 10 ** np.linspace(-3, 2, 5):
        for et in 10 ** np.linspace(-3, 2, 5):
            u, n = S.interior_un(d, et); u, n = float(u), float(n)
            cf = float(S.Wsph(u) if MUT == "M1" else S.Wg(u, n))
            qd = quad_J(float(d), float(et), n)
            # slab: L(X) per unit area = X l_in + (Lbox - X) l_out with l = -|grad Phi|^2 / 2 + S J + d Phi_x, differenced in X
            l_in = -0.5 * (n * n + et * et) + S.Jt(u) + d * n; l_out = -0.5 * (d * d + et * et) + d * d
            X1, X2, Lb = 0.3, 0.7, 1.0
            slab = ((X2 * l_in + (Lb - X2) * l_out) - (X1 * l_in + (Lb - X1) * l_out)) / (X2 - X1)
            worst = max(worst, abs(cf / qd - 1)); worst_slab = max(worst_slab, abs(cf / slab - 1))
            rows.append(dict(d=float(d), et=float(et), closed=cf, quad=qd, slab=float(slab)))
    ok = worst <= 1e-8 and worst_slab <= 1e-5
    P(f"KA6 oblique planar wall, 5 x 5 (d, e_t) from 1e-3 to 1e2: closed form vs quadrature of J dS {worst:.2e} (line 1e-8); "
      f"vs the slab Lagrangian {worst_slab:.2e} (line 1e-5): {'PASS' if ok else 'FAIL'}")
    RES["KA"]["KA6"] = dict(pass_=bool(ok), worst_quad=worst, worst_slab=worst_slab, rows=rows); return ok

def ka1():
    js = json.load(open(os.path.join(HERE, "..", "SWT1_switch_theorems", "swt1.json")))["KA"]["KA_W1"]["rows"]
    worst_nu = worst_p = worst_m = 0.0
    for row in js:
        y = row["y"]; a = 1 / math.sqrt(y)
        b = S.Bubble(S.Spheroid(a, 1.0), S.s_grid(min(1e-3, 1e-2 * a) / a, 0.03), M=16, ext="conf", flux_mutate=(MUT == "M2"))
        b.solve(S.initial_guess(b)); wq = b.wall(mutate_W=(MUT == "M1"))
        Fs, _ = b.faces(b.Phi, newton=True); rf = a * b.mf
        worst_nu = max(worst_nu, float(np.max(np.abs(0.5 * Fs.sum(axis=1) / S.nu(1 / rf ** 2) - 1))))
        worst_p = max(worst_p, float(np.max(np.abs(wq["p"] / row["closed"] - 1)))); worst_m = max(worst_m, abs(wq["M_ext"] - 1))
    vol = {}
    worst_v = 0.0
    if MUT is None:
        for y in (1e-3, 0.1, 1.0):
            a = 1 / math.sqrt(y); F = [smooth_bubble(1.0, a, w_, 8, 0.06, 40.0).volume_force()[0] for w_ in WIDTHS]
            vol[str(y)] = dict(F=F, extrap=extrap0(F), exact=float(S.Wsph(S.u_in(y)) / y)); worst_v = max(worst_v, abs(vol[str(y)]["extrap"] / vol[str(y)]["exact"] - 1))
    okb = worst_nu <= 1e-6 and worst_p <= 1e-8; okc = worst_v <= 2e-4
    P(f"KA1 sphere at swt1.json's six KA_W1 values of y: interior nu(y) {worst_nu:.2e} (line 1e-6); wall pressure (surface route, in "
      f"a0^2 / 4 pi G, the quantity 'closed' holds) {worst_p:.2e} (line 1e-8); exterior mass - 1 {worst_m:.2e}; volume route w -> 0 "
      f"at y 1e-3, 0.1, 1: {worst_v:.2e} (line 2e-4): {'PASS' if (okb and okc) else 'FAIL'} (b, c; part a is taken over every solve at the end)")
    RES["KA"]["KA1"] = dict(pass_bc=bool(okb and okc), worst_nu=worst_nu, worst_p=worst_p, worst_Mext_sphere=worst_m, volume_route=vol)
    return okb and okc, worst_m

def ka2():
    emv = ((3.95e-13, -0.4938), (7.23e-13, -0.4887), (8.35e-13, -0.4870), (9.37e-13, -0.4854),
           (1.20e-12, -0.4815), (1.80e-12, -0.4728), (1.98e-12, -0.4702), (2.14e-12, -0.4679))     # EMV1 RESULT, canonical: g_wall, alpha_law
    w1 = 0.0
    for gw, al in emv:
        u = gw / A0["canonical"]; w1 = max(w1, abs(S.alpha_law_y(u * u / (1 + u)) - al))
    w2 = 0.0; rows = []
    for yw in (1e-4, 1e-3, 1e-2, 0.1, 1.0):
        a = 1 / math.sqrt(yw); b = solve_point(S.Spheroid(a, 1.0), *PROD)
        a0_, a1_ = b.response(0)[0] / a ** 3, b.response(1)[0] / a ** 3; al = S.alpha_law_y(yw)
        rows.append(dict(yw=yw, alpha_m0=a0_, alpha_m1=a1_, alpha_law=al)); w2 = max(w2, abs(a0_ / al - 1), abs(a1_ / al - 1))
    ok = w1 <= 1.5e-4 and w2 <= 1e-3
    P(f"KA2 SWT1's alpha_law (transcribed) vs EMV1 RESULT's eight printed values: {w1:.1e} (printed to 1e-4 from g_wall printed to "
      f"three digits; line 1.5e-4); m = 0 and m = 1 responses of a sphere vs alpha_law at y_w 1e-4 .. 1: {w2:.2e} relative "
      f"(line 1e-3): {'PASS' if ok else 'FAIL'}")
    RES["KA"]["KA2"] = dict(pass_=bool(ok), worst_printed=w1, worst_response=w2, rows=rows); return ok

def ka3():
    wf = wF = 0.0; rows = []
    for q in QS:
        amax = 10 ** -2.5; a = amax / max(1, q)
        b = S.Bubble(S.Spheroid(a, q), S.s_grid(1e-4 / amax, 0.03), M=PROD[0], ext="conf"); b.solve(S.initial_guess(b))
        wq = b.wall(mutate_W=(MUT == "M1")); c = b.c
        GwN = 0.5 * float(np.sum(b.w * c["Sarea"] / c["Xabs"] ** 2))
        dev = float(np.max(np.abs(b.node_u(b.Phi) * (b.m[:, None] * c["Xabs"][None, :]) ** 2 - 1)))
        rows.append(dict(q=q, field_dev=dev, Fn_over_GwN=wq["Fn"] / GwN, Gamma_w=wq["Gamma_w"], Gamma_w_newton=GwN))
        wf = max(wf, dev); wF = max(wF, abs(wq["Fn"] / GwN - 1))
    ok = wf <= 1e-4 and wF <= 2e-3
    P(f"KA3 Newtonian limit (y >= 1e5 inside), eight shapes: |g| r^2 - 1 at most {wf:.2e} (line 1e-4); F_n / (a0 M_b Gamma_w) - 1 at "
      f"most {wF:.2e} (line 2e-3): {'PASS' if ok else 'FAIL'}")
    RES["KA"]["KA3"] = dict(pass_=bool(ok), rows=rows); return ok

def ka4():
    rows = []
    for M, ds in ((96, 0.03), (128, 0.03), (192, 0.02)):
        aout = 300.0; b = S.Bubble(S.Spheroid(aout, 1.0), S.s_grid(1e-2 / aout, ds), M=M, ext="far", point=False)
        b.mass, out = S.kuzmin_mass(b, 1.0); b.solve(S.initial_guess(b))
        u = b.node_u(b.Phi); r = b.m[:, None] * b.c["Xabs"][None, :]; z = b.m[:, None] * b.c["zw"][None, :]; R = b.m[:, None] * b.c["Rw"][None, :]
        ex = S.u_in(1.0 / (R ** 2 + (np.abs(z) + 1.0) ** 2)); sel = (r >= 0.5) & (r <= 20) & (np.abs(z) >= 0.3)
        rows.append(dict(M=M, ds=ds, worst=float(np.max(np.abs(u[sel] / ex[sel] - 1))), conv=bool(b.converged), points=int(sel.sum()), mass_outside=out))
    ok = rows[-1]["worst"] <= 2e-3 and rows[-1]["conv"]
    P(f"KA4 Kuzmin disc of scale r_M, law everywhere, |g| against nu(g_N) g_N at radii 0.5-20 r_M and heights >= 0.3 r_M: "
      + ", ".join(f"{r_['worst']:.2e} (M {r_['M']})" for r_ in rows) + f" (line 2e-3 on the finest; the error falls as 1 / M: a razor-thin "
      f"sheet between two rows of cells): {'PASS' if ok else 'FAIL'}")
    RES["KA"]["KA4"] = dict(pass_=bool(ok), rows=rows); return ok

def lin_alpha(q, mu_c, M, ds):
    g = S.Spheroid(1.0, q); b = S.Bubble(g, S.s_grid(1e-2, ds), M=M, ext="conf", kmode="lin", Kconst=mu_c, point=False, ref=None)
    b.Phi = np.zeros((b.N + 1, M)); return b.response(0)[0], b.response(1)[0], g.volume()

def ka5():
    worst = 0.0; worst_prod = 0.0; rows = []
    for q in (0.2, 0.5, 2.0):
        for mu_c in (0.1, 0.5, 2.0):
            lz = Lz(q); lx = (1 - lz) / 2
            p0, p1, V = lin_alpha(q, mu_c, 256, 0.012); q0, q1, _ = lin_alpha(q, mu_c, *PROD)
            e0 = (V / (4 * math.pi)) * (mu_c - 1) / (1 + lz * (mu_c - 1)); e1 = (V / (4 * math.pi)) * (mu_c - 1) / (1 + lx * (mu_c - 1))
            rows.append(dict(q=q, mu=mu_c, par=p0 / e0 - 1, perp=p1 / e1 - 1, par_prod=q0 / e0 - 1, perp_prod=q1 / e1 - 1))
            worst = max(worst, abs(p0 / e0 - 1), abs(p1 / e1 - 1)); worst_prod = max(worst_prod, abs(q0 / e0 - 1), abs(q1 / e1 - 1))
    ok = worst <= 1e-3
    P(f"KA5 linear spheroids (mu 0.1, 0.5, 2; q 0.2, 0.5, 2) against the depolarization closed forms: {worst:.2e} on the grid "
      f"256 x 0.012 (line 1e-3); on the production grid {PROD[0]} x {PROD[1]} the same check reads {worst_prod:.2e}: {'PASS' if ok else 'FAIL'}")
    RES["KA"]["KA5"] = dict(pass_=bool(ok), worst=worst, worst_production_grid=worst_prod, rows=rows); return ok

def ka7():
    rows = []; ok = True
    for q, a in ((0.5, 3.0), (2.0, 3.0), (0.5, 10.0), (2.0, 10.0)):
        bs = solve_point(S.Spheroid(a, q), 128, 0.03); wq = bs.wall(mutate_W=(MUT == "M1"))
        F, D = [], []; bw = None
        for w_ in WIDTHS:
            b = smooth_bubble(q, a, w_, 96, 0.03, 20.0); f_, d_ = b.volume_force(); F.append(f_); D.append(d_)
            if w_ == 0.02: bw = b
        Fx, Dx = extrap0(F), extrap0(D)
        row = dict(q=q, a=a, Fn_surface=wq["Fn"], Dil_surface=wq["Dil"], Fn_volume=Fx, Dil_volume=Dx, rel_Fn=wq["Fn"] / Fx - 1, rel_Dil=wq["Dil"] / Dx - 1)
        if MUT is None:
            ds = 0.03; Dv = bw.volume_force()[1]; dL = {}
            for k in (1, 2):
                Lp = smooth_bubble(q, a * math.exp(k * ds), 0.02, 96, ds, 20.0).lagrangian()
                Lm = smooth_bubble(q, a * math.exp(-k * ds), 0.02, 96, ds, 20.0).lagrangian()
                dL[k] = (Lp - Lm) / (2 * k * ds)
            vw = (4 * dL[1] - dL[2]) / 3
            row.update(virtual_work=vw, Dil_volume_w002=Dv, rel_vw=vw / Dv - 1)
            ok = ok and abs(row["rel_vw"]) <= 1e-2
        ok = ok and abs(row["rel_Fn"]) <= 1e-3 and abs(row["rel_Dil"]) <= 1e-3
        rows.append(row)
        P(f"   KA7 q {q} a {a}: F_n surface {row['Fn_surface']:.6f} volume {Fx:.6f} ({row['rel_Fn']:+.1e}); dilation moment "
          f"{row['Dil_surface']:.6f} / {Dx:.6f} ({row['rel_Dil']:+.1e})" + (f"; virtual work {row['virtual_work']:.6f} vs volume at w 0.02 "
          f"{row['Dil_volume_w002']:.6f} ({row['rel_vw']:+.1e})" if MUT is None else ""))
    P(f"KA7 two routes to the force on oblique walls (line 1e-3) and virtual work (line 1e-2): {'PASS' if ok else 'FAIL'}")
    RES["KA"]["KA7"] = dict(pass_=bool(ok), rows=rows); return ok

def ka9():
    """the unit chain: two masses at the same a / r_M, q and R_d / r_M, entered in kpc and solar masses."""
    out = []
    for lm in (10.0, 11.0):
        for f, a0 in A0.items():
            rM = math.sqrt(G * 10 ** lm * MS / a0); a_kpc = 10.0 * rM / KPC; Rd_kpc = 0.3 * rM / KPC
            a_d = a_kpc * KPC / rM; Rd_d = Rd_kpc * KPC / rM
            b, br, fo, ff = solve_disc(S.Spheroid(a_d, 0.5), Rd_d, 48, 0.06); st = stats(b, b.geom, a_d, ref_signal(br, ff, b.geom), gref=br.inplane()[1], Rmin=0.05 * Rd_d)
            out.append((st["Gamma_F"], st["Gamma_C"], st["Fn"]))
    out = np.array(out); w = float(np.max(np.abs(out / out[0] - 1)))
    ok = w <= 1e-6
    P(f"KA9 scale symmetry (log M_b 10 and 11, both footings, a = 10 r_M, q = 0.5, R_d = 0.3 r_M entered in kpc): ratios agree to "
      f"{w:.1e} (line 1e-6): {'PASS' if ok else 'FAIL'}")
    RES["KA"]["KA9"] = dict(pass_=bool(ok), worst=w); return ok

def ka10():
    rows = []; ok = True
    for a in (10.0, 30.0, 100.0):
        geom = S.Spheroid(a, 1.0); b = solve_point(geom, *PROD); st = stats(b, geom, a, DS_LAW)
        r, m, _, mc = b.eff_mass(); _, dsc = S.delta_sigma(EDGES, r, m, mc)
        rs, ms, m0 = S.sphere_shells(a); _, dss = S.delta_sigma(EDGES, rs, ms, m0); sel = MID <= 0.8 * a
        w = float(np.max(np.abs(dsc[sel] / dss[sel] - 1)))
        rows.append(dict(a=a, signal_dev=w, Gamma_F=st["Gamma_F"], Gamma_C=st["Gamma_C"], R_len=st["R_len"], R_len_closed=sphere_reach(a)))
        ok = ok and w <= 2e-3 and abs(st["Gamma_F"] - 1) <= 1e-2 and abs(st["Gamma_C"] - 1) <= 1e-2
    P("KA10 the chain on a sphere (a = 10, 30, 100 r_M): signal vs closed form at R <= 0.8 a "
      + ", ".join(f"{r_['signal_dev']:.1e}" for r_ in rows) + " (line 2e-3); Gamma_F "
      + ", ".join(f"{r_['Gamma_F']:.4f}" for r_ in rows) + "; Gamma_C " + ", ".join(f"{r_['Gamma_C']:.4f}" for r_ in rows)
      + f" (line 1 +- 1e-2); reach / a " + ", ".join(f"{r_['R_len'] / r_['a']:.4f}" for r_ in rows) + f": {'PASS' if ok else 'FAIL'}")
    RES["KA"]["KA10"] = dict(pass_=bool(ok), rows=rows); return ok


# ------------------------------------------------------------------ B3: free boundary at uniform exterior pressure
def b3_one(ptil, Rd, grid, itmax=15):
    """wall on which p_wall = ptil (units a0^2 / 4 pi G) around an exponential disc; star-shaped, starting from SWT1's sphere."""
    M, ds = grid
    a_s = 1 / math.sqrt(math.exp(brentq(lambda ly: math.log(float(S.Wsph(S.u_in(math.exp(ly)))) / ptil), math.log(1e-12), math.log(1e6))))
    cl = np.array([a_s]); hist = []
    for it in range(itmax):
        geom = S.Star(cl); b, _, fout, _ = solve_disc(geom, Rd, M, ds, ext="ray", with_ref=False)
        wq = b.wall(); dev = wq["p"] / ptil - 1; hist.append(float(np.max(np.abs(dev))))
        if hist[-1] <= 1e-3 or not b.converged: break
        # AMENDMENT A1: the step is taken degree by degree with the deep law's response kappa_l = 3 (1 + sqrt(l (l + 1) / 2));
        # the criteria's first reading (the sphere's |dp/dn| for every degree) multiplies the l = 2 error by -1.73 per step.
        pi_l = b.ext.T0 @ dev; pi_l[1::2] = 0.0; pi_l[17:] = 0.0
        ll = np.arange(len(pi_l)); kap = 3 * (1 + np.sqrt(ll * (ll + 1) / 2.0))
        rho_new = geom.rho(b.mu) * (1 + b.ext.P0.T @ (pi_l / kap))        # pressure too high: move the wall out
        c_new = b.ext.T0 @ rho_new; c_new[1::2] = 0.0; cl = c_new[:17]
    b, br, fout, f = solve_disc(geom, Rd, M, ds, ext="ray")
    st = stats(b, geom, float(geom.rho(np.array([0.0]))[0]), ref_signal(br, f, geom), gref=br.inplane()[1], Rmin=0.05 * Rd)
    rho = geom.rho(b.mu)
    st.update(a_sphere=a_s, iterations=len(hist), flatness_history=hist, flat=bool(hist[-1] <= 1e-3), shape_dev=float(np.max(np.abs(rho / a_s - 1))),
              axis_ratio=float(geom.rho(np.array([1.0]))[0] / geom.rho(np.array([0.0]))[0]), vol_ratio=geom.volume() / (4 * math.pi / 3 * a_s ** 3),
              disc_outside=fout, legendre=cl.tolist())
    return st


# ------------------------------------------------------------------ main
def finish(extra=None):
    RES["seconds"] = time.time() - T0
    if extra: RES.update(extra)
    json.dump(RES, open(os.path.join(HERE, f"nsw1{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"nsw1{TAG}.out"), "w").write("\n".join(OUT) + "\n")

def main():
    P(f"NSW1 {'MUTATE ' + MUT + ' ' if MUT else ''}run. Criteria 052f87daad, amendment A1 0dfa03d257. Production grid {PROD[0]} x {PROD[1]}, refinement {FINE[0]} x {FINE[1]}. "
      f"rho_d0 {RHO_D0:.4e} kg / m^3. Units r_M, a0, M_b.")
    mono = bool(np.all(np.diff(RLEN_TAB) > 0))
    P(f"Reference spheres: reach / radius from {RLEN_TAB[0] / RS_TAB[0]:.3f} (R_s {RS_TAB[0]:.2f}) to {RLEN_TAB[-1] / RS_TAB[-1]:.3f} "
      f"(R_s {RS_TAB[-1]:.0f}); table monotone: {mono}")
    RES["sphere_table"] = dict(Rs=RS_TAB.tolist(), R_len=RLEN_TAB.tolist(), monotone=mono)

    if MUT == "M1":
        k6 = ka6(); k7 = ka7(); bites = (not k6) and (not k7)
        P(f"MUTATE M1 (tangential term dropped: W(u) at the full magnitude in place of W_g): KA6 {'fails' if not k6 else 'PASSES'}, "
          f"KA7 {'fails' if not k7 else 'PASSES'} -> {'BITES' if bites else 'DOES NOT BITE'}"); finish(dict(bites=bool(bites))); return
    if MUT == "M2":
        _, wm = ka1(); rows = []
        for q in (0.5, 2.0):
            b = solve_point(S.Spheroid(10.0, q), 48, 0.06, flux_mutate=True); rows.append(dict(q=q, M_ext=b.wall()["M_ext"], conv=bool(b.converged)))
        bites = wm > 1e-6 and all(abs(r_["M_ext"] - 1) > 1e-6 for r_ in rows)
        P(f"MUTATE M2 (dPhi/dn continuous at the wall): exterior mass - 1 on the spheres up to {wm:.3f}; spheroids q 0.5, 2 at a 10: "
          + ", ".join(f"{r_['M_ext']:.4f}" for r_ in rows) + f" -> KA1(a) {'fails: BITES' if bites else 'PASSES: DOES NOT BITE'}")
        finish(dict(bites=bool(bites), rows=rows)); return
    if MUT == "M3":
        rows = []
        for q, a in ((1.0, 10.0), (0.5, 10.0), (2.0, 10.0), (0.2, 30.0), (3.0, 30.0)):
            b = solve_point(S.Spheroid(a, q), 48, 0.06, law_sign=-1.0); wq = b.wall()
            rows.append(dict(q=q, a=a, conv=bool(b.converged), p_max=float(np.max(wq["p"])), p_min=float(np.min(wq["p"])), Fn=wq["Fn"]))
        bites = all(r_["p_max"] < 0 for r_ in rows)
        P("MUTATE M3 (sign of the S J term flipped): largest wall pressure per case " + ", ".join(f"{r_['p_max']:.3e}" for r_ in rows)
          + f"; F_n " + ", ".join(f"{r_['Fn']:.4f}" for r_ in rows) + f" -> force {'inward on every element: BITES' if bites else 'NOT inward everywhere: DOES NOT BITE'}")
        finish(dict(bites=bool(bites), rows=rows)); return
    if MUT == "M4":
        p0, p1, V = lin_alpha(0.05, 0.01, 256, 0.012); Vbar = 4 * math.pi / 9 * (p0 + 2 * p1)
        s0, s1, Vs = lin_alpha(1.0, 0.01, 96, 0.03); Vsb = 4 * math.pi / 9 * (s0 + 2 * s1)
        lz = Lz(0.05); lx = (1 - lz) / 2; ex = (V / 3) * (-0.99) * (1 / (1 - 0.99 * lz) + 2 / (1 - 0.99 * lx)) / 3
        gc = abs(Vsb) / abs(Vbar); bites = gc >= 5
        P(f"MUTATE M4 (power check): planted linear insulating disc q 0.05, mu 0.01 at equal equatorial radius: V |alpha_bar| "
          f"{abs(Vbar):.4f} (closed form {abs(ex):.4f}) against the sphere's {abs(Vsb):.4f}: Gamma_C = {gc:.3f} -> "
          f"{'the pipeline reports a lift (>= 5): PASSES ITS POWER CHECK' if bites else 'NO POWER'}")
        finish(dict(bites=bool(bites), Gamma_C=gc, Va_bar=Vbar, Va_bar_closed=ex, Va_sphere=Vsb)); return

    # ---- known answers
    kas = {}
    kas["KA6"] = ka6(); k1, wm_sph = ka1(); kas["KA1bc"] = k1; kas["KA2"] = ka2(); kas["KA3"] = ka3(); kas["KA4"] = ka4()
    kas["KA5"] = ka5(); kas["KA7"] = ka7(); kas["KA9"] = ka9(); kas["KA10"] = ka10()
    P(f"[{time.time() - T0:.0f} s] known answers before the graded run: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in kas.items()))
    if "--ka-only" in sys.argv:
        P("--ka-only: stopping before the graded cases; nothing written."); return

    # ---- graded cases
    ck = os.path.join(HERE, "nsw1_ckpt.json")
    done = json.load(open(ck)) if os.path.exists(ck) else {}
    cases = [(src, q, a) for src in ["P"] + [f"E{r_}" for r_ in RDS] for a in AS for q in QS if not (src == "E1.0" and a == 3.0)]
    for src, q, a in cases:
        key = f"{src}_q{q}_a{a}"
        if key not in done:
            t1 = time.time(); st = run_case(src, q, a, PROD); sf = run_case(src, q, a, FINE)
            st["fine"] = {k: sf[k] for k in ("Gamma_F", "Gamma_C", "Fn", "Va_bar", "R_len", "inplane_dev", "admissible", "M_ext", "conv")}
            st["seconds"] = time.time() - t1
            if not (src == "P" and a == 30.0): st.pop("wall")
            done[key] = st; json.dump(done, open(ck, "w"))
        st = done[key]
        P(f"case {key:<16} adm {str(st['admissible']):<5} plane dev {st['inplane_dev']:.3f} | F_n {st['Fn']:.5f} Gw {st['Gamma_w']:.3f} col {st['col_max']:.4f} | "
          f"V|a| {abs(st['Va_bar']):.4g} | R_len {st['R_len']:.2f} R_sph {st['R_sph']:.2f} | Gamma_F {st['Gamma_F']:.3f} Gamma_C {st['Gamma_C']:.3f} "
          f"(fine {st['fine']['Gamma_F']:.3f} {st['fine']['Gamma_C']:.3f}) | M_ext-1 {st['M_ext'] - 1:+.1e}")
        if STOP["flag"]:
            P("SIGTERM: checkpoint written, stopping."); finish(dict(interrupted=True)); sys.exit(143)
    RES["cases"] = done

    # ---- B3
    b3 = {}
    for f, a0 in A0.items():
        b3[f] = {}
        for sig in (17.5, 35.0, 52.5):
            ptil = 4 * math.pi * G * RHO_D0 * (sig * 1e3) ** 2 / a0 ** 2
            for Rd in RDS:
                key = f"sig{sig}_Rd{Rd}"; ckey = f"B3_{f}_{key}"
                if ckey not in done:
                    st = b3_one(ptil, Rd, PROD); sf = b3_one(ptil, Rd, FINE)
                    st["fine"] = {k: sf[k] for k in ("Gamma_F", "Gamma_C", "Fn", "Va_bar", "R_len", "inplane_dev", "admissible", "M_ext", "conv", "shape_dev", "flat")}
                    st.pop("wall"); st["p_ext_tilde"] = ptil
                    st["a_kpc"] = {str(lm): st["a_sphere"] * math.sqrt(G * 10 ** lm * MS / a0) / KPC for lm in KIDS}
                    done[ckey] = st; json.dump(done, open(ck, "w"))
                st = done[ckey]; b3[f][key] = st
                P(f"B3 [{f}] sigma {sig} km/s, R_d {Rd} r_M: sphere {st['a_sphere']:.1f} r_M ({', '.join(f'{v:.0f}' for v in st['a_kpc'].values())} kpc); "
                  f"{st['iterations']} solve(s), |p / p_ext - 1| <= {st['flatness_history'][-1]:.1e} (flat {st['flat']}); shape dev {st['shape_dev']:.2e}, "
                  f"pole / equator {st['axis_ratio']:.5f}, volume / sphere {st['vol_ratio']:.5f}; adm {st['admissible']} (plane dev {st['inplane_dev']:.3f}); "
                  f"Gamma_F {st['Gamma_F']:.3f} Gamma_C {st['Gamma_C']:.3f} (fine {st['fine']['Gamma_F']:.3f} {st['fine']['Gamma_C']:.3f})")
                if STOP["flag"]:
                    P("SIGTERM: checkpoint written, stopping."); finish(dict(interrupted=True)); sys.exit(143)
    RES["B3"] = b3

    # ---- remaining known answers and Part A's numerical checks
    allst = [done[f"{s_}_q{q}_a{a}"] for s_, q, a in cases] + [b3[f][k] for f in b3 for k in b3[f]]
    wm = max(max(abs(s_["M_ext"] - 1), abs(s_["fine"]["M_ext"] - 1)) for s_ in allst); wm = max(wm, wm_sph)
    kas["KA1a"] = wm <= 1e-6
    P(f"KA1(a) exterior effective mass - 1 over every solved case and both grids: at most {wm:.2e} (line 1e-6): {'PASS' if kas['KA1a'] else 'FAIL'}")
    adm = [s_ for s_ in allst if s_["admissible"]]
    w8 = max(max(abs(s_["fine"]["Gamma_F"] / s_["Gamma_F"] - 1), abs(s_["fine"]["Gamma_C"] / s_["Gamma_C"] - 1)) for s_ in adm) if adm else float("nan")
    flips = sum(1 for s_ in allst if s_["admissible"] != s_["fine"]["admissible"])
    kas["KA8"] = bool(adm) and w8 <= 0.02
    P(f"KA8 convergence: Gamma_F and Gamma_C of the {len(adm)} admissible cases move by at most {w8:.2e} between {PROD[0]} x {PROD[1]} and "
      f"{FINE[0]} x {FINE[1]} (line 2e-2): {'PASS' if kas['KA8'] else 'FAIL'}; cases whose admissibility differs between the grids: {flips}")
    conv_all = all(s_["conv"] and s_["fine"]["conv"] for s_ in allst)
    P(f"Every Newton solve converged: {conv_all}. B3 walls flat to 1e-3: {all(b3[f][k]['flat'] and b3[f][k]['fine']['flat'] for f in b3 for k in b3[f])}")
    sph = [done[f"{s_}_q{q}_a{a}"] for s_, q, a in cases]
    a3b = min(s_["A3b_margin"] for s_ in allst); a4 = max(s_["Fn"] - s_["Gamma_w"] for s_ in allst); colm = max(s_["col_max"] for s_ in allst)
    P(f"Part A, numerical: A3(b) |g_out| - W_g >= {a3b:.2e} at every wall node of every case; A4 F_n - Gamma_w <= {a4:.3e} (a0 M_b); "
      f"largest column {colm:.4f} of a0 / (4 pi G) = {colm * A0['canonical'] / (4 * math.pi * G) * PC ** 2 / MS:.1f} / "
      f"{colm * A0['alt'] / (4 * math.pi * G) * PC ** 2 / MS:.1f} M_sun / pc^2 (bound {A0['canonical'] / (4 * math.pi * G) * PC ** 2 / MS:.1f} / "
      f"{A0['alt'] / (4 * math.pi * G) * PC ** 2 / MS:.1f})")
    a6 = []
    for src, q, a in cases:
        if src != "P" or q == 1.0: continue
        s_ = done[f"P_q{q}_a{a}"]; rmin, rmax = a * min(1, q), a * max(1, q)
        dn, dfar = (s_["d_pole"], s_["d_eq"]) if q < 1 else (s_["d_eq"], s_["d_pole"])
        a6.append(dict(q=q, a=a, near_ok=bool(dn >= 1 / rmin ** 2 * (1 - 1e-6)), far_ok=bool(dfar <= 1 / rmax ** 2 * (1 + 1e-6)), d_near_over_y=dn * rmin ** 2,
                       d_far_over_y=dfar * rmax ** 2, Fn_over_deep=s_["Fn"] / (2 / 3 * s_["sqrt_d_flux"]),
                       bracket_ok=bool(2 / 3 * math.sqrt(s_["d_min"]) <= s_["Fn"] <= 2 / 3 * math.sqrt(s_["d_max"]))))
    RES["A6_numeric"] = a6
    P(f"A6, numerical (point baryons, {len(a6)} non-spherical walls): d >= y(r_min) at the nearest points in {sum(r_['near_ok'] for r_ in a6)}, d <= y(r_max) at "
      f"the farthest in {sum(r_['far_ok'] for r_ in a6)}; F_n / [(2/3) flux-weighted sqrt(d)] at a = 100: "
      + ", ".join(f"{r_['Fn_over_deep']:.3f}" for r_ in a6 if r_["a"] == 100.0) + f"; deep bracket holds in {sum(r_['bracket_ok'] for r_ in a6)}")
    RES["KA_summary"] = {k: bool(v) for k, v in kas.items()}

    # ---- labels
    ka_ok = all(kas.values()) and conv_all
    for f in A0:
        pool = [(k, done[k]) for k in (f"{s_}_q{q}_a{a}" for s_, q, a in cases)] + [(f"B3_{k}", b3[f][k]) for k in b3[f]]
        ad = [(k, s_) for k, s_ in pool if s_["admissible"]]
        gF = max(ad, key=lambda t: t[1]["Gamma_F"]); gC = max(ad, key=lambda t: t[1]["Gamma_C"])
        if not ka_ok: lab = "NO VERDICT"
        elif gF[1]["Gamma_F"] >= LINE_F[f] or gC[1]["Gamma_C"] >= LINE_C[f]: lab = "CAP LIFTS"
        elif gF[1]["Gamma_F"] < 2 and gC[1]["Gamma_C"] < 2: lab = "CAP HOLDS"
        else: lab = "PARTIAL"
        RES["labels"][f] = dict(label_before_lean=lab, admissible=len(ad), of=len(pool), max_Gamma_F=gF[1]["Gamma_F"], at_F=gF[0], max_Gamma_C=gC[1]["Gamma_C"], at_C=gC[0],
                                line_F=LINE_F[f], line_C=LINE_C[f])
        P(f"LABEL [{f}] (before the Lean check of A2): {lab}. Admissible {len(ad)} of {len(pool)}. Largest Gamma_F {gF[1]['Gamma_F']:.3f} ({gF[0]}; line "
          f"{LINE_F[f]}), largest Gamma_C {gC[1]['Gamma_C']:.3f} ({gC[0]}; line {LINE_C[f]}).")
    P(f"[{time.time() - T0:.0f} s] done.")
    finish()

if __name__ == "__main__":
    main()
