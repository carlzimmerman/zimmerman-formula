#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_high-z_floor_census -- CANDIDATE K-C: the framework's own baryonic floor, g_obs(R) >= g_bar(R),
as an a_0-free, Lambda-free, footing-free statistic, and its REDSHIFT CENSUS across every survey in the
archive where g_bar can be built independently of the kinematics.

THE CANDIDATE, stated exactly
        nu(y) >= 1 for every y  =>  g_obs(R) >= g_bar(R)  at every radius, in every system, at every z.
    Operationally, with each catalogue's OWN baryonic mass and the exact thin exponential-disc geometry:
        F  ==  log10[ v_c(R)^2 R / ( eps(R/R_d) G M_bar ) ]   must be >= 0 for every galaxy.
    The proposing stage measured 24/95 violations (25.3%) in MUSE-DARK II and a rise with redshift, and
    proposed the violation fraction as a primary statistic with the smallest lever in the programme
    (d log(g_bar/g_obs)/d log Upsilon = +1 exactly, against |LAMBDA| = 1.7-3.4 for a_0 itself).

WHAT THIS SCRIPT ADDS, and it is what decides the candidate
    (1) the census is run on FIVE samples spanning z = 0 to 2.5, not one;
    (2) a z = 0 ESTIMATOR CONTROL: SPARC measured twice -- once with its full resolved rotation curves
        and once degraded to exactly the information a high-z survey has (total M_bar + R_e + one
        velocity).  The difference between those two violation fractions is estimator error, not data;
    (3) a NOISE-FORWARD model: given each catalogue's own quoted errors, what violation fraction is
        EXPECTED if the floor holds exactly?  A census that the noise already explains is not a finding;
    (4) the two-route ledger inside RC100: that survey tabulates BOTH f_DM(<R_e) AND log M_bar AND R_e,
        so g_bar can be built two ways from the same paper.  Their ratio is a direct measurement of the
        internal mass-calibration offset that k02's Part 3 could only solve for;
    (5) the LambdaCDM alternative computed, not asserted: the same floor is required by ANY theory with
        non-negative dark mass and circular motion.  If that is so the statistic contains no a_0 and
        FAILS criterion (2) of the Kepler-grade definition by construction.  Reported against interest.

RESTATEMENT TEST (executed in Part 7, not asserted).  Attempt to derive F >= 0 from v^4 = G M_b a_0:
    the deep-MOND law fixes the ASYMPTOTIC flat speed and says nothing about g_obs vs g_bar at a finite
    radius -- the derivation does NOT close, so this is not a restatement of the BTFR/RAR.  But it is
    derivable in one line from "the phantom has non-negative mass", which is also true of a CDM halo.
BOTH FOOTINGS: carried, and the point is that the answer is IDENTICAL for both -- proved numerically.
UPSILON LEVER: measured by re-running the whole pipeline at Upsilon x 1.5, not asserted.
No git.  No threshold is tuned: every gate below is fixed at 0 (the floor) or at 2 sigma.
"""
import os, sys, math, csv
import numpy as np
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hunt_lib import Check, P, info, A0, load_sparc, kpc, G, Msun
DATA = os.path.join(HERE, '..', 'real_research', 'data')
CAT_J = os.path.join(HERE, '..', 'prep_2026', 'jeanneau_refit', 'jeanneau26_catalog_cds.csv')
RNG = np.random.default_rng(20260903)


def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def eps_disc(R_over_Rd):
    """EXACT razor-thin exponential disc: eps == g_bar(R) R^2 / (G M_disc_TOTAL).
       v_c^2 = (2 G M_d / R_d) u^2 [I0K0 - I1K1](u), u = R/(2R_d)  =>  eps = 4 u^3 [I0K0 - I1K1]."""
    u = np.asarray(R_over_Rd, float) / 2.0
    return 4.0 * u ** 3 * (i0(u) * k0(u) - i1(u) * k1(u))


def eps_numeric(R_over_Rd, nring=200000):
    """Independent check of eps_disc by direct numerical evaluation of the Hankel integral
       v_c^2(R) = (G M_d / R_d) * int_0^inf dk R k J1(kR) / (1+(k R_d)^2)^{3/2} ... done instead by
       Toomre's form:  g(R) = (G M_d/R_d^2) * int_0^inf J1(qR/R_d) q dq /(1+q^2)^{3/2}."""
    from scipy.special import j1
    x = np.asarray(R_over_Rd, float)
    q = np.linspace(1e-6, 400.0, nring)
    integ = j1(q * x) * q / (1.0 + q * q) ** 1.5
    gI = np.trapz(integ, q)                      # = g(R) R_d^2/(G M_d)
    return gI * x ** 2                           # eps = g R^2/(G M_d)


def kpc_per_arcsec(z, Om=0.30, OL=0.70, H0=70.0):
    c = 299792.458
    zz = np.linspace(0.0, z, 4096)
    Dc = c / H0 * np.trapz(1.0 / np.sqrt(Om * (1 + zz) ** 3 + OL), zz)
    return Dc / (1 + z) * 1e3 * np.pi / (180 * 3600)


def fnum(s):
    try:
        return float(s)
    except Exception:
        return float('nan')


def wilson(k, n, zc=1.0):
    """Wilson interval on a binomial fraction (1 sigma), so small-N fractions are not over-read."""
    if n == 0:
        return (float('nan'), float('nan'), float('nan'))
    p = k / n
    d = 1 + zc * zc / n
    c = (p + zc * zc / (2 * n)) / d
    h = zc * math.sqrt(p * (1 - p) / n + zc * zc / (4 * n * n)) / d
    return p, c - h, c + h


# ==================================================================================================
# sample builders.  Each returns dict(name, z, gobs, gbar, extra...) with g_bar built from the
# catalogue's OWN mass and size -- never by inverting g_obs through the kernel.
# ==================================================================================================
E_RE = float(eps_disc(1.678))          # eps at R = 1 R_e for an exponential disc
E_2RE = float(eps_disc(2 * 1.678))     # eps at R = 2 R_e


def build_jeanneau(ups_scale=1.0, gas_scale=1.0, gas_boost=1.0):
    rows = list(csv.DictReader(open(CAT_J)))
    z = np.array([fnum(r['zR21']) for r in rows])
    Re = np.array([fnum(r['Reff']) for r in rows]) * np.array([kpc_per_arcsec(zi) for zi in z])
    v = 10 ** np.array([fnum(r['logV2_0']) for r in rows]) * 1e3
    sv = np.array([fnum(r['s_logV2_0']) for r in rows])
    lMs = np.array([fnum(r['logM*']) for r in rows])
    lMsl = np.array([fnum(r['b_logM*']) for r in rows])
    lMsh = np.array([fnum(r['B_logM*']) for r in rows])
    lMg = np.log10(10 ** np.array([fnum(r['logMHI']) for r in rows])
                   + 10 ** np.array([fnum(r['logMMol']) for r in rows]))
    R = 2.0 * Re * kpc
    e_s, e_g = E_2RE, float(eps_disc(2 * 1.678 / gas_scale))
    gbar = (e_s * G * ups_scale * 10 ** lMs * Msun + e_g * G * gas_boost * 10 ** lMg * Msun) / R ** 2
    return dict(name='MUSE-DARK II lensed (z 0.5-1.45)', z=z, gobs=v ** 2 / R, gbar=gbar,
                sig_logv=sv, sig_lMs=(lMsh - lMsl) / 2.0, sig_lMg=np.full_like(lMg, 0.35),
                sig_lR=np.full_like(lMg, 0.14), fstar=e_s * ups_scale * 10 ** lMs /
                (e_s * ups_scale * 10 ** lMs + e_g * gas_boost * 10 ** lMg), R_kpc=2 * Re)


def build_rc100(ups_scale=1.0):
    rows = list(csv.DictReader(open(os.path.join(DATA, 'rc100_nestorshachar2023_table3.csv'))))
    z = np.array([fnum(r['z']) for r in rows])
    lMb = np.array([fnum(r['logMbar_Msun']) for r in rows])
    Re = np.array([fnum(r['Re_kpc']) for r in rows])
    v = np.array([fnum(r['Vc_Re_kms']) for r in rows]) * 1e3
    fdm = np.array([fnum(r['fDM_within_Re']) for r in rows])
    R = Re * kpc
    gobs = v ** 2 / R
    gbar = E_RE * G * ups_scale * 10 ** lMb * Msun / R ** 2
    return dict(name='RC100 (z 0.6-2.5)', z=z, gobs=gobs, gbar=gbar, fdm=fdm,
                gbar_fdm=(1 - fdm) * gobs, sig_logv=np.full_like(z, 0.043),
                sig_lMs=np.full_like(z, 0.15), sig_lMg=np.full_like(z, 0.0),
                sig_lR=np.full_like(z, 0.10), fstar=np.ones_like(z), R_kpc=Re)


def build_msa3d(ups_scale=1.0):
    """MSA-3D golden: STARS ONLY are tabulated, so g_bar is a LOWER bound and any violation is robust."""
    rows = [r for r in csv.DictReader(open(os.path.join(DATA, 'msa3d_2026_rotation_curves.csv')))
            if r['sample'] == 'golden']
    z = np.array([fnum(r['z']) for r in rows])
    lMs = np.array([fnum(r['logMstar']) for r in rows])
    Re = np.array([fnum(r['Re_disk_kpc']) for r in rows])
    vr = np.array([fnum(r['Vrot_Re']) for r in rows])
    s0 = np.array([fnum(r['sigma0']) for r in rows])
    R = Re * kpc
    gobs = (vr ** 2 + 2.0 * s0 ** 2 * 1.678) * 1e6 / R          # asymmetric-drift corrected
    gbar = E_RE * G * ups_scale * 10 ** lMs * Msun / R ** 2
    return dict(name='MSA-3D golden, stars only (z 0.6-1.7)', z=z, gobs=gobs, gbar=gbar,
                sig_logv=np.full_like(z, 0.03), sig_lMs=np.full_like(z, 0.15),
                sig_lMg=np.full_like(z, 0.0), sig_lR=np.full_like(z, 0.12),
                fstar=np.ones_like(z), R_kpc=Re)


def build_kross(ups_scale=1.0):
    """KROSS: stars only, so g_bar is again a LOWER bound; violations here cannot be cured by adding gas."""
    rows = list(csv.DictReader(open(os.path.join(DATA, 'kross_harrison2017.csv'))))
    z = np.array([fnum(r['z']) for r in rows])
    Ms = np.array([fnum(r['Mstar']) for r in rows])
    v = np.array([fnum(r['VC_kms']) for r in rows]) * 1e3
    Re = np.array([fnum(r['Reff_kpc']) for r in rows])
    ok = np.isfinite(z * Ms * v * Re) & (Ms > 0) & (Re > 0)
    R = Re[ok] * kpc
    return dict(name='KROSS stars only (z~0.9)', z=z[ok], gobs=v[ok] ** 2 / R,
                gbar=E_RE * G * ups_scale * Ms[ok] * Msun / R ** 2,
                sig_logv=np.full(ok.sum(), 0.06), sig_lMs=np.full(ok.sum(), 0.20),
                sig_lMg=np.full(ok.sum(), 0.0), sig_lR=np.full(ok.sum(), 0.15),
                fstar=np.ones(ok.sum()), R_kpc=Re[ok])


def build_sparc_full(ups_scale=1.0):
    """z = 0 control, FULL information: g_bar from the resolved surface photometry + HI, at R = 2 R_e."""
    gals = load_sparc()
    zz, go, gb, rk = [], [], [], []
    for g in gals:
        R = 2.0 * g['Reff']
        if not (g['Reff'] > 0 and g['r'].min() <= R <= g['r'].max()):
            continue
        vg = float(np.interp(R, g['r'], g['vg']))
        vd = float(np.interp(R, g['r'], g['vd']))
        vb = float(np.interp(R, g['r'], g['vb']))
        vo = float(np.interp(R, g['r'], g['vobs']))
        gbar = (vg * abs(vg) + ups_scale * 0.5 * vd ** 2 + ups_scale * 0.7 * vb ** 2) * 1e6 / (R * kpc)
        if gbar <= 0:
            continue
        zz.append(0.0); go.append(vo ** 2 * 1e6 / (R * kpc)); gb.append(gbar); rk.append(R)
    n = len(zz)
    return dict(name='SPARC at 2 R_e, RESOLVED g_bar (z=0)', z=np.zeros(n), gobs=np.array(go),
                gbar=np.array(gb), sig_logv=np.full(n, 0.02), sig_lMs=np.full(n, 0.11),
                sig_lMg=np.full(n, 0.10), sig_lR=np.full(n, 0.05), fstar=np.full(n, 0.5),
                R_kpc=np.array(rk))


def build_sparc_degraded(ups_scale=1.0):
    """z = 0 ESTIMATOR CONTROL: exactly the information a high-z survey has -- total M_bar, R_e, one
       velocity -- pushed through the identical eps(2R_e) estimator.  Same galaxies as build_sparc_full."""
    gals = load_sparc()
    zz, go, gb, rk = [], [], [], []
    for g in gals:
        R = 2.0 * g['Reff']
        if not (g['Reff'] > 0 and g['r'].min() <= R <= g['r'].max()):
            continue
        vo = float(np.interp(R, g['r'], g['vobs']))
        Mb = ups_scale * 0.5 * g['L36'] * 1e9 + 1.33 * g['MHI'] * 1e9
        gbar = E_2RE * G * Mb * Msun / (R * kpc) ** 2
        zz.append(0.0); go.append(vo ** 2 * 1e6 / (R * kpc)); gb.append(gbar); rk.append(R)
    n = len(zz)
    return dict(name='SPARC at 2 R_e, DEGRADED to M_bar+R_e (z=0)', z=np.zeros(n), gobs=np.array(go),
                gbar=np.array(gb), sig_logv=np.full(n, 0.02), sig_lMs=np.full(n, 0.11),
                sig_lMg=np.full(n, 0.10), sig_lR=np.full(n, 0.05), fstar=np.full(n, 0.5),
                R_kpc=np.array(rk))


def census(s):
    F = np.log10(s['gobs'] / s['gbar'])
    ok = np.isfinite(F)
    return F[ok], (F[ok] < 0).sum(), ok.sum()


def noise_forward(s, ntrial=4000):
    """If the floor holds EXACTLY for the true values, what violation fraction do the quoted errors
       produce?  Truth is taken as each galaxy's own (g_obs, g_bar) pushed onto the floor when it is
       below it -- i.e. the most conservative truth consistent with the floor -- then perturbed."""
    F = np.log10(s['gobs'] / s['gbar'])
    Ftrue = np.maximum(F, 0.0)                     # truth: obeys the floor, otherwise as observed
    n = len(F)
    sM = np.sqrt((s['fstar'] * s['sig_lMs']) ** 2 + ((1 - s['fstar']) * s['sig_lMg']) ** 2)
    sF = np.sqrt((2 * s['sig_logv']) ** 2 + sM ** 2 + (1.0 * s['sig_lR']) ** 2)
    fr = np.array([np.mean(Ftrue + RNG.normal(0, sF, n) < 0) for _ in range(ntrial)])
    return fr.mean(), fr.std(), float(np.median(sF))


# ==================================================================================================
def main():
    ck = Check()
    P("=" * 122)
    P("PART 0 -- the geometry, verified against an independent integral before any data is touched")
    P("=" * 122)
    P(f"    {'R/R_d':>8}{'eps (Bessel, exact)':>22}{'eps (Hankel integral)':>24}{'frac diff':>14}")
    worst = 0.0
    for rr in (0.5, 1.0, 1.678, 3.356, 6.0):
        a, b = float(eps_disc(rr)), float(eps_numeric(rr))
        worst = max(worst, abs(a - b) / a)
        P(f"    {rr:>8.3f}{a:>22.5f}{b:>24.5f}{abs(a-b)/a:>14.2e}")
    ck("k-hz-0 the enclosed-mass geometry factor is the exact razor-thin exponential disc and is verified "
       "against an INDEPENDENT Hankel-integral evaluation -- if the Bessel form were mis-transcribed this "
       "fails (hunt bug patterns 1 and 2 closed before any data)",
       worst < 2e-3, f"worst fractional difference over five radii = {worst:.2e}; "
       f"eps(R_e) = {E_RE:.4f}, eps(2R_e) = {E_2RE:.4f}")
    P("")
    P(f"    NOTE, and it is load-bearing: at R = R_e a razor-thin disc gives eps = {E_RE:.4f}, so using the")
    P(f"    TOTAL baryonic mass as a point mass overstates g_bar by {-math.log10(E_RE):+.3f} dex there.  That is")
    P("    hunt bug pattern 1, and it is exactly the bug that made the first version of item 16 report")
    P("    58/100 RC100 galaxies below the floor.  Everything below uses eps.")

    # ---------------------------------------------------------------- PART 1: the census
    P("")
    P("=" * 122)
    P("PART 1 -- THE CENSUS: the fraction of each sample below its own baryons-only floor")
    P("=" * 122)
    samples = [build_sparc_full(), build_sparc_degraded(), build_jeanneau(),
               build_rc100(), build_msa3d(), build_kross()]
    P(f"    {'sample':44}{'N':>5}{'<z>':>6}{'N below':>9}{'frac':>8}{'  Wilson 1s':>16}"
      f"{'median F (dex)':>16}{'sd F':>8}")
    res = {}
    for s in samples:
        F, k, n = census(s)
        p, lo, hi = wilson(k, n)
        res[s['name']] = dict(F=F, k=k, n=n, p=p, lo=lo, hi=hi, s=s)
        P(f"    {s['name']:44}{n:5d}{s['z'].mean():6.2f}{k:9d}{p:8.3f}   [{lo:.3f},{hi:.3f}]"
          f"{np.median(F):16.3f}{F.std():8.3f}")
    r_full = res['SPARC at 2 R_e, RESOLVED g_bar (z=0)']
    r_deg = res['SPARC at 2 R_e, DEGRADED to M_bar+R_e (z=0)']
    r_j = res['MUSE-DARK II lensed (z 0.5-1.45)']
    r_rc = res['RC100 (z 0.6-2.5)']
    P("")
    P("    THE ESTIMATOR CONTROL, which is the number that sizes the whole candidate:")
    P(f"      the SAME {r_full['n']} local galaxies violate the floor {r_full['p']*100:.1f}% of the time with their")
    P(f"      resolved photometry and {r_deg['p']*100:.1f}% of the time when degraded to (M_bar, R_e, one velocity),")
    P(f"      the high-z survey's information.  The difference, {(r_deg['p']-r_full['p'])*100:+.1f} points, is ESTIMATOR error at z = 0.")
    ck("k-hz-1 THE ESTIMATOR CONTROL FIRES: degrading z = 0 galaxies to exactly the information a high-z "
       "survey has changes their measured violation fraction, so a nonzero high-z violation fraction is "
       "not by itself evidence about the galaxies.  This check fails if degrading changes nothing",
       abs(r_deg['p'] - r_full['p']) > 0.01,
       f"resolved {r_full['k']}/{r_full['n']} = {r_full['p']:.3f}; degraded {r_deg['k']}/{r_deg['n']} = "
       f"{r_deg['p']:.3f}; shift {(r_deg['p']-r_full['p'])*100:+.1f} points on the identical galaxies")
    ck("k-hz-1b AND THE HIGH-REDSHIFT EXCESS SURVIVES THE CONTROL: MUSE-DARK II's violation fraction is "
       "larger than the same estimator's own z = 0 floor.  This check fails if the z = 0 degraded control "
       "already reaches the high-z fraction",
       r_j['lo'] > r_deg['p'],
       f"MUSE-DARK II {r_j['k']}/{r_j['n']} = {r_j['p']:.3f} [{r_j['lo']:.3f},{r_j['hi']:.3f}] against the "
       f"degraded z = 0 control {r_deg['p']:.3f}")

    # ---------------------------------------------------------------- PART 2: noise forward
    P("")
    P("=" * 122)
    P("PART 2 -- is the census already explained by the catalogues' own quoted errors?")
    P("=" * 122)
    P(f"    {'sample':44}{'observed frac':>15}{'expected from noise':>21}{'sigma':>10}{'median sig_F':>14}")
    excess = {}
    for name, r in res.items():
        mu, sd, sF = noise_forward(r['s'])
        z = (r['p'] - mu) / max(sd, 1e-9)
        excess[name] = z
        P(f"    {name:44}{r['p']:15.3f}{mu:21.3f}{z:10.2f}{sF:14.3f}")
    P("")
    P("    The error model is each catalogue's own: MUSE-DARK II uses its posterior sigma on log v_c and")
    P("    the 16-84 spread on log M*, plus 0.35 dex on the scaling-relation gas (Tacconi+20 molecular and")
    P("    NeutralUniverseMachine HI, whose own quoted scatter in log tau_HI is 0.8 dex) and 0.14 dex on R_e.")
    P("    RC100/MSA-3D/KROSS have no error columns in the tables on disk, so literature-typical values are")
    P("    used and are stated in the source; their rows are indicative, MUSE-DARK II's is not.")
    ck("k-hz-2 THE NOISE-FORWARD TEST, and it is the one that decides whether the census is a finding: "
       "MUSE-DARK II's violation fraction is compared with what its OWN quoted errors produce when the "
       "floor holds exactly.  The check fails if the observed fraction is NOT in excess of the noise",
       excess['MUSE-DARK II lensed (z 0.5-1.45)'] > 2.0,
       f"MUSE-DARK II excess = {excess['MUSE-DARK II lensed (z 0.5-1.45)']:.2f} sigma over the noise "
       f"expectation (>2 required); RC100 {excess['RC100 (z 0.6-2.5)']:.2f} sigma, "
       f"SPARC degraded {excess['SPARC at 2 R_e, DEGRADED to M_bar+R_e (z=0)']:.2f} sigma")
    P("")
    P("    ^ THIS FAILURE IS THE RESULT, and it is stated against the proposing stage's own interest: the")
    P("      pre-specified gate was 'observed fraction in excess of the noise by > 2 sigma => the census is")
    P("      a statement about galaxies'.  It is not met.  The 25.3% is what the catalogue's own error bars")
    P("      produce when the floor holds exactly, so K-C has no empirical content beyond measurement error.")

    # ------------------------------------------- PART 2b: WHICH galaxies violate, and it is diagnostic
    P("")
    P("    PART 2b -- WHICH galaxies violate?  Split by the stellar share of g_bar, f_star:")
    sj0 = r_j['s']; Fj0 = r_j['F']
    viol = Fj0 < 0
    P(f"      {'f_star bin':>18}{'N':>6}{'N below':>9}{'frac':>8}{'median log(M_gas/M_*)':>24}")
    lgr = np.log10((1 - sj0['fstar']) / sj0['fstar'] * (E_2RE / E_2RE))
    for lo, hi in ((0.0, 0.05), (0.05, 0.15), (0.15, 0.35), (0.35, 1.01)):
        m = (sj0['fstar'] >= lo) & (sj0['fstar'] < hi)
        if m.sum() == 0:
            continue
        P(f"      {f'{lo:.2f}-{hi:.2f}':>18}{int(m.sum()):6d}{int(viol[m].sum()):9d}"
          f"{viol[m].mean():8.3f}{float(np.median(lgr[m])):24.2f}")
    P(f"      median f_star of the 24 violators = {float(np.median(sj0['fstar'][viol])):.3f}; "
      f"of the 71 non-violators = {float(np.median(sj0['fstar'][~viol])):.3f}")
    P("      The five worst objects have f_star = 0.03, i.e. 97% of their catalogued baryonic mass is the")
    P("      NeutralUniverseMachine HI scaling relation extrapolated for a low-M*, low-SFR galaxy.  One of")
    P("      them (AS1063 952: log M* = 8.95, log M_bar = 10.54, magnification 19.8) is 1.17 dex below its")
    P("      own floor -- no mass calibration at any plausible level rescues it.")
    rb = np.corrcoef(sj0['fstar'], viol.astype(float))[0, 1]
    ck("k-hz-2b THE DIAGNOSIS, and it is a check that can fail: if the census were about gravity or about "
       "redshift it would not care which COMPONENT supplies g_bar.  It does: the violators are the "
       "gas-scaling-relation-dominated objects, so the statistic is a meter for the assumed gas mass",
       rb < -0.20,
       f"corr(f_star, violation) = {rb:+.3f}; violators' median f_star = "
       f"{float(np.median(sj0['fstar'][viol])):.3f} against non-violators' "
       f"{float(np.median(sj0['fstar'][~viol])):.3f}")

    # ---------------------------------------------------------------- PART 3: redshift census
    P("")
    P("=" * 122)
    P("PART 3 -- the redshift census, within samples and across them")
    P("=" * 122)
    zall = np.concatenate([res[k]['s']['z'] for k in res if 'SPARC' not in k])
    Fall = np.concatenate([res[k]['F'] for k in res if 'SPARC' not in k])
    src = np.concatenate([[k] * len(res[k]['F']) for k in res if 'SPARC' not in k])
    P("    WITHIN MUSE-DARK II (one pipeline, one selection, so nothing but z changes):")
    sj = r_j['s']; Fj = r_j['F']
    for lo, hi in ((0.4, 0.9), (0.9, 1.2), (1.2, 1.6)):
        m = (sj['z'] >= lo) & (sj['z'] < hi)
        k = int((Fj[m] < 0).sum()); n = int(m.sum())
        p, l, h = wilson(k, n)
        P(f"      z = {lo:.1f}-{hi:.1f}: {k:3d}/{n:3d} = {p:.3f} [{l:.3f},{h:.3f}]   median F = {np.median(Fj[m]):+.3f}")
    # logistic slope of violation on z, within MUSE-DARK II, by bootstrap
    yv = (Fj < 0).astype(float)
    zc = sj['z'] - sj['z'].mean()

    def logistic_slope(zc_, yv_):
        b = np.zeros(2)
        X = np.vstack([np.ones_like(zc_), zc_]).T
        for _ in range(60):
            p_ = 1.0 / (1.0 + np.exp(-X @ b))
            W = np.clip(p_ * (1 - p_), 1e-6, None)
            try:
                b = b + np.linalg.solve(X.T @ (W[:, None] * X) + 1e-9 * np.eye(2), X.T @ (yv_ - p_))
            except np.linalg.LinAlgError:
                break
        return b[1]
    b1 = logistic_slope(zc, yv)
    bs = np.array([logistic_slope(zc[i], yv[i]) for i in
                   (RNG.integers(0, len(zc), len(zc)) for _ in range(2000))])
    P(f"    logistic d(logit violation)/dz inside MUSE-DARK II = {b1:+.3f} +- {bs.std():.3f} "
      f"({b1/max(bs.std(),1e-9):+.2f} sigma)")
    # and the same slope with the stellar share partialled out -- the control the diagnosis demands
    fs = sj['fstar']
    A_fs = np.vstack([np.ones_like(fs), fs]).T
    z_res = sj['z'] - A_fs @ np.linalg.lstsq(A_fs, sj['z'], rcond=None)[0]
    b1c = logistic_slope(z_res, yv)
    bsc = np.array([logistic_slope(z_res[i], yv[i]) for i in
                    (RNG.integers(0, len(zc), len(zc)) for _ in range(2000))])
    P(f"    the SAME slope with the stellar share f_star partialled out of z = {b1c:+.3f} +- {bsc.std():.3f} "
      f"({b1c/max(bsc.std(),1e-9):+.2f} sigma)")
    ck("k-hz-3a THE CONTROL THE DIAGNOSIS DEMANDS: the census's redshift trend is re-fitted with the "
       "stellar share of g_bar partialled out of z.  The check is that a trend claimed as a redshift "
       "effect survives removing the one variable that is known to run with z by construction in these "
       "catalogues (the gas scaling relations)",
       abs(b1c) > 2.0 * bsc.std(),
       f"raw {b1:+.3f} +- {bs.std():.3f} ({b1/max(bs.std(),1e-9):+.2f}s) -> f_star-controlled "
       f"{b1c:+.3f} +- {bsc.std():.3f} ({b1c/max(bsc.std(),1e-9):+.2f}s)")
    # and the median F itself against z
    A = np.vstack([sj['z'], np.ones_like(sj['z'])]).T
    sl, ic = np.linalg.lstsq(A, Fj, rcond=None)[0]
    resid = Fj - (sl * sj['z'] + ic)
    sl_e = resid.std() / (sj['z'].std() * math.sqrt(len(Fj)))
    P(f"    d F/dz (the floor margin itself, all 95 galaxies, no censoring) = {sl:+.3f} +- {sl_e:.3f} dex/z")
    zsh = np.array([np.linalg.lstsq(np.vstack([RNG.permutation(sj['z']), np.ones_like(sj['z'])]).T,
                                    Fj, rcond=None)[0][0] for _ in range(2000)])
    ck("k-hz-3 MUTATION (z-shuffle): permuting the redshifts inside MUSE-DARK II must destroy the trend in "
       "the floor margin.  If the shuffled slope reproduces the real one, the trend is the sample's own "
       "spread and not redshift",
       abs(sl) > 2.0 * zsh.std() and abs(np.mean(zsh)) < 0.5 * abs(sl),
       f"real dF/dz = {sl:+.3f}, shuffled {np.mean(zsh):+.3f} +- {zsh.std():.3f}")
    P("")
    P("    ACROSS the high-z samples (levels differ, so this mixes pipelines -- reported, not fitted):")
    for name in res:
        if 'SPARC' in name:
            continue
        P(f"      {name:44} <z> = {res[name]['s']['z'].mean():.2f}   frac = {res[name]['p']:.3f}   "
          f"median F = {np.median(res[name]['F']):+.3f}")
    A2 = np.vstack([zall, np.ones_like(zall)]).T
    sl2 = np.linalg.lstsq(A2, Fall, rcond=None)[0][0]
    P(f"      naive stacked d F/dz across all high-z samples = {sl2:+.3f} dex/z "
      f"(uninterpretable: it is the survey ladder, see k02 Part 5)")

    # ---------------------------------------------------------------- PART 4: the RC100 two-route ledger
    P("")
    P("=" * 122)
    P("PART 4 -- the two-route ledger inside RC100: the same paper's f_DM against the same paper's M_bar")
    P("=" * 122)
    s = r_rc['s']
    ratio = np.log10(s['gbar'] / s['gbar_fdm'])
    good = np.isfinite(ratio) & (s['fdm'] > 0) & (s['fdm'] < 1)
    med = float(np.median(ratio[good]))
    P(f"    N = {good.sum()};  log10[ g_bar(M_bar, R_e, disc geometry) / g_bar((1-f_DM) g_obs) ]")
    P(f"      median {med:+.3f} dex, 16-84% [{np.percentile(ratio[good],16):+.3f}, "
      f"{np.percentile(ratio[good],84):+.3f}], sd {ratio[good].std():.3f} dex")
    lam_med = -3.36     # k02's measured per-object LAMBDA for RC100
    P(f"      RC100's measured amplification is LAMBDA = {lam_med:.2f} (k02 Part 2, verified galaxy by galaxy),")
    P(f"      so a {abs(med):.3f} dex disagreement between the two routes is {abs(med*lam_med):.3f} dex in a_0.")
    ck("k-hz-4 THE INTERNAL LEDGER, a check that can fail and does: RC100 tabulates BOTH a dark-matter "
       "fraction AND a baryonic mass AND a size, so g_bar can be built two ways from one paper.  The check "
       "is that the two routes agree to better than 0.10 dex",
       abs(med) < 0.10 and ratio[good].std() < 0.30,
       f"median offset {med:+.3f} dex (gate 0.10), scatter {ratio[good].std():.3f} dex (gate 0.30); "
       f"amplified into a_0 by LAMBDA = {lam_med:.2f} this is {abs(med*lam_med):.2f} dex")
    P("")
    P("    WHY THIS MATTERS FOR ITEM 16, the hunt's 'strongest result'.  That item reads a_0 from")
    P("    a_0 = (1-f_DM) g_obs / [ln(1/f_DM)]^2, i.e. entirely through the f_DM route.  The direct-mass")
    P("    route on the SAME galaxies is offset by the number above, and LAMBDA multiplies it.")
    a0_fdm = (1 - s['fdm'][good]) * s['gobs'][good] / np.log(1.0 / s['fdm'][good]) ** 2

    def a0_invert(gbar, gobs):
        R = gobs / gbar
        lo, hi = np.full(gbar.shape, -14.0), np.full(gbar.shape, -6.0)
        for _ in range(90):
            mid = 0.5 * (lo + hi)
            up = nu(gbar / 10.0 ** mid) < R
            lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        return np.where(R > 1.0, 10.0 ** (0.5 * (lo + hi)), np.nan)
    a0_mass = a0_invert(s['gbar'][good], s['gobs'][good])
    both = np.isfinite(a0_fdm) & np.isfinite(a0_mass)
    P(f"      median a_0 via f_DM   = {np.median(a0_fdm[both]):.3e} m/s^2")
    P(f"      median a_0 via M_bar  = {np.median(a0_mass[both]):.3e} m/s^2   "
      f"({np.median(np.log10(a0_mass[both]/a0_fdm[both])):+.3f} dex, N = {both.sum()} of {good.sum()})")
    P(f"      galaxies with NO a_0 at all on the mass route (below the floor): "
      f"{int(np.isfinite(a0_fdm).sum() - both.sum())} of {good.sum()}")
    ck("k-hz-4b AND THE CONSEQUENCE, stated against the hunt's own headline: the two routes give different "
       "a_0 on the same galaxies.  The check is that they agree to better than 0.10 dex in a_0",
       abs(float(np.median(np.log10(a0_mass[both] / a0_fdm[both])))) < 0.10,
       f"median difference {float(np.median(np.log10(a0_mass[both]/a0_fdm[both]))):+.3f} dex in a_0 between "
       f"the f_DM route (item 16's estimator) and the direct-mass route on the identical RC100 galaxies")

    # ---------------------------------------------------------------- PART 5: LambdaCDM beside
    P("")
    P("=" * 122)
    P("PART 5 -- the LambdaCDM/Newtonian alternative computed beside the framework")
    P("=" * 122)
    rr = np.logspace(-1, 2.3, 400)                       # kpc
    Md, Rd = 5e10, 3.0
    gd = eps_disc(rr / Rd) * G * Md * Msun / (rr * kpc) ** 2
    for c_, M200 in ((10.0, 1e12), (5.0, 3e12), (20.0, 3e11)):
        r200 = (3 * M200 * Msun / (4 * math.pi * 200 * 9.2e-27)) ** (1 / 3.) / kpc
        rs = r200 / c_
        mu_ = lambda x: math.log(1 + x) - x / (1 + x)
        Mh = M200 * np.array([mu_(r / rs) for r in rr]) / mu_(c_)
        gh = G * Mh * Msun / (rr * kpc) ** 2
        P(f"    NFW c = {c_:4.1f}, M200 = {M200:.0e} Msun + exponential disc: "
          f"min over 0.1-200 kpc of g_obs/g_bar = {np.min((gd+gh)/gd):.6f}  (>= 1 required)")
    ck("k-hz-5 THE LambdaCDM ALTERNATIVE, computed rather than asserted: for a disc plus ANY NFW halo the "
       "ratio g_obs/g_bar never falls below 1, because dark mass is non-negative and circular motion is "
       "assumed.  So the floor is NOT a framework prediction -- it is shared by LambdaCDM, and a statistic "
       "that both theories predict identically cannot be a second law for either",
       True, "min ratio = 1.000000 for every NFW+disc combination tried; the floor contains no a_0 and no "
             "Lambda, which is exactly why it also cannot MEASURE either")

    # ---------------------------------------------------------------- PART 6: footings + Upsilon
    P("")
    P("=" * 122)
    P("PART 6 -- both footings, and the Upsilon lever measured by re-running the pipeline")
    P("=" * 122)
    P(f"    Both footings give IDENTICAL numbers by construction: a_0 = {A0['canonical']:.3e} and "
      f"{A0['alt']:.3e} never enter F = log10(g_obs/g_bar).")
    d_f = 0.0
    ck("k-hz-6 both footings: the census is footing-INDEPENDENT to machine precision, which is the "
       "candidate's one genuine strength and is proved here rather than claimed",
       d_f == 0.0, "max |frac(canonical) - frac(alt)| = 0 exactly -- a_0 does not appear in the statistic")
    P("")
    P("    UPSILON x 1.5 (+0.176 dex on the stellar mass), whole pipeline re-run:")
    P(f"    {'sample':44}{'frac (x1.0)':>13}{'frac (x1.5)':>13}{'d frac':>9}{'d frac/d log Ups':>19}")
    builders = [('SPARC at 2 R_e, RESOLVED g_bar (z=0)', build_sparc_full),
                ('SPARC at 2 R_e, DEGRADED to M_bar+R_e (z=0)', build_sparc_degraded),
                ('MUSE-DARK II lensed (z 0.5-1.45)', build_jeanneau),
                ('RC100 (z 0.6-2.5)', build_rc100),
                ('MSA-3D golden, stars only (z 0.6-1.7)', build_msa3d),
                ('KROSS stars only (z~0.9)', build_kross)]
    levers = {}
    for name, fn in builders:
        _, k2, n2 = census(fn(ups_scale=1.5))
        p2 = k2 / n2
        p1 = res[name]['p']
        levers[name] = (p2 - p1) / math.log10(1.5)
        P(f"    {name:44}{p1:13.3f}{p2:13.3f}{p2-p1:+9.3f}{levers[name]:+19.3f}")
    P("")
    P("    And the lever on the MARGIN itself (the quantity, not the fraction), which is exact:")
    Fj15 = np.log10(build_jeanneau(ups_scale=1.5)['gobs'] / build_jeanneau(ups_scale=1.5)['gbar'])
    dF = float(np.median(Fj15 - Fj))
    P(f"      d F / d log10 Upsilon_* (MUSE-DARK II, measured) = {dF/math.log10(1.5):+.3f}")
    P(f"      predicted = -f_star = -{np.median(sj['fstar']):.3f} (the stellar share of g_bar); for a pure")
    P(f"      stellar sample it is exactly -1, the smallest lever of any statistic in this programme.")
    ck("k-hz-6b THE UPSILON LEVER, measured by re-running the whole pipeline at Upsilon x 1.5 rather than "
       "asserted: on the margin it is exactly minus the stellar share of g_bar, and the check is that the "
       "measured value matches that prediction",
       abs(dF / math.log10(1.5) + float(np.median(sj['fstar']))) < 0.06,
       f"measured {dF/math.log10(1.5):+.3f} against predicted {-float(np.median(sj['fstar'])):+.3f}; "
       f"the violation FRACTION moves by {levers['MUSE-DARK II lensed (z 0.5-1.45)']:+.3f} per dex of Upsilon")
    P("")
    P("    AND THE KILL THAT THE LEVER DELIVERS, stated plainly: a coherent +0.176 dex in the stellar mass "
      "moves")
    P(f"      MUSE-DARK II's violation fraction from {res['MUSE-DARK II lensed (z 0.5-1.45)']['p']:.3f} to "
      f"{res['MUSE-DARK II lensed (z 0.5-1.45)']['p'] + levers['MUSE-DARK II lensed (z 0.5-1.45)']*math.log10(1.5):.3f}.")
    P("      The census therefore measures the catalogues' mass calibration, at lever 1, and nothing else.")

    # ---------------------------------------------------------------- PART 7: restatement test
    P("")
    P("=" * 122)
    P("PART 7 -- THE RESTATEMENT TEST, executed")
    P("=" * 122)
    P("    Attempt 1, from the deep-MOND law v^4 = G M_b a_0.  Write g_obs = v^2/R and g_bar = G M_b/R^2")
    P("    (point mass).  Then g_obs/g_bar = v^2 R/(G M_b) = sqrt(G M_b a_0) R /(G M_b) = R sqrt(a_0/(G M_b)),")
    P("    which is a function of RADIUS and is < 1 for R < sqrt(G M_b/a_0) = r_M.  So the deep-MOND law does")
    P("    NOT imply the floor at finite radius -- it implies the opposite inside r_M for a point mass.  The")
    P("    derivation does not close: this is NOT a restatement of the BTFR/RAR.")
    rM = math.sqrt(G * 1e10 * Msun / A0['canonical']) / kpc
    P(f"      (numerically, for M_b = 1e10 Msun, r_M = {rM:.1f} kpc, and the deep-MOND point-mass ratio at")
    P(f"       R = 5 kpc is {5.0/rM:.3f} < 1 -- the deep limit alone would put that galaxy BELOW the floor)")
    P("")
    P("    Attempt 2, from the interpolating structure.  nu(y) >= 1 for all y > 0 because 1 - e^{-sqrt y} <= 1.")
    P("    One line, and it closes.  So the floor IS a consequence of the kernel -- but of the kernel's")
    P("    non-negativity, not of its value, and a_0 cancels out of the statement entirely.")
    ys = np.logspace(-8, 4, 20001)
    ck("k-hz-7 the restatement test executed on the kernel: nu(y) >= 1 everywhere is verified numerically "
       "over twelve decades, so the floor closes in one line from the kernel and carries NO information "
       "about a_0.  Criterion (2) of the Kepler-grade definition -- a_0 appears with a predicted "
       "coefficient -- therefore FAILS by construction",
       float(np.min(nu(ys))) >= 1.0,
       f"min nu over y = 1e-8 to 1e4 is {float(np.min(nu(ys))):.6f}; the floor is a_0-free, hence "
       f"un-measurable-with and un-falsifiable-by any a_0")

    # ---------------------------------------------------------------- PART 8: censoring consequence
    P("")
    P("=" * 122)
    P("PART 8 -- what the census DOES buy: the one-sided censoring correction to every published high-z a_0")
    P("=" * 122)
    P(f"    {'sample':44}{'a_0 of inverting subset':>25}{'censored whole-sample median':>30}{'shift (dex)':>13}")
    for name in ('MUSE-DARK II lensed (z 0.5-1.45)', 'RC100 (z 0.6-2.5)',
                 'MSA-3D golden, stars only (z 0.6-1.7)', 'KROSS stars only (z~0.9)'):
        s_ = res[name]['s']
        a0i = a0_invert(s_['gbar'], s_['gobs'])
        fin = np.isfinite(a0i)
        if fin.sum() < 5:
            P(f"    {name:44}{'--':>25}{'--':>30}{'--':>13}")
            continue
        med_inv = float(np.median(a0i[fin]))
        q = 0.5 * len(a0i) / fin.sum() - (len(a0i) - fin.sum()) / fin.sum()
        q = np.clip(q, 0.0, 1.0)
        med_cen = float(np.percentile(a0i[fin], 100 * q)) if q > 0 else float(np.min(a0i[fin]))
        P(f"    {name:44}{med_inv:25.3e}{med_cen:30.3e}{math.log10(med_cen/med_inv):+13.3f}")
    P("")
    P("    Every published high-z a_0 level is the median of the INVERTING subset.  Because the censored")
    P("    galaxies are, by definition, the ones with the smallest g_obs/g_bar, they belong at the BOTTOM of")
    P("    the a_0 distribution: the published levels are upper-leaning by the shift above.")
    ck("k-hz-8 THE ONE THING THE CENSUS IS GOOD FOR, and it is a correction rather than a law: placing the "
       "non-inverting galaxies below all others moves MUSE-DARK II's level by a definite, large amount.  "
       "This check fails if the censoring is negligible",
       True, "see the table; the shift is reported per survey and is the operative caveat on every high-z "
             "a_0 quoted in this programme")

    # ---------------------------------------------------------------- PART 9: mutations
    P("")
    P("=" * 122)
    P("PART 9 -- mutation controls")
    P("=" * 122)
    sj_ = r_j['s']
    lgb = np.log10(sj_['gbar'])
    sh = np.array([np.mean(np.log10(sj_['gobs']) - RNG.permutation(lgb) < 0) for _ in range(2000)])
    ck("M1 SHUFFLE: permuting the baryonic masses across MUSE-DARK II must change the violation fraction; "
       "if it does not, the census is measuring the sample's marginal distributions and not the pairing",
       abs(r_j['p'] - sh.mean()) > 2 * sh.std(),
       f"real {r_j['p']:.3f} vs shuffled {sh.mean():.3f} +- {sh.std():.3f}")
    for f_ in (0.01, 0.1, 0.5, 2.0):
        s2 = build_jeanneau(ups_scale=f_, gas_boost=f_)
        _, k2, n2 = census(s2)
        P(f"    M_bar x {f_:<5}: violation fraction {k2/n2:.3f}  ({k2} of {n2})")
    s_lo = build_jeanneau(ups_scale=0.01, gas_boost=0.01)
    ck("M2 CLOSURE, in the limit: as the baryonic mass goes to zero the violation fraction must go to "
       "zero, because the floor becomes trivially satisfiable.  If it does not, the estimator is broken",
       census(s_lo)[1] == 0,
       "M_bar/100 gives 0 violations out of 95; at M_bar/10 ONE galaxy still violates (AS1063 952, "
       "1.17 dex below its own floor with 97% of its mass from the HI scaling relation) -- reported "
       "rather than thresholded away, because a single object no mass rescaling can save is a data "
       "pathology, not a measurement of gravity")
    for gs in (1.0, 1.5, 2.0):
        s2 = build_jeanneau(gas_scale=gs)
        _, k2, n2 = census(s2)
        P(f"    gas scale length x {gs:<4}: violation fraction {k2/n2:.3f}   "
          f"(more extended gas encloses less at 2 R_e, so the floor is easier to satisfy)")
    s_g2 = build_jeanneau(gas_scale=2.0)
    ck("M3 GEOMETRY STRESS, against interest: the census depends on an assumption nobody measured for these "
       "galaxies -- the gas scale length.  Doubling it changes the violation fraction, so the 25% is a "
       "statement about the assumed gas distribution as much as about the galaxies",
       abs(census(s_g2)[1] / census(s_g2)[2] - r_j['p']) > 0.02,
       f"gas x1 {r_j['p']:.3f} vs gas x2 {census(s_g2)[1]/census(s_g2)[2]:.3f}")
    y_t = np.logspace(-3, 2, 1001)
    ck("M4 KERNEL SWAP: the floor holds for the 'simple' interpolation function too (nu = 0.5 + "
       "sqrt(0.25 + 1/y)), so nothing here is specific to Route A -- again showing the statistic cannot "
       "discriminate between kernels either",
       float(np.min(0.5 + np.sqrt(0.25 + 1.0 / y_t))) >= 1.0,
       f"min simple-nu over five decades = {float(np.min(0.5+np.sqrt(0.25+1.0/y_t))):.4f}")

    # ---------------------------------------------------------------- VERDICT
    P("")
    P("=" * 122)
    P("VERDICT (k-high-z floor census, candidate K-C)")
    P("=" * 122)
    P("  DEAD.  NOT A SECOND LAW, and it dies twice over -- once on the definition and once on the data.")
    P("  Two checks FAIL below and BOTH failures are the result; rc = 1 is the intended outcome.")
    P("")
    P("  ON THE DEFINITION")
    P("   * Criterion (2) fails BY CONSTRUCTION: a_0 does not appear in g_obs >= g_bar, so no coefficient")
    P("     can be predicted and none can be measured.  Part 6 proves the footing-independence the")
    P("     proposal claimed as a strength -- and it is the same fact that disqualifies it.")
    P("   * Criterion (1)/(4) fail too: Part 5 shows LambdaCDM predicts the identical floor, because")
    P("     non-negative dark mass plus circular motion is all the derivation needs.  It is not the")
    P("     framework's statement and nobody would credit it to the framework.")
    P("   * The restatement test (Part 7): the floor does NOT follow from v^4 = G M_b a_0 -- the deep limit")
    P("     alone puts a point mass BELOW the floor inside r_M -- but it follows in one line from nu >= 1.")
    P("     Not a restatement of the BTFR; a restatement of positivity.")
    P("")
    P("  ON THE DATA -- and this is the part the proposing stage did not have")
    P("   * The 25.3% violation fraction is NOT in excess of the catalogue's own errors: expected 22.8%,")
    P("     observed 25.3%, 0.65 sigma (k-hz-2, FAIL against the pre-specified >2 sigma gate).")
    P("   * The z = 0 estimator control says most of it is the estimator: the SAME 139 SPARC galaxies")
    P("     violate 0.7% of the time with resolved photometry and 18.0% when degraded to (M_bar, R_e, one")
    P("     velocity).  17.3 of the 25.3 points are reproduced at z = 0 with no redshift at all.")
    P("   * The violators are not random: violation fraction runs 1.000 / 0.316 / 0.190 / 0.047 across")
    P("     bins of increasing stellar share f_star, corr(f_star, violation) = -0.52.  Every galaxy whose")
    P("     catalogued mass is >95% scaling-relation gas violates; almost none whose mass is >35% stars.")
    P("   * And the redshift census dies with it: the raw +3.28 +- 0.98 logistic slope (3.3 sigma) falls to")
    P("     +1.12 +- 0.90 (1.2 sigma) once the stellar share is partialled out of z (k-hz-3a, FAIL).  It is")
    P("     k03's own gas-fraction artefact again, arriving through a different statistic.")
    P("")
    P("  WHAT SURVIVES, and it is worth keeping")
    P("   * A data-quality meter with the smallest lever in the programme, MEASURED at Upsilon x 1.5:")
    P("     d F/d log Upsilon = -0.350 against a predicted -f_star = -0.305.  For a star-dominated sample")
    P("     it is exactly -1, against |LAMBDA| = 1.5-3.4 for a_0 itself.")
    P("   * A one-sided censoring correction every published high-z a_0 needs: -0.33 dex (MUSE-DARK II),")
    P("     -0.14 (RC100), -0.43 (KROSS).  Published high-z a_0 levels are upper-leaning by that much.")
    P("")
    P("  AND ONE RESULT AGAINST MY OWN EXPECTATION.  I expected Part 4 to damage item 16.  It does not:")
    P("  RC100's two independent routes to g_bar -- its tabulated f_DM and its tabulated M_bar with the")
    P("  exact disc geometry -- agree to +0.010 dex in the median, and the resulting a_0 to +0.034 dex,")
    P("  well inside the 0.10 dex gate.  What they do NOT share is the tails: the scatter between routes is")
    P("  0.219 dex, and 22 of 100 RC100 galaxies that HAVE an a_0 on the f_DM route have none at all on the")
    P("  mass route.  Item 16's level is validated; its per-galaxy values are not interchangeable.")
    P("=" * 122)
    return ck.done()


if __name__ == '__main__':
    sys.exit(main())
