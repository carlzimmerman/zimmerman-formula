#!/usr/bin/env python3
"""CB1 Part C data step: per box, walk the tree as the authors do; keep SnapNum and each node's descendant position only; delete the file. Light; resumes.

    DREAMS_AUTH_DIR=<dir with dreams_get.py + token> python3 cb1_graphs_fetch.py <scratch_dir> <out.npz>
"""
import os, sys
import numpy as np, h5py
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.environ["DREAMS_AUTH_DIR"])
import dreams_get
from cb1_fetch import ROOT, BOXES, authors_recursion

def authors_get_edges(subid, desid):       # graph_script.py get_edges, test == "normal", verbatim logic
    desid_to_idx = {}
    for j, did in enumerate(desid): desid_to_idx[did] = j
    s, e = [], []
    for i, sid in enumerate(subid):
        if sid in desid_to_idx:
            s.append(i); e.append(desid_to_idx[sid])
    return np.array([s, e], dtype=np.int64)

def one(path):
    idx, sn = authors_recursion(path)
    with h5py.File(path, "r") as t: sid = np.array(t["SubhaloID"])[idx]; des = np.array(t["DescendantID"])[idx]
    pos = {int(v): i for i, v in enumerate(sid)}
    d = np.array([pos.get(int(x), -1) for x in des], dtype=np.int32)
    return sn[idx].astype(np.uint8), d, authors_get_edges(sid, des).shape[1]

if __name__ == "__main__":
    d, out = sys.argv[1], sys.argv[2]; os.makedirs(d, exist_ok=True); part = out + ".parts"; os.makedirs(part, exist_ok=True); tok = dreams_get.token()
    for n, b in enumerate(BOXES):
        f = os.path.join(part, f"{b}.npz")
        if os.path.exists(f): continue
        tree = os.path.join(d, f"g{b}.hdf5"); dreams_get.get(f"{ROOT}/box_{b}/tree_extended.hdf5", tree, tok); sn, de, ne = one(tree); os.remove(tree)
        tmp = f + ".tmp.npz"; np.savez(tmp, sn=sn, de=de, ne=ne); os.replace(tmp, f)
        if n % 100 == 0: print(n, b, len(sn), ne, flush=True)
    A = [np.load(os.path.join(part, f"{b}.npz")) for b in BOXES]; L = np.array([len(a["sn"]) for a in A])
    np.savez_compressed(out, box=np.array(BOXES), n=L, ne=np.array([int(a["ne"]) for a in A]), sn=np.concatenate([a["sn"] for a in A]), de=np.concatenate([a["de"] for a in A]))
    print("done", L.sum(), flush=True)
