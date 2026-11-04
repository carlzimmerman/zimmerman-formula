#!/usr/bin/env python3
"""CZ4: CZ2/CZ3's filter rules TID, LOC (HALF beside) with the solar neighbourhood inside the filter: baryon disc tide (S3 MW
models), nearby-star discreteness (Campbell bound + alpha Cen), re-graded on AZ12's planet gate and KT16's Cassini Q2.
Criteria 285353a57b. CZ2/CZ3 code copied. OMP_NUM_THREADS=1 python3 -I cz4.py [--mutate]. kappa = 1/2 FITTED and held
fixed; not theory closed."""
import json, math, os, resource, sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "rebuild_2026_10_22", "S3_v3_mw_seals")); import s3_mw as MW
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
KAP = 0.5; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; GEXT, CEIL = 2.32e-10, 5.2e-27
G = 6.6743e-11; MSUN = 1.98892e30; PC = 3.0857e16; RHOU = MSUN / PC ** 3
GM = 1.32712440018e20; GMs = G * MSUN; AU = 149597870700.0; YR = 365.25 * 86400; MAS = math.pi / (180 * 3600 * 1000)
ECC = dict(Mercury=.206, Venus=.007, Earth=.017, Mars=.093, Jupiter=.048, Saturn=.054)
PL = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/RQ3_acceptance_v2/tolerances.json")))["PLANETS"]
CZ3 = json.load(open(os.path.join(HERE, "..", "CZ3_planet_precession_filters", "cz3.json")))
CZ2 = json.load(open(os.path.join(HERE, "..", "CZ2_filter_regrade_newtonian_efe", "cz2.json")))
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
dnu_s = lambda y: -1 / (2 * y * y * math.sqrt(0.25 + 1 / y))
P(f"CZ4 (criteria 285353a57b){'  [MUTATE: rho_b x 1e5]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")

# ---------- neighbourhood inputs (S3 MW models, R0 = 8.122 kpc, midplane) ----------
R0 = MW.R0 * 1e3 * PC
RHOB = {"McMillan": float(MW.rho_mcm(MW.R0, 0.0)) / 1e9, **{k: float(f(MW.R0, 0.0)) / 1e9 for k, f in MW.VARIANTS.items()}}
RHOS = float(MW.rho_stars(MW.R0, 0.0)) / 1e9; RHOTOT = {"canonical": 0.166, "alt": 0.174}
kb = max(RHOB, key=RHOB.get); rho_b = RHOB[kb] * (1e5 if MUT else 1.0); MW_SYS, DMIN, ACEN = 2.0, 1.3, (2.1, 1.34)
P(f"rho_b(R0, 0) [Msun/pc^3]: " + ", ".join(f"{k} {v:.4f}" for k, v in RHOB.items()) + f"; graded {kb} {rho_b:.4g}; stars {RHOS:.4f}")
def zsmooth(xi_pc):
    z = np.linspace(-6 * xi_pc, 6 * xi_pc, 4001) / 1e3; w = np.exp(-0.5 * (z * 1e3 / xi_pc) ** 2); w /= w.sum()
    return float(np.sum(w * MW.VARIANTS[kb](MW.R0, z) if kb in MW.VARIANTS else w * MW.rho_mcm(MW.R0, z)) / 1e9 / RHOB[kb])
def Ttensor(e, beta, rho):
    return np.array([beta * e / R0, -e / R0, -4 * math.pi * G * rho * RHOU - (beta - 1) * e / R0])

# ---------- filter lengths (CZ2/CZ3, copied; tenv adds the neighbourhood tide in x units) ----------
def xi_loc(r, gm, gs, clip, tenv=0.0):
    dg = np.abs(np.gradient(gm, r)) + tenv; return np.minimum(gm * gm / np.maximum(dg * gs, 1e-300), clip)
def xi_tid(r, gm, gs, clip, tenv=0.0):
    tau = np.sqrt(np.gradient(gm, r) ** 2 + 2 * (gm / r) ** 2 + tenv ** 2); lt = np.log(np.maximum(tau, 1e-300))
    dt = np.abs(tau * np.gradient(lt, np.log(r)) / r); return np.minimum(4 / math.sqrt(3) * tau ** 3 / np.maximum(dt * dt * gs, 1e-300), clip)
def gh_pt(r, xi):
    xi = np.broadcast_to(xi, r.shape); x = r / xi; out = np.empty_like(r); s = x < 1e-3
    out[~s] = (erf(x[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * x[~s] * np.exp(-x[~s] ** 2 / 2)) / r[~s] ** 2; out[s] = math.sqrt(2 / math.pi) / 3 * r[s] / xi[s] ** 3; return out
def xi_fn(c, eta, tenv=0.0):
    def f(x):
        gq = np.sqrt(x ** -4.0 + eta * eta)
        return xi_loc(x, nu_s(gq) * gq, 1 / KAP, 1e4, tenv) if c == "LOC" else xi_tid(x, nu_s(gq) * x ** -2.0, 1 / KAP, 1e4, tenv)
    return f
def xi_table(c, eta, tenv=0.0, n=20000):
    if c == "HALF": return lambda xx: np.full_like(np.asarray(xx, float), 0.5)
    x = np.exp(np.linspace(math.log(1e-7), math.log(1e5), n)); X = xi_fn(c, eta, tenv)(x)
    return lambda xx: np.exp(np.interp(np.log(xx), np.log(x), np.log(X)))
def qcas(eta, xi, nr=20000, nm=200):
    u = np.linspace(math.log(1e-7), math.log(1e5), nr); r = np.exp(u); mu, w = np.polynomial.legendre.leggauss(nm)
    X = xi(r) if callable(xi) else xi; g = gh_pt(r, X)[:, None]; M = mu[None, :]
    A_ = nu_s(np.sqrt(eta * eta + g * g + 2 * eta * g * M)) - 1; return abs(1.5 * float(np.trapz(((A_ * (eta * (3 * M - 5 * M ** 3) + g * (1 - 3 * M * M))) @ w) / r, u)))

# ---------- stars: Gaussian-smoothed point mass, per unit mass (SI) ----------
def blob(s, xi):
    q = G * gh_pt(s, np.full_like(s, xi)); dq = np.gradient(q, s); return q, dq
def campbell(xi, smin, n=6000):
    s = np.exp(np.linspace(math.log(max(smin, 1e-4 * xi) if smin > 0 else 1e-4 * xi), math.log(1e3 * max(xi, smin)), n)); q, dq = blob(s, xi)
    tr = dq + 2 * q / s; fr = dq * dq + 2 * (q / s) ** 2; jac = 4 * math.pi * s ** 3
    return float(np.trapz(tr * tr * jac, np.log(s))), float(np.trapz(fr * jac, np.log(s)))
def stars_T(xi):
    """bounds on |tr T_*| and |T_*|_F (s^-2): 3 sigma Campbell (systems beyond DMIN, mass-weighted M_W_SYS) + alpha Cen."""
    itr, ifr = campbell(xi, DMIN * PC); nm2 = RHOS * RHOU * MW_SYS * MSUN
    m, d = ACEN[0] * MSUN, ACEN[1] * PC; s = d * np.array([0.999, 1.0, 1.001]); q, dq = blob(s, xi)
    tra = m * abs(dq[1] + 2 * q[1] / d); fra = m * math.sqrt(dq[1] ** 2 + 2 * (q[1] / d) ** 2)
    return 3 * math.sqrt(nm2 * itr) + tra, 3 * math.sqrt(nm2 * ifr) + fra

# ---------- AZ12's gate with the neighbourhood ----------
def rate(A, a, e, n, N):
    t, w = np.polynomial.legendre.leggauss(N); E = math.pi * (t + 1); c = np.cos(E); r = a * (1 - e * c)
    return math.sqrt(1 - e * e) / (n * a * e) * float(np.sum(.5 * w * A(r) * (c - e)))
def mono2d(r, h, T, ge, a0, nmu, nph):
    mu, w = np.polynomial.legendre.leggauss(nmu); ph = (np.arange(nph) + 0.5) * 2 * math.pi / nph
    s = np.sqrt(1 - mu * mu); cx = mu[:, None] * np.ones(nph)[None, :]; cy = s[:, None] * np.cos(ph)[None, :]; cz = s[:, None] * np.sin(ph)[None, :]
    out = np.empty_like(r)
    for i in range(r.size):
        gx = h[i] * cx + ge + r[i] * T[0] * cx; gy = (h[i] + r[i] * T[1]) * cy; gz = (h[i] + r[i] * T[2]) * cz
        rg = h[i] + ge * cx + r[i] * (T[0] * cx * cx + T[1] * cy * cy + T[2] * cz * cz)
        f = (nu_s(np.sqrt(gx * gx + gy * gy + gz * gz) / a0) - 1) * rg; out[i] = 0.5 * float(np.sum(w[:, None] * f)) / nph
    return out
def grade(c, a0, eta, ge, T, stars, orders=(256, 160, 64)):
    rM = math.sqrt(GM / a0); xt = xi_table(c, eta); yv = ge / a0; ne1, dn = float(nu_s(yv)) - 1, dnu_s(yv)
    h = (lambda r: a0 * gh_pt(r / rM, 0.5)) if c == "HALF" else (lambda r: a0 * gh_pt(r / rM, xt(r / rM)))
    kst = {}
    def kstar(r):
        out = np.empty_like(r)
        for i, rr in enumerate(r):
            xi = float(xt(np.array([rr / rM]))[0]) * rM; key = round(math.log(xi), 4)
            if key not in kst: kst[key] = stars_T(xi)
            ta, tf = kst[key]; out[i] = (ne1 * ta + abs(dn) * yv * tf) / 3 * rr
        return out
    rows = {}
    for nm, d in PL.items():
        e = ECC[nm]; a = d["a_au"] * AU; nn = math.sqrt(GM / a ** 3); sg = max(d["EPM"], d["INPOP"])
        r_sd = rate(lambda r: mono2d(r, h(r), T, ge, a0, orders[1], orders[2]), a, e, nn, orders[0]) * YR / MAS
        r_s = rate(lambda r: mono2d(r, h(r), np.zeros(3), ge, a0, orders[1], orders[2]), a, e, nn, orders[0]) * YR / MAS
        r_lin = rate(lambda r: r / 3 * (ne1 * T.sum() + dn * yv * T[0]), a, e, nn, orders[0]) * YR / MAS
        r_st = rate(kstar, a, e, nn, orders[0]) * YR / MAS if stars else 0.0
        xi_pc = float(xt(np.array([a / rM]))[0]) * rM / PC
        rows[nm] = dict(Z_sun=abs(r_s) / sg, Z_sun_disc=abs(r_sd) / sg, Z_stars=abs(r_st) / sg, Z_cons=(abs(r_sd) + abs(r_st)) / sg,
                        disc_num=r_sd - r_s, disc_lin=r_lin, xi_pc=xi_pc)
    return rows

for foot, a0 in A0SI.items():
    eta0 = GEXT / a0; etaN = brentq(lambda y: float(nu_s(y)) * y - eta0, 1e-6, eta0); ge = GEXT ** 2 / (GEXT + a0)
    yv = ge / a0; ne1, dn = float(nu_s(yv)) - 1, dnu_s(yv); RES[foot] = {}
    P(f"\n[{foot}] e = {ge:.4e}, nu_e - 1 = {ne1:.4f}, nu'_e e/a0 = {dn * yv:.4f}")
    for c in ("TID", "LOC", "HALF"):
        # K1: no neighbourhood reproduces CZ3
        k1 = grade(c, a0, etaN, ge, np.zeros(3), False)
        for p in ("Saturn", "Mars"):
            v = CZ3[foot][c]["rows"][p]["Z"]; ok = abs(k1[p]["Z_sun"] / v - 1) <= 1e-4; fail += not ok
        P(f"[{foot}] {c} K1 no neighbourhood: Saturn Z {k1['Saturn']['Z_sun']:.6g} (CZ3 {CZ3[foot][c]['rows']['Saturn']['Z']:.6g}), Mars {k1['Mars']['Z_sun']:.6g}: {'PASS' if ok else 'FAIL'}")
        worst = None
        for beta in (0.0, 1.0, 2.0):
            T = Ttensor(ge, beta, rho_b); g = grade(c, a0, etaN, ge, T, True)
            wp = max(g, key=lambda p: g[p]["Z_cons"])
            if worst is None or g[wp]["Z_cons"] > max(v["Z_cons"] for v in worst[2].values()): worst = (beta, T, g)
            k2 = max(abs(g[p]["disc_num"] / g[p]["disc_lin"] - 1) for p in g); ok2 = k2 <= 0.01; fail += not ok2
            P(f"  beta {beta:.0f}: worst {wp} Z_cons {g[wp]['Z_cons']:.4g} (Sun {g[wp]['Z_sun']:.3g}, Sun+disc {g[wp]['Z_sun_disc']:.3g}, stars bound {g[wp]['Z_stars']:.3g}); K2 linear {k2:.1e} {'PASS' if ok2 else 'FAIL'}")
        beta, T, g = worst
        gc = grade(c, a0, etaN, ge, T, True, orders=(256, 320, 128)); k3 = max(abs(gc[p]["Z_cons"] / g[p]["Z_cons"] - 1) for p in g); ok3 = k3 <= 0.01; fail += not ok3
        # Cassini
        rM = math.sqrt(GMs / a0); qp = CEIL / (1.5 * a0 / rM); TF = float(np.linalg.norm(T)); tenv = TF * rM / a0
        if c != "HALF":
            q0 = qcas(etaN, xi_fn(c, etaN)) / qp; qe = qcas(etaN, xi_fn(c, etaN, tenv)) / qp
            v6 = CZ2[f"cassini|{foot}"]["rows"][f"N|{c}"]["x_ceiling"]; ok6 = abs(q0 / v6 - 1) <= 1e-6; fail += not ok6
            rp = math.sqrt(GM / a0); x_pl = np.array([PL[p]["a_au"] * AU / rp for p in PL])
            k4 = float(np.max(np.abs(xi_table(c, etaN, TF * rp / a0)(x_pl) / xi_table(c, etaN)(x_pl) - 1))); ok4 = k4 <= 1e-6; fail += not ok4
        else:
            q0 = qe = qcas(etaN, 0.5) / qp; ok6 = ok4 = True; v6 = k4 = float("nan")
        xi_sat = g["Saturn"]["xi_pc"]; ta, tf = stars_T(min(g[p]["xi_pc"] for p in g) * PC)
        Mtl = np.diag([(ne1 + dn * yv) * T[0], ne1 * T[1], ne1 * T[2]]); Mtl -= np.trace(Mtl) / 3 * np.eye(3)
        q_loc = (float(np.linalg.norm(Mtl)) + max(abs(ne1), abs(ne1 + dn * yv)) * tf) * math.sqrt(1.5)
        q_all = 4 * math.pi * G * RHOTOT[foot] * RHOU * (1e5 if MUT else 1.0); q_env = max(q_loc, q_all)
        qt = qe + q_env / CEIL
        badp = [p for p in g if g[p]["Z_cons"] > 2]; bad = badp + (["Cassini"] if qt > 1 else [])
        lab = f"{c} PASSES WITH NEIGHBOURS" if not bad else f"{c} FAILS WITH NEIGHBOURS: " + ", ".join(bad)
        wp = max(g, key=lambda p: g[p]["Z_cons"])
        RES[foot][c] = dict(beta=beta, rows=g, worst=wp, K3=k3, cassini=dict(q_sun_plain=q0, q_sun_neigh=qe, q_env_local=q_loc / CEIL, q_env_alltide=q_all / CEIL, total=qt),
                            label=lab, rho_smooth_ratio={p: zsmooth(g[p]["xi_pc"]) for p in g})
        P(f"[{foot}] {c} worst beta {beta:.0f}: {wp} Z_cons {g[wp]['Z_cons']:.4g}; xi Mercury {g['Mercury']['xi_pc']:.4g} pc, Saturn {xi_sat:.4g} pc; K3 {k3:.1e} {'PASS' if ok3 else 'FAIL'}")
        P(f"  rows: " + "; ".join(f"{p} {g[p]['Z_cons']:.3g}" for p in g))
        P(f"  smoothed/unsmoothed rho at xi (beside): " + ", ".join(f"{p} {RES[foot][c]['rho_smooth_ratio'][p]:.3f}" for p in g))
        P(f"  Cassini: Q2_sun {q0:.4g}x (CZ2 {v6:.4g}, K6 {'PASS' if ok6 else 'FAIL'}) -> with neighbourhood xi {qe:.4g}x; Q2_env local {q_loc / CEIL:.3g}x, whole tide {q_all / CEIL:.3g}x; total {qt:.4g}x; K4 xi at planets {k4:.1e} {'PASS' if ok4 else 'FAIL'}")
        P(f"LABEL [{foot}] {lab}")
# K5 blob oracle
xi = 8 * PC; itr, _ = campbell(xi, 0.0); ref = (4 * math.pi * G) ** 2 / (8 * math.pi ** 1.5 * xi ** 3); k5 = abs(itr / ref - 1); ok5 = k5 <= 1e-3; fail += not ok5
P(f"\nK5 blob Hessian: int (tr T)^2 d^3s / (4 pi G)^2/(8 pi^1.5 xi^3) - 1 = {k5:.1e}: {'PASS' if ok5 else 'FAIL'}")
ta1, tf1 = stars_T(8 * PC); MW_SYS = 1.0; ta2, tf2 = stars_T(8 * PC); MW_SYS = 2.0
P(f"stars bound at xi 8 pc: |tr T*| {ta1:.3g}, |T*|_F {tf1:.3g} s^-2 (M_w 1: {ta2:.3g}, {tf2:.3g}); disc 4 pi G rho_b {4 * math.pi * G * rho_b * RHOU:.3g}")
P("\nJoined with CZ2:")
for foot in A0SI:
    for c in ("TID", "LOC"):
        s2 = CZ2[f"label|{foot}|{c}"]["label"]; ok = s2.endswith("SURVIVES") and RES[foot][c]["label"].endswith("PASSES WITH NEIGHBOURS")
        P(f"  [{foot}] {c}: CZ2 {s2}; CZ4 {RES[foot][c]['label']}" + (f"  ->  {c} SURVIVES FIVE ON {foot.upper()} WITH NEIGHBOURS" if ok else ""))
if MUT:
    w = {f"{f}|{c}": RES[f][c]["rows"]["Saturn"]["Z_cons"] for f in A0SI for c in ("TID", "LOC")}
    P(f"MUTATE bite (Saturn Z_cons > 10, TID and LOC, both footings): {w} -> {'BITES' if min(w.values()) > 10 else 'DOES NOT BITE'}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30; RES["peak_rss_GB"] = rss; RES["fail"] = fail; RES["rho_b"] = RHOB
P(f"\npeak RSS {rss:.2f} GB; failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"cz4{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"cz4{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)
