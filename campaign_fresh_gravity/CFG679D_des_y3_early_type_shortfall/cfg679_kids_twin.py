#!/usr/bin/env python3
"""CFG679D KiDS twin (FROZEN_CRITERIA.md section 4): the framework-native eps on the KiDS f30 lenses with the SAME estimator that is
applied to DES (E = 0, unstripped LAW_RTA own profile, GLS amplitude per band, 50-patch jackknife / Hartlap).
Inputs (read-only, on disk): real_research/data/lensing_rar/{cfg110_perlens, lr_lenses, lr_esd_jackknife, cfg96_isoflags}.npz;
control K-T1 against CFG503's committed own table (../_external_data/cfg503_work/cfg503_own_tables.npz) when present.
Output: cfg679_kids_twin.out, cfg679_kids_twin_results.json (+ _MUTATE under CFG679_MUTATE=1: rotated-shear analogue = sign-randomised
per-lens WG, and the Newtonian own profile).
Run: nice -n 10 python3 cfg679_kids_twin.py
"""
import os, sys, json, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg679_common as K                                                   # noqa: E402
import cfg679_lib as L                                                      # noqa: E402

MUTATE = os.environ.get("CFG679_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
T0 = time.time()
LOG = []
RES = {"lane": "CFG679D", "script": "cfg679_kids_twin", "mutate": MUTATE,
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu_mono; E = 0 (framework-native); cold energy mass required; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


L.guard(P)
D = os.path.join(K.REPO, "real_research", "data", "lensing_rar")
lens = np.load(os.path.join(D, "lr_lenses.npz"))
pl = np.load(os.path.join(D, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
patch = np.load(os.path.join(D, "lr_esd_jackknife.npz"))["patch"]
F30 = np.load(os.path.join(D, "cfg96_isoflags.npz"))["f30"].astype(bool)
z, Mg, lms, typ = lens["z"], lens["Mgal"], lens["logM"], lens["typ"].astype(int)
gi, GM, GZ = K.groups(z, Mg)
P(f"KiDS stack P {len(z):,} lenses, f30 {F30.sum():,}; groups {len(GM):,}")

# own tables (all groups that hold an f30 lens are needed; compute for all groups touched by f30)
need = np.unique(gi[F30])
OWN = {}
for foot in K.FOOTS:
    tab = np.full((len(GM), 15), np.nan)
    for g in need:
        tab[g] = K.own_law_rta(GM[g], GZ[g], foot)
    OWN[foot] = tab
P(f"own LAW_RTA tables built for {len(need):,} groups ({time.time() - T0:.0f} s)")
NEWT = np.full((len(GM), 15), np.nan)
for g in need:
    NEWT[g] = K.own_newton(GM[g])

# control K-T1: CFG503's committed own LAW_RTA full_moster table (if the work file exists)
EXT = os.path.abspath(os.path.join(K.REPO, "..", "_external_data", "cfg503_work", "cfg503_own_tables.npz"))
if os.path.exists(EXT):
    OT = np.load(EXT)
    same_groups = np.array_equal(OT["gi"], gi) and np.allclose(OT["GM"], GM, rtol=1e-12)
    dev = {}
    for foot in K.FOOTS:
        key = f"{foot}|LAW_RTA|full_moster"
        if key in OT.files and same_groups:
            dev[foot] = float(np.nanmax(np.abs(OT[key][need] / OWN[foot][need] - 1)))
    RES["K_T1"] = dict(same_groups=bool(same_groups), max_rel_dev=dev, ok=bool(same_groups and dev and max(dev.values()) < 1e-6))
    P(f"[{'PASS' if RES['K_T1']['ok'] else 'FAIL'}] K-T1 own table = CFG503 committed LAW_RTA full_moster: {RES['K_T1']}")
else:
    RES["K_T1"] = dict(ok=None, msg="cfg503 work table not on disk")
    P("K-T1 not run (CFG503 work table absent)")

rng = np.random.default_rng(679)
WGm = WG.copy()
if MUTATE:
    # rotated-shear analogue on stored per-lens sums: a random sign per lens (a random 90-degree rotation of all its sources' shears)
    WGm = WG * rng.choice([-1.0, 1.0], size=len(WG))[:, None]


def measure(mask, own, wl=None):
    d, Cv, loo = K.esd_jk(WGm[mask], WW[mask], patch[mask], wl=None if wl is None else wl[mask])
    o = K.stack(own, gi[mask], WW[mask], wl=None if wl is None else wl[mask])
    out = {b: K.eps_band(d, Cv, o, idx) for b, idx in K.BANDS.items()}
    return out, d, Cv, loo, o


SAMPLES = {"f30_all": F30, "f30_early": F30 & (typ == 1), "f30_late": F30 & (typ == 0),
           "f30_early_z020": F30 & (typ == 1) & (z > 0.2), "f30_all_z020": F30 & (z > 0.2)}
RES["samples"] = {}
for name, m in SAMPLES.items():
    RES["samples"][name] = {"n": int(m.sum()), "logMs_wmean_Kin": float(np.average(lms[m], weights=WW[m][:, 12:15].sum(1)))}
    for foot in K.FOOTS:
        out, d, Cv, loo, o = measure(m, OWN[foot])
        RES["samples"][name][foot] = out
        if name in ("f30_early", "f30_late"):
            RES["samples"][name][foot + "_loo"] = {b: [float(x) for x in (np.array([float(o[idx] @ (l[idx] - o[idx])) / float(o[idx] @ o[idx]) for l in loo]))]
                                                   for b, idx in K.BANDS.items()}
        P(f"{name:16s} {foot:9s} " + "  ".join(f"{b} {v['eps']:+.3f}±{v['sig']:.3f}" for b, v in out.items()))
    RES["samples"][name]["R_kpc"] = [float(x) for x in K.bin_radii(Mg[m], WW[m])]

# early - late difference: jackknife of the per-patch eps (unweighted LS amplitude per realisation), plus quadrature
RES["early_minus_late"] = {}
for foot in K.FOOTS:
    for b in K.BANDS:
        e, l = RES["samples"]["f30_early"][foot][b], RES["samples"]["f30_late"][foot][b]
        le = np.array(RES["samples"]["f30_early"][foot + "_loo"][b]); ll = np.array(RES["samples"]["f30_late"][foot + "_loo"][b])
        dd = le - ll
        sjk = float(np.sqrt((K.NPATCH - 1) / K.NPATCH * ((dd - dd.mean()) ** 2).sum()))
        sq = float(np.hypot(e["sig"], l["sig"]))
        RES["early_minus_late"][f"{foot}|{b}"] = dict(diff=e["eps"] - l["eps"], sig_jk=sjk, sig_quad=sq, sig=max(sjk, sq),
                                                       Z=(e["eps"] - l["eps"]) / max(sjk, sq))
# Newtonian own profile (MUTATE tooth T2 analogue on KiDS: eps must move far above the law's)
RES["newton_own_f30_early"] = measure(SAMPLES["f30_early"], NEWT)[0]
P("Newtonian own (f30 early): " + "  ".join(f"{b} {v['eps']:+.3f}" for b, v in RES["newton_own_f30_early"].items()))

RES["elapsed_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, f"cfg679_kids_twin_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg679_kids_twin{SUF}.out"), "w").write("\n".join(LOG) + "\n")
P(f"done {RES['elapsed_s']:.0f} s")
