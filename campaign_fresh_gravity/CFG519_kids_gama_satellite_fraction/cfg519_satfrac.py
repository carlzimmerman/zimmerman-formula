#!/usr/bin/env python3
"""CFG519: observed satellite (leakage) fraction and spectroscopic companion count of the KiDS isolated lenses (stack P, W = 10)
from the KiDS-bright x GAMA DR4 G3C v10 overlap (G09 / G12 / G15).  Criteria: FROZEN_CRITERIA.md (ff98baf04), committed alone first.

Pure data: no gravity model is evaluated; the a0 footings (canonical 9.3603e-11, alt 1.1312e-10 m/s^2; kappa = 1/2 FITTED) do not enter.
Inputs: ../_external_data/cfg502_work/cfg502_stage.npz (ISO / ALL lenses, WW, photometric companion counts),
        real_research/data/lensing_rar/KiDS_DR4_brightsample*.fits (pool), ../_external_data/cfg519_work/G3C*v10.csv (CFG471's logged fetch).
MUTATE (CFG519_MUTATE=1): M1 G3C redshifts shuffled within each field; M2 KiDS RA shifted +1 deg inside each field before matching.
Run: nice -n 10 python3 -u cfg519_satfrac.py ; CFG519_MUTATE=1 nice -n 10 python3 -u cfg519_satfrac.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import time, json, hashlib
import numpy as np
import pandas as pd
from astropy.io import fits
from scipy.spatial import cKDTree

MUT = os.environ.get("CFG519_MUTATE", "0") == "1"
MODE = os.environ.get("CFG519_MODE", "")
if MUT and MODE == "":              # run M1 and M2 separately, combine into *_MUTATE.out / *_MUTATE.json
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__)); outs = []; rc = 0; J = {}
    for m in ("M1", "M2"):
        e = dict(os.environ, CFG519_MODE=m)
        rc |= subprocess.call([sys.executable, "-u", os.path.abspath(__file__)], env=e)
        outs.append(open(os.path.join(here, f"cfg519_satfrac_MUTATE_{m}.tmp.out")).read())
        J[m] = json.load(open(os.path.join(here, f"cfg519_satfrac_results_MUTATE_{m}.tmp.json")))
        os.remove(os.path.join(here, f"cfg519_satfrac_MUTATE_{m}.tmp.out")); os.remove(os.path.join(here, f"cfg519_satfrac_results_MUTATE_{m}.tmp.json"))
    open(os.path.join(here, "cfg519_satfrac_MUTATE.out"), "w").write("\n\n".join(outs))
    json.dump(J, open(os.path.join(here, "cfg519_satfrac_results_MUTATE.json"), "w"), indent=1, default=float)
    sys.exit(rc)
M1, M2 = MUT and MODE == "M1", MUT and MODE == "M2"
TAG = f"_MUTATE_{MODE}.tmp" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D = os.path.join(REPO, "real_research", "data", "lensing_rar")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg519_work")
c_ms = 2.998e8; c_kms = 2.998e5; Mpc = 3.0857e22; H0 = 70 * 1e3 / Mpc
T0 = time.time(); LOG = []; CHK = {}; RES = {"mutate": MUT}


def say(s=""):
    print(s, flush=True); LOG.append(s)


def check(name, ok, msg, load=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=load, msg=msg)
    say(f"  [{'PASS' if ok else 'FAIL'}]{'' if load else ' (reported)'} {name}: {msg}")


def DC(z, n=4096):                       # the record's comoving distance (H0 = 70, Om = 0.3), Mpc
    zz = np.linspace(0, 0.7, n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_ms / H0) / Mpc
    return np.interp(z, zz, chi)


def unit(ra, dec):
    r, d = np.radians(ra), np.radians(dec)
    return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]


say(__doc__.split("Run:")[0].strip())
say(f"\nmode: {'MUTATE M1 (G3C redshifts shuffled within each field)' if M1 else ('MUTATE M2 (KiDS RA shifted +1 deg inside each field)' if M2 else 'MAIN')}")
say("a0 footings: irrelevant here (pure data); kappa = 1/2 is FITTED elsewhere; nothing here evaluates a gravity model.")

# ------------------------------------------------------------------ inputs
S = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
lra, ldec, lz, llm, ltyp, lchi = (S[k] for k in ("ra", "dec", "z", "logM", "typ", "chi"))
iso10, iso30 = S["iso10"], S["iso30"]; iso_idx = S["iso_idx"]
wl = S["WW"].sum(1)
NA = len(lra)
phot_meas = np.full(NA, np.nan); phot_meas[iso_idx] = S["cin"] - S["can"] * 0.25 / 20.0
say("\n== C1 / C2: staging and pool")
check("C1 ISO count and weights = staging", iso10.sum() == 181477 and np.array_equal(np.where(iso10)[0], iso_idx),
      f"ISO {int(iso10.sum()):,}, ALL {NA:,}, f30 {int(iso30.sum()):,}")

b = fits.open(os.path.join(D, "KiDS_DR4_brightsample.fits"))[1].data
L = fits.open(os.path.join(D, "KiDS_DR4_brightsample_LePhare.fits"))[1].data
r = np.array(b["MAG_AUTO_CALIB"], "f8"); z = np.array(b["zphot_ANNz2"], "f8"); masked = b["masked"]
logM = np.array(L["MASS_MED"], "f8") + 0.15
ur = np.array(L["MAG_ABS_u"] - L["MAG_ABS_r"], "f8")
ra = np.array(b["RAJ2000"], "f8"); dec = np.array(b["DECJ2000"], "f8")
pool = (r < 20) & (z > 0.1) & (z < 0.5) & (masked == 0) & np.isfinite(logM) & (logM > 7)
sel = pool & (logM < 11.0) & np.isfinite(ur)
ip = np.where(pool)[0]; il = np.where(sel)[0]
lpos = np.searchsorted(ip, il)                     # lens -> pool index
P_ra, P_dec, P_z, P_lm, P_r = ra[ip].copy(), dec[ip].copy(), z[ip], logM[ip], r[ip]
P_chi = DC(P_z)
del b, L, r, z, masked, logM, ur, ra, dec
c2 = (len(il) == NA) and np.array_equal(P_ra[lpos], lra) and np.array_equal(P_dec[lpos], ldec) and np.array_equal(P_z[lpos], lz) \
     and np.array_equal(P_lm[lpos], llm)
check("C2 rebuilt pool reproduces the staging lenses exactly", c2, f"pool {len(ip):,}; lens candidates {len(il):,}")

# ------------------------------------------------------------------ G3C
say("\n== C3: G3C files (CFG471's logged fetch, copied)")
SHA = {"G3CGalv10.csv": "051950e193e447ebf8bf7a9458c3ffe4ea368596b8042732ee933fc95f6ad9f8",
       "G3CFoFGroupv10.csv": "eb81594ad6994e3fb44d2ee7c2e4eac4a99e3c7c27750bbf620d9f103a5b96c7"}
got = {f: hashlib.sha256(open(os.path.join(WORK, f), "rb").read()).hexdigest() for f in SHA}
ok3 = all(got[f] == SHA[f] for f in SHA)
check("C3 SHA-256 of both G3C files = CFG471 FETCH_LOG", ok3, "; ".join(f"{f} {'ok' if got[f] == SHA[f] else 'MISMATCH'}" for f in SHA))
if not ok3:
    sys.exit(2)
g = pd.read_csv(os.path.join(WORK, "G3CGalv10.csv"))
G = pd.read_csv(os.path.join(WORK, "G3CFoFGroupv10.csv")).set_index("GroupID")
FIELDS = [(129.0, 141.0, -2.0, 3.0), (174.0, 186.0, -3.0, 2.0), (211.5, 223.5, -2.0, 3.0)]


def field_of(ra_, dec_):
    f = np.full(len(ra_), -1)
    for k, (a0, a1, d0, d1) in enumerate(FIELDS):
        f[(ra_ > a0) & (ra_ < a1) & (dec_ > d0) & (dec_ < d1)] = k
    return f


g_ra, g_dec, g_z = g.RA.values, g.Dec.values, g.Z.values.copy()
g_fld = field_of(g_ra, g_dec)
gkeep = g_fld >= 0
say(f"  G3CGal rows {len(g):,}; in G09/G12/G15 {int(gkeep.sum()):,}; grouped {float((g.GroupID.values[gkeep] > 0).mean()):.3f}")
if M1:   # M1: shuffle Z within each field
    rng = np.random.default_rng(519)
    for k in range(3):
        m = np.where(g_fld == k)[0]; g_z[m] = g_z[m][rng.permutation(len(m))]
    say("  M1: G3C redshifts permuted within each field (seed 519)")
g_nfof = np.zeros(len(g), int)
gid = g.GroupID.values
hasg = gid > 0
g_nfof[hasg] = G.loc[gid[hasg], "Nfof"].values
g_ic = g.RankIterCen.values; g_bcg = g.RankBCG.values
cat2row = pd.Series(np.arange(len(g)), index=g.CATAID.values)

# ------------------------------------------------------------------ positions, fields, matching
P_fld = field_of(P_ra, P_dec)
if M2:   # M2: shift RA by +1 deg wrapped inside the field box
    for k, (a0, a1, d0, d1) in enumerate(FIELDS):
        m = P_fld == k
        P_ra[m] = a0 + ((P_ra[m] - a0 + 1.0) % (a1 - a0))
    say("  M2: KiDS RA shifted +1.0 deg (wrapped inside each field box)")
inf = np.where(P_fld >= 0)[0]
say(f"  KiDS pool in the three fields: {len(inf):,}")
gt = cKDTree(unit(g_ra[gkeep], g_dec[gkeep])); gidx = np.where(gkeep)[0]
dd, jj = gt.query(unit(P_ra[inf], P_dec[inf]), distance_upper_bound=np.radians(1.5 / 3600))
ok = np.isfinite(dd)
cand_p, cand_g, cand_d = inf[ok], gidx[jj[ok]], dd[ok]
o = np.argsort(cand_d); _, first = np.unique(cand_g[o], return_index=True)
keep = o[first]
P_g = np.full(len(ip), -1); P_g[cand_p[keep]] = cand_g[keep]
P_sep = np.full(len(ip), np.nan); P_sep[cand_p[keep]] = np.degrees(cand_d[keep]) * 3600
P_zs = np.full(len(ip), np.nan); P_zs[P_g >= 0] = g_z[P_g[P_g >= 0]]
matched = P_g >= 0
say(f"  matched (1.5 arcsec, one-to-one): {int(matched.sum()):,} of {len(inf):,} in-field pool ({matched.sum() / len(inf):.3f}); "
    f"{len(cand_p) - len(keep)} duplicate claims dropped")
mz = matched & np.isfinite(P_zs)
dzn = (P_z[mz] - P_zs[mz]) / (1 + P_zs[mz])
nmad = 1.4826 * np.median(np.abs(dzn - np.median(dzn)))
check("C4 match quality (median sep < 0.5 arcsec)", np.nanmedian(P_sep[matched]) < 0.5 if matched.any() else False,
      f"median sep {np.nanmedian(P_sep[matched]) if matched.any() else np.nan:.3f}\"; photo-z NMAD {nmad:.4f}, bias {np.median(dzn):+.4f}, "
      f"|dz|/(1+z) > 0.15: {float((np.abs(dzn) > 0.15).mean()):.4f}", load=False)
RES["match"] = dict(n_infield=int(len(inf)), n_matched=int(matched.sum()), median_sep_arcsec=float(np.nanmedian(P_sep[matched])) if matched.any() else None,
                    photoz_nmad=float(nmad), photoz_bias=float(np.median(dzn)), outlier_frac=float((np.abs(dzn) > 0.15).mean()))

# lens-level arrays
L_p = lpos                                         # pool index of each lens candidate
L_fld = P_fld[L_p]
L_ra, L_dec = P_ra[L_p], P_dec[L_p]
rad = np.degrees(0.5 / lchi)
inside = np.zeros(NA, bool)
for k, (a0, a1, d0, d1) in enumerate(FIELDS):
    cd = np.cos(np.radians(L_dec))
    inside |= (L_fld == k) & (L_ra - rad / cd > a0) & (L_ra + rad / cd < a1) & (L_dec - rad > d0) & (L_dec + rad < d1)
L_g = P_g[L_p]; L_m = inside & (L_g >= 0)
L_zs = np.where(L_m, P_zs[L_p], np.nan)
REG = np.full(NA, -1)
for k, (a0, a1, d0, d1) in enumerate(FIELDS):
    m = inside & (L_fld == k); REG[m] = 4 * k + np.clip(((L_ra[m] - a0) // 3.0).astype(int), 0, 3)
P_reg = np.full(len(ip), -1)
for k, (a0, a1, d0, d1) in enumerate(FIELDS):
    m = P_fld == k; P_reg[m] = 4 * k + np.clip(((P_ra[m] - a0) // 3.0).astype(int), 0, 3)

gg = np.where(L_m, L_g, 0)
S_IC = L_m & (gid[gg] > 0) & (g_ic[gg] != 1)
S_BCG = L_m & (gid[gg] > 0) & (g_bcg[gg] != 1)
S_N3 = S_IC & (g_nfof[gg] >= 3)
iso_in = iso10 & inside
mrate = float(L_m[iso_in].sum() / max(iso_in.sum(), 1))
say(f"\n  ISO lenses in overlap {int(iso_in.sum()):,} (of 181,477), matched {int(L_m[iso_in].sum()):,} ({mrate:.3f}); "
    f"ALL in overlap {int(inside.sum()):,}, matched {int(L_m[inside].sum()):,}")
RES["n"] = dict(iso_in=int(iso_in.sum()), iso_in_matched=int(L_m[iso_in].sum()), all_in=int(inside.sum()),
                all_in_matched=int(L_m[inside].sum()), iso_match_rate=mrate)
if M2:
    m2_ok = mrate < 0.02
    check("M2 MUTATE: displaced positions kill the matches (ISO match rate < 2%)", m2_ok, f"match rate {mrate:.4f}")
    if m2_ok:
        say("  M2: V1 cannot be computed (no positional matches), as required.")
    RES["checks"] = CHK
    json.dump(RES, open(os.path.join(HERE, f"cfg519_satfrac_results{TAG}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg519_satfrac{TAG}.out"), "w").write("\n".join(LOG) + "\n")
    sys.exit(0 if m2_ok else 1)

# ------------------------------------------------------------------ cells and reweighting
ME = np.array([8.5, 9.5, 10.0, 10.25, 10.5, 10.75, 11.0]); ZE = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
cm = np.clip(np.digitize(llm, ME) - 1, 0, len(ME) - 2); cz = np.clip(np.digitize(lz, ZE) - 1, 0, len(ZE) - 2)
NCM, NCZ = len(ME) - 1, len(ZE) - 1
cell = (cm * NCZ + cz) * 2 + ltyp
NC = NCM * NCZ * 2


def cell_frac(val, src, w=wl):
    """per-cell weighted mean of val over src lenses, with the frozen fallback (pool over z, then over typ). Returns (f, n, direct)."""
    num = np.bincount(cell[src], weights=(w * val)[src], minlength=NC)
    den = np.bincount(cell[src], weights=w[src], minlength=NC)
    n = np.bincount(cell[src], minlength=NC)
    f = np.full(NC, np.nan); direct = n >= 20
    f[direct] = num[direct] / den[direct]
    n3 = n.reshape(NCM, NCZ, 2); num3 = num.reshape(NCM, NCZ, 2); den3 = den.reshape(NCM, NCZ, 2)
    f3 = f.reshape(NCM, NCZ, 2)
    for a in range(NCM):
        for t in range(2):
            for zc in range(NCZ):
                if np.isnan(f3[a, zc, t]):
                    if n3[a, :, t].sum() >= 20:
                        f3[a, zc, t] = num3[a, :, t].sum() / den3[a, :, t].sum()
                    elif n3[a].sum() >= 20:
                        f3[a, zc, t] = num3[a].sum() / den3[a].sum()
    return f3.reshape(NC), n, direct


def reweight(val, src, tgt, w=wl):
    f, n, direct = cell_frac(val, src, w)
    W = np.bincount(cell[tgt], weights=w[tgt], minlength=NC)
    good = np.isfinite(f)
    res = float((W[good] * f[good]).sum() / W[good].sum()) if W[good].sum() > 0 else np.nan
    return res, dict(W_share_direct=float(W[direct].sum() / W.sum()), W_share_defined=float(W[good].sum() / W.sum()))


# ------------------------------------------------------------------ completeness map c(r, z_phot)
RE_ = np.arange(14.0, 20.0001, 0.1); ZE_ = np.arange(0.10, 0.5001, 0.05)
P_cr = np.clip(np.digitize(P_r, RE_) - 1, 0, len(RE_) - 2); P_cz = np.clip(np.digitize(P_z, ZE_) - 1, 0, len(ZE_) - 2)
P_ccell = P_cr * (len(ZE_) - 1) + P_cz
NCC = (len(RE_) - 1) * (len(ZE_) - 1)


def cmap(excl=-1):
    m = (P_fld >= 0) & (P_reg != excl)
    tot = np.bincount(P_ccell[m], minlength=NCC); hit = np.bincount(P_ccell[m & matched], minlength=NCC)
    return np.where(tot > 0, hit / np.maximum(tot, 1), 0.0)


C_MAP = cmap()
cr_print = [(lo, float(np.average(C_MAP.reshape(len(RE_) - 1, -1)[(RE_[:-1] >= lo) & (RE_[:-1] < lo + 0.5)].ravel()))) for lo in (17.0, 18.0, 19.0, 19.5)]
say("  pool completeness (mean over z cells): " + ", ".join(f"r {lo:.1f}-{lo + 0.5:.1f}: {v:.3f}" for lo, v in cr_print))
RES["completeness_r"] = {f"{lo:.1f}": v for lo, v in cr_print}

# ------------------------------------------------------------------ pair search around matched in-overlap ISO lenses (spec) and ISO in overlap (phot)
say("\n== pair searches")
pt = cKDTree(unit(P_ra[inf], P_dec[inf]))
src_spec = np.where(iso_in & L_m)[0]
src_phot = np.where(iso_in)[0]
rng = np.random.default_rng(519)


def ann_frac(idx, chi):
    """fraction of the 4-6 Mpc annulus inside the lens's field box (200 random points)."""
    out = np.zeros(len(idx))
    u = rng.random((len(idx), 200)); th = 2 * np.pi * rng.random((len(idx), 200))
    Rr = np.sqrt(16 + 20 * u)                                   # uniform in area over 4..6 Mpc
    ang = np.degrees(Rr / chi[:, None])
    dd_ = L_dec[idx][:, None] + ang * np.sin(th); rr_ = L_ra[idx][:, None] + ang * np.cos(th) / np.cos(np.radians(L_dec[idx]))[:, None]
    for k, (a0, a1, d0, d1) in enumerate(FIELDS):
        m = L_fld[idx] == k
        out[m] = ((rr_[m] > a0) & (rr_[m] < a1) & (dd_[m] > d0) & (dd_[m] < d1)).mean(1)
    return out


# spec pairs: store (lens, pool j, inner?, annulus?) for matched pool j only
SP = dict(l=[], j=[], R=[], dv=[])
chi_s = DC(np.nan_to_num(L_zs, nan=0.3))
for i0 in range(0, len(src_spec), 4000):
    idx = src_spec[i0:i0 + 4000]
    lists = pt.query_ball_point(unit(L_ra[idx], L_dec[idx]), r=6.0 / chi_s[idx])
    k_ = np.repeat(np.arange(len(idx)), [len(x) for x in lists])
    js = inf[np.fromiter((j for x in lists for j in x), dtype=np.int64, count=sum(len(x) for x in lists))]
    li = idx[k_]
    m = (js != L_p[li]) & matched[js] & (P_lm[js] > llm[li])
    js, li = js[m], li[m]
    cosd = np.clip((unit(P_ra[js], P_dec[js]) * unit(L_ra[li], L_dec[li])).sum(1), -1, 1)
    R = np.arccos(cosd) * chi_s[li]
    dv = c_kms * (P_zs[js] - L_zs[li]) / (1 + L_zs[li])
    m = (R < 6.0) & (np.abs(dv) < 2000)
    SP["l"].append(li[m]); SP["j"].append(js[m]); SP["R"].append(R[m]); SP["dv"].append(dv[m])
SP = {k: np.concatenate(v) if len(v) else np.zeros(0) for k, v in SP.items()}
SP["l"] = SP["l"].astype(int); SP["j"] = SP["j"].astype(int)
afr_s = np.zeros(NA); afr_s[src_spec] = ann_frac(src_spec, chi_s[src_spec]) if len(src_spec) else 0
say(f"  spec pairs stored: {len(SP['l']):,} (matched lenses {len(src_spec):,})")

# phot pairs (recompute CFG502's photometric count on the overlap lenses; store companion (r, z) for the c < 0.1 share)
PP = dict(l=[], j=[], inner=[])
for i0 in range(0, len(src_phot), 4000):
    idx = src_phot[i0:i0 + 4000]
    lists = pt.query_ball_point(unit(L_ra[idx], L_dec[idx]), r=6.0 / lchi[idx])
    k_ = np.repeat(np.arange(len(idx)), [len(x) for x in lists])
    js = inf[np.fromiter((j for x in lists for j in x), dtype=np.int64, count=sum(len(x) for x in lists))]
    li = idx[k_]
    m = (js != L_p[li]) & (P_lm[js] > llm[li])
    js, li = js[m], li[m]
    adc = np.abs(P_chi[js] - lchi[li])
    cosd = np.clip((unit(P_ra[js], P_dec[js]) * unit(L_ra[li], L_dec[li])).sum(1), -1, 1)
    R = np.arccos(cosd) * lchi[li]
    m = (adc > 10) & (adc < 600) & ((R < 0.5) | ((R >= 4) & (R < 6)))
    PP["l"].append(li[m]); PP["j"].append(js[m]); PP["inner"].append(R[m] < 0.5)
PP = {k: np.concatenate(v) for k, v in PP.items()}
cin_re = np.bincount(PP["l"][PP["inner"]], minlength=NA)
can_re = np.bincount(PP["l"][~PP["inner"]], minlength=NA)
# CFG502's annulus was not footprint-limited (pool galaxies anywhere); our tree only holds in-field pool, so compare inner counts exactly
pos_in_iso = np.searchsorted(iso_idx, src_phot)
c2b = np.array_equal(cin_re[src_phot], S["cin"][pos_in_iso].astype(int))
check("C2b inner photometric companion counts on overlap lenses = CFG502's cin", c2b,
      f"{len(src_phot):,} lenses", load=not MUT)
inner_j = PP["j"][PP["inner"]]; ann_j = PP["j"][~PP["inner"]]
low_c_in = C_MAP[P_ccell[inner_j]] < 0.1; low_c_an = C_MAP[P_ccell[ann_j]] < 0.1
afr_p = np.zeros(NA); afr_p[src_phot] = ann_frac(src_phot, lchi[src_phot])
ex_all = len(inner_j) - (0.25 / 20) * np.sum(1 / np.maximum(afr_p[PP["l"][~PP["inner"]]], 0.05))
ex_low = low_c_in.sum() - (0.25 / 20) * np.sum(low_c_an / np.maximum(afr_p[PP["l"][~PP["inner"]]], 0.05))
share_low = float(ex_low / ex_all) if ex_all > 0 else np.nan
say(f"  share of the photometric companion excess on overlap lenses in completeness cells c < 0.1: {share_low:.3f}")
RES["phot_excess_share_lowc"] = share_low


def cspec_per_lens(cm_, dvmax=1000.0):
    wj = np.where(cm_[P_ccell[SP["j"]]] >= 0.1, 1 / np.maximum(cm_[P_ccell[SP["j"]]], 0.1), 0.0)
    sel_ = np.abs(SP["dv"]) < dvmax
    inn = sel_ & (SP["R"] < 0.5); ann = sel_ & (SP["R"] >= 4.0)
    ci = np.bincount(SP["l"][inn], weights=wj[inn], minlength=NA)
    ca = np.bincount(SP["l"][ann], weights=wj[ann], minlength=NA)
    out = ci - ca * (0.25 / 20) / np.maximum(afr_s, 0.05)
    # pair satellite: raw indicator (any matched more-massive companion, unweighted) and chance rate
    ri = np.bincount(SP["l"][inn], minlength=NA) > 0
    lam = np.bincount(SP["l"][ann], minlength=NA) * (0.25 / 20) / np.maximum(afr_s, 0.05)
    return out, ri.astype(float), np.exp(-lam)


# ------------------------------------------------------------------ all statistics for one jackknife configuration
SUB = llm >= 10.44


def stats(excl=-1):
    use = (REG != excl)
    srcI = iso_in & L_m & use; srcA = inside & L_m & use; src30 = iso30 & inside & L_m & use
    o = {}
    o["f_IC"], meta = reweight(S_IC.astype(float), srcI, iso10)
    o["f_BCG"], _ = reweight(S_BCG.astype(float), srcI, iso10)
    o["f_N3"], _ = reweight(S_N3.astype(float), srcI, iso10)
    o["f_raw"] = float((wl * S_IC)[srcI].sum() / max(wl[srcI].sum(), 1e-300))
    o["f_ALL_parent"], _ = reweight(S_IC.astype(float), srcA, sel_all)
    o["f_ALL_on_isocells"], _ = reweight(S_IC.astype(float), srcA, iso10)
    o["f30"], _ = reweight(S_IC.astype(float), src30, iso30)
    o["iso_over_all"] = o["f_IC"] / o["f_ALL_on_isocells"] if o["f_ALL_on_isocells"] > 0 else np.nan
    cm_ = cmap(excl)
    cs, ri, eb = cspec_per_lens(cm_, 1000.0)
    cs2, _, _ = cspec_per_lens(cm_, 2000.0)
    ph = np.nan_to_num(phot_meas)
    for nm, sub in (("sub", SUB), ("all", np.ones(NA, bool))):
        o[f"C_spec_{nm}"], _ = reweight(cs, srcI & sub, iso10 & sub)
        o[f"C_spec2000_{nm}"], _ = reweight(cs2, srcI & sub, iso10 & sub)
        o[f"C_phot_{nm}"], _ = reweight(ph, srcI & sub, iso10 & sub)
        o[f"C_phot_overlap_all_{nm}"], _ = reweight(ph, iso_in & use & sub, iso10 & sub)
        o[f"C_diff_{nm}"] = o[f"C_spec_{nm}"] - o[f"C_phot_{nm}"]
    fr, _ = reweight(ri, srcI, iso10); ebm, _ = reweight(eb, srcI, iso10)
    o["f_pair_raw"] = fr; o["f_pair"] = 1 - (1 - fr) / ebm
    return o, meta


sel_all = np.ones(NA, bool)
main, meta = stats()
jk = [stats(k)[0] for k in range(12)]
keys = list(main.keys())
sig = {}
for k in keys:
    v = np.array([j[k] for j in jk], float)
    sig[k] = float(np.sqrt(11 / 12 * np.nansum((v - np.nanmean(v)) ** 2))) if np.isfinite(v).sum() > 1 else np.nan
say("\n== results (stack-P weighted, completeness-reweighted to the full 181,477-lens stack; 12-region jackknife)")
say(f"  weight share in cells with >= 20 matched lenses: {meta['W_share_direct']:.3f}; defined after fallback: {meta['W_share_defined']:.3f}")
for k in keys:
    say(f"  {k:24s} {main[k]: .4f} +- {sig[k]:.4f}")
RES["main"] = main; RES["sigma_stat"] = sig; RES["cell_meta"] = meta

# per-cell table (log M*, z), typ combined with stack-P weights
fcell, ncell, _ = cell_frac(S_IC.astype(float), iso_in & L_m)
W = np.bincount(cell, weights=wl * iso10, minlength=NC)
say("\n  f_sat (S_IC) per (log M*, z_phot) cell [typ combined with stack-P weights; n matched]:")
tab = {}
for a in range(NCM):
    row = []
    for zc in range(NCZ):
        ii = [(a * NCZ + zc) * 2 + t for t in range(2)]
        ww = np.array([W[i] if np.isfinite(fcell[i]) else 0 for i in ii]); ff = np.array([fcell[i] if np.isfinite(fcell[i]) else 0 for i in ii])
        v = float((ww * ff).sum() / ww.sum()) if ww.sum() > 0 else np.nan
        n = int(sum(ncell[i] for i in ii))
        row.append(f"{v:.3f} ({n})"); tab[f"{ME[a]:.2f}-{ME[a + 1]:.2f}|{ZE[zc]:.1f}-{ZE[zc + 1]:.1f}"] = dict(f=v, n=n)
    say(f"    log M* {ME[a]:5.2f}-{ME[a + 1]:5.2f}: " + "  ".join(row))
RES["cells"] = tab

# ------------------------------------------------------------------ C5 representativeness and C6 veto efficiency
say("\n== C5 / C6")
allt = cKDTree(unit(P_ra, P_dec))


def p10(lens_idx):
    H_in = np.zeros(240); H_an = np.zeros(240); DE = np.arange(-600.0, 600.0 + 1e-9, 5.0)
    for i0 in range(0, len(lens_idx), 5000):
        idx = lens_idx[i0:i0 + 5000]
        lists = allt.query_ball_point(unit(L_ra[idx], L_dec[idx]), r=6.0 / lchi[idx])
        k_ = np.repeat(np.arange(len(idx)), [len(x) for x in lists])
        js = np.fromiter((j for x in lists for j in x), dtype=np.int64, count=sum(len(x) for x in lists))
        li = idx[k_]
        m = (js != L_p[li]) & (P_lm[js] > llm[li] - 1.0)
        js, li = js[m], li[m]
        cosd = np.clip((unit(P_ra[js], P_dec[js]) * unit(L_ra[li], L_dec[li])).sum(1), -1, 1)
        R = np.arccos(cosd) * lchi[li]; dc = P_chi[js] - lchi[li]
        H_in += np.histogram(dc[R < 0.3], DE)[0]; H_an += np.histogram(dc[(R >= 4) & (R < 6)], DE)[0]
    ex = H_in - H_an * 0.09 / 20; cen = 0.5 * (DE[1:] + DE[:-1])
    return float(ex[np.abs(cen) < 10].sum() / ex.sum())


rr = np.random.default_rng(5190)
zl3 = lz < 0.3
in_idx = np.where(inside & zl3)[0]; out_idx = np.where(~inside & (L_fld < 0) & zl3)[0]
in_idx = np.sort(rr.choice(in_idx, min(60000, len(in_idx)), replace=False)); out_idx = np.sort(rr.choice(out_idx, min(60000, len(out_idx)), replace=False))
p_in, p_out = p10(in_idx), p10(out_idx)
c5 = abs(p_in - p_out) <= 0.02
check("C5 GAMA-area photo-z representative (|p_10,in - p_10,out| <= 0.02, z < 0.3)", c5, f"p_10 in {p_in:.4f}, out {p_out:.4f}",
      load=not MUT)
pass_in = float(iso10[inside].mean()); pass_out = float(iso10[L_fld < 0].mean())
say(f"  ISO pass fraction: overlap {pass_in:.3f}, outside fields {pass_out:.3f}")
RES["C5"] = dict(p10_in=p_in, p10_out=p_out, iso_pass_in=pass_in, iso_pass_out=pass_out)

# C6: veto efficiency of true (G3C) satellite-centre pairs
g2p = np.full(len(g), -1); g2p[P_g[matched]] = np.where(matched)[0]
satA = np.where(inside & S_IC)[0]
icc = G.loc[gid[L_g[satA]], "IterCenCATAID"].values
icrow = cat2row.reindex(icc).values
okr = np.isfinite(icrow); icrow = np.where(okr, icrow, 0).astype(int)
cp = np.where(okr, g2p[icrow], -1)
v = cp >= 0
li, cj = satA[v], cp[v]
cosd = np.clip((unit(P_ra[cj], P_dec[cj]) * unit(L_ra[li], L_dec[li])).sum(1), -1, 1)
Rr = np.arccos(cosd) * lchi[li]
q = (Rr < 3.0) & (P_lm[cj] > llm[li] - 1.0)
vet = np.abs(P_chi[cj] - lchi[li]) < 10
for lab, mz_ in (("z<0.3", lz[li] < 0.3), ("all z", np.ones(len(li), bool))):
    mm = q & mz_
    say(f"  C6 veto efficiency, G3C satellite vs its matched iterative centre ({lab}): {vet[mm].mean() if mm.any() else np.nan:.4f} "
        f"of {int(mm.sum()):,} qualifying pairs; ISO share of these satellites {iso10[li[mm]].mean() if mm.any() else np.nan:.3f}")
    RES[f"C6_{lab}"] = dict(veto=float(vet[mm].mean()) if mm.any() else None, n=int(mm.sum()),
                           iso_share=float(iso10[li[mm]].mean()) if mm.any() else None)

# ------------------------------------------------------------------ verdicts
say("\n== verdicts (frozen rules)")
sys_ = float(np.hypot(main["f_IC"] - main["f_BCG"], main["f_IC"] - main["f_raw"]))
stot = float(np.hypot(sig["f_IC"], sys_))
RES["sigma_sys"] = sys_; RES["sigma_tot"] = stot
lab = [] if c5 else ["GAMA-AREA PHOTO-Z NOT REPRESENTATIVE"]
V1 = {}
REFS = {"CFG502_HOD": 0.17122385594807057, "CFG503": 0.1805564701196465, "CFG506_F": 0.3434843404193193, "CFG506_P": 0.4316614798131967}
for nm, X in REFS.items():
    zsc = abs(main["f_IC"] - X) / stot
    V1[nm] = dict(X=X, n_sigma=float(zsc), verdict="CONSISTENT" if zsc <= 2 else ("EXCLUDED" if zsc > 3 else "TENSION"))
    say(f"  V1 f_obs = {main['f_IC']:.4f} +- {stot:.4f} (stat {sig['f_IC']:.4f}, sys {sys_:.4f}) vs {nm} {X:.3f}: "
        f"{zsc:.2f} sigma -> {V1[nm]['verdict']}")
recal = V1["CFG506_F"]["verdict"] == "EXCLUDED"
conf502 = V1["CFG502_HOD"]["verdict"] == "CONSISTENT"
say(f"  -> CFG506 box galaxy-halo rule needs re-calibration: {'YES' if recal else 'NO'}; "
    f"CFG502/503 leakage input confirmed: {'YES' if conf502 else 'NO'}"
    + ("" if V1["CFG502_HOD"]["verdict"] != "EXCLUDED" else " (LEAKAGE INPUT CONTRADICTED)"))
ratio = main["C_spec_sub"] / 0.3133211723403403
d2 = abs(main["C_diff_sub"]) / sig["C_diff_sub"] if sig["C_diff_sub"] > 0 else np.nan
V2 = dict(C_spec_sub=main["C_spec_sub"], sig=sig["C_spec_sub"], ratio_to_506F=ratio,
          box_prediction=("CONSISTENT" if 0.67 <= ratio <= 1.5 else "NOT CONSISTENT"),
          C_phot_sub=main["C_phot_sub"], diff_sigma=float(d2), photometric_excess=("CONFIRMED" if d2 <= 2 else "QUESTIONED"))
say(f"  V2 C_spec (log M* >= 10.44) = {main['C_spec_sub']:.4f} +- {sig['C_spec_sub']:.4f}; / 0.313 = {ratio:.3f} -> box prediction "
    f"{V2['box_prediction']}; C_phot same lenses {main['C_phot_sub']:.4f}; |diff| = {d2:.2f} sigma -> photometric excess {V2['photometric_excess']}")
RES["V1"] = V1; RES["V2"] = V2; RES["labels"] = lab
RES["recalibration_needed"] = recal; RES["cfg502_leakage_confirmed"] = conf502

if MUT:
    ref = json.load(open(os.path.join(HERE, "cfg519_satfrac_results.json")))["main"]
    m1a = abs(main["C_spec_sub"]) < max(3 * sig["C_spec_sub"], 0.2 * abs(ref["C_spec_sub"]))
    m1b = abs(main["f_pair"]) < max(3 * sig["f_pair"], 0.2 * abs(ref["f_pair"]))
    check("M1 MUTATE: shuffled redshifts kill C_spec", m1a, f"C_spec {main['C_spec_sub']:+.4f} +- {sig['C_spec_sub']:.4f} (main {ref['C_spec_sub']:.4f})")
    check("M1 MUTATE: shuffled redshifts kill f_pair", m1b, f"f_pair {main['f_pair']:+.4f} +- {sig['f_pair']:.4f} (main {ref['f_pair']:.4f})")
RES["checks"] = CHK
if not MUT:   # state for the post-hoc diagnostics (git-ignored work dir)
    np.savez(os.path.join(WORK, "cfg519_state.npz"), P_ra=P_ra, P_dec=P_dec, P_z=P_z, P_chi=P_chi, P_lm=P_lm, P_r=P_r, P_fld=P_fld,
             P_g=P_g, P_zs=P_zs, matched=matched, C_MAP=C_MAP, P_ccell=P_ccell, L_p=L_p, inside=inside, L_m=L_m, L_zs=L_zs, REG=REG,
             S_IC=S_IC, S_BCG=S_BCG, L_g=L_g, cell=cell, afr_p=afr_p, afr_s=afr_s)
say(f"\nlabels: {lab if lab else 'none'}; elapsed {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"cfg519_satfrac_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg519_satfrac{TAG}.out"), "w").write("\n".join(LOG) + "\n")
lb_fail = [k for k, v in CHK.items() if v["load_bearing"] and not v["ok"]]
sys.exit(1 if lb_fail else 0)
