#!/usr/bin/env python3
"""AG4i: AG4h's five clean positive-pull galaxies against independent kinematics (K) and radial M/L gradients from the
[3.6]-[4.5] colour (M; Meidt+2014 Eq. 4), and K+M, each against 200 law-true mocks.  Baryons from SPARC; AG4g's estimator.
Criteria: FROZEN_CRITERIA.md (committed alone, before this script).  Downloaded files are only read (astropy / text parsing).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 ag4i.py      AG4I_MUTATE=1: SPARC's own curve and beta = 0 must reproduce the pulls.
kappa = 1/2 fitted; not theory closed."""
import csv, gzip, json, math, os, sys, warnings
import numpy as np
from scipy.special import j0, j1, i0, i1, k0, k1

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.join(os.path.dirname(REPO), "_external_data"); FG = os.path.join(EXT, "five_galaxies_2026_10_20")
G4G = os.path.join(REPO, "argon_push", "AG4g_galaxy_pull_census"); SP = os.path.join(REPO, "real_research", "data", "sparc_data")
MUT = os.environ.get("AG4I_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag4i{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n"); OUT.flush()
src = open(os.path.join(G4G, "ag4g.py")).read()
ns = {"__file__": os.path.join(G4G, "ag4g.py"), "__name__": "ag4g_frozen", "P": P, "MUT": False, "FAILS": [], "check": None}
exec(compile(src[:src.index("MUT = os.environ.get")], "ag4g_head", "exec"), ns); ns["P"] = P; ns["MUT"] = False
exec(compile(src[src.index("LN10 = math.log(10.0)"):src.index("PR = props(D_)")], "ag4g_body", "exec"), ns)
fit, NU1, A0C, LU0, SIG_U, S0, LN10, UG, LU, D4G = ns["fit"], ns["NU1"], ns["A0C"], ns["LU0"], ns["SIG_U"], ns["S0"], ns["LN10"], ns["UG"], ns["LU"], ns["D_"]
KPC_S = 3.0857e19; AS2RAD = 1.0 / 206264.806
P("AG4i: five clean positive-pull galaxies vs independent kinematics and [3.6]-[4.5] M/L gradients" + ("   *** MUTATE ***" if MUT else ""))
P("kappa = 1/2 fitted; not theory closed.")
FIVE = ["NGC0024", "NGC5985", "UGC00128", "UGC00731", "UGC08286"]
BETAS = {"primary 3.98": 3.98, "-1 sigma 2.99": 2.99, "+1 sigma 4.97": 4.97, "LMC Eq.5 -0.74": -0.74}
ZPC = 2.5 * math.log10(280.9 / 179.7)                                  # Vega colour from equal-unit intensities
res4g = json.load(open(os.path.join(G4G, "ag4g_results.json")))
PULL4G = dict(zip(res4g["names"], res4g["stage1"]["n=1 canonical (PRIMARY)"]["pulls"]))
META = {d["name"]: d for d in D4G}


def rotmod(name):
    a = np.genfromtxt(os.path.join(SP, f"{name}_rotmod.dat"), comments="#")
    return dict(R=a[:, 0], Vo=a[:, 1], eV=a[:, 2], Vg=a[:, 3], Vd=a[:, 4], Vb=a[:, 5], SBd=a[:, 6], SBb=a[:, 7])


def make(R, V, eV, gas2, Vd2, Vb2, cg, m=None):
    """AG4g's per-galaxy dict (AG4g's point cuts) from radii (kpc), velocities and baryonic V^2 components."""
    m = np.ones_like(R) if m is None else m
    Rm = R * KPC_S; star = (Vd2 * m + 1.4 * Vb2) * 1e6 / Rm; gas = gas2 * 1e6 / Rm; go = (V * 1e3) ** 2 / Rm
    ok = (V > 0) & (go > 0) & (gas + star * UG[0] > 0) & (gas + star * UG[-1] > 0) & np.isfinite(go) & (R > 0)
    return dict(go=go[ok], gas=gas[ok], star=star[ok], sv=2.0 / LN10 * np.clip(eV[ok], 1, None) / np.clip(V[ok], 1, None), cg=cg, n=int(ok.sum()))


def pull1(d):
    return float(fit([d], NU1, A0C)[0])


def mock_p(d, seeds=range(1, 201)):
    out = []
    for s in seeds:
        rng = np.random.default_rng(s)
        lu = float(np.clip(LU0 + SIG_U * rng.standard_normal(), LU[0], LU[-1])); gb = d["gas"] + d["star"] * 10 ** lu
        lgo = np.log10(NU1(gb / A0C) * gb) + d["cg"] * rng.standard_normal() + np.sqrt(d["sv"] ** 2 + S0 ** 2) * rng.standard_normal(len(gb))
        out.append(pull1(dict(d, go=10 ** lgo)))
    return np.array(out)


def shape_dchi(d):
    LUW = LU0 + np.linspace(-1.5, 1.5, 1201)
    def chi(lu):
        gb = d["gas"][:, None] + d["star"][:, None] * (10 ** np.atleast_1d(lu))[None, :]
        bad = np.any(gb <= 0, axis=0); gb = np.where(gb > 0, gb, 1.0)
        r = np.log10(d["go"])[:, None] - np.log10(NU1(gb / A0C) * gb); w = (1.0 / (d["sv"] ** 2 + S0 ** 2))[:, None]
        c = (w * r).sum(0) / w.sum(0); return np.where(bad, np.inf, (w * (r - c) ** 2).sum(0))
    return float(chi(np.array([LU0]))[0] - chi(LUW).min())


def judge(d):
    p = pull1(d); pm = mock_p(d); pe = float(np.mean(np.abs(pm) >= abs(p) - 1e-12))
    rd = "RESOLVED" if abs(p) < 3 - 1e-9 else ("PERSISTS" if pe < 0.01 else "WEAK")
    return dict(pull=p, p_emp=pe, reading=rd, mock_sd=float(np.std(pm)), dchi2_shape=shape_dchi(d), n=d["n"])


# ------------------------------------------------------------------------------------------------ independent curves
def bin6(r_as, V, e, side):
    out = []
    for b in np.unique(np.floor(r_as / 6.0)):
        k = np.floor(r_as / 6.0) == b; n = int(k.sum()); v = V[k]
        sm = float(np.std(v, ddof=1) / math.sqrt(n)) if n >= 2 else float(np.median(e[k]))
        sides = sorted(set(side[k])); asym = abs(np.mean(v[side[k] == sides[0]]) - np.mean(v[side[k] == sides[1]])) if len(sides) == 2 else 0.0
        out.append((float(np.mean(r_as[k])), float(np.mean(v)), max(math.sqrt(sm ** 2 + (asym / 2) ** 2), 3.0)))
    return np.array(out)


def indep_curve(name, Dmpc, inc):
    if name == "NGC5985":
        rows = [l for l in open(os.path.join(FG, "kinematics", "ghasp_epinat2008", "tablef.dat")) if l[:8].strip() == "UGC 9969"]
        r = np.array([float(l[20:25]) for l in rows]); V = np.array([float(l[31:34]) for l in rows]); e = np.array([float(l[35:38]) for l in rows])
        side = np.array([l[42] for l in rows])
    else:
        key = {"UGC00731": "UGC731", "UGC08286": "NGC5023"}[name]
        rows = [l for l in gzip.open(os.path.join(FG, "kinematics", "deblok_bosma2002", "rawcurve.dat.gz"), "rt") if l[:11].strip() == key]
        rr = np.array([float(l[11:19]) for l in rows]); vv = np.array([float(l[19:28]) for l in rows]); e = np.array([float(l[28:34]) for l in rows])
        r = np.abs(rr); V = np.abs(vv) / math.sin(math.radians(inc)); e = e / math.sin(math.radians(inc)); side = np.where(rr < 0, "n", "p")
    b = bin6(r, V, e, side)
    return b[:, 0] * Dmpc * 1e3 * AS2RAD, b[:, 1], b[:, 2], len(rows)


# ------------------------------------------------------------------------------------------------ colour profiles
def s4g_colour(name):
    tag = {"NGC0024": "NGC0024", "NGC5985": "NGC5985", "UGC08286": "NGC5023"}[name]
    def rd(ch):
        A = []
        for l in open(os.path.join(FG, "profiles", "s4g_p3", f"{tag}.{ch}fx2a_noclean_fin.dat")):
            t = l.split()
            try:
                A.append((float(t[0]), float(t[1]), float(t[2])))
            except ValueError:
                continue
        return np.array(A)
    a1, a2 = rd(1), rd(2)                                               # match the two bands by radius, not by row
    k2 = {round(r, 2): (i, e) for r, i, e in a2}; m = [(r, i, e) + k2[round(r, 2)] for r, i, e in a1 if round(r, 2) in k2]
    a = np.array(m); a1, a2 = a[:, :3], a[:, [0, 3, 4]]
    ok = (a1[:, 1] > 0) & (a2[:, 1] > 0) & (a1[:, 1] >= 10 * a1[:, 2]) & (a2[:, 1] >= 10 * a2[:, 2])
    r = a1[ok, 0] * 0.75; c = -2.5 * np.log10(a1[ok, 1] / a2[ok, 1]) + ZPC
    return r, c, None


def img_profile(path, ra, dec, pa, ba, edges):
    from astropy.io import fits
    from astropy.wcs import WCS
    with fits.open(path, memmap=False) as h:
        hdu = next(x for x in h if x.data is not None and getattr(x.data, "ndim", 0) == 2); data = np.asarray(hdu.data, float); w = WCS(hdu.header)
    yy, xx = np.mgrid[0:data.shape[0], 0:data.shape[1]]
    cx, cy = w.all_world2pix(ra, dec, 0); rmax = edges[-1] * 2.0
    scale = abs(w.proj_plane_pixel_scales()[0].to_value("arcsec")) if hasattr(w.proj_plane_pixel_scales()[0], "to_value") else abs(w.proj_plane_pixel_scales()[0]) * 3600
    half = int(rmax / scale) + 5
    y0, y1, x0, x1 = max(0, int(cy) - half), min(data.shape[0], int(cy) + half), max(0, int(cx) - half), min(data.shape[1], int(cx) + half)
    sub = data[y0:y1, x0:x1]; X, Y = xx[y0:y1, x0:x1], yy[y0:y1, x0:x1]
    wra, wde = w.all_pix2world(X.ravel(), Y.ravel(), 0)
    dx = ((wra - ra + 540) % 360 - 180) * math.cos(math.radians(dec)) * 3600; dy = (wde - dec) * 3600
    dx, dy, v = dx.reshape(sub.shape), dy.reshape(sub.shape), sub
    fin = np.isfinite(v)
    def clipmean(vals):
        vals = vals[np.isfinite(vals)]
        if len(vals) < 5:
            return np.nan, np.nan, 0
        med = np.median(vals); sig = 1.4826 * np.median(np.abs(vals - med)); keep = vals <= med + 5 * sig
        return float(np.mean(vals[keep])), float(sig), int(keep.sum())
    if pa is None:                                                      # PA from intensity-weighted second moments within 60"
        rc = np.hypot(dx, dy); bgm, _, _ = clipmean(v[fin & (rc > 1.5 * edges[-1]) & (rc < 2.0 * edges[-1])])
        k = fin & (rc < 60); wgt = np.clip(v[k] - bgm, 0, None)
        mxx, myy, mxy = (wgt * dx[k] ** 2).sum(), (wgt * dy[k] ** 2).sum(), (wgt * dx[k] * dy[k]).sum()
        th = 0.5 * math.atan2(2 * mxy, mxx - myy); pa = (90.0 - math.degrees(th)) % 180.0
    s, c = math.sin(math.radians(pa)), math.cos(math.radians(pa))
    a = dx * s + dy * c; b = -dx * c + dy * s; rell = np.sqrt(a ** 2 + (b / ba) ** 2)
    bg, bgs, _ = clipmean(v[fin & (rell >= 1.5 * edges[-1]) & (rell < 2.0 * edges[-1])])
    prof = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        mval, _, npx = clipmean(v[fin & (rell >= lo) & (rell < hi)])
        I = mval - bg; err = bgs / math.sqrt(max(npx, 1))
        prof.append((0.5 * (lo + hi), I, err))
    return np.array(prof), pa


def img_colour(name, Rmax_as):
    pos = {r["sparc_name"]: (float(r["ra_deg"]), float(r["dec_deg"])) for r in csv.DictReader(open(os.path.join(EXT, "cosmicflows4", "sesame_sparc.csv"))) if r["ra_deg"]}
    ra, dec = pos[name]; inc = META[name]["meta"]["Inc"]; ba = max(math.cos(math.radians(inc)), 0.1)
    files = {"UGC00128": ("images/ugc00128_irac_seip/50059080.50059080-0.IRAC.1.mosaic.fits", "images/ugc00128_irac_seip/50059080.50059080-0.IRAC.2.mosaic.fits"),
             "UGC00731": ("images/ugc00731_irac_pbcd/SPITZER_I1_40287488_0000_2_E11351845_maic.fits", "images/ugc00731_irac_pbcd/SPITZER_I2_40287488_0000_2_E11354434_maic.fits")}[name]
    edges = np.arange(0.0, max(Rmax_as, 30.0) + 6.0, 6.0)
    p1, pa = img_profile(os.path.join(FG, files[0]), ra, dec, None, ba, edges)
    p2, _ = img_profile(os.path.join(FG, files[1]), ra, dec, pa, ba, edges)
    ok = (p1[:, 1] > 0) & (p2[:, 1] > 0) & (p1[:, 1] >= 10 * p1[:, 2]) & (p2[:, 1] >= 10 * p2[:, 2])
    return p1[ok, 0], -2.5 * np.log10(p1[ok, 1] / p2[ok, 1]) + ZPC, dict(pa=pa, ba=ba, r36=p1[ok, 0], I36=p1[ok, 1], n_valid=int(ok.sum()))


def runmed(x, k=5):
    h = k // 2
    return np.array([np.median(x[max(0, i - h):i + h + 1]) for i in range(len(x))])


# ------------------------------------------------------------------------------------------------ thin-disc multiplier
def vdisk2(Rs, Sig, Rd):
    """thin-disc V^2 (arbitrary units) at radii Rs from Sigma at radii Rs (kpc), Hankel transform, exponential tail."""
    lo = np.log(np.clip(Sig[-3:], 1e-30, None)); sl = np.polyfit(Rs[-3:], lo, 1)[0]; h = -1.0 / sl if sl < 0 else Rd
    Rf = np.linspace(0, Rs[-1] + 12 * h, 6000)[1:]
    Sf = np.where(Rf <= Rs[-1], np.exp(np.interp(Rf, Rs, np.log(np.clip(Sig, 1e-30, None)))), Sig[-1] * np.exp(-(Rf - Rs[-1]) / h))
    Sf = np.where(Rf < Rs[0], Sig[0], Sf)
    kk = np.logspace(math.log10(0.01 / Rf[-1]), math.log10(400.0 / max(Rs[0], 0.02)), 3000)
    S = np.array([np.trapz(Sf * j0(k * Rf) * Rf, Rf) for k in kk])
    return np.array([R * np.trapz(kk * S * j1(kk * R), kk) for R in Rs])


def multiplier(Rs, SBd, cR, beta, Rd):
    if beta == 0.0:
        return np.ones_like(Rs)
    w = SBd * Rs; cbar = float(np.sum(w * cR) / np.sum(w)); U = 10 ** (beta * (cR - cbar))
    v0 = vdisk2(Rs, SBd, Rd); v1 = vdisk2(Rs, SBd * U, Rd)
    return np.where(v0 > 0, v1 / np.where(v0 > 0, v0, 1), 1.0)


# ------------------------------------------------------------------------------------------------ controls K2a/K2
y = np.linspace(0.1, 5, 40); Rs_t = y; ft = vdisk2(Rs_t, np.exp(-Rs_t), 1.0); fr = (Rs_t / 2) ** 2 * (i0(Rs_t / 2) * k0(Rs_t / 2) - i1(Rs_t / 2) * k1(Rs_t / 2))
k2a = float(np.max(np.abs(ft / ft.max() / (fr / fr.max()) - 1)[Rs_t > 0.3]))
P(f"  [{'PASS' if k2a <= 0.01 else 'FAIL'}] K2a (added check) Hankel code vs Freeman exponential disc: max |dev| {k2a:.4f} beyond 0.3 h")

RES = {"lane": "AG4i", "mutate": MUT, "galaxies": {}}
for name in FIVE:
    md = META[name]; meta = md["meta"]; rm = rotmod(name); Dm = meta["D"]; inc = meta["Inc"]
    P(f"\n=== {name}  (AG4g pull {PULL4G[name]:+.2f}; D {Dm} Mpc, i {inc}, Q {meta['Q']}) ===")
    gas2 = np.sign(rm["Vg"]) * rm["Vg"] ** 2; Vd2 = rm["Vd"] ** 2; Vb2 = rm["Vb"] ** 2
    base = make(rm["R"], rm["Vo"], rm["eV"], gas2, Vd2, Vb2, md["cg"])
    p0 = pull1(base); k1 = abs(p0 - PULL4G[name]) < 1e-12
    P(f"  [{'PASS' if k1 else 'FAIL'}] K1 SPARC curve, beta 0: pull {p0:+.2f} (AG4g {PULL4G[name]:+.2f})")
    G = dict(K1=k1, variants={})
    # K2: thin-disc shape vs SPARC Vdisk
    v0 = vdisk2(rm["R"], np.clip(rm["SBd"], 1e-6, None), meta["Rdisk"]); okv = (rm["Vd"] > 0) & (v0 > 0)
    sh = np.sqrt(v0[okv] / v0[okv].max()) / (rm["Vd"][okv] / rm["Vd"][okv].max()); k2 = bool(np.all(np.abs(sh[1:] - 1) <= 0.15))
    P(f"  [{'PASS' if k2 else 'FAIL'}] K2 thin-disc shape vs SPARC Vdisk within 15%: max |dev| {np.max(np.abs(sh[1:] - 1)):.3f}")
    G["K2"] = k2
    # colour profile
    Rmax_as = rm["R"][-1] / (Dm * 1e3 * AS2RAD)
    if name in ("UGC00128", "UGC00731"):
        r_as, c, info = img_colour(name, Rmax_as)
        if info["n_valid"] >= 3:
            Ras = rm["R"] / (Dm * 1e3 * AS2RAD); inr = (Ras >= info["r36"][0]) & (Ras <= info["r36"][-1]) & (rm["SBd"] > 0)
            if inr.sum() >= 4:
                d_ = -2.5 * np.log10(np.interp(Ras[inr], info["r36"], info["I36"])) + 2.5 * np.log10(rm["SBd"][inr]); k3rms = float(np.std(d_))
            else:
                k3rms = float("inf")
        else:
            k3rms = float("inf")
        k3 = k3rms <= 0.3
        P(f"  [{'PASS' if k3 else 'FAIL'}] K3 own 3.6 um profile vs SPARC SBdisk shape: rms {k3rms:.2f} mag (PA {info['pa']:.1f}, b/a {info['ba']:.2f}, valid annuli {info['n_valid']})")
        G["K3"] = dict(ok=k3, rms=k3rms, pa=info["pa"], n_valid=info["n_valid"])
        colour_ok = k3
    else:
        r_as, c, _ = s4g_colour(name); colour_ok = len(r_as) >= 3
    if colour_ok:
        c = runmed(c); Rk = r_as * Dm * 1e3 * AS2RAD
        cR = np.interp(rm["R"], Rk, c, left=c[0], right=c[-1])
        P(f"  colour [3.6]-[4.5] (Vega): {len(c)} valid radii {r_as[0]:.0f}-{r_as[-1]:.0f}\"; range {c.min():+.3f}..{c.max():+.3f}; at SPARC radii {cR.min():+.3f}..{cR.max():+.3f}")
    # independent curve
    ind = None
    if name in ("NGC5985", "UGC00731", "UGC08286"):
        Ri, Vi, ei, nraw = indep_curve(name, Dm, inc)
        inr = (Ri >= rm["R"][0]) & (Ri <= rm["R"][-1]); Ri, Vi, ei = Ri[inr], Vi[inr], ei[inr]
        ind = (Ri, Vi, ei)
        vs = np.interp(Ri, rm["R"], rm["Vo"]); P(f"  independent curve: {nraw} raw points -> {len(Ri)} bins in SPARC range; K4 median V_ind/V_SPARC {np.median(Vi / vs):.3f}")
        G["K4"] = float(np.median(Vi / vs))
    ip = lambda arr, Rn: np.interp(Rn, rm["R"], arr)
    variants = []
    if ind is not None:
        variants.append(("K", "indep", 0.0))
    if colour_ok:
        for bn, bv in BETAS.items():
            variants.append((f"M {bn}", "sparc", bv))
            if ind is not None and bn.startswith("primary"):
                variants.append((f"K+M {bn}", "indep", bv))
    else:
        P("  M: NOT AVAILABLE (no valid colour profile / K3 failed)")
    for vn, curve, beta in variants:
        if MUT:
            curve, beta = "sparc", 0.0
        mR = multiplier(rm["R"], np.clip(rm["SBd"], 1e-6, None), cR, beta, meta["Rdisk"]) if (colour_ok and beta != 0.0) else np.ones_like(rm["R"])
        if curve == "sparc":
            d = make(rm["R"], rm["Vo"], rm["eV"], gas2, Vd2, Vb2, md["cg"], m=mR)
        else:
            Ri, Vi, ei = ind
            d = make(Ri, Vi, ei, ip(gas2, Ri), ip(Vd2, Ri), ip(Vb2, Ri), md["cg"], m=ip(mR, Ri))
        if d["n"] < 5:
            P(f"  {vn:22s} too few points ({d['n']})"); continue
        j = judge(d); j["m_range"] = [float(mR.min()), float(mR.max())]; G["variants"][vn] = j
        P(f"  {vn:22s} pull {j['pull']:+5.2f}  p_emp {j['p_emp']:.3f}  mock sd {j['mock_sd']:.2f}  shape dchi2 {j['dchi2_shape']:6.1f}  n {j['n']:3d}  m(R) {mR.min():.2f}-{mR.max():.2f}  -> {j['reading']}")
    V = G["variants"]; res_ = lambda k: k in V and V[k]["reading"] == "RESOLVED"
    if any(res_(k) for k in V if k == "K"):
        cls = "KINEMATIC"
    elif res_("M primary 3.98"):
        cls = "M/L GRADIENT"
    elif res_("K+M primary 3.98"):
        cls = "BOTH NEEDED"
    elif V and all(V[k]["reading"] == "PERSISTS" for k in V):
        cls = "UNEXPLAINED"
    elif V and all(V[k]["reading"] != "RESOLVED" for k in V):
        cls = "NOT RESOLVED, but WEAK in: " + ", ".join(k for k in V if V[k]["reading"] == "WEAK")
    else:
        cls = "UNEXPLAINED (primary); resolved only in a variant: " + ", ".join(k for k in V if res_(k))
    if not V:
        cls = "NO VARIANT AVAILABLE"
    G["class"] = cls; P(f"  CLASS: {cls}")
    RES["galaxies"][name] = G

if MUT:
    allp = all(all(abs(v["pull"]) >= 3 - 1e-9 and v["reading"] in ("PERSISTS", "WEAK") for v in G["variants"].values()) for G in RES["galaxies"].values() if G["variants"])
    P(f"\nMUTATE (SPARC curve, beta 0): all variants keep |pull| >= 3 -> {'control BITES (exit 1, as designed)' if allp else 'control DID NOT BITE (recorded)'}")
    json.dump(RES, open(os.path.join(HERE, f"ag4i_results{TAG}.json"), "w"), indent=1, default=float); OUT.close(); sys.exit(1 if allp else 0)
P("\nSUMMARY: " + "; ".join(f"{n}: {RES['galaxies'][n]['class']}" for n in FIVE))
fails = [n for n in FIVE if not RES["galaxies"][n]["K1"]]
P(f"K1 failures: {fails or 'none'}; K2 failures: {[n for n in FIVE if not RES['galaxies'][n]['K2']] or 'none'}")
json.dump(RES, open(os.path.join(HERE, "ag4i_results.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(1 if fails else 0)
