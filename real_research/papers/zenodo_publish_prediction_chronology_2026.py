"""Publish this requested chronology note; persist the draft ID before uploads.

Uses the existing project's Zenodo credential file without printing credentials.
Rerunning resumes the same deposition and checks for an already-published record.
"""
import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEM = "PREDICTION_CHRONOLOGY_2026"
BASE = "https://zenodo.org/api"
STATE = HERE / (STEM + ".zenodo-record.json")
FILES = [HERE / (STEM + suffix) for suffix in
         [".pdf", ".md", "_build.py", "_evidence.zip", ".zenodo.json"]]


def main():
    for path in FILES:
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Missing deliverable: {path.name}")
    token = None
    for line in Path("/Users/carlzimmerman/new_physics/.env").read_text().splitlines():
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            token = line.split("=", 1)[1].strip().strip("\"'")
            break
    if not token:
        raise RuntimeError("Zenodo credential is unavailable")

    def request(method, url, data=None, raw=None):
        headers = {"Authorization": "Bearer " + token}
        body = raw
        if data is not None:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
        elif raw is not None:
            headers["Content-Type"] = "application/octet-stream"
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read() or "{}")
        except urllib.error.HTTPError as error:
            raise RuntimeError(f"Zenodo {method} failed with HTTP {error.code}; draft ID is retained") from None

    if STATE.exists():
        dep_id = json.loads(STATE.read_text())["id"]
        dep = request("GET", f"{BASE}/deposit/depositions/{dep_id}")
    else:
        dep = request("POST", f"{BASE}/deposit/depositions", data={})
        STATE.write_text(json.dumps({"id": dep["id"], "status": "draft"}, indent=2) + "\n")
    dep_id = dep["id"]
    print(f"Deposition {dep_id}", flush=True)
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in FILES}
    if not dep.get("submitted"):
        bucket = dep["links"]["bucket"]
        for path in FILES:
            request("PUT", f"{bucket}/{path.name}", raw=path.read_bytes())
            print(f"Uploaded {path.name}", flush=True)
        metadata = json.loads((HERE / (STEM + ".zenodo.json")).read_text())
        request("PUT", f"{BASE}/deposit/depositions/{dep_id}", data={"metadata": metadata})
        dep = request("POST", f"{BASE}/deposit/depositions/{dep_id}/actions/publish")
        dep = request("GET", f"{BASE}/deposit/depositions/{dep_id}")
    if not dep.get("submitted") or dep.get("state") != "done":
        raise RuntimeError(f"Deposition {dep_id} has not confirmed publication")
    doi = dep.get("doi") or dep.get("metadata", {}).get("doi")
    if not doi:
        raise RuntimeError("Published deposition has no confirmed DOI")
    files = dep.get("files", [])
    uploaded = {entry["filename"] for entry in files}
    if uploaded != set(hashes):
        raise RuntimeError("Published file inventory differs from requested deliverables")
    state = dict(id=dep_id, status="published", doi=doi, url=f"https://zenodo.org/records/{dep_id}",
                 conceptdoi=dep.get("conceptdoi"), publication_date="2026-10-14",
                 file_sha256=hashes, published_files=[dict(filename=f["filename"], size=f["filesize"], checksum=f["checksum"]) for f in files])
    STATE.write_text(json.dumps(state, indent=2) + "\n")
    print(f"Published: {state['url']} | DOI: {doi}", flush=True)


if __name__ == "__main__":
    main()
