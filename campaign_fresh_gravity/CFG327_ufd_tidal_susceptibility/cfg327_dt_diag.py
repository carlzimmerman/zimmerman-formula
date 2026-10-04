"""CFG327 post-run diagnostic (labelled POST HOC; changes no verdict): why C2 failed. Re-integrates every orbit at dt = 0.25 Myr
(canonical footing) and compares pericentres; reports the worst |dE/E| with |E|/|phi| (near-zero-energy orbits inflate dE/E)."""
import io, contextlib, os, numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg327_tidal.py")).read().split("rng = np.random.default_rng(327)")[0]
g = {"__file__": os.path.join(HERE, "cfg327_tidal.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "cfg327_tidal.py", "exec"), g)
A0, a0 = g["A0"], g["A0"]["canonical"]
worst, drp = [], []
for d in g["RES"]:
    c = SkyCoord(ra=d["ra"] * u.deg, dec=d["dec"] * u.deg, distance=10 ** (d["dm"] / 5 + 1) * u.pc, pm_ra_cosdec=d["pmra"] * u.mas / u.yr,
                 pm_dec=d["pmdec"] * u.mas / u.yr, radial_velocity=d["vlos"] * u.km / u.s).transform_to(g["gc"])
    x = np.array([c.x.to(u.m).value, c.y.to(u.m).value, c.z.to(u.m).value]); v = np.array([c.v_x.to(u.m / u.s).value, c.v_y.to(u.m / u.s).value, c.v_z.to(u.m / u.s).value])
    rp1, E1 = g["integrate"](x, v, a0, dt=0.5); rp2, E2 = g["integrate"](x, v, a0, dt=0.25)
    ph = g["phi"](np.linalg.norm(x), a0); E0 = 0.5 * v @ v + ph
    drp.append(abs(rp2 / rp1 - 1)); worst.append((E1, E2, abs(E0) / abs(ph), d["name"]))
worst.sort(reverse=True)
print(f"POST HOC: max |r_p(dt 0.25)/r_p(dt 0.5) - 1| over {len(drp)} orbits = {max(drp):.2e}")
for e1, e2, r, n in worst[:4]:
    print(f"  {n:20s} dE/E {e1:.2e} (dt 0.5) {e2:.2e} (dt 0.25)  |E|/|phi| {r:.3f}")
