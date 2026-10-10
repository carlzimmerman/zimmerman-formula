#!/usr/bin/env python3
"""CFG555 heavy stage (FROZEN_CRITERIA.md): for each run's saved z = 0 state, call the run's OWN engine `forces` (diag = True, imported
unchanged, the run's own settings), capture the total potential from the three acceleration transforms (CFG526 method), and measure P(k), sigma8
of the particle density and of the GRAVITATING density delta_grav = -k^2 phi_k / (1.5 Om) (a = 1).  Small per-run caches (spectra + diagnostics,
no fields) go to ../_external_data/cfg555_work/.  Read-only use of every other lane's files.
  nice -n 10 python3 cfg555_compute.py [RUN ...]      (default: every run; 512^3 runs are processed one at a time, serially)
  python3 cfg555_compute.py --list"""
import os, sys, json, time, math, importlib.util
NTH = int(os.environ.get("CFG555_THREADS", "8"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = str(NTH)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
WORK = os.path.join(EXT, "cfg555_work")
E424 = os.path.join(CFG, "CFG424_turnaround_catchment", "cfg424_pm.py")
E518 = os.path.join(CFG, "CFG518_depletion_consistent_growth", "cfg518_pm.py")
E527 = os.path.join(CFG, "CFG527_law_respecting_engine", "cfg527_pm.py")
W424, W518, W527, W530 = (os.path.join(EXT, d) for d in ("cfg424_work", "cfg518_work", "cfg527_work", "cfg530_work"))
S0_359 = os.path.join(EXT, "cfg359_work", "cfg359_S0_FLAT_canonical_N256")
S0_411 = lambda s: os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N256" + (f"_seed{s}" if s != 359 else "")) if s != 512 else \
    os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512")
S0_424_512_360 = os.path.join(W424, "cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360")

def r424(br, ft, N, mix="MIXA", seed=359, eps=None, nocomp=False):
    tag = f"RES_TA{'_NOCOMP' if nocomp else ''}_{mix}_MASSCONS_fret1_{br}_{ft}_N{N}" + (f"_seed{seed}" if seed != 359 else "") + (f"_eps{eps:g}" if eps else "")
    env = {"EPS": str(eps) if eps else "0.077", "NOCOMP": "1" if nocomp else "0", "FRET": "1.0", "SEED": str(seed)}
    return dict(engine=E424, pre="CFG424", env=env, mix=mix, switch="RES", branch=br, foot=ft, N=N, base=os.path.join(W424, f"cfg424_{tag}"))
def r518(ft, N, mode="census", nocomp=False):
    tag = f"RES_TA{'_NOCOMP' if nocomp else ''}_MIXA_MASSCONS_fret{mode}_FLAT_{ft}_N{N}"
    return dict(engine=E518, pre="CFG518", env={"FRET_MODE": mode, "NOCOMP": "1" if nocomp else "0"}, mix="MIXA", switch="RES", branch="FLAT",
                foot=ft, N=N, base=os.path.join(W518, f"cfg518_{tag}"))
def r527(ft, N=256, nocomp=False, base=None):
    tag = f"RES_TA{'_NOCOMP' if nocomp else ''}_NOFILT_MASSCONS_fretcensus_FLAT_{ft}_N{N}_drawSHELL"
    return dict(engine=E527, pre="CFG527", env={"FRET_MODE": "census", "NOCOMP": "1" if nocomp else "0", "DRAW": "SHELL", "L": "200", "RMIN": "1.56"},
                mix="NOFILT", switch="RES", branch="FLAT", foot=ft, N=N, base=base or os.path.join(W527, f"cfg527_{tag}"))

# name -> (spec, matched S0 base path [JSON = base + '.json'])
RUNS = {
    "424_TAcan": (r424("FLAT", "canonical", 256), S0_359),
    "424_TAalt": (r424("FLAT", "alt", 256), S0_359),
    "424_MUTATE_nocomp": (r424("FLAT", "canonical", 256, nocomp=True), S0_359),
    "425_R1_can_s360": (r424("FLAT", "canonical", 256, seed=360), S0_411(360)),
    "425_R2_can_s361": (r424("FLAT", "canonical", 256, seed=361), S0_411(361)),
    "426_D1_DEcan": (r424("DE", "canonical", 256), S0_359),
    "426_D2_DEalt": (r424("DE", "alt", 256), S0_359),
    "426_A1_alt_s360": (r424("FLAT", "alt", 256, seed=360), S0_411(360)),
    "426_A2_alt_s361": (r424("FLAT", "alt", 256, seed=361), S0_411(361)),
    "427_E1_eps0.0385": (r424("FLAT", "canonical", 256, eps=0.0385), S0_359),
    "427_E2_eps0.154": (r424("FLAT", "canonical", 256, eps=0.154), S0_359),
    "427_G1_MIXB": (r424("FLAT", "canonical", 256, mix="MIXB"), S0_359),
    "427_G2_HOT1": (r424("FLAT", "canonical", 256, mix="HOT1"), S0_359),
    "518_DCcan": (r518("canonical", 256), S0_359),
    "518_DCalt": (r518("alt", 256), S0_359),
    "518_MUTATE_nocomp": (r518("canonical", 256, nocomp=True), S0_359),
    "518_K1_fretone": (r518("canonical", 256, mode="one"), S0_359),
    "527_LRcan_L200": (r527("canonical"), S0_359),
    "527_LRalt_L200": (r527("alt"), S0_359),
    "527_MUTB_nocomp_L200": (r527("canonical", nocomp=True), S0_359),
    "530_LRcan_L200_N256_rebuild": (r527("canonical", base=os.path.join(W530, "runs", "LRcan_L200_N256",
                                         "cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_canonical_N256_drawSHELL")),
                                    os.path.join(W530, "runs", "S0_L200_N256", "cfg527_S0_TA_NOFILT_MASSCONS_fretcensus_FLAT_canonical_N256_drawSHELL")),
    # 512^3 (one at a time)
    "425_R3_can_512": (r424("FLAT", "canonical", 512), S0_411(512)),
    "439_A_alt_512": (r424("FLAT", "alt", 512), S0_411(512)),
    "439_B_DEcan_512": (r424("DE", "canonical", 512), S0_411(512)),
    "460_can_512_s360": (r424("FLAT", "canonical", 512, seed=360), S0_424_512_360),
    "518_DCcan_512": (r518("canonical", 512), S0_411(512)),
}
# S0 states (capture control C2; gravitating = particles)
S0RUNS = {"S0_359_N256": dict(engine=E424, pre="CFG424", env={}, mix="MIXA", switch="S0", branch="FLAT", foot="canonical", N=256, base=S0_359)}

def load_engine(spec):
    pre = spec["pre"]
    for k in list(os.environ):
        if k.startswith(pre + "_"): del os.environ[k]
    os.environ.update({f"{pre}_{k}": v for k, v in spec["env"].items()})
    os.environ[f"{pre}_THREADS"] = str(NTH)
    sp = importlib.util.spec_from_file_location(f"eng_{pre}_{time.time_ns()}", spec["engine"]); mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    mod.RC = 0.0; mod.MIX = spec["mix"]; mod.NTH = NTH
    return mod

def pk_split(mod, mesh, dp, ds):
    """reported-only variant: CIC window deconvolved from the particle part only (ds is a mesh field). Binning = engine measure_pk."""
    M, L = mesh.M, mod.L
    W = 1.0
    for kv in mesh.kvec:
        W = W * np.sinc(kv * mesh.dx / (2 * np.pi)) ** 2
    dk = mesh.fwd(dp) / W + (mesh.fwd(ds) if ds is not None else 0.0)
    pk3 = (np.abs(dk) ** 2) * L ** 3 / M ** 6
    kk = np.sqrt(mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2)
    wt = np.full(dk.shape, 2.0, np.float32); wt[..., 0] = 1.0
    if M % 2 == 0: wt[..., -1] = 1.0
    wt[0, 0, 0] = 0.0
    kf = 2 * np.pi / L; edges = np.arange(0.5, M // 2 + 1, 1.0) * kf
    ib = np.digitize(kk.ravel(), edges); wv = wt.ravel()
    nb = np.bincount(ib, weights=wv, minlength=len(edges) + 1)
    sp = np.bincount(ib, weights=wv * pk3.ravel(), minlength=len(edges) + 1)
    ok = nb[1:len(edges)] > 0
    pb = (sp[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]
    x = (kk * 8.0).astype(np.float64); x = np.where(x > 0, x, 1e-3)
    s8 = math.sqrt(float(np.sum(wt * pk3 * (3 * (np.sin(x) - x * np.cos(x)) / x ** 3) ** 2)) / L ** 3)
    return pb.tolist(), s8

def compute(name, spec, s0base=None, force=False):
    out = os.path.join(WORK, f"cfg555_{name}.json")
    if os.path.exists(out) and not force:
        print("cached", name, flush=True); return
    if not os.path.exists(spec["base"] + "_z0.npz"):
        json.dump({"name": name, "missing": spec["base"] + "_z0.npz"}, open(out, "w")); print("MISSING", name, flush=True); return
    t0 = time.time()
    mod = load_engine(spec)
    js = json.load(open(spec["base"] + ".json"))["snap"]["z0"]
    mesh = mod.Mesh(spec["N"]); dta = mod.dta_table()
    pos = np.load(spec["base"] + "_z0.npz")["pos"].astype(np.float64)
    npart = pos.shape[0]; delta = mesh.deposit(pos); del pos
    rec = []; inv0 = mesh.inv
    def inv_rec(xk):
        rec.append(xk); del rec[:-3]
        return inv0(xk)
    mesh.inv = inv_rec
    _, info = mod.forces(mesh, delta, 1.0, spec["switch"], spec["branch"], spec["foot"], dta, diag=True)
    mesh.inv = inv0
    info.pop("_grids", None)
    num = sum(kv * x for kv, x in zip(mesh.kvec, rec)); del rec                      # = 1j k^2 phik
    dgk = (-num / (1j * 1.5 * mod.Om)).astype(np.complex64); del num                # -k^2 phik / (1.5 Om), a = 1
    dgk[0, 0, 0] = 0
    dgrav = mesh.inv(dgk); del dgk
    dsrc = (dgrav - delta).astype(np.float32)
    kb, pb, s8 = mod.measure_pk(mesh, delta, npart)
    _, pg, s8g = mod.measure_pk(mesh, dgrav, npart)
    pgs, s8gs = pk_split(mod, mesh, delta, dsrc)                                       # reported only
    pps, s8ps = pk_split(mod, mesh, delta, None)                                       # == engine measure_pk on particles (check)
    _, psrc, s8src = mod.measure_pk(mesh, dsrc, npart)
    shared = {}
    for k_, v in info.items():
        if k_ in js and isinstance(v, (int, float)) and not isinstance(v, bool) and k_ != "t":
            shared[k_] = [float(v), float(js[k_])]
    res = dict(name=name, base=os.path.relpath(spec["base"], EXT), engine=os.path.relpath(spec["engine"], CFG), N=spec["N"], foot=spec["foot"],
               branch=spec["branch"], mix=spec["mix"], env=spec["env"], switch=spec["switch"],
               k=kb, P_part=pb, s8_part=s8, P_grav=pg, s8_grav=s8g, P_grav_splitdeconv=pgs, s8_grav_splitdeconv=s8gs,
               P_part_splitfn=pps, s8_part_splitfn=s8ps, P_src=psrc, s8_src=s8src,
               P_part_json=js["P"], s8_part_json=js["sigma8"], shared_diag=shared,
               mean_grav_minus_p=float(dsrc.astype(np.float64).mean()), src_rms=float(dsrc.astype(np.float64).std()),
               src_min=float(dsrc.min()), src_max=float(dsrc.max()), part_max=float(delta.max()),
               s0_base=os.path.relpath(s0base, EXT) if s0base else None, runtime_s=time.time() - t0)
    if spec["switch"] == "S0":
        res["s0_maxdiff_rel"] = float(np.abs(dsrc).max() / (1.0 + float(delta.max())))
        c = 0.05                                                                      # C2: inject (1 + c) delta into the S0 capture path
        rec = []
        mesh.inv = inv_rec
        mod.forces(mesh, ((1 + c) * delta).astype(np.float32), 1.0, "S0", "FLAT", "canonical", dta, diag=False)
        mesh.inv = inv0
        num = sum(kv * x for kv, x in zip(mesh.kvec, rec)); dgk = (-num / (1j * 1.5 * mod.Om)).astype(np.complex64); dgk[0, 0, 0] = 0
        _, pc, _ = mod.measure_pk(mesh, mesh.inv(dgk), npart)
        rr = np.array(pc) / np.array(pb); m = np.array(kb) <= 1.0
        res["C2_inject_ratio_dev"] = float(np.max(np.abs(rr[m] - (1 + c) ** 2)))
        # C1: synthetic fixed-amplitude random-phase field with P_syn = 0.05 P_S0(k) (bin-wise exact by construction)
        rng = np.random.default_rng(555)
        kk = np.sqrt(mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2)
        W = 1.0
        for kv in mesh.kvec: W = W * np.sinc(kv * mesh.dx / (2 * np.pi)) ** 2
        Ptarget = 0.05 * np.interp(kk, np.array(kb), np.array(pb))
        amp = np.sqrt(Ptarget * mesh.M ** 6 / mod.L ** 3) * W                       # measure_pk divides by W^2
        wk = mesh.fwd(rng.standard_normal((mesh.M,) * 3).astype(np.float32))       # hermitian-consistent random phases
        ph = wk / np.maximum(np.abs(wk), 1e-30); del wk
        amp[0, 0, 0] = 0.0
        syn = mesh.inv((amp * ph).astype(np.complex64))
        # recover: expected bin power = bin mean of |FFT(syn)|^2 L^3/M^6/W^2 computed directly -> compare with interp target averaged in bins
        _, psyn, _ = mod.measure_pk(mesh, syn, npart)
        # reference: same binning applied to the declared target on the realised (hermitian-projected) modes
        sk = mesh.fwd(syn); ptrue3 = (np.abs(sk) ** 2) * mod.L ** 3 / mesh.M ** 6 / W ** 2
        kf = 2 * np.pi / mod.L; edges = np.arange(0.5, mesh.M // 2 + 1, 1.0) * kf
        wt = np.full(sk.shape, 2.0, np.float32); wt[..., 0] = 1.0; wt[..., -1] = 1.0; wt[0, 0, 0] = 0.0
        ib = np.digitize(kk.ravel(), edges); nb = np.bincount(ib, weights=wt.ravel(), minlength=len(edges) + 1)
        tb = np.bincount(ib, weights=(wt * Ptarget).ravel(), minlength=len(edges) + 1)[1:len(edges)] / np.maximum(nb[1:len(edges)], 1)
        tb = tb[nb[1:len(edges)] > 0]
        inner = (np.array(kb) <= 0.5 * math.pi * mesh.M / mod.L)                     # away from the Nyquist planes (hermitian projection)
        res["C1_syn_recovery_maxrel"] = float(np.max(np.abs(np.array(psyn)[inner] / tb[inner] - 1)))
        res["C1_syn_recovery_maxrel_k_le_1"] = float(np.max(np.abs(np.array(psyn)[m] / tb[m] - 1)))
        del ptrue3, sk
    json.dump(res, open(out, "w"))
    print(f"done {name} {time.time() - t0:.0f}s s8 part {s8:.5f} grav {s8g:.5f}  shared q_max {shared.get('q_max')}", flush=True)

if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    if "--list" in sys.argv:
        for n in list(S0RUNS) + list(RUNS): print(n)
        sys.exit(0)
    try: os.nice(10)
    except OSError: pass
    force = "--force" in sys.argv
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or (list(S0RUNS) + list(RUNS))
    for n in want:
        if n in S0RUNS: compute(n, S0RUNS[n], force=force)
        else: compute(n, RUNS[n][0], RUNS[n][1], force=force)
