#!/usr/bin/env python3
"""
G1 -- characterize the REAL public Gaia asteroid astrometry we'd fit.
Queries the Gaia DR3 Solar-System-Object tables (public) to get: number of asteroids,
observations per object, along-scan astrometric precision, and the epoch baseline.
This turns the order-of-magnitude feasibility into real numbers. Bounded queries + timeout.
"""
import sys
from astroquery.gaia import Gaia
Gaia.ROW_LIMIT = -1

def q(adql, label):
    try:
        job = Gaia.launch_job(adql)
        r = job.get_results()
        print(f"[{label}] rows={len(r)}")
        return r
    except Exception as e:
        print(f"[{label}] FAILED: {e}")
        return None

print("="*70)
print("Gaia DR3 Solar System Objects -- real data characterization")
print("="*70)

# 1. how many asteroids (sso_source), how many total observations
r = q("SELECT COUNT(*) AS n_ast FROM gaiadr3.sso_source", "sso_source count")
if r is not None: print("   asteroids in sso_source:", int(r['n_ast'][0]))

r = q("SELECT COUNT(*) AS n_obs FROM gaiadr3.sso_observation", "sso_observation count")
if r is not None: print("   total epoch observations:", int(r['n_obs'][0]))

# 2. epoch baseline + along-scan precision from a sample
r = q("SELECT MIN(epoch_utc) AS tmin, MAX(epoch_utc) AS tmax FROM gaiadr3.sso_observation", "epoch range")
if r is not None:
    print(f"   epoch_utc range: {r['tmin'][0]} .. {r['tmax'][0]} (JD-2455197.5 days)")

# along-scan (AL) position uncertainty is the precise axis; sample it
r = q("SELECT TOP 20000 position_angle_scan, ra, dec, "
      "x_gaia_geocentric, y_gaia_geocentric, z_gaia_geocentric "
      "FROM gaiadr3.sso_observation", "sample obs")
if r is not None:
    print("   sample columns available:", list(r.colnames)[:12])

# 3. observations-per-asteroid distribution
r = q("SELECT number_mp, num_of_obs FROM gaiadr3.sso_source WHERE num_of_obs > 0 ORDER BY num_of_obs DESC", "obs per source")
if r is not None:
    import numpy as np
    nobs = np.array(r['num_of_obs'])
    print(f"   obs/asteroid: median={np.median(nobs):.0f}, mean={nobs.mean():.0f}, "
          f"max={nobs.max()}, N with >=20 obs = {(nobs>=20).sum()}")
print("\nDone -- this tells us N_ast, N_obs, baseline, precision for the real feasibility.")
