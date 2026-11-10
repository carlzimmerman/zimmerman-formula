"""GO1 Part A step 2 (FROZEN_CRITERIA.md c1a9527ebf): per-group KiDS-1000 shear and ACT y in x = R/R500 bins, for the eRASS1 groups
of Lovisari's gas-mass range and their randoms. Estimator copied verbatim from CFG686 (cfg686_shear.py esd(): e2-flipped tangential
sign, inverse-Sigma_crit^2 weights, m = -0.01, Z_B > z_l + 0.2, Z_B <= 1.2, BAO-raw distances); only the bin edges change (x units).
y strip read by memmap with FR3's geometry. Preemptible: checkpoint to argv[2] every 20 groups; SIGTERM saves and exits; reruns resume.
python3 -I go1_measure.py <kids column dir> <checkpoint.npz>. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, math, time, signal, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter
from astropy.io import fits
from astropy.wcs import WCS
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); EXT = os.path.join(os.path.dirname(REPO), "_external_data")
COLS, CKPT = sys.argv[1], sys.argv[2]
G = 6.674e-11; c = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; KG_PER_MSUN_PC2 = MSUN/(3.0857e16)**2; M_BIAS = -0.01
# ---- distances from raw DESI DR2 BAO (CFG686 verbatim) ----
zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
pch = PchipInterpolator(np.r_[0, 0.295, zb], np.r_[0, DMb, DMr]); RD = 101.54/0.70
def DM(z): z = np.asarray(z, float); return pch(np.minimum(z, 2.33))*RD
# ---- frozen radial grid ----
EDGES = np.geomspace(0.25, 16.0, 13); NB = 12; XMAX = EDGES[-1]
YEDGES = np.r_[0.0, EDGES]; NY = len(YEDGES) - 1                               # y: inner disc 0-0.25 + the 12 annuli
# ---- groups (CFG687's parser; frozen selection) ----
def boxes(ra, de):
    inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
    return ("N" if inN else "S" if inS else None)
GR = []
for r in (l.rstrip("\n").split("\t") for l in open(os.path.join(EXT, "cfg687_inputs", "erass1_main.tsv"))):
    try: ra, de, z, mg, R5, M5 = float(r[1]), float(r[2]), float(r[3]), float(r[5])*1e11, float(r[8])/1e3, float(r[10])*1e13
    except Exception: continue
    b = boxes(ra, de)
    if b and -35 < de < 3.5 and 0.05 <= z <= 0.30 and 1.35e12 <= mg <= 1.15e13 and R5 > 0 and M5 > 0:
        GR.append(dict(name=r[0].strip(), ra=ra, dec=de, z=z, Mgas500=mg, R500=R5, M500=M5, box=b))
print(f"selected eRASS1 groups (box x strip x gas range x z 0.05-0.30): {len(GR)}", flush=True)
# ---- sources (CFG686 verbatim) ----
ra_s = np.load(os.path.join(COLS, "kids_ra.npy")); de_s = np.load(os.path.join(COLS, "kids_dec.npy"))
e1 = np.load(os.path.join(COLS, "kids_e1.npy")).astype(float); e2 = np.load(os.path.join(COLS, "kids_e2.npy")).astype(float)
ws = np.load(os.path.join(COLS, "kids_w.npy")).astype(float); zs = np.load(os.path.join(COLS, "kids_zb.npy")).astype(float)
ok = np.isfinite(ra_s) & np.isfinite(e1) & (ws > 0) & (zs <= 1.2); ra_s, de_s, e1, e2, ws, zs = ra_s[ok], de_s[ok], e1[ok], e2[ok], ws[ok], zs[ok]
def xyz(ra, de): ra, de = np.radians(ra), np.radians(de); return np.c_[np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)]
tree = cKDTree(xyz(ra_s, de_s)); DMs = DM(zs); print(f"sources {len(zs):,}", flush=True)
def esd_x(ra, de, zl, R500):
    """CFG686 esd() with bins in x = R/R500; returns tangential and cross sums per bin plus the x 1-5 weight/variance/count."""
    Dl_M = float(DM(zl)); Dl = Dl_M/(1 + zl); th = XMAX*R500/Dl*1.02
    ii = np.array(tree.query_ball_point(xyz(np.array([ra]), np.array([de]))[0], 2*np.sin(th/2)), int)
    if ii.size < 10: return None
    ii = ii[zs[ii] > zl + 0.2]
    dra = (np.radians(ra_s[ii]) - np.radians(ra))*np.cos(np.radians(de)); dra = (dra + np.pi) % (2*np.pi) - np.pi; dde = np.radians(de_s[ii]) - np.radians(de)
    R = np.hypot(dra, dde)*Dl; phi = np.arctan2(dde, dra); x = R/R500
    et = -(e1[ii]*np.cos(2*phi) - e2[ii]*np.sin(2*phi)); ex = -(e1[ii]*np.sin(2*phi) + e2[ii]*np.cos(2*phi))
    Dls = (DMs[ii] - Dl_M)/(1 + zs[ii]); Ds = DMs[ii]/(1 + zs[ii])
    isc = 4*np.pi*G/c**2*(Dl*MPC)*(Dls/Ds); isc = np.clip(isc, 0, None)
    k = np.digitize(x, EDGES) - 1; g = (k >= 0) & (k < NB) & (isc > 0)
    ww = ws[ii]*isc**2; vt = et/np.where(isc > 0, isc, 1); vx = ex/np.where(isc > 0, isc, 1)
    out = dict(numt=np.bincount(k[g], (ww*vt)[g], NB), numx=np.bincount(k[g], (ww*vx)[g], NB), den=np.bincount(k[g], ww[g], NB),
               var=np.bincount(k[g], (ww**2*vt**2)[g], NB), n=np.bincount(k[g], minlength=NB)[:NB])
    b = g & (x >= 1) & (x <= 5); out["n15"] = int(b.sum()); out["den15"] = float(ww[b].sum()); out["var15"] = float((ww[b]**2*vt[b]**2).sum())
    return out
# ---- y strips (FR3 geometry, memmap) ----
NX, R0, R1 = 43200, 3239, 8040; NR = R1 - R0 + 1; PIX = 0.5; BM = 1.6/(2*math.sqrt(2*math.log(2)))/PIX
YM = {m: np.memmap(os.path.join(EXT, "act_dr6_nilc", f"strip_{m}.f32be"), dtype=">f4", mode="r", shape=(NR, NX)) for m in ("ComptonY", "ComptonY_deproj_cib_1.0_10.7")}
cof = lambda ra: 21600.0 - 120.0*(ra - 360 if ra >= 180 else ra); rof = lambda de: 7559.5 + 120.0*de
hd = fits.Header.fromstring(open(os.path.join(EXT, "act_dr6_nilc", "header_ComptonY.fits"), "rb").read(2880).decode("ascii"))
tp = np.array([[12.3, -5.0], [133.7, 1.2], [200.1, -30.5], [355.2, 2.9]]); px = WCS(hd).all_world2pix(tp, 0)
GEO = max(max(abs(cof(a) - p[0]), abs(rof(b) - p[1])) for (a, b), p in zip(tp, px)); print(f"KA3a map geometry vs WCS: {GEO:.1e} pix ({'PASS' if GEO < 0.01 else 'FAIL'})", flush=True)
def gnfw(x): cc, a, b, gg = 1.177, 1.051, 5.4905, .3081; u = cc*np.maximum(x, 1e-4); return u**-gg*(1 + u**a)**((gg - b)/a)
def beta_p(x): return (1 + (np.maximum(x, 0)/0.15)**2)**-1.5                    # isothermal beta = 2/3 pressure (KA3 test shape)
SS = np.geomspace(1e-4, 64, 3000); RG = np.geomspace(1e-3, 20, 500)
def yproj(f): return np.array([2*np.trapz(f(np.sqrt(R*R + SS*SS)), SS) for R in RG])
YT = {"gnfw": yproj(gnfw), "beta": yproj(beta_p)}
def y_ann(ra, de, th, templates=False):
    """mean y per annulus (inner disc + 12), valid fraction; th = theta500 in arcmin. Optional noise-free templates (raw / beam)."""
    cosd = math.cos(math.radians(de)); hw = int(math.ceil(XMAX*1.01*th/PIX/cosd)) + 2; hh = int(math.ceil(XMAX*1.01*th/PIX)) + 2
    cx = cof(ra); cy = rof(de) - R0; ic = int(round(cx)); iy = int(round(cy))
    if iy - hh < 0 or iy + hh + 1 > NR: return None
    cols = np.arange(ic - hw, ic + hw + 1) % NX
    yy, xx = np.indices((2*hh + 1, 2*hw + 1)); rr = np.hypot((xx - hw - (cx - ic))*cosd, yy - hh - (cy - iy))*PIX/th
    k = np.digitize(rr, YEDGES) - 1; inb = (k >= 0) & (k < NY); out = {}
    for m, Y in YM.items():
        img = np.asarray(Y[iy - hh:iy + hh + 1][:, cols], dtype=float); val = np.isfinite(img) & (img != 0) & inb
        tot = np.bincount(k[inb], minlength=NY)[:NY]; nv = np.bincount(k[val], minlength=NY)[:NY]; s = np.bincount(k[val], img[val], NY)
        out[m] = s/np.maximum(nv, 1); out["vf_" + m] = nv/np.maximum(tot, 1)
    if templates:
        for t, yt in YT.items():
            im = np.interp(rr, RG, yt, right=0.0); cnt = np.bincount(k[inb], minlength=NY)[:NY]
            out["tr_" + t] = np.bincount(k[inb], im[inb], NY)/np.maximum(cnt, 1)
            imb = gaussian_filter(im, (BM, BM/cosd)); out["tb_" + t] = np.bincount(k[inb], imb[inb], NY)/np.maximum(cnt, 1)
    return out
def y_ok(o): return o is not None and all(o["vf_" + m].min() >= 0.90 for m in YM)
# ---- measure, checkpointed ----
STOP = [False]; signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__(0, True))
done = dict(np.load(CKPT, allow_pickle=True))["res"].item() if os.path.exists(CKPT) else {}
print(f"resuming with {len(done)} groups already measured", flush=True)
rng = np.random.default_rng(20261110); T0 = time.time()
def save(): np.savez_compressed(CKPT + ".tmp.npz", res=np.array(done, dtype=object)); os.replace(CKPT + ".tmp.npz", CKPT)
for i, g in enumerate(GR):
    rs = np.random.default_rng([20261110, i])                                     # per-group stream: resumable and order-free
    if i in done: continue
    Dl = float(DM(g["z"]))/(1 + g["z"]); th = g["R500"]/Dl*180/math.pi*60
    rec = dict(g, th500=th, keep=False, why="")
    m = esd_x(g["ra"], g["dec"], g["z"], g["R500"])
    yo = y_ann(g["ra"], g["dec"], th, templates=True)
    if m is None or m["n15"] < 200: rec["why"] = "sources"
    elif (m["n"] == 0).any(): rec["why"] = "empty bin"
    elif not y_ok(yo): rec["why"] = "y mask"
    else:
        rnd = []
        for _ in range(16):
            if g["box"] == "N": ra_r, de_r = rs.uniform(125, 240), rs.uniform(-6, 3.5)
            else: ra_r, de_r = rs.uniform(-35, 60) % 360, rs.uniform(-35, -25)
            mr = esd_x(ra_r, de_r, g["z"], g["R500"])
            if mr is None or mr["n15"] < 0.5*m["n15"] or (mr["n"] == 0).any(): continue
            yr = y_ann(ra_r, de_r, th)
            if not y_ok(yr): continue
            rnd.append(dict(ra=ra_r, dec=de_r, shear=mr, y=yr))
            if len(rnd) >= 4: break
        a = rs.uniform(0, 2*np.pi); s = rs.uniform(1, 3)                       # MUTATE M2: y at a position shifted 1-3 deg
        ys = y_ann((g["ra"] + s*np.cos(a)/math.cos(math.radians(g["dec"]))) % 360, float(np.clip(g["dec"] + s*np.sin(a), -34.5, 3.0)), th)
        if len(rnd) < 2: rec["why"] = "randoms"
        else: rec.update(keep=True, shear=m, y=yo, rnd=rnd, yshift=ys if y_ok(ys) else None)
    done[i] = rec
    if len(done) % 20 == 0 or STOP[0]:
        save(); print(f"  {len(done)}/{len(GR)} groups, kept {sum(r['keep'] for r in done.values())}, {time.time() - T0:.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
    if STOP[0]: print("SIGTERM: checkpoint saved, exiting", flush=True); sys.exit(0)
save(); print(f"done: {len(done)} groups, kept {sum(r['keep'] for r in done.values())}; drop reasons " +
              str({w: sum(r['why'] == w for r in done.values()) for w in ('sources', 'empty bin', 'y mask', 'randoms')}), flush=True)
