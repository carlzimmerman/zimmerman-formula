#!/usr/bin/env python3
"""CFG569: KURVS-15 (cdfs_31127, z 1.613) archival ALMA CO -> measured gas shape -> CFG385 self-calibrated a0 fit.
Criteria: FROZEN_CRITERIA.md (committed alone first, 83f1d4ba0). ONE GALAXY = a demonstration, never an a0(z) verdict.
kappa = 1/2 FITTED; both a0 footings; cold mass still required.
Modes (env MODE): main | MUTATE_B (injection into Ibar B3) | MUTATE_A (gas shape -> exponential; only if a shape was measured).
Data: campaign_fresh_gravity/_external_data/cfg569/ (git-ignored). Outputs named by mode.
"""
import os, sys, json, math, gzip, shutil, hashlib
import numpy as np
from astropy.io import fits
from astropy.cosmology import Planck18
from scipy.special import ellipk

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
EXT = os.path.join(CFG, "_external_data", "cfg569")
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
sys.path.insert(0, os.path.join(CFG, "CFG44_fluid_target"))
from Bcommon import nu_mono, nu_p2  # read-only import (kernels only)

MODE = os.environ.get("MODE", "main")
OUT = []
CHECKS = []


def say(s=""):
    print(s)
    OUT.append(s)


def check(name, ok, val):
    CHECKS.append((name, bool(ok), str(val)))
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


C = 299792.458
Z = 1.613
RA0, DEC0 = 53.070583, -27.834461
NU21 = 230.538 / (1 + Z)
NU54 = 576.268 / (1 + Z)
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KPC_M = 3.0856775814913673e19
G = 4.30091727e-6
WIN, WIN2 = 300.0, 200.0
rng = np.random.default_rng(569)

M = {
    "ibar_b3": ("member.uid___A001_X133d_X7a8.cdfs_31127_sci.spw29.cube.I.pbcor.fits",
                "member.uid___A001_X133d_X7a8.cdfs_31127_sci.spw29.cube.I.pb.fits.gz", NU21),
    "ibar_b6": ("member.uid___A001_X133d_X7ac.cdfs_31127_sci.spw29.cube.I.pbcor.fits",
                "member.uid___A001_X133d_X7ac.cdfs_31127_sci.spw29.cube.I.pb.fits.gz", NU54),
    "molina_b3": ("member.uid___A001_X1465_X137f.CDFS_31127_sci.spw23.repBW.I.pbcor.fits",
                  "member.uid___A001_X1465_X137f.CDFS_31127_sci.spw23.repBW.I.pb.fits.gz", NU21),
}


def rd(p):
    import csv
    return list(csv.DictReader(open(p)))


# ---------------------------------------------------------------- record (R1)
say(f"CFG569 KURVS-15 archival CO self-calibration  MODE={MODE}")
say("=" * 78)
I = [r for r in rd(os.path.join(AT, "kurvs2023_integrated.csv")) if r["kurvs_id"] == "15"][0]
K = [r for r in rd(os.path.join(AT, "kurvs2023_kinematics.csv")) if r["kurvs_id"] == "15"][0]
V = [r for r in rd(os.path.join(AT, "kurvs2023_velocities_at_radii.csv")) if r["kurvs_id"] == "15"][0]
LM, RE, ISFR, ISTAR = float(I["logMstar"]), float(I["reff_kpc"]), float(I["inc_sfr_deg"]), float(I["inc_star_deg"])
SIG0, RMAX, VMAX = float(K["sigma0_kms"]), float(V["R_halpha_max_kpc"]), float(V["v_at_last_point_kms"])
MSTAR = 10 ** LM
RD = RE / 1.68
KPCAS = Planck18.kpc_proper_per_arcmin(Z).value / 60.0
DL = Planck18.luminosity_distance(Z).value
say(f"record: z {I['z_halpha']} logM* {LM} R_e {RE} i_SFR {ISFR} i* {ISTAR} sigma0 {SIG0} R_max {RMAX} V(R_max) {VMAX};"
    f" kpc/\" {KPCAS:.3f}, D_L {DL:.1f} Mpc")
mc = [r for r in rd(os.path.join(AT, "kurvs_rc_profiles", "kurvs_rc_model_curves.csv")) if r["kurvs_id"] == "15"]
mr = np.array([abs(float(r["R_kpc"])) for r in mc]); mv = np.array([abs(float(r["v_model_obs_kms"])) for r in mc])
o = np.argsort(mr)
vmod = np.interp(RMAX, mr[o], mv[o]) / math.sin(math.radians(ISFR))
check("R1 authors' model at R_max / sin i_SFR reproduces V(R_max) 112.2 within 2%", abs(vmod / VMAX - 1) < 0.02, f"{vmod:.1f}")
check("R1b table row as expected (z 1.613, logM* 10.07, R_e 3.8, i_SFR 38, sigma0 68, R_max 9.2)",
      (float(I["z_halpha"]), LM, RE, ISFR, SIG0, RMAX) == (1.613, 10.07, 3.8, 38.0, 68.0, 9.2), "read")


# ---------------------------------------------------------------- cubes
def open_cube(key):
    fp, fpb, nul = M[key]
    p = os.path.join(EXT, fp)
    pbp = os.path.join(EXT, fpb)
    pbu = pbp[:-3]
    if not os.path.exists(pbu):
        with gzip.open(pbp, "rb") as fi, open(pbu + ".part", "wb") as fo:
            shutil.copyfileobj(fi, fo, 1 << 24)
        os.replace(pbu + ".part", pbu)
    h = fits.open(p, memmap=True)
    hpb = fits.open(pbu, memmap=True)
    return h, hpb, nul


def axes(hd):
    n = hd["NAXIS3"]; ch = np.arange(n)
    nu = (hd["CRVAL3"] + (ch + 1 - hd["CRPIX3"]) * hd["CDELT3"]) / 1e9
    return nu


def beam(h):
    hd = h[0].header
    if "BMAJ" in hd:
        return hd["BMAJ"] * 3600, hd["BMIN"] * 3600, hd.get("BPA", 0.0)
    b = h["BEAMS"].data
    return float(np.median(b["BMAJ"])), float(np.median(b["BMIN"])), float(np.median(b["BPA"]))


def cube3(h):
    d = h[0].data
    return d[0] if d.ndim == 4 else d


def pix_of(hd):
    from astropy.wcs import WCS
    w = WCS(hd).celestial
    x, y = w.all_world2pix([[RA0, DEC0]], 0)[0]
    return float(x), float(y)


def mom0(cube, nu, nul, lo, hi):
    v = C * (nul - nu) / nul
    sel = np.where((v >= lo) & (v <= hi))[0]
    dv = abs(C * (nu[1] - nu[0]) / nul)
    m = np.zeros(cube.shape[1:], np.float64)
    for c in sel:  # channel by channel (memmap friendly)
        m += np.nan_to_num(np.asarray(cube[c], np.float64), nan=0.0)
    bad = ~np.isfinite(np.asarray(cube[sel[len(sel) // 2]]))
    m[bad] = np.nan
    return m * dv, len(sel), dv


def stat_at(m, x, y, rap, bpix):
    if rap <= 0:
        return float(m[int(round(y)), int(round(x))])
    ny, nx = m.shape
    r = int(math.ceil(rap)) + 1
    yi, xi = int(round(y)), int(round(x))
    if yi - r < 0 or xi - r < 0 or yi + r >= ny or xi + r >= nx:
        return float("nan")
    sub = m[yi - r:yi + r + 1, xi - r:xi + r + 1]
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    msk = (xx + xi - x) ** 2 + (yy + yi - y) ** 2 <= rap ** 2
    return float(np.sum(sub[msk]) / bpix)


def offsource(m, pb, x0, y0, rap, bpix, minsep, mindist, nmax=200):
    ny, nx = m.shape
    ok = np.isfinite(m) & (pb >= 0.5)
    ys, xs = np.where(ok)
    keep = []
    order = rng.permutation(len(xs))
    for i in order[:200000]:
        x, y = xs[i], ys[i]
        if math.hypot(x - x0, y - y0) < mindist:
            continue
        if any(math.hypot(x - a, y - b) < minsep for a, b in keep):
            continue
        s = stat_at(m, x, y, rap, bpix)
        if not np.isfinite(s):
            continue
        keep.append((x, y))
        if len(keep) >= nmax:
            break
    vals = np.array([stat_at(m, x, y, rap, bpix) for x, y in keep])
    return vals


def robust(v):
    return 1.4826 * np.median(np.abs(v - np.median(v)))


RES = {"mode": MODE, "checks": None}
DET = {}
for key in ("ibar_b3", "ibar_b6", "molina_b3"):
    say(f"\n--- {key} ---")
    h, hpb, nul = open_cube(key)
    hd = h[0].header
    nu = axes(hd)
    bmaj, bmin, bpa = beam(h)
    pixas = abs(hd["CDELT2"]) * 3600
    bpix = math.pi * bmaj * bmin / (4 * math.log(2)) / pixas ** 2
    cube = cube3(h)
    pbc = cube3(hpb)
    v = C * (nul - nu) / nul
    say(f"  shape {cube.shape}, nu {nu.min():.4f}-{nu.max():.4f} GHz, dchan {abs(nu[1]-nu[0])*1e3:.3f} MHz "
        f"({abs(C*(nu[1]-nu[0])/nul):.2f} km/s), beam {bmaj:.3f}x{bmin:.3f}\" PA {bpa:.0f}, pix {pixas:.4f}\", BUNIT {hd.get('BUNIT')}")
    check(f"H1 {key}: +-300 km/s window inside the spw", v.min() < -WIN and v.max() > WIN, f"v {v.min():.0f}..{v.max():.0f}")
    exp = {"ibar_b3": (1.8, 3.2), "ibar_b6": (0.6, 1.6), "molina_b3": (0.05, 0.4)}[key]
    check(f"H2 {key}: beam class", exp[0] <= math.sqrt(bmaj * bmin) <= exp[1], f"{math.sqrt(bmaj*bmin):.3f}\"")
    x0, y0 = pix_of(hd)
    pbplane = np.asarray(pbc[int(np.argmin(abs(v)))], np.float64)
    pb0 = float(pbplane[int(round(y0)), int(round(x0))])
    check(f"H3 {key}: source pb >= 0.9", pb0 >= 0.9, f"pb {pb0:.3f} at pixel ({x0:.1f},{y0:.1f})")
    check(f"H4 {key}: units Jy/beam", str(hd.get("BUNIT", "")).strip().lower() == "jy/beam", hd.get("BUNIT"))
    rap = 0.0 if key != "molina_b3" else 1.2 / pixas
    minsep = (bmaj / pixas) if rap == 0 else 2 * rap
    mindist = (6.0 if key != "molina_b3" else 3.0) / pixas
    rows = {}
    for lab, lo, hi in (("w300", -WIN, WIN), ("w200", -WIN2, WIN2)):
        m, nch, dv = mom0(cube, nu, nul, lo, hi)
        if MODE == "MUTATE_B" and key == "ibar_b3":
            sv = 300 / 2.3548
            frac = 0.5 * (math.erf(hi / (sv * math.sqrt(2))) - math.erf(lo / (sv * math.sqrt(2))))
            yy, xx = np.mgrid[:m.shape[0], :m.shape[1]]
            fw = math.sqrt(bmaj * bmin) / pixas
            m = m + 0.5 * frac * np.exp(-4 * math.log(2) * ((xx - x0) ** 2 + (yy - y0) ** 2) / fw ** 2)
        s = stat_at(m, x0, y0, rap, bpix)
        off = offsource(m, pbplane, x0, y0, rap, bpix, minsep, mindist)
        sg = robust(off)
        rows[lab] = dict(S=s, sigma=float(sg), snr=float(s / sg), n_off=int(len(off)), nchan=nch, dv=dv)
        say(f"  {lab}: S {s:+.4f} Jy km/s (stat {'peak pixel' if rap == 0 else '1.2in aperture'}), sigma {sg:.4f} "
            f"(MAD of {len(off)} off-source; plain std {np.std(off):.4f}), S/N {s/sg:+.2f}; {nch} chans")
        if lab == "w300":
            check(f"{key}: >= 50 off-source positions", len(off) >= 50, len(off))
            if key == "ibar_b3" and rap == 0:
                s2 = stat_at(m, x0, y0, 2.0 / pixas, bpix)
                rows[lab]["S_ap2"] = s2
                say(f"  reported: 2.0\"-radius aperture sum/beam {s2:+.4f} Jy km/s")
            mon = m
    # N1 line-free windows
    width = 2 * WIN
    edge = 0.05 * (v.max() - v.min())
    cen = []
    for sgn in (-1, 1):
        c = sgn * (600 + WIN)
        while v.min() + edge <= c - WIN and c + WIN <= v.max() - edge:
            cen.append(c); c += sgn * width
    zs = []
    for c in cen:
        m, _, _ = mom0(cube, nu, nul, c - WIN, c + WIN)
        s = stat_at(m, x0, y0, rap, bpix)
        off = offsource(m, pbplane, x0, y0, rap, bpix, minsep, mindist)
        zs.append(s / robust(off))
    zs = np.array(zs)
    if len(zs):
        check(f"N1 {key}: line-free windows at the source |median z| < 1.5, scatter 0.5-2 (n={len(zs)})",
              abs(np.median(zs)) < 1.5 and (len(zs) < 3 or 0.5 <= np.std(zs) <= 2.0),
              f"median {np.median(zs):+.2f}, std {np.std(zs):.2f}, z = {np.round(zs, 2).tolist()}")
    else:
        check(f"N1 {key}: line-free windows exist", False, "none fit inside the spw")
    DET[key] = dict(rows=rows, beam=[bmaj, bmin, bpa], pix=pixas, pb0=pb0, linefree_z=zs.tolist(), xy=[x0, y0])
    if key == "molina_b3":
        MOL = dict(m=mon, x0=x0, y0=y0, pixas=pixas, bmaj=bmaj, bmin=bmin, pb=pbplane, bpix=bpix)
    h.close(); hpb.close()


# ---------------------------------------------------------------- conversion
def mmol(S, aco):
    Lp = 3.25e7 * S * NU21 ** -2 * DL ** 2 * (1 + Z) ** -3
    return aco * Lp / 0.77


r = DET["ibar_b3"]["rows"]["w300"]
snr = r["snr"]
say("\n--- detection and conversion ---")
for aco in (4.36, 1.0):
    lim = mmol(3 * r["sigma"] + max(r["S"], 0) * 0, aco)
    say(f"  alpha_CO {aco}: M_mol(S measured {r['S']:+.4f}) = {mmol(r['S'], aco):.3e} Msun (mu {mmol(r['S'], aco)/MSTAR:+.2f});"
        f" 3-sigma limit S < {3*r['sigma']:.3f} Jy km/s -> M_mol < {lim:.3e} (mu < {lim/MSTAR:.2f})")
RES["mu_mol_3sig_limit"] = {str(a): mmol(3 * r["sigma"], a) / MSTAR for a in (4.36, 1.0)}
ib_det = snr >= 5
mol = DET["molina_b3"]["rows"]["w300"]
mol_det = mol["snr"] >= 5
say(f"  Ibar B3 CO(2-1) S/N {snr:+.2f} -> {'DETECTED' if ib_det else ('TENTATIVE' if snr >= 3 else 'NOT DETECTED')};"
    f" Molina S/N {mol['snr']:+.2f} -> {'DETECTED' if mol_det else 'NOT DETECTED'};"
    f" Ibar B6 CO(5-4) S/N {DET['ibar_b6']['rows']['w300']['snr']:+.2f} (reported only)")

if MODE == "MUTATE_B":
    # the injected line adds 0.5 x (window fraction) on top of whatever is there; recovered = S - (measured main S)
    main = json.load(open(os.path.join(HERE, "cfg569_results.json")))["det"]["ibar_b3"]["rows"]["w300"]["S"] if os.path.exists(
        os.path.join(HERE, "cfg569_results.json")) else 0.0
    sv = 300 / 2.3548
    fr = math.erf(WIN / (sv * math.sqrt(2)))
    rec = (r["S"] - main) / (0.5 * fr)
    check("MUTATE_B injected 0.5 Jy km/s line reads DETECTED", ib_det, f"S/N {snr:+.2f}")
    check("MUTATE_B recovered / injected (window fraction applied) within 30%", abs(rec - 1) < 0.3, f"{rec:.3f}")


# ---------------------------------------------------------------- rotation curve + span (descriptive; no a0 number)
pts = [x for x in rd(os.path.join(AT, "kurvs_rc_profiles", "kurvs_rc_points.csv")) if x["kurvs_id"] == "15" and x["clipped_white_marker"] == "0"]
R = np.array([abs(float(x["R_kpc"])) for x in pts]); vo = np.array([abs(float(x["v_obs_kms"])) for x in pts])
ev = np.array([float(x["err_up_kms"]) for x in pts])
INFL = math.sqrt(0.57 * KPCAS / 0.847)
RMIN = 0.285 * KPCAS


def gfreeman(Rk, Md, Rd):
    from scipy.special import i0 as I0, i1 as I1, k0 as K0, k1 as K1
    yy = Rk / (2 * Rd)
    v2 = 4 * math.pi * G * (Md / (2 * math.pi * Rd ** 2)) * Rd * yy ** 2 * (I0(yy) * K0(yy) - I1(yy) * K1(yy))
    return v2 / Rk


def g_ring_disc(Rk, redges, sig, z0=0.05):
    """in-plane radial acceleration of a thin axisymmetric disc of annuli (surface density sig on redges), ring sum."""
    rc = 0.5 * (redges[1:] + redges[:-1])
    nsub = 40
    out = np.zeros_like(Rk, float)
    for j in range(len(rc)):
        a = np.linspace(redges[j], redges[j + 1], nsub + 1); a = 0.5 * (a[1:] + a[:-1])
        ma = sig[j] * 2 * math.pi * a * (redges[j + 1] - redges[j]) / nsub
        for aa, mm in zip(a, ma):
            def phi(Rq):
                d2 = (Rq + aa) ** 2 + z0 ** 2
                k2 = 4 * Rq * aa / d2
                return -2 * G * mm * ellipk(k2) / (math.pi * np.sqrt(d2))
            e = 1e-3
            out += (phi(Rk * (1 + e)) - phi(Rk * (1 - e))) / (2 * e * Rk)  # inward magnitude dPhi/dR (sign fixed after run 1)
    return out


# disc-solver control: the ring sum on an exponential reproduces Freeman
re_ = np.linspace(0, 12 * RD, 241)
sige = MSTAR / (2 * math.pi * RD ** 2) * np.exp(-0.5 * (re_[1:] + re_[:-1]) / RD)
tr = np.array([2.0, 4.0, 8.0])
rat = g_ring_disc(tr, re_, sige) / gfreeman(tr, MSTAR, RD)
check("C_disc ring-sum exponential vs Freeman at 2/4/8 kpc within 3%", np.all(abs(rat - 1) < 0.03), np.round(rat, 4).tolist())

say("\n--- rotation-curve span (data property; no a0 number unless a gas shape is measured) ---")
SPAN = {}
for ilab, inc in (("i38", ISFR), ("i65", ISTAR)):
    for rlab, rmin in (("Rpsf", RMIN), ("R0.5", 0.5)):
        u = R >= rmin
        vr = vo[u] / math.sin(math.radians(inc))
        for plab in ("P0", "B10"):
            vc2 = vr ** 2 + (2 * SIG0 ** 2 * R[u] / RD if plab == "B10" else 0)
            g = vc2 / R[u]
            gb = gfreeman(R[u], MSTAR, RD)
            spa = float(g.max() / g.min())
            yb = {f: (float(gb.max() / (A0F[f] * KPC_M / 1e6)), float(gb.min() / (A0F[f] * KPC_M / 1e6))) for f in A0F}
            SPAN[f"{ilab}_{rlab}_{plab}"] = dict(n=int(u.sum()), R=[float(R[u].min()), float(R[u].max())], gobs_span=spa,
                                                 ystar_only_f1=yb)
            say(f"  {ilab} {rlab:4s} {plab:3s}: n {u.sum():2d}, R {R[u].min():.2f}-{R[u].max():.2f} kpc, g_obs max/min {spa:.2f}"
                f" (need >= 6.4); stars-only y (f=1) {yb['canonical'][0]:.2f} -> {yb['canonical'][1]:.2f} canonical,"
                f" {yb['alt'][0]:.2f} -> {yb['alt'][1]:.2f} alt (need >= 3 -> <= 0.3)")
prim = SPAN["i38_Rpsf_P0"]
span_ok_data = prim["gobs_span"] >= 6.4
say(f"  RESULT span criterion (primary i38/Rpsf/P0) g_obs max/min >= 6.4: {'MET' if span_ok_data else 'NOT MET'} ({prim['gobs_span']:.2f})")


# ---------------------------------------------------------------- the fit (only with a measured gas shape)
def fit(gshape_edges, gsig, mu, kern, plab, inc=ISFR, rmin=RMIN):
    u = R >= rmin
    Rk = R[u]
    vr = vo[u] / math.sin(math.radians(inc)); er = ev[u] * INFL / math.sin(math.radians(inc))
    vc = np.sqrt(vr ** 2 + (2 * SIG0 ** 2 * Rk / RD if plab == "B10" else 0)); ec = er * vr / vc
    gs = gfreeman(Rk, MSTAR, RD)
    gg = g_ring_disc(Rk, gshape_edges, gsig / np.sum(gsig * math.pi * (gshape_edges[1:] ** 2 - gshape_edges[:-1] ** 2))) * mu * MSTAR
    lf = np.linspace(-1.5, 1.5, 301); la = np.linspace(-2, 2, 401)
    nu_ = {"nu_mono": nu_mono, "P2": nu_p2, "expRAR": lambda y: 1 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-12))))}[kern]
    out = {}
    for f in A0F:
        a0 = A0F[f] * KPC_M / 1e6
        X2 = np.empty((len(lf), len(la)))
        for i, l1 in enumerate(lf):
            gb = 10 ** l1 * (gs + gg)
            for j, l2 in enumerate(la):
                y = gb / (a0 * 10 ** l2)
                vm = np.sqrt(nu_(y) * gb * Rk)
                X2[i, j] = np.sum(((vm - vc) / ec) ** 2)
        prof = X2.min(0); jb = int(np.argmin(prof)); ib = int(np.argmin(X2[:, jb]))
        inside = la[prof <= prof[jb] + 1]
        gb = 10 ** lf[ib] * (gs + gg); y = gb / (a0 * 10 ** la[jb])
        out[f] = dict(log_ratio=float(la[jb]), lo=float(inside.min()), hi=float(inside.max()), logf=float(lf[ib]),
                      chi2=float(prof[jb]), dof=int(len(Rk) - 2), y_in=float(y.max()), y_out=float(y.min()),
                      edge=bool(inside.min() <= la[0] or inside.max() >= la[-1]))
    return out


VERD = None
if not ib_det:
    VERD = "NOT POSSIBLE -- CO NOT DETECTED"
elif not mol_det:
    VERD = "NOT POSSIBLE -- GAS SHAPE UNMEASURED"
else:
    # gas shape from Molina (section 5)
    from scipy.ndimage import gaussian_filter
    m = MOL["m"]; pa = MOL["pixas"]
    sm_sig = math.sqrt(max(0.30 ** 2 - MOL["bmaj"] * MOL["bmin"], 0)) / 2.3548 / pa
    ms = gaussian_filter(np.nan_to_num(m), sm_sig) if sm_sig > 0 else np.nan_to_num(m)
    yy, xx = np.mgrid[:m.shape[0], :m.shape[1]]
    dx = (xx - MOL["x0"]) * pa; dy = (yy - MOL["y0"]) * pa
    ap = dx ** 2 + dy ** 2 <= 1.2 ** 2
    w = np.clip(ms[ap], 0, None)
    cxx, cyy, cxy = np.sum(w * dx[ap] ** 2), np.sum(w * dy[ap] ** 2), np.sum(w * dx[ap] * dy[ap])
    PA = 0.5 * math.atan2(2 * cxy, cxx - cyy)
    VERD = "DEMONSTRATION"
    RES["PA_rad"] = PA
    for ilab, inc in (("i38", ISFR), ("i65", ISTAR)):
        xr = dx * math.cos(PA) + dy * math.sin(PA); yr = (-dx * math.sin(PA) + dy * math.cos(PA)) / math.cos(math.radians(inc))
        rr = np.hypot(xr, yr)
        ed = np.arange(0, 1.2001, 0.15)
        prof = np.array([np.mean(ms[(rr >= ed[k]) & (rr < ed[k + 1])]) for k in range(len(ed) - 1)])
        nsd = robust(ms[(~ap) & (MOL["pb"] >= 0.5)])
        nb = np.array([max(np.sum((rr >= ed[k]) & (rr < ed[k + 1])) * (pa ** 2) / (math.pi * 0.30 ** 2 / (4 * math.log(2))), 1) for k in range(len(ed) - 1)])
        eprof = nsd / np.sqrt(nb)
        ngood = int(np.sum(prof / eprof >= 2))
        say(f"  gas profile {ilab}: PA {math.degrees(PA):.0f} deg; Sigma_CO annuli {np.round(prof/eprof,1).tolist()} sigma; "
            f"{ngood} annuli >= 2 sigma -> {'measured' if ngood >= 3 else 'POORLY MEASURED'}")
        RES[f"gas_profile_{ilab}"] = dict(edges_as=ed.tolist(), prof=prof.tolist(), err=eprof.tolist(), ngood=ngood)
        if ilab == "i38":
            GED = ed * KPCAS; GSIG = np.clip(prof, 0, None)
    S_tot = r["S"]
    FITS = {}
    for aco in (4.36, 1.0):
        mu = mmol(S_tot, aco) / MSTAR
        for plab in ("P0", "B10"):
            for kern in ("nu_mono", "P2", "expRAR"):
                if MODE == "MUTATE_A":
                    gsig_use = np.exp(-0.5 * (GED[1:] + GED[:-1]) / RD)
                else:
                    gsig_use = GSIG
                fr_ = fit(GED, gsig_use, mu, kern, plab)
                FITS[f"a{aco}_{plab}_{kern}"] = fr_
                c = fr_["canonical"]; a = fr_["alt"]
                say(f"  aCO {aco} {plab} {kern:7s}: a0(1.6)/a0(0) canonical {10**c['log_ratio']:.2f} [{10**c['lo']:.2f},{10**c['hi']:.2f}]"
                    f"{' GRID-EDGE' if c['edge'] else ''} alt {10**a['log_ratio']:.2f} [{10**a['lo']:.2f},{10**a['hi']:.2f}];"
                    f" chi2 {c['chi2']:.1f}/{c['dof']}; y {c['y_in']:.2f}->{c['y_out']:.2f}")
    RES["fits"] = FITS
    p = FITS["a4.36_P0_nu_mono"]["canonical"]
    if not (span_ok_data and p["y_in"] >= 3 and p["y_out"] <= 0.3):
        VERD += ", SPAN-LIMITED"
    else:
        VERD += ", SPAN OK"
    if MODE == "MUTATE_A":
        base = json.load(open(os.path.join(HERE, "cfg569_results.json")))["fits"]["a4.36_P0_nu_mono"]["canonical"]["log_ratio"]
        d = p["log_ratio"] - base
        say(f"  MUTATE_A: exponential gas shape moves log a0 by {d:+.3f} dex")
        RES["mutateA_shift_dex"] = d

if MODE == "MUTATE_A" and not (ib_det and mol_det):
    say("  MUTATE_A cannot run: no measured gas shape exists (disclosed per the frozen plan).")

say(f"\nVERDICT ({MODE}): {VERD}. One galaxy: a demonstration at most; it cannot decide a0(z).")
nfail = sum(1 for c in CHECKS if not c[1])
say(f"checks: {len(CHECKS)-nfail}/{len(CHECKS)} pass")
RES.update(verdict=VERD, det=DET, span=SPAN, checks=CHECKS, ib_snr=snr, molina_snr=mol["snr"])
suf = "" if MODE == "main" else "_" + MODE
json.dump(RES, open(os.path.join(HERE, f"cfg569_results{suf}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg569{suf}.out"), "w").write("\n".join(OUT) + "\n")
rc = 0 if nfail == 0 else 1
if MODE == "MUTATE_A" and "mutateA_shift_dex" in RES and abs(RES["mutateA_shift_dex"]) > 0.1:
    rc = 1
sys.exit(rc)
