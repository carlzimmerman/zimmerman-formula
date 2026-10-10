#!/usr/bin/env python3
"""CFG543 ADDENDUM (2026-10-09, post-freeze, no verdict weight): the Tian+26 paper text (owner-approved arXiv source fetch by
the coordinating session) says group M_bar = member stars (K-band, Kroupa) + observed X-ray hot gas (median ~8% of M_bar), and
Re = the mean projected radius of all members; sigma = biweight of members within that radius.
1. Mean-projected-radius conversion for the Hernquist tracer: <R> = (pi/4) <r> (isotropic projection); <r> diverges
   logarithmically for an untruncated Hernquist, so it is given for members truncated at r_t = c a (c = 10, 20, 50, 100):
   k(c) = <R>/R_e, R_e = 1.8153 a.
2. C0 and P2 rerun with R_e = Re/k(c) (aperture infinity, as primary), and P2 with sigma inside R < Re (aperture = the mean
   radius, CFG540 sigma2 with the class-A cap edge; single baryon component, members only).
"""
import os, json, math
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np
from scipy.integrate import quad
import cfg543_group_supply as M
C = M.C
OUT = []
def log(s=""): print(s); OUT.append(s)

def kfac(c):
    m = c ** 2 / (1 + c) ** 2
    rbar = quad(lambda r: r * 2 * r / (1 + r) ** 3, 0, c, limit=200)[0] / m
    return (math.pi / 4) * rbar / M.HERN_RE

def p2_aperture(o, a0, k=1.0):
    Mc = 10 ** o["lM"]; Msup = M.COLD_PER_B * Mc / 0.10
    Re = o["Re"] / k; a = Re * C.KPC / C.HERN_RE; GM = C.G * Mc * C.MSUN; a0d = a0 * a * a / GM
    rho, m = C.prof("hern", C.X); gN = m / C.X ** 2; mph = (C.nu(gN / a0d) - 1) * gN * C.X ** 2
    kk = np.where(mph >= Msup / Mc)[0]; xe = None if not len(kk) else float(C.X[kk[0]])
    return 0.5 * math.log10(C.sigma2("hern", a0d, 0.0, o["Re"] * C.KPC / a, xe) * GM / a) - 3.0

def main():
    rows = M.read_groups(); M.GEO = M.gas_geometry(M.lovisari())
    ks = {c: kfac(c) for c in (10, 20, 50, 100)}
    log("CFG543 ADDENDUM (post-freeze, no verdict weight)")
    log("Hernquist mean projected radius of members truncated at r_t = c a: <R>/R_e = " + ", ".join(f"c={c}: {v:.3f}" for c, v in ks.items()))
    res = dict(k=ks, footings={})
    ls = np.array([o["ls"] for o in rows])
    for fk, a0 in M.FOOT.items():
        r = {}
        log(f"\n=== {fk} ===")
        for c, k in ks.items():
            for b in ("C0", "P2"):
                D, s, st = M.run(rows, a0, dict(kind=b, k=k))
                r[f"{b}_c{c}"] = dict(mean=st["mean"], Z=st["Z"], label=st["label"])
                log(f"  {b} R_e = Re/{k:.3f} (c={c}): mean {st['mean']:+.3f} Z {st['Z']:+.2f} -> {st['label']}")
        for c in (None, 20):
            k = 1.0 if c is None else ks[c]
            lp = np.array([p2_aperture(o, a0, k) for o in rows]); D = ls - lp
            se = D.std(ddof=1) / math.sqrt(len(D))
            r[f"P2_aperture_{c}"] = dict(mean=float(D.mean()), se=float(se))
            log(f"  P2 sigma inside R < Re (R_e = Re/{k:.3f}): mean {D.mean():+.3f} +- {se:.3f} (SE only)")
        res["footings"][fk] = r
    json.dump(res, open(os.path.join(M.HERE, "cfg543_addendum_results.json"), "w"), indent=1)
    open(os.path.join(M.HERE, "cfg543_addendum.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
