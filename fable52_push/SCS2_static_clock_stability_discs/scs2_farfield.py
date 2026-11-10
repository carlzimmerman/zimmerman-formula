"""SCS2 (reported, not graded): where the external-field brackets' negative D.P comes from.

1. Closed form (sympy, exact). In a uniform external field g_e along e, the law's linearised far field (the solver's own
   Dirichlet data) is Phi = g_e x_par + phi1, phi1 = -A / s, s = sqrt(r_perp^2 + x_par^2/(1 + L_e)), L_e = 1/(1 + g_e/a0).
   phi1 solves the linearised equation (d_perp^2 + (1 + L_e) d_par^2) phi1 = 0 off the source, so
       K D.P = lap Phi = -L_e d_par^2 phi1 = -L_e A [r_perp^2 - 2 x_par^2/(1 + L_e)] / ((1 + L_e) s^5),
   negative wherever r_perp^2 > 2 x_par^2/(1 + L_e): a band around the plane through the disc perpendicular to the field
   (angle from the field's axis above arctan sqrt(2/(1 + L_e)), about 45 degrees), positive in cones along the axis.
2. The solved maps (fine grids, axial field): of the off-plane cells at r >= 3 r_e, the share of negative cells inside the
   predicted band, and the share of band cells that are negative. Near the disc (r < 3 r_e) the rest of the negative charge
   sits at the null of the total field on the axis, on the side where the disc's pull opposes g_e.
Reads $SCS2_CACHE. TEST lane; adopts nothing.
"""
import os, sys, json, glob, math, time
import numpy as np
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scs2_aqual as S

CACHE = os.environ.get("SCS2_CACHE", os.path.join(HERE, "_cache"))
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))
t0 = time.time()

# ---- 1. closed form
x, y, z, A, L = sp.symbols("x y z A L", real=True)
s = sp.sqrt(x ** 2 + y ** 2 + z ** 2 / (1 + L))             # field along z
phi1 = -A / s
lin = sp.simplify(sp.diff(phi1, x, 2) + sp.diff(phi1, y, 2) + (1 + L) * sp.diff(phi1, z, 2))
lap = sp.diff(phi1, x, 2) + sp.diff(phi1, y, 2) + sp.diff(phi1, z, 2)
claim = -L * A * (x ** 2 + y ** 2 - 2 * z ** 2 / (1 + L)) / ((1 + L) * s ** 5)
ok_lin = sp.simplify(lin) == 0
ok_lap = sp.simplify(lap - claim) == 0
P_(f"closed form: phi1 solves the linearised equation: {ok_lin}; K D.P = -L A [r_perp^2 - 2 z^2/(1+L)]/((1+L) s^5): {ok_lap}")

# ---- 2. the maps
G = S.G
rows = []
for f in sorted(glob.glob(os.path.join(CACHE, "bracket_EF_axis_*_z_.npz"))):
    tag = os.path.basename(f)[:-4]
    bg = S.load_cache(f); g = bg["g"]; dp = bg["dp"]
    ge = bg["ge"]; a0 = bg["a0"]; M = bg["M"]
    re = math.sqrt(G * M * a0) / (ge * a0)
    Le = 1.0 / (1.0 + ge)                                       # ge is in units of a0
    R = g.R[..., 0]; Z = g.Z[..., 0]; r = np.sqrt(R ** 2 + Z ** 2); d = dp[..., 0]
    ok = np.isfinite(d); ok[:, [g.nt // 2 - 1, g.nt // 2]] = False   # plane cells (full theta grid)
    far = ok & (r >= 3 * re)
    band = R ** 2 > 2 * Z ** 2 / (1 + Le)
    scale = np.nanmax(np.abs(d[ok]))
    neg = d < -1e-6 * scale                                     # the frozen map threshold
    n_neg_far = int(np.sum(far & neg)); n_band_far = int(np.sum(far & band))
    raw = d < 0                                                 # sign alone (the far field is far below the threshold at 0.01 a0)
    in_band_raw = float(np.sum(far & raw & band) / max(int(np.sum(far & raw)), 1))
    band_neg_raw = float(np.sum(far & band & raw) / max(n_band_far, 1))
    axis_cone = far & ~band
    cone_pos_raw = float(np.sum(axis_cone & (d > 0)) / max(int(np.sum(axis_cone)), 1))
    in_band = float(np.sum(far & neg & band) / max(n_neg_far, 1))
    band_neg = float(np.sum(far & band & neg) / max(n_band_far, 1))
    near_neg = ok & neg & (r < 3 * re)
    Rn = R[near_neg]; Zn = Z[near_neg]
    rows.append(dict(tag=tag, r_e_kpc=re, L_e=Le, far_negative_cells=n_neg_far, far_negative_in_band=in_band,
                     far_band_cells_negative=band_neg, far_negative_in_band_sign_only=in_band_raw,
                     far_band_cells_negative_sign_only=band_neg_raw, far_axis_cone_cells_positive_sign_only=cone_pos_raw,
                     near_negative_cells=int(near_neg.sum()),
                     near_negative_z_sign=sorted(set(np.sign(Zn).astype(int).tolist())),
                     near_negative_r_over_re=[float(np.sqrt(Rn ** 2 + Zn ** 2).min() / re), float(np.sqrt(Rn ** 2 + Zn ** 2).max() / re)] if near_neg.any() else None))
    P_(f"[{tag}] r_e {re:.1f} kpc; r >= 3 r_e: {n_neg_far} negative cells, {in_band:.3f} of them in the band; "
       f"{band_neg:.3f} of band cells negative; by sign alone {in_band_raw:.3f} in band, {band_neg_raw:.3f} of band negative, "
       f"{cone_pos_raw:.3f} of axis-cone cells positive; r < 3 r_e: {int(near_neg.sum())} negative cells")
mn_in = min(r_["far_negative_in_band"] for r_ in rows if r_["far_negative_cells"] > 0)
mn_bn = min(r_["far_band_cells_negative"] for r_ in rows)
mn_in_raw = min(r_["far_negative_in_band_sign_only"] for r_ in rows)
mn_bn_raw = min(r_["far_band_cells_negative_sign_only"] for r_ in rows)
mn_cone = min(r_["far_axis_cone_cells_positive_sign_only"] for r_ in rows)
P_(f"far field (r >= 3 r_e), all {len(rows)} axial backgrounds: negative cells (frozen threshold) inside the predicted band "
   f">= {mn_in:.3f}; band cells negative (threshold) >= {mn_bn:.3f}; by sign alone: negative cells in the band >= "
   f"{mn_in_raw:.3f}, band cells negative >= {mn_bn_raw:.3f}, axis-cone cells positive >= {mn_cone:.3f}")
RES = dict(lane="SCS2", script="scs2_farfield.py", closed_form=dict(solves_linearised=bool(ok_lin), laplacian_identity=bool(ok_lap)),
           rows=rows, min_far_negative_in_band=mn_in, min_far_band_negative=mn_bn, min_far_negative_in_band_sign_only=mn_in_raw,
           min_far_band_negative_sign_only=mn_bn_raw, min_far_axis_cone_positive_sign_only=mn_cone, seconds=round(time.time() - t0, 1),
           footer="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "scs2_farfield.json"), "w") as fh:
    json.dump(RES, fh, indent=1)
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "scs2_farfield.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
