#!/usr/bin/env python3
"""Phase-1 driver: build gext_vectors.csv for all SPARC galaxies + run GATE-A / GATE-B.
No hard-coded pass thresholds are asserted; gates are COMPUTED and reported."""
import csv, sys, numpy as np
sys.path.insert(0, '/Users/carlzimmerman/new_physics/gext_vectors_2026/src')
from gext_estimator import (GextEstimator, radec_to_cart, R_ICRS2SG, A0, H0,
                            lf_visible_fraction)

BASE = '/Users/carlzimmerman/new_physics/gext_vectors_2026'
RAW  = BASE + '/data/raw'
CHAE_ENV = ('/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews/'
            'directional_efe_2026/laneB_data/chae21_env.csv')

# ---- SPARC positions ----
def load_sparc():
    rows = []
    with open(RAW + '/sparc_table1_vizier.tsv') as fh:
        for ln in fh:
            if ln.startswith('#') or not ln.strip(): continue
            p = ln.rstrip('\n').split('\t')
            if len(p) < 9: continue
            try:
                D = float(p[1]); ra = float(p[7]); dec = float(p[8])
            except ValueError:
                continue
            rows.append(dict(name=p[0].strip(), D=D, ra=ra, dec=dec))
    return rows

def main():
    catalog_mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    write_csv = '--write' in sys.argv
    sparc = load_sparc()
    print(f"catalog_mode = {catalog_mode}")
    print(f"SPARC galaxies with coordinates: {len(sparc)}")
    est = GextEstimator(RAW + '/2mpp_vizier.tsv', RAW + '/mcxc.tsv', gas=True,
                        ez_sqrt=False, c115_weight=False, catalog_mode=catalog_mode)
    print(f"2M++ sources after cuts: {est.n_gal} (Chae quotes 54,483 of 69,160)")
    print(f"MCXC clusters with D<=200 Mpc: {est.n_clu} (of 1743 total)")

    out = []
    for g in sparc:
        r_no  = est.eN_at(g['ra'], g['dec'], g['D'], completeness=False,
                          missing_baryons_x8=False)
        r_max = est.eN_at(g['ra'], g['dec'], g['D'], completeness=True,
                          missing_baryons_x8=True)
        # direction robustness: share of |g_total| carried by the single largest contributor
        # (computed in the maxclu weighting, which is the primary gate target)
        top = r_max['top']
        dom_share = top[0][3] if top else 0.0
        robust = 'robust' if dom_share >= 0.5 else 'soft'
        # primary unit vector = maxclu weighting (the primary gate target); noclu kept via cos
        u = r_max['unit_icrs']; usg = r_max['unit_sg']
        um = r_no['unit_icrs']
        # unit vector as RA/Dec of the direction the field points TOWARD
        ra_dir = np.degrees(np.arctan2(u[1], u[0])) % 360
        dec_dir = np.degrees(np.arcsin(np.clip(u[2], -1, 1)))
        out.append(dict(
            name=g['name'], ra=g['ra'], dec=g['dec'], D=g['D'],
            log_eN_noclu=np.log10(max(r_no['eN'], 1e-30)),
            log_eN_maxclu=np.log10(max(r_max['eN'], 1e-30)),
            ux_icrs=u[0], uy_icrs=u[1], uz_icrs=u[2],
            ux_sg=usg[0], uy_sg=usg[1], uz_sg=usg[2],
            ra_dir=ra_dir, dec_dir=dec_dir,
            cos_no_max=float(np.dot(u, um)),
            dom_name=top[0][0] if top else '', dom_kind=top[0][1] if top else '',
            dom_share=dom_share, flag=robust))
    if write_csv:
        cols = list(out[0].keys())
        with open(BASE + '/data/gext_vectors.csv', 'w', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            for r in out:
                w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})
        print(f"wrote {BASE}/data/gext_vectors.csv ({len(out)} rows)")

    # ---------------- GATE A ----------------
    chae = {}
    with open(CHAE_ENV) as fh:
        rd = csv.DictReader(fh)
        for row in rd:
            chae[row['galaxy'].strip()] = (float(row['log_eN_maxclu']), float(row['log_eN_noclu']))
    ours = {r['name']: r for r in out}
    matched = sorted(set(chae) & set(ours))
    unmatched = sorted(set(chae) - set(ours))
    print(f"\nGATE-A: matched {len(matched)}/{len(chae)} Chae galaxies; unmatched: {unmatched}")
    for col, idx in [('maxclu', 0), ('noclu', 1)]:
        x = np.array([ours[n]['log_eN_' + col] for n in matched])
        y = np.array([chae[n][idx] for n in matched])
        r = np.corrcoef(x, y)[0, 1]
        off = np.median(y - x)
        sc = np.std(y - x - off)
        sc_mad = 1.4826*np.median(np.abs((y - x - off) - np.median(y - x - off)))
        print(f"  {col}: Pearson r = {r:.3f} | global offset (Chae-ours, median) = {off:+.3f} dex"
              f" | scatter after 1 global offset: std = {sc:.3f} dex, robust(MAD) = {sc_mad:.3f} dex")
    # cross: our maxclu vs his maxclu is the primary gate
    # also: our noclu direction vs maxclu direction consistency
    cosv = np.array([ours[n]['cos_no_max'] for n in matched])
    print(f"  direction stability noclu-vs-maxclu weighting: median cos = {np.median(cosv):.3f}, "
          f"min = {cosv.min():.3f}")

    # ---------------- GATE B ----------------
    print("\nGATE-B: dominant-attractor direction sanity")
    VIRGO = radec_to_cart([187.70], [12.34])[0] * 16.5   # M87 / Virgo core, D~16.5 Mpc
    COMA  = radec_to_cart([194.95], [27.98])[0] * 100.0  # Coma cluster D~100 Mpc
    for label, att, attpos in [('Virgo', 'VIRGO', VIRGO), ('Coma', 'COMA', COMA)]:
        print(f"  -- galaxies within {'20' if label=='Virgo' else '30'} Mpc of {label}:")
        rad = 20.0 if label == 'Virgo' else 30.0
        nlist = []
        for r0 in out:
            p = radec_to_cart([r0['ra']], [r0['dec']])[0] * r0['D']
            dsep = np.linalg.norm(p - attpos)
            if dsep < rad and dsep > 1.0:
                towards = (attpos - p); towards /= np.linalg.norm(towards)
                u = np.array([r0['ux_icrs'], r0['uy_icrs'], r0['uz_icrs']])
                ang = np.degrees(np.arccos(np.clip(np.dot(u, towards), -1, 1)))
                nlist.append((r0['name'], dsep, ang, r0['dom_name'].strip(), r0['flag']))
        for n, dsep, ang, dom, fl in sorted(nlist, key=lambda t: t[1]):
            print(f"     {n:12s} sep={dsep:5.1f} Mpc  angle(g_vec, ->{label}) = {ang:6.1f} deg"
                  f"  dominant={dom[:22]:22s} [{fl}]")
        if nlist:
            angs = np.array([t[2] for t in nlist])
            print(f"     median angle = {np.median(angs):.1f} deg (blind expectation if random: 90)")

    # weak check: farthest SPARC galaxies vs the Great Attractor / Norma direction
    NORMA = radec_to_cart([243.89], [-60.91])[0] * 67.8
    print("  -- WEAK check: SPARC galaxies with D > 60 Mpc, angle to Norma/Great Attractor:")
    angs = []
    for r0 in out:
        if r0['D'] > 60.0:
            p = radec_to_cart([r0['ra']], [r0['dec']])[0] * r0['D']
            towards = NORMA - p; towards /= np.linalg.norm(towards)
            u = np.array([r0['ux_icrs'], r0['uy_icrs'], r0['uz_icrs']])
            ang = float(np.degrees(np.arccos(np.clip(np.dot(u, towards), -1, 1))))
            angs.append(ang)
            print(f"     {r0['name']:12s} D={r0['D']:6.1f}  angle = {ang:6.1f} deg"
                  f"  dominant={r0['dom_name'][:22]:22s} [{r0['flag']}]")
    if angs:
        print(f"     median = {np.median(angs):.1f} deg -- WEAK: most far SPARC galaxies are "
              f"northern; local walls (CfA2/Perseus-Pisces) legitimately compete with the GA.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
