#!/usr/bin/env python3
"""G1_smooth_cap (FROZEN_CRITERIA.md, commit 9921a5172a): is the CFG555 gravitating-power excess an aliasing artefact of the
settling rule's sharp cell-wise cap  e = fsw * catch * max(s_ph - s_c, 0)  (CFG424 engine, RES, RC = 0)?

Lean, < 1 GB re-implementation of the engine's diag path (chunked streaming CIC deposit, slab-wise eigenvalues / nu_mono /
P(k)); the engine module is imported unchanged for its constants and helpers (nu_mono, eig3, catch_labels, x_supply, dta).
Old engine only: the covariant theory v3 has no settling rule and no additive QUMOND phantom (F3).

  OMP_NUM_THREADS=1 nice -n 15 python3 g1_smooth_cap.py            -> g1_smooth_cap.out, g1_smooth_cap_results.json
  G1_MUTATE=1 ...                                                    -> *_MUTATE.* (step replaced by no cap: K0 must fail)
"""
import os, sys, json, math, time, zipfile, importlib.util, resource
if os.environ.get("MallocMediumZone") != "0" or os.environ.get("MallocLargeCache") != "0":
    # macOS allocator: without these, freed 1-16 MB numpy temporaries stay resident and RSS passes 1 GB at 256^3
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, MallocMediumZone="0", MallocLargeCache="0"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy import fft as sfft

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
MUT = os.environ.get("G1_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
OUT, OUTJ = os.path.join(HERE, f"g1_smooth_cap{SUF}.out"), os.path.join(HERE, f"g1_smooth_cap_results{SUF}.json")
LINES, RES, CHECKS = [], {}, []

def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LINES.append(s)
def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # macOS: bytes
def check(name, ok, val, thr):
    CHECKS.append(bool(ok)); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")

# ---------------------------------------------------------------- engine (imported unchanged, run's own settings as in CFG555)
for k in list(os.environ):
    if k.startswith("CFG424_"): del os.environ[k]
os.environ.update({"CFG424_EPS": "0.077", "CFG424_NOCOMP": "0", "CFG424_FRET": "1.0", "CFG424_SEED": "359", "CFG424_THREADS": "1"})
_sp = importlib.util.spec_from_file_location("eng424", os.path.join(CFG, "CFG424_turnaround_catchment", "cfg424_pm.py"))
E = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(E)
E.RC = 0.0; E.MIX = "MIXA"; E.NTH = 1
L, Om, FB, EPS = E.L, E.Om, E.FB, E.EPS
DTA = E.dta_table()
SLAB = 64

# ---------------------------------------------------------------- lean mesh + I/O
class Mesh(E.Mesh):
    """engine Mesh (same kx/ky/kz/ik2/fwd/inv) with a lazily built float32 |k|."""
    def kk(self):
        return np.sqrt(self.kx ** 2 + self.ky ** 2 + self.kz ** 2)

def stream_pos(path, chunk=250_000, block=1 << 20):
    """yield float64 (n,3) chunks of pos from an npz member without loading it: raw zlib inflate into a reused buffer
    (zipfile's own reader fragments the allocator and keeps ~0.25 GB resident)."""
    import struct, zlib
    with zipfile.ZipFile(path) as z:
        zi = z.getinfo("pos.npy")
    with open(path, "rb") as f:
        f.seek(zi.header_offset); hdr = f.read(30)
        nlen, xlen = struct.unpack("<HH", hdr[26:30]); f.seek(zi.header_offset + 30 + nlen + xlen)
        left = zi.compress_size
        if zi.compress_type == zipfile.ZIP_STORED:
            dec = None
        else:
            assert zi.compress_type == zipfile.ZIP_DEFLATED; dec = zlib.decompressobj(-15)
        pend = bytearray()
        def more():
            nonlocal left
            raw = f.read(min(block, left)); left -= len(raw)
            pend.extend(dec.decompress(raw) if dec is not None else raw)
        while len(pend) < 128 and left: more()
        import io
        bio = io.BytesIO(bytes(pend[:4096]))
        ver = np.lib.format.read_magic(bio); shape, fortran, dt = np.lib.format._read_array_header(bio, ver)
        assert not fortran and shape[1] == 3
        del pend[:bio.tell()]
        n, done, rec = shape[0], 0, 3 * dt.itemsize
        buf = np.empty(chunk * 3, np.float64)
        while done < n:
            m = min(chunk, n - done)
            while len(pend) < m * rec: more()
            a = np.frombuffer(pend, dtype=dt, count=m * 3)
            out = buf[:m * 3]; out[:] = a; del a
            del pend[:m * rec]
            yield out.reshape(m, 3); done += m

def deposit_multi(path, Ms):
    """CIC deposit (engine weights, chunked; the 8 corners in one bincount per chunk) onto each mesh size in Ms."""
    rhos = {M: np.zeros(M ** 3, np.float64) for M in Ms}; npart = 0
    for pos in stream_pos(path):
        npart += pos.shape[0]
        for M in Ms:
            dx = L / M; u = pos / dx; i0 = np.floor(u).astype(np.int64); w = (u - i0).astype(np.float32); del u
            i1 = (i0 + 1) % M; i0 %= M; idx, wts = [], []
            for cx in (0, 1):
                ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
                for cy in (0, 1):
                    iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                    for cz in (0, 1):
                        iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                        idx.append((ix * M + iy) * M + iz); wts.append(wx * wy * wz)
            del i0, i1, w
            rhos[M] += np.bincount(np.concatenate(idx), weights=np.concatenate(wts), minlength=M ** 3); del idx, wts
    out = {}
    for M in Ms:
        r = rhos.pop(M); r /= r.mean(); r -= 1.0; out[M] = r.astype(np.float32).reshape((M,) * 3); del r
    return out, npart

def deposit_files(path, Ms):
    """run deposit_multi in a child process (its allocator retention dies with it); returns {M: delta}, npart."""
    import subprocess
    tmp = os.environ.get("TMPDIR", "/tmp"); base = os.path.join(tmp, f"g1_dep_{os.getpid()}")
    code = ("import os,sys,json; sys.argv=['x']; __file__=%r; "
            "exec(open(__file__).read().split('# ' + '=' * 64 + ' main')[0]); "
            "d,n=deposit_multi(%r,%r); [d[M].tofile(%r+f'_{M}.f32') for M in d]; json.dump(n,open(%r+'_n.json','w'))"
            % (os.path.abspath(__file__), path, tuple(Ms), base, base))
    subprocess.run([sys.executable, "-c", code], check=True, env=dict(os.environ))
    out = {M: np.fromfile(base + f"_{M}.f32", dtype=np.float32).reshape((M,) * 3) for M in Ms}
    n = json.load(open(base + "_n.json"))
    for M in Ms: os.remove(base + f"_{M}.f32")
    os.remove(base + "_n.json")
    return out, n

def pk(mesh, delta):
    """engine measure_pk arithmetic (CIC-deconvolved, no shot noise), slab-wise; returns k, P, sigma8."""
    M = mesh.M; dk = mesh.fwd(delta); kf = 2 * np.pi / L; edges = np.arange(0.5, M // 2 + 1, 1.0) * kf
    nb = np.zeros(len(edges) + 1); sk = np.zeros(len(edges) + 1); sp = np.zeros(len(edges) + 1); s8 = 0.0
    wyz = (np.sinc(mesh.ky * mesh.dx / (2 * np.pi)) ** 2) * (np.sinc(mesh.kz * mesh.dx / (2 * np.pi)) ** 2)
    for i in range(0, M, SLAB):
        kx = mesh.kx[i:i + SLAB]; W = (np.sinc(kx * mesh.dx / (2 * np.pi)) ** 2) * wyz
        pk3 = (np.abs(dk[i:i + SLAB]) ** 2) * L ** 3 / M ** 6 / W ** 2
        kk = np.sqrt(kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2)
        wt = np.full(pk3.shape, 2.0, np.float32); wt[..., 0] = 1.0
        if M % 2 == 0: wt[..., -1] = 1.0
        if i == 0: wt[0, 0, 0] = 0.0
        ib = np.digitize(kk.ravel(), edges); wv = wt.ravel()
        nb += np.bincount(ib, weights=wv, minlength=len(edges) + 1)
        sk += np.bincount(ib, weights=wv * kk.ravel(), minlength=len(edges) + 1)
        sp += np.bincount(ib, weights=wv * pk3.ravel(), minlength=len(edges) + 1)
        x = (kk * 8.0).astype(np.float64); x = np.where(x > 0, x, 1e-3)
        s8 += float(np.sum(wt * pk3 * (3 * (np.sin(x) - x * np.cos(x)) / x ** 3) ** 2))
    ok = nb[1:len(edges)] > 0
    kb = (sk[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]; pb = (sp[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]
    return kb, pb, math.sqrt(s8 / L ** 3)

def tophat_k(mesh, R):
    """engine tophat_k, filled slab by slab (same float32 arithmetic)."""
    out = np.empty((mesh.M, mesh.M, mesh.M // 2 + 1), np.float32)
    for i in range(0, mesh.M, SLAB):
        kr = np.sqrt(mesh.kx[i:i + SLAB] ** 2 + mesh.ky ** 2 + mesh.kz ** 2) * R; o = np.ones_like(kr); nz = kr > 1e-8
        x = kr[nz]; o[nz] = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; out[i:i + SLAB] = o
    return out

def in_cover(mesh, delta, Dta, x, a=1.0, branch="FLAT", foot="canonical"):
    """engine in_cover (cfg424_pm.py L302-338), same arithmetic, fewer simultaneous temporaries."""
    from scipy import ndimage
    M, dx = mesh.M, mesh.dx; tau = (Dta - 1.0) / 3.0
    mx = ndimage.maximum_filter(delta, size=3, mode="wrap")
    pkm = (delta == mx) & (delta >= 3 * (tau - EPS)); del mx
    if not pkm.any(): return np.zeros(delta.shape, bool)
    Rg = np.geomspace(dx, 8.0, 14)
    rhok = mesh.fwd((1.0 + delta).astype(np.float32))
    idx = np.argwhere(pkm); del pkm
    ok = np.ones(len(idx), bool); ron = np.zeros(len(idx))
    for R in Rg:
        mean = mesh.inv(rhok * tophat_k(mesh, R))[idx[:, 0], idx[:, 1], idx[:, 2]]
        ok &= mean >= Dta; ron[ok] = R
    del rhok
    res = ron >= E.RMIN_PHYS; mask = np.zeros(delta.shape, bool)
    g = np.arange(M); g = np.minimum(g, M - g) * dx
    for R in Rg[Rg >= E.RMIN_PHYS - 1e-9]:
        sel = res & (np.abs(ron - R) < 1e-9)
        if not sel.any(): continue
        pts = np.zeros(delta.shape, np.float32); pts[idx[sel, 0], idx[sel, 1], idx[sel, 2]] = 1.0
        rb = (E.x_supply(R, Dta, a, branch, foot) if x is None else x) * R
        if rb < 0.5 * dx:
            mask |= pts > 0.5; continue
        ball = ((g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2) <= rb * rb).astype(np.float32)
        conv = mesh.inv(mesh.fwd(pts) * mesh.fwd(ball)); del pts, ball
        mask |= conv > 0.5; del conv
    return mask

def fields(mesh, delta, a=1.0, branch="FLAT", foot="canonical"):
    """the engine's diag-path inputs to the cap: s_ph, s_c, fsw (x in_cover), catch mask, catchment labels."""
    D = math.exp(np.interp(math.log(1 / a), np.log1p(DTA["z"]), np.log(DTA["D"]))); tau = (D - 1.0) / 3.0
    cover = in_cover(mesh, delta, D, None, a, branch, foot)
    catch = in_cover(mesh, delta, D, 1.0, a, branch, foot)
    dk = mesh.fwd(delta)
    phik = (-1.5 * Om / a) * dk * mesh.ik2
    tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    tmp = os.environ.get("TMPDIR", "/tmp")
    fns = [os.path.join(tmp, f"g1_t{c}_{os.getpid()}.f32") for c in range(6)]     # tidal components parked on disk (plain files)
    for c, (i, j) in enumerate(tk):
        mesh.inv(mesh.kvec[i] * mesh.kvec[j] * dk * mesh.ik2).tofile(fns[c])
    del dk
    M = mesh.M; ES = 8; plane = M * M
    fsw = np.empty(delta.shape, np.float32)
    for i in range(0, M, ES):
        t6 = [np.fromfile(fn, dtype=np.float32, count=ES * plane, offset=4 * i * plane).reshape(ES, M, M) for fn in fns]
        _, l2, _ = E.eig3(t6); del t6
        fsw[i:i + ES] = np.clip(0.5 + (l2 - tau) / (2 * EPS), 0, 1).astype(np.float32)
    for fn in fns: os.remove(fn)
    fsw *= cover.astype(np.float32); del cover
    fc, fh, fs = E.MIXES[E.MIX]; kk2 = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
    kJ = lambda T: math.sqrt(1.5 * Om / a) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    Wk = (fc / (1.0 + kk2 / kJ(1e4) ** 2) + fh / (1.0 + kk2 / kJ(1e6) ** 2) + fs).astype(np.float32); del kk2
    gb = [FB * (-mesh.inv(1j * kv * phik * Wk)) for kv in mesh.kvec]; del phik
    y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (a * E.a0_code(a, branch, foot))
    w = np.empty(y.shape, np.float32)
    for i in range(0, mesh.M, SLAB):
        w[i:i + SLAB] = E.nu_mono(y[i:i + SLAB]).astype(np.float32) - 1.0
    del y
    divk = None
    for kv, g in zip(mesh.kvec, gb):
        t = 1j * kv * mesh.fwd(w * g); divk = t if divk is None else divk + t; del t
    del gb, w
    s_ph = -mesh.inv(divk); del divk
    s_c = (1.5 * Om * (1.0 - FB) / a) * (1.0 + delta)
    r, nc = E.catch_labels(catch); r = r.astype(np.int32)
    return dict(s_ph=s_ph, s_c=s_c, fsw=fsw, catch=catch, r=r, nc=nc, Wk=Wk, kJ=(kJ(1e4), kJ(1e6)))

def cap(F, kind):
    """the cell-wise excess e (before compensation)."""
    s_ph, s_c, fsw, catch = F["s_ph"], F["s_c"], F["fsw"], F["catch"]
    if MUT or kind == "nocap":
        e = fsw * s_ph
    elif kind == "step":
        e = fsw * np.maximum(s_ph - s_c, 0.0)
    elif kind == "smooth":                                     # s_ph - s_c x/(1+x), x = s_ph/s_c  (harmonic min), s_ph > 0
        sp = np.maximum(s_ph, 0.0); e = fsw * (sp * sp / np.maximum(sp + s_c, 1e-30))
    else:
        raise ValueError(kind)
    return (e * catch).astype(np.float32)

def compensate(F, e):
    """engine L412-420: src = e - s_c * (sum_catch e / sum_catch s_c)."""
    r, nc = F["r"], F["nc"]; mm = r >= 0; s_c = F["s_c"]
    E_ = np.bincount(r[mm], weights=e.ravel()[mm].astype(np.float64), minlength=nc)
    C_ = np.bincount(r[mm], weights=s_c.ravel()[mm].astype(np.float64), minlength=nc)
    q = E_ / np.maximum(C_, 1e-30)
    comp = np.zeros(e.size, np.float32); comp[mm] = (s_c.ravel()[mm] * q[r[mm]]).astype(np.float32)
    return e - comp.reshape(e.shape), E_

def renorm(F, e, E_target):
    r, nc = F["r"], F["nc"]; mm = r >= 0
    E_ = np.bincount(r[mm], weights=e.ravel()[mm].astype(np.float64), minlength=nc)
    f = np.where(E_ > 0, E_target / np.maximum(E_, 1e-300), 0.0)
    out = e.ravel().copy(); out[mm] = (out[mm] * f[r[mm]]).astype(np.float32); return out.reshape(e.shape)

def kernel(mesh, e, Wk):
    return mesh.inv(mesh.fwd(e) * Wk)

def variant_sources(mesh, F, kinds):
    """yield (name, src) one at a time (memory)."""
    e_step = cap(F, "step"); src, E_step = compensate(F, e_step); yield "a_step", src; del src
    if "b1" in kinds:
        e_s = cap(F, "smooth"); src = compensate(F, e_s)[0]; yield "b1_smooth", src; del src
        e_sn = renorm(F, e_s, E_step); del e_s
        src = compensate(F, e_sn)[0]; yield "b1n_smooth_samenorm", src; del src
        if "b3" in kinds:
            src = compensate(F, (kernel(mesh, e_sn, F["Wk"]) * F["catch"]).astype(np.float32))[0]; yield "b3_smooth_samenorm_Jeans", src; del src
        del e_sn
    if "b2" in kinds:
        src = compensate(F, (kernel(mesh, e_step, F["Wk"]) * F["catch"]).astype(np.float32))[0]; yield "b2_step_Jeans", src; del src
    if "lstar" in kinds:
        Ls = 21.7e-6 * E.h                                   # 21.7 pc in Mpc/h (D10 lower bound)
        kk2 = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
        GL = np.exp(-0.5 * kk2 * Ls ** 2).astype(np.float32); del kk2
        eL = kernel(mesh, e_step, GL); del GL
        RES.setdefault("K6", {})[f"N{mesh.M}"] = dict(Lstar_Mpch=Ls, rms_rel_change_e=float(np.sqrt(np.mean((eL - e_step) ** 2)) / np.sqrt(np.mean(e_step ** 2))))
        src = compensate(F, (eL * F["catch"]).astype(np.float32))[0]; del eL; yield "b4_step_Lstar", src; del src

def score(k, Pg, Pp, k0, P0):
    k = np.asarray(k); m = k <= 1.0; P0i = np.interp(k, k0, P0)
    rg = Pg / P0i; rp = Pp / P0i; i = int(np.argmax(np.abs(rg[m] - 1)))
    return dict(maxdev=float(np.abs(rg[m] - 1).max()), k_max=float(k[m][i]), r_grav_kmax=float(rg[m][i]), r_part_kmax=float(rp[m][i]),
                r_grav=rg.tolist(), r_part=rp.tolist())

def run_state(tag, delta, mesh, k0, P0, s80, kinds):
    t0 = time.time(); F = fields(mesh, delta)
    kb, pp, s8p = pk(mesh, delta)
    out = dict(N=mesh.M, k=kb.tolist(), s8_part=s8p, s8_part_ratio=s8p / s80, n_catch=int(F["nc"]), kJ=F["kJ"])
    sc_step = None
    for name, src in variant_sources(mesh, F, kinds):
        dg = (delta + src / (1.5 * Om)).astype(np.float32); del src; dg -= dg.mean()
        _, pg, s8g = pk(mesh, dg); del dg
        sc = score(kb, pg, pp, k0, P0); sc["s8_ratio"] = s8g / s80; sc["P_grav"] = pg.tolist()
        if name == "a_step": sc_step = sc
        i = int(np.argmin(np.abs(kb - sc_step["k_max"])))
        sc["excess_at_step_kmax"] = sc["r_grav"][i] - sc["r_part"][i]
        sc["rel_change_vs_step"] = sc["excess_at_step_kmax"] / sc_step["excess_at_step_kmax"] - 1.0 if name != "a_step" else 0.0
        out[name] = sc
        P(f"  {tag} {name:28s} max|P-1| {sc['maxdev']:.4f} at k {sc['k_max']:.3f}; s8 ratio {sc['s8_ratio']:.4f}; "
          f"excess(r_grav-r_part) at step k_max {sc['excess_at_step_kmax']:.4f} (change vs step {sc['rel_change_vs_step']:+.3f})")
    out["runtime_s"] = time.time() - t0
    del F
    P(f"  {tag}: runtime {out['runtime_s']:.0f} s, peak RSS so far {rss_gb():.2f} GB")
    return out

# ---------------------------------------------------------------- K3: direct aliasing measurement of the cap (N -> 2N -> N)
def upsample(mesh, mesh2, x):
    M, M2 = mesh.M, mesh2.M; xk = mesh.fwd(x); h = M // 2
    yk = np.zeros((M2, M2, M2 // 2 + 1), np.complex64)
    ix = np.r_[0:h, M2 - h:M2]; sx = np.r_[0:h, M - h:M]
    yk[np.ix_(ix, ix, np.arange(h))] = xk[np.ix_(sx, sx, np.arange(h))]     # Nyquist planes dropped (zero), symmetric
    return (mesh2.inv(yk) * (M2 / M) ** 3).astype(np.float32)
def downsample(mesh, mesh2, y):
    M, M2 = mesh.M, mesh2.M; yk = mesh2.fwd(y); h = M // 2
    xk = np.zeros((M, M, M // 2 + 1), np.complex64)
    ix = np.r_[0:h, M2 - h:M2]; sx = np.r_[0:h, M - h:M]
    xk[np.ix_(sx, sx, np.arange(h))] = yk[np.ix_(ix, ix, np.arange(h))]
    return (mesh.inv(xk) * (M / M2) ** 3).astype(np.float32)
def rep(x, f=2):
    return np.repeat(np.repeat(np.repeat(x, f, 0), f, 1), f, 2)

def aliasing_test(tag, delta, mesh, k0, P0):
    M2 = 2 * mesh.M; mesh2 = Mesh(M2); F = fields(mesh, delta)
    kb, pp, _ = pk(mesh, delta)
    res = {}
    # pure-interpolation control: s_ph alone (linear), N -> 2N -> N must return itself on k <= 1
    U_sph = downsample(mesh, mesh2, upsample(mesh, mesh2, F["s_ph"]))
    ctl = float(np.max(np.abs(pk(mesh, (delta + U_sph / (1.5 * Om)).astype(np.float32))[1] / pk(mesh, (delta + F["s_ph"] / (1.5 * Om)).astype(np.float32))[1] - 1)[kb <= 1.0]))
    res["linear_control_max_rel_dP_k_le_1"] = ctl; del U_sph
    P(f"  {tag} N{mesh.M}->{M2} linear control (s_ph round trip): max rel dP(k<=1) {ctl:.2e}")
    for kind in ("step", "nocap"):
        e = cap(F, kind); src_d, _ = compensate(F, e); del e
        # 2N evaluation: spectral interpolation of the smooth inputs, masks/labels replicated, cap applied at 2N
        U = dict(s_ph=upsample(mesh, mesh2, F["s_ph"]), s_c=upsample(mesh, mesh2, F["s_c"]),
                 fsw=np.clip(upsample(mesh, mesh2, F["fsw"]), 0, 1), catch=rep(F["catch"]), nc=F["nc"])
        U["r"] = rep(F["r"].reshape(F["catch"].shape)).ravel()
        e2 = cap(U, kind); src2, _ = compensate(U, e2); del e2, U
        src_u = downsample(mesh, mesh2, src2); del src2
        sc = {}
        for nm, s in (("direct_N", src_d), ("dealiased_2N", src_u)):
            dg = (delta + s / (1.5 * Om)).astype(np.float32); dg -= dg.mean(); _, pg, _ = pk(mesh, dg); del dg
            sc[nm] = score(kb, pg, pp, k0, P0)
        i = int(np.argmin(np.abs(kb - sc["direct_N"]["k_max"])))
        ex_d = sc["direct_N"]["r_grav"][i] - 1.0; ex_u = sc["dealiased_2N"]["r_grav"][i] - 1.0
        sx_d = sc["direct_N"]["r_grav"][i] - sc["direct_N"]["r_part"][i]; sx_u = sc["dealiased_2N"]["r_grav"][i] - sc["dealiased_2N"]["r_part"][i]
        # high-k: excess near Nyquist
        hk = kb >= 0.5 * math.pi * mesh.M / L
        res[kind] = dict(k_max=float(kb[i]), r_grav_minus1_direct=ex_d, r_grav_minus1_dealiased=ex_u,
                         src_excess_direct=sx_d, src_excess_dealiased=sx_u,
                         aliasing_share_of_excess=abs(ex_d - ex_u) / max(abs(ex_d), 1e-30),
                         aliasing_share_of_src_excess=abs(sx_d - sx_u) / max(abs(sx_d), 1e-30),
                         maxdev_direct=sc["direct_N"]["maxdev"], maxdev_dealiased=sc["dealiased_2N"]["maxdev"],
                         max_rel_diff_Pgrav_k_le_1=float(np.max(np.abs(np.array(sc["dealiased_2N"]["r_grav"]) / np.array(sc["direct_N"]["r_grav"]) - 1)[kb <= 1.0])),
                         max_rel_diff_Pgrav_k_ge_kNy_half=float(np.max(np.abs(np.array(sc["dealiased_2N"]["r_grav"]) / np.array(sc["direct_N"]["r_grav"]) - 1)[hk])))
        P(f"  {tag} N{mesh.M}->{M2} {kind:5s}: k_max {kb[i]:.3f}; r_grav-1 direct {ex_d:+.4f} dealiased {ex_u:+.4f}; "
          f"source excess {sx_d:+.4f} -> {sx_u:+.4f}; aliasing share {res[kind]['aliasing_share_of_excess']:.4f}; "
          f"max rel dP k<=1 {res[kind]['max_rel_diff_Pgrav_k_le_1']:.2e}, k>=kNy/2 {res[kind]['max_rel_diff_Pgrav_k_ge_kNy_half']:.2e}")
    del F
    return res

# ================================================================ main
if __name__ == "__main__":
    try: os.nice(15)
    except OSError: pass
    T0 = time.time()
    P(f"G1_smooth_cap{' (MUTATE: step -> no cap)' if MUT else ''}; engine CFG424 (imported unchanged); L = {L} Mpc/h; one thread; old engine only.")
    W424, W359, W411 = (os.path.join(EXT, d) for d in ("cfg424_work", "cfg359_work", "cfg411_work"))
    TA = os.path.join(W424, "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N256")
    R3 = os.path.join(W424, "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512")
    S0_256 = os.path.join(W359, "cfg359_S0_FLAT_canonical_N256"); S0_512 = os.path.join(W411, "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512")
    for p in (TA, R3, S0_256, S0_512):
        RES.setdefault("inputs", {})[os.path.relpath(p, EXT)] = os.path.getsize(p + "_z0.npz")
    P("inputs (bytes, _z0.npz):", json.dumps(RES["inputs"]))

    # ---------------- K1 / K2 from the record caches
    P("\n== K1/K2: where the record's gravitating excess sits, and how it scales (CFG555 caches)")
    K1 = {}
    for fn in sorted(os.listdir(os.path.join(EXT, "cfg555_work"))):
        if not fn.endswith(".json") or "S0" in fn: continue
        d = json.load(open(os.path.join(EXT, "cfg555_work", fn)))
        if d.get("switch") != "RES" or "P_grav" not in d: continue
        s0 = json.load(open(os.path.join(EXT, d["s0_base"] + ".json")))["snap"]["z0"]
        k = np.array(d["k"]); P0i = np.interp(k, s0["k"], s0["P"]); rg = np.array(d["P_grav"]) / P0i; rp = np.array(d["P_part"]) / P0i
        N, Lb = d["N"], (200.0); kny = math.pi * N / Lb; m = k <= 1.0; i = int(np.argmax(np.abs(rg[m] - 1)))
        hk = k >= 0.5 * kny
        K1[d["name"]] = dict(N=N, k_Ny=kny, k_max=float(k[m][i]), k_max_over_kNy=float(k[m][i] / kny), maxdev=float(abs(rg[m][i] - 1)),
                             src_excess_kmax=float(rg[m][i] - rp[m][i]),
                             max_abs_rgrav_minus_rpart_k_ge_kNy_half=float(np.max(np.abs(rg[hk] - rp[hk]))) if hk.any() else None,
                             rgrav_minus_rpart_at_k_0p32=float(np.interp(0.32, k, rg - rp)),
                             Psrc_over_Ppart_at=[[float(f), float(np.interp(f * kny, k, np.array(d["P_src"]) / np.array(d["P_part"])))] for f in (0.04, 0.1, 0.25, 0.5, 0.9)])
    for n, v in K1.items():
        P(f"  {n:28s} N{v['N']}: max|P-1| {v['maxdev']:.3f} at k {v['k_max']:.2f} = {v['k_max_over_kNy']:.3f} k_Ny; source excess there {v['src_excess_kmax']:+.3f}; "
          f"|r_grav-r_part| max at k>=k_Ny/2 {v['max_abs_rgrav_minus_rpart_k_ge_kNy_half']:.3f}; P_src/P_part at k/k_Ny 0.1, 0.5, 0.9: "
          + ", ".join(f"{x[1]:.3g}" for x in v["Psrc_over_Ppart_at"] if x[0] in (0.1, 0.5, 0.9)))
    RES["K1"] = K1
    lowk = all(v["k_max_over_kNy"] < 0.25 for v in K1.values())
    check("K1", len(K1) >= 10, f"{len(K1)} runs; max k_max/k_Ny {max(v['k_max_over_kNy'] for v in K1.values()):.3f}; all < 0.25: {lowk}", ">= 10 runs read")
    ta, r3 = K1["424_TAcan"], K1["425_R3_can_512"]
    RES["K2"] = dict(src_excess_k0p32_256=ta["rgrav_minus_rpart_at_k_0p32"], src_excess_k0p32_512=r3["rgrav_minus_rpart_at_k_0p32"],
                     ratio_512_over_256=r3["rgrav_minus_rpart_at_k_0p32"] / ta["rgrav_minus_rpart_at_k_0p32"],
                     aliasing_expectation="falls with N at fixed k (folded images move from 2k_Ny-k to 4k_Ny-k)")
    check("K2", True, f"source excess at k 0.32: 256^3 {ta['rgrav_minus_rpart_at_k_0p32']:.4f} -> 512^3 {r3['rgrav_minus_rpart_at_k_0p32']:.4f} "
          f"(x{RES['K2']['ratio_512_over_256']:.2f}; aliasing would fall)", "computed")

    s0j = json.load(open(S0_256 + ".json"))["snap"]["z0"]; k0, P0, s80 = np.array(s0j["k"]), np.array(s0j["P"]), s0j["sigma8"]
    rec = json.load(open(os.path.join(EXT, "cfg555_work", "cfg555_424_TAcan.json")))

    # ---------------- K0 + K4 + K6: TA-can 256^3 state on its own grid
    P("\n== K0/K4/K6: TA-can 256^3 state on the 256^3 grid (record grid)")
    d256, np256 = deposit_files(TA + "_z0.npz", (256, 128))
    mesh256 = Mesh(256)
    R = run_state("TA256@256", d256[256], mesh256, k0, P0, s80, ("b1", "b2", "b3", "lstar"))
    RES["K4_TA256_at_256"] = {k_: (v if not isinstance(v, dict) else {a: b for a, b in v.items() if a not in ("r_grav", "r_part", "P_grav")}) for k_, v in R.items()}
    Pg_rec = np.array(rec["P_grav"]); kr = np.array(rec["k"]); m = kr <= 1.0
    dev = float(np.max(np.abs(np.array(R["a_step"]["P_grav"])[m] / Pg_rec[m] - 1)))
    devp = float(np.max(np.abs(np.interp(kr[m], R["k"], pk(mesh256, d256[256])[1]) / np.array(rec["P_part"])[m] - 1)))
    RES["K0"] = dict(max_rel_dev_Pgrav_k_le_1=dev, max_rel_dev_Ppart=devp, maxdev=R["a_step"]["maxdev"], k_max=R["a_step"]["k_max"],
                     record_maxdev=0.0749, record_r_grav_0p35=1.0749, r_grav_kmax=R["a_step"]["r_grav_kmax"], n_catch=R["n_catch"])
    ok0 = dev <= 1e-4 and abs(R["a_step"]["r_grav_kmax"] - 1.0749) <= 1e-3
    check("K0", ok0, f"P_grav vs CFG555 cache max rel dev {dev:.2e} (P_part {devp:.1e}); max|P-1| {R['a_step']['maxdev']:.4f} at k {R['a_step']['k_max']:.3f}; "
          f"r_grav {R['a_step']['r_grav_kmax']:.4f}; catchments {R['n_catch']}", "<= 1e-4 and |r_grav-1.0749| <= 1e-3")
    sm = {k_: abs(R[k_]["rel_change_vs_step"]) for k_ in ("b1n_smooth_samenorm", "b2_step_Jeans", "b3_smooth_samenorm_Jeans")}
    RES["K4_S"] = max(sm.values())
    check("K4", True, "excess change vs step at k_max: " + ", ".join(f"{a} {R[a]['rel_change_vs_step']:+.3f}" for a in
          ("b1_smooth", "b1n_smooth_samenorm", "b2_step_Jeans", "b3_smooth_samenorm_Jeans", "b4_step_Lstar")) + f"; S = {RES['K4_S']:.3f}", "computed")
    k6 = RES["K6"]["N256"]["rms_rel_change_e"]
    check("K6", k6 < 1e-3, f"L* Gaussian (21.7 pc) rms rel change of e at 256^3 {k6:.2e}", "< 1e-3")
    del R

    # ---------------- K3: aliasing of the cap measured directly (128 -> 256 -> 128), TA-can state
    P("\n== K3: direct aliasing measurement of the cap, TA-can 256^3 state deposited at 128^3 (2N = 256)")
    mesh128 = Mesh(128)
    # S0 at 128 for the ratio (same deposit)
    s0d, _ = deposit_files(S0_256 + "_z0.npz", (128,))
    k0_128, P0_128, _ = pk(mesh128, s0d[128]); del s0d
    A_TA = aliasing_test("TA256@128", d256[128], mesh128, k0_128, P0_128)
    del d256

    # ---------------- K5: the 512^3 state (R3) on the 256^3 and 128^3 operator grids
    P("\n== K5: R3 512^3 state on the 256^3 operator grid (and K3 at 128^3)")
    s0d, _ = deposit_files(S0_512 + "_z0.npz", (256, 128))
    k0_5_256, P0_5_256, s80_5_256 = pk(mesh256, s0d[256]); k0_5_128, P0_5_128, _ = pk(mesh128, s0d[128]); del s0d
    d512, np512 = deposit_files(R3 + "_z0.npz", (256, 128))
    R5 = run_state("R3_512@256", d512[256], mesh256, k0_5_256, P0_5_256, s80_5_256, ("b1", "b2", "b3"))
    RES["K5_R3_512_at_256"] = {k_: (v if not isinstance(v, dict) else {a: b for a, b in v.items() if a not in ("r_grav", "r_part", "P_grav")}) for k_, v in R5.items()}
    check("K5", True, f"R3 512^3 state at 256^3 grid: step max|P-1| {R5['a_step']['maxdev']:.4f} at k {R5['a_step']['k_max']:.3f} "
          f"(record at 512^3 grid 0.163); b1n {R5['b1n_smooth_samenorm']['maxdev']:.4f}, b2 {R5['b2_step_Jeans']['maxdev']:.4f}, b3 {R5['b3_smooth_samenorm_Jeans']['maxdev']:.4f}", "computed")
    A_R3 = aliasing_test("R3_512@128", d512[128], mesh128, k0_5_128, P0_5_128)
    del d512
    RES["K3"] = dict(TA256_at_128=A_TA, R3_512_at_128=A_R3)
    A = max(A_TA["step"]["aliasing_share_of_excess"], A_R3["step"]["aliasing_share_of_excess"])
    ctrl = max(A_TA["linear_control_max_rel_dP_k_le_1"], A_R3["linear_control_max_rel_dP_k_le_1"])
    RES["K3_A"] = A
    check("K3", ctrl <= 1e-5, f"aliasing share of the excess at k_max (step): TA {A_TA['step']['aliasing_share_of_excess']:.4f}, R3 {A_R3['step']['aliasing_share_of_excess']:.4f}; "
          f"linear round-trip control max rel dP(k<=1) {ctrl:.1e}", "control <= 1e-5")

    # ---------------- verdict (FROZEN_CRITERIA §5)
    S = RES["K4_S"]; s5 = min(R5["b1n_smooth_samenorm"]["maxdev"], R5["b2_step_Jeans"]["maxdev"])
    if A >= 0.5 or (S >= 0.5 and s5 < 0.10): V = "ARTEFACT"
    elif A < 0.2 and S < 0.2 and lowk: V = "PHYSICAL (old engine)"
    else: V = "MIXED"
    RES["verdict"] = dict(verdict=V, A=A, S=S, low_k=lowk, K5_best_smooth_maxdev=s5)
    P(f"\nVERDICT (FROZEN §5): {V}  [A = {A:.4f}, S = {S:.3f}, low-k = {lowk}, K5 best smooth max|P-1| {s5:.4f}]")
    RES["peak_rss_gb"] = rss_gb(); RES["runtime_s"] = time.time() - T0
    P(f"peak RSS {RES['peak_rss_gb']:.2f} GB; runtime {RES['runtime_s']:.0f} s")
    n = sum(CHECKS); P(f"G1_SMOOTH_CAP COMPLETE: {n}/{len(CHECKS)} checks PASS.")
    json.dump(RES, open(OUTJ, "w"), indent=1); open(OUT, "w").write("\n".join(LINES) + "\n")
    sys.exit(0 if n == len(CHECKS) else 1)
