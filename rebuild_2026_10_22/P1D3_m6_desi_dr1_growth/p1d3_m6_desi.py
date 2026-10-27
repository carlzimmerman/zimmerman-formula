#!/usr/bin/env python3
"""P1D3_m6_desi_dr1_growth: X57's M6 at its bound vs DESI DR1 QMLE Lyman-alpha P1D, z 2.2-4.4, at DESI's own k cut.
Native linear gas model (P1D1 section 3) per z; full covariance (cross-z kept); joint nuisance fit.
FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md committed alone first (d50412913d).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I p1d3_m6_desi.py      (P1D3_MUTATE=1 twin)
"""
import os, sys, json, math, time, resource, hashlib, tarfile, io
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize, minimize_scalar, brentq, nnls
from scipy.interpolate import CubicSpline
from scipy.stats import chi2 as CHI2
from astropy.io import fits

MUT = os.environ.get("P1D3_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW = os.path.join(REPO, "_external_data", "desi_dr1_p1d_qmle", "raw", "data_points.tar")
T0 = time.time()
OUT = open(os.path.join(HERE, f"p1d3_m6_desi{TAG}.out"), "w")
RES = {"lane": "P1D3_m6_desi_dr1_growth", "criteria": "d50412913d", "mutate": MUT, "checks": {},
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; not theory closed"}
trapz = getattr(np, "trapezoid", None) or np.trapz


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


def dump():
    RES["elapsed_s"] = time.time() - T0
    RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    json.dump(RES, open(os.path.join(HERE, f"p1d3_m6_desi_results{TAG}.json"), "w"), indent=1, default=float)


FOOTS = ("canonical", "alt")
P("P1D3_m6_desi_dr1_growth" + (" [MUTATE m1-m3: control output, not physics]" if MUT else "") +
  ": criteria d50412913d; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")

# ============================================================== STEP 0
P("\n== STEP 0 (stop rule)")
s0 = {"S0a": hashlib.md5(open(RAW, "rb").read()).hexdigest() == "33d7fc21bfd3d745ed71a0bbe80ca433"}
with tarfile.open(RAW) as tf:
    HD = fits.open(io.BytesIO(tf.extractfile("desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits").read()))
    try:
        INFL = fits.open(io.BytesIO(tf.extractfile("cov_diag_inflation.fits").read()))[0].data.astype(float)
    except KeyError:
        INFL = None
T = HD["P1D_BLIND"].data
RES["blinding_header"] = HD["P1D_BLIND"].header.get("BLINDING")
Zall, Kall = np.asarray(T["Z"], float), np.asarray(T["K"], float)
DCOL = "PRAW" if MUT else "PLYA"                                             # m2
Pall = np.asarray(T[DCOL], float); Eall = np.asarray(T["E_PK"], float)
C_full = np.asarray(HD["COVARIANCE"].data, float)
C_stat = np.asarray(HD["COVARIANCE_STAT"].data, float); C_syst = np.asarray(HD["COVARIANCE_SYST"].data, float)
ZB = np.round(np.unique(Zall), 2)
s0["S0b"] = len(ZB) == 12 and abs(ZB[0] - 2.2) < 1e-6 and abs(ZB[-1] - 4.4) < 1e-6 and all((np.round(Zall, 2) == z).sum() == 85 for z in ZB)
CLIGHT, LLYA, DLAM = 299792.458, 1215.67, 0.8
kmaxz = lambda z: 0.5 * math.pi / (CLIGHT * DLAM / ((1 + z) * LLYA))


def selection(kcap=None, zmin=None):
    sel = np.zeros(len(Zall), bool)
    for z in ZB:
        if zmin is not None and z < zmin - 1e-9:
            continue
        km = kmaxz(z) if kcap is None else min(kmaxz(z), kcap)
        sel |= (np.round(Zall, 2) == z) & (Kall > 0.001) & (Kall < km)
    return sel


SEL = selection()
nper = {str(z): int((SEL & (np.round(Zall, 2) == z)).sum()) for z in ZB}
check("K1", s0["S0b"], f"12 z bins 2.2-4.4 x 85 rows; selected per z {nper} (total {SEL.sum()})", "12 x 85; DESI cut 0.001 < k < 0.5 pi/R_z")
Cs = C_full[np.ix_(SEL, SEL)]
sym = float(np.linalg.norm(Cs - Cs.T) / np.linalg.norm(Cs))
pd = bool(np.all(np.linalg.eigvalsh(0.5 * (Cs + Cs.T)) > 0))
sumdev = float(np.linalg.norm(C_full - (C_stat + C_syst)) / np.linalg.norm(C_full))
s0["S0c"] = sym <= 1e-8 and pd
RES["S0c"] = {"sym": sym, "posdef": pd, "full_vs_stat_plus_syst": sumdev}
P(f"  S0c COVARIANCE symmetric {sym:.1e}, positive definite {pd}; ||FULL - (STAT + SYST)|| / ||FULL|| = {sumdev:.2e}")
r_full = np.sqrt(np.diag(C_full))[SEL] / Eall[SEL]
r_stat = np.sqrt(np.diag(C_stat))[SEL] / Eall[SEL]
s0["S0d"] = bool(np.all(np.abs(r_full - 1) <= 0.15))
RES["S0d"] = {"full_max": float(np.max(np.abs(r_full - 1))), "stat_max": float(np.max(np.abs(r_stat - 1)))}
P(f"  S0d sqrt(diag COV)/E_PK: FULL max |r-1| {RES['S0d']['full_max']:.3f}, STAT {RES['S0d']['stat_max']:.3f} (FULL must be <= 0.15)")
if not s0["S0d"] and np.all(np.abs(r_stat - 1) <= 0.15):
    P("  S0d: E_PK matches COVARIANCE_STAT, not COVARIANCE: quantity match ambiguous -> STOP (frozen)")

# native background + M6 (P1D1 re-implementation)
P1 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/P1D1_m6_boera_high_z_forest/p1d1_m6_boera_results.json")))
X22 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")))
FMAX = {f: X22["step2"]["per_footing"][f]["f_max"] for f in FOOTS}
RL = X22["step2"]["per_footing"]["canonical"]["R_L_Mpc_h"][2]
KG = np.logspace(-4, math.log10(200.0), 60001)
LNK = np.log(KG)
W = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
W2G = W(KG * RL) ** 2
VP = 4 * math.pi * RL ** 3 / 3


class BG:
    def __init__(self, name, OM, OB, h, ns, s8, shape=None):
        self.name, self.OM, self.OB, self.h, self.ns = name, OM, OB, h, ns
        self.OL, self.RRAT = 1 - OM, (OM - OB) / OB
        sOM, sOB, sh = shape if shape is not None else (OM, OB, h)
        Gam = sOM * sh * np.exp(-sOB * (1.0 + np.sqrt(2 * sh) / sOM))
        Tk = lambda kk: (np.log(1 + 2.34 * kk / Gam) / (2.34 * kk / Gam) * (1 + 3.89 * kk / Gam + (16.1 * kk / Gam) ** 2
                         + (5.46 * kk / Gam) ** 3 + (6.71 * kk / Gam) ** 4) ** -0.25)
        kf = np.logspace(-4, 3, 4000)
        shp = kf ** (3 + ns) * Tk(kf) ** 2
        NORM = s8 ** 2 / trapz(shp * W(kf * 8.0) ** 2, np.log(kf))
        self.s2R0 = NORM * trapz(shp * W(kf * RL) ** 2, np.log(kf))
        self.PAD0_G = 2 * math.pi ** 2 * NORM * KG ** (3 + ns) * Tk(KG) ** 2 / KG ** 3
        self.D0 = self._D(1.0)
        D3 = self.Dz(3.0)
        self.m6 = {}
        for f in FOOTS:
            dci = -(1 - FMAX[f]); dbi = -self.RRAT * dci
            Fb3 = 0.2 * self.s2R0 * D3 ** 2 / (dbi ** 2 / (1 + dbi))
            fV = Fb3 / (1 + dbi)
            self.m6[f] = {"delta_b_in": dbi, "f_V": fV, "Fb_max_z3": Fb3, "A": fV * dbi ** 2 * VP}

    def Ez(self, z):
        return math.sqrt(self.OM * (1 + z) ** 3 + self.OL)

    def _D(self, a):
        Ea = lambda x: math.sqrt(self.OM * x ** -3 + self.OL)
        return 2.5 * self.OM * Ea(a) * quad(lambda x: 1.0 / (x * Ea(x)) ** 3, 0, a, epsabs=0, epsrel=1e-12, limit=400)[0]

    def Dz(self, z):
        return self._D(1 / (1 + z)) / self.D0

    def kh(self, kv, z):
        return kv * 100.0 * self.Ez(z) / (1 + z)


def p1d(p3d_on_grid, kpar):
    f = KG ** 2 * p3d_on_grid
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(LNK))])
    return (cum[-1] - np.interp(np.log(kpar), LNK, cum)) / (2 * math.pi)


NAT_OM, NAT_h, NAT_wb = 0.2976016, 0.6856427, 0.0223081
NAT = BG("native", NAT_OM, NAT_wb / NAT_h ** 2, NAT_h, 0.965, 0.827959)
INH = BG("inherited", 0.0493 * 6.364, 0.0493, 0.674, 0.965, 0.82742, shape=(0.315, 0.0493, 0.674))
ok_e, txt = [], []
for f in FOOTS:
    ref = P1["backgrounds"]["native"]["m6"][f]
    for key, mine in (("delta_b_in", NAT.m6[f]["delta_b_in"]), ("f_V", NAT.m6[f]["f_V"]), ("Fb_max_z3", NAT.m6[f]["Fb_max_z3"]), ("A", NAT.m6[f]["A"])):
        tgt = ref[key] * (1.01 if (MUT and f == "canonical" and key == "f_V") else 1.0)       # m3
        ok_e.append(round(mine, 4) == round(tgt, 4)); txt.append(f"{f} {key} {mine:.5f}/{tgt:.5f}")
s0["S0e"] = all(ok_e)
P(f"  S0e P1D1 native M6 reproduced (4 dp): {sum(ok_e)}/{len(ok_e)}")
check("S0", all(s0.values()), f"{s0}", "all Step-0 items")
RES["step0"] = {"items": s0, "S0e": txt, "selected_per_z": nper}
if not all(s0.values()) and not MUT:
    P("STOP: Step 0 failed; nothing graded."); RES["verdict"] = "STOPPED AT STEP 0"; dump(); sys.exit(1)
check("K5", all(abs(NAT.kh(0.01, z) - 0.01 * 100 * NAT.Ez(z) / (1 + z)) <= 1e-12 for z in ZB),
      f"native k(0.01 s/km, z 2.2 / 4.4) = {NAT.kh(0.01, 2.2):.5f} / {NAT.kh(0.01, 4.4):.5f} h/Mpc", "exact")

# ============================================================== model tables (spline in R_J)
RJG = np.linspace(0.02, 0.30, 141)
KP = 0.01
SIGN = -1.0 if MUT else 1.0                                                   # m1


class Analysis:
    def __init__(self, name, bg, foot, sel, cov, tilt=True, smoothz=False, mu_per_z=False):
        self.name, self.bg, self.foot, self.tilt, self.smoothz, self.mu_per_z = name, bg, foot, tilt, smoothz, mu_per_z
        self.sel = sel
        self.zs = [z for z in ZB if (sel & (np.round(Zall, 2) == z)).any()]
        self.idx = {z: np.where(sel & (np.round(Zall, 2) == z))[0] for z in self.zs}
        order = np.concatenate([self.idx[z] for z in self.zs])
        self.order = order
        self.d = Pall[order]
        C = cov[np.ix_(order, order)]
        self.L = np.linalg.cholesky(np.linalg.inv(C))                         # whitening: chi2 = |L^T r|^2
        self.WT = self.L.T
        self.sl = {}
        o = 0
        for z in self.zs:
            n = len(self.idx[z]); self.sl[z] = slice(o, o + n); o += n
        A = bg.m6[foot]["A"]
        self.spl = {}
        for z in self.zs:
            kv = Kall[self.idx[z]]; kh = bg.kh(kv, z); D2 = bg.Dz(z) ** 2
            pa = np.empty((len(RJG), len(kv))); pi = np.empty_like(pa)
            for i, rj in enumerate(RJG):
                filt = np.exp(-KG ** 2 * rj ** 2)
                pa[i] = p1d(bg.PAD0_G * D2 * filt, kh); pi[i] = p1d(A * W2G * filt, kh)
            self.spl[z] = (CubicSpline(RJG, np.log(pa), axis=0), CubicSpline(RJG, np.log(pi), axis=0), kv)
        self.nz = len(self.zs)

    def shapes(self, theta, mu):
        """theta -> per-z (RJ, alpha); returns column matrix M (nbins x nz) of unit-amplitude shapes."""
        if self.smoothz:
            r0, r1, a0, a1 = theta
            rj = {z: float(np.clip(r0 + r1 * (z - 3.3), 0.02, 0.30)) for z in self.zs}
            al = {z: float(np.clip(a0 + a1 * (z - 3.3), -1, 1)) if self.tilt else 0.0 for z in self.zs}
        else:
            k = 2 if self.tilt else 1
            rj = {z: float(theta[k * i]) for i, z in enumerate(self.zs)}
            al = {z: float(theta[k * i + 1]) if self.tilt else 0.0 for i, z in enumerate(self.zs)}
        M = np.zeros((len(self.d), self.nz))
        for j, z in enumerate(self.zs):
            sa, si, kv = self.spl[z]
            muz = mu[j] if self.mu_per_z else mu
            M[self.sl[z], j] = (kv / KP) ** al[z] * (np.exp(sa(rj[z])) + SIGN * muz * np.exp(si(rj[z])))
        return M

    def chi(self, theta, mu, d=None, ret=False):
        d = self.d if d is None else d
        M = self.shapes(theta, mu)
        A_ = self.WT @ M
        sc = np.linalg.norm(A_, axis=0)
        sc[~np.isfinite(sc) | (sc <= 0)] = 1.0
        y, _ = nnls(A_ / sc, self.WT @ d, maxiter=5000)                   # column-scaled for conditioning
        b2 = y / sc
        r_ = self.WT @ (d - M @ b2)
        c = float(r_ @ r_)
        return (c, b2) if ret else c

    def bounds(self):
        if self.smoothz:
            return [(0.02, 0.30), (-0.2, 0.2), (-1, 1) if self.tilt else (0, 0), (-1, 1) if self.tilt else (0, 0)]
        b = []
        for _ in self.zs:
            b.append((0.02, 0.30))
            if self.tilt: b.append((-1, 1))
        return b

    def nnuis(self):
        return self.nz + (4 if self.smoothz else self.nz * (2 if self.tilt else 1))

    def start(self, mu, d):
        if self.smoothz:
            best = None
            for r0 in (0.05, 0.1, 0.18):
                for a0 in ((-0.3, 0.0, 0.3) if self.tilt else (0.0,)):
                    th = np.array([r0, 0.0, a0, 0.0]); c = self.chi(th, mu, d)
                    if best is None or c < best[0]: best = (c, th)
            return best[1]
        # per z coarse grid, block approximation, then joint
        th = []
        for z in self.zs:
            best = None
            for rj in (0.03, 0.06, 0.1, 0.15, 0.22):
                for a in ((-0.5, -0.2, 0.0, 0.2, 0.5) if self.tilt else (0.0,)):
                    one = {zz: (0.1, 0.0) for zz in self.zs}; one[z] = (rj, a)
                    t = np.array([v for zz in self.zs for v in (one[zz] if self.tilt else one[zz][:1])])
                    c = self.chi(t, mu, d)
                    if best is None or c < best[0]: best = (c, (rj, a))
            th += list(best[1] if self.tilt else best[1][:1])
        return np.array(th)

    def prof(self, mu, d=None, x0=None):
        d = self.d if d is None else d
        x0 = self.start(mu, d) if x0 is None else x0
        bnd = self.bounds()
        r = minimize(lambda t: self.chi(t, mu, d), x0, method="L-BFGS-B", bounds=bnd,
                     options={"maxiter": 3000, "ftol": 1e-12, "gtol": 1e-8, "maxfun": 60000})
        r2 = minimize(lambda t: self.chi(t, mu, d), r.x, method="Powell", bounds=bnd, options={"xtol": 1e-5, "ftol": 1e-9, "maxfev": 20000})
        x = r2.x if r2.fun <= r.fun else r.x
        return float(min(r.fun, r2.fun)), x

    def predict(self, theta, mu, b2):
        return self.shapes(theta, mu) @ b2


def mu_scan(an, d=None, warm=None):
    MUG = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 15.0]
    ch, xs = {}, {}
    x = warm
    for m in MUG:
        c, x = an.prof(m, d, x); ch[m] = c; xs[m] = x
    ms = sorted(ch); cs = [ch[m] for m in ms]; i = int(np.argmin(cs))
    lo, hi = ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)]
    f = lambda m: an.prof(m, d, xs[ms[i]])[0]
    r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-3})
    muh, cmin = (float(r.x), float(r.fun)) if r.fun < cs[i] else (ms[i], cs[i])
    mu95 = None
    up = [m for m in ms if m > muh and ch[m] - cmin > 3.84]
    if up:
        try:
            mu95 = float(brentq(lambda m: f(m) - cmin - 3.84, muh, up[0], xtol=1e-3))
        except ValueError:
            mu95 = None
    return {"mu_hat": muh, "chi2_min": cmin, "chi2_mu0": ch[0.0], "chi2_mu1": ch[1.0], "dchi2_1": ch[1.0] - cmin,
            "dchi2_0": ch[0.0] - cmin, "mu95": mu95, "grid": {str(k): v for k, v in ch.items()}}


def analyse(an, label, planted=False):
    c0, x0 = an.prof(0.0)
    _, b20 = an.chi(x0, 0.0, ret=True)
    nb = len(an.d); dof = nb - an.nnuis()
    pj = float(CHI2.sf(c0, dof))
    r0 = an.d - an.predict(x0, 0.0, b20)
    perz = {}
    Cfull_inv = an.WT.T @ an.WT
    for j, z in enumerate(an.zs):
        s = an.sl[z]
        Cz = np.linalg.inv(Cfull_inv)[s, s]
        cz = float(r0[s] @ np.linalg.solve(Cz, r0[s]))
        dz = (s.stop - s.start) - (1 + (0 if an.smoothz else (2 if an.tilt else 1)))
        perz[str(z)] = {"chi2": cz, "dof": dz, "p": float(CHI2.sf(cz, dz))}
    G0 = pj >= 0.01 and all(v["p"] >= 0.001 for v in perz.values())
    asim = an.predict(x0, 0.0, b20)
    cA1, _ = an.prof(1.0, asim, x0); cA0, _ = an.prof(0.0, asim, x0)
    dA = cA1 - cA0; G1 = dA >= 9
    sc = mu_scan(an, warm=x0)
    cls = ("NOT DIAGNOSTIC (LINEAR NATIVE MODEL INADEQUATE)" if not G0 else "NOT DIAGNOSTIC (NUISANCE ABSORBS M6)" if not G1
           else "M6 AT X57's BOUND EXCLUDED" if sc["dchi2_1"] >= 9 else "M6-SHAPED EXCESS PRESENT" if sc["dchi2_0"] >= 9 else "NOT EXCLUDED")
    Fb = an.bg.m6[an.foot]["Fb_max_z3"]
    out = {"class": cls, "G0": {"pass": G0, "chi2": c0, "dof": dof, "p": pj, "per_z": perz}, "G1": {"pass": G1, "dchi2_asimov": dA},
           "scan": sc, "Fb_max_z3": Fb, "Fb_95": None if sc["mu95"] is None else sc["mu95"] * Fb, "nbins": nb}
    worst = sorted(perz.items(), key=lambda kv: kv[1]["p"])[:3]
    P(f"  [{label}] {cls}")
    P(f"     G0 null chi2 {c0:.1f} / {dof} dof, p {pj:.3g}; worst z: " + ", ".join(f"z{z} {v['chi2']:.1f}/{v['dof']} p {v['p']:.2g}" for z, v in worst))
    P(f"     G1 Asimov {dA:.2f}; mu_hat {sc['mu_hat']:.4f}, dchi2(mu=1) {sc['dchi2_1']:.2f}, dchi2(mu=0) {sc['dchi2_0']:.2f}, mu95 "
      + ("none" if sc["mu95"] is None else f"{sc['mu95']:.4f} -> F_b <= {sc['mu95'] * Fb:.5f} (bound {Fb:.5f})"))
    if planted:
        rng = np.random.default_rng(0)
        Csel = np.linalg.inv(an.WT.T @ an.WT)
        noise = rng.multivariate_normal(np.zeros(nb), Csel)
        _, b21 = an.chi(x0, 1.0, ret=True)
        pl1 = an.predict(x0, 1.0, b20) + noise
        pl0 = an.predict(x0, 0.0, b20) + noise
        s1 = mu_scan(an, pl1, x0); s0p = mu_scan(an, pl0, x0)
        out["K3"] = {"pass": (0.5 <= s1["mu_hat"] <= 1.5 and s1["dchi2_0"] >= 9) if G1 else True, "vacuous": not G1, "scan": s1}
        out["K4"] = {"pass": (s0p["mu95"] is not None and s0p["mu95"] < 1) if G1 else True, "vacuous": not G1, "scan": s0p}
    return out, x0


# ============================================================== runs
RES["footings"] = {}
for f in FOOTS:
    P(f"\n== {f.upper()} footing")
    an = Analysis("primary", NAT, f, SEL, C_full)
    if f == "canonical":
        Mz = an.shapes(an.start(0.0, an.d), 0.0)
        k2 = float(np.max(np.abs(an.shapes(np.zeros(1) + an.start(0.0, an.d), 0.0) - Mz)))
        check("K2", k2 == 0.0, "mu = 0 shapes reproducible and patch-free", "== 0")
    prim, x0 = analyse(an, "PRIMARY", planted=(f == "canonical"))
    fr = {"primary": prim, "variants": {}}
    if f == "canonical":
        check("K3", prim["K3"]["pass"], f"planted mu=1: mu_hat {prim['K3']['scan']['mu_hat']:.3f}, dchi2_0 {prim['K3']['scan']['dchi2_0']:.2f} (vacuous {prim['K3']['vacuous']})",
              "mu_hat in [0.5, 1.5], dchi2_0 >= 9 when G1 passes")
        check("K4", prim["K4"]["pass"], f"planted null: mu95 {prim['K4']['scan']['mu95']} (vacuous {prim['K4']['vacuous']})", "mu95 < 1 when G1 passes")
    VAR = [("V-k02", dict(sel=selection(kcap=0.02))), ("V-stat", dict(cov=C_stat)),
           ("V-ns 0.92", dict(bg=BG("ns0.92", NAT_OM, NAT_wb / NAT_h ** 2, NAT_h, 0.92, 0.827959))),
           ("V-ns 1.00", dict(bg=BG("ns1.00", NAT_OM, NAT_wb / NAT_h ** 2, NAT_h, 1.00, 0.827959))),
           ("V-tilt0", dict(tilt=False)), ("V-smoothz", dict(smoothz=True)), ("V-hiz", dict(sel=selection(zmin=3.6)))]
    for vn, kw in VAR:
        a = Analysis(vn, kw.get("bg", NAT), f, kw.get("sel", SEL), kw.get("cov", C_full), tilt=kw.get("tilt", True), smoothz=kw.get("smoothz", False))
        fr["variants"][vn] = analyse(a, vn)[0]
    fr["inherited_reported"] = analyse(Analysis("inherited", INH, f, SEL, C_full), "V-inherited (reported)")[0]
    if INFL is not None and INFL.shape == (1020,) and np.all(INFL >= 1):
        D = np.diag(np.sqrt(INFL)); fr["inflation_reported"] = analyse(Analysis("infl", NAT, f, SEL, D @ C_full @ D), "V-inflation (reported)")[0]
    else:
        fr["inflation_reported"] = f"not applied (shape {None if INFL is None else INFL.shape}, min {None if INFL is None else float(INFL.min())})"
        P(f"  [V-inflation] {fr['inflation_reported']}")
    if f == "canonical":
        # per-z mu (reported only): does any excess follow 1/D^2?
        apz = Analysis("perz", NAT, f, SEL, C_full, mu_per_z=True)
        best = None
        def fz(v):
            th, mz = v[:-apz.nz], v[-apz.nz:]
            return apz.chi(th, mz)
        x = np.concatenate([x0, np.full(apz.nz, 0.5)])
        bnd = apz.bounds() + [(0.0, 15.0)] * apz.nz
        r = minimize(fz, x, method="L-BFGS-B", bounds=bnd, options={"maxiter": 5000, "maxfun": 200000})
        muz = {str(z): float(m) for z, m in zip(apz.zs, r.x[-apz.nz:])}
        fr["per_z_mu_reported"] = {"mu": muz, "chi2": float(r.fun)}
        P("  [reported] per-z mu_hat (mu >= 0): " + ", ".join(f"z{z} {m:.2f}" for z, m in muz.items()))
    classes = {v["class"] for v in fr["variants"].values()} | {prim["class"]}
    flips = [k for k, v in fr["variants"].items() if v["class"] != prim["class"]]
    fr["verdict"] = prim["class"] + (" (ROBUST)" if not flips else f" (FRAGILE: flips in {', '.join(flips)})")
    P(f"  ==> {f}: {fr['verdict']}")
    RES["footings"][f] = fr
    dump()

peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
check("K6", peak < 1.0, f"peak RSS {peak:.3f} GB, 1 thread, {time.time() - T0:.0f} s", "< 1 GB")
P("\n== VERDICT")
for f in FOOTS:
    P(f"  {f}: {RES['footings'][f]['verdict']}")
P(f"  checks {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])}")
dump()
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
