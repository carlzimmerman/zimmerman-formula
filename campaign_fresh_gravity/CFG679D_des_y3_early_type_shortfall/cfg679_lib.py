#!/usr/bin/env python3
"""CFG679D shared helpers: memory guard (orchestrator rule), HTTP range reads with byte accounting.

Memory guard: pause while a cfg650 / cfg654 engine runs AND free+inactive pages < 8 GB, or while any cfg*pm* process holds > 20 GB RSS.
Paths in logs are repo-relative.
"""
import os, re, subprocess, time

BASE = "https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/"
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(LANES, "_external_data", "cfg679_des")


def free_inactive_gb():
    out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    ps = int(re.search(r"page size of (\d+)", out).group(1))
    get = lambda k: int(re.search(rf"{k}:\s+(\d+)", out).group(1))
    return (get("Pages free") + get("Pages inactive")) * ps / 1e9


def engines():
    out = subprocess.run(["ps", "axo", "rss=,command="], capture_output=True, text=True).stdout
    eng, big = False, False
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        rss, cmd = line.split(None, 1)
        rss_gb = int(rss) * 1024 / 1e9
        if re.search(r"cfg65[04]\w*\.py", cmd) and "waiter" not in cmd:
            eng = True
        if re.search(r"cfg\w*pm\w*\.py", cmd) and rss_gb > 20:
            big = True
    return eng, big


def guard(say=print, poll=120):
    """Block while the orchestrator's pause condition holds."""
    first = True
    while True:
        eng, big = engines()
        fi = free_inactive_gb()
        if big or (eng and fi < 8.0):
            if first:
                say(f"[guard] PAUSE: engine={eng} bigPM={big} free+inactive={fi:.1f} GB")
                first = False
            time.sleep(poll)
            continue
        if not first:
            say(f"[guard] resume: free+inactive={fi:.1f} GB")
        return fi


import requests
from collections import OrderedDict

SESSION = requests.Session()
BYTES = {"n": 0, "req": 0}


def get_range(url, a, b, tries=8):
    """bytes [a, b) by HTTP range with retries; counts bytes."""
    for k in range(tries):
        try:
            r = SESSION.get(url, headers={"Range": f"bytes={a}-{b - 1}"}, timeout=(30, 300))
            if r.status_code == 206 and len(r.content) == b - a:
                BYTES["n"] += len(r.content); BYTES["req"] += 1
                return r.content
            err = f"status {r.status_code} len {len(r.content)}"
        except Exception as e:
            err = repr(e)
        time.sleep(min(60, 2 ** k))
    raise IOError(f"range {a}-{b} of {url} failed: {err}")


class RangeFile:
    """read-only, seekable file object over HTTP range requests, LRU block cache (for h5py metadata/small reads)."""
    def __init__(self, url, block=1 << 20, nblocks=64):
        self.url, self.block, self.nb = url, block, nblocks
        self.size = int(SESSION.head(url, timeout=60).headers["Content-Length"])
        self.pos, self.cache = 0, OrderedDict()
    def _blk(self, i):
        if i in self.cache:
            self.cache.move_to_end(i); return self.cache[i]
        a = i * self.block; b = min(self.size, a + self.block)
        d = get_range(self.url, a, b)
        self.cache[i] = d
        if len(self.cache) > self.nb:
            self.cache.popitem(last=False)
        return d
    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self.pos
        n = max(0, min(n, self.size - self.pos))
        out = bytearray(); p = self.pos
        while len(out) < n:
            i = p // self.block; o = p - i * self.block
            d = self._blk(i)
            take = d[o:o + n - len(out)]
            out += take; p += len(take)
        self.pos = p
        return bytes(out)
    def readinto(self, buf):
        d = self.read(len(buf)); buf[:len(d)] = d; return len(d)
    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off)
        return self.pos
    def tell(self): return self.pos
    def seekable(self): return True
    def readable(self): return True
    def close(self): pass
