"""AN2 diagnostic P160 (PRED160_NOTE.md): full-engine shape rows at 160^3, as AN2 S1 rows.
python3 pred160.py SHAPE KEY"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import an2  # noqa: E402


def main(shape, key, N=160):
    S = an2.build_row(key, 56.6, "canonical", shape, N, 0.05, 8)
    o = S.run(S.t0, cap=an2.CPU_CAP)
    f = o.get("fold_q") or {}
    r = dict(id="P160", key=key, shape_in=shape, N=N, status=o["status"], t_q=f.get("t_Gyr"), z=f.get("z"), shape=f.get("shape"),
             nstep=o.get("nstep"), cpu_s=o.get("cpu_s"), rss_gb=o.get("rss_gb"))
    print(json.dumps(r), flush=True)
    with open(os.path.join(HERE, "pred160.jsonl"), "a") as fh: fh.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
