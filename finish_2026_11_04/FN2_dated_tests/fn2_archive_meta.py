#!/usr/bin/env python3
"""FN2 A3 and B2 (FROZEN_CRITERIA.md, 755f05c3cf): ALMA archive METADATA only, no data product downloaded.
TAP ObsCore rows and the DataLink listing for (A) MOUS uid://A001/X3788/Xbfd2 (2024.1.00100.L, U4_28473) and (B) the 2025.1.01377.L
unit whose footprint holds GS4_24110. PI and author columns are never selected. Each raw response is saved with URL, UTC time, HTTP
status and SHA-256; their text is data.
    python3 -B fn2_archive_meta.py            writes a3_*/b2_* raw files and fn2_archive_meta.out/.json in this lane
kappa = 1/2 FITTED; one disc excludes no model; not theory closed."""
import csv, datetime, hashlib, io, json, math, os, re, sys, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
HOSTS = ("https://almascience.eso.org", "https://almascience.nrao.edu", "https://almascience.nao.ac.jp")
UA = "research-metadata/1.0 (ALMA archive metadata only; open research repository)"
OUT = []; LOG = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
COLS = ["obs_id", "member_ous_uid", "group_ous_uid", "proposal_id", "target_name", "s_ra", "s_dec", "s_fov", "s_resolution", "spatial_resolution",
        "t_exptime", "em_min", "em_max", "frequency_support", "velocity_resolution", "sensitivity_10kms", "cont_sensitivity_bandwidth", "band_list",
        "antenna_arrays", "is_mosaic", "data_rights", "obs_release_date", "dataproduct_type", "calib_level", "schedblock_name"]
NAMEISH = re.compile(r"pi_name|obs_creator|author|first_author|proposal_authors", re.I)

def get(path, params=None, label=""):
    last = None
    for h in HOSTS:
        url = h + path + ("?" + urllib.parse.urlencode(params) if params else "")
        for k in range(2):
            try:
                r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=180); body = r.read(); st = r.status
            except urllib.error.HTTPError as e:
                body, st = e.read(), e.code
            except Exception as e:
                last = repr(e); time.sleep(3 + 3 * k); continue
            rec = dict(label=label, url=url, status=st, bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
            LOG.append(rec); return body, rec
    raise SystemExit(f"{label}: no archive host answered ({last})")

def tap(adql, label):
    body, rec = get("/tap/sync", dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", MAXREC="5000", QUERY=adql), label)
    txt = body.decode("utf8", "replace"); rows = list(csv.DictReader(io.StringIO(txt))) if txt.startswith(COLS[0]) else []
    return txt, rows, rec

def datalink(uid, label):
    body, rec = get("/datalink/sync", dict(ID=uid), label); txt = body.decode("utf8", "replace"); files = []; errors = []
    try:
        root = ET.fromstring(body); N = root.tag.split("}")[0] + "}" if root.tag.startswith("{") else ""
        fields = [f.get("name") for f in root.iter(N + "FIELD")]
        for tr in root.iter(N + "TR"):
            d = dict(zip(fields, ["".join(td.itertext()) for td in tr.findall(N + "TD")]))
            if d.get("error_message"): errors.append(d["error_message"][:200])
            u = d.get("access_url") or ""
            files.append(dict(name=u.split("/")[-1] or d.get("ID", ""), access_url=u, content_length=int(float(d["content_length"])) if d.get("content_length") else None,
                              content_type=d.get("content_type"), semantics=d.get("semantics"), service_def=d.get("service_def"), description=(d.get("description") or "")[:160]))
        # service descriptors: the nested DataLink of each product tar (its file listing), followed one level only
        svc = {res.get("ID"): [p.get("value") for p in res.iter(N + "PARAM") if p.get("name") == "accessURL"] for res in root.iter(N + "RESOURCE") if res.get("type") == "meta"}
        for f in files: f["nested_url"] = (svc.get(f["service_def"]) or [None])[0] if f.get("service_def") else None
    except ET.ParseError as e:
        errors.append(f"not a VOTable: {e}")
    return txt, files, errors, rec

def nested(files, prefix):
    """Follow each nested DataLink (a product tar's listing) once; return the inner file rows. Metadata only."""
    out = []
    for f in files:
        u = f.get("nested_url")
        if not u: continue
        q = urllib.parse.urlparse(u); body, rec = get(q.path, dict(urllib.parse.parse_qsl(q.query)), f"{prefix} nested {f['service_def']}")
        tag = re.sub(r"\W", "_", f["service_def"].replace("DataLink.", ""))[:90]; save(f"{prefix}_datalink_nested_{tag}.xml", body.decode("utf8", "replace"))
        try:
            root = ET.fromstring(body); N = root.tag.split("}")[0] + "}" if root.tag.startswith("{") else ""; fields = [x.get("name") for x in root.iter(N + "FIELD")]
            for tr in root.iter(N + "TR"):
                d = dict(zip(fields, ["".join(td.itertext()) for td in tr.findall(N + "TD")])); a = d.get("access_url") or ""
                out.append(dict(parent=f["service_def"], name=a.split("/")[-1] or d.get("ID", ""), access_url=a, content_length=int(float(d["content_length"])) if d.get("content_length") else None,
                                content_type=d.get("content_type"), semantics=d.get("semantics"), error=(d.get("error_message") or "")[:160]))
        except ET.ParseError as e:
            out.append(dict(parent=f["service_def"], error=f"not a VOTable: {e}", status=rec["status"]))
    return out

def save(name, txt): open(os.path.join(HERE, name), "w").write(txt); return name
CKMS = 299792.458
def coverage(nu0, wins, shift, half):
    """Information: fraction of the frozen window [shift - half, shift + half] km/s (radio convention about nu0, the harnesses' _vaxis)
    that lies inside the archive window holding nu0; None if no window holds nu0."""
    w = [(a, b) for a, b, _ in wins if a <= nu0 <= b]
    if not w: return None
    a, b = w[0]; vlo, vhi = CKMS * (nu0 - b) / nu0, CKMS * (nu0 - a) / nu0
    return dict(window_GHz=(a, b), v_cover_kms=(round(vlo, 1), round(vhi, 1)), shift=shift, half=half,
                covered_fraction=round(max(0.0, min(vhi, shift + half) - max(vlo, shift - half)) / (2 * half), 4))
def sep_arcsec(r1, d1, r2, d2): return math.degrees(math.acos(min(1.0, math.sin(math.radians(d1)) * math.sin(math.radians(d2)) + math.cos(math.radians(d1)) * math.cos(math.radians(d2)) * math.cos(math.radians(r1 - r2))))) * 3600
def windows(fs):
    """frequency_support '[94.79..96.67GHz,7812.50kHz,...] U [...]' -> sorted (lo, hi, resolution text) per window."""
    out = []
    for m in re.finditer(r"\[([\d.]+)\.\.([\d.]+)GHz,([^,\]]*)", fs or ""): out.append((float(m.group(1)), float(m.group(2)), m.group(3)))
    return sorted(set(out))

if __name__ == "__main__":
    RES = dict(criteria="755f05c3cf", queries=LOG)
    P("FN2 archive metadata (TAP ObsCore + DataLink listings). No data product downloaded. kappa = 1/2 FITTED; not theory closed.")
    # ---------------- A3: the 2026-11-06 MOUS ----------------
    MOUS = "uid://A001/X3788/Xbfd2"; PC = (34.422382000017684, -5.181044500002704)   # AC1's phase centre (ac1_predict.py K1)
    txt, rows, rec = tap(f"SELECT {', '.join(COLS)} FROM ivoa.obscore WHERE member_ous_uid = '{MOUS}'", "A3 obscore MOUS")
    save("a3_obscore_mous.csv", txt); P(f"\n[A3] TAP {MOUS}: HTTP {rec['status']}, {len(rows)} rows, sha256 {rec['sha256'][:16]}")
    allrows = rows; rows = [r for r in allrows if r["target_name"] == "UDS28473"]   # run 2: the science target's rows only (run 1 compared calibrators too)
    P(f"    science target rows (UDS28473): {len(rows)}; other targets (calibrators): {sorted({r['target_name'] for r in allrows} - {'UDS28473'})}")
    A = {}
    if rows:
        dates = sorted({r["obs_release_date"] for r in rows}); tg = sorted({r["target_name"] for r in rows}); rights = sorted({r["data_rights"] for r in rows})
        wins = sorted({w for r in rows for w in windows(r["frequency_support"])}); sens = sorted({r["sensitivity_10kms"] for r in rows})
        seps = [sep_arcsec(float(r["s_ra"]), float(r["s_dec"]), *PC) for r in rows]
        A = dict(rows=len(rows), release_dates=dates, targets=tg, data_rights=rights, windows_GHz=[(a, b, c) for a, b, c in wins], sensitivity_10kms=sens,
                 phase_centre_sep_arcsec=[min(seps), max(seps)], spatial_resolution=sorted({r["spatial_resolution"] for r in rows}), t_exptime=sorted({r["t_exptime"] for r in rows}),
                 s_fov=sorted({r["s_fov"] for r in rows}), proposal_id=sorted({r["proposal_id"] for r in rows}), obs_id=sorted({r["obs_id"] for r in rows}),
                 group_ous_uid=sorted({r["group_ous_uid"] for r in rows}), schedblock_name=sorted({r["schedblock_name"] for r in rows}), velocity_resolution=sorted({r["velocity_resolution"] for r in rows}))
        for k, v in A.items(): P(f"    {k}: {v}")
    want = [(94.79, 96.67), (97.60, 98.62), (106.75, 108.73), (108.74, 110.61)]
    got = [(a, b) for a, b, _ in A.get("windows_GHz", [])]
    kw = len(got) == 4 and all(abs(a - x) <= 0.01 + 1e-9 and abs(b - y) <= 0.01 + 1e-9 for (a, b), (x, y) in zip(sorted(got), want))
    kp = bool(A) and A["phase_centre_sep_arcsec"][1] <= 0.1
    dA = A.get("release_dates", [])
    labA = "NOT FOUND" if not dA else ("DATE CONFIRMED" if len(dA) == 1 and dA[0].startswith("2026-11-06T02:42:31") else f"DATE CHANGED {dA}")
    P(f"[{'PASS' if kp else 'FAIL'}] K-A3 phase centre within 0.1\" of AC1's U4_28473 position: {A.get('phase_centre_sep_arcsec')}")
    P(f"[{'PASS' if kw else 'FAIL'}] K-A3 four windows equal PAPER66's within 0.01 GHz: {got}")
    P(f"[A3] release date label: {labA}")
    txt, files, errs, rec = datalink(MOUS, "A3 datalink MOUS"); save("a3_datalink_mous.xml", txt)
    P(f"[A3] DataLink {MOUS}: HTTP {rec['status']}, {len(files)} rows, errors {errs[:3]}")
    for f in files[:400]: P(f"    {f['name']}  {f['content_length']}  {f['content_type']}  {f['semantics']}")
    A.update(K_phase_centre=kp, K_windows=kw, label=labA, datalink_status=rec["status"], datalink_rows=len(files), datalink_errors=errs, datalink_files=files)
    # information: do the frozen windows and MUTATE shifts fit inside the archive windows? (no criteria line; reported only)
    wl = A.get("windows_GHz", []); cv = {}
    for nm, nu0, sh, hw in (("U4_28473 CO(3-2), true window", 345.796 / 3.52455, 0.0, 500.0), ("U4_28473 CO(3-2), AC1 MUTATE +1000", 345.796 / 3.52455, 1000.0, 500.0),
                            ("U4_27928 CO(2-1), true window", 230.538 / 2.41933, 0.0, 500.0), ("U4_27928 CO(2-1), CFG806 MUTATE +2000", 230.538 / 2.41933, 2000.0, 500.0)):
        cv[nm] = coverage(nu0, wl, sh, hw); P(f"[A3 information] {nm}: {cv[nm]}")
    A["window_coverage_information"] = cv
    tot = sum(f["content_length"] or 0 for f in files); A["datalink_total_bytes"] = tot
    if files: P(f"[A3] DataLink total {tot / 1e9:.3f} GB over {len(files)} rows")
    inner = nested(files, "a3"); A["nested_files"] = inner
    P(f"[A3] nested DataLink (files inside the product tars): {len(inner)} rows")
    for f in inner: P(f"    [{f.get('parent', '')[-30:]}] {f.get('name')}  {f.get('content_length')}  {f.get('semantics')}  {f.get('error', '')}")
    RES["A3"] = A
    # ---------------- B2: GS4_24110 ----------------
    RA, DEC = 53.166889, -27.798733
    txt, rows, rec = tap(f"SELECT {', '.join(COLS)} FROM ivoa.obscore WHERE proposal_id = '2025.1.01377.L' AND 1=CONTAINS(POINT('ICRS', {RA}, {DEC}), s_region)", "B2 obscore GS4")
    save("b2_obscore_gs4.csv", txt); P(f"\n[B2] TAP 2025.1.01377.L containing GS4_24110: HTTP {rec['status']}, {len(rows)} rows, sha256 {rec['sha256'][:16]}")
    B = dict(rows=len(rows), units=[])
    for mo in sorted({r["member_ous_uid"] for r in rows}):
        rr = [r for r in rows if r["member_ous_uid"] == mo]; ws = sorted({w for r in rr for w in windows(r["frequency_support"])})
        cov = any(a <= 270.006 <= b for a, b, _ in ws); sp = min(sep_arcsec(float(r["s_ra"]), float(r["s_dec"]), RA, DEC) for r in rr)
        u = dict(member_ous_uid=mo, rows=len(rr), release_dates=sorted({r["obs_release_date"] for r in rr}), targets=sorted({r["target_name"] for r in rr}), windows_GHz=ws,
                 covers_270p006=cov, min_sep_arcsec=sp, data_rights=sorted({r["data_rights"] for r in rr}), sensitivity_10kms=sorted({r["sensitivity_10kms"] for r in rr}),
                 spatial_resolution=sorted({r["spatial_resolution"] for r in rr}), t_exptime=sorted({r["t_exptime"] for r in rr}), is_mosaic=sorted({r["is_mosaic"] for r in rr}),
                 s_fov=sorted({r["s_fov"] for r in rr}), n_pointings_rows=len({(r['s_ra'], r['s_dec']) for r in rr}))
        B["units"].append(u); P(f"    {json.dumps(u)}")
    cu = [u for u in B["units"] if u["covers_270p006"]]
    dB = sorted({d for u in cu for d in u["release_dates"]})
    labB = "NOT FOUND" if not dB else ("DATE CONFIRMED" if all(d.startswith("2026-11-28") for d in dB) else f"DATE CHANGED {dB}")
    P(f"[B2] units covering 270.006 GHz: {[u['member_ous_uid'] for u in cu]}; release dates {dB}; label: {labB}")
    for u in cu:
        txt, files, errs, rec = datalink(u["member_ous_uid"], "B2 datalink GS4 unit"); nm = "b2_datalink_" + re.sub(r"\W", "_", u["member_ous_uid"].split("//")[-1]) + ".xml"; save(nm, txt)
        u.update(datalink_status=rec["status"], datalink_rows=len(files), datalink_errors=errs, datalink_files=files, datalink_total_bytes=sum(f["content_length"] or 0 for f in files))
        P(f"[B2] DataLink {u['member_ous_uid']}: HTTP {rec['status']}, {len(files)} rows, errors {errs[:3]}")
        for f in files[:400]: P(f"    {f['name']}  {f['content_length']}  {f['content_type']}  {f['semantics']}")
        inner = nested(files, "b2"); u["nested_files"] = inner
        P(f"[B2] nested DataLink (files inside the product tars): {len(inner)} rows")
        for f in inner: P(f"    [{f.get('parent', '')[-30:]}] {f.get('name')}  {f.get('content_length')}  {f.get('semantics')}  {f.get('error', '')}")
    for u in cu:
        u["window_coverage_information"] = {f"[CI](2-1) shift {sh:+.0f}": coverage(809.342 / 2.9975, u["windows_GHz"], sh, 300.0) for sh in (0.0, 2000.0, 1000.0)}
        P(f"[B2 information] {u['member_ous_uid']} frozen G1 window +-300 and MUTATE +2000 / fallback +1000 (A-G11): {u['window_coverage_information']}")
    d4 = json.load(open(os.path.join(ROOT, "doors_push_2026_10_22", "D4_alma_status", "d4_alma_status_results.json")))["summary"]["GS4 n=1 vs n=2"]
    kb3 = abs(d4["max_z_noisefree"] - 0.51) <= 0.005; B["K_B3"] = dict(max_z_noisefree=d4["max_z_noisefree"], branch=d4["branch"], reaches_3sigma=d4["reaches_3sigma"], ok=kb3)
    P(f"[{'PASS' if kb3 else 'FAIL'}] K-B3 largest GS4 n=1 vs n=2 separation (D4) = 0.51 +- 0.005 sigma: {d4['max_z_noisefree']:.4f} ({d4['branch']}), reaches 3 sigma {d4['reaches_3sigma']}")
    B["label"] = labB; RES["B2"] = B
    # never save a person's name: refuse if a name-like column slipped into any saved file
    bad = [n for n in os.listdir(HERE) if n.startswith(("a3_", "b2_")) and NAMEISH.search(open(os.path.join(HERE, n), errors="replace").read().split("\n", 1)[0])]
    if bad: raise SystemExit(f"name-like column header in {bad}: not saved for commit")
    json.dump(RES, open(os.path.join(HERE, "fn2_archive_meta.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, "fn2_archive_meta.out"), "w").write("\n".join(OUT) + "\n")
