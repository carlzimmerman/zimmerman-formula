#!/usr/bin/env python3
"""
L325 -- KP2 / KP3 / R-F3 against the PUBLIC per-object LRD data (2026-09-22).  stdlib + numpy only.
(Door-swing lane for the BH* campaign's open items 3-4; tests the PUBLISHED BH* family, not the framework.)

Registered claims under test (real_research/reviews/bhstar_t1_kepler_predictions.py,
bhstar_u1_decircularization.py, BHSTAR_CAMPAIGN_INDEX_2026-09-20.md):
  KP2   v_inf ∝ M^{1/4} (spread 10^0.225 = 1.68 across the published band, 350-588 km/s
        at kappa = 3.6); a classic M^{1/2} scaling kills the recombination-pinned family.
  KP3   T_eff follows the Saha front curve in the layer density n_H
        (repo definition: 2.4e15 T^1.5 exp(-13.5984 eV/kT)/n_H = 0.5).
  R-F3  Gamma = kappa_es sigma T_eff^4 / (c g_phot) per object; claimed range [36, 90].

DATA ACTUALLY PUBLIC (fetched 2026-09-22 into this directory; nothing read off plots):
  * arXiv:2609.09274 (Sun+ 2026) e-print TeX: Table 2 (4 STACKS: median N=117 + 3
    substacks) and Tables 3-4 (stack masses).  NO per-object T_eff / log g / L / M; the
    text says individual BH* spectra are too noisy and stacks are used by design.  No
    Zenodo / GitHub / data-availability link.
  * arXiv:2511.21820 (de Graaff+ 2026) -> Zenodo 10.5281/zenodo.21977747 (CC-BY-4.0),
    181 rows / 146 unique LRDs: modified-blackbody T (z<4.5 only), L_MBB, L_5100, line
    fluxes/EWs.  NO atmosphere log g, NO n_H, NO velocities, NO masses.
  * arXiv:2606.30711 (Naidu+ 2026) Table A1: v_blue,95%(Halpha) for 11 LRDs (the proxy
    for v_inf used by Sun+ Table 2).
  * arXiv:2603.17667 (Matthee+ 2026) Tables: coordinates + L_Halpha,tot for those 11.
  * arXiv:2603.02317 (Liu+ 2026): ONE per-object atmosphere fit (the local LRD 'the Egg').
Transcribed values are checked against the arXiv TeX files when present (x_<id>/...; not committed --
fetch https://arxiv.org/e-print/<id> and untar to re-verify; 54/54 matched on 2026-09-22).  The Zenodo
catalogue lrds_dG26_mnras.fits (de Graaff+ 2026, CC-BY-4.0, doi:10.5281/zenodo.21977747) is committed
alongside.  Run from the repository root:  python3 real_research/bhstar_audit_2026/L325_lrd_per_object_kp_doors.py
"""

import json
import math
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- constants (SI). NB: the repo scripts carry C = 2.99772458e8 (digit typo, 7e-5 rel.).
SIGMA = 5.670374419e-8
C = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98841e30
MP = 1.67262192e-27
MU = 1.4                      # repo's mass per H nucleus, in m_p
EV, KB = 1.602176634e-19, 1.380649e-23

out = {}


def hdr(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# =====================================================================================
# 0. TRANSCRIBED TABLES (with TeX verification)
# =====================================================================================
# Sun+ 2609.09274 Table 2 (tab:substacks) + Table 4 (tab:mass, surface-gravity column).
# (name, N, T, T+, T-, logg, g+, g-, logLbol, |v95|, v95_lo, v95_hi, logM_grav, M+, M-)
# v95 given as -523^{+121}_{-251} => |v| in [523-121, 523+251].
SUN = [
    ("Median", 117, 4662, 27, 15, -2.2, 0.2, 0.2, 43.8, 495, 495 - 95, 495 + 92, 4.0, 0.2, 0.2),
    ("Luminous", 17, 4757, 37, 20, -2.5, 0.1, 0.1, 44.5, 523, 523 - 121, 523 + 251, 4.3, 0.1, 0.2),
    ("Inter", 85, 4716, 38, 40, -1.9, 0.9, 0.4, 43.8, 364, 364 - 185, 364 + 195, 4.2, 0.9, 0.4),
    ("Faint", 15, 4233, 23, 21, -2.5, 0.3, 0.3, 43.5, None, None, None, 3.4, 0.4, 0.3),
]
SUN_TEX = [r"Median BH* ($N=117$) & $43.5^{+0.1}_{-0.1}$ & $4662^{+27}_{-15}$ & $-2.2^{+0.2}_{-0.2}$",
           r"Luminous BH* ($N=17$) & $44.2^{+0.1}_{-0.1}$ & $4757^{+37}_{-20}$ & $-2.5^{+0.1}_{-0.1}$",
           r"Inter. BH* ($N=85$) & $43.5^{+0.1}_{-0.1}$ & $4716^{+38}_{-40}$ & $-1.9^{+0.9}_{-0.4}$",
           r"Faint BH* ($N=15$) & $42.9^{+0.1}_{-0.1}$ & $4233^{+23}_{-21}$ & $-2.5^{+0.3}_{-0.3}$",
           r"$-495^{+95}_{-92}$", r"$-523^{+121}_{-251}$", r"$-364^{+185}_{-195}$",
           r"Median BH* ($N=117$) & $4.0^{+0.2}_{-0.2}$", r"Luminous BH* ($N=17$) & $4.3^{+0.1}_{-0.2}$",
           r"Inter. BH* ($N=85$) & $4.2^{+0.9}_{-0.4}$", r"Faint BH* ($N=15$) & $3.4^{+0.4}_{-0.3}$",
           r"$43.8^{+0.1}_{-0.1}$", r"$44.5^{+0.1}_{-0.1}$", r"$43.5^{+0.1}_{-0.1}$"]

# Naidu+ 2606.30711 Table A1 (tab:v95): v_blue,95%(Halpha) = v^{+a}_{-b}  [km/s, negative]
NAIDU = [("FRESCO-GN-9771", -400, 6, 5), ("FRESCO-GN-15498", -239, 4, 6),
         ("FRESCO-GS-13971", -443, 38, 83), ("JADES-GN-68797", -1130, 183, 134),
         ("JADES-GN-38147", -411, 22, 26), ("RUBIES-EGS-42046", -1041, 60, 120),
         ("RUBIES-EGS-55604", -561, 19, 22), ("RUBIES-EGS-49140", -794, 214, 178),
         ("RUBIES-UDS-182791", -569, 30, 26), ("The Cliff", -145, 21, 111),
         ("UNCOVER-A2744-45924", -389, 5, 8)]

# Matthee+ 2603.17667 tab:sample (RA, Dec) and tab:lum_cat L_Halpha,tot [1e42 erg/s]
MATTHEE = {"FRESCO-GN-9771": (189.2810, 62.2473, 64.4), "FRESCO-GN-15498": (189.2855, 62.2807, 5.6),
           "FRESCO-GS-13971": (53.1386, -27.7903, 11.9), "JADES-GN-68797": (189.2291, 62.1462, 60.0),
           "JADES-GN-38147": (189.2707, 62.1484, 13.8), "RUBIES-EGS-42046": (214.7954, 52.7888, 38.6),
           "RUBIES-EGS-55604": (214.9830, 52.9560, 75.2), "RUBIES-EGS-49140": (214.8922, 52.8774, 60.8),
           "RUBIES-UDS-182791": (34.2138, -5.0870, 15.0), "The Cliff": (34.4107, -5.1297, 0.7),
           "UNCOVER-A2744-45924": (3.5848, -30.3436, 66.0)}
MATTHEE_TEX = {"FRESCO-GN-9771": ("189.2810 & 62.2473", r"$64.4\pm0.1$"),
               "FRESCO-GN-15498": ("189.2855 & 62.2807", r"$5.6\pm0.1$"),
               "FRESCO-GS-13971": ("53.1386 & 27.7903", r"$11.9\pm0.1$"),   # TeX drops the minus
               "JADES-GN-68797": ("189.2291 & 62.1462", r"$60.0\pm0.3$"),
               "JADES-GN-38147": ("189.2707 & 62.1484", r"$13.8\pm0.3$"),
               "RUBIES-EGS-42046": ("214.7954 & 52.7888", r"$38.6\pm0.3$"),
               "RUBIES-EGS-55604": ("214.9830 & 52.9560", r"$75.2\pm0.8$"),
               "RUBIES-EGS-49140": ("214.8922 & 52.8774", r"$60.8\pm0.6$"),
               "RUBIES-UDS-182791": ("34.2138 & -5.0870", r"$15.0\pm0.2$"),
               "The Cliff": ("34.4107 & -5.1297", r"$0.7\pm0.1$"),
               "UNCOVER-A2744-45924": ("3.5848 &-30.3436", r"$66.0\pm0.1$")}

# Liu+ 2603.02317 (the Egg, local LRD; NOT in the 117): fiducial posterior (tab:sensivitity)
EGG = dict(T=4506, Tp=47, Tm=49, logg=-2.86, gp=0.14, gm=0.09,
           logg_sens=[-2.86, -2.83, -2.78, -2.85, -2.86, -2.94],
           rho_ph_cgs=7e-12)   # text: T=4500, log g=-3 <-> rho_ph = 7e-12 g/cm^3


def verify_tex():
    checks, ok = 0, 0
    fails = []
    p = os.path.join(HERE, "x_2609.09274", "main.tex")
    if os.path.exists(p):
        s = open(p, errors="replace").read()
        for frag in SUN_TEX:
            checks += 1
            ok += frag in s
            if frag not in s:
                fails.append(("Sun", frag))
    p = os.path.join(HERE, "x_2606.30711", "main.tex")
    if os.path.exists(p):
        s = open(p, errors="replace").read()
        for nm, v, a, b in NAIDU:
            frag = f"{nm} & $%d^{{+%d}}_{{-%d}}$" % (v, a, b)
            checks += 1
            ok += frag in s
            if frag not in s:
                fails.append(("Naidu", frag))
    p = os.path.join(HERE, "x_2603.17667", "aanda.tex")
    if os.path.exists(p):
        s = re.sub(r"\s+", " ", open(p, errors="replace").read())
        for nm, (coord, lum) in MATTHEE_TEX.items():
            for frag in (coord, lum):
                checks += 1
                ok += frag in s
                if frag not in s:
                    fails.append(("Matthee", nm, frag))
    p = os.path.join(HERE, "x_2603.02317", "main_v3.tex")
    if os.path.exists(p):
        s = open(p, errors="replace").read()
        for frag in (r"$4506^{+47}_{-49}$ & $-2.86^{+0.14}_{-0.09}$", r"$-2.83^{+0.11}_{-0.10}$",
                     r"$-2.78^{+0.05}_{-0.04}$", r"$-2.85^{+0.22}_{-0.11}$", r"$-2.86^{+0.22}_{-0.10}$",
                     r"$-2.94^{+0.07}_{-0.04}$", r"\rho_{\rm ph}=7\times10^{-12}"):
            checks += 1
            ok += frag in s
            if frag not in s:
                fails.append(("Liu", frag))
    return checks, ok, fails


# =====================================================================================
# minimal numpy FITS BINTABLE reader (for the Zenodo catalogue)
# =====================================================================================
def read_fits_bintable(path):
    raw = open(path, "rb").read()
    pos, hdus = 0, []
    while pos < len(raw):
        cards = {}
        order = []
        while True:
            block = raw[pos:pos + 2880]
            pos += 2880
            end = False
            for i in range(36):
                card = block[80 * i:80 * i + 80].decode("ascii", "replace")
                key = card[:8].strip()
                if key == "END":
                    end = True
                    break
                if card[8:10] == "= ":
                    val = card[10:].split("/")[0].strip() if "'" not in card[10:] else \
                        card[10:].split("'")[1].strip()
                    cards[key] = val
                    order.append(key)
            if end:
                break
        naxis = int(cards.get("NAXIS", 0))
        nbytes = 1
        for k in range(1, naxis + 1):
            nbytes *= int(cards["NAXIS%d" % k])
        nbytes = nbytes * abs(int(cards.get("BITPIX", 8))) // 8 if naxis else 0
        nbytes += int(cards.get("PCOUNT", 0)) if naxis else 0
        hdus.append((cards, pos))
        pos += int(math.ceil(nbytes / 2880.0)) * 2880
        if cards.get("XTENSION", "").strip() == "BINTABLE":
            break
    cards, start = hdus[-1]
    nrow, rowlen, nf = int(cards["NAXIS2"]), int(cards["NAXIS1"]), int(cards["TFIELDS"])
    code = {"K": ">i8", "J": ">i4", "I": ">i2", "D": ">f8", "E": ">f4", "B": "u1", "L": "S1"}
    names, fmts = [], []
    for k in range(1, nf + 1):
        m = re.match(r"(\d*)([A-Z])", cards["TFORM%d" % k])
        r, t = int(m.group(1) or 1), m.group(2)
        names.append(cards["TTYPE%d" % k])
        if t == "A":
            fmts.append("S%d" % r)
        elif r == 1:
            fmts.append(code[t])
        else:
            fmts.append((code[t], (r,)))
    dt = np.dtype({"names": names, "formats": fmts})
    assert dt.itemsize == rowlen, (dt.itemsize, rowlen)
    return np.frombuffer(raw[start:start + nrow * rowlen], dtype=dt, count=nrow)


# =====================================================================================
# statistics helpers
# =====================================================================================
def ols(x, y):
    X = x - x.mean()
    return float((X * (y - y.mean())).sum() / (X * X).sum())


def boot_slope(x, y, n=20000, seed=20260922):
    rng = np.random.default_rng(seed)
    N = len(x)
    out_ = []
    for _ in range(n):
        j = rng.integers(0, N, N)
        if np.ptp(x[j]) > 0:
            out_.append(ols(x[j], y[j]))
    out_ = np.array(out_)
    return float(out_.std()), np.percentile(out_, [2.5, 16, 50, 84, 97.5])


def perm_p(x, y, n=20000, seed=7):
    rng = np.random.default_rng(seed)
    r0 = abs(np.corrcoef(x, y)[0, 1])
    hits = sum(abs(np.corrcoef(x, rng.permutation(y))[0, 1]) >= r0 for _ in range(n))
    return (hits + 1) / (n + 1)


def m2lnL_profile(x, y, sy, b, sx=0.0, want_s=False):
    """-2 ln L minimised over intercept a and intrinsic scatter s at fixed slope b."""
    best, sbest = np.inf, 0.0
    for s in np.concatenate([[0.0], np.logspace(-3, 0.5, 700)]):
        var = s * s + sy * sy + (b * sx) ** 2
        w = 1 / var
        a = float(((y - b * x) * w).sum() / w.sum())
        v = float((((y - a - b * x) ** 2) / var + np.log(var)).sum())
        if v < best:
            best, sbest = v, float(s)
    return (best, sbest) if want_s else best


def ml_scan(x, y, sy, sx=0.0):
    bs = np.round(np.arange(-0.5, 1.5001, 0.005), 4)
    L = np.array([m2lnL_profile(x, y, sy, b, sx) for b in bs])
    i = int(L.argmin())
    inside = bs[L <= L[i] + 1.0]
    return float(bs[i]), float(inside.min()), float(inside.max()), float(L[i]), bs, L


# =====================================================================================
# 0. inventory + verification
# =====================================================================================
hdr("0. DATA INVENTORY + TRANSCRIPTION CHECK")
n_chk, n_ok, fails = verify_tex()
print(f"  transcribed table cells verified against the e-print TeX: {n_ok}/{n_chk}")
for f in fails:
    print("   MISMATCH:", f)
out["transcription_check"] = dict(checked=n_chk, ok=n_ok, fails=[list(f) for f in fails])

fits_path = os.path.join(HERE, "lrds_dG26_mnras.fits")
cat = read_fits_bintable(fits_path) if os.path.exists(fits_path) else None
if cat is not None:
    use = cat["use_dG26"] == b"T"
    print(f"  Zenodo 21977747 catalogue: {len(cat)} rows, {int(use.sum())} unique (use_dG26)")
    print("   columns:", ", ".join(cat.dtype.names))
    print("   -> no log g, no atmosphere T_eff, no n_H, no v_inf, no mass column.")
    has_T = np.isfinite(cat["Teff"][:, 2]) & use
    print(f"   MBB T per object exists for {int(has_T.sum())}/{int(use.sum())} (z<4.5 subset only)")

print("""
  MISSING (not public anywhere found):
   - per-object atmosphere T_eff, log g, L_bol, R_phot, M for the 117 BH*s (2609.09274
     fits 4 STACKS only; Sec.2: 'Individual BH* spectra are generally too noisy').
   - per-object CLOUDY layer density n_H for ANY sample (only population ranges quoted:
     n_H ~ 1e9-1e12 cm^-3).
   - per-object Gamma-free engine masses (gravity mass needs per-object log g).
   - v_inf for all 117: only 11 v_blue,95% (Naidu+ Table A1).""")

# =====================================================================================
# 1. KP2
# =====================================================================================
hdr("1. KP2 -- log v_inf vs log M (per object; mass PROXIED by luminosity)")
names = [r[0] for r in NAIDU]
v = np.array([-r[1] for r in NAIDU], float)
v_lo = np.array([-r[1] - r[2] for r in NAIDU], float)      # |v| lower bound
v_hi = np.array([-r[1] + r[3] for r in NAIDU], float)      # |v| upper bound
y = np.log10(v)
sy = 0.5 * np.log10(v_hi / v_lo)
print(f"  N = {len(v)} v_blue,95% values: min {v.min():.0f}, max {v.max():.0f} km/s; "
      f"max/min = {v.max() / v.min():.2f} ({np.log10(v.max() / v.min()):.2f} dex); "
      f"sd(log v) = {y.std(ddof=1):.3f} dex")
band = (v >= 350) & (v <= 588)
print(f"  registered band 350-588 km/s: {int(band.sum())}/{len(v)} inside; above: "
      f"{[n for n, vv in zip(names, v) if vv > 588]}; below: {[n for n, vv in zip(names, v) if vv < 350]}")
print("  registered spread across the stack mass band: x1.68 (M^1/4) vs x4.5 (M^1/2)")

print("""
  NO Gamma-free per-object mass exists.  Proxy: M ∝ L/Gamma with Gamma held constant
  (this is the framework's own KP2 premise: T pinned + log g mass-independent => Gamma
  fixed => L ∝ M, R_phot ∝ sqrt(M)).  Under that premise d log v/d log L = the KP2 slope.
  L_Halpha tracks L_bol with ~0.2 dex scatter (de Graaff+ 2026) -> sigma_x = 0.2 dex used
  for the attenuation correction.  If Gamma varies with L, these slopes are NOT M-slopes.""")

proxies = {}
proxies["P1 Matthee L_Ha,tot (N=11)"] = np.array([math.log10(MATTHEE[n][2] * 1e42) for n in names])
ok_nocliff = np.array([n != "The Cliff" for n in names])

dg = {}
if cat is not None:
    for n in names:
        ra, de, _ = MATTHEE[n]
        d = np.hypot((cat["ra"] - ra) * math.cos(math.radians(de)), cat["dec"] - de) * 3600
        j = np.where((d < 1.0) & use)[0]
        if len(j):
            k = j[0]
            dg[n] = dict(pid=int(cat["pid"][k]), srcid=int(cat["srcid"][k]), sep=float(d[k]),
                         logL5100=float(cat["logL_5100"][k][2]), logLHa=float(cat["logLHa_total"][k][2]),
                         logLMBB=float(cat["logL_MBB"][k][2]), mu=float(cat["mu"][k]))
    print(f"\n  cross-match Naidu x Zenodo (<1\", use_dG26): {len(dg)}/11 matched "
          f"(FRESCO-GN-9771, GN-15498, JADES-GN-38147 absent from the DJA PRISM catalogue)")
    for n in names:
        if n in dg:
            e = dg[n]
            print(f"   {n:20s} pid {e['pid']} src {e['srcid']:6d}  logL5100 {e['logL5100']:.2f}  "
                  f"logLHa {e['logLHa']:.2f}  logL_MBB {e['logLMBB']:.2f}  (Matthee logLHa "
                  f"{math.log10(MATTHEE[n][2] * 1e42):.2f})")
    print("   NB The Cliff: Matthee L_Ha,tot = 7e41 vs Zenodo 10^42.82 (0.97 dex apart) -- a proxy"
          "\n      inconsistency on the highest-leverage point; P1b drops it, P1c swaps it.")

rows = []


def run(label, x, yy, ss):
    N = len(x)
    b = ols(x, yy)
    sd, pc = boot_slope(x, yy)
    binv = 1.0 / ols(yy, x)
    varx = x.var(ddof=1)
    b_att = float(np.cov(x, yy)[0, 1] / (varx - 0.2 ** 2)) if varx > 0.2 ** 2 else float("nan")
    r = float(np.corrcoef(x, yy)[0, 1])
    p = perm_p(x, yy)
    bml, lo, hi, Lmin, bs, L = ml_scan(x, yy, ss, sx=0.2)
    L25 = float(L[np.argmin(abs(bs - 0.25))])
    L50 = float(L[np.argmin(abs(bs - 0.50))])
    d25, d50 = L25 - Lmin, L50 - Lmin
    print(f"\n  [{label}]  N={N}  x-range {np.ptp(x):.2f} dex")
    print(f"    OLS(y|x) slope = {b:.3f} +- {sd:.3f} (bootstrap; 68% [{pc[1]:.3f},{pc[3]:.3f}], "
          f"95% [{pc[0]:.3f},{pc[4]:.3f}])")
    print(f"    attenuation-corrected (sigma_x=0.2) = {b_att:.3f};  inverse OLS(x|y) = {binv:.3f}")
    print(f"    ML w/ intrinsic scatter: slope {bml:.3f}, 68% profile [{lo:.3f}, {hi:.3f}]")
    print(f"    Delta(-2lnL): slope 0.25 -> {d25:.2f};  slope 0.50 -> {d50:.2f};  "
          f"0.50 vs 0.25 -> {L50 - L25:+.2f}")
    s25 = m2lnL_profile(x, yy, ss, 0.25, 0.2, want_s=True)[1]
    s50 = m2lnL_profile(x, yy, ss, 0.50, 0.2, want_s=True)[1]
    print(f"    intrinsic scatter in log v needed: {s25:.2f} dex at slope 0.25, {s50:.2f} dex at 0.50"
          f"  (= object-to-object spread of v_inf/v_esc if the slope law held)")
    print(f"    Pearson r = {r:.2f}, permutation p = {p:.3f}")
    print(f"    0.25 sits {(b - 0.25) / sd:+.2f} sd, 0.50 sits {(b - 0.5) / sd:+.2f} sd from the OLS slope")
    rows.append(dict(label=label, N=N, ols=b, boot_sd=sd, boot_pct=[float(q) for q in pc],
                     slope_att=b_att, inverse=binv, ml=bml, ml68=[lo, hi], d2lnL_025=d25,
                     d2lnL_050=d50, r=r, perm_p=p, s_int_025=s25, s_int_050=s50))


x1 = proxies["P1 Matthee L_Ha,tot (N=11)"]
run("P1  Matthee L_Ha,tot, all", x1, y, sy)
run("P1b Matthee L_Ha,tot, no Cliff", x1[ok_nocliff], y[ok_nocliff], sy[ok_nocliff])
if "The Cliff" in dg:
    x1c = x1.copy()
    x1c[names.index("The Cliff")] = dg["The Cliff"]["logLHa"]
    run("P1c Matthee L_Ha, Cliff <- Zenodo", x1c, y, sy)
if dg:
    m = np.array([n in dg for n in names])
    run("P2  Zenodo L_5100 (matched)", np.array([dg[n]["logL5100"] for n in names if n in dg]), y[m], sy[m])
    run("P3  Zenodo L_Ha,tot (matched)", np.array([dg[n]["logLHa"] for n in names if n in dg]), y[m], sy[m])
out["KP2"] = dict(N=len(v), v=v.tolist(), names=names, in_band_350_588=int(band.sum()),
                  spread_ratio=float(v.max() / v.min()), fits=rows)

print("\n  stack-level cross-check with Gamma-FREE gravity masses (Sun+ Tables 2+4):")
print("    Luminous: |v95| 523 [402,774] (8 absorbers), logM_grav 4.3;  Inter: 364 [179,559]"
      " (2 absorbers), logM_grav 4.2")
print(f"    two-point slope = {math.log10(523 / 364) / 0.1:.1f} over Delta logM = 0.1 dex with "
      f">=0.2 dex v errors -> UNINFORMATIVE")

# =====================================================================================
# 2. KP3
# =====================================================================================
hdr("2. KP3 -- T_eff vs n_H against the repo's Saha front")


def saha_S(T, n):
    return 2.4e15 * T ** 1.5 * math.exp(-13.5984 * EV / (KB * T)) / n


def t_front(n):             # exactly the repo bisection (bhstar_t1 KP3)
    lo, hi = 3000.0, 12000.0
    for _ in range(60):
        T = (lo + hi) / 2
        if saha_S(T, n) > 0.5:
            hi = T
        else:
            lo = T
    return (lo + hi) / 2


def n_of_T(T):              # invert: the n_H at which T_front(n) = T
    lo, hi = 0.0, 16.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if t_front(10 ** mid) < T:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


for n in (1e9, 1e10, 1e11, 1e12):
    print(f"   Saha front: n_H = {n:.0e} cm^-3 -> T_front = {t_front(n):.0f} K")
print("\n  per-object (T_eff, n_H) pairs: NONE PUBLISHED -> the KP3 correlation test CANNOT RUN.")
print("  stack-level T_eff (no n_H attached) vs the curve:")
kp3 = []
for r in SUN:
    ln = n_of_T(r[2])
    d9, d12 = r[2] - t_front(1e9), r[2] - t_front(1e12)
    print(f"   {r[0]:9s} T_eff {r[2]} K: below T_front by {-d9:.0f} K (n=1e9) .. {-d12:.0f} K (n=1e12);"
          f" Saha-equivalent n_H = 10^{ln:.2f} cm^-3")
    kp3.append(dict(stack=r[0], T=r[2], dT_1e9=d9, dT_1e12=d12, log_n_equiv=ln))
nE = EGG["rho_ph_cgs"] / (MU * MP * 1e3)
print(f"   Egg (Liu+26; PHOTOSPHERIC model density, not the CLOUDY layer n_H): rho_ph 7e-12 g/cc ->"
      f" n_H = {nE:.1e}; T_front = {t_front(nE):.0f} K vs T_eff {EGG['T']} K")
print("  (the absolute offset below the front was pre-conceded in R-F1; only the per-object SLOPE"
      "\n   T_eff(n_H) is a test, and it needs per-object n_H that do not exist.)")
out["KP3"] = dict(status="NOT RUNNABLE: no per-object n_H (and no per-object atmosphere T_eff)",
                  curve={f"{n:.0e}": t_front(n) for n in (1e9, 1e10, 1e11, 1e12)}, stacks=kp3,
                  egg_photosphere=dict(n_H=nE, T_front=t_front(nE), T_eff=EGG["T"]))

# =====================================================================================
# 3. R-F3
# =====================================================================================
hdr("3. R-F3 -- Gamma = kappa_es sigma T^4 / (c g)  (stacks + the one per-object fit)")


def gamma(T, logg_cgs, kappa_cgs):
    return (kappa_cgs * 0.1) * SIGMA * T ** 4 / (C * 10 ** (logg_cgs - 2))


def ledd_sun(kappa_cgs):   # erg/s per Msun
    return 4 * math.pi * G * C * MSUN / (kappa_cgs * 0.1) * 1e7


print("  repo reproduction (median stack, log g -2.2 +- 0.2, kappa 0.40): "
      f"Gamma = {gamma(4662, -2.2, 0.4):.1f} in [{gamma(4662, -2.0, 0.4):.0f}, {gamma(4662, -2.4, 0.4):.0f}]")
rf3 = []
for kap in (0.40, 0.34):
    print(f"\n  kappa_es = {kap:.2f} cm^2/g")
    for r in SUN:
        nm, T, Tp, Tm, lg, gp, gm, lL, lM = r[0], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[12]
        G0 = gamma(T, lg, kap)
        Glo = gamma(T - Tm, lg + gp, kap)
        Ghi = gamma(T + Tp, lg - gm, kap)
        Gm = 10 ** lL / (ledd_sun(kap) * 10 ** lM)        # cross-check from Table-4 gravity mass
        inside = 36 <= G0 <= 90
        print(f"   {nm:9s} T {T} logg {lg:+.1f}: Gamma = {G0:6.1f}  [{Glo:5.1f}, {Ghi:6.1f}]"
              f"   (L/L_Edd(M_grav) = {Gm:6.1f})  in [36,90]: {inside}")
        rf3.append(dict(kappa=kap, obj=nm, Gamma=G0, lo=Glo, hi=Ghi, from_table_mass=Gm, in_36_90=inside))
    GE = gamma(EGG["T"], EGG["logg"], kap)
    GElo = gamma(EGG["T"] - EGG["Tm"], EGG["logg"] + EGG["gp"], kap)
    GEhi = gamma(EGG["T"] + EGG["Tp"], EGG["logg"] - EGG["gm"], kap)
    Gs = [gamma(EGG["T"], g_, kap) for g_ in EGG["logg_sens"]]
    print(f"   Egg (1 obj) T {EGG['T']} logg {EGG['logg']}: Gamma = {GE:6.1f}  [{GElo:5.1f}, {GEhi:6.1f}]"
          f"  sensitivity runs {min(Gs):.0f}-{max(Gs):.0f}  in [36,90]: {36 <= GE <= 90}")
    rf3.append(dict(kappa=kap, obj="Egg", Gamma=GE, lo=GElo, hi=GEhi, sens=[min(Gs), max(Gs)],
                    in_36_90=36 <= GE <= 90))
for kap in (0.40, 0.34):
    st = [d for d in rf3 if d["kappa"] == kap and d["obj"] != "Egg"]
    print(f"\n  kappa {kap:.2f}: stack central Gamma span {min(d['Gamma'] for d in st):.1f}-"
          f"{max(d['Gamma'] for d in st):.1f}; {sum(d['in_36_90'] for d in st)}/4 stacks inside [36,90]; "
          f"median-stack Gamma {st[0]['Gamma']:.1f} vs the paper's dial cap 50 "
          f"({'above' if st[0]['Gamma'] > 50 else 'below'}); from Table-4 rounded mass: {st[0]['from_table_mass']:.1f}")
print("""
  caveats: (i) g is the NET gravity g - g_dyn (Sun+ Sec.2.2), so this is a net-gravity
  Gamma; an outflow inflates g and deflates Gamma.  (ii) stacks are medians of 15-85
  objects -- the per-object spread is at least as wide and is NOT measurable from the
  public data.  (iii) the Egg is a z~0.1 LRD outside the 117 and its fit includes host +
  dust components.""")
out["RF3"] = rf3

p = os.path.join(HERE, "L325_lrd_per_object_kp_doors_results.json")
with open(p, "w") as fh:
    json.dump(out, fh, indent=1, default=float)
print(f"\nresults -> {os.path.basename(p)}")
