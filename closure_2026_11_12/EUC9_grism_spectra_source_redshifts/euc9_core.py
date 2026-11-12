#!/usr/bin/env python3
"""EUC9 core: the mirrored line-pair search in Euclid's co-added 1D red-grism spectra, and the dither test.

Frozen criteria: FROZEN_CRITERIA.md (commit bea4eacfa8), section 3.  The search (everything down to `inject`) was
written and tested on 31 field spectra (none from ECLIPSE) before the criteria were frozen and is unchanged since.
`dither_test` and `inject_dithers` implement AMENDMENT_A0.md (82cf65da28) A0.2; they were written after that
amendment was committed and before any lens or grade-X spectrum was opened.
"""
import math
import numpy as np
from scipy import sparse
from scipy.ndimage import maximum_filter1d
from scipy.special import erf

# ------------------------------------------------------------------ frozen numbers
W0, DW, NPIX = 11900.0, 13.4, 531            # the co-added spectra's common wavelength grid (Angstrom)
GSTEP = DW / 2.0                             # grid of line centres
DISP = DW / 0.3                              # Angstrom per arcsec along the dispersion (13.4 A per 0.3 arcsec pixel)
S_MIN, S_EXTRA = 30.0, 0.5                   # half-split range: 30 A to DISP * (theta_E + 0.5 arcsec)
SIG_PAIR = (12.0, 16.0, 20.0, 25.0)          # Gaussian sigma of each component (Angstrom)
SIG_SINGLE = (12.0, 16.0, 20.0, 25.0, 32.0, 40.0, 50.0, 65.0, 80.0, 100.0, 130.0)
RATIO = (0.45, 2.2)                          # blue / red line-flux ratio
NDITH_MIN = 3
COVER_MIN = 0.8
MEDWIN = 41                                  # running-median continuum window (pixels)
TIERS = (("TA", 3.5, 6.0, 9.0), ("TB", 5.0, 8.0, 16.0))      # name, each component S/N, combined S/N, pair-over-single dchi2
HA, O3B, O3A, HB, S2 = 6564.61, 5008.24, 4960.295, 4862.69, 6725.5
PARTNER_SN = 3.0

WL = W0 + DW * np.arange(NPIX)
CENT = np.arange(W0 + 4 * DW, WL[-1] - 4 * DW, GSTEP)
NC = len(CENT)

def template(cent, sig):
    """pixel-integrated unit-flux Gaussian(s): rows = centres, columns = pixels (per Angstrom)"""
    c = np.atleast_1d(cent)[:, None]
    a = (WL[None, :] + DW / 2 - c) / (sig * math.sqrt(2.0)); b = (WL[None, :] - DW / 2 - c) / (sig * math.sqrt(2.0))
    g = 0.5 * (erf(a) - erf(b)) / DW
    g[g < 1e-9 / DW] = 0.0
    return g

G = {s: sparse.csr_matrix(template(CENT, s)) for s in SIG_PAIR}
G2 = {s: G[s].multiply(G[s]).tocsr() for s in SIG_PAIR}
G1 = {s: sparse.csr_matrix(template(CENT, s)) for s in SIG_SINGLE}
G12 = {s: G1[s].multiply(G1[s]).tocsr() for s in SIG_SINGLE}
KMAX = int((DISP * (3.0 + S_EXTRA + 0.7)) / (GSTEP / 2.0)) + 1
_CROSS = {}
def cross(sig, k):
    if (sig, k) not in _CROSS:
        _CROSS[(sig, k)] = G[sig][:-k].multiply(G[sig][k:]).tocsr()
    return _CROSS[(sig, k)]

def prepare(d):
    """continuum-subtracted residual, rescaled error, good-pixel mask"""
    f = np.asarray(d["SIGNAL"], float); e = np.asarray(d["UNCERTAINTY"], float)
    m = np.asarray(d["MASK"]).astype(int); nd = np.asarray(d["NDITH"]).astype(int)
    if len(f) != NPIX or abs(float(d["WAVELENGTH"][0]) - W0) > 0.5 or abs(float(d["WAVELENGTH"][-1]) - WL[-1]) > 0.5:
        return None
    good = (m % 2 == 0) & (m < 64) & (e > 0) & np.isfinite(f) & np.isfinite(e) & (nd >= 1)
    if good.sum() < 100: return None
    cont = np.full(NPIX, np.nan); h = MEDWIN // 2
    idx = np.where(good)[0]
    for p in range(NPIX):
        lo, hi = np.searchsorted(idx, p - h), np.searchsorted(idx, p + h + 1)
        if hi - lo >= 10: cont[p] = np.median(f[idx[lo:hi]])
    good &= np.isfinite(cont)
    r = np.where(good, f - cont, 0.0)
    x = r[good] / e[good]
    k = max(1.0, 1.4826 * float(np.median(np.abs(x - np.median(x)))))
    e2 = np.where(good, e * k, np.inf)
    return dict(r=r, e=e2, good=good, nd=nd, k=k, cont=np.where(good, cont, 0.0))

def search(p, theta_E, sign=1.0, single_only=False):
    """best mirrored pair per tier (or None).  sign = -1 searches the sign-flipped residual (signal-free null)."""
    r = sign * p["r"]; iv = np.where(p["good"], 1.0 / p["e"] ** 2, 0.0); riv = r * iv
    gd = p["good"].astype(float)
    ndc = p["nd"][np.clip(np.rint((CENT - W0) / DW).astype(int), 0, NPIX - 1)]
    # single-line alternative: best dchi2 at each centre over all widths
    M1 = np.zeros(NC); S1 = np.zeros(NC); A1 = np.zeros(NC)
    for s in SIG_SINGLE:
        T = G1[s] @ riv; N = G12[s] @ iv
        d2 = np.where((N > 0) & (T > 0), T * T / np.where(N > 0, N, 1.0), 0.0)
        up = d2 > M1; M1 = np.where(up, d2, M1); S1 = np.where(up, s, S1); A1 = np.where(up, T / np.where(N > 0, N, 1.0), A1)
    if single_only:
        cov = (G1[16.0] @ gd) * DW
        ok = (cov >= COVER_MIN) & (ndc >= NDITH_MIN) & (S1 <= 40.0)
        out = {}
        for tn, each, comb, dchi in TIERS:
            j = int(np.argmax(np.where(ok, M1, 0.0)))
            out[tn] = dict(lam0=float(CENT[j]), s=0.0, sig=float(S1[j]), sn=float(math.sqrt(M1[j])), flux=float(A1[j])) if ok[j] and math.sqrt(M1[j]) >= comb else None
        return out
    kmin = int(math.ceil(S_MIN / (GSTEP / 2.0))); kmax = int(math.floor(DISP * (theta_E + S_EXTRA) / (GSTEP / 2.0)))
    best = {tn: None for tn, _, _, _ in TIERS}
    for sig in SIG_PAIR:
        T = G[sig] @ riv; N = G2[sig] @ iv; cov = (G[sig] @ gd) * DW
        okc = (cov >= COVER_MIN) & (ndc >= NDITH_MIN) & (N > 0)
        for k in range(kmin, min(kmax, KMAX) + 1):
            # blue centre j, red centre j + k; half-split s = k * GSTEP / 2
            C = cross(sig, k) @ iv
            Tb, Tr, Nb, Nr = T[:-k], T[k:], N[:-k], N[k:]
            det = Nb * Nr - C * C
            ok = okc[:-k] & okc[k:] & (det > 0)
            dd = np.where(ok, det, 1.0)
            ab = (Nr * Tb - C * Tr) / dd; ar = (Nb * Tr - C * Tb) / dd
            sb = ab / np.sqrt(np.where(ok, Nr / dd, 1.0)); sr = ar / np.sqrt(np.where(ok, Nb / dd, 1.0))
            d2 = ab * Tb + ar * Tr
            ok &= (ab > 0) & (ar > 0)
            ratio = np.where(ok, ab / np.where(ar > 0, ar, 1.0), 0.0)
            ok &= (ratio >= RATIO[0]) & (ratio <= RATIO[1])
            if not ok.any(): continue
            # best single line anywhere from 4 grid steps blueward of the blue centre to 4 redward of the red one
            size = k + 9
            ms = maximum_filter1d(M1, size=size, mode="constant", cval=0.0, origin=-(size // 2) + 4)[:NC - k]
            for tn, each, comb, dchi in TIERS:
                q = ok & (sb >= each) & (sr >= each) & (d2 >= comb * comb) & (d2 - ms >= dchi)
                if not q.any(): continue
                j = int(np.argmax(np.where(q, d2, 0.0)))
                if best[tn] is None or d2[j] > best[tn]["d2"]:
                    best[tn] = dict(d2=float(d2[j]), lam0=float(CENT[j] + k * GSTEP / 2.0), s=float(k * GSTEP / 2.0), sig=sig, k=k, j=j,
                                    flux_b=float(ab[j]), flux_r=float(ar[j]), sn_b=float(sb[j]), sn_r=float(sr[j]), ratio=float(ratio[j]),
                                    sn=float(math.sqrt(d2[j])), dchi=float(d2[j] - ms[j]))
    return best

def partner(p, pair, lam_mid, sign=1.0):
    """S/N and flux of a pair with the primary's split, width and flux ratio, centred at lam_mid"""
    if lam_mid - pair["s"] < WL[4] or lam_mid + pair["s"] > WL[-5]: return None
    iv = np.where(p["good"], 1.0 / p["e"] ** 2, 0.0)
    tb = template(lam_mid - pair["s"], pair["sig"])[0]; tr = template(lam_mid + pair["s"], pair["sig"])[0]
    fb = pair["ratio"] / (1.0 + pair["ratio"]); t = fb * tb + (1.0 - fb) * tr           # unit total flux
    if float(np.sum(t * p["good"]) * DW) < COVER_MIN: return None
    N = float(np.sum(t * t * iv))
    if N <= 0: return None
    a = float(np.sum(sign * p["r"] * t * iv)) / N
    return dict(flux=a, sn=a * math.sqrt(N))

def identify(p, pair, sign=1.0):
    """which line the primary pair is: O3 ([O III] 5008 with its 4960 partner), HA2 (H-alpha with a second line), HA1"""
    tot = pair["flux_b"] + pair["flux_r"]
    q = partner(p, pair, pair["lam0"] * O3A / O3B, sign)
    if q is not None and q["sn"] >= PARTNER_SN and 0.15 <= q["flux"] / tot <= 0.6:
        return "O3", pair["lam0"] / O3B - 1.0, ["OIII4960 %.1f" % q["sn"]]
    sup = []
    for nm, lam in (("SII", S2), ("OIII5008", O3B), ("Hbeta", HB)):
        q = partner(p, pair, pair["lam0"] * lam / HA, sign)
        if q is not None and q["sn"] >= PARTNER_SN: sup.append("%s %.1f" % (nm, q["sn"]))
    return ("HA2" if sup else "HA1"), pair["lam0"] / HA - 1.0, sup

def inject(d, lam0, s, sig, flux, ratio=1.0):
    """a copy of the raw spectrum with a mirrored pair (s > 0) or a single line (s = 0) of total line flux `flux` added"""
    out = {k: np.array(v, copy=True) for k, v in d.items()}
    if s > 0:
        fb = ratio / (1.0 + ratio)
        add = flux * (fb * template(lam0 - s, sig)[0] + (1.0 - fb) * template(lam0 + s, sig)[0])
    else:
        add = flux * template(lam0, sig)[0]
    out["SIGNAL"] = np.asarray(out["SIGNAL"], float) + add
    return out

# ------------------------------------------------------------------ AMENDMENT A0.2: the dither test
D_MIN = 3.0
POS = ("RGS000", "RGS180")

def dither_test(raw, pair, sign=1.0):
    """is the blue component in one grism position and the red in the other?  None if it cannot be tested."""
    tb = template(pair["lam0"] - pair["s"], pair["sig"])[0]; tr = template(pair["lam0"] + pair["s"], pair["sig"])[0]
    out = {}
    for g in POS:
        Nbb = Nrr = Nbr = Tb = Tr = 0.0; used = 0
        for i in range(len(raw["DS"])):
            if str(raw["dpos"][i]).strip() != g: continue
            p = prepare(dict(WAVELENGTH=raw["WAVELENGTH"], SIGNAL=raw["DS"][i], UNCERTAINTY=np.sqrt(np.clip(np.asarray(raw["DV"][i], float), 0, None)),
                             MASK=raw["DM"][i], NDITH=np.ones(NPIX, int)))
            if p is None: continue
            if float(np.sum(tb * p["good"]) * DW) < COVER_MIN or float(np.sum(tr * p["good"]) * DW) < COVER_MIN: continue
            iv = np.where(p["good"], 1.0 / p["e"] ** 2, 0.0); r = sign * p["r"]
            Tb += float(np.sum(r * tb * iv)); Tr += float(np.sum(r * tr * iv))
            Nbb += float(np.sum(tb * tb * iv)); Nrr += float(np.sum(tr * tr * iv)); Nbr += float(np.sum(tb * tr * iv)); used += 1
        det = Nbb * Nrr - Nbr * Nbr
        if used == 0 or det <= 0: return None
        Fb = (Nrr * Tb - Nbr * Tr) / det; Fr = (Nbb * Tr - Nbr * Tb) / det
        out[g] = dict(A=Fr - Fb, var=(Nrr + Nbb + 2.0 * Nbr) / det, Fb=Fb, Fr=Fr, n=used)
    a0, a1 = out[POS[0]], out[POS[1]]
    stat = (a0["A"] - a1["A"]) / math.sqrt(a0["var"] + a1["var"])
    return dict(stat=float(stat), A000=float(a0["A"]), A180=float(a1["A"]), n000=a0["n"], n180=a1["n"],
                passes=bool(a0["A"] * a1["A"] < 0 and abs(stat) >= D_MIN))

def inject_dithers(raw, lam0, s, sig, flux, mirrored=True):
    """a copy of the raw arrays with a pair of total co-added line flux `flux` added to the co-add and to the dithers:
    mirrored = blue component in the RGS000 dithers and red in the RGS180 ones; otherwise a true doublet in every dither"""
    out = {k: np.array(v, copy=True) for k, v in raw.items()}
    tb = template(lam0 - s, sig)[0]; tr = template(lam0 + s, sig)[0]
    out["SIGNAL"] = np.asarray(out["SIGNAL"], float) + 0.5 * flux * (tb + tr)
    DS = np.asarray(out["DS"], float).copy()
    for i in range(len(DS)):
        g = str(raw["dpos"][i]).strip()
        if mirrored: DS[i] += flux * (tb if g == POS[0] else tr if g == POS[1] else 0.0)
        else: DS[i] += 0.5 * flux * (tb + tr)
    out["DS"] = DS
    return out
