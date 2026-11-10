#!/usr/bin/env python3
"""KO3F: power forecast for a spectroscopic host veto on KiDS lenses. A forecast, not a graded lane: no label.

Question: if KO1's host veto is redone with DESI DR1 redshifts where they exist, how small does the error on the late-type
(disc) outer amplitude get, at the frozen veto radius and at the widened ones that remove the veto's edge effect?

Reads NO lensing signal. cfg110_perlens's WG is never accessed; only the pair weights WW and the law's model cells are used.
From KO1's result file only the published ERRORS are read (index 1 of each [amplitude, error] pair).

Forecast: sigma = c / sqrt(I),  I(mask) = sum over the four outer bins k of (sum_l WW_lk M_lk)^2 / sum_l WW_lk  (M = law cell),
with c calibrated per footing on the errors KO1 published for fourteen samples that are rebuilt here.

Host of lens l (KO1's rule): pool object j != l, log M*_j >= log M*_l + 0.3, projected d <= F R_h,l, and
  photometric rule  |chi_j - chi_l| < 230 Mpc;
  hybrid rule       if l and j both have a good DESI redshift, c |z_j - z_l| / (1 + z_l) < V; otherwise the photometric rule.
Good DESI redshift (CFG316's D1): ZWARN == 0, DELTACHI2 > 40, SPECTYPE GALAXY, COADD_FIBERSTATUS == 0; match radius 1 arcsec.

Inputs, all on disk before this script was written (nothing downloaded): the staged KO1 inputs under real_research/data/lensing_rar
and DESI DR1 BGS_BRIGHT_full_HPmapcut.dat.fits under ../_external_data/desi_dr1_bgs (fetched 2026-10-03 by CFG316).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import json, time
import numpy as np
from scipy.spatial import cKDTree
import fitsio, healpy as hp
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
F_BGS = os.environ.get("KO3F_BGS", os.path.normpath(os.path.join(REPO, "..", "_external_data", "desi_dr1_bgs", "BGS_BRIGHT_full_HPmapcut.dat.fits")))
KO1 = os.path.join(HERE, "..", "KO1_kids_outer_points", "ko1_shape.json")
T0 = time.time(); LOG = open(os.path.join(HERE, "ko3f_forecast.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()

G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt")
O = [0, 1, 2, 3]
FS = (1.0, 1.3, 1.6); VS = (1000.0, 1500.0); WIN = 230.0; DM = 0.3
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def glaw(g, a0): return nu(g / a0) * g
def DC(z, n=2048):
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc
    return np.interp(z, zz, chi)
def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]

P("KO3F power forecast for a spectroscopic host veto. No lensing signal is read. No label is given.")
# ---------------------------------------------------------------- lenses, weights (no signal), model cells
ln = np.load(os.path.join(DATA, "lr_lenses.npz")); PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WWo = PL["WW"][:, O].copy(); EDGES = PL["gbar_edges"]                     # PL["WG"] is never read
f30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"]
NL = len(ln["ra"]); typ = ln["typ"]; zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
LATE, EARLY, ALL = typ == 0, typ == 1, np.ones(NL, bool)
XG, WGL = np.polynomial.legendre.leggauss(24); R3 = (3.0 * Mpc) ** 2
LAW = {}
for ft in FOOT:
    m_ = np.zeros((NL, len(O)))
    for c, k in enumerate(O):
        t_lo = G * Mg / EDGES[k + 1]; t_hi = np.minimum(G * Mg / EDGES[k], R3); ok = t_hi > t_lo
        t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            f = glaw(G * Mg[:, None] / t, A0[ft])
        m_[:, c] = np.where(ok, (f * WGL[None, :]).sum(1) / 2, 0.0)
    LAW[ft] = m_
def info(mask, ft):
    tw = WWo[mask].sum(0); tm = (WWo[mask] * LAW[ft][mask]).sum(0)
    return float(np.sum(np.where(tw > 0, tm * tm / np.where(tw > 0, tw, 1), 0.0)))
P(f"lenses {NL:,} (late {int(LATE.sum()):,}, early {int(EARLY.sum()):,})")

# ---------------------------------------------------------------- KiDS neighbour pool (KO1's)
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); b = HB[1].data
HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL[1].data
assert np.array_equal(np.asarray(b["ID"]), np.asarray(Lp["ID"]))
r = np.array(b["MAG_AUTO_CALIB"], dtype="f8"); zp = np.array(b["zphot_ANNz2"], dtype="f8")
logM = np.array(Lp["MASS_MED"], dtype="f8") + 0.15
ra = np.array(b["RAJ2000"], dtype="f8"); dec = np.array(b["DECJ2000"], dtype="f8")
del b, Lp; HB.close(); HL.close()
nb = (r < 20) & (zp >= 0.02) & (zp <= 0.8) & np.isfinite(logM) & (logM > 7)
inb = np.where(nb)[0]
xN = unitvec(ra[inb], dec[inb]); chiN = DC(zp[inb]); logMN = logM[inb]; rN = r[inb]; zN = zp[inb]
treeN = cKDTree(xN)
xL = unitvec(ln["ra"], ln["dec"])
dd, selfN = treeN.query(xL, k=1)
assert dd.max() < 1e-9 and np.allclose(zN[selfN], zl) and np.allclose(logMN[selfN], logMs), "lens rows not found in the pool"
P(f"pool {len(inb):,}; every lens found in it (max offset {dd.max():.1e})")

# ---------------------------------------------------------------- DESI DR1 BGS_BRIGHT
B = fitsio.FITS(F_BGS)[1].read(columns=["RA", "DEC", "Z_not4clus", "ZWARN", "DELTACHI2", "SPECTYPE", "COADD_FIBERSTATUS"])
dra, ddec, dz = B["RA"].astype("f8"), B["DEC"].astype("f8"), B["Z_not4clus"].astype("f8")
spt = np.char.strip(B["SPECTYPE"].astype(str))
good = (B["ZWARN"] == 0) & (B["DELTACHI2"] > 40) & (spt == "GALAXY") & (B["COADD_FIBERSTATUS"] == 0)
ND = len(dra); del B
cov256 = np.zeros(hp.nside2npix(256), bool); cov256[hp.ang2pix(256, dra, ddec, lonlat=True)] = True
near = (ddec > dec[inb].min() - 0.1) & (ddec < dec[inb].max() + 0.1)
xD = unitvec(dra[near], ddec[near]); zD = dz[near]; gD = good[near]
treeD = cKDTree(xD)
ch1 = 2 * np.sin(np.radians(1.0 / 3600) / 2)
d1, i1 = treeD.query(xN, k=1, distance_upper_bound=ch1)
mt = np.isfinite(d1); i1c = np.where(mt, i1, 0)
zsN = np.where(mt & gD[i1c], zD[i1c], np.nan)                               # good DESI redshift of each pool object
covN = cov256[hp.ang2pix(256, ra[inb], dec[inb], lonlat=True)]
covL = covN[selfN]; zsL = zsN[selfN]; hasL = np.isfinite(zsL)
bright = covN & (rN < 19.5)
P(f"DESI BGS_BRIGHT full: {ND:,} targets, good redshift {int(good.sum()):,}")
P(f"pool inside the DESI coverage (nside-256 occupancy) {int(covN.sum()):,} ({covN.mean():.3f}); matched to a target {int(mt.sum()):,}; "
  f"with a good redshift {int(np.isfinite(zsN).sum()):,}")
P(f"  pool r < 19.5 inside the coverage: {int(bright.sum()):,}; matched {mt[bright].mean():.3f}; good redshift {np.isfinite(zsN[bright]).mean():.3f}")
P(f"lenses inside the DESI coverage {int(covL.sum()):,} ({covL.mean():.3f}); with a good redshift {int(hasL.sum()):,} "
  f"(late {int((hasL & LATE).sum()):,}, early {int((hasL & EARLY).sum()):,})")
dzl = (zsL[hasL] - zl[hasL]) / (1 + zsL[hasL])
P(f"  lens photo-z against DESI: median {np.median(dzl):+.4f}, 1.4826 MAD {1.4826 * np.median(np.abs(dzl - np.median(dzl))):.4f}, "
  f"|dz|/(1+z) > 0.1: {np.mean(np.abs(dzl) > 0.1):.4f}")

# ---------------------------------------------------------------- host scan (one pass at the widest veto)
rh = np.minimum(3.0, np.sqrt(G * Mg / 1e-15) / Mpc)
th = rh * (1 + zl) / chil
chord1 = 2 * np.sin(th / 2); chordF = 2 * np.sin(max(FS) * th / 2)
keys = ["P", "U"] + [f"{t}{int(V)}" for V in VS for t in ("H", "S")]
CNT = {(k, F): np.zeros(NL, np.int32) for k in keys for F in FS}
CH = 400
for i0 in range(0, NL, CH):
    i1_ = min(i0 + CH, NL)
    lists = treeN.query_ball_point(xL[i0:i1_], r=chordF[i0:i1_])
    cnum = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(cnum.sum())
    if tot == 0: continue
    li = i0 + np.repeat(np.arange(len(cnum)), cnum)
    j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot)
    keep = (j != selfN[li]) & (logMN[j] >= logMs[li] + DM)
    li, j = li[keep], j[keep]
    sep = np.sqrt(((xL[li] - xN[j]) ** 2).sum(1)) / chord1[li]              # projected separation in units of R_h (chord ratio)
    phot = np.abs(chiN[j] - chil[li]) < WIN
    both = np.isfinite(zsL[li]) & np.isfinite(zsN[j])
    with np.errstate(invalid="ignore"):
        dv = c_SI / 1e3 * np.abs(zsN[j] - zsL[li]) / (1 + zsL[li])
    for F in FS:
        inF = sep <= F
        np.add.at(CNT[("P", F)], li[inF & phot], 1)
        np.add.at(CNT[("U", F)], li[inF & phot & ~both], 1)
        for V in VS:
            sin = both & (dv < V); hyb = np.where(both, sin, phot); v = int(V)
            np.add.at(CNT[(f"H{v}", F)], li[inF & hyb], 1)
            np.add.at(CNT[(f"S{v}", F)], li[inF & sin], 1)
HFp = {F: CNT[("P", F)] == 0 for F in FS}

# ---------------------------------------------------------------- checks and calibration on KO1's published errors
pub = json.load(open(KO1))["foot"]
P("\nCHECK the photometric host-free samples rebuilt here against KO1's (ko1_shape.json E7)")
ok_n = True
for F in FS:
    n_pub = pub["canonical"]["E7"][f"{F:.1f}"]["n"]; ok_n &= (int(HFp[F].sum()) == n_pub)
    P(f"  veto {F:.1f} R_h: {int(HFp[F].sum()):,} here, {n_pub:,} in KO1")
cache = os.environ.get("KO1_CACHE", "")
if cache and os.path.exists(cache):
    ck = np.load(cache)
    P(f"  per-lens flag against KO1's scan cache: {int((HFp[1.0] != (ck['c230_0.3'] == 0)).sum())} lenses differ; max |R_h difference| {float(np.max(np.abs(ck['rh'] - rh))):.1e} Mpc")
P(f"  [{'PASS' if ok_n else 'FAIL'}] sample sizes equal at all three radii")

HF = HFp[1.0]
CALS = [("W10 all", ALL, ("PH1", "W10 all", "outer")), ("hosted", ~HF, ("PH1", "hosted", "outer")),
        ("host-free all", HF, ("PH1", "host-free all", "outer")), ("host-free late", HF & LATE, ("PH1", "host-free late", "outer")),
        ("host-free early", HF & EARLY, ("PH1", "host-free early", "outer")), ("W30 all", f30, ("PH1", "W30 all", "outer")),
        ("W30 late", f30 & LATE, ("PH1", "W30 late", "outer")), ("W30 early", f30 & EARLY, ("PH1", "W30 early", "outer"))]
for F in (1.3, 1.6):
    CALS += [(f"host-free all, veto {F}", HFp[F], ("E7", f"{F:.1f}", "outer")), (f"host-free late, veto {F}", HFp[F] & LATE, ("E7", f"{F:.1f}", "late")),
             (f"host-free early, veto {F}", HFp[F] & EARLY, ("E7", f"{F:.1f}", "early"))]
res = {"lane": "KO3F", "kind": "forecast, no label, no lensing signal read", "calibration": {}, "rows": {}, "moves": {}}
CL, CE = {}, {}
for ft in FOOT:
    P(f"\nCALIBRATION, {ft}: c = published error x sqrt(I)")
    cs = {}
    for name, mk, (a, b_, c_) in CALS:
        s = float(pub[ft][a][b_][c_][1]); I = info(mk, ft); cs[name] = s * np.sqrt(I)
        P(f"  {name:28s} n {int(mk.sum()):7,}  published error {s:.3f}  c {cs[name]:.4e}")
    v = np.array(list(cs.values())); lt = np.array([cs[k] for k in cs if "late" in k]); et = np.array([cs[k] for k in cs if "early" in k])
    CL[ft] = (float(lt.min()), float(np.median(lt)), float(lt.max())); CE[ft] = float(np.median(et))
    res["calibration"][ft] = dict(c=cs, spread_all=float(v.max() / v.min()), c_late=CL[ft], c_early=CE[ft])
    P(f"  spread of c over all fourteen samples: max / min = {v.max() / v.min():.3f}; late samples {lt.min():.4e} to {lt.max():.4e}")
ok_c = all(res["calibration"][ft]["spread_all"] < 1.25 for ft in FOOT)
P(f"  [{'PASS' if ok_c else 'FAIL'}] one constant reproduces every published error to 25 % (so the errors are weight-limited and the forecast scaling is usable)")

# ---------------------------------------------------------------- the forecast table
def row(name, mk):
    out = dict(n=int(mk.sum()), n_late=int((mk & LATE).sum()), n_early=int((mk & EARLY).sum()))
    txt = f"  {name:66s} late {out['n_late']:6,}"
    for ft in FOOT:
        Il, Ie = info(mk & LATE, ft), info(mk & EARLY, ft)
        out[ft] = dict(sigma_late=[c / np.sqrt(Il) for c in CL[ft]] if Il > 0 else None, sigma_early=CE[ft] / np.sqrt(Ie) if Ie > 0 else None)
        sl = out[ft]["sigma_late"]
        txt += f"   {ft} sigma_late {sl[1]:.2f} ({sl[0]:.2f}-{sl[2]:.2f})" if sl else f"   {ft} n/a"
    txt += f"   early {out['n_early']:6,} sigma_early {out['canonical']['sigma_early']:.2f} / {out['alt']['sigma_early']:.2f}"
    res["rows"][name] = out; P(txt)
P("\nFORECAST: error on the outer-bin amplitude (units of the law). Late types first; early types canonical / alt.")
for F in FS:
    P(f" veto radius {F:.1f} R_h")
    row(f"F{F} photometric veto, all KiDS (KO1's own sample)", HFp[F])
    for V in VS:
        v = int(V); H = CNT[(f"H{v}", F)] == 0
        row(f"F{F} V{v} hybrid veto, all KiDS", H)
        row(f"F{F} V{v} hybrid veto, lenses with a DESI redshift only", H & hasL)
        row(f"F{F} V{v} UPPER BOUND: DESI lenses, no confirmed host, unresolved ignored", hasL & (CNT[(f"S{v}", F)] == 0))
        mv = dict(rescued=int((H & ~HFp[F]).sum()), rescued_late=int((H & ~HFp[F] & LATE).sum()),
                  lost=int((~H & HFp[F]).sum()), lost_late=int((~H & HFp[F] & LATE).sum()),
                  desi_lenses_with_confirmed_host=int((hasL & (CNT[(f"S{v}", F)] > 0)).sum()),
                  desi_lenses_with_unresolved_photometric_host=int((hasL & (CNT[("U", F)] > 0)).sum()))
        res["moves"][f"F{F}_V{v}"] = mv
        P(f"     V {v}: rescued by spectroscopy {mv['rescued']:,} (late {mv['rescued_late']:,}); lost to a spectroscopic host outside the photo window "
          f"{mv['lost']:,} (late {mv['lost_late']:,}); DESI lenses with a confirmed host {mv['desi_lenses_with_confirmed_host']:,}, "
          f"with an unresolved photometric host {mv['desi_lenses_with_unresolved_photometric_host']:,}")
res["counts"] = dict(NL=NL, pool=int(len(inb)), desi_targets=ND, desi_good=int(good.sum()), pool_in_cov=int(covN.sum()),
                     pool_bright_good_fraction=float(np.isfinite(zsN[bright]).mean()), lenses_in_cov=int(covL.sum()),
                     lenses_with_desi_z=int(hasL.sum()), lenses_with_desi_z_late=int((hasL & LATE).sum()))
res["checks"] = {"photometric sample sizes equal KO1's at 1.0, 1.3, 1.6 R_h": bool(ok_n), "one constant reproduces the published errors to 25 %": bool(ok_c)}
json.dump(res, open(os.path.join(HERE, "ko3f_forecast.json"), "w"), indent=1)
P("\nwrote ko3f_forecast.json, ko3f_forecast.out")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
