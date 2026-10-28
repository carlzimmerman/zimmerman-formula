"""Publish only this user-requested release, with persistent deposition state."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUTPUT = ROOT / "output/pdf"
BASE = "https://zenodo.org/api"
STATE = HERE / "publication.json"
FILES = [
    OUTPUT / "YANG_MILLS_BOUNDS_2026.pdf",
    OUTPUT / "YANG_MILLS_BOUNDS_2026_source.zip",
    HERE / "release_checks.json",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["draft", "publish", "verify"])
    action = parser.parse_args().action
    for path in FILES:
        if not path.is_file() or not path.stat().st_size:
            raise RuntimeError("Missing release file: " + path.name)
    checks = json.loads((HERE / "release_checks.json").read_text())
    if not checks["ready_to_publish"]:
        raise RuntimeError("Release checks are incomplete")
    for path in FILES[:2]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != checks["artifacts"][path.name]["sha256"]:
            raise RuntimeError("Artifact changed after checks: " + path.name)
    token = None
    for line in Path("/Users/carlzimmerman/new_physics/.env").read_text().splitlines():
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            token = line.split("=", 1)[1].strip().strip("\"'")
            break
    if not token:
        raise RuntimeError("Configured Zenodo credential is unavailable")

    def request(method, url, data=None, raw=None, auth=True, binary=False):
        if urlsplit(url).scheme != "https" or urlsplit(url).hostname != "zenodo.org":
            raise RuntimeError("Unexpected Zenodo destination")
        headers = {"Authorization": "Bearer " + token} if auth else {}
        body = raw
        if data is not None:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
        elif raw is not None:
            headers["Content-Type"] = "application/octet-stream"
        try:
            with urlopen(Request(url, data=body, headers=headers, method=method), timeout=60) as response:
                content = response.read()
                return content if binary else json.loads(content or "{}")
        except HTTPError as error:
            raise RuntimeError(f"Zenodo {method} returned HTTP {error.code}; saved deposition ID retained") from None

    if STATE.exists():
        state = json.loads(STATE.read_text())
        dep = request("GET", BASE + "/deposit/depositions/" + str(state["id"]))
    elif action == "draft":
        dep = request("POST", BASE + "/deposit/depositions", data={})
        state = {"id": dep["id"], "status": "draft"}
        STATE.write_text(json.dumps(state, indent=2) + "\n")
    else:
        raise RuntimeError("Create and inspect the draft first")
    dep_id = dep["id"]
    endpoint = BASE + "/deposit/depositions/" + str(dep_id)
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
    md5 = {p.name: hashlib.md5(p.read_bytes()).hexdigest() for p in FILES}
    print("Deposition:", dep_id, flush=True)
    if action == "draft" and not dep.get("submitted"):
        bucket = dep["links"]["bucket"]
        for path in FILES:
            request("PUT", bucket + "/" + path.name, raw=path.read_bytes())
            print("Uploaded:", path.name, flush=True)
        metadata = json.loads((HERE / "metadata.json").read_text())
        dep = request("PUT", endpoint, data={"metadata": metadata})
        dep = request("GET", endpoint)
        state.update(status="draft", file_sha256=hashes,
                     reserved_doi=dep.get("metadata", {}).get("prereserve_doi", {}).get("doi"))
        STATE.write_text(json.dumps(state, indent=2) + "\n")

    entries = {f["filename"]: f for f in dep.get("files", [])}
    if set(entries) != set(hashes):
        raise RuntimeError("Deposition file inventory differs from checked release")
    for name, entry in entries.items():
        if entry["checksum"].removeprefix("md5:") != md5[name]:
            raise RuntimeError("Uploaded checksum mismatch: " + name)
    if action == "publish" and not dep.get("submitted"):
        if state.get("file_sha256") != hashes:
            raise RuntimeError("Draft changed after upload; refresh draft first")
        request("POST", endpoint + "/actions/publish")
        dep = request("GET", endpoint)
    if dep.get("submitted"):
        if dep.get("state") != "done":
            raise RuntimeError("Publication is not confirmed done")
        doi = dep.get("doi") or dep.get("metadata", {}).get("doi")
        if not doi:
            raise RuntimeError("Published record has no DOI")
        public = request("GET", BASE + "/records/" + str(dep_id), auth=False)
        public_files = {f["key"]: f for f in public["files"]}
        if set(public_files) != set(hashes):
            raise RuntimeError("Public file inventory differs from release")
        verified = {}
        for name, entry in public_files.items():
            download_url = entry["links"].get("self") or entry["links"].get("download")
            actual = hashlib.sha256(request("GET", download_url, auth=False, binary=True)).hexdigest()
            if actual != hashes[name]:
                raise RuntimeError("Public downloaded content differs: " + name)
            verified[name] = actual
        state.update(status="published", doi=doi, url="https://zenodo.org/records/" + str(dep_id),
                     conceptdoi=dep.get("conceptdoi"), file_sha256=hashes,
                     public_download_sha256=verified, public_verified=True)
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        print("Published and public downloads verified:", state["url"], "| DOI:", doi, flush=True)
    else:
        print("Draft ready; uploaded checksums verified.", flush=True)


if __name__ == "__main__":
    main()
