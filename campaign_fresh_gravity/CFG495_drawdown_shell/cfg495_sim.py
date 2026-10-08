#!/usr/bin/env python3
"""CFG495 Step 1 (simulation): the cold-fluid DRAWDOWN around resolved halos in the zero-knob runs (CFG424 engine, RC = 0).

For one committed z = 0 snapshot pair (TA run + matched-seed S0 control) this script
  1. deposits the TA particles and recomputes the RES/TA source fields with the CFG424 engine's own functions (imported read-only):
     e    = phantom excess (T1 switch x edge balls x catchment),
     comp = s_c * q_C on each catchment C (the proportional draw the engine applies; q_C = sum_C e / sum_C s_c),
     comp_sh = the OUTER-SHELL-ONLY variant (same sum_C e drawn only from catchment cells outside every edge ball) - static, z = 0 only;
  2. finds the resolved hosts with the engine's own peak finder (r_ON >= 1.56 Mpc/h), their edge r_edge = x_supply * r_ON;
  3. stacks, per mass bin, 3D profiles in r/r_ta and r/r_edge of: delta_TA (particles), delta_S0 (control, same centres), e, comp, comp_sh;
  4. projects along x, y, z and stacks Delta Sigma(R) in R/r_ta of the same fields (units h Msun/pc^2 at z = 0);
  5. (S0 only) stacks the ENVIRONMENT term Delta Sigma_out(R) = lensing by everything outside each peak's own r_ta ball, around
     isolated galaxy-scale peaks (r_ON 0.62-1.25 Mpc/h at 512^3), for the frozen two-halo template of Step 3;
  6. MUTATE (CFG495_MUTATE=1): the same stacks at randomly placed centres (shuffled positions) - the drawdown must vanish.

Fix (10-08, after the first frozen run): an annulus / shell with no cell centres now gives NaN instead of a spurious value (the annulus mean was
set to 0, so Delta Sigma there returned the inner mean). Stacks use NaN-aware means.

Usage: nice -n 15 python3 cfg495_sim.py KEY      KEY in RUNS below.  Writes ../../../_external_data/cfg495_work/cfg495_sim_KEY[_MUTATE].npz + .json
"""
import os, sys, json, math, time, importlib.util
os.environ.setdefault("CFG424_THREADS", "4")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = os.environ["CFG424_THREADS"]
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
OUTW = os.path.join(EXT, "cfg495_work"); os.makedirs(OUTW, exist_ok=True)
W424 = os.path.join(EXT, "cfg424_work")
MUTATE = os.environ.get("CFG495_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""

RUNS = {  # key: (N, foot, branch, TA snapshot, S0 snapshot, NOCOMP snapshot or None, TA json)
    "N512_s360_can": (512, "canonical", "FLAT", f"{W424}/cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360_z0.npz",
                      f"{W424}/cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360_z0.npz", None),
    "N512_s359_can": (512, "canonical", "FLAT", f"{W424}/cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_z0.npz",
                      f"{EXT}/cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512_z0.npz", None),
    "N512_s359_alt": (512, "alt", "FLAT", f"{W424}/cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_alt_N512_z0.npz",
                      f"{EXT}/cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512_z0.npz", None),
    "N256_s359_can": (256, "canonical", "FLAT", f"{W424}/cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N256_z0.npz",
                      f"{EXT}/cfg359_work/cfg359_S0_FLAT_canonical_N256_z0.npz",
                      f"{W424}/cfg424_RES_TA_NOCOMP_MIXA_MASSCONS_fret1_FLAT_canonical_N256_z0.npz"),
    "N256_s359_alt": (256, "alt", "FLAT", f"{W424}/cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_alt_N256_z0.npz",
                      f"{EXT}/cfg359_work/cfg359_S0_FLAT_canonical_N256_z0.npz", None),
}
KEY = sys.argv[1]
N, FOOT, BRANCH, F_TA, F_S0, F_NC = RUNS[KEY]
T0 = time.time()
def say(s): print(f"[{time.time() - T0:7.1f}s] {s}", flush=True)

# ---------------------------------------------------------------- the engine, imported read-only
spec = importlib.util.spec_from_file_location("eng424", os.path.join(HERE, "..", "CFG424_turnaround_catchment", "cfg424_pm.py"))
eng = importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)
eng.RC = 0.0; eng.MIX = "MIXA"
Om, FB, L = eng.Om, eng.FB, eng.L
mesh = eng.Mesh(N); dx = mesh.dx
dta = eng.dta_table(); A = 1.0
DTA = math.exp(np.interp(math.log(1 / A), np.log1p(dta["z"]), np.log(dta["D"])))
RHOM = Om * 2.775e11                                   # h^2 Msun / Mpc^3 (comoving mean matter)
SIG_UNIT = RHOM * dx / 1e12                            # (sum of delta along a column) -> h Msun / pc^2
say(f"KEY {KEY}: N {N}, foot {FOOT}, dx {dx:.4f} Mpc/h, Delta_ta(z=0) {DTA:.3f}, MUTATE {MUTATE}")

def load_delta(path):
    pos = np.load(path)["pos"]
    d = mesh.deposit(pos); del pos
    return d

# ---------------------------------------------------------------- peaks (copy of the engine's in_cover peak finder; checked against in_cover below)
def peaks(delta):
    from scipy import ndimage
    tau = (DTA - 1.0) / 3.0
    mx = ndimage.maximum_filter(delta, size=3, mode="wrap")
    pk = (delta == mx) & (delta >= 3 * (tau - eng.EPS))
    Rg = np.geomspace(dx, 8.0, 14)
    kk = np.sqrt(mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2)
    def tophat_k(R):
        kr = kk * R; out = np.ones_like(kr); nz = kr > 1e-8
        out[nz] = 3 * (np.sin(kr[nz]) - kr[nz] * np.cos(kr[nz])) / kr[nz] ** 3
        return out.astype(np.float32)
    rhok = mesh.fwd((1.0 + delta).astype(np.float32))
    idx = np.argwhere(pk); ok = np.ones(len(idx), bool); ron = np.zeros(len(idx))
    for R in Rg:
        mean = mesh.inv(rhok * tophat_k(R))[idx[:, 0], idx[:, 1], idx[:, 2]]
        ok &= mean >= DTA; ron[ok] = R
    return idx, ron, Rg

def ball_union(idx, rad):
    """union of balls (radius rad per peak) around peak cells, same FFT construction as the engine."""
    mask = np.zeros((N,) * 3, bool)
    for R in np.unique(rad):
        sel = rad == R
        pts = np.zeros((N,) * 3, np.float32); pts[idx[sel, 0], idx[sel, 1], idx[sel, 2]] = 1.0
        if R < 0.5 * dx:
            mask |= pts > 0.5; continue
        g = np.arange(N); g = np.minimum(g, N - g) * dx
        ball = ((g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2) <= R * R).astype(np.float32)
        mask |= mesh.inv(mesh.fwd(pts) * mesh.fwd(ball)) > 0.5
    return mask

# ---------------------------------------------------------------- the TA source fields (engine's RES / RC = 0 branch at a = 1, diag path)
def sources(delta):
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
    e = (fsw * np.maximum(s_ph - s_c, 0.0) * catch).astype(np.float32); del fsw, s_ph
    r, nc = eng.catch_labels(catch); mm = r >= 0
    E_ = np.bincount(r[mm], weights=e.ravel()[mm].astype(np.float64), minlength=nc)
    C_ = np.bincount(r[mm], weights=s_c.ravel()[mm].astype(np.float64), minlength=nc)
    q = E_ / np.maximum(C_, 1e-30)
    comp = np.zeros(e.size, np.float32); comp[mm] = (s_c.ravel()[mm] * q[r[mm]]).astype(np.float32); comp = comp.reshape(e.shape)
    # outer-shell-only variant: draw sum_C e only from catchment cells outside every edge ball
    sh = mm & ~edge.ravel()
    Csh = np.bincount(r[sh], weights=s_c.ravel()[sh].astype(np.float64), minlength=nc)
    qsh = np.where(Csh > 0, E_ / np.maximum(Csh, 1e-30), 0.0)
    lost = float(E_[(Csh <= 0) & (E_ > 0)].sum() / max(E_.sum(), 1e-30))
    comp_sh = np.zeros(e.size, np.float32); comp_sh[sh] = (s_c.ravel()[sh] * qsh[r[sh]]).astype(np.float32); comp_sh = comp_sh.reshape(e.shape)
    w_ = np.bincount(r[mm], weights=(1.0 + delta).ravel()[mm].astype(np.float64), minlength=nc)
    info = dict(q_max=float(q.max()) if nc else 0.0, overdraw_mass=float(w_[q > 1].sum() / max(w_.sum(), 1e-30)),
                src_sum=float((e - comp).sum()), e_mean=float(e.mean()), n_catch=int(nc),
                q_massweighted=float((q * C_).sum() / max(C_.sum(), 1e-30)), q_med=float(np.median(q[E_ > 0])) if (E_ > 0).any() else 0.0,
                qsh_max=float(qsh.max()), qsh_overdraw_mass=float(w_[qsh > 1].sum() / max(w_.sum(), 1e-30)), shell_lost_frac=lost,
                vol_catch=float(catch.mean()), vol_edge=float(edge.mean()))
    lab = r.reshape(e.shape)
    return e, comp, comp_sh, edge, catch, lab, q, info

# ---------------------------------------------------------------- stacking
XB = np.linspace(0.0, 3.0, 31)        # r / r_ta and R / r_ta bin edges
YB = np.linspace(0.0, 12.0, 25)       # r / r_edge bin edges
def prof3d(fields, c, R, re):
    n = int(math.ceil(3.0 * R / dx)) + 1
    o = np.arange(-n, n + 1); ix = (c[0] + o) % N; iy = (c[1] + o) % N; iz = (c[2] + o) % N
    rr = np.sqrt(o[:, None, None] ** 2 + o[None, :, None] ** 2 + o[None, None, :] ** 2).ravel() * dx
    bx = np.digitize(rr / R, XB) - 1; okx = (bx >= 0) & (bx < len(XB) - 1)
    by = np.digitize(rr / re, YB) - 1; oky = (by >= 0) & (by < len(YB) - 1)
    cx = np.bincount(bx[okx], minlength=len(XB) - 1); cy = np.bincount(by[oky], minlength=len(YB) - 1)
    outx, outy, own = [], [], []
    for F in fields:
        sub = F[np.ix_(ix, iy, iz)].ravel().astype(np.float64)
        outx.append(np.where(cx > 0, np.bincount(bx[okx], weights=sub[okx], minlength=len(XB) - 1) / np.maximum(cx, 1), np.nan))   # empty shell -> NaN
        outy.append(np.where(cy > 0, np.bincount(by[oky], weights=sub[oky], minlength=len(YB) - 1) / np.maximum(cy, 1), np.nan))
        own.append(sub[rr <= R].sum())
    return np.array(outx), np.array(outy), np.array(own)

def dsig2d(maps, c2, R, Rmax_fac=3.0, bins=XB):
    """Delta Sigma(R) = mean Sigma inside the annulus' outer edge - annulus mean, bins in R / r_ta. maps: list of 2D column sums."""
    n = int(math.ceil(Rmax_fac * R / dx)) + 1
    o = np.arange(-n, n + 1); ix = (c2[0] + o) % N; iy = (c2[1] + o) % N
    rr = np.sqrt(o[:, None] ** 2 + o[None, :] ** 2).ravel() * dx
    b = np.digitize(rr / R, bins) - 1; ok = (b >= 0) & (b < len(bins) - 1)
    cnt = np.bincount(b[ok], minlength=len(bins) - 1); ccum = np.cumsum(cnt)
    out = []
    for M in maps:
        sub = M[np.ix_(ix, iy)].ravel()
        s = np.bincount(b[ok], weights=sub[ok], minlength=len(bins) - 1)
        out.append(np.where(cnt > 0, np.cumsum(s) / np.maximum(ccum, 1) - s / np.maximum(cnt, 1), np.nan))   # empty annulus -> NaN (fix 10-08)
    return np.array(out) * SIG_UNIT

RB_ENV = np.geomspace(0.1, 6.0, 25)   # Mpc/h comoving, environment-term bins (edges)
def dsig_env(Smap, delta, c, R, axis):
    """environment term around one peak: Delta Sigma of the projected field with the peak's own r_ta ball removed (delta set to 0 there)."""
    n = int(math.ceil(RB_ENV[-1] / dx)) + 1
    o = np.arange(-n, n + 1)
    a2 = [ax for ax in range(3) if ax != axis]
    i0 = (c[a2[0]] + o) % N; i1 = (c[a2[1]] + o) % N
    rr = np.sqrt(o[:, None] ** 2 + o[None, :] ** 2).ravel() * dx
    sub = Smap[np.ix_(i0, i1)].astype(np.float64)
    # subtract the ball's own column content
    nb = int(math.ceil(R / dx)) + 1; ob = np.arange(-nb, nb + 1)
    cube = delta[np.ix_((c[0] + ob) % N, (c[1] + ob) % N, (c[2] + ob) % N)].astype(np.float64)
    r3 = np.sqrt(ob[:, None, None] ** 2 + ob[None, :, None] ** 2 + ob[None, None, :] ** 2) * dx
    colb = np.where(r3 <= R, cube, 0.0).sum(axis)
    sub[n - nb:n + nb + 1, n - nb:n + nb + 1] -= colb
    s = sub.ravel()
    b = np.digitize(rr, RB_ENV) - 1; ok = (b >= 0) & (b < len(RB_ENV) - 1)
    inner = rr < RB_ENV[0]
    cnt = np.bincount(b[ok], minlength=len(RB_ENV) - 1); sm = np.bincount(b[ok], weights=s[ok], minlength=len(RB_ENV) - 1)
    ccum = np.cumsum(cnt) + inner.sum(); scum = np.cumsum(sm) + s[inner].sum()
    return np.where(cnt > 0, scum / ccum - sm / np.maximum(cnt, 1), np.nan) * SIG_UNIT   # empty annulus -> NaN (fix 10-08)

# ================================================================= run
OUT = dict(key=KEY, N=N, foot=FOOT, branch=BRANCH, dx=dx, Delta_ta=DTA, rho_m=RHOM, mutate=MUTATE, XB=XB.tolist(), YB=YB.tolist(), RB_ENV=RB_ENV.tolist(),
           files=dict(TA=os.path.basename(F_TA), S0=os.path.basename(F_S0), NC=os.path.basename(F_NC) if F_NC else None))
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

say("deposit TA")
dTA = load_delta(F_TA)
say("sources")
e, comp, comp_sh, edge, catch, lab, qC, info = sources(dTA)
OUT["info"] = info
say(f"  info {json.dumps(info)}")
js = json.load(open(F_TA.replace("_z0.npz", ".json")))["snap"]["z0"]
dq = abs(info["q_max"] / js["q_max"] - 1)
check("K1 engine q_max reproduced (<1%)", dq < 0.01, f"q_max {info['q_max']:.4f} vs engine diag {js['q_max']:.4f} (rel {dq:.1e}); overdraw {info['overdraw_mass']} vs {js['overdraw_mass']}")
check("K2 per-catchment mass conservation", abs(info["src_sum"]) < 1e-5 * max(e.sum(), 1.0) + 1.0,
      f"sum(e - comp) {info['src_sum']:.3e} vs sum e {float(e.sum()):.3e}")

idx, ron, Rg = peaks(dTA)
res = ron >= eng.RMIN_PHYS
xs = {R: eng.x_supply(R, DTA, A, BRANCH, FOOT) for R in Rg}
redge = np.array([xs[R] * R if R > 0 else 0.0 for R in ron])
cat_chk = ball_union(idx[res], ron[res]); edge_chk = ball_union(idx[res], redge[res])
m1 = float((cat_chk != catch).mean()); m2 = float((edge_chk != edge).mean())
check("K3 peak catalogue reproduces the engine's catchment and edge masks", m1 == 0 and m2 == 0, f"mismatch fractions {m1:.2e} / {m2:.2e}")
del cat_chk, edge_chk
hid = idx[res]; hR = ron[res]; hre = redge[res]; hM = 4 * math.pi / 3 * hR ** 3 * DTA * RHOM
say(f"  resolved hosts {len(hR)}; r_ON values {np.unique(hR).round(3).tolist()}; x_edge {[round(xs[R], 4) for R in np.unique(hR)]}")
OUT["x_edge_by_R"] = {f"{R:.4f}": xs[R] for R in Rg}

say("deposit S0")
dS0 = load_delta(F_S0)
dNC = load_delta(F_NC) if F_NC else None

if MUTATE:   # shuffled positions: random centres, keeping each host's r_ta and r_edge
    rng = np.random.default_rng(495)
    hid = rng.integers(0, N, size=hid.shape)

k15 = 1.5 * Om
fields = [dTA, dS0, e / k15, comp / k15, comp_sh / k15] + ([dNC] if dNC is not None else [])
fnames = ["dTA", "dS0", "de", "dc", "dcsh"] + (["dNC"] if dNC is not None else [])
del e, comp, comp_sh
# cold-fluid fractional depletion per cell: comp / s_c = q_C inside catchments
nH = len(hR)
PX = np.zeros((nH, len(fields), len(XB) - 1)); PY = np.zeros((nH, len(fields), len(YB) - 1)); OWN = np.zeros((nH, len(fields)))
qh = np.zeros(nH)
for i in range(nH):
    PX[i], PY[i], OWN[i] = prof3d(fields, hid[i], hR[i], max(hre[i], 0.5 * dx))
    l = lab[hid[i][0], hid[i][1], hid[i][2]]; qh[i] = qC[l] if l >= 0 else 0.0
say("  3D profiles done")
DS = np.zeros((nH, len(fields), len(XB) - 1))
for axis in range(3):
    maps = [F.sum(axis=axis, dtype=np.float64) for F in fields]
    a2 = [ax for ax in range(3) if ax != axis]
    for i in range(nH):
        DS[i] += dsig2d(maps, (hid[i][a2[0]], hid[i][a2[1]]), hR[i]) / 3.0   # an annulus empty in one projection is empty in all (same lattice)
    del maps
say("  projected profiles done")
OUT.update(nH=nH, fnames=fnames, checks=CHK)
np.savez_compressed(os.path.join(OUTW, f"cfg495_sim_{KEY}{TAG}.npz"), PX=PX, PY=PY, OWN=OWN, DS=DS, hR=hR, hre=hre, hM=hM, qh=qh, hid=hid)

# ---------------------------------------------------------------- environment (two-halo) term from the S0 control, isolated galaxy-scale peaks
if not MUTATE and N == 512:
    say("environment term (S0)")
    del fields, dTA, lab
    idx0, ron0, _ = peaks(dS0)
    M0 = 4 * math.pi / 3 * ron0 ** 3 * DTA * RHOM
    from scipy.spatial import cKDTree
    tree = cKDTree((idx0 + 0.5) * dx, boxsize=L)
    ENV = {}
    rng = np.random.default_rng(4950)
    classes = [R for R in np.unique(ron0) if 0.6 < R < 2.6]
    maps = [dS0.sum(axis=ax, dtype=np.float64) for ax in range(3)]
    for R in classes:
        cand = np.where(ron0 == R)[0]
        for iso_name, fac in (("iso1", 1.0), ("iso05", 0.5), ("all", None)):
            if fac is None:
                sel = cand
            else:
                keep = []
                for j in cand:
                    nb = tree.query_ball_point((idx0[j] + 0.5) * dx, 3.0)
                    if not any((k != j) and (M0[k] >= fac * M0[j]) for k in nb): keep.append(j)
                sel = np.array(keep, int)
            if len(sel) > 1500: sel = rng.choice(sel, 1500, replace=False)
            prof = np.zeros((len(sel), len(RB_ENV) - 1))
            for t_, j in enumerate(sel):
                for ax in range(3):
                    prof[t_] += dsig_env(maps[ax], dS0, idx0[j], R, ax) / 3.0
            ENV[f"{R:.4f}|{iso_name}"] = dict(R_ta=R, M_ta=4 * math.pi / 3 * R ** 3 * DTA * RHOM, n_cand=int(len(cand)), n=int(len(sel)),
                                              mean=np.nanmean(prof, 0).tolist(), sem=(np.nanstd(prof, 0) / math.sqrt(max(len(sel), 1))).tolist())
            say(f"   r_ta {R:.3f} {iso_name}: n {len(sel)} of {len(cand)}; DS_out at ~1/2/4 Mpc/h "
                f"{np.round(np.nanmean(prof, 0)[[13, 17, 21]], 3).tolist()}")
    OUT["env"] = ENV
json.dump(OUT, open(os.path.join(OUTW, f"cfg495_sim_{KEY}{TAG}.json"), "w"), indent=1)
say(f"done; checks {CHK}")
sys.exit(0 if all(CHK.values()) else 1)
