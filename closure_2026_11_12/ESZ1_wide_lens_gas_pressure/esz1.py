#!/usr/bin/env python3
"""ESZ1 (WIDE-LENS GAS PRESSURE).  Frozen criteria: FROZEN_CRITERIA.md (commit 07a07ec1a6).

Is the hot gas there that law S would need to supply Euclid's wide-separation lenses?
Part G: the gas body law S needs per lens, its least hydrostatic pressure, against a stack of the ACT Compton-y map.
Part C: wide lenses against controls matched in redshift and stellar mass.
Part D: what the stack measures, in physical units.

Run (map directory = the folder holding strip_*.f32be, south_*.f32be and header_ComptonY.fits):
  python3 -I esz1.py --data-dir <ECLIPSE csv dir> --y-dir <map dir> --erass <erass1_main.tsv>
  ESZ1_MUTATE=inject python3 -I esz1.py ...     (must exit 1)
  ESZ1_MUTATE=shift  python3 -I esz1.py ...     (must exit 1)
  ESZ1_MUTATE=newton python3 -I esz1.py ...     (must exit 1)
"""
import argparse, csv, hashlib, json, math, os, sys, time
import numpy as np
from scipy.special import i0e
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in ("EUC1_eclipse_saturation_ceiling", "EUC4_wide_lenses", "EUC8_wide_lens_residual_profile"):
    sys.path.insert(0, os.path.join(HERE, "..", _d))
import euc1 as E
import euc4 as G4
import euc8 as L8
MUT = (os.environ.get("ESZ1_MUTATE", "") or "").strip()
if MUT == "newton": E.FOOT = {k: 1.0e-30 for k in E.FOOT}
G, C, MSUN, KPC = E.G, E.C, E.MSUN, E.KPC
MPC = 1.0e3 * KPC
MP, SIGT, MEC2, KEV = 1.67262192e-27, 6.6524587e-29, 8.1871058e-14, 1.602176634e-16
MU, MUE = 0.59, 1.14
KSZ = SIGT / MEC2
ARCMIN = math.pi / 10800.0
NX, RSPLIT, ROWS, PIX = 43200, 3239, 8041, 0.5
HB = 52                                   # 26 arcmin in rows
THD = (2.0, 1.5, 3.0)                     # primary first
SQ2 = math.sqrt(2.0)
SIGB = 1.6 / (2.0 * math.sqrt(2.0 * math.log(2.0)))
MAPS = ("ComptonY", "ComptonY_deproj_cib_1.0_10.7")
FAMS = ("B30", "B100", "G2")
CASES = ("far", "central", "near")
BSTAR = (-0.10, 0.0, 0.10)
SHARE = 5.41
RT = 300.0 * KPC
NBOOT = 2000
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

cof =lambda ra: 21600.0 - 120.0 * (ra - 360.0 if ra >= 180.0 else ra)
rof = lambda de: 7559.5 + 120.0 * de

class YMap:
    def __init__(self, ydir, name):
        self.s = np.memmap(os.path.join(ydir, "south_%s.f32be" % name), dtype=">f4", mode="r", shape=(RSPLIT, NX))
        self.n = np.memmap(os.path.join(ydir, "strip_%s.f32be" % name), dtype=">f4", mode="r", shape=(ROWS - RSPLIT, NX))
    def block(self, r0, r1, cols):
        if r1 <= RSPLIT: a = self.s[r0:r1]
        elif r0 >= RSPLIT: a = self.n[r0 - RSPLIT:r1 - RSPLIT]
        else: a = np.vstack([np.asarray(self.s[r0:RSPLIT]), np.asarray(self.n[0:r1 - RSPLIT])])
        if cols[-1] > cols[0] and cols[-1] - cols[0] == len(cols) - 1: return np.asarray(a[:, cols[0]:cols[-1] + 1], dtype=float)
        return np.asarray(a[:, cols], dtype=float)
    def row(self, r):
        return np.asarray(self.s[r] if r < RSPLIT else self.n[r - RSPLIT], dtype=float)

def measure(YM, ra, dec):
    """one position: (inside, finite on the primary map, rms outside 6', caps[map][theta], finite on the bracket map)."""
    cosd = math.cos(math.radians(dec)); hw = int(math.ceil(HB / cosd))
    cx, cy = cof(ra), rof(dec); ic, iy = int(round(cx)), int(round(cy))
    if iy - HB < 0 or iy + HB > ROWS - 1: return None
    cols = np.arange(ic - hw, ic + hw + 1) % NX
    dx = (np.arange(-hw, hw + 1) - (cx - ic)) * PIX * cosd; dy = (np.arange(-HB, HB + 1) - (cy - iy)) * PIX
    sq = (np.abs(dx)[None, :] <= 26.0) & (np.abs(dy)[:, None] <= 26.0)
    rr = np.hypot(dx[None, :], dy[:, None]); om = PIX * PIX * cosd
    disks = [(rr < t, (rr >= t) & (rr < SQ2 * t)) for t in THD]
    res = []
    for m in YM:
        img = m.block(iy - HB, iy + HB + 1, cols)
        fin = bool(np.isfinite(img[sq]).all())
        rms = float(np.std(img[sq & (rr > 6.0)])) if fin else float("nan")
        caps = [om * (img[d].sum() - d.sum() / max(r.sum(), 1) * img[r].sum()) if fin else float("nan") for d, r in disks]
        res.append((fin, rms, caps))
    return res

def offsets(ra, dec):
    out = []
    for k in range(16):
        ph = math.radians(22.5 * k)
        out.append(((ra + (20.0 / 60.0) * math.sin(ph) / math.cos(math.radians(dec))) % 360.0, dec + (20.0 / 60.0) * math.cos(ph)))
    return out

def measure_targets(YM, pos, label):
    """pos: list of (ra, dec).  Returns ok[n,17], rms[n,17], cap[n,17,2,3], fin1[n,17]."""
    n = len(pos); ok = np.zeros((n, 17), bool); rms = np.full((n, 17), np.nan); cap = np.full((n, 17, 2, 3), np.nan); f1 = np.zeros((n, 17), bool)
    t0 = time.time()
    for i, (ra, dec) in enumerate(pos):
        for k, (a, d) in enumerate([(ra, dec)] + offsets(ra, dec)):
            r = measure(YM, a, d)
            if r is None: continue
            ok[i, k] = r[0][0]; rms[i, k] = r[0][1]; cap[i, k, 0] = r[0][2]; cap[i, k, 1] = r[1][2]; f1[i, k] = r[1][0]
    P("  measured %-9s %6d targets x 17 positions x 2 maps" % (label, n))
    print("    (%.0f s)" % (time.time() - t0), file=sys.stderr, flush=True)
    return ok, rms, cap, f1

def values(ok, rms, cap, f1, lo, hi):
    """coverage, values (target minus the mean of its covered offsets) and the 16 null values, per map and theta."""
    cov = ok & (rms >= lo) & (rms <= hi)
    oc = cov[:, 1:]; noff = oc.sum(1); valid = cov[:, 0] & (noff >= 12)
    n = len(cov); val = np.full((n, 2, 3), np.nan); nul = np.full((n, 16, 2, 3), np.nan)
    for m in range(2):
        ocm = oc & (f1[:, 1:] if m == 1 else True); nm = ocm.sum(1)
        vm = valid & (f1[:, 0] if m == 1 else True) & (nm >= 12)
        for t in range(3):
            co = np.where(ocm, cap[:, 1:, m, t], 0.0); tot = co.sum(1)
            with np.errstate(invalid="ignore", divide="ignore"):
                val[:, m, t] = np.where(vm, cap[:, 0, m, t] - tot / np.maximum(nm, 1), np.nan)
                for k in range(16):
                    nul[:, k, m, t] = np.where(vm & ocm[:, k], cap[:, 1 + k, m, t] - (tot - co[:, k]) / np.maximum(nm - 1, 1), np.nan)
    return cov, valid, noff, val, nul

def stack(v, nul, seed, w=None):
    """mean, sigma = max(bootstrap, rms of the 16 null stacks).  w multiplies each target's value (and its nulls)."""
    v = np.asarray(v, float); keep = np.isfinite(v); v = v[keep]; nul = np.asarray(nul, float)[keep]
    if w is not None: w = np.asarray(w, float)[keep]; v = v * w; nul = nul * w[:, None]
    N = len(v)
    if N == 0: return dict(N=0, mean=float("nan"), sigma=float("nan"), sig_boot=float("nan"), sig_null=float("nan"), nulls=[])
    rng = np.random.default_rng(E.SEED)            # the one frozen seed for every stack (the argument seed is unused)
    bs = v[rng.integers(0, N, (NBOOT, N))].mean(1); ns = np.nanmean(nul, axis=0)
    sb, sn = float(bs.std()), float(np.sqrt(np.mean(ns ** 2)))
    return dict(N=N, mean=float(v.mean()), sigma=max(sb, sn), sig_boot=sb, sig_null=sn, nulls=[float(x) for x in ns])

# ---------------------------------------------------------------- model
GLX, GLW = np.polynomial.legendre.leggauss(160); GLX = 0.5 * (GLX + 1.0); GLW = 0.5 * GLW
NRAD, NRP = 1000, 240
THG = np.arange(0.0, 6.0001, 0.02)
def grids(rout):
    """radial grid, projected-radius grid and the matrix that turns electron pressure on r into y on R."""
    r = np.geomspace(0.02 * KPC, rout, NRAD); R = np.geomspace(0.05 * KPC, rout * (1.0 - 1.0e-6), NRP)
    A = np.zeros((NRP, NRAD)); lr0 = math.log(r[0]); h = math.log(r[1] / r[0])
    for j, Rj in enumerate(R):
        U = math.acosh(rout / Rj); u = U * GLX; rr = Rj * np.cosh(u); w = 2.0 * KSZ * U * GLW * rr
        t = (np.log(rr) - lr0) / h; i0 = np.clip(np.floor(t).astype(int), 0, NRAD - 2); f = np.clip(t - i0, 0.0, 1.0)
        np.add.at(A[j], i0, w * (1.0 - f)); np.add.at(A[j], i0 + 1, w * f)
    return r, R, A
GRID = {}
def grid(rout_kpc):
    if rout_kpc not in GRID: GRID[rout_kpc] = grids(rout_kpc * KPC)
    return GRID[rout_kpc]

def lnw(x):
    dl = math.log(x[1] / x[0]); w = np.full(len(x), dl); w[0] = w[-1] = 0.5 * dl
    return w
def beam_matrix(th, thp):
    """K[k, j]: beam-convolved profile at th[k] from the profile on the log grid thp (arcmin)."""
    a, b = th[:, None], thp[None, :]
    return (b * b / SIGB ** 2) * np.exp(-(a - b) ** 2 / (2.0 * SIGB ** 2)) * i0e(a * b / SIGB ** 2) * lnw(thp)[None, :]

def pixgeom(ra, dec, thmax):
    cosd = math.cos(math.radians(dec)); cx, cy = cof(ra), rof(dec); fx, fy = cx - round(cx), cy - round(cy)
    hw = int(math.ceil(SQ2 * thmax / PIX / cosd)) + 2; hh = int(math.ceil(SQ2 * thmax / PIX)) + 2
    dx = (np.arange(-hw, hw + 1) - fx) * PIX * cosd; dy = (np.arange(-hh, hh + 1) - fy) * PIX
    return dx, dy, cosd, fx, fy
def cap_weights(ra, dec, thd):
    """c on THG such that the model's CAP on this lens's pixel grid is c . y_beam(THG) (3 x 3 sub-samples per pixel)."""
    dx, dy, cosd, _, _ = pixgeom(ra, dec, thd)
    rr = np.hypot(dx[None, :], dy[:, None]); disk = rr < thd; ring = (rr >= thd) & (rr < SQ2 * thd)
    wp = PIX * PIX * cosd * (disk.astype(float) - disk.sum() / ring.sum() * ring); sel = wp != 0.0
    c = np.zeros(len(THG)); dth = THG[1] - THG[0]
    for sx in (-1.0 / 3.0, 0.0, 1.0 / 3.0):
        for sy in (-1.0 / 3.0, 0.0, 1.0 / 3.0):
            rs = np.hypot(dx[None, :] + sx * PIX * cosd, dy[:, None] + sy * PIX)[sel]
            t = rs / dth; i0 = np.clip(np.floor(t).astype(int), 0, len(THG) - 2); f = t - i0
            np.add.at(c, i0, wp[sel] / 9.0 * (1.0 - f)); np.add.at(c, i0 + 1, wp[sel] / 9.0 * f)
    return c

FAMDEF = {"B30": ("beta", 30.0, 500.0), "B100": ("beta", 100.0, 500.0), "G2": ("iso", None, 300.0), "CS": ("beta", 100.0, 300.0)}
def gas_body(fam, Mg, r):
    """enclosed mass and density (N x Nr) of the gas body with mass Mg (kg) inside its cut-off."""
    kind, rc, rcut = FAMDEF[fam]; Mg = np.asarray(Mg, float)[:, None]
    if kind == "iso":
        return Mg * (r / RT)[None, :], Mg / (4.0 * math.pi * RT * r ** 2)[None, :]
    rc *= KPC; x = r / rc; X = rcut * KPC / rc; nrm = X - math.atan(X)
    return Mg * ((x - np.arctan(x)) / nrm)[None, :], Mg / (4.0 * math.pi * rc ** 3 * nrm) / (1.0 + x * x)[None, :]
def gas_density_at(fam, Mg, rr):
    kind, rc, rcut = FAMDEF[fam]
    if kind == "iso": return Mg / (4.0 * math.pi * RT * rr ** 2)
    rc *= KPC; X = rcut * KPC / rc
    return Mg / (4.0 * math.pi * rc ** 3 * (X - math.atan(X))) / (1.0 + (rr / rc) ** 2)
def pressure(r, rho, g):
    """hydrostatic pressure with zero pressure at the outer edge: P(r) = int_r^rout rho g dr (trapezoid in ln r)."""
    f = rho * g * r[None, :]; h = math.log(r[1] / r[0]); seg = 0.5 * (f[:, :-1] + f[:, 1:]) * h
    Pr = np.zeros_like(f); Pr[:, :-1] = np.cumsum(seg[:, ::-1], axis=1)[:, ::-1]
    return Pr

class Model:
    """per-lens pieces that do not depend on the gas: stellar field on both radial grids and the CAP response vectors."""
    def __init__(self, ra, dec, z, RE, Re, n, Ms):
        self.N = len(z); self.z, self.RE, self.Re, self.n, self.Ms = z, RE, Re, n, Ms
        self.DA = E.EUCLID.DA(z); self.gs0, self.q = {}, {}
        for rout in (500.0, 300.0):
            r, R, A = grid(rout)
            self.gs0[rout] = G * Ms[:, None] * E.M3D_frac(r[None, :], Re[:, None], n[:, None]) / r[None, :] ** 2
            q = np.zeros((len(THD), self.N, NRAD))
            for i in range(self.N):
                K = beam_matrix(THG, R / self.DA[i] / ARCMIN)
                for t, thd in enumerate(THD): q[t, i] = (cap_weights(ra[i], dec[i], thd) @ K) @ A
            assert np.isfinite(q).all()
            self.q[rout] = q
    def run(self, fam, Mg, Bs, a0, gx=None):
        """CAP (arcmin^2) per theta_d and lens, mass-weighted kT (keV), electron density at R_E (cm^-3)."""
        rout = FAMDEF[fam][2]; r = grid(rout)[0]
        Menc, rho = gas_body(fam, Mg, r)
        gN = Bs * self.gs0[rout] + G * Menc / r[None, :] ** 2
        if gx is not None: gN = gN + gx
        Pr = pressure(r, rho, E.g_law(gN, a0, "S"))
        cap = np.einsum("tim,im->ti", self.q[rout], Pr * (MU / MUE))          # arcmin^2 (the weights carry the pixel solid angle)
        with np.errstate(invalid="ignore", divide="ignore"):
            kT = np.where(Mg > 0, MU * MP * 4.0 * math.pi * np.sum(Pr * r[None, :] ** 3 * lnw(r)[None, :], axis=1) / np.maximum(Mg, 1e-300), np.nan) / KEV
        ne = gas_density_at(fam, Mg, self.RE) / (MUE * MP) * 1.0e-6
        return cap, kT, ne

def solve_gas(fam, RE, Re, n, Ms, Mt, Bs, a0, eng):
    """gas mass (kg) inside the family's cut-off so that stars + gas under law S give the lensing mass Mt."""
    if fam == "G2":
        A, need = eng["L2"].solve(Mt, Bs, eng["gx2"], a0); return np.where(need, A, 0.0)
    lg, none = eng[fam].solve(Mt, Bs, a0)
    return np.where(np.isfinite(lg), 10.0 ** np.where(np.isfinite(lg), lg, 0.0) * MSUN, 0.0)
def engines(RE, Re, n, Ms):
    L2 = L8.Lens2(RE, Re, n, Ms)
    return {"B30": G4.GasEngine(RE, Re, n, Ms, 30.0 * KPC), "B100": G4.GasEngine(RE, Re, n, Ms, 100.0 * KPC), "L2": L2, "gx2": L2.gx("2.0")}

def brute_cap(thp, y, ra, dec, thd):
    """independent rendering: profile drawn at 0.05', convolved in 2D, rebinned to the lens's 0.5' pixel grid, same estimator."""
    fp, half = 0.05, 9.0; n = int(round(2 * half / fp)); ax = (np.arange(n) + 0.5) * fp - half
    img = np.zeros((n, n)); ss = (np.arange(5) + 0.5) / 5.0 - 0.5; ly = np.log(thp)
    for sx in ss:
        for sy in ss:
            rr = np.hypot(ax[None, :] + sx * fp, ax[:, None] + sy * fp)
            img += np.interp(np.log(np.maximum(rr, thp[0])), ly, y, right=0.0)
    img = gaussian_filter(img / 25.0, SIGB / fp, mode="constant", truncate=6.0)
    dx, dy, cosd, fx, fy = pixgeom(ra, dec, thd); hw, hh = (len(dx) - 1) // 2, (len(dy) - 1) // 2
    kx = np.floor(ax / (PIX * cosd) + fx + 0.5).astype(int) + hw; ky = np.floor(ax / PIX + fy + 0.5).astype(int) + hh
    okx, oky = (kx >= 0) & (kx < len(dx)), (ky >= 0) & (ky < len(dy))
    flat = (ky[:, None] * len(dx) + kx[None, :])[np.ix_(oky, okx)].ravel(); v = img[np.ix_(oky, okx)].ravel()
    cnt = np.bincount(flat, minlength=len(dx) * len(dy)); s = np.bincount(flat, v, minlength=len(dx) * len(dy))
    co = (s / np.maximum(cnt, 1)).reshape(len(dy), len(dx))
    rr = np.hypot(dx[None, :], dy[:, None]); d = rr < thd; rg = (rr >= thd) & (rr < SQ2 * thd)
    return PIX * PIX * cosd * (co[d].sum() - d.sum() / rg.sum() * co[rg].sum())

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()

def fam_word(meas, sig, pmin):
    if not (np.isfinite(meas) and np.isfinite(sig) and np.isfinite(pmin)): return "NO POWER"
    if pmin < 3.0 * sig: return "NO POWER"
    return "EXCLUDED" if meas + 2.0 * sig < pmin else "ALLOWED"
def lane_word(fw, nW, checks_ok):
    if not checks_ok or nW < 100: return "NOT EVALUABLE"
    if all(fw[f] == "EXCLUDED" for f in FAMS): return "HOT GAS DOES NOT SUPPLY THE WIDE LENSES"
    if fw["B30"] == "EXCLUDED" and fw["B100"] == "EXCLUDED": return "ONLY A CUSP IS LEFT"
    if fw["B30"] == "ALLOWED" or fw["B100"] == "ALLOWED": return "HOT GAS NOT EXCLUDED"
    return "NO VERDICT"

# ================================================================== main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True); ap.add_argument("--y-dir", required=True); ap.add_argument("--erass", required=True)
    ap.add_argument("--checks-only", action="store_true", help="run the instrument checks that need no stack, then stop")
    a = ap.parse_args(); t0 = time.time(); tag = "esz1" + ("_MUTATE_" + MUT if MUT else "")
    P("ESZ1 (WIDE-LENS GAS PRESSURE)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    RES = dict(lane="ESZ1", criteria_commit="07a07ec1a6", mutate=MUT, footings=E.FOOT)
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    SHIFT = 0.5 if MUT == "shift" else 0.0

    # ---------------------------------------------------------------- catalogue
    P("\n[data]")
    rows, _ = E.load(a.data_dir); OUT.extend(E.OUT); E.OUT.clear()
    radec = {}
    with open(os.path.join(a.data_dir, "eclipse_dr1_catalogue_key_v20261103.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): radec[r["unique_identifier"]] = (E.fl(r["ra"]), E.fl(r["dec"]))
    S, _ = E.select(rows, ("A", "B")); S = sorted([r for r in S if np.isfinite(radec[r["id"]]).all()], key=lambda r: r["id"])
    LL = sorted([r for r in rows if r["grade"] in ("A", "B") and r["large"] and np.isfinite(radec[r["id"]]).all()], key=lambda r: r["id"])
    P("  sample S (grades A and B, EUC1's select): %d lenses; flagged large systems L: %d" % (len(S), len(LL)))
    CL = []
    for r in (l.rstrip("\n").split("\t") for l in open(a.erass, encoding="latin-1")):
        try: ra, de, z, M5 = float(r[1]), float(r[2]), float(r[3]), float(r[10]) * 1.0e13
        except Exception: continue
        if M5 >= 2.0e14 and 0.1 <= z <= 0.6: CL.append((ra, de, z, M5))
    P("  eRASS1 clusters with M500 >= 2e14 Msun, 0.1 <= z <= 0.6 (whole table): %d" % len(CL))

    # ---------------------------------------------------------------- maps
    YM = [YMap(a.y_dir, m) for m in MAPS]
    sizes = [os.path.getsize(os.path.join(a.y_dir, "south_%s.f32be" % m)) for m in MAPS]
    for m in MAPS:
        P("  sha256 south_%s.f32be  %s" % (m, sha256(os.path.join(a.y_dir, "south_%s.f32be" % m))))

    # ---------------------------------------------------------------- instrument checks that need no stack
    P("\n[instrument checks]")
    from astropy.io import fits
    from astropy.wcs import WCS
    hd = fits.Header.fromstring(open(os.path.join(a.y_dir, "header_ComptonY.fits"), "rb").read(2880).decode("ascii"))
    tp = np.array([[12.3, -5.0], [47.7, -56.2], [60.0, -45.0], [355.2, 2.9]]); px = WCS(hd).all_world2pix(tp, 0)
    geo = max(max(abs(cof(x) - p[0]), abs(rof(y) - p[1])) for (x, y), p in zip(tp, px))
    ck("K1", "pixel map against the header's WCS at four points (< 0.01 pixel)", "%.1e" % geo, geo < 0.01)
    seam = []
    for m in YM:
        r0, r1, r2 = m.row(RSPLIT - 1), m.row(RSPLIT), m.row(RSPLIT + 1)
        b1 = r1.reshape(432, 100).std(1); b0 = r0.reshape(432, 100).std(1); med = np.median(b1)
        inb = np.repeat((b1 >= 0.5 * med) & (b1 <= 2.0 * med) & (b0 >= 0.5 * med) & (b0 <= 2.0 * med), 100)
        seam.append((float(np.corrcoef(r0[inb], r1[inb])[0, 1]), float(np.corrcoef(r1[inb], r2[inb])[0, 1]), int(inb.sum())))
    ck("K2", "new files are 559,699,200 bytes; rows 3238|3239 correlate at >= 0.9 x rows 3239|3240, both maps",
       "sizes %s; corr %.3f vs %.3f (%d columns) and %.3f vs %.3f (%d)" % (sizes, seam[0][0], seam[0][1], seam[0][2], seam[1][0], seam[1][1], seam[1][2]),
       all(s == 559699200 for s in sizes) and all(c[0] >= 0.9 * c[1] for c in seam))

    # whole-sky W for the reproduction checks and the model
    Wall = [r for r in S if r["tE"] >= 1.7]
    engW, zW, REW, ReW, nW, lmW = E.build(Wall); MsW = 10.0 ** lmW * MSUN
    raW = np.array([radec[r["id"]][0] for r in Wall]); deW = np.array([radec[r["id"]][1] + SHIFT for r in Wall])
    ENG = engines(REW, ReW, nW, MsW)
    MtW = {c: math.pi * REW ** 2 * E.EUCLID.sigcr(zW, L8.zs_case(zW, c)) for c in CASES}
    # K4 hydrostatic solver, Newtonian, G2 alone
    r3 = grid(300.0)[0]; Mt4 = 1.0e13 * MSUN
    Me, rho = gas_body("G2", np.array([Mt4]), r3); Pn = pressure(r3, rho, E.g_law(G * Me / r3[None, :] ** 2, 1.0e-30, "S"))[0]
    e4 = 0.0
    for fr in (0.01, 0.1, 0.5):
        j = int(np.argmin(np.abs(r3 - fr * RT))); ana = G * Mt4 ** 2 / (8.0 * math.pi * RT ** 2) * (r3[j] ** -2 - RT ** -2)
        e4 = max(e4, abs(Pn[j] / ana - 1.0))
    ck("K4", "hydrostatic solver, Newtonian r^-2 gas alone, at the grid nodes nearest 0.01, 0.1, 0.5 r_t (1e-4)", "%.1e" % e4, e4 < 1.0e-4)
    # K5 beam
    thp = np.geomspace(1.0e-4, 1.0e-2, 60); th = np.arange(0.0, 8.0001, 0.01); yb = beam_matrix(th, thp) @ np.ones(60)
    Yin = 2.0 * math.pi * np.sum(thp ** 2 * lnw(thp)); cum = np.concatenate([[0.0], np.cumsum(0.5 * (yb[1:] * th[1:] + yb[:-1] * th[:-1]) * 2.0 * math.pi * 0.01)]) / Yin
    e5a = max(abs(cum[int(round(t / 0.01))] - (1.0 - math.exp(-t * t / (2.0 * SIGB ** 2)))) for t in (1.0, 2.0, 3.0))
    # the median W lens (middle of W sorted by theta_E)
    iw = int(np.argsort(E.arr(Wall, "tE"), kind="stable")[len(Wall) // 2]); one = np.array([iw])
    M1 = Model(raW[one], deW[one], zW[one], REW[one], ReW[one], nW[one], MsW[one])
    a0c = list(E.FOOT.values())[0]; prof = {}
    for fam in FAMS:
        Mg = solve_gas(fam, REW, ReW, nW, MsW, MtW["far"], 1.0, a0c, ENG)[one]; rout = FAMDEF[fam][2]; r, R, A = grid(rout)
        Me, rho = gas_body(fam, Mg, r); Pr = pressure(r, rho, E.g_law(M1.gs0[rout] + G * Me / r[None, :] ** 2, a0c, "S"))[0]
        prof[fam] = (R / M1.DA[0] / ARCMIN, A @ (Pr * MU / MUE), M1.run(fam, Mg, 1.0, a0c)[0][:, 0])
    tb, yb100, _ = prof["B100"]; th2 = np.arange(0.0, tb[-1] + 6.0, 0.01); ybb = beam_matrix(th2, tb) @ yb100
    e5b = abs(TRAPZ(ybb * 2.0 * math.pi * th2, th2) / (2.0 * math.pi * np.sum(yb100 * tb ** 2 * lnw(tb))) - 1.0)
    ck("K5", "beam: point-source fraction inside 1, 2, 3 arcmin and total Y of a B100 profile conserved (1e-3)", "%.1e ; %.1e" % (e5a, e5b), e5a < 1e-3 and e5b < 1e-3)
    # K3 prediction against brute force
    e3 = {}
    for fam in FAMS:
        tpf, yf, capf = prof[fam]
        e3[fam] = max(abs(capf[t] / brute_cap(tpf, yf, raW[iw], deW[iw], thd) - 1.0) for t, thd in enumerate(THD))
    ck("K3", "predicted CAP of the median W lens against a brute-force rendering (3 % B30, B100; 5 % G2; three apertures)",
       "B30 %.2f %%, B100 %.2f %%, G2 %.2f %%" % (100 * e3["B30"], 100 * e3["B100"], 100 * e3["G2"]), e3["B30"] < 0.03 and e3["B100"] < 0.03 and e3["G2"] < 0.05)
    if not MUT:
        Pm, _ = E.select(rows, ("A",)); Bm, _ = E.select(rows, ("B",)); wide4 = [r for r in Pm if r["tE"] >= 1.7] + [r for r in Bm if r["tE"] >= 1.7]
        _, z4, RE4, Re4, n4, lm4 = E.build(wide4); Mm4 = math.pi * RE4 ** 2 * E.EUCLID.sigcr(z4, E.ZS_INF); got = []
        for rc in (30.0, 100.0):
            ge = G4.GasEngine(RE4, Re4, n4, 10.0 ** lm4 * MSUN, rc * KPC)
            for a0 in E.FOOT.values():
                lg, _ = ge.solve(Mm4, 1.0, a0); got.append(float(np.percentile(np.where(np.isfinite(lg), lg, 0.0), 50)))
        ck("K6", "EUC4 Part B reproduced: N = 316, median log M_gas 13.44 / 13.37 (r_c 30), 13.84 / 13.77 (r_c 100), +- 0.01",
           "N = %d, %.2f / %.2f, %.2f / %.2f" % (len(wide4), *got), len(wide4) == 316 and all(abs(g - x) <= 0.01 for g, x in zip(got, (13.44, 13.37, 13.84, 13.77))))
        ref8 = json.load(open(os.path.join(HERE, "..", "EUC8_wide_lens_residual_profile", "euc8_results.json")))["partA"]; e7 = []
        for nm, a0 in E.FOOT.items():
            Mx = solve_gas("G2", REW, ReW, nW, MsW, MtW["far"], 1.0, a0, ENG)
            e7.append(abs(float(np.median(Mx / MSUN)) / ref8["W theta_E >= 1.7|%s|far" % nm]["fam"]["2.0"]["M_300"][0] - 1.0))
        ck("K7", "EUC8 reproduced: median r^-2 mass inside 300 kpc for W (far, b_star 0), both footings (0.1 %)", "%.1e / %.1e" % (e7[0], e7[1]), max(e7) < 1.0e-3)

    if not all(v["ok"] for v in CK.values()):
        P("\nan instrument check failed before the stack; the map was not read at any target.  LANE WORD: NOT EVALUABLE / NOT EVALUABLE")
        RES["checks"] = CK; RES["checks_all_pass"] = False
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(3 if not MUT else 2)

    if a.checks_only:
        print("--checks-only: stopping before the map is read at any target", file=sys.stderr); sys.exit(0)

    # ---------------------------------------------------------------- measurement
    P("\n[measurement: compensated aperture photometry, value = target minus the mean of its covered offsets]")
    posS = [(radec[r["id"]][0], radec[r["id"]][1] + SHIFT) for r in S]
    okS, rmsS, capS, f1S = measure_targets(YM, posS, "S")
    base = okS[:, 0]; med = float(np.median(rmsS[base, 0])); lo, hi = 0.5 * med, 2.0 * med
    P("  coverage: %d of %d S positions pass rules (i) and (ii); median pixel rms %.3e; rule (iii) window %.3e to %.3e" % (base.sum(), len(S), med, lo, hi))
    covS, validS, noffS, valS, nulS = values(okS, rmsS, capS, f1S, lo, hi)
    P("  S: lens position covered %d; with >= 12 covered offsets (valid) %d" % (covS[:, 0].sum(), validS.sum()))
    okL, rmsL, capL, f1L = measure_targets(YM, [(radec[r["id"]][0], radec[r["id"]][1] + SHIFT) for r in LL], "L")
    covL, validL, _, valL, nulL = values(okL, rmsL, capL, f1L, lo, hi)
    okC, rmsC, capC, f1C = measure_targets(YM, [(c[0], c[1] + SHIFT) for c in CL], "clusters")
    covC, validC, _, valC, nulC = values(okC, rmsC, capC, f1C, lo, hi)

    tE = E.arr(S, "tE"); zS = E.arr(S, "z"); lmS = E.arr(S, "lm"); gradeA = np.array([r["grade"] == "A" for r in S]); DAS = E.EUCLID.DA(zS)
    Wm = validS & (tE >= 1.7); idxW = np.where(Wm)[0]; NWv = int(Wm.sum())
    P("  W (theta_E >= 1.7 arcsec, valid): %d of %d on the whole sky (required >= 100)" % (NWv, len(Wall)))
    # map valid W back onto the whole-sky W arrays used by the model
    posW = {r["id"]: k for k, r in enumerate(Wall)}; kW = np.array([posW[S[i]["id"]] for i in idxW], int)
    # controls
    pool = [i for i in np.where(validS & (tE < 1.0))[0]]; used = np.zeros(len(S), bool); pairs = []
    pz, pl = zS[pool], lmS[pool]; pool = np.array(pool, int)
    for i in idxW:
        d = ((pz - zS[i]) / 0.05) ** 2 + ((pl - lmS[i]) / 0.1) ** 2; d = np.where(used[pool], np.inf, d)
        if not np.isfinite(d).any(): continue
        j = pool[int(np.argmin(d))]; used[j] = True; pairs.append((i, j))
    pairs = np.array(pairs, int)
    P("  controls: %d pairs; median |dz| %.3f, median |d log M*| %.3f; W medians z %.3f, log M* %.2f, theta_E %.2f\"; C medians z %.3f, log M* %.2f, theta_E %.2f\""
      % (len(pairs), np.median(np.abs(zS[pairs[:, 0]] - zS[pairs[:, 1]])), np.median(np.abs(lmS[pairs[:, 0]] - lmS[pairs[:, 1]])),
         np.median(zS[idxW]), np.median(lmS[idxW]), np.median(tE[idxW]), np.median(zS[pairs[:, 1]]), np.median(lmS[pairs[:, 1]]), np.median(tE[pairs[:, 1]])))

    # ---------------------------------------------------------------- model on the valid W lenses
    P("\n[model: gas law S needs, least hydrostatic pressure, beam, same estimator]")
    MW = Model(raW[kW], deW[kW], zW[kW], REW[kW], ReW[kW], nW[kW], MsW[kW])
    ENGv = engines(REW[kW], ReW[kW], nW[kW], MsW[kW]); Mtv = {c: MtW[c][kW] for c in CASES}
    PRED, INFO = {}, {}
    for nm, a0 in E.FOOT.items():
        for fam in FAMS:
            for case in CASES:
                for bs in BSTAR:
                    Mg = solve_gas(fam, REW[kW], ReW[kW], nW[kW], MsW[kW], Mtv[case], 10.0 ** bs, a0, ENGv)
                    cap, kT, ne = MW.run(fam, Mg, 10.0 ** bs, a0)
                    PRED[(nm, fam, case, bs)] = cap
                    INFO[(nm, fam, case, bs)] = dict(Mg_med=float(np.median(Mg / MSUN)), frac_zero=float(np.mean(Mg <= 0)), kT_med=float(np.nanmedian(kT)),
                                                     ne_med=float(np.nanmedian(np.where(Mg > 0, ne, np.nan))), stack=[float(x) for x in cap.mean(1)])
    for nm in E.FOOT:
        P("  %s footing (predicted stack in 1e-6 arcmin^2 at theta_d = 2.0 arcmin; median gas mass; median mass-weighted kT; median n_e at R_E)" % nm)
        for fam in FAMS:
            for case in CASES:
                P("    %-4s %-7s " % (fam, case) + " | ".join("b* %+.2f: %9.2f  %.2e Msun  %.2f keV  %.1e cm^-3" % (bs, 1e6 * INFO[(nm, fam, case, bs)]["stack"][0],
                  INFO[(nm, fam, case, bs)]["Mg_med"], INFO[(nm, fam, case, bs)]["kT_med"], INFO[(nm, fam, case, bs)]["ne_med"]) for bs in BSTAR))
    RES["model"] = {"%s|%s|%s|%+.2f" % k: v for k, v in INFO.items()}
    # cold-share reading
    CSR = {}
    for nm, a0 in E.FOOT.items():
        Mx = solve_gas("G2", REW[kW], ReW[kW], nW[kW], MsW[kW], Mtv["far"], 1.0, a0, ENGv)
        Mgas = np.maximum(Mx / SHARE - MsW[kW], 0.0); r3 = grid(300.0)[0]
        cap, kT, _ = MW.run("CS", Mgas, 1.0, a0, gx=G * Mx[:, None] * (r3 / RT)[None, :] / r3[None, :] ** 2)
        CSR[nm] = dict(stack=[float(x) for x in cap.mean(1)], Mx_med=float(np.median(Mx / MSUN)), Mb_req_med=float(np.median(Mx / SHARE / MSUN)),
                       Mgas_med=float(np.median(Mgas / MSUN)), frac_no_gas=float(np.mean(Mgas <= 0)), kT_med=float(np.nanmedian(kT)))

    if MUT == "inject":
        inj = PRED[("canonical", "B100", "far", 0.10)]
        for t in range(3): valS[idxW, :, t] += inj[t][:, None]
        P("\n[MUTATE inject] the B100 prediction (far, b_star +0.10, canonical) added to every W lens's value, both maps, each aperture")

    # ---------------------------------------------------------------- stacks, checks that need them
    P("\n[stacks, primary map, theta_d = 2.0 arcmin, in 1e-6 arcmin^2]")
    def st(vals, nuls, sel, m, t, seed, w=None):
        return stack(vals[sel, m, t], nuls[sel][:, :, m, t], seed, None if w is None else w[sel])
    sW = st(valS, nulS, idxW, 0, 0, 1)
    P("  W: N = %d, stack %+.3f, sigma %.3f (bootstrap %.3f, null stacks %.3f)" % (sW["N"], 1e6 * sW["mean"], 1e6 * sW["sigma"], 1e6 * sW["sig_boot"], 1e6 * sW["sig_null"]))
    selC = np.where(validC)[0]; sC = stack(valC[selC, 0, 0], nulC[selC][:, :, 0, 0], 2)
    zc = sC["mean"] / sC["sigma"] if sC["N"] else float("nan")
    ck("K8", "eRASS1 clusters (M500 >= 2e14, 0.1 <= z <= 0.6, covered, N >= 20): stack positive at >= 5 sigma",
       "N = %d, stack %+.2f +- %.2f (1e-6 arcmin^2), %.1f sigma" % (sC["N"], 1e6 * sC["mean"], 1e6 * sC["sigma"], zc), sC["N"] >= 20 and zc >= 5.0)
    ns = np.array(sW["nulls"]); k9a = abs(ns.mean()) <= 3.0 * sW["sigma"] / 4.0; k9b = np.max(np.abs(ns)) <= 3.5 * sW["sigma"]
    ck("K9", "the 16 null stacks of W: mean within 3 sigma / 4 of zero, none beyond 3.5 sigma",
       "mean %+.3f, largest %.3f, sigma %.3f (1e-6 arcmin^2)" % (1e6 * ns.mean(), 1e6 * np.max(np.abs(ns)), 1e6 * sW["sigma"]), k9a and k9b)
    RES["checks"] = CK; allok = all(v["ok"] for v in CK.values())
    need_ck = ["K1", "K2", "K3", "K4", "K5", "K8", "K9"] + ([] if MUT else ["K6", "K7"])
    allok = allok and all(k in CK for k in need_ck)

    # ---------------------------------------------------------------- Part G
    P("\n[Part G: family words in the least demanding setting (far source, b_star = +0.10); units 1e-6 arcmin^2]")
    def part_g(sel_local, m, t, seed, show):
        """sel_local indexes the valid W lenses (0..NWv-1)."""
        s = stack(valS[idxW[sel_local], m, t], nulS[idxW[sel_local]][:, :, m, t], seed); out = dict(N=s["N"], meas=s["mean"], sigma=s["sigma"], fam={}, word={})
        keep = np.isfinite(valS[idxW[sel_local], m, t])
        for nm in E.FOOT:
            fw = {}
            for fam in FAMS:
                pmin = float(PRED[(nm, fam, "far", 0.10)][t][sel_local][keep].mean()) if keep.any() else float("nan")
                fw[fam] = fam_word(s["mean"], s["sigma"], pmin)
                out["fam"]["%s|%s" % (nm, fam)] = dict(pred_min=pmin, word=fw[fam], f_T=(s["mean"] + 2.0 * s["sigma"]) / pmin if pmin > 0 else float("nan"),
                                                       z_excl=(pmin - s["mean"]) / s["sigma"] if s["sigma"] > 0 else float("nan"))
                if show: P("    %-9s %-4s pred_min %9.2f   measured %+7.2f +- %.2f   (pred - meas) / sigma = %6.1f   f_T = %.3f   -> %s"
                           % (nm, fam, 1e6 * pmin, 1e6 * s["mean"], 1e6 * s["sigma"], out["fam"]["%s|%s" % (nm, fam)]["z_excl"], out["fam"]["%s|%s" % (nm, fam)]["f_T"], fw[fam]))
            out["word"][nm] = lane_word(fw, s["N"], allok)
        return out
    allW = np.arange(NWv)
    G0 = part_g(allW, 0, 0, 10, True)
    BR = {"CIB-deprojected map": part_g(allW, 1, 0, 11, False), "theta_d 1.5 arcmin": part_g(allW, 0, 1, 12, False), "theta_d 3.0 arcmin": part_g(allW, 0, 2, 13, False),
          "grade A only": part_g(np.where(gradeA[idxW])[0], 0, 0, 14, False), "z_l <= 0.6 only": part_g(np.where(zS[idxW] <= 0.6)[0], 0, 0, 15, False)}
    P("  brackets (lane word per footing; measured +- sigma; pred_min B30 / B100 / G2 canonical):")
    for k, b in BR.items():
        P("    %-22s N = %3d  %+7.2f +- %.2f   %8.2f / %8.2f / %8.2f   %s / %s" % (k, b["N"], 1e6 * b["meas"], 1e6 * b["sigma"],
          *[1e6 * b["fam"]["canonical|%s" % f]["pred_min"] for f in FAMS], b["word"]["canonical"], b["word"]["alt"]))
    WORD = {}
    for nm in E.FOOT:
        moved = [k for k, b in BR.items() if b["word"][nm] != G0["word"][nm]]
        WORD[nm] = G0["word"][nm] + (" [BRACKET-DEPENDENT: %s]" % ", ".join(moved) if moved and G0["word"][nm] != "NOT EVALUABLE" else "")
    P("  LANE WORD (Part G): %s / %s" % (WORD["canonical"], WORD["alt"]))
    RES["partG"] = dict(primary=G0, brackets=BR, word=WORD)

    # ---------------------------------------------------------------- Part C
    P("\n[Part C: wide lenses against matched controls]")
    def part_c(m, seed):
        D = valS[pairs[:, 0], m, 0] - valS[pairs[:, 1], m, 0]; D = D[np.isfinite(D)]; N = len(D)
        if N < 100: return dict(N=N, word="NOT EVALUABLE", mean=float("nan"), lo=float("nan"), hi=float("nan"))
        rng = np.random.default_rng(E.SEED); bs = D[rng.integers(0, N, (NBOOT, N))].mean(1)
        lo_, hi_ = float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
        return dict(N=N, mean=float(D.mean()), lo=lo_, hi=hi_, word="WIDE LENSES HOLD MORE GAS PRESSURE" if lo_ > 0 else "NO EXCESS DETECTED")
    C0, C1 = part_c(0, 20), part_c(1, 21)
    wc = C0["word"] + (" [BRACKET-DEPENDENT: CIB-deprojected map]" if C1["word"] != C0["word"] and C0["word"] != "NOT EVALUABLE" else "")
    if not allok: wc = "NOT EVALUABLE"
    P("  primary map: N = %d pairs, mean difference %+.3f [%+.3f, %+.3f] x 1e-6 arcmin^2 -> %s" % (C0["N"], 1e6 * C0["mean"], 1e6 * C0["lo"], 1e6 * C0["hi"], C0["word"]))
    P("  CIB-deprojected map: N = %d pairs, mean difference %+.3f [%+.3f, %+.3f] x 1e-6 arcmin^2 -> %s" % (C1["N"], 1e6 * C1["mean"], 1e6 * C1["lo"], 1e6 * C1["hi"], C1["word"]))
    P("  LANE WORD (Part C): %s" % wc)
    RES["partC"] = dict(primary=C0, cib=C1, word=wc)

    # ---------------------------------------------------------------- Part D
    P("\n[Part D: what the stack measures (no word).  Y in 1e-6 arcmin^2; Y D_A^2 in 1e-8 Mpc^2; int P_e dV = N_e kT in 1e52 J]")
    conv = ARCMIN ** 2 * DAS ** 2                      # arcmin^2 -> m^2, per lens
    classes = (("W theta_E >= 1.7", idxW), ("C controls", pairs[:, 1] if len(pairs) else np.array([], int)), ("1.3 - 1.7", np.where(validS & (tE >= 1.3) & (tE < 1.7))[0]),
               ("1.0 - 1.3", np.where(validS & (tE >= 1.0) & (tE < 1.3))[0]), ("below 1.0", np.where(validS & (tE < 1.0))[0]), ("all valid S", np.where(validS)[0]))
    PD = {}
    P("  %-18s %5s  %18s  %18s  %20s  %22s   gas mass at kT = 0.5 / 1 / 2 keV [1e12 Msun] (2-sigma upper limit at 1 keV; in mean M*)" % ("class", "N", "Y (primary)", "Y (CIB-deproj.)", "Y D_A^2", "N_e kT"))
    for j, (cn, sel) in enumerate(classes):
        if len(sel) == 0: continue
        s0 = st(valS, nulS, sel, 0, 0, 30 + j); s1 = st(valS, nulS, sel, 1, 0, 40 + j); sE = st(valS, nulS, sel, 0, 0, 50 + j, conv)
        Ee, sEe = sE["mean"] / KSZ, sE["sigma"] / KSZ; mst = float(np.mean(10.0 ** lmS[sel])); gm = [Ee * MUE * MP / (k * KEV) / MSUN for k in (0.5, 1.0, 2.0)]
        up = (Ee + 2.0 * sEe) * MUE * MP / KEV / MSUN
        PD[cn] = dict(N=s0["N"], Y=s0["mean"], sY=s0["sigma"], Y_cib=s1["mean"], sY_cib=s1["sigma"], YDA2_Mpc2=sE["mean"] / MPC ** 2, sYDA2_Mpc2=sE["sigma"] / MPC ** 2,
                      NekT_J=Ee, sNekT_J=sEe, Mgas_Msun_at_keV={"0.5": gm[0], "1": gm[1], "2": gm[2]}, Mgas_2sig_upper_1keV=up, mean_Mstar=mst)
        P("  %-18s %5d  %+8.3f +- %6.3f  %+8.3f +- %6.3f  %+9.3f +- %7.3f  %+10.3f +- %8.3f   %+.2f / %+.2f / %+.2f  (< %.2f; %.1f M*)"
          % (cn, s0["N"], 1e6 * s0["mean"], 1e6 * s0["sigma"], 1e6 * s1["mean"], 1e6 * s1["sigma"], 1e8 * sE["mean"] / MPC ** 2, 1e8 * sE["sigma"] / MPC ** 2,
             Ee / 1e52, sEe / 1e52, gm[0] / 1e12, gm[1] / 1e12, gm[2] / 1e12, up / 1e12, up / mst))
    selL = np.where(validL)[0]
    if len(selL):
        sL = stack(valL[selL, 0, 0], nulL[selL][:, :, 0, 0], 60); sL1 = stack(valL[selL, 1, 0], nulL[selL][:, :, 1, 0], 61)
        PD["L flagged large systems"] = dict(N=sL["N"], Y=sL["mean"], sY=sL["sigma"], Y_cib=sL1["mean"], sY_cib=sL1["sigma"])
        P("  %-18s %5d  %+8.3f +- %6.3f  %+8.3f +- %6.3f" % ("L flagged large", sL["N"], 1e6 * sL["mean"], 1e6 * sL["sigma"], 1e6 * sL1["mean"], 1e6 * sL1["sigma"]))
    P("  W at the three apertures (primary map): " + "; ".join("%.1f arcmin: %+.3f +- %.3f" % (thd, 1e6 * st(valS, nulS, idxW, 0, t, 70 + t)["mean"], 1e6 * st(valS, nulS, idxW, 0, t, 70 + t)["sigma"]) for t, thd in enumerate(THD)))
    P("  cold-share reading (EUC8's r^-2 component as cold dark energy; baryons = M_X / %.2f; gas = baryons - stars, B100 shape to 300 kpc, hydrostatic, zero edge pressure):" % SHARE)
    for nm in E.FOOT:
        c = CSR[nm]; gap = (sW["mean"] - c["stack"][0]) / sW["sigma"]
        P("    %-9s median M_X %.2e, baryons required %.2e, gas %.2e Msun (%.0f %% of lenses need none), kT %.2f keV; predicted stack %.4f against sigma %.3f (1e-6 arcmin^2); measured minus predicted = %+.1f sigma"
          % (nm, c["Mx_med"], c["Mb_req_med"], c["Mgas_med"], 100 * c["frac_no_gas"], c["kT_med"], 1e6 * c["stack"][0], 1e6 * sW["sigma"], gap))
        c["measured_minus_predicted_in_sigma"] = float(gap)
    RES["partD"] = dict(classes=PD, cold_share=CSR)
    RES["samples"] = dict(S=len(S), S_valid=int(validS.sum()), W_whole_sky=len(Wall), W_valid=NWv, pairs=int(len(pairs)), L_valid=int(validL.sum()), clusters_valid=int(validC.sum()),
                          rms_median=med)
    RES["stack_W"] = sW; RES["checks_all_pass"] = bool(allok)

    # ---------------------------------------------------------------- twins
    if MUT:
        if MUT == "inject":
            ok = all(G0["fam"]["%s|B100" % nm]["word"] == "ALLOWED" for nm in E.FOOT); msg = "B100 reads %s / %s" % tuple(G0["fam"]["%s|B100" % nm]["word"] for nm in E.FOOT)
        elif MUT == "shift":
            ok = not CK["K8"]["ok"]; msg = "K8 %s" % ("FAILS" if ok else "still passes")
        elif MUT == "newton":
            ref = json.load(open(os.path.join(HERE, "esz1_results.json")))["partG"]["primary"]["fam"]
            now = [G0["fam"]["%s|B100" % nm]["pred_min"] for nm in ("canonical", "alt")]; was = [ref["%s|B100" % nm]["pred_min"] for nm in ("canonical", "alt")]
            ok = all(x > y for x, y in zip(now, was)); msg = "pred_min of B100 %.3e / %.3e against %.3e / %.3e arcmin^2" % (now[0], now[1], was[0], was[1])
        else: ok, msg = False, "unknown twin"
        P("\n[MUTATE %s] %s -> %s" % (MUT, msg, "BITES (exit 1)" if ok else "DOES NOT BITE (exit 2)"))
        RES["mutate_bites"] = bool(ok)
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if ok else 2)

    with open(os.path.join(HERE, "esz1_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["unique_identifier", "grade", "z_l", "theta_E_arcsec", "log_Mstar", "valid", "n_offsets", "pixel_rms", "is_W", "control_of",
                    "value_2arcmin_primary", "value_2arcmin_cib", "pred_min_B30_canonical", "pred_min_B100_canonical", "pred_min_G2_canonical",
                    "pred_min_B30_alt", "pred_min_B100_alt", "pred_min_G2_alt"])
        ctl = {int(j): S[int(i)]["id"] for i, j in pairs}; loc = {int(i): k for k, i in enumerate(idxW)}
        for i, r in enumerate(S):
            pr = ["%.4e" % PRED[(nm, fam, "far", 0.10)][0][loc[i]] if i in loc else "" for nm in ("canonical", "alt") for fam in FAMS]
            w.writerow([r["id"], r["grade"], "%.4f" % zS[i], "%.4f" % tE[i], "%.4f" % lmS[i], int(validS[i]), int(noffS[i]), "%.4e" % rmsS[i, 0] if np.isfinite(rmsS[i, 0]) else "",
                        int(i in loc), ctl.get(i, ""), "%.4e" % valS[i, 0, 0] if np.isfinite(valS[i, 0, 0]) else "", "%.4e" % valS[i, 1, 0] if np.isfinite(valS[i, 1, 0]) else ""] + pr)
    P("\nchecks all pass: %s" % allok)
    print("run time %.0f s" % (time.time() - t0), file=sys.stderr)
    json.dump(RES, open(os.path.join(HERE, "esz1_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "esz1.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
