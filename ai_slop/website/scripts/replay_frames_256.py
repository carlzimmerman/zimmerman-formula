"""Replay the CFG424 engine at 256^3 (CFG425 R1 settings, seed 360) and keep frames through time, for the /cosmic-web timeline.

The engine file is imported unchanged (campaign_fresh_gravity/CFG424_turnaround_catchment/cfg424_pm.py); the time loop below is run()'s loop
copied line for line, with capture added. The engine's own diagnostic call (forces(..., diag=True)) overwrites _INC["catch"], which the
following steps then use, so at every extra frame that state is saved and restored. At the engine's own snapshots (z = 1, 0.5, 0) it is
NOT restored, exactly as in the committed run. validate_replay() in build_cosmic_web_replay.py checks sigma8 and P(k) against the committed JSONs.

Usage: CFG424_THREADS=6 python3 replay_frames_256.py RES|S0      (RES = framework run, S0 = Newtonian control; both seed 360, NSEED 256)
Output: _external_data/cosmic_web_replay/<RUN>/ : frames.npz, pos_<k>.npy (all 16.7M particles at each frame), meta.json
"""
import os, sys, json, math, time, importlib.util
RUN = sys.argv[1]
assert RUN in ("RES", "S0")
NP = 256
os.environ.setdefault("CFG424_THREADS", "6")
os.environ["CFG424_FRET"] = "1.0"; os.environ["CFG424_NSEED"] = "256"; os.environ["CFG424_SEED"] = "360"; os.environ["CFG424_NOCOMP"] = "0"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ENGINE = os.path.join(REPO, "campaign_fresh_gravity", "CFG424_turnaround_catchment", "cfg424_pm.py")
OUT = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cosmic_web_replay", RUN))
os.makedirs(OUT, exist_ok=True)
spec = importlib.util.spec_from_file_location("cfg424_pm", ENGINE); eng = importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)
eng.RC = 0.0; eng.MIX = "MIXA"; eng.FRETX = 1.0                  # as run_425.py launches it: RES FLAT canonical 256 0 MIXA
try:
    os.nice(10)
except OSError:
    pass

switch, branch, foot = RUN, "FLAT", "canonical"
Z0, Z1 = 112, 144                                                 # slab of the projected images: z cells 112..143 of 256 (87.5-112.5 Mpc/h)
mesh = eng.Mesh(NP); dta = eng.dta_table(); t0 = time.time()
pos, mom = eng.initial_conditions(NP, 1.0)
aa = eng.step_grid()
SNAP_IDX = {int(np.argmin(np.abs(aa - x))): nm for x, nm in ((0.5, "z1"), (2 / 3, "z0.5"), (1.0, "z0"))}       # the engine's own snapshots
CAP = sorted(set([0] + list(range(6, 124, 6)) + [123, 128, 134, 140, 146, 150]) | set(SNAP_IDX))
rec = {"a": [], "k": [], "P": [], "sigma8": [], "diag": []}; slab = []; fsl = []; engine_snap = {}

def capture(idx, a, delta):
    kb, pb, s8 = eng.measure_pk(mesh, delta, NP ** 3)
    rec["a"].append(float(a)); rec["P"].append(pb); rec["sigma8"].append(s8)
    if not rec["k"]:
        rec["k"] = kb
    slab.append(np.log10(np.maximum(1.0 + delta[:, :, Z0:Z1].mean(axis=2), 1e-3)).astype(np.float32))
    d = {}
    if switch == "RES":
        keep = eng._INC["catch"]
        _, info = eng.forces(mesh, delta, a, switch, branch, foot, dta, diag=True)
        fsw = info.pop("_grids")[0]
        fsl.append(fsw[:, :, Z0:Z1].mean(axis=2).astype(np.float32))
        d = {k: v for k, v in info.items() if isinstance(v, float)}
        if idx not in SNAP_IDX:
            eng._INC["catch"] = keep                               # restore: the committed run does not call diag at this step
    rec["diag"].append(d)
    np.save(os.path.join(OUT, f"pos_{len(rec['a']) - 1}.npy"), pos.astype(np.float32))
    if idx in SNAP_IDX:
        engine_snap[SNAP_IDX[idx]] = dict(a=float(a), sigma8=s8, k=kb, P=pb)
    print(f"  [{RUN}] frame {len(rec['a']) - 1:2d} step {idx:3d} a={a:.4f} sigma8={s8:.4f} t={time.time() - t0:.0f}s", flush=True)

delta = mesh.deposit(pos)
if switch == "RES":                                                # run() calls snapshot("zi") first: a diag call at AI
    eng.forces(mesh, delta, eng.AI, switch, branch, foot, dta, diag=True)
capture(0, eng.AI, delta)
acc, _ = eng.forces(mesh, delta, eng.AI, switch, branch, foot, dta); accp = mesh.interp(acc, pos); del acc
for n in range(len(aa) - 1):
    a0, a1 = aa[n], aa[n + 1]; am = math.sqrt(a0 * a1)
    mom += eng.quad(lambda x: 1 / (x * x * eng.E(x)), a0, am)[0] * accp
    pos = (pos + eng.quad(lambda x: 1 / (x ** 3 * eng.E(x)), a0, a1)[0] * mom) % eng.L
    delta = mesh.deposit(pos); acc, _ = eng.forces(mesh, delta, a1, switch, branch, foot, dta)
    accp = mesh.interp(acc, pos); del acc
    mom += eng.quad(lambda x: 1 / (x * x * eng.E(x)), am, a1)[0] * accp
    if n + 1 in CAP:
        capture(n + 1, a1, delta)
        if n + 1 in SNAP_IDX and switch == "RES":
            pass                                                   # engine snapshot: its diag call already ran inside capture() without restore

np.savez_compressed(os.path.join(OUT, "frames.npz"), slab=np.array(slab), f=np.array(fsl) if fsl else np.zeros(0), a=np.array(rec["a"]))
json.dump(dict(run=RUN, np=NP, seed=360, L=eng.L, z_i=eng.ZI, nsteps=len(aa) - 1, slab=[Z0, Z1], runtime_s=time.time() - t0, **rec, engine_snap=engine_snap),
          open(os.path.join(OUT, "meta.json"), "w"))
print(f"[{RUN}] done in {time.time() - t0:.0f}s", flush=True)
