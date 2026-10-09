"""Build FETCH_LOG.md (relative paths only) from the work-dir manifest, ledger and cached files."""
import collections, hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg523_work"))
rel = "../../../_external_data/cfg523_work"
man = [json.loads(l) for l in open(os.path.join(WORK, "FETCH_MANIFEST.jsonl"))]
led = json.load(open(os.path.join(WORK, "LEDGER.json")))
agg = collections.OrderedDict()
for m in man:
    k = (m["label"].split(":")[0], m["url"], "hdr" if m["label"].endswith(":hdr") else "data")
    a = agg.setdefault(k, dict(n=0, bytes=0, first=m["utc"], last=m["utc"], h=hashlib.sha256()))
    a["n"] += 1; a["bytes"] += m["bytes"]; a["last"] = m["utc"]; a["h"].update(m["sha256"].encode())
L = ["# CFG523 FETCH_LOG (public ALMA Science Archive; owner approval in chat 2026-10-09; budget 20 GB)", "",
     f"Work dir (outside git): `{rel}/`. Per-request records (label, URL, byte offset, bytes, sha256 of the bytes, UTC) are in `{rel}/FETCH_MANIFEST.jsonl`; "
     f"the cumulative ledger is `{rel}/LEDGER.json`. All products are PUBLIC pipeline (`*.cube.I.pbcor.fits`) cubes; DataLink reported link_auth = false for every file used. "
     "Nothing proprietary or login-gated was requested.", "",
     f"**Total bytes received: {led['used']:,} ({led['used']/1e9:.3f} GB) in {led['requests']} requests**, including one 2026-10-09 range-support probe "
     "(223,694,848 bytes of the head of `member.uid___A001_X3788_X5cda.zC_406690_sci.spw15.cube.I.pbcor.fits`, sha256 "
     "9e684fd08f1fb64f403d6fec97f83efea2507d0c3193b94d9f34267146c9d101, deleted after the test).", "",
     "## Metadata (TAP / DataLink)", "| date | what | file | sha256 |", "|---|---|---|---|"]
for f, what in (("alma_rows_parents.csv", "ALMA TAP sync ivoa.obscore, INTERSECTS(s_region, CIRCLE) per parent field group, s_resolution <= 0.6\""),
                ("alma_rows_sweep.csv", "ALMA TAP sync ivoa.obscore, blind sweep S (see cfg523_sweep_results.json for the ADQL)")):
    p = os.path.join(WORK, f)
    if os.path.exists(p):
        L.append(f"| 2026-10-09 | {what} | `{rel}/{f}` ({os.path.getsize(p):,} B) | {hashlib.sha256(open(p,'rb').read()).hexdigest()} |")
for f in sorted(os.listdir(WORK)):
    if f.startswith("datalink_"):
        p = os.path.join(WORK, f)
        L.append(f"| 2026-10-09 | DataLink file list for MOUS {f[9:-5]} (astroquery.alma get_data_info) | `{rel}/{f}` | {hashlib.sha256(open(p,'rb').read()).hexdigest()} |")
L += ["", "## Product byte ranges (headers and line sub-cubes)", "| target | file (archive URL basename) | kind | requests | bytes | UTC first..last | sha256 over the per-request sha256 list |", "|---|---|---|---|---|---|---|"]
for (t, u, kind), a in agg.items():
    L.append(f"| {t} | `{u.split('/')[-1]}` | {kind} | {a['n']} | {a['bytes']:,} | {a['first']}..{a['last'][11:]} | {a['h'].hexdigest()[:32]}… |")
sub = os.path.join(WORK, "subcubes")
if os.path.isdir(sub):
    L += ["", "## Saved sub-cubes (cropped FITS written locally from the byte ranges above)", "| file | bytes | sha256 |", "|---|---|---|"]
    for f in sorted(os.listdir(sub)):
        p = os.path.join(sub, f); L.append(f"| `{rel}/subcubes/{f}` | {os.path.getsize(p):,} | {hashlib.sha256(open(p,'rb').read()).hexdigest()} |")
open(os.path.join(HERE, "FETCH_LOG.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L[:12]))
