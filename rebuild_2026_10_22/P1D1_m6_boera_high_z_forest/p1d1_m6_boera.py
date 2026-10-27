#!/usr/bin/env python3
"""P1D1_m6_boera_high_z_forest: does the measured z 4.2/4.6/5.0 Lyman-alpha flux power (Boera et al. 2019) allow X57's
M6 (displacement) at X57's bound? Linear native gas model with per-z nuisance (b^2, R_J, tilt); common M6 amplitude mu.
FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md committed alone first (8f6e3db4bc); AMENDMENTS.md A1 (e6d278b747).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I p1d1_m6_boera.py      (P1D1_MUTATE=1 twin)
"""
import os, sys, json, math, time, resource, re, hashlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize, minimize_scalar, brentq
from scipy.stats import chi2 as CHI2

MUT = os.environ.get("P1D1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(REB, ".."))
DATA = os.path.join(REPO, "_external_data", "boera2019_p1d", "raw")
T0 = time.time()
OUT = open(os.path.join(HERE, f"p1d1_m6_boera{TAG}.out"), "w")
RES = {"lane": "P1D1_m6_boera_high_z_forest", "criteria": "8f6e3db4bc", "amendments": ["A1 e6d278b747", "A2 (see AMENDMENTS.md)"], "mutate": MUT,
       "checks": {}, "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, "
                                 "never a particle; not theory closed"}
trapz = getattr(np, "trapezoid", None) or np.trapz


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


def J(rel):
    return json.load(open(os.path.join(REPO, rel)))


def dump():
    RES["elapsed_s"] = time.time() - T0
    RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # bytes on darwin
    json.dump(RES, open(os.path.join(HERE, f"p1d1_m6_boera_results{TAG}.json"), "w"), indent=1, default=float)


FOOTS = ("canonical", "alt")
ZS = ("4.2", "4.6", "5.0")
P("P1D1_m6_boera_high_z_forest" + (" [MUTATE m1-m3: control output, not physics]" if MUT else "") +
  ": criteria 8f6e3db4bc + A1 e6d278b747; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")

# ============================================================== STEP 0
P("\n== STEP 0 (stop rule)")
SHA = {"src_1809.06980v2.tar.gz": "9583568fe3076be9687567f54e81716a8dd452b4061da1e9476e1d299931f1a8",
       "Cov_Matrixz=4.2.dat": "872daaf273d3f212968b750b5b263c4b03c3cd57091b144ae120a480e76bb4dc",
       "Cov_Matrixz=4.6.dat": "44e75dc183fab9083add6a924dd3b2787869c2579bc1ea152592c1e864d261ed",
       "Cov_Matrixz=5.0.dat": "c44356e7f2f05d47a4a20dd274fc1d5f7812f09f8327636322c89063ff167d05"}
s0 = {}
s0["S0a"] = all(hashlib.sha256(open(os.path.join(DATA, f), "rb").read()).hexdigest() == h for f, h in SHA.items())
P(f"  S0a checksums: {'OK' if s0['S0a'] else 'MISMATCH'}")

import tarfile
with tarfile.open(os.path.join(DATA, "src_1809.06980v2.tar.gz")) as tf:
    TEX = tf.extractfile("PSpaperApJRef_New.tex").read().decode("utf-8", "replace")
TAB = {}
for z in ZS:
    lab = TEX.index("\\label{table:%sbin}" % z)
    beg = TEX.rindex("\\begin{tabular}", 0, lab)
    body = TEX[beg:lab]
    rows = []
    for line in body.splitlines():
        m = re.match(r"^\s*(-?\d+\.\d+)\s*&\s*([0-9.eE+-]+)\s*&\s*([0-9.eE+-]+)\s*&\s*([0-9.eE+-]+)\s*\\\\", line)
        if m:
            rows.append([float(v) for v in m.groups()])
    TAB[z] = np.array(rows)
ok_b = all(TAB[z].shape == (16, 4) and np.max(np.abs(TAB[z][:, 0] - np.round(np.arange(-2.2, -0.65, 0.1), 1))) <= 0.01
           and np.all(TAB[z][:, 1:3] > 0) for z in ZS)
s0["S0b"] = ok_b
check("K1", ok_b, "; ".join(f"z {z}: {TAB[z].shape[0]} rows, logk {TAB[z][0, 0]}..{TAB[z][-1, 0]}" for z in ZS),
      "16 rows, logk -2.2..-0.7 step 0.1, P > 0")
COV = {z: np.asfortranarray(np.load(os.path.join(DATA, f"Cov_Matrixz={z}.dat"))) for z in ZS}
ok_c = True
for z in ZS:
    C = COV[z]
    asym = float(np.max(np.abs(C - C.T)) / np.max(np.abs(C)))
    pd = bool(np.all(np.linalg.eigvalsh(0.5 * (C + C.T)) > 0))
    ok_c &= C.shape == (16, 16) and asym <= 1e-8 and pd
s0["S0c"] = ok_c
P(f"  S0c covariances 16x16 symmetric positive definite: {ok_c}")
qm = {z: float(np.max(np.abs(np.sqrt(np.diag(COV[z])) / TAB[z][:, 3] - 1))) for z in ZS}
s0["S0d"] = all(v <= 0.15 for v in qm.values())
P(f"  S0d sqrt(diag Cov) vs table sigma, max |ratio - 1|: " + ", ".join(f"z {z} {v:.2e}" for z, v in qm.items()) + " (<= 0.15; quantity = P_k in km/s)")
COL = 1 if MUT else 2                                               # m2: uncorrected column
KV = {z: 10 ** TAB[z][:, 0] for z in ZS}                            # s/km
DAT = {z: TAB[z][:, COL] for z in ZS}

# ============================================================== cosmology / M6 (re-implementation of X57 L399-428, X63 L147-206)
X57 = J("rebuild_2026_10_22/X57_exclusion_mechanism/x57_exclusion_results.json")
X22 = J("rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")
X63 = J("rebuild_2026_10_22/X63_displacement_forest_prediction/x63_m6_forest_results.json")
FMAX = {f: X22["step2"]["per_footing"][f]["f_max"] for f in FOOTS}
RL = X22["step2"]["per_footing"]["canonical"]["R_L_Mpc_h"][2]
KMAX = 200.0
KG = np.logspace(-4, math.log10(KMAX), 60001)
LNK = np.log(KG)
W = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
W2G = W(KG * RL) ** 2
VP = 4 * math.pi * RL ** 3 / 3


class BG:
    def __init__(self, name, OM, OB, h, ns, s8, shape=None):
        """shape = (Om, Ob, h) for the BBKS shape if it differs from the background (X57/X63 inherited: A2)."""
        self.name, self.OM, self.OB, self.h, self.ns, self.s8 = name, OM, OB, h, ns, s8
        self.OL = 1 - OM
        self.RRAT = (OM - OB) / OB
        sOM, sOB, sh = shape if shape is not None else (OM, OB, h)
        self.shape = (sOM, sOB, sh)
        Gam = sOM * sh * np.exp(-sOB * (1.0 + np.sqrt(2 * sh) / sOM))
        self.Tk = lambda kk: (np.log(1 + 2.34 * kk / Gam) / (2.34 * kk / Gam) * (1 + 3.89 * kk / Gam + (16.1 * kk / Gam) ** 2
                              + (5.46 * kk / Gam) ** 3 + (6.71 * kk / Gam) ** 4) ** -0.25)
        kf = np.logspace(-4, 3, 4000)
        shape = kf ** (3 + ns) * self.Tk(kf) ** 2
        self.NORM = s8 ** 2 / trapz(shape * W(kf * 8.0) ** 2, np.log(kf))
        self.s2R0 = self.NORM * trapz(shape * W(kf * RL) ** 2, np.log(kf))
        self.D0 = self._D(1.0)
        self.D3 = self.Dz(3.0)
        self.PAD0_G = 2 * math.pi ** 2 * self.NORM * KG ** (3 + ns) * self.Tk(KG) ** 2 / KG ** 3
        self.m6 = {}
        for f in FOOTS:
            dci = -(1 - FMAX[f])
            dbi = -self.RRAT * dci
            per = dbi ** 2 / (1 + dbi)
            Fb3 = 0.2 * self.s2R0 * self.D3 ** 2 / per
            fV = Fb3 / (1 + dbi)
            self.m6[f] = {"delta_c_in": dci, "delta_b_in": dbi, "fV_max": 1.0 / (1.0 + self.RRAT * (1 - FMAX[f])),
                          "Fb_max_z3": Fb3, "Fb_max_z2": 0.2 * self.s2R0 * self.Dz(2.0) ** 2 / per, "f_V": fV,
                          "A": fV * dbi ** 2 * VP}

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
    tail = cum[-1] - np.interp(np.log(kpar), LNK, cum)
    return tail / (2 * math.pi)


def spectra(bg, A, z, kh, RJ):
    """(P1D_ad, P1D_iso) in (Mpc/h) at kh, gas filter exp(-k^2 RJ^2) in power."""
    filt = np.exp(-KG ** 2 * RJ ** 2)
    return p1d(bg.PAD0_G * bg.Dz(z) ** 2 * filt, kh), p1d(A * W2G * filt, kh)


INH = BG("inherited", 0.0493 * 6.364, 0.0493, 0.674, 0.965, 0.82742, shape=(0.315, 0.0493, 0.674))
NAT_OM, NAT_h, NAT_wb = 0.2976016, 0.6856427, 0.0223081
NAT = BG("native", NAT_OM, NAT_wb / NAT_h ** 2, NAT_h, 0.965, 0.827959)

# S0e: reproduce X63's committed max S at R_J 0.1 on the X63 KV grid, and F_b,max(z 3)
KV63 = np.array(X63["KV_s_per_km"])
s0e, s0e_txt = [], []
for f in FOOTS:
    for z in ZS:
        pa, pi = spectra(INH, INH.m6[f]["A"], float(z), INH.kh(KV63, float(z)), 0.1)
        mine = float(np.max(pi / pa))
        tgt = float(np.max(X63["footings"][f]["pred"]["0.1"]["S"][z])) * (1.01 if (MUT and f == "canonical" and z == "4.2") else 1.0)   # m3
        s0e.append(round(mine, 3) == round(tgt, 3)); s0e_txt.append(f"{f} z{z} {mine:.4f}/{tgt:.4f}")
    fb_t = X57["M6"][f]["Fb_max"]["3.0"]
    s0e.append(round(INH.m6[f]["Fb_max_z3"], 3) == round(fb_t, 3) and abs(INH.m6[f]["Fb_max_z3"] / fb_t - 1) <= 1e-3)
    s0e_txt.append(f"{f} Fb3 {INH.m6[f]['Fb_max_z3']:.5f}/{fb_t:.5f}")
s0["S0e"] = all(s0e)
P(f"  S0e X63/X57 reproduced (3 dp): {sum(s0e)}/{len(s0e)}: " + "; ".join(s0e_txt))
check("S0", all(s0.values()), f"{s0}", "all Step-0 items")
RES["step0"] = {"items": s0, "S0d_max_rel": qm, "S0e": s0e_txt}
if not all(s0.values()) and not MUT:
    P("STOP: Step 0 failed; nothing graded.")
    RES["verdict"] = "STOPPED AT STEP 0"
    dump(); sys.exit(1)

for bg in (INH, NAT):
    P(f"  [{bg.name}] Om {bg.OM:.5f} Ob {bg.OB:.5f} h {bg.h:.5f} ns {bg.ns} s8 {bg.s8}; Oc/Ob {bg.RRAT:.4f}; "
      f"sigma2_ad(R_L, 0) {bg.s2R0:.4f}; " + "; ".join(f"{f}: d_c,in {bg.m6[f]['delta_c_in']:+.4f} d_b,in {bg.m6[f]['delta_b_in']:+.4f} "
      f"Fb3 {bg.m6[f]['Fb_max_z3']:.5f} f_V {bg.m6[f]['f_V']:.5f} (<= {bg.m6[f]['fV_max']:.4f}) A {bg.m6[f]['A']:.5f}" for f in FOOTS))
RES["backgrounds"] = {bg.name: {"OM": bg.OM, "OB": bg.OB, "h": bg.h, "ns": bg.ns, "s8": bg.s8, "Oc_over_Ob": bg.RRAT,
                                "sigma2_ad_RL_z0": bg.s2R0, "m6": bg.m6} for bg in (INH, NAT)}
k5 = abs(NAT.kh(0.01, 5.0) - 100 * NAT.Ez(5.0) / 6 * 0.01) <= 1e-12
check("K5", k5, f"native k(0.01 s/km, z 5) = {NAT.kh(0.01, 5.0):.6f} h/Mpc", "exact")

# ============================================================== fitting machinery
RJG = np.round(np.arange(0.02, 0.30 + 1e-9, 0.002), 6)
ALG = np.round(np.arange(-1.0, 1.0 + 1e-9, 0.02), 6)
KP = 0.03
SIGN = -1.0 if MUT else 1.0                                         # m1


class Setup:
    """One analysis configuration: background, bin mask, covariance mode, nuisance options."""

    def __init__(self, name, bg, foot, kmax=None, diag=False, tilt=True, rjfix=None, data=None):
        self.name, self.bg, self.foot, self.tilt, self.rjfix = name, bg, foot, tilt, rjfix
        self.A = bg.m6[foot]["A"]
        self.z = {}
        for z in ZS:
            msk = np.ones(16, bool) if kmax is None else KV[z] <= kmax * (1 + 1e-9)
            C = COV[z][np.ix_(msk, msk)]
            if diag:
                C = np.diag(np.diag(C))
            kv = KV[z][msk]; kh = bg.kh(kv, float(z))
            rjs = np.array([rjfix]) if rjfix is not None else RJG
            pa = np.empty((len(rjs), msk.sum())); pi = np.empty_like(pa)
            for i, rj in enumerate(rjs):
                pa[i], pi[i] = spectra(bg, self.A, float(z), kh, rj)
            als = ALG if tilt else np.array([0.0])
            T = (kv[None, :] / KP) ** als[:, None]
            self.z[z] = {"msk": msk, "Ci": np.linalg.inv(C), "kv": kv, "kh": kh, "rjs": rjs, "als": als,
                         "pa": pa, "pi": pi, "T": T, "d": (DAT[z] if data is None else data[z])[msk]}

    def model_shape(self, z, mu, rj, al):
        Z = self.z[z]
        pa, pi = spectra(self.bg, self.A, float(z), Z["kh"], rj)
        return (Z["kv"] / KP) ** al * (pa + SIGN * mu * pi)

    @staticmethod
    def gls(m, d, Ci):
        """Best b^2 >= 0 and chi^2 for model b^2 m."""
        a = m @ Ci @ d; bb = m @ Ci @ m
        b2 = max(a / bb, 0.0)
        r = d - b2 * m
        return b2, float(r @ Ci @ r)

    def prof_z(self, z, mu, d=None):
        Z = self.z[z]
        d = Z["d"] if d is None else d
        Ci = Z["Ci"]
        # grid: shapes (nRJ, nAL, nk)
        M = Z["T"][None, :, :] * (Z["pa"] + SIGN * mu * Z["pi"])[:, None, :]
        a = np.einsum("ijk,kl,l->ij", M, Ci, d)
        bb = np.einsum("ijk,kl,ijl->ij", M, Ci, M)
        b2 = np.clip(a / bb, 0, None)
        chi = float(d @ Ci @ d) - 2 * b2 * a + b2 ** 2 * bb
        i, j = np.unravel_index(np.argmin(chi), chi.shape)
        rj0, al0 = Z["rjs"][i], Z["als"][j]
        best = (float(chi[i, j]), rj0, al0, float(b2[i, j]))
        free = []
        if self.rjfix is None: free.append("rj")
        if self.tilt: free.append("al")
        if free:
            def fun(x):
                p = dict(zip(free, x)); rj = p.get("rj", rj0); al = p.get("al", al0)
                return self.gls(self.model_shape(z, mu, rj, al), d, Ci)[1]
            x0 = [rj0 if n == "rj" else al0 for n in free]
            bnds = [(0.02, 0.30) if n == "rj" else (-1.0, 1.0) for n in free]
            r = minimize(fun, x0, method="L-BFGS-B", bounds=bnds, options={"ftol": 1e-12, "gtol": 1e-10, "maxiter": 500})
            if r.fun < best[0]:
                p = dict(zip(free, r.x)); rj = p.get("rj", rj0); al = p.get("al", al0)
                b2v, c = self.gls(self.model_shape(z, mu, rj, al), d, Ci)
                best = (c, float(rj), float(al), b2v)
        return best

    def prof(self, mu, data=None):
        out = {z: self.prof_z(z, mu, None if data is None else data[z]) for z in ZS}
        return sum(v[0] for v in out.values()), out

    def nbins(self):
        return sum(int(Z["msk"].sum()) for Z in self.z.values())

    def npar(self):
        return 3 * (1 + (self.rjfix is None) + self.tilt)

    def predict(self, z, mu, rj, al, b2):
        return b2 * self.model_shape(z, mu, rj, al)


def mu_scan(S, data=None):
    MUG = np.concatenate([np.linspace(0, 3, 61), np.geomspace(3.2, 300, 30)])
    ch = np.array([S.prof(m, data)[0] for m in MUG])
    i = int(np.argmin(ch))
    lo, hi = MUG[max(i - 1, 0)], MUG[min(i + 1, len(MUG) - 1)]
    if i == 0:
        r = minimize_scalar(lambda m: S.prof(m, data)[0], bounds=(0.0, MUG[1]), method="bounded", options={"xatol": 1e-5})
        muh, cmin = (r.x, r.fun) if r.fun < ch[0] else (0.0, float(ch[0]))
    else:
        r = minimize_scalar(lambda m: S.prof(m, data)[0], bounds=(lo, hi), method="bounded", options={"xatol": 1e-5})
        muh, cmin = (r.x, r.fun) if r.fun < ch[i] else (MUG[i], float(ch[i]))
    c0 = S.prof(0.0, data)[0]; c1 = S.prof(1.0, data)[0]
    g = lambda m: S.prof(m, data)[0] - cmin - 3.84
    mu95 = None
    up = [m for m, c in zip(MUG, ch) if m > muh and c - cmin > 3.84]
    if up:
        mu95 = brentq(g, muh, up[0], xtol=1e-5)
    return {"mu_hat": float(muh), "chi2_min": float(cmin), "chi2_mu0": float(c0), "chi2_mu1": float(c1),
            "dchi2_1": float(c1 - cmin), "dchi2_0": float(c0 - cmin), "mu95": None if mu95 is None else float(mu95)}


def analyse(S, label, verbose=True):
    c0, b0 = S.prof(0.0)
    nb, npar = S.nbins(), S.npar()
    dof = nb - npar
    pj = float(CHI2.sf(c0, dof))
    perz = {}
    for z in ZS:
        nbz = int(S.z[z]["msk"].sum()); dz = nbz - npar // 3
        perz[z] = {"chi2": b0[z][0], "dof": dz, "p": float(CHI2.sf(b0[z][0], dz)), "R_J": b0[z][1], "alpha": b0[z][2], "b2": b0[z][3]}
    G0 = pj >= 0.01 and all(v["p"] >= 0.001 for v in perz.values())
    asimov = {z: S.predict(z, 0.0, b0[z][1], b0[z][2], b0[z][3]) for z in ZS}
    cA1 = S.prof(1.0, asimov)[0]; cA0 = S.prof(0.0, asimov)[0]
    dA = cA1 - cA0
    G1 = dA >= 9
    sc = mu_scan(S)
    if not G0:
        cls = "NOT DIAGNOSTIC (LINEAR NATIVE MODEL INADEQUATE)"
    elif not G1:
        cls = "NOT DIAGNOSTIC (NUISANCE ABSORBS THE M6 SHAPE)"
    elif sc["dchi2_1"] >= 9:
        cls = "M6 AT X57's BOUND EXCLUDED"
    elif sc["dchi2_0"] >= 9:
        cls = "M6-SHAPED EXCESS PRESENT"
    else:
        cls = "NOT EXCLUDED"
    r = {"class": cls, "G0": {"pass": G0, "chi2": c0, "dof": dof, "p": pj, "per_z": perz},
         "G1": {"pass": G1, "dchi2_asimov": dA}, "scan": sc,
         "Fb_max_z3": S.bg.m6[S.foot]["Fb_max_z3"],
         "Fb_95": None if sc["mu95"] is None else sc["mu95"] * S.bg.m6[S.foot]["Fb_max_z3"]}
    if verbose:
        P(f"  [{label}] {cls}")
        P(f"     G0 null chi2 {c0:.2f} / {dof} dof, p {pj:.3g}; per z: " + ", ".join(
            f"z{z} {v['chi2']:.2f}/{v['dof']} p {v['p']:.3g} (R_J {v['R_J']:.3f}, alpha {v['alpha']:+.3f})" for z, v in perz.items()))
        P(f"     G1 Asimov dchi2(mu=1 vs 0) {dA:.2f} (>= 9)")
        P(f"     scan: mu_hat {sc['mu_hat']:.4f}, dchi2(mu=1) {sc['dchi2_1']:.2f}, dchi2(mu=0) {sc['dchi2_0']:.2f}, mu95 "
          f"{'none in range' if sc['mu95'] is None else f'{sc[chr(109)+chr(117)+chr(57)+chr(53)]:.4f}'}"
          + ("" if r["Fb_95"] is None else f" -> F_b <= {r['Fb_95']:.5f} (bound {r['Fb_max_z3']:.5f})"))
    return r, b0


# ============================================================== K2
S_chk = Setup("chk", NAT, "canonical")
k2 = max(float(np.max(np.abs(S_chk.model_shape(z, 0.0, 0.1, 0.2) - (S_chk.z[z]["kv"] / KP) ** 0.2 *
                                   spectra(NAT, 0.0, float(z), S_chk.z[z]["kh"], 0.1)[0]))) for z in ZS)
check("K2", k2 == 0.0, f"mu = 0 model vs null (A = 0): max abs diff {k2:.1e}", "== 0")

# ============================================================== primary + variants, per footing
VARS = [("V-ns 0.92", dict(bg=BG("native ns 0.92", NAT_OM, NAT_wb / NAT_h ** 2, NAT_h, 0.92, 0.827959))),
        ("V-ns 1.00", dict(bg=BG("native ns 1.00", NAT_OM, NAT_wb / NAT_h ** 2, NAT_h, 1.00, 0.827959))),
        ("V-tilt0", dict(tilt=False)), ("V-kcut", dict(kmax=0.1)), ("V-diag", dict(diag=True)),
        ("V-RJfix", dict(rjfix=0.1))]
RES["footings"] = {}
for f in FOOTS:
    P(f"\n== {f.upper()} footing (a0 {'9.3603e-11' if f == 'canonical' else '1.1312e-10'} m/s^2)")
    Sp = Setup("primary", NAT, f)
    prim, b0 = analyse(Sp, "PRIMARY native")
    fr = {"primary": prim, "variants": {}}
    if f == "canonical":
        # K3 / K4: planted mu = 1 and planted null from the mu = 0 best fit + published-covariance noise (seed 0)
        rng = np.random.default_rng(0)
        noise = {z: rng.multivariate_normal(np.zeros(16), COV[z]) for z in ZS}
        pl1 = {z: Sp.predict(z, 1.0, b0[z][1], b0[z][2], b0[z][3]) + noise[z] for z in ZS}
        pl0 = {z: Sp.predict(z, 0.0, b0[z][1], b0[z][2], b0[z][3]) + noise[z] for z in ZS}
        s1 = mu_scan(Sp, pl1); s0p = mu_scan(Sp, pl0)
        g1 = prim["G1"]["pass"]
        k3ok = (0.5 <= s1["mu_hat"] <= 1.5 and s1["dchi2_0"] >= 9) if g1 else True
        k4ok = (s0p["mu95"] is not None and s0p["mu95"] < 1) if g1 else True
        check("K3", k3ok, f"planted mu=1: mu_hat {s1['mu_hat']:.4f}, dchi2(mu=0) {s1['dchi2_0']:.2f} (G1 {'pass' if g1 else 'fail: vacuous'})",
              "mu_hat in [0.5, 1.5] and dchi2_0 >= 9 when G1 passes")
        check("K4", k4ok, f"planted null: mu_hat {s0p['mu_hat']:.4f}, mu95 {s0p['mu95']}", "mu95 < 1 when G1 passes")
        RES["K3_K4"] = {"planted_mu1": s1, "planted_null": s0p}
    for vname, kw in VARS:
        bgv = kw.pop("bg", NAT)
        Sv = Setup(vname, bgv, f, **kw)
        kw["bg"] = bgv if bgv is not NAT else None
        if kw["bg"] is None: kw.pop("bg")
        fr["variants"][vname] = analyse(Sv, vname)[0]
    fr["inherited_reported"] = analyse(Setup("inherited", INH, f), "V-inherited (reported only)")[0]
    classes = {v["class"] for v in fr["variants"].values()} | {prim["class"]}
    fr["robust"] = len(classes) == 1
    fr["flips"] = [k for k, v in fr["variants"].items() if v["class"] != prim["class"]]
    fr["inherited_flips"] = fr["inherited_reported"]["class"] != prim["class"]
    fr["verdict"] = prim["class"] + (" (ROBUST)" if fr["robust"] else f" (FRAGILE: flips in {', '.join(fr['flips'])})")
    P(f"  ==> {f}: {fr['verdict']}" + ("; inherited background flips (disclosed)" if fr["inherited_flips"] else ""))
    RES["footings"][f] = fr

RES["footings_agree"] = RES["footings"]["canonical"]["verdict"] == RES["footings"]["alt"]["verdict"]
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
check("K6", peak < 1.0, f"peak RSS {peak:.3f} GB, 1 thread, {time.time() - T0:.1f} s", "< 1 GB")
P("\n== VERDICT")
for f in FOOTS:
    P(f"  {f}: {RES['footings'][f]['verdict']}")
P(f"  footings agree: {RES['footings_agree']}")
P(f"  checks: {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])} pass")
dump()
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
