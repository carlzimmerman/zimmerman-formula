#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""hunt_lib.py -- shared loaders and kernel for the second-law hunt (predictions_2026/SECOND_LAW_HUNT_2026.md).
Both a_0 footings everywhere; Route A kernel; SPARC and Brouwer+2021 loaders lifted verbatim from the committed
scripts they come from (prep_2026/rar_origin_2026/rar_origin_detector_2026.py; condensate_pincer_2026/*)."""
import os, math, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "real_research", "data")
G = 6.674e-11; c_light = 2.99792458e8; kpc = 3.0857e19; Mpc = 3.0857e22; Msun = 1.989e30
KMS2_KPC = 1e6/kpc; h = 0.674; H0 = 100*h*1e3/Mpc
OM_B = 0.02237/h**2; OM_DM = 0.1200/h**2; OM_M = OM_B + OM_DM; OM_L = 1 - OM_M
rho_crit = 3*H0**2/(8*math.pi*G)
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
UPS_D, UPS_B = 0.5, 0.7
def nu(y):
    y = np.maximum(np.asarray(y, dtype=float), 1e-12); return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_s(y):
    y = max(float(y), 1e-12); return 1.0/(1.0 - math.exp(-math.sqrt(y)))
def read_master():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----"))
    rows = {}
    for line in lines[last+1:]:
        f = line.split()
        if len(f) < 18: continue
        try:
            rows[f[0]] = dict(T=int(f[1]), D=float(f[2]), eD=float(f[3]), inc=float(f[5]), einc=float(f[6]),
                              L36=float(f[7]), eL36=float(f[8]), Reff=float(f[9]), SBeff=float(f[10]),
                              Rdisk=float(f[11]), SBdisk=float(f[12]), MHI=float(f[13]), RHI=float(f[14]),
                              Vflat=float(f[15]), eVflat=float(f[16]), Q=int(f[17]))
        except ValueError: continue
    return rows
def load_sparc(qmax=2, incmin=30, npts=6, ups_d=UPS_D, ups_b=UPS_B):
    master = read_master(); gals = []
    for f in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
        name = os.path.basename(f).replace("_rotmod.dat", "")
        if name not in master: continue
        m = master[name]
        if m["Q"] > qmax or m["inc"] < incmin: continue
        d = np.loadtxt(f); d = d[d[:, 1] > 0]
        if len(d) < npts: continue
        r, vobs, ev, vg, vd, vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
        sbd, sbb = d[:, 6], d[:, 7]
        gbar = (vg*np.abs(vg) + ups_d*vd**2 + ups_b*vb**2)/r*KMS2_KPC
        gobs = vobs**2/r*KMS2_KPC
        good = gbar > 0
        Mb = ups_d*m["L36"]*1e9 + 1.33*m["MHI"]*1e9
        gals.append(dict(name=name, r=r[good], vobs=vobs[good], ev=ev[good], vg=vg[good], vd=vd[good],
                         vb=vb[good], sbd=sbd[good], sbb=sbb[good], gbar=gbar[good], gobs=gobs[good], Mb=Mb, **m))
    return gals
# ---------------------------------------------------------------- Brouwer+ 2021 KiDS-1000
B = os.path.join(DATA, "lensing_rar", "brouwer2021_rar")
PC_PER_M = 3.086e16; G_PC = 4.52e-30; CONV = 4*G_PC*PC_PER_M
def load_rar(fname):
    """RAR files: col0 = g_bar (m/s^2), returns (g_bar, g_obs, err) with the bias correction applied."""
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    return d[:, 0], CONV*d[:, 1]/d[:, 4], CONV*d[:, 3]/d[:, 4]
def load_esd(fname):
    """Rotation-curve files: col0 = projected R (Mpc), returns (R_Mpc, ESD, err) bias-corrected, Msun/pc^2."""
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    return d[:, 0], d[:, 1]/d[:, 4], d[:, 3]/d[:, 4]
def load_cov(fname, n):
    """Brouwer covariance files.  UNBINNED (n=15): the flat order is (i,j) and a plain reshape is correct.
    BINNED (n=60, 4 observable bins x 15 acceleration bins): the flat order is (m,n,i,j), so the 60x60 matrix is
    reshape(4,4,15,15).transpose(0,2,1,3) -- a plain reshape(60,60) is NOT positive definite and gives negative chi2.
    Verified here at load time: the returned matrix must be symmetric positive definite."""
    d = np.genfromtxt(os.path.join(B, fname), comments="#"); v = (d[:, 4]/d[:, 6])*CONV*CONV
    nb = len(np.unique(d[:, 0])); npb = n//nb
    if nb*npb != n: raise ValueError(f"{fname}: {nb} observable bins x {npb} rows != {n}")
    C = v.reshape(n, n) if nb == 1 else v.reshape(nb, nb, npb, npb).transpose(0, 2, 1, 3).reshape(n, n)
    ev = np.linalg.eigvalsh((C + C.T)/2)
    if ev.min() <= 0:
        raise ValueError(f"{fname}: covariance not positive definite (min eig {ev.min():.3e}) -- ordering wrong")
    return C
def load_cov_esd(fname, n):
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    return (d[:, 4]/d[:, 6]).reshape(n, n)
def esd_to_gobs(R_Mpc, ESD):
    """B21 eq 23: v_c^2 = 4 G ESD R  ->  g_obs = v_c^2/R = 4 G ESD (units: G_PC pc^3/(Msun s^2), ESD Msun/pc^2)"""
    return 4*G_PC*ESD*PC_PER_M*np.ones_like(R_Mpc)*1.0
class Check:
    def __init__(self): self.n = 0; self.fails = []
    def __call__(self, name, ok, detail=""):
        self.n += 1; print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
        if not ok: self.fails.append(name)
    def done(self):
        print(f"\nRESULT: {self.n} checks, {len(self.fails)} FAIL" + (f" -> {self.fails}" if self.fails else "") + f"   rc={1 if self.fails else 0}", flush=True)
        return 1 if self.fails else 0
def P(*a): print(*a, flush=True)
def info(s): print("  " + s, flush=True)
def fit_loglog(x, y, w=None):
    lx, ly = np.log10(x), np.log10(y); A = np.vstack([lx, np.ones_like(lx)]).T
    if w is None: s, b = np.linalg.lstsq(A, ly, rcond=None)[0]
    else:
        W = np.diag(w); s, b = np.linalg.solve(A.T @ W @ A, A.T @ W @ ly)
    return s, b, (ly - (s*lx + b)).std()
# ---------------------------------------------------------------- ALFALFA (hunt items 31, 32)
# Fetched this session from the VizieR CfA mirror into real_research/data/:
#   alfalfa_a100_haynes2018.tsv        J/ApJ/861/49  table2   -- ALFALFA alpha.100, 31502 HI sources (W50, M_HI, D, SNR, rms)
#   alfalfa_sdss_durbala2020_t1/2.tsv  J/AJ/160/271  table1/2 -- ALFALFA-SDSS: SDSS r-band axis ratio b/a and stellar masses
#   alfalfa_huds_leisman2017.tsv       J/ApJ/842/133 table1   -- 115 HI-bearing ultra-diffuse ALFALFA galaxies ("almost darks")
def vizier_tsv(fname):
    """VizieR ASU-TSV: '#' comment block, then header / units / dashes / rows.  Returns a list of dicts of strings."""
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, fname), encoding="latin-1")
            if l.strip() and not l.startswith("#")]
    hdr = [h.strip() for h in rows[0]]
    return [{hdr[i]: (r[i].strip() if i < len(r) else "") for i in range(len(hdr))} for r in rows[3:]]
def _f(v):
    try: return float(v)
    except Exception: return float("nan")
def inclination_from_ba(ba, q0=0.2):
    """Hubble's formula, intrinsic axis ratio q0 = 0.2.  Returns inclination in DEGREES (nan where b/a missing)."""
    ba = np.asarray(ba, dtype=float); q = np.clip(ba, q0 + 1e-6, 1.0)
    return np.degrees(np.arcsin(np.sqrt(np.clip((1 - q**2)/(1 - q0**2), 0.0, 1.0))))
def load_alfalfa():
    """alpha.100 merged with the ALFALFA-SDSS value-added catalogue.  Arrays, one entry per alpha.100 source."""
    a = vizier_tsv("alfalfa_a100_haynes2018.tsv")
    t1 = {r["AGC"].strip(): r for r in vizier_tsv("alfalfa_sdss_durbala2020_t1.tsv")}
    t2 = {r["AGC"].strip(): r for r in vizier_tsv("alfalfa_sdss_durbala2020_t2.tsv")}
    g = [r["AGC"].strip() for r in a]
    col = lambda k: np.array([_f(r[k]) for r in a])
    d = dict(agc=np.array(g), W50=col("W50"), eW50=col("e_W50"), W20=col("W20"), flux=col("HIflux"),
             eflux=col("e_HIflux"), snr=col("SNR"), rms=col("rms"), dist=col("Dist"), edist=col("e_Dist"),
             logMHI=col("logMHI"), elogMHI=col("e_logMHI"), code=col("HI"))
    d["ba"]    = np.array([_f(t1[k]["b/a"])    if k in t1 else np.nan for k in g])
    d["eba"]   = np.array([_f(t1[k]["e_b/a"])  if k in t1 else np.nan for k in g])
    d["pflag"] = np.array([_f(t1[k]["Flag"])   if k in t1 else np.nan for k in g])
    d["logMsM"] = np.array([_f(t2[k]["logMsM"]) if k in t2 else np.nan for k in g])
    d["logMsT"] = np.array([_f(t2[k]["logMsT"]) if k in t2 else np.nan for k in g])
    d["inc"] = inclination_from_ba(d["ba"])
    return d
def load_huds():
    """Leisman+2017 HI-bearing ultra-diffuse ALFALFA galaxies, merged with the ALFALFA-SDSS b/a and M_star."""
    h = vizier_tsv("alfalfa_huds_leisman2017.tsv")
    t1 = {r["AGC"].strip(): r for r in vizier_tsv("alfalfa_sdss_durbala2020_t1.tsv")}
    t2 = {r["AGC"].strip(): r for r in vizier_tsv("alfalfa_sdss_durbala2020_t2.tsv")}
    g = [r["AGC"].strip() for r in h]
    col = lambda k: np.array([_f(r[k]) for r in h])
    d = dict(agc=np.array(g), cz=col("cz"), W50=col("W50"), eW50=col("e_W50"), flux=col("SdV"),
             dist=col("Dist"), logMHI=col("logMHI"), elogMHI=col("e_logMHI"), mug0=col("mug0"),
             rh=col("rh"), gMAG=col("gMAG"), gr=col("g-r"),
             sset=np.array([r["Set"].strip() for r in h]))
    d["ba"]     = np.array([_f(t1[k]["b/a"])    if k in t1 else np.nan for k in g])
    d["pflag"]  = np.array([_f(t1[k]["Flag"])   if k in t1 else np.nan for k in g])
    d["logMsM"] = np.array([_f(t2[k]["logMsM"]) if k in t2 else np.nan for k in g])
    d["logMsT"] = np.array([_f(t2[k]["logMsT"]) if k in t2 else np.nan for k in g])
    d["inc"] = inclination_from_ba(d["ba"])
    return d
