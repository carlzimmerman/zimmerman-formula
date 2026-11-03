"""MB1 check K6: arm K unchanged, plus a log of units on the keys path. On the first call per cluster it reads the caller's
pp_["Mb"] (the harness's own baryon mass) and compares gb r^2 / G at r500 with it. Writes k6_probe.jsonl. kappa = 1/2 FITTED."""
import inspect, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mb1_core as C
NAME = "MB1 K6 probe"; VERTICAL = ("R",); TRAINED_ON = ("xcop",)
SEEN = set(); LOG = os.path.join(HERE, "k6_probe.jsonl")
def g(Q):
    if "S" in Q:
        r5 = float(np.ravel(Q["r500"])[0]); k =(round(r5, 3), float(Q["a0"]), os.environ.get("X73_FSTAR", ""))
        if k not in SEEN:
            SEEN.add(k); f = inspect.currentframe().f_back; pp = f.f_locals.get("pp_"); r = np.asarray(Q["r"], float); gb = np.asarray(Q["gb"], float)
            mine = float(np.interp(r5, r, gb * r * r / C.G)); theirs = float(np.interp(r5, r, np.asarray(pp["Mb"], float))) if pp is not None else float("nan")
            with open(LOG, "a") as o: o.write(json.dumps(dict(r500_Mpc=r5 / 3.0857e22, a0=float(Q["a0"]), fstar=k[2], Mb500_from_g=mine / C.MS, Mb500_harness=theirs / C.MS, ratio=mine / theirs, GE=f.f_globals.get("GE"))) + "\n")
    return C.g(Q, "K")
