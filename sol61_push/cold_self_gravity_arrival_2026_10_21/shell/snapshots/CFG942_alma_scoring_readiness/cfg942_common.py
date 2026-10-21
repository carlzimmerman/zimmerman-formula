#!/usr/bin/env python3
"""CFG942 shared machinery (FROZEN_CRITERIA.md, 556c36582): seal and plan hashes, CFG571's functions executed read-only,
frozen-table transcription, cube I/O, moment maps and masks, translated-mask apertures, beam-convolved 2D Gaussian fit,
thin-disc cube model and fit, MOCK cube generation.  Nothing here writes into another lane.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, hashlib, subprocess, re, resource
sys.dont_write_bytecode = True
import numpy as np
from scipy import ndimage, optimize, special
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
CFGD = os.path.dirname(HERE)
REPO = os.path.dirname(CFGD)
CKMS = 2.99792458e5
A571 = "campaign_fresh_gravity/CFG571_prereg_proprietary_alma"
FOOTS = ("canon 9.36e-11", "alt 1.13e-10")
MODELS = ("F-DESI", "F-flat", "R-H", "L-fb(RAR-eq)")
FRAMEWORK, RIVAL = ("F-DESI", "F-flat"), "R-H"

# (label, repo-relative path, freezing commit): every file the harness reads as frozen input (criteria section 1)
FROZEN = [
    ("CFG571 criteria", A571 + "/FROZEN_CRITERIA.md", "5f68a68c3"),
    ("CFG571 sealed results", A571 + "/cfg571_prereg_results.json", "259f7825c"),
    ("CFG571 hash file", A571 + "/PREDICTIONS_HASH.txt", "259f7825c"),
    ("CFG571 code", A571 + "/cfg571_prereg.py", "259f7825c"),
    ("CFG571 README", A571 + "/README.md", "259f7825c"),
    ("nu_mono kernel (Bcommon)", "campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py", "259f7825c"),
    ("U4 plan (CFG806 dir)", "campaign_fresh_gravity/CFG806_u4_27928_scoring/FROZEN_CRITERIA.md", "1bf70683b"),
    ("U4 ID note a", "campaign_fresh_gravity/CFG806_u4_27928_scoring/ID_NOTE_2026-10-15.md", "79321a577"),
    ("U4 ID note b", "campaign_fresh_gravity/CFG806_u4_27928_scoring/ID_NOTE_2026-10-15b.md", "38c7bc24d"),
    ("GS4 plan (CFG809 dir)", "campaign_fresh_gravity/CFG809_gs4_24110_ci21_scoring/FROZEN_CRITERIA.md", "966d50a87"),
    ("CFG572 results (public GS4 routes)", "campaign_fresh_gravity/CFG572_gs4_24110_gas_now/cfg572_gas_results.json", "12779c1e5"),
    ("CFG775 seal", "campaign_fresh_gravity/CFG775_bh_horizon_dark_energy/SEALED_BH_BRANCH.json", "8a7634027"),
    ("CFG778 seal", "campaign_fresh_gravity/CFG778_sealed_event_horizon_branch/SEALED_EVENT_HORIZON.json", "aac6ddd23"),
    ("THEORY_CANONICAL 10-14", "campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md", "b7356ac57"),
    ("KMOS3D catalogue (U4 position, axis ratio)", "data_assembly/kmos3d_phibss/kmos3d_catalog.csv", None),
]
SEAL_HASH_EXPECT = "be27457db6bad870a734c52d2bad92c6669cde53ca7a81553e79154dbedc3714"


# ------------------------------------------------------------------------------------------------ run bookkeeping
class Run:
    def __init__(self, slug, sample_memory=False):
        self.slug, self.lines, self.checks, self.flags = slug, [], [], []
        self.peak_uss = 0
        if sample_memory:
            import threading
            def _mon():
                try:
                    import psutil, time, ctypes, ctypes.util
                    pr = psutil.Process(); relief = None
                    if sys.platform == "darwin":   # return freed pages to the OS so resident size tracks real use
                        lc = ctypes.CDLL(ctypes.util.find_library("c")); relief = lc.malloc_zone_pressure_relief
                        relief.restype = ctypes.c_size_t; relief.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
                    while True:
                        if relief: relief(None, 0)
                        self.peak_uss = max(self.peak_uss, pr.memory_full_info().uss); time.sleep(0.25)
                except Exception:
                    pass
            threading.Thread(target=_mon, daemon=True).start()

    def P(self, s=""):
        print(s, flush=True); self.lines.append(str(s))

    def check(self, name, ok, extra=""):
        self.checks.append((name, bool(ok), extra)); self.P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {extra}" if extra else "")); return bool(ok)

    def flag(self, code, text):
        if code not in [c for c, _ in self.flags]:
            self.flags.append((code, text))
        self.P(f"  {{flag {code}}} {text}")

    def failed(self):
        return [n for n, ok, _ in self.checks if not ok]

    def save(self, results):
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
        self.P(f"\n(peak RSS {rss:.0f} MB, incl. freed pages macOS keeps resident; peak unique set size {self.peak_uss / 1048576:.0f} MB)")
        out = dict(slug=self.slug, checks=self.checks, flags=self.flags, results=results, peak_rss_MB=round(rss), peak_uss_MB=round(self.peak_uss / 1048576))
        json.dump(out, open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1, default=_js)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")


def _js(o):
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)


# ------------------------------------------------------------------------------------------------ hashes (K1, K5)
def sha256_file(p, _cache={}):
    st = os.stat(p); key = (p, st.st_size, st.st_mtime_ns)
    if key not in _cache:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for blk in iter(lambda: f.read(8 * 2 ** 20), b""): h.update(blk)
        _cache[key] = h.hexdigest()
    return _cache[key]


def sha256_git(commit, rel):
    r = subprocess.run(["git", "-C", REPO, "show", f"{commit}:{rel}"], capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None


def snapshot():
    out = {}
    for _, rel, _ in FROZEN:
        p = os.path.join(REPO, rel)
        out[rel] = (sha256_file(p), os.stat(p).st_mtime_ns)
    return out


def verify_frozen(run):
    """K1: working tree == freezing commit for every frozen file; recorded hashes match. Returns dict of results."""
    run.P("K1 hashes (working tree vs freezing commit; recorded hashes)")
    res = {}
    for label, rel, com in FROZEN:
        wt = sha256_file(os.path.join(REPO, rel))
        if com is None:
            head = sha256_git("HEAD", rel); ok = head == wt
            run.check(f"K1 {label} == HEAD", ok, wt[:16] + "…"); res[rel] = dict(sha256=wt, commit="HEAD", ok=ok); continue
        gc = sha256_git(com, rel); ok = gc == wt
        run.check(f"K1 {label} == {com}", ok, wt[:16] + "…"); res[rel] = dict(sha256=wt, commit=com, ok=ok)
    seal = sha256_file(os.path.join(REPO, A571, "cfg571_prereg_results.json"))
    rec = open(os.path.join(REPO, A571, "PREDICTIONS_HASH.txt")).read().split()[0]
    run.check("K1 sealed JSON sha256 == PREDICTIONS_HASH.txt == be27457d…", seal == rec == SEAL_HASH_EXPECT, seal)
    u4 = sha256_file(os.path.join(REPO, "campaign_fresh_gravity/CFG806_u4_27928_scoring/FROZEN_CRITERIA.md"))
    q = set()
    for n in ("ID_NOTE_2026-10-15.md", "ID_NOTE_2026-10-15b.md"):
        q |= set(re.findall(r"[0-9a-f]{64}", open(os.path.join(REPO, "campaign_fresh_gravity/CFG806_u4_27928_scoring", n)).read()))
    run.check("K1 U4 plan sha256 == value quoted in its ID notes (bc56aa71…)", q == {u4}, u4)
    for lab, rel, readme in (("CFG775", FROZEN[11][1], "campaign_fresh_gravity/CFG775_bh_horizon_dark_energy/README.md"),
                             ("CFG778", FROZEN[12][1], "campaign_fresh_gravity/CFG778_sealed_event_horizon_branch/README.md")):
        h = sha256_file(os.path.join(REPO, rel)); rq = re.findall(r"[0-9a-f]{64}", open(os.path.join(REPO, readme)).read())
        run.check(f"K1 {lab} seal sha256 == value in its README", h in rq, h[:16] + "…")
    tc = sha256_file(os.path.join(REPO, FROZEN[13][1])); tq = open(os.path.join(REPO, FROZEN[13][1].replace(".md", ".sha256"))).read().split()[0]
    run.check("K1 THEORY_CANONICAL_2026-10-14.md sha256 == its .sha256 file", tc == tq, tc[:16] + "…")
    res["sealed_json_sha256"] = seal
    return res


# ------------------------------------------------------------------------------------------------ CFG571 functions, read-only
def load_cfg571():
    """Execute only the text above '# ---- controls ----' of cfg571_prereg.py in a private namespace (no file is written;
    a plain import would run the whole script, rewrite its results JSON and call sys.exit)."""
    p = os.path.join(REPO, A571, "cfg571_prereg.py")
    src = open(p).read()
    assert "# ---- controls ----" in src
    head = src.split("# ---- controls ----")[0]
    ns = {"__file__": p, "__name__": "cfg571_head_readonly"}
    argv = sys.argv; sys.argv = [argv[0]]
    try:
        exec(compile(head, p + "[head]", "exec"), ns)
    finally:
        sys.argv = argv
    assert ns["NU"] is ns["nu_mono"], "MUTATE flag leaked into the CFG571 head"
    return ns


def sealed():
    return json.load(open(os.path.join(REPO, A571, "cfg571_prereg_results.json")))["results"]


def u4_geometry():
    """exactly CFG571's U4 block expression (D_A from flat LCDM H0 70, Om 0.3; angular size only)"""
    z = 1.41933
    dc = 2.99792458e5 / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z)[0] * 1e3; da = dc / (1 + z); Re = 0.49 / 206264.806 * da
    return dict(z=z, Re=Re, R=2 * Re, Rd=Re / 1.678, lmstar=10.74)


GS4 = dict(z=1.997, R=7.39, Rd=7.39 / 1.678, Vc=206.0, lmstars=(10.89, 10.76))


def predict(ns, R, Vc, z, lm, Rd):
    return {f"{a}|{b}": c for (a, b), c in ns["predict"](R, float(Vc), z, 10 ** lm, Rd).items()}


def newtonian_round_trip(ns):
    save = ns["NU"]; ns["NU"] = lambda y: np.ones_like(np.asarray(y, float))
    try:
        g = 150.0 ** 2 / 9.0; v = math.sqrt(ns["gbar_req"](g, 1.13e-10) * 9.0) / 150.0
    finally:
        ns["NU"] = save
    return abs(v - 1)


def freeman_peak(ns):
    ys = np.linspace(0.3, 2.0, 20001); b = 2 * ns["B"](ys); return float(b.max()), float(2 * ys[b.argmax()])


def reproduce(ns, target):
    S = sealed()[target]; worst, n = 0.0, 0; bad = []
    for key, ent in S.items():
        if target == "U4_27928":
            g = u4_geometry(); r = predict(ns, g["R"], float(key), g["z"], g["lmstar"], g["Rd"])
        else:
            r = predict(ns, GS4["R"], GS4["Vc"], GS4["z"], float(key), GS4["Rd"])
        for k2, d in ent.items():
            m = r[k2]; worst = max(worst, abs(m["logVbar2R_G"] - d["logVbar2R_G"])); n += 1
            if str(bool(m["floor"])) != str(d["floor"]): bad.append((key, k2, "floor"))
            for sh in ("logMgas_Rg=Rd", "logMgas_Rg=1.5Rd"):
                if (m[sh] is None) != (d[sh] is None): bad.append((key, k2, sh))
                elif m[sh] is not None: worst = max(worst, abs(m[sh] - d[sh]))
    return worst, n, bad


# ------------------------------------------------------------------------------------------------ R3: plan tables vs the seal
def _cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def transcription(plan_rel, target):
    S = sealed()[target]; rows = 0; worst = 0.0; bad = []
    for line in open(os.path.join(REPO, plan_rel)):
        if not line.startswith("|"): continue
        c = _cells(line)
        if len(c) != 6 or c[0] in ("V_c [km/s]", "M★") or set(c[0]) <= set("-| "): continue
        keys = {"150–200": ("150", "175", "200")}.get(c[0], (c[0],))
        foots = FOOTS if c[1] == "both" else tuple(f for f in FOOTS if f.split()[0] == c[1].split()[0])
        if not foots or any(k not in S for k in keys): continue
        rows += 1
        for k in keys:
            for f in foots:
                for m, cell in zip(MODELS, c[2:]):
                    d = S[k][f"{f}|{m}"]
                    if cell == "FLOOR":
                        if d["logMgas_Rg=Rd"] is not None or d["logMgas_Rg=1.5Rd"] is not None: bad.append((k, f, m, cell))
                    else:
                        a, b = [float(x) for x in re.findall(r"\d+\.\d+", cell)]
                        if d["logMgas_Rg=Rd"] is None or d["logMgas_Rg=1.5Rd"] is None: bad.append((k, f, m, cell)); continue
                        e = max(abs(a - d["logMgas_Rg=Rd"]), abs(b - d["logMgas_Rg=1.5Rd"])); worst = max(worst, e)
                        if e > 0.005 + 1e-9: bad.append((k, f, m, cell, round(e, 4)))
    return rows, worst, bad


# ------------------------------------------------------------------------------------------------ cosmology and line conversions
def DC_Mpc(z):
    return CKMS / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z)[0]


def DL_Mpc(z): return DC_Mpc(z) * (1 + z)
def kpc_per_arcsec(z): return DC_Mpc(z) * 1e3 / (1 + z) / 206264.806
def Lprime(SdV, nu_obs, z): return 3.25e7 * SdV * nu_obs ** -2 * DL_Mpc(z) ** 2 * (1 + z) ** -3
def SdV_from_Lprime(Lp, nu_obs, z): return Lp / (3.25e7 * nu_obs ** -2 * DL_Mpc(z) ** 2 * (1 + z) ** -3)


def mgas_co21(SdV, z, nu_obs, aco=4.36, r21=0.77):
    return aco * Lprime(SdV, nu_obs, z) / r21


def Q_ci(T): return 1 + 3 * math.exp(-23.6 / T) + 5 * math.exp(-62.5 / T)
C21_CFG809 = 4.566e-4


def mci_21(Lp, T=25.0, c21=C21_CFG809): return c21 * Q_ci(T) / 5 * math.exp(62.5 / T) * Lp
def mci_10(Lp, T=25.0, c10=5.706e-4): return c10 * Q_ci(T) / 3 * math.exp(23.6 / T) * Lp
def mgas_ci21(SdV, z, nu_obs, X=1.9e-5, T=25.0): return 1.36 * mci_21(Lprime(SdV, nu_obs, z), T) / (6 * X)


# ------------------------------------------------------------------------------------------------ cube I/O
def _hdu(path):
    """open without memory-mapping; pixels are read through .section (only the requested bytes)"""
    from astropy.io import fits
    hl = fits.open(path, memmap=False, lazy_load_hdus=True)
    for h in hl:
        if h.header.get("NAXIS", 0) >= 2:
            return hl, h
    raise ValueError("no image HDU in " + os.path.basename(path))


def header_info(h):
    """beam, pixel scale and the (linear) frequency axis; ALMA pipeline cubes carry CTYPE3 = 'FREQ'."""
    pix = abs(h["CDELT2"]) * 3600.0
    beam = (h["BMAJ"] * 3600, h["BMIN"] * 3600, h.get("BPA", 0.0)) if "BMAJ" in h else None
    spec = None
    if h.get("NAXIS", 0) >= 3 and str(h.get("CTYPE3", "")).upper().startswith("FREQ"):
        n = h["NAXIS3"]; nu = (h["CRVAL3"] + (np.arange(n) + 1 - h["CRPIX3"]) * h["CDELT3"]) / 1e9
        spec = nu
    return dict(pix=pix, beam=beam, nu=spec, restfrq=h.get("RESTFRQ", h.get("RESTFREQ")), object=h.get("OBJECT", ""), bunit=h.get("BUNIT", ""))


def _cut(hdr, info, ra, dec, half):
    from astropy.wcs import WCS
    w = WCS(hdr).celestial; xc, yc = [float(t) for t in w.world_to_pixel_values(ra, dec)]
    nx, ny = hdr["NAXIS1"], hdr["NAXIS2"]; hp = half / info["pix"]
    x0, x1 = max(0, int(math.floor(xc - hp))), min(nx, int(math.ceil(xc + hp)) + 1)
    y0, y1 = max(0, int(math.floor(yc - hp))), min(ny, int(math.ceil(yc + hp)) + 1)
    return x0, x1, y0, y1, xc, yc


def _chan(h, k, y0, y1, x0, x1):
    nd = h.header["NAXIS"]
    return np.asarray(h.section[(0,) * (nd - 3) + (k, slice(y0, y1), slice(x0, x1))], np.float32)


def _vaxis(info, nu_line, vshift):
    if info["nu"] is None: raise ValueError("cube has no FREQ axis (CTYPE3); the harness reads FREQ cubes only")
    return CKMS * (nu_line - info["nu"]) / nu_line - vshift


def _cont_channels(v_all, vcont, vmaxcont):
    return np.where((np.abs(v_all) > vcont) & (np.abs(v_all) <= vmaxcont))[0]


def _cont_median(h, kc, y0, y1, x0, x1, block_bytes=8 * 2 ** 20):
    """per-pixel median over ALL line-free channels kc, computed in row blocks (bounded memory)"""
    shp = (y1 - y0, x1 - x0); cont = np.zeros(shp, np.float32)
    if len(kc) < 3: return cont
    rows = max(1, int(block_bytes // (4 * len(kc) * shp[1])))
    for r0 in range(y0, y1, rows):
        r1 = min(y1, r0 + rows); st = np.empty((len(kc), r1 - r0, shp[1]), np.float32)
        for i, k in enumerate(kc): st[i] = _chan(h, k, r0, r1, x0, x1)
        cont[r0 - y0:r1 - y0] = np.nanmedian(st, axis=0) if np.isnan(st).any() else np.median(st, axis=0); del st
    return cont


def stream_mom0(path, ra, dec, nu_line, half, vwin, vcont=600.0, vshift=0.0, vmaxcont=np.inf):
    """continuum-subtracted moment-0 over |v| <= vwin in a box (half-size arcsec), read channel by channel (bounded memory).
    v = c (nu_line - nu)/nu_line - vshift (radio convention about the catalogue line; MUTATE shifts the axis).
    Continuum per pixel = median of all line-free channels vcont < |v| <= vmaxcont."""
    hl, h = _hdu(path); hdr = h.header; info = header_info(hdr); D = h
    v_all = _vaxis(info, nu_line, vshift); x0, x1, y0, y1, xc, yc = _cut(hdr, info, ra, dec, half)
    kw = np.where(np.abs(v_all) <= vwin)[0]; kc = _cont_channels(v_all, vcont, vmaxcont)
    dv = float(abs(np.median(np.diff(v_all)))) if len(v_all) > 1 else float("nan")
    shp = (y1 - y0, x1 - x0)
    cont = _cont_median(D, kc, y0, y1, x0, x1)
    r = radius_map(shp, xc - x0, yc - y0) * info["pix"]
    probe = kc[np.unique(np.linspace(0, len(kc) - 1, min(8, len(kc))).round().astype(int))] if len(kc) else kw[:1]
    sig_ch = robust_std(np.concatenate([(_chan(D, k, y0, y1, x0, x1) - cont)[r > 2.0] for k in probe])) if len(probe) else float("nan")
    m0 = np.zeros(shp); nfin = np.zeros(shp, int)
    for k in kw:
        c = _chan(D, k, y0, y1, x0, x1) - cont; f = np.isfinite(c); m0[f] += c[f]; nfin += f
    m0 *= dv; m0[nfin == 0] = np.nan
    hl.close()
    return dict(m0=m0, xc=xc - x0, yc=yc - y0, x0=x0, y0=y0, pix=info["pix"], beam=info["beam"], dv=dv, nwin=int(len(kw)), ncont=int(len(kc)), sig_ch=sig_ch,
                win_covered=bool(len(v_all) and v_all.min() <= -vwin and v_all.max() >= vwin), v_cover=(float(v_all.min()), float(v_all.max())),
                nu_cover=(float(info["nu"].min()), float(info["nu"].max())), restfrq=info["restfrq"], object=info["object"], bunit=info["bunit"],
                file=os.path.basename(path), sha256=sha256_file(path))


def load_box(path, ra, dec, nu_line, half, vkeep=650.0, vcont=600.0, vshift=0.0, vmaxcont=np.inf):
    """continuum-subtracted sub-cube: channels |v| <= vkeep in a box (half-size arcsec) about (ra, dec)."""
    hl, h = _hdu(path); hdr = h.header; info = header_info(hdr); D = h
    v_all = _vaxis(info, nu_line, vshift); x0, x1, y0, y1, xc, yc = _cut(hdr, info, ra, dec, half)
    kk = np.where(np.abs(v_all) <= vkeep)[0]; kc = _cont_channels(v_all, vcont, vmaxcont)
    shp = (y1 - y0, x1 - x0)
    cont = _cont_median(D, kc, y0, y1, x0, x1)
    data = np.empty((len(kk),) + shp, np.float32)
    for i, k in enumerate(kk): data[i] = _chan(D, k, y0, y1, x0, x1) - cont
    dv = float(abs(np.median(np.diff(v_all)))) if len(v_all) > 1 else float("nan")
    hl.close()
    return dict(data=data, v=v_all[kk].astype(float), dv=dv, pix=info["pix"], beam=info["beam"], xc=xc - x0, yc=yc - y0, x0=x0, y0=y0,
                ncont=int(len(kc)), file=os.path.basename(path), sha256=sha256_file(path), object=info["object"])


def mask_sum_noise(mask, beam, pix, sig_ch, dv, nwin, ncont):
    """analytic ('quoted') noise of S dv summed over a mask: interferometric noise with autocorrelation = the beam (peak 1),
    per-pixel channel noise sig_ch, nwin window channels, continuum = median of ncont channels (variance pi/2/ncont)."""
    from scipy import fft as sfft
    ny, nx = mask.shape; yy, xx = np.indices((ny, nx)); X, Y = (xx - nx // 2) * pix, (yy - ny // 2) * pix
    inv = np.linalg.inv(beam_cov(beam)); B = np.exp(-0.5 * (inv[0, 0] * X * X + 2 * inv[0, 1] * X * Y + inv[1, 1] * Y * Y))
    m = mask.astype(float); conv = sfft.irfft2(sfft.rfft2(m) * sfft.rfft2(np.fft.ifftshift(B)), s=(ny, nx))
    vs = float((m * conv).sum()); ft = nwin * (1 + (nwin * math.pi / (2 * ncont) if ncont >= 3 else 0.0))
    return sig_ch * dv * math.sqrt(ft * vs) / beam_pix(beam, pix)


def sub_mask(mask, m0d, box):
    """the part of a mask defined on the moment-0 grid that falls on the sub-cube grid"""
    dy, dx = box["y0"] - m0d["y0"], box["x0"] - m0d["x0"]; ny, nx = box["data"].shape[1:]
    out = np.zeros((ny, nx), bool)
    ys, xs = np.nonzero(mask); ys2, xs2 = ys - dy, xs - dx
    ok = (ys2 >= 0) & (ys2 < ny) & (xs2 >= 0) & (xs2 < nx); out[ys2[ok], xs2[ok]] = True
    return out, int((~ok).sum())


def load_image(path, ra, dec, half):
    from astropy.wcs import WCS
    hl, h = _hdu(path); hdr = h.header; info = header_info(hdr)
    w = WCS(hdr).celestial; xc, yc = [float(t) for t in w.world_to_pixel_values(ra, dec)]
    nx, ny = hdr["NAXIS1"], hdr["NAXIS2"]; hp = half / info["pix"]
    x0, x1 = max(0, int(math.floor(xc - hp))), min(nx, int(math.ceil(xc + hp)) + 1)
    y0, y1 = max(0, int(math.floor(yc - hp))), min(ny, int(math.ceil(yc + hp)) + 1)
    nd = hdr["NAXIS"]; img = np.asarray(h.section[(0,) * (nd - 2) + (slice(y0, y1), slice(x0, x1))], np.float64)
    hl.close()
    return dict(img=img, pix=info["pix"], beam=info["beam"], xc=xc - x0, yc=yc - y0, object=info["object"], file=os.path.basename(path), sha256=sha256_file(path))


def beam_pix(beam, pix):
    return math.pi / (4 * math.log(2)) * beam[0] * beam[1] / pix ** 2


# ------------------------------------------------------------------------------------------------ moment maps, masks, apertures
def robust_std(x):
    x = x[np.isfinite(x)]
    return float(1.4826 * np.median(np.abs(x - np.median(x)))) if x.size else float("nan")


def radius_map(shape, xc, yc):
    yy, xx = np.indices(shape); return np.hypot(xx - xc, yy - yc)


def make_mask(m0, sig, xc, yc, pix, seed_r=0.5, thr=2.0):
    m = np.isfinite(m0) & (m0 >= thr * sig)
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    seed = radius_map(m0.shape, xc, yc) <= seed_r / pix
    keep = set(np.unique(lab[seed & m])) - {0}
    return np.isin(lab, list(keep)) if keep else np.zeros_like(m)


def aperture_sum(m0, mask, dx, dy, bpix):
    ys, xs = np.nonzero(mask); ys2, xs2 = ys + dy, xs + dx
    if ys2.min() < 0 or xs2.min() < 0 or ys2.max() >= m0.shape[0] or xs2.max() >= m0.shape[1]: return None
    vals = m0[ys2, xs2]
    if not np.all(np.isfinite(vals)): return None
    return float(vals.sum() / bpix)


def translated_apertures(m0, mask, bpix, offsets):
    out = []
    for dx, dy in offsets:
        s = aperture_sum(m0, mask, int(round(dx)), int(round(dy)), bpix)
        if s is not None: out.append(s)
    return out


def random_offsets(rng, mask, shape, xc, yc, rmin_pix, n, tries=200000):
    ys, xs = np.nonzero(mask); offs = []
    if ys.size == 0: return offs
    for _ in range(tries):
        dx, dy = int(rng.integers(-shape[1], shape[1])), int(rng.integers(-shape[0], shape[0]))
        ys2, xs2 = ys + dy, xs + dx
        if ys2.min() < 0 or xs2.min() < 0 or ys2.max() >= shape[0] or xs2.max() >= shape[1]: continue
        if np.min(np.hypot(xs2 - xc, ys2 - yc)) < rmin_pix: continue
        offs.append((dx, dy))
        if len(offs) >= n: break
    return offs


def independent_count(mask, offsets):
    """greedy count of mutually non-overlapping translated copies of the mask (for the error of the mean of overlapping apertures)"""
    from scipy import fft as sfft
    ys, xs = np.nonzero(mask)
    if ys.size == 0 or not offsets: return 0
    m = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(float); h, w = m.shape
    ac = sfft.irfft2(np.abs(sfft.rfft2(m, s=(2 * h, 2 * w))) ** 2, s=(2 * h, 2 * w)) > 0.5
    chosen = []
    for dx, dy in offsets:
        ok = True
        for cx, cy in chosen:
            ddx, ddy = int(round(dx - cx)), int(round(dy - cy))
            if abs(ddx) < w and abs(ddy) < h and ac[ddy % (2 * h), ddx % (2 * w)]: ok = False; break
        if ok: chosen.append((dx, dy))
    return len(chosen)


def ring_offsets(r_pix, n=8, phase=0.0):
    return [(r_pix * math.cos(phase + 2 * math.pi * k / n), r_pix * math.sin(phase + 2 * math.pi * k / n)) for k in range(n)]


# ------------------------------------------------------------------------------------------------ beam-convolved 2D Gaussian fit
def beam_cov(beam):
    """beam covariance in the pixel frame (x right, y up; BPA east of north, east = -x for CDELT1 < 0), arcsec^2"""
    sa, sb, t = beam[0] / 2.3548, beam[1] / 2.3548, math.radians(beam[2])
    u = np.array([-math.sin(t), math.cos(t)]); w = np.array([math.cos(t), math.sin(t)])
    return sa ** 2 * np.outer(u, u) + sb ** 2 * np.outer(w, w)


def gauss2d_model(p, X, Y, Sb, pix, bpix):
    F, x0, y0, lsa, lsb, th = p
    sa, sb = math.exp(lsa), math.exp(lsb); c, s = math.cos(th), math.sin(th)
    Si = np.array([[c * c * sa * sa + s * s * sb * sb, c * s * (sa * sa - sb * sb)], [c * s * (sa * sa - sb * sb), s * s * sa * sa + c * c * sb * sb]])
    So = Si + Sb; det = So[0, 0] * So[1, 1] - So[0, 1] ** 2; inv = np.array([[So[1, 1], -So[0, 1]], [-So[0, 1], So[0, 0]]]) / det
    dx, dy = X - x0, Y - y0
    q = inv[0, 0] * dx * dx + 2 * inv[0, 1] * dx * dy + inv[1, 1] * dy * dy
    return F * bpix * pix * pix * np.exp(-0.5 * q) / (2 * math.pi * math.sqrt(det))


def fit_gauss2d(img, sig, pix, beam, xc, yc, half=2.0, p0=None):
    """2D elliptical Gaussian convolved with the beam; returns intrinsic FWHMs (arcsec), axis ratio, total flux, errors from the
    fit covariance (independent-pixel assumption: underestimates errors for beam-correlated noise; see flag)."""
    ny, nx = img.shape; yy, xx = np.indices(img.shape)
    sel = (np.hypot(xx - xc, yy - yc) <= half / pix) & np.isfinite(img)
    X, Y = (xx[sel] - xc) * pix, (yy[sel] - yc) * pix; D = img[sel]
    bp = beam_pix(beam, pix); Sb = beam_cov(beam)
    if p0 is None:
        w = np.clip(D, 0, None); tot = max(w.sum(), 1e-30)
        mx, my = (w * X).sum() / tot, (w * Y).sum() / tot
        cxx, cyy, cxy = (w * (X - mx) ** 2).sum() / tot, (w * (Y - my) ** 2).sum() / tot, (w * (X - mx) * (Y - my)).sum() / tot
        th0 = 0.5 * math.atan2(2 * cxy, cxx - cyy); s0 = math.sqrt(max(cxx + cyy, 4 * (beam[0] / 2.3548) ** 2) / 2)
        p0 = [max(D.sum() / bp, 1e-6), mx, my, math.log(s0), math.log(0.7 * s0), th0]
    f = lambda p: (gauss2d_model(p, X, Y, Sb, pix, bp) - D) / sig
    lo = [-np.inf, -half, -half, math.log(1e-4), math.log(1e-4), -10]; hi = [np.inf, half, half, math.log(5.0), math.log(5.0), 10]
    p0 = np.clip(p0, np.array(lo) + 1e-9, np.array(hi) - 1e-9)
    r = optimize.least_squares(f, p0, bounds=(lo, hi), x_scale="jac", max_nfev=2000)
    J = r.jac
    try:
        cov = np.linalg.inv(np.einsum("ki,kj->ij", J, J))
    except np.linalg.LinAlgError:
        cov = np.full((6, 6), np.nan)
    F, x0, y0, lsa, lsb, th = r.x
    sa, sb = math.exp(lsa), math.exp(lsb)
    if sb > sa:
        sa, sb = sb, sa; th += math.pi / 2
    fc = 2.3548 * math.sqrt(sa * sb); vc = 0.25 * (cov[3, 3] + cov[4, 4] + 2 * cov[3, 4])
    return dict(F=F, eF=math.sqrt(max(cov[0, 0], 0)), x=x0, y=y0, fwhm_maj=2.3548 * sa, fwhm_min=2.3548 * sb, q=sb / sa, theta=th,
                fwhm_circ=fc, efwhm_circ=fc * math.sqrt(max(vc, 0)), chi2=float((r.fun ** 2).sum()), npix=int(sel.sum()),
                corr_factor=math.sqrt(bp))


def inc_from_q(q, q0=0.2):
    c2 = (q * q - q0 * q0) / (1 - q0 * q0)
    if c2 <= 0: return 90.0, True
    if c2 >= 1: return 0.0, True
    return math.degrees(math.acos(math.sqrt(c2))), False


# ------------------------------------------------------------------------------------------------ thin-disc cube model and fit
def kernel_rfft(shape, beam, pix, dtype=np.float64):
    from scipy import fft as sfft
    ny, nx = shape; yy, xx = np.indices(shape)
    X, Y = (xx - nx // 2) * pix, (yy - ny // 2) * pix
    inv = np.linalg.inv(beam_cov(beam))
    k = np.exp(-0.5 * (inv[0, 0] * X * X + 2 * inv[0, 1] * X * Y + inv[1, 1] * Y * Y)); k /= k.sum()
    return sfft.rfft2(np.fft.ifftshift(k).astype(dtype), workers=1)


def disc_model(p, X, Y, v, dv, inc, kpa, kf, q_int=None, dtype=np.float64):
    """p = [x0, y0, pa, vsys, vf, rt_kpc, s0, I0, h_arcsec]; V(R) = vf (2/pi) arctan(R/rt); exponential intensity; channel-integrated
    Gaussian line; beam convolution by FFT.  pa: angle of the receding major axis from +x (pixel frame)."""
    from scipy import fft as sfft
    x0, y0, pa, vsys, vf, rt, s0, I0, h = p
    c, s = math.cos(pa), math.sin(pa); ci, si = math.cos(math.radians(inc)), math.sin(math.radians(inc))
    xr = (X - x0) * c + (Y - y0) * s; yr = -(X - x0) * s + (Y - y0) * c
    R = np.sqrt(xr ** 2 + (yr / ci) ** 2); cth = xr / np.maximum(R, 1e-9)
    Vlos = (vsys + vf * (2 / math.pi) * np.arctan(R * kpa / rt) * si * cth).astype(dtype)
    qi = ci if q_int is None else q_int
    I = (I0 * np.exp(-np.sqrt(xr ** 2 + (yr / qi) ** 2) / h) / dv).astype(dtype)
    w = 1.0 / (math.sqrt(2) * s0)
    cube = np.empty((len(v),) + X.shape, dtype)
    for i, vk in enumerate(v):
        a = (vk - dv / 2 - Vlos) * w
        cube[i] = 0.5 * (special.erf(a + dv * w) - special.erf(a)) * I
    return sfft.irfft2(sfft.rfft2(cube, axes=(1, 2), workers=1, overwrite_x=True) * kf[None], s=X.shape, axes=(1, 2), workers=1, overwrite_x=True)


def vc_from_params(p, cov, R_kpc, Rd_kpc):
    """V_rot(R), P-B V_c = sqrt(V_rot^2 + 2 s0^2 R/Rd), P0 V_c = V_rot, with delta-method errors from cov (indices vf 4, rt 5, s0 6)."""
    vf, rt, s0 = p[4], p[5], p[6]
    at = math.atan(R_kpc / rt); Vr = vf * 2 / math.pi * at
    dVr = np.zeros(len(p)); dVr[4] = 2 / math.pi * at; dVr[5] = vf * 2 / math.pi * (-R_kpc / (rt * rt + R_kpc * R_kpc))
    Vpb = math.sqrt(Vr * Vr + 2 * s0 * s0 * R_kpc / Rd_kpc)
    dVpb = (Vr * dVr) / Vpb; dVpb[6] = 2 * s0 * R_kpc / Rd_kpc / Vpb
    e = lambda g: math.sqrt(max(float((g[:, None] * cov * g[None, :]).sum()), 0.0))
    return dict(Vrot=Vr, eVrot=e(dVr), Vc_PB=Vpb, eVc_PB=e(dVpb), Vc_P0=Vr, eVc_P0=e(dVr))


def lm_fit(res, p0, lo, hi, max_iter=80, tol=1e-9):
    """projected Levenberg-Marquardt that accumulates J^T J and J^T r column by column (J is never stored: low memory).
    Covariance = inv(J^T J) at the solution from central differences."""
    p = np.clip(np.asarray(p0, float), lo, hi); f = res(p); cost = float(np.sum(f * f)); nfev = 1; lam = 1e-3; status = 0
    def jtj(p, f, central=False):
        nonlocal nfev
        n = len(p); cols = []
        for i in range(n):
            h = 1e-4 * max(abs(p[i]), 1e-2 if i not in (7,) else abs(p[i]) + 1e-30)
            if central:
                pp, pm = p.copy(), p.copy(); pp[i] += h; pm[i] -= h; cols.append((res(pp) - res(pm)) / (2 * h)); nfev += 2
            else:
                pp = p.copy(); pp[i] = pp[i] + h if pp[i] + h <= hi[i] else pp[i] - h; cols.append((res(pp) - f) / (pp[i] - p[i])); nfev += 1
        A = np.array([[float(np.sum(c1 * c2)) for c2 in cols] for c1 in cols]); g = np.array([float(np.sum(c * f)) for c in cols]); del cols
        return A, g
    for it in range(max_iter):
        A, g = jtj(p, f)
        improved = False
        for _ in range(12):
            M = A + lam * np.diag(np.maximum(np.diag(A), 1e-30))
            try:
                d = -np.linalg.solve(M, g)
            except np.linalg.LinAlgError:
                lam *= 10; continue
            pn = np.clip(p + d, lo, hi); fn = res(pn); nfev += 1; cn = float(np.sum(fn * fn))
            if cn < cost:
                rel = (cost - cn) / max(cost, 1e-300); p, f, cost = pn, fn, cn; lam = max(lam / 3, 1e-9); improved = True; break
            lam *= 4
        if not improved: status = 2; break
        if rel < tol: status = 1; break
    A, _ = jtj(p, f, central=True)
    try:
        cov = np.linalg.inv(A)
    except np.linalg.LinAlgError:
        cov = np.full((len(p), len(p)), np.nan)
    return p, cov, cost, nfev, int(f.size), status


def fit_disc(box, inc, kpa, sig_vox, centre, pa0, vsys0, vf0, h0, R_kpc, Rd_kpc, rfit=1.4, vfit=600.0, I0=None):
    """Thin-disc forward-model fit (centre, PA, V_sys, V_f, R_t, sigma0, I0, h free; inclination fixed)."""
    v = box["v"]; sel_v = np.abs(v) <= vfit; data = box["data"][sel_v]; vv = v[sel_v]; dv = box["dv"]; pix = box["pix"]
    ny, nx = data.shape[1:]; hp = int(math.ceil(rfit / pix)) + 4
    xc, yc = box["xc"], box["yc"]
    x0i, x1i = max(0, int(xc) - hp), min(nx, int(xc) + hp + 1); y0i, y1i = max(0, int(yc) - hp), min(ny, int(yc) + hp + 1)
    sub = np.nan_to_num(data[:, y0i:y1i, x0i:x1i].astype(np.float64))
    yy, xx = np.indices(sub.shape[1:]); X, Y = (xx - (xc - x0i)) * pix, (yy - (yc - y0i)) * pix
    circ = np.hypot(X, Y) <= rfit
    kf = kernel_rfft(sub.shape[1:], box["beam"], pix)
    if I0 is None:
        I0 = max(float(np.nanmax(np.nansum(sub, axis=0)) * dv), 1e-12)
    p0 = np.array([centre[0], centre[1], pa0, vsys0, vf0, 1.0, 40.0, I0, h0])
    lo = np.array([-0.5, -0.5, pa0 - math.pi, -400, 10, 0.05, 3.0, 0.0, 0.01]); hi = np.array([0.5, 0.5, pa0 + math.pi, 400, 800, 15.0, 250, np.inf, 3.0])
    p0 = np.clip(p0, lo + 1e-6, hi - 1e-6)
    D = sub[:, circ]
    def res(p):
        m = disc_model(p, X, Y, vv, dv, inc, kpa, kf); return ((m[:, circ] - D) / sig_vox).ravel()
    x, cov, chi2, nfev, nvox, status = lm_fit(res, p0, lo, hi)
    bp = beam_pix(box["beam"], pix)
    out = dict(params=x.tolist(), names=["x0", "y0", "pa", "vsys", "vf", "rt_kpc", "s0", "I0", "h_arcsec"], chi2=chi2, nvox=nvox, nfev=nfev, status=status, inc=inc)
    out.update({k: v for k, v in vc_from_params(x, cov, R_kpc, Rd_kpc).items()})
    vb = vc_from_params(x, cov * bp, R_kpc, Rd_kpc)
    out.update({k + "_beamcorr": vb[k] for k in ("eVrot", "eVc_PB", "eVc_P0")})
    out["cov"] = cov.tolist()
    return out


def kinematic_pa(box, m0, mask, vwin, xc, yc):
    """initial guesses from the masked moment-1: receding-side direction, systemic velocity, velocity amplitude"""
    v = box["v"]; win = np.abs(v) <= vwin; d = np.nan_to_num(box["data"][win].astype(np.float64)); vv = v[win]
    w = np.clip(d, 0, None).sum(axis=0); m1 = np.where(w > 0, (np.clip(d, 0, None) * vv[:, None, None]).sum(axis=0) / np.maximum(w, 1e-30), 0.0)
    ys, xs = np.nonzero(mask)
    if ys.size < 5: return 0.0, 0.0, 150.0, m1
    wt = m0[ys, xs].clip(0); vs = float((wt * m1[ys, xs]).sum() / max(wt.sum(), 1e-30))
    gx = float((wt * (m1[ys, xs] - vs) * (xs - xc)).sum()); gy = float((wt * (m1[ys, xs] - vs) * (ys - yc)).sum())
    amp = float(np.percentile(np.abs(m1[ys, xs] - vs), 90))
    return math.atan2(gy, gx), vs, max(amp, 30.0), m1


# ------------------------------------------------------------------------------------------------ MOCK cubes (never real data)
def beam_noise(rng, shape, beam, pix, sigma):
    kf = kernel_rfft(shape, (beam[0] / math.sqrt(2), beam[1] / math.sqrt(2), beam[2]), pix)
    n = np.fft.irfft2(np.fft.rfft2(rng.standard_normal(shape)) * kf, s=shape)
    return (n * (sigma / n.std())).astype(np.float32)


def write_mock_cube(path, sp):
    """sp: ra, dec, nu_line (observed line GHz), restfrq, pix, n, beam (fwhm, fwhm, bpa), dv, vlo, vhi, inc, pa, q_int, h, vf, rt, s0, kpa,
    SdV (Jy km/s), sigma (Jy/beam per channel), seed, label, true (dict of true values written to the header). Written channel by channel."""
    from astropy.io import fits
    rng = np.random.default_rng(sp["seed"]); n = sp["n"]; pix = sp["pix"]
    v = np.arange(sp["vlo"], sp["vhi"] + 1e-6, sp["dv"]); nch = len(v)
    yy, xx = np.indices((n, n)); X, Y = (xx - n // 2) * pix, (yy - n // 2) * pix
    bp = beam_pix(sp["beam"], pix); kf = kernel_rfft((n, n), sp["beam"], pix)
    kn = kernel_rfft((n, n), (sp["beam"][0] / math.sqrt(2), sp["beam"][1] / math.sqrt(2), sp["beam"][2]), pix)   # noise autocorrelation = beam
    msub = min(n, 2 * int(math.ceil((10 * sp["h"] + 4 * sp["beam"][0]) / pix)) + 1); a0 = n // 2 - msub // 2
    Xs, Ys = X[a0:a0 + msub, a0:a0 + msub], Y[a0:a0 + msub, a0:a0 + msub]; kfs = kernel_rfft((msub, msub), sp["beam"], pix, np.float32)
    if sp["SdV"] > 0:
        c, s = math.cos(sp["pa"]), math.sin(sp["pa"]); xr = X * c + Y * s; yr = -X * s + Y * c
        I0 = sp["SdV"] * bp / np.exp(-np.sqrt(xr ** 2 + (yr / sp["q_int"]) ** 2) / sp["h"]).sum()
        p = [0.0, 0.0, sp["pa"], 0.0, sp["vf"], sp["rt"], sp["s0"], I0, sp["h"]]
    nu = sp["nu_line"] * (1 - v / CKMS)
    h = fits.Header()
    h["SIMPLE"] = True; h["BITPIX"] = -32; h["NAXIS"] = 3; h["NAXIS1"] = n; h["NAXIS2"] = n; h["NAXIS3"] = nch
    h["OBJECT"] = "MOCK"; h["COMMENT"] = "MOCK cube generated by the CFG942 harness. NOT ALMA DATA."; h["MOCKLAB"] = sp["label"]
    h["BUNIT"] = "Jy/beam"; h["CTYPE1"] = "RA---SIN"; h["CTYPE2"] = "DEC--SIN"; h["CUNIT1"] = h["CUNIT2"] = "deg"
    h["CRVAL1"], h["CRVAL2"] = sp["ra"], sp["dec"]; h["CRPIX1"] = h["CRPIX2"] = n // 2 + 1
    h["CDELT1"], h["CDELT2"] = -pix / 3600.0, pix / 3600.0
    h["CTYPE3"] = "FREQ"; h["CUNIT3"] = "Hz"; h["CRVAL3"] = nu[0] * 1e9; h["CRPIX3"] = 1.0; h["CDELT3"] = (nu[1] - nu[0]) * 1e9
    h["SPECSYS"] = "LSRK"; h["RESTFRQ"] = sp["restfrq"] * 1e9
    h["BMAJ"], h["BMIN"], h["BPA"] = sp["beam"][0] / 3600.0, sp["beam"][1] / 3600.0, sp["beam"][2]
    for k, val in sp.get("true", {}).items(): h["HIERARCH MOCK " + k] = val
    if os.path.exists(path): os.remove(path)
    sh = fits.StreamingHDU(path, h)
    for j0 in range(0, nch, 4):
        vv = v[j0:j0 + 4]; blk = np.zeros((len(vv), n, n), np.float32)
        if sp["SdV"] > 0 and np.any(np.abs(vv) <= 900):
            blk[:, a0:a0 + msub, a0:a0 + msub] += disc_model(p, Xs, Ys, vv, sp["dv"], sp["inc"], sp["kpa"], kfs, q_int=sp["q_int"], dtype=np.float32) * (np.abs(vv) <= 900)[:, None, None]
        for i in range(len(vv)):
            nz = np.fft.irfft2(np.fft.rfft2(rng.standard_normal((n, n))) * kn, s=(n, n)); blk[i] += (nz * (sp["sigma"] / nz.std())).astype(np.float32)
        sh.write(blk.astype(">f4"))
    sh.close()
    return sha256_file(path)


def write_mock_image(path, sp):
    """2D MOCK continuum image: exponential disc of total flux S (Jy), beam-convolved, plus beam-correlated noise."""
    from astropy.io import fits
    rng = np.random.default_rng(sp["seed"]); n = sp["n"]; pix = sp["pix"]
    yy, xx = np.indices((n, n)); X, Y = (xx - n // 2) * pix, (yy - n // 2) * pix
    c, s = math.cos(sp["pa"]), math.sin(sp["pa"]); xr = X * c + Y * s; yr = -X * s + Y * c
    I = np.exp(-np.sqrt(xr ** 2 + (yr / sp["q_int"]) ** 2) / sp["h"]); I *= sp["S"] * beam_pix(sp["beam"], pix) / I.sum()
    img = np.fft.irfft2(np.fft.rfft2(I) * kernel_rfft((n, n), sp["beam"], pix), s=(n, n)) + beam_noise(rng, (n, n), sp["beam"], pix, sp["sigma"])
    h = fits.Header()
    h["OBJECT"] = "MOCK"; h["COMMENT"] = "MOCK continuum generated by the CFG942 harness. NOT ALMA DATA."; h["MOCKLAB"] = sp["label"]
    h["BUNIT"] = "Jy/beam"; h["CTYPE1"] = "RA---SIN"; h["CTYPE2"] = "DEC--SIN"; h["CUNIT1"] = h["CUNIT2"] = "deg"
    h["CRVAL1"], h["CRVAL2"] = sp["ra"], sp["dec"]; h["CRPIX1"] = h["CRPIX2"] = n // 2 + 1
    h["CDELT1"], h["CDELT2"] = -pix / 3600.0, pix / 3600.0
    h["BMAJ"], h["BMIN"], h["BPA"] = sp["beam"][0] / 3600.0, sp["beam"][1] / 3600.0, sp["beam"][2]
    fits.PrimaryHDU(img.astype(np.float32), h).writeto(path, overwrite=True)
    return sha256_file(path)


# ------------------------------------------------------------------------------------------------ R7 sensitivity forecast
def aperture_noise_SdV(sens10_mJy, beam_fwhm, r_ap, W):
    """noise on S dv (Jy km/s) in a circular aperture of radius r_ap (arcsec) over a velocity window W (km/s), from the archive
    line sensitivity at 10 km/s (mJy/beam), with N_beam = area / (1.1331 theta^2) independent beams."""
    nb = max(1.0, math.pi * r_ap ** 2 / (1.1331 * beam_fwhm ** 2))
    return sens10_mJy * 1e-3 * 10.0 * math.sqrt(W / 10.0) * math.sqrt(nb), nb


def exp_frac(r_over_Rd):
    x = r_over_Rd; return 1 - (1 + x) * math.exp(-x)
