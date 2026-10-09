#!/usr/bin/env python3
"""CFG506 per-box pass (FROZEN_CRITERIA.md sections 2-6, 10, 11; criteria commit 27a6c64ee). One particle load per box.

1. lensing source of the zero-knob model: CIC particle contrast + S = e - comp (the CFG424 engine's RES / RC = 0 source, recomputed at z = 0
   with the engine's own functions, imported read-only; sources() copied from CFG495's cfg495_sim.py), K1 / K2 checks;
2. CFG504's halo finder (copied from cfg504_pm.py; thresholds 11.5 / 11.8, disclosed in the criteria);
3. galaxies: joint abundance matching of the box's halos to the GAMA SMF (Baldry+12, (U)), CFG502 satellite occupation on host particles;
4. KiDS isolation emulation per axis and z node with the measured close-pair kernel; companion counts;
5. DeltaSigma of the lensing field around every lens (Fourier disc filters on fine 2D maps), centrals' own r_ta sphere removed;
   shuffled-centre twin (MUTATE SHUF) in the same pass; 27-subvolume jackknife sums;
6. diagnostics: settled / unsettled slabs, catchment q, concentration proxy, 3D stacked profiles, catalogue for the HMF.
Usage: nice -n 15 python3 -u cfg506_box.py KEY      (KEY in BOXES)
Writes ../../../_external_data/cfg506_work/cfg506_box_KEY.npz and updates cfg506_box_results.json / cfg506_box.out in this folder.
"""
import os, sys
os.environ.setdefault("CFG424_THREADS", "4")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = os.environ["CFG424_THREADS"]
import json, math, time, subprocess, importlib.util
import numpy as np
from scipy import fft as sfft
from scipy.ndimage import maximum_filter
from scipy.spatial import cKDTree
from scipy.special import j1
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg506_work"); os.makedirs(WORK, exist_ok=True)
W424 = "cfg424_work/cfg424_RES_TA_MIXA_MASSCONS_fret1_"
BOXES = {  # key: (snapshot base relative to _external_data, kind, branch, foot, N)
    "TA512_can359": (W424 + "FLAT_canonical_N512", "TA", "FLAT", "canonical", 512),
    "TA512_can360": (W424 + "FLAT_canonical_N512_seed360", "TA", "FLAT", "canonical", 512),
    "TA512_alt359": (W424 + "FLAT_alt_N512", "TA", "FLAT", "alt", 512),
    "TA512_DEcan359": (W424 + "DE_canonical_N512", "TA", "DE", "canonical", 512),
    "S0512_359": ("cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512", "S0", "FLAT", "canonical", 512),
    "S0512_360": ("cfg424_work/cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360", "S0", "FLAT", "canonical", 512),
    "TA256_can359": (W424 + "FLAT_canonical_N256", "TA", "FLAT", "canonical", 256),
    "TA256_can360": (W424 + "FLAT_canonical_N256_seed360", "TA", "FLAT", "canonical", 256),
    "TA256_can361": (W424 + "FLAT_canonical_N256_seed361", "TA", "FLAT", "canonical", 256),
    "TA256_alt359": (W424 + "FLAT_alt_N256", "TA", "FLAT", "alt", 256),
    "TA256_alt360": (W424 + "FLAT_alt_N256_seed360", "TA", "FLAT", "alt", 256),
    "TA256_alt361": (W424 + "FLAT_alt_N256_seed361", "TA", "FLAT", "alt", 256),
    "TA256_DEcan359": (W424 + "DE_canonical_N256", "TA", "DE", "canonical", 256),
    "TA256_DEalt359": (W424 + "DE_alt_N256", "TA", "DE", "alt", 256),
    "S0256_359": ("cfg359_work/cfg359_S0_FLAT_canonical_N256", "S0", "FLAT", "canonical", 256),
    "S0256_360": ("cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360", "S0", "FLAT", "canonical", 256),
    "S0256_361": ("cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed361", "S0", "FLAT", "canonical", 256),
}
KEY = sys.argv[1]
BASE, KIND, BRANCH, FOOT, N = BOXES[KEY]
T0 = time.time()
LOG = []
CHK = {}


def say(s):
    s = f"[{KEY} {time.time() - T0:7.1f}s] {s}"; print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


# ---------------------------------------------------------------- one 512^3 load at a time
def others_512():
    pats = ["N512|512 0 MIXA|cfg4[0-9][0-9]_pm.py .* 512", "cfg504_pm.py", "cfg495_sim.py N512", "cfg506_box.py .*512"]
    me = {os.getpid(), os.getppid()}
    out = set()
    for p in pats:
        r = subprocess.run(["pgrep", "-f", p], capture_output=True, text=True)
        out |= {int(x) for x in r.stdout.split() if x.strip()}
    return sorted(out - me)


if N >= 512:
    while True:
        o = others_512()
        if not o:
            break
        say(f"waiting: other 512^3 job(s) running {o}")
        time.sleep(60)

# ---------------------------------------------------------------- engine (read-only)
spec = importlib.util.spec_from_file_location("eng424", os.path.join(LANES, "CFG424_turnaround_catchment", "cfg424_pm.py"))
eng = importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)
eng.RC = 0.0; eng.MIX = "MIXA"
Om, FB, L = eng.Om, eng.FB, eng.L
h = 0.6736
RHOM_H = Om * 2.77536627e11                    # (Msun/h) / (Mpc/h)^3 comoving mean matter (CFG504's constant with the engine's Om)
J = json.load(open(os.path.join(EXT, BASE + ".json")))
assert int(J["mesh"]) == N and abs(float(J["L"]) - L) < 1e-9
DTA = float(J["snap"]["z0"]["Delta_ta"])
mesh = eng.Mesh(N); dx = mesh.dx
A = 1.0
say(f"{BASE.split('/')[-1]}: kind {KIND}, branch {BRANCH}, foot {FOOT}, N {N}, dx {dx:.4f} Mpc/h, Delta_ta {DTA:.4f}")


def sources(delta):
    """CFG495's copy of the engine's RES / RC = 0 branch at a = 1 (diag path). Returns e, comp, fsw, edge, catch labels, q."""
    a = A
    dk = mesh.fwd(delta)
    phik = (-1.5 * Om / a) * dk * mesh.ik2
    tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    t = [mesh.inv(mesh.kvec[i] * mesh.kvec[j] * dk * mesh.ik2) for i, j in tk]
    _, l2, _ = eng.eig3(t); del t, dk
    tau = (DTA - 1.0) / 3.0
    fsw = np.clip(0.5 + (l2 - tau) / (2 * eng.EPS), 0, 1).astype(np.float32); del l2
    edge = eng.in_cover(mesh, delta, DTA, None, a, BRANCH, FOOT)
    catch = eng.in_cover(mesh, delta, DTA, 1.0, a, BRANCH, FOOT)
    fsw *= edge.astype(np.float32)
    fc, fh, fs = eng.MIXES["MIXA"]; kk = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
    kJ = lambda T: math.sqrt(1.5 * Om / a) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    Wk = (fc / (1.0 + kk / kJ(1e4) ** 2) + fh / (1.0 + kk / kJ(1e6) ** 2) + fs).astype(np.float32); del kk
    gb = [FB * (-mesh.inv(1j * kv * phik * Wk)) for kv in mesh.kvec]; del Wk, phik
    y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (a * eng.a0_code(a, BRANCH, FOOT))
    w = (eng.nu_mono(y) - 1.0).astype(np.float32); del y
    divk = sum(1j * kv * mesh.fwd(w * g) for kv, g in zip(mesh.kvec, gb)); del gb, w
    s_ph = -mesh.inv(divk); del divk
    s_c = ((1.5 * Om * (1.0 - FB) / a) * (1.0 + delta)).astype(np.float32)
    e = (fsw * np.maximum(s_ph - s_c, 0.0) * catch).astype(np.float32); del s_ph
    r, nc = eng.catch_labels(catch); mm = r >= 0
    E_ = np.bincount(r[mm], weights=e.ravel()[mm].astype(np.float64), minlength=nc)
    C_ = np.bincount(r[mm], weights=s_c.ravel()[mm].astype(np.float64), minlength=nc)
    q = E_ / np.maximum(C_, 1e-30)
    comp = np.zeros(e.size, np.float32); comp[mm] = (s_c.ravel()[mm] * q[r[mm]]).astype(np.float32); comp = comp.reshape(e.shape)
    w_ = np.bincount(r[mm], weights=(1.0 + delta).ravel()[mm].astype(np.float64), minlength=nc)
    info = dict(q_max=float(q.max()) if nc else 0.0, overdraw_mass=float(w_[q > 1].sum() / max(w_.sum(), 1e-30)),
                src_sum=float((e - comp).sum(dtype=np.float64)), e_sum=float(e.sum(dtype=np.float64)), n_catch=int(nc),
                vol_catch=float(catch.mean()), vol_edge=float(edge.mean()))
    return e, comp, fsw, r.reshape(e.shape), q, w_, E_, info


# ================================================================= 1. particles, delta, lensing source
pos32 = np.load(os.path.join(EXT, BASE + "_z0.npz"))["pos"]
NP = len(pos32); MP = RHOM_H * L ** 3 / NP
say(f"loaded {NP:,} particles, m_p {MP:.4e} Msun/h")
OUT = dict(key=KEY, base=BASE.split("/")[-1], kind=KIND, branch=BRANCH, foot=FOOT, N=N, dx=dx, m_p=MP, Delta_ta=DTA, NP=NP)
SRC = None
D1 = {}
if KIND == "TA":
    delta = mesh.deposit(pos32)
    e, comp, fsw, lab, qC, wC, EC, info = sources(delta)
    js = J["snap"]["z0"]
    dq = abs(info["q_max"] / js["q_max"] - 1)
    check("K1 engine q_max reproduced (1e-4 rel)", dq < 1e-4, f"q_max {info['q_max']:.6f} vs run JSON {js['q_max']:.6f} (rel {dq:.1e})")
    check("K2 per-catchment conservation |sum S| / sum e < 1e-3", abs(info["src_sum"]) < 1e-3 * info["e_sum"],
          f"sum S {info['src_sum']:.3e}, sum e {info['e_sum']:.3e}")
    OUT["source_info"] = info
    k15 = 1.5 * Om
    SRC = ((e - comp) / k15).astype(np.float32)                 # S in density-contrast units
    # D1 slabs (20 Mpc/h along z, centred at L/2) and global fractions
    ns = int(round(20.0 / dx)); z0 = N // 2 - ns // 2
    rho = 1.0 + delta
    cold = (1.0 - FB) * rho
    D1 = dict(settled=(cold * fsw)[:, :, z0:z0 + ns].sum(2), unsettled=(cold * (1 - fsw))[:, :, z0:z0 + ns].sum(2),
              e=(e / k15)[:, :, z0:z0 + ns].sum(2), comp=(comp / k15)[:, :, z0:z0 + ns].sum(2), total=rho[:, :, z0:z0 + ns].sum(2))
    OUT["D1"] = dict(settled_mass_frac=float((cold * fsw).sum(dtype=np.float64) / cold.sum(dtype=np.float64)),
                     edge_vol_frac=info["vol_edge"], catch_vol_frac=info["vol_catch"],
                     e_mass_frac=float((e / k15).sum(dtype=np.float64) / rho.sum(dtype=np.float64)),
                     comp_mass_frac=float((comp / k15).sum(dtype=np.float64) / rho.sum(dtype=np.float64)))
    # D2 catchments: q, mass (Msun/h), label kept for host matching
    D2_q = qC.copy(); D2_M = wC * MP                                    # mass per mesh cell at mean density = m_p (NP = N^3)
    del e, comp, fsw, cold, rho, delta
    say(f"sources done: q_max {info['q_max']:.4f}, catchments {info['n_catch']}, settled mass fraction {OUT['D1']['settled_mass_frac']:.4f}")

# ================================================================= 2. CFG504 finder (copied)
pos = pos32.astype(np.float64) % L
del pos32


def cic3(pos, N, L):                                     # CFG502's CIC (copied via CFG504)
    x = pos / (L / N); i0 = np.floor(x).astype(np.int64); d = x - i0
    rho = np.zeros(N ** 3)
    for dx_ in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (d[:, 0] if dx_ else 1 - d[:, 0]) * (d[:, 1] if dy else 1 - d[:, 1]) * (d[:, 2] if dz else 1 - d[:, 2])
                idx = (((i0[:, 0] + dx_) % N) * N + (i0[:, 1] + dy) % N) * N + (i0[:, 2] + dz) % N
                rho += np.bincount(idx, weights=w, minlength=N ** 3)
    return rho.reshape(N, N, N)


def so_mass(tree, cen, Dta, mp, rg):
    n = len(cen)
    dens = np.full((n, len(rg)), np.nan)
    active = np.arange(n)
    for j, r in enumerate(rg):
        if len(active) == 0:
            break
        c = tree.query_ball_point(cen[active], r, return_length=True, workers=4)
        dens[active, j] = c * mp / (4 * math.pi / 3 * r ** 3) / RHOM_H
        active = active[dens[active, j] >= Dta]
    out = {}
    for lab_, D in (("ta", Dta), ("200m", 200.0)):
        M = np.zeros(n); R = np.zeros(n)
        for i in range(n):
            dd = dens[i]
            ok = np.isfinite(dd)
            if not ok[0] or dd[0] < D:
                continue
            below = np.where(ok & (dd < D))[0]
            if len(below) == 0:
                continue
            j = below[0]
            f = (math.log(dd[j - 1]) - math.log(D)) / (math.log(dd[j - 1]) - math.log(dd[j]))
            R[i] = math.exp(math.log(rg[j - 1]) + f * (math.log(rg[j]) - math.log(rg[j - 1])))
            M[i] = D * RHOM_H * 4 * math.pi / 3 * R[i] ** 3
        out[lab_] = (M, R)
    return out


rho = cic3(pos, N, L); rho /= rho.mean()
pk = (rho == maximum_filter(rho, size=3, mode="wrap")) & (rho > 20.0)
seeds = (np.argwhere(pk) + 0.5) * dx
del rho, pk
tree = cKDTree(pos, boxsize=L, leafsize=32, balanced_tree=False, compact_nodes=False)
rg = np.geomspace(0.5 * dx, 12.0, 50)
so0 = so_mass(tree, seeds, DTA, MP, rg)
cen = seeds[so0["ta"][0] >= 10 ** 11.5]
say(f"seeds {len(seeds)}; pre-screen (log M_ta >= 11.5): {len(cen)}")
for it in range(2):
    lists = tree.query_ball_point(cen, dx, workers=4)
    newc = np.empty_like(cen)
    for i, li in enumerate(lists):
        if len(li) == 0:
            newc[i] = cen[i]; continue
        d = pos[li] - cen[i]; d -= L * np.round(d / L)
        newc[i] = (cen[i] + d.mean(0)) % L
    cen = newc
so = so_mass(tree, cen, DTA, MP, rg)
Mta, rta = so["ta"]; M200m, r200m = so["200m"]
ok = Mta > 0
cen, Mta, rta, M200m, r200m = cen[ok], Mta[ok], rta[ok], M200m[ok], r200m[ok]
o = np.argsort(-Mta); cen, Mta, rta, M200m, r200m = cen[o], Mta[o], rta[o], M200m[o], r200m[o]
keep = np.ones(len(cen), bool); tc = cKDTree(cen, boxsize=L)
for i in range(len(cen)):
    if not keep[i]:
        continue
    for j in tc.query_ball_point(cen[i], rta[i]):
        if j > i:
            keep[j] = False
cen, Mta, rta, M200m, r200m = cen[keep], Mta[keep], rta[keep], M200m[keep], r200m[keep]
m = np.log10(Mta) >= 11.8
cen, Mta, rta, M200m, r200m = cen[m], Mta[m], rta[m], M200m[m], r200m[m]
lM = np.log10(Mta)
MCOMP = 150 * MP
say(f"catalogue: {len(cen)} distinct halos with log M_ta >= 11.8; complete (>= 150 m_p, log {math.log10(MCOMP):.2f}): {(Mta >= MCOMP).sum()}")
OUT["n_halos"] = int(len(cen)); OUT["logM_complete"] = math.log10(MCOMP)
if KEY == "S0512_360":
    f504 = os.path.join(EXT, "cfg504_work", "cfg504_pm_S0_512_b.npz")
    if os.path.exists(f504):
        C4 = np.load(f504)
        s4 = np.log10(C4["Mta"]) >= 12.3; mine = lM >= 12.3
        t4 = cKDTree(C4["cen"][s4], boxsize=L)
        dd, jj = t4.query(cen[mine], distance_upper_bound=dx)
        okm = np.isfinite(dd)
        dl = np.abs(lM[mine][okm] - np.log10(C4["Mta"][s4][jj[okm]]))
        med = float(np.median(dl)) if okm.any() else float("inf")
        check("C10 (reported) finder = CFG504's catalogue on S0 512^3 seed 360 (median |dlogM| < 0.01)", med < 0.01,
              f"{okm.sum()} of {mine.sum()} matched within 1 cell; median |d log M_ta| {med:.2e}", lb=False)

# D3 concentration proxy and 3D stacked profiles of distinct halos
res5 = rta >= 5 * dx
Mhalf = np.zeros(len(cen))
ii = np.where(res5 & (r200m > 0))[0]
if len(ii):
    Mhalf[ii] = tree.query_ball_point(cen[ii], 0.5 * r200m[ii], return_length=True, workers=4) * MP


def mnfw(x): return np.log1p(x) - x / (1 + x)


cprox = np.full(len(cen), np.nan)
for i in ii:
    rr = Mhalf[i] / M200m[i]
    try:
        cprox[i] = brentq(lambda c: mnfw(c / 2) / mnfw(c) - rr, 0.3, 80.0)
    except ValueError:
        pass
PBINS = [(12.0, 12.5), (12.5, 13.0), (13.0, 13.5), (13.5, 14.0), (14.0, 15.2)]
EDGES3 = np.geomspace(0.15, 20.0, 49)
rngp = np.random.default_rng(506)
P3 = np.zeros((len(PBINS), len(EDGES3))); P3n = np.zeros(len(PBINS), int); P3S = np.zeros((len(PBINS), len(EDGES3) - 1))
nb10 = int(math.ceil(10.0 / dx)) + 1; ob = np.arange(-nb10, nb10 + 1)
r3c = np.sqrt(ob[:, None, None] ** 2 + ob[None, :, None] ** 2 + ob[None, None, :] ** 2).ravel() * dx
b3 = np.digitize(r3c, EDGES3) - 1; ok3 = (b3 >= 0) & (b3 < len(EDGES3) - 1); cnt3 = np.bincount(b3[ok3], minlength=len(EDGES3) - 1)
for ib, (a_, b_) in enumerate(PBINS):
    sel = np.where((lM >= a_) & (lM < b_))[0]
    if len(sel) > 200:
        sel = np.sort(rngp.choice(sel, 200, replace=False))
    P3n[ib] = len(sel)
    for i in sel:
        t1 = cKDTree(cen[i][None, :], boxsize=L)
        P3[ib] += t1.count_neighbors(tree, EDGES3)
        if SRC is not None:
            c = np.floor(cen[i] / dx).astype(int)
            sub = SRC[np.ix_((c[0] + ob) % N, (c[1] + ob) % N, (c[2] + ob) % N)].ravel()
            P3S[ib] += np.bincount(b3[ok3], weights=sub[ok3], minlength=len(EDGES3) - 1) / np.maximum(cnt3, 1)
say(f"D3 / 3D profiles done: {len(ii)} halos with r_ta >= 5 cells")

# D2 host matching: each catchment's host = the most massive distinct halo whose centre cell lies in it
if KIND == "TA":
    ci = np.floor(cen / dx).astype(int) % N
    labc = lab[ci[:, 0], ci[:, 1], ci[:, 2]]
    hostM = np.zeros(len(D2_q))
    for i in np.argsort(Mta):                      # ascending, so the most massive wins
        if labc[i] >= 0:
            hostM[labc[i]] = Mta[i]
    OUT["D2_n_catch_with_host"] = int((hostM > 0).sum())
    del lab

# ================================================================= 3. galaxies: joint abundance matching + satellites
LH = 0.6736
def smf_phi(lm):                                   # Baldry+12 (U), per dex, Mpc^-3 (h = 0.7)
    Ms = 10 ** 10.66; x = 10 ** lm / Ms
    return math.log(10) * np.exp(-x) * (3.96e-3 * x ** (-0.35 + 1) + 0.79e-3 * x ** (-1.47 + 1))
LMG = np.linspace(7.0, 12.8, 5801)
_cum = np.concatenate([[0.0], np.cumsum(0.5 * (smf_phi(LMG[1:]) + smf_phi(LMG[:-1])) * np.diff(LMG))])
NCUM = (_cum[-1] - _cum) / 0.7 ** 3               # n(> m) in (Mpc/h)^-3
def n_smf(m): return np.interp(m, LMG, NCUM)
V = L ** 3
MGRID = np.arange(12.2, 8.59, -0.02)
# box HMF: catalogue counts above the completeness mass; below it a power law n(> M) = n(> Mc) (M / Mc)^-s fitted on [Mc, 10 Mc]
# (implementation detail, disclosed in the README: the abundance matching needs n(> M) below completeness for faint neighbours and satellites)
Mcomp_sorted = np.sort(Mta[Mta >= MCOMP])[::-1]
MFIT = np.geomspace(MCOMP, 10 * MCOMP, 11)
NFIT = np.array([np.searchsorted(-Mcomp_sorted, -x) for x in MFIT], float)
okf = NFIT > 10
SLOPE_HMF = -np.polyfit(np.log10(MFIT[okf]), np.log10(NFIT[okf]), 1)[0]
NC_ = np.searchsorted(-Mcomp_sorted, -MCOMP) / V
LMX = np.linspace(7.5, math.log10(MCOMP), 400); MX = 10 ** LMX
DNDM = SLOPE_HMF * NC_ * (MX / MCOMP) ** (-SLOPE_HMF) / MX          # |dn/dM| of the extension


def f_root(lMmin, m):
    Mm = 10 ** lMmin
    if Mm >= MCOMP:
        ncen = np.searchsorted(-Mcomp_sorted, -Mm) / V
    else:
        ncen = NC_ * (Mm / MCOMP) ** (-SLOPE_HMF)
    sel = Mcomp_sorted[Mcomp_sorted > Mm]
    nsat = (sel - Mm).sum() / (17 * Mm) / V
    if Mm < MCOMP:
        u = MX > Mm
        nsat += np.trapz(((MX - Mm) / (17 * Mm) * DNDM)[u], MX[u])
    return ncen + nsat - n_smf(m)


lMmin = np.full(len(MGRID), np.nan)
for k, mm_ in enumerate(MGRID):
    lo, hi = 7.6, 15.8
    if f_root(lo, mm_) < 0 or f_root(hi, mm_) > 0:
        continue
    lMmin[k] = brentq(lambda x: f_root(x, mm_), lo, hi, xtol=1e-5)
okm_ = np.isfinite(lMmin)
valid = okm_ & (lMmin >= math.log10(MCOMP))
if not valid.any():
    raise SystemExit("abundance matching failed")
mlim_box = float(MGRID[valid].min())
vm, vM = MGRID[okm_][::-1], lMmin[okm_][::-1]            # ascending m (whole solved range, extension included)
def ms_of_lM(x): return np.interp(np.asarray(x, float), vM, vm)
def lMmin_of_m(mm_): return np.interp(np.asarray(mm_, float), vm, vM)
rng = np.random.default_rng(506)
lms_c = ms_of_lM(lM) + rng.normal(0, 0.15, len(lM))
say(f"abundance matching: m_lim,box {mlim_box:.2f}; "
    f"log M_min(10.5) {float(lMmin_of_m(10.5)):.2f}, (10.0) {float(lMmin_of_m(10.0)):.2f}, (11.0) {float(lMmin_of_m(11.0)):.2f}")
OUT["sham"] = dict(m_lim_box=mlim_box, MGRID=MGRID[okm_].tolist(), lMmin=lMmin[okm_].tolist(), hmf_ext_slope=float(SLOPE_HMF),
                   m_solved_min=float(MGRID[okm_].min()))
say(f"  HMF extension slope s {SLOPE_HMF:.3f}; matching solved down to log M* {MGRID[okm_].min():.2f}")
# satellites
MF = 8.6
MS_FINE = np.arange(MF, 12.5, 0.01)
Mmin_f = 10 ** lMmin_of_m(MS_FINE)
sat_pos, sat_lms, sat_host = [], [], []
nsat_exp = np.maximum(Mta - Mmin_f[0], 0) / (17 * Mmin_f[0])
nsat = rng.poisson(nsat_exp)
hosts = np.where(nsat > 0)[0]
for i in hosts:
    rr = r200m[i] if r200m[i] > 0 else 0.3 * rta[i]
    li = tree.query_ball_point(cen[i], rr)
    if len(li) == 0:
        li = [tree.query(cen[i])[1]]
    cum = np.maximum(Mta[i] - Mmin_f, 0) / (17 * Mmin_f)            # N_sat(> m | M), decreasing in m
    u = rng.uniform(0, 1, nsat[i]) * cum[0]
    ms = np.interp(u, cum[::-1], MS_FINE[::-1])
    pick = rng.choice(len(li), nsat[i], replace=True)
    sat_pos.append(pos[np.asarray(li)[pick]]); sat_lms.append(ms); sat_host.append(np.full(nsat[i], i))
sat_pos = np.concatenate(sat_pos) if sat_pos else np.zeros((0, 3)); sat_lms = np.concatenate(sat_lms) if sat_lms else np.zeros(0)
sat_host = np.concatenate(sat_host) if sat_host else np.zeros(0, int)
GPOS = np.concatenate([cen, sat_pos]); GLMS = np.concatenate([lms_c, sat_lms])
GSAT = np.concatenate([np.zeros(len(cen), bool), np.ones(len(sat_lms), bool)])
GHALO = np.concatenate([np.arange(len(cen)), sat_host])
NGAL = len(GPOS)
say(f"galaxies: {len(cen)} centrals + {len(sat_lms)} satellites (log M* >= {MF}); satellite fraction above 10.0: "
    f"{GSAT[GLMS >= 10].mean():.3f}, above 10.5: {GSAT[GLMS >= 10.5].mean():.3f}")
OUT["n_sat"] = int(len(sat_lms))
OUT["fsat_par"] = {f"{a:.1f}": float(GSAT[(GLMS >= a) & (GLMS < a + 0.1)].mean()) if ((GLMS >= a) & (GLMS < a + 0.1)).any() else None
                   for a in np.arange(9.0, 11.1, 0.1)}

def finish(extra):
    np.savez_compressed(os.path.join(WORK, f"cfg506_box_{KEY}.npz"), LB=LB, ZN=np.array([0.15, 0.25, 0.35, 0.45]),
                        cen=cen.astype(np.float32), Mta=Mta, rta=rta, M200m=M200m, r200m=r200m, cprox=cprox, lms_c=lms_c,
                        sat_lms=sat_lms, sat_host=sat_host, P3=P3, P3n=P3n, P3S=P3S, EDGES3=EDGES3, PBINS=np.array(PBINS),
                        **({f"D1_{k}": v.astype(np.float32) for k, v in D1.items()}),
                        **(dict(D2_q=D2_q, D2_M=D2_M, D2_hostM=hostM) if KIND == "TA" else {}),
                        mlim_box=mlim_box, MP=MP, dx=dx, **extra)
    OUT["checks"] = CHK; OUT["elapsed_s"] = round(time.time() - T0, 1)
    fr = os.path.join(HERE, "cfg506_box_results.json")
    allres = json.load(open(fr)) if os.path.exists(fr) else {}
    OUT["log"] = LOG
    allres[KEY] = OUT
    json.dump(allres, open(fr, "w"), indent=1)
    with open(os.path.join(HERE, "cfg506_box.out"), "w") as f:
        for k in BOXES:
            if k in allres:
                f.write("\n".join(allres[k]["log"]) + "\n\n")
    say("done")
    bad = [k for k, c in CHK.items() if c["load_bearing"] and not c["ok"]]
    sys.exit(1 if bad else 0)


LB = np.round(np.arange(8.5, 11.1001, 0.1), 2)
VB = [k for k in range(len(LB) - 1) if LB[k] >= mlim_box - 1e-9]
if not VB:
    say(f"no lens bin above m_lim,box {mlim_box:.2f}: no ruler from this box (diagnostics only)")
    OUT["valid_bins"] = []
    finish({})

# ================================================================= 4. lenses, kernels, isolation, companion counts
lens_idx, lens_bin = [], []
for k in VB:
    for issat in (False, True):
        sel = np.where((GLMS >= LB[k]) & (GLMS < LB[k + 1]) & (GSAT == issat))[0]
        if len(sel) > 6000:
            sel = np.sort(rng.choice(sel, 6000, replace=False))
        lens_idx.append(sel); lens_bin.append(np.full(len(sel), k))
lens_idx = np.concatenate(lens_idx); lens_bin = np.concatenate(lens_bin)
NL = len(lens_idx)
LPOS = GPOS[lens_idx]; LLMS = GLMS[lens_idx]; LSAT = GSAT[lens_idx]
rng7 = np.random.default_rng(507)
SPOS = rng7.uniform(0, L, size=(NL, 3))                    # MUTATE SHUF centres
# fix (10-08, after the first run's C3 failure): every centre is snapped to the fine-grid node (<= 0.75 fine cell; 0.04 Mpc/h at 512^3) so the
# map is read at nodes (no interpolation) and the own content is measured around exactly the same point
DXF = L / (8 * N)
LPOS = (np.round(LPOS / DXF) * DXF) % L; SPOS = (np.round(SPOS / DXF) * DXF) % L
say(f"lenses: {NL} in {len(VB)} bins ({LB[VB[0]]:.1f}-{LB[VB[-1] + 1]:.1f}); centrals {int((~LSAT).sum())}, satellites {int(LSAT.sum())}")

S = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
ZN = np.array([0.15, 0.25, 0.35, 0.45])
DEh = S["DE"]; Hin, Han = S["H_in"], S["H_an"]
xc = 0.5 * (DEh[1:] + DEh[:-1]); bw = np.diff(DEh)
KER = []
for n in range(4):
    ex = (Hin[2 * n] + Hin[2 * n + 1]) - (Han[2 * n] + Han[2 * n + 1]) * (0.09 / 20.0)
    ex = 0.5 * (ex + ex[::-1])                              # symmetrise
    KER.append(ex / ex.sum())
DG = np.arange(0.0, 800.0, 0.5)                             # true |D| in Mpc
PTAB = np.zeros((4, len(DG)))
for n in range(4):
    for i, D in enumerate(DG):                              # p(D) = sum_b K_b * overlap([x_b - bw/2, x_b + bw/2] + D, [-10, 10]) / bw
        lo_ = np.maximum(DEh[:-1] + D, -10.0); hi_ = np.minimum(DEh[1:] + D, 10.0)
        PTAB[n, i] = np.clip((KER[n] * np.maximum(hi_ - lo_, 0) / bw).sum(), 0, 1)
DMAXB = 0.5 * L / LH                                        # Mpc (148.5)
IFAR = np.array([2 * np.trapz(PTAB[n][DG >= DMAXB], DG[DG >= DMAXB]) * LH for n in range(4)])   # Mpc/h
IALL = np.array([2 * np.trapz(PTAB[n], DG) * LH for n in range(4)])
MLIM = np.interp(ZN, S["Z0"], S["mlim"])
# DEPARTURE D1 (disclosed in the README; decided after seeing the box isolation pass fraction, before any KiDS re-score): the frozen neighbour
# threshold mlim (the pool's 5th percentile) treats the flux-limited pool as complete above it, so the box's neighbour density is ~5x the
# KiDS pool's. Variant "P": a completeness step m_c(z_n) set so that the SMF density above max(M*_lens - 1, m_c), averaged over the CFG502
# close-pair lens subsample of that node, reproduces the MEASURED chance count of qualifying neighbours (4-6 Mpc annulus pairs with
# |dchi| < 10 Mpc, scaled to 3 Mpc). Photometry only. Variant "F" = the frozen rule. Both are carried to the end.
xcm = 0.5 * (DEh[1:] + DEh[:-1]); w10 = np.abs(xcm) < 10
zsub = S["z"][S["sub"]]; lmsub = S["logM"][S["sub"]]; ZBs = S["ZB"]
MC = np.zeros(4); LAMM = np.zeros(4)
for n in range(4):
    lam = (S["H_an"][2 * n][w10].sum() + S["H_an"][2 * n + 1][w10].sum()) / (S["NLZ"][2 * n] + S["NLZ"][2 * n + 1]) * 9.0 / 20.0
    msk = (zsub >= ZBs[2 * n]) & (zsub < ZBs[2 * n + 2]); lmn = lmsub[msk]
    g = lambda mc: float(np.mean(n_smf(np.maximum(lmn - 1.0, mc)))) * 0.343 * math.pi * 9.0 * 20.0 - lam
    MC[n] = brentq(g, 7.0, 12.5); LAMM[n] = lam
THRS = {"F": MLIM, "P": MC}
OUT["D1_departure"] = dict(m_c=MC.tolist(), lambda_meas=LAMM.tolist(), mlim=MLIM.tolist())
say(f"departure D1: measured chance neighbours per lens {np.round(LAMM, 3).tolist()}; pool completeness step m_c {np.round(MC, 2).tolist()} "
    f"(frozen mlim {np.round(MLIM, 2).tolist()})")
OUT["kernel"] = dict(ZN=ZN.tolist(), p_at_0=PTAB[:, 0].tolist(), Ifar_Mpch=IFAR.tolist(), Iall_Mpch=IALL.tolist(), mlim=MLIM.tolist())
say(f"kernels: p(0) {np.round(PTAB[:, 0], 4).tolist()}, int p dD (Mpc/h) {np.round(IALL, 2).tolist()} (13.47 expected), far part {np.round(IFAR, 3).tolist()}")
GSORT = np.sort(GLMS)
def n_box_above(t): return (NGAL - np.searchsorted(GSORT, t)) / V

R_ISO, R_IN, R_A1, R_A2 = 3.0 * LH, 0.5 * LH, 4.0 * LH, 6.0 * LH
AREA_RATIO = R_IN ** 2 / (R_A2 ** 2 - R_A1 ** 2)
WISO = {v: np.zeros((3, 4, NL)) for v in THRS}; CEX = {v: np.zeros((3, 4, NL)) for v in THRS}
for ax in range(3):
    a2 = [i for i in range(3) if i != ax]
    t2 = cKDTree(GPOS[:, a2] % L, boxsize=L)
    for c0 in range(0, NL, 4000):
        sl = slice(c0, min(c0 + 4000, NL))
        lists = t2.query_ball_point(LPOS[sl][:, a2] % L, R_A2, workers=4)
        ln = np.repeat(np.arange(sl.start, sl.stop), [len(x) for x in lists])
        jn = np.concatenate([np.asarray(x, int) for x in lists])
        selfm = jn != lens_idx[ln]
        ln, jn = ln[selfm], jn[selfm]
        dtr = GPOS[jn][:, a2] - LPOS[ln][:, a2]; dtr -= L * np.round(dtr / L); Rt = np.hypot(dtr[:, 0], dtr[:, 1])
        dl = GPOS[jn, ax] - LPOS[ln, ax]; dl -= L * np.round(dl / L)
        Dm = np.abs(dl) / LH
        for n in range(4):
            p = np.interp(Dm, DG, PTAB[n])
            for v, TH in THRS.items():
                thr = np.maximum(LLMS[ln] - 1.0, TH[n])
                iso = (Rt < R_ISO) & (GLMS[jn] > thr)
                lw = np.bincount(ln[iso] - sl.start, weights=np.log(np.maximum(1 - p[iso], 1e-12)), minlength=sl.stop - sl.start)
                thr_l = np.maximum(LLMS[sl] - 1.0, TH[n])
                nthr = n_smf(thr_l); nmiss = np.maximum(nthr - np.array([n_box_above(t) for t in thr_l]), 0)
                lam = nthr * math.pi * R_ISO ** 2 * IFAR[n] + nmiss * math.pi * R_ISO ** 2 * (2 * 10.0 * LH)
                WISO[v][ax, n, sl] = np.exp(lw - lam)
                cm = GLMS[jn] > np.maximum(LLMS[ln], TH[n])
                wq = 1 - p
                cin = np.bincount(ln[cm & (Rt < R_IN)] - sl.start, weights=wq[cm & (Rt < R_IN)], minlength=sl.stop - sl.start)
                can = np.bincount(ln[cm & (Rt >= R_A1) & (Rt < R_A2)] - sl.start, weights=wq[cm & (Rt >= R_A1) & (Rt < R_A2)],
                                  minlength=sl.stop - sl.start)
                CEX[v][ax, n, sl] = cin - can * AREA_RATIO
    del t2
# pass fraction of all lens candidates (box, sampling-corrected) vs KiDS (ISO / ALL), per node, lenses >= the lowest valid bin
NALL = {(b, t): int(((GLMS >= LB[b]) & (GLMS < LB[b + 1]) & (GSAT == t)).sum()) for b in VB for t in (False, True)}
NUSE = {(b, t): int(((lens_bin == b) & (LSAT == t)).sum()) for b in VB for t in (False, True)}
OUT["pass_fraction"] = {}
for v in THRS:
    for n in range(4):
        num = den = 0.0
        for b in VB:
            for t in (False, True):
                m_ = (lens_bin == b) & (LSAT == t)
                if m_.any():
                    num += NALL[(b, t)] * WISO[v][:, n, m_].mean(); den += NALL[(b, t)]
        zz = (S["z"] >= ZBs[2 * n]) & (S["z"] < ZBs[2 * n + 2]) & (S["logM"] >= LB[VB[0]])
        kp = float(S["iso10"][zz].mean())
        OUT["pass_fraction"][f"{v}|{ZN[n]}"] = dict(box=num / den, kids=kp)
    say(f"  variant {v}: isolation pass fraction box / KiDS per node: " + ", ".join(
        f"{ZN[n]}: {OUT['pass_fraction'][f'{v}|{ZN[n]}']['box']:.3f}/{OUT['pass_fraction'][f'{v}|{ZN[n]}']['kids']:.3f}" for n in range(4))
        + f"; mean w centrals {WISO[v][:, 1, ~LSAT].mean():.3f}, satellites {WISO[v][:, 1, LSAT].mean():.3f}")

# ================================================================= 5. DeltaSigma
RE = np.geomspace(0.02, 15.0, 41); RM = np.sqrt(RE[1:] * RE[:-1])
NF = 8 * N; DXF = L / NF
kf1 = 2 * np.pi * sfft.fftfreq(NF, d=DXF); kf2 = 2 * np.pi * sfft.rfftfreq(NF, d=DXF)
KK = np.sqrt(kf1[:, None] ** 2 + kf2[None, :] ** 2)


SIGF = DXF                                                  # Gaussian taper of the disc filter (1 fine cell)
from scipy import stats as sst
WCIC = (np.sinc(kf1[:, None] * DXF / (2 * np.pi)) ** 2 * np.sinc(kf2[None, :] * DXF / (2 * np.pi)) ** 2)
TAPER = np.exp(-0.5 * KK ** 2 * SIGF ** 2) / WCIC          # CIC deconvolved, Gaussian-tapered


def disc_filter(R):
    """fix (10-08): the bare disc filter rang by up to 7.7% at R >= 3 fine cells (first run, C3 FAIL, kept in the README); the filter is now
    a disc convolved with a 2D Gaussian of sigma = 1 fine cell (CIC deconvolved), and the own content gets the SAME smoothing exactly (PT)."""
    x = KK * R; out = np.ones_like(x); nz = x > 1e-12
    out[nz] = 2 * j1(x[nz]) / x[nz]
    return out * TAPER


# PT[i, j] = P(|rho_i + g| < RE_j), g ~ 2D Gaussian(SIGF): the smoothed disc mass of a unit point at projected distance rho_i (Rice CDF)
RHO_E = np.arange(0.0, 2.6 + 1e-9, 0.0025); RHO_C = 0.5 * (RHO_E[1:] + RHO_E[:-1])
PT = np.array([sst.rice.cdf(R, RHO_C / SIGF, scale=SIGF) for R in RE]).T       # (n_rho, 41)


def node(xy):
    return (np.round(xy / DXF).astype(np.int64)) % NF


# C3: one particle deposited by CIC off-node, read at its nearest node, against the exact smoothed expectation (criterion: within 2% at R >= 3 cells)
xp = np.array([L / 2 + 0.37 * DXF, L / 2 + 0.21 * DXF])
pm = np.zeros(NF * NF); u = xp / DXF; i0 = np.floor(u).astype(np.int64); f = u - i0
for sx in (0, 1):
    for sy in (0, 1):
        pm[((i0[0] + sx) % NF) * NF + (i0[1] + sy) % NF] += (f[0] if sx else 1 - f[0]) * (f[1] if sy else 1 - f[1])
pm = pm.reshape(NF, NF) / DXF ** 2
pk_ = sfft.rfft2(pm, workers=4)
nd = node(xp[None, :])[0]; off = np.hypot(*(xp - nd * DXF))
vals = np.array([sfft.irfft2(pk_ * disc_filter(R), s=(NF, NF), workers=4)[nd[0], nd[1]] * math.pi * R ** 2 for R in RE])
expct = sst.rice.cdf(RE, off / SIGF, scale=SIGF)
okR = RE >= 3 * DXF
c3 = float(np.max(np.abs(vals[okR] / expct[okR] - 1)))
check("C3 Fourier-disc mass of a point mass = M within 2% at R >= 3 fine cells (smoothed-disc expectation)", c3 < 0.02,
      f"max |M(<R)/expected - 1| {c3:.2e}; expected/M at 3 cells {expct[okR][0]:.4f}")
del pm, pk_

MCUM = np.zeros((3, NL, len(RE))); MCUMS = np.zeros((3, NL, len(RE))); MCUM_SRC = np.zeros((3, NL, len(RE)))
for ax in range(3):
    a2 = [i for i in range(3) if i != ax]
    mp2 = np.zeros(NF * NF)
    for c0 in range(0, NP, 16_000_000):
        u = pos[c0:c0 + 16_000_000][:, a2] / DXF; i0 = np.floor(u).astype(np.int64); f = u - i0
        for sx in (0, 1):
            for sy in (0, 1):
                w = (f[:, 0] if sx else 1 - f[:, 0]) * (f[:, 1] if sy else 1 - f[:, 1])
                mp2 += np.bincount(((i0[:, 0] + sx) % NF) * NF + (i0[:, 1] + sy) % NF, weights=w, minlength=NF * NF)
    mp2 = mp2.reshape(NF, NF) * MP / DXF ** 2                  # Sigma, (Msun/h) / (Mpc/h)^2
    maps = [mp2]
    if SRC is not None:
        sc = SRC.sum(axis=ax, dtype=np.float64) * RHOM_H * dx ** 3          # mass per coarse column
        sf = np.roll(np.kron(sc / 64.0, np.ones((8, 8))), (-4, -4), axis=(0, 1)) / DXF ** 2
        maps = [mp2 + sf, sf]
        del sc, sf
    Fks = [sfft.rfft2(M_, workers=4) for M_ in maps]
    for ir, R in enumerate(RE):
        filt = disc_filter(R)
        for im, Fk in enumerate(Fks):
            sm = sfft.irfft2(Fk * filt, s=(NF, NF), workers=4)
            if im == 0:
                ndl = node(LPOS[:, a2]); MCUM[ax, :, ir] = sm[ndl[:, 0], ndl[:, 1]] * math.pi * R ** 2
                nds = node(SPOS[:, a2]); MCUMS[ax, :, ir] = sm[nds[:, 0], nds[:, 1]] * math.pi * R ** 2
            else:
                ndl = node(LPOS[:, a2]); MCUM_SRC[ax, :, ir] = sm[ndl[:, 0], ndl[:, 1]] * math.pi * R ** 2
            del sm
        del filt
    del Fks
    del maps, mp2
    say(f"  axis {ax}: maps + disc means done")

# own-sphere content (centrals and shuffled centrals): particles + S cells within r_rem(z node)
ET = np.load(os.path.join(EXT, "cfg503_work", "cfg503_env_table.npz"))
LMS_, ZG_ = ET["LMS"], ET["ZG"]
from scipy.interpolate import RegularGridInterpolator
frta = RegularGridInterpolator((LMS_, ZG_), ET["moster_RTA"], bounds_error=False, fill_value=None)
RREM = np.zeros((4, NL))
for n in range(4):
    RREM[n] = frta(np.c_[np.clip(LLMS, LMS_[0], LMS_[-1]), np.full(NL, ZN[n])]) * (1 + ZN[n]) * LH      # comoving Mpc/h
RREM[:, LSAT] = 0.0
OWN = np.zeros((3, 4, NL, len(RE))); OWNS = np.zeros((3, 4, NL, len(RE))); OWN_SRC = np.zeros((3, 4, NL, len(RE)))
rmax = RREM.max(0)
cidx = np.where(~LSAT)[0]


def own_content(P3, rem_max, store, store_src):
    for c0 in range(0, len(cidx), 2000):
        ids = cidx[c0:c0 + 2000]
        lists = tree.query_ball_point(P3[ids], rem_max[ids], workers=4)
        for t_, i in enumerate(ids):
            li = np.asarray(lists[t_], int)
            d = pos[li] - P3[i]; d -= L * np.round(d / L)
            r3 = np.sqrt((d ** 2).sum(1))
            if SRC is not None:
                nb = int(math.ceil(rem_max[i] / dx)) + 1; obb = np.arange(-nb, nb + 1)
                cc = np.floor(P3[i] / dx).astype(int)
                gx = (cc[0] + obb) % N; gy = (cc[1] + obb) % N; gz = (cc[2] + obb) % N
                cube = SRC[np.ix_(gx, gy, gz)].astype(np.float64) * RHOM_H * dx ** 3
                off = (obb * dx)[:, None, None], (obb * dx)[None, :, None], (obb * dx)[None, None, :]
                cpos = [(cc[k] * dx + off[k]) for k in range(3)]                       # cell nodes (CIC node convention)
                dcx = (cpos[0] - P3[i][0]); dcy = (cpos[1] - P3[i][1]); dcz = (cpos[2] - P3[i][2])
                dcx, dcy, dcz = np.broadcast_arrays(dcx, dcy, dcz)
                rc = np.sqrt(dcx ** 2 + dcy ** 2 + dcz ** 2).ravel(); dcs = np.c_[dcx.ravel(), dcy.ravel(), dcz.ravel()]
                cw = cube.ravel()
            for n in range(4):
                rr = RREM[n, i]
                s_ = r3 < rr
                if SRC is not None:
                    sc_ = rc < rr
                for ax in range(3):
                    a2 = [k for k in range(3) if k != ax]
                    R2 = np.hypot(d[s_][:, a2[0]], d[s_][:, a2[1]])
                    hb = np.bincount(np.minimum((R2 / 0.0025).astype(np.int64), len(RHO_C) - 1), minlength=len(RHO_C))
                    store[ax, n, i] = (hb @ PT) * MP
                    if SRC is not None:
                        Rc_ = np.hypot(dcs[sc_][:, a2[0]], dcs[sc_][:, a2[1]])
                        hs_ = np.bincount(np.minimum((Rc_ / 0.0025).astype(np.int64), len(RHO_C) - 1), weights=cw[sc_], minlength=len(RHO_C))
                        v = hs_ @ PT
                        store[ax, n, i] += v
                        if store_src is not None:
                            store_src[ax, n, i] = v


own_content(LPOS, rmax, OWN, OWN_SRC)
own_content(SPOS, rmax, OWNS, None)
say("own-sphere content done")


def dsig_from_cum(Mc):
    """Mc[..., 41] cumulative projected mass at RE -> DeltaSigma at RM (constant Sigma within each annulus)."""
    dM = np.diff(Mc, axis=-1); dA = math.pi * np.diff(RE ** 2)
    Sig = dM / dA
    Mmid = Mc[..., :-1] + dM * (RM ** 2 - RE[:-1] ** 2) / np.diff(RE ** 2)
    return Mmid / (math.pi * RM ** 2) - Sig


# uniform rho_bar sphere (the hole alone), same discretisation
def sphere_cum(a):
    a = np.asarray(a, float)[..., None]
    Mt = 4 * math.pi / 3 * a ** 3 * RHOM_H
    x = np.clip(RE / np.maximum(a, 1e-12), 0, 1)
    return np.where(a > 0, Mt * (1 - (1 - x ** 2) ** 1.5), 0.0)


NB = len(LB) - 1
jk = (np.floor(LPOS / (L / 3)).astype(int) % 3) @ np.array([9, 3, 1])
jks = (np.floor(SPOS / (L / 3)).astype(int) % 3) @ np.array([9, 3, 1])
idx_l = jk * NB + lens_bin; idx_s = jks * NB + lens_bin
SAVE = {}
for v in THRS:
    TAB = {k: np.zeros((27, NB, 4, len(RM))) for k in ("E", "E_cen", "E_sat", "E_src", "TOT_cen", "SHUF", "H", "HSHUF")}
    WT = {k: np.zeros((27, NB, 4)) for k in ("all", "cen", "sat", "shuf")}
    CT = np.zeros((27, NB, 4)); FS = np.zeros((27, NB, 4))
    LMW = np.zeros((NB, 4)); LMWW = np.zeros((NB, 4))
    for n in range(4):
        Hc = dsig_from_cum(sphere_cum(RREM[n]))                  # hole for centrals, 0 for satellites
        for ax in range(3):
            w = WISO[v][ax, n]
            Ei = dsig_from_cum(MCUM[ax] - OWN[ax, n])
            Es = dsig_from_cum(MCUMS[ax] - OWNS[ax, n])
            Esrc = dsig_from_cum(MCUM_SRC[ax] - OWN_SRC[ax, n]) if SRC is not None else np.zeros_like(Ei)
            Tc = dsig_from_cum(MCUM[ax])
            for key_, arr, ix_, wsel in (("E", Ei, idx_l, None), ("E_cen", Ei, idx_l, ~LSAT), ("E_sat", Ei, idx_l, LSAT),
                                         ("E_src", Esrc, idx_l, None), ("TOT_cen", Tc, idx_l, ~LSAT), ("SHUF", Es, idx_s, None),
                                         ("H", Hc, idx_l, None), ("HSHUF", Hc, idx_s, None)):
                ww = w if wsel is None else w * wsel
                acc = np.zeros((27 * NB, len(RM)))
                np.add.at(acc, ix_, ww[:, None] * arr)
                TAB[key_][:, :, n] += acc.reshape(27, NB, len(RM))
            WT["all"][:, :, n] += np.bincount(idx_l, weights=w, minlength=27 * NB).reshape(27, NB)
            WT["cen"][:, :, n] += np.bincount(idx_l, weights=w * ~LSAT, minlength=27 * NB).reshape(27, NB)
            WT["sat"][:, :, n] += np.bincount(idx_l, weights=w * LSAT, minlength=27 * NB).reshape(27, NB)
            WT["shuf"][:, :, n] += np.bincount(idx_s, weights=w, minlength=27 * NB).reshape(27, NB)
            CT[:, :, n] += np.bincount(idx_l, weights=w * CEX[v][ax, n], minlength=27 * NB).reshape(27, NB)
            FS[:, :, n] += np.bincount(idx_l, weights=w * LSAT, minlength=27 * NB).reshape(27, NB)
            LMW[:, n] += np.bincount(lens_bin, weights=w * LLMS, minlength=NB); LMWW[:, n] += np.bincount(lens_bin, weights=w, minlength=NB)
    SAVE.update({f"{v}_T_{k}": x for k, x in TAB.items()}); SAVE.update({f"{v}_W_{k}": x for k, x in WT.items()})
    SAVE.update({f"{v}_CT": CT, f"{v}_FS": FS, f"{v}_LMW": LMW, f"{v}_LMWW": LMWW})
    den_ = WT["all"].sum(0)
    E_all = TAB["E"].sum(0) / np.maximum(den_[..., None], 1e-300)
    fs = FS.sum(0) / np.maximum(den_, 1e-300)
    for b in VB[::2]:
        n = 1
        say(f"  [{v}] bin {LB[b]:.1f}-{LB[b + 1]:.1f} z {ZN[n]}: f_sat(iso) {fs[b, n]:.3f}; E_native(R_com 0.1/0.5/1/2/4 Mpc/h) "
            f"{np.round(np.interp([0.1, 0.5, 1, 2, 4], RM, E_all[b, n]) / 1e12 * LH, 3).tolist()} Msun/pc^2 (z = 0, comoving); "
            f"companions {CT.sum(0)[b, n] / max(den_[b, n], 1e-300):.3f}")
say("stacks done")

OUT["n_lenses"] = int(NL); OUT["valid_bins"] = [float(LB[b]) for b in VB]
finish(dict(RE=RE, RM=RM, VB=np.array(VB), **SAVE, NL=NL, nlens_cen=int((~LSAT).sum()), nlens_sat=int(LSAT.sum())))
