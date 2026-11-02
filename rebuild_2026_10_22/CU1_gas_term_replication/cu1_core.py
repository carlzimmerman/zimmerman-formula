"""CU1: own implementation of the law, the gas term, and the 15-key statistic.
Written from the written definitions (CRG1 SPEC 4.1-4.3); no repo code imported."""
import os, csv, json, hashlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import chi2 as chi2dist
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
INP = os.path.join(HERE, "..", "CRG1_clean_room_regrade", "inputs")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
G = 6.674e-11; MS = 1.989e30; MPC = 3.0857e22; PC = 3.0857e16; KG_PC2 = MS / PC**2
GT = 6.67430e-11; MPCT = 3.0856775814913673e22
GE = 6.67430e-11; MSE = 1.98847e30
OMN, HN, WB = 0.2976016, 0.6856427, 0.0223081
SCAL = json.load(open(os.path.join(INP, "scalars.json")))
S_TAIL = SCAL["gs1_s_meas"]
HS = {"h0672": (0.672, 1, 0), "h0686": (0.686, 2, 1)}
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}

RG = np.logspace(-3, np.log10(30), 3000); RM = RG * MPC
RF = np.logspace(np.log10(2e-3), np.log10(3.5), 90)
EDGES = np.logspace(np.log10(0.15), np.log10(3), 9); RC = np.sqrt(EDGES[:-1] * EDGES[1:])
UU = np.linspace(0, 1, 2001)
PHI = np.linspace(0, np.pi, 181)

NU_MUTATE = False
def nu(y):
    if NU_MUTATE:
        return np.ones_like(y)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)

# ---- precomputed line-of-sight table
_u = UU[None, :] * np.arccosh(RG[-1] / RF)[:, None]
_rr = RF[:, None] * np.cosh(_u)
_lnrr = np.log(_rr); _lnRG = np.log(RG)
_ii = np.clip(np.searchsorted(_lnRG, _lnrr) - 1, 0, RG.size - 2)
_w = np.clip((_lnrr - _lnRG[_ii]) / (_lnRG[_ii + 1] - _lnRG[_ii]), 0, 1)
_rrdu_m = _rr * MPC

def project(Msrc, off_mpc):
    """Returns P(RC) [Msun/pc2], Sigma_b(RC) [as the record's units], n_nonpositive rho cells."""
    rho = np.gradient(Msrc, RM) / (4 * np.pi * RM**2)
    bad = rho <= 0
    lnr = np.log(np.where(bad, 1e-300, rho))
    f = np.exp(lnr[_ii] * (1 - _w) + lnr[_ii + 1] * _w) * _rrdu_m
    du = _u[:, 1] - _u[:, 0]
    Sig = 2 * du * (0.5 * f[:, 0] + f[:, 1:-1].sum(1) + 0.5 * f[:, -1])
    if off_mpc > 1e-4:
        lnR = np.log(RF); lnS = np.log(np.maximum(Sig, 1e-300))
        Rp = np.sqrt(RF[:, None]**2 + off_mpc**2 + 2 * RF[:, None] * off_mpc * np.cos(PHI)[None, :])
        vals = np.exp(np.interp(np.log(Rp), lnR, lnS))
        Sig = 0.5 * (vals[:, 0] + vals[:, -1]) + vals[:, 1:-1].sum(1)
        Sig = Sig * (PHI[1] - PHI[0]) / np.pi
    x = Sig * RF
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (x[1:] + x[:-1]) * np.diff(RF))]) + 0.5 * Sig[0] * RF[0]**2
    dS = 2 * cum / RF**2 - Sig
    P = np.exp(np.interp(np.log(RC), np.log(RF), np.log(np.maximum(dS, 1e-30)))) / KG_PC2
    Sb = np.exp(np.interp(np.log(RC), np.log(RF), np.log(np.maximum(Sig, 1e-300))))
    return P, Sb, int(bad.sum())

def li(r, m, t):
    good = (r > 0) & (m > 0)
    return float(np.interp(np.log(t), np.log(r[good]), np.log(m[good]), left=np.nan, right=np.nan)) 

# ---- X-COP
XDIR = os.path.join(INP, "xcop")
def xcop_rows():
    rows = []
    for nm in sorted(os.listdir(XDIR)):
        if not os.path.isdir(os.path.join(XDIR, nm)):
            continue
        hy = fits.open(os.path.join(XDIR, nm, nm + "_hydro_mass.fits"))
        fg = fits.open(os.path.join(XDIR, nm, nm + "_fgas_profile.fits"))
        ms = fits.open(os.path.join(XDIR, nm, nm + "_mstar.fits"))
        R500 = float(hy[1].header["R500"])
        Rg = float(fg[1].header["R500"])
        rh = np.asarray(hy[1].data["RADIUS"], float); mh = np.asarray(hy[1].data["M_FORW"], float)
        rg = np.asarray(fg[1].data["RADIUS"], float) * Rg; mg = np.asarray(fg[1].data["MGAS"], float)
        rs = np.asarray(ms[2].data["RADIUS"], float); mst = np.asarray(ms[2].data["MSTAR"], float)
        for x in (0.1, 0.2, 0.3, 0.5, 0.7):
            r = x * R500
            a, b, c = li(rh, mh, r), li(rg, mg, r), li(rs, mst, r)
            if np.isfinite(a) and np.isfinite(b) and np.isfinite(c):
                rows.append((nm, x, r * 1e3 * PC, np.exp(a), np.exp(b), np.exp(c)))
    return rows

class XC:
    def __init__(self):
        rs = xcop_rows()
        self.names = sorted({r[0] for r in rs})
        self.cl = np.array([self.names.index(r[0]) for r in rs])
        self.x = np.array([r[1] for r in rs])
        self.r = np.array([r[2] for r in rs])
        self.mh = np.array([r[3] for r in rs])
        self.mg = np.array([r[4] for r in rs])
        self.mst = np.array([r[5] for r in rs])
    def law(self, foot):
        mb = self.mg + self.mst
        return mb * nu(GE * mb * MSE / self.r**2 / A0[foot])
    def term(self, foot):
        return GE * self.mg * MSE / self.r**2 / A0[foot]
    def d(self, foot, k):
        return np.log10(self.mh / (self.law(foot) * (1 + k * self.term(foot))))
    def fit(self, foot, wt):
        """wt = weight per cluster index (len 7). Minimises the weighted sum d^2."""
        w = np.asarray(wt, float)[self.cl]
        f = lambda k: float((w * self.d(foot, k)**2).sum())
        res = minimize_scalar(f, bounds=(0, 100), method="bounded", options={"xatol": 1e-7})
        return float(res.x)
    def fit_mean0(self, foot, wt):
        w = np.asarray(wt, float)[self.cl]
        return float(brentq(lambda k: (w * self.d(foot, k)).sum(), 0, 1000, xtol=1e-9))
    def fit_linear(self, foot, wt):
        w = np.asarray(wt, float)[self.cl]
        y = self.mh / self.law(foot) - 1; t = self.term(foot)
        return float((w * y * t).sum() / (w * t * t).sum())
    def stat(self, foot, k, sel=None):
        dd = self.d(foot, k)
        if sel is not None:
            dd = dd[np.isin(self.cl, sel)]
        return float(dd.mean()), float(np.sqrt((dd**2).mean()))

# ---- shear
class Shear:
    def __init__(self, gdex=0.005, fs=0.034):
        self.g = 10**gdex; self.fs = fs
        c = np.load(os.path.join(INP, "clusters", "x2_catalogue_columns.npz"), allow_pickle=True)
        m = np.load(os.path.join(INP, "clusters", "x7_measure_percluster.npz"), allow_pickle=True)
        self.m = m
        assert (c["name"] == m["name"]).all()
        self.name = c["name"]; self.ra = c["ra"]; self.z = c["z"]; self.Mg = c["Mgas500"]; self.R5 = c["R500"]; self.off = c["off_deg"]
        self.N = self.name.size
        kt = {r["name"]: r["KT_keV"] for r in csv.DictReader(open(os.path.join(INP, "clusters", "erass1_kt.csv")))}
        KT = np.array([float(kt.get(str(n), "nan") or "nan") for n in self.name])
        self.I = np.where(np.isfinite(KT) & (KT > 0))[0]
        xkt = np.log10(KT[self.I] / np.median(KT[self.I]))
        self.xkt = xkt
        self.T = np.digitize(xkt, np.quantile(xkt, [1 / 3, 2 / 3]))
        self.X1 = np.column_stack([np.ones(xkt.size), xkt])
        Mm = m["Mgas500"]
        self.Mt = np.digitize(Mm, np.quantile(Mm, [1 / 3, 2 / 3]))
        order = np.argsort(self.ra); self.PATCH = np.zeros(self.N, int); self.PATCH[order] = np.arange(self.N) * 30 // self.N
        self.cal = json.load(open(os.path.join(INP, "clusters", "x7_outer_mgas_cal.json")))
        self._dm = self._dm_table()
        self.chain = {}
        for hk in HS:
            self.chain[hk] = [self._chain(i, hk) for i in range(self.N)]
        self.vc = {}
        self.meas = {}
    def _dm_table(self):
        DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295)
        DMb = np.sqrt(7.942**3 / (0.295 * DHb))
        return PchipInterpolator([0, 0.295, 0.510, 0.706, 0.934, 1.321, 1.484, 2.330], [0, DMb, 13.588, 17.351, 21.576, 27.601, 30.512, 38.988])
    def _DAcat(self, z):
        zz = np.linspace(0, z, 600)
        f = 1 / np.sqrt(0.3 * (1 + zz)**3 + 0.7)
        return float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(zz))) * 2.998e8 / (1e3 * 70) / (1 + z)
    def _chain(self, i, hk):
        h = HS[hk][0]; z = float(self.z[i])
        DM = float(self._dm(min(z, 2.33))) * 101.54 / h
        q = (DM / (1 + z)) / self._DAcat(z)
        Mg5 = float(self.Mg[i]) * q**2.5 * self.g; R5 = float(self.R5[i]) * q
        rc = 0.15 * R5
        sh = (1 + (RG / rc)**2)**-1.0
        s5 = (1 + (R5 / rc)**2)**-1.0
        out = RG > R5
        sh = np.where(out, s5 * (RG / R5)**(-S_TAIL), sh)
        y = 4 * np.pi * RM**2 * sh
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(RM))])
        Mbx = (1 + self.fs) * cum * Mg5 * MS / np.interp(R5, RG, cum)
        # seed, 3 Mpc-cut profile
        shP = (1 + (RG / rc)**2)**-1.0
        w = RG > 2.2 * R5
        shP = np.where(w, (1 + (2.2 * R5 / rc)**2)**-1.0 * (RG / (2.2 * R5))**-3.0, shP)
        shP = np.where(RG > 3.0, 0.0, shP)
        yP = 4 * np.pi * RM**2 * shP
        cP = np.concatenate([[0.0], np.cumsum(0.5 * (yP[1:] + yP[:-1]) * np.diff(RM))])
        Mbt = (1 + self.fs) * cP[-1] * Mg5 * MS / np.interp(R5, RG, cP)
        H0 = HN * 1e5 / MPCT; rhoc = 3 * H0**2 / (8 * np.pi * GT)
        Ob = WB / HN**2
        rhom = OMN * rhoc
        rta = None
        for _ in range(199):
            rta = (3 * (OMN / Ob) * Mbt / (4 * np.pi * 5.55 * rhom))**(1 / 3) / (1 + z)
            new = float(np.interp(rta, RM, Mbx))
            done = abs(new / Mbt - 1) < 1e-6
            Mbt = new
            if done:
                break
        Mb = np.where(RM <= rta, Mbx, Mbt)
        return dict(Mb=Mb, Mbx=Mbx, off=np.radians(float(self.off[i])) * DM / (1 + z), rta=rta)
    def vector(self, i, hk, Msrc):
        hi = HS[hk][1]; m = self.m
        E = m["E"][i, hi]
        W = np.where(E < 1e8, 1 / np.where(E > 0, E, np.inf)**2, 0.0)
        P, Sb, nb = project(Msrc, self.chain[hk][i]["off"])
        den = m["den"][i, hi]
        fr = np.ones(8)
        g = den > 0
        mm = m["m3to8"][i, hi]
        tot = sum(Sb**(p + 1) * mm[p] for p in range(6))
        fr[g] = 1 + tot[g] / den[g]
        return W * P * fr, nb
    def msrc(self, foot, i, hk, k, uncapped=False):
        c = self.chain[hk][i]; Mb = c["Mb"]
        y = G * Mb / RM**2 / A0[foot]
        pos = Mb > 0
        out = Mb.copy()
        out[pos] = Mb[pos] * nu(y[pos])
        if k != 0:
            Mgas = (c["Mbx"] if uncapped else Mb) / (1 + self.fs)
            out = out * (1 + k * G * Mgas / RM**2 / A0[foot])
        return out
    def _vcstar(self, foot, hk):
        key = (foot, hk)
        if key in self.vc:
            return self.vc[key]
        t = np.load(os.path.join(INP, "clusters", "efe_table_%s.npz" % foot))
        ts, tM = t["s"], t["M"]
        Ct = tM / (0.5 + np.sqrt(0.25 + ts**2))
        a0 = A0[foot]
        V = np.zeros((self.N, 8))
        for i in range(self.N):
            Mb = self.chain[hk][i]["Mb"]
            gN = G * Mb / RM**2
            with np.errstate(divide="ignore", invalid="ignore"):
                base = 0.5 * gN + np.sqrt(0.25 * gN**2 + gN * a0)
            M3 = float(np.interp(3.0, RG, Mb))
            s = RG / (np.sqrt(G * M3 / a0) / MPC)
            C = np.interp(np.log(s), np.log(ts), Ct)
            C = np.where(s < ts[0], 1.0, C)
            hi = s > ts[-1]
            C = np.where(hi, tM[-1] / (0.5 + np.sqrt(0.25 + s**2)), C)
            V[i], _ = self.vector(i, hk, base * C * RM**2 / G)
        self.vc[key] = V
        return V
    def _measure(self, foot, hk):
        key = (foot, hk)
        if key in self.meas:
            return self.meas[key]
        m = self.m; h, hi, li_ = HS[hk]
        E = m["E"][:, hi]
        W = np.where(E < 1e8, 1 / np.where(E > 0, E, np.inf)**2, 0.0)
        Bst = m["den"][:, hi].sum(0) / m["den_r"][:, hi].sum(0)
        D = m["D"][:, hi]; leak = m["leakP"][:, li_, 0]
        out = {"n": W * Bst * (D - leak), "raw": W * Bst * D, "x": W * Bst * m["Dx"][:, hi], "rr": W * Bst * m["DRR"][:, hi]}
        vc = self._vcstar(foot, hk)
        res = {}
        for b, ix in BANDS.items():
            res[b] = {nm: out[nm][:, ix].sum(1) for nm in out}
            res[b]["d"] = vc[:, ix].sum(1)
        self.meas[key] = res
        return res
    # key plumbing
    def _sets(self):
        I = self.I; a = np.arange(self.N)
        d = {"I": I, "all": a}
        for t in range(3):
            d["T%d" % t] = I[self.T == t]
            d["M%d" % t] = a[self.Mt == t]
        return d
    KEYS = ["G-IN-all", "G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-T3",
            "G-OUT-b", "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-IN-Mall"]
    def _key_def(self, key):
        tail = key.split("-")
        band = {"IN": "INNER", "MID": "MID", "OUT": "OUTER"}[tail[1]]
        t = tail[2]
        if t == "all":
            return band, "I", 0
        if t == "Mall":
            return band, "all", 0
        if t == "b":
            return band, "b", 5010
        if t[0] == "T":
            return band, "T%d" % (int(t[1]) - 1), 20100 + int(t[1]) - 1
        return band, "M%d" % (int(t[1]) - 1), 200 + int(t[1]) - 1
    def _wls(self, n, d, Wt=None):
        X = self.X1
        w = np.ones(n.size) if Wt is None else Wt
        Am = (X.T * (w * d)) @ X
        return np.linalg.solve(Am, X.T @ (w * n))
    def _sig_ratio(self, raw, d, seed, ids):
        nsel = ids.size
        idx = np.random.default_rng([20261024, seed]).integers(0, nsel, size=(2000, nsel))
        off = np.arange(2000)[:, None]
        cnt = np.zeros((2000, nsel)); np.add.at(cnt, (off, idx), 1)
        v = (cnt @ raw[ids]) / (cnt @ d[ids])
        sb = v.std(ddof=1)
        pv = self.PATCH[ids]; jk = []
        for q in range(30):
            if (pv == q).any():
                w = pv != q
                jk.append((raw[ids][w]).sum() / (d[ids][w]).sum())
        jk = np.array(jk); nj = jk.size
        return max(sb, np.sqrt((nj - 1) / nj * ((jk - jk.mean())**2).sum()))
    def _sig_slope(self, n, d):
        ids = self.I; nsel = ids.size
        idx = np.random.default_rng([20261024, 5010]).integers(0, nsel, size=(2000, nsel))
        vals = np.empty(2000)
        for r in range(2000):
            Wt = np.bincount(idx[r], minlength=nsel).astype(float)
            vals[r] = self._wls(n[ids], d[ids], Wt)[1]
        pv = self.PATCH[ids]; jk = []
        for q in range(30):
            if (pv == q).any():
                jk.append(self._wls(n[ids], d[ids], (pv != q).astype(float))[1])
        jk = np.array(jk); nj = jk.size
        return max(vals.std(ddof=1), np.sqrt((nj - 1) / nj * ((jk - jk.mean())**2).sum()))
    def meas_keys(self, foot, hk):
        """A and sigma per key; independent of k."""
        ck = (foot, hk, "mk")
        if ck in self.meas:
            return self.meas[ck]
        B = self._measure(foot, hk); sets = self._sets(); out = {}
        cal = self.cal["%s|%s" % (foot, hk)]
        for key in self.KEYS:
            band, st, seed = self._key_def(key)
            b = B[band]
            if st == "b":
                A = self._wls(b["n"][self.I], b["d"][self.I])[1]
                s = self._sig_slope(b["n"], b["d"])
            else:
                ids = sets[st]
                A = b["n"][ids].sum() / b["d"][ids].sum()
                if key in ("G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3"):
                    c = cal[key.split("-")[2]]
                    s = c["s_CAL"] * A / c["A_CAL"]
                else:
                    s = self._sig_ratio(b["raw"], b["d"], seed, ids)
                    if band == "INNER":
                        s = np.sqrt(s**2 + (b["x"][ids].sum() / b["d"][ids].sum())**2 + (b["rr"][ids].sum() / b["d"][ids].sum())**2)
            out[key] = (float(A), float(s))
        self.meas[ck] = out
        return out
    def corr(self, foot, hk, seed=20261102, ndraw=2000):
        ck = (foot, hk, "R")
        if ck in self.meas:
            return self.meas[ck]
        B = self._measure(foot, hk); sets = self._sets()
        idx = np.random.default_rng(seed).integers(0, self.N, size=(ndraw, self.N))
        rep = np.zeros((ndraw, 15))
        cn = np.zeros((ndraw, self.N)); np.add.at(cn, (np.arange(ndraw)[:, None], idx), 1)
        for j, key in enumerate(self.KEYS):
            band, st, _ = self._key_def(key)
            b = B[band]
            if st == "b":
                for r in range(ndraw):
                    rep[r, j] = self._wls(b["n"][self.I], b["d"][self.I], cn[r, self.I])[1]
            else:
                ids = sets[st]
                rep[:, j] = (cn[:, ids] @ b["raw"][ids]) / (cn[:, ids] @ b["d"][ids])
        R = np.corrcoef(rep.T)
        self.meas[ck] = R
        return R
    def predict(self, foot, hk, k, uncapped=False):
        V = np.zeros((self.N, 8)); nb = 0; ncl = 0
        for i in range(self.N):
            V[i], b = self.vector(i, hk, self.msrc(foot, i, hk, k, uncapped))
            nb += b; ncl += b > 0
        return V, nb, ncl
    def grade(self, foot, hk, k, uncapped=False):
        V, nb, ncl = self.predict(foot, hk, k, uncapped)
        return self.grade_V(foot, hk, V), nb, ncl
    def grade_V(self, foot, hk, V):
        mk = self.meas_keys(foot, hk); vc = self._vcstar(foot, hk); sets = self._sets(); res = {}
        for key in self.KEYS:
            band, st, _ = self._key_def(key)
            ix = BANDS[band]; v = V[:, ix].sum(1); c = vc[:, ix].sum(1)
            if st == "b":
                pred = self._wls(v[self.I], c[self.I])[1]
            else:
                ids = sets[st]; pred = v[ids].sum() / c[ids].sum()
            A, s = mk[key]
            res[key] = dict(A=A, s=s, pred=float(pred), Z=float((A - pred) / s))
        return res
    def joint(self, foot, hk, res, identity=False):
        R = np.eye(15) if identity else self.corr(foot, hk)
        z = np.array([res[k]["Z"] for k in self.KEYS])
        lam, U = np.linalg.eigh(R)
        keep = lam >= (1e-3 * lam.max())
        pz = U[:, keep].T @ z
        chi = float((pz**2 / lam[keep]).sum()); dof = int(keep.sum())
        return chi, dof, float(chi2dist.sf(chi, dof))

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()
