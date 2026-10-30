#!/usr/bin/env python3
"""CB1 Part B data step: per box, fetch the SubLink tree and the z=0 catalog, verify the row mapping, keep the counts, delete the files.

Frozen criteria: FROZEN_CRITERIA.md (53735de87f). Light (one thread, one box on disk at a time). Each box is appended to a checkpoint, so a stop loses at most one box.

    DREAMS_AUTH_DIR=<dir with dreams_get.py + token> python3 cb1_fetch.py <scratch_dir> check   -> K5 on boxes 0, 3, 1000: walk vs the authors' recursion
    DREAMS_AUTH_DIR=<dir with dreams_get.py + token> python3 cb1_fetch.py <scratch_dir> all     -> cb1_counts.jsonl (resumes), then cb1_counts.npz
"""
import json, os, sys
import numpy as np, h5py

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.environ["DREAMS_AUTH_DIR"])
import dreams_get
from cb1_part_b import extract_box, walk, REMOVED, H

ROOT = "/FOF_Subfind/WDM/MW_zooms/SB4"
T = np.loadtxt(os.path.join(HERE, "authors_code", "WDM_TNG_MW_SB4_parameters.txt")); BOXES = [b for b in range(1024) if b not in REMOVED]
CK = os.path.join(HERE, "cb1_counts.jsonl"); TOL = 6e-5     # BlackHoleFeedbackFactor is stored to 5 decimals, so /0.1 rounds by up to 5e-5

def authors_recursion(path):
    """merger_tree_script.py walk_tree, same visiting order, in memory. Root found as get_MW_idx + nearest FirstSubhaloInFOFGroupID."""
    with h5py.File(path, "r") as t:
        sn = np.array(t["SnapNum"]); sid = np.array(t["SubhaloID"]); fp = np.array(t["FirstProgenitorID"]); np_ = np.array(t["NextProgenitorID"])
        fs = np.array(t["FirstSubhaloInFOFGroupID"]); m = np.array(t["GroupMassType"]) * 1e10 / H
    tot = m.sum(1); con = m[:, 2] / tot; cut = (tot > 7e11) & (tot < 2.5e12) & (sn == 90)
    mw = np.arange(len(sn))[cut][np.argmin(con[cut])]
    z0 = np.arange(len(sn))[sn == 90]; root = z0[np.argmin(np.abs(fs[z0] - fs[mw]))]; rid = sid[root]; seen = [root]; init = [root]
    n = np_[root]
    while n != -1:
        i = root + (n - rid); seen.append(i); init.append(i); n = np_[i]
    def go(index):
        f = fp[index]
        while f != -1:
            k = root + (f - rid); seen.append(k); q = np_[k]
            while q != -1:
                j = root + (q - rid); seen.append(j); go(j); q = np_[j]
            f = fp[k]
    sys.setrecursionlimit(100000)
    for i in init: go(i)
    return np.array(seen), sn

def fetch(b, d, tok):
    os.makedirs(d, exist_ok=True); tree = os.path.join(d, f"t{b}.hdf5"); tab = os.path.join(d, f"c{b}.hdf5")
    dreams_get.get(f"{ROOT}/box_{b}/tree_extended.hdf5", tree, tok); dreams_get.get(f"{ROOT}/box_{b}/fof_subhalo_tab_090.hdf5", tab, tok)
    return tree, tab

def mapping(b, tab):
    a = h5py.File(tab, "r")["Parameters"].attrs; r = T[BOXES.index(b)]
    got = np.array([a["WindEnergyIn1e51erg"] / 3.6, a["VariableWindVelFactor"] / 7.4, a["BlackHoleFeedbackFactor"] / 0.1])
    return float(np.abs(got - r[1:]).max())

def main():
    d, mode = sys.argv[1], sys.argv[2]; tok = dreams_get.token()
    if mode == "check":
        for b in (0, 3, 1000):
            tree, tab = fetch(b, d, tok); s, sn = authors_recursion(tree); r = extract_box(tree)
            same = len(s) == r["N"] and np.array_equal(np.bincount(sn[s], minlength=91)[:91], r["counts"]) and len(set(s.tolist())) == len(s)
            print(f"K5 box {b}: authors' recursion N {len(s)}, ours {r['N']}, unique {len(set(s.tolist()))}, per-snapshot equal {same}; main branch {r['main']}; mapping max diff {mapping(b, tab):.1e}", flush=True)
            os.remove(tree); os.remove(tab)
            if not same: return 1
        return 0
    done = {json.loads(l)["box"] for l in open(CK)} if os.path.exists(CK) else set()
    with open(CK, "a") as out:
        for n, b in enumerate(BOXES):
            if b in done: continue
            tree, tab = fetch(b, d, tok); diff = mapping(b, tab)
            if diff > TOL: print(f"MAPPING FAIL box {b}: {diff}", flush=True); return 1
            r = extract_box(tree); os.remove(tree); os.remove(tab)
            out.write(json.dumps(dict(box=b, N=r["N"], main=r["main"], counts=r["counts"].tolist(), mdm=r["mdm"].tolist(), map_diff=diff)) + "\n"); out.flush()
            if n % 50 == 0: print(n, b, r["N"], flush=True)
    R = {x["box"]: x for x in map(json.loads, open(CK))}; R = [R[b] for b in BOXES]
    np.savez(os.path.join(HERE, "cb1_counts.npz"), y=T[:, 0], box=np.array(BOXES), N=np.array([x["N"] for x in R]), counts=np.array([x["counts"] for x in R]), mdm=np.array([x["mdm"] for x in R]), main=np.array([x["main"] for x in R]))
    print("all", len(R), "max mapping diff", max(x["map_diff"] for x in R), flush=True); return 0

if __name__ == "__main__":
    sys.exit(main())
