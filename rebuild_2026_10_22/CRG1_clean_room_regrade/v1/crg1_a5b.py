"""A5(b): one CODATA set on every path, all lines. Reported, not graded."""
from crg1_core import *
import shutil, subprocess, sys
assert ONESET
for f in ("zoom_eta", "zoom_shape_info", "efe_canonical", "efe_alt"):
    shutil.copy(os.path.join(HERE, "partials", f + ".json"), PART)
for f in ("shape_stacks.npz", "efe_canonical.npz", "efe_alt.npz"):
    shutil.copy(os.path.join(HERE, "cache", f), CACHE)
for s in ("crg1_sparc.py", "crg1_clusters.py", "crg1_groups.py", "crg1_lens.py", "crg1_dwarfs.py"):
    subprocess.run([sys.executable, s], check=True, capture_output=True, env=os.environ)
K = load_part("K_C1")["f0.034_g0.005"]; K4 = load_part("K_C4")["canonical"]; K2 = load_part("K_C2")
X = load_part("X_all"); G = load_part("G"); D = load_part("Dw")
def sum_(n):
    r = load_part(n)["rows"]
    return {t: dict(rms=v["S"]["rms"], Y_med=v["S"]["Y_med"], tilt=v["Tl"]["tilt"], LT=v["LT"]) for t, v in r.items()}
res = dict(note="A5(b): reported, not graded", S_Tl_LT={c: sum_("sparc_%s_canonical" % c) for c in ("C1", "C2", "C3", "C4")},
           K=dict(C1=dict(n_pass=K["n_pass"], failing=K["failing"], Z={h: {k: v["Z"] for k, v in t.items()} for h, t in K["tables"].items()}),
                  C2=dict(n_pass=K2["n_pass"], failing=K2["failing"]), C4=dict(n_pass=K4["n_pass"], failing=K4["failing"])),
           X=dict(C1=dict(mean=X["C1_f0.034"]["mean"], rms=X["C1_f0.034"]["rms"]), C2=dict(mean=X["C2_f0.034"]["mean"], rms=X["C2_f0.034"]["rms"])),
           G={c: G[c]["canonical"]["Z"] for c in ("C1", "C3", "C4")}, Dw={c: {k: v["Z"] for k, v in D[c]["canonical"]["classes"].items()} for c in ("C1", "C3", "C4")})
write_atomic(os.path.join(HERE, "crg1_results_A5b_oneset.json"), dumps(res) + "\n")
