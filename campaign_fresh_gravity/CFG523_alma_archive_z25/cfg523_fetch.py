"""CFG523 capped, logged fetcher for PUBLIC ALMA pipeline product FITS (owner approval in chat 2026-10-09; budget 20 GB).

Only the ALMA dataPortal hosts are allowed. The archive answers closed byte ranges with HTTP 416 but open ranges ('bytes=N-') with 206,
so each request opens at offset N, reads exactly the bytes needed and closes. Used for (a) FITS headers and (b) sub-cubes: for each
channel plane only the needed contiguous block of image rows is read (FITS planes are row-major, x fastest), so a +-800 km/s,
+-R arcsec sub-cube costs a few MB instead of the 1-11 GB full cube. Every request is logged (label, url, offset, bytes, sha256 of the
bytes received, UTC time) to ../../../_external_data/cfg523_work/FETCH_MANIFEST.jsonl; the cumulative byte ledger (cap 20e9) is enforced
before every request. Nothing downloaded is executed. Data stay outside git.
"""
import datetime, hashlib, json, os, threading, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import requests
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg523_work"))
LEDGER = os.path.join(WORK, "LEDGER.json"); MAN = os.path.join(WORK, "FETCH_MANIFEST.jsonl")
ALLOWED = {"almascience.nrao.edu", "almascience.eso.org", "almascience.nao.ac.jp"}
CAP = 20_000_000_000
UA = "research-fetch/1.0 (public ALMA product retrieval for an open research repository)"
LOCK = threading.Lock()
_TL = threading.local()
def _sess():
    if not hasattr(_TL, 's'):
        _TL.s = requests.Session(); _TL.s.headers['User-Agent'] = UA
    return _TL.s

def _led():
    return json.load(open(LEDGER)) if os.path.exists(LEDGER) else {"used": 0, "requests": 0, "cap": CAP}

def get_bytes(label, url, offset, n, log=True):
    if urllib.parse.urlparse(url).netloc not in ALLOWED:
        raise SystemExit("REFUSED host " + url)
    with LOCK:
        led = _led()
        if led["used"] + n > led["cap"]:
            raise SystemExit(f"REFUSED: cap ({led['used']} + {n} > {led['cap']})")
    for attempt in range(4):
        try:
            r = _sess().get(url, headers={"Range": f"bytes={offset}-"}, stream=True, timeout=120, allow_redirects=True)
            if r.status_code != 206:
                r.close(); raise SystemExit(f"expected 206, got {r.status_code} for {url}")
            buf = bytearray()
            for chunk in r.iter_content(chunk_size=min(1 << 20, max(n, 1))):
                buf += chunk
                if len(buf) >= n: break
            r.close()
            body = bytes(buf[:n])
            if len(body) == n: break
        except requests.RequestException:
            if attempt == 3: raise
    with LOCK:
        led = _led(); led["used"] += len(body); led["requests"] += 1; json.dump(led, open(LEDGER, "w"))
        if log:
            open(MAN, "a").write(json.dumps(dict(label=label, url=url, offset=offset, bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                                             utc=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))) + "\n")
    return body

def header(label, url):
    raw = b""; off = 0
    while True:
        raw += get_bytes(label + ":hdr", url, off, 2880 * 4); off = len(raw)
        for i in range(0, len(raw), 80):
            if raw[i:i + 80].startswith(b"END" + b" " * 5):
                hl = ((i // 2880) + 1) * 2880
                return fits.Header.fromstring(raw[:hl].decode("ascii")), hl

def subcube(label, url, hdr, hl, c0, c1, y0, y1, x0, x1):
    """channels [c0, c1), rows [y0, y1), cols [x0, x1) (0-based); reads full rows y0..y1 per plane, crops x after."""
    nx, ny = hdr["NAXIS1"], hdr["NAXIS2"]; bp = abs(hdr["BITPIX"]) // 8
    dt = {-32: ">f4", -64: ">f8"}[hdr["BITPIX"]]
    out = np.empty((c1 - c0, y1 - y0, x1 - x0), dtype=np.float32)
    def one(kc):
        k, c = kc
        off = hl + (c * ny + y0) * nx * bp
        b = get_bytes(f"{label}:ch{c}", url, off, (y1 - y0) * nx * bp)
        out[k] = np.frombuffer(b, dtype=dt).reshape(y1 - y0, nx)[:, x0:x1]
    with ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(one, enumerate(range(c0, c1))))
    return out
