#!/usr/bin/env python3
"""ZN1 measurement: from the z = 0.5, 0.25, 0 snapshots, M(<r), R200, shape m(x) = M(<x R200)/M200, the edge; median stacks; the reported read-outs. K2 tests it on a sampled exact NFW.
    python3 zn1_measure.py --k2       # K2 only, reads no ZN1 snapshot
    python3 zn1_measure.py            # all finished runs; writes zn1_shapes.json, zn1_readouts.out
kappa = 1/2 FITTED; not theory closed."""
import glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
X77P = os.path.join(REB, "X77_direct_core_surface_density", "x77_direct_eta.py"); _src = open(X77P).read(); _src = _src[:_src.index("# K2: formula vs direct integration")]
NS = dict(__file__=X77P, __name__="x77_prefix"); _a = sys.argv; sys.argv = [X77P]; exec(compile(_src, X77P, "exec"), NS); sys.argv = _a; FIT, XA = NS["fit"], NS["XA"]
XG = np.geomspace(1e-3, 40.0, 500)   # x = r/R200
G = 4.30091e-9; Om, h = 0.2976016, 0.6856427; H0 = 100 * h
def rho_c(z): return 3 * H0 ** 2 * (Om * (1 + z) ** 3 + 1 - Om) / (8 * math.pi * G)   # Msun/Mpc^3
def measure(x, m, z, eps):
    c = XA.centre(x, m); r = np.sort(np.sqrt(((x - c) ** 2).sum(1))); Menc = np.arange(1, len(r) + 1) * m; dens = Menc / (4 / 3 * math.pi * r ** 3); thr = 200 * rho_c(z)
    i = np.where(dens >= thr)[0].max(); R200 = float(r[i] * (dens[i] / thr) ** (1 / 3)) if i + 1 == len(r) else float(math.exp(np.interp(math.log(thr), [math.log(dens[i + 1]), math.log(dens[i])], [math.log(r[i + 1]), math.log(r[i])])))
    M200 = thr * 4 / 3 * math.pi * R200 ** 3; xc = 3 * eps / R200; xe = float(r[int(0.9 * len(r)) - 1] / R200)
    lm = np.interp(np.log(XG * R200), np.log(r), np.log(Menc)) - math.log(M200); j = XG < xc
    if j.any():
        lc = float(np.interp(math.log(xc * R200), np.log(r), np.log(Menc)) - math.log(M200)); lm[j] = lc + 2 * np.log(XG[j] / xc)
    return dict(R200=R200, M200=M200, x_conv=xc, x_edge=xe, lnm=lm.tolist(), r=r, Menc=Menc)
def k2():
    """AMENDMENT A2: the frozen 2 % at x >= 0.05 is below the sampling noise (about 550 particles inside x 0.05, 4.3 %), so the test averages 20 samples, limit 1 %. Single-sample worst case is printed too."""
    mu = lambda y: np.log1p(y) - y / (1 + y); c = 4.0; N = 57777; M200 = 1e14; R200 = (3 * M200 / (4 * math.pi * 200 * rho_c(0.0))) ** (1 / 3); ymax = c * 3.0; yg = np.geomspace(1e-6, ymax, 40000); s = (XG >= 0.05) & (XG <= 1.0); ex = mu(c * XG[s]) / mu(c); L = []; dR = []
    for seed in range(1, 21):
        rng = np.random.default_rng(seed); u = rng.random(N) * float(mu(ymax)); y = np.interp(u, mu(yg), yg); v = rng.standard_normal((N, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
        o = measure((y / c * R200)[:, None] * v, M200 * float(mu(ymax) / mu(c)) / N, 0.0, 1e-4 * R200); L.append(np.exp(np.array(o["lnm"])[s]) / ex); dR.append(abs(o["R200"] / R200 - 1))
    L = np.array(L); d = float(np.abs(L.mean(0) - 1).max()); ok = d <= 0.01 and max(dR) <= 0.01
    print(f"K2 sampled NFW c 4, N {N}, 20 samples: mean m/m_exact at x 0.05-1 within {d:.4f} (limit 0.01), worst single sample {float(np.abs(L - 1).max()):.4f}, R200 {max(dR):.4f} (0.01): {'PASS' if ok else 'FAIL'}", flush=True); return ok
if __name__ == "__main__":
    if "--k2" in sys.argv: sys.exit(0 if k2() else 1)
    if not k2(): sys.exit("K2 failed: no measurement")
    OUT = []; RES = {}
    def P(s): print(s, flush=True); OUT.append(s)
    RD = os.path.join(HERE, "runs"); X48 = os.path.join(REB, "X48_native_cf_zoom", "runs"); P("ZN1 read-outs; kappa = 1/2 FITTED; not theory closed")
    for M in ("1e12", "1e13", "1e14"):
        RES[M] = {}; zf_rows = {}
        for zs in ("0.50", "0.25", "0.00"):
            rows = []
            for d in sorted(glob.glob(os.path.join(RD, f"M{M}_s?_ng64"))):
                f = os.path.join(d, f"snap_z{zs}.npz"); s = os.path.basename(d)
                if not os.path.exists(f): continue
                Z = np.load(f, allow_pickle=False); meta = json.loads(str(Z["meta"])); x, m = Z["x"], float(Z["m"]); o = measure(x, m, float(zs), meta["eps"]); assert len(x) == meta["N"], "K4 N changed"
                rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + float(zs)) ** 3; f0, f1 = FIT(x, m, rho, meta["eps"])
                A = np.load(os.path.join(X48, s, "snap_zf.npz"), allow_pickle=False); rf = meta["rf_phys"]; ca = XA.centre(A["x"], float(A["m"])); ra = np.sort(np.sqrt(((A["x"] - ca) ** 2).sum(1))); g = np.array([0.1, 0.2, 0.5, 1.0, 1.5]) * rf; gr = (np.searchsorted(o["r"], g) / np.maximum(np.searchsorted(ra, g), 1)).tolist()
                nin = int(np.searchsorted(ra, rf)); nz = int(np.searchsorted(o["r"], rf)); fr = (nz - nin) / max(np.searchsorted(o["r"], o["R200"]) - nin, 1)
                i2 = np.searchsorted(XG, 1.0); ie = np.searchsorted(XG, o["x_edge"]); slope = float(np.polyfit(np.log(XG[i2:ie]), np.array(o["lnm"])[i2:ie], 1)[0]) if ie > i2 + 3 else float("nan")
                rows.append(dict(seed=s, lgM=math.log10(o["M200"]), R200=o["R200"], M_over_nom=o["M200"] / meta["M"], x_conv=o["x_conv"], x_edge=o["x_edge"], lnm=o["lnm"], c_nfw=(f0.get("c_nfw_fit") if f1 is not None else None), eta=(f1["S"]["eta"] if f1 is not None else None), a=(f1["S"]["a"] if f1 is not None else None), ratio_rf=gr, late_inside_rf=fr, gamma_out=3 - slope, r_over_rf=o["R200"] / rf))
            if not rows: continue
            lm = np.array([q["lnm"] for q in rows]); xe = min(q["x_edge"] for q in rows); RES[M][zs] = dict(n=len(rows), lgM=float(np.median([q["lgM"] for q in rows])), x_edge=xe, lnm=np.median(lm, axis=0).tolist(), seeds=rows, x=XG.tolist())
            md = lambda k: float(np.nanmedian([np.nan if q[k] is None else q[k] for q in rows]))
            P(f"  M {M} z {zs}: n {len(rows)}; lg M200 {RES[M][zs]['lgM']:.3f}, M200/M nominal {md('M_over_nom'):.3f}, R200/r_f {md('r_over_rf'):.3f}, x_edge min {xe:.2f}; c_nfw {md('c_nfw'):.2f}, eta {md('eta'):.2f}, a {md('a'):.2f}; slope past R200 {md('gamma_out'):.2f}; late mass inside r_f {md('late_inside_rf'):.3f}; M(<r)/M(<r, z_f) at r/r_f 0.1, 0.2, 0.5, 1, 1.5: " + ", ".join(f"{float(np.median([q['ratio_rf'][k] for q in rows])):.3f}" for k in range(5)))
    json.dump(RES, open(os.path.join(HERE, "zn1_shapes.json"), "w")); open(os.path.join(HERE, "zn1_readouts.out"), "w").write("\n".join(OUT) + "\n")
