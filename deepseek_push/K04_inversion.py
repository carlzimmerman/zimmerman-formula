#!/usr/bin/env python3
"""
K04 -- OPACITY INVERSION + THE THREE-OBSERVABLE TEST (anti-circular core)
========================================================================
2026-09-23.  Family kappa(r) = tau0 (1 + q r^2), T = 1, central source.
Engine: J02_moment_hierarchy.simulate (exact optical-depth bisection; no
null-collision thinning).  No git commit.  No circular fitting anywhere:
(A, E[D]) enter ONLY the inversion; E[v^2] enters ONLY the comparison.

(A) CLOSED-FORM INVERSION of (A, E[D]) -> (tau0, q):

        A      = P(N=0) = exp(-tau0 (1 + q/3))          (atom law, exact)
        E[D]   = tau0 (1/2 + q/4)  = int_0^1 r kappa dr (Theorem 1, exact)

    Eliminate q:  q = 4 E[D]/tau0 - 2  ->  -ln A = tau0/3 + 4 E[D]/3.
    Hence the unique closed-form inverse
        tau0_hat = -3 ln A_hat - 4 E[D]_hat
        q_hat    =  4 E[D]_hat / tau0_hat - 2
    (bijective on the family for tau0 > 0, q > -1).

(B) THIRD OBSERVABLE, PREDICTED (never fitted):
    E[v^2] = 2 E[ang] = 2 E[N]  (conditional-Gaussian lemma + Thomson
    mean-cosine 0, T = 1 -- exact per photon).  E[N] = E[int_0^tau kappa(X_s)
    ds] = int_0^1 kappa(r) rho(r) dr with rho the exact time-at-r residence
    density.  No algebraic identity ties E[N] to (A, E[D]); the prediction is
    the EXACT SURFACE from an independent deterministic transport solve
    (state (r, mu); Thomson kernel -> closed quadratic moments A(r), B(r);
    fixed point C(r,mu) = Pi(r,mu) + int kappa e^{-Lambda} [A + B gamma^2] ds,
    E[N] = (1 - A0) + int_0^1 kappa e^{-Lambda} (A + B) dr, the gamma = 1
    first-collision projection).  Evaluated at (tau0_hat, q_hat) from (A) and
    compared with the MEASURED E[v^2].  Thin-cloud closed form
    E[N] = tau0(1+q/3) + c2 tau0^2 + O(tau0^3) with c2 computed analytically
    in closed form and verified against the solver.

(C) FALSIFIER: see K04_OPACITY_INVERSION.md section 5.
"""
import json, math, sys, time
import numpy as np

sys.path.insert(0, "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push")
from J02_moment_hierarchy import simulate

OUT = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)

# ----------------------------------------------------------------------
# Deterministic exact-surface solver for E[N](tau0, q), central source.
# One shared geometry; each (tau0,q) precomputes its own flight kernel.
# ----------------------------------------------------------------------
class Geom:
    def __init__(self, nr=700, nmu=72, ns=20, nseg_max=8, mublk=8):
        self.r = np.linspace(0.0, 1.0, nr)
        self.mu, self.wmu = np.polynomial.legendre.leggauss(nmu)
        R0, MU0 = np.meshgrid(self.r, self.mu, indexing="ij")
        self.R0, self.MU0 = R0, MU0
        SW = -R0*MU0 + np.sqrt(np.maximum(R0*R0*MU0*MU0 + 1.0 - R0*R0, 0.0))
        self.SW = SW
        xg, wg = np.polynomial.legendre.leggauss(ns)
        NS = np.clip(np.ceil(SW/0.30).astype(int), 1, nseg_max)
        ntot = nseg_max*ns
        Sall = np.zeros((nr, nmu, ntot)); Wall = np.zeros_like(Sall)
        Mask = np.zeros_like(Sall)
        for i in range(nr):
            for j in range(nmu):
                sw = SW[i, j]; nsg = NS[i, j]
                if nsg == 0:
                    continue
                pts = (np.arange(nsg)[:, None] + 0.5*(xg[None, :] + 1.0))*(sw/nsg)
                Sall[i, j, :nsg*ns] = pts.ravel()
                Wall[i, j, :nsg*ns] = (sw/(2.0*nsg))*np.tile(wg, nsg)
                Mask[i, j, :nsg*ns] = 1.0
        self.Sall, self.Wall, self.Mask = Sall, Wall, Mask
        self.nr, self.nmu, self.mublk = nr, nmu, mublk
        # precomputed geometry blocks over mu
        self.blocks = []
        for b in range(nmu // mublk):
            j0 = b*mublk; j1 = j0 + mublk
            Sj = Sall[:, j0:j1, :]
            Wj = Wall[:, j0:j1, :]
            Mj = Mask[:, j0:j1, :]
            R = R0[:, j0:j1, None]
            M = MU0[:, j0:j1, None]
            RS2 = R*R + 2.0*R*M*Sj + Sj*Sj
            RS = np.sqrt(RS2 + 1e-30)
            GAM = (R*M + Sj)/RS
            self.blocks.append((R, M, Sj, Wj, Mj, RS2, RS, GAM))
        self.ntot = ntot

class SurfaceSolver:
    def __init__(self, geom, tau0, q):
        self.g = geom; self.tau0 = tau0; self.q = q
        r, mu, wmu = geom.r, geom.mu, geom.wmu
        SW = geom.SW
        self.Pi = 1.0 - np.exp(-tau0*(SW + q*(geom.R0**2*SW
                      + geom.R0*geom.MU0*SW**2 + SW**3/3.0)))
        Lf = tau0*(r + q*r**3/3.0)
        self.f = tau0*(1.0 + q*r*r)*np.exp(-Lf)
        self.A0 = np.exp(-Lf[-1])
        self.FLY = []
        for (R, M, Sj, Wj, Mj, RS2, RS, GAM) in geom.blocks:
            LAM = Sj + q*(R*R*Sj + R*M*Sj*Sj + Sj**3/3.0)
            FL = tau0*(1.0 + q*RS2)*np.exp(-tau0*LAM)*Wj*Mj
            self.FLY.append(FL)
        self.RS = [b[6] for b in geom.blocks]
        self.GAM = [b[7] for b in geom.blocks]

    def moments(self, C):
        mu, wmu = self.g.mu, self.g.wmu
        A = (3.0/16.0)*np.sum(C*(3.0 - mu*mu)*wmu, axis=1)
        B = (3.0/16.0)*np.sum(C*(3.0*mu*mu - 1.0)*wmu, axis=1)
        return A, B

    def E_N_of(self, C):
        A, B = self.moments(C)
        return (1.0 - self.A0) + np.trapz(self.f*(A + B), self.g.r)

    def apply_K(self, C):
        A, B = self.moments(C)
        g = self.g; r = g.r
        KC = np.zeros_like(C)
        nb = g.nmu // g.mublk
        for b in range(nb):
            j0 = b*g.mublk; j1 = j0 + g.mublk
            RS = self.RS[b]; GAM = self.GAM[b]
            AA = np.interp(RS.ravel(), r, A).reshape(RS.shape)
            BB = np.interp(RS.ravel(), r, B).reshape(RS.shape)
            KC[:, j0:j1] = np.sum((AA + BB*GAM*GAM)*self.FLY[b], axis=2)
        return KC

    def solve(self, tol=1e-11, max_iter=8000, C0=None, depth=5, anderson=True):
        g = self.g
        C = np.zeros((g.nr, g.nmu)) if C0 is None else C0.copy()
        hist_x = []; hist_f = []
        it = 0; t0 = time.time()
        while it < max_iter:
            Cn = self.Pi + self.apply_K(C)
            res = Cn - C
            d = np.max(np.abs(res))
            mC = np.max(np.abs(C))
            if d < tol*(1.0 + mC):
                # verify: 12 plain steps must not move E[N]
                Cv = Cn
                for _ in range(12):
                    Cv = self.Pi + self.apply_K(Cv)
                if abs(self.E_N_of(Cv) - self.E_N_of(Cn)) < 1e-9*max(1.0, abs(self.E_N_of(Cn))):
                    C = Cv
                    break
            if mC > 1e3:
                raise RuntimeError(f"solver exploded |C|={mC:.3g} tau0={self.tau0} q={self.q}")
            hist_x.append(C.copy()); hist_f.append(res.copy())
            if len(hist_x) > depth:
                hist_x.pop(0); hist_f.pop(0)
            if anderson and len(hist_x) >= 2:
                FF = np.stack(hist_f, axis=-1)
                DF = FF - FF[..., -1:]
                m = DF.shape[-1]
                Am = DF.reshape(-1, m)
                bb = -FF[..., -1].reshape(-1)
                gamma, *_ = np.linalg.lstsq(Am, bb, rcond=1e-10)
                Ctry = np.tensordot(np.stack(hist_x + [Cn], axis=-1),
                                    np.append(gamma, 1.0 - gamma.sum()), axes=([-1], [0]))
                C = Ctry if np.max(np.abs(Ctry)) < 1e3 else Cn
            else:
                C = Cn
            it += 1
        if it >= max_iter:
            raise RuntimeError(f"solver not converged tau0={self.tau0} q={self.q}")
        EN = self.E_N_of(C)
        if not (EN > 0.3*(1.0-self.A0) and EN < 1e6):
            raise RuntimeError(f"solver nonsense E[N]={EN} tau0={self.tau0} q={self.q}")
        return EN, C, it, time.time()-t0

# ----------------------------------------------------------------------
# Closed-form O(tau0^2) coefficient of E[N] (analytic validation of surface)
#   E[N] = tau0(1+q/3) + c2 tau0^2 + O(tau0^3),
#   c2 = -(1+q/3)^2/2 + I,
#   I = int_0^1 (1+q r^2) (3/8) int_-1^1 (1+mu^2) [ s_w + q(r^2 s_w
#       + r mu s_w^2 + s_w^3/3) ] dmu dr,  s_w = -r mu + sqrt(r^2 mu^2 + 1 - r^2)
# ----------------------------------------------------------------------
def c2_analytic(q, nr=3000, nmu=400):
    r, wr = np.polynomial.legendre.leggauss(nr); r = 0.5*(r+1.0); wr = 0.5*wr
    mu, wmu = np.polynomial.legendre.leggauss(nmu)
    R, M = np.meshgrid(r, mu, indexing="ij")
    sw = -R*M + np.sqrt(R*R*M*M + 1.0 - R*R)
    Lw = sw + q*(R*R*sw + R*M*sw**2 + sw**3/3.0)
    inner = (3.0/8.0)*np.sum((1.0 + M*M)*Lw*wmu, axis=1)
    return -(1.0 + q/3.0)**2/2.0 + np.sum((1.0 + q*r*r)*inner*wr)

def c2_fit(q, geom, tau0s=(3e-4, 6e-4, 1.2e-3)):
    ys = []
    for t in tau0s:
        S = SurfaceSolver(geom, t, q)
        ys.append(S.solve(tol=1e-11)[0]/t)
    xs = np.array(tau0s)
    return np.polyfit(xs, np.array(ys), 1)[0]

def upres(C, g_old, g_new):
    """Resample C from g_old's (r x mu) grid onto g_new's grid.
    Separable bilinear interpolation (r linear, mu GL): first along mu at each
    old r, then along r for each new mu column."""
    r_o, r_n = g_old.r, g_new.r
    mu_o, mu_n = g_old.mu, g_new.mu
    tmp = np.empty((len(r_o), len(mu_n)))
    for l, mn in enumerate(mu_n):
        tmp[:, l] = np.array([np.interp(mn, mu_o, row) for row in C])
    out = np.empty((len(r_n), len(mu_n)))
    for l in range(len(mu_n)):
        out[:, l] = np.interp(r_n, r_o, tmp[:, l])
    return out

# ----------------------------------------------------------------------
def se(x):
    return float(np.std(x, ddof=1)/np.sqrt(len(x)))

CLOUDS = [  # (name, tau0, q, n, seed)
    ("C1", 1.0,  0.0, 1_000_000, 101),
    ("C2", 1.0,  3.0, 1_000_000, 102),
    ("C3", 1.0, 10.0, 1_000_000, 103),
    ("C4", 2.0,  3.0, 1_000_000, 104),
    ("C5", 0.5,  2.0, 1_000_000, 105),
]

def main():
    res = {"checks": {}, "measurements": {}, "inversion": {}, "test": {}}
    ok = True
    log("="*88)
    log("K04 OPACITY INVERSION + THREE-OBSERVABLE TEST  (family kappa = tau0(1+q r^2), T=1, central)")
    log("="*88)

    G = Geom(nr=700, nmu=72, ns=20, nseg_max=8)

    # ---- 0. closed-form O(tau0^2) coefficient: analytic vs solver ----
    log("\n[0] Surface validation -- closed-form O(tau0^2) coefficient c2")
    for q in (0.0, 3.0):
        ca = c2_analytic(q)
        cf = c2_fit(q, G)
        rel = abs(ca - cf)/max(1.0, abs(ca))
        okc = rel < 2e-2
        ok &= okc
        res["checks"][f"K0_c2_q{q:g}"] = bool(okc)
        res["measurements"][f"c2_q{q:g}"] = dict(analytic=ca, solver_fit=cf, rel=rel)
        log(f"  q={q}: c2 analytic={ca:+.8f}  solver fit={cf:+.8f}  rel={rel:.2e}  "
            f"{'PASS' if okc else 'FAIL'}")

    # ---- 1. grid certification: warm-started high-resolution solve ----
    log("\n[1] Surface grid certification (science 700x72 vs hi-res 1000x88)")
    grid_err = 0.0
    for (t, q) in [(1.0, 3.0), (1.0, 10.0)]:
        S1 = SurfaceSolver(G, t, q)
        e1, C1, _, _ = S1.solve(tol=1e-11)
        Gh = Geom(nr=1000, nmu=88, ns=24, nseg_max=10)
        e2 = SurfaceSolver(Gh, t, q).solve(tol=1e-10, C0=upres(C1, G, Gh),
                                           anderson=False)[0]
        d = abs(e1 - e2)/abs(e1)
        grid_err = max(grid_err, d)
        okc = d < 1e-4
        ok &= okc
        res["checks"][f"K1_grid_{t:g}_{q:g}"] = bool(okc)
        res["measurements"][f"grid_{t:g}_{q:g}"] = dict(science=e1,
                                                        hires=e2, rel=d)
        log(f"  tau0={t} q={q}: E[N]science={e1:.6f} E[N]hires={e2:.6f} "
            f"rel={d:.2e} {'PASS' if okc else 'FAIL'}")
    SURF_CERT = max(grid_err, 1e-6)*3.0   # conservative certified bound

    # ---- 2. clouds: measure, invert, predict, test ----
    warm = None
    for (name, tau0, q, n, seed) in CLOUDS:
        log(f"\n[2] Cloud {name}: tau0={tau0} q={q} n={n} seed={seed}")
        t0 = time.time()
        r = simulate(n, tau0, q, "central", seed)
        log(f"    engine run: {time.time()-t0:.1f}s")
        N = r["N"]; D = r["D"]; v2 = r["v2"]; ang = r["ang"]
        A = float(np.mean(N == 0)); sA = se(N == 0)
        ED = float(np.mean(D));  sD = se(D)
        Ev2 = float(np.mean(v2)); sv2 = se(v2)
        ENm = float(np.mean(N)); sNm = se(N)
        Eang = float(np.mean(ang))
        m = res["measurements"][name] = dict(
            A=A, sA=sA, E_D=ED, sD=sD, E_v2=Ev2, s_v2=sv2, E_N=ENm, s_N=sNm,
            E_ang=Eang, A_pred=float(np.exp(-tau0*(1.0+q/3.0))),
            ED_pred=float(tau0*(0.5+q/4.0)))

        # exact identities on the run
        zz1 = abs(Ev2 - 2.0*Eang)/(sv2 + 2.0*se(ang))
        zz2 = abs(Eang - ENm)/(se(ang) + sNm)
        zz3 = abs(A - m["A_pred"])/(sA + 1e-12)
        zz4 = abs(ED - m["ED_pred"])/(sD + 1e-12)
        for zz, key in ((zz1, "B1_Ev2_2Eang"), (zz2, "B2_Eang_EN"),
                        (zz3, "A_atom_law"), (zz4, "D_mean_law")):
            okc = zz < 6.0
            ok &= okc; res["checks"][f"{name}_{key}"] = bool(okc)
            log(f"    {key}: z={zz:5.2f} {'PASS' if okc else 'FAIL'}")

        # ---- (A) closed-form inversion ----
        tau0h = -3.0*math.log(A) - 4.0*ED
        qh = 4.0*ED/tau0h - 2.0
        stau = math.sqrt((3.0*sA/A)**2 + (4.0*sD)**2)
        sq = math.sqrt((4.0*sD/tau0h)**2 + (4.0*ED*stau/tau0h**2)**2)
        res["inversion"][name] = dict(tau0_hat=tau0h, s_tau0hat=stau,
                                      q_hat=qh, s_qhat=sq)
        zt = abs(tau0h - tau0)/stau
        zq = abs(qh - q)/sq
        okc = zt < 6.0 and zq < 6.0
        ok &= okc
        res["checks"][f"{name}_inv_tau0"] = bool(zt < 6.0)
        res["checks"][f"{name}_inv_q"] = bool(zq < 6.0)
        log(f"    INVERSION: tau0_hat={tau0h:.5f} +/- {stau:.5f} (z={zt:5.2f})  "
            f"q_hat={qh:+.5f} +/- {sq:.5f} (z={zq:5.2f})  {'PASS' if okc else 'FAIL'}")

        # ---- (B) third-observable prediction at (tau0_hat, q_hat) ----
        t1 = time.time()
        S = SurfaceSolver(G, tau0h, qh)
        EN_surf, Cstar, isteps, dt = S.solve(tol=1e-11, C0=warm)
        St = SurfaceSolver(G, tau0, q)
        EN_true, _, _, _ = St.solve(tol=1e-11, C0=Cstar)
        warm = Cstar
        zcv = abs(EN_true - ENm)/(sNm + SURF_CERT*EN_true)
        okc = zcv < 3.0
        ok &= okc; res["checks"][f"{name}_surf_vs_engine"] = bool(okc)
        log(f"    surface@true: E[N]={EN_true:.6f} vs engine {ENm:.6f}+-{sNm:.5f} "
            f"z={zcv:5.2f} {'PASS' if okc else 'FAIL'}  ({isteps}it {dt:.0f}s)")
        # prediction error: delta method from inversion SEs (no fitting);
        # plain-iteration solves (Anderson unstable on tiny perturbations)
        h1, h2 = 2e-3, 2e-3
        dtau = (SurfaceSolver(G, tau0h*(1+h1), qh).solve(tol=1e-9, C0=Cstar,
                                                          anderson=False)[0] -
                SurfaceSolver(G, tau0h*(1-h1), qh).solve(tol=1e-9, C0=Cstar,
                                                          anderson=False)[0]) / (2.0*h1*tau0h)
        dq = ((SurfaceSolver(G, tau0h, qh*(1+h2)).solve(tol=1e-9, C0=Cstar,
                                                         anderson=False)[0] -
               SurfaceSolver(G, tau0h, qh*(1-h2)).solve(tol=1e-9, C0=Cstar,
                                                         anderson=False)[0]) /
              (2.0*h2*qh)) if abs(qh) > 1e-9 else 0.0
        se_pred = abs(dtau)*stau + abs(dq)*sq + SURF_CERT*EN_surf
        Ev2_pred = 2.0*EN_surf
        z3o = abs(Ev2 - Ev2_pred)/(sv2 + se_pred)
        okc = z3o < 5.0
        ok &= okc; res["checks"][f"{name}_THIRD_OBSERVABLE"] = bool(okc)
        res["test"][name] = dict(E_v2_measured=Ev2, s_v2=sv2,
                                 E_v2_predicted=Ev2_pred, se_pred=se_pred,
                                 E_N_surface=EN_surf, z=z3o, dEN_dtau=dtau,
                                 dEN_dq=dq)
        log(f"    THIRD OBSERVABLE: measured E[v^2]={Ev2:.4f}+-{sv2:.4f} | "
            f"predicted 2*E[N](tau0h,qh)={Ev2_pred:.4f}+-{se_pred:.4f} | "
            f"z={z3o:5.2f}  {'PASS' if okc else 'FAIL'}")
        res["checks"][f"{name}_N_v2_identity"] = bool(
            abs(ENm - Ev2/2.0) < 6.0*(sNm + sv2/2.0))
        ok &= res["checks"][f"{name}_N_v2_identity"]

    # ---- 3. thin-cloud closed-form limit vs engine (bonus cloud) ----
    log("\n[3] Thin-cloud check: surface vs engine at tau0=0.05, q=0, n=4e6")
    r = simulate(4_000_000, 0.05, 0.0, "central", seed=201)
    N = r["N"]
    ENm = float(np.mean(N)); sNm = se(N)
    EN_s = SurfaceSolver(G, 0.05, 0.0).solve(tol=1e-11)[0]
    z = abs(EN_s - ENm)/(sNm + 1e-5*EN_s)
    okc = z < 3.0
    ok &= okc; res["checks"]["K3_thin_cloud"] = bool(okc)
    res["measurements"]["thin"] = dict(E_N_engine=ENm, s=sNm,
                                       E_N_surface=EN_s, z=z, leading=0.05)
    log(f"    surface E[N]={EN_s:.6f} engine {ENm:.6f}+-{sNm:.5f} z={z:5.2f} "
        f"{'PASS' if okc else 'FAIL'}  (leading 0.05, c2*tau0^2="
        f"{c2_analytic(0.0)*0.0025:.6f})")

    res["verdict"] = "PASS: all checks" if ok else "FAIL: see checks"
    res["surface_certified_rel_err"] = SURF_CERT
    with open("K04_results.json", "w") as fh:
        json.dump(res, fh, indent=2)
    log("\n" + "="*88)
    log(f"VERDICT: {'ALL CHECKS PASS' if ok else 'FAILURES PRESENT'}")
    log("="*88)
    return ok

if __name__ == "__main__":
    okf = main()
    with open("K04_inversion.out", "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    sys.exit(0 if okf else 1)