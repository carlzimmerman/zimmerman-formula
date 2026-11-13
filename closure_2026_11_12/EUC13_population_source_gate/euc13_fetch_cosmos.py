#!/usr/bin/env python3
"""EUC13: fetch COSMOS2020 Classic (Weaver+2022, VizieR J/ApJS/258/11/classic) columns HSCimagAuto, lpzBEST,
FlagCOMBINED from the CfA VizieR ASU mirror (TAP did not answer before freezing), in magnitude slices, one paced
stream (>= 2 s apart), generic User-Agent; then aggregate to counts N(i, z) (frozen criteria sec. 2, M3 step 2).

  python3 -I euc13_fetch_cosmos.py --out-dir <_external_data/euc13_population_gate> --agg euc13_cosmos2020_counts.csv

Raw slices stay under --out-dir (untracked) with MANIFEST.txt; only the aggregate is written beside this script.
"""
import argparse, csv, datetime, hashlib, os, sys, time, urllib.parse, urllib.request
import numpy as np

ASU = "https://vizier.cfa.harvard.edu/viz-bin/asu-tsv"
UA = "python-asu-client/1.0"
SLICES = [(10.0, 21.0), (21.0, 22.0), (22.0, 23.0), (23.0, 24.0), (24.0, 24.5), (24.5, 25.0), (25.0, 25.5),
          (25.5, 26.0), (26.0, 26.5), (26.5, 27.0), (27.0, 27.5), (27.5, 28.0)]
IEDGE = np.round(np.arange(16.0, 28.0001, 0.1), 2)
ZEDGE = np.round(np.arange(0.0, 6.0001, 0.05), 3)

def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()

def fetch(lo, hi, path):
    q = [("-source", "J/ApJS/258/11/classic"), ("-out", "HSCimagAuto,lpzBEST,FlagCOMBINED"), ("-out.max", "unlimited"),
         ("HSCimagAuto", "%.2f..%.2f" % (lo, hi)), ("FlagCOMBINED", "=0")]
    url = ASU + "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        data = r.read()
    open(path, "wb").write(data)
    return url, len(data), time.time() - t0

def valid(path):
    """a slice is valid if it carries the table's column header, no error report, and a footer-free body"""
    txt = open(path, encoding="latin-1").read()
    return ("#Column\tFlagCOMBINED" in txt) and ("Error=" not in txt) and ("QUERY_STATUS=ERROR" not in txt)

def parse(path):
    I, Z = [], []
    for line in open(path, encoding="latin-1"):
        if line.startswith("#") or not line.strip(): continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 3: continue
        try:
            i, z, fl = float(f[0]), float(f[1]), int(f[2])
        except ValueError:
            continue
        if fl == 0 and np.isfinite(i) and np.isfinite(z) and z >= 0: I.append(i); Z.append(z)
    return np.array(I), np.array(Z)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out-dir", required=True); ap.add_argument("--agg", required=True)
    a = ap.parse_args(); os.makedirs(a.out_dir, exist_ok=True)
    man = os.path.join(a.out_dir, "MANIFEST.txt")
    Iall, Zall = [], []
    for k, (lo, hi) in enumerate(SLICES):
        path = os.path.join(a.out_dir, "cosmos2020_classic_i%05.2f_%05.2f.tsv" % (lo, hi))
        tries = 0
        while not (os.path.exists(path) and valid(path)):
            if os.path.exists(path):        # a server-side failure page: keep it aside, note it, retry
                os.replace(path, path + ".failed%d" % tries)
                with open(man, "a") as m:
                    m.write("%s\tFAILED attempt %d (server error page or no table), kept as .failed%d, not used\n"
                            % (os.path.basename(path), tries, tries))
                if tries >= 8: sys.exit("slice %.2f-%.2f failed 8 times" % (lo, hi))
                time.sleep(20.0)
            else:
                time.sleep(2.0)
            tries += 1
            url, nb, dt = fetch(lo, hi, path)
            with open(man, "a") as m:
                m.write("%s\t%s\t%d bytes\tsha256 %s\t%s\tVizieR/CDS terms (academic use, cite Weaver et al. 2022, ApJS 258, 11)\n"
                        % (os.path.basename(path), url, nb, sha(path), datetime.date.today().isoformat()))
            print("  slice %.2f-%.2f: %d bytes in %.0f s%s" % (lo, hi, nb, dt, "" if valid(path) else "  (failed page)"), flush=True)
        I, Z = parse(path)
        # ASU ranges are inclusive at both ends: keep [lo, hi) except the last slice
        keep = (I >= lo) & ((I < hi) | (k == len(SLICES) - 1))
        Iall.append(I[keep]); Zall.append(Z[keep])
        print("  slice %.2f-%.2f: %d galaxies kept" % (lo, hi, keep.sum()), flush=True)
    I = np.concatenate(Iall); Z = np.concatenate(Zall)
    H, _, _ = np.histogram2d(I, Z, bins=[IEDGE, ZEDGE])
    with open(a.agg, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["i_lo"] + ["z%.3f" % z for z in ZEDGE[:-1]])
        for j in range(len(IEDGE) - 1):
            w.writerow(["%.1f" % IEDGE[j]] + [int(v) for v in H[j]])
    print("aggregate: %d galaxies in the grid (of %d kept), z >= 6: %d" % (int(H.sum()), len(I), int((Z >= 6).sum())))

if __name__ == "__main__":
    main()
