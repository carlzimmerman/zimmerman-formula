"""Turn the two 256^3 replays (replay_frames_256.py) into the /cosmic-web timeline assets, after checking them against the committed runs.

Inputs (read-only): _external_data/cosmic_web_replay/{RES,S0}/ (frames.npz, meta.json, pos_<k>.npy)
Committed numbers the replay must reproduce (same seed 360, 256^3):
  framework : _external_data/cfg424_work/cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N256_seed360.json   (CFG425 R1)
  control   : _external_data/cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360.json
  and campaign_fresh_gravity/CFG425_turnaround_catchment_confirm/cfg425_results.json (R1: sigma8 ratio and max|P-1|)
Outputs (public/data/cosmic512/): tl_res.png, tl_s0.png, tl_swi.png (6-wide atlases of 256 x 256 slab images, one per frame),
  tl_halo.bin (Int16 [run][frame][id][xyz], tracked particles of the most massive halo), timeline.json (frame table, sigma8, P(k), ranges, validation).
Run from the repo root: python3 ai_slop/website/scripts/build_cosmic_web_replay.py
"""
import json, os, sys
import numpy as np
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
RP = os.path.join(EXT, "cosmic_web_replay")
OUT = os.path.join(REPO, "ai_slop", "website", "public", "data", "cosmic512")
L, NP, COLS = 200.0, 256, 6
H, OM_B, OM_C, RHO_CRIT = 0.6736, 0.02237, 0.1200, 2.77536627e11
M_P = (OM_B + OM_C) / H ** 2 * RHO_CRIT * (L / NP) ** 3
NHALO, HALO_R = 6000, 3.0
os.makedirs(OUT, exist_ok=True)
meta = {k: json.load(open(os.path.join(RP, k, "meta.json"))) for k in ("RES", "S0")}
fr = {k: np.load(os.path.join(RP, k, "frames.npz")) for k in ("RES", "S0")}
F = len(meta["RES"]["a"])
assert F == len(meta["S0"]["a"]) and np.allclose(meta["RES"]["a"], meta["S0"]["a"])

# ---------------------------------------------------------------- 1. does the replay reproduce the committed run?
def committed(path):
    return json.load(open(path))["snap"]

ref = {"RES": committed(os.path.join(EXT, "cfg424_work", "cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N256_seed360.json")),
       "S0": committed(os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360.json"))}
SIG_LIM, PK_LIM = 2e-3, 5e-3
validation = []
for run, label in (("RES", "framework"), ("S0", "control")):
    for snap in ("z1", "z0.5", "z0"):
        mine, old = meta[run]["engine_snap"][snap], ref[run][snap]
        ds = abs(mine["sigma8"] / old["sigma8"] - 1)
        k = np.array(old["k"]); m = k <= 1
        dp = float(np.max(np.abs(np.array(mine["P"])[m] / np.array(old["P"])[m] - 1)))
        validation.append(dict(name=f"{label} σ₈ at {snap}", value=float(ds), limit=SIG_LIM, ok=bool(ds < SIG_LIM), note=f"replay {mine['sigma8']:.4f} vs committed {old['sigma8']:.4f}"))
        validation.append(dict(name=f"{label} P(k≤1) at {snap}", value=dp, limit=PK_LIM, ok=bool(dp < PK_LIM), note=f"largest bin difference {dp * 100:.3f}%"))
r1 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG425_turnaround_catchment_confirm", "cfg425_results.json")))["R1 256^3 seed 360"]
mr, ms = meta["RES"]["engine_snap"]["z0"], meta["S0"]["engine_snap"]["z0"]
kk = np.array(mr["k"]); mk = kk <= 1
pdev = float(np.max(np.abs(np.array(mr["P"])[mk] / np.interp(kk[mk], np.array(ms["k"]), np.array(ms["P"])) - 1)))
s8 = mr["sigma8"] / ms["sigma8"]
validation.append(dict(name="growth check, σ₈ ratio (CFG425 R1)", value=float(abs(s8 - r1["s8"])), limit=2e-3, ok=bool(abs(s8 - r1["s8"]) < 2e-3), note=f"replay {s8:.4f} vs CFG425 {r1['s8']:.4f}"))
validation.append(dict(name="growth check, max |P−1| (CFG425 R1)", value=float(abs(pdev - r1["pdev"])), limit=5e-3, ok=bool(abs(pdev - r1["pdev"]) < 5e-3), note=f"replay {pdev:.4f} vs CFG425 {r1['pdev']:.4f}"))
for v in validation:
    print(("ok  " if v["ok"] else "FAIL"), v["name"], v["note"])
bad = [v for v in validation if not v["ok"]]
if bad:
    print(f"\n{len(bad)} validation check(s) FAILED; assets are still written and the page prints them as failed.", flush=True)

# ---------------------------------------------------------------- 2. frame images
def enc(a):
    lo, hi = float(a.min()), float(a.max())
    return np.round((a - lo) / max(hi - lo, 1e-12) * 255).astype(np.uint8), [lo, hi]

def atlas(imgs, path):
    rows = -(-len(imgs) // COLS)
    big = np.zeros((rows * NP, COLS * NP), np.uint8)
    for i, im in enumerate(imgs):
        r, c = divmod(i, COLS); big[r * NP:(r + 1) * NP, c * NP:(c + 1) * NP] = im
    Image.fromarray(big).save(path, optimize=True); return os.path.getsize(path)

rng, imgs = {}, {}
for run, tag in (("RES", "res"), ("S0", "s0")):
    e = [enc(fr[run]["slab"][i]) for i in range(F)]
    imgs[tag] = [x[0] for x in e]; rng[tag] = [x[1] for x in e]
swi_imgs = [np.clip(np.round(fr["RES"]["f"][i] * 255), 0, 255).astype(np.uint8) for i in range(F)]
sizes = dict(tl_res=atlas(imgs["res"], os.path.join(OUT, "tl_res.png")), tl_s0=atlas(imgs["s0"], os.path.join(OUT, "tl_s0.png")),
             tl_swi=atlas(swi_imgs, os.path.join(OUT, "tl_swi.png")))

# ---------------------------------------------------------------- 3. one halo, tracked through time
def minimg(d):
    return d - L * np.round(d / L)

def sphere(pos, c, R):
    d = minimg(pos - c); k = (d ** 2).sum(1) < R * R
    return np.flatnonzero(k), d[k]

final = {k: np.load(os.path.join(RP, k, f"pos_{F - 1}.npy")) for k in ("RES", "S0")}
H3, _ = np.histogramdd(final["RES"], bins=(32,) * 3, range=[(0, L)] * 3)
from scipy import ndimage
sm = ndimage.uniform_filter(H3, size=2, mode="wrap")
c = (np.array(np.unravel_index(int(np.argmax(sm)), sm.shape)) + 0.5) * (L / 32)
def shrink(pos, c):
    """shrinking-sphere centre: move to the mean of the particles inside R until the step is below 5 kpc/h."""
    for _ in range(60):
        _, dd = sphere(pos, c, HALO_R); step = dd.mean(0); c = (c + step) % L
        if np.sqrt((step ** 2).sum()) < 0.005:
            break
    return c
c = shrink(final["RES"], c)
ix, d = sphere(final["RES"], c, HALO_R)
cs = shrink(final["S0"], c.copy())
n_s0 = len(sphere(final["S0"], cs, HALO_R)[0])
NHALO = min(NHALO, len(ix))
ids = np.sort(np.random.default_rng(0).choice(ix, NHALO, replace=False))
rel = np.zeros((2, F, NHALO, 3), np.float32)
for ri, run in enumerate(("RES", "S0")):
    for f in range(F):
        rel[ri, f] = minimg(np.load(os.path.join(RP, run, f"pos_{f}.npy"), mmap_mode="r")[ids] - c)
scale = float(np.ceil(np.abs(rel).max() * 1.02))
q = np.clip(np.round(rel / scale * 32767), -32767, 32767).astype("<i2")
q.tofile(os.path.join(OUT, "tl_halo.bin")); sizes["tl_halo"] = q.nbytes
print(f"halo: centre {c.round(1).tolist()}  {len(ix)} particles in the framework run, {n_s0} in the control; tracked {NHALO}; scale {scale} Mpc/h", flush=True)

# ---------------------------------------------------------------- 4. frame table
a = meta["RES"]["a"]
k = np.array(meta["RES"]["k"]); nk = int(np.searchsorted(k, 1.2))
sig = lambda x: [float(f"{v:.6g}") for v in x]
tl = dict(frames=F, n=NP, cols=COLS, a=sig(a), z=[float(f"{1 / x - 1:.5g}") for x in a], k=sig(k[:nk]),
          sigma8=dict(res=sig(meta["RES"]["sigma8"]), s0=sig(meta["S0"]["sigma8"])),
          P=dict(res=[sig(p[:nk]) for p in meta["RES"]["P"]], s0=[sig(p[:nk]) for p in meta["S0"]["P"]]),
          range=dict(res=[[float(f"{x:.6g}") for x in r] for r in rng["res"]], s0=[[float(f"{x:.6g}") for x in r] for r in rng["s0"]]),
          diag=dict(vol_on=[float(d.get("vol_on", 0.0)) for d in meta["RES"]["diag"]], mass_on=[float(d.get("mass_on", 0.0)) for d in meta["RES"]["diag"]]),
          slab_mpc_h=[meta["RES"]["slab"][0] * L / NP, meta["RES"]["slab"][1] * L / NP],
          runtime_s=dict(res=meta["RES"]["runtime_s"], s0=meta["S0"]["runtime_s"]), validation=validation,
          halo=dict(n=NHALO, scale=scale, centre=[float(x) for x in c], n_sphere_res=int(len(ix)), n_sphere_s0=int(n_s0),
                    mass_msun_h=float(len(ix) * M_P), particle_mass_msun_h=float(M_P)),
          bytes=sizes)
json.dump(tl, open(os.path.join(OUT, "timeline.json"), "w"))
print({k: f"{v / 1e6:.2f} MB" for k, v in sizes.items()}, "timeline.json", f"{os.path.getsize(os.path.join(OUT, 'timeline.json')) / 1e3:.0f} kB")
sys.exit(1 if bad else 0)
