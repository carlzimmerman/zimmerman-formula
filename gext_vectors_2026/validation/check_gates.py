#!/usr/bin/env python3
"""Standalone gate checker: recomputes GATE-A and GATE-B from the DELIVERED CSV
(data/gext_vectors.csv) against Chae 2021's published amplitudes. No estimator rerun,
no hard-coded pass values -- everything below is computed. exit 0 always (the numbers
are the report; thresholds are stated, not asserted)."""
import csv, numpy as np

BASE = '/Users/carlzimmerman/new_physics/gext_vectors_2026'
CHAE_ENV = ('/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews/'
            'directional_efe_2026/laneB_data/chae21_env.csv')

def cart(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec)
    return np.array([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)])

ours = {r['name']: r for r in csv.DictReader(open(BASE + '/data/gext_vectors.csv'))}
chae = {r['galaxy'].strip(): r for r in csv.DictReader(open(CHAE_ENV))}
m = sorted(set(ours) & set(chae))
print(f"GATE-A: {len(m)}/{len(chae)} Chae galaxies matched by name")
for col in ('maxclu', 'noclu'):
    x = np.array([float(ours[n]['log_eN_' + col]) for n in m])
    y = np.array([float(chae[n]['log_eN_' + col]) for n in m])
    off = np.median(y - x)
    print(f"  {col}: Pearson r = {np.corrcoef(x,y)[0,1]:.3f}, global offset = {off:+.3f} dex, "
          f"scatter (std after offset) = {np.std(y-x-off):.3f} dex  "
          f"[targets: r >~ 0.8, scatter <~ 0.3]")

print("GATE-B (from delivered vectors):")
for label, aradec, aD, rad in [('Virgo', (187.70, 12.34), 16.5, 20.0),
                               ('Coma', (194.95, 27.98), 100.0, 30.0)]:
    apos = cart(*aradec) * aD
    angs = []
    for r in ours.values():
        p = cart(float(r['ra']), float(r['dec'])) * float(r['D'])
        sep = np.linalg.norm(p - apos)
        if 1.0 < sep < rad:
            t = (apos - p) / np.linalg.norm(apos - p)
            u = np.array([float(r['ux_icrs']), float(r['uy_icrs']), float(r['uz_icrs'])])
            angs.append(np.degrees(np.arccos(np.clip(np.dot(u, t), -1, 1))))
    print(f"  {label}: n = {len(angs)}, median angle(g_vec -> {label}) = "
          f"{np.median(angs):.1f} deg (random would be 90)")
