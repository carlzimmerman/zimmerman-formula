"""CFG922 (criteria a9d0669c5): is the cluster-core (MID 0.5-1.2 Mpc) lensing excess a baryon-census artefact?

Modes (one process at a time, OMP_NUM_THREADS=1, nice 10; run from this directory):
  CFG922_MODE=K   python3 cfg922.py      -> cfg922_K.out           (K0-K5)
                  python3 cfg922.py      -> cfg922.out, cfg922_results.json, cfg922_census.json   (main, both footings)
  CFG922_MUTATE=1 python3 cfg922.py      -> cfg922_MUTATE.out, cfg922_results_MUTATE.json         (M1-M5)
Inputs (read-only, nothing downloaded): CFG687 per-cluster arrays + results, CFG686 results + its ACCEPT setup (exec'd slices of
cfg686_shear.py / cfg687_stack.py, no KiDS shear columns loaded), cfg726_work arrays, CFG916/CFG817/CFG450/CFG652 results,
KiDS DR4 bright sample + LePhare, eRASS1 main tsv and FITS units, ACCEPT profiles, X-COP gas/stellar profiles, SLACS
Auger+2009, xGASS, BUDHIES. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, io, json, math, time, contextlib
import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import brentq
from scipy.special import erfc

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data")); DATA = os.path.join(REPO, "real_research", "data")
MODE = os.environ.get("CFG922_MODE", "MAIN"); MUT = os.environ.get("CFG922_MUTATE", "") == "1"
AMEND = os.environ.get("CFG922_AMEND", "")                                # "A1" = post-hoc census amendment (2026-10-20), see README
TAG = "_K" if MODE == "K" else ("_MUTATE" if MUT else ("_A1" if AMEND == "A1" else ""))
OUT = open(os.path.join(HERE, "cfg922" + TAG + ".out"), "w") if MODE in ("K", "MAIN") else open(os.devnull, "w")
assert not (AMEND and (MUT or MODE == "K")), "A1 applies to the main run only"
T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


sys.path.insert(0, LANES)
os.environ.pop("MUTATE", None)
import CFG4_common as C4                                                  # noqa: E402  committed nu_mono + both a0 footings
A0 = {"canonical": float(C4.A0["canonical"]), "alt": float(C4.A0["alt"])}
FEET = ("canonical", "alt")


def nu_s(y):                                                              # CFG695 / CFG726: g_N = g^2/(g + a0)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


KERN = {"s": nu_s, "mono": C4.nu_mono}
TRAPZ = np.trapz

# ---- CFG686 setup by exec (distances, ACCEPT profiles, projection, law_dsigma); the KiDS-source part is NOT executed ----
SRC686 = os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py"); TXT686 = open(SRC686).read()
NS = {"__file__": SRC686, "__name__": "cfg686"}
_argv = sys.argv; sys.argv = [SRC686, "UNUSED"]
with contextlib.redirect_stdout(io.StringIO()) as _buf:
    exec(TXT686.split("# ---- sources ----")[0], NS)
    NS["EDGES"] = np.logspace(np.log10(0.15), np.log10(3.0), 9); NS["RC"] = np.sqrt(NS["EDGES"][1:] * NS["EDGES"][:-1]); NS["M_BIAS"] = -0.01
    exec(TXT686.split("# ---- the law's prediction from ACCEPT gas ----")[1].split("# ---- measure ----")[0], NS)
sys.argv = _argv
SELFTEST = _buf.getvalue().strip().splitlines()
G, MSUN, MPC, KG, DM, RC, RGRID = NS["G"], NS["MSUN"], NS["MPC"], NS["KG_PER_MSUN_PC2"], NS["DM"], NS["RC"], NS["RGRID"]
CLIGHT = NS["c"]
# CFG687's law() verbatim (exec'd from its committed source, with CFG687's names)
SRC687 = os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_stack.py"); TXT687 = open(SRC687).read()
NS7 = dict(RGRID=RGRID, MPC=MPC, MSUN=MSUN, G=G, nu_mono=C4.nu_mono, sigma_proj=NS["sigma_proj"], RC=RC, KG=KG, np=np)
exec("def law(" + TXT687.split("def law(")[1].split("BR = [")[0], NS7)
law687 = NS7["law"]

R = RGRID; RM = R * MPC; NR = len(R); LR = np.log(R)
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
RAP = 0.5                                                                 # core aperture (Mpc), projected / 3D for gas
# ---- vectorised engine: Mb (N x NR, kg) -> DeltaSigma (N x 8, Msun/pc^2), identical algebra to CFG687 law()'s tail ----
_UG = NS["U_GRID"]; PRE = []
for Rj in RC:
    umax = np.arccosh(R[-1] / Rj); u = _UG * umax; rr = Rj * np.cosh(u)
    idxf = np.interp(np.log(rr), LR, np.arange(NR, dtype=float)); i0 = np.clip(np.floor(idxf).astype(int), 0, NR - 2); f = idxf - i0
    sel = R > Rj; fac = 4 * np.pi * (R[sel] * MPC) ** 2 * (1 - np.sqrt(1 - (Rj / R[sel]) ** 2))
    PRE.append((u, rr, i0, f, sel, fac))


def proj_cyl(M3, Rcyl):
    """projected (cylinder) mass inside Rcyl (Mpc) of a 3D cumulative mass M3 (N x NR) - CFG686's M2D algebra."""
    M3 = np.atleast_2d(M3); rho = np.gradient(M3, RM, axis=1) / (4 * np.pi * RM ** 2); sel = R > Rcyl
    fac = 4 * np.pi * (R[sel] * MPC) ** 2 * (1 - np.sqrt(1 - (Rcyl / R[sel]) ** 2))
    return np.array([np.interp(Rcyl, R, m) for m in M3]) + TRAPZ(rho[:, sel] * fac, R[sel] * MPC, axis=1)


def dsig(Mb, a0, nu, chunk=40):
    Mb = np.atleast_2d(Mb)
    if Mb.shape[0] > chunk:                                               # chunked over clusters to keep the process small
        return np.vstack([dsig(Mb[i:i + chunk], a0, nu, chunk) for i in range(0, Mb.shape[0], chunk)])
    gb = G * Mb / RM ** 2; gL = gb * nu(gb / a0) if a0 > 0 else gb
    ML = gL * RM ** 2 / G; rhoL = np.gradient(ML, RM, axis=1) / (4 * np.pi * RM ** 2)
    out = np.empty((Mb.shape[0], len(RC))); bad = ~(rhoL > 0).all(1)
    lrho = np.log(np.where(rhoL > 0, rhoL, 1e-300))
    for j, (u, rr, i0, f, sel, fac) in enumerate(PRE):
        lr_u = (1 - f) * lrho[:, i0] + f * lrho[:, i0 + 1]
        Sig = 2 * TRAPZ(np.exp(lr_u) * rr * MPC, u, axis=1)
        M2 = np.array([np.interp(RC[j], R, m) for m in ML]) + TRAPZ(rhoL[:, sel] * fac, R[sel] * MPC, axis=1)
        out[:, j] = (M2 / (np.pi * (RC[j] * MPC) ** 2) - Sig) / KG
    for i in np.where(bad)[0]:                                            # exact fallback (never expected)
        Sig = np.array([NS["sigma_proj"](rhoL[i], R, Rj) for Rj in RC])
        M2 = np.array([np.interp(Rj, R, ML[i]) + TRAPZ(4 * np.pi * (R[R > Rj] * MPC) ** 2 * rhoL[i][R > Rj] * (1 - np.sqrt(1 - (Rj / R[R > Rj]) ** 2)), R[R > Rj] * MPC) for Rj in RC])
        out[i] = (M2 / (np.pi * (RC * MPC) ** 2) - Sig) / KG
    return out


def gas_beta(mg, R500, beta=2 / 3, rcf=0.15):
    """CFG687 law()'s gas, kg, (N x NR)."""
    out = np.empty((len(mg), NR))
    for i in range(len(mg)):
        rc = rcf * R500[i]; shape = (1 + (R / rc) ** 2) ** (-1.5 * beta); shape[R > 3.0] = 0
        dm = 4 * np.pi * RM ** 2 * shape; M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RM))]
        out[i] = M * (mg[i] * MSUN / np.interp(R500[i], R, M))
    return out


def gas_accept(key, z, ne_fac=1.0, beta_shift=0.0):
    """CFG686 law_dsigma()'s gas (kg) and the rescaled data edge (Mpc); ne_fac only for MUTATE M5."""
    Pp = np.array(NS["prof"][key]); Pp = Pp[np.argsort(Pp[:, 0])]; rin, rout, ne = Pp[:, 0], Pp[:, 1], Pp[:, 2] * ne_fac
    ok_ = ne > 0; rin, rout, ne = rin[ok_], rout[ok_], ne[ok_]
    zz = np.linspace(0, z, 400); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7); DA_acc = TRAPZ(1 / E, zz) * CLIGHT / (70e3 / MPC) / MPC / (1 + z)
    q = (float(DM(z)) / (1 + z)) / DA_acc; rin, rout, ne = rin * q, rout * q, ne * q ** -0.5
    rm = 0.5 * (rin + rout); rho = 1.17 * NS["MP"] * ne * 1e6
    half = rm >= np.exp(0.5 * (np.log(rm[0]) + np.log(rm[-1]))); b0 = -np.polyfit(np.log(rm[half]), np.log(rho[half]), 1)[0]
    flag = not (b0 >= 1.5); b0 = 2.0 if flag else b0; b = b0 + beta_shift
    rho_g = np.interp(R, rm, rho, left=rho[0], right=np.nan); out = R > rm[-1]; rho_g[out] = rho[-1] * (R[out] / rm[-1]) ** (-b); rho_g[R > 3.0] = 0.0
    Mg = np.r_[0, np.cumsum(0.5 * (4 * np.pi * RM[1:] ** 2 * rho_g[1:] + 4 * np.pi * RM[:-1] ** 2 * rho_g[:-1]) * np.diff(RM))]
    return Mg, float(rm[-1])


A_BCG = 0.015 / 1.8153; A_ICL = 0.100 / 1.8153; A_BCG50 = 0.050 / 1.8153
def hern(a): return R ** 2 / (R + a) ** 2                                  # unit total mass


H15, H100, H50 = hern(A_BCG), hern(A_ICL), hern(A_BCG50)
P15, P100, P50 = (float(proj_cyl(h[None, :], RAP)[0]) for h in (H15, H100, H50))


# ---- band amplitudes ----
class Stack:
    def __init__(self, D, E, ra, kind, nboot=1000):
        self.D = np.nan_to_num(D); self.W = np.where(np.isfinite(E) & (E > 0), 1 / E ** 2, 0); self.n = len(D); self.kind = kind
        if kind == "jk":
            order = np.argsort(ra); self.patch = np.empty(self.n, int); self.patch[order] = np.arange(self.n) * 30 // self.n
        else:
            rb = np.random.default_rng(1); self.boot = [rb.integers(0, self.n, self.n) for _ in range(nboot)]

    def A(self, Pm, sel=None, D=None):
        D = self.D if D is None else D
        if sel is None: sel = np.arange(self.n)
        W, Dd, Pp = self.W[sel], D[sel], Pm[sel]
        return {b: float((W[:, j] * Dd[:, j]).sum() / (W[:, j] * Pp[:, j]).sum()) for b, j in BANDS.items()}

    def band(self, Pm, D=None):
        full = self.A(Pm, D=D)
        if self.kind == "jk":
            reps = [self.A(Pm, self.patch != p, D=D) for p in range(30)]
            sig = {k: float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2))) for k in full}
        else:
            bs = [self.A(Pm, s, D=D) for s in self.boot]; sig = {k: float(np.nanstd([b[k] for b in bs])) for k in full}
        return {k: (full[k], sig[k]) for k in full}


def zsc(b, k): return (b[k][0] - 1) / b[k][1]


# ---- inputs ----
PC7 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
R7 = json.load(open(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_results.json")))
R6 = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))
R916 = json.load(open(os.path.join(LANES, "CFG916_lock_and_release", "cfg916_results.json")))
ER = dict(mg=PC7["mg"], R500=PC7["R500"], z=PC7["z"], ra=PC7["ra"], dec=PC7["dec"], D=PC7["D"], E=PC7["E"])
NE = len(ER["mg"]); STE = Stack(ER["D"], ER["E"], ER["ra"], "jk")
AC = R6["clusters"]; NA = len(AC)
ACD = dict(D=np.nan_to_num(np.array([c["dsig"] for c in AC])), E=np.array([c["err"] for c in AC], float),
           z=np.array([c["z"] for c in AC]), ra=np.array([c["ra"] for c in AC]), dec=np.array([c["dec"] for c in AC]))
STA = Stack(ACD["D"], ACD["E"], ACD["ra"], "boot")
GAS_E = gas_beta(ER["mg"], ER["R500"]); GAS_A = np.array([gas_accept(c["key"], c["z"])[0] for c in AC])
RES = {"lane": "CFG922", "criteria": "a9d0669c5", "mode": MODE, "mutate": MUT, "selftest_686": SELFTEST}


def unit(ra, de):
    ra, de = np.radians(ra), np.radians(de); return np.c_[np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)]


def DA(z): return float(DM(z)) / (1 + z)


# ---- KiDS bright census ----
def read_cols(path, names, chunk=20000):
    """read selected binary-table columns with plain chunked file reads (no memory map; keeps the process small)."""
    from astropy.io import fits
    with fits.open(path, memmap=True, lazy_load_hdus=True) as h:
        hdr = h[1].header; dt = h[1].columns.dtype.newbyteorder(">"); loc = h.fileinfo(1)["datLoc"]
    n = int(hdr["NAXIS2"]); rl = int(hdr["NAXIS1"]); assert dt.itemsize == rl
    out = {k: np.empty(n, "f8") for k in names}
    buf = bytearray(chunk * rl)
    with open(path, "rb") as f:
        f.seek(loc)
        for i0 in range(0, n, chunk):
            m = min(chunk, n - i0); mv = memoryview(buf)[:m * rl]; f.readinto(mv); rec = np.frombuffer(mv, dtype=dt)
            for k in names: out[k][i0:i0 + m] = rec[k]
            del rec, mv
    return out


def load_bright():
    B = {}
    cb = read_cols(os.path.join(DATA, "lensing_rar", "KiDS_DR4_brightsample.fits"), ["RAJ2000", "DECJ2000", "zphot_ANNz2", "MAG_AUTO_CALIB", "masked"])
    B.update(ra=cb["RAJ2000"], dec=cb["DECJ2000"], z=cb["zphot_ANNz2"], mag=cb["MAG_AUTO_CALIB"], masked=cb["masked"].astype(int))
    cl = read_cols(os.path.join(DATA, "lensing_rar", "KiDS_DR4_brightsample_LePhare.fits"), ["RAJ2000", "MASS_MED", "MASS_SUP"])
    B.update(mmed=cl["MASS_MED"], msup=cl["MASS_SUP"]); B["align_maxdiff_deg"] = float(np.nanmax(np.abs(B["ra"] - cl["RAJ2000"]))); del cb, cl
    if AMEND == "A1":
        # A1 (post hoc): LePhare masses are from GAaP aperture photometry. Rebuild the GAaP r magnitude from the catalogue's own
        # absolute magnitude convention (m = M_abs + DM + K, LePhare default H0 70 / Om 0.3 bookkeeping, provisional) and scale each
        # mass to the total (AUTO) flux, brightening only: central capped at 1 mag (x2.5), upper uncapped. Masked galaxies kept.
        from astropy.cosmology import FlatLambdaCDM
        la = read_cols(os.path.join(DATA, "lensing_rar", "KiDS_DR4_brightsample_LePhare.fits"), ["REDSHIFT", "MAG_ABS_r", "K_COR_r"])
        zz = np.linspace(0.005, 1.5, 3000); dmz = FlatLambdaCDM(H0=70, Om0=0.3).distmod(zz).value
        good = (la["REDSHIFT"] > 0.005) & np.isfinite(la["MAG_ABS_r"]) & (la["MAG_ABS_r"] > -30) & np.isfinite(B["mag"])
        fs = np.where(good, B["mag"] - (la["MAG_ABS_r"] + np.interp(la["REDSHIFT"], zz, dmz) + la["K_COR_r"]), 0.0); del la
        B["fluxscale"] = fs; v = B["mmed"] > 5
        B["mmed"] = np.where(v, B["mmed"] - 0.4 * np.clip(fs, -1.0, 0.0), B["mmed"]); B["msup"] = np.where(v & (B["msup"] > 5), B["msup"] - 0.4 * np.minimum(fs, 0.0), B["msup"])
        B["masked"] = np.zeros_like(B["masked"])
    B["msup"] = np.where(np.isfinite(B["msup"]) & (B["msup"] >= B["mmed"]), B["msup"], B["mmed"])
    B["ok"] = (B["mmed"] > 5) & np.isfinite(B["z"])
    return B


def mlim_table(B):
    zg = np.round(np.arange(0.03, 0.56, 0.01), 3); s = (B["mag"] >= 19.5) & (B["mag"] <= 20.0) & B["ok"]
    zz, mm = B["z"][s], B["mmed"][s]; ml = []
    for z0 in zg:
        k = np.abs(zz - z0) <= 0.02; ml.append(float(np.median(mm[k])) if k.sum() >= 20 else np.nan)
    ml = np.array(ml); good = np.isfinite(ml)
    return zg[good], ml[good], dict(mag_range=[float(np.nanmin(B["mag"])), float(np.nanmax(B["mag"]))])


class Census:
    def __init__(self, B):
        self.B = B; self.xyz = unit(B["ra"], B["dec"]); self.tree = cKDTree(self.xyz)
        self.zg, self.ml, self.maginfo = mlim_table(B)

    def comp(self, z):
        x = 10 ** (np.interp(z, self.zg, self.ml) - 11.0)
        return float(math.exp(x)), float(1 / erfc(math.sqrt(x))), float(np.interp(z, self.zg, self.ml))

    def run(self, ra, dec, z, extra=None, thresholds=()):
        B = self.B; Da = DA(z); c0 = unit(np.array([ra]), np.array([dec]))[0]
        th5 = 5.0 / Da; ii = np.array(self.tree.query_ball_point(c0, 2 * math.sin(th5 / 2) * 1.0001), int)
        xyz = self.xyz[ii]; zz = B["z"][ii]; mk = B["masked"][ii]; ok = B["ok"][ii]; mmed = B["mmed"][ii]; msup = B["msup"][ii]
        if extra is not None:                                             # MUTATE M4: planted galaxy for this cluster only
            xyz = np.vstack([xyz, extra["xyz"]]); zz = np.r_[zz, extra["z"]]; mk = np.r_[mk, extra["masked"]]; ok = np.r_[ok, True]
            mmed = np.r_[mmed, extra["logm"]]; msup = np.r_[msup, extra["logm"]]
        dot = np.clip(np.einsum('ij,j->i', xyz, c0), -1, 1); Rg = np.arccos(dot) * Da
        win = ok & (np.abs(zz - z) <= 0.05 * (1 + z))
        ap = win & (Rg <= RAP); ann = win & (Rg >= 2.5) & (Rg <= 5.0); bc = win & (Rg <= 0.15); ratio = (np.pi * RAP ** 2) / (np.pi * (5.0 ** 2 - 2.5 ** 2))
        um = mk == 0; Mm, Ms = 10 ** mmed, 10 ** msup
        net_med = Mm[ap & um].sum() - Mm[ann & um].sum() * ratio
        bcg_med = Mm[bc & um].max() if (bc & um).any() else 0.0
        sig_sup = math.sqrt((Ms[ann] ** 2).sum() * ratio); net_sup = Ms[ap].sum() - Ms[ann].sum() * ratio
        bcg_sup = Ms[bc].max() if bc.any() else 0.0
        c_cen, c_up, mlim = self.comp(z)
        S_cen = bcg_med + c_cen * max(net_med - bcg_med, 0.0); S_up = bcg_sup + c_up * max(net_sup + 2 * sig_sup - bcg_sup, 0.0)
        out = dict(net_med=float(net_med), bcg_med=float(bcg_med), net_sup=float(net_sup), sig_sup=float(sig_sup), bcg_sup=float(bcg_sup),
                   c_cen=c_cen, c_up=c_up, mlim=mlim, S_cen=float(S_cen), S_up=float(S_up), n_ap=int((ap & um).sum()),
                   n_ann_allz=int(((Rg >= 2.5) & (Rg <= 5.0)).sum()), n_ap_allz=int((Rg <= RAP).sum()), bg_med_per_ap=float(Mm[ann & um].sum() * ratio))
        out["coverage"] = float(out["n_ap_allz"] / (out["n_ann_allz"] * ratio)) if out["n_ann_allz"] > 0 else 0.0
        for t in thresholds:
            hi = mmed > t; out[f"net_above_{t:.2f}"] = float(Mm[ap & um & hi].sum() - Mm[ann & um & hi].sum() * ratio)
            out[f"bcg_above_{t:.2f}"] = float(bcg_med if bcg_med > 10 ** t else 0.0)
        return out


def census_652(B, ra, dec, z, R500_arcmin):
    """CFG652's frozen recipe (cfg652_test.py lines 80-105), its planar ra*cos(dec) metric and G09 box, for K4."""
    box = (B["ra"] > 122) & (B["ra"] < 150) & (B["dec"] > -7) & (B["dec"] < 9)
    bra, bde, bz, bmk, bm = B["ra"][box], B["dec"][box], B["z"][box], B["masked"][box], B["mmed"][box]
    ok = (bmk == 0) & (bm > 5) & np.isfinite(bz); bra, bde, bz, bm = bra[ok], bde[ok], bz[ok], 10 ** bm[ok]
    bt = cKDTree(np.c_[bra * np.cos(np.radians(bde)), bde]); Mc = np.zeros(len(ra)); Mb = np.zeros(len(ra))
    for i in range(len(ra)):
        th = R500_arcmin[i] / 60.0; p = [ra[i] * math.cos(math.radians(dec[i])), dec[i]]; zw = np.abs(bz - z[i]) <= 0.05 * (1 + z[i])
        kin = np.array(bt.query_ball_point(p, th), int); kin = kin[zw[kin]]
        kout = np.array(bt.query_ball_point(p, 6 * th), int); kout = kout[zw[kout]]
        k3 = np.array(bt.query_ball_point(p, 3 * th), int); k3 = k3[zw[k3]]; ann = np.setdiff1d(kout, k3)
        bkg = bm[ann].sum() * (1.0 / (36 - 9)); net = bm[kin].sum() - bkg
        inner = np.array(bt.query_ball_point(p, 0.2 * th), int); inner = inner[zw[inner]]
        Mb[i] = bm[inner].max() if len(inner) else 0.0; Mc[i] = max(net, Mb[i])
    return Mc, Mb


# ---- other on-disk brackets ----
def read_erass_tsv():
    rows = []
    for l in open(os.path.join(EXT, "cfg687_inputs", "erass1_main.tsv")):
        r = l.rstrip("\n").split("\t")
        try: rows.append((r[0].strip(), float(r[1]), float(r[2]), float(r[3]), float(r[5]) * 1e11, float(r[8]) / 1e3))
        except Exception: continue
    return rows


def xcop_list():
    from astropy.io import fits
    xd = os.path.join(DATA, "xcop"); out = []
    for nm in sorted(n for n in os.listdir(xd) if os.path.isdir(os.path.join(xd, n))):
        fg = os.path.join(xd, nm, f"{nm}_fgas_profile.fits")
        if not os.path.exists(fg): continue
        F = fits.open(fg)["FGAS"]; h = F.header; d = F.data
        rec = dict(name=nm, ra=float(h["RA"]), dec=float(h["DEC"]), z=float(h["REDSHIFT"]), R500=float(h["R500"]) / 1e3, M500=float(h["M500"]) * 1e14,
                   tunit=F.columns["RADIUS"].unit, r=np.asarray(d["RADIUS"], float) * float(h["R500"]) / 1e3, mgas=np.asarray(d["MGAS"], float),
                   mnfw_at1=float(math.exp(np.interp(0.0, np.log(np.asarray(d["RADIUS"], float)), np.log(np.asarray(d["M_NFW"], float))))))
        fs = os.path.join(xd, nm, f"{nm}_mstar.fits")
        if os.path.exists(fs):
            S = fits.open(fs); rec["mstar_tunit_raw"] = S["MSTAR_RAW"].columns["RADIUS"].unit
            sm = S["MSTAR_SMOOTHED"].data; rec["rs"] = np.asarray(sm["RADIUS"], float) / 1e3; rec["ms"] = np.asarray(sm["MSTAR"], float)
            rec["ms_hi"] = np.asarray(sm["MSTAR_HI"], float)
        out.append(rec)
    return out


def m_at(r, m, r0): return float(math.exp(np.interp(math.log(r0), np.log(r), np.log(m))))


def gas_crossmatch(ne_fac=1.0):
    er = read_erass_tsv(); exyz = unit(np.array([e[1] for e in er]), np.array([e[2] for e in er])); et = cKDTree(exyz)
    ez = np.array([e[3] for e in er]); ch = 2 * math.sin(math.radians(3 / 60) / 2)
    def best(ra, de, z):
        c0 = unit(np.array([ra]), np.array([de]))[0]; ii = [i for i in et.query_ball_point(c0, ch) if abs(ez[i] - z) <= 0.02]
        if not ii: return None
        return min(ii, key=lambda i: float(np.linalg.norm(exyz[i] - c0)))
    rows = {}
    for nm, (ra, de, z, kT) in NS["T1"].items():                        # ACCEPT (Chandra deprojected n_e)
        key = NS["match"](nm)
        if key is None: continue
        i = best(ra, de, z)
        if i is None: continue
        Mg, redge = gas_accept(key, z, ne_fac=ne_fac); rcmp = min(RAP, redge)
        if rcmp < 0.2: continue
        Mp = gas_beta(np.array([er[i][4]]), np.array([er[i][5]]))[0]
        rows[er[i][0]] = dict(src="ACCEPT", name=nm, erass=er[i][0], z=z, rcmp=rcmp, rho=float(np.interp(rcmp, R, Mg) / np.interp(rcmp, R, Mp)),
                              mgas500_erass=er[i][4], R500_erass=er[i][5])
    for x in xcop_list():                                                # X-COP (XMM MGAS), preferred where both exist
        i = best(x["ra"], x["dec"], x["z"])
        if i is None: continue
        Mp = gas_beta(np.array([er[i][4]]), np.array([er[i][5]]))[0]
        rows[er[i][0]] = dict(src="X-COP", name=x["name"], erass=er[i][0], z=x["z"], rcmp=RAP,
                              rho=m_at(x["r"], x["mgas"], RAP) / float(np.interp(RAP, R, Mp) / MSUN), mgas500_erass=er[i][4], R500_erass=er[i][5])
    return list(rows.values())


def slacs():
    lines = [l.rstrip("\n") for l in open(os.path.join(DATA, "slacs_auger2009_lenses.tsv")) if not l.startswith("#") and l.strip()]
    hdr = lines[0].split("\t"); rows = [l.split("\t") for l in lines[3:]]
    def col(n):
        k = hdr.index(n); v = []
        for r in rows:
            try: v.append(float(r[k]))
            except Exception: v.append(np.nan)
        return np.array(v)
    Fc, lmc, lms = col("Fc"), col("logMc"), col("logMs"); g = np.isfinite(Fc) & (Fc > 0)
    return dict(n=int(g.sum()), alpha_max=float(np.percentile(1 / Fc[g], 95)), inv_fc_median=float(np.median(1 / Fc[g])),
                salp_over_chab=float(np.nanmedian(10 ** (lms - lmc))))


def xgass():
    f = os.path.join(DATA, "xgass", "xGASS_representative_sample.ascii"); hdr = None; rows = []
    for l in open(f):
        if l.startswith("#"): hdr = l[1:].split(); continue
        rows.append(l.split())
    k = {n: hdr.index(n) for n in ("lgMstar", "lgGF", "HIsrc")}
    ms = np.array([float(r[k["lgMstar"]]) for r in rows]); gf = np.array([float(r[k["lgGF"]]) for r in rows]); src = np.array([int(float(r[k["HIsrc"]])) for r in rows])
    s = ms >= 11.0
    return dict(n=int(s.sum()), n_limits=int((s & (src == 4)).sum()), f95=float(np.percentile(10 ** gf[s], 95)), fmed=float(np.median(10 ** gf[s])))


def budhies_a963():
    T1 = NS["T1"]; cand = [n for n in T1 if "963" in n and ("ABELL" in n.upper() or n.upper().startswith("A"))]
    if not cand: return dict(status="A963 not in ACCEPT table1")
    nm = cand[0]; ra, de, z, kT = T1[nm]; key = NS["match"](nm)
    Da = DA(z); c0 = unit(np.array([ra]), np.array([de]))[0]; hi = 0.0; n = 0
    for l in open(os.path.join(EXT, "cds_tables", "J_MNRAS_496_3531", "tablea1.dat")):
        try:
            rah, ram, ras = int(l[26:28]), int(l[29:31]), float(l[32:37]); sg = -1 if l[37] == "-" else 1
            ded, dem, des = int(l[38:40]), int(l[41:43]), float(l[44:48]); zh = float(l[49:56]); mhi = float(l[98:103]) * 1e9
        except Exception: continue
        rg, dg = 15 * (rah + ram / 60 + ras / 3600), sg * (ded + dem / 60 + des / 3600)
        sep = math.acos(min(1.0, float(unit(np.array([rg]), np.array([dg]))[0] @ c0))) * Da
        if sep <= RAP and abs(zh - z) * 2.998e5 / (1 + z) <= 3000: hi += mhi; n += 1
    out = dict(name=nm, z=z, n_hi=n, MHI_ap=hi)
    if key:
        Mg, redge = gas_accept(key, z); out.update(Mgas3D_ap=float(np.interp(RAP, R, Mg) / MSUN), data_edge=redge,
                                                   HI_over_gas=float(hi / (np.interp(RAP, R, Mg) / MSUN)))
    return out


# ---- model building ----
def members_template(gas):
    return gas / proj_cyl(gas, RAP)[:, None]                              # unit projected mass inside RAP


def stars_profile(gas, bcg, tot):
    """BCG (total mass, Hernquist R_e 15 kpc) + members (tot - bcg) ~ gas, normalised to projected mass in RAP. kg."""
    mem = np.maximum(np.asarray(tot) - np.asarray(bcg), 0.0)
    return (np.asarray(bcg)[:, None] * H15[None, :] + mem[:, None] * members_template(gas)) * MSUN


def solve(fun, st, lo, hi, target="A1", D=None, maxhi=1e3):
    """root of A_MID(v) = 1 (target 'A1') or Z_MID(v) = 2 ('Z2'); fun(v) -> per-cluster DeltaSigma models."""
    def g(v):
        b = st.band(fun(v), D=D)
        return (b["MID"][0] - 1.0) if target == "A1" else (b["MID"][0] - 1.0 - 2.0 * b["MID"][1])
    glo = g(lo)
    if glo <= 0: return dict(value=lo, status="no excess at the lower bound")
    h = hi
    while g(h) > 0:
        h *= 2.0
        if h > maxhi: return dict(value=float("inf"), status=f"needed > {maxhi:g}")
    v = brentq(g, lo, h, xtol=1e-7, rtol=1e-9, maxiter=200)
    return dict(value=float(v), status="solved")


def cls_mult(need, upper):
    if not np.isfinite(need): return "CANNOT"
    if need <= upper: return "CAN EXPLAIN"
    return "STRAINED" if need <= 2 * upper else "CANNOT"


def cls_sign(a_base, a_best):
    if a_best <= 1: return "CAN EXPLAIN"
    return "CANNOT" if (a_base - a_best) < 0.5 * (a_base - 1) else "STRAINED"


# =====================================================================================================================
if MODE == "K":
    from astropy.io import fits
    P("CFG922 K stage (criteria a9d0669c5)."); P("  CFG686 projection self-test:", SELFTEST[-1] if SELFTEST else "-")
    K = {}
    # K0 units
    h = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"), memmap=True)[1].columns
    u = dict(zip(h.names, h.units)); X = xcop_list()
    k0 = dict(MGAS500=u.get("MGAS500"), R500=u.get("R500"), xcop_tunit=sorted(set(x["tunit"] for x in X)),
              xcop_mstar_tunit=sorted(set(x.get("mstar_tunit_raw", "-") for x in X)),
              xcop_mnfw1_over_M500=[round(x["mnfw_at1"] / x["M500"], 4) for x in X])
    k0["pass"] = (k0["MGAS500"] == "10**11 solMass" and k0["R500"] == "kpc" and k0["xcop_tunit"] == ["R/R500"]
                  and all(abs(v - 1) < 0.02 for v in k0["xcop_mnfw1_over_M500"]))
    K["K0"] = k0; P(f"K0 units: {k0}")
    # K1 CFG687 (nu_mono, exec'd law) and the vectorised engine identity
    PL_exec = np.array([law687(dict(Mgas500=ER["mg"][i], R500=ER["R500"][i]), A0["canonical"]) for i in range(NE)])
    PA_exec = np.array([law687(dict(Mgas500=ER["mg"][i], R500=ER["R500"][i]), A0["alt"]) for i in range(NE)])
    r1 = float(np.max(np.abs(PL_exec / PC7["PL"] - 1)))
    eng = {f: dsig(GAS_E * 1.2, A0[f], C4.nu_mono) for f in FEET}
    r1e = max(float(np.max(np.abs(eng["canonical"] / PL_exec - 1))), float(np.max(np.abs(eng["alt"] / PA_exec - 1))))
    bc, ba = STE.band(PL_exec), STE.band(PA_exec)
    sc, sa = R7["A"]["canonical|b0.67|rc0.15|f0.20"], R7["A"]["alt|b0.67|rc0.15|f0.20"]
    d1 = max(abs(bc[b][i] - sc[b][i]) for b in ("MID", "OUTER") for i in (0, 1)); d1 = max(d1, max(abs(ba[b][i] - sa[b][i]) for b in ("MID", "OUTER") for i in (0, 1)))
    K["K1"] = dict(maxrel_PL=r1, engine_vs_exec=r1e, A_can=bc, A_alt=ba, maxdiff_A=d1, pass_=bool(r1 < 1e-9 and d1 < 1e-6 and r1e < 1e-10))
    P(f"K1 CFG687: law vs stored PL max rel {r1:.2e}; engine vs exec'd law {r1e:.2e}; MID {bc['MID'][0]:.4f}±{bc['MID'][1]:.4f} / "
      f"{ba['MID'][0]:.4f}±{ba['MID'][1]:.4f}; max |dA| {d1:.1e} -> {'PASS' if K['K1']['pass_'] else 'FAIL'}")
    # K2 CFG686 (ACCEPT), replaying its shared bootstrap sequence
    keys = list(AC[0]["pred"].keys()) + ["newton"]; rb = np.random.default_rng(1); draws = {k: [rb.integers(0, NA, NA) for _ in range(1000)] for k in keys}
    m2 = 0.0; out2 = {}
    for foot in FEET:
        k = f"{foot}|b+0.0|f0.20"; Pst = np.array([c["pred"][k] for c in AC])
        Pre = np.array([NS["law_dsigma"](c, A0[foot], 0.0, 0.20)[0] for c in AC]); Peng = dsig(GAS_A * 1.2, A0[foot], C4.nu_mono)
        m2 = max(m2, float(np.max(np.abs(Pre / Pst - 1))), float(np.max(np.abs(Peng / Pst - 1))))
        A = STA.A(Pre); bs = [STA.A(Pre, s) for s in draws[k]]; sig = float(np.nanstd([b["MID"] for b in bs]))
        out2[foot] = (A["MID"], sig); st = R6["A"][k]["MID"]; m2a = max(abs(A["MID"] - st[0]), abs(sig - st[1])); out2[foot + "_diff"] = m2a
    K["K2"] = dict(maxrel_pred=m2, A_MID=out2, pass_=bool(m2 < 1e-9 and max(out2["canonical_diff"], out2["alt_diff"]) < 1e-6))
    P(f"K2 CFG686: preds max rel {m2:.2e}; MID {out2['canonical'][0]:.4f}±{out2['canonical'][1]:.4f} / {out2['alt'][0]:.4f}±{out2['alt'][1]:.4f}"
      f" -> {'PASS' if K['K2']['pass_'] else 'FAIL'}")
    # K3 CFG916 / CFG726 nu_s plain law
    W726 = np.load(os.path.join(EXT, "cfg726_work", "erass.npy"), allow_pickle=True); A726 = np.load(os.path.join(EXT, "cfg726_work", "accept.npy"), allow_pickle=True)
    k3 = {}; ok3 = True
    for foot in FEET:
        Ls = np.array([d[f"law|s|{foot}"] for d in W726]); Le = dsig(GAS_E * 1.2, A0[foot], nu_s); rel = float(np.max(np.abs(Le / Ls - 1)))
        La = np.array([d[f"law|s|{foot}"] for d in A726]); Lae = dsig(GAS_A * 1.2, A0[foot], nu_s); rela = float(np.max(np.abs(Lae / La - 1)))
        be, ba_ = STE.band(Le), STA.band(Lae); st = R916["readings"]["LR-c"]["M"]["can" if foot == "canonical" else "alt"]["peri"]
        de = max(abs(be["MID"][0] - st["eRASS1"]["A_MID"][0]), abs(be["MID"][1] - st["eRASS1"]["A_MID"][1]))
        da = max(abs(ba_["MID"][0] - st["ACCEPT"]["A_MID"][0]), abs(ba_["MID"][1] - st["ACCEPT"]["A_MID"][1]))
        k3[foot] = dict(rel_erass=rel, rel_accept=rela, eRASS1_MID=be["MID"], ACCEPT_MID=ba_["MID"], diff_e=de, diff_a=da)
        ok3 &= rel < 1e-6 and rela < 1e-6 and de < 1e-6 and da < 1e-6
        P(f"K3 CFG916/726 nu_s [{foot}]: law rel {rel:.1e} / {rela:.1e}; eRASS1 MID {be['MID'][0]:.4f}±{be['MID'][1]:.4f} (stored "
          f"{st['eRASS1']['A_MID'][0]:.4f}); ACCEPT MID {ba_['MID'][0]:.4f}±{ba_['MID'][1]:.4f} (stored {st['ACCEPT']['A_MID'][0]:.4f}); max diff {max(de, da):.1e}")
    K["K3"] = dict(k3, pass_=bool(ok3)); P(f"K3 -> {'PASS' if ok3 else 'FAIL'}")
    # K4 census recipe vs CFG652 stored M_cond / M_bcg
    B = load_bright(); I652 = np.load(os.path.join(EXT, "cfg652_work", "cfg652_inputs.npz"))
    Mc, Mb = census_652(B, I652["ra"], I652["dec"], I652["z"], I652["R500_arcmin"])
    r4 = max(float(np.max(np.abs(Mc - I652["Mcond"]) / np.maximum(I652["Mcond"], 1))), float(np.max(np.abs(Mb - I652["Mbcg"]) / np.maximum(I652["Mbcg"], 1))))
    K["K4"] = dict(n=int(len(Mc)), maxrel=r4, align_maxdiff_deg=B["align_maxdiff_deg"], pass_=bool(r4 < 1e-9 and B["align_maxdiff_deg"] < 1e-6))
    P(f"K4 census recipe vs CFG652 (N {len(Mc)}): max rel {r4:.1e}; bright/LePhare RA alignment {B['align_maxdiff_deg']:.1e} deg -> {'PASS' if K['K4']['pass_'] else 'FAIL'}")
    # K5 record values
    c817 = json.load(open(os.path.join(LANES, "CFG817_erass1_countrate_selection", "cfg817_results_CONDN.json")))["corr_terciles"]
    c450 = json.load(open(os.path.join(LANES, "CFG450_xcop_gas_radius_audit", "cfg450_results.json")))
    br = {f: [v["MID"][0] for k, v in R7["A"].items() if k.startswith(f + "|")] for f in FEET}
    K["K5"] = dict(cfg817_corr=c817, cfg450=[c450["verdict_units"], c450["decision"]], cfg687_bracket_minMID={f: min(br[f]) for f in FEET},
                   cfg687_bracket_n={f: len(br[f]) for f in FEET}, pass_=bool(len(c817) == 3 and c450["decision"] == "UNCHANGED"))
    P(f"K5 record: CFG817 credible corrections {np.round(c817, 4).tolist()}; CFG450 {K['K5']['cfg450']}; CFG687 bracket cells {K['K5']['cfg687_bracket_n']}, "
      f"min MID {np.round(list(K['K5']['cfg687_bracket_minMID'].values()), 3).tolist()}")
    allp = all(K[k].get("pass", K[k].get("pass_")) for k in K); P(f"\nK overall: {'ALL PASS' if allp else 'FAILURES PRESENT'}  ({time.time() - T0:.0f} s)")
    json.dump(dict(RES, K=K, all_pass=allp), open(os.path.join(HERE, "cfg922_K.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    sys.exit(0 if allp else 1)

# =====================================================================================================================
# MAIN and MUTATE share the census
P(f"CFG922 {'MUTATE' if MUT else 'MAIN'}{' + POST-HOC CENSUS AMENDMENT A1 (2026-10-20)' if AMEND == 'A1' else ''} (criteria a9d0669c5). "
  f"Samples: eRASS1 {NE} (decisive), ACCEPT {NA} (reported).")
B = load_bright(); CEN = Census(B); P(f"  bright sample {len(B['ra']):,} rows; M_lim(z) table {len(CEN.zg)} nodes, z 0.03-0.55: "
                                     f"{np.round(np.interp([0.1, 0.2, 0.3, 0.4, 0.5], CEN.zg, CEN.ml), 2).tolist()}; mag range {CEN.maginfo['mag_range']}")
THR = (10.5, 11.0)
CE = [CEN.run(ER["ra"][i], ER["dec"][i], ER["z"][i], thresholds=THR) for i in range(NE)]
CA = [CEN.run(ACD["ra"][i], ACD["dec"][i], ACD["z"][i], thresholds=THR) for i in range(NA)]
P(f"  census done ({time.time() - T0:.0f} s)")


def arr(C, k): return np.array([c[k] for c in C])


A1INFO = {}
if AMEND == "A1":
    # A1 footprint gaps: coverage = all-z bright count in the aperture / (annulus density x area). < 0.5: NOT MEASURED, given the
    # measured clusters' median (central) and 84th-percentile (upper) S/gas_cyl and median BCG share; 0.5-1: divided by coverage.
    for nmA, C, gasA in (("eRASS1", CE, GAS_E), ("ACCEPT", CA, GAS_A)):
        gcyl = proj_cyl(gasA, RAP) / MSUN; cov = arr(C, "coverage"); meas = cov >= 0.5
        for c, cv in zip(C, cov):
            if 0.5 <= cv < 1.0:
                for k in ("S_cen", "S_up"): c[k] = c[k] / cv
        rc_, ru_ = arr(C, "S_cen")[meas] / gcyl[meas], arr(C, "S_up")[meas] / gcyl[meas]
        fb_c = float(np.median(arr(C, "bcg_med")[meas] / np.maximum(arr(C, "S_cen")[meas], 1))); fb_u = float(np.median(arr(C, "bcg_sup")[meas] / np.maximum(arr(C, "S_up")[meas], 1)))
        for i in np.where(~meas)[0]:
            C[i].update(S_cen=float(np.median(rc_) * gcyl[i]), S_up=float(np.percentile(ru_, 84) * gcyl[i]), not_measured=True)
            C[i].update(bcg_med=fb_c * C[i]["S_cen"], bcg_sup=fb_u * C[i]["S_up"])
        A1INFO[nmA] = dict(n_not_measured=int((~meas).sum()), n_partial=int(((cov >= 0.5) & (cov < 1)).sum()), ratio_cen_median=float(np.median(rc_)),
                           ratio_up_84=float(np.percentile(ru_, 84)), bcg_share_cen=fb_c, bcg_share_up=fb_u)
    fsg = B["fluxscale"][B["ok"]]
    A1INFO["fluxscale_median"] = float(np.median(fsg)); A1INFO["fluxscale_p16_p84"] = [float(np.percentile(fsg, 16)), float(np.percentile(fsg, 84))]
    P(f"  A1 census amendment: {json.dumps(A1INFO)}")


SAMPLES = {"eRASS1": dict(gas=GAS_E, st=STE, C=CE, n=NE), "ACCEPT": dict(gas=GAS_A, st=STA, C=CA, n=NA)}
for s in SAMPLES.values():
    s["Scen"], s["Sup"] = arr(s["C"], "S_cen"), arr(s["C"], "S_up"); s["Bcen"], s["Bup"] = arr(s["C"], "bcg_med"), arr(s["C"], "bcg_sup")
    s["gcyl"] = proj_cyl(s["gas"], RAP) / MSUN; s["g3d"] = s["gas"][:, np.searchsorted(R, RAP)] / MSUN
    s["stars_cen"] = stars_profile(s["gas"], s["Bcen"], s["Scen"]); s["stars_up"] = stars_profile(s["gas"], s["Bup"], s["Sup"])
    s["base_stars_cyl"] = 0.20 * s["gcyl"]

if MUT:
    # ------------------------------------------------- MUTATE -------------------------------------------------
    M = {}; s = SAMPLES["eRASS1"]; st = s["st"]; ok_all = True
    for foot in FEET:
        a0 = A0[foot]; nu = nu_s; cen = s["gas"] + s["stars_cen"]
        ext = lambda k: (cen + (k * s["Sup"] / P15)[:, None] * H15[None, :] * MSUN)
        # M1 hidden concentrated baryons (4 x S_up), noiseless and noisy
        D1 = dsig(ext(4.0), a0, nu); a_seen = st.band(dsig(cen, a0, nu), D=D1)["MID"]
        r1 = solve(lambda k: dsig(ext(k), a0, nu), st, 0.0, 1.0, D=D1)
        rng = np.random.default_rng(922); noise = rng.normal(0, 1, D1.shape) * np.where(s["st"].W > 0, 1 / np.sqrt(np.where(s["st"].W > 0, s["st"].W, 1)), 0)
        noise[s["st"].W < 1e-12] = 0; D1n = D1 + noise; r1n = solve(lambda k: dsig(ext(k), a0, nu), st, 0.0, 1.0, D=D1n)
        p1 = abs(r1["value"] / 4 - 1) < 0.01 and a_seen[0] > 1 and abs(r1n["value"] / 4 - 1) < 0.25
        # M2 gas x 1.5
        D2 = dsig(1.5 * s["gas"] + s["stars_cen"], a0, nu); r2 = solve(lambda m: dsig(m * s["gas"] + s["stars_cen"], a0, nu), st, 1.0, 2.0, D=D2)
        p2 = abs(r2["value"] / 1.5 - 1) < 0.01
        # M3 null
        D3 = dsig(cen, a0, nu); a3 = st.band(dsig(cen, a0, nu), D=D3)["MID"][0]
        r3 = solve(lambda k: dsig(ext(k), a0, nu), st, 0.0, 1.0, D=D3); r3m = solve(lambda m: dsig(m * s["gas"] + s["stars_cen"], a0, nu), st, 1.0, 2.0, D=D3)
        p3 = abs(a3 - 1) < 1e-9 and r3["value"] <= 1e-6 and abs(r3m["value"] - 1) <= 1e-6
        # M1b (POST-HOC AMENDMENT 2026-10-20, no class weight): the frozen M1 injection (4 x S_up) moves A_MID only to ~1.1, below the
        # shear noise, so its noisy leg cannot test recovery. Inject an excess of the real size: a concentrated 2.0 x gas_cyl mass.
        extU = lambda l: (cen + (l * s["gcyl"] / P15)[:, None] * H15[None, :] * MSUN)
        D1b = dsig(extU(2.0), a0, nu); a_seen_b = st.band(dsig(cen, a0, nu), D=D1b)["MID"]
        r1b = solve(lambda l: dsig(extU(l), a0, nu), st, 0.0, 1.0, D=D1b); r1bn = solve(lambda l: dsig(extU(l), a0, nu), st, 0.0, 1.0, D=D1b + noise)
        p1b = abs(r1b["value"] / 2 - 1) < 0.01 and a_seen_b[0] > 1 and abs(r1bn["value"] / 2 - 1) < 0.25
        P(f"[{foot}] M1b (post hoc) hidden 2.0 x gas_cyl: pipeline sees MID {a_seen_b[0]:.3f}; recovers {r1b['value']:.4f} (noisy {r1bn['value']:.3f}) -> "
          f"{'BITES' if p1b else 'FAIL'}")
        M[foot] = dict(M1=dict(A_MID_seen=a_seen, k_rec=r1, k_rec_noisy=r1n, noiseless_pass=bool(abs(r1["value"] / 4 - 1) < 0.01 and a_seen[0] > 1), pass_=bool(p1)),
                       M1b_posthoc=dict(A_MID_seen=a_seen_b, l_rec=r1b, l_rec_noisy=r1bn, pass_=bool(p1b)),
                       M2=dict(m_rec=r2, pass_=bool(p2)), M3=dict(A_MID=a3, k=r3, m=r3m, pass_=bool(p3)))
        ok_all &= p1 and p2 and p3; ok_amended = M.get("_amended", True) and p1b and p2 and p3; M["_amended"] = ok_amended
        P(f"[{foot}] M1 hidden 4xS_up: pipeline sees MID {a_seen[0]:.3f}±{a_seen[1]:.3f}; recovers k {r1['value']:.4f} (noisy {r1n['value']:.3f}) -> "
          f"{'BITES' if p1 else 'FAIL'}")
        P(f"[{foot}] M2 gas x1.5: recovers m {r2['value']:.5f} -> {'BITES' if p2 else 'FAIL'};  M3 null: A_MID {a3:.12f}, k {r3['value']:.2e}, m {r3m['value']:.6f} -> "
          f"{'PASS' if p3 else 'FAIL'}")
    # M4 census plant + random null
    d4 = []
    for i in range(NE):
        x0 = unit(np.array([ER["ra"][i]]), np.array([ER["dec"][i]]))
        c1 = CEN.run(ER["ra"][i], ER["dec"][i], ER["z"][i], extra=dict(xyz=x0, z=np.array([ER["z"][i]]), masked=np.array([0]), logm=np.array([12.0])))
        d4.append(c1["net_med"] - CE[i]["net_med"])
    d4 = np.array(d4); p4a = float(np.max(np.abs(d4 / 1e12 - 1))) < 0.01
    rr = np.random.default_rng(9220); rnet = []
    for i in range(NE):
        for _ in range(20):
            a = rr.uniform(0, 2 * np.pi); sh = rr.uniform(1, 3); ra_ = (ER["ra"][i] + sh * np.cos(a) / np.cos(np.radians(ER["dec"][i]))) % 360; de_ = ER["dec"][i] + sh * np.sin(a)
            c1 = CEN.run(ra_, de_, ER["z"][i])
            if c1["n_ann_allz"] >= 0.5 * CE[i]["n_ann_allz"]: rnet.append(c1["net_med"]); break
    rnet = np.array(rnet); sem = float(rnet.std(ddof=1) / math.sqrt(len(rnet))); p4b = abs(float(rnet.mean())) < 3 * sem
    M["M4"] = dict(plant_maxrel=float(np.max(np.abs(d4 / 1e12 - 1))), random_n=int(len(rnet)), random_mean=float(rnet.mean()), random_sem=sem,
                   cluster_mean_net=float(arr(CE, "net_med").mean()), pass_=bool(p4a and p4b))
    P(f"M4 census: planted 1e12 recovered to max rel {M['M4']['plant_maxrel']:.1e}; random positions N {len(rnet)} mean net {rnet.mean():.3e} ± {sem:.2e} "
      f"(clusters {M['M4']['cluster_mean_net']:.3e}) -> {'BITES' if M['M4']['pass_'] else 'FAIL'}")
    # M5 cross-match plant
    g1 = gas_crossmatch(1.0); g2 = gas_crossmatch(2.0); acc1 = {r["erass"]: r["rho"] for r in g1 if r["src"] == "ACCEPT"}; acc2 = {r["erass"]: r["rho"] for r in g2 if r["src"] == "ACCEPT"}
    rr5 = [acc2[k] / acc1[k] for k in acc1 if k in acc2]; p5 = len(rr5) > 0 and max(abs(x - 2) for x in rr5) < 1e-9
    M["M5"] = dict(n=len(rr5), max_dev=float(max(abs(x - 2) for x in rr5)) if rr5 else None, pass_=bool(p5))
    P(f"M5 ACCEPT n_e x2: {len(rr5)} matched ratios double to max dev {M['M5']['max_dev']:.1e} -> {'BITES' if p5 else 'FAIL'}")
    ok_all &= M["M4"]["pass_"] and p5; amended = bool(M.pop("_amended") and M["M4"]["pass_"] and p5)
    P(f"\nMUTATE as frozen: {'every arm bites / null passes' if ok_all else 'FAILURES PRESENT (see M1 noisy leg)'}; with the post-hoc M1b in place of M1's "
      f"noisy leg: {'every arm bites' if amended else 'FAILURES PRESENT'} ({time.time() - T0:.0f} s)")
    json.dump(dict(RES, MUTATE=M, all_pass_frozen=bool(ok_all), all_pass_with_M1b_posthoc=amended), open(os.path.join(HERE, "cfg922_results_MUTATE.json"), "w"), indent=1,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    sys.exit(0 if ok_all else 1)

# ------------------------------------------------- MAIN -------------------------------------------------
P("\n== Brackets from disk")
GX = gas_crossmatch(); rhos = np.array([g["rho"] for g in GX])
GB = dict(n=len(GX), n_accept=sum(g["src"] == "ACCEPT" for g in GX), n_xcop=sum(g["src"] == "X-COP" for g in GX),
          rho_med=float(np.median(rhos)) if len(rhos) else np.nan, rho_84=float(np.percentile(rhos, 84)) if len(rhos) else np.nan,
          rho_16=float(np.percentile(rhos, 16)) if len(rhos) else np.nan, rho_max=float(rhos.max()) if len(rhos) else np.nan, rows=GX)
GAS_TESTABLE = GB["n"] >= 5
P(f"  gas cross-match eRASS1 vs deprojected: N {GB['n']} (ACCEPT {GB['n_accept']}, X-COP {GB['n_xcop']}); rho median {GB['rho_med']:.3f}, "
  f"16-84% {GB['rho_16']:.3f}-{GB['rho_84']:.3f}, max {GB['rho_max']:.3f} -> {'testable' if GAS_TESTABLE else 'NOT TESTABLE'}")
SL = slacs(); XG = xgass(); BU = budhies_a963()
P(f"  SLACS (N {SL['n']}): alpha_max = 95th pct of 1/Fc = {SL['alpha_max']:.3f} (median 1/Fc {SL['inv_fc_median']:.3f}); Salpeter/Chabrier {SL['salp_over_chab']:.3f}")
P(f"  xGASS log M* >= 11 (N {XG['n']}, {XG['n_limits']} limits): M_HI/M* median {XG['fmed']:.4f}, 95th pct {XG['f95']:.4f}")
P(f"  BUDHIES A963 (supplementary): {BU}")
XC = []
for x in xcop_list():
    if "rs" in x:
        XC.append(dict(name=x["name"], Mstar_ap=m_at(x["rs"], x["ms"], RAP), Mstar_hi_ap=m_at(x["rs"], x["ms_hi"], RAP), Mgas_ap=m_at(x["r"], x["mgas"], RAP)))
for x in XC: x["ratio"] = x["Mstar_ap"] / x["Mgas_ap"]
P("  X-COP measured M*(<0.5 Mpc)/M_gas(<0.5 Mpc) (3D; supplementary): " + ", ".join(f"{x['name']} {x['ratio']:.3f}" for x in XC))
c817 = json.load(open(os.path.join(LANES, "CFG817_erass1_countrate_selection", "cfg817_results_CONDN.json")))["corr_terciles"]
br687 = {f: min(v["MID"][0] for k, v in R7["A"].items() if k.startswith(f + "|")) for f in FEET}

P("\n== Census per cluster (projected R <= 0.5 Mpc)")
for nm, s in SAMPLES.items():
    rS = s["Scen"] / s["gcyl"]; rU = s["Sup"] / s["gcyl"]
    P(f"  {nm}: S_cen median {np.median(s['Scen']):.3e} (BCG {np.median(s['Bcen']):.3e}), S_up median {np.median(s['Sup']):.3e}; gas_cyl median "
      f"{np.median(s['gcyl']):.3e}; S_cen/gas_cyl median {np.median(rS):.3f} [16-84 {np.percentile(rS, 16):.3f}-{np.percentile(rS, 84):.3f}], "
      f"S_up/gas_cyl median {np.median(rU):.3f}; baseline f*=0.20 stars in aperture = 0.20 x gas_cyl; c_cen median {np.median(arr(s['C'], 'c_cen')):.2f}, "
      f"c_up median {np.median(arr(s['C'], 'c_up')):.2f}")
lowz = [c for c, z in zip(CE, ER["z"]) if z < 0.12]
emp = {}
for t in THR:
    num = sum(max(c[f"net_above_{t:.2f}"] - c[f"bcg_above_{t:.2f}"], 0) for c in lowz); den = sum(max(c["net_med"] - c["bcg_med"], 0) for c in lowz)
    x = 10 ** (t - 11.0); emp[t] = dict(F_emp=num / den if den > 0 else np.nan, F_alpha1=math.exp(-x), F_alpha15=float(erfc(math.sqrt(x))))
P(f"  low-z (z<0.12, N {len(lowz)}) empirical member-mass fraction above 10^10.5 / 10^11: " +
  "; ".join(f"{t}: emp {v['F_emp']:.3f} vs alpha=-1 {v['F_alpha1']:.3f}, alpha=-1.5 {v['F_alpha15']:.3f}" for t, v in emp.items()))


def analyse(nm, kern, foot):
    s = SAMPLES[nm]; st = s["st"]; a0 = A0[foot]; nu = KERN[kern]; gas = s["gas"]
    cen = gas + s["stars_cen"]; out = {}
    def band(Mb): return st.band(dsig(Mb, a0, nu))
    out["baseline_f020"] = band(gas * 1.2); out["census_central"] = band(cen)
    rmed = GB["rho_med"] if GAS_TESTABLE else 1.0; rhi = GB["rho_84"] if GAS_TESTABLE else 1.0
    hi_cen = (XG["fmed"] * s["stars_cen"]); hi_up = (XG["f95"] * s["stars_up"])
    out["central_census_full"] = band(rmed * gas + s["stars_cen"] + hi_cen)
    out["corner"] = band(rhi * gas + SL["alpha_max"] * s["stars_up"] + hi_up)
    aB = out["census_central"]["MID"][0]
    knobs = {
        "1a_stars_k_on_Sup": (lambda k: dsig(gas + k * s["stars_up"], a0, nu), 0.0, 1.0, 1.0),
        "4_IMF_alpha_on_Scen": (lambda al: dsig(gas + al * s["stars_cen"], a0, nu), 1.0, 2.0, SL["alpha_max"]),
        "2a_gas_m_whole": (lambda m: dsig(m * gas + s["stars_cen"], a0, nu), 1.0, 2.0, rhi),
        "3a_HI_h_on_f95Sup": (lambda h: dsig(cen + h * hi_up, a0, nu), 0.0, 1.0, 1.0),
        "1b_ICL_k_on_Sup": (lambda k: dsig(cen + (k * s["Sup"] / P100)[:, None] * H100[None, :] * MSUN, a0, nu), 0.0, 1.0, None),
        "3b_H2_k_on_Sup": (lambda k: dsig(cen + (k * s["Sup"] / P15)[:, None] * H15[None, :] * MSUN, a0, nu), 0.0, 1.0, None),
        "U_lambda_conc_on_gascyl": (lambda l: dsig(cen + (l * s["gcyl"] / P15)[:, None] * H15[None, :] * MSUN, a0, nu), 0.0, 1.0, None),
        "1a_stars_k_on_Sup_BCG50": (lambda k: dsig(gas + k * ((s["Bup"][:, None] * H50[None, :] + np.maximum(s["Sup"] - s["Bup"], 0)[:, None] * members_template(gas)) * MSUN), a0, nu), 0.0, 1.0, 1.0),
    }
    core = np.minimum(R, RAP); idx_core = np.searchsorted(R, core)
    knobs["2a_gas_m_core_only"] = (lambda m: dsig(gas + (m - 1) * gas[:, idx_core] * 1.0 + s["stars_cen"], a0, nu), 1.0, 2.0, rhi)
    for kn, (fun, lo, hi, upper) in knobs.items():
        rows = {}
        for tgt in ("A1", "Z2"):
            r = solve(fun, st, lo, hi, target=tgt); v = r["value"]
            row = dict(r)
            if np.isfinite(v):
                b = st.band(fun(v)); row.update(A_MID=b["MID"], A_OUTER=b["OUTER"], Z_OUTER=zsc(b, "OUTER"))
            if upper is not None: row["class"] = cls_mult(v, upper)
            rows[tgt] = row
        rows["upper"] = upper; out[kn] = rows
    # needed masses inside the aperture (median over clusters, Msun)
    def med(x): return float(np.median(x))
    nd = {}
    v = out["1a_stars_k_on_Sup"]["A1"]["value"]; nd["1a"] = dict(needed=med(v * s["Sup"]) if np.isfinite(v) else np.inf, bracket_upper=med(s["Sup"]), measured_central=med(s["Scen"]))
    v = out["4_IMF_alpha_on_Scen"]["A1"]["value"]; nd["4"] = dict(needed_alpha=v, alpha_max=SL["alpha_max"], needed=med(v * s["Scen"]) if np.isfinite(v) else np.inf, bracket_upper=med(SL["alpha_max"] * s["Scen"]))
    v = out["2a_gas_m_whole"]["A1"]["value"]; nd["2a"] = dict(needed_m=v, rho_84=rhi, needed=med(v * s["gcyl"]) if np.isfinite(v) else np.inf, bracket_upper=med(rhi * s["gcyl"]), measured=med(s["gcyl"]))
    v = out["3a_HI_h_on_f95Sup"]["A1"]["value"]; nd["3a"] = dict(needed=med(v * XG["f95"] * s["Sup"]) if np.isfinite(v) else np.inf, bracket_upper=med(XG["f95"] * s["Sup"]))
    for kk, key in (("1b", "1b_ICL_k_on_Sup"), ("3b", "3b_H2_k_on_Sup")):
        v = out[key]["A1"]["value"]; nd[kk] = dict(k=v, needed=med(v * s["Sup"]) if np.isfinite(v) else np.inf, scale_Sup=med(s["Sup"]))
    v = out["U_lambda_conc_on_gascyl"]["A1"]["value"]; nd["U"] = dict(lam=v, needed=med(v * s["gcyl"]) if np.isfinite(v) else np.inf)
    out["needed_masses"] = nd
    # sign-limited knobs (eRASS1 only for hydrostatic / Eddington)
    sign = {}
    if nm == "eRASS1":
        hyd = {}
        for b_ in (0.1, 0.2, 0.3, 0.4):
            g2 = gas_beta(ER["mg"], ER["R500"], rcf=0.15 * (1 - b_) ** (-1 / 3)); s2 = stars_profile(g2, s["Bcen"], s["Scen"]); hyd[b_] = band(g2 + s2)["MID"]
        best = min(v[0] for v in hyd.values()); sign["2c_hydrostatic"] = dict(A_MID_by_b=hyd, best=min(best, aB), cls=cls_sign(aB, min(best, aB)))
        mg = ER["mg"]; q = np.quantile(mg, [0, 1 / 3, 2 / 3, 1]); tid = np.clip(np.digitize(mg, q[1:-1]), 0, 2); corr = np.array(c817)[tid]
        ae = band(corr[:, None] * gas + s["stars_cen"])["MID"]; sign["2e_eddington_CFG817"] = dict(A_MID=ae, cls=cls_sign(aB, min(ae[0], aB)))
        sign["2f_beta_shape_CFG687"] = dict(min_MID_stored=br687[foot], base_stored=R7["A"][f"{foot}|b0.67|rc0.15|f0.20"]["MID"][0],
                                            cls=cls_sign(R7["A"][f"{foot}|b0.67|rc0.15|f0.20"]["MID"][0], br687[foot]))
    ac2 = band(gas / math.sqrt(2.0) + s["stars_cen"])["MID"]
    sign["2d_clumping"] = dict(A_MID_C2=ac2, best_in_bracket=aB, cls=cls_sign(aB, min(aB, ac2[0])))
    sign["2b_xcop_radius_CFG450"] = dict(note="RADIUS is R/R500 (CFG450); CFG686/687 never read X-COP; no lever", cls="CANNOT")
    out["sign_limited"] = sign
    return out


RESULTS = {}
for nm in ("eRASS1", "ACCEPT"):
    for kern in ("s", "mono"):
        for foot in FEET:
            t1 = time.time(); RESULTS[f"{nm}|{kern}|{foot}"] = analyse(nm, kern, foot)
            r = RESULTS[f"{nm}|{kern}|{foot}"]
            P(f"\n== {nm} | nu_{kern} | {foot}  ({time.time() - t1:.0f} s)")
            for lab in ("baseline_f020", "census_central", "central_census_full", "corner"):
                b = r[lab]; P(f"  {lab:20s} MID {b['MID'][0]:.3f}±{b['MID'][1]:.3f} (Z {zsc(b, 'MID'):+.2f})  OUTER {b['OUTER'][0]:.3f}±{b['OUTER'][1]:.3f} (Z {zsc(b, 'OUTER'):+.2f})")
            for kn in [k for k in r if k[0].isdigit() or k.startswith("U_")]:
                a, z2 = r[kn]["A1"], r[kn]["Z2"]
                extra = f" OUTER {a['A_OUTER'][0]:.3f} (Z {a['Z_OUTER']:+.2f})" if "A_OUTER" in a else ""
                P(f"  {kn:26s} needed {a['value']:.4g} [{a['status']}] (lenient Z=2: {z2['value']:.4g}); upper {r[kn]['upper']}; "
                  f"class {a.get('class', 'NOT TESTABLE' if kn[:2] in ('1b', '3b') else '-')} / lenient {z2.get('class', '-')};{extra}")
            for kn, v in r["sign_limited"].items(): P(f"  {kn:26s} {v['cls']}: " + json.dumps({k: v[k] for k in v if k != 'cls'}, default=str)[:220])
            nd = r["needed_masses"]
            P("  needed (median, Msun, R<=0.5 Mpc): " + "; ".join(f"{k}: {json.dumps(v, default=lambda o: round(o, 4) if isinstance(o, float) else str(o))}" for k, v in nd.items()))


# ---- per-component classes and overall (eRASS1, nu_s decides; nu_mono bracket) ----
def component_classes(key):
    r = RESULTS[key]; c = {}
    c["1a BCG+member stars"] = r["1a_stars_k_on_Sup"]["A1"]["class"]
    c["1b ICL"] = "NOT TESTABLE"
    c["2a hot-gas normalisation/shape"] = r["2a_gas_m_whole"]["A1"]["class"] if GAS_TESTABLE else "NOT TESTABLE"
    for k in ("2b_xcop_radius_CFG450", "2c_hydrostatic", "2d_clumping", "2e_eddington_CFG817", "2f_beta_shape_CFG687"):
        if k in r["sign_limited"]: c[k] = r["sign_limited"][k]["cls"]
    c["3a cold atomic gas"] = r["3a_HI_h_on_f95Sup"]["A1"]["class"]
    c["3b cold molecular gas"] = "NOT TESTABLE"
    c["4 stellar M/L, IMF"] = r["4_IMF_alpha_on_Scen"]["A1"]["class"]
    lenient = dict(c); lenient["1a BCG+member stars"] = r["1a_stars_k_on_Sup"]["Z2"]["class"]; lenient["3a cold atomic gas"] = r["3a_HI_h_on_f95Sup"]["Z2"]["class"]
    lenient["4 stellar M/L, IMF"] = r["4_IMF_alpha_on_Scen"]["Z2"]["class"]
    if GAS_TESTABLE: lenient["2a hot-gas normalisation/shape"] = r["2a_gas_m_whole"]["Z2"]["class"]
    return c, lenient


def overall(kern):
    keys = [f"eRASS1|{kern}|{f}" for f in FEET]; per = {}
    for k in keys:
        r = RESULTS[k]; c, _ = component_classes(k); testable = {n: v for n, v in c.items() if v != "NOT TESTABLE"}
        can = []
        for n, v in testable.items():
            if v == "CAN EXPLAIN":
                kn = {"1a BCG+member stars": "1a_stars_k_on_Sup", "2a hot-gas normalisation/shape": "2a_gas_m_whole", "3a cold atomic gas": "3a_HI_h_on_f95Sup",
                      "4 stellar M/L, IMF": "4_IMF_alpha_on_Scen"}.get(n)
                zo = r[kn]["A1"].get("Z_OUTER", 0.0) if kn else 0.0
                if abs(zo) < 2: can.append(n)
        cc = r["central_census_full"]; art = bool(can) or (zsc(cc, "MID") < 2 and abs(zsc(cc, "OUTER")) < 2)
        allcannot = all(v == "CANNOT" for v in testable.values())
        corner_z = zsc(r["corner"], "MID"); kicl = r["1b_ICL_k_on_Sup"]["A1"]["value"]; kh2 = r["3b_H2_k_on_Sup"]["A1"]["value"]
        stands = allcannot and corner_z >= 2 and kicl > 10 and kh2 > 10
        per[k] = dict(artefact=art, can_explain_outer_ok=can, all_testable_cannot=allcannot, corner_Z_MID=corner_z, k_ICL=kicl, k_H2=kh2, stands=stands)
    if all(per[k]["artefact"] for k in keys): o = "ARTEFACT LIKELY"
    elif all(per[k]["stands"] for k in keys): o = "EXCESS STANDS"
    else: o = "NOT DIAGNOSTIC"
    return o, per


OV = {}; CL = {}
for kern in ("s", "mono"):
    OV[kern] = overall(kern)
    for f in FEET: CL[f"eRASS1|{kern}|{f}"] = component_classes(f"eRASS1|{kern}|{f}")
for f in FEET: CL[f"ACCEPT|s|{f}"] = component_classes(f"ACCEPT|s|{f}")
fragile_kernel = OV["s"][0] != OV["mono"][0]
fragile_comp = sorted({n for k, (c, l) in CL.items() if k.startswith("eRASS1|s") for n in c if c[n] != l[n]})
P("\n== Component classes (eRASS1, nu_s; canonical | alt)  [lenient Z_MID=2 in brackets]")
for n in CL["eRASS1|s|canonical"][0]:
    P(f"  {n:34s} {CL['eRASS1|s|canonical'][0][n]:12s} | {CL['eRASS1|s|alt'][0][n]:12s}   [{CL['eRASS1|s|canonical'][1][n]} | {CL['eRASS1|s|alt'][1][n]}]"
      f"   nu_mono: {CL['eRASS1|mono|canonical'][0][n]} | {CL['eRASS1|mono|alt'][0][n]}   ACCEPT nu_s: {CL['ACCEPT|s|canonical'][0].get(n, '-')} | {CL['ACCEPT|s|alt'][0].get(n, '-')}")
P(f"\nOVERALL (eRASS1, nu_s, both footings): {OV['s'][0]}" + ("  [FRAGILE (kernel): nu_mono gives " + OV["mono"][0] + "]" if fragile_kernel else f"  (nu_mono agrees: {OV['mono'][0]})"))
P("  per footing: " + json.dumps({k: {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in OV["s"][1].items()}, default=str))
if fragile_comp: P(f"  components whose class moves under the lenient target: {fragile_comp}")
QX = max(x["Mstar_hi_ap"] / x["Mgas_ap"] for x in XC) if XC else float("nan")
for f in FEET:
    r = RESULTS[f"eRASS1|s|{f}"]; lam = r["U_lambda_conc_on_gascyl"]["A1"]["value"]; rc_ = float(np.median(SAMPLES["eRASS1"]["Scen"] / SAMPLES["eRASS1"]["gcyl"]))
    P(f"  X-COP stellar cross-bracket [{f}] (supplementary): needed stars/gas in the aperture ~ {lam + rc_:.3f} (concentrated) vs X-COP "
      f"max measured M*_hi/M_gas(<0.5 Mpc) {QX:.3f} -> x{(lam + rc_) / QX:.1f}")
P(f"\nDone ({time.time() - T0:.0f} s). kappa = 1/2 FITTED; footings never pooled; cold energy mass still required; not theory closed.")

CENSUS = dict(eRASS1=[dict(c, z=float(ER["z"][i]), gas_cyl=float(SAMPLES["eRASS1"]["gcyl"][i])) for i, c in enumerate(CE)],
              ACCEPT=[dict(c, name=AC[i]["name"], z=float(ACD["z"][i]), gas_cyl=float(SAMPLES["ACCEPT"]["gcyl"][i])) for i, c in enumerate(CA)],
              mlim_table=dict(z=CEN.zg.tolist(), mlim=CEN.ml.tolist()), lowz_empirical=emp)
json.dump(dict(CENSUS, A1=A1INFO), open(os.path.join(HERE, "cfg922_census" + TAG + ".json"), "w"), indent=1, default=float)


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else str(float(o))
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o


json.dump(clean(dict(RES, amendment=AMEND, A1=A1INFO, brackets=dict(gas=GB, slacs=SL, xgass=XG, budhies_a963=BU, xcop_stars=XC, cfg817=c817, cfg687_bracket_minMID=br687),
                     results=RESULTS, classes={k: dict(primary=v[0], lenient=v[1]) for k, v in CL.items()},
                     overall=dict(nu_s=OV["s"][0], nu_mono=OV["mono"][0], per_footing_nu_s=OV["s"][1], per_footing_nu_mono=OV["mono"][1],
                                  fragile_kernel=fragile_kernel, fragile_components=fragile_comp))),
          open(os.path.join(HERE, "cfg922_results" + TAG + ".json"), "w"), indent=1)
