#!/usr/bin/env python3
"""CFG525 stage 2 (FROZEN_CRITERIA.md 7f99a4371, M-i(a), K5, T3): baryons of photometric neighbours inside each stack-P lens's turnaround
sphere (projected < r_ta, comoving r_ta (1+z)), |d chi| < 10 Mpc (the W10 isolation window), self excluded, with a local background from
the 2.5-3.5 Mpc comoving annulus (same window), area-scaled.  Pool exactly as lr_esd_remeasure.stage_lens builds it (r < 20,
0.1 < z_phot < 0.5, unmasked, logM = MASS_MED + 0.15, M_gal = M*(1 + f_cold)).  Both footings (r_ta differs).
MUTATE (CFG525_MUTATE=1): lens positions displaced by +1 deg in Dec (T3: background-subtracted excess must vanish).
Output: ../../../_external_data/cfg525_work/cfg525_neighbours[_MUTATE].npz ; cfg525_neighbours[_MUTATE].out / _results[_MUTATE].json
Run: nice -n 10 python3 cfg525_neighbours.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import math, json, time
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
import cfg100_lib as C                                                       # noqa: E402  (read-only)
try:
    os.nice(10)
except OSError:
    pass
MUTATE = os.environ.get("CFG525_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg525_work"))
os.makedirs(WORK, exist_ok=True)
W503 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work"))
FOOTS = ("canonical", "alt")
WIN, A_IN, A_OUT = 10.0, 2.5, 3.5
LOG, CHK = [], {}
RES = {"lane": "CFG525", "script": "cfg525_neighbours", "mutate": MUTATE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
c = 2.998e8; Mpc = 3.0857e22; H0 = 70 * 1e3 / Mpc


def DC(z, n=2048):            # copied from lr_esd_remeasure (h70 Mpc, Om 0.3)
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c / H0) / Mpc
    return np.interp(z, zz, chi)


b = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
Lp = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
r = np.array(b["MAG_AUTO_CALIB"], dtype="f8"); z = np.array(b["zphot_ANNz2"], dtype="f8"); masked = np.array(b["masked"])
logM = np.array(Lp["MASS_MED"], dtype="f8") + 0.15
ra = np.array(b["RAJ2000"], dtype="f8"); dec = np.array(b["DECJ2000"], dtype="f8")
del b, Lp
pool = (r < 20) & (z > 0.1) & (z < 0.5) & (masked == 0) & np.isfinite(logM) & (logM > 7)
ip = np.where(pool)[0]
zP, lMP = z[ip], logM[ip]; chiP = DC(zP)
MgP = 10 ** lMP * (1 + 10 ** (-0.69 * lMP + 6.63))
raP, decP = np.radians(ra[ip]), np.radians(dec[ip])
xyzP = np.c_[np.cos(decP) * np.cos(raP), np.cos(decP) * np.sin(raP), np.sin(decP)]
del r, z, masked, logM, ra, dec
tree = cKDTree(xyzP)
P(f"pool {len(ip):,} galaxies")

lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
lz, lchi, lMg = lens["z"].astype(float), lens["chi"].astype(float), lens["Mgal"].astype(float)
lra, ldec = np.radians(lens["ra"]), np.radians(lens["dec"])
nL = len(lz)
xyzL = np.c_[np.cos(ldec) * np.cos(lra), np.cos(ldec) * np.sin(lra), np.sin(ldec)]
dd, jj = tree.query(xyzL, k=1)
k5 = (np.max(dd) < 1e-9) and np.allclose(lMg, MgP[jj], rtol=1e-6) and np.allclose(lchi, chiP[jj], rtol=1e-9)
check("K5 every stack-P lens is in the rebuilt pool at zero separation with identical M_gal and chi", k5,
      f"max sep {np.max(dd):.1e} rad; max |dM/M| {np.max(np.abs(MgP[jj] / lMg - 1)):.1e}")
SELF = jj
if MUTATE:
    ldec2 = ldec + math.radians(1.0)
    xyzL = np.c_[np.cos(ldec2) * np.cos(lra), np.cos(ldec2) * np.sin(lra), np.sin(ldec2)]
    SELF = np.full(nL, -1)
    P("  *** MUTATE: lens positions displaced by +1 deg in Dec (T3) ***")

OT = np.load(os.path.join(W503, "cfg503_own_tables.npz"))
gi, GM, GZ = OT["gi"], OT["GM"], OT["GZ"]
RTA = {f: np.array([C.r_ta_law(GM[g], C.A0[f], GZ[g]) for g in range(len(GM))]) for f in FOOTS}
RC = {f: RTA[f][gi] * (1 + lz) for f in FOOTS}                                # comoving r_ta per lens
P("  comoving r_ta per lens, median: " + ", ".join(f"{f} {np.median(RC[f]):.3f} Mpc" for f in FOOTS))

raw = {f: np.zeros(nL) for f in FOOTS}; nin = {f: np.zeros(nL) for f in FOOTS}
ann = np.zeros(nL); nann = np.zeros(nL)
CH = 4000
rmax = np.maximum(A_OUT, np.maximum(RC["canonical"], RC["alt"]))
for i0 in range(0, nL, CH):
    sl = slice(i0, min(i0 + CH, nL))
    lists = tree.query_ball_point(xyzL[sl], r=rmax[sl] / lchi[sl])
    cnt = np.array([len(x) for x in lists]); li = np.repeat(np.arange(sl.start, sl.stop), cnt)
    J = np.concatenate([np.asarray(x, dtype=np.int64) for x in lists]) if cnt.sum() else np.zeros(0, np.int64)
    keep = (J != SELF[li]) & (np.abs(chiP[J] - lchi[li]) < WIN)
    li, J = li[keep], J[keep]
    cosang = np.clip(np.einsum("ij,ij->i", xyzL[li], xyzP[J]), -1, 1)
    Rp = np.arccos(cosang) * lchi[li]                                       # comoving projected separation [Mpc]
    m = MgP[J]
    a_ = (Rp >= A_IN) & (Rp < A_OUT)
    ann += np.bincount(li - 0, weights=m * a_, minlength=nL)
    nann += np.bincount(li, weights=a_.astype(float), minlength=nL)
    for f in FOOTS:
        w = Rp < RC[f][li]
        raw[f] += np.bincount(li, weights=m * w, minlength=nL)
        nin[f] += np.bincount(li, weights=w.astype(float), minlength=nL)
    if (i0 // CH) % 10 == 0:
        P(f"    {sl.stop:,}/{nL:,} lenses ({time.time() - T0:.0f} s)")
AREA_ANN = math.pi * (A_OUT ** 2 - A_IN ** 2)
bg = {f: ann * math.pi * RC[f] ** 2 / AREA_ANN for f in FOOTS}
exc = {f: raw[f] - bg[f] for f in FOOTS}
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); wl = pl["WW"].sum(1)


def jk_mean(v):
    m = np.average(v, weights=wl)
    loo = np.array([np.average(v[patch != k], weights=wl[patch != k]) for k in range(50)])
    return float(m), float(math.sqrt(49 / 50 * np.sum((loo - loo.mean()) ** 2)))


for f in FOOTS:
    mr, er = jk_mean(raw[f] / lMg); mb, eb = jk_mean(bg[f] / lMg); me, ee = jk_mean(exc[f] / lMg)
    RES[f] = dict(raw_over_Mlens=[mr, er], bg_over_Mlens=[mb, eb], excess_over_Mlens=[me, ee],
                  mean_count_in=float(np.average(nin[f], weights=wl)), frac_lenses_raw_gt_0p1=float(np.average(raw[f] / lMg > 0.1, weights=wl)))
    P(f"  [{f}] lens-weighted neighbour baryons / M_lens: raw {mr:.4f} +- {er:.4f}; background {mb:.4f} +- {eb:.4f}; "
      f"excess {me:.4f} +- {ee:.4f}; mean count in {RES[f]['mean_count_in']:.2f}")
np.savez(os.path.join(WORK, f"cfg525_neighbours{SUF}.npz"), raw_canonical=raw["canonical"], raw_alt=raw["alt"], bg_canonical=bg["canonical"],
         bg_alt=bg["alt"], ann=ann, nann=nann)
if MUTATE:
    Jp = json.load(open(os.path.join(HERE, "cfg525_neighbours_results.json")))
    ok = True; msg = []
    for f in FOOTS:
        me, ee = RES[f]["excess_over_Mlens"]; mp = Jp[f]["excess_over_Mlens"][0]
        ok_f = abs(me) < 3 * ee or abs(me) < 0.2 * abs(mp)
        ok &= ok_f; msg.append(f"{f}: displaced excess {me:+.4f} +- {ee:.4f} vs primary {mp:+.4f}")
    check("T3 displaced positions: background-subtracted neighbour excess consistent with zero", ok, "; ".join(msg))
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg525_neighbours_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg525_neighbours{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
