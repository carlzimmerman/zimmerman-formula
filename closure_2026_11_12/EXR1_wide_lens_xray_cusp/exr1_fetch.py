#!/usr/bin/env python3
"""EXR1 fetch (network).  Frozen criteria: FROZEN_CRITERIA.md (commit 0cc195b7f6).

Reads, on one paced stream with a generic client name, and caches outside git:
  1. eROSITA-DE upper-limit service (band 024, DR1_eRASS1) at every lens of S, at 8 positions 0.5 deg from every W lens,
     at the positive-control clusters and at the same clusters moved +0.5 deg in Dec (twin shift);
  2. HI4PI N_HI (HEASARC nH tool) at every W lens and at the K4 groups;
  3. eRASS1 Main catalogue cones (SCS, VERB 1): 0.55 deg around every de_sky W lens (covers the lens and its 8 shifted
     positions), 60 arcsec around 60 positive-control clusters (and the same moved +0.5 deg in Dec).
Run:  python3 -I exr1_fetch.py --data-dir <ECLIPSE dir> --clusters <erass1cl_primary_v3.2.fits> --out <cache dir>
Re-running reuses every cached file.
"""
import argparse, csv, hashlib, json, math, os, re, sys, time, html, urllib.request, urllib.parse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E

UA = {"User-Agent": "python-client"}
UL_URL = "https://erosita.mpe.mpg.de/erodat/upperlimit/service_multi"
SCS_URL = "https://erosita.mpe.mpg.de/erodat/catalogue/SCS"
NH_URL = "https://heasarc.gsfc.nasa.gov/cgi-bin/Tools/w3nh/w3nh.pl"
PAUSE = 1.2
MAN = []
_last = [0.0]

def pace():
    dt = time.time() - _last[0]
    if dt < PAUSE: time.sleep(PAUSE - dt)
    _last[0] = time.time()

def get(url, path, data=None, ctype=None, timeout=180):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return open(path, "rb").read()
    pace(); hdr = dict(UA)
    if ctype: hdr["Content-Type"] = ctype
    for attempt in range(4):
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, data=data, headers=hdr), timeout=timeout).read(); break
        except Exception as e:
            print("  retry %d %s: %s" % (attempt + 1, url[:80], e), file=sys.stderr); time.sleep(5 * (attempt + 1))
    else:
        raise RuntimeError("fetch failed: " + url)
    open(path, "wb").write(b)
    MAN.append(dict(url=url, method="POST" if data else "GET", file=os.path.basename(path), bytes=len(b),
                    sha256=hashlib.sha256(b).hexdigest(), time=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
    return b

def shifted(ra, dec, pa_deg, rad_deg=0.5):
    """true-angle offset on the sphere (PA from north through east)."""
    d0, a0, th, pa = math.radians(dec), math.radians(ra), math.radians(rad_deg), math.radians(pa_deg)
    d1 = math.asin(math.sin(d0) * math.cos(th) + math.cos(d0) * math.sin(th) * math.cos(pa))
    a1 = a0 + math.atan2(math.sin(pa) * math.sin(th) * math.cos(d0), math.cos(th) - math.sin(d0) * math.sin(d1))
    return (math.degrees(a1) % 360.0, math.degrees(d1))

def positions(data_dir, clusters):
    rows, _ = E.load(data_dir)
    radec = {}
    with open(os.path.join(data_dir, "eclipse_dr1_catalogue_key_v20261103.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): radec[r["unique_identifier"]] = (E.fl(r["ra"]), E.fl(r["dec"]))
    S, _ = E.select(rows, ("A", "B")); S = sorted([r for r in S if np.isfinite(radec[r["id"]]).all()], key=lambda r: r["id"])
    W = [r for r in S if r["tE"] >= 1.7]
    from astropy.io import fits
    d = fits.open(clusters)[1].data
    z, M5 = np.asarray(d["BEST_Z"], float), np.asarray(d["M500"], float) * 1.0e13
    pc = np.where((M5 >= 2.0e14) & (z >= 0.1) & (z <= 0.6))[0]
    kt, ktl, kth = (np.asarray(d[c], float) for c in ("KT", "KT_L", "KT_H"))
    with np.errstate(invalid="ignore"):
        gi = np.where((kt > 0) & (ktl > 0) & (kth - ktl < 0.3 * kt) & (z > 0.05))[0]
    CL = [(float(d["RA"][i]), float(d["DEC"][i])) for i in pc]
    GR = [(float(d["RA"][i]), float(d["DEC"][i])) for i in gi]
    return S, W, radec, CL, GR, pc, gi

def nh_parse(txt):
    x = html.unescape(re.sub(r"<[^>]+>", " ", txt)); x = re.sub(r"\s+", " ", x)
    out = []
    for blk in x.split("Input Equatorial coordinates:")[1:]:
        m = re.search(r"\[ ([-\d.]+)\S*, ([-\d.]+)\S* \]", blk); w = re.search(r"Weighted average nH \(cm\*\*-2\) ([\d.E+\-]+)", blk)
        out.append((float(m.group(1)), float(m.group(2)), float(w.group(1)) if w else float("nan")))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True); ap.add_argument("--clusters", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    for sub in ("ul", "nh", "scs"): os.makedirs(os.path.join(a.out, sub), exist_ok=True)
    S, W, radec, CL, GR, pc, gi = positions(a.data_dir, a.clusters)
    print("S %d, W %d, positive-control clusters %d, K4 groups %d" % (len(S), len(W), len(CL), len(GR)))
    # ---------------------------------------------------------------- 1. upper limits
    Q = [("S", r["id"], 0, radec[r["id"]][0], radec[r["id"]][1]) for r in S]
    for r in W:
        for k in range(8):
            ra, de = shifted(*radec[r["id"]], 45.0 * k); Q.append(("Wshift", r["id"], k, ra, de))
    for j, (ra, de) in enumerate(CL): Q.append(("CL", str(int(pc[j])), 0, ra, de))
    for j, (ra, de) in enumerate(CL): Q.append(("CLshift", str(int(pc[j])), 0, ra, min(de + 0.5, 90.0)))
    print("upper-limit lookups: %d" % len(Q))
    res = []
    CH = 3000
    for c0 in range(0, len(Q), CH):
        body = json.dumps([dict(ra=round(q[3], 7), dec=round(q[4], 7), band="024", dr_survey="DR1_eRASS1") for q in Q[c0:c0 + CH]]).encode()
        b = get(UL_URL, os.path.join(a.out, "ul", "ul_%05d.json" % c0), data=body, ctype="application/json", timeout=600)
        r = json.loads(b)
        if r.get("error") not in (None, "None"): raise RuntimeError("upper-limit service error: %s" % r.get("error"))
        if len(r["limits"]) != len(Q[c0:c0 + CH]): raise RuntimeError("upper-limit count mismatch")
        res.extend(r["limits"]); print("  upper limits %d / %d" % (len(res), len(Q)), flush=True)
    with open(os.path.join(a.out, "ul_table.csv"), "w", newline="") as f:
        w = csv.writer(f); keys = ("Count", "Bkg_counts", "Bkg_SourceMap", "Exposure", "UL_B", "UL_S", "Flag_pos", "de_sky", "field")
        w.writerow(["kind", "id", "k", "ra", "dec"] + list(keys))
        for q, r in zip(Q, res):
            for qq, rr in ((q[3], r.get("ra")), (q[4], r.get("dec"))):
                if rr is None or abs(float(rr) - qq) > 1e-5: raise RuntimeError("upper-limit position mismatch")
            w.writerow(list(q[:3]) + ["%.7f" % q[3], "%.7f" % q[4]] + [r.get(k, "") for k in keys])
    desky = {q[1]: bool(r.get("de_sky")) for q, r in zip(Q, res) if q[0] == "S"}
    # ---------------------------------------------------------------- 2. N_HI
    NP = [("W", r["id"], radec[r["id"]][0], radec[r["id"]][1]) for r in W] + [("GR", str(int(gi[j])), ra, de) for j, (ra, de) in enumerate(GR)]
    nh = []
    for c0 in range(0, len(NP), 20):
        ent = ";".join("%.5f,%.5f" % (p[2], p[3]) for p in NP[c0:c0 + 20])
        url = NH_URL + "?" + urllib.parse.urlencode(dict(Entry=ent, NR="GRB/SIMBAD+Sesame/NED", CoordSys="Equatorial", equinox="2000", radius="0.1", usemap="0"))
        txt = get(url, os.path.join(a.out, "nh", "nh_%04d.html" % c0)).decode("utf-8", "replace")
        got = nh_parse(txt)
        if len(got) != len(NP[c0:c0 + 20]): raise RuntimeError("nH parse count mismatch at %d (%d)" % (c0, len(got)))
        for p, g in zip(NP[c0:c0 + 20], got):
            if abs(g[0] - p[2]) > 1e-4 or abs(g[1] - p[3]) > 1e-4: raise RuntimeError("nH position mismatch")
        nh.extend(got); print("  N_HI %d / %d" % (len(nh), len(NP)), flush=True)
    with open(os.path.join(a.out, "nh_table.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["kind", "id", "ra", "dec", "NHI_cm2"])
        for p, g in zip(NP, nh): w.writerow([p[0], p[1], "%.5f" % p[2], "%.5f" % p[3], "%.4e" % g[2]])
    # ---------------------------------------------------------------- 3. Main catalogue cones
    from astropy.io.votable import parse
    import warnings; warnings.simplefilter("ignore")
    rng = np.random.default_rng(E.SEED); pick = sorted(rng.choice(len(CL), 60, replace=False).tolist())
    CQ = [("W", r["id"], radec[r["id"]][0], radec[r["id"]][1], 0.55) for r in W if desky.get(r["id"])]
    CQ += [("CL", str(int(pc[j])), CL[j][0], CL[j][1], 60.0 / 3600.0) for j in pick]
    CQ += [("CLshift", str(int(pc[j])), CL[j][0], min(CL[j][1] + 0.5, 90.0), 60.0 / 3600.0) for j in pick]
    print("cone searches: %d" % len(CQ))
    with open(os.path.join(a.out, "scs_table.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["kind", "id", "cone_ra", "cone_dec", "cone_deg", "iauname", "ra", "dec", "ext", "ext_like", "det_like_0", "ml_flux_1"])
        for n, q in enumerate(CQ):
            url = SCS_URL + "?" + urllib.parse.urlencode(dict(CAT="DR1_Main", RA="%.6f" % q[2], DEC="%.6f" % q[3], SR="%.6f" % q[4], VERB="1"))
            b = get(url, os.path.join(a.out, "scs", "scs_%s_%s.xml" % (q[0], q[1])))
            tpath = os.path.join(a.out, "scs", "scs_%s_%s.xml" % (q[0], q[1]))
            t = parse(tpath).get_first_table().to_table()
            for s in t:
                w.writerow([q[0], q[1], "%.6f" % q[2], "%.6f" % q[3], "%.6f" % q[4], s["iauname"], "%.6f" % s["ra"], "%.6f" % s["dec"],
                            "%.3f" % s["ext"], "%.3f" % s["ext_like"], "%.3f" % s["det_like_0"], "%.4e" % s["ml_flux_1"]])
            if n % 25 == 0: print("  cones %d / %d" % (n + 1, len(CQ)), flush=True)
    mpath = os.path.join(a.out, "MANIFEST.json")
    old = json.load(open(mpath)) if os.path.exists(mpath) else []
    json.dump(old + MAN, open(mpath, "w"), indent=1)
    print("done; %d new fetches recorded in MANIFEST.json" % len(MAN))

if __name__ == "__main__":
    main()
