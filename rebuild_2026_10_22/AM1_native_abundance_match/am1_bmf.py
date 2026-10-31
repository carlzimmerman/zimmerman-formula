#!/usr/bin/env python3
"""AM1 step 1: the measured baryonic mass function from GAMA G3C + KiDS-bright, by P2's own text through its mass definitions. Writes am1_bmf.json. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
HERE1 = os.path.dirname(os.path.abspath(__file__)); RB1 = os.path.dirname(HERE1); P2 = os.path.join(RB1, "P2_spec_isolated_lensing", "p2_spec_isolated_lensing.py"); T = open(P2).read(); END = "lMb_g = lMb_nat(lMa, z_g)"; assert T.count(END) == 1
src = T[:T.index(END)] + END + "\n"; sys.argv = [P2, "unused_cache", "unused_work", "--phase=B"]; G = {"__file__": P2, "__name__": "p2_head"}; exec(compile(src, P2, "exec"), G)
np, math = G["np"], G["math"]; BOX = G["BOX"]; z_g, rp_g, lMa, lMb_g, CHI_N, DL_70, ZZ = (G[k] for k in ("z_g", "rp_g", "lMa", "lMb_g", "CHI_N", "DL_70", "ZZ")); RK, GR = G["G_RANKIC"], G["G_GROUP"]; lMsn = G["lMs_nat"](lMa, z_g); OUT = []
def P_(s): print(s, flush=True); OUT.append(s)
AREA = np.array([(math.radians(b - a)) * (math.sin(math.radians(d)) - math.sin(math.radians(c))) for a, b, c, d in BOX.values()]); OMEGA = float(AREA.sum())
zg_ = np.linspace(0.0, 0.8, 8001); DLg = DL_70(zg_); DLz = DL_70(z_g); zmax = np.clip(np.interp(DLz * 10 ** ((19.8 - rp_g) / 5), DLg, zg_), z_g, 0.30)
Vmax = OMEGA / 3 * (CHI_N(zmax) ** 3 - CHI_N(0.02) ** 3); zsel = (z_g > 0.02) & (z_g < 0.30)
rho = float(np.sum((10 ** lMb_g / Vmax)[zsel & (lMa >= 8.0)])); k2 = abs(rho / 2.959e8 - 1) <= 1e-3; P_(f"K2 P2's formula and cuts: rho_b,gal {rho:.4e} vs printed 2.959e8: {'PASS' if k2 else 'FAIL'}")
fg = 10 ** (-0.69 * lMa + 6.63); lMbc = lMsn + np.log10(1 + fg); cen = (GR == 0) | (RK == 1); P_(f"G3C in the boxes {len(z_g):,}; in z range {int(zsel.sum()):,}; centrals or ungrouped {int((zsel & cen).sum()):,} ({np.mean(cen[zsel]):.3f}); RankIterCen values {sorted(set(np.unique(RK).tolist()))[:4]}; area {OMEGA:.5f} sr")
GRID = np.arange(7.5, 12.8001, 0.05)
Vlow = OMEGA / 3 * (CHI_N(np.minimum(zmax, 0.15)) ** 3 - CHI_N(0.02) ** 3)
def cum(s, x, V=None): V = Vmax if V is None else V; w = 1 / V[s]; o = np.argsort(x[s])[::-1]; xs, c = x[s][o], np.cumsum(w[o]); return np.interp(-GRID, -xs, c, left=0.0, right=float(c[-1])).tolist()
S = dict(grid=GRID.tolist(), cen=cum(zsel & cen, lMbc), all=cum(zsel, lMbc), cen_zlow=cum((z_g > 0.02) & (z_g < 0.15) & cen, lMbc, Vlow), cen_plus=cum(zsel & cen, lMbc + 0.2), cen_minus=cum(zsel & cen, lMbc - 0.2), k2=bool(k2), n=int((zsel & cen).sum()))
for lg in (9.0, 9.5, 10.0, 10.5, 11.0, 11.5): P_(f"  n_b(> 10^{lg}): centrals {np.interp(lg, GRID, S['cen']):.3e}, all {np.interp(lg, GRID, S['all']):.3e} /Mpc^3; z < 0.15 centrals {np.interp(lg, GRID, S['cen_zlow']):.3e}")
json.dump(S, open(os.path.join(HERE1, "am1_bmf.json"), "w")); open(os.path.join(HERE1, "am1_bmf.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if k2 else 1)
