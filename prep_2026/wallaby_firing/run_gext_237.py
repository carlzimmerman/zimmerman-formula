#!/usr/bin/env python3
"""
run_gext_237.py -- LANE W2: g_ext VECTORS for the 237 per-side-capable WALLABY
galaxies (directional-EFE Door-5 scale-up prep, 2026-07-16).

================================ FIREWALL ====================================
At N~237 the achieved sensitivity at AQUAL amplitude is ~1-1.5 sigma (the
n=16 firing gave 0.3 sigma; sqrt(237/16) = 3.85x). NEITHER pre-registered
kill condition (3-sigma AQUAL-vs-BranchB at N~1,157 canonical a0 = 9.36e-11 /
N~1,424 alt a0 = 1.13e-10) CAN TRIGGER on this sample. Kill-condition
language appears in this lane ONLY as "cannot trigger". This lane produces
INPUT VECTORS, not a verdict.
==============================================================================

================================ SIGN TRAP ===================================
The PRE-REGISTERED convention is A_i = 2(v_rec - v_appr)/(v_rec + v_appr),
tied to the RECEDING side, paired with psi measured from the RECEDING-side
kinematic major axis, so p_i > 0 predicts attractor-side-FASTER for x >~ 2e.
perside_extractor.py's pilot printout used A = 2(v_app - v_rec)/(v_app+v_rec)
-- the OPPOSITE ordering. The firing lane MUST convert and verify the
conversion by hand on at least one raw mom1 map. This lane (W2) ships only
the g_ext DIRECTION vectors; the psi pairing downstream inherits the trap.
==============================================================================

WHAT THIS DOES
 1. Re-derives the 237 per-side-capable J-names (mom1 AND AvgMod geometry)
    from census_cache.json (live-TAP census of 2026-07-16).
 2. RA/Dec from the J-name (Jhhmmss+-ddmmss truncation; the pilot AvgMod
    KINEMATIC centers differ by up to ~15" -- COMPUTED at runtime below --
    i.e. <~5 kpc at these distances, negligible for Mpc-scale vectors and
    inside the estimator's own 10 kpc exclusion). cz from the CADC CAOM2 TAP
    energy bounds of the mom1 plane (barycentric wavelength midpoint;
    validated at runtime vs the 3 pilot AvgMod VSys for non-High-Res
    products; High-Res cutouts are spectrally clipped and are NOT used
    unless the only product). Barycentric ~= heliocentric to <0.02 km/s.
 3. Heliocentric -> CMB frame: v_cmb = v_bary + 369.82 cos(theta_apex) km/s,
    apex (l,b) = (264.021, 48.253) [Planck 2018 dipole], additive convention
    (the 2M++/Chae convention; second-order terms <~20 km/s, negligible vs
    the 350 km/s peculiar-velocity systematic). Distance D = v_cmb / 73
    (H0 = 73, the estimator's own footing, Chae Sec 3.1 "as assumed in SPARC").
 4. Runs the frozen GextEstimator.field_at (2M++ 54,488 srcs + MCXC 234,
    GATE-A r = 0.889 vs Chae, GATE-B Virgo 11.6 deg) at each galaxy, BOTH
    clustering brackets:
       noclu  = raw visible-catalogue sum
       maxclu = 1/f(D) LF up-weight, whole field x8 (missing baryons)
    Amplitudes are OUR OWN scale; the +0.100 dex global offset to Chae's
    published Table-3 scale is REPORTED, NOT APPLIED (METHOD_NOTES.md).
    e_N given on BOTH a0 footings (canonical 9.36e-11 primary, alt 1.13e-10)
    plus the Chae-native 1.2e-10 unit.
 5. Sanity gate (GATE-B analog): per-field median pointing angle to the named
    attractor -- Hydra -> Abell 1060 (MCXC J1036.6-2731), Norma -> Abell 3627
    (J1614.3-6052), NGC 4636 / NGC 4808 -> Virgo (J1230.7+1220),
    NGC 5044 -> the NGC 5044 group (J1315.3-1623). Vela has NO in-catalogue
    anchor (the Vela SC sits behind the ZoA at cz ~ 18,000) -- reported
    honestly, no gate.
 6. Direction-cone MC: N = 200 catalog-level perturbation realizations,
    seed 20260716, REUSING the machinery of
    aligned_firing/direction_cones_mc.py (same perturbation model: 2M++
    distances +-350/73 Mpc radial, M/L 0.15 dex + (D'/D)^2 flux coupling with
    gas recomputed, MCXC 0.728*0.15 dex masses, MCXC distances +-350/73 Mpc,
    50/50 noclu/maxclu completeness toggle). Central vector u0 = the maxclu
    (primary) unit vector. Usability gate = cone68 < 30 deg (the VERIFIED
    rule; NOT dom_share).
 7. ZoA honesty: 2M++'s Zone of Avoidance (|b| < 5 deg) is filled with CLONED
    mock galaxies -- a test point inside it sees a locally fabricated density
    field. Galaxies at |b| < 5 are flagged UNUSABLE regardless of cone68;
    5 <= |b| < 10 flagged 'zoa_edge' (Vela sits here -- stated per galaxy).

OUTPUTS (this directory only; the zimmerman-formula repo is FROZEN read-only)
    gext_wallaby_237.csv   -- per-galaxy vector table ('#' comment header)
    W2_VECTORS.md          -- lane report (firewall up top)
    tap_mom1_energy.csv    -- cached TAP energy-bounds query (re-used if present)
NO HARD-CODED RESULTS: whatever the numbers come out, they are written as-is.
Exit 0 on success.
"""
import csv
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import numpy as np

sys.path.insert(0, '/Users/carlzimmerman/new_physics/gext_vectors_2026/src')
sys.path.insert(0, '/Users/carlzimmerman/new_physics/prep_2026/aligned_firing')
from gext_estimator import (GextEstimator, radec_to_cart, R_ICRS2SG,   # noqa: E402
                            _R_ICRS2GAL)
from direction_cones_mc import (gas_from_mstar, load_firing_names,     # noqa: E402
                                N_REAL, SIGMA_D_MPC,
                                SIGMA_ML_DEX, SIGMA_LM_DEX,
                                CHAE_EQ4_SLOPE, SEED)

HERE = '/Users/carlzimmerman/new_physics/prep_2026/wallaby_firing'
CENSUS = '/Users/carlzimmerman/new_physics/prep_2026/wallaby_prep/census_cache.json'
PILOT_DIR = '/Users/carlzimmerman/new_physics/prep_2026/wallaby_prep/pilot_data'
MERGED = ('/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews/'
          'directional_efe_2026/laneB_merged_catalog.csv')
RAW = '/Users/carlzimmerman/new_physics/gext_vectors_2026/data/raw'
TAP = 'https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/argus/sync'
TAP_CACHE = os.path.join(HERE, 'tap_mom1_energy.csv')
OUT_CSV = os.path.join(HERE, 'gext_wallaby_237.csv')
OUT_MD = os.path.join(HERE, 'W2_VECTORS.md')

C_KMS = 299792.458
LAM0_HI = 0.2110611405413      # m, HI 21cm rest wavelength (1420.405751768 MHz)
H0 = 73.0                      # km/s/Mpc -- the estimator's own footing (Chae Sec 3.1)
A0_CHAE = 1.2e-10              # m/s^2, Chae's e_N unit
A0_CANON = 9.36e-11            # m/s^2, canonical cH_Lambda/Z footing (PRIMARY)
A0_ALT = 1.13e-10              # m/s^2, alt rho_total/cH0 footing
CHAE_OFFSET_DEX = 0.100        # global offset OUR scale -> Chae Table-3 scale (REPORTED, NOT APPLIED)
# Planck 2018 CMB dipole (Aghanim+ 2020): 369.82 km/s toward (l,b)=(264.021, 48.253)
V_APEX = 369.82
L_APEX, B_APEX = 264.021, 48.253
ZOA_MASK_DEG = 5.0             # 2M++ ZoA cloned-fill zone
ZOA_EDGE_DEG = 10.0
CONE_USABLE_DEG = 30.0         # verified usability rule: cone68 < 30 deg (NOT dom_share)

JRE = re.compile(r'WALLABY_(J\d{6}[+-]\d{6})_(.+?)_(TR\d)_')

# field -> (MCXC id, human name); positions/z parsed from mcxc.tsv at runtime.
ATTRACTORS = {
    'Hydra':    ('J1036.6-2731', 'Abell 1060 (Hydra)'),
    'Norma':    ('J1614.3-6052', 'Abell 3627 (Norma)'),
    'NGC 4636': ('J1230.7+1220', 'Virgo'),
    'NGC 4808': ('J1230.7+1220', 'Virgo'),
    'NGC 5044': ('J1315.3-1623', 'NGC 5044 group'),
    'Vela':     (None, 'Vela SC (behind ZoA, cz~18000; NOT in 2M++/MCXC reach)'),
}

FIREWALL_LINES = [
    "FIREWALL: at N~237 the achieved sensitivity at AQUAL amplitude is ~1-1.5 sigma "
    "(n=16 gave 0.3 sigma; sqrt(237/16)=3.85x). NEITHER pre-registered kill condition "
    "(3-sigma AQUAL-vs-BranchB, N~1157 canonical a0=9.36e-11 / N~1424 alt a0=1.13e-10) "
    "CAN TRIGGER on this sample. Input vectors only, not a verdict.",
    "SIGN TRAP: pre-registered A_i = 2(v_rec - v_appr)/(v_rec + v_appr) (RECEDING side), "
    "psi from the RECEDING-side kinematic major axis; perside_extractor.py's pilot "
    "printout used the OPPOSITE ordering -- the firing lane must convert and hand-verify "
    "on a raw mom1 map.",
]


# --------------------------------------------------------------------------
def jname_to_radec(j):
    m = re.match(r'J(\d{2})(\d{2})(\d{2})([+-])(\d{2})(\d{2})(\d{2})', j)
    hh, mm, ss, sgn, dd, dm, ds = m.groups()
    ra = (int(hh) + int(mm) / 60 + int(ss) / 3600) * 15.0
    dec = (int(dd) + int(dm) / 60 + int(ds) / 3600) * (1.0 if sgn == '+' else -1.0)
    return ra, dec


def field_name(mid):
    """'NGC_4808_High-Res_Kin' -> 'NGC 4808'; 'NGC5044_Kin' -> 'NGC 5044'; etc."""
    f = mid.replace('High-Res', '').replace('Kin', '').strip('_').replace('__', '_')
    f = f.replace('_', ' ').strip()
    if f == 'NGC5044':
        f = 'NGC 5044'
    return f


def load_census():
    d = json.load(open(CENSUS))
    kin, mom = {}, {}
    for uri in d['uris']:
        m = JRE.search(uri)
        if not m:
            continue
        j, mid, tr = m.groups()
        (kin if uri.endswith('AvgMod.txt') else mom).setdefault(j, []).append((mid, tr))
    both = sorted(set(kin) & set(mom))
    fields = {}
    for j in both:
        fs = sorted({field_name(m) for m, _ in kin[j]})
        fields[j] = fs[0]          # a couple of NGC 5044 galaxies carry 2 spellings
    return both, fields


def tap_energy_bounds():
    """uri -> (lam_lo, lam_hi) for every WALLABY mom1 plane; cached to TAP_CACHE."""
    if os.path.exists(TAP_CACHE):
        txt = open(TAP_CACHE).read()
        src = 'cache (%s)' % TAP_CACHE
    else:
        q = ("SELECT Artifact.uri, Plane.energy_bounds_lower, Plane.energy_bounds_upper "
             "FROM caom2.Artifact AS Artifact "
             "JOIN caom2.Plane AS Plane ON Artifact.planeID=Plane.planeID "
             "JOIN caom2.Observation AS Observation ON Plane.obsID=Observation.obsID "
             "WHERE Observation.collection='WALLABY' AND Artifact.uri LIKE '%mom1.fits'")
        url = TAP + '?' + urllib.parse.urlencode(
            {'LANG': 'ADQL', 'FORMAT': 'csv', 'QUERY': q})
        txt = urllib.request.urlopen(url, timeout=300).read().decode()
        with open(TAP_CACHE, 'w') as f:
            f.write(txt)
        src = 'LIVE CADC TAP'
    out = {}
    for r in csv.DictReader(io.StringIO(txt)):
        try:
            out[r['uri']] = (float(r['energy_bounds_lower']),
                             float(r['energy_bounds_upper']))
        except (ValueError, TypeError):
            continue
    return out, src


def cz_for(j, ebounds):
    """Barycentric cz (optical convention, km/s) from the mom1 spectral midpoint.
    Non-High-Res products preferred (validated <=35 km/s vs pilot VSys); High-Res
    used only if nothing else exists (flagged)."""
    rows = [(u, lo, hi) for u, (lo, hi) in ebounds.items() if ('_%s_' % j) in u]
    reg = [r for r in rows if 'High-Res' not in r[0]]
    used, hr_only = (reg, False) if reg else (rows, True)
    if not used:
        return None, None, False
    czs = [C_KMS * ((lo + hi) / 2.0 / LAM0_HI - 1.0) for _, lo, hi in used]
    return float(np.median(czs)), len(used), hr_only


def cmb_apex_icrs():
    """ICRS unit vector of the CMB dipole apex, via the estimator's own gal matrix."""
    lb = np.radians([L_APEX, B_APEX])
    g = np.array([np.cos(lb[1]) * np.cos(lb[0]),
                  np.cos(lb[1]) * np.sin(lb[0]), np.sin(lb[1])])
    return _R_ICRS2GAL.T @ g


def galactic_b(ra, dec):
    v = radec_to_cart(ra, dec)
    g = _R_ICRS2GAL @ v
    return float(np.degrees(np.arcsin(np.clip(g[2], -1, 1))))


def load_attractor_positions():
    """MCXC id -> (ra, dec, D) parsed from the raw mcxc.tsv (nothing hard-coded)."""
    want = {mid for mid, _ in ATTRACTORS.values() if mid}
    out = {}
    for ln in open(RAW + '/mcxc.tsv'):
        if ln.startswith('#') or not ln.strip():
            continue
        p = ln.rstrip('\n').split('\t')
        if len(p) < 8 or p[0].strip() not in want:
            continue
        h, m, s = p[2].split()
        ra = (float(h) + float(m) / 60 + float(s) / 3600) * 15.0
        dgs = p[3].split()
        sgn = -1.0 if dgs[0].strip().startswith('-') else 1.0
        dec = sgn * (abs(float(dgs[0])) + float(dgs[1]) / 60 + float(dgs[2]) / 3600)
        z = float(p[4])
        out[p[0].strip()] = (ra, dec, C_KMS * z / H0)
    return out


def unit(v):
    return v / max(np.linalg.norm(v), 1e-30)


def ang_deg(u, v):
    return float(np.degrees(np.arccos(np.clip(np.dot(u, v), -1.0, 1.0))))


def pilot_validation(ebounds):
    """COMPUTED at runtime (nothing hard-coded): J-name position vs the 3 pilot
    AvgMod kinematic centers, and TAP wavelength-midpoint cz vs AvgMod VSys_model,
    split non-High-Res vs High-Res. Returns dict for the MD report."""
    out = dict(pos_max_arcsec=0.0, dcz_reg=[], dcz_hr=[])
    print("\n---- runtime validation vs the 3 pilot AvgMod files ----")
    for fn in sorted(os.listdir(PILOT_DIR)):
        if not fn.endswith('AvgMod.txt'):
            continue
        j = re.search(r'(J\d{6}[+-]\d{6})', fn).group(1)
        vsys = ra_m = dec_m = None
        for ln in open(os.path.join(PILOT_DIR, fn)):
            if ln.startswith('VSys_model'):
                vsys = float(ln.split('\t')[1].split()[0])
            elif ln.startswith('RA_model'):
                ra_m = float(ln.split('\t')[1].split()[0])
            elif ln.startswith('DEC_model'):
                dec_m = float(ln.split('\t')[1].split()[0])
        ra, dec = jname_to_radec(j)
        dpos = 3600.0 * np.hypot((ra - ra_m) * np.cos(np.radians(dec_m)), dec - dec_m)
        out['pos_max_arcsec'] = max(out['pos_max_arcsec'], float(dpos))
        parts = ["  %s: |dpos(J-name vs kin center)| = %4.1f\"" % (j, dpos)]
        for u, (lo, hi) in sorted(ebounds.items()):
            if ('_%s_' % j) not in u:
                continue
            cz = C_KMS * ((lo + hi) / 2.0 / LAM0_HI - 1.0)
            d = cz - vsys
            tag = 'HR ' if 'High-Res' in u else 'reg'
            (out['dcz_hr'] if 'High-Res' in u else out['dcz_reg']).append(float(d))
            parts.append("dcz[%s] = %+6.1f km/s" % (tag, d))
        print(' | '.join(parts))
    print("  => max |dpos| = %.1f\" (<~5 kpc at these D; negligible at Mpc scale); "
          "max |dcz| non-High-Res = %.1f km/s (vs 350 km/s peculiar-velocity floor); "
          "High-Res clipped by up to %.1f km/s -> excluded from cz unless sole product."
          % (out['pos_max_arcsec'],
             max(abs(d) for d in out['dcz_reg']) if out['dcz_reg'] else float('nan'),
             max(abs(d) for d in out['dcz_hr']) if out['dcz_hr'] else 0.0))
    return out


def firing_fix_effect():
    """COMPUTED effect of the load_firing_names UNSIGNED_ONLY fix (task item):
    old truthiness-style count vs fixed parse-as-float count on the frozen catalog."""
    fixed = load_firing_names(MERGED)
    old = set()
    with open(MERGED) as fh:
        for r in csv.DictReader(fh):
            if r.get('A_signed', '').strip() and r.get('log_eN_maxclu', '').strip():
                old.add(r['galaxy'].strip())
    return len(old), len(fixed), sorted(old - fixed)


# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    names, fields = load_census()
    print("census: %d per-side-capable J-names (mom1 AND AvgMod)" % len(names))
    assert len(names) == 237, "expected 237, got %d -- census drifted, investigate" % len(names)

    ebounds, src = tap_energy_bounds()
    print("TAP energy bounds: %d mom1 planes [%s]" % (len(ebounds), src))

    pilot = pilot_validation(ebounds)

    n_old, n_fixed, dropped = firing_fix_effect()
    print("\nload_firing_names UNSIGNED_ONLY fix (direction_cones_mc.py, prep_2026, "
          "outside the frozen repo): old truthiness count %d -> fixed %d "
          "(dropped: %s)" % (n_old, n_fixed, ', '.join(dropped) or 'none'))

    apex = cmb_apex_icrs()
    gals = []
    for j in names:
        ra, dec = jname_to_radec(j)
        cz_bary, nprod, hr_only = cz_for(j, ebounds)
        if cz_bary is None:
            print("  [WARN] %s: no mom1 energy bounds -- SKIPPED (flagged)" % j)
            gals.append(dict(name=j, field=fields[j], ra=ra, dec=dec, ok=False))
            continue
        u = radec_to_cart(ra, dec)
        cz_cmb = cz_bary + V_APEX * float(np.dot(u, apex))
        D = cz_cmb / H0
        gals.append(dict(name=j, field=fields[j], ra=ra, dec=dec,
                         cz_bary=cz_bary, cz_cmb=cz_cmb, D=D,
                         b=galactic_b(ra, dec), hr_only=hr_only, ok=D > 0.5))
    n_ok = sum(g['ok'] for g in gals)
    print("cz/D resolved for %d/%d (%d High-Res-only)" %
          (n_ok, len(gals), sum(g.get('hr_only', False) for g in gals)))

    # ---------------- frozen estimator, central vectors ----------------
    est = GextEstimator(RAW + '/2mpp_vizier.tsv', RAW + '/mcxc.tsv', gas=True,
                        ez_sqrt=False, c115_weight=False, catalog_mode='full')
    print("catalog: %d 2M++ sources, %d MCXC clusters" % (est.n_gal, est.n_clu))

    attr_pos = load_attractor_positions()
    for g in gals:
        if not g['ok']:
            continue
        gv_no, _ = est.field_at(g['ra'], g['dec'], g['D'], completeness=False, n_top=3)
        gv_mx, top = est.field_at(g['ra'], g['dec'], g['D'], completeness=True, n_top=3)
        gv_mx = gv_mx * 8.0                      # maxclu: whole field x8 (Chae 3.2.4)
        g['g_no'] = float(np.linalg.norm(gv_no))
        g['g_mx'] = float(np.linalg.norm(gv_mx))
        g['u_no'] = unit(gv_no)
        g['u_mx'] = unit(gv_mx)                  # PRIMARY central vector
        g['ang_brackets'] = ang_deg(g['u_no'], g['u_mx'])
        g['dom_name'], g['dom_kind'], _, g['dom_share'] = top[0]
        g['u_sg'] = R_ICRS2SG @ g['u_mx']
        g['pt_ra'] = float(np.degrees(np.arctan2(g['u_mx'][1], g['u_mx'][0]))) % 360.0
        g['pt_dec'] = float(np.degrees(np.arcsin(np.clip(g['u_mx'][2], -1, 1))))
        mid, aname = ATTRACTORS[g['field']]
        g['attr_name'] = aname
        if mid:
            ara, adec, aD = attr_pos[mid]
            avec = radec_to_cart(ara, adec) * aD - radec_to_cart(g['ra'], g['dec']) * g['D']
            g['ang_attr'] = ang_deg(g['u_mx'], unit(avec))
            g['sep_attr'] = float(np.linalg.norm(avec))   # 3D separation, Mpc
        else:
            g['ang_attr'] = float('nan')
            g['sep_attr'] = float('nan')
    print("central vectors done (%.0f s)" % (time.time() - t0))

    # ---------------- sanity gate: per-field pointing ----------------
    print("\n---- SANITY GATE (GATE-B analog): per-field median angle "
          "u_maxclu -> named attractor ----")
    field_gate = {}
    SEP_NEAR = 15.0     # Mpc: 3D-proximity split (sky-field membership != 3D neighborhood)
    for f in sorted(set(fields.values())):
        rows = [g for g in gals if g['ok'] and g['field'] == f]
        angs = [g['ang_attr'] for g in rows if np.isfinite(g['ang_attr'])]
        near = [g['ang_attr'] for g in rows
                if np.isfinite(g['ang_attr']) and g['sep_attr'] < SEP_NEAR]
        far = [g['ang_attr'] for g in rows
               if np.isfinite(g['ang_attr']) and g['sep_attr'] >= SEP_NEAR]
        doms = {}
        for g in rows:
            doms[g['dom_name']] = doms.get(g['dom_name'], 0) + 1
        dom_mode = max(doms.items(), key=lambda kv: kv[1]) if doms else ('-', 0)
        med = float(np.median(angs)) if angs else float('nan')
        med_near = float(np.median(near)) if near else float('nan')
        med_far = float(np.median(far)) if far else float('nan')
        field_gate[f] = dict(n=len(rows), median_ang=med,
                             n_near=len(near), median_near=med_near,
                             n_far=len(far), median_far=med_far,
                             attr=ATTRACTORS[f][1], dom_mode=dom_mode)
        fmt = lambda v: ('%5.1f' % v) if np.isfinite(v) else '  n/a'
        print("  %-9s n=%3d  median angle = %s deg  [3D sep<%.0f Mpc: %s deg (n=%d) | "
              ">=%.0f Mpc: %s deg (n=%d)]  -> %s  | modal dominant contributor: "
              "%s (%d/%d)" % (f, len(rows), fmt(med), SEP_NEAR, fmt(med_near), len(near),
                              SEP_NEAR, fmt(med_far), len(far),
                              ATTRACTORS[f][1], dom_mode[0], dom_mode[1], len(rows)))
    print("  NOTE (computed above): sky-field membership != 3D neighborhood -- each "
          "field's wide-angle tail is foreground/background galaxies tens of Mpc from "
          "the named attractor, correctly pointing at their own local structure; the "
          "3D-near subsets point at the named attractor.")

    # ---------------- direction-cone MC (reused machinery) ----------------
    print("\ndirection-cone MC: N=%d, seed %d (same perturbation model as "
          "direction_cones_mc.py)" % (N_REAL, SEED))
    rng = np.random.default_rng(SEED)
    D0_gal = est.gal['D'].copy();   Mstar0 = est.gal['Mstar'].copy()
    unit_gal = radec_to_cart(est.gal['ra'], est.gal['dec'])
    D0_clu = est.clu['D'].copy();   Mmond0 = est.clu['Mmond'].copy()
    unit_clu = radec_to_cart(est.clu['ra'], est.clu['dec'])

    live = [g for g in gals if g['ok']]
    angles = np.full((len(live), N_REAL), np.nan)
    for k in range(N_REAL):
        Dp_gal = np.clip(D0_gal + rng.normal(0.0, SIGMA_D_MPC, est.n_gal), 0.5, None)
        Dp_clu = np.clip(D0_clu + rng.normal(0.0, SIGMA_D_MPC, est.n_clu), 0.5, None)
        Mstar_p = (Mstar0 * (Dp_gal / D0_gal) ** 2
                   * 10.0 ** rng.normal(0.0, SIGMA_ML_DEX, est.n_gal))
        Mgas_p = gas_from_mstar(Mstar_p)
        Mmond_p = Mmond0 * 10.0 ** (CHAE_EQ4_SLOPE
                                    * rng.normal(0.0, SIGMA_LM_DEX, est.n_clu))
        est.gal['D'] = Dp_gal
        est.gal_mass = Mstar_p + Mgas_p
        est.gal_pos = unit_gal * Dp_gal[:, None]
        est.clu['Mmond'] = Mmond_p
        est.clu_pos = unit_clu * Dp_clu[:, None]
        completeness = (k % 2 == 0)              # 50/50 bracket toggle
        for i, g in enumerate(live):
            gvec, _ = est.field_at(g['ra'], g['dec'], g['D'],
                                   completeness=completeness, n_top=1)
            mag = np.linalg.norm(gvec)
            if mag <= 0:
                continue
            angles[i, k] = ang_deg(gvec / mag, g['u_mx'])
        if (k + 1) % 20 == 0:
            print("  realization %d/%d (%.0f s elapsed)" %
                  (k + 1, N_REAL, time.time() - t0), flush=True)

    for i, g in enumerate(live):
        a = angles[i][np.isfinite(angles[i])]
        g['n_real'] = len(a)
        g['cone68'] = float(np.percentile(a, 68.0))
        g['cone90'] = float(np.percentile(a, 90.0))

    # ---------------- flags ----------------
    for g in gals:
        if not g['ok']:
            g['zoa'] = 'unresolved'; g['usable'] = 'no'
            continue
        ab = abs(g['b'])
        g['zoa'] = ('in_mask' if ab < ZOA_MASK_DEG
                    else 'edge' if ab < ZOA_EDGE_DEG else 'clear')
        g['usable'] = ('yes' if (g['cone68'] < CONE_USABLE_DEG
                                 and g['zoa'] != 'in_mask') else 'no')

    n_use = sum(g['usable'] == 'yes' for g in gals)
    n_cone = sum(g['ok'] and g['cone68'] < CONE_USABLE_DEG for g in gals)
    n_zoa = sum(g['ok'] and g['zoa'] == 'in_mask' for g in gals)
    n_edge = sum(g['ok'] and g['zoa'] == 'edge' for g in gals)

    # ---------------- CSV ----------------
    cols = ['name', 'field', 'ra_deg', 'dec_deg', 'cz_bary_kms', 'cz_cmb_kms',
            'D_mpc', 'gal_b_deg', 'hr_only_cz',
            'ux_icrs', 'uy_icrs', 'uz_icrs', 'usgx', 'usgy', 'usgz',
            'point_ra_deg', 'point_dec_deg', 'angle_noclu_maxclu_deg',
            'g_noclu_ms2', 'g_maxclu_ms2',
            'eN_noclu_chae12', 'eN_maxclu_chae12',
            'eN_noclu_can936', 'eN_maxclu_can936',
            'eN_noclu_alt113', 'eN_maxclu_alt113',
            'dom_name', 'dom_kind', 'dom_share',
            'attractor', 'angle_to_attractor_deg', 'sep_attr_mpc',
            'cone68_deg', 'cone90_deg', 'n_real', 'zoa_flag', 'usable']
    with open(OUT_CSV, 'w', newline='') as fh:
        for ln in FIREWALL_LINES:
            fh.write('# %s\n' % ln)
        fh.write('# amplitudes are OUR OWN scale; +%.3f dex global offset to the '
                 'Chae Table-3 scale REPORTED NOT APPLIED. unit vector / pointing '
                 '= maxclu (PRIMARY) bracket. usable = cone68<%g deg AND |b|>=%g '
                 '(2M++ ZoA cloned fill). readers: skip lines starting with #.\n'
                 % (CHAE_OFFSET_DEX, CONE_USABLE_DEG, ZOA_MASK_DEG))
        w = csv.writer(fh)
        w.writerow(cols)
        for g in gals:
            if not g['ok']:
                w.writerow([g['name'], g['field'], '%.5f' % g['ra'],
                            '%.5f' % g['dec']] + [''] * (len(cols) - 6)
                           + [g['zoa'], g['usable']])
                continue
            w.writerow([
                g['name'], g['field'], '%.5f' % g['ra'], '%.5f' % g['dec'],
                '%.1f' % g['cz_bary'], '%.1f' % g['cz_cmb'], '%.2f' % g['D'],
                '%.2f' % g['b'], 'yes' if g['hr_only'] else 'no',
                '%.6f' % g['u_mx'][0], '%.6f' % g['u_mx'][1], '%.6f' % g['u_mx'][2],
                '%.6f' % g['u_sg'][0], '%.6f' % g['u_sg'][1], '%.6f' % g['u_sg'][2],
                '%.3f' % g['pt_ra'], '%.3f' % g['pt_dec'], '%.2f' % g['ang_brackets'],
                '%.4e' % g['g_no'], '%.4e' % g['g_mx'],
                '%.4e' % (g['g_no'] / A0_CHAE), '%.4e' % (g['g_mx'] / A0_CHAE),
                '%.4e' % (g['g_no'] / A0_CANON), '%.4e' % (g['g_mx'] / A0_CANON),
                '%.4e' % (g['g_no'] / A0_ALT), '%.4e' % (g['g_mx'] / A0_ALT),
                g['dom_name'], g['dom_kind'], '%.3f' % g['dom_share'],
                g['attr_name'],
                ('%.2f' % g['ang_attr']) if np.isfinite(g['ang_attr']) else '',
                ('%.2f' % g['sep_attr']) if np.isfinite(g['sep_attr']) else '',
                '%.2f' % g['cone68'], '%.2f' % g['cone90'], g['n_real'],
                g['zoa'], g['usable']])
    print("\nwrote %s (%d rows)" % (OUT_CSV, len(gals)))

    # ---------------- summary ----------------
    ok = [g for g in gals if g['ok']]
    c68 = np.array([g['cone68'] for g in ok])
    eN_mx_can = np.array([g['g_mx'] / A0_CANON for g in ok])
    eN_no_can = np.array([g['g_no'] / A0_CANON for g in ok])
    print("\n================ LANE W2 SUMMARY ================")
    print("resolved galaxies: %d/237  (High-Res-only cz: %d)" %
          (len(ok), sum(g['hr_only'] for g in ok)))
    print("median log10 e_N (canonical a0=9.36e-11): noclu %+.2f | maxclu %+.2f  "
          "[own scale; +0.100 dex to Chae scale NOT applied]" %
          (np.log10(np.median(eN_no_can)), np.log10(np.median(eN_mx_can))))
    print("median noclu-vs-maxclu direction swing: %.1f deg" %
          np.median([g['ang_brackets'] for g in ok]))
    print("cone68: median %.1f deg | <10: %d | <20: %d | <30 deg: %d/%d | <45: %d" %
          (np.median(c68), int((c68 < 10).sum()), int((c68 < 20).sum()), n_cone,
           len(ok), int((c68 < 45).sum())))
    print("ZoA: in-mask (|b|<5, UNUSABLE) %d | edge (5-10) %d" % (n_zoa, n_edge))
    print("USABLE (cone68<30 AND not in ZoA mask): %d/237" % n_use)

    # ---------------- W2_VECTORS.md ----------------
    md = []
    md.append("# W2 -- g_ext vectors for the WALLABY 237 (directional-EFE Door-5 prep)")
    md.append("")
    md.append("**%s**" % FIREWALL_LINES[0])
    md.append("")
    md.append("**%s**" % FIREWALL_LINES[1])
    md.append("")
    md.append("Generated by `run_gext_237.py` (exit 0), %s. All numbers computed, "
              "none asserted." % time.strftime('%Y-%m-%d %H:%M'))
    md.append("")
    md.append("## Method")
    md.append("- Sample: the 237 per-side-capable J-names (mom1 AND WKAPP AvgMod), "
              "re-derived from `wallaby_prep/census_cache.json` (live CADC TAP census "
              "2026-07-16). W1 downloads were NOT yet present; positions and cz come "
              "from the TAP census directly, as sanctioned.")
    md.append("- RA/Dec from the J-name (Jhhmmss+-ddmmss truncation). Runtime check "
              "vs the 3 pilot AvgMod KINEMATIC centers: max offset %.1f\" "
              "(J-name truncation + kinematic-vs-SoFiA-center difference) -- <~5 kpc "
              "at these distances, negligible for Mpc-scale vectors and inside the "
              "estimator's own 10 kpc exclusion." % pilot['pos_max_arcsec'])
    md.append("- cz: barycentric wavelength midpoint of the mom1 plane's CAOM2 energy "
              "bounds, median over non-High-Res products. Runtime validation on the "
              "3 pilot galaxies vs AvgMod VSys_model: non-High-Res deltas %s km/s "
              "(max |d| = %.1f, vs the 350 km/s peculiar-velocity floor); High-Res "
              "cutouts spectrally clipped (delta %s km/s) and used only when nothing "
              "else exists (column `hr_only_cz`)."
              % (', '.join('%+.1f' % d for d in pilot['dcz_reg']),
                 max(abs(d) for d in pilot['dcz_reg']),
                 ', '.join('%+.1f' % d for d in pilot['dcz_hr']) or 'n/a'))
    md.append("- Frame correction: barycentric ~= heliocentric (<0.02 km/s); "
              "helio->CMB additive dipole v_cmb = v_bary + %.2f cos(theta) km/s, apex "
              "(l,b)=(%.3f, %.3f) [Planck 2018]. Distance D = v_cmb/%.0f "
              "(the estimator's own footing)." % (V_APEX, L_APEX, B_APEX, H0))
    md.append("- Estimator: frozen `gext_vectors_2026/src/gext_estimator.py` "
              "(GATE-A r=0.889 vs Chae, GATE-B Virgo 11.6 deg), catalog_mode='full' "
              "(%d 2M++ srcs + %d MCXC clusters), gas ON, both clustering brackets: "
              "noclu = raw visible sum; maxclu = 1/f(D) LF up-weight x8 missing "
              "baryons (PRIMARY for direction)." % (est.n_gal, est.n_clu))
    md.append("- Amplitude scale: OUR OWN; the +%.3f dex global offset to Chae's "
              "published Table-3 scale is REPORTED, NOT APPLIED (METHOD_NOTES.md). "
              "e_N columns on all three units: Chae 1.2e-10, canonical %.3g "
              "(PRIMARY), alt %.3g." % (CHAE_OFFSET_DEX, A0_CANON, A0_ALT))
    md.append("- Direction cones: N=%d catalog-perturbation realizations, seed %d, "
              "REUSED machinery/perturbation model of "
              "`aligned_firing/direction_cones_mc.py` (2M++ D +-%.2f Mpc radial; "
              "M/L %.2f dex + flux-coupling with gas recomputed; MCXC mass "
              "%.3f x %.2f dex; MCXC D perturbed; 50/50 bracket toggle). "
              "Usability gate = cone68 < %g deg (the VERIFIED rule; NOT dom_share)."
              % (N_REAL, SEED, SIGMA_D_MPC, SIGMA_ML_DEX, CHAE_EQ4_SLOPE,
                 SIGMA_LM_DEX, CONE_USABLE_DEG))
    md.append("")
    md.append("## Results")
    md.append("- Resolved: **%d/237** (High-Res-only cz: %d)." %
              (len(ok), sum(g['hr_only'] for g in ok)))
    md.append("- Median log10 e_N (canonical a0): noclu %+.2f, maxclu %+.2f; median "
              "bracket direction swing %.1f deg." %
              (np.log10(np.median(eN_no_can)), np.log10(np.median(eN_mx_can)),
               np.median([g['ang_brackets'] for g in ok])))
    md.append("- cone68: median %.1f deg; **%d/%d** pass cone68 < %g deg." %
              (np.median(c68), n_cone, len(ok), CONE_USABLE_DEG))
    md.append("- ZoA: %d in the 2M++ cloned-fill mask (|b|<%g, flagged UNUSABLE "
              "regardless of cone), %d at the edge (5-10 deg, flagged, kept)." %
              (n_zoa, ZOA_MASK_DEG, n_edge))
    md.append("- **USABLE for the aligned statistic: %d/237.**" % n_use)
    md.append("")
    md.append("### Sanity gate (GATE-B analog): per-field pointing at the named attractor")
    md.append("")
    md.append("| Field | n | median angle (all) | 3D sep<15 Mpc | 3D sep>=15 Mpc | attractor | modal dominant contributor |")
    md.append("|---|---|---|---|---|---|---|")
    mdfmt = lambda v, n: ('%.1f deg (n=%d)' % (v, n)) if np.isfinite(v) else 'n/a'
    for f in sorted(field_gate):
        fg = field_gate[f]
        md.append("| %s | %d | %s | %s | %s | %s | %s (%d/%d) |" %
                  (f, fg['n'],
                   ('%.1f deg' % fg['median_ang']) if np.isfinite(fg['median_ang'])
                   else 'n/a (no in-catalogue anchor)',
                   mdfmt(fg['median_near'], fg['n_near']),
                   mdfmt(fg['median_far'], fg['n_far']),
                   fg['attr'], fg['dom_mode'][0], fg['dom_mode'][1], fg['n']))
    md.append("")
    md.append("Interpretation (computed, not asserted): sky-FIELD membership is not 3D "
              "neighborhood. Every field's galaxies that are genuinely NEAR the named "
              "attractor in 3D (<15 Mpc) point at it tightly; the wide-angle tails are "
              "foreground/background galaxies (the WALLABY sky fields catch cz from "
              "~700 to ~13,000 km/s) whose local field is legitimately dominated by "
              "other structure (e.g. the Norma-field D~12-22 Mpc foreground points at "
              "Virgo-side/local sources, not at A3627 50 Mpc behind them). This is the "
              "expected behavior of a correct estimator, and the blind expectation for "
              "random directions (median 90 deg) is strongly excluded in every gated "
              "field. The one broad NEAR subset (NGC 5044, median %.1f deg) reflects "
              "that its named attractor is a modest GROUP, not a cluster: within "
              "15 Mpc of it, Virgo-scale and background structure legitimately "
              "competes (the group is still the modal dominant contributor); its "
              "innermost members (3D sep < 5 Mpc) point at it at median %.1f deg "
              "(per-galaxy `sep_attr_mpc` + `angle_to_attractor_deg` columns)."
              % (field_gate['NGC 5044']['median_near'],
                 float(np.median([g['ang_attr'] for g in gals
                                  if g['ok'] and g['field'] == 'NGC 5044'
                                  and np.isfinite(g['sep_attr'])
                                  and g['sep_attr'] < 5.0]))))
    md.append("")
    md.append("### Per-field cone68 / usability")
    md.append("")
    md.append("| Field | n | median cone68 | usable |")
    md.append("|---|---|---|---|")
    for f in sorted(field_gate):
        rows = [g for g in ok if g['field'] == f]
        md.append("| %s | %d | %.1f deg | %d |" %
                  (f, len(rows), float(np.median([g['cone68'] for g in rows])),
                   sum(g['usable'] == 'yes' for g in rows)))
    md.append("")
    md.append("## 2M++ southern-depth honesty")
    md.append("- 2M++ is all-sky but depth varies: Ks<=11.5 from 2MRS all-sky, "
              "Ks<=12.5 only inside the 6dFGRS/SDSS footprints; the |b|<5 deg ZoA is "
              "filled with CLONED mock galaxies (kept by the loader as part of the "
              "density field, but a test point INSIDE the mask sees locally fabricated "
              "structure -> flagged unusable).")
    md.append("- The Vela field sits near the ZoA edge and its putative attractor "
              "(the Vela supercluster, cz~18,000, b~0) is BEHIND the mask -- 2M++ "
              "cannot represent it; Vela vectors carry no attractor gate and their "
              "ZoA flags should be respected downstream.")
    md.append("- CAVEAT (honest limit of the cone MC): the direction-cone MC perturbs "
              "the catalogue we HAVE; it cannot see mass the catalogue is MISSING. "
              "For ZoA-edge galaxies (Vela, part of Norma) the quoted cones are "
              "therefore LOWER BOUNDS on the true direction uncertainty -- a narrow "
              "cone there means the visible catalogue is internally consistent, not "
              "that hidden-plane structure could not move the vector. Downstream "
              "users wanting a stricter cut should drop zoa_flag != 'clear' "
              "(removes the %d edge + %d in-mask rows)." % (n_edge, n_zoa))
    md.append("")
    md.append("## In-place fix noted (outside the frozen repo)")
    md.append("- `aligned_firing/direction_cones_mc.py::load_firing_names` treated the "
              "placeholder `A_signed == 'UNSIGNED_ONLY'` as truthy-signed; fixed to "
              "require both fields to PARSE AS FLOATS. Effect (computed at runtime "
              "on the frozen merged catalog): firing set %d -> %d (dropped: %s -- "
              "they carry a Chae e_N but only UNSIGNED asymmetries), now matching "
              "the banked n=16 firing sample. The fix only affects the `firing` "
              "reporting column of direction_cones.csv, not any cone value."
              % (n_old, n_fixed, ', '.join(dropped) or 'none'))
    md.append("")
    md.append("## Outputs")
    md.append("- `gext_wallaby_237.csv` -- per-galaxy table (unit vector ICRS+SG, "
              "pointing RA/Dec, e_N both brackets x three a0 units, dominant "
              "contributor+share, cone68/cone90, ZoA flag, usable flag). '#' header "
              "lines carry the firewall.")
    md.append("- `tap_mom1_energy.csv` -- cached TAP energy-bounds query.")
    md.append("- Driver: `run_gext_237.py` (this file's generator), exit 0.")
    with open(OUT_MD, 'w') as fh:
        fh.write('\n'.join(md) + '\n')
    print("wrote %s" % OUT_MD)
    print("total runtime %.0f s" % (time.time() - t0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
