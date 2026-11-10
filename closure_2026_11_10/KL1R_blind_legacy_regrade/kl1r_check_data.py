#!/usr/bin/env python3
"""KL1R: check that the extracted KiDS-Legacy files used here are byte-identical to the members of the verified tarball.
Untrusted data: nothing is executed; members are only hashed. Run: python3 -I kl1r_check_data.py <tarball> <extracted top folder>"""
import sys, tarfile, hashlib, os
tb, top = sys.argv[1], sys.argv[2]
want = ("data/KiDS_Legacy_xipm.fits", "data/Nz_covariance.txt", "chains_and_config_files/xipm/KiDS_Legacy_priors.ini")
h = hashlib.sha256(); f = open(tb, "rb")
for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
print("tarball sha256", h.hexdigest())
with tarfile.open(tb, "r:gz") as T:
    names = T.getnames()
    for w in want:
        m = [n for n in names if n.endswith(w)]
        if not m: print("MISSING in tarball:", w); continue
        mi = T.getmember(m[0]); assert mi.isfile()
        a = hashlib.sha256(T.extractfile(mi).read()).hexdigest()
        p = os.path.join(os.path.dirname(top), m[0]); b = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None
        print(w, "member", a[:16], "on disk", (b or "absent")[:16], "MATCH" if a == b else "DIFFER")
