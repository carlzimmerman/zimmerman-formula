"""K2 data checks: hashes vs MANIFEST and sample sizes."""
from crg1_core import *
import sys
import crg1_sparc as SP, crg1_clusters as C

def main():
    man = {}
    for l in open(os.path.join(INP, "MANIFEST.txt")):
        if l.startswith("#"): continue
        f = l.rstrip("\n").split("\t")
        if len(f) >= 3: man[f[0]] = f[2]
    files = []; bad = []
    for root, _, fs in os.walk(INP):
        for n in fs:
            p = os.path.join(root, n); rel = os.path.relpath(p, INP)
            if rel == "MANIFEST.txt" or n == ".DS_Store": continue
            h = sha256(p); files.append((rel, h))
            if man.get(rel) != h: bad.append(rel)
    files.sort()
    write_atomic(os.path.join(HERE, "crg1_input_hashes.txt"), "".join("%s  %s\n" % (h, r) for r, h in files))
    missing = sorted(set(man) - {r for r, _ in files})
    G = SP.load_gal(); T = SP.tilt(G, np.array([0.5] * 175))
    LT = SP.load_lt()
    grp = 0
    for l in open(os.path.join(INP, "groups", "J_A_A_710_L39.tsv")):
        if l.startswith("#"): continue
        f = l.rstrip("\n").split("\t")
        if len(f) >= 13 and f[0].strip().isdigit() and f[1].strip() == "Galaxy group": grp += 1
    D = C.Data(); XC = C.xcop_load()
    nrow = 0
    for c in XC:
        for x in C.XS:
            r = x * c["R500"]
            nrow += all(np.isfinite(v) for v in (C.li(c["hr"], c["hm"], r), C.li(c["gr"], c["gm"], r), C.li(c["sr"], c["sm"], r)))
    rows = list(csv.DictReader(open(os.path.join(INP, "dwarfs", "x1_per_system_inputs.csv"))))
    cl = {}
    for r in rows:
        if r["footing"] == "canonical": cl[r["cls"]] = cl.get(r["cls"], 0) + 1
    ze, zs = len(glob.glob(os.path.join(INP, "zooms", "eta", "*.npz"))), len(glob.glob(os.path.join(INP, "zooms", "shape", "*.npz")))
    got = dict(sparc=len(G), tilt=[T["n_quality"], T["n_lo"], T["n_hi"]], lt=len(LT), groups=grp, clusters=D.N, kt=len(D.I), xcop_rows=nrow, xcop_clusters=len(XC),
               dw_mw_uf=cl["MW ultra-faint"], dw_b31=cl["bright M31"], dw_m31o=cl["M31 others"], dw_mwc=cl["MW classical"], dw_lg=cl["LG field"],
               zooms=[ze, zs], bcg=int(np.isfinite(D.BCGraw).sum()))
    exp = dict(sparc=175, tilt=[153, 47, 53], lt=20, groups=63, clusters=326, kt=106, xcop_rows=35, xcop_clusters=7, dw_mw_uf=31, dw_b31=25, dw_m31o=5, dw_mwc=8, dw_lg=13, zooms=[27, 63], bcg=190)
    res = dict(n_files_hashed=len(files), hash_mismatch=bad, manifest_missing=missing, sizes=got, expected=exp, sizes_ok=got == exp, all_ok=(got == exp and not bad and not missing))
    save_part("k2", res); log(str({k: v for k, v in res.items() if k != "expected"}))
    return res["all_ok"]

if __name__ == "__main__": sys.exit(0 if main() else 1)
