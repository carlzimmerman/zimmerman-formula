#!/usr/bin/env python3
"""Parse Tables 1, 3 and 4 of Price+2021 (arXiv:2109.02659, 'Rotation Curves in z~1-2 Star-Forming Disks: Comparison of Dark Matter Fractions and Disk Properties for Different Fitting Methods';
the RC41 sample, 41 galaxies at z = 0.65-2.45) from its arXiv HTML page (fetched 2026-09-29; copy and sha256 in raw_small/ and manifest.json).
Table 1: general parameters (z, SED M*, SFR, M_gas 'from direct measurements, or gas-mass scaling relations', B/T, R_e,disk, Sersic n, q0, inclination, halo concentration).
Table 3: best-fit parameters of the 1D MCMC fit (NFW halo, no adiabatic contraction, asymmetric-drift correction): log M_bar, R_e, sigma_0, f_DM(R_e), log M_vir (inferred), MAP values with shortest-68% intervals.
Table 4: priors of the 2D fits (14 galaxies).  No acceleration, a0 or verdict is computed.
Checks: 41 rows; the ID and z columns agree between Tables 1 and 3; f_DM in [0,1]; the fitted M_bar is compared descriptively with SED M* + M_gas.
"""
import csv, hashlib, html, json, math, os, re, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "raw_small", "arxiv_2109.02659_html_fetched_2026-09-29.html")
LOG = []
def check(c, m):
    LOG.append(("PASS  " if c else "FAIL  ") + m); print(LOG[-1])
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n"); raise SystemExit(m)
s = open(SRC, errors="ignore").read()
def flat(x):
    x = re.sub(r'<math[^>]*alttext="([^"]*)"[^>]*>.*?</math>', lambda m: " [" + html.unescape(m.group(1)) + "] ", x, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
def table(tid):
    i = s.index('<table id="%s"' % tid); j = s.index("</table>", i)
    return [[flat(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)] for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s[i:j], flags=re.S)]
def num(x):
    m = re.search(r"-?\d+\.?\d*", x.replace("−", "-")); return float(m.group(0)) if m else None
def asym(x):
    m = re.search(r"\[?\s*(-?\d+\.?\d*)_\{\s*-\s*(\d+\.?\d*)\}\^\{\s*\+\s*(\d+\.?\d*)\}", x)
    return (float(m.group(1)), float(m.group(2)), float(m.group(3))) if m else (num(x), None, None)
ISROW = lambda r: len(r) >= 3 and r[0] and re.match(r"^\d+\.\d+$", r[1] or "") is not None
t1 = [r for r in table("S2.T1.4") if ISROW(r)]
t3 = [r for r in table("S3.T3.4") if ISROW(r)]
t4 = [r for r in table("S3.T4.6") if len(r) >= 6 and r[0] and not r[0].startswith(("ID", "["))]
check(len(t1) == 41 and len(t3) == 41, f"Table 1 and Table 3 have 41 galaxies each (got {len(t1)}, {len(t3)})")
check([r[0] for r in t1] == [r[0] for r in t3] or sorted(r[0] for r in t1) == sorted(r[0] for r in t3), "the two tables list the same 41 IDs")
by3 = {r[0]: r for r in t3}
rows = []
for r in t1:
    a = by3[r[0]]
    zz = num(r[1]); check(abs(zz - num(a[1])) < 1e-6, f"{r[0]}: z agrees between Tables 1 and 3") if abs(zz - num(a[1])) > 1e-6 else None
    mb, mbl, mbu = asym(a[2]); re_, rel, reu = asym(a[3]); sg, sgl, sgu = asym(a[4]); fd, fdl, fdu = asym(a[5]); mv, mvl, mvu = asym(a[6])
    rows.append(dict(id=r[0], z=zz, logMstar_SED=num(r[2]), SFR_Msun_yr=num(r[3]), logMgas=num(r[4]), BT=num(r[5]), Re_disk0_kpc=num(r[6]), n_Sersic_disk=num(r[7]), q0_disk=num(r[8]), incl_deg=num(r[9]), c_halo_fixed=num(r[10]),
                     logMbar_1D=mb, logMbar_lo=mbl, logMbar_hi=mbu, Re_1D_kpc=re_, Re_lo=rel, Re_hi=reu, sigma0_1D_kms=sg, sigma0_lo=sgl, sigma0_hi=sgu, fDM_Re_1D=fd, fDM_lo=fdl, fDM_hi=fdu, logMvir_1D=mv, logMvir_lo=mvl, logMvir_hi=mvu,
                     in_2D_priors_table=int(r[0] in {x[0].replace("_", "_") for x in t4})))
check(all(0 <= r["fDM_Re_1D"] <= 1 for r in rows), "f_DM(R_e) in [0, 1] for all 41")
check(all(r["logMbar_1D"] and r["Re_1D_kpc"] and r["sigma0_1D_kms"] for r in rows), "M_bar, R_e and sigma_0 parsed for all 41")
check(0.6 < min(r["z"] for r in rows) < 0.7 and 2.4 < max(r["z"] for r in rows) < 2.5, f"z range {min(r['z'] for r in rows)}-{max(r['z'] for r in rows)} (the paper says 0.65-2.45)")
with open(os.path.join(HERE, "price2021_rc41.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(HERE, "price2021_2D_priors.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["id", "logMbar_prior", "fDM_prior", "sigma0_prior", "Re_disk_prior", "Vsys_prior"]); w.writerows([r[:6] for r in t4])
# descriptive
d = [math.log10(10 ** r["logMstar_SED"] + 10 ** r["logMgas"]) - r["logMbar_1D"] for r in rows]
LOG.append(f"log10(M*_SED + M_gas) minus the 1D-fit log M_bar (dex): median {st.median(d):+.2f}, 16-84% {sorted(d)[int(.16*41)]:+.2f} to {sorted(d)[int(.84*41)]:+.2f}, |diff| > 0.3 dex for {sum(abs(x) > 0.3 for x in d)} of 41"); print(LOG[-1])
fd = [r["fDM_Re_1D"] for r in rows]; LOG.append(f"f_DM(R_e) 1D: median {st.median(fd):.2f}, min {min(fd):.2f}, max {max(fd):.2f}; galaxies with f_DM < 0.2: {sum(x < 0.2 for x in fd)}"); print(LOG[-1])
sg = [r["sigma0_1D_kms"] for r in rows]; LOG.append(f"sigma_0 (fitted): median {st.median(sg):.0f} km/s, range {min(sg):.0f}-{max(sg):.0f}"); print(LOG[-1])
gm = [r["logMgas"] - r["logMstar_SED"] for r in rows]; LOG.append(f"log(M_gas/M*_SED): median {st.median(gm):+.2f}, range {min(gm):+.2f} to {max(gm):+.2f}"); print(LOG[-1])
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
json.dump(dict(source_html_sha256=hashlib.sha256(open(SRC, "rb").read()).hexdigest(), url="https://arxiv.org/html/2109.02659", fetched="2026-09-29"), open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
