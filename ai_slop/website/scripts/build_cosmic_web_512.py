"""Build the /cosmic-web assets from the record's 512^3 particle-mesh snapshots (CFG425 R3 vs its Newtonian control).

Inputs (read-only, outside the repo; ~1.6 GB each):
  _external_data/cfg424_work/cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512{,_z0.npz}    framework run (CFG425 R3, seed 359)
  _external_data/cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512{,_z0.npz}                    Newtonian + Lambda control (same ICs)
Each npz holds pos (134,217,728 x 3, float32, Mpc/h in a 200 Mpc/h box), f (the T1 switch field, 512^3 float16) and l3.
Row i of pos is the same simulation particle in both runs (same initial conditions), so particles can be compared one by one.

Outputs (public/data/cosmic512/), kept small on purpose (Firebase transfer):
  vol128_{res,s0}.u8.gz, swi128.u8.gz   log10 CIC density block-averaged 4x from the 512^3 grid, 0..255 over [LOG_LO, LOG_HI]; switch field f 0..255
  layers_{res,s0}.png, layers_swi.png    16 full-resolution layers (every 32nd z cell) of the 512^3 particle counts: a 4 x 4 atlas of 512 x 512 cells,
                                         uint8 count code c for c <= 127, else 127 + round(16 log2(c/127)); the switch atlas is f * 255
  halo_XX.bin                            every 8th particle inside r < 3 Mpc/h of 12 halos: Int16 x3 framework, Int16 x3 control (same particle ids),
                                         Uint8 switch value; positions relative to the halo centre in units of HALO_SCALE/32767 Mpc/h.
                                         meta.json holds radial counts of ALL particles of each run about that run's own halo centre
  meta.json                              box, encodings, P(k) of both runs, per-halo table, particle-by-particle comparison, and this script's checks
The exact per-cell counts of all 134M particles stay in the cache directory (not hosted).

Checks asserted: CIC mass = 134217728, mean density = 1, measured sigma8 within 1.5% of each run's recorded sigma8, counts sum to 134217728.
Run from the repo root: python3 ai_slop/website/scripts/build_cosmic_web_512.py [--cache DIR] [--keep-volumes]
--keep-volumes re-runs only the particle comparison and halo stages and leaves the volume files in place.
The deposit and count stages are cached (512^3 arrays) so re-encoding does not repeat them.
"""
import gzip, json, os, sys, time
import numpy as np
from PIL import Image
from scipy import ndimage

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
RUNS = {
    "res": os.path.join(EXT, "cfg424_work", "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512"),
    "s0": os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512"),
}
OUT = os.path.join(REPO, "ai_slop", "website", "public", "data", "cosmic512")
N, L = 512, 200.0
LOG_LO, LOG_HI = -1.5, 2.5          # log10 of rho/rho_bar mapped to 0..255 in the preview volumes
HALO_R, HALO_SCALE = 3.0, 4.0       # Mpc/h: selection radius, and full scale of the int16 positions (control particles may stray past R)
HALO_RANKS = list(range(10)) + [29, 59]
HALO_STRIDE = 8                                            # ship every 8th particle of each halo
PROF_LO, PROF_BINS = 0.04, 16                              # profile shells, Mpc/h
H, OM_B, OM_C = 0.6736, 0.02237, 0.1200                  # engine constants (cfg424_pm.py)
RHO_CRIT = 2.77536627e11                                  # (Msun/h) / (Mpc/h)^3
M_P = (OM_B + OM_C) / H ** 2 * RHO_CRIT * (L / N) ** 3   # total-matter mass per particle, Msun/h
cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else os.path.join(EXT, "cosmic_web_512_cache")
os.makedirs(cache, exist_ok=True); os.makedirs(OUT, exist_ok=True)
KEEP_VOLUMES = "--keep-volumes" in sys.argv                # re-run only the halo / comparison stages
for fn in os.listdir(OUT):                                 # drop assets of earlier layouts
    if fn.startswith(("vol256", "slabs_", "swi256", "swi512", "cnt512", "halo_", "layers_")) or (not KEEP_VOLUMES and fn.startswith(("vol128", "swi"))):
        os.remove(os.path.join(OUT, fn))


def cic(pos, n, box, chunk=1 << 25):
    """cloud-in-cell deposit of n^3 mean-1 density from (M,3) positions."""
    grid = np.zeros(n ** 3, np.float32)
    s = n / box
    for a in range(0, len(pos), chunk):
        u = pos[a:a + chunk].astype(np.float64) * s
        i0 = np.floor(u).astype(np.int64); d = u - i0
        for cx in (0, 1):
            wx = d[:, 0] if cx else 1 - d[:, 0]
            for cy in (0, 1):
                wy = d[:, 1] if cy else 1 - d[:, 1]
                for cz in (0, 1):
                    wz = d[:, 2] if cz else 1 - d[:, 2]
                    idx = (((i0[:, 0] + cx) % n) * n + (i0[:, 1] + cy) % n) * n + (i0[:, 2] + cz) % n
                    grid += np.bincount(idx, weights=wx * wy * wz, minlength=n ** 3).astype(np.float32)
    return grid.reshape(n, n, n)


def cells_of(pos, chunk=1 << 25):
    """flat nearest-grid-point cell index of every particle (int64)."""
    out = np.empty(len(pos), np.int64)
    for a in range(0, len(pos), chunk):
        c = np.floor(pos[a:a + chunk].astype(np.float64) * (N / L)).astype(np.int64) % N
        out[a:a + chunk] = (c[:, 0] * N + c[:, 1]) * N + c[:, 2]
    return out


def sigma_R(rho, box, R=8.0):
    """sigma(R) of the mean-1 density with a k-space top hat (no window deconvolution; CIC bias is < 0.5% at these k)."""
    n = rho.shape[0]
    dk = np.fft.rfftn(rho / rho.mean() - 1.0) / n ** 3
    k1 = 2 * np.pi * np.fft.fftfreq(n, box / n); kz = 2 * np.pi * np.fft.rfftfreq(n, box / n)
    k = np.sqrt(k1[:, None, None] ** 2 + k1[None, :, None] ** 2 + kz[None, None, :] ** 2)
    x = np.maximum(k * R, 1e-8)
    w = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    wt = np.full(dk.shape, 2.0, np.float64); wt[:, :, 0] = 1.0; wt[:, :, -1] = 1.0
    return float(np.sqrt(np.sum(wt * np.abs(dk * w) ** 2)))


def block(a, f):
    n = a.shape[0] // f
    return a.reshape(n, f, n, f, n, f).mean(axis=(1, 3, 5))


def enc(a):
    return np.clip(np.round((np.log10(np.maximum(a, 1e-6)) - LOG_LO) / (LOG_HI - LOG_LO) * 255), 0, 255).astype(np.uint8)


def code_counts(c):
    c = c.astype(np.float32)
    return np.clip(np.where(c <= 127, c, 127 + np.round(16 * np.log2(np.maximum(c, 1) / 127))), 0, 255).astype(np.uint8)


def gz(path, arr):
    with gzip.GzipFile(path, "wb", compresslevel=9, mtime=0) as f:
        f.write(np.ascontiguousarray(arr).tobytes())
    return os.path.getsize(path)


_pos = {}
def getpos(key):
    if key not in _pos:
        t0 = time.time(); z = np.load(RUNS[key] + "_z0.npz"); p = z["pos"]
        assert p.shape == (N ** 3, 3)
        _pos[key] = [np.ascontiguousarray(p[:, i]) for i in range(3)]; del p
        print(f"[{key}] positions loaded in {time.time() - t0:.0f}s", flush=True)
    return _pos[key]


# ---------------------------------------------------------------- 1. deposit + counts (cached)
rho, cnt, rec, checks = {}, {}, {}, {}
for key, base in RUNS.items():
    cp, np_ = os.path.join(cache, f"rho_{key}.npy"), os.path.join(cache, f"cnt_{key}.npy")
    if not os.path.exists(cp) or not os.path.exists(np_):
        t0 = time.time(); z = np.load(base + "_z0.npz"); pos = z["pos"]
        assert pos.shape == (N ** 3, 3)
        np.save(cp, cic(pos, N, L))
        np.save(np_, np.bincount(cells_of(pos), minlength=N ** 3).astype(np.int32).reshape(N, N, N))
        if key == "res":
            np.save(os.path.join(cache, "swi_res.npy"), z["f"].astype(np.float32))
        del pos, z
        print(f"[{key}] deposited in {time.time() - t0:.0f}s", flush=True)
    rho[key], cnt[key] = np.load(cp), np.load(np_)
    j = json.load(open(base + ".json")); s = j["snap"]["z0"]
    rec[key] = dict(tag=j["tag"], sigma8=s["sigma8"], k=s["k"], P=s["P"], runtime_s=j["runtime_s"], L=j["L"], z_i=j["z_i"], nsteps=j["nsteps"],
                    **{q: s[q] for q in ("vol_on", "mass_on", "vol_on_knot", "vol_on_fil", "mass_on_knot", "mass_on_fil") if q in s})
    mass, mean = float(rho[key].sum(dtype=np.float64)), float(rho[key].mean(dtype=np.float64))
    s8 = sigma_R(rho[key], L)
    checks[key] = dict(mass=mass, mean=mean, sigma8_grid=s8, sigma8_record=s["sigma8"], rel=s8 / s["sigma8"] - 1,
                       count_sum=int(cnt[key].sum(dtype=np.int64)), count_max=int(cnt[key].max()), frac_cells_empty=float((cnt[key] == 0).mean()),
                       frac_particles_in_cells_gt_127=float(cnt[key][cnt[key] > 127].sum(dtype=np.int64) / N ** 3))
    print(f"[{key}] CIC mass {mass:.0f}  mean {mean:.6f}  sigma8 grid {s8:.4f} vs record {s['sigma8']:.4f} ({100 * (s8 / s['sigma8'] - 1):+.2f}%)  "
          f"counts sum {checks[key]['count_sum']}  max {checks[key]['count_max']}", flush=True)
    assert abs(mass - N ** 3) < 2 and abs(mean - 1) < 1e-5, "CIC mass not conserved"
    assert checks[key]["count_sum"] == N ** 3, "counts do not sum to the particle number"
    assert abs(checks[key]["rel"]) < 0.015, "grid sigma8 disagrees with the run's recorded sigma8"
swi = np.load(os.path.join(cache, "swi_res.npy"))

# ---------------------------------------------------------------- 2. encode volumes
sizes = {}
LAYERS = [16 + 32 * i for i in range(16)]                        # z cells of the full-resolution layers
if KEEP_VOLUMES:
    ls = lambda pre: sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.startswith(pre))
    sizes = {"vol128_res": ls("vol128_res"), "vol128_s0": ls("vol128_s0"), "swi128": ls("swi128")}
else:
    for key in ("res", "s0"):
        sizes[f"vol128_{key}"] = gz(os.path.join(OUT, f"vol128_{key}.u8.gz"), enc(block(rho[key], 4)))
    sizes["swi128"] = gz(os.path.join(OUT, "swi128.u8.gz"), np.clip(np.round(block(swi, 4) * 255), 0, 255).astype(np.uint8))

def atlas(layers, path):
    img = np.zeros((4 * N, 4 * N), np.uint8)
    for k, im in enumerate(layers):
        r, c = divmod(k, 4); img[r * N:(r + 1) * N, c * N:(c + 1) * N] = im
    Image.fromarray(img).save(path, optimize=True); return os.path.getsize(path)

for key in ("res", "s0"):
    sizes[f"layers_{key}"] = atlas([code_counts(cnt[key][:, :, z]) for z in LAYERS], os.path.join(OUT, f"layers_{key}.png"))
sizes["layers_swi"] = atlas([np.clip(np.round(swi[:, :, z] * 255), 0, 255).astype(np.uint8) for z in LAYERS], os.path.join(OUT, "layers_swi.png"))
print({k: f"{v / 1e6:.1f} MB" for k, v in sizes.items()}, flush=True)

# ---------------------------------------------------------------- 3. field-level numbers
r128, r128s = block(rho["res"], 4), block(rho["s0"], 4)
both = (r128 > 0) & (r128s > 0)                                                  # cells empty in either run have no finite log ratio
diff = np.log10(r128[both]) - np.log10(r128s[both])
by_density = {}
for lo, hi in ((0, 1), (1, 3), (3, 10), (10, 100), (100, 1e12)):
    mk = (r128 >= lo) & (r128 < hi) & both
    dd = np.log10(r128[mk]) - np.log10(r128s[mk])
    by_density[f"{lo:g}-{hi:g}" if hi < 1e12 else f">={lo:g}"] = dict(frac_cells=float(mk.mean()), mean_dlog10=float(dd.mean()), rms_dlog10=float(np.sqrt(np.mean(dd ** 2))))
kk = np.array(rec["res"]["k"]); m = kk <= 1
pr = np.array(rec["res"]["P"])[m] / np.interp(kk[m], np.array(rec["s0"]["k"]), np.array(rec["s0"]["P"]))
stats = dict(
    corr_log_density_128=float(np.corrcoef(np.log10(r128[both]), np.log10(r128s[both]))[0, 1]),
    rms_dlog10_128=float(np.sqrt(np.mean(diff ** 2))),
    frac_cells_within_0p1dex_128=float(np.mean(np.abs(diff) < 0.1)),
    frac_cells_empty_in_either_128=float(1 - both.mean()),
    by_density_128=by_density,
    s8_ratio=rec["res"]["sigma8"] / rec["s0"]["sigma8"], pk_max_dev=float(np.max(np.abs(pr - 1))),
    frac_volume_rho_gt_100_512={k: float(np.mean(rho[k] > 100)) for k in rho},
    frac_mass_rho_gt_100_512={k: float(rho[k][rho[k] > 100].sum() / rho[k].sum()) for k in rho},
)

# ---------------------------------------------------------------- 4. particle by particle: framework vs control (same row = same particle)
def minimg(d):
    d -= np.float32(L) * np.rint(d / np.float32(L)); return d

px, qx = getpos("res"), getpos("s0")
EDGES = np.geomspace(1e-4, 20.0, 161)
hist = np.zeros(len(EDGES) + 1); hist_cls = {c: np.zeros(len(EDGES) + 1) for c in ("c0-2", "c3-30", "c31+")}
cflat = cnt["res"].reshape(-1)
for a in range(0, N ** 3, 1 << 24):
    sl = slice(a, a + (1 << 24))
    dx = [minimg(px[i][sl] - qx[i][sl]) for i in range(3)]
    r = np.sqrt(dx[0] ** 2 + dx[1] ** 2 + dx[2] ** 2)
    c = cflat[cells_of(np.stack([px[0][sl], px[1][sl], px[2][sl]], 1))]
    b = np.searchsorted(EDGES, r)
    hist += np.bincount(b, minlength=len(EDGES) + 1)
    for name, mk in (("c0-2", c <= 2), ("c3-30", (c > 2) & (c <= 30)), ("c31+", c > 30)):
        hist_cls[name] += np.bincount(b[mk], minlength=len(EDGES) + 1)

def pct(h, q):
    cdf = np.cumsum(h) / h.sum(); i = int(np.searchsorted(cdf, q)); return float(EDGES[min(max(i - 1, 0), len(EDGES) - 1)])
particle_cmp = dict(
    n=int(hist.sum()), median_mpc_h=pct(hist, 0.5), p90_mpc_h=pct(hist, 0.9), p99_mpc_h=pct(hist, 0.99), p999_mpc_h=pct(hist, 0.999),
    frac_gt_cell=float(hist[np.searchsorted(EDGES, L / N) + 1:].sum() / hist.sum()),
    by_framework_cell_count={k: dict(n=int(h.sum()), frac=float(h.sum() / hist.sum()), median_mpc_h=pct(h, 0.5), p90_mpc_h=pct(h, 0.9)) for k, h in hist_cls.items()},
    cell_mpc_h=L / N)
print("particle displacement between runs:", json.dumps(particle_cmp)[:400], flush=True)
assert particle_cmp["median_mpc_h"] < 0.5, "row i is not the same particle in both runs"

# ---------------------------------------------------------------- 5. halos: the real particles
sm = ndimage.uniform_filter(cnt["res"].astype(np.float32), size=8, mode="wrap")
peaks = []
for _ in range(max(HALO_RANKS) + 1):
    i = np.unravel_index(int(np.argmax(sm)), sm.shape); peaks.append((float(sm[i]), i))
    ex = [np.arange(i[a] - 20, i[a] + 21) % N for a in range(3)]
    sm[np.ix_(*ex)] = 0
del sm

def sphere(cols, c, R, ids=None):
    """indices (into cols) of particles with min-image distance < R from c."""
    ix = np.flatnonzero(np.abs(minimg(cols[0] - np.float32(c[0]))) < R)
    for a in (1, 2):
        ix = ix[np.abs(minimg(cols[a][ix] - np.float32(c[a]))) < R]
    d = np.stack([minimg(cols[a][ix] - np.float32(c[a])) for a in range(3)], 1)
    k = (d ** 2).sum(1) < R * R
    return ix[k], d[k]

fgrid = swi.reshape(-1)
halos = []
for rank in HALO_RANKS:
    mbox, i = peaks[rank]
    c = (np.array(i, np.float64) + 0.5) * (L / N)
    for _ in range(3):                                           # shrinking-sphere centre
        ix, d = sphere(px, c, HALO_R); c = (c + d.mean(0)) % L
    ix, d = sphere(px, c, HALO_R)
    dq = np.stack([minimg(qx[a][ix] - np.float32(c[a])) for a in range(3)], 1)           # same particles, control run
    dd = np.sqrt(((d - dq) ** 2).sum(1))
    cs = c.copy()
    for _ in range(3):                                           # the control run's own centre
        _, dcs = sphere(qx, cs, HALO_R); cs = (cs + dcs.mean(0)) % L
    ixq, dall = sphere(qx, cs, HALO_R)
    pedges = np.geomspace(PROF_LO, HALO_R, PROF_BINS + 1)
    prof_fw = np.histogram(np.sqrt((d ** 2).sum(1)), pedges)[0]
    prof_s0 = np.histogram(np.sqrt((dall ** 2).sum(1)), pedges)[0]
    dcen = minimg((cs - c).astype(np.float32))
    pf = np.stack([px[0][ix], px[1][ix], px[2][ix]], 1)
    f8 = np.clip(np.round(fgrid[cells_of(pf)] * 255), 0, 255).astype(np.uint8)
    hid = f"H{len(halos) + 1:02d}"
    q = lambda a: np.clip(np.round(a / HALO_SCALE * 32767), -32767, 32767).astype("<i2")
    with open(os.path.join(OUT, f"halo_{hid}.bin"), "wb") as fh:
        fh.write(q(d[::HALO_STRIDE]).tobytes()); fh.write(q(dq[::HALO_STRIDE]).tobytes()); fh.write(f8[::HALO_STRIDE].tobytes())
    halos.append(dict(id=hid, rank=rank + 1, centre=[float(x) for x in c], n=int(len(ix)), n_control_sphere=int(len(ixq)),
                      mass_msun_h=float(len(ix) * M_P), mass_control_msun_h=float(len(ixq) * M_P),
                      moved_median_kpc_h=float(np.median(dd) * 1e3), moved_rms_kpc_h=float(np.sqrt(np.mean(dd ** 2)) * 1e3),
                      frac_switch_on=float((f8 > 127).mean()), n_shown=int(len(ix[::HALO_STRIDE])), bytes=int(len(ix[::HALO_STRIDE]) * 13),
                      centre_s0=[float(x) for x in cs], centre_offset_kpc_h=float(np.sqrt((dcen ** 2).sum()) * 1e3),
                      prof_edges=[float(x) for x in pedges], prof_fw=[int(x) for x in prof_fw], prof_s0=[int(x) for x in prof_s0]))
    print(f"  {hid} n={len(ix)} M={len(ix) * M_P:.2e} Msun/h  control sphere n={len(ixq)}  median move {np.median(dd) * 1e3:.0f} kpc/h  on={halos[-1]['frac_switch_on']:.2f}", flush=True)

meta = dict(N=N, L=L, log_lo=LOG_LO, log_hi=LOG_HI, halo_r=HALO_R, halo_scale=HALO_SCALE, halo_stride=HALO_STRIDE, layers=LAYERS, m_particle_msun_h=M_P, rec=rec, checks=checks, stats=stats,
            particle_cmp=particle_cmp, halos=halos, bytes=sizes, count_code="c<=127: c ; else 127*2^((code-127)/16)",
            source="campaign_fresh_gravity/CFG425_turnaround_catchment_confirm (R3) vs the cfg411 S0 control; engine CFG424_turnaround_catchment/cfg424_pm.py")
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
print("total public bytes:", sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) / 1e6, "MB")
