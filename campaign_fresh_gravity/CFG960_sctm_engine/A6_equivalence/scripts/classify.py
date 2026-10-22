import json, sys, glob, os, numpy as np
A, B = sys.argv[1], sys.argv[2]
fa = glob.glob(os.path.join(A, "*lean.json"))[0]; a = json.load(open(fa)); b = json.load(open(os.path.join(B, os.path.basename(fa))))
bk = [x["step"] for x, y in zip(a["book"], b["book"]) if x != y]
ev = [x["step"] for x, y in zip(a["events"], b["events"]) if x != y]
out = dict(book_steps_differing=bk[:5], n_book_diff=len(bk), events_differing=ev[:5])
for s in a["snap"]:
    sa, sb = a["snap"][s], b["snap"][s]
    P = np.array(sa["P"]); Q = np.array(sb["P"]); G = np.array(sa["P_grav"]); H = np.array(sb["P_grav"])
    out[s] = dict(P_identical=bool((P == Q).all()), P_maxrel=float(np.max(np.abs(P / Q - 1))), Pgrav_identical=bool((G == H).all()), Pgrav_maxrel=float(np.max(np.abs(G / H - 1))),
                  sct_identical=sa["sct"] == sb["sct"])
for za in sorted(glob.glob(os.path.join(A, "*.npz"))):
    x = np.load(za); y = np.load(os.path.join(B, os.path.basename(za)))
    out[os.path.basename(za)[-30:]] = {k: bool(x[k].tobytes() == y[k].tobytes()) for k in x.files if k in ("dpart", "dgrav")} or "domains:" + str(all(x[k].tobytes() == y[k].tobytes() for k in x.files))
print(json.dumps(out, indent=0))
