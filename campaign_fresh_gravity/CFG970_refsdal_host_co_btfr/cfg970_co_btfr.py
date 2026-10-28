"""CFG970: SN Refsdal host CO(3-2) from ALMA 2013.1.00582.S A1.4 - detection, flux, edge clipping, W50/W20, apparent gas mass, and the BTFR check
through the magnification the law would need (mu*). Criteria: FROZEN_CRITERIA.md (1b0dee952f). Single thread, plane by plane, RSS < 1 GB.
Run:  nice python3 cfg970_co_btfr.py           -> cfg970.out, cfg970_results.json, cfg970_*.png
      MUTATE=1 nice python3 cfg970_co_btfr.py  -> channels shuffled (default_rng(9701)); primary S/N must fall below 3 (rc 1)
Implementation choices (disclosed in README): detection on the flat-noise frame F = pbcor x PB; the 2x-beam-smoothed field is sampled every 4th
pixel (0.32") for the 3-D labelling; fluxes are summed on the full-resolution pbcor grid; PB is read from the beam cube at the line-centre plane."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, gzip, hashlib, resource, time, numpy as np
from astropy.io import fits
from astropy.wcs import WCS, FITSFixedWarning
import warnings; warnings.filterwarnings("ignore", category=FITSFixedWarning)
from scipy import ndimage
from scipy.interpolate import PchipInterpolator

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
DD = os.path.join(os.path.dirname(REPO), "_external_data", "alma_2013.1.00582.S_A1.4")
F_CUBE = os.path.join(DD, "member.uid___A001_X12b_Xa.MACS1149_A1.4_CO_v_0_3_2_image.pbcor.fits")
F_PB = os.path.join(DD, "member.uid___A001_X12b_Xa.MACS1149_A1.4_CO_v_0_3_2_image.flux.fits.gz")
F_CONT = [os.path.join(DD, "member.uid___A001_X12b_Xa.calibrated_final_cont_A1.4_image.pbcor.fits"),
          os.path.join(DD, "member.uid___A001_X12b_Xa.calibrated_final_cont_A1.4_image.flux.fits.gz")]
SHA = {F_CUBE: "64fb0ec2415b625711b64cb1511abe4526e528703f08c792421ef7baa034dc38", F_PB: "04dce427ca0371357428588c86df68e9ad3e099ff60922a30ba0d7ea836bbd72",
       F_CONT[0]: "6b2b78479baa31a04e52ea571a9392cedccae0ebf764d6147a3fa93d30aac1f9", F_CONT[1]: "fbefd9e93e3698c8e3f280c3f3c095b13b74fd2910ca557d6c343d3a3da275e2"}
MUT = os.environ.get("MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT, CONTROLS = [], []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def K(name, ok, val): CONTROLS.append({"name": name, "pass": bool(ok), "value": val}); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
T0 = time.time()
Z, NU0 = 1.4906, 345.79599e9 / (1 + 1.4906)                      # line frequency at the adopted z (Hz)
C_KMS = 299792.458; KLASS = (177.397034, 22.396011)
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}

P("CFG970 SN Refsdal host CO(3-2), ALMA 2013.1.00582.S A1.4" + ("  [MUTATE: channels shuffled]" if MUT else "")); P("=" * 100)
# ---------------------------------------------------------------- K1 identity
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
P("\nCONTROLS (identity)")
k1s = {os.path.basename(p): sha256(p) == s for p, s in SHA.items()}
H = fits.getheader(F_CUBE)
hdr_ok = (H["NAXIS1"], H["NAXIS2"], H["NAXIS3"]) == (784, 784, 250) and abs(H["BMAJ"] * 3600 - 0.44) < 0.006 and abs(H["BMIN"] * 3600 - 0.35) < 0.006 \
         and abs(abs(H["CDELT1"]) * 3600 - 0.08) < 1e-4
K("K1 sha256 of the 4 files equal the manifest; cube header as recorded", all(k1s.values()) and hdr_ok, {"sha": k1s, "header": hdr_ok})

# ---------------------------------------------------------------- geometry, PB plane, velocity axis
NX, NY, NC = H["NAXIS1"], H["NAXIS2"], H["NAXIS3"]
W = WCS(H).celestial
pix_as = abs(H["CDELT1"]) * 3600; bmaj, bmin = H["BMAJ"] * 3600, H["BMIN"] * 3600
beam_pix = 1.1331 * bmaj * bmin / pix_as ** 2
freq = H["CRVAL3"] + (np.arange(NC) + 1 - H["CRPIX3"]) * H["CDELT3"]
vel = C_KMS * (NU0 - freq) / NU0                                   # radio velocity relative to z = 1.4906
dv = abs(vel[1] - vel[0])
hb = fits.getheader(F_PB); hsize = len(hb.tostring()); plane_bytes = NX * NY * 4
cmid = NC // 2
with gzip.open(F_PB, "rb") as g:
    g.seek(hsize + cmid * plane_bytes); PB = np.frombuffer(g.read(plane_bytes), dtype=">f4").reshape(NY, NX).astype(np.float32)
PB = np.where(np.isfinite(PB), PB, 0.0)
cube = fits.open(F_CUBE, memmap=True)[0].data                       # (1, NC, NY, NX), big-endian float32, memory-mapped
yy, xx = np.mgrid[0:NY, 0:NX]
kx, ky = (float(v) for v in W.world_to_pixel_values(*KLASS))
P(f"  beam {bmaj:.2f}x{bmin:.2f}\" ({beam_pix:.1f} px), dv {dv:.3f} km/s, velocity range {vel.min():+.1f} .. {vel.max():+.1f} km/s; "
  f"KLASS position at pixel ({kx:.1f}, {ky:.1f}), PB there {PB[int(round(ky)), int(round(kx))]:.3f}")
rng_m = np.random.default_rng(9701); PERM = rng_m.permutation(NC) if MUT else np.arange(NC)
def plane(c, inject=None):
    a = np.array(cube[0, PERM[c]], dtype=np.float32); a[~np.isfinite(a)] = 0.0
    if inject is not None: a = a + inject(c)
    return a

# ---------------------------------------------------------------- noise in the flat frame (K2) and S1 source finding
VALID = PB >= 0.3; CORE = PB >= 0.9
LF = list(range(40)) + list(range(NC - 40, NC))
def mad(x): x = x[np.isfinite(x)]; return 1.4826 * float(np.median(np.abs(x - np.median(x))))
SIGK = math.sqrt(3) * math.sqrt(bmaj * bmin) / 2.3548 / pix_as    # smoothing kernel sigma (px): beam -> 2x beam (circularised)
D = 4
def find_sources(inject=None):
    sm = np.zeros((NC, NY // D, NX // D), np.float32); sig_f = []
    vnorm = ndimage.gaussian_filter(VALID.astype(np.float32), SIGK); vnorm[vnorm < 1e-3] = np.inf
    for c in range(NC):
        Fc = plane(c, inject) * PB; Fc[~VALID] = 0.0
        if c in LF: sig_f.append(mad(Fc[CORE]))
        s = ndimage.gaussian_filter(Fc, SIGK) / vnorm * (vnorm != np.inf)
        sm[c] = s[::D, ::D]
    sm = ndimage.uniform_filter1d(sm, 3, axis=0)
    vb = VALID[::D, ::D]
    sig_s = float(np.median([mad(sm[c][vb]) for c in LF]))
    seeds = (sm >= 4 * sig_s) & vb[None]; grow = (sm >= 2 * sig_s) & vb[None]
    lab, n = ndimage.label(grow)
    keep = np.unique(lab[seeds]); keep = keep[keep > 0]
    regs = []
    sl = ndimage.find_objects(lab)
    for k in keep:
        s3 = sl[k - 1]; m = lab[s3] == k
        foot = m.any(axis=0); nchan = int(m.any(axis=(1, 2)).sum())
        area_full = foot.sum() * D * D
        if area_full < beam_pix or nchan < 3: continue
        w = np.where(m, sm[s3], 0).sum(axis=0)
        jy, jx = np.indices(foot.shape); cy = (w * jy).sum() / w.sum() * D + s3[1].start * D; cx = (w * jx).sum() / w.sum() * D + s3[2].start * D
        if PB[int(round(cy)), int(round(cx))] < 0.3: continue
        ra, de = W.pixel_to_world_values(cx, cy)
        regs.append(dict(label=int(k), slc=s3, cx=float(cx), cy=float(cy), ra=float(ra), dec=float(de), nchan=nchan, area_beams=area_full / beam_pix,
                         c0=int(s3[0].start), c1=int(s3[0].stop - 1), sep_klass=float(math.hypot((cx - kx), (cy - ky)) * pix_as)))
    return dict(lab=lab, regs=regs, sig_s=sig_s, sig_f=float(np.median(sig_f)))

def full_mask(fs, reg, c):
    """full-resolution mask of region reg in channel c (nearest upsampling of the decimated label)."""
    m = np.zeros((NY, NX), bool)
    if not (reg["c0"] <= c <= reg["c1"]): return m
    lm = fs["lab"][c] == reg["label"]
    if not lm.any(): return m
    up = np.kron(lm, np.ones((D, D), bool))[:NY, :NX]; m[:up.shape[0], :up.shape[1]] = up
    return m & VALID

def measure(fs, reg, inject=None):
    """S2 flux in the 3-D mask, the footprint spectrum (S3/S4), and the 2" aperture variant."""
    sig_flat = fs["sig_f"]; Sdv = 0.0; var = 0.0; foot = np.zeros((NY, NX), bool)
    for c in range(reg["c0"], reg["c1"] + 1):
        m = full_mask(fs, reg, c)
        if not m.any(): continue
        a = plane(c, inject); foot |= m
        Sdv += a[m].sum() / beam_pix * dv
        var += (sig_flat ** 2 * (1.0 / PB[m] ** 2).sum() / beam_pix) * dv ** 2
    spec = np.zeros(NC); w = 1.0 / PB[foot] ** 2
    for c in range(NC): spec[c] = plane(c, inject)[foot].sum() / beam_pix
    sig_spec = sig_flat * math.sqrt(w.sum() / beam_pix)
    ap = ((xx - reg["cx"]) ** 2 + (yy - reg["cy"]) ** 2) <= (2.0 / pix_as) ** 2
    ap &= VALID; ca0, ca1 = max(0, reg["c0"] - 10), min(NC - 1, reg["c1"] + 10)
    Sap = sum(plane(c, inject)[ap].sum() for c in range(ca0, ca1 + 1)) / beam_pix * dv
    eap = sig_flat * math.sqrt((1.0 / PB[ap] ** 2).sum() / beam_pix) * dv * math.sqrt(ca1 - ca0 + 1)
    return dict(Sdv=Sdv, eSdv=math.sqrt(var), SN=Sdv / math.sqrt(var) if var > 0 else 0.0, spec=spec, sig_spec=sig_spec, foot=foot,
                Sap=Sap, eSap=eap, foot_beams=float(foot.sum() / beam_pix))

def widths(spec, sig_spec, rng=None, nreal=0):
    def wd(s):
        s2 = ndimage.uniform_filter1d(s, 2); pk = s2.max(); out = {}
        for f, nm in ((0.5, "W50"), (0.2, "W20")):
            th = f * pk; above = np.where(s2 >= th)[0]
            if len(above) == 0: out[nm] = (np.nan, np.nan, np.nan); continue
            i0, i1 = above[0], above[-1]
            def xing(i, j):
                if j < 0 or j >= len(s2): return vel[i]
                t = (th - s2[j]) / (s2[i] - s2[j]) if s2[i] != s2[j] else 0.0; return vel[j] + t * (vel[i] - vel[j])
            va, vb = xing(i0, i0 - 1), xing(i1, i1 + 1)
            out[nm] = (abs(vb - va), min(va, vb), max(va, vb))
        return out
    base = wd(spec)
    if not nreal: return base, {}
    reals = [wd(spec + rng.normal(0, sig_spec, len(spec))) for _ in range(nreal)]
    err = {k: float(np.nanstd([r[k][0] for r in reals])) for k in ("W50", "W20")}
    return base, err

# ---------------------------------------------------------------- run S1-S4 on the data
P("\nS1 SOURCE FINDING")
FS = find_sources()
P(f"  flat-frame rms per {dv:.2f} km/s channel at PB >= 0.9: {FS['sig_f']*1e6:.1f} uJy/beam; smoothed-field sigma {FS['sig_s']*1e6:.2f} uJy/beam; "
  f"regions kept {len(FS['regs'])} [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
K2v = FS["sig_f"] * 1e6
if not MUT:
    K("K2 noise: flat-frame rms per 2 km/s channel at PB >= 0.9 within x1.5 of 48.4 uJy/beam", 48.4 / 1.5 <= K2v <= 48.4 * 1.5, f"{K2v:.1f} uJy/beam")
cand = sorted([r for r in FS["regs"] if r["sep_klass"] <= 3.0], key=lambda r: r["sep_klass"])
RES = {"lane": "CFG970", "mutate": MUT, "beam_arcsec": [bmaj, bmin], "dv_kms": dv, "vel_range": [float(vel.min()), float(vel.max())],
       "sig_flat_uJy": K2v, "n_regions": len(FS["regs"])}
if not cand:
    P("  primary image: NOT FOUND within 3\" of the KLASS position")
    prim = None
else:
    prim = cand[0]
    P(f"  primary image: region {prim['label']} at ({prim['ra']:.5f}, {prim['dec']:+.5f}), {prim['sep_klass']:.2f}\" from KLASS, channels {prim['c0']}-{prim['c1']} "
      f"({vel[prim['c0']]:+.0f} .. {vel[prim['c1']]:+.0f} km/s), {prim['area_beams']:.1f} beams")

if MUT:
    sn = measure(FS, prim)["SN"] if prim else 0.0
    K("MUTATE channels shuffled: primary image integrated S/N falls below 3", sn < 3, f"S/N {sn:.2f}" + ("" if prim else " (not found)"))
    RES.update(controls=CONTROLS, primary_SN=sn)
    json.dump(RES, open(os.path.join(HERE, "cfg970_results_MUTATE.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg970_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1)

others = sorted([r for r in FS["regs"] if prim is None or r["label"] != prim["label"]], key=lambda r: -r["area_beams"] * r["nchan"])
P(f"  other regions: {len(others)}; largest (area x channels): " + "; ".join(f"({r['ra']:.4f},{r['dec']:+.4f}) {r['area_beams']:.1f} beams x {r['nchan']} ch" for r in others[:6]))

if prim:
    M = measure(FS, prim)
    G0 = "DETECTED" if M["SN"] >= 5 else ("MARGINAL" if M["SN"] >= 3 else "UPPER LIMIT")
else:
    M, G0 = None, "UPPER LIMIT (NOT FOUND)"
if G0.startswith("UPPER"):
    ap = (((xx - kx) ** 2 + (yy - ky) ** 2) <= (2.0 / pix_as) ** 2) & VALID; cw = np.where(np.abs(vel) <= 200)[0]
    ul = 3 * FS["sig_f"] * math.sqrt((1.0 / PB[ap] ** 2).sum() / beam_pix) * dv * math.sqrt(len(cw))
    Sdv_use, Sdv_err = ul, 0.0
    P(f"\nG0: {G0}; 3-sigma upper limit S dv <= {ul:.4f} Jy km/s (2\" aperture, +-200 km/s)")
else:
    Sdv_use, Sdv_err = M["Sdv"], M["eSdv"]
    P(f"\nS2 FLUX  G0: {G0}  S dv = {M['Sdv']:.4f} +- {M['eSdv']:.4f} Jy km/s (S/N {M['SN']:.1f}); 2\" aperture variant {M['Sap']:.4f} +- {M['eSap']:.4f}; footprint {M['foot_beams']:.1f} beams")

# ---------------------------------------------------------------- S3 edge clipping, S4 widths
if M:
    spec, ss = M["spec"], M["sig_spec"]
    eL, eH = spec[:10].sum(), spec[-10:].sum(); se = ss * math.sqrt(10)
    rng = np.random.default_rng(970); Wb, We = widths(spec, ss, rng, 200)
    w20lo, w20hi = Wb["W20"][1], Wb["W20"][2]
    inside = (w20lo - vel.min() >= 20) and (vel.max() - w20hi >= 20)
    lowc = abs(eL) > 2 * se or (w20lo - vel.min() < 20); highc = abs(eH) > 2 * se or (vel.max() - w20hi < 20)
    S3 = "CLEAN" if not (lowc or highc) else ("CLIPPED-BOTH" if (lowc and highc) else ("CLIPPED-LOW" if lowc else "CLIPPED-HIGH"))
    mid = 0.5 * (Wb["W50"][1] + Wb["W50"][2]); blue = spec[vel < mid].sum(); red = spec[vel >= mid].sum()
    asym = max(blue, red) / max(min(blue, red), 1e-30)
    P(f"\nS3 EDGE CLIPPING: {S3}  (edge sums {eL*1e3:+.3f} / {eH*1e3:+.3f} mJy vs 2 sigma {2*se*1e3:.3f} mJy; W20 edges {w20lo:+.0f} / {w20hi:+.0f} km/s "
      f"vs band {vel.min():+.0f} / {vel.max():+.0f})")
    VCO = {i: Wb["W50"][0] / (2 * math.sin(math.radians(i))) for i in (25, 35, 45)}
    P(f"S4 WIDTHS: W50 {Wb['W50'][0]:.1f} +- {We['W50']:.1f} km/s, W20 {Wb['W20'][0]:.1f} +- {We['W20']:.1f} km/s; V_CO = W50/(2 sin i) at i 25/35/45: "
      + " / ".join(f"{v:.0f}" for v in VCO.values()) + f" km/s{' (LOWER BOUNDS)' if S3 != 'CLEAN' else ''}; blue/red asymmetry {asym:.2f}{' LOPSIDED' if asym >= 1.5 else ''}")
else:
    S3, Wb, We, VCO, asym = "n/a", {}, {}, {}, None

# ---------------------------------------------------------------- S5 gas mass, S6 BTFR via mu*
g = {}
T6 = open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py")).read()
exec(T6[T6.index("# ---- distances from raw DESI DR2 BAO"):T6.index("# ---- clusters:")], {"np": np, "PchipInterpolator": PchipInterpolator}, g)
DL = float(g["DM"](Z)) * (1 + Z)
zz = np.linspace(0, Z, 4000); DL70 = (1 + Z) * np.trapz(1 / np.sqrt(0.3 * (1 + zz) ** 3 + 0.7), zz) * C_KMS / 70.0
nu_ghz = NU0 / 1e9
def Lp(S): return 3.25e7 * S * nu_ghz ** -2 * DL ** 2 * (1 + Z) ** -3
L32 = Lp(Sdv_use)
P(f"\nS5 GAS (apparent, not de-lensed): D_L native {DL:.1f} Mpc (h70/Om0.3: {DL70:.1f}); L'CO(3-2) {'<= ' if G0.startswith('UPPER') else ''}{L32:.3e} K km/s pc^2")
Mgas_app = {(a, r): a * L32 / r for a in (0.8, 4.3) for r in (0.5, 0.8)}
for (a, r), m in Mgas_app.items(): P(f"    alpha_CO {a}, R31 {r}: M_gas,app {'<= ' if G0.startswith('UPPER') else ''}{m:.3e} Msun")
VF = {"low": 109.0, "mid": 128.0, "high": 157.0}; MS = (10 ** 9.5, 10 ** 9.7)
corners, mus = [], []
for foot, a0 in A0.items():
    for vk, V in VF.items():
        Mreq_b = (V * 1e3) ** 4 / (G * a0) / MSUN
        for ms in MS:
            Mreq_g = Mreq_b - ms
            for (a, r), mg in Mgas_app.items():
                mu = (mg / Mreq_g) if Mreq_g > 0 else float("inf")
                corners.append(dict(footing=foot, V=V, Mstar=ms, alpha=a, R31=r, Mb_req=Mreq_b, Mgas_req=Mreq_g, mu_star=mu)); mus.append(mu)
mus = np.array(mus); lo, hi = float(np.min(mus)), float(np.max(mus))
if G0.startswith("UPPER"):
    S6 = "GAS SHORT" if hi < 2 else "UNDECIDED (upper limit: only GAS SHORT is readable)"
else:
    S6 = "CONSISTENT" if (lo <= 12.4 and hi >= 4) else ("GAS SHORT" if hi < 2 else ("GAS EXCESS" if lo > 24.8 else "UNDECIDED"))
P(f"\nS6 BTFR (law's need M_b = V^4/(G a0); V_flat 109/128/157 km/s; M* 10^9.5/9.7): M_b,req canonical {(128e3)**4/(G*A0['canonical'])/MSUN:.2e} at 128 km/s")
P(f"  mu* = M_gas,app / M_gas,req across {len(corners)} corners: {lo:.2f} .. {hi:.2f} (published mu 4 .. 12.4)  ->  {S6}")
for foot in A0:
    sub = [c["mu_star"] for c in corners if c["footing"] == foot]; P(f"    {foot}: mu* {min(sub):.2f} .. {max(sub):.2f}")
rep = {}
if VCO and S3 == "CLEAN" and not G0.startswith("UPPER"):
    for i, V in VCO.items():
        mm = []
        for foot, a0 in A0.items():
            Mr = (V * 1e3) ** 4 / (G * a0) / MSUN
            for ms in MS:
                for mg in Mgas_app.values(): mm.append(mg / (Mr - ms) if Mr > ms else float("inf"))
        rep[f"V_CO i={i}"] = (float(min(mm)), float(max(mm)))
    P("  reported, V_CO in place of V_flat: " + "; ".join(f"{k}: mu* {v[0]:.2f}..{v[1]:.2f}" for k, v in rep.items()))
imp = {}
for mu in (4.0, 5.42, 12.4):
    vals = []
    for ms in MS:
        for mg in Mgas_app.values():
            Mb = ms + mg / mu; vals.append((128e3) ** 4 / (G * Mb * MSUN) / A0["canonical"])
    imp[mu] = (float(min(vals)), float(max(vals)))
P("  reported, implied a0/a0_local (canonical, V 128) at mu 4 / 5.42 / 12.4: " + "; ".join(f"{k}: {v[0]:.2f}..{v[1]:.2f}" for k, v in imp.items())
  + "  (FLAT 1, DE-tracking ~0.93, H(z) 2.355; one disc excludes nothing)")

# ---------------------------------------------------------------- K3 injections (S1-S4 on injected copies)
def disc_model(x0, y0, Stot):
    rr = 3.0 / pix_as; sl = (slice(int(y0 - rr), int(y0 + rr)), slice(int(x0 - rr), int(x0 + rr)))
    yl, xl = np.mgrid[sl]; dx, dy = (xl - x0) * pix_as, (yl - y0) * pix_as / math.cos(math.radians(45))
    R = np.hypot(dx, dy); I = np.exp(-R / 0.5); vlos = 60.0 * np.tanh(R / 0.3) * np.where(R > 0, dx / np.maximum(R, 1e-9), 0)
    prof = np.exp(-0.5 * ((vel[:, None, None] - vlos[None]) / 20.0) ** 2)                  # (NC, ny, nx)
    cubem = I[None] * prof
    sb = ndimage.gaussian_filter(cubem, (0, bmin / 2.3548 / pix_as, bmaj / 2.3548 / pix_as))
    tot = sb.sum() / beam_pix * dv; sb *= Stot / tot                                       # Jy/beam such that S dv = Stot
    spec_true = sb.sum(axis=(1, 2)) / beam_pix
    def inj(c):
        a = np.zeros((NY, NX), np.float32); a[sl] = sb[c]; return a
    return inj, spec_true
P("\nK3 INJECTIONS")
used = [(r["cx"], r["cy"]) for r in FS["regs"] if r["area_beams"] * r["nchan"] > 20]
cx0, cy0 = (float(v) for v in W.world_to_pixel_values(H["CRVAL1"], H["CRVAL2"]))
spots = []
for ang in range(0, 360, 30):
    x, y = cx0 + 8 / pix_as * math.cos(math.radians(ang)), cy0 + 8 / pix_as * math.sin(math.radians(ang))
    if PB[int(y), int(x)] < 0.7 or math.hypot(x - kx, y - ky) * pix_as < 5: continue
    if any(math.hypot(x - u, y - v) * pix_as < 5 for u, v in used): continue
    spots.append((x, y))
k3 = []
for (x, y), St in zip(spots[:3], (0.1, 0.3, 1.0)):
    inj, strue = disc_model(x, y, St)
    fs = find_sources(inj); cc = sorted([r for r in fs["regs"] if math.hypot(r["cx"] - x, r["cy"] - y) * pix_as <= 1.5], key=lambda r: -r["area_beams"])
    if not cc: k3.append(dict(S=St, found=False)); P(f"  injection {St} Jy km/s at ({x:.0f},{y:.0f}): NOT FOUND"); continue
    mm = measure(fs, cc[0], inj); wt, _ = widths(strue, 0.0); wm, _ = widths(mm["spec"], mm["sig_spec"])
    # the injected source sits on real noise; compare to truth
    ok = abs(mm["Sdv"] / St - 1) <= 0.20 and abs(wm["W50"][0] - wt["W50"][0]) <= 10
    k3.append(dict(S=St, found=True, Sdv=mm["Sdv"], W50=wm["W50"][0], W50_true=wt["W50"][0], ok=ok))
    P(f"  injection {St} Jy km/s at ({x:.0f},{y:.0f}): recovered {mm['Sdv']:.3f} (ratio {mm['Sdv']/St:.2f}), W50 {wm['W50'][0]:.1f} vs true {wt['W50'][0]:.1f} -> {'ok' if ok else 'MISS'}"
      f"  [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
K("K3 three injected discs recovered (S dv within 20%, W50 within 10 km/s)", len(k3) == 3 and all(r.get("ok") for r in k3), [(r["S"], r.get("ok")) for r in k3])

# ---------------------------------------------------------------- S7 moment-0 / spectrum / PV (reported)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
if prim:
    m0 = np.zeros((NY, NX)); m1n = np.zeros((NY, NX))
    for c in range(prim["c0"], prim["c1"] + 1):
        m = full_mask(FS, prim, c)
        if m.any(): a = plane(c); m0[m] += a[m] * dv; m1n[m] += a[m] * dv * vel[c]
    with np.errstate(invalid="ignore", divide="ignore"): m1 = np.where(m0 > 0, m1n / m0, np.nan)
    fp = M["foot"] & np.isfinite(m1) & (m0 > 0)
    A_ = np.c_[np.ones(fp.sum()), xx[fp] - prim["cx"], yy[fp] - prim["cy"]]; wts = m0[fp]
    coef = np.linalg.lstsq(A_ * wts[:, None] ** 0.5, m1[fp] * wts ** 0.5, rcond=None)[0]
    pa = math.atan2(coef[2], coef[1])                                                     # direction of steepest velocity gradient (image axes)
    s = np.linspace(-4, 4, 101); px, py = prim["cx"] + s / pix_as * math.cos(pa), prim["cy"] + s / pix_as * math.sin(pa)
    pv = np.array([ndimage.map_coordinates(plane(c), [py, px], order=1) for c in range(NC)])
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
    r0 = int(5 / pix_as); ys, xs = slice(int(prim["cy"]) - r0, int(prim["cy"]) + r0), slice(int(prim["cx"]) - r0, int(prim["cx"]) + r0)
    ax[0].imshow(m0[ys, xs], origin="lower", cmap="magma"); ax[0].set_title("moment 0 (mask), 10\" box"); ax[0].plot(*(np.array([px, py]) - [[xs.start], [ys.start]]), "c-", lw=0.8)
    ax[1].step(vel, spec * 1e3, where="mid"); ax[1].axhline(0, color="k", lw=0.5); ax[1].set_xlabel("v (km/s, z=1.4906)"); ax[1].set_ylabel("mJy"); ax[1].set_title(f"spectrum ({S3})")
    ax[2].imshow(pv * 1e3, origin="lower", aspect="auto", extent=[s[0], s[-1], vel[0], vel[-1]], cmap="viridis"); ax[2].set_xlabel("offset along kinematic axis (\", image plane)")
    ax[2].set_ylabel("v (km/s)"); ax[2].set_title("PV (image plane; source plane needs a lens model)")
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "cfg970_mom0_spec_pv.png"), dpi=90); plt.close(fig)
    RES.update(kin_axis_angle_deg=math.degrees(pa), grad_kms_per_arcsec=float(math.hypot(coef[1], coef[2]) / pix_as))
    P(f"\nS7 PV: kinematic-axis angle {math.degrees(pa):.0f} deg (image x-y), velocity gradient {math.hypot(coef[1], coef[2])/pix_as:.1f} km/s per arcsec; figure cfg970_mom0_spec_pv.png")

valid = all(c["pass"] for c in CONTROLS)
P(f"\nREADING (frozen): G0 {G0}; S3 {S3}; S6 {S6}" + ("" if valid else "  -> INVALID (a control failed)"))
P(f"controls {sum(c['pass'] for c in CONTROLS)}/{len(CONTROLS)}; runtime {time.time()-T0:.0f} s; peak RSS {rss():.2f} GB")
RES.update(controls=CONTROLS, G0=G0, S3=S3, S6=S6 if valid else "INVALID", Sdv=Sdv_use, eSdv=Sdv_err, SN=(M["SN"] if M else None),
           aperture=(M["Sap"], M["eSap"]) if M else None, W=Wb, W_err=We, V_CO=VCO, asymmetry=asym, DL_native=DL, DL_h70=DL70, Lp32=L32,
           Mgas_app={f"a{a}_R{r}": v for (a, r), v in Mgas_app.items()}, mu_star_range=[lo, hi], corners=corners, reported_VCO=rep, implied_a0=imp,
           injections=k3, primary=({k: v for k, v in prim.items() if k != "slc"} if prim else None),
           other_regions=[{k: v for k, v in r.items() if k != "slc"} for r in others[:30]])
json.dump(RES, open(os.path.join(HERE, "cfg970_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg970.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if valid else 2)
