#!/usr/bin/env python3
"""FN4a fits in the cube (FROZEN_CRITERIA.md models; AMENDMENTS A3-A8). Stage 0 failed (fn4a_s0.json: S0a, S0b), so by the
frozen rule the lane's label is NOT EVALUABLE; these fits are run and reported as POST-RESULT diagnostics, with the frozen
label rule applied to them only as a reading.
Stages (each writes cache/fit_<stage>.json):
  free      M_free on the real cube
  law_<f>   M_law scan over i = 15..60 (5 deg) and a free-i refinement, footing f (canonical, alt)
  nc_<f>    M_law+nc scan over i = 15..60 (7.5 deg), footing f
  newton    M_N scan over i (KA3)
  ka1, ka2  mocks (A8): M_free and the canonical M_law scan on each
  mutate    M_free on the real cube with the channel order shuffled
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I fn4a_fit.py <stage>     kappa = 1/2 FITTED; not theory closed."""
import json, math, os, resource, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy.optimize import least_squares
from scipy import ndimage
import fn4a_core as C

T0 = time.time()
def say(s): print(f"[{time.time() - T0:7.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB] {s}", flush=True)

P = dict(np.load(os.path.join(C.CACHE, "prep.npz")))
NR = int(P["nring"]); RC = (np.arange(NR) + 0.5) * C.RING; ROUT = float(P["R_out"])
SN = np.linspace(0, ROUT, 6)                                     # sigma and nc nodes (A6, A3)
INC_LAW = np.arange(15.0, 60.01, 5.0); INC_NC = np.arange(15.0, 60.01, 7.5)
G0 = dict(x0=0.0, y0=0.0, pa=C.OH15["pa"], vsys=C.OH15["vsys"])


def vfun_rings(V): return C.interp_nodes(np.r_[0.0, RC], np.r_[0.0, V])
def sfun(s): return C.interp_nodes(SN, s)


class Free:
    def __init__(s, cube): s.c = cube
    def unpack(s, p): return p[0], p[1], p[2], p[3], p[4], p[5:5 + NR], p[5 + NR:11 + NR]
    def res(s, p):
        x0, y0, pa, inc, vs, V, sg = s.unpack(p); vl, sig, _ = C.vfield(s.c, x0, y0, pa, inc, vs, vfun_rings(V), sfun(sg)); return s.c.resid(vl, sig)
    def sparsity(s, p0):
        """ring k touches only voxels whose deprojected radius (start geometry) lies within 3 rings of it; geometry and sigma are dense."""
        from scipy.sparse import coo_matrix
        R, _, _ = C.disc_coords(s.c.XE, s.c.YN, p0[0], p0[1], p0[2], p0[3]); Rv = np.broadcast_to(R[None], s.c.sel.shape)[s.c.sel]; m = len(Rv)
        ri, ci = [], []
        for j in list(range(5)) + list(range(5 + NR, 11 + NR)): ri.append(np.arange(m)); ci.append(np.full(m, j))
        for k in range(NR):
            rows = np.nonzero(np.abs(Rv - RC[k]) <= 3 * C.RING)[0]; ri.append(rows); ci.append(np.full(len(rows), 5 + k))
        ri = np.concatenate(ri); ci = np.concatenate(ci)
        return coo_matrix((np.ones(len(ri), np.int8), (ri, ci)), shape=(m, len(p0))).tocsr()
    def fit(s, p0):
        lo = np.r_[-60, -60, 40, 15, -250, np.zeros(NR), np.full(6, 2.0)]; hi = np.r_[60, 60, 110, 60, -215, np.full(NR, 80.0), np.full(6, 25.0)]
        xs = np.r_[5, 5, 3, 3, 1, np.full(NR, 2.0), np.full(6, 1.0)]; p0 = np.clip(p0, lo + 1e-6, hi - 1e-6)
        r = least_squares(s.res, p0, bounds=(lo, hi), x_scale=xs, method="trf", max_nfev=30, diff_step=1e-3, jac_sparsity=s.sparsity(p0))
        return r


class Law:
    def __init__(s, cube, bary, a0, nu=True, nc=False): s.c = cube; s.b = bary; s.a0 = a0; s.nu = nu; s.nc = nc
    def rot(s, x0, y0, pa, inc, sg):
        Rg, v2, gsum = s.b.vc2(x0, y0, pa, inc, s.a0, nu=s.nu)
        sig = sfun(sg)(Rg); q = np.log(np.clip(gsum, 1e-30, None) * sig ** 2); d = np.gradient(ndimage.uniform_filter1d(q, 5), np.log(Rg))
        vr2 = v2 + sig ** 2 * d; return C.interp_nodes(Rg, np.sqrt(np.clip(vr2, 0, None))), Rg, np.sqrt(np.clip(v2, 0, None))
    def res_at(s, p, inc):
        x0, y0, pa, vs = p[:4]; sg = p[4:10]; Vf, _, _ = s.rot(x0, y0, pa, inc, sg)
        ncf = None
        if s.nc:
            a = p[10:16]; b_ = p[16:22]; c_ = p[22:28]; ncf = lambda R: (np.interp(R, SN, a), np.interp(R, SN, b_), np.interp(R, SN, c_))
        vl, sig, _ = C.vfield(s.c, x0, y0, pa, inc, vs, Vf, sfun(sg), nc=ncf); return s.c.resid(vl, sig)
    def fit_at(s, inc, p0):
        n = 10 + (18 if s.nc else 0)
        lo = np.r_[-60, -60, 40, -250, np.full(6, 2.0), np.full(n - 10, -20.0)]; hi = np.r_[60, 60, 110, -215, np.full(6, 25.0), np.full(n - 10, 20.0)]
        xs = np.r_[5, 5, 3, 1, np.full(6, 1.0), np.full(n - 10, 2.0)]
        r = least_squares(lambda p: s.res_at(p, inc), np.clip(p0[:n], lo + 1e-6, hi - 1e-6), bounds=(lo, hi), x_scale=xs, method="trf", max_nfev=25, diff_step=1e-3)
        return r


def cube_of(D):
    Q = dict(P); Q["cube"] = D
    return C.Cube(Q)


def free_start(c):
    s0 = json.load(open(os.path.join(HERE, "fn4a_s0.json")))["S0b"]["rings"]
    V0 = np.interp(RC, s0["R"], s0["V"]); V0 = np.nan_to_num(V0, nan=10.0)
    return np.r_[G0["x0"], G0["y0"], G0["pa"], 48.0, G0["vsys"], np.clip(V0, 1, 60), np.full(6, 9.0)]


def run_free(c, tag):
    f = Free(c); r = f.fit(free_start(c)); p = r.x; chi2 = float(np.sum(r.fun ** 2)); dof = c.ndat - len(p)
    out = dict(stage=tag, chi2=chi2, ndat=c.ndat, npar=len(p), dof=dof, chi2_red=chi2 / dof, x0=p[0], y0=p[1], pa=p[2], inc=p[3], vsys=p[4],
               V=p[5:5 + NR].tolist(), sigma=p[5 + NR:11 + NR].tolist(), RC=RC.tolist(), nfev=int(r.nfev), status=int(r.status))
    say(f"{tag} M_free: chi2 {chi2:.1f} / {dof} = {chi2 / dof:.3f}; i {p[3]:.1f}, PA {p[2]:.1f}, vsys {p[4]:.2f}, centre ({p[0]:+.1f}, {p[1]:+.1f})\"")
    return out


def run_scan(c, bary, foot, incs, nu=True, nc=False, start=None, tag=""):
    L = Law(c, bary, C.A0[foot], nu=nu, nc=nc); p = np.r_[start["x0"], start["y0"], start["pa"], start["vsys"], np.array(start["sigma"]), np.zeros(18)]
    rows = []
    for inc in incs:
        r = L.fit_at(inc, p); p = np.r_[r.x, np.zeros(28 - len(r.x))] if len(r.x) < 28 else r.x
        chi2 = float(np.sum(r.fun ** 2)); _, Rg, vc = L.rot(r.x[0], r.x[1], r.x[2], inc, r.x[4:10])
        rows.append(dict(inc=float(inc), chi2=chi2, x=r.x.tolist(), nfev=int(r.nfev), vc_at_2kpc=float(np.interp(2000.0 / C.arcsec_to_pc(1.0), Rg, vc))))
        say(f"{tag} i {inc:5.1f}: chi2 {chi2:.1f} (vc(2 kpc) {rows[-1]['vc_at_2kpc']:.1f} km/s)")
    b = min(rows, key=lambda q: q["chi2"])
    return dict(stage=tag, footing=foot, nu=nu, nc=nc, rows=rows, best_inc=b["inc"], best_chi2=b["chi2"])


def mock(rot_scale, seed):
    """A8: the law's rotation (canonical) at i 35, sigma 9, geometry from the real M_free fit, real moment 0, beam-correlated noise."""
    fr = json.load(open(os.path.join(C.CACHE, "fit_free.json"))); c = cube_of(P["cube"]); bary = C.Baryons(P, 2.88e7)
    L = Law(c, bary, C.A0["canonical"]); sg = np.full(6, 9.0); Vf, _, _ = L.rot(fr["x0"], fr["y0"], fr["pa"], 35.0, sg)
    vl, sig, _ = C.vfield(c, fr["x0"], fr["y0"], fr["pa"], 35.0, fr["vsys"], lambda R: rot_scale * Vf(R), sfun(sg))
    M = c.model(vl, sig); rng = np.random.default_rng(seed); n = rng.standard_normal(M.shape)
    n = np.fft.irfft2(np.fft.rfft2(n, s=(c.py, c.px)) * c.otf[None], s=(c.py, c.px))[:, :c.ny, :c.nx]
    n = ndimage.convolve1d(n, [0.25, 0.5, 0.25], axis=0, mode="nearest"); n *= c.sig / n.std()
    return M + n, dict(x0=fr["x0"], y0=fr["y0"], pa=fr["pa"], vsys=fr["vsys"])


if __name__ == "__main__":
    st = sys.argv[1]; out = None
    if st == "free":
        out = run_free(cube_of(P["cube"]), "free")
    elif st.startswith(("law_", "nc_")) or st == "newton":
        foot = "canonical" if st == "newton" else st.split("_")[1]; fr = json.load(open(os.path.join(C.CACHE, "fit_free.json")))
        nc = st.startswith("nc_"); out = run_scan(cube_of(P["cube"]), C.Baryons(P, 2.88e7), foot, INC_NC if nc else INC_LAW, nu=(st != "newton"), nc=nc, start=fr, tag=st)
        if st.startswith("law_"):                                        # bracket M* 1.9e8 at the best inclination (reported)
            b = min(out["rows"], key=lambda q: q["chi2"]); L = Law(cube_of(P["cube"]), C.Baryons(P, 1.9e8), C.A0[foot]); r = L.fit_at(b["inc"], np.array(b["x"]))
            out["bracket_Mstar_1.9e8"] = dict(inc=b["inc"], chi2=float(np.sum(r.fun ** 2)))
    elif st in ("ka1", "ka2"):
        D, g = mock(1.0 if st == "ka1" else 0.505, 20261104 if st == "ka1" else 20261105); c = cube_of(D)
        f = run_free(c, st + "_free"); s = run_scan(c, C.Baryons(P, 2.88e7), "canonical", INC_LAW, start=dict(g, sigma=[9.0] * 6), tag=st + "_law")
        out = dict(stage=st, free=f, law=s)
    elif st == "mutate":
        rng = np.random.default_rng(7); D = P["cube"][rng.permutation(P["cube"].shape[0])]
        out = run_free(cube_of(D), "mutate")
    json.dump(out, open(os.path.join(C.CACHE, f"fit_{st}.json"), "w"), indent=1, sort_keys=True, default=float)
    say(f"stage {st} done")
