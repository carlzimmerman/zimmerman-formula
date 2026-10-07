#!/usr/bin/env python3
"""CFG395: rebuild etg16_serra16_lelli17.tsv from the two arXiv e-prints (see FETCH_LOG.md for URLs and sha256).
Run: python3 parse_sources.py <1604.07902 e-print tar.gz> <1610.08981 e-print tar.gz>   (writes the TSV to stdout)."""
import re, sys, tarfile, hashlib
SHA = {"1604.07902": "0c3409392a762e4aa819b82e532747af04b7fe23b9923e3b6613f4e0cc3e0309",
       "1610.08981": "3e6bd3e5bc7860900c0a3b5f51f4a5f395335f754fc49e62b308a82a82658be4"}
def member(path, key, name):
    assert hashlib.sha256(open(path, "rb").read()).hexdigest() == SHA[key], f"sha256 mismatch for {key}"
    with tarfile.open(path) as t:
        return t.extractfile(name).read().decode()
ms = member(sys.argv[1], "1604.07902", "ms.tex"); te = member(sys.argv[2], "1610.08981", "TableETG.tex")
ser = {}
for l in ms.splitlines()[144:160]:
    c = [x.strip() for x in l.replace('\\\\', '').split('&')]
    n = c[0].replace('~', '').replace('UGC06176', 'UGC6176')
    nums = [re.findall(r'[\d.]+', x) for x in c[1:]]
    ser[n] = dict(Re_as=nums[0][0], sig=nums[1][0], Rmax_as=nums[2][0], Vjam=nums[3][0], RHI_as=nums[4][0], VHI=nums[5][0], dVHI=nums[5][1])
lel = {}
for l in te.splitlines():
    if l.startswith('NGC') or l.startswith('UGC'):
        c = [x.strip() for x in l.replace('\\\\', '').split('&')]
        n = c[0].replace('\\,', '')
        if n not in ser: continue
        D, eD = re.findall(r'[\d.]+', c[2]); L, eL = re.findall(r'[\d.]+', c[4])
        lel[n] = dict(T=c[1], D=D, eD=eD, met=c[3], L36=L, eL36=eL, Reff_kpc=c[5], SBeff=c[6], Rd_kpc=c[7], SBd=c[8], ref=c[9])
assert len(ser) == 16 and len(lel) == 16
print("# CFG395 ETG input: the 16 ATLAS3D rotating early types with regular outer HI discs (den Heijer+2015).")
print("# Columns Re_as..dVHI: Serra, Oosterloo, Cappellari, den Heijer & Jozsa 2016, MNRAS 460, 1382, Table 1 (arXiv:1604.07902 source ms.tex,")
print("#   e-print sha256 0c3409392a762e4a...): Re_as circularised half-light radius (arcsec), sig sigma_e (km/s), Rmax_as / Vjam JAM peak radius/speed,")
print("#   RHI_as radius where den Heijer+2015 measure V_HI (arcsec), VHI, dVHI (km/s).")
print("# Columns T..ref: Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836, 152, Table of ETGs (arXiv:1610.08981 source TableETG.tex,")
print("#   e-print sha256 3e6bd3e5bc7860900...): morphological T string, D +- eD (Mpc), met = distance method (1 Virgocentric infall, 2 SBF),")
print("#   L36 +- eL36 (1e9 Lsun at 3.6um), Reff_kpc, SBeff (Lsun/pc^2), Rd_kpc, SBd (exp. disc scale length, central SB; Lsun/pc^2), ref (1 Serra16, 2 Weijmans08).")
print("# Parsed by script from the LaTeX sources on 2026-10-06 (see FETCH_LOG.md); nothing typed by hand.")
k1 = ['Re_as', 'sig', 'Rmax_as', 'Vjam', 'RHI_as', 'VHI', 'dVHI']; k2 = ['T', 'D', 'eD', 'met', 'L36', 'eL36', 'Reff_kpc', 'SBeff', 'Rd_kpc', 'SBd', 'ref']
print('\t'.join(['name'] + k1 + k2))
for n in ser:
    print('\t'.join([n] + [ser[n][k] for k in k1] + [lel[n][k] for k in k2]))
