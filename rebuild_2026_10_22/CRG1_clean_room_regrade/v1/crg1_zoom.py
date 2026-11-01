"""Zoom re-estimates: eta per seed (section 0.3), shape stacks. Writes partials/zoom_eta.json, cache/shape_stacks.npz."""
from crg1_core import *

def centre(x):
    c = x.mean(0); r = np.sqrt(((x - c) ** 2).sum(1)).max()
    while True:
        sel = ((x - c) ** 2).sum(1) < r * r
        if sel.sum() < 100: return c
        c = x[sel].mean(0); r *= 0.8

def load(f):
    d = np.load(f); x = d["x"].astype(np.float64); m = float(d["m"]); meta = json.loads(str(d["meta"]))
    return x, m, meta

def mu(y): return np.log1p(y) - y / (1 + y)

CGRID = np.linspace(1, 30, 581)
def nfw_c(r, Menc, rvir, rconv):
    sel = (r >= rconv) & (r <= rvir)
    rr = r[sel]; lnm = np.log(Menc[sel] / Menc[sel][-1])
    best, bc = np.inf, None
    for c in CGRID:
        v = np.log(mu(c * rr / rvir) / mu(c)) - lnm
        s = float((v * v).sum())
        if s < best: best, bc = s, c
    return float(bc)

AGRID = np.geomspace(0.5, 60, 2001)
def eta_from_c(c):
    xs = np.geomspace(0.001, 1, 20001); Ms = mu(c * xs)
    q = np.linspace(Ms[0], Ms[-1], 2000); u = np.interp(q, Ms, xs); y = np.log(q / Ms[-1])
    best, ba = np.inf, None
    for a in AGRID:
        v = np.log(B_S(a * u) / B_S(a)) - y
        s = float((v * v).sum())
        if s < best: best, ba = s, a
    return float(4.0 / 3 * ba ** 2 / B_S(ba)), float(ba)

def measure_eta(f):
    x, m, M = load(f); c = centre(x)
    r = np.sort(np.sqrt(((x - c) ** 2).sum(1))); n = np.arange(1, len(r) + 1)
    Menc = n * m; dens = Menc / (4.0 / 3 * math.pi * r ** 3)
    rho_m = M["Mf"] / (4.0 / 3 * math.pi * M["qM"] ** 3) * (1 + M["zf"]) ** 3
    ii = np.nonzero(dens >= 18 * math.pi ** 2 * rho_m)[0]
    if len(ii) == 0: return {"flag": "no r_vir"}
    rvir = r[ii[-1]]; rconv = max(3 * M["eps"], r[199])
    if rconv >= rvir / 2: return {"flag": "r_conv >= r_vir/2"}
    edges = np.geomspace(rconv, rvir, 25)
    if (np.histogram(r, edges)[0] > 0).sum() < 8: return {"flag": "bins"}
    cc = nfw_c(r, Menc, rvir, rconv); eta, a = eta_from_c(cc)
    return {"c": cc, "eta": eta, "a": a, "r_vir": rvir, "r_conv": rconv, "N": len(r)}

XG = np.geomspace(1e-3, 40, 500)
G_Z = 4.30091e-9
def shape_measure(x, m, eps, thr):
    c = centre(x)
    r = np.sort(np.sqrt(((x - c) ** 2).sum(1))); N = len(r); n = np.arange(1, N + 1)
    Menc = n * m; dens = Menc / (4.0 / 3 * math.pi * r ** 3)
    i = np.nonzero(dens >= thr)[0][-1]
    if i == N - 1: R200 = r[i] * (dens[i] / thr) ** (1.0 / 3)
    else:
        t = (math.log(thr) - math.log(dens[i])) / (math.log(dens[i + 1]) - math.log(dens[i]))
        R200 = math.exp(math.log(r[i]) + t * (math.log(r[i + 1]) - math.log(r[i])))
    M200 = thr * 4.0 / 3 * math.pi * R200 ** 3
    xconv = 3 * eps / R200; xedge = r[int(math.floor(0.9 * N)) - 1] / R200
    lr, lM = np.log(r), np.log(Menc)
    lnm = np.interp(np.log(XG * R200), lr, lM) - math.log(M200)
    low = XG < xconv
    lc = np.interp(math.log(xconv * R200), lr, lM) - math.log(M200)
    lnm[low] = lc + 2 * np.log(XG[low] / xconv)
    return lnm, math.log10(M200), xedge, R200

def shape_one(f, ztag):
    x, m, M = load(f)
    z = M["zf"] if "zf_as" in os.path.basename(f) else float(ztag)
    rc = 3 * (100 * h_nat) ** 2 * (Om_nat * (1 + z) ** 3 + 1 - Om_nat) / (8 * math.pi * G_Z)
    return shape_measure(x, m, M["eps"], 200 * rc)

def stacks():
    out = {}; info = {}
    for mt in ("1e13", "1e14", "1e15"):
        for zt in ("0.00", "0.25", "0.50"):
            fs = sorted(glob.glob(os.path.join(INP, "zooms", "shape", "M%s_s*_z%s.npz" % (mt, zt))))
            if zt == "0.50":
                fs += sorted(glob.glob(os.path.join(INP, "zooms", "shape", "M%s_s*_zf_as_z0.50.npz" % mt)))
            L, lg, xe = [], [], []
            for f in fs:
                a, b, e, _ = shape_one(f, zt); L.append(a); lg.append(b); xe.append(e)
            k = mt + "_" + zt
            out["lnm_" + k] = np.median(np.array(L), axis=0)
            out["lgM_" + k] = np.median(lg); out["xe_" + k] = np.min(xe)
            info[k] = {"n_seeds": len(fs), "lgM200_med": float(np.median(lg)), "x_edge_min": float(np.min(xe))}
    return out, info

def main():
    if not have_part("zoom_eta"):
        res = {}; maxd = {}
        for mt in ("1e10", "1e11", "1e12"):
            key = "%s_ng80" % {"1e10": "1e+10", "1e11": "1e+11", "1e12": "1e+12"}[mt]
            given = SC["nr2"]["per_seed_eta"][key]; etas = []; rows = []
            for s in range(1, 10):
                r = measure_eta(os.path.join(INP, "zooms", "eta", "M%s_s%d_ng80_zf.npz" % (mt, s)))
                rows.append(r); etas.append(r.get("eta", float("nan")))
                log("eta %s s%d %s" % (mt, s, "ok" if "eta" in r else r["flag"]))
            res[mt] = {"seeds": rows, "median_eta": float(np.nanmedian(etas)),
                       "max_abs_diff_vs_scalars": float(np.nanmax(np.abs(np.array(etas) - np.array(given))))}
        save_part("zoom_eta", res)
    st, info = stacks()
    np.savez(os.path.join(CACHE, "shape_stacks.npz"), X=XG, **st)
    save_part("zoom_shape_info", info)

def get_nr(reading="a"):
    e = load_part("zoom_eta")
    m10, m11, m12 = e["1e10"]["median_eta"], e["1e11"]["median_eta"], e["1e12"]["median_eta"]
    if reading == "a":
        an = SC["nr2"]["eta12_anchor"]; return NR(an, m10 / an, m11 / an, "A1a")
    return NR(m12, m10 / m12, m11 / m12, "A1b")

if __name__ == "__main__": main()
