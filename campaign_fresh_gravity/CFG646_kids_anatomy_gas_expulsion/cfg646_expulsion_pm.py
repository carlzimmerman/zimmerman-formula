#!/usr/bin/env python3
"""CFG646 (ii) estimate 2: PM-NATIVE post-process of the census gas expulsion (DECLARATIONS.md 3c1c5a42f).

On a run's own 256^3 fields (CFG596 P1: block means of the 1024^3 particle and gravitating fields at z = 0, 0.5, 1;
CFG530 L100 N512 cross-check: its z = 0 gravitating field block-meaned x2 and its z = 0 particles CIC-deposited at 256^3),
the engine's own catchment routines (cfg596_pm.cover_peaks / cover_balls / catch_labels, imported unchanged, RMIN 0.78125,
census fret_of, Delta_ta(z) table, flat a0 of the footing) are re-run at 256^3 on the particle field.  Then

    e(x)  = f_b (1 - f_ret(x)) (1 + delta_part(x))           (the census non-retained baryons the PM keeps as collisionless mass)
    delta_grav' = delta_grav - e + placement(sum e)

  DIFF-S  (the grid realisation of the DECLARED PRIMARY, CFG632 DIFF: no one-halo profile, host large-scale bias kept, mass conserved):
          each catchment class's e Gaussian-smoothed with sigma = its catchment radius R;
  DIFF-F  (bracket): re-placed in proportion to the matter outside every catchment (diffuse, field-clustered; its large-scale
          bias turns out ~ 0, so it behaves like DIFF-U).  [2026-10-12 disclosure: an earlier draft of this docstring, written
          before any number, called DIFF-F the grid primary; DECLARATIONS.md (3c1c5a42f) fixes the primary as CFG632 DIFF with the
          host bias, which DIFF-S realises and DIFF-F does not.  DIFF-F is the MORE favourable to the framework.]
  DIFF-U  (bracket, maximal removal): uniform;
  SHELL   (bracket): per connected catchment, into its own shell cells (catchment AND NOT census edge) in proportion to (1 + delta_part).
Reported: P'(k)/P(k) of the gravitating field (same estimator for both, so the window cancels), at every node z.
Resolution-limited (catchments rebuilt on a 4x / 2x coarser mesh than the engine's); an ESTIMATE, not a verdict.
  nice -n 10 python3 cfg646_expulsion_pm.py [P1|530can|530alt ...]   -> cfg646_expulsion_pm.out / .json (merged per source)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, time, importlib.util
SCR = os.environ.get("CFG646_SCRATCH", "/tmp")
os.environ.update(CFG596_L="100", CFG596_RMIN="0.78125", CFG596_THREADS="2", CFG596_WORK=SCR, CFG596_SPILL="0", CFG596_RELIEF="1")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "2"
import numpy as np
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(CFG, "..", "..", "_external_data"))
spec = importlib.util.spec_from_file_location("cfg596_pm", os.path.join(CFG, "CFG596_lean_pm_1024", "cfg596_pm.py"))
PM = importlib.util.module_from_spec(spec); spec.loader.exec_module(PM)
assert PM.L == 100.0 and PM.RMIN_PHYS == 0.78125 and PM.FRET_MODE == "census"
FB = PM.FB; M = 256; L = 100.0
OUTF = os.path.join(HERE, "cfg646_expulsion_pm.json"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

def pk(delta):
    dk = np.fft.rfftn(delta.astype(np.float64)); kf = 2 * np.pi / L
    k1 = np.fft.fftfreq(M, 1.0 / M); kz = np.fft.rfftfreq(M, 1.0 / M)
    kk = np.sqrt(k1[:, None, None] ** 2 + k1[None, :, None] ** 2 + kz[None, None, :] ** 2)
    wt = np.full(dk.shape, 2.0); wt[..., 0] = 1.0; wt[..., -1] = 1.0; wt[0, 0, 0] = 0.0
    ib = np.rint(kk).astype(int).ravel(); p3 = (np.abs(dk) ** 2).ravel() * L ** 3 / M ** 6
    n = np.bincount(ib, wt.ravel(), M); s = np.bincount(ib, wt.ravel() * p3, M); kb = np.bincount(ib, wt.ravel() * kk.ravel(), M)
    m = n > 0
    return (kb[m] / n[m]) * kf, s[m] / n[m]

def gsmooth(x, sig):
    k1 = 2 * np.pi * np.fft.fftfreq(M, L / M); kz = 2 * np.pi * np.fft.rfftfreq(M, L / M)
    k2 = k1[:, None, None] ** 2 + k1[None, :, None] ** 2 + kz[None, None, :] ** 2
    return np.fft.irfftn(np.fft.rfftn(x) * np.exp(-0.5 * k2 * sig ** 2), s=x.shape).astype(np.float32)

def expel(dpart, dgrav, a, foot):
    mesh = PM.Mesh(M); dta = PM.dta_table()
    D = math.exp(np.interp(math.log(1 / a), np.log1p(dta["z"]), np.log(dta["D"])))
    peaks = PM.cover_peaks(mesh, dpart.astype(np.float32), D)
    edge_p = PM.cover_balls(mesh, peaks, D, None, a, "FLAT", foot)
    catch_p, code, tab = PM.cover_balls(mesh, peaks, D, 1.0, a, "FLAT", foot, want_fret=True)
    catch = PM.unpack(catch_p).astype(bool); edge = PM.unpack(edge_p).astype(bool)
    idx, ron, Rg = peaks
    fr = tab[code]
    rho = 1.0 + dpart.astype(np.float64)
    e = FB * (1.0 - fr) * rho; E = e.sum()
    info = dict(Delta_ta=D, n_peaks_resolved=int((ron >= PM.RMIN_PHYS).sum()), catch_vol_frac=float(catch.mean()), catch_mass_frac=float(rho[catch].sum() / rho.sum()),
                expelled_frac_of_all_mass=float(E / rho.sum()), expelled_frac_of_catch_mass=float(E / rho[catch].sum()),
                fret_mass_weighted_in_catch=float((fr * rho)[catch].sum() / rho[catch].sum()))
    out = {}
    base = dgrav.astype(np.float64) - e
    fld = np.where(catch, 0.0, rho); out["DIFF-F"] = (base + E * fld / fld.sum()).astype(np.float32); del fld
    out["DIFF-U"] = (base + E / M ** 3).astype(np.float32)
    # DIFF-S: per catchment class (one catchment radius R per code), Gaussian sigma = R
    sm = np.zeros_like(base)
    Rres = [R for R in Rg[Rg >= PM.RMIN_PHYS - 1e-9] if np.any((ron >= PM.RMIN_PHYS) & (np.abs(ron - R) < 1e-9))]
    for kc, R in enumerate(Rres, start=1):
        m = code == kc
        if m.any(): sm += gsmooth(np.where(m, e, 0.0).astype(np.float32), R)
    out["DIFF-S"] = (base + sm * (E / sm.sum())).astype(np.float32); del sm
    # SHELL: per connected catchment, into its own shell cells
    r, nc = PM.catch_labels(catch)
    lab = np.full(M ** 3, -1, np.int64); lab[catch.ravel()] = r
    shell = (catch & ~edge).ravel()
    Ec = np.bincount(r, e.ravel()[catch.ravel()], nc)
    Wc = np.bincount(lab[shell], rho.ravel()[shell], nc)
    add = np.zeros(M ** 3)
    ok = Wc > 0
    add[shell] = (Ec / np.where(ok, Wc, 1.0))[lab[shell]] * rho.ravel()[shell]
    noshell = ~ok
    if noshell.any():                                   # catchment with no shell cell at 256^3: keep its gas in place (disclosed)
        inl = np.isin(lab, np.nonzero(noshell)[0]); add[inl] += e.ravel()[inl]
    out["SHELL"] = (base + add.reshape(base.shape)).astype(np.float32); del add, lab
    info["shell_kept_in_place_frac"] = float(Ec[noshell].sum() / max(Ec.sum(), 1e-300))
    info["n_catchments"] = int(nc)
    for k_, v in out.items(): assert abs(v.astype(np.float64).sum() - dgrav.astype(np.float64).sum()) <= 1e-5 * rho.sum(), k_
    return out, info

KSEL = (0.3, 0.5, 1.0, 2.0, 4.0)
def stream_pos(fn, n_rows=1 << 20):
    import zipfile
    with zipfile.ZipFile(fn) as zf, zf.open("pos.npy") as f:
        ver = np.lib.format.read_magic(f); shape, fortran, dt = np.lib.format._read_array_header(f, ver)
        assert not fortran and shape[1] == 3; left = shape[0]; rb = 3 * dt.itemsize
        while left > 0:
            n = min(n_rows, left); buf = f.read(n * rb); yield np.frombuffer(buf, dt).reshape(n, 3); left -= n
def run_source(name):
    t0 = time.time(); res = dict(nodes={})
    if name == "P1":
        foot = "canonical"; W = os.path.join(EXT, "cfg596_work", "P1")
        nodes = [(1.0, "z0"), (2 / 3, "z0.5"), (0.5, "z1")]
        for a, key in nodes:
            d = np.load(os.path.join(W, f"cfg596_RES_canonical_N1024_L100_ns1024_lean_{key}_mesh256.npz"))
            dp, dg = d["dpart"], d["dgrav"]
            res["nodes"][key] = node(dp, dg, a, foot)
            P(f"  [{name} {key}] {fmt(res['nodes'][key])}  ({time.time() - t0:.0f} s)")
    else:
        foot = "canonical" if name == "530can" else "alt"; run = "LRcan" if foot == "canonical" else "LRalt"
        g = np.load(os.path.join(EXT, "cfg530_work", "profiles", "N512", f"cfg526_{run}_L100_rhog.npy"), mmap_mode="r")
        rg = np.empty((M, M, M))
        for i in range(M): rg[i] = np.asarray(g[2 * i:2 * i + 2], np.float64).reshape(2, M, 2, M, 2).mean(axis=(0, 2, 4))
        del g
        dg = (rg / rg.mean() - 1.0).astype(np.float32); del rg
        fn = os.path.join(EXT, "cfg530_work", "runs", f"{run}_L100_N512", f"cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_{foot}_N512_L100_drawSHELL_z0.npz")
        rho = np.zeros(M ** 3)
        for chunk in stream_pos(fn):                       # streamed from the zip member (keeps the process under 3 GB)
            u = chunk.astype(np.float64) * (M / L); i = np.floor(u).astype(np.int64); w = u - i; i %= M
            for dx in (0, 1):
                wx = w[:, 0] if dx else 1 - w[:, 0]
                for dy in (0, 1):
                    wy = w[:, 1] if dy else 1 - w[:, 1]
                    for dz in (0, 1):
                        wz = w[:, 2] if dz else 1 - w[:, 2]
                        rho += np.bincount((((i[:, 0] + dx) % M) * M + (i[:, 1] + dy) % M) * M + (i[:, 2] + dz) % M, wx * wy * wz, M ** 3)
        dp = (rho / rho.mean() - 1.0).reshape(M, M, M).astype(np.float32); del rho
        res["nodes"]["z0"] = node(dp, dg, 1.0, foot)
        P(f"  [{name} z0] {fmt(res['nodes']['z0'])}  ({time.time() - t0:.0f} s)")
    res["foot"] = foot
    return res

def node(dp, dg, a, foot):
    var, info = expel(dp, dg, a, foot)
    k, p0 = pk(dg); o = dict(k=k.tolist(), P_grav=p0.tolist(), info=info, ratio={}, ratio_at={})
    for nm, v in var.items():
        _, pv = pk(v); rr = pv / p0
        o["ratio"][nm] = rr.tolist(); o["ratio_at"][nm] = {str(kk): float(np.interp(math.log(kk), np.log(k), rr)) for kk in KSEL}
    return o
def fmt(o):
    i = o["info"]
    return (f"catch mass {i['catch_mass_frac']:.3f}, f_ret(mass-wtd, catch) {i['fret_mass_weighted_in_catch']:.3f}, expelled {i['expelled_frac_of_all_mass']:.4f} of all mass; "
            + "; ".join(f"{nm}: " + "/".join(f"{x:.3f}" for x in r.values()) for nm, r in o["ratio_at"].items()) + "  (P'/P at k 0.3/0.5/1/2/4)")

if __name__ == "__main__":
    srcs = sys.argv[1:] or ["P1", "530can", "530alt"]
    ALL = json.load(open(OUTF)) if os.path.exists(OUTF) else dict(lane="CFG646", part="ii_pm_postprocess", declarations="3c1c5a42f", sources={})
    P("CFG646 (ii) PM-native post-process (estimate; resolution-limited). kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    for s in srcs:
        ALL["sources"][s] = run_source(s)
    json.dump(ALL, open(OUTF, "w"))
    with open(os.path.join(HERE, "cfg646_expulsion_pm.out"), "a") as f: f.write("\n".join(OUT) + "\n")
