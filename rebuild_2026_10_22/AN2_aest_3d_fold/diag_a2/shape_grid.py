"""AN2 diagnostic SG (SHAPE_GRID_NOTE.md): pure-dust shapes A and B against exact dust ellipsoids.
python3 shape_grid.py SHAPE KEY N"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import an2  # noqa: E402


def main(shape, key, N):
    S = an2.build_row(key, 56.6, "canonical", shape, N, 0.05, 8, dust=True)
    S.rf = None
    o = S.run(S.t0, cap=an2.CPU_CAP)
    f = o.get("fold_q") or {}
    r = dict(id="G0", key=key, shape_in=shape, N=N, dust=True, stop=False, kernel="TSC", status=o["status"],
             t_q=f.get("t_Gyr"), z=f.get("z"), shape=f.get("shape"), nstep=o.get("nstep"), cpu_s=o.get("cpu_s"), rss_gb=o.get("rss_gb"))
    print(json.dumps(r), flush=True)
    with open(os.path.join(HERE, "shape_grid.jsonl"), "a") as fh: fh.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
