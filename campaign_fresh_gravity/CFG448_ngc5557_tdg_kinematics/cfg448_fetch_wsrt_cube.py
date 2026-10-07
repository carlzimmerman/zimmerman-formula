#!/usr/bin/env python3
"""CFG448 fetch helper: extract ONE member (NGC5557_cube.fits.gz) from the public ATLAS3D/WSRT HI release
(allcubes.tar, 24.7 GB, Google Drive folder linked from the ATLAS3D 'Data and Published Quantities' page) by walking
the tar headers with HTTP range requests (512 bytes each), then range-downloading only the wanted member.
Output: campaign_fresh_gravity/_external_data/cfg448/NGC5557_cube.fits.gz (git-ignored) + the member list
(fetched/allcubes_tar_members.tsv). Network only; negligible CPU.
"""
import os, sys, subprocess, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(os.path.dirname(HERE), "_external_data", "cfg448")
URL = ("https://drive.usercontent.google.com/download?id=1xznJ5sbxnwrvHtJ4E-GF9uUMkLcLKxDU&export=download&confirm=t")
WANT = sys.argv[1] if len(sys.argv) > 1 else "NGC5557_cube.fits.gz"


def rng(a, b, out=None):
    cmd = ["curl", "-sL", "-m", "600", "-r", f"{a}-{b}", URL]
    if out:
        subprocess.run(cmd + ["-o", out], check=True); return None
    return subprocess.run(cmd, check=True, capture_output=True).stdout


off, members, hit = 0, [], None
while True:
    h = rng(off, off + 511)
    name = h[:100].split(b"\0")[0].decode()
    if not name:
        break
    size = int(h[124:136].split(b"\0")[0].strip() or b"0", 8)
    members.append((name, off + 512, size))
    if name.endswith(WANT):
        hit = members[-1]; break
    off += 512 + ((size + 511) // 512) * 512
with open(os.path.join(HERE, "fetched", "allcubes_tar_members.tsv"), "w") as f:
    f.write("member\tdata_offset\tbytes\n" + "".join(f"{n}\t{o}\t{s}\n" for n, o, s in members))
print(f"walked {len(members)} members")
if hit is None:
    sys.exit(f"{WANT} not found")
os.makedirs(EXT, exist_ok=True)
out = os.path.join(EXT, WANT)
rng(hit[1], hit[1] + hit[2] - 1, out)
data = open(out, "rb").read()
assert len(data) == hit[2], (len(data), hit[2])
print(f"{WANT}: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}, tar offset {hit[1]}")
