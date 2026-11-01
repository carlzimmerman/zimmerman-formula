#!/usr/bin/env python3
"""Publish the Dark River Tavern Menu (PDF and page) to Zenodo production. Owner's go 2026-11-01. Token read by PAPER66's helper from .env, never printed.
Gates: both files committed and unmodified, 49 dishes, no pending picture, no home path. --check runs gates only."""
import hashlib, importlib.util, json, os, re, subprocess, sys, time
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "..", "..", "qwen_claude_field_theory", "papers_2026", "PAPER66_zenodo_publish.py"); FILES = ["Dark_River_Tavern_Menu.pdf", "menu.html"]; META = os.path.join(H, "menu.zenodo.json")
for f in FILES + ["menu.zenodo.json"]:
    if subprocess.run(["git", "status", "--porcelain", f], cwd=H, capture_output=True, text=True).stdout.strip(): sys.exit(f"REFUSING: {f} not committed clean")
t = open(os.path.join(H, "menu.html"), encoding="utf-8").read(); n = t.count('<article class="dish"')
if n != 49 or "Picture not ready" in t or "/Users/" in t: sys.exit(f"REFUSING: dishes {n}, or pending picture, or home path")
print(f"gates passed: {n} dishes; " + "; ".join(f"{f} {hashlib.md5(open(os.path.join(H, f), 'rb').read()).hexdigest()}" for f in FILES))
if "--check" in sys.argv: sys.exit(0)
s = importlib.util.spec_from_file_location("zp", R); Z = importlib.util.module_from_spec(s); s.loader.exec_module(Z); tok = Z.token(); B = Z.BASE; meta = json.load(open(META))["metadata"]
st, dep = Z.req("POST", f"{B}/deposit/depositions", tok, data={})
if st not in (200, 201): sys.exit(f"create failed [{st}]")
did, bucket = dep["id"], dep["links"]["bucket"]; print("draft", did)
for f in FILES:
    blob = open(os.path.join(H, f), "rb").read()
    for a in range(8):
        st, _ = Z.req("PUT", f"{bucket}/{f}", tok, raw=blob, ctype="application/octet-stream", tries=1); _, d = Z.req("GET", f"{B}/deposit/depositions/{did}", tok)
        if any(x.get("filename") == f and x.get("filesize") == len(blob) and x.get("checksum") == hashlib.md5(blob).hexdigest() for x in d.get("files", [])): print("confirmed", f, len(blob)); break
        time.sleep(20 * (a + 1))
    else: sys.exit(f"upload not confirmed: {f}; draft {did} left unpublished")
st, r = Z.req("PUT", f"{B}/deposit/depositions/{did}", tok, data={"metadata": meta})
if st != 200: sys.exit(f"metadata failed [{st}]: {str(r)[:300]}; draft {did} unpublished")
st, r = Z.req("POST", f"{B}/deposit/depositions/{did}/actions/publish", tok, tries=1)
if st != 202: sys.exit(f"publish failed [{st}]: {str(r)[:300]}; draft {did} unpublished")
out = dict(doi=r["doi"], url=r["links"].get("record_html") or r["links"].get("html"), conceptdoi=r.get("conceptdoi"), date="2026-11-01", version=meta["version"]); json.dump(out, open(os.path.join(H, "menu.zenodo.deposited.json"), "w"), indent=1); print(out)
