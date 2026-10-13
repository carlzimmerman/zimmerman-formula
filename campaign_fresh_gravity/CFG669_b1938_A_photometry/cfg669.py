#!/usr/bin/env python3
"""CFG669: independent F277W photometry of B1938+666 perturber A (criteria 899403b81), scoring the sealed CFG668 prediction.
Run with python3 -I. Reads the GO 8281 F277W level-3 mosaic (memory-mapped cutout only).
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, math
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data", "cfg668_go8281")
IMG = os.path.join(DATA, "jw08281-o001_t001_nircam_clear-f277w_i2d.fits")
CAT = os.path.join(DATA, "jw08281-o001_t001_nircam_clear-f277w_cat.ecsv")
MUT = os.environ.get("CFG669_MUTATE", "0") == "1"
TAG = ("_MUTATE" if MUT else "") + ("_FROZENCENTRE" if os.environ.get("CFG669_CENTRE") == "frozen" else "")
PRED = {"canonical": {"faint": 29.63, "excl": 30.82}, "alt": {"faint": 29.77, "excl": 30.96}}
R_AP, R_IN, R_OUT, EE = 0.075, 0.10, 0.18, 0.60
OUT, RES = [], {"lane": "CFG669", "criteria": "899403b81", "scores": "CFG668 9162427f", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


hd = fits.open(IMG, memmap=True)
sci = hd["SCI"]; w = WCS(sci.header); pixar = sci.header.get("PIXAR_SR") or hd[0].header.get("PIXAR_SR")
scale = math.sqrt(pixar) * 206264.806                              # arcsec / pixel
P(f"F277W mosaic {sci.data.shape}, pixel {scale:.4f}\", PIXAR_SR {pixar:.4e}, BUNIT {sci.header.get('BUNIT')}")

cat = Table.read(CAT)
sc = cat["sky_centroid"]
tgt = SkyCoord(294.6050 * u.deg, 66.8146 * u.deg)
i = int(np.argmin(sc.separation(tgt).arcsec)); c0 = sc[i]
P(f"catalogue source nearest target: id {cat['label'][i] if 'label' in cat.colnames else i}, sep {sc[i].separation(tgt).arcsec:.2f}\"")
x0, y0 = w.world_to_pixel(c0)
H = int(round(4.0 / scale))
xc, yc = int(round(float(x0))), int(round(float(y0)))
cut = np.array(sci.data[yc - H:yc + H + 1, xc - H:xc + H + 1], dtype=float)
cut[~np.isfinite(cut)] = np.nan
ox, oy = xc - H, yc - H
yy, xx = np.mgrid[0:cut.shape[0], 0:cut.shape[1]]
r1 = int(round(1.0 / scale))
m = (xx - H) ** 2 + (yy - H) ** 2 <= r1 ** 2
CENTRE = os.environ.get("CFG669_CENTRE", "nucleus")
if CENTRE == "frozen":                                   # the frozen rule: brightest pixel within 1" (locks onto a ring knot)
    yb, xb = np.unravel_index(np.nanargmax(np.where(m, cut, -np.inf)), cut.shape)
else:                                                    # DISCLOSED DEVIATION (README): the nucleus = local maximum nearest the
    bx = int(round(1.2 / scale)); sbox = cut[H - bx:H + bx + 1, H - bx:H + bx + 1] - np.nanmedian(cut)   # flux-weighted
    sbox = np.clip(np.nan_to_num(sbox), 0, None); gyy, gxx = np.mgrid[-bx:bx + 1, -bx:bx + 1]          # centre of the
    cx, cy = H + (sbox * gxx).sum() / sbox.sum(), H + (sbox * gyy).sum() / sbox.sum()                    # lens + ring
    pk = [(j, k) for j in range(H - r1, H + r1 + 1) for k in range(H - r1, H + r1 + 1)
          if m[j, k] and np.isfinite(cut[j, k]) and cut[j, k] == np.nanmax(cut[j - 1:j + 2, k - 1:k + 2])]
    yb, xb = min(pk, key=lambda p: (p[1] - cx) ** 2 + (p[0] - cy) ** 2)
s = cut[yb - 2:yb + 3, xb - 2:xb + 3]; gy, gx = np.mgrid[-2:3, -2:3]
lx, ly = xb + (s * gx).sum() / s.sum(), yb + (s * gy).sum() / s.sum()
lens = w.pixel_to_world(lx + ox, ly + oy)
P(f"lens centre RA {lens.ra.deg:.6f} Dec {lens.dec.deg:.6f}")


def offset_pix(dn, dw):
    """pixel position of lens + (dn arcsec north, dw arcsec west)"""
    c = lens.spherical_offsets_by(-dw * u.arcsec, dn * u.arcsec)
    px, py = w.world_to_pixel(c)
    return float(px) - ox, float(py) - oy


SUB = 5
def apsum(img, x, y, r):
    """sub-pixel (5x5) sampled circular aperture sum and area (pixels)"""
    R = int(r / scale) + 2; X, Y = int(round(x)), int(round(y))
    tot, area = 0.0, 0.0
    off = (np.arange(SUB) + 0.5) / SUB - 0.5
    for j in range(Y - R, Y + R + 1):
        for k in range(X - R, X + R + 1):
            fr = np.mean(((k + off[None, :] - x) ** 2 + (j + off[:, None] - y) ** 2) <= (r / scale) ** 2)
            if fr > 0:
                tot += fr * img[j, k]; area += fr
    return tot, area


def excess(img, x, y):
    a, area = apsum(img, x, y, R_AP)
    d2 = ((xx - x) ** 2 + (yy - y) ** 2) * scale ** 2
    ann = img[(d2 >= R_IN ** 2) & (d2 <= R_OUT ** 2)]
    ann = ann[np.isfinite(ann)]
    for _ in range(5):
        med, sd = np.median(ann), np.std(ann); ann = ann[np.abs(ann - med) <= 3 * sd]
    return a - np.median(ann) * area


def to_jy(v):                                   # sum of MJy/sr pixels -> Jy
    return v * 1e6 * pixar


def ab(jy):
    return -2.5 * math.log10(jy / 3631.0) if jy > 0 else float("inf")


def measure(img, dn, dw, label):
    ax, ay = offset_pix(dn, dw)
    rad = math.hypot(ax - lx, ay - ly); phA = math.atan2(ay - ly, ax - lx)
    EA = excess(img, ax, ay); ref = []
    for k in range(36):
        ph = math.radians(10 * k); px, py = lx + rad * math.cos(ph), ly + rad * math.sin(ph)
        if math.hypot(px - ax, py - ay) * scale < 0.25:
            continue
        ref.append(excess(img, px, py))
    ref = np.array(ref); sig = 1.4826 * np.median(np.abs(ref - np.median(ref)))
    S = EA / sig; rank = int((ref < EA).sum())
    mA = ab(to_jy(EA) / EE); mlim = ab(to_jy(2 * sig) / EE)
    d = dict(label=label, A_pix=[ax + ox, ay + oy], radius_arcsec=rad * scale, n_ref=len(ref), E_A_Jy=to_jy(EA),
             sigma_emp_Jy=to_jy(sig), S=S, rank_of_A=f"{rank}/{len(ref)}", m_A=mA, m_lim_2sig=mlim)
    P(f"  [{label}] A at r = {rad*scale:.3f}\": E_A = {to_jy(EA):.3e} Jy, sigma_emp = {to_jy(sig):.3e} Jy (n={len(ref)}), "
      f"S = {S:.2f}, A ranks above {rank}/{len(ref)}; m_A = {mA:.2f} AB, 2sig limit = {mlim:.2f} AB")
    return d


img = cut.copy()
if MUT:
    ax, ay = offset_pix(0.576, 0.036); sg = 0.092 / scale / 2.3548
    G = np.exp(-((xx - ax) ** 2 + (yy - ay) ** 2) / (2 * sg ** 2)); G /= G.sum()
    for mag in (28.0, 29.6):
        inj = img + G * (3631.0 * 10 ** (-0.4 * mag)) / (1e6 * pixar)
        RES[f"inject_{mag}"] = measure(inj, 0.576, 0.036, f"MUTATE inject {mag} AB")
    r = RES["inject_28.0"]; bite = r["S"] >= 3 and abs(r["m_A"] - 28.0) <= 0.5
    P(f"MUTATE: 28.0 AB injection {'RECOVERED (bites)' if bite else 'NOT recovered'}")
    RES["bite"] = bite
else:
    RES["primary"] = measure(img, 0.576, 0.036, "primary: 0.576 N, 0.036 W")
    RES["alt_E"] = measure(img, 0.576, -0.036, "robust: 0.576 N, 0.036 E")
    RES["alt_swap"] = measure(img, 0.036, 0.576, "robust: 0.036 N, 0.576 W (axes swapped)")
    pr = RES["primary"]
    for f, p in PRED.items():
        if pr["S"] >= 3 and pr["m_A"] <= p["faint"]:
            v = "SURVIVES"
        elif pr["S"] < 2 and pr["m_lim_2sig"] > p["excl"]:
            v = "EXCLUDED"
        elif pr["m_lim_2sig"] < p["faint"]:
            v = "NOT DIAGNOSTIC"
        else:
            v = "TENSION"
        RES[f"verdict_{f}"] = v; P(f"VERDICT ({f}): {v}  [crude independent measurement; not the PI team's lens+light model]")
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        Z = int(round(1.2 / scale)); ax_, ay_ = offset_pix(0.576, 0.036)
        sub = img[int(ly) - Z:int(ly) + Z + 1, int(lx) - Z:int(lx) + Z + 1]
        fig, a = plt.subplots(figsize=(5, 5))
        a.imshow(np.arcsinh(sub / np.nanpercentile(sub, 99) * 20), origin="lower", cmap="gray")
        a.add_patch(plt.Circle((ax_ - int(lx) + Z, ay_ - int(ly) + Z), R_AP / scale, fill=False, color="r"))
        a.set_title("B1938+666 F277W (GO 8281); red = A aperture"); a.set_xticks([]); a.set_yticks([])
        fig.savefig(os.path.join(HERE, f"cfg669_cutout{TAG}.png"), dpi=120, bbox_inches="tight")
    except Exception as e:
        P(f"(figure skipped: {e})")

json.dump(RES, open(os.path.join(HERE, f"cfg669_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg669{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit((1 if RES.get("bite") else 0) if MUT else 0)
