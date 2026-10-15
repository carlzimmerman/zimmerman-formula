"""CFG799 fetch + reduce: one HIFI observation at a time (criteria: FROZEN_CRITERIA.md).

For each obsid (largest integration first): download Level-1 and Level-0 tars from the ESA HSA, extract only the WBS
boxes that hold science datasets with 3.9 <= |nu_t - LO| <= 8.1 GHz (plus their comb/zero and hot/cold datasets),
delete the tars, reduce to a compact per-observation .npz of per-dataset arrays (zero-subtracted, t=1 normalised sky
counts, hot/cold loads, load temperatures, spacecraft-frame IF axes, Level-1 kept-row means and flags, L1-anchor
statistics), then delete the extracted FITS.  Downloaded files are untrusted data: members are read through tarfile
and written under fixed local names; nothing inside the data directory is executed.

Run:  python3 -I cfg799_fetch.py <data_dir> [max_obs]
Disk rule: no download if free space would fall below 25 GB.  Machine rule: stop if a 1024^3 run is live.
"""
import csv, gzip, json, os, re, shutil, subprocess, sys, tarfile, time
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(sys.argv[1])
MAXOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 6
NU_T = 541.664  # GHz, primary (FROZEN_CRITERIA)
URL = "https://archives.esac.esa.int/hsa/whsa-tap-server/data?RETRIEVAL_TYPE=OBSERVATION&OBSERVATION_ID={}&INSTRUMENT_NAME=HIFI&PRODUCT_LEVEL={}"
MODES = {"HifiPointModeDBS", "HifiPointModeFastDBS", "HifiSScanModeDBS", "HifiSScanModeFastDBS"}
FREE_MIN_GB = 25.0
MAN = os.path.join(DATA, "cfg799_manifest.json")
H_NU_K = 6.62607015e-34 * 541.7e9 / 1.380649e-23
EV = np.arange(1976) % 2 == 0


def log(s):
    print(time.strftime("%H:%M:%S"), s, flush=True)


def sim_running():
    """True if a 1024^3 run is live (pgrep -f equivalent, ignoring shells/pgrep/this lane, which may quote the pattern)."""
    ps = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout.splitlines()
    for line in ps:
        cmd = line.strip().split(None, 1)[-1] if line.strip() else ""
        if re.search(r"cfg650_pm|cfg654_pm|run_65", cmd) and not re.search(r"pgrep|cfg799|^\S*(ba|z)?sh\b", cmd):
            return True
    return False


def free_gb():
    st = os.statvfs(DATA)
    return st.f_bavail * st.f_frsize / 1e9


def J(T):
    return H_NU_K / np.expm1(H_NU_K / T)


def download(obsid, level, dest, tries=int(os.environ.get("CFG799_TRIES", "4"))):
    """curl with full retries: the HSA server sometimes closes long transfers early (curl error 18) and has no byte ranges."""
    err = ""
    for k in range(tries):
        cmd = ["curl", "-f", "-sS", "--max-time", "7200", "-o", dest, URL.format(obsid, level)]
        if os.path.exists(dest):   # the HSA server does not support byte ranges: restart from zero
            os.remove(dest)
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 10000:
            with tarfile.open(dest) as tf:   # integrity check: full member listing
                tf.getmembers()
            return os.path.getsize(dest)
        err = r.stderr.strip()[:200]
        time.sleep(5)
    raise RuntimeError(f"download {level} failed: {err}")


def extract(tarpath, pattern, outdir):
    """Extract regular members whose name matches pattern to outdir/<sanitised name> (gunzipped)."""
    got = {}
    with tarfile.open(tarpath) as tf:
        for m in tf.getmembers():
            if not m.isfile() or not re.search(pattern, m.name):
                continue
            parts = m.name.split("/")
            key = "_".join(p for p in parts[-3:] if re.fullmatch(r"[A-Za-z0-9_.\-]+", p))
            out = os.path.join(outdir, key.replace(".gz", ""))
            with tf.extractfile(m) as fsrc, open(out, "wb") as fdst:
                if m.name.endswith(".gz"):
                    with gzip.GzipFile(fileobj=fsrc) as g:
                        shutil.copyfileobj(g, fdst)
                else:
                    shutil.copyfileobj(fsrc, fdst)
            got[m.name] = out
    return got


def summary(path):
    d = fits.open(path)[1].data
    return [dict(ds=int(r["dataset"]), type=str(r["type"]).strip(), bbid=int(r["Bbid"]), bbn=int(r["bbNumber"]),
                 lo=float(r["LoFrequency"]) if "LoFrequency" in d.columns.names else np.nan) for r in d]


def box_of(ds):
    return (ds - 1) // 100 + 1, (ds - 1) % 100 + 1


def needed_datasets(summ):
    sci = [s for s in summ if s["type"] == "science" and 3.9 <= abs(NU_T - s["lo"]) <= 8.1]
    need = set()
    for s in sci:
        need.add(s["ds"])
        prev_hc = [t for t in summ if t["type"] == "hc" and t["ds"] < s["ds"]]
        next_hc = [t for t in summ if t["type"] == "hc" and t["ds"] > s["ds"]]
        for hc in (prev_hc[-1:] + next_hc[:1]):
            need.add(hc["ds"])
            cb = [t for t in summ if t["type"] == "comb" and t["ds"] < hc["ds"]]
            if cb:
                need.add(cb[-1]["ds"])
        cb = [t for t in summ if t["type"] == "comb" and t["ds"] < s["ds"]]
        if cb:
            need.add(cb[-1]["ds"])
    return sci, need


def nsub(row_flux, row_dark, zero, zdark):
    """Zero-subtracted counts (t = 1) for the 4 sub-bands, channels 52..2027 each -> (4, 1976)."""
    out = np.empty((4, 1976))
    dk = np.asarray(row_dark).reshape(4, 4); dz = np.asarray(zdark).reshape(4, 4)
    for sb in range(4):
        raw = row_flux[sb * 2048 + 52: sb * 2048 + 2028]
        zz = zero[sb * 2048 + 52: sb * 2048 + 2028]
        out[sb] = raw - zz * np.where(EV, dk[sb, 0] / dz[sb, 0], dk[sb, 1] / dz[sb, 1])
    return out


def smooth16(x):
    k = np.ones(16) / 16
    return np.array([np.convolve(r, k, "valid") for r in x])


def reduce_obs(obsid, files_l0, files_l1, summ):
    sci, need = needed_datasets(summ)
    bydsl = {s["ds"]: s for s in summ}
    res = {}
    for pol in ("h", "v"):
        l0 = {}; l1 = {}
        for b in sorted({box_of(d)[0] for d in need}):
            f0 = [p for n, p in files_l0.items() if f"WBS-{pol.upper()}/box_{b:03d}/" in n]
            f1 = [p for n, p in files_l1.items() if f"WBS-{pol.upper()}/box_{b:03d}/" in n]
            if f0: l0[b] = fits.open(f0[0], memmap=True)
            if f1: l1[b] = fits.open(f1[0], memmap=True)

        def hdu(store, ds):
            b, k = box_of(ds)
            if b not in store or k >= len(store[b]):
                return None
            d = store[b][k].data
            s = bydsl[ds]
            if int(d["bbtype"][0]) != s["bbid"] or int(d["bbnumber"][0]) != s["bbn"]:
                raise RuntimeError(f"box mapping mismatch ds {ds}")
            return d

        def zero_for(ds):
            cb = [t for t in summ if t["type"] == "comb" and t["ds"] < ds]
            if not cb:
                return None
            d = hdu(l0, cb[-1]["ds"])
            if d is None:
                return None
            # zero row = the flat one (the comb row carries comb spikes); addendum A: 6004 supplies only the zero
            peak = [np.percentile(np.abs(np.diff(np.asarray(d["flux"][r][52:2028], float))), 99.9) for r in range(len(d))]
            r = int(np.argmin(peak))
            return np.array(d["flux"][r], float), np.array(d["dark"][r], float)

        def load_hc(ds):
            d0 = hdu(l0, ds); d1 = hdu(l1, ds)
            z = zero_for(ds)
            if d0 is None or d1 is None or z is None or len(d0) < 2:
                return None
            tmap = {int(s): float(t) for s, t in zip(d1["sequenceNumber"], d1["integrationTime"])}
            N = []
            for r in range(2):
                t = tmap.get(int(d0["sequenceNumber"][r]))
                if not t:
                    return None
                N.append(nsub(np.array(d0["flux"][r], float), d0["dark"][r], *z) / t)
            hi = int(np.median(N[1]) > np.median(N[0]))
            H, C = N[hi], N[1 - hi]
            if np.mean(H - C <= 0) > 0.01:  # addendum A: corrupt load
                return None
            th, tc = (float(x) for x in d0["hot_cold"][0])
            ifax = np.array([d1[f"frequency_{k + 1}"][0] for k in range(4)], float)
            chop = (float(d0["Chopper"][hi]), float(d0["Chopper"][1 - hi]))
            return dict(H=H, C=C, JH=J(max(th, tc)), JC=J(min(th, tc)), IF=ifax, lo=float(d0["LoFrequency"][0]), chop=chop)

        dsets = []
        skipped = []
        for s in sci:
            d0 = hdu(l0, s["ds"]); d1 = hdu(l1, s["ds"])
            if d0 is None or d1 is None:
                skipped.append((s["ds"], "missing box")); continue
            lo0 = float(d0["LoFrequency"][0])
            hcs = []
            for cand in ([t for t in summ if t["type"] == "hc" and t["ds"] < s["ds"]][-1:] +
                         [t for t in summ if t["type"] == "hc" and t["ds"] > s["ds"]][:1]):
                hc = load_hc(cand["ds"])
                if hc is not None and abs(hc["lo"] - lo0) < 1e-3:
                    hcs.append(hc)
            z = zero_for(s["ds"])
            if not hcs or z is None:
                skipped.append((s["ds"], "no hc/zero")); continue
            H = np.mean([h["H"] for h in hcs], 0); C = np.mean([h["C"] for h in hcs], 0)
            JH = np.mean([h["JH"] for h in hcs]); JC = np.mean([h["JC"] for h in hcs])
            chops = [c for h in hcs for c in h["chop"]]
            kept = set(int(x) for x in d1["sequenceNumber"])
            seq0 = [int(x) for x in d0["sequenceNumber"]]
            if not kept or not kept.issubset(seq0):
                skipped.append((s["ds"], "L1 rows not subset of L0")); continue
            sky = [r for r in range(len(d0)) if min(abs(float(d0["Chopper"][r]) - c) for c in chops) > 0.3]
            on = [r for r in sky if seq0[r] in kept]; ref = [r for r in sky if seq0[r] not in kept]
            if not on or not ref:
                skipped.append((s["ds"], "no ON/REF split")); continue
            Nr = {r: nsub(np.array(d0["flux"][r], float), d0["dark"][r], *z) for r in sky}
            Non = np.mean([Nr[r] for r in on], 0); Nref = np.mean([Nr[r] for r in ref], 0)
            Nall = np.mean([Nr[r] for r in sky], 0)
            L1m = np.array([np.mean(d1[f"flux_{k + 1}"], 0) for k in range(4)], float)
            L1f = np.array([np.bitwise_or.reduce(np.asarray(d1[f"flag_{k + 1}"]), 0) for k in range(4)])
            G = (JH - JC) / (H - C)
            D1 = (Non - Nref) * G  # reference-subtracted spectrum at t_S = 1 s
            Ds, Ls = smooth16(D1).ravel(), smooth16(L1m).ravel()
            ok = np.isfinite(Ds) & np.isfinite(Ls)
            corr = float(np.corrcoef(Ds[ok], Ls[ok])[0, 1])
            tS = float(np.sign(corr) * np.std(Ds[ok]) / np.std(Ls[ok]))
            dsets.append(dict(ds=s["ds"], lo=lo0, nsky=len(sky), non=len(on), nref=len(ref), Nall=Nall, Nref=Nref,
                              H=H, C=C, JH=JH, JC=JC, IF=hcs[0]["IF"], L1=L1m, L1flag=L1f, tS=tS, corr=corr))
        for st in (l0, l1):
            for f in st.values():
                f.close()
        res[pol] = (dsets, skipped)
    return res


def save(obsid, res, out):
    arr = {}
    meta = {"obsid": obsid, "pol": {}}
    for pol, (dsets, skipped) in res.items():
        meta["pol"][pol] = {"n": len(dsets), "skipped": skipped}
        for i, d in enumerate(dsets):
            for k in ("Nall", "Nref", "H", "C", "L1"):
                arr[f"{pol}{i}_{k}"] = d[k].astype(np.float32)
            arr[f"{pol}{i}_IF"] = d["IF"]
            arr[f"{pol}{i}_L1flag"] = d["L1flag"].astype(np.int32)
            arr[f"{pol}{i}_scal"] = np.array([d["ds"], d["lo"], d["nsky"], d["non"], d["nref"], d["JH"], d["JC"], d["tS"], d["corr"]])
    arr["meta"] = np.array(json.dumps(meta))
    np.savez_compressed(out, **arr)


def main():
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "..", "CFG798_herschel_hifi_dish", "cfg798_matches.csv")))
            if r["target_GHz"] == "541.7" and r["mode"] in MODES]
    # point observations first (most hours per downloaded byte), then scans; largest integration first within each
    rows.sort(key=lambda r: ("SScan" in r["mode"], -float(r["t_int_h"])))
    if os.environ.get("CFG799_ONLY"):
        rows = [r for r in rows if r["observation_id"] == os.environ["CFG799_ONLY"]]
    man = json.load(open(MAN)) if os.path.exists(MAN) else {}
    man.pop("_stopped", None)
    rows.sort(key=lambda r: man.get(r["observation_id"], {}).get("status") == "failed")  # stable: retry failures last
    done = 0
    for r in rows:
        oid = r["observation_id"]
        if oid in man and man[oid].get("status") in ("ok", "empty", "failed_permanent"):
            continue
        if done >= MAXOBS:
            break
        if sim_running():
            log("1024^3 simulation running -> stop (machine rule)"); man["_stopped"] = "sim running"; break
        need_gb = 1.2 if "SScan" in r["mode"] else 0.6
        if free_gb() - need_gb < FREE_MIN_GB:
            log(f"disk rule: free {free_gb():.1f} GB -> stop"); man["_stopped"] = "disk"; break
        work = os.path.join(DATA, f"w_{oid}")
        os.makedirs(work, exist_ok=True)
        ent = {"mode": r["mode"], "t_int_h": float(r["t_int_h"]), "target": r["target_name"]}
        l0p = None
        try:
            t0 = time.time()
            l1tar = os.path.join(work, "l1.tar")
            # reuse the test download for the test obs
            pre = {"1342191482": ("test_1342191482.tar", "l0_1342191482.tar")}.get(oid)
            if pre and os.path.exists(os.path.join(DATA, pre[0])):
                shutil.move(os.path.join(DATA, pre[0]), l1tar); ent["l1_bytes"] = os.path.getsize(l1tar)
            else:
                # same observation: fetch Level-0 concurrently with Level-1 (still one observation at a time)
                import threading
                l0res = {}

                def _l0():
                    try:
                        l0res["n"] = download(oid, "LEVEL0", os.path.join(work, "l0.tar"))
                    except Exception as ex:  # noqa
                        l0res["err"] = str(ex)
                l0p = threading.Thread(target=_l0); l0p.start()
                ent["l1_bytes"] = download(oid, "LEVEL1", l1tar)
            htp = extract(l1tar, r"level1/WBS-[HV]/[^/]*htp[^/]*\.fits", work)
            hf = [p for n, p in htp.items() if "WBS-H" in n]
            if not hf:
                raise RuntimeError("no L1 htp")
            summ = summary(hf[0])
            sci, need = needed_datasets(summ)
            boxes = sorted({box_of(d)[0] for d in need})
            ent.update(n_sci=len(sci), boxes=boxes)
            if not sci:
                if l0p is not None:
                    l0p.join()
                ent["status"] = "empty"; os.remove(l1tar); shutil.rmtree(work); man[oid] = ent
                json.dump(man, open(MAN, "w"), indent=1); continue
            pat = r"level1/WBS-[HV]/box_(" + "|".join(f"{b:03d}" for b in boxes) + r")/"
            f1 = extract(l1tar, pat, work)
            os.remove(l1tar)
            l0tar = os.path.join(work, "l0.tar")
            if pre and os.path.exists(os.path.join(DATA, pre[1])):
                shutil.move(os.path.join(DATA, pre[1]), l0tar); ent["l0_bytes"] = os.path.getsize(l0tar)
            else:
                l0p.join()
                if "n" not in l0res:
                    raise RuntimeError(l0res.get("err", "download LEVEL0 failed"))
                ent["l0_bytes"] = os.path.getsize(l0tar)
            f0 = extract(l0tar, r"level0/WBS-[HV]/box_(" + "|".join(f"{b:03d}" for b in boxes) + r")/", work)
            os.remove(l0tar)
            if sim_running():
                log("1024^3 simulation running -> stop before reduction"); man["_stopped"] = "sim running"
                man[oid] = dict(ent, status="extracted_not_reduced"); json.dump(man, open(MAN, "w"), indent=1); break
            res = reduce_obs(oid, f0, f1, summ)
            save(oid, res, os.path.join(DATA, f"red_{oid}.npz"))
            ent.update(status="ok", n_dsets={p: len(v[0]) for p, v in res.items()},
                       skipped={p: v[1][:20] for p, v in res.items()}, secs=round(time.time() - t0))
            shutil.rmtree(work)
            log(f"{oid} ok  {r['mode']}  boxes {boxes}  dsets {ent['n_dsets']}  {ent['secs']} s  free {free_gb():.1f} GB")
        except Exception as e:  # noqa
            if l0p is not None:
                l0p.join()
            ent.update(status="failed", error=str(e)[:300])
            log(f"{oid} FAILED: {e}")
            shutil.rmtree(work, ignore_errors=True)
        man[oid] = ent
        json.dump(man, open(MAN, "w"), indent=1)
        done += 1
    json.dump(man, open(MAN, "w"), indent=1)


if __name__ == "__main__":
    main()
