"""LAM7: stream the rest of KU2's MaNGA cubes through LAM4's integrate() unchanged (criteria f10b6db28c).
Run: python3 -I lam7_stream.py [NWORKERS]. Resumable; each worker single thread. kappa = 1/2 FITTED; not theory closed."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); EXT = os.path.join(os.path.dirname(RB), "_external_data")
sys.path.insert(0, os.path.join(RB, "LAM4_whole_galaxy_absorption")); import lam4_stream as L4
L4.OUTD = os.path.join(EXT, "lam7_integrated_2026_11_04"); L4.TMP = os.path.join(EXT, "lam7_cube_tmp")
os.makedirs(L4.OUTD, exist_ok=True); os.makedirs(L4.TMP, exist_ok=True)
def work(row): return L4.work(row)
def draw():
    fn = os.path.join(HERE, "lam7_sample.csv")
    if os.path.exists(fn): return [l.strip().split(",") for l in open(fn).readlines()[1:]]
    import numpy as np; from astropy.io import fits
    ku2 = os.path.join(RB, "KU2_kappa_universality_model_choice", "ku2.py"); argv = sys.argv; sys.argv = ["ku2.py"]
    K = {"__file__": ku2, "__name__": "ku2"}; exec(compile(open(ku2).read().split("ok1 = slow.sum()")[0], "ku2.py", "exec"), K); sys.argv = argv
    done = {int(l.split(",")[2]) for l in open(os.path.join(RB, "LAM4_whole_galaxy_absorption", "lam4_sample.csv")).readlines()[1:]}
    dp = fits.open(L4.DP)[1].data; rows = [int(r) for r in np.flatnonzero(K["sel"]) if int(r) not in done]
    rows = [rows[i] for i in np.random.default_rng(20261104).permutation(len(rows))]; out = []
    with open(fn, "w") as fo:
        fo.write("order,unused,dynpop_row,plateifu,unused2\n")
        for o, r in enumerate(rows): out.append([str(o), "", str(r), dp["plateifu"][r].strip(), ""]); fo.write(",".join(out[-1]) + "\n")
    return out
if __name__ == "__main__":
    rows = draw(); n = int(sys.argv[1]) if len(sys.argv) > 1 else 20; print(f"new sample {len(rows)}; workers {n}", flush=True)
    from concurrent.futures import ProcessPoolExecutor
    log = open(os.path.join(HERE, "lam7_stream.log"), "a")
    with ProcessPoolExecutor(n) as ex:
        for k, (pifu, st) in enumerate(ex.map(work, rows)):
            log.write(f"{pifu},{st}\n"); log.flush()
            if (k + 1) % 100 == 0: print(k + 1, "processed", flush=True)
    print("done", flush=True)
