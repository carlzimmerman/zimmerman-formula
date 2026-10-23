#!/usr/bin/env python3
"""CFG967 stage A (criteria FROZEN_CRITERIA.md, 908091f9b; AMENDMENT_A1.md 7a7faac97, d grid aligned on CFG687's edges): the framework's catalogue two-halo term (CFG903 machinery, no free
amplitude) around CFG687's 318 eRASS1 clusters and around 50 random clones per cluster.  No shear and no score here.

Reused read-only:
  CFG903  cfg903_lib.py (imported: pool, N_of_declared, edge_of, d/m binning, watchdog); cfg903_score.py exec'd slices
          (profiles, F2, point_I, kernel, twoh_table, T_at; bin edges replaced by CFG687's 8 bins where stated);
          cfg903_stage_results.json (completeness); ../_external_data/cfg903_work/cfg903_stage.npz (neighbour pool);
          cfg903_hist_bin{1-4}.npz (K2 only); bright-sample RA/Dec/masked (random mask, CFG903's rule).
  CFG686  cfg686_shear.py exec'd slices without the KiDS source columns (CFG949's recipe): BAO-raw DM(z), RGRID, MPC, MSUN.
  CFG687  cfg687_percluster.npz (positions, z, Mgas500, R500).
Output: cfg967_tables.npz (per-cluster two-halo vectors, lens and random means), cfg967_pairs.json, cfg967_pairs.out.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg967_pairs.py
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import contextlib, io, json, math, time, types
import numpy as np
from scipy.spatial import cKDTree
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
D903 = os.path.join(LANES, "CFG903_framework_two_halo_kids")
sys.path.insert(0, D903)
import cfg903_lib as L                                                        # noqa: E402
L.LIM_RSS, L.LIM_T = 0.95e9, 45 * 60                                          # criteria section 9: stop at 0.95 GB current RSS
L.start_watchdog("CFG967 pairs")
OUT, CHK = [], {}
def P(s=""):
    s = f"[{time.time() - L.T0:7.1f} s, {L.cur_rss() / 1e6:5.0f} MB] {s}"; print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
FOOTS = ("canonical", "alt")
NR_PER = 50                                                                   # random clones per cluster (criteria)
FSTAR = 0.20

# ============================================================== CFG686 distances / grid (CFG949's exec recipe, no KiDS sources)
sys.path.insert(0, LANES)
os.environ.pop("MUTATE", None)
SRC686 = os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py"); TXT686 = open(SRC686).read()
NS6 = {"__file__": SRC686, "__name__": "cfg686"}
_argv = sys.argv; sys.argv = [SRC686, "UNUSED"]
with contextlib.redirect_stdout(io.StringIO()) as _buf:
    exec(TXT686.split("# ---- sources ----")[0], NS6)
    NS6["EDGES"] = np.logspace(np.log10(0.15), np.log10(3.0), 9); NS6["RC"] = np.sqrt(NS6["EDGES"][1:] * NS6["EDGES"][:-1]); NS6["M_BIAS"] = -0.01
    exec(TXT686.split("# ---- the law's prediction from ACCEPT gas ----")[1].split("# ---- measure ----")[0], NS6)
sys.argv = _argv
DM, RGRID, MPC, MSUN = NS6["DM"], NS6["RGRID"], NS6["MPC"], NS6["MSUN"]
EDGES687 = NS6["EDGES"]
P(f"CFG967 stage A; CFG686 slices exec'd (no KiDS sources): {_buf.getvalue().strip().splitlines()[-1]}")

# ============================================================== clusters (CFG687 per-cluster file)
PC = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
RA, DEC, ZC, MG, R500 = (np.asarray(PC[k], float) for k in ("ra", "dec", "z", "mg", "R500"))
NCL = len(ZC)
DA = DM(ZC) / (1 + ZC)                                                        # CFG687's BAO-raw D_A (Mpc), the shear bins' radius scale
CHI = L.DC(ZC)                                                                # CFG903's chi (window only, as the stored neighbour chi)
def mgas_model_total(m500, r500, beta=2 / 3, rcf=0.15):
    """total gas of CFG687's primary model (beta-model cut at 3 Mpc, normalised to Mgas500 inside R500): law() algebra, copied."""
    r = RGRID; rc = rcf * r500; shape = (1 + (r / rc) ** 2) ** (-1.5 * beta); shape[r > 3.0] = 0
    dm = 4 * np.pi * (r * MPC) ** 2 * shape; M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * MPC))]
    return float(M[-1] * (m500 * MSUN / np.interp(r500, r, M)) / MSUN)
MB_X1 = np.array([(1 + FSTAR) * mgas_model_total(m, r) for m, r in zip(MG, R500)])   # criteria X1: (1+f*) Mgas(<3 Mpc)
MB_X2 = (1 + FSTAR) * MG                                                              # criteria X2: (1+f*) Mgas500
N_X1 = np.array([L.N_of_declared(math.log10(m)) for m in MB_X1]); N_X2 = np.array([L.N_of_declared(math.log10(m)) for m in MB_X2])
RX = {}
for foot in FOOTS:
    a0 = L.a0_kms2pc(foot)
    RX[(foot, "X1")] = np.array([L.edge_of(n) * math.sqrt(L.Gpc * m / a0) / 1e6 for n, m in zip(N_X1, MB_X1)])
    RX[(foot, "X2")] = np.array([L.edge_of(n) * math.sqrt(L.Gpc * m / a0) / 1e6 for n, m in zip(N_X2, MB_X2)])
    RX[(foot, "X3")] = np.full(NCL, 3.0)
P(f"clusters {NCL}; z {ZC.min():.3f}-{ZC.max():.3f}; Mgas500 median {np.median(MG):.3e}; M_b,cl X1/X2 median {np.median(MB_X1):.3e} / {np.median(MB_X2):.3e}")
P(f"  N_cl X1 {N_X1.min():.2f}-{N_X1.max():.2f}, X2 {N_X2.min():.2f}-{N_X2.max():.2f}")
for foot in FOOTS:
    P(f"  r_x {foot}: X1 median {np.median(RX[(foot, 'X1')]):.2f} Mpc ({RX[(foot, 'X1')].min():.2f}-{RX[(foot, 'X1')].max():.2f}), "
      f"X2 median {np.median(RX[(foot, 'X2')]):.2f} ({RX[(foot, 'X2')].min():.2f}-{RX[(foot, 'X2')].max():.2f})")

# ============================================================== completeness (CFG903 A1, rebuilt from its stage JSON)
SJ = json.load(open(os.path.join(D903, "cfg903_stage_results.json")))["completeness"]
Z0, MLIM, ME = np.array(SJ["Z0"]), np.array(SJ["mlim"]), np.array(SJ["ME"])
rho = np.array([np.nan if x is None else x for x in SJ["rho_tot"]]); m_f = float(SJ["m_f"])
keep = np.isfinite(rho); CUM = np.concatenate([[0.0], np.cumsum(np.where(keep, rho, 0.0) * 0.1)]); CT = float(CUM[-1])
def Ccum(m): return np.interp(m, ME, CUM)
def f_C1(ml):
    ml = np.asarray(ml, float); num = Ccum(ml) - Ccum(m_f); den = Ccum(ml + 0.5) - Ccum(ml)
    return np.where(ml > m_f, num / np.maximum(den, 1e-300), 0.0)
def R_C2(ml):
    ml = np.asarray(ml, float); return (CT - Ccum(m_f)) / (CT - Ccum(np.maximum(ml, m_f)))
S = np.load(os.path.join(L.WORK, "cfg903_stage.npz"))
lz, lf, lr = S["L_z"][:5000], S["L_fC1"][:5000], S["L_RcC2"][:5000]
k0 = max(float(np.max(np.abs(f_C1(np.interp(lz, Z0, MLIM)) - lf))), float(np.max(np.abs(R_C2(np.interp(lz, Z0, MLIM)) - lr))),
         float(np.max(np.abs(f_C1(MLIM) - np.array(SJ["f_C1"])))), float(np.max(np.abs(R_C2(MLIM) - np.array(SJ["R_C2"])))))
check("K0 completeness functions rebuilt from CFG903's stage JSON reproduce its stored per-lens f_C1'/R_C2' (5000 lenses) and grids", k0 <= 1e-12, f"max |d| {k0:.1e}")
MLC = np.interp(ZC, Z0, MLIM); FC1 = f_C1(MLC); RC2 = R_C2(MLC)
P(f"  clusters: m_lim {MLC.min():.2f}-{MLC.max():.2f}; f_C1' {FC1.min():.3f}-{FC1.max():.3f}; R_C2' {RC2.min():.3f}-{RC2.max():.3f}")

# ============================================================== neighbour pool (CFG903 stage A arrays)
NBx = np.asarray(S["NB_xyz"], float); NBchi = np.asarray(S["NB_chi"], float); NBlb = np.asarray(S["NB_logMb"], float)
NBls = np.asarray(S["NB_logMs"], float); NBm = np.asarray(S["NB_masked"]).astype(np.int64)
del S, lz, lf, lr
NBMb = 10 ** NBlb; NBmb = L.mbin_of(NBlb)
treeNB = cKDTree(NBx)
P(f"neighbour pool {len(NBlb):,} (masked = 1: {int((NBm == 1).sum()):,}); max log M_b {NBlb.max():.2f}; tree built")

# ============================================================== randoms (CFG903 stage A rule, seed 967)
from astropy.io import fits                                                   # noqa: E402
HB = fits.open(os.path.join(L.DATA, "KiDS_DR4_brightsample.fits"), memmap=True); b = HB[1].data
ra = np.array(b["RAJ2000"], dtype="f8"); dec = np.array(b["DECJ2000"], dtype="f8"); masked = np.array(b["masked"]).astype(np.int64)
del b; HB.close()
xyzA = L.unitvec(ra, dec); treeA = cKDTree(xyzA)
rng = np.random.default_rng(967)
south = dec < -15.0
boxes = []
for m in (~south, south):                                                     # CFG903 stage A, verbatim
    rau = np.where(dec[m] < -15.0, (ra[m] + 180.0) % 360.0, ra[m])
    lo, hi = float(rau.min()), float(rau.max()); dlo, dhi = float(dec[m].min()), float(dec[m].max())
    area = np.radians(hi - lo) * (math.sin(math.radians(dhi)) - math.sin(math.radians(dlo)))
    boxes.append((lo, hi, dlo, dhi, area))
pbox = np.array([bx[4] for bx in boxes]); pbox /= pbox.sum()
TH = math.radians(4.0 / 60.0); CHR = 2 * math.sin(TH / 2)
NRT = NCL * NR_PER
acc_ra, acc_dec = [], []; ntry = 0; nacc = 0
while nacc < NRT:
    n = 100000; ntry += n
    fb = rng.random(n) < pbox[1]
    rr = np.empty(n); dd = np.empty(n)
    for q, bx in enumerate(boxes):
        mm = fb if q == 1 else ~fb
        lo, hi, dlo, dhi = bx[:4]
        rau = lo + (hi - lo) * rng.random(mm.sum())
        sd = math.sin(math.radians(dlo)) + (math.sin(math.radians(dhi)) - math.sin(math.radians(dlo))) * rng.random(mm.sum())
        rr[mm] = (rau - 180.0) % 360.0 if q == 1 else rau
        dd[mm] = np.degrees(np.arcsin(sd))
    dist, nn = treeA.query(L.unitvec(rr, dd), k=1)
    ok = (dist < CHR) & (masked[nn] == 0)
    acc_ra.append(rr[ok]); acc_dec.append(dd[ok]); nacc += int(ok.sum())
RRA = np.concatenate(acc_ra)[:NRT].reshape(NCL, NR_PER); RDE = np.concatenate(acc_dec)[:NRT].reshape(NCL, NR_PER)
del treeA, xyzA, ra, dec, masked
P(f"randoms: {NRT:,} accepted of {ntry:,} drawn (acceptance {nacc / ntry:.3f}; CFG903 had {json.load(open(os.path.join(D903, 'cfg903_stage_results.json')))['random_acceptance']:.3f}); clone c of cluster i = row i")

# ============================================================== CFG903 kernel code, exec'd read-only
SRC903 = os.path.join(D903, "cfg903_score.py"); TXT = open(SRC903).read()
def sl(a, b):
    i = TXT.index(a); j = TXT.index(b, i); return TXT[i:j]
BASE = dict(np=np, math=math, quad=quad, L=L, time=time)
NSK = dict(BASE)
exec(sl("rho3 = lambda", "t0 = time.time()"), NSK)                            # rho3, QG, sigma_profile, prof, F2, brute
exec(sl("PROFS = {}", 'P(f"\\n  neighbour profiles'), NSK)                     # PROFS for NGRID_NB x (P1, P2), verbatim loop
P(f"neighbour profiles: {len(NSK['PROFS'])} (CFG903 exec'd)")
KSLICE = sl("RB = L.B21_EDGES; NBIN = 15", "# K2c: synthetic uniform field")
DSLICE = sl("SH = (L.ND, L.NM, 2, L.NW, 2)", "VMAP = {")
NSB = dict(NSK); exec(KSLICE, NSB); exec(DSLICE, NSB)                         # B21 edges (K2)
# AMENDMENT A1: this lane's d grid, aligned on CFG687's edges (log bins of log10(20)/128 dex), substituted in the L the code sees
LA = types.SimpleNamespace(**{k: getattr(L, k) for k in dir(L) if not k.startswith("__")})
DELTA = math.log10(20.0) / 128
LA.D_EDGES = np.concatenate([[0.0], 0.15 * 10 ** (DELTA * np.arange(-167, 148))])
LA.ND = len(LA.D_EDGES) - 1; LA.D_MAX = float(LA.D_EDGES[-1])
def dbin_A(d):
    jj = np.floor(np.log10(np.maximum(d, 1e-12) / 0.15) / DELTA).astype(np.int64)
    return np.where(d < LA.D_EDGES[1], 0, jj + 168)
LA.dbin_of = dbin_A
assert LA.ND == 315 and np.allclose(LA.D_EDGES[168 + 16 * np.arange(9)], EDGES687, rtol=1e-12, atol=0)
_tst = np.sqrt(LA.D_EDGES[1:-1] * LA.D_EDGES[2:]); assert np.array_equal(dbin_A(_tst), np.arange(1, LA.ND))
P(f"A1 d grid: {LA.ND} bins, edges {LA.D_EDGES[1]:.5f}-{LA.D_MAX:.3f} Mpc, CFG687's 9 edges on bin edges; neighbour cut d < {L.D_MAX:.2f} Mpc")
NS8 = dict(NSK); NS8["L"] = LA
A1, B1 = "RB = L.B21_EDGES; NBIN = 15", "RB = EDGES687; NBIN = 8"
A2, B2 = "(L.D_EDGES <= 3.0)", "(L.D_EDGES <= 4.69)"
assert KSLICE.count(A1) == 1 and DSLICE.count(A2) == 1
NS8["EDGES687"] = EDGES687
exec(KSLICE.replace(A1, B1), NS8); exec(DSLICE.replace(A2, B2), NS8)          # CFG687's 8 bins; exclusion radii on d-bin edges to 4.61 Mpc
F2, PROFS = NSK["F2"], NSK["PROFS"]

# K3 (a): CFG903's K2b limits on F2
lim = 0.0
for N in (1.0, 10.0):
    pr = PROFS[(N, "P1")]
    for xi in (1.0, 3.0, 100.0, 1e4):
        lim = max(lim, abs(float(F2(pr, xi, xi - 1.0)) - 1), abs(float(F2(pr, xi, xi + 1.0))))
check("K3a CFG903 K2b kernel limits (F = 1 inside, 0 outside)", lim <= 1e-6, f"max |d| {lim:.1e} (<= 1e-6)")

# kernels at CFG687's 8 bins: footing x shape (P0 analytic, P1, P2)
K8 = {}
for foot in FOOTS:
    for shape in ("P1", "P0", "P2"):
        t0 = time.time(); K8[(foot, shape)] = NS8["kernel"](foot, shape); P(f"  kernel 8-bin {foot} {shape}: {time.time() - t0:.0f} s")
# K3 (b): uniform neighbour field -> Delta Sigma = 0 at CFG687's bins
k3b = 0.0
ann = math.pi * (LA.D_EDGES[1:] ** 2 - LA.D_EDGES[:-1] ** 2) * 1e12
for foot in FOOTS:
    for lm in (10.5, 12.0):
        c = int(L.mbin_of(np.array([lm]))[0]); dsig = ann @ K8[(foot, "P1")][c]; tot = 1 + L.SUP * L.N_of_declared(L.M_CEN[c])
        k3b = max(k3b, float(np.max(np.abs(dsig))) / tot)
kfin = all(bool(np.all(np.isfinite(v))) for v in K8.values())
check("K3c every 8-bin kernel entry is finite (A1)", kfin, f"{len(K8)} kernels, shape {next(iter(K8.values())).shape}")
check("K3b uniform neighbour field gives Delta Sigma = 0 in CFG687's 8 bins (log M_b 10.5, 12.0; P1; both footings)", k3b <= 2e-3, f"max |DS| / Sigma0 = {k3b:.1e} (<= 2e-3)")

# ============================================================== K2: CFG903's stored two-halo vectors from its own histograms
R903 = json.load(open(os.path.join(D903, "cfg903_results.json")))
k2 = 0.0
KB = {foot: NSB["kernel"](foot, "P1") for foot in FOOTS}
for bb in range(4):
    h = np.load(os.path.join(L.WORK, f"cfg903_hist_bin{bb + 1}.npz"))
    HLb, HRb, NORMb = h["HL"], h["HR"], h["NORM"]
    Dd = (NSB["_sel"](HLb, 0, 500, "M0") - NSB["_sel"](HRb, 0, 500, "M0")) / float(NORMb[0])
    for foot in FOOTS:
        ref = R903["footings"][foot]
        Tall, Tex = NSB["twoh_table"](Dd, KB[foot], "E1")
        T = NSB["T_at"](Tex, ref["primary"]["score"]["all"]["rx_Mpc"][bb])
        k2 = max(k2, float(np.max(np.abs(T - np.array(ref["T2h_primary"][bb])))))
    del h, HLb, HRb, Dd
del KB
check("K2 CFG903's stored T2h_primary (both footings, 4 bins x 15) reproduced from its histograms via the exec'd kernel/exclusion code",
      k2 <= 1e-9, f"max |d| {k2:.1e} Msun/pc^2 (<= 1e-9)")

# ============================================================== pairs, cluster by cluster (lens + its 50 clones)
NM, ND = L.NM, LA.ND
NC3 = ND * NM * 3                                    # cell = (d bin, m bin, mass class): 0 >= M_X1; 1 in [M_X2, M_X1); 2 < M_X2
VAR = ["V0", "V1", "V2", "V3", "V4"]                 # V0 primary C1' W500 M0; V1 C0; V2 W300; V3 W1000; V4 M1 (masked added)
COMBOS = [("V0", "P1"), ("V0", "P0"), ("V0", "P2"), ("V1", "P1"), ("V2", "P1"), ("V3", "P1"), ("V4", "P1")]
KT = {k: np.ascontiguousarray(v.transpose(1, 0, 2)) for k, v in K8.items()}  # (d, m, 8)
del K8
EIDX8, T_at8 = NS8["EIDX"], NS8["T_at"]
NB8 = 8
def G3_of(H, foot, shape):
    return np.matmul(H.reshape(ND, NM, 3).transpose(0, 2, 1), KT[(foot, shape)])     # (d, class, 8)
def T_from_G(G3, rx, mode):
    """CFG903 twoh_table/T_at algebra on a 3-class G: cells with d < r_x dropped for neighbours less massive than the cluster
    (classes 1+2 for M_X1, class 2 for M_X2); E0 none."""
    Tall = G3.sum(axis=(0, 1))
    if mode == "E0": return Tall
    Gx = G3[:, 1:, :].sum(axis=1) if mode == "X1" else G3[:, 2, :]
    cum = np.concatenate([np.zeros((1, NB8)), np.cumsum(Gx, axis=0)])
    return T_at8(Tall[None, :] - cum[EIDX8], rx)
KEYS = []
for foot in FOOTS:
    KEYS += [f"{foot}|V0P1X1", f"{foot}|V0P1X2", f"{foot}|V0P1X3", f"{foot}|V0P1E0", f"{foot}|V0P0X1", f"{foot}|V0P2X1",
             f"{foot}|V1P1X1", f"{foot}|V2P1X1", f"{foot}|V3P1X1", f"{foot}|V4P1X1", f"{foot}|V0P1host"]
TL = {k: np.zeros((NCL, NB8)) for k in KEYS}; TR = {k: np.zeros((NCL, NB8)) for k in KEYS}
TRA = {f: np.zeros((NCL, NB8)) for f in FOOTS}; TRB = {f: np.zeros((NCL, NB8)) for f in FOOTS}
NPAIR_L = np.zeros(NCL, np.int64); NPAIR_R = np.zeros(NCL, np.int64)
def tables(H, i):
    """H: dict variant -> (NC3,) histogram; returns dict key -> 8-vector for cluster i."""
    out = {}
    for foot in FOOTS:
        for v, shape in COMBOS:
            G3 = G3_of(H[v], foot, shape)
            if (v, shape) == ("V0", "P1"):
                for X in ("X1", "X2", "X3"):
                    out[f"{foot}|V0P1{X}"] = T_from_G(G3, RX[(foot, X)][i], "X2" if X == "X2" else "X1")
                out[f"{foot}|V0P1E0"] = T_from_G(G3, 0.0, "E0")
                out[f"{foot}|V0P1host"] = G3[:, 0, :].sum(axis=0)
            else:
                out[f"{foot}|{v}{shape}X1"] = T_from_G(G3, RX[(foot, "X1")][i], "X1")
    return out
def histos(xyz, i, halves=False):
    """pairs of objects (rows of xyz) around cluster i's redshift -> per-variant histograms (summed over objects)."""
    chmax = 2 * np.sin(L.D_MAX / DA[i] / 2)
    lists = treeNB.query_ball_point(xyz, r=chmax)
    cnt = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists))
    k = np.repeat(np.arange(len(lists)), cnt)
    j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=int(cnt.sum()))
    del lists
    dchi = np.abs(NBchi[j] - CHI[i]); m = dchi < 1000.0
    k, j, dchi = k[m], j[m], dchi[m]
    ch = np.linalg.norm(NBx[j] - xyz[k], axis=1); d = 2 * np.arcsin(np.minimum(ch / 2, 1.0)) * DA[i]
    m = d < L.D_MAX; k, j, dchi, d = k[m], j[m], dchi[m], d[m]
    db = LA.dbin_of(d); mb = NBmb[j]; Mb = NBMb[j]
    cls = np.where(Mb >= MB_X1[i], 0, np.where(Mb >= MB_X2[i], 1, 2))
    cell = (db * NM + mb) * 3 + cls
    wb = np.searchsorted(L.WEDGES[:4], dchi, side="right"); mk = NBm[j]
    inwin = (NBls[j] >= MLC[i]) & (NBls[j] < MLC[i] + 0.5); c1w = 1.0 + FC1[i] * inwin
    sel = {"V0": (wb <= 3) & (mk == 0), "V1": (wb <= 3) & (mk == 0), "V2": (wb <= 2) & (mk == 0), "V3": (mk == 0), "V4": (wb <= 3)}
    wts = {"V0": Mb * c1w, "V1": Mb, "V2": Mb * c1w, "V3": Mb * c1w, "V4": Mb * c1w}
    H = {v: np.bincount(cell[sel[v]], weights=wts[v][sel[v]], minlength=NC3) for v in VAR}
    HA = HB_ = None
    if halves:
        a = (k % 2 == 0)
        s0 = sel["V0"]
        HA = np.bincount(cell[s0 & a], weights=wts["V0"][s0 & a], minlength=NC3)
        HB_ = np.bincount(cell[s0 & ~a], weights=wts["V0"][s0 & ~a], minlength=NC3)
    return H, HA, HB_, int(len(j))
# internal check: the G route equals CFG903's verbatim twoh_table on the same histogram (cluster 0, canonical, X1)
t0 = time.time()
for i in range(NCL):
    H, _, _, npl = histos(L.unitvec(RA[i:i + 1], DEC[i:i + 1]), i)
    HR, HA, HB_, npr = histos(L.unitvec(RRA[i], RDE[i]), i, halves=True)
    HR = {v: HR[v] / NR_PER for v in VAR}
    tl, tr = tables(H, i), tables(HR, i)
    for kk in KEYS:
        TL[kk][i] = tl[kk]; TR[kk][i] = tr[kk]
    for foot in FOOTS:
        TRA[foot][i] = T_from_G(G3_of(HA / (NR_PER // 2), foot, "P1"), RX[(foot, "X1")][i], "X1")
        TRB[foot][i] = T_from_G(G3_of(HB_ / (NR_PER - NR_PER // 2), foot, "P1"), RX[(foot, "X1")][i], "X1")
    if i == 0:
        D2 = np.stack([H["V0"].reshape(ND, NM, 3)[:, :, 0], H["V0"].reshape(ND, NM, 3)[:, :, 1:].sum(-1)], axis=-1)
        Kc = np.ascontiguousarray(KT[("canonical", "P1")].transpose(1, 0, 2))
        _, Tex = NS8["twoh_table"](D2, Kc, "E1"); Tv = NS8["T_at"](Tex, RX[("canonical", "X1")][0]); del Kc
        kg = float(np.max(np.abs(Tv - tl["canonical|V0P1X1"])) / max(1e-30, float(np.max(np.abs(Tv)))))
        check("K2x this lane's G route equals CFG903's verbatim twoh_table/T_at on the same histogram (cluster 0, canonical, X1)", kg <= 1e-10, f"max rel |d| {kg:.1e}")
    NPAIR_L[i] = npl; NPAIR_R[i] = npr
    if i % 40 == 0 or i == NCL - 1:
        P(f"  cluster {i + 1}/{NCL}: z {ZC[i]:.3f}, pairs lens {npl:,}, clones {npr:,} ({time.time() - t0:.0f} s)")

# ============================================================== save
np.savez_compressed(os.path.join(HERE, "cfg967_tables.npz"),
                    **{"L_" + k: v for k, v in TL.items()}, **{"R_" + k: v for k, v in TR.items()},
                    **{"RA_" + f: TRA[f] for f in FOOTS}, **{"RB_" + f: TRB[f] for f in FOOTS},
                    **{f"RX_{f}_{X}": RX[(f, X)] for f in FOOTS for X in ("X1", "X2", "X3")},
                    MB_X1=MB_X1, MB_X2=MB_X2, N_X1=N_X1, N_X2=N_X2, MLC=MLC, FC1=FC1, RC2=RC2, NPAIR_L=NPAIR_L, NPAIR_R=NPAIR_R,
                    rand_ra=RRA, rand_dec=RDE, EDGES687=EDGES687)
RES = dict(lane="CFG967", stage="A", criteria="908091f9b", amendments=["7a7faac97"], d_grid_bins=int(LA.ND), n_clusters=int(NCL), clones_per_cluster=NR_PER, random_acceptance=nacc / ntry,
           checks=CHK, K2_maxdiff=k2, K3a=lim, K3b=k3b, K0=k0,
           rx_median={f"{f}|{X}": float(np.median(RX[(f, X)])) for f in FOOTS for X in ("X1", "X2")},
           pairs_lens_median=int(np.median(NPAIR_L)), pairs_clones_median=int(np.median(NPAIR_R)),
           runtime_s=round(time.time() - L.T0, 1), peak_current_rss_MB=round(L.PEAK_CUR[0] / 1e6, 1))
json.dump(RES, open(os.path.join(HERE, "cfg967_pairs.json"), "w"), indent=1)
P(f"saved cfg967_tables.npz; checks {sum(CHK.values())}/{len(CHK)} PASS; runtime {time.time() - L.T0:.0f} s; peak current RSS {L.PEAK_CUR[0] / 1e6:.0f} MB")
open(os.path.join(HERE, "cfg967_pairs.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
