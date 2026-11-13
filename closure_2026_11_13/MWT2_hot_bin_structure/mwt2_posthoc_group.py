#!/usr/bin/env python3
"""
MWT2 POST HOC (not graded; changes no label): what does the 30-40 kpc cold component look like?
Re-fits step (a)'s two-Gaussian model on the 30-40 bin (same deterministic code, taken from mwt2.py by AST) and
prints the cold component's members' distribution in Sagittarius coordinates, sky, distance and [Fe/H].
Usage: python3 -I -B mwt2_posthoc_group.py <path to MWS_BHB.fits>  -> mwt2_posthoc_group.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, ast, warnings
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
RAW1 = os.path.normpath(os.path.join(HERE, "..", "..", "closure_2026_11_12", "RAW1_halo_stars_direct"))
FITS = sys.argv[1]
sys.path.insert(0, RAW1)
def defs(path, keep_assign=()):
    t = ast.parse(open(path).read())
    return ast.Module(body=[n for n in t.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef)) or
                            (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in keep_assign)], type_ignores=[])
R1 = {"FITS": FITS, "HERE": RAW1, "__name__": "raw1_functions"}
exec(compile(defs(os.path.join(RAW1, "raw1.py"), ("K474", "BINS", "NOMINAL", "FOOT", "SG", "NGRID", "_GCACHE")), "raw1.py", "exec"), R1)
M2 = {"__name__": "mwt2_functions", "np": np}
exec(compile(defs(os.path.join(HERE, "mwt2.py")), "mwt2.py", "exec"), M2)
out = open(os.path.join(HERE, "mwt2_posthoc_group.out"), "w")
def say(s): print(s); out.write(s + "\n")
from astropy.coordinates import SkyCoord
import astropy.units as u
D = R1["load"]()
from astropy.io import fits
D["feh"] = np.asarray(fits.open(FITS, memmap=False)["RVTAB"].data["FEH"], float)
c = SkyCoord(ra=D["ra"] * u.deg, dec=D["dec"] * u.deg, frame="icrs").galactic
D["l"], D["b"] = c.l.deg, c.b.deg; D["lsgr"], D["bsgr"] = R1["sgr_lat_lon"](D["l"], D["b"])
S = R1["build"](D, dict(R1["NOMINAL"]))
for k in ("l", "b", "lsgr", "bsgr", "feh"): S[k] = D[k][S["i"]]
m = (S["r"] >= 30) & (S["r"] < 40); v = S["vgsr"][m]; e2 = S["verr"][m] ** 2
f2 = M2["xd2"](v, e2); g, h = M2["order"](f2, v); q = g["q"]
say(f"30-40 kpc: N {m.sum()}; cold component w {g['w']:.3f} mu {g['mu']:+.1f} s {g['s']:.1f}; halo w {h['w']:.3f} mu {h['mu']:+.1f} s {h['s']:.1f} (as mwt2.out)")
G, H = q >= 0.8, q <= 0.2
for nm, k in (("Lambda_Sgr", "lsgr"), ("B_Sgr", "bsgr"), ("l", "l"), ("b", "b"), ("r", "r"), ("[Fe/H]", "feh")):
    a, b_ = S[k][m][G], S[k][m][H]
    say(f"  {nm:10s} cold core (N {G.sum()}): 16/50/84 pct {np.nanpercentile(a, 16):7.1f} {np.nanpercentile(a, 50):7.1f} {np.nanpercentile(a, 84):7.1f}"
        f" | halo core (N {H.sum()}): {np.nanpercentile(b_, 16):7.1f} {np.nanpercentile(b_, 50):7.1f} {np.nanpercentile(b_, 84):7.1f}")
say(f"  fraction with |B_Sgr| < 25 deg: cold {np.mean(np.abs(S['bsgr'][m][G]) < 25):.2f}, halo {np.mean(np.abs(S['bsgr'][m][H]) < 25):.2f}")
say(f"  fraction in the northern Galactic hemisphere: cold {np.mean(S['b'][m][G] > 0):.2f}, halo {np.mean(S['b'][m][H] > 0):.2f}")
say("  cold-core stars (Lambda_Sgr, B_Sgr, l, b, r, v_gsr), sorted by Lambda_Sgr:")
ii = np.argsort(S["lsgr"][m][G])
for j in ii:
    say(f"    {S['lsgr'][m][G][j]:6.1f} {S['bsgr'][m][G][j]:+6.1f} {S['l'][m][G][j]:6.1f} {S['b'][m][G][j]:+6.1f} {S['r'][m][G][j]:5.1f} {v[G][j]:+7.1f}")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
out.close()
