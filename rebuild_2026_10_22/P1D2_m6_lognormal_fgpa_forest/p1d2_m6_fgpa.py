#!/usr/bin/env python3
"""P1D2_m6_lognormal_fgpa_forest: X57's M6 (displacement) against Boera et al. 2019 z 4.2/4.6/5.0 P1D with a
framework-native nonlinear forward model: lognormal gas from the native linear power (fixed-amplitude modes) + FGPA +
thermal broadening; M6 patches inserted in real space as Poisson chords (stratified, A1). Per-z nuisance F, gamma, b, R_J.
FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md committed alone first (d89e0f9469); AMENDMENTS.md A1 (219abb9fb3).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I p1d2_m6_fgpa.py      (P1D2_MUTATE=1 twin)
Preemptible: per-configuration checkpoint; SIGTERM exits cleanly, rerun resumes.
"""
import os, sys, json, math, time, resource, re, hashlib, signal, tarfile
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize, minimize_scalar, brentq
from scipy.stats import chi2 as CHI2

MUT = os.environ.get("P1D2_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(REB, ".."))
DATA = os.path.join(REPO, "_external_data", "boera2019_p1d", "raw")
CKPT = os.path.join(HERE, f"p1d2_checkpoint{TAG}.json")
T0 = time.time()
OUT = open(os.path.join(HERE, f"p1d2_m6_fgpa{TAG}.out"), "a")
trapz = getattr(np, "trapezoid", None) or np.trapz
STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.update(flag=True))


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


RES = json.load(open(CKPT)) if os.path.exists(CKPT) else {
    "lane": "P1D2_m6_lognormal_fgpa_forest", "criteria": "d89e0f9469", "amendments": ["A1 219abb9fb3"], "mutate": MUT,
    "checks": {}, "configs": {}, "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating "
                                             "field component, never a particle; not theory closed"}


def save():
    RES["elapsed_s_last"] = time.time() - T0
    RES["peak_rss_GB"] = max(RES.get("peak_rss_GB", 0.0), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9)
    tmp = CKPT + ".tmp"
    json.dump(RES, open(tmp, "w"), indent=1, default=float); os.replace(tmp, CKPT)


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


def J(rel):
    return json.load(open(os.path.join(REPO, rel)))


FOOTS = ("canonical", "alt")
ZS = ("4.2", "4.6", "5.0")
P("\n" + "=" * 100 + "\nP1D2_m6_lognormal_fgpa_forest" + (" [MUTATE m1-m3: control output, not physics]" if MUT else "") +
  ": criteria d89e0f9469 + A1 219abb9fb3; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed"
  + (f"  [resumed: {len(RES['configs'])} configurations in checkpoint]" if RES["configs"] else ""))

# ============================================================== STEP 0
P("\n== STEP 0 (stop rule)")
SHA = {"src_1809.06980v2.tar.gz": "9583568fe3076be9687567f54e81716a8dd452b4061da1e9476e1d299931f1a8",
       "Cov_Matrixz=4.2.dat": "872daaf273d3f212968b750b5b263c4b03c3cd57091b144ae120a480e76bb4dc",
       "Cov_Matrixz=4.6.dat": "44e75dc183fab9083add6a924dd3b2787869c2579bc1ea152592c1e864d261ed",
       "Cov_Matrixz=5.0.dat": "c44356e7f2f05d47a4a20dd274fc1d5f7812f09f8327636322c89063ff167d05"}
s0 = {"S0a": all(hashlib.sha256(open(os.path.join(DATA, f), "rb").read()).hexdigest() == h for f, h in SHA.items())}
with tarfile.open(os.path.join(DATA, "src_1809.06980v2.tar.gz")) as tf:
    TEX = tf.extractfile("PSpaperApJRef_New.tex").read().decode("utf-8", "replace")
TAB = {}
for z in ZS:
    lab = TEX.index("\\label{table:%sbin}" % z)
    body = TEX[TEX.rindex("\\begin{tabular}", 0, lab):lab]
    rows = [[float(v) for v in m.groups()] for m in (re.match(r"^\s*(-?\d+\.\d+)\s*&\s*([0-9.eE+-]+)\s*&\s*([0-9.eE+-]+)\s*&\s*([0-9.eE+-]+)\s*\\\\", l)
                                                      for l in body.splitlines()) if m]
    TAB[z] = np.array(rows)
s0["S0b"] = all(TAB[z].shape == (16, 4) and np.max(np.abs(TAB[z][:, 0] - np.round(np.arange(-2.2, -0.65, 0.1), 1))) <= 0.01 for z in ZS)
check("K1", s0["S0b"], "; ".join(f"z {z}: {TAB[z].shape[0]} rows" for z in ZS), "16 rows, logk -2.2..-0.7")
COV = {z: np.asfortranarray(np.load(os.path.join(DATA, f"Cov_Matrixz={z}.dat"))) for z in ZS}
COL = 1 if MUT else 2                                                         # m2
LOGK = {z: TAB[z][:, 0] for z in ZS}
KV = {z: 10 ** LOGK[z] for z in ZS}
DAT = {z: TAB[z][:, COL] for z in ZS}

# native background + M6 (P1D1 re-implementation, checked against P1D1's committed JSON)
P1 = J("rebuild_2026_10_22/P1D1_m6_boera_high_z_forest/p1d1_m6_boera_results.json")
X22 = J("rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")
FMAX = {f: X22["step2"]["per_footing"][f]["f_max"] for f in FOOTS}
RL = X22["step2"]["per_footing"]["canonical"]["R_L_Mpc_h"][2]
KG = np.logspace(-4, math.log10(200.0), 60001)
LNK = np.log(KG)
W = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
NAT_OM, NAT_h, NAT_wb = 0.2976016, 0.6856427, 0.0223081


class BG:
    def __init__(self, ns, OM=NAT_OM, h=NAT_h, wb=NAT_wb, s8=0.827959):
        OB = wb / h ** 2
        self.OM, self.OB, self.h, self.ns, self.OL, self.RRAT = OM, OB, h, ns, 1 - OM, (OM - OB) / OB
        Gam = OM * h * np.exp(-OB * (1.0 + np.sqrt(2 * h) / OM))
        Tk = lambda kk: (np.log(1 + 2.34 * kk / Gam) / (2.34 * kk / Gam) * (1 + 3.89 * kk / Gam + (16.1 * kk / Gam) ** 2
                         + (5.46 * kk / Gam) ** 3 + (6.71 * kk / Gam) ** 4) ** -0.25)
        kf = np.logspace(-4, 3, 4000)
        shape = kf ** (3 + ns) * Tk(kf) ** 2
        NORM = s8 ** 2 / trapz(shape * W(kf * 8.0) ** 2, np.log(kf))
        self.s2R0 = NORM * trapz(shape * W(kf * RL) ** 2, np.log(kf))
        self.PAD0_G = 2 * math.pi ** 2 * NORM * KG ** (3 + ns) * Tk(KG) ** 2 / KG ** 3
        self.D0 = self._D(1.0)
        D3 = self.Dz(3.0)
        self.m6 = {}
        for f in FOOTS:
            dci = -(1 - FMAX[f]); dbi = -self.RRAT * dci
            Fb3 = 0.2 * self.s2R0 * D3 ** 2 / (dbi ** 2 / (1 + dbi))
            self.m6[f] = {"delta_b_in": dbi, "f_V": Fb3 / (1 + dbi), "Fb_max_z3": Fb3,
                          "A_lin": Fb3 / (1 + dbi) * dbi ** 2 * 4 * math.pi * RL ** 3 / 3}

    def Ez(self, z):
        return math.sqrt(self.OM * (1 + z) ** 3 + self.OL)

    def _D(self, a):
        Ea = lambda x: math.sqrt(self.OM * x ** -3 + self.OL)
        return 2.5 * self.OM * Ea(a) * quad(lambda x: 1.0 / (x * Ea(x)) ** 3, 0, a, epsabs=0, epsrel=1e-12, limit=400)[0]

    def Dz(self, z):
        return self._D(1 / (1 + z)) / self.D0


def p1d(p3d_on_grid, kpar):
    f = KG ** 2 * p3d_on_grid
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(LNK))])
    return (cum[-1] - np.interp(np.log(kpar), LNK, cum)) / (2 * math.pi)


NAT = BG(0.965)
ok_c, txt = [], []
for f in FOOTS:
    ref = P1["backgrounds"]["native"]["m6"][f]
    for key, mine in (("delta_b_in", NAT.m6[f]["delta_b_in"]), ("f_V", NAT.m6[f]["f_V"]), ("Fb_max_z3", NAT.m6[f]["Fb_max_z3"])):
        tgt = ref[key] * (1.01 if (MUT and f == "canonical" and key == "f_V") else 1.0)       # m3
        ok_c.append(round(mine, 4) == round(tgt, 4)); txt.append(f"{f} {key} {mine:.5f}/{tgt:.5f}")
s0["S0c"] = all(ok_c)
P(f"  S0c P1D1 native M6 reproduced (4 dp): {sum(ok_c)}/{len(ok_c)}: " + "; ".join(txt))

# ============================================================== mock machinery
NSK, LSK, DX = 20, 200.0, 0.02
NPX = int(round(LSK / DX))
LTOT = NSK * LSK
KX = 2 * math.pi * np.fft.rfftfreq(NPX, DX)                                   # comoving h/Mpc


class Mock:
    def __init__(self, bg, z, seeds=(0, 1, 2)):
        self.bg, self.z = bg, float(z)
        self.cz = 100.0 * bg.Ez(self.z) / (1 + self.z)                       # km/s per Mpc/h
        self.D2 = bg.Dz(self.z) ** 2
        rng = np.random.default_rng(seeds[0])
        self.phase = np.exp(2j * math.pi * rng.random((NSK, len(KX))))
        self.phase[:, 0] = 0.0
        if NPX % 2 == 0:
            self.phase[:, -1] = np.sign(self.phase[:, -1].real) + 0.0
        self.seeds = seeds
        kv = KX / self.cz
        self.bins = {}
        for zz in ZS:
            pass
        lk = np.log10(np.where(kv > 0, kv, 1e-30))
        self.binmask = [(np.abs(lk - c) <= 0.05) & (kv > 0) for c in LOGK[z]]
        self.nmodes = [int(m.sum()) for m in self.binmask]
        self._gcache = {}
        self._pcache = {}

    def gfield(self, RJ):
        key = round(RJ, 10)
        if key not in self._gcache:
            Pg = p1d(self.bg.PAD0_G * self.D2 * np.exp(-KG ** 2 * RJ ** 2), np.maximum(KX, 1e-6))
            Pg[0] = 0.0
            amp = np.sqrt(LSK * Pg) / DX
            g = np.fft.irfft(amp[None, :] * self.phase, n=NPX, axis=1)
            if len(self._gcache) > 16:
                self._gcache.clear()
            self._gcache[key] = (g, Pg)
        return self._gcache[key]

    def patches(self, foot, mu, dbi_override=None):
        """Stratified chords (A1): returns indicator array (NSK, NPX)."""
        key = (foot, round(mu, 12))
        if key in self._pcache:
            return self._pcache[key]
        fV = self.bg.m6[foot]["f_V"]
        lam1 = 3 * fV / (4 * RL)
        N1 = int(round(lam1 * LTOT))
        r1 = np.random.default_rng(self.seeds[1])
        pos = r1.random(N1) * LTOT; u = r1.random(N1); tags = (r1.permutation(N1) + 0.5) / N1
        keep = tags <= mu
        pos, hl = pos[keep], RL * np.sqrt(1 - u[keep])
        if mu > 1:
            r2 = np.random.default_rng(self.seeds[2])
            Nx = int(round((mu - 1) * lam1 * LTOT))
            pos = np.concatenate([pos, r2.random(Nx) * LTOT]); hl = np.concatenate([hl, RL * np.sqrt(1 - r2.random(Nx))])
        I = np.zeros(NSK * NPX)
        x = (np.arange(NSK * NPX) + 0.5) * DX
        for p0, h0 in zip(pos, hl):
            i0, i1 = int((p0 - h0) / DX), int((p0 + h0) / DX) + 1
            idx = np.arange(i0, i1 + 1)
            sel = np.abs(x[idx % (NSK * NPX)] - p0 + LTOT * np.round((p0 - x[idx % (NSK * NPX)]) / LTOT)) <= h0
            I[idx[sel] % (NSK * NPX)] = 1.0
        I = I.reshape(NSK, NPX)
        if len(self._pcache) > 8:                                          # memory cap (K6)
            self._pcache.clear()
        self._pcache[key] = I
        return I

    def flux_p1d(self, pars, mu, foot, smooth=True, dbi_override=None, want_pdf=False, want_skewers=False):
        Fbar, gam, b, RJ = pars
        g, _ = self.gfield(RJ)
        eg = np.exp(g)
        Dad = eg / eg.mean()
        if mu > 0:
            I = self.patches(foot, mu)
            if smooth:
                Is = np.fft.irfft(np.fft.rfft(I, axis=1) * np.exp(-0.5 * KX ** 2 * RJ ** 2)[None, :], n=NPX, axis=1)
                Is = np.clip(Is, 0.0, 1.0)
            else:
                Is = I
            dbi = self.bg.m6[foot]["delta_b_in"] if dbi_override is None else dbi_override
            fv_eff = float(I.mean())
            Delta = Dad * (1 + dbi * Is - fv_eff * dbi * (1 - Is) / (1 - fv_eff))
            Delta = np.clip(Delta, 0.0, None)
        else:
            Delta = Dad
        beta = 2 - 0.7 * (gam - 1)
        sx = (b / math.sqrt(2)) / self.cz
        tau0 = np.fft.irfft(np.fft.rfft(Delta ** beta, axis=1) * np.exp(-0.5 * KX ** 2 * sx ** 2)[None, :], n=NPX, axis=1)
        tau0 = np.clip(tau0, 0.0, None)
        # Newton on log A for <exp(-A tau0)> = Fbar
        lA = math.log(max(-math.log(Fbar) / max(tau0.mean(), 1e-30), 1e-30))
        for _ in range(60):
            A = math.exp(lA); e = np.exp(-A * tau0)
            fm = e.mean() - Fbar
            d = -(A * tau0 * e).mean()
            if d == 0: break
            step = fm / d
            lA -= max(min(step, 2.0), -2.0)
            if abs(fm) < 1e-10: break
        F = np.exp(-math.exp(lA) * tau0)
        dF = F / F.mean() - 1
        Pk = np.abs(DX * np.fft.rfft(dF, axis=1)) ** 2 / LSK * self.cz           # km/s, per skewer
        Psk = np.array([[Pk[s, m].mean() for m in self.binmask] for s in range(NSK)])
        out = {"P": Psk.mean(0), "Pvar": Psk.var(0, ddof=1) / NSK}
        if want_pdf:
            out["frac_F_lt_0.05"] = float((F < 0.05).mean())
        if want_skewers:
            out["Delta_mean"] = float(Delta.mean()); out["Dad_mean"] = float(Dad.mean())
        return out


# S0d: Gaussian-field power through the same FFT / units / binning vs input
s0d_dev = 0.0
for z in ZS:
    mk = Mock(NAT, z)
    g, Pg = mk.gfield(0.1)
    Pk = np.abs(DX * np.fft.rfft(g, axis=1)) ** 2 / LSK * mk.cz
    meas = np.array([Pk[:, m].mean() for m in mk.binmask])
    inp = np.array([(Pg * mk.cz)[m].mean() for m in mk.binmask])
    s0d_dev = max(s0d_dev, float(np.max(np.abs(meas / inp - 1))))
    RES.setdefault("nmodes", {})[z] = mk.nmodes
s0["S0d"] = s0d_dev <= 0.05
P(f"  S0d Gaussian field power vs input (fixed-amplitude, units, bins): max |ratio-1| {s0d_dev:.2e} (<= 0.05); "
  f"modes per bin z4.2 {RES['nmodes']['4.2'][:3]}...")
# S0e: covered fraction at mu = 1 vs f_V
s0e_txt, s0e_ok = [], []
for f in FOOTS:
    mk = Mock(NAT, "4.6")
    I = mk.patches(f, 1.0)
    fV = NAT.m6[f]["f_V"]
    N1 = int(round(3 * fV / (4 * RL) * LTOT))
    sig = fV * math.sqrt(2.0 / max(N1, 1))                                 # chord-length variance ~ (mean)^2 -> sqrt(2/N)
    s0e_ok.append(abs(I.mean() - fV) <= 3 * sig); s0e_txt.append(f"{f}: covered {I.mean():.5f} vs f_V {fV:.5f} (N1 {N1}, 3 sigma {3 * sig:.5f})")
s0["S0e"] = all(s0e_ok)
P("  S0e " + "; ".join(s0e_txt))
check("S0", all(s0.values()), f"{s0}", "all Step-0 items")
RES["step0"] = {"items": s0, "S0c": txt, "S0d_maxdev": s0d_dev, "S0e": s0e_txt}
if not all(s0.values()) and not MUT:
    P("STOP: Step 0 failed; nothing graded."); RES["verdict"] = "STOPPED AT STEP 0"; save(); sys.exit(1)

# K5: mean baryon conservation (and m1 twin: negative patch gas clipped)
mk = Mock(NAT, "4.6")
k5 = []
for f in FOOTS:
    dbo = -1.5 if MUT else None                                           # m1
    o = mk.flux_p1d((0.3, 1.4, 12.0, 0.08), 1.0, f, dbi_override=dbo, want_skewers=True)
    I = mk.patches(f, 1.0)
    N1 = int(round(3 * NAT.m6[f]["f_V"] / (4 * RL) * LTOT))
    dbi = dbo if dbo is not None else NAT.m6[f]["delta_b_in"]
    tol = 3 * abs(dbi) * NAT.m6[f]["f_V"] * math.sqrt(2.0 / N1) + 1e-6
    k5.append((abs(o["Delta_mean"] - o["Dad_mean"]) / o["Dad_mean"] <= tol, f"{f}: <Delta> {o['Delta_mean']:.5f} vs <Delta_ad> {o['Dad_mean']:.5f} (tol {tol:.4f})"))
check("K5", all(a for a, _ in k5), "; ".join(t for _, t in k5), "mean baryon conserved within 3 Poisson sigma of the patch term")
o0 = mk.flux_p1d((0.3, 1.4, 12.0, 0.08), 0.0, "canonical")
o00 = mk.flux_p1d((0.3, 1.4, 12.0, 0.08), 1e-15, "canonical")
check("K2", float(np.max(np.abs(o0["P"] / o00["P"] - 1))) <= 1e-9, "mu = 0 vs mu -> 0 (no chords kept): identical P1D", "<= 1e-9")
save()

# ============================================================== fitting
LO = np.array([0.02, 1.0, 4.0, 0.02]); HI = np.array([0.70, 1.8, 30.0, 0.30])
GRID0 = [(F, g, b, r) for F in (0.15, 0.35, 0.55) for g in (1.2, 1.5) for b in (8.0, 16.0) for r in (0.05, 0.12)]


class Config:
    def __init__(self, name, ns=0.965, kmax=None, diag=False, smooth=True, gamfix=None, seeds=(0, 1, 2)):
        self.name, self.smooth, self.gamfix = name, smooth, gamfix
        self.bg = NAT if ns == 0.965 else BG(ns)
        self.mk = {z: Mock(self.bg, z, seeds) for z in ZS}
        self.msk = {z: (np.ones(16, bool) if kmax is None else KV[z] <= kmax * (1 + 1e-9)) for z in ZS}
        self.C0 = {}
        for z in ZS:
            C = COV[z][np.ix_(self.msk[z], self.msk[z])]
            self.C0[z] = np.diag(np.diag(C)) if diag else C
        self.Ci = {z: np.linalg.inv(self.C0[z]) for z in ZS}
        self.npar_z = 3 if gamfix is not None else 4

    def augment(self, mcvar):
        for z in ZS:
            self.Ci[z] = np.linalg.inv(self.C0[z] + np.diag(mcvar[z][self.msk[z]]))

    def full(self, x):
        if self.gamfix is not None:
            return (x[0], self.gamfix, x[1], x[2])
        return tuple(x)

    def chi_z(self, z, x, mu, foot, d):
        m = self.mk[z].flux_p1d(self.full(x), mu, foot, smooth=self.smooth)["P"][self.msk[z]]
        r = d - m
        return float(r @ self.Ci[z] @ r)

    def prof_z(self, z, mu, foot, d=None, x0=None):
        d = DAT[z][self.msk[z]] if d is None else d
        lo, hi = (LO, HI) if self.gamfix is None else (LO[[0, 2, 3]], HI[[0, 2, 3]])
        starts = [np.array(s if self.gamfix is None else (s[0], s[2], s[3])) for s in GRID0]
        if x0 is not None:
            cands = [np.array(x0)]
        else:
            vals = [(self.chi_z(z, s, mu, foot, d), i) for i, s in enumerate(starts)]
            vals.sort()
            cands = [starts[i] for _, i in vals[:2]]
        best = None
        for c in cands:
            r = minimize(lambda x: self.chi_z(z, x, mu, foot, d), c, method="Powell",
                         bounds=list(zip(lo, hi)), options={"xtol": 1e-3, "ftol": 1e-6, "maxfev": 800})
            if best is None or r.fun < best[0]:
                best = (float(r.fun), [float(v) for v in r.x])
        return best

    def prof(self, mu, foot, data=None, warm=None):
        out = {z: self.prof_z(z, mu, foot, None if data is None else data[z], None if warm is None else warm[z][1]) for z in ZS}
        return sum(v[0] for v in out.values()), out

    def predict(self, z, x, mu, foot):
        return self.mk[z].flux_p1d(self.full(x), mu, foot, smooth=self.smooth)["P"][self.msk[z]]

    def nbins(self):
        return sum(int(m.sum()) for m in self.msk.values())


MUG = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]


def mu_scan(cf, foot, data=None, null=None, warm0=None):
    ch = {}
    warm = null if null is not None else warm0
    for m in MUG:
        if m == 0.0 and null is not None and data is None:
            ch[m] = sum(v[0] for v in null.values()); continue
        c, warm_new = cf.prof(m, foot, data, warm)
        ch[m] = c
        warm = warm_new
    ms = sorted(ch); cs = [ch[m] for m in ms]
    i = int(np.argmin(cs))
    lo, hi = ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)]
    f = lambda m: cf.prof(m, foot, data, warm)[0]
    r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 2e-3, "maxiter": 25})
    muh, cmin = (float(r.x), float(r.fun)) if r.fun < cs[i] else (ms[i], cs[i])
    mu95 = None
    up = [m for m in ms if m > muh and ch[m] - cmin > 3.84]
    if up:
        try:
            mu95 = float(brentq(lambda m: f(m) - cmin - 3.84, muh, up[0], xtol=2e-3, maxiter=30))
        except ValueError:
            mu95 = None
    return {"mu_hat": muh, "chi2_min": cmin, "chi2_mu0": ch[0.0], "chi2_mu1": ch[1.0], "dchi2_1": ch[1.0] - cmin,
            "dchi2_0": ch[0.0] - cmin, "mu95": mu95, "grid": {str(k): v for k, v in ch.items()}}


def run_config(cf):
    """Two-pass null fit (A1.2), then per footing: G0, G1, scan."""
    P(f"\n== CONFIG {cf.name}")
    c0a, n0a = cf.prof(0.0, "canonical")
    mcvar = {z: cf.mk[z].flux_p1d(cf.full(n0a[z][1]), 0.0, "canonical", smooth=cf.smooth)["Pvar"] for z in ZS}
    cf.augment(mcvar)
    c0, n0 = cf.prof(0.0, "canonical", warm=n0a)
    dof = cf.nbins() - 3 * cf.npar_z
    pj = float(CHI2.sf(c0, dof))
    perz = {}
    for z in ZS:
        dz = int(cf.msk[z].sum()) - cf.npar_z
        perz[z] = {"chi2": n0[z][0], "dof": dz, "p": float(CHI2.sf(n0[z][0], dz)), "pars": cf.full(n0[z][1])}
    G0 = pj >= 0.01 and all(v["p"] >= 0.001 for v in perz.values())
    P(f"  null pass1 chi2 {c0a:.2f}; pass2 (+MC var) chi2 {c0:.2f} / {dof} dof, p {pj:.3g}; per z: " + ", ".join(
        f"z{z} {v['chi2']:.2f}/{v['dof']} p {v['p']:.3g} (F {v['pars'][0]:.3f} gam {v['pars'][1]:.2f} b {v['pars'][2]:.1f} RJ {v['pars'][3]:.3f})" for z, v in perz.items()))
    res = {"null": {"chi2_pass1": c0a, "chi2": c0, "dof": dof, "p": pj, "per_z": perz, "G0": G0,
                    "mc_rel_err": {z: (np.sqrt(mcvar[z]) / DAT[z]).tolist() for z in ZS}}, "footings": {}}
    for foot in FOOTS:
        if STOP["flag"]:
            break
        asim = {z: cf.predict(z, n0[z][1], 0.0, foot) for z in ZS}
        cA1, _ = cf.prof(1.0, foot, asim, warm=n0)
        cA0, _ = cf.prof(0.0, foot, asim, warm=n0)
        dA = cA1 - cA0
        G1 = dA >= 9
        sc = mu_scan(cf, foot, null=n0)
        if not G0:
            cls = "NOT DIAGNOSTIC (NATIVE FGPA MODEL INADEQUATE)"
        elif not G1:
            cls = "NOT DIAGNOSTIC (NUISANCE ABSORBS M6)"
        elif sc["dchi2_1"] >= 9:
            cls = "M6 AT X57's BOUND EXCLUDED"
        elif sc["dchi2_0"] >= 9:
            cls = "M6-SHAPED EXCESS PRESENT"
        else:
            cls = "NOT EXCLUDED"
        Fb = cf.bg.m6[foot]["Fb_max_z3"]
        fr = {"class": cls, "G1": {"pass": G1, "dchi2_asimov": dA, "chi2_A0": cA0}, "scan": sc, "Fb_max_z3": Fb,
              "Fb_95": None if sc["mu95"] is None else sc["mu95"] * Fb}
        P(f"  [{foot}] {cls}: G1 Asimov dchi2 {dA:.2f}; mu_hat {sc['mu_hat']:.3f}, dchi2(mu=1) {sc['dchi2_1']:.2f}, "
          f"dchi2(mu=0) {sc['dchi2_0']:.2f}, mu95 {sc['mu95']}" + ("" if fr["Fb_95"] is None else f" -> F_b <= {fr['Fb_95']:.4f} (bound {Fb:.4f})"))
        res["footings"][foot] = fr
    return res, n0


VARS = [("primary", {}), ("V-kcut", dict(kmax=0.1)), ("V-diag", dict(diag=True)), ("V-nosmooth", dict(smooth=False)),
        ("V-ns 0.92", dict(ns=0.92)), ("V-ns 1.00", dict(ns=1.00)), ("V-gamma15", dict(gamfix=1.5)),
        ("V-seed", dict(seeds=(10, 11, 12)))]
for name, kw in VARS:
    if name in RES["configs"] and len(RES["configs"][name].get("footings", {})) == 2:
        P(f"\n== CONFIG {name}: from checkpoint"); continue
    if STOP["flag"]:
        P("SIGTERM: checkpoint saved; rerun to resume."); save(); sys.exit(0)
    cf = Config(name, **kw)
    r, n0 = run_config(cf)
    if name == "primary":
        # K3 / K4 (canonical) + reported: linear-proxy comparison, flux PDF
        f = "canonical"
        rng = np.random.default_rng(0)
        noise = {z: rng.multivariate_normal(np.zeros(16), COV[z]) for z in ZS}
        pl1 = {z: cf.predict(z, n0[z][1], 1.0, f) + noise[z] for z in ZS}
        pl0 = {z: cf.predict(z, n0[z][1], 0.0, f) + noise[z] for z in ZS}
        s1 = mu_scan(cf, f, pl1, warm0=n0); s0p = mu_scan(cf, f, pl0, warm0=n0)
        g1 = r["footings"][f]["G1"]["pass"]
        r["K3"] = {"pass": (0.5 <= s1["mu_hat"] <= 1.5 and s1["dchi2_0"] >= 9) if g1 else True, "scan": s1, "vacuous": not g1}
        r["K4"] = {"pass": (s0p["mu95"] is not None and s0p["mu95"] < 1) if g1 else True, "scan": s0p, "vacuous": not g1}
        rep = {}
        for foot in FOOTS:
            rep[foot] = {}
            for z in ZS:
                x = cf.full(n0[z][1])
                a = cf.mk[z].flux_p1d(x, 0.0, foot, want_pdf=True); b_ = cf.mk[z].flux_p1d(x, 1.0, foot, want_pdf=True)
                kh = KV[z] * cf.mk[z].cz
                Plin_ad = p1d(cf.bg.PAD0_G * cf.mk[z].D2 * np.exp(-KG ** 2 * x[3] ** 2), kh)
                Plin_iso = p1d(cf.bg.m6[foot]["A_lin"] * W(KG * RL) ** 2 * np.exp(-KG ** 2 * x[3] ** 2), kh)
                rep[foot][z] = {"S_fgpa": (b_["P"] / a["P"] - 1).tolist(), "S_linear": (Plin_iso / Plin_ad).tolist(),
                                "frac_F_lt_0.05_mu0": a["frac_F_lt_0.05"], "frac_F_lt_0.05_mu1": b_["frac_F_lt_0.05"]}
            P(f"  [reported, {foot}] S at null best fit, FGPA vs linear (k 0.0063 / 0.025 / 0.1 s/km): " + "; ".join(
                f"z{z} " + "/".join(f"{rep[foot][z]['S_fgpa'][i]:+.3f}" for i in (0, 6, 12)) + " vs " +
                "/".join(f"{rep[foot][z]['S_linear'][i]:+.3f}" for i in (0, 6, 12)) +
                f" (F<0.05: {rep[foot][z]['frac_F_lt_0.05_mu0']:.3f}->{rep[foot][z]['frac_F_lt_0.05_mu1']:.3f})" for z in ZS))
        r["reported"] = rep
    RES["configs"][name] = r
    save()
    del cf
    import gc; gc.collect()

check("K3", RES["configs"]["primary"]["K3"]["pass"], f"planted mu=1: mu_hat {RES['configs']['primary']['K3']['scan']['mu_hat']:.3f}, "
      f"dchi2_0 {RES['configs']['primary']['K3']['scan']['dchi2_0']:.2f} (vacuous: {RES['configs']['primary']['K3']['vacuous']})",
      "mu_hat in [0.5,1.5], dchi2_0 >= 9 when G1 passes")
check("K4", RES["configs"]["primary"]["K4"]["pass"], f"planted null: mu95 {RES['configs']['primary']['K4']['scan']['mu95']} "
      f"(vacuous: {RES['configs']['primary']['K4']['vacuous']})", "mu95 < 1 when G1 passes")
RES["verdict"] = {}
P("\n== VERDICT")
for f in FOOTS:
    prim = RES["configs"]["primary"]["footings"][f]["class"]
    flips = [n for n, _ in VARS[1:] if RES["configs"][n]["footings"][f]["class"] != prim]
    v = prim + (" (ROBUST)" if not flips else f" (FRAGILE: flips in {', '.join(flips)})")
    RES["verdict"][f] = v
    P(f"  {f}: {v}")
peak = max(RES.get("peak_rss_GB", 0.0), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9)
check("K6", peak < 1.0, f"peak RSS {peak:.3f} GB, 1 thread, this session {time.time() - T0:.0f} s", "< 1 GB")
P(f"  checks: {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])} pass")
save()
os.replace(CKPT, os.path.join(HERE, f"p1d2_m6_fgpa_results{TAG}.json"))
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
